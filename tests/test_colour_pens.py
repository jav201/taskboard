"""Pens in the task editor and the live ink in its notes field (batch 2026-11-01-v3-incC,
Inc C, US-4201, HLR-4203 / HLR-4204, AT-4201).

Field report (the board's owner, `username_subject`): "switching colour should be as easy
as switching pens in a notebook". In the editor's notes `alt+1`..`alt+6` take a pen
(r o y g b v), what is typed goes into that pen's span, `alt+0` lifts it, and the notes
field itself shows the ink while typing (not only the preview). A pen must never corrupt
text already written, never fire outside the notes, and the ink must never cost the
editor: an exception in it shows plain text, it never crashes and loses an unsaved edit.

Drives the SHIPPED surface: a real `TaskboardApp` on a synthetic board under `tmp_path`,
the editor opened with `e`, keys pressed through the pilot — and, where the terminal's own
encoding matters (ARCH-1, ARCH-2), the bytes a legacy-encoding terminal sends (`ESC 5`)
fed through Textual's `XTermParser` and posted to the driver, so the key the app sees is
the key Windows Terminal produces (`Key("alt+5", "5")`, a printable character). Colours
are read from the rendered strips of the notes field (cells, not markup).

RED on base `0a8dfaa`: `alt+5` inserts nothing (pilot) or types `∞` (terminal), the Notes
label is the legacy text, the field paints no colour, and the names Inc C adds
(`ink_highlights`, `pen_label`, `_unshadow_alt_digits`, `colour_spans` in modals) are
absent — reached through `_need`, so each test fails on an assertion. GUARD that passes on
base by design: `test_P_M1_7_the_textual_internals_the_ink_rests_on_keep_their_shape`
(ruling P-M1-7: it fails when a Textual upgrade changes the private shape).
"""
from __future__ import annotations

import json
import statistics
import time

import pytest
from rich.cells import cell_len
from rich.style import Style
from textual import events
from textual._xterm_parser import XTermParser
from textual.geometry import Offset
from textual.widgets import Input, TextArea
from textual.widgets.text_area import TextAreaTheme

import taskboard.modals as modals                  # imported BEFORE any parser test (ARCH-1)
from taskboard import views
from taskboard.app import TaskboardApp
from taskboard.modals import TaskDetails, TaskModal
from taskboard.models import Board, Project, Task
from taskboard.views import HEX, highlight_segments

from test_colour_notes import DERIVED_SINGLE, ref_spans

SIZE = (118, 30)
CODES = "roygbv"
TONE = {"r": "over", "o": "orange", "y": "soon", "g": "green", "b": "blue", "v": "violet"}
NAME = {"r": "red", "o": "orange", "y": "yellow", "g": "green", "b": "blue", "v": "violet"}
BLUE, DIM = HEX["blue"], HEX["dim"]
NOTICE_PEN = "Pens write new text — use alt+c to recolour."
NOTICE_N4 = "That colour would change the text you see: nothing changed."


def _need(mod, name: str):
    obj = getattr(mod, name, None)
    if obj is None:
        pytest.fail(f"{mod.__name__}.{name} is missing: Inc C is not built here")
    return obj


def _pen(scr):
    """[Data: TaskModal.pen] — the index into PEN_CODES of the pen that is on, or None."""
    if not hasattr(scr, "pen"):
        pytest.fail("TaskModal.pen is missing: Inc C is not built here")
    return scr.pen


# --------------------------------------------------------------------------- #
# The app, the editor, the keys, the cells
# --------------------------------------------------------------------------- #
def _app(tmp_path, notes: str = "", raw_notes: str | None = None) -> TaskboardApp:
    b = Board.load(tmp_path / "board.json")
    b.projects.clear()
    b.tasks.clear()
    p = Project("Field notes", "sky")
    b.projects.append(p)
    b.tasks.append(Task("Write the multicolour note", p.id, "Doing", notes=notes))
    b.save()
    if raw_notes is not None:          # a board file holding a JSON escape no str can save
        path = tmp_path / "board.json"
        path.write_text(path.read_text(encoding="utf-8").replace("RAWNOTES", raw_notes),
                        encoding="utf-8")
    return TaskboardApp(board_path=str(tmp_path / "board.json"), team_sync_interval=1e9)


async def _editor(app, pilot, cursor=None):
    """Through the shipped surface: select the task, `e`, focus the notes, place the
    cursor (default: the end of the notes)."""
    await pilot.pause()
    app.selected_task_id = app.board.tasks[0].id
    await pilot.press("e")
    for _ in range(3):
        await pilot.pause()
    assert isinstance(app.screen, TaskModal), "`e` did not open the editor"
    scr = app.screen
    ta = scr.query_one("#f-notes", TextArea)
    ta.focus()
    ta.move_cursor(ta.document.end if cursor is None else cursor)
    for _ in range(2):
        await pilot.pause()
    return scr, ta


async def _type(pilot, s: str):
    await pilot.press(*s)


async def _terminal(app, pilot, *chunks: str):
    """What a legacy-encoding terminal sends (Windows Terminal answers no kitty query:
    evidence/wt-kitty-query.log), parsed by Textual's own XTermParser, posted to the
    driver as the terminal's events. Each chunk is flushed on its own (a lone ESC waits
    for the next byte)."""
    for chunk in chunks:
        parser = XTermParser()
        evs = [e for e in list(parser.feed(chunk)) + list(parser.feed(""))
               if isinstance(e, events.Key)]
        for ev in evs:
            ev.set_sender(app)
            app._driver.send_message(ev)
            await pilot.pause()
    await pilot.pause()


async def _post_key(app, pilot, key: str, char: str | None):
    ev = events.Key(key, char)
    ev.set_sender(app)
    app._driver.send_message(ev)
    for _ in range(2):
        await pilot.pause()


def _ids(app) -> set:
    return {n.identity for n in app._notifications}


def _new_notices(app, before: set) -> list[str]:
    return [str(n.message) for n in app._notifications if n.identity not in before]


def _cells(strip) -> list[tuple[str, str | None, str | None]]:
    """One (char, fg hex, bg hex) per terminal CELL of a strip; a wide glyph's second
    cell is ("", fg, bg)."""
    out = []
    for seg in strip:
        st = seg.style
        fg = st.color.triplet.hex.lower() if st and st.color and st.color.triplet else None
        bg = st.bgcolor.triplet.hex.lower() if st and st.bgcolor and st.bgcolor.triplet else None
        for ch in seg.text:
            out.append((ch, fg, bg))
            out += [("", fg, bg)] * (cell_len(ch) - 1)
    return out


def _ink(ta, row: int = 0) -> list[tuple[str, str | None, str | None]]:
    """The notes field's rendered cells of one document row (its widget line `row`)."""
    return _cells(ta.render_line(row))


