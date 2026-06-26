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

Open a GitHub issue with the label `security`. Include:

1. A short description of the issue.
2. Steps to reproduce.
3. The file or line where the issue appears.

Do not include exploits or proof-of-concept attack code in public issues. If the issue is sensitive, email amplifyais.com directly.

## Response

We aim to respond within 5 business days and to publish a fix within 14 days of confirmation.

## What is not in scope

- Social engineering.
- Issues in Claude Code itself (report those to Anthropic).
- Issues that require physical access to the machine.

---

Built by Amplify AI at amplifyais.com
