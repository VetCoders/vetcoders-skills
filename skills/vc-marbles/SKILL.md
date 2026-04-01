---
name: vc-marbles
version: 4.0.0
description: >
  Convergence through counterexample — the loop that makes code healthier.
  Tools find what is wrong. You categorize and prioritize. Agent eliminates.
  Each fix changes the landscape, revealing issues hidden beneath worse ones.
  The system cannot get worse, only better. Monotonic entropy reduction.
  Stop when nothing is wrong. The circle is full.
  Trigger phrases: "marbles", "loop until done", "fill the gaps", "kulki",
  "iteruj aż będzie gotowe", "convergence loop", "counterexample",
  "what is still wrong", "adaptive loops", "keep going until clean",
  "wypełnij okrąg", "entropy reduction", "konwergencja".
---

# vc-marbles — Convergence Through Counterexample

> Not "is it correct?" — that cannot be proven.
> Only "what is still wrong?" — and eliminate it.
> Each loop removes entropy. Stop when the circle is full.

---

## The Mechanism

Traditional quality asks: _is this correct?_ and tries to prove yes.
That question has no finite answer for a living codebase.

Marbles asks a different question: **what is still wrong?**

Each loop inspects the current state and finds **counterexamples** —
concrete things that contradict health. A dead export in `utils.ts:42`.
A circular import between `auth/` and `api/`. A twin export `Button`
living in two files. These are not abstract noise. They are specific,
named, located violations of health.

This is counterexample-guided convergence — CEGIS applied to code:

```
hypothesis:      "this codebase is healthy"
counterexample:  sniff finds dead export `formatDate` in utils.ts:42
correction:      remove dead export
new landscape:   utils.ts is now empty → new counterexample revealed
correction:      remove empty file
new landscape:   import in api.ts pointed to utils.ts → broken import revealed
correction:      fix import
new landscape:   cycle between api.ts and auth.ts disappeared → health score jumps

No single loop understood the whole.
Each loop only answered: "what is still wrong?"
The convergence was emergent.
```

Fixing one issue **changes the landscape**, exposing issues hidden beneath
worse ones. This is the cascade effect — the primary convergence driver.
Entropy drops monotonically. You cannot go backwards.

## Operational Doctrine (Agent Execution Model)

You are the Vibecrafted Marbles executor.

Focus on identifying and eliminating issues in this codebase.
You role is not to prove correctness.

### Roles

**Tools (loctree, linters, tests, compilers)** = prosecution. They find
evidence of what is wrong. They have unlimited zeal because they are machines.

**Human** = the authority who categorizes, prioritizes, and signs warrants.
Or — in autonomous mode — the quality gates serve as automatic prosecution,
and the human is the sleeping judge whose verdict comes when the prosecution
runs out of accusations.

**Agent** = executor. Focused, precise, destructive within its assigned
target. Sees through a periscope, not the whole battlefield. Needs the
prosecution (tools) and authority (human) to tell it where to aim.

The agent does not discover what is wrong. **The tools discover.
The agent eliminates.**

### Evidence-Based Execution

Every fix must trace to a tool output:

- "Removing this export because `follow(dead)` shows zero consumers"
- "Not touching this file because `impact` shows 24 dependents"
- "Fixing this import because the compiler reports unresolved path"

If the agent cannot cite evidence to justify an edit, it is guessing.
Guessing is the primary source of agent-generated entropy.

---

## When To Use

- After first implementation pass leaves known gaps
- When followup reveals findings that need iterative fixing
- When the team says "keep going until it's clean"
- Anytime the answer to "is it done?" is "almost"
- When you need adaptive iteration count (not fixed 2 loops)

Marbles typically follows from `/vc-workflow` or `/vc-followup` identifying
issues that need iterative pressure. It can also run from a raw prompt or
plan file. Either way, each agent gets the same starting brief against an
evolving codebase.

## Convergence Protocol

### Each Loop Iteration

