"""Trust-surface regressions (Story 5.2).

Pin the corrected security-reporting channel (AC1) and the corrected
contribution-licence clause (AC2) so neither can quietly regress to the old
broken wording.
"""
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SECURITY = REPO_ROOT / "SECURITY.md"
CONTRIBUTING = REPO_ROOT / "CONTRIBUTING.md"

LICENSED_FILES = [
    "commands/amplify.md",
    "harness/05-the-amplify-logic.md",
    "docs/why-guides/amplify-why-guide.md",
]


# --- AC1: real, private security channel ------------------------------------

def test_security_points_at_private_reporting():
    """SECURITY.md routes sensitive reports to GitHub private reporting."""
    text = SECURITY.read_text(encoding="utf-8")
    assert "Report a vulnerability" in text, (
        "SECURITY.md must point sensitive reports at the GitHub Security tab's "
        "'Report a vulnerability' private advisory flow"
    )


def test_security_has_no_broken_bare_domain_contact():
    """The broken 'email amplifyais.com' bare-domain contact is gone.

    (The MIT footer 'Built by Amplify AI at amplifyais.com' is attribution, not
    a report channel, so we only forbid the email instruction.)
    """
    text = SECURITY.read_text(encoding="utf-8")
    assert "email amplifyais.com" not in text, (
        "SECURITY.md must not tell reporters to 'email amplifyais.com' -- a bare "
        "domain is not a mailbox"
    )


def test_security_keeps_a_working_fallback():
    """A reporter always has a channel, even before private reporting is enabled."""
    text = SECURITY.read_text(encoding="utf-8").lower()
    assert "request private contact" in text, (
        "SECURITY.md must keep a working fallback (request private contact via a "
        "detail-free public issue) so the flow is never a dead end"
    )


# --- AC2: unambiguous contribution licence ----------------------------------

def test_contributing_licence_clause_is_unambiguous():
    """The licence clause grandfathers contributions merged before the
    PolyForm switch as MIT, states PolyForm applies to new pull requests,
    and names the three maintainer-owned content-licensed files as a
    closed list."""
    text = CONTRIBUTING.read_text(encoding="utf-8")
    lower = text.lower()
    assert "stays mit licensed" in lower, (
        "CONTRIBUTING must grandfather contributions merged before the "
        "PolyForm switch as MIT licensed"
    )
    assert "#38" in text and "#40" in text, (
        "CONTRIBUTING must name PRs #38 and #40 as examples covered by the "
        "MIT grandfather clause"
    )
    assert "polyform noncommercial 1.0.0" in lower, (
        "CONTRIBUTING must state new pull requests ship under PolyForm "
        "Noncommercial 1.0.0"
    )
    assert "maintainer-owned" in lower, (
        "CONTRIBUTING must state the LICENSE-CONTENT files are maintainer-owned"
    )
    for f in LICENSED_FILES:
        assert f in text, (
            f"CONTRIBUTING's licence clause must name the content-licensed file {f}"
        )
    assert "must not add files to that list" in lower, (
        "CONTRIBUTING must forbid a PR from adding files to the LICENSE-CONTENT list"
    )


# --- Usage disclosure matches reality (v1.3.0) -------------------------------

README = REPO_ROOT / "README.md"
AGENTS = REPO_ROOT / "AGENTS.md"
FRIDAY_UPGRADE = REPO_ROOT / "commands" / "friday-upgrade.md"

DEAL_SENTENCE = (
    "Free means we see which of her commands you use and whether they worked. "
    "Never what you typed, never what she wrote. "
    "Need her fully private? That is Friday SUPPORT."
)

FORBIDDEN_CLAIMS = (
    "phones home",
    "Does not collect data",
    "no network requests at runtime",
    "No separate Shortcuts account or backend",
    "no off switch",
    "cannot be turned off",
)


def test_repo_text_matches_usage_reality():
    readme_text = README.read_text(encoding="utf-8")
    assert DEAL_SENTENCE in readme_text
    assert "What Shortcuts sends home" in readme_text

    security_text = SECURITY.read_text(encoding="utf-8")
    assert "All four" not in security_text

    checked = [README, SECURITY, AGENTS, FRIDAY_UPGRADE, REPO_ROOT / "install.sh"]
    checked += sorted((REPO_ROOT / "commands").glob("*.md"))
    checked += sorted((REPO_ROOT / "docs").glob("*.md"))
    checked += sorted((REPO_ROOT / "harness").glob("*.md"))
    for path in checked:
        text = path.read_text(encoding="utf-8")
        for claim in FORBIDDEN_CLAIMS:
            assert claim not in text, f"{path.name} still contains: {claim}"
