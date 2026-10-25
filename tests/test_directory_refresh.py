"""The directories stay fresh across windows (batch 2026-10-24-batch-02, HD-5).

HLR-2706 / LLR-2706.1, LLR-2706.2, LLR-2706.3 · TC-2701 · AT-2706 (US-2702):
`people.Directory` and `marks.Directory` re-read their files when the mtime or
size moved since the last read, swapping the entries into the live dict in
place — a person or class another window added shows in the `@` picker, the
`#` manager, the editor's `alt+m` Select and the `/` `@…` completion without a
restart. HLR-2707 / LLR-2707.1 · TC-2702 · AT-2707: a re-read that cannot parse
the file keeps the in-memory directory and is said once (markup=False). The
`/` seat fires the re-read the first time its query names `@`/`#`, an initial
query included (PDR #D3). Synthetic data only: the multi-board round's boards
(`tests/multi_board_fixture.py`), trimmed to two, under this test's own
temporary home; the other window is a second `Directory` instance.
"""
from __future__ import annotations

import json
import os
from datetime import date, datetime
from pathlib import Path

import pytest
from textual.widgets import Input, Select

import multi_board_fixture as mb
from taskboard import app as app_module
from taskboard import marks as marks_module
from taskboard import modals
from taskboard.marks import COLOURS, MARKS_NAME, SHAPES
from taskboard.people import PEOPLE_NAME
from test_home_deferred_start import _open, _press, _two_boards
from test_people_look import screen_text


class _Today(date):
    @classmethod
    def today(cls):
        return mb.TODAY


class _Now(datetime):
    @classmethod
    def now(cls, tz=None):
        return datetime(2026, 10, 20, 9, 30)


@pytest.fixture
def home(tmp_path, monkeypatch):
    """`Path.home()` → this test's folder; the calendar and the clock frozen at
    every module that reads them (the house pattern of tests/test_boards_home.py)."""
    from taskboard import models, views
    import taskboard.__main__ as entry
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
    for mod in (app_module, models, views, modals):
        monkeypatch.setattr(mod, "date", _Today)
    monkeypatch.setattr(app_module, "datetime", _Now)
    monkeypatch.setattr(entry, "datetime", _Now)
    return tmp_path / ".taskboard"


# --------------------------------------------------------------------------- #
# The directory files: one entry seeded, the other window's entry appended
# --------------------------------------------------------------------------- #
def _seed_people(path: Path, extra: bool = False) -> None:
    people = [{"id": "ada.one", "name": "Ada One", "role": "", "note": ""}]
    if extra:
        people.append({"id": "zoe.quill", "name": "Zoe Quill", "role": "", "note": ""})
    path.write_text(json.dumps({"version": 1, "people": people}, indent=2,
                               ensure_ascii=False), encoding="utf-8")


def _seed_marks(path: Path, extra: bool = False) -> None:
    marks = [{"id": "basics", "name": "Basics", "shape": SHAPES[0], "colour": COLOURS[0]}]
    if extra:
        marks.append({"id": "launch", "name": "Launch", "shape": SHAPES[1],
                      "colour": COLOURS[1]})
    path.write_text(json.dumps({"version": 1, "marks": marks}, indent=2,
                               ensure_ascii=False), encoding="utf-8")


def _loaded(tmp_path, kind: str):
    """A directory loaded from one valid entry: (path, directory, the live dict)."""
    if kind == "people":
        path = tmp_path / PEOPLE_NAME
        _seed_people(path)
        directory = app_module.Directory.load(path)
        return path, directory, directory.people
    path = tmp_path / MARKS_NAME
    _seed_marks(path)
    directory = marks_module.Directory.load(path)
    return path, directory, directory.marks


