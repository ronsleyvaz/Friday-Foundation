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
