# inc88 — the three cursors, the dither and the thin asterisk: the `EFF` column emptied

Batch `rework-9`, increment 2 of 4.

## §0 — the rulings, verbatim

Rulings (orchestrator, 2026-09-07, on the operator's delegation):

- **Declared seat by seat, not by character:** the declared-seat derivation intersects the mark with
  the seat its contract method paints (`log_row`'s rung column, not any cell with the same
  character); prose never counts.
- **Cursors are marks:** the three cursors in `accent` (instrument `⣿` 2.94, swiss `▮` 2.57,
  industrial `▶` 2.97) obey Q1's effective clause; fix by the smallest hue-preserving lightness step
  of `accent`, and re-run the match-tier law (inc73) since `accent` is a match ink in some kits: both
  must hold.
- **Drawing problems are fixed by drawing:** corgi's invalid wall `░` (1.44 in ink, a dither) takes
  the heavy shade `▓` (panel register, inc67), and ledger's warn rung `*` (2.86 on light paper) takes
  a heavier printer's mark by area from ledger's own alphabet (`¶`, `§`, `※` or `**`'s sibling; cite
  #9 and keep error distinct), both judged by Q1 at the seat.
- **Both-clause seats move by area** (inc82's kind): the eight seats failing coverage AND contrast
  take a bigger glyph from their language's alphabet; `naught ◦` (13.5 %) is among them and gets no
  eye exemption.
- **naught_S2 L10:** the 12 homoglyph rows and 8 state rows on naught's form are fixed by SHAPE and
  COUNT (the lattice counts, the pixel charges: inc61), so the form's marks stop resting on one
  drawing.
- **inc84 §6 correction:** the packet's claim "gallery 30–51 none changed" was read off
  `prototypes/gallery/` (boards), not the component grids; entries 35 and 36 did change. Correct the
  packet in place with a dated note, never silently.

This increment is the **second** and the **third**.

## §1 — cause

`BELOW_THE_FLOOR` had five rows left whose ONLY failure was Q1's effective clause, and they were the
two kinds inc85's remedy could not reach:

- **three cursors painted in `accent`.** inc85's ruling moves marks out of `mut` and `dim`; `accent`
  is neither, and repainting a cursor in `ink` deletes the one channel that says WHERE YOU ARE. The
  family fails as a **family** — 2.94, 2.57, 2.97, one of them three hundredths under.
- **two marks already in the loudest neutral their kit owns.** corgi's `░` is a DITHER: 68.4 % of the
  cell covered and 1.44 effective, because at 9×19 its lit pixels are almost all partway back to the
  ground. ledger's `*` is a small high asterisk on the corpus's one LIGHT ground, where `ink` is as
  loud as neutral gets, and it measured 2.86 there. **No tier fixes either; only another cell does.**

## §2 — mechanism

### The three cursors: one token, three sizes of step

Each kit's `accent` takes the **smallest** step along its own hue/saturation ray that clears 3:1
effective at the cursor's declared seat. The ray is walked at 0.0002 of a lightness turn — finer than
8 bits can represent — so every colour available between the two was tried and every one of them
still misses.

| kit | cell | was | now | ΔL | Δhue | eff | declared |
| --- | --- | --- | --- | --- | --- | --- | --- |
| instrument | `⣿` | `#2dd4bf` | `#39d7c3` | +0.0290 | −0.05° | 2.94 → **3.01** | 10.45 → 10.82 |
| swiss | `▮` | `#e7372e` | `#eb574f` | +0.0720 | +0.16° | 2.57 → **3.00** | 4.52 → 5.44 |
| industrial | `▶` | `#ff6039` | `#ff623b` | +0.0038 | +0.12° | 2.97 → **3.00** | 5.79 → 5.85 |

**The three steps differ by a factor of eighteen**, which is the reason this is a roster and not a
rule: a single "brighten the accent" would have overshot two of the three.

### corgi: the cell the ruling named, and the one the census allowed

`▓` clears Q1 (100 % coverage, 3.47 effective) and **it was refused**. It is the cell corgi's
textfield already wears when it is ACTIVE — and the switch indicator's, the checkbox knob's, the
radio's, the button's, the stepper's, the pane rule's and the mascot's. Taking it was measured, not
argued: `collision_census.py` went **27 → 28** and `▓` came back carrying **nine families**, one of
them *"you are typing here"* on the very field whose rejection it would have been spelling. That is
**ruling C reversed** and it is the exact defect inc52 fixed — which is why `░` was chosen: *"the one
cell in this language's block alphabet that no meaning and no other control state spends"*.

The criterion was kept and the family moved. The shade ramp has no free cell (`▒` and `▓` are both
control states); inc58 forbids drawing a control as a driven bar, which rules out every eighth-block;
what remains is the **quadrant family**, which is already this field's wall vocabulary (`▛▛·▜▜`
focused, `▛▛▒▜▜` edited). The two diagonal halves are free in every state of every control this kit
draws, and they mirror like every other wall pair here: **`░░·░░` → `▚▚·▞▞`**, 57.9 % at 12.80 and
60.2 % at 13.83. The knob and the stepper come with it (inc51 clause 2: whatever cells the kit spends
on a rejected value at its knob and its field are the cells its stepper spends).

**The reading changes with the drawing and it is a better one.** A ghost says *the machine did not
drive this*; a strike says *the machine refused it*, which is what the state means.

### ledger: the printer's order, advanced by one

The kit's own comment declares the mechanism: *"REFERENCE MARKS ARE ASSIGNED, NOT RANKED. The
printer's order is `* † ‡ § ‖ ¶`; `†` and `‡` are spoken for above, so the ladder takes the FIRST
mark of that order and DOUBLES it."* So the ladder does not need a new idea, only the next free mark
of the order it already declares:

- `†`, `‡` — still spoken for (REQUIRED, INVALID);
- `‖` — **not in the face this corpus is measured on.** It rasters as the fallback box: 39.2 % at
  6.24, which is the identical figure eleven other absent glyphs return, and that is how it was
  detected;
- `§` — free in every state of every control this kit draws.

`* ` / `**` → **`§ ` / `§§`**. 30.4 % → 51.5 % coverage, 2.86 → **4.42** effective in `ink` (2.45 in
`mut`, which is why the seat stays in `RUNG_TAKES_INK`). **The doubling is untouched** — the ladder
still COUNTS, which is this language's own commitment and the reason `error` stays distinct without a
second shape. The ruling's *"cite #9"* is round five §7 row 9, `naught ∙` at 14.0 %: *"la mas facil de
las diez … un disco macizo"* — a reader finds MASS.

## §3 — law

| law | what it binds |
| --- | --- |
| `test_the_cursor_took_the_smallest_hue_preserving_step_that_clears` (×3) | (a) the kit's token holds the new value today and the cursor is painted in it, read off `menu` and not off the table; (b) both numbers reproduce off the pixels to 2 dp at the old value AND at the new one; (c) the step CROSSES the clause; (d) hue moves < 0.25° and saturation < 0.01, and the step is upward; **(e) it is the SMALLEST — every colour the hue's own ray can reach between the two still misses** |
| `test_the_swiss_red_is_one_hue_at_two_lightnesses_and_says_why` | the light red clears Q1 at the cursor and fails inc73 at the match; the dark red does the reverse; the hue is one hue. **Neither value can do both jobs**, which is the whole content of "both must hold" |
| `test_a_mark_no_tier_could_fix_took_another_cell_of_its_own_alphabet` (×3) | (a) the old cell is gone from that family's declared seats and the new one is there; (b) all four numbers reproduce off the pixels; (c) the new cell clears BOTH clauses where the old missed at least one — a replacement trading contrast for area is red; **(d) the new cell is FREE: the census credits it to this family in this kit and to no other** |
| `test_the_cell_the_ruling_named_is_one_the_census_refuses` | the refusal is a COUNT, not a sentence: `▓` is spent by ≥ 8 families in corgi today, `invalid` is not among them, and it is asserted to CLEAR Q1 — so it is on record that it was refused for the right reason |
| `test_the_uncured_table_is_empty_and_the_corpus_agrees` | the roster is empty AND the corpus produces no row for it, swept over all eleven at once; and the sweep is asserted **not** empty of everything — the floor is still failed, by area, in six kits |

**`EFFECTIVE_UNCURED` is kept and empty.** An empty roster with a symmetric law over it is a claim; a
deleted roster is a silence. `test_no_meaning_mark_that_only_misses_the_contrast_clause_is_left_quiet`
now asserts the ruling itself with no roster between: **no meaning mark in this corpus misses Q1's
effective clause alone.**

## §4 — teeth

- **`test_the_cursor_step_bites_when_the_token_goes_back`** — three arms, one per kit, because three
  steps of three sizes are three different things to break; the old value is also asserted to MISS
  the clause, so the red is a measurement and not a string comparison. **And a fourth kind of arm for
  the word SMALLEST:** overshoot by ONE colour on the same ray. Every other clause still holds — the
  hue is preserved, the step is upward, the cursor clears — so if clause (e) were decorative the
  mutant would pass.
- **`test_the_area_cure_bites_when_the_mark_goes_back`** — two arms because the two mechanisms are
  different (`PART_GLYPHS`, a control state; `LEVELS`, a meaning ladder), and a third that is the one
  worth having: **corgi's invalid wall set to `▓`, the cell the ruling named.** The freedom clause
  must go red — on a cell that clears Q1 and would pass every other clause in the file. Without that
  arm the refusal would be a comment.
- **`test_the_ink_move_bites_when_one_seat_keeps_its_mut`** — its old vacuity arm emptied
  `EFFECTIVE_UNCURED`, which since this increment would do nothing. The mutant now goes the other
  way and puts a row IN: a row named with no failing seat behind it must be as red as a failing seat
  with no row.

## §5 — what was found by looking

**1. The cell the ruling named would have re-created the defect inc52 fixed, and the census said so
in one number.** 27 → 28, `▓` carrying nine families. This is the second time in two increments that
a ruling written from the report met a fact only the corpus had.

**2. And the cell taken instead CLOSED a collision nobody was aiming at: 27 → 26.** `░` was never as
free as inc52's comment claimed. It said *"no meaning and no other CONTROL STATE"* and that was true;
what it did not cover is the **B set** — `meter.track`, `spark.floor` and `scrollbar.main` all spend
`░`, and inc67's ruling A-amended brought those into the census two batches after inc52 wrote the
sentence. So corgi's `░` had been a three-family collision the whole time, and the freedom criterion
this increment applied — *no other family at all* — is strictly stronger than the one inc52 could
state. **corgi 4 → 3 colliding cells, TOTAL 27 → 26**, and it is the first fall in this programme's
census that was a side effect rather than a target.

**3. swiss's one red cannot be both inks, and the arithmetic is a scissors.** Q1 pushes the cursor's
ink UP in lightness; inc73's achromatic fallback asks the match ink to stay 1.5:1 in luminance away
from `mut`, which pushes it DOWN. The whole-token move was made first and measured:
`test_the_match_run_is_legible_and_distinct_on_its_declared_channel[swiss]` went red at **1.26**
against a floor of 1.5. So `accent` moved alone and `warn`/`alert` kept `#e7372e`. **The kit still
spends one HUE at two lightnesses**, which is what its own grey ladder does three times over — and
the ruling's *"both must hold"* is exactly what forced the split.

**4. `‖` is not in the face, and the fallback box is how you can tell.** Eleven candidate glyphs
returned **39.2 % coverage at 6.24 effective**, to six digits, because they are all the same tofu
rectangle. A candidate list checked by eye would have taken `‖` as the next mark of the printer's
order and shipped a box in eleven kits' worth of logs.

**5. L12 moved for instrument and did not for swiss, and the difference is which token the match
spends.** instrument's `MATCH_STYLE` is `underline {accent}`, so the cursor's step carried the grey
match with it: **2.34 → 2.42**, the only one of the four Limits that has ever improved. swiss's is
`bold {alert}`, and `alert` did not move — so swiss keeps 1.52, the corpus's thinnest reading, and
keeps it for the reason finding 3 names.

**6. The `EFF` column is empty and the arithmetic behind it is four increments and four different
kinds of failure.** 29 → 6 (inc85, a quiet tier under a floor written for text) → 5 (inc87, a row
that was never a seat) → 0 (inc88, a hue and two drawings). **What is left under the floor is
coverage, and coverage only** — four rows that miss area alone and eight that miss area and contrast.
Not one row in `BELOW_THE_FLOOR` is a tone question any more, which is the shape the round asked for
when it made Q1 two clauses instead of a product.

**7. The bound-seat count ROSE for the first time, 84 → 85, and it is a drawing.** corgi's invalid
wall stopped being one cell repeated and became a mirrored pair, so one seat became two. Three moves
in three increments and no two of them the same kind of event (89 → 86 tier, → 84 derivation, → 85
drawing), all three asserted.

## §6 — files and frames

| file | change |
| --- | --- |
| `taskboard/themes.py` | three `accent` values, each with its measurement and its step; swiss's split from `warn`/`alert` with the scissors written out |
| `taskboard/language.py` | corgi `textfield.main[INVALID]`, `knob[INVALID]`, `stepper.step[INVALID]`; ledger `LEVELS`; the `RUNG_TAKES_INK` roster row for ledger; instrument's L12 paragraph (2.34 → 2.42) |
| `tests/test_components.py` | `CURSOR_TOOK_A_LIGHTNESS_STEP`, `SWISS_RED_SPLIT`, `MARK_CURED_BY_AREA`, `REFUSED_BY_THE_CENSUS`, `_hls`, `_ray`; five laws and two teeth; `BELOW_THE_FLOOR` 12 → 7 keys, `FLOOR_SEATS_BOUND/FAILING` 84/17 → 85/12, `EFFECTIVE_UNCURED` emptied, `SEATS_MOVED_TO_INK` two cells replaced, `MATCH_IN_GREY["instrument"]` 2.34 → 2.42, `MEANING_MARKS` (79, 38) → (80, 37), `test_ledgers_two_daggers_are_an_order_and_not_a_pair` asserts the ORDER rather than the letter |
| `prototypes/out/legibility.txt` | 876 → 879 lines; §F re-measured (two rows where corgi had one) |
| `prototypes/out/collision_census.txt` | corgi 4 → 3 colliding cells, TOTAL 27 → **26** |

**Frames changed:**

```
100x32   3 .txt   corgi_S2 · ledger_S2 · ledger_S5      (the two new drawings)
        21 .svg   the same 3, plus 6 x instrument, 6 x industrial, 6 x swiss
                  (colour only -- an accent is a tone, not a cell)
 80x24   the same 3 .txt and 21 .svg
  png    42 files (14 frames x colour + grey + json)
gallery  6 .svg -- board_ and gallery_ for industrial, instrument and swiss.
         The other 16 byte-identical.  Counted by looking for the accent.
```

**Gallery 30–51, byte-wise in `.txt`, read off `prototypes/components/`: entry 40 `ledger_S2`, and
no other.** `corgi_S2` and `ledger_S5` also moved and neither is a source. The `.svg` half of that
comparison is not meaningful and is said so here rather than reported as a change: the skill's
`assets/gallery/svg/` frames are rendered by that directory's own `render_svg.py`, so all
twenty-two differ from `prototypes/components/*.svg` and always have — `corgi_S3.svg`, which this
increment did not touch at all, differs too.

## §7 — deviations, named

- **The ruling's `▓` was refused, and the refusal is §5.1 with a number and a law behind it.** The
  cell taken instead is out of the same kit, satisfies the criterion inc52 stated, and closed a
  collision. If the round wants `▓` anyway, the change is one line, the cost is a ninth family on a
  cell and a census row, and `REFUSED_BY_THE_CENSUS` is where the argument lives.
- **swiss's `accent` moved alone**, against the kit's "one red" declaration and inc73's own
  precedent of moving all three together. §5.3 is the measurement that forced it; the alternative
  was shipping a match ink red under inc73, which the ruling's "both must hold" forbids.
- **`warn` and `alert` moved with `accent` in industrial** and not in swiss. industrial's own theme
  comment declares them one hex *"by declaration"* and industrial's match is a `reverse` plate whose
  numbers do not move; swiss's match is the hue itself. The rule applied is the same in both: move
  every token the kit declares as one value, unless a measured law forbids it.
- **`ledger`'s seat stays in `RUNG_TAKES_INK`.** `§` in `mut` measures 2.45, still under the clause,
  so the tier move inc85 made is still what carries it. Only the drawing changed.
- **The census TOTAL moved and nothing was done about it.** 27 → 26 is a collision CLOSING, which is
  the direction this programme wants; it is recorded in §5.2 and in `spec.md` rather than pinned,
  because no law in the suite pins the total and inventing one here would be a fifth thing this
  increment did.
- **`naught ◦` is untouched.** It misses both clauses and is inc89's.

## §8 — gates

```
pytest -q                1488 passed, 2 skipped, 26 warnings in 45.74s
                         (inc87 1478 -> 1488, +10: 11 new laws and teeth,
                          minus `test_the_uncured_table_covers_what_it_claims_
                          to`, whose subject is an empty roster and which is
                          replaced by `test_the_uncured_table_is_empty_and_the_
                          corpus_agrees`.  ZERO failed --
                          test_win_clipboard_roundtrip passed in this run)
verify_language.py       ALL PASSED                                     exit 0
render.py                66 .txt + 66 .svg / 330 pairs / 0 hand-drawn    exit 0
raster.py                132 PNGs identical across two PROCESSES
                         (66 colour + 66 grey)                          exit 0
legibility.py            879 lines · byte-identical across two PROCESSES exit 0
second_width.py          0 rows cut in 0 frames · 330 pairs distinct     exit 0
matrix.py                refusals [] for all eleven                      exit 0
collision_census.py      TOTAL 27 -> 26 · homoglyph rows 24 (unchanged)  exit 0
capture_languages.py     22 grids identical across two PROCESSES ·
                         6 gallery artefacts moved (3 frames)            exit 0
export_to_skill.py       runs at the batch close (inc90)
```

`BELOW_THE_FLOOR`, old → new: **17 → 12 rows.** The five that left are `corgi invalid ░`,
`instrument cursor ⣿`, `swiss cursor ▮`, `industrial cursor ▶` and `ledger severity *`. The twelve
that remain are four `COV` and eight `COVEFF`, and **every one of them is an AREA failure**:

```
naught      severity ∙ #8a8a8a  COV      14.0%   3.50    the muted rung
naught      severity ∙ #f5f5f5  COV      14.0%   9.66    the same rung in ink
naught      danger   ∙ #f5f5f5  COV      14.0%   9.66    DANGER_FORM
swiss       required • #f4f4f4  COV      14.0%   9.13    exempt by EYE (inc86)
naught      severity ◦ #8a8a8a  COVEFF   14.0%   2.40  ] the eight the round
instrument  severity ⠂ #6e7b89  COVEFF    5.3%   1.90  ] put in its ten worst
instrument  severity ⠆ #6e7b89  COVEFF   10.5%   1.90  ] by eye; inc89's brief
swiss       severity · #9b9b9b  COVEFF    4.7%   2.64  ]
nord        severity · #919cb0  COVEFF    4.7%   2.26  ]
darkside    severity · #757575  COVEFF    4.7%   1.90  ]
prism       severity ⣀ #8b98a5  COVEFF    9.9%   2.38  ] two rows, two grounds
```

## §9 — pending / next

- **inc89** — the eight both-clause seats by area, `naught ◦` included and with no eye exemption.
- **Handed back by this increment:** the census total fell to 26 and no law pins it (§7); `‖` and
  ten other candidate glyphs are absent from the measured face and nothing in the repo detects a
  fallback box except by its coincident numbers (§5.4).
