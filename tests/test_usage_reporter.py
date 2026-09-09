"""Unit tests for friday-usage.sh. Every test runs the real script via
subprocess with an isolated temp cwd (never the repo root) and an
unroutable FRIDAY_USAGE_URL, so no test can ever reach the real production
endpoint. The receipt file is written before any network attempt (see the
script's own header comment), so these tests never need a live server --
tests/test_usage_golden.py covers the real POST separately."""
import json
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SCRIPT = REPO_ROOT / "friday-usage.sh"
UNROUTABLE_URL = "http://127.0.0.1:1"


def run_hook(tmp_path: Path, stdin_json: dict, install_id: str = "test-install-id") -> subprocess.CompletedProcess:
    if install_id is not None:
        (tmp_path / "friday").mkdir(exist_ok=True)
        (tmp_path / "friday" / ".install-id").write_text(install_id)
    env = {"PATH": "/usr/bin:/bin:/usr/local/bin", "FRIDAY_USAGE_URL": UNROUTABLE_URL}
    return subprocess.run(
        ["bash", str(SCRIPT)],
        input=json.dumps(stdin_json),
        cwd=str(tmp_path),
        env=env,
        capture_output=True,
        text=True,
        timeout=5,
    )


def receipt_lines(tmp_path: Path) -> list[dict]:
    path = tmp_path / "friday" / "usage-sent.jsonl"
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line]


from contextlib import contextmanager
import tempfile


@contextmanager
def subprocess_tmp_install():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d)
        (p / "friday").mkdir()
        (p / "friday" / ".install-id").write_text("test-install-id")
        yield p


def test_command_event_keeps_only_the_name(tmp_path):
    result = run_hook(tmp_path, {
        "hook_event_name": "UserPromptSubmit",
        "prompt": "/decide should I hire Sarah",
        "session_id": "abc123",
    })
    assert result.returncode == 0
    lines = receipt_lines(tmp_path)
    assert len(lines) == 1
    assert lines[0]["event"] == "command"
    assert lines[0]["command"] == "decide"
    body_text = json.dumps(lines[0])
    for forbidden in ("should", "hire", "Sarah"):
        assert forbidden not in body_text


def test_custom_command_masked(tmp_path):
    result = run_hook(tmp_path, {
        "hook_event_name": "UserPromptSubmit",
        "prompt": "/pitch-acme-corp draft",
        "session_id": "abc123",
    })
    assert result.returncode == 0
    lines = receipt_lines(tmp_path)
    assert lines[0]["command"] == "custom"
    body_text = json.dumps(lines[0])
    assert "acme" not in body_text.lower()


def test_non_slash_prompt_posts_nothing(tmp_path):
    result = run_hook(tmp_path, {
        "hook_event_name": "UserPromptSubmit",
        "prompt": "hello there",
        "session_id": "abc123",
    })
    assert result.returncode == 0
    assert receipt_lines(tmp_path) == []


def test_missing_install_id_is_silent(tmp_path):
    result = run_hook(tmp_path, {
        "hook_event_name": "UserPromptSubmit",
        "prompt": "/decide anything",
        "session_id": "abc123",
    }, install_id=None)
    assert result.returncode == 0
    assert receipt_lines(tmp_path) == []


def test_malformed_stdin_exits_zero(tmp_path):
    (tmp_path / "friday").mkdir()
    (tmp_path / "friday" / ".install-id").write_text("test-install-id")
    env = {"PATH": "/usr/bin:/bin:/usr/local/bin", "FRIDAY_USAGE_URL": UNROUTABLE_URL}
    result = subprocess.run(
        ["bash", str(SCRIPT)],
        input="{not valid json",
        cwd=str(tmp_path),
        env=env,
        capture_output=True,
        text=True,
        timeout=5,
    )
    assert result.returncode == 0
    assert receipt_lines(tmp_path) == []


def run_write(tmp_path: Path, file_path: str, install_id: str = "test-install-id") -> subprocess.CompletedProcess:
    return run_hook(tmp_path, {
        "hook_event_name": "PostToolUse",
        "tool_name": "Write",
        "tool_input": {"file_path": file_path, "content": "irrelevant"},
        "session_id": "abc123",
        "cwd": str(tmp_path),
    }, install_id=install_id)


def test_output_event_known_file(tmp_path):
    result = run_write(tmp_path, str(tmp_path / "friday" / "decisions.md"))
    assert result.returncode == 0
    lines = receipt_lines(tmp_path)
    assert lines[0]["event"] == "output"
    assert lines[0]["output_file"] == "decisions.md"


def test_output_event_folder_forms(tmp_path):
    result = run_write(tmp_path, str(tmp_path / "friday" / "sops" / "Onboarding Sarah.md"))
    assert result.returncode == 0
    lines = receipt_lines(tmp_path)
    assert lines[0]["output_file"] == "sops"
    body_text = json.dumps(lines[0])
    assert "Sarah" not in body_text
    assert "Onboarding" not in body_text


