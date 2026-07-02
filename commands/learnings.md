---
name: learnings
description: Review, search, and prune what Friday has learned about your business. First run creates friday/learnings.md with a starter structure. Later runs let you review, search by keyword, and mark entries for removal. Plain markdown, no database.
---
# /learnings

Config that never gets reviewed rots. This command keeps `friday/learnings.md` honest: a plain log of patterns, preferences, and pitfalls you want Friday to remember about your business, that you can review, search, and prune whenever it's due for a clean-up.

You, Claude, run the whole flow below in order, using your own file tools. There is no module to import, no database, and nothing to install. Everything lives in one markdown file.

## Step 1: Read the founder's voice profile (if it exists)

Check whether `friday/voice.md` exists in the current directory. If it does, read it and write all output in the founder's voice.

If `friday/voice.md` does not exist, write in a direct, plain style: short sentences, active voice, no hedging.

## Step 2: Check for an existing learnings file

Check whether `friday/learnings.md` exists in the current directory.

**If it does not exist,** this is a first run. Go to Step 3 (first-run setup).

**If it exists,** read it. Go to Step 4 (review, search, or prune).

## Step 3: First-run setup

Tell the founder:

> No learnings file yet. This is where Friday keeps a running log of patterns, preferences, and pitfalls about how you run your business, things worth remembering so they don't have to be re-explained every time. Let's start it with one real entry. What's one thing you'd want remembered? Could be a preference ("I never schedule client calls before 10am"), a pattern ("Q4 leads convert slower, don't panic about it"), or a pitfall ("the old CRM export drops phone numbers, always double check").

Wait for their answer.

Create `friday/` folder if it does not exist. Write `friday/learnings.md` with this starter structure, filling in the founder's first entry:

```
# Learnings

A running log of patterns, preferences, and pitfalls about how this business runs.
Reviewed and pruned with /learnings. Stale or contradicted entries get removed,
not left to rot.

## Patterns

<If the founder's first entry was a pattern, put it here as "- <entry> (added YYYY-MM-DD)". Otherwise leave this section with no entries yet.>

## Preferences

<If the founder's first entry was a preference, put it here the same way. Otherwise leave empty.>

## Pitfalls

<If the founder's first entry was a pitfall, put it here the same way. Otherwise leave empty.>

Last updated: <YYYY-MM-DD>
```

After writing, print:

> `friday/learnings.md` created with your first entry. Run `/learnings` again any time to add more, search, or prune what's gone stale.

Stop here for a first run. Do not continue to Step 4.

## Step 4: Review, search, or prune

Ask the founder what they want to do:

> What do you want to do with your learnings?
>
> A) Review everything, show me the full list
> B) Search, find entries about a specific topic
> C) Add a new entry
> D) Prune, help me find and remove entries that are stale or no longer true

Wait for their answer.

**If A (Review):** Print the full contents of `friday/learnings.md`, organized by section (Patterns, Preferences, Pitfalls). If any section is empty, say so plainly rather than skipping it silently.

**If B (Search):** Ask for a keyword. Search the file's entries for that keyword (case-insensitive substring match across all three sections). Show matching entries with their section. If nothing matches, say so and ask if they want to add a new entry instead.

**If C (Add):** Ask what the new entry is and which category it belongs in (pattern, preference, or pitfall). Append it to the matching section in the format `- <entry> (added YYYY-MM-DD)`. Confirm what was added.

**If D (Prune):** Walk through the existing entries one at a time. For each one, ask: is this still true? Is it still useful? If the founder says no to either, remove it. If they say it needs updating, ask for the corrected version and replace it in place rather than leaving both the old and new versions in the file. Keep going until every entry has been checked or the founder says to stop.

## Step 5: Write the update

After any add, edit, or prune, write the updated content back to `friday/learnings.md`. Update the `Last updated:` line to today's date.

Print:

> `friday/learnings.md` updated. Your config is growing, and staying honest.

## What this does not do

This command does not run in the background, does not auto-detect patterns from your other files, and does not maintain a database. It is one markdown file, and you decide what goes in it and what gets pruned.

## What this builds toward

`friday/learnings.md` compounds the longer you keep it honest. A file full of stale, contradicted, or half-true entries is worse than no file at all, which is why pruning is a first-class option here, not an afterthought.

The full stack is Friday at friday.amplifyais.com. Nine specialists, running against your real inbox, calendar, and tasks every morning before you are up.

---

Built by Amplify AI at amplifyais.com
