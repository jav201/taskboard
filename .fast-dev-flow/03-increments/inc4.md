# Increment 4 — the chrome reaches the raster path: `image_box` and `chrome`

Batch `2026-09-04-fastflow-07` ("chrome-on-raster", F-4) · phase B · increment
**1 of 2** · one agent, sequential. Scope from spec §7: *`RenderResult.chrome`
+ `image_box` + the sentinel + AC-1/AC-2 tests + the AC-4 baseline.*

**Why this file is `inc4.md` and not `inc1.md`.** `inc1.md`–`inc3.md` in this
directory are the `surface` batch's and were not archived when its spec was.
`inc3.md` is the file this batch was told to read — it carries the F-4 finding
being closed — so writing this batch's first increment as `inc1.md` would have
overwritten a document the batch depends on. Numbering continues instead.

## 1. What changed

**P-2 was measured FALSE, and the spec's named fallback was taken.** The
premise table asks whether "the image cells inside `rows` are identifiable —
the primitive knows where it painted the glass", and instructs: *read
`raster_region()` first; if the fused rendering does not keep the image
rectangle, the fix is to have it keep one.* It does not keep one. Every
mechanism computes its interior locally (`iw, ih = max(1, w - 2), max(1, h - 2)`
in `_surface_display`, `body = RS.halfblock(pix, w, max(1, h - 2))` in
`_surface_tint`, and so on), draws the body into it, and then **discards the
geometry**: `RenderResult` had no field for it and nothing downstream could
recover it, because the chrome and the image are the same list of markup rows
by the time the caller sees them. So the fallback was taken: each mechanism now
returns the rectangle it actually drew into.

**`RenderResult` gains `image_box` (a field) and `chrome` (a property).**

- `image_box: (col, row, w, h) | None` — where the glass went inside `rows`.
  `None` for the refusing postures, and `None` rather than a zero-size
  rectangle: a caller handed `(0, 0, 0, 0)` would reserve a degenerate region
  and composite into it, where `None` forces it to decide what refusing means.
- `chrome` — `rows` with the `image_box` cells replaced by `RASTER_HOLE`.
  A **property**, deliberately, not a fifth thing a mechanism builds: a
  mechanism that built its chrome separately could build one that disagreed
  with its own `rows` and nothing would catch it. Derived, they cannot drift —
  and `rows` never moves, which is what makes AC-4 structural rather than
  lucky. When `image_box is None`, `chrome` returns `self.rows` *itself*, so
  AC-2's `chrome is rows` is object identity.

**The sentinel is `RASTER_HOLE = "\ue000"`**, the first Private Use Area
codepoint, chosen on two measurements rather than on taste. It is one cell wide
by rich's own width table, so punching it in cannot move the reserved
rectangle. And nothing else can say it: every glyph these languages draw comes
from a declared alphabet (`LATTICE_GLYPHS`, the box constants, `RS.HALF`, the
shade ramps) and none reaches the PUA — asserted by a test, because **the
obvious sentinel fails exactly this check**: a space cannot distinguish a hole
from chrome that is blank on purpose, and swiss pads its gutter with real
spaces.

**The boxes, one line each.** `untinted` and `lattice` take the whole region —
for `untinted` that is the posture's answer ("there is no chrome") said in the
same vocabulary as every other posture, and for `lattice` the unlit dots are
the picture's dark half rather than a frame around it. `display` and `frame`
take `(1, 1, w-2, h-2)`, inside the bars. `depth` takes the same, so its chrome
is the grey inset and nothing else — the literal reading of "separates by a
step of background, never a border". `tint` takes `(0, 1, w, h-2)`, leaving
blueprint's two dimension spans above and below. `figure` stops at the gutter,
so swiss's "never full-bleed" survives into the raster path instead of being
undone by a compositor filling edge to edge.

