"""The presentation's items of the backlog round.

Batch 2026-10-20-batch-03: HLR-2402 / LLR-2402.1 · TC-2402 · AT-2402 — the board's chip
on the hint row; HLR-2403 / LLR-2403.1, LLR-2403.2 · TC-2403 · AT-2403 — `?` and the
presentation's key seat; HLR-2404 / LLR-2404.1 · TC-2404 · AT-2404 — the view-3 export
without the cursor, cut to its content; HLR-2405 / LLR-2405.1 · TC-2405 · AT-2405 — `K`/`J`
(US-2402, US-2403). The round's boards (`backlog_round_fixture`), synthetic, under this
test's own home.
"""
from __future__ import annotations

import html
import re
from collections import defaultdict
from datetime import date
from pathlib import Path

import pytest

import backlog_round_fixture as fx
import multi_board_fixture as mb
from taskboard import app as app_module, keymap, models, modals, views
from taskboard.app import BoardsHome, PresentScreen, TaskboardApp
from taskboard.boards import peek_board
from taskboard.models import present_order

_TEXT = re.compile(r'<text [^>]*clip-path="url\(#[^)]*-line-(\d+)\)"[^>]*>([^<]*)</text>')


def svg_rows(svg: str) -> list[str]:
    """An exported SVG's text, row by row (qa QA-2): `&#160;` read as a space, the
    `<text>` pieces of each `line-N` joined; as many rows as the highest `line-N` + 1
    (Rich defines one clip path fewer than its rows — qa QA-3)."""
    rows: dict[int, list[str]] = defaultdict(list)
    for n, body in _TEXT.findall(svg):
        rows[int(n)].append(html.unescape(body).replace("\xa0", " "))
    top = max(rows) + 1 if rows else 0
    return ["".join(rows.get(i, [])) for i in range(top)]


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


@pytest.fixture
def png(monkeypatch):
    """The PNG rasteriser (headless Edge) stubbed: the suite has no Edge. Records the
    cells it was asked for — a declared seam (qa QA-16)."""
    asked = []

    def fake(svg_path, png_path, width, height):
        asked.append((width, height))
        return None
    monkeypatch.setattr(app_module, "save_present_png", fake)
    return asked


def _round(home, last="client-a"):
    from taskboard.__main__ import open_app
    fx.build(home, last=last)
    return open_app(None)


async def _press(pilot, *keys):
    for k in keys:
        await pilot.press(k)
        await pilot.pause()


def _plain(widget) -> str:
    c = widget.render()
    return c.plain if hasattr(c, "plain") else str(c)


def _hint(app) -> str:
    return _plain(app.screen.query_one("#present-hint"))


def _style_at(widget, needle: str) -> str:
    """The style the widget's Text gives the first cell of `needle`."""
    t = widget.content
    at = t.plain.index(needle)
    return next((str(s.style) for s in t.spans if s.start <= at < s.end), "")


def _frame(app) -> str:
    return _plain(app.screen.query_one("#present-frame"))


async def _present(pilot, app, *keys):
    if isinstance(app.screen, BoardsHome):
        await _press(pilot, "escape")
    await _press(pilot, "R", *keys)
    assert isinstance(app.screen, PresentScreen)


def _exports(home, suffix=".svg"):
    return sorted((home / "boards" / "client-a" / "reports").glob(f"present-*{suffix}"))


# --------------------------------------------------------------------------- #
# HLR-2402 — the chip on the hint row
# --------------------------------------------------------------------------- #
async def test_TC_2402_the_hint_opens_with_the_chip(home):
    """TC-2402: ` Client A ` bold on sky, then a space, then the hint fitted to what is
    left; a 30-character name cut to 24 cells; no label, no chip."""
    app = _round(home)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        await _present(pilot, app)
        scr = app.screen
        hint = scr._hint(118)
        assert hint.plain.startswith(" Client A  1 gantt"), hint.plain
        assert hint.cell_len <= 116
        span = next(s for s in hint.spans if "Client" in hint.plain[s.start:s.end])
        assert "bold" in str(span.style) and f"on {views.HEX['sky']}" in str(span.style)
        app.board.label = ("x" * 30, "sky")
        assert scr._hint(118).plain.startswith(" " + "x" * 23 + "…  1 gantt")
        app.board.label = None
        assert scr._hint(118).plain.startswith("1 gantt")
        assert "x" * 5 not in scr._frame_text().plain


