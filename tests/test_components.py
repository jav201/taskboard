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
    mark on the field are the same claim.

    AND THE LADDER IS NOT MADE OF THEM ANY MORE (inc45). `LEVELS` read
    `† ` / `‡ `, so `†` meant "this entry must be made" beside a caption and
    "there is a warning about this" on a log row — two claims, one mark, no
    channel between them. The ladder now takes the FIRST mark of the
    printer's order, `*`, doubled for the graver note; the daggers are an
    order of TWO and nothing else, which is what this test's title claimed
    all along."""
    k = LG.kit("ledger")
    assert plain(k.required()) == "†"
    assert k.field_form(LG.INVALID, "textfield")[0] == "‡"
    assert not {"†", "‡"} & set("".join(k.LEVELS.values()))
    assert k.LEVELS["error"].strip() == "**"


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
#:
#: INSTRUMENT'S ENTRY IS THE MIRROR OF WHAT IT WAS, and the reason is written
#: here rather than lost: inc46 turned this language's rails round so the dots
#: face the words (`⠸ … ⠇` where it used to set `⠇ … ⠸`), because `⠇` is the
#: error rung and it was OPENING the safe button. The pre-inc39 defect was
#: literally `⠸⠶⠇`; under the new orientation that string is LEGAL, and the
#: exchanged form -- the thing this constant exists to restore -- is `⠇⠶⠸`.
#: The defect being restored is the same defect; only its spelling moved.
FLIPPED_INVALID = {"nord": "] [", "instrument": "⠇⠶⠸",
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
#:
#: SWISS JOINED THE SET IN inc46, which is exactly what this roster is for.
#: Its field used to close with the same rule it opened with (`│ │`); with the
#: enclosure gone it opens with a rule and closes with AIR, so opens and
#: closes are different vocabularies and the law can fire on it. Nobody
#: decided that; the derivation below noticed it and this line is where it
#: had to be written down.
HANDED_FIELDS = ("instrument", "swiss", "industrial", "nord", "ledger",
                 "blueprint")


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
# inc41 (rework-1) - the SVG paints the tier the kit declared, and nothing else
# ---------------------------------------------------------------------------
#: every markup tag in a composed row, escaped brackets lifted out first —
#: `plain()`'s own order, applied to the tags instead of to the cells.
_TAG_BODY = re.compile(r"\[([^\]]*)\]")
#: a tag that sets a GROUND. Rich spells it `fg on bg` or bare `on bg`, and
#: both shapes are in these kits: blueprint's knockout is the first, the plate
#: industrial stamps under a card is the second.
_ON_TAG = re.compile(r"(?:^|\s)on\s+(\S+)$")
#: the four style words a kit can reach for. `reverse` is the one that IS a
#: ground channel, which is why it is listed beside the three that are not.
_STYLE_WORDS = ("reverse", "bold", "underline", "italic")
#: the frames that declare at least one ground, measured rather than assumed —
#: the roster the ground law is non-vacuous on. 14 of 66; the other 52 declare
#: none and paint none, which is a true pass and an empty one.
#:
#: `industrial_S6` JOINED THE ROSTER IN inc43 without one glyph changing. Its
#: `MATCH_STYLE` is `reverse {accent}`, which was always a ground declaration
#: wearing a style word's costume; before inc43 neither this list nor the
#: exporter could see it. `solari_S6` was already here for a different reason
#: (its bands) and its `reverse {ink}` resolves to the SAME hue those bands
#: use, so the SET did not move even though six new rects did.
GROUNDED_FRAMES = ("industrial_S1", "darkside_S1", "prism_S1", "ledger_S1",
                   "solari_S1", "solari_S2", "solari_S3", "prism_S4",
                   "ledger_S4", "solari_S4", "blueprint_S4", "solari_S5",
                   "solari_S6", "industrial_S6", "darkside_S6")


def sheet_rows(lang, screen):
    """The composed MARKUP of a frame, from the sheet that made it.

    The only place the tiers exist as DECLARATIONS: the `.txt` has them
    stripped and the `.svg` has them rendered, so neither can say what was
    asked for. `screens.py` imports without Textual — unlike `render.py`,
    which is why FRAMES is a path and not an import — and it needs the repo
    root, `prototypes/` and `prototypes/components/` on the path for its own
    `fixture` import."""
    import sys
    for p in (FRAMES.parents[1], FRAMES.parent, FRAMES):
        if str(p) not in sys.path:
            sys.path.insert(0, str(p))
    import screens
    return screens.build(lang, screen).rows


def declared_grounds(lang, screen):
    """The set of ground colours this frame's composition asks for.

    TWO SPELLINGS, AND THE SECOND IS WHY inc41 MEASURED A GAP THAT WAS NOT
    THERE. `[#123 on #456]` is the obvious one. `[reverse #456]` is the other:
    a reversed run paints its hue as the GROUND and the cell's own ground as
    the ink — the same channel, said backwards. Until inc43 the exporter
    dropped it and this helper did not count it, so the two agreed on zero and
    `industrial_S6` read as a frame that declares no ground. It declares six."""
    out = set()
    for row in sheet_rows(lang, screen):
        for m in _TAG_BODY.finditer(row.replace("\\[", _ESC)):
            body = m.group(1).strip()
            hit = _ON_TAG.search(body)
            if hit:
                out.add(hit.group(1))
            parts = body.split()
            if len(parts) == 2 and parts[0] == "reverse":
                out.add(parts[1])
    return out


def declared_styles(lang, screen):
    """The style-tier runs this frame's composition asks for: `(word, text)`.

    Separate from the grounds because the exporter treats them differently —
    which is the whole finding below."""
    out = []
    for row in sheet_rows(lang, screen):
        for m in _TAG_BODY.finditer(row.replace("\\[", _ESC)):
            body = m.group(1).strip()
            if body.split(" ")[0] in _STYLE_WORDS:
                out.append(body)
    return out


def painted_grounds(lang, screen):
    """The grounds the `.svg` actually paints. The FIRST `<rect>` is the
    sheet's own canvas — `svg_from_grid` writes it before any cell run — so it
    is dropped by POSITION rather than by colour: two languages ground their
    page in a colour a cell could also carry."""
    svg = (FRAMES / f"{lang}_{screen}.svg").read_text(encoding="utf-8")
    return set(re.findall(r'<rect[^>]*fill="([^"]+)"', svg)[1:])


@pytest.mark.parametrize("lang", LANGS)
def test_the_svg_paints_exactly_the_grounds_the_kit_declared(lang):
    """THE TIER LAW, over all six screens of every language: the `.svg` paints
    the ground a kit asked for, nothing it did not ask for, and nothing else.

    THIS IS THE QUESTION `PROTOTYPE-inheritors.md` §0b ASKED AND ANSWERED THE
    WRONG WAY. It found `blueprint_S4.svg` painting `DELETE` as the sheet's
    knockout while `blueprint_S4.txt` shows a bare word, and concluded that
    "the exporter answered by itself" — that a design decision nobody made had
    been taken by `svg_from_grid`. It had not. The exporter has no opinion:
    across 66 frames it paints the declared set exactly, and the declaration
    for that cell is `screens.s4_blueprint` calling `knockout_cell`, under
    operator ruling 10 (§ the next test).

    Compared as SETS and not as counts on purpose. A ground run crossing a row
    boundary becomes several `<rect>`s — prism declares one and gets 22 — so
    counting would assert a fact about Textual's segmentation instead of about
    the kit. What the law is for is a colour appearing that nobody asked for,
    or one that was asked for and did not arrive."""
    for screen in SCREENS:
        assert declared_grounds(lang, screen) == painted_grounds(lang, screen), \
            (lang, screen, declared_grounds(lang, screen),
             painted_grounds(lang, screen))


def test_the_ground_law_is_not_vacuous():
    """WHICH FRAMES THE LAW ACTUALLY BITES ON, measured and written down.

    52 of the 66 declare no ground and paint none: a true pass, and an empty
    one. The 14 that do are the law's whole evidence, so the roster is derived
    and compared with a written one — a frame that stops declaring a ground
    (blueprint's knockout going away, solari's bands going flat) changes this
    list and somebody has to look at it.

    IT WAS 13 UNTIL inc43 AND THE FOURTEENTH IS THE POINT. `industrial_S6`
    declared six reversed runs the whole time; the roster could not see them
    because `declared_grounds` only knew the `on <colour>` spelling, and the
    exporter could not paint them for the mirror-image reason. Two blind spots
    facing each other read as agreement. This list is where that shows up.

    AND IT IS 15 SINCE inc48: `darkside_S6` joined it, because that language's
    `MATCH_STYLE` stopped being `bold {ink}` — weight, in a language that has
    renounced hue by commitment, on terminals that render bold as "brighter"
    — and became a ±1 grey STEP of ground, which is the channel §8 says this
    language owns. A frame arriving on this roster is the same event as a
    frame leaving it, and both have to be looked at."""
    got = tuple(f"{lang}_{sc}" for sc in SCREENS for lang in LANGS
                if declared_grounds(lang, sc))
    assert sorted(got) == sorted(GROUNDED_FRAMES), got
    assert len(got) == 15


def test_blueprints_knockout_is_where_operator_ruling_10_put_it():
    """NOT A DEFECT — A RULING, MADE ON 2026-09-04 AND RECORDED.

        "10. Blueprint's knockout may MOVE from the title block to the default
             answer in a confirm — exactly one per view."
        (`.fast-dev-flow/archive/spec-20260905-kits-learn-3-closed.md` §6.1,
         the operator's ten rulings; implemented by inc17, cited at
         `Kit.knockout_cell` and at `screens.s4_blueprint`.)

    `PROTOTYPE.md` §4 is the list of questions PUT to the operator, and the
    round read its question 10 as unanswered. All ten were answered; this one
    was answered yes. So the `.svg` painting `DELETE` is the ruling being
    obeyed, and the `.txt` not showing it is the limit `knockout_cell`'s own
    docstring records — "the one mark in this file that does not survive the
    `.txt` ... the honest place to read a knockout is the SVG" — which
    `PROTOTYPE.md` §3 had already published as a collateral finding.

    THE TITLE BLOCK LOST NOTHING, which is what makes the move legal rather
    than merely permitted. The state cell reverses on the `alert` mood alone,
    and the seeded board is calm — so the sheet's one knockout was UNSPENT and
    the confirm could take it. "Exactly one per view" holds by arithmetic. The
    mechanism is exercised in both moods here, so "the title block carries no
    knockout" is shown to be an unspent law and not a dead one."""
    k = LG.kit("blueprint")
    assert k.knockout_cell(" DELETE ") == \
        f"[{k.t['ground']} on {k.c['ink']}] DELETE [/]"
    assert declared_grounds("blueprint", "S4") == {k.c["ink"]}
    svg = (FRAMES / "blueprint_S4.svg").read_text(encoding="utf-8")
    pair = re.search(r'<rect[^>]*fill="%s"/>\s*<text[^>]*fill="([^"]+)"[^>]*>'
                     r'([^<]*)</text>' % re.escape(k.c["ink"]), svg)
    assert pair, svg[:200]
    assert pair.group(1) == k.t["ground"]
    assert pair.group(2).replace("\u00a0", " ") == " DELETE "

    # the title block's own cell: unspent, not absent
    assert k.mood != "alert"
    assert k._state_cell() == ("├ CLEAR ┤", False)
    calm = LG.kit("blueprint")
    calm.mood = "alert"
    assert calm._state_cell()[1] is True, "the first-fixation law is dead"


