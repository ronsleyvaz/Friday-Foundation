# The Five Minutes That Decide Every Meeting

The follow-up meeting exists because nobody named an outcome before the first one. The meeting ran long, the conversation drifted, and the result was another calendar invite. The problem is not the meeting. It is the five minutes before it.

The Meeting Prep command changes those five minutes.

---

## What the brief contains

Three things. No more.

**What you know.** A sharp read of the person and the context. Not a biography. Two or three sentences on who they are and why this meeting exists. If you know little, that is useful information too. Walking in aware of your blind spots beats walking in with assumed context.

**The outcome you want.** One sentence. Not a vague intention like "get on the same page" or "explore options." A specific outcome: a number confirmed, a decision made, a next step agreed. If you cannot name a specific outcome before the meeting, you are not ready for it.

**Three questions.** Not ten. Not a list of talking points. Three questions that advance the outcome. Each one earns its place or it does not go in.

That structure is deliberate. Walking in with a clear outcome and three sharp questions changes how you listen. You stop waiting for a gap to talk and start steering the conversation.

---

## Why three questions

A list of ten questions is a list of things you hope to cover. Three questions is a plan.

The first question opens the conversation. The second comes from a different angle. The third is the one you would ask if you only had sixty seconds left. Write the third question first and you will know immediately whether you understand what you actually need from this meeting.

---

## Why writing it down matters

The brief lives in `friday/meetings.md`. Over time that file becomes a meeting log: who you met, what you wanted from each one, what the context was.

Before any future meeting with the same person, read their entry. You will stop re-establishing context from scratch and start building on it.

---

## What the brief does not do

This command does not connect to your calendar. It does not pull contact data from your CRM. It does not read previous meeting notes.

You bring the context. The brief gives it structure.

The full stack is Friday at friday.amplifyais.com. Friday syncs your calendar, pulls contacts, and surfaces past meetings before you walk in.

---

## The growing config

Every capability you install adds a file to your `friday/` folder.

You now have your voice profile, your decision log, your nine recurring decisions, your morning brief, and this command starts your meeting log. Each file is real. Each one compounds.

---

## Run it now

You need Claude Code installed and open. If you do not have it yet: https://docs.anthropic.com/claude-code

```
curl -fsSL https://raw.githubusercontent.com/ronsleyvaz/Friday-for-Claude-Code/main/install.sh | bash -s -- meetingprep
```

Then in Claude Code:

```
/meetingprep
```

Give it a name and two sentences about the meeting. Walk in with a brief in two minutes.

---

Built by Amplify AI at amplifyais.com
