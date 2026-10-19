"""The presentation polish the operator approved (batch 2026-10-18-batch-03).

HLR-2001..HLR-2003 / LLR-2001.1..LLR-2003.1 · AT-2001..AT-2003 · TC-2001..TC-2003.

Why: on 2026-10-18 the operator approved («Si, apruebo.») variant A of the three
items of the prototype round `prototypes/backlog_polish/`. These tests hold the
shipped presentation to what that round showed, for the reason each item exists:

1. The view word and the marks that say a note or a column was cut were `dim`
   (3.25:1 on the presentation's background) and vanish on a projector; they are
   now `reached` (4.87:1) — above the 4.5:1 reading floor, yet below `mut`, so
   they still do not compete with the titles and dates. The contrast is computed
   here from the colours, never read from the code under test.
2. At 80 columns the hint row fell to its short wording with ~20 cells to spare,
   losing `next` and `show all` — the two keys a first-time presenter does not
   guess. A middle wording, the long one's vocabulary and order without its
   longest words, now sits between the long and the short one. Its widths are
   the ones measured on the design before it was built (P-3).
3. The gantt view kept the cursor's note to 3 rows with 6 (80x25) to 12
   (118x31) rows empty below it; the presenter had to switch views to talk from
   the note. The note now takes every free row (3 at least) and still declares
   its cut. The frames it is held to are the round's own variant-A output on the
   base tree (`evidence/frames/gen_frames.py`), not this batch's renderer.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

import present_board as pb
import present_notes_board as nb
from taskboard import views
from test_present_views_app import _Presenting, frozen  # noqa: F401  (fixture)

BACKGROUND = "#0d1117"          # PresentScreen's background (app.py DEFAULT_CSS)
DIM, REACHED, MUT = views.HEX["dim"], views.HEX["reached"], views.HEX["mut"]
# the quiet marks: the cut marks, the edge marks of a paged window
MARKS = re.compile(r"… \+\d+ lines|↑ \d+ lines above|↓ \d+ more lines")
# the dim marks that stay dim: the note lead, the separators, `no notes`, the overflow row
STAY_DIM = re.compile(r"  · |no notes|\+\d+ more rows not shown")


def _contrast(fg: str, bg: str = BACKGROUND) -> float:
    """The WCAG 2 contrast ratio of two `#rrggbb` colours."""
    def lum(h: str) -> float:
        rgb = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
        lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
        return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]
    hi, lo = sorted((lum(fg), lum(bg)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def _styles_at(text, at: int) -> str:
    return " ".join(str(s.style) for s in text.spans if s.start <= at < s.end)


def _view_word_at(text) -> int:
    head = text.plain.split("\n")[0]
    m = re.search(r"  (gantt|split) ", head)
    assert m, head
    return m.start(1)


# --------------------------------------------------------------------------- #
# TC-2001 — the four tone sites (LLR-2001.1)
# --------------------------------------------------------------------------- #
def test_TC_2001_the_quiet_marks_are_reached_and_the_rest_stays_dim(tmp_path):
    """TC-2001 (LLR-2001.1): over both presentation boards, both views, the
    operator and breakpoint widths, three heights, every open task as cursor and
    three pages: every view word, cut mark and edge mark is painted `reached`
    and never `dim` (the view word wherever the header keeps its tones — a
    title too wide for its row is painted whole in bold `bright`, `header()`);
    the note lead, `no notes` and the overflow row stay `dim`. The sweep must meet every kind of mark at least once."""
    seen = set()
    for name, build in (("present", pb.build), ("notes", nb.build)):
        board = build(tmp_path / f"{name}.json")
        cursors = [t.id for t in views.present_tasks(board, pb.PROJECT_ID)[0]]
        for w in (36, 60, 80, 100, 118):
            for h in (12, 20, 24, 30):
                for view in views.PRESENT_VIEWS:
                    for cur in cursors:
                        for scroll in ((0, 1, 3) if view == "split" else (0,)):
                            text = views.render_present(board, pb.PROJECT_ID, cur, pb.TODAY,
                                                        w, h, view, scroll)
                            at = _view_word_at(text)
                            # the header keeps its tones (header(): vis(title) + 2 <= width; the
                            # view word ends the title, so this is that rule, read off the row)
                            if at + len(view) + 2 <= w:
                                assert REACHED in _styles_at(text, at), (name, w, h, view)
                                assert DIM not in _styles_at(text, at), (name, w, h, view)
                                seen.add("word")
                            for m in MARKS.finditer(text.plain):
                                st = _styles_at(text, m.start())
                                assert REACHED in st and DIM not in st, (name, w, h, view, m[0], st)
                                seen.add({"…": "cut", "↑": "up", "↓": "down"}[m[0][0]])
                            for m in STAY_DIM.finditer(text.plain):
                                i = m.start() + (2 if m[0].startswith("  ·") else 0)
                                st = _styles_at(text, i)
                                assert DIM in st, (name, w, h, view, m[0], st)
                                seen.add(m[0].strip()[0])
    assert seen == {"word", "cut", "up", "down", "·", "n", "+"}, seen


def test_TC_2001_a_one_row_cut_is_reached(tmp_path):
    """TC-2001 (LLR-2001.1, boundary): a note kept to one row in the split view
    (60x20) carries ` … +N lines` beside its first line — that tag is `reached`."""
    board = nb.build(tmp_path / "board.json")
    text = views.render_present(board, pb.PROJECT_ID, pb.CURSOR, pb.TODAY, 60, 20, "split")
    tags = [m for m in re.finditer(r"\S … \+\d+ lines", text.plain)]
    assert tags, text.plain
    for m in tags:
        st = _styles_at(text, m.start() + 2)
        assert REACHED in st and DIM not in st, (m[0], st)


def test_TC_2001_no_project_to_present_stays_dim(tmp_path):
    """TC-2001 (LLR-2001.1): the empty-board line is not a quiet mark of a
    frame — it is out of the verdict's scope and stays `dim`."""
    from taskboard.models import Board
    empty = Board.load(str(tmp_path / "empty.json"))
    empty.projects.clear()
    empty.tasks.clear()
    text = views.render_present(empty, None, None, pb.TODAY, 80, 10)
    assert text.plain.startswith("no project to present"), text.plain
    assert DIM in _styles_at(text, 0)


