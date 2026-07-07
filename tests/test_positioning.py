"""
Positioning command validity: the /positioning command must exist with valid
frontmatter and content that follows the CONTRIBUTING quality bar.
"""
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
COMMANDS_DIR = REPO_ROOT / "commands"


def parse_frontmatter(text: str):
    """Return (frontmatter_dict, body) or (None, text) if no frontmatter."""
    if not text.startswith("---"):
        return None, text
    end = text.find("---", 3)
    if end == -1:
        return None, text
    raw = text[3:end].strip()
    body = text[end + 3:].strip()
    fm = {}
    for line in raw.splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            fm[key.strip()] = val.strip()
    return fm, body


def test_positioning_command_exists():
    """commands/positioning.md exists as a new command file."""
    cmd = COMMANDS_DIR / "positioning.md"
    assert cmd.exists(), "commands/positioning.md is missing"


def test_positioning_has_valid_frontmatter():
    """positioning.md has valid frontmatter with name and description."""
    cmd = COMMANDS_DIR / "positioning.md"
    text = cmd.read_text(encoding="utf-8")
    fm, _ = parse_frontmatter(text)
    assert fm is not None, "positioning.md: missing frontmatter"
    assert fm.get("name") == "positioning", f"positioning.md: name should be 'positioning', got '{fm.get('name')}'"
    assert fm.get("description"), "positioning.md: frontmatter missing 'description' field"


def test_positioning_has_quality_bar_compliance():
    """positioning.md passes all CONTRIBUTING quality-bar checks."""
    cmd = COMMANDS_DIR / "positioning.md"
    text = cmd.read_text(encoding="utf-8")
    _, body = parse_frontmatter(text)
    assert len(body.strip()) > 100, "positioning.md: body too short"

    # No em dashes
    assert "–" not in text and "—" not in text, "positioning.md: contains em dashes"

    # Writes to friday/ folder
    assert "friday/positioning.md" in text, "positioning.md: should write to friday/positioning.md"

    # Reads friday/voice.md
    assert "friday/voice.md" in text, "positioning.md: should read friday/voice.md"

    # Tells founder what to do next
    assert "Your config is growing" in text, "positioning.md: should tell founder what to do next"
