"""The COMPONENT CONTRACT in the pytest suite — batch `kits-learn-3`.

Until this file the contract was asserted only by `prototypes/verify_language.py`,
which pytest does not run: 2178 checks that go red in a script nobody's gate
executes. The six primitives the operator ruled on (2026-09-04) are new
SURFACE, so they get a seat where the gate can see them.

WHAT KIND OF TEST LIVES HERE. Every test in this file is a PROPERTY test, not
a mutation test, and the distinction is the one `kits-learn-2` had to learn the
hard way: "swap the token and the render moves" proves a token is READ; it does
not prove it is read CORRECTLY. So these ask the second question — is the state
distinguishable with the colour taken away, do five languages actually differ,
does the caller's text come back byte for byte — and they ask it of ALL ELEVEN
languages rather than of the five that happened to be prototyped, because a
contract seat with six implementations and five holes is a hand list waiting to
happen.
"""
from __future__ import annotations

import pathlib
import re

import pytest

from taskboard import language as LG

LANGS = tuple(LG.KITS)
#: where `prototypes/components/render.py` writes its sweep. Reached as a path
#: and not imported: that module pulls `capture_languages` and Textual, and the
#: only question this file asks of it is which frames exist on disk.
FRAMES = pathlib.Path(__file__).resolve().parents[1] / "prototypes" / "components"
#: where `prototypes/components/render.py` writes its sweep. Reached as a path
#: and not imported: that module pulls `capture_languages` and Textual, and the
#: only question this file asks of it is which frames exist on disk.
FRAMES = pathlib.Path(__file__).resolve().parents[1] / "prototypes" / "components"
#: where `prototypes/components/render.py` writes its sweep. Reached as a path
#: and not imported: that module pulls `capture_languages` and Textual, and the
#: only question this file asks of it is which frames exist on disk.
FRAMES = pathlib.Path(__file__).resolve().parents[1] / "prototypes" / "components"
#: the five the PROTOTYPE round rendered; the others inherit the seat, and the
#: laws below are asked of ALL of them either way
PROTOTYPED = ("corgi", "blueprint", "prism", "naught", "ledger")
#: the six the PROTOTYPE round never rendered, which is why they inherited
#: seat after seat from `Kit` -- inc32 gave them seven mechanisms, inc35 and
#: inc36 the last two. Declared here beside `PROTOTYPED` because both halves
#: of the eleven are read from the first law onward.
INHERITORS = ("instrument", "swiss", "industrial", "nord", "darkside",
              "solari")

_ESC = "\x00"
_TAG = re.compile(r"\[[^\]]*\]")


def plain(s: str) -> str:
    """The CELLS a markup row will occupy, colour removed at the source.

    `mark()` escapes a literal `[` as `\\[`, so the two substitutions must
    happen in this order or an escaped bracket is read as a style tag — the
    module's own documented pitfall A1, applied to the oracle instead of to
    the renderer."""
    return _TAG.sub("", s.replace("\\[", _ESC)).replace(_ESC, "[")


def shape(cells) -> str:
    """A component render with the tone channel DELETED rather than filtered:
    the cells carry their own tone, so joining the glyphs is a projection and
    not a regex over a coloured string."""
    return "".join(g for _, g, _ in cells)


# ===========================================================================
# inc14 — INVALID, the sixth derived control state (ruling 1)
# ===========================================================================
INVALID_TAKERS = ("slider", "textfield", "stepper")
INVALID_REFUSERS = ("bar", "scrollbar", "button",
                    "switch", "checkbox", "radio")


def test_invalid_is_derived_from_the_registry_and_not_hand_listed():
    """The axis is DERIVED, and a NEW component proves it.

    Four probe components are registered, none of which any language has ever
    heard of, and the derivation answers for all four with nothing hand-listed
    anywhere: an actuator plus an interior takes INVALID, a readout does not
    (no actuator), a valueless control does not (no interior), and a checkable
    does not (its range is boolean, so both of its values are legal).

    This is the test that a `INVALID_COMPONENTS = ("slider", ...)` tuple would
    fail, which is precisely why there isn't one."""
    probes = {
        "_p_knobbed": ("main", "indicator", "knob"),      # settable
        "_p_flat": ("main", "indicator"),                 # readout
        "_p_bare": ("main",),                             # button-shaped
        "_p_field": ("main", "caret"),                    # settable, no extent
    }
    LG.COMPONENT_PARTS.update(probes)
    try:
        assert LG.INVALID in LG.component_states("_p_knobbed")
        assert LG.INVALID in LG.component_states("_p_field")
        assert LG.INVALID not in LG.component_states("_p_flat")
        assert LG.INVALID not in LG.component_states("_p_bare")
        # and the CHECKABLE limb, on the same probe that just took it
        LG.CHECKABLE = LG.CHECKABLE + ("_p_knobbed",)
        assert LG.INVALID not in LG.component_states("_p_knobbed")
    finally:
        LG.CHECKABLE = tuple(n for n in LG.CHECKABLE
                             if not n.startswith("_p_"))
        for n in probes:
            del LG.COMPONENT_PARTS[n]


def test_invalid_reaches_exactly_the_components_that_take_edited():
    """ONE SENTENCE, ASSERTED: what the arrows can change, the form can
    reject. If the two axes ever come apart, one of them grew a special case
    and this is where it is named."""
    for name in LG.COMPONENT_PARTS:
        assert ((LG.INVALID in LG.COMPONENT_STATES[name])
                == (LG.EDITED in LG.COMPONENT_STATES[name])), name
    assert all(LG.INVALID in LG.COMPONENT_STATES[n] for n in INVALID_TAKERS)
    assert all(LG.INVALID not in LG.COMPONENT_STATES[n]
               for n in INVALID_REFUSERS)


def test_invalid_is_in_the_state_axis_once_and_in_order():
    assert LG.STATES.count(LG.INVALID) == 1
    assert LG.STATES.index(LG.INVALID) > LG.STATES.index(LG.ACTIVE)
    assert LG.STATES.index(LG.INVALID) < LG.STATES.index(LG.DISABLED)


@pytest.mark.parametrize("lang", LANGS)
def test_invalid_survives_greyscale_in_every_language(lang):
    """THE PROPERTY: with the colour removed, INVALID is distinguishable from
    every other state of the same component, in every language.

    Not "the render moved" — moved from WHAT? A language that declared an
    invalid mark identical to its disabled one would satisfy a diff against
    DEFAULT and tell a user with a dead field that it is a wrong one. So the
    render is compared against EVERY state the registry derives, pairwise, on
    the glyph channel alone.

    The failure mode this is written against is a MISS rather than a mistake:
    `part_glyph` falls back along the state chain, so a language that simply
    forgot to declare INVALID renders it as DEFAULT and reads as "fine". That
    silence is what goes red here."""
    k = LG.kit(lang)
    for name in INVALID_TAKERS:
        states = LG.COMPONENT_STATES[name]
        if name == "textfield":
            got = {s: plain(k.textfield("task", 2, 12, s)) for s in states}
        elif name == "stepper":
            got = {s: plain(k.stepper(("alpha", "beta", "gamma"), 1, 7, s))
                   for s in states}
        else:
            got = {s: shape(k.component_cells(name, 5, 0, 10, 12, s))
                   for s in states}
        assert got[LG.INVALID] != got[LG.DEFAULT], (lang, name)
        assert got[LG.INVALID] != got[LG.DISABLED], (lang, name)
        assert len(set(got.values())) == len(states), (
            lang, name, sorted(set(got.values())))


@pytest.mark.parametrize("lang", LANGS)
def test_the_invalid_mark_is_shape_and_costs_no_hue(lang):
    """Colour is NOT the channel, and that is a decision rather than an
    omission (spec §6.2). Two of these languages have already spent their
    alert hue on something a control borrowing it would break — ledger's on
    literal debt, blueprint's on overdue — so the state is asserted to leave
    the tone channel exactly where DEFAULT leaves it.

    If a later pass decides an invalid control should also carry the alert,
    this test is the seat that has to be argued with."""
    k = LG.kit(lang)
    for name in INVALID_TAKERS:
        tones_d = [t for _, _, t in
                   k.component_cells(name, 5, 0, 10, 12, LG.DEFAULT)]
        tones_i = [t for _, _, t in
                   k.component_cells(name, 5, 0, 10, 12, LG.INVALID)]
        assert tones_d == tones_i, (lang, name)


@pytest.mark.parametrize("lang", LANGS)
def test_an_invalid_field_still_returns_its_value_byte_for_byte(lang):
    """The CONTENT law (L-33 / inc12) does not lapse because the value is
    wrong. A field that hid, truncated or recased a rejected value would be
    editing the user's text as a way of complaining about it."""
    k = LG.kit(lang)
    bad = "31/02/2026"
    assert bad in plain(k.textfield(bad, None, 20, LG.INVALID)), lang


# ===========================================================================
# inc15 — Kit.field_row, the definition row (ruling 2)
# ===========================================================================
CAP, VAL, FW = "due date", "12/09/26", 40


@pytest.mark.parametrize("lang", LANGS)
def test_a_field_row_is_exactly_the_width_it_was_asked_for(lang):
    """The rectangle law, at the one seat most likely to break it: this row
    interpolates TWO caller strings and pads between them, and `mark()`
    escapes a `[` into two characters that occupy one cell (pitfall A1). A row
    that did its arithmetic on the escaped string comes back one cell short
    per bracket, and in a `Static` a short row does not look wrong — it looks
    like a design decision."""
    k = LG.kit(lang)
    assert len(plain(k.field_row(CAP, VAL, FW))) == FW, lang
    assert len(plain(k.field_row("a[b]c", "x[y]", FW))) == FW, lang


@pytest.mark.parametrize("lang", LANGS)
def test_a_field_row_returns_its_figure_byte_for_byte(lang):
    """THE VALUE IS CONTENT (L-33 / inc12), and a definition row is where a
    language is most tempted to letter it: three of these languages set their
    captions in capitals, and the figure sits right beside the caption."""
    k = LG.kit(lang)
    for val in (VAL, "hi", "Q3 -1,204.55", "AbCd"):
        assert val in plain(k.field_row(CAP, val, FW)), (lang, val)


@pytest.mark.parametrize("lang", LANGS)
def test_a_field_row_never_truncates_the_figure(lang):
    """`w` IS A MINIMUM FOR THE FIGURE, the stepper's rule for the stepper's
    reason: a row that shortened a number to fit would be lying about it. The
    row is allowed to come back WIDER than asked; it is not allowed to come
    back with less of the value than it was given."""
    k = LG.kit(lang)
    long_val = "2026-09-04T11:22:33.4455Z"
    row = plain(k.field_row(CAP, long_val, 12))
    assert long_val in row, lang


@pytest.mark.parametrize("lang", LANGS)
def test_a_field_rows_caption_keeps_its_letters(lang):
    """The caption is a LABEL and a label is notation, so a language may
    letter it — corgi engraves, ledger and blueprint print in capitals. What
    no language may do is drop it, cut it, or spell it differently."""
    k = LG.kit(lang)
    row = plain(k.field_row(CAP, VAL, FW))
    assert CAP.lower() in row.lower(), lang


def test_five_languages_return_five_different_rows():
    """THE PROPERTY, and the whole reason this primitive exists.

    Before it, all five frames drew LEDGER's mechanism — dot leaders — because
    the prototype had to pick one and ledger's was the only one written down.
    One language's signature generalised into four is the palette-swap failure
    with a leader instead of a hue.

    Same caption, same value, same width, five rows that differ AS CELLS: air
    to a right column (nord's terminal list), an engraved silkscreen (corgi),
    a dimension (blueprint), an ember frontier (prism), an unlit lattice
    (naught), dot leaders (ledger). Compared on the PLAIN text rather than on
    the markup, because two rows that differ only in a colour token are two
    recolours and this test would then pass on exactly the defect it names."""
    rows = {n: plain(LG.kit(n).field_row(CAP, VAL, FW)) for n in PROTOTYPED}
    assert len(set(rows.values())) == len(PROTOTYPED), rows


def test_no_language_borrows_ledgers_leaders():
    """The anti-palette-swap law, made falsifiable rather than promised.

    Ledger's mechanism is the dot leader and it is ledger's ALONE: it is the
    typographic argument that language is built on ("every gap between a name
    and its figure closes with dot leaders"). Any other language whose row
    contains a run of that mark is drawing ledger's answer, which is the exact
    defect the PROTOTYPE round reported."""
    lead_run = LG.kit("ledger").LEAD * 3
    assert lead_run in plain(LG.kit("ledger").field_row(CAP, VAL, FW))
    for lang in LANGS:
        if lang == "ledger":
            continue
        assert lead_run not in plain(LG.kit(lang).field_row(CAP, VAL, FW)), lang


