"""
install.sh integration tests.

Two independent paths:
- Full pack (no argument): clones the whole repo into ~/friday-shortcuts via
  git, from a local git mirror in tests (never GitHub), personalises the
  brain file, wires spinner + status line settings, installs commands into
  ~/friday-shortcuts/.claude/commands/ (folder-scoped, never a global sync),
  and opens Claude Code. Re-running it on an existing clone updates
  Foundation's own tracked files in place, leaving CLAUDE.md and friday/
  untouched.
- Single capability (`-- <name>`): unchanged, downloads one command file over
  HTTP into the current directory. Covered against a local HTTP server, same
  as before this rebuild.
"""
import http.server
import os
import re
import shutil
import subprocess
import tempfile
import threading
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
INSTALL_SH = REPO_ROOT / "install.sh"

# Which bash runs install.sh. CI's macOS leg sets this to /bin/bash so the tests
# exercise stock bash 3.2 (Homebrew bash 5 sits ahead of it on the runner PATH).
BASH = os.environ.get("FRIDAY_TEST_BASH", "bash")


def start_local_server(directory: Path):
    """Serve `directory` over HTTP on a random loopback port. Returns (httpd, port)."""
    class RepoHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(directory), **kwargs)

        def log_message(self, *args):
            pass  # suppress stdout noise during tests

    httpd = http.server.HTTPServer(("127.0.0.1", 0), RepoHandler)
    port = httpd.server_address[1]
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    return httpd, port


def run_install_custom_path(tmp_home: Path, cwd: Path, tool_names, capability: str = ""):
    """Run install.sh with PATH holding ONLY symlinks to the named host tools.

    Lets a test withhold `curl`, `claude`, or `git` deterministically to
    exercise the prerequisite gates, regardless of what is installed on the
    test host.
    """
    bin_dir = tmp_home / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    for name in tool_names:
        src = shutil.which(name)
        assert src, f"host is missing required tool for this test: {name}"
        (bin_dir / name).symlink_to(src)

    env = {"HOME": str(tmp_home), "PATH": str(bin_dir)}
    cmd = [BASH, str(INSTALL_SH)]
    if capability:
        cmd.append(capability)
    return subprocess.run(
        cmd, env=env, capture_output=True, text=True, cwd=str(cwd), stdin=subprocess.DEVNULL,
    )


def make_fake_claude(bin_dir: Path):
    """Write a minimal fake 'claude' binary so the installer's check passes."""
    bin_dir.mkdir(parents=True, exist_ok=True)
    fake = bin_dir / "claude"
    fake.write_text("#!/bin/sh\necho 'claude-code-fake'\n")
    fake.chmod(0o755)
    return str(bin_dir)


def run_install(tmp_home: Path, cwd: Path, repo_raw_url: str, capability: str) -> subprocess.CompletedProcess:
    """Run the single-capability install path (`install.sh -- <capability>`)
    with isolated HOME and FRIDAY_REPO_RAW override. Unaffected by the
    full-pack rebuild: still one file over HTTP into cwd."""
    fake_bin = make_fake_claude(tmp_home / "bin")
    env = os.environ.copy()
    env["HOME"] = str(tmp_home)
    env["FRIDAY_REPO_RAW"] = repo_raw_url
    env["PATH"] = fake_bin + ":" + env.get("PATH", "")

    cmd = [BASH, str(INSTALL_SH), capability]
    return subprocess.run(
        cmd, env=env, capture_output=True, text=True, cwd=str(cwd), stdin=subprocess.DEVNULL,
    )


# ---------------------------------------------------------------------------
# Full-pack git mirror fixture
# ---------------------------------------------------------------------------


