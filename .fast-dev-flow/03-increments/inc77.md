# Increment 77 — the measures on the raster: `• ∙` is 0.00 %

**Batch:** `rework-7b`, increment 2 of 3 · the fifth-round instrument, second half.
**Files:** `prototypes/components/legibility.py` (new), `tests/test_components.py`, `.gitignore` —
**3 source files**, plus `prototypes/out/legibility.txt` (591 lines) and this packet.

**The corpus contains exactly one pair of glyphs that are literally the same drawing, and four rounds
of reading could not have found it.** `•` U+2022 BULLET and `∙` U+2219 BULLET OPERATOR rasterise
**byte for byte identically** in Cascadia Mono at 16 px — the XOR area is `0.0`, not `0.004`.
`HOMOGLYPH_FAMILIES` puts them in one row on the strength of a reading; this is the first artefact in
the programme that can say the reading was not a guess. Every other pair of the corpus's 205 painted
glyphs is distinguishable, and the sweep that says so is over **20 706 pairs**, not over a list
anybody wrote.

Four measures, `prototypes/out/legibility.txt`, byte-identical across two processes. Suite
**1363 → 1367**. No frame moved, no token moved, no declaration moved: census **28 / 24** unchanged.

---

## 0. Ruling (orchestrator, 2026-09-07, on the operator's delegation)

> (a) per-glyph ink area; (b) homoglyph pair distance as XOR area over cell area, *"so 'same drawing'
> becomes a number"*, reporting the ten smallest and the pairs the rounds argued about; (c) per-cell
> effective contrast, reporting the contrast AND the coverage; (d) a legibility floor **to propose,
> not enforce**, tabulated for every meaning mark in every kit.

> **Laws:** the measure is deterministic; a mutant (swap two homoglyphs) moves the distance to zero;
> teeth.

## 1. The four measures, and what each is

Every number is an AREA or a RATIO over pixels a font actually drew, at inc76's declared 9x19 box.
The definitions matter more than the numbers and they are in the file:

- **`ink`** — the antialiasing-weighted share of the cell the drawing covers. A pixel half covered by
  the outline counts a half.
- **`touch`** — the share of the cell the drawing reaches at all. The gap between `ink` and `touch`
  is fringe, and a glyph that is mostly fringe is section C's whole subject.
- **`distance`** — `Σ|cov_a − cov_b| / cell`, symmetric, zero only when two glyphs rasterise
  identically, and **in the same unit as `ink`** — which is what makes *"these two differ by 3 % of a
  cell"* a sentence somebody can act on.
- **`coverage`** — the share of a painted cell whose pixels differ from the ground under it.
- **`effective`** — the contrast between the **mean colour of exactly those pixels** and that ground.
  Equal to the declared ratio for a solid glyph; far below it for a hairline, because most of a
  hairline's pixels are partway to the ground and the declared ratio describes a colour that appears
  in hardly any of them. **This is the number four rounds did not have.**

**Ink and distance are measured on canonical white-on-black tiles**, so the number is the DRAWING and
not the colour it happened to be painted in. **Coverage and effective are measured on the 66 shipped
PNGs**, so the ground is the one actually under the cell — ruling K6, and it arrives that way already
because `cell_grid` resolves `reverse` and the sidecar records what the cell was painted on.

**This file does not decide what a meaning mark is.** `collision_census.role_map()` does, through
`A_FAMILIES` — severity, danger, required, invalid, cursor, which is `LEVELS` / `DANGER_FORM` /
`REQUIRED` / `INVALID` / `CUR` exactly as the brief names them. A second list here would have been a
second census, and the first one already has teeth.

## 2. The ten smallest distances in the corpus

**Every pair of distinct glyphs the 66 sheets draw**, not only the pairs a family list generates —
20 706 pairs, which is the sweep no declared table can produce:

