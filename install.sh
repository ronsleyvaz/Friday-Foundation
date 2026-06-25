#!/usr/bin/env bash
set -euo pipefail

# Friday for Claude Code: capability installer.
# No account, no paid install, nothing phones home.
#
# Usage:
#   curl -fsSL .../install.sh | bash              -- installs /voice-installer (default)
#   curl -fsSL .../install.sh | bash -s -- decide -- installs /decide
#
# The no-argument path always installs the Voice Installer.
# Pass a capability name to install a different capability.

REPO_RAW="https://raw.githubusercontent.com/ronsleyvaz/Friday-for-Claude-Code/main"
DEST="${HOME}/.claude/commands"

# Determine which capability to install (default: voice-installer).
CAPABILITY="${1:-voice-installer}"

case "${CAPABILITY}" in
  voice-installer)
    COMMAND_FILE="voice-installer.md"
    DISPLAY_NAME="Voice Installer"
    SLASH_CMD="/voice-installer"
    ;;
  decide)
    COMMAND_FILE="decide.md"
    DISPLAY_NAME="Decision Runner"
    SLASH_CMD="/decide"
    ;;
  *)
    echo "Unknown capability: ${CAPABILITY}"
    echo "Available: voice-installer (default), decide"
    exit 1
    ;;
esac

echo "Friday for Claude Code: ${DISPLAY_NAME}"
echo

# 1. Claude Code must be present.
if ! command -v claude >/dev/null 2>&1; then
  echo "Claude Code was not found (no 'claude' command on your PATH)."
  echo "Install it first: https://docs.anthropic.com/claude-code"
  echo "Then run this line again."
  exit 1
fi

# 2. Install the command file.
mkdir -p "${DEST}"
curl -fsSL "${REPO_RAW}/commands/${COMMAND_FILE}" -o "${DEST}/${COMMAND_FILE}"

# 3. Verify it landed.
if [ -s "${DEST}/${COMMAND_FILE}" ]; then
  echo "Installed: ${DEST}/${COMMAND_FILE}"
  echo
  echo "Next step: open Claude Code and run  ${SLASH_CMD}"
else
  echo "Install failed: the command file did not download."
  exit 1
fi
