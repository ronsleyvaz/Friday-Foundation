<!-- audience: buyer -->
# Friday Foundation: Build Your Own AI Chief of Staff

**Free. Open-source. Runs on your machine, with your keys.**

Foundation is the skeleton. Install it, run the commands, and your AI starts writing in your voice, filtering your priorities through your nine business decisions, and diagnosing where to push next.

There are no specialists running in the background. No overnight queue. No connected inbox. Those live in the paid stack. Foundation is what you build yourself, step by step, with full visibility into every command you run.

Three rules sit under everything Foundation does:

1. **Foundation drafts. You decide. Nothing sends itself.** Every command writes a file to your project directory. No external connections fire unless you wire them yourself.
2. **Foundation uses what you give it.** The voice profile reads your actual writing. The brief works from priorities you paste in. The growth diagnostic scores what you tell it. No fabricated data.
3. **If a file does not exist yet, Foundation tells you which command creates it.** Clear sequencing. No silent failures.

---

## Start where you are

Find your state below. There is a move for each.

| You are | It feels like | Your move |
|---|---|---|
| **Brand new** | Just installed, not sure what to run first | `/voice-installer`, five minutes, once |
| **Voice set up, nothing else running** | Output sounds generic, not like you | `/brief` to set your nine decisions and write today's brief |
| **Briefed, want growth clarity** | Busy but no clear priority | `/amplify`, eight vital signs, one 90-day plan |
| **Running well, want to extend** | The built-in commands do not cover your workflow | `/new-capability` to scaffold your own |
| **Something is off** | A command is not writing where you expect | Check the Troubleshooting section below |

### Brand new
Install Foundation in one line and start with `/voice-installer`. That command interviews you, reads two or three files you have written, and builds your voice profile. Every other command reads from that profile. Without it, every command writes in generic AI copy.

### Voice set up, nothing else running
Run `/brief`. The first run walks you through naming your nine decisions: the recurring forks your business turns on. Hire or contract. Build or buy. Which channel gets this week's content. Once they are named, every brief filters your open items through them and names one thing to start with.

### Briefed, want growth clarity
Run `/amplify`. It scores eight vital signs, detects your business stage, finds your biggest lever, and writes a prioritised 90-day plan. Takes about five minutes. Honest scores get you a useful plan. Optimistic scores get you a plan that misses the real gap.

### Running well, want to extend
Run `/new-capability`. It asks for a name, a purpose, and an output file. It scaffolds a command from a template. You fill in the logic and it runs like any other slash command.

---

## Quick start: install and first fifteen minutes

### Install

```bash
curl -fsSL https://raw.githubusercontent.com/ronsleyvaz/Friday-Foundation/release/install.sh | bash
```

You need Claude Code installed first. Get it at https://docs.anthropic.com/claude-code

The installer puts all 22 commands into `~/.claude/commands/`, creates a `CLAUDE.md` brain file in your current directory from `CLAUDE.md.template` (any existing one is left untouched), and downloads the six-part harness guide to `./harness/`.

### Install a single command

```bash
curl -fsSL https://raw.githubusercontent.com/ronsleyvaz/Friday-Foundation/release/install.sh | bash -s -- amplify
```

Replace `amplify` with any command name.

### First fifteen minutes

Open Claude Code in your project directory.

**One. Run the growth diagnostic (your fastest win, no setup).**

```
/amplify
```

Eight vital signs. Five minutes. One prioritised 90-day plan written to `friday/growth.md`. Nothing to configure first.

**Two. Build your voice profile (optional but recommended, run once).**

```
/voice-installer
```

It asks you five questions, reads two or three files you have written, and writes `friday/voice.md`. Every command that runs after reads from that file, so your output matches your actual writing instead of a generic AI imitation. Skipping it is safe: commands fall back to a neutral, direct style until you run it.

**Three. Get your morning brief.**

```
/brief
```

First run walks you through naming your recurring decisions (three is enough to start). Every run after that filters your priorities through them and writes `friday/morning.md`. The brief names one thing to start with.

You are running.

---

## How Foundation works

Foundation is a set of commands built on top of Claude Code. There is no background process. Nothing runs while you are not in a session.

Each capability is a markdown file in `~/.claude/commands/`. When you run a command, Claude Code reads that file and follows the steps inside it. You see every step. You own every file it creates.

### The friday/ folder

Every command writes to a `friday/` folder in your project directory. That folder is your config, growing over time.

