"""The presentation at any width (batch 2026-10-18-batch-02, increment 002).

HLR-1903, HLR-1904 / LLR-1903.1, LLR-1904.1 · AT-1903, AT-1904 · TC-1903, TC-1904.

Why: a presenter's terminal can be narrowed at any moment (a split screen, a
small window). Below 36 columns the presentation's gantt field has no cell
left, and the renderer's own width assert killed the whole app. Now the frame
says how wide it must be — the number and the way out survive longest — and
nothing a key would do there can happen unseen: no key but `esc`/`q` acts, and
`x` says why it writes nothing. The hint row under the frame shortens in steps
and, when even its last wording does not fit, says it was cut with `…` instead
of being clipped silently by the widget.

The thresholds are literal tables, measured on the design before it was built
(`01-requirements.md` §2.7 P-7), never recomputed from the code under test.
"""
from __future__ import annotations

import pytest

import present_board as pb
import present_notes_board as nb
from taskboard import views
from taskboard.models import Board, Task
from test_present_views_app import _Presenting, _plain, frozen  # noqa: F401  (fixture)

MUT = views.HEX["mut"]

# the narrow frame's row 0, by width (LLR-1903.1's literal table)
RUNGS = [(0, ""), (1, "…"), (2, "3…")] + [(w, "36+") for w in range(3, 8)] \
    + [(w, "36+ cols") for w in range(8, 14)] + [(w, "needs 36+ cols") for w in range(14, 20)] \
    + [(w, "widen to 36+ columns") for w in range(20, 32)] \
    + [(w, "widen to 36+ columns · esc leave") for w in range(32, 36)]


def _boards(tmp_path) -> dict[str, Board]:
    """The two presentation boards, a board with no project, and the oracle
    board with every task of the presented project hidden."""
    empty = Board.load(str(tmp_path / "empty.json"))
    empty.projects.clear()
    empty.tasks.clear()
    hidden = pb.build(tmp_path / "hidden.json")
    for t in hidden.tasks:
        if t.project_id == pb.PROJECT_ID:
            t.show_in_present = False
    return {"present": pb.build(tmp_path / "p.json"), "notes": nb.build(tmp_path / "n.json"),
            "empty": empty, "hidden": hidden}


def test_TC_1903_every_width_renders_a_whole_frame(tmp_path):
    """TC-1903 (LLR-1903.1): every width below 36 and the boundary and operator
    widths above it (36, 37, 50, 79, 80, 99, 100, 118, 120) never raise; every frame is exactly
    `height` rows of `width` cells; below 36 it is the rung for that width in
    `mut`, the same for every view, cursor, scroll and board; from 36 the
    views' frame."""
    rungs = dict(RUNGS)
    wide = (36, 37, 50, 79, 80, 99, 100, 118, 120)      # the floor, the breakpoints, the operator sizes
    for name, board in _boards(tmp_path).items():
        for w in [*range(0, 36), *wide]:
            for h in (1, 5, 31):
                frames = set()
                for view in views.PRESENT_VIEWS:
                    for cursor in (pb.CURSOR, None):
                        for scroll in ((0, 3) if view == "split" else (0,)):
                            text = views.render_present(board, pb.PROJECT_ID, cursor, pb.TODAY,
                                                        w, h, view, scroll)
                            rows = text.plain.split("\n")
                            assert len(rows) == h, (name, w, h, view)
                            assert all(views.vis(r) == w for r in rows), (name, w, h, view, rows)
                            frames.add(text.plain)
                            if w < 36:
                                assert rows[0].rstrip() == rungs[w], (name, w, rows[0])
                                assert all(not r.strip() for r in rows[1:]), (name, w, rows)
                                if w:
                                    assert any(s.start == 0 and MUT in str(s.style)
                                               for s in text.spans), (w, text.spans)
                if w < 36:
                    assert len(frames) == 1, (name, w, h, frames)
    at36 = views.render_present(_boards(tmp_path)["present"], pb.PROJECT_ID, pb.CURSOR,
                                pb.TODAY, 36, 10).plain.split("\n")
    assert at36[0].startswith("◆ PRESENT"), at36[0]