def build_git_mirror(dest: Path, branch: str = "release", omit=(), extra_files=None) -> Path:
    """Create a local git repo at `dest`: a snapshot of REPO_ROOT, committed on
    `branch`. Used as FRIDAY_CLONE_URL so full-pack tests never touch GitHub.

    `omit`: repo-relative paths removed before the commit, to exercise honest
    degrade branches (e.g. a missing CLAUDE.md.template or VERSION).
    `extra_files`: {relative_path: content} written before the commit.
    """
    shutil.copytree(
        REPO_ROOT,
        dest,
        ignore=shutil.ignore_patterns(".git", ".pytest_cache", "__pycache__", "*.pyc"),
    )
    for rel in omit:
        target = dest / rel
        if target.is_dir():
            shutil.rmtree(target)
        elif target.exists():
            target.unlink()
    if extra_files:
        for rel, content in extra_files.items():
            path = dest / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
    subprocess.run(["git", "init", "-q", "-b", branch, str(dest)], check=True)
    subprocess.run(["git", "-C", str(dest), "config", "user.email", "test@example.com"], check=True)
    subprocess.run(["git", "-C", str(dest), "config", "user.name", "Friday Foundation Tests"], check=True)
    subprocess.run(["git", "-C", str(dest), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(dest), "commit", "-q", "-m", "snapshot"], check=True)
    return dest


def run_full_pack(
    tmp_home: Path,
    mirror: Path,
    shortcuts_path: Path,
    branch: str = "release",
    context_url: str = None,
    lead: str = None,
) -> subprocess.CompletedProcess:
    """Run the no-argument (full-pack) install path against a local git
    mirror. stdin=DEVNULL guarantees the no-tty branch deterministically."""
    fake_bin = make_fake_claude(tmp_home / "bin")
    env = os.environ.copy()
    env["HOME"] = str(tmp_home)
    env["FRIDAY_CLONE_URL"] = f"file://{mirror}"
    env["FRIDAY_CLONE_BRANCH"] = branch
    env["FRIDAY_SHORTCUTS_PATH"] = str(shortcuts_path)
    env["PATH"] = fake_bin + ":" + env.get("PATH", "")
    if context_url:
        env["FRIDAY_CONTEXT_URL"] = context_url
    cmd = [BASH, str(INSTALL_SH)]
    if lead:
        cmd += ["--lead", lead]
    return subprocess.run(
        cmd, env=env, capture_output=True, text=True, cwd=str(tmp_home),
        stdin=subprocess.DEVNULL, timeout=60,
    )


# ---------------------------------------------------------------------------
# Full pack: clones the whole repo
# ---------------------------------------------------------------------------


def test_full_pack_clones_whole_repo(tmp_path):
    mirror = build_git_mirror(tmp_path / "mirror")
    tmp_home = tmp_path / "home"
    shortcuts = tmp_path / "friday-shortcuts"

    result = run_full_pack(tmp_home, mirror, shortcuts)
    assert result.returncode == 0, f"install failed:\n{result.stdout}\n{result.stderr}"

    assert (shortcuts / "commands").is_dir()
    assert (shortcuts / "harness").is_dir()
    assert (shortcuts / "tests").is_dir(), "whole repo means tests/ ships too"
    assert (shortcuts / ".github").is_dir(), "whole repo means .github/ ships too"
    assert (shortcuts / "README.md").exists()
    assert (shortcuts / "install.sh").exists()
    assert (shortcuts / ".git").is_dir(), "must be a real git clone, not a file copy"


def test_full_pack_path_has_no_space():
    """The install path is the literal folder name, never the display label."""
    content = INSTALL_SH.read_text()
    match = re.search(r'INSTALL_PATH="\$\{FRIDAY_SHORTCUTS_PATH:-(.+)\}"$', content, re.MULTILINE)
    assert match, "Could not find the INSTALL_PATH default assignment in install.sh"
    default_path = match.group(1)
    assert " " not in default_path, f"INSTALL_PATH default must have no space, got: {default_path!r}"
    assert default_path.endswith("/friday-shortcuts"), default_path


