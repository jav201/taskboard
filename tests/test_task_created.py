"""`Task.created`: every persisted task records when it was added; old boards are never
rewritten (Inc L, dev-flow-v3-beta; HLR-4301, HLR-4302 · LLR-4301.1..4301.11,
LLR-4302.1..4302.7 · AT-4302, AT-4303).

WHY. The field report behind US-4301: the owner (`username_subject`) captures tasks in a
hurry and must later find them by WHEN THEY WERE ADDED, not by their planned dates — so
every path that creates a persisted task (the editor, a template insert, the link picker's
create row, `Board.add_task`, the seeded first board) must stamp it, and every path that
merely keeps a task (edit, a project move, undo, a rescued entry) must leave the stamp as it
was. And the operator's D3: old tasks are inferred, NEVER REWRITTEN — a board written before
the field must keep its bytes through a load and a save, an add must not touch the other
entries, and the stamp (a log of working hours) must not leave the machine in the team push.

RED on the base revision (eb411e1): `Task` has no `created` field, `models.stamp` does not
exist, `Board._to_dict` takes no `with_created`, nothing stamps, and `N` opens nothing. Every
new name is reached through `added_list_fixture.need` / `created_of`, so each test fails on
an assertion with a message, never at collection. Guards that PASS on base by design: the
three byte-stability arms of TC-4315 and TC-4316 (an old board's bytes and an add's old
entries are the same at base; the mutants they catch are the increment's own).

Synthetic boards only. Clock: today 2026-11-01, now 2026-11-01T08:10:00 (`models.datetime`
monkeypatched where `stamp()` reads it, P-D-4); TC-4303 / TC-4306 use a clock that moves one
second per call (P-D-10, P-S-2), so a stamp taken per task instead of per insert is caught.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import textwrap
from datetime import datetime, timedelta
from pathlib import Path

import pytest
from textual.widgets import Input

import added_list_fixture as fx
from added_list_fixture import (created_of, home, need, need_created_field, open_list,  # noqa: F401
                                open_s_app, press, seen)
from taskboard import history, models
from taskboard.app import TaskboardApp
from taskboard.boards import move_plan, move_project, peek_board
from taskboard.models import Board, Project, Task, _rescue_task
from taskboard.team_sync import TEAM_FILENAME, TeamState

ADD_AT = "2026-11-01T08:10:00"


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _file(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _records(path: Path) -> dict:
    return {r["id"]: r for r in _file(path)["tasks"]}


def _text(path: Path) -> str:
    return Path(path).read_bytes().decode("utf-8").replace("\r\n", "\n")


def _slice(rec: dict) -> str:
    """A task entry as it sits in a board file: `json.dumps(entry, indent=2)`, indented
    the 4 cells of the `tasks` list (Board._serialized's own dump)."""
    return textwrap.indent(json.dumps(rec, indent=2), "    ")


def _record(item, with_created: bool = True) -> dict:
    """`Board._to_dict(item, with_created=…)`, the SEC-1 form; its absence fails here."""
    try:
        return Board._to_dict(item, with_created=with_created)
    except TypeError as exc:
        pytest.fail(f"Board._to_dict takes no `with_created` (not built yet): {exc}")


def _single_board(tmp_path: Path, archived_on_alpha=False) -> Path:
    """Alpha of the S fixture as a one-board app's file (+ its history.jsonl)."""
    path = tmp_path / "alpha" / "board.json"
    b, created = fx.alpha_board(path, archived_on_alpha)
    fx.write_board(path, b, created)
    fx.write_history(path.parent, fx.ALPHA_HISTORY)
    return path


def _app(path: Path) -> TaskboardApp:
    return TaskboardApp(board_path=str(path), team_sync_interval=1e9)


# --------------------------------------------------------------------------- #
# HLR-4301 — the field and the stamp
# --------------------------------------------------------------------------- #
def test_TC_4301_created_is_an_optional_field_that_defaults_to_none():
    """TC-4301 (LLR-4301.1): `Task("x").created is None` (a transient Task is not
    stamped: NC a `default_factory` stamp); a given value is kept; positional fields keep
    their meaning (the field follows them)."""
    need_created_field()
    assert Task("x").created is None
    assert Task("x", created="2026-10-31T18:20:00").created == "2026-10-31T18:20:00"
    t = Task("Design", "pid", "Doing", "high")
    assert (t.project_id, t.phase, t.priority, t.created) == ("pid", "Doing", "high", None)


def test_TC_4302b_the_stamp_is_local_time_to_the_second(monkeypatch):
    """TC-4302b (stamp, graph-interfaces): `stamp(now)` is `now` to the second in the
    format of `history.append`'s `at`; `stamp()` reads `models.datetime.now()` — the one
    clock every creation path stamps from (P-D-4)."""
    stamp = need(models, "stamp")
    assert stamp(datetime(2026, 11, 1, 8, 10, 7, 999)) == "2026-11-01T08:10:07"
    monkeypatch.setattr(models, "datetime", fx.FixedNow, raising=False)
    assert stamp() == ADD_AT
    assert re.match(fx.STAMP_RE, stamp())


async def test_TC_4302_a_task_added_in_the_editor_is_stamped(tmp_path):
    """TC-4302 (LLR-4301.2): `a`, a title, `alt+s` (real clock) → the saved task's
    `created` is `YYYY-MM-DDTHH:MM:SS` within [t0, t1] of the test's clock reads, and the
    board file holds the same value. NC: no stamp on the add path → None."""
    path = _single_board(tmp_path)
    app = _app(path)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        t0 = datetime.now().replace(microsecond=0)
        await press(pilot, "a")
        assert type(app.screen).__name__ == "TaskModal"
        await pilot.press(*"Call the bank")
        await press(pilot, "alt+s")
        t1 = datetime.now()
        assert type(app.screen).__name__ != "TaskModal"
    new = next(t for t in app.board.tasks if t.title == "Call the bank")
    c = _records(path)[new.id].get("created")
    assert isinstance(c, str) and re.match(fx.STAMP_RE, c), f"the file holds created={c!r}"
    assert t0 <= datetime.fromisoformat(c) <= t1
    assert created_of(new) == c


async def test_TC_4303_a_template_insert_stamps_every_task_with_one_moment(tmp_path,
                                                                          monkeypatch):
    """TC-4303 (LLR-4301.3): `I`, `Simple chain` → Plan, Build, Ship each stamped, ONE
    distinct value under a clock that moves 1 s per call (NC a stamp per task: 3 values);
    the file holds it in the 3 new entries; the insert still writes no history line."""
    path = _single_board(tmp_path)
    monkeypatch.setattr(models, "datetime", fx.advancing_clock(), raising=False)
    hist_before = (path.parent / "history.jsonl").read_text(encoding="utf-8")
    app = _app(path)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        app.selected_task_id = "ta1"
        await press(pilot, "I")
        await press(pilot, "down", "enter")
    new = app.board.tasks[3:]
    assert [t.title for t in new] == ["Plan", "Build", "Ship"]
    recs = _records(path)
    values = [recs[t.id].get("created") for t in new]
    assert all(isinstance(v, str) and re.match(fx.STAMP_RE, v) for v in values), values
    assert len(set(values)) == 1, f"one insert, one stamp: {values}"
    assert fx.NOW <= datetime.fromisoformat(values[0]) <= fx.NOW + timedelta(minutes=5)
    assert [created_of(t) for t in new] == values
    assert (path.parent / "history.jsonl").read_text(encoding="utf-8") == hist_before


async def test_TC_4304_the_link_pickers_create_row_stamps_the_new_task(tmp_path, monkeypatch):
    """TC-4304 (LLR-4301.4): `_create_and_link(waiter, "new")` → the new task stamped
    `2026-11-01T08:10:00`, the waiter waits on it, and its birth record is written. NC: a
    create that bypasses the stamp → None."""
    path = _single_board(tmp_path)
    monkeypatch.setattr(models, "datetime", fx.FixedNow, raising=False)
    app = _app(path)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        waiter = app.board.task_by_id("ta1")
        app._create_and_link(waiter, "new")
        await pilot.pause()
    new = next(t for t in app.board.tasks if t.title == "new")
    assert new.id in app.board.task_by_id("ta1").depends_on
    assert any(r["task"] == new.id and r["from"] is None for r in history.read(path)[0])
    assert _records(path)[new.id].get("created") == ADD_AT
    assert created_of(new) == ADD_AT


def test_TC_4305_add_task_stamps_before_the_save_and_the_birth_record_agrees(tmp_path,
                                                                            monkeypatch):
    """TC-4305 (LLR-4301.5): `Board.add_task(Task("a"))` → the file read back holds
    `"created": "2026-11-01T08:10:00"` (NC stamp after `save()`: the key missing); the
    birth record's `at` is the same second — one clock read (P-D-4), checked under a
    clock that moves 1 s per call."""
    monkeypatch.setattr(models, "datetime", fx.FixedNow, raising=False)
    path = tmp_path / "b" / "board.json"
    b = Board([], [Task("old", id="to")], path, {})
    b.save()
    b.add_task(Task("a", id="tn"))
    assert _records(path)["tn"].get("created") == ADD_AT
    assert [r for r in history.read(path)[0] if r["task"] == "tn"] == [
        {"task": "tn", "from": None, "to": "Backlog", "at": ADD_AT}]
    assert created_of(b.task_by_id("tn")) == ADD_AT

    monkeypatch.setattr(models, "datetime", fx.advancing_clock(), raising=False)
    path2 = tmp_path / "c" / "board.json"
    b2 = Board([], [], path2, {})
    b2.add_task(Task("b", id="tq"))
    at = next(r["at"] for r in history.read(path2)[0] if r["task"] == "tq")
    assert _records(path2)["tq"].get("created") == at, "created and the birth `at` disagree"


def test_TC_4306_a_seeded_board_stamps_every_task_with_one_moment(tmp_path, monkeypatch):
    """TC-4306 (LLR-4301.6): `Board.load` on a missing file → the 16 seeded tasks share
    ONE stamp under a clock that moves 1 s per call (NC a stamp per task: 16 values); the
    file holds 16 `"created":` keys; no history is written for the seed."""
    monkeypatch.setattr(models, "datetime", fx.advancing_clock(), raising=False)
    path = tmp_path / "new" / "board.json"
    board = Board.load(path)
    assert len(board.tasks) == 16
    assert _text(path).count('"created":') == 16
    values = [created_of(t) for t in board.tasks]
    assert all(isinstance(v, str) and re.match(fx.STAMP_RE, v) for v in values), values
    assert len(set(values)) == 1, f"one seed, one stamp: {sorted(set(values))}"
    # The advancing-clock arm (P-D-10, graph-proto-D Board.load example 1; CR-4): the one
    # stamp is the clock's FIRST read, 08:10:00, and the file holds that same value in all
    # 16 keys. NC a later read (an extra clock read first, or the objects re-stamped after
    # the save): every value 08:10:01 and the file and the board disagree — one distinct
    # value still, so only this arm sees it.
    assert values == [ADD_AT] * 16, f"the seed stamp is not the first clock read: {values[:1]}"
    assert re.findall(r'"created": "([^"]*)"', _text(path)) == [ADD_AT] * 16
    assert not (path.parent / "history.jsonl").exists()


def test_TC_4307_add_task_keeps_a_created_that_is_already_set(tmp_path, monkeypatch):
    """TC-4307 (LLR-4301.7): a task arriving with `created="2026-10-01T09:00:00"` keeps
    it through `add_task` (NC: always overwrite → 08:10:00)."""
    need_created_field()
    monkeypatch.setattr(models, "datetime", fx.FixedNow, raising=False)
    path = tmp_path / "b" / "board.json"
    b = Board([], [], path, {})
    b.add_task(Task("b", id="tp", created="2026-10-01T09:00:00"))
    assert b.task_by_id("tp").created == "2026-10-01T09:00:00"
    assert _records(path)["tp"].get("created") == "2026-10-01T09:00:00"


async def test_TC_4308_an_edit_keeps_created_as_it_was(tmp_path, monkeypatch):
    """TC-4308 (LLR-4301.8): `e`, a new title, `alt+s` on a stamped task and on an
    unstamped one → `"2026-10-31T18:20:00"` and None unchanged, the unstamped entry still
    holds no `created` key (NC stamp on edit: arm 2 gets 08:10:00)."""
    path = _single_board(tmp_path)
    monkeypatch.setattr(models, "datetime", fx.FixedNow, raising=False)
    app = _app(path)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        for tid, title in (("ta1", "Sync notes v2"), ("ta2", "Pilot store list v2")):
            app.selected_task_id = tid
            await press(pilot, "e")
            assert type(app.screen).__name__ == "TaskModal"
            app.screen.query_one("#f-title", Input).value = title
            await press(pilot, "alt+s")
            assert app.board.task_by_id(tid).title == title
    recs = _records(path)
    assert created_of(app.board.task_by_id("ta1")) == "2026-10-31T18:20:00"
    assert created_of(app.board.task_by_id("ta2")) is None
    assert recs["ta1"].get("created") == "2026-10-31T18:20:00"
    assert "created" not in recs["ta2"]


def test_TC_4309_a_project_move_keeps_each_moved_tasks_created(tmp_path, monkeypatch):
    """TC-4309 (LLR-4301.9): `move_project` of `pm` → in the target file the stamped
    task keeps `"2026-10-30T09:00:00"` and the unstamped one holds no key; read back, the
    fields are the same (NC re-stamp moved tasks → 08:10:00)."""
    monkeypatch.setattr(models, "datetime", fx.FixedNow, raising=False)
    src_p, dst_p = tmp_path / "src" / "board.json", tmp_path / "dst" / "board.json"
    src = Board([Project("Move me", "sky", id="pm"), Project("Stay", "lime", id="ps")],
                [Task("m1", project_id="pm", id="m1"), Task("s1", project_id="ps", id="s1"),
                 Task("m2", project_id="pm", id="m2")], src_p, dict(fx.SETTINGS))
    fx.write_board(src_p, src, {"m1": "2026-10-30T09:00:00"})
    dst = Board([], [Task("d1", id="d1")], dst_p, dict(fx.SETTINGS))
    fx.write_board(dst_p, dst, {})
    src, dst = Board.load(src_p), peek_board(dst_p)
    plan = move_plan(src, dst, "pm", set(), set())
    assert plan.refusal is None, plan.refusal
    move_project(src, dst, "pm", plan, "2026-11-01", ("Src", "Dst"))
    recs = _file(dst_p)["tasks"]
    assert [r["id"] for r in recs] == ["d1", "m1", "m2"]
    assert recs[1].get("created") == "2026-10-30T09:00:00"
    assert "created" not in recs[2]
    moved = Board.load(dst_p)
    assert created_of(moved.task_by_id("m1")) == "2026-10-30T09:00:00"
    assert created_of(moved.task_by_id("m2")) is None


async def test_TC_4310_undo_restores_a_deleted_task_with_its_created(tmp_path, monkeypatch):
    """TC-4310 (LLR-4301.10): `d`, `y`, `u` on a stamped and on an unstamped task → each
    back with `created` as it was and the file the same (NC re-stamp on restore)."""
    path = _single_board(tmp_path)
    monkeypatch.setattr(models, "datetime", fx.FixedNow, raising=False)
    app = _app(path)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        for tid in ("ta1", "ta2"):
            app.selected_task_id = tid
            await press(pilot, "d", "y")
            assert app.board.task_by_id(tid) is None
            await press(pilot, "u")
            assert app.board.task_by_id(tid) is not None
    assert [t.id for t in app.board.tasks][:3] == ["ta1", "ta2", "ta3"]
    recs = _records(path)
    assert created_of(app.board.task_by_id("ta1")) == "2026-10-31T18:20:00"
    assert created_of(app.board.task_by_id("ta2")) is None
    assert recs["ta1"].get("created") == "2026-10-31T18:20:00"
    assert "created" not in recs["ta2"]


def test_TC_4311_a_rescued_entry_is_not_stamped():
    """TC-4311 (LLR-4301.11): an unreadable entry rescued (`Task.from_dict(["x"])`, or
    `_rescue_task` on a dict that tripped the parser) has `created` None — even when the
    entry held a `created` string (it survives only in the rescued notes)."""
    t = Task.from_dict(["x"])
    assert t.title == "(recovered task)" and t.extra.get("_rescued") is True
    assert created_of(t) is None
    r = _rescue_task({"title": "Bad", "created": "2026-10-01T09:00:00"}, "TypeError")
    assert r.title == "Bad" and "2026-10-01T09:00:00" in r.notes
    assert created_of(r) is None


# --------------------------------------------------------------------------- #
# HLR-4302 — the board file
# --------------------------------------------------------------------------- #
def test_TC_4312_created_is_written_only_when_set(tmp_path):
    """TC-4312 (LLR-4302.1): the saved record of `Task("x")` holds no `created` key (NC
    always write: `"created": null`); with a value the key holds it, just before `id`
    (group D's field position); a project's record is as at base."""
    need_created_field()
    plain = _record(Task("x", id="t1"))
    assert "created" not in plain and list(plain)[-3:] == ["phase_changed", "milestone", "id"]
    assert "created" not in _record(Task("x", id="t1"), with_created=False)
    set_ = _record(Task("x", id="t2", created=ADD_AT))
    assert set_["created"] == ADD_AT and list(set_)[-3:] == ["milestone", "created", "id"]
    b = Board([], [Task("x", id="t1"), Task("y", id="t2", created=ADD_AT)],
              tmp_path / "board.json", {})
    saved = {r["id"]: r for r in json.loads(b._serialized())["tasks"]}
    assert "created" not in saved["t1"] and saved["t2"]["created"] == ADD_AT
    assert list(_record(Project("Alpha", "sky", "on_track"))) == [
        "name", "color", "status", "archived", "pinned", "start_date", "due_date", "id"]


def test_TC_4313_a_string_created_is_read_as_it_is(tmp_path):
    """TC-4313 (LLR-4302.2): a `str` `created` is read verbatim — a valid stamp and
    `"not a date"` alike (validity is the list's concern, LLR-4304.8; NC parse-or-drop on
    read) — and none lands in `extra`; `Board.load` reads it and writes nothing."""
    for value in ("2026-10-30T08:10:00", "not a date"):
        t = Task.from_dict({"title": "a", "created": value})
        assert created_of(t) == value and "created" not in t.extra
    path = tmp_path / "b" / "board.json"
    b = Board([], [Task("a", id="t1")], path, {})
    fx.write_board(path, b, {"t1": "2026-10-30T08:10:00"})
    before = path.read_bytes()
    assert created_of(Board.load(path).task_by_id("t1")) == "2026-10-30T08:10:00"
    assert path.read_bytes() == before


def test_TC_4314_a_non_string_created_is_written_back_unchanged(tmp_path):
    """TC-4314 (LLR-4302.3): entries with `"created": 5`, `null` and `true` round-trip
    load → save with the same VALUES (the key may move to the front, P-D-3), the field
    None and the raw value in `extra`; a second save is a fixed point. An entry with no
    key gains none. NC: drop non-string values."""
    path = tmp_path / "b" / "board.json"
    raw = {"phases": ["Backlog", "Done"], "projects": [], "settings": {},
           "tasks": [{"title": "a", "created": 5, "id": "t5"},
                     {"title": "b", "created": None, "id": "t6"},
                     {"title": "c", "created": True, "id": "t7"},
                     {"title": "d", "id": "t8"}]}
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps(raw, indent=2), encoding="utf-8")
    board = Board.load(path)
    for tid, value in (("t5", 5), ("t6", None), ("t7", True)):
        t = board.task_by_id(tid)
        assert created_of(t) is None and "created" in t.extra and t.extra["created"] == value
        assert _record(t)["created"] == value
    board.save()
    recs = _records(path)
    assert (recs["t5"]["created"], recs["t6"]["created"], recs["t7"]["created"]) == \
        (5, None, True)
    assert "created" in recs["t6"] and "created" not in recs["t8"]
    once = path.read_bytes()
    Board.load(path).save()
    assert path.read_bytes() == once