async def test_AT_2402_the_presenter_reads_the_board_the_slide_never_does(home, png):
    """AT-2402 (US-2402): `R` on Client A — the hint row starts with the chip; the
    frame and both exports (views 1 and 3) never hold the board's name; one board,
    no chip."""
    app = _round(home)
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.pause()
        await _present(pilot, app)
        assert _hint(app).startswith(" Client A  1 gantt"), _hint(app)
        assert "Client A" not in _frame(app)
        await _press(pilot, "x")
        await _press(pilot, "3", "x")
    svgs = _exports(home)
    assert len(svgs) == 2, svgs
    for svg in svgs:
        assert not any("Client A" in r for r in svg_rows(svg.read_text(encoding="utf-8")))
    one = TaskboardApp(board_path=home / "one" / "board.json")
    async with one.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        await _present(pilot, one)
        assert _hint(one).startswith("1 gantt"), _hint(one)


# --------------------------------------------------------------------------- #
# HLR-2403 — `?` and the seat
# --------------------------------------------------------------------------- #
def _pairs(bindings) -> set:
    out = set()
    for b in bindings:
        for k in b.key.split(","):
            out.add((k.strip(), b.action))
    return out


#: the presentation's (key, action) pairs before the seat (batch 2026-10-19-batch-01, at
#: `fab1206`), literal: the seat must keep every one (code review CR-6)
OLD_PAIRS = {("escape", "close"), ("q", "close"), ("left", "side(-1)"), ("h", "side(-1)"),
             ("right", "side(1)"), ("l", "side(1)"), ("up", "move(-1)"), ("k", "move(-1)"),
             ("down", "move(1)"), ("j", "move(1)"), ("shift+up", "reorder(-1)"),
             ("shift+down", "reorder(1)"), ("enter", "fold"), ("x", "export"), ("space", "hide"),
             ("a", "show_all"), ("u", "hidden_picker"), ("1", "view(0)"), ("2", "view(1)"),
             ("3", "view(2)"), ("tab", "cycle(1)"), ("shift+tab", "cycle(-1)"),
             ("pagedown", "scroll(1)"), ("pageup", "scroll(-1)")}


@pytest.mark.parametrize("label", [("Client A", "sky"), ("y" * 30, "sky")])
def test_TC_2402_the_chip_never_costs_the_keys(tmp_path, label):
    """TC-2402 (code review CR-1, CR-2): with a chip, from 36 columns up the hint ends
    `? keys`, never wider than its row; view 3 from 100 columns takes the rail's
    wording (`←→ rail`) whatever the chip."""
    from test_present_all import _screen_all
    scr = _screen_all(tmp_path, 1)
    scr._board.label = label
    for w in range(36, 140):
        got = scr._hint(w)
        assert got.plain.endswith("  ? keys"), (w, got.plain)
        assert got.cell_len <= w - 2, (w, got.plain)
        if w >= 100 and "←→" in got.plain:
            assert "↑↓ ←→" in got.plain or "←→ rail" in got.plain, (w, got.plain)


def test_TC_2403_the_bindings_are_the_seat():
    """TC-2403: the presentation binds exactly the seat's (key, action) pairs, every
    one priority — nothing bound outside the seat, nothing in the seat unbound."""
    seat = set()
    for row in keymap.PRESENT_KEYS:
        for keys, action in row.binds:
            seat |= {(k.strip(), action) for k in keys.split(",")}
    assert _pairs(PresentScreen.BINDINGS) == seat
    assert OLD_PAIRS <= seat, OLD_PAIRS - seat
    assert all(b.priority for b in PresentScreen.BINDINGS)
    assert {("K", "reorder(-1)"), ("J", "reorder(1)"), ("question_mark", "keys")} <= seat


