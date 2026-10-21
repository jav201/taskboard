"""The agenda of every board (`A`).

Batch 2026-10-20-batch-03: HLR-2401 / LLR-2401.1, LLR-2401.2 · TC-2401 · AT-2401
(US-2401) — the round's item 1, variant C: a lane per board, a dot per due in each bucket
(`LATE`, `TODAY`, each day to Sunday), the chosen bucket's tasks; `enter` opens a task on
its board. The round's boards (`backlog_round_fixture`), synthetic, under this test's own
home; the calendar frozen on Tuesday 2026-10-20.
"""
from __future__ import annotations

from datetime import date, datetime
from pathlib import Path

import pytest

import backlog_round_fixture as fx
from taskboard import app as app_module, models, modals, views
from taskboard.app import BoardsHome, PresentScreen, TaskboardApp
from taskboard.boards import peek_board
from taskboard.models import Task
from test_modal_keys import _svg_rows

NOW = datetime(2026, 10, 20, 9, 30)


class _Today(date):
    @classmethod
    def today(cls):
        return fx.TODAY


class _Now(datetime):
    @classmethod
    def now(cls, tz=None):
        return NOW


@pytest.fixture
def home(tmp_path, monkeypatch):
    import taskboard.__main__ as entry
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
    for mod in (app_module, models, views, modals):
        monkeypatch.setattr(mod, "date", _Today)
    monkeypatch.setattr(app_module, "datetime", _Now)
    monkeypatch.setattr(entry, "datetime", _Now)
    return tmp_path / ".taskboard"


def _lanes(root):
    out = []
    for bid, name, colour, _rel, _h in fx.BOARDS:
        out.append((name, colour, peek_board(fx.board_path(root, bid)), ""))
    return out


async def _press(pilot, *keys):
    for k in keys:
        await pilot.press(k)
        await pilot.pause()


async def _rows(pilot, w, h) -> list[str]:
    await pilot.pause(0.5)
    return _svg_rows(pilot.app.export_screenshot(), w, h)


def _on_agenda(app) -> bool:
    return type(app.screen).__name__ == "AllBoardsAgenda"


def _open():
    from taskboard.__main__ import open_app
    return open_app(None)


# --------------------------------------------------------------------------- #
# TC-2401 — the pure render (LLR-2401.1)
# --------------------------------------------------------------------------- #
def test_TC_2401_buckets_and_dues(tmp_path):
    """TC-2401: seven buckets to Sunday 25 (two on a Sunday); 3 late, 2 today, 8 to
    Sunday, ordered by due then lane; no done, archived or later task."""
    b = views.agenda_buckets(fx.TODAY)
    assert [lab for _k, lab in b] == ["LATE", "TODAY", "Wed 21", "Thu 22", "Fri 23", "Sat 24",
                                      "Sun 25"]
    assert [lab for _k, lab in views.agenda_buckets(date(2026, 10, 25))] == ["LATE", "TODAY"]
    fx.build(tmp_path)
    items = views.all_agenda(_lanes(tmp_path), fx.TODAY)
    late = [x for x in items if x.bucket == "late"]
    today = [x for x in items if x.bucket == fx.TODAY]
    assert (len(late), len(today), len(items) - len(late) - len(today)) == (3, 2, 8)
    assert [x.task.title for x in today] == ["Week 3 plan", "Golden question set"]
    assert all(x.due <= date(2026, 10, 25) for x in items)
    titles = {x.task.title for x in items}
    assert "Parse catalog PDFs" not in titles and "10k race" not in titles   # done; later


@pytest.mark.parametrize("width", [118, 80])
def test_TC_2401_every_row_is_the_width_and_board_text_is_literal(tmp_path, width):
    """TC-2401: every rendered row is exactly the width; the project column only from
    100 cells; a markup-looking title printed as typed; a missing board's lane dimmed
    with its state from 100 cells; `1 board`, `1 due` singular."""
    fx.build(tmp_path)
    lanes = _lanes(tmp_path)
    lanes[0][2].tasks.append(Task("[b]x[/b]", phase="Doing", due_date="2026-10-20", id="tz"))
    lanes.append(("Gone", "pink", None, "file missing"))
    items = views.all_agenda(lanes, fx.TODAY)
    text = views.render_all_agenda(lanes, items, 1, 0, fx.TODAY, width, 30)
    rows = text.plain.split("\n")
    assert all(views.cell_len(r) == width for r in rows), [views.cell_len(r) for r in rows]
    assert "[b]x[/b]" in text.plain
    assert ("Fitness block" in text.plain) is (width >= 100)
    gone = next(r for r in rows if "Gone" in r)
    assert ("file missing" in gone) is (width >= 100) and "●" not in gone
    one = views.render_all_agenda(lanes[:1], views.all_agenda(lanes[:1], fx.TODAY), 2, 0,
                                  fx.TODAY, width, 30).plain
    assert "1 board · read-only" in one and "WED 21 · 1 due across 1 board" in one


