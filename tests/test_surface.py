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

from pathlib import Path

import pytest
from PIL import Image
from rich.console import Console
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


def flipped_probe() -> Image.Image:
    """`probe()` with its two halves exchanged — a DIFFERENT image of the SAME
    size. Same size because the captioning postures put the figure's metrics
    in their chrome, so a resize would move chrome legitimately and a test
    that read the move as leakage would be measuring its own probe."""
    w, h = 64, 32
    img = Image.new("RGB", (w, h))
    img.putdata([(20, 20, 20) if y < h // 2
                 else (255 - (x * 255 // w),) * 3
                 for y in range(h) for x in range(w)])
    return img


def sweep_image():
    """The image `capture_languages.py --surface` photographs, or None.

    Rebuilt here rather than imported for the reason that module's own header
    gives for rebuilding it: importing it drags in a Textual app. Returning
    None rather than raising is what lets the shipped-frame check SKIP with a
    reason on a machine that has neither numpy nor the other repo."""
    npy = Path(r"C:\Users\jjgh8\Github\tui-demos\lab\mbb_rho_final.npy")
    if not npy.exists():
        return None
    try:
        import numpy as np
    except ImportError:
        return None
    paper, ink, scale = (248, 246, 240), (28, 32, 44), 6
    g = np.clip(np.load(npy), 0, 1)[..., None]
    rgb = (np.array(paper, np.uint8) * (1 - g)
           + np.array(ink, np.uint8) * g).astype(np.uint8)
    img = Image.fromarray(rgb)
    return img.resize((img.width * scale, img.height * scale), Image.NEAREST)


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
def test_every_optional_argument_is_read_or_declared_refused(name):
    """L-31's GENERAL FORM: *an optional argument no implementation reads is
    not an argument, it is a comment.*

    `raster_region`'s one optional argument is `label`, documented as "what
    the figure IS, for the postures that caption or audit one". Blueprint's
    `tint` dropped it — so the sheet stated `480px` above the drawing and had
    no way to say those pixels were a 60 x 20 mesh, and the posture that
    captions HARDEST was the one that could not be told what it was
    captioning. Nothing caught it because "I decided not to caption" and "I
    forgot to caption" are the same code: `label=""` in the signature, and
    nothing in the body.

    So the argument must reach the render, OR the refusal must be DECLARED —
    and this asserts the declaration is true, in both directions. A posture in
    the table whose render moves is as much a failure as one outside it whose
    render does not: the first means the table is stale, the second means an
    argument went unread with no one saying so."""
    img = probe()
    posture = THEMES[name]["surface"]
    bare = LG.kit(name).raster_region(img, W, H).blob()
    told = LG.kit(name).raster_region(img, W, H, label="60 X 20 CELLS").blob()

    why = LG.LABEL_REFUSED_BY_LANGUAGE.get(name) or LG.LABEL_REFUSED.get(posture)
    if why is None:
        assert told != bare, (
            f"{name}: posture {posture!r} renders IDENTICAL bytes with and "
            f"without `label` — the argument is a comment. Either read it, or "
            f"declare the refusal in LABEL_REFUSED with the commitment it "
            f"follows from.")
    else:
        assert told == bare, (
            f"{name}: posture {posture!r} is declared to REFUSE the label "
            f"({why}) and the render moved anyway — the declaration is stale")


def test_the_declared_refusals_name_postures_that_exist():
    """A refusal table is only honest while its keys are real. A renamed
    posture would leave an entry excusing a mechanism that no longer exists,
    and the test above would then silently stop checking the one that does."""
    assert set(LG.LABEL_REFUSED) <= set(LG.LIVE_SURFACES), (
        sorted(set(LG.LABEL_REFUSED) - set(LG.LIVE_SURFACES)))
    assert set(LG.LABEL_REFUSED_BY_LANGUAGE) <= set(ORDER), (
        sorted(set(LG.LABEL_REFUSED_BY_LANGUAGE) - set(ORDER)))
    assert all(v.strip() for v in {**LG.LABEL_REFUSED,
                                   **LG.LABEL_REFUSED_BY_LANGUAGE}.values()), (
        "a refusal with no commitment behind it is a skip with better "
        "punctuation")


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


# --------------------------------------------------------------------------
# CHROME ON THE RASTER PATH (batch "chrome-on-raster", its AC-1 and AC-2)
#
# The numbering below belongs to THAT batch's spec, not to the AC-1..AC-7
# sections above, which are the `surface` batch's. Said here because the two
# sets of numbers meet in this one file and nothing else distinguishes them.
#
# The finding being closed (inc3 F-4): `rows` is chrome and image FUSED and
# `pixels` is the glass alone, so a consumer that draws the true raster has
# nothing to draw corgi's `[1] DISPLAY` box or blueprint's spans from. The
# fix is `image_box` — where the glass went — and `chrome`, which is `rows`
# with that rectangle punched out. `rows` itself does not move.
# --------------------------------------------------------------------------

GALLERY = Path(__file__).resolve().parents[1] / "prototypes" / "gallery"

#: the sweep's own geometry, from `capture_languages.py`. Repeated rather than
#: imported: importing that module pulls in numpy and a Textual app to read two
#: integers, and it is those integers the shipped frames were rendered at.
SHEET_W, SHEET_H = 116, 26
SHEET_LABEL = "mbb rho final"


def cellwise(row: str) -> list[tuple[str, str]]:
    """A markup row as a list of (character, resolved style) per CELL.

    Comparing rendered rows by their markup strings would call two rows
    different because one says `[/]` where the other says `[/red]`. What a
    reader sees is the cell, so the cell is what is compared — and the style
    is carried along because these rows are half-blocks, whose glyph is `▀`
    everywhere and whose entire content is colour."""
    t = Text.from_markup(row)
    return [(t.plain[i], str(t.get_style_at_offset(Console(), i)))
            for i in range(len(t.plain))]


def boxed(res) -> tuple[int, int, int, int]:
    assert res.image_box is not None, f"{res.posture} has no image box"
    return res.image_box


@pytest.mark.parametrize("name", DECLARED)
def test_chrome_is_rows_with_the_image_cells_punched_out(name):
    """AC-1, cell by cell. Inside `image_box` every chrome cell is the hole;
    outside it every chrome cell is the SAME cell `rows` drew — character and
    style. That second half is the load-bearing one: a `chrome` that redrew
    the frame from its own idea of the language would satisfy "there is a
    frame" and could still disagree with the rendering it claims to describe.
    """
    res = LG.kit(name).raster_region(probe(), W, H, label=SHEET_LABEL)
    if res.posture == "refuse":
        pytest.skip("refuse has no box; asserted by its own test")
    x, y, bw, bh = boxed(res)
    assert len(res.chrome) == H, "chrome lost a row of the reserved rectangle"
    bad = [(i, cells(r)) for i, r in enumerate(res.chrome) if cells(r) != W]
    assert not bad, f"{name}: chrome rows not {W} cells wide: {bad}"

    for i, (crow, rrow) in enumerate(zip(res.chrome, res.rows)):
        c, r = cellwise(crow), cellwise(rrow)
        assert len(c) == len(r) == W
        inside = range(x, x + bw) if y <= i < y + bh else range(0, 0)
        for j in range(W):
            if j in inside:
                assert c[j][0] == LG.RASTER_HOLE, (
                    f"{name}: chrome[{i}][{j}] is inside the image box and is "
                    f"{c[j][0]!r}, not the hole")
            else:
                assert c[j] == r[j], (
                    f"{name}: chrome[{i}][{j}] is outside the image box and "
                    f"differs from rows: {c[j]!r} != {r[j]!r}")


@pytest.mark.parametrize("name", DECLARED)
def test_the_image_box_names_the_image_and_nothing_else(name):
    """The box is only worth having if it is TRUE, and "true" is checkable
    without trusting any glyph alphabet: render the same region twice with two
    DIFFERENT images of the same size, and the cells that move are the image.

    Every cell that moves must lie inside the box — a box that were too small
    or misplaced would leak — and cells inside it must actually move, or the
    box would be a claim about a region that carries nothing. The two probes
    are the same SIZE on purpose: swiss captions its figure's metrics and
    blueprint spans them, so a different-sized image would legitimately change
    chrome outside the box and the check would be measuring the wrong thing.
    """
    kit = LG.kit(name)
    a = kit.raster_region(probe(), W, H, label=SHEET_LABEL)
    b = kit.raster_region(flipped_probe(), W, H, label=SHEET_LABEL)
    if a.posture == "refuse":
        assert [cellwise(r) for r in a.rows] == [cellwise(r) for r in b.rows], (
            f"{name} refused and still tracked the image")
        return
    x, y, bw, bh = boxed(a)
    ca = [cellwise(r) for r in a.rows]
    cb = [cellwise(r) for r in b.rows]
    outside = [(i, j) for i in range(H) for j in range(W)
               if not (y <= i < y + bh and x <= j < x + bw)
               and ca[i][j] != cb[i][j]]
    assert not outside, (
        f"{name}: the image reached cells OUTSIDE image_box {a.image_box}: "
        f"{outside[:6]} — the box does not name the glass")
    moved = sum(1 for i in range(y, y + bh) for j in range(x, x + bw)
                if ca[i][j] != cb[i][j])
    # A FLOOR, NOT A TARGET, and it cannot be "all of it": naught's lattice
    # draws unlit grid air INSIDE the image (that air is the posture's whole
    # commitment) and a duotone maps many source values onto one cell, so a
    # correct box legitimately holds cells that two different images agree on.
    # Measured across the eight rendering postures at this size on 2026-09-04:
    # naught 88/192 is the floor, every other posture is 88-96 %. A quarter
    # sits clear of the real minimum and still fails a box that names nothing.
    assert moved > bw * bh // 4, (
        f"{name}: only {moved} of {bw * bh} cells inside image_box changed "
        f"when the image did — the box does not name the glass either")


def test_refusing_postures_have_no_box_and_their_chrome_is_the_rendering():
    """AC-2. `None`, never a zero-size rectangle, and `chrome` is `rows`
    ITSELF — the same object, because there is nothing to derive: no glass
    means no hole, and a copy would only invite one of the two to drift."""
    for name in ("ledger", "solari"):
        res = LG.kit(name).raster_region(probe(), 40, H, label=SHEET_LABEL)
        assert res.posture == "refuse"
        assert res.image_box is None, (
            f"{name} refuses the image and still offered a box: "
            f"{res.image_box!r}")
        assert res.chrome is res.rows, (
            f"{name}: a refusing posture's chrome is its rendering")


#: THE ONE PAIR OF POSTURES THAT SHARE A FRAME, named rather than skipped.
#: `untinted` and `lattice` are both full-bleed and frameless — their image box
#: is the whole reserved rectangle — so their chrome is nothing but holes and
#: the two are identical by construction, for every language. That is not a
#: hole in the mutation check, it is the check reporting a real property: the
#: postures differ entirely in what they do to the GLASS (`nord` hands the
#: pixels over untouched, `naught` quantises them onto its dot grid) and not at
#: all in what they draw around it, because neither draws anything around it.
#: Measured over all eleven languages on 2026-09-04: this is the ONLY pair
#: whose chrome collides, and no language's own posture collides with any other
#: except through it.
FRAME_TWINS = frozenset({"untinted", "lattice"})


@pytest.mark.parametrize("name", DECLARED)
def test_mutation_changes_the_chrome_too(name):
    """AC-5's limb. The 77-swap table above proves the token is dispatched;
    this proves it reaches the SURFACE THE FRAME IS ON. Without it a posture
    could differ from every other only in its glass and still be reported as a
    distinct posture to a consumer that draws chrome — which is precisely the
    consumer F-4 exists for.

    The `FRAME_TWINS` exception is NAMED rather than skipped: a skip would
    hide the day a third posture went frameless by accident. Here, a collision
    with any posture outside that pair fails, and a collision *within* it is
    asserted to still be there — so the exception cannot silently widen."""
    kit_probe = probe()
    original = THEMES[name]["surface"]

    def chrome_of(posture: str) -> str:
        THEMES[name]["surface"] = posture
        return "\n".join(
            LG.kit(name).raster_region(kit_probe, W, H, label="fig").chrome)

    try:
        got = {p: chrome_of(p) for p in LG.LIVE_SURFACES}
    finally:
        THEMES[name]["surface"] = original

    for other in (p for p in LG.LIVE_SURFACES if p != original):
        collided = got[other] == got[original]
        twins = {original, other} == FRAME_TWINS
        if twins:
            assert collided, (
                f"{name}: {original!r} and {other!r} are the declared frame "
                f"twins and their chrome now DIFFERS — one of them grew a "
                f"frame, and the exception above is out of date")
        else:
            assert not collided, (
                f"{name}: swapping surface {original!r} -> {other!r} left the "
                f"CHROME identical — the frame does not follow the token")


@pytest.mark.parametrize("name", DECLARED)
def test_no_language_can_draw_the_hole_itself(name):
    """The sentinel only means "do not paint" if nothing else can say it. Every
    glyph these languages draw comes from a declared alphabet and none of them
    reaches the Private Use Area — asserted rather than assumed, because the
    obvious sentinel (a space) fails exactly this check: swiss pads its gutter
    with real spaces."""
    res = LG.kit(name).raster_region(probe(), W, H, label=SHEET_LABEL)
    assert LG.RASTER_HOLE not in text_of(res), (
        f"{name} drew the transparent sentinel as ordinary content")


@pytest.mark.parametrize("name", DECLARED)
def test_chrome_preserves_the_frame_the_shipped_capture_shows(name):
    """AC-1 against the ARTEFACT, not only against a synthetic probe.

    `surface_<lang>.txt` is what a reader of the skill actually looks at, and
    the whole point of F-4 is that the frame visible THERE — corgi's boxed
    `[1] DISPLAY`, blueprint's `360px`/`120px` spans, swiss's hairline and
    caption — never reached the raster path. So the check is run against that
    file: at the sweep's own geometry, `rows` must be the frame the capture
    shows, and every cell of it that is not glass must survive into `chrome`.

    Skipped, loudly, when the sweep's inputs are absent: the test image is a
    `.npy` in another repo and numpy is not a dependency of this package."""
    img = sweep_image()
    if img is None:
        pytest.skip("sweep image unavailable (numpy or the .npy is missing)")
    shipped = GALLERY / f"surface_{name}.txt"
    if not shipped.exists():
        pytest.skip(f"{shipped.name} not captured; run capture_languages.py "
                    f"--surface")
    kit = LG.kit(name)
    res = kit.raster_region(img, SHEET_W, SHEET_H, label=SHEET_LABEL)
    head = kit.sect("SURFACE", f"{res.posture} - {img.width}x{img.height} px",
                    SHEET_W, SHEET_H)
    grid = shipped.read_text(encoding="utf-8").splitlines()

    # the sheet is `head + rows`, drawn in a Static with one cell of padding
    frame = [grid[len(head) + i][1:1 + SHEET_W] for i in range(SHEET_H)]
    drawn = [Text.from_markup(r).plain for r in res.rows]
    assert frame == drawn, (
        f"{name}: the shipped capture is not what raster_region renders — "
        f"the frames are stale, or the geometry moved")

    holes = [Text.from_markup(r).plain for r in res.chrome]
    if res.image_box is None:
        assert holes == frame, f"{name} refused; chrome is the frame"
        return
    x, y, bw, bh = res.image_box
    for i in range(SHEET_H):
        keep = (frame[i] if not (y <= i < y + bh)
                else frame[i][:x] + LG.RASTER_HOLE * bw + frame[i][x + bw:])
        assert holes[i] == keep, (
            f"{name}: chrome row {i} is not the shipped frame with the glass "
            f"punched out")
