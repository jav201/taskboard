# Increment 2 — the remaining postures, and two languages that were wearing another's clothes

Batch `2026-09-03-fastflow-06` ("surface") · phase B · one agent, sequential.
Scope from spec §7: *the remaining mechanisms and kits (`refuse`, `frame`,
`depth`, `figure`, `untinted`).*

## 1. What changed

**Four mechanisms added, so all eight postures in LANGUAGES.md now exist
(AC-2).**

- `refuse` (ledger, solari) — `pixels is None`, and that is the commitment
  being exercised rather than a gap. It delegates to `kit.exhibit()`: solari
  inherits the base, which is nothing at all ("one shape, the row; an image
  cannot flip"); ledger overrides with a **ruled exhibit** that states the
  figure and its metrics under dot leaders and draws none of it ("a figure is
  audited, not shown"), padded to a receipt's width so the page keeps the rest.
- `frame` (neo-brutalist) — raw pixels handed on untouched inside a heavy
  double box. **No kit declares this token**: LANGUAGES.md §7 has no kit in
  this repo. It is implemented because AC-2 requires the posture and because
  the mutation test renders every language through it.
- `depth` (darkside, prism) — no border glyph anywhere; the region separates on
  an inset of the language's **own next grey rung**, read from the declared
  `focus` token rather than invented as a delta. The one slow ambient motion
  LANGUAGES.md permits here is **not** implemented — nothing in this batch
  animates, and a still frame is the honest render of a motion nobody plays.
- `figure` (swiss) — set inside the type grid's gutter so it is **never
  full-bleed**, one hairline under it from the `frame` token, and a caption in
  plain cells (this language renounces drawn type).

**Two languages stopped borrowing another's vocabulary.**

- `Instrument.lattice_rows` now draws **braille** at 2×4 sub-cells with `⠐` —
  its own meter's unlit mark — for cells with no dot. It was rendering
  naught's `∙`/`◦` through the inherited hook, which put naught's identity on
  instrument's screen while `base="braille"` sat in its token dict unread.
  (Reported as R-1 in increment 1; fixed here.)
- `Industrial.DISPLAY_BOX` is a **stamped plate** (`▛▜▙▟▀▄▌▐`) — a different
  top edge from its bottom, which is why `display_chrome` returns eight glyphs
  and not two. Its glass is achromatic: LANGUAGES.md is explicit that severity
  still cannot ride colour inside that display, and the test asserts every
  pixel of it has `r == g == b`. (R-2; fixed here.)

**`raster_region` gained an optional `label`.** The postures that caption or
audit a figure (swiss, ledger) need to know what it is; the parameter is
optional because such a posture must still render without being told, falling
back to the figure's own metrics — a caption a drawing office would accept,
which an empty string is not. AC-1's `(img, w, h)` signature is unchanged.

**Tokens for the remaining five** (swiss, darkside, prism, ledger, solari), so
all eleven languages now declare a posture.

## 2. Files modified

| file | source? | what |
| --- | --- | --- |
| `taskboard/language.py` | source | four mechanisms; `depth_ground`/`caption` hooks; `DISPLAY_BOX` widened to 8 glyphs; `Instrument` lattice in braille; `Industrial` plate chrome; `Ledger.exhibit`; `label` threaded through |
| `taskboard/themes.py` | source | `surface` on the last five languages |
| `taskboard/raster.py` | source | `inset()` — the depth posture's pixel side |
| `tests/test_surface.py` | test | 11 new tests (outside the cap) |

**3 of 4 source files used.** No new dependency.

## 3. How to test

    cd C:\Users\jjgh8\Github\taskboard\.claude\worktrees\kanban-variants
    python -m pytest -q
    $env:PYTHONIOENCODING = "utf-8"
    python prototypes\capture_languages.py

AC-6 again compared against a control sweep with every `surface` token popped
before any kit is built.

## 4. Test results

    231 passed, 4 warnings in 26.85s     (194 after increment 1, +37)
    tests/test_surface.py: 67 passed in 0.29s

**AC-1 mutation table — all eleven languages, seven swaps each:**

| language | token | swaps tried | all differ | restored |
| --- | --- | --- | --- | --- |
| naught | `lattice` | 7 | YES | byte-identical |
| corgi | `display` | 7 | YES | byte-identical |
| instrument | `lattice` | 7 | YES | byte-identical |
| swiss | `figure` | 7 | YES | byte-identical |
| industrial | `display` | 7 | YES | byte-identical |
| nord | `untinted` | 7 | YES | byte-identical |
| darkside | `depth` | 7 | YES | byte-identical |
| prism | `depth` | 7 | YES | byte-identical |
| ledger | `refuse` | 7 | YES | byte-identical |
| solari | `refuse` | 7 | YES | byte-identical |
| blueprint | `tint` | 7 | YES | byte-identical |

**77 swaps, 77 differ, 11 restores byte-identical. Dead-metadata cases: none.**

**AC-6:** 22 / 22 captures byte-identical against the token-popped control, and
the sweep's own cross-process reproducibility check passed on the same run.

## 5. Risks and findings

**Bug found only by looking at the renders, not by any test that was passing.**
After 56 green tests I printed every posture as plain cells. `display_label()`
returns a literal `[1] DISPLAY` and the postures interpolate a caller's `label`
straight into a **markup** row — the codebase's own pitfall A1. It happens to
render today because rich's tag pattern rejects a leading digit, but the module
already has a convention for this (`mark()`, used by `Kit.head`) and this code
was not following it. Fixed in three places. The subtle half is the arithmetic:
escaping changes a string's **character** count and not its **cell** count, so
a mechanism that padded the escaped string would hand back a rectangle one cell
short. Padding is now measured on the plain string and the escaped one emitted.
Covered by `test_a_label_cannot_inject_markup_or_steal_a_cell`, which detects
"does this posture show a label" by asking the render for a marker rather than
by naming languages — verified non-vacuous: it asserts on swiss and ledger.

**A test I wrote was inverted and the failure caught it.** The first version
asserted the injected markup was *absent* from the plain text. Correct escaping
makes it *present* as literal characters; absence is what a **parsed** tag
looks like. The assertion has been flipped and the reasoning written into it.

**No posture proved unimplementable as written** (spec §5 / AC-7). Nothing was
substituted. Two things are narrower than LANGUAGES.md's prose and are stated
rather than hidden:

- **`depth`'s ambient motion is not implemented.** LANGUAGES.md allows the
  region "one slow ambient motion (their shader hero, at ~0.25 speed)". Nothing
  in this batch animates and no screen consumes the region (spec §5), so there
  is nothing to animate in. The still frame is complete; the motion is
  unbuilt, not refused.
- **`refuse` for ledger renders at the region's full width below ~34 cells.**
  `EXHIBIT_W` is 34 and clamps to `w`, so in a narrow region the "small ruled
  exhibit" fills it. Degrading to full width is better than degrading to
  illegible, but it is a departure from "small" at narrow measures.

**Carried from increment 1, still open:** F-1 (the capture harness's
intermittent non-determinism in `board_solari` and `gallery_blueprint`), F-2
(the shipped skill captures were already stale before this batch), F-3 (prism
is in the code and in neither skill asset — a decision is needed before
`export_to_skill.py` runs in increment 3).

## 6. Pending

- Increment 3: the `--surface` sweep over the MBB test image, AC-5 true-raster
  captures in Windows Terminal, `export_to_skill.py`, INDEX.md rows, the AC-6
  re-check. **F-3 blocks the export step and needs an operator decision.**
- `frame` has a mechanism and no language. That is correct today (no
  neo-brutalist kit exists) and worth stating in the skill.

## 7. Suggested next task

Increment 3 as specified. First question to settle: whether `export_to_skill.py`
may add prism to the skill's `languages.py`, or whether the export must be
pinned to the ten the skill currently carries.
