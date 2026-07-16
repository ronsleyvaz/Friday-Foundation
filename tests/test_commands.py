"""
Command markdown validity: every file in commands/ must have valid frontmatter
with a non-empty name and description, and must have content after the frontmatter.
"""
from pathlib import Path
import re

REPO_ROOT = Path(__file__).parent.parent
COMMANDS_DIR = REPO_ROOT / "commands"
INSTALL_SH = REPO_ROOT / "install.sh"


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


def manifest_command_files():
    """Command file names named in install.sh's PACK_COMMANDS manifest."""
    text = INSTALL_SH.read_text(encoding="utf-8")
    match = re.search(r"PACK_COMMANDS=\(\n(.*?)\n\)", text, re.DOTALL)
    assert match, "install.sh: PACK_COMMANDS manifest not found"
    return re.findall(
        r'^\s*"[a-z0-9-]+\s+([a-z0-9-]+\.md)\s+/[a-z0-9-]+"\s*$',
        match.group(1),
        re.MULTILINE,
    )


def test_expected_commands_exist():
    """Every command file named in the installer manifest exists on disk.

    Derived from PACK_COMMANDS rather than a hardcoded list, so this check
    tracks the installer manifest and cannot drift out of date.
    """
    files = manifest_command_files()
    assert files, "No command files parsed from PACK_COMMANDS in install.sh"
    missing = [f for f in files if not (COMMANDS_DIR / f).exists()]
    assert not missing, f"Manifest names missing command files: {missing}"


def test_voice_installer_sample_fallbacks():
    """voice-installer Step 2 offers paste and no-samples paths so it never dead-ends."""
    text = (COMMANDS_DIR / "voice-installer.md").read_text(encoding="utf-8")
    lower = text.lower()
    assert "rather paste" in lower, "voice-installer Step 2 must offer a paste-your-samples option"
    assert (
        "no samples" in lower or "nothing handy" in lower or "no writing samples" in lower
    ), "voice-installer must handle the no-samples case"
    assert "estimate" in lower, (
        "voice-installer must let the Rhythm line be marked an estimate when built from the interview"
    )
    # The proof mechanism and config plumbing must survive the edit.
    assert "<!-- FRIDAY-VOICE-START -->" in text and "<!-- FRIDAY-VOICE-END -->" in text, (
        "voice sentinel block must remain intact"
    )
    assert "## Banned words" in text, "banned-words block must remain intact"


def test_brief_soft_starts_nine_decisions():
    """brief.md offers a starter decision list, accepts three to start, and no longer forbids examples."""
    text = (COMMANDS_DIR / "brief.md").read_text(encoding="utf-8")
    lower = text.lower()
    assert "hire or contract" in lower, "brief must offer a starter decision list"
    assert "build or buy" in lower, "brief starter list must include the common decisions"
    assert "adopt, edit, or replace" in lower, "the starter list must be framed as adopt/edit/replace"
    assert "at least three" in lower, "brief must accept as few as three decisions to start"
    assert "do not suggest example decisions by default" not in lower, (
        "the examples-forbidden prohibition must be removed"
    )
    # No fabricated padding to nine.
    assert (
        "do not pad" in lower or "do not fabricate" in lower or "do not invent decisions" in lower
    ), "brief must forbid padding the list with filler decisions"
    # The file identity and required fields survive.
    assert "# Nine Decisions" in text, "the nine-decisions file header must remain"
    assert "Last updated:" in text, "the nine-decisions file must keep a Last updated line"


def test_roadmap_command_exists():
    """The roadmap command file exists and has valid frontmatter."""
    roadmap = COMMANDS_DIR / "roadmap.md"
    assert roadmap.exists(), "roadmap.md is missing from commands/"
    text = roadmap.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)
    assert fm is not None, "roadmap.md: missing frontmatter"
    assert fm.get("name") == "roadmap", f"roadmap.md: name field is '{fm.get('name')}', expected 'roadmap'"
    assert fm.get("description"), "roadmap.md: missing description field"
    assert len(body) > 100, "roadmap.md: body too short"


