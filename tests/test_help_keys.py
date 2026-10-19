"""The `?` help shows every key (batch 2026-10-16-batch-01, increment 003).

HLR-1603 / LLR-1603.1, LLR-1603.2 · TC-1606, TC-1607 · AT-1603 (US-1603).

Why these matter: `?` is where a user looks for a key. On the base tree the
Keys list sat at the end of the right column and ran off the box, and the
palette-only global keys (`R` Present, `S` Standup, …) were in no list at all
(`bar_keys` drops `bar=False`). Now the view's keys are a full-width
column-major band under the two columns (inside the scrolled body, listed whole),
and the global keys are DOCKED at the bottom of the box, outside the scroll, so
they are on screen at every supported size without scrolling — read from
`KEYMAP`, so a key added later appears without anyone editing the help.
RED on the base tree: no `global_keys`, no band, `R Present` never painted.
"""
from __future__ import annotations

import pytest
from rich.cells import cell_len

import present_board as pb
from taskboard import keymap
from taskboard.modals import GLOBAL_LEAD, global_lines, keys_grid


# --------------------------------------------------------------------------- #
# TC-1606 — the band: column-major, every key once, never wider than the box
# --------------------------------------------------------------------------- #
def test_TC_1606_the_grid_reads_down_then_across():
    """TC-1606 (LLR-1603.1): 7 cells in a width for 3 columns make 3 rows, the
    last column short — the one shape where column-major and row-major differ:
    down the first column come a, b, c."""
    cells = [f"{c}   key {c}" for c in "abcdefg"]           # 9 cells wide each, cw 11
    rows = keys_grid(cells, 33)
    assert len(rows) == 3
    assert [r.split()[0] for r in rows] == ["a", "b", "c"]  # row-major would give a, d, g
    assert rows[0].split()[::3] == ["a", "d", "g"]
    assert rows[2].split()[::3] == ["c", "f"]
    flat = " ".join(rows).split()
    assert sorted(flat[::3]) == list("abcdefg")              # every key exactly once
    assert all(cell_len(r) <= 33 for r in rows)


def test_TC_1606_a_box_narrower_than_one_cell_gets_one_column():
    """TC-1606 (LLR-1603.1 boundary): one column, one key per row."""
    rows = keys_grid(["?   Map", "q   Quit", "esc Focus off"], 5)
    assert rows == ["?   Map", "q   Quit", "esc Focus off"]


@pytest.mark.parametrize("width", [70, 104])
def test_TC_1606_the_gantt_band_fits_the_box_at_both_sizes(width):
    """TC-1606 (LLR-1603.1): the gantt view's ~40 keys at the box's inner width
    at 80 (70) and 118 (104) columns: every key once, no row wider than the box."""
    keys = keymap.bar_keys("gantt")
    rows = keys_grid([f"{k.show:<3} {k.label}" for k in keys], width)
    assert all(cell_len(r) <= width for r in rows)
    joined = "\n".join(rows)
    for k in keys:
        assert joined.count(f"{k.show:<3} {k.label}") == 1, k


async def test_TC_1606_the_band_re_lays_when_the_terminal_shrinks(tmp_path):
    """TC-1606 (LLR-1603.1): the user scales the terminal. `?` opened at 118x30,
    then the terminal shrinks to 80x24: the band and the global line are laid
    out again at the new box width — no row wider than the box's content."""
    from textual.widgets import Label

    from taskboard.app import TaskboardApp

    path = tmp_path / "board.json"
    pb.build(path).save()
    app = TaskboardApp(board_path=str(path))
    async with app.run_test(size=(118, 30)) as pilot:
        for _ in range(50):
            if type(app.screen).__name__ == "MilestoneOffer":
                await pilot.press("escape")
                break
            await pilot.pause()
        await pilot.press("3")
        await pilot.pause()
        await pilot.press("question_mark")
        for _ in range(3):
            await pilot.pause()
        await pilot.resize_terminal(80, 24)
        for _ in range(4):
            await pilot.pause()
        width = app.screen.query_one("#help-modal-box").scrollable_content_region.width
        for wid in ("#help-keys", "#help-global"):
            text = app.screen.query_one(wid, Label).render()
            rows = (text.plain if hasattr(text, "plain") else str(text)).split("\n")
            assert max(cell_len(r) for r in rows) <= width, (wid, width, rows)


