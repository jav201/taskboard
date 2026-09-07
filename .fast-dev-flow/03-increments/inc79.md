# Increment 79 — the density measure counts a blank as ink

**Batch:** `rework-7c`, increment 1 of 2 · a defect `legibility.py` found by looking (inc77 §7.1) and
declined to fix, because `capture_languages.ink()` is shared with the board sweep.
**Files:** `prototypes/capture_languages.py`, `tests/test_components.py` — **2 source files**, and
this packet. No frame, sheet, PNG or JSON is touched — only what a console prints moves.

**`capture_languages.ink()` did not read `BLANKS` at all.** It excluded the ASCII space and U+00A0
NON-BREAKING SPACE from its density count — a set nobody asked for and that matches nothing in the
corpus (0 NBSP in any of the 66 `.txt`, checked) — and counted **U+2800 BRAILLE PATTERN BLANK, an
EMPTY braille cell, as ink**. `verify_ink.py --frames` already had the right set (inc44:
`BLANKS = " ⠀"`) and has been reporting the correct number the whole time; `ink()` simply never read
it, so the two instruments disagreed about the same 66 files every time either was run.

One definition now: `BLANKS` lives in `capture_languages.py`, `ink()` reads it, and a new law checks
`verify_ink.py`'s own `BLANKS` against it by source text. **421 U+2800 cells moved from ink to blank —
instrument 174, prism 247 — nothing else.**

---

## 0. What was asked, and the one deviation from it, named

The brief: move `BLANKS` to one place both files read, "the module both already import." **No such
module exists, and I did not invent one.** `capture_languages.py` and `verify_ink.py` share no
project-level import today — `capture_languages` imports `taskboard.themes` (a kit file, explicitly
off-limits for this batch) and nothing else; `verify_ink.py` imports nothing project-level at module
scope. The one module that genuinely fits "both already import" is `taskboard/themes.py`, and it is
named in this worktree's own instructions as a file this batch may not edit.

**And `verify_ink.py` cannot import `capture_languages.py` for free.** Importing it sets
`os.environ["TEXTUAL_ANIMATIONS"] = "none"` at module scope (line 159) — a side effect the suite
already treats as consequential enough to save and restore around (`tests/test_capture_settle.py:41-52`
does exactly that). `verify_ink.py`'s own docstring names the two live-widget runs it drives as
**drifting for a cause "NOT established; animation phase is the suspicion, not a finding."** Importing
`capture_languages` into `verify_ink.py` would flip that exact suspect for `live_mode()` as a side
effect of moving a two-character string — a behaviour change to a different subsystem, not asked for,
and not small enough to wave through. `verify_ink.py --frames` also exists specifically to avoid the
Textual import `capture_languages` carries (its own docstring: *"it reads files"*); making it import
`capture_languages` anyway defeats that.

**So: one definition, enforced by a checked restatement, not a runtime import** — the same stance this
file already takes in `test_this_files_picture_metrics_are_the_exporters` for the SVG's cell geometry,
and the stance `raster.py`/`legibility.py`'s own laws take for the same reason (`no increment imports
raster.py or legibility.py into the suite`). `BLANKS` is declared once, in `capture_languages.py`
(§2), and a new law reads both files' source and asserts the two literals agree (§4). This is a
deviation from the brief's literal wording and is flagged here rather than done silently.

## 1. Where `BLANKS` lives now

`prototypes/capture_languages.py`, immediately before `ink()`:

```python
BLANKS = " ⠀"

def ink(rows: list[str]) -> float:
    total = sum(len(r) for r in rows)
    return sum(1 for r in rows for c in r if c not in BLANKS) / total * 100