# --------------------------------------------------------------------------- #
# TC-2701 — the mtime/size gate, per directory (LLR-2706.1/2706.2)
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("kind", ["people", "marks"])
def test_TC_2701_refresh_gates_on_mtime_or_size(tmp_path, monkeypatch, kind):
    """LLR-2706.1/2706.2: an unchanged file is not re-parsed (the same live dict,
    zero parses); an mtime move with the size kept re-parses exactly once and the
    edit shows; a size move with the mtime frozen re-parses too (the gate's size
    arm). RED: the size arm dropped → the third refresh stays None."""
    path, directory, live = _loaded(tmp_path, kind)
    real_read = type(directory)._read
    calls = {"n": 0}

    def spy(p):
        calls["n"] += 1
        return real_read(p)

    monkeypatch.setattr(type(directory), "_read", staticmethod(spy))

    assert directory.refresh() is None
    assert calls["n"] == 0                         # unchanged: no parse, the dict untouched

    stat = path.stat()                             # (b) the same size, the mtime moves
    data = json.loads(path.read_text(encoding="utf-8"))
    if kind == "people":
        data["people"][0]["name"] = "Eva One"      # an equal-length edit in place
    else:
        data["marks"][0]["colour"] = "pink"
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    assert path.stat().st_size == stat.st_size
    os.utime(path, ns=(stat.st_atime_ns, stat.st_mtime_ns + 10_000_000))
    assert directory.refresh() is True
    assert calls["n"] == 1
    if kind == "people":
        assert live["ada.one"].name == "Eva One"
    else:
        assert live["basics"].colour == "pink"

    stamp_mtime, stamp_size = directory._stamp     # (c) the size moves, the mtime frozen
    if kind == "people":
        _seed_people(path, extra=True)
    else:
        _seed_marks(path, extra=True)
    os.utime(path, ns=(path.stat().st_atime_ns, stamp_mtime))
    assert path.stat().st_mtime_ns == stamp_mtime
    assert path.stat().st_size != stamp_size
    assert directory.refresh() is True
    assert calls["n"] == 2
    assert ("zoe.quill" if kind == "people" else "launch") in live


# --------------------------------------------------------------------------- #
# TC-2702 — a failed re-read keeps the directory and flags once (LLR-2707.1)
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("kind", ["people", "marks"])
def test_TC_2702_a_failed_refresh_keeps_and_flags_once(tmp_path, kind):
    """LLR-2707.1: a re-read of an unparseable file returns False and keeps every
    in-memory entry; the stamp advances, so the still-bad file is not re-parsed
    on the next refresh; a fixed file reloads. RED: True on failure inverts the
    flag arm; clearing the dict on failure inverts the keep arm."""
    path, directory, live = _loaded(tmp_path, kind)
    held = next(iter(live))
    stat = path.stat()
    path.write_bytes(b"\x00\x01 not json at all")
    os.utime(path, ns=(stat.st_atime_ns, stat.st_mtime_ns + 10_000_000))
    assert directory.refresh() is False
    assert list(live) == [held]                    # the failure keeps the directory
    assert directory.refresh() is None             # the stamp advanced: no re-parse, no re-flag
    if kind == "people":
        _seed_people(path, extra=True)
    else:
        _seed_marks(path, extra=True)
    os.utime(path, ns=(path.stat().st_atime_ns, stat.st_mtime_ns + 20_000_000))
    assert directory.refresh() is True
    assert set(live) == ({"ada.one", "zoe.quill"} if kind == "people"
                         else {"basics", "launch"})