def test_full_pack_personalizes_brain_file_and_keeps_repo_guide(tmp_path):
    """The repo's own CLAUDE.md (contributor guide) is moved aside, and a
    fresh buyer CLAUDE.md is created from CLAUDE.md.template."""
    mirror = build_git_mirror(tmp_path / "mirror")
    tmp_home = tmp_path / "home"
    shortcuts = tmp_path / "friday-shortcuts"

    result = run_full_pack(tmp_home, mirror, shortcuts)
    assert result.returncode == 0, f"install failed:\n{result.stdout}\n{result.stderr}"

    repo_guide = shortcuts / "CLAUDE.md.repo-guide"
    buyer_claude_md = shortcuts / "CLAUDE.md"
    template = shortcuts / "CLAUDE.md.template"

    assert repo_guide.exists(), "the repo's own CLAUDE.md must be preserved as CLAUDE.md.repo-guide"
    assert "@AGENTS.md" in repo_guide.read_text(), "the moved-aside file must be the repo's contributor guide"

    assert buyer_claude_md.exists()
    assert buyer_claude_md.read_text() == template.read_text(), (
        "CLAUDE.md must be a fresh copy of the template, not the contributor guide"
    )

    agents_guide = shortcuts / "AGENTS.md.repo-guide"
    assert agents_guide.exists(), "AGENTS.md must also be moved aside for the same reason as CLAUDE.md"
    assert not (shortcuts / "AGENTS.md").exists()


def test_full_pack_installs_commands_folder_scoped(tmp_path):
    """Commands land inside ~/friday-shortcuts/.claude/commands/, so they
    only work when Claude Code is opened from inside that folder -- never
    a global sync into ~/.claude/commands/."""
    mirror = build_git_mirror(tmp_path / "mirror")
    tmp_home = tmp_path / "home"
    shortcuts = tmp_path / "friday-shortcuts"

    result = run_full_pack(tmp_home, mirror, shortcuts)
    assert result.returncode == 0, f"install failed:\n{result.stdout}\n{result.stderr}"

    commands_dir = shortcuts / ".claude" / "commands"
    expected = sorted(f.name for f in (REPO_ROOT / "commands").glob("*.md"))
    missing = [f for f in expected if not (commands_dir / f).exists()]
    assert not missing, f"Commands missing after install: {missing}"

    global_commands_dir = tmp_home / ".claude" / "commands"
    assert not global_commands_dir.exists(), (
        "full-pack install must never write into the global ~/.claude/commands/"
    )


def test_full_pack_activates_statusline_and_spinner_settings(tmp_path):
    mirror = build_git_mirror(tmp_path / "mirror")
    tmp_home = tmp_path / "home"
    shortcuts = tmp_path / "friday-shortcuts"

    result = run_full_pack(tmp_home, mirror, shortcuts)
    assert result.returncode == 0, f"install failed:\n{result.stdout}\n{result.stderr}"

    settings_path = shortcuts / ".claude" / "settings.json"
    assert settings_path.exists()
    import json

    settings = json.loads(settings_path.read_text())
    assert settings.get("statusLine", {}).get("type") == "command"
    assert settings["statusLine"]["command"] == str(shortcuts / "friday-statusline.sh")
    assert "spinnerVerbs" in settings, "statusLine merge must not clobber the spinner settings"

    script = shortcuts / "friday-statusline.sh"
    assert script.exists()
    assert os.access(script, os.X_OK), "friday-statusline.sh must be executable after install"


def test_full_pack_prints_version(tmp_path):
    mirror = build_git_mirror(tmp_path / "mirror")
    tmp_home = tmp_path / "home"
    shortcuts = tmp_path / "friday-shortcuts"

    result = run_full_pack(tmp_home, mirror, shortcuts)
    assert result.returncode == 0, f"install failed:\n{result.stdout}\n{result.stderr}"

    expected = (REPO_ROOT / "VERSION").read_text().strip()
    assert expected in result.stdout


def test_full_pack_honest_when_version_missing(tmp_path):
    mirror = build_git_mirror(tmp_path / "mirror", omit=["VERSION"])
    tmp_home = tmp_path / "home"
    shortcuts = tmp_path / "friday-shortcuts"

    result = run_full_pack(tmp_home, mirror, shortcuts)
    assert result.returncode == 0, "a missing VERSION must never fail the install"
    assert "unknown" in result.stdout.lower()