#: the sheet's own query, from the fixture the six result rows are built from.
#: It is the DISCRIMINATOR a painted count needs and not a convenience: solari
#: reverses to `#f0ede4`, which is exactly the colour its S6 bands already use,
#: so counting rects by fill alone would score two bands as match runs; and the
#: query also appears in the search FIELD one row above the results, so counting
#: `<text>` by content alone would score seven where six were declared.
QUERY = "re"
#: `svg_from_grid`'s cell width. A reversed match run is the query's own cells
#: turned into a ground, so its rect is exactly this wide.
CELL_W = 8.4


def painted_styles(lang, screen):
    """The style-tier runs the `.svg` actually paints, as a list of words.

    TWO SHAPES, BECAUSE THE TIER HAS TWO SHAPES. `bold` and `underline` are
    properties of the text and arrive as attributes on a `<text>`. `reverse`
    is not and must not be looked for as one: it is a GROUND channel wearing a
    style word's costume, so `cell_grid` resolves it back into the (ink,
    ground) pair it always was and what reaches the `.svg` is a `<rect>` of the
    declared hue with the query painted on it in the cell's own ground.

    A reversed run is therefore counted as a rect of the declared hue that is
    exactly the query wide — both halves load-bearing, and §QUERY says which
    frame breaks without which half."""
    svg = (FRAMES / f"{lang}_{screen}.svg").read_text(encoding="utf-8")
    out = []
    for m in re.finditer(r"<text[^>]*>", svg):
        if 'font-weight="bold"' in m.group(0):
            out.append("bold")
        if 'text-decoration="underline"' in m.group(0):
            out.append("underline")
    hue = LG.kit(lang).MATCH_STYLE.split()[-1].format(**LG.kit(lang).c)
    wide = f'width="{len(QUERY) * CELL_W:.1f}"'
    for m in re.finditer(r"<rect[^>]*/>", svg):
        if wide in m.group(0) and f'fill="{hue}"' in m.group(0):
            out.append("reverse")
    return out


