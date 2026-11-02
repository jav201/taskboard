"""Inc X: the presentation exports its scoped HTML deck (LLR-4501..4506).

Every export is driven through the shipped ``run_test`` pilot and real keys.
The byte oracle for TC-4703/4704 is deliberately a second, independently built
fixture whose tasks start with no URLs; it is never an implementation proxy.
"""
from __future__ import annotations

import hashlib
import html
import json
import os
import re
import subprocess
from datetime import date
from pathlib import Path

import pytest
from textual.content import Content

from taskboard import app as app_module, keymap, models, modals, views
from taskboard.app import PresentScreen, TaskboardApp
from taskboard.boards import BoardEntry, Registry
from taskboard.marks import Mark
from taskboard.models import Board, Project, Task
from taskboard.people import Person

ROOT = Path(__file__).resolve().parents[1]
TODAY = date(2026, 11, 1)
DAY = TODAY.isoformat()
TASK_URL = "https://example.test/capability-a1"
MAIN_VIEWS = ("swimlanes", "agenda", "gantt", "kanban", "focus",
              "chainmap", "flow", "standup", "people", "setup")


class _Today(date):
    @classmethod
    def today(cls):
        return TODAY


@pytest.fixture(autouse=True)
def _frozen_day(monkeypatch):
    for module in (app_module, models, views, modals):
        monkeypatch.setattr(module, "date", _Today)


def _task(tid: str, title: str, project_id: str | None = "pA",
          phase: str = "Doing", **kw) -> Task:
    return Task(id=tid, title=title, project_id=project_id, phase=phase,
                start_date=kw.pop("start_date", "2026-10-28"),
                due_date=kw.pop("due_date", "2026-11-05"),
                phase_changed=kw.pop("phase_changed", "2026-10-28"), **kw)


def _default_board(path: Path, *, with_urls: bool = True) -> Board:
    projects = [Project("Alpha", "sky", id="pA", present_rank=0),
                Project("Beta", "lime", id="pB", present_rank=1)]
    tasks = [
        _task("a1", "a-open-1", notes="ask @user.one",
              urls=[TASK_URL] if with_urls else []),
        _task("a2", "a-done", phase="Done", notes="DONE-NOTE-ALPHA"),
        _task("a3", "a-gate", milestone=True, mark="gate", depends_on=["a1"]),
        _task("b1", "b-open", project_id="pB", notes="B-OPEN-NOTE"),
    ]
    return Board(projects, tasks, path, {}, ["Backlog", "Doing", "Done"])


def _save(board: Board) -> Board:
    board.path.parent.mkdir(parents=True, exist_ok=True)
    board.save()
    return board


def _app(board: Board, *, entries: list[BoardEntry] | None = None,
         selected: str | None = "a1") -> TaskboardApp:
    _save(board)
    if entries is None:
        entries = [BoardEntry("main", "Main", "sky", str(board.path))]
    registry = Registry(board.path.parent / "boards.json", entries,
                        entries[0].id if entries else None)
    app = TaskboardApp(board_path=str(board.path), registry=registry,
                       team_sync_interval=1e9)
    app.selected_task_id = selected
    app.people.people["user.one"] = Person(id="user.one", name="Synthetic Person",
                                           role="Fixture")
    app.marks.marks["gate"] = Mark(id="gate", name="Gate", shape="▲", colour="cyan")
    return app


async def _press(pilot, *keys: str) -> None:
    for key in keys:
        await pilot.press(key)
        await pilot.pause()


async def _main(pilot) -> None:
    await pilot.pause()
    if type(pilot.app.screen).__name__ == "BoardsHome":
        await _press(pilot, "escape")
    assert len(pilot.app.screen_stack) == 1


async def _present(pilot, view: int = 1) -> None:
    await _main(pilot)
    await _press(pilot, "R")
    assert isinstance(pilot.app.screen, PresentScreen)
    if view != 1:
        await _press(pilot, str(view))


def _present_path(board: Board, name: str = f"present-alpha-{DAY}.html") -> Path:
    return board.path.parent / "reports" / name


def _deck_bytes(path: Path) -> bytes:
    assert path.exists(), f"x must write the HTML deck {path.name}, not SVG/PNG"
    return path.read_bytes()


def _page(path: Path) -> str:
    return _deck_bytes(path).decode("utf-8")


def _slide_names(page: str) -> list[str]:
    sections = re.findall(r'<section class="slide" data-project=.*?</section>', page, re.S)
    return [html.unescape(re.search(r'<span class="pname">(.*?)</span>', s, re.S).group(1))
            for s in sections]


def _toasts(app: TaskboardApp, title: str = "Report") -> list:
    return [n for n in app._notifications if n.title == title]


def _hashes(folder: Path) -> dict[Path, str]:
    return {p: hashlib.sha256(p.read_bytes()).hexdigest()
            for p in folder.rglob("*") if p.is_file()}


async def _h_deck(root: Path, scope: str) -> bytes:
    board = _default_board(root / "reference" / "board.json", with_urls=False)
    assert all(not t.urls for t in board.tasks)
    app = _app(board)
    async with app.run_test(size=(118, 31)) as pilot:
        await _main(pilot)
        await _press(pilot, "H", *(("p",) if scope == "project" else ()), "c")
    name = (f"deck-main-alpha-{DAY}.html" if scope == "project"
            else f"deck-{DAY}.html")
    return (board.path.parent / "reports" / name).read_bytes()


