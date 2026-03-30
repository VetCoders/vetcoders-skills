from pathlib import Path
import sys

import pytest

from scripts import installer_tui
from scripts import vetcoders_install


def test_read_framework_version_reads_version_file(tmp_path: Path) -> None:
    (tmp_path / "VERSION").write_text("9.9.9\n", encoding="utf-8")

    assert installer_tui.read_framework_version(str(tmp_path)) == "9.9.9"


def test_read_framework_version_returns_unknown_when_missing(tmp_path: Path) -> None:
    assert installer_tui.read_framework_version(str(tmp_path)) == "unknown"


def test_build_install_command_includes_compact_noninteractive_flags(
    tmp_path: Path,
) -> None:
    installer_path = tmp_path / "scripts" / "vetcoders_install.py"
    installer_path.parent.mkdir()
    installer_path.write_text("#!/usr/bin/env python3\n", encoding="utf-8")

    command = installer_tui.build_install_command(str(tmp_path))

    assert command[0] == sys.executable
    assert command[1] == str(installer_path)
    assert command[2:] == [
        "install",
        "--source",
        str(tmp_path.resolve()),
        "--with-shell",
        "--compact",
        "--non-interactive",
    ]


def test_build_install_command_raises_when_installer_missing(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        installer_tui.build_install_command(str(tmp_path))


def test_installer_tui_vibecrafted_home_expands_user(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    home = tmp_path / "home"
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("VIBECRAFTED_HOME", "~/.portable-vc")

    assert installer_tui.vibecrafted_home() == home / ".portable-vc"
    assert installer_tui.framework_store_dir() == home / ".portable-vc" / "skills"
    assert installer_tui.install_log_path() == home / ".portable-vc" / "install.log"


def test_vetcoders_install_env_paths_expand_user(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    home = tmp_path / "home"
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("VIBECRAFTED_HOME", "~/.portable-vc")
    monkeypatch.setenv("XDG_CONFIG_HOME", "~/.portable-config")

    assert vetcoders_install.vibecrafted_home() == home / ".portable-vc"
    assert (
        vetcoders_install._helper_target_path()
        == home / ".portable-config" / "vetcoders" / "vc-skills.sh"
    )
    assert (
        vetcoders_install._helper_legacy_path()
        == home / ".portable-config" / "zsh" / "vc-skills.zsh"
    )
