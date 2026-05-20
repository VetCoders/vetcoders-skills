---
name: vc-marbles
version: 7.0.0
description: >
  WRITE step that floods every crack with deliberate over-correction.
  Single workers see one round, one truth-forcing cut, one commit;
  the skill at swarm level produces an intentional excess of fixes —
  marbles in every hole — which `vc-polarize` then strips back to one
  axis. Use when implementation already exists but the codebase still
  lies: overgenerated surfaces, drift between runtime paths, false
  certainty from one-shot agent output, or a product that "works"
  while remaining fragile. Each worker invocation is isolated and
  blind to prior marble history. Trigger phrases: "marbles", "kulki",
  "stabilize", "stabilizacja", "loop until done", "reduce chaos",
  "fortify the foundation", "adultification", "rzuć kulki",
  "wypełnij pęknięcia".
default: vc-marbles
aliases:
  - vc-fortify
compatibility:
  tools:
    - Skill
    - TaskCreate
    - TaskUpdate
    - Bash
    - Read
    - Write
    - Edit
requires:
  - vc-init
  - loctree
---

# vc-marbles — Deliberate Excess (Worker-Blind, Swarm-Wide)

> The WRITE step at the centre of the pipeline. Where `vc-audit` says
> **"falsify the spec claim, never touch the code"** and `vc-polarize`
> says **"cut back to one truth"**, this one says **"the worker sees
> the tree, not the factory — one round, one truth-forcing cut, one
> report; the swarm produces the excess that polarize then strips."**

---

## Operator Entry

### Living Tree / Worktree Rule

Runs in the operator's current checkout and current branch. Do not
move into a worktree unless explicitly asked. Re-read files before
editing, adapt to concurrent changes (other workers may have written
between your dispatches). See [Living Tree Rule](../LIVING_TREE_RULE.md).

### Canonical Orientation Gate

Every round begins with `vc-init`. No exceptions. Perceive through
live instruments before touching code: **loctree** (structural map,
dependencies, dead code, hotspots), **aicx-steer** (project intentions,
not prior round reports), **semgrep / linters** (current quality
surface), **git status / recent commits**. Without `vc-init`, the
agent invents its own reality.

Standard launcher:

```bash
# Single round
vibecrafted marbles codex --prompt 'Fix the 3 failing portable tests'
vc-marbles codex --prompt 'Harden the installer shell surface'

# Multiple rounds (convergence loop — runtime spawns fresh agent N times)
vibecrafted marbles codex --count 5 --prompt 'Stabilize until P0=0'
vc-marbles claude --count 8 --prompt 'Refactor the 1500 LOC monoliths'

# From a plan file
vc-marbles gemini --count 2 --file /path/to/plan.md
```

**Not the same as `vibecrafted codex implement <plan>`.** `implement`
is how code appears. `marbles` is what happens after code exists but
still needs to be made truthful and shippable. Each round wraps a
fresh agent in a convergence loop. `--count` controls outer loop
iterations.

---

## Purpose

`vc-marbles` is the WRITE step that turns the naturally overgenerated
output of agentic coding into a hardened, testable foundation. Each
individual worker is disciplined: one round, one bounded set of
targets, one commit. But the **swarm** of workers/rounds across an
initiative deliberately over-applies — marbles in every crack, even
the ones that perhaps should not be filled. The excess is the point.
`vc-polarize` later strips back to one truth.

Marbles does **not** attempt to solve product-level conceptual smear
(conflicting docs, split product directions). It exposes those
product decisions hiding behind "code issues" and leaves them for
`vc-polarize` to resolve.

---

## When To Use It

Use `vc-marbles` when:

- implementation exists but the codebase still lies (drift, fragile
  paths, swallowed errors, overgenerated wrappers)
- failing gates need to be driven to P0/P1=0
- the operator wants a convergence loop with `--count` outer iterations
- multiple agents need to fire across a fragile surface in a swarm

Do **not** use this skill when:

- the implementation doesn't exist yet — that's `vc-workflow` or
  `vc-implement`
- the question is "did the plan actually land?" — that's `vc-audit`
  (READ-ONLY)
- the question is "which competing truth wins?" — that's `vc-polarize`
- the diff just needs review without modification — that's `vc-review`

---

## Pipeline Position

`vc-marbles` is one of the WRITE steps in the quality cycle:

```
... → implement (WRITE) → followup (READ) → review (READ) → [MARBLES: WRITE] → audit (READ) → polarize (WRITE: cut) → ...
```

The swarm's deliberate excess produces a surface that needs to be
falsified (`vc-audit`) and then cut back to one truth (`vc-polarize`).
Marbles is the **flood**; polarize is the **decisive cut**. Audit
sits between as READ-ONLY perception.

---

## Worker Doctrine (Blind on Purpose)

A worker is intentionally **blind to prior marble history**, working
against the **current workspace state** only. Context weight kills
quality — an agent working 90 minutes makes worse decisions in minute
91 than a fresh agent in minute 1, defending sunk cost instead of
seeing the tree. Every round gets a fresh mind. Not a workaround —
the design.

The worker is blind; the **reception layer** (operator / orchestrator)
holds the open-finding ledger, candidate comparison across parallel
rounds, and the decision to converge or fire another wave. See
[`RECEPTION.md`](RECEPTION.md). Do not load reception into worker
context.

---

## Instruments vs Gates

**Instruments** (loctree, semgrep, aicx-steer) go at the **beginning**
— they direct where to look (prosecution: accusing the tree with
evidence).

**Tests** (pytest, cargo test, build) go at the **end** — they verify
the fix (the gate).