def test_naughts_row_fills_after_the_figure_and_never_between():
    """The structural difference between a LATTICE and a LEADER, asserted.

    A leader connects two marks, so it lives BETWEEN them; a lattice is a
    ground that was already there, so it lives wherever ink is not. Naught's
    figure therefore sits immediately after its caption and the remainder of
    the row is unlit grid — take that away and this language is drawing
    ledger's row with a rounder dot."""
    from taskboard import naught as NA
    row = plain(LG.kit("naught").field_row(CAP, VAL, FW))
    assert row.startswith(f"{CAP} {VAL} "), row
    assert row.endswith(NA.OFF), row
    assert NA.OFF not in row[:len(CAP) + len(VAL) + 2], row


# ===========================================================================
# inc16 — Kit.select, Kit.menu (ruling 7) and button(danger=True) (ruling 6)
# ===========================================================================
OPTS = ("low", "normal", "high")


@pytest.mark.parametrize("lang", LANGS)
def test_a_select_is_not_a_stepper(lang):
    """THE PROPERTY of ruling 7, and the reason the ruling was needed: the
    PROTOTYPE round drew the closed select AS a stepper, because that was the
    nearest thing the contract had.

    They answer different questions. A stepper shows THE TWO WAYS OFF a value
    — its steps are the ± of a set moved through in place. A select shows THE
    ONE WAY INTO a list — its disclosure is a door. A select drawn as a
    stepper tells the user the arrow keys will change the setting, which in a
    select they do not: they open it."""
    k = LG.kit(lang)
    assert plain(k.select(OPTS, 2, 7)) != plain(k.stepper(OPTS, 2, 7)), lang


@pytest.mark.parametrize("lang", LANGS)
def test_a_select_shows_the_chosen_word_byte_for_byte(lang):
    k = LG.kit(lang)
    for i, word in enumerate(OPTS):
        assert word in plain(k.select(OPTS, i, 7)), (lang, word)


@pytest.mark.parametrize("lang", LANGS)
def test_a_selects_edges_do_not_move_when_the_choice_does(lang):
    """Bodmer T2, reserve the widest form: the field is sized for the widest
    option in the set, so spinning through the set cannot reflow the row that
    holds it. A control whose width follows its value makes every row beside
    it move, and in a settings screen that is every row."""
    k = LG.kit(lang)
    widths = {len(plain(k.select(OPTS, i, 7))) for i in range(len(OPTS))}
    assert len(widths) == 1, (lang, widths)


@pytest.mark.parametrize("lang", LANGS)
def test_a_select_refuses_an_index_the_set_does_not_have(lang):
    """One choice model, three mechanisms: `radio_group`, `stepper` and now
    `select` all reach `group_states`, so all three refuse the same index in
    the same seat. A select that quietly clamped would be inventing a choice
    the caller did not make."""
    k = LG.kit(lang)
    with pytest.raises(Exception):
        k.select(OPTS, 7, 7)


@pytest.mark.parametrize("lang", LANGS)
def test_a_menu_is_one_row_per_option_with_exactly_one_marked(lang):
    k = LG.kit(lang)
    rows = k.menu(OPTS, 1, 9)
    assert len(rows) == len(OPTS), lang
    marked = [r for r in rows if plain(r).startswith(k.CUR)]
    assert len(marked) == 1 and OPTS[1] in plain(marked[0]), lang


@pytest.mark.parametrize("lang", LANGS)
def test_a_menu_is_a_list_and_not_a_surface(lang):
    """A MENU IS NOT A MODAL, so no language draws a frame around one —
    including the one language whose commitment licenses a border, because
    prism's borders are reserved for MODALS and a dropdown is not one.

    Asserted on the LID and the WALL rather than on corner glyphs, and the
    difference is a finding: blueprint's cursor IS a registration corner
    (`┌`), because four corners that never join is that language's selection
    mechanism. A corner is not a box. What makes a box is a lid — a run of
    rule between two corners — or a vertical stroke, and four of these eleven
    languages have a commitment that makes both unconstructable."""
    k = LG.kit(lang)
    for row in k.menu(OPTS, 1, 9):
        got = plain(row)
        assert not (set(got) & set("│┃║╎╏┆┇")), (lang, "wall", row)
        assert not any(r * 3 in got for r in "─━═╌"), (lang, "lid", row)


@pytest.mark.parametrize("lang", LANGS)
def test_danger_survives_greyscale_in_every_language(lang):
    """THE PROPERTY of ruling 6: severity on a control, read with the colour
    taken away, in EVERY language — including the two whose alert hue was
    already spent on something a button borrowing it would break (ledger's on
    literal debt, blueprint's on overdue).

    Compared against the ordinary button of the same label and width, because
    "the danger button looks different from a checkbox" would prove nothing:
    the question is whether the same control at the same size says something
    different when it is about to destroy something."""
    k = LG.kit(lang)
    ordinary = plain(k.button("Delete", 12))
    danger = plain(k.button("Delete", 12, danger=True))
    assert ordinary != danger, lang


@pytest.mark.parametrize("lang", LANGS)
def test_danger_costs_no_hue_at_all(lang):
    """The form is the WHOLE channel. Not "colour plus a glyph" — no colour,
    which is stronger than the law requires and is the only version that
    survives contact with a language that has already spent its alert."""
    k = LG.kit(lang)
    tags = lambda s_: _TAG.findall(s_.replace("\\[", _ESC))
    assert tags(k.button("Delete", 12)) == tags(
        k.button("Delete", 12, danger=True)), lang


@pytest.mark.parametrize("lang", LANGS)
def test_a_danger_button_still_returns_its_label_byte_for_byte(lang):
    """The label is content and severity does not license editing it — the
    button's oldest ruling, asked again at the one call that adds marks
    around the word."""
    k = LG.kit(lang)
    assert "Delete 7 tasks" in plain(
        k.button("Delete 7 tasks", 20, danger=True)), lang


def test_ledgers_danger_is_the_contra_entry_and_not_a_refusal():
    """Operator ruling 6, and the retraction it carries.

    The PROTOTYPE round had ledger REFUSING a destructive control on the
    genre's rule ("nothing is deleted, everything is balanced"). The operator
    ruled that the refusal is retracted and the answer is a SHAPE: a ledger
    writes a reversing figure IN PARENTHESES — the notation its own genre has
    used for centuries for an amount that takes something away.

    So ledger's danger button is neither refused nor tinted: it is bracketed,
    and this test is what that ruling looks like as code."""
    k = LG.kit("ledger")
    assert "(Delete)" in plain(k.button("Delete", 12, danger=True))
    assert plain(k.button("Delete", 12)) != plain(
        k.button("Delete", 12, danger=True))


def test_five_languages_show_five_danger_forms():
    """The anti-palette-swap law again, on severity: a `!` in five languages
    is the same defect as a red `!` in five languages."""
    forms = {n: plain(LG.kit(n).button("Delete", 12, danger=True))
             for n in PROTOTYPED}
    assert len(set(forms.values())) == len(PROTOTYPED), forms


# ===========================================================================
# inc17 — Kit.overlay and the refusal registry (rulings 4, 5, 10)
# ===========================================================================
UNDER = [f"row {i} of the board" for i in range(24)]
DIALOG_W, DIALOG_H = 60, 12


def dialog(k):
    return [LG.mark("Delete 3 tasks?"), "",
            k.button("Delete", 10) + "   " + k.button("Cancel", 10)]


def has_lid(rows) -> bool:
    """A LID: two corner marks with a RUN OF RULE between them. That is what
    makes a box, and it is what four of these languages have committed
    against — not the corner, which blueprint spends on every selection it
    draws, and not the rule, which ledger rules across the whole measure on
    every page."""
    import re as _re
    return any(_re.search(r"[┌└╔╚][─━═╌]{2,}[┐┘╗╝]", plain(r)) for r in rows)


def test_the_refusal_registry_names_languages_that_exist():
    """A declared refusal that names nothing is a comment with a dict around
    it. This is `LABEL_REFUSED`'s own law, asked of the second table to use
    the pattern."""
    assert set(LG.MODAL_BORDER_REFUSED) <= set(LG.KITS)
    # SEVEN, not four: `kits-learn-4` inc32 asked the six inheriting
    # languages and three of them turned out to have been committed against a
    # lid all along while drawing the terminal's.
    assert set(LG.MODAL_BORDER_REFUSED) == {"corgi", "blueprint", "naught",
                                            "ledger", "instrument", "swiss",
                                            "solari"}
    assert all(len(v) > 40 for v in LG.MODAL_BORDER_REFUSED.values())


def test_prism_is_the_one_language_licensed_to_draw_the_box():
    """Operator ruling 5. Prism's commitment is the only one of the eleven
    that names this component as its exception — "depth by one grey step,
    never borders: borders are RESERVED for modals" — so it is absent from
    the registry and it draws the lid."""
    assert "prism" not in LG.MODAL_BORDER_REFUSED
    k = LG.kit("prism")
    assert has_lid(k.overlay(dialog(k), DIALOG_W, DIALOG_H, UNDER))


@pytest.mark.parametrize("lang", sorted(LG.MODAL_BORDER_REFUSED))
def test_a_refusing_language_draws_no_lid(lang):
    """Parametrised on the REGISTRY rather than on a copy of it, so a
    language added to the table is checked the moment it is added. The
    table's own membership is asserted above, which is what keeps this from
    passing vacuously if the table ever emptied."""
    k = LG.kit(lang)
    out = k.overlay(dialog(k), DIALOG_W, DIALOG_H, UNDER)
    assert not has_lid(out), (lang, [plain(r) for r in out])


@pytest.mark.parametrize("lang", LANGS)
def test_an_overlay_returns_the_rectangle_it_was_asked_for(lang):
    """`h` rows, always. A composition that returned fewer would push
    everything under it up the screen, which in a full-frame render is the
    one failure that still looks like a design."""
    k = LG.kit(lang)
    assert len(k.overlay(dialog(k), DIALOG_W, DIALOG_H, UNDER)) == DIALOG_H


def test_the_registry_is_read_and_not_printed():
    """THE TEETH, both ways — this is the test that makes the table a
    mechanism rather than a note.

    Take naught OUT of the registry and it draws the terminal's box, which is
    a direct violation of one of its four commitments. Put prism IN and the
    one language licensed to draw a border stops. Neither language's code is
    touched in either direction: the table is what decides."""
    k_n, k_p = LG.kit("naught"), LG.kit("prism")
    saved = dict(LG.MODAL_BORDER_REFUSED)
    try:
        del LG.MODAL_BORDER_REFUSED["naught"]
        assert has_lid(k_n.overlay(dialog(k_n), DIALOG_W, DIALOG_H, UNDER))
        LG.MODAL_BORDER_REFUSED["prism"] = "a false refusal, for one assert"
        assert not has_lid(k_p.overlay(dialog(k_p), DIALOG_W, DIALOG_H, UNDER))
    finally:
        LG.MODAL_BORDER_REFUSED.clear()
        LG.MODAL_BORDER_REFUSED.update(saved)


def test_corgis_confirm_takes_the_screen_and_leaves_nothing_behind():
    """"The mode takes over the screen." A dialog floating over a board is
    two modes at once, so the backdrop is not dimmed — it is GONE. The
    argument is accepted and dropped, and that dropping IS the refusal."""
    k = LG.kit("corgi")
    out = k.overlay(dialog(k), DIALOG_W, DIALOG_H, UNDER)
    assert not any("row 0 of the board" in plain(r) for r in out)
    # and the question is CENTRED on the panel: a mode is not a dialog that
    # lost its box, it is the whole glass, so the question sits in the middle
    # of it rather than in the corner a window would start from.
    assert any("Delete 3 tasks?" in plain(r) for r in out)
    assert plain(out[0]).strip() == ""


def test_ledgers_confirm_is_posted_on_the_page_that_stays_legible():
    """"Nothing is deleted, everything is balanced", and a ledger has no
    surface IN FRONT OF the page. The question is posted at the foot, under a
    rule, and the entries above it are kept AT FULL STRENGTH — the exact
    opposite of every other answer here. Dimming them would be the language
    claiming those postings are less true while a question is open."""
    k = LG.kit("ledger")
    out = k.overlay(dialog(k), DIALOG_W, DIALOG_H, UNDER)
    assert out[0] == UNDER[0], out[0]
    assert "Delete 3 tasks?" in plain(out[-3])


def test_naughts_separation_is_charge_and_not_a_frame():
    """Operator ruling 4. The page keeps every dot it had and loses its
    CHARGE; the question is the only region left lit, bounded by the lattice
    at full charge. No box, no scrim, no mark laid in front of anything."""
    from taskboard import naught as NA
    k = LG.kit("naught")
    out = k.overlay(dialog(k), DIALOG_W, DIALOG_H, UNDER)
    lit = [r for r in out if plain(r) and plain(r).strip(NA.ON) == ""]
    assert len(lit) == 2, [plain(r) for r in out]
    assert all(k.c["ink"] in r for r in lit)
    backdrop = [r for r in out if "row 0 of the board" in plain(r)]
    assert backdrop and k.c["dim"] in backdrop[0]


