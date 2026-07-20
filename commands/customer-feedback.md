---
name: customer-feedback
description: Synthesize pasted customer feedback or sanitized local notes into recurring themes, supporting evidence, contradictions, unanswered questions, and prioritized actions. Writes friday/customer-feedback.md. Reads friday/voice.md if present and writes in your voice.
---
# /customer-feedback

Customer feedback gets noisy fast. This command turns scattered notes into a grounded synthesis: what people keep saying, what evidence supports it, what contradicts it, what is still unknown, and what to do next.

You, Claude, run the whole flow below in order, using your own file tools. There is no module to import, no database, and no network call.

## Step 1: Read the founder's voice profile (if it exists)

Check whether `friday/voice.md` exists in the current directory. If it does, read it and write all output in the founder's voice.

If `friday/voice.md` does not exist, write in a direct, plain style: short sentences, active voice, no hedging.

## Step 2: Collect the feedback source

Ask the founder:

> Paste the customer feedback you want synthesized, or give me paths to sanitized local Markdown or text files. Include only material you are comfortable storing in `friday/customer-feedback.md`.

Wait for their answer.

If they paste feedback directly, use only that pasted text.

If they provide file paths, read only `.md`, `.markdown`, or `.txt` files they explicitly named. If a path looks like a secret, credential, private key, environment file, token dump, browser export, cookie store, or unrelated personal data, refuse to read it and ask for a sanitized text file instead.

If they provide no usable feedback, ask for pasted notes or sanitized file paths before continuing.

## Step 3: Extract evidence without inventing anything

Work from the feedback text only. Do not fabricate quotes, customer counts, sentiment, dates, names, company names, feature requests, or severity.

When you quote a customer, copy only short, exact snippets from the supplied feedback. If the source is paraphrased notes rather than direct quotes, label the evidence as notes, not quotes.

If the feedback does not support a claim, mark it as unknown rather than filling the gap with a plausible answer.

## Step 4: Synthesize the patterns

Group the feedback into recurring themes. For each theme, include:

- What customers are saying
- Supporting evidence from the supplied material
- Counterexamples or contradictions
- Who seems affected, only when the supplied feedback says so
- How confident the theme is, based on the volume and consistency of supplied evidence

Keep one-off comments separate from recurring themes. Do not inflate a single comment into a trend.

## Step 5: Identify unanswered questions

List the questions the feedback raises but does not answer. Include questions about missing segments, unclear causes, unknown frequency, unclear willingness to pay, implementation risk, and whether the loudest feedback is representative.

Do not answer those questions unless the supplied feedback already contains the answer.

## Step 6: Prioritize actions

Turn the synthesis into a short action list. Prioritize actions using:

- Evidence strength
- Customer or revenue impact stated in the supplied feedback
- Reversibility
- Effort or risk, if the feedback mentions it

Separate actions into:

- Do now
- Test next
- Watch
- Do not act on yet

Every action must point back to a theme, evidence item, contradiction, or unanswered question from the synthesis.

## Step 7: Write the customer feedback synthesis

Create the `friday/` folder if it does not exist. Write the result to `friday/customer-feedback.md`. If the file already exists, overwrite it with this run's synthesis.

Use this structure:

```
# Customer Feedback: <YYYY-MM-DD>

## Source

<Pasted notes or named sanitized files used. Do not include private file paths if the founder asked you not to.>

## Executive summary

<Three to five grounded bullets. No invented counts or sentiment.>

## Recurring themes

### <Theme name>

What customers are saying: <summary>
Evidence: <short exact snippets or clearly labelled notes>
Counterexamples or contradictions: <what pushes against the theme, or "None found in the supplied feedback.">
Affected segment: <only if supplied, otherwise "Unknown">
Confidence: <High, medium, or low, with a reason tied to the supplied material>

<Repeat for each recurring theme.>

## One-off signals

<Comments that matter but do not repeat enough to call a theme.>

## Unanswered questions

<Questions the founder should resolve before making bigger decisions.>

## Prioritized actions

### Do now

<Actions tied to strong evidence.>

### Test next

<Actions that need a small experiment.>

### Watch

<Signals worth monitoring.>

### Do not act on yet

<Requests or ideas with too little evidence, too much contradiction, or unclear impact.>
```

After writing, print:

> Customer feedback synthesis saved to `friday/customer-feedback.md`. Your config is growing.

## What this does not do

This command does not scrape support tools, analytics, reviews, CRM records, or live customer data. It works from pasted feedback or sanitized local files the founder explicitly provides.

It does not turn every comment into a product requirement. A useful synthesis keeps weak signals weak until real evidence supports them.

## What this builds toward

`friday/customer-feedback.md` gives founders a durable evidence base for product, messaging, sales, and support decisions. Re-run it whenever a meaningful batch of new feedback comes in.

The full stack is Friday at friday.amplifyais.com. Nine specialists, running against your real inbox, calendar, and tasks every morning before you are up.

---

Built by Amplify AI at amplifyais.com
