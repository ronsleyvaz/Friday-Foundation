#!/usr/bin/env bash
set -euo pipefail

# Friday Shortcuts: capability installer.
# No account, no paid install, nothing phones home.
#
# Usage:
#   curl -fsSL .../install.sh | bash                         -- clones the whole
#                                                                repo into
#                                                                ~/friday-shortcuts
#                                                                and prints the
#                                                                command to open it
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
#   curl -fsSL .../install.sh | bash -s -- customer-feedback -- installs just /customer-feedback
#   curl -fsSL .../install.sh | bash -s -- risk-register     -- installs just /risk-register
#   curl -fsSL .../install.sh | bash -s -- friday-upgrade    -- installs just /friday-upgrade
#
# The no-argument path clones the whole Friday Shortcuts repo into
# ~/friday-shortcuts (a fixed path, independent of where you run this from),
# gives you a personalised CLAUDE.md brain file, wires up the status line and
# spinner settings, installs commands into ~/friday-shortcuts/.claude/commands/
# so they only work when Claude Code is opened from inside that folder, and
# prints the command to open Claude Code there. Re-running it on an existing install updates
# Shortcuts's own files from the release branch in place, leaving your
# CLAUDE.md and friday/ folder untouched.
# Pass a capability name to install a single command file into the current
# directory instead (unrelated to the ~/friday-shortcuts folder).
#
# To add a new capability to the pack: add it to PACK_COMMANDS below.
#
# Override the source URL for testing single-capability installs (set
# FRIDAY_REPO_RAW before running):
#   FRIDAY_REPO_RAW=http://localhost:8000 bash install.sh -- decide
#
# Full-pack overrides (for testing against a local mirror instead of GitHub):
#   FRIDAY_SHORTCUTS_PATH   where the repo is cloned (default ~/friday-shortcuts)
#   FRIDAY_CLONE_URL        git remote to clone (default the public GitHub repo)
#   FRIDAY_CLONE_BRANCH     branch to clone (default "release")

REPO_RAW="${FRIDAY_REPO_RAW:-https://raw.githubusercontent.com/ronsleyvaz/Friday-Foundation/release}"
# DEST is the single-capability path's destination only (install_single via
# install_one). The full-pack path installs commands into INSTALL_PATH's own
# .claude/commands/ instead -- see sync_commands_to_folder.
DEST="${HOME}/.claude/commands"
INSTALL_PATH="${FRIDAY_SHORTCUTS_PATH:-${HOME}/friday-shortcuts}"
CLONE_URL="${FRIDAY_CLONE_URL:-https://github.com/ronsleyvaz/Friday-Foundation.git}"
CLONE_BRANCH="${FRIDAY_CLONE_BRANCH:-release}"

# OnePath-S3: --lead <token> fetches a pre-filled CLAUDE.md from the landing
# site instead of the blank template, when the founder came from
# friday.amplifyais.com's signup flow. LEAD_TOKEN is set by main()'s argument
# parsing; empty means no --lead was passed.
CONTEXT_BASE="${FRIDAY_CONTEXT_URL:-https://friday.amplifyais.com/api/context}"
LEAD_TOKEN=""

# Full pack -- every command file synced into DEST by the no-arg path, and the
# only file the single-capability path downloads.
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
  "customer-feedback customer-feedback.md /customer-feedback"
  "risk-register risk-register.md /risk-register"
  "friday-upgrade  friday-upgrade.md  /friday-upgrade"
)

# Download/sync failures are collected, never fatal mid-pack, and reported
# honestly at the end. Appended to by the helpers below.
FAILED_COMMANDS=()

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
  # Used only by the single-capability path (install_single).
  local file="$1"
  local dest="${DEST}/${file}"
  local tmp
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

fetch_prefilled_claude_md() {
  # Attempts to fetch a pre-filled CLAUDE.md for LEAD_TOKEN. On success writes
  # ./CLAUDE.md.prefilled and returns 0. On ANY failure (no token, bad token,
  # no network) returns 1 and writes nothing -- the caller falls back to the
  # stock template. Install must never break on personalisation.
  if [ -z "${LEAD_TOKEN}" ]; then
    return 1
  fi
  local tmp
  tmp="$(mktemp "${TMPDIR:-/tmp}/friday-context.XXXXXX")" || return 1
  if curl -fsSL "${CONTEXT_BASE}/${LEAD_TOKEN}" -o "${tmp}" && [ -s "${tmp}" ]; then
    mv "${tmp}" "./CLAUDE.md.prefilled"
    return 0
  fi
  rm -f "${tmp}"
  return 1
}

