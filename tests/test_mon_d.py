"""The one `Mon D` formatter (batch 2026-10-07-batch-05, LLR-1102.1 · AT-1102).

`def _md` shipped three times — `models.py`, `views.py`, `app.py` — with the same
body `f"{d:%b} {d.day}"`. The dedup keeps the `models` definition and re-points
the other two at it. This pin proves the package holds exactly one definition and
that every access path renders identical strings across a boundary sweep.

RED on base: the identity arm fails while the three definitions are distinct
objects (even if byte-identical), and a consumer shadowing a divergent body fails
the sweep arm.
"""
from __future__ import annotations

from datetime import date

from taskboard import app, models, views


def _sweep():
    """14 boundary dates: every month start, the year end (Dec 31) and the leap
    day (Feb 29, 2024 is a leap year)."""
    return [date(2024, m, 1) for m in range(1, 13)] + [date(2023, 12, 31),
                                                       date(2024, 2, 29)]


def test_one_md_definition_shared_by_all():
    """LLR-1102.1: `views._md` and `app._md` are the SAME object as `models._md`
    — the package holds exactly one `def _md`."""
    assert views._md is models._md
    assert app._md is models._md


def test_md_renders_identically_through_every_access_path():
    """LLR-1102.1: the sweep renders identical strings through all three access
    paths, and matches the pinned literal shape for the boundary dates."""
    assert models._md(date(2024, 2, 29)) == "Feb 29"
    assert models._md(date(2023, 12, 31)) == "Dec 31"
    for d in _sweep():
        want = models._md(d)
        assert views._md(d) == want
        assert app._md(d) == want
