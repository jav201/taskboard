"""Find files that carry a private board's data.

WHY THIS EXISTS: on 2026-08-07 a generated capture of the operator's live board
(25 verbatim task titles) was found committed on a branch of a PUBLIC remote,
and three more real strings on `main` itself, public since 2026-07-24. Both
were removed by hand. A hand removal is an act, not a defence: the generator
that produced the capture was still reading `~/.taskboard/board.json`, so the
next run restored it.

TRUNCATED FORMS ARE THE POINT, NOT AN EXTRA. The first hand scrub replaced the
19-character token `Telemetry_Ingestion` everywhere and declared the branch
clean. It was not: `tests/test_app.py` asserted on `Telemetry_Ingestio` -- the
same name minus its last letter, because the assertion was written against a
label column that ELLIPSISES. Six rewritten commits still carried it and the
test suite is what noticed. A sweeper that only matches whole strings would
have signed off on exactly the tree that was still leaking, which is why
`prefixes()` below is load-bearing and has its own test.

THE FLOOR OF 10 IS A REAL TRADE, STATED. Prefixes shorter than that stop being
distinctive -- `Training` alone is an ordinary English word and matching it
would flag every file discussing training. So this sweeper CANNOT see a leak
truncated below 10 characters, and says so here rather than implying it is
exhaustive.
"""
from __future__ import annotations

import json
from pathlib import Path

#: shortest prefix still treated as identifying. See the module docstring --
#: this is a floor on sensitivity, deliberately chosen, not a tuning knob.
MIN_PREFIX = 10

#: strings shorter than this are not considered identifying at all.
MIN_STRING = 12

SKIP_SUFFIXES = {".png", ".gif", ".jpg", ".jpeg", ".ico", ".pyc", ".zip",
                 ".woff", ".woff2", ".ttf", ".pdf", ".webp", ".mp4"}


def board_strings(board_path: str | Path) -> list[str]:
    """Every project name and task title worth protecting, longest first.

    Longest first matters for `prefixes`: a shorter string that is a prefix of
    a longer one would otherwise report the short match and hide which record
    actually leaked.
    """
    data = json.loads(Path(board_path).read_text(encoding="utf-8"))
    out = [p.get("name", "") for p in data.get("projects", [])]
    out += [t.get("title", "") for t in data.get("tasks", [])]
    return sorted({s for s in out if s and len(s) >= MIN_STRING},
                  key=len, reverse=True)


def prefixes(s: str) -> list[str]:
    """`s` and every prefix of it down to MIN_PREFIX, longest first.

    This is what catches a name that reached a file through an ellipsising
    label rather than whole.
    """
    return [s[:k] for k in range(len(s), MIN_PREFIX - 1, -1)]


def sweep(board_path: str | Path, files) -> dict[str, str]:
    """Map each leaking file to the LONGEST private string found in it.

    Only the longest is reported per file: a leak of one title also matches all
    of its own shorter prefixes, and listing those would inflate a single
    finding into dozens.
    """
    needles = [(p, s) for s in board_strings(board_path) for p in prefixes(s)]
    found: dict[str, str] = {}
    for f in files:
        path = Path(f)
        if path.suffix.lower() in SKIP_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for needle, whole in needles:
            if needle in text:
                found[str(f)] = whole
                break
    return found
