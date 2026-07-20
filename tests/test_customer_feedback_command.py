from pathlib import Path

from tests.test_commands import parse_frontmatter

REPO_ROOT = Path(__file__).parent.parent
COMMAND_PATH = REPO_ROOT / "commands" / "customer-feedback.md"


def get_customer_feedback_command():
    return COMMAND_PATH.read_text(encoding="utf-8")


def test_customer_feedback_command_frontmatter():
    text = get_customer_feedback_command()
    fm, body = parse_frontmatter(text)

    assert fm["name"] == "customer-feedback"
    assert "friday/customer-feedback.md" in fm["description"]
    assert "friday/voice.md" in fm["description"]
    assert "pasted customer feedback" in fm["description"]
    assert body.startswith("# /customer-feedback")


def test_customer_feedback_accepts_paste_and_sanitized_files():
    text = get_customer_feedback_command()

    required_phrases = [
        "Paste the customer feedback",
        "sanitized local Markdown or text files",
        "read only `.md`, `.markdown`, or `.txt` files",
        "explicitly named",
        "refuse to read it and ask for a sanitized text file instead",
    ]

    for phrase in required_phrases:
        assert phrase in text


def test_customer_feedback_preserves_voice_and_privacy():
    text = get_customer_feedback_command()

    assert "Check whether `friday/voice.md` exists" in text
    assert "write all output in the founder's voice" in text
    assert "secret, credential, private key, environment file, token dump" in text
    assert "Do not fabricate quotes, customer counts, sentiment" in text


def test_customer_feedback_writes_expected_sections():
    text = get_customer_feedback_command()

    required_phrases = [
        "Write the result to `friday/customer-feedback.md`",
        "Create the `friday/` folder if it does not exist",
        "## Recurring themes",
        "## One-off signals",
        "## Unanswered questions",
        "## Prioritized actions",
        "### Do now",
        "### Test next",
        "### Watch",
        "### Do not act on yet",
        "Customer feedback synthesis saved to `friday/customer-feedback.md`",
    ]

    for phrase in required_phrases:
        assert phrase in text