@pytest.mark.parametrize("view, live, dim", [("all", "⇧↑↓ K J", "pgdn pgup"),
                                             ("split", "pgdn pgup", "⇧↑↓ K J")])
def test_TC_2403_the_window_is_the_seat_live_by_view(view, live, dim):
    """TC-2403: every seat row's keys appear once; a row of the current view (or of
    every view) in the key style, another view's dimmed with its view named."""
    text = modals.PresentKeys(view).lines()
    for row in keymap.PRESENT_KEYS:
        assert text.plain.count(f"  {row.show:<10}{row.label}") == 1, row.show
    for keys, want in ((live, keymap.KEY_STYLE), (dim, views.HEX["dim"])):
        at = text.plain.index(f"  {keys}")
        style = next(str(s.style) for s in text.spans if s.start <= at + 2 < s.end)
        assert style == want, (keys, style)
    other = "split" if view == "all" else "all"
    assert f"({other})" in text.plain


async def test_AT_2403_question_mark_shows_every_key(home, png):
    """AT-2403 (US-2402): `?` in view 3 opens the keys window (view all), `?` closes it
    on the same frame; in view 1 the reorder row is another view's; `esc` closes; the
    window never reaches an export; at 118 and 80 every view's hint ends `? keys`."""
    app = _round(home)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        await _present(pilot, app, "3")
        before = _frame(app)
        await _press(pilot, "x")
        first = _exports(home)[0].read_bytes()
        await _press(pilot, "question_mark")
        assert isinstance(app.screen, modals.PresentKeys)
        text = _plain(app.screen.query_one("#pk-text"))
        for want in ("PRESENTATION KEYS · view all", "VIEWS", "MOVE", "CURATE", "OUT",
                     "⇧↑↓ K J   move a project up / down", "scroll the notes  (split)"):
            assert want in text, want
        pk = app.screen.query_one("#pk-text")
        assert _style_at(pk, "⇧↑↓ K J") == keymap.KEY_STYLE           # this view's: bright
        assert _style_at(pk, "pgdn pgup") == views.HEX["dim"]          # another view's: dim
        await _press(pilot, "question_mark")
        assert isinstance(app.screen, PresentScreen) and _frame(app) == before
        await _press(pilot, "x")
        assert _exports(home)[0].read_bytes() == first
        await _press(pilot, "1", "question_mark")
        text = _plain(app.screen.query_one("#pk-text"))
        assert "view gantt" in text and "move a project up / down  (all)" in text
        assert _style_at(app.screen.query_one("#pk-text"), "⇧↑↓ K J") == views.HEX["dim"]
        await _press(pilot, "escape")
        assert isinstance(app.screen, PresentScreen)
        for v in ("1", "2", "3"):
            await _press(pilot, v)
            assert _hint(app).rstrip().endswith("? keys"), _hint(app)
    app = _round(home / "small")
    async with app.run_test(size=(80, 24)) as pilot:
        await pilot.pause()
        await _present(pilot, app)
        for v in ("1", "2", "3"):
            await _press(pilot, v)
            assert _hint(app).rstrip().endswith("? keys"), _hint(app)