# --- LLR-4302.4: the three synthetic old boards of graph-proto-D.cw.md --------
_PA = {"name": "Alpha", "color": "sky", "status": "on_track", "archived": False,
       "pinned": False, "start_date": None, "due_date": None, "id": "pa"}


def _R(title, tid, **over):
    rec = {"title": title, "project_id": None, "phase": "Backlog", "priority": "normal",
           "start_date": None, "due_date": None, "notes": "", "urls": [], "images": [],
           "archived": False, "pinned": False, "blocked": False, "depends_on": [],
           "phase_changed": None, "milestone": False, "id": tid}
    rec.update(over)
    return rec


def _old(tasks) -> str:
    return json.dumps({"phases": ["Backlog", "Doing", "Review", "Done"], "projects": [_PA],
                       "tasks": tasks, "settings": {}}, indent=2)


OLD_BOARDS = {
    "plain": _old([_R("Sync notes", "ta", project_id="pa", phase="Doing"),
                   _R("Ship caf\u00e9", "tb")]),
    "legacy": _old([{"title": "Old one", "status": "doing", "url": "https://example.com/a",
                     "id": "tl"}]),
    "unknown": _old([{"zz": 1, **_R("Has extra", "tu")}]),
}

# The bytes eb411e1's `Board.load` + `save()` write for the legacy board (P-D-1 ruling):
# captured by the tester in the base tree (C:/Users/jjgh8/Github/taskboard-wt/incL-base,
# `taskboard.__file__` = …\incL-base\taskboard\__init__.py), LF form, 761 bytes, sha256
# fa38dbd0… — the same digest group D reports for both trees. Frozen here.
LEGACY_ORACLE = (
    '{\n  "phases": [\n    "Backlog",\n    "Doing",\n    "Review",\n    "Done"\n  ],\n'
    '  "projects": [\n    {\n      "name": "Alpha",\n      "color": "sky",\n'
    '      "status": "on_track",\n      "archived": false,\n      "pinned": false,\n'
    '      "start_date": null,\n      "due_date": null,\n      "id": "pa"\n    }\n  ],\n'
    '  "tasks": [\n    {\n      "title": "Old one",\n      "project_id": null,\n'
    '      "phase": "Doing",\n      "priority": "normal",\n      "start_date": null,\n'
    '      "due_date": null,\n      "notes": "",\n      "urls": [\n'
    '        "https://example.com/a"\n      ],\n      "images": [],\n'
    '      "archived": false,\n      "pinned": false,\n      "blocked": false,\n'
    '      "depends_on": [],\n      "phase_changed": null,\n      "milestone": false,\n'
    '      "id": "tl"\n    }\n  ],\n  "settings": {}\n}')
