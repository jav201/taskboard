"""Width is measured in CELLS, not in characters.

WHY THIS FILE EXISTS: every view here spends a width it was handed — `fit` pads
to it, `_pad` closes a row out to it, the field allocator divides it. All of that
arithmetic used `len()`, which counts CODEPOINTS. A terminal does not draw
codepoints, it draws cells, and plenty of characters are not one cell wide: an
emoji is 2, CJK is 2, a combining mark is 0. Measured before this file existed, a
single task titled `arreglar :bug: parser` made its own row **93 cells** in a
96-cell view, and a literal `🐛` made it **97** — the row stopped agreeing with
every other row on the screen, which is the one thing a column layout may never
do.

THE LAW: a rendered row is exactly as wide as the width the view was given, and
it stays exactly that wide no matter what a human typed into a task. The tests
below measure with `rich.cells.cell_len` — the same function the terminal's own
renderer agrees with — because measuring the fix with the broken ruler (`len`)
would pass on the very input that breaks the screen.

These are written against the VIEWS, not against `fit`/`clip`, on purpose: a unit
test of the helpers would not have caught a caller that does its own arithmetic,
and the bug lived in the callers too.
"""

from datetime import date, timedelta
from pathlib import Path

import pytest
from rich.cells import cell_len

from taskboard.models import Board, Project, Task
from taskboard.views import clip, fit, render_view

# These boards are never saved; the path exists only because Board requires
# one. Naming it makes that explicit instead of leaving a repo-relative
# landmine for the first test that does call save().
_UNWRITTEN = Path("__never_written__.json")

PHASES = ["Backlog", "Doing", "Review", "Done"]
VIEWS = ["swimlanes", "agenda", "gantt", "kanban"]

# Every one of these renders to something that is NOT len()-wide. The names say
# what each is for, so a failure names the class of character that broke it.
WIDE = "\U0001F41B"            # bug emoji, 2 cells, 1 codepoint
CJK = "日本語"     # 3 codepoints, 6 cells
ZERO = "é"               # e + combining acute: 2 codepoints, 1 cell
SHORTCODE = ":bug:"            # 5 codepoints, renders as 2 cells under emoji=True

HOSTILE = {
    "ascii-control": "arreglar el parser",
    "emoji-ancho-2": f"arreglar {WIDE} parser",
    "emoji-al-final": f"arreglar parser {WIDE}",
    "muchos-emoji": WIDE * 12,
    "cjk": f"revisar {CJK} ahora",
    "combinante": f"caf{ZERO} con leche",
    "shortcode": f"arreglar {SHORTCODE} parser",
    "mezcla": f"{WIDE}{CJK} fix {SHORTCODE} {ZERO}",
    "muy-largo-y-ancho": (WIDE + "x") * 60,
}


def board_titled(title: str) -> Board:
    """One project, one task per phase, all carrying the same hostile title so
    the character under test reaches every view's row builders."""
    p = Project(name=f"Proj {title[:6]}", color="cyan")
    today = date.today()
    tasks = [
        Task(title=title, project_id=p.id, phase=phase,
             start_date=str(today - timedelta(days=10)),
             due_date=str(today + timedelta(days=k - 1)))
        for k, phase in enumerate(PHASES)
    ]
    return Board([p], tasks, _UNWRITTEN, phases=PHASES)


@pytest.mark.parametrize("name,title", sorted(HOSTILE.items()))
@pytest.mark.parametrize("mode", VIEWS)
@pytest.mark.parametrize("width", [68, 96, 120])
def test_every_row_is_exactly_the_width_it_was_given(mode, name, title, width):
    """The invariant. A row that is 3 cells short leans the whole column."""
    text = render_view(mode, board_titled(title), False, None,
                       width=width, height=24, line_map={},
                       presentation="grouped", tick=0)
    bad = [(i, cell_len(line)) for i, line in enumerate(text.plain.split("\n"))
           if line.strip() and cell_len(line) != width]
    assert not bad, (
        f"{mode} @ {width} with {name!r}: rows {bad[:4]} are not {width} cells")


