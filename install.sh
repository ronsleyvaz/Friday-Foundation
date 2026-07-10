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
#   curl -fsSL .../install.sh | bash -s -- explore-idea      -- installs just /explore-idea
#   curl -fsSL .../install.sh | bash -s -- scope-decision    -- installs just /scope-decision
#   curl -fsSL .../install.sh | bash -s -- learnings         -- installs just /learnings
#   curl -fsSL .../install.sh | bash -s -- shipping-retro    -- installs just /shipping-retro
#   curl -fsSL .../install.sh | bash -s -- teach-team        -- installs just /teach-team
#   curl -fsSL .../install.sh | bash -s -- validate-idea     -- installs just /validate-idea
#   curl -fsSL .../install.sh | bash -s -- go-to-market      -- installs just /go-to-market
#   curl -fsSL .../install.sh | bash -s -- pricing-strategy  -- installs just /pricing-strategy
#   curl -fsSL .../install.sh | bash -s -- offer-creation    -- installs just /offer-creation
#   curl -fsSL .../install.sh | bash -s -- competitive-analysis -- installs just /competitive-analysis
#   curl -fsSL .../install.sh | bash -s -- sop-builder       -- installs just /sop-builder
#   curl -fsSL .../install.sh | bash -s -- product-hunt-launch -- installs just /product-hunt-launch
#   curl -fsSL .../install.sh | bash -s -- changelog         -- installs just /changelog
#   curl -fsSL .../install.sh | bash -s -- positioning       -- installs just /positioning
#   curl -fsSL .../install.sh | bash -s -- roadmap           -- installs just /roadmap
#
# The no-argument path installs the full command pack, CLAUDE.md.template,
# and the harness/ guide to the current working directory.
# Pass a capability name to install a single capability (commands only).
#
# To add a new capability to the pack: add it to PACK_COMMANDS below.
#
# Override the source URL for testing (set FRIDAY_REPO_RAW before running):
#   FRIDAY_REPO_RAW=http://localhost:8000 bash install.sh

REPO_RAW="${FRIDAY_REPO_RAW:-https://raw.githubusercontent.com/ronsleyvaz/Friday-Foundation/release}"
DEST="${HOME}/.claude/commands"
PROJECT_DIR="$(pwd)"

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
  "explore-idea     explore-idea.md     /explore-idea"
  "scope-decision   scope-decision.md   /scope-decision"
  "learnings        learnings.md        /learnings"
  "shipping-retro   shipping-retro.md   /shipping-retro"
  "teach-team       teach-team.md       /teach-team"
  "validate-idea    validate-idea.md    /validate-idea"
  "go-to-market     go-to-market.md     /go-to-market"
  "pricing-strategy pricing-strategy.md /pricing-strategy"
  "offer-creation   offer-creation.md   /offer-creation"
  "competitive-analysis competitive-analysis.md /competitive-analysis"
  "sop-builder      sop-builder.md      /sop-builder"
  "product-hunt-launch product-hunt-launch.md /product-hunt-launch"
  "changelog        changelog.md        /changelog"
  "positioning      positioning.md      /positioning"
  "roadmap          roadmap.md          /roadmap"
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

activate_brain_file() {
  # Turn the template into a live CLAUDE.md the first time; never clobber an
  # existing one. Claude Code reads CLAUDE.md, not the .template, each session.
  if [ ! -f "./CLAUDE.md.template" ]; then
    return 0
  fi
  if [ -f "./CLAUDE.md" ]; then
    echo "  Found an existing ./CLAUDE.md. Left it untouched."
    echo "  The template is saved alongside as ./CLAUDE.md.template to merge in yourself."
  else
    cp "./CLAUDE.md.template" "./CLAUDE.md"
    echo "  Created ./CLAUDE.md from the template. Open it and replace every [bracket]."
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
  echo "The brain file (CLAUDE.md) and harness guide will be saved to this directory:"
  echo "  ${PROJECT_DIR}"
  echo "If that is not your project directory, re-run this from the right place."
  echo
  install_template
  activate_brain_file
  echo
  install_harness

  echo
  echo "All done. The full command pack is installed to ${DEST}."
  echo
  echo "Open Claude Code in this directory:"
  echo "  ${PROJECT_DIR}"
  echo
  echo "Then start here, in order:"
  echo "  1. /amplify          Your fastest first win. Five minutes, no setup."
  echo "                       Writes friday/growth.md: where to push next."
  echo "  2. /voice-installer  Optional but recommended. Makes every command"
  echo "                       write in your voice instead of a generic style."
  echo "  3. /brief            Tomorrow morning. Your priorities, filtered."
  echo
  echo "The full list of commands is in README.md and docs/foundation-manual.md."
  echo "New here? Read harness/00-how-friday-works.md to understand what you installed."

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
    echo "Available: voice-installer, decide, brief, meetingprep, weeklyreview, amplify, new-capability, explore-idea, scope-decision, learnings, shipping-retro, teach-team, validate-idea, go-to-market, pricing-strategy, offer-creation, competitive-analysis, sop-builder, product-hunt-launch, changelog, positioning, roadmap"
    exit 1
  fi
fi
