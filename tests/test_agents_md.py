"""AGENTS.md and the root CLAUDE.md are the coding-agent guide. They must stay
accurate (licence list, dev commands, registration and claim steps), em-dash
clean, and inside the content sweeps, and CLAUDE.md must stay a thin @AGENTS.md
pointer rather than a second source that can drift.
"""
import re
from pathlib import Path

from tests.test_cleanroom import SCAN_FILES

REPO_ROOT = Path(__file__).parent.parent
AGENTS = REPO_ROOT / "AGENTS.md"
ROOT_CLAUDE = REPO_ROOT / "CLAUDE.md"
CI = REPO_ROOT / ".github" / "workflows" / "ci.yml"

LICENSE_CONTENT_FILES = {
    "commands/amplify.md",
    "harness/05-the-amplify-logic.md",
    "docs/why-guides/amplify-why-guide.md",
}


def test_agents_md_exists():
    assert AGENTS.exists(), "AGENTS.md is missing"


def test_agents_md_names_exactly_the_three_licensed_files():
    """The Licence Rules section names exactly the three LICENSE-CONTENT files.

    Guards both directions: a licensed file dropped, or a fourth file smuggled
    into the closed list.
    """
    text = AGENTS.read_text(encoding="utf-8")
    assert "## Licence Rules" in text, "AGENTS.md must keep a Licence Rules section"
    section = text.split("## Licence Rules", 1)[1].split("\n## ", 1)[0]
    listed = set(re.findall(r"`([a-zA-Z0-9_./-]+\.md)`", section))
    assert listed == LICENSE_CONTENT_FILES, (
        f"AGENTS.md Licence Rules lists {sorted(listed)}, "
        f"expected exactly {sorted(LICENSE_CONTENT_FILES)}"
    )


def test_agents_md_states_python3_test_command():
    assert "python3 -m pytest tests/" in AGENTS.read_text(encoding="utf-8"), (
        "AGENTS.md must state the python3 test command"
    )


def test_agents_md_names_dev_requirements():
    assert "requirements-dev.txt" in AGENTS.read_text(encoding="utf-8"), (
        "AGENTS.md Run and Test must name requirements-dev.txt so dev setup matches CONTRIBUTING and CI"
    )


def test_agents_md_names_registration_step():
    text = AGENTS.read_text(encoding="utf-8")
    assert "PACK_COMMANDS" in text, "AGENTS.md must name the PACK_COMMANDS registration step"
    assert "test_catalog_parity.py" in text, "AGENTS.md must name the parity tests that enforce the rest"


def test_agents_md_carries_claim_convention():
    # Assert on the distinctive section, not the bare token "claim": AGENTS.md
    # already contains "claim" in unrelated sentences ("command-count claims",
    # "claim authorship of"), so a bare-substring check would pass even if the
    # whole claiming section were deleted.
    text = AGENTS.read_text(encoding="utf-8")
    assert "## Claiming an Issue" in text, (
        "AGENTS.md must carry the issue-claiming section so agents do not duplicate in-flight work"
    )
    assert "pick another" in text.lower(), (
        "AGENTS.md claiming guidance must tell agents to pick another issue if one is already taken"
    )


def test_agents_md_permits_dev_pytest_dependency():
    """The reconcile must not leave AGENTS.md forbidding the dev dependency it now requires."""
    text = AGENTS.read_text(encoding="utf-8")
    lower = text.lower()
    # The pre-reconcile flat prohibition contradicted requirements-dev.txt; it must be gone.
    assert "no runtime or development dependencies" not in lower, (
        "AGENTS.md Hard Constraints must not flatly forbid dev dependencies now that requirements-dev.txt exists"
    )
    assert "requirements-dev.txt" in text, (
        "AGENTS.md must acknowledge the pinned dev dependency file so the guide agrees with CONTRIBUTING and CI"
    )


def test_ci_grep_sweep_covers_agents_and_root_claude():
    """The ci.yml belt-and-suspenders grep sweep must still scan both root guide files.

    AC3 names the ci.yml raw grep file list as one of the three sweep vectors;
    without this, dropping the files from the sweep would pass every test.
    """
    text = CI.read_text(encoding="utf-8")
    grep_line = next(
        (line for line in text.splitlines() if "LICENSE-CONTENT" in line and "install.sh" in line),
        None,
    )
    assert grep_line, "ci.yml raw-grep sweep target list not found"
    tokens = grep_line.split()
    assert "AGENTS.md" in tokens, "ci.yml grep sweep must list AGENTS.md as a scan target"
    assert "CLAUDE.md" in tokens, (
        "ci.yml grep sweep must list the root CLAUDE.md as its own target (not only CLAUDE.md.template)"
    )


def test_agents_md_no_em_dashes():
    for lineno, line in enumerate(AGENTS.read_text(encoding="utf-8").splitlines(), start=1):
        assert "–" not in line and "—" not in line, f"AGENTS.md:{lineno} contains an en/em dash"


def test_root_claude_no_em_dashes():
    for lineno, line in enumerate(ROOT_CLAUDE.read_text(encoding="utf-8").splitlines(), start=1):
        assert "–" not in line and "—" not in line, f"CLAUDE.md:{lineno} contains an en/em dash"


def test_root_claude_imports_agents():
    assert "@AGENTS.md" in ROOT_CLAUDE.read_text(encoding="utf-8"), (
        "root CLAUDE.md must import @AGENTS.md as the canonical guide (thin pointer, no duplicated guidance)"
    )


def test_sweeps_cover_agents_and_root_claude():
    """Both root files must be inside the clean-room scan list (root files are
    otherwise outside the directory-based sweeps)."""
    assert "AGENTS.md" in SCAN_FILES, "clean-room SCAN_FILES must cover AGENTS.md"
    assert "CLAUDE.md" in SCAN_FILES, "clean-room SCAN_FILES must cover the root CLAUDE.md"
