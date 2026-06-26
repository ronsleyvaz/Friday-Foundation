---
name: new-capability
description: Scaffold a new Friday command from a template. Prompts for a name and description, writes commands/<name>.md with the correct frontmatter and step structure, ready for you to fill in.
---
# /new-capability

Build a new Friday command from scratch. This command prompts you for a name and a purpose, then scaffolds `commands/<name>.md` with the right frontmatter and structure. You fill in the steps.

You, Claude, run the whole flow below in order, using your own file tools. Nothing phones home. Everything happens in this session.

## Step 1: Get the command name

Ask the founder:

> What do you want to call this command? Give me a short kebab-case name (e.g. quarterly-plan, project-status, content-brief). This becomes the slash command name.

Wait for their answer. Validate: the name should be lowercase, use hyphens not spaces, and not clash with an existing command name (voice-installer, decide, brief, meetingprep, weeklyreview, amplify, new-capability).

If there is a clash, tell them and ask for a different name.

## Step 2: Get the purpose

Ask:

> One sentence: what does this command do for the founder when they run it? This becomes the description in the command picker.

Wait for their answer.

## Step 3: Get the output

Ask:

> What file should this command write to? For example: `friday/your-file.md`. Every Friday command writes a real file -- it is how your config grows. If you are not sure, I will default to `friday/<name>.md`.

If they say they are not sure or skip this, default to `friday/<name>.md`.

## Step 4: Scaffold the command file

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

## Step 5: Confirm

After writing the file, print:

> Scaffolded `commands/<name>.md`. Open it and fill in Step 2 and Step 3 with your logic.
>
> When you are ready to test it, copy it to `~/.claude/commands/<name>.md` and run `/<name>` in a new Claude Code session.

Then add a note:

> To install it permanently via install.sh, add an entry to the PACK_COMMANDS list in `install.sh`.

## What this command is not

This scaffold gives you the structure. You fill in the content. The steps in `commands/<name>.md` are placeholders -- replace them with the actual flow you want Claude to follow.

For examples of well-built commands, read any of the existing commands in `commands/`.

---

Built by Amplify AI at amplifyais.com
