"""Present v3 through the real app (batch 2026-10-18-batch-01, increment 002).

HLR-1801, HLR-1802, HLR-1803 / LLR-1803.1, LLR-1803.2, LLR-1803.3 ·
AT-1801, AT-1802, AT-1803 · TC-1808, TC-1809.

Why: the presenter switches between the timeline and the task text while the
room watches, so the switch must be one key, must never leave the room on a
half-state (the cursor and the hidden tasks are the same in both views), must
not fire the board's own `1`/`2`/`tab` behind the presentation, and must never
paint a key in the frame — the frame is what the room sees and what `x`
exports. `R` always opens on the gantt view, and the presentation still writes
nothing but the "show in presentation" flag.

Every arm presses real keys through `run_test`'s pilot on a synthetic board
saved to `tmp_path` (`tests/present_notes_board.py`).
"""
from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

import present_board as pb
import present_notes_board as nb
from taskboard import views
from taskboard.models import Board

ROOT = Path(__file__).resolve().parents[1]
FRAMES = ROOT / ".dev-flow" / "2026-10-18-batch-01" / "evidence" / "frames"
FRAMES_V4 = ROOT / ".dev-flow" / "2026-10-18-batch-03" / "evidence" / "frames"   # gantt notes since then
KEY_WORDS = ("pgdn", "⇥", "1 gantt", "2 split", "esc", "x export", "hide")


class _Today(date):
    @classmethod
    def today(cls):
        return pb.TODAY


@pytest.fixture
def frozen(monkeypatch):
    """The house seam (`tests/test_present.py`): the screen and the startup
    sweep both read the frozen day."""
    from taskboard import app as app_module
    from taskboard import models

    monkeypatch.setattr(app_module, "date", _Today)
    monkeypatch.setattr(models, "date", _Today)


def _frame(name: str) -> list[str]:
    return (FRAMES / name).read_text(encoding="utf-8").splitlines()


def _plain(widget) -> str:
    content = widget.content
    return content.plain if hasattr(content, "plain") else str(content)


class _Presenting:
    """The app on the notes board saved to disk; saves counted (each still
    writes the file)."""

    def __init__(self, tmp_path, monkeypatch, size=(118, 31)):
        self.path = tmp_path / "board.json"
        nb.build(self.path).save()
        self.saves = []
        real = Board.save

        def counted(board):
            self.saves.append(1)
            real(board)
        monkeypatch.setattr(Board, "save", counted)
        from taskboard.app import TaskboardApp
        self.app = TaskboardApp(board_path=str(self.path))
        self.size = size

    async def open(self, pilot, cursor=nb.CURSOR):
        app = self.app
        for _ in range(50):
            if type(app.screen).__name__ == "MilestoneOffer":
                break
            await pilot.pause()
        app.selected_task_id = cursor
        self.saves.clear()                    # what mounting wrote is not the presentation's
        await pilot.press("R")
        await pilot.pause()
        assert type(app.screen).__name__ == "PresentScreen"

    async def press(self, pilot, *keys):
        for k in keys:
            await pilot.press(k)
        await pilot.pause()

    def rows(self) -> list[str]:
        return _plain(self.app.screen.query_one("#present-frame")).split("\n")

    def frame(self) -> str:
        return "\n".join(self.rows())

    def hint(self) -> str:
        return _plain(self.app.screen.query_one("#present-hint")).strip()


TITLES = {"tw2": "Build component library", "tw3": "Fix checkout 500 error",
          "tw4": "Optimize image assets", "tw5": "Launch new homepage",
          "tw6": "SEO redirects map"}      # the fixture's open tasks, gantt order


def _noted_first_words() -> dict[str, str]:
    """From the fixture, not from the app: each open task with notes (every
    task of the notes board is shown) -> its note's first words."""
    out = {}
    for tid, notes in nb.NOTES.items():
        if notes.strip():
            line = next(ln.strip() for ln in notes.splitlines() if ln.strip())
            out[tid] = line.lstrip("-*• ")[:14]
    return out


# --------------------------------------------------------------------------- #
# AT-1801 — `2` shows every shown open task's notes at once
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("size, name", [((118, 31), "PRES-V3-split-118x30.txt"),
                                        ((80, 25), "PRES-V3-split-80x24.txt")])
