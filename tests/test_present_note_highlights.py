"""The presentation colours the notes' highlights (batch 2026-10-25-batch-02).

HLR-2901 / LLR-2901.1 · HLR-2902 / LLR-2902.1 · HLR-2903 / LLR-2903.1 ·
HLR-2904 / LLR-2904.1 · AT-2901 .. AT-2904 + the layer-0 unit arms.

Why these tests exist: a note's `==soon==` / `!!over!!` / `++green++` highlights
were painted as plain ink in the presentation — the room could not see what the
note calls urgent. The one tokeniser (`highlight_segments`) colours every path
(the gantt cursor note, the split view's blocks, the `x` export) with the
markers dropped, the wrap measured on the marker-free text (a note and its
marker-free twin wrap to identical shapes), mentions bold pink inside any span,
and every byte escaped before it enters markup.

The app-driving ATs reuse the people round's synthetic directory
(`people_round_fixture.py`, `tests/people_look.py`'s `home` seam) and the
AT-1001 pattern (`run_test`, wait for the milestone offer, press keys, read
`#present-frame`). Synthetic people only — never the operator's real name.

RED on the base tree: `present_note_lines` returns (lead, str) rows, the note
rows paint everything `ink`, and the markers reach the screen.
"""
from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest
from rich.text import Text

import people_round_fixture as fx
from taskboard import app as app_module
from taskboard import models, views
from taskboard.models import Board

NB = " "
HEX = views.HEX


class _Today(date):
    @classmethod
    def today(cls):
        return fx.TODAY


@pytest.fixture
def home(tmp_path, monkeypatch):
    """The people round's registry in a fake home, the calendar frozen on the
    fixture's TODAY (tests/people_look.py's seam)."""
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
    from taskboard import modals
    for mod in (app_module, models, views, modals):
        monkeypatch.setattr(mod, "date", _Today)
    return tmp_path / ".taskboard"


def _seed(home, notes: dict[str, str]) -> None:
    """The people round's Client A board with `notes` overlaid, saved to disk."""
    fx.build(home, last="client-a")
    b = Board.load(fx.board_path(home, "client-a"))
    for tid, text in notes.items():
        b.task_by_id(tid).notes = text
    b.save()


async def _present(pilot, app, task: str, *keys: str) -> None:
    """`R` (+ `keys`) on the presentation of `task`'s project, frame painted."""
    await pilot.press("escape")                     # the home screen -> the board
    app.selected_task_id = task
    app.refresh_view()
    await pilot.press("R", *keys)
    await pilot.pause()


def _frame(content) -> list[tuple[str, list[tuple[str, str]]]]:
    """The frame Text as (plain row, [(clipped span text, style)]) rows."""
    plain = content.plain
    rows, off = [], 0
    for line in plain.split("\n"):
        spans = []
        for s in content.spans:
            a, b = max(s.start, off), min(s.end, off + len(line))
            if a < b:
                spans.append((plain[a:b], str(s.style)))
        rows.append((line, spans))
        off += len(line) + 1
    return rows


def _has(spans: list[tuple[str, str]], text: str, style: str) -> bool:
    return (text, style) in spans


def _alpha_styles(spans: list[tuple[str, str]]) -> list[tuple[str, str]]:
    return [(t, s) for t, s in spans if any(ch.isalpha() for ch in t)]


# --------------------------------------------------------------------------- #
# AT-2901 — the gantt view's cursor note colours the highlights (HLR-2901)
# --------------------------------------------------------------------------- #
async def test_AT_2901_gantt_cursor_note_colours_highlights(home):
    """AT-2901 (HLR-2901, LLR-2901.1): the cursor note's `==a== !!b!! ++c++`
    reaches the frame with the markers dropped — `a` in #fbbf24, `b` in
    #f43f5e, `c` in #4ade80, no `==`/`!!`/`++` run anywhere — and the note's
    unmarked words keep the presentation's base tone #e6edf3."""
    from textual.widgets import Static

    from taskboard.__main__ import open_app
    _seed(home, {"tc5": "==a== !!b!! ++c++\nunmarked words read in ink"})
    app = open_app(None)
    async with app.run_test(size=(118, 31)) as pilot:
        await _present(pilot, app, "tc5")
        content = app.screen.query_one("#present-frame", Static).content
        rows = _frame(content)
        joined = "\n".join(line for line, _ in rows)
        for run in ("==", "!!", "++"):
            assert run not in joined, (run, joined)
        tone_row = next(spans for line, spans in rows if "a b c" in line)
        assert _has(tone_row, "a", HEX["soon"]), tone_row
        assert _has(tone_row, "b", HEX["over"]), tone_row
        assert _has(tone_row, "c", HEX["green"]), tone_row
        ink_row = next(spans for line, spans in rows if "unmarked words" in line)
        for text, style in _alpha_styles(ink_row):
            assert style == HEX["ink"], (text, style, ink_row)


