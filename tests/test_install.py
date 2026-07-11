"""
install.sh integration tests:
- Real run against a local HTTP server (not just unit-test in isolation)
- Commands land in DEST
- CLAUDE.md.template and harness/ land in CWD
- Re-run replaces files (idempotency -- no duplicates)
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
    """Serve `directory` over HTTP on a random loopback port. Returns (httpd, port).

    One server, bound and served. (An earlier version bound a throwaway socket
    it never served or closed; that leaked a port on every call.)
    """
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


def build_served_repo(dest: Path, omit=()):
    """Mirror the installer-fetched surface (commands/, harness/, template) into
    `dest`, skipping any repo-relative paths in `omit` so they 404 when served."""
    omit = set(omit)
    shutil.copytree(REPO_ROOT / "commands", dest / "commands")
    shutil.copytree(REPO_ROOT / "harness", dest / "harness")
    shutil.copy2(REPO_ROOT / "CLAUDE.md.template", dest / "CLAUDE.md.template")
    for rel in omit:
        target = dest / rel
        if target.exists():
            target.unlink()
    return dest


def run_install_custom_path(tmp_home: Path, cwd: Path, tool_names, capability: str = ""):
    """Run install.sh with PATH holding ONLY symlinks to the named host tools.

    Lets a test withhold `curl` or `claude` deterministically to exercise the
    prerequisite gates, regardless of what is installed on the test host.
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
    return subprocess.run(cmd, env=env, capture_output=True, text=True, cwd=str(cwd))


def make_fake_claude(bin_dir: Path):
    """Write a minimal fake 'claude' binary so the installer's check passes."""
    bin_dir.mkdir(parents=True, exist_ok=True)
    fake = bin_dir / "claude"
    fake.write_text("#!/bin/sh\necho 'claude-code-fake'\n")
    fake.chmod(0o755)
    return str(bin_dir)


def run_install(tmp_home: Path, cwd: Path, repo_raw_url: str, capability: str = "") -> subprocess.CompletedProcess:
    """Run install.sh with isolated HOME and FRIDAY_REPO_RAW override."""
    fake_bin = make_fake_claude(tmp_home / "bin")
    env = os.environ.copy()
    env["HOME"] = str(tmp_home)
    env["FRIDAY_REPO_RAW"] = repo_raw_url
    env["PATH"] = fake_bin + ":" + env.get("PATH", "")

    cmd = [BASH, str(INSTALL_SH)]
    if capability:
        cmd.append(capability)

    return subprocess.run(
        cmd,
        env=env,
        capture_output=True,
        text=True,
        cwd=str(cwd),
    )


def test_install_full_pack_lands_commands():
    """Full-pack install places all command files in ~/.claude/commands/."""
    httpd, port = start_local_server(REPO_ROOT)
    repo_raw = f"http://127.0.0.1:{port}"

    try:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_home = Path(tmp) / "home"
            cwd = Path(tmp) / "project"
            tmp_home.mkdir()
            cwd.mkdir()

            result = run_install(tmp_home, cwd, repo_raw)
            assert result.returncode == 0, f"install.sh failed:\n{result.stdout}\n{result.stderr}"

            commands_dir = tmp_home / ".claude" / "commands"
            expected = sorted(f.name for f in (REPO_ROOT / "commands").glob("*.md"))
            missing = [f for f in expected if not (commands_dir / f).exists()]
            assert not missing, f"Commands missing after install: {missing}"
    finally:
        httpd.shutdown()
        httpd.server_close()