async def test_AT_1801_2_shows_every_task_text_at_once(tmp_path, monkeypatch, frozen,
                                                       size, name):
    """AT-1801 (US-1801, HLR-1801): `R` then `2` paints the split frame — the
    gantt rows on top and, below, text from EVERY shown open task that has
    notes, at the same time (the operator: «que todas se vieran al mismo
    tiempo»); the painted rows equal the PRES-V3 split frame; moving the
    cursor keeps every note on screen and accents the new cursor's block."""
    s = _Presenting(tmp_path, monkeypatch, size)
    async with s.app.run_test(size=s.size) as pilot:
        await s.open(pilot)
        await s.press(pilot, "2")
        assert s.rows() == _frame(name)
        words = _noted_first_words()
        assert len(words) == 4, words
        for cursor in ("tw3", "tw4", "tw5", "tw6", "tw6"):
            text = s.frame()
            for tid, w in words.items():
                assert w in text, (size, cursor, tid, w)
            assert "no notes" in text
            accented = [r for r in s.rows()[10:] if "▌ " + TITLES[cursor] in r]
            assert accented, (size, cursor)
            await s.press(pilot, "right")
        assert s.saves == []


# --------------------------------------------------------------------------- #
# AT-1802 — the gantt view keeps the note's line breaks
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("size, name", [((118, 31), "PRES-V4-gantt-notes-118x30.txt"),
                                        ((80, 25), "PRES-V4-gantt-notes-80x24.txt")])
async def test_AT_1802_the_gantt_note_keeps_its_line_breaks(tmp_path, monkeypatch, frozen,
                                                            size, name):
    """AT-1802 (US-1802, HLR-1802): `R` opens on the gantt view; the cursor moved
    onto `Launch new homepage` expands its note with its line breaks kept —
    `1. Feature-flag …` starts its own row, never `Sep 22. 1. Feature-flag` —
    and the painted rows equal the gantt-notes frame — since batch
    2026-10-18-batch-03 (LLR-2003.1, the note fills the free rows) that
    batch's PRES-V4 frame; the PRES-V3 files stay as recorded."""
    s = _Presenting(tmp_path, monkeypatch, size)
    async with s.app.run_test(size=s.size) as pilot:
        await s.open(pilot)
        assert s.rows()[0].startswith("◆ PRESENT · Website Redesign  gantt ")
        await s.press(pilot, "right", "right")
        assert s.rows() == (FRAMES_V4 / name).read_text(encoding="utf-8").splitlines()
        assert any(r.startswith("  · 1. Feature-flag") for r in s.rows())
        assert "Sep 22. 1." not in s.frame()


