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

import colorsys
import functools
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


def test_corgis_confirm_keeps_the_mode_strip_and_nothing_else():
    """"The mode takes over the screen." A dialog floating over a board is
    two modes at once, so the backdrop is not dimmed — it is GONE. The
    argument is accepted and everything but its first row is dropped, and that
    dropping IS the refusal.

    THE FIRST ROW IS THE ONE EXCEPTION, AND inc65 MADE IT. "The board is gone"
    is doctrine about the BOARD; row 1 of this page is `[1]BOARD [2]FORM
    [3]CFG [4]LOG`, the strip that says which mode the operator is in. A mode
    that erases the mode indicator is the one thing a MODE may not do, and
    `corgi_S4` was the single frame of the sixty-six that could not answer
    "which mode is this?" — inc40's own criterion, which this kit had an
    exemption from on the strength of a sentence about the board. Its `.svg`
    held seven text runs in total.

    THE REFUSAL'S CITATION LIVES HERE NOW, word for word, because the head law
    no longer carries it: a commitment may not outlive the sentence that earns
    it."""
    k = LG.kit("corgi")
    assert "corgi" in MODAL_KEEPS_ONLY_THE_HEAD
    assert "the board is gone" in LG.MODAL_BORDER_REFUSED["corgi"]
    out = [plain(r) for r in k.overlay(dialog(k), DIALOG_W, DIALOG_H, UNDER)]
    # the head survives, at its own index
    assert out[0].rstrip() == plain(UNDER[0]).rstrip(), out[0]
    # and nothing else of the page does -- the board is still gone
    rest = [plain(r) for r in UNDER[1:]]
    assert not any(r.strip() and r.strip() in o for r in rest for o in out), out
    # and the question is CENTRED on the panel: a mode is not a dialog that
    # lost its box, it is the whole glass, so the question sits in the middle
    # of it rather than in the corner a window would start from.
    assert any("Delete 3 tasks?" in r for r in out)
    assert out[1].strip() == "" and out[2].strip() == ""


def test_ledgers_confirm_is_posted_on_the_page_that_stays_legible():
    """"Nothing is deleted, everything is balanced", and a ledger has no
    surface IN FRONT OF the page. The question is posted at the foot, under a
    rule, and the entries above it are kept AT FULL STRENGTH — the exact
    opposite of every other answer here. Dimming them would be the language
    claiming those postings are less true while a question is open.

    AND THE POSTING IS RULED OFF AT ITS FOOT (inc72, C2). It opened on a rule
    and closed on nothing, so the lower limit of the question was the EDGE OF
    THE TERMINAL and the irreversible answer sat on the last row a reader can
    see. The two clauses added here are the two halves of that: the block's
    FIRST and LAST rows are the same rule, and the destructive answer is not
    on the sheet's last row."""
    k = LG.kit("ledger")
    out = k.overlay(dialog(k), DIALOG_W, DIALOG_H, UNDER)
    assert out[0] == UNDER[0], out[0]
    rows = [plain(r) for r in out]
    # the block opens and closes on the SAME rule, at full measure
    rule = plain(k.rule_line(DIALOG_W))
    assert rows[-1] == rule, rows[-1]
    head = [i for i, r in enumerate(rows) if r == rule]
    assert len(head) == 2 and head[1] == len(rows) - 1, head
    assert "Delete 3 tasks?" in rows[head[0] + 1], rows[head[0] + 1]
    # and the answers -- the destructive one included -- are INSIDE the block
    ans = [i for i, r in enumerate(rows) if "Delete" in r and "?" not in r]
    assert ans and max(ans) < len(rows) - 1, (ans, rows[-3:])


def test_naughts_separation_is_charge_and_not_a_frame():
    """Operator ruling 4. The page keeps every dot it had and loses its
    CHARGE; the question is the only region left lit, bounded by the lattice.
    No box, no scrim, no mark laid in front of anything.

    inc72: AND THE BOUND IS THE GROUND, NOT THE DANGER FORM. The two rules
    were the LIT dot — `DANGER_FORM`, `LEVELS["error"]` and `LEVELS["warn"]`'s
    first cell — two hundred cells of it on the one screen where a reader has
    to find the mark that means "this destroys data". They are the UNLIT
    lattice now, which `THE_GROUND_IS_NOT_A_MARK` rules a ground and not a
    mark, drawn at the band's own charge. The separation is still CHARGE and
    is now literally the lattice: the last clause counts the lit `DANGER_FORM`
    cells inside the band and there are exactly the two the answer spends."""
    from taskboard import naught as NA
    k = LG.kit("naught")
    out = k.overlay(dialog(k), DIALOG_W, DIALOG_H, UNDER)
    bounds = [r for r in out if plain(r) and plain(r).strip(NA.OFF) == ""
              and len(plain(r)) == DIALOG_W]
    assert len(bounds) == 2, [plain(r) for r in out]
    assert all(k.c["ink"] in r for r in bounds)
    backdrop = [r for r in out if "row 0 of the board" in plain(r)]
    assert backdrop and k.c["dim"] in backdrop[0]
    # THE COUNT THAT IS THE POINT: the band adds no LIT dot of its own. It
    # used to add two hundred -- two rules of `NA.ON`, which is the
    # `DANGER_FORM` and two severity rungs -- on the one screen where a
    # reader has to find the cells that mean "this destroys data". Whatever
    # the question itself spends is all there is inside it now.
    lo, hi = out.index(bounds[0]), out.index(bounds[1])
    band = "".join(plain(r) for r in out[lo:hi + 1])
    asked = "".join(plain(r) for r in dialog(k))
    assert band.count(NA.ON) == asked.count(NA.ON), (band.count(NA.ON),
                                                     asked.count(NA.ON))
    assert all(NA.ON not in plain(r) for r in bounds)


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
#:
#: CORGI JOINED IN inc58, for the same kind of reason and by the same
#: derivation. Its field walls were a bank at a height (`▁▁ … ▁▁`,
#: `▔▔ … ▔▔`), and a bank has no hand; the walls are now the engraved key's
#: two SHOULDERS (`▛▛ … ▜▜`), which are mirror images by construction. The
#: language always drew a key that way — `button.main`'s own comment says
#: "both shoulders are two cells wide and the label sits in the milled
#: channel between them" — and only now spells the two shoulders with two
#: marks. corgi's INVALID walls stay unhanded (`░░ … ░░`, inc52's ghost), so
#: the law passes on it rather than being widened to a language it cannot
#: reach.
HANDED_FIELDS = ("corgi", "instrument", "swiss", "industrial", "nord",
                 "ledger", "blueprint")


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
#: the ONE language whose refusal says the BOARD does not survive a confirm.
#: Named rather than derived, and its citation is asserted word for word in
#: `test_corgis_confirm_keeps_the_mode_strip_and_nothing_else` — a commitment
#: may not outlive the sentence that earns it, and "the board is gone" is the
#: phrase that earns this one.
#:
#: inc65 (C8): IT IS NO LONGER AN EXEMPTION FROM THE HEAD LAW. "The board is
#: gone" is doctrine about the board; a mode strip is not the board, and
#: `corgi_S4` was the one frame of the sixty-six that could not answer "which
#: mode is this?" — which is the criterion inc40 wrote the head law for. All
#: eleven keep row 1 now, and this roster says which of them keeps ONLY row 1.
MODAL_KEEPS_ONLY_THE_HEAD = ("corgi",)


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
    off. Measured on the shipped frames, against the shipped page.

    A ROW THE MODAL DRAWS BLANK OVER A BLANK PAGE ROW IS STILL THE MODAL'S
    (inc66). `modal_band` reads the rows that DIFFER, which is the only thing
    a shipped frame can be asked; a band with air in it, laid over a page that
    also has air there, comes back with a HOLE in the run. That is exactly
    what happened the moment `swiss_S4` gained its closing rule and the
    block's two air rows landed on the page's own air: the composition was
    right and the proxy was wrong. So the run is measured END TO END, and
    every row inside it that did not change must be blank on BOTH sides. The
    half that carries the meaning of "overlay" -- every row OUTSIDE the run is
    the page's own row at the same index -- is untouched and is asserted
    below."""
    band = modal_band(lang)
    assert band, lang
    s1 = page_rows(lang)
    s4 = (FRAMES / f"{lang}_S4.txt").read_text(
        encoding="utf-8").rstrip("\n").split("\n")
    for i in range(band[0], band[-1] + 1):
        if i in band:
            continue
        assert not s1[i].strip() and not s4[i].strip(), (lang, i, s1[i], s4[i])


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

    AND SINCE inc65 IT IS ASKED OF ALL ELEVEN. corgi held an exemption from
    it, earned by its refusal — "a dialog floating over a board is two modes
    at once ... so a confirm is a MODE and the board is gone". That sentence
    is about the BOARD. The mode strip is not the board; it is the row that
    says which mode the operator is in, and a confirm that erases it is a mode
    that has erased its own indicator. `corgi_S4` was the one frame of the
    sixty-six that could not answer "which mode is this?", which is the
    question this law exists to keep answerable. The board is still gone — see
    `test_corgis_confirm_keeps_the_mode_strip_and_nothing_else`, which is
    where the refusal's citation now lives."""
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
        assert row0.rstrip() == u[0].rstrip(), other


# ---------------------------------------------------------------------------
# inc50 (rework-4) - the band SHRINKS to its content; it does not slide
# ---------------------------------------------------------------------------
#: A GATE HEADER, as the board prints one: the gate's name, its count, and the
#: column captions. Matched rather than compared to a literal so the law reads
#: the SHAPE of a header and not this fixture's three gates.
_GATE_HEAD = re.compile(r"GATE [A-Z]+ \d\d\s")


def solari_s4_rows(k):
    """The words `screens.s4` hands `overlay`, rebuilt from the shipped frame.

    `screens.s4` composes `[title, "", body1, body2, "", answers]` — six rows,
    two of them the page's air between a title, a body and its answers — and
    hands the same six to all eleven kits. The teeth below have to run THAT
    block and not a three-row stand-in, because the whole finding is about how
    many rows the block occupies; a stand-in whose length was chosen here
    would be the test deciding its own outcome.

    THE FOUR ROWS ARE FOUND, NOT COUNTED (inc55). This used to slice `[4:8]`,
    which was the band's seat while the band stood at the schedule's head;
    ruling F moved it, and a hard-coded slice would have gone on returning
    four rows of BOARD without failing. The band is read off the frame with
    `modal_band` and the words are what lies between its bar and its seam."""
    band = modal_band("solari")
    said = [r.rstrip() for r in (FRAMES / "solari_S4.txt").read_text(
        encoding="utf-8").rstrip("\n").split("\n")[band[0] + 1: band[-1]]]
    assert len(said) == 4, said
    return ([LG.mark(said[0]), ""] + [LG.mark(s) for s in said[1:3]]
            + ["", LG.mark(said[3])])


def test_solaris_band_is_its_content_and_stands_at_a_gates_head():
    """THE BAND SHRINKS TO ITS CONTENT, AND IT STANDS AT A GATE'S HEAD.

    CLAUSE 2 CHANGED ENDS IN inc55 (ruling F), and that is written here
    rather than left in a commit message, because a clause that quietly got
    weaker is how a law becomes decoration:

      inc50 clause 2   the row immediately BELOW the band is a gate header
      inc55 clause 2   the row the band STARTS on is a gate header

    Both are the same sentence read from opposite ends — *a band takes a
    gate's head, not the middle of one*. inc50 could only assert the foot,
    because the band stood at the schedule's head and the head there is the
    plate's business, not a gate's. Ruling F moves the band off the gate the
    confirm NAMES, so the head becomes the assertable end and the foot now
    lands INSIDE the gate the band moved onto. **That cost is real, it is
    named in `inc55.md` §6 and at `Solari.overlay_instead`, and the row under
    the band is a departure's orphan seam again.** Clauses 1 and 3 are
    inc50's, word for word.

    inc40 moved the band off the station's plate and the round measured what
    that cost: *"la banda no encogió, se deslizó tres filas"*. It gave back
    the mode strip, the masthead and the head seam and it took two more rows
    of board — `GATE DOING 04` and `FIX LOGIN REDIRECT` — so `solari_S4` came
    back with the SEAM of a departure the band had taken as its first row and
    five task rows under no gate header at all. A schedule whose first row is
    the underline of a flight that is not on it is not "the rows still
    legible under it".

    THREE CLAUSES, ALL MEASURED ON THE SHIPPED FRAME AGAINST THE SHIPPED PAGE:

    1. THE BAND IS ITS CONTENT. Its length is `1 + the rows that say
       something + 1` — the reverse-video bar, the words, the closing seam —
       and between the first word and the seam there is no empty row.
       `MODAL_BORDER_REFUSED["solari"]` calls it a BAND, and a band with air
       in it is two bands.
    2. THE BAND STANDS AT A GATE'S HEAD (inc55). The row the band starts on
       is a gate header on the PAGE, at its own index — not a seam and not a
       task row. Ruling F is what makes this the assertable end; see the top
       of this docstring for the clause it replaces and what that cost.
    3. IT IS STILL AN OVERLAY. Every row outside the band is the page's row at
       the same index — inc40's second half, re-asserted here because a
       "shrink" implemented by inserting rows would satisfy clause 2 and push
       the whole board down."""
    s1, s4 = page_rows("solari"), (FRAMES / "solari_S4.txt").read_text(
        encoding="utf-8").rstrip("\n").split("\n")
    band = modal_band("solari")
    said = [i for i in band if s4[i].strip()]

    # 1 — the bar, the words, the seam, and no air between them
    assert band == list(range(band[0], band[-1] + 1)), band
    assert len(band) == len(said) + 1, (band, said)      # +1: the blank bar
    assert said == list(range(said[0], said[-1] + 1)), said
    assert set(s4[said[-1]].strip()) == {"▁"}, s4[said[-1]]   # the seam closes
    assert "Delete 3 tasks?" in s4[said[0]], s4[said[0]]

    # 2 — the band starts on the row BELOW a gate header of the page, at its
    #     own index, and no gate header of any gate is inside it (inc65,
    #     F amended)
    assert _GATE_HEAD.search(s1[band[0] - 1]), (band[0], s1[band[0] - 1])
    assert not _GATE_HEAD.search(s1[band[0]]), (band[0], s1[band[0]])
    assert not any(_GATE_HEAD.search(s1[i]) for i in band),         [(i, s1[i]) for i in band if _GATE_HEAD.search(s1[i])]

    # 3 — still an overlay: nothing outside the band moved
    assert all(s4[i].rstrip() == s1[i].rstrip()
               for i in range(len(s1)) if i not in band)


def test_an_unshrunk_band_leaves_the_schedule_opening_on_an_orphan_seam(
        monkeypatch):
    """TEETH. The pre-inc50 body restored exactly — `[bar] + list(rows) +
    [seam]`, the air kept — and handed the block `screens.s4` really hands it.

    It has to name what goes wrong and not merely that something does: with
    the two empty rows back the band is EIGHT rows, it swallows `GATE DOING
    04` and `FIX LOGIN REDIRECT` as well, and the first row of the surviving
    board is that departure's own SEAM — a rule under a flight that is no
    longer on the board. That is the round's finding, reproduced from the
    declaration rather than described.

    The band's HEAD is asserted unmoved by the same patch, which is what says
    this is a length finding and not a re-run of inc40's anchor finding."""
    k = LG.kit("solari")
    s1 = page_rows("solari")
    under, w, h = page_markup("solari"), len(s1[0]), len(s1)
    rows = solari_s4_rows(k)

    out = [plain(r) for r in k.overlay(rows, w, h, under)]
    band = [i for i, (a, b) in enumerate(zip(s1, out))
            if a.rstrip() != b.rstrip()]
    assert len(band) == 6 and band[0] == 3, band
    assert _GATE_HEAD.search(out[band[-1] + 1]), out[band[-1] + 1]

    def unshrunk(self, rows, w, h, under, about=None):
        c = self.c
        bar = (f"[{self.t.get('ground', '#000000')} on {c['accent']}]"
               f"{LG.mark(' ' * w)}[/]")
        block = [bar] + list(rows) + [self.seam(w)]
        y = self.schedule_head(under)
        return [block[i - y] if y <= i < y + len(block)
                else self.recede(under[i] if i < len(under) else "")
                for i in range(h)]

    monkeypatch.setattr(LG.Solari, "overlay_instead", unshrunk)
    out = [plain(r) for r in k.overlay(rows, w, h, under)]
    band = [i for i, (a, b) in enumerate(zip(s1, out))
            if a.rstrip() != b.rstrip()]
    assert len(band) == 8 and band[0] == 3, band          # the head is the same
    eaten = [s1[i] for i in band]
    assert any("GATE DOING 04" in r for r in eaten), eaten
    assert any("FIX LOGIN REDIRECT" in r for r in eaten), eaten
    orphan = out[band[-1] + 1]
    assert not _GATE_HEAD.search(orphan), orphan
    assert set(orphan.strip()) == {"▁"}, orphan           # a seam, not a gate


# ---------------------------------------------------------------------------
# inc55 (rework-5b) - a confirm never covers the gate it names (ruling F)
# ---------------------------------------------------------------------------
#: the same header shape as `_GATE_HEAD`, with the gate's NAME captured. Two
#: patterns rather than one so `_GATE_HEAD`'s call sites keep reading as a
#: yes/no question about a row.
_GATE_NAMED = re.compile(r"GATE ([A-Z]+) \d\d\s")


def gate_blocks(rows):
    """`{name: [indices]}` — every gate on a page and the whole block it owns,
    from its header down to the row before the next gate's header.

    A BLOCK AND NOT A HEADER, because ruling F's law is about the gate's
    DEPARTURES as well: a confirm that left `GATE BACKLOG 05` on the frame and
    took the two flights under it would still have hidden what it is about."""
    heads = [(i, m.group(1)) for i, r in enumerate(rows)
             if (m := _GATE_NAMED.search(r))]
    out = {}
    for j, (i, name) in enumerate(heads):
        end = heads[j + 1][0] if j + 1 < len(heads) else len(rows)
        out[name] = list(range(i, end))
    return out


def test_a_solari_confirm_never_covers_the_gate_it_names():
    """RULING F (orchestrator, 2026-09-06, on the operator's delegation):
    *a confirm never covers the gate it names.*

    `MODAL_BODY` says "3 tasks will be removed from BACKLOG" and every anchor
    this band has had — index 0 (pre-inc40), the schedule's head (inc40),
    the schedule's head shrunk (inc50) — put the band on `GATE BACKLOG 05`
    and its two departures. `inc50.md` §4 named the three ways out and called
    them design decisions; this is the first of them, taken.

    THE NAME IS INTERSECTED, NOT PARSED. This file does not import the
    prototype fixture, and reading "removed from BACKLOG" with a regular
    expression would make the law a reader of one sentence's English. The
    gates the PAGE declares are a set; the words the BAND says are a string;
    the gate the confirm names is the one member of the first that appears in
    the second, and there is asserted to be exactly one. A fixture that
    renamed its columns would move both halves together.

    TWO READINGS, and the second is what stops the first being a lucky
    fixture. The shipped frame is asked whether the named gate's block
    survived; then the MECHANISM is asked the same question about EVERY gate
    on the page in turn, so a placement that happened to miss BACKLOG while
    eating whichever gate it was pointed at goes red."""
    s1 = page_rows("solari")
    s4 = (FRAMES / "solari_S4.txt").read_text(
        encoding="utf-8").rstrip("\n").split("\n")
    band = modal_band("solari")
    blocks = gate_blocks(s1)
    assert len(blocks) >= 2, blocks              # a one-gate page is the foot case

    words = " ".join(s4[i] for i in band)
    named = [g for g in blocks if g in words]
    assert len(named) == 1, (named, words)       # the gate the confirm is about
    for i in blocks[named[0]]:
        assert s4[i].rstrip() == s1[i].rstrip(), (named[0], i, s4[i], s1[i])
    assert not (set(band) & set(blocks[named[0]])), (band, blocks[named[0]])

    # and the same question of the mechanism, once per gate on the page
    k = LG.kit("solari")
    under, w, h = page_markup("solari"), len(s1[0]), len(s1)
    rows = solari_s4_rows(k)
    for gate, block in blocks.items():
        out = [plain(r) for r in k.overlay(rows, w, h, under, about=gate)]
        for i in block:
            assert out[i].rstrip() == s1[i].rstrip(), (gate, i, out[i])


def test_the_bands_old_anchor_ate_the_gate_the_confirm_names(monkeypatch):
    """TEETH, and they are the round's own evidence rather than a description
    of it: `band_head` put back to `schedule_head` IS the inc50 body, and
    under it the band covers `GATE BACKLOG 05`, `AUDIT THE THEME TOKENS` and
    `DROP THE LEGACY SHIM` — the gate the confirm names and both of its
    departures.

    THE LAW MUST NAME THE GATE AND THE FLIGHTS, not merely fail. A teeth arm
    that asserted "something differs" would stay green if the band moved one
    row for an unrelated reason.

    THE THIRD ARM IS THE DEFAULT. `about=None` is documented at
    `Kit.overlay` as "a caller that did not say leaves every language exactly
    where it was", and every other test in this file relies on it — so it is
    asserted here rather than trusted: with no `about`, the band is inc50's,
    at the schedule's head, eating BACKLOG."""
    k = LG.kit("solari")
    s1 = page_rows("solari")
    under, w, h = page_markup("solari"), len(s1[0]), len(s1)
    rows = solari_s4_rows(k)
    blocks = gate_blocks(s1)

    def band_of(**kw):
        out = [plain(r) for r in k.overlay(rows, w, h, under, **kw)]
        return [i for i, (a, b) in enumerate(zip(s1, out))
                if a.rstrip() != b.rstrip()], out

    band, _ = band_of(about="BACKLOG")
    assert not (set(band) & set(blocks["BACKLOG"])), band

    monkeypatch.setattr(LG.Solari, "band_head",
                        lambda self, under, depth, about=None:
                        self.schedule_head(under))
    band, _ = band_of(about="BACKLOG")
    eaten = [s1[i] for i in band]
    assert any("GATE BACKLOG 05" in r for r in eaten), eaten
    assert any("AUDIT THE THEME TOKENS" in r for r in eaten), eaten
    assert any("DROP THE LEGACY SHIM" in r for r in eaten), eaten

    monkeypatch.undo()
    assert band_of()[0] == band, "about=None is inc50's anchor"


def test_a_page_whose_every_gate_is_named_puts_the_band_at_the_foot():
    """THE FALLBACK, WHICH NO FRAME IN THIS REPO REACHES.

    Ruling F's second sentence: *if every gate is named or the page has one
    gate, the band goes to the foot of the schedule (above the plate's
    closing seam, if any)*. The sweep's confirm names one of four gates, so
    this branch is exercised HERE and nowhere else — which is the reason it
    is asserted at all rather than left to be discovered dead.

    THE PAGE IS SYNTHETIC AND SAYS SO. It is built to the shape
    `schedule_head` and `gate_of` read — a masthead, a full-measure seam, one
    gate, its departures, and a closing seam — because the claim is about a
    page with ONE gate and the shipped page has four."""
    k = LG.kit("solari")
    seam = "▁" * 40
    page = ["THE PLATE", seam,
            "   GATE BACKLOG 05   STATUS",
            "    21  AUDIT THE THEME TOKENS",
            "    30  DROP THE LEGACY SHIM",
            "", "", "", "", "", "", "", seam]
    under = [LG.mark(r) for r in page]
    assert k.schedule_head(under) == 2
    assert k.gate_of(under[2]) == "BACKLOG"

    # named: the band cannot stand at the only gate, so it takes the foot,
    # above the page's closing seam
    assert k.band_head(under, 6, "BACKLOG") == len(page) - 1 - 6
    # not named: the first gate the confirm does not name is the only gate,
    # and the band takes the row BELOW its header (inc65, F amended)
    assert k.band_head(under, 6, "DOING") == 3
    # and a caller that says nothing is still inc40's answer
    assert k.band_head(under, 6, None) == k.schedule_head(under)

    out = [plain(r) for r in k.overlay(
        [LG.mark("Delete 3 tasks?"), "", LG.mark("body"), "",
         LG.mark("Delete   Cancel")], 40, len(page), under, about="BACKLOG")]
    assert out[-1].rstrip() == page[-1].rstrip()          # the closing seam
    assert all(out[i].rstrip() == page[i].rstrip() for i in range(5))
    assert any("Delete 3 tasks?" in r for r in out[-7:])


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
#:
#: AND IT IS 16 SINCE inc56, WITH `blueprint_S2` — the frame round decision
#: (G) said did not exist. The first-fixation law fires on the `alert` mood
#: alone and no sheet had ever set one, so the corpus's ONE knockout mechanism
#: was asserted in a test and in no image. `screens.s2` now hands the kit the
#: mood the fixture's own tasks imply, and the title block reverses.
GROUNDED_FRAMES = ("industrial_S1", "darkside_S1", "prism_S1", "ledger_S1",
                   "solari_S1", "solari_S2", "blueprint_S2", "solari_S3",
                   "prism_S4", "ledger_S4", "solari_S4", "blueprint_S4",
                   "solari_S5", "solari_S6", "industrial_S6", "darkside_S6")


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
    frame leaving it, and both have to be looked at.

    AND IT IS 16 SINCE inc56, and this one arrived because a fact was handed
    over rather than because a declaration changed: `blueprint_S2` joined when
    `screens.s2` started telling its kit the board's mood. Nothing in
    `Blueprint` moved — `_state_cell` has reversed on `alert` since inc17 —
    and the roster is where "the mechanism is now in a picture" becomes a
    number."""
    got = tuple(f"{lang}_{sc}" for sc in SCREENS for lang in LANGS
                if declared_grounds(lang, sc))
    assert sorted(got) == sorted(GROUNDED_FRAMES), got
    assert len(got) == 16


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
    knockout" is shown to be an unspent law and not a dead one.

    WHAT inc54 CHANGED AND WHAT IT DID NOT. The ruling stands and the cell
    still reverses; what moved is that the reversed thing is a BUTTON. The row
    was built with `knockout_cell(" DELETE ")` \u2014 a cell, not a control \u2014 so
    the sheet's one irreversible answer carried no danger form and no focused
    walls in either tier. The seat is asserted below and the `.svg`'s reversed
    run is now the whole button rather than the bare word."""
    k = LG.kit("blueprint")
    seat = k.button("DELETE", 8, LG.FOCUSED, danger=True, knockout=True)
    assert seat == f"[{k.t['ground']} on {k.c['ink']}]\u255e \u2501DELETE\u2501 \u2561[/]", seat
    assert k.knockout_cell(" DELETE ") == \
        f"[{k.t['ground']} on {k.c['ink']}] DELETE [/]"
    assert declared_grounds("blueprint", "S4") == {k.c["ink"]}
    svg = (FRAMES / "blueprint_S4.svg").read_text(encoding="utf-8")
    pair = re.search(r'<rect[^>]*fill="%s"/>\s*<text[^>]*fill="([^"]+)"[^>]*>'
                     r'([^<]*)</text>' % re.escape(k.c["ink"]), svg)
    assert pair, svg[:200]
    assert pair.group(1) == k.t["ground"]
    assert pair.group(2).replace("\u00a0", " ") == "\u255e \u2501DELETE\u2501 \u2561"

    # the title block's own cell: unspent, not absent
    assert k.mood != "alert"
    assert k._state_cell() == ("├ CLEAR ┤", False)
    calm = LG.kit("blueprint")
    calm.mood = "alert"
    assert calm._state_cell()[1] is True, "the first-fixation law is dead"


# ---------------------------------------------------------------------------
# inc54 (rework-5a) — the destructive default answer is a BUTTON
# ---------------------------------------------------------------------------
#: the label and minimum width `screens.py` gives the destructive default
#: answer, per language. Two entries and not eleven: `answers()` composes it
#: once for ten languages and `s4_blueprint` composes it once for the eleventh,
#: which is the whole structure this law is about — the eleventh was the one
#: that was not a button.
S4_ANSWER = {"blueprint": ("DELETE", 8)}
S4_ANSWER_DEFAULT = ("Delete", 10)


@pytest.mark.parametrize("lang", LANGS)
def test_the_destructive_default_answer_is_a_focused_danger_button(lang):
    """THE LAW, over all eleven: in every language's S4 the irreversible
    default answer carries THIS LANGUAGE'S DANGER FORM, THIS LANGUAGE'S
    FOCUSED WALLS, and — where the language's registry spends a knockout —
    the KNOCKOUT TIER over the whole seat, in the `.txt` and in the `.svg`.

    IT IS READ OFF THE SHIPPED FRAME AND NOT OFF THE COMPOSITION, which is
    what keeps it from asserting that `screens.py` equals itself: the pattern
    is built from the KIT's declarations — `button.main[FOCUSED]` split in
    half and `DANGER_FORM` around the word — and searched for in
    `<lang>_S4.txt`. A language that stopped drawing its focused walls there,
    or drew a bare word, goes red.

    `PROTOTYPE-inheritors-2.md` §5 C1 IS WHY: `blueprint_S4`'s DELETE was
    built with `knockout_cell(" DELETE ")`, a cell rather than a control, so
    the one irreversible answer on that sheet had no danger form and no focus
    ring in EITHER tier while ten other languages' S4 carried both. Operator
    ruling 10 moved the knockout to the default answer; it did not say the
    default answer stops being a button."""
    k = LG.kit(lang)
    label, w = S4_ANSWER.get(lang, S4_ANSWER_DEFAULT)
    lo, hi = k.DANGER_FORM
    walls = k.part_glyph("main", LG.FOCUSED, "button")
    half = len(walls) // 2
    word = f"{lo}{label}{hi}"
    seat = walls[:half] + word.center(max(w, len(word))) + walls[half:]

    txt = (FRAMES / f"{lang}_S4.txt").read_text(encoding="utf-8")
    assert seat in txt, (lang, seat, [r for r in txt.splitlines()
                                      if label in r])
    assert plain(k.button(label, w, LG.FOCUSED, danger=True,
                          knockout=k.knockout)) == seat, lang

    if not k.knockout:
        return
    # the tier, in the DECLARATION and in the SVG. inc41's law already asserts
    # declared == painted over all 66; this asserts WHICH RUN carries it.
    assert k.c["ink"] in declared_grounds(lang, "S4"), lang
    svg = (FRAMES / f"{lang}_S4.svg").read_text(encoding="utf-8")
    pair = re.search(r'<rect[^>]*fill="%s"/>\s*<text[^>]*fill="([^"]+)"[^>]*>'
                     r'([^<]*)</text>' % re.escape(k.c["ink"]), svg)
    assert pair, lang
    assert pair.group(1) == k.t["ground"], lang
    assert pair.group(2).replace(" ", " ") == seat, (lang, pair.group(2))


def test_a_knockout_a_language_refuses_falls_back_to_the_plain_button():
    """TEN OF THE ELEVEN HAVE NO `knockout` TOKEN, and a caller composing one
    S4 for all of them may not have to know which.

    So the request is IGNORED rather than raised on, and the fallback is the
    button they would have got anyway — same walls, same tones, same danger
    form, byte for byte. Asserted as an EQUALITY against the un-knocked call
    rather than as "no ` on ` appears", because the second would also pass if
    the knocked call returned something else entirely.

    AND THE ONE THAT DOES SPEND IT MUST DIFFER, which is the half that keeps
    this from being vacuous: an implementation that ignored the keyword
    everywhere would satisfy the ten and fail here."""
    spent = [lang for lang in LANGS if LG.kit(lang).knockout]
    assert spent == ["blueprint"], spent
    for lang in LANGS:
        k = LG.kit(lang)
        plainer = k.button("Delete", 10, LG.FOCUSED, danger=True)
        knocked = k.button("Delete", 10, LG.FOCUSED, danger=True,
                           knockout=True)
        if k.knockout:
            assert knocked != plainer, lang
            assert knocked.count(" on ") == 1, knocked
        else:
            assert knocked == plainer, lang


def test_exactly_one_knockout_per_view_still_holds_on_blueprints_confirm():
    """*Exactly ONE element per view reverses*, counted on the COMPOSED ROWS
    of the frame the knockout moved to — the arithmetic `s4_blueprint`'s
    docstring claims.

    THE COUNT IS OVER ` on ` TAGS and that is why `button` emits ONE span
    rather than three: a knockout that gave the walls and the word a tag each
    would still be one element to a reader and three to this test, and the
    test is the only thing that can tell. The title block's state cell is
    UNSPENT here (the sheet's mood is calm), which is what makes the move
    legal — asserted in the ruling-10 test above and re-counted here from the
    other end."""
    rows = sheet_rows("blueprint", "S4")
    assert sum(r.count(" on ") for r in rows) == 1, \
        [r for r in rows if " on " in r]
    assert any("╞ ━DELETE━ ╡" in plain(r) for r in rows), "the seat is gone"


# ---------------------------------------------------------------------------
# inc56 (rework-5b) - the corpus's one knockout is finally in a picture (G)
# ---------------------------------------------------------------------------
def test_blueprints_first_fixation_is_painted_on_the_form():
    """RULING G (orchestrator, 2026-09-06, on the operator's delegation): *the
    S2 fixture carries one alert-mood item for all eleven.*

    `PROTOTYPE-inheritors-2.md` §6 G: blueprint's first-fixation law is
    *"ejercitada en un test y no está en ninguna imagen"*. `_state_cell`
    reverses on the `alert` mood alone; `Kit.mood` is set by the app from the
    real task list; and no screen builder in `screens.py` had ever set it, so
    all 66 frames were composed by kits carrying the constructor's default.
    The fixture has had an overdue task since it was written. `screens.s2`
    now hands the fact over and the title block reverses.

    THIS EXTENDS inc41's TIER COMPARISON THE WAY inc54 DID. inc41 asserts
    *declared == painted* over 66 frames as SETS; inc54 asserted WHICH run
    carries the ground on S4 and what is inside it. This asserts the same of
    the ALERT run on S2 — the rect is found by the kit's own ink, and the
    reversed text is matched at the RECT'S OWN X, because the state cell is
    the fourth thing on that row and a search by colour alone would find the
    mode strip's words first.

    AND THE MECHANISM IS SHOWN SPENT RATHER THAN MERELY PRESENT: the same
    kit's seat is read in both moods, so "the title block reverses" cannot
    pass on a cell that reverses in every mood."""
    import fixture
    rows = sheet_rows("blueprint", "S2")
    assert fixture.MOOD == "alert", fixture.MOOD

    # exactly one knockout on this view, and it is the state cell
    assert sum(r.count(" on ") for r in rows) == 1, \
        [r for r in rows if " on " in r]
    knocked = [r for r in rows if " on " in r][0]
    assert "├ OVERDUE ┤" in plain(knocked), plain(knocked)

    # the .txt carries the SHAPE (the two-channel law); the .svg the ground
    txt = (FRAMES / "blueprint_S2.txt").read_text(encoding="utf-8")
    assert "├ OVERDUE ┤" in txt and "├ CLEAR ┤" not in txt

    k = LG.kit("blueprint")
    svg = (FRAMES / "blueprint_S2.svg").read_text(encoding="utf-8")
    rect = re.search(r'<rect x="([\d.]+)"[^>]*fill="%s"/>'
                     % re.escape(k.c["ink"]), svg)
    assert rect, "the alert run is not painted"
    run = re.search(r'<text x="%s"[^>]*fill="%s">([^<]*)</text>'
                    % (re.escape(rect.group(1)), re.escape(k.t["ground"])), svg)
    assert run, rect.group(0)
    assert run.group(1).replace(" ", " ") == "├ OVERDUE ┤"

    # spent, not merely present
    calm = LG.kit("blueprint")
    assert calm.mood == "clear"
    assert calm._state_cell() == ("├ CLEAR ┤", False)
    calm.mood = "alert"
    assert calm._state_cell() == ("├ OVERDUE ┤", True)


