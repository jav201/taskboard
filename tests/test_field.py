"""The shared day axis and the field — the helpers, before any view uses them.

Adapted from `_tui_prism_proposal/verify_prism.py` law 12, "CLIP AND FLAG, never
clamp", which asserted only that `Geo.day_dc` RETURNS a flag. These tests keep
that law and add the half the proposal never had: that the flag becomes a MARK.
"""

from datetime import date, timedelta

from taskboard.views import (LATTICE, OFF_LEFT, OFF_RIGHT, RULE, day_col,
                             field_geometry, field_rows, off_window_glyph)
from taskboard.wave import Bitmap

TODAY = date(2026, 7, 30)
WIDTHS = (24, 25, 31, 32, 33, 40, 63, 72, 87, 88, 96, 97, 130, 201)


def plain(markup: str) -> str:
    """The visible cells of a markup row — width math lives on plain text."""
    out, depth = [], 0
    for ch in markup:
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
        elif depth == 0:
            out.append(ch)
    return "".join(out)


# --------------------------------------------------------------------------- #
# the axis
# --------------------------------------------------------------------------- #
def test_one_dot_column_is_one_day_and_today_never_straddles_a_cell():
    """Today must land on an EVEN dot column: a boundary that fell between two
    cells would be drawn half in one character and half in the next, and the
    rule would look like it moved when nothing had."""
    for w in WIDTHS:
        for h in (12, 24, 30, 40):
            g = field_geometry(w, h)
            assert g.dot_w == g.field_w * 2
            assert g.today_dc % 2 == 0
            assert 0 <= g.today_dc < g.dot_w
            assert g.today_cell == g.field_x + g.today_dc // 2


def test_a_date_inside_the_window_is_a_plain_column():
    g = field_geometry(96, 30)
    assert day_col(TODAY, TODAY, g) == g.today_dc
    assert day_col(TODAY + timedelta(days=3), TODAY, g) == g.today_dc + 3
    assert day_col(TODAY - timedelta(days=3), TODAY, g) == g.today_dc - 3
    assert off_window_glyph(day_col(TODAY, TODAY, g)) == ""


def test_a_date_outside_the_window_is_flagged_and_never_silently_clamped():
    """verify_prism law 12, kept verbatim in intent: the return value SAYS it
    was clipped. A bare clamped integer would make 'due at the edge' and 'due
    three years past the edge' the same picture."""
    g = field_geometry(96, 30)
    far = day_col(TODAY + timedelta(days=3650), TODAY, g)
    past = day_col(TODAY - timedelta(days=3650), TODAY, g)
    assert isinstance(far, tuple) and far[0] == "R" and far[1] == g.dot_w - 1
    assert isinstance(past, tuple) and past[0] == "L" and past[1] == 0


def test_a_flagged_column_earns_a_mark():
    """The half the proposal specified (§4.2, R3) but never drew: every caller
    of `Geo.day_dc` took `c[1]` and dropped the flag, so nothing marked the
    window. Here the flag has a glyph."""
    g = field_geometry(96, 30)
    assert off_window_glyph(day_col(TODAY - timedelta(days=999), TODAY, g)) == OFF_LEFT
    assert off_window_glyph(day_col(TODAY + timedelta(days=999), TODAY, g)) == OFF_RIGHT
    assert off_window_glyph(day_col(TODAY + timedelta(days=1), TODAY, g)) == ""


def test_the_window_boundaries_are_inclusive_on_the_left_and_exclusive_on_the_right():
    """The exact day the window ends is the last one that fits; the next is
    flagged. Off-by-one here would silently drop a day at each edge."""
    g = field_geometry(96, 30)
    first = TODAY - timedelta(days=g.today_dc)
    last = TODAY + timedelta(days=g.dot_w - 1 - g.today_dc)
    assert day_col(first, TODAY, g) == 0
    assert day_col(last, TODAY, g) == g.dot_w - 1
    assert isinstance(day_col(first - timedelta(days=1), TODAY, g), tuple)
    assert isinstance(day_col(last + timedelta(days=1), TODAY, g), tuple)


# --------------------------------------------------------------------------- #
# the field
# --------------------------------------------------------------------------- #
def _empty_field(w: int, h: int, rows: int = 1):
    g = field_geometry(w, h)
    return g, field_rows(Bitmap(g.dot_w, rows * 4), g, "violet")


def test_the_field_is_width_exact_at_every_width():
    """Width-exactness is this codebase's oldest law — a row that is one cell
    wrong breaks every box-drawing alignment below it."""
    for w in WIDTHS:
        for h in (12, 24, 30):
            g, rows = _empty_field(w, h, rows=2)
            assert len(rows) == 2
            for r in rows:
                assert len(plain(r)) == g.field_w, f"width {w}x{h}"