def _painted_row(app, y: int) -> list[tuple[str, str | None, str | None]]:
    return _cells(app.screen._compositor.render_strips(app.screen.size)[y])


def _label_cells(app, scr):
    """The Notes label's VISIBLE cells: its painted row cut to the notes column (the
    label is the first section label above #f-notes)."""
    lab = scr.query_one("#task-edit").query(".task-sec").first()
    col = scr.query_one("#task-edit").content_region
    return _painted_row(app, lab.region.y)[col.x:col.x + col.width]


def _text(cells) -> str:
    return "".join(ch for ch, _f, _b in cells)


def _label_state(app, scr) -> str:
    """`none` when the label shows `pen: none`; else the name of the chip — a pen's name
    painted ON its tone (background), so a legacy word like `red` is never read as a
    chip; else `?<visible text>`."""
    cells = _label_cells(app, scr)
    vis = _text(cells)
    if "pen: none" in vis:
        return "none"
    for code in CODES:
        chip = f" {NAME[code]} "
        at = vis.find(chip)
        while at >= 0:
            if {bg for _c, _f, bg in cells[at:at + len(chip)]} == {HEX[TONE[code]]}:
                return NAME[code]
            at = vis.find(chip, at + 1)
    return f"?{vis!r}"


# --------------------------------------------------------------------------- #
# TC-4249 — the terminal's ESC <digit> reaches the app as alt+<digit> (LLR-4203.16)
# --------------------------------------------------------------------------- #
def _parse(data: str):
    p = XTermParser()
    return [(e.key, e.character) for e in list(p.feed(data)) + list(p.feed(""))
            if isinstance(e, events.Key)]


def test_TC_4249_esc_digit_parses_as_alt_digit_after_the_import():
    """TC-4249 (LLR-4203.16, ARCH-1). With `taskboard.modals` imported, XTermParser fed
    `ESC 5` / `ESC 0` / `ESC 1` gives `alt+5` / `alt+0` / `alt+1` with the digit as its
    character; `ESC 7` (not a pen) keeps its base glyph and `ESC s` stays `alt+s`.
    NC: the base Textual table → `infinity` / `º`: RED on base."""
    assert _parse("\x1b5") == [("alt+5", "5")]
    assert _parse("\x1b0") == [("alt+0", "0")]
    assert _parse("\x1b1") == [("alt+1", "1")]
    assert _parse("\x1b7") == [("pilcrow_sign", "¶")]
    assert _parse("\x1bs") == [("alt+s", "s")]


def test_TC_4249_the_unshadowing_is_idempotent_and_spares_foreign_values(monkeypatch):
    """TC-4249 (A-1, SEC-R2-1): a second call changes nothing and raises nothing; an entry
    whose value is no longer Textual 8.2.8's glyph is left alone (only the known glyphs
    `º ¡ ™ £ ¢ ∞ §` are removed)."""
    unshadow = _need(modals, "_unshadow_alt_digits")
    from textual import _ansi_sequences as seq
    table = seq.ANSI_SEQUENCES_KEYS
    before = dict(table)
    unshadow()
    assert dict(table) == before
    monkeypatch.setitem(table, "\x1b3", "custom")       # someone else's mapping
    monkeypatch.setitem(table, "\x1b4", "¢")            # the 8.2.8 glyph, back again
    unshadow()
    assert table.get("\x1b3") == "custom"
    assert "\x1b4" not in table
    assert all(f"\x1b{d}" in table for d in "789")


class _ReadOnlyTable(dict):
    """A table that refuses every write, and records that it was read."""
    reads = 0

    def _ro(self, *a, **k):
        raise TypeError("read-only table")
    pop = __delitem__ = __setitem__ = popitem = clear = update = setdefault = _ro

    def get(self, *a):
        type(self).reads += 1
        return super().get(*a)

    def __getitem__(self, k):
        type(self).reads += 1
        return super().__getitem__(k)

    def __contains__(self, k):
        type(self).reads += 1
        return super().__contains__(k)


def test_TC_4249_a_read_only_table_never_stops_the_app_starting(monkeypatch):
    """TC-4249 immutable-table arm (A-1, SEC-R2-1): if Textual's table refuses writes,
    `_unshadow_alt_digits` raises nothing (the app still starts; alt+digit then degrades
    to glyphs). The fake table is read (so the arm is not vacuous)."""
    unshadow = _need(modals, "_unshadow_alt_digits")
    from textual import _ansi_sequences as seq
    real = seq.ANSI_SEQUENCES_KEYS
    fake = _ReadOnlyTable({**real, "\x1b5": "∞", "\x1b0": "º"})
    _ReadOnlyTable.reads = 0
    monkeypatch.setattr(seq, "ANSI_SEQUENCES_KEYS", fake)
    for name, val in list(vars(modals).items()):        # a module-level alias of the table
        if val is real:
            monkeypatch.setattr(modals, name, fake)
    unshadow()                                          # must not raise
    assert _ReadOnlyTable.reads >= 1, "the function never read the table it should unshadow"
    assert fake["\x1b5"] == "∞"


# --------------------------------------------------------------------------- #
# TC-4230..TC-4238 — set, type, lift, switch, enter, leave (LLR-4203.1..8)
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("via", ["pilot", "terminal"])
async def test_TC_4230_alt_n_opens_a_spaced_pair_with_the_cursor_inside(tmp_path, via):
    """TC-4230 (LLR-4203.1): empty notes, `alt+5` → `::b::  ::`, cursor (0, 6), pen 4 —
    by the pilot key and by the terminal's `ESC 5` (the digit must not be typed).
    NC: insert without spaces → RED. RED on base: nothing inserted / `∞` typed."""
    app = _app(tmp_path, "")
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot)
        if via == "pilot":
            await pilot.press("alt+5")
        else:
            await _terminal(app, pilot, "\x1b5")
        assert ta.text == "::b::  ::"
        assert ta.cursor_location == (0, 6)
        assert _pen(scr) == 4


async def test_TC_4231_typing_under_a_pen_stays_inside_its_span(tmp_path):
    """TC-4231 (LLR-4203.2): `alt+5`, `abc` → `::b:: abc ::`, tokenised `[("abc","blue")]`,
    the pen still on at the inner end. NC: cursor placed after the closer → RED."""
    app = _app(tmp_path, "")
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot)
        await pilot.press("alt+5")
        await _type(pilot, "abc")
        assert ta.text == "::b:: abc ::"
        assert highlight_segments(ta.text) == [("abc", "blue")]
        assert ta.cursor_location == (0, 9) and _pen(scr) == 4


async def test_TC_4232_alt_0_moves_past_the_closer(tmp_path):
    """TC-4232 (LLR-4203.3): `alt+5 abc alt+0 d` → `::b:: abc ::d`, `d` plain.
    NC: alt+0 ignored → `d` lands inside."""
    app = _app(tmp_path, "")
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot)
        await pilot.press("alt+5", *"abc", "alt+0", "d")
        assert ta.text == "::b:: abc ::d"
        assert highlight_segments(ta.text) == [("abc", "blue"), ("d", "mut")]


