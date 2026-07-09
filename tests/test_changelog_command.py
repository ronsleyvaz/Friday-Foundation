from pathlib import Path

from tests.test_commands import parse_frontmatter

REPO_ROOT = Path(__file__).parent.parent
COMMAND_PATH = REPO_ROOT / "commands" / "changelog.md"


def get_changelog_command():
    return COMMAND_PATH.read_text(encoding="utf-8")


def test_changelog_command_frontmatter():
    text = get_changelog_command()
    fm, body = parse_frontmatter(text)

    assert fm["name"] == "changelog"
    assert "friday/changelog.md" in fm["description"]
    assert "friday/voice.md" in fm["description"]
    assert "git history since the last release" in fm["description"]
    assert body.startswith("# /changelog")


def test_changelog_command_reads_git_history_since_release():
    text = get_changelog_command()

    required_phrases = [
        "git rev-parse --is-inside-work-tree",
        "git describe --tags --abbrev=0",
        "git log <tag>..HEAD",
        "git diff --stat <tag>..HEAD",
        "last 30 days",
    ]

    for phrase in required_phrases:
        assert phrase in text


def test_changelog_command_writes_expected_output_and_next_steps():
    text = get_changelog_command()

    required_phrases = [
        "Write the result to `friday/changelog.md`",
        "Create the `friday/` folder if it does not exist",
        "## Added",
        "## Changed",
        "## Fixed",
        "## Removed",
        "### Next steps",
        "Changelog saved to `friday/changelog.md`",
    ]

    for phrase in required_phrases:
        assert phrase in text


def test_changelog_command_preserves_voice_and_privacy():
    text = get_changelog_command()

    assert "Check whether `friday/voice.md` exists" in text
    assert "write all output in the founder's voice" in text
    assert "Do not expose secrets" in text
    assert "anything the founder marked as not public" in text
