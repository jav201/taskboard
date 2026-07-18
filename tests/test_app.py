"""Pilot tests that prove the app actually works (assert rendered content)."""

from __future__ import annotations

from datetime import date

import pytest

from textual.widgets import Button, Footer, Input, Static, TextArea

from taskboard.app import BoardView, TaskboardApp
from taskboard.models import Board, Task
from taskboard.ribbon import Ribbon
from taskboard.views import render_agenda, render_gantt


def make_app(tmp_path) -> TaskboardApp:
    return TaskboardApp(board_path=str(tmp_path / "board.json"))


def board_text(app) -> str:
    """Plain-text render of the main board widget."""
    return str(app.query_one("#board", Static).render())


async def save_open_modal(app, pilot) -> None:
    app.screen.query_one("#save", Button).press()
    await pilot.pause()


# --------------------------------------------------------------------------- #
async def test_boots_and_seeds(tmp_path):
    app = make_app(tmp_path)
    async with app.run_test() as pilot:
        assert app.query_one("#board", Static) is not None
        # seeded demo data is present
        assert len(app.board.projects) > 0
        assert len(app.board.tasks) > 0
        assert "TASKBOARD" in board_text(app)


async def test_all_four_views_switch(tmp_path):
    app = make_app(tmp_path)
    async with app.run_test() as pilot:
        await pilot.press("1")
        assert "TASKBOARD" in board_text(app)   # swimlanes
        await pilot.press("2")
        assert "KANBAN" in board_text(app)       # columns
        await pilot.press("3")
        assert "AGENDA" in board_text(app)       # agenda
        await pilot.press("4")
        assert "GANTT" in board_text(app)        # gantt


async def test_add_task_modal_appears(tmp_path):
    app = make_app(tmp_path)
    async with app.run_test() as pilot:
        await pilot.press("a")
        await pilot.pause()
        app.screen.query_one("#f-title", Input).value = "ZZZTASK"
        await save_open_modal(app, pilot)
        assert any(t.title == "ZZZTASK" for t in app.board.tasks)
        await pilot.press("2")  # columns -> backlog has the new task
        assert "ZZZTASK" in board_text(app)


async def test_edit_task(tmp_path):
    app = make_app(tmp_path)
    async with app.run_test() as pilot:
        # add first so we have a known selected task
        await pilot.press("a")
        await pilot.pause()
        app.screen.query_one("#f-title", Input).value = "ORIGTASK"
        await save_open_modal(app, pilot)
        assert app.selected_task_id is not None
        await pilot.press("e")
        await pilot.pause()
        app.screen.query_one("#f-title", Input).value = "EDITEDTASK"
        await save_open_modal(app, pilot)
        assert any(t.title == "EDITEDTASK" for t in app.board.tasks)
        assert not any(t.title == "ORIGTASK" for t in app.board.tasks)


async def test_archive_and_show_archived_toggle(tmp_path):
    app = make_app(tmp_path)
    async with app.run_test() as pilot:
        await pilot.press("a")
        await pilot.pause()
        app.screen.query_one("#f-title", Input).value = "ARCHME"
        await save_open_modal(app, pilot)
        tid = next(t.id for t in app.board.tasks if t.title == "ARCHME")
        app.selected_task_id = tid
        await pilot.press("x")            # archive it
        assert app.board.task_by_id(tid).archived is True
        await pilot.press("2")
        assert "ARCHME" not in board_text(app)   # hidden by default
        await pilot.press("v")            # show archived (moved off 'h' -> vim-left)
        await pilot.press("2")
        assert "ARCHME" in board_text(app)       # now visible


async def test_add_project(tmp_path):
    app = make_app(tmp_path)
    async with app.run_test() as pilot:
        before = len(app.board.projects)
        await pilot.press("p")
        await pilot.pause()
        app.screen.query_one("#f-name", Input).value = "NEWPROJ"
        await save_open_modal(app, pilot)
        assert len(app.board.projects) == before + 1
        assert any(p.name == "NEWPROJ" for p in app.board.projects)


async def test_ribbon_shows_time_date_week_and_two_clocks(tmp_path):
    app = make_app(tmp_path)
    async with app.run_test() as pilot:
        ribbon = app.query_one("#ribbon", Ribbon)
        text = str(ribbon.render())
        # HH:MM:SS + week token + both DEFAULT clock cities (Mexico City / New York)
        assert ":" in text
        assert "W" in text
        assert "Mexico City" in text
        assert "New York" in text