def test_install_fetches_claude_md_template():
    """Full-pack install fetches CLAUDE.md.template to the current working directory."""
    httpd, port = start_local_server(REPO_ROOT)
    repo_raw = f"http://127.0.0.1:{port}"

    try:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_home = Path(tmp) / "home"
            cwd = Path(tmp) / "project"
            tmp_home.mkdir()
            cwd.mkdir()

            result = run_install(tmp_home, cwd, repo_raw)
            assert result.returncode == 0, f"install.sh failed:\n{result.stdout}\n{result.stderr}"

            template = cwd / "CLAUDE.md.template"
            assert template.exists(), "CLAUDE.md.template was not fetched to cwd"
            assert template.stat().st_size > 100, "CLAUDE.md.template is suspiciously empty"
    finally:
        httpd.shutdown()
        httpd.server_close()


def test_install_fetches_harness():
    """Full-pack install fetches the harness/ guide docs to the current working directory."""
    httpd, port = start_local_server(REPO_ROOT)
    repo_raw = f"http://127.0.0.1:{port}"

    try:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_home = Path(tmp) / "home"
            cwd = Path(tmp) / "project"
            tmp_home.mkdir()
            cwd.mkdir()

            result = run_install(tmp_home, cwd, repo_raw)
            assert result.returncode == 0, f"install.sh failed:\n{result.stdout}\n{result.stderr}"

            harness = cwd / "harness"
            assert harness.exists(), "harness/ directory was not created in cwd"
            expected_harness = [
                "00-how-friday-works.md",
                "01-add-a-command.md",
                "02-add-an-agent.md",
                "03-connect-your-own-tools.md",
                "04-the-friday-folder.md",
                "05-the-amplify-logic.md",
            ]
            missing = [f for f in expected_harness if not (harness / f).exists()]
            assert not missing, f"Harness docs missing after install: {missing}"
    finally:
        httpd.shutdown()
        httpd.server_close()


def test_install_idempotency():
    """Running install.sh twice replaces files, never duplicates content."""
    httpd, port = start_local_server(REPO_ROOT)
    repo_raw = f"http://127.0.0.1:{port}"

    try:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_home = Path(tmp) / "home"
            cwd = Path(tmp) / "project"
            tmp_home.mkdir()
            cwd.mkdir()

            # First run
            r1 = run_install(tmp_home, cwd, repo_raw)
            assert r1.returncode == 0, f"First install failed:\n{r1.stdout}\n{r1.stderr}"

            commands_dir = tmp_home / ".claude" / "commands"
            sizes_after_first = {f.name: f.stat().st_size for f in commands_dir.glob("*.md")}
            template_size_1 = (cwd / "CLAUDE.md.template").stat().st_size

            # Second run
            r2 = run_install(tmp_home, cwd, repo_raw)
            assert r2.returncode == 0, f"Second install failed:\n{r2.stdout}\n{r2.stderr}"

            sizes_after_second = {f.name: f.stat().st_size for f in commands_dir.glob("*.md")}
            template_size_2 = (cwd / "CLAUDE.md.template").stat().st_size

            # Same files, same sizes -- idempotent
            assert sizes_after_first == sizes_after_second, (
                "File sizes changed between first and second install (possible duplication)"
            )
            assert template_size_1 == template_size_2, (
                "CLAUDE.md.template size changed between runs (possible duplication)"
            )
    finally:
        httpd.shutdown()
        httpd.server_close()


def test_repo_raw_defaults_to_release():
    """install.sh's REPO_RAW default must point at the release branch, not main.

    Guards AC2.3: the installer distributes from `release`, so a merge to
    `main` does not ship until a maintainer deliberately promotes it.
    """
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


def test_readme_primary_install_oneliner_uses_release():
    """README's install one-liners must point at /release/install.sh, and no
    pasteable /main/install.sh one-liner may remain.

    Guards against a future edit silently repointing distribution back at
    the integration branch (AC2.3).
    """
    readme_text = (REPO_ROOT / "README.md").read_text()
    assert "/release/install.sh" in readme_text, (
        "README must reference /release/install.sh"
    )
    assert "/main/install.sh" not in readme_text, (
        "README must not leave a pasteable /main/install.sh one-liner"
    )


