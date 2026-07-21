"""Pilot tests that prove the app actually works (assert rendered content)."""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path

import pytest

from textual.widgets import Button, Footer, Input, OptionList, Select, Static, TextArea

from taskboard import models, modals
from taskboard.app import BoardView, TaskboardApp
from taskboard.models import Board, Task
from taskboard.modals import CalendarModal, TaskDetails, TaskModal, image_block
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


# ---- project manager (edit / archive / delete existing projects) ---------- #
async def test_manage_projects_edit_status_persists(tmp_path):
    """P opens the manager; editing a project's status to 'paused' updates the
    board AND survives a reload from disk (real key presses, on-disk oracle)."""
    board_path = str(tmp_path / "board.json")
    app = TaskboardApp(board_path=board_path)
    async with app.run_test(size=(120, 40)) as pilot:
        target = next(p for p in app.board.projects if p.name == "Mobile App")
        assert target.status == "on_track"                 # precondition
        idx = app.board.projects.index(target)
        await pilot.press("P")                              # open project manager
        await pilot.pause()
        app.screen.query_one("#proj-list", OptionList).highlighted = idx
        await pilot.press("e")                              # edit highlighted project
        await pilot.pause()
        app.screen.query_one("#f-status", Select).value = "paused"
        app.screen.query_one("#save", Button).press()
        await pilot.pause()
        assert app.board.project_by_id(target.id).status == "paused"
    reloaded = Board.load(board_path)                       # reload from disk
    assert reloaded.project_by_id(target.id).status == "paused"


async def test_manage_projects_archive_hides_and_persists(tmp_path):
    """Archiving a project via the manager hides it under the archived toggle in
    the board render, and the archived flag persists to disk."""
    board_path = str(tmp_path / "board.json")
    app = TaskboardApp(board_path=board_path)
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("1")                              # swimlanes shows project rows
        target = next(p for p in app.board.projects if p.name == "Mobile App")
        assert not target.archived
        assert "Mobile App" in board_text(app)             # visible before archiving
        idx = app.board.projects.index(target)
        await pilot.press("P")
        await pilot.pause()
        app.screen.query_one("#proj-list", OptionList).highlighted = idx
        await pilot.press("x")                              # archive
        await pilot.pause()
        assert app.board.project_by_id(target.id).archived is True
        await pilot.press("escape")                         # close the manager
        await pilot.pause()
        assert "Mobile App" not in board_text(app)         # hidden by default
        await pilot.press("v")                              # show archived
        assert "Mobile App" in board_text(app)             # visible again
    reloaded = Board.load(board_path)
    assert reloaded.project_by_id(target.id).archived is True


async def test_manage_projects_delete_moves_tasks_to_inbox(tmp_path):
    """Deleting a project reassigns its tasks to Inbox (project_id=None); the
    tasks survive and the reassignment persists to disk (least-destructive)."""
    board_path = str(tmp_path / "board.json")
    app = TaskboardApp(board_path=board_path)
    async with app.run_test(size=(120, 40)) as pilot:
        target = next(p for p in app.board.projects if p.name == "API Platform")
        task_ids = [t.id for t in app.board.tasks if t.project_id == target.id]
        assert task_ids                                     # precondition: it has tasks
        idx = app.board.projects.index(target)
        await pilot.press("P")
        await pilot.pause()
        app.screen.query_one("#proj-list", OptionList).highlighted = idx
        await pilot.press("d")                              # delete -> ConfirmModal
        await pilot.pause()
        app.screen.query_one("#yes", Button).press()        # confirm
        await pilot.pause()
        assert app.board.project_by_id(target.id) is None
        assert all(app.board.task_by_id(t).project_id is None for t in task_ids)
    reloaded = Board.load(board_path)
    assert reloaded.project_by_id(target.id) is None
    assert all(reloaded.task_by_id(t) is not None for t in task_ids)      # survived
    assert all(reloaded.task_by_id(t).project_id is None for t in task_ids)