async def test_TC_4233_alt_0_turns_the_pen_off_and_the_chip_says_so(tmp_path):
    """TC-4233 (LLR-4203.4): before `alt+0` the label's chip names the pen (`blue`); after
    it the pen is None and the label shows `pen: none`. NC: state not reset → RED."""
    app = _app(tmp_path, "")
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot)
        assert _label_state(app, scr) == "none"
        await pilot.press("alt+5", *"abc")
        assert _label_state(app, scr) == "blue"
        await pilot.press("alt+0")
        await pilot.pause()
        assert _pen(scr) is None
        assert _label_state(app, scr) == "none"


async def test_TC_4234_another_pen_closes_the_first_and_opens_after_it(tmp_path):
    """TC-4234 (LLR-4203.5): `alt+1 ab alt+5 x` → `::r:: ab ::::b:: x ::`; segments red
    `ab`, blue `x`; the rendered text `abx` is what was typed. NC: m opened inside n →
    RED."""
    app = _app(tmp_path, "")
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot)
        await pilot.press("alt+1", *"ab", "alt+5", "x")
        assert ta.text == "::r:: ab ::::b:: x ::"
        assert highlight_segments(ta.text) == [("ab", "over"), ("x", "blue")]
        assert "".join(s for s, _ in highlight_segments(ta.text)) == "abx"
        assert _pen(scr) == 4


@pytest.mark.parametrize("notes, keys, want", [
    ("x", ["alt+2", "alt+0"], "x"),                       # lift with alt+0
    ("", ["alt+2", "alt+5", "y"], "::b:: y ::"),           # lift with another pen
])
async def test_TC_4235_lifting_an_empty_pen_removes_its_span(tmp_path, notes, keys, want):
    """TC-4235 (LLR-4203.6; graph-interfaces TC-4259): a pen lifted while its span is
    empty leaves no `::o::  ::` behind, 2/2. NC: keep the empty span → RED."""
    app = _app(tmp_path, notes)
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot)
        await pilot.press(*keys)
        assert ta.text == want
        if want == "x":
            assert ta.cursor_location == (0, 1) and _pen(scr) is None


async def test_TC_4236_enter_under_a_pen_continues_the_pen_on_the_next_line(tmp_path):
    """TC-4236 (LLR-4203.7): `alt+5 ab enter cd` → `::b:: ab ::\\n::b:: cd ::`, both
    lines blue. NC: plain newline → line 2 shows `cd ::` literally (RED)."""
    app = _app(tmp_path, "")
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot)
        await pilot.press("alt+5", *"ab", "enter")
        assert ta.text == "::b:: ab ::\n::b::  ::"
        assert ta.cursor_location == (1, 6) and _pen(scr) == 4
        await _type(pilot, "cd")
        assert ta.text == "::b:: ab ::\n::b:: cd ::"
        assert [highlight_segments(ln) for ln in ta.text.split("\n")] == [
            [("ab", "blue")], [("cd", "blue")]]


async def test_TC_4236_enter_mid_span_splits_it_in_two_spans_of_the_same_pen(tmp_path):
    """TC-4236 (LLR-4203.7): with the cursor inside `abcd` (after `ab`), `enter` carries
    `cd` into the same pen's span on the next line."""
    app = _app(tmp_path, "")
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot)
        await pilot.press("alt+5", *"abcd", "left", "left")
        assert _pen(scr) == 4
        await pilot.press("enter")
        assert ta.text == "::b:: ab ::\n::b:: cd ::"
        assert ta.cursor_location == (1, 6)


async def test_TC_4236_leaving_the_fresh_span_after_enter_removes_it(tmp_path):
    """TC-4236 + LLR-4203.14 (ARCH-8): `enter` then `home` at once → the empty span the
    enter opened is removed; the line break stays, the pen is off."""
    app = _app(tmp_path, "")
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot)
        await pilot.press("alt+5", *"ab")
        await pilot.press("enter", "home")
        await pilot.pause()
        assert ta.text == "::b:: ab ::\n"
        assert ta.cursor_location == (1, 0) and _pen(scr) is None


async def test_TC_4237_enter_with_the_pen_off_is_a_plain_new_line(tmp_path):
    """TC-4237 (check_action's pen_enter arm, ARCH-8): once the cursor has left the pen's
    span (`end`), `enter` is the field's own new line, no pen pair."""
    app = _app(tmp_path, "")
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot)
        await pilot.press("alt+5", *"ab", "end", "enter")
        assert ta.text == "::b:: ab ::\n"
        assert _pen(scr) is None


@pytest.mark.parametrize("keys, cursor, pen", [
    (["right"], (0, 9), None),                    # onto the closer's space
    (["right", "right", "right"], (0, 11), None),  # past the closer
    (["left"], (0, 7), 4),                        # still inside: the pen stays
    (["home"], (0, 0), None),
    (["end"], (0, 11), None),
    (["shift+left"], None, None),                 # a selection
])
async def test_TC_4238_leaving_the_span_turns_the_pen_off(tmp_path, keys, cursor, pen):
    """TC-4238 (LLR-4203.8): after `alt+5 ab`, a cursor move out of the span (arrows,
    home/end, a selection) turns the pen off and the label says `pen: none`; a move
    inside keeps it. NC: the pen survives leaving → RED."""
    app = _app(tmp_path, "")
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot)
        await pilot.press("alt+5", *"ab")
        await pilot.press(*keys)
        await pilot.pause()
        assert ta.text == "::b:: ab ::"
        if cursor is not None:
            assert ta.cursor_location == cursor
        assert _pen(scr) == pen
        assert _label_state(app, scr) == ("none" if pen is None else "blue")


async def test_TC_4238_a_click_before_the_span_turns_the_pen_off(tmp_path):
    """TC-4238 (LLR-4203.8, the click limb): a mouse click on the field's first cell."""
    app = _app(tmp_path, "")
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot)
        await pilot.press("alt+5", *"ab")
        cr = ta.content_region
        await pilot.click("#f-notes", offset=Offset(cr.x - ta.region.x, cr.y - ta.region.y))
        await pilot.pause()
        assert ta.cursor_location == (0, 0)
        assert ta.text == "::b:: ab ::"
        assert _pen(scr) is None


# --------------------------------------------------------------------------- #
# TC-4239 — the Notes label (LLR-4203.9, LLR-4202.10)
# --------------------------------------------------------------------------- #
STATES = [None, 0, 1, 2, 3, 4, 5]


