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

import re

import pytest

from taskboard import language as LG

LANGS = tuple(LG.KITS)
#: the five the PROTOTYPE round rendered; the others inherit the seat, and the
#: laws below are asked of ALL of them either way
PROTOTYPED = ("corgi", "blueprint", "prism", "naught", "ledger")

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
    assert set(LG.MODAL_BORDER_REFUSED) == {"corgi", "blueprint", "naught",
                                            "ledger"}
    assert all(len(v) > 40 for v in LG.MODAL_BORDER_REFUSED.values())


def test_prism_is_the_one_language_licensed_to_draw_the_box():
    """Operator ruling 5. Prism's commitment is the only one of the eleven
    that names this component as its exception — "depth by one grey step,
    never borders: borders are RESERVED for modals" — so it is absent from
    the registry and it draws the lid."""
    assert "prism" not in LG.MODAL_BORDER_REFUSED
    k = LG.kit("prism")
    assert has_lid(k.overlay(dialog(k), DIALOG_W, DIALOG_H, UNDER))


@pytest.mark.parametrize("lang", sorted({"corgi", "blueprint", "naught",
                                         "ledger"}))
def test_a_refusing_language_draws_no_lid(lang):
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
