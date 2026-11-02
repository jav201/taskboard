"""`N` — every task of every board in the order it was added (Inc L, dev-flow-v3-beta;
HLR-4303..HLR-4306 · LLR-4303.1..4303.24, LLR-4304.1..4304.15 + .17 (.16 withdrawn),
LLR-4305.1..4305.4, LLR-4306.1..4306.7, LLR-4302.6 · AT-4301, AT-4304, AT-4305).

WHY. The field report behind US-4301: the owner (`username_subject`) captures tasks in a
hurry and must find them again BY WHEN THEY WERE ADDED, not by their planned dates — one list
of every board, newest first, with where each task stands (a box per phase) and everything
about the one under the cursor. Old tasks carry no stamp: their moment is inferred honestly
(history `≈`, else unknown `?`, placed before every dated row) and NOTHING is rewritten — the
list view reads every board once and writes no board file and no history (LLR-4302.6). The
archived toggle is the list's own, independent of the main screen's `v`.

Layer 0 runs the pure functions of graph-interfaces.cw.md / graph-proto-V.cw.md on the F-V
fixture (`added_list_fixture.fv_lanes`) at the render sizes 116x29 and 78x23 (the bodies of
118x30 and 80x24), with exact strings, cell positions and styles. The pilots drive the
shipped app on the S fixture (two registry boards, `Path.home` redirected) at 118x30 and
80x24 through its keys.

RED on the base revision (eb411e1): `views.added_rows`, `added_moment`, `added_order`,
`first_created`, `state_boxes`, `render_added_list` and `AddedRow` do not exist, `N` is
unbound (no list view opens) and the README has no `N` row. New names are reached only
through `added_list_fixture.need`, and every pilot asserts the list view opened right after
`N` (`open_list`), so each test fails on an assertion, never a collection error. No test of
this module is a guard: every one is RED on base.

Synthetic data only; clock today 2026-11-01 (a Sunday), now 08:10:00.
"""
from __future__ import annotations

import hashlib
import json
import time
from datetime import date, datetime
from pathlib import Path

import pytest

import added_list_fixture as fx
from added_list_fixture import (cursor, home, key_row, lists_on_stack, names, need,  # noqa: F401
                                notices, on_list, open_list, open_s_app, parse_list, press,
                                seen, titles)
from taskboard import history, keymap, views
from taskboard.app import TaskboardApp
from taskboard.models import Board, Project, Task

W118, W80 = (118, 30), (80, 24)
HEAD_116 = ("ADDED  6 tasks · every board · newest first  ·  time = created  ≈ = history  "
            "? = unknown · 1 archived hidden")
HEAD_78 = "ADDED  6 tasks · newest first  ·  time = created  ≈ = his… · 1 archived hidden"
KEYS_5 = "↑↓ move   ↵ open on board   o newest/oldest   v archived   esc / N back"
READ_ONLY = "   · read-only: nothing here edits a task"


# --------------------------------------------------------------------------- #
# layer-0 helpers
# --------------------------------------------------------------------------- #
def _v(name):
    return need(views, name)


def _rows(lanes):
    return _v("added_rows")(lanes)


def _order(rows, newest=True, show=False):
    return _v("added_order")(rows, newest, show)


def _render(rows, sel=0, newest=True, show=False, hidden=0, unread=0, first=None,
            today=fx.TODAY, people=None, width=116, height=29):
    return _v("render_added_list")(rows, sel, newest, show, hidden, unread, first, today,
                                   people or {}, width, height)


def _ids(rows) -> list:
    return [r.task.id for r in rows]


def _by_id(rows) -> dict:
    return {r.task.id: r for r in rows}


def _row(task, lane, pos, source, at, board=None, bname="B", bcolour="sky"):
    """An AddedRow built by hand (graph-interfaces `[Data: AddedRow]`), for the shuffled
    inputs of ARCH-1."""
    AddedRow = _v("AddedRow")
    board = board or Board([], [task], Path("unused/board.json"), {})
    return AddedRow(task=task, lane=lane, bname=bname, bcolour=bcolour, board=board,
                    source=source, at=at, pos=pos)


def _listed_body(lanes, sel=0, newest=True, show=False, people=None, width=116, height=29,
                 unread=0):
    """What the screen paints for `lanes`: rows read once, `first` over all of them
    (archived included), ordered and filtered, `hidden` = archived left out."""
    rows = _rows(lanes)
    first = _v("first_created")(rows)
    listed = _order(rows, newest, show)
    hidden = 0 if show else sum(1 for r in rows if r.task.archived)
    body = _render(listed, sel, newest, show, hidden, unread, first, fx.TODAY, people,
                   width, height)
    return body, listed


def _fv_body(tmp_path, sel=2, width=116, height=29, show=False, newest=True):
    return _listed_body(fx.fv_lanes(tmp_path), sel, newest, show, fx.fv_people(), width,
                        height)


def _plain_lines(body) -> list[str]:
    return body.plain.split("\n")


def _lw(width):
    return 46 if width >= 100 else 34


def _pane(body, width) -> list[str]:
    return fx.pane(_plain_lines(body), _lw(width))


def _list(body, width):
    return parse_list(_plain_lines(body), _lw(width))


def _line(left: str, right: str, lw: int, width: int) -> str:
    return (left.ljust(lw) + " │ " + right).ljust(width)


FV_116 = [HEAD_116.ljust(116), " " * 116] + [_line(a, b, 46, 116) for a, b in [
    ("TODAY", "Sync notes"),
    (" 08:10  ■□□□ ▍Pay the rent", "Eval harness · Work"),
    ("YESTERDAY", "Doing  ▲ high  Oct 30→Nov 3  ◆ milestone  @Ana Ruiz  ↗ 1  ▤ 1"),
    (" 21:47  ■■■  ▍Compose file anatomy", "added Sat Oct 31 · 18:20 · the created field"),
    ("▶18:20  ■■□□ ▍Sync notes", "─" * 67),
    ("WED OCT 28 ≈", "ask the vendor"),
    (" ≈10:30 ■■■□ ▍Pilot store list", "ping @Ana Ruiz before Friday"),
    ("BEFORE OCT 31 · ?", "↗ https://example.com/spec"),
    (" ?      ■□□  ▍Hybrid search index", "▤ board.png"),
    (" ?      ■□□□ ▍Volume oracle script", "after: Pilot store list"),
]] + [_line("", "", 46, 116)] * 17

FV_78 = [HEAD_78.ljust(78), " " * 78] + [_line(a, b, 34, 78) for a, b in [
    ("TODAY", "Sync notes"),
    (" 08:10  ■□□□ ▍Pay the rent", "Eval harness · Work"),
    ("YESTERDAY", "Doing  ▲ high  Oct 30→Nov 3  ◆ milestone"),
    (" 21:47  ■■■  ▍Compose file anatomy", "@Ana Ruiz  ↗ 1  ▤ 1"),
    ("▶18:20  ■■□□ ▍Sync notes", "added Sat Oct 31 · 18:20 · the created"),
    ("WED OCT 28 ≈", "field"),
    (" ≈10:30 ■■■□ ▍Pilot store list", "─" * 41),
    ("BEFORE OCT 31 · ?", "ask the vendor"),
    (" ?      ■□□  ▍Hybrid search index", "ping @Ana Ruiz before Friday"),
    (" ?      ■□□□ ▍Volume oracle script", "↗ https://example.com/spec"),
    ("", "▤ board.png"),
    ("", "after: Pilot store list"),
]] + [_line("", "", 34, 78)] * 9


# --------------------------------------------------------------------------- #
# HLR-4304 — the added moment (layer 0)
# --------------------------------------------------------------------------- #
def test_TC_4361_a_valid_created_is_the_moment_even_with_a_birth_record(tmp_path):
    """TC-4361 (LLR-4304.1): F-V's stamped tasks are source `c` at their created; a task
    with a created AND a birth record of another time takes the created (NC prefer
    history → 2026-10-20 10:00)."""
    rows = _by_id(_rows(fx.fv_lanes(tmp_path)))
    assert (rows["w2"].source, rows["w2"].at) == ("c", datetime(2026, 10, 31, 18, 20))
    assert (rows["h2"].source, rows["h2"].at) == ("c", datetime(2026, 10, 31, 21, 47))
    assert (rows["w4"].source, rows["w4"].at) == ("c", datetime(2026, 11, 1, 8, 10))
    lanes = fx.solo_lanes(tmp_path, [fx.make_task("Both", created="2026-10-31T18:20:00",
                                                  id="x1")],
                          history=[fx.birth("x1", "2026-10-20T10:00:00", "Todo")])
    (only,) = _rows(lanes)
    assert (only.source, only.at) == ("c", datetime(2026, 10, 31, 18, 20))


def test_TC_4362_no_created_takes_the_first_birth_record(tmp_path):
    """TC-4362 (LLR-4304.2): w3 has births at 10-28 10:30 then 10-29 11:00 → source `h`
    at the FIRST (NC last record → 10-29)."""
    w3 = _by_id(_rows(fx.fv_lanes(tmp_path)))["w3"]
    assert (w3.source, w3.at) == ("h", datetime(2026, 10, 28, 10, 30))


