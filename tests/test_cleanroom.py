"""
Clean-room guard: verify the public repo contains zero operator identity,
proprietary markers, or secrets.

Scans: commands/, harness/, docs/, examples/, README.md, CONTRIBUTING.md,
       SECURITY.md, CLAUDE.md.template, install.sh, LICENSE-CONTENT.
Excludes: tests/ (contains pattern strings by necessity), LICENSE (MIT text).
"""
import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent

# Paths to scan (relative to repo root)
SCAN_DIRS = [
    "commands",
    "harness",
    "docs",
    "examples",
]
SCAN_FILES = [
    "README.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "CLAUDE.md.template",
    "install.sh",
    "LICENSE-CONTENT",
]

# Exact forbidden strings (case-sensitive where noted).
# "Ronsley" is the operator name.
# Operator email patterns.
# Internal proprietary module names.
# Internal env var prefixes from the operator repo.
FORBIDDEN_PATTERNS = [
    r"Ronsley",                 # operator name
    r"ronsley@",                # operator email
    r"cogmem",                  # proprietary cognitive memory module
    r"mempalace",               # proprietary memory system
    r"FRIDAY_METACOG",          # internal env var
    r"FRIDAY_SPRINT",           # internal env var
    r"FRIDAY_COGMEM",           # internal env var
    r"FRIDAY_DEBRIEF",          # internal env var
]

# Strings that are explicitly allowed (brand URL and book link are fine).
ALLOWED_EXCEPTIONS = [
    "amplifyais.com",           # brand URL
    "amazon.com",               # book link
]


def collect_files():
    """Return all file paths that must pass the clean-room check."""
    files = []
    for d in SCAN_DIRS:
        path = REPO_ROOT / d
        if path.exists():
            files.extend(path.rglob("*.md"))
            files.extend(path.rglob("*.sh"))
            files.extend(path.rglob("*.txt"))
    for f in SCAN_FILES:
        path = REPO_ROOT / f
        if path.exists():
            files.append(path)
    return files


def check_file(file_path: Path):
    """Return list of (line_number, line, pattern) tuples for violations."""
    violations = []
    text = file_path.read_text(encoding="utf-8", errors="replace")
    for lineno, line in enumerate(text.splitlines(), start=1):
        for pattern in FORBIDDEN_PATTERNS:
            if re.search(pattern, line):
                # Allow lines that only match because of an allowed exception
                clean = line
                for allowed in ALLOWED_EXCEPTIONS:
                    clean = clean.replace(allowed, "")
                if re.search(pattern, clean):
                    violations.append((lineno, line.strip(), pattern))
    return violations


def test_cleanroom_guard():
    """Zero forbidden patterns in all public-facing content files."""
    files = collect_files()
    assert files, "No files found to scan -- check SCAN_DIRS and SCAN_FILES"

    all_violations = []
    for f in files:
        viol = check_file(f)
        for lineno, line, pattern in viol:
            all_violations.append(f"  {f.relative_to(REPO_ROOT)}:{lineno} [{pattern}]  {line[:80]}")

    if all_violations:
        msg = "Clean-room violations found:\n" + "\n".join(all_violations)
        raise AssertionError(msg)
