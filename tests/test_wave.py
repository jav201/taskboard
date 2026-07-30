"""The braille dot engine — the laws that make it worth having.

Adapted from `_tui_prism_proposal/verify_prism.py` (laws 3 "sub-cell
resolution", 4 "carved time" and 12's notch clause), narrowed to what can be
asserted about the module ALONE: no view, no board, no composed frame.

The engine's whole claim is that it works below cell resolution. Most of these
tests are written so that the obvious cheaper implementation — lighting whole
braille rows, the REV1 behaviour — fails them.
"""

from taskboard.wave import BRAILLE_BITS, DOT_COLS, DOT_ROWS, FONT_4x7, Bitmap, load_curve

# Derived from the bit map itself, so a change to the packing cannot leave these
# constants quietly describing the old one.
LEFT_BITS = sum(b for (r, c), b in BRAILLE_BITS.items() if c == 0)
RIGHT_BITS = sum(b for (r, c), b in BRAILLE_BITS.items() if c == 1)


def dots(ch: str) -> int:
    return 0 if ch == " " else ord(ch) - 0x2800


def asymmetric_cells(bm: Bitmap) -> int:
    """Cells whose LEFT and RIGHT dot columns carry a different number of dots —
    the count a whole-row fill can never raise above zero."""
    n = 0
    for row in bm.to_braille():
        for ch in row:
            b = dots(ch)
            if b and bin(b & LEFT_BITS).count("1") != bin(b & RIGHT_BITS).count("1"):
                n += 1
    return n


# --------------------------------------------------------------------------- #
# resolution — the reason this module exists
# --------------------------------------------------------------------------- #
def test_one_cell_can_carry_two_different_dot_columns():
    """The minimal statement of the claim: inside a single character, the left
    half and the right half hold different values. A boundary can therefore land
    at half-cell precision instead of snapping to the next character."""
    bm = Bitmap(DOT_COLS, DOT_ROWS)
    bm.fill_to(0, 1)
    bm.fill_to(1, 3)
    cell = bm.to_braille()[0][0]
    assert bin(dots(cell) & LEFT_BITS).count("1") == 1
    assert bin(dots(cell) & RIGHT_BITS).count("1") == 3
    assert asymmetric_cells(bm) == 1


def test_a_drawn_curve_resolves_below_cell_width():
    """The same claim over a real figure rather than a hand-set pair of dots:
    a curve drawn across 96 cells lands its edge mid-character often. Measured:
    52 of 96 cells. The floor is set well below it on purpose — this is a law
    about the mechanism, not about the fixture."""
    bm = Bitmap(96 * DOT_COLS, DOT_ROWS)
    load_curve(bm, [x % 9 for x in range(bm.w)], total=9, edge=bm.w)
    assert asymmetric_cells(bm) >= 20


def test_a_curve_that_only_moves_between_cells_is_the_thing_we_rejected():
    """Anti-vacuity twin of the test above: when the same figure is quantised to
    whole cells (REV1's fill), the census is ZERO. If asymmetric_cells() ever
    stopped measuring, this test would keep passing while the one above broke —
    together they pin both directions."""
    bm = Bitmap(96 * DOT_COLS, DOT_ROWS)
    for cell in range(96):
        h = cell % 5
        bm.fill_to(cell * DOT_COLS, h)
        bm.fill_to(cell * DOT_COLS + 1, h)
    assert asymmetric_cells(bm) == 0


# --------------------------------------------------------------------------- #
# carving — a figure is cut out of a field, never printed over it
# --------------------------------------------------------------------------- #
def test_a_notch_can_never_erase_its_column():
    """The REV2 regression, kept verbatim: at one cell tall a 2-dot bite removed
    a 2-dot curve and two projects' waves disappeared from the frame entirely.
    With no field left it is not a carve, it is a deletion."""
    bm = Bitmap(8, 4)
    bm.fill_to(3, 2)
    bm.carve_notch(3, 4)
    assert bm.ink_at(3) >= 1


def test_a_notch_bites_from_the_top_and_leaves_the_base():
    """Direction matters: the notch is work that fell due off the TOP of the
    day's ink. Biting from the bottom would read as the day never existing."""
    bm = Bitmap(4, 8)
    bm.fill_to(1, 4)
    bm.carve_notch(1, 2)
    assert bm.ink_at(1) == 2
    assert bm.px[bm.h - 1][1] == 1        # the base survived
    assert bm.px[bm.h - 4][1] == 0        # the top two dots are gone


def test_carving_the_boundary_leaves_an_absence_and_touches_nothing_else():
    """Today is drawn by REMOVING a dot column. Overprinting it would put two
    meanings in one cell; carving keeps every cell either field or figure."""
    bm = Bitmap(6, 4)
    for x in range(6):
        bm.fill_to(x, 4)
    bm.carve_col(3)
    assert bm.ink_at(3) == 0
    assert all(bm.ink_at(x) == 4 for x in (0, 1, 2, 4, 5))


