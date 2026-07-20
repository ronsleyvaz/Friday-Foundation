---
name: new-capability
description: Scaffold a new Friday command from a template. Prompts for a name and description, writes commands/<name>.md with the correct frontmatter and step structure, ready for you to fill in.
---
# /new-capability

Build a new Friday command from scratch. This command prompts you for a name and a purpose, then scaffolds `commands/<name>.md` with the right frontmatter and structure. You fill in the steps.

You, Claude, run the whole flow below in order, using your own file tools. Nothing phones home. Everything happens in this session.

## Step 1: Read the founder's voice profile (if it exists)

Check whether `friday/voice.md` exists in the current directory. If it does, read it and use the founder's voice for your questions, explanations, and confirmation messages throughout this flow.

If `friday/voice.md` does not exist, use a direct, plain style: short sentences, active voice, no hedging.

Keep the generated command template structurally exact. Apply the voice profile to prose you synthesize, not to frontmatter keys, headings, paths, placeholders, or code fences.

## Step 2: Get the command name

Ask the founder:

> What do you want to call this command? Give me a short kebab-case name (e.g. quarterly-plan, project-status, content-brief). This becomes the slash command name.

Wait for their answer. Validate: the name should be lowercase, use hyphens not spaces, and not clash with an existing command name (voice-installer, decide, brief, meetingprep, weeklyreview, amplify, new-capability, explore-idea, scope-decision, learnings, shipping-retro, teach-team, validate-idea, go-to-market, pricing-strategy, offer-creation, competitive-analysis, sop-builder, product-hunt-launch, changelog, positioning, roadmap, customer-feedback).

If there is a clash, tell them and ask for a different name.

## Step 3: Get the purpose

Ask:

> One sentence: what does this command do for the founder when they run it? This becomes the description in the command picker.

Wait for their answer.

## Step 4: Get the output

Ask:

> What file should this command write to? For example: `friday/your-file.md`. Every Friday command writes a real file -- it is how your config grows. If you are not sure, I will default to `friday/<name>.md`.

If they say they are not sure or skip this, default to `friday/<name>.md`.

## Step 5: Scaffold the command file

Check whether `commands/<name>.md` already exists in the current directory. If it does, ask:

> That file already exists. Do you want to overwrite it?

Wait for confirmation before proceeding.

Create `commands/` folder if it does not exist.

Write `commands/<name>.md` using this template, filling in `<name>`, `<description>`, and `<output-file>` from the answers above:

```
---
name: <name>
description: <description>
---
# /<name>

<description>

You, Claude, run the whole flow below in order, using your own file tools. Nothing phones home. Everything happens in this session.

## Step 1: Read the founder's voice profile (if it exists)

Check whether `friday/voice.md` exists in the current directory. If it does, read it and write all output in the founder's voice.

If `friday/voice.md` does not exist, write in a direct, plain style: short sentences, active voice, no hedging.

## Step 2: [Your first step here]

[Describe what Claude does in this step. Ask a question, read a file, or take an action.]

## Step 3: [Your next step here]

[Add as many steps as you need. Keep each step focused on one thing.]

## Step 4: Write the output

Write the result to `<output-file>` in the current directory. Create the `friday/` folder if it does not exist.

After writing, print:

> Output saved to `<output-file>`. Your config is growing.

## What this builds toward

[One or two sentences on how this fits into the founder's wider Friday config.]

---

Built by Amplify AI at amplifyais.com
```

## Step 6: Write or refresh the skill-writing playbook

Check whether `docs/skill-writing-playbook.md` exists in the current directory.

If it does not exist, create the `docs/` folder if needed and write `docs/skill-writing-playbook.md`. This is a static reference doc, not specific to any one command, so write it once and leave it alone on later runs unless the founder asks you to update it.

Use this content:

```
# Skill-Writing Playbook

Notes for writing your own Friday Foundation commands, so they stay useful instead of rotting into an unreliable mess. Every command you scaffold with `/new-capability` should be checked against the five failure modes below before you consider it done.

## The five failure modes

**Premature completion.** A step ends before the work is actually finished, because the model's attention slipped to "looking done" instead of "being done." If a step in your command says "ask the founder for their priorities," Claude might take the first vague answer and move on. Fix it by giving the step a clear finish line: "ask for at least three priorities, and confirm they're done before moving on."

**Duplication.** The same instruction shows up in more than one place, worded slightly differently each time. This costs you twice: it's more to maintain, and it makes Claude unsure which version is authoritative. If two steps in your command both explain how to read the voice profile, collapse them into one.

**Sediment.** Old instructions pile up because adding a new caveat feels safe and deleting an old one feels risky. Every command that gets edited a dozen times without a clean-up pass ends up carrying dead weight: instructions for a case that no longer applies, or a step that was superseded by a later one but never removed. Read your command file end to end occasionally and cut what no longer earns its place.

**Sprawl.** The command is too long, even if every line still does something. A command that was supposed to take five minutes but now has fifteen steps, because you kept bolting new asks onto it, is sprawling. If a command has grown past what a founder can run in one sitting, split it into two commands rather than one long one.

**No-op.** An instruction that Claude was already going to do by default. Telling Claude to "be thorough" or "think carefully" changes nothing; it's not a real instruction, it's noise. Every line in your command should change what Claude actually does. If you can delete a sentence and nothing in the output would differ, delete it.

## The completion-criterion discipline

Every step in a Friday command should end with a way to tell "done" from "not done." Not a vague sense that the step is finished, a real check.

A weak step: "Ask the founder about their nine decisions."

A strong step: "Ask the founder to list their nine decisions. Accept at least five, and confirm they're done before moving on."

The strong version is checkable: you can point at the moment it's satisfied. Where it matters, make the criterion exhaustive too, not just "produce a summary" but "every priority from the founder's list is accounted for in the output." A vague completion criterion is where premature completion sneaks in.

## Using this with `/new-capability`

When you scaffold a new command, walk each step you write against this list:

1. Does every step have a checkable finish line?
2. Does any instruction say the same thing a different step already said?
3. Is there a caveat left over from an earlier version of the command that no longer applies?
4. Could this command be split into two shorter, more focused ones?
5. Is every sentence actually changing what Claude does, or just restating what it would do anyway?

A command that passes all five stays reliable the tenth time you run it, not just the first.

---

Built by Amplify AI at amplifyais.com
```

If `docs/skill-writing-playbook.md` already exists, leave it as-is and skip straight to Step 7.

## Step 7: Confirm

After writing the file, print:

> Scaffolded `commands/<name>.md`. Open it and fill in Step 2 and Step 3 with your logic.
>
> `docs/skill-writing-playbook.md` has the five failure modes worth checking your new command against before you consider it done.
>
> When you are ready to test it, copy it to `~/.claude/commands/<name>.md` and run `/<name>` in a new Claude Code session.

Then add a note:

> To install it permanently via install.sh, add an entry to the PACK_COMMANDS list in `install.sh`.

## What this command is not

This scaffold gives you the structure. You fill in the content. The steps in `commands/<name>.md` are placeholders -- replace them with the actual flow you want Claude to follow.

For examples of well-built commands, read any of the existing commands in `commands/`.

---

Built by Amplify AI at amplifyais.com