# ---------------------------------------------------------------------------
# LLR-4501: writing the deck
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("view", [1, 2])
async def test_TC_4701_LLR_4501_1_project_views_write_exact_html_name(tmp_path, view):
    board = _default_board(tmp_path / "board.json")
    app = _app(board)
    async with app.run_test(size=(118, 31)) as pilot:
        await _present(pilot, view)
        await _press(pilot, "x")
    path = _present_path(board)
    assert _deck_bytes(path)
    assert sorted(p.name for p in path.parent.iterdir()) == [path.name]


@pytest.mark.parametrize("project_name, expected", [
    (r"..\..\evil", f"present-evil-{DAY}.html"),
    ("CON", f"present-con-{DAY}.html"),
    ("!!!", f"present-project-{DAY}.html"),
])
async def test_TC_4701b_LLR_4501_1_names_cannot_escape_reports(tmp_path, project_name, expected):
    projects = [Project(project_name, "sky", id="pA")]
    board = Board(projects, [_task("a1", "safe")], tmp_path / "board.json")
    app = _app(board)
    async with app.run_test(size=(118, 31)) as pilot:
        await _present(pilot)
        await _press(pilot, "x")
    path = _present_path(board, expected)
    assert _deck_bytes(path)
    assert path.resolve().parent == (board.path.parent / "reports").resolve()
    assert not (tmp_path / f"present-evil-{DAY}.html").exists()


async def test_TC_4702_LLR_4501_2_all_view_writes_exact_html_name(tmp_path):
    board = _default_board(tmp_path / "board.json")
    app = _app(board)
    async with app.run_test(size=(118, 31)) as pilot:
        await _present(pilot, 3)
        await _press(pilot, "x")
    assert _deck_bytes(_present_path(board, f"present-{DAY}.html"))


@pytest.mark.parametrize("view", [1, 2])
async def test_TC_4703_LLR_4501_3_bytes_equal_independent_url_free_H_fixture(tmp_path, view):
    reference = await _h_deck(tmp_path, "project")
    board = _default_board(tmp_path / "presented" / "board.json", with_urls=True)
    app = _app(board)
    async with app.run_test(size=(118, 31)) as pilot:
        await _present(pilot, view)
        await _press(pilot, "x")
    # A-R2-2: H ran on a separate fixture already holding urls=[]; x ran here
    # on original URLs. No proxy or extracted dict is compared with itself.
    assert _deck_bytes(_present_path(board)) == reference


async def test_TC_4704_LLR_4501_4_all_bytes_equal_independent_url_free_H_fixture(tmp_path):
    reference = await _h_deck(tmp_path, "all")
    board = _default_board(tmp_path / "presented" / "board.json", with_urls=True)
    app = _app(board)
    async with app.run_test(size=(118, 31)) as pilot:
        await _present(pilot, 3)
        await _press(pilot, "x")
    assert _deck_bytes(_present_path(board, f"present-{DAY}.html")) == reference


@pytest.mark.parametrize("shown", [True, False])
async def test_TC_4705_LLR_4501_5_project_scope_ignores_own_rail_flag(tmp_path, shown):
    projects = [Project("Alpha", "sky", id="pA", show_in_present=shown),
                Project("Beta", "lime", id="pB"), Project("Gamma", "pink", id="pC")]
    tasks = [_task("a1", "alpha-task"), _task("b1", "beta-task", "pB"),
             _task("c1", "gamma-task", "pC")]
    board = Board(projects, tasks, tmp_path / "board.json")
    app = _app(board)
    async with app.run_test(size=(118, 31)) as pilot:
        await _present(pilot)
        await _press(pilot, "x")
    page = _page(_present_path(board))
    assert _slide_names(page) == ["Alpha"]
    assert "Beta" not in page and "Gamma" not in page


async def test_TC_4706_LLR_4501_6_all_scope_uses_presentation_order(tmp_path):
    projects = [Project("Alpha", "sky", id="pA", present_rank=1),
                Project("Beta", "lime", id="pB", present_rank=2),
                Project("Gamma", "pink", id="pC", present_rank=0)]
    board = Board(projects, [_task("a1", "alpha-task"),
                             _task("b1", "beta-task", "pB"),
                             _task("c1", "gamma-task", "pC")], tmp_path / "board.json")
    app = _app(board)
    async with app.run_test(size=(118, 31)) as pilot:
        await _present(pilot, 3)
        await _press(pilot, "x")
    page = _page(_present_path(board, f"present-{DAY}.html"))
    assert _slide_names(page) == ["Gamma", "Alpha", "Beta"]
    overview = page.split('<h2>All projects — the overview</h2>', 1)[1].split(
        '<section class="slide" data-project=', 1)[0]
    positions = [overview.index(f">{name}</text>") for name in ("Gamma", "Alpha", "Beta")]
    assert positions == sorted(positions)


