# inc81 — the floor as law (Q1–Q3) and the glyphless run (K8/E6)

Batch `rework-8`, increment 1 of 4.

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

`legibility.py` §E ended with three questions and enforced nothing, and said why at length. The round
answered all three. Until this increment the answers lived in a `.md` and nothing in the repo could go
red on them.

Two things were unaskable rather than merely unasked:

1. **What a DECLARED seat is.** §D of the report judges every mark at its **worst** seat, which is
   almost always its decorative one — so `instrument ·` in a masthead decided instrument's score.
   Q3 says the opposite and nothing in the programme could tell the two apart.
2. **A run with no glyph.** `solari_S4` row 10 is a hundred blank cells on `#f5a300` — the band's
   opener and the brightest thing that kit draws — and the `.svg` has **no `<text>` element on that
   row at all**. Every instrument in eleven batches walks glyphs, so this was not a gap in a reader;
   it was structurally out of reach of every reader that has ever been written here.

## §2 — mechanism

**The declared seat is derived, not listed.** It is the `(cell, tone)` pair the kit's OWN contract
method paints when the family is exercised — `log_row`, `button(danger=True)`, `required`, `menu`,
`textfield(INVALID)` — intersected with `collision_census.role_map`, which stays the only thing that
decides *which family* a cell carries. **Five calls, not fifty-five rows.** A kit that moves the tone
of its severity rung moves its own seat and no table has to keep up.

**Q2 is arithmetic on the `.txt`.** The run is the uninterrupted horizontal stretch of one glyph
through the seat, read off the TEXT and not off the svg's run encoding — the exporter splits a run
wherever the colour changes, so a hundred cells of one glyph in two tiers is two svg runs and one
drawn stroke, and it is the stroke the eye integrates along.

**K8 has two readers and they are honestly different.** The **sidecar's colour-run** unit — the unit
the exporter paints and the unit round five counted — gives **18** runs of ≥ 8 blank cells in 3 kits.
The **rect sweep** now inside `painted_runs()`, which subtracts the cells a glyph lands in and returns
what is left, gives **60** in the same 3 kits. Both are true and they answer different questions; the
ruling names the first, and the second is what makes E6 an assertion instead of a complaint.

## §3 — law

| law | what it binds |
| --- | --- |
| `test_a_meaning_mark_clears_the_two_clause_floor_at_its_declared_seat` (×11) | Q1+Q2+Q3 over every meaning mark each kit declares; the failing set must equal `BELOW_THE_FLOOR` exactly, in both directions |
| `test_the_two_clause_floor_is_the_one_the_instrument_enforces` | the two clauses and the two run boundaries read off `legibility.py`'s SOURCE; the counts read off the report on disk |
| `test_the_eleven_obligations_are_judged_at_their_own_declared_seat` | one seat per kit, all eleven clear the contrast clause, exactly three miss coverage |
| `test_every_middle_band_run_is_named_and_the_table_is_not_vacuous` | Q2's 5–7 class: every middle run named, every named row reached |
| `test_a_glyphless_run_on_a_second_ground_is_ink` | the 18 runs, and Q2's structure clause (surface ≠ ground) |
| `test_the_exporter_paints_a_surface_no_text_run_can_name` | E6: `solari_S4` row 10 has no `<text>`; 60 vs 18 stated rather than reconciled |

`+18` law arms. **Nothing is a gate that the round has not ruled on:** `BELOW_THE_FLOOR` is a
RECORDED SET, the shape `SECOND_WIDTH_RED` and `DIM_CLASSIFIES` already have in this file.

## §4 — teeth

- `test_the_floor_law_bites_on_the_two_marks_the_round_sent_back` — removes instrument `⠁` and
  prism `⡀` from the recorded set one at a time (the row inc82 is about to remove for real); each
  arm must go red for that kit and stay green for the other ten. Plus the clause arm: all three
  failing obligations fail on **COV**, never on **EFF**.
- `test_the_glyphless_law_bites_when_the_plate_becomes_the_page` — repaints `solari_S4` row 10 at the
  kit's own ground **in the sidecar, not in the corpus**; the count drops 18 → 17, solari leaves the
  set, and the law goes red. The shipped PNGs are artefacts and an increment that rewrites one to
  make a law bite has proved nothing.
- `test_every_painted_run_clears_its_tiers_floor_on_its_own_ground` keeps its own teeth
  (`test_the_second_ground_law_bites_on_the_four_runs_round_four_measured`) and stays green: blank
  runs are skipped there by name, because `TIER_FLOOR` is WCAG 1.4.3 on words a reader reads.

## §5 — what was found by looking