def test_an_empty_field_is_a_lattice_and_a_rule_not_a_void():
    """Nothing to show is a DESIGNED state: the ground keeps its own lattice so
    the row still has a floor, and the rule still says where today is."""
    g, rows = _empty_field(96, 30)
    row = plain(rows[0])
    assert set(row) == {LATTICE, RULE}
    assert row[g.today_dc // 2] == RULE
    assert row.count(RULE) == 1


def test_the_ground_is_ash_behind_today_and_dim_ahead():
    """The consumed field reads differently from the field still to spend —
    that difference IS the datum, and it is carried by a boundary that moves,
    not by a count."""
    g, rows = _empty_field(96, 30)
    from taskboard.views import HEX
    cells = rows[0].split("[/]")
    ash = sum(1 for s in cells if HEX["ash"] in s)
    dim = sum(1 for s in cells if HEX["dim"] in s)
    assert ash == g.today_dc // 2                  # every cell fully behind today
    assert dim == g.field_w - ash - 1              # the rest, minus the rule cell
    assert HEX["accent"] in rows[0]                # the rule wears attention


def test_the_figure_is_drawn_over_the_lattice_and_keeps_the_rule():
    """A drawn wave replaces lattice cells with braille, but the today rule is
    an ABSENCE carved through it, so it survives."""
    g = field_geometry(96, 30)
    bm = Bitmap(g.dot_w, 4)
    for x in range(g.dot_w):
        bm.fill_to(x, 4)
    bm.carve_col(g.today_dc)
    bm.carve_col(g.today_dc + 1)                   # the rule cell's other dot column
    row = plain(field_rows(bm, g, "violet")[0])
    assert len(row) == g.field_w
    assert row[g.today_dc // 2] == RULE
    assert row.count(LATTICE) == 0                 # the figure covered the ground
    assert row.count("⣿") == g.field_w - 1


def test_a_figure_behind_today_is_ash_and_ahead_is_its_own_hue():
    from taskboard.views import HEX
    g = field_geometry(96, 30)
    bm = Bitmap(g.dot_w, 4)
    bm.fill_to(0, 4)                               # far behind today
    bm.fill_to(g.dot_w - 1, 4)                     # far ahead
    row = field_rows(bm, g, "violet")[0]
    assert HEX["ash"] in row
    assert HEX["violet"] in row


def test_something_outside_the_window_is_marked_at_the_edge():
    """`◂`/`▸`, never a crush: the row says the window is missing something
    instead of pretending the edge is the end of the data."""
    g, rows = _empty_field(96, 30)
    marked = field_rows(Bitmap(g.dot_w, 4), g, "violet", off_left=True, off_right=True)
    row = plain(marked[0])
    assert len(row) == g.field_w
    assert row[0] == OFF_LEFT and row[-1] == OFF_RIGHT
    assert plain(rows[0])[0] == LATTICE            # and absent when nothing is out


def test_the_mark_is_neutral_it_neither_names_nor_judges():
    """The ration still holds here: the edge mark reports the WINDOW, so it may
    not wear an identity hue or a judging one."""
    from taskboard.views import HEX
    g = field_geometry(96, 30)
    row = field_rows(Bitmap(g.dot_w, 4), g, "violet", off_left=True, off_right=True)[0]
    marks = [seg for seg in row.split("[/]") if OFF_LEFT in seg or OFF_RIGHT in seg]
    assert len(marks) == 2
    for seg in marks:
        assert HEX["mut"] in seg
        for forbidden in ("over", "soon", "violet"):
            assert HEX[forbidden] not in seg


def test_a_short_bitmap_is_padded_with_lattice_never_with_holes():
    """A caller may hand in a bitmap narrower than the window (a project whose
    life ends before the right edge). The field still covers its whole width."""
    g = field_geometry(96, 30)
    row = plain(field_rows(Bitmap(8, 4), g, "violet")[0])
    assert len(row) == g.field_w
    assert row[-1] == LATTICE


def test_the_ported_geometry_does_not_fit_below_32_columns():
    """CHARACTERISTIC, not aspiration — this records what the ported `Geo`
    actually does so a later fix is deliberate. `field_w` has a floor of 8, so
    below 32 columns the label + field + figures add up to MORE than the width.
    No view calls this yet, which is why it is safe to ship and name."""
    for w in range(24, 32):
        g = field_geometry(w, 24)
        assert g.field_w == 8
        assert g.label_w + g.field_w + g.figs_w + 1 > w      # overflows, measured
    for w in range(32, 88):
        g = field_geometry(w, 24)
        assert g.label_w + g.field_w + g.figs_w + 1 == w     # fits exactly
