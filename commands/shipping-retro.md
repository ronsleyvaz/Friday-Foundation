---
name: shipping-retro
description: A weekly reflection built from your real git history. Reads recent commits, asks what shipped, what hurt, and what carries forward. Writes friday/shipping-retro.md. Reads friday/voice.md if present and writes in your voice.
---
# /shipping-retro

`/weeklyreview` covers your whole week. This command is narrower: it looks at what you actually shipped in code, using your real commit history as the anchor, then asks what worked and what carried a cost. Ships standalone rather than folding into `/weeklyreview`, because not every founder using Friday Foundation ships code every week, and this command should stay skippable for the weeks that don't apply.

You, Claude, run the whole flow below in order, using your own file tools. There is no module to import and nothing to install.

## Step 1: Read the founder's voice profile (if it exists)

Check whether `friday/voice.md` exists in the current directory. If it does, read it and write all output in the founder's voice.

If `friday/voice.md` does not exist, write in a direct, plain style: short sentences, active voice, no hedging.

## Step 2: Check for a git repo and read recent history

Check whether the current directory is inside a git repository:

```bash
git rev-parse --is-inside-work-tree 2>/dev/null
```

**If it is a git repo:** run this to get the last 7 days of commits:

```bash
git log --since="7 days ago" --pretty=format:"%h %ad %s" --date=short
```

If that returns commits, hold them in context for Step 3. If it returns nothing (no commits in the last 7 days), tell the founder:

> No commits in the last 7 days. We'll still run the reflection, just without commit history to anchor it.

Then proceed to Step 3 without commit data.

**If it is not a git repo:** tell the founder:

> This isn't a git repo, so there's no commit history to read. We'll run the reflection questions directly instead.

Then proceed to Step 3 without commit data. Do not error or stop.

## Step 3: Walk through the reflection

If you have commit history, show it to the founder first:

> Here's what shipped in the last 7 days:
>
> <list each commit as one line: date, short hash, message>
>
> Let's reflect on it.

Ask three questions, one at a time. Wait for each answer before asking the next.

**Question 1:** Looking at what shipped, what actually moved the business forward? Not everything that shipped matters equally, name what mattered.

**Question 2:** What hurt? Name anything that took longer than it should have, broke something, or you're not happy with the way it came out.

**Question 3:** What carries forward into next week? Anything half-shipped, anything you learned that changes the plan, anything you're picking back up.

If there was no commit history, ask the same three questions, but reframe Question 1 as: "What did you actually get done this week, code or otherwise, that moved the business forward?"

## Step 4: Write the retro

Write the result to `friday/shipping-retro.md`. Create the `friday/` folder if it does not exist. If the file already exists, append this run below the previous one with a separator, the same way `/weeklyreview` appends to `friday/review.md`.

Use this structure:

```
# Shipping Retro: <YYYY-MM-DD>

## What shipped

<The commit list from Step 2, if there was one. If there wasn't, write "No commits in the last 7 days.">

## What mattered

<The founder's answer to Question 1.>

## What hurt

<The founder's answer to Question 2. Plain language, no softening. A miss is a miss.>

## What carries forward

<The founder's answer to Question 3.>
```

Write in the founder's voice. If their profile lists banned words, do not use any of them.

Use this format when appending to an existing file:

```
---

<the full retro from this run>
```

After writing, print:

> Shipping retro saved to `friday/shipping-retro.md`. Your config is growing.

## What this does not do

This command does not track code quality metrics, does not break work down per contributor, and does not maintain analytics across runs. It reads your commit history once, asks three questions, and writes the answer down. If you want a fuller weekly reflection that isn't code-specific, run `/weeklyreview` instead.

## What this builds toward

Run weekly, `friday/shipping-retro.md` becomes a record of what actually shipped versus what you meant to ship, and what kept carrying forward. That gap is worth seeing plainly.

The full stack is Friday at friday.amplifyais.com. Nine specialists, running against your real inbox, calendar, and tasks every morning before you are up.

---

Built by Amplify AI at amplifyais.com
