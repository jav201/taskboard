"""The colour palette over a selection or a word, and the details' Notes label (batch
2026-11-01-v3-incC, Inc C, US-4201, HLR-4205, LLR-4202.9, AT-4202).

Field report (the board's owner, `username_subject`): colouring a word already written
must be as quick as taking a pen — select it (or stand on it), `alt+c`, a digit. The
palette must never corrupt a note: it rewrites only the target, refuses what would change
the text the reader sees (`std::vector`), refuses a target that crosses a colour edge, and
`esc` / `0` on plain text leave the notes exactly as they were when it opened.

Pure rules (`colour_target`, `recolour`, `palette_offset`) are checked on the design's
example table (graph-proto-M2, run there through a reference scanner); every key path is
driven on the shipped surface: a real `TaskboardApp` on a synthetic board, `e`, keys —
and for AT-4202 and the focus gate (ARCH-2) the bytes a legacy-encoding terminal sends,
parsed by Textual's `XTermParser` (`ESC c` arrives as `Key("alt+c", "c")`, printable).

RED on base `0a8dfaa`: `alt+c` opens nothing in the editor (and the terminal's `ESC c`
types `c` over the selection), the details label is the legacy one-line hint, and the
pure functions are absent (reached through `_need`: an assertion failure, never an
ImportError). No test here passes on base by design.
"""
from __future__ import annotations

import json

import pytest
from textual import events
from textual._xterm_parser import XTermParser
from textual.geometry import Region
from textual.widgets import Input, TextArea
from textual.widgets.text_area import Selection

import taskboard.modals as modals
from taskboard.app import TaskboardApp
from taskboard.modals import TaskDetails, TaskModal
from taskboard.models import Board, Project, Task
from taskboard.views import HEX, highlight_segments

from test_colour_notes import ref_visible

SIZE = (118, 30)
CODES = "roygbv"
TONE = {"r": "over", "o": "orange", "y": "soon", "g": "green", "b": "blue", "v": "violet"}
NAME = {"r": "red", "o": "orange", "y": "yellow", "g": "green", "b": "blue", "v": "violet"}
N1 = "Colour one line at a time."
N2 = "The selection crosses a colour edge: select inside one colour, or plain text."
N3 = "Nothing to colour: select text or put the cursor on a word."
N4 = "That colour would change the visible text: nothing changed."
N5 = "The notes changed while the palette was open: nothing changed."


def _need(mod, name: str):
    obj = getattr(mod, name, None)
    if obj is None:
        pytest.fail(f"{mod.__name__}.{name} is missing: Inc C is not built here")
    return obj


def _pen(scr):
    if not hasattr(scr, "pen"):
        pytest.fail("TaskModal.pen is missing: Inc C is not built here")
    return scr.pen


def _app(tmp_path, notes: str = "") -> TaskboardApp:
    b = Board.load(tmp_path / "board.json")
    b.projects.clear()
    b.tasks.clear()
    p = Project("Field notes", "sky")
    b.projects.append(p)
    b.tasks.append(Task("Write the multicolour note", p.id, "Doing", notes=notes))
    b.save()
    return TaskboardApp(board_path=str(tmp_path / "board.json"), team_sync_interval=1e9)


async def _editor(app, pilot, cursor=None, selection=None):
    await pilot.pause()
    app.selected_task_id = app.board.tasks[0].id
    await pilot.press("e")
    for _ in range(3):
        await pilot.pause()
    assert isinstance(app.screen, TaskModal), "`e` did not open the editor"
    scr = app.screen
    ta = scr.query_one("#f-notes", TextArea)
    ta.focus()
    if selection is not None:
        ta.selection = Selection(*selection)
    else:
        ta.move_cursor(ta.document.end if cursor is None else cursor)
    for _ in range(2):
        await pilot.pause()
    return scr, ta


def _on_palette(app) -> bool:
    return type(app.screen).__name__ == "ColourPalette"


async def _alt_c(pilot):
    await pilot.press("alt+c")
    for _ in range(2):
        await pilot.pause()


async def _key(pilot, *keys):
    await pilot.press(*keys)
    for _ in range(2):
        await pilot.pause()


async def _terminal(app, pilot, *chunks: str):
    for chunk in chunks:
        parser = XTermParser()
        for ev in [e for e in list(parser.feed(chunk)) + list(parser.feed(""))
                   if isinstance(e, events.Key)]:
            ev.set_sender(app)
            app._driver.send_message(ev)
            await pilot.pause()
    await pilot.pause()


def _ids(app) -> set:
    return {n.identity for n in app._notifications}


