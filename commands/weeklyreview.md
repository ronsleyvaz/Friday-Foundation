---
name: weeklyreview
description: Run a structured weekly review. Walk through wins, misses, and what carries forward. Produces one clear priority for the week ahead. Writes to friday/review.md. Reads friday/voice.md if present and writes in your voice.
---
# /weeklyreview

A week without a review is a week that does not compound. This command walks you through your wins, misses, and carry-forwards, then names one priority for the week ahead. Writes in your voice. Saves to disk.

You, Claude, run the whole flow below in order, using your own file tools. There is no module to import and nothing to install.

## Step 1: Read the founder's voice profile (if it exists)

Check whether `friday/voice.md` exists in the current directory. If it does, read it.

From the profile, note:
- Their tone and rhythm.
- Their signature phrases.
- Their banned words list. You must not use any word on that list in any output from this command.

If `friday/voice.md` does not exist, write in a neutral, direct style: short sentences, no hedging, active voice.

## Step 2: Walk through the week

Ask the founder three questions, one at a time. Wait for each answer before asking the next.

**Question 1:** What went well this week? Name the wins, big or small. Ship, decision made, call that landed. Whatever moved the needle.

**Question 2:** What did not go as planned? Name the misses without softening them. A miss is a miss. Note it.

**Question 3:** What carries forward into next week? Anything left open, anything you said yes to, anything you need to pick back up.

Wait for all three answers before proceeding.

## Step 3: Produce the weekly review

Write a structured review in the founder's voice.

Format:

```
# Weekly Review: <YYYY-MM-DD>

## Wins

<List the wins. One line each. Concrete. Not vague. If they shipped something, name it. If they closed a deal, name the number.>

## Misses

<List the misses. One line each. Plain language. No excuses in the review itself. The miss is a fact.>

## Carry-forwards

<List what is moving into next week. Each item gets one line. If an item has been carrying forward for more than two weeks, note it plainly.>

## One priority for next week

<Name the single most important thing. Not the most urgent. The most consequential. One sentence. No hedging.>
```

Write the full review in the founder's voice. If their profile lists banned words, do not use any of them.

## Step 4: Write the review to disk

Write the full review to `friday/review.md` in the current directory. If the file already exists, append this review below the previous one with a separator. Create the file if it does not exist. Create the `friday/` folder if it does not exist.

Use this format when appending to an existing file:

```
---

<the full review from Step 3>
```

After writing, print:

- Review written to `friday/review.md`.

## What this does not do

This command does not connect to any live system. It does not pull from your task manager, your calendar, or your inbox.

You bring the raw material. The review gives it structure.

The full stack is Friday at friday.amplifyais.com. Your completed tasks, meetings, and decisions pulled automatically. The review is ready when you sit down.

---

Built by Amplify AI at amplifyais.com