@pytest.mark.parametrize("lang", LANGS)
def test_a_knockout_trades_ink_for_ground(lang):
    """The inversion has ONE seat since inc17, which is what lets operator
    ruling 10 move blueprint's single knockout from the title block to a
    confirm's default answer: a mark that can move needs somewhere to move
    to, and two copies of it spelled the same way is not that."""
    k = LG.kit(lang)
    out = k.knockout_cell("DELETE")
    assert f"{k.t['ground']} on {k.c['ink']}" in out, lang
    assert "DELETE" in plain(out), lang


def test_blueprints_title_block_knockout_comes_from_the_same_seat():
    """The move is only legal if it is the SAME mark. Asserted by rendering
    the title block and finding the seat's exact output inside it."""
    k = LG.kit("blueprint")
    # THE KNOCKOUT FIRES ON `alert` ALONE — a sheet with nothing overdue
    # carries no reversed cell and still states its condition (`_state_cell`).
    # That is also why ruling 10's move is cheap: on a calm sheet the single
    # knockout is UNSPENT, so a confirm may take it and the title block loses
    # nothing.
    k.mood = "alert"
    k.meter(3, 9, [1, 1, 1], 60)          # the block reads its figures here
    state, knocked = k._state_cell()
    assert knocked, "the alert mood is what spends the knockout"
    assert k.knockout_cell(state) in k.tabs(["board", "log"], "board")


# ===========================================================================
# inc18 — Kit.log_row, a full row contract (ruling 8)
# ===========================================================================
TS, MSG = "11:42:07", "worker 3 lost the lease"
LEVELS = ("info", "warn", "error")


@pytest.mark.parametrize("lang", LANGS)
def test_the_log_level_reads_with_the_colour_removed(lang):
    """THE PROPERTY of ruling 8. Three levels, three shapes, compared on the
    PLAIN row — because the defect this replaces was five languages marking
    ERROR with the same `!!` in the same hue, which is legible only as long
    as the hue is."""
    k = LG.kit(lang)
    rows = {lv: plain(k.log_row(lv, TS, MSG)) for lv in LEVELS}
    assert len(set(rows.values())) == 3, (lang, rows)


@pytest.mark.parametrize("lang", LANGS)
def test_the_level_marks_are_one_width_so_the_column_aligns(lang):
    """A ladder whose rungs are different widths moves the message under
    itself, one row in three. Bodmer T2 again: reserve the widest form."""
    k = LG.kit(lang)
    assert len({len(k.LEVELS[lv]) for lv in LEVELS}) == 1, (lang, k.LEVELS)


@pytest.mark.parametrize("lang", LANGS)
def test_a_log_row_returns_its_time_and_its_message_byte_for_byte(lang):
    """Both fields are CONTENT. A log that recased its messages would be
    editing the record, and a log that reformatted its timestamps would be
    disagreeing with the thing that produced them."""
    k = LG.kit(lang)
    for lv in LEVELS:
        got = plain(k.log_row(lv, TS, MSG))
        assert TS in got and MSG in got, (lang, lv)
    odd = "GET /a[b] 500 in 12ms"
    assert odd in plain(k.log_row("error", TS, odd)), lang


@pytest.mark.parametrize("lang", LANGS)
def test_a_log_row_spends_no_rationed_hue(lang):
    """The severity is SHAPE plus NEUTRAL WEIGHT, in all eleven, and the
    reason is two commitments this contract must not break: ledger spends
    `alert` on literal debt, blueprint on overdue and nothing else ("a calm
    sheet carries zero alert"). A log that reached for red on every ERROR
    would spend the one mark those languages guard, on the noisiest row on
    the screen.

    ASSERTED AS A WHITELIST rather than as "no alert token", and the
    difference is a finding: blueprint's `warn` token IS its `mut` token
    (`#7fa8c4` in both), so a test that banned the warn hue by value would
    have banned a neutral in one language and passed vacuously in the others.
    What the row may spend is the neutral family — ink, mut, dim — plus the
    accent on the live edge, and nothing else."""
    k = LG.kit(lang)
    allowed = {k.c["ink"], k.c["mut"], k.c["dim"]}
    for lv in LEVELS:
        used = set(_TAG.findall(k.log_row(lv, TS, MSG))) - {"[/]"}
        assert used <= {f"[{t}]" for t in allowed}, (lang, lv, used)
    live = set(_TAG.findall(k.log_row("info", TS, MSG, tail=True))) - {"[/]"}
    assert live <= {f"[{t}]" for t in allowed | {k.c["accent"]}}, lang


@pytest.mark.parametrize("lang", LANGS)
def test_the_tail_is_the_live_edge_and_only_the_tail_has_it(lang):
    """`tail=True` marks the row the next line will arrive after, with the
    language's own DISCLOSE — the same declaration the select spends, because
    it is the same sentence: THERE IS MORE. A select points at a list, a log
    points at the line that has not arrived yet."""
    k = LG.kit(lang)
    quiet = plain(k.log_row("info", TS, MSG))
    live = plain(k.log_row("info", TS, MSG, tail=True))
    assert live != quiet, lang
    assert live.endswith(k.DISCLOSE), (lang, live)
    assert not quiet.endswith(k.DISCLOSE), (lang, quiet)


def test_five_languages_mark_five_ladders():
    """The anti-palette-swap law on severity, for the third time in this
    batch. `INVALID`, `danger`, and now the log level: every one of them is a
    place where the obvious answer is a red glyph in eleven languages."""
    rows = {n: plain(LG.kit(n).log_row("error", TS, MSG)) for n in PROTOTYPED}
    assert len(set(rows.values())) == len(PROTOTYPED), rows


# ===========================================================================
# inc19 — Kit.match (ruling 9) and Kit.keyhint (rulings 3, 9)
# ===========================================================================
RESULT = "Fix login redirect"
HINTS = (("↑↓", "move"), ("enter", "run"), ("esc", "close"))


@pytest.mark.parametrize("lang", LANGS)
def test_match_returns_the_text_byte_for_byte(lang):
    """THE PROPERTY of ruling 9, and it is BYTE IDENTITY rather than
    containment: the same bytes, in the same order, with nothing inserted
    between them.

    Three of these languages letter their titles in capitals — `tile_row`
    does it, `sect` does it, `field_row`'s caption does it — and in THIS row
    they may not. A palette that answered a search for `re` with a row
    reading `FIX LOGIN REDIRECT` would have taken away the one thing a result
    row is for: seeing that what you typed is what was found.

    Asserted with `==` on the plain row, so an emphasis that added a single
    cell — a bracket, a dagger, a dot — goes red. That is deliberate: see the
    docstring at the seat for why this is the one mark in the contract that
    cannot be a shape."""
    k = LG.kit(lang)
    assert plain(k.match(RESULT, "re")) == RESULT, lang
    assert plain(k.match(RESULT, "RE")) == RESULT, lang
    assert plain(k.match("MiXeD CaSe Title", "case")) == "MiXeD CaSe Title"


@pytest.mark.parametrize("lang", LANGS)
def test_match_marks_the_span_the_query_found_in_the_texts_own_case(lang):
    """The marked run is the text's bytes at the query's position — `RE`
    typed against `redirect` marks `re`, because the row shows the TEXT, and
    the query only says where to look."""
    k = LG.kit(lang)
    got = k.match(RESULT, "RE")
    style = k.MATCH_STYLE.format(**k.c)
    assert f"[{style}]re[/]" in got, (lang, got)


@pytest.mark.parametrize("lang", LANGS)
def test_a_result_that_no_longer_matches_comes_back_unmarked(lang):
    """No match is a CASE, not an error: it is what a result row should look
    like while a query is still being typed past it."""
    k = LG.kit(lang)
    out = k.match(RESULT, "zzz")
    assert plain(out) == RESULT, lang
    assert k.MATCH_STYLE.format(**k.c) not in out, lang


@pytest.mark.parametrize("lang", LANGS)
def test_the_match_emphasis_is_not_a_hue_alone(lang):
    """The one place in this contract where the second channel cannot be a
    glyph, so it is a STYLE — weight, underline, reverse. None of them is a
    hue, and none of them survives a cell grid either: recorded at the seat,
    asserted here, and visible in the `.svg` only."""
    k = LG.kit(lang)
    assert any(w in k.MATCH_STYLE for w in ("bold", "underline", "reverse")), \
        (lang, k.MATCH_STYLE)


@pytest.mark.parametrize("lang", LANGS)
def test_keyhint_prints_the_key_it_was_handed(lang):
    """inc12 §8.3, paid for once already by a consumer app: "a mark that
    encodes a binding belongs to whoever owns the keymap. Never the library."
    The kit owns the bracket, the leader, the extension line; the caller owns
    every key inside them."""
    k = LG.kit(lang)
    got = plain(k.keyhint(HINTS))
    for key, label in HINTS:
        assert key in got, (lang, key)
        assert label.lower() in got.lower(), (lang, label)


@pytest.mark.parametrize("lang", LANGS)
def test_a_button_never_numbers_itself(lang):
    """OPERATOR RULING 3, as a law over all eleven languages: a button is
    LABELLED with a word, and the numbers stay the parameter keymap (L-33).

    corgi is the language this is about — its numbering IS its keybinding
    notation — and the temptation is exactly the one the kit already fell for
    once, when `display_label` hardcoded `[1]` and spent a binding on behalf
    of every app that drew a display. A digit in a control's face that the
    caller did not put there is the kit claiming a key."""
    k = LG.kit(lang)
    for out in (k.button("Save"), k.button("Delete", 12),
                k.button("Delete", 12, danger=True),
                k.button("Cancel", 8, LG.FOCUSED)):
        assert not any(ch.isdigit() for ch in plain(out)), (lang, plain(out))


def test_corgis_numbering_lives_in_the_hint_row_where_it_is_functional():
    """The other half of ruling 3: the numbers are not banned, they are
    PLACED. §3b — "in a TUI the numbers ARE the keybindings" — so the bracket
    belongs on the row that says which key does what, and the caller still
    supplies the digit."""
    k = LG.kit("corgi")
    got = plain(k.keyhint([("1", "board"), ("2", "log")]))
    assert "[1]" in got and "[2]" in got and "BOARD" in got


def test_five_languages_letter_five_hint_rows():
    rows = {n: plain(LG.kit(n).keyhint(HINTS)) for n in PROTOTYPED}
    assert len(set(rows.values())) == len(PROTOTYPED), rows


# ===========================================================================
# inc28 (kits-learn-4) — `Kit.pane_split`, the last composition primitive
# ===========================================================================
SPLIT_H, SPLIT_W = 6, 3


@pytest.mark.parametrize("lang", LANGS)
def test_a_pane_split_is_the_rectangle_it_was_asked_for(lang):
    """`h` rows of exactly `w` cells, in every language including the two
    that refuse the rule.

    This is the law that makes the seat usable at all: the two panes sit on
    either side of it on EVERY line, so a row that came back short or long
    would move the right pane down the page. A refusal is air at the same
    width, never a missing row."""
    rows = LG.kit(lang).pane_split(SPLIT_H, SPLIT_W)
    assert len(rows) == SPLIT_H, lang
    assert [len(plain(r)) for r in rows] == [SPLIT_W] * SPLIT_H, \
        (lang, [plain(r) for r in rows])


def test_five_languages_split_five_ways():
    """THE PROPERTY (AC-1), and the defect it names is one cell wide.

    Before this seat `screens.py` printed `[dim]│[/]` between the two panes in
    all five languages, exactly as it had printed a red `!` for INVALID and
    ledger's dot leaders for every definition row. Composition is the last
    palette-swap and this is where it lived.

    Same height, same width, five splits that differ AS CELLS: a solid display
    bar (corgi), an unlit lattice column (naught), a ruled money column opened
    at its head rule (ledger), a grey step of background (prism), two datums
    that never join (blueprint). Compared on the PLAIN text — two splits
    differing only in a colour token are two recolours."""
    got = {n: tuple(plain(r) for r in LG.kit(n).pane_split(SPLIT_H, SPLIT_W))
           for n in PROTOTYPED}
    assert len(set(got.values())) == len(PROTOTYPED), got


def test_the_pane_split_registry_names_languages_that_exist():
    """`LABEL_REFUSED`'s law, asked of the third table to use the pattern.

    The set is five since inc36: swiss, darkside and solari joined the two the
    PROTOTYPE round found. It is written out rather than counted, so adding a
    language to the table without deciding its commitment is red."""
    assert set(LG.PANE_SPLIT_REFUSED) <= set(LG.KITS)
    assert set(LG.PANE_SPLIT_REFUSED) == {"blueprint", "prism", "swiss",
                                          "darkside", "solari"}
    assert all(len(v) > 40 for v in LG.PANE_SPLIT_REFUSED.values())


