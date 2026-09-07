# inc84 — the key bar at 24 rows (C12), the greyscale capture (L12), and a cut that says so (C13)

Batch `rework-8`, increment 4 of 4.

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

**C12.** The S6 key bar — `enter run · esc close · ^p prev · ^n next`, the row that says how the
palette is closed — was appended with `Sheet.row()`, so it landed wherever the builder's content
happened to end. At 32 rows it sat between row 17 (ledger, solari, darkside) and row 26 (nord); at 24
rows `body()` clipped it off the bottom in **instrument, nord, blueprint and prism**. The seven kits
that kept it kept it by having shorter content. **That is luck, not composition.**

**C13.** `screens.s1` sliced the detail panel's title with a bare Python expression —
`F.TASKS[F.SELECTED][0][:right - 14]`. At 100 columns `right` is 37 and the title fits with room to
spare; at 80 columns `right` is 17 and `Fix login redirect` becomes `Fix`, with nothing to say a cut
happened. All eleven. And `clip()` — whose docstring calls clipping *"the honest failure"* — was
honest to the **writer** (`body()` reports it on stdout) and silent to the **reader**, which is how
swiss shipped `phase: do` and `priority: hi` as if those were the values.

**L12.** Round five §0d: *"el canal es el matiz solo … en escala de grises no queda nada"*, and
*"ninguna de estas cinco rondas puede resolver [esto], porque no hay lector daltonico en este equipo
ni captura en escala de grises en este repo."* The second half of that sentence was a missing
artefact, not a missing argument.

## §2 — mechanism

### C12 — a key bar is a footer, so dock it

`Sheet` gains `foot`, and `s6` calls `sh.dock(...)` instead of `sh.row(...)`. `build()` reserves the
docked rows at the bottom of the frame **at whatever height the frame has**, in the order the
commitments demand: **the key bar first and the title block last**, so blueprint's three-row stamp
keeps the bottom corner its own commitment names (`LANGUAGES.md` §11) and the key bar sits on the row
above it.

### C13 — `Kit.elide`, and a `clip` that can be told

`Kit.elide(text, w)` returns the text when it fits and `text[:w-1] + DISCLOSE` when it does not.
**The mark is the language's own disclosure and not a new table** — the same decision `textarea`'s
wrap mark took in inc30 and for the same reason: `DISCLOSE` already means *there is more beyond* in
all eleven, it is **one cell in all eleven**, and `…` is in none of these alphabets while `...` costs
three cells to say what one already says. The mark takes a cell **of the budget**, so an elided string
is never wider than the seat it is protecting.

`screens.clip(s, n, k=None)` takes an optional kit and, when it has one and something was cut, ends
the row on that kit's `DISCLOSE` in `dim`. The detail panel passes it; nothing else does.

### L12 — a greyscale pass that is a measurement and not a filter

`raster.py` writes `png/<name>.grey.png` beside every frame. **It is not `Image.convert("L")`**: PIL's
`L` applies ITU-R 601-2 coefficients to the **encoded** values, which is a display convenience. What a
legibility question needs is WCAG's own relative luminance — linearise sRGB, weight by Rec.709,
re-encode — because then **the contrast ratio between two greys in the image equals the ratio the
colour pair had**, and "does the match survive greyscale" is answered by the same arithmetic as every
other number in this programme. The weights are declared (`GREY_WEIGHTS`), E4's rule applied one
artefact over, and checked against the shipped PNGs by the suite.

**And the measurement points at DISTINCTNESS, not legibility.** A match run is legible against its
**ground** and distinct against the **body** it stands in — the six `re` of `nord_S6` are teal among
slate words. So section H measures the match ink against `mut` and against `ink`, in grey.

## §3 — law

| law | what it binds |
| --- | --- |
| `test_the_key_bar_is_the_last_row_of_the_palette_at_any_height` (×11) | C12, at **both** widths: the row is present, and it is the last row below everything except the chrome a language docks under it |
| `test_elide_marks_the_cut_with_the_languages_own_disclosure` (×11) | text that fits comes back byte for byte; the result is never wider than the seat; a cut always ends in `DISCLOSE`; `DISCLOSE` is one cell |
| `test_no_detail_title_is_cut_without_saying_so_at_either_width` (×11) | C13 on the shipped frames — found by the TITLE, not by the caption, which is spelled eleven ways — plus swiss's values |
| `test_the_greyscale_pass_is_the_declared_transform` (×11) | same size as the colour frame; **every** pixel a true grey; every distinct colour equal to the declared transform |
| `test_the_rasters_greyscale_declaration_is_the_one_measured_here` | the weights and both sRGB break points read off `raster.py`'s SOURCE; 66 grey PNGs exist |
| `test_the_match_that_rides_hue_alone_keeps_a_thin_step_in_grey` | L12, measured, with the kits that have a second channel asserted to have one |

