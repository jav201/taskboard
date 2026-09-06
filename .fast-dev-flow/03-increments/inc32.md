# Increment 32 — the six that inherited, asked to choose

**Batch:** `kits-learn-4` · **AC-5**
**Files:** `taskboard/language.py`, `tests/test_components.py` — **2 source files**.

---

## 1. The defect, and it is the batch's own shape one level up

`inc19.md` §7, one line, carried forward without a fix: *"Five languages inherit the base hint row and
the base match style."* Measured at this HEAD it was **six languages and seven mechanisms**:

```
              field_row  DISCLOSE  DANGER_FORM  LEVELS  MATCH_STYLE  keyhint  overlay
instrument        Kit       Kit        Kit        Kit       Kit        Kit      Kit
swiss             Kit       Kit        Kit        Kit       Kit        Kit      Kit
industrial        Kit       Kit        Kit        Kit       Kit        Kit      Kit
nord              Kit       Kit        Kit        Kit       Kit        Kit      Kit
darkside          Kit       Kit        Kit        Kit       Kit        Kit      Kit
solari            Kit       Kit        Kit        Kit       Kit        Kit      Kit
```

**A seat with five implementations and six holes is the palette-swap failure with a longer fuse.** The
five languages the PROTOTYPE round rendered diverge and are tested for it; the six nobody rendered agree
quietly, and agreement that nothing asked for looks exactly like a contract until you photograph it.

---

## 2. The mechanisms, each with the commitment it was derived from

### instrument — LANGUAGES.md §1 · *"whitespace structure · drawn dot-matrix type · borders almost absent"*

```
field_row   due date ⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒12/09/26   the GRATICULE, running to the figure
keyhint     up⠒move   esc⠒close                         the same mark at one cell
DISCLOSE    ⠿   DANGER ⠛⠛   LEVELS ⠂⠂ / ⠆⠆ / ⠇⠇          severity by DOT COUNT
overlay     BANDED: two graticule rules, page unlit      "borders almost absent"
```

The graticule **is not a leader**, which is the distinction ledger's row forces every language to make: a
leader is a run drawn *between* two marks to connect them; a graticule was on the glass before either
arrived. Naught draws the same distinction about its lattice and fills **after** the figure; this one
fills **before** it, because a scope's reading sits at the trace's end.

### swiss — §2 · *"airy · flush-left everything · no boxes — alignment does the dividing"*

```
field_row   due date       12/09/26                     FLUSH LEFT, both, on the grid
keyhint     up   move      esc   close                  GUTTER and 2×GUTTER, its own two measures
DISCLOSE    ─   DANGER ╲ ╱   LEVELS · / ─ / ━            a WEIGHT ladder
overlay     the question under the single hairline      "no boxes, at any width"
```

**Every other language closes the gap somehow.** This one does not close it: the figure starts at the
next *column* and the emptiness is the divider — the method stated as one row. And its danger form is
`╲ ╱`, which is **`field_form(INVALID)`'s own pair**: one rejection notation, not two.

### industrial — §3 · *"boxed groups · numbered and labelled · FAILS when colour must carry severity"*

```
field_row   DUE DATE                    ▐ 12/09/26 ▌    the figure stands on a PLATE
keyhint     ▐up▌ MOVE   ▐esc▌ CLOSE                     the key is plated, the label is its legend
DISCLOSE    ▼   DANGER ╱╱ ╱╱   LEVELS ▫▫ / ▪▪ / ■■       hazard striping; a plate ladder
overlay     it DRAWS the lid, and MODAL_BOX IS DISPLAY_BOX
```

**That last clause of its commitment decides three of the seven.** A language documented as unable to put
severity on colour has to put it on shape, and the shape it owns is the stamped plate. It is also the
**only one of the eleven whose commitment asks for a box** — so it draws one, in its own half-cell plate
chrome rather than the terminal's hairline. Corgi brackets its keys; this one stamps them, which is the
difference between a silkscreened panel and a machined one.

### nord — §6 · *"the only language that INHERITS THE USER'S ENVIRONMENT instead of overriding it"*

**Nord's answer is the base, and for this one language that is a commitment rather than a gap.** A
right-flushed two-column list, `▾`, `!`, the `· / ! / !!` ladder, bold accent on a match, `key label`
hints and a `┌─┐` modal are the terminal's own conventions — and the base kit *was written as nord*.
Giving it a mechanism of its own would not be filling a hole, it would be leaving base16 doctrine.

