"""The editor's class Select and the `#` manager (batch 2026-10-24-batch-01).

HLR-2605 / LLR-2605.1 — the editor's variant-A Select: a Textual `Select` in
`#task-chips-what` directly after `#f-milestone`, its options `none` and every
class of the directory as explicit-style `Text` pieces (never markup, C-17),
NO `+ new class…` option; `alt+m` focuses it and opens it, and the key sits in
`TASK_KEYS` on the editor's key line; choosing a class writes the task's
`mark`, choosing `none` saves with no `mark` key; an EMPTY directory composes
no Select and the editor draws as before. HLR-2606 / LLR-2606.1/.2/.3 — `#`
opens `app.MarksManager` (global, off the key bar like `@`): the frame is
`views.render_marks` with the live open/all counts of every board; `n`/`e` open
`modals.MarkForm` (name, shape row, colour row, a live preview; the modal-keys
law); `space` toggles `hidden`, persisted in `marks.json`; `esc` AND `#`
close; `d` and `↵` are inert; a refused write says
`The marks directory was not saved: <reason>` and keeps the form.

Laws: TC-2605, TC-2606, AT-2601 (`test_AT_2601_a_class_is_created_and_survives`
— `#`, `n`, a name, a shape, a colour, `alt+s`; the editor's `alt+m`; a
restart; the class persists and the gantt draws its glyph in its colour, the
styled-segment export oracle). Boards are the round's synthetic fixture;
TODAY is pinned. RED on base_ref: `#` is unbound, no manager, no Select.
"""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import pytest
from rich.text import Text
from textual.widgets import Input, Select

import milestone_marks_fixture as fx
from taskboard import app as app_module
from taskboard import keymap, modals, views
from taskboard.app import BoardsHome, MarksManager, TaskboardApp
from taskboard.marks import MARKS_NAME

TODAY = fx.TODAY
HEX = {k: v.lower() for k, v in views.HEX.items()}


class _Today(date):
    @classmethod
    def today(cls):
        return fx.TODAY


