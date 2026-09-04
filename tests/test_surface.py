"""The `surface` axis: is the token DISPATCHED, or is it decoration?

The whole batch exists because of one recorded failure (LANGUAGES.md, "a
language definition is code, not a manifest"): eight languages each declared a
`base`, `frame`, `numbered` and `dot_w`, none of them were read, and two of the
eight rendered byte-identically while the file header claimed otherwise. The
check that catches it is the MUTATION check — swap the token, and if the render
does not change, the token is dead metadata.

So the load-bearing test in this file is `test_mutation_changes_the_render`.
Every other test asserts a posture's DEFINING property, which is what stops the
mutation test from passing vacuously: eight mechanisms that all differ from each
other but none of which does what its language committed to would satisfy a
diff and satisfy nothing else.
"""
from __future__ import annotations

import pytest
from PIL import Image
from rich.text import Text

from taskboard import language as LG
from taskboard import raster as RS
from taskboard.themes import ORDER, THEMES

W, H = 24, 8


def probe(size=(64, 32)) -> Image.Image:
    """A synthetic image with a KNOWN gradient and a hard edge.

    Not a flat field: a flat frame quantises to ONE colour (tui-demos LIMITS
    L-18) and every posture would then agree with every other by accident —
    the mutation test would pass on an input that cannot distinguish them. And
    not noise either, because the lattice postures must be allowed to produce a
    lattice rather than a hash."""
    w, h = size
    img = Image.new("RGB", size)
    img.putdata([(255 - (x * 255 // w), 255 - (x * 255 // w),
                  255 - (x * 255 // w)) if y < h // 2 else (20, 20, 20)
                 for y in range(h) for x in range(w)])
    return img


def cells(row: str) -> int:
    """The cells a markup row actually draws — measured through rich, not by
    `len()`, which counts the markup tags."""
    return Text.from_markup(row).cell_len


def text_of(res) -> str:
    return "".join(Text.from_markup(r).plain for r in res.rows)


def on_ramp(c, low: str, high: str, tol: int = 2) -> bool:
    """Is colour `c` a blend of `low` and `high`?

    This is what "the posture tinted the pixels" MEANS, and it is checked as a
    property of every colour rather than by looking for the two endpoints: a
    source image whose luma never reaches 0 or 255 legitimately never produces
    the endpoints, so an endpoint test would fail on a correct render and pass
    on a source that happened to be black somewhere."""
    lo, hi = RS.rgb(low), RS.rgb(high)
    spans = [hi[i] - lo[i] for i in range(3)]
    i = max(range(3), key=lambda j: abs(spans[j]))
    if spans[i] == 0:
        return c == lo
    t = (c[i] - lo[i]) / spans[i]
    return (-0.02 <= t <= 1.02
            and all(abs(c[j] - (lo[j] + t * spans[j])) <= tol for j in range(3)))


DECLARED = [n for n in ORDER if "surface" in THEMES[n]]


# --------------------------------------------------------------------------
# AC-1 — the token is dispatched, not decorative
# --------------------------------------------------------------------------

def test_every_declared_token_has_a_mechanism():
    """The lenient `.get(..., default)` dispatch (the shape `METERS` uses) will
    happily render an unknown posture as `untinted`. That is right for a THEME
    the app does not ship, and wrong for one it does: a typo'd token would
    render plausibly forever. So the declared set is checked against the
    registry rather than trusted to the default."""
    missing = [n for n in DECLARED if THEMES[n]["surface"] not in LG.SURFACES]
    assert not missing, f"declared postures with no mechanism: {missing}"


@pytest.mark.parametrize("name", DECLARED)
def test_mutation_changes_the_render(name):
    """AC-1. For each language: swap `surface` to a DIFFERENT posture and the
    rendered bytes must change; swap it back and they must return byte for
    byte. Both halves matter — a render that changed for any other reason
    (a clock, a hash seed) would also fail the restore."""
    img = probe()
    kit = LG.kit(name)
    before = kit.raster_region(img, W, H).blob()

    others = [p for p in LG.LIVE_SURFACES if p != THEMES[name]["surface"]]
    assert others, "a posture with nothing to swap to cannot be mutation-tested"
    original = THEMES[name]["surface"]
    try:
        for other in others:
            THEMES[name]["surface"] = other
            got = LG.kit(name).raster_region(img, W, H).blob()
            assert got != before, (
                f"{name}: swapping surface {original!r} -> {other!r} rendered "
                f"IDENTICAL bytes — the token is dead metadata")
    finally:
        THEMES[name]["surface"] = original

    assert LG.kit(name).raster_region(img, W, H).blob() == before, (
        f"{name}: restoring surface {original!r} did not restore the render")


@pytest.mark.parametrize("name", DECLARED)
def test_region_is_the_rectangle_the_layout_reserved(name):
    """AC-3. The region is an OPAQUE RECTANGLE the layout reserves, on both
    paths (CEILINGS §7 — the compositor never knows an image's content, so a
    ragged or short region is a region something else can be composited into).
    Exactly `h` rows, each exactly `w` cells."""
    res = LG.kit(name).raster_region(probe(), W, H)
    assert res.reserved == (W, H)
    assert len(res.rows) == H, f"{name}: {len(res.rows)} rows, wanted {H}"
    bad = [(i, cells(r)) for i, r in enumerate(res.rows) if cells(r) != W]
    assert not bad, f"{name}: rows not {W} cells wide: {bad}"


@pytest.mark.parametrize("name", DECLARED)
def test_posture_is_reported_and_matches_the_token(name):
    res = LG.kit(name).raster_region(probe(), W, H)
    assert res.posture == THEMES[name]["surface"]


# --------------------------------------------------------------------------
# AC-7 — phosphor and BBS stay honest
# --------------------------------------------------------------------------

@pytest.mark.parametrize("posture", ["phosphor", "bbs"])
def test_catalogue_postures_refuse_by_name(posture):
    """They are documented in LANGUAGES.md and no kit renders them. Mapping
    either onto a posture that merely looks similar would report a commitment
    no code implements — undetectable from outside, which is why AC-7 exists."""
    assert posture in LG.SURFACES
    assert posture not in LG.LIVE_SURFACES
    kit = LG.kit("nord")
    THEMES["nord"]["surface"] = posture
    try:
        with pytest.raises(NotImplementedError) as e:
            LG.kit("nord").raster_region(probe(), W, H)
        assert posture in str(e.value)
        assert "CATALOGUE-ONLY" in str(e.value)
    finally:
        THEMES["nord"]["surface"] = "untinted"
    assert kit  # the kit itself never raised — only rendering the posture did


# --------------------------------------------------------------------------
# AC-2 — each mechanism does its language's declared thing
# --------------------------------------------------------------------------

def test_lattice_draws_only_lattice_glyphs():
    """Naught: "a photograph would break the one thing that makes it Naught".
    The rendered cells must come from the language's own dot alphabet and
    nothing else — no half-blocks, no shade ramp, no image glyphs."""
    res = LG.kit("naught").raster_region(probe(), W, H)
    extra = set(text_of(res)) - set(LG.Kit.LATTICE_GLYPHS)
    assert not extra, f"non-lattice glyphs in a lattice surface: {sorted(extra)}"


def test_lattice_shows_the_unlit_grid():
    """The commitment that separates an LED panel from sparse block type: the
    dark dots are RENDERED, not spaces."""
    res = LG.kit("naught").raster_region(probe(), W, H)
    body = text_of(res)
    from taskboard import naught as NA
    assert NA.ON in body and NA.OFF in body


def test_lattice_pixels_are_two_colours():
    """AC-3's other half: the posture is applied TO THE PIXELS too. A lattice
    that dithered the cells and handed `textual_image` the original photograph
    would be two languages in one region."""
    res = LG.kit("naught").raster_region(probe(), W, H)
    assert len(set(res.pixels.getdata())) == 2


def test_display_draws_a_frame_and_keeps_pixels_inside_it():
    """Corgi: "pixels live only inside the numbered, boxed display; every
    control around it stays a label"."""
    res = LG.kit("corgi").raster_region(probe(), W, H)
    rows = [Text.from_markup(r).plain for r in res.rows]
    assert rows[0][0] == "┌" and rows[0][-1] == "┐"
    assert rows[-1][0] == "└" and rows[-1][-1] == "┘"
    assert all(r[0] == "│" and r[-1] == "│" for r in rows[1:-1])
    assert "DISPLAY" in rows[0]
    assert "1" in rows[0], "corgi is `numbered`; its display is numbered too"
    assert RS.HALF not in rows[0] and RS.HALF not in rows[-1], (
        "image glyphs escaped the display region")


def test_display_tints_to_the_screen_not_to_the_source():
    """The glass is two colours, and they are the language's own screen — a
    full-colour photograph inside an LCD is a picture of a different device."""
    kit = LG.kit("corgi")
    res = kit.raster_region(probe(), W, H)
    _, low, high = kit.display_chrome()
    seen = set(res.pixels.convert("RGB").getdata())
    off = [c for c in seen if not on_ramp(c, low, high)]
    assert not off, f"colours outside the screen ramp {low}->{high}: {sorted(off)[:4]}"
    assert len(seen) > 2, "the glass carries the image, not two flat values"


def test_tint_is_cyanotype_and_carries_a_dimension_span():
    """Blueprint: "linework at true resolution, cyanotype-tinted, WITH
    DIMENSION SPANS DRAWN OVER IT — the chrome stays the data-viz even on
    pixels"."""
    kit = LG.kit("blueprint")
    res = kit.raster_region(probe(), W, H)
    low, high = kit.tint_pair()
    assert (low, high) == (THEMES["blueprint"]["ground"],
                           THEMES["blueprint"]["ink"])
    seen = set(res.pixels.convert("RGB").getdata())
    off = [c for c in seen if not on_ramp(c, low, high)]
    assert not off, f"colours off the cyanotype ramp: {sorted(off)[:4]}"
    assert all(c[2] > c[0] for c in seen), (
        "a cyanotype is blue-dominant in every pixel, at both ends of the ramp")
    rows = [Text.from_markup(x).plain for x in res.rows]
    spans = [x for x in rows if x.startswith("├") and x.rstrip().endswith("┤")]
    assert spans, f"no dimension span drawn over the tint: {rows[0]!r}"
    assert any("px" in x for x in spans), "a span with no figure is not a span"


def test_untinted_hands_over_the_source_pixels_unchanged():
    """base16/nord: "the single thing the user's scheme cannot restyle, so it
    is shown as-is, with no frame — the environment's rules stop at its edge"."""
    img = probe()
    res = LG.kit("nord").raster_region(img, W, H)
    assert res.pixels is img
    plain = [Text.from_markup(r).plain for r in res.rows]
    assert all(set(r) <= {RS.HALF, " "} for r in plain), (
        "untinted drew chrome; the posture is that there is none")


def test_refuse_yields_no_pixels_at_all():
    """The defining property, and the one a caller can overrule by accident:
    a refusing posture hands `textual_image` nothing. `pixels is None` is the
    commitment, not a gap — ledger and solari are exercising a decision."""
    for name in ("ledger", "solari"):
        res = LG.kit(name).raster_region(probe(), W, H)
        assert res.posture == "refuse"
        assert res.pixels is None, f"{name} refused and still produced pixels"
        assert RS.HALF not in text_of(res), f"{name} drew the image anyway"


def test_solari_refuses_by_showing_nothing():
    """Solari: "one shape, the row; an image cannot flip. If a board needs a
    picture it is not a departure board." Nothing means nothing.
    """
    res = LG.kit("solari").raster_region(probe(), W, H)
    assert text_of(res).strip() == ""


def test_ledger_audits_the_figure_instead_of_showing_it():
    """Ledger: "a figure is audited, not shown. At most one small ruled
    exhibit with dot leaders to its caption, like a receipt stapled to the
    page."
    """
    kit = LG.kit("ledger")
    res = kit.raster_region(probe(), 40, H, label="mbb rho")
    body = text_of(res)
    assert kit.RULE_V in body and kit.RULE_HEAD in body, "the exhibit is ruled"
    assert kit.LEAD * 3 in body, "the caption is reached by dot leaders"
    assert "MBB RHO" in body, "the exhibit states which figure it audits"
    assert "64 px" in body and "32 px" in body, "and its metrics"
    assert "shown" in body and "no" in body, "and that it is not shown"
    plain = [Text.from_markup(r).plain for r in res.rows]
    assert any(r.rstrip() != r for r in plain), (
        "a receipt is stapled to a page — it does not span the region")


def test_frame_is_a_heavy_box_around_untouched_pixels():
    """Neo-brutalist: "a raw image at full strength, hard edge, inside a heavy
    box — no smoothing, no caption softening it." No kit declares this token,
    so it is reached the way the mutation test reaches it."""
    img = probe()
    THEMES["nord"]["surface"] = "frame"
    try:
        res = LG.kit("nord").raster_region(img, W, H)
    finally:
        THEMES["nord"]["surface"] = "untinted"
    rows = [Text.from_markup(r).plain for r in res.rows]
    assert rows[0][0] == "╔" and rows[0][-1] == "╗"
    assert rows[-1][0] == "╚" and rows[-1][-1] == "╝"
    assert res.pixels is img, "frame does not smooth, tint or caption"


def test_depth_never_draws_a_border():
    """Darkside: "separates from its neighbours by ±1 grey step of BACKGROUND,
    NEVER a border." The literal reading is the checkable one."""
    for name in ("darkside", "prism"):
        res = LG.kit(name).raster_region(probe(), W, H)
        plain = text_of(res)
        drawn = set(plain) & set("┌┐└┘─│╔╗╚╝═║▀▄▌▐▛▜▙▟")
        assert drawn <= {RS.HALF}, f"{name} drew a border: {sorted(drawn)}"
        assert plain.strip(RS.HALF + " ") == "", f"{name} drew chrome"


def test_depth_separates_on_the_languages_own_grey_ladder():
    """The step is READ off the language (`focus`, the rung above `panel`),
    not invented as a delta — a second ladder beside the declared one would be
    two answers to one question."""
    kit = LG.kit("darkside")
    assert kit.depth_ground() == THEMES["darkside"]["focus"]
    assert kit.depth_ground() != THEMES["darkside"]["panel"], (
        "a step that lands on the ground it started from is not a step")
    assert f"on {kit.depth_ground()}" in kit.raster_region(probe(), W, H).rows[0]


def test_figure_is_never_full_bleed_and_always_captioned():
    """Swiss: "one image per screen, hairline rule and a caption in plain
    cells, NEVER FULL-BLEED — the magazine photograph, not the poster."
    """
    kit = LG.kit("swiss")
    res = kit.raster_region(probe(), W, H, label="mbb density field")
    plain = [Text.from_markup(r).plain for r in res.rows]
    assert all(r.endswith(" " * kit.GUTTER) for r in plain), (
        "the figure bleeds to the region's edge; swiss sets it in the gutter")
    rules = [r for r in plain if set(r.strip()) == {"─"}]
    assert len(rules) == 1, f"a hairline is ONE rule, got {len(rules)}"
    assert "mbb density field" in plain[-1], "the caption is the label given"
    assert RS.HALF not in plain[-1], "the caption is in PLAIN cells"


def test_figure_captions_itself_when_given_no_label():
    """A caption is not optional in this posture — a figure without one is a
    poster, which is exactly what swiss refuses."""
    res = LG.kit("swiss").raster_region(probe(), W, H)
    assert "64x32 px" in Text.from_markup(res.rows[-1]).plain


# --------------------------------------------------------------------------
# two languages, one mechanism, their own vocabulary (AC-2)
# --------------------------------------------------------------------------

def test_instrument_latticizes_in_braille_not_in_naughts_dots():
    """They share `lattice` and they must not share an alphabet: instrument
    declares `base="braille"`, and drawing naught's `∙`/`◦` here would put
    naught's identity on instrument's screen."""
    from taskboard import naught as NA
    kit = LG.kit("instrument")
    body = text_of(kit.raster_region(probe(), W, H))
    assert set(body) <= set(kit.LATTICE_GLYPHS), "non-braille in a braille lattice"
    assert NA.ON not in body and NA.OFF not in body, "borrowed naught's dots"
    assert kit.BLANK in body, "the unlit lattice must stay visible"
    assert kit.lattice_grid(W, H) == (W * 2, H * 4), "braille is 2x4 per cell"


def test_the_two_lattice_languages_do_not_render_identically():
    """The failure LANGUAGES.md records by name: "two of the eight languages
    rendered byte-identically". One shared mechanism must not mean one look."""
    img = probe()
    a = LG.kit("naught").raster_region(img, W, H)
    b = LG.kit("instrument").raster_region(img, W, H)
    assert a.blob() != b.blob()
    assert set(text_of(a)) & set(text_of(b)) <= {" "}, (
        "the two lattices share glyphs; one is wearing the other's alphabet")


def test_industrial_display_has_its_own_frame_and_no_colour_in_its_glass():
    """Corgi and industrial share `display` with their own frames (AC-2), and
    LANGUAGES.md is explicit that inside industrial's display "severity still
    cannot ride colour"."""
    ind, corgi = LG.kit("industrial"), LG.kit("corgi")
    assert ind.DISPLAY_BOX != corgi.DISPLAY_BOX
    res = ind.raster_region(probe(), W, H)
    rows = [Text.from_markup(r).plain for r in res.rows]
    assert rows[0][0] == "▛" and rows[-1][0] == "▙", "the stamped plate"
    seen = set(res.pixels.convert("RGB").getdata())
    assert all(c[0] == c[1] == c[2] for c in seen), (
        f"colour inside industrial's display: {sorted(seen)[:3]}")


@pytest.mark.parametrize("name", DECLARED)
def test_a_label_cannot_inject_markup_or_steal_a_cell(name):
    """Every captioning posture interpolates a caller's string into a MARKUP
    row (the codebase's pitfall A1). Escaping it changes the string's
    character count and not its cell count, so a mechanism that padded the
    ESCAPED string would silently hand back a rectangle one cell short —
    which is the kind of defect a reserved region cannot survive."""
    evil = "[bold red]x[/] [ ["
    res = LG.kit(name).raster_region(probe(), 40, H, label=evil)
    assert len(res.rows) == H
    bad = [(i, cells(r)) for i, r in enumerate(res.rows) if cells(r) != 40]
    assert not bad, f"{name}: a label moved the rectangle: {bad}"
    # A label that was escaped survives as LITERAL TEXT. A label that was
    # parsed disappears from the plain text (rich consumed it as a style) and
    # takes the row's colours with it — so presence, not absence, is the tell.
    # Whether this posture SHOWS a label is asked of the render, not of the
    # language's name: a benign marker either reaches the cells or it does
    # not. Solari refuses the label along with everything else, which is its
    # own commitment (`test_solari_refuses_by_showing_nothing`).
    marker = "ZQXJ"
    shown = LG.kit(name).raster_region(probe(), 40, H, label=marker)
    if marker in text_of(shown).upper():
        assert "[bold red]" in text_of(res).lower(), (
            f"{name}: the label was parsed as markup instead of printed")


# --------------------------------------------------------------------------
# the raster transport, reported rather than assumed
# --------------------------------------------------------------------------

def test_transport_is_reported_honestly():
    """`raster_available()` must not answer "yes" merely because a widget class
    exists — `textual_image` always gives one, and on a terminal with no
    transport that widget draws half-cells."""
    assert RS.TRANSPORT in ("none", "glyph", "sixel", "tgp")
    assert RS.raster_available() == (RS.TRANSPORT in ("sixel", "tgp"))


def test_widget_is_none_without_a_transport_and_never_for_a_refusal():
    res = LG.kit("nord").raster_region(probe(), W, H)
    if not RS.raster_available():
        assert res.widget() is None
    ghost = LG.RenderResult("refuse", [" " * W] * H, None, (W, H))
    assert ghost.widget() is None, "a refusing posture may never yield pixels"