# --------------------------------------------------------------------------- #
# AT-2902 — the split view colours the highlights, at 118x30 and 80x24 (HLR-2902)
# --------------------------------------------------------------------------- #
_WRAP_NOTE = ("==one== !!two!! ++alpha bravo charlie delta echo foxtrot golf "
              "hotel india juliet kilo lima++ plain tail words")
_WRAP_TWIN = ("one two alpha bravo charlie delta echo foxtrot golf hotel india "
              "juliet kilo lima plain tail words")
_CE_TITLES = ("Golden question set", "Judge rubric", "Eval report v1")


def _block(rows, title):
    """A task's block below the gantt separator: its heading row and the note
    rows under it, read from the block's own column (the two-column split
    pairs both columns in one frame row). The block ends at an empty row or
    the next task's heading in the same column."""
    start = next(i for i, (line, _) in enumerate(rows) if line.strip().startswith("─"))

    def col(line):
        return line[1:line.index("│")] if "│" in line else line[1:]

    i = next(i for i, (line, _) in enumerate(rows[start:], start) if title in col(line))
    out = []
    for line, _ in rows[i + 1:]:
        part = col(line)
        if not part.strip() or any(t in part for t in _CE_TITLES if t != title):
            break
        out.append(part)
    return out


@pytest.mark.parametrize("size", [(118, 30), (80, 24)])
async def test_AT_2902_split_view_colours_highlights_two_sizes(home, size):
    """AT-2902 (HLR-2902, LLR-2902.1): the split view at 118x30 AND 80x24
    carries the three tones with no marker run; the `++…++` span crossing a
    row boundary keeps #4ade80 on BOTH rows it touches; a note and its
    marker-free twin wrap to identical row shapes (row count and per-row cell
    counts)."""
    from textual.widgets import Static

    from taskboard.__main__ import open_app
    _seed(home, {"tc5": _WRAP_NOTE, "tc6": _WRAP_TWIN})
    app = open_app(None)
    async with app.run_test(size=size) as pilot:
        await _present(pilot, app, "tc5", "2")
        content = app.screen.query_one("#present-frame", Static).content
        rows = _frame(content)
        joined = "\n".join(line for line, _ in rows)
        for run in ("==", "!!", "++"):
            assert run not in joined, (size, run, joined)
        styles = {style for _, spans in rows for _, style in spans}
        for key in ("soon", "over", "green", "ink"):
            assert HEX[key] in styles, (size, key, styles)
        first = next(spans for line, spans in rows if "alpha" in line)
        last = next(spans for line, spans in rows if "lima" in line)
        assert any(s == HEX["green"] and "alpha" in t for t, s in first), (size, first)
        assert any(s == HEX["green"] and "lima" in t for t, s in last), (size, last)
        tail = next(spans for line, spans in rows if "plain tail words" in line)
        assert any(s == HEX["ink"] and "plain tail words" in t for t, s in tail), (size, tail)
        # width equivalence: the note and its marker-free twin shape identically
        marked, twin = _block(rows, "Golden question set"), _block(rows, "Judge rubric")
        assert marked and twin, (size, [l for l, _ in rows])
        assert "… +" not in "\n".join(marked + twin)
        assert [views.vis(r) for r in marked] == [views.vis(r) for r in twin], \
            (size, marked, twin)
        assert [r[2:] for r in marked] == [r[2:] for r in twin], (size, marked, twin)