def test_output_event_teaching_folder_form(tmp_path):
    result = run_write(tmp_path, str(tmp_path / "friday" / "teaching" / "New hire.md"))
    assert result.returncode == 0
    assert receipt_lines(tmp_path)[0]["output_file"] == "teaching"


def test_output_event_new_capability_folder_form(tmp_path):
    result = run_write(tmp_path, str(tmp_path / "commands" / "my-command.md"))
    assert result.returncode == 0
    assert receipt_lines(tmp_path)[0]["output_file"] == "new-capability"


def test_output_event_unknown_path_posts_nothing(tmp_path):
    result = run_write(tmp_path, str(tmp_path / "notes" / "private.md"))
    assert result.returncode == 0
    assert receipt_lines(tmp_path) == []


def test_output_event_outside_install_folder_posts_nothing(tmp_path):
    outside = tmp_path.parent / "not-the-install-folder" / "voice.md"
    result = run_write(tmp_path, str(outside))
    assert result.returncode == 0
    assert receipt_lines(tmp_path) == []


def test_output_event_sops_folder_outside_friday_posts_nothing(tmp_path):
    result = run_write(tmp_path, str(tmp_path / "other" / "sops" / "x.md"))
    assert result.returncode == 0
    assert receipt_lines(tmp_path) == []


def test_output_event_nested_commands_path_posts_nothing(tmp_path):
    result = run_write(tmp_path, str(tmp_path / "commands" / "nested" / "x.md"))
    assert result.returncode == 0
    assert receipt_lines(tmp_path) == []


def test_output_event_ignores_non_write_tool(tmp_path):
    result = run_hook(tmp_path, {
        "hook_event_name": "PostToolUse",
        "tool_name": "Bash",
        "tool_input": {"command": "rm -rf /tmp/x"},
        "session_id": "abc123",
    })
    assert result.returncode == 0
    assert receipt_lines(tmp_path) == []


def test_curl_absent_exits_zero_fast_and_writes_receipt(tmp_path):
    import time
    (tmp_path / "friday").mkdir()
    (tmp_path / "friday" / ".install-id").write_text("test-install-id")
    env = {"PATH": str(tmp_path / "empty-bin"), "FRIDAY_USAGE_URL": UNROUTABLE_URL}
    (tmp_path / "empty-bin").mkdir()
    # python3 and cat must still resolve (the script's bash preamble shells
    # out to cat to capture stdin); curl is the one binary deliberately
    # left off this PATH.
    import shutil as _shutil
    for _name in ("python3", "cat"):
        (tmp_path / "empty-bin" / _name).symlink_to(_shutil.which(_name))
    # bash itself must be resolved by absolute path: the child's PATH is
    # deliberately restricted to empty-bin (python3 and cat only, curl
    # absent), so a bare "bash" argument would fail PATH lookup before the
    # script runs.
    bash_path = _shutil.which("bash")
    start = time.monotonic()
    result = subprocess.run(
        [bash_path, str(SCRIPT)],
        input=json.dumps({
            "hook_event_name": "UserPromptSubmit", "prompt": "/decide x", "session_id": "s",
        }),
        cwd=str(tmp_path), env=env, capture_output=True, text=True, timeout=5,
    )
    elapsed = time.monotonic() - start
    assert result.returncode == 0
    assert elapsed < 1.0
    assert receipt_lines(tmp_path)[0]["command"] == "decide"


def test_receipt_trims_to_500_only_past_600(tmp_path):
    # 600 existing lines + 1 new append = 601, past RECEIPT_TRIM_THRESHOLD,
    # so this write must trigger the temp-file-plus-rename trim to the
    # last 500 -- spec 3.6's "when the file passes 600 lines" (amended
    # 2026-09-08). This was already true under the old always-cap-at-500
    # design for this specific input, but the new threshold is what the
    # next test below locks in as the real, distinguishing behavior.
    (tmp_path / "friday").mkdir()
    (tmp_path / "friday" / ".install-id").write_text("test-install-id")
    receipt = tmp_path / "friday" / "usage-sent.jsonl"
    receipt.write_text("\n".join(json.dumps({"n": i}) for i in range(600)) + "\n")
    run_hook(tmp_path, {
        "hook_event_name": "UserPromptSubmit", "prompt": "/decide x", "session_id": "s",
    })
    lines = receipt_lines(tmp_path)
    assert len(lines) == 500
    assert lines[-1]["command"] == "decide"
    assert lines[0] == {"n": 101}


def test_receipt_not_trimmed_below_600(tmp_path):
    # 550 existing lines + 1 new append = 551, at or under the 600-line
    # threshold, so no trim runs and the file simply grows -- this is the
    # behavior spec 3.6's amendment changed (the old design capped at 500
    # on every single write; the new design only rewrites the file once it
    # passes 600, an intentional loosening to make every normal write a
    # single >>-style append with no read-the-whole-file cost).
    (tmp_path / "friday").mkdir()
    (tmp_path / "friday" / ".install-id").write_text("test-install-id")
    receipt = tmp_path / "friday" / "usage-sent.jsonl"
    receipt.write_text("\n".join(json.dumps({"n": i}) for i in range(550)) + "\n")
    run_hook(tmp_path, {
        "hook_event_name": "UserPromptSubmit", "prompt": "/decide x", "session_id": "s",
    })
    lines = receipt_lines(tmp_path)
    assert len(lines) == 551
    assert lines[0] == {"n": 0}
    assert lines[-1]["command"] == "decide"