def test_full_pack_honest_when_template_missing(tmp_path):
    mirror = build_git_mirror(tmp_path / "mirror", omit=["CLAUDE.md.template"])
    tmp_home = tmp_path / "home"
    shortcuts = tmp_path / "friday-shortcuts"

    result = run_full_pack(tmp_home, mirror, shortcuts)
    assert result.returncode == 0, "a missing template must not fail the whole install"
    assert not (shortcuts / "CLAUDE.md").exists(), "no brain file should be created when the template is missing"
    assert "CLAUDE.md.template" in result.stdout


def test_full_pack_closing_message_is_three_step(tmp_path):
    mirror = build_git_mirror(tmp_path / "mirror")
    tmp_home = tmp_path / "home"
    shortcuts = tmp_path / "friday-shortcuts"

    result = run_full_pack(tmp_home, mirror, shortcuts)
    assert result.returncode == 0, f"install failed:\n{result.stdout}\n{result.stderr}"

    out = result.stdout
    for numbered in ["1. /amplify", "2. /voice-installer", "3. /brief"]:
        assert numbered in out, f"closing message missing ordered first-run step '{numbered}'"
    assert str(shortcuts) in out


def test_full_pack_no_tty_prints_cd_and_claude_instruction(tmp_path):
    mirror = build_git_mirror(tmp_path / "mirror")
    tmp_home = tmp_path / "home"
    shortcuts = tmp_path / "friday-shortcuts"

    result = run_full_pack(tmp_home, mirror, shortcuts)
    assert result.returncode == 0, f"install failed:\n{result.stdout}\n{result.stderr}"
    assert f"cd {shortcuts} && claude" in result.stdout


def test_tty_guard_uses_exec_open():
    """The /dev/tty guard must use exec open, not -r stat (matches the paid
    installer's pattern, copied deliberately)."""
    source = INSTALL_SH.read_text()
    assert "(exec 3</dev/tty)" in source
    assert "[ -r /dev/tty ]" not in source


def test_no_tty_branch_does_not_exec_claude():
    """The no-tty else branch must not exec claude -- only the interactive
    branch does. Source-level check (no pty harness in this repo's test
    suite), matching the precedent for the paid installer's identical pattern."""
    source = INSTALL_SH.read_text()
    exec_pos = source.rfind("exec claude </dev/tty")
    else_pos = source.find('echo "Open Claude Code from inside that folder:"')
    assert exec_pos != -1, "exec claude </dev/tty must exist for the interactive path"
    assert else_pos != -1, "the no-tty fallback message must exist"
    assert else_pos > exec_pos, "the no-tty branch must be the later (else) branch"


def test_full_pack_upgrade_preserves_personalisation_and_updates_foundation(tmp_path):
    """A re-run over an existing Friday Foundation git clone updates in
    place, not backup-then-reclone. The founder's personalised CLAUDE.md and
    their whole friday/ folder survive byte for byte, while Foundation's own
    tracked files (VERSION, a command) genuinely move to the new release."""
    mirror = build_git_mirror(tmp_path / "mirror")
    tmp_home = tmp_path / "home"
    shortcuts = tmp_path / "friday-shortcuts"

    r1 = run_full_pack(tmp_home, mirror, shortcuts)
    assert r1.returncode == 0, f"first install failed:\n{r1.stdout}\n{r1.stderr}"

    personalised = "# My own brain file\n\nI run a bookkeeping practice.\n"
    (shortcuts / "CLAUDE.md").write_text(personalised)

    sentinel = shortcuts / "friday" / "my-own-work.md"
    sentinel.parent.mkdir(parents=True, exist_ok=True)
    sentinel.write_text("do not lose this\n")

    # A new release lands: bump VERSION and change a command file upstream.
    (mirror / "VERSION").write_text("friday-foundation-v9.9.9\n")
    (mirror / "commands" / "decide.md").write_text(
        (mirror / "commands" / "decide.md").read_text() + "\n<!-- v9.9.9 marker -->\n"
    )
    subprocess.run(["git", "-C", str(mirror), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(mirror), "commit", "-q", "-m", "release bump"], check=True)

    r2 = run_full_pack(tmp_home, mirror, shortcuts)
    assert r2.returncode == 0, f"upgrade failed:\n{r2.stdout}\n{r2.stderr}"

    backups = sorted(tmp_path.glob("friday-shortcuts.bak-*"))
    assert not backups, "an upgrade over a valid git clone must not back up and reclone"

    assert (shortcuts / "CLAUDE.md").read_text() == personalised, (
        "the founder's personalised CLAUDE.md must survive an upgrade byte for byte"
    )
    assert sentinel.read_text() == "do not lose this\n", (
        "the founder's friday/ output must survive an upgrade byte for byte"
    )
    assert "friday-foundation-v9.9.9" in (shortcuts / "VERSION").read_text(), (
        "Foundation's own tracked VERSION must actually update to the new release"
    )
    assert "v9.9.9 marker" in (shortcuts / ".claude" / "commands" / "decide.md").read_text(), (
        "an updated command file must reach the folder-scoped .claude/commands/ too"
    )