# --------------------------------------------------------------------------- #
# AT-2903 — the `x` export carries the same colours, no markers (HLR-2903)
# --------------------------------------------------------------------------- #
async def test_AT_2903_split_export_svg_carries_tones(home):
    """AT-2903 (HLR-2903, LLR-2903.1): the `x` SVG of the split view holds
    #fbbf24 / #f43f5e / #4ade80, no marker run, the span words inside the
    text elements; a hostile note with `<`, `&` and a `<script>` tag reaches
    the file only escaped (0 raw `<script` bytes)."""
    from taskboard.__main__ import open_app
    _seed(home, {"tc5": _WRAP_NOTE,
                 "tc7": "hostile <b> & <script>alert(1)</script> end"})
    app = open_app(None)
    async with app.run_test(size=(118, 30)) as pilot:
        await _present(pilot, app, "tc5", "2")
        await pilot.press("x")
        await pilot.pause()
        svgs = list((home / "boards/client-a/reports").glob("*.svg"))
        assert len(svgs) == 1, svgs
        data = svgs[0].read_bytes()
        for key in ("soon", "over", "green"):
            assert HEX[key].encode() in data, (key, data[:400])
        for run in (b"==one==", b"!!two!!", b"++alpha"):
            assert run not in data, run
        for word in (b"one", b"two", b"alpha", b"lima"):
            assert word in data, word
        assert b"<script" not in data
        assert b"&lt;script" in data
        assert b"<b>" not in data
        assert b"&lt;b&gt;" in data
        assert b"&amp;" in data


# --------------------------------------------------------------------------- #
# AT-2904 — mentions, bullets and unpaired markers keep their rules (HLR-2904)
# --------------------------------------------------------------------------- #
async def test_AT_2904_mentions_bullets_unpaired_markers(home):
    """AT-2904 (HLR-2904, LLR-2904.1): a mention inside a highlighted span
    stays bold #f472b6 with the span keeping its tone; an unclosed `!!` marker
    paints its text literally in #e6edf3; a `• `-led highlighted item keeps
    the lead `mut`; hostile payloads (`[bold red]`, `a [/] b`, `\\x1b[31m`)
    render literal — 0 ESC bytes in the painted frame, no exception, no style
    leak (the red never applies)."""
    from textual.widgets import Static

    from taskboard.__main__ import open_app
    _seed(home, {
        "tc5": "==ping @ana.ruiz now== done",
        "tc6": "pay !!attention today\nmarkup [bold red] and a [/] b end \x1b[31m",
        "tc7": "- ==bullet item== tail",
    })
    app = open_app(None)
    async with app.run_test(size=(118, 30)) as pilot:
        await _present(pilot, app, "tc5", "2")
        content = app.screen.query_one("#present-frame", Static).content
        assert "\x1b" not in content.plain          # the painted frame: 0 ESC bytes
        rows = _frame(content)
        # the mention inside the span: bold pink, the span keeps its tone
        row = next(spans for line, spans in rows if "ping" in line)
        assert _has(row, f"@Ana{NB}Ruiz", f"bold {HEX['pink']}"), row
        assert _has(row, "ping ", HEX["soon"]), row
        assert _has(row, " now", HEX["soon"]), row
        # the unpaired marker is literal text in the base tone
        row = next(spans for line, spans in rows if "pay" in line)
        assert _has(row, "pay !!attention today", HEX["ink"]), row
        # the bullet lead stays `mut`, the span keeps its tone
        row = next(spans for line, spans in rows if "bullet item" in line)
        assert _has(row, "• ", HEX["mut"]), row
        assert _has(row, "bullet item", HEX["soon"]), row
        # the hostile payloads render literal in ink — nothing else applies
        row = next(spans for line, spans in rows if "[bold red]" in line)
        assert _has(row, "markup [bold red] and a [/] b end [31m", HEX["ink"]), row
        for _text, style in row:
            assert "red" not in style.lower(), (_text, style, row)   # the red never applies


# --------------------------------------------------------------------------- #
# Layer 0 — the _tone_row matcher, the twin shapes, the cut seat
# --------------------------------------------------------------------------- #
def test_L0_tone_row_whitespace_drops_at_row_breaks():
    """Class (a): the wrap drops ASCII whitespace at a row break — the walk
    skips it, attributes the row, and reports where the next row begins."""
    pieces = [("foo bar baz", "ink")]
    p, at = views._tone_row("foo", pieces)
    assert p == [("foo", "ink")] and at == 3
    p, at = views._tone_row("bar", pieces, at)
    assert p == [("bar", "ink")] and at == 7
    p, at = views._tone_row("baz", pieces, at)
    assert p == [("baz", "ink")] and at == 11