@pytest.mark.parametrize("view", [1, 3])
async def test_TC_4707_LLR_4501_7_only_presented_board_reaches_deck(tmp_path, view):
    board = _default_board(tmp_path / "main" / "board.json")
    other = Board([Project("Other Project", "pink", id="pO")],
                  [_task("o1", "other-task", "pO")], tmp_path / "other" / "board.json")
    _save(other)
    entries = [BoardEntry("main", "Main", "sky", str(board.path)),
               BoardEntry("other", "Other Board", "pink", str(other.path))]
    app = _app(board, entries=entries)
    async with app.run_test(size=(118, 31)) as pilot:
        await _present(pilot, view)
        await _press(pilot, "x")
    name = f"present-alpha-{DAY}.html" if view == 1 else f"present-{DAY}.html"
    page = _page(_present_path(board, name))
    assert re.findall(r"<tr><td>(.*?)</td>", page) == ["Main"]
    assert "Other Board" not in page and "Other Project" not in page


async def test_TC_4708_LLR_4501_8_folded_project_keeps_tasks_and_notes(tmp_path):
    projects = [Project("Alpha", "sky", id="pA", present_rank=0),
                Project("Beta", "lime", id="pB", present_rank=1)]
    tasks = [_task("a1", "alpha-open"),
             _task("b1", "beta-open", "pB", notes="B-OPEN-NOTE"),
             _task("b2", "beta-done", "pB", phase="Done", notes="B-DONE-NOTE")]
    board = Board(projects, tasks, tmp_path / "board.json")
    app = _app(board)
    async with app.run_test(size=(118, 31)) as pilot:
        await _present(pilot, 3)
        await _press(pilot, "down", "enter")       # fold Beta on the rail
        assert app.screen._folded == {"pB"}
        await _press(pilot, "x")
    page = _page(_present_path(board, f"present-{DAY}.html"))
    beta = next(s for s in re.findall(r'<section class="slide" data-project=.*?</section>',
                                      page, re.S) if "Beta" in s)
    assert all(token in beta for token in
               ("beta-open", "beta-done", "B-OPEN-NOTE", "B-DONE-NOTE", "2 tasks"))


@pytest.mark.parametrize("view", [1, 3])
async def test_TC_4709_LLR_4501_9_done_task_title_and_notes_reach_file(tmp_path, view):
    board = _default_board(tmp_path / "board.json")
    app = _app(board)
    async with app.run_test(size=(118, 31)) as pilot:
        await _present(pilot, view)
        await _press(pilot, "x")
    name = f"present-alpha-{DAY}.html" if view == 1 else f"present-{DAY}.html"
    page = _page(_present_path(board, name))
    alpha = next(s for s in re.findall(r'<section class="slide" data-project=.*?</section>',
                                       page, re.S) if "Alpha" in s)
    assert "3 tasks" in alpha and "a-done" in alpha and "DONE-NOTE-ALPHA" in alpha


@pytest.mark.parametrize("view", [1, 2, 3])
async def test_TC_4710_LLR_4501_10_export_changes_neither_board_nor_history(
        tmp_path, monkeypatch, view):
    board = _default_board(tmp_path / "board.json")
    history = board.path.parent / "history.jsonl"
    _save(board)
    history.write_bytes(b'{"event":"synthetic"}\n')
    app = _app(board)
    async with app.run_test(size=(118, 31)) as pilot:
        await _present(pilot, view)
        before = {p: hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in (board.path, history)}
        # A byte-identical re-save keeps the hashes equal, so the write path
        # itself is watched: the export reaches no save at all (M10).
        saves: list[str] = []
        for name in ("save", "save_atomic"):
            def spy(self, *args, _real=getattr(Board, name), _name=name, **kwargs):
                saves.append(_name)
                return _real(self, *args, **kwargs)
            monkeypatch.setattr(Board, name, spy)
        await _press(pilot, "x")
        saved_by_export = list(saves)
        after = {p: hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in (board.path, history)}
    assert after == before
    assert saved_by_export == []
    name = f"present-{DAY}.html" if view == 3 else f"present-alpha-{DAY}.html"
    assert _deck_bytes(_present_path(board, name))


@pytest.mark.parametrize("label, expected", [(("Client A", "pink"), "Client A"),
                                             (None, "this board")])
async def test_TC_4711_LLR_4501_11_unlisted_board_uses_label_or_fallback(tmp_path, label, expected):
    board = _default_board(tmp_path / "board.json")
    app = _app(board, entries=[])
    async with app.run_test(size=(118, 31)) as pilot:
        await _main(pilot)
        app.board.label = label
        await _press(pilot, "R", "x")
    page = _page(_present_path(board))
    assert f"<tr><td>{expected}</td>" in page


async def test_TC_4712_LLR_4501_12_empty_all_scope_still_writes_deck(tmp_path):
    board = _default_board(tmp_path / "board.json")
    for project in board.projects:
        project.show_in_present = False
    app = _app(board)
    async with app.run_test(size=(118, 31)) as pilot:
        await _present(pilot, 3)
        await _press(pilot, "x")
    assert "No project in this scope holds a task." in _page(
        _present_path(board, f"present-{DAY}.html"))