def test_TC_2001_reached_reads_on_a_projector_and_stays_below_the_text():
    """TC-2001 (HLR-2001's why): the new tone clears the 4.5:1 reading floor the
    old one missed, and stays quieter than `mut`, the secondary text's tone."""
    assert _contrast(DIM) < 4.5 <= _contrast(REACHED) < _contrast(MUT)


# --------------------------------------------------------------------------- #
# AT-2001 — the presenter sees the marks in `reached` (HLR-2001)
# --------------------------------------------------------------------------- #
async def test_AT_2001_the_quiet_marks_read_in_the_running_app(tmp_path, monkeypatch, frozen):
    """AT-2001 (HLR-2001): the app at 80x25, `R`, `→ →` (the long note under
    the cursor, cut): the header's `gantt` and the `… +N lines` are `#7a828c`,
    the `· ` lead stays `#5b6675`; `2`: the split view's word and every cut and
    edge mark are `#7a828c` too, `pgdn` paging the
    cursor's note so its `↑`/`↓` edge marks show."""
    s = _Presenting(tmp_path, monkeypatch, (80, 25))
    async with s.app.run_test(size=s.size) as pilot:
        await s.open(pilot)
        await s.press(pilot, "right", "right")
        frame = s.app.screen.query_one("#present-frame").content
        assert "#7a828c" in _styles_at(frame, _view_word_at(frame))
        assert "#5b6675" not in _styles_at(frame, _view_word_at(frame))
        cuts = list(MARKS.finditer(frame.plain))
        assert cuts, frame.plain
        for m in cuts:
            assert "#7a828c" in _styles_at(frame, m.start()), m[0]
            assert "#5b6675" not in _styles_at(frame, m.start()), m[0]
        lead = frame.plain.index("\n  · ") + 3
        assert "#5b6675" in _styles_at(frame, lead)

        await s.press(pilot, "2")
        frame = s.app.screen.query_one("#present-frame").content
        assert frame.plain.split("\n")[0].count("  split ") == 1
        assert "#7a828c" in _styles_at(frame, _view_word_at(frame))
        assert "#5b6675" not in _styles_at(frame, _view_word_at(frame))
        await s.press(pilot, "pagedown")          # the cursor's note pages: its edge marks show
        frame = s.app.screen.query_one("#present-frame").content
        marks = list(MARKS.finditer(frame.plain))
        assert any(m[0][0] in "↑↓" for m in marks), frame.plain
        for m in marks:
            assert "#7a828c" in _styles_at(frame, m.start()), m[0]
            assert "#5b6675" not in _styles_at(frame, m.start()), m[0]


# --------------------------------------------------------------------------- #
# TC-2002 — the middle wording (LLR-2002.1)
# --------------------------------------------------------------------------- #
MIDDLE = "⇥ next · ←→ ↑↓ · ␣ hide · a show all · x export · esc"
SHORT = "⇥ · ←→ · ␣ hide · a all · x export · esc"
LONG = "⇥ next · ←→ ↑↓ move · ␣ hide · a show all · x export · esc leave"
# the first width the middle wording is painted at, and the long one (P-3, measured on the
# design before it was built — never recomputed from the code under test)
MIDDLE_FIRST = {("gantt", 0): (73, 84), ("gantt", 1): (84, 95), ("gantt", 3): (84, 95),
                ("gantt", 10): (85, 96), ("split", 0): (80, 97), ("split", 1): (91, 108),
                ("split", 3): (91, 108), ("split", 10): (92, 109)}