def _new_notices(app, before: set) -> list[str]:
    return [str(n.message) for n in app._notifications if n.identity not in before]


def _cells(strip):
    from rich.cells import cell_len
    out = []
    for seg in strip:
        st = seg.style
        fg = st.color.triplet.hex.lower() if st and st.color and st.color.triplet else None
        for ch in seg.text:
            out.append((ch, fg))
            out += [("", fg)] * (cell_len(ch) - 1)
    return out


def _painted(app):
    return app.screen._compositor.render_strips(app.screen.size)


def _palette_rows(app) -> list[list[tuple[str, str | None]]]:
    """The palette box's painted content rows (inside its border and padding), as cells,
    blank rows dropped."""
    box = app.screen.query_one("#cp-box")
    r = box.content_region
    strips = _painted(app)
    rows = []
    for y in range(r.y, r.y + r.height):
        cells = _cells(strips[y])[r.x:r.x + r.width]
        if "".join(c for c, _ in cells).strip():
            rows.append(cells)
    return rows


def _row_text(cells) -> str:
    return "".join(c for c, _ in cells).rstrip()


# --------------------------------------------------------------------------- #
# Pure rules — the design's example table (graph-proto-M2)
# --------------------------------------------------------------------------- #
RECOLOUR = [   # (line, a, b, key code, new line, col)  — table rows 1..23 + TC-4282
    ("the plan works", 4, 8, "r", "the ::r:: plan :: works", 17),
    ("the plan works", 4, 8, "o", "the ::o:: plan :: works", 17),
    ("the plan works", 4, 8, "y", "the ::y:: plan :: works", 17),
    ("the plan works", 4, 8, "g", "the ::g:: plan :: works", 17),
    ("the plan works", 4, 8, "b", "the ::b:: plan :: works", 17),
    ("the plan works", 4, 8, "v", "the ::v:: plan :: works", 17),
    ("go ::o::now:: ok", 8, 11, "r", "go ::r:: now :: ok", 15),
    ("go ::o::now:: ok", 8, 11, "o", "go ::o:: now :: ok", 15),
    ("go ::o::now:: ok", 8, 11, "y", "go ::y:: now :: ok", 15),
    ("go ::o::now:: ok", 8, 11, "g", "go ::g:: now :: ok", 15),
    ("go ::o::now:: ok", 8, 11, "b", "go ::b:: now :: ok", 15),
    ("go ::o::now:: ok", 8, 11, "v", "go ::v:: now :: ok", 15),
    ("::r:: a b ::", 6, 7, "y", "::y:: a b ::", 12),
    ("::b::  x  ::", 7, 8, "y", "::y::  x  ::", 12),
    ("==late==", 0, 8, "b", "::b:: late ::", 13),
    ("!!x!! y", 2, 3, "r", "::r:: x :: y", 10),
    ("++done++", 2, 6, "g", "::g:: done ::", 13),
    ("x ::b:: y :: z", 8, 9, "0", "x y z", 3),
    ("==y==", 0, 5, "0", "y", 1),
    ("::r:: open", 6, 10, "0", "open", 4),
    ("::b:: x ::r:: y ::", 6, 7, "0", "x ::r:: y ::", 2),
    ("the plan works", 4, 8, "0", "the plan works", None),
    ("::r:: open", 6, 10, "y", "::y:: open ::", 13),
    ("::b:: x ::r:: y ::", 6, 7, "y", "::y:: x  ::::r:: y ::", 11),
    ("a:plan", 2, 6, "b", "a:::b:: plan ::", 15),
    ("é café ☕", 2, 6, "o", "é ::o:: café :: ☕", 15),
    ("std::vector", 0, 11, "b", "::b:: std::vector ::", 20),     # refused later (N4)
    ("planb::", 0, 4, "b", "::b:: plan ::b::", 13),               # refused later (N4)
    ("==a::b==", 0, 8, "b", "::b:: a::b ::", 13),                 # refused later (N4)
    ("==a::b==", 0, 8, "0", "a::b", 4),
]
REFUSED = {("std::vector", "b"), ("planb::", "b"), ("==a::b==", "b")}


@pytest.mark.parametrize("line, a, b, code, new, col", RECOLOUR,
                         ids=[f"{r[0]}|{r[3]}" for r in RECOLOUR])
def test_TC_4263_recolour_rewrites_the_target_or_its_span(line, a, b, code, new, col):
    """TC-4263..TC-4267, TC-4282 (LLR-4205.4..7): a plain target is wrapped in the spaced
    form (`::c:: text ::`); a target inside a span has that span's markers replaced, the
    inner text kept (any of the 9 marker forms); `0` removes them; `0` on plain text
    changes nothing. `col` is the column just after the written closer. NC: unspaced form,
    nested wrap, opener-only removal → RED."""
    recolour = _need(modals, "recolour")
    assert recolour(line, a, b, code) == (new, col)


