# 04 - The Friday Folder

The `friday/` folder is where everything lands.

Every workflow command writes to it. Every file in it is yours to read, edit, and share. As you run more capabilities, the folder grows into a config that represents how you work. `/new-capability` is the developer-tool exception: it scaffolds `commands/<name>.md` and may create `docs/skill-writing-playbook.md` on its first run.

---

## What lives here

| File | Created by | What it holds |
|---|---|---|
| `friday/voice.md` | `/voice-installer` | Your voice profile: tone, rhythm, signature phrases, banned words |
| `friday/nine-decisions.md` | `/brief` (first run) | The nine recurring decisions your business turns on |
| `friday/morning.md` | `/brief` | Today's priorities, filtered and ordered (overwritten each run) |
| `friday/decisions.md` | `/decide` | Your decision log, one entry per run (append-only) |
| `friday/growth.md` | `/amplify` | Your growth diagnostic: biggest opportunity, plan, metrics |

Custom commands you build will add their own files here.

---

## How the files behave

The files here fall into three groups, and it helps to know which is which:

- **Snapshots, rewritten each run.** `friday/morning.md` (the brief) and `friday/growth.md` (the Amplify diagnostic), along with the other one-off analysis outputs, are regenerated from scratch every time. The latest run replaces the last.
- **Logs, appended to.** `friday/decisions.md`, `friday/meetings.md`, `friday/review.md`, and `friday/shipping-retro.md` grow over time. Each run adds a new entry below the previous ones, so the history stays intact.
- **Config, kept and edited.** `friday/nine-decisions.md` and `friday/voice.md` are written once, then persist. You edit them directly, and commands read them rather than overwrite them.

`friday/learnings.md` sits between the last two: you add to it over time, but `/learnings` also lets you review and prune it, so treat it as a curated log rather than an immutable one.

---

## You own these files

The `friday/` folder is not a database. It is plain text. You can:

- Read any file directly.
- Edit a file to add context (your growth diagnostic is a starting point, not locked).
- Share specific files with a collaborator (your voice profile, your decision log).
- Version-control the folder alongside your project.

---

## The CLAUDE.md brain reads from here

When you add `friday/voice.md` to your `CLAUDE.md` brain file, Claude reads it every session. Your voice profile becomes the baseline for everything Claude writes for you.

To wire it in, add this to `CLAUDE.md`:

```
## Voice

See `friday/voice.md` for the full voice profile. Match the tone, rhythm, and signature phrases. Never use the words on the banned list.
```

---

## Keeping the folder clean

A few rules that keep the folder useful:

- Keep file names consistent. Use kebab-case: `project-name-decisions.md`, not `MyDecisions.md`.
- Do not put credentials or API keys in this folder.
- If you version-control the folder, add `friday/morning.md` to `.gitignore` (it changes daily).

---

## A real friday/ folder looks like this

```
friday/
  voice.md            -- the voice profile, built from your writing samples
  nine-decisions.md   -- the nine forks your business turns on
  morning.md          -- today's brief (regenerated each morning)
  decisions.md        -- log of every decision run through /decide
  growth.md           -- the Amplify diagnostic and 90-day plan
```

That is a functional configuration. Five files. Built by running five commands.

---

Next: [05 - The Amplify Logic](05-the-amplify-logic.md)
