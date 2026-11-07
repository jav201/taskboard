"""Inc MR-b — the presentation's milestones share one row (LLR-4651.1 .. LLR-4654.1).

Layer 0 over the shipped seats `render_present` (views 1 `gantt`, 2 `split`) and
`render_present_all` (view 3 `all`), plus the pilot where an LLR is about keys.
Every frame is read after `to_text`: the plain cells of `Text.plain`, measured with
`cell_len`, and the Style painted at a cell — never the markup (SEC-B2).

Why: the operator presents a project to a room (US-4651). One row per milestone
spends the room's screen on dates; the board gantt already draws a project's
milestones on one row (MR-a), so `R` follows it, and the arrows still stop at each
milestone one by one with the keys already learned.

Fixture MR-F (`milestone_row_fixture.py`), TODAY 2026-10-20; ids `t<key>`,
projects `ppr` Pilot rollout, `ppe` Eval harness, `ppd` Docs & handover.
Base revision: 8ca174c (MR-a merged). The base oracle (`milestone_row_present_base.json`)
was captured on a worktree at 8ca174c by `.dev-flow/2026-11-06-v3-incMRb/evidence/capture_base.py`.
TC ids: LLR-4651.n -> TC-(4900+n), LLR-4652.n -> TC-(4910+n) (LLR-4652.10 -> TC-4920),
LLR-4653.n -> TC-(4920+n), LLR-4654.n -> TC-(4930+n).
"""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

import pytest
from rich.cells import cell_len

import milestone_row_fixture as fx
import milestone_row_present_fixture as mp
from milestone_row_present_fixture import GROUND, MS_GLYPHS, PILOT_MS_TITLES, PILOT_TASKS
from taskboard import app as app_module
from taskboard import models, views

TODAY = fx.TODAY
T = fx.task
HEX = {k: v.lower() for k, v in views.HEX.items()}


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


def _hex(st):
    return fx.hexof(st)


def _walk(b, pid):
    """The drawn milestones of `pid` in walk order — the oracle's own statement of
    the board gantt's rule `(due is None, due or date.max, title, id)` (SEAM-1)."""
    ms = [t for t in views.present_tasks_m(b, pid)[0] if t.milestone]
    return tuple(sorted(ms, key=lambda t: (t.due_date is None, t.due_date or "9999-12-31",
                                           t.title, t.id)))


def _expected_field(cells) -> str:
    """`gantt_milestone_row`'s (glyph, tone) cells as the plain field shows them: a
    run's text in its first cell, a consumed cell (`""`) adds nothing, a blank is
    the ground (read as one blank, as `norm` reads the frame)."""
    return "".join(" " if g == " " else g for g, _tone in cells)


def _ms_row12(rows):
    """Views 1/2: the milestone row is the line directly under the span row."""
    return rows.span() + 1


def _ms_row3(rows, name):
    return rows.head(name) + 1


def _alone(field: str, x: int, glyph: str) -> bool:
    """The cell holds `glyph` with no count digit / `+` beside it."""
    return field[x] == glyph and (x + 1 >= len(field) or not re.match(r"[0-9+]", field[x + 1]))


# =============================================================================
# 4.1 the row (HLR-4651)
# =============================================================================
@pytest.mark.parametrize("view", mp.VIEWS12)
def test_TC_4901_LLR_4651_1_one_milestone_row_directly_under_the_span(view):
    """TC-4901 (LLR-4651.1, HLR-4651): MR-F *Pilot rollout*, views 1 and 2 at 118x30,
    no cursor → line 4 the span, line 5 the milestone row (the marks of m2..m5),
    lines 6-9 the 4 tasks, line 10 the rule; no other field line holds a milestone
    mark; 5 field body rows (base 8). RED on base: one row per milestone (8 rows,
    marks on lines 5, 7, 8, 11)."""
    r = mp.frame(fx.board(), "ppr", None, 118, 30, view)
    assert (r.span(), r.rule()) == (4, 10), r.lines[:12]
    assert r.rule() - r.span() - 1 == 5                       # HLR-4651: 5 body rows
    assert [i for i in range(r.span() + 1, r.rule()) if r.has_mark(i)] == [5], r.lines[4:13]
    for i in range(6, 10):                                    # the task rows carry no mark
        assert not MS_GLYPHS & set(r.label(i)), (i, r.label(i))


def test_TC_4902_LLR_4651_2_view_3_one_row_under_each_head():
    """TC-4902 (LLR-4651.2): MR-F, `3`, 118x30 → heads at lines 3, 10, 16; one
    milestone row each, the line directly under its head (4: m2..m5; 11: `▲` g1 and
    `■` g2; 17: `◆` h1); no other line of a project holds a mark; 3/3. NC: no row in
    view 3 (per-task rows kept) — RED on base."""
    r, _pa = mp.frame3(fx.board(), ("proj", "ppr"), 118, 30)
    names = ("Pilot rollout", "Eval harness", "Docs & handover")
    heads = [r.head(n) for n in names]
    assert heads == [3, 10, 16], r.lines[:20]
    ends = heads[1:] + [len(r)]
    for h, end in zip(heads, ends):
        assert [i for i in range(h + 1, end) if r.has_mark(i)] == [h + 1], (h, r.lines[h:end])
    assert {"▲", "■"} <= set(r.field(11)), r.field(11)
    assert "◆" in r.field(17), r.field(17)