```
┌─────────────────────────────────────────────────────────┐
│  LOOP N                                                  │
│                                                          │
│  1. TOOLS ACCUSE: "what is still wrong?"                 │
│     └─ Run loctree-mcp tools (multiple sources)          │
│     └─ Run quality gates                                 │
│     └─ List concrete counterexamples to health           │
│                                                          │
│  2. TARGET the most prominent counterexamples            │
│     └─ Max 3-5 items per loop (don't boil the ocean)     │
│     └─ Expect cascades: fixing these will reveal more    │
│                                                          │
│  3. AGENT ELIMINATES counterexamples                     │
│     └─ vc-agents (first choice) or vc-delegate (small)   │
│     └─ Each fix narrows the space of possible bugs       │
│                                                          │
│  4. TOOLS OBSERVE the new landscape                      │
│     └─ Run gates on the changed codebase                 │
│     └─ NEW findings may appear (cascade) — expected      │
│                                                          │
│  5. SCORE                                                │
│     └─ Distinguish cascade from divergence               │
│     └─ Decide: continue or converged?                    │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Convergence Metrics

After each loop, track:

- **P0 / P1 / P2 counts** (must all be 0 to converge)
- **Cascade findings** (new issues revealed by fixes — expected and healthy)
- **Net counterexamples remaining**
- **Quality gates** (build, lint, tests, security)
- **Convergence score** (0-100: 0=deep issues, 100=circle full)

### Stopping Criteria

**STOP when:**

1. No counterexamples remain at any priority
2. Two consecutive loops with zero delta (plateaued)
3. User says stop

**DO NOT STOP when:**

- Counterexamples remain (unless user explicitly accepts)
- Quality gates failing
- Divergence detected (stop iterating, but investigate)

### Cascade vs Divergence

When loop N has MORE findings than loop N-1:

**Cascade (healthy):** Previous findings RESOLVED, new ones appeared
because fixes revealed hidden issues. Old problems gone, new ones shallower.
Continue — the cascade will settle.

**Divergence (unhealthy):** Previous findings STILL PRESENT, new ones
appeared on top. Fixes are introducing problems without solving old ones.
**STOP.** Re-examine the approach. Do not continue blind iteration.

## Multi-Agent Modes

### `vc-marbles <agent>` — Single Agent

One agent, one loop. Tools accuse, agent eliminates, tools re-examine.
The simplest mode. Default.

### `vc-marbles duo` — Adversarial Pair

Two agents. One implements fixes. The other is a second prosecutor that
scrutinizes the first agent's work and hunts for new counterexamples from
a different angle. Not two tanks on the same target — one tank and one
counter-intelligence sniper. Convergence is stronger because accusations
come from two independent sources.

### `vc-marbles trio` — Specialized Triad

Three agents, three roles. Claude for complex reasoning and architectural
cuts. Codex for rapid surgical fixes. Gemini for broad scanning and
validation. Tank, aerial reconnaissance, artillery. Each sees different
things, each covers the others' blind spots.

### `vc-marbles multi` — Full Battalion

N agents, coordinated by a supervisor (marbles watchdog). Each agent gets
a sector of the codebase. Supervisor collects reports from all fronts and
decides: "north sector clear, east sector has 3 remaining accusations,
redirect forces." Requires `rust-ai-locker` as resource police to prevent
multiple heavy builds from crashing the system.

### Lifecycle: `pause / stop / resume / session`

- **`pause`** — current agent finishes its active fix, does not start next
  loop. Resources released for other agents.
- **`stop`** — front terminated. Write final loop report. Convergence
  trajectory preserved.
- **`resume`** — restart from last recorded state. Re-run tools to detect
  landscape changes during pause.
- **`session`** — status report across all active fronts. Who is where,
  what remains, convergence trajectory per sector.

## Last Pass: Prune Before You Leave

Before declaring convergence, step back and look at the repo from a distance.

Implementation loops accumulate sediment: dead helpers, orphaned modules,
stale experiments, duplicated glue. Every loop that adds code without
removing dead code increases entropy.

Run `/vc-prune` as the final gate. Use loctree and structural tools to find
what the implementation loops left behind:

- Dead code that no runtime, build, or test path reaches
- Twin files and near-duplicates introduced across loops
- Stale scaffolding necessary mid-convergence but not after
- Orphaned registrations, imports, and manifest entries

This is the last counterexample class: **the sediment itself.**
The circle is not full until the debris from filling it is gone too.

## Integration with 𝚅𝚒𝚋𝚎𝚌𝚛𝚊𝚏𝚝𝚎𝚍. Pipeline

```
scaffold → init → workflow → followup → [MARBLES] ↻ → dou → decorate → hydrate → release
                                         ^^^^^^^^^^^^^
```

Marbles is the gate between building and shipping.
It loops itself until the circle is full.

## Anti-Patterns

- Fixed loop count ("always run 4 loops") — defeats adaptive convergence
- Looping without asking "what is still wrong?" — blind iteration
- Agent inventing accusations instead of reading tool output — hallucination
- Leaking loop awareness to agents (count, reports, status)
- Rigid P0→P1→P2 ordering as steering — cascades don't respect categories
- Continuing past convergence (overfit — introduces new problems)
- Looping without writing reports (no trajectory = no learning)
- Confusing cascade with divergence
- Single counterexample per loop (too slow — target 3-5)
- Entire codebase per loop (too broad — scope to affected area)
- Skipping prune pass before declaring convergence
- Running multiple heavy builds without resource locking (system crash)

---

_"Not 'is it correct?' — that cannot be proven._
_Only 'what is still wrong?' — and eliminate it._
_Stop when the circle is full."_

_Vibecrafted with AI Agents by VetCoders (c)2026 VetCoders_
