"""Inc MR-b acceptance — AT-4651..AT-4656, black box through the real app and its keys.

Each AT builds MR-F as a real registry in a temporary home, starts the shipped app
(`open_app`), and drives `R` and its keys only (`↑↓←→`, `1 2 3`, `enter`, `space`,
`u`, `a`, `#`, `?`, `x`) at 118x30 and 80x24. It reads what the PresentScreen paints:
its `#present-frame` Text (after `to_text`), measured per line with `cell_len`, and
the hint row. The terminal's last row is the hint, so the frame is one row shorter
than the terminal.

Why: US-4651 — the room sees the work, not a row per milestone, and nothing the
presenter learned changes: the same keys still stop at every milestone.
RED on base 8ca174c: one field row per milestone, and the cursor walks by due.
"""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

import pytest

import milestone_row_fixture as fx
import milestone_row_present_fixture as mp
from milestone_row_present_fixture import PILOT_MS_TITLES, PILOT_TASKS, cursor_brief, keys
from taskboard import app as app_module
from taskboard import modals, models, views

TODAY = fx.TODAY
T = fx.task


class _Today(date):
    @classmethod
    def today(cls):
        return TODAY


@pytest.fixture(autouse=True)
def _pin_today(monkeypatch):
    for mod in (app_module, models, views, modals):
        monkeypatch.setattr(mod, "date", _Today)


