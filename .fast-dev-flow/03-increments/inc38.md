# Increment 38 — the button's walls, in the language that has no boxes

**Batch:** `inheritors-2` · `spec.md` §8's last recorded debt, closed by operator verdict 2026-09-05
**Files:** `taskboard/language.py`, `tests/test_components.py` — **2 source files**.

**Swiss drew `│   Cancel   │`: a pair of full-height vertical rules in the one language whose commitment
is "no boxes, at any width", and the very stroke swiss is already in `PANE_SPLIT_REFUSED` for refusing
between two panes. The walls were defended in a comment that read the choice as WALLS OR NOTHING; the
third option is ONE mark, on ONE side, which cannot enclose anything. Swiss's button is now its own
weight ladder — `·` `•` `●`, three cells it already spends — and DISABLED is air. This was NOT done with
a registry, and §2 says why. The other ten were measured at the same time: swiss was the only one.**

---

## 1. The state this increment found

```
naught ◦  ◦    corgi ▁▁▁▁    instrument ⠇  ⠸    industrial ▐  ▌    nord [  ]
swiss  │  │    darkside ▬  ▬    prism ⣿⣀⣀⣿    ledger │  │    solari ▁  ▁    blueprint ├  ┤
```

Ten of the eleven already declare their own `button.main`; nord declares the base, which is its
commitment. So this was never the inheritance shape inc32/35/36 fixed — **it was one language's own wrong
answer**, written under a comment that conceded it out loud:

> "THE ONE LANGUAGE THAT WOULD RENOUNCE THE WALLS AND CANNOT. Space is this language's structure and a
> bare word would be the honest swiss button — but the label is the CALLER's and may not be restyled, so
> with the walls gone the four states would separate on colour alone, which is the one thing forbidden
> here."

**That reasoning is false, and it is false in one word.** It reads the choice as *walls or nothing*. A
wall is a PAIR — it is border-shaped precisely because it encloses — and there is a third option the
paragraph never considers: **one mark, on one side**. A single cell cannot close a corner at any width,
and it carries a shape channel, so the four states never touch colour.

---

## 2. Why this is an override and NOT a `BUTTON_REFUSED` registry

The brief asked for the shape that matches `pane_split` and `label`. **Neither shape fits, and the reason
is a precondition those two seats have that this one does not.**

`pane_split` and `overlay` needed a registry because their entry points **draw a shared default**: every
language that overrode nothing got `PANE_RULE`, so the only way to make a refusal falsifiable — and
un-bypassable — was a table read *before* the drawing, consulted by a method nobody overrides.

**`Kit.button` has no shared default to intercept.** It composes `component_cells("button", …)` →
`part_glyph("main", state, "button")` → **the language's own `PART_GLYPHS`**. The dispatch is already
per-language, already keyed by language, and already reached from a method no kit overrides. Adding a
registry would put a second, parallel dispatch in front of a dispatch that works.

**And `verify_language.py` already holds it shut**, which is the load-bearing half of the argument:

```
{name}: ... and the word never escapes the control: the render opens with this state's left wall
        and closes with its right, with the label strictly between them
   r.startswith(ws[st][:len(ws[st]) // 2]) and r.endswith(ws[st][len(ws[st]) // 2:])
```

A `BUTTON_REFUSED` branch would render something the language's own declaration does not describe, and
that check goes **red** — so the registry route would have required editing the harness to accommodate
the fix. A registry whose first act is to weaken the law that would have caught it is not the pattern
`pane_split` established; it is the pattern wearing the wrong seat. The declaration IS the registry here,
and the teeth test (§4) is what proves it can still be wrong out loud.

---

## 3. The mechanism, and the ten it was measured against

### swiss — §2 · *"near-mono + one accent · airy · flush-left everything · NO BOXES — alignment does the dividing"*

```
DEFAULT   ·   Cancel        FOCUSED   •   Cancel
ACTIVE    ●   Cancel        DISABLED      Cancel
```