@pytest.fixture
def home(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
    for mod in (app_module, modals, views):
        monkeypatch.setattr(mod, "date", _Today)
    return tmp_path / ".taskboard"


def _open(home, last="client-a"):
    from taskboard.__main__ import open_app
    fx.build(home, last=last)
    return open_app(None)


def _open_empty(home, last="client-a"):
    """The fixture's boards with NO class directory: the app always loads one,
    possibly empty (LLR-2601.3)."""
    from taskboard.__main__ import open_app
    fx.build(home, last=last)
    (home / MARKS_NAME).unlink()
    return open_app(None)


async def _press(pilot, *keys):
    for k in keys:
        await pilot.press(k)
        await pilot.pause()


def _notes(app) -> list[str]:
    return [str(n.message) for n in app._notifications]


# --------------------------------------------------------------------------- #
# The painted-frame helpers (Textual's styled-segment export — the tone oracle)
# --------------------------------------------------------------------------- #
def _painted(app) -> list[list[tuple[str, str | None]]]:
    strips = app.screen._compositor.render_strips(app.screen.size)
    rows = []
    for s in strips:
        cells = []
        for seg in s:
            hx = (seg.style.color.triplet.hex.lower()
                  if seg.style and seg.style.color and seg.style.color.triplet else None)
            cells += [(ch, hx) for ch in seg.text]
        rows.append(cells)
    return rows


def _text(rows) -> list[str]:
    return ["".join(ch for ch, _ in r) for r in rows]


def _prow(rows, needle):
    for r in rows:
        if needle in "".join(ch for ch, _ in r):
            return r
    raise AssertionError(f"{needle!r} not painted")


# --------------------------------------------------------------------------- #
# TC-2605 — the editor's class Select (LLR-2605.1)
# --------------------------------------------------------------------------- #
async def test_TC_2605_the_editor_mounts_the_class_select_after_milestone(home):
    """`e` on a classed milestone → the Select in `#task-chips-what` directly
    after `f-milestone`, `none` first then the directory's classes, each option
    a Text piece, the task's class selected; `alt+m` focuses it and opens the
    overlay; the key line names `alt+m mark`; `TASK_KEYS` carries it. RED: the
    Select mounted elsewhere, or `alt+m` unbound."""
    app = _open(home)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        await pilot.press("escape")                  # the home → the main screen
        app.selected_task_id = "tc4"                 # Index v1 delivered · delivery
        app.refresh_view()
        await pilot.pause()
        await _press(pilot, "e")
        scr = app.screen
        assert isinstance(scr, modals.TaskModal)
        chips = [w.id for w in scr.query_one("#task-chips-what").query("*") if w.id]
        assert chips.index("f-mark") == chips.index("f-milestone") + 1
        sel = scr.query_one("#f-mark", Select)
        assert sel.value == "delivery"
        opts = sel._options                       # (prompt, value) pairs, as composed
        assert [v for _p, v in opts] == ["", "delivery", "payment", "review", "launch"]
        # every option its shape in its colour and its name in the ink tone —
        # Text pieces, never markup (C-17)
        assert all(isinstance(p, Text) for p, _v in opts)
        pay = next(p for p, v in opts if v == "payment")
        assert pay.plain == "⬢ Payment"
        assert str(pay.spans[0].style) == views.HEX["amber"]
        assert str(pay.spans[1].style) == views.HEX["ink"]
        none = opts[0][0]
        assert none.plain == "◆ none"
        # no `+ new class…` option: the manager adds, the Select only picks
        assert all("new class" not in p.plain for p, _v in opts)
        # the key is SAID: on the key line, and in TASK_KEYS after the save key
        assert ("alt+m", "mark") in modals.TASK_KEYS
        painted = "\n".join(_text(_painted(app)))
        assert "alt+m mark" in painted
        # `alt+m` → the Select takes the focus and its overlay opens
        await _press(pilot, "alt+m")
        assert sel.expanded and sel.has_focus_within
        overlay = "\n".join(_text(_painted(app)))
        for _cid, n, s, _h, _k in fx.CLASSES:
            assert n in overlay and s in overlay
        assert "none" in overlay
        await _press(pilot, "escape")


async def test_TC_2605_down_enter_carries_the_next_class(home):
    """`alt+m`, `down`, `enter` → the next class saved on the task; the file
    holds the id. RED: the Select writes markup, or nothing is saved."""
    app = _open(home)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        await pilot.press("escape")
        app.selected_task_id = "tc4"                 # delivery (index 1)
        app.refresh_view()
        await pilot.pause()
        await _press(pilot, "e", "alt+m", "down", "enter", "alt+s")
        assert not isinstance(app.screen, modals.TaskModal)
        assert app.board.task_by_id("tc4").mark == "payment"
    data = json.loads(fx.board_path(home, "client-a").read_text(encoding="utf-8"))
    t = next(t for t in data["tasks"] if t["id"] == "tc4")
    assert t["mark"] == "payment"


async def test_TC_2605_none_saves_with_no_mark_key(home):
    """`alt+m`, `up` to `none`, `enter`, `alt+s` → the saved task carries no
    `mark` key (the board file's other marks untouched). RED: `mark: null`
    written, or the field kept."""
    app = _open(home)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        await pilot.press("escape")
        app.selected_task_id = "tc4"                 # delivery
        app.refresh_view()
        await pilot.pause()
        await _press(pilot, "e", "alt+m", "up", "enter", "alt+s")
        assert app.board.task_by_id("tc4").mark is None
    data = json.loads(fx.board_path(home, "client-a").read_text(encoding="utf-8"))
    t = next(t for t in data["tasks"] if t["id"] == "tc4")
    assert "mark" not in t
    assert next(t for t in data["tasks"] if t["id"] == "tc6")["mark"] == "review"


async def test_TC_2605_a_markup_looking_class_name_shows_as_typed(home):
    """A class named `[b]x[/b]`: its option and its overlay row print as typed
    — a Text piece, never parsed (C-17). RED: the option built as a markup
    string (the name renders bold or vanishes)."""
    fx.build(home, last="client-a")
    path = home / MARKS_NAME
    data = json.loads(path.read_text(encoding="utf-8"))
    data["marks"].append({"id": "hostile", "name": "[b]x[/b]", "shape": "★",
                          "colour": "pink"})
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    from taskboard.__main__ import open_app
    app = open_app(None)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        await pilot.press("escape")
        app.selected_task_id = "tc4"
        app.refresh_view()
        await pilot.pause()
        await _press(pilot, "e")
        sel = app.screen.query_one("#f-mark", Select)
        hostile = next(p for p, v in sel._options if v == "hostile")
        assert hostile.plain == "★ [b]x[/b]"
        await _press(pilot, "alt+m")
        overlay = "\n".join(_text(_painted(app)))
        assert "[b]x[/b]" in overlay


async def test_TC_2605_an_empty_directory_composes_no_select(home):
    """The app always loads a directory, possibly empty: with none, the editor
    draws NO Select — no `#f-mark`, no `alt+m` on the key line, and the tab
    walk has no stop between `milestone` and `start` (the walk of
    tests/test_edit_window.py stays green). RED: the Select composed for an
    empty directory."""
    app = _open_empty(home)
    async with app.run_test(size=(80, 24)) as pilot:
        await pilot.pause()
        await pilot.press("escape")
        app.selected_task_id = "tc4"
        app.refresh_view()
        await pilot.pause()
        await _press(pilot, "e")
        scr = app.screen
        assert isinstance(scr, modals.TaskModal)
        assert not scr.query("#f-mark")
        painted = "\n".join(_text(_painted(app)))
        assert "alt+m" not in painted
        # the tab walk: f-milestone is followed by f-start, no Select between
        scr.query_one("#f-milestone").focus()
        await _press(pilot, "tab")
        assert app.focused is not None and app.focused.id == "f-start"


# --------------------------------------------------------------------------- #
# TC-2606 — `#` in the seat, the manager, the form (LLR-2606.1/.2)
# --------------------------------------------------------------------------- #
def test_TC_2606_keymap_hash_is_global_off_the_bar_and_listed():
    """The seat: `#` is `number_sign` → `marks_manager`, `Milestone classes`,
    global and off the bar like `@`; `?`'s global line and the palette list it;
    the action exists on the app."""
    seat = {k.action: k for k in keymap.KEYMAP}
    k = seat["marks_manager"]
    assert k.keys == "number_sign" and k.show == "#"
    assert k.label == "Milestone classes" and k.group == "misc"
    assert k.views is None and not k.bar and not k.universal
    assert hasattr(TaskboardApp, "action_marks_manager")
    assert ("# Milestone classes" in {f"{g.show} {g.label}" for g in keymap.global_keys("gantt")})
    assert "marks_manager" in {a for _s, _l, a in keymap.palette_commands("kanban")}


@pytest.mark.parametrize("size", [(118, 30), (80, 24)])
async def test_TC_2606_the_manager_lists_every_class_with_counts_and_the_key_row(home, size):
    """`#` → the manager over the main screen: every class with its shape in
    its colour, its name, the open/all counts read from every board, the
    chosen row `▶`; the key row names `↑↓ move ␣ hide/show n new e edit esc
    close`; `d` and `↵` change nothing (inert, like `@`'s seat behind its
    screen). RED: a count missing, or `d` bound."""
    app = _open(home)
    async with app.run_test(size=size) as pilot:
        await pilot.pause()
        await pilot.press("escape")
        await _press(pilot, "number_sign")
        assert isinstance(app.screen, MarksManager)
        rows = _painted(app)
        painted = "\n".join(_text(rows))
        for _cid, n, s, _h, _k in fx.CLASSES:
            assert n in painted and s in painted, (n, painted)
        assert "↑↓ move   ␣ hide/show   n new   e edit   esc close" in painted
        assert "only this" not in painted and "delete" not in painted
        assert "# Milestone classes" in painted and "marks.json" in painted
        # the chosen row is the first, marked ▶
        row = _prow(rows, "Delivery")
        assert "▶" in "".join(ch for ch, _ in row)
        # the shape wears the class colour (the styled-segment export)
        dtext = "".join(ch for ch, _ in row)
        assert row[dtext.index("▲")][1] == HEX["cyan"]
        # the counts: delivery = 1 open of 2 (one reached)
        drow = "".join(ch for ch, _ in row)
        assert "1 open 2 in all" in drow
        # `d` and `↵` are inert: the file and the screen do not move
        before = (home / MARKS_NAME).read_bytes()
        n_tasks = len(app.board.tasks)
        await _press(pilot, "d", "enter")
        assert isinstance(app.screen, MarksManager)
        assert (home / MARKS_NAME).read_bytes() == before
        assert len(app.board.tasks) == n_tasks


async def test_TC_2606_space_hides_a_class_persisted_and_the_frame_redraws(home):
    """`space` on a class → `marks.json` holds `hidden: true`, the frame
    redraws it dimmed with `hidden: gantt + present`, and the board beneath is
    refreshed (its live `marks` dict already holds the flag). RED: the toggle
    not persisted, or the frame unchanged."""
    app = _open(home)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        await pilot.press("escape")
        await _press(pilot, "number_sign", "down")    # on Payment
        await _press(pilot, "space")
        data = json.loads((home / MARKS_NAME).read_text(encoding="utf-8"))
        assert next(m for m in data["marks"] if m["id"] == "payment")["hidden"] is True
        assert app.marks.marks["payment"].hidden is True     # the board's live dict
        assert app.board.marks["payment"].hidden is True
        row = "".join(ch for ch, _ in _prow(_painted(app), "Payment"))
        assert "[ ]" in row and "hidden: gantt + present" in row
        await _press(pilot, "space")                  # back
        data = json.loads((home / MARKS_NAME).read_text(encoding="utf-8"))
        assert next(m for m in data["marks"] if m["id"] == "payment")["hidden"] is False


async def test_TC_2606_e_edits_the_class_and_keeps_its_id(home):
    """`e` on a class → the form on it (its name shown); a new name, `alt+s` →
    the same id in `marks.json`, the name changed, the frame redrawn. RED: the
    id lost on rename (the tasks' marks would dangle)."""
    app = _open(home)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        await pilot.press("escape")
        await _press(pilot, "number_sign", "down")    # on Payment
        await _press(pilot, "e")
        assert isinstance(app.screen, modals.MarkForm)
        assert app.screen.query_one("#mf-name", Input).value == "Payment"
        app.screen.query_one("#mf-name", Input).value = "Billing"
        await _press(pilot, "alt+s")
        assert isinstance(app.screen, MarksManager)
    data = json.loads((home / MARKS_NAME).read_text(encoding="utf-8"))
    m = next(m for m in data["marks"] if m["id"] == "payment")
    assert m["name"] == "Billing" and m["shape"] == "⬢" and m["colour"] == "amber"


async def test_TC_2606_a_refused_write_says_so_and_keeps_the_form(home, monkeypatch):
    """A failed `Directory.add` → `The marks directory was not saved: <reason>`
    and the FORM STAYS OPEN (the operator fixes the name or cancels). RED: the
    form dismissed, or nothing said."""
    app = _open(home)
    monkeypatch.setattr(app.marks, "add",
                        lambda *a: (_ for _ in ()).throw(OSError("disk full")))
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.pause()
        await pilot.press("escape")
        await _press(pilot, "number_sign", "n")
        assert isinstance(app.screen, modals.MarkForm)
        await _press(pilot, *"Legal", "alt+s")
        assert isinstance(app.screen, modals.MarkForm)    # the form is kept
        assert any("The marks directory was not saved: disk full" in n
                   for n in _notes(app)), _notes(app)
        # the directory did not gain the class
        assert "legal" not in app.marks.marks
        await _press(pilot, "escape")                     # esc cancels, form drops


async def test_TC_2606_a_blank_name_is_refused_and_the_form_is_kept(home):
    """`alt+s` with no name → `A class needs a name.`, the form kept. RED: an
    unnamed class saved, or the form dropped."""
    app = _open(home)
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.pause()
        await pilot.press("escape")
        await _press(pilot, "number_sign", "n")
        assert isinstance(app.screen, modals.MarkForm)
        await _press(pilot, "alt+s")
        assert isinstance(app.screen, modals.MarkForm)
        assert any("A class needs a name." in n for n in _notes(app)), _notes(app)
        await _press(pilot, "escape")


async def test_TC_2606_hash_opens_from_the_main_screen_and_the_home_and_hash_esc_close(home):
    """`#` on the main screen and on the home opens the manager; `#` closes it
    too, and `esc`; `?` lists it. RED: `#` bound on a screen only, or it does
    not close."""
    app = _open(home)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        await pilot.press("escape")                   # the main screen
        await _press(pilot, "number_sign")
        assert isinstance(app.screen, MarksManager)
        await _press(pilot, "number_sign")            # `#` closes it too
        assert not isinstance(app.screen, MarksManager)
        await _press(pilot, "B")                      # the home
        assert isinstance(app.screen, BoardsHome)
        await _press(pilot, "number_sign")
        assert isinstance(app.screen, MarksManager)
        await _press(pilot, "escape")                 # back to the home
        assert isinstance(app.screen, BoardsHome)
        await _press(pilot, "escape")                 # the main screen again
        # `?` lists it among the globals
        await _press(pilot, "question_mark")
        painted = "\n".join(_text(_painted(app)))
        assert "Milestone classes" in painted
        await _press(pilot, "escape")


async def test_TC_2606_hash_over_a_modal_does_nothing(home):
    """`#` pressed while the task editor is open opens nothing: a pushed modal
    holds its own keys (architect A-9). RED: the manager piles over the
    editor."""
    app = _open(home)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        await pilot.press("escape")
        await _press(pilot, "a")
        assert isinstance(app.screen, modals.TaskModal)
        await _press(pilot, "number_sign", "d", "1")
        assert isinstance(app.screen, modals.TaskModal)
        await _press(pilot, "escape")


async def test_TC_2606_the_seat_keys_are_refused_behind_the_manager(home):
    """While the manager holds the keys, no seat action but `quit` acts: `a`,
    `d`, `1`, `B`, `4` change nothing. RED: a seat key fires behind the
    manager."""
    app = _open(home)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        await pilot.press("escape")
        view_mode, n_tasks = app.view_mode, len(app.board.tasks)
        await _press(pilot, "number_sign")
        assert isinstance(app.screen, MarksManager)
        await _press(pilot, "a", "d", "1", "B", "4")
        assert isinstance(app.screen, MarksManager)
        assert app.view_mode == view_mode and len(app.board.tasks) == n_tasks


async def test_TC_2606_an_empty_directory_says_so_and_n_still_works(home):
    """An empty directory: the frame says `No classes yet.` and `n` still
    opens the form (the boundary: adding the first class). RED: the empty
    state drawn as a blank frame, or `n` dead."""
    app = _open_empty(home)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        await pilot.press("escape")
        await _press(pilot, "number_sign")
        assert isinstance(app.screen, MarksManager)
        painted = "\n".join(_text(_painted(app)))
        assert "No classes yet." in painted and "n adds the first class." in painted
        await _press(pilot, "n")
        assert isinstance(app.screen, modals.MarkForm)
        await _press(pilot, *"First", "alt+s")
        assert isinstance(app.screen, MarksManager)
    data = json.loads((home / MARKS_NAME).read_text(encoding="utf-8"))
    assert next(m for m in data["marks"] if m["name"] == "First")


# --------------------------------------------------------------------------- #
# AT-2601 — a class is created and survives (the manager → the editor → restart)
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("size", [(118, 30), (80, 24)])
async def test_AT_2601_a_class_is_created_and_survives(home, size):
    """AT-2601 (HLR-2601/2605/2606): `#` → the manager lists every class with
    its shape and colour; `n` → the form with the name focused, the shape row
    and the colour row and a live preview; a name, `alt+h`, `right`, `alt+c`,
    `left`, `alt+s` → the class in `marks.json` with the chosen shape and
    colour; `alt+m` in the editor carries it to a milestone; a restart keeps
    it and the gantt draws its glyph in its colour (the styled-segment export,
    never plain text). RED: `_commit` updating memory only (restart loses the
    class), or the seat returning `◆` always."""
    app = _open(home)
    async with app.run_test(size=size, notifications=True) as pilot:
        await pilot.pause()
        await pilot.press("escape")
        await _press(pilot, "number_sign")
        assert isinstance(app.screen, MarksManager)
        painted = "\n".join(_text(_painted(app)))
        for _cid, n, s, _hh, _k in fx.CLASSES:
            assert n in painted and s in painted
        assert "↑↓ move   ␣ hide/show   n new   e edit   esc close" in painted
        # n → the form: the name focused, the rows, the preview, the key line
        await _press(pilot, "n")
        assert isinstance(app.screen, modals.MarkForm)
        assert app.focused is not None and app.focused.id == "mf-name"
        form = app.screen
        assert form.query_one("#mf-shape") is not None
        assert form.query_one("#mf-colour") is not None
        painted = "\n".join(_text(_painted(app)))
        assert "preview" in painted and "open" in painted
        assert "late" in painted and "reached" in painted
        assert ("alt+n name   alt+c colour   alt+h shape   alt+s save   esc cancel"
                in painted), painted
        # a name, alt+h, right, alt+c, left, alt+s → the class saved
        await _press(pilot, *"Legal", "alt+h", "right", "alt+c", "left", "alt+s")
        assert isinstance(app.screen, MarksManager)
        # the editor's `alt+m` carries the class to a milestone
        await _press(pilot, "escape")                # back to the main screen
        app.selected_task_id = "tcd"                 # Handover call · unclassified
        app.refresh_view()
        await pilot.pause()
        await _press(pilot, "e", "alt+m")
        sel = app.screen.query_one("#f-mark", Select)
        assert sel.expanded
        for _ in range(5):                           # none → … → Legal (last)
            await _press(pilot, "down")
        await _press(pilot, "enter", "alt+s")
        assert app.board.task_by_id("tcd").mark == "legal"
    data = json.loads((home / MARKS_NAME).read_text(encoding="utf-8"))
    m = next(m for m in data["marks"] if m["name"] == "Legal")
    assert m["id"] == "legal"
    # the defaults stepped once each: shape ⬟→▼, colour orange→green
    assert m["shape"] == "▼" and m["colour"] == "green"
    # a restart: the class persists and the gantt draws it in its colour
    from taskboard.__main__ import open_app
    app2 = open_app(None)
    async with app2.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        await pilot.press("escape")
        assert "legal" in app2.marks.marks
        app2.selected_task_id = "tcd"
        await _press(pilot, "3")                     # the gantt
        rows = _painted(app2)
        row = _prow(rows, "Handover call")
        text = "".join(ch for ch, _ in row)
        assert row[text.index("▼")][1] == HEX["green"]