@pytest.fixture
def home(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
    return tmp_path / ".taskboard"


def _body(r):
    """Views 1/2: the field lines between the span and the rule."""
    return list(range(r.span() + 1, r.rule()))


def _widths_ok(r):
    return [(i, w) for i, w in enumerate(r.widths()) if w != r.W] == []


def _row_cells(r, b, i, ax, keys_):
    f = r.field(i)
    return f, {k: mp.due_cell(r, b, k, ax) for k in keys_}


# =============================================================================
@pytest.mark.parametrize("size", mp.SIZES)
async def test_AT_4651_view_1_one_row_and_the_walk(home, size):
    """AT-4651 (LLR-4651.1, .3, .4, .8; LLR-4652.1-.5, .7, .8; LLR-4653.1, .3, .5): `R`
    on Pilot rollout with no cursor → the field is the span, ONE milestone row, then
    the 4 task rows; the cursor starts on m2: its mark reversed (with `Rubric…` beside
    it at 118) and the label ` ⟦▎ ■ Rubric sign-off` (118) / ` ⟦▎ ■ Rubric sign-…`
    (80, RB-3); `↓` → m3 (its title beside `■2` at 118), `↓` → m4 (`▲2`, the tag
    `2/2`), `↓` → m5, `↓` → `Pilot store list`; the briefs in the same order; the
    row's gutter blank; every line exactly the width. RED on base."""
    W, _H = size
    async with mp.present(home, size, sel=None, focus="ppr") as (app, pilot):
        r = mp.pframe(app)
        body = _body(r)
        assert len(body) == 5 and r.has_mark(body[0]), r.lines
        assert not any(r.has_mark(i) for i in body[1:]), r.lines
        assert [r.label(i)[4:].strip()[:10] for i in body[1:]] == [t[:10] for t in PILOT_TASKS]
        ms = body[0]
        want = " ⟦▎ ■ Rubric sign-off" if W == 118 else " ⟦▎ ■ Rubric sign-…"
        assert r.label(ms).rstrip() == want, r.label(ms)
        assert r.gutter(ms) == " "
        b = mp.screen_of(app)._board
        x = mp.due_cell(r, b, "tm2", mp.axis12(b, "ppr", W))
        assert r.fcells(ms)[x] == "■" and r.fstyle(ms, x).reverse, r.lines[ms]
        if W == 118:
            assert "■ Rubric…" in r.field(ms), r.field(ms)
        assert mp.briefs(r) == PILOT_MS_TITLES + PILOT_TASKS, mp.briefs(r)
        assert _widths_ok(r), r.widths()
        steps = []
        for _ in range(4):
            await keys(pilot, "down")
            r = mp.pframe(app)
            steps.append((cursor_brief(r), r.label(_body(r)[0]).rstrip(), r.field(_body(r)[0])))
            assert _widths_ok(r), r.widths()
            assert r.gutter(_body(r)[0]) == " "
        assert [s[0] for s in steps] == PILOT_MS_TITLES[1:] + ["Pilot store list"], steps
        assert steps[0][1].startswith(" ⟦▎ ■ Steering"), steps[0]
        if W == 118:
            assert "■2 Steerin…" in steps[0][2], steps[0]
        assert steps[1][1].startswith(" ⟦▎ ▲ Store") and steps[1][1].endswith("2/2"), steps[1]
        assert "▲2" in steps[1][2], steps[1]
        assert steps[2][1].startswith(" ⟦▎ ★ Pilot launch"), steps[2]
        assert steps[3][1].startswith("  ▎ ◆ 4 m"), steps[3]                 # at rest again


@pytest.mark.parametrize("size", mp.SIZES)
async def test_AT_4652_view_2_the_same_field_and_blocks_in_stop_order(home, size):
    """AT-4652 (LLR-4651.1; LLR-4653.1, .5): `2` → the same field (span, one milestone
    row, 4 tasks) and the same cursor walk m2 → m3 → m4 → m5 → `Pilot store list`
    (read as the cursor block `▌`); the blocks in stop order (118: left the 4
    milestones, right the 4 tasks; 80: one column in that order). RED on base."""
    W, _H = size
    async with mp.present(home, size, sel=None, focus="ppr", view=2) as (app, pilot):
        r = mp.pframe(app)
        body = _body(r)
        assert len(body) == 5 and r.has_mark(body[0]), r.lines
        left, right = mp.blocks(r)
        assert (left + right) == PILOT_MS_TITLES + PILOT_TASKS, (left, right)
        if W == 118:
            assert (left, right) == (PILOT_MS_TITLES, PILOT_TASKS)
        seen = []
        for _ in range(5):
            r = mp.pframe(app)
            cur = [m.group(1).strip() for ln in r.lines[r.rule() + 1:]
                   for m in re.finditer(r"▌ (.+?)\s{2,}", ln)]
            seen.append(cur[0] if cur else None)
            assert _widths_ok(r), r.widths()
            await keys(pilot, "down")
        assert seen == PILOT_MS_TITLES + ["Pilot store list"], seen


async def test_AT_4653_view_3_rows_walk_fold_rail_and_overflow(home):
    """AT-4653 (LLR-4651.2, .6, .7; LLR-4653.2): `3` at 118x30 → under each head one
    milestone row, then the tasks; `→` to the timeline, `↓` from Pilot rollout's head
    walks m2..m5 (the row's `⟦` label), then the 4 tasks; `←` → the rail on Pilot
    rollout (base); `→`, then down to Eval harness's head, `enter` folds it: no
    milestone row under it. Then at 118x19 (the frame 18 rows: room 15, need 15, RB-4)
    the overflow folds no project, where base folds 2. RED on base."""
    async with mp.present(home, (118, 30), sel="tm2", view=3) as (app, pilot):
        r = mp.ptimeline(app)
        heads = r.heads()
        assert len(heads) == 3, r.lines
        for h, end in zip(heads, heads[1:] + [len(r)]):
            assert [i for i in range(h + 1, end) if r.has_mark(i)] == [h + 1], r.lines[h:end]
        await keys(pilot, "right")
        walk = []
        for _ in range(8):
            await keys(pilot, "down")
            r = mp.ptimeline(app)
            cur = mp.cursor_rows(r)
            assert len(cur) == 1, r.lines
            walk.append((cur[0], r.label(cur[0])))
        ms_line = r.head("Pilot rollout") + 1
        assert [w[0] for w in walk[:4]] == [ms_line] * 4, walk
        for (_i, lab), t in zip(walk[:4], PILOT_MS_TITLES):
            assert lab[6:].startswith(t[:8]), (lab, t)
        assert [w[0] for w in walk[4:]] == [ms_line + 1 + k for k in range(4)], walk
        for (_i, lab), t in zip(walk[4:], PILOT_TASKS):
            assert lab[4:].startswith(t[:10]), (lab, t)
        await keys(pilot, "left")
        rail = [ln[:views.PRESENT_RAIL_W] for ln in mp.pframe(app).lines]
        assert any(x.startswith("▶ 1 ● Pilot rollout") for x in rail), rail
        await keys(pilot, "right")
        for _ in range(12):
            if mp.screen_of(app)._all_cur == ("proj", "ppe"):
                break
            await keys(pilot, "down")
        await keys(pilot, "enter")
        r = mp.ptimeline(app)
        h = r.head("Eval harness")
        assert r.lines[h].startswith(("▸", "⟦")), r.lines[h]
        nxt = r.head("Docs & handover")
        assert not any(r.has_mark(i) for i in range(h + 1, nxt)), r.lines[h:nxt]
    async with mp.present(home, (118, 19), sel="tm2",
                          view=3) as (app, pilot):
        r = mp.ptimeline(app)
        assert len(r) == 18
        assert len(r.heads()) == 3 and not any(r.lines[h].startswith("▸") for h in r.heads()), \
            r.lines


@pytest.mark.parametrize("size", mp.SIZES)
async def test_AT_4654_hiding_milestones_from_the_row(home, size):
    """AT-4654 (LLR-4651.3, .5; LLR-4653.4): view 1, the cursor on m3, `space` → the row
    holds m2, m4, m5 (m4 alone: `▲`, no count); `u` lists m3; `a` → m3 back on the row
    (`■2`); class Review hidden in `#`, then `R` → the row holds m4, m5 only; h1 hidden
    with `space` → Docs & handover draws no milestone row. RED on base."""
    W, _H = size
    async with mp.present(home, size, sel="tm3") as (app, pilot):
        b = mp.screen_of(app)._board
        ax = mp.axis12(b, "ppr", W)
        await keys(pilot, "space")
        r = mp.pframe(app)
        f, at = _row_cells(r, b, _body(r)[0], ax, ("tm2", "tm4", "tm5"))
        assert f[at["tm2"]] == "■" and f[at["tm5"]] == "★", f
        assert f[at["tm4"]] == "▲" and not re.match(r"[0-9+]", f[at["tm4"] + 1]), f
        await keys(pilot, "u")
        rows = app.screen.query_one("#picker-rows").content.plain
        assert "Steering go/no-go" in rows, rows
        await keys(pilot, "escape", "a")
        r = mp.pframe(app)
        # base `space` steps the cursor to the next stop (m4), and LLR-4653.4 keeps
        # that: m3 back shares m4's cell, the cursor member leading it, counted 2
        assert mp.screen_of(app)._cursor_id == "tm4"
        f, at = _row_cells(r, b, _body(r)[0], ax, ("tm3", "tm4"))
        assert at["tm3"] == at["tm4"] and f[at["tm3"]:at["tm3"] + 2] == "▲2", f
    async with mp.present(home, size, sel="tstore",
                          hidden=("review",)) as (app, pilot):
        b = mp.screen_of(app)._board
        r = mp.pframe(app)
        f, at = _row_cells(r, b, _body(r)[0], mp.axis12(b, "ppr", W), ("tm4", "tm5"))
        assert "■" not in f and f[at["tm4"]] == "▲" and f[at["tm5"]] == "★", f
        assert not any(r.has_mark(i) for i in _body(r)[1:]), r.lines
    async with mp.present(home, size, sel="th1") as (app, pilot):
        await keys(pilot, "space")
        r = mp.pframe(app)
        assert len(_body(r)) == 2 and not any(r.has_mark(i) for i in _body(r)), r.lines


HOSTILE = ["a]b[/]", "[@click=app.quit]x", "\\", "x\\", "a\\[b]", "日本語のタイトル"]


@pytest.mark.parametrize("title", HOSTILE)
async def test_AT_4655_hostile_titles_stay_literal_at_80x24(home, title):
    """AT-4655 (LLR-4652.6, .9, .10; LLR-4653.6; SEC-B2, SEC-B3): a milestone titled
    `a]b[/]`, `[@click=app.quit]x`, `\\`, `x\\`, `a\\[b]` or a wide-glyph title, walked
    onto in views 1, 2 and 3 at 80x24 → literal text in the row's label, the brief
    `⟦…⟧` and the block `▌ …` (each backslash once, none dropped); every line of the
    rendered frame exactly 80 cells; 0 exceptions, the app still presenting; `?` → the
    window as at base. The milestone shares Pilot rollout's row with m2..m5 (alone in
    its cell, Nov 1). RED on base for every title: the line under the span is m2's own
    row, not the cursor's (and for a trailing backslash the brief doubles it, 81 cells)."""
    extra = [T("mx", "pr", title, "Next", None, 12, True, None)]   # alone on Nov 1
    gold = mp.golden()["keys_window"]
    async with mp.present(home, (80, 24), sel="tmx", focus=None, extra=extra) as (app, pilot):
        r = mp.pframe(app)
        lab = r.label(_body(r)[0])
        assert lab.startswith(" ⟦▎ ◆ ") and mp.literal_cut(lab[6:], title), (lab, title)
        brief = cursor_brief(r)
        assert brief is not None and mp.literal_cut(brief, title), (brief, title)
        assert _widths_ok(r), r.widths()
        for sp in r.text.spans:
            assert "@click" not in str(sp.style) and not getattr(sp.style, "meta", None)
        await keys(pilot, "2")
        r = mp.pframe(app)
        heads = [ln[ln.index("▌ ") + 2:] for ln in r.lines[r.rule() + 1:] if "▌ " in ln]
        assert heads and mp.literal_cut(re.split(r"\s{2,}", heads[0])[0], title), heads
        assert _widths_ok(r), r.widths()
        await keys(pilot, "3")
        r = mp.ptimeline(app)
        assert mp.screen_of(app)._all_cur == ("task", "tmx")
        lab = r.label(r.head("Pilot rollout") + 1)
        assert lab.startswith(" ⟦▎ ◆ ") and mp.literal_cut(lab[6:], title), (lab, title)
        assert _widths_ok(mp.pframe(app)), mp.pframe(app).widths()
        assert type(app.screen).__name__ == "PresentScreen" and app.is_running
        await keys(pilot, "question_mark")
        c = app.screen.query_one("#pk-text").content
        assert (c.plain if hasattr(c, "plain") else str(c)) == gold["3"]
        await keys(pilot, "escape")


@pytest.mark.parametrize("size", mp.SIZES)
async def test_AT_4655_the_hint_row_is_base(home, size):
    """AT-4655 / LLR-4652.8 (the hint row) and LLR-4653.6: views 1, 2, 3 with the cursor
    on m2 → each hint row equals the base oracle captured on 8ca174c through the same
    keys. Passes on base by design (the oracle is base's)."""
    W, H = size
    gold = mp.golden()["hint"]
    async with mp.present(home, size, sel="tm2") as (app, pilot):
        for v in (1, 2, 3):
            await keys(pilot, str(v))
            assert mp.hint(app) == gold[f"{v}-{W}x{H}"], (v, mp.hint(app))


async def test_AT_4656_the_x_deck_is_the_base_deck(home):
    """AT-4656 (LLR-4654.1): `x` in views 1, 2 and 3 → each written file's sha256 equals
    the base oracle captured on 8ca174c through the same keys on the same fixture;
    3/3. Passes on base by design; the byte check's negative control is TC-4931's NC
    (`test_present_milestone_row.py`), 3/3 RED."""
    gold = mp.golden()["deck_app"]
    async with mp.present(home, (118, 30), sel="tm2") as (app, pilot):
        for v in (1, 2, 3):
            await keys(pilot, str(v), "x")
            name = (f"present-{TODAY.isoformat()}.html" if v == 3 else
                    f"present-pilot-rollout-{TODAY.isoformat()}.html")
            path = home / "reports" / name
            assert mp.sha(path.read_bytes()) == gold[str(v)], v
            path.unlink()
