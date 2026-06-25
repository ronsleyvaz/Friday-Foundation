<!-- audience: external-general -->
# Friday for Claude Code

Make every AI tool you use write in your voice. Five minutes, one command, no code.

This is the free, runnable version of Friday, the AI Chief of Staff. You build it one capability at a time. Each capability is a brick you install into Claude Code with one line. Each brick writes a real file to your machine and shows you the before and the after, so you feel the improvement the moment it lands.

Brick 1 is the Voice Installer.

## Install

You need Claude Code installed and open. Then run this in your terminal:

```
curl -fsSL https://raw.githubusercontent.com/ronsleyvaz/Friday-for-Claude-Code/main/install.sh | bash
```

It checks for Claude Code, drops the command into `~/.claude/commands/`, and tells you the next step. Nothing phones home. No account. No paid install.

Then open Claude Code and run:

```
/voice-installer
```

## What brick 1 does

The Voice Installer interviews you, reads two or three things you have written, and writes a real voice config to your machine:

- `friday/voice.md`, your voice profile, readable by any AI tool
- a voice block in your `CLAUDE.md`, so Claude Code reads it every session

Then it proves the win. It takes a sample paragraph of default AI copy, rewrites it in your voice using the profile it just wrote, and shows you both side by side. That difference is the point.

Full background: [why the Voice Installer matters](docs/voice-installer-why-guide.md).

## The ladder

This is brick 1. More bricks land in this repo over time, and each one appends to the same `friday/` folder:

- Brick 2: Decision Runner. Paste a real decision, get one problem, three options, one pick, written in your voice.
- More to come.

You watch your `friday/` config grow, capability by capability.

## What this is not

A brick runs when you run it. It does not read your inbox, your calendar, or your transcripts. It does not work while you sleep.

That part is Friday, the full AI Chief of Staff: nine specialists wired together, trained on your voice and your stories, connected to your stack, in one install. That is the paid product at [friday.amplifyais.com](https://friday.amplifyais.com).

This repo is what one capability feels like, by hand, for free.

## Prerequisite

Claude Code, installed and logged in. Setup guide: https://docs.anthropic.com/claude-code

## Licence

MIT. See [LICENSE](LICENSE).

---

Built by Amplify AI at amplifyais.com