async def test_manage_projects_empty_state_no_crash(tmp_path):
    """Zero projects -> a friendly placeholder, and e/x/d are safe no-ops (no
    project selected -> no editor/confirm pushed, no crash)."""
    app = make_app(tmp_path)
    async with app.run_test(size=(120, 40)) as pilot:
        app.board.projects.clear()
        app.board.save()
        app.refresh_view()
        await pilot.press("P")
        await pilot.pause()
        assert len(app.screen_stack) == 2                   # picker is open
        for key in ("e", "x", "d"):
            await pilot.press(key)
            await pilot.pause()
            assert len(app.screen_stack) == 2               # nothing pushed, still open
        assert app.board.projects == []


async def test_manage_projects_escapes_markup_name(tmp_path):
    """A project name full of markup is listed literally (escaped), never parsed
    as tags -> no MarkupError when the picker builds its list (pitfall A1)."""
    app = make_app(tmp_path)
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("p")                              # add a markup-named project
        await pilot.pause()
        app.screen.query_one("#f-name", Input).value = "[red]boom[/red]"
        await save_open_modal(app, pilot)
        await pilot.press("P")                              # open manager (builds the list)
        await pilot.pause()
        ol = app.screen.query_one("#proj-list", OptionList)
        prompts = [str(ol.get_option_at_index(i).prompt)
                   for i in range(len(app.board.projects))]
        # the brackets are backslash-escaped in the list -> rendered literally
        assert any("\\[red]boom\\[/red]" in pr for pr in prompts)


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


# ---- US-3: images per task ------------------------------------------------ #
def test_task_images_model(tmp_path):
    """TC-005a/b (LLR-005.1/005.2): default_factory list + lenient read + round-trip."""
    from taskboard.models import Board, Task
    assert Task("t").images == []
    assert Task("a").images is not Task("b").images
    assert Task.from_dict({"title": "x", "images": ["a", "b"]}).images == ["a", "b"]
    assert Task.from_dict({"title": "x"}).images == []
    assert Task.from_dict({"title": "x", "images": "nope"}).images == []
    p = str(tmp_path / "b.json")
    board = Board.load(p)
    refs = ["./mockups/home.png", "https://pics.example.com/b.jpg"]
    board.add_task(Task("img", None, "backlog", "normal", images=refs))
    t = next(t for t in Board.load(p).tasks if t.title == "img")
    assert t.images == refs


async def test_open_images_allowlist_and_isfile(tmp_path, monkeypatch):
    """TC-007c (LLR-007.3): os.startfile fires ONLY for an existing image-ext
    local file; missing files, non-image extensions, UNC and file:// are all
    refused (never executed, never crash)."""
    real = tmp_path / "ok.png"
    real.write_bytes(b"x")
    app = make_app(tmp_path)
    async with app.run_test() as pilot:
        started = []
        monkeypatch.setattr("taskboard.app.os.startfile", started.append)
        t = Task("imgs", None, "backlog", "normal", images=[
            str(real),                      # existing .png  -> opened
            str(tmp_path / "gone.png"),     # allowed ext, missing file -> skip
            str(tmp_path / "x.svg"),        # scriptable ext -> skip (F4)
            "C:/evil.exe",                  # executable -> skip
            "\\\\host\\share\\a.png",       # UNC -> skip (F3)
            "file:///c:/a.png",             # file URL -> skip (F3)
        ])
        app.board.add_task(t)
        app.selected_task_id = t.id
        app.open_all_images_raw(app.selected_task)
        assert started == [str(real)]       # only the existing allowed image file


SEED_DENYLIST = re.compile(
    r"grndia|textualize\.io|job\s*hunt|m22|dev-flow|proposal v2|funnel|"
    r"portfolio|interview prep|cv refresh|systems 5/5|count-guard|rag paper|"
    r"textual", re.IGNORECASE)


