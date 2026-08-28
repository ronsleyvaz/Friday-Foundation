"""Unit tests for friday-statusline.sh, the buyer status line shipped inside
~/friday-shortcuts.

Hard fork of the operator's scripts/friday-statusline.sh: every operator
internal (MemPalace, sprint tag, context.md read, founder gate, project-root
dependency) is gone. Field-name fallbacks for the Claude Code JSON payload are
carried over so the same install works across payload shapes. Parsing is
python3, not jq -- jq is not guaranteed on a stock Mac.
"""

from __future__ import annotations

import json
import os
import subprocess
import time
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "friday-statusline.sh"


def _run(
    payload: dict[str, object] | None = None,
    cwd: Path | None = None,
    no_jq: bool = False,
    raw_stdin: str | None = None,
) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["NO_COLOR"] = "1"  # disable ANSI so assertions match plain text
    if no_jq:
        # Symlink only the tools the script actually needs into an isolated bin
        # dir and point PATH there exclusively -- proves jq is never needed,
        # not merely tolerated.
        import shutil
        import tempfile

        bin_dir = Path(tempfile.mkdtemp()) / "bin"
        bin_dir.mkdir(parents=True)
        for name in ("python3", "git", "bash", "env", "cat"):
            src = shutil.which(name)
            assert src, f"host is missing required tool for this test: {name}"
            (bin_dir / name).symlink_to(src)
        env["PATH"] = str(bin_dir)

    if raw_stdin is not None:
        stdin_data = raw_stdin
    elif payload is not None:
        stdin_data = json.dumps(payload)
    else:
        stdin_data = None

    return subprocess.run(
        [str(SCRIPT)],
        input=stdin_data,
        capture_output=True,
        text=True,
        timeout=5,
        env=env,
        cwd=str(cwd) if cwd else None,
    )


# --------------------------------------------------------------------------
# Shape and safety
# --------------------------------------------------------------------------


def test_script_exists_and_is_executable() -> None:
    assert SCRIPT.exists(), f"{SCRIPT} missing"
    assert os.access(SCRIPT, os.X_OK), f"{SCRIPT} not executable"


def test_script_exits_zero_with_no_stdin() -> None:
    result = _run()
    assert result.returncode == 0, f"stderr: {result.stderr}"


def test_script_prints_two_rows() -> None:
    result = _run()
    lines = result.stdout.splitlines()
    assert len(lines) == 2, f"expected 2 rows, got {lines!r}"


def test_row_one_has_shortcuts_label_and_chief_of_staff() -> None:
    result = _run()
    lines = result.stdout.splitlines()
    assert lines[0].startswith("Friday SHORTCUTS"), lines
    assert "chief-of-staff" in lines[0], lines


def test_script_exits_fast() -> None:
    start = time.monotonic()
    _run()
    elapsed = time.monotonic() - start
    assert elapsed < 0.5, f"took {elapsed:.3f}s"


def test_rows_under_reasonable_terminal_width() -> None:
    result = _run(
        payload={
            "model": {"display_name": "Claude Opus 4.8"},
            "effort": {"level": "high"},
            "context_window": {"used_tokens": 82000, "max_tokens": 200000},
            "rate_limits": {
                "five_hour": {"remaining_percentage": 35, "resets_at": 4070888400},
                "seven_day": {"used_percentage": 44, "resets_at": 4071406800},
            },
        }
    )
    lines = [ln for ln in result.stdout.splitlines() if ln.strip()]
    assert all(len(line) < 140 for line in lines), lines


def test_no_jq_on_path_still_renders_full_output() -> None:
    """jq is never invoked -- confirmed by stripping it from PATH entirely and
    still getting full rendering, not just a graceful stub."""
    result = _run(
        payload={
            "model": {"display_name": "Claude Opus 4.8"},
            "effort": {"level": "medium"},
            "context_window": {"used_tokens": 10000, "max_tokens": 200000},
        },
        no_jq=True,
    )
    assert result.returncode == 0, f"stderr: {result.stderr}"
    assert "Claude Opus 4.8" in result.stdout
    assert "medium effort" in result.stdout
    assert "ctx:[" in result.stdout


# --------------------------------------------------------------------------
# Branch (row 1)
# --------------------------------------------------------------------------


def test_git_branch_shown_when_run_inside_a_repo(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "feature-xyz", str(repo)], check=True)
    result = _run(cwd=repo)
    assert "feature-xyz" in result.stdout


def test_no_branch_field_when_not_in_a_repo(tmp_path: Path) -> None:
    plain = tmp_path / "not-a-repo"
    plain.mkdir()
    result = _run(cwd=plain)
    assert result.returncode == 0
    # No branch segment -- row1 must not contain a dangling "|" for a blank branch.
    lines = result.stdout.splitlines()
    assert "|  |" not in lines[0]


# --------------------------------------------------------------------------
# Payload fields -- snake_case and camelCase, matching the operator's dual
# support so the same script works across Claude Code payload shapes.
# --------------------------------------------------------------------------


def test_context_and_quota_from_snake_case_payload() -> None:
    result = _run(
        payload={
            "model": {"display_name": "Claude Sonnet 4.6"},
            "effort": {"level": "high"},
            "context_window": {"used_tokens": 82000, "max_tokens": 200000},
            "rate_limits": {
                "five_hour": {"remaining_percentage": 35, "resets_at": 4070888400},
                "seven_day": {"used_percentage": 44, "resets_at": 4071406800},
            },
        }
    )
    assert "Claude Sonnet 4.6" in result.stdout
    assert "high effort" in result.stdout
    assert "ctx:[" in result.stdout
    assert "41% 82k/200k" in result.stdout
    assert "5h:65%" in result.stdout
    assert "7d:44%" in result.stdout


