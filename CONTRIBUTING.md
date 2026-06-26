# Contributing to Friday Foundation

Thank you for building here.

Friday Foundation is an open-source founder harness built on top of Claude Code. Contributions are welcome. Here is what you need to know before you open a pull request.

## What belongs here

- New slash commands that help founders get leverage from Claude Code.
- Improvements to the harness guide docs (clearer steps, better examples).
- Bug fixes to install.sh (cross-platform issues, edge cases).
- New why-guides that explain the reasoning behind a capability.
- Tests that prove a new command works end to end.

## What does not belong here

- Commands that are project-specific or only useful to one person.
- Content that includes proprietary IP, credentials, or personal data.
- Dependencies beyond bash and Claude Code. The harness has none.

## How to submit a command

1. Copy `commands/new-capability.md` as your starting point.
2. Fill in the frontmatter (name and description).
3. Write the steps the way the existing commands do: one thing at a time, file tools only, no imports.
4. Add a test in `tests/` that validates the frontmatter and content.
5. Run `python -m pytest tests/` and confirm green before submitting.
6. Open a pull request against `main`. Use the issue template if you are proposing something new before building it.

## Command quality bar

A command is ready when:

- It produces a real file output (not just printed text).
- It works on a clean machine with only Claude Code installed.
- It reads `friday/voice.md` if it exists and writes in the founder's voice.
- It appends to the `friday/` folder rather than overwriting unrelated files.
- It has no em dashes in the text.
- It tells the founder what to do next after it runs.

## Code style (install.sh and tests)

- Shell: bash, `set -euo pipefail`, POSIX-compatible where possible.
- Python tests: pytest, no external dependencies beyond the stdlib.
- No environment assumptions except that `bash` and `python3` are on the PATH.

## Licence

By contributing, you agree that your contribution is licensed under MIT (for code) or the content licence in `LICENSE-CONTENT` (for framework-derived content). See those files for terms.

---

Built by Amplify AI at amplifyais.com