**And it is asserted rather than written.** `test_nord_declares_the_environment_and_the_declaration_is_
checked` walks the MRO for all seven and requires the owner to be `Kit`, so a mechanism landing on nord by
accident goes red and one landing on purpose has to delete the paragraph that says nord is base16 first.

### darkside — §8 · *"depth by ±1 grey step, never borders — borders are RESERVED for modals"*

```
field_row   due date                      ▬ 12/09/26    quiet lowercase, air, the figure's own seat
keyhint     up move  ·  esc close                       the calmest divider that is still a mark
DISCLOSE    ▿   DANGER Ø Ø   LEVELS ·  / o  / O          a dimming ladder made of its own CUR
overlay     it DRAWS the lid, ROUNDED (╭╮╰╯)            the "clinical-WARM" half of its adjective
```

**The reservation is the interesting half.** Prism inherited this doctrine and spends it — it is the one
language `MODAL_BORDER_REFUSED` leaves out. So does its parent, but not in the terminal's hairline. The
`▬` before the figure **is not a leader**: a leader is a run that connects, this is one cell that says
where the figure begins, and the gap itself stays air because this language has committed against drawing
a stroke through one.

### solari — §10 · *"the SEAM is the whole divider vocabulary · A STATE IS A WORD IN A STATUS COLUMN"*

```
field_row   DUE DATE ▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁ 12/09/26    the seam closes the gap
keyhint     up▁MOVE   esc▁CLOSE                         the key, the seam, the word
DISCLOSE    ═   DANGER ▀ ▄   LEVELS "OK " / "DLY" / "CNX"
overlay     a BAND IN REVERSE VIDEO at the head of the schedule
```

**`LEVELS` is the one ladder of the eleven that is not a glyph**, and it is this language's headline
commitment. A departure board does not *draw* severity, it **prints** it — the same argument DATAVIZ law 1
already credits it with for quantity (*"you read `07`, you do not estimate a bar"*). `CNX` for a rejected
field is the language having an opinion rather than borrowing a word: on this board an entry that will not
run is cancelled, and a form field that will not parse is the same event.

Every other language here has to choose how to close a gap; this one had already chosen, and
`rule_line()` returning `None` is the same decision seen from the other side.

---

## 3. Two seats moved, and both were the same hole

**`overlay` got `pane_split`'s refactor.** Industrial and darkside needed their own lids, and an override
of `overlay` would have **bypassed `MODAL_BORDER_REFUSED`** — the exact hole inc28's teeth test found in
`pane_split` three increments ago. So `overlay` is now the entry point nobody overrides, `overlay_box` is
the drawing branch, and `overlay_instead` is the refusal branch. Same shape, both families.

**`MODAL_BOX` is eight cells, in `DISPLAY_BOX`'s order** — (tl, tr, bl, br, top, bottom, left, right).
Six was the first draft and industrial's `▛▀▜` over `▙▄▟` disproved it: half-cell chrome has a different
glyph at the top of a box than at the bottom. Eight also lets industrial write `MODAL_BOX = DISPLAY_BOX`,
which is the honest thing for a language that has already declared its frame.

**Three languages joined `MODAL_BORDER_REFUSED`** — instrument, swiss and solari. Every one of them was
already committed against a lid and had been drawing the terminal's since the seat existed. The registry
is seven now, not four.

---

## 4. What the harness found that the tests did not

`verify_language.py` went red once, on a check written for something else entirely:

```
#46 census: ... every `⡇` still in language.py outside a comment is one of the five claimed seats
```

Instrument's first `DISCLOSE` was `⡇`, which is **spoken for**: that glyph is the half-cell fill this repo
hunted once, and the census keeps a closed list of the five seats allowed to keep it. A sixth live one is
a fill site a pass did not find — so the census did exactly what it was written for, against a change
written three months later. The mark moved to `⠿` (saturated), and `LEVELS` moved off `⠿⠿` with it so the
log's worst row and the "there is more" mark are not the same cell.

---

## 5. Files modified

| file | what |
| --- | --- |
| `taskboard/language.py` | `overlay` split into `overlay` / `overlay_box` / `overlay_instead`; `MODAL_BOX` (8 cells); 3 new `MODAL_BORDER_REFUSED` entries; 30 mechanisms across 5 classes; nord's declaration |
| `tests/test_components.py` | 10 new laws, 40 new tests; two existing registry tests re-pointed at the table instead of a copy of it |

---

## 6. The property test

`test_no_two_languages_answer_a_mechanism_the_same_way`, parametrised over the six mechanisms where a
plain difference is **lawful** — same input, eleven answers, no two the same string of cells.

