"""Offline tests for scripts/seed-good-first-issues.sh (issue #28).

Every test runs the real script via subprocess against a private copy of the
repo tree under tmp_path, with a fake ``gh`` shim first on PATH. The shim logs
every invocation and answers ``gh issue list`` from a fixture file, so no test
can ever reach GitHub or create a real issue.

The two skip conditions under test:
  (a) the seed's command already ships (``commands/<name>.md`` exists, or the
      name is registered in PACK_COMMANDS in install.sh);
  (b) an issue with the exact seed title already exists, open OR closed.
"""
import re
import shutil
import stat
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SCRIPT_REL = Path("scripts") / "seed-good-first-issues.sh"

# Record and field separators used by the shim's invocation log. Issue bodies
# contain newlines, so a line-per-call log would not survive a real body.
RS = "\x1e"
FS = "\x1f"

SHIM = """#!/bin/sh
# Fake GitHub CLI for tests. Logs argv, never talks to the network.
LOG="{log}"
TITLES="{titles}"
printf '%s\\037' "$@" >> "$LOG"
printf '\\036' >> "$LOG"
case "$1 $2" in
  "label create") exit 0 ;;
  "issue list") cat "$TITLES"; exit 0 ;;
  "issue create") exit 0 ;;
  *) exit 99 ;;
esac
"""


def _copy_repo(tmp_path: Path) -> Path:
    """Private copy of the parts of the tree the script reads, so the script's
    BASH_SOURCE-based root resolution lands inside tmp_path, never the real tree."""
    copy = tmp_path / "repo"
    copy.mkdir()
    shutil.copytree(REPO_ROOT / "commands", copy / "commands")
    shutil.copytree(REPO_ROOT / "scripts", copy / "scripts")
    shutil.copy2(REPO_ROOT / "install.sh", copy / "install.sh")
    return copy


def _make_shim(tmp_path: Path, existing_titles: list) -> Path:
    shim_dir = tmp_path / "bin"
    shim_dir.mkdir()
    log = tmp_path / "gh-calls.log"
    log.write_text("")
    titles = tmp_path / "existing-titles.txt"
    titles.write_text("".join(t + "\n" for t in existing_titles), encoding="utf-8")
    gh = shim_dir / "gh"
    gh.write_text(SHIM.format(log=log, titles=titles), encoding="utf-8")
    gh.chmod(gh.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    return shim_dir


def _run_seed(tmp_path: Path, existing_titles: list):
    """Run the script in a copied tree with the shim first on PATH.
    Returns (CompletedProcess, list of gh argv lists, path to the copied tree)."""
    copy = _copy_repo(tmp_path)
    shim_dir = _make_shim(tmp_path, existing_titles)
    env = {"PATH": f"{shim_dir}:/usr/bin:/bin", "HOME": str(tmp_path)}
    result = subprocess.run(
        ["bash", str(copy / SCRIPT_REL)],
        cwd=str(tmp_path),
        env=env,
        capture_output=True,
        text=True,
        timeout=30,
    )
    raw = (tmp_path / "gh-calls.log").read_text(encoding="utf-8")
    calls = [rec.split(FS)[:-1] for rec in raw.split(RS) if rec]
    return result, calls, copy


def _seed_titles() -> list:
    """Every title the script seeds, read from the script so new seeds are
    covered without editing this test."""
    text = (REPO_ROOT / SCRIPT_REL).read_text(encoding="utf-8")
    titles = re.findall(r'^create_issue "([^"]+)"', text, flags=re.MULTILINE)
    assert titles, "no create_issue lines found in the seed script"
    return titles


def _command_name(title: str) -> str:
    match = re.search(r"/([a-z0-9-]+) command", title)
    return match.group(1) if match else ""


def _ships(copy: Path, name: str) -> bool:
    """Oracle for skip condition (a), evaluated against the copied tree."""
    if (copy / "commands" / f"{name}.md").exists():
        return True
    install = (copy / "install.sh").read_text(encoding="utf-8")
    return f'"{name} ' in install


def _skip_lines(stdout: str) -> list:
    """(reason, title) pairs for every SKIP line the script printed."""
    out = []
    for line in stdout.splitlines():
        if line.startswith("SKIP"):
            reason, _, title = line.partition(": ")
            out.append((reason, title))
    return out


def _created_titles(calls: list) -> list:
    created = []
    for argv in calls:
        if argv[:2] == ["issue", "create"]:
            created.append(argv[argv.index("--title") + 1])
    return created


def _has_state_all(argv: list) -> bool:
    if "--state=all" in argv:
        return True
    return any(a == "--state" and argv[i + 1] == "all" for i, a in enumerate(argv[:-1]))


def test_shipped_commands_are_skipped_without_creating_issues(tmp_path):
    """Skip condition (a): seeds whose command already ships never reach gh issue create."""
    result, calls, copy = _run_seed(tmp_path, existing_titles=[])
    assert result.returncode == 0, result.stderr

    seeds = _seed_titles()
    shipped = [t for t in seeds if _ships(copy, _command_name(t))]
    expected_created = [t for t in seeds if t not in shipped]

    # The fixture tree really does ship these three, so the skip is exercised.
    for name in ("changelog", "roadmap", "positioning"):
        assert f"[GOOD FIRST ISSUE] /{name} command" in shipped, name

    skips = _skip_lines(result.stdout)
    for name in ("changelog", "roadmap", "positioning"):
        title = f"[GOOD FIRST ISSUE] /{name} command"
        matching = [reason for reason, t in skips if t == title]
        assert matching, f"no SKIP line for {title}\nstdout:\n{result.stdout}"
        reason = matching[0]
        assert name in reason, f"SKIP reason must name the command: {reason}"
        assert "exist" in reason.lower(), f"SKIP reason must say it already exists: {reason}"

    created = _created_titles(calls)
    for name in ("changelog", "roadmap", "positioning"):
        assert not any(f"/{name} command" in t for t in created), created
    assert len(created) == len(seeds) - len(shipped), created
    assert sorted(created) == sorted(expected_created)


def test_existing_issue_is_skipped_even_when_closed(tmp_path):
    """Skip condition (b): an exact-title match is skipped, and the lookup asks
    for --state all so a closed issue counts too."""
    standup = "[GOOD FIRST ISSUE] /standup command"
    result, calls, copy = _run_seed(tmp_path, existing_titles=[standup])
    assert result.returncode == 0, result.stderr

    skips = _skip_lines(result.stdout)
    matching = [reason for reason, t in skips if t == standup]
    assert matching, f"no SKIP line for {standup}\nstdout:\n{result.stdout}"
    assert "exist" in matching[0].lower(), (
        f"SKIP reason must say the issue already exists: {matching[0]}"
    )

    created = _created_titles(calls)
    assert standup not in created, created

    list_calls = [argv for argv in calls if argv[:2] == ["issue", "list"]]
    assert list_calls, "script never called gh issue list"
    for argv in list_calls:
        assert _has_state_all(argv), f"gh issue list must pass --state all: {argv}"

    seeds = _seed_titles()
    expected_created = [
        t for t in seeds if t != standup and not _ships(copy, _command_name(t))
    ]
    assert sorted(created) == sorted(expected_created)


def test_seed_script_syntax():
    result = subprocess.run(
        ["bash", "-n", str(REPO_ROOT / SCRIPT_REL)],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
