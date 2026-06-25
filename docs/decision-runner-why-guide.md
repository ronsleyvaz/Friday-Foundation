# Why Most Decisions Stay Open (and How to Close Them in Five Minutes)

Founders do not fail at decisions because they lack information. They fail because they mistake thinking about a decision for making one. The decision stays open. The window closes. The default wins.

The Decision Runner ends that pattern. Paste your decision, get a structured analysis, walk away with one recommendation and a record on disk.

---

## What the 1-3-1 protocol is

1-3-1 is a decision-making protocol developed for Friday, the AI Chief of Staff.

The structure is simple: one problem, three options, one pick.

**One problem.** State what must be decided, what is at stake, and what is driving the timing. Most decision paralysis comes from treating the symptom as the decision. Naming the real problem is half the work.

**Three options.** Generate exactly three. Not two (false dilemma), not seven (paralysis). Three forces you to look past the obvious pair and find the alternative you were not considering. Each option gets one upside and one risk, side by side, so you see the trade-offs at a glance.

**One pick.** The recommendation names which option wins and why the others did not make the cut. This is not a hedge. This is a call.

The protocol was built for Friday because a Chief of Staff who presents three options and asks "what do you think?" has done less than half the job. The job is to present one recommendation with reasoning the founder can accept or override. That is what the Decision Runner gives you.

---

## Why three options and not two

Two options is a false dilemma. Your brain treats it as a coin flip and the default usually wins.

Seven options is analysis that never ends.

Three forces you off the obvious pair. In practice, Option C is almost always the one that solves the actual problem instead of the stated one. If you find Option C is what you choose most often, the protocol is working.

---

## Why writing it down matters

Most decisions disappear after they are made. Six months later you cannot remember why you chose what you chose, which means you relitigate the same question when a similar situation comes up.

The Decision Runner writes every decision to `friday/decisions.md`. That file is a record. Not a journal, not notes. A record: what the decision was, what the options were, what you chose, and why the others did not win.

Over time, `friday/decisions.md` becomes one of the most useful files on your machine. You start to see patterns in what you choose and why. You stop relitigating old decisions. And when you hand something off to a team member or a future AI tool, the record is already there.

---

## How the voice profile connects

If you have already run the Voice Installer, your voice profile lives at `friday/voice.md`. The Decision Runner reads it before writing a single line.

That means the problem statement, the three options, and the recommendation all come out in your voice: your rhythm, your phrasing, and nothing from your banned-words list. The analysis sounds like you thought it through, not like a consulting report.

If you have not run the Voice Installer yet, the Decision Runner still works. It writes in a neutral, direct style. The voice comes after.

---

## What this is not

The Decision Runner does not connect to your inbox. It does not read your calendar. It does not know what is in your Notion or your CRM. If the decision requires that context, it will ask you to paste it in.

That is by design. This capability works by hand. You give it the context. It gives you the structure and the recommendation.

The full stack, nine specialists wired together and running against your real data, is Friday. When you hit the wall where the context it needs is live in your systems, that is the moment the upgrade makes sense.

---

## The growing config

Every capability you install adds a file to your `friday/` folder.

The Voice Installer added `voice.md`. The Decision Runner appends to `decisions.md`. Each time you run `/decide`, that file gets one more entry.

The folder is the proof that your config is growing. Not a product promise. A real file on your machine.

---

## Run it now

You need Claude Code installed and open. If you do not have it yet: https://docs.anthropic.com/claude-code

```
curl -fsSL https://raw.githubusercontent.com/ronsleyvaz/Friday-for-Claude-Code/main/install.sh | bash -s -- decide
```

Then in Claude Code:

```
/decide
```

Paste your decision and two lines of context. The rest takes thirty seconds.

---

Built by Amplify AI at amplifyais.com
