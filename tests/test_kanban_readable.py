"""The readable kanban — K-A cards + the R-1b high band (batch 2026-10-02-batch-03).

Field report (the operator, prototype rounds 1–2 and 8, 2026-09-30/10-01): the
shipped grouped kanban cut every title to about eight characters, named each
project again in every column and gave finished work a full column. The
verdicts: K-A — two-row cards, the title across the column, the facts on a quiet
second row, a `┈` rule between stacked cards ("se ve menos cargado"), one band
rule per project across the board, DONE as a narrow rail — and R-1b: the open
high cards of every column in ONE band on top. The approved frames are
`prototypes/kg_mejoras/out/R-1b-118x30.txt` / `-80x24.txt`.

The laws, each RED on the base tree or under a recorded mutation:
- a card is two rows of exactly its column's width; the due token is the last
  fact to go; every title piece is escaped after it is cut (HLR-301);
- one `┈` row between two cards of a cell; widths follow the titles (HLR-302);
- each group is named once, by a band rule (HLR-303); the last phase is a rail
  (HLR-304); the highs ride one band on top (HLR-305);
- the board fits the panel by folding whole bands and naming them (HLR-309);
- nothing new wears the accent; soon is amber (HLR-307);
- the cursor walks what is drawn (F-3) through ONE seat, `kanban_plan`.

Batch 2026-10-02-batch-03 · HLR-301..310 · AT-301..AT-308 · TC-301..TC-313
(increment 001: the board; increment 002: the cap's nodes, the copy, the cursor
off undrawn done work, the filtered nav).
"""
from __future__ import annotations

import re
from datetime import timedelta
from pathlib import Path

import pytest
from rich.cells import cell_len
from rich.text import Text

import kg_board
from kg_board import TODAY
from taskboard import app as app_mod
from taskboard import models, views
from taskboard.app import TaskboardApp
from taskboard.models import Board, Project, Task
from taskboard.views import (_KANBAN_GROUP_MODES, _KANBAN_SORT_MODES, HEX, KANBAN_BAND,
                             MIN_COL, PRIORITY_BADGE, kanban_order, nav_model, render_view)

# the batch's new seat, read tolerantly so the base tree reports RED per node
# (its absence) rather than one collection error
_due_fact = getattr(views, "_due_fact", None)
_kanban_widths = getattr(views, "_kanban_widths", None)
kanban_card = getattr(views, "kanban_card", None)
kanban_plan = getattr(views, "kanban_plan", None)

from kg_board import body, readability  # noqa: E402  (the prototype's metric)

ACCENT = HEX["accent"].lower()
def tone(key: str) -> tuple[str, str]:
    """A palette tone as rich writes it (`#rrggbb`) and as Textual's painted
    spans write it (`rgb(r,g,b)`)."""
    h = HEX[key].lower()
    return h, "rgb({},{},{})".format(*(int(h[i:i + 2], 16) for i in (1, 3, 5)))


def has(st: str, key: str) -> bool:
    return any(x in st for x in tone(key))


FOLD = re.compile(r"^[▲▼] \d+ (above|below|more)")
HIGH_IDS = {"tw5", "tm4", "ta2", "to5", "ta3", "to2", "tw3", "ta4", "to1"}   # P-2


def _plain(markup: str) -> str:
    return Text.from_markup(markup, emoji=False).plain


def render(b, w, h, sel="tw3", **kw):
    lm: dict = {}
    text = render_view("kanban", b, False, sel, TODAY, w, h, lm, **kw)
    return text, text.plain.split("\n"), lm


def is_rule(row: str) -> bool:
    """A band rule: `▐ name  N open …` across the board (a shipped per-column
    `▐ name` header carries no open count, so it is not one)."""
    return row.startswith("▐ ") and " open" in row.split("─")[0]


def seps_of(rows):
    """The column separators, read off the phase row (the second row)."""
    return [x for x, ch in enumerate(rows[1]) if ch == "│"]


def cell(row, seps, i):
    bounds = [-1] + seps + [len(row)]
    return row[bounds[i] + 1:bounds[i + 1]]


def mixed_board(path) -> Board:
    """The 60-arm board (qa Q-8): two projects and the Inbox, open highs in both
    projects and the Inbox, a blocked high, archived open and done tasks, a done
    high — so `show_archived`, the Inbox and the band all change something."""
    a, b = Project("Alpha", "sky"), Project("Bravo", "lime")
    d = lambda n: (TODAY + timedelta(days=n)).isoformat()   # noqa: E731
    tasks = [
        Task("Bravo urgent", b.id, "Doing", "high", due_date=d(9), phase_changed=d(-10), id="hb"),
        Task("Alpha urgent", a.id, "Doing", "high", due_date=d(1), phase_changed=d(-2), id="ha"),
        Task("Alpha blocked", a.id, "Doing", "high", blocked=True, due_date=d(5),
             phase_changed=d(-5), id="hx"),
        Task("Alpha shelved", a.id, "Doing", "high", archived=True, id="har"),
        Task("Alpha plain", a.id, "Doing", "normal", due_date=d(2), phase_changed=d(-1), id="na"),
        Task("Bravo someday", b.id, "Doing", "low", id="lb"),
        Task("Bravo next", b.id, "Backlog", "normal", due_date=d(3), id="nb"),
        Task("Loose idea", None, "Backlog", "high", due_date=d(20), id="hi"),
        Task("Loose chore", None, "Backlog", "normal", id="ni"),
        Task("Old normal", a.id, "Review", "normal", archived=True, id="nar"),
        Task("Shipped thing", a.id, "Done", "high", phase_changed=d(-3), id="hd"),
        Task("Shipped long ago", b.id, "Done", "normal", archived=True, phase_changed=d(-40),
             id="dar"),
    ]
    return Board([a, b], tasks, path, phases=["Backlog", "Doing", "Review", "Done"])


def eight_phases(path) -> Board:
    phases = [f"P{i}" for i in range(7)] + ["Done"]
    p = Project("Wide", "violet")
    tasks = [Task(f"task in {ph}", p.id, ph, "normal", id=f"t{i}") for i, ph in enumerate(phases)]
    return Board([p], tasks, path, phases=phases)


# --------------------------------------------------------------------------- #
# LLR-301.2 — the two-row card (TC-302, TC-303)
# --------------------------------------------------------------------------- #
HOSTILE = ["[b]x[/b] [link=http://e]y", "a [ b c", "x\\ y\\", "\\[b]z", "aaa [/link]",
           "日本語 レビュー 🚀 launch"]


def _card_tasks():
    b = kg_board.build()
    extra = []
    for i, title in enumerate(HOSTILE + ["A very long title that runs well past two rows of any card",
                                         "Supercalifragilisticexpi"]):
        for url in (None, "https://example.org/x"):
            t = Task(title, b.projects[i % 5].id, "Doing", "normal",
                     due_date=kg_board._d(i - 2), phase_changed=kg_board._d(-i),
                     urls=[url] if url else [], id=f"h{i}{bool(url)}")
            extra.append(t)
    b.tasks.extend(extra)
    return b


@pytest.mark.parametrize("wc", range(0, 41))
def test_TC_302_a_card_is_two_rows_of_exactly_its_width(wc):
    """TC-302 (LLR-301.2). The width law on BOTH rows, at every width down to 0,
    for the oracle board plus hostile titles (P2 S-1/S-2: a lone `[`,
    backslashes at a cut and at the end, an escaped tag, a closing tag that
    lands on row 2, wide characters), each with and without a URL. A piece
    escaped BEFORE it is cut opens a tag or leaves `[/link]` literal; rich then
    raises or the row leans. RED: escape the title before the cut."""
    b = _card_tasks()
    for t in b.tasks:
        for sel in (False, True):
            r1, r2 = kanban_card(t, b, wc, sel, today=TODAY)
            p1, p2 = _plain(r1), _plain(r2)
            assert cell_len(p1) == wc and cell_len(p2) == wc, (t.title, wc, p1, p2)
            if wc >= 40 and not b.is_done(t):
                head = t.title.split(" ")[0]
                assert head in p1, (t.title, p1)   # the user's text, literally
                # the two rows hold the title's head and the start of its rest
                words = t.title.split(" ")
                shown = (p1[5:] + " " + p2[5:]).split()
                assert shown[:2] == [w for w in words if w][:2] or len(words) < 2 \
                    or shown[1].endswith("…"), (t.title, p1, p2)


