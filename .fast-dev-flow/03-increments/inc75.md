# Increment 75 — corgi's mode gets an edge, and industrial's paper stops being something a value can say

**Batch:** `rework-7a`, increment 4 of 4 · **C8's second half** and **the `/` ruling**.
**Files:** `taskboard/language.py`, `tests/test_components.py` — **2 source files**, plus 2
regenerated component `.txt` and 2 regenerated `.svg`, and the regenerated census table.

**Two frames, two composed cells, two laws.** `corgi_S4` kept its mode strip in inc65 and left the
other thirty-one rows blank, so a destructive question had no opener, no closer and no box — round
four's §7.4: *"the exemption was renamed rather than retired."* `industrial_S2` row 6 read
`▐12/09/26//////…▌`, twenty-six paper slashes and two of the value's own, with no frontier between
them — the collision inc71 measured in the declaration and could not show in the corpus.

**Census 29 → 28.** industrial drops a colliding cell: `/` loses its chrome role at the field, so
what is left of it is one A-family and it stops colliding.

Suite **1313 → 1338**.

---

## 0. Rulings (orchestrator, 2026-09-07, on the operator's delegation)

> **K6:** contrast is measured against the background actually under the run (the second grounds:
> selection bands, plates, match rects), not only the canvas. `ink` and `mut` ≥ 4.5:1 against every
> ground they are painted on; `focus` ≥ 3:1.

> **K7:** `dim` ≥ 3:1 wherever it classifies (a severity rung on a log row, a dash count, a state
> mark); a purely decorative leader or seam is exempt by seat, named. `alert` ≥ 4.5:1 against every
> ground it is painted on, all eleven.

> **Match tier:** `accent` (or the match ink) against `mut` and against `ink` ≥ 3:1, all eleven, so
> raising `mut` cannot silently erase the match.

> **L7 measured:** the `info` rung may be air (blueprint, ledger, doctrine) or drawn; if drawn it
> obeys K7 (≥ 3:1). Nine languages draw it under 2:1: fix each.

> **C8, second half:** corgi's confirm gets walls from its display frame (`▓`, inc67's register
> ruling) with the board still gone; thirty blank rows with no opener or closer is not a modal.

> **swiss `╎`:** stands; consistency with the kit's own dead cell beats one fewer vertical.
> Recorded.