@pytest.mark.parametrize("case", ["all", "review_hidden", "m3_hidden"])
@pytest.mark.parametrize("view", [1, 3])
def test_TC_4903_LLR_4651_3_the_row_holds_exactly_the_drawn_milestones(case, view):
    """TC-4903 (LLR-4651.3): Pilot rollout's row → {m2, m3, m4, m5} with the reached
    m1 absent (no `⬢`/`⬡` anywhere on the row); class Review hidden in `#` → {m4, m5};
    m3 hidden by `space` → {m2, m4, m5} with m4 alone in its cell (`▲`, no count);
    views 1 and 3 at 118x30; 6/6. NC: include the reached m1 → RED."""
    hidden = ("review",) if case == "review_hidden" else ()
    b = fx.board(hidden=hidden)
    if case == "m3_hidden":
        b.task_by_id("tm3").show_in_present = False
    if view == 1:
        r = mp.frame(b, "ppr", "tstore", 118, 30)
        ax, i = mp.axis12(b, "ppr", 118), _ms_row12(r)
    else:
        r, pa = mp.frame3(b, ("task", "tstore"), 118, 30)
        ax, i = mp.axis3(b, pa.timeline_w), _ms_row3(r, "Pilot rollout")
    f = r.field(i)
    at = {k: mp.due_cell(r, b, f"t{k}", ax) for k in ("m2", "m3", "m5")}
    assert "⬢" not in f and "⬡" not in f, f                 # the reached m1 (payment) absent
    assert f[at["m5"]] == "★", f
    if case == "all":
        assert f[at["m2"]] == "■" and f[at["m3"]:at["m3"] + 2] == "■2", f
    elif case == "review_hidden":
        assert f[at["m2"]] == " " and _alone(f, at["m3"], "▲"), f
        assert "■" not in f, f
    else:
        assert f[at["m2"]] == "■" and _alone(f, at["m3"], "▲"), f


@pytest.mark.parametrize("view", ["gantt", "split", "all"])
def test_TC_4904_LLR_4651_4_tasks_one_per_row_in_base_order_under_the_row(view):
    """TC-4904 (LLR-4651.4): Pilot rollout's 4 tasks, one per field row in their base
    order (`Pilot store list`, `Pilot telemetry`, `Train store staff`, `Field support
    rota`) directly under the milestone row; views 1, 2, 3; 3/3. NC: sort by title →
    RED. RED on base: the lines under the span interleave milestones."""
    b = fx.board()
    if view == "all":
        r, _pa = mp.frame3(b, ("proj", "ppr"), 118, 30)
        top = _ms_row3(r, "Pilot rollout") + 1
    else:
        r = mp.frame(b, "ppr", None, 118, 30, view)
        top = _ms_row12(r) + 1
    for k, title in enumerate(PILOT_TASKS):
        lab = r.label(top + k)
        assert lab.startswith("  ▎ ") and lab[4:].startswith(title[:12]), (top + k, lab)


@pytest.mark.parametrize("view", [1, 3])
def test_TC_4905_LLR_4651_5_no_drawn_milestone_no_row(view):
    """TC-4905 (LLR-4651.5): *Docs & handover* with h1 hidden by `space` → the field is
    its span (view 1) or head (view 3) and its 2 task rows (`API reference`, `Runbook
    draft`), no milestone row; a project with no milestone at all → likewise; 3/3
    (the PRES-V3 board stays byte-equal in `test_present.py`). NC: always emit the
    row → RED. Passes on base by design (base draws no row of its own)."""
    b = fx.board(extra=[T("za", "pz", "Zeta intake", "Doing", -2, 4),
                        T("zb", "pz", "Zeta wrap-up", "Next", 3, 9)],
                 extra_projects=[fx.project("pz", "Zeta pilot")])
    b.task_by_id("th1").show_in_present = False
    for pid, name, want in (("ppd", "Docs & handover", ["API reference", "Runbook draft"]),
                            ("ppz", "Zeta pilot", ["Zeta intake", "Zeta wrap-up"])):
        if view == 1:
            r = mp.frame(b, pid, None, 118, 30)
            body = list(range(r.span() + 1, r.rule()))
        else:
            r, _pa = mp.frame3(b, ("proj", pid), 118, 40)
            h = r.head(name)
            body = []
            for i in range(h + 1, len(r)):
                if not r.lines[i].strip() or i in r.heads():
                    break
                body.append(i)
        assert len(body) == 2, (pid, [r.lines[i] for i in body])
        assert not any(r.has_mark(i) for i in body), (pid, [r.lines[i] for i in body])
        for i, title in zip(body, want):
            assert r.label(i)[4:].startswith(title[:12]), (pid, r.label(i))


