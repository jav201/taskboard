"""A direct key for every modal button, written on the modal.

Batch 2026-10-20-batch-03: HLR-2406 / LLR-2406.1 · TC-2406 · AT-2406 (US-2404) — a
confirmation answers `y`/`n`, says so, and shows its whole message; HLR-2407 /
LLR-2407.1 · TC-2407 · AT-2407 (US-2404) — beside text fields every button has an
`alt+<letter>` key on a key line, and the inventory law holds every `ModalScreen` of
the package to it. The operator's objection to the round's item 6: «Para tener un
acceso directo a los botones. (y cuando hay bloques de entrada de texto usar una
combinación específica)». Synthetic data only, under this test's own home.
"""
from __future__ import annotations

import html
import inspect
import json
import re
from datetime import date
from pathlib import Path

import pytest
from rich.text import Text
from textual.screen import ModalScreen
from textual.widgets import Button

import backlog_round_fixture as fx
from taskboard import app as app_module, keymap, models, modals, views
from taskboard.app import BoardsHome, TaskboardApp
from taskboard.modals import ConfirmModal

_SVG = re.compile(r'<text class="[^"]*" x="([\d.]+)" y="[\d.]+" textLength="[\d.]+" '
                  r'clip-path="url\(#[^)]*-line-(\d+)\)">([^<]*)</text>')


def _svg_rows(svg: str, width: int, height: int) -> list[str]:
    """The text rows of a Textual `export_screenshot` SVG, each `<text>` at its column."""
    rows = [[" "] * width for _ in range(height)]
    for x, line, body in _SVG.findall(svg):
        y, col = int(line), round(float(x) / 12.2)
        if y >= height:
            continue
        for i, ch in enumerate(html.unescape(body).replace("\xa0", " ")):
            if col + i < width:
                rows[y][col + i] = ch
    return ["".join(r).rstrip() for r in rows]


async def _screen(pilot, w, h) -> str:
    await pilot.pause(0.5)          # a pushed screen paints before it is read
    return "\n".join(_svg_rows(pilot.app.export_screenshot(), w, h))


def _flat(text: str) -> str:
    """The screen's words in one line: a wrapped message reads as one sentence."""
    return " ".join(text.split())


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


def _round_app(home, last="client-a"):
    from taskboard.__main__ import open_app
    fx.build(home, last=last)
    return open_app(None)


async def _press(pilot, *keys):
    for k in keys:
        await pilot.press(k)
        await pilot.pause()


def _notes(app) -> list:
    return [str(n.message) for n in app._notifications]


# --------------------------------------------------------------------------- #
# TC-2406 — `key_line` and `ConfirmModal`'s keys (LLR-2406.1)
# --------------------------------------------------------------------------- #
def test_TC_2406_key_line_is_the_key_bar_style_and_keeps_its_keys():
    """TC-2406: each key bold bright, its word muted, three spaces apart, a ` / `
    inside a key dim; fitted, the words go from the right before any key."""
    key_line = keymap.key_line
    line = key_line([("y", "archive"), ("n / esc", "cancel")])
    assert line.plain == "y archive   n / esc cancel"
    styles = {line.plain[s.start:s.end]: str(s.style) for s in line.spans}
    assert styles["y"] == keymap.KEY_STYLE and styles["esc"] == keymap.KEY_STYLE
    assert styles[" archive"] == views.HEX["mut"] and styles[" / "] == views.HEX["dim"]
    pairs = [("alt+s", "save"), ("alt+i", "paste image"), ("esc", "cancel")]
    assert key_line(pairs, 30).plain == "alt+s save   alt+i   esc"
    assert key_line(pairs, 20).plain == "alt+s   alt+i   esc"
    assert key_line(pairs, 12).plain == "alt+s"          # the keys go last, from the right
    assert key_line([]).plain == ""


@pytest.mark.parametrize("key, answer", [("y", [True]), ("n", [False]), ("escape", [False]),
                                         ("enter", [])])
async def test_TC_2406_a_confirmation_answers_y_and_n_and_not_enter(home, key, answer):
    """TC-2406: `y` → True, `n` and `esc` → False; `enter` alone answers nothing
    while the box holds the focus."""
    app = TaskboardApp(board_path=home / "board.json")
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        got = []
        app.push_screen(ConfirmModal("Delete 'x'?"), got.append)
        await pilot.pause()
        await _press(pilot, key)
        assert got == answer
        assert isinstance(app.screen, ConfirmModal) is (answer == [])