def test_TC_302_the_title_wraps_on_a_word_and_the_rest_sits_under_it():
    """TC-302. The approved frame's own card (`out/R-1b-118x30.txt` rows 20–21,
    `tm5`: normal, 15 days in phase, due +35d, no dependant, no URL) at its
    column width 24, and a first word wider than the cell cut with `…`."""
    b = kg_board.build()
    r1, r2 = kanban_card(b.task_by_id("tm5"), b, 24, False, today=TODAY)
    assert _plain(r1) == "▊ == Beta release to    "
    assert _plain(r2) == "▊    testers ·15d +35d  "
    t = Task("Supercalifragilisticexpialidocious now", b.projects[0].id, "Doing")
    r1, r2 = kanban_card(t, b, 16, False, today=TODAY)
    assert _plain(r1).rstrip().endswith("…") and _plain(r2).strip() in ("▊", "▊ ·0d")


def test_TC_303_the_due_token_is_the_last_fact_to_go():
    """TC-303 (LLR-301.2). Under width pressure the meta strip sheds from the
    left — age, then `⛓N`, then the due token LAST: at every width from 9 a
    dated open card still shows its due. RED: `⛓N` after the due → at `wc` 14
    `Fix checkout`'s `-2d` is shed before `⛓`."""
    b = kg_board.build()
    unb = {t.id: models.unblocks_count(b, t) for t in b.tasks}
    for t in b.tasks:
        due, _tone = views.reldue_token(t, TODAY, b, include_done=True)
        if not due or t.archived:
            continue
        for wc in range(9, 41):
            _r1, r2 = kanban_card(t, b, wc, False, today=TODAY, unblocks=unb)
            assert _plain(r2).rstrip().endswith(due), (t.id, wc, _plain(r2))
    hub = b.task_by_id("tw2")                       # ⛓2 and a due
    _r1, r2 = kanban_card(hub, b, 14, False, today=TODAY, unblocks=unb)
    assert _plain(r2).rstrip().endswith("-3d")


def test_TC_302_the_selected_title_is_reverse_and_the_badge_stays():
    b = kg_board.build()
    r1, r2 = kanban_card(b.task_by_id("tw3"), b, 23, True, today=TODAY)
    assert "[reverse]Fix checkout 500" in r1 and "[reverse]" in r2
    token, tone = PRIORITY_BADGE["high"]
    assert f"[b reverse {HEX[tone]}]{token}[/]" in r1
    r1, _r2 = kanban_card(b.task_by_id("tw1"), b, 23, False, today=TODAY)   # done
    assert "reverse" not in r1


# --------------------------------------------------------------------------- #
# LLR-302.1 — separators and widths (TC-304, TC-305)
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("w", [24, 40, 60, 80, 100, 118, 160])
def test_TC_304_every_row_is_the_width_and_stacked_cards_are_separated(w):
    """TC-304 (HLR-302). Every row is exactly the panel width; in each cell one
    `┈` row sits between two cards and none after the last. The cells are read
    off the plan (band × column), the rows off the render. RED: no separator →
    the second card's row 1 sits right under the first card's row 2."""
    b = kg_board.build()
    text, rows, lm = render(b, w, 0)
    assert all(cell_len(r) == w for r in rows if r.strip()), w
    plan = kanban_plan(b, False, "tw3", TODAY, w, 0)
    seps = seps_of(rows)
    cells = [plan.high] + [band.cols for band in plan.bands]
    for cols in cells:
        for i in range(plan.start, plan.start + len(plan.widths)):
            ids = [t.id for t in cols[i]]
            for a, nxt in zip(ids, ids[1:]):
                assert lm[nxt] == lm[a] + 3, (w, a, nxt)
                between = cell(rows[lm[a] + 2], seps, i - plan.start)
                assert set(between) == {"┈"}, (w, a, between)
            if ids:
                after = cell(rows[lm[ids[-1]] + 2], seps, i - plan.start) \
                    if lm[ids[-1]] + 2 < len(rows) else ""
                assert "┈" not in after