def test_a_form_never_told_the_mood_shows_no_first_fixation(monkeypatch):
    """TEETH. The picture depends on the FACT being handed over, and this is
    the arm that says so: with `F.MOOD` back at `clear` — which is what every
    sheet in this file did until inc56 — blueprint's S2 carries no reversed
    run at all and the title block reads `CLEAR`.

    IT PATCHES THE FIXTURE AND NOT THE KIT, deliberately. Patching
    `Blueprint.mood` would prove the kit reads an attribute; what round
    decision (G) is about is that nobody ever WROTE to it, so the teeth have
    to run the real composition with the real default."""
    sheet_rows("blueprint", "S2")            # puts screens on the path
    import fixture
    import screens
    monkeypatch.setattr(fixture, "MOOD", "clear")
    rows = screens.build("blueprint", "S2").rows
    assert sum(r.count(" on ") for r in rows) == 0, \
        [r for r in rows if " on " in r]
    assert any("├ CLEAR ┤" in plain(r) for r in rows), \
        [plain(r) for r in rows[-3:]]
    # ... and the ten that do not read the mood are unmoved either way
    for lang in LANGS:
        if lang == "blueprint":
            continue
        assert screens.build(lang, "S2").rows == sheet_rows(lang, "S2"), lang


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
        # the six runs: the query, in the page's ground, ON a rect of the hue.
        # PAIRED BY COORDINATE SINCE inc63. This used to read "no text run
        # anywhere in the sheet is painted in the ground colour except these
        # six", and it held only because the canvas was WRONG: the ground the
        # exporter wrote was Textual's `#121212`, a colour no kit declares, so
        # every legitimate knockout in the frame fell outside the query. With
        # the declared ground in place, solari's masthead plates paint ink in
        # `#0b0b0c` as well, and they are not match runs. Position is the
        # honest test of "on a plate": `svg_from_grid` puts a text run's
        # baseline 0.78 of a line below the top of its row, which is exactly
        # where that row's background rect starts.
        on_plate = []
        for tx, ty in re.findall(
                r'<text x="([-\d.]+)" y="([-\d.]+)" fill="%s"[^>]*>%s</text>'
                % (re.escape(ground), re.escape(QUERY)), svg):
            top = f"{float(ty) - 0.78 * 17.0:.1f}"
            on_plate.append(bool(re.search(
                r'<rect x="%s" y="%s" width="[\d.]+" height="[\d.]+" '
                r'fill="%s"/>' % (re.escape(tx), re.escape(top),
                                  re.escape(hue)), svg)))
        assert on_plate == [True] * 6, (lang, on_plate)
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
    those two are the only marks in this range it may contain.

    AND THE DASHED STROKES ARE EXCLUDED TOO, since inc69, ON THE DIAGONALS'
    OWN ARGUMENT EXTENDED: a stroke that is BROKEN closes no corner either.
    U+2504–U+250B and U+254C–U+254F are the light and heavy double, triple
    and quadruple dashes, and **this kit already spends five of them at five
    DEAD control seats** — `┆` at the knob, the checkbox, the field and the
    stepper's step, `╎` at the radio's ground and at `stepper.main` — without
    anybody having called them boxes in eight increments. Ruling L2 needs a
    mark for the one control that had none, and the marks a language spends
    on deadness are the marks it has.

    THE EXCLUSION IS PAID FOR IN THE SAME MOVE, and the law it buys is
    stronger than the clause it loosens: the test below now also asserts that
    **no button seat carries a mark at BOTH ends**, which is what "no boxes"
    actually claims and what a per-character codepoint rule could never see —
    `▪ Cancel ▪` is an enclosure and passes `is_wall` at every width, because
    neither cell is in the Box Drawing block at all."""
    if 0x2504 <= ord(ch) <= 0x250B or 0x254C <= ord(ch) <= 0x254F:
        return False              # broken: closes no corner (inc69)
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

    # AND NO SEAT IS MARKED AT BOTH ENDS (inc69). A box is an ENCLOSURE, and
    # a per-character rule cannot see one built out of cells that are not box
    # drawing at all. The declared seat is read at its two halves, the way
    # `Kit.button` splits it, and only the OPENING half may carry a mark. The
    # danger form is not in this clause for the reason it is not in `is_wall`:
    # `Kit.button` sets it round the WORD and not round the field.
    for st, glyph in k.PART_GLYPHS["button.main"].items():
        half = len(glyph) // 2
        assert not glyph[half:].strip(), (st, glyph, "marked at both ends")


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

    DISABLED IS NO LONGER AIR (inc69, ruling L2: *"a disabled control always
    carries a mark; air is not a state"*). inc38 made it air and gave the
    reason — *"nothing in this alphabet is lighter than `·` except a dashed
    RULE (`┆ ╎ ┈`), the shape being given up"* — and the shape was not given
    up: this kit draws a dashed rule at five other dead seats. The dead rung
    is `╎`, which is `stepper.main`'s dead cell, so it is DERIVED from the
    kit's own other `▫` seat rather than chosen; it is a different SHAPE from
    the square (so K4's channel law reads SHAPE, not diameter), it is no cell
    of `LEVELS`, `DANGER_FORM` or `REQUIRED`, and it is the one dashed
    vertical in this kit's dead vocabulary that is East-Asian-Width NEUTRAL
    where `┆` is AMBIGUOUS."""
    k = LG.kit("swiss")
    rungs = [k.PART_GLYPHS["button.main"][st].strip()
             for st in (LG.DEFAULT, LG.FOCUSED, LG.ACTIVE)]
    assert rungs == ["▫", "▪", "■"], rungs
    dead = k.PART_GLYPHS["button.main"][LG.DISABLED].strip()
    assert dead == "╎", dead
    # the kit's own other `▫` seat already answered "what is a dead ▫ here"
    assert k.PART_GLYPHS["stepper.main"][LG.DEFAULT] == "▫▫"
    assert set(k.PART_GLYPHS["stepper.main"][LG.DISABLED]) == {dead}
    # and it is not a square at another size -- the ladder keeps its own
    # shape and the dead rung steps OFF it, which is what "given up" means
    assert dead not in _twins("▫"), (dead, sorted(_twins("▫")))
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
#: WHAT A CHANNEL IS — ruling D (orchestrator, 2026-09-06, on the operator's
#: delegation), written here because every law in this section that says "the
#: two are distinct on a channel that language declares" needs the word to
#: mean something fixed.
#:
#:   COUNT      how many marks. `◎ ◉` against `· o O` — two concentric
#:              strokes against one (inc49).
#:   WEIGHT     how much ink one mark spends. `O` against `▊` (inc45).
#:   POSITION   where the mark stands. A caret inside a value against chrome
#:              at an opener (inc48, inc49).
#:   DIRECTION  which way it points. `▪` against `▶` (inc45).
#:
#: DIAMETER ALONE IS NOT A CHANNEL. Two drawings that differ only in HOW BIG
#: they are read as one mark, so `• / ●` is one bullet and `o / ◦` is one
#: ring. A language may not tell a MEANING apart from its own CHROME that
#: way, and `PROTOTYPE-inheritors-2.md` §0b is why the ruling was needed: five
#: of the six languages that had an increment resolved a collision by moving
#: to a neighbouring drawing. Four of the five spend a real channel and are
#: ACCEPTED, with the channel named — industrial `▪ → ▶` (direction), solari
#: `▁ → ▮` (shape family), darkside `O → ▊` (weight), darkside's knobs `◎ ◉`
#: against `· o O` (count). The fifth, swiss `• → ●`, is a homoglyph and
#: inc53 moved it.
#:
#: THE INSTRUMENT IS `prototypes/collision_census.py`, whose `HOMOGLYPHS`
#: table lists the pairs and whose `HOMOGLYPH_ROSTER` counts the rows per
#: language. The two cells THIS ruling covers have their teeth here, because
#: one of them is drawn outside `PART_GLYPHS` where no census can reach it.
#: THE THREE SLOTS A LANGUAGE DECLARES A REJECTED VALUE WITH — the grip
#: (`knob[INVALID]`), the two WALLS of the field (`textfield.main[INVALID]`)
#: and the two steps (`stepper.step[INVALID]`). This is inc51's clause 2 read
#: as a set instead of as a source: "what that kit already spends on a
#: rejected VALUE", the DECLARED invalid channel.
#:
#: THE RUNE IS NOT IN IT, and the exclusion is named rather than silent. A
#: field's glyph is "wall, RUNE, wall" (`Kit.field_form`) and the rune is the
#: PAPER the value's own cells are laid on — blueprint's `·` is the paper of
#: DEFAULT, ACTIVE and FOCUSED too, naught's and ledger's likewise. A paper
#: shared with every other state is not a rejection mark, and counting it
#: would have made "your value is wrong" out of "this is what a field is made
#: of here".
#:
#: THE SPLIT IS `LG.split_field_glyph` (rework-6c) — the same function
#: `Kit.field_form` calls and `collision_census.py::role_map` calls, so this
#: law and the census read the rune off one definition and cannot disagree
#: about which cell it is again.
#:
#: A FALLBACK IS NOT A DECLARATION, the same line `collision_census.py` draws:
#: only a table that has the key at all is read.
def _invalid_marks(k) -> str:
    out = []
    for key in ("knob", "textfield.main", "stepper.step"):
        g = k.PART_GLYPHS[key].get(LG.INVALID)
        if not g:
            continue
        if key == "textfield.main":
            op, _rune, cl = LG.split_field_glyph(g)
            out += [op, cl]                     # the two WALLS, not the rune
        else:
            out.append(g)
    return "".join(out)


#: THE FIVE LANGUAGE-LEVEL DECLARATIONS THAT MEAN SOMETHING ABOUT THE WORK,
#: read straight off the kit: how bad it is (the severity LADDER, all three
#: rungs as ONE declaration), whether the control destroys (`DANGER_FORM`),
#: whether the field is compulsory (`REQUIRED`), where the reader is (`CUR`),
#: and whether the value was REFUSED (the declared invalid channel). Three
#: rungs count as one because the census counts them as one: "two severity
#: rungs sharing a cell is a severity problem, not a collision"
#: (`prototypes/collision_census.py`).
#:
#: `invalid` JOINED THE SET IN inc52. It was excluded by name until then,
#: under inc39's ruling that a field whose un-flipped walls would collide with
#: DEFAULT takes that language's `DANGER_FORM` (spec §9.2). That ruling is
#: REVOKED: "does not parse" and "destroys data" are two meanings, and a
#: language that says both with one cell has said one of them.
def _meaning_marks(k) -> dict[str, str]:
    return {"ladder": "".join(k.LEVELS[x] for x in ("info", "warn", "error")),
            "danger": "".join(k.DANGER_FORM),
            "required": k.REQUIRED,
            "cursor": k.CUR,
            "invalid": _invalid_marks(k)}


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
#:
#: IT IS THE ONLY EXEMPTION, AND IT DOES NOT REACH `invalid` (inc52). TIER is
#: a channel a language declares — a rung set as a FORM around a label is the
#: same claim in another grammar. A REJECTED VALUE is not that claim at all,
#: so `DANGER_FORM` against the declared invalid channel has no exemption by
#: name and none by silence: swiss, darkside and blueprint each said both
#: with one cell and each moved one of the two.
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

    INVALID IS IN THIS SET SINCE inc52, and the ruling it reverses is named
    rather than left silent. inc39 ruled that where un-flipping a field's
    walls would collide with DEFAULT byte for byte, the walls take that
    language's own `DANGER_FORM` (spec §9.2), and inc51 applied it twice
    more. THAT RULING IS REVOKED (rework-5a): "does not parse" and "destroys
    data" are two meanings and one cell cannot carry both, so the declared
    invalid channel — the grip, the field's two WALLS, the two steps — is a
    fifth meaning here and may not share a cell with any of the other four.

    THE ONE EXEMPTION is `DANGER_IS_THE_TOP_RUNG`, by name and with the
    citation each kit carries, and it covers `danger` against `ladder` ONLY:
    a rung set as a form is a TIER of one declared channel. Nothing exempts a
    rejection from being told apart from a destruction."""
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
# inc52 (rework-5a) — the invalid channel joins the meaning set
# ===========================================================================
#: THE FIVE DECLARATIONS inc52 MOVED, as
#: `(language, kit, glyph-table key, the byte string HEAD carried, the two
#: roles the law must name)`. One arm each, restored one at a time, because
#: five languages moving in one increment is five independent declarations
#: and a teeth test that patched them together would prove one thing about
#: five kits.
#:
#: `darkside` IS THE ONE THAT PATCHES A MEANING RATHER THAN A GLYPH TABLE,
#: and that is the ruling: `Ø` was declared as this kit's rejection mark and
#: the danger form took it afterwards ("its own INVALID wall, the struck
#: mark"), so the mark that arrived second is the one that moved.
#: THE FIFTH FIELD IS inc60'S, and it exists because an arm can be killed by
#: a LATER cure rather than by a regression. blueprint's knob arm restores
#: `├` and asks for `("required", "invalid")` — and inc60 moved `REQUIRED`
#: off `├` onto `═`, so restoring the pre-inc52 byte string on its own now
#: collides with NOTHING and the arm went green for the wrong reason. The
#: fix is to restore the whole pre-inc52 state, obligation included, rather
#: than to weaken what the arm asserts: `(attribute, value)` is set on the
#: kit for the duration of the arm, `None` where the language's meanings have
#: not moved since inc52.
INVALID_CHANNEL_BEFORE = (
    ("swiss", "knob", "╲", ("danger", "invalid"), None),
    ("swiss", "textfield.main", "╲  ", ("danger", "invalid"), None),
    ("swiss", "stepper.step", "╲╲", ("danger", "invalid"), None),
    ("blueprint", "knob", "├", ("required", "invalid"), ("REQUIRED", "├")),
    ("blueprint", "textfield.main", "━·━", ("danger", "invalid"), None),
    ("blueprint", "stepper.step", "━━", ("danger", "invalid"), None),
    ("corgi", "knob", "▀▄", ("required", "invalid"), None),
    ("corgi", "textfield.main", "▄▀·▀▄", ("required", "invalid"), None),
    ("corgi", "stepper.step", "▀▄▄▀", ("required", "invalid"), None),
    ("instrument", "textfield.main", "⠸⠶⠇", ("ladder", "invalid"), None),
)


@pytest.mark.parametrize("lang,key,before,want,restore",
                         INVALID_CHANNEL_BEFORE)
def test_the_invalid_channel_law_goes_red_on_the_declarations_inc52_moved(
        monkeypatch, lang, key, before, want, restore):
    """TEETH — and they have to name the LANGUAGE and the TWO ROLES.

    The ruling this increment carries out is stated as a NEGATIVE: the
    declared invalid channel may not draw a cell from `DANGER_FORM`, `LEVELS`
    or `REQUIRED`. So the teeth restore one pre-inc52 declaration at a time
    and assert that the pair the ruling named is the pair reported — not that
    something, somewhere, went red.

    AND EACH ARM HOLDS THE OTHER TEN STILL, which is what says these are ten
    declarations in four kits rather than one shared defect: swiss's three
    slots each carry the collision alone, and so do blueprint's and corgi's.
    `instrument`'s single arm is the one that is NOT a danger collision — its
    closing rail `⠇` is `LEVELS["error"]` — and it is in the table to prove
    the law reaches the ladder and the obligation mark too, not only the
    danger form the ruling's teeth clause names."""
    def roles(x):
        return {frozenset(row[:2]) for row in shared_cell_pairs(x)}

    for x in LANGS:
        assert not roles(x), (x, shared_cell_pairs(x))

    kit = LG.kit(lang)
    tbl = dict(kit.PART_GLYPHS[key])
    tbl[LG.INVALID] = before
    monkeypatch.setitem(kit.PART_GLYPHS, key, tbl)
    if restore is not None:
        # the pre-inc52 MEANING, where a later increment moved it (inc60).
        attr, value = restore
        assert getattr(type(kit), attr) != value, (lang, attr, value)
        monkeypatch.setattr(type(kit), attr, value)

    assert frozenset(want) in roles(lang), (lang, key, shared_cell_pairs(lang))
    with pytest.raises(AssertionError):
        test_a_languages_meaning_marks_do_not_share_a_cell(lang)
    for x in LANGS:
        if x != lang:
            assert not roles(x), (x, shared_cell_pairs(x))


def test_the_invalid_channel_law_goes_red_on_darksides_restored_danger_form(
        monkeypatch):
    """THE ELEVENTH ARM, and the only one that moves a MEANING.

    darkside's `Ø` is the invalid mark at the knob, the field and the
    stepper, and `DANGER_FORM = ("Ø", "Ø")` carried the comment naming where
    it came from: *"its own INVALID wall, the struck mark"*. So the danger
    form is what inc52 moved and the invalid channel is what stayed, which is
    the opposite direction from swiss and blueprint — and the arm asserts the
    same two roles either way, because the law is about the CELL and not
    about which declaration is at fault."""
    def roles(x):
        return {frozenset(row[:2]) for row in shared_cell_pairs(x)}

    monkeypatch.setattr(LG.Darkside, "DANGER_FORM", ("Ø", "Ø"))
    assert frozenset(("danger", "invalid")) in roles("darkside"), \
        shared_cell_pairs("darkside")
    with pytest.raises(AssertionError):
        test_a_languages_meaning_marks_do_not_share_a_cell("darkside")
    for x in LANGS:
        if x != "darkside":
            assert not roles(x), (x, shared_cell_pairs(x))


def test_the_rune_is_excluded_from_the_invalid_channel_by_name(monkeypatch):
    """THE EXCLUSION'S OWN TEETH — an exclusion nobody can watch is a hole.

    `_invalid_marks` reads the field's two WALLS and not its RUNE. This
    asserts the boundary in both directions: a rune that IS a meaning is not
    a hit, and the SAME cell put on a WALL is one.

    inc60 HAD TO REBUILD THIS TEST AND THE REASON IS WORTH MORE THAN THE
    TEST. It used to ride on a live defect: blueprint's rune was `·` and
    `LEVELS["info"]` was `··`, so the exclusion could be watched without
    patching anything. inc60 sent blueprint's info rung to AIR, and with that
    the corpus has NO language left whose rune is a meaning — measured, all
    eleven. **An exclusion whose teeth depend on a defect being present dies
    the day the defect is cured**, and it dies GREEN, which is the worst way.
    So the meaning is patched in: `LEVELS["info"]` is set to the rune's own
    cell for the duration, and the two directions are asked of that."""
    k = LG.kit("blueprint")
    rune = LG.split_field_glyph(k.PART_GLYPHS["textfield.main"][LG.INVALID])[1]
    assert rune == "·", rune

    # ... and the corpus really has none left, which is what makes the patch
    # necessary rather than convenient.
    for lang in LANGS:
        kk = LG.kit(lang)
        g = kk.PART_GLYPHS.get("textfield.main", {}).get(LG.INVALID)
        if not g:
            continue
        r = LG.split_field_glyph(g)[1]
        live = {f: v for f, v in _meaning_marks(kk).items() if f != "invalid"}
        assert not any(r in _cells(v) for v in live.values()), (lang, r)

    monkeypatch.setattr(LG.Blueprint, "LEVELS",
                        {"info": rune * 2, "warn": "╌╌", "error": "━━"})
    assert rune in LG.kit("blueprint").LEVELS["info"]
    assert not shared_cell_pairs("blueprint")          # the rune is not read

    tbl = dict(k.PART_GLYPHS["textfield.main"])
    tbl[LG.INVALID] = f"{rune}╲{rune}"                 # rune and walls SWAPPED
    monkeypatch.setitem(k.PART_GLYPHS, "textfield.main", tbl)
    assert frozenset(("ladder", "invalid")) in {
        frozenset(r[:2]) for r in shared_cell_pairs("blueprint")}


def test_the_census_and_the_law_read_the_rune_off_one_function(monkeypatch):
    """rework-6c: `LG.split_field_glyph` is the one place that decides which
    cell of a rejected field is the RUNE. Before it existed, the LAW
    (`_invalid_marks`) and the CENSUS (`collision_census.role_map`) each
    split the glyph by hand — and could disagree, which is exactly what
    happened for five languages since inc52 and a sixth since inc66: twelve
    rows (six collisions, six homoglyphs) waiting on one decision (`spec.md`
    §15.5, §17.4, §17.8). This proves the two now read one function rather
    than two copies of the same arithmetic: break the split and both
    instruments move together, on the same live declaration."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "_census", FRAMES.parent / "collision_census.py")
    census = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(census)

    k = LG.kit("blueprint")
    glyph = k.PART_GLYPHS["textfield.main"][LG.INVALID]
    op, rune, cl = LG.split_field_glyph(glyph)
    assert rune == "·", (op, rune, cl)

    # TODAY: neither instrument reads the rune as a rejection mark.
    assert "·" not in _invalid_marks(k)
    named, _ = census.role_map("blueprint")
    assert "invalid" not in named.get("·", {}), named.get("·")

    # MOVE THE SPLIT, and both move: with the rune read one cell early, the
    # real rune becomes a WALL to both readers at once, not to one of them.
    monkeypatch.setattr(LG, "split_field_glyph", lambda g: ("", g[0], g[1:]))
    assert "·" in _invalid_marks(k)
    named2, _ = census.role_map("blueprint")
    assert "invalid" in named2.get("·", {}), named2.get("·")


# ===========================================================================
# inc53 (rework-5a) — diameter alone is not a channel
# ===========================================================================
#: ONE DRAWING AT ANOTHER SIZE OR FILL — ruling D AMENDED (2026-09-07). The
#: five hand-picked pairs became five FAMILIES and the pairs are derived from
#: them; `collision_census.py` owns the families and this file reads them, so
#: there is one table and not two (`test_the_homoglyph_table_is_one_table_in_
#: two_files` still asserts it, now over the families AND the derivation).
#:
#: WHY A FAMILY AND NOT A PAIR. inc53 decided "adjacent sizes only" and
#: measured the alternative at 20 rows against 6. That decision was taken
#: when the table was five pairs somebody had noticed, and
#: `PROTOTYPE-inheritors-3.md` §0d is what it cost: the four TIGHTEST pairs
#: in the corpus were outside it, so ruling D could only ever be enforced
#: against the pairs already found by hand. The amendment reverses it and
#: publishes the bill — 1 homoglyph row becomes 30.
HOMOGLYPH_FAMILIES = ("⋅·∙•●", "◦o○◎◉⊙⊛O", "▫□▪■", "†‡", "╌┄┈")
HOMOGLYPHS = tuple((a, b) for fam in HOMOGLYPH_FAMILIES
                   for i, a in enumerate(fam) for b in fam[i + 1:])


def _twins(ch: str) -> set:
    """Every cell that is the same drawing as `ch` at another size or fill.

    A SET AND NOT A CELL, since inc68: the old `_twin` returned ONE partner
    because the table was pairs. A family has as many as it has members, and
    a caller asking "is this mark a homoglyph of that one" has to be handed
    all of them or it is asking about whichever the table happened to list
    first."""
    for fam in HOMOGLYPH_FAMILIES:
        if ch in fam:
            return set(fam) - {ch}
    return set()


def test_swisss_chosen_option_is_not_the_obligation_mark_at_another_size():
    """`REQUIRED` is `•` and the radio's chosen mark was `●` — one solid disc
    at two diameters, which ruling D says is no channel at all.

    THE ASSERTION IS ABOUT THE PAIR AND NOT ABOUT THE NEW CELL, so it still
    bites if somebody picks a different answer later: no cell of any
    `radio.knob` state may be `REQUIRED`, and none may be `REQUIRED`'s
    HOMOGLYPH. The second clause is the one inc46 walked past.

    AND THE DISTINCTION THE BULLET USED TO CARRY IS ASSERTED WHERE IT MOVED:
    a checkbox leads with a full-height rule and a radio with a half-height
    tick, in every state, so the two controls are still told apart without
    the shape of their bullet."""
    k = LG.kit("swiss")
    req = k.REQUIRED
    for st, glyph in k.PART_GLYPHS["radio.knob"].items():
        assert req not in glyph, (st, glyph, req)
        assert not (_twins(req) & set(glyph)), (st, glyph, sorted(_twins(req)))
    box = k.PART_GLYPHS["checkbox.knob"]
    radio = k.PART_GLYPHS["radio.knob"]
    assert set(box) == set(radio), (sorted(box), sorted(radio))
    for st in box:
        assert box[st][0] != radio[st][0], (st, box[st], radio[st])
        assert box[st][1:] == radio[st][1:], (st, box[st], radio[st])


def test_naughts_two_option_controls_do_not_rest_on_one_drawing():
    """L10, and it is the objection three rounds put to `naught_S2`.

    Nine languages separate a radio from a checkbox by SHAPE FAMILY — round
    well, square box — and this one cannot: everything here is round, and the
    kit says so in its own table. What it CAN do is not spend both controls'
    RESTING cells out of one homoglyph family, and until inc72 it did:
    `HOMOGLYPH_FAMILIES` reads `◦ ○ ◎ ◉ ⊙ ⊛` as one drawing at six diameters
    and fills, and rows 9 and 11 of `naught_S2` were drawn from four of them,
    two rows apart. The round's criterion — *"cover the label column and say
    which row is a single choice and which are independent boxes"* — had no
    answer.

    THE LAW IS ABOUT THE RESTING PAIR AND NOT ABOUT THE NEW CELLS, so it
    still bites if somebody picks different answers later: neither cell a
    radio rests on may be a checkbox's resting cell, nor that cell's
    homoglyph. It is deliberately NOT asked of every state — closing the
    whole table is `STATES_TOLD_APART_BY_SIZE`'s eight rows and that roster
    says in its own note that it needs a second channel for this alphabet.
    What a form DRAWS is the unticked box and the unchosen well, and those
    are what this asks about.

    AND IT IS READ OFF THE SHIPPED FRAME TOO, because a kit table can be
    right while the sheet a reader holds is not: the two option rows of
    `naught_S2` may share no cell at all."""
    k = LG.kit("naught")
    box = (k.PART_GLYPHS["checkbox.main"][LG.DEFAULT],
           k.PART_GLYPHS["checkbox.knob"][LG.DEFAULT])
    well = (k.PART_GLYPHS["radio.main"][LG.DEFAULT],
            k.PART_GLYPHS["radio.knob"][LG.DEFAULT])
    for a in well:
        for b in box:
            assert a != b, (a, b)
            assert b not in _twins(a), (a, b, sorted(_twins(a)))

    rows = (FRAMES / "naught_S2.txt").read_text(
        encoding="utf-8").splitlines()
    opts = [r for r in rows if " low " in r or " api " in r]
    assert len(opts) == 2, opts
    marks = [set(r) - set(" abcdefghijklmnopqrstuvwxyz") for r in opts]
    assert marks[0] and marks[1], marks
    assert not (marks[0] & marks[1]), sorted(marks[0] & marks[1])


def test_the_option_control_law_bites_on_the_declaration_naught_shipped(
        monkeypatch):
    """TEETH, on the exact table this kit carried for six batches.

    Both arms are asserted, because the two halves of the defect are
    different: the WELL's ring was the box's ring at another diameter
    (`○` against `◦`) and the CHOSEN mark was the ticked mark at another
    diameter (`⊙` against `◉`). Restoring either one alone must be enough to
    go red, or the law would be passing on the pair rather than on the
    cells."""
    k = LG.kit("naught")
    for part, cell in (("radio.main", "○"), ("radio.knob", "⊙")):
        monkeypatch.setitem(k.PART_GLYPHS[part], LG.DEFAULT, cell)
        with pytest.raises(AssertionError):
            test_naughts_two_option_controls_do_not_rest_on_one_drawing()
        monkeypatch.undo()
    assert k.PART_GLYPHS["radio.main"][LG.DEFAULT] == "◌"
    assert k.PART_GLYPHS["radio.knob"][LG.DEFAULT] == "⊚"


def test_darksides_field_leader_is_not_a_severity_rung_at_another_size():
    """The seat under every figure in darkside's detail pane was `◦`, and
    `LEVELS["warn"]` is `o ` — one ring at two diameters.

    THIS TEST EXISTS BECAUSE NO CENSUS CAN SEE IT. `field_row` draws the mark
    itself, outside `PART_GLYPHS`, which is the limit inc49 §11 published for
    `Darkside.tabs()` and spec §10.4 for `▬`. So the law is read off the
    RENDERED ROW.

    IT ALSO ASSERTS THE SECOND REASON, which is a different law's: `◦` is
    `LG.NA.OFF`, naught's own unlit pixel, and `verify_language` holds
    "naught's pixel pair is exclusive to naught on the board". That law is
    scoped to the meter, so this row sat just outside it."""
    k = LG.kit("darkside")
    cap, val = "status", "open"
    row = plain(k.field_row(cap, val, 40))
    # THE LEADER IS ISOLATED RATHER THAN SEARCHED FOR, so the assertion cannot
    # be satisfied by a letter of the caption or of the figure: everything
    # between the end of one and the start of the other, stripped.
    assert row.startswith(cap) and row.endswith(val), row
    leader = row[len(cap):len(row) - len(val)].strip()
    assert len(leader) == 1, (leader, row)

    rungs = set("".join(k.LEVELS.values())) - set(" ")
    assert leader not in rungs, (leader, sorted(rungs))
    assert not (_twins(leader) & rungs), (leader, sorted(_twins(leader) & rungs))
    assert leader != "◦" and LG.NA.OFF == "◦", (leader, LG.NA.OFF)
    assert leader == "▔", leader


def test_the_homoglyph_table_is_one_table_in_two_files():
    """Two copies of a list is two lists. The census owns the table and this
    suite reads it, so a pair added in one file and not the other goes red
    here rather than making the two instruments disagree in silence."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "_census", FRAMES.parent / "collision_census.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert tuple(mod.HOMOGLYPH_FAMILIES) == HOMOGLYPH_FAMILIES, \
        (mod.HOMOGLYPH_FAMILIES, HOMOGLYPH_FAMILIES)
    assert tuple(mod.HOMOGLYPHS) == HOMOGLYPHS, (mod.HOMOGLYPHS, HOMOGLYPHS)
    # AND THE DERIVATION IS THE SAME DERIVATION, not two spellings of it: a
    # family of n members is n(n-1)/2 pairs, and both files have to agree on
    # that as well as on the families.
    assert len(HOMOGLYPHS) == sum(len(f) * (len(f) - 1) // 2
                                  for f in HOMOGLYPH_FAMILIES) == 48
    # triangles are NOT a family (ruling D amended, and the D-addendum's
    # reason: they differ by DIRECTION, which is a channel)
    assert not any({"▶", "▼"} <= set(f) for f in HOMOGLYPH_FAMILIES)


# ===========================================================================
# inc46 (rework-3) — the other two seats the batch rule names
# ===========================================================================
#: the six controls the census reads, so the two files ask the same question
#: of the same set.
RULED_CONTROLS = ("button", "checkbox", "radio", "switch", "textfield",
                  "stepper")

#: THE KNOB IS A NAMED SEAT TOO (inc49), and leaving it out was a BLIND SPOT
#: rather than a narrowing. inc46 wrote the indicator clause as
#: `comp == "switch" and part == "indicator"` — and in these kits the
#: indicator is the TRACK and the knob is the PERILLA, the cell a reader
#: points at and calls "the switch". `PROTOTYPE-inheritors-2.md` §0c
#: photographed what the gap hid: darkside drew the knob of all five switches
#: on `darkside_S3` with `O`, which is `LEVELS["error"]` (`▬▬O`, `O──`),
#: while this roster said **0**. The same hole hid `naught ◉` (`REQUIRED` at
#: the knob) and `corgi ██` / `▀▀` (the error and warn rungs at the knob).
#:
#: So the seat set is every KNOB the registry reaches — `switch.knob`,
#: `checkbox.knob`, `radio.knob` — plus the switch indicator and every
#: disabled mark. The slider's knob is out only because `RULED_CONTROLS` is
#: the census's six and the slider is not one of them; that boundary is the
#: census's, not this law's.
#:
#: WHAT IS STILL WRONG, COUNTED. Four languages draw a mark that MEANS
#: something at a seat the batch rule names — a DISABLED mark, a switch's
#: INDICATOR or a KNOB — and this roster is the measurement rather than a
#: promise. It is asserted exactly, both ways: a language that gets worse is
#: red, and a language that gets better is red until somebody edits this
#: line, which is the only way a roster stays a record instead of a
#: decoration (`HANDED_FIELDS`, one screen up, is the same bargain).
#:
#:   naught     0  WAS 12 (8 + 4) and is ZERO since inc61 (`rework-5c`,
#:                 ruling A) — the LAST of the eleven. `∙` was the switch's
#:                 ON indicator, and the composer draws that track TWO cells
#:                 wide, so `naught_S3` rendered every live switch as `∙∙◉`
#:                 — `∙∙` is `LEVELS["error"]` and the `DANGER_FORM` byte
#:                 for byte, twelve rows above `◦ ∙Delete all∙ ◦`. `◉` was
#:                 `REQUIRED` at both knobs. The live track is scoped to
#:                 `switch.indicator` and takes `⊖`, the contact CLOSED;
#:                 obligation takes `⊛`. `◦`, the dead track, is exempt by
#:                 name — `THE_GROUND_IS_NOT_A_MARK`, one language, one cell.
#:   corgi      0  WAS 16 (8 + 8) and is ZERO since inc58 (`rework-5c`,
#:                 ruling A). The segment bank was the switch's whole
#:                 track — `▄▄` ON, `▁▁` dead, `LEVELS["warn"]` and
#:                 `LEVELS["info"]` — and the grip of every switch and
#:                 slider was `██` / `▀▀`, the error rung and the obligation
#:                 mark. inc58's ruling: THE BANK IS THE READING, THE PANEL
#:                 IS THE METAL. The four DRIVEN heights (`▁ ▄ ▀ █`) carry
#:                 the meanings and nothing else; the switch takes scoped
#:                 `switch.main` / `switch.indicator` on the shade ramp and
#:                 the KNOB takes the QUADRANT family (`▙▟ ▛▜ ▘▝ ▖▗`),
#:                 which is inc46's "a knob drawn like the fill is not a
#:                 knob" made structural rather than repeated.
#:   prism      0  WAS 16 (8 + 8) and is ZERO since inc59 (`rework-5c`,
#:                 ruling A). `⣿` was the switch's ON indicator and `⣤` its
#:                 dead one — the ladder's top two rungs — and the radio's
#:                 chosen cell was `⣿` at six more seats. inc59's ruling: THE
#:                 EMBER IS READ FROM THE BOTTOM, A CONTROL IS READ FROM THE
#:                 TOP. The switch takes scoped tables on the top-carved
#:                 ramp (`⠉ ⠛ ⠿`) and the radio's chosen cell takes the HALF
#:                 CELL `⢸`, which is this kit's own sentence about the part
#:                 it is: "the knob is a HALF-CELL mark ... the only
#:                 vocabulary here whose grip can sit inside a cell".
#:   blueprint  0  WAS 12 (8 + 4) and is ZERO since inc60 (`rework-5c`,
#:                 ruling A). `╌` was `LEVELS["warn"]` AND this language's
#:                 whole DISABLED vocabulary — five parts wore it — and `├`,
#:                 `REQUIRED`, stood at the checkbox's and the radio's knob.
#:                 inc60's ruling: THE TERMINATORS ARE CHROME AND NOTHING
#:                 ELSE, AND A MEANING IS A LINE TYPE. Obligation left the
#:                 terminator for a doubled RUN (`═`); every DEAD run took
#:                 `┄`, the light TRIPLE dash this kit already drew at its
#:                 dead indicator, told from `╌`'s double dash by COUNT.
#:
#: THE FOUR WERE NOT NEW FAILURES WHEN inc49 WIDENED THE CLAUSE, and they are
#: the four languages `PROTOTYPE-inheritors-2.md` §6 decision **A** puts to
#: the operator (corgi, prism and blueprint have never had an increment;
#: naught has no unspent cell). **Ruling A (orchestrator, 2026-09-06, on the
#: operator's delegation) gives each of them an increment**, and `rework-5c`
#: is those increments: corgi in inc58, prism in inc59, blueprint in inc60,
#: naught and ledger in inc61. The one language the blind spot was HIDING —
#: darkside, which read 0 while wearing the error rung on five knobs — is
#: fixed at its own declaration in inc49 and is 0 for a reason now.
#:
#: SOLARI WAS 6 AND IS 0 (inc47): `▁` was `REQUIRED` and the switch's
#: indicator and eighteen more chrome seats; obligation moved to `▮` and the
#: seam went back to being alphabet. instrument and swiss went to zero in
#: inc46, darkside in inc49, corgi in inc58, prism in inc59, blueprint in
#: inc60 and naught in inc61. **ALL ELEVEN are clean.**
MEANING_AT_A_NAMED_SEAT = {"naught": 0, "corgi": 0, "instrument": 0,
                           "swiss": 0, "industrial": 0, "nord": 0,
                           "darkside": 0, "prism": 0, "ledger": 0,
                           "solari": 0, "blueprint": 0}


#: THE SECOND NAMED EXEMPTION, ONE LANGUAGE AND ONE CELL (inc61) — and it is
#: an extension of `BLANKS`, not of the rule.
#:
#: `BLANKS` above says the ASCII space and U+2800 BRAILLE PATTERN BLANK are
#: "not a cell — a language that pads two roles with the same nothing has not
#: overloaded anything". **naught's nothing is not a space.** LANGUAGES.md §0
#: commits it to a VISIBLE unlit grid — "dark dots render in the dim tier
#: rather than as spaces ... that faint lattice IS the signature" — so where
#: ledger and blueprint write an info rung as `"  "`, naught writes `◦◦`, two
#: UNLIT dots, and `naught_S1` draws some seven hundred more of them ruling
#: every gap, every leader and both panes. A ground is not a mark.
#:
#: WHAT IT COVERS AND WHERE IT STOPS. `NA.OFF` only, at the two seat laws
#: only. `NA.ON` — the LIT dot — is NOT in it and never will be: it carries
#: `DANGER_FORM` and two rungs of the ladder, and inc61 moved every control
#: off it (the switch's live track was drawing `∙∙`, byte for byte
#: `LEVELS["error"]`, on five rows of `naught_S3`). The one-mark-one-meaning
#: law is untouched — a ladder's rungs are MEANT to share cells — and so is
#: the census, whose rows are questions rather than verdicts.
#:
#: DERIVED, NOT TYPED: the cell is read from `LG.NA.OFF`, so a kit that moves
#: its unlit pixel moves the exemption with it and cannot leave a stale
#: literal behind.
THE_GROUND_IS_NOT_A_MARK = {
    "naught": ("`NA.OFF` — the UNLIT lattice dot. LANGUAGES.md §0: \"the "
               "unlit grid is visible ... that faint lattice IS the "
               "signature\". It is this language's BLANK, the way `\"  \"` "
               "is ledger's and blueprint's."),
}


def _seat_meanings(k, lang: str) -> set[str]:
    """The cells a MEANING would be read from at a control seat, with the
    named ground exemption subtracted.

    ONE FUNCTION FOR BOTH SEAT LAWS, so the opener law and the named-seat law
    can never drift apart about what a meaning is — which is the drift
    `test_the_homoglyph_table_is_one_table_in_two_files` exists to prevent
    one screen up, applied to this file's own two readers."""
    out = (set("".join(k.LEVELS.values())) | {k.REQUIRED}
           | set("".join(k.DANGER_FORM))) - set(BLANKS)
    if lang in THE_GROUND_IS_NOT_A_MARK:
        assert THE_GROUND_IS_NOT_A_MARK[lang].strip(), lang
        out -= {LG.NA.OFF}
    return out


#: THE KNOB SEATS THE REGISTRY REACHES. `COMPONENT_PARTS` gives the switch,
#: the checkbox and the radio a `knob`, and all three are the cell a reader
#: reads as the control's VALUE. Written as a set rather than as
#: `part == "knob"` so the slider's exclusion is visible: the slider is not
#: in `RULED_CONTROLS`, and that is the census's boundary, not a claim that a
#: slider's grip may wear a severity rung.
#:
#: inc67 ADDS THE SLIDER'S (K5, ruling A amended). The exclusion above was
#: honest and its reason expired: the census's boundary moved, so the slider
#: is in set B and its grip is a seat like the other three. It costs nothing
#: -- all eleven knobs are clean (`◉ ▙▟ ⡇ │ | ▌ ◎ ⢸ ▪ ▼ ┤`, not one of them a
#: rung) -- and it is here so the day one is not, somebody has to edit a
#: number.
#:
#: THE DEAD-MARK CLAUSE IS NOT EXTENDED WITH IT, and the narrowing is
#: measured rather than assumed. Ruling A amended asks for "the opener/knob
#: laws where a quantity widget has an opener or a knob"; a slider's DISABLED
#: track is neither. Measured before it was left out: looping the slider
#: through the dead clause as well costs exactly ONE row, corgi's
#: `slider.indicator[disabled]` (`▁▁`, `LEVELS["info"]` -- a dead fill drawn
#: with the calm rung), and nothing anywhere else. Named so the next round
#: argues with a number.
KNOB_SEATS = (("switch", "knob"), ("checkbox", "knob"), ("radio", "knob"),
              ("slider", "knob"))


def meaning_marks_at_named_seats(lang: str) -> list[tuple]:
    """Every DISABLED mark, every switch INDICATOR and every KNOB that is
    drawn with a cell this language spends on severity, danger or obligation.

    `CUR` is deliberately NOT in the set. The batch rule's second clause names
    three seats a MEANING may not stand at, and inc48's opener law names the
    same three declarations — `LEVELS`, `DANGER_FORM`, `REQUIRED`. A cursor
    says where the reader is, not what the work is worth, and a language that
    spends its cursor cell on a knob has not told anybody their data is
    rejected. Named, so the narrowing is a decision and not an oversight."""
    k = LG.kit(lang)
    meanings = _seat_meanings(k, lang)
    out = []
    # the six ruled controls, plus the slider for its KNOB alone (inc67) --
    # see `KNOB_SEATS` for why the dead clause does not follow it here.
    for comp in RULED_CONTROLS + ("slider",):
        for part in LG.COMPONENT_PARTS[comp]:
            table = k.PART_GLYPHS[k.part_key(comp, part)]
            for st in LG.component_states(comp):
                dead = (LG.control_of(st) == LG.DISABLED
                        and comp in RULED_CONTROLS)
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
                named = (dead
                         or (comp == "switch" and part == "indicator")
                         or (comp, part) in KNOB_SEATS)
                if named:
                    out.append((f"{comp}.{part}", st, glyph,
                                "".join(sorted(hit))))
    return out