@pytest.mark.parametrize("view, hidden", sorted(MIDDLE_FIRST))
def test_TC_2002_the_middle_wording_sits_between_the_long_and_the_short(tmp_path, view, hidden):
    """TC-2002 (LLR-2002.1): at the middle wording's first width the hint is the
    middle wording with two-space gaps, one column narrower it is the short one,
    and at the long wording's first width the long one — for both views and
    0 / 1 / 3 / 10 hidden; never wider than the row."""
    from test_present_narrow import _screen
    scr, mine = _screen(tmp_path)
    scr._view = views.PRESENT_VIEWS.index(view)
    for t in mine[:hidden]:
        t.show_in_present = False
    pg = view == "split"
    tail = f" · {hidden} hidden" if hidden else ""
    first, long_first = MIDDLE_FIRST[(view, hidden)]
    middle = "1 gantt  2 split  " + ("pgdn · " if pg else "") + MIDDLE + tail
    short = "1 gantt 2 split " + ("pgdn · " if pg else "") + SHORT + tail
    long_ = "1 gantt  2 split  " + ("pgdn notes · " if pg else "") + LONG + tail
    assert scr._hint(first).plain == middle
    assert scr._hint(long_first - 1).plain == middle
    assert scr._hint(first - 1).plain == short
    assert scr._hint(long_first).plain == long_
    for w in (first - 1, first, long_first - 1, long_first):
        assert views.vis(scr._hint(w).plain) <= w - 2, (view, hidden, w)


# --------------------------------------------------------------------------- #
# AT-2002 — at 80 columns the hint names next and show all (HLR-2002)
# --------------------------------------------------------------------------- #
async def test_AT_2002_the_80_column_hint_names_next_and_show_all(tmp_path, monkeypatch, frozen):
    """AT-2002 (HLR-2002): the app at 80x25, `R`: the hint row reads the middle
    wording — `next` and `show all`, the two keys a first-time presenter does
    not guess — the current view bold; `2`: the split view's middle wording,
    exactly the 78 cells the row holds; `space` (one hidden): the count no
    longer leaves room, the short wording as shipped; at 118x31 the long one."""
    s = _Presenting(tmp_path, monkeypatch, (80, 25))
    async with s.app.run_test(size=s.size) as pilot:
        await s.open(pilot)
        assert s.hint() == "1 gantt  2 split  " + MIDDLE
        assert "next" in s.hint() and "show all" in s.hint()
        hint = s.app.screen.query_one("#present-hint").content
        assert "bold #e6edf7" in _styles_at(hint, hint.plain.index("1 gantt"))
        await s.press(pilot, "2")
        assert s.hint() == "1 gantt  2 split  pgdn · " + MIDDLE
        assert views.vis(s.hint()) == 78
        await s.press(pilot, "space")
        assert s.hint() == "1 gantt 2 split pgdn · " + SHORT + " · 1 hidden"
    s = _Presenting(tmp_path, monkeypatch, (118, 31))
    async with s.app.run_test(size=s.size) as pilot:
        await s.open(pilot)
        assert s.hint() == "1 gantt  2 split  " + LONG


# --------------------------------------------------------------------------- #
# TC-2003 — the gantt note fills the free rows (LLR-2003.1)
# --------------------------------------------------------------------------- #
FRAMES = Path(__file__).resolve().parents[1] / ".dev-flow" / "2026-10-18-batch-03" / "evidence" / "frames"


def _v4(name: str) -> list[str]:
    """A PRES-V4 frame: the round's own `cap_fork("fill")` output on base_ref
    (`evidence/frames/gen_frames.py`), not this batch's renderer."""
    return (FRAMES / name).read_text(encoding="utf-8").splitlines()


@pytest.mark.parametrize("w, h", [(118, 30), (80, 24)])
def test_TC_2003_the_long_note_equals_the_rounds_frame(tmp_path, w, h):
    """TC-2003 (LLR-2003.1): the long note under the cursor, at both operator
    sizes, equals the round's variant-A frame row for row."""
    b = nb.build(tmp_path / "board.json")
    rows = views.render_present(b, pb.PROJECT_ID, nb.LONG, pb.TODAY, w, h, "gantt").plain.split("\n")
    assert rows == _v4(f"PRES-V4-gantt-notes-{w}x{h}.txt")