| | distinct, of 11 |
| --- | --- |
| `field_row` · `DISCLOSE` · `DANGER_FORM` · `LEVELS` · `keyhint` | **11 / 11** |
| `overlay` | **10 / 11** — nord and prism, and the test asserts *exactly* that pair |
| `MATCH_STYLE` | **excluded, by a ruling** |

**`MATCH_STYLE` is absent on purpose and the reason is operator ruling 9**: a result row must come back
byte for byte, so two languages *must* render `match` identically as cells and the only channel left is
style. Its law is `test_the_match_emphasis_is_not_a_hue_alone`, not distinctness. That is worth stating
because it is the one place in this contract where "no two languages agree" is the wrong law.

**The `overlay` exception is named and asserted, not tolerated**:
`test_prisms_overlay_differs_from_nords_in_the_svg_and_not_the_txt` — the two `.txt`s are equal, the two
markups are not, and prism's `depth_ground()` is in its own. A background is not a cell. Third mark in
this contract with that limit, after blueprint's knockout and every language's match.

Beside those: nord's declaration checked through the MRO for all seven; the six new danger forms held to
inc16's law (a pair of marks inside the walls, no hue, and the calm button differs); the six new level
ladders held to ruling 8 (one width, three shapes); solari's three words asserted as words and as the mark
its `error()` row starts with; industrial's lid asserted to be its own plate and **not** `┌`; darkside's
rounded and prism's not; and `MODAL_BOX` eight cells in all eleven.

---

## 7. Test results

```
python -X utf8 -m pytest -q
878 passed, 2 skipped, 4 warnings in 30.74s        (inc31 left it at 835 — +43)

python -X utf8 prototypes/verify_language.py
10857 PASS · ALL PASSED                            (one red found and fixed — §4)

python -X utf8 prototypes/components/render.py
0 hand-drawn elements declared · no two frames identical within a screen (60 pairs)

python -X utf8 prototypes/components/matrix.py
30 of 30 implementa

python -X utf8 prototypes/capture_languages.py --surface      # plain and alone (F-8)
11 surfaces ; no two identical (55 pairs) ; prototypes/gallery/ CLEAN — nothing moved
```

**Nothing in `taskboard/` outside `language.py` consumes any of these seven seats** (grepped), so the 22
committed board frames cannot have moved and `git status prototypes/gallery/` confirms it.

---

## 8. Risks

- **Nord's answer being the base is a claim about doctrine, not a measurement.** If base16 ever stops
  being "inherit the environment", nord has six mechanisms it has never thought about. The MRO test makes
  that a deliberate act rather than a discovery.
- **Prism's overlay is nord's in the `.txt`.** Recorded and asserted, but a review that reads only cell
  grids sees two languages agreeing on a whole dialog.
- **`MATCH_STYLE` distinctness is not a law, and four languages share `bold {ink}`.** That is correct
  under ruling 9 and it means one of the seven mechanisms is unfalsifiable by the property test.
- **Solari's `CNX` is a departure board's word applied to a form field.** It is the language having an
  opinion; a reader who wants "ERROR" will find it wrong, and that is the point of a language.
- **These six render in no frame.** They are exercised by 40 property tests and by nothing anyone can
  look at, because the PROTOTYPE round chose five. A sweep of all eleven through the six screens would be
  180 frames and was not asked for.
- **`required` and `pane_split` are still the base's for these six** — spec §5's declared debt, and two of
  them (swiss, darkside) carry the commitment that puts them in `PANE_SPLIT_REFUSED`.

## 9. For the skill

- **The languages nobody photographs are where a contract rots.** Five diverging implementations and six
  quiet agreements look identical from inside the code and completely different in a sweep. LANGUAGES.md
  should say that a language's second consumer is its first test — it already says that about *apps*, and
  it is equally true about *screens*.
- **A refusal registry must be consulted by a method no language overrides.** Found in `pane_split`,
  re-found in `overlay` three increments later. That is a rule of the pattern, not a detail of a seat.
- **"No two languages agree" is not always the right law.** Where a content ruling forces byte identity,
  distinctness must be asserted on the *channel that is left* — and a property test that quietly includes
  such a mechanism will either fail forever or be weakened until it means nothing.
- **A commitment's FAILURE clause is load-bearing.** Industrial's *"fails when colour must carry
  severity"* decided three of its seven mechanisms. The half of a language description that says what it
  is bad at is the half that tells you what its mechanisms have to be.