# --------------------------------------------------------------------------- #
# HLR-2404 — the clean export
# --------------------------------------------------------------------------- #
def test_TC_2404_the_export_has_no_cursor_and_ends_at_its_content(tmp_path):
    """TC-2404: Client A at 118×29 → 93 × 21, no `⟦`, no `project span`, the last row
    not blank; a folded project exports folded; a timeline that fills the frame keeps
    every row; an overflowing board anchored on its last project folds as the screen
    does with the cursor there."""
    fx.build(tmp_path, last="client-a")
    board = peek_board(fx.board_path(tmp_path, "client-a"))
    text, w, rows = views.present_all_export(board, fx.TODAY, 118, 29)
    assert (w, rows) == (93, 21)
    lines = text.plain.split("\n")
    assert len(lines) == 21 and lines[-1].strip()
    assert "⟦" not in text.plain and "project span" not in text.plain
    first = present_order(board)[0]
    folded, _w, frows = views.present_all_export(board, fx.TODAY, 118, 29, {first.id})
    assert frows < rows
    shown = [t.title for t in board.tasks if t.project_id == first.id and not board.is_done(t)]
    assert shown and not any(t in folded.plain for t in shown)
    mb.build(tmp_path / "mb", "main")
    big = peek_board(tmp_path / "mb" / "board.json")
    _t, _w, brows = views.present_all_export(big, mb.TODAY, 118, 29)
    assert brows == 29
    last = present_order(big)[-1].id
    shot, _w, _r = views.present_all_export(big, mb.TODAY, 118, 12, frozenset(), last)
    screen, _s, _c = views._all_timeline(big, 93, 12, mb.TODAY, ("proj", last), frozenset(),
                                          False)
    titles = [t.title for t in big.tasks]
    plain_screen = views.to_text(screen, len(screen), 93).plain
    assert ([t for t in titles if t in shot.plain]
            == [t for t in titles if t in plain_screen])


@pytest.mark.parametrize("size, width", [((118, 30), 93), ((80, 24), 80)])
async def test_AT_2404_the_export_reads_as_a_slide(home, png, size, width):
    """AT-2404 (US-2403): `R`, `3`, `x` on Client A writes 21 rows of text, neither
    `⟦` nor `project span`, every shown project's name; the rasteriser is asked for
    those cells; the screen keeps its cursor."""
    app = _round(home)
    async with app.run_test(size=size, notifications=True) as pilot:
        await pilot.pause()
        await _present(pilot, app, "3", "x")
        assert "⟦" in _frame(app)
    svg = home / "boards" / "client-a" / "reports" / "present-board-2026-10-20-all.svg"
    rows = svg_rows(svg.read_text(encoding="utf-8"))
    assert len(rows) == 21, len(rows)
    joined = "\n".join(rows)
    assert "⟦" not in joined and "project span" not in joined
    for name in ("Ingest & index", "Eval harness", "Pilot rollout"):
        assert name in joined, name
    assert png == [(width, 21)]


# --------------------------------------------------------------------------- #
# HLR-2405 — K / J
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("label", [None, ("Client A", "sky")])
async def test_TC_2405_the_hint_names_K_J(home, label):
    """TC-2405: view 3's hint names `K J` at every wording — `⇧↑↓/K J reorder` at 160,
    `K J order` at 118, `K J` at 80 — with and without the chip."""
    app = _round(home)
    async with app.run_test(size=(160, 45)) as pilot:
        await pilot.pause()
        await _present(pilot, app, "3")
        app.board.label = label
        scr = app.screen
        want = {160: "⇧↑↓/K J reorder", 118: "K J order", 80: "K J"} if label is None else \
            {160: "K J", 118: "K J", 80: "K J"}
        for w, text in want.items():
            assert text in scr._hint(w).plain, (w, scr._hint(w).plain)


def _rail(app) -> list[str]:
    """The rail's project names, top to bottom (view 3 from 100 columns)."""
    names = []
    for row in _frame(app).split("\n")[3:]:
        m = re.match(r"^.\s*\d+ [●○] (.+?)\s*│", row)
        if m:
            names.append(m.group(1).strip())
    return names


async def test_AT_2405_K_and_J_reorder(home):
    """AT-2405 (US-2402): `down`, `K` puts `Eval harness` first on the rail and in the
    file; `J` puts it back second; the hint names `K J` at 118 and at 80."""
    app = _round(home)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        await _present(pilot, app, "3")
        assert "K J" in _hint(app)
        start = _rail(app)
        await _press(pilot, "down", "K")
        rail = _rail(app)
        assert rail[0] == "Eval harness", rail
        disk = present_order(peek_board(fx.board_path(home, "client-a")))
        assert disk[0].name == "Eval harness"
        await _press(pilot, "J")
        assert _rail(app)[:2] == start[:2]
    small = _round(home / "small")
    async with small.run_test(size=(80, 24)) as pilot:
        await pilot.pause()
        await _present(pilot, small, "3")
        assert "K J" in _hint(small)