# --------------------------------------------------------------------------- #
# The hint row
# --------------------------------------------------------------------------- #
# three view names and the `u` tail since batch 2026-10-19-batch-01 (LLR-2104.1)
NAMES2, NAMES1 = "1 gantt  2 split  3 all  ", "1 gantt 2 split 3 all "
WORDINGS = {
    "gantt": {"long": NAMES2 + "⇥ next · ←→ ↑↓ move · ␣ hide · a show all · x export · esc leave",
              "middle": NAMES2 + "⇥ next · ←→ ↑↓ · ␣ hide · a show all · x export · esc",
              "short": NAMES1 + "⇥ · ←→ · ␣ hide · a all · x export · esc",
              "compact": NAMES1 + "⇥ ←→ ␣ x esc",
              "esc": NAMES1 + "esc"},
    "split": {"long": NAMES2 + "pgdn notes · ⇥ next · ←→ ↑↓ move · ␣ hide · a show all · x export · esc leave",
              "middle": NAMES2 + "pgdn · ⇥ next · ←→ ↑↓ · ␣ hide · a show all · x export · esc",
              "short": NAMES1 + "pgdn · ⇥ · ←→ · ␣ hide · a all · x export · esc",
              "compact": NAMES1 + "pgdn ⇥ ←→ ␣ x esc",
              "esc": NAMES1 + "esc"},
}
# the first width each wording is painted at — since batch 2026-10-19-batch-01 the
# three view names and the `u` tail, measured with `rich.cells.cell_len` over the
# literal strings outside the code (`.dev-flow/2026-10-19-batch-01/evidence/
# hint-widths.txt`; before: P-7 of 2026-10-18-batch-02, P-3 of 2026-10-18-batch-03)
THRESHOLDS = {
    ("gantt", 0): {"compact": 36, "short": 64, "middle": 80, "long": 91},
    ("gantt", 1): {"esc": 36, "compact": 49, "short": 77, "middle": 93, "long": 104},
    ("gantt", 3): {"esc": 36, "compact": 49, "short": 77, "middle": 93, "long": 104},
    ("gantt", 10): {"esc": 36, "compact": 50, "short": 78, "middle": 94, "long": 105},
    ("split", 0): {"esc": 36, "compact": 41, "short": 71, "middle": 87, "long": 104},
    ("split", 1): {"esc": 36, "compact": 54, "short": 84, "middle": 100, "long": 117},
    ("split", 3): {"esc": 36, "compact": 54, "short": 84, "middle": 100, "long": 117},
    ("split", 10): {"esc": 36, "compact": 55, "short": 85, "middle": 101, "long": 118},
}


def _screen(tmp_path):
    """A `PresentScreen` (not mounted) on the oracle project grown to 12 tasks,
    so 10 can be hidden — a two-digit count."""
    from taskboard.app import PresentScreen
    b = pb.build(tmp_path / "h.json")
    for i in range(6):
        b.tasks.append(Task(f"Extra {i}", project_id=pb.PROJECT_ID, phase="Doing"))
    mine = [t for t in b.tasks if t.project_id == pb.PROJECT_ID]
    assert len(mine) == 12
    return PresentScreen(b, pb.PROJECT_ID, "Website", pb.CURSOR), mine


def _expected(view: str, hidden: int, w: int) -> str:
    tail = f" · u {hidden} hidden" if hidden else ""
    room = w - 2
    if room <= 0:
        return ""
    if w < 36:
        s = "esc leave" + (f" · {hidden} hidden" if hidden else "")
        return s if len(s) <= room else s[:room - 1] + "…"
    table = THRESHOLDS[(view, hidden)]
    tier = max((t for t, first in table.items() if first <= w), key=lambda t: table[t])
    s = WORDINGS[view][tier] + tail
    return s if len(s) <= room else s[:room - 1] + "…"    # none fits: the last, cut


def test_TC_1904_the_hint_takes_the_first_wording_that_fits(tmp_path):
    """TC-1904 (LLR-1904.1): over widths 1–140, both views, 0 / 1 / 3 / 10 hidden,
    the hint is the wording of the literal threshold table — never wider than
    its `w - 2` cells, never longer as the width shrinks — and below 36 only
    the way out and the hidden count, cut with `…`."""
    scr, mine = _screen(tmp_path)
    for vi, view in enumerate(views.PRESENT_VIEWS):
        scr._view = vi
        for hidden in (0, 1, 3, 10):
            for t in mine:
                t.show_in_present = True
            for t in mine[:hidden]:
                t.show_in_present = False
            prev = 0
            for w in range(1, 141):
                got = scr._hint(w).plain
                assert got == _expected(view, hidden, w), (view, hidden, w, got)
                assert views.vis(got) <= max(0, w - 2), (view, hidden, w, got)
                assert views.vis(got) >= prev or w == 36, (view, hidden, w)   # 35→36 swaps branch
                prev = views.vis(got)


def test_TC_1904_the_current_view_is_bold_and_bright(tmp_path):
    """TC-1904 (LLR-1904.1): the current view's name is bold `#e6edf7`, the
    other `#5b6675`, at every wording that shows the names."""
    scr, _ = _screen(tmp_path)
    for vi in (0, 1):
        scr._view = vi
        for w in (118, 80, 50, 36):
            hint = scr._hint(w)
            plain = hint.plain
            for i, name in enumerate(views.PRESENT_VIEWS):
                at = plain.index(f"{i + 1} {name}")
                styles = [str(s.style) for s in hint.spans if s.start <= at < s.end]
                want = "bold #e6edf7" if i == vi else "#5b6675"
                assert want in styles, (vi, w, name, styles)


