"""The chain map's unit layer (batch 2026-10-07-batch-02, increment 001).

HLR-801 / LLR-801.1 · TC-801, TC-802, TC-803, TC-804, TC-807, TC-808.

The oracle is C-2b (round-7 verdict): the exact rows the shipped renderer must
paint, byte-faithful at 118x30 and 80x24, are
`.dev-flow/2026-10-07-batch-06/evidence/frames/C-2b-*.txt` — amended under
LED-2026-10-07-batch-06.1 (the `○` tiles); the sealed batch-02 frames stay
history. The fixture is the
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
from taskboard.models import Board, Project, Task

ROOT = Path(__file__).resolve().parents[1]
FRAMES = ROOT / ".dev-flow" / "2026-10-07-batch-06" / "evidence" / "frames"


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


def test_TC_810_the_fold_caps_a_partial_band_and_still_drops_whole(tmp_path):
    """TC-810 (code review CM-2, HIGH, amended by LED-2026-10-07-batch-06.1): a
    band that no longer fits whole draws its fitting chains + `○` tiles + one
    `+N more ↓` tail (N exact -- the band's chains AND tiles minus the drawn
    ones) and only the drawn rows reach the line_map; a band whose FIRST row
    does not fit still drops whole (head and canvas together)."""
    from taskboard.views import render_chainmap
    today = kg_board.TODAY

    def add_chains(b, pid, n):
        for k in range(n):
            a = Task(f"Head {pid} {k}", phase="Next", project_id=pid,
                     start_date=(today + timedelta(days=k)).isoformat(),
                     due_date=(today + timedelta(days=k + 1)).isoformat(), id=f"h{pid}{k}")
            z = Task(f"Tail {pid} {k}", phase="Next", project_id=pid,
                     start_date=(today + timedelta(days=k + 2)).isoformat(),
                     due_date=(today + timedelta(days=k + 3)).isoformat(),
                     depends_on=[f"h{pid}{k}"], id=f"t{pid}{k}")
            b.tasks += [a, z]

    # (1) the partial band: Data Warehouse alone -- its base chain + 6 added
    # chains + its 2 open `○` tiles (td2, td3) no longer fit at 80x24. It draws
    # the fitting chains and names the rest `+3 more ↓` (1 chain + 2 tiles); the
    # folded chains and tiles never reach the line_map.
    b = kg_board.build(tmp_path / "board.json")
    b.projects = [p for p in b.projects if p.id == "pdwh"]
    b.tasks = [t for t in b.tasks if t.project_id == "pdwh"]
    add_chains(b, "pdwh", 6)
    line_map: dict = {}
    text = render_chainmap(b, False, None, today, 80, 24, line_map).plain
    assert "Data Warehouse" in text, text
    assert "+3 more ↓" in text, text
    for tid in ("td1", "td4", "td5"):
        assert tid in line_map, (tid, line_map)
    for tid in ("td2", "td3", "hpdwh5", "tpdwh5"):
        assert tid not in line_map, (tid, line_map)

    # (2) the zero-fit band: 5 chains on Website Redesign (the FIRST project)
    # spend the whole body, so Mobile App's first chain no longer fits and the
    # band drops whole -- head AND canvas gone, no tile in the line_map.
    b2 = kg_board.build(tmp_path / "board2.json")
    add_chains(b2, "pweb", 5)
    lm2: dict = {}
    text2 = render_chainmap(b2, False, None, today, 80, 24, lm2).plain
    assert "Mobile App" not in text2, text2
    assert not any(tid in lm2 for tid in ("tm2", "tm3", "tm4", "tm5")), lm2


# --------------------------------------------------------------------------- #
# LLR-1201.1 / LLR-1201.2 — every open task is a tile (batch 2026-10-07-batch-06)
# --------------------------------------------------------------------------- #
def test_an_open_unlinked_task_is_a_selectable_open_tile(tmp_path, frozen):
    """LLR-1201.1: an open task with no links paints as a one-row `○` tile with
    its title and late mark, and reaches the line_map (it is selectable)."""
    b = _base(tmp_path)
    line_map: dict = {}
    rows = _render(b, "tw3", 118, 30, line_map)
    assert "tw3" in line_map
    row = rows[line_map["tw3"]]
    assert "○" in row and "Fix checkout 500 error" in row, row
    assert "▲2d" in row, row                    # the late mark rides the tile


def test_the_no_links_row_only_for_a_project_with_no_open_work(tmp_path, frozen):
    """LLR-1201.1: a project with no open work at all keeps the inert `no links`
    row; a project with an open unlinked task draws an `○` tile instead."""
    lonely = Project("Lonely", "sky")
    busy = Project("Busy", "lime")
    done = Task("shipped", lonely.id, "Done", phase_changed=TODAY.isoformat(), id="s1")
    todo = Task("todo", busy.id, "Doing", id="b1")
    b = Board([lonely, busy], [done, todo], tmp_path / "b.json",
              phases=["Doing", "Done"])
    line_map: dict = {}
    rows = _render(b, "b1", 118, 30, line_map)
    assert "no links" in "\n".join(rows)        # Lonely: no open work at all
    assert "b1" in line_map and "○" in rows[line_map["b1"]]


def test_the_nav_reaches_an_open_tile_in_band_order(tmp_path, frozen):
    """LLR-1201.2: the `○` tiles sit in the depth-0 nav column, after the band's
    chained heads, so the arrows reach them."""
    b = _base(tmp_path)
    cols = views._chainmap_nav(b, False)
    flat = [tid for col in cols for tid in col]
    assert "tw3" in flat and "tw6" in flat and "td2" in flat
    assert cols[0][0] == "tw1"                  # the first depth-0 chain head
    assert flat.index("tw3") < flat.index("td2")  # band order preserved
