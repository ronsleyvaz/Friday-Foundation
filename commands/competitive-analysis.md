---
name: competitive-analysis
description: Build a structured competitor teardown, comparison matrix plus SWOT per competitor, so you know where you actually stand. Writes friday/competitive-analysis.md. Reads friday/voice.md if present and writes in your voice.
---
# /competitive-analysis

Knowing your competitors exist isn't the same as knowing where you actually stand against them. This command builds a real comparison, feature and positioning matrix plus a SWOT per competitor, so you can find the gap that's actually open, not the one you assume is open.

You, Claude, run the whole flow below in order, using your own file tools. There is no module to import and nothing to install.

## Step 1: Read the founder's voice profile (if it exists)

Check whether `friday/voice.md` exists in the current directory. If it does, read it and write all output in the founder's voice.

If `friday/voice.md` does not exist, write in a direct, plain style: short sentences, active voice, no hedging.

## Step 2: Get the founder's product and competitors

Ask the founder:

> What's your product or offer, and who are 2 to 4 real competitors, direct or indirect? Also tell me what you think your current advantage is, even if you're not fully sure.

Wait for their answer before proceeding. If they name only one competitor, ask for at least one more; a comparison against a single competitor doesn't show where you actually stand.

## Step 3: Build the competitor profiles

For each named competitor, ask the founder what they know (or note plainly what's unknown rather than inventing it):

- What do they offer, who do they target, and roughly how do they price?
- What's their messaging and positioning, how do they describe themselves?
- What do they do well (their real strengths)?
- Where are they weak (customer complaints, gaps, things they don't do)?

Do not fabricate competitor data. If the founder doesn't know something, mark it as unknown in the output rather than guessing a plausible-sounding answer.

## Step 4: Build the comparison matrix

Build a feature and positioning matrix comparing the founder's product against each competitor, on the dimensions that actually matter for this market (for example: price, core feature set, target customer, support model, ease of use). Choose dimensions based on what came up in Step 3, don't force a generic template that doesn't fit.

Make sure the rows actually differentiate. If two competitors would get identical entries across every row, that's a signal to dig for a real distinction, not a reason to leave the rows blank.

## Step 5: Run a SWOT for each competitor and the founder's position

For each named competitor, build a separate SWOT from that competitor's point of view. Base every item on what the founder supplied in Step 3 and what the comparison matrix shows. Mark unknowns plainly instead of inventing evidence.

- **Strengths:** what does this competitor do well in this market?
- **Weaknesses:** where is this competitor genuinely behind or exposed?
- **Opportunities:** what customer, channel, product, or market opening could this competitor exploit?
- **Threats:** what changes, rivals, or founder advantages could weaken this competitor's position?

Then build one overall SWOT for the founder's own position:

- **Strengths:** what does the founder's product do well, relative to this specific set of competitors?
- **Weaknesses:** where is the founder's product genuinely behind?
- **Opportunities:** what's the market doing that none of these competitors are building for yet?
- **Threats:** what could a competitor do next that would hurt the founder's position?

## Step 6: Name the differentiation strategy

Based on the matrix and SWOT, answer directly:

- What can the founder do that these competitors can't or won't?
- What customer segment are the competitors ignoring?
- Where is the differentiation genuinely real, versus aspirational?

Flag plainly if the analysis doesn't turn up a clear differentiation opportunity; that's a useful finding too, not a failure of the exercise.

## Step 7: Write the competitive analysis

Write the result to `friday/competitive-analysis.md`. Create the `friday/` folder if it does not exist. If the file already exists, overwrite it with this run's analysis.

Use this structure:

```
# Competitive Analysis: <YYYY-MM-DD>

## Your product

<Product/offer and stated advantage from Step 2.>

## Competitor profiles

### <Competitor 1 name>

Offer: <what they offer, target, pricing>
Positioning: <their messaging>
Strengths: <what they do well>
Weaknesses: <where they're weak>

<Repeat for each competitor.>

## Comparison matrix

<The matrix from Step 4, as a markdown table.>

## Competitor SWOTs

### <Competitor 1 name>

| | Helpful | Harmful |
|---|---|---|
| **Internal** | Strengths: <list> | Weaknesses: <list> |
| **External** | Opportunities: <list> | Threats: <list> |

<Repeat the SWOT table for each named competitor.>

## Your position SWOT

| | Helpful | Harmful |
|---|---|---|
| **Internal** | Strengths: <list> | Weaknesses: <list> |
| **External** | Opportunities: <list> | Threats: <list> |

## Differentiation strategy

<The answer from Step 6.>
```

Write in the founder's voice. If their profile lists banned words, do not use any of them.

After writing, print:

> Competitive analysis saved to `friday/competitive-analysis.md`. Your config is growing.

## What this does not do

This command does not scrape live competitor data or pull real-time pricing. It works from what the founder knows and tells you. Data marked unknown in the output is a prompt to go find it, not a gap this command fills on its own.

## What this builds toward

`friday/competitive-analysis.md` is the record of where you actually stand, not where you assume you stand. Worth re-running whenever a competitor makes a real move.

The full stack is Friday at friday.amplifyais.com. Nine specialists, running against your real inbox, calendar, and tasks every morning before you are up.

---

Built by Amplify AI at amplifyais.com