def test_install_closing_message_is_three_step():
    """The full-pack close guides to three first-run commands and prints the absolute project dir."""
    httpd, port = start_local_server(REPO_ROOT)
    repo_raw = f"http://127.0.0.1:{port}"

    try:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_home = Path(tmp) / "home"
            cwd = Path(tmp) / "project"
            tmp_home.mkdir()
            cwd.mkdir()

            result = run_install(tmp_home, cwd, repo_raw)
            assert result.returncode == 0, f"install failed:\n{result.stdout}\n{result.stderr}"

            out = result.stdout
            # The numbered prefixes lock both presence and the amplify-first order.
            for numbered in ["1. /amplify", "2. /voice-installer", "3. /brief"]:
                assert numbered in out, f"closing message missing ordered first-run step '{numbered}'"
            assert str(cwd) in out or str(cwd.resolve()) in out, (
                "closing message must print the absolute project directory"
            )
            # The old wall of every command on its own line is gone.
            per_command_lines = re.findall(r'^\s{2}/[a-z0-9-]+\s{2,}', out, re.MULTILINE)
            assert not per_command_lines, (
                f"closing message should not re-list every command, found {per_command_lines}"
            )
    finally:
        httpd.shutdown()
        httpd.server_close()


def test_install_creates_brain_file_when_absent():
    """CLAUDE.md is created from the template when the project has none."""
    httpd, port = start_local_server(REPO_ROOT)
    repo_raw = f"http://127.0.0.1:{port}"

    try:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_home = Path(tmp) / "home"
            cwd = Path(tmp) / "project"
            tmp_home.mkdir()
            cwd.mkdir()

            result = run_install(tmp_home, cwd, repo_raw)
            assert result.returncode == 0, f"install failed:\n{result.stdout}\n{result.stderr}"

            claude_md = cwd / "CLAUDE.md"
            template = cwd / "CLAUDE.md.template"
            assert claude_md.exists(), "CLAUDE.md was not created from the template"
            assert template.exists(), "CLAUDE.md.template should still be saved alongside"
            assert claude_md.read_text() == template.read_text(), (
                "CLAUDE.md should be a byte copy of the template on first install"
            )
    finally:
        httpd.shutdown()
        httpd.server_close()


def test_install_preserves_existing_brain_file():
    """A pre-existing CLAUDE.md survives a full-pack install byte-identical."""
    httpd, port = start_local_server(REPO_ROOT)
    repo_raw = f"http://127.0.0.1:{port}"

    try:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_home = Path(tmp) / "home"
            cwd = Path(tmp) / "project"
            tmp_home.mkdir()
            cwd.mkdir()

            sentinel = "# My own brain file\nDo not overwrite me.\n"
            (cwd / "CLAUDE.md").write_text(sentinel)

            result = run_install(tmp_home, cwd, repo_raw)
            assert result.returncode == 0, f"install failed:\n{result.stdout}\n{result.stderr}"

            assert (cwd / "CLAUDE.md").read_text() == sentinel, "existing CLAUDE.md must not be touched"
            assert (cwd / "CLAUDE.md.template").exists(), "template should still be saved alongside"
    finally:
        httpd.shutdown()
        httpd.server_close()


def test_readme_first_run_guidance():
    """README tells users to cd into their project dir and that skipping voice is safe."""
    plain = re.sub(r"[`*]", "", (REPO_ROOT / "README.md").read_text()).lower()
    assert "cd into your project" in plain, "README must tell users to cd into their project directory"
    assert "skipping" in plain and "neutral" in plain, (
        "README must reassure that skipping voice falls back to a neutral style"
    )


def test_manual_brain_file_step_is_accurate():
    """The manual says the template becomes CLAUDE.md and that Claude Code reads CLAUDE.md, not the template."""
    plain = re.sub(r"[`]", "", (REPO_ROOT / "docs" / "foundation-manual.md").read_text())
    assert "installer copies it to CLAUDE.md" in plain, (
        "manual must state the installer copies the template to CLAUDE.md"
    )
    assert "reads CLAUDE.md (not the template)" in plain, (
        "manual must clarify Claude Code reads CLAUDE.md, not the template"
    )