# --------------------------------------------------------------------------- #
# TC-1607 — the global line: from KEYMAP, packed, never splitting an entry
# --------------------------------------------------------------------------- #
def test_TC_1607_global_keys_are_the_live_palette_only_keys(monkeypatch):
    """TC-1607 (LLR-1603.2): `global_keys` is exactly the live `bar=False`
    entries in seat order — and a key added to the seat later is in it with no
    edit to the help (the negative control a hand-typed list fails)."""
    want = [k for k in keymap.KEYMAP if not k.bar and (k.views is None or "gantt" in k.views)]
    assert keymap.global_keys("gantt") == want
    assert {"R", "S"} <= {k.show for k in want}
    extra = keymap.Key("Z", "Z", "zz_test", "Zed", group="misc", bar=False)
    monkeypatch.setattr(keymap, "KEYMAP", keymap.KEYMAP + (extra,))
    assert keymap.global_keys("gantt")[-1] == extra


def test_TC_1607_the_line_packs_and_wraps_only_between_entries():
    """TC-1607 (LLR-1603.2): the expected row count is COMPUTED from the
    entries (a global key added later must not break this arm): one row when
    `Global  ` + the entries joined by two spaces fits, else as many as the
    greedy entry-boundary wrap needs; every entry stays whole on one row."""
    entries = [f"{k.show} {k.label}" for k in keymap.global_keys("gantt")]
    one_row = cell_len(GLOBAL_LEAD + "  ".join(entries))
    for width in (104, 70):
        lines = global_lines(entries, width)
        assert (len(lines) == 1) == (one_row <= width), (width, lines)
        assert all(cell_len(ln) <= width for ln in lines), lines
        assert lines[0].startswith(GLOBAL_LEAD)
        body = [ln.strip() for ln in lines]
        body[0] = body[0][len(GLOBAL_LEAD.strip()):].strip()
        assert "  ".join(body).split("  ") == entries        # no entry split across rows


# --------------------------------------------------------------------------- #
# AT-1603 — `?` in the gantt view: R and S on screen, unscrolled, at both sizes
# --------------------------------------------------------------------------- #
GANTT_PAIRS = ["L   Link", "M   Milestone", "[   Phase−", "esc Focus off", "/   Search",
               "6   Chains"]


def _painted(app) -> list[str]:
    """The screen as the compositor paints it, one string per row."""
    return ["".join(seg.text for seg in strip)
            for strip in app.screen._compositor.render_strips(app.screen.size)]


@pytest.mark.parametrize("size", [(118, 30), (80, 24)], ids=lambda s: f"{s[0]}x{s[1]}")
async def test_AT_1603_the_help_shows_the_global_keys_without_scrolling(tmp_path, size):
    """AT-1603 (US-1603, HLR-1603): the gantt view, `?` → the painted screen
    holds `R Present` and `S Standup` with no scroll; then `end` scrolls the
    body and the Keys band paints the gantt keys whole (hard-coded pairs) while
    the global line is still on screen."""
    from taskboard.app import TaskboardApp

    path = tmp_path / "board.json"
    pb.build(path).save()
    app = TaskboardApp(board_path=str(path))
    async with app.run_test(size=size) as pilot:
        for _ in range(50):
            if type(app.screen).__name__ == "MilestoneOffer":
                await pilot.press("escape")
                break
            await pilot.pause()
        await pilot.press("3")
        await pilot.pause()
        await pilot.press("question_mark")
        for _ in range(3):
            await pilot.pause()
        rows = "\n".join(_painted(app))
        assert "R Present" in rows and "S Standup" in rows, rows

        await pilot.press("end")
        for _ in range(50):        # the scroll paints when it paints: wait for it, bounded
            await pilot.pause()
            rows = "\n".join(_painted(app))
            if all(pair in rows for pair in GANTT_PAIRS):
                break
        for pair in GANTT_PAIRS:
            assert pair in rows, (pair, rows)
        assert "R Present" in rows and "S Standup" in rows, rows