@pytest.mark.parametrize("lang", LANGS)
def test_the_svg_paints_exactly_the_style_runs_the_kit_declared(lang):
    """THE OTHER TIER, AND IT IS NOW A LAW INSTEAD OF A RECORDED DEFECT.

    `Kit.match` is the one contract seat whose emphasis may not add a cell —
    operator ruling 9, the result text comes back byte for byte — so every one
    of the eleven spells `MATCH_STYLE` as a STYLE over a hue: seven `bold`, two
    `underline`, and industrial/solari `reverse`. Each S6 sheet declares six
    such runs, 66 across the eleven.

    inc41 measured 66 declared and 0 painted and asserted that as a fact,
    because painting them re-renders every `.svg` and re-opens the round that
    judged them (`PROTOTYPE-inheritors.md` §7 q9). inc43 painted them. THIS IS
    THE SAME COMPARISON inc41 RAN, with the answer it could not have: equal, in
    11 of 11.

    THE WORD MUST MATCH TOO, not just the count. A language that declares
    `bold` and paints an underline would satisfy an arithmetic law and be
    wrong; the run's own word is asserted against the kit's `MATCH_STYLE`. And
    the negative half is asserted with it — a `bold` language's S6 carries no
    `text-decoration` at all, which is what stops "six of something" from
    passing for "six of the right thing"."""
    declared = declared_styles(lang, "S6")
    assert len(declared) == 6, (lang, declared)
    word = LG.kit(lang).MATCH_STYLE.split()[0]
    assert word in _STYLE_WORDS, (lang, word)
    assert {d.split()[0] for d in declared} == {word}, (lang, declared)

    painted = painted_styles(lang, "S6")
    assert len(painted) == len(declared), (lang, declared, painted)
    assert set(painted) == {word}, (lang, painted)

    svg = (FRAMES / f"{lang}_S6.svg").read_text(encoding="utf-8")
    for other in ("bold", "underline"):
        attr = ('font-weight="bold"' if other == "bold"
                else 'text-decoration="underline"')
        assert (attr in svg) == (word == other), (lang, word, other)


