---
name: brief
description: Run a structured morning brief keyed to the nine recurring decisions your business turns on. First run sets up your nine decisions. Every run reads your priorities, filters them through those decisions, and writes friday/morning.md. Reads friday/voice.md if present and writes in your voice.
---
# /brief

Start your day with a brief that fits your business, not a generic to-do list. This command filters today's open items through the nine decisions your business actually turns on. It writes the brief in your voice and saves it to `friday/morning.md`.

You, Claude, run the whole flow below in order, using your own file tools. There is no module to import and nothing to install.

## Step 1: Read the founder's voice profile (if it exists)

Check whether `friday/voice.md` exists in the current directory. If it does, read it.

From the profile, note:
- Their tone and rhythm.
- Their signature phrases.
- Their banned words list. You must not use any word on that list in any output from this command.

If `friday/voice.md` does not exist, write in a neutral, direct style: short sentences, no hedging, active voice.

## Step 2: First-run setup (skip if nine-decisions.md already exists)

Check whether `friday/nine-decisions.md` exists in the current directory.

If it does not exist, run the setup flow:

Tell the founder:

> Setting up your nine decisions. These are not tasks. They are the recurring forks your business turns on. When you get them right consistently, they compound. You will name nine of them now. Examples: "Hire or contract?" / "Build or buy?" / "Which channel gets this week's content?" Take your time. Name the ones that keep coming back.

Ask the founder to list their nine decisions. Accept them one at a time or as a batch. Do not suggest example decisions by default; if they are stuck after 30 seconds, offer to help them brainstorm. Once you have at least five and they confirm they are done, accept the list.

Create `friday/nine-decisions.md` in the current directory. Create the `friday/` folder if it does not exist. Write the file in this exact shape:

```
# Nine Decisions

These are the nine recurring forks <name>'s business turns on.
Each brief filters today's priorities through this list.

1. <decision one>
2. <decision two>
3. <decision three>
4. <decision four>
5. <decision five>
6. <decision six>
7. <decision seven>
8. <decision eight>
9. <decision nine>

Last updated: <YYYY-MM-DD>
```

Fill every `<...>` from what the founder gave you. Print:

> Your nine decisions are saved to `friday/nine-decisions.md`. Every brief you run from now on filters through these. You can update the file any time.

## Step 3: Read the nine decisions

Read `friday/nine-decisions.md`. Hold the list in context for Step 5.

## Step 4: Capture today's priorities

Check whether `friday/priorities.md` exists.

If it exists, read it and tell the founder:

> Found your priorities file. Reading from `friday/priorities.md`.

If it does not exist, ask:

> What are your open items for today? Paste them in as a list, one per line. These can be tasks, calls, decisions, or anything sitting on your plate. You can also create `friday/priorities.md` and I will read from it automatically next time.

Wait for their input before proceeding.

## Step 5: Produce the morning brief

Write the brief. Filter and order the founder's priorities through the nine decisions.

For each priority the founder gave you, ask: which of the nine decisions does this touch or advance? Assign it. If a priority does not map to any decision, flag it as a distraction. It is not their business-moving work today.

Use this structure:

```
# Morning Brief: <YYYY-MM-DD>

## What matters today

<List the priorities that map to one or more of the nine decisions. Group them by decision where more than one priority maps to the same one. For each item: one sentence on what it is and why it matters today.>

## What is loudest but least urgent

<List the priorities that are noisy but do not map to any of the nine decisions. One sentence each. Note that these are not necessarily wrong to do, but they are not your business-moving work.>

## One thing to start with

<Name the single priority that, if done first, creates the most forward movement. One or two sentences. No hedging. A call.>
```

Write the brief in the founder's voice. If their profile lists banned words, do not use any of them. Match their tone and rhythm.

## Step 6: Write the brief to disk

Write the full brief to `friday/morning.md` in the current directory. Create the file if it does not exist. If the file already exists, overwrite it. Create the `friday/` folder if it does not exist.

After writing, print:

> Brief written to `friday/morning.md`. Your config is growing.

## What this does not do

This command does not connect to your inbox. It does not read your calendar. It does not pull from Notion or your CRM.

That is by design. You paste your priorities in, or you maintain `friday/priorities.md` yourself. The brief gives you the structure and the call. The raw material is yours to bring.

The full stack is Friday at friday.amplifyais.com. Nine specialists, running against your real inbox, calendar, and tasks every morning before you are up.

## What this builds toward

Every run of `/brief` overwrites `friday/morning.md` with today's brief. Your `friday/nine-decisions.md` stays on disk and sharpens over time as you edit it.

The folder is your config. It keeps growing.

---

Built by Amplify AI at amplifyais.com