activate_brain_file() {
  # Turn the template into a live CLAUDE.md the first time; never clobber an
  # existing one. Claude Code reads CLAUDE.md, not the .template, each
  # session. Runs after personalize_brain_files, so by the time this runs,
  # "existing" means a buyer's own prior personalisation, never the repo's
  # own contributor guide.
  if [ ! -f "./CLAUDE.md.template" ]; then
    echo "  CLAUDE.md.template is missing from the clone; no brain file was created."
    echo "  Everything else installed. Re-run the same install line to retry."
    return 0
  fi
  if [ -f "./CLAUDE.md" ]; then
    echo "  Found an existing ./CLAUDE.md. Left it untouched."
    echo "  The template is saved alongside as ./CLAUDE.md.template to merge in yourself."
    return 0
  fi
  if fetch_prefilled_claude_md; then
    mv "./CLAUDE.md.prefilled" "./CLAUDE.md"
    echo "  Created ./CLAUDE.md pre-filled with what you told us. Open it and check the rest."
    return 0
  fi
  cp "./CLAUDE.md.template" "./CLAUDE.md"
  echo "  Created ./CLAUDE.md from the template. Open it and replace every [bracket]."
}

personalize_brain_files() {
  # The clone ships this repo's OWN CLAUDE.md and AGENTS.md: contributor
  # guides for someone hacking on Friday Shortcuts itself (run pytest, claim
  # a GitHub issue, never touch secrets). Move them aside before
  # activate_brain_file runs, so Claude Code loads a buyer's own context the
  # moment it opens this folder, not this repo's dev rules. Best-effort: a
  # missing or unmovable file here is never fatal, and if the move fails the
  # repo guide is simply left in place (activate_brain_file will then leave
  # it untouched rather than overwrite it).
  if [ -f "./CLAUDE.md" ]; then
    if mv "./CLAUDE.md" "./CLAUDE.md.repo-guide" 2>/dev/null; then
      echo "  Moved the repo's own CLAUDE.md aside to ./CLAUDE.md.repo-guide"
    else
      echo "  Could not move the repo's CLAUDE.md aside; it is left as your CLAUDE.md."
    fi
  fi
  if [ -f "./AGENTS.md" ]; then
    if mv "./AGENTS.md" "./AGENTS.md.repo-guide" 2>/dev/null; then
      echo "  Moved the repo's own AGENTS.md aside to ./AGENTS.md.repo-guide"
    fi
  fi
}

activate_spinner_settings() {
  # Gives Claude Code Friday's own spinner words and tips, scoped to this
  # folder's own ./.claude/settings.json only -- never the founder's global
  # config. Best-effort throughout: every branch below is guarded so a
  # failure here never fails the install (a founder's global settings.json
  # is not something a free public installer gets to break).
  if [ ! -f "./spinner-settings.json.template" ]; then
    return 0
  fi

  local settings="./.claude/settings.json"

  if [ ! -f "${settings}" ]; then
    if ! mkdir -p "./.claude"; then
      echo "  Could not create ./.claude; skipped the spinner settings step."
      return 0
    fi
    if cp "./spinner-settings.json.template" "${settings}"; then
      echo "  Created ${settings} with Friday's spinner words and tips."
    else
      echo "  Could not write ${settings}; skipped the spinner settings step."
    fi
    return 0
  fi

  if ! command -v python3 >/dev/null 2>&1; then
    echo "  python3 was not found, so the spinner settings step was skipped."
    echo "  Merge ./spinner-settings.json.template into ${settings} yourself."
    return 0
  fi

  # Check first, before ever touching disk: a settings.json that already
  # opts into spinner settings is a true no-op, never even a transient
  # backup file. (The check used to happen inside the merge step, after the
  # backup was already written and merely cleaned up again on a no-op --
  # a run killed between those two steps left a stray .bak behind.)
  local check_rc=0
  python3 -c 'import json,sys; s=json.load(open(sys.argv[1])); sys.exit(2 if ("spinnerVerbs" in s or "spinnerTipsOverride" in s) else 0)' "${settings}" || check_rc=$?

  if [ "${check_rc}" = "2" ]; then
    echo "  ${settings} already has spinner settings. Left it untouched."
    echo "  The template is saved alongside as ./spinner-settings.json.template to merge in yourself."
    return 0
  fi
  if [ "${check_rc}" != "0" ]; then
    echo "  Could not merge spinner settings into ${settings}; left it untouched."
    echo "  The template is saved alongside as ./spinner-settings.json.template to merge in yourself."
    return 0
  fi

  local backup="${settings}.pre-friday-$(date +%F).bak"
  if ! cp "${settings}" "${backup}"; then
    echo "  Could not back up ${settings}; skipped the spinner settings step."
    return 0
  fi

  # A single physical line by design (not a heredoc): install.sh's own test
  # suite (test_install_wraps_all_logic_in_main) scans every column-0 line in
  # this file and rejects anything outside a function definition, so a
  # multi-line inline script would misread as top-level bash. json.load()
  # raises on invalid JSON, which python turns into exit code 1 with no
  # explicit try/except needed; the check below treats that as "skip and
  # restore", never as a reason to fail the install.
  local merge_rc=0
  python3 -c 'import json,sys; s=json.load(open(sys.argv[1])); t=json.load(open(sys.argv[2])); s["spinnerVerbs"]=t["spinnerVerbs"]; s["spinnerTipsOverride"]=t["spinnerTipsOverride"]; f=open(sys.argv[1],"w"); json.dump(s,f,indent=2); f.write("\n"); f.close()' "${settings}" "./spinner-settings.json.template" || merge_rc=$?

  if [ "${merge_rc}" = "0" ]; then
    echo "  Backed up your existing settings to ${backup}"
    echo "  Added Friday's spinner words and tips to ${settings}"
  else
    rm -f "${backup}"
    echo "  Could not merge spinner settings into ${settings}; left it untouched."
    echo "  The template is saved alongside as ./spinner-settings.json.template to merge in yourself."
  fi
}