async def test_TC_2406_the_message_wraps_and_is_whole(home):
    """TC-2406: a 128-character message takes two rows or more in the box, its last
    words on screen (the round cut it at «…its folder is not»)."""
    msg = ("Archive Personal? It leaves the home; its folder is not touched. "
           "taskboard --board /x/boards/personal/board.json brings it back.")
    app = TaskboardApp(board_path=home / "board.json")
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        app.push_screen(ConfirmModal(msg, confirm="Archive", variant="warning"))
        await pilot.pause()
        label = app.screen.query_one("#confirm-box .modal-title")
        assert label.size.height >= 2
        assert "brings it back." in _flat(await _screen(pilot, 118, 30))


# --------------------------------------------------------------------------- #
# AT-2406 — the home's archive and a task's delete by keys (US-2404)
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("size", [(118, 30), (80, 24)])
async def test_AT_2406_a_confirmation_is_one_written_key(home, size):
    """AT-2406 (US-2404): the home's `x` shows the whole message and its key line;
    `enter` does nothing, `n` cancels, `y` archives; a task's `d`, `y` deletes it."""
    w, h = size
    app = _round_app(home)
    path = str((home / "board.json").resolve())
    async with app.run_test(size=size, notifications=True) as pilot:
        await pilot.pause()
        assert isinstance(app.screen, BoardsHome)
        await _press(pilot, "left", "x")
        assert isinstance(app.screen, ConfirmModal)
        r = app.screen.query_one("#confirm-box").region     # the box as painted, cropped
        rows = (await _screen(pilot, w, h)).splitlines()
        flat = _flat(" ".join(row[r.x + 1:r.right - 1] for row in rows[r.y + 1:r.bottom - 1]))
        msg = (f"Archive Personal? It leaves the home; its folder is not touched. "
               f"taskboard --board {path} brings it back.")
        # every character of it, in order: a path wider than the box breaks inside itself
        assert "".join(msg.split()) in "".join(flat.split())
        assert "y archive n / esc cancel ⇥ the buttons" in flat
        await _press(pilot, "enter")
        assert isinstance(app.screen, ConfirmModal)
        await _press(pilot, "n")
        assert isinstance(app.screen, BoardsHome)
        assert app.registry.get("main").archived is False
        await _press(pilot, "x", "y")
        assert any(n.startswith("Archived Personal") for n in _notes(app))
        reg = json.loads((home / "boards.json").read_text(encoding="utf-8"))
        assert next(e for e in reg["boards"] if e["id"] == "main")["archived"] is True
        await _press(pilot, "escape")
        task = app.selected_task
        assert task is not None
        await _press(pilot, "d")
        assert isinstance(app.screen, ConfirmModal)
        await _press(pilot, "y")
        assert app.board.task_by_id(task.id) is None
    # the move's confirmation, on a fresh app over the same fixture (qa QA-22; ux UX-2)
    import shutil
    shutil.rmtree(home)
    app = _round_app(home)
    async with app.run_test(size=size, notifications=True) as pilot:
        await pilot.pause()
        await _press(pilot, "escape", "P", "down", "m", "enter")
        assert type(app.screen).__name__ == "MoveConfirm", _notes(app)
        flat = _flat(await _screen(pilot, w, h))
        assert "y move" in flat and "n / esc cancel" in flat
        before = len(app.board.projects)
        await _press(pilot, "enter")
        assert type(app.screen).__name__ == "MoveConfirm"       # a stray enter moves nothing
        await _press(pilot, "y")
        assert type(app.screen).__name__ != "MoveConfirm"
        assert len(app.board.projects) == before - 1
        assert any(n.startswith("Moved ") for n in _notes(app)), _notes(app)


# --------------------------------------------------------------------------- #
# TC-2407 — the forms' `alt` keys and the inventory law (LLR-2407.1)
# --------------------------------------------------------------------------- #
def _forms(board):
    return [("TaskModal", lambda: modals.TaskModal(board), dict),
            ("ProjectModal", lambda: modals.ProjectModal(), dict),
            ("TemplateEditor", lambda: modals.TemplateEditor(), dict),
            ("ClockModal", lambda: modals.ClockModal("Madrid", "London"), dict),
            ("TextPrompt", lambda: modals.TextPrompt("Name", "kept"), str)]


@pytest.mark.parametrize("name", ["TaskModal", "ProjectModal", "TemplateEditor", "ClockModal",
                                  "TextPrompt"])
