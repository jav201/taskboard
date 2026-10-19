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
