"""requirements.txt must actually describe what this app imports.

THE BUG THIS FILE EXISTS FOR: `pyproject.toml` declared `pillow` and
`textual-image` as runtime dependencies, but `requirements.txt` — the file whose
own header claims to pin "runtime + test deps" — listed neither. A venv built
from it could not run the suite: five tests in `test_app.py` died on ImportError
before reaching an assertion.

The cure is not a skip. `pillow` is not optional to this app — paste-image and
the image viewer are features that are supposed to work — and a skip would have
turned a broken install into a green run with a quiet note.

So the law is stated against the IMPORTS rather than against a list someone
maintains by hand: every third-party module the package or the tests import must
be covered by a declared requirement. A new dependency added without declaring
it fails here, on the machine that added it, instead of on a fresh clone.
"""

import ast
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
STDLIB = set(sys.stdlib_module_names)

# import name -> distribution name, where they differ
DIST = {"PIL": "pillow", "textual_image": "textual-image",
        "zoneinfo": "tzdata", "yaml": "pyyaml"}


def declared() -> set[str]:
    out = set()
    for raw in (ROOT / "requirements.txt").read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].strip()
        if line:
            out.add(line.split("==")[0].split(">=")[0].strip().lower())
    return out


def first_party() -> set[str]:
    """Top-level packages this repository owns, DISCOVERED not listed.

    It was the hand-written tuple `("taskboard", "tests")`, which is the same
    shape of defect this file was written to prevent one level up: a list
    someone maintains by hand. Adding `tools/` reported it as an undeclared
    third-party distribution, and the tempting fix -- append "tools" -- would
    have left the next package to hit the same wall.
    """
    names = {p.name for p in ROOT.iterdir()
             if p.is_dir() and (p / "__init__.py").exists()}
    names.add("tests")
    return names


def source_roots() -> list[pathlib.Path]:
    """Every first-party package is SCANNED, not just the two that were named.

    `tools/` was outside the sweep when it arrived, so a third-party import
    added there would have gone undeclared and this law would have said
    nothing -- silently narrower than its own docstring claims.
    """
    return [ROOT / n for n in sorted(first_party()) if (ROOT / n).is_dir()]


def test_the_scan_covers_the_packages_it_claims_to():
    """Guards the discovery above. If `first_party()` ever returns nothing --
    a renamed layout, a missing `__init__.py` -- every import below becomes
    third-party or the sweep goes empty, and the law would flip from strict to
    vacuous without anyone noticing."""
    fp = first_party()
    assert {"taskboard", "tests", "tools"} <= fp, fp
    assert all(p.is_dir() for p in source_roots())


def imported() -> dict[str, set[str]]:
    """top-level third-party module -> the files that import it."""
    found: dict[str, set[str]] = {}
    paths: list[pathlib.Path] = []
    for root in source_roots():
        paths += list(root.rglob("*.py"))
    for path in paths:
        tree = ast.parse(path.read_text(encoding="utf-8"), str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom):
                names = [node.module] if node.module and node.level == 0 else []
            else:
                continue
            for name in names:
                top = name.split(".")[0]
                if top in STDLIB or top in first_party() or not top:
                    continue
                found.setdefault(top, set()).add(path.name)
    return found


def test_every_third_party_import_is_a_declared_requirement():
    have, missing = declared(), {}
    for module, files in imported().items():
        dist = DIST.get(module, module).lower()
        if dist not in have:
            missing[f"{module} (dist {dist})"] = sorted(files)
    assert not missing, (
        "imported but not declared in requirements.txt — a fresh venv cannot run "
        f"this: {missing}")


def test_pillow_is_declared_because_it_is_not_optional():
    """The specific regression, named. `pillow` is a RUNTIME dependency in
    pyproject; if it ever leaves requirements.txt again, the five image tests go
    back to failing on a fresh clone and this says so directly."""
    assert "pillow" in declared()
    assert "PIL" in imported(), "fixture is stale: nothing imports PIL any more"


def test_requirements_and_pyproject_do_not_contradict_each_other():
    """Two files declare dependencies and they drifted apart once already. Any
    runtime dependency pyproject names must also be pinned in requirements."""
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    body = text.split("dependencies = [", 1)[1].split("]", 1)[0]
    runtime = {p.strip().strip('"').split(">=")[0].split("==")[0].lower()
               for p in body.split(",") if p.strip()}
    assert runtime, "fixture failed to parse pyproject's dependency list"
    assert not (runtime - declared()), (
        f"declared in pyproject but not pinned in requirements.txt: "
        f"{sorted(runtime - declared())}")