async def test_clock_modal_search_pick_persists(tmp_path):
    board_path = str(tmp_path / "board.json")
    app = TaskboardApp(board_path=board_path)
    async with app.run_test() as pilot:
        assert app.board.get_clocks() == ("Mexico City", "New York")   # fresh defaults
        await pilot.press("c")
        await pilot.pause()
        # type-to-find: 'tokyo' resolves to the canonical 'Tokyo' city
        app.screen.query_one("#f-clock1", Input).value = "tokyo"
        app.screen.query_one("#save", Button).press()
        await pilot.pause()
        # (a) ribbon now shows the chosen city
        ribbon = app.query_one("#ribbon", Ribbon)
        assert "Tokyo" in str(ribbon.render())
        assert app.board.get_clocks()[0] == "Tokyo"
    # (b) persisted: reload the board file from disk, clock2 keeps its default
    reloaded = Board.load(board_path)
    assert reloaded.get_clocks() == ("Tokyo", "New York")


async def test_clock_modal_unknown_city_falls_back(tmp_path):
    app = make_app(tmp_path)
    async with app.run_test() as pilot:
        await pilot.press("c")
        await pilot.pause()
        app.screen.query_one("#f-clock1", Input).value = "Nowhereville"  # not a city
        app.screen.query_one("#save", Button).press()
        await pilot.pause()
        assert app.board.get_clocks()[0] == "Mexico City"   # kept current value


def test_city_clock_is_zoneinfo_dst_aware():
    from datetime import datetime, timezone
    from zoneinfo import ZoneInfo
    from taskboard.ribbon import clock_hhmm
    from taskboard.models import CITY_TO_ZONE
    utc = datetime(2026, 7, 17, 12, 0, tzinfo=timezone.utc)
    for city in ("Mexico City", "New York", "Tokyo", "London", "Mumbai"):
        expected = utc.astimezone(ZoneInfo(CITY_TO_ZONE[city])).strftime("%H:%M")
        assert clock_hhmm(CITY_TO_ZONE[city], utc) == expected
    # sanity: Tokyo (UTC+9) is 15h ahead of Mexico City (UTC-6, no DST in 2022+)
    mx = clock_hhmm(CITY_TO_ZONE["Mexico City"], utc)
    tk = clock_hhmm(CITY_TO_ZONE["Tokyo"], utc)
    assert mx == "06:00" and tk == "21:00"


def test_board_clock_settings_backcompat(tmp_path):
    import json
    # (1) no settings at all -> fresh city defaults
    p = tmp_path / "old.json"
    p.write_text(json.dumps({"projects": [], "tasks": []}), encoding="utf-8")
    assert Board.load(str(p)).get_clocks() == ("Mexico City", "New York")
    # (2) legacy fixed-offset abbreviations migrate to representative cities
    q = tmp_path / "legacy.json"
    q.write_text(json.dumps({"projects": [], "tasks": [],
                             "settings": {"clock1": "CST", "clock2": "EST"}}),
                 encoding="utf-8")
    assert Board.load(str(q)).get_clocks() == ("Mexico City", "New York")
    r = tmp_path / "legacy2.json"
    r.write_text(json.dumps({"projects": [], "tasks": [],
                             "settings": {"clock1": "JST", "clock2": "CET"}}),
                 encoding="utf-8")
    assert Board.load(str(r)).get_clocks() == ("Tokyo", "Madrid")


async def test_ribbon_is_painted_and_not_overlapping_footer(tmp_path):
    """Painted-region check (M22 C-32): a render-string test alone is a
    false-positive class — the ribbon can render text while being invisible."""
    app = make_app(tmp_path)
    async with app.run_test(size=(120, 35)) as pilot:
        await pilot.pause()
        ribbon = app.query_one("#ribbon", Ribbon)
        footer = app.query_one(Footer)
        # (a) the ribbon has a real content row to paint into
        assert ribbon.content_size.height >= 1
        # (b) ribbon and footer occupy DIFFERENT rows (no overlap)
        r, f = ribbon.region, footer.region
        assert r.height >= 1 and f.height >= 1
        assert (r.y + r.height <= f.y) or (f.y + f.height <= r.y)
        assert r.y < f.y   # ribbon sits ABOVE the footer