@pytest.mark.parametrize("lang", LANGS)
def test_a_meaning_never_stands_at_a_disabled_or_indicator_seat(lang):
    """THE BATCH RULE'S SECOND CLAUSE, at every seat but the opener.

    A mark that means something about the WORK — a severity rung, the danger
    form, the obligation mark — may not stand where a reader would take it for
    that meaning. The seats are the OPENER of a control (inc48), the
    INDICATOR of a switch, a DISABLED mark, and — since inc49 — every KNOB
    the registry declares. This law is all of those but the opener.

    THE KNOB WAS MISSING AND IT WAS THE SEAT THE FRAME SHOWS. inc46 wrote the
    clause as `comp == "switch" and part == "indicator"`; in these kits the
    indicator is the TRACK. `PROTOTYPE-inheritors-2.md` §0c photographed the
    hole: `darkside_S3` drew five switch knobs with `O`, this language's
    `LEVELS["error"]` (`▬▬O   ▬▬O   O──`), and the roster said 0 —
    the census saw it (`O [3 families]`) and the law did not. Widening the
    clause to `switch.knob`, `checkbox.knob` and `radio.knob` moves five of
    the eleven: darkside 0 → 4 (fixed at the declaration, back to 0),
    naught 8 → 12, corgi 8 → 16, prism 8 → 16, blueprint 8 → 12.

    THE FRAMES IT WAS WRITTEN OFF. `instrument_S3`: `⠁` is `REQUIRED` in `S2`
    and the DISABLED switch here, and the round's criterion is that showing
    the two screens in sequence produces two correct answers to "what does
    `⠁` mean" with no cue on either. `swiss_S1`/`S5`: `━` is the error rung
    and the switch's ON indicator, so a switch that is on and a row that has
    failed are one cell.

    IT IS A MEASUREMENT, NOT A PASS. Four languages still fail it and the
    count is asserted per language, so the roster can only move when somebody
    edits it. That is deliberate: a law scoped to the languages that already
    obey it would be a law that never says anything about the ones that do
    not."""
    assert len(meaning_marks_at_named_seats(lang))         == MEANING_AT_A_NAMED_SEAT[lang], (lang,
                                           meaning_marks_at_named_seats(lang))


def test_the_named_seat_law_goes_red_on_the_three_declarations_it_moved(
        monkeypatch):
    """TEETH — and they have to be, because four of the eleven arms of the law
    above assert a NON-ZERO count, which is the shape of assertion that rots
    into a snapshot if nobody watches it fire.

    Arm one restores instrument's dead rung to `⠁`, the obligation mark, on
    the one part `instrument_S3` photographed. Arm two restores swiss's switch
    indicator to `━`, the error rung. Arm three restores darkside's grip to
    `O`, `LEVELS["error"]` — the declaration inc49 moved, and the seat inc46's
    clause could not reach. Each must move that language's count off zero, and
    each must name the SEAT and the MARK, because "darkside is 4" without
    `switch.knob` and `O` in it is a number the next reader has to re-derive
    from the kit."""
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

    # ARM THREE — the knob seat, and the one the old clause was blind to.
    # `knob` is the SHARED table, so restoring it moves the switch and leaves
    # `checkbox.knob` (its own table) where inc49 put it: the hits must name
    # the two SHARED knob seats and nothing else, which is what proves the
    # widening is what caught it rather than the disabled arm catching it
    # sideways.
    #
    # inc67 ADDED THE SECOND OF THOSE TWO. This arm read `switch.knob` alone
    # until the slider's grip joined `KNOB_SEATS`; darkside's `knob` table is
    # the switch's AND the slider's, so one restored declaration now shows at
    # both, and the arm says so rather than being narrowed back to one.
    tbl = dict(LG.Darkside.PART_GLYPHS["knob"])
    tbl[LG.DEFAULT] = "O"
    monkeypatch.setitem(LG.Darkside.PART_GLYPHS, "knob", tbl)
    hits = meaning_marks_at_named_seats("darkside")
    assert hits, hits
    assert {h[0] for h in hits} == {"switch.knob", "slider.knob"}, hits
    assert all(h[3] == LG.kit("darkside").LEVELS["error"].strip()
               for h in hits), hits
    assert all(len(meaning_marks_at_named_seats(o))
               == MEANING_AT_A_NAMED_SEAT[o]
               for o in LANGS if o != "darkside")
    monkeypatch.undo()

    for lang in LANGS:
        assert (len(meaning_marks_at_named_seats(lang))
                == MEANING_AT_A_NAMED_SEAT[lang]), lang


# ===========================================================================
# inc48 (rework-3) — the opener law, the batch rule's first named seat
# ===========================================================================
#: THE STEPPER IS IN SINCE inc51, AND ITS EXCLUSION IS WHAT WENT AWAY. This
#: tuple used to stop at `textfield`, on inc39's ruling that "a stepper's
#: halves are DIRECTIONS, not walls, so it needs its own law" (spec §9.5) — a
#: law about what OPENS an enclosure could not be asked of a pair that
#: encloses nothing. That ruling was right about ENCLOSURE and wrong about
#: ANNOUNCEMENT: whatever cell stands first is what a reader meets first,
#: whether it is a wall or an arrow. The stepper's own law is written now
#: (`test_a_steppers_halves_are_directions_and_invalid_is_not_a_turn`), so the
#: exclusion has nothing left to stand on.
#:
#: WHAT IT COST, PAID RATHER THAN ABSORBED. inc48 §5 published the bill in
#: advance: "it costs the law swiss's and nord's `stepper.main` (`··`, whose
#: first cell is `LEVELS["info"]`), five seats each". Both were paid at the
#: declaration in inc51 and not by an exemption — swiss's dead end takes `▫`,
#: the lightest rung of the one-shape ladder inc46 built it, and nord's takes
#: `░`, the lightest rung of the shade ramp this kit already owns — so both
#: stay at 0. The four languages that grew (naught 2→3, corgi 31→40,
#: prism 19→25, blueprint 6→12) were already on the roster.
OPENING_CONTROLS = ("button", "checkbox", "radio", "switch", "textfield",
                    "stepper")

#: WHAT STILL OPENS WITH A MEANING, COUNTED — the same bargain
#: `MEANING_AT_A_NAMED_SEAT` and `HANDED_FIELDS` make, for the same reason:
#: a roster is a record only while somebody has to edit it.
#:
#:   naught      0  WAS 3 (2 + 1) and is ZERO since inc61 (`rework-5c`,
#:                  ruling A). `◉◉`, the ACTIVE step, opened on `REQUIRED`
#:                  and obligation moved off the charge ramp. **The other
#:                  two were the argument this comment carried unresolved
#:                  since inc48 and it is GRANTED now**: `◦` opens the button
#:                  and the field, `LEVELS["info"]` is `◦◦`, and naught's
#:                  info rung is ZERO LIT DOTS — the unlit lattice
#:                  LANGUAGES.md §0 calls this language's visible GROUND. So
#:                  "nothing is lit" and "an empty seat" ARE one thing, the
#:                  way `"  "` is one thing for ledger and blueprint. The
#:                  exemption is `THE_GROUND_IS_NOT_A_MARK`, by name, with
#:                  its citation, and ruling A is the authority the comment
#:                  said it was waiting for.
#:   corgi       0  WAS 38 — the widest entry this roster ever carried — and
#:                  is ZERO since inc58 (`rework-5c`, ruling A). The segment
#:                  bank was `LEVELS` and the chrome ladder at once
#:                  (`▁▁ ▄▄ ██` against `▁▁ ▔▔ ▂▂ ··`), and inc51's stepper
#:                  added ten seats of it. **An exemption for the whole ramp
#:                  was measured and refused**: the exemption's own condition
#:                  is that a control's opener stay distinct from an error
#:                  rung IN THE FRAME, and `corgi_S2` draws `██` as the
#:                  error message's leader (`██ expected YYYY-MM-DD`) three
#:                  rows under `██ ON ui`, the CHECKED checkbox, while
#:                  `corgi_S3` draws `██` as the slider's KNOB twelve rows
#:                  above `▁▁█Delete all█▁▁`. So the controls moved instead:
#:                  the four driven heights are the readings, the shade ramp
#:                  and the quadrants are the panel.
#:   prism       0  WAS 25 (19 + 6) and is ZERO since inc59 (`rework-5c`,
#:                  ruling A). `⣿` was `LEVELS["error"]`, the `DANGER_FORM`
#:                  **and** the opening cell of the button, the checkbox and
#:                  the field, so `prism_S4` drew
#:                  `⣿⣤ ⣿Delete⣿ ⣤⣿   ⣿⣀  Cancel  ⣀⣿` — the destructive
#:                  form and the safe button's WALL, the same cell, eight
#:                  columns apart on ONE ROW. inc51's five ground seats and
#:                  the DEFAULT step (`⡀⢀`, opening on `REQUIRED`) went with
#:                  them. The ember fills the cell from the bottom; a control
#:                  is the same dot-rows read from the TOP and stops one row
#:                  short of `⣿` by construction.
#:   blueprint   0  WAS 12 (6 + 6) and is ZERO since inc60 (`rework-5c`,
#:                  ruling A). `├` was `REQUIRED` and the dimension's opening
#:                  terminator — §9.4's `blueprint_S2`, the oldest finding
#:                  still open in this worktree, and the frame shows it
#:                  twice: `title├` and `due├` eleven rows above `├ ┤ api`
#:                  and `├   Cancel   ┤`. inc51's ground (`··` at five
#:                  states, `LEVELS["info"]`) and its dead one (`╌╌`,
#:                  `LEVELS["warn"]`) went with it — the ground stopped
#:                  being a rung when INFO WENT TO AIR, which is this
#:                  sheet's own commitment ("a calm sheet carries zero
#:                  alert") and `Ledger.LEVELS`'s precedent since inc45.
#:
#: **ALL ELEVEN ARE ZERO SINCE inc61**: instrument (inc46), swiss (inc46 and
#: inc51), industrial (inc48), darkside (inc48), nord (inc51), ledger and
#: solari (inc47), corgi (inc58), prism (inc59), blueprint (inc60) and naught
#: (inc61). Two exemptions carry the corpus and both are by name with a
#: citation: `DANGER_IS_THE_TOP_RUNG` (four languages) and
#: `THE_GROUND_IS_NOT_A_MARK` (naught's unlit dot). **swiss and nord stayed at zero through the stepper's
#: arrival because inc51 paid their two `stepper.main` declarations rather
#: than exempting them** — see `OPENING_CONTROLS` above for the bill and who
#: paid it.
MEANING_AT_AN_OPENER = {"naught": 0, "corgi": 0, "instrument": 0, "swiss": 0,
                        "industrial": 0, "nord": 0, "darkside": 0, "prism": 0,
                        "ledger": 0, "solari": 0, "blueprint": 0}


def meaning_marks_at_an_opener(lang: str) -> list[tuple]:
    """Every control glyph whose FIRST cell is a mark this language spends on
    severity, danger or obligation.

    NO EXEMPTIONS (inc52). This carried one until rework-5a: a field whose
    INVALID walls are that language's own `DANGER_FORM`, on inc39's ruling
    that where un-flipping the walls would collide with DEFAULT byte for byte
    the walls take the danger form (spec §9.2). THAT RULING IS REVOKED —
    "does not parse" and "destroys data" are two meanings — so the exemption
    has no ruling to stand on and it is deleted rather than left as an
    exemption nothing sits under. Measured before the deletion, it fired ZERO
    times across all eleven: swiss, darkside, blueprint and corgi had already
    moved off it in the same increment, so the rosters below are unchanged by
    the deletion itself and corgi's -2 is the DECLARATIONS moving."""
    k = LG.kit(lang)
    meanings = _seat_meanings(k, lang)
    out = []
    for comp in OPENING_CONTROLS:
        for part in LG.COMPONENT_PARTS[comp]:
            for st in LG.component_states(comp):
                glyph = k.part_glyph(part, st, comp)
                if len(glyph) < 2 or glyph[0] not in meanings:
                    continue
                out.append((f"{comp}.{part}", st, glyph, glyph[0]))
    # THE QUANTITY WIDGET THAT HAS AN OPENER, and only that one (inc67, K5,
    # ruling A amended). Two of the thirteen mechanisms BRACKET their run --
    # industrial's `[ ... ]` and blueprint's `├ ... ┤` -- and a bracket is an
    # announcement in exactly the sense this law means: the first cell the eye
    # reaches before the quantity starts.
    #
    # THE SLIDER, THE BAR AND THE SCROLL BAR ARE NOT ASKED, and the narrowing
    # is structural rather than a scope choice. Their `main` and `indicator`
    # are a cell the composer REPEATS, so `▁▁`'s "opener" is `▁` and its
    # "closer" is `▁` -- the same cell twice, with no bracket and nothing
    # announced. Reading a run's first cell as an opener would ask the fill
    # law's question a second time in worse words; measured before it was left
    # out, it fires on corgi FIFTEEN times and on nothing else, and every one
    # of those fifteen is already a row on `FILL_IS_NOT_A_MEANING`.
    for seat in ("meter.open", "meter.close"):
        glyph = k.quantity_glyphs().get(seat, "")
        if glyph and glyph[0] in meanings:
            out.append((seat, "declared", glyph, glyph[0]))
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


# ===========================================================================
# inc58 (rework-5c) — corgi crosses its own frontier
# ===========================================================================
#: THE ELEVEN DECLARATIONS inc58 MOVED, as `(glyph-table key, the table HEAD
#: carried before this increment, the opener seats it is worth, the named
#: seats it is worth)`. `None` for a table means the key DID NOT EXIST: the
#: switch had no scoped tables and fell through to the slider's `main` and
#: `indicator`, which is the whole reason its track was a severity rung.
#:
#: ONE ARM EACH, RESTORED ONE AT A TIME, because eleven tables moving in one
#: increment is eleven independent declarations and a teeth test that patched
#: them together would prove one thing about eleven. The two counts are the
#: measurement, not a boolean: a reader who changes one table can see from
#: this constant what it was worth.
#:
#: THE RULING THE ARMS ARE UNDER (orchestrator, 2026-09-06, on the operator's
#: delegation, decision **A**): THE BANK IS THE READING AND THE PANEL IS THE
#: METAL. corgi's segment bank is glass driven to a HEIGHT and all four of
#: its driven steps carry a meaning — `▁` info, `▄` warn, `▀` obligation,
#: `█` error and the danger form. The shade ramp and the quadrants are not
#: bars; they are milled aluminium, which is the register `Corgi.field_row`'s
#: docstring already named ("the two REGISTERS -- engraved aluminium against
#: driven glass"). A control is never drawn as a driven bar.
#:
#: AN EXEMPTION FOR THE WHOLE RAMP WAS MEASURED AND REFUSED, and the
#: measurement is in the frames rather than in an argument: `corgi_S2` drew
#: `██` as the error message's own leader (`██ expected YYYY-MM-DD`) three
#: rows under `██ ON ui`, a CHECKED checkbox, and `corgi_S3` drew `██` as the
#: slider's KNOB twelve rows above `▁▁█Delete all█▁▁`.
CORGI_BANK_BEFORE = (
    ("switch.main", None, 6, 0),
    ("switch.indicator", None, 8, 8),
    # inc67: the named-seat count on this row went 4 → 6. `knob` is the
    # SHARED table — the switch's grip and the SLIDER's — and `KNOB_SEATS`
    # gained `("slider", "knob")`, so one restored declaration now shows at
    # both. The two extra rows are `slider.knob` at `default` and `focused`,
    # which is `corgi_S3`'s own finding: this kit drew `██` as the slider's
    # KNOB twelve rows above `▁▁█Delete all█▁▁` and only the switch's half of
    # it was ever counted.
    ("knob", {LG.DEFAULT: "██", LG.FOCUSED: "▀▀", LG.EDITED: "▓▓",
              LG.ACTIVE: "▒▒", LG.INVALID: "░░", LG.DISABLED: "╳╳"}, 4, 6),
    ("checkbox.main", {LG.DEFAULT: "▁▁", LG.FOCUSED: "▔▔", LG.ACTIVE: "▂▂",
                       LG.DISABLED: "··"}, 2, 0),
    ("checkbox.knob", {LG.DEFAULT: "██", LG.FOCUSED: "▛▜", LG.ACTIVE: "▓▓",
                       LG.DISABLED: "▒▒"}, 2, 2),
    ("radio.main", {LG.DEFAULT: "▁◦", LG.FOCUSED: "▔◦", LG.ACTIVE: "▂◦",
                    LG.DISABLED: "·◦"}, 2, 0),
    ("radio.knob", {LG.DEFAULT: "▁●", LG.FOCUSED: "▔●", LG.ACTIVE: "▂●",
                    LG.DISABLED: "·◌"}, 2, 2),
    ("button.main", {LG.DEFAULT: "▁▁▁▁", LG.FOCUSED: "▔▔▔▔",
                     LG.ACTIVE: "▄▄▄▄", LG.DISABLED: "····"}, 2, 0),
    ("textfield.main", {LG.DEFAULT: "▁▁·▁▁", LG.FOCUSED: "▔▔·▔▔",
                        LG.EDITED: "▔▔▁▔▔", LG.ACTIVE: "▄▄·▄▄",
                        LG.INVALID: "░░·░░", LG.DISABLED: "·····"}, 2, 0),
    ("stepper.main", {LG.DEFAULT: "▁▁▁▁", LG.DISABLED: "····"}, 5, 0),
    ("stepper.step", {LG.DEFAULT: "▄▄▄▄", LG.FOCUSED: "▀▀▀▀",
                      LG.EDITED: "▓▓▓▓", LG.ACTIVE: "████",
                      LG.INVALID: "░░░░", LG.DISABLED: "╳╳╳╳"}, 3, 0),
)


def test_both_seat_laws_go_red_on_each_of_the_eleven_tables_inc58_moved(
        monkeypatch):
    """TEETH — and corgi needs them more than any language in the corpus,
    because it is the one whose roster entries were 38 and 16 and are now the
    two zeroes a reader is most likely to trust without looking.

    EACH ARM RESTORES ONE TABLE and asserts BOTH counts, so an arm cannot
    pass by moving the other law. The first two arms DELETE a key instead of
    restoring one, which is the defect in its original shape: corgi declared
    no `switch.main` and no `switch.indicator` at all, so the hardware toggle
    was drawn from the SLIDER's tables — `▁▁` and `▄▄`, `LEVELS["info"]` and
    `LEVELS["warn"]` — at six openers and eight named seats.

    THE OTHER TEN LANGUAGES ARE HELD STILL in every arm. A law that let corgi
    go red by moving somebody else would be a law about the reader, not about
    the kit."""
    def counts():
        return (len(meaning_marks_at_an_opener("corgi")),
                len(meaning_marks_at_named_seats("corgi")))

    assert counts() == (0, 0), meaning_marks_at_an_opener("corgi")

    for key, table, want_open, want_named in CORGI_BANK_BEFORE:
        glyphs = dict(LG.Corgi.PART_GLYPHS)
        if table is None:
            assert key in glyphs, (key, "inc58 declared it; the arm deletes it")
            del glyphs[key]
        else:
            assert glyphs[key] != table, (key, "already the pre-inc58 table")
            glyphs[key] = table
        monkeypatch.setattr(LG.Corgi, "PART_GLYPHS", glyphs)

        opened, named = counts()
        assert opened == want_open, (key, opened, want_open,
                                     meaning_marks_at_an_opener("corgi"))
        assert named == want_named, (key, named, want_named,
                                     meaning_marks_at_named_seats("corgi"))
        if want_open:
            with pytest.raises(AssertionError):
                test_no_control_opens_with_a_mark_that_means_something("corgi")
        if want_named:
            with pytest.raises(AssertionError):
                test_a_meaning_never_stands_at_a_disabled_or_indicator_seat(
                    "corgi")
        for other in LANGS:
            if other == "corgi":
                continue
            assert (len(meaning_marks_at_an_opener(other))
                    == MEANING_AT_AN_OPENER[other]), (key, other)
            assert (len(meaning_marks_at_named_seats(other))
                    == MEANING_AT_A_NAMED_SEAT[other]), (key, other)
        monkeypatch.undo()

    assert counts() == (0, 0)


def test_corgi_draws_no_control_as_a_driven_bar():
    """THE RULING ITSELF, and not just its two rosters.

    The seat laws ask about ONE cell — the opener, the knob, the indicator,
    the dead mark. This asks the ruling's whole sentence of every cell of
    every ruled control: **a control is never drawn as a driven bar.** The
    bar set is corgi's own segment bank, `▁▂▃▄▅▆▇█▀▔`, and it is written as
    the full Unicode run rather than as the four cells that happen to mean
    something today — the point of the ruling is that the BANK is the
    reading, so a control that reached for an undeclared step of it (`▃`,
    `▅`) would be reaching into the readings' register whether or not that
    step is spoken for yet.

    THE SLIDER, THE BAR AND THE SCROLL BAR ARE OUT, by name and with the
    cost declared. They are QUANTITY, and a quantity here is a reading: "the
    reading rides on segment HEIGHT, not on lit-vs-ghost" is this kit's own
    twice-cured defect, so `main`, `indicator` and `scrollbar.*` keep the
    bank. What that costs is measured in the census — corgi's
    "would collide if slider/bar/scrollbar were in the B set" line goes 1 to
    3 — and is `inc58.md` §4, not a silence.

    THE KNOB IS THE ONE PART DRAWN WITH QUADRANTS, asserted here rather than
    left to the eye, because it is inc46's "a knob drawn like the fill is not
    a knob" turned from a lesson into a structure."""
    k = LG.kit("corgi")
    bank = set("▁▂▃▄▅▆▇█▀▔")
    quadrants = set("▖▗▘▝▙▟▛▜")
    seen_quadrant_parts = set()
    for comp in RULED_CONTROLS:
        for part in LG.COMPONENT_PARTS[comp]:
            for st in LG.component_states(comp):
                glyph = k.part_glyph(part, st, comp)
                assert not (set(glyph) & bank), (comp, part, st, glyph,
                                                 "".join(sorted(set(glyph)
                                                                & bank)))
                if set(glyph) & quadrants:
                    seen_quadrant_parts.add(part)
    assert seen_quadrant_parts == {"knob", "main", "step"}, seen_quadrant_parts
    # ... and the tracks that keep the bank are the ones the ruling names.
    assert k.PART_GLYPHS["main"][LG.DEFAULT] == "▁▁", k.PART_GLYPHS["main"]
    assert k.PART_GLYPHS["indicator"][LG.DEFAULT] == "▄▄", "the slider's fill"
    assert k.part_key("switch", "main") == "switch.main"
    assert k.part_key("slider", "main") == "main"


# ===========================================================================
# inc59 (rework-5c) — prism's ember is read from the bottom
# ===========================================================================
#: THE TEN DECLARATIONS inc59 MOVED, in the same shape as `CORGI_BANK_BEFORE`
#: one screen up: `(key, the table HEAD carried, opener seats, named seats)`,
#: `None` for a key that DID NOT EXIST. prism declared no `switch.main` and
#: no `switch.indicator`, so its hardware toggle was drawn from the SLIDER's
#: tables — the off-track was `LEVELS["info"]`, the on-track was
#: `LEVELS["error"]` and the `DANGER_FORM`, the dead on-track was
#: `LEVELS["warn"]`.
#:
#: THE RULING (orchestrator, 2026-09-06, decision **A**): THE EMBER IS READ
#: FROM THE BOTTOM AND A CONTROL IS READ FROM THE TOP. prism's ramp is the
#: four dot-ROWS of a braille cell filling upward — `⣀` one row, `⣤` two,
#: `⣶` three, `⣿` the whole cell — and three of those plus the leading dot
#: `⡀` carry a meaning. No control draws a rung of that ramp; where a control
#: needs a field it draws the SAME dot-rows read from the TOP (`⠁ ⠉ ⠛ ⠿`),
#: the identical shape ladder at the opposite POSITION in the cell (ruling
#: D's third channel), stopping one row short of `⣿` by construction.
#:
#: IT IS THE KIT'S OWN KNOB RULE, WIDENED. `Prism.PART_GLYPHS["knob"]`
#: already said "every state is a BROKEN field ... precisely so the knob can
#: never be mistaken for a full cell of fire". That was true of one part and
#: false of every other, and `prism_S4` is what it cost: `⣿⣤ ⣿Delete⣿ ⣤⣿
#: ⣿⣀  Cancel  ⣀⣿` — the DANGER FORM and the safe button's WALL, the same
#: cell, eight columns apart on ONE ROW.
#:
#: `switch.main` IS WORTH ZERO ON BOTH ROSTERS AND MOVED ANYWAY, which is the
#: entry a reader should look at hardest. Its glyph is ONE cell, so the
#: opener law skips it (`len(glyph) < 2`), and `main` is a named seat only
#: when the control is dead. So `⣀` — `LEVELS["info"]` — was the off-track of
#: every prism switch and NO law in this file reached it. It moved under the
#: ruling, not under a roster, and this row is where that is written down.
PRISM_EMBER_BEFORE = (
    ("switch.main", None, 0, 0),
    ("switch.indicator", None, 0, 8),
    ("checkbox.main", {LG.DEFAULT: "⣿⣀⣿", LG.FOCUSED: "⣷⣀⣷",
                       LG.ACTIVE: "⣾⣀⣾", LG.DISABLED: "⠄⠄⠄"}, 2, 0),
    ("checkbox.knob", {LG.DEFAULT: "⣿⠀⣿", LG.FOCUSED: "⣷⠀⣷",
                       LG.ACTIVE: "⣾⠀⣾", LG.DISABLED: "⠄⠀⠄"}, 2, 2),
    ("radio.main", {LG.DEFAULT: "⣀⣀⣀", LG.FOCUSED: "⣤⣤⣤",
                    LG.ACTIVE: "⣶⣶⣶", LG.DISABLED: "⠄⠄⠄"}, 4, 0),
    ("radio.knob", {LG.DEFAULT: "⣀⣿⣀", LG.FOCUSED: "⣤⣿⣤",
                    LG.ACTIVE: "⣶⣿⣶", LG.DISABLED: "⠄⠁⠄"}, 4, 6),
    ("button.main", {LG.DEFAULT: "⣿⣀⣀⣿", LG.FOCUSED: "⣿⣤⣤⣿",
                     LG.ACTIVE: "⣿⣿⣿⣿", LG.DISABLED: "⠄⠄⠄⠄"}, 3, 0),
    ("textfield.main", {LG.DEFAULT: "⣿⠀⣿", LG.FOCUSED: "⣿⣀⣿",
                        LG.EDITED: "⣿⣤⣿", LG.ACTIVE: "⣿⣶⣿",
                        LG.INVALID: "⣹⠀⣏", LG.DISABLED: "⠄⠄⠄"}, 4, 0),
    ("stepper.main", {LG.DEFAULT: "⣀⣀", LG.DISABLED: "⠄⠄"}, 5, 0),
    ("stepper.step", {LG.DEFAULT: "⡀⢀", LG.FOCUSED: "⡄⢠", LG.EDITED: "⡆⢰",
                      LG.ACTIVE: "⣇⣸", LG.INVALID: "⣹⣹",
                      LG.DISABLED: "⠁⠈"}, 1, 0),
)


def test_both_seat_laws_go_red_on_each_of_the_ten_tables_inc59_moved(
        monkeypatch):
    """TEETH — the same shape inc58 used for corgi, because the same shape of
    defect was found in the same batch and two languages that failed for one
    reason should be watched failing the same way.

    THE COUNTS ARE CUMULATIVE, restored in declaration order, so each arm
    asserts the total after ITS table goes back. That is what makes the two
    zero-scoring arms legible rather than suspicious: `switch.main` scores
    nothing on either roster and `switch.indicator` scores nothing on the
    opener roster, because a one-cell glyph has no opener — and both were
    still drawing the severity ladder.

    THE OTHER TEN LANGUAGES ARE HELD STILL in every arm."""
    def counts():
        return (len(meaning_marks_at_an_opener("prism")),
                len(meaning_marks_at_named_seats("prism")))

    assert counts() == (0, 0), meaning_marks_at_an_opener("prism")

    glyphs = dict(LG.Prism.PART_GLYPHS)
    want_open = want_named = 0
    for key, table, d_open, d_named in PRISM_EMBER_BEFORE:
        if table is None:
            assert key in glyphs, (key, "inc59 declared it; the arm deletes it")
            del glyphs[key]
        else:
            assert glyphs[key] != table, (key, "already the pre-inc59 table")
            glyphs[key] = table
        monkeypatch.setattr(LG.Prism, "PART_GLYPHS", dict(glyphs))
        want_open += d_open
        want_named += d_named
        assert counts() == (want_open, want_named), (
            key, counts(), (want_open, want_named))
        for other in LANGS:
            if other == "prism":
                continue
            assert (len(meaning_marks_at_an_opener(other))
                    == MEANING_AT_AN_OPENER[other]), (key, other)
            assert (len(meaning_marks_at_named_seats(other))
                    == MEANING_AT_A_NAMED_SEAT[other]), (key, other)

    assert counts() == (25, 16), counts()
    with pytest.raises(AssertionError):
        test_no_control_opens_with_a_mark_that_means_something("prism")
    with pytest.raises(AssertionError):
        test_a_meaning_never_stands_at_a_disabled_or_indicator_seat("prism")
    monkeypatch.undo()
    assert counts() == (0, 0)


def test_prism_draws_no_control_on_the_embers_own_rungs():
    """THE RULING'S SENTENCE, over every cell of every ruled control.

    THE BAR SET IS THE WHOLE RAMP AND NOT THE THREE RUNGS THAT MEAN
    SOMETHING. `RAMP` is `⣀ ⣤ ⣶ ⣿` and `LEVELS` spends three of the four, so
    a control reaching for `⣶` — the step nothing means today — would be
    reaching into the readings' register anyway. That is the same widening
    `test_corgi_draws_no_control_as_a_driven_bar` makes for the block bank
    one increment earlier, and for the same reason: the ruling is about the
    REGISTER, not about today's bookkeeping.

    THE BAR IS OUT BY NAME AND THE SLIDER IS NOT, SINCE inc67. inc59 wrote
    all three out — "they are a QUANTITY, and this kit says a quantity IS the
    ember" — and named the cost in the census ("would collide if
    slider/bar/scrollbar were in the B set: 0 → 2"). K5 collected that cost:
    `prism_S3` row 16 drew nine cells of the error rung and the danger form
    four rows above `Delete all` set in the same cell, and ruling A's own
    condition is that an exemption leave a control's fill distinct from an
    error rung IN THE FRAME. A SLIDER IS A CONTROL by the registry fact that
    makes a toggle one (`GRIPS`: it has a knob; `COMPONENT_PARTS`: a switch is
    a slider whose range is boolean), so it takes the toggle's top-carved
    tables, and the pager's thumb follows its own shaft off the ember. The
    READBAR keeps it: no grip, nobody sets it, and it is
    `THE_METER_IS_THE_SEVERITY_DEVICE`'s second exempt seat.

    AND THE CHECKBOX'S LADDER NOW CLIMBS. Its walls ran `⣿` (8 dots) at rest,
    `⣷` (7) focused, `⣾` (7) active — a control that DIMMED when the reader
    arrived at it. Asserted in dot COUNTS, off the shipped declarations."""
    k = LG.kit("prism")
    ramp = set(k.RAMP)
    assert ramp == set("⣀⣤⣶⣿"), k.RAMP
    for comp in RULED_CONTROLS:
        for part in LG.COMPONENT_PARTS[comp]:
            for st in LG.component_states(comp):
                glyph = k.part_glyph(part, st, comp)
                assert not (set(glyph) & ramp), (
                    comp, part, st, glyph, "".join(sorted(set(glyph) & ramp)))
    # the two tables that keep the ember, and the scoping that lets them
    assert k.PART_GLYPHS["main"][LG.DEFAULT] == "⣀", "the readbar's floor"
    assert k.PART_GLYPHS["indicator"][LG.DEFAULT] == "⣿", "the readbar's fill"
    assert k.part_key("bar", "indicator") == "indicator"
    # and the three seats that left it in inc67, each scoped like the toggle
    assert k.part_key("switch", "indicator") == "switch.indicator"
    assert k.part_key("slider", "indicator") == "slider.indicator"
    assert (k.part_glyph("main", LG.DEFAULT, "slider"),
            k.part_glyph("indicator", LG.DEFAULT, "slider")) ==         (k.part_glyph("main", LG.DEFAULT, "switch"),
         k.part_glyph("indicator", LG.DEFAULT, "switch"))
    assert k.PART_GLYPHS["scrollbar.indicator"][LG.DEFAULT] == "⠿"
    assert not (set("⣀⣤⣶⣿") & set(
        "".join(k.PART_GLYPHS["slider.main"].values())
        + "".join(k.PART_GLYPHS["slider.indicator"].values())
        + "".join(k.PART_GLYPHS["scrollbar.indicator"].values()))),         "the slider and the pager are off the ember"

    def dots(g):
        return sum(bin(ord(ch) - 0x2800).count("1") for ch in g)

    walls = [k.part_glyph("main", st, "checkbox")[0]
             for st in (LG.DEFAULT, LG.FOCUSED, LG.ACTIVE)]
    assert dots(walls[0]) < dots(walls[1]), (walls, [dots(w) for w in walls])
    assert dots(walls[0]) < dots(walls[2]), (walls, [dots(w) for w in walls])


# ===========================================================================
# inc60 (rework-5c) — blueprint's terminators are chrome and nothing else
# ===========================================================================
#: THE TWO MEANINGS inc60 MOVED, and the five glyph tables that moved with
#: them. blueprint's defect was not one language reaching for chrome: it was
#: obligation standing ON the chrome and severity standing UNDER it, so the
#: fix had to move in both directions and the teeth have to show which half
#: did the work.
#:
#: THE RULING (orchestrator, 2026-09-06, decision **A**):
#:   (i)   THE TERMINATORS ARE CHROME AND NOTHING ELSE. `├ ┤` and their
#:         weight ramp fix where a run BEGINS and ENDS, and every control on
#:         the sheet is built from them, so no MEANING may be one. `REQUIRED`
#:         leaves `├` for a doubled RUN, `═`.
#:   (ii)  A MEANING IS A LINE TYPE, AND A DEAD THING IS NOT A MEANING.
#:         Severity is nothing / `╌╌` / `━━`; the dead runs are `┈` (a dead
#:         LEADER) and `┄` (a dead EXTENT), told from `╌` by dash COUNT.
#:   (iii) THE HATCH IS ONE MARK AT TWO DIRECTIONS. `╱` is HELD (LANGUAGES.md
#:         §11: "held work is HATCHED, never coloured"), `╲` is REFUSED —
#:         the drawing office's own opposite-direction convention for
#:         adjacent parts, and DIRECTION is one of ruling D's four.
#:
#: `LEVELS["info"]` IS THE ONE THAT DROPPED A MARK RATHER THAN MOVING IT, and
#: the brief asked for exactly that decision by name. `··` was the info rung
#: AND `LEAD`, the leader-origin dot this drawing rules every gap with — the
#: sheet's most-spent chrome cell, at the stepper's ground, the field's paper
#: and the switch's track. The sheet's own commitment decides which gives
#: way: **"alert is spent on OVERDUE and nothing else. A CALM SHEET CARRIES
#: ZERO ALERT."** A drawing office does not rule a line to say there is
#: nothing to note.
#: THE THREE HALVES AND WHAT EACH IS WORTH, measured rather than guessed —
#: `(opener, named)` AFTER each is restored, cumulative, and the first draft
#: of this constant had the first row as `(0, 0)` and was wrong. The five
#: tables alone are worth (1, 8): `╌` is STILL `LEVELS["warn"]` — inc60 moved
#: the DEAD RUNS off it, not the rung — so putting the dead datums back
#: lights the named-seat law without any meaning moving at all. `REQUIRED`
#: back on `├` is worth the six openers and the four knobs. `LEVELS["info"]`
#: back on `··` is worth the stepper's ground, five states of it, and nothing
#: on the named-seat roster.
#: inc72 TOOK IT TO `(0, 0)`, AND THAT IS THE MEASUREMENT OF THE INCREMENT.
#: The dead runs went back to `╌` — byte for byte the pre-inc60 spelling at
#: `main` and at `stepper.main` — and restoring the whole pre-inc60 table set
#: now lights NOTHING, where it lit `(1, 8)` before. The reason is the one
#: this comment already argued in the other direction: those seats scored
#: because `╌` was `LEVELS["warn"]`, and inc72 moved the warn rung to `" ━"`
#: instead of moving the chrome. **The same cells at the same seats are worth
#: eight rows or none depending on where one meaning sits**, which is the
#: whole of inc60's ruling (ii) stated as arithmetic.
BLUEPRINT_TABLES_WORTH = (0, 0)
#: inc67 MOVED THE FIRST OF THESE BY ONE, and the extra row is the point of
#: the increment rather than noise: restoring `REQUIRED = "├"` now also lights
#: `meter.open`, because blueprint's `dimension` mechanism opens its span with
#: the very terminator inc60 took obligation off — a seat no law in this file
#: could reach until the quantity widgets were declared. 7 → 8.
BLUEPRINT_SHEET_BEFORE = (
    # inc72: `(8, 12)` → `(7, 4)`. Both halves fell because the dead runs are
    # back on `╌` while the warn rung is not: the opener roster loses the seat
    # `╌` used to light on its own, and the named-seat roster loses the eight
    # rows `BLUEPRINT_TABLES_WORTH` above just recorded going to zero.
    ("REQUIRED", "├", (7, 4)),
    # inc67: the arms are CUMULATIVE, so `meter.open` is still lit from the
    # restored `REQUIRED`. The end point is UNCHANGED at `(13, 12)`: with both
    # meanings put back the sheet is exactly as bad as it was before inc60,
    # which is what an end point is for.
    ("LEVELS", {"info": "··", "warn": "╌╌", "error": "━━"}, (13, 12)),
)
BLUEPRINT_TABLES_BEFORE = (
    ("main", {LG.DEFAULT: "·", LG.DISABLED: "╌"}),
    ("checkbox.knob", {LG.DEFAULT: "├╪┤", LG.FOCUSED: "╞╪╡",
                       LG.ACTIVE: "┣╪┫", LG.DISABLED: "╎╌╎"}),
    ("radio.knob", {LG.DEFAULT: "┤○├", LG.FOCUSED: "╡◉╞", LG.ACTIVE: "┫●┣",
                    LG.DISABLED: "╏╌╏"}),
    ("textfield.main", {LG.DEFAULT: "├·┤", LG.FOCUSED: "╞·╡",
                        LG.EDITED: "╞╌╡", LG.ACTIVE: "┣·┫",
                        LG.INVALID: "╱·╱", LG.DISABLED: "╎╌╎"}),
    ("stepper.main", {LG.DEFAULT: "··", LG.DISABLED: "╌╌"}),
)


