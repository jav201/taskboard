"""Inc MR-a — a group's milestones share ONE row of the board gantt (US-4601).

Written by the independent tester from the design only (`.dev-flow/2026-11-06-v3-incMR/`:
`01-requirements.md` LLR-4601.1..LLR-4606.5, the graphs' examples, `e2-seams.md`,
rulings R-1..R-8, `e3-addenda.md`). TC ids follow the requirements: LLR-4601.n →
TC-(4800+n), LLR-4602.n → TC-(4810+n), LLR-4603.n → TC-(4820+n) except
LLR-4603.11 → TC-4820, LLR-4604.n → TC-(4830+n), LLR-4605.n → TC-(4840+n),
LLR-4606.n → TC-(4850+n).

Why these matter: a milestone is a date, not work; one row each spent the board's
height (MR-F at 118x30: 23 body rows, 18 with the shared row) and folded projects
the operator needed to see. Every assertion reads the OBSERVABLE frame — the
plain cells, the painted style, `line_map`, the nav column, the app's selection
after a key — never the internal call sequence. Layer 0 goes through the shipped
painter `render_gantt` (no hand-built `GanttAxis`, A-1, A-2); the keys go through
the real app (`open_app`, a real registry in a temporary home).

Fixture MR-F (`tests/milestone_row_fixture.py`, synthetic, TODAY 2026-10-20).
RED on base 154e260: one row per milestone, `←→` a no-op in the gantt, a nav column
that keeps hidden classes (R-4).
"""
from __future__ import annotations

import re
from datetime import date, timedelta
from pathlib import Path

import pytest
from rich.text import Text

import milestone_marks_fixture as mmfx
import milestone_row_fixture as fx
from milestone_row_fixture import (GROUND, HEX, MARKS, Frame, cell_len, gantt, hide_class,
                                   keys, norm, screen)
from taskboard import app as app_module
from taskboard import models, views
from taskboard.models import parse_iso

TODAY = fx.TODAY
PILOT = fx.PILOT_MS
EVAL, DOCS, INBOX = ["tg1", "tg2"], ["th1"], ["ti1"]
LANES = {"Pilot rollout": PILOT, "Eval harness": EVAL, "Docs & handover": DOCS,
         "Inbox": INBOX}


class _Today(date):
    @classmethod
    def today(cls):
        return TODAY


@pytest.fixture(autouse=True)
def _pin_today(monkeypatch):
    for mod in (app_module, models, views):
        monkeypatch.setattr(mod, "date", _Today)