async def test_board_fills_viewport_width(tmp_path):
    app = make_app(tmp_path)
    async with app.run_test(size=(140, 40)) as pilot:
        await pilot.pause()
        board = app.query_one("#board", BoardView)
        vp = app.query_one("#viewport")
        # board content width tracks the viewport (fills, not stuck at 66)
        assert abs(board.content_size.width - vp.size.width) <= 4
        assert board.content_size.width >= 120   # definitely not the old 66


async def test_board_reflows_on_resize(tmp_path):
    app = make_app(tmp_path)
    async with app.run_test(size=(90, 30)) as pilot:
        await pilot.pause()
        board = app.query_one("#board", BoardView)
        first = board.content_size.width
        await pilot.resize_terminal(150, 40)
        await pilot.pause()
        second = board.content_size.width
        assert second > first                       # width tracked the resize
        assert abs(second - app.query_one("#viewport").size.width) <= 4


async def test_tiny_size_does_not_crash(tmp_path):
    app = make_app(tmp_path)
    async with app.run_test(size=(40, 12)) as pilot:
        await pilot.pause()
        for key in ("1", "2", "3", "4"):
            await pilot.press(key)          # every view renders at 40x12
        board = app.query_one("#board", BoardView)
        assert board.content_size.width > 0  # rendered something, no exception


async def test_columns_nav_follows_displayed_order_not_board_order(tmp_path):
    from taskboard.views import nav_model
    app = make_app(tmp_path)
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.pause()
        await pilot.press("2")   # columns
        cols = nav_model("columns", app.board, False)
        backlog = cols[0]
        board_order = [t.id for t in app.board.visible_tasks(False)]
        # the displayed column order differs from flat board order (the old bug)
        assert backlog != board_order[:len(backlog)]

        app.selected_task_id = backlog[0]
        app.refresh_view()
        visited = [app.selected_task_id]
        for _ in range(len(backlog) - 1):
            await pilot.press("down")
            visited.append(app.selected_task_id)
        # Down visits the BACKLOG column in its displayed order, exactly
        assert visited == backlog
        assert all(app.board.task_by_id(t).status == "backlog" for t in visited)
        # and render places them strictly top-to-bottom in that same order
        idxs = [app._line_map[t] for t in backlog if t in app._line_map]
        assert idxs == sorted(idxs)


async def test_right_moves_to_next_column_first_task(tmp_path):
    from taskboard.views import nav_model
    app = make_app(tmp_path)
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.pause()
        await pilot.press("2")
        cols = nav_model("columns", app.board, False)
        app.selected_task_id = cols[0][0]
        app.refresh_view()
        await pilot.press("right")
        assert app.selected_task_id == cols[1][0]   # ACTIVE column's first task
        await pilot.press("right")
        # BLOCKED has one task in seed; Right lands on its first task
        assert app.selected_task_id == cols[2][0]


async def test_up_at_top_of_column_is_noop(tmp_path):
    from taskboard.views import nav_model
    app = make_app(tmp_path)
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.pause()
        await pilot.press("2")
        cols = nav_model("columns", app.board, False)
        app.selected_task_id = cols[0][0]
        app.refresh_view()
        await pilot.press("up")                 # already at top
        assert app.selected_task_id == cols[0][0]   # unchanged, no jump


async def test_no_keypress_selects_offscreen_task(tmp_path):
    app = make_app(tmp_path)
    async with app.run_test(size=(100, 30)) as pilot:
        await pilot.pause()
        visible = {t.id for t in app.board.visible_tasks(False)}
        for view in ("1", "2", "3", "4"):
            await pilot.press(view)
            for key in ("down", "down", "right", "down", "left", "up", "right", "j", "k"):
                await pilot.press(key)
                assert app.selected_task_id in visible


async def test_agenda_nav_follows_urgency_order(tmp_path):
    from taskboard.views import nav_model
    app = make_app(tmp_path)
    async with app.run_test(size=(100, 40)) as pilot:
        await pilot.pause()
        await pilot.press("3")   # agenda
        order = nav_model("agenda", app.board, False)[0]
        board_order = [t.id for t in app.board.visible_tasks(False)]
        assert order != board_order              # grouped by urgency, not board order
        app.selected_task_id = order[0]
        app.refresh_view()
        visited = [app.selected_task_id]
        for _ in range(len(order) - 1):
            await pilot.press("down")
            visited.append(app.selected_task_id)
        assert visited == order