@pytest.mark.parametrize("name,title", sorted(HOSTILE.items()))
def test_the_project_name_is_hostile_too(name, title):
    """A project name reaches a different set of builders than a task title
    (lane labels, the kanban group heads), so it gets its own pass."""
    p = Project(name=title, color="pink")
    b = Board([p], [Task(title="ordinary", project_id=p.id, phase="Doing")],
              _UNWRITTEN, phases=PHASES)
    for mode in VIEWS:
        text = render_view(mode, b, False, None, width=96, height=24,
                           line_map={}, presentation="grouped", tick=0)
        bad = [cell_len(l) for l in text.plain.split("\n")
               if l.strip() and cell_len(l) != 96]
        assert not bad, f"{mode} with project name {name!r}: widths {bad[:4]}"


# --------------------------------------------------------------------------- #
# the helpers, measured with the ruler the terminal uses
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("s", list(HOSTILE.values()))
@pytest.mark.parametrize("w", [1, 2, 3, 8, 20])
def test_fit_returns_exactly_w_cells(s, w):
    assert cell_len(fit(s, w)) == w, f"fit({s!r}, {w}) mis-sized"


@pytest.mark.parametrize("align", ["left", "right", "center"])
def test_fit_pads_to_w_cells_in_every_alignment(align):
    assert cell_len(fit(f"a{WIDE}b", 10, align)) == 10


@pytest.mark.parametrize("s", list(HOSTILE.values()))
@pytest.mark.parametrize("w", [1, 2, 5, 12, 40])
def test_clip_never_exceeds_w_cells(s, w):
    """clip may come back SHORTER (a 2-cell glyph cannot half-fit a 1-cell gap)
    but it may never come back wider, which is what overflows a row."""
    assert cell_len(clip(s, w)) <= w, f"clip({s!r}, {w}) overflowed"


def test_clip_does_not_split_a_wide_glyph():
    """Cutting between the two cells of one glyph is how a row gains a stray
    half-character; the cut has to land on a glyph boundary."""
    out = clip(WIDE * 5, 5)
    assert cell_len(out) <= 5
    assert WIDE not in out or out.count(WIDE) * 2 <= 5 + 1
    # whatever came back must still be measurable and drawable as itself
    assert cell_len(out) == sum(cell_len(ch) for ch in out)


# --------------------------------------------------------------------------- #
# why the substitution had to go
# --------------------------------------------------------------------------- #
def test_a_shortcode_is_drawn_as_itself_not_as_a_glyph():
    """THE LAW THIS CLOSES: rich's emoji substitution runs INSIDE
    `Text.from_markup`, downstream of every width the row builders computed. A
    title holding `:bug:` measured 5 cells and drew 2, so its row came out 3
    short — and no correct ruler can reach that, because at measuring time the
    string genuinely IS 5 cells. So `to_text` renders with `emoji=False` and the
    text is drawn as written. Emoji are typed as the glyph itself, which `vis()`
    can measure; that is what the picker inserts.

    If someone re-enables the substitution to "support :shortcodes:", this test
    goes red and the row-width invariant above goes red with it."""
    b = board_titled("arreglar :bug: parser")
    text = render_view("kanban", b, False, None, width=96, height=24,
                       line_map={}, presentation="grouped", tick=0)
    assert ":bug:" in text.plain, "the shortcode was substituted behind the width math"
    assert "\U0001F41B" not in text.plain
    assert all(cell_len(l) == 96 for l in text.plain.split("\n") if l.strip())


def test_a_literal_emoji_survives_and_is_measured():
    """The other half: the glyph the picker inserts must reach the screen."""
    b = board_titled(f"arreglar {WIDE} parser")
    text = render_view("kanban", b, False, None, width=96, height=24,
                       line_map={}, presentation="grouped", tick=0)
    assert WIDE in text.plain, "the emoji the user chose did not reach the screen"
    assert all(cell_len(l) == 96 for l in text.plain.split("\n") if l.strip())


# --------------------------------------------------------------------------- #
# the card aging token (batch-04 R-06, HLR-006/LLR-006.1 — TC-009)
# --------------------------------------------------------------------------- #
def _aging_cell_board() -> Board:
    p = Project("Proj", "cyan")
    return Board([p], [], _UNWRITTEN, phases=PHASES)


