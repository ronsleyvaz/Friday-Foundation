#!/usr/bin/env bash
# Friday SHORTCUTS usage reporter. Two jobs, nothing else:
#  1. Hook mode (default, no arguments): read one Claude Code hook payload
#     on stdin, decide whether it is a slash command or a known output
#     write, and report a content-free usage message.
#  2. Install mode (`friday-usage.sh install <version> <previous_version>
#     <lead_token>`): reports the one-time install message. Called by
#     install.sh's report_install step; never run standalone by a founder.
#
# Both modes share the same receipt file, the same allowlists, and the
# same fail-open posture: no curl, no python3, no install ID, malformed
# input -- exit 0, nothing sent, no retry, no queue. Never prints anything
# and never returns context to Claude.
#
# Message shapes: see docs/superpowers/specs/2026-09-08-shortcuts-usage-
# learning-design.md section 3 in the operator repo (not shipped here).
#
# Target URL: FRIDAY_USAGE_URL, default https://friday.amplifyais.com/api/shortcuts/usage.
# The override exists for tests only and is not documented for founders.

set -u

if ! command -v python3 >/dev/null 2>&1; then
  exit 0
fi

FRIDAY_USAGE_STDIN="$(cat 2>/dev/null || true)"
FRIDAY_USAGE_URL="${FRIDAY_USAGE_URL:-https://friday.amplifyais.com/api/shortcuts/usage}"
FRIDAY_USAGE_MODE="${1:-hook}"
FRIDAY_USAGE_ARG2="${2:-}"
FRIDAY_USAGE_ARG3="${3:-}"
FRIDAY_USAGE_ARG4="${4:-}"

export FRIDAY_USAGE_STDIN FRIDAY_USAGE_URL FRIDAY_USAGE_MODE FRIDAY_USAGE_ARG2 FRIDAY_USAGE_ARG3 FRIDAY_USAGE_ARG4

python3 - <<'PYEOF'
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone

COMMANDS = {
    "amplify", "brief", "changelog", "competitive-analysis", "customer-feedback",
    "decide", "delegation-brief", "explore-idea", "friday-upgrade", "go-to-market",
    "learnings", "meetingprep", "new-capability", "offer-creation", "positioning",
    "pricing-strategy", "product-hunt-launch", "risk-register", "roadmap",
    "scope-decision", "shipping-retro", "sop-builder", "teach-team",
    "validate-idea", "voice-installer", "weeklyreview",
}

OUTPUT_FILES = {
    "growth.md", "morning.md", "changelog.md", "competitive-analysis.md",
    "customer-feedback.md", "decisions.md", "idea-exploration.md",
    "upgrade-log.md", "learnings.md", "meetings.md", "offer.md",
    "positioning.md", "pricing.md", "product-hunt-launch.md",
    "risk-register.md", "roadmap.md", "shipping-retro.md", "voice.md",
    "review.md", "scope-decision.md", "validation.md", "gtm-plan.md",
}


def detect_os():
    if sys.platform == "darwin":
        version = ""
        try:
            out = subprocess.run(
                ["sw_vers", "-productVersion"], capture_output=True, stdin=subprocess.DEVNULL, text=True, timeout=1,
            )
            version = out.stdout.strip().split(".")[0]
        except Exception:
            version = ""
        return "macos", version
    try:
        with open("/proc/version", encoding="utf-8", errors="replace") as f:
            proc_version = f.read().lower()
    except OSError:
        proc_version = ""
    os_name = "wsl2" if "microsoft" in proc_version else "linux"
    version = ""
    try:
        with open("/etc/os-release", encoding="utf-8", errors="replace") as f:
            for line in f:
                if line.startswith("VERSION_ID="):
                    version = line.split("=", 1)[1].strip().strip('"')
                    break
    except OSError:
        version = ""
    return os_name, version


def classify_output(file_path, install_folder=None):
    """Return the output_file value for a Write path, or None when it does
    not resolve under the install folder into one of Shortcuts' own known
    output locations -- a founder-named file elsewhere on disk, or a file
    that merely shares a name or folder with a known output, never leaves
    the machine."""
    if install_folder is None:
        install_folder = os.getcwd()
    if not file_path:
        return None
    folder_real = os.path.realpath(install_folder)
    target_real = os.path.realpath(
        file_path if os.path.isabs(file_path) else os.path.join(install_folder, file_path)
    )
    try:
        if os.path.commonpath([folder_real, target_real]) != folder_real:
            return None
    except ValueError:
        return None
    rel = os.path.relpath(target_real, folder_real)
    if rel == os.curdir:
        return None
    segments = rel.split(os.sep)
    if len(segments) == 2 and segments[0] == "friday" and segments[1] in OUTPUT_FILES:
        return segments[1]
    if len(segments) >= 3 and segments[0] == "friday" and segments[1] == "sops":
        return "sops"
    if len(segments) >= 3 and segments[0] == "friday" and segments[1] == "teaching":
        return "teaching"
    if len(segments) >= 3 and segments[0] == "friday" and segments[1] == "delegation":
        return "delegation"
    if len(segments) == 2 and segments[0] == "commands" and segments[1].endswith(".md"):
        return "new-capability"
    return None


RECEIPT_PATH = os.path.join("friday", "usage-sent.jsonl")
RECEIPT_TRIM_THRESHOLD = 600
RECEIPT_TRIM_TO_LINES = 500


