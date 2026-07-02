"""
PR and issue template validity: the templates that guide external contributors
must exist and cover the CONTRIBUTING quality bar, so a contributor self-checks
before a maintainer ever looks, and CONTRIBUTING's issue-template reference
resolves to a real file.
"""
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
GITHUB_DIR = REPO_ROOT / ".github"


def test_pr_template_exists_and_has_quality_bar_checklist():
    """PULL_REQUEST_TEMPLATE.md exists and covers every CONTRIBUTING quality-bar item."""
    pr_template = GITHUB_DIR / "PULL_REQUEST_TEMPLATE.md"
    assert pr_template.exists(), "PULL_REQUEST_TEMPLATE.md is missing"

    text = pr_template.read_text(encoding="utf-8")
    required_phrases = [
        "real file output",
        "clean machine",
        "voice.md",
        "appends",
        "em dash",
        "what to do next",
        "pytest",
    ]
    missing = [p for p in required_phrases if p.lower() not in text.lower()]
    assert not missing, f"PR template missing quality-bar items: {missing}"

    checkbox_count = text.count("- [ ]")
    assert checkbox_count >= 6, f"PR template needs checkbox items, found {checkbox_count}"


def test_new_command_issue_template_exists_and_has_frontmatter():
    """The new-command issue template exists with valid YAML frontmatter."""
    issue_template = GITHUB_DIR / "ISSUE_TEMPLATE" / "new-command.md"
    assert issue_template.exists(), "new-command.md issue template is missing"

    text = issue_template.read_text(encoding="utf-8")
    assert text.startswith("---"), "issue template must start with YAML frontmatter"
    end = text.find("---", 3)
    assert end != -1, "issue template frontmatter is not closed"
    frontmatter = text[3:end]
    assert "name:" in frontmatter, "issue template frontmatter missing 'name'"
    assert "about:" in frontmatter, "issue template frontmatter missing 'about'"


def test_contributing_issue_template_reference_resolves():
    """CONTRIBUTING.md's 'issue template' reference points at a file that exists."""
    contributing_text = (REPO_ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
    assert "issue template" in contributing_text.lower(), (
        "CONTRIBUTING.md no longer mentions the issue template"
    )
    assert (GITHUB_DIR / "ISSUE_TEMPLATE" / "new-command.md").exists(), (
        "CONTRIBUTING.md's issue-template reference is dangling"
    )
