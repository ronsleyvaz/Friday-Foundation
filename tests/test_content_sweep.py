"""
Content sweep: widen the em-dash and clean-room guard beyond commands/ to
every directory that ships in the public repo (docs/, harness/, .github/),
so a stray em dash or proprietary term in a why-guide, harness guide, or
CI workflow file blocks CI the same way a bad command file already does.

Reuses the clean-room deny-list from test_cleanroom.py rather than
re-inventing it.
"""
import re
from pathlib import Path

from tests.test_cleanroom import ALLOWED_EXCEPTIONS, FORBIDDEN_PATTERNS

REPO_ROOT = Path(__file__).parent.parent

SWEEP_DIRS = ["commands", "docs", "harness", ".github"]
SWEEP_EXTENSIONS = (".md", ".sh", ".txt", ".yml", ".yaml")


def collect_swept_files():
    """Return every text file under SWEEP_DIRS."""
    files = []
    for d in SWEEP_DIRS:
        path = REPO_ROOT / d
        if path.exists():
            for f in path.rglob("*"):
                if f.is_file() and f.suffix in SWEEP_EXTENSIONS:
                    files.append(f)
    return files


def test_sweep_covers_docs_and_harness_not_just_commands():
    """Guard against SWEEP_DIRS silently narrowing back to commands/ only."""
    assert "commands" in SWEEP_DIRS, "content sweep must still cover commands/"
    assert "docs" in SWEEP_DIRS, "content sweep must cover docs/"
    assert "harness" in SWEEP_DIRS, "content sweep must cover harness/"


def test_no_em_dashes_anywhere_shipped():
    """No em dashes in any file under commands/, docs/, harness/, .github/."""
    violations = []
    for f in collect_swept_files():
        text = f.read_text(encoding="utf-8", errors="replace")
        for lineno, line in enumerate(text.splitlines(), start=1):
            if "–" in line or "—" in line:
                violations.append(f"{f.relative_to(REPO_ROOT)}:{lineno}: {line.strip()[:80]}")
    assert not violations, "Em dashes found:\n" + "\n".join(violations)


def test_no_proprietary_terms_anywhere_shipped():
    """No clean-room deny-list terms in any file under commands/, docs/, harness/, .github/."""
    violations = []
    for f in collect_swept_files():
        text = f.read_text(encoding="utf-8", errors="replace")
        for lineno, line in enumerate(text.splitlines(), start=1):
            for pattern in FORBIDDEN_PATTERNS:
                if not re.search(pattern, line):
                    continue
                clean = line
                for allowed in ALLOWED_EXCEPTIONS:
                    clean = clean.replace(allowed, "")
                if re.search(pattern, clean):
                    violations.append(
                        f"{f.relative_to(REPO_ROOT)}:{lineno} [{pattern}]: {line.strip()[:80]}"
                    )
    assert not violations, "Proprietary terms found:\n" + "\n".join(violations)
