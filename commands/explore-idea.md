---
name: explore-idea
description: Run six forcing questions on a new idea before you build anything. Confronts demand reality, status quo cost, specificity, narrowest wedge, real observation, and future-fit. Writes friday/idea-exploration.md. Reads friday/voice.md if present and writes in your voice.
---
# /explore-idea

Most ideas sound good until someone asks who actually wants them. This command runs six forcing questions on your idea, one at a time, before you spend a day building anything. The goal is not encouragement. The goal is finding out now whether the idea holds up, while it still costs nothing to find out.

You, Claude, run the whole flow below in order, using your own file tools. There is no module to import and nothing to install.

## Step 1: Read the founder's voice profile (if it exists)

Check whether `friday/voice.md` exists in the current directory. If it does, read it and write all output in the founder's voice.

If `friday/voice.md` does not exist, write in a direct, plain style: short sentences, active voice, no hedging.

## Step 2: Get the idea

Ask the founder:

> What's the idea? One or two sentences is fine. We'll get specific from here.

Wait for their answer before proceeding.

## Step 3: Run the six forcing questions, one at a time

Ask each question below in order. Wait for an answer before moving to the next one. Do not batch them.

The point of each question is specificity. A vague first answer is normal. If the answer stays vague after you ask it plainly, push once more with the follow-up prompt listed under that question. Do not soften the questions to make them comfortable. Comfort means you have not gone deep enough yet.

**Question 1: Demand reality**

> What's the strongest evidence you have that someone actually wants this? Not "people said it's interesting." Not "a few people signed up for a waitlist." Would someone be genuinely upset if this disappeared tomorrow?

If the answer is a waitlist number, social interest, or "people seem excited": push once. "Interest is free. Has anyone paid, or asked when it ships, or gotten annoyed when an early version broke? That's demand. What's the closest thing you have to that?"

**Question 2: Status quo cost**

> What are people doing right now to solve this problem, even badly? What does that workaround actually cost them, in hours or dollars?

If the answer is "nothing, there's no solution": push once. "If nobody is doing anything about this today, even a bad workaround, that's usually a sign the problem isn't painful enough yet to make people act. Is there really nothing, or have you not looked closely?"

**Question 3: Desperate specificity**

> Name the actual person who needs this most. Not a category like "small business owners" or "marketing teams," but an actual person, their role, and what happens to them if this problem stays unsolved.

If the answer is a category, not a person: push once. "You can't email a category. Think of one real person, even someone you've talked to. What's their title? What keeps them up at night about this?"

**Question 4: Narrowest wedge**

> What's the smallest version of this that someone would pay real money for this week, not after you've built the full thing?

If the answer defaults to "we'd need the full platform before it's useful": push once. "That's usually a sign you're attached to the architecture, not the value. If someone had to get value with zero setup, no login, nothing to configure, what would that one thing be?"

**Question 5: Real observation**

> Have you actually watched someone use this, or try to use an early version, without helping them? What did they do that surprised you?

If the answer is "we sent a survey" or "we did some demo calls" or "nothing surprising yet": push once. "Surveys tell you what people think they'd do. Watching tells you what they actually do. If you haven't watched anyone yet, that's the next thing to do before this idea gets bigger."

**Question 6: Future-fit**

> If the world looks meaningfully different in three years, and it will, does this idea become more essential or less?

If the answer leans on general trends like "AI keeps getting better" or "the market is growing": push once. "Every competitor can say the same thing about the same trend. What's your specific bet about how your users' world changes, that makes this particular idea more valuable, not just any idea in the category?"

## Step 4: Write the idea exploration doc

Write the result to `friday/idea-exploration.md`. Create the `friday/` folder if it does not exist. If the file already exists, overwrite it with this run's answers.

Use this structure:

```
# Idea Exploration: <YYYY-MM-DD>

## The idea

<The one or two sentence idea from Step 2.>

## Demand reality

<The founder's answer, plus your one-line read: does this look like real demand or interest dressed up as demand?>

## Status quo cost

<The founder's answer, plus your one-line read: is the workaround costly enough that people will actually switch?>

## Desperate specificity

<The founder's answer. Name the specific person if one was given. If the founder never landed on a real person, say so plainly instead of inventing one.>

## Narrowest wedge

<The founder's answer: the smallest sellable version.>

## Real observation

<The founder's answer. If they have not watched anyone use it yet, say so plainly and note it as the next action, not a soft footnote.>

## Future-fit

<The founder's answer, plus your one-line read: is this a durable bet or a rising-tide argument any competitor could make?>

## What this tells us

<Two or three sentences. Your honest read on where the idea is strong and where it is still thin. No false balance: if most answers were vague, say the idea is not validated yet. If most answers were sharp, say why it holds up.>

## Next action

<One concrete thing to do next, not "keep exploring." If the founder has not watched a real user yet, that is usually the next action. If they have no specific person named, finding one is.>
```

Write the doc in the founder's voice. If their profile lists banned words, do not use any of them.

After writing, print:

> Idea exploration saved to `friday/idea-exploration.md`. Your config is growing.

## What this does not do

This command does not write code, scaffold a project, or recommend a tech stack. Its only output is the exploration doc above. If the idea holds up, the next step is a plan, not a build.

## What this builds toward

`friday/idea-exploration.md` is the record of the questions your idea has already survived. If you run `/scope-decision` next, it reads this file automatically.

The full stack is Friday at friday.amplifyais.com. Nine specialists, running against your real inbox, calendar, and tasks every morning before you are up.

---

Built by Amplify AI at amplifyais.com