@pytest.fixture
def home(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
    return tmp_path / ".taskboard"


def mrf(**kw):
    return fx.board(**kw)


T = fx.task
P = fx.project


def _with(*tasks, projects=(), hidden=()):
    return fx.board(extra=list(tasks), extra_projects=list(projects), hidden=hidden)


def _due_off(day: date) -> int:
    return (day - TODAY).days


# =============================================================================
# 4.1 The row (HLR-4601)
# =============================================================================
def test_TC_4801_LLR_4601_1_one_milestone_row_right_under_each_span_row():
    """4 groups with drawn milestones → 4 milestone rows, each the line after its
    span row, and no other body line holds a milestone mark. NC: the row after
    the group's last task; base: one row per milestone."""
    f = Frame(mrf(), "tstore")
    rows = {}
    for name, ids in LANES.items():
        rows[name] = f.lane_line(ids)
        assert rows[name] == f.span_of(name) + 1, name
    assert len(rows) == 4
    for i in set(f.lm.values()) - set(rows.values()):
        assert not set(f.fcells(i)) & MARKS, (i, f.lines[i])


def test_TC_4802_LLR_4601_2_the_row_holds_exactly_the_groups_drawn_milestones():
    """Per group, the ids on the row = base's drawn milestones (Pilot rollout 5
    with the reached m1, Eval 2, Docs 1, Inbox 1); a group with only reached
    milestones and no open work → no row (D-606). NC: drop reached ones."""
    closed = P("pz", "Closed gates")
    b = _with(T("z1", "pz", "Gate paid", "Done", None, -3, True, "payment"),
              T("z2", "pz", "Wrap-up", "Done", -6, -4), projects=[closed])
    f = Frame(b, "tstore", 118, 0)
    for name, ids in LANES.items():
        row = f.lane_line(ids)
        on_row = {k for k, ln in f.lm.items() if ln == row and b.task_by_id(k).milestone}
        assert on_row == set(ids), name
    assert len(PILOT) == 5
    assert "tz1" not in f.lm


def test_TC_4803_LLR_4601_3_tasks_one_per_row_in_base_order_under_the_row():
    """Under the milestone row, the non-milestone tasks one per row in base's
    order, the done one last. NC: sort by title."""
    b = _with(T("d1", "pr", "Site survey", "Done", -9, -4))
    f = Frame(b, "tstore", 118, 0)
    order = {"Pilot rollout": (PILOT, ["tstore", "ttele", "ttrain", "trota", "td1"]),
             "Eval harness": (EVAL, ["tgq", "tgr", "tgx"]),
             "Docs & handover": (DOCS, ["tha", "thr"]),
             "Inbox": (INBOX, ["tip"])}
    for name, (lane, tasks) in order.items():
        row = f.lane_line(lane)
        assert [f.lm[k] for k in tasks] == list(range(row + 1, row + 1 + len(tasks))), name


def test_TC_4804_LLR_4601_4_the_inbox_has_its_own_row():
    """i1 on the line after the `Inbox` span row; no project row holds it. NC: i1
    on the first project's row."""
    f = Frame(mrf(), "tstore")
    assert f.lm["ti1"] == f.span_of("Inbox") + 1
    assert f.lm["ti1"] not in {f.lm.get(k) for k in PILOT + EVAL + DOCS}


def test_TC_4805_LLR_4601_5_no_drawn_milestone_no_row():
    """No milestone; every milestone archived; only reached milestones and no
    open work → 0 milestone rows, the group's lines = span + tasks. NC: always
    emit the row. Passes on base by design (base draws no row for them)."""
    groups = {
        "Quiet ops": (P("pq", "Quiet ops"),
                      [T("q1", "pq", "Rota", "Next", 0, 6), T("q2", "pq", "Audit", "Next", 1, 8)]),
        "Archived gates": (P("pa", "Archived gates"),
                           [T("a1", "pa", "Prep", "Next", 0, 5),
                            T("a2", "pa", "Old gate", "Next", None, 4, True, "review")]),
        "Closed gates": (P("pz", "Closed gates"),
                         [T("z1", "pz", "Gate paid", "Done", None, -3, True, "payment"),
                          T("z2", "pz", "Wrap-up", "Done", -6, -4)]),
    }
    for name, (proj, tasks) in groups.items():
        for t in tasks:
            if t.id == "ta2":
                t.archived = True
        b = _with(*tasks, projects=[proj])
        f = Frame(b, "tstore", 118, 0)
        s = f.span_of(name)
        ms = [t.id for t in tasks if t.milestone]
        assert not any(k in f.lm for k in ms), name
        block = sorted(k for k, ln in f.lm.items() if b.task_by_id(k).project_id == proj.id)
        assert [f.lm[k] for k in block] == list(range(s + 1, s + 1 + len(block))), name


def test_TC_4806_LLR_4601_6_a_folded_group_draws_no_row():
    """MR-F at 118x12 → each folded group's span row is followed by no task or
    milestone line. NC: the row under a folded span. Passes on base by design."""
    f = Frame(mrf(), "tstore", 118, 12)
    folded = [i for i in f.spans() if f.lines[i].startswith("▸ ")]
    assert folded
    for i in folded:
        assert i + 1 not in set(f.lm.values()), f.lines[i + 1]


def test_TC_4807_LLR_4601_7_the_row_costs_one_row_of_the_fold_budget():
    """MR-F at 80x24 → 0 folded groups (base folds 1); at 118x30 → 0 folded and
    18 body rows (base 23). NC: count each milestone in the budget."""
    narrow = Frame(mrf(), "tstore", 80, 24)
    assert [ln for ln in narrow.lines if ln.startswith("▸ ")] == []
    wide = Frame(mrf(), "tstore", 118, 30)
    assert [ln for ln in wide.lines if ln.startswith("▸ ")] == []
    assert len(wide.spans()) + len(set(wide.lm.values())) == 18


def test_TC_4808_LLR_4601_8_the_rows_dependency_gutter_is_blank():
    """MR-F with m3 waiting on the open `store` → every milestone row's gutter is
    blank and no `waits`/`early` comes from a milestone row (base: m3's row draws
    `↳`, N-10). NC: draw the stop's `gantt_dep_mark`."""
    b = mrf()
    b.task_by_id("tm3").depends_on = ["tstore"]
    f = Frame(b, "tstore")
    assert "waits" not in f.drawn and "early" not in f.drawn, f.drawn
    for ids in LANES.values():
        i = f.lane_line(ids)
        assert f.gutter(i) == " ", f.lines[i]


# =============================================================================
# 4.2 The marks (HLR-4602)
# =============================================================================
def test_TC_4811_LLR_4602_1_each_mark_is_its_class_glyph_in_its_class_style():
    """Nothing selected on the row → g1 `▲` cyan, g2 `■` violet, h1 `◆` mut (the
    seat), i1 `⬢` amber, each at `ax.cell(due)`. NC: `◆` for every class."""
    f = Frame(mrf(), "tstore")
    for key, glyph, tone, lane in (("tg1", "▲", "cyan", EVAL), ("tg2", "■", "violet", EVAL),
                                   ("th1", "◆", "mut", DOCS), ("ti1", "⬢", "amber", INBOX)):
        i, x = f.lane_line(lane), f.cell(key)
        assert f.fcells(i)[x] == glyph, (key, f.lines[i])
        assert fx.hexof(f.fstyle(i, x)) == HEX[tone], key


def test_TC_4812_LLR_4602_2_a_shared_cell_is_one_glyph_and_its_count():
    """m3 + m4 (Oct 24) → `■2` (m3 first in walk order); m4 selected → `▲2`. The
    digit is `bright` beside the selected glyph, else in the class style (A-7).
    NC: only the first glyph, no count."""
    f = Frame(mrf(), "tstore")
    i, x = f.lane_line(PILOT), f.cell("tm3")
    assert f.fcells(i)[x:x + 2] == ["■", "2"], f.lines[i]
    assert fx.hexof(f.fstyle(i, x + 1)) == HEX["violet"]
    g = Frame(mrf(), "tm4")
    i = g.lane_line(PILOT)
    assert g.fcells(i)[x:x + 2] == ["▲", "2"], g.lines[i]
    assert fx.hexof(g.fstyle(i, x + 1)) == HEX["bright"]


def test_TC_4813_LLR_4602_3_ten_or_more_in_one_cell_is_glyph_plus():
    """10 milestones on one day → `<glyph>+` in 2 cells; the cell after `+` is not
    overwritten. NC: print `10` (3 cells)."""
    ten = [T(f"z{n}", "pt", f"Gate {n}", "Next", None, 6, True, "delivery") for n in range(10)]
    b = _with(T("tt", "pt", "Gate prep", "Doing", -2, 12), *ten,
              projects=[P("pt", "Ten gates")])
    f = Frame(b, "ttt", 118, 0)
    i, x = f.lane_line([t.id for t in ten]), f.cell("tz0")
    cells = f.fcells(i)
    assert cells[x:x + 2] == ["▲", "+"], f.lines[i]
    assert cells[x + 2] in GROUND, f.lines[i]


def test_TC_4814_LLR_4602_4_a_reached_milestone_alone_is_hollow_and_tick():
    """m1 (Payment, reached) alone in its cell → `⬡✓`, the `✓` in `reached`.
    NC: the filled glyph."""
    f = Frame(mrf(), "tstore")
    i, x = f.lane_line(PILOT), f.cell("tm1")
    assert f.fcells(i)[x:x + 2] == ["⬡", "✓"], f.lines[i]
    assert fx.hexof(f.fstyle(i, x + 1)) == HEX["reached"]


def test_TC_4815_LLR_4602_5_the_selected_mark_is_reverse_video():
    """m2 selected → its cell `reverse` (in violet); every other mark lacks it.
    NC: no reverse."""
    f = Frame(mrf(), "tm2")
    i = f.lane_line(PILOT)
    st = f.fstyle(i, f.cell("tm2"))
    assert st.reverse and fx.hexof(st) == HEX["violet"], f.lines[i]
    for key in ("tm1", "tm3", "tm5"):
        assert not f.fstyle(i, f.cell(key)).reverse, key


def test_TC_4816_LLR_4602_6_off_window_dues_draw_the_edge_glyph_and_the_mark_inward():
    """Through `render_gantt` (A-1): a reached milestone 40 days back (before
    `ctx`, Oct 14) → `◂⬡✓` at cells 0-2; one reached early, due 90 days ahead →
    `⬡✓▸` in the last three; two reached after the window share the drawn cell →
    `⬡2▸`; N-8: an in-window reached one inside `◂⬡✓`'s footprint joins its bucket
    (`◂⬡2`), never two marks on one cell. NC: clamp without the edge glyph."""
    old = T("x1", "pr", "Old deposit", "Done", None, -40, True, "payment")
    early = T("x2", "pr", "Early payout", "Done", None, 90, True, "payment")
    f = Frame(_with(old, early), "tstore", 118, 0)
    assert TODAY + timedelta(days=-40) < f.ax.start
    i = f.lane_line(PILOT + ["tx1", "tx2"])
    cells = f.fcells(i)
    assert cells[:3] == ["◂", "⬡", "✓"], f.lines[i]
    assert cells[-3:] == ["⬡", "✓", "▸"], f.lines[i]
    late2 = T("x3", "pr", "Late payout", "Done", None, 95, True, "payment")
    g = Frame(_with(early, late2), "tstore", 118, 0)
    i = g.lane_line(PILOT + ["tx2", "tx3"])
    assert g.fcells(i)[-3:] == ["⬡", "2", "▸"], g.lines[i]
    probe = Frame(mrf(), "tstore", 118, 0)
    near = T("y1", "pr", "Near deposit", "Done", None, _due_off(probe.ax.day(2)), True, "payment")
    h = Frame(_with(old, near), "tstore", 118, 0)
    assert h.ax.cell(parse_iso(near.due_date)) == 2
    i = h.lane_line(PILOT + ["tx1", "ty1"])
    assert h.fcells(i)[:3] == ["◂", "⬡", "2"], h.lines[i]


def test_TC_4817_LLR_4602_7_no_due_draws_no_mark():
    """An undated milestone beside one dated one → 1 mark in the field, 0
    exceptions. NC: draw it at today's cell."""
    b = _with(T("nt", "pn", "Bench prep", "Doing", -1, 9),
              T("ny", "pn", "Dated gate", "Next", None, 5, True, "review"),
              T("nd", "pn", "Undated gate", "Next", None, None, True, "launch"),
              projects=[P("pn", "No-date gates")])
    f = Frame(b, "tnt", 118, 0)
    i = f.lane_line(["tny", "tnd"])
    assert sum(ch in MARKS for ch in f.fcells(i)) == 1, f.lines[i]


def test_TC_4818_LLR_4602_8_a_two_cell_mark_in_the_last_cell_starts_one_before():
    """Through `render_gantt` (A-2): a reached milestone due on the field's last
    day (cell w-1) → `⬡✓` at w-2..w-1; two sharing it → `⬡2`; the row exactly `w`
    field cells and the line exactly the width. NC: start at w-1."""
    probe = Frame(mrf(), "tstore", 118, 0)
    last = probe.ax.day(probe.ax.w - 1)
    assert probe.ax.cell(last) == probe.ax.w - 1, "deviation A-2: no day lands on w-1"
    one = T("xl", "pr", "Closing payout", "Done", None, _due_off(last), True, "payment")
    two = T("xm", "pr", "Closing fee", "Done", None, _due_off(last), True, "payment")
    for extra, want in (((one,), ["⬡", "✓"]), ((one, two), ["⬡", "2"])):
        f = Frame(_with(*extra), "tstore", 118, 0)
        assert f.ax.w == probe.ax.w
        i = f.lane_line(PILOT + [t.id for t in extra])
        w = f.ax.w
        assert len(f.fcells(i)) == w
        assert f.fcells(i)[w - 2:w] == want, f.lines[i]
        assert cell_len(f.lines[i]) == 118


# =============================================================================
# 4.3 Labels, label column, chip (HLR-4603)
# =============================================================================
def test_TC_4821_LLR_4603_1_the_selected_title_after_its_mark_else_before():
    """The selected title whole, one ground cell after its mark when it fits; else
    before it, ending one cell before the mark. Threshold as amended by
    LED-2026-11-06-incMR.7 (F-T1, evidence/i2-measure.txt): at 118x30 m5
    selected → `Pilot launch` follows `★ `; a reached milestone due on the field's
    last day selected → its title ends one cell before `⬡✓`. Also g2 (nothing to
    its right). MR-F's m3 cannot fit after `■2` (8 cells to m5) — TC-4822 holds the
    cut. NC: always after, overflowing: the `before` case is RED."""
    m = Frame(mrf(), "tm5")
    i, x = m.lane_line(PILOT), m.cell("tm5")
    assert m.fcells(i)[x + 1] in GROUND
    assert "".join(m.fcells(i)[x + 2:x + 2 + len("Pilot launch")]) == "Pilot launch", m.lines[i]
    f = Frame(mrf(), "tg2")
    i, x = f.lane_line(EVAL), f.cell("tg2")
    title = "Eval report v1"
    assert f.fcells(i)[x + 1] in GROUND
    assert "".join(f.fcells(i)[x + 2:x + 2 + len(title)]) == title, f.lines[i]
    probe = Frame(mrf(), "tstore", 118, 0)
    last = probe.ax.day(probe.ax.w - 1)
    xr = T("xr", "pr", "Final acceptance", "Done", None, _due_off(last), True, "payment")
    g = Frame(_with(xr), "txr", 118, 0)
    i, w = g.lane_line(PILOT + ["txr"]), g.ax.w
    t = "Final acceptance"
    cells = g.fcells(i)
    assert cells[w - 2:w] == ["⬡", "✓"]
    assert cells[w - 3] in GROUND
    assert "".join(cells[w - 3 - len(t):w - 3]) == t, g.lines[i]


def test_TC_4822_LLR_4603_2_no_room_cuts_on_the_roomier_side_from_6_cells():
    """m2 selected → `Rubric…` (7 cells) between m2 and `■2`; m3 selected →
    `Steerin…` (8 cells, the round's oracle `A-sel`); marks 4 cells apart → no
    title cell, the row still exactly the width (SEC-6). NC: any width (`R…`)."""
    f = Frame(mrf(), "tm2")
    i, x = f.lane_line(PILOT), f.cell("tm2")
    assert "".join(f.fcells(i)[x + 2:x + 9]) == "Rubric…", f.lines[i]
    g = Frame(mrf(), "tm3")
    i, x = g.lane_line(PILOT), g.cell("tm3")
    assert "".join(g.fcells(i)[x + 3:x + 11]) == "Steerin…", g.lines[i]
    b = _with(T("kt", "pk", "Cramp prep", "Doing", -2, 14),
              T("k1", "pk", "Left gate", "Next", None, 2, True, "review"),
              T("k2", "pk", "Middle gate", "Next", None, 4, True, "review"),
              T("k3", "pk", "Right gate", "Next", None, 6, True, "review"),
              projects=[P("pk", "Cramped gates")])
    h = Frame(b, "tk2", 118, 0)
    assert h.cell("tk2") - h.cell("tk1") == 4 and h.cell("tk3") - h.cell("tk2") == 4
    i = h.lane_line(["tk1", "tk2", "tk3"])
    field = "".join(h.fcells(i))
    assert "Mi" not in field and "…" not in field, h.lines[i]
    assert cell_len(h.lines[i]) == 118


def test_TC_4823_LLR_4603_3_other_marks_carry_their_leads_whole_date_where_it_fits():
    """Nothing selected on Pilot rollout → `■2 Oct 24` (its lead m3's date),
    `★ Oct 30`; Eval → `▲ Oct 21`, `■ Oct 28`; never a cut date. NC: `Oct`."""
    f = Frame(mrf(), "tstore")
    p, e = f.lane_line(PILOT), f.lane_line(EVAL)
    for i, key, want in ((p, "tm3", "■2 Oct 24"), (p, "tm5", "★ Oct 30"),
                         (e, "tg1", "▲ Oct 21"), (e, "tg2", "■ Oct 28")):
        x = f.cell(key)
        assert norm(f.fcells(i)[x:x + len(want)]) == want, (key, f.lines[i])
    for i in (p, e):
        assert not re.search(r"(Oct|Nov)(?! \d)", f.ftext(i)), f.lines[i]


def test_TC_4824_LLR_4603_4_a_late_lead_shows_its_days_late_in_over():
    """m2 not selected → `▲1d` in `over` beside its mark, `Oct 19` absent. NC:
    `Oct 19`."""
    f = Frame(mrf(), "tstore")
    i, x = f.lane_line(PILOT), f.cell("tm2")
    assert norm(f.fcells(i)[x:x + 5]) == "■ ▲1d", f.lines[i]
    assert fx.hexof(f.fstyle(i, x + 2)) == HEX["over"]
    assert "Oct 19" not in f.ftext(i)


SCENES = ("tstore", "tm3", "tm4", "tm5", "tm1")


@pytest.mark.parametrize("W,H", [(118, 30), (80, 24)])
def test_TC_4825_LLR_4603_5_no_label_covers_a_mark_or_the_edge(W, H):
    """Every row of the AT-4601..AT-4603 scenes at 118 and 80 (5 frames each):
    every mark cell still holds a mark, and the cell before a mark is never a
    label character (the one-cell gap). NC: drop the gap check."""
    for sel in SCENES:
        f = Frame(mrf(), sel, W, H)
        for ids in LANES.values():
            i = f.lane_line(ids)
            cells = f.fcells(i)
            assert len(cells) == f.ax.w
            for x in {f.cell(k) for k in ids}:
                assert cells[x] in MARKS, (sel, W, x, f.lines[i])
                if x > 0:
                    assert not (cells[x - 1].isalnum() or cells[x - 1] == "…"), (
                        sel, W, x, f.lines[i])


def test_TC_4826_LLR_4603_6_the_label_column_at_rest():
    """No member selected → `◆ 2 milestones`, `◆ 1 milestone` at 118 (label ≥ 24
    cells); `◆ 5 ms ▲1` at 80, `▲1` in `over`. NC: omit the late count."""
    f = Frame(mrf(), "tstore")
    assert f.label(f.lane_line(EVAL)).strip() == "◆ 2 milestones"
    assert f.label(f.lane_line(DOCS)).strip() == "◆ 1 milestone"
    assert f.label(f.lane_line(PILOT)).strip() == "◆ 5 milestones ▲1"
    n = Frame(mrf(), "tstore", 80, 24)
    i = n.lane_line(PILOT)
    lab = n.label(i)
    assert lab.strip() == "◆ 5 ms ▲1", n.lines[i]
    assert fx.hexof(n.style(i, lab.index("▲"))) == HEX["over"]


def test_TC_4827_LLR_4603_7_the_label_column_names_the_selected_member():
    """m2 → `■ Rubric sign-off`; m4 → `▲ Store list frozen 2/2`, cut at 80 with the
    `2/2` kept; the title wears `title_markup(t, w, selected=True)`'s cue (A-7).
    NC: drop the `i/N` tag."""
    f = Frame(mrf(), "tm2")
    i = f.lane_line(PILOT)
    assert f.label(i).strip() == "■ Rubric sign-off"
    assert fx.hexof(f.style(i, f.label(i).index("■"))) == HEX["violet"]
    cue = Text.from_markup(views.title_markup(f.b.task_by_id("tm2"), 20, True))
    want = cue.get_style_at_offset(fx._CON, 0)
    got = f.style(i, f.label(i).index("R"))
    assert (fx.hexof(got), got.bold, got.reverse, got.underline) == (
        fx.hexof(want), want.bold, want.reverse, want.underline)
    g = Frame(mrf(), "tm4")
    assert re.sub(" +", " ", g.label(g.lane_line(PILOT)).strip()) == "▲ Store list frozen 2/2"
    n = Frame(mrf(), "tm4", 80, 24)
    lab = n.label(n.lane_line(PILOT)).strip()
    assert lab.startswith("▲ Store") and "…" in lab and lab.endswith("2/2"), lab


def test_TC_4827b_R6_i_of_n_counts_the_cell_not_the_day():
    """E4 I-1 (R-6 F-1): at k = 2 days per cell, m3, m4 (day 4) and a third due
    day 5 fall in ONE cell → one mark `<glyph>3`, and the label column tags each
    `i/3` by the same buckets. NC: count by due date (`2/2`, no tag on the day-5
    one): RED."""
    xa = T("xa", "pr", "Audit hand-in", "Next", None, 5, True, "review")
    b = _with(xa)
    lane = tuple(b.task_by_id(k) for k in ("tm3", "tm4", "txa"))   # walk order
    ax = views.GanttAxis(TODAY, 2, 40, TODAY)
    assert {ax.cell(parse_iso(t.due_date)) for t in lane} == {2}
    field = "".join(g for g, _ in views.gantt_milestone_row(lane, "txa", b, ax, TODAY))
    assert field[2:4] == "■3", field
    for key, tag in (("tm3", "1/3"), ("tm4", "2/3"), ("txa", "3/3")):
        lab = Text.from_markup(views.gantt_lane_label(lane, key, b, ax, TODAY, 30)).plain
        assert lab.rstrip().endswith(tag), (key, lab)


def test_TC_4828_LLR_4603_8_the_chip_is_the_selected_else_the_upcoming_anchor():
    """m2 selected → `▲1d`; nothing on Pilot rollout selected → `in 4d` (m3); a
    row whose only milestones are late → blank. NC: the first one's `✓ done`."""
    assert Frame(mrf(), "tm2").chip(Frame(mrf(), "tm2").lane_line(PILOT)) == "▲1d"
    f = Frame(mrf(), "tstore")
    assert f.chip(f.lane_line(PILOT)) == "in 4d"
    b = _with(T("lt", "pl", "Late prep", "Doing", -2, 5),
              T("l1", "pl", "Missed gate", "Next", None, -3, True, "review"),
              T("l2", "pl", "Slipped gate", "Next", None, -1, True, "delivery"),
              projects=[P("pl", "Late gates")])
    g = Frame(b, "tstore", 118, 0)
    assert g.chip(g.lane_line(["tl1", "tl2"])) == ""


def _scene_boards():
    """The AT-4601..AT-4607 frames as board states: (board, selection)."""
    edges = [T("x2", "pr", "Early payout", "Done", None, 90, True, "payment"),
             T("xn", "pr", "Undated gate", "Next", None, None, True, "launch")]
    edges += [T(f"z{n}", "pr", f"Gate {n}", "Next", None, 6, True, "delivery")
              for n in range(10)]
    out = [(mrf(), s) for s in SCENES]
    out += [(views.filtered_board(mrf(), "store", False), "ttrain"),
            (mrf(hidden={"review"}), "tm1"), (_with(*edges), "tstore")]
    return out


@pytest.mark.parametrize("W,H", [(118, 30), (80, 24), (118, 12)])
def test_TC_4829_LLR_4603_9_no_line_wider_than_the_terminal(W, H):
    """Every frame of the AT scenes → max `cell_len` per line ≤ width. NC: a label
    padded to label_w + 1. Passes on base by design (a regression guard)."""
    for b, sel in _scene_boards():
        f = Frame(b, sel, W, H)
        assert max(cell_len(ln) for ln in f.lines) <= W, (sel, W)


def test_TC_4830_LLR_4603_10_the_legend_names_the_rows_marks():
    """MR-F at 118x30 → the legend holds `◆ milestone` and, with m1 drawn,
    `◆✓ reached`; `drawn` holds both. NC: the row not adding to `drawn`. Passes
    on base by design (base's per-milestone rows add them)."""
    f = Frame(mrf(), "tstore")
    assert {"milestone", "reached"} <= f.drawn
    legend = next(ln for ln in f.lines if "⟦━⟧" in ln)
    assert "◆ milestone" in legend and "◆✓ reached" in legend


# ---- TC-4820 / LLR-4603.11 / R-7 / SEC-1, SEC-2, SEC-7 -------------------------
DANGER = ["a]b[/]", "[@click=app.quit]x", "x\\", "里程碑 frozen", "étape"]
LONG = {"a]b[/]": "a]b[/] a]b[/] a]b[/]",
        "[@click=app.quit]x": "[@click=app.quit]x [@click=app.quit]x",
        "x\\": "x\\" * 6,
        "里程碑 frozen": "里程碑 frozen 里程碑 frozen",
        "étape": "étape" * 3}


def _lab_board(place: str, title: str, W: int):
    """A `Lab bench` group whose selected milestone `ts` lands its title `place`:
    `after` (a twin shares its cell, so the `bright` count digit sits next to the
    title run, A-8), `before` (a reached one on the field's last day) or `cut`
    (neighbours leave 5 cells before and 9 after)."""
    lab = [T("lb", "pb", "Bench run", "Doing", -1, 12)]
    if place == "after":
        lab += [T("s", "pb", title, "Next", None, 2, True, "delivery"),
                T("s2", "pb", "zz twin", "Next", None, 2, True, "delivery")]
    elif place == "before":
        probe = Frame(mrf(), "tstore", W, 0)
        last = probe.ax.day(probe.ax.w - 1)
        lab += [T("s", "pb", title, "Done", None, _due_off(last), True, "payment")]
    else:
        lab += [T("n1", "pb", "Left gate", "Next", None, 2, True, "review"),
                T("s", "pb", LONG[title], "Next", None, 6, True, "delivery"),
                T("n2", "pb", "Right gate", "Next", None, 12, True, "review")]
    return _with(*lab, projects=[P("pb", "Lab bench")]), [t.id for t in lab if t.milestone]


def _no_live_spans(text: Text):
    for sp in text.spans:
        st = sp.style
        if isinstance(st, str):
            assert "@click" not in st, st
        else:
            assert not st.meta and "@click" not in str(st), st


CASES = ([(p, t, 118) for p in ("after", "before", "cut") for t in DANGER]
         + [("cut", t, 80) for t in DANGER])


@pytest.mark.parametrize("place,title,W", CASES,
                         ids=[f"{p}-{i}-{w}" for p, i, w in
                              [(p, DANGER.index(t), w) for p, t, w in CASES]])
def test_TC_4820_LLR_4603_11_a_field_label_draws_its_literal_text_in_cells(place, title, W):
    """R-7: markup brackets, a backslash, wide and zero-width glyphs in the
    selected title, drawn after its mark, before it and cut with `…` (at 118, and
    the cut again at 80, SEC-7) → 0 exceptions; the field holds the exact title or
    its `fit` cut ending in `…`; no span carries `@click` or any meta; the
    milestone row's `cell_len` = the width, every other line ≤ (N-10). Goes through
    the real seat (`collapse_runs` + `Text.from_markup`, A-8). NC: one character
    per cell through `c()` (`a]b[/]` raises `MarkupError`); NC 2: room measured
    with `len` (the wide title's line too wide)."""
    b, ids = _lab_board(place, title, W)
    f = Frame(b, "ts", W, 0)
    i = f.lm["ts"]
    field = "".join(f.fcells(i))
    full = LONG[title] if place == "cut" else title
    if place == "cut":
        cuts = [views.fit(full, n) for n in range(6, cell_len(full))]
        piece = next((p for p in sorted(cuts, key=len, reverse=True) if p in field), None)
        assert piece is not None and piece.endswith("…"), (place, title, f.lines[i])
    else:
        piece = full
        assert piece in field, (place, title, f.lines[i])
    start = cell_len(field[:field.index(piece)])
    x = f.cell("ts")
    if place == "after":
        assert start > x
    elif place == "before":
        assert start + cell_len(piece) < f.ax.w - 2
    assert f.lane_line(ids) == i
    assert cell_len(f.lines[i]) == W, f.lines[i]
    assert max(cell_len(ln) for ln in f.lines) <= W
    _no_live_spans(f.text)


# =============================================================================
# 4.4 Navigation (HLR-4604) — through keys, the real app
# =============================================================================
def test_TC_4831b_LLR_4604_1_the_nav_column_holds_one_stop_per_row():
    """Layer 0 (graph example): the gantt nav column is one column, each
    milestone row one id (its stop) before the group's tasks."""
    cols = views.nav_model("gantt", mrf(), False, TODAY, 118, 30, selected_id="tstore")
    assert cols == [["tm3", "tstore", "ttele", "ttrain", "trota", "tg1", "tgq", "tgr", "tgx",
                     "th1", "tha", "thr", "ti1", "tip"]]


async def test_TC_4831_LLR_4604_1_up_down_stop_on_the_row_once(home):
    """From `Pilot store list`: `↑` → a Pilot rollout milestone; `↑` again → no
    move (the first group); `↓`×2 from the row → `Pilot telemetry`. NC: one stop
    per milestone."""
    async with gantt(home) as (app, pilot):
        await keys(pilot, "up")
        first = app.selected_task_id
        assert first in PILOT
        await keys(pilot, "up")
        assert app.selected_task_id == first
        await keys(pilot, "down", "down")
        assert app.selected_task_id == "ttele"


def test_TC_4832_LLR_4604_2_landing_on_a_row_selects_its_anchor():
    """The stop `↑↓` land on: Pilot rollout → m3 (m1 reached, m2 late); a row of
    only late ones → the first late; only reached ones (open work in the group) →
    the first. Read from the nav column: the id right before the group's first
    task. NC: the first in walk order (m1)."""
    late = [T("lt", "pl", "Late prep", "Doing", -2, 5),
            T("l1", "pl", "Missed gate", "Next", None, -3, True, "review"),
            T("l2", "pl", "Slipped gate", "Next", None, -1, True, "delivery")]
    done = [T("rt", "pr2", "Close-out", "Doing", -2, 6),
            T("r1", "pr2", "Paid gate", "Done", None, -5, True, "payment"),
            T("r2", "pr2", "Signed gate", "Done", None, -2, True, "review")]
    b = _with(*late, *done, projects=[P("pl", "Late gates"), P("pr2", "Reached gates")])
    col = views.nav_model("gantt", b, False, TODAY, 118, 0, selected_id="tstore")[0]
    for task, want in (("tstore", "tm3"), ("tlt", "tl1"), ("trt", "tr1")):
        assert col[col.index(task) - 1] == want, (task, col)


async def test_TC_4832b_LLR_4604_2_up_lands_on_the_anchor(home):
    async with gantt(home) as (app, pilot):
        await keys(pilot, "up")
        assert app.selected_task_id == "tm3"


async def test_TC_4833_LLR_4604_3_right_walks_to_the_next_in_walk_order(home):
    """m3 → m4 (same day, after m3) → m5. NC: skip same-day ones (m3 → m5)."""
    async with gantt(home, sel="tm3") as (app, pilot):
        await keys(pilot, "right")
        assert app.selected_task_id == "tm4"
        await keys(pilot, "right")
        assert app.selected_task_id == "tm5"


async def test_TC_4834_LLR_4604_4_left_walks_back(home):
    """m3 → m2 → m1. NC: `←` moves forward."""
    async with gantt(home, sel="tm3") as (app, pilot):
        await keys(pilot, "left")
        assert app.selected_task_id == "tm2"
        await keys(pilot, "left")
        assert app.selected_task_id == "tm1"


async def test_TC_4835_LLR_4604_5_the_ends_keep_the_selection(home):
    """m1 + `←` → m1; m5 + `→` → m5; no other group's milestone. NC: wrap
    around. Passes on base by design (`hmove` is a no-op in the gantt there)."""
    async with gantt(home, sel="tm1") as (app, pilot):
        await keys(pilot, "left")
        assert app.selected_task_id == "tm1"
        app.selected_task_id = "tm5"
        app.refresh_view()
        await keys(pilot, "right")
        assert app.selected_task_id == "tm5"


async def test_TC_4836_LLR_4604_6_off_the_row_left_right_are_base(home):
    """A task selected in the gantt → unchanged by `←`/`→`; the kanban → base's
    next-column jump; no selection in the gantt → base `_select_first`. NC: `→`
    on a task row jumps to its group's row. Passes on base by design."""
    async with gantt(home, sel="tstore") as (app, pilot):
        await keys(pilot, "left")
        assert app.selected_task_id == "tstore"
        await keys(pilot, "right")
        assert app.selected_task_id == "tstore"
        app.selected_task_id = None
        app._select_first()                          # base's own pick, read first
        want = app.selected_task_id
        app.selected_task_id = None          # no refresh: it re-selects (E4 I-T1)
        await keys(pilot, "right")
        assert app.selected_task_id == want
        await keys(pilot, "4")                       # the kanban
        cols = app._nav_columns()
        here = next(ci for ci, c in enumerate(cols) if app.selected_task_id in c)
        nxt = next((c[0] for c in cols[here + 1:] if c), app.selected_task_id)
        await keys(pilot, "right")
        assert app.selected_task_id == nxt


async def test_TC_4837_LLR_4604_7_enter_opens_the_walked_milestone(home):
    """m3, `→`, `enter` → `TaskDetails` of m4. NC: the anchor's (m3)."""
    from taskboard.modals import TaskDetails
    async with gantt(home, sel="tm3") as (app, pilot):
        await keys(pilot, "right", "enter")
        assert isinstance(app.screen, TaskDetails)
        assert app.screen._detail_task.id == "tm4"


async def test_TC_4838_LLR_4604_8_task_keys_act_on_the_walked_milestone(home):
    """m3, `→`, `]` → m4 one phase on (Next → Doing), m3 unchanged; `e` → the
    editor holds m4's title. NC: the row's stop stays the anchor."""
    async with gantt(home, sel="tm3") as (app, pilot):
        await keys(pilot, "right", "right_square_bracket")
        assert app.board.task_by_id("tm4").phase == "Doing"
        assert app.board.task_by_id("tm3").phase == "Next"
        await keys(pilot, "e")
        assert app.screen.query_one("#f-title").value == "Store list frozen"
        await keys(pilot, "escape")


# =============================================================================
# 4.5 Search and hidden classes (HLR-4605, D3, R-4)
# =============================================================================
def test_TC_4841_LLR_4605_1_a_query_keeps_only_the_matching_milestones_on_the_row():
    """`/store` → Pilot rollout's row draws only m4 (`◆ 1 milestone`); no other
    group draws a milestone row. NC: the row from the unfiltered board."""
    fb = views.filtered_board(mrf(), "store", False)
    f = Frame(fb, "tstore")
    i = f.lm["tm4"]
    assert i == f.span_of("Pilot rollout") + 1
    assert f.label(i).strip() == "◆ 1 milestone", f.lines[i]
    assert [ch for ch in f.fcells(i) if ch in MARKS] == ["▲"]
    assert not any(k in f.lm for k in ("tm1", "tm2", "tm3", "tm5", "tg1", "tg2", "th1", "ti1"))


def test_TC_4842_LLR_4605_2_a_hidden_class_leaves_the_row():
    """Review hidden → Pilot rollout's row draws m1, m4, m5; the Oct 24 cell is
    `▲` with no count. NC: the row built before the class filter."""
    f = Frame(mrf(hidden={"review"}), "tstore")
    i = f.lane_line(["tm1", "tm4", "tm5"])
    assert "tm2" not in f.lm and "tm3" not in f.lm
    cells, x = f.fcells(i), f.cell("tm4")
    assert cells[x] == "▲" and not cells[x + 1].isdigit(), f.lines[i]
    assert sum(ch in MARKS for ch in cells) == 3, f.lines[i]


async def test_TC_4843_LLR_4605_3_the_walk_skips_what_the_row_does_not_draw(home):
    """Review hidden, m1 selected, `→`, `→` → m4, m5; `/store` + `←`/`→` → m4
    stays. NC: walk the unfiltered milestones."""
    async with gantt(home, sel="tm1", hidden=("review",)) as (app, pilot):
        await keys(pilot, "right")
        assert app.selected_task_id == "tm4"
        await keys(pilot, "right")
        assert app.selected_task_id == "tm5"
    async with gantt(home, sel="tm4") as (app, pilot):
        await keys(pilot, "slash", *"store", "enter")
        app.selected_task_id = "tm4"
        app.refresh_view()
        await keys(pilot, "left")
        assert app.selected_task_id == "tm4"
        await keys(pilot, "right")
        assert app.selected_task_id == "tm4"


def test_TC_4843b_R4_the_nav_column_holds_no_hidden_class_milestone():
    """R-4 regression (P-10, A-6): the test_legend fixture with class `payment`
    hidden, 118x30 → the nav column holds none of tc8, tcc, tce, which the frame
    does not draw; MR-F with Review hidden → no m2, m3. RED on base."""
    b = mmfx.build_board(Path("unused"), "client-a")
    from taskboard.marks import Mark
    b.marks = {cid: Mark(cid, n, s, k, hidden=(cid == "payment"))
               for cid, n, s, _h, k in mmfx.CLASSES}
    col = views.nav_model("gantt", b, False, TODAY, 118, 30)[0]
    assert not {"tc8", "tcc", "tce"} & set(col), col
    col = views.nav_model("gantt", mrf(hidden={"review"}), False, TODAY, 118, 30,
                          selected_id="tstore")[0]
    assert not {"tm2", "tm3"} & set(col), col


async def test_TC_4843b_R4_the_cursor_never_stops_on_a_hidden_class_milestone(home):
    """R-4, through keys: Review hidden in `#`; from `Pilot store list`, `↑` to the
    top and `↓` through every row → no stop is m2 or m3, and every stop is drawn.
    RED on base (base `↑` lands on the hidden m2)."""
    async with gantt(home, hidden=("review",)) as (app, pilot):
        seen = []
        for k in ["up"] * 3 + ["down"] * 20:
            await keys(pilot, k)
            seen.append(app.selected_task_id)
        assert not {"tm2", "tm3"} & set(seen), seen
        drawn = set(screen(app)[:28])
        assert not any("Rubric sign-off" in ln or "Steering go/no-go" in ln for ln in drawn)


def test_TC_4843c_R4_the_stop_is_the_one_the_frame_draws():
    """MR-F with Review hidden, `store` selected → Pilot rollout's stop is m4 (m3
    is hidden). RED on base."""
    col = views.nav_model("gantt", mrf(hidden={"review"}), False, TODAY, 118, 30,
                          selected_id="tstore")[0]
    assert col[0] == "tm4", col


async def test_TC_4843d_A5_hiding_the_selected_milestones_class(home):
    """A-5 (N-3, SEC-5): m3 selected, hide Review in `#` → `↑` falls back to a
    drawn stop with 0 exceptions, `→` likewise; `enter` and `]` do not act on m3;
    no painted line names m3. NC: the selection stays on the hidden m3."""
    from taskboard.modals import TaskDetails
    async with gantt(home, sel="tm3") as (app, pilot):
        await hide_class(pilot, "review")
        await keys(pilot, "up")
        assert app.selected_task_id not in ("tm2", "tm3")
        await keys(pilot, "right")
        assert app.selected_task_id not in ("tm2", "tm3")
        assert not any("Steering go/no-go" in ln for ln in screen(app))
        await keys(pilot, "right_square_bracket")
        assert app.board.task_by_id("tm3").phase == "Next"
        await keys(pilot, "enter")
        if isinstance(app.screen, TaskDetails):
            assert app.screen._detail_task.id != "tm3"


# =============================================================================
# 4.6 Link mode and the paged fold (HLR-4606.1, HLR-4606.2)
# =============================================================================
GOLDEN = Path(__file__).with_name("milestone_row_link_golden.json")


def _golden(size):
    import json
    return json.loads(GOLDEN.read_text(encoding="utf-8"))["frames"][f"{size[0]}x{size[1]}"]


@pytest.mark.parametrize("size", [(118, 30), (80, 24)])
async def test_TC_4851_LLR_4606_1_the_link_frame_keeps_one_row_per_milestone(home, size):
    """m4 selected, `L` → the link frame draws m1..m5 one row each, byte-equal to
    base's frame (golden captured from base 154e260 by the tester, R-3). NC: the
    shared row in the link frame. Passes on base by design."""
    async with gantt(home, size=size, sel="tm4") as (app, pilot):
        await keys(pilot, "L")
        assert app.screen.waiter.id == "tm4"
        t = app.screen.query_one("#glink-frame").content
        g = _golden(size)
        assert t.plain == g["plain"]
        assert t.markup == g["markup"]


async def test_TC_4852_LLR_4606_2_L_on_a_walked_milestone_makes_it_the_waiter(home):
    """m3, `→` (m4), `L` → the waiter is m4. NC: the anchor (m3)."""
    async with gantt(home, sel="tm3") as (app, pilot):
        await keys(pilot, "right", "L")
        assert app.screen.waiter.id == "tm4"


REST = re.compile(r"^ ◆ \d+ (milestones?|ms)\b")


async def test_TC_4853_LLR_4606_3_closing_the_link_mode_brings_the_rows_back(home):
    """`L`, `esc` → the gantt equals the gantt before `L`; `L`, a candidate,
    `enter` → 4 milestone rows again. NC: a flag left set by the link frame."""
    async with gantt(home) as (app, pilot):
        before = screen(app)[:27]
        await keys(pilot, "L", "escape")
        assert screen(app)[:27] == before
        await keys(pilot, "L", "enter")
        rows = screen(app)[:27]
        assert sum(bool(REST.match(ln)) for ln in rows) == 4, "\n".join(rows)


def _big_board():
    tasks = [T(f"b{n:02}", "pg", f"Big task {n:02}", "Next", -2, n) for n in range(1, 21)]
    tasks += [T("bm1", "pg", "Big gate one", "Next", None, 5, True, "delivery"),
              T("bm2", "pg", "Big gate two", "Next", None, 12, True, "review")]
    b = models.Board([P("pg", "Big rollout", due=25)], tasks, Path("big.json"),
                     fx.settings(), fx.PHASES)
    b.marks = fx.marks()
    return b, tasks


def test_TC_4854_LLR_4606_4_a_selected_member_selects_the_page_holding_the_row():
    """A group of one milestone row + 20 tasks at 118x14, a member selected → the
    page starts with the row and the hint reads `▼ 13 below` (body 10 with the
    strip, page of 8; the hint counts task rows off the page). NC: page by the
    milestone's base row index."""
    b, _t = _big_board()
    f = Frame(b, "tbm1", 118, 14)
    i = f.lane_line(["tbm1", "tbm2"])
    assert i == f.span_of("Big rollout") + 1
    hint = next(ln for ln in f.lines if "below" in ln or "above" in ln)
    assert "▼ 13 below" in hint and "above" not in hint, hint


@pytest.mark.parametrize("sel,label,glyph,tone", [
    ("tm3", "■ Steering go/no-go 1/2", "■", "violet"),
    ("tm4", "▲ Store list frozen 2/2", "▲", "cyan")])
def test_TC_4855_LLR_4606_5_only_spans_and_the_selection_draws_the_row(sel, label, glyph, tone):
    """MR-F at 118x6 (body 2, D8) → Pilot rollout's span row, then the milestone
    row: label `<glyph> <title> i/N`, the mark reverse. NC: base `task_row(sel)`."""
    f = Frame(mrf(), sel, 118, 6)
    s = f.span_of("Pilot rollout")
    i = f.lm[sel]
    assert i == s + 1
    assert re.sub(" +", " ", f.label(i).strip()) == label, f.lines[i]
    x = f.cell(sel)
    assert f.fcells(i)[x:x + 2] == [glyph, "2"], f.lines[i]
    st = f.fstyle(i, x)
    assert st.reverse and fx.hexof(st) == HEX[tone]
