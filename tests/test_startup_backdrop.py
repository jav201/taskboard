"""The board shows behind the start-up modals (batch 2026-10-25-batch-01, D-12).

HLR-2801..HLR-2804 / LLR-2801.1..LLR-2803.1 · AT-2801..AT-2803 · TC-2801 (US-001).
The cause was the missing `#0007` backdrop on the two start-up modal screens
(taskboard.tcss; the `Screen { background: #0d1117 }` rule painted them opaque) —
the fix is one background-only declaration; no timing change (LLR-2801.2). The
oracle is the composited full screen-stack render (the `App.export_screenshot`
source); every node asserts its modal is the top screen and locates the box's
title row BEFORE counting rows outside the box — a missing modal or an unlocated
box fails the node, never a vacuous 0-count pass (the §5.1 vacuity guard).
Synthetic data only.
"""
from __future__ import annotations

import io
import json
from datetime import date, datetime
from pathlib import Path

import pytest
from rich.console import Console

import kg_board
import multi_board_fixture as mb
from taskboard.app import TaskboardApp
from taskboard.modals import MilestoneOffer, TeamIdentityPicker
from taskboard.models import Board

pytestmark = pytest.mark.milestone_offer

RENUMBER = "seen_view_renumber_2026_07"
SIZES = [(118, 30), (80, 24)]
OFFER_TITLE = "convert one-day tasks"


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
    from taskboard import app as app_module
    from taskboard import models, views
    from taskboard import modals
    import taskboard.__main__ as entry
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
    for mod in (app_module, models, views, modals):
        monkeypatch.setattr(mod, "date", _Today)
    monkeypatch.setattr(app_module, "datetime", _Now)
    monkeypatch.setattr(entry, "datetime", _Now)
    return tmp_path / ".taskboard"


def _strips(app) -> list[str]:
    """The composited full screen stack as text rows (what a terminal shows)."""
    render = app.screen._compositor.render_update(
        full=True, screen_stack=app._background_screens)
    console = Console(width=app.size.width, height=app.size.height,
                      file=io.StringIO(), force_terminal=True,
                      color_system="truecolor", record=True,
                      legacy_windows=False, safe_box=False)
    console.print(render)
    return console.export_text().splitlines()


def _box(rows: list[str], title: str) -> tuple[int, int]:
    """(top border row, bottom border row) of the bordered box holding `title`.

    The corners are located by glyph, not by whole-row shape: with the dimmed
    backdrop the rows flanking the box carry board text beside the border.
    Fails (never returns a vacuous count) when the title row or the corners
    are absent from the render."""
    hits = [i for i, r in enumerate(rows) if title in r]
    assert hits, f"box title {title!r} not found in the render"
    t = hits[0]
    top = next((i for i in range(t, -1, -1) if "╭" in rows[i]), None)
    bottom = next((i for i in range(t + 1, len(rows)) if "╰" in rows[i]), None)
    assert top is not None and bottom is not None, \
        f"box borders around {title!r} not found (top={top}, bottom={bottom})"
    return top, bottom


def _rows_outside(rows: list[str], title: str) -> tuple[int, int]:
    """Non-blank rows above the box's top border and below its bottom border."""
    top, bottom = _box(rows, title)
    above = sum(1 for r in rows[:top] if r.strip())
    below = sum(1 for r in rows[bottom + 1:] if r.strip())
    return above, below


def _offer_board(path: Path) -> Path:
    """The kg board with 8 one-day candidates and the renumber key (no notice
    save mid-start; the house `_legacy` pattern)."""
    b = kg_board.one_day(kg_board.shifted(path), date.today())
    b.settings[RENUMBER] = True
    b.save()
    return path


def _team_dir(tmp_path: Path) -> Path:
    team = tmp_path / "team"
    team.mkdir()
    (team / "team.json").write_text(json.dumps(kg_board.TEAM), encoding="utf-8")
    return team


