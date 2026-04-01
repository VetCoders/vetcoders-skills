# Quick Start

You have a repo. You have AI agents. You want them to stop guessing
and start converging.

## 1. Install

```bash
curl -fsSLO https://raw.githubusercontent.com/VetCoders/vibecrafted/main/install.sh
bash install.sh
```

Non-destructive. Interactive. Tells you what it does before it does it.
Asks before touching your shell config. Everything reversible with
`make -C ~/.vibecrafted/tools/vibecrafted-current uninstall`.

After install, open a new terminal or:

```bash
source "${XDG_CONFIG_HOME:-$HOME/.config}/vetcoders/vc-skills.sh"
```

## 2. Verify

```bash
make -C ~/.vibecrafted/tools/vibecrafted-current doctor
```

Green means ready. Yellow means the doctor tells you why.

## 3. Orient your agent

Go to any git repo:

```bash
cd ~/your-project
```

Start a Claude Code session and say:

```
Init session
```

This runs `vc-init` — your agent gets three things before touching anything:

- **Memory** — what was done before (indexed session history)
- **Sight** — what the code looks like now (structural map via loctree)
- **Ground truth** — whether quality gates actually pass

Your agent now has orientation instead of assumptions.

## 4. Build something

```
Just do: add user authentication with JWT
```

`vc-justdo` chains the entire pipeline:

- **Craft** — examines the repo, researches the approach, implements
- **Converge** — runs marbles loops: _"what is still wrong?"_ → fix → repeat
- **Ship** — checks product surface, decorates, packages for release

## 5. Run phases individually

```
Scaffold this                           # vc-scaffold — architecture planning
Init session                            # vc-init — context bootstrap
ERi pipeline for adding auth module     # vc-workflow — examine, research, implement
Follow-up check                         # vc-followup — what went wrong
Fill the gaps                           # vc-marbles — convergence until circle is full
Run a Definition of Undone audit        # vc-dou — is it actually ready to ship?
Decorate this                           # vc-decorate — brand, UI, visual polish
Hydrate the product                     # vc-hydrate — packaging, docs, discoverability
Release this                            # vc-release — deployment, distribution
```

## 6. Multi-agent research

For hard problems, send the same question to multiple planners:

```
Research: what is the best auth strategy for this codebase?
```

`vc-partner` sends the same plan to Claude, Codex, and Gemini independently.
You get three expert opinions. Synthesize the strongest parts. Resume the
winning agent into implementation.

## 7. Convergence loops

When the code is close but not done:

```
Marbles: fill the circle on the auth module
```

The agent enters a convergence loop — tools find what is wrong, agent fixes it,
tools check the new landscape, repeat. Stops when no tool can find a single
remaining accusation.

## The tab trick

Type `vc-` and hit tab. Everything is discoverable from the terminal.

---

`// 𝚟𝚒𝚋𝚎𝚌𝚛𝚊𝚏𝚝𝚎𝚍؞`