**A weight ladder of one shape, and no glyph is new.** `·` is `LEVELS["info"]` and `stepper.main`; `•` is
`REQUIRED` (inc35: *"the ladder's own mark set solid"*) and the radio knob's bullet; `●` is that knob's
**own ACTIVE cell**, so a press here wears the cell this language already presses with. Weight is the
language's declared hierarchy device and it is a SHAPE channel, so all four survive greyscale — which is
exactly what the deleted comment said was unreachable without a border.

**DISABLED is air, and it is the one decision that is not the ladder.** Nothing in this alphabet is
lighter than `·` except a dashed RULE (`┆ ╎ ┈`) — the shape being given up. So the mark is simply not set,
which is `stepper.step`'s own end behaviour three slots down, in its own words: *"the mark is simply not
set, and the word does not move because the field was reserved for it."* A control nobody may press is a
word, and that is what this language would have said anyway.

**Four cells, split in half like every other language's.** The mark and one cell of air lead the field;
the two cells that used to close it stay air. Same even count, same one width across four states, same
overhead per label — a caller laying out a row of buttons sees no arithmetic change at all.

### The other ten, measured

The question is not "does it draw a box glyph" — blueprint's whole alphabet is box glyphs and its
commitment licenses them. The falsifiable question is **does a language rule, around a word, the stroke
it has already declared with a citation that it may not rule between two panes** — `Kit.PANE_RULE`, off
`PANE_SPLIT_REFUSED`, which is a registry and not a reviewer's eye.

```
language    default  pressed   in refusal table   PANE_RULE round the word?
naught      '◦  ◦'   '●●●●'    modal              no
corgi       '▁▁▁▁'   '▄▄▄▄'    modal              no
instrument  '⠇  ⠸'   '⣇⣀⣀⣸'    modal              no
swiss       '·   '   '●   '    pane, modal        no      <- was YES
industrial  '▐  ▌'   '▐##▌'    -                  no
nord        '[  ]'   '▓▓▓▓'    -                  no
darkside    '▬  ▬'   '█  █'    pane               no
prism       '⣿⣀⣀⣿'   '⣿⣿⣿⣿'    pane               no
ledger      '│  │'   '▶  ◀'    modal              YES     <- legal, see below
solari      '▁  ▁'   '▂  ▂'    pane, modal        no
blueprint   '├  ┤'   '┣  ┫'    pane, modal        no
```

**Swiss was the only one, and the frame proves it rather than asserting it.**

