"""`H` exports the HTML reports from the app (batch 2026-10-29-batch-01, increment 004:
HLR-3107, LLR-3107.1..LLR-3107.5; AT-3101, AT-3105; TC-3117..TC-3120).

The app runs on a synthetic home of its own (the suite's `_never_the_real_home` seam):
the report fixture's three boards Personal / Client A / Course, each in its own folder
under `~/.taskboard/boards/`, registered in `~/.taskboard/boards.json`, Client A opened
last; `missing=True` adds a fourth registry board whose file is gone. Expected names,
slides and counts are typed from `report_fixture.py`, never read back from the code.

The written files are loaded headless per increment 001's PQ6 decision: the app's pilot
runs in the test's event loop, where the sync Playwright API refuses to start, so each
check launches Playwright INSIDE a worker thread (`asyncio.to_thread`). This module holds
no shared browser fixture — a module-scoped sync browser on the main thread breaks the
pilot's loop.
"""
from __future__ import annotations

import asyncio
import inspect
import json
import os
import re
from datetime import date
from pathlib import Path

import pytest
import report_fixture as F
from report_browser import new_context, open_page, require_browser, shown_ids
from test_modal_keys import INVENTORY
from test_report_deck import SLIDES, slides_of
from textual.widgets import Button

from taskboard import app as app_module, keymap, models, modals, views
from taskboard.models import LINKS_MIGRATION, MILESTONES_MIGRATION

DAY = "2026-10-29"
ARCH = " · "
LISTED = {"personal": ("Personal", "violet", F.personal),
          "client-a": ("Client A", "sky", F.client_a),
          "course": ("Course", "fuchsia", F.course)}
# The fixture's slides without the unlisted side board (not in this home's registry), and
# the open board AS THE APP HOLDS IT: opening Client A auto-archives its done work finished
# `AUTO_ARCHIVE_DAYS` (20) days ago — `Stakeholder interviews` (st1) — so Storefront
# relaunch reads 10 open-or-done tasks and 2 archived. The peeked boards are read as saved.
STOREFRONT = ("Storefront relaunch", "10 tasks" + ARCH + "2 archived")
HOME_SLIDES = SLIDES[:4] + [STOREFRONT] + SLIDES[5:-1]
assert SLIDES[4] == ("Storefront relaunch", "11 tasks" + ARCH + "1 archived")
assert HOME_SLIDES[-1] == (F.HOSTILE_NAME, "1 task") and len(HOME_SLIDES) == 10
HOME_SHOWN = {k for k in F.DEFAULT_SHOWN if not k.startswith("#3:")} - {"client-a:tst1"}


class _Today(date):
    @classmethod
    def today(cls):
        return F.TODAY


@pytest.fixture
def home(monkeypatch):
    for mod in (app_module, models, views, modals):
        monkeypatch.setattr(mod, "date", _Today)
    return Path.home() / ".taskboard"


def board_file(home: Path, bid: str) -> Path:
    return home / "boards" / bid / "board.json"


def build_home(home: Path, *, missing: bool = False, last: str = "client-a") -> None:
    entries = []
    for bid, (name, colour, make) in LISTED.items():
        board = make(board_file(home, bid))
        board.settings = {"migrations": {"links": LINKS_MIGRATION,
                                         "milestones": MILESTONES_MIGRATION},
                          "seen_view_renumber_2026_07": True}
        board.path.parent.mkdir(parents=True, exist_ok=True)
        board.save()
        entries.append({"id": bid, "name": name, "color": colour, "path": str(board.path),
                        "last_opened": "2026-10-29T09:00", "archived": False})
    if missing:
        entries.append({"id": "gone", "name": "Gone board", "color": "pink",
                        "path": str(board_file(home, "gone")),
                        "last_opened": "2026-10-28T09:00", "archived": False})
    (home / "boards.json").write_text(
        json.dumps({"version": 1, "last": last, "boards": entries}, indent=2), encoding="utf-8")


def open_home(home: Path, **kw):
    from taskboard.__main__ import open_app
    build_home(home, **kw)
    app = open_app(None)
    app.people.people.update(F.PEOPLE)         # the live directories, in memory only
    app.marks.marks.update(F.MARKS)
    return app


