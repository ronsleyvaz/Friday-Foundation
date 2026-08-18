"""
Spinner settings install tests: install.sh gives Claude Code Friday's own
spinner words and tips, scoped to the project's own ./.claude/settings.json,
never the founder's global config.

Golden tests run the real installer against a temp directory and read the
produced file off disk (same pattern as tests/test_install.py). Unit tests
check the template's own content: verb parity against the shipped Mk5 list,
tip-to-command membership, and JSON shape.
"""
import http.server
import json
import os
import re
import shutil
import subprocess
import tempfile
import threading
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
INSTALL_SH = REPO_ROOT / "install.sh"
TEMPLATE = REPO_ROOT / "spinner-settings.json.template"
COMMANDS_DIR = REPO_ROOT / "commands"

# Canonical Mk5 buyer settings, source of the 51 verbs. Lives on the `serve`
# worktree of the Friday repo, not the `main` worktree the sprint brief named
# (that copy predates the commit that added spinnerVerbs). See build report.
MK5_SETTINGS = Path(
    "/Users/ronsley/Projects/Friday-serve/workstreams/new/mk-v-full-build/"
    "code/.claude/settings.json"
)

BASH = os.environ.get("FRIDAY_TEST_BASH", "bash")


def start_local_server(directory: Path):
    class RepoHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(directory), **kwargs)

        def log_message(self, *args):
            pass

    httpd = http.server.HTTPServer(("127.0.0.1", 0), RepoHandler)
    port = httpd.server_address[1]
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    return httpd, port


def make_fake_claude(bin_dir: Path):
    bin_dir.mkdir(parents=True, exist_ok=True)
    fake = bin_dir / "claude"
    fake.write_text("#!/bin/sh\necho 'claude-code-fake'\n")
    fake.chmod(0o755)
    return str(bin_dir)


def run_install(tmp_home: Path, cwd: Path, repo_raw_url: str, extra_path="") -> subprocess.CompletedProcess:
    """Run install.sh with isolated HOME and FRIDAY_REPO_RAW override.

    extra_path, if given, is prepended to PATH -- used to withhold python3 by
    building a PATH that only has curl/claude/bash symlinked in.
    """
    fake_bin = make_fake_claude(tmp_home / "bin")
    env = os.environ.copy()
    env["HOME"] = str(tmp_home)
    env["FRIDAY_REPO_RAW"] = repo_raw_url
    if extra_path:
        env["PATH"] = extra_path
    else:
        env["PATH"] = fake_bin + ":" + env.get("PATH", "")

    return subprocess.run(
        [BASH, str(INSTALL_SH)],
        env=env,
        capture_output=True,
        text=True,
        cwd=str(cwd),
    )


def run_install_without_python3(tmp_home: Path, cwd: Path, repo_raw_url: str) -> subprocess.CompletedProcess:
    """Build a PATH holding symlinks to every host tool install.sh actually
    calls -- bash, curl, and the coreutils install_one/awk parsing needs --
    but deliberately no python3, so the installer's own python3 gate is
    exercised deterministically rather than accidentally testing a PATH
    missing tools unrelated to this feature."""
    bin_dir = tmp_home / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    for name in ("bash", "curl", "mkdir", "mktemp", "mv", "rm", "cmp", "awk", "date", "cp", "cat"):
        src = shutil.which(name)
        assert src, f"host is missing required tool for this test: {name}"
        (bin_dir / name).symlink_to(src)
    make_fake_claude(bin_dir)
    env = {"HOME": str(tmp_home), "PATH": str(bin_dir), "FRIDAY_REPO_RAW": repo_raw_url}
    return subprocess.run(
        [BASH, str(INSTALL_SH)],
        env=env,
        capture_output=True,
        text=True,
        cwd=str(cwd),
    )


# ---------------------------------------------------------------------------
# AC1: fresh install into an empty directory
# ---------------------------------------------------------------------------

def test_fresh_install_creates_settings_with_spinner_keys():
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

            settings_path = cwd / ".claude" / "settings.json"
            assert settings_path.exists(), "./.claude/settings.json was not created"
            data = json.loads(settings_path.read_text())

            assert data["spinnerVerbs"]["mode"] == "replace"
            mk5 = json.loads(MK5_SETTINGS.read_text())
            assert data["spinnerVerbs"]["verbs"] == mk5["spinnerVerbs"]["verbs"], (
                "verbs must be byte-identical to the shipped Mk5 list"
            )
            assert len(data["spinnerVerbs"]["verbs"]) == 51

            assert data["spinnerTipsOverride"]["excludeDefault"] is True
            tips = data["spinnerTipsOverride"]["tips"]
            assert 12 <= len(tips) <= 16, f"expected 12-16 tips, got {len(tips)}"
    finally:
        httpd.shutdown()
        httpd.server_close()


# ---------------------------------------------------------------------------
# AC2: existing settings.json with unrelated keys
# ---------------------------------------------------------------------------

