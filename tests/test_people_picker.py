"""The `@` picker in the task editor's notes (batch 2026-10-21-batch-01, the round's
item 2, variant A: a dropdown under the cursor).

HLR-2503 / LLR-2503.1, LLR-2503.2 · TC-2503 · AT-2503 (US-2502). Why it matters: a
mention is a word the operator types without leaving the note — `@an`, `↵`, and the
note holds `@ana.ruiz`; a new person is added in place, once, for every board. The
picker must never eat a key the notes need while it is closed (`enter`, the arrows,
`esc`), and must never save the task by accident (the role is confirmed with `↵`, not
`alt+s`). Synthetic people only, under the seam's home.
"""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import pytest
from textual.widgets import Input, Static, TextArea

import people_round_fixture as fx
from taskboard import app as app_module, boards, models, modals, views
from taskboard.modals import MentionDrop, TaskModal, pick_rows
from taskboard.people import Directory


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


def typed(s: str) -> list[str]:
    return ["enter" if ch == "\n" else "space" if ch == " " else "at" if ch == "@" else ch
            for ch in s]


async def _editor(pilot, app, tid="tc8"):
    await pilot.pause()
    await pilot.press("escape")                 # the home
    app.selected_task_id = tid
    app.refresh_view()
    await pilot.press("e")
    await pilot.pause()
    notes = app.screen.query_one("#f-notes", TextArea)
    notes.focus()
    notes.move_cursor(notes.document.end)
    await pilot.pause()
    return notes


async def _type(pilot, s):
    for k in typed(s):
        await pilot.press(k)
    await pilot.pause(0.2)


def _drop(app) -> MentionDrop:
    return app.screen.query_one("#mdrop", MentionDrop)


def _list(app) -> str:
    return str(_drop(app).query_one("#md-list", Static).render())


def _open_app(home, last="client-a"):
    from taskboard.__main__ import open_app
    fx.build(home, last=last)
    return open_app(None)


# --------------------------------------------------------------------------- #
# TC-2503 — the rows (LLR-2503.1)
# --------------------------------------------------------------------------- #
def test_TC_2503_rows_list_the_finds_then_add_when_no_name_matches(tmp_path):
    fx.build(tmp_path)
    d = Directory.load(tmp_path / "people.json")
    rows, opts = pick_rows(d, "an", 0, 44, 5)
    assert [o[1].id if o[0] == "p" else o for o in opts] == [
        "ana.ruiz", "andres.lima", "juana.soto", "marta.gil", ("add", "an")]
    assert rows[0].plain.startswith("▶ Ana Ruiz") and rows[-1].plain.startswith("  + add 'an'")
    assert all(r.cell_len == 44 for r in rows)
    _rows, opts = pick_rows(d, "ana ruiz", 0, 44, 5)
    assert [o[0] for o in opts] == ["p"]              # an exact name: no `+ add`
    rows, opts = pick_rows(d, "", 0, 44, 5)
    assert len(opts) == 5 and all(o[0] == "p" for o in opts)   # `@` alone: no add row
    rows, opts = pick_rows(Directory(tmp_path / "none.json"), "", 0, 44, 5)
    assert opts == [] and rows[0].plain.strip() == "type a name"


def test_TC_2503_a_name_that_looks_like_markup_is_a_text_piece(tmp_path):
    d = Directory(tmp_path / "people.json")
    d.add("[b]Bold[/b]", "[red]role")
    rows, _ = pick_rows(d, "", 0, 44, 5)
    assert "[b]Bold[/b]" in rows[0].plain and "[red]role" in rows[0].plain


# --------------------------------------------------------------------------- #
# AT-2503 — writing a mention in the real editor
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("size", [(118, 30), (80, 24)])
async def test_AT_2503_at_an_enter_writes_the_handle_and_the_preview_the_name(home, size):
    app = _open_app(home)
    async with app.run_test(size=size) as pilot:
        notes = await _editor(pilot, app)
        await _type(pilot, "\nAsk @an")
        drop = _drop(app)
        assert drop.display
        listing = _list(app)
        assert listing.index("Ana Ruiz") < listing.index("Andrés Lima") < listing.index("+ add 'an'")
        x, _y = drop.styles.offset.x.value, drop.styles.offset.y.value
        assert 0 <= x and x + drop.outer_size.width <= size[0]
        await pilot.press("enter")
        await _type(pilot, "about the stores")
        assert notes.text.splitlines()[-1] == "Ask @ana.ruiz about the stores"
        assert not _drop(app).display
        preview = str(app.screen.query_one("#task-preview", Static).render())
        assert "Ask @Ana Ruiz about the stores" in preview
        await pilot.press("alt+s")
        await pilot.pause()
    saved = json.loads(fx.board_path(home, "client-a").read_text(encoding="utf-8"))
    task = next(t for t in saved["tasks"] if t["id"] == "tc8")
    assert task["notes"].endswith("Ask @ana.ruiz about the stores")


