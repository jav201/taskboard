"""inc16: append the select / menu / danger laws."""
import pathlib

p = pathlib.Path("tests/test_components.py")
s = p.read_text(encoding="utf-8")
ADD = '''

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

    Asserted on the corner glyphs rather than on a promise: four of these
    eleven languages have a commitment that makes a box unconstructable, and
    a menu that boxed itself would break it in the quietest possible place."""
    k = LG.kit(lang)
    for row in k.menu(OPTS, 1, 9):
        assert not (set(plain(row)) & set("┌┐└┘╔╗╚╝")), (lang, row)


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
    tags = lambda s_: _TAG.findall(s_.replace("\\\\[", _ESC))
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
'''
assert "def test_a_select_is_not_a_stepper" not in s
p.write_text(s + ADD, encoding="utf-8")
print("inc16 laws appended")
