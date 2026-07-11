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

# Download failures are collected, never fatal mid-pack, and reported honestly
# at the end. These module-level trackers are appended to by the helpers below.
FAILED_COMMANDS=()
FAILED_HARNESS=()
TEMPLATE_FAILED="no"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

require_tool() {
  # $1 = command name, $2 = one-line install hint. Returns 1 if absent.
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "$1 was not found (no '$1' command on your PATH)."
    echo "$2"
    echo "Then run this line again."
    return 1
  fi
}

install_one() {
  # Download one command file into DEST. Backs up a differing existing copy to
  # <name>.md.bak; replaces identical content silently (no .bak litter on
  # idempotent re-runs). Returns 1 on any download failure without aborting.
  local file="$1"
  local dest="${DEST}/${file}"
  local tmp
  # set -e is suppressed inside this function (it is called as `if ! install_one`),
  # so every failure is checked explicitly and turned into a return 1 the caller
  # collects. Nothing here may fail silently and still report success.
  mkdir -p "${DEST}" || {
    echo "  Failed to create ${DEST}"
    return 1
  }
  tmp="$(mktemp "${TMPDIR:-/tmp}/friday-install.XXXXXX")" || {
    echo "  Failed to create a temp file for: ${file}"
    return 1
  }
  if ! curl -fsSL "${REPO_RAW}/commands/${file}" -o "${tmp}" || [ ! -s "${tmp}" ]; then
    rm -f "${tmp}"
    echo "  Failed to download: ${file}"
    return 1
  fi
  if [ -f "${dest}" ] && ! cmp -s "${tmp}" "${dest}"; then
    if ! mv "${dest}" "${dest}.bak"; then
      echo "  Could not back up your existing ${file}; leaving it untouched."
      rm -f "${tmp}"
      return 1
    fi
    echo "  Backed up your existing ${file} to ${file}.bak"
  fi
  if ! mv "${tmp}" "${dest}"; then
    echo "  Failed to install: ${file}"
    rm -f "${tmp}"
    return 1
  fi
  echo "  Installed: ${dest}"
  return 0
}

install_harness() {
  echo "Fetching the harness guide..."
  mkdir -p "./harness"
  local f
  for f in "${HARNESS_FILES[@]}"; do
    if curl -fsSL "${REPO_RAW}/harness/${f}" -o "./harness/${f}" && [ -s "./harness/${f}" ]; then
      echo "  Fetched: ./harness/${f}"
    else
      rm -f "./harness/${f}"
      echo "  Failed to fetch harness file: ${f}"
      FAILED_HARNESS+=("${f}")
    fi
  done
}

install_template() {
  if curl -fsSL "${REPO_RAW}/CLAUDE.md.template" -o "./CLAUDE.md.template" && [ -s "./CLAUDE.md.template" ]; then
    echo "  Fetched: ./CLAUDE.md.template"
  else
    rm -f "./CLAUDE.md.template"
    echo "  Failed to fetch CLAUDE.md.template"
    TEMPLATE_FAILED="yes"
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

install_full_pack() {
  echo "Friday Foundation: installing the full command pack"
  echo

  local entry file
  for entry in "${PACK_COMMANDS[@]}"; do
    file=$(echo "${entry}" | awk '{print $2}')
    if ! install_one "${file}"; then
      FAILED_COMMANDS+=("${file}")
    fi
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

  # Honest close: never claim success while any file is missing.
  if [ ${#FAILED_COMMANDS[@]} -gt 0 ] || [ "${TEMPLATE_FAILED}" = "yes" ] || [ ${#FAILED_HARNESS[@]} -gt 0 ]; then
    echo
    echo "Finished, but some files did not download:"
    if [ ${#FAILED_COMMANDS[@]} -gt 0 ]; then
      local c
      for c in "${FAILED_COMMANDS[@]}"; do
        echo "  command: ${c}"
      done
    fi
    if [ "${TEMPLATE_FAILED}" = "yes" ]; then
      echo "  CLAUDE.md.template (so no CLAUDE.md was created for you)"
    fi
    if [ ${#FAILED_HARNESS[@]} -gt 0 ]; then
      local h
      for h in "${FAILED_HARNESS[@]}"; do
        echo "  harness: ${h}"
      done
    fi
    echo
    echo "Re-run the same install line to retry. Anything already installed is reused, so only the missing files are fetched again."
    exit 1
  fi

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
  exit 0
}

install_single() {
  local capability="$1"
  local entry slug file slash matched=""
  for entry in "${PACK_COMMANDS[@]}"; do
    slug=$(echo "${entry}" | awk '{print $1}')
    file=$(echo "${entry}" | awk '{print $2}')
    slash=$(echo "${entry}" | awk '{print $3}')
    if [ "${slug}" = "${capability}" ]; then
      matched="yes"
      echo "Friday Foundation: installing ${slug}"
      echo
      if install_one "${file}"; then
        echo
        echo "Next step: open Claude Code and run  ${slash}"
      else
        echo
        echo "That did not install. Re-run the same line to retry."
        exit 1
      fi
      break
    fi
  done

  if [ -z "${matched}" ]; then
    echo "Unknown capability: ${capability}"
    echo "Available: voice-installer, decide, brief, meetingprep, weeklyreview, amplify, new-capability, explore-idea, scope-decision, learnings, shipping-retro, teach-team, validate-idea, go-to-market, pricing-strategy, offer-creation, competitive-analysis, sop-builder, product-hunt-launch, changelog, positioning, roadmap"
    exit 1
  fi
}

# ---------------------------------------------------------------------------
# Entry point. All work lives in main() and runs only from the final line, so a
# curl | bash download cut off mid-transfer never executes a partial install.
# ---------------------------------------------------------------------------

main() {
  require_tool curl "Install curl first: it ships with macOS and most Linux distributions (for example 'sudo apt-get install curl')." || exit 1
  require_tool claude "Install Claude Code first: https://docs.anthropic.com/claude-code" || exit 1

  local capability="${1:-}"
  if [ -z "${capability}" ]; then
    install_full_pack
  else
    install_single "${capability}"
  fi
}

main "$@"
