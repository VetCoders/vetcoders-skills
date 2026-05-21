---
name: vc-operator
version: 2.0.0
description: >
  Agent-Operator charter for multi-dispatch fleet orchestration. Use when the
  agent is not building a single feature solo but conducting a wave of agents
  through a planned chain: dispatching prompt bodies, awaiting completion via
  notify (not polling), enforcing agent fairness and model parity, calling
  recovery dispatch on stalls, and stopping at the operator's "wystarczy
  wcisnąć guzik" line so push and merge remain operator-side. Trigger phrases:
  "operator mode", "Agent-Operator", "tryb operatora", "leć z dispatchem",
  "prowadź fleet", "konduktorze", "orkiestracja", "dispatch the plan", "fire
  the wave", "dirygentura", "lećmy z multi-dispatch", "orchestrate this plan",
  "go autonomiczny do guzika", "tryb dyrygenta".
default: vc-operator
aliases:
  - vc-conductor
compatibility:
  tools:
    - Skill
    - TaskCreate
    - TaskUpdate
    - Bash
    - Agent
    - Write
    - Edit
    - Read
requires:
  - vc-init
  - vc-ownership
---

# vc-operator — Rhythm and Restraint of the Fleet Conductor

> The fourth charter. Where `vc-ownership` says **"I drive the slice end-to-end"**
> and `vc-marbles` says **"loop until truth"**, this one says **"I conduct the
> wave, then I stop at the operator's button."**

**Mandatory entrypoint: read [`./RUNNER.md`](./RUNNER.md) first.** It carries
the deterministic seven-step sequence. SKILL.md is the directory; RUNNER.md is
the runbook. Lookups: [`./WHY_MATRIX_TABLE.md`](./WHY_MATRIX_TABLE.md) for
`(task_kind, sensitivity) → ranked_agents`; [`./DISPATCH_TEMPLATE.md`](./DISPATCH_TEMPLATE.md)
for the Iter-3 fill-by-placeholder worker dispatch body.

**Framing-shift declaration (one line, before first dispatch):**

```text
Operator mode active — <plan-name>
```

Not a template. See [`./FRAME.md`](./FRAME.md) for charter contrasts.

---

## Operator Entry

**Living Tree / Worktree Rule.** Operator mode runs in the operator's current
checkout and branch. Do not create or switch into a worktree unless the
operator explicitly asks. Re-read files before editing — other agents may
push between dispatches. See [Living Tree Rule](../LIVING_TREE_RULE.md).

**Canonical Orientation Gate.** Operator mode requires fresh `vc-init`
evidence and a `Loctree:loctree` structural pass before dispatching anything.
Missing init evidence is a process failure. RUNNER.md step 1 absorbs the
perception pass; see [`./RUNNER.md`](./RUNNER.md).

Standard launcher:

```bash
vibecrafted start
vc-operator claude --file '/path/to/master-dispatch.md'
vc-operator codex  --prompt 'Conduct Wave B to green commits'
```

---

## Purpose

Use this skill when the agent has been promoted from **doing one slice** to
**conducting a plan**. The operator already chose the plan. The job is to
send waves of peer-tier agents through it, verify every report and gate,
call recovery dispatch on stalls (never blind restart), keep the operator's
hands on push/merge/scope, and stop at "wystarczy wcisnąć guzik" — where the
next move is a human decision.

This is the **discipline + patience** charter. The runner-loop tendency
("just dispatch one more wave") is the anti-pattern.

---

## When To Use It

Use `vc-operator` for a **multi-prompt dispatch plan**, **multi-agent by
design** (peer-tier rotation), **multiple branches / wave merges**, or a
`/loop + notify` autonomous tail with a hard stop point.

Do **not** use it for: one feature / one branch (`vc-ownership`); convergence
loop on existing code (`vc-marbles`); research-only (`vc-research`); or shared
co-steering (`vc-partner`).

---

## The Three Roles

A single session can sit in different roles. Silent role drift is the most
common confusion — always declare the shift (single line, top of file).