def test_the_style_law_is_not_vacuous_and_the_reverse_kits_are_the_proof():
    """WHERE THE LAW BITES, and the one case that could have passed hollow.

    Six of the eleven are `bold` and two are `underline`: for those, "the
    exporter learned the tier" is one attribute on one element and the law is
    honest but easy. The THREE that are `reverse` are the ones inc41 called the
    sharp case — the same ground channel this exporter paints 16 times in
    `industrial_S1` and dropped entirely in `industrial_S6`, because Rich hands
    `reverse` over as a style FLAG with colour and bgcolor still in their
    declared order.

    So the swap itself is asserted, not just its arithmetic: each of the six
    runs paints the query in the CELL'S OWN GROUND on a rect of the kit's hue.
    Painting the hue as ink on the ground would keep the count at six and mean
    nothing had been fixed.

    AND THE SEVENTH `re` IS THE TEETH. The query also sits in the search field
    one row above the results, painted in ordinary ink. It is in every one of
    the eleven frames and it is NOT a match run; a measurement that counted
    text content would score 7 here and 7 is the number this test refuses."""
    words = {lang: LG.kit(lang).MATCH_STYLE.split()[0] for lang in LANGS}
    assert sorted(words.values()).count("reverse") == 3
    assert {l for l, w in words.items() if w == "reverse"} == {"industrial",
                                                              "solari",
                                                              "darkside"}

    for lang in ("industrial", "solari", "darkside"):
        k = LG.kit(lang)
        hue = k.MATCH_STYLE.split()[-1].format(**k.c)
        svg = (FRAMES / f"{lang}_S6.svg").read_text(encoding="utf-8")
        canvas = re.search(r'<rect width="[\d.]+" height="[\d.]+" '
                           r'fill="([^"]+)"/>', svg)
        assert canvas, lang
        ground = canvas.group(1)
        assert ground != hue, (lang, hue)
        # the six runs: the query, in the page's ground, and nothing else
        on_ground = re.findall(r'<text[^>]*fill="%s"[^>]*>([^<]*)</text>'
                               % re.escape(ground), svg)
        assert on_ground == [QUERY] * 6, (lang, on_ground)
        # and the seventh `re` -- the search field -- is NOT one of them
        every = re.findall(r'<text[^>]*fill="([^"]+)"[^>]*>%s</text>'
                           % re.escape(QUERY), svg)
        assert len(every) == 7, (lang, every)
        assert every.count(ground) == 6, (lang, every)
        assert len(painted_styles(lang, "S6")) == 6, lang


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


def test_the_swiss_buttons_ladder_is_one_shape_at_three_weights():
    """ONE SHAPE, THREE WEIGHTS — and NOT the marks that mean something.

    inc38 built this ladder out of `· • ●` and asserted that every cell in it
    appeared elsewhere in swiss's own declaration, which was the right
    instinct and the wrong set: `·` is `LEVELS["info"]` and `•` is `REQUIRED`,
    so two of the three rungs were DECLARATIONS. `swiss_S3` is what that
    renders as — `· ╲Delete all╱`, the lowest rung of the severity ladder
    opening the most dangerous control on the screen — and `swiss_S4` puts
    `•`, the obligation mark, on the focus ring of an irreversible button.

    SO THE LAW CHANGED SHAPE WITH THE LADDER. "Made of marks it already
    spends" is replaced by something stronger and narrower: the ladder is ONE
    shape at three weights, the shape is the square bullet this language
    already declares for a box, and NO rung may be a mark that means
    something. `▫` and `■` are not new ideas — they are `▪` hollow and `▪`
    full — but they ARE new code points, and that is the trade this test now
    records instead of hiding.

    DISABLED IS STILL AIR, asserted rather than tolerated: there is nothing
    lighter than the hollow square in this alphabet that is not a dashed
    RULE, which is the shape being given up."""
    k = LG.kit("swiss")
    rungs = [k.PART_GLYPHS["button.main"][st].strip()
             for st in (LG.DEFAULT, LG.FOCUSED, LG.ACTIVE)]
    assert rungs == ["▫", "▪", "■"], rungs
    assert not k.PART_GLYPHS["button.main"][LG.DISABLED].strip()
    meanings = set("".join(k.LEVELS.values())) | {k.REQUIRED} | set(k.DANGER_FORM)
    assert not (set(rungs) & meanings), sorted(set(rungs) & meanings)
    # the square bullet the ladder is three weights OF is still the checkbox's
    # own checked mark, so the shape is the language's and not the test's
    assert "▪" in k.PART_GLYPHS["checkbox.knob"][LG.DEFAULT]


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


# ===========================================================================
# inc45 (rework-3) — one mark, one meaning
# ===========================================================================
#: THE FOUR LANGUAGE-LEVEL DECLARATIONS THAT MEAN SOMETHING ABOUT THE WORK,
#: read straight off the kit: how bad it is (the severity LADDER, all three
#: rungs as ONE declaration), whether the control destroys (`DANGER_FORM`),
#: whether the field is compulsory (`REQUIRED`), and where the reader is
#: (`CUR`). Three rungs count as one because the census counts them as one:
#: "two severity rungs sharing a cell is a severity problem, not a collision"
#: (`prototypes/collision_census.py`).
def _meaning_marks(k) -> dict[str, str]:
    return {"ladder": "".join(k.LEVELS[x] for x in ("info", "warn", "error")),
            "danger": "".join(k.DANGER_FORM),
            "required": k.REQUIRED,
            "cursor": k.CUR}


#: not a cell — the ASCII space and U+2800 BRAILLE PATTERN BLANK, the same
#: pair the census discards. A language that pads two roles with the same
#: nothing has not overloaded anything.
BLANKS = " ⠀"

