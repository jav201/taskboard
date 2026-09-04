# Increment 10 — AC-6 and AC-7: the workarounds are deletable, and the export is staged

Batch `2026-09-04-fastflow-08` ("kits-learn") · increment 4 of 4 · base ref `ea64fdf`.
Scope: *prove emersio-lab's two workarounds are deletable, from a temp copy; run
`export_to_skill.py` into staging and report the diff.* No git operations. **`tui-demos`
was never written to** — `git status --porcelain` there is empty, checked after the copy.

## 1. AC-6 — the lab's two workarounds are deletable

A throwaway copy of `lab-emersio` at
`%TEMP%\lab-emersio-ac6`, driven by a scratch script that renders the blueprint
chrome both ways. `_blueprint_titleblock` (48 lines) is replaced by a 10-line
function that builds **rows of cells** and hands them to `k.stamp()`;
`_cell_span` is replaced by **one changed argument** at the `raster_region()`
call site.

**The cell span (L-31):**

    BEFORE  lab, `_cell_span()`, drawn one row ABOVE the region
            '├─────────────── 60 x 20 CELLS ────────────────┤'
    AFTER   kit, inside the reserved region, from `label=`
            '├─────────────── 60 X 20 CELLS ────────────────┤'
    image_box now (0, 2, 48, 7)      -- was (0, 1, 48, 8)

**The title block (L-32):**

    BEFORE (lab, `_blueprint_titleblock`)
      |                    ──────────────────────────────────────────────────────────|
      |                    EMERSIO  MBB 60x20   PENAL 3.00  RMIN 1.50  VOLFRAC 0.40  |
      |                    ITER 6/40   C 0.130   REV 07    CONVERGED                 |
      |                    ──────────────────────────────────────────────────────────|
    AFTER  (kit, `stamp(rows, w)`)
      |                       ───────────────────────────────────────────────────────|
      |                       EMERSIO  MBB 60x20  PENAL 3.00  RMIN 1.50  VOLFRAC 0.40|
      |                       ITER 6/40  C 0.130  REV 07  CONVERGED                  |
      |                       ───────────────────────────────────────────────────────|

**What must not differ, and did not:**

| check | before | after |
| --- | --- | --- |
| token multiset (every caption and value) | 17 tokens | **identical** |
| knockouts | 1 | **1** |
| glyphs drawn | `─` | `─` |
| glyphs outside the language's ten | — | **none** |
| rows | 4 | 4 |

**What differs, and why each cell of it does.** The block is **3 cells
narrower** — 2 from the lab's `bw = max(plain) + 2` padding, 1 from the lab's
3-space separator where the kit's `GAP` is 2 — so it docks 3 cells further
right and its two rules are 3 cells shorter. **Every differing cell is the lab
adopting the kit's arithmetic**, which is what AC-6 was corrected to require
before implementing. Plus one register change: the kit letters the label in
CAPS (`60 X 20 CELLS`), which is a decision recorded in increment 8, not a
content change.

## 2. AC-7 — the export, into staging

    python prototypes\export_to_skill.py .fast-dev-flow\staging\skill

    wrote ...\assets\languages.py (22 KB, 11 languages)
    verified: 11 languages, every token, doc and family round-trips
    captures: 66 written, 0 already identical
    wrote SURFACES.md (11 postures)

("0 already identical" is the empty staging directory, not 66 changed frames.)

**Diff of the staged tree against the LIVE skill — 5 files, and they have three
different causes:**

| file | cause |
| --- | --- |
| `assets/languages.py` | **this batch** — Blueprint's `DOC` gains the series commitment and the `stamp()` clause (the two docstring edits from increments 9 and 7) |
| `assets/languages/SURFACES.md` | **this batch** — blueprint's ink `75.7 % -> 75.6 %` and its image box `0, 1 116x24 -> 0, 2 116x23` |
| `surface_blueprint.txt` / `.svg` | **this batch** — the L-31 caption span |
| `gallery_darkside.txt` / `.svg` | **NOT this batch** — byte-identical to the pre-edit baseline; the live skill is simply stale here, from the export `inc3.md` recorded as blocked. Attributed by three-way comparison rather than assumed |

