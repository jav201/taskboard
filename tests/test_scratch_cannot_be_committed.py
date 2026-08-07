"""`git add -A` must not be able to swallow the scratch yard.

WHY THIS FILE EXISTS: `prototypes/out/` held ~890 untracked files -- probe
scripts, logs, rendered boards -- and nothing in `.gitignore` covered it. One
`git add -A` would have committed every one. That directory is also where the
capture scripts WRITE, so the accident and the leak of 2026-08-07 shared a
path: `out/variants.txt` reached a public remote from exactly here.

BOTH DIRECTIONS ARE ASSERTED. Ignoring the whole yard is easy and wrong: the
fixture every capture reads, and the four reviewed `.svg` artifacts, live in
the same directory and must stay committable. A rule that ignores everything
would pass a "scratch is ignored" test and silently drop the fixture out of the
repo -- which is the state this batch already had to fix once.
"""

import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]

MUST_BE_IGNORED = [
    "prototypes/out/_probe999.py",
    "prototypes/out/_scratch.log",
    "prototypes/out/variants.txt",       # the file that actually leaked
    "prototypes/out/some-render.svg",
]

MUST_STAY_COMMITTABLE = [
    "prototypes/out/_fixture_late.json",
    "prototypes/out/kanban-baseline.svg",
    "prototypes/out/kanban-flow.svg",
    "prototypes/out/kanban-matrix.svg",
    "prototypes/out/kanban-triage.svg",
]


def ignored(rel: str) -> bool:
    """Does `.gitignore` ITSELF ignore this path -- index not consulted.

    `--no-index` is load-bearing and was added after the mutation harness
    caught its absence. Without it, `git check-ignore` reports an already-
    TRACKED file as not-ignored no matter what the rules say, so deleting
    `!prototypes/out/_fixture_late.json` left every test in this file green:
    the negations were untested and the law was measuring the index, not the
    rule it claims to protect.

    It also answers for paths that need not exist, which is what lets this
    test name `variants.txt` -- a file that must never come back.
    """
    return subprocess.run(["git", "check-ignore", "-q", "--no-index", rel],
                          cwd=ROOT).returncode == 0


@pytest.mark.parametrize("rel", MUST_BE_IGNORED)
def test_scratch_output_cannot_be_staged(rel):
    assert ignored(rel), f"{rel} would be committed by `git add -A`"


@pytest.mark.parametrize("rel", MUST_STAY_COMMITTABLE)
def test_the_inputs_and_reviewed_artifacts_stay_committable(rel):
    """THE OTHER DIRECTION. Without this, ignoring the whole directory passes
    every test above and quietly removes the fixture from the repository."""
    assert not ignored(rel), f"{rel} is a repository file and must not be ignored"
    r = subprocess.run(["git", "ls-files", "--error-unmatch", rel],
                       cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, f"{rel} is not tracked"


def test_the_ignored_directory_is_the_one_the_capture_writes_into():
    """Ties the rule to the WRITER, so the two cannot drift apart.

    This was first written as `len(list(out.iterdir())) > 100` -- "the yard is
    full, so the rule is not theoretical". That asserted transient local state:
    it passed in the worktree that happened to hold ~890 scratch files and
    failed the moment the same test ran on a fresh checkout, where the
    directory holds only the five tracked files. A law that depends on what a
    machine happens to contain is not a law about the repository.

    What actually matters is durable: `capture.py` writes into exactly the
    directory `.gitignore` covers. If someone repoints `OUT`, the ignore rule
    silently stops covering the output and this goes red."""
    src = (ROOT / "prototypes" / "capture.py").read_text(encoding="utf-8")
    assert 'OUT = ROOT / "prototypes" / "out"' in src, (
        "capture.py no longer writes into the directory .gitignore covers")
    assert ignored("prototypes/out/variants.txt"), (
        "the capture's own output filename is not covered by the rule")
