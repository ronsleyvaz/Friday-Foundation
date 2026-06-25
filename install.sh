#!/usr/bin/env bash
set -euo pipefail

# Friday for Claude Code: capability installer.
# No account, no paid install, nothing phones home.
#
# Usage:
#   curl -fsSL .../install.sh | bash                       -- installs the full command pack
#   curl -fsSL .../install.sh | bash -s -- decide          -- installs just /decide
#   curl -fsSL .../install.sh | bash -s -- brief           -- installs just /brief
#   curl -fsSL .../install.sh | bash -s -- voice-installer -- installs just /voice-installer
#   curl -fsSL .../install.sh | bash -s -- meetingprep     -- installs just /meetingprep
#   curl -fsSL .../install.sh | bash -s -- weeklyreview    -- installs just /weeklyreview
#
# The no-argument path installs the full command pack (all capabilities).
# Pass a capability name to install a single capability.
#
# To add a new capability to the pack: add it to PACK_COMMANDS below.

REPO_RAW="https://raw.githubusercontent.com/ronsleyvaz/Friday-for-Claude-Code/main"
DEST="${HOME}/.claude/commands"

# Full pack -- every command file installed by the no-arg path.
# One entry per line: "<capability-slug> <file-name> <slash-command>"
PACK_COMMANDS=(
  "voice-installer voice-installer.md /voice-installer"
  "decide          decide.md          /decide"
  "brief           brief.md           /brief"
  "meetingprep     meetingprep.md     /meetingprep"
  "weeklyreview    weeklyreview.md    /weeklyreview"
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

install_one() {
  local file="$1"
  mkdir -p "${DEST}"
  curl -fsSL "${REPO_RAW}/commands/${file}" -o "${DEST}/${file}"
  if [ -s "${DEST}/${file}" ]; then
    echo "  Installed: ${DEST}/${file}"
  else
    echo "  Failed to download: ${file}"
    return 1
  fi
}

# ---------------------------------------------------------------------------
# Claude Code must be present
# ---------------------------------------------------------------------------

if ! command -v claude >/dev/null 2>&1; then
  echo "Claude Code was not found (no 'claude' command on your PATH)."
  echo "Install it first: https://docs.anthropic.com/claude-code"
  echo "Then run this line again."
  exit 1
fi

# ---------------------------------------------------------------------------
# Route: no-arg = full pack; arg = single capability
# ---------------------------------------------------------------------------

CAPABILITY="${1:-}"

if [ -z "${CAPABILITY}" ]; then
  # ---- Full pack install ----
  echo "Friday for Claude Code: installing the full command pack"
  echo

  for entry in "${PACK_COMMANDS[@]}"; do
    slug=$(echo "${entry}" | awk '{print $1}')
    file=$(echo "${entry}" | awk '{print $2}')
    install_one "${file}"
  done

  echo
  echo "All commands installed. Open Claude Code and run:"
  echo "  /voice-installer   -- set up your voice profile first"
  echo "  /brief             -- your morning brief"
  echo "  /decide            -- run the 1-3-1 decision protocol"
  echo "  /meetingprep       -- prepare for any meeting in five minutes"
  echo "  /weeklyreview      -- structured weekly review and one clear priority"

else
  # ---- Single capability install ----
  matched=""
  for entry in "${PACK_COMMANDS[@]}"; do
    slug=$(echo "${entry}" | awk '{print $1}')
    file=$(echo "${entry}" | awk '{print $2}')
    slash=$(echo "${entry}" | awk '{print $3}')
    if [ "${slug}" = "${CAPABILITY}" ]; then
      matched="yes"
      echo "Friday for Claude Code: installing ${slug}"
      echo
      install_one "${file}"
      echo
      echo "Next step: open Claude Code and run  ${slash}"
      break
    fi
  done

  if [ -z "${matched}" ]; then
    echo "Unknown capability: ${CAPABILITY}"
    echo "Available: voice-installer, decide, brief, meetingprep, weeklyreview"
    exit 1
  fi
fi
