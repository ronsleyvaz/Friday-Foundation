"""Dev setup must work first try on a clean machine: a pinned dev-dependency
file, CI that installs from it with a pinned Python, honest dependency wording,
and docs that use `python3` (bare `python` is missing on a clean macOS).
"""
import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
REQUIREMENTS = REPO_ROOT / "requirements-dev.txt"
CI = REPO_ROOT / ".github" / "workflows" / "ci.yml"
CONTRIBUTING = REPO_ROOT / "CONTRIBUTING.md"
SEED_SCRIPT = REPO_ROOT / "scripts" / "seed-good-first-issues.sh"


def test_requirements_dev_exists_and_pins_pytest():
    """requirements-dev.txt exists and pins pytest to an exact version."""
    assert REQUIREMENTS.exists(), "requirements-dev.txt is missing"
    text = REQUIREMENTS.read_text(encoding="utf-8")
    assert re.search(r"^pytest==\d+\.\d+", text, re.MULTILINE), (
        "requirements-dev.txt must pin pytest to an exact version (pytest==X.Y...)"
    )


def test_ci_installs_from_requirements_dev():
    """CI installs from requirements-dev.txt, not a duplicated inline pin."""
    text = CI.read_text(encoding="utf-8")
    assert "requirements-dev.txt" in text, "ci.yml must install from requirements-dev.txt"
    assert "pip install pytest==" not in text, (
        "ci.yml must not hardcode the pytest version; the pin lives in requirements-dev.txt"
    )


def test_ci_pins_python_version():
    """CI pins the Python version with actions/setup-python (no drifting system python)."""
    text = CI.read_text(encoding="utf-8")
    assert "actions/setup-python" in text, "ci.yml must pin Python with actions/setup-python"
    assert re.search(r"python-version:\s*['\"]?3\.12", text), "ci.yml must pin Python to 3.12"


def test_ci_runs_os_matrix():
    """Story 4.2 AC1: CI runs a matrix of ubuntu and macOS, both with pinned setup-python."""
    text = CI.read_text(encoding="utf-8")
    assert "matrix" in text, "ci.yml must use a job matrix"
    assert "ubuntu-latest" in text, "ci.yml matrix must include ubuntu-latest"
    assert "macos-latest" in text, "ci.yml matrix must include macos-latest"
    assert "actions/setup-python" in text, "both matrix legs must pin Python via setup-python"


def test_ci_macos_leg_exercises_stock_bash():
    """Story 4.2 AC2: the macOS leg points installer tests at stock /bin/bash 3.2."""
    text = CI.read_text(encoding="utf-8")
    assert "FRIDAY_TEST_BASH=/bin/bash" in text, (
        "ci.yml macOS leg must set FRIDAY_TEST_BASH=/bin/bash so the installer tests exercise stock bash 3.2"
    )


def test_ci_raw_grep_sweep_scoped_to_ubuntu():
    """Story 4.2 AC3: the raw grep sweep is scoped to the ubuntu leg (the Python
    content sweep runs on both), so BSD versus GNU grep divergence cannot red macOS."""
    text = CI.read_text(encoding="utf-8")
    assert "if: matrix.os == 'ubuntu-latest'" in text, (
        "the raw grep sweep step must be guarded by `if: matrix.os == 'ubuntu-latest'`"
    )


def test_docs_use_python3_not_bare_python():
    """No bare `python -m pytest` in the docs a contributor copies (fails on clean macOS)."""
    for path in [CONTRIBUTING, SEED_SCRIPT]:
        text = path.read_text(encoding="utf-8")
        assert "python -m pytest" not in text, (
            f"{path.name} uses bare 'python -m pytest'; use 'python3' so it runs on a clean macOS"
        )


def test_contributing_documents_dev_dependency_honestly():
    """CONTRIBUTING states the honest dependency story and the install command."""
    text = CONTRIBUTING.read_text(encoding="utf-8")
    lower = text.lower()
    assert "requirements-dev.txt" in text, "CONTRIBUTING must show the requirements-dev.txt install"
    assert "one dev dependency" in lower or "only dev dependency" in lower, (
        "CONTRIBUTING must state pytest is the only dev dependency"
    )
    assert "standard library" in lower or "stdlib" in lower, (
        "CONTRIBUTING must state the tests import only the standard library"
    )
    assert "zero runtime dependencies" in lower, (
        "CONTRIBUTING must state the shipped pack has zero runtime dependencies"
    )
    assert "repo root" in lower, "CONTRIBUTING setup must say to run from the repo root"
    assert "wsl" in lower or "git bash" in lower, (
        "CONTRIBUTING setup must give Windows users a WSL or Git Bash path"
    )