#: THE ONE EXEMPTION, BY NAME AND WITH ITS CITATION. `DANGER_FORM` may be the
#: severity ladder's TOP rung set around the label — one claim about one
#: gravity, said as a FORM rather than as a rung, which is what
#: `Kit.DANGER_FORM` declares it to be ("a pair of marks that bracket the
#: label INSIDE the walls ... the form is therefore the WHOLE channel"). It is
#: the TOP rung or nothing: nord's `!` (warn) and corgi's `▄▄` (warn) were
#: both this exemption spent one rung too low, and inc45 moved both.
DANGER_IS_THE_TOP_RUNG = {
    "naught": "`∙∙` — LEVELS[error]; two lit dots, and not the one red",
    "corgi": "`██` — LEVELS[error]; the segment driven to full height",
    "prism": "`⣿⣿` — LEVELS[error]; nothing left to burn",
    "blueprint": "`━━` — LEVELS[error]; the HEAVY weight, this alphabet's "
                 "loudest mark",
}


def _cells(glyph: str) -> set[str]:
    return {ch for ch in glyph if ch not in BLANKS}


def shared_cell_pairs(lang: str) -> list[tuple]:
    """Every pair of meaning marks that shares a cell, as
    `(role, role, the shared cells, mark, mark)`.

    A FUNCTION AND NOT AN INLINE LOOP, because the teeth test below has to
    read WHICH pair fired: pytest's assertion rewriting turns an assert's own
    message into a formatted string long before a caller can inspect it, so a
    teeth test that scraped `AssertionError.args` would be asserting on a
    repr."""
    k = LG.kit(lang)
    marks = _meaning_marks(k)
    exempt = (lang in DANGER_IS_THE_TOP_RUNG
              and marks["danger"] == k.LEVELS["error"])
    names = sorted(marks)
    out = []
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            shared = _cells(marks[a]) & _cells(marks[b])
            if not shared:
                continue
            if exempt and {a, b} == {"danger", "ladder"}:
                continue
            out.append((a, b, "".join(sorted(shared)), marks[a], marks[b]))
    return out


@pytest.mark.parametrize("lang", LANGS)
def test_a_languages_meaning_marks_do_not_share_a_cell(lang):
    """ONE MARK, ONE MEANING — asked of all eleven, off the declarations.

    `PROTOTYPE-inheritors.md` left sixteen `rework` frames and the census
    (inc44) measured what most of them are: a language with a small alphabet
    spends one cell on severity or obligation and then spends the same cell
    on something else that also MEANS something. Six of those were two
    meanings on one mark with no control involved at all — `naught ∙` carried
    five, `swiss ━` was the cursor AND the error rung, `nord !` was warn AND
    the destructive form, `industrial ▪` was warn AND the cursor,
    `darkside O` was error AND the cursor, `ledger † ‡` were obligation and
    refusal AND the two severity rungs.

    THE LAW. In one language, the four marks that carry a MEANING may not
    share a cell. Not "may not be equal" — SHARE, because the defect the
    round photographed is a reader meeting a familiar cell in an unfamiliar
    seat, and `industrial ▪` against `▪▪` proves that doubling a mark for
    alignment is not a channel: the first cell of the rung is the cursor
    either way.

    THE LADDER IS ONE DECLARATION, not three. Its rungs are MEANT to share
    cells — that is what a ladder is, and the census makes the same choice for
    the same reason.

    INVALID IS NOT IN THIS SET, and the exclusion is named rather than
    silent (VERIFY.md, "assert distinctness on the channel that is left"):
    inc39 ruled that where un-flipping a field's walls would collide with
    DEFAULT byte for byte, the walls take that language's own `DANGER_FORM`
    (spec §9.2). Five languages spell rejection with their danger form ON
    PURPOSE, so a law over `INVALID` would be a law over that ruling. inc39's
    own law governs those slots.

    THE ONE EXEMPTION is `DANGER_IS_THE_TOP_RUNG`, by name and with the
    citation each kit carries."""
    k = LG.kit(lang)
    if lang in DANGER_IS_THE_TOP_RUNG:
        assert "".join(k.DANGER_FORM) == k.LEVELS["error"], (
            lang, k.DANGER_FORM, k.LEVELS)
        assert DANGER_IS_THE_TOP_RUNG[lang].strip(), lang
    assert not shared_cell_pairs(lang), (lang, shared_cell_pairs(lang))