def test_TC_4269_recolour_changes_nothing_outside_the_rewritten_range():
    """TC-4269 (LLR-4205.9): over the 12 cases of 6 codes × {plain, inside a span}, the
    text before and after the rewritten range (the target, or the span holding it) is
    byte-equal. NC: rewrite the whole line → RED."""
    recolour = _need(modals, "recolour")
    cases = [(r, 4, 8, 4, 8) for r in RECOLOUR[:6]] + [(r, 8, 11, 3, 13) for r in RECOLOUR[6:12]]
    assert len(cases) == 12
    for (line, a, b, code, _new, _col), _a, _b, x, y in cases:
        new_line, _ = recolour(line, a, b, code)
        assert new_line[:x] == line[:x], (line, code)
        tail = len(line) - y
        assert new_line[len(new_line) - tail:] == line[y:], (line, code)


def test_TC_4287_every_allowed_rewrite_keeps_the_visible_text():
    """TC-4287 (LLR-4205.15's invariant on the allowed cases): for every recolour case but
    the three refused ones, the visible text (joined segments) is unchanged, measured by
    the product tokeniser AND the independent reference scanner; the refused ones DO
    change it (so the refusal is needed)."""
    recolour = _need(modals, "recolour")
    for line, a, b, code, _new, _col in RECOLOUR:
        new_line, _ = recolour(line, a, b, code)
        vis_old = "".join(s for s, _ in highlight_segments(line))
        vis_new = "".join(s for s, _ in highlight_segments(new_line))
        assert vis_old == ref_visible(line) and vis_new == ref_visible(new_line)
        if (line, code) in REFUSED:
            assert vis_new != vis_old, line
        else:
            assert vis_new == vis_old, (line, code, new_line)


TARGETS = [   # (lines, start, end, target, notice)
    (["the plan works"], (0, 6), (0, 6), (0, 4, 8), None),
    (["the plan works"], (0, 8), (0, 8), (0, 4, 8), None),       # just after the word
    (["the plan works"], (0, 4), (0, 4), (0, 4, 8), None),       # on its first letter
    (["the plan works"], (0, 8), (0, 4), (0, 4, 8), None),       # a selection, any order
    (["::r:: a b ::"], (0, 6), (0, 6), (0, 6, 7), None),
    (["::b:: ab ::"], (0, 11), (0, 11), (0, 9, 11), None),       # the closer word
    (["::b:: abc ::d"], (0, 12), (0, 12), (0, 12, 13), None),    # ARCH-4: never "::d"
    (["==late=="], (0, 3), (0, 3), (0, 2, 6), None),
    (["x ::b:: y :: z"], (0, 1), (0, 1), (0, 0, 1), None),
    (["x::b::y::"], (0, 0), (0, 0), (0, 0, 1), None),            # the word stops at the span
    (["ab", "cd"], (0, 1), (1, 1), None, N1),
    (["ab", "cd"], (0, 0), (1, 0), None, N1),
    (["::b:: ab :: cd"], (0, 7), (0, 13), None, N2),
    (["x ::b:: y :: z"], (0, 0), (0, 14), None, N2),             # a whole span + plain text
    (["x::b::y::"], (0, 0), (0, 9), None, N2),
    ([""], (0, 0), (0, 0), None, N3),
    (["the  plan"], (0, 4), (0, 4), None, N3),                   # two spaces at the cursor
    (["a   b"], (0, 1), (0, 4), None, N3),                       # whitespace-only selection
]


@pytest.mark.parametrize("lines, start, end, target, notice", TARGETS)
def test_TC_4261_the_target_is_the_selection_or_the_word_and_never_crosses_an_edge(
        lines, start, end, target, notice):
    """TC-4260, TC-4261, TC-4270..TC-4272, TC-4280, TC-4281 (LLR-4205.1/.2/.10/.11/.12;
    ARCH-4, P-M2-1, P-M2-3): `colour_target` gives (row, a, b) — the selection, or the
    word holding / ending at the cursor inside ONE region (a word never takes span
    markers with it) — or exactly one notice."""
    colour_target = _need(modals, "colour_target")
    assert colour_target(lines, start, end) == (target, notice)