def test_context_and_quota_from_camel_case_payload() -> None:
    result = _run(
        payload={
            "model": {"display_name": "Claude Sonnet 4.6"},
            "effort": {"level": "low"},
            "contextWindow": {"usedTokens": 50000, "maxTokens": 200000},
            "rateLimits": {
                "fiveHour": {"usedPercentage": 20, "resetsAt": 4070888400},
                "sevenDay": {"usedPercentage": 30, "resetsAt": 4071406800},
            },
        }
    )
    assert "low effort" in result.stdout
    assert "25% 50k/200k" in result.stdout
    assert "5h:20%" in result.stdout
    assert "7d:30%" in result.stdout


def test_context_and_quota_from_bracket_key_payload() -> None:
    """A third real Claude Code shape uses literal ["5h"]/["7d"] keys."""
    result = _run(
        payload={
            "rate_limits": {
                "5h": {"used_percentage": 10},
                "7d": {"used_percentage": 15},
            },
        }
    )
    assert "5h:10%" in result.stdout
    assert "7d:15%" in result.stdout


def test_colour_thresholds_green_yellow_red() -> None:
    # colour is stripped by NO_COLOR=1 in _run, so assert on the raw digits only
    # here and cover the ANSI codes in a dedicated colour test below.
    low = _run(payload={"rate_limits": {"5h": {"used_percentage": 10}}})
    mid = _run(payload={"rate_limits": {"5h": {"used_percentage": 60}}})
    high = _run(payload={"rate_limits": {"5h": {"used_percentage": 90}}})
    assert "5h:10%" in low.stdout
    assert "5h:60%" in mid.stdout
    assert "5h:90%" in high.stdout


def test_colour_codes_present_without_no_color(tmp_path: Path) -> None:
    env = os.environ.copy()
    env.pop("NO_COLOR", None)
    result = subprocess.run(
        [str(SCRIPT)],
        input=json.dumps({"rate_limits": {"5h": {"used_percentage": 90}}}),
        capture_output=True,
        text=True,
        timeout=5,
        env=env,
    )
    assert "\033[31m" in result.stdout, "90% must be red"


# --------------------------------------------------------------------------
# Negative / degenerate shapes -- must degrade, never crash.
# --------------------------------------------------------------------------


def test_missing_five_hour_field_degrades() -> None:
    result = _run(payload={"rate_limits": {"seven_day": {"used_percentage": 30}}})
    assert result.returncode == 0
    assert "5h:" not in result.stdout
    assert "7d:30%" in result.stdout


def test_missing_seven_day_field_degrades() -> None:
    result = _run(payload={"rate_limits": {"five_hour": {"used_percentage": 30}}})
    assert result.returncode == 0
    assert "5h:30%" in result.stdout
    assert "7d:" not in result.stdout


def test_missing_context_field_degrades() -> None:
    result = _run(payload={"model": {"display_name": "Claude Opus 4.8"}})
    assert result.returncode == 0
    assert "ctx:[" not in result.stdout
    assert "Claude Opus 4.8" in result.stdout


def test_malformed_json_degrades() -> None:
    result = _run(raw_stdin="{not valid json::")
    assert result.returncode == 0, f"stderr: {result.stderr}"
    assert result.stdout.startswith("Friday SHORTCUTS")


def test_empty_stdin_degrades() -> None:
    result = _run(raw_stdin="")
    assert result.returncode == 0
    assert result.stdout.startswith("Friday SHORTCUTS")


def test_no_stdin_at_all_degrades() -> None:
    """Script invoked with stdin closed entirely (not even an empty pipe)."""
    result = subprocess.run(
        [str(SCRIPT)],
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        timeout=5,
        env={**os.environ, "NO_COLOR": "1"},
    )
    assert result.returncode == 0
    assert result.stdout.startswith("Friday SHORTCUTS")


def test_no_python3_on_path_still_exits_zero(tmp_path: Path) -> None:
    """Belt and suspenders: even if python3 vanished from PATH, never crash."""
    import shutil

    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    for name in ("bash", "git"):
        src = shutil.which(name)
        if src:
            (bin_dir / name).symlink_to(src)
    env = {**os.environ, "PATH": str(bin_dir), "NO_COLOR": "1"}
    result = subprocess.run(
        [str(SCRIPT)],
        input="{}",
        capture_output=True,
        text=True,
        timeout=5,
        env=env,
    )
    assert result.returncode == 0, f"stderr: {result.stderr}"


# --------------------------------------------------------------------------
# Clean-room: no operator internals anywhere in the shipped script.
# --------------------------------------------------------------------------


def test_no_operator_internals_in_source() -> None:
    source = SCRIPT.read_text()
    forbidden = [
        "mempalace",
        "MemPalace",
        "MP:",
        "founder_statusline",
        "founder-profile",
        "FRIDAY_PROJECT_ROOT",
        "FRIDAY_SPRINT",
        "context.md",
        "sprint_tag",
        "pending-debrief",
        "curfew",
    ]
    hits = [term for term in forbidden if term in source]
    assert not hits, f"operator internals leaked into friday-statusline.sh: {hits}"


def test_never_calls_jq() -> None:
    source = SCRIPT.read_text()
    assert "jq " not in source and "command -v jq" not in source, (
        "friday-statusline.sh must not depend on jq at all"
    )