## §4 — teeth

- `test_the_key_bar_is_docked_and_not_stacked` — `Sheet.dock` put back to `Sheet.row`, which **is**
  the pre-inc84 composition, and the sheet rebuilt at the default size, so the arm needs no module
  global to be mutated and inherits none. Under the mutant the bar stops being the last row in **all
  eleven**. The un-mutated build is asserted first, so the mutant cannot pass by accident.
- `test_the_elide_law_bites_on_the_bare_slice_it_replaced` — `Kit.elide` put back to `text[:w]`, the
  expression `screens.py` used to spell inline; all eleven go red.

## §5 — what was found by looking

**1. The greyscale capture does NOT say what L12 said, and that is the finding.** Round five wrote
*"en escala de grises no queda nada"* about three kits and could not check it. Checked:

```
kit         channel   v ground   v mut   v ink | grey mut  grey ink  verdict
instrument  hue          10.45    2.32    1.58 |     2.34      1.57  holds
swiss       hue           4.52    1.52    3.83 |     1.52      3.85  holds
nord        hue           5.99    1.33    1.81 |     1.34      1.80  holds
prism       hue          10.17    1.58    1.58 |     1.59      1.57  holds
```

**None of them goes to 1.00:1.** What survives is a **luminance step the accent carries along with its
hue**, and it is thin: nord 1.34, swiss 1.52, prism 1.59, instrument 2.34 against the body — **all
four under 3:1**. So the objection is **right in shape and wrong in degree**: the channel is thin, not
absent. L12 is **amended by this table and not closed by it** — a step nobody chose is not a channel a
language may claim, and no ruling has said which of the two readings the corpus is held to.