@pytest.mark.parametrize("x, y, w, h, box", [
    (4, 5, 80, 24, (3, 6)), (70, 20, 80, 24, (65, 10)),
    (0, 3, 118, 30, (0, 4)), (110, 26, 118, 30, (103, 16)),
])
def test_TC_4273_the_box_sits_next_to_the_target_and_on_screen(x, y, w, h, box):
    """TC-4273 (LLR-4205.13, P-M2-9): a 15×10 box below the anchor (top row = anchor + 1),
    or above it when it would not fit (bottom row = anchor − 1), clamped to the screen."""
    palette_offset = _need(modals, "palette_offset")
    assert tuple(palette_offset(x, y, w, h)) == box


# --------------------------------------------------------------------------- #
# Key paths — the palette opens, shows, picks, cancels (HLR-4205)
# --------------------------------------------------------------------------- #
async def test_TC_4260_alt_c_over_a_selection_opens_the_palette(tmp_path):
    """TC-4260 (LLR-4205.1): `plan` selected (right to left), `alt+c` → the palette is the
    screen on top; `5` colours exactly `plan`. NC: binding absent → RED (RED on base)."""
    app = _app(tmp_path, "the plan works")
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot, selection=((0, 8), (0, 4)))
        await _alt_c(pilot)
        assert _on_palette(app), type(app.screen).__name__
        await _key(pilot, "5")
        assert isinstance(app.screen, TaskModal)
        assert ta.text == "the ::b:: plan :: works"


@pytest.mark.parametrize("col", [6, 8])
async def test_TC_4261_alt_c_on_a_word_colours_that_word(tmp_path, col):
    """TC-4261 (LLR-4205.2): no selection, the cursor inside `plan` (0, 6) or just after
    it (0, 8) → the palette's `5` gives `the ::b:: plan :: works`, 2/2. NC: target the
    line → RED."""
    app = _app(tmp_path, "the plan works")
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot, (0, col))
        await _alt_c(pilot)
        assert _on_palette(app), f"no palette: the screen is {type(app.screen).__name__}"
        await _key(pilot, "5")
        assert ta.text == "the ::b:: plan :: works"


async def test_TC_4262_the_palette_lists_six_pens_none_and_cancel(tmp_path):
    """TC-4262 (LLR-4205.3): 8 rows in order — `<n> ██ <name>` for the six pens, then
    `0 none` and `esc cancel`; each name (and its swatch) painted in its tone (6/6), each
    key in bold bright. NC: letters for keys → RED."""
    app = _app(tmp_path, "the plan works")
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot, (0, 6))
        await _alt_c(pilot)
        assert _on_palette(app), f"no palette: the screen is {type(app.screen).__name__}"
        rows = _palette_rows(app)
        want = [f"{i + 1} ██ {NAME[c]}" for i, c in enumerate(CODES)] + ["0 none", "esc cancel"]
        assert [_row_text(r).strip() for r in rows] == want
        for i, code in enumerate(CODES):
            cells = [(ch, fg) for ch, fg in rows[i] if ch.strip()]
            key, *rest = cells
            assert key == (str(i + 1), HEX["bright"]), cells
            assert {fg for _ch, fg in rest} == {HEX[TONE[code]]}, (code, cells)
        assert [fg for ch, fg in rows[6] if ch == "0"] == [HEX["bright"]]
        await _key(pilot, "escape")


@pytest.mark.parametrize("notes, cursor, key, want", [
    ("==late==", (0, 3), "5", "::b:: late ::"),
    ("::r:: a b ::", (0, 6), "3", "::y:: a b ::"),
])
async def test_TC_4264_a_digit_inside_a_span_swaps_its_markers(tmp_path, notes, cursor, key,
                                                               want):
    """TC-4264 / TC-4265 (LLR-4205.5): inside one span, a digit replaces that span's
    markers with the chosen code's, the inner text kept, 2/2. NC: wrap again (nested) →
    RED."""
    app = _app(tmp_path, notes)
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot, cursor)
        await _alt_c(pilot)
        assert _on_palette(app), f"no palette: the screen is {type(app.screen).__name__}"
        await _key(pilot, key)
        assert ta.text == want


@pytest.mark.parametrize("notes, cursor, want", [
    ("x ::b:: y :: z", (0, 8), "x y z"),
    ("==y==", (0, 2), "y"),
])
async def test_TC_4266_zero_inside_a_span_uncolours_it(tmp_path, notes, cursor, want):
    """TC-4266 (LLR-4205.6): `0` inside one span removes both markers, the inner text
    kept, 2/2. NC: remove only the opener → RED."""
    app = _app(tmp_path, notes)
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot, cursor)
        await _alt_c(pilot)
        assert _on_palette(app), f"no palette: the screen is {type(app.screen).__name__}"
        await _key(pilot, "0")
        assert ta.text == want


