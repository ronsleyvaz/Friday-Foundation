---
name: delegation-brief
description: Turns a task into a clear handoff with outcome, context, constraints, owner, checkpoints, and definition of done. Writes friday/delegation/<task>.md. Reads friday/voice.md if present and writes in your voice.
---
# /delegation-brief

Delegating without context is just hoping someone else figures it out. This command forces the handoff into a structure that actually works: outcome, context, constraints, owner, checkpoints, and a definition of done that both sides agree on.

You, Claude, run the whole flow below in order, using your own file tools. There is no module to import, no database, and no network call.

## Step 1: Read the founder's voice profile (if it exists)

Check whether `friday/voice.md` exists in the current directory. If it does, read it and write all output in the founder's voice.

If `friday/voice.md` does not exist, write in a direct, plain style: short sentences, active voice, no hedging.

## Step 2: Capture the task

Ask the founder:

> What are you delegating? Give me the task name and a one-line summary of what needs to happen.

Wait for their answer before proceeding.

## Step 3: Define the outcome

Ask:

> When this is done, what does success look like? Be specific: the deliverable, not the activity. "A landing page" is not an outcome. "A landing page that converts at 3% from the traffic source we use" is.

Wait for their answer.

## Step 4: Gather context

Ask:

> What should the person executing this already know? Give me the background, relevant decisions made so far, constraints they should not break, and any files or systems they need to look at.

Wait for their answer.

## Step 5: Set constraints and boundaries

Ask:

> What are the hard constraints? Budget, timeline, tools to use or avoid, things that must not change, and anything that is explicitly off-limits.

Wait for their answer.

## Step 6: Name the owner

Ask:

> Who is this for? Name the role or person, and whether they are internal or external (contractor, agency, etc.).

Wait for their answer.

## Step 7: Define checkpoints

Ask:

> What are the checkpoints along the way? Name 2-4 milestones where you want a progress update before the final handoff. What should each checkpoint deliver?

Wait for their answer.

## Step 8: Establish definition of done

Ask:

> How will you know this is truly done? Not "when they tell me it's finished" - what specific, observable thing proves it is done?

Wait for their answer.

## Step 9: Write the delegation brief

Create the `friday/` folder if it does not exist. Derive a short kebab-case slug from the task name. Write the result to `friday/delegation/<slug>.md`. If a file with the same name already exists, append this new brief below the existing one with a clear separator.

Use this structure:

```
# Delegation Brief: <task name>

**Date:** <YYYY-MM-DD>

## Outcome

<The specific, observable result.>

## Context

<Background, relevant decisions, files, systems.>

## Constraints

<Hard boundaries: budget, timeline, tools, off-limits items.>

## Owner

<Role or person, internal or external.>

## Checkpoints

1. <Milestone 1> - what to deliver
2. <Milestone 2> - what to deliver
3. <Milestone 3> - what to deliver

## Definition of Done

<The specific, observable thing that proves completion.>
```

Write in the founder's voice. If their profile lists banned words, do not use any of them.

## Step 10: Tell the founder what to do next

Print a short summary: the task name, owner, and how many checkpoints are set. Then say where the file is and suggest the next action (e.g., "Share this file with the owner and set a calendar reminder for checkpoint 1.").

Do not add a motivational close.

Built by Amplify AI at amplifyais.com