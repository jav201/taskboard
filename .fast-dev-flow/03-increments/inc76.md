# Increment 76 — the raster: E2, asked for three times, built once

**Batch:** `rework-7b`, increment 1 of 3 · ruling **the fifth round runs against a raster at real cell
size, not against svg attributes** (orchestrator, 2026-09-07, on the operator's delegation).
**Files:** `prototypes/components/raster.py` (new), `prototypes/components/render.py`,
`tests/test_components.py` — **3 source files**, plus **66 PNG + 66 JSON** in
`prototypes/components/png/` and this packet.

**E2 has been open for three rounds and its whole content is that the `.svg` carries no font.**
Round four says it in one sentence (§8.2): *«el `.svg` no dice a que tamanio de celda ni con que
fuente se va a renderizar, asi que `⠂` a 1,74:1 a una altura desconocida es un numero y no una
fotografia»*. Seven objections are parked behind it — the four homoglyph pairs, `blueprint_S3`'s
three dashes, `† / ‡`, and the whole of §0a. This increment does not resolve any of them. **It builds
the instrument that can**: 66 PNGs at **9x19 px per cell**, Cascadia Mono 16 px, byte-identical
across two processes, with a sidecar that says what every cell was asked to be. inc77 measures.

Suite **1338 → 1363** (+25). `.txt` and `.svg` byte-identical, all 132 — the render path was
refactored and the refactor is provably neutral.

---

## 0. Rulings (orchestrator, 2026-09-07, on the operator's delegation)

> The fifth round runs against a **raster at real cell size**, not against svg attributes; the raster
> is an instrument the suite owns.

> The font is a **declared constant, never inferred**. Record which one and its path.

> **Law:** the raster's cell count equals the txt's rows × cols; a probe cell's pixel colour equals
> the declared fg/bg.

> Decide whether the PNGs are committed. **Decided: committed** (§6).

## 1. The face, and why it and not the other three

Declared in `raster.py` as `FONT_NAME` / `FONT_PATH`, checked against the machine on every run before
a pixel is drawn. **Cascadia Mono, `C:\WINDOWS\Fonts\CascadiaMono.ttf`, 16 px** — Windows Terminal's
own default face at its own default size (12 pt at 96 dpi).

The alternatives the brief named were rejected **by measurement over the corpus's own 206 distinct
cells**, not by taste:

| face | cells of the corpus it cannot draw |
|---|---|
| **Cascadia Mono** | **4** — `⊖ ⊚ ⊛ ⋅` |
| Cascadia Code | 4 — the same face **with ligatures**, and a ligature is one glyph across two cells, which is the one thing a cell-grid raster must not be handed |
| Consolas | 64 — no braille at all, half the block elements |
| Lucida Console | 87 — no braille, no rounded box drawing, no `▸` |

DejaVu Sans Mono, also named in the brief, **is not installed on this machine and was not installed
to make it fit**.

**The cell box is MEASURED, not declared**, and that is the difference between this artefact and the
`.svg`. At 16 px Cascadia's advance is **9.0 px** and its ascent/descent **15/4**, so the box is
**9 x 19 integer pixels** and the grid needs no rounding anywhere. That is luck, and `_declare()`
refuses to run if the advance ever comes back fractional: a fractional advance puts every column at a
different subpixel phase and a per-cell measurement stops meaning one thing. The `.svg`'s nominal
`8.4 x 17` is a number no font ever agreed to.

```
  face      Cascadia Mono 16px  C:\WINDOWS\Fonts\CascadiaMono.ttf
  bold      variable instance 'Bold' (not a synthetic stroke)
  cell      9x19 px  (advance 9.0, ascent 15, descent 4)
  underline baseline+2 px, 1 px thick
  corpus    206 distinct cells, 202 in the face
  fallback  Segoe UI Symbol for ⊖⊚⊛⋅ at {'⊖': 11, '⊚': 11, '⊛': 11, '⋅': 16} px, centred
```

**`bold` is the real bold face, not a stroke.** Cascadia ships as a variable font on Windows and
`Bold` is a named instance, so the seven kits whose `MATCH_STYLE` is `bold` get the face a terminal
would show. The brief allowed `stroke_width=1` as the fallback and it is **not taken**, because the
difference lands squarely in inc77: a stroked glyph gains ink at its outline and a bold face gains it
in the stem, and only one of those is what anybody will see.

**And the four cells Cascadia does not have are drawn by Segoe UI Symbol, declared by name.** A
terminal does not draw tofu there, it falls back — so drawing a missing-glyph box would have made
four of the corpus's cells look like a defect of the DESIGN when they are a defect of the FACE, and
inc77 measures ink area per glyph: four boxes would have scored as four confident wrong numbers.
Segoe is proportional (`⊖` is 13 px against a 9 px cell), so a fallback glyph is drawn at the largest
integer size whose advance fits the cell and centred — **11 px for the three circled operators, 16 px
for `⋅`** — and that size is written into all 66 sidecars, per glyph, so those four carry their own
asterisk instead of pretending to have been measured like the other 202.

The list is **exhaustive and asserted both ways**: the primary must lack exactly these four among the
corpus's cells and the fallback must have all four. A twelfth kit reaching for a fifth uncovered cell
fails loud here instead of being drawn as a box nobody looks at.

## 2. Coverage is asked of the RASTERISER, not of a cmap — and that avoided a dependency

`uncovered()` decides a glyph is missing when FreeType draws it **byte for byte the same as two
codepoints no face has** (one private-use, one non-character; they must agree with each other before
the answer is trusted). This was cross-checked against a `fontTools` cmap read while it was written —
**identical answers on all four faces, 4 / 4 / 64 / 87** — and `fontTools` is *not* a declared
dependency of this project, so the agreement is recorded and the dependency is not taken.

It is also the better question. A cmap says what a face CLAIMS; this says what it DRAWS, and the
picture will contain the second one.

**No new dependency in this increment.** Pillow is already `pyproject.toml`'s and is already imported
by `capture_languages.py`, `export_to_skill.py`, `taskboard/models.py` and `tests/test_app.py`.

## 3. The render path is not reimplemented — and the refactor that made that true is neutral

`render.one()` was split into **`render.frame()`** (compose, settle, `cell_grid`) and `one()`
(`frame()` plus its two `write_text` calls). `raster.py` calls `frame()`. So the PNG and the SVG come
out of the same `capture_languages.cell_grid()`, and a disagreement between them would be the
exporter disagreeing with itself — a finding this file can produce rather than a confound it
introduces.

`frame()` also takes a `size`, defaulting to the sheets' own `(100, 32)`. That argument exists for
inc78 and for the same reason: a second width rendered by a second renderer would be a second
question.

**The refactor moved nothing.** `render.py` re-run immediately after it:
`git status --porcelain prototypes/components/` returned **only `M render.py`** — 0 of 66 `.txt`,
0 of 66 `.svg`, 0 of 66 `.candidates.md`.

## 4. The laws

Four laws and one teeth, all reading the pictures **as bytes off disk** — `raster.py` reaches Textual
through `render.py`, and `test_components.py` reads artefacts by path on purpose (the same stance
`test_this_files_picture_metrics_are_the_exporters` already takes).

1. **`test_the_rasters_declarations_are_the_ones_this_file_measures_against`** — the face, the size,
   the fallback face and the four fallback cells read out of `raster.py`'s SOURCE; the 9x19 box and
   the 9.0 advance checked against all **66 sidecars**, because the box is measured and not written
   down. If the face moves, every number inc77 published was measured at a size that no longer
   exists, and this is where that gets said.

2. **`test_the_raster_has_one_cell_per_character_of_the_txt`** (11 arms × 6 sheets) — the `.txt` is a
   rectangle, the sidecar agrees with it, the cell grid agrees with the sidecar, and
   `PNG width × height == cols·9 × rows·19`, read out of the **IHDR by hand** so the law cannot be
   satisfied by whatever Pillow decides a truncated file is. A raster that drew 99 columns would
   still look like a taskboard and every number inc77 reports would be one column off from the middle
   of the sheet onwards.

3. **`test_a_probe_cells_pixels_are_the_declared_colours`** (11 arms) — and the brief's wording had
   to be sharpened, which is §9's first finding. Every pixel of every distinct cell is
   `ground + t·(ink − ground)` for some `t` in `[0, 1]`, within **one unit per channel**. Measured
   over the whole corpus while it was written: **7081 distinct cells, worst channel error 1, zero
   outside**. Not vacuous at either end, asserted: blank cells are exactly the ground (`t = 0`
   reached) and some pixel reaches full ink (`t = 1` reached) in every kit.

   The clause also carries **tile identity**: two cells sharing
   `(glyph, ink, ground, weight, decoration)` must be byte-identical pixel blocks. That is the clause
   that says **no glyph bleeds**, and it is not decorative — Cascadia's `█` measures 10x20 against a
   9x19 box, so a raster that drew the frame as text instead of as cells would hand a full block's
   right-hand neighbour a column of ink it never declared.

4. **`test_the_faces_full_block_leaves_a_seam_and_that_is_the_coverage_ceiling`** — §9.2.

5. **`test_the_raster_laws_bite_on_the_three_defects_they_were_written_for`** — teeth, on
   `instrument`'s six shipped PNGs copied to a tmp dir, with `RASTER` monkeypatched at the copy so
   **the real laws run against the mutant**. Three arms, each restored and re-passed afterwards so a
   red is the mutation and never the copying:

   - **(a) the grid slips** — one column cropped off `instrument_S1.png`. Law 2 red.
   - **(b) the ground is not the kit's** — **inc63's defect reproduced in the new artefact**: every
     pixel of `#0a0d12` repainted `#121212`, the colour all 66 sheets really did ship until inc63.
     The picture still looks like a taskboard and every cell is still internally consistent. Law 3
     red, on the blank clause and on the segment clause.
   - **(c) the sidecar claims an 8 px box over a 9 px picture** — laws 2 *and* 1 red, because between
     them they are the sentence *"the cell inc77 measured is the cell that was drawn"*.

## 5. Determinism, checked across two PROCESSES

`raster.py` re-renders the whole sweep in a **fresh interpreter** (`--raster-to <tmpdir>`) and diffs
every PNG byte for byte — the same bargain `capture_languages.check_reproducible` makes, and taken
for the reason that function's own docstring gives: two passes in one interpreter share whatever
state the confound lives in. A raster has two confounds a second in-process pass would sail straight
through — **a font object cached across calls, and a variation axis left set by a previous frame** —
and both are exactly the kind of thing that reproduces perfectly until somebody else runs the script.

```
  re-rendering in a fresh process to check determinism...
  66 PNGs identical across two PROCESSES
```

## 6. The artefacts, and the decision to commit them

```
prototypes/components/png/<lang>_S<n>.png    66 files   2.6 MB   17-71 KB each
prototypes/components/png/<lang>_S<n>.json   66 files   1.0 MB   11-30 KB each
```

**Committed**, per the brief's own guidance and for the reason it gives: a round has to be able to
cite them. 3.8 MB total, and the alternative — a round that has to regenerate the pictures before it
can argue about one — is how E2 stayed open for three rounds.

**The sidecar carries the grid**, run-encoded on `(fg, bg, bold, underline)`, so inc77 and any law
can read what a cell was DECLARED to be beside the pixels it actually got **without re-driving
Textual**. It also carries the font, the fallback and its per-glyph sizes, the measured box, and the
`.txt`'s own dimensions, which is what law 2 compares.

`.gitignore`: **unchanged**. `prototypes/components/` is not the scratch yard; `prototypes/out/*` is,
and nothing this increment ships lands there.

## 7. Gate tails, verbatim

```
$ python -X utf8 -m pytest -q
FAILED tests/test_app.py::test_win_clipboard_roundtrip - AssertionError: assert None == 'roundtrip 123 ABC taskboard'
1 failed, 1363 passed, 2 skipped, 4 warnings in 38.47s

$ python -X utf8 prototypes/verify_language.py
  [PASS] settle() keeps headroom under its bound (a gate near its limit is a gate about to rot)  worst 3 of 40 over 155 captures

ALL PASSED
                                                        (exit 0)

$ python -X utf8 prototypes/components/render.py
  66 .txt + 66 .svg -> ...\prototypes\components
  66 candidates files
  no two frames identical within a screen (330 pairs)
  0 hand-drawn elements declared (0 refused, 0 evoked)
                                                        (exit 0)

$ python -X utf8 prototypes/components/matrix.py
--- refusals, by language ---
naught     []   corgi      []   instrument []   swiss      []   industrial []   nord       []
darkside   []   prism      []   ledger     []   solari     []   blueprint  []
                                                        (exit 0)

$ python -X utf8 prototypes/collision_census.py
TOTAL                       28
TOTAL homoglyph rows            24
                                                        (exit 0)

$ python -X utf8 prototypes/components/raster.py
11 languages x 6 screens | viewport 100x32 cells
  face      Cascadia Mono 16px  C:\WINDOWS\Fonts\CascadiaMono.ttf
  bold      variable instance 'Bold' (not a synthetic stroke)
  cell      9x19 px  (advance 9.0, ascent 15, descent 4)
  underline baseline+2 px, 1 px thick
  corpus    206 distinct cells, 202 in the face
  fallback  Segoe UI Symbol for ⊖⊚⊛⋅ at {'⊖': 11, '⊚': 11, '⊛': 11, '⋅': 16} px, centred

  re-rendering in a fresh process to check determinism...
  66 PNGs identical across two PROCESSES

  66 .png + 66 .json -> ...\prototypes\components\png
  every raster is 100x32 cells of 9x19 px  (2522 KB total)
                                                        (exit 0)

$ git status --porcelain prototypes/components/*.txt prototypes/components/*.svg
                                                        (empty)
```

Suite **1338 → 1363** (+25: 11 + 11 arms of the two parametrised laws, +3 unparametrised).
Census **28** and homoglyph rows **24**, both unchanged: this increment moved no declaration.

## 8. Risks

1. **The raster is a picture of THIS box.** Cascadia Mono 16 px on Windows with FreeType's hinting.
   A different machine with a different FreeType will produce different antialiasing and inc77's
   numbers will move in the third decimal. The determinism check proves reproducibility **on this
   machine across processes**, which is what a law can hold; it does not prove portability, and no
   claim of portability is made.
2. **It is not a terminal.** Windows Terminal ships its **own** box-drawing and block glyphs and does
   not use the font's for those — so the corpus's box drawing is drawn here by Cascadia and there by
   the terminal, and the seam in §9.2 is one visible consequence. Said out loud rather than left to
   be discovered: **every number inc77 reports about a box-drawing or block cell is a number about
   the FONT's version of that cell.**
3. **`render.frame()` has a new signature and one new caller.** `one()` and `raster.sweep()` are the
   two; `size` defaults, so nothing that called `render.py` had to change, and the neutrality of that
   is measured in §3 rather than argued.
4. **The sidecar duplicates the grid the `.svg` already encodes.** Two artefacts now describe the
   same 3200 cells. They are written by one function from one grid in one call, so they cannot
   disagree without `cell_grid` disagreeing with itself — which is the thing law 3 would catch.

## 9. Found by looking, not fixed

1. **The brief's law could not be written as the brief wrote it, and the reason is antialiasing.**
   *"A probe cell's pixel colour equals the declared fg/bg"* is exactly true only at the two ENDS of
   the segment; the first draft asserted it of every `█` cell and went **RED in five kits at once**.
   The segment version is strictly stronger — it catches a wrong ground, a wrong ink, a swapped pair
   and a bleeding neighbour, where the two-colour version catches only the first two — and it is the
   version that is true. **A law that has to be weakened to pass is usually the wrong law; this one
   had to be generalised to pass, and got sharper.**

2. **Cascadia Mono's `█` does not fill its cell: the bottom pixel row comes out at 75 % coverage.**
   162 of the box's 171 pixels are full ink and 9 are three quarters, so a run of full blocks leaves
   a seam. This is why Windows Terminal ships its own box glyphs. It is now `FULL_BLOCK_COVERAGE` and
   asserted, because **inc77 reports coverage and 94.7 % is the ceiling this face gives that
   measure** — no cell in this corpus can score 100, and a coverage table that did not know that
   would read every glyph as 5 points worse than it is.

3. **Six of the eleven kits never draw a full block at all.** The first draft's ink probe asserted
   one per kit and was **vacuous in six**: naught, instrument, swiss, ledger, solari and blueprint
   draw zero. The counts are now a constant (`BLOCK_KITS`: industrial 84, nord 88, darkside 21,
   corgi 11, **prism 1**) so the fact cannot change quietly. **prism's single `█` in six sheets is
   worth a look by somebody**: a kit that spends a glyph exactly once is either precise or
   accidental, and nothing in this repo says which.

4. **The four cells Cascadia lacks are not incidental — two of them are in `HOMOGLYPH_FAMILIES`.**
   `⋅` opens the filled-dot family and `⊛` sits in the hollow one, so **two of the pairs inc77 has to
   measure are drawn by a different font at a different size than their partners**. That is not a
   defect of this increment, it is what a terminal does; it means those distances need their asterisk
   and inc77 must carry it.

5. **`◌`, `⊚` and `⊖` entered the corpus in `rework-7a` and nobody checked they could be drawn.**
   inc72 moved naught's radio to `◌ ◌ ⊚` on a legibility argument, three of the four uncovered cells
   are on that row, and **the check that they render at all did not exist until this increment**.
   The corpus has been choosing glyphs for eleven batches with no coverage gate anywhere.

## 10. Pending — not this increment

- **inc77** — ink area per glyph, homoglyph XOR distance, per-cell coverage × contrast, the floor to
  propose. This increment measures nothing on purpose.
- **inc78** — the second width.
- The seven objections E2 parks (four homoglyph pairs, `blueprint_S3`, `ledger_S2`, §0a) are
  **unresolved**; the instrument that can resolve them now exists and inc77 uses it.
- K6/K7's open questions, C5–C7, C9, C10, E3, G1, G2, L4, L6 — untouched.

## 11. Suggested next task

`inc77`, as briefed: `legibility.py` over the 66 PNGs, `prototypes/out/legibility.txt`, with the ten
smallest homoglyph distances and the coverage × contrast table for every meaning mark in every kit.

## Evidence checklist

- [x] **Tests/type checks/lint pass — WITH ONE RED, NAMED.** `1363 passed, 2 skipped, 1 failed`
      (baseline measured before any edit: `1338 passed, 2 skipped, 1 failed`,
      `prototypes/out/_b7b_base_suite.log`). The failure is
      `tests/test_app.py::test_win_clipboard_roundtrip`, environment-coupled (spec §10.6) —
      **reported, not counted, not touched.** `verify_language.py` ALL PASSED exit 0. `render.py`
      66 frames / 330 pairs / 0 hand-drawn. `matrix.py` refusals `[]` for all eleven.
      `collision_census.py` both self-checks green, TOTAL 28, homoglyph rows 24 — unchanged.
      `raster.py` 66 PNGs identical across two processes.
- [x] **No secrets in code or output** — one new script, one function split, four laws and one teeth.
      No network, **no new dependency** (§2), no path outside the worktree and `C:\WINDOWS\Fonts`,
      which is read-only here.
- [x] **No destructive commands run without approval** — none. The teeth copy into pytest's
      `tmp_path` and never write into `prototypes/components/png/`.
- [x] **File count within cap** — **3 source files**: `prototypes/components/raster.py` (new),
      `prototypes/components/render.py`, `tests/test_components.py`. The 132 artefacts in
      `prototypes/components/png/` are generated output, like the 66 `.svg`.
- [x] **Review packet attached** — this document.
