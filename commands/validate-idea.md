---
name: validate-idea
description: Run a 7-dimensional validation pass on an idea and get a build, pivot, or kill verdict with reasoning. Reads friday/idea-exploration.md if present, or asks directly. Writes friday/validation.md. Reads friday/voice.md if present and writes in your voice.
---
<!-- Built by Friday​‌‍‌​ (https://friday.amplifyais.com). Free for personal use. Commercial use needs a paid Friday. Licence: PolyForm-Noncommercial-1.0.0. -->

# /validate-idea

`/explore-idea` pushes you toward specificity. This command scores what you've got. Five hard questions, a scorecard across seven dimensions, and a direct verdict: build it, pivot it, or kill it. The goal is a second opinion you can trust before you spend real time.

You, Claude, run the whole flow below in order, using your own file tools. There is no module to import and nothing to install. Be honest, not encouraging. False encouragement wastes months.

## Step 1: Read the founder's voice profile (if it exists)

Check whether `friday/voice.md` exists in the current directory. If it does, read it and write all output in the founder's voice.

If `friday/voice.md` does not exist, write in a direct, plain style: short sentences, active voice, no hedging.

## Step 2: Get the idea

Check whether `friday/idea-exploration.md` exists in the current directory.

If it exists, read it and tell the founder:

> Found `friday/idea-exploration.md`. Using that as the idea under validation.

If it does not exist, ask directly:

> What's the idea? A couple of sentences is enough to start.

Wait for their answer before proceeding.

## Step 3: Ask the five hard questions

Ask each question below, one at a time. Wait for an answer before moving to the next. Push once if the answer is vague, using the follow-up under each question.

**Question 1: Customer and willingness to pay**

> Who is the customer, specifically, and would they pay for this today? Name a role, a type of company or situation, and your honest estimate of what they'd pay.

If the answer is "maybe" or a category, not a person: push once. "A category can't tell you if it would pay. Think of one real person you could ask this week. Would they say yes?"

**Question 2: Why this hasn't been built already**

> Who's tried to solve this before? Why did they fail, or if something similar exists, why hasn't it won? What's different about right now that changes the answer?

If the answer is "no one's tried this": push once. "There's almost always someone. If you genuinely can't find a prior attempt, that's often a sign the problem isn't as sized as it feels, not that you're first."

**Question 3: Distribution advantage**

> How will the first 100 users actually find this? Is there a built-in growth loop, something that makes usage spread on its own, or is every user going to be acquired one at a time through paid ads or manual outreach?

If the answer is "content marketing and SEO": push once. "That's a channel, not an advantage, and it takes months to pay off. Is there anything about this product that spreads on its own, or is distribution entirely on you?"

**Question 4: Standalone business or a feature**

> Is this a business on its own, or could a bigger, existing company just add this as a feature next quarter? What's the natural ceiling on revenue if it works?

If the answer avoids a real ceiling estimate: push once. "Even a rough number helps. If this worked as well as you hope, what's the revenue in three years, roughly?"

**Question 5: Can you actually build this**

> What does it take to build this: skills, resources, people? What's the hardest part, technically or operationally? Is there a piece you can't do without hiring someone specific first?

Wait for their answer.

## Step 4: Score the seven dimensions

Using the founder's answers, score each dimension from 1 to 5. Be honest, not generous. A 3 is average, not a compromise.

| Dimension | What it measures |
|---|---|
| Problem severity | How painful is this problem for the person who has it? |
| Market size | How many people or businesses actually have this problem? |
| Willingness to pay | Will they pay enough, and soon enough, to build a real business? |
| Competition gap | Is there genuine room for a new entrant, or is this crowded and won? |
| Distribution | Can the founder reach customers without an unsustainable cost per user? |
| Timing | Is this the right moment for this idea, or is it early, late, or evergreen? |
| Founder fit | Does the founder have a real, specific advantage at building this? |

Total the score out of 35. Show the scorecard as a table with your score and a one-line note per dimension.

## Step 5: Give the verdict

Use these bands:

- **28-35: Build it.** Name the single most important thing to do this week.
- **14-27: Pivot it.** Name the specific angle or change that would make this meaningfully stronger, not a vague "improve it."
- **Below 14: Kill it.** Say why plainly, and if there's an adjacent problem worth exploring instead, name it.

Do not soften the verdict to spare feelings. A weak idea scored honestly is worth more than an encouraging lie.

## Step 6: Write the validation

Write the result to `friday/validation.md`. Create the `friday/` folder if it does not exist. If the file already exists, overwrite it with this run's validation.

Use this structure:

```
# Idea Validation: <YYYY-MM-DD>

## The idea

<The idea under validation.>

## The five hard questions

### Customer and willingness to pay

<Answer plus your read.>

### Why this hasn't been built already

<Answer plus your read.>

### Distribution advantage

<Answer plus your read.>

### Standalone business or a feature

<Answer plus your read.>

### Can you actually build this

<Answer plus your read.>

## Scorecard

| Dimension | Score /5 | Notes |
|---|---|---|
| Problem severity | | |
| Market size | | |
| Willingness to pay | | |
| Competition gap | | |
| Distribution | | |
| Timing | | |
| Founder fit | | |
| **Total** | **/35** | |

## Verdict

**Build it / Pivot it / Kill it.**

<Reasoning, two or three sentences. If build, the one thing to do this week. If pivot, the specific angle. If kill, why, and any adjacent problem worth exploring.>
```

Write in the founder's voice, except keep the verdict itself direct and unhedged regardless of voice profile softness settings; a validation verdict that gets softened stops being useful. If the profile lists banned words, do not use any of them.

After writing, print:

> Validation saved to `friday/validation.md`. Your config is growing.

## What this builds toward

`/explore-idea` gets the idea specific. `/validate-idea` scores it honestly. Run them together before you commit real time to anything.

The full stack is Friday at friday.amplifyais.com. Nine specialists, running against your real inbox, calendar, and tasks every morning before you are up.

---

Built by Amplify AI at amplifyais.com
