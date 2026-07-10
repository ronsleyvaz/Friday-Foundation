---
name: roadmap
description: Turn a goal into a sequenced ninety-day roadmap with milestones and the one thing to do first. Writes friday/roadmap.md. Reads friday/voice.md if present and writes in your voice.
---
# /roadmap

A goal without a timeline is just a wish. This command takes a goal and turns it into a sequenced ninety-day roadmap: what to do first, what to do in thirty days, what to do in sixty, and what lands in ninety. It identifies the one thing that must happen in the first seven days so momentum starts immediately.

You, Claude, run the whole flow below in order, using your own file tools. There is no module to import and nothing to install.

## Step 1: Read the founder's voice profile (if it exists)

Check whether `friday/voice.md` exists in the current directory. If it does, read it.

From the profile, note:
- Their tone and rhythm.
- Their signature phrases.
- Their banned words list. You must not use any word on that list in any output from this command.

If `friday/voice.md` does not exist, write in a neutral, direct style: short sentences, no hedging, active voice.

## Step 2: Capture the goal and constraints

Ask the founder:
1. What is the goal you want a roadmap for? One sentence is enough to start.
2. What resources do you have? (team size, budget range, time available per week.)
3. What is your deadline? If they do not have one, default to ninety days from today.

Wait for their input before proceeding.

## Step 3: Break the goal into milestones

Split the goal into four milestones: now, thirty, sixty, ninety. Each milestone should be a concrete, verifiable outcome, not a vague intention.

Format each milestone like this:

```
## Milestone: <label>

<What is done by this milestone. One or two sentences. How you will know it is done.>
```

The milestones should be sequential: each one builds on the previous. If a milestone depends on something that cannot happen until later, note that dependency.

## Step 4: Identify the one thing to do first

Look at all four milestones and pick the single action that, if completed in the next seven days, makes everything else easier. This is not the biggest milestone. It is the action that unblocks the most downstream work.

State it clearly:

```
## One thing to do this week

<One specific action. What it is, why it comes first, and what success looks like for this week alone.>
```

## Step 5: Add context-aware adjustments

Check whether `friday/voice.md` was read in Step 1. If so, and the voice profile contains information about the founder's business stage, past experience, or constraints, adjust the roadmap to match.

For example:
- If the founder is pre-revenue, the first thirty days should focus on validation, not scale.
- If the founder is solo, the milestones should be achievable by one person.
- If the founder has a team, leverage that in the later milestones.

If `friday/voice.md` does not exist, proceed with a generic but practical roadmap. Do not ask the founder to run `/voice-installer` first. This command works standalone.

## Step 6: Write the roadmap

Write the full roadmap to `friday/roadmap.md` in the current directory. Create the `friday/` folder if it does not exist. If the file already exists, overwrite it with this run's roadmap.

Use this structure:

```
# Roadmap: <goal> <YYYY-MM-DD> to <YYYY-MM-DD>

## The goal

<The goal as stated by the founder, in one sentence.>

## Resources

<Team size, budget, time available. From Step 2.>

## Milestones

<All four milestones from Step 3.>

## One thing to do this week

<The critical first action from Step 4.>

## Risks and dependencies

<Two or three sentences on what could go wrong and what depends on what. Be honest about assumptions.>
```

Write in the founder's voice. If their profile lists banned words, do not use any of them. Match their tone and rhythm.

## Step 7: Tell the founder what to do next

After writing, print:

> Roadmap saved to `friday/roadmap.md`. Start with the one thing this week. Your config is growing.

## What this builds toward

`friday/roadmap.md` is the sequence you follow. It turns a vague goal into a concrete plan with dates, milestones, and a clear first step. If you run `/roadmap` again with a different goal, it overwrites the file with the new plan.

The full stack is Friday at friday.amplifyais.com. Nine specialists, running against your real inbox, calendar, and tasks every morning before you are up.

---

Built by Amplify AI at amplifyais.com