def test_full_pack_reinstall_over_non_git_folder_falls_back_to_backup_and_reclone(tmp_path):
    """A hand-made or corrupted ~/friday-shortcuts (no .git) is not a
    Friday Foundation git clone, so the installer falls back to the old
    backup-then-clone-fresh path rather than failing or updating garbage."""
    mirror = build_git_mirror(tmp_path / "mirror")
    tmp_home = tmp_path / "home"
    shortcuts = tmp_path / "friday-shortcuts"

    shortcuts.mkdir(parents=True)
    (shortcuts / "hand-made.txt").write_text("not a git clone\n")

    result = run_full_pack(tmp_home, mirror, shortcuts)
    assert result.returncode == 0, f"install failed:\n{result.stdout}\n{result.stderr}"

    backups = sorted(tmp_path.glob("friday-shortcuts.bak-*"))
    assert backups, "a non-git-clone folder must be backed up, not silently discarded"
    assert (backups[-1] / "hand-made.txt").read_text() == "not a git clone\n"
    assert (shortcuts / ".git").is_dir(), "the fallback install must be a real git clone"
    assert "not a Friday Foundation git clone" in result.stdout


def test_full_pack_clone_failure_is_honest(tmp_path):
    """A bad clone URL/branch exits 1 with a clear retry instruction, and
    leaves no partial folder behind."""
    tmp_home = tmp_path / "home"
    shortcuts = tmp_path / "friday-shortcuts"
    fake_bin = make_fake_claude(tmp_home / "bin")
    env = os.environ.copy()
    env["HOME"] = str(tmp_home)
    env["FRIDAY_CLONE_URL"] = f"file://{tmp_path}/does-not-exist"
    env["FRIDAY_SHORTCUTS_PATH"] = str(shortcuts)
    env["PATH"] = fake_bin + ":" + env.get("PATH", "")

    result = subprocess.run(
        [BASH, str(INSTALL_SH)], env=env, capture_output=True, text=True,
        cwd=str(tmp_home), stdin=subprocess.DEVNULL, timeout=60,
    )
    assert result.returncode != 0
    assert re.search(r"[Rr]e-run", result.stdout)
    assert not shortcuts.exists(), "a failed clone must not leave a partial folder"


def test_missing_git_exits_1_for_full_pack_only(tmp_path):
    """git is required for the full-pack path but not for single-capability."""
    tmp_home = tmp_path / "home"
    cwd = tmp_path / "cwd"
    tmp_home.mkdir()
    cwd.mkdir()

    result = run_install_custom_path(tmp_home, cwd, ["bash", "curl", "claude"])
    assert result.returncode == 1, f"missing git must exit 1 for full pack:\n{result.stdout}\n{result.stderr}"
    assert "git" in (result.stdout + result.stderr).lower()


# ---------------------------------------------------------------------------
# --lead flag: pre-filled CLAUDE.md, now inside the cloned folder
# ---------------------------------------------------------------------------


