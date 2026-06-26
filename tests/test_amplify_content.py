"""
Amplify content guard: commands/amplify.md must reference the required
content elements and must NOT be a verbatim dump of the framework source.
"""
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
AMPLIFY_CMD = REPO_ROOT / "commands" / "amplify.md"

# All eight vital signs must be named in the command.
VITAL_SIGNS = ["team", "audience", "leads", "meetings", "content", "sales", "partnerships", "profit"]

# All four quadrants must be named.
QUADRANTS = ["revenue", "brand", "operations"]  # audience appears as a vital sign too

# The book link must appear.
BOOK_LINK = "amazon.com/Amplify"

# The output file must be referenced.
OUTPUT_FILE = "friday/growth.md"

# Framework code markers that must NOT appear (verbatim dump check).
FORBIDDEN_CODE_MARKERS = [
    "const quadrantPriority =",
    "function determineBusinessStage(",
    "const amplifySteps =",
    "const vitalSigns =",
    "function analyzeVitalSignsConnections(",
    "const ethicalParameters =",
    "const challengeSolutions =",
    "function identifyBiggestOpportunity(",
    "const aiToolsByExperience =",
    "function generateImplementationPlan(",
    "const successMetrics =",
]


def get_amplify_text():
    assert AMPLIFY_CMD.exists(), f"{AMPLIFY_CMD} does not exist"
    return AMPLIFY_CMD.read_text(encoding="utf-8").lower()


def get_amplify_text_raw():
    assert AMPLIFY_CMD.exists(), f"{AMPLIFY_CMD} does not exist"
    return AMPLIFY_CMD.read_text(encoding="utf-8")


def test_amplify_references_output_file():
    """The amplify command references friday/growth.md."""
    text = get_amplify_text()
    assert OUTPUT_FILE in text, f"amplify.md does not reference '{OUTPUT_FILE}'"


def test_amplify_names_all_vital_signs():
    """All eight vital signs are named in the amplify command."""
    text = get_amplify_text()
    missing = [vs for vs in VITAL_SIGNS if vs not in text]
    assert not missing, f"amplify.md missing vital signs: {missing}"


def test_amplify_names_quadrants():
    """Revenue, brand, and operations quadrants are named in the amplify command."""
    text = get_amplify_text()
    missing = [q for q in QUADRANTS if q not in text]
    assert not missing, f"amplify.md missing quadrants: {missing}"


def test_amplify_has_book_link():
    """The amplify command contains the book link."""
    text = get_amplify_text()
    assert BOOK_LINK.lower() in text, f"amplify.md missing book link ('{BOOK_LINK}')"


def test_amplify_not_verbatim_dump():
    """The amplify command does not contain verbatim framework code blocks."""
    raw = get_amplify_text_raw()
    found = [m for m in FORBIDDEN_CODE_MARKERS if m in raw]
    assert not found, (
        "amplify.md contains verbatim framework code markers -- "
        "translate the logic to founder-facing prose:\n" + "\n".join(found)
    )


def test_amplify_has_symbioethical_check():
    """The amplify command includes a SymbioEthical check step."""
    text = get_amplify_text()
    assert "symbio" in text, "amplify.md missing SymbioEthical check step"


def test_amplify_has_implementation_plan():
    """The amplify command includes the 1-1-1-1-1 implementation plan."""
    text = get_amplify_text()
    assert "1-1-1-1-1" in text or "five ones" in text or "5 ones" in text, (
        "amplify.md missing 1-1-1-1-1 implementation plan"
    )


def test_amplify_has_experience_levels():
    """The amplify command references AI tool suggestions by experience level."""
    text = get_amplify_text()
    has_levels = "beginner" in text or "intermediate" in text or "advanced" in text or "experience level" in text
    assert has_levels, "amplify.md missing experience-level AI tool suggestions"
