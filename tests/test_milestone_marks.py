"""Every milestone mark draws through ONE seat (batch 2026-10-24-batch-01, HLR-2604).

MM-D1 (verdict D1 B): shape and colour say the class; state moves to text. The seat
`views.milestone_mark(task, board, today) -> (glyph, style, late_chip)` is the only
way a milestone mark is drawn: classed milestones wear their class's shape in its
colour, a late one's date renders `over` with an `▲Nd` chip (one channel — a
non-empty chip implies `over` at every site), a reached one is hollow with `✓` in
`reached`, and an unclassified one (no mark, or an id the directory does not hold)
keeps `◆` in `mut`. The 20 sites of LLR-2604.2 route through it; the exclusions
(title glyphs, project-span due marks, the slip notice, the month ruler's lateness)
stay byte-identical. `views.render_marks` — the `#` manager's pure frame — ships
here (the ARQ's A-1 fold) and is unwired until increment 003 (D-4's accepted cost).

Laws: TC-2604 (the seat's truth table + the site enumeration), AT-2603 (the state
shows in text — the styled-segment export oracle, never plain text), AT-2607 (an
unknown id is safe), TC-2606's render_marks arms. Boards are the round's synthetic
fixture (`tests/milestone_marks_fixture.py`); TODAY is pinned. RED on base_ref:
the seat does not exist (`AttributeError`).
"""
from __future__ import annotations

import io
import json
import tokenize
from datetime import date, timedelta
from pathlib import Path

import pytest
from rich.text import Text

import milestone_marks_fixture as fx
from taskboard import app as app_module
from taskboard import models, views
from taskboard.marks import MARKS_NAME, Directory, Mark
from taskboard.models import Board, Task

TODAY = fx.TODAY

VIOLET, CYAN, AMBER, PINK = (views.HEX[k] for k in ("violet", "cyan", "amber", "pink"))
MUT, OVER, REACHED = (views.HEX[k].lower() for k in ("mut", "over", "reached"))
HEX = {k: v.lower() for k, v in views.HEX.items()}


class _Today(date):
    @classmethod
    def today(cls):
        return fx.TODAY


