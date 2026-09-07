# Increment 78 — a second width: 79 law-arms at 80×24, and two of them are red

**Batch:** `rework-7b`, increment 3 of 3 · round four's §8.5 and §9c.2, *«Un solo ancho»*.
**Files:** `prototypes/components/second_width.py` (new), `tests/test_components.py` — **2 source
files**, plus **264 artefacts** in `prototypes/components/w80/` (66 × txt, svg, png, json) and this
packet.

**The sheets resize.** All 66 build and render at 80×24 with **zero clipped rows** — `Sheet.body()`
has reported every row it had to cut since the first sweep and it reports none. Round four costed this
at *"one line of `render.py`"* and it was one line: `size`, the argument inc76 added to
`render.frame()` for exactly this.

**And the corpus is not as width-independent as its commitments say.** Of **79 law-arms** asked of the
80×24 frames — 53 inside the suite, 26 by hand in a throwaway process — **77 are green and 2 are red,
both solari**, and only one of the two is the frame's fault:

1. **Ruling F fails.** *A confirm never covers the gate it names* — and at 24 rows solari's band
   covers a gate it does **not** name, by two rows, because the placement rule satisfies the ruling by
   moving the band **below** the named gate and at 24 rows there is no below.
2. **A law is width-bound and the frame is fine.** `test_a_confirm_opens_and_closes_on_marks_of_its_own`
   asserts solari's plate is at full measure with `any(w > 800)`. 800 is 100 cells × 8.4 units. At 80
   columns the plate is 672 units wide and **is** at full measure. **The law only means what it says
   at one width**, and no amount of rendering at 100 could have shown it.

Suite **1367 → 1370**. The 100×32 corpus is byte-identical: 0 of 198 artefacts moved.

---

## 0. Ruling (orchestrator, 2026-09-07, on the operator's delegation)

> Find whether `screens.py`/`render.py` can render at 80×24; if yes, render the 66 there and report
> **which frames break a law at that width** (closure, contiguity, band, walls, opener) and **which
> commitments fail**; if the sheets cannot resize, say exactly what blocks it and stop. **Do not fix
> languages here; the round judges.**

Nothing is fixed. Two reds are recorded and left standing.

## 1. Can the sheets resize? Yes, and the reason is that `W` and `H` are read at call time