async def test_TC_4713_LLR_4501_13_narrow_warning_is_unchanged(tmp_path):
    board = _default_board(tmp_path / "board.json")
    app = _app(board)
    async with app.run_test(size=(30, 20)) as pilot:
        await _present(pilot)
        await _press(pilot, "x")
    toast = _toasts(app, "Present")[-1]
    assert toast.message == "Widen the terminal to 36+ columns to export"
    assert toast.severity == "warning" and toast.timeout == 6


async def test_TC_4714_LLR_4501_14_narrow_export_writes_nothing(tmp_path):
    board = _default_board(tmp_path / "board.json")
    app = _app(board)
    async with app.run_test(size=(30, 20)) as pilot:
        await _present(pilot)
        await _press(pilot, "x")
    assert not (board.path.parent / "reports").exists()


@pytest.mark.parametrize("none_visible", [False, True])
async def test_TC_4715_LLR_4501_15_missing_project_falls_back_to_first_visible(
        tmp_path, none_visible):
    board = _default_board(tmp_path / "board.json")
    app = _app(board)
    async with app.run_test(size=(118, 31)) as pilot:
        await _present(pilot)
        app.screen._project_id = "missing"
        if none_visible:
            # Nothing visible to fall back to: the deck holds no project,
            # never a `None` slot (M15).
            for project in app.board.projects:
                project.archived = True
        await _press(pilot, "x")
    if none_visible:
        page = _page(_present_path(board, f"present-{DAY}.html"))
        assert "No project in this scope holds a task." in page
        assert _slide_names(page) == []
    else:
        page = _page(_present_path(board))
        assert _slide_names(page) == ["Alpha"] and "Beta" not in page


# ---------------------------------------------------------------------------
# LLR-4502: hidden data and URLs stay out of the bytes
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("view", [1, 2, 3])
async def test_TC_4721_LLR_4502_1_hidden_task_and_id_have_zero_occurrences(tmp_path, view):
    board = _default_board(tmp_path / "board.json")
    board.tasks.append(_task("hidt7q", "HIDDEN-T-7Q", show_in_present=False))
    app = _app(board)
    async with app.run_test(size=(118, 31)) as pilot:
        await _present(pilot, view)
        await _press(pilot, "x")
    name = f"present-{DAY}.html" if view == 3 else f"present-alpha-{DAY}.html"
    page = _page(_present_path(board, name))
    assert "HIDDEN-T-7Q" not in page and "hidt7q" not in page


async def test_TC_4722_LLR_4502_2_hidden_project_and_its_tasks_have_zero_occurrences(tmp_path):
    board = _default_board(tmp_path / "board.json")
    board.projects.append(Project("HIDDEN-P-4K", "pink", id="pH", show_in_present=False))
    board.tasks.append(_task("ph1", "UNDER-HIDDEN-P", "pH"))
    app = _app(board)
    async with app.run_test(size=(118, 31)) as pilot:
        await _present(pilot, 3)
        await _press(pilot, "x")
    page = _page(_present_path(board, f"present-{DAY}.html"))
    assert "HIDDEN-P-4K" not in page and "UNDER-HIDDEN-P" not in page


@pytest.mark.parametrize("view", [1, 3])
async def test_TC_4723_LLR_4502_3_archived_and_projectless_tasks_are_excluded(tmp_path, view):
    board = _default_board(tmp_path / "board.json")
    board.projects.append(Project("Archived Project", "pink", id="pR", archived=True))
    board.tasks.extend([_task("ar1", "ARCH-T", archived=True),
                        _task("ar2", "ARCH-P-TASK", "pR"),
                        _task("np1", "NO-PROJ-T", None)])
    app = _app(board)
    async with app.run_test(size=(118, 31)) as pilot:
        await _present(pilot, view)
        await _press(pilot, "x")
    name = f"present-{DAY}.html" if view == 3 else f"present-alpha-{DAY}.html"
    page = _page(_present_path(board, name))
    assert all(s not in page for s in ("ARCH-T", "ARCH-P-TASK", "NO-PROJ-T", "Inbox"))


@pytest.mark.parametrize("view", [1, 3])
async def test_TC_4724_LLR_4502_4_hidden_milestone_class_is_excluded(tmp_path, view):
    board = _default_board(tmp_path / "board.json")
    board.tasks.append(_task("hm1", "HID-CLASS-MS", milestone=True, mark="secret"))
    app = _app(board)
    app.marks.marks["secret"] = Mark("secret", "Secret Class", "■", "pink", hidden=True)
    async with app.run_test(size=(118, 31)) as pilot:
        await _present(pilot, view)
        await _press(pilot, "x")
    name = f"present-{DAY}.html" if view == 3 else f"present-alpha-{DAY}.html"
    assert "HID-CLASS-MS" not in _page(_present_path(board, name))


async def test_TC_4725_LLR_4502_5_legend_omits_class_used_only_by_hidden_task(tmp_path):
    board = _default_board(tmp_path / "board.json")
    board.tasks.append(_task("hc1", "hidden-class-user", milestone=True, mark="secret",
                             show_in_present=False))
    app = _app(board)
    app.marks.marks["secret"] = Mark("secret", "CLASS-ONLY-HIDDEN", "■", "pink")
    async with app.run_test(size=(118, 31)) as pilot:
        await _present(pilot)
        await _press(pilot, "x")
    assert "CLASS-ONLY-HIDDEN" not in _page(_present_path(board))