async def start(pilot):
    """The app opens on the home of boards (a registry of several); `esc` is the board."""
    await pilot.pause()
    await press(pilot, "escape")
    assert len(pilot.app.screen_stack) == 1


async def press(pilot, *keys):
    for k in keys:
        await pilot.press(k)
        await pilot.pause()


def painted(app) -> str:
    return "\n".join("".join(seg.text for seg in strip)
                     for strip in app.screen._compositor.render_strips(app.screen.size))


def report_toasts(app) -> list:
    return [n for n in app._notifications if n.title == "Report"]


def reports(home: Path, bid: str = "client-a") -> list[str]:
    folder = board_file(home, bid).parent / "reports"
    return sorted(p.name for p in folder.iterdir()) if folder.exists() else []


def toast_text(names: list[str], folder: Path, skipped: str = "") -> str:
    return f"Report written: {' and '.join(names)}{skipped}\n{folder}\no opens it (10 s)"


def footer(n: int, k: int) -> str:
    return f"{n} task{'s' if n != 1 else ''}" + (f"{ARCH}{k} archived" if k else "")


def embedded(page: str) -> dict:
    raw = re.search(r'<script id="board-data" type="application/json">(.*?)</script>',
                    page, re.S).group(1)
    return json.loads(raw)


def load_headless(path: Path, ready: str) -> tuple[list, object]:
    """Run in a worker thread (PQ6): Playwright launched here, never shared."""
    api = require_browser()
    with api.sync_playwright() as pw:
        browser = pw.chromium.launch()
        try:
            o = open_page(new_context(browser), path, ready=ready)
            out = {"problems": o.problems(),
                   "shown": set(shown_ids(o.page)) if ready == "#tbody" else None,
                   "scope": o.page.text_content("#scope-line") if ready == "#tbody" else None,
                   "slides": o.page.locator("section.slide").count()}
        finally:
            browser.close()
    return out["problems"], out


# --------------------------------------------------------------------------- #
# AT-3101 — `H b` writes the workspace, the toast names it, the file loads clean
# --------------------------------------------------------------------------- #
async def test_AT_3101_H_b_writes_the_workspace_and_the_toast_names_it(home, monkeypatch):
    """AT-3101 (US-3101, HLR-3107, HLR-3106): on the main screen `H`, `b` writes exactly
    one file, `reports/workspace-2026-10-29.html` beside the open board (Client A); one
    toast names it and the folder and offers `o`; `o` within the 10 s opens that file.
    The file, loaded headless, logs 0 console errors and 0 page errors, makes 0 requests
    but itself, and shows every loaded board's non-archived task from its embedded data
    under the scope line `All loaded boards (3): …`. RED: the toast drops the file name,
    or `o` keeps `open_url`."""
    require_browser()
    opened = []
    monkeypatch.setattr(os, "startfile", lambda p: opened.append(Path(p)), raising=False)
    app = open_home(home)
    folder = board_file(home, "client-a").parent / "reports"
    async with app.run_test(size=(118, 30)) as pilot:
        await start(pilot)
        await press(pilot, "H")
        assert isinstance(app.screen, modals.ReportExport)
        await press(pilot, "b")
        assert not isinstance(app.screen, modals.ReportExport)
        assert reports(home) == [f"workspace-{DAY}.html"]
        path = folder / f"workspace-{DAY}.html"
        assert path.stat().st_size > 0
        toasts = report_toasts(app)
        assert [n.message for n in toasts] == [toast_text([path.name], folder)]
        assert toasts[0].severity == "information" and toasts[0].timeout == 10
        await press(pilot, "o")
        assert opened == [path]
    problems, seen = await asyncio.to_thread(load_headless, path, "#tbody")
    assert problems == []
    assert seen["shown"] == HOME_SHOWN
    assert seen["scope"] == "All loaded boards (3): Personal, Client A, Course"