def test_the_one_mark_one_meaning_law_goes_red_on_the_six_it_was_written_for(
        monkeypatch):
    """TEETH — the six declarations inc45 moved, restored one at a time.

    A law that has never been watched fail is a law nobody has watched, and
    this one has to name the LANGUAGE and the TWO ROLES when it fires or the
    next reader gets a boolean. Each arm restores exactly the byte string
    HEAD carried before this increment; the assertion checks that the pair
    the round complained about is the pair reported.

    The seventh arm is the exemption's own teeth: corgi's danger form put
    back one rung DOWN the ladder — `▄▄` is `LEVELS["warn"]` — must be red,
    because the exemption is for the TOP rung and for nothing else."""
    def roles(lang):
        return {frozenset(row[:2]) for row in shared_cell_pairs(lang)}

    for lang in LANGS:
        assert not roles(lang), lang

    monkeypatch.setattr(LG.Naught, "CUR", "∙")
    assert frozenset(("cursor", "ladder")) in roles("naught")
    monkeypatch.setattr(LG.Naught, "REQUIRED", "∙")
    assert frozenset(("required", "ladder")) in roles("naught")

    monkeypatch.setattr(LG.Swiss, "CUR", "━")
    assert frozenset(("cursor", "ladder")) in roles("swiss")

    monkeypatch.setattr(LG.Kit, "DANGER_FORM", ("!", "!"))
    assert frozenset(("danger", "ladder")) in roles("nord")

    monkeypatch.setattr(LG.Industrial, "CUR", "▪")
    assert frozenset(("cursor", "ladder")) in roles("industrial")

    monkeypatch.setattr(LG.Darkside, "CUR", "O")
    assert frozenset(("cursor", "ladder")) in roles("darkside")

    monkeypatch.setattr(LG.Ledger, "LEVELS",
                        {"info": "  ", "warn": "† ", "error": "‡ "})
    assert frozenset(("required", "ladder")) in roles("ledger")

    monkeypatch.setattr(LG.Corgi, "DANGER_FORM", ("▄", "▄"))
    assert frozenset(("danger", "ladder")) in roles("corgi")
    with pytest.raises(AssertionError):
        test_a_languages_meaning_marks_do_not_share_a_cell("corgi")


# ===========================================================================
# inc46 (rework-3) — the other two seats the batch rule names
# ===========================================================================
#: the six controls the census reads, so the two files ask the same question
#: of the same set.
RULED_CONTROLS = ("button", "checkbox", "radio", "switch", "textfield",
                  "stepper")

#: WHAT IS STILL WRONG, COUNTED. Six languages draw a mark that MEANS
#: something at a seat the batch rule names — a DISABLED mark or a switch's
#: INDICATOR — and this roster is the measurement rather than a promise. It
#: is asserted exactly, both ways: a language that gets worse is red, and a
#: language that gets better is red until somebody edits this line, which is
#: the only way a roster stays a record instead of a decoration
#: (`HANDED_FIELDS`, one screen up, is the same bargain).
#:
#:   naught     8  `∙` is the switch's ON indicator and `◦` its dead one, and
#:                 both are rungs of the count ladder. Naught has ONE round
#:                 pixel at six charges; it has no unspent cell. Open.
#:   corgi      8  the segment bank: `▄▄` ON, `▁▁` dead — `LEVELS["warn"]`
#:                 and `LEVELS["info"]`. corgi has no increment in this
#:                 batch. Open.
#:   prism      8  `⣿` ON, `⣤` dead — the top two rungs. Open.
#:   blueprint  8  `╌` is `LEVELS["warn"]` and this language's whole DISABLED
#:                 vocabulary — five parts wear it. Open.
#:
#: SOLARI WAS 6 AND IS 0 (inc47): `▁` was `REQUIRED` and the switch's
#: indicator and eighteen more chrome seats; obligation moved to `▮` and the
#: seam went back to being alphabet. instrument and swiss went to zero in
#: inc46. Five of the eleven are clean.
MEANING_AT_A_NAMED_SEAT = {"naught": 8, "corgi": 8, "instrument": 0,
                           "swiss": 0, "industrial": 0, "nord": 0,
                           "darkside": 0, "prism": 8, "ledger": 0,
                           "solari": 0, "blueprint": 8}


def meaning_marks_at_named_seats(lang: str) -> list[tuple]:
    """Every DISABLED mark and every switch INDICATOR that is drawn with a
    cell this language spends on severity, danger or obligation.

    `CUR` is deliberately NOT in the set. The batch rule's second clause names
    three seats a MEANING may not stand at, and inc48's opener law names the
    same three declarations — `LEVELS`, `DANGER_FORM`, `REQUIRED`. A cursor
    says where the reader is, not what the work is worth, and a language that
    spends its cursor cell on a knob has not told anybody their data is
    rejected. Named, so the narrowing is a decision and not an oversight."""
    k = LG.kit(lang)
    meanings = (set("".join(k.LEVELS.values())) | {k.REQUIRED}
                | set("".join(k.DANGER_FORM))) - set(" ⠀")
    out = []
    for comp in RULED_CONTROLS:
        for part in LG.COMPONENT_PARTS[comp]:
            table = k.PART_GLYPHS[k.part_key(comp, part)]
            for st in LG.component_states(comp):
                dead = LG.control_of(st) == LG.DISABLED
                if dead and LG.DISABLED not in table:
                    # A FALLBACK IS NOT A DECLARATION, and `collision_census`
                    # already had to learn this: `part_glyph` walks the state
                    # chain, so a part with no `disabled` key returns its
                    # DEFAULT glyph. Crediting that to the DISABLED seat made
                    # solari's CARET a "disabled mark" the moment its
                    # obligation mark moved onto the caret's cell (inc47) --
                    # a field nobody may type in draws no caret at all.
                    continue
                glyph = k.part_glyph(part, st, comp)
                hit = set(glyph) & meanings
                if not hit:
                    continue
                if dead or (comp == "switch" and part == "indicator"):
                    out.append((f"{comp}.{part}", st, glyph,
                                "".join(sorted(hit))))
    return out


