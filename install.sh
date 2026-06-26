#!/usr/bin/env bash
set -euo pipefail

# Friday Foundation: capability installer.
# No account, no paid install, nothing phones home.
#
# Usage:
#   curl -fsSL .../install.sh | bash                         -- installs the full command pack
#   curl -fsSL .../install.sh | bash -s -- decide            -- installs just /decide
#   curl -fsSL .../install.sh | bash -s -- brief             -- installs just /brief
#   curl -fsSL .../install.sh | bash -s -- voice-installer   -- installs just /voice-installer
#   curl -fsSL .../install.sh | bash -s -- meetingprep       -- installs just /meetingprep
#   curl -fsSL .../install.sh | bash -s -- weeklyreview      -- installs just /weeklyreview
#   curl -fsSL .../install.sh | bash -s -- amplify           -- installs just /amplify
#   curl -fsSL .../install.sh | bash -s -- new-capability    -- installs just /new-capability
#
# The no-argument path installs the full command pack, CLAUDE.md.template,
# and the harness/ guide to the current working directory.
# Pass a capability name to install a single capability (commands only).
#
# To add a new capability to the pack: add it to PACK_COMMANDS below.
#
# Override the source URL for testing (set FRIDAY_REPO_RAW before running):
#   FRIDAY_REPO_RAW=http://localhost:8000 bash install.sh

REPO_RAW="${FRIDAY_REPO_RAW:-https://raw.githubusercontent.com/ronsleyvaz/Friday-Foundation/main}"
DEST="${HOME}/.claude/commands"

# Full pack -- every command file installed by the no-arg path.
# One entry per line: "<capability-slug> <file-name> <slash-command>"
PACK_COMMANDS=(
  "voice-installer  voice-installer.md  /voice-installer"
  "decide           decide.md           /decide"
  "brief            brief.md            /brief"
  "meetingprep      meetingprep.md      /meetingprep"
  "weeklyreview     weeklyreview.md     /weeklyreview"
  "amplify          amplify.md          /amplify"
  "new-capability   new-capability.md   /new-capability"
)

# Harness guide files fetched alongside the full pack.
HARNESS_FILES=(
  "00-how-friday-works.md"
  "01-add-a-command.md"
  "02-add-an-agent.md"
  "03-connect-your-own-tools.md"
  "04-the-friday-folder.md"
  "05-the-amplify-logic.md"
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

install_harness() {
  echo "Fetching the harness guide..."
  mkdir -p "./harness"
  for f in "${HARNESS_FILES[@]}"; do
    curl -fsSL "${REPO_RAW}/harness/${f}" -o "./harness/${f}"
    if [ -s "./harness/${f}" ]; then
      echo "  Fetched: ./harness/${f}"
    else
      echo "  Failed to fetch harness file: ${f}"
    fi
  done
}

install_template() {
  curl -fsSL "${REPO_RAW}/CLAUDE.md.template" -o "./CLAUDE.md.template"
  if [ -s "./CLAUDE.md.template" ]; then
    echo "  Fetched: ./CLAUDE.md.template"
  else
    echo "  Failed to fetch CLAUDE.md.template"
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
  echo "Friday Foundation: installing the full command pack"
  echo

  for entry in "${PACK_COMMANDS[@]}"; do
    slug=$(echo "${entry}" | awk '{print $1}')
    file=$(echo "${entry}" | awk '{print $2}')
    install_one "${file}"
  done

  echo
  install_template
  echo
  install_harness

  echo
  echo "All done. Open Claude Code in this directory and run:"
  echo "  /voice-installer   -- set up your voice profile first"
  echo "  /amplify           -- run the growth diagnostic"
  echo "  /brief             -- your morning brief"
  echo "  /decide            -- run the 1-3-1 decision protocol"
  echo "  /meetingprep       -- prepare for any meeting in five minutes"
  echo "  /weeklyreview      -- structured weekly review and one clear priority"
  echo "  /new-capability    -- scaffold your own command"
  echo
  echo "Read harness/00-how-friday-works.md to understand what you just installed."

else
  # ---- Single capability install ----
  matched=""
  for entry in "${PACK_COMMANDS[@]}"; do
    slug=$(echo "${entry}" | awk '{print $1}')
    file=$(echo "${entry}" | awk '{print $2}')
    slash=$(echo "${entry}" | awk '{print $3}')
    if [ "${slug}" = "${CAPABILITY}" ]; then
      matched="yes"
      echo "Friday Foundation: installing ${slug}"
      echo
      install_one "${file}"
      echo
      echo "Next step: open Claude Code and run  ${slash}"
      break
    fi
  done

  if [ -z "${matched}" ]; then
    echo "Unknown capability: ${CAPABILITY}"
    echo "Available: voice-installer, decide, brief, meetingprep, weeklyreview, amplify, new-capability"
    exit 1
  fi
fi