def test_allowlist_matches_commands_folder():
    real_slugs = {p.stem for p in (REPO_ROOT / "commands").glob("*.md")}
    assert len(real_slugs) == 25
    for slug in sorted(real_slugs):
        with subprocess_tmp_install() as tmp_path:
            result = run_hook(tmp_path, {
                "hook_event_name": "UserPromptSubmit", "prompt": f"/{slug} x", "session_id": "s",
            })
            assert result.returncode == 0
            assert receipt_lines(tmp_path)[0]["command"] == slug, slug
    with subprocess_tmp_install() as tmp_path:
        run_hook(tmp_path, {
            "hook_event_name": "UserPromptSubmit", "prompt": "/not-a-real-command x", "session_id": "s",
        })
        assert receipt_lines(tmp_path)[0]["command"] == "custom"


def test_output_allowlist_matches_spec(tmp_path):
    flat_names = [
        "growth.md", "morning.md", "changelog.md", "competitive-analysis.md",
        "customer-feedback.md", "decisions.md", "idea-exploration.md",
        "upgrade-log.md", "learnings.md", "meetings.md", "offer.md",
        "positioning.md", "pricing.md", "product-hunt-launch.md",
        "risk-register.md", "roadmap.md", "shipping-retro.md", "voice.md",
        "review.md", "scope-decision.md", "validation.md", "gtm-plan.md",
    ]
    assert len(flat_names) == 22
    for name in flat_names:
        with subprocess_tmp_install() as tmp_path2:
            result = run_write(tmp_path2, str(tmp_path2 / "friday" / name))
            assert receipt_lines(tmp_path2)[0]["output_file"] == name, name


def test_script_has_no_dashes_and_passes_cleanroom():
    text = SCRIPT.read_text(encoding="utf-8")
    assert "\u2014" not in text  # em dash literal excluded from this plan doc
    assert "\u2013" not in text  # en dash literal excluded from this plan doc
    import sys
    sys.path.insert(0, str(REPO_ROOT))
    from tests.test_cleanroom import check_file
    assert check_file(SCRIPT) == []


def run_install_mode(tmp_path: Path, version="friday-foundation-v1.3.0", previous="", lead="", install_id="test-install-id"):
    if install_id is not None:
        (tmp_path / "friday").mkdir(exist_ok=True)
        (tmp_path / "friday" / ".install-id").write_text(install_id)
    (tmp_path / "VERSION").write_text(version)
    env = {"PATH": "/usr/bin:/bin:/usr/local/bin", "FRIDAY_USAGE_URL": UNROUTABLE_URL}
    return subprocess.run(
        ["bash", str(SCRIPT), "install", version, previous, lead],
        cwd=str(tmp_path), env=env, capture_output=True, text=True, timeout=5,
    )


def test_install_mode_reports_install_event(tmp_path):
    result = run_install_mode(tmp_path)
    assert result.returncode == 0
    lines = receipt_lines(tmp_path)
    assert lines[0]["event"] == "install"
    assert lines[0]["version"] == "friday-foundation-v1.3.0"
    assert lines[0]["os"] in ("macos", "linux", "wsl2")
    assert "lead" not in lines[0]
    assert "previous_version" not in lines[0]


def test_install_mode_carries_lead_only_when_given(tmp_path):
    # The receipt never holds a usable token (spec 3.6, amended
    # 2026-09-08): write_receipt redacts lead to "present" on its own
    # local copy of the message. The real token still reaches the network
    # -- Task 6's test_install_message_carries_lead_only_when_given proves
    # that against a capture server, since Task 4's tests use an
    # unroutable URL and cannot observe the POST body themselves.
    result = run_install_mode(tmp_path, lead="lead-token-abc")
    assert result.returncode == 0
    assert receipt_lines(tmp_path)[0]["lead"] == "present"


def test_install_mode_carries_previous_version_on_upgrade(tmp_path):
    result = run_install_mode(tmp_path, previous="friday-foundation-v1.2.2")
    assert result.returncode == 0
    assert receipt_lines(tmp_path)[0]["previous_version"] == "friday-foundation-v1.2.2"


def test_install_mode_missing_install_id_is_silent(tmp_path):
    result = run_install_mode(tmp_path, install_id=None)
    assert result.returncode == 0
    assert receipt_lines(tmp_path) == []


def test_install_mode_empty_version_is_silent(tmp_path):
    result = run_install_mode(tmp_path, version="")
    assert result.returncode == 0
    assert receipt_lines(tmp_path) == []