def test_at_001_seed_generic_and_complete(tmp_path):
    """AT-001 (US-1, black-box): the freshly seeded, on-disk board.json contains
    ZERO author-denylist tokens AND at least one item in every feature dimension.
    The dimension checks are derived from the seed itself (input-set-as-oracle)."""
    from pathlib import Path
    from taskboard.models import (Board, PROJECT_STATUSES, TASK_STATUSES,
                                  TASK_PRIORITIES)
    from taskboard.views import urgency

    p = tmp_path / "board.json"
    board = Board.load(str(p))          # non-existent path -> seed_data() fires + saves
    projects, tasks = board.projects, board.tasks

    # (a) 0 author tokens over the ACTUAL persisted deliverable
    on_disk = Path(p).read_text(encoding="utf-8")
    assert SEED_DENYLIST.findall(on_disk) == []

    # (b) all four project statuses (incl. the previously-missing 'cancelled')
    assert {pr.status for pr in projects} == set(PROJECT_STATUSES)
    # (c) all four task statuses + all three priorities
    assert {t.status for t in tasks} == set(TASK_STATUSES)
    assert {t.priority for t in tasks} == set(TASK_PRIORITIES)
    # (d) >=1 archived project AND >=1 archived task
    assert sum(1 for pr in projects if pr.archived) >= 1
    assert sum(1 for t in tasks if t.archived) >= 1
    # (e) standalone AND project-bound tasks
    assert any(t.project_id is None for t in tasks)
    assert any(t.project_id is not None for t in tasks)
    # (f) urgency buckets span overdue / today / this-week-or-later / none / done
    today = date.today()
    buckets = {urgency(t, today) for t in tasks}
    assert {"overdue", "today", "none", "done"} <= buckets
    assert buckets & {"week", "later"}
    # (g) the batch's own new capabilities are showcased
    assert any(len(t.urls) >= 2 for t in tasks)
    assert any(len(t.images) >= 1 for t in tasks)


async def test_at_003_images_black_box(tmp_path, monkeypatch):
    """AT-003 (US-3, black-box): a task with image refs shows the ▤ glyph, and
    pressing the real `i` key opens the image URL (browser) + the existing
    image-ext local file (os.startfile). A .svg, an .exe and a missing file are
    NOT startfile'd and do not crash."""
    real_png = tmp_path / "shot.png"
    real_png.write_bytes(b"x")
    svg = tmp_path / "vec.svg"
    svg.write_bytes(b"<svg/>")              # exists -> only the extension gate stops it
    exe = tmp_path / "evil.exe"
    exe.write_bytes(b"MZ")
    missing = tmp_path / "gone.png"
    refs = [str(real_png), "https://pics.example.com/a.png",
            str(svg), str(exe), str(missing)]
    app = make_app(tmp_path)
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("a")
        await pilot.pause()
        app.screen.query_one("#f-title", Input).value = "IMGTASK"
        app.screen.query_one("#f-images", TextArea).text = "\n".join(refs)
        await save_open_modal(app, pilot)
        task = next(t for t in app.board.tasks if t.title == "IMGTASK")
        assert task.images == refs          # modal keeps every non-blank line, in order
        # the card renders the width-1 image glyph, lines stay width-exact
        app.selected_task_id = task.id
        await pilot.press("2")
        text = board_text(app)
        assert "▤" in text
        # every rendered line is the same width -> the glyph is single-cell
        assert len({len(l) for l in text.split("\n") if l}) == 1
        # pressing the actual `i` binding routes each ref safely
        started, browsed = [], []
        monkeypatch.setattr("taskboard.app.os.startfile", started.append)
        monkeypatch.setattr("taskboard.app.webbrowser.open", browsed.append)
        app.open_all_images_raw(app.selected_task)
        assert started == [str(real_png)]                       # existing image only
        assert browsed == ["https://pics.example.com/a.png"]    # the http image URL
        assert str(svg) not in started and str(exe) not in started
        assert str(missing) not in started


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


def test_save_pil_image_increments(tmp_path):
    """save_pil_image writes paste-001, paste-002, ... in the given folder."""
    from PIL import Image as PILImage
    from taskboard.models import save_pil_image
    d = tmp_path / "imgs"
    a = save_pil_image(d, PILImage.new("RGB", (4, 4)))
    b = save_pil_image(d, PILImage.new("RGB", (4, 4)))
    assert a.name == "paste-001.png" and b.name == "paste-002.png"
    assert a.is_file() and b.is_file()


async def test_clipboard_paste_saves_and_appends(tmp_path, monkeypatch):
    """Pasting a clipboard bitmap writes a PNG under the task's image folder and
    appends its path to the modal's images field (real key + button presses)."""
    from PIL import Image as PILImage
    from taskboard import modals
    app = make_app(tmp_path)
    async with app.run_test() as pilot:
        monkeypatch.setattr(modals, "grab_clipboard_image",
                            lambda: PILImage.new("RGB", (20, 12), (10, 20, 30)))
        await pilot.press("a")                     # open new-task modal
        await pilot.pause()
        app.screen.query_one("#f-title", Input).value = "SHOT"
        app.screen.query_one("#paste-img", Button).press()
        await pilot.pause()
        area = app.screen.query_one("#f-images", TextArea)
        lines = [l for l in area.text.splitlines() if l.strip()]
        assert len(lines) == 1
        assert lines[0].endswith(".png")
        assert Path(lines[0]).is_file()


