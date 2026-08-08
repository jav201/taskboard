"""The gate is EXECUTED here, never read.

A hook is the one kind of code whose whole value is what it does at a moment
nobody is watching, so asserting on its source would be exactly the wrong
shape. Every test below stages real content in a real throwaway repository and
runs the real script.

BOTH DIRECTIONS AND THE FAIL-CLOSED CASE. A gate that refuses everything passes
the leak tests; a gate that refuses nothing passes the clean test; a gate that
quietly succeeds when it cannot read the board passes both while protecting
nothing -- and that last one is the dangerous shape, because it is believed.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "precommit_privacy.py"

PRIVATE_TITLE = "Telemetry_Ingestion_Navigation"


def git(repo, *args, **kw):
    return subprocess.run(["git", *args], cwd=repo, capture_output=True,
                          text=True, **kw)


@pytest.fixture
def repo(tmp_path):
    r = tmp_path / "repo"
    r.mkdir()
    git(r, "init", "-q")
    git(r, "config", "user.email", "t@example.invalid")
    git(r, "config", "user.name", "t")
    return r


@pytest.fixture
def board(tmp_path):
    p = tmp_path / "board.json"
    p.write_text(json.dumps({
        "projects": [{"name": "Atlas Pipeline (ML)"}],
        "tasks": [{"title": PRIVATE_TITLE}],
    }), encoding="utf-8")
    return p


def run_gate(repo, board_path):
    env = dict(os.environ, TASKBOARD_BOARD=str(board_path))
    env.pop("TASKBOARD_PRIVACY_SWEEP", None)
    return subprocess.run([sys.executable, str(SCRIPT)], cwd=repo, env=env,
                          capture_output=True, text=True)


def stage(repo, name, text):
    (repo / name).write_text(text, encoding="utf-8")
    git(repo, "add", name)


def test_a_staged_leak_is_refused_and_the_file_is_named(repo, board):
    stage(repo, "notes.md", f"renamed {PRIVATE_TITLE} this week")
    r = run_gate(repo, board)
    assert r.returncode != 0, "the gate let a leak through"
    assert "notes.md" in r.stderr, r.stderr
    assert PRIVATE_TITLE in r.stderr, "refused without naming what it found"


def test_a_truncated_leak_is_refused_too(repo, board):
    """The regression the sweeper exists for, at the gate: an ellipsised label
    puts part of a name in a file, and part is enough."""
    stage(repo, "row.txt", f"| {PRIVATE_TITLE[:16]}… |")
    assert run_gate(repo, board).returncode != 0


def test_clean_staged_content_commits(repo, board):
    stage(repo, "ok.py", "def render(width):\n    return ' ' * width\n")
    r = run_gate(repo, board)
    assert r.returncode == 0, r.stderr


def test_it_reads_the_INDEX_not_the_working_tree(repo, board):
    """The staged version is what gets committed. A gate reading the file on
    disk would wave through a commit whose staged blob leaks, which is the
    exact case a person creates by fixing a file and forgetting to re-add it."""
    stage(repo, "x.md", f"leaking {PRIVATE_TITLE}")
    (repo / "x.md").write_text("clean now", encoding="utf-8")   # NOT re-added
    r = run_gate(repo, board)
    assert r.returncode != 0, "the gate judged the working tree, not the index"


def test_it_fails_closed_when_it_cannot_read_the_board(repo, tmp_path):
    stage(repo, "ok.md", "nothing private here")
    missing = tmp_path / "no-such-board.json"
    r = run_gate(repo, missing)
    assert r.returncode != 0
    assert "CANNOT RUN" in r.stderr


def test_it_fails_closed_on_a_corrupt_board(repo, tmp_path):
    stage(repo, "ok.md", "nothing private here")
    bad = tmp_path / "bad.json"
    bad.write_text("{ not json", encoding="utf-8")
    r = run_gate(repo, bad)
    assert r.returncode != 0
    assert "CANNOT RUN" in r.stderr


def test_the_escape_hatch_is_explicit_and_only_that(repo, board):
    """Bypassing must be a deliberate act, not a default. Asserted alongside
    the leak case so the hatch cannot quietly become the behaviour."""
    stage(repo, "notes.md", f"renamed {PRIVATE_TITLE} this week")
    env = dict(os.environ, TASKBOARD_BOARD=str(board),
               TASKBOARD_PRIVACY_SWEEP="off")
    r = subprocess.run([sys.executable, str(SCRIPT)], cwd=repo, env=env,
                       capture_output=True, text=True)
    assert r.returncode == 0
    assert "disabled" in r.stderr


def test_binary_staged_files_do_not_break_the_gate(repo, board):
    """A png whose bytes are not utf-8 must be skipped, not crash the commit."""
    (repo / "img.png").write_bytes(b"\x89PNG\r\n\x1a\n\xff\xfe\x00binary")
    git(repo, "add", "img.png")
    stage(repo, "ok.md", "fine")
    assert run_gate(repo, board).returncode == 0


def test_the_hook_wired_in_this_repo_points_at_the_script():
    """The logic being correct is worthless if nothing calls it. `core.hooksPath`
    is repo config, so this asserts the wiring a fresh clone must repeat."""
    hook = ROOT / ".githooks" / "pre-commit"
    assert hook.is_file(), "the hook file is missing"
    assert "precommit_privacy.py" in hook.read_text(encoding="utf-8")
    got = subprocess.run(["git", "config", "core.hooksPath"], cwd=ROOT,
                         capture_output=True, text=True).stdout.strip()
    assert got == ".githooks", (
        f"core.hooksPath is {got!r}; run: git config core.hooksPath .githooks")


# --------------------------------------------------------------------------- #
# the CI gate — the half of the protection that a fresh clone cannot skip
# --------------------------------------------------------------------------- #
def test_ci_actually_runs_the_suite_and_enables_the_hooks():
    """A workflow that stops invoking the suite is a green tick over nothing,
    and nothing else in the repository would notice.

    Two claims, both load-bearing:
      * it RUNS pytest — otherwise CI enforces no law at all;
      * it sets `core.hooksPath` — CI is a fresh clone every time, so without
        that step `test_the_hook_wired_in_this_repo_points_at_the_script` fails
        there and the obvious "fix" is to weaken that law instead of doing the
        setup it exists to demand.

    Parsed as YAML rather than grepped, so a command mentioned in a comment
    cannot satisfy it."""
    import re
    import yaml   # declared in requirements.txt — and it was NOT, on the
                  # first draft of this test. `test_requirements.py` named
                  # the file and the missing dist on the next run.
    wf = ROOT / ".github" / "workflows" / "ci.yml"
    assert wf.is_file(), "the CI workflow is gone"
    spec = yaml.safe_load(wf.read_text(encoding="utf-8"))
    runs = [s.get("run", "") for s in spec["jobs"]["suite"]["steps"]]
    # INVOKED, not merely mentioned. `any("pytest" in r)` was the first version
    # and a mutation replacing the step with `echo 'no pytest here'` SURVIVED
    # it — the word was in the string, so the substring test was satisfied by a
    # command that runs nothing.
    assert any(re.match(r"(python -m )?pytest\b", r.strip()) for r in runs), (
        f"CI never INVOKES the suite: {runs}")
    assert any("core.hooksPath" in r for r in runs), (
        f"CI does not enable the repository's hooks: {runs}")


def test_ci_tests_the_python_floor_the_project_promises():
    """`pyproject.toml` says >= 3.10. A gate that only exercises the version on
    the author's machine does not test that promise, and the promise is what a
    fresh clone relies on."""
    import re
    import yaml
    floor = re.search(r'requires-python\s*=\s*">=\s*([\d.]+)"',
                      (ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert floor, "pyproject no longer declares requires-python"
    spec = yaml.safe_load((ROOT / ".github" / "workflows" / "ci.yml")
                          .read_text(encoding="utf-8"))
    versions = spec["jobs"]["suite"]["strategy"]["matrix"]["python-version"]
    assert floor.group(1) in versions, (
        f"pyproject promises >= {floor.group(1)}; CI runs {versions}")
