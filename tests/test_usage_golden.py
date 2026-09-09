"""End-to-end proof that a real install, a real /decide prompt, and a real
Write to friday/decisions.md produce exactly three messages at the
receiving server, none of them carrying the prompt tail. Uses the same
git-mirror + local-HTTP-server fixtures as test_install.py, imported
directly rather than duplicated."""
import http.server
import json
import subprocess
import threading
import time
from pathlib import Path

from tests.test_install import BASH, INSTALL_SH, build_git_mirror, make_fake_claude

REAL_PROMPT_JSON = {
    "session_id": "9f2b1c4d-golden",
    "transcript_path": "/dev/null",
    "cwd": "PLACEHOLDER",
    "prompt_id": "p1",
    "permission_mode": "default",
    "hook_event_name": "UserPromptSubmit",
    "prompt": "/decide should I hire Sarah",
}

REAL_WRITE_JSON = {
    "session_id": "9f2b1c4d-golden",
    "cwd": "PLACEHOLDER",
    "hook_event_name": "PostToolUse",
    "tool_name": "Write",
    "tool_input": {"file_path": "PLACEHOLDER/friday/decisions.md", "content": "irrelevant"},
    "tool_response": {"ok": True},
}


def test_three_messages_reach_the_server(tmp_path):
    received = []

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_POST(self):
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            received.append(json.loads(body))
            self.send_response(200)
            self.end_headers()

        def log_message(self, *a):
            pass

    httpd = http.server.HTTPServer(("127.0.0.1", 0), Handler)
    port = httpd.server_address[1]
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    usage_url = f"http://127.0.0.1:{port}"

    mirror = build_git_mirror(tmp_path / "mirror")
    tmp_home = tmp_path / "home"
    tmp_home.mkdir()
    bin_dir = tmp_home / "bin"
    for name in ("bash", "git", "curl", "python3"):
        import shutil
        src = shutil.which(name)
        bin_dir.mkdir(exist_ok=True, parents=True)
        (bin_dir / name).symlink_to(src)
    make_fake_claude(bin_dir)
    import os
    env = os.environ.copy()
    env["HOME"] = str(tmp_home)
    env["PATH"] = str(bin_dir) + ":" + env.get("PATH", "")
    env["FRIDAY_CLONE_URL"] = str(mirror)
    env["FRIDAY_CLONE_BRANCH"] = "release"
    env["FRIDAY_USAGE_URL"] = usage_url
    try:
        install_result = subprocess.run(
            [BASH, str(INSTALL_SH)], env=env, capture_output=True, text=True,
            cwd=str(tmp_home), stdin=subprocess.DEVNULL,
        )
        assert install_result.returncode == 0

        # report_install backgrounds its curl POST so install.sh's own exit code
        # is never blocked on it (spec 4.2). In real use a founder cannot open
        # Claude Code and type a command before the CLI has even finished
        # printing "All done", so the install message always lands first; here
        # the two events are milliseconds apart, so wait for it to actually
        # reach the server before firing the hook events below, or the install
        # message's own OS-detection subprocess call can lose the race to the
        # hook messages' faster path.
        for _ in range(30):
            if len(received) >= 1:
                break
            time.sleep(0.1)

        install_dir = tmp_home / "friday-shortcuts"
        prompt_json = dict(REAL_PROMPT_JSON, cwd=str(install_dir))
        write_json = dict(REAL_WRITE_JSON, cwd=str(install_dir))
        write_json["tool_input"] = {
            "file_path": str(install_dir / "friday" / "decisions.md"),
            "content": "irrelevant",
        }

        result = subprocess.run(
            ["bash", str(install_dir / "friday-usage.sh")],
            input=json.dumps(prompt_json), cwd=str(install_dir),
            env={"PATH": env["PATH"], "FRIDAY_USAGE_URL": usage_url},
            capture_output=True, text=True, timeout=5,
        )
        assert result.returncode == 0

        # Wait for the command message to arrive before firing the output message,
        # to enforce ordering deterministically rather than relying on timing.
        for _ in range(30):
            if len(received) >= 2:
                break
            time.sleep(0.1)

        result = subprocess.run(
            ["bash", str(install_dir / "friday-usage.sh")],
            input=json.dumps(write_json), cwd=str(install_dir),
            env={"PATH": env["PATH"], "FRIDAY_USAGE_URL": usage_url},
            capture_output=True, text=True, timeout=5,
        )
        assert result.returncode == 0

        for _ in range(30):
            if len(received) >= 3:
                break
            time.sleep(0.1)

        assert len(received) == 3
        events = [m["event"] for m in received]
        assert events == ["install", "command", "output"]
        assert received[1]["command"] == "decide"
        assert received[2]["output_file"] == "decisions.md"
        for message in received:
            body_text = json.dumps(message)
            for forbidden in ("should", "hire", "Sarah"):
                assert forbidden not in body_text

        receipt_path = install_dir / "friday" / "usage-sent.jsonl"
        receipt_lines = [json.loads(line) for line in receipt_path.read_text().splitlines() if line]
        assert len(receipt_lines) == 3
        for line in receipt_lines:
            body_text = json.dumps(line)
            for forbidden in ("should", "hire", "Sarah"):
                assert forbidden not in body_text
    finally:
        httpd.shutdown()
