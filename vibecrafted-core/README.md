# vibecrafted-core

Core Python library for Vibecrafted runtime surfaces.

This package exposes the stable runtime path helpers, control-plane state
normalization, workflow launch construction, repository status inspection,
doctor summaries, and iTerm2 surface helpers (OSC primitives + Dynamic
Profiles installer) needed by sibling packages such as `vibecrafted-mcp`.

Install from the repository root:

```bash
pip install -e ./vibecrafted-core
```

Smoke the public API:

```bash
python -c "from vibecrafted_core import vibecrafted_home, repo_full, doctor_run; print(repo_full('.'))"
```

## iTerm2 surface helpers

Two zero-dependency modules for working with iTerm2 visually from inside
panes (zellij child, ssh remote, agent shell) and for materializing the
VetCoders mesh as Dynamic Profiles.

### `vibecrafted_core.iterm2_osc`

Emit OSC escape sequences for badges, progress bars, custom buttons,
profile switches, hyperlinks, FinalTerm shell-integration markers, and
the rest of the iTerm2 1337 / 9 / 8 / 133 / 4 vocabulary.

```python
from vibecrafted_core import set_badge, progress, custom_button

print(set_badge(r"\(user.vetcoders.repo) — \(user.vetcoders.zellij_session)"))
print(progress(1, 75))            # success-state progress bar at 75%
print(custom_button(42, "star.fill"))  # tab title button → CSI ? 1337 ; 42 ~
```

CLI form (use from bash launchers, hooks, or shell prompts):

```bash
python -m vibecrafted_core.iterm2_osc badge "build green"
python -m vibecrafted_core.iterm2_osc progress 1 50
python -m vibecrafted_core.iterm2_osc --help
```

### `vibecrafted_core.iterm2_profiles`

Generate iTerm2 Dynamic Profiles JSON for the VetCoders mesh (one parent
profile + per-host children for `dragon`, `sztudio`, `silver`, `div0` +
per-repo children for `vibecrafted`, `vista`, `loctree`) and write it to
`~/Library/Application Support/iTerm2/DynamicProfiles/vibecrafted.json`,
where iTerm2 hot-reloads it.

**Status: experimental.** All profile names carry the `[experimental]`
prefix and the install file is named `vibecrafted-experimental.json`, so
the layer sits ALONGSIDE existing iTerm2 profiles, never replacing them.

The runtime install step is opt-in. Preferred entry point is the
top-level `Makefile`:

```bash
make iterm-plugin            # install (idempotent — refuses to overwrite)
make iterm-plugin-refresh    # overwrite (creates .bak first)
make iterm-plugin-show       # print generated JSON to stdout
make iterm-plugin-uninstall  # remove the installed file
```

Direct CLI access (skip `make`):

```bash
uv run --project vibecrafted-core python -m vibecrafted_core.iterm2_profiles install
uv run --project vibecrafted-core python -m vibecrafted_core.iterm2_profiles path
uv run --project vibecrafted-core python -m vibecrafted_core.iterm2_profiles --help
```

The source-of-truth is `PROFILE_SPECS` in `iterm2_profiles.py`. To extend,
add a `ProfileSpec(...)` entry — every spec produces a stable, deterministic
GUID derived from `(namespace, name)`, so refreshing never duplicates.

## Tests

```bash
PYTHONPATH=. uv run --with pytest python -m pytest tests/ -q
```
