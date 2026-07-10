# Repository Guide for Coding Agents

This is the shared source of truth for agents working in this repository.
`CLAUDE.md` imports this file for Claude Code. Keep shared instructions here and
Claude-specific setup in `CLAUDE.md`; do not duplicate guidance between them.

## Read First

Read the relevant source documents before changing anything:

1. `README.md` for the product, audience, installation flow, and command list.
2. `CONTRIBUTING.md` for contribution scope, command quality, and code style.
3. `SECURITY.md` for the local-only security model.
4. `RELEASING.md` for the `main` to `release` promotion flow.
5. `LICENSE` and `LICENSE-CONTENT` before changing licensed material.
6. The tests covering the area you will edit.

When these documents disagree, stop and report the conflict. Do not silently
choose one.

## Project and Audience

Friday Foundation is a free, local-first AI Chief of Staff configuration for
Claude Code. It serves founders, solo operators, and small teams who want
guided help with decisions, planning, meetings, growth, launches, pricing, and
operations while keeping control of their files and actions.

The product is Markdown plus a small Bash installer. Slash-command definitions
run inside Claude Code and write durable output into a user's `friday/` folder.
There is no application server, database, runtime package, or background worker.

## Folder Map

- `commands/`: installable Claude Code slash-command definitions.
- `harness/`: extension guides for commands, agents, tools, and local config.
- `docs/`: the manual, writing playbook, why-guides, and media assets.
- `examples/`: examples and community contribution templates.
- `tests/`: pytest coverage for content, commands, installer, and templates.
- `scripts/`: maintainer utilities that may create external state.
- `.github/`: CI, pull request template, and issue templates.
- `install.sh`: full-pack and single-command installer.
- `CLAUDE.md.template`: template shipped to Foundation users, not repo guidance.
- `AGENTS.md`: shared coding-agent guidance.
- `CLAUDE.md`: Claude Code entrypoint importing this file.
- Root Markdown files: product, contribution, security, release, credits, and
  licence sources of truth.

Ignore generated caches such as `.pytest_cache/` and `__pycache__/`.

## Run and Test

Run the same full suite as CI:

```bash
python3 -m pytest tests/ -v
```

Focused examples:

```bash
python3 -m pytest tests/test_commands.py -v
python3 -m pytest tests/test_install.py -v
python3 -m pytest tests/test_cleanroom.py tests/test_content_sweep.py -v
```

Validate both Bash scripts without executing them:

```bash
bash -n install.sh scripts/seed-good-first-issues.sh
```

Do not run `install.sh` during routine development. It writes outside the
worktree to `~/.claude/commands/` and writes installer assets to the current
directory. Installer integration tests use temporary directories instead.

Do not run `scripts/seed-good-first-issues.sh` unless a maintainer explicitly
requests it. It creates GitHub labels and issues.

## Hard Constraints

- Add no runtime or development dependencies.
- Add no package manifests, lockfiles, frameworks, or vendored libraries.
- Keep Python tests on pytest plus the standard library.
- Keep Bash in the existing style: `set -euo pipefail` and portable constructs
  where practical.
- Add no network calls to slash-command runtime behavior. Network access is an
  installer concern only.
- Keep the full test suite green.
- Preserve the clean-room guard. `tests/test_cleanroom.py` is the authoritative
  deny-list for operator identity and proprietary terms.
- Do not add U+2013 en dashes or U+2014 em dashes to shipped Markdown, shell,
  YAML, or text content covered by the content sweep.
- Keep `main` as the integration branch and `release` as the installer source.
- Do not point install URLs at `main`.
- Do not promote, force-push, or otherwise rewrite `release` without explicit
  maintainer instruction.
- Preserve user changes and keep unrelated edits out of the patch.

## Command Changes

Every file in `commands/` must have YAML frontmatter with a non-empty `name`
and `description`, followed by substantial instructions.

A command must:

1. Work inside a Claude Code session without importing a runtime module.
2. Read `friday/voice.md` when present and follow the founder's voice.
3. Produce a real file under `friday/`.
4. Write only its owned output and never overwrite unrelated files.
5. Tell the founder what it wrote and what to do next.
6. Work on a clean machine with Bash, Python 3, and Claude Code.
7. Avoid mandatory integrations and accept manual input when practical.

When adding or renaming a command, keep the installer manifest, README, manual,
tests, and relevant templates consistent.

## Licence Rules

Most files are MIT licensed under `LICENSE`. Preserve notices and relevant
credits.

These files use `LICENSE-CONTENT`:

- `commands/amplify.md`
- `harness/05-the-amplify-logic.md`
- `docs/why-guides/amplify-why-guide.md`

Keep their content-licence header and Amplify AI attribution. Do not resell,
rebrand, claim authorship of, or misrepresent the source methodology. Read
`LICENSE-CONTENT` before editing any of them.

## Never Read or Touch Secrets

Never open, print, copy, edit, rename, delete, change permissions on, stage, or
commit:

- `.env` or `.env.*` files anywhere.
- Private keys or keystores: `*.pem`, `*.key`, `*.p12`, `*.pfx`, `*.jks`,
  `id_rsa*`, or `id_ed25519*`.
- `credentials*.json`, `client_secret*.json`, `service-account*.json`, or
  `secrets.*`.
- `~/.claude/claude.json`, `~/.claude.json`, or MCP credential configuration.
- `~/.ssh/**`, `~/.gnupg/**`, `~/.aws/**`, `~/.config/gcloud/**`, or
  `~/.kube/config`.
- `~/.netrc`, `~/.npmrc`, `~/.pypirc`, authenticated CLI configuration, shell
  profiles, keychains, browser credential stores, cookies, or token caches.

Never dump the environment or credential stores with commands such as `env`,
`printenv`, unrestricted `set`, or keychain and authentication export commands.

Treat a real user's `friday/` folder and writing samples as private business
data. Do not inspect or modify them unless the user explicitly provides
sanitized fixtures for the task.

If work appears to require a secret, stop and ask for a sanitized fixture or a
non-secret interface. Do not inspect the suspected file first.

## Completion Gate

Before handing off a change:

1. Review the diff for scope, attribution, and accidental sensitive content.
2. Run the relevant focused tests while iterating.
3. Run `python3 -m pytest tests/ -v`.
4. Run the Bash syntax check when either shell script could be affected.
5. Report what changed, what passed, and any remaining risk.
