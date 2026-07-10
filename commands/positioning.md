---
name: positioning
description: Build a clear positioning statement from category, target customer, key benefit, and difference from alternatives. Writes friday/positioning.md. Reads friday/voice.md if present and writes in your voice.
---
# /positioning

Positioning is the short answer to "why this, for whom, instead of what they already do?" This command turns scattered founder thinking into one clear line, then saves the thinking behind it so the next page, pitch, or offer has a spine.

You, Claude, run the whole flow below in order, using your own file tools. There is no module to import and nothing to install.

## Step 1: Read the founder's voice profile (if it exists)

Check whether `friday/voice.md` exists in the current directory. If it does, read it and write all output in the founder's voice.

If `friday/voice.md` does not exist, write in a direct, plain style: short sentences, active voice, no hedging.

If the voice profile lists banned words, do not use any of them in the output file or the final message.

## Step 2: Get the raw positioning inputs

Ask the founder these questions one at a time. Wait for an answer before moving to the next.

**Category**

> What category should this live in? Name the thing a buyer already understands, like "project management tool", "AI sales assistant", "fractional CFO", or "founder coaching program."

**Target customer**

> Who is this specifically for? Name the buyer and the situation they are in. Do not settle for "everyone" or "small businesses" if there is a sharper group.

**Pain or job**

> What problem are they trying to solve, or what job are they hiring this to do?

**Key benefit**

> What is the most important result they get if this works?

**Difference from alternatives**

> What do they use today instead, and what makes this meaningfully different from that?

## Step 3: Tighten vague answers

Review the answers before writing. If any answer is vague, ask one follow-up question for that answer before proceeding.

Use these checks:

- Category is vague if it is a slogan instead of a known market or workflow.
- Target customer is vague if it could describe almost any buyer.
- Pain or job is vague if it names a feature instead of a real problem.
- Key benefit is vague if it is only "better", "faster", "easier", or "AI-powered" without a concrete outcome.
- Difference is vague if it only says "higher quality", "more efficient", or "unique" without naming the alternative and the contrast.

Stop after one follow-up per vague answer. Do not turn this into an endless workshop.

## Step 4: Write the positioning draft

Create `friday/` if it does not exist. Write the result to `friday/positioning.md`. If the file already exists, overwrite it with this run's positioning draft.

Use this structure:

```
# Positioning: <YYYY-MM-DD>

## One-line positioning

For <target customer>, <name or offer> is a <category> that helps them <key benefit> by <difference from alternatives>.

## Inputs

**Category:** <category>

**Target customer:** <target customer>

**Pain or job:** <pain or job>

**Key benefit:** <key benefit>

**Alternative:** <what they use today>

**Difference:** <what makes this different>

## Why this should work

<Two or three short sentences explaining why the position is believable and where it is sharpest.>

## Where it is still weak

<One honest sentence naming the weakest part of the current position.>

## Next move

<One concrete next action: a homepage headline to test, a landing-page section to rewrite, a sales-call question to ask, or a proof point to collect.>
```

If the founder did not give a product or offer name, use "this offer" in the one-line positioning instead of inventing a name.

Write in the founder's voice. Keep the one-line positioning to one sentence. Make the weak point useful, not insulting.

After writing, print:

> Positioning saved to `friday/positioning.md`. Your config is growing.

Then add one next action from the `Next move` section.

## What this builds toward

Positioning is a reusable decision. Once it is saved in `friday/positioning.md`, the founder can use it to sharpen a homepage, sales deck, cold email, product page, or offer review without re-deciding the basics every time.

The full stack is Friday at friday.amplifyais.com. Nine specialists, running against your real inbox, calendar, and tasks every morning before you are up.

---

Built by Amplify AI at amplifyais.com
