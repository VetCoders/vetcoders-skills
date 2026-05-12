# Living Tree Rule

VetCoders work in one shared repository checkout.

Vibecrafted workflows do **not** create, switch to, or move work into git
worktrees by default. Worktrees are not a harmless implementation detail here:
they split runtime truth, hide concurrent edits, multiply merge surfaces, and
turn fast Vibecraftsmanship into branch archaeology.

## Hard Rule

- Work in the current checkout and current branch.
- Do not run `git worktree add`, create a side checkout, or relocate execution
  into another lane.
- Do not switch branches during active workflow execution.
- Do not create branches unless the operator explicitly asks for that git move.
- Re-read files before editing when time has passed or concurrent agents may be
  active.
- Treat local changes as shared work. Never stash, discard, reset, or overwrite
  changes you did not make.

## Only Exception

A worktree is allowed only when the operator explicitly says to use a worktree.
Generic requests like "isolate this", "work in parallel", "make a clean branch",
or "avoid conflicts" are not enough.

If the current substrate is too poisoned to continue safely, stop and report the
substrate failure. Do not solve substrate invalidity by escaping into a worktree.

## Why

Vibecrafting optimizes for rapid convergence on runtime truth. The pace is the
point. We do not move that fast so that a stale side tree can later force the
team into rebase drift, duplicate conflict repair, or backwards motion.

Training-data defaults about worktrees are subordinate to this repository
doctrine.

## Race-protection helper (added 2026-05-12, Plan 07)

Living Tree disciplines parallel work but does not by itself make
`git commit --only path1 path2` atomic against another agent's
simultaneous commit on the same branch. Kronika 2026-04-16/17 captured the
exact failure mode: under concurrent activity, one agent's commit message
can land under another agent's tree envelope.

Plan 07 ships a reusable primitive that detects this race after the fact
and refuses to silently accept the unsafe commit.

**Operator-facing entry point**:

```
make commit-safe MSG="<commit message>" FILES="path1 path2 ..."
```

**Direct shell invocation**:

```
scripts/lib/living-tree-commit.sh "<commit message>" -- path1 path2 ...
```

The helper captures pre-flight `HEAD`, stages only the named files, snapshots
the staged tree, then commits. After the commit it cross-checks three
invariants:

1. The new commit's parent equals the pre-flight `HEAD` (no concurrent
   commit slipped in via ref update).
2. The new commit's tree matches the staged-tree fingerprint (no foreign
   index mutation rode in on the commit).
3. The set of files changed by the commit matches the staged-files
   snapshot exactly (no foreign files in the envelope).

On race the helper prints both commit SHAs plus the foreign-file list,
offers two operator-driven recovery options, and exits nonzero. It does
**not** auto-amend, auto-reset, or auto-rebase. Recovery is intentionally
operator-driven, consistent with the rest of this rule.

The helper enforces the existing safety rule against wildcard staging:
arguments like `.`, `-A`, `--all`, `-a` are rejected. Name the files.

Verification:

```
make test-race-protection
```

The test suite at `tests/race_protection_test.sh` exercises both the
clean-commit path and two synthetic race injections (concurrent ref update
and foreign-index mutation).