def test_TC_2003_the_note_takes_every_free_row_and_declares_its_cut(tmp_path):
    """TC-2003 (LLR-2003.1): over both boards, every open task as cursor, six
    widths and seven heights, plus one free row (`L + 1`) and, for a note of 4+
    rows, the room equal to the note and one row short: the frame is `height`
    rows; where the frame holds the 3-row floor the note shows
    `min(n, max(3, height - L))` rows (`L` the rows that are not the note) and
    nothing overflows — a cut note leaves no blank row and ends on
    `· … +N lines` counting what it hides; where it does not, the shipped
    `+N more rows not shown` closes the frame. The expectation is counted from
    the fixture's notes and the frame's own other rows, never from the
    renderer's cap."""
    seen = set()
    for name, build in (("present", pb.build), ("notes", nb.build)):
        board = build(tmp_path / f"{name}.json")
        open_t = views.present_tasks(board, pb.PROJECT_ID)[0]
        L = 1 + 2 + 1 + len(open_t) + 1 + len(open_t)      # header, ruler, span, tasks, rule, briefs
        for t in open_t:
            for w in (36, 50, 80, 100, 118, 140):
                n = len(views.present_note_lines(t.notes, w - 6))
                exact = {L + n, L + n - 1} if n > 3 else set()   # the room equal to the note, one short
                for h in sorted({5, 12, 20, 24, 30, 40, 60, L + 1} | exact):    # L + 1: one free row
                    rows = views.render_present(board, pb.PROJECT_ID, t.id, pb.TODAY, w, h,
                                                "gantt").plain.split("\n")
                    assert len(rows) == h, (name, t.id, w, h)
                    if h < L + min(n, 3):                            # the floor overflows, as shipped
                        assert re.search(r"\+\d+ more rows not shown", rows[-1]), rows[-1]
                        seen.add("overflow")
                        continue
                    want = min(n, max(3, h - L))
                    note = [r for r in rows if r.startswith("  · ")]
                    assert len(note) == want, (name, t.id, w, h, len(note), want)
                    assert not any("more rows not shown" in r for r in rows), (name, t.id, w, h)
                    if want < n:
                        assert note[-1].rstrip() == f"  · … +{n - want + 1} lines", note[-1]
                        assert all(r.strip() for r in rows), (name, t.id, w, h)
                        seen.add("cut")
                    if h == L + n:
                        assert note[-1].rstrip() != "" and "… +" not in note[-1], note
                        assert all(r.strip() for r in rows), (name, t.id, w, h)
                        seen.add("exact")
                    if h == L + n - 1:
                        assert note[-1].rstrip() == "  · … +2 lines", note
                        seen.add("one short")
    assert seen == {"overflow", "cut", "exact", "one short"}, seen


def test_TC_2003_no_cursor_note_without_a_cursor_or_notes(tmp_path):
    """TC-2003 (LLR-2003.1, empty): a cursor task with no notes, and a project
    with no shown open task (so no cursor), paint no note row however many rows
    are free."""
    b = nb.build(tmp_path / "board.json")
    bare = next(t for t in views.present_tasks(b, pb.PROJECT_ID)[0] if not t.notes.strip())
    rows = views.render_present(b, pb.PROJECT_ID, bare.id, pb.TODAY, 118, 60, "gantt").plain.split("\n")
    assert not [r for r in rows if r.startswith("  · ")], rows
    for t in b.tasks:
        if t.project_id == pb.PROJECT_ID:
            t.show_in_present = False
    rows = views.render_present(b, pb.PROJECT_ID, nb.LONG, pb.TODAY, 118, 60, "gantt").plain.split("\n")
    assert not [r for r in rows if r.startswith("  · ")], rows
    assert "◆ PRESENT" in rows[0] and not views.present_tasks(b, pb.PROJECT_ID)[0], rows[0]


# --------------------------------------------------------------------------- #
# AT-2003 — the presenter talks from the whole note (HLR-2003)
# --------------------------------------------------------------------------- #
async def test_AT_2003_the_gantt_note_runs_to_the_bottom_of_the_frame(tmp_path, monkeypatch, frozen):
    """AT-2003 (HLR-2003): the app at 80x25, `R`, `→ →` (the long note under the
    cursor): the frame is the round's variant-A frame — the note runs on to the
    last free row and ends on `… +5 lines`, the next brief closes the frame, no
    row is blank; at 118x31 the same note shows whole, no cut mark."""
    for size, name in (((80, 25), "PRES-V4-gantt-notes-80x24.txt"),
                       ((118, 31), "PRES-V4-gantt-notes-118x30.txt")):
        (tmp_path / f"{size[0]}").mkdir()
        s = _Presenting(tmp_path / f"{size[0]}", monkeypatch, size)
        async with s.app.run_test(size=s.size) as pilot:
            await s.open(pilot)
            await s.press(pilot, "right", "right")
            rows = s.rows()
            assert rows == _v4(name), size
            if size[0] == 80:
                assert all(r.strip() for r in rows), rows
                assert rows[-2].rstrip() == "  · … +5 lines" and "SEO redirects map" in rows[-1]
            else:
                assert "… +" not in "\n".join(rows)
