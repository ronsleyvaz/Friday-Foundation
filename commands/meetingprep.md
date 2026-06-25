---
name: meetingprep
description: Prepare for any meeting in five minutes. Ask for the person and purpose, produce a brief with context, the outcome you want, and three sharp questions. Writes to friday/meetings.md. Reads friday/voice.md if present and writes in your voice.
---
# /meetingprep

Walk into any meeting knowing exactly what you want from it. This command asks you for a name and what the meeting is about, then produces a sharp brief: what you know, the outcome you are after, and three questions worth asking. Written in your voice and saved to disk.

You, Claude, run the whole flow below in order, using your own file tools. There is no module to import and nothing to install.

## Step 1: Read the founder's voice profile (if it exists)

Check whether `friday/voice.md` exists in the current directory. If it does, read it.

From the profile, note:
- Their tone and rhythm.
- Their signature phrases.
- Their banned words list. You must not use any word on that list in any output from this command.

If `friday/voice.md` does not exist, write in a neutral, direct style: short sentences, no hedging, active voice.

## Step 2: Capture the meeting details

Ask the founder:

1. Who is the meeting with? Give the person's name and any context (their role, company, or how you know them).
2. What is the meeting about? One or two sentences on the type of meeting and the topic.

Wait for their input before proceeding. You do not have access to their calendar or contact list. Everything comes from what they paste in.

## Step 3: Produce the meeting brief

Write a brief with three sections. Use the founder's voice throughout.

Format:

```
## Meeting Brief: <person name> - <YYYY-MM-DD>

### What you know

<Two or three sentences on this person and the context of the meeting. Draw from what the founder gave you. If they gave thin context, say so plainly and note what would be useful to know before walking in.>

### The outcome you want

<One clear sentence. Name the one thing that would make this meeting a win. Not a vague intention. A specific outcome: a decision made, a next step agreed, a number confirmed.>

### Three questions to ask

1. <Question one. Sharp and specific. Opens something or advances the outcome.>
2. <Question two. Different angle. Not a version of question one.>
3. <Question three. The one you would ask if you only had sixty seconds left.>
```

Do not pad the questions. Three is the number. Each one should earn its place.

## Step 4: Save the brief

Append the full brief to `friday/meetings.md` in the current directory. Create the file if it does not exist. Create the `friday/` folder if it does not exist.

Use this exact format when appending:

```
---

<the full brief from Step 3>
```

After writing, print:

- Brief saved to `friday/meetings.md`.

## What this does not do

This command does not connect to your calendar. It does not pull contact data from your CRM. It does not read previous meeting notes automatically.

You bring the context. The brief gives it structure.

The full stack is Friday at friday.amplifyais.com. Calendar synced, contacts pulled, past notes surfaced before you walk in.

---

Built by Amplify AI at amplifyais.com