def test_TC_4906_LLR_4651_6_a_folded_project_draws_no_row():
    """TC-4906 (LLR-4651.6): `enter` on *Eval harness* (folded) at 118x30 → its head
    `▸`, then the next head, no milestone row between and no stop for tg1/tg2; at
    80x14 the overflow folds `ppd` then `ppe` → `▸` heads with no row under them; the
    cursor's project still draws its row (the positive control); 2/2. NC: draw the
    row under a folded head → RED. The positive control is RED on base (no row)."""
    b = fx.board()
    r, pa = mp.frame3(b, ("proj", "ppr"), 118, 30, frozenset({"ppe"}))
    h = r.head("Eval harness")
    assert r.lines[h].startswith("▸"), r.lines[h]
    nxt = r.head("Docs & handover")
    assert not any(r.has_mark(i) for i in range(h + 1, nxt)), r.lines[h:nxt]
    assert ("proj", "ppe") in pa.stops
    assert not {("task", "tg1"), ("task", "tg2"), ("task", "tgq")} & set(pa.stops), pa.stops
    r, pa = mp.frame3(b, ("proj", "ppr"), 80, 14)
    for name in ("Eval harness", "Docs & handover"):
        h = r.head(name)
        assert r.lines[h].startswith("▸"), (name, r.lines)
        assert h + 1 >= len(r) or not r.has_mark(h + 1), (name, r.lines)
    p = r.head("Pilot rollout")
    assert r.has_mark(p + 1) and [i for i in range(p + 1, r.head("Eval harness"))
                                  if r.has_mark(i)] == [p + 1], r.lines


def test_TC_4907_LLR_4651_7_the_row_counts_as_one_row_for_the_overflow():
    """TC-4907 (LLR-4651.7): MR-F view 3 at 118x18 (room 15): need = 6 + 5 + 4 = 15 →
    no project folded (base folds Eval harness and Docs & handover, P-4); the 15 body
    lines are 3 heads + 3 milestone rows + 9 task rows, no gap line; every task is a
    stop; 2/2. NC: count one row per milestone in `need` → folds → RED. RED on base."""
    r, pa = mp.frame3(fx.board(), ("proj", "ppr"), 118, 18)
    heads = r.heads()
    assert heads == [3, 9, 14], r.lines
    assert not any(r.lines[h].startswith("▸") for h in heads), r.lines
    assert all(r.lines[i].strip() for i in range(3, 18)), r.lines          # no gap: 15 rows
    assert sum(r.has_mark(i) for i in range(3, 18) if i not in heads) == 3
    tasks = {f"t{k}" for k, *_ in fx.TASKS} - {"tm1", "ti1", "tip"}
    assert {s[1] for s in pa.stops if s[0] == "task"} == tasks, pa.stops
    assert len(pa.stops) == 3 + len(tasks)


@pytest.mark.parametrize("size", mp.SIZES)
@pytest.mark.parametrize("view", [1, 3])
def test_TC_4908_LLR_4651_8_the_rows_dependency_gutter_is_blank(view, size):
    """TC-4908 (LLR-4651.8, RB-5): m3 waits on the open task `store`; views 1 and 3 at
    118x30 and 80x24 with the cursor on m3 → the milestone row's gutter cell (the cell
    after the present label column) is a blank, and no line shows the `↳` base draws
    in m3's own row's gutter; 4/4. NC: draw the cursor milestone's `gantt_dep_mark` in
    the gutter → RED. RED on base (`↳` in m3's row)."""
    W, H = size
    b = fx.board()
    b.task_by_id("tm3").depends_on = ["tstore"]
    if view == 1:
        r = mp.frame(b, "ppr", "tm3", W, H)
        i = _ms_row12(r)
    else:
        r, _pa = mp.frame3(b, ("task", "tm3"), W, H)
        i = _ms_row3(r, "Pilot rollout")
    assert r.label(i).startswith(" ⟦▎"), r.label(i)          # the row is m3's (the cursor's)
    assert r.gutter(i) == " ", (r.gutter(i), r.lines[i])
    assert not any("↳" in ln for ln in r.lines), [ln for ln in r.lines if "↳" in ln]


# =============================================================================
# 4.2 the row's drawing (HLR-4652)
# =============================================================================
@pytest.mark.parametrize("width", [118, 80])
@pytest.mark.parametrize("cursor", ["tm3", "tm4", "tstore"])
@pytest.mark.parametrize("view", [1, 3])
def test_TC_4911_LLR_4652_1_the_field_is_the_board_gantts_row(view, cursor, width):
    """TC-4911 (LLR-4652.1): views 1 and 3 at 118 and 80, the cursor on m3, on m4, on a
    task → the row's field cells are `gantt_milestone_row(lane, sel, board, ax, today)`
    on the view's own axis (`sel` the cursor milestone, else None), over the field's
    ground. NC: select the anchor (the cell's first member, m3) in place of the cursor
    milestone (m4) → `■2 Steerin…` where `▲2 Store l…` is due → RED. RED on base."""
    H = 30 if width == 118 else 24
    b = fx.board()
    lane = _walk(b, "ppr")
    sel = cursor if cursor.startswith("tm") else None
    if view == 1:
        r = mp.frame(b, "ppr", cursor, width, H)
        i, ax = _ms_row12(r), mp.axis12(b, "ppr", width)
    else:
        r, pa = mp.frame3(b, ("task", cursor), width, H)
        i, ax = _ms_row3(r, "Pilot rollout"), mp.axis3(b, pa.timeline_w)
    want = _expected_field(views.gantt_milestone_row(lane, sel, b, ax, TODAY))
    assert r.field(i) == mp.norm(want), (r.field(i), want)
    rev = [x for x in range(r.field_w) if (st := r.fstyle(i, x)) is not None and st.reverse]
    if sel is None:
        assert rev == [], rev
    else:
        assert len(rev) == 1, rev
    if view == 1 and width == 118:               # the graph's own literals (P-6)
        f = r.field(i)
        if cursor == "tm3":
            assert "■2 Steerin…" in f and rev == [18], (f, rev)
            assert _hex(r.fstyle(i, 18)) == HEX["violet"]
        elif cursor == "tm4":
            assert "▲2 Store l…" in f and rev == [18], (f, rev)
            assert _hex(r.fstyle(i, 18)) == HEX["cyan"]
        else:
            assert "■ ▲1d" in f and "■2 Oct 24" in f and "★ Oct 30" in f, f
    if view == 1 and width == 80 and cursor == "tstore":
        f = r.field(i)
        assert "▲1d ■" in f and "■2" in f and "★ Oct 30" in f, f