def test_lead_flag_prefills_claude_md_from_context_endpoint(tmp_path):
    mirror = build_git_mirror(tmp_path / "mirror")
    tmp_home = tmp_path / "home"
    shortcuts = tmp_path / "friday-shortcuts"

    context_dir = tmp_path / "context"
    context_dir.mkdir()
    (context_dir / "lead-abc").write_text(
        "# Priya's AI Chief of Staff\n\nWho I am: I am Priya's AI Chief of Staff for a bookkeeping practice.\n"
    )
    context_httpd, context_port = start_local_server(context_dir)
    context_url = f"http://127.0.0.1:{context_port}"

    try:
        result = run_full_pack(tmp_home, mirror, shortcuts, context_url=context_url, lead="lead-abc")
        assert result.returncode == 0, f"install failed:\n{result.stdout}\n{result.stderr}"

        claude_md = (shortcuts / "CLAUDE.md").read_text()
        assert "Priya" in claude_md
        assert "bookkeeping practice" in claude_md
    finally:
        context_httpd.shutdown()
        context_httpd.server_close()


def test_lead_flag_falls_back_to_template_on_bogus_token(tmp_path):
    mirror = build_git_mirror(tmp_path / "mirror")
    tmp_home = tmp_path / "home"
    shortcuts = tmp_path / "friday-shortcuts"

    context_dir = tmp_path / "context"  # empty: every id 404s
    context_dir.mkdir()
    context_httpd, context_port = start_local_server(context_dir)
    context_url = f"http://127.0.0.1:{context_port}"

    try:
        result = run_full_pack(tmp_home, mirror, shortcuts, context_url=context_url, lead="bogus-token")
        assert result.returncode == 0, f"install must still exit 0:\n{result.stdout}\n{result.stderr}"

        claude_md = (shortcuts / "CLAUDE.md").read_text()
        template = (shortcuts / "CLAUDE.md.template").read_text()
        assert claude_md == template
    finally:
        context_httpd.shutdown()
        context_httpd.server_close()


def test_lead_flag_alone_still_installs_full_pack(tmp_path):
    mirror = build_git_mirror(tmp_path / "mirror")
    tmp_home = tmp_path / "home"
    shortcuts = tmp_path / "friday-shortcuts"

    context_dir = tmp_path / "context"
    context_dir.mkdir()
    context_httpd, context_port = start_local_server(context_dir)
    context_url = f"http://127.0.0.1:{context_port}"

    try:
        result = run_full_pack(tmp_home, mirror, shortcuts, context_url=context_url, lead="any-token")
        assert result.returncode == 0, f"install failed:\n{result.stdout}\n{result.stderr}"

        commands_dir = shortcuts / ".claude" / "commands"
        expected = sorted(f.name for f in (REPO_ROOT / "commands").glob("*.md"))
        missing = [f for f in expected if not (commands_dir / f).exists()]
        assert not missing, f"Commands missing after --lead install: {missing}"
    finally:
        context_httpd.shutdown()
        context_httpd.server_close()


# ---------------------------------------------------------------------------
# README: full-pack behaviour description and release-branch pin
# ---------------------------------------------------------------------------


def test_repo_raw_defaults_to_release():
    """install.sh's REPO_RAW default must point at the release branch, not main."""
    content = INSTALL_SH.read_text()
    match = re.search(
        r'REPO_RAW="\$\{FRIDAY_REPO_RAW:-(https://raw\.githubusercontent\.com/[^}]+)\}"',
        content,
    )
    assert match, "Could not find the REPO_RAW default assignment in install.sh"
    default_url = match.group(1)
    assert default_url.endswith("/release"), (
        f"install.sh REPO_RAW default must end in /release, got: {default_url}"
    )


def test_clone_branch_defaults_to_release():
    content = INSTALL_SH.read_text()
    match = re.search(r'CLONE_BRANCH="\$\{FRIDAY_CLONE_BRANCH:-([^}]+)\}"', content)
    assert match, "Could not find the CLONE_BRANCH default assignment in install.sh"
    assert match.group(1).strip('"') == "release"


def test_readme_primary_install_oneliner_uses_release():
    readme_text = (REPO_ROOT / "README.md").read_text()
    assert "/release/install.sh" in readme_text
    assert "/main/install.sh" not in readme_text


def test_readme_describes_the_single_folder_flow():
    plain = re.sub(r"[`*]", "", (REPO_ROOT / "README.md").read_text())
    assert "friday-shortcuts" in plain, "README must describe the ~/friday-shortcuts folder"


