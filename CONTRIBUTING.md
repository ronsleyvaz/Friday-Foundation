# Contributing to Friday Foundation

Thank you for building here.

Friday Foundation is an open-source founder harness built on top of Claude Code. Contributions are welcome. Here is what you need to know before you open a pull request.

## Ship your first command

Scaffolding a command takes about ten minutes with `/new-capability`; polishing it into something you would ship usually takes an hour or two, which matches the estimate on each good first issue.

The fastest way in is to pick a [good first issue](https://github.com/ronsleyvaz/Friday-Foundation/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) and build the command it describes.

**Claim it first.** Comment on the issue to say you are taking it, and a maintainer assigns it to you. If an issue is already assigned or already has a claim comment, pick another one so two people never build the same command.

1. Fork the repo and clone your fork.
2. Copy an existing command that is close to what you want as your model. `commands/weeklyreview.md` and `commands/meetingprep.md` are short, readable examples.
3. Save it as `commands/<your-command>.md`. Fill in the frontmatter name and description, then write the steps: one thing at a time, file tools only, no imports. It should read `friday/voice.md` if it exists and write its output into the `friday/` folder.
4. Register it in the installer: add a line to the `PACK_COMMANDS` array in `install.sh`. The catalog parity tests then check that the command also appears everywhere else it is listed: the installer's usage and completion output, the README and manual tables, the command-count lines, and `new-capability.md`'s reserved-name list. They go red and name each place that is still out of sync, so you know exactly what to update.
5. Add a test in `tests/` that checks your command's frontmatter and structure. Copy the shape of an existing test in `test_commands.py`.
6. Run `python3 -m pytest tests/` and confirm green.
7. Open a pull request against `main`. CI runs the full suite on your PR, so you see green or red before a maintainer reviews. Your very first PR may need a one-click maintainer approval before CI starts; after that it runs automatically.

That is the whole loop. The sections below have the detail.

## Setting up your environment

You need Python 3 and Claude Code. Install the one dev dependency (pytest) and run the suite from the repo root:

```
python3 -m pip install -r requirements-dev.txt
python3 -m pytest tests/
```

If your system Python is externally managed and the install errors, create a virtual environment first with `python3 -m venv .venv && source .venv/bin/activate`, then re-run the install.

pytest is the only dev dependency. The tests themselves import only the Python standard library, and the shipped command pack has zero runtime dependencies beyond Claude Code. On Windows, run these from WSL or Git Bash so the bash installer and shell tests behave.

## What belongs here

- New slash commands that help founders get leverage from Claude Code.
- Improvements to the harness guide docs (clearer steps, better examples).
- Bug fixes to install.sh (cross-platform issues, edge cases).
- New why-guides that explain the reasoning behind a capability.
- Tests that prove a new command works end to end.

## What does not belong here

- Commands that are project-specific or only useful to one person.
- Content that includes proprietary IP, credentials, or personal data.
- Runtime dependencies beyond Claude Code. The shipped pack has none. (pytest is a dev-only dependency for the test suite, listed in `requirements-dev.txt`.)

## How to submit a command

1. Copy `commands/new-capability.md` as your starting point.
2. Fill in the frontmatter (name and description).
3. Write the steps the way the existing commands do: one thing at a time, file tools only, no imports.
4. Register it in `PACK_COMMANDS` in `install.sh`. The catalog parity tests then require it in every other place a command is listed (the README and manual tables, the installer's output, the command counts, and `new-capability.md`'s reserved-name list) and name any you miss.
5. Add a test in `tests/` that validates the frontmatter and content.
6. Run `python3 -m pytest tests/` and confirm green before submitting.
7. Open a pull request against `main`. Use the issue template if you are proposing something new before building it.

## Command quality bar

A command is ready when:

- It produces a real file output (not just printed text).
- It works on a clean machine with only Claude Code installed.
- It reads `friday/voice.md` if it exists and writes in the founder's voice.
- It writes only its own output into the `friday/` folder and never overwrites unrelated files.
- It has no em dashes in the text.
- It tells the founder what to do next after it runs.

## Code style (install.sh and tests)

- Shell: bash, `set -euo pipefail`, POSIX-compatible where possible.
- Python tests: pytest, no external dependencies beyond the stdlib.
- No environment assumptions except that `bash` and `python3` are on the PATH.

## Releasing

`main` is the integration branch; the installer distributes from `release`.
See `RELEASING.md` for how a maintainer promotes a batch of merged pull
requests to `release`.

## Getting credit

When your command is merged, add a line for yourself under Contributors in `CREDITS.md`. Foundation credits the people who build it. That is the honest version of open source.

## Licence

All contributions are MIT licensed. By opening a pull request, you agree your contribution ships under the MIT `LICENSE`.

Three files carry the separate `LICENSE-CONTENT` licence instead: `commands/amplify.md`, `harness/05-the-amplify-logic.md`, and `docs/why-guides/amplify-why-guide.md`. These are maintainer-owned. A pull request must not add files to that list, remove the content-licence header from them, or change the terms in `LICENSE-CONTENT`.

---

Built by Amplify AI at amplifyais.com
