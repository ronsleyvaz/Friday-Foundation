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

## The folder is append-friendly

Most commands append to existing files rather than overwrite them. `friday/decisions.md` grows with every decision you run. `friday/voice.md` gets updated when you re-run `/voice-installer`.

The exception is `friday/morning.md` -- the brief overwrites each day, so it always shows today's priorities.

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