async def test_image_viewer_opens_without_crash(tmp_path):
    """i opens the inline viewer for a task holding a real local image + a URL."""
    from PIL import Image as PILImage
    from taskboard.modals import ImageViewer
    app = make_app(tmp_path)
    async with app.run_test(size=(100, 40)) as pilot:
        img = tmp_path / "pic.png"
        PILImage.new("RGB", (16, 16), (0, 128, 255)).save(img)
        t = app.board.tasks[0]
        t.images = [str(img), "https://example.com/x.png"]
        app.selected_task_id = t.id
        await pilot.press("i")
        await pilot.pause()
        assert isinstance(app.screen, ImageViewer)


async def test_image_viewer_open_raw_fires(tmp_path, monkeypatch):
    """`o` inside the viewer opens every image raw via open_all_images_raw
    (regression: the viewer must reference the task, not Textual's _task slot)."""
    from PIL import Image as PILImage
    opened = []
    app = make_app(tmp_path)
    async with app.run_test(size=(100, 40)) as pilot:
        img = tmp_path / "pic.png"
        PILImage.new("RGB", (16, 16), (0, 200, 120)).save(img)
        t = app.board.tasks[0]
        t.images = [str(img)]
        app.selected_task_id = t.id
        monkeypatch.setattr("os.startfile", lambda p: opened.append(p), raising=False)
        await pilot.press("i")                 # open the viewer
        await pilot.pause()
        await pilot.press("o")                 # open raw
        await pilot.pause()
        assert opened == [str(img)]


# --------------------------------------------------------------------------- #
# Notes field + read-only details view (fast-dev-flow: notes-details batch)
# --------------------------------------------------------------------------- #
def _details_text(app) -> str:
    """Plain text of every Static/Label on the current screen (markup stripped)."""
    from textual.widgets import Static
    return " ".join(str(w.render()) for w in app.screen.query(Static))


def test_task_notes_backcompat_from_dict():
    """AC1: a task dict with no 'notes' key loads with notes == '' (old boards)."""
    t = Task.from_dict({"title": "legacy", "status": "backlog"})
    assert t.notes == ""


async def test_task_notes_persist_through_reload(tmp_path):
    """AC2: notes typed in the edit modal survive a fresh Board.load from disk."""
    app = make_app(tmp_path)
    async with app.run_test() as pilot:
        await pilot.press("a")
        await pilot.pause()
        app.screen.query_one("#f-title", Input).value = "NOTETASK"
        app.screen.query_one("#f-notes", TextArea).text = "remember the LUKS passphrase"
        await save_open_modal(app, pilot)
    reloaded = Board.load(str(tmp_path / "board.json"))
    t = next(t for t in reloaded.tasks if t.title == "NOTETASK")
    assert t.notes == "remember the LUKS passphrase"


async def test_enter_opens_readonly_details(tmp_path):
    """AC3/AC6: Enter opens TaskDetails (not the editor) and it has no Save control."""
    app = make_app(tmp_path)
    async with app.run_test() as pilot:
        assert app.selected_task is not None          # a seeded task is selected
        await pilot.press("enter")
        await pilot.pause()
        assert isinstance(app.screen, TaskDetails)
        assert not isinstance(app.screen, TaskModal)
        assert len(app.screen.query("#save")) == 0    # read-only: no save button


