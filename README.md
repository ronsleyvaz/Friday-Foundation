# Friday Foundation

[![CI](https://github.com/ronsleyvaz/Friday-Foundation/actions/workflows/ci.yml/badge.svg)](https://github.com/ronsleyvaz/Friday-Foundation/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Build your own AI Chief of Staff inside Claude Code. 22 commands, a growth diagnostic, and a harness to extend it to your workflow.

Free to install. No separate Foundation account or backend. Claude Code supplies the AI and has its own account and network requirements. Foundation keeps its durable outputs as local files in your project.

![Installing Friday Foundation: one curl command, then running your first command inside Claude Code](docs/assets/install-demo.gif)

---

## Install in one line

First, `cd` into your project directory. The commands install globally, but your `CLAUDE.md` brain file and the harness guide land wherever you run this:

```
curl -fsSL https://raw.githubusercontent.com/ronsleyvaz/Friday-Foundation/release/install.sh | bash
```

You need Claude Code installed first. Get it at https://docs.anthropic.com/claude-code

The installer drops the commands into `~/.claude/commands/`, creates a `CLAUDE.md` in your current directory from the template (any existing one is left untouched), fetches the harness guide, and tells you what to do next.

---

## Start here

Open Claude Code in your project directory. You have two good first moves.

Your fastest win, no setup required:

```
/amplify
```

Five minutes. It runs the growth diagnostic on your numbers and writes a 90-day plan to `friday/growth.md`.

Optional, but it sharpens every other command:

```
/voice-installer
```

It reads your writing samples, builds a voice profile, and writes it to `friday/voice.md`. Every command that runs after reads that profile and writes in your voice instead of a generic AI voice. Skipping it is safe: commands fall back to a neutral, direct style until you run it.

Want the full walkthrough first? The manual covers every command, the `friday/` folder, and how to extend Foundation: [`docs/foundation-manual.md`](docs/foundation-manual.md).

---

## What each command does

| Command | What it does | Output |
|---|---|---|
| `/voice-installer` | Builds your voice profile from writing samples | `friday/voice.md` |
| `/brief` | Filters today's priorities through your nine decisions | `friday/morning.md` |
| `/decide` | Runs the 1-3-1 protocol: one problem, three options, one pick | `friday/decisions.md` |
| `/meetingprep` | Prepares you for any meeting in five minutes | `friday/meetings.md` |
| `/weeklyreview` | Structured weekly review and one clear priority | `friday/review.md` |
| `/amplify` | Runs the Amplify growth diagnostic on your numbers | `friday/growth.md` |
| `/new-capability` | Scaffolds a new command from a template | `commands/<name>.md` |
| `/explore-idea` | Six forcing questions on a new idea before you build anything | `friday/idea-exploration.md` |
| `/scope-decision` | Forces an expansion, hold, or reduction call on your plan's scope | `friday/scope-decision.md` |
| `/learnings` | Reviews, searches, and prunes what Friday has learned about your business | `friday/learnings.md` |
| `/shipping-retro` | Weekly reflection built from your real git commit history | `friday/shipping-retro.md` |
| `/changelog` | Turns git history into customer-facing release notes | `friday/changelog.md` |
| `/teach-team` | Scaffolds an onboarding plan for a team member or contractor | `friday/teaching/<topic>.md` |
| `/validate-idea` | 7-dimensional validation pass, build, pivot, or kill verdict | `friday/validation.md` |
| `/roadmap` | Turns a goal into a sequenced 90-day roadmap | `friday/roadmap.md` |
| `/go-to-market` | Phased launch plan: pre-launch, launch week, 30/60/90 days | `friday/gtm-plan.md` |
| `/pricing-strategy` | Value-based pricing model and tier design with real numbers | `friday/pricing.md` |
| `/offer-creation` | Value-equation review, finds your offer's weakest lever | `friday/offer.md` |
| `/positioning` | Builds a clear positioning statement and next move | `friday/positioning.md` |
| `/competitive-analysis` | Competitor teardown: comparison matrix plus a SWOT for each competitor | `friday/competitive-analysis.md` |
| `/sop-builder` | Turns a repeatable process into a documented, followable SOP | `friday/sops/<process-name>.md` |
| `/product-hunt-launch` | Product Hunt specific launch runbook, pre-launch through post-launch | `friday/product-hunt-launch.md` |

Workflow commands write to a `friday/` folder in your project directory. That folder is your config, growing over time. `/new-capability` is the developer-tool exception: it scaffolds `commands/<name>.md` and may create `docs/skill-writing-playbook.md` on its first run.

---

## The Amplify growth diagnostic

`/amplify` is the flagship capability.

It walks you through eight business vital signs, detects your growth stage, maps to your priority quadrant (Revenue, Brand, Audience, or Operations), runs an ethics check on the recommendation, and writes a 90-day plan to `friday/growth.md`.

It takes about five minutes. It tells you where to push next and which AI tools to use first, matched to your experience level.

Based on the Amplify AI method. Full breakdown in the book: https://www.amazon.com/Amplify-Integrating-Intelligence-Humanity-Acceleration/dp/1998756831

---

## Install a single command

```
curl -fsSL https://raw.githubusercontent.com/ronsleyvaz/Friday-Foundation/release/install.sh | bash -s -- amplify
```

Replace `amplify` with any command name to install just that one.

---

## Build your own command

Run `/new-capability <name>` in Claude Code. It scaffolds a command file with the right frontmatter and step structure.

For a full walkthrough, read the harness guide (fetched to `./harness/` when you install):

- `harness/00-how-friday-works.md` -- the mental model
- `harness/01-add-a-command.md` -- write your first custom command
- `harness/02-add-an-agent.md` -- build a specialist agent
- `harness/03-connect-your-own-tools.md` -- wire your own APIs and CLIs
- `harness/04-the-friday-folder.md` -- how the config grows
- `harness/05-the-amplify-logic.md` -- the Amplify method explained

---

## The soft ladder

**Friday Foundation (here):** free, open-source, 22 commands, bring your own Claude Code.

**The Amplify book:** the full framework behind the growth diagnostic. Read it for the complete methodology. https://www.amazon.com/Amplify-Integrating-Intelligence-Humanity-Acceleration/dp/1998756831

**Friday (paid):** nine specialists wired together, connected to your inbox, calendar, tasks, and transcript archive, running before you wake up. friday.amplifyais.com

Foundation gives you the shape of Friday. The paid product is Friday running while you sleep.

---

## Licence

Code (everything except the three content-licensed files) is **MIT**. See `LICENSE`.

The Amplify method content -- `commands/amplify.md`, `harness/05-the-amplify-logic.md`, and `docs/why-guides/amplify-why-guide.md` -- is licensed separately under `LICENSE-CONTENT`: free to use and share with attribution, not to resell or rebrand. Those files carry a header pointing to `LICENSE-CONTENT`.

---

## Contributing

Pull requests are open, and the test gate runs on every one, so you get fast feedback before a maintainer ever looks.

New here? The best place to start is a [good first issue](https://github.com/ronsleyvaz/Friday-Foundation/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22). Each one is a self-contained command to build, with the founder problem and the definition of done written out.

You can ship your first command in about ten minutes. `CONTRIBUTING.md` has the step by step, the quality bar, and how to get credit for what you add.

If Foundation is useful to you, star the repo. It is the cheapest way to help more founders find it.

---

## Credits

Twelve commands started as methodology from five open-source projects: gstack,
Matt Pocock's skills repo, and three founder-focused skill packs. Full list and
sources in `CREDITS.md`.

---

Built by Amplify AI at amplifyais.com