# --------------------------------------------------------------------------- #
# AT-1803 — the keys: switch, share, scroll, export, leave
# --------------------------------------------------------------------------- #
async def test_AT_1803_the_view_keys_and_what_the_views_share(tmp_path, monkeypatch, frozen):
    """AT-1803 (US-1803, HLR-1803): `2` / `1` / `tab` / `shift+tab` switch the
    view and never reach the board behind (its view stays, no add-task editor,
    the presentation stays open); the cursor moved in one view is the cursor in
    the other; `space` in the split view hides the task from both; `pgdn`
    scrolls the cut cursor note and `pgup` brings it back; `x` exports the
    current view's frame with no key in it; `esc` leaves, and `R` again opens
    on the gantt view; only `space` / `a` wrote the board."""
    s = _Presenting(tmp_path, monkeypatch, (80, 25))
    async with s.app.run_test(size=s.size) as pilot:
        board_view = s.app.view_mode
        await s.open(pilot)
        head = lambda: s.rows()[0]                                  # noqa: E731
        assert "  gantt " in head()
        await s.press(pilot, "2")
        assert "  split " in head()
        await s.press(pilot, "tab")                 # three views since 2026-10-19-batch-01
        assert "  all " in head()
        await s.press(pilot, "tab")
        assert "  gantt " in head()
        await s.press(pilot, "shift+tab")
        assert "  all " in head()
        await s.press(pilot, "shift+tab")
        assert "  split " in head()
        await s.press(pilot, "tab", "tab", "tab")
        assert "  split " in head()
        await s.press(pilot, "1")
        assert "  gantt " in head()
        assert type(s.app.screen).__name__ == "PresentScreen"
        assert s.app.view_mode == board_view

        # the cursor is shared: moved in split, it is the gantt view's cursor
        await s.press(pilot, "2", "right", "right")                # -> Launch new homepage
        split_rows = s.rows()
        assert any(r.startswith(" ▌ Launch new homepage") for r in split_rows), split_rows
        await s.press(pilot, "1")
        assert "⟦Launch new homepage⟧" in s.frame()

        # pgdn scrolls the cut cursor note (split), pgup brings it back
        await s.press(pilot, "2")
        top = s.frame()
        await s.press(pilot, "pagedown")
        assert "lines above" in s.frame()
        assert s.frame() != top
        await s.press(pilot, "pageup")
        assert s.frame() == top
        for _ in range(12):                                        # past the end: no dead pages
            await s.press(pilot, "pagedown")
        end = s.frame()
        assert "username_subject" in end                           # the note's last line
        await s.press(pilot, "pageup")
        assert s.frame() != end, "pgup after the last page did not move"

        # space in split hides from both views
        await s.press(pilot, "space")
        assert "Launch new homepage" not in s.frame()
        await s.press(pilot, "1")
        assert "Launch new homepage" not in s.frame()
        assert len(s.saves) == 1

        # x exports the current view's frame, each view to its own file, no key in it
        reports = tmp_path / "reports"
        await s.press(pilot, "x")                                  # the gantt view
        await s.press(pilot, "2", "x")                             # the split view
        gantt_svg = reports / "present-website-redesign-2026-09-30.svg"
        split_svg = reports / "present-website-redesign-2026-09-30-split.svg"
        assert gantt_svg.is_file() and split_svg.is_file(), sorted(reports.iterdir())
        g = gantt_svg.read_text(encoding="utf-8").replace("&#160;", " ")
        sp = split_svg.read_text(encoding="utf-8").replace("&#160;", " ")
        assert "gantt" in g and "split" in sp
        assert "Design tokens are frozen" in sp and "Design tokens are frozen" not in g
        for k in KEY_WORDS:
            assert k not in s.frame(), k
            assert k not in sp and k not in g, k

        await s.press(pilot, "a")
        assert len(s.saves) == 2
        await s.press(pilot, "escape")
        assert type(s.app.screen).__name__ != "PresentScreen"
        await s.press(pilot, "R")
        assert type(s.app.screen).__name__ == "PresentScreen"
        assert "  gantt " in s.rows()[0]
    assert len(s.saves) == 2


# --------------------------------------------------------------------------- #
# TC-1808 — the hint row carries the keys (LLR-1803.2)
# --------------------------------------------------------------------------- #
LONG = "⇥ next · ←→ ↑↓ move · ␣ hide · a show all · x export · esc leave"
SHORT = "⇥ · ←→ · ␣ hide · a all · x export · esc"
MIDDLE = "⇥ next · ←→ ↑↓ · ␣ hide · a show all · x export · esc"   # 2026-10-18-batch-03


@pytest.mark.parametrize("size, gantt, split, split_hidden", [
    # three view names and the `u` tail since batch 2026-10-19-batch-01 (the first
    # widths of `.dev-flow/2026-10-19-batch-01/evidence/hint-widths.txt`)
    ((118, 31), "1 gantt  2 split  3 all  " + LONG, "1 gantt  2 split  3 all  " + "pgdn notes · " + LONG,
     "1 gantt  2 split  3 all  " + "pgdn notes · " + LONG + " · u 1 hidden"),
    ((100, 31), "1 gantt  2 split  3 all  " + LONG, "1 gantt  2 split  3 all  " + "pgdn · " + MIDDLE,
     "1 gantt  2 split  3 all  " + "pgdn · " + MIDDLE + " · u 1 hidden"),
    ((99, 31), "1 gantt  2 split  3 all  " + LONG, "1 gantt  2 split  3 all  " + "pgdn · " + MIDDLE,
     "1 gantt 2 split 3 all " + "pgdn · " + SHORT + " · u 1 hidden"),
    ((96, 31), "1 gantt  2 split  3 all  " + LONG, "1 gantt  2 split  3 all  " + "pgdn · " + MIDDLE,
     "1 gantt 2 split 3 all " + "pgdn · " + SHORT + " · u 1 hidden"),
    ((80, 25), "1 gantt  2 split  3 all  " + MIDDLE, "1 gantt 2 split 3 all " + "pgdn · " + SHORT,
     "1 gantt 2 split 3 all " + "pgdn ⇥ ←→ ␣ x esc · u 1 hidden"),
], ids=["118", "100", "99", "96", "80"])
async def test_TC_1808_the_hint_row_per_view(tmp_path, monkeypatch, frozen, size, gantt, split,
                                             split_hidden):
    """TC-1808 (LLR-1803.2): the hint names both views, the current one bright
    and bold, then `pgdn` in the split view only, then the moves and the
    hidden count — in the long wording when it fits the hint's cells, else the
    middle one (batch 2026-10-18-batch-03: it keeps `next` and `show all`, the
    keys a first-time presenter does not guess), else the short one, so the hint
    is never cut (code-review: at 100 columns the long split hint with a count is
    107 cells in a 98-cell row)."""
    s = _Presenting(tmp_path, monkeypatch, size)
    async with s.app.run_test(size=s.size) as pilot:
        await s.open(pilot)
        assert s.hint() == gantt
        hint = s.app.screen.query_one("#present-hint").content
        spans = {hint.plain[sp.start:sp.end]: str(sp.style) for sp in hint.spans}
        assert "bold" in spans["1 gantt"] and "bold" not in spans["2 split"], spans
        await s.press(pilot, "2")
        assert s.hint() == split
        await s.press(pilot, "space")
        assert s.hint() == split_hidden
        for h in (gantt, split, split_hidden):
            assert views.vis(h) <= size[0] - 2, (size, h)