async def test_details_shows_all_fields_and_image(tmp_path):
    """AC4/AC5: details renders every field + notes + urls, and an on-disk image
    goes through the render path (never the 'missing' branch)."""
    from PIL import Image as PILImage
    app = make_app(tmp_path)
    async with app.run_test(size=(100, 40)) as pilot:
        img = tmp_path / "pic.png"
        PILImage.new("RGB", (16, 16), (0, 150, 90)).save(img)
        t = Task(title="DETAILTASK", status="doing", priority="high",
                 due_date="2026-09-01", notes="line one\nline two",
                 urls=["https://example.com/x"], images=[str(img)])
        app.board.tasks.append(t)
        app.selected_task_id = t.id
        app.refresh_view()
        await pilot.press("enter")
        await pilot.pause()
        assert isinstance(app.screen, TaskDetails)
        text = _details_text(app)
        assert "DETAILTASK" in text
        assert "doing" in text and "high" in text and "2026-09-01" in text
        assert "line one" in text and "line two" in text     # notes shown
        assert "example.com/x" in text                       # url listed
        assert "missing" not in text                         # the real file resolved


async def test_details_escapes_notes_markup(tmp_path):
    """AC6: bracketed notes are escaped, not interpreted as Rich markup (A1)."""
    app = make_app(tmp_path)
    async with app.run_test() as pilot:
        t = Task(title="X", notes="[bold]INJECT[/bold]")
        app.board.tasks.append(t)
        app.selected_task_id = t.id
        app.refresh_view()
        await pilot.press("enter")
        await pilot.pause()
        # literal brackets survive -> markup was escaped, not rendered as bold
        assert "[bold]INJECT[/bold]" in _details_text(app)


def test_image_block_link_and_missing_fallbacks(tmp_path):
    """AC5: the shared image_block helper links remote URLs and flags missing
    local files, and never raises on either."""
    remote = list(image_block("https://example.com/a.png"))
    assert remote and "link" in str(remote[0].render())
    missing = list(image_block(str(tmp_path / "nope.png")))
    assert missing and "missing" in str(missing[0].render())


# --------------------------------------------------------------------------- #
# Reliable paste (Ctrl+V) + calendar date picker (fast-dev-flow: dates+paste)
# --------------------------------------------------------------------------- #
import sys as _sys


def test_grab_clipboard_text_dispatch_and_never_raises(monkeypatch):
    """AC1: grab_clipboard_text returns the text or None, and never raises even
    when the underlying reader blows up."""
    if _sys.platform == "win32":
        monkeypatch.setattr(models, "_win_clipboard_text", lambda: "hello clip")
        assert models.grab_clipboard_text() == "hello clip"

        def boom():
            raise RuntimeError("nope")
        monkeypatch.setattr(models, "_win_clipboard_text", boom)
        assert models.grab_clipboard_text() is None          # guarded
    else:
        def raise_os(*a, **k):
            raise OSError("no clipboard tool")
        monkeypatch.setattr("subprocess.run", raise_os)
        assert models.grab_clipboard_text() is None


async def test_ctrl_v_pastes_into_focused_input(tmp_path, monkeypatch):
    """AC2: Ctrl+V inserts clipboard text into the focused Input."""
    monkeypatch.setattr(modals, "grab_clipboard_text", lambda: "PASTED-TEXT")
    app = make_app(tmp_path)
    async with app.run_test() as pilot:
        await pilot.press("a")                       # open TaskModal
        await pilot.pause()
        inp = app.screen.query_one("#f-title", Input)
        inp.focus()
        await pilot.pause()
        await pilot.press("ctrl+v")
        await pilot.pause()
        assert "PASTED-TEXT" in inp.value


async def test_ctrl_v_pastes_into_focused_textarea(tmp_path, monkeypatch):
    """AC3: Ctrl+V inserts clipboard text into the focused notes TextArea."""
    monkeypatch.setattr(modals, "grab_clipboard_text", lambda: "MULTI\nLINE")
    app = make_app(tmp_path)
    async with app.run_test() as pilot:
        await pilot.press("a")
        await pilot.pause()
        ta = app.screen.query_one("#f-notes", TextArea)
        ta.focus()
        await pilot.pause()
        await pilot.press("ctrl+v")
        await pilot.pause()
        assert "MULTI" in ta.text and "LINE" in ta.text


async def test_ctrl_v_empty_clipboard_is_noop(tmp_path, monkeypatch):
    """AC4: with no clipboard text, Ctrl+V changes nothing and doesn't crash."""
    monkeypatch.setattr(modals, "grab_clipboard_text", lambda: None)
    app = make_app(tmp_path)
    async with app.run_test() as pilot:
        await pilot.press("a")
        await pilot.pause()
        inp = app.screen.query_one("#f-title", Input)
        inp.focus()
        await pilot.pause()
        await pilot.press("ctrl+v")
        await pilot.pause()
        assert inp.value == ""                       # unchanged, no crash


