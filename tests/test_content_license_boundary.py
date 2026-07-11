"""Content-licence boundary (Story 5.2 AC3).

The LICENSE-CONTENT marker comment must appear in exactly the three
maintainer-owned files and nowhere else in the shipped content. This pins the
content-licence boundary so no pull request can silently extend it to a new
file or drop a required header from one of the three.

LICENSE-CONTENT itself and the tests/ directory are excluded from the scan:
the licence file defines the terms, and the tests name the files as data.
"""
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
MARKER = "<!-- Content licensed under LICENSE-CONTENT"

# The only files permitted to carry the content licence.
LICENSED_FILES = {
    "commands/amplify.md",
    "harness/05-the-amplify-logic.md",
    "docs/why-guides/amplify-why-guide.md",
}

# Content roots scanned for the marker. This is the full shipped-content
# surface: the four content directories plus the root Markdown guides below.
# LICENSE-CONTENT (defines the terms) and tests/ (name the files as data) are
# intentionally out of scope; caches and .git are never Markdown content.
SCAN_DIRS = ["commands", "harness", "docs", "examples"]
SCAN_ROOT_FILES = [
    "README.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "RELEASING.md",
    "CREDITS.md",
    "AGENTS.md",
    "CLAUDE.md",
    "CLAUDE.md.template",
]


def _iter_content_files():
    for d in SCAN_DIRS:
        base = REPO_ROOT / d
        if base.exists():
            for p in base.rglob("*.md"):
                yield p
    for f in SCAN_ROOT_FILES:
        p = REPO_ROOT / f
        if p.exists():
            yield p


def test_content_licence_marker_in_exactly_the_three_files():
    """The marker appears in exactly the three named files, nowhere else."""
    found = set()
    for p in _iter_content_files():
        if MARKER in p.read_text(encoding="utf-8"):
            found.add(p.relative_to(REPO_ROOT).as_posix())
    assert found == LICENSED_FILES, (
        "content-licence marker boundary drifted.\n"
        f"  expected exactly: {sorted(LICENSED_FILES)}\n"
        f"  found:            {sorted(found)}\n"
        "Every content-licensed file must carry the marker, and no other "
        "shipped file may."
    )


def test_each_licensed_file_carries_the_marker():
    """Each of the three files still carries the marker (header not dropped)."""
    for rel in sorted(LICENSED_FILES):
        p = REPO_ROOT / rel
        assert p.exists(), f"licensed file missing: {rel}"
        assert MARKER in p.read_text(encoding="utf-8"), (
            f"{rel} lost its content-licence marker; restore the "
            f"'{MARKER} ...' comment near the top of the file"
        )
