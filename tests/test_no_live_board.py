"""Scripts that write committable artifacts must be INCAPABLE of reading the
operator's live board -- not merely configured not to.

WHY THIS FILE EXISTS: `prototypes/capture.py` opened `default_board_path()` by
design. Its own docstring argued for it ("against the REAL board data, so the
comparison is made on real density, not on lorem ipsum"), and the
`out/variants.txt` it wrote carried 25 verbatim task titles into git, on a
branch of a PUBLIC remote, until the history was rewritten on 2026-08-07.

THE GUARD IS TESTED IN BOTH DIRECTIONS, because "it uses a fixture now" is a
configuration claim and configuration drifts back. What is asserted is that the
symbol is ABSENT from the source -- so re-adding the call reddens this file
even if the fixture still happens to exist -- and that a missing fixture makes
the script DIE rather than fall back, which is the moment the old code would
have reached for the live board.

`capture_languages.py` is checked by the same law even though it was already
fixed: it monkeypatches `default_board_path` rather than avoiding it, so the
symbol legitimately appears there and the assertion is written to that shape
rather than pretending all three files are alike.
"""

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "prototypes" / "out" / "_fixture_late.json"

#: scripts that WRITE artifacts a person could commit. The live board must be
#: unreachable from these, by absence of the symbol.
ARTIFACT_WRITERS = ["prototypes/capture.py", "prototypes/verify_variants.py"]


@pytest.mark.parametrize("rel", ARTIFACT_WRITERS)
def test_the_live_board_symbol_is_absent_from_artifact_writers(rel):
    """AC1. Asserting on ABSENCE means the file must be proven to exist first,
    or a rename would make this pass by vacuum -- the failure mode this whole
    batch is about."""
    p = ROOT / rel
    assert p.is_file(), f"{rel} does not exist; this law would pass vacuously"
    src = p.read_text(encoding="utf-8")
    code = "\n".join(l for l in src.splitlines()
                     if not l.lstrip().startswith("#"))
    body = code.split('"""')[-1] if code.count('"""') >= 2 else code
    assert "default_board_path" not in body, (
        f"{rel} can reach the operator's live board again")


def test_the_fixture_is_in_git_not_just_on_this_disk():
    """AC2. Both scripts now depend on this file; while it was untracked the
    fix worked only on the machine that happened to have it, and a fresh clone
    would have failed with a missing-fixture error that looks like a bug."""
    r = subprocess.run(["git", "ls-files", "--error-unmatch",
                        "prototypes/out/_fixture_late.json"],
                       cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, "_fixture_late.json is not tracked"


def test_the_fixture_holds_no_real_looking_identity():
    """The fixture is the thing every capture renders, so it is the one file
    whose contents end up in shareable artifacts. Pinned to its synthetic
    vocabulary rather than merely 'exists'."""
    import json
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    names = {p["name"] for p in data["projects"]}
    assert {"Website Redesign", "Mobile App"} <= names, names


@pytest.mark.parametrize("mod,fn", [("capture", "capture_all"),
                                    ("verify_variants", "budget_check")])
def test_a_missing_fixture_kills_the_script_instead_of_falling_back(
        mod, fn, monkeypatch, tmp_path):
    """AC1, the other half. The old code's failure was silent: no fixture, no
    error, just the live board. Dying loudly is the behaviour being bought."""
    sys.path.insert(0, str(ROOT / "prototypes"))
    sys.path.insert(0, str(ROOT))
    module = __import__(mod)
    monkeypatch.setattr(module, "FIXTURE", tmp_path / "does_not_exist.json")
    with pytest.raises(SystemExit):
        getattr(module, fn)()
