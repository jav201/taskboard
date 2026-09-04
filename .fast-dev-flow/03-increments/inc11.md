# Increment 11 — F-12: the surface index now checks its own table

Standalone close-out of `F-12` (recorded in `inc10.md`, batch `2026-09-04-fastflow-08` "kits-learn",
increment 4 of 4) · base ref `99824be` (branch `kanban-variants`, tree clean). One agent, one increment,
2 source files. No git operations.

Scope: *make `surfaces_index()` in `export_to_skill.py` verify, for every language, that the `image box`
it is about to print matches the shipped `surface_<lang>.txt` frame it names — an error that aborts the
export on disagreement, not a warning — then run the export into staging and diff it against the live
skill.*

## 1. The finding, restated

`inc10.md` §6: `surfaces_index()` asked each posture for its box with a **fresh, unlabelled**
`raster_region()` call and printed it beside the `.txt` filename, and nothing checked the two actually
agreed. In the kits-learn batch this printed blueprint's box as `0, 1 116x24` beside a frame rendered at
`0, 2 116x23` — caught by a person reading the staged table, not by a test. The comment above the call
already claimed the number "gives exactly the rectangle the `.txt` beside it was rendered with"; nothing
tested that claim.

The label bug itself was fixed in `inc10.md` (`SHEET_LABEL`/`SURFACE_LABEL`, named in both files). F-12
is the second half: **nothing stops the claim going false again**, by the same failure or a different
one (a stale capture, a kit whose `raster_region()` changes shape). This increment adds that check.

## 2. What F-12's own wording got wrong once I tried to build it

Two things the finding said, that turned out not to hold exactly as written:

**"the RASTER_HOLE/glass rectangle actually present in `surface_<lang>.txt`."** `RASTER_HOLE` never
appears in a shipped `.txt` — `test_no_language_can_draw_the_hole_itself` already asserts that, and it is
true here too: the shipped artefact is `rows` (frame **and** image, fused), not `chrome`. The hole only
exists in a freshly computed `chrome`. So "the rectangle actually present" has to be **derived**, not
read off the file: compute `chrome` fresh from `raster_region()`, and find where the shipped frame and
that `chrome` **disagree** — that disagreement *is* the glass rectangle, measured independently of
whatever `image_box` claims about itself, which is the property that makes the check worth having (a bug
in `image_box` cannot mark its own homework this way).

