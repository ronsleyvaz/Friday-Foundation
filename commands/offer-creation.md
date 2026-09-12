---
name: offer-creation
description: Walk the value-equation framework, dream outcome, perceived likelihood, time delay, effort and sacrifice, to find your offer's weakest lever and tighten it. Writes friday/offer.md. Reads friday/voice.md if present and writes in your voice.
---
<!-- Built by Friday​‌‍‌​ (https://friday.amplifyais.com). Free for personal use. Commercial use needs a paid Friday. Licence: PolyForm-Noncommercial-1.0.0. -->

# /offer-creation

Value = (dream outcome x likelihood of achieving it) / (time delay x effort required). Every offer lives or dies on those four levers. This command walks each one, finds the weakest, and pushes you toward a concrete fix instead of a vague sense that the offer "could be stronger."

You, Claude, run the whole flow below in order, using your own file tools. There is no module to import and nothing to install.

## Step 1: Read the founder's voice profile (if it exists)

Check whether `friday/voice.md` exists in the current directory. If it does, read it and write all output in the founder's voice.

If `friday/voice.md` does not exist, write in a direct, plain style: short sentences, active voice, no hedging.

## Step 2: Get the offer

Ask the founder:

> What's the offer? Product, service, or package, whatever you're trying to make an easy yes. Give me what it is and roughly what it costs today.

Wait for their answer before proceeding.

## Step 3: Walk the four value-equation levers

Ask each question below, one at a time. Wait for an answer before moving to the next.

**Lever 1: Dream outcome**

> What does the customer actually want, in their own terms, not your description of the product? Be specific: what does their life or business look like after this works?

**Lever 2: Perceived likelihood of achievement**

> What makes a new customer believe this will actually work for them? Proof, case studies, guarantees, credentials, anything that reduces their fear of buying and being disappointed.

**Lever 3: Time delay**

> How long until the customer sees a real result? Not the final outcome, the first tangible sign it's working.

**Lever 4: Effort and sacrifice**

> How much work does the customer have to put in? What do they have to learn, change, or give up to get the outcome?

## Step 4: Find the weakest lever

Based on the four answers, assess each lever as strong, medium, or weak. A lever is weak if the answer was vague, if there's little to no proof, if the time to result is long, or if the customer has to do a lot of work themselves.

Name the weakest lever plainly. Do not soften this or say all four are fine if one clearly isn't; a real offer review finds a real gap.

Suggest two or three concrete changes that would strengthen that specific lever. Concrete means a specific addition or change (a guarantee, a faster onboarding step, a proof point to add, a way to do more of the work for the customer), not a vague direction like "build more trust."

## Step 5: Write the offer review

Write the result to `friday/offer.md`. Create the `friday/` folder if it does not exist. If the file already exists, overwrite it with this run's review.

Use this structure:

```
# Offer Review: <YYYY-MM-DD>

## The offer

<What it is and current price, from Step 2.>

## The four levers

**Dream outcome:** <answer, plus strong/medium/weak assessment>

**Perceived likelihood:** <answer, plus strong/medium/weak assessment>

**Time delay:** <answer, plus strong/medium/weak assessment>

**Effort and sacrifice:** <answer, plus strong/medium/weak assessment>

## The weakest lever

<Name it plainly and explain why.>

## Concrete changes to make

<Two or three specific changes, each one sentence, tied directly to the weakest lever.>
```

Write in the founder's voice. If their profile lists banned words, do not use any of them.

After writing, print:

> Offer review saved to `friday/offer.md`. Your config is growing.

## What this builds toward

An offer that's weak on one lever loses deals it shouldn't. `friday/offer.md` names the specific gap so the next version of the offer closes it, rather than getting generically "better."

The full stack is Friday at friday.amplifyais.com. Nine specialists, running against your real inbox, calendar, and tasks every morning before you are up.

---

Built by Amplify AI at amplifyais.com