def test_manual_brain_file_step_is_accurate():
    plain = re.sub(r"[`]", "", (REPO_ROOT / "docs" / "foundation-manual.md").read_text())
    assert "installer copies it to CLAUDE.md" in plain
    assert "reads CLAUDE.md (not the template)" in plain


# ---------------------------------------------------------------------------
# Story 4.1 (retained): install.sh failure semantics
# ---------------------------------------------------------------------------


def test_install_wraps_all_logic_in_main():
    """A curl|bash download cut off mid-transfer must not half-run. main() is
    defined, it is invoked only on the final meaningful line, and NO
    side-effecting statement sits at the top level, so a truncated pipe
    reaches no work before main."""
    lines = INSTALL_SH.read_text().splitlines()
    assert any(re.match(r"^main\s*\(\)\s*\{", line) for line in lines), "install.sh must define main()"
    meaningful = [line for line in lines if line.strip() and not line.strip().startswith("#")]
    assert meaningful[-1].strip() == 'main "$@"', (
        f'install.sh must end by invoking main "$@"; last meaningful line is {meaningful[-1]!r}'
    )
    allowed = [
        re.compile(r"^#"),
        re.compile(r"^set\s"),
        re.compile(r"^[A-Za-z_][A-Za-z0-9_]*\+?="),
        re.compile(r"^\)\s*$"),
        re.compile(r"^[A-Za-z_][A-Za-z0-9_]*\s*\(\)\s*\{"),
        re.compile(r"^\}\s*$"),
        re.compile(r'^main\s+"\$@"\s*$'),
    ]
    offenders = [
        line for line in lines
        if line and not line[0].isspace() and not any(p.match(line) for p in allowed)
    ]
    assert not offenders, (
        "install.sh runs logic at the top level; it must live inside main() so a "
        f"truncated curl|bash never half-runs it: {offenders}"
    )


def test_missing_curl_exits_1():
    with tempfile.TemporaryDirectory() as tmp:
        tmp_home = Path(tmp) / "home"
        cwd = Path(tmp) / "project"
        tmp_home.mkdir()
        cwd.mkdir()

        result = run_install_custom_path(tmp_home, cwd, ["bash"])
        assert result.returncode == 1, f"missing curl must exit 1:\n{result.stdout}\n{result.stderr}"
        assert "curl" in (result.stdout + result.stderr).lower(), "the message must name curl"


def test_missing_claude_exits_1():
    with tempfile.TemporaryDirectory() as tmp:
        tmp_home = Path(tmp) / "home"
        cwd = Path(tmp) / "project"
        tmp_home.mkdir()
        cwd.mkdir()

        result = run_install_custom_path(tmp_home, cwd, ["bash", "curl"])
        assert result.returncode == 1, f"missing claude must exit 1:\n{result.stdout}\n{result.stderr}"
        assert "claude" in (result.stdout + result.stderr).lower(), "the message must name claude"


def test_unknown_capability_exits_1():
    with tempfile.TemporaryDirectory() as tmp:
        tmp_home = Path(tmp) / "home"
        cwd = Path(tmp) / "project"
        tmp_home.mkdir()
        cwd.mkdir()

        result = run_install(tmp_home, cwd, "http://127.0.0.1:9/unused", capability="definitely-not-a-command")
        assert result.returncode == 1, f"unknown capability must exit 1:\n{result.stdout}\n{result.stderr}"
        assert "Available:" in result.stdout, "must print the Available list"


# ---------------------------------------------------------------------------
# Single-capability path (unchanged: one HTTP file fetch into cwd)
# ---------------------------------------------------------------------------


def test_install_single_capability():
    httpd, port = start_local_server(REPO_ROOT)
    repo_raw = f"http://127.0.0.1:{port}"

    try:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_home = Path(tmp) / "home"
            cwd = Path(tmp) / "project"
            tmp_home.mkdir()
            cwd.mkdir()

            result = run_install(tmp_home, cwd, repo_raw, capability="decide")
            assert result.returncode == 0, f"Single install failed:\n{result.stdout}\n{result.stderr}"

            commands_dir = tmp_home / ".claude" / "commands"
            assert (commands_dir / "decide.md").exists(), "decide.md not installed"
            assert not (commands_dir / "brief.md").exists(), (
                "brief.md should not be installed in single-capability mode"
            )
    finally:
        httpd.shutdown()
        httpd.server_close()