def test_carving_text_only_removes_ink_and_reports_its_footprint():
    """Digits are cut out of the field too. The return value exists so a caller
    can check the figure had field to be carved FROM — a carve into emptiness
    draws nothing and must not be mistaken for a drawn number."""
    bm = Bitmap(20, 8)
    for x in range(20):
        bm.fill_to(x, 8)
    before = bm.lit()
    w, h = bm.carve_text("40", 0, 0)
    glyph_dots = sum(line.count("#") for line in FONT_4x7["4"]) \
        + sum(line.count("#") for line in FONT_4x7["0"])
    assert bm.lit() == before - glyph_dots      # removed exactly the glyph
    assert bm.lit() < before                    # and never added a dot
    assert (w, h) == (10, 7)                    # 4 wide + 1 gap, twice

    empty = Bitmap(20, 8)
    empty.carve_text("40", 0, 0)
    assert empty.lit() == 0                     # nothing to carve -> nothing drawn


# --------------------------------------------------------------------------- #
# packing — the bitmap becomes characters only at the last step
# --------------------------------------------------------------------------- #
def test_each_dot_packs_to_its_documented_bit():
    for (r, c), bit in BRAILLE_BITS.items():
        bm = Bitmap(DOT_COLS, DOT_ROWS)
        bm.px[r][c] = 1
        assert bm.to_braille()[0][0] == chr(0x2800 + bit), f"dot {(r, c)}"


def test_a_full_cell_is_dense_and_an_empty_cell_is_a_space():
    """The unlit ground comes back as ' ', NOT as blank braille U+2800: the
    caller decides what the ground is (the field's own lattice), so the engine
    must not silently commit it to a void."""
    full = Bitmap(DOT_COLS, DOT_ROWS)
    for r in range(DOT_ROWS):
        for c in range(DOT_COLS):
            full.px[r][c] = 1
    assert full.to_braille()[0][0] == "⣿"
    assert Bitmap(DOT_COLS, DOT_ROWS).to_braille()[0][0] == " "
    assert Bitmap(DOT_COLS, DOT_ROWS).to_braille()[0][0] != "⠀"


def test_the_grid_packs_to_cell_shape_including_a_ragged_edge():
    bm = Bitmap(2 * 3, 4 * 2)
    assert [len(r) for r in bm.to_braille()] == [3, 3]
    ragged = Bitmap(5, 6)                      # not a whole number of cells
    out = ragged.to_braille()
    assert len(out) == 2 and all(len(r) == 3 for r in out)
    ragged.px[5][4] = 1                        # the last, partly out-of-grid cell
    assert ragged.to_braille()[1][2] != " "


def test_the_same_input_draws_the_same_dots_twice():
    """Determinism: the engine is pure. Two identical builds must be identical
    down to the character, or a redraw would flicker for no reason."""
    def build():
        bm = Bitmap(40, 8)
        load_curve(bm, [x // 2 for x in range(40)], total=12, edge=30)
        bm.carve_col(14)
        bm.carve_notch(9, 2)
        bm.carve_text("7", 2, 0)
        return bm
    a, b = build(), build()
    assert a.px == b.px
    assert a.to_braille() == b.to_braille()
    assert a.to_braille() == a.to_braille()


# --------------------------------------------------------------------------- #
# load_curve — the cumulative bank
# --------------------------------------------------------------------------- #
def test_the_curve_stops_at_the_projects_own_edge():
    """The bank spans the life the project has left, not the width of the
    screen. Past its due date a plateau would run to the right edge saying
    nothing."""
    bm = Bitmap(20, 4)
    load_curve(bm, [5] * 20, total=5, edge=9)
    assert all(bm.ink_at(x) > 0 for x in range(10))
    assert all(bm.ink_at(x) == 0 for x in range(10, 20))


def test_any_nonzero_load_lights_at_least_one_dot():
    """Visibility floor: one item out of two hundred still rounds to nothing,
    and 'nothing' is a lie the reader cannot detect."""
    bm = Bitmap(4, 4)
    load_curve(bm, [1, 0, 200, 0], total=200, edge=4)
    assert bm.ink_at(0) == 1
    assert bm.ink_at(1) == 0            # a genuine zero stays empty
    assert bm.ink_at(2) == 4


def test_a_bigger_stable_total_paints_less_ink_not_more():
    """REV1's bug, pinned: it normalised to the shrinking OPEN count, so a
    project with half the load drew MORE ink. The denominator is the whole task
    set — finishing work must lower the wave, never raise it."""
    steps = [3] * 10
    light, heavy = Bitmap(10, 8), Bitmap(10, 8)
    load_curve(light, steps, total=20, edge=10)
    load_curve(heavy, steps, total=4, edge=10)
    assert light.lit() < heavy.lit()


def test_non_decreasing_steps_never_draw_a_falling_curve():
    """It is a CUMULATIVE bank: monotone in, monotone out. A dip would claim
    work was un-scheduled."""
    bm = Bitmap(30, 8)
    load_curve(bm, sorted(x % 7 for x in range(30)), total=6, edge=30)
    heights = [bm.ink_at(x) for x in range(30)]
    assert heights == sorted(heights)


def test_columns_outside_the_grid_are_ignored_not_wrapped():
    """Every op takes a column index that a caller may compute off the edge of
    the window; the engine must drop it, never fold it onto the far side."""
    bm = Bitmap(4, 4)
    for x in range(4):
        bm.fill_to(x, 2)
    before = [row[:] for row in bm.px]
    bm.fill_to(-1, 4)
    bm.fill_to(99, 4)
    bm.carve_col(-1)
    bm.carve_col(99)
    bm.carve_notch(-1)
    bm.carve_notch(99)
    assert bm.px == before
    assert bm.ink_at(-1) == 0 and bm.ink_at(99) == 0
