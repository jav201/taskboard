"""inc17: append the overlay / refusal-registry / knockout laws."""
import pathlib

p = pathlib.Path("tests/test_components.py")
s = p.read_text(encoding="utf-8")
ADD = '''

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
    assert "Delete 3 tasks?" in plain(out[0])


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
    lit = [r for r in out if plain(r).strip(NA.ON) == ""]
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
    k.meter(3, 9, [1, 1, 1], 60)          # the block reads its figures here
    stamp = "\\n".join(k.tabs(["board", "log"], "board").split("\\n"))
    assert any(k.knockout_cell(w) in stamp
               for w in ("BOARD", "board", "LOG", "log", k.mood.upper(),
                         k.mood)), stamp
'''
assert "def has_lid" not in s
p.write_text(s + ADD, encoding="utf-8")
print("inc17 laws appended")