# --------------------------------------------------------------------------- #
# TC-2401 — the screen and `A` (LLR-2401.2)
# --------------------------------------------------------------------------- #
async def test_TC_2401_where_A_acts_and_what_it_holds(home):
    """TC-2401 (app): `A` does nothing over a confirmation or the presentation; on the
    home it opens over it; with the agenda open the main screen's keys do nothing;
    `enter` on a task whose board file is gone says so and keeps the open board; `A`
    closes the agenda."""
    fx.build(home, last="client-a")
    app = _open()
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.pause()
        assert isinstance(app.screen, BoardsHome)
        await _press(pilot, "A")
        assert _on_agenda(app) and len(app.screen_stack) == 3
        await _press(pilot, "A")
        assert isinstance(app.screen, BoardsHome)
        await _press(pilot, "escape", "A")              # from the main screen, the home gone
        assert _on_agenda(app) and len(app.screen_stack) == 2
        tasks = len(app.board.tasks)
        await _press(pilot, "a", "d", "1", "B", "x")
        assert _on_agenda(app) and len(app.board.tasks) == tasks
        await _press(pilot, "escape")
        app.push_screen(modals.ConfirmModal("Delete 'x'?"))
        await pilot.pause()
        await _press(pilot, "A")
        assert type(app.screen).__name__ == "ConfirmModal"
        await _press(pilot, "n", "R")
        assert isinstance(app.screen, PresentScreen)
        await _press(pilot, "A")
        assert isinstance(app.screen, PresentScreen)
        await _press(pilot, "escape", "A")
        assert _on_agenda(app)
        fx.board_path(home, "main").unlink()
        await _press(pilot, "enter")          # Week 3 plan, on Personal — whose file is gone
        assert app.board_id == "client-a"
        assert any("its file is missing" in str(n.message) for n in app._notifications)
        assert not _on_agenda(app) and len(app.screen_stack) == 1    # nothing left open over it


async def test_TC_2401_the_unlisted_board_is_the_last_lane(home):
    """TC-2401 (app, LLR-2401.2): a board opened with `--open` is the agenda's last
    lane, under its chip's name; `enter` on its due opens it there, with no switch."""
    fx.build(home, last="client-a")
    loose = home.parent / "loose.json"
    loose.write_bytes(fx.board_path(home, "main").read_bytes())
    from taskboard.__main__ import open_app
    app = open_app(None, unlisted=str(loose))
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        assert app.board_id is None
        await _press(pilot, "A")
        agenda = app.screen
        assert agenda.lanes[-1][0] == "loose · not listed" and agenda.ids[-1] is None
        rows = await _rows(pilot, 118, 30)
        assert rows[6].strip(" ▌").startswith("loose"), rows[3:7]     # the lane column cuts the name
        chosen = agenda._chosen()
        mine = next(i for i, x in enumerate(chosen) if x.lane == len(agenda.lanes) - 1)
        await _press(pilot, *["down"] * mine, "enter")
        assert not _on_agenda(app) and len(app.screen_stack) == 1
        assert app.board_id is None and app.board.path == loose
        assert app.selected_task.title == chosen[mine].task.title


# --------------------------------------------------------------------------- #
# AT-2401 — through the shipped surface (US-2401)
# --------------------------------------------------------------------------- #
async def test_AT_2401_one_screen_for_every_board(home):
    """AT-2401 (US-2401): `A` on the home shows every board's week — the lanes in the
    registry's order, today's two dues — `enter` opens `Week 3 plan` on Personal; `A`,
    `down`, `enter` opens `Golden question set` on Client A; the board files keep their
    bytes; at 80×24 the home names `A all boards` and keeps `q` (the round's capture), and the agenda keeps
    every key."""
    fx.build(home, last="client-a")
    files = {bid: fx.board_path(home, bid).read_bytes() for bid, *_ in fx.BOARDS}
    app = _open()
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        await _press(pilot, "A")
        rows = await _rows(pilot, 118, 30)
        text = "\n".join(rows)
        for want in ("◆ ALL BOARDS", "3 boards · read-only", "▲3 late · 2 today · 8 to Sun 25",
                     "LATE", "▼ TODAY", "Wed 21", "Sun 25", "TODAY · 2 due across 2 boards"):
            assert want in text, want
        assert rows[29].rstrip().endswith("· read-only: nothing here edits a task"), rows[29]
        lanes = [r.strip(" ▌").split()[0] for r in rows[3:6]]
        assert lanes == ["Personal", "Client", "Course"], rows[3:6]
        assert text.index("Week 3 plan") < text.index("Golden question set")
        await _press(pilot, "enter")
        assert not (_on_agenda(app) or isinstance(app.screen, BoardsHome))
        head = (await _rows(pilot, 118, 30))[0]
        assert head.startswith(" Personal "), head
        assert app.selected_task.title == "Week 3 plan"
        await _press(pilot, "A", "down", "enter")
        head = (await _rows(pilot, 118, 30))[0]
        assert head.startswith(" Client A "), head
        assert app.selected_task.title == "Golden question set"
    for bid, data in files.items():
        assert fx.board_path(home, bid).read_bytes() == data, bid
    app = _open()
    async with app.run_test(size=(80, 24)) as pilot:
        await pilot.pause()
        keys = (await _rows(pilot, 80, 24))[23]
        assert keys.rstrip().endswith("A all boards  esc back  q"), keys    # the round C capture at 80
        await _press(pilot, "A")
        rows = await _rows(pilot, 80, 24)
        for k in ("←→", "↑↓", "↵", "esc"):
            assert k in rows[23], rows[23]
        assert "read-only" not in rows[23] and not rows[23].rstrip().endswith("·"), rows[23]   # the tail went whole
        assert "Fitness block" not in "\n".join(rows)
        assert "Week 3 plan" in "\n".join(rows)
