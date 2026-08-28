#!/usr/bin/env bash
# Friday SHORTCUTS status line. Two rows, <100ms, never exits non-zero.
#
# Row 1:  Friday SHORTCUTS · chief-of-staff  |  <git branch>  |  <model>  |  <effort> effort
# Row 2:  ctx:[bar] <pct> <used>/<max>  ·  5h:<pct>(<reset>)  ·  7d:<pct>(<reset>)
#
# This is a standalone fork for Friday Foundation buyers. It has zero
# dependency on the Friday operator repo: no memory-palace reads, no sprint
# tag, no phase-file read, no founder gate. It runs from inside
# ~/friday-shortcuts with nothing but bash, git, and python3.
#
# Claude Code pipes a JSON payload on stdin (model, effort, context window,
# rate limits). Field names vary across Claude Code releases (snake_case,
# camelCase, and literal "5h"/"7d" bracket keys have all been observed), so
# every field is looked up under all three spellings.
#
# Parsing runs on python3 only; jq, absent from a stock Mac, is never
# invoked, and python3 is already a requirement for this installer.
#
# Colour-coded: green=healthy (<50%), yellow=warning (50-80%), red=critical (>80%).
# Env: NO_COLOR set (any value) disables ANSI colour codes.

set -u

# ---- Read JSON payload from stdin (never blocks: a closed/absent stdin
# yields an empty string, handled as "no data" below) ----
FRIDAY_STATUSLINE_JSON="$(cat 2>/dev/null || true)"

# ---- Git branch (row 1), from the process's own working directory. Claude
# Code invokes a statusLine command with cwd set to the project folder. ----
FRIDAY_STATUSLINE_BRANCH="$(git branch --show-current 2>/dev/null || true)"

export FRIDAY_STATUSLINE_JSON FRIDAY_STATUSLINE_BRANCH

if ! command -v python3 >/dev/null 2>&1; then
    printf 'Friday SHORTCUTS\n\n'
    exit 0
fi

python3 - <<'PYEOF'
import json
import os
import sys
import time


def env_flag(name):
    return bool(os.environ.get(name, ""))


NO_COLOR = env_flag("NO_COLOR")

if NO_COLOR:
    C_RESET = C_GREEN = C_YELLOW = C_RED = C_CYAN = C_DIM = C_BOLD = ""
else:
    C_RESET = "\033[0m"
    C_GREEN = "\033[32m"
    C_YELLOW = "\033[33m"
    C_RED = "\033[31m"
    C_CYAN = "\033[36m"
    C_DIM = "\033[90m"
    C_BOLD = "\033[1m"


def first(data, paths):
    """Return the first non-None value found at any of the given key paths.

    Each path is a tuple of keys walked through nested dicts, e.g.
    ("context_window", "used_tokens"). Mirrors the operator statusline's
    field-name fallback list, as plain dict lookups.
    """
    for path in paths:
        cur = data
        ok = True
        for key in path:
            if isinstance(cur, dict) and key in cur:
                cur = cur[key]
            else:
                ok = False
                break
        if ok and cur is not None:
            return cur
    return None


def as_number(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def pct_from_fields(direct, remaining, used, maximum):
    d = as_number(direct)
    if d is not None:
        return d
    r = as_number(remaining)
    if r is not None:
        return 100 - r
    u = as_number(used)
    m = as_number(maximum)
    if u is not None and m is not None and m > 0:
        return (u / m) * 100
    return None


def colour_pct(value):
    if value < 50:
        colour = C_GREEN
    elif value < 80:
        colour = C_YELLOW
    else:
        colour = C_RED
    return f"{colour}{value:.0f}%{C_RESET}"


def fmt_tokens(n):
    n = as_number(n)
    if n is None:
        return None
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n / 1_000:.0f}k"
    return f"{n:.0f}"