async def test_TC_2503_arrows_choose_and_esc_leaves_plain_text(home):
    app = _open_app(home)
    async with app.run_test(size=(118, 30)) as pilot:
        notes = await _editor(pilot, app)
        await _type(pilot, "\nwith @an")
        await pilot.press("down", "down", "up", "enter")
        assert notes.text.splitlines()[-1] == "with @andres.lima "
        await _type(pilot, "and @ma")
        assert _drop(app).display
        await pilot.press("escape")                       # the picker closes, nothing else
        await pilot.pause()
        assert not _drop(app).display and isinstance(app.screen, TaskModal)
        assert notes.text.splitlines()[-1] == "with @andres.lima and @ma"
        await pilot.press("enter")                        # closed: enter is a new line again
        assert notes.text.endswith("and @ma\n")
        await pilot.press("escape")                       # and esc cancels the editor
        await pilot.pause()
        assert not isinstance(app.screen, TaskModal)


async def test_TC_2503_add_a_person_in_place_for_every_board(home):
    app = _open_app(home)
    async with app.run_test(size=(118, 30)) as pilot:
        notes = await _editor(pilot, app)
        await _type(pilot, "\nCall @Sofia")
        assert _list(app).splitlines()[0].strip() == "▶ + add 'Sofia'  new person"
        await pilot.press("enter")
        await pilot.pause()
        name = app.screen.query_one("#md-name", Input)
        role = app.screen.query_one("#md-role", Input)
        assert name.value == "Sofia" and role.has_focus
        assert "add + mention" in str(_drop(app).query_one("#md-keys", Static).render())
        await pilot.press("tab")
        assert name.has_focus
        await pilot.press("end")                          # focus selects the field's text
        await _type(pilot, " Vega")
        await pilot.press("tab")
        await _type(pilot, "Legal counsel")
        await pilot.press("enter")
        await pilot.pause()
        assert notes.text.splitlines()[-1] == "Call @sofia.vega "
        assert isinstance(app.screen, TaskModal)          # ↵ added the person, it saved nothing
        preview = str(app.screen.query_one("#task-preview", Static).render())
        assert "@Sofia Vega" in preview
    raw = json.loads((home / "people.json").read_text(encoding="utf-8"))
    assert {"id": "sofia.vega", "name": "Sofia Vega", "role": "Legal counsel", "note": ""} in raw["people"]
    saved = json.loads(fx.board_path(home, "client-a").read_text(encoding="utf-8"))
    assert "sofia" not in json.dumps(saved)               # esc'd editor: the task unsaved


async def test_TC_2503_esc_in_the_new_person_goes_back_to_the_list(home):
    app = _open_app(home)
    async with app.run_test(size=(118, 30)) as pilot:
        notes = await _editor(pilot, app)
        await _type(pilot, "\n@Sofia")
        await pilot.press("enter", "escape")
        await pilot.pause()
        assert _drop(app).display and notes.has_focus
        assert "+ add 'Sofia'" in _list(app)
        assert not (home / "people.json").read_text(encoding="utf-8").count("Sofia")


async def test_TC_2503_a_failed_add_says_so_and_keeps_the_form(home, monkeypatch):
    monkeypatch.setattr(boards, "LOCK_WAIT", 0.1)
    app = _open_app(home)
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        notes = await _editor(pilot, app)
        await _type(pilot, "\n@Sofia")
        await pilot.press("enter")
        with boards.file_lock(home / "people.json"):
            await pilot.press("enter")
            await pilot.pause()
        msgs = [str(n.message) for n in app._notifications]
        assert any(m.startswith("The person was not added: ") and "busy" in m for m in msgs)
        assert app.screen._mention == "add" and notes.text.endswith("@Sofia")


@pytest.mark.parametrize("text", ["\nmail ana@x", "\n@ana.ruiz", "\nword@an", "\nAsk @ana.ruiz."])
async def test_TC_2503_no_picker_inside_a_word_or_on_a_known_handle(home, text):
    app = _open_app(home)
    async with app.run_test(size=(118, 30)) as pilot:
        await _editor(pilot, app)
        await _type(pilot, text)
        assert not _drop(app).display


