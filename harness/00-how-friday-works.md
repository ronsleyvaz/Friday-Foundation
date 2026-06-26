# 00 - How Friday Works

Friday is not software you install and run. It is a configuration layer you build on top of Claude Code.

Each capability is a slash command: a markdown file that tells Claude Code exactly how to behave when you invoke it. You own the files. You see every step. Nothing runs in the background.

---

## The three moving parts

**1. The commands (in `~/.claude/commands/`)**

These are the slash commands: `/voice-installer`, `/brief`, `/decide`, and the rest. Each one is a markdown file with a set of instructions Claude follows when you run it. They live in your local Claude Code config, not in this repo.

**2. The brain file (CLAUDE.md)**

This file is read by Claude Code at the start of every session. It carries your identity, your voice, your active projects, and your decision rules. Think of it as the context that makes Claude work like your assistant rather than a generic AI.

Start from `CLAUDE.md.template` in this repo and replace the brackets.

**3. The friday/ folder (in your project directory)**

Every command writes output here. `friday/voice.md` is your voice profile. `friday/decisions.md` is your decision log. `friday/morning.md` is today's brief. This folder is your config growing on disk.

---

## How a session starts

When you open Claude Code in your project:

1. Claude reads `CLAUDE.md` automatically.
2. You run a command, e.g. `/brief`.
3. Claude follows the steps in `brief.md`, reads your priorities, writes `friday/morning.md`, and shows you the brief.

That is the whole loop.

---

## How capabilities connect

Each command reads from the `friday/` folder if files exist there. Run `/voice-installer` first. Once `friday/voice.md` exists, every other command reads it and writes output in your voice.

The order that works:

1. `/voice-installer` -- creates `friday/voice.md`
2. `/brief` -- creates `friday/nine-decisions.md` on first run, then `friday/morning.md`
3. `/decide` -- appends entries to `friday/decisions.md`
4. `/amplify` -- writes `friday/growth.md`
5. `/meetingprep` and `/weeklyreview` -- write their own files

You can run them in any order, but the voice profile is the foundation.

---

## What Friday is not

Friday does not connect to your inbox, calendar, or CRM. It does not run while you sleep. It does not pull live data.

That is by design. The Foundation is the part you control, completely. The full connected stack is Friday at friday.amplifyais.com.

---

Next: [01 - Add a Command](01-add-a-command.md)