def test_TC_4912_LLR_4652_2_a_reversed_mark_and_a_covered_label_paint_once():
    """TC-4912 (LLR-4652.2): view 1 118x30, cursor on m2 → field cell 8 is `■` in
    reverse video, bold, in its class style (violet); the `Rubric…` run is painted
    once over its cells — no doubled glyph, no stray tone name in the plain; the
    field is exactly 73 cells. NC: `_present_field` unchanged (reads `rev:…` as a
    style name: KeyError) → RED. RED on base (m2's own row: the cursor accent echo)."""
    b = fx.board()
    r = mp.frame(b, "ppr", "tm2", 118, 30)
    i = _ms_row12(r)
    st = r.fstyle(i, 8)
    assert r.fcells(i)[8] == "■" and st.reverse and st.bold, (r.fcells(i)[8], st)
    assert _hex(st) == HEX["violet"], st
    f = r.field(i)
    assert len(r.fcells(i)) == 73 and cell_len(f) == 73
    assert f.count("Rubric…") == 1 and f.count("■") == 2, f
    for word in ("rev:", "run:", "violet", "bright", "accent"):
        assert word not in r.lines[i], (word, r.lines[i])


@pytest.mark.parametrize("view, width, want", [
    (1, 118, "  ▎ ◆ 4 milestones ▲1"), (1, 80, "  ▎ ◆ 4 ms ▲1"),
    (3, 118, "  ▎ ◆ 4 ms ▲1"), (3, 80, "  ▎ ◆ 4 ms ▲1")])
def test_TC_4913_LLR_4652_3_the_label_at_rest(view, width, want):
    """TC-4913 (LLR-4652.3): the cursor on a task → the row's present label column reads
    ` `, a blank lead, the hue bar `▎` and LLR-4603.6's text: `◆ 4 milestones ▲1` at
    label 30 (`label_w - 3` = 27 ≥ 24), `◆ 4 ms ▲1` at label 20; the late count in
    `over`; view 1 at 118 and 80 (the threshold) and view 3. NC: drop the late count →
    RED. RED on base (m2's own row)."""
    H = 30 if width == 118 else 24
    b = fx.board()
    if view == 1:
        r = mp.frame(b, "ppr", "tstore", width, H)
        i = _ms_row12(r)
    else:
        r, _pa = mp.frame3(b, ("task", "tstore"), width, H)
        i = _ms_row3(r, "Pilot rollout")
    lab = r.label(i)
    assert lab.rstrip() == want, (lab, want)
    assert _hex(r.style(i, lab.index("▲1"))) == HEX["over"]
    assert _hex(r.style(i, 2)) == HEX["indigo"]                # the project's hue bar


@pytest.mark.parametrize("cursor, width, want", [
    ("tm4", 118, " ⟦▎ ▲ Store list frozen   2/2"), ("tm4", 80, " ⟦▎ ▲ Store li… 2/2"),
    ("tm2", 118, " ⟦▎ ■ Rubric sign-off"), ("tm2", 80, " ⟦▎ ■ Rubric sign-…")])
def test_TC_4914_LLR_4652_4_the_label_on_a_milestone(cursor, width, want):
    """TC-4914 (LLR-4652.4, RB-3): the cursor on m4 → ` ⟦▎ ▲ Store list frozen   2/2`
    at 118 and ` ⟦▎ ▲ Store li… 2/2` at 80 (cut by cell width with `…`, the tag kept);
    on m2 → ` ⟦▎ ■ Rubric sign-off` / ` ⟦▎ ■ Rubric sign-…`; the lead `⟦` in accent;
    4/4. NC: the lead `⟦` absent → RED. RED on base for 3/4 (base's line 5 is m2's
    own row; at 80 it reads `Rubric sign-o…`); m2 at 118 passes on base by design."""
    H = 30 if width == 118 else 24
    r = mp.frame(fx.board(), "ppr", cursor, width, H)
    i = _ms_row12(r)
    assert r.label(i).rstrip() == want, (r.label(i), want)
    assert _hex(r.style(i, 1)) == HEX["accent"]