# --------------------------------------------------------------------------- #
# AT-2706 — the other window's entries appear at every seat (HLR-2706)
# --------------------------------------------------------------------------- #
async def test_AT_2706_the_directories_stay_fresh(home):
    """AT-2706 (US-2702): with the app open on the home, a second `Directory`
    instance (the other window) appends a person and a class; `@` names the new
    person, `#` names the new class, the editor's `alt+m` Select offers the new
    class, and the `/` `@…` completion names the new person — no restart."""
    _two_boards(home)
    _seed_people(home / PEOPLE_NAME)
    _seed_marks(home / MARKS_NAME)
    app = _open(None)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        assert type(app.screen).__name__ == "BoardsHome"
        app_module.Directory.load(home / PEOPLE_NAME).add("Zoe Quill")
        marks_module.Directory.load(home / MARKS_NAME).add("Launch", SHAPES[1], COLOURS[1])
        await _press(pilot, "at")
        assert "Zoe Quill" in await screen_text(pilot, 118, 30)
        await _press(pilot, "escape")              # back to the home
        await _press(pilot, "number_sign")
        assert "Launch" in await screen_text(pilot, 118, 30)
        await _press(pilot, "escape", "escape")    # the home → the board (the start runs)
        app.selected_task_id = app.board.tasks[0].id
        app.refresh_view()
        await pilot.pause()
        await _press(pilot, "e")
        assert type(app.screen).__name__ == "TaskModal"
        opts = [p for p, _v in app.screen.query_one("#f-mark", Select)._options]
        assert any("Launch" in o.plain for o in opts)
        await _press(pilot, "escape")              # the editor cancels
        await _press(pilot, "4", "slash", "at", "z", "o")
        assert type(app.screen).__name__ == "SearchPrompt"
        text = await screen_text(pilot, 118, 30)
        assert "PEOPLE · names only" in text and "Zoe Quill" in text
        await _press(pilot, "escape")


# --------------------------------------------------------------------------- #
# AT-2707 — an unreadable re-read keeps the directory (HLR-2707)
# --------------------------------------------------------------------------- #
async def test_AT_2707_a_failed_re_read_keeps_the_directory(home):
    """AT-2707 (US-2702): after the mount loaded a person, the other window's bad
    write replaces people.json; `@` keeps the directory and says so once — one
    warning titled People, markup off — and reopening `@` on the still-bad file
    adds no second notice."""
    _two_boards(home)
    _seed_people(home / PEOPLE_NAME)
    app = _open(None)
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.pause()
        (home / PEOPLE_NAME).write_bytes(b"\x00\x01 not json at all")
        await _press(pilot, "at")
        notes = [n for n in app._notifications if n.title == "People"]
        assert len(notes) == 1
        assert notes[0].severity == "warning" and notes[0].markup is False
        assert "could not be read" in str(notes[0].message)
        assert "Ada One" in await screen_text(pilot, 118, 30)
        await _press(pilot, "escape")
        await _press(pilot, "at")                  # the file is still bad
        assert len([n for n in app._notifications if n.title == "People"]) == 1
        assert "Ada One" in await screen_text(pilot, 118, 30)
        await _press(pilot, "escape")


# --------------------------------------------------------------------------- #
# PDR #D3 — the `/` seat fires the re-read once, the first time the query names
# the directories (an initial `@`/`#` query included)
# --------------------------------------------------------------------------- #
async def test_D3_the_search_query_refreshes_the_directories_once(home):
    """PDR #D3 / LLR-2706.3: an initial query that already names the directories
    fires the callback before the first frame; however often the query later
    names them, it fires once; a text query never fires. RED: the callback
    dropped from `on_mount` → the initial arm inverts."""
    _two_boards(home)
    app = _open(None)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        calls = []
        app.push_screen(modals.SearchPrompt(
            "Filter tasks", initial="@x", people=app.people,
            open_person=lambda h: None, on_directory_query=lambda: calls.append(1)))
        await pilot.pause()
        assert calls == [1]
        box = app.screen.query_one("#f-text", Input)
        box.value = "#y"
        await pilot.pause()
        box.value = "@z"
        await pilot.pause()
        assert calls == [1]                        # once, however often the query names them
        await _press(pilot, "escape")
        app.push_screen(modals.SearchPrompt(
            "Filter tasks", initial="plain", people=app.people,
            open_person=lambda h: None, on_directory_query=lambda: calls.append(1)))
        await pilot.pause()
        assert calls == [1]                        # a text query names no directory
        await _press(pilot, "escape")