async def test_calendar_enter_and_escape(tmp_path):
    """AC5: Enter returns the highlighted date; Esc returns None."""
    app = make_app(tmp_path)
    async with app.run_test() as pilot:
        out = {}
        app.push_screen(CalendarModal("2026-07-20"), lambda r: out.__setitem__("v", r))
        await pilot.pause()
        await pilot.press("enter")
        await pilot.pause()
        assert out["v"] == "2026-07-20"

        out2 = {}
        app.push_screen(CalendarModal("2026-07-20"), lambda r: out2.__setitem__("v", r))
        await pilot.pause()
        await pilot.press("escape")
        await pilot.pause()
        assert out2["v"] is None


async def test_calendar_navigation(tmp_path):
    """AC6: arrows/month/today move the highlighted date (both directions), and
    a month hop clamps the day to the shorter month."""
    async def pick_after(keys, seed="2026-07-20"):
        app = make_app(tmp_path)
        out = {}
        async with app.run_test() as pilot:
            app.push_screen(CalendarModal(seed), lambda r: out.__setitem__("v", r))
            await pilot.pause()
            for k in keys:
                await pilot.press(k)
            await pilot.press("enter")
            await pilot.pause()
        return out["v"]

    assert await pick_after(["right"]) == "2026-07-21"           # +1 day
    assert await pick_after(["left"]) == "2026-07-19"            # -1 day
    assert await pick_after(["down"]) == "2026-07-27"            # +1 week
    assert await pick_after(["up"]) == "2026-07-13"              # -1 week
    assert await pick_after(["right_square_bracket"]) == "2026-08-20"   # +1 month
    assert await pick_after(["left_square_bracket"]) == "2026-06-20"    # -1 month
    assert await pick_after(["pagedown"]) == "2026-08-20"        # +1 month (alias)
    assert await pick_after(["t"]) == date.today().isoformat()   # today
    # day-clamp: Jan 31 -> Feb has no 31st -> 28 (2026 not a leap year)
    assert await pick_after(["right_square_bracket"], seed="2026-01-31") == "2026-02-28"


async def test_calendar_button_writes_date_into_field(tmp_path):
    """AC7: the calendar button opens the picker and writes YYYY-MM-DD back into
    the date Input (empty field -> today)."""
    app = make_app(tmp_path)
    async with app.run_test() as pilot:
        await pilot.press("a")                       # TaskModal
        await pilot.pause()
        app.screen.query_one("#cal-f-start", Button).press()
        await pilot.pause()
        assert isinstance(app.screen, CalendarModal)
        await pilot.press("enter")                   # pick seeded (today)
        await pilot.pause()
        val = app.screen.query_one("#f-start", Input).value
        assert val == date.today().isoformat()


def test_clean_clipboard_text_strips_controls_and_caps():
    """Guards the freeze/terminal-corruption fix: control bytes (e.g. the ESC in
    a mouse escape sequence) and NULs are dropped, tab/newline kept, length capped."""
    from taskboard.models import _clean_clipboard_text, _MAX_PASTE_CHARS
    assert _clean_clipboard_text("a\tb\nc") == "a\tb\nc"          # tab/newline kept
    assert _clean_clipboard_text("x\x1b[<0;5;5M\x00y") == "x[<0;5;5My"  # ESC + NUL removed
    assert _clean_clipboard_text("") is None
    assert _clean_clipboard_text(None) is None
    assert len(_clean_clipboard_text("z" * (_MAX_PASTE_CHARS + 50))) == _MAX_PASTE_CHARS


def test_win_clipboard_roundtrip():
    """Proves the 64-bit handle fix on real Windows: a string put on the clipboard
    reads back intact (the truncated-handle bug returned None or garbage)."""
    import sys
    import subprocess
    if sys.platform != "win32":
        pytest.skip("windows clipboard path only")
    sample = "roundtrip 123 ABC taskboard"
    subprocess.run(["powershell", "-NoProfile", "-Command", f"Set-Clipboard -Value '{sample}'"],
                   check=False)
    assert models.grab_clipboard_text() == sample