@pytest.mark.parametrize("lang", sorted(LG.PANE_SPLIT_REFUSED))
def test_a_refusing_language_rules_no_stroke(lang):
    """The refusal, measured on the cells rather than trusted.

    Neither of these may put a vertical stroke between two panes, and their
    reasons differ: blueprint's ten marks do not contain one, prism has
    forbidden itself to spend one. The assertion is the same either way."""
    rows = LG.kit(lang).pane_split(SPLIT_H, SPLIT_W)
    assert not any(ch in "│┃║╎╏┆┇┊┋|" for r in rows for ch in plain(r)), \
        (lang, [plain(r) for r in rows])


def test_the_pane_split_registry_is_read_and_not_printed():
    """THE TEETH, both ways — what makes the table a mechanism, not a note.

    Take blueprint OUT and it rules a line its alphabet cannot construct. Put
    naught IN and the language whose answer IS the lattice loses it. Neither
    language's code is touched in either direction: the table decides."""
    k_b, k_n = LG.kit("blueprint"), LG.kit("naught")
    saved = dict(LG.PANE_SPLIT_REFUSED)
    try:
        del LG.PANE_SPLIT_REFUSED["blueprint"]
        assert "│" in plain(k_b.pane_split(2, 3)[0])
        LG.PANE_SPLIT_REFUSED["naught"] = "a false entry"
        assert plain(k_n.pane_split(2, 3)[0]).strip() == ""
    finally:
        LG.PANE_SPLIT_REFUSED.clear()
        LG.PANE_SPLIT_REFUSED.update(saved)
    assert "│" not in plain(k_b.pane_split(2, 3)[0])
    assert LG.kit("naught").pane_split(2, 3)[0].strip() != ""


# ---------------------------------------------------------------------------
# inc36 (inheritors-2) — `pane_split` for the six that inherited it
# ---------------------------------------------------------------------------
#: the six languages that DRAW a pane rule, i.e. the eleven minus the registry.
#: Derived from the table rather than typed, so a language changing sides
#: changes this list too and the distinctness law follows it.
DRAWERS = tuple(n for n in LANGS if n not in LG.PANE_SPLIT_REFUSED)


def test_every_language_that_draws_a_pane_rule_draws_a_different_one():
    """THE PROPERTY, and it is asked only of the languages that DRAW.

    A refusal is not required to be distinct — four of the five answer with
    air and two of those four are a grey STEP the `.txt` cannot show, so a
    distinctness law over all eleven would be a law about a limit rather than
    about a design. Over the six that draw it is exactly the palette-swap
    question: same height, same width, six rules that differ AS CELLS — an
    unlit lattice column (naught), a solid display bar (corgi), a graticule
    column (instrument), two plates facing (industrial), the terminal's
    hairline (nord), a ruled money column opened at its head rule (ledger)."""
    got = {n: tuple(plain(r) for r in LG.kit(n).pane_split(SPLIT_H, SPLIT_W))
           for n in DRAWERS}
    assert len(set(got.values())) == len(DRAWERS), got


@pytest.mark.parametrize("lang", LANGS)
def test_the_closure_law_holds_on_every_pane_seat_at_every_width(lang):
    """`w` IS A SEAT — the law `pane_split`'s own docstring states, asked at
    every width a caller can reach and not only at 3.

    A row that came back short or long moves the right pane down the page, so
    this is the one property a refusal must satisfy as strictly as a rule.
    Widths 1 and 2 are in the list because industrial's mechanism draws TWO
    marks and has to degrade to one; a seat that only closes at its design
    width is a seat that will be found open by a narrow terminal."""
    k = LG.kit(lang)
    for w in (1, 2, 3, 4, 7, 12):
        for h in (0, 1, 5):
            rows = k.pane_split(h, w)
            assert len(rows) == h, (lang, w, h)
            assert [len(plain(r)) for r in rows] == [w] * h, (
                lang, w, [plain(r) for r in rows])


@pytest.mark.parametrize("lang", ("swiss", "darkside", "solari"))
def test_the_three_new_refusals_are_read_and_not_printed(lang):
    """THE TEETH FOR inc36'S OWN ENTRIES, in the direction that matters.

    Each of these three was ruling the terminal's `│` before this increment —
    a stroke all three had committed against in `LANGUAGES.md` and none of
    them had been asked about. Delete the entry and the language goes straight
    back to that stroke, with no other line of its code touched. That is the
    table deciding, and it is what separates a registry from a comment."""
    k = LG.kit(lang)
    assert "│" not in plain(k.pane_split(2, 3)[0]), lang
    saved = dict(LG.PANE_SPLIT_REFUSED)
    try:
        del LG.PANE_SPLIT_REFUSED[lang]
        assert "│" in plain(LG.kit(lang).pane_split(2, 3)[0]), lang
    finally:
        LG.PANE_SPLIT_REFUSED.clear()
        LG.PANE_SPLIT_REFUSED.update(saved)
    assert "│" not in plain(LG.kit(lang).pane_split(2, 3)[0]), lang


@pytest.mark.parametrize("lang", DRAWERS)
def test_a_false_entry_silences_any_language_that_draws(lang):
    """The other direction, asked of all six rather than of naught alone: a
    table that only bites the languages already in it decides nothing for the
    ones that are not."""
    saved = dict(LG.PANE_SPLIT_REFUSED)
    try:
        LG.PANE_SPLIT_REFUSED[lang] = "a false entry, long enough to be one"
        assert plain(LG.kit(lang).pane_split(2, 3)[0]).strip() == "", lang
    finally:
        LG.PANE_SPLIT_REFUSED.clear()
        LG.PANE_SPLIT_REFUSED.update(saved)
    assert plain(LG.kit(lang).pane_split(2, 3)[0]).strip() != "", lang


def test_industrial_closes_one_pane_and_opens_the_next_in_its_own_chrome():
    """The only one of the eleven whose commitment ASKS for a box, ruling a
    gutter in half-cell plate instead of the terminal's hairline — and in
    `keyhint`'s order, which is what makes it one convention rather than two.

    `keyhint` plates a key as `▐up▌`: the ink faces the CONTENT. So a gutter
    closes the left pane with `▌` and opens the right with `▐`, and the air
    between belongs to the panes."""
    k = LG.kit("industrial")
    rows = [plain(r) for r in k.pane_split(3, 3)]
    assert set(rows) == {"▌ ▐"}, rows
    assert k.DISPLAY_BOX[6] + k.DISPLAY_BOX[7] == "▌▐"
    assert plain(k.pane_split(1, 5)[0]) == "▌   ▐"
    # and below two cells there is no room for two plates
    assert plain(k.pane_split(1, 1)[0]) == "▐"


def test_instruments_graticule_column_is_not_its_error_rung():
    """A neutral divider may not wear the severity ladder's cell.

    This language's rungs are dot COUNT in the LEFT column (`⠂⠂ / ⠆⠆ / ⠇⠇`),
    and `⠇` — three dots, left column — is the error rung. A gutter ruled with
    it would say "rejected" down the whole page to a greyscale reader, which
    is the failure ruling 8 exists against. `⠸` is the same three dots in the
    other column and says nothing else in this alphabet."""
    k = LG.kit("instrument")
    cell = plain(k.pane_split(1, 3)[0]).strip()
    assert cell == "⠸"
    assert cell not in "".join(k.LEVELS.values())
    assert cell != k.DISCLOSE and cell not in k.DANGER_FORM


def test_darkside_and_prism_step_the_ground_and_swiss_and_solari_do_not():
    """The four air-answering refusals are not one answer, and the `.txt` is
    where that stops being visible.

    Darkside and prism separate by a ±1 grey step of BACKGROUND — the doctrine
    the parent holds and the child inherited — so their markup carries a
    ground and their cells do not. Swiss and solari separate by the pad
    itself, so there is no markup at all. All four read as `w` spaces in a
    cell grid, which is the limit this file already carries for the knockout
    and for every language's match emphasis, and the honest place to read a
    step is the `.svg`."""
    for lang in ("darkside", "prism"):
        k = LG.kit(lang)
        got = k.pane_split(2, 3)
        assert k.depth_ground() in "".join(got), lang
        assert all(plain(r) == "   " for r in got), lang
    for lang in ("swiss", "solari"):
        got = LG.kit(lang).pane_split(2, 3)
        assert got == ["   ", "   "], (lang, got)


def test_ledgers_column_is_opened_at_the_head_rule():
    """The one thing separating ledger's `│` from the terminal's own.

    `cols_frame` opens a ruled column at the head rule and rules DOWN from it,
    so a column rule that started in mid-air would be a stroke this page never
    posted. Nord rules because a terminal rules; ledger rules because the
    column was OPENED, and the difference is row 0."""
    k = LG.kit("ledger")
    rows = [plain(r) for r in k.pane_split(4, 3)]
    assert rows[0] == k.RULE_HEAD * 3
    assert set(rows[1:]) == {" " + k.RULE_V + " "}
    assert plain(LG.kit("nord").pane_split(4, 3)[0]) != rows[0]


def test_blueprints_two_datums_never_join():
    """The registration pair's law, applied to a pane seat: the left field
    TERMINATES and the right field OPENS, once, and no stroke runs between
    them. One row of declaration and the rest is air is a DIMENSION — it
    states an extent and then stops."""
    rows = [plain(r) for r in LG.kit("blueprint").pane_split(5, 3)]
    assert rows[0] == "┤ ├"
    assert set(rows[1:]) == {"   "}


# ===========================================================================
# inc29 (kits-learn-4) — `Kit.error` and `Kit.required`, S2's other two
# ===========================================================================
MSG = "due must be a date (dd/mm/yy)"
EW = 44


@pytest.mark.parametrize("lang", LANGS)
def test_an_error_row_returns_its_message_byte_for_byte(lang):
    """THE CONTENT LAW, on the one string in a form that must not be edited.

    The words are the caller's account of what is wrong. Three of these
    languages letter their labels in capitals and none of them may letter
    this; none may truncate it either, however narrow the row is asked for —
    a validation message trimmed to fit is a complaint the user cannot act
    on."""
    k = LG.kit(lang)
    for w in (EW, 8, 200):
        assert MSG in plain(k.error(MSG, w)), (lang, w, plain(k.error(MSG, w)))
    weird = "Q3 -1,204.55 [ref] AbCd"
    assert weird in plain(k.error(weird, EW)), lang


@pytest.mark.parametrize("lang", LANGS)
def test_an_error_row_survives_greyscale(lang):
    """The mark is a SHAPE, so the row still says ERROR with every hue
    removed — and it is not any of the language's other two rungs, so a
    greyscale eye can tell a rejection from a warning."""
    k = LG.kit(lang)
    got = plain(k.error(MSG, EW))
    assert got.startswith(k.LEVELS["error"]), (lang, got)
    assert k.LEVELS["error"] != k.LEVELS["warn"] != k.LEVELS["info"], lang


def test_five_languages_explain_a_rejection_five_ways():
    """THE PROPERTY (AC-2). Same message, same width, five rows that differ
    as cells: the segment bank on bare panel (corgi), two lit dots over an
    unlit lattice (naught), a single-daggered footnote ruled out to the
    margin (ledger), the ember at full strength (prism), a revision note on a
    dashed extension (blueprint)."""
    rows = {n: plain(LG.kit(n).error(MSG, EW)) for n in PROTOTYPED}
    assert len(set(rows.values())) == len(PROTOTYPED), rows


def test_the_error_mark_is_the_languages_own_level_ladder_and_not_a_new_table():
    """A second severity table beside `LEVELS` would be two answers to one
    question. An inline validation failure and a log line at ERROR are the
    same claim about the same severity, made about a field instead of an
    event — so the mark is read off the ladder that already survives
    greyscale by ruling 8."""
    for lang in LANGS:
        k = LG.kit(lang)
        assert plain(k.error("x", 4)).startswith(k.LEVELS["error"]), lang


@pytest.mark.parametrize("lang", ("ledger", "blueprint"))
def test_the_two_rationing_languages_spend_no_alert_on_a_rejected_field(lang):
    """The commitment `log_row` already guards, asked of the other component
    that wants red: ledger's alert is literal debt, blueprint's is overdue
    and nothing else ("a calm sheet carries zero alert"). A rejected form
    field is neither."""
    k = LG.kit(lang)
    assert k.c["alert"] not in k.error(MSG, EW), lang
    assert k.c["alert"] not in k.required(), lang


