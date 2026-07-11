# 03 - Connect Your Own Tools

Friday Foundation ships with no external connections. That is intentional. You own the stack and you add connections yourself.

This guide explains the patterns for wiring your own tools.

---

## The three connection patterns

**Pattern 1: Read a file (no connection needed)**

The simplest integration. Your tool exports a file, your command reads it.

Example: your CRM lets you export a CSV of open deals. Put it in your project directory. Your command reads it.

```
Check whether `leads.csv` exists. If it does, read it and pull the top five open deals by value.
```

No API key. No connection. Just a file.

**Pattern 2: Use an MCP server**

Claude Code supports Model Context Protocol (MCP) servers. These are small servers that expose external tool APIs directly to Claude.

Official MCP servers exist for: GitHub, Slack, Linear, Notion, Google Calendar, Supabase, and more.

To add an MCP server, run `claude mcp add` from your terminal (run `claude mcp add --help` for the full syntax). You give it a name, a transport, and the server's URL or launch command:

```
claude mcp add --scope user --transport http <name> <server-url>
```

The `--scope` flag decides where the server is saved. `user` (all your projects) and the default `local` (this project only) both write to `~/.claude.json` in your home folder. `project` writes a `.mcp.json` file in the project root that you can commit and share with teammates. Then, in your command, reference the tool name the server exposes.

Your credentials stay on your machine. You configure the MCP server with your own API keys.

**Pattern 3: Shell commands in an agent**

If you give an agent the `Bash` tool, it can run shell commands. This lets you call any CLI tool: the GitHub CLI (`gh`), the Notion CLI, `curl`, or any script you have written.

Example agent step:

```
Run: gh issue list --limit 10 --json title,number,body
Read the output and write a summary to friday/open-issues.md.
```

---

## Adding your API keys

Never put API keys in command files or agent files. They are tracked by git.

The safe pattern:

1. Add your key to your shell environment: `export MY_API_KEY=...` in `~/.zshrc` or `~/.bashrc`.
2. Or add it to a `.env` file in your project directory and add `.env` to `.gitignore`.
3. In your agent, reference the key as an environment variable: `os.environ.get("MY_API_KEY")`.

Claude Code agents with the `Bash` tool can read environment variables set in the shell that launched Claude Code.

---

## Example: connecting Notion

1. Install the Notion MCP server. Follow: https://github.com/makenotion/notion-mcp-server
2. Add your Notion integration token to the MCP config (not to any tracked file).
3. In your command:

```
Use the Notion MCP tool to read the database with ID [your-database-id].
Write the open tasks to friday/tasks.md.
```

---

## What to avoid

- Do not hardcode API keys in command or agent files.
- Do not make a command require a connection that might not exist. Wrap connection steps with a fallback: "If the tool is not available, ask the founder to paste the data manually."
- Do not add MCP servers to the repo. They are personal config.

---

Next: [04 - The Friday Folder](04-the-friday-folder.md)
