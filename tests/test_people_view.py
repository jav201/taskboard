"""The people directory's view on `@` (batch 2026-10-21-batch-01, the round's item 1:
variant A's two panes, with C's mentioning note line under each task and B's progress
box — the operator's objection to item 1).

HLR-2504 / LLR-2504.1, LLR-2504.2, LLR-2504.3 · TC-2504 · AT-2504 (US-2503). Why it
matters: in a meeting the operator answers «what do I owe Ana?» from one screen —
who needs them most, that person's open tasks of every board by urgency, what was
written about them, and one key to the task on its board. D4: the view is titled
`PEOPLE · directory` and `@` is `People directory`, apart from view 9's team `People`.
Synthetic people only, under the seam's home.
"""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import pytest
from rich.text import Text

import people_round_fixture as fx
from taskboard import app as app_module, keymap, models, modals, views
from taskboard.app import PeopleDirectory
from taskboard.models import Board
from taskboard.people import Directory, Person
from test_people_look import screen_text

TODAY = fx.TODAY


class _Today(date):
    @classmethod
    def today(cls):
        return fx.TODAY


@pytest.fixture
def home(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
    for mod in (app_module, models, views, modals):
        monkeypatch.setattr(mod, "date", _Today)
    return tmp_path / ".taskboard"


def _lanes(root: Path):
    out = []
    for bid, name, colour, _rel, _h in fx.BOARDS:
        out.append((name, colour, Board.load(fx.board_path(root, bid)), ""))
    return out


@pytest.fixture
def world(tmp_path):
    fx.build(tmp_path)
    d = Directory.load(tmp_path / "people.json")
    lanes = _lanes(tmp_path)
    items = {h: views.person_items(lanes, h, TODAY) for h in d.people}
    return d, lanes, items


# --------------------------------------------------------------------------- #
# TC-2504 — the pure parts (LLR-2504.1)
# --------------------------------------------------------------------------- #
def test_TC_2504_a_persons_items_are_banded_and_ordered(world):
    d, _lanes_, items = world
    ana = items["ana.ruiz"]
    assert [(x.band, x.task.title, x.board_name) for x in ana] == [
        ("late", "Chunking experiments", "Client A"),
        ("today", "Golden question set", "Client A"),
        ("week", "Steering committee", "Client A"),
        ("later", "Guest talk: RAG in retail", "Course"),
        ("later", "Eval report v1", "Client A")]
    assert views.person_counts(ana) == (1, 1, 5)
    assert views.person_counts(items["pablo.ortiz"]) == (0, 0, 1)


def test_TC_2504_done_and_archived_tasks_are_not_owed(tmp_path):
    fx.build(tmp_path)
    b = Board.load(fx.board_path(tmp_path, "client-a"))
    golden = b.task_by_id("tc5")
    golden.archived = True
    chunk = b.task_by_id("tc2")
    chunk.phase = b.phases[-1]
    titles = [x.task.title for x in views.person_items([("Client A", "sky", b, "")], "ana.ruiz", TODAY)]
    assert "Golden question set" not in titles and "Chunking experiments" not in titles
    assert views.person_items([("X", "sky", None, "file missing")], "ana.ruiz", TODAY) == []


def test_TC_2504_people_are_ordered_by_who_needs_the_operator_most(world):
    d, _l, items = world
    order = [p.id for p in views.people_by_urgency(list(d.people.values()), items)]
    assert order == ["ana.ruiz", "diego.paz", "marta.gil", "luis.mora", "andres.lima",
                     "elena.vidal", "juana.soto", "pablo.ortiz"]


def test_TC_2504_the_progress_box_says_late_today_open():
    box = views.progress_box([], 40)
    assert [r.plain for r in box] == ["╭──────────────╮", "│ nothing open │", "╰──────────────╯"]


@pytest.mark.parametrize("w", [116, 78, 40])
def test_TC_2504_every_row_is_the_width_and_the_composition_holds(world, w):
    d, _l, items = world
    people = views.people_by_urgency(list(d.people.values()), items)
    t = views.render_people_directory(people, items, 0, "tasks", 1, TODAY, w, 29, d.people)
    rows = t.plain.split("\n")
    assert len(rows) == 29 and all(Text(r).cell_len == w for r in rows)
    flat = t.plain
    assert flat.startswith("◆ PEOPLE · directory")
    if w >= 78:
        assert "1 late · 1 today · 5 open" in flat
        assert "“Review the 40 questions with @Ana" in flat
        assert ("“Review the 40 questions with @Ana Ruiz in Tuesday's sync”" in flat) is (w == 116)
        assert any("│ ▶  Client A" in r and "Golden question set" in r for r in rows)
    assert ("Eval harness" in flat) is (w >= 116)        # the project column from 78 cells of pane


def test_TC_2504_each_task_carries_its_mentioning_line_under_it(world):
    d, _l, items = world
    people = views.people_by_urgency(list(d.people.values()), items)
    rows = views.render_people_directory(people, items, 0, "people", 0, TODAY, 116, 40,
                                         d.people).plain.split("\n")
    for title, quote in [("Chunking experiments", "“Waiting on @Ana Ruiz to confirm"),
                         ("Steering committee", "“ask @Ana Ruiz for the go/no-go criteria”"),
                         ("Eval report v1", "(@Elena Vidal)”")]:
        i = next(k for k, r in enumerate(rows) if title in r)
        assert quote in rows[i + 1], (title, rows[i + 1])


def test_TC_2504_strings_are_printed_as_typed_and_the_empty_directory_says_what_to_do(tmp_path):
    p = Person("x.y", "[b]Bold[/b]", "[red]role", "[i]note")
    t = views.render_people_directory([p], {}, 0, "people", 0, TODAY, 100, 20).plain
    assert "[b]Bold[/b]" in t and "[red]role" in t and "[i]note" in t and "nothing open" in t
    t = views.render_people_directory([], {}, 0, "people", 0, TODAY, 80, 10).plain
    assert "No one in the directory yet." in t and "n adds a person" in t
    assert "0 people · tasks read-only" in t                            # QA-10
    one = views.render_people_directory([p], {}, 0, "people", 0, TODAY, 80, 20).plain
    assert "1 person · tasks read-only" in one                            # QA-6: singular


def test_TC_2504_the_tasks_pane_scrolls_to_keep_the_cursor(world):
    d, _l, items = world
    people = views.people_by_urgency(list(d.people.values()), items)
    t = views.render_people_directory(people, items, 0, "tasks", 4, TODAY, 78, 22, d.people).plain
    assert "▶  Client A Eval report v1" in t and "“Draft with @Ana Ruiz; sign-off by the…" in t
    rows = t.split("\n")
    first = next(r.split("│", 1)[1] for r in rows[8:] if r.split("│", 1)[1].strip())
    assert not first.lstrip().startswith("“")                 # ux UX-5: no orphan quote
    top = views.render_people_directory(people, items, 0, "people", 0, TODAY, 78, 22,
                                        d.people).plain
    assert "↓ 2 more below" in top and "Eval report v1" not in top


# --------------------------------------------------------------------------- #
# D4 — named apart from view 9
# --------------------------------------------------------------------------- #
def test_D4_the_directory_is_named_apart_from_the_team_people_view():
    seat = {k.action: k for k in keymap.KEYMAP}
    assert seat["people_directory"].show == "@" and seat["people_directory"].keys == "at"
    assert seat["people_directory"].label == "People directory"
    assert seat["view('people')"].label == "People" and not seat["people_directory"].bar
    assert views.PEOPLE_TITLE == "PEOPLE · directory"


# --------------------------------------------------------------------------- #
# AT-2504 — the view in the real app
# --------------------------------------------------------------------------- #
def _open(home, last="client-a"):
    from taskboard.__main__ import open_app
    fx.build(home, last=last)
    return open_app(None)


@pytest.mark.parametrize("size", [(118, 30), (80, 24)])
async def test_AT_2504_at_shows_who_needs_what_and_enter_opens_the_task(home, size):
    app = _open(home, last="main")                 # opened on Personal
    async with app.run_test(size=size) as pilot:
        await pilot.pause()
        await pilot.press("at")                    # from the home (qa QA-3)
        text = await screen_text(pilot, *size)
        assert isinstance(app.screen, PeopleDirectory)
        assert isinstance(app.screen_stack[-2], app_module.BoardsHome)
        assert "◆ PEOPLE · directory" in text and "▶ Ana Ruiz" in text
        assert "1 late · 1 today · 5 open" in text and "“Waiting on @Ana Ruiz" in text
        last = text.splitlines()[-1].strip()
        assert last == "↑↓ move   ⇥ panes   ↵ their tasks   / find   n add   e edit person   esc back"
        await pilot.press("tab")
        last = (await screen_text(pilot, *size)).splitlines()[-1]
        assert "↵ open task" in last and "esc back" in last              # ux UX-1, UX-4
        await pilot.press("down", "enter")
        await pilot.pause()
        assert len(app.screen_stack) == 1 and app.board_id == "client-a"   # the home too
        assert app.selected_task_id == "tc5"


async def test_AT_2504_enter_on_the_people_goes_to_their_tasks_and_esc_or_at_closes(home):
    app = _open(home)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        await pilot.press("escape", "at", "down", "down")
        scr = app.screen
        assert scr.people[scr.sel].id == "marta.gil"
        await pilot.press("enter")
        assert scr.pane == "tasks" and isinstance(app.screen, PeopleDirectory)
        text = await screen_text(pilot, 118, 30)
        assert "Marta Gil" in text and "Invoice October" in text
        await pilot.press("escape")
        assert not isinstance(app.screen, PeopleDirectory)
        await pilot.press("at")
        await pilot.pause()
        await pilot.press("at")
        await pilot.pause()
        assert not isinstance(app.screen, PeopleDirectory)


async def test_AT_2504_n_adds_e_edits_and_slash_finds(home):
    app = _open(home)
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.pause()
        await pilot.press("escape", "at", "n")
        await pilot.pause()
        assert isinstance(app.screen, modals.PersonForm)
        for k in "Sofia":
            await pilot.press(k)
        await pilot.press("space", "V", "e", "g", "a", "tab")
        for k in "Legal":
            await pilot.press(k)
        await pilot.press("alt+s")
        await pilot.pause()
        scr = app.screen
        assert isinstance(scr, PeopleDirectory) and scr.people[scr.sel].id == "sofia.vega"
        await pilot.press("e")
        await pilot.pause()
        assert "Edit person @sofia.vega" in await screen_text(pilot, 118, 30)   # QA-6
        await pilot.press("end", "space", "R", "u", "i", "z", "enter")         # QA-9: typed
        await pilot.pause()
        assert scr.people[scr.sel].name == "Sofia Vega Ruiz" and scr.people[scr.sel].id == "sofia.vega"
        await pilot.press("slash")
        await pilot.pause()
        for k in "marta":
            await pilot.press(k)
        await pilot.press("enter")
        await pilot.pause()
        assert scr.people[scr.sel].id == "marta.gil"
        await pilot.press("slash", "z", "z", "enter")
        await pilot.pause()
        assert "No one in the directory matches 'zz'." in [str(n.message) for n in app._notifications]
        await pilot.press("n", "alt+s")                                   # QA-6: no name
        await pilot.pause()
        assert "A person needs a name." in [str(n.message) for n in app._notifications]
        assert isinstance(app.screen, modals.PersonForm)
        await pilot.press("escape")
    raw = json.loads((home / "people.json").read_text(encoding="utf-8"))
    assert {"id": "sofia.vega", "name": "Sofia Vega Ruiz", "role": "Legal", "note": ""} in raw["people"]


async def test_AT_2504_the_main_screens_keys_do_not_act_behind_it(home):
    app = _open(home)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        await pilot.press("escape")
        before = (app.view_mode, app.board_id, len(app.board.tasks), app.selected_task_id)
        await pilot.press("at", "a", "d", "1", "B", "4")
        await pilot.pause()
        assert isinstance(app.screen, PeopleDirectory) and len(app.screen_stack) == 2
        assert (app.view_mode, app.board_id, len(app.board.tasks),
                app.selected_task_id) == before                          # QA-8
        app.pop_screen()
        app.push_screen(modals.ConfirmModal("Sure?"))
        await pilot.pause()
        await pilot.press("at")
        await pilot.pause()
        assert isinstance(app.screen, modals.ConfirmModal)
        await pilot.press("n", "R")                                       # A-11: the presentation
        await pilot.pause()
        await pilot.press("at")
        await pilot.pause()
        assert isinstance(app.screen, app_module.PresentScreen)


def test_TC_2504_the_tones_say_late_today_and_who(world):
    """ux UX-2: the box's blocks red/amber/grey and its words; the counts' ▲ red, ● amber;
    the chosen person's name pink — read from the Text's spans, not inspected."""
    d, _l, items = world
    box = views.progress_box(items["ana.ruiz"], 60)[1]
    spans = [(box.plain[s.start:s.end], str(s.style)) for s in box.spans]
    assert ("█", views.HEX["over"]) in spans and ("█", views.HEX["soon"]) in spans
    assert ("███", views.HEX["later"]) in spans
    assert ("1 late", f"b {views.HEX['over']}") in spans and ("1 today", f"b {views.HEX['soon']}") in spans
    people = views.people_by_urgency(list(d.people.values()), items)
    t = views.render_people_directory(people, items, 0, "people", 0, TODAY, 116, 29, d.people)
    row = t.split("\n")[2]
    styles = {row.plain[s.start:s.end]: str(s.style) for s in row.spans}
    assert styles["▲1"] == f"b {views.HEX['over']}" and styles["●1"] == f"b {views.HEX['soon']}"
    assert styles["Ana Ruiz"] in (f"b {views.HEX['pink']}", f"b {views.HEX['bright']}")
    assert f"b {views.HEX['pink']}" in [str(s.style) for s in row.spans]


async def test_AT_2504_errors_are_said_and_change_nothing(home, monkeypatch):
    """qa QA-5: a task whose board file vanished, and a directory that cannot be written."""
    from taskboard import boards
    monkeypatch.setattr(boards, "LOCK_WAIT", 0.1)
    app = _open(home, last="main")
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.pause()
        await pilot.press("escape", "at", "tab", "down")
        fx.board_path(home, "client-a").unlink()
        await pilot.press("enter")
        await pilot.pause()
        assert app.board_id == "main"
        assert any("its file is missing" in str(n.message) for n in app._notifications)
        before = (home / "people.json").read_bytes()
        await pilot.press("at", "n")
        await pilot.pause()
        for k in "Zoe":
            await pilot.press(k)
        with boards.file_lock(home / "people.json"):
            await pilot.press("alt+s")
            await pilot.pause()
        assert any(str(n.message).startswith("The directory was not saved: ")
                   for n in app._notifications)
        assert (home / "people.json").read_bytes() == before


async def test_AT_2504_at_from_the_main_screen(home):
    """architect A-11: `@` on the main screen itself (not the home)."""
    app = _open(home)
    async with app.run_test(size=(80, 24)) as pilot:
        await pilot.pause()
        await pilot.press("escape")
        assert len(app.screen_stack) == 1
        await pilot.press("at")
        await pilot.pause()
        assert isinstance(app.screen, PeopleDirectory) and len(app.screen_stack) == 2


@pytest.mark.parametrize("h, row", [(20, 4), (21, 4), (22, 4), (20, 3), (24, 2)])
def test_TC_2504_the_cursors_task_and_quote_are_always_shown_and_the_marker_counts(world, h, row):
    """code review CR-1 of increment 004: at any height the cursor's task and its quote
    are on screen, a marker never says `↓ 0 more below`, and it counts the tasks below."""
    d, _l, items = world
    people = views.people_by_urgency(list(d.people.values()), items)
    t = views.render_people_directory(people, items, 0, "tasks", row, TODAY, 78, h, d.people).plain
    title = items["ana.ruiz"][row].task.title
    lines = t.split("\n")
    i = next(k for k, r in enumerate(lines) if "│" in r and "▶  " in r.split("│", 1)[1]
             and title in r)
    assert "“" in lines[i + 1]                                   # its quote right under it
    assert "↓ 0 more below" not in t
    if "more below" in t:
        n = int(t.split("↓ ", 1)[1].split(" ", 1)[0])
        unseen = [x for x in items["ana.ruiz"][row + 1:] if x.task.title not in t]
        assert n == len(unseen) > 0


async def test_AT_2504_at_and_a_never_pile_up(home):
    """code review CR-2 of increment 004: `@`, `A`, `@` brings the directory back to the
    top instead of pushing a second one."""
    app = _open(home)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        await pilot.press("escape", "at", "A", "at")
        await pilot.pause()
        names = [type(s).__name__ for s in app.screen_stack]
        assert names == ["Screen", "PeopleDirectory"]
        await pilot.press("A", "A")                   # `A` on the agenda closes it
        await pilot.pause()
        assert [type(s).__name__ for s in app.screen_stack] == ["Screen", "PeopleDirectory"]


def test_TC_2504_today_outranks_a_longer_list():
    """Who needs the operator most: one due today beats two with no date (the urgency
    key's second term)."""
    from taskboard.views import PersonItem
    x, y = Person("x", "Xavier"), Person("y", "Yara")
    item = lambda band: PersonItem(band, 0, "B", "sky", None, "", None)
    items = {"x": [item("today")], "y": [item("nodate"), item("nodate")]}
    assert [p.id for p in views.people_by_urgency([y, x], items)] == ["x", "y"]


def test_TC_2504_the_wide_head_says_tasks_read_only():
    t = views.render_people_directory([], {}, 0, "people", 0, TODAY, 116, 6).plain
    assert "0 in the directory · tasks read-only" in t


@pytest.mark.parametrize("h, row", [(22, 3), (18, 2), (14, 1), (20, 4), (24, 4)])
def test_TC_2504_a_quote_is_never_shown_without_its_task(world, h, row):
    """ux UX-5: scrolled, every quote on screen sits right under its task's row."""
    d, _l, items = world
    people = views.people_by_urgency(list(d.people.values()), items)
    t = views.render_people_directory(people, items, 0, "tasks", row, TODAY, 78, h, d.people).plain
    right = [r.split("│", 1)[1] for r in t.split("\n") if "│" in r]
    for i, r in enumerate(right):
        if r.lstrip().startswith("“"):
            assert i and any(b in right[i - 1] for b in ("Client A", "Course", "Personal")), \
                (h, row, right[i - 1])
