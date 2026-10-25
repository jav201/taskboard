"""The home at start defers the board's start (batch 2026-10-24-batch-02, HD-1..HD-4).

HLR-2701..HLR-2705 / LLR-2701.1, LLR-2701.2, LLR-2702.1..LLR-2702.4, LLR-2703.1,
LLR-2704.1, LLR-2705.1 · AT-2701..AT-2705 · TC-2703 (US-2701). The multi-board
round's boards (`tests/multi_board_fixture.py`), trimmed to two, under this test's
own temporary home; a foreign window is a planted presence marker, synthetic data only.
"""
from __future__ import annotations

import json
from datetime import date, datetime, timedelta
from pathlib import Path
from types import SimpleNamespace

import pytest

import multi_board_fixture as mb
from taskboard import app as app_module
from taskboard import boards
from taskboard.app import BoardsHome
from taskboard.models import Board, Task
from taskboard.modals import MilestoneOffer

NOW = datetime(2026, 10, 20, 9, 30)
OPEN_TWICE = "Boards · open twice"


class _Today(date):
    @classmethod
    def today(cls):
        return mb.TODAY


class _Now(datetime):
    @classmethod
    def now(cls, tz=None):
        return NOW


@pytest.fixture
def home(tmp_path, monkeypatch):
    """`Path.home()` → this test's folder; the calendar and the clock frozen at
    every module that reads them (the house pattern of tests/test_boards_home.py)."""
    from taskboard import models, views
    import taskboard.__main__ as entry
    from taskboard import modals
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
    for mod in (app_module, models, views, modals):
        monkeypatch.setattr(mod, "date", _Today)
    monkeypatch.setattr(app_module, "datetime", _Now)
    monkeypatch.setattr(entry, "datetime", _Now)
    return tmp_path / ".taskboard"


def _open(board=None, unlisted=None):
    from taskboard.__main__ import open_app
    return open_app(board, unlisted)


async def _press(pilot, *keys):
    for k in keys:
        await pilot.press(k)
        await pilot.pause()


def _two_boards(home) -> None:
    """The round's registry trimmed to the default `personal` and the second board."""
    reg_path = mb.build(home, "personal")
    reg = json.loads(reg_path.read_text(encoding="utf-8"))
    reg["boards"] = [e for e in reg["boards"]
                     if e["id"] in ("personal", "client-retail-rag")]
    reg_path.write_text(json.dumps(reg), encoding="utf-8")


def _plant_sweepable(path: Path) -> None:
    """A Done task finished 40 days ago: the start's sweep archives it (the age
    gate is AUTO_ARCHIVE_DAYS = 20)."""
    b = Board.load(path)
    b.tasks.append(Task("Old done task", project_id=b.projects[0].id, phase="Done",
                        phase_changed=(mb.TODAY - timedelta(days=40)).isoformat(),
                        id="t-old"))
    b.save()


def _markers_for(path: Path) -> list[str]:
    d = boards.presence_dir()
    stem = boards._presence_stem(path)
    if not d.is_dir():
        return []
    return sorted(p.name for p in d.iterdir() if p.name.startswith(stem + "-"))


# --------------------------------------------------------------------------- #
# AT-2701 — the home at start touches nothing (HLR-2701, LLR-2701.1/2701.2)
# --------------------------------------------------------------------------- #
async def test_AT_2701_the_home_touches_nothing(home):
    """AT-2701 (US-2701): with a foreign marker planted and a sweepable done task
    on the default board, the start home shows — no open-twice notice, no marker of
    this window, the default board's bytes untouched; and `q` from the home quits
    with nothing written (LLR-2701.2)."""
    _two_boards(home)
    default = mb.board_path(home, "personal")
    _plant_sweepable(default)
    foreign = boards.announce(default, NOW)
    before = default.read_bytes()
    app = _open(None)
    try:
        async with app.run_test(size=(118, 30), notifications=True) as pilot:
            await pilot.pause()
            assert type(app.screen).__name__ == "BoardsHome"
            assert not [n for n in app._notifications if n.title == OPEN_TWICE]
            assert [m for m in _markers_for(default) if m != foreign.name] == []
            assert default.read_bytes() == before
            await pilot.press("q")               # LLR-2701.2: quit from the home
        assert [m for m in _markers_for(default) if m != foreign.name] == []
        assert default.read_bytes() == before
    finally:
        boards.withdraw(foreign)