# --------------------------------------------------------------------------- #
# TC-1809 — the export names the view (LLR-1803.3)
# --------------------------------------------------------------------------- #
def test_TC_1809_each_view_exports_to_its_own_file(tmp_path):
    """TC-1809 (LLR-1803.3): the gantt view keeps the shipped file name; the
    split view adds `-split`, so exporting both on one day keeps both."""
    b = nb.build(tmp_path / "board.json")
    g = views.present_paths(b, "Website Redesign", pb.TODAY)
    assert g == views.present_paths(b, "Website Redesign", pb.TODAY, "gantt")
    assert g[0].name == "present-website-redesign-2026-09-30.svg"
    sp = views.present_paths(b, "Website Redesign", pb.TODAY, "split")
    assert sp[0].name == "present-website-redesign-2026-09-30-split.svg"
    assert sp[1].name == "present-website-redesign-2026-09-30-split.png"


# --------------------------------------------------------------------------- #
# TC-1810 — the screen's view keys and state (LLR-1803.1)
# --------------------------------------------------------------------------- #
async def test_TC_1810_the_bindings_and_the_scroll_state(tmp_path, monkeypatch, frozen):
    """TC-1810 (LLR-1803.1): the six keys are the screen's own priority
    bindings — the app's `1`/`2` stay non-priority and its `tab` is released
    while the screen is open, so the board behind never reacts; a new screen
    starts on view 0 with scroll 0; `pgdn` moves the split view's scroll one
    step, never past the last page (a page that paints the same frame is not
    taken), `pgup` never below 0, `pgdn` in the gantt view moves nothing, and a
    cursor move or a resize scrolls back to the top."""
    from taskboard.app import PresentScreen, TaskboardApp

    want = {"1": "view(0)", "2": "view(1)", "tab": "cycle(1)", "shift+tab": "cycle(-1)",
            "pagedown": "scroll(1)", "pageup": "scroll(-1)"}
    got = {b.key: (b.action, b.priority) for b in PresentScreen.BINDINGS if b.key in want}
    assert got == {k: (a, True) for k, a in want.items()}, got
    app_keys = {b.key: b.priority for b in TaskboardApp.BINDINGS if b.key in ("1", "2")}
    assert app_keys == {"1": False, "2": False}, app_keys

    s = _Presenting(tmp_path, monkeypatch, (80, 25))
    async with s.app.run_test(size=s.size) as pilot:
        await s.open(pilot, cursor=nb.LONG)
        scr = s.app.screen
        assert (scr._view, scr._scroll) == (0, 0)
        assert s.app.check_action("toggle_presentation", ()) is False
        await s.press(pilot, "pagedown")
        assert scr._scroll == 0                                    # gantt: nothing moves
        await s.press(pilot, "2", "pageup")
        assert scr._scroll == 0
        await s.press(pilot, "pagedown")
        assert scr._scroll == 1
        for _ in range(20):
            await s.press(pilot, "pagedown")
        last = scr._scroll
        assert last < 20 * 1, last
        await s.press(pilot, "pagedown")
        assert scr._scroll == last
        await s.press(pilot, "left")
        assert scr._scroll == 0
        await s.press(pilot, "pagedown")
        assert scr._scroll == 1
        await pilot.resize_terminal(80, 40)                       # code-review F1
        await pilot.pause()
        assert scr._scroll == 0, "a resize kept a page cut for the old size"