@pytest.mark.parametrize("lang", LANGS)
def test_a_required_mark_is_one_cell_and_costs_no_rationed_hue(lang):
    """One cell, so a caption's column does not move when a field becomes
    obligatory; and the ink tier rather than alert, because a required field
    is a PROPERTY of the field and not an alarm about it."""
    k = LG.kit(lang)
    assert len(plain(k.required())) == 1, (lang, plain(k.required()))
    assert plain(k.required()).strip() != "", lang


def test_the_required_mark_is_not_a_bare_star_in_any_prototyped_language():
    """The candidate's own commitment, made falsifiable: "it may NOT be a
    bare `*` in five languages, which is the palette-swap failure at one
    glyph". `*` is the terminal's convention and the base kit keeps it; a
    language with an alphabet of its own answers for itself."""
    marks = {n: plain(LG.kit(n).required()) for n in PROTOTYPED}
    assert "*" not in marks.values(), marks
    assert len(set(marks.values())) == len(PROTOTYPED), marks
    assert plain(LG.kit("nord").required()) == "*"


# ---------------------------------------------------------------------------
# inc35 (inheritors-2) — `required` for the six that inherited it
# ---------------------------------------------------------------------------
def test_eleven_languages_mark_an_obligation_eleven_ways():
    """THE PROPERTY, and it is the one the five-language version could not
    make: `required` is ONE CELL, so it is the narrowest seat in this file
    and the easiest place in the repo for eleven languages to agree by
    accident. Five did not agree; six inherited `*` and therefore did.

    Eleven marks, no two the same cell — a graticule's floor dot
    (instrument), the weight ladder's own mark set solid (swiss), the plate
    opened (industrial), one achromatic solid cell (darkside), a seam with
    nothing flipped onto it (solari), and the five the PROTOTYPE round
    already had."""
    marks = {n: plain(LG.kit(n).required()) for n in LANGS}
    assert len(set(marks.values())) == len(LANGS), marks


def test_only_the_language_that_declares_the_environment_marks_with_a_star():
    """`*` IS AN ANSWER EXACTLY ONCE, and the test says whose.

    The base comment's claim is "`*` is the terminal's own convention and the
    base kit is the terminal; every language with an alphabet of its own
    answers below". So the bare star may survive in exactly one language, and
    it is the one whose whole commitment is to inherit the environment
    (LANGUAGES.md §6: "the only language here that INHERITS THE USER'S
    ENVIRONMENT instead of overriding it"). Any OTHER language reaching `*`
    is the palette-swap failure at one glyph, which is what this asserts —
    not "no star anywhere", which would make nord's declaration illegal."""
    starred = [n for n in LANGS if plain(LG.kit(n).required()) == "*"]
    assert starred == ["nord"], starred


@pytest.mark.parametrize("lang", LANGS)
def test_a_required_mark_survives_greyscale(lang):
    """Ruling 8's law asked of the narrowest mark there is.

    The cell must carry the claim with every hue removed, so: it is a SHAPE
    (non-blank in `plain`, which is the row with colour stripped at the
    source), it is one cell, and it is still distinct from every other
    language's once the colour is gone. The last clause is the one that
    matters — two languages whose marks differ only in a hue token are two
    recolours of one mark, which is the defect this seat exists against."""
    k = LG.kit(lang)
    cell = plain(k.required())
    assert len(cell) == 1 and cell.strip(), (lang, repr(cell))
    others = {plain(LG.kit(n).required()) for n in LANGS if n != lang}
    assert cell not in others, (lang, cell)


@pytest.mark.parametrize("lang", INHERITORS)
def test_an_inheritors_required_mark_costs_no_rationed_hue(lang):
    """The six held to the base's stated tier rather than trusted: the ink
    tier, one weight step above the `mut` caption it stands beside, and NOT
    the alert hue — a required field is a PROPERTY of the field and not an
    alarm about it. Industrial is the row that matters, because its own entry
    in LANGUAGES.md says it "FAILS when colour must carry severity"."""
    k = LG.kit(lang)
    got = k.required()
    assert k.c["alert"] not in got, (lang, got)
    assert k.c["ink"] in got, (lang, got)


def test_no_language_numbers_a_required_field():
    """L-33, applied to the mark most likely to reach for a digit: corgi's
    numbers ARE its keymap, and an obligation is not a key."""
    for lang in LANGS:
        assert not any(ch.isdigit() for ch in plain(LG.kit(lang).required())), \
            lang


def test_ledgers_two_daggers_are_an_order_and_not_a_pair():
    """Footnote order is the whole notation: `†` marks the entry that must be
    made, `‡` marks the one that was refused — and `‡` is also the wall this
    language's invalid field is daggered with, so the mark on the row and the
    mark on the field are the same claim."""
    k = LG.kit("ledger")
    assert plain(k.required()) == "†"
    assert k.LEVELS["error"].strip() == "‡"
    assert k.field_form(LG.INVALID, "textfield")[0] == "‡"


# ===========================================================================
# inc30 (kits-learn-4) — `Kit.textarea`, the field over a rectangle
# ===========================================================================
TA_LINES = ["ship the kit", "check the sweep", "then push"]
TA_W, TA_H = 20, 4


@pytest.mark.parametrize("lang", LANGS)
def test_a_three_line_text_renders_three_rows_with_a_visible_caret_row(lang):
    """THE PROPERTY (AC-3), and it is two claims in one sentence.

    THREE LINES, THREE ROWS: the caller owns the line breaks, so row `i` is
    line `i` and nothing is reflowed underneath it.

    ONE VISIBLE CARET ROW: the caret takes a column of its own — the one-line
    field's law, for the one-line field's reason — and it appears on exactly
    the row it was addressed to. A field with an insertion point on every row
    is a state the model cannot be in."""
    k = LG.kit(lang)
    rows = k.textarea(TA_LINES, (1, 5), TA_W, TA_H, LG.EDITED)
    assert len(rows) == TA_H, lang
    caret = k.part_glyph("caret", LG.EDITED, "textfield")
    for i, line in enumerate(TA_LINES):
        # the caret's column SPLITS its row, which IS the mechanism: every
        # byte is there and one cell was inserted between two of them
        assert line in plain(rows[i]).replace(caret, ""),             (lang, i, plain(rows[i]))
    marked = [i for i, r in enumerate(rows)
              if caret in plain(r)[1:-1]]
    assert marked == [1], (lang, caret, [plain(r) for r in rows])


@pytest.mark.parametrize("lang", LANGS)
def test_a_textarea_returns_the_rectangle_it_was_asked_for(lang):
    """`h` rows of `w` cells between the walls, whatever it was handed —
    fewer lines than rows, more lines than rows, no lines at all. A row that
    came back short would move everything under the field up the frame."""
    k = LG.kit(lang)
    op, _rune, cl = k.field_form(LG.DEFAULT, "textfield")
    for lines in ([], TA_LINES, TA_LINES * 4):
        rows = k.textarea(lines, None, TA_W, TA_H)
        assert len(rows) == TA_H, (lang, lines)
        for r in rows:
            assert len(plain(r)) == TA_W + len(op) + len(cl), (lang, plain(r))


@pytest.mark.parametrize("lang", LANGS)
def test_a_line_that_fits_comes_back_byte_for_byte(lang):
    """The content law, and the frame's own notes are the case that matters:
    a language that letters its labels in capitals may not letter these."""
    k = LG.kit(lang)
    weird = ["Q3 -1,204.55 [ref]", "AbCd  eF"]
    rows = k.textarea(weird, None, 30, 2)
    for i, line in enumerate(weird):
        assert line in plain(rows[i]), (lang, plain(rows[i]))


@pytest.mark.parametrize("lang", LANGS)
def test_an_overlong_line_is_marked_and_never_silently_cut(lang):
    """The one place the bytes stop, and it says so with a mark.

    A one-line field moves its WINDOW sideways; a rectangle's rows cannot. So
    the row shows the line's own leading bytes, in order, and spends the
    language's `DISCLOSE` on the last cell — the same declaration a select
    and a log's tail spend: THERE IS MORE."""
    k = LG.kit(lang)
    row = plain(k.textarea(["x" * 40], None, 10, 1)[0])
    assert k.DISCLOSE in row, (lang, row)
    assert "x" * 9 in row, (lang, row)


def test_the_wrap_mark_is_the_languages_own_disclosure_and_not_a_new_table():
    """Three components, one declaration. A second constant for "this row
    continues" would be an eleventh restatement of a mark every language has
    already chosen."""
    for lang in LANGS:
        k = LG.kit(lang)
        assert plain(k.textarea(["y" * 40], None, 8, 1)[0]).rstrip(
            k.field_form(LG.DEFAULT, "textfield")[2]).endswith(k.DISCLOSE), \
            lang


def test_five_languages_paper_five_rectangles():
    """The rectangle is composed out of seats the languages already differ
    on, so it differs without a single new per-language line. That is the
    claim this test makes falsifiable: if it ever goes red, a language has
    lost its `field_form` or its caret part, not its textarea."""
    got = {n: tuple(plain(r)
                    for r in LG.kit(n).textarea(TA_LINES, (0, 2), TA_W, TA_H,
                                                LG.EDITED))
           for n in PROTOTYPED}
    assert len(set(got.values())) == len(PROTOTYPED), got


@pytest.mark.parametrize("lang", LANGS)
def test_a_textarea_with_no_caret_draws_none(lang):
    """S2's own case: the caret is in `title` on that frame, so the notes
    rectangle must not draw a second one. `caret=None` means the field is not
    where the next keystroke lands, and the render says so."""
    k = LG.kit(lang)
    caret = k.part_glyph("caret", LG.DEFAULT, "textfield")
    for r in k.textarea(TA_LINES, None, TA_W, TA_H):
        assert caret not in plain(r)[1:-1], (lang, plain(r))


# ===========================================================================
# inc31 (kits-learn-4) — `Kit.readout_label`, L-33 with a seat
# ===========================================================================
NUMBERED = tuple(sorted(n for n in LANGS if LG.kit(n).numbered))


def test_the_readout_registry_names_exactly_the_numbered_languages():
    """The one table here whose keys are DERIVABLE, so it cannot drift.

    A language that numbers nothing has no numbering to refuse, and a
    language that numbers everything must say why this one component is
    exempt. Add a `numbered` language to `KITS` and this test tells you to
    write its citation rather than letting it silently number a bar."""
    assert set(LG.READOUT_NUMBER_REFUSED) == set(NUMBERED)
    assert set(NUMBERED) == {"corgi", "industrial", "ledger"}
    assert all(len(v) > 40 for v in LG.READOUT_NUMBER_REFUSED.values())


@pytest.mark.parametrize("lang", LANGS)
def test_no_language_numbers_a_readout(lang):
    """L-33, measured on a real app and now asked of all eleven: a `[5]` over
    a chart nobody can act on is a keybinding spent on something unpressable.

    Asserted with a caller string that OPENS with a binding, because that is
    the input a numbering language would letter it from."""
    k = LG.kit(lang)
    for label in ("rate", "5 rate", "12 events per minute"):
        got = plain(k.readout_label(label))
        assert not any(ch.isdigit() for ch in got), (lang, label, got)


@pytest.mark.parametrize("lang", NUMBERED)
def test_the_readout_and_the_display_diverge_and_the_divergence_is_the_law(lang):
    """The two seats side by side, which is where L-33 actually lives: the
    SAME language, the SAME caller string, a number on the control and no
    number on the readout."""
    k = LG.kit(lang)
    assert k.display_label(1, "5 rate") == "[5] RATE", lang
    assert plain(k.readout_label("5 rate")) == "RATE", lang


def test_the_readout_registry_is_read_and_not_printed():
    """THE TEETH. Take ledger out and it spends a key on a bar nobody can
    press; the language's own code is not touched in either direction.

    This table can only be wrong in ONE direction and the test says so: a
    false entry for a language that numbers nothing changes nothing, because
    there was no notation there to withhold."""
    saved = dict(LG.READOUT_NUMBER_REFUSED)
    try:
        del LG.READOUT_NUMBER_REFUSED["ledger"]
        assert plain(LG.kit("ledger").readout_label("5 rate")) == "[5] RATE"
        LG.READOUT_NUMBER_REFUSED["prism"] = "a false entry"
        assert plain(LG.kit("prism").readout_label("5 rate")) == "RATE"
    finally:
        LG.READOUT_NUMBER_REFUSED.clear()
        LG.READOUT_NUMBER_REFUSED.update(saved)
    assert plain(LG.kit("ledger").readout_label("5 rate")) == "RATE"


@pytest.mark.parametrize("lang", LANGS)
def test_a_readouts_word_is_the_callers(lang):
    """The legend is the caller's and the notation is the language's — the
    ruling `display_label` already carries, and this method is its twin
    because a readout's legend and a display's legend are the same object."""
    k = LG.kit(lang)
    assert "EVENTS PER MINUTE" in plain(k.readout_label("events per minute"))
    assert plain(k.readout_label("")) == "READOUT", lang