**2. There are FOUR hue-only kits, not three.** Round five's L12 names instrument, nord and prism.
`swiss` has the same branch — its `accent` is a saturated red against an achromatic `mut`, which is
exactly the case §0d describes — and round five discussed it under `swiss_S6` (*"la peor cifra del
corpus"*, 1.52:1) without adding it to L12. The derivation is mechanical and the fourth kit falls out
of it.

**3. C13 propagates further than round five measured.** The detail title is drawn on `S1` **and on the
board behind `S4`**, so the silent cut was in **21 frames at 80 columns**, not 11: eleven `S1` and ten
`S4` (corgi's confirm blacks the page, so it has no board behind it to cut).

**4. The key bar's stacked position was wrong in all eleven, not four.** Round five counted the four
that LOSE it at 24 rows. Under the mutant arm, `dock` reverted to `row` puts the bar off the last row
in **every one of the eleven** at 32 rows too — it was simply not fatal there. The four were the ones
where the same defect became visible.

## §6 — files and frames

| file | change |
| --- | --- |
| `taskboard/language.py` | `Kit.elide` |
| `prototypes/components/screens.py` | `Sheet.foot` + `Sheet.dock`, `build()` docks foot-then-titleblock, `s6` docks the key bar, `clip(s, n, k=None)` marks, `s1` elides the title and marks the definition rows |
| `prototypes/components/raster.py` | `GREY_WEIGHTS`, `_linear`, `_encode`, `grey_of`; the sweep writes and reproducibility-checks 66 grey PNGs |
| `prototypes/components/legibility.py` | `match_branch`, `_grey`, `GREY_DISTINCT`; report section **H** |
| `tests/test_components.py` | six laws and two teeth (above), `KEY_BAR_KEYS`, `MATCH_IN_GREY`, `GREY_WEIGHTS` |
| `prototypes/out/legibility.txt` | 790 → 870 lines (section H) |

**Frames changed:**

```
100x32   11 S6                       (txt, svg, png, json)   -- the docked key bar
 80x24   11 S1 · 10 S4 · 9 S6        (txt, svg, png, json)   -- the marked cut, the docked bar
new      66 png/<name>.grey.png                              -- the greyscale capture
```

`industrial_S6` and `darkside_S6` did not move at 80 columns: their key bar was already the last row.
`corgi_S4` did not move: its confirm keeps no board behind it.
**Gallery 30–51: none changed byte-wise** (`capture_languages.py` run plain; `git status --porcelain`
empty on `prototypes/gallery/`).

> ### CORRECTION — 2026-09-07, inc87 (orchestrator's ruling, `rework-9`)
>
> **The line above is wrong, and the way it is wrong is worth more than the two entries it
> miscounts.** Gallery 30–51 are the twenty-two numbered frames of the SKILL's own gallery
> (`assets/gallery/30_…` to `51_…`), and each is a copy of one sheet in `prototypes/components/`.
> They are **not** the twenty-two board and component grids in `prototypes/gallery/`, which is what
> `capture_languages.py` writes and what `git status --porcelain` was run against. Two directories
> are called "gallery" in this repo and the packet checked the wrong one.
>
> **What actually changed: entries 35 `corgi_S6` and 36 `ledger_S6`.** This increment moved all
> eleven `S6` sheets at 100×32 (the docked key bar) and two of the twenty-two gallery sources are
> `S6` sheets. Verified two ways: `git show --name-only 12ee92c -- prototypes/components` lists
> `corgi_S6.txt` and `ledger_S6.txt` and no other gallery source, and each installed frame is
> byte-identical to its component sheet today (`cmp` on all eight spot-checked pairs, including the
> four pairs `inc67.md` and `inc69.md` name independently: 32 `prism_S3`, 35 `corgi_S6`,
> 37 `corgi_S1`, 43 `prism_S4`, 46 `swiss_S1`).
>
> The 80×24 sheets this increment also moved (11 `S1`, 10 `S4`, 9 `S6`) are **not** in the count:
> the skill's gallery is installed at 100×32 only.
>
> Corrected in place with a date rather than rewritten, which is this programme's rule for a claim
> that shipped. `inc85.md`'s and `inc86.md`'s "none changed" for 30–51 are **not** affected — inc85
> moved zero `.txt` at either width and inc86 moved no frame at all.

## §7 — deviations, named

- **`GREY_DISTINCT = 1.10` is a REPORTING threshold and nothing is gated on it.** It is roughly the
  smallest step this corpus's own tone ladders spend deliberately (solari's seam is 1.20:1 against its
  ground and round five found it legible at 100 cells of length). It is named in the source so the
  number is arguable rather than buried in a comparison. **No kit is under it**, so nothing turns on
  the value today.
- **The greyscale pass does not model colour vision deficiency**, and section H says so at length. A
  deuteranope does not see this image; simulating one would be a fourth instrument this programme has
  not built and has no reader for. Written down so the number is not spent on a claim it cannot
  support.
- **`second_width.py` writes no grey PNGs.** The ruling asks for `png/<name>.grey.png` and the
  greyscale question is about tokens, which do not change with width.

## §8 — gates

```
pytest -q                1449 passed, 2 skipped, 26 warnings in 45.33s
                         (inc83 1401 -> 1449, +48; ZERO failed --
                          test_win_clipboard_roundtrip passed again)
verify_language.py       ALL PASSED                                    exit 0
render.py                66 .txt + 66 .svg / 330 pairs / 0 hand-drawn   exit 0
matrix.py                refusals [] for all eleven                     exit 0
collision_census.py      TOTAL 27 · homoglyph rows 24 (unchanged)       exit 0
raster.py                132 PNGs identical across two PROCESSES
                         (66 colour + 66 grey)                          exit 0
legibility.py            870 lines · byte-identical across two PROCESSES exit 0
second_width.py          0 rows cut · 330 pairs distinct                exit 0
capture_languages.py     22 grids identical across two PROCESSES · gallery UNCHANGED
```

## §9 — pending / next

Handed back to the round, all three unfixed on purpose:

- **swiss `•` at 14.0 % coverage** (inc82 §6) — the floor says fail, the round that wrote the floor
  says it is visible.
- **K6 against Q1** (inc81 §5.2) — 29 of the 41 rows under the floor are `mut` and `dim` seats that
  are green under the contrast law written for them and red under the one written this week.
- **L12, amended** (§5.1) — the channel is thin, not absent. Which reading binds is a ruling nobody
  has made.
