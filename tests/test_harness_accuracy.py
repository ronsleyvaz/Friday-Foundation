"""Harness and docs accuracy regressions (Story 5.1).

Each test pins a corrected mechanism so a future edit cannot quietly
reintroduce a dead file or a wrong Claude Code mechanism.
"""
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent

HARNESS_ADD_COMMAND = REPO_ROOT / "harness" / "01-add-a-command.md"
HARNESS_ADD_AGENT = REPO_ROOT / "harness" / "02-add-an-agent.md"
HARNESS_CONNECT = REPO_ROOT / "harness" / "03-connect-your-own-tools.md"
HARNESS_FOLDER = REPO_ROOT / "harness" / "04-the-friday-folder.md"
MANUAL = REPO_ROOT / "docs" / "foundation-manual.md"
CONTRIBUTING = REPO_ROOT / "CONTRIBUTING.md"
README = REPO_ROOT / "README.md"

# Files scanned for the phantom MCP config path. Mirrors the shipped content
# surface: harness/docs/commands plus the root guides and the installer.
SCAN_GLOBS = ["*.md", "*.sh", "*.txt", "*.template"]
SCAN_DIRS = ["commands", "harness", "docs", ".github"]
SCAN_ROOT_FILES = [
    "README.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "AGENTS.md",
    "CLAUDE.md",
    "CLAUDE.md.template",
    "install.sh",
]


def _shipped_files():
    for d in SCAN_DIRS:
        base = REPO_ROOT / d
        if base.exists():
            for pattern in SCAN_GLOBS:
                yield from base.rglob(pattern)
    for f in SCAN_ROOT_FILES:
        p = REPO_ROOT / f
        if p.exists():
            yield p


# --- AC1: MCP configuration -------------------------------------------------

def test_no_phantom_claude_json_path_anywhere():
    """The fabricated `~/.claude/claude.json` path appears nowhere in the repo.

    The real Claude Code config is `~/.claude.json` (no `claude/` subdirectory).
    """
    offenders = []
    for p in _shipped_files():
        if "~/.claude/claude.json" in p.read_text(encoding="utf-8"):
            offenders.append(p.relative_to(REPO_ROOT).as_posix())
    assert not offenders, (
        "phantom path `~/.claude/claude.json` found in: " + ", ".join(sorted(offenders))
        + " -- the real path is `~/.claude.json`"
    )


def test_mcp_docs_teach_claude_mcp_add():
    """The MCP guidance runs `claude mcp add` and names the real storage paths."""
    for path in (HARNESS_CONNECT, MANUAL):
        text = path.read_text(encoding="utf-8")
        assert "claude mcp add" in text, (
            f"{path.name} must tell readers to run `claude mcp add`"
        )
        assert "~/.claude.json" in text, (
            f"{path.name} must name the real user-scope path `~/.claude.json`"
        )
    # The connect guide also names the project-scope file.
    assert ".mcp.json" in HARNESS_CONNECT.read_text(encoding="utf-8"), (
        "the connect guide must name the project-scope file `.mcp.json`"
    )


# --- AC2: command naming ----------------------------------------------------

def test_command_guide_says_filename_names_the_command():
    """The add-a-command guide says the filename becomes the command name and
    does not claim the frontmatter names the command."""
    text = HARNESS_ADD_COMMAND.read_text(encoding="utf-8")
    assert "filename becomes the command name" in text, (
        "01-add-a-command.md must state the filename becomes the command name"
    )
    assert "frontmatter to name the command" not in text, (
        "01-add-a-command.md must not claim Claude Code reads the frontmatter to "
        "name the command; the filename is authoritative"
    )


# --- AC3: no dead spawned-agents file ---------------------------------------

def test_no_spawned_agents_file_reference():
    """No doc tells readers to maintain a `spawned-agents.md` index."""
    offenders = []
    for p in _shipped_files():
        if "spawned-agents" in p.read_text(encoding="utf-8"):
            offenders.append(p.relative_to(REPO_ROOT).as_posix())
    assert not offenders, (
        "dead `spawned-agents.md` reference found in: " + ", ".join(sorted(offenders))
    )


def test_agent_guide_has_the_lightweight_replacement():
    """AC3's second half: the dead-file instruction is replaced with a
    lightweight 'keep a note' pointer, not just deleted."""
    text = HARNESS_ADD_AGENT.read_text(encoding="utf-8").lower()
    assert "keep a note" in text, (
        "02-add-an-agent.md must replace the spawned-agents.md instruction with a "
        "one-line 'keep a note wherever you track your setup'"
    )


# --- AC4: three-way friday/ folder behaviour --------------------------------

def _bullet_line(text, label):
    """Return the '- **<label>...' bullet line from the behaviour split, or ''."""
    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith(f"- **{label}"):
            return line
    return ""


def test_friday_folder_states_three_way_split():
    """04-the-friday-folder.md names the snapshot / log / config split, assigns
    each file to the correct group, and no longer over-claims that most commands
    append. Assertions are anchored to the bullet lines so pre-existing mentions
    of the same words elsewhere in the file cannot make the test vacuous."""
    text = HARNESS_FOLDER.read_text(encoding="utf-8")

    snapshot = _bullet_line(text, "Snapshot")
    log = _bullet_line(text, "Log")
    config = _bullet_line(text, "Config")
    assert snapshot and log and config, (
        "folder guide must have a Snapshots, a Logs, and a Config bullet in the "
        "behaviour split"
    )

    # Each file sits in its verified group (checked on the group's own line).
    assert "friday/morning.md" in snapshot and "friday/growth.md" in snapshot, (
        "morning.md and growth.md are snapshots (rewritten each run)"
    )
    assert "friday/decisions.md" in log and "friday/shipping-retro.md" in log, (
        "decisions.md and shipping-retro.md are append-only logs"
    )
    assert "friday/nine-decisions.md" in config and "friday/voice.md" in config, (
        "nine-decisions.md and voice.md are kept-and-edited config"
    )

    # learnings.md is curated/prunable, so it must NOT be sold as an append-only
    # log; it is described separately.
    assert "friday/learnings.md" not in log, (
        "learnings.md is curated and prunable, not an append-only log"
    )
    lower = text.lower()
    assert "learnings.md" in lower and "prune" in lower, (
        "the guide must describe learnings.md as a curated log you can prune"
    )

    # The over-claim the plan flagged must be gone.
    assert "most commands append" not in lower, (
        "folder guide must not claim most commands append; the real behaviour is a "
        "three-way split"
    )


# --- AC5: honest first-command effort ---------------------------------------

def test_first_command_effort_is_honest():
    """CONTRIBUTING and README frame the scaffold as ten minutes and a polished
    command as an hour or two; the dishonest all-in-ten-minutes claim is gone."""
    contributing = CONTRIBUTING.read_text(encoding="utf-8").lower()
    readme = README.read_text(encoding="utf-8").lower()
    for name, text in (("CONTRIBUTING.md", contributing), ("README.md", readme)):
        assert "hour or two" in text, (
            f"{name} must state a polished command takes an hour or two"
        )
    # The specific over-promises must be gone.
    assert "ship your first command in ten minutes" not in contributing, (
        "CONTRIBUTING.md must not promise a shipped command in ten minutes"
    )
    assert "ship your first command in about ten minutes" not in readme, (
        "README.md must not promise a shipped command in about ten minutes"
    )