def test_TC_4362b_an_invalid_first_birth_record_does_not_hide_a_later_valid_one(tmp_path):
    """TC-4362b (LLR-4304.2 as amended at E5, CR-1; LLR-4304.13): the moment of an
    unstamped task is its FIRST VALID birth record. A hand-edited history whose first birth
    `at` is offset-aware ("…+00:00", not a valid moment, ARCH-3) or garbage ("yesterday")
    must not turn a task with a later valid birth into `?`: the owner would lose a moment
    the file does hold. Arms: aware-then-valid and garbage-then-valid → source `h` at
    2026-10-28 10:30; a later valid birth (10-29) never wins over the first valid one.
    NC `first record, then validate` (the E4 code): `('?', None)`; NC `last valid`: 10-29."""
    lanes = fx.solo_lanes(tmp_path, [fx.make_task("Aware first", id="ba"),
                                     fx.make_task("Garbage first", id="bg")],
                          history=[fx.birth("ba", "2026-10-27T09:00:00+00:00", "Todo"),
                                   fx.birth("bg", "yesterday", "Todo"),
                                   fx.birth("ba", "2026-10-28T10:30:00", "Todo"),
                                   fx.birth("bg", "2026-10-28T10:30:00", "Todo"),
                                   fx.birth("ba", "2026-10-29T11:00:00", "Todo"),
                                   fx.birth("bg", "2026-10-29T11:00:00", "Todo")])
    by = _by_id(_rows(lanes))
    first_valid = ("h", datetime(2026, 10, 28, 10, 30))
    # both arms in one compare, so a failure shows each of them
    assert {tid: (by[tid].source, by[tid].at) for tid in ("ba", "bg")} == {
        "ba": first_valid,                          # offset-aware first
        "bg": first_valid}                          # garbage first


def test_TC_4363_neither_created_nor_birth_is_unknown(tmp_path):
    """TC-4363 (LLR-4304.3): w1, w5 (archived) and h1 → source `?`, moment None (NC a
    file-time guess); every task of every lane is a row, archived included, lane then file
    position, each with its lane and position."""
    rows = _rows(fx.fv_lanes(tmp_path))
    assert _ids(rows) == ["w1", "w2", "w3", "w4", "w5", "h1", "h2"]
    assert [(r.lane, r.pos) for r in rows] == [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
                                               (1, 0), (1, 1)]
    by = _by_id(rows)
    for tid in ("w1", "w5", "h1"):
        assert (by[tid].source, by[tid].at) == ("?", None)


def test_TC_4368_a_created_that_is_not_a_date_is_no_created(tmp_path):
    """TC-4368 (LLR-4304.8): `added_moment` gives None for "not a date" and for 5, a
    naive datetime for "2026-10-31"; a task whose created is "not a date" is `h` with a
    birth, `?` without; 0 exceptions (NC crash on parse)."""
    added_moment = _v("added_moment")
    assert added_moment("not a date") is None
    assert added_moment(5) is None
    assert added_moment(None) is None
    assert added_moment("2026-10-31") == datetime(2026, 10, 31, 0, 0)
    lanes = fx.solo_lanes(tmp_path, [fx.make_task("With birth", created="not a date", id="y1"),
                                     fx.make_task("Without", created="not a date", id="y2")],
                          history=[fx.birth("y1", "2026-10-28T10:30:00", "Todo")])
    by = _by_id(_rows(lanes))
    assert (by["y1"].source, by["y1"].at) == ("h", datetime(2026, 10, 28, 10, 30))
    assert (by["y2"].source, by["y2"].at) == ("?", None)


def test_TC_4373_an_offset_aware_moment_is_not_valid(tmp_path):
    """TC-4373 (LLR-4304.13, ARCH-3): `added_moment` of "…+00:00" is None (no conversion,
    the same on every machine); such a created with no birth → `?`, with a birth → `h`;
    a birth `at` with an offset is no birth; 0 exceptions (NC convert/strip the offset →
    source `c`)."""
    assert _v("added_moment")("2026-10-31T18:20:00+00:00") is None
    aware = "2026-10-31T18:20:00+00:00"
    lanes = fx.solo_lanes(tmp_path, [fx.make_task("No birth", created=aware, id="z1"),
                                     fx.make_task("Birth", created=aware, id="z2"),
                                     fx.make_task("Aware birth", id="z3")],
                          history=[fx.birth("z2", "2026-10-28T10:30:00", "Todo"),
                                   fx.birth("z3", "2026-10-28T10:30:00+00:00", "Todo")])
    by = _by_id(_rows(lanes))
    assert by["z1"].source == "?" and by["z1"].at is None
    assert (by["z2"].source, by["z2"].at) == ("h", datetime(2026, 10, 28, 10, 30))
    assert by["z3"].source == "?" and by["z3"].at is None


def test_TC_4373b_a_zulu_or_pre_1970_offset_moment_is_none_without_raising():
    """TC-4373b (LLR-4304.13): "…Z" and "1960-01-01T00:00:00+00:00" → None, no exception
    (the conversion P-V-2 guarded is gone, ARCH-3)."""
    added_moment = _v("added_moment")
    assert added_moment("2026-10-31T18:20:00Z") is None
    assert added_moment("1960-01-01T00:00:00+00:00") is None


def _unreadable_history_lanes(tmp_path, content: bytes | None = None, directory=False):
    """One board: a stamped task and an unstamped one with a birth record its history
    file cannot give."""
    lanes = fx.solo_lanes(tmp_path, [fx.make_task("Stamped", created="2026-10-31T18:20:00",
                                                  id="s1"),
                                     fx.make_task("Unstamped", id="s2")],
                          history=[fx.birth("s2", "2026-10-28T10:30:00", "Todo")])
    hist = tmp_path / "solo" / "history.jsonl"
    if directory:
        hist.unlink()
        hist.mkdir()
    elif content is not None:
        hist.write_bytes(content)
    return lanes


def _assert_unread_history(rows):
    by = _by_id(rows)
    assert (by["s1"].source, by["s2"].source) == ("c", "?")
    assert by["s2"].at is None


def test_TC_4372_a_history_read_that_raises_oserror_gives_no_births(tmp_path, monkeypatch):
    """TC-4372 (LLR-4304.12): `history.read` raising PermissionError → rows built, the
    unstamped task `?`, the stamped one `c`, no exception; the same when history.jsonl is
    a folder (a real OSError through the real read). NC an unguarded read."""
    real = history.read

    def refuse(_path):
        raise PermissionError(13, "Permission denied")

    lanes = _unreadable_history_lanes(tmp_path)
    assert _by_id(_rows(lanes))["s2"].source == "h"            # readable: the birth counts
    with monkeypatch.context() as m:
        m.setattr(history, "read", refuse)
        for name, value in list(vars(views).items()):         # a `from history import read`
            if value is real:
                m.setattr(views, name, refuse)
        _assert_unread_history(_rows(lanes))
    _assert_unread_history(_rows(_unreadable_history_lanes(tmp_path / "d", directory=True)))


def test_TC_4372b_a_history_file_that_is_not_utf8_gives_no_births(tmp_path):
    """TC-4372b (LLR-4304.12, P-V-1): a history.jsonl holding the bytes 0xff 0xfe
    (UnicodeDecodeError, a ValueError) → rows built, no exception."""
    _assert_unread_history(_rows(_unreadable_history_lanes(tmp_path, b"\xff\xfe\n")))


def test_TC_4372c_a_deeply_nested_history_line_gives_no_births(tmp_path):
    """TC-4372c (LLR-4304.12, SEC-2): one line of 10 000 nested `[` (RecursionError from
    the base `history.read`) → rows built, no exception."""
    line = ("[" * 10000 + "]" * 10000 + "\n").encode()
    _assert_unread_history(_rows(_unreadable_history_lanes(tmp_path, line)))


def test_TC_4377_a_task_id_that_is_not_a_string_is_listed_unknown(tmp_path):
    """TC-4377 (LLR-4304.17, SEC-3): a peeked board holding tasks of id ["x"] and
    {"a": 1}, and a birth record for "x" → both listed `?`; the cursor on each paints the
    pane; a task waiting on "x" shows `after: x` (the list id resolves no title); 0
    exceptions (NC `births.get(task.id)` → TypeError)."""
    folder = tmp_path / "odd"
    folder.mkdir()
    (folder / "board.json").write_text(json.dumps({
        "phases": ["Todo", "Doing", "Done"], "projects": [], "settings": {},
        "tasks": [{"title": "Odd", "id": ["x"]}, {"title": "Odder", "id": {"a": 1}},
                  {"title": "Waits", "id": "w", "depends_on": ["x"],
                   "created": "2026-10-31T18:20:00"}]}), encoding="utf-8")
    fx.write_history(folder, [fx.birth("x", "2026-10-28T10:30:00", "Todo")])
    board = Board.load(folder / "board.json")
    assert [t.id for t in board.tasks][:2] == [["x"], {"a": 1}]
    lanes = [("Odd", "pink", board, "")]
    rows = _rows(lanes)
    assert [r.source for r in rows] == ["?", "?", "c"] and rows[0].at is None
    for sel in range(3):
        body, listed = _listed_body(lanes, sel=sel)
        assert _pane(body, 116)[0] == listed[sel].task.title
    body, listed = _listed_body(lanes, sel=0)                 # newest first: "Waits"
    assert listed[0].task.id == "w"
    assert [ln for ln in _pane(body, 116) if ln.startswith("after:")] == ["after: x"]


# --------------------------------------------------------------------------- #
# HLR-4304 — the order (layer 0, ARCH-1: hand-shuffled inputs)
# --------------------------------------------------------------------------- #
def _five():
    t = {k: Task(k, id=k) for k in "ABCDE"}
    ten, nine = datetime(2026, 10, 31, 10, 0), datetime(2026, 10, 31, 9, 0)
    return [_row(t["D"], 1, 1, "c", ten), _row(t["E"], 0, 2, "c", nine),
            _row(t["B"], 1, 0, "?", None), _row(t["C"], 0, 1, "c", ten),
            _row(t["A"], 0, 0, "?", None)]


def test_TC_4364_ties_break_by_board_order_then_file_position():
    """TC-4364 (LLR-4304.4): the shuffled input D(1,1,10:00) E(0,2,09:00) B(1,0,?)
    C(0,1,10:00) A(0,0,?), oldest first → A, B, E, C, D; two rows of one moment on two
    boards follow the registry order whichever comes first in the input (NC sort by
    moment alone: input order kept)."""
    assert _ids(_order(_five(), newest=False)) == ["A", "B", "E", "C", "D"]
    at = datetime(2026, 10, 31, 10, 0)
    work, home_ = Task("Work row", id="wk"), Task("Home row", id="hm")
    assert _ids(_order([_row(home_, 1, 0, "c", at), _row(work, 0, 3, "c", at)],
                       newest=False)) == ["wk", "hm"]
    assert _ids(_order([_row(work, 1, 3, "c", at), _row(home_, 0, 0, "c", at)],
                       newest=False)) == ["hm", "wk"]