async def test_TC_2407_alt_s_does_what_save_does(home, name):
    """TC-2407: `alt+s` dismisses each form with what its Save button returns."""
    app = TaskboardApp(board_path=home / "board.json")
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        make, kind = next((m, k) for n, m, k in _forms(app.board) if n == name)
        by_key, by_button = [], []
        app.push_screen(make(), by_key.append)
        await pilot.pause()
        await _press(pilot, "alt+s")
        app.push_screen(make(), by_button.append)
        await pilot.pause()
        app.screen.query_one("#save", Button).press()     # the button itself, scrolled or not
        await pilot.pause()
        assert len(by_key) == 1 and isinstance(by_key[0], kind)
        strip = (lambda d: {k: v for k, v in d.items() if k != "id"}) if kind is dict else str
        assert strip(by_key[0]) == strip(by_button[0])


@pytest.mark.parametrize("name, key, field", [("TaskModal", "alt+t", "f-start"),
                                              ("TaskModal", "alt+d", "f-due"),
                                              ("ProjectModal", "alt+t", "f-start"),
                                              ("ProjectModal", "alt+d", "f-due")])
async def test_TC_2407_alt_t_and_alt_d_open_the_calendars(home, monkeypatch, name, key, field):
    """TC-2407: `alt+t` / `alt+d` open the start / due calendar, as the 📅 buttons."""
    asked = []
    monkeypatch.setattr(modals.DatePickerMixin, "_open_calendar",
                        lambda self, fid: asked.append(fid))
    app = TaskboardApp(board_path=home / "board.json")
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        make = next(m for n, m, _k in _forms(app.board) if n == name)
        app.push_screen(make())
        await pilot.pause()
        await _press(pilot, key)
        assert asked == [field]


async def test_TC_2407_alt_i_pastes_an_image(home, monkeypatch):
    """TC-2407: the editor's `alt+i` is its Paste image button."""
    monkeypatch.setattr(modals, "grab_clipboard_image", lambda: None)
    app = TaskboardApp(board_path=home / "board.json")
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.pause()
        app.push_screen(modals.TaskModal(app.board))
        await pilot.pause()
        await _press(pilot, "alt+i")
        assert "No image found in the clipboard." in _notes(app)


#: THE INVENTORY (D-6): every `ModalScreen` subclass of the package, and how each of
#: its buttons is reached by a direct key. A modal without buttons acts on keys alone
#: (its own BINDINGS; its key line or hint says them). A new modal must be added here.
INVENTORY: dict[str, dict[str, str]] = {
    "TaskModal": {"paste-img": "alt+i", "save": "alt+s", "cancel": "escape",
                  "cal-f-start": "alt+t", "cal-f-due": "alt+d"},
    "ProjectModal": {"save": "alt+s", "cancel": "escape", "cal-f-start": "alt+t",
                     "cal-f-due": "alt+d"},
    "TemplateEditor": {"save": "alt+s", "cancel": "escape"},
    "ClockModal": {"save": "alt+s", "cancel": "escape"},
    "TextPrompt": {"save": "alt+s", "cancel": "escape"},
    "ConfirmModal": {"yes": "y", "no": "n"},
    # no buttons: keys only
    "CalendarModal": {}, "EmojiPicker": {}, "ProjectPicker": {}, "LinkPicker": {},
    "TemplatePicker": {}, "MilestoneOffer": {}, "PresentHiddenPicker": {}, "GanttLinkMode": {},
    "TeamIdentityPicker": {}, "PhaseEditor": {}, "ImageViewer": {}, "TaskDetails": {},
    "HelpModal": {}, "StandupModal": {}, "CommandPalette": {}, "BoardForm": {},
    "MoveTarget": {}, "MoveConfirm": {}, "HelpScreen": {}, "PresentScreen": {},
    "PresentKeys": {},
}


def _package_modals() -> dict[str, type]:
    found = {}
    for mod in (modals, app_module):
        for name, obj in vars(mod).items():
            if (inspect.isclass(obj) and issubclass(obj, ModalScreen) and obj is not ModalScreen
                    and obj.__module__ == mod.__name__):
                found[name] = obj
    return found


def _bound(cls) -> set[str]:
    keys = set()
    for b in cls.BINDINGS:
        key = b.key if hasattr(b, "key") else b[0]
        keys.update(k.strip() for k in key.split(","))
    return keys


def test_TC_2406_the_move_confirms_on_y_never_on_enter():
    """TC-2406 (ux UX-2): `MoveConfirm` takes the confirmation standard — `y` yes,
    `n`/`esc` no, no `enter`."""
    bound = {}
    for b in modals.MoveConfirm.BINDINGS:
        for k in b.key.split(","):
            bound[k.strip()] = b.action
    assert bound.get("y") == "yes" and bound.get("n") == "no" and bound.get("escape") == "no"
    assert "enter" not in bound