def test_L0_tone_row_whitespace_substitutions():
    """Class (b): the wrap draws whitespace differently — one whitespace char
    substituted for another, and `expand_tabs` drawing one tab as several
    spaces — every drawn char re-attributed, none lost, none invented."""
    p, at = views._tone_row("a b", [("a\fb", "soon")])          # one for one
    assert p == [("a b", "soon")] and at == 3
    p, at = views._tone_row("a" + " " * 7 + "b", [("a\tb", "ink")])   # tab -> 7 spaces
    assert p == [("a       b", "ink")] and at == 3


def test_L0_tone_row_empty_row_stays_put():
    assert views._tone_row("", [("x", "ink")]) == ([("", "ink")], 0)


def test_L0_tone_row_zero_misattributed_chars():
    """The tones follow the stream, never the row's look-alike chars: the last
    `n` of `n o n` is `ink` even though the stream opens on a `soon` one."""
    pieces = [("n ", "soon"), ("o n", "ink")]
    p, at = views._tone_row("n o", pieces)
    assert p == [("n ", "soon"), ("o", "ink")] and at == 3
    p, at = views._tone_row("n", pieces, at)
    assert p == [("n", "ink")] and at == 5
    # a multi-tone paragraph re-attributed row for row, exactly
    pieces = [("alpha ", "soon"), ("bravo ", "over"), ("charlie", "green")]
    p, at = views._tone_row("alpha bravo", pieces)
    assert p == [("alpha ", "soon"), ("bravo", "over")] and at == 11
    p, at = views._tone_row("charlie", pieces, at)
    assert p == [("charlie", "green")] and at == 19


def test_L0_tone_row_alarm_outside_whitespace():
    """A wrap that mutated non-whitespace is a bug alarm, never silently
    absorbed — and the stream never emits past its end."""
    with pytest.raises(AssertionError):
        views._tone_row("xbb", [("abb", "ink")])
    with pytest.raises(AssertionError):
        views._tone_row("bbq", [("bb", "ink")])


@pytest.mark.parametrize("w", [7, 12, 24, 30, 50])
def test_L0_marker_free_twin_wraps_identically(w):
    """LLR-2902.1: the width counts the marker-free text only — a note and its
    marker-free twin wrap to identical row shapes (row count and per-row cell
    counts) at every width."""
    marked = "==alpha== bravo ++charlie delta echo foxtrot++ golf"
    twin = "alpha bravo charlie delta echo foxtrot golf"

    def shape(notes):
        return [(lead, views.vis("".join(seg for seg, _ in pieces)))
                for lead, pieces in views.present_note_lines(notes, w)]

    assert shape(marked) == shape(twin), w


def test_L0_cut_seat_k1_paints_lead_span_and_tag():
    """LLR-2901.2's seat: the one-row cut composes the plain (lead + pieces),
    cuts it to `w - vis(tag)` cells on a glyph boundary, rstrips, and paints
    the lead `mut`, the body piece by piece in its tones, the `… +N lines`
    tag `reached`."""
    notes = "- ==alpha== bravo charlie delta echo foxtrot golf hotel india juliet"
    rows = views.present_note_lines(notes, 30)
    assert len(rows) > 1
    cut = views._present_cut(rows, 1, 30, ())
    assert len(cut) == 1
    t = Text.from_markup(cut[0])
    spans = {(t.plain[s.start:s.end]): str(s.style) for s in t.spans}
    assert spans["• "] == HEX["mut"], spans
    assert spans["alpha"] == HEX["soon"], spans
    assert any(str(s.style) == HEX["ink"] and "bravo" in t.plain[s.start:s.end]
               for s in t.spans), spans
    assert any(str(s.style) == HEX["reached"] and f"+{len(rows) - 1} lines"
               in t.plain[s.start:s.end] for s in t.spans), spans
    assert views.vis(t.plain) == 30
    # the k >= len and k <= 0 paths keep their shapes
    assert views._present_cut(rows, 99, 30, ()) == \
        [views._present_note_markup(r, 30, ()) for r in rows]
    assert views._present_cut(rows, 0, 30, ()) == []