def test_TC_4366b_newest_first_is_the_exact_reverse(tmp_path):
    """TC-4366b (LLR-4304.6): the same shuffled input, newest first → D, C, E, B, A —
    the exact reverse of oldest first; F-V likewise."""
    assert _ids(_order(_five(), newest=True)) == ["D", "C", "E", "B", "A"]
    rows = _rows(fx.fv_lanes(tmp_path))
    assert _order(rows, True, True) == list(reversed(_order(rows, False, True)))


def test_TC_4365_unknown_rows_come_first_in_board_then_file_order(tmp_path):
    """TC-4365 (LLR-4304.5): F-V rows given in REVERSE (lane, pos) order, oldest first →
    w1, h1, w3, w2, h2, w4: the 2 unknown rows are rows 0–1 in file order (NC unknowns in
    input order: h1, w1 …; NC unknowns last)."""
    rows = list(reversed(_rows(fx.fv_lanes(tmp_path))))
    assert _ids(rows) == ["h2", "h1", "w5", "w4", "w3", "w2", "w1"]
    assert _ids(_order(rows, False, False)) == ["w1", "h1", "w3", "w2", "h2", "w4"]


def test_TC_4365b_with_archived_shown_unknowns_stay_in_board_then_file_order(tmp_path):
    """TC-4365b (LLR-4304.5): the reversed input, archived shown → w1, w5, h1, w3, w2,
    h2, w4 (w5 at Work's position 4 before Home's lane)."""
    rows = list(reversed(_rows(fx.fv_lanes(tmp_path))))
    assert _ids(_order(rows, False, True)) == ["w1", "w5", "h1", "w3", "w2", "h2", "w4"]


def test_TC_4391_archived_tasks_are_left_out_while_hidden(tmp_path):
    """TC-4391 (LLR-4306.1): newest first, archived hidden → w4, h2, w2, w3, h1, w1 (6,
    w5 absent; NC no filter → 7); shown → w5 between h1 and w1 (7)."""
    rows = _rows(fx.fv_lanes(tmp_path))
    assert _ids(_order(rows, True, False)) == ["w4", "h2", "w2", "w3", "h1", "w1"]
    assert _ids(_order(rows, True, True)) == ["w4", "h2", "w2", "w3", "h1", "w5", "w1"]


def test_TC_4370_first_created_is_the_earliest_valid_created(tmp_path):
    """TC-4370 (LLR-4304.10's first created date): over every F-V row (archived
    included) the earliest valid created is 2026-10-31 18:20."""
    rows = _rows(fx.fv_lanes(tmp_path))
    assert _v("first_created")(rows) == datetime(2026, 10, 31, 18, 20)


def test_TC_4370_the_source_line_names_how_the_moment_is_known(tmp_path):
    """TC-4370 (LLR-4304.10): the pane's source line for w2 (`c`), w3 (`h`) and h1 (`?`)
    at 118x30; at 80x24 it wraps inside the pane, never clipped (P-V-3). NC omit `#n`."""
    want = {2: "added Sat Oct 31 · 18:20 · the created field",
            3: "added ≈ Wed Oct 28 · 10:30 · from history.jsonl",
            4: "added: unknown, before Oct 31 · #1 in Home's board file"}
    for sel, line in want.items():
        body, listed = _fv_body(tmp_path / str(sel), sel=sel)
        assert _pane(body, 116)[3] == line, (listed[sel].task.id, _pane(body, 116)[:5])
    body, _ = _fv_body(tmp_path / "n", sel=2, width=78, height=23)
    assert _pane(body, 78)[4:6] == ["added Sat Oct 31 · 18:20 · the created", "field"]


def test_TC_4371_with_no_valid_created_anywhere_unknowns_sit_before_any_record(tmp_path):
    """TC-4371 (LLR-4304.11): a board of 2 unknown tasks → first None and the header
    `BEFORE ANY RECORD · ?` (NC `BEFORE NONE · ?`); a board whose only stamped task is
    archived and hidden still dates the header `BEFORE OCT 30 · ?` (ARCH-8: archived
    included)."""
    lanes = fx.solo_lanes(tmp_path / "a", [Task("One", id="s1"), Task("Two", id="s2")])
    rows = _rows(lanes)
    assert _v("first_created")(rows) is None
    body, _ = _listed_body(lanes)
    assert _list(body, 116)[1] == ["BEFORE ANY RECORD · ?"]
    lanes = fx.solo_lanes(tmp_path / "b", [
        fx.make_task("Gone", created="2026-10-30T09:00:00", archived=True, id="g"),
        Task("One", id="s1"), Task("Two", id="s2")])
    assert _v("first_created")(_rows(lanes)) == datetime(2026, 10, 30, 9, 0)
    body, listed = _listed_body(lanes)
    assert _ids(listed) == ["s2", "s1"]
    assert _list(body, 116)[1] == ["BEFORE OCT 30 · ?"]


def test_TC_4375_with_no_valid_created_the_unknown_source_line_names_no_date(tmp_path):
    """TC-4375 (LLR-4304.15): no valid created anywhere → `added: unknown · #2 in Solo's
    board file` for the board's second task (NC `before None`); F-V's h1 rendered with
    `first` None → `added: unknown · #1 in Home's board file`."""
    lanes = fx.solo_lanes(tmp_path, [Task("One", id="s1"), Task("Two", id="s2")])
    body, listed = _listed_body(lanes, sel=1, newest=False)
    assert listed[1].task.id == "s2"
    assert _pane(body, 116)[3] == "added: unknown · #2 in Solo's board file"
    rows = _rows(fx.fv_lanes(tmp_path / "fv"))
    listed = _order(rows, True, False)
    body = _render(listed, 4, True, False, 1, 0, None, fx.TODAY, fx.fv_people())
    assert listed[4].task.id == "h1"
    assert _pane(body, 116)[3] == "added: unknown · #1 in Home's board file"


# --------------------------------------------------------------------------- #
# HLR-4303 / HLR-4304 / HLR-4305 — the body (layer 0)
# --------------------------------------------------------------------------- #
def test_TC_4327_the_body_at_118x30_is_the_designed_capture(tmp_path):
    """TC-4327 / TC-4328 / TC-4329 / TC-4330 (LLR-4303.7..4303.10): F-V, newest first,
    the cursor on w2, render 116x29 → the 29 lines of graph-proto-V's capture exactly:
    every line 116 cells, `│` at cell 47 (lw 46 + 1) on lines 2–28 and nowhere else."""
    body, _ = _fv_body(tmp_path)
    lines = _plain_lines(body)
    assert len(lines) == 29 and all(len(ln) == 116 for ln in lines)
    for i, (got, want) in enumerate(zip(lines, FV_116)):
        assert got == want, f"line {i}:\n got {got.rstrip()!r}\nwant {want.rstrip()!r}"
    for ln in lines[2:]:
        assert ln.index("│") == 47 and ln.count("│") == 1


def test_TC_4327_the_body_at_80x24_is_the_designed_capture(tmp_path):
    """TC-4327 (LLR-4303.7, LLR-4303.11 P-V-3, LLR-4304.14 P-V-6): the same state at
    78x23 → 23 lines of 78 cells, `│` at cell 35 (lw 34 + 1), the meta and source lines
    wrapped inside the pane, the head's legend clipped before the archived count."""
    body, _ = _fv_body(tmp_path, width=78, height=23)
    lines = _plain_lines(body)
    assert len(lines) == 23 and all(len(ln) == 78 for ln in lines)
    for i, (got, want) in enumerate(zip(lines, FV_78)):
        assert got == want, f"line {i}:\n got {got.rstrip()!r}\nwant {want.rstrip()!r}"
    for ln in lines[2:]:
        assert ln.index("│") == 35 and ln.count("│") == 1


def test_TC_4328_a_row_reads_cursor_time_boxes_hue_title(tmp_path):
    """TC-4328 (LLR-4303.8): the cursor's row `▶18:20  ■■□□ ▍Sync notes` — `▶` accent,
    the label ink, `■■` ink, `□□` dim, `▍` the project's hue (blue), the title bold ink
    (NC boxes after the title); no row exceeds lw; a tab or newline in a title is drawn
    as one space (P-V-9)."""
    body, _ = _fv_body(tmp_path)
    line = fx.text_lines(body)[6]
    assert line.plain.startswith("▶18:20  ■■□□ ▍Sync notes")
    assert fx.colour_at(line, 0) == fx.ACCENT
    assert all(fx.colour_at(line, i) == fx.INK for i in range(1, 6))
    assert [fx.colour_at(line, i) for i in range(8, 12)] == [fx.INK, fx.INK, fx.DIM, fx.DIM]
    assert fx.colour_at(line, 13) == fx.BLUE
    assert all(fx.colour_at(line, i) == fx.INK and fx.bold_at(line, i) for i in range(14, 24))
    for ln in _plain_lines(body)[2:]:
        assert len(ln[:46].rstrip()) <= 46 and ln[46:49] == " │ "
    lanes = fx.solo_lanes(tmp_path / "t", [fx.make_task("a\nb\tc", created="2026-11-01T08:00:00",
                                                        id="q")])
    body, _ = _listed_body(lanes)
    rows, _ = _list(body, 116)
    assert rows[0]["title"] == "a b c" and len(_plain_lines(body)) == 29


