"""The template store's unit layer (batch 2026-10-07-batch-07, increment 001).

HLR-1301 / LLR-1301.1 · AT-1301.

`settings["templates"]` is a list of ``{"name": str, "tasks": [{"title": str,
"notes"?: str, "wait": int|null}]}``. The read is lenient — a malformed entry is
skipped (non-text name, empty title, non-list tasks, bad task fields), never
raising; a `wait` that is not a valid earlier index reads as None (the task is
kept, the link dropped). Two factory presets ship always, listed AFTER user
templates: `Simple chain` (Plan → Build → Ship) and `Bugfix` (Triage → Fix →
Verify).
"""
from __future__ import annotations

from pathlib import Path

from taskboard.models import Board, Template, TemplateTask, templates


def _board(settings: dict) -> Board:
    return Board([], [], Path("store.json"), settings)


def test_round_trip_reads_back_equal():
    """A well-formed settings list reads back equal — user templates first, the
    two presets after."""
    b = _board({"templates": [
        {"name": "Release", "tasks": [
            {"title": "Cut branch"},
            {"title": "Tag", "wait": 0},
            {"title": "Announce", "wait": 1, "notes": "changelog"},
        ]},
    ]})
    got = templates(b)
    assert got[0] == Template("Release", (
        TemplateTask("Cut branch"),
        TemplateTask("Tag", wait=0),
        TemplateTask("Announce", notes="changelog", wait=1),
    ))
    assert [t.name for t in got[1:]] == ["Simple chain", "Bugfix"]


def test_lenient_read_skips_junk_and_drops_bad_waits():
    """A junk list yields only the valid entries; a malformed `wait` is dropped
    (the link) but the task is kept."""
    b = _board({"templates": [
        "junk",                                              # not a dict
        {"name": 42, "tasks": [{"title": "A"}]},             # non-text name
        {"name": "No tasks", "tasks": "nope"},               # non-list tasks
        {"name": "Empty title", "tasks": [{"title": ""}]},   # empty title
        {"name": "Bad wait", "tasks": [
            {"title": "A"},
            {"title": "B", "wait": 5},                       # forward -> dropped
            {"title": "C", "wait": "x"},                     # non-int -> dropped
        ]},
        {"name": "Good", "tasks": [
            {"title": "A"},
            {"title": "B", "wait": 0},
        ]},
    ]})
    user = [t for t in templates(b) if t.name not in ("Simple chain", "Bugfix")]
    assert [t.name for t in user] == ["Bad wait", "Good"]
    bad = user[0]
    assert [x.title for x in bad.tasks] == ["A", "B", "C"]
    assert [x.wait for x in bad.tasks] == [None, None, None]
    assert user[1].tasks[1].wait == 0


def test_presets_present_with_names_and_counts():
    """The two factory presets ship with their exact names, shapes and counts."""
    got = templates(_board({}))
    assert [(t.name, len(t.tasks)) for t in got] == [("Simple chain", 3), ("Bugfix", 3)]
    assert [x.title for x in got[0].tasks] == ["Plan", "Build", "Ship"]
    assert [x.wait for x in got[0].tasks] == [None, 0, 1]
    assert [x.title for x in got[1].tasks] == ["Triage", "Fix", "Verify"]
    assert [x.wait for x in got[1].tasks] == [None, 0, 1]


def test_no_user_templates_returns_presets_only():
    """The boundary: an absent or empty settings list -> the presets only."""
    assert [t.name for t in templates(_board({}))] == ["Simple chain", "Bugfix"]
    assert [t.name for t in templates(_board({"templates": []}))] == \
        ["Simple chain", "Bugfix"]