# ===========================================================================
# inc32 (kits-learn-4) — the six that inherited, asked to choose
# ===========================================================================
#: the six that had `Kit`'s answer to the seven mechanisms below and had never
#: been asked for one of their own
#: the mechanisms where a PLAIN difference is lawful. `MATCH_STYLE` is absent
#: on purpose and the reason is a ruling: operator ruling 9 requires a result
#: row to come back byte for byte, so two languages MUST render `match`
#: identically as cells and the only channel left is style. Its law is
#: `test_the_match_emphasis_is_not_a_hue_alone`, not distinctness.
SEVEN_PLAIN = ("field_row", "DISCLOSE", "DANGER_FORM", "LEVELS", "keyhint",
               "overlay")

_UNDER = ["board row " + str(i) for i in range(9)]
_DIALOG = ["DELETE 3 TASKS?", "", "yes   no"]


def _mech(k, name):
    """One mechanism's PLAIN render, for a fixed input, in one language."""
    if name == "field_row":
        return plain(k.field_row("due date", "12/09/26", 40))
    if name == "DISCLOSE":
        return k.DISCLOSE
    if name == "DANGER_FORM":
        return plain(k.button("Delete", 12, LG.DEFAULT, danger=True))
    if name == "LEVELS":
        return tuple(k.LEVELS[x] for x in ("info", "warn", "error"))
    if name == "keyhint":
        return plain(k.keyhint([("up", "move"), ("esc", "close")]))
    if name == "overlay":
        return tuple(plain(r) for r in k.overlay(_DIALOG, 34, 9, _UNDER))
    raise AssertionError(name)


@pytest.mark.parametrize("mech", SEVEN_PLAIN)
def test_no_two_languages_answer_a_mechanism_the_same_way(mech):
    """THE PROPERTY (AC-5), asked of all eleven rather than of the six.

    A seat with five implementations and six holes is the palette-swap
    failure with a longer fuse: the five that were prototyped diverge and the
    six that were never rendered quietly agree, which looks like a contract
    and is a default. Same input, eleven answers, no two of them the same
    string of cells.

    `overlay` is the one that can only ALMOST hold, and its exception is
    named in the test below: a grey step of background is not a cell."""
    got = {n: _mech(LG.kit(n), mech) for n in LANGS}
    dupes = {}
    for n, v in got.items():
        dupes.setdefault(v, []).append(n)
    clash = [v for v in dupes.values() if len(v) > 1]
    if mech == "overlay":
        assert clash == [["nord", "prism"]], clash
        return
    assert not clash, (mech, clash)


def test_prisms_overlay_differs_from_nords_in_the_svg_and_not_the_txt():
    """The one collision the property test allows, and it is a limit of the
    medium rather than a hole.

    Prism is the one language `MODAL_BORDER_REFUSED` leaves out, so it draws
    the terminal's lid; what it changes is the page BEHIND, which `recede`
    steps by one grey of BACKGROUND. A background is not a cell, so the
    `.txt` of the two is identical and the `.svg` is not — the third mark in
    this contract with that limit, after the knockout and the match."""
    n, p = LG.kit("nord"), LG.kit("prism")
    a = n.overlay(_DIALOG, 34, 9, _UNDER)
    b = p.overlay(_DIALOG, 34, 9, _UNDER)
    assert [plain(r) for r in a] == [plain(r) for r in b]
    assert a != b
    assert p.depth_ground() in "".join(b)


@pytest.mark.parametrize("attr", ["field_row", "DISCLOSE", "DANGER_FORM",
                                  "LEVELS", "MATCH_STYLE", "keyhint",
                                  "overlay", "REQUIRED", "PANE_RULE",
                                  "pane_split_rule", "pane_split_instead"])
def test_nord_declares_the_environment_and_the_declaration_is_checked(attr):
    """NORD'S ANSWER IS THE BASE, AND FOR THIS ONE LANGUAGE THAT IS A
    COMMITMENT RATHER THAN A GAP.

    LANGUAGES.md §6: "the only language here that INHERITS THE USER'S
    ENVIRONMENT instead of overriding it — the app looks like the rest of
    their terminal ... Fails: when you need a distinctive identity — BY
    CONSTRUCTION IT HAS NONE OF ITS OWN."

    A block of comments saying so is a promise. This walks the MRO and
    requires the owner to be `Kit`, so a mechanism landing on nord by
    accident goes red and one landing on purpose has to delete the paragraph
    that says nord is base16 first."""
    for klass in type(LG.kit("nord")).__mro__:
        if attr in klass.__dict__:
            assert klass is LG.Kit, (attr, klass.__name__)
            return
    raise AssertionError(attr + " is not defined anywhere")


@pytest.mark.parametrize("lang", INHERITORS)
def test_an_inheritors_danger_still_survives_greyscale(lang):
    """The six's new `DANGER_FORM`s held to inc16's law rather than trusted:
    the severity is a pair of marks INSIDE the walls and it costs no hue at
    all — which matters most for industrial, whose own entry in LANGUAGES.md
    says it "FAILS when colour must carry severity, because the palette
    already spent colour on identity"."""
    k = LG.kit(lang)
    hot = plain(k.button("Delete", 12, LG.DEFAULT, danger=True))
    calm = plain(k.button("Delete", 12, LG.DEFAULT))
    assert hot != calm, lang
    assert k.DANGER_FORM[0] in hot and k.DANGER_FORM[1] in hot, lang


@pytest.mark.parametrize("lang", INHERITORS)
def test_an_inheritors_levels_are_one_width_and_three_shapes(lang):
    """`log_row`'s law (operator ruling 8), asked of the six new ladders: one
    width per language so a column of rows aligns, three distinct shapes so
    the level sorts with the colour taken away."""
    k = LG.kit(lang)
    marks = [k.LEVELS[x] for x in ("info", "warn", "error")]
    assert len({len(m) for m in marks}) == 1, (lang, marks)
    assert len(set(marks)) == 3, (lang, marks)


def test_solari_prints_its_severity_because_a_board_prints_everything():
    """The one ladder of the eleven that is not a glyph, and it is this
    language's headline commitment: "a state is a WORD in a status column".
    A departure board does not draw severity, it prints it — the same
    argument DATAVIZ law 1 already credits it with for quantity."""
    k = LG.kit("solari")
    assert tuple(k.LEVELS[x] for x in ("info", "warn", "error")) == (
        "OK ", "DLY", "CNX")
    row = plain(k.error("expected YYYY-MM-DD", 40))
    assert row.startswith("CNX")
    assert "expected YYYY-MM-DD" in row


def test_industrial_is_the_second_language_licensed_to_draw_a_box():
    """"BOXED GROUPS" is a commitment, and this is the only language of the
    eleven whose commitment ASKS for a lid. The box it draws is its own
    stamped plate rather than the terminal's hairline, and `MODAL_BOX` IS
    `DISPLAY_BOX` — a language that has declared its frame hands the same
    string to both seats instead of spelling its corners twice."""
    k = LG.kit("industrial")
    assert "industrial" not in LG.MODAL_BORDER_REFUSED
    assert k.MODAL_BOX == k.DISPLAY_BOX
    out = [plain(r) for r in k.overlay(_DIALOG, 34, 9, _UNDER)]
    assert any(r.lstrip().startswith("▛") for r in out), out
    assert not any("┌" in r for r in out), out


def test_darksides_lid_is_rounded_and_prisms_is_not():
    """The parent and the descendant share the doctrine that licenses a
    border ("reserved for modals") and do not share the lid. Darkside rounds
    its corners, which is the "clinical-WARM" half of its own adjective;
    prism keeps the terminal's and spends its difference on the page
    behind."""
    d, p = LG.kit("darkside"), LG.kit("prism")
    assert d.MODAL_BOX.startswith("╭╮╰╯")
    assert p.MODAL_BOX == LG.Kit.MODAL_BOX
    out = [plain(r) for r in d.overlay(_DIALOG, 34, 9, _UNDER)]
    assert any("╭" in r for r in out), out


@pytest.mark.parametrize("lang", LANGS)
def test_the_modal_box_is_eight_cells_in_every_language(lang):
    """`DISPLAY_BOX`'s order: (tl, tr, bl, br, top, bottom, left, right).
    Eight rather than six, because half-cell chrome has a different glyph at
    the top of a box than at the bottom — industrial's `▛▀▜` over `▙▄▟` is
    the case that forced it."""
    assert len(LG.kit(lang).MODAL_BOX) == 8, lang


# ---------------------------------------------------------------------------
# inc39 (rework-1) - INVALID is a FORM, not the field's walls turned round
# ---------------------------------------------------------------------------
#: the widths the field law is asked at. `w=1` is the seat with no room for
#: anything but the walls themselves, `34` is what `screens.py` gives S2's
#: `due` field - the frame the inheritors round read the defect off - and 12
#: is this file's own default, so a language that only answers at the width
#: somebody photographed goes red here. inc38's three-width precedent, applied
#: to the other component whose walls are its state channel.
FIELD_WIDTHS = (1, 12, 34)
#: the five OTHER states a text field has. INVALID is the one under test, so
#: its own walls are not in the vocabulary they are measured against.
FIELD_STATES = (LG.DEFAULT, LG.FOCUSED, LG.EDITED, LG.ACTIVE, LG.DISABLED)
#: what the four carried before this increment, kept HERE and not in the kits:
#: the teeth restore them byte for byte, and a constant living in the test is
#: the only copy of a deleted declaration that nothing can reach by accident.
FLIPPED_INVALID = {"nord": "] [", "instrument": "⠸⠶⠇",
                   "industrial": "▌/▐", "blueprint": "┤·├"}
#: WHERE each was declared, and the entry that matters is nord's. nord owns no
#: `PART_GLYPHS` at all — `test_nord_declares_the_environment_and_the_declaration_is_checked`
#: walks the MRO and requires the owner to be `Kit` — so its flip was the
#: BASE's, and that is what moves this from four arguable design decisions to
#: one base defect inherited four times.
FLIPPED_OWNER = {"nord": LG.Kit, "instrument": LG.Instrument,
                 "industrial": LG.Industrial, "blueprint": LG.Blueprint}
#: the languages whose field walls HAVE a handedness — the ones where the law
#: below can actually fire. Derived, then asserted against this roster, so the
#: law's own vacuity is a fact somebody has to look at rather than a silence.
HANDED_FIELDS = ("instrument", "industrial", "nord", "ledger", "blueprint")


def field_walls(k, state):
    """The two walls of a field's ground, off `field_form`'s own split."""
    op, _, cl = k.field_form(state, "textfield")
    return op, cl


def wall_vocabularies(k):
    """What this language uses to OPEN a field and what it uses to CLOSE one,
    read off its five other states rather than off a reviewer's eye."""
    return ({field_walls(k, st)[0] for st in FIELD_STATES},
            {field_walls(k, st)[1] for st in FIELD_STATES})


def invalid_walls_are_handed_right(lang):
    """THE LAW as one predicate, so the teeth can call the same thing the
    law calls instead of a second copy of it."""
    k = LG.kit(lang)
    opens, closes = wall_vocabularies(k)
    op, cl = field_walls(k, LG.INVALID)
    return op not in (closes - opens) and cl not in (opens - closes)


@pytest.mark.parametrize("lang", LANGS)
def test_an_invalid_field_is_not_a_field_with_its_walls_exchanged(lang):
    """THE PROPERTY: a rejected field OPENS with a mark this language opens
    fields with and CLOSES with one it closes them with — in every language,
    at three widths.

    THE DEFECT, which was four frames of one mistake. `nord_S2` drew
    `]12/09/26   [`, `instrument_S2` `⠸…⠇`, `industrial_S2` `▌…▐` and
    `blueprint_S2` `┤…├`: in each, "this value was rejected" was spelled by
    EXCHANGING the two walls and by nothing else. Orientation is not a channel
    a reader can use here — the two marks sit at opposite ends of a 34-cell
    row, so answering "which field is wrong?" means comparing both ends of the
    row against a convention held in memory, and the inheritors round's
    observable criterion (cover the error line, point at the bad field) fails
    on all four.

    WHY THIS IS ONE DEFECT AND NOT FOUR. nord declares no `PART_GLYPHS`, so
    its flip was `Kit`'s own — the base answer every language falls back to.
    The other three re-declared the same turn. Fixed at the declaration seat
    in all four; the law is written once, here, over all eleven.

    HOW THE LAW IS DERIVED, and why it is not "INVALID must keep DEFAULT's
    walls". Seven languages change the wall's FORM for INVALID — swiss's
    `╲ ╱`, darkside's `Ø Ø`, ledger's daggers — and that is the right answer,
    not a violation. So the law asks about HANDEDNESS: the invalid opening
    mark may not be one this language uses ONLY to close, and the closing mark
    may not be one it uses ONLY to open. A new form passes; a turned pair does
    not.

    SCOPED TO THE FIELD ON PURPOSE, and the exemption is named rather than
    left silent: blueprint's `radio.main` points its terminators IN (`┤ ├`)
    where its own checkbox points them OUT (`├ ┤`), and the kit says why — a
    callout selecting one item from a schedule. That is a DECLARED use of
    orientation as a channel between two components, with a citation, so the
    same law over `radio.main` would be red on doctrine. This increment does
    not extend it there.

    THREE WIDTHS, because `field_form` is width-free but the RENDER is not,
    and the render is the artefact a reader judges."""
    k = LG.kit(lang)
    opens, closes = wall_vocabularies(k)
    op, cl = field_walls(k, LG.INVALID)
    assert op not in (closes - opens), (lang, op, sorted(closes - opens))
    assert cl not in (opens - closes), (lang, cl, sorted(opens - closes))
    for w in FIELD_WIDTHS:
        row = plain(k.textfield("12/09/26", None, w, LG.INVALID))
        assert row.startswith(op), (lang, w, row)
        assert row.endswith(cl), (lang, w, row)