async def test_TC_4267_zero_on_plain_text_changes_nothing(tmp_path):
    """TC-4267 (LLR-4205.7): `plan` selected, `alt+c`, `0` → the notes byte-equal to the
    notes at palette open, the selection as it was. NC: strip the word → RED."""
    app = _app(tmp_path, "the plan works")
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot, selection=((0, 8), (0, 4)))
        await _alt_c(pilot)
        assert _on_palette(app), f"no palette: the screen is {type(app.screen).__name__}"
        at_open = ta.text
        await _key(pilot, "0")
        assert not _on_palette(app), "the palette opened"
        assert ta.text == at_open == "the plan works"
        assert ta.selection == Selection((0, 8), (0, 4))


async def test_TC_4268_esc_closes_the_palette_and_changes_nothing(tmp_path):
    """TC-4268 (LLR-4205.8): `esc` → the palette gone, the notes byte-equal, the selection
    still (0, 8)→(0, 4), the focus back in the notes, the editor still open.
    NC: `esc` applies `0` → RED."""
    app = _app(tmp_path, "the plan works")
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot, selection=((0, 8), (0, 4)))
        await _alt_c(pilot)
        assert _on_palette(app), f"no palette: the screen is {type(app.screen).__name__}"
        await _key(pilot, "escape")
        assert isinstance(app.screen, TaskModal)
        assert ta.text == "the plan works"
        assert ta.selection == Selection((0, 8), (0, 4))
        assert app.focused is ta


async def test_TC_4268_esc_compares_with_the_notes_at_palette_open(tmp_path):
    """TC-4268 (P-M2-4, ARCH-10): a pen span with no closer (`::b:: ab`, pen on); `alt+c`
    lifts the pen (writing ` ::`) and opens the palette on `ab`; `esc` leaves
    `::b:: ab ::` — the notes at palette open, not the notes before `alt+c`."""
    app = _app(tmp_path, "")
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot)
        await pilot.press("alt+5", *"ab", "delete", "delete", "delete")
        assert ta.text == "::b:: ab"
        await _alt_c(pilot)
        assert _on_palette(app), f"no palette: the screen is {type(app.screen).__name__}"
        assert ta.text == "::b:: ab ::"
        await _key(pilot, "escape")
        assert ta.text == "::b:: ab ::" and _pen(scr) is None


@pytest.mark.parametrize("notes, kw, notice", [
    ("ab\ncd", {"selection": ((0, 1), (1, 1))}, N1),          # LLR-4205.10
    ("::b:: ab :: cd", {"selection": ((0, 7), (0, 13))}, N2),  # LLR-4205.11
    ("x ::b:: y :: z", {"selection": ((0, 0), (0, 14))}, N2),  # P-M2-1
    ("", {"cursor": (0, 0)}, N3),                              # LLR-4205.12
    ("a   b", {"selection": ((0, 1), (0, 4))}, N3),            # P-M2-3
    ("the  plan", {"cursor": (0, 4)}, N3),
])
async def test_TC_4270_alt_c_refuses_with_one_notice_and_no_palette(tmp_path, notes, kw, notice):
    """TC-4270, TC-4271, TC-4272, TC-4280, TC-4281 (LLR-4205.10/.11/.12): a multi-line
    selection, a target over a colour edge, or nothing to colour → no palette, ONE
    notice saying why, the notes byte-equal. NC: open anyway → RED."""
    app = _app(tmp_path, notes)
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot, **kw)
        before = _ids(app)
        await _alt_c(pilot)
        assert not _on_palette(app), "the palette opened"
        assert ta.text == notes
        assert _new_notices(app, before) == [notice]


@pytest.mark.parametrize("size", [(80, 24), (118, 30)], ids=lambda s: f"{s[0]}x{s[1]}")
@pytest.mark.parametrize("where", ["first", "last"])
async def test_TC_4273_the_palette_box_is_on_screen_next_to_the_target(tmp_path, size, where):
    """TC-4273 (LLR-4205.13): at 80x24 and 118x30, for a target on the notes field's first
    and last visible row, the box lies wholly on screen and its top row is the anchor row
    + 1, or its bottom row the anchor row − 1 (4/4). NC: no clamping → RED at 80x24 last
    row."""
    notes = "plan" if where == "first" else "\n".join(f"line {n}" for n in range(30))
    app = _app(tmp_path, notes)
    async with app.run_test(size=size) as pilot:
        scr, ta = await _editor(app, pilot, (0, 0))
        if where == "first":
            ta.move_cursor((0, 4))
        else:
            ta.scroll_to(y=0, animate=False)
            r = ta.content_region.height - 1
            ta.move_cursor((r, 6))
        for _ in range(2):
            await pilot.pause()
        anchor = ta.cursor_screen_offset
        if where == "last":
            assert anchor.y == ta.content_region.y + ta.content_region.height - 1
        await _alt_c(pilot)
        assert _on_palette(app), f"no palette: the screen is {type(app.screen).__name__}"
        box = app.screen.query_one("#cp-box").region
        assert Region(0, 0, *size).contains_region(box), (box, size)
        assert box.y == anchor.y + 1 or box.y + box.height - 1 == anchor.y - 1, (box, anchor)
        await _key(pilot, "escape")


