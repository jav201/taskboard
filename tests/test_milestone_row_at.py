"""Inc MR-a acceptance — AT-4601..AT-4607, black box through the real app.

Each AT drives the shipped `TaskboardApp` (`open_app`, a real registry in a temporary
home, fixture MR-F, TODAY pinned) with keys only — `↑↓`, `←→`, `enter`, `esc`, `/`,
`#`, `L`, `]` — and reads what the screen PAINTS (the compositor's strips: glyph,
colour, reverse per cell) at 118x30 and 80x24. No seat is called. Width clauses
("no line wider than the terminal") are evidenced at layer 0 by TC-4829: the
compositor crops to the terminal, so a screen check of width cannot fail.

Why: the operator's story (US-4601) is that a project's milestones stop spending a
row each, the board fits the screen, and the arrows still reach every milestone.
RED on base 154e260: one row per milestone and `←→` a no-op in the gantt.
"""
from __future__ import annotations

import re
from datetime import date
from pathlib import Path

import pytest

import milestone_row_fixture as fx
from milestone_row_fixture import MARKS, cells_of, gantt, hide_class, keys, norm, painted
from taskboard import app as app_module
from taskboard import models, views

TODAY = fx.TODAY
PILOT = fx.PILOT_MS
REST = re.compile(r"^ ◆ \d+ (milestones?|ms)\b")
SIZES = [(118, 30), (80, 24)]
T = fx.task


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


class Screen:
    """The gantt as painted: its rows (above the ribbon and the key bar)."""

    def __init__(self, app, size):
        self.W, self.H = size
        self.paint = painted(app)[:self.H - 2]
        self.rows = ["".join(ch for ch, _h, _r in r) for r in self.paint]
        self.label_w, self.chip_w, self.fw = views.gantt_columns(self.W)
        self.x0 = self.label_w + 1

    def spans(self, folded=None):
        heads = ("▸ ",) if folded else ("▾ ",) if folded is False else ("▾ ", "▸ ")
        return [i for i, r in enumerate(self.rows) if r[:2] in heads]

    def span_of(self, name):
        return next(i for i, r in enumerate(self.rows) if r[:2] in ("▾ ", "▸ ")
                    and r[2:].startswith(name[:10]))

    def label(self, i):
        return "".join(cells_of(self.rows[i])[:self.label_w])

    def field(self, i):
        return norm(cells_of(self.rows[i])[self.x0:self.x0 + self.fw])

    def chip(self, i):
        return "".join(cells_of(self.rows[i])[-self.chip_w:]).strip()

    def rev_at(self, i, needle):
        """Is the first cell of `needle` in row `i`'s field painted reverse?"""
        x = self.x0 + self.field(i).index(needle)
        return self.paint[i][x][2]

    def body(self):
        """The body rows: below the ruler and the class strip, above the legend."""
        out = []
        for r in self.rows[4:]:
            if "⟦━⟧" in r or not r.strip():
                break
            out.append(r)
        return out


def pilot_row(s: Screen) -> int:
    return s.span_of("Pilot rollout") + 1


# =============================================================================
@pytest.mark.parametrize("size", SIZES)
async def test_AT_4601_the_row_at_rest(home, size):
    """MR-F, `3`, the cursor on `Pilot store list` → one milestone row under each of
    the 4 span rows; Pilot rollout's reads `⬡✓`, `■ ▲1d`, `■2 Oct 24`, `★ Oct 30`;
    18 body rows at 118x30 (base 23); 0 folded groups at 80x24; a blank gutter on
    every milestone row."""
    async with gantt(home, size=size) as (app, pilot):
        s = Screen(app, size)
        spans = s.spans()
        assert len(spans) == 4 and not s.spans(folded=True), "\n".join(s.rows)
        for i in spans:
            assert REST.match(s.rows[i + 1]), s.rows[i + 1]
            assert s.rows[i + 1][s.label_w] == " "          # the gutter
        f = s.field(pilot_row(s))
        for want in ("⬡✓", "■ ▲1d", "■2 Oct 24", "★ Oct 30"):
            assert want in f, (want, f)
        if size == (118, 30):
            assert len(s.body()) == 18, "\n".join(s.body())
        assert all(len(cells_of(r)) <= size[0] for r in s.rows)