def test_TC_4329_day_headers_newest_first(tmp_path):
    """TC-4329 (LLR-4303.9): F-V's headers TODAY, YESTERDAY, WED OCT 28 ≈, BEFORE OCT 31 ·
    ? on lines 2, 4, 7, 9 (NC no ≈); one header per day, ` ≈` only when every row of the
    day is from history (P-V-5); other days `%a %b %d` upper case, zero-padded."""
    body, _ = _fv_body(tmp_path)
    lines = _plain_lines(body)
    assert [lines[i][:46].rstrip() for i in (2, 4, 7, 9)] == [
        "TODAY", "YESTERDAY", "WED OCT 28 ≈", "BEFORE OCT 31 · ?"]
    assert _list(body, 116)[1] == ["TODAY", "YESTERDAY", "WED OCT 28 ≈", "BEFORE OCT 31 · ?"]

    def headers(name, tasks, hist):
        lanes = fx.solo_lanes(tmp_path / name, tasks, history=hist)
        return _list(_listed_body(lanes)[0], 116)[1]

    mixed = [fx.make_task("C row", created="2026-10-31T18:20:00", id="c1"), Task("H row", id="h1")]
    assert headers("mixed", mixed, [fx.birth("h1", "2026-10-31T09:00:00", "Todo")]) == \
        ["YESTERDAY"]
    assert headers("honly", [Task("H row", id="h1")],
                   [fx.birth("h1", "2026-10-31T09:00:00", "Todo")]) == ["YESTERDAY ≈"]
    assert headers("htoday", [Task("H row", id="h1")],
                   [fx.birth("h1", "2026-11-01T07:05:00", "Todo")]) == ["TODAY ≈"]
    days = [fx.make_task("Early", created="2026-10-05T09:00:00", id="e1"),
            fx.make_task("Ahead", created="2026-11-02T09:00:00", id="e2")]
    assert headers("days", days, []) == ["MON NOV 02", "MON OCT 05"]


def test_TC_4330_the_pane_heads_with_title_chip_meta_source_and_rule(tmp_path):
    """TC-4330 (LLR-4303.10): pane lines 1–5 for w2 at 118x30: the title in bold ink;
    `Eval harness · Work` (project hue, a dim ` · `, the board's colour); the meta line;
    the source line; a rule of 67 `─` (NC source line missing)."""
    body, _ = _fv_body(tmp_path)
    assert _pane(body, 116)[:5] == [
        "Sync notes", "Eval harness · Work",
        "Doing  ▲ high  Oct 30→Nov 3  ◆ milestone  @Ana Ruiz  ↗ 1  ▤ 1",
        "added Sat Oct 31 · 18:20 · the created field", "─" * 67]
    lines = fx.text_lines(body)
    assert all(fx.colour_at(lines[2], 49 + i) == fx.INK and fx.bold_at(lines[2], 49 + i)
               for i in range(10))
    chip = lines[3]
    assert fx.colour_at(chip, 49) == fx.BLUE and fx.colour_at(chip, 49 + 13) == fx.DIM
    assert fx.colour_at(chip, 49 + 15) == views.board_hex("sky")
    assert fx.colour_at(lines[5], 49) == fx.MUT


def test_TC_4331_the_meta_line_holds_every_fact_the_task_has(tmp_path):
    """TC-4331 (LLR-4303.11): w2 (all seven facts) → `Doing  ▲ high  Oct 30→Nov 3  ◆
    milestone  @Ana Ruiz  ↗ 1  ▤ 1` in one line at 118 (7/7, each in its style), two at
    80 (7/7, P-V-3); the bare w1 → `Backlog  · normal` (2 pieces). NC drop the dates."""
    body, _ = _fv_body(tmp_path)
    line = fx.text_lines(body)[4]
    meta = line.plain[49:].rstrip()
    expect = [("Doing", fx.SKY, False), ("▲ high", fx.ROSE, False),
              ("Oct 30→Nov 3", fx.MUT, False), ("◆ milestone", fx.MUT, False),
              ("@Ana Ruiz", fx.PINK, True), ("↗ 1", fx.MUT, False), ("▤ 1", fx.MUT, False)]
    assert meta == "  ".join(p for p, _c, _b in expect)
    for piece, colour, bold in expect:
        i = 49 + meta.index(piece)
        assert (fx.colour_at(line, i), fx.bold_at(line, i)) == (colour, bold), piece
    body, _ = _fv_body(tmp_path / "n", width=78, height=23)
    assert _pane(body, 78)[2:4] == ["Doing  ▲ high  Oct 30→Nov 3  ◆ milestone",
                                    "@Ana Ruiz  ↗ 1  ▤ 1"]
    body, listed = _fv_body(tmp_path / "b", sel=5)
    assert listed[5].task.id == "w1"
    assert _pane(body, 116)[2] == "Backlog  · normal"


def test_TC_4332_notes_are_drawn_through_notes_text_never_as_markers(tmp_path):
    """TC-4332 (LLR-4303.12): `::b:: ask the vendor ::` → `ask the vendor` in blue, no
    `::` drawn (NC plain Text(notes)); a mention drawn `@Ana Ruiz` bold pink; a long
    green note wraps at the pane width keeping its colour."""
    body, _ = _fv_body(tmp_path)
    assert "::" not in body.plain
    lines = fx.text_lines(body)
    assert lines[7].plain[49:].rstrip() == "ask the vendor"
    assert all(fx.colour_at(lines[7], 49 + i) == fx.BLUE for i in range(14))
    ping = lines[8]
    assert ping.plain[49:].rstrip() == "ping @Ana Ruiz before Friday"
    assert fx.colour_at(ping, 49) == fx.MUT
    assert (fx.colour_at(ping, 54), fx.bold_at(ping, 54)) == (fx.PINK, True)
    assert fx.colour_at(ping, 49 + 15) == fx.MUT
    note = "::g:: done: the rubric draft is ready for the pilot review on friday :: then ship"
    lanes = fx.solo_lanes(tmp_path / "g", [fx.make_task("Green", created="2026-11-01T08:00:00",
                                                        notes=note, id="g1")])
    body, _ = _listed_body(lanes, width=78, height=23)
    pane = _pane(body, 78)
    i = next(k for k, ln in enumerate(pane) if ln.startswith("done:"))
    assert pane[i:i + 2] == ["done: the rubric draft is ready for the",
                             "pilot review on friday then ship"]
    tl = fx.text_lines(body)
    assert fx.colour_at(tl[2 + i], 37) == fx.GREEN
    assert fx.colour_at(tl[3 + i], 37) == fx.GREEN
    assert fx.colour_at(tl[3 + i], 37 + len("pilot review on friday ")) == fx.MUT


