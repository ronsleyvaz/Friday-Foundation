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
> Upgrading re-runs the official installer. It updates Foundation's own files in `~/friday-shortcuts` to the current release in place. Your personalised `CLAUDE.md` and your whole `friday/` output folder are left untouched, byte for byte. The commands in `~/friday-shortcuts/.claude/commands/` are replaced with the current ones; if you had edited any, your version is saved next to it as `<name>.md.bak`.
>
> Want me to run it?

Wait for a clear yes. If they say no, stop.

## Step 5: Record what is there now

Before the upgrade, capture the current command files so you can name what changed afterwards:

```bash
ls -1 ./.claude/commands/*.md 2>/dev/null | xargs -n1 basename
```

Keep that list as `BEFORE`.

## Step 6: Run the installer

Run the official install line, from inside `~/friday-shortcuts`:

```bash
curl -fsSL https://raw.githubusercontent.com/ronsleyvaz/Friday-Foundation/release/install.sh | bash
```

Read its output rather than assuming it worked. Because this folder is already a Friday Foundation install, the installer updates it in place: your `CLAUDE.md` and `friday/` folder are left untouched, and Foundation's own files (commands, harness, `VERSION`) move to the new release. It reports the version it fetched and any command that failed to sync. If it reports failures, say so plainly and name the files. A partial upgrade is a real outcome, not something to smooth over.

If the installer instead reports that this folder was not a valid git clone and it backed the whole thing up before cloning fresh, that is the one case where your `CLAUDE.md` and `friday/` folder end up in the timestamped backup path it names. Tell the founder plainly and offer to copy them back.

## Step 7: Work out what changed

List the command files again:

```bash
ls -1 ./.claude/commands/*.md 2>/dev/null | xargs -n1 basename
```

Compare against `BEFORE`. Anything in the new list and not in `BEFORE` is a new command you now have.

Then look for backups the installer just made:

```bash
find ./.claude/commands -name "*.md.bak" -newermt "-10 minutes" 2>/dev/null
```

Each one is a command you had edited. Your edits are in the `.bak` file and the current release is in the live file. Tell the founder which ones, and that reconciling them is their call.

`CLAUDE.md` needs no check here: the upgrade path preserves it in place, so unless Step 6 reported the non-git-clone fallback, it is exactly what it was before you ran this.

## Step 8: Write the upgrade log

Write the result to `friday/upgrade-log.md`. Create the `friday/` folder if it does not exist.

If the file does not exist, create it with this structure:

```markdown
# Upgrade log

## <YYYY-MM-DD>: <LOCAL> to <LATEST>

**New commands:** <names, or "none">

**Your edited commands, now backed up:** <names of .bak files, or "none">

**Brain file:** <"preserved in place, untouched" or, only if Step 6 reported the non-git-clone fallback, "your personalised CLAUDE.md is in the backup folder, not copied back yet">

**Failures:** <anything the installer could not fetch, or "none">
```

If `friday/upgrade-log.md` already exists, add the new entry immediately after the `# Upgrade log` heading, so the most recent upgrade is at the top.

After writing, print:

> Upgraded to `<LATEST>`. The record is in `friday/upgrade-log.md`. New commands are live in your next Claude Code session.

Tell them plainly that slash commands are read when a session starts, so a brand new command shows up after they restart Claude Code.

## What this does not do

This command does not upgrade Claude Code itself, and it does not touch your global Claude Code config. It does not downgrade. If you need a specific older version, install it by hand from that tag on GitHub.

It updates Foundation's own files in `~/friday-shortcuts` in place. Your personalised `CLAUDE.md` and your whole `friday/` output folder are never touched, unless the installer had to fall back to a fresh clone because the folder was not a valid git clone -- it says so plainly when that happens.

## What this builds toward

Run whenever you want the current release, `friday/upgrade-log.md` becomes the record of which version you were on when a given piece of work was done. That matters the first time a command behaves differently than it did last month.

The full stack is Friday at friday.amplifyais.com. Nine specialists, running against your real inbox, calendar, and tasks every morning before you are up.

---

Built by Amplify AI at amplifyais.com
