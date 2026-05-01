from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Sequence

from .runtime_paths import vibecrafted_home


def _repo_root_from_source() -> Path | None:
    package_root = Path(__file__).resolve().parents[2]
    candidate = package_root.parent if package_root.name == "vibecrafted-core" else None
    if candidate and (candidate / "scripts" / "vetcoders_install.py").is_file():
        return candidate
    return None


def _installer_module() -> Any:
    repo_root = _repo_root_from_source()
    if repo_root is not None and str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    try:
        from scripts import vetcoders_install
    except ModuleNotFoundError:
        import vetcoders_install  # type: ignore[no-redef]
    return vetcoders_install


def doctor_run(
    store_path: str | Path | None = None,
    state: Any | None = None,
) -> list[Any]:
    """Run the existing Vibecrafted installer doctor through a package API."""
    installer = _installer_module()
    resolved_store = (
        Path(store_path) if store_path is not None else vibecrafted_home() / "skills"
    )
    resolved_state = (
        state if state is not None else installer.InstallState.load(resolved_store)
    )
    return installer.run_doctor(resolved_store, resolved_state)


def doctor_summary(findings: Sequence[Any]) -> dict[str, Any]:
    oks = sum(1 for finding in findings if finding.level == "ok")
    warnings = sum(1 for finding in findings if finding.level == "warn")
    failures = sum(1 for finding in findings if finding.level == "fail")
    return {
        "ok": oks,
        "warnings": warnings,
        "failures": failures,
        "healthy": failures == 0,
        "findings": [
            {
                "level": finding.level,
                "component": finding.component,
                "message": finding.message,
            }
            for finding in findings
        ],
    }