# --------------------------------------------------------------------------- #
# AT-3105 — `H c` writes the deck, one slide per chosen project; `a` agrees
# --------------------------------------------------------------------------- #
async def test_AT_3105_H_c_writes_the_deck_with_one_slide_per_chosen_project(home):
    """AT-3105 (US-3101, HLR-3105, HLR-3101): `H`, `c` (scope `o`, the default) writes
    `deck-2026-10-29.html` whose project slides are the three boards' literal slides
    (titles and `<n> tasks · <k> archived`); with a task of Storefront relaunch selected,
    `H`, `p`, `c` writes `deck-client-a-storefront-relaunch-2026-10-29.html` holding that
    project's slide only; `H`, `a` writes both files from one extraction: every deck
    slide's counts equal the workspace's embedded tasks of that project. The deck loads
    headless with 0 problems and 2 + 10 slides. RED: the deck keeps archived projects,
    or `p` is ignored."""
    require_browser()
    app = open_home(home)
    folder = board_file(home, "client-a").parent / "reports"
    async with app.run_test(size=(118, 30)) as pilot:
        await start(pilot)
        await press(pilot, "H", "c")
        deck = folder / f"deck-{DAY}.html"
        assert reports(home) == [deck.name]
        assert slides_of(deck.read_text(encoding="utf-8")) == HOME_SLIDES

        app.selected_task_id = "tst2"                    # Product photos, Storefront relaunch
        await press(pilot, "H", "p", "c")
        one = folder / f"deck-client-a-storefront-relaunch-{DAY}.html"
        assert one.exists()
        page = one.read_text(encoding="utf-8")
        assert slides_of(page) == [STOREFRONT]
        assert '<p class="scope">Project Storefront relaunch on Client A</p>' in page

        await press(pilot, "H", "a")
        ws = folder / f"workspace-{DAY}.html"
        assert reports(home) == sorted([deck.name, one.name, ws.name])
        data = embedded(ws.read_text(encoding="utf-8"))
        both = deck.read_text(encoding="utf-8")
        keys = re.findall(r'<section class="slide" data-project="([^"]+)"', both)
        assert len(keys) == len(HOME_SLIDES)
        for key, (_title, foot) in zip(keys, slides_of(both)):
            mine = [t for t in data["tasks"] if t["project"] == key]
            n = sum(1 for t in mine if t["status"] != "archived")
            assert foot == footer(n, len(mine) - n), key
    problems, seen = await asyncio.to_thread(load_headless, deck, "#cnt")
    assert problems == [] and seen["slides"] == 2 + len(HOME_SLIDES)


# --------------------------------------------------------------------------- #
# TC-3117 — the `H` seat
# --------------------------------------------------------------------------- #
async def test_TC_3117_H_is_seated_once_off_the_bar(home):
    """TC-3117 (LLR-3107.1): exactly one `KEYMAP` row shows `H` — action `report_export`,
    group misc, off the bar like `R`/`A`/`S`; it is in the palette and in `?`'s global
    keys of every view, and `?` paints `H Report`; lowercase `h` keeps its meaning (left).
    RED: the row dropped."""
    rows = [k for k in keymap.KEYMAP if k.show == "H"]
    assert len(rows) == 1
    h = rows[0]
    assert (h.keys, h.action, h.label, h.group, h.bar) == ("H", "report_export", "Report",
                                                            "misc", False)
    for view in keymap.VIEWS:
        assert ("H", "Report", "report_export") in keymap.palette_commands(view)
        assert h in keymap.global_keys(view)
    assert next(k for k in keymap.KEYMAP if k.action == "hmove(-1)").keys == "left,h"
    app = open_home(home)
    async with app.run_test(size=(118, 30)) as pilot:
        await start(pilot)
        await press(pilot, "question_mark")
        await pilot.pause()
        assert "H Report" in painted(app)