`screens.W, screens.H` are module globals and **every sheet builder reads them when it is called**, so
a second width costs an assignment and not a rewrite. `Sheet.body()` already clips to them and already
reports what it clipped (*"a frame that only fits because it was trimmed is a finding about the
language's width appetite"*). `second_width.py` sets the two globals once, in a process that renders
one width and exits — so there is no state to restore and nothing that can half-restore it.

```
$ python -X utf8 prototypes/components/second_width.py
11 languages x 6 screens | viewport 80x24 cells

  rows the sheets had to CUT: 0 in 0 frames
  no two frames identical within a screen (330 pairs)

  66 .txt + .svg + .png + .json -> ...\prototypes\components\w80
  ink 13.9% .. 58.4%
```

**Nothing is re-implemented.** `render.frame()` for the composited grid, `capture_languages.
svg_from_grid()` for the picture, `raster.png_of()` for the raster — the same three functions the
100×32 corpus is made of. inc54's *«nada en este repo renderiza `S4` por debajo de 100»* was true and
is no longer.

**What changes in the fixture at 24 rows, said before any verdict:** the board loses a gate. At 100×32
solari's S1 shows four (`BACKLOG DOING BLOCKED DONE`); at 80×24 it shows three, `DONE` falling off the
bottom. That is the sheets doing what they are supposed to do with less room, and it is named here
because it is the mechanical cause of §2.

## 2. Ruling F fails for solari at 80×24, and it is a HEIGHT finding wearing a width's clothes

The law has two arms. The first asks the **shipped frame** whether the gate the confirm names survived;
it is green at both sizes, because the confirm names `BACKLOG` and `BACKLOG` is rows 3–8 at both. The
second — the arm inc55 added, *"so a placement that happened to miss BACKLOG while eating whichever
gate it was pointed at goes red"* — asks the **mechanism** the same question **once per gate**. That
arm is the one that goes red, and inc55's sentence is the exact defect it caught:

```
                     band rows        rows of its OWN block the band ate
100x32  about=BACKLOG  10..15          none
        about=DOING    24..28          none          <- moved BELOW the block (9..18)
        about=BLOCKED  10..15          none
        about=DONE     10..15          none

 80x24  about=BACKLOG  10..15          none
        about=DOING    17..22          17, 18        <- there is no below
        about=BLOCKED  10..15          none
```

At 32 rows a confirm about `DOING` puts its six-row band at 24–28, clear beneath `DOING`'s block
(9–18). At 24 rows the page ends at 23, the band lands at 17–22, and **rows 17 and 18 are `DOING`'s own
departures**. `REWRITE THE ONBOARDING` and its seam are covered by a question about `DOING`.

**The placement rule was written, and tested, on a page that always had somewhere to go.** Ruling F was
issued 2026-09-06, inc55 gave it a mechanism arm, inc50 named three ways out and took one — and every
one of those decisions was made at 32 rows. This is the strongest single argument in the batch for
rendering at a second size at all: the corpus's only geometric ruling has a precondition nobody stated.

**Not fixed** — the brief says the round judges. The shape of a fix is visible from the table
(shrink the band, or refuse to place it when neither above nor below is clear) and it is a solari
design decision, not an increment's.

## 3. What was asked, and what it answered

**53 arms in the suite**, thirteen laws — four asked of all eleven kits, nine asked once — re-run with
`FRAMES` and `RASTER` pointed at `w80/`. **No law is restated for the new width**, which is the whole
method: a second set of 80-column laws would be a second opinion about what the corpus must do, and
the objection is precisely that the commitments say *"at any width"* and were only ever asked at one.

The recorded set has a **control arm that runs first**: the same 53 arms against the 100×32 corpus,
where all 53 are green. Without it the two reds could be laws that were broken all along with the
width as a bystander.

```
contiguity   test_a_modal_changes_one_contiguous_band_of_the_page          11 arms  GREEN
opener/edge  test_a_confirm_opens_and_closes_on_marks_of_its_own           11 arms  10 GREEN, solari RED
raster       test_the_raster_has_one_cell_per_character_of_the_txt         11 arms  GREEN
raster       test_a_probe_cells_pixels_are_the_declared_colours            11 arms  GREEN
             test_every_language_has_a_frame_for_every_screen               1        GREEN
             test_no_two_languages_render_a_screen_identically              1        GREEN
closure      test_every_confirm_says_where_it_ends                          1        GREEN
             test_naughts_two_option_controls_do_not_rest_on_one_drawing    1        GREEN
walls        test_swisss_rejected_field_has_a_wall_paper_and_a_closer       1        GREEN
band         test_solaris_announcement_takes_the_head_of_the_schedule...    1        GREEN
band         test_solaris_band_is_its_content_and_stands_at_a_gates_head    1        GREEN
band         test_no_gate_header_stands_inside_solaris_band                 1        GREEN
band         test_a_solari_confirm_never_covers_the_gate_it_names           1        RED
```

**26 more arms by hand**, in a throwaway process, because they BUILD a sheet as well as reading one and
that means mutating `screens.W`/`H` — a global a test sets is a global the next test inherits, so they
are not run inside the suite. **All 26 green** (`prototypes/out/_b7b_i78_excluded.txt`):

```
GREEN  test_blueprints_first_fixation_is_painted_on_the_form
GREEN  test_blueprints_knockout_is_where_operator_ruling_10_put_it
GREEN  test_the_destructive_default_answer_is_a_focused_danger_button      11 arms
GREEN  test_the_svg_paints_exactly_the_style_runs_the_kit_declared         11 arms
GREEN  test_solari_never_files_a_departure_under_the_wrong_gate             2 arms
```

**And one law is excluded because it is not a width question at all:**
`test_the_faces_full_block_leaves_a_seam_and_that_is_the_coverage_ceiling` pins how many times each kit
draws `█` in the 100×32 corpus. A smaller viewport draws fewer cells — industrial 84 → 55, nord
88 → 56, darkside 21 → 12, corgi 11 and prism 1 unchanged — so asking it at 80×24 asks the wrong
thing. Recorded rather than quietly dropped.

## 4. Which commitments fail

**One: ruling F, for solari, at 24 rows.** Everything else the frames can be asked survives.

That sentence needs its own caveat, and it is the finding under the finding. **The commitments that say
*"at any width"* are almost all enforced at the DECLARATION level in this repo, not at the frame
level** — `MODAL_BORDER_REFUSED`, `PANE_SPLIT_REFUSED`, `STATES_TOLD_APART_BY_SIZE`, `TIER_FLOOR`,
`DIM_CLASSIFIES`, the whole role and contrast tier. A declaration cannot notice a width. So *"77 of 79
green"* is a weaker statement than it reads: **most of what "at any width" promises was never asked of
a picture at any width, and this increment did not change that** — it asked the thirteen laws that
read a picture, and thirteen is what there is.

The one commitment already written width-parametrically, `test_the_closure_law_holds_on_every_pane_
seat_at_every_width`, asks `pane_split` at widths 1, 2, 3, 4, 7 and 12 and does not read a frame at
all. It is green and it was green before this increment; a second rendered width neither strengthens
nor weakens it, which is the correct behaviour for a law written that way and an argument for writing
more of them like it.

## 5. The other red: a law with a magic number

`test_a_confirm_opens_and_closes_on_marks_of_its_own` exempts solari by name — solari's band is a
`reverse` plate rather than a pair of marks — and then **checks the refusal instead of taking it on its
word**: *"the plate has to be in the picture, at full measure, or this is a kit with no edge and a
sentence about one."* It spells "at full measure" as

```python
assert any(w > 800 for w, _f in runs), (lang, runs[:3])
```

800 is 100 cells × 8.4 units, minus room. At 80 columns the picture is 672 units wide, the plate is
`(672.0, '#f5a300')` — **the full measure of the page it is on** — and the law says no.

**The frame is correct and the law is wrong**, and the fix is one line (`w > 0.95 * page width`,
read off the canvas rect). It is **not taken here**: this increment renders and judges, and changing a
law to make a red go away in the same increment that found it is how a gate stops meaning anything.
It goes on the list for the round with a diff already written in this sentence.

## 6. Gate tails, verbatim

```
$ python -X utf8 -m pytest -q
FAILED tests/test_app.py::test_win_clipboard_roundtrip - AssertionError: assert None == 'roundtrip 123 ABC taskboard'
1 failed, 1370 passed, 2 skipped, 4 warnings in 43.03s

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
naught     []   corgi      []   instrument []   swiss      []   industrial []   nord       []
darkside   []   prism      []   ledger     []   solari     []   blueprint  []
                                                        (exit 0)

$ python -X utf8 prototypes/collision_census.py
TOTAL                       28
TOTAL homoglyph rows            24
                                                        (exit 0)

$ python -X utf8 prototypes/components/raster.py
  66 PNGs identical across two PROCESSES
  every raster is 100x32 cells of 9x19 px  (2522 KB total)
                                                        (exit 0)

$ python -X utf8 prototypes/components/legibility.py
  re-measuring in a fresh process...
  the report is byte-identical across two PROCESSES
                                                        (exit 0)

$ python -X utf8 prototypes/components/second_width.py
  rows the sheets had to CUT: 0 in 0 frames
  no two frames identical within a screen (330 pairs)
  66 .txt + .svg + .png + .json -> ...\prototypes\components\w80
  ink 13.9% .. 58.4%
                                                        (exit 0)

$ git status --porcelain prototypes/components/*.txt prototypes/components/*.svg prototypes/components/png
                                                        (empty)
```

Suite **1367 → 1370** (+3). Census **28 / 24**, the 66 PNGs, the 66 `.txt` and the 66 `.svg` all
unchanged.

`prototypes/components/w80/` is **264 files, 4.1 MB**, committed on inc76's precedent and for its
reason: a round that has to regenerate the pictures before it can argue about one is how a question
stays open for three rounds.

## 7. Risks

1. **80×24 is one more width, not "any width".** Two data points make a line only if somebody draws
   one. inc78 does not claim the corpus is width-independent; it claims two arms go red at one other
   width and names them.
2. **The recorded red set is a snapshot with a control arm, not a gate.** If somebody fixes solari,
   `test_the_frame_laws_at_eighty_by_twenty_four_are_the_ones_recorded` goes RED — deliberately. The
   set changing in either direction is a thing a person should look at.
3. **`screens.W`/`H` are process-global.** `second_width.py` sets them and exits; the suite never sets
   them, which is why 26 arms were run by hand. A future increment that wants those 26 inside the
   suite needs `W`/`H` to become parameters, and that is a `screens.py` refactor nobody has asked for.
4. **The 26 hand-run arms are evidence from a throwaway process**, reproduced by the script quoted in
   §3 and kept at `prototypes/out/_b7b_i78_excluded.txt`. They are not in the suite and this packet
   does not count them as if they were.

## 8. Found by looking, not fixed

1. **`FRAMES` is doing two jobs and one of them is not a width.**
   `test_solari_never_files_a_departure_under_the_wrong_gate` loads `FRAMES / "fixture.py"` — a SOURCE
   file — through the same constant that says where the pictures are. Point `FRAMES` at a second
   corpus and the law asks for a `fixture.py` that has no business being there. It is excluded from the
   suite's list for that reason and run by hand instead (**green, both arms**).

2. **The band's placement is the only rule in this corpus that depends on the page having spare
   rows**, and nothing says so. `overlay`'s contract is about a rectangle; ruling F is about a gate;
   the interaction between them is a height budget that exists only in the arithmetic.

3. **A magic number outlived the width it was measured at** (§5), inside a law whose own docstring
   says the refusal must be *checked, not taken on its word*. **The check was right and its
   constant was a width.**

4. **The fixture shows three gates at 24 rows and four at 32**, so the 80×24 corpus is not the same
   board photographed smaller — it is a shorter board. Every comparison in this packet is between two
   pages that differ in content as well as in size, and that is stated rather than smoothed over.

5. **77 of 79 green reads better than it is** (§4). Most of *"at any width"* lives in declarations that
   no width can reach.

## 9. Pending — not this increment

- **solari's ruling-F failure at 24 rows** — a design decision, for the round.
- **the `w > 800` clause** — a one-line fix, deliberately not taken in the increment that found it.
- **A third width** (120, or 60). Two points, one line.
- The whole of `rework-7b` is instrument work: **E2 is closed as an instrument and no objection it was
  blocking has a verdict.** That is the round's job.

## 10. Suggested next task

The fifth round, run against `prototypes/components/png/` and `prototypes/components/w80/` with
`prototypes/out/legibility.txt` in hand — which is what this batch was built to make possible. Its
first three questions are written: the floor (inc77 §4), solari's ruling F at 24 rows (§2), and the
`w > 800` clause (§5).

## Evidence checklist

- [x] **Tests/type checks/lint pass — WITH ONE RED, NAMED.** `1370 passed, 2 skipped, 1 failed`
      (inc77 left `1367 passed`). The failure is `tests/test_app.py::test_win_clipboard_roundtrip`,
      environment-coupled (spec §10.6) — **reported, not counted, not touched.** `verify_language.py`
      ALL PASSED exit 0. `render.py` 66 / 330 / 0. `matrix.py` refusals `[]` for all eleven.
      `collision_census.py` TOTAL 28, homoglyph rows 24 — unchanged. `raster.py` and `legibility.py`
      both byte-identical across two processes.
- [x] **No secrets in code or output** — one render script and three laws. No network, no new
      dependency, no path outside the worktree.
- [x] **No destructive commands run without approval** — none. `second_width.py` writes only into
      `prototypes/components/w80/`, a new directory.
- [x] **File count within cap** — **2 source files**: `prototypes/components/second_width.py` (new)
      and `tests/test_components.py`. The 264 files in `w80/` are generated output.
- [x] **Review packet attached** — this document.