**1. The round's prediction is wrong by one, and it is the round's own arithmetic.** §7 Q1 says *«los
once obligatorios pasan el contraste y dos fallan la cobertura (instrument 5,8 %, prism 5,3 %)»*.
Measured at the declared seat, **three** fail: `swiss •` is at **14.0 %**, one point under the 15 %
the round set — and the same round recorded that mark as visible (`swiss_S2`: *"`•` obligatorio …
se ve"*). It is reported and **not** adjusted. A floor moved to fit the corpus it was written for is
not a floor. **This is a live question for inc82**, whose brief names two marks and whose law says
*every* REQUIRED mark passes Q1.

**2. Two floors in one repo contradict, and nobody has ruled on which wins.** 29 of the 43 failing
rows miss the effective-contrast clause **only**, and they are overwhelmingly `mut` and `dim` seats:
the severity rung inc74 moved to `mut`, and the invalid field's walls, which nine kits draw in `dim`
as PAPER. K6 asks `mut` for **4.5:1 declared**; a thin glyph at 4.5:1 declared lands near **2:1
effective**. Q1 is strictly the harder floor for everything that is not solid. Every one of these
seats is green under the law that was written for it and red under the law written this week.

**3. The two clauses and the eye agree exactly where §7 said they would.** The 8 rows that miss BOTH
clauses are the marks round five's §7 listed as *"no se encuentra a ojo"*: the three `·` severity
rungs (swiss, nord, darkside), instrument `⠂`/`⠆`, prism `⣀`, naught `◦`. That is the strongest
evidence the floor is measuring the right thing.

**4. The glyphless run is bigger than one row.** 16 of the 18 are industrial's detail plate; the
finding round five wrote up (solari's opener) is one row and prism's confirm plate is another.

## §6 — files

| file | change |
| --- | --- |
| `prototypes/components/legibility.py` | `COVERAGE_FLOOR` / `EFFECTIVE_FLOOR` / `MEANING_MAX` / `STRUCTURE_MIN`, `A_SEAT_CALLS`, `declared_tones()`, `Sheets`, `run_class()`, `NAMED_RUNS`, `blank_runs()`; report sections **F** (the floor as law, F1–F4) and **G** (the glyphless run); §E retitled and its three open questions replaced by the ruling |
| `tests/test_components.py` | `painted_runs()` returns a sixth `blank` field and walks the RECTS; `runs_under_floor` skips blanks by name; the inc81 section: 6 laws + 2 teeth, `BELOW_THE_FLOOR` (43 rows), `GLYPHLESS_RUNS` (18 rows), `NAMED_RUNS_5_TO_7` (3 rows) |
| `prototypes/out/legibility.txt` | 591 → 790 lines |

**Frames changed: none.** No kit, no token, no screen was edited. `prototypes/components/*.txt`,
`*.svg`, `png/*`, `w80/*` and `prototypes/gallery/*` are byte-identical to `5d987a5`
(`git status --porcelain` empty on all four after every gate was re-run).

## §7 — deviation, named

**`collision_census.py` does not count the glyphless run and cannot.** The ruling says *"the census,
`painted_runs()` and `legibility.py` count it"*. The census reads **declarations** — `LEVELS`,
`DANGER_FORM`, `PART_GLYPHS`, `quantity_glyphs()` — and never opens a frame; its `TOTAL 28` is a count
of cells a kit declares, and a run that exists only in a picture has no declaration to be counted in.
Making it read frames would have changed what `TOTAL` means in six documents and two gates. **The
frame-side count lives in `legibility.py` §G and in the suite, and the census's 28 is unchanged and
means what it always meant.** Named here for the round to overrule if it disagrees.

## §8 — gates

```
pytest -q                1 failed, 1389 passed, 2 skipped, 4 warnings in 43.50s
                         (baseline 1371 -> 1389, +18; the one red is
                          tests/test_app.py::test_win_clipboard_roundtrip,
                          environment-coupled, red at the baseline, reported
                          and not counted and not touched)
verify_language.py       ALL PASSED                                    exit 0
render.py                66 .txt + 66 .svg / 330 pairs / 0 hand-drawn   exit 0
matrix.py                refusals [] for all eleven                     exit 0
collision_census.py      TOTAL 28 · TOTAL homoglyph rows 24             exit 0
raster.py                66 PNGs identical across two PROCESSES         exit 0
legibility.py            790 lines · byte-identical across two PROCESSES exit 0
second_width.py          0 rows cut · 330 pairs distinct                exit 0
git status --porcelain   only legibility.py, legibility.txt, test_components.py
```

`capture_languages.py` and `export_to_skill.py` **not run** — no board, kit, token or gallery
artefact was touched, and running them would have been the only way to move one.

## §9 — pending / next

- **inc82** must decide what to do about `swiss •`: the brief authorises fixing two marks and the law
  it asks for binds eleven. Options are (a) fix swiss too — a third kit, outside the brief;
  (b) name swiss as a measured exception on the law with the round's own "se ve" as its citation;
  (c) stop and ask. **The increment will take (b) and say so**, because (a) exceeds the brief and
  (c) stalls three further increments over one percentage point.
- The `mut` / effective-contrast collision (§5.2) is a ruling nobody has made. Not fixed here.
