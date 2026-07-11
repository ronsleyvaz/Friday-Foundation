# 02 - Add an Agent

Commands are interactive. Agents are autonomous specialists.

Use a command when you want to run a guided flow yourself, step by step. Use an agent when you want Claude to go off and do a body of work -- deep research, a multi-file build, a long content project -- without you staying in the loop for each step.

---

## When to use an agent instead of a command

Agents are the right choice when:

- The work takes more than 30 minutes.
- The work is in a specific domain that needs different rules or a different model.
- You want to run it in parallel with other work.
- You want a specialist that stays focused on one thing (brand, research, operations) rather than a generalist.

Commands are the right choice when:

- The work is interactive (you answer questions, Claude acts, you see the result).
- The work is short (under 30 minutes).
- You want to stay in the loop for every decision.

---

## The agent file format

Agents live in `.claude/agents/` in your project directory (not in the global Claude config). Each agent is a markdown file with frontmatter.

```
---
name: agent-name
description: One line description. The router uses this to pick the agent.
model: claude-haiku-4-5-20251001
tools:
  - Read
  - Write
  - Bash
---

# Agent name

[System prompt here. Write this like you are briefing a specialist colleague on their job.]

## Your job

[What the agent does and does not do.]

## Voice

[How the agent writes. Match this to your CLAUDE.md voice profile.]

## Done criteria

[How the agent signals it is finished. What file does it write? What does it print?]
```

---

## Model selection

Pick the smallest model that does the job:

- **Haiku** for routine, fast, repetitive tasks (summarising, formatting, categorising).
- **Sonnet** for complex reasoning, writing, and multi-step plans.
- **Opus** for critical decisions, high-stakes drafts, and anything you would not send to a junior.

Haiku is faster and cheaper. Start there.

---

## A minimal working agent

Create `.claude/agents/researcher.md` in your project:

```
---
name: researcher
description: Web research agent. Use for fact-finding, competitive analysis, and source gathering.
model: claude-haiku-4-5-20251001
tools:
  - WebSearch
  - WebFetch
  - Write
---

# researcher

You do research. You find facts. You write a short report with sources.

## Your job

When given a question, search the web, read the top results, and write a 200-word summary with three bullet points and source links to `friday/research-[topic].md`.

## Done criteria

You are done when the file exists and has sources.
```

Save it. In Claude Code, type: `Use the researcher agent to find the top three AI scheduling tools for founders.`

Claude routes the task to the specialist agent.

---

## Keeping track

When you add a new agent, keep a note wherever you track your setup so you remember what you have built. There is no special file Claude Code reads for this; the agent works the moment its file is saved.

---

Next: [03 - Connect Your Own Tools](03-connect-your-own-tools.md)