@pytest.mark.parametrize("size", [(118, 30), (80, 24)], ids=lambda s: f"{s[0]}x{s[1]}")
@pytest.mark.parametrize("state", STATES, ids=lambda s: "none" if s is None else CODES[s])
async def test_TC_4239_the_label_shows_the_pen_and_every_key_unclipped(tmp_path, size, state):
    """TC-4239 (LLR-4203.9, LLR-4202.10): in each of the 7 pen states, at 118x30 and
    80x24, the label's VISIBLE cells hold the state (`pen: none`, or a chip naming the pen
    on its tone), the keys `1`..`6` each in its tone, `0 off` and `alt+c` — the whole
    label from `Notes` to `alt+c`, 0 clipped glyphs (14/14). NC: base label → RED."""
    app = _app(tmp_path, "")
    async with app.run_test(size=size) as pilot:
        scr, ta = await _editor(app, pilot)
        if state is not None:
            await pilot.press(f"alt+{state + 1}")
            await pilot.pause()
        cells = _label_cells(app, scr)
        vis = _text(cells)
        body = vis.strip()
        assert body.startswith("Notes") and body.endswith("alt+c"), vis
        for token in ("alt+123456", "0 off", "alt+c"):
            assert token in vis, (token, vis)
        if state is None:
            assert "pen: none" in vis, vis
        else:
            code = CODES[state]
            chip = f" {NAME[code]} "
            assert chip in vis, vis
            at = vis.index(chip)
            assert {bg for _c, _f, bg in cells[at:at + len(chip)]} == {HEX[TONE[code]]}
        k = vis.index("alt+123456") + 4
        assert [(ch, fg) for ch, fg, _b in cells[k:k + 6]] == [
            (str(i + 1), HEX[TONE[code]]) for i, code in enumerate(CODES)]


def test_TC_4239_every_label_form_fits_the_narrow_column():
    """TC-4239 (P-M1-6, ARCH-7): one label form, <= 38 cells in every pen state, so it
    fits the 39-cell notes column at 80x24 with a cell to spare; Text pieces, not markup."""
    pen_label = _need(modals, "pen_label")
    for state in STATES:
        label = pen_label(state)
        assert hasattr(label, "cell_len"), "the label must be Text pieces (C-17)"
        assert label.cell_len <= 38, (state, label.plain)


# --------------------------------------------------------------------------- #
# TC-4240 — pens act only in the notes (LLR-4203.10, ARCH-2)
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("key, char", [("alt+5", "5"), ("alt+0", "0")])
async def test_TC_4240_a_pen_key_outside_the_notes_changes_no_field(tmp_path, key, char):
    """TC-4240 (LLR-4203.10, ARCH-2): focus on the title (`T`), notes `n`; the terminal's
    `Key("alt+5", "5")` / `Key("alt+0", "0")` — a printable event — changes no field:
    title and notes byte-equal, no pen, no notice. NC: a denied binding lets the Input
    type the digit (`T5`) → RED; RED on base (no binding: `T5`)."""
    app = _app(tmp_path, "n")
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot)
        title = scr.query_one("#f-title", Input)
        title.value = "T"
        title.focus()
        title.cursor_position = 1
        await pilot.pause()
        before = _ids(app)
        await _post_key(app, pilot, key, char)
        assert title.value == "T"
        assert ta.text == "n"
        assert _pen(scr) is None
        assert _new_notices(app, before) == []


# --------------------------------------------------------------------------- #
# TC-4241 — save drops an empty pen span (LLR-4203.11)
# --------------------------------------------------------------------------- #
async def test_TC_4241_saving_with_an_empty_pen_saves_no_empty_span(tmp_path):
    """TC-4241 (LLR-4203.11): notes `x`, `alt+3`, `alt+s` → the saved notes are `x`, on
    the board and in the file. NC: `x::y::  ::` saved (strip keeps it) → RED."""
    app = _app(tmp_path, "x")
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot)
        await pilot.press("alt+3")
        assert ta.text == "x::y::  ::"
        await pilot.press("alt+s")
        for _ in range(3):
            await pilot.pause()
        assert not isinstance(app.screen, TaskModal)
        assert app.board.tasks[0].notes == "x"
    saved = json.loads((tmp_path / "board.json").read_text(encoding="utf-8"))
    assert [t["notes"] for t in saved["tasks"]] == ["x"]


# --------------------------------------------------------------------------- #
# TC-4248 / TC-4255 — the same pen again changes nothing (LLR-4203.15)
# --------------------------------------------------------------------------- #
async def test_TC_4255_the_same_pen_key_again_changes_nothing(tmp_path):
    """TC-4248 / TC-4255 (LLR-4203.15, P-M1-8): `alt+5 ab alt+5` → `::b:: ab ::`, cursor
    (0, 8), pen 4, no notice. NC: a second pair → RED."""
    app = _app(tmp_path, "")
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot)
        await pilot.press("alt+5", *"ab")
        before = _ids(app)
        await pilot.press("alt+5")
        assert ta.text == "::b:: ab ::"
        assert ta.cursor_location == (0, 8) and _pen(scr) == 4
        assert _new_notices(app, before) == []


# --------------------------------------------------------------------------- #
# TC-4250 — a typed `::` closes the pen's span (P-M1-5, ARCH-13)
# --------------------------------------------------------------------------- #
async def test_TC_4250_typing_a_double_colon_under_a_pen_closes_its_span(tmp_path):
    """TC-4250 (LLR-4203.2's stated exception, P-M1-5): pen `b`, typing `std::` gives
    `::b:: std:: ::` — `std` blue, the pen off (the cursor is past the new closer)."""
    app = _app(tmp_path, "")
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot)
        await pilot.press("alt+5", *"std::")
        await pilot.pause()
        assert ta.text == "::b:: std:: ::"
        assert highlight_segments(ta.text)[0] == ("std", "blue")
        assert ta.cursor_location == (0, 11) and _pen(scr) is None


async def test_TC_4250_two_colons_first_thing_in_a_fresh_pen_leave_only_the_old_closer(tmp_path):
    """TC-4250 (ARCH-13, pinned; re-pinned at E5 after SR-2): pen `b` on `::b::  ::`,
    typing `:` `:` makes the typed `::` the closer of an empty span. Since SR-2's guard
    (a remembered empty span is removed only while its row reads exactly as recorded) the
    edited row no longer matches, so nothing is deleted: the text is `::b:: :: ::`, the
    VISIBLE text is still ` ::` (as at the first pin), the pen off."""
    app = _app(tmp_path, "")
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot)
        await pilot.press("alt+5", ":", ":")
        await pilot.pause()
        assert ta.text == "::b:: :: ::"
        assert "".join(s for s, _ in views.highlight_segments(ta.text)) == " ::"
        assert _pen(scr) is None


