"""BLUEPRINT'S FRAME MECHANISM — the stamp, taken as content rather than as a
mode strip (LIMITS L-32).

`title_block(options, active, w)` had no test at all, which is part of how it
came to have a signature only one app could satisfy: nothing outside the board
ever called it, so nothing outside the board ever noticed that nothing outside
the board COULD. These tests call the mechanism the way a second app does —
with rows of cells and no selection — because that is the case the old
interface could not express.
"""
import pytest
from rich.text import Text

import taskboard.language as LG


W = 116


def kit():
    return LG.kit("blueprint")


def plain(rows) -> list[str]:
    return [Text.from_markup(r).plain for r in rows]


def cells(row: str) -> int:
    """Cells the row actually draws — measured through rich, never `len()`."""
    return len(Text.from_markup(row).plain)


# --------------------------------------------------------------------------
# AC-2 — content is data, selection is an extra
# --------------------------------------------------------------------------

def test_a_stamp_needs_no_mode_strip_at_all():
    """L-32: *a frame mechanism should take its content as data (rows of
    cells, a state string) and its selection as an optional extra, so the
    block is reusable by anything with an identity and a state.*

    This is emersio-lab's stamp — an identity, four parameter cells, a tally
    and a knocked-out state, over two body rows, with no mode strip anywhere
    in it — and the point is that it renders at all."""
    k = kit()
    rows = [[("", "EMERSIO  MBB 60x20", False),
             ("PENAL", "3.0", False), ("RMIN", "1.5", False)],
            [("ITER", "12/40", False), ("C", "0.412", False),
             ("", "CONVERGED", True)]]
    out = k.stamp(rows, W)

    assert len(out) == len(rows) + 2, "two rules bracket the body, always"
    assert all(cells(r) == W for r in out), [cells(r) for r in out]
    body = plain(out)[1:-1]
    assert "EMERSIO" in body[0] and "CONVERGED" in body[1]
    assert "PENAL 3.0" in body[0], "a captioned cell is `CAP value`"


def test_a_stamp_with_no_selection_draws_no_registration_marks():
    """The registration marks are this language's SELECTION mechanism. An app
    with nothing selected gets none of them — which is not the same as getting
    marks around nothing, and is the distinction `strip=None` exists to carry.
    """
    k = kit()
    rows = [[("SHEET", "EMERSIO", False), ("", "RUNNING", True)]]
    bare = "".join(plain(k.stamp(rows, W)))
    assert not (set(k.REG) & set(bare)), (
        f"a stamp with no strip registered something: {sorted(set(k.REG) & set(bare))}")

    marked = "".join(plain(k.stamp(rows, W, strip=(["a", "b"], "a"))))
    assert set(k.REG) <= set(marked), (
        "a stamp WITH a strip must still register the active mode — the "
        "assertion above would pass vacuously if it never did")


def test_a_stamp_docks_to_the_bottom_corner_and_rules_only_itself():
    """*The two rules run from the block's own origin to the sheet's edge* —
    a rule the full width of the page would be a third stroke on a sheet whose
    whole frame budget is this stamp. So the rules start where the block does
    and the cells above and below them are blank."""
    k = kit()
    rows = [[("SHEET", "EMERSIO", False), ("", "RUNNING", True)]]
    top, mid, bot = plain(k.stamp(rows, W))
    assert top == bot, "the two rules bracket the block symmetrically"
    ruled = top.index(k.EXT)
    assert top[ruled:] == k.EXT * (W - ruled), "the rule runs to the edge"
    assert top[:ruled].strip() == "", "nothing is drawn left of the rule"
    assert mid[:ruled].strip() == "", "the block is docked, not centred"
    assert W - ruled == k.block_w(rows[0]), (
        "the rule is exactly as long as the block it brackets, so a wider "
        "sheet buys the stamp air and not a longer stroke")


def test_the_knockout_is_the_only_reversed_cell():
    """*Exactly ONE element per view reverses to a pale ground with dark ink*,
    and it is the first-fixation law of this language."""
    k = kit()
    rows = [[("SHEET", "EMERSIO", False), ("REV", "01", False),
             ("", "RUNNING", True)]]
    markup = "".join(k.stamp(rows, W))
    assert markup.count(" on ") == 1, "one knockout per sheet, no more"
    assert f"[{k.t['ground']} on {k.c['ink']}]" in markup