@pytest.mark.parametrize("notes, setup, then, want", [
    ("", ["alt+5", *"ab"], "3", "::y:: ab ::"),       # the pen's span is the target
    ("now", ["alt+5", *"go"], "3", "::y:: go ::now"),  # ARCH-3: not the word "::now"
])
async def test_TC_4274_alt_c_under_a_pen_targets_the_pens_span(tmp_path, notes, setup, then,
                                                               want):
    """TC-4274 (LLR-4205.14, ARCH-3): `alt+5 ab alt+c 3` → `::y:: ab ::`, the pen off; with
    text glued after the span (`::b:: go ::now`) the target is still the pen's own span.
    NC: pen kept / the word at the lifted cursor → RED."""
    app = _app(tmp_path, notes)
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot, (0, 0))
        await pilot.press(*setup)
        await _alt_c(pilot)
        assert _on_palette(app), f"no palette: the screen is {type(app.screen).__name__}"
        assert _pen(scr) is None
        await _key(pilot, then)
        assert ta.text == want


@pytest.mark.parametrize("notes, cursor", [("x ", (0, 2)), ("plan", (0, 4))])
async def test_TC_4274_alt_c_on_an_empty_pen_removes_it_and_says_nothing_to_colour(
        tmp_path, notes, cursor):
    """TC-4274 (ARCH-3): an EMPTY pen span is removed by the lift and the call ends with
    the "nothing to colour" notice — it does not fall back to the word before it."""
    app = _app(tmp_path, notes)
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot, cursor)
        await pilot.press("alt+5")
        assert "::b::  ::" in ta.text
        before = _ids(app)
        await _alt_c(pilot)
        assert not _on_palette(app), "the palette opened"
        assert ta.text == notes and ta.cursor_location == cursor
        assert _new_notices(app, before) == [N3]
        assert _pen(scr) is None


async def test_TC_4275_after_a_pick_the_cursor_stands_after_the_new_closer(tmp_path):
    """TC-4275: `the plan works`, cursor on `plan`, `alt+c`, `3` → `the ::y:: plan :: works`,
    cursor (0, 17), no selection; the next `!` is outside the colour."""
    app = _app(tmp_path, "the plan works")
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot, (0, 6))
        await _alt_c(pilot)
        await _key(pilot, "3")
        assert ta.text == "the ::y:: plan :: works"
        assert ta.cursor_location == (0, 17) and ta.selection.is_empty
        await _key(pilot, "!")
        assert ta.text == "the ::y:: plan ::! works"
        assert ("plan", "soon") in highlight_segments(ta.text)
        assert all("!" not in s for s, tone in highlight_segments(ta.text) if tone == "soon")


async def test_TC_4283_keys_the_palette_does_not_list_do_nothing(tmp_path):
    """TC-4283 (P-M2-8): `a`, `enter`, `7` in the palette → still the palette, the notes
    byte-equal."""
    app = _app(tmp_path, "the plan works")
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot, (0, 6))
        await _alt_c(pilot)
        assert _on_palette(app), f"no palette: the screen is {type(app.screen).__name__}"
        await _key(pilot, "a", "enter", "7")
        assert _on_palette(app), f"no palette: the screen is {type(app.screen).__name__}"
        assert ta.text == "the plan works"
        await _key(pilot, "escape")


async def test_TC_4284_alt_c_outside_the_notes_changes_no_field(tmp_path):
    """TC-4284 (LLR-4205.16, ARCH-2): focus on the title `T`, notes `n`; the terminal's
    `ESC c` (`Key("alt+c", "c")`, printable) → no palette, title and notes byte-equal,
    no notice. NC: a denied binding → the title becomes `Tc` (RED; RED on base)."""
    app = _app(tmp_path, "n")
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot)
        title = scr.query_one("#f-title", Input)
        title.value = "T"
        title.focus()
        title.cursor_position = 1
        await pilot.pause()
        before = _ids(app)
        await _terminal(app, pilot, "\x1bc")
        assert not _on_palette(app), "the palette opened"
        assert title.value == "T" and ta.text == "n"
        assert _new_notices(app, before) == []


