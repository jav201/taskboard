"""inc19: append the match / keyhint laws."""
import pathlib

p = pathlib.Path("tests/test_components.py")
s = p.read_text(encoding="utf-8")
ADD = '''

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
    assert any(w in k.MATCH_STYLE for w in ("bold", "underline", "reverse")), \\
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
'''
assert "def test_match_returns_the_text" not in s
p.write_text(s + ADD, encoding="utf-8")
print("inc19 laws appended")
