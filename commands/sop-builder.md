---
name: sop-builder
description: Turn a process you do repeatedly into a documented SOP you can hand off. Asks for the process name, walks step capture, writes friday/sops/<process-name>.md. Reads friday/voice.md if present and writes in your voice.
---
<!-- Built by Friday​‌‍‌​ (https://friday.amplifyais.com). Free for personal use. Commercial use needs a paid Friday. Licence: PolyForm-Noncommercial-1.0.0. -->

# /sop-builder

If a process only lives in your head, you're the bottleneck, and you can't take a day off without something breaking. This command turns a repeatable process into a documented SOP someone who's never done it before could actually follow.

You, Claude, run the whole flow below in order, using your own file tools. There is no module to import and nothing to install.

## Step 1: Read the founder's voice profile (if it exists)

Check whether `friday/voice.md` exists in the current directory. If it does, read it and write all output in the founder's voice.

If `friday/voice.md` does not exist, write in a direct, plain style: short sentences, active voice, no hedging.

## Step 2: Identify the process

Ask the founder:

> What process do you want to document? Give me the name, who currently does it (the role, not necessarily a specific name), how often it happens, and what triggers it, a customer request, a schedule, an event.

Wait for their answer before proceeding. Also ask:

> What does "done" look like for this process, the specific thing that tells you it's finished correctly?

Wait for their answer.

## Step 3: Extract the steps

Walk through the process step by step. Ask:

> Walk me through it from the very start. What happens first?

After each step they describe, ask "then what?" until they reach the end. For each step, also ask:

- What could go wrong at this step?
- Is there a decision point here, a fork where the next action depends on something? ("If X, do this. If not, do that.")
- What tool, login, or system is used at this step?
- Roughly how long does this step take?

Keep going until the process is fully captured, start to finish. Do not stop at a summary level, every step should be specific enough that someone who has never done this could follow it without guessing.

## Step 4: Add the why

For any step that isn't obviously self-explanatory, ask the founder why it matters, not just what to do. A step without its reason gets skipped or done wrong by someone who doesn't understand the stakes.

Also ask:

> Are there common mistakes people make on this process? Anything you've had to correct before?

## Step 5: Review with the founder

Read the captured process back to the founder in summary form and ask:

> Does this match how you actually do it? Any edge cases I'm missing?

Adjust based on their answer before writing the final version.

## Step 6: Write the SOP

Derive a short kebab-case slug from the process name. Write the result to `friday/sops/<slug>.md`. Create the `friday/sops/` folder if it does not exist.

Use this structure:

```
# <Process Name>: Standard Operating Procedure

**Owner:** <role, from Step 2>
**Frequency:** <how often, from Step 2>
**Trigger:** <what starts this process>
**Done means:** <the specific finish condition from Step 2>
**Last updated:** <YYYY-MM-DD>

## Steps

### 1. <Step name>

**Action:** <what to do>
**Tool:** <system or app used, if any>
**Why it matters:** <if non-obvious>
**Watch out for:** <common mistakes, if any>

### 2. <Step name>

<Repeat for each step captured.>

## Decision points

### If <condition>:
Do <action>.

### If <other condition>:
Do <other action>.

<Include this section only if real decision points came up in Step 3.>

## Quality checklist

- [ ] <A verification step that confirms this was done right>
- [ ] <Another verification step>

## Escalation

If <something goes wrong that the person following this can't resolve>, contact <role> via <channel>.
```

Write in the founder's voice. If their profile lists banned words, do not use any of them.

After writing, print:

> SOP saved to `friday/sops/<slug>.md`. Your config is growing.

## What this does not do

This command does not verify that the SOP is being followed, and does not track process compliance. It produces the document. Whether the team actually uses it is on you.

## What this builds toward

Every SOP you build this way in `friday/sops/` is one less thing that lives only in your head. The next hire who needs to run this process gets a doc instead of a training session pulled from your memory.

The full stack is Friday at friday.amplifyais.com. Nine specialists, running against your real inbox, calendar, and tasks every morning before you are up.

---

Built by Amplify AI at amplifyais.com