async def _await_offer(pilot, app):
    for _ in range(20):
        await pilot.pause()
        if isinstance(app.screen, MilestoneOffer):
            return
    raise AssertionError(f"MilestoneOffer never opened; top screen "
                         f"{type(app.screen).__name__}")


async def _await_picker(pilot, app):
    for _ in range(20):
        await pilot.pause()
        if isinstance(app.screen, TeamIdentityPicker):
            return
    raise AssertionError(f"TeamIdentityPicker never opened; top screen "
                         f"{type(app.screen).__name__}")


# --------------------------------------------------------------------------- #
# AT-2801 — the single-board start's offer shows the board behind it (HLR-2801)
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("size", SIZES)
async def test_AT_2801_the_offer_opens_over_the_painted_board(tmp_path, size):
    """AT-2801 (US-001): with candidates on a single-board start, the offer is
    the top screen and > 0 of the board's rows show outside the offer box at
    118x30 and 80x24. RED: the declaration deleted (opaque screen, 0 rows
    outside)."""
    path = _offer_board(tmp_path / "board.json")
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=size) as pilot:
        await _await_offer(pilot, app)
        assert isinstance(app.screen, MilestoneOffer)      # the vacuity guard
        above, below = _rows_outside(_strips(app), OFFER_TITLE)
        assert above + below > 0, f"{size}: no board rows outside the offer box"


# --------------------------------------------------------------------------- #
# AT-2802 — the home path's offer shows the chosen board (HLR-2802)
# --------------------------------------------------------------------------- #
def _two_boards(home) -> None:
    reg_path = mb.build(home, "personal")
    reg = json.loads(reg_path.read_text(encoding="utf-8"))
    reg["boards"] = [e for e in reg["boards"]
                     if e["id"] in ("personal", "client-retail-rag")]
    reg_path.write_text(json.dumps(reg), encoding="utf-8")


@pytest.mark.parametrize("size", SIZES)
async def test_AT_2802_enter_on_the_home_opens_the_offer_over_the_chosen_board(
        home, size):
    """AT-2802 (US-001): two boards, `enter` on the default card — the offer is
    the top screen over the chosen board (no `BoardsHome` beneath; the one
    white-box reach, by house precedent test_TC_616's stack assertion) and the
    board's rows show outside the box at both sizes. RED: the declaration
    deleted."""
    _two_boards(home)
    _offer_board(mb.board_path(home, "personal"))
    from taskboard.__main__ import open_app
    app = open_app(None)
    async with app.run_test(size=size) as pilot:
        await pilot.pause()
        assert type(app.screen).__name__ == "BoardsHome"
        await pilot.press("enter")
        await _await_offer(pilot, app)
        assert isinstance(app.screen, MilestoneOffer)      # the vacuity guard
        assert "BoardsHome" not in [type(s).__name__ for s in app.screen_stack]
        above, below = _rows_outside(_strips(app), OFFER_TITLE)
        assert above + below > 0, f"{size}: no board rows outside the offer box"


# --------------------------------------------------------------------------- #
# AT-2803 — team mode: the board behind both modals, today's order (HLR-2803)
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("size", SIZES)
async def test_AT_2803_team_mode_shows_the_board_behind_both_modals_in_todays_order(
        tmp_path, size):
    """AT-2803 (US-001, D-615): team-shared board with no identity — the picker
    opens first, the offer last (the stack tail), and the board's rows show
    outside the offer box at both sizes. RED: the declaration deleted; a
    recentered picker trips the geometry arm of the 118x30 node."""
    path = _offer_board(tmp_path / "board.json")
    b = Board.load(path)
    b.settings["team_shared_dir"] = str(_team_dir(tmp_path))
    b.save()
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=size) as pilot:
        await _await_offer(pilot, app)
        assert isinstance(app.screen, MilestoneOffer)      # the vacuity guard
        kinds = [type(s).__name__ for s in app.screen_stack]
        assert kinds[-2:] == ["TeamIdentityPicker", "MilestoneOffer"], kinds
        above, below = _rows_outside(_strips(app), OFFER_TITLE)
        assert above + below > 0, f"{size}: no board rows outside the offer box"


