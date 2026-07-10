"""
Command markdown validity: every file in commands/ must have valid frontmatter
with a non-empty name and description, and must have content after the frontmatter.
"""
from pathlib import Path
import re

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


def get_command_files():
    return list(COMMANDS_DIR.glob("*.md"))


def test_all_commands_have_frontmatter():
    """Every command file has valid YAML frontmatter."""
    files = get_command_files()
    assert files, f"No command files found in {COMMANDS_DIR}"
    for f in files:
        text = f.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)
        assert fm is not None, f"{f.name}: missing frontmatter (must start with ---)"


def test_all_commands_have_name_field():
    """Every command file has a non-empty 'name' field in frontmatter."""
    for f in get_command_files():
        text = f.read_text(encoding="utf-8")
        fm, _ = parse_frontmatter(text)
        assert fm and fm.get("name"), f"{f.name}: frontmatter missing 'name' field"


def test_all_commands_have_description_field():
    """Every command file has a non-empty 'description' field in frontmatter."""
    for f in get_command_files():
        text = f.read_text(encoding="utf-8")
        fm, _ = parse_frontmatter(text)
        assert fm and fm.get("description"), f"{f.name}: frontmatter missing 'description' field"


def test_all_commands_have_body():
    """Every command file has content after the frontmatter."""
    for f in get_command_files():
        text = f.read_text(encoding="utf-8")
        _, body = parse_frontmatter(text)
        assert body and len(body.strip()) > 100, f"{f.name}: body too short (< 100 chars) -- likely empty"


def test_no_em_dashes_in_commands():
    """No em dashes (U+2013 or U+2014) in any command file."""
    violations = []
    for f in get_command_files():
        text = f.read_text(encoding="utf-8")
        for lineno, line in enumerate(text.splitlines(), start=1):
            if "–" in line or "—" in line:
                violations.append(f"{f.name}:{lineno}: {line.strip()[:80]}")
    assert not violations, "Em dashes found in commands:\n" + "\n".join(violations)


def test_expected_commands_exist():
    """The expected command files from the build manifest exist."""
    expected = [
        "voice-installer.md",
        "decide.md",
        "brief.md",
        "meetingprep.md",
        "weeklyreview.md",
        "new-capability.md",
        "amplify.md",
        "changelog.md",
    ]
    missing = [f for f in expected if not (COMMANDS_DIR / f).exists()]
    assert not missing, f"Missing command files: {missing}"
