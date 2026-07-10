@AGENTS.md

# Claude Code Entry Point

`AGENTS.md` is the canonical repository guide. Do not copy its project map,
commands, constraints, licence rules, or safety rules into this file. Put shared
guidance there and keep only Claude Code-specific setup here.

## First-Session Onboarding

For a fresh clone or after a major repository restructuring:

1. Confirm that the imported `AGENTS.md` loaded and read the sources relevant
   to the planned work.
2. Inspect the worktree before making changes.
3. Run the baseline test suite from `AGENTS.md`.
4. Note any mismatch between the guide and the repository as an onboarding bug.
5. In the interactive Claude Code session, run `/init` once as the final
   onboarding step so Claude re-analyzes the repository and recalibrates its
   project guidance.

Because this `CLAUDE.md` already exists, review `/init` suggestions before
accepting them. Run `/init` interactively, never headlessly or with automatic
edit acceptance. Preserve the `@AGENTS.md` import, reject duplicated shared
guidance, and add only genuinely Claude-specific improvements here.