@pytest.mark.parametrize("case", ["cursor_m2", "cursor_task", "only_late"])
def test_TC_4915_LLR_4652_5_the_rows_chip(case):
    """TC-4915 (LLR-4652.5): the cursor on m2 → its base chip `    due Oct 19` in
    `over`; the cursor on a task → m3's (`    due Oct 24`, the first due on or after
    today in walk order); a row of only late ones (m3, m4, m5 hidden), the cursor on a
    task → 14 blanks; 3/3. NC: the first milestone's chip (m2's) with the cursor
    elsewhere → RED."""
    b = fx.board()
    cursor = "tm2" if case == "cursor_m2" else "tstore"
    if case == "only_late":
        for k in ("tm3", "tm4", "tm5"):
            b.task_by_id(k).show_in_present = False
    r = mp.frame(b, "ppr", cursor, 118, 30)
    i = _ms_row12(r)
    assert r.has_mark(i), r.lines[i]
    want = {"cursor_m2": "    due Oct 19", "cursor_task": "    due Oct 24",
            "only_late": " " * 14}[case]
    assert r.chip(i) == want, (r.chip(i), want)
    if case == "cursor_m2":
        assert _hex(r.style(i, r.W - 1)) == HEX["over"]


HOSTILE_MS = ["a]b[/]", "[@click=app.quit]x", "\\", "日本語のタイトル"]


@pytest.mark.parametrize("title", HOSTILE_MS)
@pytest.mark.parametrize("view", [1, 3])
def test_TC_4916_LLR_4652_6_hostile_milestone_titles_are_literal(view, title):
    """TC-4916 (LLR-4652.6, R-7): a milestone titled `a]b[/]`, `[@click=app.quit]x`,
    `\\` or `日本語のタイトル` is the cursor milestone, views 1 and 3 at 80x24 → the
    row's label holds the title (or its `…` cut) literally; every line of the frame is
    exactly 80 cells after `to_text`; no span carries `@click` or meta; 0 exceptions;
    8/8. NC: build the label column with the title unescaped → RED. RED on base (the
    row is not the cursor's; the `\\` brief is 81 cells)."""
    b = fx.board(extra=[T("mx", "pr", title, "Next", None, 2, True, "review")])
    if view == 1:
        text = views.render_present(b, "ppr", "tmx", TODAY, 80, 24)
        r = mp.Rows(text, 80)
        i = _ms_row12(r)
    else:
        pa = views.render_present_all(b, ("task", "tmx"), TODAY, 80, 24)
        text = pa.frame
        r = mp.Rows(pa.timeline, pa.timeline_w)
        i = _ms_row3(r, "Pilot rollout")
    lab = r.label(i)
    assert lab.startswith(" ⟦▎ ■ "), lab
    assert mp.literal_cut(lab[6:], title), (lab, title)
    assert [w for w in mp.Rows(text, 80).widths() if w != 80] == [], mp.Rows(text, 80).widths()
    for sp in text.spans:
        st = sp.style
        assert "@click" not in str(st), st
        assert not getattr(st, "meta", None), st


@pytest.mark.parametrize("size", [(118, 30), (100, 30), (80, 24)])
@pytest.mark.parametrize("view", ["gantt", "split", "all"])
def test_TC_4917_LLR_4652_7_no_line_wider_than_the_terminal(view, size):
    """TC-4917 (LLR-4652.7): views 1, 2, 3 × {118x30, 100x30, 80x24} on MR-F, the
    cursor on m3 → every line's `cell_len` is the width (the frame and view 3's
    timeline); 9/9. NC: pass the board gantt's label width (30 at 80) → RED. Passes
    on base by design (base keeps the width on MR-F's titles)."""
    W, H = size
    b = fx.board()
    if view == "all":
        r, pa = mp.frame3(b, ("task", "tm3"), W, H)
        assert set(r.widths()) == {pa.timeline_w}, r.widths()
        assert set(mp.Rows(pa.frame, W).widths()) == {W}
    else:
        r = mp.frame(b, "ppr", "tm3", W, H, view)
        assert set(r.widths()) == {W}, r.widths()


@pytest.mark.parametrize("size", mp.SIZES)
@pytest.mark.parametrize("view", ["gantt", "split", "all"])
def test_TC_4918_LLR_4652_8_header_ruler_and_strip_as_at_base(view, size):
    """TC-4918 (LLR-4652.8, B-8): views 1, 2, 3 × {118x30, 80x24}, the SAME cursor m2
    on base and new → the header, the two ruler rows and the legend strip (views 1/2:
    lines 0-3; view 3: the timeline's lines 0-2) equal the base oracle captured on
    8ca174c; 6/6 (the hint row: AT-4655 and TC-4926). NC: count the milestone row in
    the header's open count → RED. Passes on base by design (the oracle is base's)."""
    W, H = size
    gold = mp.golden()["rows"][f"{view}-{W}x{H}"]
    b = fx.board()
    if view == "all":
        got = mp.frame3(b, ("task", "tm2"), W, H)[0].lines[:3]
    else:
        got = mp.frame(b, "ppr", "tm2", W, H, view).lines[:4]
    assert got == gold, (got, gold)


BRIEF_TITLES = [("\\", "⟦\\⟧"), ("x\\", "⟦x\\⟧"), ("a\\[b]", "⟦a\\[b]⟧"), ("\\[x", "⟦\\[x⟧")]