def test_risk_register_command_exists():
    """The risk-register command file exists and has valid frontmatter."""
    register = COMMANDS_DIR / "risk-register.md"
    assert register.exists(), "risk-register.md is missing from commands/"
    text = register.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)
    assert fm is not None, "risk-register.md: missing frontmatter"
    assert fm.get("name") == "risk-register", f"risk-register.md: name field is '{fm.get('name')}', expected 'risk-register'"
    assert fm.get("description"), "risk-register.md: missing description field"
    assert len(body) > 100, "risk-register.md: body too short"
    # Must read voice profile as Step 1
    first_step = body.split("## Step 2", 1)[0]
    assert "## Step 1: Read the founder's voice profile (if it exists)" in first_step, "risk-register.md: voice read is not the first step"
    assert "friday/voice.md" in first_step, "risk-register.md: first step does not check friday/voice.md"
    assert "does not exist" in first_step, "risk-register.md: first step has no neutral fallback"
    # Must write to friday/risk-register.md
    assert "friday/risk-register.md" in text, "risk-register.md: output path not mentioned"
    # Must have the required risk fields
    for field in ["Probability", "Impact", "Early trigger", "Mitigation", "Contingency", "Owner"]:
        assert field in text, f"risk-register.md: missing '{field}' field"


def test_positioning_command_matches_issue_contract():
    """The positioning command has the output, voice, and structure requested in #10."""
    text = (COMMANDS_DIR / "positioning.md").read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)

    assert fm["name"] == "positioning"
    assert "friday/voice.md" in fm["description"]
    assert "friday/positioning.md" in fm["description"]

    required_sections = [
        "# /positioning",
        "## Step 1: Read the founder's voice profile (if it exists)",
        "## Step 2: Get the raw positioning inputs",
        "## Step 3: Tighten vague answers",
        "## Step 4: Write the positioning draft",
    ]
    for section in required_sections:
        assert section in body

    required_terms = [
        "category",
        "target customer",
        "key benefit",
        "difference from alternatives",
        "friday/positioning.md",
        "Positioning saved to `friday/positioning.md`",
        "Next move",
    ]
    for term in required_terms:
        assert term in body


def test_every_command_after_voice_installer_reads_voice_first():
    """Every other command reads voice in its top-level first step."""
    expected_heading = "## Step 1: Read the founder's voice profile (if it exists)"

    for path in get_command_files():
        if path.name == "voice-installer.md":
            continue

        text = path.read_text(encoding="utf-8")
        _, body = parse_frontmatter(text)
        first_step = body.split("## Step 2", 1)[0]
        assert expected_heading in first_step, f"{path.name}: voice read is not the first step"
        assert "Check whether `friday/voice.md` exists" in first_step, (
            f"{path.name}: first step does not check friday/voice.md"
        )
        assert "does not exist" in first_step, f"{path.name}: first step has no neutral fallback"


def test_competitive_analysis_has_swot_per_competitor():
    """The implementation fulfills its promise of a separate SWOT per competitor."""
    text = (COMMANDS_DIR / "competitive-analysis.md").read_text(encoding="utf-8")

    assert "## Step 5: Run a SWOT for each competitor" in text
    assert "For each named competitor, build a separate SWOT" in text
    assert "## Competitor SWOTs" in text
    assert "<Repeat the SWOT table for each named competitor.>" in text
    assert "## Your position SWOT" in text


def test_docs_name_new_capability_output_exception():
    """Every broad friday-folder explanation names the developer-tool exception."""
    paths = [
        REPO_ROOT / "README.md",
        REPO_ROOT / "docs" / "foundation-manual.md",
        REPO_ROOT / "harness" / "00-how-friday-works.md",
        REPO_ROOT / "harness" / "04-the-friday-folder.md",
        REPO_ROOT / "CLAUDE.md.template",
        REPO_ROOT / "AGENTS.md",
    ]

    for path in paths:
        text = path.read_text(encoding="utf-8")
        assert "/new-capability" in text, f"{path}: missing /new-capability exception"
        assert "developer-tool exception" in text, f"{path}: exception is not explicit"
        assert "commands/<name>.md" in text, f"{path}: scaffold output is not documented"
        assert "docs/skill-writing-playbook.md" in text, f"{path}: playbook output is not documented"