**Using a small probe image (the exporter's existing `2x2`, or the test file's `24x8`) is not enough.**
The original `surfaces_index()` used a flat `2x2` probe because "a posture's image box depends on the
RESERVED SIZE and on the kit, never on the image's content" (true for `image_box` itself). But two
languages caption or audit the image's **dimensions** as literal text, read off `img.size` rather than
off a pixel: Ledger's `exhibit()` prints `"{img.size[0]} px"` / `"{img.size[1]} px"` rows, and
Blueprint's third dimension span prints `"{img.width}px"`. Checking those kits' `chrome` against the
shipped frame with a `2x2` probe produced **false positives** — a small, non-rectangular block of
disagreeing cells from `"2px"` vs the shipped `"360px"`, nowhere near the real glass — even though the
exporter's printed rectangles were correct. Fixed by sizing the probe to the sweep's own image dimensions
(`IMG_W, IMG_H = 360, 120`, matching `capture_languages.py`'s `test_image()`) while keeping its pixel
content flat and synthetic, so the check needs neither `numpy` nor the other repo's `.npy` — only the
caption *text* has to agree, and captions read a size, never a colour.

## 3. Implementation

`prototypes/export_to_skill.py`:
- `IMG_W, IMG_H = 360, 120` — the sweep's own image size, repeated (not imported) for the reason
  `SHEET_LABEL` already gives: importing `capture_languages.py` pulls in a Textual app and numpy to write
  a markdown table.
- `_probe()` now returns a flat `IMG_W`x`IMG_H` image instead of `2x2` — same reasoning above.
- `SurfaceIndexMismatch(RuntimeError)` — the error the export raises (uncaught, aborting the script) when
  a language's box disagrees with its shipped frame.
- `_derive_glass_box(shipped, chrome)` — the rectangle where two texts disagree; raises
  `SurfaceIndexMismatch` if the disagreeing cells are not a solid rectangle (a partial or leaked hole),
  returns `None` if they agree everywhere (the `refuse` postures).
- `check_box_matches_shipped(n, gallery=GALLERY)` — reads `surface_<n>.txt`, re-derives the head offset
  via `kit.sect("SURFACE", "probe", SHEET_W, SHEET_H)` (the same technique
  `test_chrome_preserves_the_frame_the_shipped_capture_shows` uses; the placeholder `note` text does not
  change `head`'s LENGTH for any of the eleven kits — verified by inspecting all eleven `sect()`
  overrides, only `title`, `w`, `h` affect it and those three are fixed), computes `raster_region()`,
  compares `_derive_glass_box(shipped, chrome)` to `res.image_box`, raises on disagreement (both
  rectangles named in the message), and returns `res` so the caller need not render twice.
- `surfaces_index()`'s loop now calls `check_box_matches_shipped(n)` in place of the old direct
  `raster_region()` call, reusing its returned `res` for the table row.

`tests/test_surface.py`:
- `test_check_box_matches_shipped_is_green_for_all_eleven_frames` — parametrized over `ORDER`, asserts no
  exception against the real shipped `prototypes/gallery/`.
- `test_check_box_matches_shipped_aborts_when_a_frame_is_stale` — the mutant: `surface_blueprint.txt`'s
  reserved 26-row band rolled down by one (its own row 0 duplicated at the top, its old last row dropped)
  in a `tmp_path` copy, same shape of drift F-12 actually shipped. Asserts `SurfaceIndexMismatch`.

## 4. Files modified

| file | source? | what |
| --- | --- | --- |
| `prototypes/export_to_skill.py` | source | `IMG_W`/`IMG_H`, sized `_probe()`, `SurfaceIndexMismatch`, `_derive_glass_box`, `check_box_matches_shipped`; `surfaces_index()` calls it |
| `tests/test_surface.py` | source | the green-over-eleven test and the stale-frame mutant |
| `.fast-dev-flow/staging/skill/**` | artefact | re-exported, see §6 |

**2 source files.** No new dependency (`rich.text.Text` was already a transitive dependency via `rich`,
already imported elsewhere in this package; `Path` already imported).

## 5. Test results

```
$ python -m pytest -q
327 passed, 2 skipped, 4 warnings in 29.98s
```

315 baseline + 12 new (11 languages × green, 1 mutant abort) = 327. No regressions, no new skips.

```
$ python -m pytest tests/test_surface.py -q -k "check_box_matches_shipped"
12 passed, 135 deselected in 0.39s
```

Manual run of the check itself against every shipped frame, before the pytest wrapper existed:

```
naught      OK lattice (0, 0, 116, 26)
corgi       OK display (1, 1, 114, 24)
instrument  OK lattice (0, 0, 116, 26)
swiss       OK figure  (0, 0, 113, 24)
industrial  OK display (1, 1, 114, 24)
nord        OK untinted(0, 0, 116, 26)
darkside    OK depth   (1, 1, 114, 24)
prism       OK depth   (1, 1, 114, 24)
ledger      OK refuse  None
solari      OK refuse  None
blueprint   OK tint    (0, 2, 116, 23)
```

Blueprint reports `(0, 2, 116, 23)` — the CORRECT rectangle `inc10.md` fixed, now independently verified
against the shipped `.txt` rather than trusted.

## 6. The export, into staging

```
$ python prototypes/export_to_skill.py .fast-dev-flow/staging/skill
  wrote .fast-dev-flow\staging\skill\assets\languages.py (22 KB, 11 languages)
  verified: 11 languages, every token, doc and family round-trips
  captures: 66 written, 0 already identical -> .fast-dev-flow\staging\skill\assets\languages
  wrote SURFACES.md (11 postures)
```

The export completed — meaning `check_box_matches_shipped` passed for all eleven inside the real run,
not only in the test. Diff against the **live** skill (`~/.claude/skills/tui-design`):

```
$ diff -q ~/.claude/skills/tui-design/assets/languages.py .fast-dev-flow/staging/skill/assets/languages.py
(identical)
$ diff -rq ~/.claude/skills/tui-design/assets/languages .fast-dev-flow/staging/skill/assets/languages
Only in ~/.claude/skills/tui-design/assets/languages: INDEX.md
```

**No diff beyond `INDEX.md`**, which `export_to_skill.py` has never written (noted already in `inc10.md`
§2). Expected: `99824be` — this worktree's base — was exported for real on 2026-09-04, so a re-export of
unchanged rendering code against an unchanged `prototypes/gallery/` reproduces the live skill exactly.
This increment changed only the exporter's own verification logic, not any language's rendering, so no
frame moved.

**The real export was NOT re-run against `~/.claude/skills/tui-design/`.** That stays the orchestrator's
call, as in every prior increment; staging is where this was proven.

## 7. Risks

- `check_box_matches_shipped`'s `_probe()` uses a **flat** `IMG_W x IMG_H` image, not the real MBB field.
  This is sufficient for what the check verifies — geometry and any caption that reads `img.size` — but a
  kit that someday captions a **content-derived** statistic (a mean, a histogram bucket) would need the
  real sweep image to check truthfully, and this check would not catch a mismatch there. None of the
  eleven kits does today (confirmed by reading all eleven `sect()` overrides and Ledger's `exhibit()`;
  Blueprint's span and Ledger's audit both read only `img.size`).
- The mutant test rolls only `blueprint`'s frame. The green-over-eleven test covers real agreement for
  all eleven, but the "shows the abort" limb is demonstrated on one language, matching the increment
  brief ("a mutant limb that shifts one frame's recorded box by a row").

## 8. Pending

- F-1, F-8 (both from `inc10.md`, untouched by this increment).
- `spec.md` §8 for the kits-learn batch — still unfilled per `inc10.md` §7; this increment does not
  reopen that batch's spec, it closes a finding recorded against it.
- The real export to `~/.claude/skills/tui-design/` — orchestrator's call, as always.

## 9. Suggested next task

Nothing else is open against this batch's findings besides F-1/F-8, both already characterized in
`inc10.md` as out of this scope. If the operator wants `spec.md` closed for kits-learn, that is the
remaining item; otherwise this line of work is done.
