---
name: voice-installer
description: Build your voice profile. Interviews you, reads your writing samples, writes friday/voice.md plus a voice block in CLAUDE.md, then rewrites a sample paragraph in your voice. Self-contained, no dependencies.
audience: external-general
skadoosh:
  shape: copy-paste-template
  action: "Run /voice-installer in Claude Code to write your voice profile to disk right now."
---
<!-- audience: external-general -->
# /voice-installer

Build your voice profile in five minutes. This command interviews you, reads two or three pieces of your writing, and writes a real voice config to your machine. Every AI tool you use will start sounding like you instead of ChatGPT.

You, Claude, run the whole flow below in order, using your own file tools. There is no module to import and nothing to install. Everything happens in this session.

## Step 1: Interview

Ask these five questions ONE AT A TIME. Wait for each answer before asking the next. Keep your own wording warm and short.

1. What name should your voice profile be saved under?
2. What do you do, in one line?
3. In three words, how would a reader describe your writing? For example: direct, warm, blunt.
4. What are two or three phrases you reach for often? These are your signature phrases.
5. Any words you never want to see in your writing? These get added to the standard banned list below.

## Step 2: Read the writing samples

Ask the founder for two or three file paths to things they have written, as plain `.txt` or `.md`. Old emails, posts, drafts. Anything they wrote, not AI-drafted. Read each file.

From the samples, work out, by counting and not guessing:

- Average sentence length in words.
- Sentence openers and phrases they actually repeat.
- Whether they run short and direct or long and layered.

## Step 3: Write friday/voice.md

Create a `friday/` folder in the current directory if it does not exist. Write `friday/voice.md` in exactly this shape:

```
# Voice Profile: <name>

## Who
<their one-line role>

## Tone
<their three words>

## Rhythm
Average sentence length in their samples: <N> words. Match it. Shorter is clearer.

## Signature phrases
- <phrase>
- <phrase>

## Banned words
Never write these. They are borrowed words that make any writer sound like everyone else.

delve, tapestry, leverage, robust, seamless, foster, realm, elevate, underscore,
plethora, myriad, holistic, synergy, cornerstone, paramount, pivotal, nuanced,
multifaceted, "a game-changer", "unlock the power"
<plus their own banned words>

## Use this anywhere
Paste this profile into any AI tool before you ask it to write. It will match your voice.
```

Fill every `<...>` from the interview and the samples. Keep the banned-words block as a plain list.

## Step 4: Append a voice block to CLAUDE.md

Add a short voice block to the `CLAUDE.md` in the current directory. Wrap it in these exact sentinel comments so it can be updated cleanly:

```
<!-- FRIDAY-VOICE-START -->
## Voice
Write as <name>. Tone: <three words>. Average sentence length around <N> words.
Signature phrases: <phrases>. Never use the banned words listed in friday/voice.md.
<!-- FRIDAY-VOICE-END -->
```

If a block between those sentinels already exists, replace it. Do not add a second one. If `CLAUDE.md` does not exist, create it with this block.

## Step 5: The proof (live rewrite)

Take this sample of default AI copy:

```
AI can help your business transform and create scalable solutions for your
customers. We leverage synergy to foster robust outcomes.
```

Show it under a heading "Before". Then rewrite the same paragraph using the voice profile you just wrote, obeying the tone, rhythm, signature phrases, and banned words. Show your rewrite under a heading "After".

This is a live rewrite, not a word-swap. You have the founder's name, tone, phrases, and banned words. Use them. The before and the after, side by side, are the proof.

## Step 6: Close

Print these two lines:

- Your voice profile is at `friday/voice.md`. Open it, read it, add to it any time.
- This is brick 1 of your `friday/` config. The next brick appends to the same folder.

## What comes next

The full stack, nine specialists wired together and connected to your inbox and calendar, is Friday, the paid product at friday.amplifyais.com. This is what one capability feels like by hand.

---

Built by Amplify AI at amplifyais.com