@pytest.fixture
def home(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
    for mod in (app_module, models, views):
        monkeypatch.setattr(mod, "date", _Today)
    return tmp_path / ".taskboard"


def _open(home, last="client-a"):
    from taskboard.__main__ import open_app
    fx.build(home, last=last)
    return open_app(None)


def _task(key, title, phase, off, mark=None, project="pc"):
    return Task(title, project, phase, start_date=fx._d(off), due_date=fx._d(off),
                milestone=True, mark=mark, id=key)


def _seat_board(marks=True):
    """A small board whose marks dict holds the round's four classes."""
    tasks = [
        _task("late", "Late one", "Next", -3, "review"),
        _task("one", "One day late", "Next", -1, "review"),
        _task("done", "Done one", "Done", -4, "review"),
        _task("open", "Open one", "Next", 5, "delivery"),
        _task("today", "Due today", "Next", 0, "launch"),
        _task("plain", "Plain one", "Next", 6),
        _task("ghost", "Ghost one", "Next", 9, "no-such-class"),
    ]
    b = Board([], tasks, fx.Path("x.json"), phases=["Next", "Done"])
    b.marks = ({cid: Mark(cid, n, s, k) for cid, n, s, _h, k in fx.CLASSES}
               if marks else {})
    return b


# --------------------------------------------------------------------------- #
# TC-2604 — the seat's truth table (LLR-2604.1)
# --------------------------------------------------------------------------- #
def test_TC_2604_the_seats_truth_table():
    """classed+late → (shape, colour, `▲3d`); classed+reached → (hollow, colour,
    `✓`); classed+open → (shape, colour, ``); unclassified (no mark / unknown id)
    → (`◆`, `mut`, ``); unclassified+late → (`◆`, `mut`, `▲3d`); no directory →
    (`◆`, `mut`, ``); due today is not late; N = 1 → `▲1d`. Every cell of
    HLR-2604's boundary catalog. RED: the seat returns `◆` always."""
    b = _seat_board()
    seat = views.milestone_mark
    assert seat(b.task_by_id("late"), b, TODAY) == ("■", "violet", "▲3d")
    assert seat(b.task_by_id("one"), b, TODAY) == ("■", "violet", "▲1d")
    assert seat(b.task_by_id("done"), b, TODAY) == ("□", "violet", "✓")
    assert seat(b.task_by_id("open"), b, TODAY) == ("▲", "cyan", "")
    assert seat(b.task_by_id("today"), b, TODAY) == ("★", "pink", "")
    assert seat(b.task_by_id("plain"), b, TODAY) == ("◆", "mut", "")
    assert seat(b.task_by_id("ghost"), b, TODAY) == ("◆", "mut", "")   # unknown id
    plain = b.task_by_id("plain")
    plain.due_date = fx._d(-3)
    assert seat(plain, b, TODAY) == ("◆", "mut", "▲3d")                 # late, unclassed
    b.marks = {}
    assert seat(b.task_by_id("late"), b, TODAY) == ("◆", "mut", "▲3d")  # no directory


def test_TC_2604_a_nonempty_chip_implies_over_at_the_gantt_cells():
    """The one channel (LLR-2604.1): a non-empty late_chip implies the milestone's
    date renders `over` — the gantt cells derive the date label's tone from the
    seat, never from their own lateness math. RED: the label re-derives."""
    b = _seat_board()
    ax = views.gantt_axis(60, TODAY, TODAY - timedelta(days=5),
                          TODAY + timedelta(days=30), TODAY)
    late = views.gantt_milestone_cells(b.task_by_id("late"), b, ax, TODAY)
    row = "".join(g for g, _ in late)
    x = row.index("■")
    assert "Oct" in row[x + 1:x + 8]
    tones = {k for g, k in late if g != " "}
    assert "over" in tones and "violet" in tones
    done = views.gantt_milestone_cells(b.task_by_id("done"), b, ax, TODAY)
    drow, dtones = "".join(g for g, _ in done), {k for _, k in done}
    assert "□✓" in drow and "reached" in dtones
    open_ = views.gantt_milestone_cells(b.task_by_id("open"), b, ax, TODAY)
    orow, otones = "".join(g for g, _ in open_), {k for _, k in open_}
    assert "▲" in orow and "over" not in otones and "cyan" in otones


# --------------------------------------------------------------------------- #
# TC-2604 — the site enumeration: no milestone mark outside the seat (LLR-2604.2)
# --------------------------------------------------------------------------- #
VIEWS_SRC = Path(views.__file__)
APP_SRC = Path(app_module.__file__)

# The 20 sites (one entry per commission line-ref; the pairs share their seat):
# (refs, function that must route through the seat)
SEAT_SITES = [
    (":1107/:1113 lanes card marker", "_grid_task_row"),
    (":1677/:1689 focus title marker", "_title_row"),
    (":1800 bank edge", "_bank_edge_mark"),
    (":2037 kanban/focus axis glyph", "render_agenda"),
    (":2541 gantt title prefix", "_milestone_title"),
    (":2554 gantt milestone cells", "gantt_milestone_cells"),
    (":2643 one-date bars", "_gantt_bar"),
    (":2732 one-date echo", "gantt_echo"),
    (":3035 ruler milestones", "_gantt_frame"),
    (":3078 gantt row label", "_gantt_frame"),
    (":3613-3617 focus review label", "_focus_review"),
    (":5053-5099 band rule facts", "band_milestone_facts"),
    (":6537-6547 presentation field row", "_present_task_row"),
    (":7146 agenda row", "_agenda_row"),
    (":8433-8467 people task rows", "_task_rows"),
    (":2133 notice reached", "_notify_folded"),
    (":2172 notice milestone", "action_milestone_toggle"),
]

# The fold row's `▲N ◆` is a count of late milestones of every class — no single
# task — so it keeps the plain diamond by design (the band facts' `+N ◆` tails
# likewise, inside the band seat above).
COUNT_TAILS = [
    'f" · ▲{late_ms} ◆"',
    'f" ── +{more} ◆"',
    'f"+{more} ◆"',
]

# Exclusions: byte-identical in behaviour, and none of them calls the seat.
EXCLUSION_LINES = {
    'c("◆ TASKBOARD", "bright", bold=True)': 2,
    'title.append("◆ TASKBOARD"': 1,
    'c("◆ GANTT", "bright", bold=True)': 1,
    'c("◆ FOCUS", "bright", bold=True)': 3,
    'c("◆ CHAIN MAP", "bright", bold=True)': 1,
    'c("◆ PRESENT", "bright", bold=True)': 2,
    'head.append("◆ " + PEOPLE_TITLE': 1,
    'Text("◆ " + PEOPLE_TITLE': 1,
    'c("◆ GANTT · LINK", "bright", bold=True)': 1,
    'left = "◆ ALL BOARDS"': 1,
    'cells[c1] = ("◆", project.color)': 1,            # _gantt_span's due
    'marks[ax.cell(pd)] = ("◆", sel_p.color)': 1,     # the gantt ruler's project due
    'tag = "◆ dates · "': 1,
    'c("◆", sel_p.color)': 1,                          # the mlabel's due
    'marks[ax.cell(pd)] = ("◆", proj.color)': 2,      # the presentation rulers' dues
    'segs.append(f"{pn} +{over}d past ◆")': 1,        # app: the slip notice
    'cells[x] = ("◆", tone)': 1,                       # a one-date TASK, not a milestone
    'cells[x] = ("◆", "reached")': 1,                  # a one-date DONE task (2026-10-26)
    'if any(gl == "◆"': 1,                             # the span row's drawn-set probe
}

# Lines the census allows although they carry a literal diamond: seat internals,
# width bookkeeping, the manager frame's `(no class)` row, and the `?`/legend
# help text that NAMES the mark (drawn in help seats, never as a live mark).
ALLOWED_LINES = [
    'ms = "◆" if t.milestone else ""',
    'ms = "◆" if task.milestone else ""',
    'return c("◆", hue)',                                # _bank_edge_mark's project fallback
    'HOLLOW = {"◆": "◇"',
    'MARK_GLYPHS = frozenset(["◆"',
    'glyph = cls.shape if cls is not None else "◆"',
    'glyph = "◆"',
    '" ", "gap")',
    'plain.append("        ◆", style=HEX["mut"])',
    '("◆", "mut", "milestone", "milestone")',
    '("◆✓", "reached", "reached", "reached")',
    '"committed due"',
    "◆ on a band rule: a milestone, never a card",
    "at ◆ (its due date). then: tab layout.",
    "◆ = the project's due date on the curve",
    "─ span · ● progress · ◆ due",
    "◆ title = a milestone · ◆✓ reached · M",
    "▎ platform ████▒░◆ 12d",
    "the curve is the load; the air before ◆ is what does not fit",
    "◂───╎──●────◆··",
    '"the project\'s own due date"',
    '"a milestone: one date, no bar"',
    '"the project\'s committed due date"',
    '"a milestone reached"',
    '"a milestone on its project\'s band rule"',
    # increment 004 (LLR-2607.2): the `?` help NAMES the classes and the plain
    # mark — drawn in help seats, never as a live mark (the strips and the
    # details line carry the class entries dynamically, with no literal ◆)
    '◆ = no class · # manage the classes,',
] + COUNT_TAILS


def _function_body(src: str, name: str) -> str | None:
    lines = src.splitlines()
    start = next((i for i, l in enumerate(lines)
                  if l.lstrip().startswith(f"def {name}(")), None)
    if start is None:
        return None
    indent = len(lines[start]) - len(lines[start].lstrip())
    body = []
    for line in lines[start + 1:]:
        stripped = line.strip()
        if stripped:
            ind = len(line) - len(line.lstrip())
            if (ind < indent
                    or (ind == indent and stripped.startswith(("def ", "class ")))
                    or (indent == 0 and ind == 0)):
                break
        body.append(line)
    return "\n".join(body)


def _diamond_code_lines(path: Path) -> list[tuple[int, str]]:
    """Every code line carrying a literal ◆ (docstrings and # comments out)."""
    src = path.read_text(encoding="utf-8")
    spans = [(t.start[0], t.end[0]) for t in tokenize.generate_tokens(
        io.StringIO(src).readline)
        if t.type == tokenize.STRING and t.end[0] > t.start[0]]
    out = []
    for n, line in enumerate(src.splitlines(), 1):
        if "◆" not in line or line.lstrip().startswith("#"):
            continue
        if any(a <= n <= b for a, b in spans):
            continue
        out.append((n, line.strip()))
    return out


def test_TC_2604_the_sites_enumeration_every_milestone_mark_routes_through_the_seat():
    """The enumeration guard (LLR-2604.2): the 20 sites take their (glyph, style,
    chip) from `milestone_mark` — the seat's call sits in each site's function —
    and every literal `◆` left in views.py/app.py is one of the declared
    exclusions, count tails, seat internals or `?`/legend help text. A NEW
    milestone site that draws outside the seat, or an exclusion edited to call
    the seat, fails this census. RED: a site edited back to `c("◆", …)`."""
    src = VIEWS_SRC.read_text(encoding="utf-8")
    app_src = APP_SRC.read_text(encoding="utf-8")
    for refs, fn in SEAT_SITES:
        body = _function_body(src, fn) or _function_body(app_src, fn)
        assert body is not None and "milestone_mark(" in body, \
            f"{refs}: {fn} does not route through the seat"
    # the fold row counts late milestones of every class: the plain diamond stays,
    # and it never calls the seat
    fold = _function_body(src, "_fold_row")
    assert "milestone_mark(" not in fold and COUNT_TAILS[0] in fold
    # the month ruler shows no lateness (the accepted cost): no seat at all
    month = _function_body(src, "gantt_month_row")
    assert "milestone_mark(" not in month
    # exclusions keep their exact line counts and never mention the seat
    for anchor, n in EXCLUSION_LINES.items():
        assert src.count(anchor) + app_src.count(anchor) == n, \
            f"exclusion moved or multiplied: {anchor!r}"
        assert "milestone_mark" not in anchor
    for anchor in ("milestone_tone(",):
        body = _function_body(app_src, "_cascade_toast")
        assert anchor not in body
    # the sweep: every literal-diamond code line is a declared one
    declared = list(EXCLUSION_LINES) + ALLOWED_LINES
    for path in (VIEWS_SRC, APP_SRC):
        for n, line in _diamond_code_lines(path):
            assert any(a in line for a in declared), \
                f"{path.name}:{n} draws ◆ outside the census: {line!r} — " \
                "route it through views.milestone_mark or declare it here"


# --------------------------------------------------------------------------- #
# TC-2606 arms — render_marks, the manager's pure frame (LLR-2606.3, ships in 002)
# --------------------------------------------------------------------------- #
def _frame(w=76, h=14, sel=2, marks=True, counts=None):
    d = Directory(fx.Path("marks.json"),
                  [Mark(cid, n, s, k) for cid, n, s, _h, k in fx.CLASSES])
    if not marks:
        d = Directory(fx.Path("marks.json"))
    if counts is None and marks:
        counts = {cid: (1 + j, 3 + j) for j, (cid, *_r) in enumerate(fx.CLASSES)}
    return views.render_marks(d, sel, w, h, counts)


def _rows(t: Text) -> list[Text]:
    return t.split("\n")


def test_TC_2606_render_marks_every_row_is_exactly_w_cells():
    """LLR-2606.3: at 76/60/40 every row is exactly `w` cells of Text pieces.
    RED: the pad/cut to `w` dropped."""
    for w in (76, 60, 40):
        for line in _rows(_frame(w=w)):
            assert line.cell_len == w, (w, line.cell_len, line.plain)


def test_TC_2606_render_marks_the_frame_names_every_class_and_the_plain_row():
    """One row per class: shape, name, counts; the chosen row `▶` shaded; the
    `◆ (no class)` row for the plain milestone; the key line naming the five
    keys (no `↵ only this`, no `d` — out of scope). RED: a row's pieces dropped."""
    t = _frame()
    plain = t.plain
    for cid, n, s, _h, k in fx.CLASSES:
        assert n in plain and s in plain
    assert "▶ [x] ■ Review" in plain and "#1d2a3a" in str(t.spans)
    assert "◆ (no class)" in plain and "the plain milestone" in plain
    assert "1 open 3 in all" in plain and "2 open 4 in all" in plain
    keys = _rows(t)[-1].plain
    assert keys.startswith("↑↓ move   ␣ hide/show   n new   e edit   esc close")
    assert "only this" not in keys and "delete" not in keys


def _span_text(line: Text, sp) -> str:
    return line.plain[sp.start:sp.end]


def test_TC_2606_render_marks_a_hidden_class_is_dimmed_with_what_hiding_means():
    """A hidden class: dimmed shape/name, `[ ]`, and `hidden: gantt + present` in
    amber beside it. RED: the dim or the note dropped."""
    d = Directory(fx.Path("marks.json"),
                  [Mark("review", "Review", "■", "violet", hidden=True),
                   Mark("payment", "Payment", "⬢", "amber")])
    t = views.render_marks(d, 0, 76, 8, {"review": (2, 5), "payment": (1, 2)})
    line = next(r for r in _rows(t) if "Review" in r.plain)
    assert "[ ]" in line.plain and "hidden: gantt + present" in line.plain
    shape = next(sp for sp in line.spans if _span_text(line, sp) == "■")
    assert str(shape.style) == views.HEX["dim"]


def test_TC_2606_render_marks_narrow_counts_drop_before_the_names():
    """Under width pressure the counts give way first; the names stay whole.
    (At 40 cells the round's short rows still keep both — the 40-cell width law
    is the exact-rows test above.)"""
    t = _frame(w=28)
    review = next(r for r in _rows(t) if "Review" in r.plain)
    assert "open" not in review.plain and "Review" in review.plain


def test_TC_2606_render_marks_an_empty_directory_says_so_and_a_markup_name_is_literal():
    """The empty directory: one `No classes yet.` line and the hint; a
    markup-looking class name prints as typed, never parsed (C-17)."""
    t = _frame(marks=False)
    assert "No classes yet." in t.plain and "n adds the first class." in t.plain
    d = Directory(fx.Path("marks.json"), [Mark("x", "[b]x[/b]", "★", "pink")])
    t = views.render_marks(d, 0, 60, 8, {})
    line = next(r for r in _rows(t) if "[b]x[/b]" in r.plain)
    name = next(sp for sp in line.spans if "[b]x[/b]" in _span_text(line, sp))
    assert str(name.style) == views.HEX["ink"] and "bold" not in str(name.style)


# --------------------------------------------------------------------------- #
# The painted-frame helpers (Textual's styled-segment export — the tone oracle)
# --------------------------------------------------------------------------- #
def _painted(app) -> list[list[tuple[str, str | None]]]:
    strips = app.screen._compositor.render_strips(app.screen.size)
    rows = []
    for s in strips:
        cells = []
        for seg in s:
            hx = (seg.style.color.triplet.hex.lower()
                  if seg.style and seg.style.color and seg.style.color.triplet else None)
            cells += [(ch, hx) for ch in seg.text]
        rows.append(cells)
    return rows


def _text(rows) -> list[str]:
    return ["".join(ch for ch, _ in r) for r in rows]


def _prow(rows, needle):
    for r in _painted_row_iter(rows, needle):
        return r
    raise AssertionError(f"{needle!r} not painted")


def _painted_row_iter(rows, needle):
    for r in rows:
        if needle in "".join(ch for ch, _ in r):
            yield r


def _hexes(row, needle) -> list[str | None]:
    """The hexes under the first occurrence of `needle` in a painted row."""
    text = "".join(ch for ch, _ in row)
    i = text.index(needle)
    return [row[i + k][1] for k in range(len(needle))]


# --------------------------------------------------------------------------- #
# AT-2603 — the state shows in text (HLR-2604, the styled-segment export oracle)
# --------------------------------------------------------------------------- #
async def test_AT_2603_the_state_shows_in_text(home):
    """On the round's boards at 118×30 (and the gantt at 80×24): a late classed
    milestone shows its class glyph in the class colour with its date in `over`
    and `▲2d` beside it; a reached one the hollow glyph with `✓` in `reached`;
    an unclassified one `◆` in `mut` — the same three in the kanban band rule,
    the gantt cells and label, the presentation field row, the agenda row, the
    people view's rows and the two notices. Tone claims are asserted on the
    styled-segment export, never on plain text."""
    fx.build(home, last="client-a")
    # a person who is mentioned by a classed milestone, for the people view —
    # written before the app loads its directories
    b = Board.load(fx.board_path(home, "client-a"))
    b.task_by_id("tc6").notes = "sign-off with @ana.ruiz"
    b.save()
    (home / "people.json").write_text(json.dumps({"version": 1, "people": [
        {"id": "ana.ruiz", "name": "Ana Ruiz", "role": "PM", "note": ""}]}),
        encoding="utf-8")
    from taskboard.__main__ import open_app
    app = open_app(None)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        await pilot.press("escape")                  # the home
        # ---- the kanban band rule (4) ----
        app.selected_task_id = "tc5"                 # an Eval harness card
        await pilot.press("4")
        await pilot.pause()
        rows = _painted(app)
        rule = _prow(rows, "▐ Eval harness")
        text = "".join(ch for ch, _ in rule)
        i = text.rindex("■", 0, text.index("Rubric sign"))   # late, classed review ■
        assert rule[i] == ("■", HEX["violet"])               # the class glyph in its colour
        assert OVER in (_h for _h in _hexes(rule, "Oct 18"))
        assert OVER in (_h for _h in _hexes(rule, "2d late"))
        # the reached arm lives on the Ingest & index band (Catalog parsed):
        # walk the selection onto its card so the band stays drawn
        app.selected_task_id = "tc3"
        app.refresh_view()
        await pilot.pause()
        rows = _painted(app)
        rule = _prow(rows, "▐ Ingest & index")
        text = "".join(ch for ch, _ in rule)
        i = text.rindex("△", 0, text.index("Catalog"))       # reached, classed delivery ▲
        assert rule[i] == ("△", HEX["cyan"])                 # the hollow twin in its colour
        assert rule[text.index("✓", i)][1] == REACHED
        # ---- the gantt cells and label (3) ----
        app.selected_task_id = "tc6"
        await pilot.press("3")
        await pilot.pause()
        rows = _painted(app)
        grow = _prow(rows, "Rubric sign-off")
        gtext = "".join(ch for ch, _ in grow)
        gi = gtext.index("■")
        assert grow[gi][1] == HEX["violet"]
        assert OVER in (_h for _h in _hexes(grow, "Oct 18"))
        assert gtext.rstrip().endswith("▲2d")
        assert OVER in (_h for _h in _hexes(grow, "▲2d"))
        prow_ = _prow(rows, "Handover call")          # unclassified ◆ in mut
        ptext = "".join(ch for ch, _ in prow_)
        assert prow_[ptext.index("◆")][1] == MUT
        # the row label's mark wears the class colour too
        lrow = _prow(rows, "Pilot launch")
        ltext = "".join(ch for ch, _ in lrow)
        assert lrow[ltext.index("★")][1] == HEX["pink"]
        # ---- the presentation field row (R) ----
        app.selected_task_id = "tc6"
        await pilot.press("R")
        await pilot.pause()
        rows = _painted(app)
        prrow = _prow(rows, "Rubric sign-off")
        prtext = "".join(ch for ch, _ in prrow)
        assert prrow[prtext.index("■")][1] == HEX["violet"]
        await pilot.press("escape")
        await pilot.pause()
        # ---- the agenda row (A): the mark before the title ----
        await pilot.press("A")
        await pilot.pause()
        rows = _painted(app)
        arow = _prow(rows, "Steering go/no-go")      # the TODAY bucket, classed review ■
        atext = "".join(ch for ch, _ in arow)
        assert arow[atext.index("■")][1] == HEX["violet"]
        await pilot.press("left")                    # the LATE bucket
        await pilot.pause()
        rows = _painted(app)
        arow = _prow(rows, "Rubric sign-off")
        atext = "".join(ch for ch, _ in arow)
        assert arow[atext.index("■")][1] == HEX["violet"]
        assert OVER in (_h for _h in _hexes(arow, "▲2d"))
        for _ in range(5):                           # LATE → on to Sat 24: the ⬢ arm
            await pilot.press("right")
        await pilot.pause()
        rows = _painted(app)
        drow = _prow(rows, "Deposit back from landlord")
        dtext = "".join(ch for ch, _ in drow)
        assert drow[dtext.index("⬢")][1] == HEX["amber"]
        await pilot.press("right")                   # Sun 25: a peeked board's class
        await pilot.pause()
        rows = _painted(app)
        krow = _prow(rows, "Module 4 publish")
        ktext = "".join(ch for ch, _ in krow)
        assert krow[ktext.index("★")][1] == HEX["pink"]   # the directory rides the peek
        await pilot.press("escape")
        await pilot.pause()
        # ---- the people view's rows (@, tasks pane) ----
        await pilot.press("at", "enter")
        await pilot.pause()
        rows = _painted(app)
        wrow = _prow(rows, "Rubric sign-off")
        wtext = "".join(ch for ch, _ in wrow)
        assert wrow[wtext.index("■")][1] == HEX["violet"]
        await pilot.press("escape")
        await pilot.pause()
        # ---- the two notices through the seat ----
        app.clear_notifications()
        app.selected_task_id = "tc2"                 # due yesterday, not a milestone
        await pilot.press("M")
        await pilot.pause()
        said = [str(n.message) for n in app._notifications]
        assert any("Chunking experiments is a milestone · ◆ Oct 19"
                   in s and "▲1d" in s for s in said), said
        app.clear_notifications()
        app.selected_task_id = "tc9"                 # classed review ■, due today
        for _ in range(3):                           # Next → Doing → Review → Done
            await pilot.press("right_square_bracket")
            await pilot.pause()
        said = [str(n.message) for n in app._notifications]
        assert any("Steering go/no-go reached · □✓" in s for s in said), said
    # ---- the gantt at 80×24: the same states ----
    app2 = _open(home)                           # the same home, a fresh app
    async with app2.run_test(size=(80, 24)) as pilot:
        await pilot.pause()
        await pilot.press("escape")
        app2.selected_task_id = "tc6"
        await pilot.press("3")
        await pilot.pause()
        rows = _painted(app2)
        grow = _prow(rows, "Rubric sign-off")
        gtext = "".join(ch for ch, _ in grow)
        assert grow[gtext.index("■")][1] == HEX["violet"]
        assert OVER in (_h for _h in _hexes(grow, "Oct 18"))
        drow = _prow(rows, "Handover call")
        dtext = "".join(ch for ch, _ in drow)
        assert drow[dtext.index("◆")][1] == MUT


# --------------------------------------------------------------------------- #
# AT-2607 — an unknown id is safe (HLR-2602, through the app's surface)
# --------------------------------------------------------------------------- #
async def test_AT_2607_an_unknown_id_is_safe(home):
    """A board file with a task whose `mark` names a class no directory holds →
    opened, drawn unclassified (`◇` in `mut` — reached, so the hollow twin),
    edited and saved → the file still holds the id. RED: a save drops the id."""
    from taskboard.__main__ import open_app
    fx.build(home, last="client-a")
    path = fx.board_path(home, "client-a")
    data = json.loads(path.read_text(encoding="utf-8"))
    data["tasks"][0]["mark"] = "zzz-unknown"
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    app = open_app(None)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        await pilot.press("escape", "3")
        await pilot.pause()
        rows = _painted(app)
        row = _prow(rows, "Catalog parsed")
        text = "".join(ch for ch, _ in row)
        i = text.index("◇")                          # reached + unknown id: unclassified
        assert row[i][1] == MUT
        j = text.index("✓")                          # the reached chip in the field
        assert row[j] == ("✓", REACHED)
        app.selected_task_id = "tc1"
        await pilot.press("e")                       # the editor, a no-op edit, save
        await pilot.pause()
        await pilot.press("alt+s")
        await pilot.pause()
    raw = path.read_text(encoding="utf-8")
    assert '"mark": "zzz-unknown"' in raw            # the id kept, byte-for-byte
    data = json.loads(raw)
    assert data["tasks"][0]["mark"] == "zzz-unknown"


# --------------------------------------------------------------------------- #
# TC-2602 arm — the seat's view of the field (round-trip lives in 001's file)
# --------------------------------------------------------------------------- #
def test_TC_2602_a_mark_set_on_a_non_milestone_is_kept_and_drawn_nowhere(home):
    """The boundary the contract names: the field is meaningful only on a
    milestone — a task carrying a mark draws no mark anywhere (its bar knows
    nothing of the class); the field round trip itself is TC-2602 in
    tests/test_marks_directory.py (increment 001)."""
    b = _seat_board()
    t = b.task_by_id("plain")
    t.milestone = False
    t.mark = "review"
    t.start_date = fx._d(0)                  # a ranged task: a bar, one date = ◆
    t.due_date = fx._d(6)                    # would draw the diamond (not a mark)
    glyph, style, chip = views.milestone_mark(t, b, TODAY)
    assert (glyph, style, chip) == ("■", "violet", "")   # the seat is pure: it reads it
    ax = views.gantt_axis(60, TODAY, TODAY - timedelta(days=5),
                          TODAY + timedelta(days=30), TODAY)
    cells = views._gantt_bar(t, b, ax, set(), 0)
    assert all(g not in views.MARK_GLYPHS for g, _ in cells)


# --------------------------------------------------------------------------- #
# AT-2606 — /#pay filters to that class (HLR-2608, through the app's surface)
# --------------------------------------------------------------------------- #
async def test_AT_2606_hash_pay_filters_to_that_class(home):
    """`/` `#pay` `enter` in the kanban and the gantt keeps exactly the Payment
    milestones, the bar reading `/ <shape> <Name>  milestones of this class
    only` with the tally; `/#zzz` keeps nothing and names nothing; `/pay`
    (no `#`) filters as text, unchanged. RED: the class rule falling through
    to the text rules, or the bar omitting the class."""
    app = _open(home)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        await pilot.press("escape")                  # the home
        await pilot.press("4")                       # the kanban
        await pilot.pause()
        await pilot.press("slash")
        for ch in "#pay":
            await pilot.press(ch)
        await pilot.press("enter")
        await pilot.pause()
        rows = _painted(app)
        text = _text(rows)
        bar = "".join(ch for ch, _ in _prow(rows, "milestones of this class only"))
        assert "/ ⬢ Payment  milestones of this class only" in bar, bar
        assert "tasks" in bar and "esc clears" in bar
        assert set(_hexes(_prow(rows, "milestones of this class only"),
                          "⬢ Payment")) == {HEX["amber"]}
        for title in ("Kickoff invoice pa", "Milestone 2 invoice", "Final payment"):
            assert any(title in ln for ln in text), title
        for other in ("Rubric sign-off", "Index v1 delivered", "Pilot launch",
                      "Steering go/no-go", "Catalog parsed"):
            assert not any(other in ln for ln in text), other
        # the gantt under the same query
        await pilot.press("3")
        await pilot.pause()
        rows = _painted(app)
        text = _text(rows)
        assert any("Milestone 2 invoice" in ln for ln in text)
        for other in ("Rubric sign-off", "Index v1 delivered", "Pilot launch"):
            assert not any(other in ln for ln in text), other
        bar = "".join(ch for ch, _ in _prow(rows, "milestones of this class only"))
        assert "⬢ Payment" in bar and "milestones of this class only" in bar
        # esc clears; a query naming no class keeps nothing, names nothing
        await pilot.press("escape")
        await pilot.pause()
        await pilot.press("slash")
        for ch in "#zzz":
            await pilot.press(ch)
        await pilot.press("enter")
        await pilot.pause()
        rows = _painted(app)
        text = _text(rows)
        bar = "".join(ch for ch, _ in _prow(rows, "#zzz"))
        assert "milestones of this class only" not in bar, bar
        assert "/ #zzz" in bar and "0/" in bar
        for title in ("Rubric sign-off", "Milestone 2 invoice", "Kickoff invoice paid"):
            assert not any(title in ln for ln in text), title
        # no `#`: plain text, exactly as before
        await pilot.press("escape")
        await pilot.pause()
        await pilot.press("slash")
        for ch in "pay":
            await pilot.press(ch)
        await pilot.press("enter")
        await pilot.pause()
        rows = _painted(app)
        text = _text(rows)
        bar = "".join(ch for ch, _ in _prow(rows, "pay▌"))
        assert "/ pay" in bar and "milestones of this class only" not in bar, bar
        assert any("Final payment" in ln for ln in text)
        assert not any("Milestone 2 invoice" in ln for ln in text)


# --------------------------------------------------------------------------- #
# TC-2608 — the class query's mechanism (LLR-2608.2, layer 0)
# --------------------------------------------------------------------------- #
def test_TC_2608_the_class_query_keeps_exactly_that_class_milestones():
    """`matches` wired: `#pay` (prefix, any case) keeps exactly the milestones
    bearing the resolved class — open or done, never a non-milestone; a name
    no class holds keeps nothing; a lone `#` resolves like the round's
    `find_class("")`: the first class in the sorted directory. RED: the class
    rule falling through to the text rules."""
    b = _seat_board()
    pay = b.marks["payment"]
    matches = views.matches
    assert matches(_task("x", "Pay day", "Next", 3, "payment"), b, "#pay") == "class"
    assert matches(_task("x", "Pay day", "Done", -2, "payment"), b, "#pay") == "class"
    assert matches(b.task_by_id("open"), b, "#pay") is None          # delivery
    plain = _task("x", "payment-ish", "Next", 3)                     # no mark
    assert matches(plain, b, "#pay") is None
    plain.milestone = False                                          # a mark, not a milestone
    assert matches(plain, b, "#pay") is None
    assert matches(_task("x", "x", "Next", 3, "payment"), b, "#pa") == "class"
    assert matches(_task("x", "x", "Next", 3, "payment"), b, "#PaY") == "class"
    assert matches(_task("x", "x", "Next", 3, "payment"), b, "#zzz") is None
    assert pay.name == "Payment" and matches(b.task_by_id("open"), b, "#") == "class"
    assert matches(b.task_by_id("late"), b, "#") is None             # "" -> delivery


def test_TC_2608_the_bar_names_the_class_and_nothing_when_no_class_holds():
    """`filter_bar` wired: the resolved class named in its colour, bold; an
    unresolved `#cls` — or no directory at all — keeps the plain bar. RED:
    the bar omitting the class, or inventing one for `#zzz`."""
    b = _seat_board()
    bar = views.filter_bar("#pay", 2, 9, 80, marks=b.marks)
    row = views._strip(bar[0])
    assert row.startswith("/ ⬢ Payment  milestones of this class only")
    assert "2/9 tasks" in row and "esc clears" in row
    assert views.HEX["amber"] in bar[0] and f"b {views.HEX['amber']}" in bar[0]
    for q in ("#zzz", "#"):
        plain = views._strip(views.filter_bar(q, 0, 9, 80, marks=b.marks)[0])
        assert "Payment" not in plain
    assert views._strip(views.filter_bar("#zzz", 0, 9, 80, marks=b.marks)[0]) \
        .startswith("/ #zzz")
    # a lone `#` resolves like the round's find_class(""): the first class
    # of the sorted directory is named (the round's rule, proto.py:500-503)
    lone = views._strip(views.filter_bar("#", 0, 9, 80, marks=b.marks)[0])
    assert lone.startswith("/ ▲ Delivery  milestones of this class only")
    bare = views._strip(views.filter_bar("#pay", 0, 9, 80)[0])       # no directory
    assert bare.startswith("/ #pay") and "milestones" not in bare


def test_TC_2608_the_class_query_lights_no_text_in_the_overlay():
    """The overlay reverse-lits a text query's hits only: a `#cls` query has
    none (the bar names the class instead). RED: the overlay lighting the
    class name, or lighting nothing for a text query."""
    b = _seat_board()
    from taskboard.views import _apply_search_overlay
    from rich.text import Text as _Text
    text = _Text("Payment milestone here · another task")
    lit = _apply_search_overlay(text, "pay", 1, 2, 80, marks=b.marks)
    assert any("reverse" in str(sp.style) for sp in lit.spans)
    dark = _apply_search_overlay(text, "#pay", 1, 2, 80, marks=b.marks)
    assert not any("reverse" in str(sp.style) for sp in dark.spans)
    assert "milestones of this class only" in dark.plain