LEGACY_SHA = "fa38dbd0e977ae0b23c3ecabbd79b3ea68558fc83efb4b93fe8761139c102e54"


def _native(text: str) -> bytes:
    """What `Path.write_text` puts on disk on this platform (Board.save's own write)."""
    return text.replace("\n", os.linesep).encode("utf-8")


@pytest.mark.parametrize("name", ["plain", "legacy", "unknown"])
def test_TC_4315_an_old_board_keeps_the_bytes_eb411e1_writes(tmp_path, monkeypatch, name):
    """TC-4315 (LLR-4302.4, HLR-4302): an old board (no `created` key anywhere) after
    `Board.load` + `save()` is byte-equal to the base oracle — the input itself for the
    plain and unknown-key boards (1126 and 741 bytes in LF form), the frozen 761-byte
    literal for the legacy one (base migrates status/url too, P-D-1). GUARD: passes on the
    base revision by design; NC `_to_dict` writing `"created": null` → RED."""
    monkeypatch.setattr(models, "datetime", fx.FixedNow, raising=False)
    assert hashlib.sha256(LEGACY_ORACLE.encode()).hexdigest() == LEGACY_SHA
    path = tmp_path / name / "board.json"
    path.parent.mkdir(parents=True)
    path.write_text(OLD_BOARDS[name], encoding="utf-8")
    Board.load(path).save()
    after = path.read_bytes()
    oracle = LEGACY_ORACLE if name == "legacy" else OLD_BOARDS[name]
    assert after == _native(oracle)
    assert len(oracle.encode()) == {"plain": 1126, "legacy": 761, "unknown": 741}[name]
    assert b'"created"' not in after
    if name == "unknown":
        assert list(_file(path)["tasks"][0])[0] == "zz"