async def test_AT_2803_the_picker_keeps_its_pre_batch_geometry(tmp_path):
    """AT-2803's geometry arm (HLR-2803, PDR-2026-10-25-batch-01#D1): with the
    picker alone on screen (the offer mark pre-set, so no offer opens), the
    picker box sits at exactly its pre-batch geometry — row 0, columns 0-61
    (width 62), bottom border row 11 (12 rendered rows) at 118x30. RED: the A1
    shape (joining the shared rule) would centre the box and lose row 0."""
    path = tmp_path / "board.json"
    b = Board.load(path)            # a load seeds both marks: no offer
    b.settings["team_shared_dir"] = str(_team_dir(tmp_path))
    b.save()
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(118, 30)) as pilot:
        await _await_picker(pilot, app)
        assert isinstance(app.screen, TeamIdentityPicker)  # the vacuity guard
        rows = _strips(app)
        top = next(i for i, r in enumerate(rows) if "╭" in r)
        bottom = next(i for i in range(top, len(rows)) if "╰" in rows[i])
        left = rows[top].index("╭")
        right = rows[top].index("╮")
        assert (top, left, right, bottom) == (0, 0, 61, 11), \
            f"picker box moved: row {top}, cols {left}-{right}, bottom {bottom}"


# --------------------------------------------------------------------------- #
# AT-2804 — the unchanged start paths stay unchanged (HLR-2804, the pin)
# --------------------------------------------------------------------------- #
async def test_AT_2804_the_unchanged_start_paths_stay_unchanged(tmp_path):
    """AT-2804 (US-001, HLR-2804): a start that owes no start-up modal is
    byte-behaviour identical to before this batch — no modal opens, the board
    paints as today. (The rest of the pin is the P4 full suite: every existing
    offer/picker/home/team arm re-run there.)"""
    path = tmp_path / "board.json"
    b = Board.load(path)            # seeded marks: the offer never opens
    b.settings[RENUMBER] = True
    b.save()
    before = path.read_bytes()
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        assert type(app.screen).__name__ == "Screen"
        rows = _strips(app)
        assert sum(1 for r in rows if r.strip()) > 0, "the board did not paint"
    assert path.read_bytes() == before


# --------------------------------------------------------------------------- #
# TC-2801 — quitting with the picker open writes nothing (LLR-2801.3)
# --------------------------------------------------------------------------- #
def _snapshot(folder: Path) -> dict[str, bytes]:
    return {p.name: p.read_bytes() for p in sorted(folder.iterdir())}


async def test_TC_2801_quitting_with_the_picker_open_writes_nothing(tmp_path):
    """TC-2801 (LLR-2801.3): team-shared board with no identity; the picker
    opens and the run exits via the context exit (the TC-616 quit precedent — a
    keypress would reach the modal's `escape`, not quit). The board file bytes,
    the persisted settings (no `team_user_id`) and the team dir — snapshotted
    BEFORE the app starts — are all unchanged. A pin, not a gate: a stylesheet
    cannot change writes (C-40 corollary)."""
    team = _team_dir(tmp_path)
    team_before = _snapshot(team)
    path = tmp_path / "board.json"
    b = Board.load(path)            # seeded marks: no offer, picker alone
    b.settings["team_shared_dir"] = str(team)
    b.settings[RENUMBER] = True     # the renumber notice would write the key
    b.save()
    board_before = path.read_bytes()
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(118, 30)) as pilot:
        await _await_picker(pilot, app)
        assert isinstance(app.screen, TeamIdentityPicker)
    assert path.read_bytes() == board_before
    assert Board.load(path).settings.get("team_user_id") is None
    assert _snapshot(team) == team_before
