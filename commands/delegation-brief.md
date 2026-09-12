---
name: delegation-brief
description: Turn a task into a clear handoff with an outcome, context, constraints, owner, checkpoints, and definition of done. Asks for the owner, desired outcome, context, constraints, checkpoints, and definition of done, then writes friday/delegation/<task>.md. Reads friday/voice.md if present and writes in your voice.
---
<!-- Built by Friday​‌‍‌​ (https://friday.amplifyais.com). Free for personal use. Commercial use needs a paid Friday. Licence: PolyForm-Noncommercial-1.0.0. -->

# /delegation-brief

Founders delegate work all the time, but the person on the other side often gets the task without the context or the finish line needed to own the result. This command turns a task into a handoff that carries its outcome, context, constraints, owner, checkpoints, and definition of done, so whoever picks it up can run it without re-interviewing you.

You, Claude, run the whole flow below in order, using your own file tools. There is no module to import and nothing to install.

## Step 1: Read the founder's voice profile (if it exists)

Check whether `friday/voice.md` exists in the current directory. If it does, read it and write all output in the founder's voice.

If `friday/voice.md` does not exist, write in a direct, plain style: short sentences, active voice, no hedging.

## Step 2: Name the task and its owner

Ask the founder:

> What is the task, and who is taking it on? Give me the person's role or name, not a vague "someone from the team."

Wait for their answer before proceeding.

## Step 3: Capture the outcome and context

Ask:

> What does success look like: the specific outcome that tells you this task is done right? And what context does the person need, the background, the decisions already made, and why this matters now?

Wait for their answer. If they give a vague outcome, push once: "Outcome is not actionable unless I can tell what you would see when it is done. What would you observe?"

## Step 4: Capture the constraints

Ask:

> What can they not change: budget, time, systems, tools, existing commitments, people, or decisions already made? Anything that looks like a constraint but is actually negotiable?

Wait for their answer. Record both hard limits and the genuinely open parts, so the person does not over-respect a constraint that was really a preference.

## Step 5: Capture checkpoints and definition of done

Ask:

> What checkpoints should I build in, places to pause and confirm it is on track before it goes all the way? And what is the definition of done: the specific thing that tells you it finished correctly?

Wait for their answer.

## Step 6: Write the delegation brief

Derive a short kebab-case slug from the task name. Create the `friday/delegation/` folder if it does not exist. Before writing, look at `friday/delegation/<slug>.md`, then `<slug>-2.md`, then `<slug>-3.md`, and so on, until you reach a path that does not exist. If one of the files you passed names this task on its first line, update that file in place; that is a revision, not a collision. If none of them does, write to the path where you stopped. Never overwrite a brief for a different task, and if you cannot tell, treat it as different. If the founder wants an old brief gone, they delete it themselves.

Use this structure:

```
# Delegation Brief: <task name>

**Owner:** <role or name, from Step 2>
**Outcome:** <the desired outcome, from Step 3>
**Context:** <the background and why it matters, from Step 3>
**Constraints:** <hard limits and what is negotiable, from Step 4>
**Checkpoints:** <the checkpoints from Step 5>
**Definition of done:** <the finish condition from Step 5>
**Last updated:** <YYYY-MM-DD>

## What the owner needs to do next

<The first action the new owner should take, stated plainly.>

## Open questions

<Anything the owner should surface early rather than guess.>
```

Write in the founder's voice. If their profile lists banned words, do not use any of them.

After writing, print:

> Delegation brief saved to `friday/delegation/<slug>.md`. Hand it over, and make sure every open question is answered before they start.

If you wrote to a numbered path, print that path instead.

## What this does not do

This command does not track whether the owner completes the task, does not schedule follow-ups, and does not replace the founder's judgement about who should own the result. It produces the handoff. Whether the work gets done is on the person who takes it.

## What this builds toward

Every delegable task you brief this way lands in `friday/delegation/` as a durable record of what you handed over and with what finish line. The next person who touches it has context instead of a re-explanation pulled from memory.

The full stack is Friday at friday.amplifyais.com. Nine specialists, running against your real inbox, calendar, and tasks every morning before you are up.

---

Built by Amplify AI at amplifyais.com