> **industrial `/`:** the value's separators and the field paper may not be one glyph: the paper
> becomes a cell that no value can contain (cite industrial's alphabet), the invalid marks at
> slider.knob/stepper.step stay.

And the two rulings correcting the match tier and industrial's `focus`, quoted verbatim in
`inc73.md` §0b — both discharged there. This increment carries out **C8's second half** and **the
`/` ruling**. **swiss `╎` is RECORDED AND NOT IMPLEMENTED**, on purpose: the ruling says it stands,
and nothing in the code had to move for that to be true.

---

## 1. Cause and mechanism — corgi's mode gets an edge

**Cause.** `Corgi.overlay_instead` composed `[head] + [""] * (y-1) + rows`. inc65 gave back
`under[0]` — the mode strip — and stopped there, on the strength of `MODAL_KEEPS_ONLY_THE_HEAD`. The
two criteria round three wrote were answered and the frame still had **thirty blank rows and no
boundary at all**, which is word for word the axis by which `swiss_S4` and `ledger_S4` were `rework`.

**Mechanism.** The question is wrapped in a bar at each end:

```python
bar = f"[{c['mut']}]{mark(self.PANE_RULE * w)}[/]"
block = [bar] + list(rows) + [bar]
y = max(1, (h - len(block)) // 2)
out = [head] + [""] * (y - 1) + block
```

```
before  f01 [1]B O A R D [2]FORM [3]CFG [4]LOG        f14 Delete 3 tasks?   ...  f19 answers
after   f01 [1]B O A R D [2]FORM [3]CFG [4]LOG   f13 ▓▓▓…▓▓ (100)  f14 Delete 3 tasks?
        ...  f19 answers   f20 ▓▓▓…▓▓ (100)
```

**The bar is the kit's own `PANE_RULE`, and no new cell enters the language.** `▓` is the milled top
step of corgi's shade ramp, put there by inc67 (K5) *precisely* so that a partition carries no rung
of anything — *"THE BANK IS THE READING, THE PANEL IS THE MILLED METAL. A pane edge is panel."* A
mode's edge is the same kind of edge as a pane's.

**Drawn in `mut`, not `dim`, and that is the one place this seat departs from `pane_split`.** A seam
divides two things a reader can already see; these two rows are the only thing saying where an
irreversible question begins and ends, and `DIM_CLASSIFIES` (inc74) is the table that draws that
line. corgi's `dim` is 1.71:1.

**Still not a box, and the board is still gone.** Two bars, no vertical, no corner. The refusal was
never about walls — it is about a dialog floating over a board — and there is still no board behind:
`test_corgis_confirm_has_an_edge_and_still_has_no_board` asserts both halves in one place, because
the increment that took only one of them is why that test exists.

## 2. Cause and mechanism — a paper no value can contain

**Cause.** `textfield.main[INVALID]` was `▐/▌`, and the value lying on that paper is a DATE. Round
four's §7.6 put the criterion plainly: *"say where the entered value ends and the paper begins. No
answer except by knowing in advance that a date carries two slashes."* And it named the deeper
problem — inc71 split `/`'s role correctly in the census, but the second role lives at
`slider.knob[INVALID]` and `stepper.step[INVALID]` and **no frame of the sixty-six draws either**, so
the row was real in the declaration and unconfirmable in the corpus.

**Mechanism.** `▐/▌` → `▐░▌`.

```
before  due!          ▐12/09/26//////////////////////////▌
after   due!          ▐12/09/26░░░░░░░░░░░░░░░░░░░░░░░░░░▌
```

**`░` is the shade ramp this kit already owns** — `░ ▓ █`, beside the plate's `▐ ▌` — it is
`indicator[DISABLED]` and carries no A-family, and, the point, **it is not a character a value can be
typed with**. A field's paper stops being something the value might have said. The `DANGER_FORM` is
untouched (ruling C, still): `╱` is nowhere near this seat, and the invalid marks at `knob` and
`stepper.step` **stay `/`**, which the teeth assert by name.

## 3. The laws

**`test_a_confirm_opens_and_closes_on_marks_of_its_own`** — over the eleven, off the shipped frames.
Each end of the confirm carries a mark of the kit's own, and the opener is never the question's own
words.

**"DRAWN" AND NOT "CHANGED", and the difference is the whole of corgi.** A confirm that erases the
page changes every row it erases, so its first *changed* row is one that went blank — a fact about
the erasure, not about the question. `confirm_span` is right for contiguity and wrong for this
reading, so `confirm_edges` walks in from both ends of the span to the first row that says something.
**inc66's `test_every_confirm_says_where_it_ends` asked only about the last row and was written
deliberately weak; this asks about both and still never asks for a rule, a lid or a corner.** Six
spellings of one shape: naught's two runs of unlit lattice at full charge (inc72), swiss's two
hairlines, ledger's two rules (inc72), corgi's two display bars, industrial's and nord's real box.

**`test_a_rejected_fields_paper_is_a_cell_no_value_can_contain`** — the `/` ruling, over the eleven,
against values read from `fixture.py` **by path**, so the law measures the corpus this repo renders
rather than a list somebody kept up to date. The paper is taken through `split_field_glyph` — the one
splitter both the law and the census share since inc71 — so the two instruments cannot disagree about
which cell of a rejected field is paper.

## 4. One exemption, and it is a ground rather than a hole

`CONFIRM_EDGE_REFUSED` holds **solari** and nobody else. Its band is `band="reverse"` — a token the
kit declares — so its edge is not a mark at all: the question is a reversed plate across the full
measure, and what says where it begins and ends is the rect's own boundary. Asking it for a glyph
would be asking a departure board to draw a line around its announcement row.

**The refusal is checked, not taken on its word.** The arm asserts the token is really `reverse` and
that `solari_S4.svg` really carries a background run wider than 800 units — so a kit that simply
forgot to draw an edge cannot claim it. And the table is asserted to hold exactly one name, because
`MODAL_KEEPS_NOTHING` taught this file that an exemption written before anybody could satisfy the law
outlives its reason.

**naught no longer needs the refusal the brief offered it.** inc72 gave its band two runs of `NA.OFF`
at full charge, so it opens and closes on marks like the other nine.

## 5. Teeth

**`test_the_confirm_edge_law_bites_on_the_composition_corgi_shipped`** restores inc65's block —
strip plus thirty-one blank rows — and asserts the reading that made it a `rework`: the band's
outermost drawn row becomes `Delete 3 tasks?` itself, so **there is nothing between the reader and
the words that says a question has begun**. It then undoes and asserts the edge is back.

**`test_the_paper_law_bites_on_the_declaration_industrial_shipped`** restores `▐/▌`, asserts the
paper reads `/` again through the shared splitter, watches the law go red on industrial and stay
green on the other ten — and asserts what the ruling PRESERVED, because a fix that swept the glyph
would have been a different decision: `knob[INVALID] == "/"` and `stepper.step[INVALID] == "//"`,
and the new paper is the kit's own `indicator[DISABLED]`.

## 6. The census went 29 → 28, and the row that closed is the one inc71 opened

```
                       inc74   inc75
INDUSTRIAL colliding      3       2
  /   [2 families]  INVALID slider.knob + INVALID stepper.step  ·  textfield.main mark (invalid)
      -> the chrome half is gone, one A-family is left, and a cell with one family does not collide
-----------------------------------------------------------------------------------
TOTAL colliding cells    29      28
TOTAL homoglyph rows     24      24   (unchanged)
```

**This is the accounting inc66 predicted in the other direction.** Giving swiss's field a paper cost
one row because a paper adds the `invalid` A-family to a chrome cell; taking industrial's field off
a cell that already carried the A-family elsewhere gives one back. The instrument is consistent in
both directions, which is the strongest thing that can be said for it.

## 7. Frames changed

| frame | txt | svg | what moved |
|---|---|---|---|
| `corgi_S4` | ✓ | ✓ | rows 13 and 20: 100 `▓` each, the display frame's bar; the question block moves up one row |
| `industrial_S2` | ✓ | ✓ | row 6: `▐12/09/26//////…▌` → `▐12/09/26░░░░░░…▌` |

**The other 64 `.txt` and 64 `.svg` are byte-identical, and all 22 gallery artefacts are** — the
gallery sheet is cut at 118×34 before its invalid-field row (`spec.md` §12.5) and corgi's confirm is
not drawn there.

**Gallery 30–51 in the skill:** the batch close runs `export_to_skill.py`; see §11.

## 8. Gate tails, verbatim

```
$ python -X utf8 -m pytest -q
FAILED tests/test_app.py::test_win_clipboard_roundtrip - AssertionError: assert None == 'roundtrip 123 ABC taskboard'
1 failed, 1338 passed, 2 skipped, 4 warnings in 36.49s

$ python -X utf8 prototypes/verify_language.py
ALL PASSED
                                                        (exit 0)

$ python -X utf8 prototypes/components/render.py
  66 .txt + 66 .svg -> ...\prototypes\components
  66 candidates files
  no two frames identical within a screen (330 pairs)
  0 hand-drawn elements declared (0 refused, 0 evoked)
                                                        (exit 0)

$ python -X utf8 prototypes/components/matrix.py
  66 of 66 · refusals [] for all eleven                 (exit 0)

$ python -X utf8 prototypes/collision_census.py
INDUSTRIAL   2 colliding cells   (LEVELS ▫▫/▪▪/■■  DANGER ╱╱╱╱  REQUIRED !  CUR ▶)
TOTAL                       28
TOTAL homoglyph rows            24
                                                        (exit 0)

$ python -X utf8 prototypes/capture_languages.py
  22 grids identical across two PROCESSES
  22 captures -> ...\prototypes\gallery
  no two boards identical
                                                        (exit 0)
```

Suite **1313 → 1338** (+11 confirm-edge arms, +11 paper arms, +1 corgi C8 arm, +2 teeth). Census
**29 → 28**; homoglyph rows unchanged at 24.

## 9. Risks

1. **corgi now draws two full-measure bars on the screen it renounced chrome for.** *"No persistent
   navigation chrome; its answer to smallness is FEWER THINGS AT ONCE"* is this kit's commitment, and
   200 cells of `▓` is not fewer things. Taken deliberately, and the same trade inc66 wrote for
   swiss's fourth hairline: a destructive question that cannot say where it begins is a worse defect
   than a bar count.
2. **`▓` is also corgi's `MASCOT_PIXEL`, its `PANE_RULE`, its switch's live track and its checkbox's
   ticked mark.** None of those is drawn on `S4`, so the confirm sheet is the benign case — but the
   cell is now this kit's most-spent chrome and a future MEANING landing on it would be K5 again.
3. **industrial's paper is `░`, which is `indicator[DISABLED]` — the dead meter fill.** On `S2` no
   meter is drawn, so nothing collides in the frame; on a screen that showed a dead meter beside a
   rejected field the two would be one texture. No artefact in this repo draws that pair.
4. **`fixture_values()` reads what the fixture declares, not what every screen composes.** A caption,
   a gate name or a keyhint the fixture does not hold is outside the law's reach; the value the
   objection is about (`12/09/26`) is added by name.

## 10. Found by looking, not fixed

- **nord papers its rejected field in AIR (`"? ?"`) and darkside does too (`"Ø Ø"`).** Their rune is
  a space, so the paper law has nothing to compare and both are named in it rather than silently
  skipped. It is an L2-shaped reading (*"air is not a state"*, inc69) at a seat L2 did not reach —
  swiss's fix was about the field's EXTENT — and no ruling covers it.
- **`/` survives at `knob[INVALID]` and `stepper.step[INVALID]` and neither is drawn in the 66.**
  The ruling preserved them on purpose; round four's §7.6 point stands unchanged — that row of the
  census is still real in the declaration and unconfirmable in the corpus, and the stepper has had a
  law since inc51 and no artefact for four rounds.
- **corgi's `▛▛ █Delete█ ▜▜` is unchanged**, and `█` is this kit's error rung and its `DANGER_FORM`.
  The focus ring on the irreversible button is still the wall pair of `S2`'s normal text field —
  round four's second objection to this frame, untouched.
- **solari's exemption is the only one in the new table and it is a GROUND argument**, which is the
  same shape as `THE_BAND_IS_A_SECOND_GROUND` (inc70) and `THE_GROUND_IS_NOT_A_MARK` (inc68). Three
  exemptions in this file now turn on "a ground is not a mark"; nobody has asked whether that is one
  idea or three.

## 11. Pending — not this increment

- The batch close: `export_to_skill.py` with captures written vs identical, and `spec.md` §19 for
  `rework-7a`.
- solari's per-row band ink (inc73 §12); `depth_ground()`'s role; nord's and darkside's air paper.

## 12. Suggested next task

Close the batch: run `export_to_skill.py`, record which of the skill's gallery 30–51 changed
byte-wise by name, and write `spec.md` §19 with the nine rulings, every token moved, the frames
changed (txt and svg separately) and the census accounting across the four increments.

## Evidence checklist

- [x] **Tests/type checks/lint pass — WITH ONE RED, NAMED.** `1338 passed, 2 skipped, 1 failed`
      (inc74 closed at `1313 passed`). The failure is
      `tests/test_app.py::test_win_clipboard_roundtrip`, environment-coupled (spec §10.6) —
      **reported, not counted, not touched.** `verify_language.py` ALL PASSED exit 0. `render.py`
      66/330/0. `matrix.py` refusals `[]` ×11. `collision_census.py` both self-checks green,
      **TOTAL 29 → 28**, homoglyph rows 24 unchanged. `capture_languages.py` plain: 22 captures, 22
      grids identical across two processes, **0 artefacts moved**.
- [x] **No secrets in code or output** — one overlay composition, one kit table cell, two laws, two
      teeth. No network, no new dependency, no path outside the worktree.
- [x] **No destructive commands run without approval** — none.
- [x] **File count within cap** — **2 source files**: `taskboard/language.py`,
      `tests/test_components.py`.
- [x] **Review packet attached** — this document.