def test_a_stamp_draws_no_glyph_this_language_does_not_own():
    """The alphabet is TEN marks and none of them is a vertical stroke. The
    stamp is the language's largest structural investment, so it is the place
    a stray `│` would be most tempting and least noticed."""
    k = kit()
    rows = [[("SHEET", "EMERSIO", False), ("", "RUNNING", True)]]
    drawn = set("".join(plain(k.stamp(rows, W, strip=(["a", "b"], "a")))))
    stray = {c for c in drawn if not (c.isalnum() or c in " -/.:")
             } - k.glyphs
    assert not stray, f"glyphs outside the language: {sorted(stray)}"


@pytest.mark.parametrize("evil", ["[bold red]x[/] [ [", "[URGENT] ship"])
def test_a_stamp_cell_cannot_inject_markup_or_steal_a_cell(evil):
    """The codebase's pitfall A1, on the new caller-facing surface. Escaping
    changes a string's CHARACTER count and not its CELL count, so a mechanism
    that measured the escaped string would hand back a rectangle one cell
    short — and a stamp is docked by arithmetic on exactly that measure."""
    k = kit()
    out = k.stamp([[("SHEET", evil, False), ("", "RUNNING", True)]], W)
    assert all(cells(r) == W for r in out), [cells(r) for r in out]
    assert evil in "".join(plain(out)), (
        "the value was parsed as markup instead of printed literally")


# --------------------------------------------------------------------------
# the board's block still works, and still narrows the way it declared
# --------------------------------------------------------------------------

def test_the_board_block_is_the_adapter_and_nothing_more():
    """`title_block()` keeps its signature so the board's captures stay
    byte-identical; what it may not keep is a second implementation of the
    docking arithmetic. Asserted by construction: it must equal the mechanism
    called with the one thing that is taskboard's about it — which cells."""
    k = kit()
    opts, active = ["board", "notes", "config"], "board"
    strip, _, _ = k._mode_strip(opts, active)
    assert k.title_block(opts, active, W) == k.stamp(
        [k.block_cells(W, len(strip))], W, strip=(opts, active))


def test_the_narrowing_ladder_sheds_in_the_declared_order():
    """Tier 1 sheds cells in `TB_DROP` order, tier 2 gives up the modes the
    sheet is not on, tier 3 renounces the strip and keeps the state. The
    STATE is never shed, because the state is the knockout."""
    k = kit()
    opts, active = ["board", "notes", "config"], "board"
    seen = {w: "".join(plain(k.title_block(opts, active, w)))
            for w in (116, 60, 40, 24, 12)}

    assert "SHEET" in seen[116] and "REV" in seen[116] and "WORK" in seen[116]
    assert "SHEET" not in seen[60], "tier 1 sheds `sheet` first"
    assert "REV" not in seen[40] and "WORK" not in seen[40]
    assert "config" not in seen[24], "tier 2 gives up the modes not on screen"
    assert "BOARD" not in seen[12], "tier 3 renounces the strip"
    for w, got in seen.items():
        assert "CLEAR" in got, f"the STATE was shed at w={w}"


# --------------------------------------------------------------------------
# AC-3 — the series, decided in spec §6.1 (LIMITS L-34)
# --------------------------------------------------------------------------

HIST = [1.0, .62, .40, .28, .19, .13, .09, .062, .045, .034, .028, .025]


def ends(row: str) -> int:
    """The column the row's closing terminator stands in — the trace itself."""
    return Text.from_markup(row).plain.index("┤")


def test_a_series_smuggles_in_no_vertical_stroke():
    """L-34's whole content: *every conventional plot axis in a terminal is
    `│` and `└`*, and neither is one of this language's ten marks. The batch's
    instruction was to decide and implement, and **not** to smuggle `│└` in —
    so the decision is worth an assertion rather than a promise."""
    k = kit()
    drawn = set("".join(plain(k.series(HIST, 46, 10, label="compliance"))))
    assert "│" not in drawn and "└" not in drawn, "an axis was smuggled in"
    stray = {c for c in drawn if not (c.isalnum() or c in " -+.,()%/")} - k.glyphs
    assert not stray, f"glyphs outside the language's ten: {sorted(stray)}"


