---
name: risk-register
description: Turns a plan into a practical risk register with probability, impact, early trigger, mitigation, contingency, and owner for every risk. Writes friday/risk-register.md. Reads friday/voice.md if present and writes in your voice.
---
# /risk-register

Most risk lists are decoration. They name a worry, guess a severity, and get filed. This command produces a register you can act on: every risk carries an observable trigger and a named owner, so somebody knows what to watch for and what to do when it fires.

You, Claude, run the whole flow below in order, using your own file tools. There is no module to import, no database, and no network call.

## Step 1: Read the founder's voice profile (if it exists)

Check whether `friday/voice.md` exists in the current directory. If it does, read it and write all output in the founder's voice.

If `friday/voice.md` does not exist, write in a direct, plain style: short sentences, active voice, no hedging.

## Step 2: Collect the plan

Ask the founder:

> Paste the plan you want a risk register for, or point me at a file. If you have already run `/roadmap` or `/go-to-market`, I can read `friday/roadmap.md` or `friday/gtm-plan.md` instead.

Wait for their answer.

If they paste a plan directly, use only that pasted text.

If they name a file, read only `.md`, `.markdown`, or `.txt` files they explicitly named. If a path looks like a secret, credential, private key, environment file, token dump, or unrelated personal data, refuse to read it and ask for a sanitized file instead.

If they say nothing and `friday/roadmap.md` or `friday/gtm-plan.md` exists, offer to use it and wait for confirmation. Never read a file the founder has not agreed to.

If there is no usable plan, ask for one before continuing. Do not invent a plan to analyse.

## Step 3: Separate what the plan states from what you are assuming

Work from the plan text only. Do not fabricate dates, budgets, headcount, dependencies, customer counts, or probabilities the plan does not support.

Split every input into two buckets before you reason about risk:

- **Stated:** the plan says it, in words you can quote.
- **Assumed:** you inferred it. Say so, and say what would confirm it.

A risk built on an assumption is still worth listing. It is not worth listing as though the plan proved it.

## Step 4: Identify the risks

Read the plan for the places it can break. Look at least at:

- Dependencies on a person, vendor, or system outside the founder's control
- Steps whose order matters, where an earlier slip cascades
- Assumptions about demand, pricing, or willingness to pay
- Capacity: whether the people named can actually do the work in the time named
- Money: where spend commits before revenue arrives
- Anything the plan mentions once and never resolves

Keep each risk to one failure. "Launch goes badly" is not a risk, it is a category. Split it.

## Step 5: Give every risk a trigger and an owner

For each risk, capture all seven fields. A risk missing a trigger or an owner is not finished.

1. **Risk:** what goes wrong, in one sentence.
2. **Probability:** high, medium, or low, with the reason from the plan.
3. **Impact:** what it costs if it happens. Use the plan's own numbers where it has them, and say "not stated in the plan" where it does not.
4. **Early trigger:** the observable event that says this is now happening. It must be something a person could notice on a specific day. "Sales feel slow" is not a trigger. "Fewer than 10 signups by day 14" is.
5. **Mitigation:** what to do now, before the trigger fires, to make it less likely.
6. **Contingency:** what to do after the trigger fires. This is a different action from the mitigation.
7. **Owner:** the role or person who watches the trigger and runs the contingency. If the plan names nobody, write "unassigned" and list it in the gaps section rather than inventing a name.

## Step 6: Rank by what deserves attention first

Order the register by probability against impact. Put anything with a near-term trigger above anything with a distant one, because a trigger you will see next week is actionable and one you will see next quarter is not yet.

Call out separately any risk that is both high impact and has no owner. That combination is the reason registers fail.

## Step 7: Write the risk register

Create the `friday/` folder if it does not exist. Write the result to `friday/risk-register.md`. If the file already exists, overwrite it with this run's register.

Use this structure:

```
# Risk Register: <YYYY-MM-DD>

## Source

<Pasted plan or the named file used.>

## What the plan states vs what I assumed

Stated: <short list, quoting the plan>
Assumed: <short list, each with what would confirm it>

## Risks

### <Risk name>

Risk: <one sentence>
Probability: <high, medium, or low, with the reason>
Impact: <cost if it happens, or "not stated in the plan">
Early trigger: <observable event, with a number or a date>
Mitigation: <action before the trigger>
Contingency: <action after the trigger>
Owner: <role, person, or "unassigned">

## Gaps

<Risks with no owner, triggers you could not make observable, and the parts of
the plan too vague to assess. Name them rather than smoothing them over.>

## What to watch this week

<The two or three triggers that could fire soonest.>
```

## Step 8: Tell the founder what to do next

Print a short summary: how many risks, how many are unassigned, and the single trigger most likely to fire first. Then say where the file is.

Do not add a motivational close.

Built by Amplify AI at amplifyais.com