activate_statusline_settings() {
  # Wires friday-statusline.sh into this folder's own ./.claude/settings.json,
  # merged alongside the spinner settings above and never clobbering them.
  # Same best-effort shape as activate_spinner_settings: never fails the
  # install, and a settings.json that already has a status line is left
  # untouched.
  local script_path="${INSTALL_PATH}/friday-statusline.sh"
  if [ ! -f "${script_path}" ]; then
    return 0
  fi
  chmod +x "${script_path}" 2>/dev/null || true

  local settings="./.claude/settings.json"

  if [ ! -f "${settings}" ]; then
    if ! mkdir -p "./.claude"; then
      echo "  Could not create ./.claude; skipped the status line step."
      return 0
    fi
    if command -v python3 >/dev/null 2>&1 && python3 -c 'import json,sys; json.dump({"statusLine": {"type": "command", "command": sys.argv[1], "padding": 0}}, open(sys.argv[2], "w"), indent=2)' "${script_path}" "${settings}" 2>/dev/null; then
      echo "  Created ${settings} with the Friday SHORTCUTS status line."
    else
      echo "  Could not write ${settings}; skipped the status line step."
    fi
    return 0
  fi

  if ! command -v python3 >/dev/null 2>&1; then
    echo "  python3 was not found, so the status line step was skipped."
    return 0
  fi

  local check_rc=0
  python3 -c 'import json,sys; s=json.load(open(sys.argv[1])); sys.exit(2 if "statusLine" in s else 0)' "${settings}" || check_rc=$?

  if [ "${check_rc}" = "2" ]; then
    echo "  ${settings} already has a status line configured. Left it untouched."
    return 0
  fi
  if [ "${check_rc}" != "0" ]; then
    echo "  Could not merge the status line into ${settings}; left it untouched."
    return 0
  fi

  local backup="${settings}.pre-friday-statusline-$(date +%F).bak"
  if ! cp "${settings}" "${backup}"; then
    echo "  Could not back up ${settings}; skipped the status line step."
    return 0
  fi

  local merge_rc=0
  python3 -c 'import json,sys; s=json.load(open(sys.argv[1])); s["statusLine"]={"type":"command","command":sys.argv[2],"padding":0}; f=open(sys.argv[1],"w"); json.dump(s,f,indent=2); f.write("\n"); f.close()' "${settings}" "${script_path}" || merge_rc=$?

  if [ "${merge_rc}" = "0" ]; then
    echo "  Backed up your existing settings to ${backup}"
    echo "  Added the Friday SHORTCUTS status line to ${settings}"
  else
    rm -f "${backup}"
    echo "  Could not merge the status line into ${settings}; left it untouched."
  fi
}

is_valid_git_clone() {
  # True only when $1 is itself a git working tree -- has its own .git here,
  # not one inherited by walking up to a parent repo -- so
  # update_foundation_repo has something real to fetch and reset. A plain
  # folder, or one whose .git got corrupted, fails this and falls back to
  # backup_existing_install_path + clone_foundation_repo instead.
  [ -d "${1}/.git" ] && git -C "${1}" rev-parse --is-inside-work-tree >/dev/null 2>&1
}