def test_TC_4316_an_add_leaves_every_old_entry_as_it_was(tmp_path, monkeypatch):
    """TC-4316 (LLR-4302.5, HLR-4302's NC): on the plain old board, whose history.jsonl
    holds a birth record for `ta` (ARCH-2: something a back-fill could copy), an add
    leaves each old entry's slice of the file byte-identical and `ta` with no `created`
    key. GUARD: passes on base by design; NC a save-time back-fill of an inferred
    `created` → `ta` gains `"created": "2026-10-20T09:00:00"`: RED."""
    monkeypatch.setattr(models, "datetime", fx.FixedNow, raising=False)
    path = tmp_path / "plain" / "board.json"
    path.parent.mkdir(parents=True)
    path.write_text(OLD_BOARDS["plain"], encoding="utf-8")
    fx.write_history(path.parent, [fx.birth("ta", "2026-10-20T09:00:00", "Doing")])
    before = _file(path)["tasks"]
    board = Board.load(path)
    board.add_task(Task("New one", id="tn"))
    after = _text(path)
    for rec in before:
        assert _slice(rec) in after, f"entry {rec['id']} rewritten"
    recs = _records(path)
    assert "created" not in recs["ta"] and "created" not in recs["tb"]
    assert list(recs) == ["ta", "tb", "tn"]


