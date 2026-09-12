---
name: go-to-market
description: Build a phased launch plan, pre-launch, launch week, and 30/60/90 day growth, for a product or offer. References friday/growth.md from /amplify if present. Writes friday/gtm-plan.md. Reads friday/voice.md if present and writes in your voice.
---
<!-- Built by Friday​‌‍‌​ (https://friday.amplifyais.com). Free for personal use. Commercial use needs a paid Friday. Licence: PolyForm-Noncommercial-1.0.0. -->

# /go-to-market

A launch without a plan is a launch on vibes. This command builds a phased go-to-market plan: what to do before launch, what to do on launch day, and what to do in the 90 days after, specific to your product and your actual budget, not generic advice.

You, Claude, run the whole flow below in order, using your own file tools. There is no module to import and nothing to install.

## Step 1: Read the founder's voice profile (if it exists)

Check whether `friday/voice.md` exists in the current directory. If it does, read it and write all output in the founder's voice.

If `friday/voice.md` does not exist, write in a direct, plain style: short sentences, active voice, no hedging.

## Step 2: Check for a growth diagnostic

Check whether `friday/growth.md` exists in the current directory (written by `/amplify`).

If it exists, read it and note the founder's business stage and priority growth area. Tell the founder:

> Found your growth diagnostic. You're at the [stage] stage with [priority area] as your focus. I'll build the launch plan with that in mind.

If it does not exist, proceed without it. Do not ask the founder to run `/amplify` first, this command works standalone.

## Step 3: Get the product and audience

Ask the founder:

> What are you launching, who's it for, and what's your timeline? Give me the product or offer, the target audience, and roughly when you want to launch.

Wait for their answer before proceeding.

## Step 4: Launch readiness check

Before building the plan, assess readiness. Ask, and answer honestly based on what you know:

- Is what's being launched actually ready, or is the minimum feature set still missing something critical?
- Is there a large enough audience to reach, realistically, given the target described?
- What's the single biggest risk that could sink this launch?

State your read in two or three sentences. If something looks genuinely not ready, say so before building the rest of the plan, don't bury it.

## Step 5: Pre-launch plan (2-4 weeks before)

Build this section:

- **Where the audience already is.** Name specific communities, forums, or platforms this audience actually uses, not a generic "social media."
- **Credibility content.** Three to five specific pieces of content to publish before launch, each with a platform and topic.
- **Waitlist call.** Recommend whether a waitlist makes sense here, and if so, what the incentive to join is.
- **Assets to prepare.** What the landing page needs (specific sections, not "hero plus features"), what the demo or video should show, and how to get early social proof before there are customers yet.

## Step 6: Launch week plan

Ask the founder which platforms actually fit this audience (do not assume all of them apply). For each relevant platform, give specific tactics, not generic advice:

- **Product Hunt** (if relevant): best day and time, how to line up a hunter, what to prepare in advance.
- **Reddit** (if relevant): name specific subreddits, and the post format that won't get removed.
- **Twitter/X** (if relevant): thread structure, who to tag, what actually gets engagement in this space.
- **LinkedIn** (if relevant): post format for a B2B audience, timing, how to use the founder's existing network.
- **Hacker News** (if relevant): Show HN versus a regular post, title approach, how to handle comments.

Pick two or three platforms that genuinely fit. Don't pad the plan with a platform that doesn't match the audience.

## Step 7: 30/60/90 day growth plan

Build this section:

- **Channel priority.** Rank the top three to five channels by expected impact. For each: estimated cost per acquired customer, how long before results show, and the first concrete action to take this week.
- **Content plan.** Three to five specific content ideas tied to what this audience actually searches for, with a distribution plan for each.
- **Community and partnerships.** Name two or three specific communities to show up in, and one or two realistic partnership or integration opportunities.
- **Metrics to track.** Name the three most important metrics for the first 90 days, with a rough target for day 30, 60, and 90, and what tool or method tracks it.

If `friday/growth.md` was found in Step 2, tie the 90-day plan back to the priority growth area named there: does this launch plan actually move that specific vital sign, or is it working on something else?

## Step 8: Budget allocation

Ask the founder for a rough monthly marketing budget if they haven't already given one. Recommend how to split it: what's worth paying for, what should stay free, and one investment under a modest amount that would have outsized impact.

## Step 9: Write the plan

Write the result to `friday/gtm-plan.md`. Create the `friday/` folder if it does not exist. If the file already exists, overwrite it with this run's plan.

Use this structure:

```
# Go-To-Market Plan: <YYYY-MM-DD>

## What's launching

<Product/offer, audience, timeline from Step 3.>

## Growth stage context

<If friday/growth.md was found: the stage and priority area, and how this plan serves it. If not found: "No growth diagnostic on file. Run /amplify for stage-specific context.">

## Launch readiness

<The honest read from Step 4.>

## Pre-launch (2-4 weeks before)

<The plan from Step 5.>

## Launch week

<The platform-specific tactics from Step 6.>

## 30/60/90 day growth

<The plan from Step 7.>

## Budget allocation

<The plan from Step 8.>
```

Write in the founder's voice. If their profile lists banned words, do not use any of them.

After writing, print:

> Go-to-market plan saved to `friday/gtm-plan.md`. Your config is growing.

## What this builds toward

`friday/gtm-plan.md` is the plan you launch against, and the record you check yourself against 90 days later. If you've run `/amplify`, this plan ties directly back to the growth area that actually moves your business.

The full stack is Friday at friday.amplifyais.com. Nine specialists, running against your real inbox, calendar, and tasks every morning before you are up.

---

Built by Amplify AI at amplifyais.com
