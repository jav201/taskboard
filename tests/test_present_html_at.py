"""Black-box acceptance tests for the presentation's HTML deck export.

AT-4501..AT-4506 from Inc X: every export is driven through `run_test` keys and
dialogs against synthetic boards saved under the suite's temporary home.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
from datetime import date
from pathlib import Path

import pytest

from taskboard import app as app_module, modals, models, views
from taskboard.__main__ import open_app
from taskboard.app import BoardsHome, PresentScreen
from taskboard.models import LINKS_MIGRATION, MILESTONES_MIGRATION, Board, Project, Task

TODAY = date(2026, 11, 1)
DAY = TODAY.isoformat()
PHASES = ["Backlog", "Doing", "Done"]
SETTINGS = {"migrations": {"links": LINKS_MIGRATION, "milestones": MILESTONES_MIGRATION},
            "seen_view_renumber_2026_07": True}


class _Today(date):
    @classmethod
    def today(cls):
        return TODAY


@pytest.fixture
def home(monkeypatch):
    for module in (app_module, models, views, modals):
        monkeypatch.setattr(module, "date", _Today)
    return Path.home() / ".taskboard"


def _project(pid: str, name: str) -> Project:
    return Project(id=pid, name=name, color="sky", start_date="2026-10-28",
                   due_date="2026-11-10")


def _task(tid: str, pid: str, title: str, phase: str = "Doing") -> Task:
    return Task(id=tid, project_id=pid, title=title, phase=phase,
                start_date="2026-10-30", due_date="2026-11-05", phase_changed=DAY)


def _board(path: Path, projects: list[Project], tasks: list[Task]) -> Board:
    return Board(projects, tasks, path, json.loads(json.dumps(SETTINGS)), PHASES)


def _app(home: Path, rows: list[tuple[str, str, str, Board]], last: str = "main"):
    entries = []
    for bid, name, colour, board in rows:
        board.save()
        entries.append({"id": bid, "name": name, "color": colour, "path": str(board.path),
                        "last_opened": "2026-11-01T09:00", "archived": False})
    (home / "boards.json").write_text(
        json.dumps({"version": 1, "last": last, "boards": entries}, indent=2), encoding="utf-8")
    return open_app(None)


def _one_board_app(home: Path):
    board = _board(home / "boards" / "main" / "board.json", [_project("pa", "Alpha")],
                   [_task("ta1", "pa", "Alpha open")])
    return _app(home, [("main", "Main", "sky", board)]), board


async def _press(pilot, *keys):
    for key in keys:
        await pilot.press(key)
        await pilot.pause()


async def _main(pilot, app):
    await pilot.pause()
    if isinstance(app.screen, BoardsHome):
        await _press(pilot, "escape")
    assert len(app.screen_stack) == 1


async def _present(pilot, app, *keys):
    await _main(pilot, app)
    await _press(pilot, "R", *keys)
    assert isinstance(app.screen, PresentScreen)


def _frame(app) -> str:
    return app.screen.query_one("#present-frame").content.plain


def _toasts(app, title: str) -> list:
    return [note for note in app._notifications if note.title == title]


def _assert_written_toast(app, path: Path):
    toast = _toasts(app, "Report")[-1]
    assert toast.message == f"Report written: {path.name}\n{path.parent}\no opens it (10 s)"
    assert toast.severity == "information"
    assert toast.timeout == 10


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _files(folder: Path) -> list[str]:
    return sorted(path.name for path in folder.iterdir()) if folder.exists() else []


async def test_AT_4501_views_1_and_2_write_only_the_presented_scope(home):
    """AT-4501: hide a task, then export views 1 and 2 to the same HTML file;
    hidden tasks, the other project and the other board stay out, with no SVG/PNG
    and no board-file write from either export."""
    main = _board(
        home / "boards" / "main" / "board.json",
        [_project("pa", "Alpha"), _project("pb", "OTHER-PROJECT-8P")],
        [_task("hidt7q", "pa", "HIDDEN-T-7Q"), _task("ta2", "pa", "Alpha shown"),
         _task("tb1", "pb", "Other project task")])
    other = _board(home / "boards" / "other" / "board.json",
                   [_project("po", "OTHER-BOARD-PROJECT")],
                   [_task("to1", "po", "Other board task")])
    app = _app(home, [("main", "MAIN-BOARD-6N", "sky", main),
                      ("other", "OTHER-BOARD-3M", "pink", other)])
    folder = main.path.parent / "reports"
    deck = folder / f"present-alpha-{DAY}.html"

    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await _present(pilot, app)
        assert "HIDDEN-T-7Q" in _frame(app)
        await _press(pilot, "space")
        assert "HIDDEN-T-7Q" not in _frame(app)
        board_hash = _sha256(main.path)

        await _press(pilot, "x")
        assert _files(folder) == [deck.name]
        assert _sha256(main.path) == board_hash
        _assert_written_toast(app, deck)
        page = deck.read_text(encoding="utf-8")
        for sentinel in ("HIDDEN-T-7Q", "OTHER-PROJECT-8P", "OTHER-BOARD-3M"):
            assert page.count(sentinel) == 0
        assert "Alpha shown" in page

        await _press(pilot, "2")
        os.utime(deck, (1, 1))
        await _press(pilot, "x")
        assert _files(folder) == [deck.name]
        assert deck.stat().st_mtime > 1
        assert _sha256(main.path) == board_hash
        _assert_written_toast(app, deck)


async def test_AT_4502_view_3_exports_order_scope_and_folded_tasks(home):
    """AT-4502: rank C first on the rail, hide B, fold A on the timeline, then
    export; overview and slides read C, A and folded A keeps every shown task."""
    board = _board(
        home / "boards" / "main" / "board.json",
        [_project("pa", "Alpha"), _project("pb", "Beta"), _project("pc", "Gamma")],
        [_task("ta1", "pa", "A-SHOWN-OPEN"), _task("ta2", "pa", "A-SHOWN-DONE", "Done"),
         _task("tb1", "pb", "UNDER-HIDDEN-B"), _task("tc1", "pc", "C-SHOWN-OPEN")])
    app = _app(home, [("main", "Main", "sky", board)])
    folder = board.path.parent / "reports"
    deck = folder / f"present-{DAY}.html"

    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await _present(pilot, app, "3")
        await _press(pilot, "down", "down", "K", "K")
        rail_order = _frame(app)
        assert rail_order.index("Gamma") < rail_order.index("Alpha") < rail_order.index("Beta")
        await _press(pilot, "down", "down", "space", "up", "right", "enter")
        assert "A-SHOWN-OPEN" not in _frame(app)
        await _press(pilot, "x")

        assert _files(folder) == [deck.name]
        _assert_written_toast(app, deck)
        page = deck.read_text(encoding="utf-8")
        assert page.count("Beta") == 0
        assert page.count("UNDER-HIDDEN-B") == 0
        overview = page.split(
            '<section class="slide"><h2>All projects — the overview</h2>', 1)[1].split(
                "</section>", 1)[0]
        assert overview.index(">Gamma</text>") < overview.index(">Alpha</text>")
        slides = re.findall(r'<section class="slide" data-project="[^"]+">(.*?)</section>',
                            page, re.S)
        names = [re.search(r'<span class="pname">(.*?)</span>', slide).group(1)
                 for slide in slides]
        assert names == ["Gamma", "Alpha"]
        assert "A-SHOWN-OPEN" in slides[1]
        assert "A-SHOWN-DONE" in slides[1]
        assert '<p class="foot">2 tasks</p>' in slides[1]


async def test_AT_4503_the_open_offer_is_single_use_and_expires(home, monkeypatch):
    """AT-4503: `o` opens the just-written deck once; a second press does nothing,
    and a new offer made ten seconds earlier is already expired."""
    app, board = _one_board_app(home)
    now = [100.0]
    opened, urls = [], []
    monkeypatch.setattr(app, "_report_clock", lambda: now[0])
    monkeypatch.setattr(os, "startfile", lambda path: opened.append(Path(path)), raising=False)
    monkeypatch.setattr(app_module.webbrowser, "open", lambda url: urls.append(url) or True)
    deck = board.path.parent / "reports" / f"present-alpha-{DAY}.html"

    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await _present(pilot, app, "x")
        assert deck.is_file()
        _assert_written_toast(app, deck)
        await _press(pilot, "o")
        assert (opened, urls) in [([deck], []), ([], [deck.as_uri()])]
        await _press(pilot, "o")
        assert (opened, urls) in [([deck], []), ([], [deck.as_uri()])]

        await _press(pilot, "x")
        now[0] += 10
        await _press(pilot, "o")
        assert (opened, urls) in [([deck], []), ([], [deck.as_uri()])]


async def test_AT_4504_an_oserror_toasts_offers_nothing_and_leaves_r_usable(home, monkeypatch):
    """AT-4504: with `reports` an existing plain file, export reports the OSError,
    offers no open action, and the presentation still answers escape."""
    app, board = _one_board_app(home)
    opened, urls = [], []
    monkeypatch.setattr(os, "startfile", lambda path: opened.append(Path(path)), raising=False)
    monkeypatch.setattr(app_module.webbrowser, "open", lambda url: urls.append(url) or True)
    (board.path.parent / "reports").write_text("not a folder", encoding="utf-8")

    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await _present(pilot, app, "x")
        toasts = _toasts(app, "Report")
        assert toasts, "a failed export must leave a Report toast"
        toast = toasts[-1]
        assert toast.message.startswith("Report not (fully) written: ")
        assert toast.message != "Report not (fully) written: "
        assert toast.severity == "error"
        await _press(pilot, "o")
        assert opened == [] and urls == []
        await _press(pilot, "escape")
        assert not isinstance(app.screen, PresentScreen)


async def test_AT_4505_narrow_export_warns_and_creates_no_folder(home):
    """AT-4505: at 30 columns the export warns about the 36-column minimum and
    leaves `reports/` absent."""
    app, board = _one_board_app(home)
    async with app.run_test(size=(30, 20), notifications=True) as pilot:
        await _present(pilot, app, "x")
        toast = _toasts(app, "Present")[-1]
        assert toast.message == "Widen the terminal to 36+ columns to export"
        assert toast.severity == "warning"
        assert not (board.path.parent / "reports").exists()


async def test_AT_4506_h_is_discoverable_and_presentation_help_says_html(home):
    """AT-4506: at 118x30 and 80x24 the main bar shows H, help lists H Report once,
    H opens the unchanged report modal, and R's help names the HTML deck and o."""
    app, _board_value = _one_board_app(home)
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await _main(pilot, app)
        for size in ((118, 30), (80, 24)):
            await pilot.resize_terminal(*size)
            await pilot.pause()
            bar = app.query_one("#keybar").render().plain
            assert re.search(r"(?:^|\s)H(?:\s|$)", bar), bar

            await _press(pilot, "question_mark")
            assert isinstance(app.screen, modals.HelpModal)
            help_text = (app.screen.query_one("#help-keys").content.plain + "\n"
                         + app.screen.query_one("#help-global").content.plain)
            assert len(re.findall(r"(?<!\w)H\s+Report(?!\w)", help_text)) == 1
            await _press(pilot, "escape", "H")
            assert isinstance(app.screen, modals.ReportExport)
            await _press(pilot, "escape")

        await _press(pilot, "R", "question_mark")
        assert isinstance(app.screen, modals.PresentKeys)
        text = app.screen.query_one("#pk-text").content.plain
        assert re.search(r"(?:^|\s)x\s+export this view · HTML deck", text)
        assert re.search(r"(?:^|\s)o\s+open the last export \(10 s\)", text)
        assert "SVG" not in text and "PNG" not in text