def _stamped(title, phase, stamp_days, project, archived=False):
    return Task(title=title, project_id=project.id, phase=phase,
                phase_changed=None if stamp_days is None
                else str(date.today() - timedelta(days=stamp_days)),
                archived=archived)


def test_card_cell_aging_token_follows_the_stamp_and_never_lies():
    """TC-009 (HLR-006/LLR-006.1): the `·Nd` aging token — N =
    `days_in_phase(task, today)` off `phase_changed` — rides the card's
    right-indicator budget INSIDE the exact-`wc` contract, in the quiet dim
    house. Pins: stamped today → `·0d` (zero is a KNOWN age); stamped N days
    ago → `·Nd`, N recomputed by the seat's own rule; None stamp → NO token
    (unknown is not zero — a pre-field board must not light up as all-fresh);
    done task → NO token (done work rests — its age is not WIP information);
    the tone is dim, never a judging hue. RED counterfactuals (each limb
    names its mutation): None rendered as 0 → the unstamped card paints `·0d`
    → the unstamped limb red; the done-suppression dropped → the done card
    paints `·9d` → the done limb red (EXECUTED, see increment-008 §4); age
    read from `start_date`/`due_date` instead of `phase_changed` → the
    recomputed-N limb red."""
    from rich.text import Text

    from taskboard.models import days_in_phase
    from taskboard.views import HEX, card_cell
    today = date.today()
    b = _aging_cell_board()
    p = b.projects[0]

    def plain(markup):
        return Text.from_markup(markup).plain

    fresh = _stamped("fresh", "Doing", 0, p)
    aged = _stamped("aged", "Doing", 5, p)
    unstamped = _stamped("quiet", "Doing", None, p)
    resting = _stamped("resting", "Done", 9, p)

    # the N=0 boundary: stamped TODAY reads `·0d` — zero is a KNOWN age
    assert "·0d" in plain(card_cell(fresh, b, 30, False, today=today))
    # the N limb: recomputed through the seat's own rule, never a literal
    n = days_in_phase(aged, today)
    assert n is not None and f"·{n}d" in plain(card_cell(aged, b, 30, False,
                                                        today=today))
    # unknown is not zero: no stamp, no token — and no lying `·0d` above all
    assert "·" not in plain(card_cell(unstamped, b, 30, False, today=today))
    # done work rests: a stamped DONE card renders no token either
    assert "·" not in plain(card_cell(resting, b, 30, False, today=today))
    # the tone is the dim house (where date distances live), never a judge
    cell = card_cell(aged, b, 30, False, today=today)
    assert HEX["dim"] in cell
    assert HEX["over"] not in cell and HEX["soon"] not in cell


def test_card_cell_aging_token_sheds_before_the_archived_mark():
    """TC-009 width limb: under width pressure the aging token sheds BEFORE
    the archived mark (the LLR-006.1 ordering — the archived mark is the last
    thing shed, the only token saying the row is not live work), and EVERY
    width still returns exactly `wc` cells, multi-cell token included. RED:
    the token listed after the archived mark (shedding order flipped) → the
    narrow-width limb red; the token's cost mis-measured as a flat 2 cells →
    the width sweep red."""
    from rich.text import Text

    from taskboard.views import ARCHIVED_MARK, card_cell
    today = date.today()
    b = _aging_cell_board()
    t = _stamped("put away", "Doing", 5, b.projects[0], archived=True)
    for wc in range(1, 40):
        cell = card_cell(t, b, wc, False, today=today)
        assert cell_len(Text.from_markup(cell).plain) == wc, \
            f"wc={wc}: an aged card is not width-exact"
    narrow = Text.from_markup(card_cell(t, b, 5, False, today=today)).plain
    assert ARCHIVED_MARK in narrow      # the not-live-work mark survives...
    assert "·5d" not in narrow          # ...and the aging token shed first
    wide = Text.from_markup(card_cell(t, b, 30, False, today=today)).plain
    assert ARCHIVED_MARK in wide and "·5d" in wide