```

Before: `c not in " \xa0"` (ASCII space + U+00A0 NBSP). After: `c not in BLANKS` (ASCII space +
U+2800 BRAILLE PATTERN BLANK) — the same pair `verify_ink.py` has declared since inc44.

**Why NBSP's removal changes nothing measured:** searched all 66 `.txt` in `prototypes/components/`
for U+00A0 — **0 occurrences.** Dropping it from the exclusion set is a no-op on the current corpus,
named so a future increment does not have to re-derive that.

## 2. Every number that moved

Recomputed old-formula vs new-formula directly against the files already on disk (no re-render
needed — `ink()` is a pure function of rows already written; the corpus was re-rendered anyway, see
§5, and moved 0 bytes). **Every row below is instrument or prism; nothing else changed anywhere.**

**`prototypes/components/*_S?.txt` (100x32, render.py's own report and `verify_ink.py --frames`'s
subject):**

```
frame           old      new     (U+2800 count)
instrument_S1  36.03%   34.28%
instrument_S4  34.06%   32.31%
instrument_S6  14.88%   12.94%
prism_S1       16.72%   14.78%
prism_S2       10.62%    8.72%
prism_S4       18.16%   16.22%
prism_S6       11.75%    9.81%
```
(instrument_S2/S3/S5 and prism_S3/S5 carry no U+2800 — unaffected.) Total moved: **174 cells across
instrument's three frames, 247 across prism's four** — 421, matching inc77's count exactly.

**`prototypes/components/w80/*_S?.txt` (80x24, `second_width.py`'s subject):**

```
instrument_S6  22.08%   18.85%
prism_S1       21.20%   20.47%
prism_S2       17.71%   14.53%
prism_S4       22.76%   22.03%
prism_S6       17.92%   14.69%
```
`second_width.py`'s printed range (`ink 13.9% .. 58.4%`) is **unchanged** — neither extreme belongs to
instrument or prism, and the JSON sidecars in `w80/` carry no `ink` field at all (`m.as_json()` and
`RA.runs_of(grid)` only), so **no committed artefact in `w80/` changes.**

**`prototypes/gallery/*.txt` (118x34, `capture_languages.py`'s own live sweep — board/gallery/surface,
a different fixture and a different geometry from the 66 components frames):**

```
board_instrument     33.70%   33.25%
gallery_instrument   15.23%   12.66%
gallery_prism        15.90%   13.24%
surface_instrument   79.16%   79.09%
```
`board_prism` carries no U+2800 and is unaffected.

**`verify_ink.py --frames` did not move** — its `BLANKS` was already correct, so it was already
printing the *new* numbers above while `render.py`'s own console (reading the same files through
`capture_languages.ink()`) printed the *old* ones for the same six frames. **The two instruments over
the identical 66 files disagreed until this increment**, which is the concrete cost of the bug this
increment closes, not merely a cosmetic one.

**No pinned test constant moved.** Searched the suite for a literal percentage, for `.ink(` call sites,
and for `k.c["ink"]` (a colour-token name that shares the string "ink" and is unrelated — grepped and
ruled out by inspection). None of `capture_languages.ink()`'s numbers are asserted anywhere in
`pytest`; they are printed to a console and, for `render.py`/`second_width.py`, folded only into a
`min`/`max` summary line that these findings do not move. **Nothing to update.**

## 3. Committed artefacts: byte-identical, checked by regenerating all of them

`render.py`, `raster.py`, `second_width.py`, `capture_languages.py`'s own sweep, and
`legibility.py` were all re-run after the fix. `git status --porcelain` on `prototypes/components/`,
`prototypes/components/png/`, `prototypes/components/w80/` and `prototypes/gallery/` is **empty** in
every case (one untracked file appeared during the run, `prototypes/components/PROTOTYPE-inheritors-5.md`
— another agent's round-five artefact, per this worktree's own instructions; not touched, not counted).
`ink()`'s return value is read only for a console print or a `min`/`max` summary in every caller; it
never reaches a `.txt`, `.svg`, `.png` or `.json` byte. **legibility.py is untouched by this fix** — its
own `ink` is a per-glyph antialiasing-coverage measure over the 9x19 raster (inc77), a different
definition with a different name that happens to share the word.

## 4. The law

**`test_capture_languages_and_verify_inks_blanks_are_one_definition`** (`tests/test_components.py`,
next to `test_this_files_picture_metrics_are_the_exporters`, which already reads
`capture_languages.py`'s source for the same reason). Reads both files' source text, regexes out each
`BLANKS = "..."` literal, and asserts they exist and are equal to each other and to `" ⠀"`. Not teeth
against a mutant — the defect it guards against is exactly "one file's constant moves and the other's
doesn't," which a source-level pin catches by construction; a planted mismatch in either file's literal
fails this law immediately (checked by hand, not left as an inference: edited a scratch copy of each
literal to `" "` alone and re-ran the law — RED both times, reverted).

## 5. Gate tails, verbatim

```
$ python -X utf8 -m pytest -q
FAILED tests/test_app.py::test_win_clipboard_roundtrip - AssertionError: assert None == 'roundtrip 123 ABC taskboard'
1 failed, 1371 passed, 2 skipped, 4 warnings in 42-44s

$ python -X utf8 prototypes/verify_language.py
  [PASS] settle() keeps headroom under its bound ...  worst 3 of 40 over 155 captures
ALL PASSED
                                                        (exit 0)

$ python -X utf8 prototypes/components/render.py
  instrument_S1        100x32  34.3% ink   0 candidates (0 refused, 0 evoked)
  instrument_S2        100x32  13.2% ink   0 candidates (0 refused, 0 evoked)
  instrument_S3        100x32  13.6% ink   0 candidates (0 refused, 0 evoked)
  instrument_S4        100x32  32.3% ink   0 candidates (0 refused, 0 evoked)
  instrument_S5        100x32  14.6% ink   0 candidates (0 refused, 0 evoked)
  instrument_S6        100x32  12.9% ink   0 candidates (0 refused, 0 evoked)
  prism_S1             100x32  14.8% ink   0 candidates (0 refused, 0 evoked)
  prism_S2             100x32   8.7% ink   0 candidates (0 refused, 0 evoked)
  prism_S3             100x32   8.9% ink   0 candidates (0 refused, 0 evoked)
  prism_S4             100x32  16.2% ink   0 candidates (0 refused, 0 evoked)
  prism_S5             100x32  11.4% ink   0 candidates (0 refused, 0 evoked)
  prism_S6             100x32   9.8% ink   0 candidates (0 refused, 0 evoked)
  66 .txt + 66 .svg -> ...\prototypes\components
  66 candidates files
  no two frames identical within a screen (330 pairs)
  0 hand-drawn elements declared (0 refused, 0 evoked)
                                                        (exit 0)

$ git status --porcelain prototypes/components/
?? prototypes/components/PROTOTYPE-inheritors-5.md     (another agent's round-5 artefact; untouched)

$ python -X utf8 prototypes/components/raster.py
  66 PNGs identical across two PROCESSES
                                                        (exit 0)

$ git status --porcelain prototypes/components/png     (empty)

$ python -X utf8 prototypes/components/legibility.py
  the report is byte-identical across two PROCESSES
                                                        (exit 0)

$ python -X utf8 prototypes/components/second_width.py
  rows the sheets had to CUT: 0 in 0 frames
  no two frames identical within a screen (330 pairs)
  66 .txt + .svg + .png + .json -> ...\prototypes\components\w80
  ink 13.9% .. 58.4%                                   (unchanged: neither extreme is instrument/prism)
                                                        (exit 0)

$ git status --porcelain prototypes/components/w80     (empty)

$ python -X utf8 prototypes/capture_languages.py
  instrument  board 118x34  33.3% ink   gallery 118x34  12.7% ink
  prism       board 118x34  27.8% ink   gallery 118x34  13.2% ink
  22 grids identical across two PROCESSES
                                                        (exit 0)

$ git status --porcelain prototypes/gallery         (empty)

$ python -X utf8 prototypes/components/matrix.py
naught [] corgi [] instrument [] swiss [] industrial [] nord []
darkside [] prism [] ledger [] solari [] blueprint []
                                                        (exit 0)

$ python -X utf8 prototypes/collision_census.py
TOTAL                       28
TOTAL homoglyph rows            24
                                                        (exit 0)
```

Suite **1370 → 1371** (+1, the one law). Census **28 / 24** unchanged. 66 `.txt`/`.svg`/`.png`, 66
`w80/` files and 22 `gallery/` captures all byte-identical to before this increment.

## 6. Risks

1. **The deviation in §0 is a judgment call, not a ruling.** The brief asked for an import; I built a
   checked restatement instead, for the reasons given, and it is weaker in one sense — a mismatch is
   caught by a suite run, not by Python failing to resolve a name. It is stronger in another: it does
   not couple a file-reading script to a Textual-importing one, and it does not touch a subsystem
   (`live_mode()`'s animation state) nobody asked to change. Flagged for the round to overrule if it
   disagrees.
2. **`collision_census.py` and `tests/test_components.py` (line 3118) each carry a THIRD and FOURTH
   independent `BLANKS = " ⠀"`.** Both already have the correct value and neither is a consumer of
   `capture_languages.ink()` — `collision_census.py`'s is for the homoglyph census, `test_components.py`'s
   `cell_ink()`/`_cells()` are a different per-cell weight, not a density fraction. Not touched: the
   brief named two files, and a fifth definition unified in the same increment would be scope this
   packet did not ask for. Named here so a future increment does not have to re-discover the count.
3. **Every number in §2 is a number this specific corpus produced.** A future language or frame that
   spends U+2800 will move by exactly its own count of that glyph; nothing about the fix is
   corpus-specific.

## 7. Pending — not this increment

- inc80: the `w > 800` width-bound law (inc78 §5), same batch, next increment.
- `collision_census.py`'s and `test_components.py`'s own `BLANKS` are correct and independent; left
  alone (§6.2).

## 8. Suggested next task

`inc80`, as briefed: rewrite the full-measure predicate relative to the frame's own width.

## Evidence checklist

- [x] **Tests/type checks/lint pass — WITH ONE RED, NAMED.** `1371 passed, 2 skipped, 1 failed`
      (baseline `1370 passed`). The failure is `tests/test_app.py::test_win_clipboard_roundtrip`,
      environment-coupled (spec §10.6) — reported, not counted, not touched. `verify_language.py` ALL
      PASSED exit 0. `render.py` 66/330/0. `matrix.py` refusals `[]` for all eleven.
      `collision_census.py` TOTAL 28, homoglyph rows 24 — unchanged. `raster.py` and `legibility.py`
      byte-identical across two processes. `second_width.py` 0 rows cut, 330 pairs distinct.
- [x] **No secrets in code or output** — one constant, one function body line, one law. No network, no
      new dependency, no path outside the worktree.
- [x] **No destructive commands run without approval** — none. All artefact regeneration overwrote
      files with byte-identical content, verified by `git status --porcelain` before any write was
      trusted.
- [x] **File count within cap** — **2 source files**: `prototypes/capture_languages.py`,
      `tests/test_components.py`.
- [x] **Review packet attached** — this document.