# --------------------------------------------------------------------------- #
# TC-4252 / TC-4254 — a pen never rewrites text already written (LLR-4203.12/13/17)
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("notes, cursor, key, notice", [
    ("::r:: ab ::", (0, 7), "alt+5", NOTICE_PEN),      # inside a colour span (LLR-4203.12)
    ("::b:: abc ::", (0, 7), "alt+5", NOTICE_PEN),     # same code: no "continue in span"
    ("==late==", (0, 1), "alt+5", NOTICE_PEN),         # inside a legacy span's opener
    ("b:: x", (0, 0), "alt+1", NOTICE_N4),             # `b::` would become an opener (LLR-4203.17)
    ("C::b", (0, 4), "alt+1", NOTICE_N4),              # would show `Cr  ::`
    ("note y::", (0, 5), "alt+1", NOTICE_N4),          # the pair's `::` + `y::` would open
])
async def test_TC_4252_a_pen_refuses_where_it_would_change_written_text(
        tmp_path, notes, cursor, key, notice):
    """TC-4252 (LLR-4203.12, LLR-4203.17; P-M1-3, SEC-2): with no pen on, `alt+<n>` inside
    a span, or where the pair would fuse with the neighbouring text, inserts nothing,
    keeps the pen off and shows ONE notice. NC: insert anyway → RED. RED on base: no
    notice."""
    app = _app(tmp_path, notes)
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot, cursor)
        before = _ids(app)
        await pilot.press(key)
        await pilot.pause()
        assert ta.text == notes
        assert ta.cursor_location == cursor
        assert _new_notices(app, before) == [notice]
        assert _pen(scr) is None


async def test_TC_4252_at_a_spans_end_the_cursor_is_outside_it(tmp_path):
    """TC-4252: `::r:: ab ::` with the cursor at col 11 (= end) is outside the span: the
    pen opens after it, no notice."""
    app = _app(tmp_path, "::r:: ab ::")
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot, (0, 11))
        before = _ids(app)
        await pilot.press("alt+5")
        assert ta.text == "::r:: ab ::::b::  ::"
        assert ta.cursor_location == (0, 17) and _pen(scr) == 4
        assert _new_notices(app, before) == []


@pytest.mark.parametrize("key, notices", [("alt+5", [NOTICE_PEN]), ("alt+0", [])])
async def test_TC_4254_a_pen_key_over_a_selection_inserts_nothing(tmp_path, key, notices):
    """TC-4254 (LLR-4203.13): `plan` selected, `alt+5` → byte-equal, the selection kept,
    one notice; `alt+0` with no pen on → nothing, no notice. NC: replace the selection →
    RED."""
    from textual.widgets.text_area import Selection
    app = _app(tmp_path, "the plan works")
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot)
        ta.selection = Selection((0, 4), (0, 8))
        await pilot.pause()
        before = _ids(app)
        await pilot.press(key)
        await pilot.pause()
        assert ta.text == "the plan works"
        assert ta.selection == Selection((0, 4), (0, 8))
        assert _new_notices(app, before) == notices
        assert _pen(scr) is None


# --------------------------------------------------------------------------- #
# TC-4256 / TC-4257 — leaving an empty pen span removes it (LLR-4203.14, SEC-4)
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("notes, start, keys, want, cursor", [
    ("x", (0, 1), ["alt+3", "home"], "x", (0, 0)),           # before the span
    ("", None, ["alt+3", "right"], "", (0, 0)),              # onto the closer's space
    ("xz", (0, 1), ["alt+3", "end"], "xz", (0, 2)),          # after it, same row
    ("a\n", (1, 0), ["alt+3", "up"], "a\n", (0, 1)),         # onto another row
])
async def test_TC_4256_leaving_an_empty_pen_span_removes_it(tmp_path, notes, start, keys,
                                                             want, cursor):
    """TC-4256 / TC-4257 (LLR-4203.14, P-M1-4): `alt+3` then a move out of the still
    empty span leaves no `::y::  ::` and puts the cursor where the text it pointed at
    now is. NC: `x::y::  ::` left → RED."""
    app = _app(tmp_path, notes)
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot, start)
        await pilot.press(keys[0])
        assert "::y::  ::" in ta.text
        await pilot.press(*keys[1:])
        await pilot.pause()
        assert ta.text == want
        assert ta.cursor_location == cursor
        assert _pen(scr) is None


async def test_TC_4257_only_the_pens_own_empty_span_is_removed(tmp_path):
    """TC-4257 (SEC-4): an older empty `::y::  ::` already in the notes is not touched
    when a new pen's empty span at col 9 is left; a non-empty span is kept as typed."""
    app = _app(tmp_path, "::y::  ::")
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot, (0, 9))
        await pilot.press("alt+3")
        assert ta.text == "::y::  ::::y::  ::"
        await pilot.press("home")
        await pilot.pause()
        assert ta.text == "::y::  ::"
        assert ta.cursor_location == (0, 0) and _pen(scr) is None


async def test_TC_4257_leaving_a_span_with_text_keeps_it(tmp_path):
    app = _app(tmp_path, "")
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot)
        await pilot.press("alt+3", *"ab", "home")
        await pilot.pause()
        assert ta.text == "::y:: ab ::" and _pen(scr) is None


# --------------------------------------------------------------------------- #
# TC-4258 — alt+0 on a span with no closer writes one (ARCH-10)
# --------------------------------------------------------------------------- #
async def test_TC_4258_lifting_a_span_with_no_closer_writes_the_closer(tmp_path):
    """TC-4258 (LLR-4203.3, ARCH-10): pen on `::b:: ab ::` at (0, 8), `delete` ×3 →
    `::b:: ab`; `alt+0` writes ` ::` and puts the cursor after it, so the next `d` is
    plain: `::b:: ab ::d`."""
    app = _app(tmp_path, "")
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot)
        await pilot.press("alt+5", *"ab", "delete", "delete", "delete")
        assert ta.text == "::b:: ab" and _pen(scr) == 4
        await pilot.press("alt+0")
        assert ta.text == "::b:: ab ::" and ta.cursor_location == (0, 11)
        await pilot.press("d")
        assert highlight_segments(ta.text) == [("ab", "blue"), ("d", "mut")]


# --------------------------------------------------------------------------- #
# TC-4242..TC-4247, TC-4251 — the live ink (HLR-4204)
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("notes, cols, tone", [
    ("a ::b:: x :: c", [8], "blue"),
    ("x ==late== y", [4, 5, 6, 7], "soon"),          # legacy spans are inked too (P-M1-1)
])
async def test_TC_4242_the_field_paints_the_inner_text_in_its_tone(tmp_path, notes, cols, tone):
    """TC-4242 (LLR-4204.1): the rendered cell of `x` in `a ::b:: x :: c` has fg
    `#60a5fa`; a legacy span's text its tone. NC: no highlight map → RED (RED on base)."""
    app = _app(tmp_path, notes)
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot, (0, 0))
        cells = _ink(ta)
        assert [cells[c][1] for c in cols] == [HEX[tone]] * len(cols), cells[:14]