def read_install_id():
    try:
        with open(os.path.join("friday", ".install-id"), encoding="utf-8") as f:
            return f.read().strip()
    except OSError:
        return ""


def read_version():
    try:
        with open("VERSION", encoding="utf-8") as f:
            return f.read().strip()
    except OSError:
        return ""


def session_hash(session_id):
    return hashlib.sha256((session_id or "").encode("utf-8")).hexdigest()[:12]


def _redact_receipt(message):
    """The receipt is a founder-facing proof file, not a copy of what was
    posted. Everything else in message is already content-free (spec 3.5);
    only the one-time install `lead` token is a usable secret, so the
    receipt gets a copy with that one field replaced -- the original dict
    is untouched and still carries the real token to post_in_background."""
    redacted = dict(message)
    if "lead" in redacted:
        redacted["lead"] = "present"
    return redacted


def write_receipt(message):
    # Appends use >> semantics: one line, one open-in-append-mode write, no
    # read-modify-rewrite of the whole file on every message. The file is
    # only rewritten (temp file + os.replace, atomic) when it has grown
    # past RECEIPT_TRIM_THRESHOLD lines, and even then only to the last
    # RECEIPT_TRIM_TO_LINES -- two hooks firing at once can each append
    # their own line safely, and neither can ever observe a half-written
    # file mid-trim.
    os.makedirs("friday", exist_ok=True)
    line = json.dumps(_redact_receipt(message), sort_keys=True)
    with open(RECEIPT_PATH, "a", encoding="utf-8") as f:
        f.write(line + "\n")
    _trim_receipt_if_needed()


def _trim_receipt_if_needed():
    try:
        with open(RECEIPT_PATH, encoding="utf-8") as f:
            lines = f.read().splitlines()
    except OSError:
        return
    if len(lines) <= RECEIPT_TRIM_THRESHOLD:
        return
    trimmed = lines[-RECEIPT_TRIM_TO_LINES:]
    tmp_path = RECEIPT_PATH + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        f.write("\n".join(trimmed) + "\n")
    os.replace(tmp_path, RECEIPT_PATH)


def post_in_background(message, url):
    # Fully detached: every one of curl's three file descriptors is
    # redirected to /dev/null before the fork, so no pipe Claude Code is
    # watching is ever inherited by the child -- that redirection is the
    # guarantee the hook can exit at once, not process-group detachment.
    # setsid is a util-linux command, not present on macOS, and is never
    # called here or by the script (spec 3.6, amended 2026-09-08).
    curl = shutil.which("curl")
    if not curl:
        return
    try:
        subprocess.Popen(
            [curl, "--max-time", "2", "-fsS", "-X", "POST",
             "-H", "Content-Type: application/json",
             "-d", json.dumps(message), url],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except OSError:
        return


def send(message, url):
    write_receipt(message)
    post_in_background(message, url)


def run_hook(stdin_text, url):
    try:
        payload = json.loads(stdin_text) if stdin_text else {}
    except (ValueError, TypeError):
        return
    if not isinstance(payload, dict):
        return
    event_name = payload.get("hook_event_name")

    if event_name == "UserPromptSubmit":
        prompt = payload.get("prompt") or ""
        if not prompt.startswith("/") or len(prompt) < 2:
            return
        tail = prompt[1:].split()
        slug = tail[0] if tail else ""
        if not slug:
            return
        install_id = read_install_id()
        if not install_id:
            return
        command = slug if slug in COMMANDS else "custom"
        send({
            "event": "command",
            "install_id": install_id,
            "command": command,
            "version": read_version(),
            "session": session_hash(payload.get("session_id", "")),
            "sent_at": datetime.now(timezone.utc).isoformat(),
        }, url)
        return

    if event_name == "PostToolUse":
        if payload.get("tool_name") != "Write":
            return
        tool_input = payload.get("tool_input") or {}
        install_folder = payload.get("cwd") or os.getcwd()
        output_file = classify_output(tool_input.get("file_path", ""), install_folder)
        if not output_file:
            return
        install_id = read_install_id()
        if not install_id:
            return
        send({
            "event": "output",
            "install_id": install_id,
            "output_file": output_file,
            "version": read_version(),
            "session": session_hash(payload.get("session_id", "")),
            "sent_at": datetime.now(timezone.utc).isoformat(),
        }, url)
        return


def run_install(version, previous_version, lead_token, url):
    install_id = read_install_id()
    if not install_id:
        return
    if not version.strip():
        return
    os_name, os_version = detect_os()
    message = {
        "event": "install",
        "install_id": install_id,
        "version": version,
        "os": os_name,
        "sent_at": datetime.now(timezone.utc).isoformat(),
    }
    if os_version:
        message["os_version"] = os_version
    if previous_version:
        message["previous_version"] = previous_version
    if lead_token:
        message["lead"] = lead_token
    send(message, url)


def main():
    mode = os.environ.get("FRIDAY_USAGE_MODE", "hook")
    url = os.environ.get("FRIDAY_USAGE_URL", "")
    if mode == "install":
        run_install(
            os.environ.get("FRIDAY_USAGE_ARG2", ""),
            os.environ.get("FRIDAY_USAGE_ARG3", ""),
            os.environ.get("FRIDAY_USAGE_ARG4", ""),
            url,
        )
        return
    run_hook(os.environ.get("FRIDAY_USAGE_STDIN", ""), url)


try:
    main()
except Exception:
    pass
PYEOF

exit 0
