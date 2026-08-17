"""Pilot tests that prove the app actually works (assert rendered content)."""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path

import pytest

from textual.widgets import Button, Input, OptionList, Select, Static, TextArea

from taskboard import models, modals
from taskboard.app import BoardView, TaskboardApp
from taskboard.models import Board, Project, Task
from taskboard.modals import (CalendarModal, PhaseEditor, TaskDetails, TaskModal,
                              image_block)
from taskboard.ribbon import Ribbon
from taskboard.views import (META_FULL_INNER, META_FULL_W, METER_W,
                             render_agenda, render_gantt)


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


def test_the_retired_view_is_gone_from_the_code_entirely():
    """Columns was retired: kanban is the same phase grid, better drawn, and the
    audit found columns had no capability of its own. A half-retirement — a
    renderer nobody can reach, a nav branch nobody calls — is worse than either
    keeping it or removing it, so this asserts there is no residue."""
    import pathlib
    from taskboard import views
    from taskboard.keymap import KEYMAP, VIEWS
    assert "columns" not in VIEWS
    assert "columns" not in views.RENDERERS
    for name in ("render_columns", "_column_card", "heat_cell"):
        assert not hasattr(views, name), f"{name} survived the retirement"
    assert not any("columns" in k.action for k in KEYMAP)
    src = pathlib.Path(views.__file__).read_text(encoding="utf-8")
    assert "columns" not in src.lower().replace("dot_columns", "").replace(
        "dot columns", "").replace("column", "")


async def test_two_now_opens_agenda(tmp_path):
    """The renumbering, stated as a fact a test can hold: 1-5, no gap."""
    from taskboard.app import VIEW_KEYS, VIEW_ORDER
    assert VIEW_ORDER == ["swimlanes", "agenda", "gantt", "kanban", "focus"]
    assert VIEW_KEYS == {"1": "swimlanes", "2": "agenda", "3": "gantt",
                         "4": "kanban", "5": "focus"}
    app = make_app(tmp_path)
    async with app.run_test() as pilot:
        await pilot.press("2")
        assert app.view_mode == "agenda"
        assert "AGENDA" in board_text(app)


async def test_the_renumbering_is_announced_exactly_once(tmp_path):
    """Moving `2` in silence is the same sin as hiding a key — so it is said.
    And said ONCE: a notice that returns every launch becomes noise the user
    learns to dismiss without reading."""
    from taskboard.app import RENUMBER_NOTICE_KEY, TaskboardApp
    board_path = str(tmp_path / "board.json")
    seen = []
    app = TaskboardApp(board_path=board_path)
    app.notify = lambda *a, **k: seen.append(k.get("title", ""))
    async with app.run_test() as pilot:
        await pilot.pause()
    assert [t for t in seen if "renumber" in t.lower()], "the renumbering was silent"
    assert Board.load(board_path).settings.get(RENUMBER_NOTICE_KEY) is True

    again = TaskboardApp(board_path=board_path)     # a second launch, same board
    seen2 = []
    again.notify = lambda *a, **k: seen2.append(k.get("title", ""))
    async with again.run_test() as pilot:
        await pilot.pause()
    assert not [t for t in seen2 if "renumber" in t.lower()], "it said it twice"


async def test_all_four_views_switch(tmp_path):
    app = make_app(tmp_path)
    async with app.run_test() as pilot:
        await pilot.press("1")
        assert "TASKBOARD" in board_text(app)   # swimlanes
        await pilot.press("2")
        assert "AGENDA" in board_text(app)       # agenda
        await pilot.press("3")
        assert "GANTT" in board_text(app)        # gantt
        await pilot.press("4")
        assert "KANBAN" in board_text(app)       # kanban
        await pilot.press("5")
        assert "FOCUS" in board_text(app)        # focus


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