@pytest.mark.parametrize("notes, kw", [
    ("std::vector", {"cursor": (0, 2)}),                        # TC-4285
    ("planb::", {"selection": ((0, 0), (0, 4))}),               # TC-4285: b:: would open
    ("==a::b==", {"cursor": (0, 3)}),                           # TC-4286
])
async def test_TC_4285_a_rewrite_that_changes_the_visible_text_is_refused(tmp_path, notes, kw):
    """TC-4285 / TC-4286 (LLR-4205.15, P-M2-2): `5` on a target whose rewrite would change
    the text the reader sees → the notes byte-equal, ONE notice N4. NC: rewrite anyway →
    the visible text changes (RED)."""
    app = _app(tmp_path, notes)
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot, **kw)
        await _alt_c(pilot)
        assert _on_palette(app), f"no palette: the screen is {type(app.screen).__name__}"
        before = _ids(app)
        await _key(pilot, "5")
        assert ta.text == notes
        assert _new_notices(app, before) == [N4]


async def test_TC_4286_uncolouring_a_span_with_colons_inside_is_allowed(tmp_path):
    """TC-4286: `0` on `==a::b==` keeps the visible text (`a::b`), so it is allowed:
    `a::b`, cursor (0, 4)."""
    app = _app(tmp_path, "==a::b==")
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot, (0, 3))
        await _alt_c(pilot)
        await _key(pilot, "0")
        assert ta.text == "a::b" and ta.cursor_location == (0, 4)


@pytest.mark.parametrize("notes, cursor, row, replacement, want", [
    ("the plan works", (0, 6), 0, "the plan", "the plan"),
    ("a\nthe plan works", (1, 6), 1, None, "a"),
])
async def test_TC_4288_a_line_changed_under_the_palette_is_left_alone(tmp_path, notes, cursor,
                                                                      row, replacement, want):
    """TC-4288 (A-4, SEC-5): the target's line is changed (or deleted) while the palette
    is on top; the pick changes nothing and shows ONE notice N5, with no exception."""
    app = _app(tmp_path, notes)
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot, cursor)
        await _alt_c(pilot)
        assert _on_palette(app), f"no palette: the screen is {type(app.screen).__name__}"
        line = ta.document.get_line(row)
        if replacement is None:                    # delete the row (and its line break)
            ta.replace("", (row - 1, len(ta.document.get_line(row - 1))), (row, len(line)))
        else:
            ta.replace(replacement, (row, 0), (row, len(line)))
        await pilot.pause()
        assert ta.text == want
        before = _ids(app)
        await _key(pilot, "5")
        assert isinstance(app.screen, TaskModal)
        assert ta.text == want
        assert _new_notices(app, before) == [N5]


# --------------------------------------------------------------------------- #
# TC-4276 — the details screen's Notes label (LLR-4202.9)
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("size", [(80, 24), (118, 30)], ids=lambda s: f"{s[0]}x{s[1]}")
async def test_TC_4276_the_details_label_lists_the_six_codes_in_their_tones(tmp_path, size):
    """TC-4276 (LLR-4202.9, C-2 / A-2): the details screen (`enter`) paints the Notes
    label `Notes  ::c:: … ::  r o y g b v` whole, each code letter in its tone (6/6, pen
    order), the hint in `mut`, no legacy listing (`==`, `!!`, `++`); the note `ask` below
    it is blue. NC: the base label → RED."""
    app = _app(tmp_path, "::b:: ask ::")
    async with app.run_test(size=size) as pilot:
        await pilot.pause()
        app.selected_task_id = app.board.tasks[0].id
        await pilot.press("enter")
        for _ in range(4):
            await pilot.pause()
        assert isinstance(app.screen, TaskDetails)
        box = app.screen.query_one("#details-box").region
        strips = _painted(app)
        rows = [(_cells(strips[y])[box.x + 1:box.x + box.width - 1])
                for y in range(box.y, box.y + box.height)]
        label_i = next((i for i, r in enumerate(rows) if _row_text(r).strip().startswith("Notes")),
                       None)
        assert label_i is not None, [_row_text(r) for r in rows]
        cells = rows[label_i]
        text = _row_text(cells)
        assert "::c:: … ::" in text and "r o y g b v" in text, text
        assert not any(m in text for m in ("==", "!!", "++")), text
        at = text.index("r o y g b v")
        assert [cells[at + 2 * i] for i in range(6)] == [(c, HEX[TONE[c]]) for c in CODES]
        hint = text.index("::c::")
        assert {fg for ch, fg in cells[hint:hint + 10] if ch.strip()} == {HEX["mut"]}
        below = [r for r in rows[label_i + 1:] if "ask" in _row_text(r)]
        assert below, "the note is not painted under the label"
        k = _row_text(below[0]).index("ask")
        assert [fg for _c, fg in below[0][k:k + 3]] == [HEX["blue"]] * 3


