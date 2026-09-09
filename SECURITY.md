# Security Policy

## Scope

Friday Shortcuts is a set of Claude Code slash commands and a bash installer. It:

- Collects usage events: which command you ran (or `custom` if it is your own), whether the run's output file was written, your Shortcuts version, your operating system, your country, and a short hash of your Claude Code session ID so a command can be paired with its output file. Tied to your signup if you came through friday.amplifyais.com.
- Makes one small network request per command run and per output file write, plus one at install time. All three go only to friday.amplifyais.com.
- Stores no credentials or API keys.
- Connects only to friday.amplifyais.com for usage reporting; every other network call is `install.sh` fetching from GitHub.

Commands run locally inside Claude Code. All output is written to files on your own machine. See `friday/usage-sent.jsonl` for the exact record of every usage message this install has sent.

## What to report

Report a security issue if you find:

- install.sh downloading content from an untrusted source.
- A command that leaks environment variables or credentials into a file.
- A harness doc that encourages an insecure practice.
- A dependency introduced without disclosure.

## How to report

Report a sensitive vulnerability privately, not in a public issue.

- **Preferred:** open the repository's **Security** tab and choose **Report a vulnerability**. This opens a private advisory that only the maintainers can see.
- **If that option is not visible:** open a public issue containing only `security: request private contact` with no details, and a maintainer will follow up privately.

Once you have a private channel, include:

1. A short description of the issue.
2. Steps to reproduce.
3. The file or line where the issue appears.

Do not post proof-of-concept or exploit code in a public issue. For a non-sensitive issue, open a normal GitHub issue with the label `security` and include the same three details.

## Response

We aim to respond within 5 business days and to publish a fix within 14 days of confirmation.

## What is not in scope

- Social engineering.
- Issues in Claude Code itself (report those to Anthropic).
- Issues that require physical access to the machine.

---

Built by Amplify AI at amplifyais.com