# --------------------------------------------------------------------------- #
# AT-2702 — enter on the default card runs the deferred start (HLR-2702/2705)
# --------------------------------------------------------------------------- #
async def test_AT_2702_enter_runs_the_deferred_start(home):
    """AT-2702 (US-2701): `enter` on the default card — the cursor starts on it —
    runs the deferred start exactly once: the pinned open-twice notice, this
    window's marker, the sweepable task archived; a later `B`, `esc` round trip
    adds no second notice, no second marker and no second write; and the agenda
    jump onto the deferred board (`A`, `enter`) is a fifth path that starts it
    too (LLR-2702.1/2702.3, code review F1)."""
    _two_boards(home)
    default = mb.board_path(home, "personal")
    _plant_sweepable(default)
    foreign = boards.announce(default, NOW)
    before = default.read_bytes()
    app = _open(None)
    try:
        async with app.run_test(size=(118, 30), notifications=True) as pilot:
            await pilot.pause()
            assert type(app.screen).__name__ == "BoardsHome"
            await _press(pilot, "enter")
            twice = [n for n in app._notifications if n.title == OPEN_TWICE]
            assert len(twice) == 1
            assert twice[0].message == (
                "Personal is already open in another taskboard window (since 09:30). "
                "Both save the same file: the last save wins. Close one of them.")
            assert len(_markers_for(default)) == 2     # the foreign marker and this window's
            assert Board.load(default).task_by_id("t-old").archived
            after = default.read_bytes()
            assert after != before                    # the sweep saved the archive
            assert app._started_board == "personal"
            await _press(pilot, "B", "escape")
            assert len([n for n in app._notifications if n.title == OPEN_TWICE]) == 1
            assert len(_markers_for(default)) == 2
            assert default.read_bytes() == after      # the round trip re-ran nothing
    finally:
        boards.withdraw(foreign)
    # the fifth path (code review F1 of increment 001): `A` from the home, `enter`
    # on a task of the deferred board jumps onto it — the pending start runs there
    # too, exactly once (LLR-2702.3's seam, shared with the people view's jump)
    foreign2 = boards.announce(default, NOW)
    app = _open(None)
    try:
        async with app.run_test(size=(118, 30), notifications=True) as pilot:
            await pilot.pause()
            assert type(app.screen).__name__ == "BoardsHome"
            await _press(pilot, "A", "enter")
            assert len(app.screen_stack) == 1          # the agenda left with the home
            assert app.board_id == "personal"
            assert len([n for n in app._notifications if n.title == OPEN_TWICE]) == 1
            assert len(_markers_for(default)) == 2     # the foreign marker and this window's
            assert app._started_board == "personal"
            await _press(pilot, "B", "escape")
            assert len([n for n in app._notifications if n.title == OPEN_TWICE]) == 1
            assert len(_markers_for(default)) == 2
    finally:
        boards.withdraw(foreign2)


# --------------------------------------------------------------------------- #
# AT-2703 — esc runs the start once; the --open sentinel (HLR-2702, PDR C2)
# --------------------------------------------------------------------------- #
async def test_AT_2703_escape_runs_the_start_once(home):
    """AT-2703 (US-2701): `esc` from the home runs the deferred start exactly once;
    `B` then `esc` later re-runs nothing. The unlisted arm (PDR C2): an `--open`
    board's record is its own `unlisted:` sentinel — the mount start ran with no
    home (HD-4), and `B`'s home pops back over it without re-running anything."""
    _two_boards(home)
    default = mb.board_path(home, "personal")
    foreign = boards.announce(default, NOW)
    app = _open(None)
    try:
        async with app.run_test(size=(118, 30), notifications=True) as pilot:
            await pilot.pause()
            await _press(pilot, "escape")
            assert len([n for n in app._notifications if n.title == OPEN_TWICE]) == 1
            assert len(_markers_for(default)) == 2
            assert app._started_board == "personal"
            after = default.read_bytes()
            await _press(pilot, "B", "escape")
            assert len([n for n in app._notifications if n.title == OPEN_TWICE]) == 1
            assert len(_markers_for(default)) == 2
            assert default.read_bytes() == after
    finally:
        boards.withdraw(foreign)
    side = home.parent / "side" / "notes.json"
    side.parent.mkdir(parents=True, exist_ok=True)
    Board([], [], side, json.loads(json.dumps(mb.SETTINGS))).save()
    app = _open(None, unlisted=str(side))
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.pause()
        assert type(app.screen).__name__ == "Screen"    # --open: no home (HD-4)
        assert app._started_key() == f"unlisted:{app.board.path}"
        assert app._started_board == app._started_key()   # the mount start ran
        assert len(_markers_for(app.board.path)) == 1     # its own marker, from the mount
        await _press(pilot, "B")
        assert type(app.screen).__name__ == "BoardsHome"
        await _press(pilot, "escape")
        assert type(app.screen).__name__ == "Screen"
        assert len(_markers_for(app.board.path)) == 1     # nothing re-ran