def test_both_seat_laws_go_red_on_the_two_meanings_inc60_moved(monkeypatch):
    """TEETH — and blueprint's are not the shape corgi's and prism's are,
    because blueprint's defect was in its MEANINGS as well as in its tables
    and the arms have to say which half did what.

    THE FIRST DRAFT OF `BLUEPRINT_TABLES_WORTH` WAS `(0, 0)` AND IT WAS
    WRONG, which is why the number is a constant here instead of a claim in a
    packet. The guess was that restoring the chrome alone would light
    nothing, because `├` is no longer the obligation mark — true — and
    because `╌` is no longer a severity rung — FALSE. inc60 left
    `LEVELS["warn"]` exactly where it was and moved the DEAD RUNS off it, so
    putting the dead datums back scored (1, 8) with no meaning restored at
    all. The measurement is the record.

    AND inc72 MADE THE FIRST DRAFT TRUE, by the move inc60 declined: the warn
    rung left `╌` and the dead runs came back to it, so the same restoration
    is worth `(0, 0)` again. The constant carries both readings and the reason
    each was right when it was taken."""
    def counts():
        return (len(meaning_marks_at_an_opener("blueprint")),
                len(meaning_marks_at_named_seats("blueprint")))

    assert counts() == (0, 0)

    glyphs = dict(LG.Blueprint.PART_GLYPHS)
    # inc72: TWO OF THE FIVE ARE NOW BYTE-IDENTICAL TO THE PRE-inc60 TABLE and
    # that is the finding, not a slip — the dead ground went back to `╌` once
    # the warn rung left it. The guard is kept and moved to the set: some of
    # these tables must still differ, or the arm below would be restoring
    # nothing at all.
    same = [key for key, table in BLUEPRINT_TABLES_BEFORE
            if glyphs[key] == table]
    assert same == ["main", "stepper.main"], same
    for key, table in BLUEPRINT_TABLES_BEFORE:
        glyphs[key] = table
    monkeypatch.setattr(LG.Blueprint, "PART_GLYPHS", glyphs)
    assert counts() == BLUEPRINT_TABLES_WORTH, (
        "the dead runs alone, with both meanings still moved", counts())

    for attr, value, want in BLUEPRINT_SHEET_BEFORE:
        assert getattr(LG.Blueprint, attr) != value, attr
        monkeypatch.setattr(LG.Blueprint, attr, value)
        assert counts() == want, (attr, counts(), want)
        for other in LANGS:
            if other == "blueprint":
                continue
            assert (len(meaning_marks_at_an_opener(other))
                    == MEANING_AT_AN_OPENER[other]), (attr, other)
            assert (len(meaning_marks_at_named_seats(other))
                    == MEANING_AT_A_NAMED_SEAT[other]), (attr, other)

    assert counts() == (13, 12), counts()
    with pytest.raises(AssertionError):
        test_no_control_opens_with_a_mark_that_means_something("blueprint")
    with pytest.raises(AssertionError):
        test_a_meaning_never_stands_at_a_disabled_or_indicator_seat(
            "blueprint")
    monkeypatch.undo()
    assert counts() == (0, 0)


def test_blueprints_refusal_is_the_held_hatch_turned_the_other_way():
    """RULING (iii), asserted at both ends.

    `Blueprint.icon` draws HELD as the hatch — "HELD is the HATCH itself, the
    one icon in this vocabulary that is a texture rather than a code" — and
    LANGUAGES.md §11 says the same ("held work is HATCHED, never coloured,
    `hatch='╱'`"). inc52 gave the SAME cell to the refused value, on the
    argument that it was "the one of the ten that states neither an extent
    nor a datum" — true, and it had missed that the icon was already there.

    BLOCKED AND REFUSED ARE TWO CLAIMS. The hatch stays one mark of the
    alphabet and spends the channel a drawing office already spends on it:
    adjacent hatched parts run in OPPOSITE DIRECTIONS. So `╱` is held and
    `╲` is refused, and all three declared invalid slots carry the turn.

    THE HELD MARK IS READ OFF THE KIT, not off a literal here, so a kit that
    moved its hatch and left the invalid channel behind goes red."""
    k = LG.kit("blueprint")
    held = "".join(k.icon(kind) for kind in ("blocked", "held"))
    assert "╱" in held and "╲" not in held, held

    inv = _invalid_marks(k)
    assert inv and set(inv) == {"╲"}, inv
    for key in ("knob", "textfield.main", "stepper.step"):
        assert "╱" not in k.PART_GLYPHS[key][LG.INVALID], key


def test_blueprint_says_nothing_when_there_is_nothing_to_note():
    """RULING (ii)'s DROPPED MARK, by name — the brief asked which meaning is
    dropped and why, so the answer is a law rather than a sentence in a
    packet.

    blueprint's info rung is AIR. Its own commitment is "alert is spent on
    OVERDUE and nothing else. A calm sheet carries zero alert", and `··` was
    also `LEAD`, the leader-origin dot that rules every gap on the sheet.
    One of the two had to give way and the cheaper one is the rung nobody
    needs to see.

    LEDGER IS THE PRECEDENT AND IT IS ASSERTED, not cited: a blank info rung
    already exists in this corpus and has since inc45, so the shape of the
    answer was available rather than invented. The other two rungs are still
    there, so the ladder did not collapse — it starts at nothing."""
    k = LG.kit("blueprint")
    assert k.LEVELS["info"].strip() == "", k.LEVELS
    assert k.LEVELS["warn"].strip() and k.LEVELS["error"].strip(), k.LEVELS
    assert LG.kit("ledger").LEVELS["info"].strip() == "", "the precedent"
    # ... and the cell it gave up is the one the sheet could not do without.
    assert k.LEAD == "·" and k.PART_GLYPHS["stepper.main"][LG.DEFAULT] == "··"
    assert "·" not in "".join(k.LEVELS.values())
    # ... and obligation is a RUN now, not a terminator.
    assert k.REQUIRED == "═" and k.REQUIRED not in (k.OPEN, k.CLOSE)


# ===========================================================================
# inc61 (rework-5c) — naught's lattice counts and its pixel charges
# ===========================================================================
#: WHAT THE GROUND EXEMPTION IS WORTH, ON THE SHIPPED KIT — `(opener, named)`
#: with `THE_GROUND_IS_NOT_A_MARK` emptied and nothing else touched.
#:
#: IT GREW BY FIVE SEATS INSIDE THIS INCREMENT AND THAT IS THE COST, PRINTED.
#: Before inc61 the exemption would have covered 2 openers (`button.main` and
#: `textfield.main`, both opening on `◦`). inc61 retired `·` (§ the ramp) and
#: `stepper.main`'s live rail could not take `⋅` — that is its DISABLED mark
#: — so the rail moved onto the UNLIT LATTICE, `◦◦`, and five more seats now
#: sit under the exemption. **Without it naught's opener roster would read 7,
#: worse than the 3 it carried before this increment**, and a reader who only
#: saw "3 → 0" would never learn that.
GROUND_EXEMPTION_IS_WORTH = (7, 2)

#: THE TWO DECLARATIONS inc61 MOVED IN naught, and what each is worth.
#: `switch.indicator` DID NOT EXIST — the toggle fell through to the SLIDER's
#: `indicator`, `NA.ON`, so its live track was the lit lattice dot at six
#: named seats. The composer draws that track TWO cells wide, so the frame
#: rendered `∙∙`, which is `LEVELS["error"]` and the `DANGER_FORM` byte for
#: byte.
NAUGHT_LATTICE_BEFORE = (
    ("switch.indicator", None, (0, 6)),
    # inc67: 10 → 11. `◉` is `PART_GLYPHS["knob"][DEFAULT]`, the SHARED knob
    # table, so restoring obligation onto it now lights the SLIDER's grip as
    # well as the switch's — `KNOB_SEATS` gained `("slider", "knob")`.
    ("REQUIRED", "◉", (1, 11)),
)


def test_the_seat_laws_go_red_on_the_two_declarations_inc61_moved(monkeypatch):
    """TEETH — the last of the eleven, and the arms are of two KINDS because
    the two defects were: a table that did not exist, and a meaning standing
    on a rung of the control ramp.

    THE ARMS ARE CUMULATIVE and the counts are asserted after each, so the
    six named seats the unscoped switch is worth are legible apart from the
    four the obligation mark is."""
    def counts():
        return (len(meaning_marks_at_an_opener("naught")),
                len(meaning_marks_at_named_seats("naught")))

    assert counts() == (0, 0)
    glyphs = dict(LG.Naught.PART_GLYPHS)
    for key, value, want in NAUGHT_LATTICE_BEFORE:
        if key in glyphs or value is None:
            assert key in glyphs, key
            del glyphs[key]
            monkeypatch.setattr(LG.Naught, "PART_GLYPHS", dict(glyphs))
        else:
            assert getattr(LG.Naught, key) != value, key
            monkeypatch.setattr(LG.Naught, key, value)
        assert counts() == want, (key, counts(), want)
        for other in LANGS:
            if other == "naught":
                continue
            assert (len(meaning_marks_at_an_opener(other))
                    == MEANING_AT_AN_OPENER[other]), (key, other)
            assert (len(meaning_marks_at_named_seats(other))
                    == MEANING_AT_A_NAMED_SEAT[other]), (key, other)

    with pytest.raises(AssertionError):
        test_no_control_opens_with_a_mark_that_means_something("naught")
    with pytest.raises(AssertionError):
        test_a_meaning_never_stands_at_a_disabled_or_indicator_seat("naught")
    monkeypatch.undo()
    assert counts() == (0, 0)


def test_the_ground_exemption_is_measured_and_not_a_silence(monkeypatch):
    """AN EXEMPTION NOBODY HAS PRICED IS A SILENCE WITH A NAME ON IT.

    `THE_GROUND_IS_NOT_A_MARK` is the second exemption in this file and the
    first one granted since inc45. This asks what it costs on the SHIPPED
    kit — empty the table, change nothing else, and read both rosters — and
    asserts the number, so a later increment that quietly leans more weight
    on it has to edit this line.

    IT ALREADY GREW ONCE, INSIDE THE INCREMENT THAT GRANTED IT. See
    `GROUND_EXEMPTION_IS_WORTH`: retiring `·` pushed `stepper.main`'s live
    rail onto `◦◦`, five seats, because `⋅` is that part's DISABLED mark.

    AND IT REACHES EXACTLY ONE LANGUAGE, asserted over all eleven: emptying
    it moves naught and nothing else."""
    before = {lang: (len(meaning_marks_at_an_opener(lang)),
                     len(meaning_marks_at_named_seats(lang)))
              for lang in LANGS}
    assert set(THE_GROUND_IS_NOT_A_MARK) == {"naught"}
    assert THE_GROUND_IS_NOT_A_MARK["naught"].strip()
    assert all(v == (0, 0) for v in before.values()), before

    # the table is this module's own global, so it is patched where the two
    # readers actually look it up rather than through an import path.
    monkeypatch.setitem(globals(), "THE_GROUND_IS_NOT_A_MARK", {})
    after = {lang: (len(meaning_marks_at_an_opener(lang)),
                    len(meaning_marks_at_named_seats(lang)))
             for lang in LANGS}
    assert after["naught"] == GROUND_EXEMPTION_IS_WORTH, after["naught"]
    assert all(after[l] == (0, 0) for l in LANGS if l != "naught"), after
    # ... and the cell it covers is DERIVED, so a kit that moves its unlit
    # pixel moves the exemption with it.
    assert LG.NA.OFF == "◦" and LG.NA.OFF in LG.kit("naught").LEVELS["info"]


def test_no_control_draws_naughts_lit_lattice_dot():
    """THE RULING'S SENTENCE: `NA.ON` belongs to the COUNT and to nothing
    else.

    naught reads the work by counting lit dots — `◦◦` none, `∙◦` one, `∙∙`
    two, LANGUAGES.md §0's "how many are lit is the signal" — and reads a
    control by how much of ONE pixel is charged. The two channels shared
    cells until this increment: the switch's live track was `NA.ON` and the
    composer draws it two cells wide, so `naught_S3` rendered `∙∙`, the error
    rung and the danger form byte for byte, on five rows.

    THE SLIDER AND THE BAR KEEP IT, by name and with the cost declared: "a
    quantity is a row of discrete LIT DOTS" is §0, so a quantity IS the
    count. They are outside the census's B set, so the cell produces no row —
    which is the same trade corgi (inc58) and prism (inc59) made."""
    k = LG.kit("naught")
    for comp in RULED_CONTROLS:
        for part in LG.COMPONENT_PARTS[comp]:
            for st in LG.component_states(comp):
                glyph = k.part_glyph(part, st, comp)
                assert LG.NA.ON not in glyph, (comp, part, st, glyph)
    assert k.PART_GLYPHS["indicator"][LG.DEFAULT] == LG.NA.ON, "the fill"
    assert k.part_key("switch", "indicator") == "switch.indicator"
    assert k.part_key("slider", "indicator") == "indicator"


def test_the_charge_ramp_retired_its_ambiguous_rung():
    """`·` IS GONE FROM naught, and the three reasons are asserted rather
    than recited.

    (1) It is the HOMOGLYPH of `NA.ON`, which carries the danger form and two
    severity rungs — `("·", "∙")` is in the census's own `HOMOGLYPHS` table,
    and ruling D forbids telling a MEANING from its CHROME that way.
    (2) LANGUAGES.md §0's pass-10 had already measured it: "`•` (U+2022), `·`
    (U+00B7) and `●` (U+25CF) measured and rejected".
    (3) It is East-Asian-Width AMBIGUOUS, and width safety is the property
    that pass chose the pixel pair for.

    THE LADDER IS STILL A LADDER. Five rungs, `⋅ ◦ ∙ ◉ ●`, and the two the
    retirement collapsed onto each other are asserted distinct at the one
    part where both appear."""
    import unicodedata as U
    k = LG.kit("naught")
    assert ("·", "∙") in HOMOGLYPHS or ("∙", "·") in HOMOGLYPHS
    assert U.east_asian_width("·") == "A"
    assert all(U.east_asian_width(c) == "N" for c in "⋅◦∙◉"), "the ramp"

    drawn = "".join(k.part_glyph(part, st, comp)
                    for comp in RULED_CONTROLS
                    for part in LG.COMPONENT_PARTS[comp]
                    for st in LG.component_states(comp))
    assert "·" not in drawn, sorted(set(drawn))
    step = k.PART_GLYPHS["stepper.main"]
    assert step[LG.DEFAULT] != step[LG.DISABLED], step


def test_ledger_does_not_bank_its_own_paper_up_by_size():
    """RULING D, applied to two STATES of one part rather than to a meaning
    against its chrome — which is the widening this increment had to decide.

    ledger's field papered its EDITED state by drawing the leader `·` one
    size larger, `∙`. The census read that as this language's one homoglyph
    row (the A side being the INVALID rune, which the test law excludes by
    name — so the row could only be closed from the CHROME side). Diameter
    alone is not a channel, and it does not become one because both drawings
    belong to the same part.

    EDITED TAKES THE RULE. `◆` was the first answer — this kit's own EDITED
    mark at the knob and at the stepper's step — and it is a ONE-CELL grip
    mark at a FIFTEEN-CELL seat: the field's paper is the whole measure, and
    a run of filled diamonds is a different claim from a grip that has been
    turned. So the space an entry goes in is a dot leader at rest and a SOLID
    RULE while it is being written, which is what a ledger does. The rule is
    read off `indicator[DEFAULT]`, the same stroke the bar's fill draws, so
    it is this kit's own mark rather than a literal chosen here."""
    k = LG.kit("ledger")
    edited = k.PART_GLYPHS["textfield.main"][LG.EDITED]
    rune = k.PART_GLYPHS["textfield.main"][LG.DEFAULT][1]
    assert rune == "·" and "∙" not in edited, (rune, edited)
    assert not (_twins(rune) & set(edited)), (rune, sorted(_twins(rune)), edited)
    rule = k.PART_GLYPHS["indicator"][LG.DEFAULT]
    assert rule in edited, (rule, edited)
    # ... and the rule carries no meaning anywhere in this kit.
    assert rule not in _seat_meanings(k, "ledger"), rule


# ===========================================================================
# inc51 (rework-4) — the stepper's own law, the one inc39 said it needed
# ===========================================================================
#: THE PAIRS THAT SAID "REJECTED" BY TURNING ROUND, and what each of them is
#: now. Six declarations, restored one at a time by the teeth below, so the
#: law is watched failing on the exact bytes HEAD carried before inc51.
#:
#: FIVE OF THE SIX ARE THEIR OWN DEFAULT EXCHANGED and go red on clause 1.
#: `nord`'s `][` is NOT: it is a turn of a pair the stepper never declares at
#: all — `[` and `]` are the BUTTON's walls and the CHECKBOX's well, which is
#: the census row `nord [ ] (4 each)` verbatim. It goes red on clause 2 only,
#: and that split is why the third column is here: a law with the orientation
#: clause alone would have left the BASE's own defect standing, which is the
#: defect spec §9.5 has been carrying since inc39.
STEP_TURNS = {
    "nord": ("][", "▚▚", False),     # `Kit`'s own, spec §9.5's unfixed flip
    "instrument": ("⢠⡄", "⠶⠶", True),
    "swiss": ("›‹", "╲╲", True),
    "industrial": ("><", "//", True),
    # inc59 moved this language's DEFAULT step off `⡀⢀` -- `⡀` is `REQUIRED`,
    # so a stepper at rest said the seat was compulsory -- and the turn this
    # arm restores is the turn of what the step reads TODAY. `⠠⠄` is `⠄⠠`
    # exchanged, the same defect inc51 found, respelt by inc59.
    "prism": ("⠠⠄", "⣹⣹", True),
    "blueprint": ("├┤", "━━", True),
}


def _halves(g: str) -> tuple[str, str]:
    """A step pair split where the kit splits it: the first half is the step
    BACK, the second the step FORWARD (`Kit.PART_GLYPHS`'s own words). Every
    declaration in the corpus is an even string, which `part_slots`' width
    reservation is what guarantees."""
    h = len(g) // 2
    return g[:h], g[h:]


def steps_that_are_another_state_turned_round(lang: str) -> list[tuple]:
    """Every pair of `stepper.step` states where one is the other with its
    halves EXCHANGED, as `(state, state, glyph, glyph)`.

    A pair whose halves are equal has no handedness and cannot violate the
    law — `corgi ████`, `solari ◆◆`, `darkside ØØ`. That exclusion is what
    keeps the law about ORIENTATION rather than about repetition."""
    k = LG.kit(lang)
    marks = {st: k.part_glyph("step", st, "stepper")
             for st in LG.component_states("stepper")}
    names = sorted(marks)
    out = []
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            back, fwd = _halves(marks[b])
            if back != fwd and marks[a] == fwd + back:
                out.append((a, b, marks[a], marks[b]))
    return out


def invalid_step_is_off_the_languages_own_refusal(lang: str) -> bool:
    """Whether `stepper.step[INVALID]` is drawn from the cells this language
    already spends on a refused VALUE — its INVALID knob, its INVALID field.

    The knob and the field are where a rejection is said in every one of the
    eleven, and both are declarations rather than fallbacks: this asks the
    tables directly so a language that declares no `INVALID` cannot pass by
    inheriting one."""
    k = LG.kit(lang)
    said = set()
    for key in ("knob", "textfield.main"):
        said |= set(k.PART_GLYPHS[key].get(LG.INVALID, ""))
    step = k.PART_GLYPHS[k.part_key("stepper", "step")][LG.INVALID]
    return bool(step) and set(step) <= (said - set(" ⠀"))


@pytest.mark.parametrize("lang", LANGS)
def test_a_steppers_halves_are_directions_and_invalid_is_not_a_turn(lang):
    """THE STEPPER'S LAW, and it is the one inc39 said out loud it was not
    writing.

    inc39 fixed four fields that spelled INVALID by EXCHANGING their two
    walls and declined to extend that law to the stepper, in these words:
    *"a stepper's halves are DIRECTIONS, not walls, so it needs its own
    law"* (spec §9.5). It has been the unwritten law of record ever since —
    §9.5, §11.5, inc48 §5 and `PROTOTYPE-inheritors-2.md` §5 K3 all name it —
    while `Kit.PART_GLYPHS["stepper.step"][INVALID]` sat at `][` and five
    other kits carried the same turn.

    THE LAW, in two clauses:

    1. **A step pair is two DIRECTIONS and no state is another state turned
       round.** `Kit`'s own declaration says what the two cells are: "the
       first half is the step BACK and the second half is the step FORWARD
       ... the cell's POSITION is what says which way it goes." A state
       spelled by exchanging another state's halves is a state spelled by
       ORIENTATION, and inc39's law already ruled that orientation is not a
       channel a reader can use. On a field the two marks sat 34 cells apart;
       on a stepper they TOUCH, so the reader is asked to compare two arrows
       side by side and remember which way they were before.
    2. **INVALID is said on the language's own refusal channel.** Whatever
       cells the kit spends on a rejected value at its knob and at its field
       are the cells its stepper spends. Five of the eleven already did it —
       `darkside ØØ`, `ledger ‡‡`, `solari ══`, `naught ◑◑`, `corgi ▀▄▄▀` —
       and inc51 moved the other six onto the same rule.

    WHY BOTH CLAUSES AND NOT JUST THE FIRST. Clause 1 alone is satisfiable by
    inventing any unused mark, which is how a kit acquires a cell nobody can
    read. Clause 2 says the mark must be one the reader has already met
    meaning exactly this, somewhere else in the same language."""
    assert not steps_that_are_another_state_turned_round(lang), (
        lang, steps_that_are_another_state_turned_round(lang))
    assert invalid_step_is_off_the_languages_own_refusal(lang), (
        lang, LG.kit(lang).PART_GLYPHS[
            LG.kit(lang).part_key("stepper", "step")][LG.INVALID])


def test_the_stepper_law_goes_red_on_the_six_turns_inc51_moved(monkeypatch):
    """TEETH — six arms, one per declaration, each restoring the exact byte
    string HEAD carried at `251511d` and each required to name the LANGUAGE
    and the TWO STATES the turn is between.

    `nord`'s arm is the base's: nord declares no `PART_GLYPHS`, so `][` was
    `Kit`'s line and patching `Kit` moves nord and nothing else — which the
    arm asserts by checking the other ten stay clean, the same proof inc39
    §9.3 q1 had to make by measurement.

    A seventh arm is the second clause's own teeth: an INVALID that is
    neither a turn nor drawn from the language's refusal — `≠≠`, a mark no
    kit declares — must still be red, because clause 1 alone would pass it."""
    for lang in LANGS:
        assert not steps_that_are_another_state_turned_round(lang), lang
        assert invalid_step_is_off_the_languages_own_refusal(lang), lang

    for lang, (turn, _fixed, is_a_turn) in STEP_TURNS.items():
        kit_cls = LG.Kit if lang == "nord" else type(LG.kit(lang))
        tbl = dict(kit_cls.PART_GLYPHS["stepper.step"])
        tbl[LG.INVALID] = turn
        monkeypatch.setitem(kit_cls.PART_GLYPHS, "stepper.step", tbl)
        hits = steps_that_are_another_state_turned_round(lang)
        if is_a_turn:
            assert hits, (lang, turn)
            assert all(LG.INVALID in (h[0], h[1]) for h in hits), (lang, hits)
            assert all(turn in (h[2], h[3]) for h in hits), (lang, hits)
        else:
            # nord: `][` turns a pair the stepper never declares, so clause 1
            # is silent and clause 2 is what fires. Asserted, not assumed.
            assert not hits, (lang, hits)
        assert not invalid_step_is_off_the_languages_own_refusal(lang), lang
        with pytest.raises(AssertionError):
            test_a_steppers_halves_are_directions_and_invalid_is_not_a_turn(
                lang)
        assert all(not steps_that_are_another_state_turned_round(o)
                   and invalid_step_is_off_the_languages_own_refusal(o)
                   for o in LANGS if o != lang), lang
        monkeypatch.undo()

    tbl = dict(LG.Darkside.PART_GLYPHS["stepper.step"])
    tbl[LG.INVALID] = "≠≠"
    monkeypatch.setitem(LG.Darkside.PART_GLYPHS, "stepper.step", tbl)
    assert not steps_that_are_another_state_turned_round("darkside")
    assert not invalid_step_is_off_the_languages_own_refusal("darkside")
    with pytest.raises(AssertionError):
        test_a_steppers_halves_are_directions_and_invalid_is_not_a_turn(
            "darkside")


# ---------------------------------------------------------------------------
# inc57 (rework-5b) - the marks a language draws OUTSIDE `PART_GLYPHS`
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("lang", LANGS)
def test_a_field_row_draws_exactly_the_leader_it_declares(lang):
    """THE DECLARATION IS LOAD-BEARING, over all eleven.

    `spec.md` §13.8, found by looking and not fixed for two batches:
    *"`field_row` is drawn outside `PART_GLYPHS` in all eleven, so the census
    can reach none of the eleven field leaders. Only darkside's was named by a
    ruling; ten others are unmeasured by any instrument here."* `FIELD_LEAD`
    is the fix, and a constant nothing checks is a comment — so this asserts
    that the cells the row DRAWS, once the caller's own words and air are
    taken out, are exactly the cells the kit DECLARES.

    THE CAPTION AND THE VALUE ARE SUBTRACTED IN EVERY CASE THIS FILE HAS.
    Four kits upper-case the caption, two lower-case it, so the words go out
    in all three registers rather than in the one they went in as — the
    alternative is a law that passes on nine languages and reports a `Z`.

    EMPTY IS ASSERTED TOO, and it is half the point. Four languages lead with
    AIR by commitment — the base's *"a column is found by ALIGNMENT rather
    than followed by a line"*, corgi's *"no leader, no right column"*, swiss's
    second column, industrial's bare register — and this law says they draw
    nothing rather than leaving it to be noticed."""
    k = LG.kit(lang)
    cap, val = "zzz", "qqq"
    words = set(cap + val + cap.upper() + val.upper()
                + cap.lower() + val.lower() + " ")
    drawn = set(plain(k.field_row(cap, val, 48))) - words
    assert drawn == set(k.FIELD_LEAD), (lang, drawn, k.FIELD_LEAD)


def test_the_census_reaches_every_mark_declared_outside_the_glyph_tables():
    """WHAT `DECLARED_MARKS` BUYS, asserted rather than described — and the
    darkside row is the evidence that the reader works.

    The census reads `PART_GLYPHS` and five meaning families. Two things a
    language DRAWS live outside both: the definition row's leader (all eleven)
    and darkside's identity marks (the moon doodle and the active tab). Until
    inc57 a meaning could stand at either seat and no instrument in this repo
    would say so — `spec.md` §12.7 found darkside's `(O)` by reading the
    source, which is exactly the method a census exists to replace.

    THE COUNTERFACTUAL IS THE TEETH. Put the OLD identity alphabet back and
    darkside goes from one colliding cell to three: `o` is `LEVELS["warn"]`
    and `O` is `LEVELS["error"]`, and both were the moon and the active tab.
    (`(.)` is a FULL STOP and `LEVELS["info"]` is a MIDDLE DOT, so the third
    rung never collided — two of three, said exactly.)"""
    import sys
    root = FRAMES.parents[1]
    for p in (root, root / "prototypes"):
        if str(p) not in sys.path:
            sys.path.insert(0, str(p))
    import collision_census as CC

    def colliding(lang):
        named, _ = CC.role_map(lang)
        return {c: sorted(f) for c, f in named.items() if CC.collides(f)}

    # every language's leader is reachable: it appears in the role map
    for lang in LANGS:
        named, _ = CC.role_map(lang)
        for cell in LG.kit(lang).FIELD_LEAD:
            assert "field" in named.get(cell, {}), (lang, cell)

    assert list(colliding("darkside")) == ["·"], colliding("darkside")

    old = ("( )", "(.)", "(o)", "(O)", "(o)", "(.)")
    saved = LG.Darkside.IDENT_GLYPHS
    try:
        LG.Darkside.IDENT_GLYPHS = old + ("(O)", "( )")
        was = colliding("darkside")
    finally:
        LG.Darkside.IDENT_GLYPHS = saved
    assert sorted(was) == ["O", "o", "·"], was
    assert "severity" in was["O"] and "identity" in was["O"], was["O"]
    assert "severity" in was["o"] and "identity" in was["o"], was["o"]


# ---------------------------------------------------------------------------
# inc63 (rework-6a) — E4: the exporter's ground is DECLARED, never inferred
# ---------------------------------------------------------------------------
#: `contrast(ink, ground)` per language, rounded, as the shipped kits measure
#: it. Written down rather than only bounded, because the floor below (4.5:1,
#: WCAG 1.4.3 for body text) is nowhere near any of these and a kit that
#: walked its ink halfway to its paper would still clear it. A number moving
#: in this table is a design change somebody has to look at.
GROUND_INK_CONTRAST = {
    "naught": 19.26, "corgi": 17.36, "instrument": 16.52, "swiss": 17.30,
    "industrial": 15.55, "nord": 10.84, "darkside": 19.26, "prism": 16.02,
    "ledger": 13.36, "solari": 16.81, "blueprint": 10.60,
}

#: Textual's own default screen ground. It is in this file for one reason: it
#: is the colour all 66 sheets shipped as their canvas until inc63, and the
#: teeth below reproduce that on real bytes.
_TEXTUAL_DEFAULT_GROUND = "#121212"

#: the sheet's own canvas — `svg_from_grid` writes it before any cell run, so
#: it is the one `<rect>` with no `x`/`y`.
_CANVAS_RECT = re.compile(
    r'<rect width="([0-9.]+)" height="([0-9.]+)" fill="(#[0-9a-fA-F]{6})"/>')
#: every other `<rect>`: one run of cells that carry a ground of their own.
_BG_RUN = re.compile(r'<rect x="[-0-9.]+" y="[-0-9.]+" width="([0-9.]+)" '
                     r'height="([0-9.]+)" fill="(#[0-9a-fA-F]{6})"/>')


def _luminance(hexcolour: str) -> float:
    """WCAG 2.x relative luminance. `L = 0.2126R + 0.7152G + 0.0722B` over
    linearised channels."""
    h = hexcolour.lstrip("#")
    ch = []
    for i in (0, 2, 4):
        v = int(h[i:i + 2], 16) / 255
        ch.append(v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4)
    return 0.2126 * ch[0] + 0.7152 * ch[1] + 0.0722 * ch[2]


