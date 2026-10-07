"""The chain map's unit layer (batch 2026-10-07-batch-02, increment 001).

HLR-801 / LLR-801.1 · TC-801, TC-802, TC-803, TC-804, TC-807, TC-808.

The oracle is C-2b (round-7 verdict): the exact rows the shipped renderer must
paint, byte-faithful at 118x30 and 80x24, are
`.dev-flow/2026-10-07-batch-02/evidence/frames/C-2b-*.txt`. The fixture is the
kg board (`tests/kg_board.py`), frozen on its own TODAY so `shifted` collapses
to the frames' fixed dates; the deviating band (Data Warehouse `together`) is
set IN-TEST — the frames carry it, the base board does not.

RED on the base tree: `views.render_chainmap` does not exist yet (the product
half lands in parallel).
"""
from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

import pytest

import kg_board
from kg_board import TODAY
from taskboard import views
from taskboard.models import Task

ROOT = Path(__file__).resolve().parents[1]
FRAMES = ROOT / ".dev-flow" / "2026-10-07-batch-02" / "evidence" / "frames"


def _frame(name: str) -> list[str]:
    """The oracle rows, universal-newline split (the frames ship CRLF)."""
    return (FRAMES / name).read_text(encoding="utf-8").splitlines()


def _render(b, sel: str, w: int, h: int, line_map=None) -> list[str]:
    """The shipped renderer's painted rows at a panel size. `today` is the
    board's own TODAY (the frozen calendar); `show_archived` is off."""
    text = views.render_chainmap(b, False, sel, TODAY, width=w, height=h,
                                 line_map=line_map)
    return text.plain.split("\n")


class _Today(date):
    @classmethod
    def today(cls):
        return TODAY


@pytest.fixture
def frozen(monkeypatch):
    """Freeze the calendar on the oracle board's TODAY so `shifted`'s delta is
    zero and the frames' fixed dates reproduce on any day (the house seam of
    `test_gantt_board.py`). `kg_board` is patched too: `shifted` reads the
    module-level `date`."""
    from taskboard import models
    monkeypatch.setattr(views, "date", _Today)
    monkeypatch.setattr(models, "date", _Today)
    monkeypatch.setattr(kg_board, "date", _Today)


def _base(tmp_path, *, together: bool = False):
    """The base board (the frames' own fixture): 15 linked tasks, frozen."""
    b = kg_board.shifted(tmp_path / "board.json")
    if together:
        b.project_by_id("pdwh").extra["date_links"] = "together"
    b.save()
    return b


# --------------------------------------------------------------------------- #
# TC-801 / TC-802 — the exact C-2b rows at both operator sizes
# --------------------------------------------------------------------------- #
def test_TC_801_the_exact_c2b_frame_at_118x30(tmp_path, frozen):
    """TC-801 (LLR-801.1): on the base board with Data Warehouse `together`, the
    rendered frame at 118x30 equals C-2b-118x30.txt, line for line."""
    b = _base(tmp_path, together=True)
    got = _render(b, "tm3", 118, 30)
    assert got == _frame("C-2b-118x30.txt")


def test_TC_802_the_exact_c2b_frame_at_80x24(tmp_path, frozen):
    """TC-802 (LLR-801.1): the same board at 80x24 equals C-2b-80x24.txt."""
    b = _base(tmp_path, together=True)
    got = _render(b, "tm3", 80, 24)
    assert got == _frame("C-2b-80x24.txt")


# --------------------------------------------------------------------------- #
# TC-803 — the greyscale law and the fan-in join
# --------------------------------------------------------------------------- #
def test_TC_803_the_critical_chain_differs_without_colour_and_the_fan_in_joins(
        tmp_path, frozen):
    """TC-803 (HLR-801): the critical chain carries its own STRUCTURE — heavy
    `━`/`┃` glyphs the light chains never wear — so the two are separable with
    the colour taken away (hue is never the only channel); and the Website
    fan-in draws its join (`┬` above, `╰───╯` below)."""
    b = _base(tmp_path)
    rows = _render(b, "tm3", 118, 30)

    crit = next(r for r in rows if "Add push notifications" in r)
    light = next(r for r in rows if "Design homepage mockups" in r)
    assert "┃" in crit and "━━" in crit, crit
    assert "┃" not in light and "━━" not in light, light
    assert "──" in light and "▸" in light and "▸" in crit, (light, crit)

    joined = "\n".join(rows)
    assert "┬" in joined, "the fan-in node is drawn"
    assert any("╰" in r and "╯" in r for r in rows), "the fan-in join lane is drawn"


# --------------------------------------------------------------------------- #
# TC-804 — the header counts on both fixtures
# --------------------------------------------------------------------------- #
def test_TC_804_the_header_counts_both_boards(tmp_path, frozen):
    """TC-804 (HLR-801): the base board's header holds `15 linked tasks`; the
    milestones board's holds `17 linked tasks` (it adds td0 and re-points td5)."""
    base = _base(tmp_path)
    head = _render(base, "tm3", 118, 30)[0]
    assert "15 linked tasks" in head, head

    milestones = kg_board.milestones(kg_board.shifted(tmp_path / "ms.json"),
                                     TODAY)
    head = _render(milestones, "td4", 118, 30)[0]
    assert "17 linked tasks" in head, head