def test_existing_settings_with_unrelated_keys_gets_merged_with_backup():
    httpd, port = start_local_server(REPO_ROOT)
    repo_raw = f"http://127.0.0.1:{port}"
    try:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_home = Path(tmp) / "home"
            cwd = Path(tmp) / "project"
            tmp_home.mkdir()
            cwd.mkdir()
            claude_dir = cwd / ".claude"
            claude_dir.mkdir()
            original = {
                "agent": "some-other-agent",
                "env": {"SOME_FLAG": "1"},
                "statusLine": {"type": "command", "command": "./my-line.sh"},
            }
            settings_path = claude_dir / "settings.json"
            settings_path.write_text(json.dumps(original, indent=2) + "\n")

            result = run_install(tmp_home, cwd, repo_raw)
            assert result.returncode == 0, f"install failed:\n{result.stdout}\n{result.stderr}"

            data = json.loads(settings_path.read_text())
            for key, value in original.items():
                assert data[key] == value, f"existing key {key!r} was not preserved"
            assert "spinnerVerbs" in data
            assert "spinnerTipsOverride" in data

            backups = list(claude_dir.glob("settings.json.pre-friday-*.bak"))
            assert backups, "no backup file was written"
            backed_up = json.loads(backups[0].read_text())
            assert backed_up == original, "backup must hold the pre-merge content"
    finally:
        httpd.shutdown()
        httpd.server_close()


# ---------------------------------------------------------------------------
# AC3: existing settings.json already has spinnerVerbs
# ---------------------------------------------------------------------------

def test_existing_spinner_verbs_leaves_file_byte_identical():
    httpd, port = start_local_server(REPO_ROOT)
    repo_raw = f"http://127.0.0.1:{port}"
    try:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_home = Path(tmp) / "home"
            cwd = Path(tmp) / "project"
            tmp_home.mkdir()
            cwd.mkdir()
            claude_dir = cwd / ".claude"
            claude_dir.mkdir()
            settings_path = claude_dir / "settings.json"
            original_text = json.dumps(
                {"spinnerVerbs": {"mode": "replace", "verbs": ["Custom"]}}, indent=2
            ) + "\n"
            settings_path.write_text(original_text)

            result = run_install(tmp_home, cwd, repo_raw)
            assert result.returncode == 0, f"install failed:\n{result.stdout}\n{result.stderr}"

            assert settings_path.read_text() == original_text, (
                "a settings.json that already opts into spinnerVerbs must not change at all"
            )
            no_backups = list(claude_dir.glob("settings.json.pre-friday-*.bak"))
            assert not no_backups, "no backup should be written when nothing changed"
    finally:
        httpd.shutdown()
        httpd.server_close()


def test_existing_spinner_tips_override_also_leaves_file_untouched():
    """AC3 sibling: spinnerTipsOverride alone (no spinnerVerbs) is also a stop sign."""
    httpd, port = start_local_server(REPO_ROOT)
    repo_raw = f"http://127.0.0.1:{port}"
    try:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_home = Path(tmp) / "home"
            cwd = Path(tmp) / "project"
            tmp_home.mkdir()
            cwd.mkdir()
            claude_dir = cwd / ".claude"
            claude_dir.mkdir()
            settings_path = claude_dir / "settings.json"
            original_text = json.dumps(
                {"spinnerTipsOverride": {"excludeDefault": True, "tips": ["Custom tip."]}},
                indent=2,
            ) + "\n"
            settings_path.write_text(original_text)

            result = run_install(tmp_home, cwd, repo_raw)
            assert result.returncode == 0

            assert settings_path.read_text() == original_text
    finally:
        httpd.shutdown()
        httpd.server_close()


# ---------------------------------------------------------------------------
# AC4: python3 unavailable
# ---------------------------------------------------------------------------

def test_missing_python3_skips_merge_but_installs_cleanly():
    httpd, port = start_local_server(REPO_ROOT)
    repo_raw = f"http://127.0.0.1:{port}"
    try:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_home = Path(tmp) / "home"
            cwd = Path(tmp) / "project"
            tmp_home.mkdir()
            cwd.mkdir()
            claude_dir = cwd / ".claude"
            claude_dir.mkdir()
            settings_path = claude_dir / "settings.json"
            original_text = json.dumps({"agent": "keep-me"}, indent=2) + "\n"
            settings_path.write_text(original_text)

            result = run_install_without_python3(tmp_home, cwd, repo_raw)
            assert result.returncode == 0, f"install must still exit 0:\n{result.stdout}\n{result.stderr}"
            assert "python3" in result.stdout.lower(), "must tell the user python3 was the reason"
            assert "skip" in result.stdout.lower(), "must say the spinner settings step was skipped"

            # existing file must survive untouched -- no half-merge without python3
            assert settings_path.read_text() == original_text
            assert (cwd / "spinner-settings.json.template").exists(), (
                "the template should still be left alongside for a manual merge"
            )
    finally:
        httpd.shutdown()
        httpd.server_close()