# --------------------------------------------------------------------------- #
# TC-3118 — the modal's scope keys, and no current project
# --------------------------------------------------------------------------- #
async def test_TC_3118_scope_keys_and_no_project(home):
    """TC-3118 (LLR-3107.2): the scope starts at `o` (all boards, marked `●`); `p` marks
    the current project — the selected task's, else the focused one — and the modal stays;
    `o` marks all boards again; `esc` closes and writes nothing. With no selected task and
    no focus, the scope and the key line read `no project selected` and `p` leaves `o`
    marked. The modal has no Button and its `INVENTORY` row is `{}`. RED: the current
    project taken from `present_project_id` (its first-project fallback)."""
    assert INVENTORY["ReportExport"] == {}
    assert not any("Button(" in line for line in
                   inspect.getsource(modals.ReportExport).splitlines())
    app = open_home(home)
    async with app.run_test(size=(118, 30)) as pilot:
        await start(pilot)
        app.selected_task_id = "tst2"
        await press(pilot, "H")
        assert not list(app.screen.query(Button))
        text = painted(app)
        assert "● all boards (3)" in text and "○ Storefront relaunch on Client A" in text
        await press(pilot, "p")
        assert isinstance(app.screen, modals.ReportExport)
        text = painted(app)
        assert "○ all boards (3)" in text and "● Storefront relaunch on Client A" in text
        await press(pilot, "o")
        assert "● all boards (3)" in painted(app)
        await press(pilot, "escape")
        assert not isinstance(app.screen, modals.ReportExport)

        app.selected_task_id = None
        app.focused_project_id = "pdocs"                 # the focused project, Client A's Docs
        await press(pilot, "H", "p")
        assert "● Docs on Client A" in painted(app)
        await press(pilot, "escape")

        app.focused_project_id = None
        await press(pilot, "H")
        text = painted(app)
        assert "○ no project selected" in text and "p no project selected" in text
        await press(pilot, "p")
        assert isinstance(app.screen, modals.ReportExport)
        assert "● all boards (3)" in painted(app)
        await press(pilot, "escape")
        assert not isinstance(app.screen, modals.ReportExport)
    assert reports(home) == []


# --------------------------------------------------------------------------- #
# TC-3119 — the files land beside the open board
# --------------------------------------------------------------------------- #
async def test_TC_3119_files_land_beside_the_open_board(home, tmp_path, monkeypatch):
    """TC-3119 (LLR-3107.3): with a registry of the three boards plus one whose file is
    gone, `H`, `a` writes exactly `workspace-` and `deck-2026-10-29.html` in the OPEN
    board's `reports/` (not the working directory), the toast counts the gone board; a
    second same-day export overwrites (still 2 files); scope `p` names the file with the
    board and project slugs, so Client A's and Personal's `Docs` get 2 distinct names; no
    board file changes a byte. RED: the files written beside the CWD."""
    cwd = tmp_path / "cwd"
    cwd.mkdir()
    monkeypatch.chdir(cwd)
    app = open_home(home, missing=True)
    folder = board_file(home, "client-a").parent / "reports"
    async with app.run_test(size=(118, 30)) as pilot:
        await start(pilot)
        kept = {bid: board_file(home, bid).read_bytes() for bid in LISTED}
        await press(pilot, "H")
        assert "all boards (3)" in painted(app)          # the gone board is not counted here
        await press(pilot, "a")
        both = [f"workspace-{DAY}.html", f"deck-{DAY}.html"]
        assert reports(home) == sorted(both)
        assert report_toasts(app)[-1].message == toast_text(both, folder, " · 1 board skipped")
        await press(pilot, "H", "a")
        assert reports(home) == sorted(both)
        app.selected_task_id = None                      # the focus decides with no selection
        app.focused_project_id = "pdocs"
        await press(pilot, "H", "p", "b")
        assert f"workspace-client-a-docs-{DAY}.html" in reports(home)
        assert {bid: board_file(home, bid).read_bytes() for bid in LISTED} == kept
    assert list(cwd.iterdir()) == []

    other = open_home(home, last="personal")
    async with other.run_test(size=(118, 30)) as pilot:
        await start(pilot)
        other.selected_task_id = "tdc1"                  # Docs index, Personal's Docs
        await press(pilot, "H", "p", "b")
    assert reports(home, "personal") == [f"workspace-personal-docs-{DAY}.html"]


