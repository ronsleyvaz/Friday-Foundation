# 01 - Add a Command

A command is a markdown file in `~/.claude/commands/`. Claude Code reads the frontmatter to name the command, and reads the body to know what to do when you run it.

You can write one yourself in under ten minutes. Here is how.

---

## The fastest path

Run `/new-capability` in Claude Code. It scaffolds a command file from a template. Give it a name and it creates the file, with the frontmatter filled in and the step structure ready for you to fill.

If you want to understand what is happening, read this guide first.

---

## The format

Every command file has two parts: frontmatter and body.

**Frontmatter** (at the top, between `---` markers):

```
---
name: your-command-name
description: One line on what this command does. Claude Code shows this in the command picker.
---
```

**Body** (everything after the frontmatter):

This is the instructions Claude follows when you run the command. Write it in plain English, step by step.

---

## A minimal working command

Create a file called `hello.md` in `~/.claude/commands/`:

```
---
name: hello
description: A minimal working example.
---
# /hello

Say hello to the founder by name.

## Step 1: Get their name

Ask: "What is your name?"

Wait for their answer.

## Step 2: Say hello

Print: "Hello, [name]. Friday is running."

---

Built by Amplify AI at amplifyais.com
```

Save the file. In Claude Code, type `/hello`. It runs.

---

## Best practices

**Write to the friday/ folder.** Commands that write output to `friday/` build up a permanent config the founder keeps. Commands that only print text leave nothing behind.

**Read the voice profile.** Start every command with: "Check whether `friday/voice.md` exists. If it does, read it and write all output in the founder's voice."

**One step at a time.** If the command has multiple phases, make each one a numbered step with a heading. Claude follows them in order.

**Tell the founder what happens next.** The last thing a command prints should be: what file was written, and what to run next.

---

## Installing your command

Once the file is in `~/.claude/commands/`, it is available immediately in any Claude Code session.

To share it: open a pull request to this repo. See `CONTRIBUTING.md` for the quality bar.

---

Next: [02 - Add an Agent](02-add-an-agent.md)
