# Friday Foundation

Build your own AI Chief of Staff inside Claude Code. Nineteen commands, a growth diagnostic, and a harness to extend it to your workflow.

Free and open-source. No account. No server. Everything runs on your machine.

---

## Install in one line

```
curl -fsSL https://raw.githubusercontent.com/ronsleyvaz/Friday-Foundation/release/install.sh | bash
```

You need Claude Code installed first. Get it at https://docs.anthropic.com/claude-code

The installer drops the commands into `~/.claude/commands/`, fetches `CLAUDE.md.template` and the harness guide to your current directory, and tells you what to do next.

---

## Start here

Open Claude Code in your project directory and run:

```
/voice-installer
```

This is the foundation. It reads your writing samples, builds a voice profile, and writes it to `friday/voice.md`. Every command that runs after reads that profile and writes in your voice instead of generic AI voice.

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
| `/teach-team` | Scaffolds an onboarding plan for a team member or contractor | `friday/teaching/<topic>.md` |
| `/validate-idea` | 7-dimensional validation pass, build, pivot, or kill verdict | `friday/validation.md` |
| `/go-to-market` | Phased launch plan: pre-launch, launch week, 30/60/90 days | `friday/gtm-plan.md` |
| `/pricing-strategy` | Value-based pricing model and tier design with real numbers | `friday/pricing.md` |
| `/offer-creation` | Value-equation review, finds your offer's weakest lever | `friday/offer.md` |
| `/competitive-analysis` | Competitor teardown: comparison matrix plus SWOT | `friday/competitive-analysis.md` |
| `/sop-builder` | Turns a repeatable process into a documented, followable SOP | `friday/sops/<process>.md` |
| `/product-hunt-launch` | Product Hunt specific launch runbook, pre-launch through post-launch | `friday/product-hunt-launch.md` |

Each command writes to a `friday/` folder in your project directory. That folder is your config, growing over time.

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

**Friday Foundation (here):** free, open-source, nineteen commands, bring your own Claude Code.

**The Amplify book:** the full framework behind the growth diagnostic. Read it for the complete methodology. https://www.amazon.com/Amplify-Integrating-Intelligence-Humanity-Acceleration/dp/1998756831

**Friday (paid):** nine specialists wired together, connected to your inbox, calendar, tasks, and transcript archive, running before you wake up. friday.amplifyais.com

Foundation gives you the shape of Friday. The paid product is Friday running while you sleep.

---

## Licence

Code (everything except the three content-licensed files) is **MIT**. See `LICENSE`.

The Amplify method content -- `commands/amplify.md`, `harness/05-the-amplify-logic.md`, and `docs/why-guides/amplify-why-guide.md` -- is licensed separately under `LICENSE-CONTENT`: free to use and share with attribution, not to resell or rebrand. Those files carry a header pointing to `LICENSE-CONTENT`.

---

## Contributing

Pull requests are open. See `CONTRIBUTING.md` for what belongs here and the quality bar for commands.

---

## Credits

Twelve commands started as methodology from five open-source projects: gstack,
Matt Pocock's skills repo, and three founder-focused skill packs. Full list and
sources in `CREDITS.md`.

---

Built by Amplify AI at amplifyais.com
