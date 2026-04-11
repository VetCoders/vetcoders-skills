# Vibecrafted built-in installer runner

Sequential trust-building installer runner, vendored into Vibecrafted so that
`make wizard` and `install.sh` have **zero external runtime dependencies** —
they bootstrap `uv` once, `uv sync` this directory into an isolated local
`.venv/`, and drive the install from `install.toml` at the repo root.

## Why vendored?

The canonical source lives in
[`~/Libraxis/vetcoders-tools/installer/`](https://github.com/VetCoders/vetcoders-tools)
and targets universal use (any repo, Python/Rust/anything). This directory is a
vendored copy kept in sync — Vibecrafted must remain self-contained so that a
fresh clone + `make wizard` _just works_, without requiring the user to
`uv tool install vetcoders-installer` globally first.

When the canonical source changes, copy the module over:

```bash
cp ~/Libraxis/vetcoders-tools/installer/vetcoders_installer/__init__.py \
   ~/Libraxis/vibecrafted/scripts/installer/vetcoders_installer/__init__.py
```

## How it's wired

- **`Makefile` target `wizard`** → `uv run --project scripts/installer vetcoders-installer install.toml`
- **`install.sh`** interactive path → same command, executed on the staged snapshot
- **`install.toml`** at repo root declares the three phases (Foundations /
  Skills & Helpers / Doctor) with `persist = true`
- **`.venv/`** lives in this directory (git-ignored); first `uv sync` creates
  it, subsequent runs reuse it

## Testing without mutating state

```bash
cd ~/Libraxis/vibecrafted
uv run --project scripts/installer vetcoders-installer install.toml --dry-run
uv run --project scripts/installer vetcoders-installer install.toml --only doctor --verbose
```
