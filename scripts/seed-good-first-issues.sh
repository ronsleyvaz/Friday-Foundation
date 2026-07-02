#!/usr/bin/env bash
#
# seed-good-first-issues.sh
#
# Posts a starter set of "good first issue" tickets to the Friday Foundation
# repo. Each one is a self-contained new command to build, sized for a first
# contribution. Run it once to open the on-ramp for contributors.
#
# Requirements: the GitHub CLI (gh) authenticated against the repo.
# Safe to re-run: it skips any issue whose exact title already exists open.
#
# Usage:
#   bash scripts/seed-good-first-issues.sh
#
set -euo pipefail

REPO="ronsleyvaz/Friday-Foundation"
LABEL="good first issue"

# Ensure the label exists. Ignore the error if it already does.
gh label create "$LABEL" --repo "$REPO" --color "7057ff" \
  --description "A contained task suitable for a first contribution" 2>/dev/null || true

create_issue() {
  local title="$1"
  local body="$2"
  if gh issue list --repo "$REPO" --state open --search "\"$title\" in:title" \
       --json title --jq '.[].title' 2>/dev/null | grep -Fxq "$title"; then
    echo "SKIP (already open): $title"
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

It is a common founder job that Foundation does not cover yet, and it fits the pack cleanly alongside the existing commands.

## What a good solution looks like

- [ ] \`commands/$1.md\` with valid frontmatter (name and description)
- [ ] Reads \`friday/voice.md\` if it exists and writes in the founder's voice
- [ ] Writes its output to \`$3\`
- [ ] Tells the founder what to do next after it runs
- [ ] A test in \`tests/\` that checks the frontmatter and structure
- [ ] \`python -m pytest tests/\` is green

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