backup_existing_install_path() {
  # A non-empty ~/friday-shortcuts that is NOT a Friday Shortcuts git clone
  # (see is_valid_git_clone) is renamed aside with an epoch-seconds suffix
  # (unique even across same-day re-installs), never clobbered. Mirrors the
  # paid installer's --force rename pattern. A valid existing clone instead
  # goes through update_foundation_repo, which updates in place.
  if [ -d "${INSTALL_PATH}" ] && [ "$(ls -A "${INSTALL_PATH}" 2>/dev/null)" ]; then
    local backup="${INSTALL_PATH}.bak-$(date +%s)"
    echo "Found an existing ${INSTALL_PATH}. Backing it up to ${backup}"
    if ! mv "${INSTALL_PATH}" "${backup}"; then
      echo "  Could not back up ${INSTALL_PATH}. Move or remove it yourself, then re-run."
      return 1
    fi
  fi
  return 0
}

clone_foundation_repo() {
  echo "Cloning Friday Shortcuts into ${INSTALL_PATH}"
  if ! git clone --quiet --depth 1 --branch "${CLONE_BRANCH}" "${CLONE_URL}" "${INSTALL_PATH}"; then
    echo "  Failed to clone ${CLONE_URL} (branch ${CLONE_BRANCH})."
    echo "  Check your network connection and re-run the same install line."
    rm -rf "${INSTALL_PATH}"
    return 1
  fi
  echo "  Cloned to ${INSTALL_PATH}"
  return 0
}

update_foundation_repo() {
  # INSTALL_PATH is already a Friday Shortcuts git clone from a prior
  # install (is_valid_git_clone passed). Fast-forward its TRACKED files to
  # the current release tip with nothing but a fetch + a hard reset, so
  # untracked content -- the founder's friday/ output, CLAUDE.md.repo-guide,
  # .claude/ -- is never touched. CLAUDE.md is itself tracked upstream (the
  # repo's own contributor guide; see personalize_brain_files), so this
  # function only moves the git state forward. install_full_pack saves the
  # founder's live CLAUDE.md aside before calling this and restores it after,
  # via the same personalize_brain_files call a fresh install uses.
  echo "Updating the existing install at ${INSTALL_PATH}"
  if ! git -C "${INSTALL_PATH}" fetch --quiet --depth 1 origin "${CLONE_BRANCH}"; then
    echo "  Failed to fetch the latest ${CLONE_BRANCH} branch."
    echo "  Check your network connection and re-run the same install line."
    return 1
  fi
  if ! git -C "${INSTALL_PATH}" reset --quiet --hard FETCH_HEAD; then
    echo "  Failed to update ${INSTALL_PATH} to the latest release."
    echo "  Re-run the same install line to retry."
    return 1
  fi
  echo "  Updated to the latest release."
  return 0
}

sync_commands_to_folder() {
  # Copies every command file from the just-cloned ./commands/ into this
  # folder's own .claude/commands/, so the slash commands are scoped to
  # ~/friday-shortcuts and only work when Claude Code is opened from inside
  # it -- never a global sync into ~/.claude/commands/. Backs up a
  # locally-edited copy to <name>.md.bak; identical content is replaced
  # silently. Returns 1 if any file could not be synced.
  local dest_dir="${INSTALL_PATH}/.claude/commands"
  echo "Installing commands into ${dest_dir}"
  mkdir -p "${dest_dir}" || {
    echo "  Failed to create ${dest_dir}"
    return 1
  }
  local entry file src dest ok=0
  for entry in "${PACK_COMMANDS[@]}"; do
    file=$(echo "${entry}" | awk '{print $2}')
    src="./commands/${file}"
    dest="${dest_dir}/${file}"
    if [ ! -f "${src}" ]; then
      echo "  Missing from the clone: ${file}"
      FAILED_COMMANDS+=("${file}")
      ok=1
      continue
    fi
    if [ -f "${dest}" ] && ! cmp -s "${src}" "${dest}"; then
      if ! mv "${dest}" "${dest}.bak"; then
        echo "  Could not back up your existing ${file}; leaving it untouched."
        FAILED_COMMANDS+=("${file}")
        ok=1
        continue
      fi
      echo "  Backed up your existing ${file} to ${file}.bak"
    fi
    if ! cp "${src}" "${dest}"; then
      echo "  Failed to sync: ${file}"
      FAILED_COMMANDS+=("${file}")
      ok=1
      continue
    fi
    echo "  Installed: ${dest}"
  done
  return "${ok}"
}

