#!/usr/bin/env bash
#
# seed-good-first-issues.sh
#
# Posts a starter set of "good first issue" tickets to the Friday Shortcuts
# repo. Each one is a self-contained new command to build, sized for a first
# contribution. Run it once to open the on-ramp for contributors.
#
# Requirements: the GitHub CLI (gh) authenticated against the repo.
# Safe to re-run: it skips any seed whose command already ships (a file in
# commands/ or an entry in install.sh's PACK_COMMANDS) and any issue whose
# exact title already exists, open or closed.
#
# Usage:
#   bash scripts/seed-good-first-issues.sh
#
set -euo pipefail

REPO="ronsleyvaz/Friday-Foundation"
LABEL="good first issue"

# Resolve the repo root from the script location so the dedup guards work
# regardless of the directory the script is invoked from.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
if [ ! -f "$REPO_ROOT/install.sh" ] || [ ! -d "$REPO_ROOT/commands" ]; then
  echo "Cannot find the repo root from $SCRIPT_DIR; run as: bash scripts/seed-good-first-issues.sh" >&2
  exit 1
fi

# Ensure the label exists. Ignore the error if it already does.
gh label create "$LABEL" --repo "$REPO" --color "7057ff" \
  --description "A contained task suitable for a first contribution" 2>/dev/null || true

# check_command_exists: returns 0 if a command file is already in commands/ or PACK_COMMANDS
check_command_exists() {
  local cmd_name="$1"
  # Check if the command markdown file exists
  if [ -f "$REPO_ROOT/commands/${cmd_name}.md" ]; then
    return 0
  fi
  # Check if the command is listed in PACK_COMMANDS in install.sh. Anchored
  # to the manifest line shape so a usage comment or an unrelated string
  # that merely starts with the name cannot match.
  if grep -qE "^[[:space:]]*\"${cmd_name}[[:space:]]" "$REPO_ROOT/install.sh"; then
    return 0
  fi
  return 1
}

create_issue() {
  local title="$1"
  local body="$2"
  # Extract the command name from the title (e.g., "/standup command" -> "standup")
  local cmd_name
  cmd_name=$(echo "$title" | sed -n 's/.*\/\([a-z0-9-]*\) command.*/\1/p')

  # Skip if a command with this name already exists on disk or in the manifest
  if [ -n "$cmd_name" ] && check_command_exists "$cmd_name"; then
    echo "SKIP (command '$cmd_name' already exists): $title"
    return 0
  fi

  # Check both open AND closed issues to avoid recreating closed ones.
  # `gh issue list` defaults to --state open, so --state all is required
  # for the dedup guard to actually see closed issues. Read the whole
  # listing into a variable first: piping it straight into grep -q can exit
  # early, kill gh with SIGPIPE and, under pipefail, read as "not found".
  # A gh failure (auth, network, search rate limit) stops the run instead of
  # falling through to gh issue create.
  local existing
  existing="$(gh issue list --repo "$REPO" --state all --limit 100 \
       --search "\"$title\" in:title" --json title --jq '.[].title')" || {
    echo "gh issue list failed for: $title" >&2
    exit 1
  }
  if grep -Fxq -- "$title" <<<"$existing"; then
    echo "SKIP (issue already exists, open or closed): $title"
    return 0
  fi
  gh issue create --repo "$REPO" --title "$title" --body "$body" --label "$LABEL" >/dev/null
  echo "CREATED: $title"
}

body_for() {
  # $1 command, $2 what it does, $3 output path, $4 model command, $5 effort
  cat <<EOF
## What needs doing?

Build a new \`/$1\` command that $2

## Why it matters

It is a common founder job that Shortcuts does not cover yet, and it fits the pack cleanly alongside the existing commands.

## How to claim

Comment on this issue to claim it, and a maintainer will assign it to you. If it is already assigned or has a claim comment, please pick another so no one duplicates work.

## What a good solution looks like

- [ ] \`commands/$1.md\` with valid frontmatter (name and description)
- [ ] Reads \`friday/voice.md\` if it exists and writes in the founder's voice
- [ ] Writes its output to \`$3\`
- [ ] Registered in \`PACK_COMMANDS\` in \`install.sh\` (keeps it installable; the catalog parity tests enforce the rest)
- [ ] Added to \`COMMANDS\` in \`friday-usage.sh\`, plus a folder form in \`classify_output\` if it writes a folder (\`tests/test_usage_reporter.py\` fails until you do)
- [ ] Tells the founder what to do next after it runs
- [ ] A test in \`tests/\` that checks the frontmatter and structure
- [ ] \`python3 -m pytest tests/\` is green

## Suggested starting point

Copy \`commands/$4.md\` as your model. Read \`CONTRIBUTING.md\` first for the quality bar.

## Estimated effort

$5
EOF
}

create_issue "[GOOD FIRST ISSUE] /standup command" \
  "$(body_for "standup" "generates a daily standup from the founder's recent git history and yesterday's notes, so they walk into the day knowing what shipped and what is next." "friday/standup.md" "shipping-retro" "One session in Claude Code, about one to two hours.")"

create_issue "[GOOD FIRST ISSUE] /follow-up command" \
  "$(body_for "follow-up" "turns a meeting note into a clear list of follow-up messages and actions with owners, so nothing agreed in the room gets dropped." "friday/follow-ups.md" "meetingprep" "One session in Claude Code, about one to two hours.")"

create_issue "[GOOD FIRST ISSUE] /changelog command" \
  "$(body_for "changelog" "turns git history since the last release into a human-readable changelog a founder can share with customers." "friday/changelog.md" "shipping-retro" "One session in Claude Code, about one to two hours.")"

create_issue "[GOOD FIRST ISSUE] /hiring-brief command" \
  "$(body_for "hiring-brief" "turns a rough role idea into a hiring brief and an interview scorecard, so a first hire is judged against clear criteria." "friday/hiring/<role>.md" "sop-builder" "One session in Claude Code, about one to two hours.")"

create_issue "[GOOD FIRST ISSUE] /objection-handler command" \
  "$(body_for "objection-handler" "maps a founder's top sales objections to honest, specific responses they can actually say out loud." "friday/objections.md" "competitive-analysis" "One session in Claude Code, about one to two hours.")"

create_issue "[GOOD FIRST ISSUE] /roadmap command" \
  "$(body_for "roadmap" "turns a goal into a sequenced ninety-day roadmap with milestones and the one thing to do first." "friday/roadmap.md" "go-to-market" "One session in Claude Code, about one to two hours.")"

create_issue "[GOOD FIRST ISSUE] /customer-interview command" \
  "$(body_for "customer-interview" "writes a non-leading discovery-call script and question set, so a founder learns the truth from a customer conversation instead of fishing for a yes." "friday/interviews/<name>.md" "validate-idea" "One session in Claude Code, about one to two hours.")"

create_issue "[GOOD FIRST ISSUE] /positioning command" \
  "$(body_for "positioning" "writes a positioning statement (category, target customer, key benefit, and what makes it different from the alternatives), so a founder can say what they do in one clear line." "friday/positioning.md" "offer-creation" "One session in Claude Code, about one to two hours.")"

echo ""
echo "Done. Review the open issues at https://github.com/$REPO/issues"