# --------------------------------------------------------------------------- #
# the card deadline countdown (operator 2026-08-24: last-phase cards lost it)
# --------------------------------------------------------------------------- #
def _dated(title, phase, project, delta, archived=False):
    return Task(title=title, project_id=project.id, phase=phase,
                due_date=str(date.today() + timedelta(days=delta)),
                archived=archived)


def test_card_cell_shows_the_deadline_countdown_on_every_dated_card():
    """The kanban card never carried a deadline indicator — the only day
    token it had (`·Nd`, days IN phase) is suppressed on the terminal phase
    by the done-rests law, so a card in the last phase went bare. The
    countdown rides EVERY dated card now, the last phase included: live work
    wears the urgency houses (reldue_token's seats: over / soon / accent /
    dim past a week); done work keeps the FACT but never the JUDGEMENT — the
    same text in the quiet dim house. Undated and archived cards paint
    nothing: no date is no countdown, and put-away work has no live deadline.
    RED counterfactuals: the done card suppressed → the `+3d` limb red; the
    done card judged → the over/soon/accent limb red; archived painted → the
    archived limb red."""
    import re

    from rich.text import Text

    from taskboard.views import HEX, card_cell
    today = date.today()
    b = _aging_cell_board()
    p = b.projects[0]

    def plain(markup):
        return Text.from_markup(markup).plain

    live_soon = _dated("live soon", "Doing", p, 4)
    cell = card_cell(live_soon, b, 40, False, today=today)
    assert "+4d" in plain(cell) and HEX["accent"] in cell

    live_late = _dated("live late", "Doing", p, -2)
    cell = card_cell(live_late, b, 40, False, today=today)
    assert "-2d" in plain(cell) and HEX["over"] in cell

    live_today = _dated("live today", "Doing", p, 0)
    cell = card_cell(live_today, b, 40, False, today=today)
    assert "today" in plain(cell) and HEX["soon"] in cell

    live_far = _dated("live far", "Doing", p, 30)
    cell = card_cell(live_far, b, 40, False, today=today)
    assert "+30d" in plain(cell) and HEX["dim"] in cell

    # the reported limb: the LAST phase keeps the countdown...
    done_task = _dated("done dated", "Done", p, 3)
    cell = card_cell(done_task, b, 40, False, today=today)
    assert "+3d" in plain(cell), "a last-phase card lost its deadline"
    # ...as FACT, not judgement — the quiet dim house, never a judging hue
    assert HEX["dim"] in cell
    assert HEX["over"] not in cell and HEX["soon"] not in cell
    assert HEX["accent"] not in cell

    # no date is no countdown
    undated = Task(title="no date", project_id=p.id, phase="Doing")
    cell = plain(card_cell(undated, b, 40, False, today=today))
    assert not re.search(r"[+-]?\d+d\b", cell) and "today" not in cell

    # put-away work has no live deadline (and the spent-mark law holds)
    away = _dated("put away", "Doing", p, -3, archived=True)
    cell = card_cell(away, b, 40, False, today=today)
    assert "-3d" not in plain(cell)
    assert HEX["over"] not in cell and HEX["soon"] not in cell


def test_card_cell_deadline_token_keeps_the_width_contract():
    """The countdown rides the SAME right-indicator budget: multi-cell token,
    exact `wc` at every width, shedding from the left so it outlives every
    token but ▣."""
    from rich.text import Text

    from taskboard.views import card_cell
    today = date.today()
    b = _aging_cell_board()
    t = _dated("dated card", "Doing", b.projects[0], 6)
    for wc in range(1, 40):
        cell = card_cell(t, b, wc, False, today=today)
        assert cell_len(Text.from_markup(cell).plain) == wc, \
            f"wc={wc}: a dated card is not width-exact"
    narrow = Text.from_markup(card_cell(t, b, 3, False, today=today)).plain
    assert "+6d" not in narrow        # shed whole under pressure, never clipped
    at_cost = Text.from_markup(card_cell(t, b, 4, False, today=today)).plain
    assert "+6d" in at_cost           # kept the moment its 4 cells fit
    wide = Text.from_markup(card_cell(t, b, 40, False, today=today)).plain
    assert "+6d" in wide