def _team(shared: Path) -> None:
    shared.mkdir(parents=True, exist_ok=True)
    (shared / TEAM_FILENAME).write_text(json.dumps({
        "version": 3, "phases": ["Backlog", "Doing", "Review", "Done"],
        "template": {"fields": ["title", "assignee", "due", "priority"]},
        "projects": [{"id": "plat", "name": "Platform", "color": "sky", "status": "on_track"}],
        "roster": [{"id": "subject", "name": "username_subject", "hue": "sky"}]}),
        encoding="utf-8")


def test_TC_4318_the_team_push_carries_no_created(tmp_path, monkeypatch):
    """TC-4318 (LLR-4302.7, SEC-1): `Board._to_dict(task)` — the push's own call — holds
    no `created` for a stamped task nor for one whose raw `created` sits in `extra` (and
    leaves that `extra` as it was); `Board._serialized()` holds both; the pushed
    `board.<user>.json` records hold no `created` key. NC: the push record keeps it."""
    need_created_field()
    monkeypatch.setattr(models, "datetime", fx.FixedNow, raising=False)
    t1 = Task("x", project_id="plat", id="t1", created=ADD_AT)
    t5 = Task.from_dict({"title": "a", "project_id": "plat", "created": 5, "id": "t5"})
    assert "created" not in Board._to_dict(t1)
    assert "created" not in Board._to_dict(t5)
    assert t5.extra.get("created") == 5
    path = tmp_path / "me" / "board.json"
    b = Board([Project("Platform", "sky", id="plat")], [t5], path, {})
    b.add_task(t1)
    saved = {r["id"]: r for r in json.loads(b._serialized())["tasks"]}
    assert saved["t1"]["created"] == ADD_AT and saved["t5"]["created"] == 5
    shared = tmp_path / "shared"
    _team(shared)
    state = TeamState(shared, user_id="subject")
    assert state.load_config() is True
    assert state.push(b) is True
    pushed = json.loads((shared / "board.subject.json").read_text(encoding="utf-8"))
    assert {r["id"] for r in pushed["tasks"]} == {"t1", "t5"}
    assert [r for r in pushed["tasks"] if "created" in r] == []