@pytest.mark.parametrize("lang", LANGS)
def test_a_meaning_never_stands_at_a_disabled_or_indicator_seat(lang):
    """THE BATCH RULE'S SECOND CLAUSE, at two of its three seats.

    A mark that means something about the WORK — a severity rung, the danger
    form, the obligation mark — may not stand where a reader would take it for
    that meaning. Three seats are named: the OPENER of a control (inc48), the
    INDICATOR of a switch, and a DISABLED mark. This law is the last two.

    THE FRAMES IT WAS WRITTEN OFF. `instrument_S3`: `⠁` is `REQUIRED` in `S2`
    and the DISABLED switch here, and the round's criterion is that showing
    the two screens in sequence produces two correct answers to "what does
    `⠁` mean" with no cue on either. `swiss_S1`/`S5`: `━` is the error rung
    and the switch's ON indicator, so a switch that is on and a row that has
    failed are one cell.

    IT IS A MEASUREMENT, NOT A PASS. Six languages still fail it and the count
    is asserted per language, so the roster can only move when somebody edits
    it. That is deliberate: a law scoped to the languages that already obey it
    would be a law that never says anything about the ones that do not."""
    assert len(meaning_marks_at_named_seats(lang))         == MEANING_AT_A_NAMED_SEAT[lang], (lang,
                                           meaning_marks_at_named_seats(lang))


def test_the_named_seat_law_goes_red_on_the_two_declarations_inc46_moved(
        monkeypatch):
    """TEETH — and they have to be, because five of the eleven arms of the law
    above assert a NON-ZERO count, which is the shape of assertion that rots
    into a snapshot if nobody watches it fire.

    Arm one restores instrument's dead rung to `⠁`, the obligation mark, on
    the one part `instrument_S3` photographed. Arm two restores swiss's switch
    indicator to `━`, the error rung. Each must move that language's count off
    zero, and each must name the part."""
    for lang in LANGS:
        assert (len(meaning_marks_at_named_seats(lang))
                == MEANING_AT_A_NAMED_SEAT[lang]), lang

    tbl = dict(LG.Instrument.PART_GLYPHS["checkbox.main"])
    tbl[LG.DISABLED] = "⠁"
    monkeypatch.setitem(LG.Instrument.PART_GLYPHS, "checkbox.main", tbl)
    hits = meaning_marks_at_named_seats("instrument")
    assert hits and all(h[0] == "checkbox.main" for h in hits), hits
    assert all(h[3] == LG.kit("instrument").REQUIRED for h in hits), hits
    monkeypatch.undo()

    tbl = dict(LG.Swiss.PART_GLYPHS["indicator"])
    tbl[LG.DEFAULT] = "━"
    monkeypatch.setitem(LG.Swiss.PART_GLYPHS, "indicator", tbl)
    hits = meaning_marks_at_named_seats("swiss")
    assert hits and all(h[0] == "switch.indicator" for h in hits), hits
    assert all(h[3] == LG.kit("swiss").LEVELS["error"] for h in hits), hits
    monkeypatch.undo()

    for lang in LANGS:
        assert (len(meaning_marks_at_named_seats(lang))
                == MEANING_AT_A_NAMED_SEAT[lang]), lang


# ===========================================================================
# inc48 (rework-3) — the opener law, the batch rule's first named seat
# ===========================================================================
#: THE STEPPER IS OUT, BY A RULING AND NOT BY CONVENIENCE. `stepper.main` and
#: `stepper.step` are two-cell strings whose halves are DIRECTIONS, not walls
#: — spec §9.5, inc39's own words when it declined to extend its INVALID law
#: there: "a stepper's halves are directions, not walls, so it needs its own
#: law". A law about what OPENS an enclosure cannot be asked of a pair that
#: encloses nothing, and the stepper's own law is still unwritten.
OPENING_CONTROLS = ("button", "checkbox", "radio", "switch", "textfield")

#: WHAT STILL OPENS WITH A MEANING, COUNTED — the same bargain
#: `MEANING_AT_A_NAMED_SEAT` and `HANDED_FIELDS` make, for the same reason:
#: a roster is a record only while somebody has to edit it.
#:
#:   naught      2  `◦` opens the button and the field, and `LEVELS["info"]`
#:                  is `◦◦`. This is the roster's arguable entry: naught's
#:                  info rung is ZERO LIT DOTS — the unlit lattice, which
#:                  LANGUAGES.md §0 calls this language's visible GROUND — so
#:                  "nothing is lit" and "an empty seat" may be one meaning
#:                  rather than two. The argument is written here and NOT
#:                  granted: an exemption is the operator's, and silence is
#:                  not one.
#:   corgi      31  the segment bank is `LEVELS` and the chrome ladder at
#:                  once (`▁▁ ▄▄ ██` against `▁▁ ▔▔ ▂▂ ··`). No increment in
#:                  this batch; this is the widest single roster entry in the
#:                  corpus.
#:   prism      19  `⣿` is `LEVELS["error"]`, the `DANGER_FORM` and the
#:                  opening cell of the button, the checkbox and the field.
#:   blueprint   6  `├` is `REQUIRED` and the dimension's opening terminator
#:                  — §9.4's `blueprint_S2`, still open.
#:
#: SEVEN ARE ZERO: instrument (inc46), swiss (inc46), industrial (inc48),
#: darkside (inc48), nord, ledger and solari (inc47).
MEANING_AT_AN_OPENER = {"naught": 2, "corgi": 31, "instrument": 0, "swiss": 0,
                        "industrial": 0, "nord": 0, "darkside": 0, "prism": 19,
                        "ledger": 0, "solari": 0, "blueprint": 6}