def test_TC_2407_every_modal_is_in_the_inventory():
    """TC-2407: the law's table is the package's set of modals, both ways — a modal
    added without its row fails here; a modal whose source yields a Button has a
    row naming its buttons, and each named key is bound on it."""
    found = _package_modals()
    assert set(found) - set(INVENTORY) == set(), "add the new modal to INVENTORY"
    assert set(INVENTORY) - set(found) == set()
    for name, cls in found.items():
        has_buttons = "Button(" in inspect.getsource(cls)
        assert has_buttons is bool(INVENTORY[name]), name
        assert set(INVENTORY[name].values()) <= _bound(cls), name


@pytest.mark.parametrize("name", ["TaskModal", "ProjectModal", "TemplateEditor", "ClockModal",
                                  "TextPrompt", "ConfirmModal"])
async def test_TC_2407_every_button_has_its_key(home, name):
    """TC-2407: composed, a modal's buttons are exactly the inventory's, and its key
    line names every key but `esc`/`n` cancel's own (written `esc`)."""
    app = TaskboardApp(board_path=home / "board.json")
    async with app.run_test(size=(160, 45)) as pilot:
        await pilot.pause()
        make = dict((n, m) for n, m, _k in _forms(app.board))
        make["ConfirmModal"] = lambda: ConfirmModal("Delete 'x'?")
        app.push_screen(make[name]())
        await pilot.pause()
        ids = {b.id for b in app.screen.query(Button)}
        assert ids == set(INVENTORY[name])
        rows = (await _screen(pilot, 160, 45)).splitlines()
        # the key line is the painted row the modal's key-line widget sits on
        line = app.screen.query_one("#confirm-keys, .modal-keys, #task-keys")
        painted = rows[line.region.y]
        for key in INVENTORY[name].values():
            # cancel is `esc cancel` on every modal, the word kept (code review CR-1)
            shown = {"escape": "esc cancel", "n": "n / esc cancel"}.get(key, key)
            assert shown in painted, (name, key, painted)


# --------------------------------------------------------------------------- #
# AT-2407 — the forms by keys (US-2404)
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("size", [(118, 30), (80, 24)])
async def test_AT_2407_alt_s_saves_and_letters_type(home, size):
    """AT-2407 (US-2404): `a`, `Draft s`, `alt+s` saves a task titled `Draft s` (the
    `s` typed, never a save); `e`, `alt+d` opens its calendar; `p`, `Site`, `alt+s`
    saves a project; the editor's last row names every button's key."""
    w, h = size
    app = TaskboardApp(board_path=home / "board.json")
    async with app.run_test(size=size) as pilot:
        await pilot.pause()
        await _press(pilot, "a")
        assert isinstance(app.screen, modals.TaskModal)
        last = (await _screen(pilot, w, h)).splitlines()[h - 1]
        if (w, h) == (80, 24):
            # the key line's row costs the notes one row at most: 11 at `base_ref` (ux UX-3)
            assert app.screen.query_one("#f-notes").size.height >= 10
        for key in ("alt+s", "alt+i", "alt+t", "alt+d", "esc"):
            assert key in last, (key, last)
        if w >= 118:
            assert "alt+s save   alt+i paste image   alt+t start date   alt+d due date" in last
        await _press(pilot, *"Draft", "space", "s")
        assert isinstance(app.screen, modals.TaskModal)
        await _press(pilot, "alt+s")
        assert not isinstance(app.screen, modals.TaskModal)
        mine = [t for t in app.board.tasks if t.title == "Draft s"]
        assert len(mine) == 1
        assert app.selected_task_id == mine[0].id          # the new task is selected
        kept = (home / "board.json").read_bytes()
        await _press(pilot, "e", "alt+d")
        assert isinstance(app.screen, modals.CalendarModal)
        await _press(pilot, "escape", "escape")
        assert not isinstance(app.screen, ModalScreen)
        assert (home / "board.json").read_bytes() == kept       # cancelled: nothing written
        # the project form opens on its box (as shipped); `tab` reaches the name
        await _press(pilot, "p", "tab", *"Site", "alt+s")
        assert any(p.name == "Site" for p in app.board.projects)
        await _press(pilot, "c")
        assert isinstance(app.screen, modals.ClockModal)
        await _press(pilot, "alt+s")
        assert not isinstance(app.screen, ModalScreen) and "clock1" in app.board.settings
        await _press(pilot, "I", "enter")
        assert isinstance(app.screen, modals.TemplateEditor)
        await _press(pilot, *"Weekly", "tab", *"Kickoff", "alt+s")
        assert not isinstance(app.screen, ModalScreen)
        assert any(t.get("name") == "Weekly" for t in app.board.settings.get("templates", []))