open_claude_in_folder() {
  # Do NOT auto-launch Claude Code here. Exec-ing `claude </dev/tty` from a
  # curl | bash context strands the founder: that first Claude Code session's
  # folder-trust prompt cannot read the keyboard (arrows, Enter, Esc all dead),
  # so they sit on a frozen screen and read Friday as broken. Launching Claude
  # by hand in a clean terminal works every time. So print the one line to run
  # instead of opening it for them. Same instruction on every path.
  echo
  echo "Friday SHORTCUTS is installed at: ${INSTALL_PATH}"
  echo
  echo "To start, open it in Claude Code:"
  echo
  echo "  cd ${INSTALL_PATH} && claude"
  echo
  echo "Then type /amplify to begin."
  echo
}

install_full_pack() {
  echo "Friday SHORTCUTS: installing the full pack"
  echo

  # A pre-existing valid clone is updated in place (CLAUDE.md and friday/
  # survive); anything else at that path (first install, or a folder that
  # is not a Friday Shortcuts git clone) goes through the backup-then-clone
  # path unchanged.
  local claude_md_backup=""
  if [ -d "${INSTALL_PATH}" ] && is_valid_git_clone "${INSTALL_PATH}"; then
    if [ -f "${INSTALL_PATH}/CLAUDE.md" ]; then
      claude_md_backup="$(mktemp "${TMPDIR:-/tmp}/friday-claude-md.XXXXXX")" || {
        echo "  Could not create a temp file to protect your CLAUDE.md; stopping before any change."
        exit 1
      }
      cp "${INSTALL_PATH}/CLAUDE.md" "${claude_md_backup}"
    fi
    update_foundation_repo || {
      [ -n "${claude_md_backup}" ] && rm -f "${claude_md_backup}"
      exit 1
    }
  else
    if [ -d "${INSTALL_PATH}" ]; then
      echo "Found an existing ${INSTALL_PATH} that is not a Friday Shortcuts git clone."
      echo "Backing it up and installing fresh instead."
    fi
    backup_existing_install_path || exit 1
    clone_foundation_repo || exit 1
  fi

  cd "${INSTALL_PATH}" || {
    echo "Could not enter ${INSTALL_PATH}."
    exit 1
  }

  echo
  personalize_brain_files
  if [ -n "${claude_md_backup}" ]; then
    mv "${claude_md_backup}" "./CLAUDE.md"
    echo "  Restored your personalised CLAUDE.md."
  fi
  activate_brain_file
  echo
  local version_value
  version_value="$(cat "./VERSION" 2>/dev/null || true)"
  if [ -n "${version_value}" ]; then
    echo "  Installed version: ${version_value}"
  else
    echo "  Installed version: unknown (VERSION file missing from the clone)"
  fi
  echo
  activate_spinner_settings
  activate_statusline_settings
  echo
  sync_commands_to_folder || true

  # Honest close: never claim success while a command failed to sync.
  if [ ${#FAILED_COMMANDS[@]} -gt 0 ]; then
    echo
    echo "Finished, but some commands did not sync:"
    local c
    for c in "${FAILED_COMMANDS[@]}"; do
      echo "  command: ${c}"
    done
    echo
    echo "Re-run the same install line to retry."
    exit 1
  fi

  echo
  echo "All done. Friday SHORTCUTS is installed in ${INSTALL_PATH}."
  echo
  echo "Start here, in order:"
  echo "  1. /amplify          Your fastest first win. Five minutes, no setup."
  echo "                       Writes friday/growth.md: where to push next."
  echo "  2. /voice-installer  Optional but recommended. Makes every command"
  echo "                       write in your voice instead of a generic style."
  echo "  3. /brief            Tomorrow morning. Your priorities, filtered."
  echo
  echo "The full list of commands is in README.md and docs/foundation-manual.md."
  echo "New here? Read harness/00-how-friday-works.md to understand what you installed."

  open_claude_in_folder
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
      echo "Friday Shortcuts: installing ${slug}"
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
    echo "Available: voice-installer, decide, brief, meetingprep, weeklyreview, amplify, new-capability, explore-idea, scope-decision, learnings, shipping-retro, teach-team, validate-idea, go-to-market, pricing-strategy, offer-creation, competitive-analysis, sop-builder, product-hunt-launch, changelog, positioning, roadmap, customer-feedback, risk-register, friday-upgrade"
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

  local capability=""
  while [ $# -gt 0 ]; do
    case "$1" in
      --lead)
        LEAD_TOKEN="${2:-}"
        shift 2
        ;;
      *)
        capability="$1"
        shift
        ;;
    esac
  done

  if [ -z "${capability}" ]; then
    require_tool git "Install git first: it ships with Xcode Command Line Tools on macOS (run 'xcode-select --install') or via 'sudo apt-get install git' on Linux." || exit 1
    install_full_pack
  else
    install_single "${capability}"
  fi
}

main "$@"