@pytest.mark.parametrize("size", mp.SIZES)
@pytest.mark.parametrize("title, want", BRIEF_TITLES)
def test_TC_4919_LLR_4652_9_a_backslash_title_in_the_brief_is_literal(title, want, size):
    """TC-4919 (LLR-4652.9, RB-2, SEC-B1, SEC-B2; regression, RED on base 8ca174c): a
    task titled `\\`, `x\\`, `a\\[b]` (and `\\[x`, a backslash before a non-tag `[`) is
    the cursor task, view 1 at 118x30 and 80x24 → measured on the rendered frame
    (`cell_len` of each line of `render_present(…).plain`): the brief holds `⟦\\⟧`,
    `⟦x\\⟧`, `⟦a\\[b]⟧`, `⟦\\[x⟧` literally, each backslash once, and every line is
    exactly the width. RED on base: `\\` and `x\\` give a 119 / 81-cell line reading
    `\\\\`; `\\[x` reads `[x`. `a\\[b]` passes on base (see e4-tests.md: the design's
    "base reads a[b]" did not reproduce). NC 1: keep `escape` → RED; NC 2: keep `escape`
    and pad/cut the line by its rendered width → RED on the literal check."""
    W, H = size
    b = fx.board(extra=[T("bx", "pd", title, "Doing", -1, 1)])
    r = mp.frame(b, "ppd", "tbx", W, H)
    line = next(ln for ln in r.lines[r.rule() + 1:] if "⟦" in ln)
    assert want in line, (line, want)
    assert [(k, w) for k, w in enumerate(r.widths()) if w != W] == [], r.widths()


HEADING_TITLES = [("a\\[b]", re.escape("▌ a\\[b]") + r"\s"),
                  ("\\[x", re.escape("▌ \\[x") + r"\s"),
                  ("ab\\[" + "x" * 60, re.escape("▌ ab\\[") + r"x+…")]


@pytest.mark.parametrize("size", mp.SIZES)
@pytest.mark.parametrize("title, pat", HEADING_TITLES)
def test_TC_4920_LLR_4652_10_a_backslash_before_a_bracket_stays_in_the_block(title, pat, size):
    """TC-4920 (LLR-4652.10, SEC-B3; regression, RED on base 8ca174c): a task titled
    `a\\[b]`, `\\[x` or `ab\\[` + 60 `x` (cut after the `\\[`) is the cursor task, view 2
    at 118x30 and 80x24 → the block's first row, measured on the rendered frame,
    holds `a\\[b]`, `\\[x`, `ab\\[x…` literally, and every line is exactly the width;
    6/6. RED on base: `[x`, `ab[x…` (the backslash dropped). `a\\[b]` passes on base
    (see e4-tests.md). NC: the heading keeps `escape` → RED."""
    W, H = size
    b = fx.board(extra=[T("bx", "pd", title, "Doing", -1, 1)])
    r = mp.frame(b, "ppd", "tbx", W, H, "split")
    rows = r.lines[r.rule() + 1:]
    assert any(re.search(pat, ln) for ln in rows), (pat, [ln for ln in rows if "▌" in ln])
    assert [(k, w) for k, w in enumerate(r.widths()) if w != W] == [], r.widths()


# =============================================================================
# 4.3 the cursor (HLR-4653, R-2)
# =============================================================================
def test_TC_4921_LLR_4653_1_the_shared_walk_and_stop_order():
    """TC-4921 (LLR-4653.1; SEAM-1, SEAM-2): `milestone_walk_key` sorts Pilot rollout's
    open milestones m2, m3, m4, m5 (m3 before m4 on Oct 24: `Steering…` < `Store…`);
    `present_stop_order` of its open list → the milestones in walk order, then the
    tasks in base order. NC: the base order (by due, milestones among tasks) → RED.
    RED on base: neither unit exists."""
    b = fx.board()
    open_t = views.present_tasks_m(b, "ppr")[0]
    ms = [t for t in open_t if t.milestone]
    assert [t.id for t in sorted(ms, key=views.milestone_walk_key)] == ["tm2", "tm3", "tm4", "tm5"]
    assert [t.id for t in views.present_stop_order(open_t)] == [
        "tm2", "tm3", "tm4", "tm5", "tstore", "ttele", "ttrain", "trota"]
    assert sorted(t.id for t in views.present_stop_order(open_t)) == sorted(t.id for t in open_t)


async def test_TC_4921_LLR_4653_1_the_arrows_step_along_the_stop_order(home):
    """TC-4921 (LLR-4653.1): view 1 on Pilot rollout, the cursor on m2, `↓`×4 → m3, m4,
    m5, `Pilot store list`; `↑` → m5; `→` → `Pilot store list` (`side` is a move in
    view 1, as at base); 3/3, read as the cursor brief `⟦…⟧`. NC: base order → `↓`
    from m2 lands on `Pilot store list` → RED. RED on base."""
    async with mp.present(home, (118, 30), sel="tm2") as (app, pilot):
        seen = [mp.cursor_brief(mp.pframe(app))]
        for _ in range(4):
            await mp.keys(pilot, "down")
            seen.append(mp.cursor_brief(mp.pframe(app)))
        assert seen == PILOT_MS_TITLES + ["Pilot store list"], seen
        await mp.keys(pilot, "up")
        assert mp.cursor_brief(mp.pframe(app)) == "Pilot launch"
        await mp.keys(pilot, "right")
        assert mp.cursor_brief(mp.pframe(app)) == "Pilot store list"