**One convention judgement, flagged rather than made silently.** `_punch()`
uses `rich.text.Text` to slice a markup row on cell boundaries, which puts a
`from rich.text import Text` back into `language.py` — a module whose 56th pass
deliberately *dropped* its rich import, and whose `mark()` documents at length
that rich and Textual disagree about escaping. Two things were measured before
doing it. `Text` is already this axis's measuring instrument on the test side
("the cells a markup row actually draws — measured through rich, not by
`len()`"), so the role is not new. And the round-trip was checked **on
Textual's own parser**, not rich's: over every row of every language at the
sweep's geometry (11 × 26 rows), `Content.from_markup` returns the same plain
text and the same spans for the original row and for the re-emitted one, in
every case — including corgi's `\[1\] DISPLAY`, which is the exact string
`mark()` exists for. Zero mismatches. If the operator would rather not have
rich in this module, the alternative is a hand-written cell-walker over the
markup string, and it is more code for the same result.

## 2. Files modified

| file | source? | what |
| --- | --- | --- |
| `taskboard/language.py` | source | `RASTER_HOLE`, `_punch()`, `RenderResult.image_box` + `.chrome`, a box from each of the nine rendering mechanisms and an explicit `None` from `_surface_refuse` |
| `tests/test_surface.py` | source | `flipped_probe()`, `sweep_image()`, `cellwise()`, and five tests (four parametrised over the eleven languages) |

**2 of 4 source files used.** No new dependency: rich already ships under
textual and the test file already imported it.

Also written, as evidence rather than source: `.fast-dev-flow/baseline-f4/`
(the 66-file pre-change baseline) and `.fast-dev-flow/after-f4/` (the
post-change sweep it is diffed against).

## 3. How to test

    cd C:\Users\jjgh8\Github\taskboard\.claude\worktrees\kanban-variants
    $env:PYTHONIOENCODING = "utf-8"
    python -m pytest -q
    python -m pytest tests\test_surface.py -q

    # AC-4: sweep into a fresh directory and diff against the baseline
    python prototypes\capture_languages.py --sweep-to .fast-dev-flow\after-f4
    python prototypes\capture_languages.py --surface .fast-dev-flow\after-f4
    # then byte-compare .fast-dev-flow\baseline-f4 against .fast-dev-flow\after-f4

`--sweep-to` / `--surface DIR` are used instead of the documented plain
`python prototypes\capture_languages.py` because that entry point is currently
red for a reason that predates this batch — see F-5 below.

## 4. Test results

    273 passed, 2 skipped, 1 failed, 4 warnings in 28.34s

**The one failure is pre-existing and environmental**, recorded on a baseline
run taken **before any edit in this batch**: `tests/test_app.py::
test_win_clipboard_roundtrip` — `assert None == 'roundtrip 123 ABC taskboard'`,
the Windows clipboard being unavailable to this agent's shell. Baseline was
`1 failed, 230 passed`; this run is `1 failed, 273 passed, 2 skipped`. The 43
new passes and 2 skips are this increment's; nothing else moved. `inc3.md`
reported 231 passed on the operator's own terminal, which is the same suite
with the clipboard reachable.

The 2 skips are `ledger` and `solari` in the punch-out test, which asserts on
`image_box`; their case is the separate AC-2 test.

**AC-1 — cell by cell, every language.** `chrome cells` is the rendered cell
count per row × rows; `holes` counts sentinel cells found against sentinel
cells expected; `outside==rows` compares every cell outside the box, character
**and resolved style**; `leak` is the oracle below; `shipped-frame` is the
assertion against `prototypes/gallery/surface_<lang>.txt`.

| language | posture | image_box | chrome cells | holes | outside==rows | leak | shipped frame |
| --- | --- | --- | --- | --- | --- | --- | --- |
| naught | lattice | (0, 0, 24, 8) | 24 × 8 | 192/192 | True | 0 | MATCH |
| corgi | display | (1, 1, 22, 6) | 24 × 8 | 132/132 | True | 0 | MATCH |
| instrument | lattice | (0, 0, 24, 8) | 24 × 8 | 192/192 | True | 0 | MATCH |
| swiss | figure | (0, 0, 21, 6) | 24 × 8 | 126/126 | True | 0 | MATCH |
| industrial | display | (1, 1, 22, 6) | 24 × 8 | 132/132 | True | 0 | MATCH |
| nord | untinted | (0, 0, 24, 8) | 24 × 8 | 192/192 | True | 0 | MATCH |
| darkside | depth | (1, 1, 22, 6) | 24 × 8 | 132/132 | True | 0 | MATCH |
| prism | depth | (1, 1, 22, 6) | 24 × 8 | 132/132 | True | 0 | MATCH |
| ledger | refuse | **None** | `chrome is rows` | — | identity | — | MATCH |
| solari | refuse | **None** | `chrome is rows` | — | identity | — | MATCH |
| blueprint | tint | (0, 1, 24, 6) | 24 × 8 | 144/144 | True | 0 | MATCH |

**The box is TRUE, not merely declared — the oracle that says so.** A box
nobody checks is a comment. `test_the_image_box_names_the_image_and_nothing
_else` renders each region twice with two **different images of the same size**
and asks which cells moved. Every moved cell must lie inside the box (the
`leak` column: **0** for all nine rendering postures), and cells inside it must
actually move. Same size on purpose: swiss captions its figure's metrics and
blueprint spans them, so a resized probe would move chrome outside the box for
an honest reason and the check would be measuring its own probe.

The comparison is on **styled** cells, and that detail is load-bearing: a
half-block rendering draws `▀` in every cell and carries its entire content in
colour, so a plain-text comparison sees zero change inside the box and would
pass vacuously. Measured on plain text first — `inside_changed=0/132` for
corgi — which is what said the oracle had to read style.

Share of the box that moved, per posture: naught 88/192 (46 %), instrument
168/192, corgi 126/132, industrial 126/132, swiss 120/126, nord 184/192,
darkside 126/132, prism 126/132, blueprint 138/144 — 88–96 % for the eight
above naught. The test's floor is a quarter, and it is a floor rather than a
target for a stated reason: naught's lattice draws unlit grid air *inside* the
image (that air is the posture's commitment) and a duotone maps many source
values onto one cell, so a correct box legitimately holds cells two different
images agree on. The first draft of the test used a half and naught failed it
at 46 % — the threshold was wrong, not the box.

**AC-4 — nothing that renders moved.**

| group | identical |
| --- | --- |
| 22 board/gallery `.txt` | **22 / 22** |
| 22 `surface_*` `.txt` + `.svg` | **22 / 22** |
| **the spec's 44 named frames** | **44 / 44** |
| 22 board/gallery `.svg` (not named by AC-4, checked anyway) | 22 / 22 |
| **every file the sweep writes** | **66 / 66** |

Baseline captured **before the first edit** into `.fast-dev-flow/baseline-f4/`,
compared by SHA-256 against a post-change sweep in `.fast-dev-flow/after-f4/`.
This is structural rather than fortunate: `chrome` is a property derived from
`rows`, so `rows` has no path by which it could have changed.

**The AC-4 baseline sweep did not hit F-1 this time.** Both the baseline pair
and the post-change pair ran clean on the first attempt — 4 sweeps, 0 re-runs,
0 stalled animation frames. The one-in-three flakiness recorded in `inc3.md`
did not bite; that is a sample of four, not a refutation.

## 5. Findings

**P-2 · FALSE, fallback taken (see §1).** The fused rendering did not keep the
image rectangle. It does now, and it stayed inside the file cap.

**P-3 · NOT YET MEASURED.** It is increment 2's question — whether a
transparent-cell sentinel can be composited around a `textual_image` widget in
a Textual layout. Nothing in this increment tests it, and nothing here should
be read as evidence for it.

**F-5 · NEW · The documented sweep command is red, and it predates this batch.**
`python prototypes\capture_languages.py` crashes in its own reproducibility
check:

    FileNotFoundError: ...\Temp\tmpd_h74b0f\surface_blueprint.txt

`main()` collects `OUT.glob("*.txt")` — which since the `surface` batch means
33 files, 11 board + 11 gallery + 11 `surface_*` — and diffs each against the
control sweep, but the control arm (`--sweep-to`) runs `sweep()` only, which
writes 22. So the check demands a control file for every surface frame and none
is ever written. **Not caused by this batch**: it reproduces on the untouched
tree, and it is why §3 uses `--sweep-to` for both arms. It was invisible in
`inc3.md` because a `--surface` run had not yet left its output in `OUT` when
the board sweep ran. The fix is one line in the glob (`board_*.txt` and
`gallery_*.txt`, which is what the control arm produces), **not applied**: it
is a source edit outside this batch's ACs and I would rather it be a decision
than a drive-by. Left open.

**F-1 (carried, not triggered).** Four sweeps, no stall. Still open.

**A convention judgement is open for the operator**, not a defect: rich is back
in `language.py` as a measuring instrument. Reasoning and the Textual-parser
measurement are in §1; the alternative is a hand-written markup cell-walker.

## 6. Pending

- P-3, AC-3, AC-5's chrome limb, AC-6 — all of increment 2.
- F-5's one-line fix: decision needed, not applied.
- The rich-in-`language.py` judgement: operator may veto.
- `.fast-dev-flow/after-f4/` is a working artefact; it can be deleted once the
  batch closes, or kept beside `baseline-f4/` as the AC-4 evidence pair.

## 7. Suggested next task

Increment 2 as the spec scopes it: composite `chrome` around the
`textual_image` widget in `capture_surface_raster.py`, recapture corgi,
blueprint and swiss through the title-selector harness (L-19/L-27 — no terminal
process killed, one title match or refuse), add the AC-5 chrome limb naming
`untinted`/`lattice` as the pair that shares an all-holes frame, and re-run the
exporter for AC-6. **Increment 2 must decide P-3 by measurement**, and if the
sentinel cannot be composited over the reserved rectangle, take the fallback
the premise table names — chrome as a bordering widget set *around* the
rectangle — and say so.
