"""inc18: append the log_row laws."""
import pathlib

p = pathlib.Path("tests/test_components.py")
s = p.read_text(encoding="utf-8")
ADD = '''

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

    Asserted for every language rather than for the two, because a rule that
    holds only where it was forced is a special case waiting to be copied."""
    k = LG.kit(lang)
    for lv in LEVELS:
        assert k.c["alert"] not in k.log_row(lv, TS, MSG), (lang, lv)
        assert k.c["warn"] not in k.log_row(lv, TS, MSG), (lang, lv)


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
'''
assert "def test_the_log_level_reads" not in s
p.write_text(s + ADD, encoding="utf-8")
print("inc18 laws appended")