async def test_TC_4726_LLR_4502_6_export_reads_hide_flags_at_each_press(tmp_path):
    board = _default_board(tmp_path / "board.json")
    app = _app(board)
    path = _present_path(board)
    async with app.run_test(size=(118, 31)) as pilot:
        await _present(pilot)
        await _press(pilot, "space", "x")
        assert "a-open-1" not in _page(path)
        await _press(pilot, "a", "x")
        assert "a-open-1" in _page(path)


@pytest.mark.parametrize("view", [1, 2, 3])
async def test_TC_4727_LLR_4502_7_urls_strip_without_mutating_source_or_next_save(tmp_path, view):
    board = _default_board(tmp_path / "board.json", with_urls=True)
    original = {t.id: list(t.urls) for t in board.tasks}
    app = _app(board)
    async with app.run_test(size=(118, 31)) as pilot:
        await _present(pilot, view)
        await _press(pilot, "x")
    name = f"present-{DAY}.html" if view == 3 else f"present-alpha-{DAY}.html"
    assert TASK_URL not in _page(_present_path(board, name))
    # S-R2-2 negative control: rebinding copies, never clearing source lists.
    assert {t.id: t.urls for t in app.board.tasks} == original
    app.board.save()
    saved = json.loads(board.path.read_text(encoding="utf-8"))
    saved_urls = {t["id"]: t.get("urls", []) for t in saved["tasks"]}
    assert saved_urls == original and saved_urls["a1"] == [TASK_URL]


# ---------------------------------------------------------------------------
# LLR-4503: toast and shared, single-use offer
# ---------------------------------------------------------------------------
async def test_TC_4731_LLR_4503_1_success_toast_is_exact(tmp_path):
    board = _default_board(tmp_path / "board.json")
    app = _app(board)
    async with app.run_test(size=(118, 31), notifications=True) as pilot:
        await _present(pilot)
        await _press(pilot, "x")
    path = _present_path(board)
    assert _deck_bytes(path)
    toast = _toasts(app)[-1]
    assert toast.message == (f"Report written: {path.name}\n{path.parent}\n"
                             "o opens it (10 s)")
    assert toast.severity == "information" and toast.timeout == 10


async def test_TC_4732_LLR_4503_2_o_opens_offered_deck_once(tmp_path, monkeypatch):
    opened = []
    monkeypatch.setattr(os, "startfile", lambda p: opened.append(Path(p)), raising=False)
    board = _default_board(tmp_path / "board.json")
    app = _app(board)
    async with app.run_test(size=(118, 31)) as pilot:
        await _present(pilot)
        await _press(pilot, "x", "o")
    assert opened == [_present_path(board)]


async def test_TC_4733_LLR_4503_3_absent_expired_and_consumed_offers_open_nothing(
        tmp_path, monkeypatch):
    now = [100.0]
    opened = []
    monkeypatch.setattr(os, "startfile", lambda p: opened.append(Path(p)), raising=False)
    board = _default_board(tmp_path / "board.json")
    app = _app(board)
    monkeypatch.setattr(app, "_report_clock", lambda: now[0])
    async with app.run_test(size=(118, 31)) as pilot:
        await _present(pilot)
        await _press(pilot, "o")
        assert opened == []
        await _press(pilot, "x")
        now[0] = 110.0
        await _press(pilot, "o")
        assert opened == []
        now[0] = 200.0
        await _press(pilot, "x", "o", "o")
        assert opened == [_present_path(board)]


async def test_TC_4733b_LLR_4503_3_shared_offer_survives_esc_for_one_main_o(
        tmp_path, monkeypatch):
    opened, urls = [], []
    monkeypatch.setattr(os, "startfile", lambda p: opened.append(Path(p)), raising=False)
    monkeypatch.setattr(app_module.webbrowser, "open", lambda u: urls.append(u) or True)
    board = _default_board(tmp_path / "board.json")
    app = _app(board)
    async with app.run_test(size=(118, 31)) as pilot:
        await _present(pilot)
        await _press(pilot, "x", "escape", "o")
    assert opened == [_present_path(board)] and urls == []


async def test_TC_4734_LLR_4503_4_write_oserror_toasts_without_crashing(tmp_path):
    board = _default_board(tmp_path / "board.json")
    _save(board)
    folder = board.path.parent / "reports"
    folder.write_text("plain file", encoding="utf-8")
    with pytest.raises(OSError) as exc:
        folder.mkdir(parents=True, exist_ok=True)
    expected = f"Report not (fully) written: {exc.value}"
    app = _app(board)
    async with app.run_test(size=(118, 31), notifications=True) as pilot:
        await _present(pilot)
        await _press(pilot, "x", "escape")
    toast = _toasts(app)[-1]
    assert toast.message == expected and toast.severity == "error" and toast.timeout == 10