async def test_clock_modal_finds_an_accented_city_from_an_ascii_keyboard(tmp_path):
    """End to end through the real picker, with the widened catalog: he types
    what his keyboard gives him and the ribbon shows the city as it is spelled.
    (Also the smoke that the 340-city suggester still drives the modal.)"""
    board_path = str(tmp_path / "board.json")
    app = TaskboardApp(board_path=board_path)
    async with app.run_test() as pilot:
        await pilot.press("c")
        await pilot.pause()
        app.screen.query_one("#f-clock1", Input).value = "sao paulo"
        app.screen.query_one("#f-clock2", Input).value = "Kathmandu"   # UTC+5:45
        app.screen.query_one("#save", Button).press()
        await pilot.pause()
        assert app.board.get_clocks() == ("São Paulo", "Kathmandu")
        assert "São Paulo" in str(app.query_one("#ribbon", Ribbon).render())
    assert Board.load(board_path).get_clocks() == ("São Paulo", "Kathmandu")


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
    false-positive class — the ribbon can render text while being invisible.
    (The bottom row is now our own KeyBar; Textual's Footer rendered blank.)"""
    from taskboard.keymap import KeyBar
    app = make_app(tmp_path)
    async with app.run_test(size=(120, 35)) as pilot:
        await pilot.pause()
        ribbon = app.query_one("#ribbon", Ribbon)
        footer = app.query_one("#keybar", KeyBar)
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


async def test_right_moves_to_next_column_first_task(tmp_path):
    from taskboard.views import nav_model
    app = make_app(tmp_path)
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.pause()
        await pilot.press("4")
        cols = nav_model("kanban", app.board, False)
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
        await pilot.press("4")
        cols = nav_model("kanban", app.board, False)
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
        await pilot.press("2")   # agenda
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
        await pilot.press("2")   # agenda (linear, taller than 18 rows)
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


def _columns_body(board, today, width=100):
    """The task-bearing body rows of the columns view (between the ├─┤ divider
    and the ╰──╯ bottom): index 3 .. -1 of the rendered lines."""
    from taskboard.views import render_kanban
    rows = str(render_kanban(board, False, None, today, width=width, height=0)).split("\n")
    return rows, rows[3:-1]


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
        await pilot.press("2")  # agenda shows titles wide enough
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


def test_task_depends_on_model(tmp_path):
    """TC-00X (LLR-001.1/001.2): default_factory list + round-trip for task dependencies."""
    from taskboard.models import Board, Task
    assert Task("t").depends_on == []
    assert Task("a").depends_on is not Task("b").depends_on
    assert Task.from_dict({"title": "x", "depends_on": ["a", "b"]}).depends_on == ["a", "b"]
    assert Task.from_dict({"title": "x"}).depends_on == []
    assert Task.from_dict({"title": "x", "depends_on": "nope"}).depends_on == []
    p = str(tmp_path / "b.json")
    board = Board.load(p)
    board.add_task(Task("child", None, "Backlog", "normal", depends_on=["p1", "p2"]))
    t = next(t for t in Board.load(p).tasks if t.title == "child")
    assert t.depends_on == ["p1", "p2"]


async def test_open_images_allowlist_and_isfile(tmp_path, monkeypatch):
    """TC-007c (LLR-007.3): os.startfile fires ONLY for an existing image-ext
    local file; missing files, non-image extensions, UNC and file:// are all
    refused (never executed, never crash)."""
    real = tmp_path / "ok.png"
    real.write_bytes(b"x")
    app = make_app(tmp_path)
    async with app.run_test() as pilot:
        started = []
        monkeypatch.setattr("taskboard.app.os.startfile", started.append,
                        raising=False)   # absent off Windows; see line ~848
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
        # the card renders the width-1 image glyph, lines stay width-exact.
        # (kanban, not columns: the one-line columns redesign drops card_cell's
        # ▤/↗/◉ indicators; kanban still renders them through the same helper.)
        app.selected_task_id = task.id
        await pilot.press("4")
        text = board_text(app)
        assert "▤" in text
        # every rendered line is the same width -> the glyph is single-cell
        assert len({len(l) for l in text.split("\n") if l}) == 1
        # pressing the actual `i` binding routes each ref safely
        started, browsed = [], []
        monkeypatch.setattr("taskboard.app.os.startfile", started.append,
                        raising=False)   # absent off Windows; see line ~848
        monkeypatch.setattr("taskboard.app.webbrowser.open", browsed.append)
        app.open_all_images_raw(app.selected_task)
        assert started == [str(real_png)]                       # existing image only
        assert browsed == ["https://pics.example.com/a.png"]    # the http image URL
        assert str(svg) not in started and str(exe) not in started
        assert str(missing) not in started


async def test_markup_injection_is_escaped(tmp_path):
    """A title full of markup must render literally, never crash (pitfall A1)."""
    app = make_app(tmp_path)
    async with app.run_test(size=(120, 60)) as pilot:
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
    """Was: undated tasks were listed under an UNSCHEDULED heading. The field
    has no separate section — an undated task draws its row like any other, with
    an empty reach and a meter that says there is NOTHING TO MEASURE rather than
    implying a date. It is still on screen, which is what the law was for."""
    from taskboard.views import METER_W
    board = Board.load(str(tmp_path / "b.json"))  # seeded
    board.add_task(Task("floating task", None, "Backlog", "normal"))
    out = str(render_gantt(board, False, None, today=date(2026, 7, 17),
                           width=120, height=60))
    assert "GANTT" in out
    assert "floating task" in out
    row = next(l for l in out.splitlines() if "floating task" in l)
    # the edge SAYS there is nothing to measure instead of drawing an empty bar
    assert row[-METER_W:].strip("·") == "—"


def test_agenda_handles_undated_tasks(tmp_path):
    board = Board.load(str(tmp_path / "b.json"))
    board.add_task(Task("no due date task", None, "Backlog", "normal"))
    out = str(render_agenda(board, False, None, today=date(2026, 7, 17)))
    assert "AGENDA" in out
    assert "no date" in out          # undated tasks collect under the 'no date' group


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


def _ps(*args):
    import subprocess
    return subprocess.run(["powershell", "-NoProfile", "-Command", *args],
                          capture_output=True, text=True)


def _ps_literal(s: str) -> str:
    """`s` as a PowerShell single-quoted literal (a `'` is escaped by doubling).

    Needed because `-Command` joins its arguments into ONE command line, so
    passing a value with spaces as separate argv elements makes PowerShell read
    the words after the first as POSITIONAL parameters and fail. The original
    test did exactly that in its `finally`, unchecked -- which means its restore
    failed on any clipboard content containing a space, i.e. almost always, and
    it had been leaving its own sample string in the operator's clipboard on
    every run."""
    return "'" + s.replace("'", "''") + "'"


def _clipboard_now() -> str:
    """What the clipboard holds according to PowerShell — an oracle INDEPENDENT
    of the code under test (ctypes/Win32 here, .NET there). `-Raw` keeps
    multi-line content intact; stdout still appends one newline of its own."""
    return _ps("Get-Clipboard -Raw").stdout.rstrip("\r\n")


def test_win_clipboard_roundtrip():
    """Proves the 64-bit handle fix on real Windows: a string put on the clipboard
    reads back intact (the truncated-handle bug returned None or garbage).

    THIS TEST WAS FLAKY AND THE FLAKINESS WAS ITS OWN, NOT THE CODE'S. It wrote
    to the machine-global clipboard and asserted the exact string came back, so
    any other process copying anything in that window turned it red — and the
    red accused `grab_clipboard_text` of the very bug it was written to guard,
    because an empty clipboard returns None and `assert None == sample` reads
    exactly like a regression. Measured 2026-08-07: it failed once inside a full
    suite run and passed 3/3 in isolation.

    Three separate defects, all in the test:

      1. `check=False` on its own `Set-Clipboard`, so a FAILED SETUP was
         reported as a failed assertion about the app.
      2. The restore ran `Set-Clipboard -Value ''` whenever the clipboard had
         been empty — which errors with "Value cannot be null" and, being
         unchecked too, silently left the sample string in the operator's
         clipboard. `$null | Set-Clipboard` is the form that empties it;
         `Clear-Clipboard` does not exist in Windows PowerShell 5.1.
      3. `prior` came from `Get-Clipboard` STDOUT, so restoring appended a
         newline to whatever the operator had copied.

    The race is closed by ORDER, not by sleeping: read with our code FIRST, then
    ask the oracle. If the oracle still sees the sample after our read, nothing
    moved during it. If it does not, the clipboard was contended and the attempt
    is retried rather than blamed on the app. Sustained contention fails loudly
    and says so, which is a different sentence from "the roundtrip is broken."
    """
    import sys
    if sys.platform != "win32":
        pytest.skip("windows clipboard path only")
    prior = _clipboard_now()
    sample = "roundtrip 123 ABC taskboard"
    try:
        for _ in range(5):
            setup = _ps(f"Set-Clipboard -Value {_ps_literal(sample)}")
            assert setup.returncode == 0, (
                "SETUP failed — this is the environment, not the code under "
                f"test: {setup.stderr.strip()!r}")
            ours = models.grab_clipboard_text()          # our reader first...
            if _clipboard_now() != sample:               # ...then confirm it held
                continue
            assert ours == sample, (
                "the clipboard held the sample and grab_clipboard_text did not "
                f"return it: {ours!r} — this IS the handle bug")
            return
        pytest.fail("another process held the clipboard on all 5 attempts; "
                    "grab_clipboard_text was never given a stable value to read")
    finally:
        if prior:
            _ps(f"Set-Clipboard -Value {_ps_literal(prior)}")
        else:
            _ps("$null | Set-Clipboard")


# ---- project palette (8 colours, after the ration) ----------------------- #
def test_palette_has_eight_and_keeps_the_lawful_originals():
    """Was: twelve colours, "the 5 originals survive with their exact hex".

    The colour ration (Prism increment 1) retired four of them — amber, cyan,
    orange, rose — because each is confusable with a hue that JUDGES (see
    test_palette_ration.py for the measured oracle). What this test still
    guarantees is the other half of the old promise: a surviving colour keeps
    its exact hex, so a project saved as `sky` looks unchanged."""
    from taskboard.models import PROJECT_COLORS
    from taskboard.views import HEX
    assert len(PROJECT_COLORS) == 8
    assert len(set(PROJECT_COLORS)) == 8                  # no duplicates
    for name in ("violet", "sky", "green"):
        assert name in PROJECT_COLORS
    for name in ("amber", "rose", "orange", "cyan"):
        assert name not in PROJECT_COLORS
    assert HEX["violet"] == "#a78bfa"
    assert HEX["sky"] == "#38bdf8"
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
    from taskboard.views import phase_buckets, render_kanban
    b = Board.load(str(tmp_path / "b.json"))            # seeded, default phases
    stuck = Task("STUCK", None, "Doing", "normal", blocked=True)
    b.add_task(stuck)
    buckets = phase_buckets(b, b.visible_tasks(False))
    assert len(buckets) == len(b.phases)
    doing = b.phases.index("Doing")
    assert stuck.id in [t.id for t in buckets[doing]]
    assert all(stuck.id not in [t.id for t in bucket]
               for i, bucket in enumerate(buckets) if i != doing)
    out = str(render_kanban(b, False, None, date(2026, 7, 17), width=120))
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
    from taskboard.views import render_kanban
    phases = ["Intake", "Design", "Build", "Review", "Shipped"]
    path = tmp_path / "custom.json"
    b = Board([], [], path, phases=phases)
    b.tasks = [Task(f"task {p}", None, p) for p in phases]
    b.save()
    assert Board.load(str(path)).phases == phases          # round-trips

    out = str(render_kanban(b, False, None, date(2026, 7, 17), width=140)).split("\n")
    header_row = out[1]                                    # the phase-name row
    for p in phases:
        assert p.upper() in header_row
    # the box is gone: only the INTERNAL dividers remain (5 columns -> 4)
    assert header_row.count("│") == len(phases) - 1
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
        await pilot.press("4")
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
GANTT_MIDWEEK = date(2026, 7, 23)        # a Thursday, so the today rule sits mid-grid


def _gantt_board(tmp_path):
    from taskboard.models import Board, Project, Task
    b = Board([], [], tmp_path / "g.json", phases=["A", "B", "C"])
    alpha = Project("Alpha", "sky", start_date="2026-07-06", due_date="2026-08-17")
    beta = Project("Beta", "violet", start_date="2026-07-13", due_date=None)
    b.projects += [alpha, beta]
    b.tasks += [
        Task("a-one", alpha.id, "A", start_date="2026-07-06", due_date="2026-07-20"),
        Task("a-two", alpha.id, "C", start_date="2026-07-20", due_date="2026-08-03"),
        Task("b-one", beta.id, "A", start_date="2026-07-13", due_date="2026-07-27"),
    ]
    return b


def _gantt_rows(board, width=96, height=30):
    return str(render_gantt(board, False, None, today=GANTT_MIDWEEK,
                            width=width, height=height)).split("\n")


def _project_row(board, name, width=96, height=30):
    return next(l for l in _gantt_rows(board, width, height) if name in l)


# --------------------------------------------------------------------------- #
# The gantt is the FIELD now (REV3). These laws replace the week-grid ones.
#
# RETIRED WITH THE DESIGN, and named here so the loss is not silent:
#   * test_gantt_bar_uses_dual_density_braille / _still_has_dual_density_bar —
#     the ⣿/⢕ dual-density bar is gone. The span is now TWO BANDS: ash for
#     elapsed and identity for what remains, with the progress band beneath.
#   * test_gantt_bar_split_follows_phase_progress — the split moved to the
#     second band, and its law is test_the_two_bands_show_the_slip below.
#   * test_gantt_divides_projects — the `┈` divider row between projects is
#     gone deliberately: it was 470 cells of pure separator on a 5-project
#     board and the single biggest reason the gantt led the app in chrome
#     (21.2 %). Measured after the redesign: 7.8 %.
#   * test_gantt_label_column_is_generous_for_names — the label column shrank
#     to the shared field geometry ON PURPOSE, because the TITLE now runs over
#     the field instead (REV5 #19), which is where the reader reads.
#   * test_gantt_meta_column_adapts_to_width — the meta band is the meter plus
#     the percent; its drop order is tested in test_gantt.py.
# --------------------------------------------------------------------------- #
def test_gantt_axis_includes_the_past(tmp_path):
    """THE REV3 FINDING, and the reason this view was the one place where MORE
    data produced LESS used screen: the old axis started on Monday of this week,
    so a project already overdue drew as an empty row with a `◂`. The more
    overdue work a board held, the emptier the view got."""
    b = _gantt_board(tmp_path)
    scale = next(l for l in _gantt_rows(b) if "today" in l and re.search(r"-\d+d", l))
    assert re.search(r"-\d+d", scale), scale        # the window reaches backwards


def test_the_slip_is_the_gap_from_the_dot_to_the_diamond(tmp_path):
    """The answer a gantt exists to give, now in ONE row.

    WAS `test_the_two_bands_show_the_slip`, and the claim has not changed: the
    span runs ash-then-identity to its `◆`, a second mark says how far the work
    actually got, and THE GAP BETWEEN THEM IS THE SLIP read as a length. What
    changed on 2026-08-07 is that the second mark stopped being a whole row of
    `▓▓▓▌` under the span and became one cell ON it — the operator's "en vez del
    cuadro sombreado, una línea y el círculo", which also handed the freed row
    back to the tasks he could not see.

    The law is rewritten rather than deleted because it still HAS a subject.
    Deleting it would have been the cheap way to a green suite and would have
    left the view's whole reason for existing unasserted."""
    b = _gantt_board(tmp_path)
    span = _project_row(b, "Alpha")
    from taskboard.views import PROGRESS_DOT, FIELD_REACH
    # by NAME, not by glyph: the field's texture is a design decision that has
    # changed twice now, and this law is about the MARKS, not the characters
    # they happen to be drawn with today.
    assert FIELD_REACH in span and "◆" in span      # the span, ending at its date
    assert PROGRESS_DOT in span                     # how far the work got
    assert span.index(PROGRESS_DOT) < span.index("◆")   # the gap IS the slip


def test_the_project_costs_exactly_one_field_row(tmp_path):
    """The row the tasks got back. A second row per project is what made the
    view run out of space, so its absence is asserted directly rather than
    inferred from the slip law above still passing."""
    b = _gantt_board(tmp_path)
    rows = _gantt_rows(b)
    span = _project_row(b, "Alpha")
    below = rows[rows.index(span) + 1]
    from taskboard.views import FIELD_PROGRESS
    assert FIELD_PROGRESS not in below, (
        "a shaded progress row is back under the project")
    # and it is a TASK row that follows, not blank filler
    assert below.strip(), "the project is followed by an empty row"


def test_a_project_with_no_progress_draws_no_progress_band(tmp_path):
    b = _gantt_board(tmp_path)
    rows = _gantt_rows(b)
    beta = _project_row(b, "Beta")
    assert "⣤" not in rows[rows.index(beta) + 1]


def test_the_today_rule_spans_every_row(tmp_path):
    """Kept from the old design, deliberately: one column every row shares."""
    b = _gantt_board(tmp_path)
    from taskboard.views import (FIELD_HALF, FIELD_PHASE_TIP, FIELD_PROGRESS,
                                 FIELD_REACH, FIELD_TASK, RULE, gantt_geometry)
    geo = gantt_geometry(94, 30)
    col = geo.label_w + geo.today_dc // 2
    body = [l for l in _gantt_rows(b) if l.startswith("▎ ") or l.startswith("▏ ")]
    assert len(body) >= 4
    for line in body:
        drawn = {FIELD_REACH, FIELD_PROGRESS, FIELD_TASK, FIELD_HALF,
                 *FIELD_PHASE_TIP}
        assert (line[col] == RULE or line[col] in drawn
                or 0x2800 <= ord(line[col]) <= 0x28FF), line[col]


def test_the_due_diamond_marks_the_projects_own_date(tmp_path):
    """`◆` sits at the project's due date and wears the project's hue. It used
    to turn red when past — that judgement moved to the meter, whose `▲` is the
    row's one alert, so the diamond says WHICH project and WHEN it is due."""
    from taskboard.views import HEX
    b = _gantt_board(tmp_path)
    text = render_gantt(b, False, None, today=GANTT_MIDWEEK, width=96, height=30)
    # Locate the diamond by CHARACTER, not by span: a run may legitimately carry
    # its neighbours (span economy merges same-hue cells), so "a span whose text
    # is exactly ◆" describes the markup's shape rather than the drawing's.
    styles: list[str | None] = [None] * len(text.plain)
    for s in text.spans:
        for i in range(s.start, min(s.end, len(styles))):
            styles[i] = str(s.style)
    worn = []
    at = 0
    for row, line in enumerate(text.plain.split("\n")):
        for col, ch in enumerate(line):
            # row 0 is the view's own title ('◆ GANTT'), which wears accent and
            # is not a due date; the diamonds under test live in the field.
            if ch == "◆" and row > 0:
                worn.append(styles[at + col])
        at += len(line) + 1
    assert worn, "no diamond drawn at all"
    for style in worn:
        assert HEX["sky"] in style or HEX["violet"] in style
        assert HEX["over"] not in style


def test_a_reach_carries_identity_and_the_meter_carries_urgency(tmp_path):
    from taskboard.models import Board, Project, Task
    from taskboard.views import HEX, METER_W
    b = Board([], [], tmp_path / "g2.json", phases=["A", "B", "C"])
    p = Project("P", "sky", start_date="2026-07-06", due_date="2026-09-30")
    b.projects.append(p)
    b.tasks += [
        Task("overduetask", p.id, "A", start_date="2026-07-06", due_date="2026-07-13"),
        Task("ontracktask", p.id, "A", start_date="2026-07-20", due_date="2026-08-24"),
    ]
    text = render_gantt(b, False, None, today=GANTT_MIDWEEK, width=96, height=30)
    from taskboard.views import FIELD_PHASE_TIP, FIELD_TASK
    reach = {FIELD_TASK, *FIELD_PHASE_TIP}
    reach_styles = [str(s.style) for s in text.spans
                    if set(text.plain[s.start:s.end]) & reach]
    assert reach_styles
    for style in reach_styles:
        assert HEX["over"] not in style and HEX["soon"] not in style
    overdue_row = next(l for l in str(text).split("\n") if "overduetask" in l)
    assert "▲" in overdue_row[-METER_W:]


def test_gantt_header_counts_past_due(tmp_path):
    b = _gantt_board(tmp_path)
    header = _gantt_rows(b)[0]
    assert "past due" in header


def test_gantt_width_exact_across_widths(tmp_path):
    b = _gantt_board(tmp_path)
    for w in (24, 40, 68, 96, 130, 200):
        assert all(len(l) == max(24, w) for l in _gantt_rows(b, w))

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


def test_gantt_titles_are_readable_because_they_run_over_the_field():
    """Was: "the label column is generous (18-30 cells)". The label column
    shrank to the shared field geometry ON PURPOSE — the title runs over the
    field now, which is where the reader reads, and gets more cells that way
    than the old column ever gave it."""
    from taskboard.views import gantt_geometry
    geo = gantt_geometry(94, 30)
    assert geo.label_w >= 12

def _agenda_board(tmp_path):
    """A board covering every axis branch: overdue, due-today, this-week, later,
    an off-window clamp (far past / far future), an undated task and a done one."""
    from taskboard.models import Board, Project, Task
    b = Board([], [], tmp_path / "a.json", phases=["A", "B", "C"])
    p = Project("Proj", "cyan", start_date="2026-07-01", due_date="2026-09-01")
    b.projects.append(p)
    b.tasks += [
        Task("past far", p.id, "A", due_date="2025-01-01"),      # clamp left
        Task("overdue", p.id, "A", due_date="2026-07-20"),       # -3d
        Task("today", p.id, "A", due_date="2026-07-23"),         # on the rule
        Task("soon", p.id, "A", due_date="2026-07-27"),          # +4d
        Task("later", p.id, "A", due_date="2026-08-10"),         # +18d
        Task("future far", p.id, "A", due_date="2027-12-31"),    # clamp right
        Task("done one", p.id, "C", due_date="2026-07-25"),      # last phase -> done
        Task("undated", p.id, "A", due_date=None),               # no date group
    ]
    return b


def _row(lines, title):
    return next(l for l in lines if title in l)


AGENDA_TODAY = date(2026, 7, 23)      # a Thursday; the today rule sits mid-axis


def _agenda_board(tmp_path):
    """A board covering every axis branch: overdue, due-today, this-week, later,
    an off-window clamp (far past / far future), an undated task and a done one."""
    from taskboard.models import Board, Project, Task
    b = Board([], [], tmp_path / "a.json", phases=["A", "B", "C"])
    p = Project("Proj", "cyan", start_date="2026-07-01", due_date="2026-09-01")
    b.projects.append(p)
    b.tasks += [
        Task("past far", p.id, "A", due_date="2025-01-01"),      # clamp left
        Task("overdue", p.id, "A", due_date="2026-07-20"),       # -3d
        Task("today", p.id, "A", due_date="2026-07-23"),         # on the rule
        Task("soon", p.id, "A", due_date="2026-07-27"),          # +4d
        Task("later", p.id, "A", due_date="2026-08-10"),         # +18d
        Task("future far", p.id, "A", due_date="2027-12-31"),    # clamp right
        Task("done one", p.id, "C", due_date="2026-07-25"),      # last phase -> done
        Task("undated", p.id, "A", due_date=None),               # no date group
    ]
    return b


def _row(lines, title):
    return next(l for l in lines if title in l)


def test_agenda_has_no_urgency_group_headers(tmp_path):
    """WHY: the shared axis now ENCODES urgency by position, so the old textual
    OVERDUE / TODAY / THIS WEEK sub-headers are pure redundancy and are gone."""
    b = _agenda_board(tmp_path)
    out = str(render_agenda(b, False, None, today=AGENDA_TODAY, width=100))
    assert "OVERDUE" not in out
    assert "TODAY" not in out            # the header count says 'today' (lower-case)
    assert "THIS WEEK" not in out
    assert "LATER" not in out


def test_agenda_dot_position_encodes_due(tmp_path):
    """WHY: distance along the axis IS urgency — a sooner due date puts its ● left
    of a later one, and a task due today sits exactly on the today-rule column."""
    from taskboard.models import Board, Project, Task
    b = Board([], [], tmp_path / "a.json", phases=["A", "B", "C"])
    p = Project("Proj", "cyan")
    b.projects.append(p)
    b.tasks += [
        Task("soonertask", p.id, "A", due_date="2026-07-24"),    # +1d
        Task("latertask", p.id, "A", due_date="2026-07-30"),     # +7d
        Task("todaytask", p.id, "A", due_date="2026-07-23"),     # +0d
    ]
    lines = str(render_agenda(b, False, None, today=AGENDA_TODAY, width=100)).splitlines()
    rs, rl, rt = _row(lines, "soonertask"), _row(lines, "latertask"), _row(lines, "todaytask")
    assert rs.index("●") < rl.index("●")          # sooner is left of later
    rule_col = rs.index("┃")                       # the rule shows on non-today rows
    assert rt.index("●") == rule_col               # a due-today dot sits on the rule column


def test_agenda_today_rule_present(tmp_path):
    """WHY: 'today' must be one vertical anchor, the SAME teal ┃ column on every
    task row — the fixed reference every dot is read against."""
    from taskboard.models import Board, Project, Task
    from taskboard.views import HEX
    b = Board([], [], tmp_path / "a.json", phases=["A", "B", "C"])
    p = Project("Proj", "cyan")
    b.projects.append(p)
    b.tasks += [
        Task("alphatask", p.id, "A", due_date="2026-07-25"),     # +2d
        Task("betatask", p.id, "A", due_date="2026-07-28"),      # +5d
    ]
    txt = render_agenda(b, False, None, today=AGENDA_TODAY, width=100)
    lines = txt.plain.split("\n")
    r1, r2 = _row(lines, "alphatask"), _row(lines, "betatask")
    assert "┃" in r1 and "┃" in r2
    assert r1.index("┃") == r2.index("┃")          # a single vertical line, same column
    li = next(i for i, l in enumerate(lines) if "alphatask" in l)
    base = sum(len(lines[j]) + 1 for j in range(li))
    off = base + r1.index("┃")
    styles = {str(sp.style) for sp in txt.spans if sp.start <= off < sp.end}
    assert any(HEX["accent"] in s for s in styles)  # the rule is teal


def test_agenda_undated_tasks_are_kept(tmp_path):
    """WHY: a task with no due date can't sit on a time axis, but dropping it would
    hide work — it must survive under a single 'no date' group."""
    from taskboard.models import Board, Project, Task
    b = Board([], [], tmp_path / "a.json", phases=["A", "B", "C"])
    p = Project("Proj", "cyan")
    b.projects.append(p)
    b.tasks += [
        Task("dateditem", p.id, "A", due_date="2026-07-25"),
        Task("floatyitem", p.id, "A", due_date=None),
    ]
    out = str(render_agenda(b, False, None, today=AGENDA_TODAY, width=100))
    assert "no date" in out               # the group label is present
    assert "floatyitem" in out            # and the undated task is not dropped


def test_agenda_dot_colour_by_urgency(tmp_path):
    """WHY: colour reinforces the position — an overdue dot is red (over), a
    due-today dot is amber (soon), so a glance reads the crunch without counting."""
    from taskboard.models import Board, Project, Task
    from taskboard.views import HEX
    b = Board([], [], tmp_path / "a.json", phases=["A", "B", "C"])
    p = Project("Proj", "cyan")
    b.projects.append(p)
    b.tasks += [
        Task("overdueitem", p.id, "A", due_date="2026-07-20"),   # -3d
        Task("duetodayitem", p.id, "A", due_date="2026-07-23"),  # +0d
    ]
    txt = render_agenda(b, False, None, today=AGENDA_TODAY, width=100)
    lines = txt.plain.split("\n")

    def dot_styles(title):
        li = next(i for i, l in enumerate(lines) if title in l)
        base = sum(len(lines[j]) + 1 for j in range(li))
        off = base + lines[li].index("●")
        return {str(sp.style) for sp in txt.spans if sp.start <= off < sp.end}

    assert any(HEX["over"] in s for s in dot_styles("overdueitem"))
    assert any(HEX["soon"] in s for s in dot_styles("duetodayitem"))


def test_agenda_width_exact_across_widths(tmp_path):
    """WHY: box-art breaks the instant one line drifts a cell. Every agenda line —
    header, scale, dot rows (incl. off-window ◂/▸ clamps), the 'no date' divider,
    the done row and the height-fill blanks — must be EXACTLY the target width."""
    b = _agenda_board(tmp_path)
    sel = b.tasks[1].id
    for w in (40, 68, 100, 140):
        lines = str(render_agenda(b, False, sel, today=AGENDA_TODAY,
                                  width=w, height=30)).splitlines()
        assert all(len(l) == w for l in lines), f"agenda {w}: a line != {w}"


# --------------------------------------------------------------------------- #
# quick keys: `[`/`]` phase move, `!` priority, `b` blocked (batch-04 R-01/R-02)
# --------------------------------------------------------------------------- #
def _key_for(action: str) -> str:
    """The physical key bound to `action`, read off the seat — never typed as
    a literal, so the test follows the seat if the key ever moves."""
    from taskboard.keymap import KEYMAP
    return next(k for k in KEYMAP if k.action == action).keys.split(",")[0]


def _ops_board(tmp_path, *tasks, name="ops.json") -> Board:
    """The quick-key AT fixture: ONE project, FOUR phases — a middle with two
    neighbours, so a wrong-target move is distinguishable from a correct one.
    Saved to disk: the app loads it for real, and the reload limbs (C-12)
    re-read that same file."""
    p = Project("Alpha", "sky")
    b = Board([p], list(tasks), tmp_path / name,
              phases=["Backlog", "Doing", "Review", "Done"])
    for t in tasks:
        t.project_id = p.id
    b.save()
    return b


def _painted_column(app, title: str) -> str:
    """Which painted kanban column holds `title` — read off the painted text
    ALONE (C-32): the phase-name header's x-offsets bracket the card's
    x-offset. No internal recompute anchors this end."""
    lines = board_text(app).split("\n")
    hdr = next(l for l in lines
               if all(p.upper() in l for p in app.board.phases))
    offs = sorted((hdr.index(p.upper()), p) for p in app.board.phases)
    x = next(l for l in lines if title in l).index(title)
    return next(p for off, p in reversed(offs) if off <= x)


def _card_row(app, title: str) -> str:
    """The one painted line holding `title` — marker searches are confined to
    it, because `!` and the box glyphs legitimately appear elsewhere."""
    return next(l for l in board_text(app).split("\n") if title in l)


async def test_phase_move_forward_dates_the_move(tmp_path):
    """AT-001 (HLR-001): `]` on a mid-phase task renders the card in the next
    column, and the move is DATED — the reloaded board shows the new phase
    with today's stamp. RED counterfactuals: the action missing (the tree's
    exact pre-increment state — executable RED from day one), or the mutation
    never saved (the reload limb fails)."""
    today = date.today().isoformat()
    task = Task("Widget", None, "Doing", phase_changed=None)
    board = _ops_board(tmp_path, task)
    app = TaskboardApp(board_path=str(board.path))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("4")                  # kanban: the columns are the readout
        await pilot.pause()
        assert _painted_column(app, "Widget") == "Doing"     # pre-state companion
        await pilot.press(_key_for("phase_move(1)"))
        await pilot.pause()
        assert _painted_column(app, "Widget") == "Review"
        reloaded = Board.load(board.path).task_by_id(task.id)
        assert reloaded.phase == "Review"
        assert reloaded.phase_changed == today


async def test_phase_move_round_trip_restamps_and_the_ends_are_silent_no_ops(tmp_path):
    """AT-002 (HLR-001, the AMD-01 round-trip): `]` advances and stamps; `[`
    returns and RE-DATES (the clock restarts); only AFTER that live forward
    drive, the first-phase `[` is a no-op that neither moves, re-stamps, nor
    even writes the file — sequenced this way a dead `[` cannot pass the
    no-op limb. RED counterfactuals: (a) `task.phase` assigned directly,
    bypassing `set_task_phase` — stamp limbs red while phase limbs stay green
    (the F-2 trap); (b) clamp missing — index -1 wraps to the last phase;
    (c) clamp that still re-stamps; (d) mutation without `board.save()`."""
    today = date.today().isoformat()
    task = Task("Widget", None, "Doing", phase_changed=None)
    board = _ops_board(tmp_path, task)
    app = TaskboardApp(board_path=str(board.path))
    fwd, back = _key_for("phase_move(1)"), _key_for("phase_move(-1)")
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.pause()
        t = app.board.task_by_id(task.id)
        # BOTH companions BEFORE any key, or the stamp assertions have no
        # discriminating gap
        assert t.phase == "Doing"
        assert t.phase_changed is None
        # the live forward drive: phase advances AND the stamp is written
        await pilot.press(fwd)
        await pilot.pause()
        assert t.phase == "Review"
        assert t.phase_changed == today
        r = Board.load(board.path).task_by_id(task.id)
        assert (r.phase, r.phase_changed) == ("Review", today)   # persisted (C-12)
        # backdate the stamp, or "the clock restarts" is unreadable: a `[`
        # that moves WITHOUT re-stamping is caught only against a stale stamp
        t.phase_changed = "2000-01-01"
        app.board.save()
        await pilot.press(back)
        await pilot.pause()
        assert t.phase == "Doing"
        assert t.phase_changed == today                 # RE-DATED, not merely kept
        # the sequenced no-op: first phase, `[` — never run first
        await pilot.press(back)                         # Doing -> Backlog, live
        await pilot.pause()
        assert t.phase == "Backlog"
        stamp, blob = t.phase_changed, board.path.read_bytes()
        await pilot.press(back)                         # the clamp: silent no-op
        await pilot.pause()
        assert t.phase == "Backlog"                     # no wrap
        assert t.phase_changed == stamp                 # no re-stamp
        assert board.path.read_bytes() == blob          # not even saved
        # the other end, symmetric
        for _ in range(3):
            await pilot.press(fwd)
            await pilot.pause()
        assert t.phase == "Done"
        stamp, blob = t.phase_changed, board.path.read_bytes()
        await pilot.press(fwd)
        await pilot.pause()
        assert t.phase == "Done" and t.phase_changed == stamp
        assert board.path.read_bytes() == blob
        # the empty boundary: no selection -> no-op, no write
        app.selected_task_id = None
        await pilot.press(back)
        await pilot.pause()
        assert t.phase == "Done"
        assert board.path.read_bytes() == blob


async def test_phase_move_clamps_unknown_phase_into_bucket_zero(tmp_path):
    """TC-001 (HLR-001/LLR-001.1): a task in an UNKNOWN phase reads as bucket
    0 (`phase_index` fallback; `phase_buckets`, views.py:616) — `[` clamps it
    to the FIRST phase instead of wrapping to the last (a missing clamp lands
    it in Done: the RED), `]` advances it one step from bucket 0. The fixture
    swaps the app's board for an in-memory one because `Board.load` snaps
    unknown phases at load (models.py:868-869) — that snap is a different
    seat, and this test pins the LIVE-path fallback."""
    task = Task("Widget", None, "Doing")
    board = _ops_board(tmp_path, task)
    app = TaskboardApp(board_path=str(board.path))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.pause()
        ghost = Task("Ghost", None, "Nowhere", phase_changed=None)
        app.board = Board(board.projects, [ghost], board.path,
                          phases=["Backlog", "Doing", "Review", "Done"])
        app.selected_task_id = ghost.id
        app.refresh_view()
        await pilot.press(_key_for("phase_move(-1)"))
        await pilot.pause()
        assert ghost.phase == "Backlog"     # bucket 0 + clamp, never a wrap
        assert ghost.phase_changed == date.today().isoformat()
        ghost.phase = "Nowhere"             # re-seat the unknown
        ghost.phase_changed = None
        await pilot.press(_key_for("phase_move(1)"))
        await pilot.pause()
        assert ghost.phase == "Doing"       # bucket 0 + one step forward


async def test_prio_cycle_walks_the_declared_order_and_paints_the_marker(tmp_path):
    """AT-003 (HLR-002): from default `normal`, `!` once -> high and the card
    row shows the `!` token; twice more closes the full cycle
    high -> low -> normal with the token gone. RED counterfactuals: cycle
    direction inverted (normal -> low first) fails the very first limb; no
    persist fails the reload limbs."""
    task = Task("Widget", None, "Doing")            # priority defaults to normal
    board = _ops_board(tmp_path, task)
    app = TaskboardApp(board_path=str(board.path))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("4")
        await pilot.pause()
        key = _key_for("prio_cycle")
        assert "!" not in _card_row(app, "Widget")      # normal paints no marker
        await pilot.press(key)
        await pilot.pause()
        assert app.board.task_by_id(task.id).priority == "high"
        assert "!" in _card_row(app, "Widget")
        assert Board.load(board.path).task_by_id(task.id).priority == "high"
        await pilot.press(key)                          # wraps high -> low
        await pilot.pause()
        assert app.board.task_by_id(task.id).priority == "low"
        assert "!" not in _card_row(app, "Widget")
        await pilot.press(key)                          # low -> normal: cycle closed
        await pilot.pause()
        assert Board.load(board.path).task_by_id(task.id).priority == "normal"
        assert "!" not in _card_row(app, "Widget")


async def test_toggle_blocked_flips_the_flag_and_the_card_prefix(tmp_path):
    """AT-004 (HLR-002): `b` -> row prefix `▲` and JSON `blocked` true; `b`
    again -> prefix `▊` and false. RED counterfactuals: a toggle that writes
    but never clears fails the second limb; a render branch that stops
    switching the prefix fails the prefix limbs."""
    task = Task("Widget", None, "Doing", blocked=False)
    board = _ops_board(tmp_path, task)
    app = TaskboardApp(board_path=str(board.path))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("4")
        await pilot.pause()
        key = _key_for("toggle_blocked")
        assert "▊" in _card_row(app, "Widget")
        assert "▲" not in _card_row(app, "Widget")
        await pilot.press(key)
        await pilot.pause()
        assert app.board.task_by_id(task.id).blocked is True
        assert "▲" in _card_row(app, "Widget")
        assert "▊" not in _card_row(app, "Widget")
        assert Board.load(board.path).task_by_id(task.id).blocked is True
        await pilot.press(key)
        await pilot.pause()
        assert Board.load(board.path).task_by_id(task.id).blocked is False
        assert "▊" in _card_row(app, "Widget")
        assert "▲" not in _card_row(app, "Widget")


# --------------------------------------------------------------------------- #
# kanban sort/group modes: the ONE `kanban_order` seat, the `s`/`g` cycles,
# and the nav/render parity oracle (batch-04 R-03/R-04, HLR-003/HLR-004)
# --------------------------------------------------------------------------- #
def _mode_board(tmp_path, name="modes.json") -> Board:
    """The sort/group fixture (AT-005…008, TC-005/006): FOUR phases with
    Review EMPTY (the empty-column case), TWO projects, and a Doing column
    crafted so the four sort orders are pairwise distinct with a deliberate
    tie in every key. Titles are short, unique and substring-free, so a
    painted-text search can never confuse one card for another — and no title
    is a substring of a project or group name."""
    from datetime import timedelta
    pa, pb = Project("ProjA", "violet"), Project("ProjB", "cyan")
    today = date.today()

    def iso(delta):
        return (today + timedelta(days=delta)).isoformat()

    tasks = [
        Task("k01", pa.id, "Doing", "high", due_date=iso(9), phase_changed=iso(-6)),
        Task("k02", pa.id, "Doing", "normal", due_date=iso(2), phase_changed=iso(-1)),
        Task("k03", pb.id, "Doing", "high", due_date=None, phase_changed=iso(-3)),
        Task("k04", pb.id, "Doing", "normal", due_date=None,
             phase_changed=None, blocked=True),
        Task("k05", pa.id, "Doing", "low", due_date=iso(4), phase_changed=None),
        Task("k06", pa.id, "Done", "normal", due_date=iso(30), phase_changed=iso(-2)),
        Task("k07", pb.id, "Done", "low", due_date=None, phase_changed=None),
        Task("k08", pa.id, "Backlog", "high", due_date=iso(-1), phase_changed=iso(-4)),
        Task("k09", pb.id, "Backlog", "low", due_date=None, phase_changed=None),
    ]
    b = Board([pa, pb], tasks, tmp_path / name,
              phases=["Backlog", "Doing", "Review", "Done"])
    b.save()
    return b


def _painted_kanban(app):
    """The painted kanban, recovered from the PAINTED TEXT ALONE (the parity
    oracle's anchor end, 01b §4 step 1 — never from `phase_buckets` or any
    internal recompute, which would make the oracle a second copy of the
    suspect). Column membership comes from the phase-header row's `│`
    separator positions; cards are located by title (unique by fixture).

    Returns (drawn phase names, per-column row lists) where each row is
    ("h", group-header text) or ("t", task title)."""
    lines = board_text(app).split("\n")
    hdr_i = next(i for i, l in enumerate(lines)
                 if all(p.upper() in l for p in app.board.phases))
    hdr = lines[hdr_i]
    seps = [x for x, ch in enumerate(hdr) if ch == "│"]
    bounds = ([(-1, seps[0])]
              + [(seps[i], seps[i + 1]) for i in range(len(seps) - 1)]
              + [(seps[-1], len(hdr))])
    names = [next(p for p in app.board.phases if p.upper() in hdr[lo + 1:hi])
             for lo, hi in bounds]
    cols: list[list[tuple[str, str]]] = [[] for _ in bounds]
    end = next((i for i in range(hdr_i + 1, len(lines)) if "┴" in lines[i]),
               len(lines))
    for l in lines[hdr_i + 2:end]:              # skip the ┼ rule row
        for ci, (lo, hi) in enumerate(bounds):
            seg = l[lo + 1:hi]
            if seg.strip().startswith("▐"):
                cols[ci].append(("h", seg.strip()[1:].strip()))
                continue
            hit = [t.title for t in app.board.tasks if t.title in seg]
            assert len(hit) <= 1, f"ambiguous painted segment {seg!r}"
            cols[ci].extend(("t", w) for w in hit)
    return names, cols


def _painted_card_ids(app, cols):
    by_title = {t.title: t.id for t in app.board.tasks}
    return [[by_title[w] for kind, w in col if kind == "t"] for col in cols]


async def _assert_kanban_parity(app, pilot):
    """01b §4, the whole law: after any mode change AND after any arrow press,
    the order the cursor walks is the order the screen paints. Anchored in the
    painted text; `app._nav_columns()` is the other end. Companions:
    non-emptiness (≥ 2 columns) and union-coverage of every visible task, so
    an unpainted board cannot satisfy `[] == []` vacuously. The `line_map`
    agreement at the end is a labelled regression PIN (step 6), not the gate."""
    names, cols = _painted_kanban(app)
    assert names == list(app.board.phases)      # nothing windowed at 120 cells
    painted = _painted_card_ids(app, cols)
    nav = app._nav_columns()
    assert len(nav) == len(painted)
    for ci, (p_col, n_col) in enumerate(zip(painted, nav)):
        assert p_col == n_col, \
            f"column {ci} ({names[ci]}): painted {p_col} != nav {n_col}"
    assert sum(1 for col in painted if col) >= 2, "vacuous: nothing painted"
    visible = {t.id for t in app.board.visible_tasks(app.show_archived)}
    assert {i for col in painted for i in col} == visible
    # arrow walk: down follows the PAINTED-next; right lands on the first
    # painted card of the next non-empty painted column
    first = next(ci for ci, col in enumerate(painted) if len(col) >= 2)
    app.selected_task_id = painted[first][0]
    app.refresh_view()
    await pilot.pause()
    await pilot.press("down")
    assert app.selected_task_id == painted[first][1]
    await pilot.press("right")
    nxt = next(ci for ci in range(first + 1, len(painted)) if painted[ci])
    assert app.selected_task_id == painted[nxt][0]
    # REGRESSION PIN (not the gate): the line_map still agrees with the paint
    text = board_text(app).split("\n")
    for tid, li in app._line_map.items():
        assert app.board.task_by_id(tid).title in text[li]
    return painted


async def test_kanban_parity_painted_text_oracle(tmp_path):
    """TC-006 (HLR-003/HLR-004, 01b §4 — the batch's central oracle): painted
    order == nav order per column, plus the arrow walk, swept after EVERY `s`
    press (4 modes), after EVERY `g` press (3 modes), and across the full
    4x3 sort-by-group cross-product. RED counterfactual (EXECUTED, see
    increment-006): nav fed a different ordering than the renderer (the nav
    branch reverted to raw `_kanban_groups` order) → the per-column assertion
    goes red, and `down` moves the cursor off the visually-next card → the
    walk assertion goes red."""
    board = _mode_board(tmp_path)
    app = TaskboardApp(board_path=str(board.path))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("4")
        await pilot.pause()
        s_key, g_key = _key_for("kanban_sort"), _key_for("kanban_group")
        for _ in range(4):                  # after every `s` press
            await _assert_kanban_parity(app, pilot)
            await pilot.press(s_key)
            await pilot.pause()
        assert app.kanban_sort == "project"             # the cycle closed
        for _ in range(3):                  # after every `g` press
            await _assert_kanban_parity(app, pilot)
            await pilot.press(g_key)
            await pilot.pause()
        assert app.kanban_group == "project"
        for sort in ("project", "priority", "due", "recent"):   # the full
            for group in ("project", "priority", "horizon"):    # cross-product
                app.kanban_sort, app.kanban_group = sort, group
                app.refresh_view()
                await pilot.pause()
                await _assert_kanban_parity(app, pilot)


async def test_kanban_sort_cycles_and_names_the_mode(tmp_path):
    """AT-005 (HLR-003): `s` cycles project→priority→due→recent→project; the
    painted Doing column follows each mode's RULE (recomputed from the
    fixture, never hand-listed); the header names every non-default mode and
    stays bare at the default. The fixture guard (four pairwise-distinct
    expected orders) runs FIRST — a palindrome fixture would be green on a
    mode-skipping mutant. RED counterfactuals: renderer not wired to the mode
    (order assertion red); sort mutating the model (the model-order companion
    red); cycle skipping a mode (a press lands on the wrong rule's order)."""
    board = _mode_board(tmp_path)
    doing = [t for t in board.tasks if t.phase == "Doing"]
    groups = [[t for t in doing if t.project_id == p.id]
              for p in board.visible_projects(False)]

    def expected(sort):                     # the stated rule, restated plainly
        if sort == "priority":
            rank = {"high": 0, "normal": 1, "low": 2}

            def key(t):
                return (not t.blocked, rank[t.priority],
                        t.due_date is None, t.due_date or "9999")
        elif sort == "due":
            def key(t):
                return (not t.blocked, t.due_date is None, t.due_date or "9999")
        elif sort == "recent":
            def key(t):
                return (t.phase_changed is None, t.phase_changed or "")
        else:
            key = None
        out = []
        for items in groups:
            if sort == "recent":            # desc, None last, ties stable
                out += sorted(items, key=lambda t: t.phase_changed or "",
                              reverse=True)
            elif key is not None:
                out += sorted(items, key=key)       # stable: ties keep board
            else:
                out += items                        # project: board order
        return [t.id for t in out]

    orders = {m: expected(m) for m in ("project", "priority", "due", "recent")}
    assert len({tuple(o) for o in orders.values()}) == 4, "palindrome fixture"
    model_order = [t.id for t in board.tasks]
    app = TaskboardApp(board_path=str(board.path))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("4")
        await pilot.pause()
        assert "sort:" not in board_text(app).split("\n")[0]   # default unnamed
        s_key = _key_for("kanban_sort")
        for mode in ("priority", "due", "recent", "project"):
            await pilot.press(s_key)
            await pilot.pause()
            assert app.kanban_sort == mode
            header_line = board_text(app).split("\n")[0]
            if mode == "project":
                assert "sort:" not in header_line      # cycle closed, bare
            else:
                assert f"sort: {mode}" in header_line
            names, cols = _painted_kanban(app)
            painted = _painted_card_ids(app, cols)
            assert painted[names.index("Doing")] == orders[mode]
        # the sort is a VIEW concern: the model order never moved (C-12 limb:
        # the file on disk agrees — a view sort that saved would show here)
        assert [t.id for t in board.tasks] == model_order
        assert [t.id for t in Board.load(board.path).tasks] == model_order


async def test_kanban_sort_parity_arrow_walk(tmp_path):
    """AT-006 (HLR-003): sort `priority` + grouping `priority` (one `s`, one
    `g`), then ↓ twice — the selection is `nav_model`'s third entry of that
    column, AND that task's title is the third card the screen paints there.
    RED counterfactual (EXECUTED): the nav branch reverted to raw
    `_kanban_groups` order → the two ends name different thirds."""
    board = _mode_board(tmp_path)
    app = TaskboardApp(board_path=str(board.path))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("4")
        await pilot.pause()
        await pilot.press(_key_for("kanban_sort"))
        await pilot.pause()
        await pilot.press(_key_for("kanban_group"))
        await pilot.pause()
        from taskboard.views import nav_model
        cols = nav_model("kanban", app.board, False,
                         kanban_sort="priority", kanban_group="priority")
        ci = next(i for i, col in enumerate(cols) if len(col) >= 3)
        app.selected_task_id = cols[ci][0]
        app.refresh_view()
        await pilot.pause()
        await pilot.press("down")
        await pilot.press("down")
        assert app.selected_task_id == cols[ci][2]
        names, painted_cols = _painted_kanban(app)     # the rendered-text limb
        painted = _painted_card_ids(app, painted_cols)
        assert painted[ci][2] == cols[ci][2]


async def test_kanban_group_cycles_headers_and_membership(tmp_path):
    """AT-007 (HLR-004): `g` cycles project→priority→horizon→project. Under
    horizon, each column's painted group headers are EXACTLY the rule-derived
    non-empty set (incl. the trailing `Done` group), in canonical order; every
    card sits under its rule-derived header (nearest header above); the union
    under all headers is the column's whole task set (a silently dropped group
    cannot satisfy the quantifier); project headers are GONE. RED
    counterfactuals: cosmetic grouping (headers change, membership doesn't) →
    per-card membership red; an empty group drawing a header → header-set
    equality red; a mode dropped from the cycle → header-set mismatch red."""
    board = _mode_board(tmp_path)
    today = date.today()

    def horizon_of(t):                      # the stated rule, restated plainly
        if t.phase == board.phases[-1]:
            return "Done"
        if t.due_date is None:
            return "No date"
        delta = (date.fromisoformat(t.due_date) - today).days
        if delta < 0:
            return "Overdue"
        return "This week" if delta <= 7 else "Later"

    def priority_of(t):
        return {"high": "High", "normal": "Normal", "low": "Low"}[t.priority]

    app = TaskboardApp(board_path=str(board.path))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("4")
        await pilot.pause()
        g_key = _key_for("kanban_group")
        for mode, rule, canon in (
                ("priority", priority_of, ["High", "Normal", "Low"]),
                ("horizon", horizon_of,
                 ["Overdue", "This week", "Later", "No date", "Done"]),
                ("project", None, None)):
            await pilot.press(g_key)
            await pilot.pause()
            assert app.kanban_group == mode
            text = board_text(app)
            names, cols = _painted_kanban(app)
            if mode == "project":                   # the cycle closed
                assert "ProjA" in text and "ProjB" in text
                assert "Overdue" not in text and "No date" not in text
                continue
            header_line = text.split("\n")[0]
            assert f"group: {mode}" in header_line
            for ci, col in enumerate(cols):
                tasks = [t for t in board.tasks
                         if t.phase == names[ci] and t.title in
                         {w for kind, w in col if kind == "t"}]
                headers = [w for kind, w in col if kind == "h"]
                want = [h for h in canon if any(rule(t) == h for t in tasks)]
                assert headers == want, f"column {names[ci]}: {headers} != {want}"
                above = None                        # membership: nearest header
                for kind, w in col:
                    if kind == "h":
                        above = w
                    else:
                        t = next(t for t in tasks if t.title == w)
                        assert rule(t) == above, \
                            f"{w} sits under {above}, belongs in {rule(t)}"
                assert {t.title for t in tasks} == \
                    {w for kind, w in col if kind == "t"}   # completeness
            assert "ProjA" not in text and "ProjB" not in text


async def test_kanban_group_parity_arrow_walk(tmp_path):
    """AT-008 (HLR-004): under `horizon` grouping, → then ↓ land on the nav
    model's computed targets — and those tasks' titles are painted in the
    same columns. RED counterfactual: the nav branch bypassing `kanban_order`
    for grouped modes → target and paint disagree."""
    board = _mode_board(tmp_path)
    app = TaskboardApp(board_path=str(board.path))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("4")
        await pilot.pause()
        g_key = _key_for("kanban_group")
        await pilot.press(g_key)
        await pilot.press(g_key)                    # horizon
        await pilot.pause()
        from taskboard.views import nav_model
        cols = nav_model("kanban", app.board, False, kanban_group="horizon")
        app.selected_task_id = cols[0][0]           # Backlog's first card
        app.refresh_view()
        await pilot.pause()
        await pilot.press("right")                  # skips the empty Review
        nxt = next(ci for ci in range(1, len(cols)) if cols[ci])
        assert app.selected_task_id == cols[nxt][0]
        await pilot.press("down")
        assert app.selected_task_id == cols[nxt][1]
        names, painted_cols = _painted_kanban(app)  # the rendered-text limb
        painted = _painted_card_ids(app, painted_cols)
        assert painted[nxt][1] == cols[nxt][1]


def test_kanban_order_sort_modes_are_stable_and_distinct(tmp_path):
    """TC-005 (LLR-003.1, §6.5 AMD-09): every sort mode is STABLE — a tie the
    mode's own keys leave open keeps the board's pre-sort order. One project,
    one column, six tasks with a deliberate tie in EVERY key; expected orders
    recomputed from the fixture by the stated rules and asserted pairwise
    distinct FIRST (a fixture where two modes coincide reads green on a
    mode-skipping mutant). RED counterfactuals: sort by title → derived-order
    mismatch; unstable/reversed tie handling → the tie limbs red; `recent`
    reading None as oldest-first or as 0 → the None-sink limb red."""
    from datetime import timedelta
    from taskboard.views import kanban_order
    today = date.today()

    def iso(delta):
        return (today + timedelta(days=delta)).isoformat()

    p = Project("ProjS", "violet")
    tasks = [
        Task("s1", p.id, "Doing", "high", due_date=iso(3), phase_changed=iso(-4)),
        Task("s2", p.id, "Doing", "high", due_date=iso(1), phase_changed=iso(-1)),
        Task("s3", p.id, "Doing", "normal", due_date=None, phase_changed=iso(-3)),
        Task("s4", p.id, "Doing", "normal", due_date=None, phase_changed=None),
        Task("s5", p.id, "Doing", "low", due_date=iso(1), phase_changed=None),
        Task("s6", p.id, "Doing", "normal", due_date=iso(5),
             phase_changed=None, blocked=True),
    ]
    b = Board([p], tasks, tmp_path / "s.json", phases=["Backlog", "Doing", "Done"])
    titles = lambda mode: [t.title for g in
                           kanban_order(b, tasks, False, group="project",
                                        sort=mode)
                           for t in g[2]]
    orders = {m: titles(m) for m in ("project", "priority", "due", "recent")}
    assert len({tuple(o) for o in orders.values()}) == 4, "palindrome fixture"
    assert orders["project"] == ["s1", "s2", "s3", "s4", "s5", "s6"]
    # blocked first; high→normal→low; priority ties by due (s2 before s1);
    # undated sink; the undated normal tie keeps board order (s3 before s4)
    assert orders["priority"] == ["s6", "s2", "s1", "s3", "s4", "s5"]
    # blocked first; due ascending; the due tie (+1/+1) keeps board order
    # (s2 before s5); undated sink, board order kept (s3 before s4)
    assert orders["due"] == ["s6", "s2", "s5", "s1", "s3", "s4"]
    # phase_changed descending, None last, None ties in board order (s4,s5,s6)
    assert orders["recent"] == ["s2", "s3", "s1", "s4", "s5", "s6"]


def test_kanban_order_default_reproduces_kanban_groups(tmp_path):
    """TC-005 regression PIN (LLR-003.1): `group="project", sort="project"`
    reproduces today's exact `_kanban_groups` output — same (name, color,
    tasks) tuples, Inbox last included — so the seat change is invisible in
    the default mode. RED: any reordering inside the new seat (even a 'helpful'
    sort) → tuple mismatch."""
    from taskboard.views import _kanban_groups, kanban_order, phase_buckets
    b = _mode_board(tmp_path)
    for bucket in phase_buckets(b, b.visible_tasks(False)):
        assert kanban_order(b, bucket, False) == _kanban_groups(b, bucket, False)


def test_kanban_order_is_pure_and_unknown_phase_falls_to_bucket_zero(tmp_path):
    """TC-005 (HLR-003 boundary catalog): `kanban_order` does no I/O and
    mutates nothing — the board's task order is byte-equal after calls in
    every mode (the 'view sort reorders board.tasks' mutation reddens the
    LAST assertion); a task in an unknown phase lands in the FIRST nav
    column through the shared seat (`phase_buckets`' bucket-0 fallback).
    RED: any append/remove/reorder side-effect → model-order assertion red."""
    from taskboard.views import kanban_order, nav_model
    b = _mode_board(tmp_path)
    before = [t.id for t in b.tasks]
    tasks = b.visible_tasks(False)
    for sort in ("project", "priority", "due", "recent"):
        for group in ("project", "priority", "horizon"):
            kanban_order(b, tasks, False, group=group, sort=sort)
    assert [t.id for t in b.tasks] == before
    stray = Task("k10", None, "Nope")       # unknown phase, no project (Inbox)
    b.add_task(stray)
    cols = nav_model("kanban", b, False)
    assert stray.id in cols[0]
    assert all(stray.id not in col for col in cols[1:])


def test_kanban_order_horizon_boundaries_and_done_group(tmp_path):
    """TC-005 + TC-007 boundaries (LLR-004.1, §6.5 AMD-04/D-11): due today−1 →
    Overdue; today → This week; today+7 → This week; today+8 → Later; None →
    No date; a last-phase task — even with a FUTURE due — lands in the
    trailing `Done` group (dim tone, `phase_changed`-descending, unknown
    stamps sunk); empty groups emit no header. RED counterfactuals: boundary
    off-by-one (`< 7` for `<= 7`) → the +7 limb red; `done` read from the due
    date instead of the phase → the future-due limb red; Done sorted by due →
    the pinned-order limb red."""
    from datetime import timedelta
    from taskboard.views import kanban_order
    today = date.today()

    def iso(n):
        return (today + timedelta(days=n)).isoformat()

    p = Project("ProjH", "violet")
    tasks = [
        Task("hb1", p.id, "Doing", due_date=iso(-1)),
        Task("hb2", p.id, "Doing", due_date=iso(0)),
        Task("hb3", p.id, "Doing", due_date=iso(7)),
        Task("hb4", p.id, "Doing", due_date=iso(8)),
        Task("hb5", p.id, "Doing"),                          # undated
        Task("hb6", p.id, "Done", due_date=iso(30), phase_changed=iso(-1)),
        Task("hb7", p.id, "Done", phase_changed=None),
    ]
    b = Board([p], tasks, tmp_path / "h.json", phases=["Backlog", "Doing", "Done"])
    groups = kanban_order(b, tasks, False, group="horizon", today=today)
    assert [g[0] for g in groups] == ["Overdue", "This week", "Later",
                                      "No date", "Done"]
    member = {n: [t.title for t in ts] for n, _c, ts in groups}
    assert member["Overdue"] == ["hb1"]
    assert member["This week"] == ["hb2", "hb3"]    # today AND exactly +7
    assert member["Later"] == ["hb4"]               # exactly +8
    assert member["No date"] == ["hb5"]
    assert member["Done"] == ["hb6", "hb7"]         # stamped first, None sunk
    assert {n: col for n, col, _ts in groups}["Done"] == "dim"
    no_later = [t for t in tasks if t.title != "hb4"]
    groups2 = kanban_order(b, no_later, False, group="horizon", today=today)
    assert "Later" not in [g[0] for g in groups2]   # empty group: no ghost


def test_kanban_mode_actions_are_registered_and_guarded(tmp_path):
    """§3.0 / LLR-012.1 four-seat registration for `s`/`g`: a kanban-scoped
    KEYMAP entry each (placed before the arrow block), a real action on the
    app, and BOARD_ACTIONS membership (what drops them on the aperture).
    RED: entry after the arrow block → the placement assertion red; action
    missing from BOARD_ACTIONS → the frozenset limb red (the aperture probe
    below is the behavioural half)."""
    from taskboard.app import TaskboardApp
    from taskboard.keymap import KEYMAP
    by_action = {k.action: k for k in KEYMAP}
    arrow_at = next(i for i, k in enumerate(KEYMAP) if k.action == "cursor(1)")
    for action in ("kanban_sort", "kanban_group"):
        entry = by_action[action]
        assert entry.views == ("kanban",)
        assert KEYMAP.index(entry) < arrow_at
        assert action in TaskboardApp.BOARD_ACTIONS
        assert callable(getattr(TaskboardApp, f"action_{action}"))


async def test_kanban_mode_keys_are_noops_outside_kanban(tmp_path):
    """§3.0 view guard (the `action_toggle_presentation` precedent): `s`/`g`
    outside the kanban view change NOTHING — not the mode state, not a pixel.
    A key acting where the bar never advertised it is the same lie in
    reverse. RED: guard dropped → the mode state flips in swimlanes."""
    app = TaskboardApp(board_path=str(tmp_path / "g.json"))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.pause()                         # swimlanes
        before = board_text(app)
        for key in (_key_for("kanban_sort"), _key_for("kanban_group")):
            await pilot.press(key)
            await pilot.pause()
        assert app.kanban_sort == "project"
        assert app.kanban_group == "project"
        assert board_text(app) == before


async def test_kanban_mode_keys_are_dead_on_the_aperture(tmp_path):
    """HLR-012 limb for `s`/`g` (the PLAN's named aperture risk, executable):
    with the aperture on top, pressing `s`/`g` leaves the mode state AND the
    board file byte-unchanged — `check_action` drops them before they reach
    the hidden board. RED: action missing from BOARD_ACTIONS → the key acts
    on the hidden board and the state assertion fails."""
    app = TaskboardApp(board_path=str(tmp_path / "a.json"))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.pause()
        blob = Path(app.board.path).read_bytes()
        await pilot.press("6")                      # the aperture
        await pilot.pause()
        for key in (_key_for("kanban_sort"), _key_for("kanban_group")):
            await pilot.press(key)
            await pilot.pause()
        assert app.kanban_sort == "project"
        assert app.kanban_group == "project"
        assert Path(app.board.path).read_bytes() == blob


# --------------------------------------------------------------------------- #
# WIP limits in the kanban phase header (batch-04 R-05, HLR-005 / LLR-005.2,
# §6.5 AMD-08) — the model half (getter/setter/rename) lives in
# tests/test_momentum.py
# --------------------------------------------------------------------------- #
def _hex_span_covers(rendered, fragment: str, hex_color: str) -> bool:
    """True when a span carrying `hex_color` covers `fragment` in the rendered
    Content — the EMITTED form (C-42), never a re-render. Colors are compared
    as parsed textual Colors: a substring check on the style would be vacuous
    (the foreground renders as `Color(244, 63, 94)`, never as the hex)."""
    from textual.color import Color
    want = Color.parse(hex_color)
    plain = str(rendered)
    at = plain.find(fragment)
    assert at >= 0, f"{fragment!r} is not painted at all"
    for s in rendered.spans:
        fg = getattr(s.style, "foreground", None)
        if (s.start <= at and s.end >= at + len(fragment)
                and fg is not None and fg == want):
            return True
    return False


async def test_kanban_wip_header_shows_count_over_default_limit(tmp_path):
    """AT-009 (HLR-005): with the DEFAULT limit (Doing <= 3, nothing written
    into settings) the Doing header paints ` n/3`, n recomputed from the
    fixture. Exactly AT the limit the tag is calm; one task over, the fraction
    burns in the `over` tone — the boundary pair is asserted on the emitted
    spans, so an off-by-one (`>=`) reddens the at-limit limb while the over
    limb stays green. RED counterfactuals: header paints the bare count only
    (fraction assertion red); burn at `>=` (at-limit span limb red —
    EXECUTED, see increment-007)."""
    from taskboard.views import HEX
    phases = ["Backlog", "Doing", "Review", "Done"]
    doing = [Task(f"wip{i}", None, "Doing") for i in range(3)]
    b = Board([], doing + [Task("other", None, "Review")], tmp_path / "w.json",
              phases=phases)
    b.save()
    app = TaskboardApp(board_path=str(b.path))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("4")                          # kanban
        await pilot.pause()
        limit = app.board.wip_limit("Doing")
        assert limit == 3                            # the operator-approved default
        assert "wip_limits" not in app.board.settings  # ...NOT materialized on read
        n = len([t for t in app.board.visible_tasks(app.show_archived)
                 if t.phase == "Doing"])
        assert n == limit                            # the at-limit pre-state
        tag = f"{n}/{limit}"
        rendered = app.query_one("#board", Static).render()
        assert tag in str(rendered)
        assert not _hex_span_covers(rendered, tag, HEX["over"])   # calm AT limit
        app.board.add_task(Task("wip-over", None, "Doing"))
        app.refresh_view()
        await pilot.pause()
        tag2 = f"{n + 1}/{limit}"
        rendered = app.query_one("#board", Static).render()
        assert tag2 in str(rendered)
        assert _hex_span_covers(rendered, tag2, HEX["over"])      # burns OVER


async def test_kanban_wip_header_honors_a_non_default_limit(tmp_path):
    """AT-010 (HLR-005, C-10): the SAME shape with settings carrying a
    non-default limit (Doing <= 2) paints ` n/2` — never the shipped
    default — while a sibling phase with NO configured limit paints its bare
    count with no fraction. RED: the default map consulted even when the
    setting exists (paints n/3 -> both fraction limbs red; this is why the
    fixture is settings-driven)."""
    phases = ["Backlog", "Doing", "Review", "Done"]
    tasks = [Task(f"lim{i}", None, "Doing") for i in range(4)]
    tasks += [Task("loose", None, "Backlog")]
    b = Board([], tasks, tmp_path / "w2.json",
              settings={"wip_limits": {"Doing": 2}}, phases=phases)
    b.save()
    app = TaskboardApp(board_path=str(b.path))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("4")
        await pilot.pause()
        n = len([t for t in app.board.visible_tasks(app.show_archived)
                 if t.phase == "Doing"])
        assert f"{n}/2" in board_text(app)           # the OPERATOR's limit
        assert f"{n}/3" not in board_text(app)       # not the shipped default
        hdr = next(l for l in board_text(app).split("\n")
                   if all(p.upper() in l for p in phases))
        backlog_cell = next(seg for seg in hdr.split("│") if "BACKLOG" in seg)
        bare = len([t for t in app.board.visible_tasks(app.show_archived)
                    if t.phase == "Backlog"])
        assert "/" not in backlog_cell               # no fraction when unlimited
        assert f" {bare}" in backlog_cell            # ...just the bare count


def test_windowed_header_wip_tag_tones_and_boundaries(tmp_path):
    """TC-008 (LLR-005.2) boundary table over n in {0, limit-1, limit,
    limit+1} with the limit from a SETTINGS dict (not the default), plus the
    None-limit case: ` n/limit` when limited, bare ` n` when not; the tag
    burns in the `over` tone ONLY when STRICTLY over — exactly at the limit
    is calm (the off-by-one limb, reddened by the `>=` mutation). The tag is
    laid out last: it survives at MIN_COL while the name truncates first."""
    from taskboard.views import HEX, MIN_COL, _strip, _windowed_header, vis
    limit = 2                                        # NON-default (C-10)
    for count in (0, limit - 1, limit, limit + 1):
        b = Board([], [Task(f"w{i}", None, "Doing") for i in range(count)],
                  tmp_path / f"h{count}.json",
                  settings={"wip_limits": {"Doing": limit}},
                  phases=["Backlog", "Doing", "Done"])
        doing_i = b.phases.index("Doing")
        cells = _windowed_header(b, 0, [40, 40, 40], b.visible_tasks(False))
        assert f"{count}/{limit}" in cells[doing_i]     # the fraction, recomputed
        assert (HEX["over"] in cells[doing_i]) == (count > limit)
        assert all(vis(_strip(cell)) == 40 for cell in cells)   # width-exact
    # no-limit phase: bare count, no fraction (asserted on the STRIPPED text —
    # the markup's own `[/]` closers would make a raw `/` search vacuous)
    b = Board([], [Task("x", None, "Backlog")], tmp_path / "hn.json",
              phases=["Backlog", "Doing", "Done"])
    cells = _windowed_header(b, 0, [40, 40, 40], b.visible_tasks(False))
    assert "/" not in _strip(cells[0]) and " 1" in _strip(cells[0])
    # the tag survives at MIN_COL width (a long phase name truncates first)
    long_phases = ["Backlog-beyond-all-measure", "Doing", "Done"]
    b2 = Board([], [Task("y", None, "Doing")], tmp_path / "hs.json",
               phases=long_phases)
    narrow = _windowed_header(b2, 0, [MIN_COL] * 3, b2.visible_tasks(False))
    assert all(vis(_strip(cell)) == MIN_COL for cell in narrow)
    assert "/3" in narrow[1]                          # the default-limit tag held


# --------------------------------------------------------------------------- #
# card aging (batch-04 R-06, HLR-006 — AT-011) and terminal-phase collapse
# (R-07, HLR-007/LLR-007.1, §6.5 AMD-02 — AT-012, TC-010)
# --------------------------------------------------------------------------- #
def _aging_board(tmp_path, name="aging.json") -> Board:
    """The aging/collapse fixture (AT-011, AT-012): FOUR phases so the
    terminal one has a NON-EMPTY Review neighbour (the relocation target),
    three tasks resting in the terminal phase (N recomputed, never a
    literal), and titles free of `·` and digits so a token search can never
    match a title. Stamps stay well inside AUTO_ARCHIVE_DAYS so the boot
    sweep cannot touch them."""
    from datetime import timedelta
    p = Project("ProjA", "violet")
    today = date.today()

    def iso(delta):
        return (today + timedelta(days=delta)).isoformat()

    tasks = [
        Task("alpha", p.id, "Backlog", "normal", phase_changed=iso(-2)),
        Task("bravo", p.id, "Doing", "normal", phase_changed=iso(-5)),
        Task("charlie", p.id, "Doing", "normal", phase_changed=None),
        Task("delta", p.id, "Review", "normal", phase_changed=iso(-1)),
        Task("echo", p.id, "Done", "normal", phase_changed=iso(-9)),
        Task("foxtrot", p.id, "Done", "normal", phase_changed=iso(-3)),
        Task("golf", p.id, "Done", "normal", phase_changed=None),
    ]
    b = Board([p], tasks, tmp_path / name,
              phases=["Backlog", "Doing", "Review", "Done"])
    b.save()
    return b


async def test_kanban_aging_token_renders_only_for_dated_open_cards(tmp_path):
    """AT-011 (HLR-006): a card stamped 5 days ago renders `·5d` in its
    painted row; a never-stamped card renders NO token; a done card stamped
    9 days ago renders NO token either (done work rests — its age is not
    work-in-progress information). N is recomputed through `days_in_phase`,
    never a literal; rows are located by title, never by index. RED
    counterfactuals: token derived from `start_date`/`due_date` instead of
    `phase_changed` → the recomputed-N limb red; None rendered as `·0d` →
    the unstamped limb red; the done-suppression dropped → the done limb
    red (EXECUTED, see increment-008 §4)."""
    from taskboard.models import days_in_phase
    board = _aging_board(tmp_path)
    app = TaskboardApp(board_path=str(board.path))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("4")
        await pilot.pause()
        text = board_text(app)
        by_title = {t.title: t for t in board.tasks}

        def card_of(title):
            """The one painted COLUMN SEGMENT holding this card — a line is
            the whole board (several columns), so a token search must be
            confined to the card's own cell or a neighbour's token leaks in."""
            hits = [seg for l in text.split("\n") for seg in l.split("│")
                    if title in seg]
            assert len(hits) == 1, f"{title}: expected one painted card: {hits}"
            return hits[0]

        dated, undated, done = (by_title[w]
                                for w in ("bravo", "charlie", "echo"))
        n = days_in_phase(dated, date.today())
        assert n is not None and f"·{n}d" in card_of("bravo")
        assert not re.search(r"·\d+d", card_of("charlie")), \
            "an unstamped card painted an age — unknown is not zero"
        assert not re.search(r"·\d+d", card_of("echo")), \
            "a done card painted an age — done work rests"


async def test_kanban_collapse_toggles_the_terminal_phase_and_restores(tmp_path):
    """AT-012 (HLR-007, §6.5 AMD-02) — both directions, both satisfiable.
    (a) selection OUTSIDE the terminal phase: `z` leaves the terminal column
    with exactly one `✓ N` summary row (N recomputed from the fixture), none
    of its titles painted, every other column byte-identical, the nav model
    SKIPPING the phase (absent, not empty — painted/nav parity holds over
    the surviving columns), and no arrow walk landing on its tasks; `z`
    again, from there, restores the render BYTE-EXACTLY. (b) selection
    INSIDE the terminal phase: `z` relocates it to the nearest non-empty
    column's first card (the `action_hmove` landing rule) and the summary
    row still renders. RED counterfactuals: collapse filters the render but
    not the nav model → the parity/nav limbs red; N hardcoded or counting
    archived with `v` off → the recomputed-N limb red; keyed to the SELECTED
    task's phase (the superseded design) → every terminal-column limb red;
    the nav column EMPTIED instead of dropped → the nav-shape limb red
    (EXECUTED, see increment-008 §4)."""
    board = _aging_board(tmp_path)
    terminal = [t for t in board.tasks if board.is_done(t)]
    terminal_ids = {t.id for t in terminal}
    assert len(terminal) >= 2, "vacuous fixture: nothing to collapse"
    app = TaskboardApp(board_path=str(board.path))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("4")
        await pilot.pause()
        z = _key_for("collapse_toggle")

        # ---- (a) selection outside the terminal phase ---------------------
        before = board_text(app)
        assert app.selected_task_id not in terminal_ids
        # every other column UNCHANGED, asserted on the painted text per
        # column (the 01b §4 anchor machinery): a raw line-by-line compare
        # cannot work here — the collapsed column is SHORTER, so the frame's
        # rows below it shift up — but each surviving column's painted rows
        # (headers and cards, in order) must be exactly what they were
        names0, cols0 = _painted_kanban(app)
        await pilot.press(z)
        await pilot.pause()
        text = board_text(app)
        n = len([t for t in board.visible_tasks(app.show_archived)
                 if board.is_done(t)])
        summary = [l for l in text.split("\n") if f"✓ {n}" in l]
        assert len(summary) == 1, f"expected one `✓ {n}` summary row: {summary}"
        for t in terminal:
            assert t.title not in text, f"{t.title} still painted under collapse"
        names, cols = _painted_kanban(app)
        assert names == names0 == list(board.phases)   # headers untouched
        assert cols[:-1] == cols0[:-1], \
            "collapse leaked into a neighbouring column"
        assert [r for r in cols[-1] if r[0] == "t"] == [], \
            "the collapsed column still paints cards"
        # the nav model SKIPS the phase — absent, not empty — and parity
        # holds over the surviving columns (01b §4 in the collapsed state,
        # LLR-007.1's "parity oracle covers ≥ 1 collapsed combination")
        nav = app._nav_columns()
        assert len(nav) == len(board.phases) - 1, \
            "the collapsed phase must be ABSENT from the nav model, not empty"
        assert not terminal_ids & {tid for col in nav for tid in col}
        assert _painted_card_ids(app, cols)[:-1] == nav, \
            "painted order != nav order in the collapsed state"
        # restore is BYTE-EXACT, from anywhere (the selection never moved)
        await pilot.press(z)
        await pilot.pause()
        assert board_text(app) == before, "restore is not byte-exact"
        # the arrow walk never lands the highlight on a terminal task
        await pilot.press(z)
        await pilot.pause()
        for key in ("right", "right", "right", "down", "down", "left"):
            await pilot.press(key)
            assert app.selected_task_id not in terminal_ids, \
                f"{key}: the cursor reached a task the board no longer draws"
        await pilot.press(z)                    # restore for limb (b)
        await pilot.pause()

        # ---- (b) selection inside the terminal phase ----------------------
        for _ in range(3):                        # walk right into Done
            await pilot.press("right")
        sel = app.selected_task
        assert sel is not None and board.is_done(sel), \
            "the fixture walk did not land inside the terminal phase"
        await pilot.press(z)
        await pilot.pause()
        expected = next(t for t in board.tasks if t.phase == board.phases[-2])
        assert app.selected_task_id == expected.id, \
            "the selection did not relocate to the nearest visible task"
        assert f"✓ {n}" in board_text(app), "the summary row did not render"


def test_kanban_collapsed_column_shape_and_nav_exclusion(tmp_path):
    """TC-010 (HLR-007/LLR-007.1), white-box: for the collapsed terminal
    phase, `_kanban_column_rows` emits EXACTLY ONE `(markup, None)` row —
    `✓ N`, N the phase's visible count recomputed — and the kanban
    `nav_model` branch contributes NOTHING for it: the column is ABSENT, not
    empty — while a genuinely EMPTY phase (Review in this fixture) KEEPS its
    empty column (the ux B-1 distinction: an empty nav column is still a
    place, a collapsed one no longer exists). The flag also flows THROUGH
    the shared seat: `kanban_order(collapsed=True)` returns no groups. The
    selection-relocation pin of TC-010 is the behavioural limb — AT-012(b)
    above (folded, V-5). RED: collapse empties the nav column instead of
    dropping it → the nav-length/`full[:-1]` limbs red (EXECUTED, see
    increment-008 §4); summary count hardcoded or counting archived → the
    recomputed-N limb red; the row given a task id → the None limb red (the
    row would be selectable)."""
    from rich.text import Text
    from rich.cells import cell_len

    from taskboard.views import _kanban_column_rows, kanban_order, nav_model
    board = _mode_board(tmp_path)               # Review is EMPTY by design
    terminal = [t for t in board.visible_tasks(False) if board.is_done(t)]
    assert terminal, "vacuous fixture: the terminal phase is empty"

    rows = _kanban_column_rows(board, terminal, 24, None, False,
                               collapsed=True)
    assert len(rows) == 1, f"a collapsed column emitted {len(rows)} rows"
    markup, tid = rows[0]
    assert tid is None, "the summary row must be non-selectable"
    plain = Text.from_markup(markup).plain
    assert plain.strip() == f"✓ {len(terminal)}"
    assert cell_len(plain) == 24, "the summary row is not width-exact"

    # the flag is an INPUT TO THE SEAT (LLR-007.1), on both paths
    assert kanban_order(board, terminal, False, collapsed=True) == []
    assert kanban_order(board, terminal, False) != []

    full = nav_model("kanban", board, False)
    collapsed = nav_model("kanban", board, False, kanban_collapsed=True)
    assert len(full) == len(board.phases)
    review_i = board.phases.index("Review")
    assert full[review_i] == [], "fixture guard: Review must be empty"
    assert collapsed == full[:-1], \
        "the nav model with collapse is not exactly full-minus-terminal"
    assert collapsed[review_i] == [], \
        "a genuinely EMPTY phase lost its column — absent is not empty"


def test_matrix_presentation_nav_ignores_the_modes_like_the_render(tmp_path):
    """Phase-4 PDR ruling (the 3-carry divergence: sort/group Inc-006,
    collapse Inc-008, focus Inc-009 — matrix render routes BEFORE the mode
    seat, so a nav that honors the modes parks the cursor on cards the screen
    does not draw, the F-3 trap in miniature). Rule: in matrix BOTH seats
    ignore sort/group/collapse/focus, so the nav walks exactly what the
    matrix draws. RED: nav keeping the focus filter under matrix → the
    includes-every-visible-task limb red; nav dropping the terminal phase
    under matrix+collapsed → the terminal-present limb red."""
    from taskboard.views import nav_model
    board = _mode_board(tmp_path)
    proj_b = next(p for p in board.projects if p.name == "ProjB")
    b_tasks = {t.id for t in board.visible_tasks(False)
               if t.project_id == proj_b.id}
    all_visible = {t.id for t in board.visible_tasks(False)}
    assert b_tasks and b_tasks < all_visible, "vacuous fixture guard"

    grouped = nav_model("kanban", board, False, kanban_focus=proj_b.id,
                        presentation="grouped")
    assert {tid for col in grouped for tid in col} == b_tasks, \
        "grouped+focus must show ONLY the focused project's cards"

    matrix = nav_model("kanban", board, False, kanban_focus=proj_b.id,
                       kanban_collapsed=True, kanban_sort="due",
                       kanban_group="horizon", presentation="matrix")
    flat = {tid for col in matrix for tid in col}
    assert flat == all_visible, \
        "matrix nav must walk exactly what the matrix draws (modes ignored)"
    assert len(matrix) == len(board.phases), \
        "matrix nav keeps the terminal column even with the collapse flag on"


def test_collapse_action_is_registered_and_guarded(tmp_path):
    """§3.0 four-seat registration for `z` (the `s`/`g` precedent): a
    kanban-scoped KEYMAP entry placed before the arrow block, a real action
    on the app, and BOARD_ACTIONS membership (what drops it on the
    aperture). RED: entry after the arrow block → the placement limb red;
    action missing from BOARD_ACTIONS → the frozenset limb red (the aperture
    probe below is the behavioural half)."""
    from taskboard.keymap import KEYMAP
    by_action = {k.action: k for k in KEYMAP}
    entry = by_action["collapse_toggle"]
    assert entry.keys == "z"
    assert entry.views == ("kanban",)
    arrow_at = next(i for i, k in enumerate(KEYMAP) if k.action == "cursor(1)")
    assert KEYMAP.index(entry) < arrow_at
    assert "collapse_toggle" in TaskboardApp.BOARD_ACTIONS
    assert callable(getattr(TaskboardApp, "action_collapse_toggle"))


async def test_collapse_key_is_a_noop_outside_kanban(tmp_path):
    """§3.0 view guard (the `action_toggle_presentation` precedent): `z`
    outside the kanban view changes NOTHING — not the flag, not a pixel. A
    key acting where the bar never advertised it is the same lie in
    reverse. RED: guard dropped → the flag flips in swimlanes."""
    app = TaskboardApp(board_path=str(tmp_path / "guard.json"))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.pause()                         # swimlanes
        before = board_text(app)
        await pilot.press(_key_for("collapse_toggle"))
        await pilot.pause()
        assert app.kanban_collapsed is False
        assert board_text(app) == before


async def test_collapse_key_is_dead_on_the_aperture(tmp_path):
    """The PLAN's named aperture risk, for `z`: with the aperture on top,
    pressing `z` leaves the collapse flag AND the board file byte-unchanged
    — `check_action` drops BOARD_ACTIONS there. RED: the action missing from
    BOARD_ACTIONS → the key acts on the hidden board → the flag limb red."""
    app = TaskboardApp(board_path=str(tmp_path / "ap.json"))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.pause()
        blob = Path(app.board.path).read_bytes()
        await pilot.press("6")                      # the aperture
        await pilot.pause()
        await pilot.press(_key_for("collapse_toggle"))
        await pilot.pause()
        assert app.kanban_collapsed is False
        assert Path(app.board.path).read_bytes() == blob


# ---------------------------------------------------------------------------
# Inc 5 — focus mode (R-08), due-date bump keys (R-09), undo (R-10)
# ---------------------------------------------------------------------------
def _focus_board(tmp_path, name="focus.json") -> Board:
    """The focus fixture (AT-013, TC-011): THREE projects so "no other
    project renders" quantifies over ≥ 2 others, plus one project-less task
    — Inbox is NEVER a focus target (§6.2 D-5), so any focus hides it.
    Titles unique and substring-free; FOUR phases so focused tasks can sit
    in different columns."""
    pa, pb, pc = (Project("AlphaP", "sky"), Project("BetaP", "lime"),
                  Project("GammaP", "pink"))
    tasks = [
        Task("alfa1", pa.id, "Doing"),
        Task("alfa2", pa.id, "Review"),
        Task("beta1", pb.id, "Doing"),
        Task("gama1", pc.id, "Backlog"),
        Task("loose1", None, "Doing"),      # Inbox: hidden by ANY focus
    ]
    b = Board([pa, pb, pc], tasks, tmp_path / name,
              phases=["Backlog", "Doing", "Review", "Done"])
    b.save()
    return b


async def test_focus_cycle_filters_the_board_and_escape_restores(tmp_path):
    """AT-013 (HLR-008): one `F` leaves only the first visible project's
    titles on screen and names it in the header; the next `F` reaches a
    DIFFERENT project; the Inbox task hides under any focus (D-5); cycling
    past the last project turns the focus OFF (full board, unnamed header);
    `escape` with an active focus restores every title and un-names the
    header; `escape` with NO focus active is a pure no-op (byte-identical
    paint) and never eats a modal's own escape (§6.5 AMD-03). Nav
    companion: under focus the nav model covers EXACTLY the rendered tasks
    — a filter that hides cards but leaves them navigable parks the cursor
    on an undrawn task (the F-3 trap in a new costume). RED
    counterfactuals: focus filters render but not nav → the nav limb red;
    header does not name the focus → the header limb red; escape SWALLOWED
    without an active focus (a priority binding) → the modal limb red
    (EXECUTED, see increment-009 §4)."""
    board = _focus_board(tmp_path)
    pa, pb, pc = board.projects
    titles = [t.title for t in board.tasks]
    app = TaskboardApp(board_path=str(board.path))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("4")
        await pilot.pause()
        f_key, esc = _key_for("focus_cycle"), _key_for("focus_exit")

        def header() -> str:
            return board_text(app).split("\n")[0]

        # ---- one F: only AlphaP renders, the header names it ---------------
        await pilot.press(f_key)
        await pilot.pause()
        assert app.focused_project_id == pa.id
        text = board_text(app)
        assert "alfa1" in text and "alfa2" in text
        for gone in ("beta1", "gama1", "loose1"):
            assert gone not in text, f"{gone} still painted under a focus"
        assert pa.name in header() and "focus" in header()
        # the nav companion: exactly the rendered tasks are navigable
        nav_ids = {i for col in app._nav_columns() for i in col}
        assert nav_ids == {t.id for t in board.tasks if t.project_id == pa.id}
        assert app.selected_task_id in nav_ids

        # ---- cycle: a DIFFERENT project, same law --------------------------
        await pilot.press(f_key)
        await pilot.pause()
        assert app.focused_project_id == pb.id
        text = board_text(app)
        assert "beta1" in text
        for gone in ("alfa1", "alfa2", "gama1", "loose1"):
            assert gone not in text
        assert pb.name in header()

        # ---- past the last project: focus OFF, the full board returns ------
        await pilot.press(f_key)                        # GammaP
        await pilot.pause()
        assert app.focused_project_id == pc.id
        await pilot.press(f_key)                        # ...and then off
        await pilot.pause()
        assert app.focused_project_id is None
        text = board_text(app)
        for w in titles:
            assert w in text, f"{w} not restored after the cycle closed"
        assert "focus" not in header()

        # ---- escape exits ONLY an active focus -----------------------------
        await pilot.press(f_key)
        await pilot.pause()
        assert app.focused_project_id == pa.id
        await pilot.press(esc)
        await pilot.pause()
        assert app.focused_project_id is None
        text = board_text(app)
        for w in titles:
            assert w in text, f"{w} not restored by escape"
        assert "focus" not in header()

        # ---- passthrough: no focus -> escape is a pure no-op ---------------
        before = board_text(app)
        await pilot.press(esc)
        await pilot.pause()
        assert app.focused_project_id is None
        assert board_text(app) == before

        # ---- ...and it never eats a modal's escape (§6.5 AMD-03) -----------
        app.selected_task_id = board.tasks[0].id
        app.refresh_view()
        await pilot.pause()
        await pilot.press(_key_for("delete"))           # the confirm modal
        await pilot.pause()
        assert len(app.screen_stack) > 1
        await pilot.press(esc)
        await pilot.pause()
        assert len(app.screen_stack) == 1, \
            "escape was swallowed before the modal could see it"
        assert board.task_by_id(board.tasks[0].id) is not None  # not deleted


async def test_focus_cycle_order_seat_filter_and_archived_drop(tmp_path):
    """TC-011 (HLR-008/LLR-008.1), white-box pins beyond AT-013: the cycle
    order is EXACTLY `visible_projects` order ending in None and closing the
    loop; the filter lives in the shared ordering SEAT (`kanban_order` takes
    the focus as an INPUT, like collapse — never a parallel filter); a focus
    naming a project archived mid-session drops to None on the next refresh;
    both actions are guarded no-ops outside the kanban view."""
    from taskboard.views import kanban_order
    board = _focus_board(tmp_path)
    pa, pb, pc = board.projects
    app = TaskboardApp(board_path=str(board.path))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("4")
        await pilot.pause()
        order = []
        for _ in range(4):                          # one FULL cycle, to off
            app.action_focus_cycle()
            order.append(app.focused_project_id)
        assert order == [pa.id, pb.id, pc.id, None]
        # the filter is an INPUT TO THE SEAT (the LLR-003.1 one-seat law)
        tasks = board.visible_tasks(False)
        focused = kanban_order(board, tasks, False, focus=pb.id)
        got = {t.id for _n, _c, items in focused for t in items}
        assert got == {t.id for t in tasks if t.project_id == pb.id}
        assert got != {t.id for t in tasks}, "vacuous: the filter hid nothing"
        # archived mid-session: the focus drops on the next refresh
        app.focused_project_id = pc.id
        app.board.projects[2].archived = True       # the app's OWN board —
        app.board.save()                            # the fixture is its load
        app.refresh_view()
        await pilot.pause()
        assert app.focused_project_id is None
        # guarded no-ops outside kanban (the bar never advertises them there)
        await pilot.press("1")
        await pilot.pause()
        app.action_focus_cycle()
        assert app.focused_project_id is None
        app.action_focus_exit()
        assert app.focused_project_id is None


def test_focus_due_undo_actions_are_registered_and_guarded(tmp_path):
    """§3.0 four-seat registration for `F` / `+,=` / `-` / `u` / escape:
    KEYMAP entries (kanban-scoped where §3.0 says so, global where it does
    not) placed BEFORE the arrow block, real actions on the app,
    BOARD_ACTIONS membership (what drops them on the aperture). The `=`
    alias is ONE `"+,="` entry driving `due_bump(1)` — never a second key,
    never a set-to-today (§6.5 AMD-06). RED: the alias split into two
    entries → the single-entry limb red; an entry after the arrow block →
    the placement limb red; an action missing from BOARD_ACTIONS → the
    aperture probe below is the behavioural half."""
    from taskboard.keymap import KEYMAP
    by_action = {k.action: k for k in KEYMAP}
    assert by_action["due_bump(1)"].keys == "+,="       # ONE aliased entry
    assert by_action["due_bump(-1)"].keys == "-"
    assert by_action["undo"].keys == "u"
    assert by_action["focus_cycle"].keys == "F"
    assert by_action["focus_cycle"].views == ("kanban", "gantt")
    assert by_action["focus_exit"].keys == "escape"
    assert by_action["focus_exit"].views == ("kanban", "gantt")
    assert by_action["due_bump(1)"].views is None       # selection-scoped,
    assert by_action["undo"].views is None              # like the other
    arrow_at = next(i for i, k in enumerate(KEYMAP)     # quick keys
                    if k.action == "cursor(1)")
    for action in ("focus_cycle", "due_bump(1)", "due_bump(-1)", "undo",
                   "focus_exit"):
        assert KEYMAP.index(by_action[action]) < arrow_at, action
    for action in ("focus_cycle", "focus_exit", "due_bump", "undo"):
        assert action in TaskboardApp.BOARD_ACTIONS, action
    for method in ("action_focus_cycle", "action_focus_exit",
                   "action_due_bump", "action_undo"):
        assert callable(getattr(TaskboardApp, method)), method


async def test_focus_due_undo_keys_are_dead_on_the_aperture(tmp_path):
    """The PLAN's named aperture risk for the Inc-5 keys: with the aperture
    on top, `F` `+` `-` `u` leave the focus, the undo stack AND the board
    file untouched — `check_action` drops BOARD_ACTIONS there. (escape is
    the aperture's OWN pop binding, so it is not in this probe's set.)
    RED: an action missing from BOARD_ACTIONS → its key acts on the hidden
    board → the corresponding limb red."""
    board = _ops_board(tmp_path, Task("Widget", None, "Doing",
                                      due_date="2026-01-01"))
    app = TaskboardApp(board_path=str(board.path))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("4")
        await pilot.pause()
        await pilot.press("6")                          # the aperture
        await pilot.pause()
        blob = Path(app.board.path).read_bytes()
        for key in (_key_for("focus_cycle"), _key_for("due_bump(1)"),
                    _key_for("due_bump(-1)"), _key_for("undo")):
            await pilot.press(key)
            await pilot.pause()
        assert app.focused_project_id is None
        assert app._undo_stack == []
        assert Path(app.board.path).read_bytes() == blob
        assert app.board.tasks[0].due_date == "2026-01-01"


async def test_due_bump_moves_dated_and_undated_tasks_forward(tmp_path):
    """AT-014 (HLR-009): `+` on a task due in 5 days persists today+6
    (reloaded JSON, C-12) and the due readout renders `+6d`; `+` on an
    UNDATED task bases on today → today+1, readout `+1d`. The key is
    pressed on the kanban (the shipped surface); the relative due token is
    read in the AGENDA view — the one surface that paints `reldue_token`
    (the kanban card has no due readout; flagged in increment-009 §6).
    Expected dates are recomputed from `date.today()` at assert time,
    never chained from earlier assertions. RED counterfactuals: the bump
    applied to `start_date` or never saved → the JSON limbs red; no
    re-render → the painted-token limbs red while the model limbs stay
    green."""
    from datetime import timedelta
    today = date.today()
    dated = Task("dated1", None, "Doing",
                 due_date=(today + timedelta(days=5)).isoformat())
    plain = Task("plain1", None, "Doing", due_date=None)
    board = _ops_board(tmp_path, dated, plain)
    app = TaskboardApp(board_path=str(board.path))
    plus = _key_for("due_bump(1)")
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("4")
        await pilot.pause()

        app.selected_task_id = dated.id
        app.refresh_view()
        await pilot.pause()
        await pilot.press(plus)
        await pilot.pause()
        want = (today + timedelta(days=6)).isoformat()
        assert Board.load(board.path).task_by_id(dated.id).due_date == want
        await pilot.press("2")                          # agenda: the token
        await pilot.pause()
        assert "+6d" in _card_row(app, "dated1")
        await pilot.press("4")
        await pilot.pause()

        app.selected_task_id = plain.id
        app.refresh_view()
        await pilot.pause()
        await pilot.press(plus)
        await pilot.pause()
        want = (today + timedelta(days=1)).isoformat()
        assert Board.load(board.path).task_by_id(plain.id).due_date == want
        await pilot.press("2")
        await pilot.pause()
        assert "+1d" in _card_row(app, "plain1")


async def test_due_bump_minus_and_the_equals_alias(tmp_path):
    """AT-015 (HLR-009, §6.5 AMD-06): `-` moves a dated task one day
    EARLIER; `=` behaves EXACTLY as `+` — dated task +1 day, undated task
    today+1 — the alias is BOUND, not just shown (the seat's ONE `"+,="`
    entry, pinned in the registration node). The today boundary: a task
    due TODAY bumped `-` crosses to yesterday and the painted token flips
    to the overdue `-1d` form — a clamp-at-today mutation reddens exactly
    that limb. RED counterfactual: `=` implementing the superseded
    set-to-today → the +1 limbs red."""
    from datetime import timedelta

    from taskboard.keymap import KEYMAP
    today = date.today()
    minus = Task("minus1", None, "Doing",
                 due_date=(today + timedelta(days=5)).isoformat())
    alias = Task("alias1", None, "Doing",
                 due_date=(today + timedelta(days=5)).isoformat())
    loose = Task("loose1", None, "Doing", due_date=None)
    edge = Task("edgecase1", None, "Doing", due_date=today.isoformat())
    board = _ops_board(tmp_path, minus, alias, loose, edge)
    app = TaskboardApp(board_path=str(board.path))
    minus_key = _key_for("due_bump(-1)")
    # the alias, read off the seat's ONE entry — never typed as a literal
    eq = next(k for k in KEYMAP if k.action == "due_bump(1)").keys.split(",")[1]
    assert eq == "=", "the seat no longer aliases `=` to `+`"
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("4")
        await pilot.pause()

        async def bump(tid, key):
            app.selected_task_id = tid
            app.refresh_view()
            await pilot.pause()
            await pilot.press(key)
            await pilot.pause()

        await bump(minus.id, minus_key)
        want = (today + timedelta(days=4)).isoformat()
        assert Board.load(board.path).task_by_id(minus.id).due_date == want

        await bump(alias.id, eq)                        # `=` IS `+`
        want = (today + timedelta(days=6)).isoformat()
        assert Board.load(board.path).task_by_id(alias.id).due_date == want

        await bump(loose.id, eq)                        # undated: base today
        want = (today + timedelta(days=1)).isoformat()
        assert Board.load(board.path).task_by_id(loose.id).due_date == want

        await bump(edge.id, minus_key)                  # across the boundary
        want = (today - timedelta(days=1)).isoformat()
        assert Board.load(board.path).task_by_id(edge.id).due_date == want
        await pilot.press("2")                          # agenda: the token
        await pilot.pause()
        assert "-1d" in _card_row(app, "edgecase1"), \
            "the token did not flip to the overdue form"


async def test_undo_restores_the_phase_and_its_stamp_verbatim(tmp_path):
    """AT-016 (HLR-010): `]` moves + stamps; `u` puts the card back in its
    original column AND restores the pre-mutation stamp VERBATIM — None
    included (reloaded JSON, C-12). Restoring the phase but leaving the
    fresh stamp is the cheap wrong implementation, and only the stamp limb
    catches it. RED counterfactual: undo restores `phase` but not
    `phase_changed` (or vice versa) → the JSON limbs red."""
    task = Task("Widget", None, "Doing", phase_changed=None)
    board = _ops_board(tmp_path, task)
    app = TaskboardApp(board_path=str(board.path))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("4")
        await pilot.pause()
        assert _painted_column(app, "Widget") == "Doing"    # pre-state
        await pilot.press(_key_for("phase_move(1)"))
        await pilot.pause()
        assert _painted_column(app, "Widget") == "Review"
        assert Board.load(board.path).task_by_id(task.id).phase_changed \
            is not None
        await pilot.press(_key_for("undo"))
        await pilot.pause()
        assert _painted_column(app, "Widget") == "Doing"
        reloaded = Board.load(board.path).task_by_id(task.id)
        assert reloaded.phase == "Doing"
        assert reloaded.phase_changed is None, \
            "the phase came back but the stamp stayed — a half-restore"


async def test_undo_covers_archive_and_delete_but_not_modal_add(tmp_path):
    """AT-016b (HLR-010, §6.5 AMD-05): `x` on a live task then `u` restores
    `archived` to False (reloaded JSON); `d`+confirm then `u` resurrects
    the task with the SAME id — id equality is the discriminating
    assertion, a resurrected copy breaks line_map, nav and every later
    undo; a task added through the MODAL is NOT undoable: `u` after it
    fires the nothing-to-undo notification and the added task STAYS.
    RED counterfactuals (EXECUTED, see increment-009 §4):
    resurrect-with-new-id → the id limb red; modal add pushing an undo
    entry whose undo removes the task → the stays-put limb red."""
    task = Task("Widget", None, "Doing")
    board = _ops_board(tmp_path, task)
    app = TaskboardApp(board_path=str(board.path))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("4")
        await pilot.pause()

        # archive `x`, undone
        app.selected_task_id = task.id
        app.refresh_view()
        await pilot.pause()
        await pilot.press(_key_for("archive"))
        await pilot.pause()
        assert Board.load(board.path).task_by_id(task.id).archived is True
        await pilot.press(_key_for("undo"))
        await pilot.pause()
        assert Board.load(board.path).task_by_id(task.id).archived is False

        # delete `d` + confirm, undone -> back with the SAME id
        app_task = app.board.task_by_id(task.id)    # the app's own instance
        app.selected_task_id = task.id
        app.refresh_view()
        await pilot.pause()
        await pilot.press(_key_for("delete"))
        await pilot.pause()
        app.screen.query_one("#yes", Button).press()
        await pilot.pause()
        assert Board.load(board.path).task_by_id(task.id) is None
        await pilot.press(_key_for("undo"))
        await pilot.pause()
        reloaded = Board.load(board.path).task_by_id(task.id)
        assert reloaded is not None, "the delete was not undone"
        assert reloaded.id == task.id, "resurrected with a NEW id — a copy"
        assert app.board.task_by_id(task.id) is app_task, \
            "resurrected as a re-instantiated copy, not the same object"

        # a modal add is NOT undoable: `u` says so and the task STAYS
        seen = []
        app.notify = lambda *a, **k: seen.append(k.get("title", ""))
        await pilot.press("a")
        await pilot.pause()
        app.screen.query_one("#f-title", Input).value = "MODALTASK"
        await save_open_modal(app, pilot)
        assert any(t.title == "MODALTASK" for t in app.board.tasks)
        await pilot.press(_key_for("undo"))
        await pilot.pause()
        assert "Undo" in seen, "no nothing-to-undo notification fired"
        assert any(t.title == "MODALTASK"
                   for t in Board.load(board.path).tasks), \
            "a modal add was undone — creation is deliberate (AMD-05)"


async def test_undo_is_lifo_and_the_empty_stack_says_so(tmp_path):
    """AT-017 (HLR-010): `!` then `b` then `u` undoes the BLOCKED flag
    first (LIFO — the priority is still high); the second `u` restores
    the priority; the third finds the stack EMPTY: the board file is
    byte-untouched and the nothing-to-undo notification fires. RED
    counterfactuals: FIFO pop order → the first-pop limbs red; an
    empty-pop mutating state → the byte-equality limb red."""
    task = Task("Widget", None, "Doing")                # normal, unblocked
    board = _ops_board(tmp_path, task)
    app = TaskboardApp(board_path=str(board.path))
    seen = []
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("4")
        await pilot.pause()
        app.selected_task_id = task.id
        app.refresh_view()
        await pilot.pause()
        t = app.board.task_by_id(task.id)
        await pilot.press(_key_for("prio_cycle"))
        await pilot.pause()
        assert t.priority == "high"
        await pilot.press(_key_for("toggle_blocked"))
        await pilot.pause()
        assert t.blocked is True
        await pilot.press(_key_for("undo"))
        await pilot.pause()
        assert t.blocked is False, "LIFO violated: blocked not undone first"
        assert t.priority == "high", "LIFO violated: priority undone first"
        await pilot.press(_key_for("undo"))
        await pilot.pause()
        assert t.priority == "normal"
        assert t.blocked is False
        # the empty stack: no write, no mutation, and it SAYS so
        app.notify = lambda *a, **k: seen.append(k.get("title", ""))
        blob = Path(app.board.path).read_bytes()
        await pilot.press(_key_for("undo"))
        await pilot.pause()
        assert Path(app.board.path).read_bytes() == blob, "empty pop wrote"
        assert "Undo" in seen, "no nothing-to-undo notification fired"
        assert t.priority == "normal" and t.blocked is False


async def test_undo_stack_snapshot_stale_skip_and_no_write_on_empty(tmp_path):
    """TC-013 (HLR-010/LLR-010.1), white-box pins beyond the ATs (selector
    `-k undo_stack`): an empty pop fires the notification and writes
    NOTHING — twice, so a phantom entry cannot hide behind the first pop;
    the snapshot records the six mutable fields VERBATIM, None stamp
    included; an entry whose task was PURGED since the snapshot (the one
    destructive route undo does not cover) is SKIPPED without raising —
    the same notification, no crash, no resurrection."""
    task = Task("Widget", None, "Doing", phase_changed=None)
    board = _ops_board(tmp_path, task)
    app = TaskboardApp(board_path=str(board.path))
    seen = []
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("4")
        await pilot.pause()
        # empty stack: notification + no write, twice (no phantom entry)
        app.notify = lambda *a, **k: seen.append(k.get("title", ""))
        blob = Path(app.board.path).read_bytes()
        for _ in range(2):
            app.action_undo()
            await pilot.pause()
        assert seen == ["Undo", "Undo"]
        assert Path(app.board.path).read_bytes() == blob
        # the snapshot is field-verbatim, None stamp included
        app.selected_task_id = task.id
        app.refresh_view()
        await pilot.pause()
        await pilot.press(_key_for("prio_cycle"))
        await pilot.pause()
        entry = app._undo_stack[-1]
        assert entry["task_id"] == task.id
        assert entry["fields"] == {"phase": "Doing", "phase_changed": None,
                                   "priority": "normal", "blocked": False,
                                   "due_date": None, "archived": False,
                                   "pinned": False}
        # purged since the snapshot -> the entry is SKIPPED, no raise
        app.board.delete_task(task.id)      # the route undo does not cover
        await pilot.pause()
        app.action_undo()
        await pilot.pause()
        assert app._undo_stack == []
        assert seen[-1] == "Undo", "the stale entry was not skipped cleanly"
        assert Board.load(board.path).task_by_id(task.id) is None


# --------------------------------------------------------------------------- #
# weekly standup modal on `S` (batch-04 R-11, HLR-011 / LLR-011.1 / LLR-011.2)
# --------------------------------------------------------------------------- #
def _modal_lines(app) -> list[str]:
    """The pushed modal's text, line by line — the labels the reader sees,
    read off the pushed screen's own widgets (never a re-render of the
    board underneath)."""
    from textual.widgets import Label
    return [str(w.render()) for w in app.screen.query(Label)]


def _standup_window_members(tasks, today):
    """The rule-derived window set, RESTATED from HLR-011 (never computed by
    calling `standup_query` — that would make the oracle a second copy of the
    suspect): visible tasks stamped with today-7 <= phase_changed <= today,
    a None or corrupt stamp OUT."""
    from datetime import timedelta

    from taskboard.models import parse_iso
    week_ago = today - timedelta(days=7)
    return {t.title for t in tasks if not t.archived
            and (d := parse_iso(t.phase_changed)) is not None
            and week_ago <= d <= today}


def test_standup_action_is_registered_and_guarded(tmp_path):
    """§3.0 / LLR-012.1 four-seat registration for `S`: a global KEYMAP entry
    (the standup reads the board in ANY view, like `R` — not kanban-scoped)
    placed BEFORE the arrow block, a real `action_standup` on the app, and
    BOARD_ACTIONS membership (what drops it on the aperture — AT-019 below is
    the behavioural half). RED: entry after the arrow block → the placement
    limb red; action missing from BOARD_ACTIONS → the frozenset limb red."""
    from taskboard.keymap import KEYMAP
    by_action = {k.action: k for k in KEYMAP}
    entry = by_action["standup"]
    assert entry.keys == "S"
    assert entry.views is None                    # global, like `R`
    arrow_at = next(i for i, k in enumerate(KEYMAP)
                    if k.action == "cursor(1)")
    assert KEYMAP.index(entry) < arrow_at
    assert "standup" in TaskboardApp.BOARD_ACTIONS
    assert callable(getattr(TaskboardApp, "action_standup"))


async def test_standup_modal_lists_the_week_grouped_and_marked(tmp_path):
    """AT-018 (HLR-011): `S` opens a modal listing this week's movers grouped
    per project — moved rows wear `→`, closed rows wear `✓`, each project
    closes with its recomputed `closed/total` line — and NOTHING outside the
    window appears: the exactly-7-days stamp is IN, 8 and 10 days are OUT,
    the never-stamped task is OUT. Esc dismisses and the modal mutated
    nothing (the board file is byte-unchanged across open+close). RED
    counterfactuals: window off-by-one (`>` for `>=` → the 7d task out; an
    8-day window → the 8d task in) → the boundary limbs red; a None stamp
    read as 0 → the never-stamped task leaks in → the exclusion limb red;
    membership read from a stored field instead of `phase_changed` → the
    inclusion limbs red; done counted off a literal "Done" instead of the
    terminal phase → the ✓ limb red on a renamed phase; count arithmetic
    off → the recomputed fraction limb red."""
    from datetime import timedelta
    today = date.today()

    def iso(n: int) -> str:
        return (today + timedelta(days=n)).isoformat()

    alpha = Project("Alpha", "sky")
    beta = Project("Beta", "lime")
    tasks = [
        Task("MOVEDTODAY", alpha.id, "Review", phase_changed=iso(0)),
        Task("CLOSEDWEEK", alpha.id, "Done", phase_changed=iso(-5)),
        Task("BOUNDARY7", alpha.id, "Doing", phase_changed=iso(-7)),
        Task("OUTEIGHT", alpha.id, "Backlog", phase_changed=iso(-8)),
        Task("BETAMOVED", beta.id, "Doing", phase_changed=iso(-2)),
        Task("OUTTEN", beta.id, "Doing", phase_changed=iso(-10)),
        Task("NEVERMOVED", beta.id, "Doing", phase_changed=None),
    ]
    board = Board([alpha, beta], tasks, tmp_path / "s.json",
                  phases=["Backlog", "Doing", "Review", "Done"])
    board.save()
    app = TaskboardApp(board_path=str(board.path))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.pause()
        blob = Path(app.board.path).read_bytes()
        await pilot.press(_key_for("standup"))
        await pilot.pause()
        from taskboard.modals import StandupModal
        assert isinstance(app.screen, StandupModal)
        lines = _modal_lines(app)
        text = "\n".join(lines)

        # inclusion: the week's movers, each UNDER its own project header
        for title, header in (("MOVEDTODAY", "Alpha"), ("CLOSEDWEEK", "Alpha"),
                              ("BOUNDARY7", "Alpha"), ("BETAMOVED", "Beta")):
            assert title in text, f"{title} is missing from the standup"
            hi = next(i for i, l in enumerate(lines) if f"▐ {header}" in l)
            ti = next(i for i, l in enumerate(lines) if title in l)
            assert hi < ti, f"{title} is not under the {header} header"

        # the marks: closed wears ✓, moved wears → with its current phase
        assert any(l.startswith("  ✓ CLOSEDWEEK") for l in lines), \
            "the closed task did not get its ✓"
        for moved, phase in (("MOVEDTODAY", "Review"), ("BOUNDARY7", "Doing"),
                             ("BETAMOVED", "Doing")):
            assert any(l.startswith(f"  → {moved}") and phase in l
                       for l in lines), f"{moved} did not get its → {phase}"

        # the per-project count line, RECOMPUTED from the fixture by the
        # stated rule (terminal phase = closed), never hand-listed
        for project in (alpha, beta):
            members = [t for t in tasks if t.project_id == project.id
                       and t.title in _standup_window_members(tasks, today)]
            closed = sum(1 for t in members if t.phase == board.phases[-1])
            assert f"{closed}/{len(members)} closed this week" in text, \
                f"{project.name}'s count line is wrong or missing"

        # the discriminating negatives: 8d OUT, 10d OUT, never-stamped OUT
        for title in ("OUTEIGHT", "OUTTEN", "NEVERMOVED"):
            assert title not in text, f"{title} leaked into the week"

        # completeness companion: the modal's task set IS the rule-derived
        # window set — a fixture task added later is covered by the rule,
        # and nothing hand-listed lets a leak slip by
        shown = {t.title for t in tasks if t.title in text}
        assert shown == _standup_window_members(tasks, today)

        # esc dismisses; the modal mutated NOTHING across open + close
        await pilot.press("escape")
        await pilot.pause()
        assert len(app.screen_stack) == 1, "escape did not dismiss the standup"
        assert Path(app.board.path).read_bytes() == blob, \
            "a read-only modal wrote to the board file"


async def test_standup_modal_empty_week_says_so_in_one_line(tmp_path):
    """AT-018 empty limb (HLR-011 boundary catalog): a board where nothing
    moved inside the window gets ONE honest line — no invented motion, no
    ghost project sections. RED counterfactuals: the empty message dropped
    → the message limb red; a None stamp read as 0 → the unstamped task
    appears and the message vanishes → both limbs red."""
    from datetime import timedelta
    today = date.today()
    old = Task("OLDSTAMP", None, "Doing",
               phase_changed=(today - timedelta(days=30)).isoformat())
    never = Task("NEVERSTAMPED", None, "Doing", phase_changed=None)
    board = _ops_board(tmp_path, old, never, name="empty.json")
    app = TaskboardApp(board_path=str(board.path))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.pause()
        await pilot.press(_key_for("standup"))
        await pilot.pause()
        lines = _modal_lines(app)
        text = "\n".join(lines)
        assert "Nothing moved this week." in text, \
            "the empty week does not say so"
        assert not any("▐" in l for l in lines), \
            "a ghost project section on an empty week"
        assert "OLDSTAMP" not in text and "NEVERSTAMPED" not in text


async def test_all_batch_keys_are_dead_on_the_aperture(tmp_path):
    """AT-019 (HLR-012): the FULL §3.0 key set — `[` `]` `!` `b` `s` `g` `z`
    `F` `+` `-` `=` `u` `S`, every physical key read off the seat (aliases
    included, never typed as literals) — is dead while the aperture is on
    top: the aperture stays the top screen, the mode/focus/undo state is
    untouched, and the board file is BYTE-EQUAL afterwards. The boundary
    limb: `escape` then pops the aperture itself (its own binding, not the
    kanban focus-exit). RED counterfactual: an action missing from
    BOARD_ACTIONS (delete one frozenset member) → its key reaches the
    hidden board — a mutation key changes the file (the byte-equality limb
    red), `S` pushes its modal over the aperture (the screen-identity limb
    red)."""
    from taskboard.aperture import ApertureScreen
    from taskboard.keymap import KEYMAP
    # the §3.0 actions — the physical keys are DERIVED from the seat below,
    # so a re-keyed binding is followed, never hard-coded (the `=` alias of
    # `+` rides along through the entry's own alias list)
    batch_actions = ("phase_move(-1)", "phase_move(1)", "prio_cycle",
                     "toggle_blocked", "kanban_sort", "kanban_group",
                     "collapse_toggle", "focus_cycle", "due_bump(1)",
                     "due_bump(-1)", "undo", "standup")
    keys = [phys for action in batch_actions
            for phys in next(k for k in KEYMAP if k.action == action)
            .keys.split(",")]
    assert len(keys) == 13, keys                  # the full §3.0 set, `=` too
    task = Task("Widget", None, "Doing", due_date="2026-01-01")
    board = _ops_board(tmp_path, task, name="ap13.json")
    app = TaskboardApp(board_path=str(board.path))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("4")
        await pilot.pause()
        await pilot.press("6")                      # the aperture
        await pilot.pause()
        assert isinstance(app.screen, ApertureScreen)
        blob = Path(app.board.path).read_bytes()
        for key in keys:
            await pilot.press(key)
            await pilot.pause()
            assert isinstance(app.screen, ApertureScreen), \
                f"{key!r} reached past the aperture (top: {app.screen!r})"
        assert Path(app.board.path).read_bytes() == blob, \
            "a key mutated the hidden board through the aperture"
        assert app.kanban_sort == "project" and app.kanban_group == "project"
        assert app.kanban_collapsed is False
        assert app.focused_project_id is None
        assert app._undo_stack == []
        assert app.board.task_by_id(task.id).due_date == "2026-01-01"
        # boundary: escape is the aperture's OWN binding — it pops it
        await pilot.press("escape")
        await pilot.pause()
        assert len(app.screen_stack) == 1, "escape did not pop the aperture"
        assert Path(app.board.path).read_bytes() == blob