def test_missing_python3_on_fresh_install_still_creates_settings():
    """A brand-new .claude/settings.json is a plain file copy -- it needs no
    JSON parsing, so it must succeed even without python3 on PATH."""
    httpd, port = start_local_server(REPO_ROOT)
    repo_raw = f"http://127.0.0.1:{port}"
    try:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_home = Path(tmp) / "home"
            cwd = Path(tmp) / "project"
            tmp_home.mkdir()
            cwd.mkdir()

            result = run_install_without_python3(tmp_home, cwd, repo_raw)
            assert result.returncode == 0, f"install must still exit 0:\n{result.stdout}\n{result.stderr}"

            settings_path = cwd / ".claude" / "settings.json"
            assert settings_path.exists()
            data = json.loads(settings_path.read_text())
            assert data["spinnerVerbs"]["mode"] == "replace"
    finally:
        httpd.shutdown()
        httpd.server_close()


# ---------------------------------------------------------------------------
# AC5-7: template content -- tip membership, verb parity, JSON shape
# ---------------------------------------------------------------------------

def _shipped_command_slugs():
    return {p.stem for p in COMMANDS_DIR.glob("*.md")}


def test_template_is_valid_json_with_correct_shape():
    assert TEMPLATE.exists(), "spinner-settings.json.template is missing"
    data = json.loads(TEMPLATE.read_text())

    assert set(data.keys()) == {"spinnerVerbs", "spinnerTipsOverride"}

    assert data["spinnerVerbs"]["mode"] == "replace"
    verbs = data["spinnerVerbs"]["verbs"]
    assert isinstance(verbs, list) and verbs, "verbs must be a non-empty array"
    assert all(isinstance(v, str) for v in verbs), "every verb must be a string"

    assert data["spinnerTipsOverride"]["excludeDefault"] is True
    tips = data["spinnerTipsOverride"]["tips"]
    assert isinstance(tips, list) and tips, "tips must be a non-empty array"
    assert all(isinstance(t, str) for t in tips), "every tip must be a string"


def test_verbs_match_shipped_mk5_list_byte_for_byte():
    data = json.loads(TEMPLATE.read_text())
    mk5 = json.loads(MK5_SETTINGS.read_text())
    assert data["spinnerVerbs"]["verbs"] == mk5["spinnerVerbs"]["verbs"]
    assert len(data["spinnerVerbs"]["verbs"]) == 51


def test_tip_count_in_range():
    data = json.loads(TEMPLATE.read_text())
    tips = data["spinnerTipsOverride"]["tips"]
    assert 12 <= len(tips) <= 16, f"expected 12-16 tips, got {len(tips)}"


def test_every_tip_names_a_shipped_command():
    """AC5: derive the shipped set from commands/*.md, not a hardcoded list."""
    shipped = _shipped_command_slugs()
    data = json.loads(TEMPLATE.read_text())
    tips = data["spinnerTipsOverride"]["tips"]

    command_pattern = re.compile(r"/([a-z0-9][a-z0-9-]*)")
    offenders = []
    for tip in tips:
        match = command_pattern.search(tip)
        if not match or match.group(1) not in shipped:
            offenders.append(tip)
    assert not offenders, f"tips naming a command Foundation does not ship: {offenders}"


def test_negative_case_unshipped_command_would_fail_membership_check():
    """Proves the membership check in the previous test actually discriminates,
    not just a tautology that always passes."""
    shipped = _shipped_command_slugs()
    fake_tip = "Use /this-command-does-not-exist to do something."
    command_pattern = re.compile(r"/([a-z0-9][a-z0-9-]*)")
    match = command_pattern.search(fake_tip)
    assert match and match.group(1) not in shipped, (
        "sanity check failed -- the fake command must not be in the shipped set"
    )


# ---------------------------------------------------------------------------
# AC3 (fix): a no-op install must leave no new files behind at all, not even
# a backup that gets cleaned up again later. The prior implementation wrote
# the backup before checking whether spinner settings already existed, so a
# process killed between the backup and the cleanup left a stray .bak.
# ---------------------------------------------------------------------------

def test_noop_install_leaves_no_new_files_behind():
    """A settings.json that already opts into spinnerVerbs must come out of
    the install with the exact same set of files in .claude/ it started
    with -- no backup ever written, not just one cleaned up afterward."""
    httpd, port = start_local_server(REPO_ROOT)
    repo_raw = f"http://127.0.0.1:{port}"
    try:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_home = Path(tmp) / "home"
            cwd = Path(tmp) / "project"
            tmp_home.mkdir()
            cwd.mkdir()
            claude_dir = cwd / ".claude"
            claude_dir.mkdir()
            settings_path = claude_dir / "settings.json"
            settings_path.write_text(
                json.dumps({"spinnerVerbs": {"mode": "replace", "verbs": ["Custom"]}}, indent=2) + "\n"
            )

            before = sorted(p.name for p in claude_dir.iterdir())

            result = run_install(tmp_home, cwd, repo_raw)
            assert result.returncode == 0, f"install failed:\n{result.stdout}\n{result.stderr}"

            after = sorted(p.name for p in claude_dir.iterdir())
            assert after == before, (
                f"no-op install must leave no new files behind, found {sorted(set(after) - set(before))}"
            )
    finally:
        httpd.shutdown()
        httpd.server_close()