| File | Created by | What it holds |
|---|---|---|
| `friday/voice.md` | `/voice-installer` | Your voice profile: tone, rhythm, signature phrases, banned words |
| `friday/nine-decisions.md` | `/brief` (first run) | The nine recurring decisions your business turns on |
| `friday/morning.md` | `/brief` | Today's brief, overwritten each run |
| `friday/decisions.md` | `/decide` | Your decision log, one entry per run |
| `friday/meetings.md` | `/meetingprep` | Your meeting briefs |
| `friday/review.md` | `/weeklyreview` | Your weekly reviews |
| `friday/growth.md` | `/amplify` | Your growth diagnostic and 90-day plan |
| `friday/idea-exploration.md` | `/explore-idea` | The six forcing questions run against a new idea |
| `friday/scope-decision.md` | `/scope-decision` | Your expansion, hold, or reduction call on a plan |
| `friday/learnings.md` | `/learnings` | A running log of patterns, preferences, and pitfalls |
| `friday/shipping-retro.md` | `/shipping-retro` | Weekly reflection built from your git commit history |
| `friday/changelog.md` | `/changelog` | Customer-facing release notes built from git history |
| `friday/teaching/<topic>.md` | `/teach-team` | Onboarding plans for team members or contractors |
| `friday/validation.md` | `/validate-idea` | A 7-dimension idea validation and verdict |
| `friday/roadmap.md` | `/roadmap` | A sequenced 90-day roadmap and first-week action |
| `friday/gtm-plan.md` | `/go-to-market` | Your phased launch plan |
| `friday/pricing.md` | `/pricing-strategy` | Your pricing model and tier structure |
| `friday/offer.md` | `/offer-creation` | Your value-equation offer review |
| `friday/positioning.md` | `/positioning` | Your positioning statement and next move |
| `friday/competitive-analysis.md` | `/competitive-analysis` | Your competitor teardown and SWOT |
| `friday/sops/<process-name>.md` | `/sop-builder` | Documented SOPs for repeatable processes |
| `friday/product-hunt-launch.md` | `/product-hunt-launch` | Your Product Hunt specific launch runbook |

Custom commands you build will add their own files here.

### The brain file

`CLAUDE.md.template` lands in your project directory during install, and the installer copies it to `CLAUDE.md` for you (unless you already have one). Open `CLAUDE.md`. Replace every `[bracket]` with your own content. Claude Code reads `CLAUDE.md` (not the template) at the start of every session. It holds your identity, your voice pointer, and your decision rules.

Once `/voice-installer` has run, wire your voice profile into `CLAUDE.md`:

```
## Voice
See `friday/voice.md` for the full voice profile.
Match the tone, rhythm, and signature phrases.
Never use the words on the banned list.
```

---

## The 22 commands

### Set up first

| Command | What it does | Output |
|---|---|---|
| `/voice-installer` | Interviews you, reads your writing samples, writes your voice profile | `friday/voice.md` |

Recommended early, though optional. Every other command reads this profile if it exists, and falls back to a neutral, direct style if you skip it.

### Daily tools

| Command | What it does | Output |
|---|---|---|
| `/brief` | Filters your priorities through your nine business decisions | `friday/morning.md` |
| `/decide` | Runs the 1-3-1 protocol: one problem, three options, one pick | `friday/decisions.md` |
| `/meetingprep` | Produces a brief with context, your desired outcome, and three sharp questions | `friday/meetings.md` |
| `/weeklyreview` | Walks through wins, misses, and carry-forwards, then names one priority | `friday/review.md` |
| `/shipping-retro` | Weekly reflection built from your real git commit history | `friday/shipping-retro.md` |
| `/learnings` | Reviews, searches, and prunes what Friday has learned about your business | `friday/learnings.md` |
| `/changelog` | Turns git history into customer-facing release notes | `friday/changelog.md` |

### Growth

| Command | What it does | Output |
|---|---|---|
| `/amplify` | Runs the Amplify growth diagnostic on your eight vital signs | `friday/growth.md` |
| `/go-to-market` | Phased launch plan: pre-launch, launch week, 30/60/90 days | `friday/gtm-plan.md` |
| `/pricing-strategy` | Value-based pricing model and tier design with real numbers | `friday/pricing.md` |
| `/offer-creation` | Value-equation review, finds your offer's weakest lever | `friday/offer.md` |
| `/positioning` | Builds a clear positioning statement and next move | `friday/positioning.md` |
| `/competitive-analysis` | Competitor teardown: comparison matrix plus SWOT | `friday/competitive-analysis.md` |
| `/product-hunt-launch` | Product Hunt specific launch runbook | `friday/product-hunt-launch.md` |

### Idea and scope

| Command | What it does | Output |
|---|---|---|
| `/explore-idea` | Six forcing questions on a new idea before you build anything | `friday/idea-exploration.md` |
| `/scope-decision` | Forces an expansion, hold, or reduction call on a plan's scope | `friday/scope-decision.md` |
| `/validate-idea` | 7-dimensional validation pass, build, pivot, or kill verdict | `friday/validation.md` |
| `/roadmap` | Turns a goal into a sequenced 90-day roadmap | `friday/roadmap.md` |

### Team and operations