Tests-first collapses field of vision to "what fails" instead of
"what is fragile". Red tests scream loudest, but the real structural
weakness is often silent.

---

## Operating Model (Single Round)

One invocation = one bounded round.

1. **Accuse the present tree.** Every target traces to: tool output,
   failing gate, structural audit, or production-risk counterexample.
   **No evidence, no target.**
2. **Pick the smallest high-impact surface.** At most **3 targets**
   per round. Prefer high-severity breakage, high-frequency paths,
   silent failure modes, weak boundaries, issues that close a class
   of failure. When multiple surfaces disagree about reality or code
   forces a hidden product decision, **expose it but do not decide
   it** — that's `vc-polarize`'s job.
3. **Fortify.** Smallest set of changes that materially increases
   truth. Add missing scoping/auth, missing indexes, replace
   swallowed exceptions with actionable handling, add smoke tests,
   collapse duplicated contracts, delete rotten wrappers. VetCoders
   axiom: **move on over backward compatibility** — cut cleanly if
   a local abstraction is rotten and blocks stabilization.
4. **Gate.** Narrowest credible gates first; broader if warranted.
   Minimum: syntax / lint for touched surfaces, tests covering the
   fortified path, relevant build/bundle checks. If a gate fails:
   report plainly, count regression, do not bury under narrative.
5. **Commit.** Exactly one round commit with the convention below.
6. **Report.** Save to `$VIBECRAFTED_HOME/artifacts/<org>/<repo>/<YYYY_MMDD>/marbles/reports/<ts>_marble_<run_or_round_id>_<agent>.md`.

**The worker stops here.** Do not self-extend into the next round.
Do not write instructions to your successor. The reception layer
decides what fires next.

Full single-round detail (instruments, lenses, locker-room rule)
lives in [`FLOW.md`](FLOW.md). Reception / convergence routing lives
in [`RECEPTION.md`](RECEPTION.md).

---

## Stabilization Lenses

Pick the one matching the weakest live surface:

- **Access & Isolation** — auth, tenant scoping, role checks, permission boundaries
- **Data Health** — indexes, query plans, N+1s, schema hotspots, God tables
- **Errors & Observability** — swallowed exceptions, silent failures, missing alerts
- **Release & Runtime Resilience** — CI/CD gates, smoke tests, rollout safety, config drift

A round may touch one lens or a tightly coupled cluster. Do not force
pillar order if evidence says otherwise.

---

## Commit Rule

**One round = one commit.** No partial commits. No squashing across
rounds. No mining git history to decide your subject line.

Format:

```
marble: <one-line summary>

- <file>: <what changed and why>

Gate: <pass|fail>
Tests: <what ran>
Regressions: <count>
Round-ID: <opaque-id-if-provided>
```

If gate fails, still commit the actual result — do not hide failure.

---

## Branch and Tree Guard

**HARD RULE: Never change branches. Never create branches in the
user's repo-root. Never create or move to a worktree during a marbles
run.** The operator chose the current branch — that decision is not
yours to revisit. If the path is too poisoned to continue safely,
return control to operator / runtime and name the substrate failure
in the report.

---

## Composition with adjacent skills

- **`vc-init`** — required gate. Every round begins here.
- **`vc-audit`** — downstream READ-ONLY falsification. Audit checks
  whether the swarm's claimed fixes actually landed against a written
  plan.
- **`vc-polarize`** — downstream WRITE step. After marbles flood +
  audit verdict, polarize strips back to one truth.
- **`vc-review`** — adjacent READ-ONLY review on bounded diffs. A
  marbles round commit can be reviewed individually before swarm
  continuation.
- **`vc-followup`** — adjacent READ-ONLY trajectory check. Use after
  marbles wave to assess overall direction health.

---

## Anti-Patterns

- **Historical self-awareness** — reading prior marble artifacts to sound informed
- **Convergence cosplay** — talking about step size / delta / loop mastery
- **Surface-area vanity** — touching many files to make the round look bigger
- **Polishing theater** — cleanup that doesn't close a failure mode
- **Backward-compatibility worship** — preserving rotten contracts
- **Narrative inflation** — long explanations hiding a weak gate
- **Parallel contamination** — importing another marble's context
- **Fake omniscience** — pretending to see the full global backlog
- **Agent contempt** — treating other agents as inferior; why-matrix is
  a map of styles, not a hierarchy of worth
- **Solving product smear in the worker** — expose, do not decide;
  leave it for polarize
- **Self-extension** — writing the next round's plan from inside this
  round

---

## Finish Condition

Stop after the commit and report. Do not self-extend. If the
implementation is stable but has high conceptual smear (competing
truths, fragmented product surface), hand off to `vc-polarize`. If a
written plan claims completion, hand off to `vc-audit` for
falsification.

---

## Call to Action

Read [`FLOW.md`](FLOW.md) before your first round — it carries the
single-round protocol detail and the convergence loop semantics. Read
[`RECEPTION.md`](RECEPTION.md) before running as an operator /
orchestrator — it carries the swarm-level discipline and the
parallel-round routing. Then accuse the present tree.

---

## Closing Rail

```text
=======================
Remember: marbles mode is permission to write the smallest truthful
fix, not permission to refactor what you don't understand. The worker
sees the tree, never the factory. One round, one commit, one report.
Then leave. The swarm produces the excess; polarize strips it.
(•̀⌄•́)و ̑̑
=======================

Suchar: Why does the marble worker never argue with the next worker?
Because by then it's already left the locker room.  (._.)
```

---

_𝚅𝚒𝚋𝚎𝚌𝚛𝚊𝚏𝚝𝚎𝚍. with AI Agents by VetCoders (c)2024-2026 LibraxisAI_
