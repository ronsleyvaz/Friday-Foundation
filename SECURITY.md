# Security Policy

## Scope

Friday Foundation is a set of Claude Code slash commands and a bash installer. It:

- Does not collect data.
- Does not make network requests at runtime (only during install.sh).
- Does not store credentials or API keys.
- Does not connect to any external service.

Commands run locally inside Claude Code. All output is written to files on your own machine.

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
