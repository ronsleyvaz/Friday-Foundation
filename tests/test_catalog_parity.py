"""Keep command files, installer surfaces, and user documentation aligned."""

import re
from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent
COMMANDS_DIR = REPO_ROOT / "commands"
INSTALL_SH = REPO_ROOT / "install.sh"
README = REPO_ROOT / "README.md"
MANUAL = REPO_ROOT / "docs" / "foundation-manual.md"
CREDITS = REPO_ROOT / "CREDITS.md"
NEW_CAPABILITY = COMMANDS_DIR / "new-capability.md"


def command_slugs():
    return {path.stem for path in COMMANDS_DIR.glob("*.md")}


def command_outputs():
    """Derive each command's primary output path from its frontmatter."""
    outputs = {}
    for path in COMMANDS_DIR.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        description_match = re.search(r"^description:\s*(.+)$", text, re.MULTILINE)
        assert description_match, f"{path.name}: description not found"
        candidates = re.findall(
            r"\b(?:friday|commands)/[a-zA-Z0-9_<>./-]+\.md\b",
            description_match.group(1),
        )
        if path.stem != "voice-installer":
            candidates = [candidate for candidate in candidates if candidate != "friday/voice.md"]
        assert candidates, f"{path.name}: primary output path not found in description"
        outputs[path.stem] = candidates[-1]
    return outputs


def installer_entries():
    text = INSTALL_SH.read_text(encoding="utf-8")
    match = re.search(r"PACK_COMMANDS=\(\n(.*?)\n\)", text, re.DOTALL)
    assert match, "install.sh: PACK_COMMANDS manifest not found"
    return re.findall(
        r'^\s*"([a-z0-9-]+)\s+([a-z0-9-]+\.md)\s+/([a-z0-9-]+)"\s*$',
        match.group(1),
        re.MULTILINE,
    )


def documented_commands(path: Path):
    text = path.read_text(encoding="utf-8")
    return re.findall(r"^\|\s*`/([a-z0-9-]+)`\s*\|", text, re.MULTILINE)


def documented_outputs(path: Path):
    text = path.read_text(encoding="utf-8")
    return dict(
        re.findall(
            r"^\|\s*`/([a-z0-9-]+)`\s*\|[^|]*\|\s*`([^`]+)`\s*\|",
            text,
            re.MULTILINE,
        )
    )


def test_installer_manifest_matches_command_directory():
    """Every command file is installable and every manifest entry resolves."""
    expected = command_slugs()
    entries = installer_entries()

    manifest_slugs = {slug for slug, _, _ in entries}
    manifest_files = {Path(filename).stem for _, filename, _ in entries}
    manifest_slashes = {slash for _, _, slash in entries}

    assert manifest_slugs == expected
    assert manifest_files == expected
    assert manifest_slashes == expected
    assert len(entries) == len(expected), "install.sh: duplicate PACK_COMMANDS entry"


def test_installer_usage_block_matches_manifest():
    """The header usage examples list exactly the single-command manifest slugs.

    No other test covers the usage comment block, so a command added to
    PACK_COMMANDS but forgotten here would ship incomplete help text.
    """
    text = INSTALL_SH.read_text(encoding="utf-8")
    usage_slugs = re.findall(r"^#.*bash -s -- ([a-z0-9-]+)\b", text, re.MULTILINE)
    manifest_slugs = {slug for slug, _, _ in installer_entries()}
    assert set(usage_slugs) == manifest_slugs, (
        "install.sh usage block out of sync with PACK_COMMANDS: "
        f"missing {manifest_slugs - set(usage_slugs)}, "
        f"extra {set(usage_slugs) - manifest_slugs}"
    )
    assert len(usage_slugs) == len(manifest_slugs), "install.sh: duplicate usage-block entry"


def test_installer_user_facing_lists_match_manifest():
    """The single-command error lists every installable command.

    The full-pack completion message is a three-step first-run path, not a
    per-command list, so only the Available list is checked here. The closing
    message itself is covered by tests in test_install.py.
    """
    expected = command_slugs()
    text = INSTALL_SH.read_text(encoding="utf-8")

    available_match = re.search(r'^\s*echo "Available: ([^"]+)"', text, re.MULTILINE)
    assert available_match, "install.sh: Available list not found"
    available_commands = [item.strip() for item in available_match.group(1).split(",")]

    assert set(available_commands) == expected
    assert len(available_commands) == len(expected)


def test_documentation_catalogues_match_command_directory():
    """README and manual tables contain every command exactly once by name."""
    expected = command_slugs()
    for path in [README, MANUAL]:
        catalogue = documented_commands(path)
        assert set(catalogue) == expected
        assert len(catalogue) == len(expected), f"{path.name}: duplicate command row"
        assert documented_outputs(path) == command_outputs()


def test_documented_command_counts_are_current():
    """Every explicit command-count claim matches the command directory."""
    expected_count = len(command_slugs())
    for path in [README, MANUAL, CREDITS]:
        text = path.read_text(encoding="utf-8")
        claims = [int(value) for value in re.findall(r"\b(\d+) commands\b", text)]
        assert claims, f"{path.name}: no numeric command-count claim found"
        assert set(claims) == {expected_count}, (
            f"{path.name}: command-count claims {claims} do not match {expected_count}"
        )


def test_new_capability_reserves_every_command_name():
    """The command scaffold cannot reuse an installed command name."""
    text = NEW_CAPABILITY.read_text(encoding="utf-8")
    match = re.search(r"not clash with an existing command name \(([^)]+)\)", text)
    assert match, "new-capability.md: existing command-name list not found"
    reserved = [item.strip() for item in match.group(1).split(",")]
    assert set(reserved) == command_slugs()
    assert len(reserved) == len(command_slugs()), "new-capability.md: duplicate command name"


def test_new_command_contributors_are_credited():
    """Contributor attribution remains attached to each merged command."""
    text = CREDITS.read_text(encoding="utf-8")
    expected_credits = {
        "ericchen913900": "changelog",
        "kernelpanic888": "positioning",
        "blut-agent": "roadmap",
    }
    for handle, command in expected_credits.items():
        expected_line = f"- {handle}, `/{command}`"
        assert expected_line in text, f"CREDITS.md: missing {expected_line}"
