from __future__ import annotations

# ruff: noqa: E402,F401,F403,F405

import sys
from pathlib import Path

_CORE_SRC = Path(__file__).resolve().parents[1] / "vibecrafted-core"
if _CORE_SRC.is_dir() and str(_CORE_SRC) not in sys.path:
    sys.path.insert(0, str(_CORE_SRC))

from vibecrafted_core import control_plane as _control_plane
from vibecrafted_core.control_plane import *  # noqa: F401,F403


def _sync_overrides() -> None:
    _control_plane.vibecrafted_home = vibecrafted_home


def sync_state() -> dict[str, object]:
    _sync_overrides()
    return _control_plane.sync_state()


def cli(argv: list[str] | None = None) -> int:
    _sync_overrides()
    return _control_plane.cli(argv)


if __name__ == "__main__":  # pragma: no cover - shim CLI entrypoint
    raise SystemExit(cli())