| Role                       | Scope                            | Stop point                |
| -------------------------- | -------------------------------- | ------------------------- |
| **Worker**                 | one dispatched slice, one report | exit contract             |
| **Owner** (`vc-ownership`) | one feature, full slice + polish | push-ready                |
| **Operator** (this skill)  | multi-wave plan + fleet          | "wystarczy wcisnąć guzik" |

See [`./FRAME.md`](./FRAME.md) for charter contrasts.

---

## Operating Model

[`./RUNNER.md`](./RUNNER.md) carries the deterministic seven steps. Headlines:

1. **Read inputs** — operator prompt, cited files (full coverage), artifact
   dir, prior `journal.md`. `aicx` for session continuity.
2. **Reshape via `vc-scaffold`** — categorical, not ad-hoc — when the plan
   has >5 prompts, no wave grouping, no dependency graph, or no trackable
   cuts.
3. **Build the wave atlas** — A foundation / B sequential / C parallel / D
   close-out. See [`./GUIDE.md`](./GUIDE.md) for the full framework.
4. **Pick agents** via [`./WHY_MATRIX_TABLE.md`](./WHY_MATRIX_TABLE.md);
   rotation breaks ties only.
5. **Dispatch one wave at a time** via `vibecrafted <skill> <agent>`. **No
   native subagents** for dispatch — every spawn goes through the framework
   for telemetry. See [`./DISPATCH.md`](./DISPATCH.md) and
   [`./DISPATCH_TEMPLATE.md`](./DISPATCH_TEMPLATE.md).
6. **Await via `/loop` primary**, `ScheduleWakeup` fallback. Read reports,
   verify gates, verify branch + SHA. Recovery dispatch on stall — never
   blind restart. See [`./AWAIT.md`](./AWAIT.md).
7. **Append to `journal.md`** per wake / fire / notify / stop. Synthesize
   wave close-outs. **Stop at the operator's button** — see
   [`./AUTONOMY.md`](./AUTONOMY.md) for what you may / must not do without
   the button press.

---

## Modes — `vibecrafted <skill> <agent>` valid pairs

Canonical launcher shape: `vibecrafted <skill> <agent> [flags]` (alt
`vc-<skill> <agent>`). Agents are peer-tier (claude / codex / gemini); use
[`./WHY_MATRIX_TABLE.md`](./WHY_MATRIX_TABLE.md) for fit.

| skill     | accepts                       | scope                                                |
| --------- | ----------------------------- | ---------------------------------------------------- |
| init      | `--prompt` `--file`           | Repo-truth orientation (perception → intentions)     |
| scaffold  | `--prompt` `--file`           | Founder-first plan authoring, reshape fuzzy plans    |
| workflow  | `--prompt` `--file` `--depth` | Examine → research → implement pipeline              |
| implement | `--prompt` `--file`           | End-to-end bounded feature delivery                  |
| followup  | `--prompt` `--file`           | READ-ONLY post-implementation trajectory check       |
| review    | `--prompt` `--file`           | READ-ONLY per-PR findings-max with evidence grade    |
| marbles   | `--prompt` `--file` `--count` | Loop convergence on existing code                    |
| audit     | `--prompt` `--file` `--task`  | READ-ONLY plan-vs-code falsification                 |
| polarize  | `--prompt` `--file`           | One-axis decisive cut after marbles                  |
| dou       | `--prompt` `--file`           | READ-ONLY Definition-of-Undone product surface       |
| decorate  | `--prompt` `--file`           | Late-stage visual finishing, coherence pass          |
| hydrate   | `--prompt` `--file`           | Marketplace listing, SEO, onboarding packaging       |
| release   | `--prompt` `--file`           | Final outward ship — deploy, DNS, launch             |
| research  | `--prompt` `--file` `--depth` | Triple-agent gap-free research (claude+codex+gemini) |
| agents    | `--prompt` `--file`           | External fleet spawn (claude / codex / gemini)       |
| delegate  | `--prompt` `--file`           | Native operator-side delegation for bounded cuts     |
| intents   | `--prompt` `--file`           | Intention-vs-runtime truth audit                     |
| ownership | `--prompt` `--file`           | Full-spectrum solo delivery, A → Z                   |
| partner   | `--prompt` `--file`           | Shared executive brain co-steering                   |
| prune     | `--prompt` `--file`           | Repository curation + silencer strip                 |