async def test_TC_4243_the_markers_are_painted_dim(tmp_path):
    """TC-4243 (LLR-4204.2): the cells of `::b::` and the closing `::` (cols 2–6, 10–11)
    have fg `#5b6675`, 7/7. NC: markers in the tone → RED."""
    app = _app(tmp_path, "a ::b:: x :: c")
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot, (0, 0))
        cells = _ink(ta)
        assert [cells[c][1] for c in (2, 3, 4, 5, 6, 10, 11)] == [DIM] * 7, cells[:14]


async def test_TC_4244_a_typed_character_is_inked_before_the_next_paint(tmp_path):
    """TC-4244 (LLR-4204.3): `y` typed into an open span is the tone after one pause.
    NC: the map built only on mount → RED."""
    app = _app(tmp_path, "::b:: x ::")
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot, (0, 7))
        await pilot.press("y")
        await pilot.pause()
        assert ta.text == "::b:: xy ::"
        assert _ink(ta)[7][:2] == ("y", BLUE)


def _byte(line: str, i: int) -> int:
    return len(line[:i].encode("utf-8", "surrogatepass"))


def _expected_ink(line: str) -> list[tuple[int, int, str]]:
    """The highlight map the requirements imply for one line, in UTF-8 byte offsets,
    from the REFERENCE scanner: markers `pen.mark`, inner text `pen.<tone>`, empty ranges
    skipped (an end of 0 would read as "to the line end")."""
    out = []
    for s, a, b, e, tone, _code in ref_spans(line):
        for x, y, name in ((s, a, "pen.mark"), (a, b, f"pen.{tone}"), (b, e, "pen.mark")):
            if y > x:
                out.append((_byte(line, x), _byte(line, y), name))
    return out


def test_TC_4245_the_ink_colours_exactly_the_tokenisers_ranges():
    """TC-4245 (LLR-4204.4): over the single-line derived set of LLR-4201.9 (7 380
    inputs), the ink's ranges equal the reference scanner's ranges for 100 %; and the
    `pen.<tone>` ranges decoded back are the non-empty, non-`mut` segments of
    `highlight_segments`. NC: a second regex that ignores LLR-4201.6 → RED."""
    ink_highlights = _need(modals, "ink_highlights")
    assert len(DERIVED_SINGLE) == 7380
    wrong = []
    for line in DERIVED_SINGLE:
        got = sorted(ink_highlights([line]).get(0, []))
        if got != sorted(_expected_ink(line)):
            wrong.append((line, got, _expected_ink(line)))
            continue
        raw = line.encode("utf-8")
        toned = [raw[x:y].decode("utf-8") for x, y, n in sorted(got) if n != "pen.mark"]
        segs = [s for s, tone in highlight_segments(line) if tone != "mut" and s]
        if toned != segs:
            wrong.append((line, toned, segs))
    assert not wrong, wrong[:5]


def test_TC_4245_rows_without_a_span_have_no_ink_and_an_open_span_no_closer_range():
    """TC-4245 (graph examples): `::r:: open` → (0,6,mark), (6,10,over) — no empty closer
    range; `["std::vector", "==late=="]` → row 1 only."""
    ink_highlights = _need(modals, "ink_highlights")
    assert sorted(ink_highlights(["::r:: open"])[0]) == [(0, 6, "pen.mark"), (6, 10, "pen.over")]
    hl = ink_highlights(["std::vector", "==late=="])
    assert 0 not in hl or hl[0] == []
    assert sorted(hl[1]) == [(0, 2, "pen.mark"), (2, 6, "pen.soon"), (6, 8, "pen.mark")]


def test_TC_4246_ink_offsets_are_utf8_bytes_even_for_a_lone_surrogate():
    """TC-4246 (LLR-4204.5, LLR-4204.9, SEC-6): `é` and `☕` take 2 and 3 bytes; a lone
    surrogate counts its 3 bytes and raises nothing. NC: str offsets used as bytes → RED;
    a strict encode → UnicodeEncodeError (RED)."""
    ink_highlights = _need(modals, "ink_highlights")
    assert sorted(ink_highlights(["é ::b:: café ☕ ::"])[0]) == [
        (3, 9, "pen.mark"), (9, 18, "pen.blue"), (18, 21, "pen.mark")]
    assert sorted(ink_highlights(["\ud800 ::b:: x ::"])[0]) == [
        (4, 10, "pen.mark"), (10, 11, "pen.blue"), (11, 14, "pen.mark")]


@pytest.mark.parametrize("unit", ["::b:: x ::", "::b:: é ::"])
def test_TC_4246_the_ink_is_built_in_linear_time(unit):
    """TC-4246 (LLR-4204.7, SEC-1): 100 000 chars with 10 000 spans build in <= 250 ms and
    t(100k)/t(10k) <= 20 (median of 3), and all 10 000 spans are inked. Since LLR-4204.10
    (E5, SR-1) a line longer than 2 000 chars gets no ink, so the 100 000 chars are 50
    lines of exactly 2 000 (each still inked) instead of one line. NC: per-offset prefix
    re-encode (1 103 ms) → RED."""
    ink_highlights = _need(modals, "ink_highlights")
    line = unit * 200
    assert len(line) == 2000
    big, small = [line] * 50, [line] * 5

    def med(arg):
        ts = []
        for _ in range(3):
            t0 = time.perf_counter()
            ink_highlights(arg)
            ts.append(time.perf_counter() - t0)
        return statistics.median(ts)
    assert sum(1 for row in ink_highlights(big).values() for *_r, n in row
               if n == "pen.blue") == 10_000
    t_big, t_small = med(big), med(small)
    assert t_big <= 0.250, f"{t_big * 1000:.1f} ms"
    assert t_big / max(t_small, 1e-6) <= 20, f"ratio {t_big / max(t_small, 1e-6):.1f}"


async def test_TC_4246_non_ascii_text_is_inked_on_exactly_its_cells(tmp_path):
    """TC-4246 (LLR-4204.5): `é ::b:: café ☕ ::` — the cells of `café ☕` (8..14, the cup
    filling 13 and 14) are blue, the `é` at col 0 is not."""
    app = _app(tmp_path, "é ::b:: café ☕ ::")
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot)                 # cursor at the end (0, 17)
        cells = _ink(ta)
        assert [fg for _c, fg, _b in cells[8:15]] == [BLUE] * 7, cells[:18]
        assert cells[0][1] != BLUE


