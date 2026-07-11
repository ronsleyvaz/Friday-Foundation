"""Contributor-facing docs must keep naming the two facts a new command needs:
the first-PR CI approval reality (Story 1.1) and the PACK_COMMANDS registration
step (Story 1.2). These assertions stop either from silently dropping out of the
docs a contributor actually reads.
"""
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
CONTRIBUTING = REPO_ROOT / "CONTRIBUTING.md"
PR_TEMPLATE = REPO_ROOT / ".github" / "PULL_REQUEST_TEMPLATE.md"
SEED_SCRIPT = REPO_ROOT / "scripts" / "seed-good-first-issues.sh"
AGENTS = REPO_ROOT / "AGENTS.md"
GOOD_FIRST_ISSUE_TEMPLATE = REPO_ROOT / ".github" / "ISSUE_TEMPLATE" / "good-first-issue.md"


def test_contributing_states_first_pr_ci_approval():
    """CONTRIBUTING is honest that the first PR may need a one-click approval."""
    text = CONTRIBUTING.read_text(encoding="utf-8").lower()
    assert "first pr" in text, "CONTRIBUTING must mention the first-PR CI approval reality"
    assert "approval" in text, "CONTRIBUTING must mention maintainer approval"
    assert "automatic" in text, "CONTRIBUTING must say CI becomes automatic after the first PR"


def _names_registration(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    return "PACK_COMMANDS" in text and "install.sh" in text


def test_registration_step_documented_in_contributing():
    assert _names_registration(CONTRIBUTING), "CONTRIBUTING must name the PACK_COMMANDS registration step"
    # AC3: the step appears in BOTH the fast loop and the "How to submit a command" list,
    # so a partial deletion from one place cannot pass unnoticed.
    assert CONTRIBUTING.read_text(encoding="utf-8").count("PACK_COMMANDS") >= 2, (
        "CONTRIBUTING must name the registration step in both the fast loop and the submit list"
    )


def test_registration_step_documented_in_pr_template():
    assert _names_registration(PR_TEMPLATE), "PR template must name the PACK_COMMANDS registration step"


def test_registration_step_documented_in_seed_script():
    assert _names_registration(SEED_SCRIPT), "seed script DoD must name the PACK_COMMANDS registration step"


def test_registration_step_documented_in_agents_md():
    assert _names_registration(AGENTS), "AGENTS.md must name the PACK_COMMANDS registration step"
    # AC4: the checklist must also point at the parity tests that enforce the rest.
    assert "test_catalog_parity.py" in AGENTS.read_text(encoding="utf-8"), (
        "AGENTS.md Command Changes checklist must name tests/test_catalog_parity.py"
    )


# Story 3.1: the issue-claiming convention must appear everywhere a contributor
# or maintainer meets an issue, so no one duplicates in-flight work (as with #12/#13).

def test_claim_convention_documented_in_contributing():
    """CONTRIBUTING's fast loop tells contributors to claim the issue first."""
    lower = CONTRIBUTING.read_text(encoding="utf-8").lower()
    assert "claim" in lower, "CONTRIBUTING must document the issue-claiming step"
    assert "assign" in lower, "CONTRIBUTING claim step must mention maintainer assignment"


def test_claim_convention_documented_in_seed_script():
    """Seeded issue bodies carry a How to claim section."""
    assert "how to claim" in SEED_SCRIPT.read_text(encoding="utf-8").lower(), (
        "seed script issue body must include a How to claim section"
    )


def test_claim_convention_documented_in_issue_template():
    """The manual good-first-issue template carries the same claim section."""
    assert GOOD_FIRST_ISSUE_TEMPLATE.exists(), "good-first-issue.md template is missing"
    assert "how to claim" in GOOD_FIRST_ISSUE_TEMPLATE.read_text(encoding="utf-8").lower(), (
        "good-first-issue.md template must include a How to claim section"
    )
