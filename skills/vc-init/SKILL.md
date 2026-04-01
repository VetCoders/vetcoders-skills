---
name: vc-init
version: 3.0.0
description: >-
  Orientation before action. Init equips the agent with three layers of
  situational awareness — History (what happened before), Eyes (what the
  code looks like now), and Verify (whether what you see is actually true).
  No implementation without orientation. The craftsman reads the brief,
  studies the material, and tests the tools before the first cut.
  Trigger: "init", "initialize", "bootstrap", "daj kontekst", "zainicjuj",
  "przygotuj agenta", "start fresh with context".
---

# vc-init — Orientation Before Action

> You would not operate on a patient without reading their chart.
> You would not navigate a city without a map.
> You would not cook without tasting the ingredients.
> Init is how you get oriented before touching anything.

## The Mission

An agent without context is dangerous. Not because it is malicious, but
because it is confident. It will edit code based on training patterns instead
of project reality. It will create symbols that already exist. It will
restructure things that other sessions already restructured differently.

Init prevents this. It gives the agent three things before any implementation:

- **Memory** — what was done before you arrived
- **Sight** — what the code looks like right now
- **Ground truth** — whether the tools actually work

This is not overhead. This is the minimum viable awareness for competent
action. A craftsman who skips orientation produces waste. An agent who
skips init produces noise that other agents (or humans) must clean up.

## Pipeline Position

```
scaffold → [INIT] → workflow → followup → marbles → dou → decorate → hydrate → release
           ^^^^^^
```

Init is the first real act of every session. Everything downstream depends
on the quality of orientation achieved here.

## When To Use

Execute at the start of every session, **before any implementation work**:

- **Cold start**: First session on a repo (zero prior context)
- **Resuming after break**: Stale context after 24+ hours away
- **Subagent delegation**: Agents inherit structured context
- **Structural drift**: Major changes by others since last session

If you are tempted to skip init because "it's a small task" — that is
exactly when init prevents the most damage.

---

## The Three Senses

### Sense 1: Memory — What Happened Before

_Your patient has a chart. Read it._

Pull historical context from previous AI sessions for this project:

- **`aicx_store(hours=168, project=<project>)`** — refresh the indexed record
- **`aicx_refs(hours=168, project=<project>, strict=true)`** — list stored context files
- **`aicx_rank(project=<project>, hours=168, strict=true, top=5)`** — prioritize densest chunks
- **Optional: `aicx_search(query=<task>, project=<project>)`** — narrow to specific feature/bug

Read the most recent 1-2 context files, or the top-ranked 1-2 if more
signal-dense. Understand:

- What was the last task worked on?
- Are there open TODOs or decisions pending?
- What signals were extracted (look for `[signals]` blocks)?

**Discipline:** AICX is a card catalog, not a backpack. Use it to find
the right cards, then read the few relevant files on demand. Do not stuff
the whole archive into context.

**Fallback:** If AICX MCP unavailable, try `aicx all -p "$PROJECT" -H 168 --incremental`
CLI. If neither exists, skip and note the gap. Memory is valuable but not blocking.

### Sense 2: Sight — What The Code Looks Like Now

_Your patient is in front of you. Look at them._

Three sub-steps, in order of breadth:

#### 2a. Structural Map (loctree MCP)

1. **`repo-view(project)`** — health, hubs, languages, LOC, dead exports, cycles
2. **`focus(directory)`** — for target module(s) relevant to the task (1-3 dirs)
3. **`follow(scope)`** — only if repo-view flagged signals (dead, cycles, twins, hotspots)

This gives the agent structural awareness: what files matter, what depends
on what, where the risk is. Without this, every edit is a guess.

#### 2b. Absorb Existing Agent Configs

Check for and read `.vibecrafted/GUIDELINES.md` — the canonical cross-tool
reference. If it exists, use as starting context but **verify against code**.

Also glob for other agent config files: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`,
`VETCODERS.md`, `README.md`, Copilot/Cursor rules, etc.

**Do NOT blindly trust any config file.** They may be outdated.
Cross-reference against what loctree and git show you. If a config file
claims a command that contradicts current code, trust the code.

#### 2c. Derive Conventions from Git History

Run `repo-full` for a complete repository snapshot, or fall back to:

```bash
git log --oneline --decorate --graph -n 15
git status -sb
git stash list
```

From the output, observe actual commit style and active contributors.
Do not invent conventions — read what the team actually does.

### Sense 3: Ground Truth — Is What You See Actually Real?

_You read the chart and looked at the patient. Now test whether your
instruments work before you start cutting._

**This step is mandatory. Do not skip it. Do not assume commands work.**

Locate the project's quality gate commands from:

- `pyproject.toml`, `Makefile`, `justfile`, `package.json`
- `.vibecrafted/GUIDELINES.md` or other agent configs
- README "Testing" or "Development" sections

Run each quality gate command and record the result:

```bash
# Python example:
uv run pytest tests/ -q --tb=no 2>&1 | tail -3
uv run ruff check <src>/ 2>&1 | tail -3