| Command | What it does | Output |
|---|---|---|
| `/teach-team` | Scaffolds an onboarding plan for a team member or contractor | `friday/teaching/<topic>.md` |
| `/sop-builder` | Turns a repeatable process into a documented, followable SOP | `friday/sops/<process-name>.md` |

### Extend

| Command | What it does | Output |
|---|---|---|
| `/new-capability` | Scaffolds a new command from a template, ready for you to fill in | `commands/<name>.md` |

---

## /amplify: the growth diagnostic

`/amplify` is the flagship.

It walks you through eight business vital signs: Leads, Meetings, Sales, Profit, Content, Partnerships, Audience, and Team. Score each from one to ten. Honest scores produce a useful plan. Optimistic scores produce a plan that misses the real gap.

From your scores it detects your business stage: Startup, Growing, Established, or Scaling. It maps you to your priority growth area, which is Revenue, Brand, Audience, or Operations. Then it finds the lowest vital sign in that area. That vital sign is your biggest lever.

It builds a six-step recommendation using the Amplify Pyramid and runs a five-question ethics check on it. Then it suggests three AI tools matched to your experience level: Beginning, Building, or Advanced. The output lands in `friday/growth.md`. Come back in 30 days and check the leading indicators.

The full Amplify method is in the book: https://www.amazon.com/Amplify-Integrating-Intelligence-Humanity-Acceleration/dp/1998756831

---

## Build your own

The built-in commands cover the daily fundamentals. Your workflow will have recurring needs they do not touch.

### Scaffold a new command

Run `/new-capability` in Claude Code. It asks for a name, a one-line purpose, and an output file. It creates `commands/<name>.md` with the correct frontmatter and step structure. Fill in your logic. Copy it to `~/.claude/commands/<name>.md` and run `/<name>` in a new Claude Code session to test it.

### The harness guide

The installer fetches six docs to `./harness/`. Read them in order when you are ready to extend.

| Doc | What it covers |
|---|---|
| `00-how-friday-works.md` | The mental model: commands, brain file, friday/ folder |
| `01-add-a-command.md` | Write your first custom command in under ten minutes |
| `02-add-an-agent.md` | Build a specialist agent for longer autonomous work |
| `03-connect-your-own-tools.md` | Wire your own APIs, CLIs, and MCP servers |
| `04-the-friday-folder.md` | How the config grows and what to keep clean |
| `05-the-amplify-logic.md` | The Amplify method explained, for adapting the diagnostic |

### Connecting your tools

Foundation ships with no external connections. That is intentional. You wire what you need.

Three patterns work well:

**Read a file.** Your tool exports a CSV or JSON file. Your command reads it. No API key needed.

**Add an MCP server.** Claude Code supports Model Context Protocol servers. Official ones exist for GitHub, Slack, Notion, Google Calendar, Supabase, and more. Configure them in `~/.claude/claude.json` with your own keys. Your credentials stay on your machine.

**Shell commands in an agent.** Give an agent the `Bash` tool and it can call any CLI: the GitHub CLI, the Notion CLI, curl, any script you have written.

Never put API keys in command or agent files. They are tracked by git.

---

## What Foundation includes, and what comes next

**Friday Foundation (here):** free, open-source, 22 commands. Bring your own Claude Code and your own API keys. Build from the skeleton up.

**The Amplify book:** the full methodology behind `/amplify`. All six Pyramid steps, the SymbioEthical framework, and case studies from founders who ran it. https://www.amazon.com/Amplify-Integrating-Intelligence-Humanity-Acceleration/dp/1998756831

**Friday Mk I (customers):** the Chief of Staff shell. Nine specialists wired together, connected to your inbox, calendar, tasks, and transcript archive, running before you wake up. friday.amplifyais.com

**Friday Mk V (fans):** the full Friday, with the intelligence layer included. friday.amplifyais.com

Foundation gives you the shape. The paid product is Friday running while you sleep.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| A command does not appear in Claude Code | Not installed to `~/.claude/commands/` | Run the installer again, or copy the file manually |
| Output is not in your voice | `friday/voice.md` is missing | Run `/voice-installer` first |
| `/brief` asks for nine decisions every time | `friday/nine-decisions.md` does not exist | Run `/brief` once to create it, or write the file manually |
| A command writes nothing to disk | Write permission error | Check that you can create files in the current directory |
| `/amplify` results feel off | Scores were optimistic | Re-run with honest scores. The diagnostic is only as useful as the input |
| A custom command is not running | File is in `commands/` but not in `~/.claude/commands/` | Run: `cp commands/<name>.md ~/.claude/commands/<name>.md` |
| Not sure what to run next | New to the setup | Start with `/voice-installer`, then `/brief` |

---

## Going deeper

- **The harness guide (six docs):** `./harness/` in your project directory after install
- **Any command in detail:** open `~/.claude/commands/<name>.md`
- **In a Claude Code session:** type the command name and ask Claude what it does

---

Built by Amplify AI® - amplifyais.com