```
     pair   distance  in a family?      cells a  cells b
      • ∙     0.00%  yes                     2      134
      ⋅ ⠀     1.38%  NO                     64      421
      ⊚ ⊛     1.46%  NO                      1        2
      ⊖ ⊚     1.85%  NO                      6        1
      ─ ┈     2.00%  NO                   6266        2
      ⊖ ⊛     2.27%  NO                      6        2
      . :     2.39%  NO                     22      209
      . ⠀     2.39%  NO                     22      421
      · ⠀     2.39%  NO                   2496      421
      ⠀ ⠄     2.52%  NO                    421       25
```

**Nine of the ten are in no declared family, and five of them involve a glyph that draws nothing.**
Both facts are §7.

**`• ∙` at 0.00 %** is the headline and it is stated without overstating: **no kit draws both.** naught
spends `∙` 134 times (danger + severity) and swiss spends `•` twice (required), so it is two languages
holding one drawing for incompatible meanings — a fact about the corpus, not a collision inside any
kit. It is `IDENTICAL_DRAWINGS` in the suite so a twelfth kit reaching for the other one is caught.

**The ten pairs four rounds argued about, by name** — round four ruled every one of them
*«irresoluble sin raster»*:

```
      • ●    21.64%      ▪ ■    26.52%
      ○ ◦    22.81%      ╌ ┄     4.09%
      ◎ ◉    21.42%      ╌ ┈     4.46%
      † ‡     4.87%      ┄ ┈     2.79%
      ▬ ◦    17.09%      ⠇ ⠸    15.13%
```

**Seven of the ten are over 15 % of a cell and are not homoglyphs by any reading of these numbers.**
`• ●`, `○ ◦`, `◎ ◉`, `▪ ■`, `▬ ◦` and `⠇ ⠸` were argued about for four rounds and the raster says they
are a fifth to a quarter of a cell apart. **The three that survive the measurement are the dash
ladder (`┄ ┈` 2.79 %, `╌ ┄` 4.09 %, `╌ ┈` 4.46 %) and `† ‡` at 4.87 %** — which is exactly the set the
rounds treated as the tightest, so the instrument agrees with the reading where the reading was
careful and contradicts it where it was not.

**And the census's own 24 rows now carry distances** (§B4 of the report). The two tightest are
`darkside ▪ ▫` at **3.20 %** (required vs radio) and `ledger † ‡` at **4.87 %** (required vs invalid),
then `swiss · •` at 7.68 % (severity vs required). Everything else the census flags is over 11 %.

## 3. The worst ten meaning marks, coverage × effective contrast

```
rank kit          gl family                      cov     eff    decl  cov*eff
   1 darkside      · severity                  4.7%   1.13   1.39    0.053
   2 swiss         · severity                  4.7%   1.28   1.75    0.060
   3 nord          · severity                  4.7%   1.30   1.69    0.061
   4 instrument    ⠂ severity                  5.3%   1.24   1.74    0.065
   5 instrument    ⠁ required                  5.3%   1.24   1.74    0.065
   6 prism         ⡀ required                  4.7%   1.77   3.25    0.083
   7 prism         ⣀ severity                  9.9%   1.46   2.41    0.145
   8 naught        ◦ severity                 13.5%   1.14   1.35    0.154
   9 naught        ∙ danger+severity          14.0%   1.20   1.35    0.169
  10 instrument    ⠇ severity                 15.8%   1.24   1.74    0.196
```

The 79 meaning marks the corpus draws span **0.053 to 9.802**; the top of that range is corgi's `▀` at
`REQUIRED` (57.9 % coverage, 16.93 effective) and the bottom is a dot at 4.7 % of a cell.

**Six of the worst ten are `severity`, which is `LEVELS`, and five of those are the `info` rung.**
Round four's §0b said seven languages paint their `info` between 1.35:1 and 1.96:1 and called the
finding *«planteada»* because a ratio at an unknown size is not a legibility test. **It is now
resolved in the direction round four suspected and worse than it argued**: `darkside ·` is not a
1.39:1 problem, it is a 1.13:1 problem **over eight of a cell's 171 pixels**.