def test_TC_305_the_columns_are_sized_by_their_titles():
    """TC-305 (LLR-302.1, LED .17). The split is proportional to each column's
    longest title (+5 for the spine and badge), the frames' rule: at 118 the
    oracle columns come out 24 / 27 / 23 / 24 — the frame's widths — and every
    split sums to its room; when the rule would leave a column under MIN_COL it
    falls back to MIN_COL first. RED: equal widths (`distribute`)."""
    b = kg_board.build()
    plan = kanban_plan(b, False, "tw3", TODAY, 118, 30)
    assert plan.widths == [24, 27, 23, 24], plan.widths
    assert len(set(plan.widths)) > 1 and min(plan.widths) >= MIN_COL
    for room in range(4 * MIN_COL, 200, 7):
        for desired in ([12, 12, 12, 12], [60, 12, 12, 12], [28, 30, 27, 28], [12, 40]):
            ws = _kanban_widths(room, desired)
            assert sum(ws) == room and min(ws) >= min(MIN_COL, room // len(desired))
    assert _kanban_widths(60, [60, 12, 12, 12]) == [24, 12, 12, 12]


# --------------------------------------------------------------------------- #
# LLR-303.1 — the band rule (TC-306)
# --------------------------------------------------------------------------- #
def test_TC_306_each_project_is_named_once_by_a_band_rule():
    """TC-306 (HLR-303). Unwindowed (h 0) the oracle board draws one band rule
    per project (5), each naming it once; no `▐` inside a card cell; the rules
    carry the facts; `┼` falls under every separator past the text. RED on
    base: 18 `▐ project` header cells."""
    b = kg_board.build()
    text, rows, lm = render(b, 118, 0)
    rules = [r for r in rows if is_rule(r)]
    assert [r.split("  ")[0][2:] for r in rules] == [p.name for p in b.projects]
    assert sum(r.count("▐") for r in rows) == 5
    web = next(r for r in rules if "Website" in r)
    assert "Website Redesign  5 open · 2 high ↑ · project due +10d" in web
    assert "at risk" in next(r for r in rules if "API Platform" in r)
    seps = seps_of(rows)
    for r in rules:
        end = len(r.rstrip("─┼ ").rstrip()) + 1
        for x in seps:
            if x > end:
                assert r[x] == "┼", (r, x)
    assert _due_fact(TODAY, TODAY) == ("due today", "soon")
    assert _due_fact(TODAY + timedelta(days=7), TODAY) == ("due +7d", "soon")
    assert _due_fact(TODAY + timedelta(days=8), TODAY) == ("due +8d", "dim")
    assert _due_fact(TODAY - timedelta(days=2), TODAY) == ("2d late", "over")


@pytest.mark.parametrize("group,names", [
    ("priority", ["High", "Normal", "Low"]),
    ("horizon", ["Overdue", "This week", "Later", "No date", "Done"])])
def test_TC_306_other_group_modes_draw_band_rules_too(group, names):
    """D-309 (PV-7): under `priority` and `horizon` each non-empty group opens a
    band rule; `priority` draws no high band (its High group IS the band).
    RED on base: per-column `▐ High` headers, no rule with an open count."""
    b = kg_board.build()
    _t, rows, _lm = render(b, 118, 0, kanban_group=group)
    rules = [r.split("  ")[0][2:] for r in rows if is_rule(r)]
    assert rules and set(rules) <= set(names)
    assert any(r.startswith("── high") for r in rows) == (group != "priority")


def test_TC_306_a_hostile_project_name_prints_literally():
    """C-17: the band rule and the fold row print the user's project name; the
    rule stays the panel's width. A regression PIN (the shipped headers obeyed
    it too); the rule's own literal is asserted on the band rule row."""
    b = kg_board.build()
    b.projects[0].name = "[b]Odd[/b] [link=http://e]x"
    for w in (24, 60, 118, 160):
        _t, rows, _lm = render(b, w, 0)
        assert all(cell_len(r) == w for r in rows if r.strip())
    _t, rows, _lm = render(b, 160, 0)
    assert any(is_rule(r) and "[b]Odd[/b] [link=http://e]x" in r for r in rows)


# --------------------------------------------------------------------------- #
# LLR-304.1 — the rail (TC-307)
# --------------------------------------------------------------------------- #
def test_TC_307_the_rail_is_titles_when_wide_and_a_count_when_narrow():
    """TC-307 (HLR-304). At 118 the rail head reads `✓ DONE 3` and Website's
    cell `✓ Design homepa…` over `done 18d ago`; at 80 `✓3` and `✓1` over
    `18d ago`; unwindowed nav's last column is the drawn done titles at 118 and
    holds no done id at 80 or collapsed. Boundary 99 / 100. RED on base: a
    full-width Done column."""
    b = kg_board.build()
    _t, rows, lm = render(b, 118, 0)
    assert rows[1].rstrip().endswith("✓ DONE 3")
    web = next(i for i, r in enumerate(rows) if r.startswith("▐ Website"))
    assert rows[web + 1].rstrip().endswith("✓ Design homepa…")
    assert rows[web + 2].rstrip().endswith("done 18d ago")
    nav = nav_model("kanban", b, False, TODAY, 118, 0, selected_id="tw3")
    assert nav[-1] == sorted(nav[-1], key=lambda i: lm[i]) == ["tw1", "tm1", "td1"]
    _t, rows, lm = render(b, 80, 0)
    assert rows[1].rstrip().endswith("✓3")
    web = next(i for i, r in enumerate(rows) if r.startswith("▐ Website"))
    assert rows[web + 1].rstrip().endswith("✓1") and rows[web + 2].rstrip().endswith("18d ago")
    done = {t.id for t in b.tasks if b.is_done(t)}
    assert not done & {i for c in nav_model("kanban", b, False, TODAY, 80, 0) for i in c}
    assert not done & set(lm)
    assert not done & {i for c in nav_model("kanban", b, False, TODAY, 118, 0,
                                           kanban_collapsed=True) for i in c}
    assert kanban_plan(b, False, None, TODAY, 100, 0).rail_titles
    assert not kanban_plan(b, False, None, TODAY, 99, 0).rail_titles
    assert kanban_plan(b, False, None, TODAY, 118, 0, collapsed=True).rail_w == 7


def test_TC_307_a_full_rail_counts_what_it_cannot_draw(tmp_path):
    """A band with one card (2 rows, room 3) and three done tasks draws ONE
    done title and `+2 more`; the newest first. A hostile done title prints
    literally and the row keeps its 16 cells (P2 S-1)."""
    p = Project("Solo", "sky")
    d = lambda n: (TODAY + timedelta(days=n)).isoformat()   # noqa: E731
    b = Board([p], [Task("only card", p.id, "Doing", id="o"),
                    Task("[/b]x [link=http://e]y", p.id, "Done", phase_changed=d(-1), id="d1"),
                    Task("older", p.id, "Done", phase_changed=d(-5), id="d2"),
                    Task("oldest", p.id, "Done", phase_changed=d(-9), id="d3")],
              tmp_path / "b.json", phases=["Doing", "Done"])
    _t, rows, lm = render(b, 118, 0, sel="d1")
    rule = next(i for i, r in enumerate(rows) if r.startswith("▐ Solo"))
    assert rows[rule + 1].endswith("✓ [/b]x [link=h…") and "d1" in lm
    assert rows[rule + 2].rstrip().endswith("  done 1d ago")
    assert rows[rule + 3].rstrip().endswith("+2 more")
    assert all(cell_len(r) == 118 for r in rows if r.strip())


# --------------------------------------------------------------------------- #
# LLR-305.1 — the high band (TC-308)
# --------------------------------------------------------------------------- #
def test_TC_308_the_high_band_is_first_and_holds_exactly_the_open_highs():
    """TC-308 (HLR-305). The band opens the body, holds the 9 open highs (P-2)
    above every project band, its rule counts what it draws; the tags drawn at
    118 are the frame's (8 of 9: `to1`'s row 2 has no room), each in its
    project's hue. RED on base: a `── high` divider in every column."""
    b = kg_board.build()
    text, rows, lm = render(b, 118, 0)
    assert rows[3].startswith("── high  9 open · 4 projects ")
    first_rule = next(i for i, r in enumerate(rows) if is_rule(r))
    assert {t for t, r in lm.items() if r < first_rule} == HIGH_IDS
    assert all(lm[t] > first_rule for t in lm if t not in HIGH_IDS)
    tagged = set()
    for tid in HIGH_IDS:
        t = b.task_by_id(tid)
        p = b.project_by_id(t.project_id)
        row2 = rows[lm[tid] + 1]
        if f" {p.name.split()[0]} " in row2:
            tagged.add(tid)
    assert tagged == HIGH_IDS - {"to1"}
    styled = [(text.plain[s.start:s.end], str(s.style)) for s in text.spans]
    assert ("Ops", HEX["rose"]) in [(t.strip(), st.split()[-1]) for t, st in styled
                                    if t.strip() == "Ops"]


@pytest.mark.parametrize("sort", _KANBAN_SORT_MODES)
def test_TC_308_the_band_keeps_the_seats_order(sort):
    """LLR-305.1. Per column, the band's cards are the seat's KANBAN_BAND group
    in the active sort's order (an oracle through the shipped seat)."""
    b = kg_board.build()
    plan = kanban_plan(b, False, "tw3", TODAY, 118, 0, sort=sort)
    for i, bucket in enumerate(views.phase_buckets(b, b.visible_tasks(False))[:-1]):
        g = kanban_order(b, bucket, False, sort=sort, band=True, today=TODAY)
        want = g[0][2] if g and g[0][0] == KANBAN_BAND else []
        assert [t.id for t in plan.high[i]] == [t.id for t in want], (sort, i)


def test_TC_308_tags_tell_projects_apart_and_print_literally(tmp_path):
    """D-307 (PV-5, P2 UX-8): the tag is the shortest run of leading WORDS no
    other project's name starts with — `API Platform` / `API Gateway` — and a
    bracket name prints literally."""
    ps = [Project("API Platform", "lime"), Project("API Gateway", "sky"),
          Project("[b]Odd[/b] Co", "pink"), Project("APIx", "violet")]
    tasks = [Task(f"urgent {i}", p.id, "Doing", "high", id=f"u{i}") for i, p in enumerate(ps)]
    b = Board(ps, tasks, tmp_path / "b.json", phases=["Doing", "Done"])
    tags = views._project_tags(b)
    assert [tags[p.id] for p in ps] == ["API Platform", "API Gateway", "[b]Odd[/b]", "APIx"]
    # WORD-wise (code review F3): `APIx` does not take the word `API`
    pair = Board([Project("API Foo", "lime"), Project("APIx", "sky")], [], tmp_path / "c.json",
                 phases=["Doing", "Done"])
    assert sorted(views._project_tags(pair).values()) == ["API", "APIx"]
    _t, rows, lm = render(b, 160, 0, sel=None)
    assert "[b]Odd[/b]" in rows[lm["u2"] + 1]


def test_TC_307_the_secondary_limbs_hold(tmp_path):
    """Code review F4/F7 of increment 001: a board whose only phase is the last
    draws every row at the panel width; the open count leaves archived cards
    out (LLR-303.1); the badge needs 9 cells (8 has none); the narrow rail's age
    is the NEWEST done task's; the head rule crosses at the rail's separator;
    two projects sharing a name keep two bands, each with its own cards."""
    one = Project("Solo", "sky")
    b = Board([one], [Task("a", one.id, "Done"), Task("b", one.id, "Done")],
              tmp_path / "one.json", phases=["Done"])
    for w in (24, 80, 120):
        _t, rows, _lm = render(b, w, 0, sel=None)
        assert all(cell_len(r) == w for r in rows), (w, [cell_len(r) for r in rows])
    m = mixed_board(tmp_path / "m.json")
    plan = kanban_plan(m, True, None, TODAY, 140, 0)
    alpha = next(band for band in plan.bands if band.name == "Alpha")
    drawn = [t for col in alpha.cols for t in col]
    assert any(t.archived for t in drawn)
    assert alpha.n_open == sum(1 for t in drawn if not t.archived) + alpha.n_high
    o = kg_board.build()
    t = o.task_by_id("tm5")
    assert "==" not in _plain(kanban_card(t, o, 8, False, today=TODAY)[0])
    assert "==" in _plain(kanban_card(t, o, 9, False, today=TODAY)[0])
    o.task_by_id("tw1").phase_changed = kg_board._d(-2)      # Website: newest 2d ago
    o.tasks.append(Task("old done", "pweb", "Done", phase_changed=kg_board._d(-40), id="tw9"))
    _t, rows, _lm = render(o, 80, 0)
    web = next(i for i, r in enumerate(rows) if r.startswith("▐ Website"))
    assert rows[web + 1].rstrip().endswith("✓2") and rows[web + 2].rstrip().endswith("2d ago")
    seps = seps_of(rows)
    assert all(rows[2][x] == "┼" for x in seps), rows[2]
    twins = [Project("Same", "sky"), Project("Same", "lime")]
    tb = Board(twins, [Task("one", twins[0].id, "Doing", id="s1"),
                       Task("two", twins[1].id, "Doing", id="s2")],
               tmp_path / "t.json", phases=["Doing", "Done"])
    bands = kanban_plan(tb, False, None, TODAY, 120, 0).bands
    assert [[x.id for x in band.cols[0]] for band in bands] == [["s1"], ["s2"]]


def test_TC_311_a_hostile_name_folds_literally_and_an_exact_fit_folds_nothing(tmp_path):
    """Code review F5: a band folded below prints its project's name literally
    in the fold row; a board whose bands fill the room EXACTLY draws no fold
    row (one row more and it folds)."""
    b = kg_board.build()
    b.project_by_id("pops").name = "[b]Odd[/b] Ops"
    _t, rows, _lm = render(b, 118, 30)
    assert FOLD.match(rows[-1]) and "[b]Odd[/b] Ops (5 open)" in rows[-1], rows[-1]
    p = Project("Fit", "sky")
    tasks = [Task(f"card {i}", p.id, "Doing", id=f"f{i}") for i in range(3)]
    fit_board = Board([p], tasks, tmp_path / "f.json", phases=["Doing", "Done"])
    q = Project("Next", "lime")
    fit_board.projects.append(q)
    fit_board.tasks.append(Task("other", q.id, "Doing", id="g0"))
    # head 3 + band Fit (1 + 8) + band Next (1 + 2) = 15 rows: h 15 fits, h 14 folds
    _t, rows, _lm = render(fit_board, 80, 15, sel="f0")
    assert not any(FOLD.match(r) for r in rows) and len(rows) == 15
    _t, rows, _lm = render(fit_board, 80, 14, sel="f0")
    assert FOLD.match(rows[-1]) and "▼ 1 below" in rows[-1]


# --------------------------------------------------------------------------- #
# LLR-301.1 — the seat: nav walks what is drawn (TC-301)
# --------------------------------------------------------------------------- #
ARMS = [(g, s, f, a) for g in _KANBAN_GROUP_MODES for s in _KANBAN_SORT_MODES
        for f in (False, True) for a in (False, True)]


def test_TC_301_the_arm_set_is_complete(tmp_path):
    """C-31 guard: the arms are derived from the seat's own tuples, and the
    board exercises every axis (archived, Inbox, highs in two projects)."""
    assert len(ARMS) == 60
    b = mixed_board(tmp_path / "m.json")
    assert any(t.archived for t in b.tasks) and any(t.project_id is None for t in b.tasks)
    assert len({t.project_id for t in b.tasks if t.priority == "high"
                and not b.is_done(t) and not t.archived}) >= 3


@pytest.mark.parametrize("group,sort,focus,archived", ARMS)
def test_TC_301_nav_is_the_draw_order(tmp_path, group, sort, focus, archived):
    """TC-301 (LLR-301.1). Unwindowed (h 0): nav ids = the drawn ids and each
    column is in draw order. Windowed (80×24, the cap at 140×14): the drawn ids
    ⊆ nav, the selection always drawn, the drawn part of each column in nav
    order. A regression PIN of the F-3 law on base (the shipped seat held it);
    RED under a nav that is not the renderer's plan (mutation battery)."""
    b = mixed_board(tmp_path / "m.json")
    fid = b.projects[0].id if focus else None
    kw = dict(kanban_sort=sort, kanban_group=group, kanban_focus=fid)
    for w, h in ((140, 0), (80, 24), (140, 14)):
        nav = nav_model("kanban", b, archived, TODAY, w, h, selected_id=None, **kw)
        flat = [i for c in nav for i in c]
        for sel in [c[0] for c in nav if c] or [None]:
            lm: dict = {}
            render_view("kanban", b, archived, sel, TODAY, w, h, lm, **kw)
            nav = nav_model("kanban", b, archived, TODAY, w, h, selected_id=sel, **kw)
            flat = [i for c in nav for i in c]
            if h == 0:
                assert set(flat) == set(lm), (w, h, sel)
            assert set(lm) <= set(flat) and (sel is None or sel in lm), (w, h, sel)
            for c in nav:
                drawn = [i for i in c if i in lm]
                assert drawn == sorted(drawn, key=lambda i: lm[i]), (w, h, c)


def test_TC_301_a_window_of_phases_follows_the_selection(tmp_path):
    """The shipped phase window over the OPEN phases: 7 open phases at 80 do
    not fit; nav keeps every open phase (one column each) plus nothing for the
    count rail; the window drawn holds the selected task's phase."""
    b = eight_phases(tmp_path / "e.json")
    nav = nav_model("kanban", b, False, TODAY, 80, 24, selected_id="t5")
    assert len(nav) == 7
    lm: dict = {}
    render_view("kanban", b, False, "t5", TODAY, 80, 24, lm)
    assert "t5" in lm


# --------------------------------------------------------------------------- #
# LLR-301.3 — the chrome as shipped (TC-313)
# --------------------------------------------------------------------------- #
def test_TC_313_the_chrome_names_the_modes_and_counts_hidden_phases(tmp_path):
    """TC-313 (LLR-301.3). The head names a non-default sort, group and focus;
    the WIP tag burns `over` when strictly over; the window markers count the
    OPEN phases hidden (never the rail's); an empty board says so. RED: the
    markers counting the rail's phase as hidden."""
    b = kg_board.build()
    text, rows, _lm = render(b, 118, 0, kanban_sort="due", kanban_group="horizon",
                             kanban_focus="pweb")
    assert "sort: due" in rows[0] and "group: horizon" in rows[0]
    assert "focus: Website Redesign" in rows[0]
    text, rows, _lm = render(b, 118, 0)
    assert "6/4" in rows[1]
    e = eight_phases(tmp_path / "e.json")
    _t, rows, _lm = render(e, 80, 24, sel="t0")
    plan = kanban_plan(e, False, "t0", TODAY, 80, 24)
    hidden = 7 - (plan.start + len(plan.widths))
    assert hidden > 0 and f"{hidden} ▶" in rows[1], rows[1]
    empty = Board([], [], tmp_path / "x.json", phases=["Doing", "Done"])
    _t, rows, _lm = render(empty, 80, 24, sel=None)
    assert any("(no tasks — press 'a' to add one)" in r for r in rows)


# --------------------------------------------------------------------------- #
# LLR-309.1 — the fold (TC-311)
# --------------------------------------------------------------------------- #
def test_TC_311_the_board_folds_whole_bands_and_names_them():
    """TC-311 (HLR-309). At 118×30 with `tw3` the render is exactly 30 rows and
    its last row is the approved frame's; with `to3` the Ops band is drawn and
    the folded bands above are named; at h 0 nothing folds. RED: an unwindowed
    render is taller than the panel and names nothing."""
    b = kg_board.build()
    _t, rows, lm = render(b, 118, 30)
    assert len(rows) == 30
    assert rows[-1].rstrip() == "▼ 2 below: Data Warehouse (4 open), Ops & Security (5 open)"
    _t, rows, lm = render(b, 118, 30, sel="to3")
    assert "to3" in lm and any(r.startswith("▐ Ops & Security") for r in rows)
    assert rows[-1].startswith("▲ 2 above: Website Redesign (5 open), Mobile App (5 open)")
    # a one-sided `▲` row keeps its names at 80 too (code review F10 of increment 003)
    _t, rows, lm = render(b, 80, 24, sel="to3")
    assert rows[-1].startswith("▲ 4 above: Website Redesign (5 open)"), rows[-1]
    _t, rows, lm = render(b, 118, 0)
    assert not any(FOLD.match(r) for r in rows) and len(lm) == 28


@pytest.mark.parametrize("w,h", [(118, 30), (80, 24), (80, 22), (40, 22)])
def test_TC_311_every_selection_is_drawn_inside_the_panel(w, h):
    """LLR-309.1 over EVERY task as the selection (the set is the board's, not
    hand-listed): the selected card is drawn, both its rows inside the panel,
    the render exactly `h` rows; at 80 with bands folded on both sides the fold
    row prints both counts (P2 UX-15)."""
    b = kg_board.build()
    names = [band.name for band in kanban_plan(b, False, None, TODAY, w, h).bands]
    both = 0
    for t in b.tasks:
        _t, rows, lm = render(b, w, h, sel=t.id)
        assert len(rows) == h, (t.id, len(rows))
        if b.is_done(t) and w < 100:
            assert t.id not in lm
            continue
        assert t.id in lm and lm[t.id] + 1 < h - (1 if FOLD.match(rows[-1]) else 0)
        # what folded, read off the band rules drawn — and the fold row must
        # print the count of EVERY side that folded (P2 UX-15), at any width
        drawn = [i for i, n in enumerate(names) if any(r.startswith(f"▐ {n}  ") for r in rows)]
        above, below = drawn[0], len(names) - 1 - drawn[-1]
        fold = rows[-1] if FOLD.match(rows[-1]) else ""
        assert (f"▲ {above} above" in fold) == bool(above), (t.id, fold)
        assert (f"▼ {below} below" in fold) == bool(below), (t.id, fold)
        both += bool(above and below)
        assert cell_len(rows[-1]) == w
    if w <= 80:
        assert both > 0, "no frame folded on both sides: the UX-15 arm is vacuous"


def test_TC_311_a_down_into_a_drawn_band_moves_nothing():
    """P2 UX-14 (D-314): walking down column 0, a step into a band already
    drawn leaves the drawn band set unchanged. RED: the prototype's
    selection-first window."""
    b = kg_board.build()
    col = nav_model("kanban", b, False, TODAY, 118, 30, selected_id="tw5")[0]

    def drawn_rules(sel):
        _t, rows, lm = render(b, 118, 30, sel=sel)
        return [r.split("  ")[0] for r in rows if is_rule(r)], lm

    assert drawn_rules(col[0])[0], "no band rule drawn: vacuous"

    for a, nxt in zip(col, col[1:]):
        before, _ = drawn_rules(a)
        after, lm = drawn_rules(nxt)
        _t, rows, lm_a = render(b, 118, 30, sel=a)
        if nxt in lm_a:
            assert after == before, (a, nxt)


# --------------------------------------------------------------------------- #
# Layer B — through the running app
# --------------------------------------------------------------------------- #
class _Today(kg_board.date):
    @classmethod
    def today(cls):
        return TODAY


@pytest.fixture
def frozen_today(monkeypatch):
    for mod in (views, app_mod, models):
        monkeypatch.setattr(mod, "date", _Today)


async def _kanban_app(tmp_path, size, sel="tw3", board=None):
    b = board or kg_board.build(tmp_path / "board.json")
    b.path = tmp_path / "board.json"
    b.save()
    app = TaskboardApp(board_path=str(b.path), team_sync_interval=1e9)
    return app


def _painted(app) -> list[str]:
    return str(app.query_one("#board").render()).split("\n")


def _viewport_h(app) -> int:
    return app.query_one("#viewport").size.height


@pytest.mark.parametrize("size,floor,full", [((118, 32), 11.0, 12), ((80, 26), 5.5, 0),
                                             ((80, 24), None, 0)])
async def test_AT_301_cards_read_across_the_column(tmp_path, frozen_today, size, floor, full):
    """AT-301 (US-301). Key `4` in the running app: every painted card is two
    rows — row 1 badge + title, row 2 the spine under it — stacked cards are
    split by `┈`, the columns differ in width, and the measured title
    readability clears the floor (base 7.3 / 1.0, P-1). RED on base: one-row
    cards, no `┈`, equal columns, 7.3 chars."""
    app = await _kanban_app(tmp_path, size)
    async with app.run_test(size=size) as pilot:
        await pilot.press("4")
        app.selected_task_id = "tw3"
        app.refresh_view()
        await pilot.pause()
        rows = _painted(app)
        h = _viewport_h(app)
        seps = seps_of(rows)
        assert len({b - a for a, b in zip([-1] + seps, seps)}) > 1, "equal columns"
        assert any(set(cell(r, seps, 0)) == {"┈"} for r in rows)
        cards = 0
        for k, r in enumerate(rows[3:h - 1], start=3):
            for i in range(len(seps)):
                c1 = cell(r, seps, i)
                if c1[:5] in ("▊ !! ", "▊ == ", "▊ ++ ", "▲ !! "):
                    cards += 1
                    assert cell(rows[k + 1], seps, i).startswith("▊"), (k, i, c1)
        assert cards >= 10
        if floor is not None:
            avg, nfull, _drawn = readability(body(rows, h), [t.title for t in app.board.tasks])
            assert avg >= floor and nfull >= full, (avg, nfull)


async def test_AT_302_projects_are_named_once_and_done_is_a_rail(tmp_path, frozen_today):
    """AT-302 (US-302). Key `4`: band rules name the projects drawn, no `▐` in a
    card cell; the rail heads `✓ DONE 3`; `right` ×4 from Backlog lands on a
    rail title; `z` collapses the rail to `✓3`; `g` ×2 draws the horizon's band
    rules; `v` draws an archived card. At 80 the rail is a count."""
    b = kg_board.build(tmp_path / "board.json")
    b.tasks.append(Task("Archived chore", "pweb", "Backlog", "normal", archived=True, id="tar"))
    app = await _kanban_app(tmp_path, (118, 32), board=b)
    async with app.run_test(size=(118, 32)) as pilot:
        await pilot.press("4")
        app.selected_task_id = "tw5"
        app.refresh_view()
        await pilot.pause()
        rows = _painted(app)
        rules = [r for r in rows if is_rule(r)]
        assert len(rules) >= 3 and sum(r.count("▐") for r in rows) == len(rules)
        assert rows[1].rstrip().endswith("✓ DONE 3")
        for _ in range(4):
            await pilot.press("right")
        assert app.board.is_done(app.selected_task)
        await pilot.press("z")
        await pilot.pause()
        assert _painted(app)[1].rstrip().endswith("✓3")
        await pilot.press("z")
        for _ in range(2):
            await pilot.press("g")
        await pilot.pause()
        assert app.kanban_group == "horizon"
        assert any(r.startswith(("▐ Overdue", "▐ This week", "▐ Later")) for r in _painted(app))
        await pilot.press("g")
        await pilot.press("v")
        await pilot.pause()
        assert any("Archived chore" in r for r in _painted(app))
    app = await _kanban_app(tmp_path, (80, 26))
    async with app.run_test(size=(80, 26)) as pilot:
        await pilot.press("4")
        await pilot.pause()
        assert _painted(app)[1].rstrip().endswith("✓3")


async def test_AT_303_the_high_band_is_first_and_the_cursor_walks_it(tmp_path, frozen_today):
    """AT-303 (US-303). Key `4`: the first band is `── high`; from the top of
    Backlog `down` visits its four highs in the band's order, then the project
    bands; `!` raising `SEO redirects map` to high moves it into the band with
    the cursor; `g` to priority draws no high band; `s` reorders the band as the
    seat orders it."""
    app = await _kanban_app(tmp_path, (118, 32))
    async with app.run_test(size=(118, 32)) as pilot:
        await pilot.press("4")
        app.selected_task_id = "tw5"
        app.refresh_view()
        await pilot.pause()
        rows = _painted(app)
        assert rows[3].startswith("── high  9 open · 4 projects")
        seen = ["tw5"]
        for _ in range(5):
            await pilot.press("down")
            seen.append(app.selected_task_id)
        assert seen[:4] == ["tw5", "tm4", "ta2", "to5"] and seen[4] == "tw6", seen
        app.selected_task_id = "tw6"
        app.refresh_view()
        await pilot.pause()
        await pilot.press("exclamation_mark")
        await pilot.pause()
        assert app.selected_task_id == "tw6" and app.board.task_by_id("tw6").priority == "high"
        rows = _painted(app)
        first_rule = next(i for i, r in enumerate(rows) if is_rule(r))
        assert app._line_map["tw6"] < first_rule
        await pilot.press("g")
        await pilot.pause()
        assert app.kanban_group == "priority"
        assert not any(r.startswith("── high") for r in _painted(app))
        await pilot.press("g", "g", "s")
        await pilot.pause()
        assert app.kanban_sort == "priority" and app.kanban_group == "project"
        nav = app._nav_columns()
        g = kanban_order(app.board, [t for t in app.board.tasks if t.phase == "Backlog"],
                         False, sort="priority", band=True, today=TODAY)
        assert nav[0][:len(g[0][2])] == [t.id for t in g[0][2]]


async def test_AT_305_the_kanban_spends_no_accent(tmp_path, frozen_today):
    """AT-305 (US-301..303). The painted board at terminals 118×32 and 80×26:
    0 accent runs (a PIN — true on base); every `+1d`..`+7d`/`today` token
    amber, every `-Nd` red; Ops & Security's `project due +5d` amber; every
    `┈` in the frame tone (the gate arms); the selection reverse (PIN)."""
    for size in ((118, 32), (80, 26)):
        app = await _kanban_app(tmp_path, size, board=kg_board.build(tmp_path / "board.json"))
        async with app.run_test(size=size) as pilot:
            await pilot.press("4")
            app.selected_task_id = "to3"
            app.refresh_view()
            await pilot.pause()
            text = app.query_one("#board").render()
            plain = text.plain
            spans = [(plain[s.start:s.end], s.style) for s in text.spans]

            def colour(st):
                st = str(st).lower()
                return st, "reverse" in st
            styled = [(t, colour(st)) for t, st in spans]
            assert any(has(st, "frame") for _t, (st, _r) in styled), "no tone readable: vacuous"
            assert not [t for t, (st, _r) in styled if has(st, "accent")]
            soon = [t for t, _x in styled if t.strip() == "today"
                    or (t.strip()[:1] == "+" and t.strip()[1:-1].isdigit()
                        and int(t.strip()[1:-1]) <= 7)]
            assert soon, "no soon token painted: vacuous"
            for t, (st, _r) in styled:
                s_ = t.strip()
                if s_ == "today" or (s_[:1] == "+" and s_[1:-1].isdigit() and s_.endswith("d")
                                     and int(s_[1:-1]) <= 7):
                    assert has(st, "soon"), (t, st)
                if s_[:1] == "-" and s_[1:-1].isdigit() and s_.endswith("d"):
                    assert has(st, "over"), (t, st)
                if s_ and set(s_) == {"┈"}:
                    assert has(st, "frame"), (t, st)
            assert any("project due +5d" in t and has(st, "soon")
                       for t, (st, _r) in styled)
            # the selection, as the terminal receives it (the composited strips)
            segs = [seg for strip in app.screen._compositor.render_strips(app.screen.size)
                    for seg in strip if "Review pull" in seg.text]
            assert segs and all(seg.style is not None and seg.style.reverse for seg in segs)


@pytest.mark.parametrize("size,kind,g_presses", [((118, 30), "oracle", 0), ((80, 24), "oracle", 0),
                                                ((80, 24), "oracle", 2), ((118, 30), "14high", 0),
                                                ((80, 24), "14high", 0)])
async def test_AT_307_the_selected_card_is_always_whole_on_screen(tmp_path, frozen_today, size,
                                                                  kind, g_presses):
    """AT-307 (US-302, US-303). Walking `down` the whole Backlog column at the
    operator's terminal sizes — on the oracle board, under `g g` (horizon, where
    the `Later` band is taller than the room) and on a board of 14 highs —
    after every step the board fits the panel (it never scrolls: the head row
    and the fold row stay on screen), both rows of the selected card and the
    rule of ITS band are inside it, and a step into a band already drawn moves
    no band (P2 UX-3, UX-14; P4 UXV3-1). RED on base at 80×24: the panel
    scrolls and the band names scroll off; RED before increment 003 under
    horizon and on the 14-high board: a band taller than the room scrolled."""
    board = many_highs(tmp_path / "board.json") if kind == "14high" else None
    app = await _kanban_app(tmp_path, size, board=board)
    async with app.run_test(size=size) as pilot:
        await pilot.press("4")
        for _ in range(g_presses):
            await pilot.press("g")
        app.selected_task_id = "tw5"
        app.refresh_view()
        await pilot.pause()
        h = _viewport_h(app)
        col = app._nav_columns()[0]
        for _ in col[1:]:
            before = [r.split("  ")[0] for r in _painted(app) if is_rule(r)]   # the band SET
            drawn_before = set(app._line_map)
            await pilot.press("down")
            await pilot.pause()
            rows, idx = _painted(app), app._line_map[app.selected_task_id]
            top = app.query_one("#viewport").scroll_offset.y
            assert top == 0 and len(rows) == h, (app.selected_task_id, top, len(rows), h)
            assert idx + 1 < h, (app.selected_task_id, idx, h)
            plan = kanban_plan(app._view_board(), False, app.selected_task_id, TODAY,
                               app.query_one("#board").size.width, h, group=app.kanban_group)
            band = next((bd.name for bd in plan.bands
                         if any(t.id == app.selected_task_id for c_ in bd.cols for t in c_)), None)
            above = [rows[k] for k in range(0, idx) if is_rule(rows[k])
                     or rows[k].startswith("── high")]
            assert above, (app.selected_task_id, "no band rule above it on screen")
            own = above[-1]
            assert (own.startswith(f"▐ {band}  ") if band else own.startswith("── high  ")), \
                (app.selected_task_id, band, own)
            if app.selected_task_id in drawn_before:
                assert [r.split("  ")[0] for r in rows if is_rule(r)] == before
        assert app.selected_task_id == col[-1]


# --------------------------------------------------------------------------- #
# Increment 002 — the cap (TC-309, AT-304), the copy (TC-310, AT-306), the
# cursor off undrawn done work (TC-312, AT-308)
# --------------------------------------------------------------------------- #
def many_highs(path=None) -> Board:
    """The oracle board plus 10 open highs in Backlog (14 there in all), spread
    over the five projects — a board the high band would otherwise fill."""
    b = kg_board.build(path or "kg-board-never-saved.json")
    pids = [p.id for p in b.projects]
    for i in range(10):
        b.tasks.append(Task(f"Urgent item {i + 1}", pids[i % 5], "Backlog", "high",
                            due_date=kg_board._d(5 + i), phase_changed=kg_board._d(-3),
                            id=f"tx{i}"))
    return b


H_TABLE = {0: None, 11: 5, 12: 6, 13: 6, 14: 7, 19: 10, 20: 11, 22: 12, 24: 14, 30: 18}


@pytest.mark.parametrize("h,R", sorted(H_TABLE.items()))
def test_TC_309_the_cap_is_two_thirds_of_the_body(h, R):
    """TC-309 (LLR-306.1, the executed h-table). With R = max(5, 2·(h − 3) // 3)
    a column of m open highs shows all when 3m − 1 ≤ R, else R // 3 and one
    `+N more ↓` row under them (no `┈` before it); its band rows never exceed
    R; the overflow is drawn in its project bands. h 0 shows every high.
    RED: K = R // 3 + 1 → the band passes R."""
    b = many_highs()
    plan = kanban_plan(b, False, "tw3", TODAY, 118, h)
    backlog = [t for t in b.visible_tasks(False) if t.phase == "Backlog"
               and t.priority == "high"]
    assert len(backlog) == 14
    shown, over = len(plan.high[0]), plan.overflow[0]
    if R is None:
        assert (shown, over) == (14, 0)
        return
    want = 14 if 3 * 14 - 1 <= R else R // 3
    assert (shown, over) == (want, 14 - want), (h, R, shown, over)
    rows = 3 * shown - 1 + (1 if over else 0)
    assert rows <= R
    in_bands = {t.id for band in plan.bands for t in band.cols[0]}
    assert {t.id for t in backlog} - {t.id for t in plan.high[0]} <= in_bands
    oracle = kanban_plan(kg_board.build(), False, "tw3", TODAY, 118, h)
    capped = h and 3 * 4 - 1 > R                 # the oracle Backlog: 4 highs
    assert (oracle.overflow[0] > 0) == bool(capped), (h, R)


def test_TC_309_the_overflow_row_sits_right_under_the_band(tmp_path):
    """The `+N more ↓` row: mut, directly under the last shown high (no `┈`),
    and the overflow highs are selectable in their project bands (nav ⊇)."""
    b = many_highs()
    text, rows, lm = render(b, 118, 30)
    seps = seps_of(rows)
    plan = kanban_plan(b, False, "tw3", TODAY, 118, 30)
    last = plan.high[0][-1].id
    assert cell(rows[lm[last] + 2], seps, 0).startswith("+8 more ↓")
    nav = nav_model("kanban", b, False, TODAY, 118, 30, selected_id="tw3")
    over = [t.id for t in b.visible_tasks(False) if t.phase == "Backlog"
            and t.priority == "high" and t.id not in {x.id for x in plan.high[0]}]
    assert len(over) == 8 and set(over) <= {i for c in nav for i in c}


async def test_AT_304_a_board_full_of_highs_keeps_its_projects(tmp_path, frozen_today):
    """AT-304 (US-303). 14 open highs in Backlog at terminal 118×32: the band
    draws 6 of them and `+8 more ↓`, at least one project band rule is still on
    screen, and walking `down` reaches every overflow high (each then drawn).
    RED: an uncapped band (41 rows) leaves no project on screen."""
    b = many_highs(tmp_path / "board.json")
    app = await _kanban_app(tmp_path, (118, 32), board=b)
    async with app.run_test(size=(118, 32)) as pilot:
        await pilot.press("4")
        app.selected_task_id = "tw5"
        app.refresh_view()
        await pilot.pause()
        rows = _painted(app)
        assert any("+8 more ↓" in r for r in rows)
        assert any(is_rule(r) for r in rows[:_viewport_h(app)])
        col = app._nav_columns()[0]
        overflow = set(col[6:]) & {t.id for t in app.board.tasks if t.priority == "high"}
        reached = set()
        for _ in col[1:]:
            await pilot.press("down")
            await pilot.pause()
            if app.selected_task_id in overflow:
                assert app.selected_task_id in app._line_map
                reached.add(app.selected_task_id)
        assert reached == overflow and len(overflow) == 8


def test_TC_310_the_help_describes_the_new_board():
    """TC-310 (LLR-308.1). The kanban help names the band rule, `┈`, the rail
    and `+N more ↓` — each absent from the shipped copy — and no longer the
    per-column band; every bullet fits the help's 44-cell column; the example
    shows the meta order (`⛓N` before the due); the legend calls `▐` the
    project's band. RED on base: "the top of each column"."""
    usage = [line for _h, lines in views.help_usage("kanban") for line in lines]
    text = " ".join(usage)
    for word in ("band rule", "┈", "rail", "more ↓"):
        assert word in text, word
    assert "top of each column" not in text and "grouped" in text
    assert all(cell_len(line) <= 44 for line in usage), [x for x in usage if cell_len(x) > 44]
    line, _meaning = views.help_example("kanban")
    assert line.index("⛓") < line.index("+4d")
    b = kg_board.build()
    labels = [m for s, m in views.legend_entries("kanban", b, TODAY, 118, 30)
              if _plain(s) == "▐"]
    assert labels == ["project band, by colour"]


async def test_AT_306_the_help_explains_what_is_drawn(tmp_path, frozen_today):
    """AT-306 (US-301..303). `?` in the kanban paints the new copy: the band
    rule, `┈`, the rail, `+N more ↓` — and not the per-column band. RED on
    base: "the top of each column"."""
    app = await _kanban_app(tmp_path, (118, 32))
    async with app.run_test(size=(118, 32)) as pilot:
        await pilot.press("4")
        await pilot.pause()
        await pilot.press("question_mark")
        await pilot.pause()
        painted = "\n".join(w.render().plain for w in app.screen.query("Label"))
        for word in ("band rule", "┈", "rail", "more ↓", "project band"):
            assert word in painted, word
        assert "top of each column" not in painted


def _posted(app, before: int) -> list[str]:
    """The notifications posted since `before` (the boot notice is not ours)."""
    return [n.message for n in list(app._notifications)[before:]]


@pytest.mark.parametrize("size,sel,lands", [((80, 24), "to3", "ta6"), ((80, 24), "tw2", "tm6"),
                                            ((118, 30), "to3", None)])
async def test_AT_308_finishing_a_card_keeps_the_cursor_on_the_board(tmp_path, frozen_today,
                                                                     size, sel, lands):
    """AT-308 (US-302). At terminal 80×24 the rail is a count: `]` on `to3`
    (Review, the column's last card) moves the cursor to `ta6`, the card above
    it; on `tw2` (Review's first) to `tm6`, the card that took its place (code
    review F3 of increment 002) — drawn, and one notification names the task
    literally; `u` brings it back. At 118×30 the rail draws done titles: the
    cursor stays on `to3`, now a rail title, and nothing is posted. RED on
    base: the cursor rests on an undrawn task, nothing posted."""
    b = kg_board.build(tmp_path / "board.json")
    app = await _kanban_app(tmp_path, size, board=b)
    title = b.task_by_id(sel).title
    async with app.run_test(size=size) as pilot:
        await pilot.press("4")
        app.selected_task_id = sel
        app.refresh_view()
        await pilot.pause()
        before = len(app._notifications)
        await pilot.press("]")
        await pilot.pause()
        assert app.board.task_by_id(sel).phase == "Done"
        notes = _posted(app, before)
        if lands:
            assert app.selected_task_id == lands and lands in app._line_map
            assert notes == [f"{title} done · counted in the ✓ rail · u undo"]
            await pilot.press("u")
            await pilot.pause()
            assert app.board.task_by_id(sel).phase == "Review"
        else:
            assert app.selected_task_id == sel and sel in app._line_map
            assert not notes


async def test_TC_312_the_notification_prints_a_bracket_title_literally(tmp_path,
                                                                          frozen_today):
    """TC-312 (LLR-310.1, C-17): the notification is markup-off — a title
    `[b]x[/b]` reaches the painted toast as typed; and a resize to a count
    rail moves a done selection by the `z` rule, with no notification."""
    b = kg_board.build(tmp_path / "board.json")
    b.task_by_id("to3").title = "[b]x[/b]"
    app = await _kanban_app(tmp_path, (80, 24), board=b)
    async with app.run_test(size=(80, 24), notifications=True) as pilot:
        await pilot.press("4")
        app.selected_task_id = "to3"
        app.refresh_view()
        await pilot.pause()
        before = len(app._notifications)
        await pilot.press("]")
        await pilot.pause()
        assert _posted(app, before) == ["[b]x[/b] done · counted in the ✓ rail · u undo"]
        await pilot.pause()
        painted = [str(t.render()) for t in app.screen.query("Toast")]
        assert any("[b]x[/b] done" in p for p in painted), painted
    app = await _kanban_app(tmp_path, (118, 30), board=kg_board.build(tmp_path / "board.json"))
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.press("4")
        app.selected_task_id = "tw1"                  # a done rail title at 118
        app.refresh_view()
        await pilot.pause()
        assert app.selected_task_id == "tw1" and "tw1" in app._line_map
        before = len(app._notifications)
        await pilot.resize_terminal(80, 24)
        await pilot.pause()
        app.refresh_view()
        await pilot.pause()
        # the `z` rule: the first card of the nearest column at or left of
        # Done — Review's first, `tw2` (code review F2 of increment 002)
        assert app.selected_task_id == app._nav_columns()[3][0] == "tw2"
        assert "tw2" in app._line_map and _posted(app, before) == []


@pytest.mark.parametrize("how", ["filter", "lost"])
async def test_TC_312_a_reset_selection_never_lands_on_a_counted_card(tmp_path, frozen_today,
                                                                       how):
    """Code review F1 of increment 002 (HIGH): when the selection stops being
    visible (a `/` filter hides it, its task is gone) the app resets it to the
    first visible task in board order — `tw1`, a DONE task the 80-cell rail
    only counts. The `z` rule must apply after that reset too. RED: the reset
    leaves the cursor on `tw1`, absent from the drawn board."""
    app = await _kanban_app(tmp_path, (80, 24), board=kg_board.build(tmp_path / "board.json"))
    async with app.run_test(size=(80, 24)) as pilot:
        await pilot.press("4")
        app.selected_task_id = "tw3"
        app.refresh_view()
        await pilot.pause()
        if how == "filter":
            app.search_query = "p"         # `Design homepage mockups` stays; `tw3` goes
        else:
            app.selected_task_id = "no-such-task"
        app.refresh_view()
        await pilot.pause()
        assert app.selected_task_id is not None and app.selected_task_id != "tw1"
        assert app.selected_task_id in app._line_map


@pytest.mark.parametrize("size", [(80, 14), (80, 15), (80, 22), (80, 23)])
async def test_TC_309_a_filtered_board_walks_what_it_draws(tmp_path, frozen_today, size):
    """D-312 (code review F2 of increment 001): under a `/` filter the board is
    drawn two rows shorter, and the cap and the window read the height — so the
    app asks the nav for that same height. At every selection of the filtered
    board, the drawn part of each nav column is in draw order. RED: the nav
    asked with the full height (panels 12, 13, 20, 21 disagree)."""
    b = kg_board.build(tmp_path / "board.json")
    for t in b.tasks:
        t.title += " zz"
    app = await _kanban_app(tmp_path, size, board=b)
    async with app.run_test(size=size) as pilot:
        await pilot.press("4")
        app.search_query = "zz"
        app.refresh_view()
        await pilot.pause()
        for sel in [i for c in app._nav_columns() for i in c]:
            app.selected_task_id = sel
            app.refresh_view()
            await pilot.pause()
            lm = app._line_map
            for col in app._nav_columns():
                drawn = [i for i in col if i in lm]
                assert drawn == sorted(drawn, key=lambda i: lm[i]), (size, sel, col)


# --------------------------------------------------------------------------- #
# P4 iteration 1 → increment 003: the shared title seat, and a band taller than
# the room
# --------------------------------------------------------------------------- #
TITLE_SEATS = [("agenda", {}), ("kanban", {"presentation": "matrix"}),
               ("kanban", {"presentation": "lanes"}),
               ("focus", {"focus_presentation": "inspector"}),
               ("focus", {"focus_presentation": "review"})]


@pytest.mark.parametrize("mode,kw", TITLE_SEATS)
def test_TC_302_the_shared_title_seat_prints_a_backslash_before_a_bracket(mode, kw):
    """P4 qa G-003a: `title_markup` — the title seat of the agenda, the kanban's
    matrix and lanes, the Focus views — now writes its piece through `_literal`
    too (increment 001). Rich drops the backslash before ANY bracket, so on the
    base tree a task titled a-backslash-[b printed as `a[b` in every one of these seats
    (measured at every width 24..100). RED on base `13745f6`."""
    title = "a" + chr(92) + "[b"
    p = Project("P", "sky")
    t = Task(title, p.id, "Doing", pinned=True, due_date=TODAY.isoformat())
    b = Board([p], [t], Path("never-written.json"), phases=["Backlog", "Doing", "Done"])
    rows = render_view(mode, b, False, t.id, TODAY, 100, 14, {}, **kw).plain.split("\n")
    assert any(title in r for r in rows), (mode, kw)


def test_TC_311_a_band_taller_than_the_room_is_cut_around_the_selection():
    """LLR-309.2 (P4 UXV3-1). Under `horizon` at panel 80×22 the `Later` band
    is taller than the room: it is cut on card boundaries around the selection
    and the fold row counts the cards cut off — `▲ 3 more in Later   ▼ 1 more in
    Later` with `td3` selected, `▲ 5 more in Later` with `td5` — so the board
    is exactly the panel's height and the card is whole; unwindowed (h 0) the
    band is drawn whole. RED: the band drawn alone and scrolling (the render
    taller than the panel, the fold row past its bottom)."""
    b = kg_board.build()
    for sel, want in (("td3", ("▲ 3 more in Later", "▼ 1 more in Later")),
                      ("td5", ("▲ 5 more in Later",))):
        _t, rows, lm = render(b, 80, 22, sel=sel, kanban_group="horizon")
        assert len(rows) == 22 and FOLD.match(rows[-1]), (sel, len(rows))
        assert all(x in rows[-1] for x in want), (sel, rows[-1])
        assert sel in lm and lm[sel] + 1 < 21
        assert any(r.startswith("▐ Later  ") for r in rows[:lm[sel]])
    _t, rows, lm = render(b, 80, 0, sel="td5", kanban_group="horizon")
    assert "more in" not in "\n".join(rows) and len(lm) == 25
    # the cut starts on a card's first row: at panel 80×23 the room is 6 body
    # rows and `td5` (row 9) needs the cut at row 5 — rounded up to the card at 6
    _t, rows, lm = render(b, 80, 23, sel="td5", kanban_group="horizon")
    rule = next(i for i, r in enumerate(rows) if r.startswith("▐ Later  "))
    assert rows[rule + 1].startswith("▊ ++ Archive"), rows[rule + 1]
    # a board of ONE band taller than the room keeps every band and still
    # names what the cut hides (the fold row is drawn for a cut alone)
    p = Project("Solo", "sky")
    solo = Board([p], [Task(f"card {i}", p.id, "Doing", id=f"c{i}") for i in range(8)],
                 Path("never-written.json"), phases=["Doing", "Done"])
    _t, rows, lm = render(solo, 80, 14, sel="c0")
    assert len(rows) == 14 and rows[-1].startswith("▼ 5 more in Solo"), rows[-1]


def _tall(tmp_path, names, cards, done=0):
    """Projects `names` with one Backlog card each, the LAST holding `cards`
    cards and `done` done ones — a band taller than any small room."""
    ps = [Project(n, "sky") for n in names]
    tasks = [Task(f"{n.split()[0]} task", p.id, "Backlog", id=f"p{i}")
             for i, (n, p) in enumerate(zip(names, ps[:-1]))]
    tasks += [Task(f"tall card {i}", ps[-1].id, "Backlog", id=f"t{i}") for i in range(cards)]
    tasks += [Task(f"tall done {i}", ps[-1].id, "Done",
                   phase_changed=(TODAY - timedelta(days=i)).isoformat(), id=f"d{i}")
              for i in range(done)]
    return Board(ps, tasks, tmp_path / "tall.json", phases=["Backlog", "Doing", "Done"])


def test_TC_311_the_cut_keeps_every_count_and_whole_cards(tmp_path):
    """Code review round 1 of increment 003. F1 (HIGH): a single band that
    EXACTLY fits the panel is not cut (the fold row's line is free when nothing
    folds). F2 (HIGH): every count prints — with the cut band last (nothing
    below) and with a long band name and bands on both sides. F3: the cut ends
    on a card's second row, never on a lone first row. F5: the cut's counts are
    the band's open cards, not its rail titles."""
    one = _tall(tmp_path, ["Solo"], 12)
    full = len(render(one, 80, 0, sel="t0")[1])
    for sel in ("t0", "t11"):
        _t, rows, lm = render(one, 80, full, sel=sel)
        assert not any("more in" in r for r in rows) and len(lm) == 12, (sel, rows[-1])
    _t, rows, lm = render(one, 80, full - 1, sel="t0")
    assert FOLD.match(rows[-1]) and "▼" in rows[-1] and "more" in rows[-1]
    last = _tall(tmp_path, ["Alpha Platform", "Bravo Migration", "Charlie Analytics",
                            "Delta Tall"], 12)
    for sel in ("t0", "t6", "t11"):
        _t, rows, lm = render(last, 80, 24, sel=sel)
        cut = [x for x in ("▲", "▼") if f"{x} " in rows[-1] and " more" in rows[-1]]
        assert cut and "▲ 3 above" in rows[-1], (sel, rows[-1])
    # the long name is the CUT band's, with bands folded on both sides
    longname = _tall(tmp_path, ["Alpha", "Zulu", "Customer Onboarding Revamp Program"], 12)
    longname.projects[1], longname.projects[2] = longname.projects[2], longname.projects[1]
    _t, rows, lm = render(longname, 80, 24, sel="t6")
    assert all(x in rows[-1] for x in ("▲ 1 above", "▲ ", " more", "▼ 1 below")), rows[-1]
    for w, h in ((80, 24), (80, 23), (118, 22)):
        _t, rows, lm = render(last, w, h, sel="t6")
        for tid, r in lm.items():
            assert rows[r + 1].strip() and not FOLD.match(rows[r + 1]), (w, h, tid)
    railed = _tall(tmp_path, ["Alpha", "Tall"], 9, done=6)
    # a rail title selected (rail rows sit every 2 rows, cards every 3): the cut
    # still starts on a card's first row
    for sel in [f"d{i}" for i in range(6)]:
        _t, rows, lm = render(railed, 118, 12, sel=sel)      # 5 body rows: d2, d4 round
        if sel not in lm:
            continue
        rule = next(i for i, r in enumerate(rows) if r.startswith("▐ Tall  "))
        first = rows[rule + 1].split("│")[0]
        assert not first.strip() or first.startswith("▊ =="), (sel, first)
    _t, rows, lm = render(railed, 118, 24, sel="t8")
    counts = [int(x) for x in re.findall(r"[▲▼] (\d+) more", rows[-1])]
    drawn = {t for t in lm if t.startswith("t")}
    assert sum(counts) + len(drawn) == 9, (rows[-1], sorted(drawn))
