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
from taskboard.modals import (CalendarModal, PhaseEditor, TaskDetails, TaskModal,
                              image_block)
from taskboard.ribbon import Ribbon
from taskboard.views import META_FULL_INNER, render_agenda, render_gantt


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
        assert "COLUMNS" in board_text(app)      # columns
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
        assert all(app.board.task_by_id(t).phase == app.board.phases[0] for t in visited)
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
        assert app.selected_task_id == cols[1][0]   # 2nd phase column's first task
        await pilot.press("right")
        # the 3rd phase column has tasks in seed; Right lands on its first task
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
                    lp.id, "Backlog", "high", due_date="2026-07-20",
                    urls=["https://example.com/x"]))
    today = date(2026, 7, 17)
    n = len(b.phases)
    seen_truncation = False
    for w in (130, 96, 40, 30, 24):     # wide, WezTerm default, narrow, tiny, MIN
        lines = str(render_columns(b, False, None, today, width=w, height=0)).split("\n")
        assert all(len(l) == w for l in lines), f"width {w}: a line != {w}"
        wc0 = distribute((w - 2) - (n - 1), n)[0]   # first phase column width
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
    board.add_task(Task("multi", None, "Backlog", "normal", urls=links))
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
    board.add_task(Task("img", None, "Backlog", "normal", images=refs))
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
        t = Task("imgs", None, "Backlog", "normal", images=[
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
    from taskboard.models import (Board, DEFAULT_PHASES, PROJECT_STATUSES,
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
    # (c) every default phase is populated, a blocked task exists, all priorities
    assert {t.phase for t in tasks} == set(DEFAULT_PHASES)
    assert any(t.blocked for t in tasks)
    assert {t.priority for t in tasks} == set(TASK_PRIORITIES)
    # (d) >=1 archived project AND >=1 archived task
    assert sum(1 for pr in projects if pr.archived) >= 1
    assert sum(1 for t in tasks if t.archived) >= 1
    # (e) standalone AND project-bound tasks
    assert any(t.project_id is None for t in tasks)
    assert any(t.project_id is not None for t in tasks)
    # (f) urgency buckets span overdue / today / this-week-or-later / none / done
    today = date.today()
    buckets = {urgency(t, today, board) for t in tasks}
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
    board.add_task(Task("floating task", None, "Backlog", "normal"))
    out = str(render_gantt(board, False, None, today=date(2026, 7, 17)))
    assert "GANTT" in out
    assert "UNSCHEDULED" in out
    assert "floating task" in out


def test_agenda_handles_undated_tasks(tmp_path):
    board = Board.load(str(tmp_path / "b.json"))
    board.add_task(Task("no due date task", None, "Backlog", "normal"))
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
        t = Task(title="DETAILTASK", phase="Doing", priority="high",
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
        assert "Doing" in text and "high" in text and "2026-09-01" in text
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
    # C0 (ESC), NUL, DEL (0x7f) and C1 (0x9b) all removed; printable payload kept
    assert _clean_clipboard_text("x\x1b[<0;5;5M\x00\x7f\x9by") == "x[<0;5;5My"
    assert _clean_clipboard_text("café 🎉 — ñ") == "café 🎉 — ñ"   # accents/emoji/≥0xA0 kept
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
    # save the user's clipboard and restore it afterward (don't clobber it)
    prior = subprocess.run(["powershell", "-NoProfile", "-Command", "Get-Clipboard"],
                           capture_output=True, text=True).stdout
    try:
        sample = "roundtrip 123 ABC taskboard"
        subprocess.run(["powershell", "-NoProfile", "-Command", f"Set-Clipboard -Value '{sample}'"],
                       check=False)
        assert models.grab_clipboard_text() == sample
    finally:
        subprocess.run(["powershell", "-NoProfile", "-Command", "Set-Clipboard", "-Value", prior],
                       check=False)


# ---- project palette (12 colours) ---------------------------------------- #
def test_palette_has_twelve_and_keeps_the_originals():
    """The 5 original colours must survive with their exact hex, so existing
    boards keep the colours their projects were saved with."""
    from taskboard.models import PROJECT_COLORS
    from taskboard.views import HEX
    assert len(PROJECT_COLORS) == 12
    assert len(set(PROJECT_COLORS)) == 12                 # no duplicates
    for name in ("violet", "sky", "amber", "rose", "green"):
        assert name in PROJECT_COLORS
    assert HEX["violet"] == "#a78bfa"
    assert HEX["sky"] == "#38bdf8"
    assert HEX["amber"] == "#fbbf24"
    assert HEX["rose"] == "#fb7185"
    assert HEX["green"] == "#4ade80"


def test_every_project_colour_has_a_hex():
    """WHY: views look colours up by name — a colour in the picker without a HEX
    entry would render wrong (or blow up) the moment a user selects it."""
    from taskboard.models import PROJECT_COLORS
    from taskboard.views import HEX
    assert [c for c in PROJECT_COLORS if c not in HEX] == []


def test_project_accepts_a_new_colour():
    from taskboard.models import Project
    assert Project.from_dict({"name": "X", "color": "indigo"}).color == "indigo"
    assert Project.from_dict({"name": "Y", "color": "nope"}).color == "violet"   # fallback


# --------------------------------------------------------------------------- #
# Ordered custom phases (fast-dev-flow increment 2)
# --------------------------------------------------------------------------- #
def test_legacy_status_migrates_to_phase():
    """WHY: boards written before phases existed must keep opening — every legacy
    status maps to exactly one (phase, blocked) pair, and 'blocked' becomes a flag
    on the Doing phase rather than a phase of its own."""
    cases = {"backlog": ("Backlog", False), "doing": ("Doing", False),
             "active": ("Doing", False), "blocked": ("Doing", True),
             "done": ("Done", False)}
    for status, expected in cases.items():
        t = Task.from_dict({"title": "x", "status": status})
        assert (t.phase, t.blocked) == expected, status
    # unknown / missing status -> the first default phase, not blocked
    for d in ({"title": "x"}, {"title": "x", "status": "nonsense"}):
        t = Task.from_dict(d)
        assert (t.phase, t.blocked) == ("Backlog", False)
    # an explicit phase wins over any legacy status still in the file
    t = Task.from_dict({"title": "x", "status": "backlog", "phase": "Done"})
    assert t.phase == "Done"


def test_migration_preserves_every_task_and_field(tmp_path):
    """WHY: migration must never cost the user data. A legacy board survives a
    load->save->load round-trip with every task, every field, and even keys this
    version does not model (written by another version) intact."""
    import json
    p = tmp_path / "legacy.json"
    p.write_text(json.dumps({
        "projects": [{"id": "p1", "name": "Old", "color": "sky", "status": "on_track",
                      "owner_email": "someone@example.com"}],          # unknown key
        "tasks": [
            {"id": "t1", "title": "one", "project_id": "p1", "status": "backlog",
             "urls": ["https://a.example.com"], "images": ["./a.png"]},
            {"id": "t2", "title": "two", "project_id": "p1", "status": "blocked",
             "urls": ["https://b.example.com", "https://c.example.com"],
             "images": ["./b.png", "./c.png"]},
            {"id": "t3", "title": "three", "status": "done",
             "estimate_hours": 7},                                      # unknown key
            {"id": "t4", "title": "four", "status": "active"},
        ],
    }), encoding="utf-8")

    Board.load(str(p)).save()                    # migrate + write back
    reloaded = Board.load(str(p))

    assert [t.id for t in reloaded.tasks] == ["t1", "t2", "t3", "t4"]     # none dropped
    assert [t.title for t in reloaded.tasks] == ["one", "two", "three", "four"]
    assert [(t.phase, t.blocked) for t in reloaded.tasks] == [
        ("Backlog", False), ("Doing", True), ("Done", False), ("Doing", False)]
    assert reloaded.task_by_id("t1").urls == ["https://a.example.com"]
    assert reloaded.task_by_id("t1").images == ["./a.png"]
    assert reloaded.task_by_id("t2").urls == ["https://b.example.com",
                                              "https://c.example.com"]
    assert reloaded.task_by_id("t2").images == ["./b.png", "./c.png"]
    assert reloaded.task_by_id("t3").extra["estimate_hours"] == 7
    assert reloaded.projects[0].extra["owner_email"] == "someone@example.com"
    # and the unknown keys are really on disk, not just in memory
    on_disk = json.loads(p.read_text(encoding="utf-8"))
    assert on_disk["phases"] == list(models.DEFAULT_PHASES)
    assert next(t for t in on_disk["tasks"] if t["id"] == "t3")["estimate_hours"] == 7
    assert on_disk["projects"][0]["owner_email"] == "someone@example.com"


def test_task_progress_from_phase_order(tmp_path):
    """WHY: progress is positional — it is the phase's index in the board's own
    order, so a custom workflow reports progress without any extra bookkeeping."""
    b = Board([], [], tmp_path / "b.json", phases=["A", "B", "C", "D"])
    assert b.task_progress(Task("t", phase="A")) == 0.0
    assert b.task_progress(Task("t", phase="B")) == pytest.approx(1 / 3)
    assert b.task_progress(Task("t", phase="D")) == 1.0
    # a phase the board doesn't know falls back to the start, never raises
    assert b.task_progress(Task("t", phase="ZZZ")) == 0.0
    # a single-phase board has no range to measure -> 0.0, no ZeroDivisionError
    single = Board([], [], tmp_path / "s.json", phases=["Only"])
    assert single.task_progress(Task("t", phase="Only")) == 0.0


def test_project_progress_is_mean_of_tasks(tmp_path):
    """WHY: this number will drive the gantt bar — it must be the mean of the
    VISIBLE tasks' progress, and an empty project must not blow up."""
    b = Board([], [], tmp_path / "b.json", phases=["A", "B", "C"])
    b.tasks = [Task("t1", "p1", "A"), Task("t2", "p1", "B"), Task("t3", "p1", "C")]
    assert b.project_progress("p1") == pytest.approx((0.0 + 0.5 + 1.0) / 3)
    b.tasks.append(Task("t4", "p1", "C", archived=True))
    assert b.project_progress("p1") == pytest.approx(0.5)          # archived excluded
    assert b.project_progress("p1", show_archived=True) == pytest.approx(0.625)
    assert b.project_progress("no-such-project") == 0.0            # empty -> 0.0


def test_blocked_task_stays_in_its_phase(tmp_path):
    """WHY: blocked is a FLAG, not a phase — a blocked task keeps its place in the
    workflow (and its marker) instead of being parked in a column of its own."""
    from taskboard.views import phase_buckets, render_columns
    b = Board.load(str(tmp_path / "b.json"))            # seeded, default phases
    stuck = Task("STUCK", None, "Doing", "normal", blocked=True)
    b.add_task(stuck)
    buckets = phase_buckets(b, b.visible_tasks(False))
    assert len(buckets) == len(b.phases)
    doing = b.phases.index("Doing")
    assert stuck.id in [t.id for t in buckets[doing]]
    assert all(stuck.id not in [t.id for t in bucket]
               for i, bucket in enumerate(buckets) if i != doing)
    out = str(render_columns(b, False, None, date(2026, 7, 17), width=120))
    assert "DOING" in out
    assert "BLOCKED" not in out              # no blocked column exists any more
    assert "▲" in out                        # the blocked marker still shows


async def test_modal_sets_phase_and_blocked_and_persists(tmp_path):
    """WHY: the editor is the only way a user changes a phase — the phase Select
    and the blocked Checkbox must reach the task and survive a reload from disk."""
    from textual.widgets import Checkbox
    board_path = str(tmp_path / "board.json")
    app = TaskboardApp(board_path=board_path)
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("a")
        await pilot.pause()
        app.screen.query_one("#f-title", Input).value = "PHASETASK"
        app.screen.query_one("#f-phase", Select).value = "Doing"
        app.screen.query_one("#f-blocked", Checkbox).value = True
        await save_open_modal(app, pilot)
        t = next(t for t in app.board.tasks if t.title == "PHASETASK")
        assert (t.phase, t.blocked) == ("Doing", True)
    t2 = next(t for t in Board.load(board_path).tasks if t.title == "PHASETASK")
    assert (t2.phase, t2.blocked) == ("Doing", True)


def test_custom_phases_drive_the_columns(tmp_path):
    """WHY: the columns view must be generated FROM the board's phases — five
    custom phases means five column headers, and the list persists to disk."""
    from taskboard.views import render_columns
    phases = ["Intake", "Design", "Build", "Review", "Shipped"]
    path = tmp_path / "custom.json"
    b = Board([], [], path, phases=phases)
    b.tasks = [Task(f"task {p}", None, p) for p in phases]
    b.save()
    assert Board.load(str(path)).phases == phases          # round-trips

    out = str(render_columns(b, False, None, date(2026, 7, 17), width=140)).split("\n")
    header_row = out[1]                                    # row under the frame title
    for p in phases:
        assert p.upper() in header_row
    assert header_row.count("│") == len(phases) + 1        # 5 columns -> 4 dividers + 2 edges
    assert all(len(l) == 140 for l in out)                 # still width-exact


async def test_view_renders_with_a_new_colour(tmp_path):
    """A project using one of the new colours renders without error."""
    from taskboard.models import Board, Project
    board_path = str(tmp_path / "board.json")
    app = TaskboardApp(board_path=board_path)
    async with app.run_test(size=(120, 40)) as pilot:
        app.board.add_project(Project(name="Cyan Proj", color="cyan"))
        app.refresh_view()
        await pilot.pause()
        assert "Cyan Proj" in board_text(app)


def test_canonical_phase_is_case_insensitive(tmp_path):
    """WHY: real boards contain 'backlog'/'done' in the wrong case. Falling back
    to phases[0] would silently demote a finished task to the first phase."""
    from taskboard.models import Board
    b = Board.load(tmp_path / "b.json")
    b.phases = ["Backlog", "Doing", "Done"]
    assert b.canonical_phase("backlog") == "Backlog"
    assert b.canonical_phase("DONE") == "Done"
    assert b.canonical_phase("  doing ") == "Doing"
    assert b.canonical_phase("Backlog") == "Backlog"
    assert b.canonical_phase("nonsense") == "Backlog"        # genuine unknown -> first


def test_load_snaps_wrong_case_phases_without_demoting(tmp_path):
    """A stored lowercase 'done' must load as Done, not be demoted to Backlog."""
    import json
    from taskboard.models import Board
    p = tmp_path / "board.json"
    p.write_text(json.dumps({
        "phases": ["Backlog", "Doing", "Done"],
        "projects": [],
        "tasks": [
            {"id": "a", "title": "lower done", "phase": "done"},
            {"id": "b", "title": "lower backlog", "phase": "backlog"},
            {"id": "c", "title": "weird", "phase": "Nope"},
        ],
        "settings": {},
    }), encoding="utf-8")
    b = Board.load(p)
    by = {t.id: t.phase for t in b.tasks}
    assert by["a"] == "Done"          # NOT demoted
    assert by["b"] == "Backlog"
    assert by["c"] == "Backlog"       # genuine unknown falls back


# --- kanban view (every task in its phase, grouped by project) -------------- #
def _kanban_board(tmp_path):
    """A board where ONE project has THREE tasks in ONE phase — the case
    swimlanes collapsed to 'first task + N more'."""
    from taskboard.models import Board, Project, Task
    b = Board.load(str(tmp_path / "k.json"))
    b.projects.clear()
    b.tasks.clear()
    alpha = Project("Alpha", "cyan", "on_track")
    beta = Project("Beta", "amber", "on_track")
    b.projects += [alpha, beta]
    b.tasks += [
        Task("KA one", alpha.id, "Backlog"),
        Task("KA two", alpha.id, "Backlog"),
        Task("KA three", alpha.id, "Backlog"),
        Task("KA doing", alpha.id, "Doing"),
        Task("KB done", beta.id, "Done"),
        Task("KB blocked", beta.id, "Doing", blocked=True),
        Task("Loose one", None, "Backlog"),
    ]
    b.save()
    return b


def test_kanban_shows_every_task_in_its_phase(tmp_path):
    """WHY: swimlanes only rendered the FIRST task of each project/phase cell and
    summarised the rest as 'N more' — this view exists to show them ALL."""
    from taskboard.views import render_kanban
    b = _kanban_board(tmp_path)
    out = str(render_kanban(b, False, None, date(2026, 7, 17), width=160, height=0))
    for title in ("KA one", "KA two", "KA three", "KA doing", "KB done", "Loose one"):
        assert title in out, f"{title} missing from the kanban render"


def test_kanban_groups_by_project(tmp_path):
    """Each phase column groups its tasks under a per-project header line."""
    from taskboard.views import render_kanban, _phase_window, distribute
    b = _kanban_board(tmp_path)
    w = 160
    lines = str(render_kanban(b, False, None, date(2026, 7, 17),
                              width=w, height=0)).split("\n")
    start, widths = _phase_window(b, w - 2, None)
    assert start == 0 and len(widths) == len(b.phases)
    col0 = [l[1:1 + widths[0]] for l in lines]          # the Backlog column only
    assert any("Alpha" in cell for cell in col0)         # project header present
    assert any("Inbox" in cell for cell in col0)         # project-less group
    # …and the header sits ABOVE that project's three tasks in the same column
    hdr = next(i for i, cell in enumerate(col0) if "Alpha" in cell)
    tasks = [i for i, cell in enumerate(col0) if "KA one" in cell or "KA three" in cell]
    assert tasks and all(i > hdr for i in tasks)


def test_kanban_marks_blocked_without_moving_it(tmp_path):
    """A blocked task keeps its own phase (blocked is a flag, not a column) and
    carries the ▲ marker."""
    from taskboard.views import render_kanban, _phase_window
    b = _kanban_board(tmp_path)
    w = 160
    lines = str(render_kanban(b, False, None, date(2026, 7, 17),
                              width=w, height=0)).split("\n")
    start, widths = _phase_window(b, w - 2, None)
    doing = b.phases.index("Doing")
    off = 1 + sum(widths[:doing]) + doing                # 1 border + prior cols + seps
    cells = [l[off:off + widths[doing]] for l in lines]
    row = next(cell for cell in cells if "KB blocked" in cell)
    assert "▲" in row
    assert not any("KB blocked" in l[1:1 + widths[0]] for l in lines)   # not moved


def test_kanban_matrix_shows_progress_percent(tmp_path):
    from taskboard.views import render_kanban
    b = _kanban_board(tmp_path)
    alpha = next(p for p in b.projects if p.name == "Alpha")
    expected = int(round(100 * b.project_progress(alpha.id)))
    out = str(render_kanban(b, False, None, date(2026, 7, 17), width=160, height=0,
                            presentation="matrix"))
    row = next(l for l in out.split("\n") if "Alpha" in l)
    assert f"{expected}%" in row
    assert "prog" in out


async def test_tab_toggles_kanban_presentation(tmp_path):
    app = make_app(tmp_path)
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("5")
        assert "grouped" in board_text(app)
        assert "prog" not in board_text(app)
        await pilot.press("tab")
        assert app.kanban_presentation == "matrix"
        assert "prog" in board_text(app)        # only the matrix has a prog column
        await pilot.press("tab")
        assert app.kanban_presentation == "grouped"
        assert "prog" not in board_text(app)


def test_kanban_width_exact_across_widths(tmp_path):
    from taskboard.views import render_kanban
    b = _kanban_board(tmp_path)
    sel = b.tasks[0].id
    for w in (40, 68, 100, 140):
        for pres in ("grouped", "matrix"):
            lines = str(render_kanban(b, False, sel, date(2026, 7, 17), width=w,
                                      height=0, presentation=pres)).split("\n")
            assert all(len(l) == w for l in lines), f"{pres} at {w}: a line != {w}"


def test_kanban_windows_phases_when_they_dont_fit(tmp_path):
    """8 phases can't fit at 40 cells with a 12-cell floor: render the window
    that fits and say how many phases are hidden."""
    from taskboard.views import render_kanban, _phase_window
    b = _kanban_board(tmp_path)
    b.phases = [f"Phase{i}" for i in range(8)]
    for t in b.tasks:
        t.phase = b.phases[0]
    b.tasks[0].phase = b.phases[7]
    start, widths = _phase_window(b, 38, b.tasks[0])     # width 40 -> inner 38
    assert len(widths) == 3 and all(wc >= 12 for wc in widths)
    assert start + len(widths) == 8                      # window followed the selection
    out = str(render_kanban(b, False, b.tasks[0].id, date(2026, 7, 17), width=40, height=0))
    assert "PHASE7" in out and "PHASE0" not in out       # only the window is drawn
    assert "◀ 5" in out                                  # 5 phases hidden to the left
    out0 = str(render_kanban(b, False, b.tasks[1].id, date(2026, 7, 17), width=40, height=0))
    assert "5 ▶" in out0                                 # …and to the right at the start

# --- gantt project bar (dual-density braille + honest due figure) ----------- #
GANTT_TODAY = date(2026, 7, 20)          # a Monday, so week 0 starts on it
DENSE, HALF = "⣿", "⢕"        # the two bar glyphs
BANNED = ("⣤", "⡀", "░", "▒")   # textures that lose height


def _gantt_board(tmp_path):
    """Phases [A, B, C]. Alpha sits at 50% (one task in A, one in C) and has a
    due date; Beta sits at 0% (both tasks in A) and has NO due date."""
    from taskboard.models import Board, Project, Task
    b = Board([], [], tmp_path / "g.json", phases=["A", "B", "C"])
    alpha = Project("Alpha", "cyan", start_date="2026-07-20", due_date="2026-08-17")
    beta = Project("Beta", "amber", start_date="2026-07-20", due_date=None)
    b.projects += [alpha, beta]
    b.tasks += [
        Task("A first", alpha.id, "A", start_date="2026-07-20", due_date="2026-07-27"),
        Task("A last", alpha.id, "C", start_date="2026-07-27", due_date="2026-08-10"),
        Task("B one", beta.id, "A", start_date="2026-07-20", due_date="2026-08-03"),
        Task("B two", beta.id, "A", start_date="2026-07-20", due_date="2026-08-03"),
    ]
    return b


def _gantt_rows(board, width=68):
    return str(render_gantt(board, False, None, today=GANTT_TODAY,
                            width=width, height=0)).splitlines()


def _project_row(board, name, width=68):
    return next(l for l in _gantt_rows(board, width) if name in l)


def test_gantt_bar_uses_dual_density_braille(tmp_path):
    """WHY: the project span must read as ONE bar of constant height — the
    completed share differs by DOT DENSITY, not by a shorter/bottom-weighted
    glyph, which is what made the old solid block look like it lost height."""
    b = _gantt_board(tmp_path)
    row = _project_row(b, "Alpha")
    assert DENSE in row and HALF in row
    out = "".join(_gantt_rows(b))
    for bad in BANNED:
        assert bad not in out, f"{bad!r} is a height-breaking texture"


def test_gantt_bar_split_follows_phase_progress(tmp_path):
    """WHY: the split is the PHASE WEIGHT (one task in A + one in C -> 0.5), not
    a done/total count — otherwise a two-task project could only ever read
    0/50/100% and would ignore the middle of the workflow."""
    b = _gantt_board(tmp_path)
    alpha = next(p for p in b.projects if p.name == "Alpha")
    assert b.project_progress(alpha.id) == pytest.approx(0.5)
    row = _project_row(b, "Alpha")
    done, todo = row.count(DENSE), row.count(HALF)
    total = done + todo
    assert total > 0
    assert abs(done - b.project_progress(alpha.id) * total) <= 1     # ±1 rounding


def test_gantt_bar_extremes(tmp_path):
    """0% draws no dense cell and 100% draws no half cell — the bar still spans
    the same width in both cases."""
    b = _gantt_board(tmp_path)
    beta = next(p for p in b.projects if p.name == "Beta")
    beta.due_date = "2026-08-17"                        # same span as Alpha
    beta_row = _project_row(b, "Beta")
    assert DENSE not in beta_row and HALF in beta_row

    alpha = next(p for p in b.projects if p.name == "Alpha")
    for t in [t for t in b.tasks if t.project_id == alpha.id]:
        t.phase = "C"                                   # everything in the last phase
    alpha_row = _project_row(b, "Alpha")
    assert HALF not in alpha_row and DENSE in alpha_row
    assert alpha_row.count(DENSE) == beta_row.count(HALF)   # same span, same width


def test_gantt_shows_due_days_not_invented_estimate(tmp_path):
    """WHY: we store no phase-transition timestamps, so a velocity ETA is not
    computable. The trailing figure is the project's own due-date distance, and
    a project without a due date gets a placeholder — never a fabricated number.
    Rendered WIDE on purpose: the due figure only exists above META_FULL_INNER."""
    b = _gantt_board(tmp_path)
    wide = META_FULL_INNER + 2                          # inner == META_FULL_INNER
    assert "due 28d" in _project_row(b, "Alpha", wide)   # 2026-07-20 -> 2026-08-17

    beta_row = _project_row(b, "Beta", wide)
    assert "—" in beta_row                          # dim em-dash placeholder
    assert "due" not in beta_row
    assert not re.search(r"\d+d", beta_row)              # no invented day figure

    beta = next(p for p in b.projects if p.name == "Beta")
    beta.due_date = "2026-07-13"                        # a week overdue
    assert "due -7d" in _project_row(b, "Beta", wide)


def test_gantt_divides_projects(tmp_path):
    """One divider BETWEEN project blocks — none before the first or after the
    last, so N projects give exactly N-1 dividers."""
    from taskboard.models import Project
    b = _gantt_board(tmp_path)
    rows = _gantt_rows(b)
    dividers = [l for l in rows if "┈" in l]
    assert len(dividers) == len(b.projects) - 1 == 1
    assert all(l.count("┈") == 68 - 2 for l in dividers)      # full-width row

    b.projects.append(Project("Gamma", "lime", start_date="2026-07-20",
                              due_date="2026-08-03"))
    assert len([l for l in _gantt_rows(b) if "┈" in l]) == len(b.projects) - 1 == 2


def test_gantt_width_exact_across_widths(tmp_path):
    b = _gantt_board(tmp_path)
    sel = b.tasks[0].id
    for w in (40, 68, 100, 140):
        lines = str(render_gantt(b, False, sel, today=GANTT_TODAY,
                                 width=w, height=0)).splitlines()
        assert all(len(l) == w for l in lines), f"gantt at {w}: a line != {w}"


# --- phase editor (increment 5) -------------------------------------------- #
def _phase_board(tmp_path, phases=("A", "B", "C"), tasks=None) -> Board:
    """Board with an explicit phase list, saved to tmp_path (never ~/.taskboard)."""
    b = Board([], list(tasks or []), tmp_path / "board.json", phases=list(phases))
    b.save()
    return b


def test_add_phase_rejects_blank_and_duplicates(tmp_path):
    """WHY: a blank or case-variant phase would produce two rows that look like
    one workflow step, and canonical_phase() resolves case-insensitively — so a
    'doing' next to 'Doing' would make task placement ambiguous."""
    b = _phase_board(tmp_path, ("Backlog", "Doing", "Done"))
    before = list(b.phases)

    assert b.add_phase("   ") is False
    assert b.phases == before
    assert b.add_phase("dOiNg") is False               # case-variant duplicate
    assert b.phases == before

    assert b.add_phase("  Review  ") is True           # stored stripped
    assert b.phases == before + ["Review"]


def test_rename_phase_moves_its_tasks(tmp_path):
    """WHY (the critical one): the phase list and task.phase are joined BY NAME.
    Renaming only the list would leave every task pointing at a name the board
    no longer knows, and Board.load() falls back to phases[0] — silently
    demoting finished work to the backlog."""
    tasks = [Task("t1", None, "B"), Task("t2", None, "B"), Task("keep", None, "C")]
    b = _phase_board(tmp_path, ("A", "B", "C"), tasks)
    moved = [t.id for t in b.tasks if t.phase == "B"]
    assert len(moved) == 2                              # precondition

    assert b.rename_phase("B", "Building") is True
    assert b.phases == ["A", "Building", "C"]
    assert all(b.task_by_id(i).phase == "Building" for i in moved)
    assert not any(t.phase == "B" for t in b.tasks)     # nothing left behind
    b.save()

    reloaded = Board.load(b.path)                       # on-disk oracle
    assert reloaded.phases == ["A", "Building", "C"]
    assert all(reloaded.task_by_id(i).phase == "Building" for i in moved)
    assert reloaded.task_by_id(tasks[2].id).phase == "C"        # untouched


def test_delete_phase_reassigns_tasks_and_never_loses_them(tmp_path):
    """WHY: deleting a workflow step must not delete the work sitting in it —
    its tasks fall back to the previous phase, the least-destructive choice."""
    tasks = [Task("a", None, "A"), Task("b1", None, "B"), Task("b2", None, "B"),
             Task("c", None, "C")]
    b = _phase_board(tmp_path, ("A", "B", "C"), tasks)

    assert b.delete_phase("B") is True
    assert b.phases == ["A", "C"]
    assert len(b.tasks) == 4                            # nothing lost
    assert [t.phase for t in b.tasks] == ["A", "A", "A", "C"]


def test_delete_last_phase_is_refused(tmp_path):
    """WHY: progress, the kanban columns and the gantt all index into phases —
    an empty list would leave every task pointing nowhere."""
    b = _phase_board(tmp_path, ("Only",), [Task("solo", None, "Only")])

    assert b.delete_phase("Only") is False
    assert b.phases == ["Only"]
    assert len(b.tasks) == 1 and b.tasks[0].phase == "Only"


def test_move_phase_reorders_and_changes_progress(tmp_path):
    """WHY: progress is POSITIONAL, so reordering is the operation that changes
    how far along a task reads — without touching any task's phase name."""
    task = Task("t", None, "C")
    b = _phase_board(tmp_path, ("A", "B", "C"), [task])
    assert b.task_progress(task) == pytest.approx(1.0)   # last of three

    assert b.move_phase("C", -1) is True
    assert b.phases == ["A", "C", "B"]
    assert task.phase == "C"                             # name untouched
    assert b.task_progress(task) == pytest.approx(0.5)

    before = list(b.phases)
    assert b.move_phase("A", -1) is False                # past the front
    assert b.move_phase("B", 1) is False                 # past the end
    assert b.move_phase("nope", 1) is False              # unknown phase
    assert b.phases == before


async def test_phase_editor_opens_and_lists_phases(tmp_path):
    """f opens the editor and every board phase gets exactly one row."""
    app = make_app(tmp_path)
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("f")
        await pilot.pause()
        assert isinstance(app.screen, PhaseEditor)
        ol = app.screen.query_one("#phase-list", OptionList)
        assert ol.option_count == len(app.board.phases)
        prompts = [str(ol.get_option_at_index(i).prompt) for i in range(ol.option_count)]
        for name in app.board.phases:
            assert any(name in pr for pr in prompts)


async def test_phase_editor_reorder_key_moves_phase(tmp_path):
    """']' moves the highlighted phase one step later, the board is saved
    immediately (on-disk oracle) and the highlight follows the phase."""
    board_path = str(tmp_path / "board.json")
    app = TaskboardApp(board_path=board_path)
    async with app.run_test(size=(120, 40)) as pilot:
        original = list(app.board.phases)
        assert len(original) >= 2                       # precondition
        await pilot.press("f")
        await pilot.pause()
        app.screen.query_one("#phase-list", OptionList).highlighted = 0
        await pilot.press("right_square_bracket")
        await pilot.pause()
        expected = [original[1], original[0]] + original[2:]
        assert app.board.phases == expected
        assert app.screen.query_one("#phase-list", OptionList).highlighted == 1
    assert Board.load(board_path).phases == expected     # persisted


def _phase_app(tmp_path, phases=("A", "B", "C"), tasks=None) -> TaskboardApp:
    """App over a board with an explicit phase list, on disk in tmp_path."""
    board = _phase_board(tmp_path, phases, tasks)
    return TaskboardApp(board_path=str(board.path))


async def test_phase_editor_add_via_prompt(tmp_path):
    """WHY: the editor's 'a' only opens a prompt — the phase does not exist until
    the prompt's callback runs AND the board is saved. Both halves are asserted,
    the second against the file on disk."""
    board_path = str(tmp_path / "board.json")
    app = TaskboardApp(board_path=board_path)
    async with app.run_test(size=(120, 40)) as pilot:
        before = list(app.board.phases)
        await pilot.press("f")
        await pilot.pause()
        await pilot.press("a")
        await pilot.pause()
        assert isinstance(app.screen, modals.TextPrompt)
        app.screen.query_one("#f-text", Input).value = "Review"
        await save_open_modal(app, pilot)
        await pilot.pause()
        assert app.board.phases == before + ["Review"]
        assert isinstance(app.screen, PhaseEditor)          # editor stays open
    assert Board.load(board_path).phases == before + ["Review"]


async def test_phase_editor_rename_moves_tasks_through_the_ui(tmp_path):
    """WHY: renaming from the editor must carry the tasks with it. The model does
    that, but only if the editor hands it the OLD name of the HIGHLIGHTED row —
    pass the wrong one and the tasks keep a name the board no longer knows, so
    the next load demotes them to phases[0]. Driven through the real widgets and
    checked after a reload, which is where such an orphan would show up."""
    app = _phase_app(tmp_path, ("A", "B", "C"),
                     [Task("t1", None, "B"), Task("t2", None, "B"),
                      Task("keep", None, "C")])
    board_path = app.board.path
    async with app.run_test(size=(120, 40)) as pilot:
        moved = [t.id for t in app.board.tasks if t.phase == "B"]
        kept = next(t.id for t in app.board.tasks if t.phase == "C")
        assert len(moved) == 2                              # precondition
        await pilot.press("f")
        await pilot.pause()
        app.screen.query_one("#phase-list", OptionList).highlighted = 1
        await pilot.press("e")                              # rename the highlighted phase
        await pilot.pause()
        assert app.screen.query_one("#f-text", Input).value == "B"   # prefilled
        app.screen.query_one("#f-text", Input).value = "Building"
        await save_open_modal(app, pilot)
        await pilot.pause()
        assert app.board.phases == ["A", "Building", "C"]
        assert all(app.board.task_by_id(i).phase == "Building" for i in moved)
        assert not any(t.phase == "B" for t in app.board.tasks)

    reloaded = Board.load(board_path)                       # on-disk oracle
    assert reloaded.phases == ["A", "Building", "C"]
    assert all(reloaded.task_by_id(i).phase == "Building" for i in moved)
    assert reloaded.task_by_id(kept).phase == "C"           # untouched


async def test_phase_editor_add_rejects_duplicate(tmp_path):
    """WHY: the prompt returns free text, so the editor is the last gate before a
    case-variant twin of an existing phase reaches the board."""
    app = _phase_app(tmp_path, ("Backlog", "Doing", "Done"))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("f")
        await pilot.pause()
        await pilot.press("a")
        await pilot.pause()
        app.screen.query_one("#f-text", Input).value = "backlog"
        await save_open_modal(app, pilot)
        await pilot.pause()
        assert app.board.phases == ["Backlog", "Doing", "Done"]
        assert isinstance(app.screen, PhaseEditor)
        assert app.screen.query_one("#phase-list", OptionList).option_count == 3


async def test_phase_editor_prompt_cancel_is_a_noop(tmp_path):
    """WHY: TextPrompt dismisses with None on escape and "" on an empty save —
    the editor must treat cancel as "changed my mind", not as a blank phase."""
    app = _phase_app(tmp_path, ("Backlog", "Doing", "Done"))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("f")
        await pilot.pause()
        await pilot.press("a")
        await pilot.pause()
        assert isinstance(app.screen, modals.TextPrompt)
        await pilot.press("escape")
        await pilot.pause()
        assert app.board.phases == ["Backlog", "Doing", "Done"]
        assert isinstance(app.screen, PhaseEditor)          # back to the editor


async def test_phase_editor_delete_reassigns_through_the_ui(tmp_path):
    """WHY: deleting a workflow step from the editor must not delete the work in
    it. The confirm dialog is part of the path — the tasks only move once it
    returns True — so the whole flow is driven, not just the model call."""
    app = _phase_app(tmp_path, ("A", "B", "C"),
                     [Task("a", None, "A"), Task("b1", None, "B"),
                      Task("b2", None, "B"), Task("c", None, "C")])
    async with app.run_test(size=(120, 40)) as pilot:
        moved = [t.id for t in app.board.tasks if t.phase == "B"]
        assert len(moved) == 2                              # precondition
        await pilot.press("f")
        await pilot.pause()
        app.screen.query_one("#phase-list", OptionList).highlighted = 1
        await pilot.press("d")
        await pilot.pause()
        assert isinstance(app.screen, modals.ConfirmModal)
        app.screen.query_one("#yes", Button).press()
        await pilot.pause()
        await pilot.pause()
        assert app.board.phases == ["A", "C"]
        assert len(app.board.tasks) == 4                    # nothing lost
        assert all(app.board.task_by_id(i).phase == "A" for i in moved)


async def test_phase_editor_refuses_deleting_the_last_phase(tmp_path):
    """WHY: every view indexes into phases, so an empty list would leave the task
    pointing nowhere. The editor must refuse before even asking to confirm."""
    app = _phase_app(tmp_path, ("Only",), [Task("solo", None, "Only")])
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("f")
        await pilot.pause()
        app.screen.query_one("#phase-list", OptionList).highlighted = 0
        await pilot.press("d")
        await pilot.pause()
        assert isinstance(app.screen, PhaseEditor)          # no confirm was pushed
        assert app.board.phases == ["Only"]
        assert len(app.board.tasks) == 1
        assert app.board.tasks[0].phase == "Only"


async def test_phase_name_with_markup_is_escaped(tmp_path):
    """WHY: phase names are user text and the editor's rows are markup — an
    unescaped '[red]' would either vanish as a tag or raise MarkupError while the
    list builds (pitfall A1)."""
    app = _phase_app(tmp_path, ("[red]boom[/red]", "Done"),
                     [Task("t", None, "[red]boom[/red]")])
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("f")
        await pilot.pause()
        ol = app.screen.query_one("#phase-list", OptionList)
        prompts = [str(ol.get_option_at_index(i).prompt) for i in range(ol.option_count)]
        assert any("\\[red]boom\\[/red]" in pr for pr in prompts)


async def test_phase_editor_reorder_left_and_boundaries(tmp_path):
    """WHY: '[' is the mirror of ']' and shares its persistence path, but the
    FIRST row has nowhere earlier to go. move_phase returns False there, and the
    editor must treat that as a no-op — not save a reordering that never happened
    and not raise while re-highlighting an index that moved out of range."""
    app = _phase_app(tmp_path, ("A", "B", "C"))
    board_path = app.board.path
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("f")
        await pilot.pause()
        app.screen.query_one("#phase-list", OptionList).highlighted = 2   # not first
        await pilot.press("left_square_bracket")
        await pilot.pause()
        assert app.board.phases == ["A", "C", "B"]
        assert app.screen.query_one("#phase-list", OptionList).highlighted == 1
        assert Board.load(board_path).phases == ["A", "C", "B"]     # persisted

        app.screen.query_one("#phase-list", OptionList).highlighted = 0   # the first
        await pilot.press("left_square_bracket")
        await pilot.pause()
        assert app.board.phases == ["A", "C", "B"]                  # unchanged
        assert isinstance(app.screen, PhaseEditor)                  # still usable
    assert Board.load(board_path).phases == ["A", "C", "B"]


async def test_phase_editor_blank_name_is_rejected(tmp_path):
    """WHY: TextPrompt dismisses an empty Save with "" (cancel is None), so the
    editor sees a real callback carrying a nameless phase. A blank row would be
    an unclickable, unnameable workflow step that every view still indexes into."""
    app = _phase_app(tmp_path, ("Backlog", "Doing", "Done"))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("f")
        await pilot.pause()
        await pilot.press("a")
        await pilot.pause()
        assert isinstance(app.screen, modals.TextPrompt)
        app.screen.query_one("#f-text", Input).value = "   "        # blank once stripped
        await save_open_modal(app, pilot)
        await pilot.pause()
        assert app.board.phases == ["Backlog", "Doing", "Done"]
        assert isinstance(app.screen, PhaseEditor)                  # back, no crash
        assert app.screen.query_one("#phase-list", OptionList).option_count == 3