**And the effective ratio is below the declared one in every row of the table.** That is not a defect,
it is what antialiasing does — but it means every contrast number in four rounds of packets is an
upper bound on what the eye receives, and for a hairline the bound is loose: `prism ⡀` is declared at
**3.25** and delivers **1.77**.

## 4. The floor, proposed and not enforced

Section E of the report proposes **coverage × effective contrast** and refuses to assert it, and gives
three reasons that are not excuses:

1. **The product has no published precedent.** WCAG 1.4.3 is a ratio and 1.4.11 is a ratio; nothing in
   either multiplies by area. A floor invented inside an increment and asserted in the same increment
   is a number nobody argued with.
2. **Half of what it would fail is decoration and this file cannot tell which half.** That is round
   four's §8.4 verbatim, and inc74's `DIM_CLASSIFIES` is the shape the answer takes — a seat list with
   verdicts, written by somebody who decides.
3. **The face is not the terminal.** Windows Terminal draws its own box and block glyphs, so every row
   whose glyph is box drawing is a number about Cascadia's version of it.

**And the count that would be the ruling's subject is taken and labelled:** **45 of the 79 meaning
marks are under 3:1 on DECLARED contrast at the seat this report picks.** The report says in its own
text that this is **not a count of violations** — "worst seat" is the report's choice of where to
look, and a mark that is a severity rung on a log row and a decorative leader in a masthead is
legitimately two things. It is pinned in the suite (`MEANING_MARKS = (79, 45)`) because 45 of 79 is
the size of the question, and nobody had taken it.

Three questions a ruling would answer, one line each, in the report:

- is it coverage × effective, or coverage AND effective as two clauses with two floors?
- does it bind every meaning mark, or only the ones a `DIM_CLASSIFIES`-shaped list says classify?
- is a mark judged at its worst seat or at its declared one? **The answer changes which kits are in
  the top ten.**

## 5. The laws

Four, and **none of them imports `legibility.py`**. Its arithmetic is restated in the test file in
four lines and checked against the artefact it shipped, so the two can only agree by being right —
the same bargain `test_this_files_picture_metrics_are_the_exporters` already makes with the exporter.
The restatement draws through the **primary face only**, so the four cells Cascadia lacks are excluded
by name: a declared limitation of the restatement, not of the instrument.

1. **`test_a_homoglyph_distance_is_zero_only_when_the_drawings_are_one`** — three clauses. A glyph
   against itself is exactly zero; the measure is symmetric; and over all 20 706 pairs of distinct
   corpus glyphs **exactly one measures zero and it is `• ∙`**. The third clause is what makes the
   first two non-vacuous: a measure returning zero for everything passes them both.
2. **`test_the_pairs_four_rounds_argued_about_have_these_distances`** — the ten named pairs computed
   independently here AND parsed out of the shipped report, and the two must agree. That is both a
   pin on the numbers and a staleness check on the artefact.
3. **`test_the_legibility_report_on_disk_is_the_one_this_corpus_produces`** — the face, the box, the
   corpus counts, the zero-ink finding, the census's row count **restated by the census itself**, and
   section E's two numbers. A report that outlives the corpus it describes is the failure mode
   `render.py`'s sidecars already carry a comment about.
4. **`test_the_distance_law_bites_when_two_homoglyphs_are_made_one`** — **teeth, the mutant the brief
   named.** ledger's `†` is REQUIRED and `‡` is INVALID; the census calls it the tightest row in the
   corpus and it measures 4.87 %. Make the invalid mark the same drawing as the required one and the
   distance goes to exactly zero **and the corpus's zero-pair sweep returns TWO pairs where it
   returned one**. The sweep is by INDEX and not by value on purpose: a set of values would silently
   swallow the duplicate that is the whole demonstration. Both vacuity arms are present — the
   un-mutated pair is not zero, and the sweep is re-run on the real glyph list afterwards and comes
   back to one.

