---
name: pricing-strategy
description: Walk value-based pricing logic and tier design, then produce a specific tier structure with real numbers. Writes friday/pricing.md. Reads friday/voice.md if present and writes in your voice.
---
<!-- Built by Friday​‌‍‌​ (https://friday.amplifyais.com). Free for personal use. Commercial use needs a paid Friday. Licence: PolyForm-Noncommercial-1.0.0. -->

# /pricing-strategy

Pricing shouldn't be a guess you made once and never revisited. This command walks you through picking a pricing model, designing tiers with real numbers, checking the unit economics, and a quick way to test whether customers agree with your number before you commit to it.

You, Claude, run the whole flow below in order, using your own file tools. There is no module to import and nothing to install.

## Step 1: Read the founder's voice profile (if it exists)

Check whether `friday/voice.md` exists in the current directory. If it does, read it and write all output in the founder's voice.

If `friday/voice.md` does not exist, write in a direct, plain style: short sentences, active voice, no hedging.

## Step 2: Gather the inputs

Ask the founder:

> Give me what you've got: the offer or product, your target customer, current pricing if you have any, and cost structure if you know it, roughly what it costs you to deliver this per customer. If you don't know the cost side yet, say so and we'll work around it.

Wait for their answer before proceeding.

Also ask:

> Do you know what competitors charge for something similar? Even one or two data points helps.

Wait for their answer. If they don't know, proceed without it and note the gap in the output rather than inventing numbers.

## Step 3: Recommend a pricing model

Based on the offer and cost structure, recommend the best fit among these:

- **Value-based**: price based on the outcome delivered, not the cost to deliver it. Best fit for most service and software businesses.
- **Cost-plus**: price equals cost plus a fixed margin. Fits commodity-like offers where the value is hard to differentiate.
- **Competitor-based**: price set relative to known alternatives. Fits crowded markets where customers are actively comparing.
- **Usage-based**: price scales with how much the customer actually uses. Fits offers where usage varies widely between customers.

State the recommendation and the reason in two or three sentences, specific to what the founder described, not a generic explanation of the model.

## Step 4: Design the tiers

Design three tiers with real numbers, not placeholders:

- **Starter/Basic**: low price, limited features. Exists to get someone in the door and to make the middle tier look reasonable by comparison.
- **Growth/Pro**: the tier you actually want most customers to land on. This is where the best value sits.
- **Business/Premium**: highest price, most complete. Exists to anchor the other two tiers higher, and may be sales-led rather than self-serve depending on the offer.

For each tier, give: a name, a monthly price and an annual price with a stated discount percentage, five to eight specific features or limits (not vague terms like "advanced features"), and the trigger that makes someone outgrow this tier and move to the next.

## Step 5: Unit economics check

If the founder gave you cost information in Step 2, calculate:

- Rough cost to deliver per customer per month.
- Gross margin at each tier, given the price and the cost.
- How many customers at each tier it takes to break even against fixed costs, if the founder gave you that number.

If the founder did not have cost information, skip the numeric calculation and instead state plainly: "No cost data given, so margin can't be calculated. Once you know your delivery cost per customer, re-run this to check the tiers hold up."

## Step 6: Pricing psychology

Recommend three specific tactics for this pricing, not a generic list:

- **Anchoring**: which tier gets shown first, and why that ordering makes the target tier look like the obvious choice.
- **Decoy effect**: is the pricing structured so the middle tier is clearly the best value next to the other two, or does it need adjusting?
- **Annual discount framing**: how to present the annual option so the saving is obvious without looking like a trick.

## Step 7: Price sensitivity check (optional)

Offer the founder a quick way to test the price before committing:

> Want to run a quick price sensitivity check? Four questions, based on the Van Westendorp method. Takes two minutes, and you can literally ask a handful of real prospects the same four questions to see where your number actually lands.

If yes, walk through the four questions with the founder (answering for their own instinct now, with the suggestion to also ask real prospects later):

1. At what price would this be so cheap you'd question the quality?
2. At what price would this be a bargain, a great deal for the value?
3. At what price would this start to feel expensive, but you'd still consider it?
4. At what price would this be so expensive you wouldn't consider it at all?

Note where the founder's chosen tier prices fall relative to their own answers. If the target tier price sits close to the "too expensive" end, flag it plainly.

If no, skip this step.

## Step 8: Write the pricing strategy

Write the result to `friday/pricing.md`. Create the `friday/` folder if it does not exist. If the file already exists, overwrite it with this run's strategy.

Use this structure:

```
# Pricing Strategy: <YYYY-MM-DD>

## The offer

<Product/offer, target customer, current pricing if any, from Step 2.>

## Recommended model

<The model and reasoning from Step 3.>

## Tier structure

| Tier | Monthly | Annual | Key features | Target customer |
|---|---|---|---|---|
| <Starter> | | | | |
| <Growth> | | | | |
| <Business> | | | | |

Upgrade triggers: <what moves someone from one tier to the next.>

## Unit economics

<The calculation from Step 5, or the plain note that cost data wasn't available.>

## Pricing psychology

<The three tactics from Step 6.>

## Price sensitivity check

<The Van Westendorp answers and read from Step 7, or "Skipped this run." if not run.>
```

Write in the founder's voice. If their profile lists banned words, do not use any of them.

After writing, print:

> Pricing strategy saved to `friday/pricing.md`. Your config is growing.

## What this does not do

This command does not pull live competitor pricing data automatically. If you gave competitor numbers in Step 2, they're used as context. If you didn't, the strategy is built from your offer and cost structure alone, and that gap is worth closing before you finalize a number.

## What this builds toward

Pricing isn't a permanent decision, it's a starting point you revisit. `friday/pricing.md` is that starting point, with the reasoning attached so future-you can see why the number was what it was.

The full stack is Friday at friday.amplifyais.com. Nine specialists, running against your real inbox, calendar, and tasks every morning before you are up.

---

Built by Amplify AI at amplifyais.com