async def test_TC_4246_a_lone_surrogate_opens_and_types_without_ink(tmp_path):
    """TC-4246 (LLR-4204.9 as amended, R1-1): notes holding a lone surrogate (a board file
    with the JSON escape `\\ud800`) → the editor opens, typing `y` changes the text, no
    ink (the map is empty); and once the surrogate is deleted the field inks again
    (LLR-4204.1 holds for the document it now holds) — the arm that is RED on base."""
    app = _app(tmp_path, "RAWNOTES ::b:: x ::", raw_notes="\\ud800")
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot)
        assert ta.text == "\ud800 ::b:: x ::"
        assert not any(ta._highlights.values())
        await pilot.press("y")
        assert ta.text == "\ud800 ::b:: x ::y"
        ta.move_cursor((0, 0))
        await pilot.press("delete", "delete")
        await pilot.pause()
        assert ta.text == "::b:: x ::y"
        assert _ink(ta)[6][:2] == ("x", BLUE)
        assert isinstance(app.screen, TaskModal)


async def test_TC_4247_the_ink_never_touches_another_text_area(tmp_path):
    """TC-4247 (LLR-4204.6): after the editor mounts, the URLs field's theme holds 0
    `pen.` styles and paints `::b:: x ::` uncoloured; Textual's built-in `css` theme is
    unchanged (same keys, 0 `pen.`), and the notes field's theme is its own (`is not` the
    built-in dict) holding `pen.blue` and `pen.mark`. NC: mutate the shared theme → RED.
    RED on base: the notes field shares the built-in dict."""
    css = TextAreaTheme.get_builtin_theme("css")
    keys_before = set(css.syntax_styles)
    app = _app(tmp_path, "a ::b:: x :: c")
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot)
        urls = scr.query_one("#f-urls", TextArea)
        assert type(urls) is TextArea and type(scr.query_one("#f-images", TextArea)) is TextArea
        urls.text = "::b:: x ::"
        await pilot.pause()
        assert not [k for k in urls._theme.syntax_styles if k.startswith("pen.")]
        assert BLUE not in {fg for _c, fg, _b in _cells(urls.render_line(0))}
        assert set(css.syntax_styles) == keys_before
        assert not [k for k in css.syntax_styles if k.startswith("pen.")]
        assert ta._theme.syntax_styles is not css.syntax_styles
        assert {"pen.blue", "pen.mark"} <= set(ta._theme.syntax_styles)


async def test_TC_4251_an_ink_that_raises_leaves_the_editor_working(tmp_path, monkeypatch):
    """TC-4251 (LLR-4204.8, SEC-3): with `taskboard.modals.colour_spans` (the ink's
    scanner) made to raise, the editor opens on `::b:: x ::`, shows it uncoloured, takes
    typing and saves: 0 uncaught exceptions (an uncaught one ends `run_test` with it).
    NC: no fallback → the editor crashes, RED. RED on base: the name is absent."""
    _need(modals, "colour_spans")

    def boom(_text):
        raise RuntimeError("ink failure (test)")
    monkeypatch.setattr(modals, "colour_spans", boom)
    app = _app(tmp_path, "::b:: x ::")
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot)
        assert ta.text == "::b:: x ::"
        assert BLUE not in {fg for _c, fg, _b in _ink(ta)}
        await pilot.press("y")
        assert ta.text == "::b:: x ::y"
        await pilot.press("alt+s")
        for _ in range(3):
            await pilot.pause()
        assert not isinstance(app.screen, TaskModal)
    assert app.board.tasks[0].notes == "::b:: x ::y"


async def test_P_M1_7_the_textual_internals_the_ink_rests_on_keep_their_shape(tmp_path):
    """Ruling P-M1-7 — GUARD, passes on base by design (Textual 8.2.8). The ink overrides
    `TextArea._build_highlight_map`, fills `_highlights` (row → [(start byte, end byte,
    name)]) and clears `_line_cache`; `_render_line` paints a name through the theme's
    `syntax_styles`. RED when a Textual upgrade renames or reshapes any of them."""
    assert callable(getattr(TextArea, "_build_highlight_map", None))
    app = _app(tmp_path, "abc def")
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot, (0, 0))
        urls = scr.query_one("#f-urls", TextArea)
        urls.text = "abc def"
        await pilot.pause()
        assert hasattr(urls, "_line_cache") and callable(urls._line_cache.clear)
        assert isinstance(urls._highlights[0], list)
        urls.register_theme(TextAreaTheme(name="probe", syntax_styles={
            "probe.x": Style(color="#123456")}))
        urls.theme = "probe"
        urls._line_cache.clear()
        urls._highlights[0].append((4, 7, "probe.x"))
        cells = _cells(urls.render_line(0))
        assert [fg for _c, fg, _b in cells[4:7]] == ["#123456"] * 3
        assert cells[0][1] != "#123456"


# --------------------------------------------------------------------------- #
# AT-4201 — pens, end to end, from the terminal's bytes to the details screen
# --------------------------------------------------------------------------- #
async def test_AT_4201_a_pen_written_note_is_saved_and_shown_blue(tmp_path):
    """AT-4201 (HLR-4203, HLR-4204, US-4201). Open the task with `e`, reach the notes with
    `tab`, then the bytes Windows Terminal sends: `ESC 5`, `ask`, `ESC 0`, ` now`,
    `ESC s` (alt+s). The saved board holds `::b:: ask :: now`; the details screen
    (`enter`, the app's binding for TaskDetails) shows `ask` in `#60a5fa` and ` now` not
    blue; the editor's field showed `ask` blue while it was open. RED on base: the terminal's
    `ESC 5` types `∞`."""
    app = _app(tmp_path, "")
    async with app.run_test(size=SIZE) as pilot:
        await pilot.pause()
        app.selected_task_id = app.board.tasks[0].id
        await pilot.press("e")
        for _ in range(3):
            await pilot.pause()
        scr = app.screen
        assert isinstance(scr, TaskModal)
        for _ in range(25):
            if app.focused is not None and app.focused.id == "f-notes":
                break
            await pilot.press("tab")
        ta = scr.query_one("#f-notes", TextArea)
        assert app.focused is ta
        await _terminal(app, pilot, "\x1b5", "a", "s", "k")
        assert [fg for _c, fg, _b in _ink(ta)[6:9]] == [BLUE] * 3
        await _terminal(app, pilot, "\x1b0", " ", "n", "o", "w")
        assert ta.text == "::b:: ask :: now"
        await _terminal(app, pilot, "\x1bs")
        for _ in range(3):
            await pilot.pause()
        assert not isinstance(app.screen, TaskModal)
        await _terminal(app, pilot, "\r")
        for _ in range(3):
            await pilot.pause()
        assert isinstance(app.screen, TaskDetails)
        box = app.screen.query_one("#details-box").region
        strips = app.screen._compositor.render_strips(app.screen.size)
        hit = None
        for y in range(box.y, box.y + box.height):
            cells = _cells(strips[y])
            row = _text(cells)
            if "ask now" in row:
                hit = (cells, row.index("ask now"))
                break
        assert hit, "the note `ask now` is not painted in the details"
        cells, at = hit
        assert [fg for _c, fg, _b in cells[at:at + 3]] == [BLUE] * 3
        assert BLUE not in {fg for _c, fg, _b in cells[at + 3:at + 7]}
    saved = json.loads((tmp_path / "board.json").read_text(encoding="utf-8"))
    assert [t["notes"] for t in saved["tasks"]] == ["::b:: ask :: now"]


