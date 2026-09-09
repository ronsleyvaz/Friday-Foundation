"""Friday Format: the reply-shape contract inside CLAUDE.md.template.

Voice governs how Friday writes content. Friday Format governs the shape of a
reply to the person running Friday: answer first, sentence limits, options
capped at three.

Two things make this worth a dedicated test file rather than a line in the
cleanroom guard:

1. This repository is public. The section is written in second person on
   purpose, and `Ronsley` is a hard fail. test_cleanroom.py already forbids the
   pattern across the template; the assertion is repeated here so a failure
   names Friday Format as the cause.
2. The template is authored by hand and filled in by the buyer. Friday Format
   must carry no `[bracket]` placeholders, or a buyer who skips it gets a
   half-configured reply rule.
"""
import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent
TEMPLATE = REPO_ROOT / "CLAUDE.md.template"

SECTION_HEADING = "## Friday Format (how Friday replies to you)"

# Headings the template carried before Friday Format was added, 2026-08-02.
# Template preservation: adding a section must not disturb the authored
# structure a buyer is told to fill in.
ORIGINAL_HEADINGS = [
    "## Identity",
    "## Voice",
    "## What I work on",
    "## How I make decisions",
    "## Autonomous vs ask first",
    "## My stack",
    "## The friday/ folder",
]

# Each rule must be present by its own words, not paraphrased away.
REQUIRED_RULES = [
    "first sentence",
    "Background only if you ask",
    "20 words maximum",
    "22 words maximum",
    "Three sentences per paragraph maximum",
    "Active voice",
    "One term per concept",
    "three maximum",
    "150 words",
    "200 words",
    "no em dashes",
]


def template_text() -> str:
    return TEMPLATE.read_text(encoding="utf-8")


def friday_format_section() -> str:
    """The Friday Format section body, heading to the next H2 or end of file."""
    text = template_text()
    start = text.index(SECTION_HEADING)
    nxt = text.find("\n## ", start + 1)
    return text[start : nxt if nxt != -1 else len(text)]


# ---------------------------------------------------------------------------
# Golden: the whole contract, end to end, against the real file on disk.
# ---------------------------------------------------------------------------


def test_template_carries_friday_format_end_to_end() -> None:
    """The regression anchor. Every rule present, second person, clean."""
    text = template_text()
    assert SECTION_HEADING in text, (
        f"CLAUDE.md.template is missing {SECTION_HEADING!r}. Shortcuts ships "
        "no reply-shape rule without it."
    )

    section = friday_format_section()

    missing = [rule for rule in REQUIRED_RULES if rule not in section]
    assert not missing, f"Friday Format is missing these rules verbatim: {missing}"

    assert "Ronsley" not in section, "operator name leaked into a public repo"
    assert "—" not in section, "em dash in the section that bans em dashes"
    assert "[" not in section, "Friday Format must work unedited, no placeholders"


# ---------------------------------------------------------------------------
# Units
# ---------------------------------------------------------------------------


def test_section_appears_after_voice() -> None:
    """Ordering is load-bearing. Voice sets tone, Friday Format sets shape,
    and the section says 'Voice above' in its first line."""
    text = template_text()
    assert text.index("## Voice") < text.index(SECTION_HEADING), (
        "Friday Format must follow ## Voice; its opening line refers back to it"
    )
    assert text.index(SECTION_HEADING) < text.index("## What I work on"), (
        "Friday Format belongs with the writing rules, not after the config"
    )


def test_no_operator_name_anywhere_in_template() -> None:
    """Public repository. Also covered by test_cleanroom.py; duplicated so a
    failure here names Friday Format as the likely cause."""
    assert not re.search(r"Ronsley", template_text(), re.IGNORECASE)


def test_no_em_dashes_in_template() -> None:
    matches = re.findall(r"[–—―]", template_text())
    assert not matches, f"found {len(matches)} em-dash-like characters"


def test_no_bracket_placeholders_inside_friday_format() -> None:
    """The rest of the template is a fill-in-the-blanks exercise. This section
    is not. A buyer who never edits it still gets working reply rules."""
    section = friday_format_section()
    brackets = re.findall(r"\[[^\]]+\]", section)
    assert not brackets, f"Friday Format carries placeholders: {brackets}"


def test_section_says_it_needs_no_editing() -> None:
    """The template's own instruction is 'Replace every [bracket] below'. Say
    plainly that this section is the exception, or a buyer will hunt for one."""
    assert "needs editing" in friday_format_section()


def test_every_original_heading_survives() -> None:
    """Template preservation, checked against a literal list rather than a
    count, so a rename is caught as well as a deletion."""
    text = template_text()
    missing = [h for h in ORIGINAL_HEADINGS if h not in text]
    assert not missing, f"adding Friday Format removed headings: {missing}"


@pytest.mark.parametrize("limit", ["20 words", "22 words", "150 words", "200 words"])
def test_sentence_limits_are_stated_as_numbers(limit: str) -> None:
    """A prose paraphrase like 'keep sentences short' is not a limit. The
    numbers have to survive every future edit."""
    assert limit in friday_format_section()


def test_no_precedence_clause() -> None:
    """Friday OG and the paid tiers carry a clause saying Friday Format
    outranks the output-style word budget. Shortcuts ships no output styles,
    so that clause here would point at nothing."""
    section = friday_format_section().lower()
    assert "output style" not in section
    assert "outranks" not in section


def test_second_person_not_third() -> None:
    """Buyer copy addresses the reader directly. 'the founder' is what the Mk5
    export map produces from a leaked 'Ronsley', and it reads as a stranger.

    The label phrases are allowed inside the address-by-name rule, which has to
    quote them to ban them. Everywhere else they are a failure.
    """
    section = friday_format_section()
    body = "\n".join(
        line for line in section.splitlines()
        if not line.startswith("**Address me by name.**")
    )
    for banned in ("the founder", "the buyer", " his ", " her "):
        assert banned not in body, f"third-person phrasing {banned!r} in buyer copy"
    assert " you" in section, "the section never addresses the reader"


def test_address_by_name_rule_is_present() -> None:
    """Ronsley, 2026-08-02: "instead of Ronsley ... Friday should use the
    user's name like me." A reply that says "the user" is the failure."""
    section = friday_format_section()
    assert "**Address me by name.**" in section, "the address-by-name rule is missing"
    for label in ('"the user"', '"the founder"', '"the operator"'):
        assert label in section, f"the rule does not ban the label {label}"


def test_name_resolution_has_a_source_and_a_fallback() -> None:
    """A rule that says 'use their name' without saying where the name comes
    from is a wish. Shortcuts resolves it from the template's own Identity
    section, and says what to do when that is still a placeholder."""
    section = friday_format_section()
    assert "Identity section at the top of this file" in section
    assert "what I tell you to call me" in section
    assert 'say "you" and ask me once' in section


def test_name_use_is_bounded() -> None:
    """Unbounded 'use their name' produces a reply that says it every
    paragraph, which reads worse than not using it at all."""
    section = friday_format_section()
    assert "Names land, they do not decorate" in section
    assert "Not in every paragraph" in section


def test_no_operator_name_in_the_name_rule() -> None:
    """The global Friday OG copy of this rule names Ronsley, because that is
    what it resolves to there. The public template must not inherit that."""
    assert "Ronsley" not in friday_format_section()