def test_install_single_capability():
    """Single-capability install places only that command file."""
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
            # Other commands should not be installed
            assert not (commands_dir / "brief.md").exists(), (
                "brief.md should not be installed in single-capability mode"
            )
    finally:
        httpd.shutdown()
        httpd.server_close()


# ---------------------------------------------------------------------------
# Story 4.1: install.sh failure semantics
# ---------------------------------------------------------------------------

def test_install_wraps_all_logic_in_main():
    """AC1: a curl|bash download cut off mid-transfer must not half-run. main() is
    defined, it is invoked only on the final meaningful line, and NO side-effecting
    statement sits at the top level, so a truncated pipe reaches no work before main."""
    lines = INSTALL_SH.read_text().splitlines()
    assert any(re.match(r"^main\s*\(\)\s*\{", line) for line in lines), "install.sh must define main()"
    meaningful = [line for line in lines if line.strip() and not line.strip().startswith("#")]
    assert meaningful[-1].strip() == 'main "$@"', (
        f'install.sh must end by invoking main "$@"; last meaningful line is {meaningful[-1]!r}'
    )
    # Every column-0 (top-level) statement must be inert: a comment, `set`, an
    # assignment (scalar or array, including the array's closing paren), a function
    # definition or close, or the single `main "$@"` call. Anything else would run
    # during a truncated download before main() is ever reached.
    allowed = [
        re.compile(r"^#"),                                    # comment or shebang
        re.compile(r"^set\s"),                                # set -euo pipefail
        re.compile(r"^[A-Za-z_][A-Za-z0-9_]*\+?="),           # scalar or array assignment
        re.compile(r"^\)\s*$"),                               # close of a multi-line array
        re.compile(r"^[A-Za-z_][A-Za-z0-9_]*\s*\(\)\s*\{"),   # function definition header
        re.compile(r"^\}\s*$"),                               # function close
        re.compile(r'^main\s+"\$@"\s*$'),                     # the single top-level call
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
    """AC2: with no curl on PATH, the installer exits 1 naming curl, before any download."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_home = Path(tmp) / "home"
        cwd = Path(tmp) / "project"
        tmp_home.mkdir()
        cwd.mkdir()

        result = run_install_custom_path(tmp_home, cwd, ["bash"])
        assert result.returncode == 1, f"missing curl must exit 1:\n{result.stdout}\n{result.stderr}"
        assert "curl" in (result.stdout + result.stderr).lower(), "the message must name curl"


def test_missing_claude_exits_1():
    """AC2 sibling: curl present but no claude exits 1 naming claude (matches the pre-existing gate)."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_home = Path(tmp) / "home"
        cwd = Path(tmp) / "project"
        tmp_home.mkdir()
        cwd.mkdir()

        result = run_install_custom_path(tmp_home, cwd, ["bash", "curl"])
        assert result.returncode == 1, f"missing claude must exit 1:\n{result.stdout}\n{result.stderr}"
        assert "claude" in (result.stdout + result.stderr).lower(), "the message must name claude"


def test_unknown_capability_exits_1():
    """An unknown capability name exits 1 and prints the Available list, before any download."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_home = Path(tmp) / "home"
        cwd = Path(tmp) / "project"
        tmp_home.mkdir()
        cwd.mkdir()

        result = run_install(tmp_home, cwd, "http://127.0.0.1:9/unused", capability="definitely-not-a-command")
        assert result.returncode == 1, f"unknown capability must exit 1:\n{result.stdout}\n{result.stderr}"
        assert "Available:" in result.stdout, "must print the Available list"


def test_install_continues_past_missing_command_file():
    """AC3: one 404 mid-pack does not abort. Other files install, the failure is
    named with a retry instruction, and the exit code is non-zero."""
    with tempfile.TemporaryDirectory() as tmp:
        served = Path(tmp) / "served"
        served.mkdir()
        build_served_repo(served, omit=["commands/decide.md"])
        httpd, port = start_local_server(served)
        repo_raw = f"http://127.0.0.1:{port}"

        try:
            tmp_home = Path(tmp) / "home"
            cwd = Path(tmp) / "project"
            tmp_home.mkdir()
            cwd.mkdir()

            result = run_install(tmp_home, cwd, repo_raw)
            assert result.returncode != 0, "a missing command file must make the installer exit non-zero"
            out = result.stdout
            assert "decide.md" in out, "the summary must name the file that failed"
            assert re.search(r"[Rr]e-run", out), "the summary must give a one-line retry instruction"

            commands_dir = tmp_home / ".claude" / "commands"
            assert (commands_dir / "brief.md").exists(), "other commands must still install past the failure"
            assert not (commands_dir / "decide.md").exists(), "the failed command must not be left behind"
        finally:
            httpd.shutdown()
            httpd.server_close()


def test_install_honest_close_when_template_missing():
    """AC4: if the template 404s, the close is honest (no 'All done'), names the
    failure, creates no brain file, and exits non-zero."""
    with tempfile.TemporaryDirectory() as tmp:
        served = Path(tmp) / "served"
        served.mkdir()
        build_served_repo(served, omit=["CLAUDE.md.template"])
        httpd, port = start_local_server(served)
        repo_raw = f"http://127.0.0.1:{port}"

        try:
            tmp_home = Path(tmp) / "home"
            cwd = Path(tmp) / "project"
            tmp_home.mkdir()
            cwd.mkdir()

            result = run_install(tmp_home, cwd, repo_raw)
            assert result.returncode != 0, "a missing template must make the installer exit non-zero"
            assert "All done" not in result.stdout, "must not claim success while the template is missing"
            assert "CLAUDE.md.template" in result.stdout, "the summary must name the missing template"
            assert not (cwd / "CLAUDE.md").exists(), "no brain file should be created when the template failed"
        finally:
            httpd.shutdown()
            httpd.server_close()


def test_install_honest_close_when_harness_file_missing():
    """AC4 (harness leg): if a harness guide file 404s, the close is honest (no
    'All done'), names the missing file with a retry line, and exits non-zero."""
    with tempfile.TemporaryDirectory() as tmp:
        served = Path(tmp) / "served"
        served.mkdir()
        build_served_repo(served, omit=["harness/00-how-friday-works.md"])
        httpd, port = start_local_server(served)
        repo_raw = f"http://127.0.0.1:{port}"

        try:
            tmp_home = Path(tmp) / "home"
            cwd = Path(tmp) / "project"
            tmp_home.mkdir()
            cwd.mkdir()

            result = run_install(tmp_home, cwd, repo_raw)
            assert result.returncode != 0, "a missing harness file must make the installer exit non-zero"
            assert "All done" not in result.stdout, "must not claim success while a harness file is missing"
            assert "00-how-friday-works.md" in result.stdout, "the summary must name the missing harness file"
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

            r1 = run_install(tmp_home, cwd, repo_raw)
            assert r1.returncode == 0, f"first install failed:\n{r1.stdout}\n{r1.stderr}"

            commands_dir = tmp_home / ".claude" / "commands"
            target = commands_dir / "decide.md"
            server_version = target.read_text()
            target.write_text("# my local edits\n")  # diverge from upstream

            r2 = run_install(tmp_home, cwd, repo_raw)
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

            assert run_install(tmp_home, cwd, repo_raw).returncode == 0
            assert run_install(tmp_home, cwd, repo_raw).returncode == 0

            commands_dir = tmp_home / ".claude" / "commands"
            baks = list(commands_dir.glob("*.bak"))
            assert not baks, f"identical re-run must not create .bak files, found {baks}"
    finally:
        httpd.shutdown()
        httpd.server_close()
