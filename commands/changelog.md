---
name: changelog
description: Turn git history since the last release into a human-readable changelog a founder can share with customers. Writes friday/changelog.md. Reads friday/voice.md if present and writes in your voice.
---
# /changelog

Release notes should sound like a founder who understands what changed, not a raw commit dump. This command reads the git history since the last release, filters it into customer-facing meaning, and writes a changelog entry that can be shared with users, investors, or the team.

You, Claude, run the whole flow below in order, using your own file tools. There is no module to import and nothing to install.

## Step 1: Read the founder's voice profile (if it exists)

Check whether `friday/voice.md` exists in the current directory. If it does, read it and write all output in the founder's voice.

If `friday/voice.md` does not exist, write in a direct, plain style: short sentences, active voice, no hedging.

## Step 2: Check for a git repo

Check whether the current directory is inside a git repository:

```bash
git rev-parse --is-inside-work-tree 2>/dev/null
```

**If it is not a git repo:** ask the founder:

> This is not a git repo, so I cannot read commit history. Paste the changes you want turned into a changelog, or tell me the release version and the main things that changed.

Wait for their answer, then go to Step 5.

**If it is a git repo:** continue to Step 3.

## Step 3: Find the release boundary

Try to find the most recent tag:

```bash
git describe --tags --abbrev=0 2>/dev/null
```

**If a tag exists:** use it as the release boundary. Tell the founder:

> Found latest release tag `<tag>`. I will build the changelog from commits after that tag.

Then read the commit history:

```bash
git log <tag>..HEAD --pretty=format:"%h %ad %s" --date=short
```

Also read the file summary:

```bash
git diff --stat <tag>..HEAD
```

**If no tag exists:** ask the founder:

> I do not see a release tag. What should count as the starting point for this changelog? Give me a tag, commit hash, date, or say "last 30 days."

Wait for the answer.

If they give a tag or commit hash, run:

```bash
git log <start>..HEAD --pretty=format:"%h %ad %s" --date=short
git diff --stat <start>..HEAD
```

If they give a date or say "last 30 days," run:

```bash
git log --since="<date or 30 days ago>" --pretty=format:"%h %ad %s" --date=short
```

If the git history is empty, tell the founder:

> I found no commits for that range. I can still write the changelog from your notes.

Then ask them to describe what changed before proceeding.

## Step 4: Get release context

Ask these questions in one batch:

> What release name or version should this use?
>
> Who is this changelog for: customers, investors, internal team, or all three?
>
> Is there anything in the commit list that should not be public?

Wait for the founder's answer before writing.

## Step 5: Turn changes into a shareable changelog

Use the commit history, diff summary, and founder context to write one changelog entry.

Group changes under only the headings that apply:

```text
## Added
<New capabilities, workflows, content, or user-visible support.>

## Changed
<Meaningful improvements to existing behavior.>

## Fixed
<Bugs, confusing behavior, broken flows, or reliability fixes.>

## Removed
<Anything intentionally removed or deprecated.>
```

Do not include raw commit hashes unless the founder asked for an internal changelog. Translate commit messages into outcomes. If a commit is unclear, say what it appears to be and keep the wording conservative. Do not expose secrets, private customer names, unreleased business plans, or anything the founder marked as not public.

Keep the entry specific. "Improved dashboard" is weak. "Added a clearer onboarding checklist for first-time users" is useful.

## Step 6: Write the changelog

Write the result to `friday/changelog.md`. Create the `friday/` folder if it does not exist.

If the file does not exist, create it with this structure:

```markdown
# Changelog

## <Release name or version>: <YYYY-MM-DD>

### Summary

<Two or three plain sentences about what changed and why it matters.>

### Added

<Only include if there are added items.>

### Changed

<Only include if there are changed items.>

### Fixed

<Only include if there are fixed items.>

### Removed

<Only include if there are removed items.>

### Next steps

<Tell the founder what to do next: review, cut a release, publish to customers, or send internally.>
```

If `friday/changelog.md` already exists, add the new entry near the top, immediately after `# Changelog` if that heading exists. If there is no top-level heading, append this run below the existing content with a separator:

```markdown
---

## <Release name or version>: <YYYY-MM-DD>
```

Write in the founder's voice. If their profile lists banned words, do not use any of them.

After writing, print:

> Changelog saved to `friday/changelog.md`. Review it for anything that should stay private, then use it as your release note or customer update.

## What this does not do

This command does not publish a GitHub release, create a tag, or push anything to a remote. It only reads local history and writes a shareable changelog entry.

## What this builds toward

Run before each release, `friday/changelog.md` becomes the plain-language record of what changed and why customers should care. It also turns scattered commit history into release discipline.

The full stack is Friday at friday.amplifyais.com. Nine specialists, running against your real inbox, calendar, and tasks every morning before you are up.

---

Built by Amplify AI at amplifyais.com
