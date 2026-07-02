---
name: scope-decision
description: Challenge your plan's scope and force an Expansion, Selective-Expansion, Hold, or Reduction call. Reads friday/idea-exploration.md if present, standalone otherwise. Writes friday/scope-decision.md. Reads friday/voice.md if present and writes in your voice.
---
# /scope-decision

Ambition drifts quietly. A plan gets a little bigger every week without anyone deciding it should. This command forces an explicit call: are you going bigger, holding the line, or cutting down? No drifting, no defaults you didn't choose.

You, Claude, run the whole flow below in order, using your own file tools. There is no module to import and nothing to install.

## Step 1: Read the founder's voice profile (if it exists)

Check whether `friday/voice.md` exists in the current directory. If it does, read it and write all output in the founder's voice.

If `friday/voice.md` does not exist, write in a direct, plain style: short sentences, active voice, no hedging.

## Step 2: Get the plan

Check whether `friday/idea-exploration.md` exists in the current directory.

If it exists, read it and tell the founder:

> Found `friday/idea-exploration.md`. Using that as the plan under review.

If it does not exist, ask directly:

> What's the plan you want to scope-check? Give me a couple of sentences on what you're building or planning to do, and what you're trying to achieve with it.

Wait for their answer before proceeding. This command works standalone: you do not need to have run `/explore-idea` first.

## Step 3: Present the four scope modes

Tell the founder:

> Before we go further, pick a mode. This decides how the rest of the session runs, so be honest about which one you actually need right now.
>
> **A) Expansion.** The plan is fine, but you suspect it could be bigger. You want the ambitious version put in front of you, one idea at a time, so you can decide what's worth adding.
>
> **B) Selective Expansion.** The current scope stays the baseline, but you want to see what else is possible before you commit. You'll cherry-pick from a list of expansion ideas rather than accepting or rejecting the whole thing at once.
>
> **C) Hold.** The scope is right. You want it stress-tested, not grown. Find the weak points, the things you haven't thought through, the risks. No new scope added.
>
> **D) Reduction.** The plan has gotten too big, or you're not sure it's the right plan at all. You want the ruthless minimum version: what's the smallest thing that actually delivers the outcome you're after?

Wait for their choice (A, B, C, or D) before continuing.

## Step 4: Run the mode

Once a mode is chosen, commit to it fully for the rest of this session. Do not drift into a different posture halfway through.

**If Expansion (A):**

Describe the bigger version of this plan. Ask: what would this look like if you had twice the resources and permission to think bigger? Name three to five concrete additions or changes that would make the outcome meaningfully better, not just bigger. For each one, state the upside in one sentence and a rough sense of effort (small, medium, large). Present them one at a time and ask the founder to accept, defer, or skip each one before moving to the next. Do not batch them into one list and ask for a blanket yes.

**If Selective Expansion (B):**

First, name the minimum version of the current plan: what's actually required to hit the stated goal, with everything else stripped away. State that in two or three sentences.

Then list three to five expansion ideas as candidates, the same way as Expansion mode, but present them neutrally: state the upside and the effort for each, without pushing the founder toward yes. Ask the founder to accept, defer, or skip each one individually.

**If Hold (C):**

Do not propose any new scope. Instead, stress-test what's already there. Ask yourself, and then tell the founder:

- What's the weakest assumption in this plan? What happens if it's wrong?
- What's the most likely way this fails? What would you see first if it started going wrong?
- What has this founder not thought about yet, that they'll wish they had in three months?

Name at least three concrete risks or gaps, each with one sentence on what to do about it.

**If Reduction (D):**

Find the ruthless minimum. Ask: what is the smallest version of this that actually delivers the core outcome, with nothing else attached? Name what gets cut and why each cut is safe. Be specific, not vague. "Cut the extra features" is not an answer. "Cut the team dashboard, it doesn't affect whether the core offer sells" is.

## Step 5: State the call

After running the chosen mode, write one paragraph naming the final scope decision: what's in, what's out, and why this serves the founder's stated goal better than the alternative modes would have. This is the call, not a summary of options. Make it directly.

## Step 6: Write the scope decision

Write the result to `friday/scope-decision.md`. Create the `friday/` folder if it does not exist. If the file already exists, overwrite it with this run's decision.

Use this structure:

```
# Scope Decision: <YYYY-MM-DD>

## The plan

<The plan under review, from idea-exploration.md or from the founder directly.>

## Mode chosen

<Expansion / Selective Expansion / Hold / Reduction>, and one sentence on why the founder picked it.

## What we found

<The output of Step 4: the expansion candidates and their accept/defer/skip decisions, the risks surfaced in Hold mode, or the cuts made in Reduction mode.>

## The call

<The final paragraph from Step 5: what's in scope, what's out, and why.>
```

Write in the founder's voice. If their profile lists banned words, do not use any of them.

After writing, print:

> Scope decision saved to `friday/scope-decision.md`. Your config is growing.

## What this builds toward

Scope drifts unless something forces the decision. `friday/scope-decision.md` is the record of the call you made and why, so three months from now you can check whether you held the line or drifted again.

The full stack is Friday at friday.amplifyais.com. Nine specialists, running against your real inbox, calendar, and tasks every morning before you are up.

---

Built by Amplify AI at amplifyais.com