# --------------------------------------------------------------------------- #
# AT-4302, AT-4303 — through the shipped surface
# --------------------------------------------------------------------------- #
async def test_AT_4302_a_task_added_on_an_old_board_is_first_in_the_list(home):
    """AT-4302 (HLR-4301, HLR-4302, HLR-4304): on the registry's boards, `a`, `Call the
    bank`, `alt+s` → Alpha's file holds its `created` 2026-11-01T08:10:00 and every old
    entry's slice is byte-identical; `N` → `Call the bank` is row 0 with `08:10` under
    TODAY, the cursor on it, the pane's source line `the created field`; row 1 `Pay the
    rent`."""
    fx.build(home)
    alpha = fx.board_path(home, "alpha")
    app = open_s_app()
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        await press(pilot, "escape")
        old = _file(alpha)["tasks"]
        await press(pilot, "a")
        await pilot.press(*"Call the bank")
        await press(pilot, "alt+s")
        new = next(t for t in app.board.tasks if t.title == "Call the bank")
        assert _records(alpha)[new.id].get("created") == ADD_AT
        after = _text(alpha)
        for rec in old:
            assert _slice(rec) in after, f"entry {rec['id']} rewritten by the add"
        await open_list(pilot, app)
        rows, headers, pane, _head = seen(app, 118)
        assert rows[0]["title"] == "Call the bank" and rows[0]["label"] == "08:10"
        assert headers[0] == "TODAY" and rows[0]["cursor"]
        assert pane[3] == "added Sun Nov 01 · 08:10 · the created field"
        assert rows[1]["title"] == "Pay the rent"


