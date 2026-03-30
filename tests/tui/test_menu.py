from scripts import installer_tui


def _empty_diagnostics() -> dict[str, dict[str, dict[str, object]]]:
    return {category: {} for category in installer_tui.CATEGORY_ORDER}


def test_summarize_diagnostics_groups_missing_items_by_category() -> None:
    diagnostics = _empty_diagnostics()
    diagnostics["foundations"] = {
        "loctree-mcp": {"label": "loctree-mcp", "found": True},
        "aicx-mcp": {"label": "aicx-mcp", "found": False},
    }
    diagnostics["agents"] = {
        "codex": {"label": "codex", "found": True},
        "gemini": {"label": "gemini", "found": False},
    }

    found, missing, needs_install = installer_tui.summarize_diagnostics(diagnostics)

    assert "Foundations: loctree-mcp" in found
    assert "Agents: codex" in found
    assert "Foundations: aicx-mcp" in missing
    assert "Agents: gemini" in missing
    assert needs_install == {"foundations": ["aicx-mcp"], "agents": ["gemini"]}


def test_handle_key_runs_diagnostics_before_entering_checklist(monkeypatch) -> None:
    refreshed = {"called": False}

    def fake_refresh(
        state: installer_tui.InstallerState,
    ) -> installer_tui.InstallerState:
        refreshed["called"] = True
        state.diagnostics_ran = True
        return state

    monkeypatch.setattr(installer_tui, "refresh_diagnostics", fake_refresh)
    state = installer_tui.InstallerState(step=installer_tui.DIAGNOSTICS_STEP)

    result = installer_tui.handle_key(state, "enter")

    assert refreshed["called"] is True
    assert result.step == installer_tui.CHECKLIST_STEP


def test_handle_key_launches_install_from_checklist(monkeypatch) -> None:
    started = {"called": False}

    def fake_start(state: installer_tui.InstallerState) -> installer_tui.InstallerState:
        started["called"] = True
        state.install_running = True
        return state

    monkeypatch.setattr(installer_tui, "start_install", fake_start)
    state = installer_tui.InstallerState(step=installer_tui.CHECKLIST_STEP)

    result = installer_tui.handle_key(state, "enter")

    assert started["called"] is True
    assert result.consent_given is True
    assert result.step == installer_tui.INSTALL_STEP