async def test_AT_4602_folding(home):
    """MR-F (plus a project with no milestone) at 118x12 → each folded group shows
    only its span row; the group with no milestone, unfolded, shows its tasks and
    no milestone row. Passes on base by design (a fold guard)."""
    quiet = [T("q1", "pq", "Rota sheet", "Next", 0, 6), T("q2", "pq", "Audit log", "Next", 1, 8)]
    async with gantt(home, size=(118, 12), sel="tq1", extra=quiet,
                     extra_projects=[fx.project("pq", "Quiet ops")]) as (app, pilot):
        s = Screen(app, (118, 12))
        folded = s.spans(folded=True)
        assert folded, "\n".join(s.rows)
        for i in folded:
            nxt = s.rows[i + 1] if i + 1 < len(s.rows) else ""
            assert nxt[:2] in ("▾ ", "▸ ") or not nxt.strip() or "⟦━⟧" in nxt, nxt
        q = s.span_of("Quiet ops")
        assert s.rows[q].startswith("▾ ")
        assert not REST.match(s.rows[q + 1]) and s.rows[q + 1].startswith("  "), s.rows[q + 1]


@pytest.mark.parametrize("size", SIZES)
async def test_AT_4603_onto_the_row_and_along_it(home, size):
    """From `Pilot store list`: `↑` → m3 selected, its title beside `■2`, the label
    column `■ Steering go/no-go 1/2`, chip `in 4d`, its mark reverse; `→` → m4
    (`▲2`, `2/2`); `→` → m5; `→` → m5; `←`×4 → m1; `←` → m1."""
    async with gantt(home, size=size) as (app, pilot):
        await keys(pilot, "up")
        assert app.selected_task_id == "tm3"
        s = Screen(app, size)
        i = pilot_row(s)
        assert "■2 Steerin" in s.field(i), s.rows[i]
        assert s.rev_at(i, "■2")
        lab = s.label(i).strip()
        assert lab.startswith("■ Steering") and lab.endswith("1/2"), lab
        assert s.chip(i) == "in 4d"
        await keys(pilot, "right")
        assert app.selected_task_id == "tm4"
        s = Screen(app, size)
        assert "▲2" in s.field(i) and s.rev_at(i, "▲2"), s.rows[i]
        assert s.label(i).strip().endswith("2/2")
        for want in ("tm5", "tm5"):
            await keys(pilot, "right")
            assert app.selected_task_id == want
        for _ in range(4):
            await keys(pilot, "left")
        assert app.selected_task_id == "tm1"
        await keys(pilot, "left")
        assert app.selected_task_id == "tm1"


async def test_AT_4604_acting_on_the_walked_one(home):
    """m3, `→`, `enter` → details of m4; `esc`, `]` → m4 one phase on; `↓` →
    `Pilot store list`; `←`/`→` → no change."""
    from taskboard.modals import TaskDetails
    async with gantt(home) as (app, pilot):
        await keys(pilot, "up", "right", "enter")
        assert isinstance(app.screen, TaskDetails)
        assert app.screen._detail_task.id == "tm4"
        await keys(pilot, "escape", "right_square_bracket")
        assert app.board.task_by_id("tm4").phase == "Doing"
        assert app.board.task_by_id("tm3").phase == "Next"
        await keys(pilot, "down")
        assert app.selected_task_id == "tstore"
        await keys(pilot, "left")
        assert app.selected_task_id == "tstore"
        await keys(pilot, "right")
        assert app.selected_task_id == "tstore"


async def test_AT_4605_search_and_hidden_classes(home):
    """`/store` `enter` → Pilot rollout's row holds m4 only; `→` keeps m4. `esc` the
    query; hide class Review in `#` → the row holds m1, m4, m5; `→` from m1 → m4."""
    async with gantt(home) as (app, pilot):
        await keys(pilot, "slash", *"store", "enter")
        for _ in range(4):                           # onto the row, by keys
            if app.selected_task_id in PILOT:
                break
            await keys(pilot, "up")
        assert app.selected_task_id == "tm4"
        s = Screen(app, (118, 30))
        f = s.field(pilot_row(s))
        assert [ch for ch in f if ch in MARKS] == ["▲"], f
        await keys(pilot, "right")
        assert app.selected_task_id == "tm4"
        await keys(pilot, "escape")
        await hide_class(pilot, "review")
        s = Screen(app, (118, 30))
        f = s.field(pilot_row(s))
        assert "■" not in f and "Rubric" not in f and "Steering" not in f, f
        assert [ch for ch in f if ch in MARKS] == ["⬡", "▲", "★"], f
        for k in ["up"] * 5:                           # back onto the row, by keys
            if app.selected_task_id in PILOT:
                break
            await keys(pilot, k)
        for _ in range(4):                           # along it to m1
            if app.selected_task_id == "tm1":
                break
            await keys(pilot, "left")
        assert app.selected_task_id == "tm1"
        await keys(pilot, "right")
        assert app.selected_task_id == "tm4"


