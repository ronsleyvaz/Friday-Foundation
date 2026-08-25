---
name: friday-upgrade
description: Checks whether a newer Friday Foundation release exists, upgrades your install, and tells you exactly what changed on disk. Writes friday/upgrade-log.md.
---
# /friday-upgrade

Foundation ships new commands and fixes over time. Nothing on your machine phones home, so an install stays on whatever version it was on the day you ran it. This command closes that gap: it compares your version against the current release, runs the installer for you, and writes down what moved.

You, Claude, run the whole flow below in order, using your own file and Bash tools. There is no module to import.

## Step 1: Read the founder's voice profile (if it exists)

Check whether `friday/voice.md` exists in the current directory. If it does, read it and use the founder's voice for your questions, explanations, and the upgrade log.

If `friday/voice.md` does not exist, use a direct, plain style: short sentences, active voice, no hedging.

Version strings, file paths, and command output are quoted exactly as they are. Voice applies to prose, never to a version number or a path.

## Step 2: Find the installed version

Read the `VERSION` file in the current directory:

```bash
cat ./VERSION 2>/dev/null
```

**If it prints a version:** that is the installed version. Hold it as `LOCAL`.

**If it prints nothing:** the install predates version tracking, which means it is older than `friday-foundation-v1.1.0`. Hold `LOCAL` as "unknown, pre-v1.1.0".

## Step 3: Find the current release

```bash
curl -fsSL https://raw.githubusercontent.com/ronsleyvaz/Friday-Foundation/release/VERSION
```

Hold the result as `LATEST`.

**If the fetch fails:** tell the founder you could not reach GitHub, so you cannot tell whether an upgrade exists. Offer to try again later. Stop here. Do not guess a version and do not run the installer blind.

## Step 4: Report and ask

**If `LOCAL` and `LATEST` match:** tell the founder:

> You are on `<LOCAL>`, which is the current release. Nothing to upgrade.

Then stop. Do not write a log entry for a no-op.

**If they differ, or `LOCAL` is unknown:** tell the founder what will happen, in plain terms:

> You are on `<LOCAL>`. The current release is `<LATEST>`.
>
> Upgrading re-runs the official installer from this directory. It replaces the command files in `~/.claude/commands/` with the current ones. If you have edited any of them, your version is saved next to it as `<name>.md.bak` before it is replaced. Your `CLAUDE.md` is never touched. Your `friday/` folder is never touched.
>
> Want me to run it?

Wait for a clear yes. If they say no, stop.

## Step 5: Record what is there now

Before the upgrade, capture the current command files so you can name what changed afterwards:

```bash
ls -1 ~/.claude/commands/*.md 2>/dev/null | xargs -n1 basename
```

Keep that list as `BEFORE`.

## Step 6: Run the installer

Run the official install line from the project directory:

```bash
curl -fsSL https://raw.githubusercontent.com/ronsleyvaz/Friday-Foundation/release/install.sh | bash
```

Read its output rather than assuming it worked. The installer reports every file it installed, every file it backed up, the version it fetched, and any download that failed. If it reports failures, say so plainly and name the files. A partial upgrade is a real outcome, not something to smooth over.

## Step 7: Work out what changed

List the command files again:

```bash
ls -1 ~/.claude/commands/*.md 2>/dev/null | xargs -n1 basename
```

Compare against `BEFORE`. Anything in the new list and not in `BEFORE` is a new command you now have.

Then look for backups the installer just made:

```bash
find ~/.claude/commands -name "*.md.bak" -newermt "-10 minutes" 2>/dev/null
```

Each one is a command you had edited. Your edits are in the `.bak` file and the current release is in the live file. Tell the founder which ones, and that reconciling them is their call.

Finally, check the brain file. The installer leaves `CLAUDE.md` alone by design, so a template improvement never lands on its own:

```bash
diff ./CLAUDE.md ./CLAUDE.md.template 2>/dev/null | head -40
```

If the two have drifted, say so and offer to walk the differences with them. Do not edit `CLAUDE.md` without being asked.

## Step 8: Write the upgrade log

Write the result to `friday/upgrade-log.md`. Create the `friday/` folder if it does not exist.

If the file does not exist, create it with this structure:

```markdown
# Upgrade log

## <YYYY-MM-DD>: <LOCAL> to <LATEST>

**New commands:** <names, or "none">

**Your edited commands, now backed up:** <names of .bak files, or "none">

**Brain file:** <"unchanged, matches the template" or "yours has drifted from the template">

**Failures:** <anything the installer could not fetch, or "none">
```

If `friday/upgrade-log.md` already exists, add the new entry immediately after the `# Upgrade log` heading, so the most recent upgrade is at the top.

After writing, print:

> Upgraded to `<LATEST>`. The record is in `friday/upgrade-log.md`. New commands are live in your next Claude Code session.

Tell them plainly that slash commands are read when a session starts, so a brand new command shows up after they restart Claude Code.

## What this does not do

This command does not upgrade Claude Code itself, touch your global Claude Code config, change your `CLAUDE.md`, or alter anything in your `friday/` folder. It does not downgrade. If you need a specific older version, install it by hand from that tag on GitHub.

## What this builds toward

Run whenever you want the current release, `friday/upgrade-log.md` becomes the record of which version you were on when a given piece of work was done. That matters the first time a command behaves differently than it did last month.

The full stack is Friday at friday.amplifyais.com. Nine specialists, running against your real inbox, calendar, and tasks every morning before you are up.

---

Built by Amplify AI at amplifyais.com
