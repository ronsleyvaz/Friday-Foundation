"""
Install Witness workflow tests.

.github/workflows/install-witness.yml runs the README's buyer install command
verbatim on a fresh ubuntu-latest and a fresh macos-latest runner every Friday,
plus on manual dispatch. These tests parse the workflow file itself and pin it
against README.md, so the two cannot drift apart silently.

The proprietary-term and em-dash sweep for everything under .github/ (this
workflow included) already runs in test_content_sweep.py (SWEEP_DIRS includes
".github"). Not duplicated here.
"""
import re
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).parent.parent
WORKFLOW_PATH = REPO_ROOT / ".github" / "workflows" / "install-witness.yml"
README_PATH = REPO_ROOT / "README.md"


def load_workflow():
    return yaml.safe_load(WORKFLOW_PATH.read_text())


def on_section(workflow):
    """PyYAML parses the unquoted `on:` key as the boolean True (YAML 1.1
    resolver), not the string "on". Handle both spellings rather than
    forcing the workflow file to quote a key GitHub Actions itself writes
    unquoted everywhere."""
    return workflow["on"] if "on" in workflow else workflow[True]


def all_steps(workflow):
    steps = []
    for job in workflow["jobs"].values():
        steps.extend(job.get("steps", []))
    return steps


def readme_install_command():
    """The first fenced-code line in README.md matching the buyer's one-line
    curl | install.sh | bash command (README.md:19)."""
    text = README_PATH.read_text()
    match = re.search(r"^curl -fsSL \S*install\.sh \| bash$", text, re.MULTILINE)
    assert match, "README.md has no 'curl ...install.sh | bash' line to pin against"
    return match.group(0)


def test_workflow_file_exists():
    assert WORKFLOW_PATH.exists(), "install-witness.yml is missing"


def test_workflow_named_install_witness():
    workflow = load_workflow()
    assert workflow.get("name") == "Install Witness"


def test_cron_matches_friday_0800_asia_calcutta():
    workflow = load_workflow()
    schedules = on_section(workflow)["schedule"]
    crons = [s["cron"] for s in schedules]
    assert "30 2 * * 5" in crons, f"expected cron '30 2 * * 5', got {crons}"


def test_workflow_dispatch_present():
    workflow = load_workflow()
    assert "workflow_dispatch" in on_section(workflow)


def test_matrix_has_both_operating_systems():
    workflow = load_workflow()
    matrices = [
        job["strategy"]["matrix"]
        for job in workflow["jobs"].values()
        if "strategy" in job and "matrix" in job["strategy"]
    ]
    assert matrices, "no job defines a matrix"
    oses = matrices[0].get("os", [])
    assert "ubuntu-latest" in oses
    assert "macos-latest" in oses


def test_matrix_fail_fast_is_false():
    workflow = load_workflow()
    for job in workflow["jobs"].values():
        strategy = job.get("strategy", {})
        if "matrix" in strategy:
            assert strategy.get("fail-fast") is False
            return
    raise AssertionError("no job with a matrix strategy found")


def test_no_checkout_step():
    workflow = load_workflow()
    for step in all_steps(workflow):
        uses = step.get("uses", "")
        assert "actions/checkout" not in uses, (
            "Install Witness must never checkout the repo; the installer "
            "fetches everything itself, exactly like a stranger's machine would"
        )


def test_readme_install_command_appears_verbatim_in_a_run_step():
    workflow = load_workflow()
    command = readme_install_command()
    run_blocks = [step.get("run", "") for step in all_steps(workflow) if "run" in step]
    combined = "\n".join(run_blocks)
    assert command in combined, (
        "the exact README install command must appear verbatim in a run: "
        "block, so README.md and the workflow cannot drift apart"
    )


def test_every_step_is_named():
    workflow = load_workflow()
    unnamed = [step for step in all_steps(workflow) if not step.get("name")]
    assert not unnamed, f"steps without a name: {unnamed}"


def test_no_secrets_or_lead_flag_referenced():
    text = WORKFLOW_PATH.read_text()
    assert "secrets." not in text
    assert "--lead" not in text