def test_TC_4922_LLR_4653_2_view_3s_stops_walk_the_row():
    """TC-4922 (LLR-4653.2; SEAM-3): view 3 at 118x30 → the stops begin with Pilot
    rollout's head, its milestones in walk order, then its tasks; Eval harness and Docs
    & handover likewise; a milestone with no due sorts after every dated one (SEAM-1).
    NC: one stop per milestone row → RED. RED on base (base stops interleave by due)."""
    _r, pa = mp.frame3(fx.board(), ("proj", "ppr"), 118, 30)
    want = [("proj", "ppr")] + [("task", k) for k in (
        "tm2", "tm3", "tm4", "tm5", "tstore", "ttele", "ttrain", "trota")] + \
        [("proj", "ppe")] + [("task", k) for k in ("tg1", "tg2", "tgq", "tgr", "tgx")] + \
        [("proj", "ppd")] + [("task", k) for k in ("th1", "tha", "thr")]
    assert pa.stops == want, pa.stops
    b = fx.board()
    undated = T("mz", "pr", "Aaa undated", "Next", None, None, True, "review")
    keys = sorted([undated] + [t for t in b.tasks if t.milestone and t.project_id == "ppr"],
                  key=views.milestone_walk_key)
    assert keys[-1].id == "tmz", [t.id for t in keys]


async def test_TC_4922_LLR_4653_2_down_from_the_head_walks_the_row(home):
    """TC-4922 (LLR-4653.2): `3` at 118x30, `→` (the timeline), the cursor on Pilot
    rollout's head, `↓`×5 → m2, m3, m4, m5 (each the row's `⟦` label), then `Pilot
    store list` (its own row); 5/5. RED on base."""
    async with mp.present(home, (118, 30), sel="tm2", view=3) as (app, pilot):
        await mp.keys(pilot, "right")
        assert mp.screen_of(app)._all_cur == ("proj", "ppr")
        got = []
        for _ in range(5):
            await mp.keys(pilot, "down")
            r = mp.ptimeline(app)
            cur = mp.cursor_rows(r)
            assert len(cur) == 1, r.lines
            got.append((cur[0], r.label(cur[0])[6 if cur[0] == 4 else 4:].strip()))
        assert [g[0] for g in got] == [4, 4, 4, 4, 5], got
        # view 3's label column is 17 cells (R-7, LLR-4652.4): the title whole, or its
        # head cut by cell width with `…`, the `k/n` tag kept after it
        for (_i, lab), t in zip(got, PILOT_MS_TITLES + PILOT_TASKS[:1]):
            head = re.sub(r" \d+/\d+$", "", lab)
            assert head == t or (head.endswith("…") and len(head) >= 9
                                 and t.startswith(head[:-1])), (lab, t)


def test_TC_4923_LLR_4653_3_the_cursor_falls_back_to_the_first_stop():
    """TC-4923 (LLR-4653.3): no cursor on Pilot rollout → m2; no cursor on Docs &
    handover → `Handover call` (h1, the stop order's first; base `API reference`, a
    task due before every milestone, P-7); the cursor m3 hidden → m2; 3/3. NC: the
    first by due among all open tasks (base `open_t[0]`) → RED on Docs & handover."""
    b = fx.board()
    assert mp.cursor_brief(mp.frame(b, "ppr", None)) == "Rubric sign-off"
    assert mp.cursor_brief(mp.frame(b, "ppd", None)) == "Handover call"
    b.task_by_id("tm3").show_in_present = False
    assert mp.cursor_brief(mp.frame(b, "ppr", "tm3")) == "Rubric sign-off"
    open_d = views.present_tasks_m(b, "ppd")[0]
    assert [t.id for t in views.present_stop_order(open_d)] == ["th1", "tha", "thr"]


async def test_TC_4923_LLR_4653_3_the_screen_starts_on_the_first_stop(home):
    """TC-4923 (LLR-4653.3; S `_shown_ids` → `_cursor`): `R` on Docs & handover with no
    cursor → the brief cursor `Handover call`; `↓` → `API reference` (the screen and
    the renderer agree on the first stop). RED on base (`API reference`, then
    `Runbook draft`)."""
    async with mp.present(home, (118, 30), sel=None, focus="ppd") as (app, pilot):
        assert mp.cursor_brief(mp.pframe(app)) == "Handover call"
        await mp.keys(pilot, "down")
        assert mp.cursor_brief(mp.pframe(app)) == "API reference"


def _saved(home) -> dict:
    return {t["id"]: t for t in json.loads((home / "board.json").read_text(encoding="utf-8"))["tasks"]}


@pytest.mark.parametrize("view", [1, 3])
async def test_TC_4924_LLR_4653_4_space_hides_the_cursor_milestone_alone(home, view):
    """TC-4924 (LLR-4653.4): the cursor on m3, `space` → m3's `show_in_present` false
    on disk; m2, m4, m5 still on the row; m4 alone in its cell (`▲`, no count); the
    cursor on m4; view 1 and view 3 at 118x30; 3/3 each. NC: hide every milestone of
    the cell → RED. RED on base (no shared row)."""
    async with mp.present(home, (118, 30), sel="tm3", view=view) as (app, pilot):
        if view == 3:
            await mp.keys(pilot, "right", "down", "down")
            assert mp.screen_of(app)._all_cur == ("task", "tm3")
        await mp.keys(pilot, "space")
        assert _saved(home)["tm3"].get("show_in_present") is False
        assert all(_saved(home)[k].get("show_in_present", True) for k in ("tm2", "tm4", "tm5"))
        b = mp.screen_of(app)._board
        if view == 1:
            r = mp.pframe(app)
            i, ax = _ms_row12(r), mp.axis12(b, "ppr", 118)
        else:
            r = mp.ptimeline(app)
            i, ax = _ms_row3(r, "Pilot rollout"), mp.axis3(b, r.W)
        f = r.field(i)
        at = {k: mp.due_cell(r, b, f"t{k}", ax) for k in ("m2", "m4", "m5")}
        assert f[at["m2"]] == "■" and f[at["m5"]] == "★", f
        assert _alone(f, at["m4"], "▲"), f                         # m4 alone: no count
        assert r.label(i).startswith(" ⟦▎ ▲ Store list"), r.label(i)   # the cursor on m4