# --------------------------------------------------------------------------- #
# AT-2704 — another board never writes the default (HLR-2703, LLR-2703.1)
# --------------------------------------------------------------------------- #
async def test_AT_2704_another_board_never_writes_the_default(home):
    """AT-2704 (US-2701): `enter` on the second board's card starts that board — its
    marker appears — while the default board, sweepable and foreign-marked but never
    started, is left byte-identical with its old done task un-archived."""
    _two_boards(home)
    default = mb.board_path(home, "personal")
    _plant_sweepable(default)
    foreign = boards.announce(default, NOW)
    before = default.read_bytes()
    app = _open(None)
    try:
        async with app.run_test(size=(118, 30), notifications=True) as pilot:
            await pilot.pause()
            await _press(pilot, "right", "enter")     # the Client · Retail RAG card
            assert app.board_id == "client-retail-rag"
            assert len(_markers_for(mb.board_path(home, "client-retail-rag"))) == 1
            assert default.read_bytes() == before
            assert Board.load(default).task_by_id("t-old").archived is False
    finally:
        boards.withdraw(foreign)


# --------------------------------------------------------------------------- #
# AT-2705 — the offer opens over the board (HLR-2704, LLR-2704.1)
# --------------------------------------------------------------------------- #
@pytest.mark.milestone_offer
async def test_AT_2705_the_offer_opens_over_the_board(home):
    """AT-2705 (US-2701): with the home up, a default board holding an unmarked
    milestone candidate opens no offer; leaving the home pushes the offer over the
    board — the home is not on the stack beneath it."""
    _two_boards(home)
    default = mb.board_path(home, "personal")
    data = json.loads(default.read_text(encoding="utf-8"))
    del data["settings"]["migrations"]["milestones"]
    default.write_text(json.dumps(data), encoding="utf-8")
    app = _open(None)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        assert type(app.screen).__name__ == "BoardsHome"
        assert not any(isinstance(sc, MilestoneOffer) for sc in app.screen_stack)
        await _press(pilot, "escape")
        assert type(app.screen).__name__ == "MilestoneOffer"
        assert not any(isinstance(sc, BoardsHome) for sc in app.screen_stack)
        assert type(app.screen_stack[0]).__name__ == "Screen"


# --------------------------------------------------------------------------- #
# TC-2703 — a failed deferred start keeps the board pending (LLR-2702.1/2702.4)
# --------------------------------------------------------------------------- #
async def test_TC_2703_a_failed_deferred_start_keeps_the_board_pending(home,
                                                                       monkeypatch):
    """TC-2703: a migration failure on the deferred start leaves the record
    unwritten, pops the home onto the board view and lets the migration's own
    notice explain; `B`, `esc` then retries the start from the migration — exactly
    once (the record names the board only on a completed start)."""
    _two_boards(home)
    default = mb.board_path(home, "personal")
    real = app_module.run_link_migration
    state = {"failed": False}

    def flaky(board):
        if not state["failed"]:
            state["failed"] = True
            return SimpleNamespace(error="disk full")
        return real(board)

    monkeypatch.setattr(app_module, "run_link_migration", flaky)
    app = _open(None)
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.pause()
        calls = []
        real_open = app._open_board

        def spy(at_mount=False):
            calls.append(at_mount)
            return real_open(at_mount=at_mount)

        app._open_board = spy
        await _press(pilot, "escape")
        fails = [n for n in app._notifications
                 if n.title == "Boards" and "link migration stopped" in str(n.message)]
        assert len(fails) == 1 and fails[0].severity == "error"
        assert app._started_board is None                  # the record stays pending
        assert type(app.screen).__name__ == "Screen"       # the home popped; the board beneath
        assert calls == [False]
        await _press(pilot, "B", "escape")                 # the retry
        assert calls == [False, False]
        assert app._started_board == "personal"
        assert len(_markers_for(default)) == 1             # the retry's start announced it