async def test_TC_4735_LLR_4503_5_failed_export_withdraws_earlier_offer(tmp_path, monkeypatch):
    opened = []
    monkeypatch.setattr(os, "startfile", lambda p: opened.append(Path(p)), raising=False)
    board = _default_board(tmp_path / "board.json")
    app = _app(board)
    async with app.run_test(size=(118, 31), notifications=True) as pilot:
        await _present(pilot)
        await _press(pilot, "x")
        path = _present_path(board)
        assert _deck_bytes(path)
        path.unlink()
        path.parent.rmdir()
        path.parent.write_text("plain file", encoding="utf-8")
        await _press(pilot, "x", "o")
    assert opened == [] and app._report_offer is None


async def test_TC_4736_LLR_4503_6_opener_oserror_has_exact_error_toast(tmp_path, monkeypatch):
    board = _default_board(tmp_path / "board.json")
    app = _app(board)
    def refuse(_path):
        raise OSError("no handler")
    monkeypatch.setattr(os, "startfile", refuse, raising=False)
    async with app.run_test(size=(118, 31), notifications=True) as pilot:
        await _present(pilot)
        await _press(pilot, "x", "o")
    toasts = _toasts(app)
    assert toasts, "o must route the opener failure to a Report toast"
    assert toasts[-1].message == f"Could not open the report present-alpha-{DAY}.html."


async def test_TC_4736b_LLR_4503_6_relative_uri_valueerror_is_caught(tmp_path, monkeypatch):
    board = _default_board(tmp_path / "board.json")
    app = _app(board)
    monkeypatch.delattr(os, "startfile", raising=False)
    async with app.run_test(size=(118, 31), notifications=True) as pilot:
        await _present(pilot)
        await _press(pilot, "x")
        path = _present_path(board)
        assert _deck_bytes(path)
        app._report_offer = (Path(path.name), app._report_clock() + 10)
        await _press(pilot, "o")
    assert _toasts(app)[-1].message == f"Could not open the report {path.name}."


async def test_TC_4737_LLR_4503_7_markup_in_folder_is_literal_toast_text(tmp_path):
    # `[red]rx[/red]` (the LLR's literal) holds a `/`, which splits the folder on
    # every OS; `[red]rx[red]` carries the same markup in ONE path segment.
    folder = "[red]rx[red]"
    board = _default_board(tmp_path / folder / "board.json")
    app = _app(board)
    async with app.run_test(size=(118, 31), notifications=True) as pilot:
        await _present(pilot)
        await _press(pilot, "x")
    toasts = _toasts(app)
    assert toasts, "x must use the shared Report toast"
    n = toasts[-1]
    # The toast's plain text, by the rule Textual's Toast.render applies.
    plain = (Content.from_markup(n.message) if n.markup else Content(n.message)).plain
    assert folder in plain


# ---------------------------------------------------------------------------
# LLR-4504: exactly one HTML file and no rasterisation code/process
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("view", [1, 2, 3])
async def test_TC_4741_LLR_4504_1_one_file_oracle(tmp_path, view):
    board = _default_board(tmp_path / "board.json")
    app = _app(board)
    async with app.run_test(size=(118, 31)) as pilot:
        await _present(pilot, view)
        before = _hashes(board.path.parent)
        await _press(pilot, "x")
        after = _hashes(board.path.parent)
    name = f"present-{DAY}.html" if view == 3 else f"present-alpha-{DAY}.html"
    path = _present_path(board, name)
    changed = {p for p in before.keys() | after.keys() if before.get(p) != after.get(p)}
    assert changed == {path}
    assert path.suffix == ".html" and _deck_bytes(path)
    assert not list(path.parent.glob("*.svg")) and not list(path.parent.glob("*.png"))


@pytest.mark.parametrize("view", [1, 2, 3])
async def test_TC_4742_LLR_4504_2_export_starts_no_subprocess(tmp_path, monkeypatch, view):
    calls = []
    def forbidden(*args, **kwargs):
        calls.append((args, kwargs))
        raise AssertionError("presentation export started a subprocess")
    monkeypatch.setattr(subprocess, "run", forbidden)
    monkeypatch.setattr(subprocess, "Popen", forbidden)
    # Guard: a returning Edge arm would find an Edge here and start it.
    monkeypatch.setattr(views, "_find_msedge", lambda: "synthetic-edge", raising=False)
    board = _default_board(tmp_path / "board.json")
    app = _app(board)
    async with app.run_test(size=(118, 31)) as pilot:
        await _present(pilot, view)
        await _press(pilot, "x")
    name = f"present-{DAY}.html" if view == 3 else f"present-alpha-{DAY}.html"
    assert _deck_bytes(_present_path(board, name)) and calls == []


def test_TC_4743_LLR_4504_3_package_has_no_svg_or_rasteriser_route():
    pattern = re.compile(r"save_svg|msedge|--screenshot|present_paths|present_all_export")
    hits = [(p.name, n, line) for p in (ROOT / "taskboard").glob("*.py")
            for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1)
            if pattern.search(line)]
    assert hits == []


# ---------------------------------------------------------------------------
# LLR-4505: H in every primary bar and exactly once in help
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("view", MAIN_VIEWS)
@pytest.mark.parametrize("width", [80, 118])
def test_TC_4751_LLR_4505_1_H_is_in_all_20_primary_bars(view, width):
    entries, _dropped = keymap.fit_bar(width, view, "primary")
    assert "H" in {show for show, _label in entries}