def test_the_field_law_can_only_bite_where_the_walls_have_a_hand():
    """THE LAW'S OWN VACUITY, measured instead of assumed.

    Six of the eleven set both walls of a field to the SAME mark in every
    state — corgi's `▁▁ ▁▁`, darkside's `▬ ▬`, solari's seam. A language with
    no handedness cannot encode a state by turning its walls round, so the law
    above is vacuously true there, and saying so is the difference between
    "eleven passed" and "eleven were asked". The roster is derived from the
    declarations and compared against a written one: a language that later
    gives its field a left mark and a right mark joins the set, and this test
    is where somebody finds out."""
    handed = tuple(lang for lang in LANGS
                   if set.symmetric_difference(*wall_vocabularies(LG.kit(lang))))
    assert handed == HANDED_FIELDS, handed
    assert set(FLIPPED_INVALID) <= set(handed)


def test_exchanging_the_field_walls_back_makes_the_law_go_red(monkeypatch):
    """TEETH, one arm per language that carried the flip.

    Each arm restores that language's pre-inc39 declaration byte for byte and
    asserts TWO things: the law goes red on it, and THE OTHER TEN STAY GREEN
    under the same patch. The second half is what proves the four entries are
    four independent declarations rather than one shared object — and it is
    the half that says something about nord, whose arm patches `Kit` itself
    and must therefore leave the ten that own their own table untouched.

    A law nobody has watched fail is a law nobody has watched."""
    assert all(invalid_walls_are_handed_right(lang) for lang in LANGS)
    for lang, old in FLIPPED_INVALID.items():
        owner = FLIPPED_OWNER[lang]
        table = dict(owner.PART_GLYPHS["textfield.main"])
        table[LG.INVALID] = old
        monkeypatch.setitem(owner.PART_GLYPHS, "textfield.main", table)
        assert not invalid_walls_are_handed_right(lang), lang
        assert all(invalid_walls_are_handed_right(other)
                   for other in LANGS if other != lang), lang
        monkeypatch.undo()
    assert all(invalid_walls_are_handed_right(lang) for lang in LANGS)


# ---------------------------------------------------------------------------
# inc40 (rework-1) - an overlay COVERS a band; it does not eat the page's head
# ---------------------------------------------------------------------------
#: the ONE language whose refusal says the page does not survive a confirm, so
#: the head law below cannot be asked of it. Named rather than derived, and its
#: citation is asserted word for word inside the test — an exemption may not
#: outlive the commitment that earns it, and "the board is gone" is the phrase
#: that earns this one.
MODAL_KEEPS_NOTHING = ("corgi",)


def page_rows(lang):
    """The page a modal stands in front of: this language's own S1 frame.

    `screens.s4` builds `under` by running the S1 builder, so the shipped S1
    `.txt` IS the backdrop — not a stand-in for it."""
    return (FRAMES / f"{lang}_S1.txt").read_text(
        encoding="utf-8").rstrip("\n").split("\n")


def page_markup(lang):
    """The same page as a CALLER hands it over: every row through `mark()`.

    A sheet's rows are markup, so a literal `[` in a page (industrial's
    `[21d]`, nord's `[x]`) reaches `overlay` escaped. Passing the raw `.txt`
    instead would have `visible()` read those runs as style tags and eat
    them — the module's own pitfall A1, from the caller's side."""
    return [LG.mark(r) for r in page_rows(lang)]


def modal_band(lang):
    """The rows S4 changes relative to the page, as indices."""
    s1 = page_rows(lang)
    s4 = (FRAMES / f"{lang}_S4.txt").read_text(
        encoding="utf-8").rstrip("\n").split("\n")
    return [i for i, (a, b) in enumerate(zip(s1, s4)) if a.rstrip() != b.rstrip()]


@pytest.mark.parametrize("lang", LANGS)
def test_a_modal_changes_one_contiguous_band_of_the_page(lang):
    """THE COMPOSITION PROPERTY: a question in front of a page occupies a
    REGION. The rows it changes are one run, and every row it does not change
    is the page's own row AT THE SAME INDEX.

    That second half is what "overlay" means and it is the half that can be
    lost silently: a composition that wrote the question and then appended the
    page would push everything down, and the frame would still be `h` rows of
    plausible-looking board — `test_an_overlay_returns_the_rectangle_it_was_
    asked_for` would stay green while every row below the question was one row
    off. Measured on the shipped frames, against the shipped page."""
    band = modal_band(lang)
    assert band, lang
    assert band == list(range(band[0], band[-1] + 1)), (lang, band)


@pytest.mark.parametrize("lang", LANGS)
def test_a_modal_leaves_the_pages_first_row_alone(lang):
    """THE HEAD LAW: the page's first row survives the modal.

    Row 1 is where every one of these languages puts the mode strip, and a
    destructive confirm is precisely the moment the operator needs to know
    which mode the question came from. `solari_S4` used to open on a blank row
    — its announcement band was anchored at screen row 0, so the mode strip,
    the masthead and the head seam were gone and the frame could not answer
    "which mode is this?" at all. Ten of the eleven kept row 1 before this
    increment; solari now does too.

    THE EXEMPTION IS NAMED AND ITS CITATION IS CHECKED. corgi's refusal is
    that a confirm is a MODE — "a dialog floating over a board is two modes at
    once ... so a confirm is a MODE and the board is gone". A language that
    has declared the board gone cannot be asked to keep its first row, and a
    language that quietly stopped keeping it without such a declaration is
    what this law is for."""
    if lang in MODAL_KEEPS_NOTHING:
        assert "the board is gone" in LG.MODAL_BORDER_REFUSED[lang], lang
        assert 0 in modal_band(lang), lang       # the exemption does work
        return
    assert 0 not in modal_band(lang), (lang, modal_band(lang))


def test_solaris_announcement_takes_the_head_of_the_schedule_not_the_screen():
    """SOLARI'S OWN DOCTRINE, kept, and the defect under it, removed.

    `MODAL_BORDER_REFUSED["solari"]`: "a question is posted the way a
    cancellation is, as a BAND IN REVERSE VIDEO at the head of the schedule,
    with the rows still legible under it." Both halves are load-bearing and
    the second one was false: the band was written at index 0, so it landed on
    the station's own plate — the mode strip, `BOARD 16 TASKS · 4 PROJECTS`,
    and the seam that closes them — and those rows were not legible under
    anything, they were gone.

    THE PLATE IS FOUND, NOT COUNTED. `schedule_head` reads the page for its
    first FULL-MEASURE seam, which on this board is what closes the masthead,
    and the schedule starts on the row after it. This is asked against the
    language's own shipped page rather than a synthetic one, because the claim
    is about a real masthead and a synthetic backdrop has none."""
    k = LG.kit("solari")
    under = page_markup("solari")
    assert k.schedule_head(under) == 3, k.schedule_head(under)
    raw = page_rows("solari")
    out = [plain(r) for r in k.overlay(dialog(k), len(raw[0]),
                                       len(raw), under)]
    assert all(a.rstrip() == b.rstrip()
               for a, b in zip(out[:3], raw[:3])), out[:3]
    assert any("Delete 3 tasks?" in r for r in out[3:]), out[3:8]
    # and a page with NO full-measure seam has no plate to protect, so the
    # band still takes the top — the behaviour `UNDER` has always had.
    assert k.schedule_head(UNDER) == 0


def test_anchoring_solaris_band_at_row_zero_eats_the_boards_own_plate(monkeypatch):
    """TEETH. `schedule_head` returning 0 IS the pre-inc40 body — the old loop
    read `if i < len(block)`, which is `0 <= i < len(block)` — so this arm
    restores the defect exactly rather than approximating it.

    The second assertion is the round's own evidence, reproduced: with the
    band at index 0 the page's row 9 comes back as the frame's row 9, which is
    what made `solari_S4.txt` row 9 equal `solari_S1.txt` row 9 byte for byte.
    The page was never SHIFTED — the head was CLOBBERED and everything below
    it stayed exactly where it was. The other ten are asserted untouched by
    the same patch, which is what says the fix is solari's and not the base's.

    A law nobody has watched fail is a law nobody has watched."""
    k = LG.kit("solari")
    under = page_markup("solari")
    raw = page_rows("solari")
    w, h = len(raw[0]), len(raw)
    assert plain(k.overlay(dialog(k), w, h, under)[0]).rstrip() == raw[0].rstrip()

    monkeypatch.setattr(LG.Solari, "schedule_head", lambda self, u: 0)
    out = [plain(r) for r in k.overlay(dialog(k), w, h, under)]
    assert out[0].rstrip() != raw[0].rstrip()
    assert not any(raw[0].strip() and raw[0].strip() in r for r in out)
    assert out[8].rstrip() == raw[8].rstrip()            # row 9 is row 9

    for other in LANGS:
        if other == "solari":
            continue
        ko, u = LG.kit(other), page_rows(other)
        row0 = plain(ko.overlay(dialog(ko), len(u[0]), len(u),
                                page_markup(other))[0])
        if other in MODAL_KEEPS_NOTHING:
            continue
        assert row0.rstrip() == u[0].rstrip(), other


# ---------------------------------------------------------------------------
# inc37 (inheritors-2) — every language is photographed, not just the five
# ---------------------------------------------------------------------------
SCREENS = ("S1", "S2", "S3", "S4", "S5", "S6")


def test_every_language_has_a_frame_for_every_screen():
    """THE DEFECT THIS GUARDS IS A LIST, and it has already happened once.

    `render.py` swept a typed list of five languages for two batches. The six
    that were not on it inherited seat after seat and then, in inc32/35/36,
    got thirty-eight mechanisms of their own — held by property tests and by
    nothing anyone could look at. The list is now read off `LG.KITS`; this is
    what says so from the outside, on the artefacts rather than on the source,
    so a kit added later that nobody sweeps is red here.

    The `.txt` is the file every law in this repo measures (the `.svg` carries
    the two marks a cell grid cannot show), so it is the one asked for."""
    missing = [f"{lang}_{sc}.txt" for lang in LANGS for sc in SCREENS
               if not (FRAMES / f"{lang}_{sc}.txt").exists()]
    assert not missing, missing
    assert len(list(FRAMES.glob("*_S?.txt"))) == len(LANGS) * len(SCREENS)


def test_no_two_languages_render_a_screen_identically():
    """`render.py`'s own sweep law, asserted where the gate runs it.

    Two languages agreeing on a WHOLE screen is the exact defect
    LANGUAGES.md records — "a language that only changes colour is not a
    language" — and until now it was checked only inside a prototype script
    that pytest does not run. 55 pairs per screen, 330 in all.

    It reads the shipped `.txt` rather than re-rendering: a re-render here
    would need Textual and a settle, and the artefact is what a reader
    judges."""
    for sc in SCREENS:
        got = {lang: (FRAMES / f"{lang}_{sc}.txt").read_text(encoding="utf-8")
               for lang in LANGS}
        assert len(set(got.values())) == len(LANGS), (
            sc, [a for a in got if list(got.values()).count(got[a]) > 1])


def test_no_frame_declares_a_hand_drawn_element():
    """THE ROUND'S HEADLINE CLAIM, read off the sidecars the sweep writes.

    A frame with a hand-drawn element is a prototype's taste standing where a
    kit's answer should be, and the sidecar is where `render.py` declares one.
    All 66 say the same sentence, and this is what keeps saying it after the
    next edit to `screens.py`."""
    drawn = [f.name for f in FRAMES.glob("*.candidates.md")
             if "Nothing was drawn by hand" not in f.read_text(encoding="utf-8")]
    assert not drawn, drawn


# ---------------------------------------------------------------------------
# inc37 (inheritors-2) — every language is photographed, not just the five
# ---------------------------------------------------------------------------
SCREENS = ("S1", "S2", "S3", "S4", "S5", "S6")


