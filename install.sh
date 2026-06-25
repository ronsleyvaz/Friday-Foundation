#!/usr/bin/env bash
set -euo pipefail

# Friday for Claude Code: Voice Installer (brick 1).
# Installs the /voice-installer command into your Claude Code.
# No account, no paid install, nothing phones home.

REPO_RAW="https://raw.githubusercontent.com/ronsleyvaz/Friday-for-Claude-Code/main"
DEST="${HOME}/.claude/commands"

echo "Friday for Claude Code: Voice Installer"
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
curl -fsSL "${REPO_RAW}/commands/voice-installer.md" -o "${DEST}/voice-installer.md"

# 3. Verify it landed.
if [ -s "${DEST}/voice-installer.md" ]; then
  echo "Installed: ${DEST}/voice-installer.md"
  echo
  echo "Next step: open Claude Code and run  /voice-installer"
else
  echo "Install failed: the command file did not download."
  exit 1
fi