async def test_TC_2503_without_a_directory_at_is_plain_text(home):
    app = _open_app(home)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        await pilot.press("escape")
        app.push_screen(TaskModal(app.board))
        await pilot.pause()
        notes = app.screen.query_one("#f-notes", TextArea)
        notes.focus()
        await _type(pilot, "@an")
        await pilot.press("enter")
        assert not _drop(app).display and notes.text == "@an\n"


async def test_TC_2503_reached_by_tab_the_list_opens_inside_the_screen_and_flips_up(home):
    """ux UX-3, qa QA-2: the notes reached the operator's way (tab from the title), the
    cursor on the notes' last visible row at 80x24: the list opens ABOVE it, every row
    of it inside the screen."""
    app = _open_app(home)
    async with app.run_test(size=(80, 24)) as pilot:
        await pilot.pause()
        await pilot.press("escape")
        app.selected_task_id = "tc8"
        app.refresh_view()
        await pilot.press("e")
        await pilot.pause()
        for _ in range(20):
            if app.focused is not None and app.focused.id == "f-notes":
                break
            await pilot.press("tab")
        notes = app.screen.query_one("#f-notes", TextArea)
        assert app.focused is notes
        notes.move_cursor(notes.document.end)
        await _type(pilot, "\n\n\n\n\n\nAsk @an")
        drop = _drop(app)
        assert drop.display
        cy = notes.cursor_screen_offset.y
        y, h = drop.styles.offset.y.value, drop.outer_size.height
        assert y + h <= 24 and y < cy                    # flipped above the cursor


async def test_TC_2503_tab_leaves_the_notes_and_the_mention_as_typed(home):
    """architect A-5: `tab` with the list open closes it; `enter` on the next field
    writes no mention into the notes."""
    app = _open_app(home)
    async with app.run_test(size=(118, 30)) as pilot:
        notes = await _editor(pilot, app)
        await _type(pilot, "\nAsk @an")
        await pilot.press("tab")
        await pilot.pause()
        assert not _drop(app).display and not notes.has_focus
        await pilot.press("enter")
        await pilot.pause()
        assert notes.text.endswith("Ask @an")


async def test_TC_2503_closed_the_arrows_move_the_cursor(home):
    """qa QA-11: with the list closed, `up` moves the notes' cursor as before."""
    app = _open_app(home)
    async with app.run_test(size=(118, 30)) as pilot:
        notes = await _editor(pilot, app)
        row = notes.cursor_location[0]
        await pilot.press("up")
        await pilot.pause()
        assert notes.cursor_location[0] == row - 1 and not _drop(app).display


async def test_TC_2503_the_form_left_for_the_notes_closes_and_writes_nothing(home):
    """code review CR-1: with the new person's form open, the focus back in the notes
    (a click) closes it; typing and `enter` there are the notes' own — no person added,
    no text replaced."""
    app = _open_app(home)
    async with app.run_test(size=(118, 30)) as pilot:
        notes = await _editor(pilot, app)
        before = (home / "people.json").read_bytes()
        await _type(pilot, "\nCall @Sofia")
        await pilot.press("enter")
        await pilot.pause()
        assert app.screen._mention == "add"
        notes.focus()                                   # the operator clicks the notes
        await pilot.pause()
        assert not _drop(app).display
        await _type(pilot, " today")
        await pilot.press("enter")
        await pilot.pause()
        assert notes.text.endswith("Call @Sofia today\n")
        assert (home / "people.json").read_bytes() == before


async def test_TC_2503_with_no_one_listed_enter_is_a_new_line(home):
    """code review CR-4: an empty directory lists no one; `enter` stays the notes'."""
    from taskboard.people import Directory
    app = _open_app(home)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        await pilot.press("escape")
        app.push_screen(TaskModal(app.board, people=Directory(home / "nobody.json")))
        await pilot.pause()
        notes = app.screen.query_one("#f-notes", TextArea)
        notes.focus()
        await _type(pilot, "@")
        assert _drop(app).display and "type a name" in _list(app)
        await pilot.press("enter")
        await pilot.pause()
        assert notes.text == "@\n"


async def test_TC_2503_a_click_away_closes_the_list(home):
    """architect A-5: the list open, a click on the title closes it; `enter` there is the
    title's own and the notes keep the typed text."""
    app = _open_app(home)
    async with app.run_test(size=(118, 30)) as pilot:
        notes = await _editor(pilot, app)
        await _type(pilot, "\nAsk @an")
        assert _drop(app).display
        app.screen.query_one("#f-title").focus()        # the operator clicks the title
        await pilot.pause()
        assert not _drop(app).display
        await pilot.press("enter")
        await pilot.pause()
        assert notes.text.endswith("Ask @an")