**Determinism** is checked the way `capture_languages` and `raster.py` check theirs — the whole report
re-measured in a **fresh interpreter** and diffed byte for byte. Not a second in-process pass, and the
confound is not hypothetical: `Ink` caches a coverage map per `(glyph, weight)`, so a bug returning
the previous glyph's map would be perfectly consistent inside one run and different in the next.

## 6. Gate tails, verbatim

```
$ python -X utf8 -m pytest -q
FAILED tests/test_app.py::test_win_clipboard_roundtrip - AssertionError: assert None == 'roundtrip 123 ABC taskboard'
1 failed, 1367 passed, 2 skipped, 4 warnings in 38.65s

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
  591 lines -> ...\prototypes\out\legibility.txt
    A. INK AREA -- how much of a 9x19 cell each drawing covers
    A1. 1 GLYPH(S) IN THIS CORPUS DRAW NOTHING AT ALL: ⠀
    B. HOMOGLYPH DISTANCE -- XOR area between two drawings, over the cell
    C. EFFECTIVE CONTRAST -- the ratio the pixels give, and the coverage
    D. THE MEANING MARKS -- coverage x effective contrast, every kit
    E. A FLOOR TO PROPOSE, NOT TO ENFORCE

  re-measuring in a fresh process...
  the report is byte-identical across two PROCESSES
                                                        (exit 0)

$ git status --porcelain prototypes/components/
                                                        (empty -- 0 of 198 artefacts moved)
```

Suite **1363 → 1367** (+4). Census **28 / 24** and the 66 PNGs unchanged: this increment measures and
changes nothing.

`.gitignore` gains **one line**, `!prototypes/out/legibility.txt`, on the precedent the file already
sets for `collision_census.txt` and for the reason written beside it: a round that has to regenerate a
measurement before it can cite it is how E2 stayed open for three rounds.

## 7. Found by looking, not fixed

1. **`⠀` U+2800 BRAILLE PATTERN BLANK draws nothing and is counted as ink 421 times.**
   `capture_languages.ink()` counts a cell as ink whenever it is not a space or a non-breaking space,
   and instrument spends this glyph **174** times and prism **247**. So the density figure `render.py`
   prints for those two kits — and every density argument four rounds made about them — counts 421
   cells of nothing. **This is a defect of the DENSITY MEASURE, not of the kits**, and it is the first
   artefact in the programme that could see it: no `.txt` and no `.svg` can distinguish a blank glyph
   from a drawn one. Reported, not fixed: `ink()` is shared with the board sweep and moving it is a
   change to a number in every packet.

2. **Nine of the corpus's ten tightest pairs are in no declared family, and five involve `⠀`.**
   `HOMOGLYPH_FAMILIES` is a list of circles, squares, dots and daggers; the raster's own sweep finds
   `⋅ ⠀` at 1.38 %, `. :` at 2.39 % and `─ ┈` at 2.00 %. **The families were derived from a reading of
   shapes, and shape families do not predict what a rasteriser makes similar.** Not a defect of the
   census — its question is "did you mean these two to be the same mark", which is about meaning —
   but the two instruments now visibly answer different questions and nobody has said which one a
   `rework` should follow.

3. **Three of the ten tightest pairs are the three fallback glyphs against each other** — `⊚ ⊛` 1.46 %,
   `⊖ ⊚` 1.85 %, `⊖ ⊛` 2.27 %. inc76 predicted exactly this and it is now measured: those three are
   drawn by **Segoe UI Symbol at 11 px, scaled to fit a 9 px cell**, and scaling three circled
   operators down to a third of their designed size collapses the difference between them. **naught
   put `⊚` into `LEVELS` in inc72 and `⊛` is its `REQUIRED`** — so the kit's severity rung and its
   obligation mark are 1.46 % of a cell apart **in the picture a terminal would draw**, and the census
   already flags them at `◦ ⊛` and `⊛ ◉`. This is the strongest single argument this increment makes
   for the raster's existence: the number could not be obtained any other way.