def test_every_language_has_a_frame_for_every_screen():
    """THE DEFECT THIS GUARDS IS A LIST, and it has already happened once.

    `render.py` swept a typed list of five languages for two batches. The six
    that were not on it inherited seat after seat and then, in inc32/35/36,
    got thirty-eight mechanisms of their own — held by property tests and by
    nothing anyone could look at. The list is now read off `LG.KITS`; this is
    what says so from the outside, on the artefacts rather than on the source,
    so a kit added later that nobody sweeps is red here.

    The `.txt` is the file every law in this repo measures (the `.svg` carries
    the two marks a cell grid cannot show), so it is the one asked for."""
    missing = [f"{lang}_{sc}.txt" for lang in LANGS for sc in SCREENS
               if not (FRAMES / f"{lang}_{sc}.txt").exists()]
    assert not missing, missing
    assert len(list(FRAMES.glob("*_S?.txt"))) == len(LANGS) * len(SCREENS)


def test_no_two_languages_render_a_screen_identically():
    """`render.py`'s own sweep law, asserted where the gate runs it.

    Two languages agreeing on a WHOLE screen is the exact defect
    LANGUAGES.md records — "a language that only changes colour is not a
    language" — and until now it was checked only inside a prototype script
    that pytest does not run. 55 pairs per screen, 330 in all.

    It reads the shipped `.txt` rather than re-rendering: a re-render here
    would need Textual and a settle, and the artefact is what a reader
    judges."""
    for sc in SCREENS:
        got = {lang: (FRAMES / f"{lang}_{sc}.txt").read_text(encoding="utf-8")
               for lang in LANGS}
        assert len(set(got.values())) == len(LANGS), (
            sc, [a for a in got if list(got.values()).count(got[a]) > 1])


def test_no_frame_declares_a_hand_drawn_element():
    """THE ROUND'S HEADLINE CLAIM, read off the sidecars the sweep writes.

    A frame with a hand-drawn element is a prototype's taste standing where a
    kit's answer should be, and the sidecar is where `render.py` declares one.
    All 66 say the same sentence, and this is what keeps saying it after the
    next edit to `screens.py`."""
    drawn = [f.name for f in FRAMES.glob("*.candidates.md")
             if "Nothing was drawn by hand" not in f.read_text(encoding="utf-8")]
    assert not drawn, drawn


# ---------------------------------------------------------------------------
# inc38 (inheritors-2) — the button's walls, in the language that has no boxes
# ---------------------------------------------------------------------------
#: the four states a button has. `component_states("button")` derives them; the
#: literal tuple is what keeps a derivation defect from taking these laws down
#: with a KeyError instead of going red where it belongs — `verify_language`'s
#: own BFOUR, same reason.
BUTTON_STATES = (LG.DEFAULT, LG.FOCUSED, LG.ACTIVE, LG.DISABLED)
#: what swiss's `button.main` said before this increment, kept HERE and not in
#: the kit: it is the state the teeth test restores, and a constant living in
#: the test is the only copy of it that nothing can reach by accident
SWISS_WALLS = {LG.DEFAULT: "│  │", LG.FOCUSED: "┃  ┃", LG.ACTIVE: "█  █",
               LG.DISABLED: "┆  ┆"}


def is_wall(ch: str) -> bool:
    """A mark that can BUILD A BOX — derived from the codepoint, not listed.

    The Box Drawing block minus its three diagonals, plus every Block
    Element. A hand list would only catch the marks whoever wrote it thought
    of, and the claim under test is "no box AT ANY WIDTH", which is a claim
    about marks nobody has thought of yet.

    THE DIAGONALS ARE EXCLUDED ON PURPOSE AND IT IS NOT A LOOPHOLE. `╲ ╱` is
    swiss's own `DANGER_FORM`, which `Kit.button` sets around the WORD and not
    around the field — a stroke that leans closes no corner, and inc16's law
    already governs it. The law below is asked of the danger button too, so
    those two are the only marks in this range it may contain."""
    return (0x2500 <= ord(ch) <= 0x257F and ch not in "╱╲╳") \
        or 0x2580 <= ord(ch) <= 0x259F


def test_swiss_puts_no_wall_around_a_button_at_any_width():
    """§2, LITERALLY: "no boxes — ALIGNMENT DOES THE DIVIDING", at any width.

    This is `inheritors-2` §8's last recorded debt. Swiss drew
    `│   Cancel   │` — a pair of full-height vertical rules, which is a
    border-shaped mechanism in the one language committed against borders at
    every width, and it is the very stroke swiss is already in
    `PANE_SPLIT_REFUSED` for refusing between two panes.

    THREE WIDTHS, because the seat takes one and the defect blueprint's pane
    split carried for eight increments was "the only width anyone tested was
    the only width anyone calls": below the label (`w=1`, no padding at all),
    at the dialog's own (10), and at this language's own MEASURE_MIN (24)."""
    k = LG.kit("swiss")
    bad = [(w, st, danger, ch)
           for w in (1, 10, k.MEASURE_MIN)
           for st in BUTTON_STATES
           for danger in (False, True)
           for ch in plain(k.button("Cancel", w, st, danger)) if is_wall(ch)]
    assert not bad, bad


def test_the_swiss_button_keeps_its_states_apart_without_a_wall_or_a_hue():
    """THE CLAIM THE WALLS WERE DEFENDED WITH, disproved by measurement.

    The comment this increment deleted said the walls could not go because
    "with the walls gone the four states would separate on COLOUR ALONE".
    They do not: the mark leading the field is a WEIGHT ladder, weight is a
    shape channel, and this asks for it with the colour stripped at the source
    — four states, four different strings of cells, one width so the word
    cannot move under the state.

    FOCUS AND PRESS ARE ASKED TWICE, once inside the four and once on their
    own, because they are the pair `verify_language` singles out: a button
    that only changes hue when pressed says nothing, and ACTIVE is the state
    the component exists for."""
    k = LG.kit("swiss")
    got = {st: plain(k.button("Cancel", 10, st)) for st in BUTTON_STATES}
    assert len(set(got.values())) == 4, got
    assert len({len(v) for v in got.values()}) == 1, got
    assert got[LG.ACTIVE] != got[LG.FOCUSED], got
    assert got[LG.FOCUSED] != got[LG.DEFAULT], got
    assert all(v.count("Cancel") == 1 for v in got.values()), got


def test_the_swiss_buttons_ladder_is_made_of_marks_it_already_spends():
    """DERIVED FROM THE LANGUAGE'S OWN TOKENS, NOT FROM A NEW GLYPH.

    A mechanism invented for one seat is a mark a reader has to learn twice.
    Every cell in this button appears somewhere else in swiss's own
    declaration — `·` is `LEVELS["info"]`, `•` is `REQUIRED` (inc35: the
    ladder's mark set solid) and `●` is this language's own pressed cell,
    already worn by its radio knob. Asserted against the declaration rather
    than typed, so a later edit reaching for a mark from outside the alphabet
    is red here.

    DISABLED IS AIR, and the blank is asserted rather than tolerated: there is
    nothing lighter than `·` in this alphabet that is not a dashed RULE, which
    is the shape being given up. `stepper.step`'s own end behaviour, one slot
    over — the mark is simply not set."""
    k = LG.kit("swiss")
    elsewhere = set()
    for key, tbl in k.PART_GLYPHS.items():
        if not key.startswith("button"):
            elsewhere |= set("".join(tbl.values()))
    elsewhere |= set("".join(k.LEVELS.values())) | {k.REQUIRED, k.DISCLOSE}
    cells = set("".join(k.PART_GLYPHS["button.main"].values())) - {" "}
    assert cells <= elsewhere, sorted(cells - elsewhere)
    assert k.PART_GLYPHS["button.main"][LG.DEFAULT].strip() == k.LEVELS["info"]
    assert k.PART_GLYPHS["button.main"][LG.FOCUSED].strip() == k.REQUIRED
    assert not k.PART_GLYPHS["button.main"][LG.DISABLED].strip()


def test_putting_the_walls_back_makes_the_no_wall_law_go_red(monkeypatch):
    """TEETH, BOTH WAYS — the law can fire, and it fires on the real defect.

    Arm one restores swiss's pre-inc38 declaration, byte for byte, and the
    law above goes red on the mark it was written for. Arm two DELETES the
    declaration instead, which is the other way a language loses its answer:
    `part_key` falls back to the unscoped `main` and the button comes back
    wearing the slider's track. Both are walls; neither is silent.

    A law nobody has watched fail is a law nobody has watched."""
    def walls_in_render():
        return [ch for st in BUTTON_STATES
                for ch in plain(LG.kit("swiss").button("Cancel", 10, st))
                if is_wall(ch)]

    assert not walls_in_render()
    monkeypatch.setitem(LG.Swiss.PART_GLYPHS, "button.main", SWISS_WALLS)
    assert "│" in walls_in_render()
    monkeypatch.delitem(LG.Swiss.PART_GLYPHS, "button.main")
    assert walls_in_render()
    assert LG.kit("swiss").part_key("button", "main") == "main"


@pytest.mark.parametrize("lang", sorted(LG.PANE_SPLIT_REFUSED))
def test_no_language_that_refuses_the_pane_rule_draws_it_round_its_button(lang):
    """THE OTHER TEN, ASKED THE SAME QUESTION — off a REGISTRY rather than
    off a reviewer's eye.

    A language that has declared, with a citation, that it may not rule a
    vertical stroke between two panes may not rule one either side of a word
    either. The mark is `Kit.PANE_RULE`, the base's own hairline, which is
    what the five in that table refused — so this law grows with the table
    instead of with a hand list, and a sixth language joining
    `PANE_SPLIT_REFUSED` is asked about its button the moment it is added.

    SWISS WAS THE ONLY ONE OF THE FIVE THAT FAILED IT. The other four answer
    with their own alphabets — blueprint's registration pair, darkside's
    weight marks, solari's seam, prism's dots — and the measured frame for
    all eleven is in inc38 §3."""
    k = LG.kit(lang)
    declared = "".join(k.PART_GLYPHS["button.main"].values())
    assert LG.Kit.PANE_RULE not in declared, (lang, declared)
    for st in BUTTON_STATES:
        assert LG.Kit.PANE_RULE not in plain(k.button("Cancel", 10, st)), lang


# ---------------------------------------------------------------------------
# inc37 (inheritors-2) — every language is photographed, not just the five
# ---------------------------------------------------------------------------
SCREENS = ("S1", "S2", "S3", "S4", "S5", "S6")


def test_every_language_has_a_frame_for_every_screen():
    """THE DEFECT THIS GUARDS IS A LIST, and it has already happened once.

    `render.py` swept a typed list of five languages for two batches. The six
    that were not on it inherited seat after seat and then, in inc32/35/36,
    got thirty-eight mechanisms of their own — held by property tests and by
    nothing anyone could look at. The list is now read off `LG.KITS`; this is
    what says so from the outside, on the artefacts rather than on the source,
    so a kit added later that nobody sweeps is red here.

    The `.txt` is the file every law in this repo measures (the `.svg` carries
    the two marks a cell grid cannot show), so it is the one asked for."""
    missing = [f"{lang}_{sc}.txt" for lang in LANGS for sc in SCREENS
               if not (FRAMES / f"{lang}_{sc}.txt").exists()]
    assert not missing, missing
    assert len(list(FRAMES.glob("*_S?.txt"))) == len(LANGS) * len(SCREENS)


def test_no_two_languages_render_a_screen_identically():
    """`render.py`'s own sweep law, asserted where the gate runs it.

    Two languages agreeing on a WHOLE screen is the exact defect
    LANGUAGES.md records — "a language that only changes colour is not a
    language" — and until now it was checked only inside a prototype script
    that pytest does not run. 55 pairs per screen, 330 in all.

    It reads the shipped `.txt` rather than re-rendering: a re-render here
    would need Textual and a settle, and the artefact is what a reader
    judges."""
    for sc in SCREENS:
        got = {lang: (FRAMES / f"{lang}_{sc}.txt").read_text(encoding="utf-8")
               for lang in LANGS}
        assert len(set(got.values())) == len(LANGS), (
            sc, [a for a in got if list(got.values()).count(got[a]) > 1])


def test_no_frame_declares_a_hand_drawn_element():
    """THE ROUND'S HEADLINE CLAIM, read off the sidecars the sweep writes.

    A frame with a hand-drawn element is a prototype's taste standing where a
    kit's answer should be, and the sidecar is where `render.py` declares one.
    All 66 say the same sentence, and this is what keeps saying it after the
    next edit to `screens.py`."""
    drawn = [f.name for f in FRAMES.glob("*.candidates.md")
             if "Nothing was drawn by hand" not in f.read_text(encoding="utf-8")]
    assert not drawn, drawn
