from __future__ import annotations

import os
import shutil
import subprocess
import textwrap
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
HELPER_SCRIPT = REPO_ROOT / "skills" / "vc-agents" / "shell" / "vetcoders.sh"
RUNTIME_HELPER = REPO_ROOT / "runtime" / "helpers" / "vetcoders-runtime-core.sh"


def _run_vetcoders_helper(
    helper_script: Path,
    command: str,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    run_env = os.environ.copy()
    if env:
        run_env.update(env)
    return subprocess.run(
        ["bash", "-lc", f'source "{helper_script}"; {command}'],
        cwd=str(REPO_ROOT),
        env=run_env,
        capture_output=True,
        text=True,
        check=False,
    )


def _install_runtime_probe_helper(helper_root: Path, marker: str) -> None:
    helper_target = helper_root / "runtime" / "helpers" / "vetcoders-runtime-core.sh"
    helper_target.parent.mkdir(parents=True, exist_ok=True)
    helper_target.write_text(
        textwrap.dedent(
            f'''
            # shellcheck shell=bash
            source "{RUNTIME_HELPER}"
            _vetcoders_spawn_home() {{
              printf "{marker}\\n"
            }}
            '''
        ),
        encoding="utf-8",
    )


def test_vetcoders_shim_prefers_runtime_helper_from_repo_root(tmp_path: Path) -> None:
    marker = "runtime-helper-from-repo-root"
    helper_root = tmp_path / "probe-runtime"
    _install_runtime_probe_helper(helper_root, marker)

    result = _run_vetcoders_helper(
        HELPER_SCRIPT,
        'printf "%s\\n" "$(_vetcoders_spawn_home codex)"',
        {"VIBECRAFTED_ROOT": str(helper_root)},
    )

    assert result.returncode == 0
    assert result.stdout.strip() == marker
    assert result.stderr == ""


def test_vetcoders_shim_prefers_staged_tools_runtime_helper(tmp_path: Path) -> None:
    marker = "runtime-helper-from-staged-tools"
    staged_home = tmp_path / "vibecrafted-home" / ".vibecrafted"
    staged_root = staged_home / "tools" / "vibecrafted-current"
    _install_runtime_probe_helper(staged_root, marker)

    installed_script = (
        tmp_path / "installed-tree" / "skills" / "vc-agents" / "shell" / "vetcoders.sh"
    )
    installed_script.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(HELPER_SCRIPT, installed_script)

    result = _run_vetcoders_helper(
        installed_script,
        'printf "%s\\n" "$(_vetcoders_spawn_home codex)"',
        {"VIBECRAFTED_HOME": str(staged_home), "VIBECRAFTED_ROOT": ""},
    )

    assert result.returncode == 0
    assert result.stdout.strip() == marker
    assert result.stderr == ""


def test_vetcoders_spawn_script_path_stays_command_compatible() -> None:
    env = os.environ.copy()
    env["VIBECRAFTED_ROOT"] = str(REPO_ROOT)
    result = _run_vetcoders_helper(
        HELPER_SCRIPT,
        'printf "%s\\n" "$(_vetcoders_spawn_script codex codex_spawn.sh)"',
        env=env,
    )

    assert result.returncode == 0
    spawn_script = Path(result.stdout.strip())
    assert spawn_script.name == "codex_spawn.sh"
    assert spawn_script.is_file()


def test_vetcoders_keeps_launcher_entrypoints_available() -> None:
    result = _run_vetcoders_helper(
        HELPER_SCRIPT,
        "command -v vc-implement && command -v vc-research && command -v vc-polarize && command -v codex-implement",
        {"VIBECRAFTED_ROOT": str(REPO_ROOT)},
    )

    assert result.returncode == 0
    assert "vc-implement" in result.stdout
    assert "vc-research" in result.stdout
    assert "vc-polarize" in result.stdout
    assert "codex-implement" in result.stdout
    assert "command not found" not in result.stderr


def test_compact_session_name_is_zsh_compatible() -> None:
    if shutil.which("zsh") is None:
        return

    result = subprocess.run(
        [
            "zsh",
            "-fc",
            (
                f'source "{HELPER_SCRIPT}"; '
                "_vetcoders_compact_session_name "
                '"lbrx-services-owne-135739-94539" "owne-135739-94539"'
            ),
        ],
        cwd=REPO_ROOT,
        env={**os.environ, "VIBECRAFTED_ROOT": str(REPO_ROOT)},
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert result.stdout.strip().endswith("owne-135739-94539")
    assert "unrecognized modifier" not in result.stderr


def test_vc_marbles_wrapper_routes_control_subcommands(tmp_path: Path) -> None:
    capture_file = tmp_path / "inspect-args.txt"
    result = _run_vetcoders_helper(
        HELPER_SCRIPT,
        (
            'marbles-inspect() { printf "%s\\n" "$@" > "$CAPTURE_FILE"; }; '
            "vc-marbles inspect marb-205740-3318"
        ),
        {"VIBECRAFTED_ROOT": str(REPO_ROOT), "CAPTURE_FILE": str(capture_file)},
    )

    assert result.returncode == 0
    assert capture_file.read_text(encoding="utf-8").splitlines() == ["marb-205740-3318"]


def test_vc_skill_wrapper_help_after_agent_does_not_launch_worker() -> None:
    result = _run_vetcoders_helper(
        HELPER_SCRIPT,
        (
            "_vetcoders_skill_entry() { printf 'launched\\n'; return 99; }; "
            "vc-ownership codex --help"
        ),
        {"VIBECRAFTED_ROOT": str(REPO_ROOT)},
    )

    assert result.returncode == 0
    assert "Usage: vc-ownership <claude|codex|gemini>" in result.stderr
    assert "launched" not in result.stdout


def test_vc_polarize_task_injects_prism_payload(tmp_path: Path) -> None:
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    fake_loct = fake_bin / "loct"
    args_file = tmp_path / "loct-args.txt"
    capture_file = tmp_path / "prompt.md"
    fake_loct.write_text(
        textwrap.dedent(
            """\
            #!/usr/bin/env bash
            printf '%s\n' "$@" > "$LOCT_ARGS_FILE"
            cat <<'JSON'
            {"schema_version":"loctree.prism.v1","total_score":13,"axis_scores":{"spread":3}}
            JSON
            """
        ),
        encoding="utf-8",
    )
    fake_loct.chmod(0o755)

    result = _run_vetcoders_helper(
        HELPER_SCRIPT,
        (
            f'export PATH="{fake_bin}:$PATH"; '
            '_vetcoders_prompt_text() { printf \'%s\' "$3" > "$CAPTURE_FILE"; }; '
            "vc-polarize codex --task 'marbles versus polarize skills: polarize them'"
        ),
        {
            "VIBECRAFTED_ROOT": str(REPO_ROOT),
            "VIBECRAFTED_HOME": str(tmp_path / "home" / ".vibecrafted"),
            "PATH": f"{fake_bin}{os.pathsep}{os.environ.get('PATH', '')}",
            "LOCT_ARGS_FILE": str(args_file),
            "CAPTURE_FILE": str(capture_file),
        },
    )

    assert result.returncode == 0, result.stderr
    args = args_file.read_text(encoding="utf-8").splitlines()
    assert args[:4] == ["prism", "--project", str(REPO_ROOT), "--with-aicx"]
    assert "marbles versus polarize skills: polarize them" in args
    assert "marbles versus polarize skills: polarize them code truth" in args
    assert "marbles versus polarize skills: polarize them product truth" in args
    assert "--json" in args

    prompt = capture_file.read_text(encoding="utf-8")
    assert "Perform the vc-polarize skill on this repository." in prompt
    assert "Polarize task: marbles versus polarize skills: polarize them" in prompt
    assert "Prism preflight command: loct prism" in prompt
    assert "--with-aicx" in prompt
    assert '"schema_version":"loctree.prism.v1"' in prompt
    assert '"total_score":13' in prompt


def test_runtime_core_preserves_origin_org_repo_resolution(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    subprocess.run(
        ["git", "init", str(repo)], check=True, capture_output=True, text=True
    )
    subprocess.run(
        [
            "git",
            "-C",
            str(repo),
            "remote",
            "add",
            "origin",
            "https://github.com/VetCoders/vibecrafted.git",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    result = _run_vetcoders_helper(
        HELPER_SCRIPT,
        f'_vetcoders_org_repo "{repo}"',
        {"VIBECRAFTED_ROOT": str(REPO_ROOT)},
    )

    assert result.returncode == 0
    assert result.stdout.strip() == "VetCoders/vibecrafted"


def test_research_summary_does_not_execute_await_command(tmp_path: Path) -> None:
    run_dir = tmp_path / "research" / "rsch-test"
    run_dir.mkdir(parents=True)
    prompt_file = run_dir / "plans" / "plan.md"
    prompt_file.parent.mkdir()
    prompt_file.write_text("research plan\n", encoding="utf-8")

    result = _run_vetcoders_helper(
        HELPER_SCRIPT,
        (
            f'_vetcoders_write_research_summary "{run_dir}" "rsch-test" '
            f'"{tmp_path}" "{prompt_file}" claude.sh codex.sh gemini.sh'
        ),
        {"VIBECRAFTED_ROOT": str(REPO_ROOT)},
    )

    assert result.returncode == 0
    summary_file = run_dir / "summary.md"
    assert result.stdout.strip() == str(summary_file)
    assert "Await: vc-research-await --run-id rsch-test" in summary_file.read_text(
        encoding="utf-8"
    )
    assert "No matching launchers or metadata found yet" not in result.stderr