4. **`▪ ▫` is the corpus's tightest CENSUS row and it is darkside's**, at 3.20 % — tighter than
   `ledger † ‡` at 4.87 %, which round three called *«la mas apretada del corpus»* and round four
   repeated. **The ranking the rounds asserted is wrong by one place**, and it was wrong because a
   dagger and a double dagger look more alike in prose than a filled and a hollow small square do.

5. **Seven of the ten pairs four rounds argued about are between 15 % and 27 % of a cell apart.**
   `▪ ■` at 26.52 % has been described as a homoglyph problem in three documents. Measured, it is the
   fourth largest distance in the argued list. **The prose was arguing about a family membership, not
   about a resemblance**, and the two were never separated because nothing could separate them.

6. **The effective ratio is below the declared ratio in every one of the 79 meaning marks.** Every
   contrast number in four rounds of packets is an upper bound; for hairlines the bound is loose
   (`prism ⡀`: declared 3.25, effective 1.77). **No law in this repo measures the delivered ratio**,
   and K6/K7 are both written against the declared one.

## 8. Risks

1. **`effective` is a definition this programme has not agreed on.** "The mean colour of the pixels
   the glyph paints" is one reasonable reading of "what the eye receives" and there are others —
   coverage-weighted mean, the darkest decile, a spatial-frequency model. The definition is in the
   file and in the report; **no ruling has endorsed it** and section E does not assert it.
2. **Every number is a number about Cascadia Mono at 16 px on this machine.** inc76's §8.1 and §8.2
   apply unchanged and are the reason section E's third refusal exists.
3. **The report is 591 lines and its section A lists all 205 glyphs.** It is meant to be read by a
   round, not skimmed; the ten-row summaries are the parts with pins in the suite.
4. **The suite gained a 20 706-pair sweep.** It runs in under a second because `_cov` and `_xor` are
   memoised; without the memo it is minutes. If somebody removes the `lru_cache` the suite gets slow
   rather than wrong, which is the right failure.

## 9. Pending — not this increment

- **inc78** — the second width.
- **The floor is proposed and not ruled.** Three questions are written for the orchestrator in §4.
- **`ink()` counts a blank glyph as ink** (§7.1). Not fixed: shared with the board sweep.
- **`⊚` and `⊛` are 1.46 % apart in naught** (§7.3). A language-level question, not an instrument one.
- E2 is **closed as an instrument**; the seven objections parked behind it now have numbers and none
  of them has a verdict — that is the round's job, not this batch's.

## 10. Suggested next task

`inc78`, as briefed: find whether `screens.py`/`render.py` can render at 80×24, and if so render the
66 there and report which frames break a law and which commitments fail.

## Evidence checklist

- [x] **Tests/type checks/lint pass — WITH ONE RED, NAMED.** `1367 passed, 2 skipped, 1 failed`
      (inc76 left `1363 passed`). The failure is `tests/test_app.py::test_win_clipboard_roundtrip`,
      environment-coupled (spec §10.6) — **reported, not counted, not touched.**
      `verify_language.py` ALL PASSED exit 0. `render.py` 66 / 330 / 0. `matrix.py` refusals `[]` for
      all eleven. `collision_census.py` TOTAL 28, homoglyph rows 24 — unchanged. `raster.py` 66 PNGs
      identical across two processes. `legibility.py` report byte-identical across two processes.
- [x] **No secrets in code or output** — one measurement script, four laws, one `.gitignore` line. No
      network, **no new dependency**, no path outside the worktree.
- [x] **No destructive commands run without approval** — none. Nothing outside
      `prototypes/out/legibility.txt` was written.
- [x] **File count within cap** — **3 source files**: `prototypes/components/legibility.py` (new),
      `tests/test_components.py`, `.gitignore`. `prototypes/out/legibility.txt` is generated output,
      committed on the census's precedent.
- [x] **Review packet attached** — this document.