@pytest.mark.parametrize("view", MAIN_VIEWS)
@pytest.mark.parametrize("width", [80, 118])
def test_TC_4752_LLR_4505_2_base_keys_and_overflow_are_preserved(
        view, width, monkeypatch):
    entries, dropped = keymap.fit_bar(width, view, "primary")
    assert "H" in {show for show, _label in entries}
    base_seat = tuple(k._replace(bar=False, primary=False) if k.show == "H" else k
                      for k in keymap.KEYMAP)
    with monkeypatch.context() as ctx:
        ctx.setattr(keymap, "KEYMAP", base_seat)
        base_entries, base_dropped = keymap.fit_bar(width, view, "primary")
    assert {s for s, _ in base_entries} <= {s for s, _ in entries}
    assert dropped == base_dropped == 0


@pytest.mark.parametrize("view", MAIN_VIEWS)
@pytest.mark.parametrize("width", [80, 118])
def test_TC_4753_LLR_4505_3_at_most_one_base_word_is_lost(view, width, monkeypatch):
    entries, _dropped = keymap.fit_bar(width, view, "primary")
    assert "H" in {show for show, _label in entries}
    base_seat = tuple(k._replace(bar=False, primary=False) if k.show == "H" else k
                      for k in keymap.KEYMAP)
    with monkeypatch.context() as ctx:
        ctx.setattr(keymap, "KEYMAP", base_seat)
        base_entries, _ = keymap.fit_bar(width, view, "primary")
    base_words = {s for s, label in base_entries if label}
    new_words = {s for s, label in entries if label}
    assert len(base_words - new_words) <= 1


def test_TC_4754_LLR_4505_4_wide_primary_bar_names_H_Report():
    assert "H Report" in keymap.key_bar_plain(250, "swimlanes", "primary")


@pytest.mark.parametrize("view", MAIN_VIEWS)
def test_TC_4755_LLR_4505_5_help_lists_H_Report_exactly_once(view):
    help_modal = modals.HelpModal(view, Board([], [], Path("unused.json")))
    band, global_line = help_modal._key_texts(104)
    assert band.count("H   Report") == 1
    assert not re.search(r"(?:^|\s)H\s+Report(?:\s|$)", global_line)


# ---------------------------------------------------------------------------
# LLR-4506: wording, exact bindings, stable hints and README
# ---------------------------------------------------------------------------
async def test_TC_4761_LLR_4506_1_present_help_names_only_HTML_deck(tmp_path):
    board = _default_board(tmp_path / "board.json")
    app = _app(board)
    async with app.run_test(size=(118, 31)) as pilot:
        await _present(pilot)
        await _press(pilot, "question_mark")
        text = app.screen.query_one("#pk-text").content.plain
    assert re.search(r"^  x\s+export this view · HTML deck$", text, re.M)
    assert "SVG" not in text and "PNG" not in text


async def test_TC_4762_LLR_4506_2_present_help_names_o_offer(tmp_path):
    board = _default_board(tmp_path / "board.json")
    app = _app(board)
    async with app.run_test(size=(118, 31)) as pilot:
        await _present(pilot)
        await _press(pilot, "question_mark")
        text = app.screen.query_one("#pk-text").content.plain
    assert re.search(r"^  o\s+open the last export \(10 s\)$", text, re.M)


def test_TC_4763_LLR_4506_3_present_bindings_are_base_plus_only_o():
    expected = {"1", "2", "3", "tab", "shift+tab", "up,k", "down,j",
                "left,h", "right,l", "pageup", "pagedown", "space", "a", "u",
                "shift+up,K", "shift+down,J", "enter", "x", "escape,q",
                "question_mark", "o"}
    assert {b.key for b in PresentScreen.BINDINGS} == expected
    offer = next(b for b in PresentScreen.BINDINGS if b.key == "o")
    assert offer.action == "open_export" and offer.priority