`assets/languages.py`'s whole diff is the two docstring blocks; no token, no
`ORDER`, no `FAMILY` moved, and the exporter's own round-trip verification says
so. `INDEX.md` exists in the live skill and is not written by this exporter.

**The real export was NOT run.** It stays the orchestrator's call, as before.

## 3. A defect the staged export caught before it shipped

The first staging run produced a `SURFACES.md` whose blueprint row read
`0, 1 116x24` — while the `surface_blueprint.txt` **named in the same row** had
been rendered at `0, 2 116x23`. `surfaces_index()` asked each posture for its
box with **no label**, and the comment above that call promises the number
"gives exactly the rectangle the `.txt` beside it was rendered with". Once
`_surface_tint` started reading the label, that promise became false.

Fixed by naming the string in both places: `SURFACE_LABEL` in
`capture_languages.py` (the producer) and `SHEET_LABEL` in `export_to_skill.py`
(the consumer, which may not import the producer — that would pull a Textual
app and numpy in to write a markdown table, which is the duplication's stated
and still-correct reason). The table now reads `0, 2 116x23`.

## 4. Files modified

| file | source? | what |
| --- | --- | --- |
| `prototypes/export_to_skill.py` | source | `SHEET_LABEL`; `surfaces_index()` asks with the label |
| `prototypes/capture_languages.py` | source | `SURFACE_LABEL` named instead of inlined |
| `.fast-dev-flow/staging/skill/**` | artefact | the staged export (68 files) |
| `prototypes/gallery/*` | artefact | final sweeps, unchanged from increment 9 |

**2 of 4 source files used.** No new dependency. **No file in `tui-demos` was
touched**; the AC-6 patch lives in `%TEMP%` and is throwaway.

## 5. Test results

**Suite:** `315 passed, 2 skipped, 4 warnings in 27.52s` — unchanged.

**AC-4, final, both sweeps re-run:**

    FINAL: 66 frames vs pre-edit baseline -> MOVED: ['surface_blueprint.svg', 'surface_blueprint.txt']
    identical: 64 / 66

**F-1:** the final board sweep was red once (run 1 stalled in its determinism
arm, re-run green) — **3 red in 8 runs this batch**, consistent with the
recorded one-in-three. **No terminal process was killed at any point.**
**F-8:** every `--surface` run was issued plain and alone; none blocked.

## 6. Findings

**F-12 · NEW · the generator has no check that its table describes the frame it
names.** `surfaces_index()`'s comment makes a strong claim about the box it
prints and nothing tested it, so the claim went false silently the moment a
posture started reading an argument the generator did not pass. The suite
covers the important half — `test_chrome_preserves_the_frame_the_shipped_capture_shows`
asserts the shipped `.txt` matches `raster_region(..., label=SHEET_LABEL)` —
but nothing asserts that **SURFACES.md agrees with either**. Not implemented
here: it is outside this batch's ACs, and the fix is a real one (the generator
would have to re-derive the sheet's head offset the way the test does).
**Portable: a comment that promises a correspondence is a test that was not
written.**

**A consequence for emersio-lab, not a defect.** The caption span is paid for
out of the reserved rectangle, so the patched lab's glass is one row shorter
than the unpatched lab's. A lab adopting this wants `p.field.h + 1`, or it
loses a raster row it used to have. Worth saying because the lab's own version
drew the span *outside* the region and paid nothing.

## 7. Pending

- The real export to `~/.claude/skills/tui-design/` — orchestrator's call.
- `LANGUAGES.md` §11 — the replacement text is staged at
  `.fast-dev-flow/staging/LANGUAGES-11-replacement.md`, unwritten, on purpose.
- `gallery_darkside.*` in the live skill is stale from a previously blocked
  export; it will be carried in by whichever export runs next.
- F-1 (open, five frames implicated), F-8, F-12.
- `spec.md` §8 — the close.

## 8. Suggested next task

Phase C: fill `spec.md` §8 with one evidence path per AC and close the batch.