- **ledger's `│` is the one YES and it is legal.** Ledger is not in `PANE_SPLIT_REFUSED` — it *draws* a
  pane rule (`═══` / `│`) because a ruled sheet's column rule is its structure device. It is in
  `MODAL_BORDER_REFUSED` on a different commitment entirely (*"a ledger has no surface IN FRONT OF the
  page"*), which says nothing about a stroke beside a word. The law is keyed to the pane table for
  exactly this reason.
- **blueprint's `├  ┤` is its registration pair**, the marks §11 calls the frame that *"stops CONTAINING
  and starts MEASURING"* — two datum terminators facing the word, which never join. Cited already.
- **darkside's `▬  ▬` / `█  █` are its weight marks**, not borders: `▬` is its own `CUR` and the seat its
  `field_row` stands a figure on, and §8 names WEIGHT as the channel its "never borders" leaves open.
  This is the closest call of the ten and it is recorded as such in §6.
- **prism, solari, instrument, naught, corgi** answer from their own alphabets; **industrial's** commitment
  asks for a box; **nord** declares the environment.

### And one thing the frame found that nobody had asked

**`instrument`'s button opens with `⠇`, which is that language's ERROR rung** (`LEVELS["error"] == "⠇⠇"`).
inc36 chose `⠸` for its pane gutter *specifically* to avoid this cell — *"a neutral divider wearing the
severity ladder's cell would say 'rejected' down the whole gutter to a greyscale reader"* — and wrote
`test_instruments_graticule_column_is_not_its_error_rung` to hold it. The button had the same collision
one seat earlier and no test looks at it. **Not fixed here** (this increment is swiss's), recorded in §7.

---

## 4. The property tests

| test | what it holds |
| --- | --- |
| `test_swiss_puts_no_wall_around_a_button_at_any_width` | no box-building mark at `w ∈ {1, 10, MEASURE_MIN}` × four states × danger on and off. The mark set is DERIVED from the codepoint (Box Drawing minus its three diagonals, plus every Block Element), not hand-listed — the claim is about marks nobody has thought of yet |
| `test_the_swiss_button_keeps_its_states_apart_without_a_wall_or_a_hue` | four states, four different strings of cells, ONE width, colour stripped at the source; ACTIVE ≠ FOCUSED and FOCUSED ≠ DEFAULT asked again on their own. This is the deleted comment's claim, disproved |
| `test_the_swiss_buttons_ladder_is_made_of_marks_it_already_spends` | every cell appears elsewhere in swiss's own declaration; `·` **is** `LEVELS["info"]` and `•` **is** `REQUIRED`, asserted against the tokens rather than typed; DISABLED asserted blank |
| `test_putting_the_walls_back_makes_the_no_wall_law_go_red` | **teeth, both arms.** Restore the pre-inc38 declaration byte for byte → `│` comes back and the law fires. DELETE the declaration → `part_key` falls back to the unscoped `main` and the button comes back wearing the slider's track. Both are walls; neither is silent |
| `test_no_language_that_refuses_the_pane_rule_draws_it_round_its_button` (×5) | parametrised **off `PANE_SPLIT_REFUSED`**, so a sixth language joining that table is asked about its button the moment it is added — declaration and render both |

`╲ ╱` is excluded from the wall set **on purpose and it is not a loophole**: it is swiss's own
`DANGER_FORM`, which `Kit.button` sets around the WORD and not around the field, a stroke that leans
closes no corner, and inc16's law already governs it. The no-wall law is asked of the danger button too,
so those two are the only marks in that range it may contain.

---

## 5. Test results

```
python -X utf8 -m pytest -q tests/test_components.py   588 passed in 0.83s      (was 579)
python -X utf8 -m pytest -q                            942 passed, 2 skipped in 34.46s   (was 933)
python -X utf8 prototypes/verify_language.py           ALL PASSED  (exit 0)
python -X utf8 prototypes/components/render.py         66 .txt + 66 .svg · 66 candidates ·
                                                       no two frames identical within a screen (330 pairs) ·
                                                       0 hand-drawn elements declared (0 refused, 0 evoked)
python -X utf8 prototypes/components/matrix.py         66 of 66 implementa · no primitive missing in any
                                                       screen · refusals [] in all eleven
python -X utf8 prototypes/capture_languages.py         22 grids identical across two PROCESSES ·
                                                       22 captures · no two boards identical
python -X utf8 prototypes/export_to_skill.py <skill>   languages.py 22 KB, 11 languages · verified: every
                                                       token, doc and family round-trips ·
                                                       captures: 2 written, 64 already identical ·
                                                       SURFACES.md (11 postures)
```

### The frames that moved, byte-wise

```
M prototypes/components/swiss_S2.{txt,svg}     Save (DISABLED) + Cancel
M prototypes/components/swiss_S3.{txt,svg}     Delete all (danger)
M prototypes/components/swiss_S4.{txt,svg}     Delete (FOCUSED, danger) + Cancel
M prototypes/gallery/gallery_swiss.{txt,svg}   the component sheet's button block, four states
```

**Four frames, all swiss, and nothing else in the 88.** The other 63 component frames and the other 21
board/gallery captures rewrote byte-identically.

```
swiss_S4   before   ┃  ╲Delete╱  ┃   │   Cancel   │
           after    •  ╲Delete╱      ·   Cancel

gallery_swiss       · ok    · Refresh     default
                    • ok    • Refresh     focused
                    ● ok    ● Refresh     active
                      ok      Refresh     disabled
```

**`capture_languages.py --surface` was NOT run, and that is a decision with a reason.** Its input is
`k.surface()` — the raster posture — which this increment did not touch (swiss's is `""`, emptiness).
`main()` and `--surface` write disjoint frame sets, and the eleven `surface_*.txt` are untouched on disk.

---

## 6. Risks

- **A DISABLED swiss button is a bare word.** `swiss_S2` now reads `     Save        ·   Cancel`, and the
  only thing saying Save is unavailable is the absence of a mark plus the dim tier — which the `.txt`
  cannot show. It is the language's own idiom (`stepper.step` does exactly this) and the caption under it
  happens to explain itself (*"Save is held until due parses"*), but **a disabled control that looks like
  a caption is a real interaction risk** and no test can see it. It is the one thing in this increment
  most likely to come back from a UX read.
- **Two cells of trailing air are now structural.** The button keeps its 4-cell overhead so the seat's
  arithmetic does not move, which means the right half is air that exists only to preserve a width. That
  is defensible (the field was always reserved) and it is also the kind of thing a later reader deletes.
- **`·` now means two things in swiss.** It is `LEVELS["info"]` and it is a resting button. Within-language
  reuse is already established here (`DISCLOSE` and `LEVELS["warn"]` are both `─`) and the two never
  appear in the same column — but nobody has looked at a log row beside a button row.
- **darkside's `▬  ▬` is the closest remaining call** and this increment cleared it by argument, not by
  test: `▬` is its `CUR` and its `field_row` seat, and §8 names weight as the channel its "never borders"
  leaves open. A reviewer who reads two marks flanking a word as a border will disagree, and the file
  carries no citation for the button the way it does for the pane.
- **The law is keyed to `PANE_SPLIT_REFUSED`.** That is what makes it grow with a registry instead of a
  hand list — and it also means a language that commits against boxes **without** joining that table is
  not asked. `MODAL_BORDER_REFUSED` was deliberately not used (ledger's entry there is about surfaces in
  front of a page, not about strokes), and that choice is the law's boundary.

## 7. Pending

- **`instrument`'s button opens with its own ERROR rung** (`⠇`, §3). inc36 refused that cell for the pane
  gutter and wrote a test for it; the button has the same collision and no test. Named, not fixed.
- **Swiss's `checkbox`, `textfield` and `radio` still carry `│ ┃ █` walls** against the same commitment,
  each defended by a comment of the same shape the button's just lost (*"a value may fill every cell, so
  a walled-off field is the only place a full one can say DISABLED without colour"*). The button's ladder
  is the counter-example to that argument at one seat; whether it transfers to a seat with an INTERIOR is
  a genuine open question and not a formality.
- **The four moved frames have not been judged.** No PROTOTYPE round, no operator verdict — same standing
  as the 36 frames inc37 shipped.
- **The skill repo is left dirty on purpose** — `assets/languages/gallery_swiss.{txt,svg}`. The operator
  commits it.
- **`tests/test_components.py` carries a duplicated inc37 block**: `FRAMES`, `SCREENS` and three tests
  (`test_every_language_has_a_frame_for_every_screen`,
  `test_no_two_languages_render_a_screen_identically`, `test_no_frame_declares_a_hand_drawn_element`) are
  defined twice, so the first copy of each is dead. No false green — pytest runs the second — but it is
  three tests' worth of code nothing executes. Found here, not touched here (rule 3).

## 8. Suggested next task

inc39 — the two findings above as one increment: instrument's button off its error rung, and swiss's
`textfield` / `checkbox` walls put to the same question the button just answered. Both are one-language,
one-token changes with a frame each, and both already have the law they would be asserted under.

---

## Evidence checklist

- [x] **Tests/type checks/lint pass** — `942 passed, 2 skipped` (§5). `verify_language.py` **ALL PASSED**,
      exit 0, including the per-language wall laws (even count, one width, four distinct shapes, press ≠
      focus, render opens and closes with the declared halves). `render.py` 66 frames / 330 pairs / 0
      hand-drawn. `matrix.py` 66 of 66. `capture_languages.py` 22 grids identical across two processes.
- [x] **No secrets in code or output** — one glyph table, one comment, five tests. No network, no
      dependency, no path outside the worktree and the skill's own asset directory.
- [x] **No destructive commands run without approval** — none. Every artefact rewritten was rewritten by
      the script that owns it; the four that moved are listed byte-wise in §5.
- [x] **File count within cap** — 2 source files (`taskboard/language.py`, `tests/test_components.py`),
      plus this packet and the `spec.md` §8 amendment: 4. Frames and skill assets are generated artefacts.
- [x] **Review packet attached** — this document.