HINT_BASE = {
    (0, 130, 0): '1 gantt  2 split  3 all  ⇥ next · ←→ ↑↓ move · ␣ hide · a show all · x export · esc leave  ? keys',
    (0, 130, 2): '1 gantt  2 split  3 all  ⇥ next · ←→ ↑↓ move · ␣ hide · a show all · x export · esc leave · u 2 hidden  ? keys',
    (0, 118, 0): '1 gantt  2 split  3 all  ⇥ next · ←→ ↑↓ move · ␣ hide · a show all · x export · esc leave  ? keys',
    (0, 118, 2): '1 gantt  2 split  3 all  ⇥ next · ←→ ↑↓ move · ␣ hide · a show all · x export · esc leave · u 2 hidden  ? keys',
    (0, 100, 0): '1 gantt  2 split  3 all  ⇥ next · ←→ ↑↓ move · ␣ hide · a show all · x export · esc leave  ? keys',
    (0, 100, 2): '1 gantt 2 split 3 all ⇥ · ←→ · ␣ hide · a all · x export · esc · u 2 hidden  ? keys',
    (0, 80, 0): '1 gantt 2 split 3 all ⇥ · ←→ · ␣ hide · a all · x export · esc  ? keys',
    (0, 80, 2): '1 gantt 2 split 3 all ⇥ ←→ ␣ x esc · u 2 hidden  ? keys',
    (0, 60, 0): '1 gantt 2 split 3 all ⇥ ←→ ␣ x esc  ? keys',
    (0, 60, 2): '1 gantt 2 split 3 all ⇥ ←→ ␣ x esc · u 2 hidden  ? keys',
    (0, 36, 0): '1 gantt 2 split 3 all esc  ? keys',
    (0, 36, 2): '1 gantt 2 split 3 all esc…  ? keys',
    (1, 130, 0): '1 gantt  2 split  3 all  pgdn notes · ⇥ next · ←→ ↑↓ move · ␣ hide · a show all · x export · esc leave  ? keys',
    (1, 130, 2): '1 gantt  2 split  3 all  pgdn notes · ⇥ next · ←→ ↑↓ move · ␣ hide · a show all · x export · esc leave · u 2 hidden  ? keys',
    (1, 118, 0): '1 gantt  2 split  3 all  pgdn notes · ⇥ next · ←→ ↑↓ move · ␣ hide · a show all · x export · esc leave  ? keys',
    (1, 118, 2): '1 gantt  2 split  3 all  pgdn · ⇥ next · ←→ ↑↓ · ␣ hide · a show all · x export · esc · u 2 hidden  ? keys',
    (1, 100, 0): '1 gantt  2 split  3 all  pgdn · ⇥ next · ←→ ↑↓ · ␣ hide · a show all · x export · esc  ? keys',
    (1, 100, 2): '1 gantt 2 split 3 all pgdn · ⇥ · ←→ · ␣ hide · a all · x export · esc · u 2 hidden  ? keys',
    (1, 80, 0): '1 gantt 2 split 3 all pgdn · ⇥ · ←→ · ␣ hide · a all · x export · esc  ? keys',
    (1, 80, 2): '1 gantt 2 split 3 all pgdn ⇥ ←→ ␣ x esc · u 2 hidden  ? keys',
    (1, 60, 0): '1 gantt 2 split 3 all pgdn ⇥ ←→ ␣ x esc  ? keys',
    (1, 60, 2): '1 gantt 2 split 3 all esc · u 2 hidden  ? keys',
    (1, 36, 0): '1 gantt 2 split 3 all esc  ? keys',
    (1, 36, 2): '1 gantt 2 split 3 all esc…  ? keys',
    (2, 130, 0): '1 gantt  2 split  3 all  ⇥ · ↑↓ · ←→ rail · ␣ hide · K J order · enter fold · a all · x · esc  ? keys',
    (2, 130, 2): '1 gantt  2 split  3 all  ⇥ · ↑↓ · ←→ rail · ␣ hide · K J order · enter fold · a all · x · esc · u 2 hidden  ? keys',
    (2, 118, 0): '1 gantt  2 split  3 all  ⇥ · ↑↓ · ←→ rail · ␣ hide · K J order · enter fold · a all · x · esc  ? keys',
    (2, 118, 2): '1 gantt  2 split  3 all  ⇥ · ↑↓ · ←→ rail · ␣ hide · K J order · enter fold · a all · x · esc · u 2 hidden  ? keys',
    (2, 100, 0): '1 gantt 2 split 3 all ⇥ ↑↓ ←→ ␣ K J enter a x esc  ? keys',
    (2, 100, 2): '1 gantt 2 split 3 all ⇥ ↑↓ ←→ ␣ K J enter a x esc · u 2 hidden  ? keys',
    (2, 80, 0): '1 gantt 2 split 3 all ⇥ ←→ ↑↓ ␣ K J enter a x esc  ? keys',
    (2, 80, 2): '1 gantt 2 split 3 all ⇥ ←→ ↑↓ ␣ K J enter a x esc · u 2 hidden  ? keys',
    (2, 60, 0): '1 gantt 2 split 3 all ⇥ ←→ ↑↓ ␣ K J enter a x esc  ? keys',
    (2, 60, 2): '1 gantt 2 split 3 all esc · u 2 hidden  ? keys',
    (2, 36, 0): '1 gantt 2 split 3 all esc  ? keys',
    (2, 36, 2): '1 gantt 2 split 3 all esc…  ? keys',
}


@pytest.mark.parametrize("view,width,hidden", list(HINT_BASE))
def test_TC_4764_LLR_4506_4_hint_text_is_byte_stable_with_base(view, width, hidden):
    screen = PresentScreen(Board([], [], Path("unused.json")), "missing", None, None)
    screen._view = view
    assert screen._keys_hint(width, hidden, width - 2).plain == HINT_BASE[view, width, hidden]


def test_TC_4765_LLR_4506_5_readme_names_html_deck_not_svg_or_png():
    text = "\n".join(line for line in (ROOT / "README.md").read_text(encoding="utf-8").splitlines()
                     if "<img" not in line)
    assert not re.search(r"SVG|PNG", text)
    assert re.search(r"^\| `R` / `S` \|.*HTML deck", text, re.M)