def meaning_marks_at_an_opener(lang: str) -> list[tuple]:
    """Every control glyph whose FIRST cell is a mark this language spends on
    severity, danger or obligation.

    ONE EXEMPTION, BY NAME AND WITH ITS RULING: a field whose INVALID walls
    are that language's own `DANGER_FORM`. inc39 ruled that where un-flipping
    a field's walls would collide with DEFAULT byte for byte, the walls take
    the danger form (spec §9.2) — swiss `╲ ╱`, darkside `Ø Ø`, blueprint
    `━ ━`, corgi, ledger. There the opening cell IS the rejection, said in the
    language's loudest form, which is the opposite of a reader mistaking it
    for one. Everything else counts."""
    k = LG.kit(lang)
    meanings = (set("".join(k.LEVELS.values())) | {k.REQUIRED}
                | set("".join(k.DANGER_FORM))) - set(" ⠀")
    danger = set(k.DANGER_FORM)
    out = []
    for comp in OPENING_CONTROLS:
        for part in LG.COMPONENT_PARTS[comp]:
            table = k.PART_GLYPHS[k.part_key(comp, part)]
            for st in LG.component_states(comp):
                glyph = k.part_glyph(part, st, comp)
                if len(glyph) < 2 or glyph[0] not in meanings:
                    continue
                if (LG.control_of(st) == LG.INVALID and LG.INVALID in table
                        and glyph[0] in danger):
                    continue
                out.append((f"{comp}.{part}", st, glyph, glyph[0]))
    return out


@pytest.mark.parametrize("lang", LANGS)
def test_no_control_opens_with_a_mark_that_means_something(lang):
    """THE BATCH RULE'S FIRST NAMED SEAT, and the finding the census was built
    around.

    `collision_census.py`'s own docstring states it: "a language has a small
    alphabet, spends one glyph on severity or obligation, and then spends the
    same glyph on a control's chrome — so a reader who has learned 'this mark
    means error' meets it OPENING A BUTTON." That is `instrument_S2`
    (`⠇   Cancel   ⠸`, the error rung on the safe button), `industrial_S2`
    (`▐` the obligation and the field's wall on one row), `swiss_S3`
    (`· ╲Delete all╱`, the LOWEST severity rung opening the most dangerous
    control on the screen) and `solari_S2` (`▁` nineteen ways).

    THE OPENER AND NOT EVERY CELL, deliberately. A mark that means something
    may stand in a control — a closer, a paper, a knob, a mark inside a box —
    because a reader meets those AFTER the control has already announced
    itself. The first cell is the announcement, which is why the round's
    phrasing is "el peldaño de error ABRE el botón seguro" and not "aparece
    en".

    IT IS A MEASUREMENT, NOT A PASS. Four languages still fail it, counted
    per language so the roster can only move when somebody edits it, and one
    of the four (naught) carries a written argument for an exemption that has
    NOT been granted. Seven are clean and four of those seven were not before
    this batch."""
    assert len(meaning_marks_at_an_opener(lang)) \
        == MEANING_AT_AN_OPENER[lang], (lang, meaning_marks_at_an_opener(lang))


def test_the_opener_law_goes_red_on_the_two_declarations_inc48_and_inc46_moved(
        monkeypatch):
    """TEETH, and they have to name the control and the mark.

    Arm one restores `Industrial.REQUIRED` to `▐`, the opening half of the
    plate every button and every field is set in — the declaration inc48
    moved, and `industrial_S2`'s finding verbatim.

    Arm two restores swiss's pre-inc46 button ladder, `· • ●`, whose two lower
    rungs are `LEVELS["info"]` and `REQUIRED` — the declaration inc46 moved,
    and `swiss_S3`'s and `swiss_S4`'s findings at once. Each arm must move its
    language off zero AND leave the other ten where they were, which is what
    proves the eleven are eleven declarations rather than one shared object."""
    for lang in LANGS:
        assert (len(meaning_marks_at_an_opener(lang))
                == MEANING_AT_AN_OPENER[lang]), lang

    monkeypatch.setattr(LG.Industrial, "REQUIRED", "▐")
    hits = meaning_marks_at_an_opener("industrial")
    assert hits, "industrial"
    assert {h[0] for h in hits} == {"button.main", "textfield.main"}, hits
    assert {h[3] for h in hits} == {"▐"}, hits
    assert all(len(meaning_marks_at_an_opener(o)) == MEANING_AT_AN_OPENER[o]
               for o in LANGS if o != "industrial")
    monkeypatch.undo()

    monkeypatch.setitem(LG.Swiss.PART_GLYPHS, "button.main",
                        {LG.DEFAULT: "·   ", LG.FOCUSED: "•   ",
                         LG.ACTIVE: "●   ", LG.DISABLED: "    "})
    hits = meaning_marks_at_an_opener("swiss")
    assert {h[0] for h in hits} == {"button.main"}, hits
    assert {h[3] for h in hits} == {"·", "•"}, hits
    assert all(len(meaning_marks_at_an_opener(o)) == MEANING_AT_AN_OPENER[o]
               for o in LANGS if o != "swiss")
    monkeypatch.undo()

    for lang in LANGS:
        assert (len(meaning_marks_at_an_opener(lang))
                == MEANING_AT_AN_OPENER[lang]), lang