def _big(n=20):
    tasks = [T(f"b{k:02}", "pg", f"Big task {k:02}", "Next", -2, k) for k in range(1, n + 1)]
    tasks += [T("bm1", "pg", "Big gate one", "Next", None, 5, True, "delivery"),
              T("bm2", "pg", "Big gate two", "Next", None, 12, True, "review")]
    return tasks


async def test_AT_4606_link_mode_and_pages(home):
    """m3, `→`, `L` → the link frame: one row per drawn milestone (m1..m5),
    byte-equal to base, waiter m4; `esc` → milestone rows back, m4 selected. A
    paged group: `↑` onto its row → the page holding the row."""
    import json
    golden = json.loads(Path(__file__).with_name("milestone_row_link_golden.json")
                        .read_text(encoding="utf-8"))["frames"]["118x30"]
    async with gantt(home) as (app, pilot):
        await keys(pilot, "up", "right", "L")
        assert app.screen.waiter.id == "tm4"
        frame = app.screen.query_one("#glink-frame").content
        assert frame.plain == golden["plain"] and frame.markup == golden["markup"]
        await keys(pilot, "escape")
        assert app.selected_task_id == "tm4"
        s = Screen(app, (118, 30))
        assert s.label(pilot_row(s)).strip().startswith("▲ Store list frozen")
        assert sum(bool(REST.match(r)) for r in s.rows) == 3


async def test_AT_4606b_a_paged_group_pages_to_its_row(home):
    """One group of a milestone row (2 milestones) + 20 tasks at 118x14, the
    cursor on the last task, `↑` until the row → the page starts with the row,
    says `▼ <n> below` with n = the task rows off the page, and nothing above."""
    async with gantt(home, size=(118, 14), sel="tb20", rows=[], extra=_big(),
                     extra_projects=[fx.project("pg", "Big rollout", due=25)],
                     base_projects=False) as (app, pilot):
        for _ in range(25):
            if app.selected_task_id in ("tbm1", "tbm2"):
                break
            await keys(pilot, "up")
        assert app.selected_task_id in ("tbm1", "tbm2")
        s = Screen(app, (118, 14))
        i = s.span_of("Big rollout")
        assert "Big gate" in s.label(i + 1), s.rows[i + 1]
        hint = next(k for k, r in enumerate(s.rows) if "below" in r or "above" in r)
        shown = [r for r in s.rows[i + 2:hint] if "Big task" in r]
        assert f"▼ {20 - len(shown)} below" in s.rows[hint], s.rows[hint]
        assert "above" not in s.rows[hint]


@pytest.mark.parametrize("size", SIZES)
async def test_AT_4607_edges(home, size):
    """On Pilot rollout's row (open work): a reached milestone due 90 days ahead
    (done early), one with no due, and 10 on one day → `⬡✓▸` in the field's last
    three cells, no mark for the undated one, `▲+`; 6 marks in all."""
    edges = [T("x2", "pr", "Early payout", "Done", None, 90, True, "payment"),
             T("xn", "pr", "Undated gate", "Next", None, None, True, "launch")]
    edges += [T(f"z{n}", "pr", f"Gate {n}", "Next", None, 6, True, "delivery") for n in range(10)]
    async with gantt(home, size=size, extra=edges) as (app, pilot):
        s = Screen(app, size)
        i = pilot_row(s)
        assert REST.match(s.rows[i]), s.rows[i]
        f = s.field(i)
        assert f[-3:] == "⬡✓▸", f
        assert "▲+" in f, f
        assert sum(ch in MARKS for ch in f) == 6, f
        assert all(len(cells_of(r)) <= size[0] for r in s.rows)