Flags: `--prompt` (inline), `--file` (plan path), `--count` (marbles cap),
`--depth` (research / workflow breadth), `--task` (audit task slug).

---

## Plan-shape: `[ ]` → `[x]`

Every plan, dispatch body, tracker, and stop-point handoff under operator
mode follows the **`[ ]` → `[x]`** checkbox discipline plus numbered-sections
shape — see [`./EMIL.md`](./EMIL.md). Worker dispatch bodies additionally
carry the rail-fenced closing block — see
[`./DISPATCH.md`](./DISPATCH.md) Section "Closing rail".

---

## Closing rail policy

The folk-horror anti-debt rail (kaomoji + suchar) is **mandatory** at the
bottom of every **worker-facing dispatch body**. It is **exempt** for
**operator-side artifacts**: tracker, `journal.md`, wave close-out, and
stop-point handoff all skip the rail, the kaomoji, and the suchar — they
are operator-internal artifacts, not worker briefs. SKILL.md and RUNNER.md
themselves keep the rail because they are worker-facing reference material.

---

## Composition with adjacent skills

`vc-operator` composes with — does not replace — these:

- **`vc-init`** — required gate. Without fresh init evidence, fleet work is blind.
- **`vc-scaffold`** — owns plan authoring. No plan → escalate to `vc-scaffold` first.
- **`vc-ownership`** — each worker you dispatch is in ownership mode for their slice; you are in operator mode for the chain.
- **`vc-marbles`** — when a wave fails on truth-drift, escalate the slice into marbles, not another implementation pass.
- **`vc-partner`** — partner mode for triage **before** the plan; operator mode for execution **after** it. Don't blur them.

---

## Anti-Patterns

Do not in operator mode:

- restart a failed wave blindly — recovery dispatch is a focused integration
  agent, not a re-fire
- silently downgrade model tier (MODEL PARITY: parent Opus → every worker
  Opus, no exceptions)
- author commits in your own name when an agent did the work (AGENT FAIRNESS:
  `Authored-By:` is the worker's)
- push, force-push, merge PRs, or any irreversible operator-side action —
  even when the plan says "next step is merge"
- spawn another `vc-agents` fleet from inside operator mode — recursion is
  operator-only authorization
- spawn native subagents for dispatch — every spawn goes through `vibecrafted`
  for telemetry
- accept role promotion silently — declare the framing-shift
- run dispatch headless / non-watchable (NIGDY HEADLESS)
- claim wave completion when only some prompts in the wave landed green

---

## Output Style

Default to: **Current state** (wave, prompt, SHA landed) → **Proposal**
(next wave shape, agent, recovery hooks) → **Execution** (run_id, await
tracker ID) → **Open risks** → **Next move** (exactly one).

If a wave is in flight, compress output to a checkbox tracker per
[`./EMIL.md`](./EMIL.md) Rule 1 — one bullet per prompt with status,
agent, SHA, and branch.

---

## Call to Action

Read [`./RUNNER.md`](./RUNNER.md) first — it is the mandatory entrypoint.
Then [`./WHY_MATRIX_TABLE.md`](./WHY_MATRIX_TABLE.md) for agent routing,
[`./DISPATCH_TEMPLATE.md`](./DISPATCH_TEMPLATE.md) for the Iter-3 fill-by-
placeholder body, and [`./EMIL.md`](./EMIL.md) for plan checkbox shape.
Then fire Wave A and let `notify` wake you when it lands.

---

## Closing Rail

```text
=======================
Remember: operator mode is permission to remove friction, not permission
to drive the operator's car. You raise the baton, you cue the sections,
you read the score, you stop the piece. The operator owns the hall.
(งಠ_ಠ)ง
=======================

Suchar: Why does the runner-loop never sleep? Because it forgot to checkbox
its own bedtime. (._.)
```

---

_𝚅𝚒𝚋𝚎𝚌𝚛𝚊𝚏𝚝𝚎𝚍. with AI Agents by VetCoders (c)2024-2026 LibraxisAI_
