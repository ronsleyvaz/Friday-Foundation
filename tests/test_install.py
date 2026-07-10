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
import subprocess
import tempfile
import threading
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
INSTALL_SH = REPO_ROOT / "install.sh"


def start_local_server(directory: Path):
    """Serve the repo directory over HTTP on a random port. Returns (httpd, port)."""
    handler_class = http.server.SimpleHTTPRequestHandler

    class QuietHandler(handler_class):
        def log_message(self, format, *args):
            pass  # suppress stdout noise during tests

    httpd = http.server.HTTPServer(("127.0.0.1", 0), QuietHandler)
    httpd.directory = str(directory)

    # Override the handler's translate_path to serve from repo root.
    original_init = QuietHandler.__init__

    class RepoHandler(QuietHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(directory), **kwargs)

    httpd2 = http.server.HTTPServer(("127.0.0.1", 0), RepoHandler)
    port = httpd2.server_address[1]
    thread = threading.Thread(target=httpd2.serve_forever, daemon=True)
    thread.start()
    return httpd2, port


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

    cmd = ["bash", str(INSTALL_SH)]
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