def test_TC_4332b_a_huge_note_is_cut_before_it_is_wrapped(tmp_path, monkeypatch):
    """TC-4332b (SEC-4, addendum A-3): a 5 000 000-character note → at most
    `room × (rw + 1)` characters reach `notes_text` (the spy arm, CR-5: deterministic, so a
    mutant that wraps the whole note and still reports `cut` fails without a timing
    threshold); the pane ends `… more lines` (no count) and one paint at 118x30 takes under
    50 ms (best of 3; the uncut wrap measured 0.92 s)."""
    note = "lorem " * (5_000_000 // 6)
    lanes = fx.solo_lanes(tmp_path, [fx.make_task("Huge", created="2026-11-01T08:00:00",
                                                  notes=note, id="hg")])
    rows = _rows(lanes)
    first = _v("first_created")(rows)
    # the spy arm: render_added_list's module looks `notes_text` up by name at call time
    width, height = 116, 29                         # the body of 118x30
    rw = max(0, width - _lw(width) - 3)             # graph-proto-V render_added_list
    room = max(0, height - 2)
    assert (rw, room) == (67, 27)
    seen_lens: list[int] = []
    real_notes_text = views.notes_text

    def spy(text, people=None):
        seen_lens.append(len(text))
        return real_notes_text(text, people)

    monkeypatch.setattr(views, "notes_text", spy)
    body = _render(rows, 0, True, False, 0, 0, first, fx.TODAY, {}, width, height)
    monkeypatch.setattr(views, "notes_text", real_notes_text)
    assert seen_lens, "the cursor's note never reached notes_text"
    assert max(seen_lens) <= room * (rw + 1), \
        f"{max(seen_lens)} characters reached notes_text (cap {room * (rw + 1)})"
    assert _pane(body, 116)[-1] == "… more lines"
    best = 9.9
    for _ in range(3):
        t0 = time.perf_counter()
        body = _render(rows, 0, True, False, 0, 0, first, fx.TODAY, {}, 116, 29)
        best = min(best, time.perf_counter() - t0)
    assert _pane(body, 116)[-1] == "… more lines"
    assert best < 0.05, f"one paint took {best:.3f} s"


def test_TC_4333_the_pane_lists_urls_images_and_what_the_task_waits_on(tmp_path):
    """TC-4333 (LLR-4303.13): after w2's notes: `↗ https://example.com/spec` (cyan),
    `▤ board.png` (muted) and `after: Pilot store list` (muted) — 3/3 (NC drop
    `after:`)."""
    body, _ = _fv_body(tmp_path)
    lines = fx.text_lines(body)
    assert [lines[i].plain[49:].rstrip() for i in (9, 10, 11)] == [
        "↗ https://example.com/spec", "▤ board.png", "after: Pilot store list"]
    assert [fx.colour_at(lines[i], 49) for i in (9, 10, 11)] == [fx.CYAN, fx.MUT, fx.MUT]


def _big(tmp_path):
    tasks = [fx.make_task(f"Task {k:02d}", created=f"2026-10-{1 + k % 28:02d}T09:{k:02d}:00",
                          phase="Todo", id=f"k{k:02d}") for k in range(40)]
    return fx.solo_lanes(tmp_path, tasks, name="Big")


def test_TC_4335_the_list_scrolls_to_keep_the_cursor_on_screen(tmp_path):
    """TC-4335 (LLR-4303.15): 40 tasks at 80x24, the cursor on the last (oldest) row →
    its row `▶09:00  ■□□ ▍Task 00` is the last body line under `THU OCT 01` (NC no
    scroll window: not drawn); with the cursor on row 0 the list starts at the top."""
    body, listed = _listed_body(_big(tmp_path), sel=39, width=78, height=23)
    assert listed[39].task.title == "Task 00"
    lines = _plain_lines(body)
    assert lines[22][:34].rstrip() == "▶09:00  ■□□ ▍Task 00"
    assert lines[20][:34].rstrip() == "THU OCT 01"
    body, _ = _listed_body(_big(tmp_path / "top"), sel=0, width=78, height=23)
    rows, headers = _list(body, 78)
    assert rows[0]["cursor"] and rows[0]["title"] == "Task 27" and rows[0]["y"] == 3


def test_TC_4335_a_note_longer_than_the_pane_ends_with_a_count(tmp_path):
    """TC-4335 (P-V-7 under LLR-4303.12): a 40-line note at 80x24 → body lines 2–21 hold
    pane lines 1–20, line 22 reads `… 26 more lines` in dim; a 100 000-character note
    reads `… more lines` (cut, no count: A-3)."""
    note = "\n".join(f"line {i}" for i in range(40))
    lanes = fx.solo_lanes(tmp_path, [fx.make_task("Long note", created="2026-10-31T18:20:00",
                                                  notes=note, id="ln")])
    body, _ = _listed_body(lanes, width=78, height=23)
    pane = _pane(body, 78)
    assert pane[6] == "line 0" and pane[19] == "line 13"
    assert pane[20] == "… 26 more lines"
    assert fx.colour_at(fx.text_lines(body)[22], 37) == fx.DIM
    lanes = fx.solo_lanes(tmp_path / "b", [fx.make_task("Huge", created="2026-10-31T18:20:00",
                                                        notes="x" * 100_000, id="hx")])
    body, _ = _listed_body(lanes, width=78, height=23)
    assert _pane(body, 78)[20] == "… more lines"
    assert fx.colour_at(fx.text_lines(body)[22], 37) == fx.DIM


def test_TC_4337_an_empty_list_says_so(tmp_path):
    """TC-4337 (LLR-4303.17): rows [] → the list area's first line `no tasks to list` in
    dim, the pane blank, `│` still at cell 47 on lines 2–28 (NC blank)."""
    body = _render([], 0, True, False, 1, 0, None, fx.TODAY, {}, 116, 29)
    lines = _plain_lines(body)
    assert lines[2].startswith("no tasks to list")
    assert fx.colour_at(fx.text_lines(body)[2], 0) == fx.DIM
    assert all(ln.index("│") == 47 and not ln[48:].strip() for ln in lines[2:])


def test_TC_4340_board_text_that_looks_like_markup_is_drawn_literally(tmp_path):
    """TC-4340 (LLR-4303.20): a title `[red]x[/red]`, a project `[b]P[/b]`, a board
    `[i]B[/i]` and a note holding `[red]x[/red]` → drawn as typed in the row and the pane
    (NC `Text.from_markup(title)`), the pen span still blue."""
    p = Project("[b]P[/b]", "blue", id="pp")
    lanes = fx.solo_lanes(tmp_path, [fx.make_task(
        "[red]x[/red]", created="2026-11-01T08:00:00", project_id="pp",
        notes="[red]x[/red] ::b:: ask the vendor ::", id="m")], name="[i]B[/i]", projects=[p])
    body, _ = _listed_body(lanes)
    lines = _plain_lines(body)
    assert lines[3][:46].rstrip() == "▶08:00  ■□□ ▍[red]x[/red]"
    pane = _pane(body, 116)
    assert pane[0] == "[red]x[/red]" and pane[1] == "[b]P[/b] · [i]B[/i]"
    note = next(k for k, ln in enumerate(pane) if ln.startswith("[red]x[/red] ask"))
    assert pane[note] == "[red]x[/red] ask the vendor"
    tl = fx.text_lines(body)[2 + note]
    assert fx.colour_at(tl, 49 + len("[red]x[/red] ")) == fx.BLUE


def test_TC_4369_time_labels_say_how_the_moment_is_known(tmp_path):
    """TC-4369 (LLR-4304.9): F-V's rows, newest first → `08:10`, `21:47`, `18:20`,
    `≈10:30`, `?`, `?` (ink ×3, muted, dim ×2; NC no ≈)."""
    body, _ = _fv_body(tmp_path)
    rows, _ = _list(body, 116)
    assert [r["label"] for r in rows] == ["08:10", "21:47", "18:20", "≈10:30", "?", "?"]
    tl = fx.text_lines(body)
    assert [fx.colour_at(tl[r["y"]], 1) for r in rows] == [fx.INK] * 3 + [fx.MUT] + [fx.DIM] * 2


def test_TC_4374_the_head_names_the_order_and_the_legend(tmp_path):
    """TC-4374 (LLR-4304.14): at 118x30 the head is `ADDED  6 tasks · every board ·
    newest first  ·  time = created  ≈ = history  ? = unknown · 1 archived hidden`;
    oldest first names `oldest first` (NC fixed text)."""
    body, _ = _fv_body(tmp_path)
    assert _plain_lines(body)[0].rstrip() == HEAD_116
    body, _ = _fv_body(tmp_path / "o", sel=0, newest=False)
    assert _plain_lines(body)[0].rstrip() == HEAD_116.replace("newest first", "oldest first")


def _head(rows, **kw):
    return fx.text_lines(_render(rows, 0, **kw))[0]


def test_TC_4326_the_head_counts_boards_not_read(tmp_path):
    """TC-4326 (LLR-4303.6, P-V-6): unread 1 → `· 1 board not read` (amber) before the
    archived count, each piece in its style; unread 2 → `· 2 boards not read`; at 80 the
    legend goes first and the counts stay (NC silent skip)."""
    listed = _order(_rows(fx.fv_lanes(tmp_path)), True, False)
    head = _head(listed, hidden=1, unread=1, width=116)
    want = ("ADDED  6 tasks · newest first  ·  time = created  ≈ = history  ? = unknown · "
            "1 board not read · 1 archived hidden")
    assert head.plain.rstrip() == want
    p = head.plain
    for piece, colour, bold in (("ADDED", fx.ACCENT, True), ("6 tasks", fx.MUT, False),
                                ("newest first", fx.INK, True), ("time = created", fx.DIM, False),
                                ("1 board not read", fx.SOON, False),
                                ("1 archived hidden", fx.MUT, False)):
        i = p.index(piece)
        assert (fx.colour_at(head, i), fx.bold_at(head, i)) == (colour, bold), piece
    assert _head(listed, hidden=1, unread=2, width=116).plain.rstrip().endswith(
        "· 2 boards not read · 1 archived hidden")
    assert _head(listed, hidden=1, unread=2, width=78, height=23).plain.rstrip() == \
        "ADDED  6 tasks · newest first · 2 boards not read · 1 archived hidden"


def test_TC_4396_the_head_ends_with_the_archived_state(tmp_path):
    """TC-4396 (LLR-4306.6): shown → ends `? = unknown · archived shown`; hidden 1 at 80
    → `… ≈ = his… · 1 archived hidden`; hidden 0 → no archived piece (NC no count)."""
    rows = _rows(fx.fv_lanes(tmp_path))
    shown = _order(rows, True, True)
    assert _head(shown, show=True, width=116).plain.rstrip().endswith(
        "? = unknown · archived shown")
    listed = _order(rows, True, False)
    assert _head(listed, hidden=1, width=78, height=23).plain.rstrip() == HEAD_78
    assert _head(listed, hidden=0, width=78, height=23).plain.rstrip() == \
        "ADDED  6 tasks · newest first  ·  time = created  ≈ = history  ? = unknown"


def test_TC_4381_boxes_fill_up_to_and_including_the_phase():
    """TC-4381 (LLR-4305.1): Backlog Doing Review Done → `■□□□`, `■■□□`, `■■■□`, `■■■■`
    (NC exclusive fill: `□□□□` for Backlog)."""
    state_boxes = _v("state_boxes")
    phases = ["Backlog", "Doing", "Review", "Done"]
    assert [state_boxes(phases, p) for p in phases] == ["■□□□", "■■□□", "■■■□", "■■■■"]


def test_TC_4382_more_than_eight_phases_draw_eight_boxes():
    """TC-4382 (LLR-4305.2): 10 phases → 8 boxes, ceil(8 × (i + 1) / 10) filled: index 0
    → 1, 4 → 4, 9 → 8 (NC 10 boxes)."""
    state_boxes = _v("state_boxes")
    phases = [f"P{i}" for i in range(10)]
    assert state_boxes(phases, "P0") == "■□□□□□□□"
    assert state_boxes(phases, "P4") == "■■■■□□□□"
    assert state_boxes(phases, "P9") == "■■■■■■■■"


def test_TC_4383_the_state_column_is_as_wide_as_the_widest_board(tmp_path):
    """TC-4383 (LLR-4305.3): a 3-phase and a 5-phase row → `▶07:00  ■□□   ▍Three` and
    ` 06:00  ■■■□□ ▍Five`, both titles at cell 15; with a 10-phase row at 80 → titles at
    cell 18 (NC no padding)."""
    def two(name, other_phases, other_phase, other_title, other_at, width, height):
        a = Board([], [fx.make_task("Three", created="2026-11-01T07:00:00", phase="A", id="t3")],
                  tmp_path / name / "a" / "board.json", {}, ["A", "B", "C"])
        b = Board([], [fx.make_task(other_title, created=other_at, phase=other_phase, id="t5")],
                  tmp_path / name / "b" / "board.json", {}, other_phases)
        for bd in (a, b):
            bd.path.parent.mkdir(parents=True, exist_ok=True)
        body, _ = _listed_body([("A", "sky", a, ""), ("B", "lime", b, "")], width=width,
                               height=height)
        return _list(body, width)[0]

    rows = two("five", ["A", "B", "C", "D", "E"], "C", "Five", "2026-11-01T06:00:00", 116, 29)
    assert [r["title"] for r in rows] == ["Three", "Five"]
    assert [r["title_at"] for r in rows] == [15, 15]
    assert [r["boxes"] for r in rows] == ["■□□", "■■■□□"]
    rows = two("ten", [f"P{i}" for i in range(10)], "P4", "Ten", "2026-11-01T05:00:00", 78, 23)
    assert [r["title_at"] for r in rows] == [18, 18]
    assert [r["boxes"] for r in rows] == ["■□□", "■■■■□□□□"]


def test_TC_4384_the_state_column_is_ink_and_dim_only(tmp_path):
    """TC-4384 (LLR-4305.4): over F-V's six rows the state-column cells carry only ink
    (filled) and dim (empty) — no phase hue; the hue bar `▍` is the project's (green for
    House, dim for the Inbox)."""
    body, _ = _fv_body(tmp_path)
    tl = fx.text_lines(body)
    rows, _ = _list(body, 116)
    colours = set()
    for r in rows:
        line = tl[r["y"]]
        for i in range(8, 12):
            ch = line.plain[i]
            if ch in "■□":
                c = fx.colour_at(line, i)
                assert c == (fx.INK if ch == "■" else fx.DIM), (r["title"], i, c)
                colours.add(c)
    assert colours == {fx.INK, fx.DIM}
    by = {r["title"]: r for r in rows}
    assert fx.colour_at(tl[by["Compose file anatomy"]["y"]], 13) == fx.GREEN
    assert fx.colour_at(tl[by["Hybrid search index"]["y"]], 13) == fx.DIM


def test_TC_4395_archived_rows_are_dimmed_while_shown(tmp_path):
    """TC-4395 (LLR-4306.5): archived shown → w5's row ` ?      ■■■■ ▍Old archived` with
    its title in dim; under the cursor, bold dim (NC no dimming)."""
    body, listed = _fv_body(tmp_path, sel=0, show=True)
    k = _ids(listed).index("w5")
    rows, _ = _list(body, 116)
    row = rows[k]
    line = fx.text_lines(body)[row["y"]]
    assert line.plain[:46].rstrip() == " ?      ■■■■ ▍Old archived"
    assert fx.colour_at(line, 14) == fx.DIM and not fx.bold_at(line, 14)
    body, _ = _fv_body(tmp_path / "on", sel=k, show=True)
    line = fx.text_lines(body)[row["y"]]
    assert line.plain.startswith("▶") and fx.colour_at(line, 14) == fx.DIM
    assert fx.bold_at(line, 14)


def test_TC_4397_the_meta_line_says_archived(tmp_path):
    """TC-4397 (LLR-4306.7): archived shown, the cursor on w5 → meta `Done  archived  ·
    normal` (NC no word)."""
    rows = _order(_rows(fx.fv_lanes(tmp_path)), True, True)
    k = _ids(rows).index("w5")
    body, _ = _fv_body(tmp_path / "m", sel=k, show=True)
    assert _pane(body, 116)[2] == "Done  archived  · normal"


# --------------------------------------------------------------------------- #
# LLR-4303.1, LLR-4303.23 — the seat and the README
# --------------------------------------------------------------------------- #
def test_TC_4321_N_is_one_global_key_of_the_seat():
    """TC-4321 (LLR-4303.1): exactly one KEYMAP entry `N` → `added_list`, label `Added
    list`, `bar=False`, no `views`, not priority (like `A`); the app has the action; the
    `?` help's global keys read … A N n @ … (`H` moved to the bar in Inc X, ruling 15);
    every palette lists N once (NC missing)."""
    entries = [k for k in keymap.KEYMAP if k.keys == "N"]
    assert len(entries) == 1, "no KEYMAP entry for N"
    n = entries[0]
    assert (n.show, n.action, n.label, n.bar, n.views, n.priority, n.group) == \
        ("N", "added_list", "Added list", False, None, False, "misc")
    assert hasattr(TaskboardApp, "action_added_list")
    assert [k.show for k in keymap.global_keys("gantt")] == [
        "o", "i", "p", "P", "f", "c", "R", "A", "N", "n", "@", "#", "I", "S"]  # n: Inc K, LLR-4401.1
    assert keymap.palette_commands("swimlanes").count(("N", "Added list", "added_list")) == 1


def test_TC_4343_the_readme_key_table_has_a_row_for_N():
    """TC-4343 (LLR-4303.23): the README's `## Keys` table carries a `| `N` |` row,
    right after the `A` row — the row `test_keymap.py::test_the_readme_keybinding_table_
    matches_the_seat` needs once `N` is bound (NC no row)."""
    readme = (Path(__file__).resolve().parents[1] / "README.md").read_text(encoding="utf-8")
    lines = readme.splitlines()
    keys = lines.index("## Keys")
    a = next(i for i in range(keys, len(lines)) if lines[i].startswith("| `A` |"))
    assert lines[a + 1].startswith("| `N` |"), lines[a + 1]


# --------------------------------------------------------------------------- #
# pilots — the S fixture through the shipped app
# --------------------------------------------------------------------------- #
FILES = (("alpha", "board"), ("beta", "board"), ("alpha", "history"), ("beta", "history"))


def _hashes(home_dir) -> dict:
    out = {}
    for bid, kind in FILES:
        p = fx.board_path(home_dir, bid) if kind == "board" else fx.history_file(home_dir, bid)
        out[(bid, kind)] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


async def _leave_home(pilot, app):
    await pilot.pause()
    if type(app.screen).__name__ == "BoardsHome":
        await press(pilot, "escape")
    assert names(app) == ["Screen"], names(app)


async def test_TC_4322_N_opens_the_list_view(home):
    """TC-4322 (LLR-4303.2): `N` on the main screen → the list view is `app.screen`,
    its head names `newest first`, its key row starts with the five keys (NC unbound)."""
    fx.build(home)
    app = open_s_app()
    async with app.run_test(size=W118) as pilot:
        await _leave_home(pilot, app)
        await open_list(pilot, app)
        assert names(app) == ["Screen", "AddedList"]
        _rows_, _h, _p, head = seen(app, 118)
        assert "newest first" in head
        assert key_row(app).startswith(KEYS_5)


async def test_TC_4323_N_brings_the_open_list_back_without_a_second_one(home):
    """TC-4323 (LLR-4303.3, LLR-4303.5): `N`, `A`, `N` → exactly one list view, the
    SAME one (read once), on top (NC always push: 2); `A` on the agenda and `escape`
    unwind to the board."""
    fx.build(home)
    app = open_s_app()
    async with app.run_test(size=W118) as pilot:
        await _leave_home(pilot, app)
        await open_list(pilot, app)
        first = app.screen
        await press(pilot, "A")
        assert names(app) == ["Screen", "AddedList", "AllBoardsAgenda"]
        await press(pilot, "N")
        assert lists_on_stack(app) == 1 and app.screen is first
        assert names(app) == ["Screen", "AddedList"]
        await press(pilot, "A")
        await press(pilot, "A")
        assert names(app) == ["Screen", "AddedList"]
        await press(pilot, "escape")
        assert names(app) == ["Screen"]


async def test_TC_4324_escape_or_N_closes_the_list(home):
    """TC-4324 (LLR-4303.4): `escape` closes the list; `N` in the list closes it too (NC
    `N` not bound in the screen: the list stays)."""
    fx.build(home)
    app = open_s_app()
    async with app.run_test(size=W118) as pilot:
        await _leave_home(pilot, app)
        await open_list(pilot, app)
        await press(pilot, "escape")
        assert names(app) == ["Screen"]
        await open_list(pilot, app)
        await press(pilot, "N")
        assert names(app) == ["Screen"] and lists_on_stack(app) == 0


async def test_TC_4324_N_on_the_home_opens_over_it_and_N_closes_it(home):
    """TC-4324 (LLR-4303.2, LLR-4303.4): at start (the home on top) `N` opens the list
    over the home; `N` returns to the home."""
    fx.build(home)
    app = open_s_app()
    async with app.run_test(size=W118) as pilot:
        await pilot.pause()
        assert names(app) == ["Screen", "BoardsHome"]
        await open_list(pilot, app)
        assert names(app) == ["Screen", "BoardsHome", "AddedList"]
        await press(pilot, "N")
        assert names(app) == ["Screen", "BoardsHome"]


async def test_TC_4325_the_list_reads_every_board_of_the_registry(home):
    """TC-4325 (LLR-4303.5): a registry of 2 boards (3 + 2 tasks) → 5 rows, both boards'
    tasks (NC only `app.board`: 3)."""
    fx.build(home)
    app = open_s_app()
    async with app.run_test(size=W118) as pilot:
        await _leave_home(pilot, app)
        await open_list(pilot, app)
        rows, _h, _p, head = seen(app, 118)
        assert sorted(titles(rows)) == sorted(["Sync notes", "Pilot store list", "Old invoice",
                                               "Pay the rent", "Archive scans"])
        assert "5 tasks" in head


async def test_TC_4326_a_board_whose_file_is_missing_is_counted_not_read(home):
    """TC-4326 (LLR-4303.6): Beta's file deleted → the head holds `1 board not read`,
    Alpha's 3 rows listed (NC silent skip)."""
    fx.build(home)
    fx.board_path(home, "beta").unlink()
    app = open_s_app()
    async with app.run_test(size=W118) as pilot:
        await _leave_home(pilot, app)
        await open_list(pilot, app)
        rows, _h, _p, head = seen(app, 118)
        assert "1 board not read" in head and len(rows) == 3


async def test_TC_4327_the_separator_follows_the_terminal_width(home):
    """TC-4327 (LLR-4303.7): at 118x30 the `│` is at screen column 48 (cell 47 after the
    1-cell gutter) on every body line; after a resize to 80x24 at body cell 35 (NC one
    width for both)."""
    from test_modal_keys import _svg_rows
    fx.build(home)
    app = open_s_app()
    async with app.run_test(size=W118) as pilot:
        await _leave_home(pilot, app)
        await open_list(pilot, app)
        lines = fx.body_lines(app)
        assert all(ln.index("│") == 47 for ln in lines[2:29]), lines[2:4]
        await pilot.pause(0.3)
        screen = _svg_rows(app.export_screenshot(), 118, 30)
        assert all(len(r) > 48 and r[48] == "│" for r in screen[2:29]), screen[2:4]
        await pilot.resize_terminal(80, 24)
        await pilot.pause(0.3)
        lines = fx.body_lines(app)
        assert len(lines) == 23
        assert all(ln.index("│") == 35 for ln in lines[2:23]), lines[2:4]


async def test_TC_4334_up_and_down_move_the_cursor_clamped(home):
    """TC-4334 (LLR-4303.14): one board, 3 rows: `up` at row 0 stays 0; `down` ×5 ends
    at 2; `k` → 1; `j` → 2 (NC no clamp)."""
    fx.build(home, only_alpha=True)
    app = open_s_app()
    async with app.run_test(size=W80) as pilot:
        await _leave_home(pilot, app)
        await open_list(pilot, app)
        rows, *_ = seen(app, 80)
        assert titles(rows) == ["Sync notes", "Pilot store list", "Old invoice"]
        await press(pilot, "up")
        assert cursor(seen(app, 80)[0]) == 0
        await press(pilot, *["down"] * 5)
        assert cursor(seen(app, 80)[0]) == 2
        await press(pilot, "k")
        assert cursor(seen(app, 80)[0]) == 1
        await press(pilot, "j")
        assert cursor(seen(app, 80)[0]) == 2
        assert on_list(app)


async def test_TC_4336_enter_opens_the_task_on_its_board(home):
    """TC-4336 (LLR-4303.16): the cursor on `Sync notes` (the open board), `enter` → the
    list gone, Alpha open, `ta1` selected (NC `enter` unbound)."""
    fx.build(home)
    app = open_s_app()
    async with app.run_test(size=W118) as pilot:
        await _leave_home(pilot, app)
        await open_list(pilot, app)
        await press(pilot, "down")
        assert seen(app, 118)[0][1]["cursor"]
        await press(pilot, "enter")
        assert names(app) == ["Screen"]
        assert (app.board_id, app.selected_task_id) == ("alpha", "ta1")


async def test_TC_4336b_enter_on_another_boards_task_switches_to_it(home):
    """TC-4336b (LLR-4303.16): row 0 `Pay the rent` of Beta, `enter` → Beta open, `tb1`
    selected, the list gone."""
    fx.build(home)
    app = open_s_app()
    async with app.run_test(size=W118) as pilot:
        await _leave_home(pilot, app)
        await open_list(pilot, app)
        assert seen(app, 118)[0][0]["title"] == "Pay the rent"
        await press(pilot, "enter")
        assert names(app) == ["Screen"]
        assert (app.board_id, app.selected_task_id) == ("beta", "tb1")


async def test_TC_4336d_enter_on_a_board_whose_file_went_missing_says_so(home):
    """TC-4336d (LLR-4303.16): Beta's file deleted while the list is open, `enter` on
    `Pay the rent` → the list gone, Alpha still open, a notice `its file is missing`."""
    fx.build(home)
    app = open_s_app()
    async with app.run_test(size=W118, notifications=True) as pilot:
        await _leave_home(pilot, app)
        await open_list(pilot, app)
        fx.board_path(home, "beta").unlink()
        await press(pilot, "enter")
        assert names(app) == ["Screen"] and app.board_id == "alpha"
        assert any("its file is missing" in m for m in notices(app))


async def test_TC_4338_an_empty_list_ignores_enter_and_the_arrows(home):
    """TC-4338 (LLR-4303.17, LLR-4303.18): every task archived → `no tasks to list`;
    `up`, `down`, `enter` change nothing: still the list, the selection unchanged, 0
    exceptions (NC index the empty list)."""
    fx.build(home, only_alpha=True, all_archived=True)
    app = open_s_app()
    async with app.run_test(size=W118) as pilot:
        await _leave_home(pilot, app)
        before = app.selected_task_id
        await open_list(pilot, app)
        lines = fx.body_lines(app)
        assert lines[2].startswith("no tasks to list")
        for key in ("up", "down", "enter"):
            await press(pilot, key)
            assert on_list(app), key
            assert fx.body_lines(app)[2].startswith("no tasks to list")
        assert app.selected_task_id == before


@pytest.mark.parametrize("size", [W80, W118])
async def test_TC_4339_the_key_row_shows_every_key_the_view_binds(home, size):
    """TC-4339 (LLR-4303.19, A-2): at 80x24 the key row is the five keys, the read-only
    tail dropped (all 5 glyphs); at 118x30 the five keys and `· read-only: nothing here
    edits a task` (all 5 words) (NC omit `v`)."""
    fx.build(home)
    app = open_s_app()
    async with app.run_test(size=size) as pilot:
        await _leave_home(pilot, app)
        await open_list(pilot, app)
        row = key_row(app).rstrip()
        if size == W80:
            assert row == KEYS_5 and "read-only" not in row
            assert all(g in row for g in ("↑↓", "↵", "o ", "v ", "esc / N"))
        else:
            assert row == KEYS_5 + READ_ONLY
            assert all(w in row for w in ("move", "open on board", "newest/oldest",
                                          "archived", "back"))


async def test_TC_4341_added_list_is_refused_under_a_modal(home):
    """TC-4341 (LLR-4303.21, P-S-1): `app.check_action("added_list", ())` is True on the
    main screen and False with the task editor or a confirmation on the stack — the only
    arm that can fail the NC (`added_list` not gated); `N` typed in the editor types `N`
    and opens no list."""
    from taskboard.modals import ConfirmModal
    fx.build(home)
    app = open_s_app()
    async with app.run_test(size=W118) as pilot:
        await _leave_home(pilot, app)
        assert app.check_action("added_list", ()) is True
        await press(pilot, "a")
        assert names(app) == ["Screen", "TaskModal"]
        assert app.check_action("added_list", ()) is False
        await press(pilot, "N")
        assert names(app) == ["Screen", "TaskModal"]
        from textual.widgets import Input
        assert app.screen.query_one("#f-title", Input).value == "N"
        await press(pilot, "escape")
        app.push_screen(ConfirmModal("Delete 'x'?"))
        await pilot.pause()
        assert app.check_action("added_list", ()) is False


async def test_TC_4342_the_list_holds_the_seat(home):
    """TC-4342 (LLR-4303.22): with the list open `a` opens no editor, `d` deletes
    nothing, `A` and `@` open over it and `N` comes back to it; the seat answers quit
    yes, templates no, agenda_all yes (NC the list missing from the holding tuple)."""
    fx.build(home)
    app = open_s_app()
    async with app.run_test(size=W118) as pilot:
        await _leave_home(pilot, app)
        await open_list(pilot, app)
        await press(pilot, "a")
        assert names(app) == ["Screen", "AddedList"]
        await press(pilot, "d")
        assert names(app) == ["Screen", "AddedList"] and len(app.board.tasks) == 3
        assert app.check_action("quit", ()) is True
        assert app.check_action("templates", ()) is False
        assert app.check_action("agenda_all", ()) is True
        await press(pilot, "A")
        assert names(app) == ["Screen", "AddedList", "AllBoardsAgenda"]
        await press(pilot, "escape")
        await press(pilot, "at")
        assert names(app) == ["Screen", "AddedList", "PeopleDirectory"]
        await press(pilot, "N")
        assert names(app) == ["Screen", "AddedList"]


async def test_TC_4344_enter_on_an_archived_task_says_so_and_selects_nothing(home):
    """TC-4344 (LLR-4303.24, P-S-3): Alpha (open) holds the archived `Old memo`; the
    list shows it (`v`), `enter` on it → the list gone, the selection unchanged, the main
    screen's `v` still off, the notice `Old memo is archived — v shows it` (NC select
    it)."""
    fx.build(home, archived_on_alpha=True)
    app = open_s_app()
    async with app.run_test(size=W118, notifications=True) as pilot:
        await _leave_home(pilot, app)
        before = app.selected_task_id
        await open_list(pilot, app)
        await press(pilot, "v", "down", "down")
        rows = seen(app, 118)[0]
        assert rows[cursor(rows)]["title"] == "Old memo"
        await press(pilot, "enter")
        assert names(app) == ["Screen"] and app.board_id == "alpha"
        assert app.selected_task_id == before and app.show_archived is False
        assert "Old memo is archived — v shows it" in notices(app)


async def test_TC_4344b_enter_on_another_boards_archived_task_switches_then_says_so(home):
    """TC-4344b (LLR-4303.24): `Old receipts` (archived, Beta) → Beta opens, `tb3` is not
    selected, the notice `Old receipts is archived — v shows it`."""
    fx.build(home, with_archived=True)
    app = open_s_app()
    async with app.run_test(size=W118, notifications=True) as pilot:
        await _leave_home(pilot, app)
        await open_list(pilot, app)
        await press(pilot, "v", "down", "down")
        rows = seen(app, 118)[0]
        assert rows[cursor(rows)]["title"] == "Old receipts"
        await press(pilot, "enter")
        assert names(app) == ["Screen"] and app.board_id == "beta"
        assert app.selected_task_id != "tb3"
        assert "Old receipts is archived — v shows it" in notices(app)


async def test_TC_4366_the_list_opens_newest_first(home):
    """TC-4366 (LLR-4304.6): on open, row 0 is the newest stamped task `Pay the rent`,
    the cursor on it, the head `newest first` (NC oldest first)."""
    fx.build(home)
    app = open_s_app()
    async with app.run_test(size=W118) as pilot:
        await _leave_home(pilot, app)
        await open_list(pilot, app)
        rows, _h, _p, head = seen(app, 118)
        assert rows[0]["title"] == "Pay the rent" and cursor(rows) == 0
        assert "newest first" in head


async def test_TC_4367_o_reverses_the_order_and_puts_the_cursor_on_top(home):
    """TC-4367 (LLR-4304.7): the cursor on row 3, `o` → oldest first, row 0 `Old
    invoice`, the cursor 0 (NC keep the index); `o` → newest first, `Pay the rent`, 0."""
    fx.build(home)
    app = open_s_app()
    async with app.run_test(size=W118) as pilot:
        await _leave_home(pilot, app)
        await open_list(pilot, app)
        await press(pilot, "down", "down", "down")
        assert cursor(seen(app, 118)[0]) == 3
        await press(pilot, "o")
        rows, _h, _p, head = seen(app, 118)
        assert "oldest first" in head and rows[0]["title"] == "Old invoice" and cursor(rows) == 0
        assert titles(rows) == ["Old invoice", "Archive scans", "Pilot store list",
                                "Sync notes", "Pay the rent"]
        await press(pilot, "o")
        rows, _h, _p, head = seen(app, 118)
        assert "newest first" in head and rows[0]["title"] == "Pay the rent" and cursor(rows) == 0


async def test_TC_4392_the_list_opens_with_archived_hidden_whatever_v_says(home):
    """TC-4392 (LLR-4306.2): the main screen showing archived (`v`), then `N` → archived
    hidden: 5 rows, no `Old receipts`, the head ends `· 1 archived hidden`; the main
    screen's `v` left as it was (NC inherit `show_archived`)."""
    fx.build(home, with_archived=True)
    app = open_s_app()
    async with app.run_test(size=W118) as pilot:
        await _leave_home(pilot, app)
        await press(pilot, "v")
        assert app.show_archived is True
        await open_list(pilot, app)
        rows, _h, _p, head = seen(app, 118)
        assert len(rows) == 5 and "Old receipts" not in titles(rows)
        assert head.rstrip().endswith("· 1 archived hidden")
        assert app.show_archived is True


async def test_TC_4393_v_toggles_archived_tasks_both_ways(home):
    """TC-4393 (LLR-4306.3): 5 rows; `v` → 6 (with `Old receipts`); `v` → 5 (NC one-way);
    the main screen's `v` untouched."""
    fx.build(home, with_archived=True)
    app = open_s_app()
    async with app.run_test(size=W118) as pilot:
        await _leave_home(pilot, app)
        await open_list(pilot, app)
        assert len(seen(app, 118)[0]) == 5
        await press(pilot, "v")
        rows = seen(app, 118)[0]
        assert titles(rows) == ["Pay the rent", "Sync notes", "Old receipts", "Pilot store list",
                                "Archive scans", "Old invoice"]
        await press(pilot, "v")
        assert len(seen(app, 118)[0]) == 5
        assert app.show_archived is False


async def test_TC_4394_the_toggle_keeps_the_cursor_on_its_task(home):
    """TC-4394 (LLR-4306.4, P-S-8): the cursor on `Pilot store list` (row 2), `v` → still
    on it (row 3), `v` → row 2 (NC reset to 0); the cursor on the archived `Old receipts`,
    `v` → row 0."""
    fx.build(home, with_archived=True)
    app = open_s_app()
    async with app.run_test(size=W118) as pilot:
        await _leave_home(pilot, app)
        await open_list(pilot, app)
        await press(pilot, "down", "down")

        def on():
            rows = seen(app, 118)[0]
            k = cursor(rows)
            return k, rows[k]["title"]

        assert on() == (2, "Pilot store list")
        await press(pilot, "v")
        assert on() == (3, "Pilot store list")
        await press(pilot, "v")
        assert on() == (2, "Pilot store list")
        await press(pilot, "v", "up")
        assert on() == (2, "Old receipts")
        await press(pilot, "v")
        assert on() == (0, "Pay the rent")


async def test_TC_4317_the_open_list_writes_no_board_and_no_history(home):
    """TC-4317 (LLR-4302.6, P-S-4): sha256 of both boards and both history.jsonl, taken
    after leaving the home, are equal after `N ↓ ↓ o v v esc` (4/4; NC a `save()` in
    the screen's compose)."""
    fx.build(home, with_archived=True)
    app = open_s_app()
    async with app.run_test(size=W118) as pilot:
        await _leave_home(pilot, app)
        before = _hashes(home)
        await open_list(pilot, app)
        await press(pilot, "down", "down", "o", "v", "v", "escape")
        assert names(app) == ["Screen"]
    assert _hashes(home) == before


async def test_TC_4331b_a_name_renamed_under_the_list_shows_when_it_returns(home):
    """TC-4331b (LLR-4303.11, ARCH-5 / A-1): the pane meta of `Sync notes` holds
    `@Ana Ruiz`; `@`, the directory renames `ana` to `Ana Ortiz`, `escape` → with no
    further key the pane holds `@Ana Ortiz` (NC no repaint on resume)."""
    fx.build(home, people={"ana": "Ana Ruiz"}, notes={"ta1": "ping @ana"})
    app = open_s_app()
    async with app.run_test(size=W118) as pilot:
        await _leave_home(pilot, app)
        await open_list(pilot, app)
        await press(pilot, "down")
        assert "@Ana Ruiz" in seen(app, 118)[2][2]
        await press(pilot, "at")
        assert names(app) == ["Screen", "AddedList", "PeopleDirectory"]
        app.people.edit("ana", "Ana Ortiz", "", "")
        await press(pilot, "escape")
        await pilot.pause(0.3)
        assert names(app) == ["Screen", "AddedList"]
        assert "@Ana Ortiz" in seen(app, 118)[2][2]


# --------------------------------------------------------------------------- #
# AT-4301, AT-4304, AT-4305 — black box
# --------------------------------------------------------------------------- #
async def test_AT_4301_one_list_of_every_board_newest_first(home):
    """AT-4301 (US-4301, HLR-4303..4305): two registry boards (3 + 2 tasks, one with 4
    phases): `N` → 5 rows newest first under their day headers with their state boxes;
    `o` → oldest first; `down` → the pane follows; `escape` → the board as it was; the
    board and history bytes unchanged."""
    fx.build(home)
    app = open_s_app()
    async with app.run_test(size=W118) as pilot:
        await _leave_home(pilot, app)
        before, selected = _hashes(home), app.selected_task_id
        await open_list(pilot, app)
        assert names(app) == ["Screen", "AddedList"]
        rows, headers, pane, head = seen(app, 118)
        assert titles(rows) == ["Pay the rent", "Sync notes", "Pilot store list",
                                "Archive scans", "Old invoice"]
        assert headers == ["TODAY", "YESTERDAY", "WED OCT 28 ≈", "BEFORE OCT 31 · ?"]
        assert [r["day"] for r in rows] == ["TODAY", "YESTERDAY", "WED OCT 28 ≈",
                                            "BEFORE OCT 31 · ?", "BEFORE OCT 31 · ?"]
        assert [r["boxes"] for r in rows] == ["■□□", "■■□□", "■□□□", "■■■", "■■■□"]
        assert [r["label"] for r in rows] == ["07:55", "18:20", "≈10:30", "?", "?"]
        assert "newest first" in head and cursor(rows) == 0 and pane[0] == "Pay the rent"
        await press(pilot, "o")
        rows, _h, pane, head = seen(app, 118)
        assert "oldest first" in head and rows[0]["title"] == "Old invoice"
        assert cursor(rows) == 0 and pane[0] == "Old invoice"
        await press(pilot, "down")
        rows, _h, pane, _head = seen(app, 118)
        assert cursor(rows) == 1 and pane[0] == "Archive scans"
        await press(pilot, "escape")
        assert names(app) == ["Screen"]
        assert (app.board_id, app.selected_task_id) == ("alpha", selected)
    assert _hashes(home) == before


async def test_AT_4304_the_archived_toggle(home):
    """AT-4304 (US-4301, HLR-4306): one archived task: `N` → not listed, the head ends
    `1 archived hidden`; `v` → listed under FRI OCT 30, its title dimmed, the head ends
    `archived shown`, the cursor still on `Pay the rent`; `v` → hidden again."""
    fx.build(home, with_archived=True)
    app = open_s_app()
    async with app.run_test(size=W118) as pilot:
        await _leave_home(pilot, app)
        await open_list(pilot, app)
        rows, _h, _p, head = seen(app, 118)
        assert len(rows) == 5 and "Old receipts" not in titles(rows)
        assert head.rstrip().endswith("· 1 archived hidden")
        await press(pilot, "v")
        rows, _h, _p, head = seen(app, 118)
        assert len(rows) == 6 and rows[2]["title"] == "Old receipts"
        assert rows[2]["day"] == "FRI OCT 30"
        assert head.rstrip().endswith("· archived shown")
        assert cursor(rows) == 0 and rows[0]["title"] == "Pay the rent"
        text, styles = fx.cell_colours(fx.body_widget(app), rows[2]["y"])
        at = text.index("Old receipts")
        assert {fx.hex_of(styles[at + i]) for i in range(len("Old receipts"))} == {fx.DIM}
        await press(pilot, "v")
        rows, _h, _p, head = seen(app, 118)
        assert len(rows) == 5 and head.rstrip().endswith("· 1 archived hidden")
        assert cursor(rows) == 0


async def test_AT_4305_old_tasks_are_inferred_honestly_and_never_rewritten(home):
    """AT-4305 (US-4301, HLR-4302, HLR-4304): an old board with a birth record for one
    task and none for another, plus a stamped task: the list shows `18:20`, `≈10:30` and
    `?` with the source lines of LLR-4304.10; after `escape` the board files and the
    histories are byte-identical and the old entries still hold no `created`."""
    fx.build(home)
    app = open_s_app()
    async with app.run_test(size=W118) as pilot:
        await _leave_home(pilot, app)
        before = _hashes(home)
        await open_list(pilot, app)
        steps = [(["down"], "18:20", "added Sat Oct 31 · 18:20 · the created field"),
                 (["down"], "≈10:30", "added ≈ Wed Oct 28 · 10:30 · from history.jsonl"),
                 (["down", "down"], "?",
                  "added: unknown, before Oct 31 · #3 in Alpha's board file")]
        for keys, label, source in steps:
            await press(pilot, *keys)
            rows, _h, pane, _head = seen(app, 118)
            assert rows[cursor(rows)]["label"] == label
            assert pane[3] == source
        await press(pilot, "escape")
        assert names(app) == ["Screen"]
    assert _hashes(home) == before
    recs = {r["id"]: r for r in json.loads(
        fx.board_path(home, "alpha").read_text(encoding="utf-8"))["tasks"]}
    assert "created" not in recs["ta2"] and "created" not in recs["ta3"]