def test_the_trace_is_the_locus_of_the_closing_terminators():
    """The mechanism's claim. A monotonically falling series must produce a
    monotonically falling column of `┤`, because that column IS the curve —
    if it does not, this is a stack of unrelated bars wearing a trace's name.
    """
    k = kit()
    # one seat per sample plus the scale row, so every body row is a sample
    body = plain(k.series(HIST, 46, len(HIST) + 1))[:-1]
    cols = [ends(r) for r in body]
    assert cols == sorted(cols, reverse=True), cols
    assert cols[0] > cols[-1], "a converging series must visibly converge"


def test_the_scale_is_published_and_is_never_shed():
    """DATAVIZ law 2 forbids a row normalised to itself. A SERIES may derive
    its ceiling — the siblings are in hand — but must then state it, or the
    reader has a shape with no units. The declared ladder therefore drops the
    label before the scale, at every height down to the minimum."""
    k = kit()
    for h in (12, 6, 3, 2):
        rows = plain(k.series(HIST, 40, h, label="compliance"))
        assert len(rows) == h
        assert "1" in rows[-1] and rows[-1].count("├") == 1, (
            f"h={h}: the scale row is gone: {rows[-1]!r}")
    assert "COMPLIANCE" not in "".join(plain(k.series(HIST, 40, 2))), (
        "at the minimum height the label must go before the scale does")


def test_a_declared_ceiling_beats_the_series_own_maximum():
    """Two traces are comparable only if neither was normalised to itself, so
    a caller comparing runs passes the ceiling and the spans must honour it."""
    k = kit()
    lone = k.series([0.5], 40, 2)
    shared = k.series([0.5], 40, 2, ceiling=1.0)
    assert ends(lone[0]) > ends(shared[0]), (
        "a declared ceiling did not change the run — the argument is dead")
    assert "1" in plain(shared)[-1], "the declared ceiling is what is stated"


def test_an_off_scale_sample_is_flagged_and_its_figure_stays_true():
    """DATAVIZ: clip and flag, never clamp. The run stops at the ceiling, the
    first cell becomes the BREAK mark, and the figure keeps saying 1.4."""
    k = kit()
    rows = plain(k.series([1.4], 30, 2, ceiling=1.0))
    assert k.BREAK in rows[0], f"an off-scale sample was clamped: {rows[0]!r}"
    assert "1.4" in rows[0], "the figure on a clipped span must stay the truth"


def test_a_small_sample_never_rounds_onto_a_zero_sample():
    """The microbar floor (DATAVIZ law 3), which this mechanism has to obey
    separately from the card's span because a convergence value is a float and
    a due date is an integer count of days."""
    k = kit()
    zero, tiny = k.series([0.0], 40, 2)[0], k.series([0.001], 40, 2, ceiling=1.0)[0]
    assert ends(tiny) > ends(zero), (
        "a small sample rounded onto zero — nothing and almost-nothing must "
        "not draw the same mark")


def test_the_series_fills_exactly_the_rectangle_it_was_given():
    """A trace is placed in a reserved seat like anything else here."""
    k = kit()
    for w, h in ((46, 10), (20, 4), (8, 2), (120, 30)):
        rows = k.series(HIST, w, h, label="c(k)")
        assert len(rows) == h, (w, h, len(rows))
        assert all(cells(r) == w for r in rows), [cells(r) for r in rows]


def test_a_long_series_keeps_both_of_its_endpoints():
    """A subsample that dropped where the run started or where it got to would
    be answering a different question from the one a convergence curve asks."""
    k = kit()
    vals = [1.0 - i / 100 for i in range(100)]
    kept = k._sample(vals, 6)
    assert len(kept) == 6 and kept[0] == vals[0] and kept[-1] == vals[-1]


def test_an_empty_series_still_states_its_scale():
    """Nothing to draw is not the same as a shorter trace, and a sheet that
    closed up the empty seats would be claiming the second."""
    k = kit()
    rows = plain(k.series([], 30, 5))
    assert len(rows) == 5
    assert rows[-1].count("├") == 1, "the scale row survived an empty series"
    assert all(r.strip() == "" for r in rows[:-1]), rows[:-1]
