---
name: teach-team
description: Scaffold a teaching plan for onboarding a team member or contractor to a process. Asks what the learner already knows, what the goal is, and what the first checkpoint looks like, then writes a progressive lesson sequence. Writes friday/teaching/<topic>.md. Reads friday/voice.md if present and writes in your voice.
---
# /teach-team

You know how to do this. The problem is getting someone else to know it too, without re-explaining it from scratch every time you hire. This command turns what's in your head into a teaching plan you can hand to a new team member or contractor, broken into a sequence they can actually follow.

This is different from `/meetingprep`. `/meetingprep` gets you ready for a conversation. `/teach-team` builds something durable: a reusable onboarding doc for someone else to learn from, on their own, more than once.

You, Claude, run the whole flow below in order, using your own file tools. There is no module to import and nothing to install.

## Step 1: Read the founder's voice profile (if it exists)

Check whether `friday/voice.md` exists in the current directory. If it does, read it and write all output in the founder's voice.

If `friday/voice.md` does not exist, write in a direct, plain style: short sentences, active voice, no hedging.

## Step 2: Name the process and the learner

Ask the founder:

> What process or skill do you want to teach? Be specific: not "sales" but "how I qualify inbound leads before a call." And who's learning it: a new hire, a contractor, a specific role?

Wait for their answer before proceeding.

## Step 3: Find the starting point

Ask:

> What does this person already know, coming in? Assume nothing they haven't actually demonstrated. If they're brand new to the role, say so plainly.

Wait for their answer. This sets the floor: the plan should not waste their time re-teaching what they already have, and should not assume ground they haven't covered.

## Step 4: Name the goal

Ask:

> What should this person be able to do on their own, without you, once this teaching is done? Name the specific capability, not a vague sense of "getting up to speed."

Wait for their answer. If the answer is vague ("understand the process"), push once: "Understanding isn't observable. What would you see them do, unsupervised, that proves they've got it?"

## Step 5: Name the first checkpoint

Ask:

> What's the very first thing you'll check, to know whether this is landing? Not the final test, the first small signal.

Wait for their answer.

## Step 6: Build the lesson sequence

Using the starting point, the goal, and the first checkpoint, break the teaching into a progressive sequence of lessons. Each lesson should:

- Teach one thing, not several.
- Match the learner's current level: not too basic for what they already know, not so advanced it assumes ground they haven't covered yet.
- End with a way to check whether it landed, before moving to the next lesson.
- Build toward the stated goal, in order, so lesson three depends on what lesson one and two actually taught.

Aim for the shortest sequence that gets someone from the stated starting point to the stated goal. Three to six lessons is typical. Do not pad the sequence with extra lessons that do not move the learner closer to the goal.

For each lesson, write:
- What they learn in this lesson, in one sentence.
- How they practice it: a real task they do, not just something they read.
- The checkpoint: how you or someone else will know this lesson landed, before moving to the next one.

## Step 7: Write the teaching plan

Derive a short kebab-case slug from the process name (for example, "how I qualify inbound leads" becomes "qualifying-inbound-leads"). Write the result to `friday/teaching/<slug>.md`. Create the `friday/teaching/` folder if it does not exist.

Use this structure:

```
# Teaching Plan: <process or skill name>

For: <who's learning this>

## Why this matters

<One or two sentences on why this person needs this, tied to their role.>

## Starting point

<What the learner already knows coming in.>

## Goal

<What the learner should be able to do on their own once this is done.>

## Lesson sequence

### Lesson 1: <title>

What they learn: <one sentence>
How they practice it: <the real task>
Checkpoint: <how you'll know it landed>

### Lesson 2: <title>

<same structure, repeat for each lesson>

## First checkpoint

<The very first signal from Step 5, restated plainly, so it's easy to find later.>
```

Write in the founder's voice. If their profile lists banned words, do not use any of them.

After writing, print:

> Teaching plan saved to `friday/teaching/<slug>.md`. Your config is growing.

## What this does not do

This command does not track whether the learner actually completes each lesson, does not generate training materials or slides, and does not replace direct feedback from you. It gives you the sequence. Running it with the person is still on you.

## What this builds toward

Every process you teach this way becomes a reusable doc in `friday/teaching/`. The next hire who needs the same thing gets a plan that already exists, instead of you re-explaining it from memory.

The full stack is Friday at friday.amplifyais.com. Nine specialists, running against your real inbox, calendar, and tasks every morning before you are up.

---

Built by Amplify AI at amplifyais.com