async def test_AT_4303_a_template_insert_lists_its_tasks_with_one_time(home):
    """AT-4303 (HLR-4301, HLR-4304): `I`, `Simple chain` → Alpha gains Plan, Build, Ship,
    each created 2026-11-01T08:10:00, history still 1 line; `N` → rows 0–2 Ship, Build,
    Plan (one moment: ties by file position, newest first the exact reverse) with one
    label `08:10` under TODAY; row 3 `Pay the rent`."""
    fx.build(home)
    alpha = fx.board_path(home, "alpha")
    app = open_s_app()
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        await press(pilot, "escape")
        app.selected_task_id = "ta1"
        await press(pilot, "I")
        await press(pilot, "down", "enter")
        recs = _file(alpha)["tasks"]
        assert [r["title"] for r in recs[3:]] == ["Plan", "Build", "Ship"]
        assert [r.get("created") for r in recs[3:]] == [ADD_AT] * 3
        assert len(fx.history_file(home, "alpha").read_text(encoding="utf-8").splitlines()) == 1
        await open_list(pilot, app)
        rows, headers, _pane, _head = seen(app, 118)
        assert [r["title"] for r in rows[:4]] == ["Ship", "Build", "Plan", "Pay the rent"]
        assert [r["label"] for r in rows[:3]] == ["08:10"] * 3
        assert headers[0] == "TODAY"