# --------------------------------------------------------------------------- #
# TC-3120 — `o` opens the report while the toast lives, once, on the main screen
# --------------------------------------------------------------------------- #
async def test_TC_3120_o_opens_the_report_while_the_toast_lives(home, monkeypatch):
    """TC-3120 (LLR-3107.4, PDR C8, D9, D16): the toast is read from the app's
    notification record; through the `_report_clock` seam, `o` at 9.9 s opens the written
    file (inside `<board dir>/reports/`) and no task URL; a second `o` is `open_url` again
    (single use); `o` past 10 s is `open_url`; an `o` over another screen leaves the offer
    for the main screen; without `os.startfile` the opener is `webbrowser.open` of the
    file URI; after `a` the offer is the workspace; an opener that fails (`OSError`, or
    `webbrowser.open` False) says so in a toast. RED: the offer never expires."""
    now = [100.0]
    opened, urls = [], []
    monkeypatch.setattr(os, "startfile", lambda p: opened.append(Path(p)), raising=False)
    browser_ok = [True]
    monkeypatch.setattr(app_module.webbrowser, "open",
                        lambda u: urls.append(u) or browser_ok[0])
    app = open_home(home)
    monkeypatch.setattr(app, "_report_clock", lambda: now[0])
    folder = board_file(home, "client-a").parent / "reports"
    path = folder / f"workspace-{DAY}.html"
    link = "https://staging.example.test/storefront"
    async with app.run_test(size=(118, 30)) as pilot:
        await start(pilot)
        app.selected_task_id = "tst4"                    # Homepage build, one valid URL
        await press(pilot, "H", "b")
        toast = report_toasts(app)
        assert len(toast) == 1 and toast[0].message == toast_text([path.name], folder)
        # DU4: the names, the folder and the offer each on a line of their own, so a long
        # folder path wraps on its own line and never splits a file name
        assert toast[0].message.split("\n") == [f"Report written: workspace-{DAY}.html",
                                                str(folder), "o opens it (10 s)"]
        now[0] = 109.9
        await press(pilot, "o")
        assert opened == [path] and urls == []
        assert path.parent == board_file(home, "client-a").parent / "reports"
        await press(pilot, "o")
        assert opened == [path] and urls == [link]

        now[0] = 200.0
        await press(pilot, "H", "b")
        now[0] = 210.01
        await press(pilot, "o")
        assert opened == [path] and urls == [link, link]

        now[0] = 300.0
        await press(pilot, "H", "b", "question_mark")
        assert len(app.screen_stack) > 1
        await press(pilot, "o", "escape")
        assert len(app.screen_stack) == 1 and opened == [path]
        await press(pilot, "o")
        assert opened == [path, path]

        now[0] = 400.0                                   # `a`: `o` opens the workspace
        await press(pilot, "H", "a", "o")
        assert opened == [path, path, path]

        monkeypatch.delattr(os, "startfile", raising=False)
        await press(pilot, "H", "b", "o")
        assert opened == [path, path, path] and urls[-1] == path.as_uri()
        cannot = f"Could not open the report {path.name}."
        assert cannot not in [n.message for n in report_toasts(app)]

        browser_ok[0] = False                            # the browser refuses: said so
        await press(pilot, "H", "b", "o")
        assert urls[-1] == path.as_uri()
        assert report_toasts(app)[-1].message == cannot

        def refuse(p):
            raise OSError("no handler")
        monkeypatch.setattr(os, "startfile", refuse, raising=False)
        await press(pilot, "H", "b", "o")
        last = report_toasts(app)[-1]
        assert last.message == cannot and last.severity == "error"


async def test_TC_3120_a_failed_write_toasts_and_offers_nothing(home, monkeypatch):
    """TC-3120 (LLR-3107.4, code review CR4-2): when writing fails (`OSError`, perhaps
    after a part was written) the app does not crash: one error toast `Report not (fully)
    written: <error>`, and no offer — not even the earlier export's, still live — so `o`
    is `open_url` again. RED: the write unguarded, or the offer left set on error."""
    opened, urls = [], []
    monkeypatch.setattr(os, "startfile", lambda p: opened.append(Path(p)), raising=False)
    monkeypatch.setattr(app_module.webbrowser, "open", lambda u: urls.append(u) or True)
    app = open_home(home)
    link = "https://staging.example.test/storefront"
    async with app.run_test(size=(118, 30)) as pilot:
        await start(pilot)
        app.selected_task_id = "tst4"
        await press(pilot, "H", "b")                     # a live offer from a good export

        def full(*args):
            raise OSError("disk full")
        monkeypatch.setattr(app_module.report_html, "write_reports", full)
        await press(pilot, "H", "b")
        assert not isinstance(app.screen, modals.ReportExport)
        last = report_toasts(app)[-1]
        assert (last.message, last.severity) == ("Report not (fully) written: disk full", "error")
        await press(pilot, "o")
        assert opened == [] and urls == [link]