def test_TC_1904_an_overflowing_count_is_cut_visibly(tmp_path, monkeypatch):
    """TC-1904 (PC-2): no wording can fit a six-digit hidden count at 36
    columns — the last is cut to the row with `…`, never painted wider."""
    from taskboard import app as app_module
    scr, _ = _screen(tmp_path)
    monkeypatch.setattr(app_module, "present_hidden", lambda board, pid: list(range(123456)))
    got = scr._hint(36).plain
    assert views.vis(got) == 34 and got.endswith("…"), got
    assert got.startswith("1 gantt 2 split 3 all esc · u 12"), got


# --------------------------------------------------------------------------- #
# Through the real app
# --------------------------------------------------------------------------- #
LADDER = [(60, None), (40, None), (36, None), (35, "widen to 36+ columns · esc leave"),
          (32, "widen to 36+ columns · esc leave"), (30, "widen to 36+ columns"),
          (20, "widen to 36+ columns"), (14, "needs 36+ cols"), (8, "36+ cols"),
          (5, "36+"), (3, "36+"), (1, "…")]


async def test_AT_1903_narrowed_the_presentation_says_how_wide_and_waits(tmp_path, monkeypatch, frozen):
    """AT-1903 (US-1902, HLR-1903): `R` at 118×31, the cursor moved, a task
    hidden, the split view; narrowed step by step to 1 column the app keeps the
    presentation, the frame names the width it needs; at 30 columns no key
    changes anything and `x` writes nothing and says why; widened again, the
    frame is the one before the narrowing."""
    s = _Presenting(tmp_path, monkeypatch, (118, 31))
    notes = []
    async with s.app.run_test(size=s.size) as pilot:
        await s.open(pilot)
        s.app.notify = lambda message, **k: notes.append(str(message))
        await s.press(pilot, "right", "space", "2")
        kept = s.frame()
        saves = len(s.saves)
        assert saves == 1 and "  split " in s.rows()[0]
        for w, rung in LADDER:
            await pilot.resize_terminal(w, 12)
            await pilot.pause()
            await pilot.pause()
            assert type(s.app.screen).__name__ == "PresentScreen", w
            rows = s.rows()
            if rung is None:
                assert rows[0].startswith("◆ PRESENT"), (w, rows[0])
            else:
                assert rows[0].strip() == rung, (w, rows[0])
                assert all(not r.strip() for r in rows[1:]), (w, rows)
            if w == 30:
                # each key would change the kept frame if it acted: `tab` the view,
                # `right` the cursor, `space`/`a` the hidden set (pairs such as
                # `tab` + `1` or `right` + `h` would undo each other unseen);
                # `1`, `shift+tab` and `h` reach the same guarded actions
                for key in ("tab", "right", "pagedown", "pageup", "space", "a", "x"):
                    await s.press(pilot, key)
                    assert s.rows()[0].strip() == rung, (key, s.rows()[0])
                assert len(s.saves) == saves, "a key below 36 wrote the board"
                assert not (tmp_path / "reports").exists(), "x below 36 wrote a file"
                assert notes == ["Widen the terminal to 36+ columns to export"], notes
        await pilot.resize_terminal(118, 31)
        await pilot.pause()
        await pilot.pause()
        assert s.frame() == kept


async def test_AT_1904_the_hint_shortens_and_cuts_visibly(tmp_path, monkeypatch, frozen):
    """AT-1904 (US-1902, HLR-1904): three tasks hidden; at 50 columns the
    compact wording in both views, at 40 the view switch and `esc`, below 36
    only the way out and the count, cut with `…` at 15 — never wider than the
    row, the current view bold."""
    s = _Presenting(tmp_path, monkeypatch, (118, 31))
    async with s.app.run_test(size=s.size) as pilot:
        await s.open(pilot)
        await s.press(pilot, "space", "space", "space")
        hint = lambda: s.app.screen.query_one("#present-hint").content  # noqa: E731

        async def at(w, h):
            await pilot.resize_terminal(w, h)
            await pilot.pause()
            await pilot.pause()
            text = _plain(s.app.screen.query_one("#present-hint")).strip()
            assert views.vis(text) <= w - 2, (w, text)
            return text

        assert await at(50, 20) == "1 gantt 2 split 3 all ⇥ ←→ ␣ x esc · u 3 hidden"
        styles = [str(sp.style) for sp in hint().spans if sp.start == 0]
        assert "bold #e6edf7" in styles, styles
        await s.press(pilot, "2")
        assert s.hint() == "1 gantt 2 split 3 all esc · u 3 hidden"   # compact needs 54
        assert await at(40, 20) == "1 gantt 2 split 3 all esc · u 3 hidden"
        at_split = [str(sp.style) for sp in hint().spans if sp.start == len("1 gantt ")]
        assert "bold #e6edf7" in at_split, at_split
        assert await at(30, 12) == "esc leave · 3 hidden"
        assert await at(15, 10) == "esc leave · …"