# --------------------------------------------------------------------------- #
# AT-4202 — the palette, end to end, from the terminal's bytes to the saved board
# --------------------------------------------------------------------------- #
async def test_AT_4202_select_a_word_colour_it_yellow_and_save(tmp_path):
    """AT-4202 (HLR-4205, US-4201): notes `the plan works`, cursor (0, 8); the bytes
    Windows Terminal sends: `shift+left` ×4 (selects `plan`), `ESC c` → the palette shows
    its 8 rows; `3`; `ESC s` → the board file holds `the ::y:: plan :: works`.
    RED on base: `ESC c` types `c` over the selection."""
    app = _app(tmp_path, "the plan works")
    async with app.run_test(size=SIZE) as pilot:
        scr, ta = await _editor(app, pilot, (0, 8))
        await _terminal(app, pilot, *["\x1b[1;2D"] * 4)
        assert ta.selected_text == "plan"
        await _terminal(app, pilot, "\x1bc")
        assert _on_palette(app), type(app.screen).__name__
        assert len(_palette_rows(app)) == 8
        await _terminal(app, pilot, "3")
        assert ta.text == "the ::y:: plan :: works"
        await _terminal(app, pilot, "\x1bs")
        for _ in range(3):
            await pilot.pause()
        assert not isinstance(app.screen, TaskModal)
    saved = json.loads((tmp_path / "board.json").read_text(encoding="utf-8"))
    assert [t["notes"] for t in saved["tasks"]] == ["the ::y:: plan :: works"]


# =========================================================================== #
# E5 corrective pass (03-pdr-rulings §E5) — regressions, written before the fixes
# =========================================================================== #
def _seen_rows(app) -> list[str]:
    """What the terminal SHOWS: the top screen composited over the screens under it
    (`App.export_screenshot`'s own path: `render_update(full=True,
    screen_stack=app._background_screens)`), as plain text rows. `render_strips` alone
    renders only the top screen and cannot tell an opaque palette from a see-through one."""
    import io
    from rich.console import Console
    w, h = app.size
    con = Console(width=w, height=h, file=io.StringIO(), force_terminal=True,
                  color_system="truecolor", record=True, legacy_windows=False, safe_box=False)
    con.print(app.screen._compositor.render_update(full=True,
                                                   screen_stack=app._background_screens))
    return con.export_text().splitlines()


@pytest.mark.parametrize("size", [(118, 30), (80, 24)], ids=lambda s: f"{s[0]}x{s[1]}")
async def test_TC_4290_the_editor_shows_through_around_the_palette(tmp_path, size):
    """TC-4290 (E13-1, ruled Fix; C-3 "a small palette over the selection"): with the
    palette open, the editor stays visible around the box — the task's title, painted on a
    row the box does not cover, is still shown on screen (`multicolour note`: at 80
    columns the title Input is scrolled), and so is the notes' text. NC: an
    opaque palette screen (the app's `Screen { background }` outranking the palette's own
    CSS) → nothing but background outside the box (RED: the shipped code,
    evidence/captures/palette_118x30.png)."""
    app = _app(tmp_path, "the plan works")
    async with app.run_test(size=size) as pilot:
        scr, ta = await _editor(app, pilot, (0, 6))
        title_row = scr.query_one("#f-title").region.y
        await _alt_c(pilot)
        assert _on_palette(app), f"no palette: the screen is {type(app.screen).__name__}"
        box = app.screen.query_one("#cp-box").region
        assert not (box.y <= title_row < box.y + box.height), "the box covers the title row"
        rows = _seen_rows(app)
        # a fragment that survives the title Input's horizontal scroll at 80 columns
        # (`… e the multicolour note`); an opaque screen paints only background here
        assert "multicolour note" in rows[title_row], rows[title_row]
        assert any("the plan works" in r for r in rows), "the notes vanished behind the palette"
        await _key(pilot, "escape")


def test_TC_4295_recolour_refuses_an_unknown_code():
    """TC-4295 (CR-4, ruled Fix): `recolour` raises ValueError on a code outside
    `r o y g b v` (and the uncolour `0`), as its contract says. NC: write `::z::` →
    `the ::z:: plan :: works` (RED: the shipped code)."""
    recolour = _need(modals, "recolour")
    with pytest.raises(ValueError):
        recolour("the plan works", 4, 8, "z")
