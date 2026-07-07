---
name: positioning
description: Write a one-line positioning statement (category, target customer, key benefit, and what makes it different from alternatives). Writes friday/positioning.md. Reads friday/voice.md if present and writes in your voice.
---
# /positioning

Every founder needs a single sentence that tells the world what they do, who it is for, and why they are different. This command writes that sentence and the short reasoning behind it, so you have something clear to put on a website, a pitch deck, or a cold email.

You, Claude, run the whole flow below in order, using your own file tools. There is no module to import and nothing to install.

## Step 1: Read the founder's voice profile (if it exists)

Check whether `friday/voice.md` exists in the current directory. If it does, read it and write all output in the founder's voice.

If `friday/voice.md` does not exist, write in a direct, plain style: short sentences, active voice, no hedging.

## Step 2: Get the basics

Ask the founder:

> What do you do, who is it for, and what is the one thing you do better than anyone else?

Wait for their answer before proceeding.

## Step 3: Draft the positioning statement

Build a single sentence using this template:

> For [target customer], [product/service] is the [category] that [key benefit]. Unlike [alternatives], it [differentiator].

Make it specific. Avoid vague words like "best," "innovative," or "seamless." If the founder's answer is too broad, push them to narrow it down before writing the final sentence.

## Step 4: Stress test it

Ask these questions and answer them honestly:

- Would a customer who does not know your product understand this sentence on first read?
- Does it say something that a competitor could not also say?
- Is it short enough to remember after hearing it once?

If the answer to any of these is no, revise the sentence.

## Step 5: Write the positioning review

Write the result to `friday/positioning.md`. Create the `friday/` folder if it does not exist. If the file already exists, overwrite it with this run's review.

Use this structure:

```
# Positioning Review: <YYYY-MM-DD>

## The statement

[The one-line positioning statement]

## Why it works

[2-3 sentences explaining why each part of the statement is the way it is, tied to the founder's actual business.]

## Stress test results

- **Understandable:** [yes/no + brief reason]
- **Different:** [yes/no + brief reason]
- **Memorable:** [yes/no + brief reason]

## If you had to change one thing

[One concrete suggestion to make the statement stronger, if applicable. If it is already strong, say so.]
```

Write in the founder's voice. If their profile lists banned words, do not use any of them.

After writing, print:

> Positioning statement saved to `friday/positioning.md`. Your config is growing.

## What this builds toward

A clear positioning statement is the foundation for every piece of external writing: website copy, pitch decks, cold emails, product descriptions. `friday/positioning.md` is the version you check every time you write something new, so it stays consistent.

The full stack is Friday at friday.amplifyais.com. Nine specialists, running against your real inbox, calendar, and tasks every morning before you are up.

---

Built by Amplify AI at amplifyais.com