# Rust example:
cargo clippy --workspace -- -D warnings 2>&1 | tail -5
cargo test --workspace -q 2>&1 | tail -5

# Installer/runtime example:
python3 scripts/vetcoders_install.py doctor 2>&1 | tail -5
```

**Rules:**

- **Run the commands.** Do not write "run pytest" in a report without running it.
- Record pass/fail and any unexpected output.
- If a command fails, note it as known issue — do not fix during init.
- If a command does not exist, note absence, do not fabricate.
- Use `--tb=no` or `tail` for conciseness — this is a health check, not debug.

---

## Produce Situational Report

After all three senses, produce two outputs:

### A. Session Report (ephemeral, for this session)

```
## Session Init: <project>

### Memory
- Last activity: <date>
- Open signals: <TODOs, pending decisions — or "none">
- Sessions: <count> entries across <agents>

### Sight
- Files: <N> | LOC: <N> | Languages: <list>
- Health: <cycles, dead exports, twins — or "clean">
- Top hubs: <top 3 files by importers>
- GUIDELINES.md: <current / stale / missing>

### Ground Truth
- <gate 1>: <pass / fail / not configured>
- <gate 2>: <pass / fail / not configured>
- <gate 3>: <pass / fail / not configured>

### Ready
Agent has memory, sight, and verified ground truth.
```

### B. GUIDELINES.md (durable, for all future agents)

Generate on first init, update on subsequent inits if stale. **Always ask
before writing.**

Structure: Product → Architecture → Quality Gates (verified) → Conventions
→ Critical Files → Known Issues. Target 200-600 words. Concise beats complete.

**Do:**

- Derive from code analysis and verified commands
- Date the "verified" timestamp
- Note critical files with high blast radius

**Do NOT:**

- Repeat easily discoverable information
- Include generic advice ("write tests", "handle errors")
- Include test commands you did not verify
- Exceed 600 words

---

## Operational Doctrine (Agent Execution Model)

_This section is for agent internalization._

### Role In The Convergence System

Init is the prosecution's case file preparation. Before any convergence
loop (marbles) can ask "what is still wrong?", the agent must know:

- **What was already fixed** (Memory/AICX) — so it does not re-break solved problems
- **What the current structure is** (Sight/loctree) — so it has objective evidence
- **What the instruments say** (Verify/gates) — so it knows baseline health

Without init, the agent is a tank with no coordinates. It will fire, but
not at the right targets.

### Evidence Chain

Every init output is evidence that downstream skills consume:

- `vc-workflow` uses the structural map to scope implementation
- `vc-followup` uses the gate baseline to measure delta
- `vc-marbles` uses everything — the baseline is what "loop 0" looks like
- `vc-dou` uses the verified gates to assess shipping readiness

If init is skipped, every downstream skill operates on assumptions instead
of evidence. Assumptions are the primary source of wasted loops.

### For Subagent Prompts

When delegating via `vc-agents`, include this preamble:

```
## Context Bootstrap

Use loctree MCP tools as primary exploration layer:
- repo-view(project) first for overview
- slice(file) before modifying any file
- find(name) before creating new symbols
- impact(file) before deleting

Derive truth from code, not from docs. If a doc says X and code says Y, trust Y.

Historical context:
- aicx_store(hours=168, project=<project>)
- aicx_refs(hours=168, project=<project>, strict=true)

Treat AICX as an index. Pull few relevant records, do not dump the archive.
Before creating new implementations, search for existing ones.
```

---

## Anti-Patterns

- Starting implementation without running init (blind coding)
- Running loctree but skipping AICX history (no memory of prior work)
- Reading every context file (context bloat) — read only 1-2 most recent
- Skipping repo-view and jumping to grep (no structural map)
- Trusting config files without cross-referencing code (doc rot)
- Writing "run pytest" without actually running pytest (unverified claims)
- Generating GUIDELINES.md with commands you never tested (hallucination)
- Including generic developer advice (noise)
- Inventing commit conventions instead of reading `git log` (fabrication)

---

_"Memory. Sight. Ground truth. Then — and only then — act."_

_Vibecrafted with AI Agents by VetCoders (c)2026 VetCoders_