# --------------------------------------------------------------------------- #
# TC-807 — S1: a hostile title renders escaped, the width holds
# --------------------------------------------------------------------------- #
def test_TC_807_a_hostile_title_renders_escaped_and_the_width_holds(tmp_path, frozen):
    """TC-807 (LLR-801.1, S1): a title holding markup (`[bold]x[/bold]`) and a
    lone close tag (`[/]`) is painted LITERALLY — never parsed — and every row
    still spends exactly the frame width (no phantom cells)."""
    b = _base(tmp_path)
    b.task_by_id("tm2").title = "[bold]x[/bold]"
    b.task_by_id("tm3").title = "[/]"
    rows = _render(b, "tm2", 118, 30)

    joined = "\n".join(rows)
    assert "[bold]x" in joined, joined          # escaped, not interpreted
    assert "[/]" in joined, joined
    for r in rows:
        assert views.vis(r) == 118, (views.vis(r), r)


# --------------------------------------------------------------------------- #
# TC-808 — a stored 2-cycle renders once, no hang
# --------------------------------------------------------------------------- #
def test_TC_808_a_stored_two_cycle_renders_once(tmp_path, frozen):
    """TC-808 (LLR-801.1, boundary/error): a hand-edited 2-cycle (A waits on B,
    B waits on A) is drawn ONCE each and the render returns — no infinite
    descent (`critical_chain`'s visited set is the guard the port must keep)."""
    b = _base(tmp_path)
    b.tasks.append(Task("Cycle A", project_id="pweb", phase="Backlog",
                        depends_on=["cycb"], id="cyca"))
    b.tasks.append(Task("Cycle B", project_id="pweb", phase="Backlog",
                        depends_on=["cyca"], id="cycb"))
    rows = _render(b, "tm3", 118, 30)
    joined = "\n".join(rows)
    assert joined.count("Cycle A") == 1, joined
    assert joined.count("Cycle B") == 1, joined


def test_TC_809_a_deep_chain_renders_instead_of_crashing(tmp_path):
    """TC-809 (code review CM-1, HIGH): a 25-task chain piles into the capped
    columns and RENDERS -- the pre-fix tile math crashed textwrap on a negative
    width. RED before the fix: ValueError from textwrap."""
    from taskboard.views import render_chainmap
    b = kg_board.build(tmp_path / "board.json")
    today = kg_board.TODAY
    pred = None
    for i in range(25):
        t = Task(f"Chain step {i}", phase="Next", project_id="pmob",
                 start_date=(today + timedelta(days=i)).isoformat(),
                 due_date=(today + timedelta(days=i + 1)).isoformat(),
                 depends_on=[pred] if pred else [], id=f"c{i}")
        b.tasks.append(t)
        pred = f"c{i}"
    text = render_chainmap(b, False, "c0", today, 118, 30, {}).plain
    assert "Chain step" in text, text[:200]          # the deep chain painted
    assert "chain 25" in text                        # and its length is named


def test_TC_810_the_fold_drops_whole_bands_never_a_dangling_head(tmp_path):
    """TC-810 (code review CM-2, HIGH): later projects carry chains that do not
    fit at 80x24 -- the fold drops WHOLE bands (no head without its canvas) and
    only the surviving bands' tiles reach the line_map. RED before the fix: the
    fold cut mid-band (a dangling head) and the line_map held undrawn rows."""
    from taskboard.views import render_chainmap
    b = kg_board.build(tmp_path / "board.json")
    today = kg_board.TODAY
    for k in range(8):                       # 8 chains on API + 8 on DWH: they fold
        for pid in ("papi", "pdwh"):
            a = Task(f"Head {pid} {k}", phase="Next", project_id=pid,
                     start_date=(today + timedelta(days=k)).isoformat(),
                     due_date=(today + timedelta(days=k + 1)).isoformat(), id=f"h{pid}{k}")
            z = Task(f"Tail {pid} {k}", phase="Next", project_id=pid,
                     start_date=(today + timedelta(days=k + 2)).isoformat(),
                     due_date=(today + timedelta(days=k + 3)).isoformat(),
                     depends_on=[f"h{pid}{k}"], id=f"t{pid}{k}")
            b.tasks += [a, z]
    line_map: dict = {}
    text = render_chainmap(b, False, None, today, 80, 24, line_map).plain
    assert line_map, "the first bands must survive the fold"
    folded_h = [f"h{pid}0" for pid in ("papi", "pdwh")]
    assert all(h not in line_map for h in folded_h), "a folded band leaked tiles"
    # and a folded band's HEAD never dangles without its canvas
    assert "API Platform" not in text and "Data Warehouse" not in text, text
