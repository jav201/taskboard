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