async def test_nav_scrolls_selection_into_view_when_overflowing(tmp_path):
    """Arrow keys must MOVE selection (not be eaten by the scroll container) and
    the selected row must scroll into view — checked with a viewport smaller
    than the content, the exact case the tall-size tests couldn't catch."""
    from taskboard.views import nav_model
    app = make_app(tmp_path)
    async with app.run_test(size=(100, 18)) as pilot:
        await pilot.pause()
        await pilot.press("3")   # agenda (linear, taller than 18 rows)
        order = nav_model("agenda", app.board, False)[0]
        app.selected_task_id = order[0]
        app.refresh_view()
        await pilot.pause()
        for _ in range(len(order) - 1):
            await pilot.press("down")
        await pilot.pause()
        assert app.selected_task_id == order[-1]     # keys moved selection, not scrolled only
        vp = app.query_one("#viewport")
        idx = app._line_map[app.selected_task_id]
        top = vp.scroll_offset.y
        assert top <= idx < top + vp.size.height     # scrolled into view


def test_columns_card_indicators_never_overlap_title(tmp_path):
    """A long-title, high-priority, has-url card: the title text and its trailing
    ↗/◉ indicators must occupy DISJOINT column ranges at every width (proved by
    column-range math on the rendered line), and every line == the exact width."""
    from taskboard.models import Board, Project, Task
    from taskboard.views import render_columns, distribute
    b = Board.load(str(tmp_path / "b.json"))
    lp = Project("Platform Reliability and Observability", "rose", "on_track")
    b.projects.append(lp)
    b.add_task(Task("Refactor the whole authentication and onboarding subsystem",
                    lp.id, "backlog", "high", due_date="2026-07-20",
                    urls=["https://example.com/x"]))
    today = date(2026, 7, 17)
    seen_truncation = False
    for w in (130, 96, 40, 30, 24):     # wide, WezTerm default, narrow, tiny, MIN
        lines = str(render_columns(b, False, None, today, width=w, height=0)).split("\n")
        assert all(len(l) == w for l in lines), f"width {w}: a line != {w}"
        wc0 = distribute((w - 2) - 3, 4)[0]        # BACKLOG (first) column width
        for l in lines:
            cell = l[1:1 + wc0]                     # chars inside the first column
            if "◉" not in cell and "↗" not in cell:
                continue
            first = min(i for i, ch in enumerate(cell) if ch in "◉↗")
            # from the first indicator onward: ONLY spaces/indicators (no title char)
            assert all(ch in " ◉↗" for ch in cell[first:]), (w, repr(cell))
            title_part = cell[2:first]              # after the "▊ " prefix
            assert "◉" not in title_part and "↗" not in title_part
            if "…" in title_part:
                seen_truncation = True
    assert seen_truncation   # the long title really was truncated to reserve room


async def test_url_task_open_action(tmp_path, monkeypatch):
    app = make_app(tmp_path)
    async with app.run_test() as pilot:
        opened = []
        monkeypatch.setattr("taskboard.app.webbrowser.open", opened.append)
        url_task = next(t for t in app.board.tasks if t.urls)
        app.selected_task_id = url_task.id
        app.action_open_url()
        assert opened == url_task.urls


async def test_url_renders_link_and_arrow(tmp_path):
    app = make_app(tmp_path)
    async with app.run_test() as pilot:
        await pilot.press("3")  # agenda shows titles wide enough
        assert "↗" in board_text(app)


# ---- US-2: multiple URLs per task ----------------------------------------- #
def test_task_urls_model_migration():
    """TC-002a/b (LLR-002.1/002.2): default_factory list + legacy migration."""
    from taskboard.models import Task
    # default is an empty list, not shared across instances (no mutable default)
    assert Task("t").urls == []
    assert Task("a").urls is not Task("b").urls
    # legacy single "url" string migrates to a one-element list
    assert Task.from_dict({"title": "x", "url": "https://x"}).urls == ["https://x"]
    # modern "urls" list is read as-is
    assert Task.from_dict({"title": "x", "urls": ["a", "b"]}).urls == ["a", "b"]
    # malformed / missing inputs degrade to [] and never raise
    assert Task.from_dict({"title": "x"}).urls == []
    assert Task.from_dict({"title": "x", "urls": "notalist"}).urls == []
    assert Task.from_dict({"title": "x", "url": None}).urls == []


