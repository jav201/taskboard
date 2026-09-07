# inc82 — the two required marks by area (instrument `⠁`, prism `⡀`)

Batch `rework-8`, increment 2 of 4.

## §0 — the rulings, verbatim

Rulings (orchestrator, 2026-09-07, on the operator's delegation), all adopted from round five's
recommendations:

- **Q1:** the legibility floor is two clauses, not a product: coverage ≥ 15 % of the cell AND
  effective contrast ≥ 3:1, both at the declared seat.
- **Q2:** runs of 1–4 cells carrying an A-family role are bound by the floor; runs of ≥ 8 cells of one
  glyph are structure, bound only to "not equal to the ground"; 5–7 named per seat like
  `DIM_CLASSIFIES`.
- **Q3:** the floor is judged at the declared seat; the worst seat is reported as a notice, never red.
- **F at 24 rows:** the band takes the nearest full-measure position that cuts no gate block, below
  first then above; if neither fits, the band is the whole page (a full-screen confirm);
  `LANGUAGES.md` gets no minimum height.
- **K8/E6:** a run of blank cells on a non-ground background is ink; the census, `painted_runs()` and
  `legibility.py` count it (18 runs in 3 kits today); it obeys Q2 as structure.
- **Greyscale:** `raster.py` also writes a greyscale PNG per frame (luminance only); L12's three
  hue-only match channels are judged on it, and a match that vanishes in grey is recorded as a Limit
  of the language, not fixed.

## §1 — cause

Round five returned `instrument_S2` and `prism_S2` as **rework** on one axis, and it is not the axis
four rounds had been arguing about:

| kit | mark | coverage | effective | **declared** | round five's criterion |
| --- | --- | --- | --- | --- | --- |
| instrument | `⠁` | **5.8 %** | 3.77 | **16.52:1** | *"point at the required fields." No answer.* |
| prism | `⡀` | **5.3 %** | 4.40 | **16.02:1** | *"point at the required fields." No answer.* |

**They hold the two best declared contrast ratios of the eleven obligations and they are three
pixels.** No amount of contrast fixes either one, and no ratio can say so — which is exactly the
arithmetic that made ruling Q1 two clauses instead of a product, and exactly why inc35, inc46 and
inc59 all reasoned correctly about these two cells and still shipped a mark nobody can point at: the
`.svg` carries a colour and not a drawing.

`⡀` had a second job as well. `Prism.FIELD_LEAD` is `⡀⡤⣶`, so **every read-only definition row in
`prism_S1` opened on the obligation mark** — one cell, two roles, and the census had the row.

## §2 — mechanism

**Both fixes are AREA and only area.** Neither kit's ink, ground or declared ratio moved; what moved
is the drawing.

### instrument `⠁` → `⣉` — the datum pair

inc35's argument is kept intact and only its failing clause is replaced. Severity in this language is
dot **count** up the **left column** (`⠂⠂ / ⠆⠆ / ⠇⠇`), so an obligation — a property, not a severity —
may not join the count; `⠁` said that by sitting at the top of the cell, off the ladder. `⣉` is the
cell's **top row and its bottom row**, lit together: a scope's **datum pair**, the two marks that say
where a reading is bounded.

- it cannot join the ladder, and not by convention — the ladder is a **column** read as a count and
  this is two **rows**, an axis a column count has no way to express;
- it still opens at the top of the cell, where a trace enters (inc35's own words);
- it is not `⠒`, the graticule this language rules a field row with, and not `⠸`, the graticule
  **column** inc46 gave the pane seat *because* `⠇` (the left column) is the error rung;
- **zero occurrences in the 66 frames before this change.**

**5.8 % → 23.4 % coverage; effective 3.77 → 3.77; declared 16.52:1 unchanged.**

### prism `⡀` → `⣆` — the frontier risen

The ember is *"a solid field being consumed"* and the frontier works at **half-cell precision**
(the kit's own docstring, and inc59's *"the ember is read from the bottom; a control is read from the
top"*). `⣆` is the bottom row alight with the frontier risen one step on the **leading edge** — one
step above `⡀` and below every rung.

- it is not a severity rung and cannot be read as one: the rungs are **flat bands** (`⣀` one row,
  `⣤` two, `⣿` four) and this is a **rising edge**;
- the one declared cell a dot away from it, `⣇`, is a `stepper.step` state no frame renders — which
  is checkable, and is checked, rather than asserted;
- **zero occurrences in the 66 frames before this change.**

**5.3 % → 21.6 % coverage; effective 4.40 → 4.22; declared 16.02:1 unchanged.**

## §3 — law

| law | what it binds |
| --- | --- |
| `test_every_required_mark_passes_the_floor_at_its_declared_seat` | **the brief's law**: every obligation clears Q1 at its own declared seat, one bound seat per kit, all eleven clearing the contrast clause, and the coverage clause failing **exactly** `OBLIGATION_UNDER_THE_FLOOR` — in both directions |
| `test_the_two_replaced_marks_are_the_ones_the_kits_now_declare` | the before-mark **re-measured** through the same restated arithmetic, on each kit's own ink and ground: `was < 15 % ≤ now`, both over 3:1, contrast untouched; and the new cell present in the `.txt` at **both** widths |

`test_the_eleven_obligations_are_judged_at_their_own_declared_seat` (inc81) is **replaced**, not kept
beside its successor: two laws over one seat with two recorded sets is the drift
`test_the_homoglyph_table_is_one_table_in_two_files` exists against.

## §4 — teeth

- `test_the_obligation_floor_bites_on_the_marks_inc82_replaced` — the roster is mutated in **both**
  directions: park a kit that is not under the floor in `OBLIGATION_UNDER_THE_FLOOR` (red), and empty
  the roster entirely (red). The mutant is the **declaration**, never the artefact: `floor_rows`
  reads the shipped PNGs, so restoring `Kit.REQUIRED` alone would leave the pixels where they are and
  prove nothing.
- `test_the_floor_law_bites_on_a_row_of_the_recorded_set` — inc81's tooth, **re-pointed**. Its
  original mutants were instrument `⠁` and prism `⡀`, and inc82 removed both rows by fixing the
  marks. *A tooth whose mutant has been fixed is a tooth that bit.* It now points at two rows the fix
  did not touch and at two different failure modes — swiss `•` (COV) and darkside `·` (COVEFF) — plus
  a grow-the-set arm.
- Two **pre-existing** teeth moved with the marks and were re-derived, not silenced:
  `test_the_named_seat_law_goes_red_on_the_three_declarations_it_moved` now reads the obligation
  **off the kit** instead of spelling `⠁`; and `PRISM_EMBER_BEFORE`'s `stepper.step` opener score
  drops 1 → 0 with the total 25 → 24, because the pre-inc59 stepper opened on `⡀` and `⡀` scored only
  as `Prism.REQUIRED`. **The historical defect those teeth reproduce is one seat smaller than it
  was**, and the table's declaration is unchanged — only what it costs.

## §5 — what was found by looking

**1. `collision_census` TOTAL 28 → 27.** Moving the obligation off `⡀` closed the `required` +
`field.leader open` row on that cell. The homoglyph rows are unchanged at 24. Nothing in the suite
pinned 28; `prototypes/out/collision_census.txt` carries the new number and it is named here so it
does not read as drift in six documents that quote it.

**2. `MEANING_MARKS` 45 → 44 under 3:1 declared at the worst seat**, and the first number stays 79.
Both replaced marks and both replacements are well over 3:1, so an AREA fix could only move a count of
CONTRAST failures by changing **which cells carry a meaning** — and it did: `⡀` stopped being a
meaning mark at all, and what remains at that cell is the field leader, which is chrome.

**3. `test_win_clipboard_roundtrip` passed once and failed twice** across three runs of the full
suite in this increment, with no change to anything it touches. It is the environment-coupled test
this worktree's brief names; the observation is recorded because "reported, not counted" is easier to
trust with the flake demonstrated than asserted.

## §6 — the third obligation, and the deviation

**swiss `•` stays under the floor and is NAMED.** It measures **coverage 14.0 % · effective 9.13 ·
declared 17.30:1** — one point under a clause the round set at 15 %, on a mark the same round recorded
as legible in the same document (§2.2 `swiss_S2`: *«`•` obligatorio mide 0,060 en su peor asiento y
1,288 en el declarado; se ve»*), in a round whose §7 also finds `naught ◦` at **13.5 %** by eye.

**The two halves of round five disagree about this mark.** The brief for this increment names two
marks; this is a third.

Neither half was adjusted:

- the **floor was not lowered** to 14 % to make the corpus pass;
- the **mark was not changed** to make the floor pass.

Both would have been an increment grading its own homework in the same breath it wrote it — the
principle `rework-7c` is built on. It is recorded in `OBLIGATION_UNDER_THE_FLOOR` with its
measurement and its citation, the roster has teeth in both directions, and it is handed back to the
round in §9.

## §7 — files and frames

| file | change |
| --- | --- |
| `taskboard/language.py` | `Instrument.REQUIRED` `⠁` → `⣉`; `Prism.REQUIRED` `⡀` → `⣆`; both doctrine comments rewritten with the raster's before/after numbers and the inc35 / inc46 / inc59 citations |
| `tests/test_components.py` | inc82's law + `REPLACED_OBLIGATIONS` + `OBLIGATION_UNDER_THE_FLOOR` + teeth; inc81's obligations law replaced; `BELOW_THE_FLOOR` loses two rows (43 → 41 rows); `FLOOR_SEATS_FAILING` 43 → 41; `MEANING_MARKS` 45 → 44; `PRISM_EMBER_BEFORE` stepper score 1 → 0 and total 25 → 24; the instrument named-seat tooth reads the mark off the kit |
| `prototypes/components/legibility.py` | §F2's note rewritten for the post-fix corpus |
| `prototypes/out/legibility.txt` | F1 89 bound / 46 pass / 43 fail → **89 / 48 / 41**; F2 3 obligations under the floor → **1** |
| `prototypes/out/collision_census.txt` | TOTAL 28 → **27** |

**Frames changed — 4, and nothing else:**

```
prototypes/components/instrument_S2.txt   .svg      prototypes/components/png/instrument_S2.png  .json
prototypes/components/prism_S2.txt        .svg      prototypes/components/png/prism_S2.png       .json
prototypes/components/w80/instrument_S2.txt  .svg  .png  .json
prototypes/components/w80/prism_S2.txt       .svg  .png  .json
```

**Gallery 30–51: none changed byte-wise.** `capture_languages.py` was run plain and rewrote all 22
captures identically (`git status --porcelain` empty on `prototypes/gallery/`) — the board and gallery
frames do not draw an obligation mark.

## §8 — gates

```
pytest -q                1 failed, 1391 passed, 2 skipped, 4 warnings in 50.03s
                         (inc81 1389 -> 1391, +2 net: 3 laws added, 1 replaced;
                          the one red is tests/test_app.py::
                          test_win_clipboard_roundtrip, environment-coupled,
                          reported and not counted and not touched -- see §5.3)
verify_language.py       ALL PASSED                                    exit 0
render.py                66 .txt + 66 .svg / 330 pairs / 0 hand-drawn   exit 0
matrix.py                refusals [] for all eleven                     exit 0
collision_census.py      TOTAL 27 (was 28) · homoglyph rows 24          exit 0
raster.py                66 PNGs identical across two PROCESSES         exit 0
legibility.py            byte-identical across two PROCESSES            exit 0
second_width.py          0 rows cut · 330 pairs distinct                exit 0
capture_languages.py     22 grids identical across two PROCESSES · 22 captures
                         written · no two boards identical · gallery UNCHANGED
```

`export_to_skill.py` is the batch's closing gate and runs at the end of `rework-8`, not here.

## §9 — pending / next

- **Back to the round: swiss `•` at 14.0 %.** Either the coverage clause is 15 % and swiss needs a
  heavier obligation (a third kit, outside this brief), or the clause is wrong at the margin and §7 of
  round five is the evidence. **This increment will not decide it.**
- The `mut` / effective-contrast collision inc81 §5.2 named is still unruled: 29 of the 41 remaining
  rows are seats that are green under K6 and red under Q1.
- **inc83** — solari `band_head` at 24 rows (ruling F) and blueprint's four corners.
