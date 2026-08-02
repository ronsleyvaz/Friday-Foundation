"""/risk-register: a register is only useful if every risk is actionable.

The command's whole claim is that it beats a decorative risk list. That claim
rests on two fields the founder can act on, an observable early trigger and a
named owner, and on a mitigation that is distinct from the contingency. These
tests hold the command to that claim.
"""
from pathlib import Path

from tests.test_commands import parse_frontmatter

REPO_ROOT = Path(__file__).parent.parent
COMMAND_PATH = REPO_ROOT / "commands" / "risk-register.md"


def get_risk_register_command() -> str:
    return COMMAND_PATH.read_text(encoding="utf-8")


def test_risk_register_command_frontmatter():
    text = get_risk_register_command()
    fm, body = parse_frontmatter(text)

    assert fm["name"] == "risk-register"
    assert "friday/risk-register.md" in fm["description"]
    assert "friday/voice.md" in fm["description"]
    assert body.startswith("# /risk-register")


def test_captures_all_seven_risk_fields():
    """Drop any one of these and the register stops being actionable."""
    text = get_risk_register_command()
    for field in (
        "**Risk:**",
        "**Probability:**",
        "**Impact:**",
        "**Early trigger:**",
        "**Mitigation:**",
        "**Contingency:**",
        "**Owner:**",
    ):
        assert field in text, f"risk field missing from the command: {field}"


def test_trigger_must_be_observable_with_an_example():
    """A vague trigger is the failure mode. The command teaches the difference
    with a concrete pair rather than asserting the rule abstractly."""
    text = get_risk_register_command()
    assert "observable event" in text
    assert "Sales feel slow" in text, "the negative example is missing"
    assert "Fewer than 10 signups by day 14" in text, "the positive example is missing"


def test_mitigation_and_contingency_are_distinguished():
    """Before the trigger versus after it. Collapsing the two is why registers
    get written once and never used."""
    text = get_risk_register_command()
    assert "before the trigger fires" in text
    assert "after the trigger fires" in text
    assert "different action from the mitigation" in text


def test_unassigned_owner_is_named_not_invented():
    """No-fabrication rule applied to the one field a plan usually omits."""
    text = get_risk_register_command()
    assert "unassigned" in text
    assert "rather than inventing a name" in text


def test_separates_stated_from_assumed():
    text = get_risk_register_command()
    assert "**Stated:**" in text
    assert "**Assumed:**" in text
    assert "Do not fabricate" in text


def test_refuses_unsanitized_and_unconsented_file_reads():
    """Same privacy bar as /customer-feedback: named files only, no secrets,
    and no reading a default file the founder did not agree to."""
    text = get_risk_register_command()
    assert "read only `.md`, `.markdown`, or `.txt` files they explicitly named" in text
    assert "private key" in text
    assert "Never read a file the founder has not agreed to." in text


def test_writes_to_the_friday_folder():
    text = get_risk_register_command()
    assert "Create the `friday/` folder if it does not exist" in text
    assert "friday/risk-register.md" in text


def test_no_em_dashes():
    text = get_risk_register_command()
    assert "—" not in text and "–" not in text


def test_no_motivational_close():
    """House rule, and the command states it for its own output too."""
    text = get_risk_register_command()
    assert "Do not add a motivational close." in text


def test_file_ends_with_a_newline():
    """The contributed draft did not. Small, but it is the repo's convention
    and it makes every future diff cleaner."""
    assert get_risk_register_command().endswith("\n")
