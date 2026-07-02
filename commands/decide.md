---
name: decide
description: Run the 1-3-1 decision protocol on any real decision. One problem statement, three options with trade-offs, one recommendation. Writes a durable decision record to friday/decisions.md. Reads friday/voice.md if present and writes in your voice.
---
# /decide

Make any decision in five minutes. Paste your decision plus two lines of context. This command runs the 1-3-1 protocol live: one problem, three options, one pick. The result is written in your voice and saved to disk so your decision record grows every time.

You, Claude, run the whole flow below in order, using your own file tools. There is no module to import and nothing to install.

## Step 1: Read the founder's voice profile (if it exists)

Check whether `friday/voice.md` exists in the current directory. If it does, read it.

From the profile, note:
- Their tone and rhythm.
- Their signature phrases.
- Their banned words list. You must not use any word on that list in any output from this command.

If `friday/voice.md` does not exist, write in a neutral, direct style: short sentences, no hedging, active voice.

## Step 2: Capture the decision

Ask the founder to paste:
1. The decision they need to make, in one sentence.
2. Two lines of context: what is at stake and what is driving the timing.

Wait for their input before proceeding.

## Step 3: Write the problem statement

State the decision as a clean problem in one paragraph. This is the "1" in 1-3-1.

Format:
```
## The decision

<One paragraph. States what must be decided, what is at stake, and the constraint or deadline driving it. No options yet.>
```

## Step 4: Generate three options

Produce exactly three options. This is the "3" in 1-3-1.

For each option:
- Give it a short label (Option A, Option B, Option C).
- State what it involves in two or three sentences.
- Name one clear upside.
- Name one clear downside or risk.

Format:
```
## Three options

**Option A: <label>**
<What it involves.>
Upside: <one thing.>
Risk: <one thing.>

**Option B: <label>**
<What it involves.>
Upside: <one thing.>
Risk: <one thing.>

**Option C: <label>**
<What it involves.>
Upside: <one thing.>
Risk: <one thing.>
```

## Step 5: Deliver one recommendation

Pick the option you would back. This is the final "1" in 1-3-1.

State which option you recommend and why in two or three sentences. Name why the other two did not make the cut.

Format:
```
## Recommendation

Go with Option <X>.

<Why this one. Two or three sentences. Concrete reasoning, not hedging.>

Why not Option <Y>: <one sentence.>
Why not Option <Z>: <one sentence.>
```

Write the full output (problem statement, three options, recommendation) in the founder's voice. If their profile lists banned words, do not use any of them. Match their tone and rhythm as described in the profile.

## Step 6: Append the decision record

Append the full output to `friday/decisions.md` in the current directory. Create the file if it does not exist. Create the `friday/` folder if it does not exist.

Use this exact format when appending:

```
---

## Decision: <date in YYYY-MM-DD> - <one-line summary of the decision>

<the full output from Steps 3, 4, and 5>
```

After writing, print this line:

- Decision saved to `friday/decisions.md`. Your config is growing.

## What this builds toward

Every run of `/decide` appends one entry to `friday/decisions.md`. That file is your config growing on disk.

The full stack, nine specialists wired to your inbox, calendar, and transcript archive, is Friday at friday.amplifyais.com.

---

Built by Amplify AI at amplifyais.com

<!-- golden-test-throwaway: em dash fixed, ready for CI to go green -->
This line no longer has an em dash, on purpose.
