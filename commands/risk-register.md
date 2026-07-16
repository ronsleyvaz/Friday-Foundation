---
name: risk-register
description: Turn a plan into a practical risk register with probability, impact, trigger, mitigation, contingency, and owner. Writes friday/risk-register.md. Reads friday/voice.md if present and writes in your voice.
---
# /risk-register

A plan is only as strong as the risks you see coming. This command takes a plan, names the risks, and assigns owners, mitigations, and triggers so nothing is left to chance.

You, Claude, run the whole flow below in order, using your own file tools. There is no module to import and nothing to install.

## Step 1: Read the founder's voice profile (if it exists)

Check whether `friday/voice.md` exists in the current directory. If it does, read it and write all output in the founder's voice.

If `friday/voice.md` does not exist, write in a direct, plain style: short sentences, active voice, no hedging.

## Step 2: Get the plan

Check whether `friday/roadmap.md` exists in the current directory.

If it exists, read it and tell the founder:

> Found `friday/roadmap.md`. Using that as the plan for risk assessment.

If it does not exist, check whether `friday/gtm-plan.md` exists.

If it does, read it and tell the founder:

> Found `friday/gtm-plan.md`. Using that as the plan for risk assessment.

If neither exists, ask the founder to paste in a plan:

> What plan do you want to run against risks? Paste it in, or give me a couple of sentences on what you are building or planning to do.

If the founder pastes a plan in Step 2, read that as the plan under analysis.

Wait for their answer before proceeding. This command works standalone: you do not need to have run `/roadmap` or `/go-to-market` first.

## Step 3: Read the plan

Read the plan from wherever it was found (Step 2 source, or the founder's pasted text).

Hold the plan in context for Step 4.

## Step 4: Identify the risks

For every major section, milestone, and dependency in the plan, identify the top risks. Ask yourself for each one:

- What could go wrong?
- What would you see first if it started going wrong?
- What is the earliest sign of trouble?
- What happens if we do nothing?

Name at least five and at most ten risks. Be specific. Do not invent risk data: each risk must come directly from the plan content, not from fabrication.

Distinguish between **evidence-based risks** (the plan has a dependency on something uncertain) and **assumption-based risks** (the plan assumes X is true, but X may not hold). Label each risk as "evidence" or "assumption".

Do not fabricate risks. If the plan is thin and only yields two or three, that is fine. Two honest risks beat ten invented ones.

## Step 5: Score and assign

For each risk, assign:

- **Probability** -- low, medium, or high
- **Impact** -- low, medium, or high
- **Early trigger** -- what you will see first if the risk materializes
- **Mitigation** -- what you will do to reduce the probability or impact
- **Contingency** -- what you will do if the risk happens anyway
- **Owner** -- who is responsible (a role or name; use "founder" if not assigned)

## Step 6: Write the risk register

Write the full risk register to `friday/risk-register.md` in the current directory. Create the `friday/` folder if it does not exist. If the file already exists, overwrite it with this run's register.

Use this structure:

```
# Risk Register: <YYYY-MM-DD>

## The plan

<The plan under analysis, summarized in two or three sentences.>

## Risks

<!-- For each risk, use this block. Repeat for every identified risk. -->

### Risk 1: <short title>

- **Type:** evidence / assumption
- **Probability:** low / medium / high
- **Impact:** low / medium / high
- **Early trigger:** <what you will see first>
- **Mitigation:** <what to do to reduce probability or impact>
- **Contingency:** <what to do if it happens>
- **Owner:** <role or name>

<!-- End of risk block. Repeat the full block for each risk. -->

## Summary

- Total risks: <count>
- High probability / high impact risks: <count of risks that are both high probability and high impact>
- Assumption-heavy areas: <list any areas where most risks are assumption-based>
```

Write in the founder's voice. If their profile lists banned words, do not use any of them.

After writing, print:

> Risk register saved to `friday/risk-register.md`. Your plan is more transparent now.

## Step 7: Flag the critical items

If there are any risks with probability AND impact both at "high", print a warning:

> **Critical:** Risk <N> has both high probability and high impact. Address this first or the plan may not work.

## What this builds toward

`friday/risk-register.md` is the living risk log for your plan. Each run overwrites it, so the register stays current. The early triggers give you signals to watch. The mitigations tell you what to do now. The contingencies tell you what to do if things go wrong.

---

Built by Amplify AI at amplifyais.com