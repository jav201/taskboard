"""inc15: append the field_row laws to tests/test_components.py."""
import pathlib

p = pathlib.Path("tests/test_components.py")
s = p.read_text(encoding="utf-8")
ADD = '''

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
'''
assert "field_row" not in s
p.write_text(s + ADD, encoding="utf-8")
print("inc15 laws appended")
