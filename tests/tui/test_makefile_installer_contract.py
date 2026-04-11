from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_makefile_keeps_gui_first_and_tui_fallback() -> None:
    text = (REPO_ROOT / "Makefile").read_text(encoding="utf-8")

    assert (
        "make vibecrafted   \\033[2mLaunch the browser-based guided installer" in text
    )
    assert "make wizard        \\033[2mInteractive CLI wizard" in text

    vibecrafted_block = text.split("vibecrafted: init-hooks", 1)[1].split(
        "\nwizard: init-hooks", 1
    )[0]
    wizard_block = text.split("wizard: init-hooks", 1)[1].split(
        "\n\ninstall: init-hooks", 1
    )[0]

    assert '@$(PYTHON) $(GUI_INSTALLER) --source "$(SOURCE)"' in vibecrafted_block
    assert (
        "@uv run --project $(INSTALLER_DIR) --quiet vetcoders-installer $(MANIFEST)"
        in wizard_block
    )