def to_epoch(value):
    """Accept a pure-digit epoch or an ISO 8601 string; return epoch seconds
    or None on parse failure."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    s = str(value)
    if s.replace(".", "", 1).replace("-", "", 1).isdigit():
        try:
            return float(s)
        except ValueError:
            return None
    cleaned = s
    if cleaned.endswith("Z"):
        cleaned = cleaned[:-1]
    cleaned = cleaned.split("+")[0]
    cleaned = cleaned.split(".")[0]
    for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"):
        try:
            return time.mktime(time.strptime(cleaned, fmt))
        except ValueError:
            continue
    return None


def format_reset(value):
    epoch = to_epoch(value)
    if epoch is None:
        return None
    diff = epoch - time.time()
    if diff <= 0:
        return "now"
    hours = int(diff // 3600)
    minutes = int((diff % 3600) // 60)
    if hours > 0:
        return f"{hours}h{minutes}m"
    return f"{minutes}m"


def bead_bar(pct):
    filled = int(round(pct / 10))
    filled = max(0, min(10, filled))
    return "[" + ("█" * filled) + ("░" * (10 - filled)) + "]"


CONTEXT_PATHS = {
    "direct": [
        ("context_window", "used_percentage"),
        ("context_window", "usage_percentage"),
        ("context_window", "percent_used"),
        ("context_window", "percent"),
        ("contextWindow", "usedPercentage"),
        ("contextWindow", "usagePercentage"),
        ("contextWindow", "percentUsed"),
        ("contextWindow", "percent"),
    ],
    "remaining": [
        ("context_window", "remaining_percentage"),
        ("contextWindow", "remainingPercentage"),
    ],
    "used": [
        ("context_window", "used_tokens"),
        ("context_window", "current_tokens"),
        ("context_window", "tokens_used"),
        ("contextWindow", "usedTokens"),
        ("contextWindow", "currentTokens"),
        ("contextWindow", "tokensUsed"),
    ],
    "max": [
        ("context_window", "max_tokens"),
        ("context_window", "total_tokens"),
        ("context_window", "size_tokens"),
        ("contextWindow", "maxTokens"),
        ("contextWindow", "totalTokens"),
        ("contextWindow", "sizeTokens"),
    ],
}


def quota_paths(snake, camel, bracket):
    return {
        "direct": [
            ("rate_limits", snake, "used_percentage"),
            ("rate_limits", snake, "usage_percentage"),
            ("rate_limits", camel, "usedPercentage"),
            ("rate_limits", camel, "usagePercentage"),
            ("rateLimits", camel, "usedPercentage"),
            ("rateLimits", snake, "used_percentage"),
            ("rate_limits", bracket, "used_percentage"),
            ("rateLimits", bracket, "usedPercentage"),
        ],
        "remaining": [
            ("rate_limits", snake, "remaining_percentage"),
            ("rate_limits", camel, "remainingPercentage"),
            ("rateLimits", camel, "remainingPercentage"),
            ("rateLimits", snake, "remaining_percentage"),
            ("rate_limits", bracket, "remaining_percentage"),
            ("rateLimits", bracket, "remainingPercentage"),
        ],
        "used": [
            ("rate_limits", snake, "used"),
            ("rate_limits", camel, "used"),
            ("rateLimits", camel, "used"),
            ("rate_limits", bracket, "used"),
            ("rateLimits", bracket, "used"),
        ],
        "max": [
            ("rate_limits", snake, "limit"),
            ("rate_limits", camel, "limit"),
            ("rateLimits", camel, "limit"),
            ("rate_limits", bracket, "limit"),
            ("rateLimits", bracket, "limit"),
        ],
        "reset": [
            ("rate_limits", snake, "resets_at"),
            ("rate_limits", snake, "reset_at"),
            ("rate_limits", camel, "resetsAt"),
            ("rate_limits", camel, "resetAt"),
            ("rateLimits", camel, "resetsAt"),
            ("rateLimits", camel, "resetAt"),
            ("rateLimits", snake, "resets_at"),
            ("rate_limits", bracket, "resets_at"),
            ("rateLimits", bracket, "resetsAt"),
        ],
    }


FIVE_HOUR_PATHS = quota_paths("five_hour", "fiveHour", "5h")
SEVEN_DAY_PATHS = quota_paths("seven_day", "sevenDay", "7d")


def build_row1(data):
    row = f"{C_CYAN}{C_BOLD}Friday SHORTCUTS{C_RESET} {C_DIM}·{C_RESET} {C_DIM}chief-of-staff{C_RESET}"

    branch = os.environ.get("FRIDAY_STATUSLINE_BRANCH", "")
    if branch:
        row += f"  {C_DIM}|{C_RESET}  {branch}"

    model_name = first(data, [("model", "display_name")])
    if model_name:
        row += f"  {C_DIM}|{C_RESET}  {model_name}"

    effort = first(data, [("effort", "level")])
    if effort:
        row += f"  {C_DIM}|{C_RESET}  {effort} effort"

    return row


def build_context_part(data):
    direct = first(data, CONTEXT_PATHS["direct"])
    remaining = first(data, CONTEXT_PATHS["remaining"])
    used = first(data, CONTEXT_PATHS["used"])
    maximum = first(data, CONTEXT_PATHS["max"])

    pct = pct_from_fields(direct, remaining, used, maximum)
    used_fmt = fmt_tokens(used)
    max_fmt = fmt_tokens(maximum)

    tokens_part = ""
    if used_fmt and max_fmt:
        tokens_part = f" {C_DIM}{used_fmt}/{max_fmt}{C_RESET}"
    elif max_fmt:
        tokens_part = f" {C_DIM}of {max_fmt}{C_RESET}"

    if pct is not None:
        bar = bead_bar(pct)
        return f"ctx:{bar} {colour_pct(pct)}{tokens_part}"
    if tokens_part:
        return f"ctx:{tokens_part.strip()}"
    return ""


def build_quota_part(data, label, paths):
    direct = first(data, paths["direct"])
    remaining = first(data, paths["remaining"])
    used = first(data, paths["used"])
    maximum = first(data, paths["max"])
    reset = first(data, paths["reset"])

    pct = pct_from_fields(direct, remaining, used, maximum)
    if pct is None:
        return ""

    reset_str = ""
    formatted = format_reset(reset)
    if formatted:
        reset_str = f"{C_DIM}({formatted}){C_RESET}"

    return f"{label}:{colour_pct(pct)}{reset_str}"


def build_row2(data):
    parts = []
    ctx_part = build_context_part(data)
    if ctx_part:
        parts.append(ctx_part)
    five_part = build_quota_part(data, "5h", FIVE_HOUR_PATHS)
    if five_part:
        parts.append(five_part)
    seven_part = build_quota_part(data, "7d", SEVEN_DAY_PATHS)
    if seven_part:
        parts.append(seven_part)
    return f"  {C_DIM}·{C_RESET}  ".join(parts)


def main():
    raw = os.environ.get("FRIDAY_STATUSLINE_JSON", "")
    data = {}
    if raw.strip():
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, dict):
                data = parsed
        except (ValueError, TypeError):
            data = {}

    print(build_row1(data))
    print(build_row2(data))


try:
    main()
except Exception:
    print("Friday SHORTCUTS")
    print("")
PYEOF

exit 0