@pytest.mark.parametrize("view", ["gantt", "split"])
def test_TC_4925_LLR_4653_5_briefs_and_blocks_follow_the_stop_order(view):
    """TC-4925 (LLR-4653.5): view 1's briefs read m2, m3, m4, m5, then the 4 tasks;
    view 2's blocks the same order, two columns from 100 wide filled in order (left
    the 4 milestones, right the 4 tasks); a project with no milestone keeps its base
    order (`present_stop_order` = `open_t`); 2/2. NC: briefs in base order → RED."""
    b = fx.board()
    r = mp.frame(b, "ppr", None, 118, 30, view)
    if view == "gantt":
        assert mp.briefs(r) == PILOT_MS_TITLES + PILOT_TASKS, mp.briefs(r)
    else:
        assert mp.blocks(r) == (PILOT_MS_TITLES, PILOT_TASKS), mp.blocks(r)
    b = fx.board(extra=[T("za", "pz", "Zeta wrap-up", "Doing", -2, 9),
                        T("zb", "pz", "Zeta intake", "Next", 3, 4)],
                 extra_projects=[fx.project("pz", "Zeta pilot")])
    base = [t.title for t in views.present_tasks_m(b, "ppz")[0]]
    r = mp.frame(b, "ppz", None, 118, 30, view)
    got = mp.briefs(r) if view == "gantt" else mp.blocks(r)[0] + mp.blocks(r)[1]
    assert got == base, (got, base)


def test_TC_4926_LLR_4653_6_the_keys_and_the_window_are_base(tmp_path):
    """TC-4926 (LLR-4653.6, SEAM-7, R-2): `PresentScreen`'s (key, action) pairs and
    `PresentKeys(view).lines()` for views gantt, split, all equal the base oracle
    captured on 8ca174c; 2/2. NC: bind `←→` to a row walk → RED. Passes on base by
    design (the oracle is base's)."""
    from taskboard import modals
    from taskboard.app import PresentScreen
    gold = mp.golden()
    pairs = sorted({(k.strip(), bd.action) for bd in PresentScreen.BINDINGS
                    for k in bd.key.split(",")})
    assert [list(p) for p in pairs] == gold["bindings"]
    for view in ("gantt", "split", "all"):
        assert modals.PresentKeys(view).lines().plain == gold["keys_lines"][view], view


# =============================================================================
# 4.4 the deck (HLR-4654)
# =============================================================================
@pytest.mark.parametrize("view", [1, 2, 3])
def test_TC_4931_LLR_4654_1_the_deck_bytes_equal_the_base_oracle(view):
    """TC-4931 (LLR-4654.1, SEAM-6): MR-F, the deck the export's own three calls write
    in views 1, 2, 3 (`present_deck_boards` → `report_html.extract` →
    `report_deck.render`) → sha256 equal to the base oracle captured on 8ca174c from
    the same fixture; 3/3. Passes on base by design (the oracle is base's); its
    negative control is the next test."""
    gold = mp.golden()["deck_l0"][str(view)]
    assert mp.sha(mp.deck_bytes(fx.board(), view)) == gold


@pytest.mark.parametrize("view", [1, 2, 3])
def test_TC_4931_LLR_4654_1_NC_a_deck_holding_the_stop_order_set_differs(view):
    """TC-4931's negative control (LLR-4654.1, B-4, RB-6, A-1): `present_deck_boards`
    holding `present_stop_order(present_tasks_m(board, p.id)[0])` in place of
    `present_tasks_m(board, p.id)[1]` drops the reached `tm1` from `ppr`'s proxy, so
    the deck's sha256 differs from the base oracle — 3/3. This proves the byte check
    above CAN fail; it is not an order-only mutant (the deck re-sorts by board
    position, so one could not fail)."""
    gold = mp.golden()["deck_l0"][str(view)]
    held = mp.deck_boards_mutant(mp.LANE + (fx.board(),), None if view == 3 else "ppr")
    assert "tm1" not in {t.id for t in held[0][3].tasks}
    assert mp.sha(mp.deck_bytes(fx.board(), view, mp.deck_boards_mutant)) != gold


def test_TC_4931_LLR_4654_1_the_proxy_holds_base_order_with_tm1():
    """TC-4931 / AT-4656's example (SEAM-6): the proxy for `ppr` holds its 9 shown
    tasks, the reached `tm1` included, in board order — the stop order is never read."""
    b = fx.board()
    held = views.present_deck_boards(mp.LANE + (b,), "ppr")[0][3].tasks
    want = [t.id for t in b.tasks if t.project_id == "ppr"]
    assert [t.id for t in held] == want and "tm1" in want