def contrast(a: str, b: str) -> float:
    """`(L1 + 0.05) / (L2 + 0.05)`, lighter over darker."""
    la, lb = _luminance(a), _luminance(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def ground_report(svg: str) -> tuple[str, dict[str, float]]:
    """`(the canvas colour, the area each ground colour actually shows)`.

    Area in square units of the picture's own coordinate space, not in cells:
    the cell width is the exporter's business and this reader has no opinion
    about it. The canvas's share is what is LEFT after every run is subtracted
    — which is the only way to ask "is the declared ground the ground you can
    see", as opposed to "is it the string in the first rect"."""
    m = _CANVAS_RECT.search(svg)
    assert m, svg[:200]
    canvas = m.group(3)
    over: dict[str, float] = {}
    for w, h, fill in _BG_RUN.findall(svg):
        over[fill] = over.get(fill, 0.0) + float(w) * float(h)
    left = float(m.group(1)) * float(m.group(2)) - sum(over.values())
    return canvas, {canvas: left, **over}


@pytest.mark.parametrize("lang", LANGS)
def test_the_svg_canvas_is_the_kits_declared_ground(lang):
    """THE GROUND IS DECLARED, AND IT IS THE GROUND YOU CAN SEE.

    Ruling E4 (orchestrator, 2026-09-07): *the exporter reads the kit's
    declared `ground` and `ink`; it never infers them from frequency.*

    WHAT WAS WRONG. `cell_grid()` took "the most common background in the
    frame" for the ground, and `render.py` assigned the screen's background
    AFTER the first paint — too late for strips the compositor had already
    cached. So every cell of all 66 sheets arrived on Textual's `#121212`, the
    exporter agreed with the mistake by counting it, and no rect was written
    over it. On ten dark languages that was luck. On ledger, the corpus's only
    light-paper kit (`ground #e9e1cf`, `ink #1c1a15`), it shipped six sheets
    of black ink on a black canvas: **1.08:1**, with the dot leaders
    (`#c4b99f`, 9.62:1) the only legible thing on the page and the hierarchy
    therefore exactly inverted.

    THREE CLAUSES, AND THE THIRD IS WHY THE FIRST IS NOT VACUOUS. A canvas can
    carry the right string and still be invisible under a full-bleed repaint,
    so the law also asks which colour has the largest area LEFT once every run
    is subtracted. `prism_S4` paints 48.8% of its picture and is legal;
    `industrial_S1` paints 28.3%. A sheet where a foreign colour outweighed
    the declared ground would be the pre-inc63 state written a second way, and
    the teeth below do exactly that to a shipped file."""
    k = LG.kit(lang)
    ground, ink = k.t["ground"], k.c["ink"]
    assert round(contrast(ink, ground), 2) == GROUND_INK_CONTRAST[lang], \
        (lang, contrast(ink, ground))
    assert contrast(ink, ground) >= 4.5, (lang, ground, ink)
    for screen in SCREENS:
        svg = (FRAMES / f"{lang}_{screen}.svg").read_text(encoding="utf-8")
        canvas, area = ground_report(svg)
        assert canvas == ground, (lang, screen, canvas, ground)
        widest = max(area, key=area.get)
        assert widest == ground, (lang, screen, widest, area)


def test_the_declared_ground_law_bites_on_the_defect_it_was_written_for():
    """Watched failing on REAL BYTES, both clauses, two ways.

    Not a monkeypatch and not a hand-built picture: `ledger_S6.svg` as it
    ships, edited the two ways the defect actually presented.

    (a) THE CANVAS TAKES TEXTUAL'S GROUND — what every one of the 66 shipped
    until inc63. One substitution on the canvas rect, and the contrast clause
    reads 1.08:1.

    (b) THE CANVAS IS RIGHT AND SOMETHING FULL-BLEED SITS ON IT — the shape a
    naive fix takes if the exporter is taught the declared ground while the
    cells still arrive on `#121212`: every clause about the first rect passes
    and the picture is unchanged. The area clause is what catches it."""
    k = LG.kit("ledger")
    svg = (FRAMES / "ledger_S6.svg").read_text(encoding="utf-8")
    canvas, area = ground_report(svg)
    assert canvas == k.t["ground"] and max(area, key=area.get) == canvas

    stale = svg.replace(f'fill="{canvas}"/>',
                        f'fill="{_TEXTUAL_DEFAULT_GROUND}"/>', 1)
    assert ground_report(stale)[0] == _TEXTUAL_DEFAULT_GROUND
    assert round(contrast(k.c["ink"], _TEXTUAL_DEFAULT_GROUND), 2) == 1.08
    assert contrast(k.c["ink"], _TEXTUAL_DEFAULT_GROUND) < 4.5

    m = _CANVAS_RECT.search(svg)
    covered = svg.replace(
        "<g font-family",
        f'<rect x="0.0" y="0.0" width="{m.group(1)}" height="{m.group(2)}" '
        f'fill="{_TEXTUAL_DEFAULT_GROUND}"/>\n<g font-family', 1)
    seen, spread = ground_report(covered)
    assert seen == k.t["ground"], "clause one still passes -- that is the point"
    assert max(spread, key=spread.get) == _TEXTUAL_DEFAULT_GROUND, spread



# ---------------------------------------------------------------------------
# inc73 (rework-7a) — K6, K7's `alert` clause, the match tier, and the role
# ruling. Every painted run in the 66 sheets, against the ground UNDER IT.
# ---------------------------------------------------------------------------
#: WHERE A CHARACTER'S BASELINE SITS RELATIVE TO ITS ROW'S BACKGROUND RECT.
#: `svg_from_grid` writes a row's rects at `ry = PAD + y*LH` and its text at
#: `ty = ry + 0.78*LH`, so a text run and the rect under it are one
#: subtraction apart.
#:
#: DECLARED HERE AND CHECKED AGAINST THE EXPORTER'S SOURCE, rather than
#: imported: `prototypes/capture_languages.py` pulls in Textual and this file
#: reads the pictures as bytes on purpose (`FRAMES` is a path and not an
#: import, for the same reason `render.py` is not imported either). The check
#: below is what stops the two drifting.
_CW, _LH, _PAD, _BASE_FRAC = 8.4, 17.0, 10.0, 0.78
_BASE = _LH * _BASE_FRAC


def test_this_files_picture_metrics_are_the_exporters():
    """The reader below attributes a character to a rect by COORDINATE, so it
    is wrong the moment the exporter's cell box changes. Read off the
    exporter's source rather than trusted."""
    src = (FRAMES.parent / "capture_languages.py").read_text(encoding="utf-8")
    assert f"CW, LH, FS, PAD = {_CW}, {_LH}, 14.0, {_PAD}" in src, "metrics"
    assert "ry = PAD + y * LH" in src, "row origin"
    assert f"ty = ry + {_BASE_FRAC} * LH" in src, "baseline"

_TEXT_RUN = re.compile(
    r'<text x="([0-9.]+)" y="([0-9.]+)" fill="(#[0-9a-fA-F]{6})"'
    r'([^>]*)>(.*?)</text>')
_RECT_RUN = re.compile(
    r'<rect x="([-0-9.]+)" y="([-0-9.]+)" width="([0-9.]+)" '
    r'height="([0-9.]+)" fill="(#[0-9a-fA-F]{6})"/>')


def _unescape(s: str) -> str:
    for a, b in (("&lt;", "<"), ("&gt;", ">"), ("&quot;", '"'),
                 ("&#39;", "'"), ("&amp;", "&")):
        s = s.replace(a, b)
    return s


def painted_runs(svg: str):
    """`(ink, ground, text, bold, underline)` for every painted stretch.

    THE GROUND IS THE ONE UNDER THE RUN, not the canvas — which is K6 in one
    sentence and the thing inc70's law could not ask. A `<text>` element is
    split wherever the rect beneath it changes, so a run that starts on the
    page and ends on a plate is returned as two runs with two grounds.
    Attribution is by COORDINATE, cell by cell: the character's own centre
    against the rect's span. Round four's §8.3 is why it is per character and
    not per run — its first pass attributed whole runs to two-cell plates and
    produced two contrasts of 1.00:1 and 1.03:1 that were the measurer's
    artefacts and not the picture's.

    Blank stretches are dropped: a run of spaces has an ink colour and no ink.
    """
    canvas = _CANVAS_RECT.search(svg).group(3)
    rows: dict[int, list] = {}
    for x, y, w, h, fill in _RECT_RUN.findall(svg):
        r = round((float(y) - _PAD) / _LH)
        rows.setdefault(r, []).append((float(x), float(x) + float(w), fill))
    out = []
    for x, y, fill, attrs, body in _TEXT_RUN.findall(svg):
        r = round((float(y) - _BASE - _PAD) / _LH)
        bold, und = "bold" in attrs, "underline" in attrs
        cur, buf = None, ""
        for i, ch in enumerate(_unescape(body)):
            cx = float(x) + (i + 0.5) * _CW
            bg = canvas
            for x0, x1, rf in rows.get(r, ()):
                if x0 - 0.01 <= cx <= x1 + 0.01:
                    bg = rf
                    break
            if bg != cur:
                if buf.strip():
                    out.append((fill, cur, buf, bold, und))
                cur, buf = bg, ""
            buf += ch
        if buf.strip():
            out.append((fill, cur, buf, bold, und))
    return out


#: WHAT EACH TIER OWES THE GROUND IT IS PAINTED ON. `ink` and `mut` are text
#: (WCAG 1.4.3); `alert` says "this is wrong" and is asked the same, because a
#: warning nobody can read is not a warning; `focus` is a non-text component
#: boundary (1.4.11).
#:
#: THE RULING (orchestrator, 2026-09-07, K6): *contrast is measured against
#: the background actually under the run (the second grounds: selection bands,
#: plates, match rects), not only the canvas. `ink` and `mut` >= 4.5:1 against
#: every ground they are painted on; `focus` >= 3:1.*
#: And K7's second half: *`alert` >= 4.5:1 against every ground it is painted
#: on, all eleven.*
#:
#: `dim` IS NOT HERE. K7's first half asks it only where it CLASSIFIES, and
#: that is a seat-by-seat table — inc74's, not this law's.
TIER_FLOOR = {"ink": 4.5, "mut": 4.5, "alert": 4.5, "focus": 3.0}


def runs_under_floor(lang: str) -> list[tuple]:
    """Every painted run of a floored tier that misses its floor, over the six
    sheets. `(screen, tier, ratio, ground, text)`."""
    t = LG.THEMES[lang]
    by_hex: dict[str, list[str]] = {}
    for tier in TIER_FLOOR:
        v = t.get(tier)
        if isinstance(v, str) and v.startswith("#"):
            by_hex.setdefault(v, []).append(tier)
    bad = []
    for screen in SCREENS:
        svg = (FRAMES / f"{lang}_{screen}.svg").read_text(encoding="utf-8")
        for ink, ground, text, _b, _u in painted_runs(svg):
            for tier in by_hex.get(ink, ()):
                c = contrast(ink, ground)
                if c < TIER_FLOOR[tier]:
                    bad.append((screen, tier, round(c, 2), ground,
                                text.strip()[:24]))
    return bad


@pytest.mark.parametrize("lang", LANGS)
def test_every_painted_run_clears_its_tiers_floor_on_its_own_ground(lang):
    """K6, over all 66 sheets, cell by cell.

    inc70 asked `contrast(token, THEMES[lang]["ground"])` — one number per
    kit, against the CANVAS. Five kits paint a second ground and round four
    measured what that hid: ledger's `mut` at 4.10:1 on its band, industrial's
    at 4.20:1 on its plate, industrial's `focus` at 1.28:1 and its `alert` at
    4.06:1. A floor cleared by the smallest possible step against one ground
    breaks against the first rect somebody paints under it, which is §7.2 of
    that round, and this law is the answer to it.

    THE EXEMPTION IS THE ONE ALREADY WRITTEN. solari's `mut` sits under the
    floor against its own canvas by an impossibility proof
    (`THE_BAND_IS_A_SECOND_GROUND`), so it cannot clear it against anything;
    the exemption is asserted to be non-empty and real rather than assumed."""
    bad = runs_under_floor(lang)
    if lang in THE_BAND_IS_A_SECOND_GROUND:
        assert THE_BAND_IS_A_SECOND_GROUND[lang].strip(), lang
        assert bad and {b[1] for b in bad} == {"mut"}, (lang, bad[:4])
        return
    assert bad == [], (lang, bad[:6])


def test_the_second_ground_law_bites_on_the_four_runs_round_four_measured(
        monkeypatch):
    """TEETH, on the REAL hexes, one kit at a time — and each arm names the
    run round four found and the ground it found it on.

    THE ARM THAT MATTERS MOST IS industrial's `mut`: `#8f8f8f` cleared 5.38:1
    against the canvas and the OLD law was green on it for two batches. It is
    the plate that catches it, which is the whole of K6."""
    for lang in LANGS:
        test_every_painted_run_clears_its_tiers_floor_on_its_own_ground(lang)

    before = {
        "industrial": [("mut", "#8f8f8f", "#2e2e2e", 4.20),
                       ("alert", "#ff4b1f", "#2e2e2e", 4.06)],
        "ledger": [("mut", "#6a6458", "#e0d7c2", 4.10)],
        "nord": [("alert", "#bf616a", "#2e3440", 3.05)],
        "corgi": [("alert", "#d92b1a", "#0d0d0d", 3.99)],
        "naught": [("alert", "#d71921", "#000000", 4.05)],
        "swiss": [("alert", "#e2231a", "#101010", 4.07)],
    }
    for lang, rows in before.items():
        for tier, hexes, ground, ratio in rows:
            # the arithmetic first, so a wrong constant fails here and not in
            # a picture nobody re-rendered
            assert round(contrast(hexes, ground), 2) == ratio, (lang, tier)
            assert contrast(hexes, ground) < TIER_FLOOR[tier], (lang, tier)
            assert LG.THEMES[lang][tier] != hexes, (lang, tier, "already old")
            assert contrast(LG.THEMES[lang][tier], ground) >= TIER_FLOOR[tier]


#: WHICH CHANNEL EACH KIT DECLARES ITS MATCH ON, derived from `MATCH_STYLE`
#: rather than typed: the STYLE word gives `bold` / `underline` / `reverse`,
#: and the TOKEN gives whether the mark is a hue of its own or the kit's own
#: ink at another weight.
#:
#: THE RULING (orchestrator, 2026-09-07), and it REPLACES the "match ink >= 3:1
#: against `mut` and against `ink`" clause, which is unsatisfiable. The
#: arithmetic that retired it, because a clause withdrawn without its reason
#: comes back:
#:
#:     contrast(ink, ground) == contrast(ink, mut) * contrast(mut, ground)
#:
#: exactly, for any three colours ordered by luminance (every term is a ratio
#: of `L + 0.05`). A match ink 3:1 from BOTH `mut` and `ink` forces
#: `contrast(ink, mut) >= 9`, and with K6's `mut >= 4.5` that forces
#: `contrast(ink, ground) >= 40.5`. **The physical maximum is 21:1**, white on
#: black. No kit could satisfy it at any token value; the corpus's best
#: `ink/mut` headroom, with `mut` sitting exactly on the K6 floor, is
#: darkside's 4.28.
#:
#: SO THE TWO THINGS A MATCH OWES ARE MEASURED ON DIFFERENT CHANNELS:
#:   (a) LEGIBLE — the match ink >= 4.5:1 against the ground it is actually
#:       painted on. For `reverse` that ground is the SWAPPED rect.
#:   (b) DISTINCT — by the channel the kit declares:
#:         weight / decoration   the svg run carries `font-weight` /
#:                               `text-decoration`. A structural assertion and
#:                               no luminance clause: 1.00:1 against `ink` is
#:                               CORRECT for a kit whose match is its own ink
#:                               made bold (operator ruling 9 — the emphasis
#:                               may not add a cell).
#:         reverse               a rect exists under exactly the match cells.
#:         hue                   the accent's hue angle differs from `mut`'s
#:                               and `ink`'s by >= 30 degrees in HLS; or, where
#:                               the kit's body and ink are ACHROMATIC and hue
#:                               distance is undefined, the accent differs from
#:                               `mut` by >= 1.5:1 in luminance.
#:
#: THE BRANCHES, AS MEASURED (inc73):
#:   weight      blueprint 10.60 · naught 19.26 · corgi 17.36
#:   decoration  ledger 13.36
#:   reverse     industrial 5.79 · darkside 4.56 · solari 16.81
#:   hue         instrument 10.45 (38.7 / 37.5) · nord 5.99 (40.0 / 38.8) ·
#:               prism 10.17 (37.5 / 35.2)
#:   hue, achromatic comparands   swiss 4.52 (1.52:1 against `mut`)
MATCH_LEGIBLE = 4.5
MATCH_HUE_DEGREES = 30.0
MATCH_ACHROMATIC_RATIO = 1.5
#: HLS saturation below which a colour has no hue to be distant from.
ACHROMATIC = 0.10


def _hls(hexcolour: str):
    h = hexcolour.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return colorsys.rgb_to_hls(r, g, b)


def hue_gap(a: str, b: str) -> float:
    """Degrees between two hue angles, the short way round."""
    d = abs(_hls(a)[0] * 360 - _hls(b)[0] * 360) % 360
    return min(d, 360 - d)


def match_branch(lang: str) -> tuple[str, str, str]:
    """`(branch, the match ink, the ground it is painted on)`."""
    k, t = LG.kit(lang), LG.THEMES[lang]
    style = k.MATCH_STYLE
    word, token = style.split()[0], style.strip().split()[-1].strip("{}")
    value = t.get(token, t["ink"])
    if word == "reverse":
        return "reverse", t["ground"], value
    if token in ("accent", "alert") and value != t["ink"]:
        return "hue", value, t["ground"]
    return word, value, t["ground"]


@pytest.mark.parametrize("lang", LANGS)
def test_the_match_run_is_legible_and_distinct_on_its_declared_channel(lang):
    """THE MATCH TIER, on the two things a match owes and no others.

    S6 is the screen with the colour taken away — six results and the word a
    reader searched for inside them — so this is the one tier whose whole job
    is to be found. See `MATCH_LEGIBLE` above for the arithmetic that retired
    the clause this replaces."""
    branch, ink, ground = match_branch(lang)
    t = LG.THEMES[lang]

    # (a) LEGIBLE, on the ground it is really painted on
    assert contrast(ink, ground) >= MATCH_LEGIBLE, \
        (lang, branch, ink, ground, round(contrast(ink, ground), 2))

    # (b) DISTINCT, on the channel the kit declares
    if branch in ("bold", "underline"):
        attr = "font-weight" if branch == "bold" else "text-decoration"
        svg = (FRAMES / f"{lang}_S6.svg").read_text(encoding="utf-8")
        styled = [r for r in painted_runs(svg)
                  if (r[3] if branch == "bold" else r[4])]
        assert styled, (lang, branch, "no styled run in the sheet")
        assert attr in svg, (lang, attr)
        # and the styled runs are the MATCH ink, not some other emphasis
        assert {r[0] for r in styled} == {ink}, (lang, {r[0] for r in styled})
    elif branch == "reverse":
        svg = (FRAMES / f"{lang}_S6.svg").read_text(encoding="utf-8")
        rects = [f for _x, _y, _w, _h, f in _RECT_RUN.findall(svg)]
        assert ground in rects, (lang, ground, sorted(set(rects)))
        knocked = [r for r in painted_runs(svg) if r[1] == ground]
        assert knocked, (lang, "a reverse match with no run on its own rect")
        assert {r[0] for r in knocked} == {ink}, (lang, {r[0] for r in knocked})
    else:
        assert branch == "hue", (lang, branch)
        pale = [k_ for k_ in ("mut", "ink") if _hls(t[k_])[2] < ACHROMATIC]
        if len(pale) == 2:
            # hue distance from a grey is not a quantity; the fallback clause
            got = contrast(ink, t["mut"])
            assert got >= MATCH_ACHROMATIC_RATIO, (lang, round(got, 2))
        else:
            assert not pale, (lang, "one of the two is grey and one is not "
                                    "-- the ruling has no branch for that")
            for other in ("mut", "ink"):
                gap = hue_gap(ink, t[other])
                assert gap >= MATCH_HUE_DEGREES, (lang, other, round(gap, 1))


def test_the_match_tier_law_bites_on_the_two_declarations_inc73_moved(
        monkeypatch):
    """TEETH, and the two arms are the two branches that actually failed.

    nord's accent was `#88c0d0`, hue 193.3 against a body at 218.7 — 25.4
    degrees, under the ruling's 30, in the kit round three called *"the
    baseline the other ten chose against"* and round four called the worst
    regression of the corpus. swiss's `alert` was `#e2231a` at 4.07:1, so it
    failed the LEGIBILITY clause, and its `mut` was `#8a8a8a`, so it also
    failed the achromatic fallback at 1.36:1 — two clauses, two tokens, and
    the arm restores them one at a time."""
    for lang in LANGS:
        test_the_match_run_is_legible_and_distinct_on_its_declared_channel(lang)

    t = dict(LG.THEMES["nord"])
    assert t["accent"] != "#88c0d0"
    assert round(hue_gap("#88c0d0", t["mut"]), 1) == 25.4
    t["accent"] = "#88c0d0"
    monkeypatch.setitem(LG.THEMES, "nord", t)
    with pytest.raises(AssertionError):
        test_the_match_run_is_legible_and_distinct_on_its_declared_channel(
            "nord")
    monkeypatch.undo()

    for token, hexes in (("alert", "#e2231a"), ("mut", "#8a8a8a")):
        t = dict(LG.THEMES["swiss"])
        assert t[token] != hexes, token
        t[token] = hexes
        monkeypatch.setitem(LG.THEMES, "swiss", t)
        with pytest.raises(AssertionError):
            test_the_match_run_is_legible_and_distinct_on_its_declared_channel(
                "swiss")
        monkeypatch.undo()

    for lang in LANGS:
        test_the_match_run_is_legible_and_distinct_on_its_declared_channel(lang)


#: A TOKEN HAS EXACTLY ONE ROLE.
#:
#: THE RULING (orchestrator, 2026-09-07): *a token has exactly one role.
#: Ground-role tokens (ground, band, plate, match rect) and ink-role tokens
#: (ink, mut, dim, focus, alert, accent) are disjoint sets in `THEMES`,
#: asserted by a test over all eleven.*
#:
#: WHAT IT WAS WRITTEN FOR. industrial declared `plate = "#2e2e2e"` and
#: `focus = "#2e2e2e"`, and `Industrial.keyhint` painted the key plate's WALLS
#: in `self.plate` — so one hex was a rect's fill in sixteen places and a
#: glyph's colour in eight, and as a glyph it stood at **1.28:1**. No floor
#: could have caught it: the value is CORRECT as a ground and wrong as ink,
#: and a law that asks "does this token clear 3:1" cannot tell which it is.
#:
#: THE OTHER TEN WERE CHECKED AND ARE CLEAN — one clash in eleven kits, and it
#: is the one the ruling names. solari's second ground already had a name
#: (`flap`, and `band = "reverse"` is a style word rather than a colour);
#: darkside's grey steps are `dim`/`rail` at one hex, both INK-role, which is
#: an alias and not a double role.
GROUND_ROLE = ("ground", "panel", "band", "plate", "flap")
INK_ROLE = ("ink", "mut", "dim", "focus", "alert", "accent")


@pytest.mark.parametrize("lang", LANGS)
def test_a_token_has_exactly_one_role(lang):
    """The role ruling, over `THEMES`, all eleven.

    ASKED OF THE VALUES AND NOT OF THE NAMES, because that is where the defect
    lived: `plate` and `focus` were two names for one hex and only one of them
    could be right about what the colour was for.

    `reverse` IS NOT A SECOND GROUND TOKEN, said here so the exclusion is
    deliberate. Three kits spell `MATCH_STYLE` as `reverse {token}`, which
    SWAPS a run's declared pair at composition time (`cell_grid`, inc43) — the
    rect is the run's own ink turned inside out for the length of a match, not
    a colour the theme names twice. The match-tier law's `reverse` branch is
    what asserts that rect exists.

    AND THE INK SET IS THE ONE A KIT PAINTS WITH: `Kit.__init__` builds
    `self.c` from exactly these six keys, so the two cannot drift."""
    t = LG.THEMES[lang]
    grounds = {k: t[k] for k in GROUND_ROLE
               if isinstance(t.get(k), str) and t[k].startswith("#")}
    inks = {k: t[k] for k in INK_ROLE
            if isinstance(t.get(k), str) and t[k].startswith("#")}
    assert grounds and inks, (lang, sorted(grounds), sorted(inks))
    clash = [(g, i, v) for g, v in grounds.items()
             for i, w in inks.items() if v == w]
    assert clash == [], (lang, clash)
    # the ink set and what the kit paints with are one list
    assert set(LG.kit(lang).c) == set(INK_ROLE) | {"warn"}, \
        (lang, sorted(LG.kit(lang).c))


def test_the_role_law_bites_on_the_declaration_industrial_shipped(monkeypatch):
    """TEETH, on the real hex, plus the reading that makes it matter: with the
    old value restored, `focus` painted as ink stands at 1.28:1 on this kit's
    ground — which no floor law caught for the life of the token, because
    `#2e2e2e` was never asked whether it was ink."""
    for lang in LANGS:
        test_a_token_has_exactly_one_role(lang)
    t = dict(LG.THEMES["industrial"])
    assert t["focus"] != t["plate"] == "#2e2e2e"
    assert round(contrast("#2e2e2e", t["ground"]), 2) == 1.28
    t["focus"] = "#2e2e2e"
    monkeypatch.setitem(LG.THEMES, "industrial", t)
    with pytest.raises(AssertionError):
        test_a_token_has_exactly_one_role("industrial")
    for other in LANGS:
        if other != "industrial":
            test_a_token_has_exactly_one_role(other)
    monkeypatch.undo()
    for lang in LANGS:
        test_a_token_has_exactly_one_role(lang)


# ---------------------------------------------------------------------------
# inc74 (rework-7a) — K7's `dim` clause and L7. Which `dim` runs CLASSIFY.
# ---------------------------------------------------------------------------
#: THE RULING (orchestrator, 2026-09-07, K7): *`dim` >= 3:1 wherever it
#: classifies (a severity rung on a log row, a dash count, a state mark); a
#: purely decorative leader or seam is exempt by seat, named.*
#: And L7: *the `info` rung may be air (blueprint, ledger, doctrine) or drawn;
#: if drawn it obeys K7 (>= 3:1).*
#:
#: `dim` IS UNDER 3:1 IN ALL ELEVEN AND UNDER 1.6:1 IN FIVE
#: (`DIM_AGAINST_GROUND`, inc70, which measured it and left it as a roster).
#: So the ruling's first branch — raise `dim` — is unavailable everywhere, and
#: what this law does is the second: it says which SEATS may spend it.
#:
#: THE TABLE IS SEATS, NOT CODE LINES. There are 160 `c["dim"]` sites in
#: `language.py` and enumerating them would be a list of expressions, not of
#: readings. A seat is something a reader points at, so each row below is
#: rendered through the kit's own contract method and read back.
#:
#:   CLASSIFIES  the run is the only thing saying WHICH KIND this is. If the
#:               tier is under 3:1 the seat moves to `mut` — never the token,
#:               which is ten kits' ground.
#:   DECORATES   the run leads, seams, rails or pages. WCAG 1.4.11 is a floor
#:               for a component boundary and a leader is not one; round four
#:               said so itself (§8.4: *"applying 4.5:1 to a dot leader is
#:               probably the wrong instrument"*).
#:   CARRIED     the run classifies AND a second, non-colour channel already
#:               carries the classification, with the law that proves it named.
#:               This is the only branch that lets a classifying seat keep
#:               `dim`, and it may not be claimed without a green law.
DIM_CLASSIFIES = {
    "log.rung": ("classifies",
                 "the mark that says WHICH KIND of event a row is. Seven "
                 "kits painted it between 1.35:1 and 1.96:1 and round four's "
                 "criterion answered two of eight. inc74 moved the SEAT: "
                 "`log_row`'s tone ladder is `mut / mut / ink`."),
    "tabs.inactive": ("classifies",
                      "the words that say which modes exist and which one "
                      "you are not in. ledger was the only kit of eleven "
                      "drawing them in `dim` (1.50:1) and inc74 moved the "
                      "WORD to `mut`; the leader beside it stays `dim`."),
    "part.disabled": ("carried",
                      "`test_two_states_of_one_part_are_told_apart_on_a_"
                      "channel` — every kit separates a DISABLED part from "
                      "its live one by GLYPH, over every declared table, and "
                      "the roster of exceptions is "
                      "`STATES_TOLD_APART_BY_SIZE`. The tier is a second "
                      "channel over a channel that is asserted green."),
    "log.time": ("decorates",
                 "a timestamp is content the row carries, not a class it "
                 "belongs to; the rung beside it is what classifies."),
    "field.leader": ("decorates",
                     "the run of dots between a caption and its figure. It "
                     "joins two things that are both legible; it says "
                     "nothing about either."),
    "tabs.separator": ("decorates",
                       "the rule between two mode names."),
    "pane.seam": ("decorates",
                  "the divider between two panes — solari names it `seam` "
                  "and it is one step off the flap face BY CONSTRUCTION."),
    "pager.unlit": ("decorates",
                    "the unlit dots of a pager. The LIT ones carry the "
                    "position and are not `dim`; an unlit dot is the track "
                    "they run on."),
}


def dim_seat_tones(lang: str) -> dict[str, set[str]]:
    """What tier each seat in `DIM_CLASSIFIES` is actually drawn in, read back
    off the kit's own contract methods rather than off the source."""
    k, t = LG.kit(lang), LG.THEMES[lang]
    seen: dict[str, set[str]] = {}

    def tones(markup: str, want: str) -> set[str]:
        """Every tier that wraps a run containing `want`."""
        out = set()
        for tone, body in re.findall(r"\[([^\]]+)\]([^\[]*)", markup):
            # CASE-INSENSITIVE, and that is not tidiness: corgi
            # UPPERCASES its mode legend, so a case-sensitive reader
            # found no seat there and the law passed on a kit that had
            # the very defect. The first draft did exactly that.
            if want and want.lower() in body.lower():
                out.add(tone.split()[-1])
        return out

    row = k.log_row("info", "09:41", "board loaded")
    rung = k.LEVELS["info"].strip()
    seen["log.rung"] = tones(row, rung) if rung else set()
    seen["log.time"] = tones(row, "09:41")

    strip = k.tabs(["board", "form", "cfg", "log"], "board")
    seen["tabs.inactive"] = tones(strip, "form")

    seen["part.disabled"] = {k.part_tone("main", LG.DISABLED, "switch")}
    return {s: v for s, v in seen.items() if v}


@pytest.mark.parametrize("lang", LANGS)
def test_a_dim_run_that_classifies_is_legible_or_has_moved(lang):
    """K7's `dim` clause, seat by seat, over all eleven.

    THE VERDICT COMES FROM THE TABLE AND THE TIER FROM THE KIT, so neither
    half can be adjusted to fit the other in one file. A `classifies` seat
    either clears 3:1 in `dim` or is not drawn in `dim`; a `carried` seat may
    keep it and must name a law; a `decorates` seat is exempt and must say
    why.

    THE ROSTER IS NON-VACUOUS BY CONSTRUCTION: `dim_seat_tones` returns only
    the seats it could actually render, and the assertion below requires the
    two classifying seats to be among them. A kit that stopped drawing a log
    or a mode strip would go red here rather than pass by absence."""
    t = LG.THEMES[lang]
    dim, ground = t["dim"], t["ground"]
    legible = contrast(dim, ground) >= 3.0
    tones = dim_seat_tones(lang)
    want = {"tabs.inactive"}
    if LG.kit(lang).LEVELS["info"].strip():
        want.add("log.rung")
    assert want <= set(tones), (lang, sorted(want), sorted(tones))
    for seat, seen in tones.items():
        verdict, why = DIM_CLASSIFIES[seat]
        assert why.strip(), (lang, seat, "a seat with no reason is not a row")
        if verdict == "classifies" and not legible:
            assert dim not in seen, (lang, seat, dim, sorted(seen),
                                     round(contrast(dim, ground), 2))
    # AND THE LADDER STAYS ORDERED, which is the clause a floor cannot carry
    assert (contrast(t["ink"], ground) > contrast(t["mut"], ground)
            > contrast(dim, ground)), lang


def test_the_dim_table_covers_what_it_claims_to(monkeypatch):
    """The table's own vacuity arms, and the shape `MEANING_AT_AN_OPENER` and
    `THE_GROUND_IS_NOT_A_MARK` already have in this file.

    (a) every verdict is one of the three the ruling allows;
    (b) the two branches that let a seat KEEP `dim` are both used, so the law
        is not passing because everything was called decorative;
    (c) `carried` names a law that exists and is green — this is the only
        branch that excuses a classifying seat, and a citation nobody runs is
        not a citation."""
    assert {v for v, _ in DIM_CLASSIFIES.values()} == {
        "classifies", "decorates", "carried"}
    assert sum(v == "classifies" for v, _ in DIM_CLASSIFIES.values()) == 2
    assert sum(v == "carried" for v, _ in DIM_CLASSIFIES.values()) == 1

    cited = DIM_CLASSIFIES["part.disabled"][1]
    assert "test_two_states_of_one_part_are_told_apart_on_a_channel" in cited
    for lang in LANGS:
        test_two_states_of_one_part_are_told_apart_on_a_channel(lang)


def test_the_dim_law_bites_on_the_two_seats_inc74_moved(monkeypatch):
    """TEETH, on the two seats and the readings round four measured.

    The `log_row` arm restores `dim` at the rung for ALL ELEVEN at once,
    because the seat is the base's and the defect was the corpus's — seven
    kits drew it and four spend air or words there. The `tabs` arm is
    ledger's alone, which is what the measurement said: ten kits already gave
    an inactive label `mut`."""
    for lang in LANGS:
        test_a_dim_run_that_classifies_is_legible_or_has_moved(lang)

    old = LG.Kit.log_row

    def dim_rung(self, level, time, message, tail=False):
        c = self.c
        mk = self.LEVELS.get(level, self.LEVELS["info"])
        tone = {"info": c["dim"], "warn": c["mut"]}.get(level, c["ink"])
        body = c["mut"] if level == "info" else c["ink"]
        return (f"[{c['dim']}]{LG.mark(str(time))}[/] "
                f"[{tone}]{LG.mark(mk)}[/] "
                f"[{body}]{LG.mark(str(message))}[/]")

    monkeypatch.setattr(LG.Kit, "log_row", dim_rung)
    red = [l for l in LANGS
           if not _passes(test_a_dim_run_that_classifies_is_legible_or_has_moved, l)]
    # EIGHT OF THE ELEVEN, and the three that survive are the three the
    # ruling predicted plus one it did not:
    #   blueprint, ledger  the rung is AIR by doctrine (L7), so there is no
    #                      mark for a tier to be wrong about;
    #   prism              its `dim` is 3.25:1, the only one of the eleven
    #                      over the 3:1 floor, so the seat may keep it.
    # solari IS in the list and its rung is three WORDS (`OK ` / `DLY` /
    # `CNX`) -- the brief's own count said nine languages draw it under 2:1
    # and the measurement says EIGHT, with solari among them and prism not.
    assert set(red) == {"instrument", "swiss", "industrial", "nord",
                        "darkside", "naught", "corgi", "solari"}, red
    monkeypatch.undo()

    k = LG.kit("ledger")
    old_tabs = LG.Ledger.tabs

    def dim_tabs(self, options, active):
        c = self.c
        return f"[{self.rule_color}] {self.RULE_V} [/]".join(
            f"[{c['ink']}]{self.tally} {o.upper()}[/]" if o == active
            else f"[{c['dim']}]{self.LEAD} {o}[/]" for o in options)

    monkeypatch.setattr(LG.Ledger, "tabs", dim_tabs)
    assert round(contrast(LG.THEMES["ledger"]["dim"],
                          LG.THEMES["ledger"]["ground"]), 2) == 1.50
    with pytest.raises(AssertionError):
        test_a_dim_run_that_classifies_is_legible_or_has_moved("ledger")
    for other in LANGS:
        if other != "ledger":
            test_a_dim_run_that_classifies_is_legible_or_has_moved(other)
    monkeypatch.undo()

    for lang in LANGS:
        test_a_dim_run_that_classifies_is_legible_or_has_moved(lang)


def _passes(fn, *args) -> bool:
    try:
        fn(*args)
    except AssertionError:
        return False
    return True


#: L7, MEASURED IN THE ARTEFACT AFTER inc74. The `info` rung's tier, per kit,
#: and what each kit spends at that seat. Four of the eleven draw NOTHING
#: there and their reason is doctrine; the seven that draw a mark now draw it
#: in `mut`, which is `MUT_FLOOR` or better in ten and solari's named
#: exemption in one.
#:
#: ROUND FOUR'S §0b IS THE BEFORE-COLUMN and every number in it is inc73's
#: reader reproducing it: instrument 1.74 · swiss 1.75 · industrial 1.96 ·
#: nord 1.69 · darkside 1.39 · naught 1.35 · corgi 1.71 · prism 3.25.
INFO_RUNG_IS_AIR = {
    "blueprint": "`\"  \"` — a line-type ladder in which ABSENCE is the calm "
                 "state (RULED doctrine, spec.md §16.1). A drawing office "
                 "does not rule a line to say there is nothing to note.",
    "ledger": "`\"  \"` — the same doctrine, and the one inc60 cited as its "
              "precedent. Round four reversed its own objection to that "
              "precedent after measuring the corpus (§2.11 `S5`).",
}


@pytest.mark.parametrize("lang", LANGS)
def test_the_info_rung_is_air_by_doctrine_or_legible_by_tier(lang):
    """L7, and it is the same law read from the other end: the seat that
    classifies a CALM row either says nothing at all — with a citation — or is
    painted in a tier a reader has.

    solari IS NEITHER AND IS COUNTED WITH THE DRAWN, deliberately: its rungs
    are WORDS (`OK ` / `DLY` / `CNX`), so the mark is text and text is exactly
    what `mut` is for. It is the one kit whose severity ladder needs no glyph
    argument at all."""
    k, t = LG.kit(lang), LG.THEMES[lang]
    rung = k.LEVELS["info"]
    if not rung.strip():
        assert lang in INFO_RUNG_IS_AIR, (lang, "air with no citation")
        assert INFO_RUNG_IS_AIR[lang].strip(), lang
        return
    assert lang not in INFO_RUNG_IS_AIR, (lang, "a citation for a drawn rung")
    tones = dim_seat_tones(lang)["log.rung"]
    assert tones == {t["mut"]}, (lang, sorted(tones))
    if lang not in THE_BAND_IS_A_SECOND_GROUND:
        assert contrast(t["mut"], t["ground"]) >= MUT_FLOOR, lang


# ---------------------------------------------------------------------------
# inc75 (rework-7a) — C8's second half, and a paper no value can contain.
# ---------------------------------------------------------------------------
#: WHERE A CONFIRM MAY REFUSE TO DRAW AN EDGE, and the citation for each.
#:
#: THE RULING (orchestrator, 2026-09-07, C8's second half): *corgi's confirm
#: gets walls from its display frame (`▓`, inc67's register ruling) with the
#: board still gone; thirty blank rows with no opener or closer is not a
#: modal.*
#:
#: C2 IS THE OLDER HALF OF THE SAME QUESTION and it took four batches to
#: close: inc66 gave swiss its second rule, inc72 gave ledger one and moved
#: naught's band off the `DANGER_FORM`, and this increment gives corgi an edge
#: at all. What is asserted now is the SHAPE of the answer rather than one
#: kit's spelling of it: a confirm's first and last DRAWN row each carry a
#: mark of the language's own.
#:
#: "DRAWN" AND NOT "CHANGED", and the difference is the whole of corgi. A
#: confirm that erases the page changes every row it erases, so its first
#: changed row is a row that went BLANK — which is a fact about the erasure
#: and not about the question. `confirm_span` is right for contiguity and
#: wrong for this reading, so this law walks in from both ends of the span to
#: the first row that says something.
#:
#: ONE REFUSAL, AND IT IS A GROUND RATHER THAN A HOLE. solari's band is
#: `band="reverse"` — a token this kit declares — so its edge is not a mark
#: at all: the question is a REVERSED PLATE across the full measure, and what
#: says where it begins and ends is the rect's own boundary. Asking it for a
#: glyph would be asking a departure board to draw a line around its
#: announcement row. The arm below asserts the plate is really there, in the
#: shipped `.svg`, so the exemption cannot be claimed by a kit that simply
#: forgot to draw an edge.
CONFIRM_EDGE_REFUSED = {
    "solari": "`band=\"reverse\"` — the announcement is a plate, not a "
              "framed block, and a plate's edge is its own rect. Asserted "
              "against `solari_S4.svg`: the band's colour is painted as a "
              "background run at full measure.",
}


def confirm_edges(lang: str) -> tuple[str, str]:
    """`(first drawn row, last drawn row)` of a kit's confirm, off the shipped
    frame: the outermost rows of the band that are not blank."""
    first, last = confirm_span(lang)
    rows = (FRAMES / f"{lang}_S4.txt").read_text(
        encoding="utf-8").splitlines()
    drawn = [rows[i].strip() for i in range(first, last + 1)
             if rows[i].strip()]
    return (drawn[0], drawn[-1]) if drawn else ("", "")


@pytest.mark.parametrize("lang", LANGS)
def test_a_confirm_opens_and_closes_on_marks_of_its_own(lang):
    """C8's second half and C2's shape, over the eleven.

    `test_every_confirm_says_where_it_ends` (inc66) asked only that the LAST
    changed row say something, and it was written deliberately weak because
    eleven languages close a question eleven ways. It could not see
    `corgi_S4`, which was exempt by a citation — and a citation is not a
    scope check: the sentence corgi cited was about the BOARD, and thirty
    blank rows are not a board.

    BOTH ENDS NOW, AND STILL NOT A BOX: what is asked is that each end carry
    a mark from the kit's own alphabet, never that it be a rule, a lid or a
    corner. naught's band is two runs of its unlit lattice at full charge
    (inc72), swiss's two hairlines, ledger's two rules (inc72), corgi's two
    bars of its display frame (this increment), industrial's and nord's the
    top and bottom of a real box — six spellings of one shape.

    THE EXEMPTION TABLE IS EMPTY AND IS ASSERTED EMPTY. It exists because
    `MODAL_KEEPS_NOTHING` taught this file that an exemption written before
    anybody could satisfy the law outlives its reason; if a twelfth language
    ever cannot draw an edge, its name and its argument go here."""
    assert set(CONFIRM_EDGE_REFUSED) == {"solari"}, sorted(CONFIRM_EDGE_REFUSED)
    top, bottom = confirm_edges(lang)
    assert top, (lang, "the confirm's first drawn row is blank")
    assert bottom, (lang, "the confirm's last drawn row is blank")
    if lang in CONFIRM_EDGE_REFUSED:
        # THE REFUSAL IS CHECKED, NOT TAKEN ON ITS WORD: the plate has to be
        # in the picture, at full measure, or this is a kit with no edge and
        # a sentence about one.
        assert CONFIRM_EDGE_REFUSED[lang].strip(), lang
        assert LG.THEMES[lang].get("band") == "reverse", lang
        svg = (FRAMES / f"{lang}_S4.svg").read_text(encoding="utf-8")
        runs = [(float(w), f) for _x, _y, w, _h, f in _RECT_RUN.findall(svg)]
        assert any(w > 800 for w, _f in runs), (lang, runs[:3])
        return
    # and the edge is a MARK, not the question's own words: the outermost
    # rows of every other band in this corpus are chrome, never prose
    assert not any(w in top for w in ("Delete", "tasks", "undone")), (lang, top)


def test_corgis_confirm_has_an_edge_and_still_has_no_board():
    """C8, BOTH HALVES IN ONE PLACE — because the two are in tension and the
    increment that took only one of them is why this test exists.

    (a) THE EDGE: the first and last drawn rows of `corgi_S4` are full-measure
        runs of this kit's own `PANE_RULE`, the bar inc67 milled precisely so
        that a partition carries no rung of anything (K5).
    (b) THE BOARD IS STILL GONE: no row of the page behind survives except the
        mode strip, which is `MODAL_KEEPS_ONLY_THE_HEAD`'s whole scope.
    (c) AND THE BARS ARE NOT THE `DANGER_FORM` — the trap naught sat in for
        six batches and inc72 dug it out of. `█` is corgi's error rung and its
        danger form; the edge may not be it."""
    k = LG.kit("corgi")
    top, bottom = confirm_edges("corgi")
    assert set(top) == set(bottom) == {k.PANE_RULE}, (top[:8], bottom[:8])
    assert len(top) == len(bottom) == 100, (len(top), len(bottom))
    assert k.PANE_RULE not in "".join(k.DANGER_FORM), k.PANE_RULE
    assert k.PANE_RULE not in "".join(k.LEVELS.values()), k.PANE_RULE

    out = [plain(r) for r in k.overlay(dialog(k), DIALOG_W, DIALOG_H, UNDER)]
    assert out[0].rstrip() == plain(UNDER[0]).rstrip(), out[0]
    rest = [plain(r) for r in UNDER[1:]]
    assert not any(r.strip() and r.strip() in o for r in rest for o in out), out
    assert "corgi" in MODAL_KEEPS_ONLY_THE_HEAD
    assert "the board is gone" in LG.MODAL_BORDER_REFUSED["corgi"]


def test_the_confirm_edge_law_bites_on_the_composition_corgi_shipped(
        monkeypatch):
    """TEETH. Restore inc65's block — the mode strip and thirty-one blank rows
    — and assert the reading that made it a `rework`: the band's outermost
    DRAWN row becomes the question itself, so there is nothing between the
    reader and the words that says a question has begun."""
    k = LG.kit("corgi")
    top, _ = confirm_edges("corgi")
    assert set(top) == {k.PANE_RULE}

    def edgeless(self, rows, w, h, under, about=None):
        head = under[0] if under else ""
        y = max(1, (h - len(rows)) // 2)
        return ([head] + [""] * (y - 1) + list(rows) + [""] * h)[:h]

    monkeypatch.setattr(LG.Corgi, "overlay_instead", edgeless)
    out = [plain(r) for r in k.overlay(dialog(k), DIALOG_W, DIALOG_H, UNDER)]
    drawn = [r.strip() for r in out[1:] if r.strip()]
    assert drawn and drawn[0] == "Delete 3 tasks?", drawn[:2]
    assert k.PANE_RULE not in "".join(drawn), "the edge is gone"
    monkeypatch.undo()

    out = [plain(r) for r in k.overlay(dialog(k), DIALOG_W, DIALOG_H, UNDER)]
    drawn = [r.strip() for r in out[1:] if r.strip()]
    assert set(drawn[0]) == {k.PANE_RULE}, drawn[0][:8]


#: THE ONE SEAT WHERE PAPER AND VALUE MEET.
#:
#: THE RULING (orchestrator, 2026-09-07): *the value's separators and the
#: field paper may not be one glyph: the paper becomes a cell that no value
#: can contain (cite industrial's alphabet), the invalid marks at
#: slider.knob/stepper.step stay.*
#:
#: inc71 SPLIT `/`'s ROLE IN THE CENSUS AND THE CORPUS COULD NOT CONFIRM IT.
#: Round four §7.6: the second role lives at `slider.knob[INVALID]` and
#: `stepper.step[INVALID]`, and **no frame of the sixty-six draws either** —
#: so the row was real in the declaration and untestable in the artefact,
#: while the collision a reader CAN see was a different one: `▐12/09/26//////
#: …▌`, twenty-six paper slashes and two of the value's own, with no frontier
#: between them.
#:
#: THE LAW IS THE READING AND NOT THE TOKEN: the rejected field's PAPER never
#: appears inside any value this repo's fixture renders. Checkable in eleven
#: languages, red in exactly one.
#:
#: TWO KITS PAPER THE FIELD IN AIR and are outside this law rather than
#: exempt by it: nord declares `"? ?"` and darkside `"Ø Ø"`, so their rune is
#: a space and there is no paper for a value to be confused with. That is an
#: L2-shaped reading ("air is not a state", inc69) at a seat L2 did not reach,
#: and no ruling covers it — recorded in `inc75.md` §11 rather than decided
#: here.
def invalid_paper(lang: str) -> str:
    """The RUNE of a kit's rejected field — its paper — through the one
    splitter both instruments share (`split_field_glyph`, inc71)."""
    g = LG.kit(lang).PART_GLYPHS["textfield.main"][LG.INVALID]
    return LG.split_field_glyph(g)[1]


def fixture_values() -> set[str]:
    """Every string this repo's fixture puts on a screen, read from
    `fixture.py` BY PATH — so the law measures the corpus that is actually
    rendered rather than a list somebody kept up to date."""
    fx = solari_fixture()
    out = {str(f) for t in fx.TASKS for f in t if f is not None}
    for row in getattr(fx, "DETAIL", ()):
        out.update(str(x) for x in row)
    # AND THE VALUE THE FORM ITSELF SETS, which is the row the objection is
    # about: `industrial_S2` puts a DATE into the rejected field.
    out |= {"12/09/26", "2026-09-12"}
    return {v for v in out if v}


@pytest.mark.parametrize("lang", LANGS)
def test_a_rejected_fields_paper_is_a_cell_no_value_can_contain(lang):
    """The `/` ruling, over the eleven, against the fixture's own values."""
    paper = invalid_paper(lang)
    values = fixture_values()
    assert len(values) > 10, "the fixture reader came back empty"
    if not paper.strip():
        # air: no paper, so nothing for a value to be confused with. Named in
        # the comment above and NOT silently skipped -- the two kits are
        # asserted by name so a third cannot join them unnoticed.
        assert lang in ("nord", "darkside"), (lang, repr(paper))
        return
    hit = sorted(v for v in values if paper in v)
    assert not hit, (lang, paper, hit[:4])


def test_the_paper_law_bites_on_the_declaration_industrial_shipped(
        monkeypatch):
    """TEETH, on the real cell and the real value — and on what the ruling
    PRESERVED, because a fix that swept the glyph would have been a different
    decision from the one taken: `/` stays the invalid mark at the knob and at
    the stepper's step, which is where inc71 put it."""
    k = LG.kit("industrial")
    assert invalid_paper("industrial") == "░"
    assert k.PART_GLYPHS["knob"][LG.INVALID] == "/"
    assert k.PART_GLYPHS["stepper.step"][LG.INVALID] == "//"
    # and the new paper is the kit's own shade ramp, not a new cell
    assert k.PART_GLYPHS["indicator"][LG.DISABLED] == "░"

    monkeypatch.setitem(k.PART_GLYPHS["textfield.main"], LG.INVALID, "▐/▌")
    assert invalid_paper("industrial") == "/"
    with pytest.raises(AssertionError):
        test_a_rejected_fields_paper_is_a_cell_no_value_can_contain(
            "industrial")
    for other in LANGS:
        if other != "industrial":
            test_a_rejected_fields_paper_is_a_cell_no_value_can_contain(other)
    monkeypatch.undo()
    assert invalid_paper("industrial") == "░"

# ---------------------------------------------------------------------------
# inc64 (rework-6a) — L8 and L9: more value is more ink, in one direction
# ---------------------------------------------------------------------------
#: RELATIVE INK PER CELL, for the fill vocabulary these eleven kits actually
#: spend. Braille and the block elements are COMPUTED — a braille cell's dots
#: over eight, a block element's declared coverage — so they cannot drift. The
#: eight below are DECLARED, with the reason, because Unicode gives no coverage
#: for them and this file will not pretend to measure a font (E2: the artefacts
#: carry no font metric). They are ordinal, not photometric: what every law
#: here asks of them is which of two cells is the fuller, and each pair below
#: is a pair the corpus draws side by side.
CELL_INK = {
    "·": 0.05,   # · MIDDLE DOT — the lightest mark in the corpus
    "◦": 0.06,   # ◦ WHITE BULLET — the same size, hollow
    "∙": 0.10,   # ∙ BULLET OPERATOR — the same size, filled
    "─": 0.08,   # ─ LIGHT HORIZONTAL — one thin stroke
    "━": 0.16,   # ━ HEAVY HORIZONTAL — the same stroke, doubled
    "▪": 0.30,   # ▪ BLACK SMALL SQUARE
    "▬": 0.50,   # ▬ BLACK RECTANGLE — half a cell, solid
    "▫": 0.15,   # ▫ WHITE SMALL SQUARE — ▪'s outline
    # inc68: the third rung of the one ladder the D-addendum blesses by name
    # (`▫▫ ▪▪ ■■`, "hollow to filled and grows, in the same direction"). Two
    # of its three were weighed and the third was not, so K4's channel law
    # was refusing a ladder the ruling had already ruled on.
    "■": 0.45,   # ■ BLACK SQUARE — ▪ at full size
    # inc67: naught's meter left the LIT dot for the CHARGED one, so the
    # direction law needs a weight for it. Ordinal and placed by the kit's own
    # ramp, which is the pair the corpus draws side by side: `⋅ ◦ ∙ ◉ ●` — a
    # ring with a filled centre is more ink than a small filled dot and less
    # than a full disc, and this file will not pretend to have measured a font.
    # ONLY THE ONE CELL, and the rest of naught's ramp is deliberately absent:
    # `○` and `●` are already scored by `mark_ink`'s own hollow/solid rule and
    # declaring weights for them here made the ticked-box law read a filled
    # disc as LIGHTER than its outline. A weight is added when a law needs it,
    # never as a set.
    "◉": 0.22,   # ◉ FISHEYE — a ring with its centre filled
}
#: coverage of the block elements, U+2580–U+259F, as eighths or quarters of a
#: cell. This is what the glyphs ARE, so it is arithmetic and not taste.
CELL_INK.update({chr(cp): v for cp, v in {
    0x2580: .5, 0x2581: .125, 0x2582: .25, 0x2583: .375, 0x2584: .5,
    0x2585: .625, 0x2586: .75, 0x2587: .875, 0x2588: 1.0, 0x2589: .875,
    0x258a: .75, 0x258b: .625, 0x258c: .5, 0x258d: .375, 0x258e: .25,
    0x258f: .125, 0x2590: .5, 0x2591: .25, 0x2592: .5, 0x2593: .75,
    0x2594: .125, 0x2595: .125, 0x2596: .25, 0x2597: .25, 0x2598: .25,
    0x2599: .75, 0x259a: .5, 0x259b: .75, 0x259c: .75, 0x259d: .25,
    0x259e: .5, 0x259f: .75,
}.items()})


def cell_ink(ch):
    """How full one cell is, in the corpus's own fill vocabulary.

    `None` means "this file has no weight for that cell", which is a REFUSAL
    and not a zero: a law that scored an unknown glyph as empty would pass
    every language that moved to one."""
    o = ord(ch)
    if ch in " ⠀":
        return 0.0
    if 0x2800 <= o <= 0x28ff:                       # braille: dots over eight
        return bin(o - 0x2800).count("1") / 8
    return CELL_INK.get(ch)


def mark_ink(ch):
    """`cell_ink`, with an unweighed glyph counted as a FULL mark.

    Used only by the ticked-box law, and only in the direction that makes it
    HARDER to pass. A box's two states differ in one cell; the corpus's tick
    vocabulary is thirty-odd glyphs (`X`, `x`, `#`, `*`, `×`, `╳`, `╪`, `◉`,
    `●`, `◍`, `◎`, `▲`, `▼`, `▽`, `┄` ...) and this file will not pretend to
    know how full each of them draws in a font it cannot see (E2). Scoring an
    unknown as 1.0 means an UNCHECKED cell that is unknown is treated as the
    fullest thing on the page, so a language that ticked by taking ink away
    cannot hide behind a glyph nobody weighed. The permissive half — blank to
    an unknown mark — is a tick that adds a mark, which is the thing the law
    is for."""
    w = cell_ink(ch)
    return 1.0 if w is None else w


def checkbox_knob(k, base, on):
    """The BOX, without the word beside it.

    `Kit.checkbox` appends `check_label`, and three languages spend a word
    there (`ON`/`--`, `posted`/`open`, `ON `/`OFF`). Counting the label would
    have made this law measure how long the English is: solari's `OFF` is one
    letter longer than its `ON `, so a whole-control reading called its ACTIVE
    checkbox lighter when ticked while the box itself goes `▁·▁` → `▁█▁`."""
    state = LG.with_checked(base, on)
    return shape(k.component_cells("checkbox", LG.bool_value(state),
                                   0, 1, 1, state))


#: the four control states a checkbox is declared at.
_BOX_STATES = (LG.DEFAULT, LG.FOCUSED, LG.ACTIVE, LG.DISABLED)


@pytest.mark.parametrize("lang", LANGS)
def test_a_ticked_box_is_never_lighter_than_an_empty_one(lang):
    """L8. TICKING A BOX ADDS INK. It does not take it away.

    `prism_S2` row 11 is the frame that asked for this law. The fixture ticks
    `ui` and `urgent` and leaves `api` clear — every other language draws it
    that way (`darkside` `( ) api  (◎) ui`, `corgi` `▒▒ -- api  ▓▓ ON ui`,
    `naught` `◦ api  ◉ ui`). prism drew the two ticked tags as `⠿⠀⠿`, the
    EMPTY well, and the one clear tag as `⠿⠉⠿`, a mark inside the box. Every
    reader who has not read the kit points at `api`.

    inc59 moved both of those tables in the same increment and did not notice,
    because no law in this file has ever compared two states of one part (K4).
    This is the first one that does.

    MEASURED ON THE BOX AND NOT ON THE CONTROL — see `checkbox_knob`. And
    measured as `>=`, not `>`: four languages tick by changing the SHAPE of a
    mark at the same weight (naught `◦`→`◉`, `○`→`●`, `◌`→`◍`), which is
    ruling D's first channel spent honestly, and a law demanding strictly more
    ink would call those defects."""
    k = LG.kit(lang)
    for base in _BOX_STATES:
        off, on = checkbox_knob(k, base, False), checkbox_knob(k, base, True)
        assert len(off) == len(on), (lang, base, off, on)
        moved = [(a, b) for a, b in zip(off, on) if a != b]
        assert moved, (lang, base, "a tick that changes nothing", off)
        for a, b in moved:
            assert mark_ink(b) >= mark_ink(a), (lang, base, off, on, a, b)


def test_the_ticked_box_law_bites_on_the_frame_it_was_written_for():
    """Watched failing on the declaration inc64 moved, not on a mock.

    The two centres are put back the way inc59 left them and the law goes red
    at all four states of prism and at no state of any other language."""
    saved = dict(LG.Prism.PART_GLYPHS)
    try:
        LG.Prism.PART_GLYPHS = dict(
            saved,
            **{"checkbox.main": {LG.DEFAULT: "⠿⠉⠿",
                                 LG.FOCUSED: "⣷⠉⣷",
                                 LG.ACTIVE: "⣾⠉⣾",
                                 LG.DISABLED: "⠄⠄⠄"},
               "checkbox.knob": {LG.DEFAULT: "⠿⠀⠿",
                                 LG.FOCUSED: "⣷⠀⣷",
                                 LG.ACTIVE: "⣾⠀⣾",
                                 LG.DISABLED: "⠄⠀⠄"}})
        red = []
        for lang in LANGS:
            k = LG.kit(lang)
            for base in _BOX_STATES:
                off = checkbox_knob(k, base, False)
                on = checkbox_knob(k, base, True)
                if any(mark_ink(b) < mark_ink(a)
                       for a, b in zip(off, on) if a != b):
                    red.append((lang, base))
    finally:
        LG.Prism.PART_GLYPHS = saved
    assert [l for l, _ in red] == ["prism"] * 4, red
    assert sorted(b for _, b in red) == sorted(_BOX_STATES), red
    # and green again on the shipped declaration
    k = LG.kit("prism")
    assert checkbox_knob(k, LG.DEFAULT, True) == "⠿⠉⠿"
    assert checkbox_knob(k, LG.DEFAULT, False) == "⠿⠀⠿"


#: the two meters that draw no fill ramp at all, by name and with the kit's
#: own word for what they draw instead. Their empty and full cells are not in
#: `CELL_INK` and never will be — a digit and a terminator are not fill — so
#: the direction law below cannot ask them anything, and a roster is the only
#: honest way to say so. A third language arriving here is a language that has
#: stopped drawing a ramp, and somebody has to look at it.
RAMPLESS_METERS = {
    "solari": "odometer",       # QUANTITY IS DIGITS, never a bar
    "blueprint": "dimension",   # quantity is a DIMENSION SPAN with terminators
}


def track_cell(rendered):
    """The cell a widget's TRACK is made of: the commonest non-ASCII glyph in
    the rendering.

    Commonest rather than first, because the head of these runs is not the
    track — it is a knob (`◉`, `⢸`, `▙▟`), a bracket or a readout, and every
    one of them appears once while the track appears ten to twenty-five
    times. ASCII is dropped so a percentage, a `[`, a `/` or the word `WORK`
    cannot win."""
    counts = {}
    for ch in plain(rendered).split("\n")[0]:
        if ord(ch) < 128:
            continue
        counts[ch] = counts.get(ch, 0) + 1
    return max(counts, key=counts.get) if counts else None


@pytest.mark.parametrize("lang", LANGS)
def test_a_languages_fill_direction_is_one_declaration(lang):
    """L9. MORE VALUE IS MORE INK, and it is the same answer at every widget
    this language draws a quantity with.

    THE FRAME THAT ASKED FOR IT. `prism_S1` row 13 drew
    `⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿  44%` — twelve LIGHT cells of
    twenty-seven, labelled 44 %, so the picture reads 56 % — while `prism_S3`
    drew `⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣀⣀⣀⣀ 70` and `prism_S5` drew
    `⣿⣿⣿⣿⣿⣿⣿⣀⣀⣀⣀⣀⣀⣀ 5`, both heavy-first, out of the same kit. Two code
    paths: `_meter_ember` composed its own bitmap and filled the DONE side
    with ash, and `component_cells` spends `indicator` on the value and `main`
    on the rest. One language, two directions, and no instrument in this repo
    reached either — the meter, the slider and the bar are all outside
    `PART_GLYPHS` and outside the census's set B (K5, spec §15.4).

    HOW THE DIRECTION IS READ. Each widget is rendered at its floor and at its
    ceiling and the track's own cell is taken from each (`track_cell`). The
    law is that the ceiling's cell is fuller than the floor's — one relation,
    asked three times, per language.

    WHY `>` HERE AND `>=` IN THE BOX LAW. A checkbox may tick by changing a
    mark's shape at the same weight; a QUANTITY may not, because the reader is
    being asked to judge an amount from a length and the two ends of that
    length have to differ."""
    k = LG.kit(lang)
    widgets = {
        "meter": lambda v: k.meter(v, 100, [5, 4, 3, 4], 37),
        "slider": lambda v: k.slider(v, 0, 100, 14),
        "readbar": lambda v: k.readbar(v, 0, 100, 27),
    }
    asked = 0
    for name, draw in widgets.items():
        empty, full = track_cell(draw(0)), track_cell(draw(100))
        if name == "meter" and lang in RAMPLESS_METERS:
            assert (empty is None or cell_ink(empty) is None
                    or full is None or cell_ink(full) is None), \
                (lang, "has grown a ramp -- take it off RAMPLESS_METERS",
                 empty, full)
            continue
        assert empty is not None and full is not None, (lang, name)
        lo, hi = cell_ink(empty), cell_ink(full)
        assert lo is not None and hi is not None, (lang, name, empty, full)
        assert hi > lo, (lang, name, empty, lo, full, hi)
        asked += 1
    assert asked == (2 if lang in RAMPLESS_METERS else 3), (lang, asked)


def test_the_fill_direction_law_bites_and_its_roster_is_not_vacuous():
    """Watched failing on the code inc64 changed, and its two skips named.

    `_meter_ember` is put back the way it filled before this increment — the
    done side as ash, the rest as the solid field — and the law goes red for
    prism's meter and for nothing else."""
    import taskboard.wave as WV
    saved = LG.METERS["ember"]

    def burnt_first(k, done, total, counts, w):
        c = k.c
        bar_w = max(4, w - 10)
        pct, _ = LG._pct_n(done, total, bar_w)
        dots_w = bar_w * WV.DOT_COLS
        burnt = 0 if not total else max(
            0, min(dots_w, round(dots_w * done / total)))
        live, ash = (WV.Bitmap(dots_w, WV.DOT_ROWS),
                     WV.Bitmap(dots_w, WV.DOT_ROWS))
        for x in range(dots_w):
            if x < burnt:
                ash.fill_to(x, 1)
            else:
                live.fill_to(x, WV.DOT_ROWS)
        lit, spent = live.to_braille()[0], ash.to_braille()[0]
        ash_c = k.t.get("ash", c["dim"])
        bar = "".join(
            f"[{ash_c}]{spent[i]}[/]" if spent[i] != " " else
            (f"[{c['accent']}]{lit[i]}[/]" if lit[i] != " " else " ")
            for i in range(bar_w))
        return f"{bar} [{c['mut']}]{pct:>3}%[/]"

    try:
        LG.METERS["ember"] = burnt_first
        k = LG.kit("prism")
        empty = track_cell(k.meter(0, 100, [5, 4, 3, 4], 37))
        full = track_cell(k.meter(100, 100, [5, 4, 3, 4], 37))
        assert (empty, full) == ("⣿", "⣀"), (empty, full)
        assert cell_ink(full) < cell_ink(empty)          # the law is RED here
    finally:
        LG.METERS["ember"] = saved

    # the shipped direction, and the two skips, both measured
    k = LG.kit("prism")
    assert track_cell(k.meter(0, 100, [5, 4, 3, 4], 37)) == "⣀"
    assert track_cell(k.meter(100, 100, [5, 4, 3, 4], 37)) == "⣿"
    got = {}
    for lang in LANGS:
        kk = LG.kit(lang)
        cells = (track_cell(kk.meter(0, 100, [5, 4, 3, 4], 37)),
                 track_cell(kk.meter(100, 100, [5, 4, 3, 4], 37)))
        if any(c is None or cell_ink(c) is None for c in cells):
            got[lang] = cells
    assert sorted(got) == sorted(RAMPLESS_METERS), got


# ---------------------------------------------------------------------------
# inc65 (rework-6a) — F amended: no gate header under the band, and no task
# filed under a gate it is not in
# ---------------------------------------------------------------------------
def solari_fixture():
    """`prototypes/components/fixture.py`, loaded BY PATH.

    Membership is a fact about the content, so it is read from the content and
    not retyped here: a law that carried its own copy of "REWRITE THE
    ONBOARDING is in DOING" would go on passing after somebody moved the task.
    Loaded by path rather than by `sys.path` because `fixture` is a name this
    repo's test session should not own."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "_inc65_fixture", FRAMES / "fixture.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def gate_above(rows):
    """`{row index: the gate whose header stands above that row}`.

    This is the reading a person does — the gate a departure is in is the gate
    whose header is the nearest one above it — carried out with the kit's own
    `gate_of`, which parses this language's header format rather than the
    page's English."""
    k, cur, out = LG.kit("solari"), None, {}
    for i, row in enumerate(rows):
        gate = k.gate_of(row)
        if gate:
            cur = gate
        else:
            out[i] = cur
    return out


def tasks_as_filed(rows):
    """`{title: the gate the FRAME files it under}` for every task on the
    page. Titles are matched upper-cased, which is how this language prints
    them (`flap()`).

    HEADER ROWS ARE SKIPPED, and that is not tidying. Row 4 of every solari
    frame is `   GATE BACKLOG 05  ...  DETAIL  FIX LOGIN REDIRECT` — the gate
    header and the detail pane's caption share a row, so the selected task's
    title appears on a header line in all six sheets. A reader does not file
    the detail pane's caption under a gate and neither does this."""
    k = LG.kit("solari")
    where, found = gate_above(rows), {}
    for i, row in enumerate(rows):
        if k.gate_of(row):
            continue
        for title, _proj, phase, *_rest in solari_fixture().TASKS:
            if title.upper() in row:
                found[title] = (where.get(i), phase.upper())
    return found


@pytest.mark.parametrize("frame", ("S1", "S4"))
def test_solari_never_files_a_departure_under_the_wrong_gate(frame):
    """F AMENDED (orchestrator, 2026-09-07): *the band never covers a gate
    HEADER row, of any gate; it covers task rows of the first gate the confirm
    does not name, below that gate's header, and goes to the foot of the
    schedule when no such rows exist. A frame must never show a task under a
    gate it does not belong to.*

    WHAT THE FRAME SAID BEFORE. inc55 anchored the band ON the first unnamed
    gate's header, so `solari_S4` covered `GATE DOING 04` and three of its four
    departures, and the fourth — `14  REWRITE THE ONBOARDING` at row 17 — stood
    under the only header left above it, which was `GATE BACKLOG 05`. The frame
    did not fail to answer *which gate is this departure in*; it answered
    BACKLOG, and the answer was wrong. A frame that asserts something false is
    worse than one that says nothing, and inc55's declared cost was the orphan
    seam, not this.

    MEMBERSHIP COMES FROM THE FIXTURE AND POSITION FROM THE FRAME. Neither
    side of the comparison is typed here.

    ASKED OF S1 AS WELL AS S4, and S1 is the control: the same reading on the
    page with no band on it must file all six departures correctly, or the
    reader is wrong rather than the composition."""
    rows = (FRAMES / f"solari_{frame}.txt").read_text(
        encoding="utf-8").rstrip("\n").split("\n")
    filed = tasks_as_filed(rows)
    for title, (rendered, own) in sorted(filed.items()):
        assert rendered == own, (frame, title, rendered, own)
    if frame == "S1":
        assert len(filed) == 6, filed          # every departure is on the page
    else:
        # the band covers three of DOING's four; what is left must include a
        # departure of the gate the band moved onto, or this arm proves
        # nothing about the gate that was mis-filed
        assert len(filed) == 3, filed
        assert "Rewrite the onboarding" in filed, filed
        assert filed["Rewrite the onboarding"][0] == "DOING", filed


def test_no_gate_header_stands_inside_solaris_band():
    """The amendment's absolute half: *of ANY gate*, not only of the one the
    confirm names. Read off the shipped frame against the shipped page — the
    band is the rows S4 changes, and every one of them is a departure row or a
    seam on the page underneath."""
    s1 = page_rows("solari")
    band = modal_band("solari")
    inside = [(i, s1[i]) for i in band if _GATE_HEAD.search(s1[i])]
    assert not inside, inside
    # and the row the band starts on is a DEPARTURE of the gate whose header
    # is immediately above it -- the anchor the amendment asks for
    assert _GATE_HEAD.search(s1[band[0] - 1]), s1[band[0] - 1]
    assert LG.kit("solari").gate_of(s1[band[0] - 1]) == "DOING", s1[band[0] - 1]


def test_the_wrong_gate_law_bites_on_the_anchor_inc55_shipped(monkeypatch):
    """TEETH. `band_head` put back to inc55's answer — the header's own index
    — and the law watched going red on the real page with the real block.

    Not an approximation: inc55's body is `for i, gate in heads: if gate !=
    named: return i`, and that is what this arm installs."""
    k = LG.kit("solari")
    s1, under = page_rows("solari"), page_markup("solari")
    w, h = len(s1[0]), len(s1)
    rows = solari_s4_rows(k)

    def on_the_header(self, under, depth, about=None):
        if about is None:
            return self.schedule_head(under)
        named = str(about).upper()
        heads = [(i, g) for i, r in enumerate(under) if (g := self.gate_of(r))]
        if not heads:
            return self.schedule_head(under)
        for i, gate in heads:
            if gate != named:
                return i
        return self.schedule_foot(under, depth)

    monkeypatch.setattr(LG.Solari, "band_head", on_the_header)
    out = [plain(r) for r in k.overlay(rows, w, h, under, about="BACKLOG")]
    filed = tasks_as_filed(out)
    assert filed["Rewrite the onboarding"] == ("BACKLOG", "DOING"), filed
    band = [i for i, (a, b) in enumerate(zip(s1, out))
            if a.rstrip() != b.rstrip()]
    assert [i for i in band if _GATE_HEAD.search(s1[i])] == [band[0]], band

    monkeypatch.undo()
    out = [plain(r) for r in k.overlay(rows, w, h, under, about="BACKLOG")]
    assert tasks_as_filed(out)["Rewrite the onboarding"] == ("DOING", "DOING")


# ---------------------------------------------------------------------------
# inc66 (rework-6a) — C2: both answers are walled, and the confirm closes
# ---------------------------------------------------------------------------
#: inc38's ruling, quoted so the exemption below cannot outlive it. Kept as a
#: string in this file rather than read off the kit because it is a RULING
#: about swiss and not a declaration of swiss's.
ONE_MARK_ONE_SIDE = ("inc38: no wall around a button at any width, derived "
                     "from the codepoint -- in a language whose divider is "
                     "alignment the extent of a control is the next column's "
                     "job")

#: the ONE language that declares NO closing wall on a button, with the
#: citation that earns it. `Swiss.button.main` is `"▫   "` / `"▪   "` /
#: `"■   "` / `"    "` — a mark on the left and air on the right — because
#: inc38 took the walls off this seat by name ("no wall around a button at any
#: width"): in a language whose divider is alignment, the extent of a control
#: is the next column's business. A language may renounce the closing wall; it
#: may not close with a cell that is another control's opener, which is what
#: the pair clause below is for.
BUTTON_HAS_NO_CLOSER = ("swiss",)

#: the mirror of every wall this corpus opens a button with, derived once from
#: the eleven kits and written down. A wall closes a seat when the closing cell
#: is the SAME mark (a symmetric bracket: `▬ ▬`, `⠿ ⠿`, `▔ ▔`) or this mark's
#: mirror. Every entry below is a pair some kit already declares AT THIS SEAT;
#: nothing is invented here, and a language reaching for an unlisted asymmetric
#: pair has to add it and say why.
WALL_MIRRORS = {
    "(": ")", "[": "]", "├": "┤", "┣": "┫", "╞": "╡", "▐": "▌",
    "▛": "▜", "▶": "◀", "⠸": "⠇", "⠼": "⠧", "⣸": "⣇",
}

#: three measures, because the round judged the corpus at ONE (§8.2) and the
#: destructive seat is where that hurts: `inc54.md` §7 wrote that blueprint's
#: answer went from 8 cells to 12 and that "nothing in this repo renders S4
#: below 100", so the two answers colliding at a narrow measure was untested
#: rather than safe.
_ANSWER_WIDTHS = (8, 12, 20)


def declared_walls(k, state):
    """`(opener, closer)` for a button in `state`, split the way
    `Kit.button` splits them: the declared slot in half, the caller's word
    between."""
    slot = k.part_glyph("main", state, "button")
    return slot[:len(slot) // 2], slot[len(slot) // 2:]


@pytest.mark.parametrize("lang", LANGS)
def test_both_answers_of_a_confirm_are_walled_by_their_declared_pair(lang):
    """C2, THE HALF THAT IS ABOUT THE TWO BUTTONS.

    `ledger_S4` row 32 read `▶  (Delete)  │   │   Cancel   │` — one `▶` and
    three `│`. `button.main[FOCUSED]` was `▶  │`: the tally pointer on the
    left and the COLUMN RULE on the right, which is the cell this page draws
    about forty times and is also the safe answer's OPENER. So the closing
    mark of the irreversible answer and the opening mark of the safe one
    standing next to it were the same cell, and the only thing saying where
    `(Delete)` ended was its own DANGER_FORM parenthesis — the mark whose job
    is to say the button is dangerous, not to say where it stops.

    TWO CLAUSES, AT THREE WIDTHS:

    1. each answer opens with the first half and closes with the second half
       of its own declared slot — asked of the KIT, so a sheet cannot satisfy
       it by drawing walls of its own;
    2. the outer cell each answer CLOSES on is a PAIR with the one it opens
       on: the same mark, or that mark's declared mirror. This is the one the
       frame failed, and it is why the row was unreadable — a seat that ends
       on a cell unrelated to the one it began with has no shape a reader can
       close, so `(Delete)`'s right-hand `│` read as `Cancel`'s left-hand one.

    WHY "SAME OR MIRROR" AND NOT "DIFFERENT FROM THE NEXT BUTTON'S OPENER",
    which was the first draft and was measured wrong. prism closes on `⠿` and
    opens on `⠿` — `⠿⠛ ⣿Delete⣿ ⠛⠿   ⠿⠉  Cancel  ⠉⠿` — so the two seats'
    adjacent cells ARE the same mark, and the row reads perfectly because each
    seat is symmetric about its own word. SYMMETRY is what closes a seat;
    difference from a neighbour is not, and the first draft went red on prism
    for doing the right thing.

    THE ONE EXEMPTION IS NAMED AND ITS CITATION IS CHECKED. swiss declares no
    closing wall at all (`BUTTON_HAS_NO_CLOSER`), by inc38's ruling, so clause
    2 has nothing to close — and the arm asserts the closer really IS blank
    rather than letting a language slip out of the clause by accident."""
    k = LG.kit(lang)
    d_open, d_close = declared_walls(k, LG.FOCUSED)
    s_open, s_close = declared_walls(k, LG.DEFAULT)

    for w in _ANSWER_WIDTHS:
        danger = plain(k.button("Delete", w, LG.FOCUSED, danger=True))
        safe = plain(k.button("Cancel", w, LG.DEFAULT))
        assert danger.startswith(d_open), (lang, w, danger, d_open)
        assert danger.endswith(d_close), (lang, w, danger, d_close)
        assert safe.startswith(s_open), (lang, w, safe, s_open)
        assert safe.endswith(s_close), (lang, w, safe, s_close)

    for state in (LG.FOCUSED, LG.DEFAULT, LG.ACTIVE, LG.DISABLED):
        opens, shuts = declared_walls(k, state)
        a, b = opens.strip()[:1], shuts.strip()[-1:]
        if lang in BUTTON_HAS_NO_CLOSER:
            assert b == "", (lang, state, shuts)
            assert "no wall around a button" in ONE_MARK_ONE_SIDE, lang
            continue
        assert a and b, (lang, state, opens, shuts)
        assert b == WALL_MIRRORS.get(a, a), (lang, state, a, b)


def test_the_answer_pair_law_bites_on_the_declaration_ledger_shipped(
        monkeypatch):
    """TEETH. `button.main[FOCUSED]` put back to `▶  │` on the real kit, and
    the clause watched going red — on ledger and on nothing else."""
    saved = dict(LG.Ledger.PART_GLYPHS)
    monkeypatch.setattr(LG.Ledger, "PART_GLYPHS", dict(
        saved, **{"button.main": {LG.DEFAULT: "│  │", LG.FOCUSED: "▶  │",
                                  LG.ACTIVE: "▶  ◀", LG.DISABLED: "╌  ╌"}}))
    red = []
    for lang in LANGS:
        if lang in BUTTON_HAS_NO_CLOSER:
            continue
        k = LG.kit(lang)
        for state in (LG.FOCUSED, LG.DEFAULT, LG.ACTIVE, LG.DISABLED):
            opens, shuts = declared_walls(k, state)
            a, b = opens.strip()[:1], shuts.strip()[-1:]
            if b != WALL_MIRRORS.get(a, a):
                red.append((lang, state))
    assert red == [("ledger", LG.FOCUSED)], red
    k = LG.kit("ledger")
    row = (plain(k.button("Delete", 9, LG.FOCUSED, danger=True)) + "   "
           + plain(k.button("Cancel", 8, LG.DEFAULT)))
    assert row.count("│") == 3 and row.count("▶") == 1, row

    monkeypatch.undo()
    k = LG.kit("ledger")
    row = (plain(k.button("Delete", 9, LG.FOCUSED, danger=True)) + "   "
           + plain(k.button("Cancel", 8, LG.DEFAULT)))
    assert row.count("│") == 2 and row.count("◀") == 1, row


#: every S4's confirm and where it ENDS, read off the shipped frames: the
#: language, and the row that closes the question. A language whose confirm
#: has no closing row at all is in this table with `None` and has to argue for
#: it in the test below — which is what C2 is.
def confirm_span(lang):
    """`(first, last)` index of the rows S4 changes — the confirm's own
    extent on the page, from `modal_band`."""
    band = modal_band(lang)
    return band[0], band[-1]


def test_every_confirm_says_where_it_ends():
    """C2, THE HALF THAT IS ABOUT THE BAND. *Say where the modal ends.*

    `swiss_S4` opened on a 100-cell rule and closed on nothing — named as
    still open in `spec.md` §11.3 since `rework-3` and untouched by five
    batches — and `ledger_S4` did the same with its destructive answer on the
    terminal's LAST ROW. Both are confirms that destroy data.

    WHAT COUNTS AS AN END, and it is deliberately weak: the last row the
    confirm changes must SAY something. A band that ends in a rule, a seam, a
    lid, a button or a word has an end a reader can point at; a band whose
    last changed row is blank has stopped rather than closed. Weak, because
    eleven languages close a question eleven ways and a law that demanded a
    rule would be one language's taste made into a rule for the other ten.

    ledger is the one that closes on its ANSWERS row, and that is checked by
    name rather than waved through: this language posts the question at the
    foot of the page under a rule, so its last row is the entry itself."""
    ends = {}
    for lang in LANGS:
        if lang in MODAL_KEEPS_ONLY_THE_HEAD:
            # A CONFIRM WITH NO PAGE BEHIND IT HAS NO EXTENT TO CLOSE: this
            # language's question IS the surface, so "where does the modal
            # end" is answered by the screen. Its citation is asserted here
            # and again in `test_corgis_confirm_keeps_the_mode_strip_and_
            # nothing_else`.
            assert "the board is gone" in LG.MODAL_BORDER_REFUSED[lang], lang
            continue
        rows = (FRAMES / f"{lang}_S4.txt").read_text(
            encoding="utf-8").rstrip("\n").split("\n")
        first, last = confirm_span(lang)
        ends[lang] = rows[last].strip()
        assert ends[lang], (lang, first, last, "the band ends on a blank row")
    assert len(ends) == len(LANGS) - len(MODAL_KEEPS_ONLY_THE_HEAD), ends
    # inc72 (C2): ledger's confirm CLOSES ON ITS OWN RULE now. It used to end
    # on the answers row, because it opened on a rule and closed on nothing --
    # so the posting's lower limit was the edge of the terminal and `(Delete)`
    # was the last row a reader can see. Both halves are asserted: the band
    # ends on the sub rule, and the answers are no longer the last thing on
    # the sheet.
    assert set(ends["ledger"]) == {"─"}, ends["ledger"]
    assert set(ends["swiss"]) == {"─"}, ends["swiss"]


def test_swisss_rejected_field_has_a_wall_paper_and_a_closer():
    """RULING C's FOLLOW-THROUGH (orchestrator, 2026-09-07): *the channel C
    freed on swiss gets filled: the invalid text field has a wall, paper and a
    closer from swiss's own alphabet.*

    inc52 took `╲` — half this language's `DANGER_FORM` — off the rejected
    field's wall and put the doubled stroke there, which was right. Nothing
    moved into the channel that opened: `swiss_S2` row 6 read `║12/09/26`,
    one wall and eight characters, no paper and no closer. *How far does the
    date field go* had no answer, and the frame had traded a wrong answer for
    none.

    THE REJECTED FIELD IS NOW THE ONE FIELD IN THIS LANGUAGE THAT SPENDS ALL
    THREE CELLS, and all three come from the stroke ladder it already owns
    (`┆ │ ┃ █` and the doubled `║`). Asserted here as the thing a reader does:
    the row has a first cell, a last cell, and something between them that is
    neither the value nor air."""
    k = LG.kit("swiss")
    wall, paper, closer = k.part_glyph("main", LG.INVALID, "textfield")
    assert (wall, closer) == ("║", "║"), (wall, closer)
    assert paper == "┆", paper          # the lightest stroke of the ladder
    # every cell of the seat is a weight this language already spends at
    # this very part -- no new mark entered the alphabet
    ladder = {ch for slot in k.PART_GLYPHS["textfield.main"].values()
              for ch in slot if ch != " "}
    assert {wall, paper, closer} <= ladder, (wall, paper, closer, ladder)
    # and the DANGER_FORM is still nowhere near it (ruling C, inc52)
    assert not ({wall, paper, closer} & set(k.DANGER_FORM)), k.DANGER_FORM
    # the shipped frame: a wall, the value, the paper, a closer
    row = [r for r in (FRAMES / "swiss_S2.txt").read_text(
        encoding="utf-8").split("\n") if "12/09/26" in r][0].rstrip()
    assert row.lstrip().startswith("due•"), row
    assert row.endswith(closer), row
    assert row.count(paper) > 10, row


# ---------------------------------------------------------------------------
# inc67 (rework-6b) — K5: the quantity widgets join set B, and a fill cell is
# not a meaning mark
# ---------------------------------------------------------------------------
#: RULING A, AMENDED (orchestrator, 2026-09-07, on the operator's delegation),
#: verbatim:
#:
#:     "the census's B set reaches every quantity widget: slider, bar,
#:      scrollbar, meter, sparkline, pager, mascot. Their fill and track cells
#:      are chrome; a fill cell may not be a meaning mark of its language."
#:
#: THE SEATS A QUANTITY IS FILLED AT. Three come out of `PART_GLYPHS` — the
#: `indicator` of the slider, the bar and the scroll bar, which is the PAGER
#: (`screens.s1` calls `k.scrollbar`) — and three out of `Kit.quantity_glyphs`,
#: the declaration inc67 adds for the widgets drawn outside the tables.
#:
#: THE FILL AND NOT THE TRACK, which is the ruling's own word ("a fill cell
#: may not be a meaning mark") and is the same narrowing the opener law makes.
#: A track is the ground a reading is laid on and three languages spend their
#: calm rung on it deliberately — corgi's two-cell `▁▁`, naught's `◦`,
#: prism's `⣀` — while the FILL is the datum, the part that grows, the part a
#: reader is asked to judge an amount from. A language may lay a quantity on
#: its own ground; it may not say "this much" with the cell it says "this is
#: an error" with.
QUANTITY_FILL_SEATS = ("slider.indicator", "bar.indicator",
                       "scrollbar.indicator")
DECLARED_FILL_SEATS = ("meter.fill", "spark.peak", "mascot.pixel")


#: THE EXEMPTION, BY NAME AND WITH ITS CITATION — the only one this law takes,
#: and the ruling names its shape: "exemptions by name only where the doctrine
#: says the meter IS the severity device".
#:
#: TWO LANGUAGES DRAW SEVERITY AS A QUANTITY AND SAY SO IN THEIR OWN KITS.
#: For them a meter filled with the top rung is not a collision, it is the
#: same instrument read twice — which is the argument `DANGER_IS_THE_TOP_RUNG`
#: already carries for the danger form, one axis over.
#:
#: IT IS NOT A BLANKET AND THE FRAME IS WHY. Ruling A's own condition is that
#: an exemption "leave the opener of a control distinct from an error rung IN
#: THE FRAME". `prism_S3` puts nine cells of the slider's fill four rows above
#: the destructive button, so the SLIDER does not get it and inc67 moved the
#: slider instead; `prism_S1`'s pager drew the same cell to say "you are
#: here", so the thumb does not get it either. What is exempt is what the
#: doctrine actually claims: the METER, and prism's readbar, which is that
#: same ember read by `component_cells` and has no grip at all.
THE_METER_IS_THE_SEVERITY_DEVICE = {
    ("prism", "meter.fill"):
        "inc59: 'the ember is read from the BOTTOM'. LEVELS is the ember's "
        "own ramp read as three rungs, and DANGER_IS_THE_TOP_RUNG already "
        "names its top here. The meter and the ladder are one device.",
    ("prism", "bar.indicator"):
        "the readbar is that same ember through `component_cells`; it has no "
        "grip (`actuator(\"bar\")` is None), so nobody sets it and it is told "
        "to you. PROTOTYPE-inheritors-3.md 2.10 judges prism_S5's readbar "
        "correct BY NAME ('aqui la rampa se llena por lo pesado').",
    ("corgi", "meter.fill"):
        "inc58: 'THE BANK IS THE READING, THE PANEL IS THE MILLED METAL'. "
        "LEVELS is the segment bank at three heights, so a segment meter "
        "drawn on the bank is the bank doing its one job.",
}


#: WHAT STILL FILLS WITH A MEANING, COUNTED PER LANGUAGE — the same bargain
#: `MEANING_AT_AN_OPENER` and `MEANING_AT_A_NAMED_SEAT` make, and inc48's own
#: words about the first roster it wrote: "IT IS A MEASUREMENT, NOT A PASS."
#: A row is `(seat, glyph)`, deduped across states, because a cell a language
#: draws at a seat in four states is one declaration seen four times.
#:
#: THE FOUR FRAMES THE ROUND NAMED ARE FIXED AND THE REST ARE HERE. 22 rows
#: before this increment, 16 after; the six declarations that moved are:
#:
#:   naught  meter.fill        the lit dot -> the CHARGED dot (`NA.CHARGE`).
#:                             `dot_meter` filled with `NA.ON`, this kit's
#:                             error rung and danger byte, so `naught_S1` row
#:                             13 was thirteen of them and row 23's overdue
#:                             leader was two more. The ladder COUNTS lit
#:                             dots; the meter CHARGES them.
#:   corgi   MASCOT_PIXEL      the block base's full cell -> the shade ramp's
#:                             top step. Eighteen cells of the error rung
#:                             drawn as a creature in `corgi_S1` and
#:                             `corgi_S6`.
#:   corgi   PANE_RULE         the same cell twenty-five rows tall down the
#:                             middle of `corgi_S1`. This law does not see a
#:                             pane rule; the census does, and inc67 declared
#:                             it there.
#:   prism   slider.main       the slider takes the toggle's top-carved
#:   prism   slider.indicator  tables — inc59's own split ("a control is read
#:                             from the TOP") carried out for the second
#:                             control that has a grip.
#:   prism   scrollbar.indicator  the shaft had left the ember and the thumb
#:                             had not.
#:
#: WHAT EACH REMAINING ROW IS, so nobody has to re-derive it:
#:
#:   naught     3  `slider.indicator` and `bar.indicator` and the creature's
#:                 own pixel, all the lit dot. The lattice IS this language,
#:                 and PROTOTYPE-inheritors-3.md 2.8 calls that face the best
#:                 thing on `naught_S6`. Named, not moved.
#:   corgi      6  the slider's and the bar's two heights and the pager's top
#:                 segment, all three the driven bank; plus the spark's peak,
#:                 which is L6 and belongs to it.
#:   swiss      3  the hairline meter's heavy rule, the spark's, and the dead
#:                 scroll thumb's light one. L6 in this language is the whole
#:                 quantity family: the severity ladder IS the weight ladder.
#:                 Not exempted, because swiss's own doctrine calls that
#:                 ladder a HIERARCHY device and not a quantity one — the day
#:                 somebody argues the other way, this is where it goes.
#:   prism      1  the mascot's pixel. The creature is drawn through the
#:                 braille base and its pixel is that base's terminal cell;
#:                 moving it means either a second base for one drawing or no
#:                 creature. `prism_S4` puts eight of them three rows under
#:                 the destructive answer, so it is a real row and it stands.
#:   solari     1  the pager's thumb, which is `DANGER_FORM`'s lower half —
#:                 one cell of a two-cell hatch whose other half is nowhere
#:                 near it. The weakest row on this roster, and still a row.
#:   blueprint  2  the pager's and the spark's heavy line type. The same
#:                 shape as swiss: a line-weight ladder spent on severity and
#:                 on quantity at once.
FILL_IS_NOT_A_MEANING = {"naught": 3, "corgi": 6, "instrument": 0, "swiss": 3,
                         "industrial": 0, "nord": 0, "darkside": 0, "prism": 1,
                         "ledger": 0, "solari": 1, "blueprint": 2}


#: HOW MANY OF THE FOUR DECLARED QUANTITY CLAUSES EACH LANGUAGE ANSWERS —
#: `meter.fill`/`meter.track` as one, `spark.peak`, `spark.floor`,
#: `mascot.pixel`. A roster and not a constant, because the absences are
#: DECLARATIONS and each has a reason on its kit:
#:
#:   swiss, darkside, ledger  3  no creature — "swiss renounces it", "identity
#:                               is the doodle, recessive", "a ledger keeps no
#:                               pet". Four kits renounce the mascot; the
#:                               fourth is solari.
#:   blueprint                3  no meter FILL — `dimension` marks a height
#:                               and never blocks it in, so it declares an
#:                               opener and a closer instead. It is one of the
#:                               two `RAMPLESS_METERS`.
#:   solari                   0  the other `RAMPLESS_METER`, and the only kit
#:                               with nothing at all here: an odometer's
#:                               quantity is a row of FIGURES, its spark is
#:                               the one branch of `Kit.spark` that never
#:                               reaches a ramp, and it keeps no pet either.
QUANTITY_SEATS_ANSWERED = {"naught": 4, "corgi": 4, "instrument": 4,
                           "swiss": 3, "industrial": 4, "nord": 4,
                           "darkside": 3, "prism": 4, "ledger": 3,
                           "solari": 0, "blueprint": 3}


def meaning_marks_at_a_fill(lang: str) -> list[tuple]:
    """Every cell a quantity widget FILLS with that this language also spends
    on severity, danger or obligation, as `(seat, glyph, hit cells)`.

    DEDUPED ACROSS STATES, unlike the two seat laws, and the reason is the
    unit: a slider's indicator wearing one cell in four control states is ONE
    declaration seen four times, and counting it four times would make a
    roster that moves whenever `component_states` grows."""
    k = LG.kit(lang)
    meanings = _seat_meanings(k, lang)
    out = set()
    for seat in QUANTITY_FILL_SEATS:
        if (lang, seat) in THE_METER_IS_THE_SEVERITY_DEVICE:
            continue
        comp, part = seat.split(".")
        for st in LG.component_states(comp):
            glyph = k.part_glyph(part, st, comp)
            hit = _cells(glyph) & meanings
            if hit:
                out.add((seat, glyph, "".join(sorted(hit))))
    declared = k.quantity_glyphs()
    for seat in DECLARED_FILL_SEATS:
        if (lang, seat) in THE_METER_IS_THE_SEVERITY_DEVICE:
            continue
        glyph = declared.get(seat, "")
        hit = _cells(glyph) & meanings
        if hit:
            out.add((seat, glyph, "".join(sorted(hit))))
    return sorted(out)


@pytest.mark.parametrize("lang", LANGS)
def test_a_fill_cell_is_never_a_meaning_mark(lang):
    """K5, and the surface PROTOTYPE-inheritors-3.md 0b called the largest
    uncovered one in the corpus.

    Every law in this file reads `PART_GLYPHS`, `FIELD_LEAD` or
    `IDENT_GLYPHS`. The meter, the sparkline and the mascot are drawn outside
    all three, and the slider, the bar and the scroll bar were declared inside
    `PART_GLYPHS` but excluded from the census's set B by the operator's own
    request — so `MEANING_AT_AN_OPENER` and `MEANING_AT_A_NAMED_SEAT` could
    both read ZERO for eleven languages while three of the round's eight new
    `rework` verdicts lived in exactly the widget nobody was reading:

        naught_S1  row 13   thirteen lit dots — `LEVELS["error"]` and the
                   `DANGER_FORM` byte for byte — ten rows above a task whose
                   overdue leader is the same cell.
        corgi_S1            forty-seven full blocks, none of them a danger:
                   twenty-five are the partition, eighteen are a creature, two
                   are the pager's current page.
        prism_S1   row 31   the pager's window drawn in the ember's top cell.
        prism_S3   row 16   nine of the same cell, four rows above
                   `Delete all` set in it.

    A ROSTER AND NOT A ZERO, on inc48's precedent. The four frames the round
    named are fixed at their declarations; sixteen rows remain, every one of
    them written out at `FILL_IS_NOT_A_MEANING` with the language that owns it
    and the objection it belongs to (L6 carries five of the sixteen). The
    number can only move when somebody edits it."""
    assert len(meaning_marks_at_a_fill(lang)) == FILL_IS_NOT_A_MEANING[lang], \
        (lang, meaning_marks_at_a_fill(lang))


def test_the_fill_law_goes_red_on_the_declarations_inc67_moved(monkeypatch):
    """TEETH, on the REAL declarations this increment changed — three arms,
    each restoring one of them and naming the seat it comes back at, plus a
    vacuity check on the exemption.

    A law asserted only against the code that satisfies it is a law nobody has
    watched fail."""
    for lang in LANGS:
        assert (len(meaning_marks_at_a_fill(lang))
                == FILL_IS_NOT_A_MEANING[lang]), lang

    # ARM ONE — naught's meter fills with the lit dot again, which is what
    # `dot_meter` did for the whole programme. The row must come back at
    # `meter.fill` and nowhere else, and it must name that cell.
    monkeypatch.setitem(LG.METER_CELLS, "dotgrid",
                        (LG.NA.ON, LG.NA.OFF, None, None))
    hits = [h for h in meaning_marks_at_a_fill("naught")
            if h[0] == "meter.fill"]
    assert hits == [("meter.fill", LG.NA.ON, LG.NA.ON)], hits
    assert (len(meaning_marks_at_a_fill("naught"))
            == FILL_IS_NOT_A_MEANING["naught"] + 1)
    monkeypatch.undo()

    # ARM TWO — prism's pager thumb goes back to the ember's top: `prism_S1`
    # row 31 verbatim.
    tbl = dict(LG.Prism.PART_GLYPHS["scrollbar.indicator"])
    tbl[LG.DEFAULT] = "⣿"
    monkeypatch.setitem(LG.Prism.PART_GLYPHS, "scrollbar.indicator", tbl)
    hits = [h for h in meaning_marks_at_a_fill("prism")
            if h[0] == "scrollbar.indicator"]
    assert hits == [("scrollbar.indicator", "⣿", "⣿")], hits
    monkeypatch.undo()

    # ARM THREE — corgi's creature goes back to the block base's full cell.
    # It is the MASCOT seat and not the pane rule: a pane rule is chrome the
    # census reads and this law does not, which is why inc67 declared it
    # there and not here.
    monkeypatch.setattr(LG.Corgi, "MASCOT_PIXEL", "")
    hits = [h for h in meaning_marks_at_a_fill("corgi")
            if h[0] == "mascot.pixel"]
    assert hits == [("mascot.pixel", "█", "█")], hits
    monkeypatch.undo()

    # AND THE EXEMPTION IS NOT VACUOUS: empty it and the four rows it covers
    # come back, in the two languages it names and in no others.
    before = {l: len(meaning_marks_at_a_fill(l)) for l in LANGS}
    monkeypatch.setitem(globals(), "THE_METER_IS_THE_SEVERITY_DEVICE", {})
    after = {l: len(meaning_marks_at_a_fill(l)) for l in LANGS}
    grew = {l: after[l] - before[l] for l in LANGS if after[l] != before[l]}
    assert grew == {"prism": 3, "corgi": 1}, grew
    monkeypatch.undo()

    for lang in LANGS:
        assert (len(meaning_marks_at_a_fill(lang))
                == FILL_IS_NOT_A_MEANING[lang]), lang


@pytest.mark.parametrize("lang", LANGS)
def test_a_quantity_widget_draws_what_it_declares(lang):
    """`Kit.quantity_glyphs()` IS BOUND TO THE DRAWING BY THIS LAW.

    A declaration nothing reads is dead metadata, and this contract has
    refused that at `GRIPS`, `CHECKABLE`, `VIEWED` and `IDENT_GLYPHS`. Two of
    the three declared seats are read by the drawing directly —
    `_meter_dotgrid` passes `meter.fill` and `meter.track` into
    `NA.dot_meter`, and `Kit.mascot` substitutes `MASCOT_PIXEL` — but the
    other eleven mechanisms spell their cells in eleven different structures
    (a braille bitmap, groups of five, a printed figure), so one `(fill,
    track)` pair read at the call site would have to be re-expanded inside
    each of them anyway. THE TABLE IS THE DECLARATION AND THIS IS WHAT MAKES
    IT TRUE: every widget is rendered at its floor and at its ceiling and the
    declared cells have to be the cells that came out.

    THE THREE CLAUSES:
      * the meter's declared FILL is drawn at 100 % and NOT at 0 %, and its
        declared TRACK is drawn at 0 % — so a mechanism that swapped its two
        cells goes red here as well as at the direction law;
      * the spark's declared PEAK is drawn for a series at its ceiling and its
        FLOOR for a series of zeros;
      * the mascot's declared PIXEL is drawn by `mascot()`, and a language
        that renounces the creature declares no pixel at all.

    `solari` DECLARES NOTHING, and the last assertion is why that is a fact
    and not a hole: an odometer's quantity is a row of FIGURES, it keeps no
    pet, and its spark is the one branch that does not route through a ramp.
    The one kit of the eleven whose whole quantity vocabulary is outside this
    law, asserted so that a ramp arriving there cannot arrive in silence."""
    k = LG.kit(lang)
    q = k.quantity_glyphs()
    asked = 0
    if "meter.fill" in q:
        floor = plain(k.meter(0, 100, [5, 4, 3, 4], 37)).split("\n")[0]
        ceil = plain(k.meter(100, 100, [5, 4, 3, 4], 37)).split("\n")[0]
        assert q["meter.fill"] in ceil, (lang, q["meter.fill"], ceil)
        assert q["meter.fill"] not in floor, (lang, q["meter.fill"], floor)
        assert q["meter.track"] in floor, (lang, q["meter.track"], floor)
        asked += 1
    for seat, series in (("spark.peak", [0, 5, 5]),
                         ("spark.floor", [0, 0, 0])):
        if seat not in q:
            continue
        drawn = plain(k.spark(series, 9, hi=5))
        assert q[seat] in drawn, (lang, seat, q[seat], drawn)
        asked += 1
    rows = [plain(r) for r in k.mascot()]
    if rows:
        assert q["mascot.pixel"] in "".join(rows), (lang, q, rows)
        asked += 1
    else:
        assert "mascot.pixel" not in q, (lang, q)
    assert asked == QUANTITY_SEATS_ANSWERED[lang], (lang, asked, q)


# ---------------------------------------------------------------------------
# inc68 (rework-6b) — K4: two states of one part are told apart on a declared
# channel, and ordered where the doctrine orders them
# ---------------------------------------------------------------------------
#: K4, open since `PROTOTYPE-inheritors-2.md` and named in all three rounds:
#: **no law in this corpus compares two states of the same part.** Every law
#: here reads a glyph against the MEANINGS, or one part against another, or a
#: frame against a fixture. Nothing asked the question a reader asks of a
#: control — *"is this one on or off?"* — which is a question about two rows
#: of ONE table.
#:
#: WHAT IT COST, twice, in frames:
#:   `blueprint_S3`  a switch's three states are `├─┤` / `├┤·` / `├╎┈`, told
#:                   apart by DASH COUNT at 2, 3 and 4. inc60's own packet:
#:                   "a un cell de 12 px se le está pidiendo al lector que
#:                   cuente guiones".
#:   `prism_S2`      inc59 rewrote a checkbox's two centres in one increment
#:                   and PRESERVED AN INVERSION between them — ticked drew the
#:                   empty well, unticked drew a mark in the box — and nothing
#:                   in eleven months of property tests could see it. inc64
#:                   wrote the first law that compares two states of one part
#:                   (`test_a_ticked_box_is_never_lighter_than_an_empty_one`),
#:                   which is one part, one pair of states, one direction.
#:                   This is the general one.
#:
#: THE CHANNEL IS RULING D'S FOUR AND NOTHING ELSE: COUNT, WEIGHT, POSITION,
#: DIRECTION. Distinct CODE POINTS is not a channel and that is the whole of
#: K2 — every one of the eleven already has pairwise-distinct glyphs in every
#: table (measured: zero duplicates in 11 kits), so a law that asked for
#: distinctness would pass everywhere and say nothing.
def state_channel(g1: str, g2: str) -> str | None:
    """Which of ruling D's four channels separates two glyphs, or `None`.

    Read in the order a reader reaches them:

      COUNT     the two are different LENGTHS — one is longer than the other,
                which is the coarsest thing an eye resolves in a run.
      POSITION  the same cells in a different order: a mark that MOVED.
      SHAPE     at least one differing cell is a different DRAWING from its
                partner (not in the same `HOMOGLYPH_FAMILIES` row). This is
                the channel ruling D calls a shape rather than a size, and it
                is what nine of the eleven spend.
      WEIGHT    every differing cell is its partner at another size or fill,
                AND this file has a measured ink order for the pair. A ladder
                that grows and fills in the same direction is a channel — the
                D-addendum says so by name for industrial's `▫▫ ▪▪ ■■`.

    `None` MEANS THIS FILE CANNOT NAME A CHANNEL, and — like `cell_ink` — that
    is a REFUSAL and not a pass. Two cells of one family with no measured
    weight between them are *"one drawing at two diameters"*, which ruling D
    says is no channel at all; and a pair this file has never weighed is a
    pair it may not certify (E2: the artefacts carry no font metric). The
    roster below is honest about which of the two each row is."""
    if len(g1) != len(g2):
        return "count"
    diff = [(a, b) for a, b in zip(g1, g2) if a != b]
    if not diff:
        return None
    if sorted(g1) == sorted(g2):
        return "position"
    for a, b in diff:
        if b not in _twins(a):
            return "shape"
    for a, b in diff:
        ia, ib = cell_ink(a), cell_ink(b)
        if ia is not None and ib is not None and ia != ib:
            return "weight"
    return None


#: WHAT STILL TELLS TWO OF ITS STATES APART BY SIZE OR FILL ALONE, counted per
#: language. `(part key, state, state)`, over the DECLARED table only — a
#: state a kit does not declare falls back through the chain and is the same
#: glyph on purpose, which is a declaration that the two states LOOK ALIKE and
#: is not this law's business.
#:
#:   naught     8  and it is the language, not a slip. Six seats tell two
#:                 states apart with a ring at another size or fill —
#:                 `◦`/`○` at the button, the checkbox and the field's paper,
#:                 `◉`/`◎` at the shared knob and the checkbox's, `○`/`◦` at
#:                 the radio's ground. `PROTOTYPE-inheritors-3.md` §2.8 is the
#:                 same finding read off `naught_S2` ("el radio y el checkbox
#:                 de este formulario se distinguen sólo por el diámetro y el
#:                 relleno de un círculo") and `spec.md` §11.5 already records
#:                 that this kit "has no unspent cell left". Closing these
#:                 means a second channel for this alphabet, which is a
#:                 language-level increment.
#:   darkside   1  `◎`/`◉` at the shared knob, default against focused — the
#:                 move inc49 made and this file's own census listed as
#:                 ACCEPTED under COUNT ("two concentric strokes against
#:                 one"). Ruling D amended reads a ring as a ring at any
#:                 fill, so the same move is now a row. Recorded as the
#:                 disagreement it is.
#:
#: SWISS IS ZERO AND IT WAS TWO UNTIL `■` WAS WEIGHED. Its button ladder is
#: `▫ ▪ ■`, which the D-addendum names as the shape that STANDS ("passes from
#: hollow to filled (weight) and grows (size) in the same direction"), and
#: this file had a weight for two of the three. That is a measurement being
#: supplied, not a law being loosened: the third weight is arithmetic on the
#: same ordinal scale, and without it the law was refusing a ladder the
#: ruling had already blessed.
STATES_TOLD_APART_BY_SIZE = {"naught": 8, "corgi": 0, "instrument": 0,
                             "swiss": 0, "industrial": 0, "nord": 0,
                             "darkside": 1, "prism": 0, "ledger": 0,
                             "solari": 0, "blueprint": 0}


def states_without_a_channel(lang: str) -> list[tuple]:
    """Every pair of DECLARED states of one part that no channel separates."""
    k = LG.kit(lang)
    out = []
    for key, table in sorted(k.PART_GLYPHS.items()):
        states = list(table)
        for i, s1 in enumerate(states):
            for s2 in states[i + 1:]:
                if state_channel(table[s1], table[s2]) is None:
                    out.append((key, s1, table[s1], s2, table[s2]))
    return out


@pytest.mark.parametrize("lang", LANGS)
def test_two_states_of_one_part_are_told_apart_on_a_channel(lang):
    """K4's first half, over every part table in every kit.

    A ROSTER AND NOT A ZERO, on the same precedent as `MEANING_AT_AN_OPENER`
    and `FILL_IS_NOT_A_MEANING`: nine of the eleven are clean, two are not,
    and both of those are a language whose whole alphabet is one drawing at
    several sizes. The number can only move when somebody edits it."""
    assert (len(states_without_a_channel(lang))
            == STATES_TOLD_APART_BY_SIZE[lang]), \
        (lang, states_without_a_channel(lang))


#: K4's SECOND HALF — "ordered where the doctrine orders them". Two kits
#: declare a state ladder in their own words and both are ARITHMETIC to read,
#: which is why these two and not the other nine: a braille cell's dots and a
#: dash glyph's dashes are properties of the code point, so no font metric is
#: needed and E2 does not reach them.
#:
#: PRISM'S FOUR, from inc59: "a control is read from the TOP" and "the ladder
#: climbs instead of dimming". Its four control states are cut from `⠄ ⠉ ⠛ ⠿`
#: — 1, 2, 4 and 6 dots — and the doctrine's order is DISABLED, DEFAULT,
#: FOCUSED, ACTIVE. inc59's own comment records what it replaced: walls that
#: ran `⣿` (8 dots) at rest, `⣷` (7) focused and `⣾` (7) active, "a control
#: that DIMMED when the reader arrived at it".
PRISM_LADDERS = ("radio.main", "button.main", "checkbox.main", "checkbox.knob")
PRISM_LADDER_ORDER = (LG.DISABLED, LG.DEFAULT, LG.FOCUSED, LG.ACTIVE)


def braille_dots(glyph: str) -> int:
    return sum(bin(ord(ch) - 0x2800).count("1") for ch in glyph
               if 0x2800 <= ord(ch) <= 0x28FF)


def test_prisms_control_ladder_climbs_in_its_declared_order():
    """K4's ordering clause, on the kit whose ladder is a dot count.

    NON-DECREASING ALONG THE ORDER AND STRICTLY UP END TO END, which is the
    weakest statement that still says "it climbs": two adjacent rungs may tie
    (`⣷` and `⣾` are both seven dots, one carved at the top and one at the
    bottom — a DIRECTION channel, and `state_channel` above is what asks that
    of them), but a control may never be dimmer at a later rung than at an
    earlier one, and the last rung must be brighter than the first."""
    k = LG.kit("prism")
    for key in PRISM_LADDERS:
        table = k.PART_GLYPHS[key]
        dots = [braille_dots(table[st]) for st in PRISM_LADDER_ORDER]
        assert dots == sorted(dots), (key, PRISM_LADDER_ORDER, dots)
        assert dots[0] < dots[-1], (key, dots)


#: BLUEPRINT'S THREE, from inc60: "a meaning is a LINE TYPE", and the three
#: horizontals this kit told apart were told apart by DASH COUNT — `╌` (two)
#: `LEVELS["warn"]`, `┄` (three) every dead INDICATOR, `┈` (four) every dead
#: GROUND. `blueprint_S3` was the frame — `├─┤` on, `├┤·` off, `├╎┈` dead —
#: and three rounds' objection (§2.7) is that counting dashes in a 12px cell
#: is not a channel a reader has. The law that stood here asserted only that
#: the ladder was MONOTONE ("if a reader can count at all, counting gives the
#: right answer"), which round four answered by measuring the three runs at
#: 1.24:1 in `dim`: a count you cannot resolve is not a channel however well
#: it is ordered.
#:
#: inc72 RETIRES THE COUNT, and it took TWO moves because the sheet has only
#: one dashed horizontal to give:
#:
#:   1. `┄` and `┈` leave the kit. The dead GROUND takes `╌`, the broken rule
#:      this sheet already flies as its CLIP flag, and the dead EXTENT takes
#:      `╏`, the dashed VERTICAL it already spends on dead terminators. What
#:      separates the two is DIRECTION — ruling D's fourth channel, and the
#:      one this sheet already spends on `╱` HELD against `╲` REFUSED.
#:   2. `LEVELS["warn"]` leaves `╌`. inc60 moved the dead runs off that cell
#:      BECAUSE it was the warn rung ("a dead thing is not a meaning", ruling
#:      (ii)); the only way to give it back to the dead runs was to move the
#:      meaning instead. The ladder counts CELLS DRAWN now — nothing / half /
#:      whole, `"  "` / `" ━"` / `"━━"` — which is COUNT, the channel
#:      `state_channel` reads first, and no cell gains a family.
#:
#: THE ROSTER IS THE HORIZONTALS THE KIT MAY STILL DRAW, so a fourth dash
#: count cannot come back in by the side door.
BLUEPRINT_DASHED_HORIZONTALS = {"╌"}
BLUEPRINT_DEAD_RUNS = {"main": "╌", "indicator": "╏"}


def test_blueprints_dead_runs_turn_instead_of_counting_dashes():
    """K4 in the frame, on the kit whose ladder was a dash count.

    FOUR CLAUSES, and each is one of the sentences above made checkable:

      1. the kit draws exactly ONE dashed horizontal, so there is no count
         left to make — `┄` and `┈` appear nowhere in any declared table;
      2. each dead run is the dashed VERTICAL the roster names, and the two
         are told apart by WEIGHT with the ground lighter than the extent;
      3. no dead run is the warn rung or its homoglyph, which is the whole of
         inc60's ruling (ii) and the reason those cells moved in the first
         place;
      4. and at the two seats that have terminators of their own, the dead
         datum is NOT the cell its own walls wear — a mark that equals its
         box is not a mark, and this is the failure the first draft made.

    THE LIVE RUNS ARE ASSERTED TOO, because the point of a direction channel
    is that both sides of it are horizontal-or-not on purpose: `─` is the live
    extent and `·` the live ground, and neither is a vertical."""
    k = LG.kit("blueprint")
    declared = "".join("".join(t.values()) for t in k.PART_GLYPHS.values())
    declared += "".join(k.LEVELS.values()) + "".join(k.DANGER_FORM)

    # 1 -- the dash COUNT is gone from the kit
    assert set("┄┈").isdisjoint(declared), sorted(set("┄┈") & set(declared))
    assert set("╌") <= BLUEPRINT_DASHED_HORIZONTALS
    assert {c for c in declared if c in "╌┄┈"} == BLUEPRINT_DASHED_HORIZONTALS

    # 2 -- the dead runs are the two the roster names, they differ, and the
    # knob a reader grips is a third cell again (this is what went red when
    # the first draft gave the track and the grip one mark)
    for part, cell in BLUEPRINT_DEAD_RUNS.items():
        assert k.PART_GLYPHS[part][LG.DISABLED] == cell, (part, cell)
    dead = [k.PART_GLYPHS[p][LG.DISABLED]
            for p in ("main", "indicator", "knob")]
    assert len(set(dead)) == 3, dead
    assert state_channel(BLUEPRINT_DEAD_RUNS["main"],
                         BLUEPRINT_DEAD_RUNS["indicator"]) is not None

    # 3 -- and no dead run is the warn rung, nor a cell of its family, which
    # is inc60's ruling (ii) unchanged: a dead thing is not a meaning
    warn = k.LEVELS["warn"].strip()[0]
    for cell in BLUEPRINT_DEAD_RUNS.values():
        assert cell != warn and cell not in _twins(warn), (cell, warn)
    # and the severity ladder counts CELLS: nothing, half the run, all of it
    rungs = [k.LEVELS[r] for r in ("info", "warn", "error")]
    assert len({len(r) for r in rungs}) == 1, rungs
    drawn = [len(r.strip()) for r in rungs]
    assert drawn == [0, 1, 2], (rungs, drawn)

    # 4 -- a dead datum is not its own walls
    for seat in ("checkbox.knob", "radio.knob", "textfield.main"):
        dead = k.PART_GLYPHS[seat][LG.DISABLED]
        assert len(dead) == 3 and dead[0] == dead[2], (seat, dead)
        assert dead[1] != dead[0], (seat, dead)

    # and the LIVE runs stayed horizontal, which is what makes the turn read
    assert k.PART_GLYPHS["indicator"][LG.DEFAULT] == "─"
    assert k.PART_GLYPHS["main"][LG.DEFAULT] == "·"


def test_the_dead_run_law_bites_on_the_declaration_blueprint_shipped(
        monkeypatch):
    """TEETH. Put inc60's dash-count ladder back on the real kit and the law
    goes red on clause 1 — and the OLD law's own assertion (the ladder is
    monotone in its count) is still true of it, which is the point: an
    ordering law could never have caught this."""
    k = LG.kit("blueprint")
    before = dict(k.PART_GLYPHS["main"]), dict(k.PART_GLYPHS["indicator"])
    monkeypatch.setitem(k.PART_GLYPHS["main"], LG.DISABLED, "┈")
    monkeypatch.setitem(k.PART_GLYPHS["indicator"], LG.DISABLED, "┄")
    monkeypatch.setitem(k.LEVELS, "warn", "╌╌")
    counts = {"╌": 2, "┄": 3, "┈": 4}
    rungs = ["╌", "┄", "┈"]
    assert [counts[r] for r in rungs] == sorted(counts.values())
    with pytest.raises(AssertionError):
        test_blueprints_dead_runs_turn_instead_of_counting_dashes()
    monkeypatch.undo()
    assert (dict(k.PART_GLYPHS["main"]),
            dict(k.PART_GLYPHS["indicator"])) == before


def test_the_state_channel_law_goes_red_on_a_real_table(monkeypatch):
    """TEETH, on the two declarations two increments of this programme moved,
    plus a vacuity arm on the channel reader itself.

    ARM ONE is inc59's, restored: prism's checkbox walls before that
    increment ran `⣿` at rest, `⣷` focused and `⣾` active — the kit's own
    comment calls it "a control that DIMMED when the reader arrived at it".
    The ordering law goes red and names the table.

    ARM TWO is inc64's frame, the one nothing in this repo could see: the two
    checkbox centres swapped back, so ticking a box TAKES INK AWAY. It is red
    at the ordering law's sibling (`test_a_ticked_box_is_never_lighter_than_
    an_empty_one`) and it leaves the CHANNEL law green, which is the point —
    an inversion is an ORDER defect and not a channel defect, and the two
    clauses of K4 are two clauses for that reason.

    ARM THREE is the channel reader itself: swap naught's radio ground for a
    ring one size along and the roster grows by exactly one row."""
    for lang in LANGS:
        assert (len(states_without_a_channel(lang))
                == STATES_TOLD_APART_BY_SIZE[lang]), lang
    test_prisms_control_ladder_climbs_in_its_declared_order()

    # ARM ONE — the pre-inc59 walls, verbatim from that increment's comment
    tbl = dict(LG.Prism.PART_GLYPHS["checkbox.main"])
    tbl[LG.DEFAULT], tbl[LG.FOCUSED], tbl[LG.ACTIVE] = "⣿⠀⣿", "⣷⠀⣷", "⣾⠀⣾"
    monkeypatch.setitem(LG.Prism.PART_GLYPHS, "checkbox.main", tbl)
    with pytest.raises(AssertionError):
        test_prisms_control_ladder_climbs_in_its_declared_order()
    monkeypatch.undo()

    # ARM TWO — inc64's inversion: an ORDER defect that is not a CHANNEL one
    box = dict(LG.Prism.PART_GLYPHS["checkbox.main"])
    knob = dict(LG.Prism.PART_GLYPHS["checkbox.knob"])
    for st in (LG.DEFAULT, LG.FOCUSED, LG.ACTIVE):
        box[st], knob[st] = knob[st], box[st]
    monkeypatch.setitem(LG.Prism.PART_GLYPHS, "checkbox.main", box)
    monkeypatch.setitem(LG.Prism.PART_GLYPHS, "checkbox.knob", knob)
    assert len(states_without_a_channel("prism")) == 0, "still a channel"
    with pytest.raises(AssertionError):
        test_a_ticked_box_is_never_lighter_than_an_empty_one("prism")
    monkeypatch.undo()

    # ARM THREE — the channel reader itself, on the seat inc68 just repaired.
    # naught's scroll shaft is `◦` live and `⋅` dead: a ring against a dot,
    # two DRAWINGS, so `state_channel` calls it SHAPE. Put the dead shaft on a
    # ring one size along and the channel is diameter and nothing else, which
    # is the whole of ruling D. Exactly one new row, and it names the part.
    tbl = dict(LG.Naught.PART_GLYPHS["scrollbar.main"])
    assert state_channel(tbl[LG.DEFAULT], tbl[LG.DISABLED]) == "shape"
    tbl[LG.DISABLED] = "○"
    monkeypatch.setitem(LG.Naught.PART_GLYPHS, "scrollbar.main", tbl)
    grew = states_without_a_channel("naught")
    assert len(grew) == STATES_TOLD_APART_BY_SIZE["naught"] + 1, grew
    assert [r for r in grew if r[0] == "scrollbar.main"] ==         [("scrollbar.main", LG.DEFAULT, "◦", LG.DISABLED, "○")], grew
    monkeypatch.undo()

    for lang in LANGS:
        assert (len(states_without_a_channel(lang))
                == STATES_TOLD_APART_BY_SIZE[lang]), lang


# ---------------------------------------------------------------------------
# inc69 (rework-6b) — L2: air is not a state
# ---------------------------------------------------------------------------
#: RULING L2 (orchestrator, 2026-09-07, on the operator's delegation),
#: verbatim: **"a disabled control always carries a mark; air is not a
#: state."**
#:
#: THE FRAME, THREE ROUNDS RUNNING. `swiss_S2` row 18 read
#: `     Save        ▫   Cancel` — the button the reader is meant to press was
#: the only control on the screen with no mark at all, and it stood directly
#: above `Save is held until due parses`, which is a LEGEND. Tapar la fila y
#: decir cuál de los dos renglones es un control: sin respuesta. `spec.md`
#: §11.3 has admitted it word for word since `rework-3`; `PROTOTYPE-
#: inheritors.md`, `-2` and `-3` each named it; six batches went past it, and
#: the only thing that changed in that row was that `Cancel` GAINED a mark.
#:
#: IT WAS A DECISION AND NOT AN OVERSIGHT, which is why it needed a ruling.
#: inc38 wrote it down: *"DISABLED is air, and it is the one decision that is
#: not the ladder. Nothing in this alphabet is lighter than `·` except a
#: dashed RULE (`┆ ╎ ┈`) — the shape being given up. So the mark is simply not
#: set… A control nobody may press is a word, and that is what this language
#: would have said anyway."* Two things are wrong with the last sentence and
#: the ruling names the second: a word is what a LEGEND is too, and the shape
#: was not given up — this kit spends a dashed rule at five dead seats.
#:
#: THE LAW IS OVER ALL ELEVEN AND IT IS TWO CLAUSES, because "air" can happen
#: two ways: a kit can DECLARE nothing, and a composer can pad a declaration
#: out of the frame at a width nobody rendered.
AIR = " ⠀"          # the ASCII space and U+2800, the same pair everything else here calls blank


def declared_air(lang: str) -> list[tuple]:
    """`(component, part, state)` for every seat this kit draws as nothing.

    Read through `part_glyph`, so a state a kit does not declare is judged on
    the glyph it actually FALLS BACK to — a fallback that is air is still air
    on the screen, and this law is about the screen."""
    k = LG.kit(lang)
    out = []
    for comp in sorted(LG.COMPONENT_PARTS):
        for part in LG.COMPONENT_PARTS[comp]:
            for st in LG.component_states(comp):
                if not k.part_glyph(part, st, comp).strip(AIR):
                    out.append((comp, part, st))
    return out


@pytest.mark.parametrize("lang", LANGS)
def test_no_control_state_is_drawn_as_air(lang):
    """L2's first clause, over every seat of every component in every kit.

    ONE SEAT IN THE WHOLE CORPUS FAILED IT and it is the one the round named:
    swiss's `button.main[DISABLED]`, four spaces. Every other kit — including
    the four that renounce a mascot, the two whose meters draw no ramp and the
    one whose severity ladder is words — marks every state of every part."""
    assert declared_air(lang) == [], (lang, declared_air(lang))


#: THE WIDTHS. A button's seat is split in half and the caller's word stands
#: between the halves, so a mark that only survived at the width somebody
#: happened to render would be a mark that vanishes when a dialog grows. Three
#: widths, and they are the three `test_swiss_puts_no_wall_around_a_button_at_
#: any_width` already argues for: below the label, at the dialog's own, and at
#: swiss's `MEASURE_MIN` — *"the only width anyone tested was the only width
#: anyone calls"*.
L2_WIDTHS = (1, 10, 24)


@pytest.mark.parametrize("lang", LANGS)
def test_no_control_state_renders_as_air_at_any_width(lang):
    """L2's second clause: the DRAWN row, with the caller's own text removed.

    A declaration is not a rendering. `Kit.button` centres the label in a
    field the caller sizes, and `Kit.textfield` lays the value on the paper —
    so the question this clause asks is the reader's: **with the words taken
    away, is there anything left that says a control is here?**

    THE WORD IS REMOVED AND NOT SEARCHED AROUND, because a label can contain
    anything: `plain(row).replace(word, "")` and then `.strip(AIR)`. What is
    left is the language's own cells, and there has to be at least one."""
    k = LG.kit(lang)
    word, value = "Cancel", "12/09/26"
    for st in LG.component_states("button"):
        for w in L2_WIDTHS:
            row = plain(k.button(word, w, st)).replace(word, "")
            assert row.strip(AIR), (lang, "button", st, w, repr(row))
    for st in LG.component_states("textfield"):
        for w in L2_WIDTHS:
            row = plain(k.textfield(value, None, w, st)).replace(value, "")
            assert row.strip(AIR), (lang, "textfield", st, w, repr(row))


def test_the_air_law_goes_red_on_the_declaration_inc69_moved(monkeypatch):
    """TEETH, on the REAL declaration — swiss's own pre-inc69 seat, four
    spaces, restored byte for byte.

    THREE ARMS, and the third is the one that matters. Arm one restores the
    seat and the DECLARED clause goes red, naming swiss's button and the
    DISABLED state and nothing else. Arm two puts a mark back that is present
    in the DECLARATION but padded away by the composer — a single cell in the
    CLOSING half of a seat whose opening half is air — and the declared clause
    goes GREEN while the rendered clause goes red, which is why L2 is two
    clauses and not one. Arm three is the vacuity check: with the shipped
    declarations, exactly zero of the eleven have an air seat, and the
    assertion that would fire if the reader stopped reading anything is the
    count of seats it visited."""
    for lang in LANGS:
        assert declared_air(lang) == [], lang

    # ARM ONE — inc38's declaration, verbatim
    tbl = dict(LG.Swiss.PART_GLYPHS["button.main"])
    tbl[LG.DISABLED] = "    "
    monkeypatch.setitem(LG.Swiss.PART_GLYPHS, "button.main", tbl)
    assert declared_air("swiss") == [("button", "main", LG.DISABLED)], \
        declared_air("swiss")
    assert all(declared_air(o) == [] for o in LANGS if o != "swiss")
    with pytest.raises(AssertionError):
        test_no_control_state_renders_as_air_at_any_width("swiss")
    monkeypatch.undo()

    # ARM TWO — a mark that EXISTS and does not survive the composer. The
    # seat is read at its two halves and the opening half is what leads the
    # field, so a mark parked in the closing half is declared and unpainted
    # at every width `Kit.button` pads.
    tbl = dict(LG.Swiss.PART_GLYPHS["button.main"])
    tbl[LG.DISABLED] = "   ╎"
    monkeypatch.setitem(LG.Swiss.PART_GLYPHS, "button.main", tbl)
    assert declared_air("swiss") == [], "the declared clause cannot see it"
    monkeypatch.undo()

    # ARM THREE — the reader is not vacuous: it visits every seat the
    # registry derives, which is a number somebody has to edit.
    seats = sum(len(LG.COMPONENT_PARTS[c]) * len(LG.component_states(c))
                for c in LG.COMPONENT_PARTS)
    assert seats == 110, seats
    for lang in LANGS:
        assert declared_air(lang) == [], lang


# ---------------------------------------------------------------------------
# inc70 (rework-6b) — `mut` is body text
# ---------------------------------------------------------------------------
#: THE RULING (orchestrator, 2026-09-07, on the operator's delegation):
#: **"`mut` is body text and must reach 4.5:1 against the declared ground in
#: every kit, with the ladder `ink > mut > dim` kept ordered."**
#:
#: WHERE IT CAME FROM. inc63 taught the exporter to read the kit's DECLARED
#: ground instead of counting pixels (ruling E4), and its own law asserts
#: `contrast(ink, ground) >= 4.5` for all eleven. Writing that law is what
#: turned up the next one: §16.7 measured `mut` against the same grounds and
#: found five kits under the floor — *"and most body text in these sheets is
#: `mut`, not `ink`"* — then declined to fix it, in writing: *"The ruling names
#: `ground` and `ink`, so the law asks about `ground` and `ink`. Measured while
#: writing it, not fixed, and not asserted: moving a `mut` is a design change
#: in five kits at once."* This increment is that ruling and that change.
#:
#: THE ORDER CLAUSE IS NOT DECORATION. A kit could clear 4.5 by lightening
#: `mut` past `ink`, which would satisfy the floor and destroy the hierarchy
#: the three tokens exist to carry. Strict, so a tie is a failure too.
MUT_FLOOR = 4.5
INK_FLOOR = 4.5

#: THE ONE EXEMPTION, BY NAME, AND IT IS AN IMPOSSIBILITY PROOF rather than a
#: preference — the shape `DANGER_IS_THE_TOP_RUNG` and
#: `THE_GROUND_IS_NOT_A_MARK` already have in this file, with the measurement
#: that forced it.
#:
#: SOLARI PAINTS A SECOND GROUND. Its selected departure inverts to amber
#: (`#f5a300`) and `verify_language.py` holds every glyph on that row to 2.5:1
#: against the ground it actually sits on — a guard that exists because an
#: earlier draft of this kit printed `#f5a300` on `#f5a300`, 1:1, and its calm
#: fields came out at 1.8:1. **Lightening `mut` to clear 4.5:1 against
#: `#0b0b0c` takes it to 2.10:1 against the band, and the gate caught it.**
#:
#: NO GREY CAN DO BOTH, and the arithmetic says so rather than the eye:
#:
#:     4.5:1 against #0b0b0c  ->  L(mut) >= 4.5 * (0.00338 + 0.05) - 0.05
#:                            ->  L(mut) >= 0.19021
#:     2.5:1 against #f5a300  ->  L(mut) <= (0.44900 + 0.05) / 2.5 - 0.05
#:                            ->  L(mut) <= 0.14960
#:
#: and a `mut` LIGHTER than the amber would need L >= 1.1475, off the top of
#: the scale. The two floors do not overlap.
#:
#: WHAT SATISFYING THE RULING HERE WOULD ACTUALLY TAKE: a per-row ink for the
#: banded row. `_sched_row` cannot see that a row is selected — the band is
#: painted by the app's own CSS and the row is composed with a foreground
#: only — so the tagged fields (`stat`, `proj`, `pri`) sit on whatever ground
#: is behind them while the `due` field, which carries its own face through
#: `Kit.cell`, is immune. That is a design decision about solari's selection
#: mechanism and no ruling has taken it. **The exemption is a request for one,
#: not a verdict**, and it is asserted below so it cannot quietly widen.
THE_BAND_IS_A_SECOND_GROUND = {
    "solari": "`#6e6a60` at 3.65:1 — the selected row inverts to `#f5a300` "
              "and `verify_language.py` holds every glyph on it to 2.5:1. "
              "The two floors do not overlap (see the proof above); "
              "satisfying one breaks the other, and the resolution is a "
              "per-row ink for the band, which is not a token change.",
}


#: `dim` IS NOT ASKED FOR 4.5 AND IT IS NOT ASKED FOR 3.0 EITHER — it is
#: MEASURED, per kit, and the number is the record.
#:
#: The brief that carried the ruling proposed a third clause, `dim >= 3.0:1`
#: (WCAG 1.4.11, the non-text floor). **Measured first, as this batch measures
#: everything: TEN OF THE ELEVEN are under it, most of them far under.** It is
#: not a defect that ten kits failed to notice — `dim` is not text and it is
#: not a UI component boundary either:
#:
#:   naught     1.35   the UNLIT LATTICE. LANGUAGES.md §0, quoted at
#:                     `THE_GROUND_IS_NOT_A_MARK`: "the unlit grid is visible
#:                     ... that faint lattice IS the signature". A ground at
#:                     3:1 is not a ground.
#:   solari     1.20   the SEAM, "the ONLY divider" — one step off the flap
#:                     face by construction.
#:   blueprint  1.24   the paper's own grid.
#:   ledger     1.50   the dot leaders, which `PROTOTYPE-inheritors-3.md` §0a
#:                     names as the thing that was WRONGLY the most legible
#:                     element on the page when the exporter was broken.
#:   darkside   1.39 · nord 1.69 · corgi 1.71 · instrument 1.74 ·
#:   swiss      1.75 · industrial 1.96
#:   prism      3.25   the only one over, and not by design.
#:
#: SO THE CLAUSE IS A ROSTER AND NOT A FLOOR. Raising `dim` to 3.0 in ten kits
#: is a design change an order of magnitude larger than this increment's, in
#: the token every language spends its GROUND on, and no ruling has asked for
#: one. What is asserted is that the numbers do not move without somebody
#: editing them, and that `dim` stays BELOW `mut` in every kit — which is the
#: ladder clause doing the work the floor would have done badly.
DIM_AGAINST_GROUND = {
    "corgi": 1.71, "naught": 1.35, "instrument": 1.74, "swiss": 1.75,
    "industrial": 1.96, "nord": 1.69, "darkside": 1.39, "prism": 3.25,
    "ledger": 1.50, "solari": 1.20, "blueprint": 1.24,
}


@pytest.mark.parametrize("lang", LANGS)
def test_the_tone_ladder_is_legible_and_ordered(lang):
    """`ink` and `mut` clear WCAG 1.4.3 against the ground the kit DECLARES,
    and the three tones stay in order.

    THE GROUND IS THE KIT'S, not the terminal's and not the frame's most
    common colour — which is the whole of ruling E4 and is why this law could
    not have been written before inc63. `contrast()` here is the same WCAG
    relative-luminance function inc63's canvas law uses, on the same two
    hexes, so the two laws cannot disagree about what a ratio is."""
    t = LG.THEMES[lang]
    g = t["ground"]
    ink, mut, dim = (contrast(t[k], g) for k in ("ink", "mut", "dim"))
    assert ink >= INK_FLOOR, (lang, "ink", t["ink"], g, round(ink, 2))
    if lang in THE_BAND_IS_A_SECOND_GROUND:
        assert THE_BAND_IS_A_SECOND_GROUND[lang].strip(), lang
        assert mut < MUT_FLOOR, (lang, "the exemption is stale -- delete it")
    else:
        assert mut >= MUT_FLOOR, (lang, "mut", t["mut"], g, round(mut, 2))
    # THE LADDER IS ASKED OF ALL ELEVEN, exemption or not: a floor may be
    # unreachable, an ORDER never is.
    assert ink > mut > dim, (lang, round(ink, 2), round(mut, 2), round(dim, 2))


@pytest.mark.parametrize("lang", LANGS)
def test_dim_against_its_ground_is_measured_and_recorded(lang):
    """THE THIRD CLAUSE, AS A MEASUREMENT. See `DIM_AGAINST_GROUND` for why it
    is a roster and not a floor: ten of the eleven are under the non-text 3:1,
    and `dim` is a ground rather than a mark in most of them.

    Two decimals, because that is the precision the roster is written at and
    a law that pinned more would go red on a rounding."""
    t = LG.THEMES[lang]
    got = round(contrast(t["dim"], t["ground"]), 2)
    assert got == DIM_AGAINST_GROUND[lang], (lang, got)


def test_the_tone_ladder_law_goes_red_on_the_five_declarations_inc70_moved(
        monkeypatch):
    """TEETH, on the REAL hexes — the five `mut` values this increment moved,
    restored one at a time, each with the ratio it shipped at.

    AND THE ORDER CLAUSE HAS ITS OWN ARM, because it is the half a floor
    cannot catch: a `mut` lightened past `ink` clears 4.5:1 and inverts the
    hierarchy the three tokens exist to carry."""
    for lang in LANGS:
        test_the_tone_ladder_is_legible_and_ordered(lang)

    before = {"nord": ("#7b88a1", 3.50),
              "instrument": ("#6b7785", 4.26), "darkside": ("#737373", 4.43),
              "ledger": ("#6b6558", 4.45)}
    for lang, (hexes, ratio) in before.items():
        t = dict(LG.THEMES[lang])
        assert t["mut"] != hexes, (lang, "already the pre-inc70 value")
        t["mut"] = hexes
        monkeypatch.setitem(LG.THEMES, lang, t)
        assert round(contrast(hexes, t["ground"]), 2) == ratio, lang
        with pytest.raises(AssertionError):
            test_the_tone_ladder_is_legible_and_ordered(lang)
        for other in LANGS:
            if other != lang:
                test_the_tone_ladder_is_legible_and_ordered(other)
        monkeypatch.undo()

    # THE ORDER ARM — a `mut` that clears the floor and outranks `ink`
    t = dict(LG.THEMES["nord"])
    t["mut"] = t["ink"]
    monkeypatch.setitem(LG.THEMES, "nord", t)
    assert contrast(t["mut"], t["ground"]) > MUT_FLOOR, "the floor passes"
    with pytest.raises(AssertionError):
        test_the_tone_ladder_is_legible_and_ordered("nord")
    monkeypatch.undo()

    for lang in LANGS:
        test_the_tone_ladder_is_legible_and_ordered(lang)

    # AND THE EXEMPTION IS NOT VACUOUS EITHER WAY: it names exactly one kit,
    # that kit is really under the floor, and the law goes red the moment the
    # exemption is emptied — so nobody can leave a fixed kit sitting under a
    # by-name exemption, and nobody can widen the exemption in silence.
    assert set(THE_BAND_IS_A_SECOND_GROUND) == {"solari"}
    monkeypatch.setitem(globals(), "THE_BAND_IS_A_SECOND_GROUND", {})
    with pytest.raises(AssertionError):
        test_the_tone_ladder_is_legible_and_ordered("solari")
    for other in LANGS:
        if other != "solari":
            test_the_tone_ladder_is_legible_and_ordered(other)
    monkeypatch.undo()
    for lang in LANGS:
        test_the_tone_ladder_is_legible_and_ordered(lang)


# ---------------------------------------------------------------------------
# inc76 — THE RASTER.  E2, which three rounds asked for and none got.
#
# `PROTOTYPE-inheritors-4.md` §8.2: *"un ratio de contraste no es una prueba de
# legibilidad, y esta ronda no tiene mas que ratios ... el `.svg` no dice a que
# tamanio de celda ni con que fuente se va a renderizar"*.  The laws below are
# about the INSTRUMENT and about no kit: they exist so that when inc77 says a
# homoglyph pair differs by 3% of a cell, the cell is a real cell.
#
# READ AS BYTES, NOT IMPORTED, for the reason the metrics law above already
# gives: `prototypes/components/raster.py` reaches Textual through
# `render.py`, and this file reads the pictures off disk on purpose.  The
# declarations are read out of the raster's SOURCE and the pixels out of its
# PNGs, so the two can only drift by someone editing both.
# ---------------------------------------------------------------------------

RASTER = FRAMES / "png"

#: THE DECLARED BOX, restated here and checked against `raster.py`'s source —
#: the same bargain `test_this_files_picture_metrics_are_the_exporters` makes.
#: If the face or the size moves, every number inc77 published was measured at
#: a size that no longer exists, and this is where that gets said out loud.
_R_FACE, _R_PX, _R_CELL = "Cascadia Mono", 16, (9, 19)
_R_FALLBACK, _R_FALLBACK_CELLS = "Segoe UI Symbol", "⊖⊚⊛⋅"


def _raster_json(name: str) -> dict:
    import json
    return json.loads((RASTER / f"{name}.json").read_text(encoding="utf-8"))


def _png_size(name: str) -> tuple[int, int]:
    """Width and height out of the PNG's IHDR, without decoding the image.

    Sixteen bytes in, big-endian, and it is read by hand so the size law
    cannot be satisfied by whatever Pillow decides a truncated file is.
    """
    b = (RASTER / f"{name}.png").read_bytes()
    assert b[:8] == b"\x89PNG\r\n\x1a\n", (name, "not a PNG")
    return (int.from_bytes(b[16:20], "big"), int.from_bytes(b[20:24], "big"))


def _cells_of(side: dict):
    """`(x, y, glyph, fg, bg, bold, underline)` from the sidecar's runs."""
    for y, runs in enumerate(side["grid"]):
        for x0, text, fg, bg, bold, und in runs:
            for i, ch in enumerate(text):
                yield x0 + i, y, ch, fg, bg, bold, und


def _cell_pixels(im, side: dict, x: int, y: int) -> set:
    w, h = side["cell"]["w"], side["cell"]["h"]
    return {im.getpixel((x * w + dx, y * h + dy))
            for dx in range(w) for dy in range(h)}


def _rgb(hexed: str) -> tuple:
    return tuple(bytes.fromhex(hexed[1:]))


def test_the_rasters_declarations_are_the_ones_this_file_measures_against():
    """The face, the size, the cell and the fallback, read off the source."""
    src = (FRAMES / "raster.py").read_text(encoding="utf-8")
    assert f'FONT_NAME = "{_R_FACE}"' in src, "face"
    assert f"FONT_PX = {_R_PX}" in src, "size"
    assert f'FALLBACK_NAME = "{_R_FALLBACK}"' in src, "fallback face"
    assert f'FALLBACK_CELLS = "{_R_FALLBACK_CELLS}"' in src, "fallback cells"
    # THE BOX IS NOT IN THE SOURCE AT ALL — it is MEASURED off the font on
    # every run, which is the point of a raster and the thing the `.svg` never
    # had.  So it is checked against the sidecars instead, all 66 of them.
    for lang in LANGS:
        for screen in SCREENS:
            side = _raster_json(f"{lang}_{screen}")
            assert side["font"]["name"] == _R_FACE, (lang, screen)
            assert side["font"]["px"] == _R_PX, (lang, screen)
            assert (side["cell"]["w"], side["cell"]["h"]) == _R_CELL, \
                (lang, screen, side["cell"])
            assert side["cell"]["advance"] == float(_R_CELL[0]), \
                (lang, screen, "a fractional advance drifts the grid")
            assert side["fallback"]["name"] == _R_FALLBACK, (lang, screen)
            assert "".join(side["fallback"]["cells"]) == _R_FALLBACK_CELLS, \
                (lang, screen)


@pytest.mark.parametrize("lang", LANGS)
def test_the_raster_has_one_cell_per_character_of_the_txt(lang):
    """THE RASTER'S FIRST LAW: cells x box = pixels, on both axes.

    The `.txt` is the artefact three rounds judged this corpus on and the PNG
    is the artefact the fifth will, so the two have to be the same picture.  A
    raster that drew 99 columns would still look like a taskboard, and every
    per-cell number inc77 reports would be attributed one column off from the
    middle of the sheet onwards.
    """
    for screen in SCREENS:
        name = f"{lang}_{screen}"
        rows = (FRAMES / f"{name}.txt").read_text(
            encoding="utf-8").rstrip("\n").split("\n")
        cols = {len(r) for r in rows}
        assert len(cols) == 1, (name, "the txt is not a rectangle", cols)
        side = _raster_json(name)
        assert (side["txt"]["cols"], side["txt"]["rows"]) == \
            (cols.pop(), len(rows)), (name, "sidecar disagrees with the txt")
        assert (side["cols"], side["rows"]) == \
            (side["txt"]["cols"], side["txt"]["rows"]), \
            (name, "the cell grid disagrees with the txt")
        assert _png_size(name) == (side["cols"] * side["cell"]["w"],
                                   side["rows"] * side["cell"]["h"]), name


def _tiles_of(lang: str) -> dict:
    """`{(glyph, ink, ground, bold, underline): pixel block}` for six sheets.

    THE RASTER COMPOSES ONE CELL AT A TIME, into a box of its own, and pastes
    it — so two cells with the same tuple must be the same pixels, and reading
    only the distinct tuples reads every cell.  That identity is asserted
    here rather than assumed, and it is the clause that says NO GLYPH BLEEDS:
    Cascadia's `█` measures 10x20 against a 9x19 box, so a raster that drew
    the frame as text instead of as cells would give a full block's right-hand
    neighbour a column of ink it never declared, and the two cells with the
    same tuple would then differ by what happens to sit beside them.
    """
    from PIL import Image
    tiles: dict = {}
    for screen in SCREENS:
        name = f"{lang}_{screen}"
        side = _raster_json(name)
        w, h = side["cell"]["w"], side["cell"]["h"]
        with Image.open(RASTER / f"{name}.png") as raw:
            im = raw.convert("RGB")
        for x, y, ch, fg, bg, bold, und in _cells_of(side):
            key = (ch, fg, bg, bold, und)
            blk = im.crop((x * w, y * h, x * w + w, y * h + h)).tobytes()
            if key in tiles:
                assert tiles[key] == blk, \
                    (name, x, y, key, "the same cell drawn two ways — a "
                                      "glyph is bleeding out of its box")
            else:
                tiles[key] = blk
    return tiles


@pytest.mark.parametrize("lang", LANGS)
def test_a_probe_cells_pixels_are_the_declared_colours(lang):
    """THE RASTER'S SECOND LAW: every pixel is a mix of the two declared
    colours of the cell it is in, and of nothing else.

    The brief asked for "a probe cell's pixel colour equals the declared
    fg/bg", and that is exactly true only at the two ENDS: antialiasing puts
    most of a glyph's pixels somewhere between.  So the law is the segment.
    For every distinct cell in six sheets, every pixel `p` satisfies
    `p == ground + t*(ink - ground)` for some `t` in `[0, 1]`, within one unit
    per channel — measured over the whole corpus while this was written:
    **7081 distinct cells, worst channel error 1**.

    That is a stronger statement than the two-colour version and it is the one
    that catches what a raster gets wrong:

    * a cell painted on the wrong GROUND fails at `t = 0` — inc63's defect one
      artefact over, where 3200 of 3200 cells shipped on Textual's `#121212`;
    * a cell painted in the wrong INK fails at `t = 1`;
    * the pair SWAPPED fails everywhere the glyph is not symmetric in
      coverage, which is every glyph that is not blank or full — and
      `cell_grid` already swaps `reverse`, so a second swap here would be
      invisible in a law that only looked at two colours;
    * a glyph BLEEDING from the neighbouring cell fails because the intruder
      carries a third colour.

    NOT VACUOUS AT EITHER END, asserted: the blank cells really are the
    ground, and the ink end is really reached.
    """
    tiles = _tiles_of(lang)
    ends, blanks = 0, 0
    for (ch, fg, bg, bold, und), blk in tiles.items():
        F, B = _rgb(fg), _rgb(bg)
        span = [abs(F[c] - B[c]) for c in range(3)]
        c = span.index(max(span))
        for i in range(0, len(blk), 3):
            q = tuple(blk[i:i + 3])
            t = 0.0 if span[c] == 0 else (q[c] - B[c]) / (F[c] - B[c])
            t = max(0.0, min(1.0, t))
            pred = tuple(round(B[k] + t * (F[k] - B[k])) for k in range(3))
            assert max(abs(pred[k] - q[k]) for k in range(3)) <= 1, \
                (lang, ch, fg, bg, q, pred, "a colour the cell never declared")
            if t >= 0.999 and span[c]:
                ends += 1
        if ch == " " and not und:
            assert blk == bytes(B) * (len(blk) // 3), \
                (lang, "a blank cell is not its ground", bg)
            blanks += 1
    assert blanks, (lang, "no blank cell — the ground end is untested")
    assert ends, (lang, "no pixel reaches full ink — the ink end is untested")


#: WHAT THE FACE DOES TO A FULL BLOCK, found by looking and asserted so it
#: cannot change quietly.  `█` in Cascadia Mono at 16 px measures 10x20 for a
#: 9x19 cell and its outline does not land on the cell's bottom edge: the last
#: pixel row comes out at **75% coverage**, 162 of the cell's 171 pixels at
#: full ink and 9 at three quarters.  A full block therefore leaves a seam,
#: which is why Windows Terminal ships its own box-drawing glyphs and does not
#: use the font's.  It is recorded because inc77 reports COVERAGE, and 94.7%
#: is the ceiling this face gives that measure — no glyph in this corpus can
#: score 100.
FULL_BLOCK_COVERAGE = (162, 171)
BLOCK_KITS = {"corgi": 11, "industrial": 84, "nord": 88, "darkside": 21,
              "prism": 1}


def test_the_faces_full_block_leaves_a_seam_and_that_is_the_coverage_ceiling():
    seen = {}
    for lang in LANGS:
        n = sum((FRAMES / f"{lang}_{s}.txt").read_text(
            encoding="utf-8").count("█") for s in SCREENS)
        if n:
            seen[lang] = n
    assert seen == BLOCK_KITS, seen
    side = _raster_json("industrial_S1")
    (_, fg, *_), blk = next((k, b) for k, b in _tiles_of("industrial").items()
                            if k[0] == "█")
    px = [tuple(blk[i:i + 3]) for i in range(0, len(blk), 3)]
    full, total = px.count(_rgb(fg)), side["cell"]["w"] * side["cell"]["h"]
    assert (full, total) == FULL_BLOCK_COVERAGE, (full, total)
    assert _rgb(side["ground"]) not in px, "the seam is not bare ground"


def test_the_raster_laws_bite_on_the_three_defects_they_were_written_for(
        tmp_path, monkeypatch):
    """TEETH — the three mistakes a raster makes, on the corpus's own bytes.

    (a) THE GRID SLIPS.  A raster that drops a column draws a picture that
        looks entirely correct and attributes every cell after the cut to its
        neighbour.  That is the defect that turns a homoglyph distance into a
        confident number about the wrong pair.
    (b) THE GROUND IS NOT THE KIT'S — **inc63's defect, reproduced in the new
        artefact.**  Every pixel of the declared ground is repainted Textual's
        own `#121212`, which is the colour all 66 sheets really did ship until
        inc63; the picture still looks like a taskboard and every cell is
        still internally consistent, and the segment clause reads a colour no
        kit declares.
    (c) THE SIDECAR CLAIMS A BOX THE PICTURE DOES NOT HAVE.  Both the size law
        and the declaration law have to catch it, because between them they
        are the sentence "the cell inc77 measured is the cell that was drawn".

    Nothing is built here: `instrument`'s six shipped PNGs are copied, edited,
    and the REAL laws are run with `RASTER` pointed at the copy — so what is
    watched failing is the law and not a restatement of it.  After every arm
    the file is restored and the law is run again, so a red is the mutation
    and never the copying.
    """
    import json
    import shutil
    from PIL import Image
    lang, shipped = "instrument", RASTER
    work = tmp_path / "png"
    shutil.copytree(shipped, work)
    monkeypatch.setitem(globals(), "RASTER", work)

    # THE CONTROL ARM, before anything is touched.
    test_the_raster_has_one_cell_per_character_of_the_txt(lang)
    test_a_probe_cells_pixels_are_the_declared_colours(lang)

    name = f"{lang}_S1"
    side = _raster_json(name)
    w, h = side["cell"]["w"], side["cell"]["h"]

    # (a) one column short — 99 cells of picture claiming 100 cells of text
    with Image.open(work / f"{name}.png") as raw:
        im = raw.convert("RGB")
    im.crop((0, 0, im.width - w, im.height)).save(work / f"{name}.png")
    assert _png_size(name)[0] == (side["cols"] - 1) * w
    with pytest.raises(AssertionError):
        test_the_raster_has_one_cell_per_character_of_the_txt(lang)
    shutil.copy(shipped / f"{name}.png", work)
    test_the_raster_has_one_cell_per_character_of_the_txt(lang)

    # (b) the kit's ground repainted Textual's default, everywhere it appears
    ground, textual = _rgb(side["ground"]), _rgb(_TEXTUAL_DEFAULT_GROUND)
    assert ground != textual, "instrument's ground is not Textual's"
    with Image.open(work / f"{name}.png") as raw:
        im = raw.convert("RGB")
    raw, g, x = bytearray(im.tobytes()), bytes(ground), bytes(textual)
    for i in range(0, len(raw), 3):  # aligned, so no match straddles a pixel
        if raw[i:i + 3] == g:
            raw[i:i + 3] = x
    Image.frombytes("RGB", im.size, bytes(raw)).save(work / f"{name}.png")
    with pytest.raises(AssertionError):
        test_a_probe_cells_pixels_are_the_declared_colours(lang)
    shutil.copy(shipped / f"{name}.png", work)
    test_a_probe_cells_pixels_are_the_declared_colours(lang)

    # (c) an 8 px cell claimed over a 9 px picture
    narrow = json.loads(json.dumps(side))
    narrow["cell"]["w"] = 8
    (work / f"{name}.json").write_text(json.dumps(narrow), encoding="utf-8")
    with pytest.raises(AssertionError):
        test_the_raster_has_one_cell_per_character_of_the_txt(lang)
    with pytest.raises(AssertionError):
        test_the_rasters_declarations_are_the_ones_this_file_measures_against()
    shutil.copy(shipped / f"{name}.json", work)
    test_the_raster_has_one_cell_per_character_of_the_txt(lang)
    test_the_rasters_declarations_are_the_ones_this_file_measures_against()


# ---------------------------------------------------------------------------
# inc77 — THE MEASURES ON THE RASTER.  What E2 was blocking.
#
# `prototypes/components/legibility.py` writes `prototypes/out/legibility.txt`.
# The laws below do NOT import it, for the reason this file gives twice
# already: the instrument's arithmetic is restated here in four lines and
# checked against the artefact it shipped, so the two can only agree by being
# right.  The restatement draws through the PRIMARY face only, so the four
# cells Cascadia lacks are excluded by name — a declared limitation of this
# restatement, not of the instrument.
# ---------------------------------------------------------------------------

LEGIBILITY = FRAMES.parents[1] / "prototypes" / "out" / "legibility.txt"


@functools.lru_cache(maxsize=None)
def _face() -> tuple:
    """The face, size and box, taken from a sidecar rather than from a path.

    inc76's declaration law already pins every sidecar to `raster.py`'s
    declared constants, so reading one here inherits that check instead of
    repeating it — and it keeps a `C:\\WINDOWS` path out of this file.
    """
    side = _raster_json("instrument_S1")
    return (side["font"]["path"], side["font"]["px"],
            (side["cell"]["w"], side["cell"]["h"]))


@functools.lru_cache(maxsize=None)
def _cov(ch: str) -> tuple:
    """The glyph's coverage over the cell: white on black, one float a pixel.

    Four lines, and they are `raster.cell_tile` for a primary-face glyph with
    the colours fixed — which is the point.  If `legibility.py` ever measures
    a different drawing than this one, the two disagree and the laws below say
    so instead of both being wrong in the same direction.
    """
    from PIL import Image, ImageDraw, ImageFont
    path, px, box = _face()
    f = ImageFont.truetype(path, px)
    im = Image.new("RGB", box, "#000000")
    ImageDraw.Draw(im).text((0, f.getmetrics()[0]), ch, font=f,
                            fill="#ffffff", anchor="ls")
    b = im.tobytes()
    return tuple(b[i] / 255 for i in range(0, len(b), 3))


@functools.lru_cache(maxsize=None)
def _xor(a: str, b: str) -> float:
    """XOR area over cell area, as a PERCENTAGE. 0.0 means one drawing."""
    ca, cb = _cov(a), _cov(b)
    return sum(abs(x - y) for x, y in zip(ca, cb)) / len(ca) * 100


def _corpus_glyphs() -> dict:
    n: dict = {}
    for lang in LANGS:
        for screen in SCREENS:
            for ch in (FRAMES / f"{lang}_{screen}.txt").read_text(
                    encoding="utf-8"):
                if ch not in ("\n", " "):
                    n[ch] = n.get(ch, 0) + 1
    return n


def _drawable() -> list:
    """The corpus's glyphs the PRIMARY face draws, sorted."""
    return sorted(g for g in _corpus_glyphs() if g not in _R_FALLBACK_CELLS)


def _zero_pairs(glyphs) -> list:
    """Index pairs whose two glyphs rasterise identically.

    By INDEX and not by value, because the teeth below make one glyph appear
    twice and a set of values would silently swallow exactly the thing being
    demonstrated.
    """
    return [(i, j) for i in range(len(glyphs))
            for j in range(i + 1, len(glyphs))
            if _xor(glyphs[i], glyphs[j]) == 0.0]


#: THE ONE PAIR IN THIS CORPUS THAT IS LITERALLY ONE DRAWING, and the whole
#: reason a raster had to be built.  `•` U+2022 BULLET and `∙` U+2219 BULLET
#: OPERATOR rasterise **byte for byte identically** in Cascadia Mono at 16 px:
#: the XOR area is 0.0, not 0.004.  `HOMOGLYPH_FAMILIES` puts them in one row
#: on the strength of a reading, and this is the first artefact in the
#: programme that can say the reading was not a guess.
#:
#: NO KIT DRAWS BOTH, and this says so rather than overstating: naught spends
#: `∙` 134 times (danger + severity) and swiss spends `•` twice (required), so
#: it is two languages holding one drawing for incompatible meanings — a fact
#: about the corpus, not a collision inside any kit.  A twelfth kit reaching
#: for the other one is what this constant is here to catch.
IDENTICAL_DRAWINGS = (("•", "∙"),)

#: THE TEN PAIRS FOUR ROUNDS ARGUED ABOUT, as XOR area over the cell.  Round
#: four ruled every one of them *"irresoluble sin raster"*; these are the
#: numbers.  Recorded so a change to a glyph, a face or a size is a diff and
#: not a discovery.
#: `(meaning marks the corpus draws, how many are under 3:1 DECLARED at the
#: seat the report picks)`. The second number is NOT a violation count and the
#: report says so at length; it is pinned because 45 of 79 is the size of a
#: question nobody had asked before this increment could ask it.
MEANING_MARKS = (79, 45)

ARGUED_DISTANCE = {("•", "●"): 21.64, ("○", "◦"): 22.81, ("◎", "◉"): 21.42,
                   ("†", "‡"): 4.87, ("▪", "■"): 26.52, ("╌", "┄"): 4.09,
                   ("╌", "┈"): 4.46, ("┄", "┈"): 2.79, ("▬", "◦"): 17.09,
                   ("⠇", "⠸"): 15.13}


def test_a_homoglyph_distance_is_zero_only_when_the_drawings_are_one():
    """THE MEASURE'S OWN LAW, and the one the brief asked for: *"the XOR area
    ... so 'same drawing' becomes a number"*.

    Three clauses. A glyph against itself is exactly zero; the measure is
    symmetric; and over every pair of distinct glyphs the 66 sheets draw,
    **exactly one pair measures zero** and it is the one named above. The
    third clause is what makes the first two non-vacuous: a measure that
    returned zero for everything would pass them both.
    """
    glyphs = _drawable()
    assert len(glyphs) > 190, len(glyphs)
    for ch in glyphs:
        assert _xor(ch, ch) == 0.0, ch
    zero = {(glyphs[i], glyphs[j]) for i, j in _zero_pairs(glyphs)}
    assert zero == set(IDENTICAL_DRAWINGS), zero
    for a, b in IDENTICAL_DRAWINGS:
        assert _xor(b, a) == _xor(a, b) == 0.0, (a, b)


def test_the_pairs_four_rounds_argued_about_have_these_distances():
    """Measured independently here AND read out of the report the instrument
    shipped — so the artefact on disk is not stale and the two implementations
    do not disagree."""
    printed = {}
    for line in LEGIBILITY.read_text(encoding="utf-8").split("\n"):
        bits = line.split()
        if (len(bits) >= 3 and bits[2].endswith("%") and len(bits[0]) == 1
                and len(bits[1]) == 1
                and (bits[0], bits[1]) in ARGUED_DISTANCE):
            printed[(bits[0], bits[1])] = float(bits[2].rstrip("%"))
    assert printed == ARGUED_DISTANCE, printed
    for (a, b), want in ARGUED_DISTANCE.items():
        assert round(_xor(a, b), 2) == want, (a, b, _xor(a, b), want)


def test_the_legibility_report_on_disk_is_the_one_this_corpus_produces():
    """The header, the census's row count and the zero-ink finding, checked
    against what this file works out for itself. A report that outlives the
    corpus it describes is the failure mode `render.py`'s sidecars already
    carry a comment about."""
    text = LEGIBILITY.read_text(encoding="utf-8")
    _, px, (w, h) = _face()
    assert f"{_R_FACE} {px}px" in text, "face"
    assert f"cell      {w}x{h} px = {w * h} pixels" in text, "cell"
    used = _corpus_glyphs()
    assert (f"corpus    {len(used)} distinct painted glyphs, "
            f"{sum(used.values())} painted cells") in text, "corpus"
    assert "A1. 1 GLYPH(S) IN THIS CORPUS DRAW NOTHING AT ALL" in text
    # the census's row count, restated by the census itself
    import importlib.util
    src = FRAMES.parents[0] / "collision_census.py"
    spec = importlib.util.spec_from_file_location("_census_for_legibility", src)
    cc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cc)
    rows = sum(len(cc.homoglyph_rows(L)) for L in LANGS)
    assert f"{rows} rows, the census's own count" in text, rows
    # AND THE TWO COUNTS SECTION E TURNS ON, pinned so a token move or a kit
    # edit shows up as a diff. The second is deliberately NOT a count of
    # violations -- inc74 judged those seats one at a time -- it is the size
    # of the question a floor ruling would be answering.
    marks, under = MEANING_MARKS
    assert f"The {marks} meaning marks the corpus draws span" in text, marks
    assert f"AND {under} OF THEM ARE UNDER 3:1 ON DECLARED" in text, under


def test_the_distance_law_bites_when_two_homoglyphs_are_made_one():
    """TEETH — the mutant the brief named: *"swap two homoglyphs"*.

    ledger's `†` is REQUIRED and its `‡` is INVALID. The census calls that the
    tightest row in the corpus, round four ruled it unresolvable without a
    raster, and it measures **4.87 %** of a cell. Make the invalid mark the
    same drawing as the required one — the swap — and the distance goes to
    exactly zero and the corpus's zero-pair sweep returns TWO pairs where it
    returned one.

    Both vacuity arms are here: the un-mutated pair is not zero, so the law
    can fail; and the sweep is re-run on the real glyph list afterwards to
    show it comes back to one.
    """
    assert round(_xor("†", "‡"), 2) == ARGUED_DISTANCE[("†", "‡")]
    assert _xor("†", "‡") > 0.0, "the pair is not already one drawing"

    glyphs = _drawable()
    assert len(_zero_pairs(glyphs)) == 1, "one identity before the mutation"

    # ledger's INVALID mark redrawn as its REQUIRED mark: `‡` becomes `†`, so
    # `†` now appears twice in the same corpus and the sweep must see it.
    mutant = ["†" if g == "‡" else g for g in glyphs]
    assert len(mutant) == len(glyphs) and mutant.count("†") == 2
    grown = _zero_pairs(mutant)
    assert len(grown) == 2, grown
    assert {mutant[i] for i, _ in grown} | {mutant[j] for _, j in grown} == \
        {"•", "∙", "†"}, grown

    assert len(_zero_pairs(glyphs)) == 1, "and back to one"
