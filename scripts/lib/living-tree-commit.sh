#!/usr/bin/env bash
# living-tree-commit.sh — Plan 07 race-protected commit helper.
#
# Captures the kronika 2026-04-16/17 incident learning: under parallel
# agent activity in a Living Tree checkout, `git commit --only path...`
# is NOT atomic versus another agent's commit running in the same instant
# — message of one commit can end up under the envelope of another's tree.
#
# This helper wraps the standard "stage these files + commit with this
# message" pattern with three race-detection primitives:
#
#   1. HEAD shift detection — capture HEAD before staging, compare against
#      the parent of the new commit afterwards.
#   2. Staged-tree fingerprinting — `git write-tree` before committing,
#      compare against the new commit's tree.
#   3. Foreign-file detection — list files in the new commit's diff vs
#      its parent and assert the set is exactly the set we staged.
#
# On race: print diagnostic with both SHAs + foreign files, leave the
# commit in place (operator decides), exit nonzero.
#
# Usage:
#   scripts/lib/living-tree-commit.sh "commit message" -- path1 path2 ...
#
# This script is intentionally append-only: it never amends, never rebases,
# never force-pushes. Recovery on race is operator-driven.

set -euo pipefail

# ----- argument parsing -------------------------------------------------------

if [[ $# -lt 3 ]]; then
    cat >&2 <<'USAGE'
usage: living-tree-commit.sh "<commit message>" -- <file> [<file>...]

Race-protected commit helper for VetCoders Living Tree workflow.

Captures pre-flight HEAD, stages only the named files, commits with the
given message, then verifies no concurrent agent commit interleaved between
stage and commit.

Exits nonzero on race; the racing commit is left in place for operator
review (no auto-rebase, no auto-reset).
USAGE
    exit 2
fi

MESSAGE=$1
shift

if [[ $1 != "--" ]]; then
    echo "living-tree-commit: expected '--' after message, got '$1'" >&2
    exit 2
fi
shift

if [[ $# -lt 1 ]]; then
    echo "living-tree-commit: at least one file path required after '--'" >&2
    exit 2
fi

FILES=("$@")

# ----- preflight --------------------------------------------------------------

if ! git rev-parse --git-dir >/dev/null 2>&1; then
    echo "living-tree-commit: not inside a git working tree" >&2
    exit 2
fi

# Disallow path arguments that look like add-everything sugar, per kronika
# safety doctrine (never `git add -A`, never `git add .`).
for f in "${FILES[@]}"; do
    case "$f" in
        "."|"-A"|"--all"|"-a")
            echo "living-tree-commit: refusing wildcard/all-files argument '$f' — name files explicitly" >&2
            exit 2
            ;;
    esac
done

# Pre-flight HEAD. Empty if the repo has no commits yet.
PRE_HEAD=$(git rev-parse --verify HEAD 2>/dev/null || echo "")

# ----- stage ------------------------------------------------------------------

git add -- "${FILES[@]}"

# Fingerprint the index we are about to commit. Even on an empty repo this
# returns a tree (the empty tree, possibly).
STAGED_TREE=$(git write-tree)

# Snapshot the set of paths that should appear in the resulting commit.
# Use --cached because we have just staged. Limit to our path args to
# tolerate other staged files left over from operator interaction (they
# would also become foreign-file evidence below).
mapfile -t STAGED_FILES < <(
    git diff --cached --name-only -- "${FILES[@]}" | LC_ALL=C sort -u
)

if [[ ${#STAGED_FILES[@]} -eq 0 ]]; then
    # Nothing actually changed in the named files. Nothing to commit. Treat
    # as success — running this twice in a row should not error noisily.
    echo "living-tree-commit: no staged changes for: ${FILES[*]} (nothing to commit)"
    exit 0
fi

# ----- commit -----------------------------------------------------------------

# Use `git commit --only` semantics by passing the paths. This commits ONLY
# the index entries for those paths, ignoring any unrelated staged work in
# the parent's index. That is exactly the safety we want under Living Tree.
COMMIT_STDERR=$(mktemp)
trap 'rm -f "$COMMIT_STDERR"' EXIT
if ! git commit -m "$MESSAGE" --only -- "${FILES[@]}" 2>"$COMMIT_STDERR"; then
    cat "$COMMIT_STDERR" >&2
    echo "living-tree-commit: git commit failed — leaving worktree as-is" >&2
    exit 1
fi

NEW_HEAD=$(git rev-parse --verify HEAD)
NEW_TREE=$(git rev-parse --verify "${NEW_HEAD}^{tree}")

# Parent of the new commit. If the repo had no commits pre-flight, the new
# commit is a root commit and has no parent.
if ! NEW_PARENT=$(git rev-parse --verify "${NEW_HEAD}^" 2>/dev/null); then
    NEW_PARENT=""
fi

# Files actually present in the new commit. For non-root commits git
# diff-tree -r implicitly diffs against the parent; for root commits we
# fall back to listing the tree's full file set.
if [[ -n "$NEW_PARENT" ]]; then
    mapfile -t COMMIT_FILES < <(
        git diff-tree --no-commit-id --name-only -r "$NEW_HEAD" | LC_ALL=C sort -u
    )
else
    mapfile -t COMMIT_FILES < <(
        git ls-tree -r --name-only "$NEW_HEAD" | LC_ALL=C sort -u
    )
fi

# ----- race detection ---------------------------------------------------------

race_reasons=()

# (a) HEAD shift: pre-flight HEAD must equal the parent of the new commit
# (or both empty for the root-commit case).
if [[ "$PRE_HEAD" != "$NEW_PARENT" ]]; then
    race_reasons+=("HEAD moved during commit: pre=${PRE_HEAD:-<root>} parent-of-new=${NEW_PARENT:-<root>}")
fi

# (b) Staged-tree mismatch: the tree we staged before committing must equal
# the tree of the new commit. If another agent's commit landed in between
# and somehow our message latched onto their tree, this catches it.
if [[ "$STAGED_TREE" != "$NEW_TREE" ]]; then
    race_reasons+=("tree-hash mismatch: staged=$STAGED_TREE committed=$NEW_TREE")
fi

# (c) Foreign-file detection: every file in the commit's diff must be in
# our staged-files snapshot. Anything extra is foreign content riding on
# our commit message.
foreign_files=()
declare -A staged_lookup=()
for f in "${STAGED_FILES[@]}"; do
    staged_lookup["$f"]=1
done
for f in "${COMMIT_FILES[@]}"; do
    if [[ -z "${staged_lookup[$f]:-}" ]]; then
        foreign_files+=("$f")
    fi
done
if [[ ${#foreign_files[@]} -gt 0 ]]; then
    race_reasons+=("foreign files in commit: ${foreign_files[*]}")
fi

if [[ ${#race_reasons[@]} -eq 0 ]]; then
    echo "living-tree-commit: clean commit $NEW_HEAD (${#STAGED_FILES[@]} file(s))"
    exit 0
fi

# ----- race diagnostic --------------------------------------------------------

{
    echo "living-tree-commit: RACE DETECTED on commit $NEW_HEAD"
    echo "  pre-flight HEAD : ${PRE_HEAD:-<root>}"
    echo "  new commit      : $NEW_HEAD"
    echo "  new parent      : ${NEW_PARENT:-<root>}"
    echo "  staged tree     : $STAGED_TREE"
    echo "  committed tree  : $NEW_TREE"
    for reason in "${race_reasons[@]}"; do
        echo "  - $reason"
    done
    echo
    echo "Recovery options (operator decides — no auto-rewrite):"
    echo "  A) git reset HEAD~1 && git stash --include-untracked \\"
    echo "       && git pull --rebase && git stash pop && rerun helper"
    echo "  B) leave the commit in place and document the race in the"
    echo "     marble report so the next agent can reason about lineage"
} >&2

exit 3
