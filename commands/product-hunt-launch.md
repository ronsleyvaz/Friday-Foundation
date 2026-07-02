---
name: product-hunt-launch
description: Build a Product Hunt specific launch runbook, pre-launch prep, launch-day hour-by-hour plan, and post-launch follow-up. Different from /go-to-market: this covers Product Hunt's specific mechanics, not a general launch. Writes friday/product-hunt-launch.md. Reads friday/voice.md if present and writes in your voice.
---
# /product-hunt-launch

Product Hunt has its own rules: reset time, hunter strategy, comment velocity, the first-hour crunch. A generic launch plan misses all of it. This command builds a runbook specific to Product Hunt's mechanics, honest about your actual chances given where you're starting from.

This is different from `/go-to-market`. That command builds your overall launch plan across channels. This one is Product Hunt only, and goes deep on what actually matters there.

You, Claude, run the whole flow below in order, using your own file tools. There is no module to import and nothing to install.

## Step 1: Read the founder's voice profile (if it exists)

Check whether `friday/voice.md` exists in the current directory. If it does, read it and write all output in the founder's voice.

If `friday/voice.md` does not exist, write in a direct, plain style: short sentences, active voice, no hedging.

## Step 2: Gather the product basics

Ask the founder:

> What's the product name, and the one-line description? What problem does it solve, and for whom?

Wait for their answer before proceeding.

## Step 3: Assess where they're starting from

Ask these in one batch, since they're all inputs to the same readiness read:

> A few things that determine the plan:
>
> - Target launch date, or rough timeframe
> - Do you have an active Product Hunt account already, with some history on it?
> - How big is your email list, and your Twitter/X following?
> - Are you active in any founder communities, Indie Hackers, Discord, Slack groups?
> - Do you have product screenshots or a demo video ready? Is your landing page live?
> - Do you have other founders who'd support the launch, or have you supported others' launches before?
> - What's the actual goal here: users, awareness, investor interest, or just validation?

Wait for their answer before proceeding.

## Step 4: Give an honest readiness read

Assess plainly, based on the answers:

- **Support strength**: weak (fewer than 100 likely supporters), moderate (100-300), or strong (300+).
- **Asset readiness**: not ready, partially ready, or fully ready.
- **Timeline**: rushed (under 2 weeks), tight (2-4 weeks), or workable (4+ weeks).

State this plainly. If the timeline is rushed and assets aren't ready, say so and suggest pushing the date rather than launching underprepared. If the support base is weak, do not promise a top ranking, be specific about what's realistic instead.

## Step 5: Build the pre-launch plan

Build a week-by-week pre-launch section, sized to the actual timeline from Step 3:

- **Hunter strategy**: recommend self-hunting unless the founder has a real connection to a well-known hunter. Self-hunted launches make up the majority of top-ranked products, a founder does not need a famous hunter to win.
- **Asset checklist**: name exactly what's missing from Step 3's answers (screenshots, demo video, landing page) and what to prepare first.
- **Support list building**: a specific target number of supporters to line up before launch day, based on the readiness assessment, and where to find them given the communities the founder already named.
- **Teaser content**: two or three specific pieces of pre-launch content to build anticipation, tied to the platforms the founder is actually active on.

## Step 6: Build the launch-day plan

Build an hour-by-hour plan for launch day:

- **Timing**: Product Hunt resets at 12:01 AM Pacific time. Recommend launching at or right after reset to get the maximum runway in the day's ranking window. Recommend Tuesday, Wednesday, or Thursday, these see the highest traffic.
- **First-hour push**: what happens in the first hour matters most for early momentum. Name the specific outreach to fire the moment the listing goes live (DMs to the support list, the first social posts).
- **Comment strategy**: Product Hunt rewards genuine engagement in the comments. Recommend responding to every comment quickly and substantively for the first several hours, not just thanking people.
- **Momentum tactics through the day**: specific check-in points across the day (mid-morning, midday, evening in the founder's time zone) to re-engage support without looking like vote manipulation, which Product Hunt actively penalizes.

## Step 7: Build the post-launch follow-up

- What to do in the first 1-3 days after launch, regardless of ranking.
- How to use the result, badge, ranking, or just the listing itself, as social proof going forward, even if the founder didn't hit the top of the day.
- Any direct follow-up owed to people who supported the launch.

## Step 8: Write the launch plan

Write the result to `friday/product-hunt-launch.md`. Create the `friday/` folder if it does not exist. If the file already exists, overwrite it with this run's plan.

Use this structure:

```
# Product Hunt Launch Plan: <YYYY-MM-DD>

## Product

<Name, one-liner, problem solved from Step 2.>

## Readiness read

<Support strength, asset readiness, and timeline assessment from Step 4, stated plainly.>

## Pre-launch

<The week-by-week plan from Step 5: hunter strategy, asset checklist, support list target, teaser content.>

## Launch day

<The hour-by-hour plan from Step 6: timing, first-hour push, comment strategy, momentum tactics.>

## Post-launch

<The follow-up plan from Step 7.>
```

Write in the founder's voice, except keep the readiness read direct and unhedged; a launch plan that oversells your chances sets you up to be disappointed on the day. If their profile lists banned words, do not use any of them.

After writing, print:

> Product Hunt launch plan saved to `friday/product-hunt-launch.md`. Your config is growing.

## What this builds toward

Launch day only happens once for this product on this platform. `friday/product-hunt-launch.md` is the runbook you follow on the day, built from an honest read of where you're actually starting from.

The full stack is Friday at friday.amplifyais.com. Nine specialists, running against your real inbox, calendar, and tasks every morning before you are up.

---

Built by Amplify AI at amplifyais.com