def test_install_continues_past_missing_command_file():
    """A 404 on the requested single command exits 1 with a clear message."""
    with tempfile.TemporaryDirectory() as tmp:
        served = Path(tmp) / "served"
        served.mkdir()
        (served / "commands").mkdir()
        for f in (REPO_ROOT / "commands").glob("*.md"):
            if f.name != "decide.md":
                shutil.copy2(f, served / "commands" / f.name)
        httpd, port = start_local_server(served)
        repo_raw = f"http://127.0.0.1:{port}"

        try:
            tmp_home = Path(tmp) / "home"
            cwd = Path(tmp) / "project"
            tmp_home.mkdir()
            cwd.mkdir()

            result = run_install(tmp_home, cwd, repo_raw, capability="decide")
            assert result.returncode != 0, "a missing command file must make the installer exit non-zero"
            assert re.search(r"[Rr]e-run", result.stdout), "the summary must give a one-line retry instruction"
        finally:
            httpd.shutdown()
            httpd.server_close()


def test_backup_on_differing_overwrite():
    """AC5: a locally-modified command file is backed up to .md.bak, not clobbered."""
    httpd, port = start_local_server(REPO_ROOT)
    repo_raw = f"http://127.0.0.1:{port}"

    try:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_home = Path(tmp) / "home"
            cwd = Path(tmp) / "project"
            tmp_home.mkdir()
            cwd.mkdir()

            r1 = run_install(tmp_home, cwd, repo_raw, capability="decide")
            assert r1.returncode == 0, f"first install failed:\n{r1.stdout}\n{r1.stderr}"

            commands_dir = tmp_home / ".claude" / "commands"
            target = commands_dir / "decide.md"
            server_version = target.read_text()
            target.write_text("# my local edits\n")  # diverge from upstream

            r2 = run_install(tmp_home, cwd, repo_raw, capability="decide")
            assert r2.returncode == 0, f"second install failed:\n{r2.stdout}\n{r2.stderr}"

            bak = commands_dir / "decide.md.bak"
            assert bak.exists(), "a differing existing file must be backed up to .md.bak"
            assert bak.read_text() == "# my local edits\n", "the .bak must hold the user's prior content"
            assert target.read_text() == server_version, "the fresh copy must overwrite after the backup"
    finally:
        httpd.shutdown()
        httpd.server_close()


def test_no_bak_on_identical_rerun():
    """AC5: re-running with unchanged upstream content leaves no .bak litter."""
    httpd, port = start_local_server(REPO_ROOT)
    repo_raw = f"http://127.0.0.1:{port}"

    try:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_home = Path(tmp) / "home"
            cwd = Path(tmp) / "project"
            tmp_home.mkdir()
            cwd.mkdir()

            assert run_install(tmp_home, cwd, repo_raw, capability="decide").returncode == 0
            assert run_install(tmp_home, cwd, repo_raw, capability="decide").returncode == 0

            commands_dir = tmp_home / ".claude" / "commands"
            baks = list(commands_dir.glob("*.bak"))
            assert not baks, f"identical re-run must not create .bak files, found {baks}"
    finally:
        httpd.shutdown()
        httpd.server_close()


def test_version_file_shape():
    """Unit check: VERSION follows the friday-foundation-vX.Y.Z convention
    used by the other Friday products (friday-mk-i-vX.Y.Z, friday-mk-v-vX.Y.Z)."""
    version_file = REPO_ROOT / "VERSION"
    assert version_file.exists(), "VERSION file is missing from the repo root"
    content = version_file.read_text().strip()
    assert re.match(r"^friday-foundation-v\d+\.\d+\.\d+$", content), (
        f"VERSION must read friday-foundation-vX.Y.Z, got {content!r}"
    )