def test_task_urls_roundtrip(tmp_path):
    """TC-002c (LLR-002.3): save serializes urls; load reconstructs it exactly."""
    from taskboard.models import Board, Task
    p = str(tmp_path / "b.json")
    board = Board.load(p)
    links = ["https://a.com", "https://b.com", "https://c.com"]
    board.add_task(Task("multi", None, "backlog", "normal", urls=links))
    reloaded = Board.load(p)
    t = next(t for t in reloaded.tasks if t.title == "multi")
    assert t.urls == links


def test_legacy_url_board_migrates_on_load(tmp_path):
    """DD-2: a hand-written legacy board (`url` key) loads with urls==[url];
    the legacy singular attribute no longer exists on the model."""
    import json
    from taskboard.models import Board, Task
    p = tmp_path / "legacy.json"
    p.write_text(json.dumps({
        "projects": [],
        "tasks": [{"title": "old", "url": "https://legacy.example.com/"}],
    }), encoding="utf-8")
    board = Board.load(str(p))
    assert board.tasks[0].urls == ["https://legacy.example.com/"]
    assert not hasattr(Task("t"), "url")   # legacy field dropped (one-way migration)


async def test_at_002_multiple_urls_black_box(tmp_path, monkeypatch):
    """AT-002 (US-2, black-box): the user enters several URLs in the modal;
    the card shows ↗ and pressing the real `o` key opens every valid URL.
    Invalid / markup-injection lines are dropped (C-3/F9), no MarkupError."""
    app = make_app(tmp_path)
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("a")
        await pilot.pause()
        app.screen.query_one("#f-title", Input).value = "MULTIURL"
        app.screen.query_one("#f-urls", TextArea).text = (
            "https://one.example.com\n"
            "https://ok.example.com/[boom]\n"   # markup chars -> valid_url drops it
            "not a url\n"                        # non-http -> dropped
            "https://two.example.com")
        await save_open_modal(app, pilot)
        task = next(t for t in app.board.tasks if t.title == "MULTIURL")
        # modal kept ONLY the two valid URLs, in order
        assert task.urls == ["https://one.example.com", "https://two.example.com"]
        # the card renders the ↗ indicator (agenda shows titles wide) — no crash
        app.selected_task_id = task.id
        await pilot.press("3")
        assert "↗" in board_text(app)
        # pressing the actual `o` binding opens EVERY valid URL
        opened = []
        monkeypatch.setattr("taskboard.app.webbrowser.open", opened.append)
        await pilot.press("o")
        assert opened == ["https://one.example.com", "https://two.example.com"]


async def test_markup_injection_is_escaped(tmp_path):
    """A title full of markup must render literally, never crash (pitfall A1)."""
    app = make_app(tmp_path)
    async with app.run_test() as pilot:
        await pilot.press("a")
        await pilot.pause()
        app.screen.query_one("#f-title", Input).value = "[red]boom[/red]"
        await save_open_modal(app, pilot)
        await pilot.press("3")
        text = board_text(app)   # would have raised MarkupError if not escaped
        assert "boom" in text
        assert "[red]" in text   # brackets preserved literally, tag not consumed


# ---- pure-render tests: undated items never crash gantt/agenda ------------- #
def test_gantt_handles_undated_tasks(tmp_path):
    board = Board.load(str(tmp_path / "b.json"))  # seeded
    # a task with no dates at all
    board.add_task(Task("floating task", None, "backlog", "normal"))
    out = str(render_gantt(board, False, None, today=date(2026, 7, 17)))
    assert "GANTT" in out
    assert "UNSCHEDULED" in out
    assert "floating task" in out


def test_agenda_handles_undated_tasks(tmp_path):
    board = Board.load(str(tmp_path / "b.json"))
    board.add_task(Task("no due date task", None, "backlog", "normal"))
    out = str(render_agenda(board, False, None, today=date(2026, 7, 17)))
    assert "AGENDA" in out
    assert "NO DATE" in out


def test_corrupt_file_starts_empty(tmp_path):
    p = tmp_path / "bad.json"
    p.write_text("{ this is not valid json ", encoding="utf-8")
    board = Board.load(str(p))
    assert board.projects == []
    assert board.tasks == []