# =========================================================================== #
# E5 corrective pass (03-pdr-rulings §E5) — regressions, written before the fixes
# =========================================================================== #
async def test_TC_4291_a_legacy_pair_typed_under_a_pen_is_pinned_as_designed(tmp_path):
    """TC-4291 (CR-1, ruled "as designed" like P-M1-5): notes `if a == b`, `alt+5`, then
    ` then c == d` typed under the pen. The typed `==` pairs with the earlier one (legacy
    spans start first, LLR-4201.7), so the pen's span is swallowed and the pen turns off.
    PIN of the result the shipped code gives (05-review-code.md probe R1), and it never
    raises. Expected to PASS before and after the E5 fixes; it goes RED only if the rule
    changes, which must then be a decision."""
    app = _app(tmp_path, "if a == b")
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot)
        await pilot.press("alt+5", *" then c == d")
        await pilot.pause()
        assert ta.text == "if a == b::b::  then c == d ::"
        assert highlight_segments(ta.text) == [("if a ", "mut"), (" b::b::  then c ", "soon"),
                                               (" d ::", "mut")]
        assert _pen(scr) is None
        assert isinstance(app.screen, TaskModal)


async def test_TC_4292_a_paste_under_a_pen_lands_as_plain_text_after_the_span(tmp_path,
                                                                             monkeypatch):
    """TC-4292 (CR-2, ruled Fix): with a pen on (`alt+5`, `x`) and a two-line clipboard
    (`ab\\ncd`), `ctrl+v` lifts the pen first: the paste lands as plain text after the
    span's closer — `::b:: x ::ab\\ncd` — and no line ends in a literal ` ::`. NC: insert
    at the cursor inside the span → `::b:: xab\\ncd ::` (RED: the shipped code)."""
    monkeypatch.setattr(modals, "grab_clipboard_text", lambda: "ab\ncd")
    app = _app(tmp_path, "")
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot)
        await pilot.press("alt+5", "x", "ctrl+v")
        await pilot.pause()
        assert ta.text == "::b:: x ::ab\ncd"
        assert [highlight_segments(ln) for ln in ta.text.split("\n")] == [
            [("x", "blue"), ("ab", "mut")], [("cd", "mut")]]
        assert _pen(scr) is None


async def test_TC_4293_save_after_leaving_an_empty_pen_span_saves_no_span(tmp_path):
    """TC-4293 (CR-3, ruled Fix; the reviewer's deterministic repro P2): notes `x`, the pen
    action called, the cursor moved to (0, 0) and `_save` run BEFORE the move's
    SelectionChanged is handled — so `_lift_pen` sees `_pen_span()` None and must fall back
    to the remembered span. The saved notes are `x`. NC: `_lift_pen` ignores `_pen_at` →
    `x::y::  ::` saved (RED: the shipped code)."""
    app = _app(tmp_path, "x")
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot)
        scr.action_pen(2)
        assert ta.text == "x::y::  ::"
        ta.move_cursor((0, 0))
        scr._save()
        for _ in range(3):
            await pilot.pause()
        assert not isinstance(app.screen, TaskModal)
    assert app.board.tasks[0].notes == "x"
    saved = json.loads((tmp_path / "board.json").read_text(encoding="utf-8"))
    assert [t["notes"] for t in saved["tasks"]] == ["x"]


@pytest.mark.parametrize("notes, cursor", [
    ("==a=::b::  ::=x", (0, 4)),        # the user's own empty span would become `==a==x`
    ("keep ::b::  :: me", (0, 5)),      # 9 characters the user wrote would be deleted
])
async def test_TC_4294_undo_after_a_pen_never_deletes_the_users_own_span(tmp_path, notes,
                                                                        cursor):
    """TC-4294 (SR-2 + CR-3, ruled Fix): `alt+5` at the start of an empty `::b::  ::` the
    USER wrote, then `ctrl+z` (the pair undone, the pen still on), then `alt+s`: the saved
    notes are byte-equal to the user's text and its visible text unchanged. NC: delete any
    empty span of the pen's code at `_pen_at` → `==a==x` / `keep  me` (RED: the shipped
    code)."""
    from test_colour_notes import ref_visible
    app = _app(tmp_path, notes)
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot, cursor)
        await pilot.press("alt+5")
        assert ta.text != notes                       # the pair went in
        await pilot.press("ctrl+z")
        await pilot.pause()
        assert ta.text == notes
        await pilot.press("alt+s")
        for _ in range(3):
            await pilot.pause()
        assert not isinstance(app.screen, TaskModal)
    saved = app.board.tasks[0].notes
    assert saved == notes
    assert ref_visible(saved) == ref_visible(notes)


async def test_TC_4296_a_line_over_2000_chars_gets_no_ink_and_stays_fast(tmp_path):
    """TC-4296 (LLR-4204.10, SR-1): one 100 000-char notes line of spans
    (`::b::x::` × 12 500) → the field's highlight list for that row is empty, and one
    keystroke on it takes <= 1.5 s in the pilot (security measured 0.5 s without ink,
    2.6 s with). NC: no length cap → the row is inked (RED: the shipped code)."""
    note = "::b::x::" * 12_500
    assert len(note) == 100_000
    app = _app(tmp_path, note)
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot, (0, 0))
        assert not ta._highlights.get(0), f"{len(ta._highlights.get(0, []))} highlights on row 0"
        t0 = time.perf_counter()
        await pilot.press("y")
        took = time.perf_counter() - t0
        assert ta.text.startswith("y::b::x::")
        assert not ta._highlights.get(0)
        assert took <= 1.5, f"one keystroke took {took:.2f} s"


async def test_TC_4297_a_line_of_exactly_2000_chars_is_still_inked(tmp_path):
    """TC-4297 (LLR-4204.10, the boundary): a 2 000-char line of spans (`::b::x::` × 250)
    is inked: its row holds 250 `pen.blue` ranges and the first `x` cell is blue. NC: a
    cap at or below 2 000 → RED. Passes on the shipped code (no cap yet) — it guards the
    boundary of the fix."""
    note = "::b::x::" * 250
    assert len(note) == 2000
    app = _app(tmp_path, note)
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot, (0, 0))
        assert sum(1 for *_r, n in ta._highlights.get(0, []) if n == "pen.blue") == 250
        assert _ink(ta)[5][:2] == ("x", BLUE)
