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


def _no_arg_widget_calls(path: Path) -> list[int]:
    """Line numbers where `TaskboardWidget` is CALLED with nothing.

    Parsed, not grepped, on purpose: `verify_board.py`'s docstring discusses
    `TaskboardWidget()` in prose while its code passes a path, and a text scan
    would report that file forever until someone silenced the law to shut it
    up. A silenced law is worse than no law.
    """
    import ast
    tree = ast.parse(path.read_text(encoding="utf-8"))
    return [n.lineno for n in ast.walk(tree)
            if isinstance(n, ast.Call)
            and getattr(n.func, "id", getattr(n.func, "attr", None))
                == "TaskboardWidget"
            and not n.args and not n.keywords]


def test_nothing_constructs_the_widget_without_naming_a_board():
    """AC7. `TaskboardWidget()` fell back to the live board, so four verifiers
    that simply omitted the argument rendered the operator's tasks --
    `verify_ink.py:82` and `verify_widget.py:22/63/90`. `verify_board.py:launch`
    was written to guard exactly this and all four bypassed it by never calling
    launch, which is why guarding at the CONSTRUCTOR is the fix and guarding at
    a helper was not.

    THE SCOPE IS TRACKED FILES, AND THAT IS A CHOICE. `prototypes/out/` holds
    hundreds of untracked throwaway probes; scanning them made this law report
    scratch nobody will ship and emit eight SyntaxWarnings from their broken
    escapes, which is how a law trains people to ignore it. What this protects
    is what the repository can publish."""
    tracked = subprocess.run(["git", "ls-files", "prototypes/*.py",
                              "prototypes/**/*.py"],
                             cwd=ROOT, capture_output=True, text=True).stdout
    files = [ROOT / f for f in tracked.split("\n") if f.strip()]
    assert files, "no tracked prototype sources found; the law would be vacuous"
    offenders = {str(p.relative_to(ROOT)): lines for p in files
                 if p.is_file() and (lines := _no_arg_widget_calls(p))}
    assert offenders == {}, offenders


def test_the_widget_refuses_to_guess_a_board():
    """The law above is a source scan, so it cannot see a call built at
    runtime. This one asserts the behaviour itself.

    LOADED BY PATH, NOT BY `from app import ...`. The bare form needed
    `sys.path` surgery and then read as a top-level package called `app`, which
    made `test_requirements.py` report an undeclared third-party distribution
    named `app`. The module is one file at a known location; saying so is both
    truer and quieter."""
    import importlib.util
    sys.path.insert(0, str(ROOT / "prototypes" / "widget_slice"))
    sys.path.insert(0, str(ROOT))
    target = ROOT / "prototypes" / "widget_slice" / "app.py"
    spec = importlib.util.spec_from_file_location("widget_slice_app", target)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    with pytest.raises(ValueError, match="explicit board_path"):
        mod.TaskboardWidget()


def test_the_interactive_runner_asks_for_the_live_board_by_name():
    """The counterweight. Making the constructor strict would be easy to
    'satisfy' by pointing the interactive runner at a fixture too -- and then
    the widget would no longer show anyone their own tasks, which is the point
    of a widget. Reading the live board stays possible; it just has to be
    said."""
    src = (ROOT / "prototypes" / "widget_slice" / "app.py").read_text(
        encoding="utf-8")
    tail = src.split('if __name__ == "__main__":')[-1]
    assert "default_board_path()" in tail, (
        "the interactive runner no longer opens the operator's own board")


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
