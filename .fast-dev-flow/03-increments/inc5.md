# Increment 5 — the frame reaches the glass: composited, captured, exported

Batch `2026-09-04-fastflow-07` ("chrome-on-raster", F-4) · phase B · increment
**2 of 2** · one agent, sequential. Scope from spec §7: *the raster compositing
in `capture_surface_raster.py` + the three recaptures (AC-3) + the AC-5 limb +
export (AC-6).*

Numbered `inc5` for the reason `inc4.md` gives: `inc1`–`inc3` are the `surface`
batch's and were not archived with its spec.

## 1. What changed

**P-3 is TRUE, measured in a real Windows Terminal.** The premise — "a
transparent-cell sentinel can be composited around a `textual_image` widget in
a Textual layout" — was a hypothesis, and CEILINGS §7 predicted against it (a
raster region is drawn by the terminal, not the compositor, so z-order over it
cannot be correct). It works. The capture shows corgi's orange box and its
`[1] DISPLAY` label around a live Sixel field, with **no sentinel glyph visible
anywhere in the hole** and the raster landing exactly inside the frame. The
premise table's fallback was **not** needed.

It was measured rather than argued, by building **both** answers and shooting
them:

- **`over`** — one Static carrying all of `chrome`, holes included, with the
  image widget on a higher layer offset to `image_box`. P-3 read literally.
- **`around`** — `chrome` cut at the box's edges and set around the reserved
  rectangle as its own widgets (rows above, a band of *left cells | widget |
  right cells*, rows below). Nothing is ever drawn over the raster. The
  fallback the premise table names.

Both were captured for corgi and are **pixel-equivalent**: same frame, same
placement, same glass. So P-3 is TRUE and the fallback is verified as well,
which is the better outcome than either alone — `around` is now a construction
someone can reach for without discovering it under pressure.

**`capture_surface_raster.py` is F-4's first consumer.** Its right pane was the
bare widget; it is now `chrome` composited around the widget, from the same
`RenderResult` as the left pane. The mode is the third CLI argument and the
head line reports it along with `image_box`, so a capture says what it is.

**`shoot.ps1` was brought up to LIMITS L-27, which it did not meet.** The
harness selected *"the newest `WindowsTerminal` process by StartTime"* — the
exact heuristic L-27 records as structurally unable to name a window, because
Windows Terminal is one process for every one of its windows, so that StartTime
is the process's and not the window's. L-27's own note applies to the three
captures already in this directory: they were correct **by luck**, the spawned
window having held focus. Now: `wt.exe --title` names the window before it
starts, the probe sets the same string through Textual once it is running (or
Textual would overwrite it with its own app title), selection is `EnumWindows`
plus a title match, and **more than one match throws rather than picking one**.
The grab is `PrintWindow(PW_RENDERFULLCONTENT)` with the interior-colour sanity
check and `CopyFromScreen` as a recorded-as-such fallback. **No terminal
process is killed anywhere (L-19); there is no `Stop-Process` in the file.**

**A new harness limit, found by the pictures.** The first capture through the
rebuilt harness came back as the **top-left quadrant of the window, magnified
2×**, with the window controls and half the right pane cut off. It reads like a
font-size change and is a coordinate-space mismatch: PowerShell is DPI-unaware
by default, so `GetWindowRect` returns logical pixels while `PrintWindow`
renders the window at its physical resolution, and the bitmap sized from the
logical rect gets its top-left corner filled. Same family as L-27(a) — the
coordinates were right and the pixels were not what the caller thought.
`SetProcessDpiAwarenessContext(PER_MONITOR_AWARE_V2)` before any window call
fixes it: 1148×683 became 1732×1032 and the whole window is in frame. Worth
carrying to `tui-demos`' own harness, which has the same shape.

**AC-6: the exporter documents both members**, in a new "two surfaces, one
token" paragraph plus a generated **`image box` column**. The column is
computed at the frames' own 116×26 geometry rather than at the `_probe()`'s
10×4, because a posture's box depends on the reserved size and the kit and
never on the image's content — so the number printed is the rectangle the
`.txt` beside it was actually rendered with, instead of one describing nothing
a reader can see.

## 2. Files modified

| file | source? | what |
| --- | --- | --- |
| `prototypes/capture_surface_raster.py` | source | `band()`, `composite()` with both modes, the mode argument, the L-27 window title, scoped layer CSS |
| `prototypes/export_to_skill.py` | source | `SHEET_W/SHEET_H`, the chrome/`image_box` paragraph, the generated `image box` column |
| `tests/test_surface.py` | source | `FRAME_TWINS` + `test_mutation_changes_the_chrome_too` (AC-5's limb) |
| `.fast-dev-flow/captures/shoot.ps1` | harness | L-27 title selector, `PrintWindow`, DPI awareness, `-Mode`/`-Suffix` |

**3 of 4 source files used.** No new dependency.

Captures written: `.fast-dev-flow/captures/surface_raster_{corgi,blueprint,
swiss}.png` (AC-3) and `.fast-dev-flow/probes/surface_raster_corgi_{over3,
around}.png` (the P-3 comparison).

## 3. How to test

    cd C:\Users\jjgh8\Github\taskboard\.claude\worktrees\kanban-variants
    $env:PYTHONIOENCODING = "utf-8"
    python -m pytest -q

    # AC-3, one language at a time; the window closes itself (L-19)
    .\.fast-dev-flow\captures\shoot.ps1 -Lang corgi     -Seconds 14 -Mode over -OutDir .\.fast-dev-flow\captures
    .\.fast-dev-flow\captures\shoot.ps1 -Lang blueprint -Seconds 14 -Mode over -OutDir .\.fast-dev-flow\captures
    .\.fast-dev-flow\captures\shoot.ps1 -Lang swiss     -Seconds 14 -Mode over -OutDir .\.fast-dev-flow\captures
    # the fallback, for comparison
    .\.fast-dev-flow\captures\shoot.ps1 -Lang corgi -Mode around -Suffix _around -OutDir .\.fast-dev-flow\probes

    # AC-6, into a STAGING dir -- see §6, the real export is still blocked
    python prototypes\export_to_skill.py $env:TEMP\skillstage2

## 4. Test results

    284 passed, 2 skipped, 1 failed, 4 warnings in 29.21s

Same single pre-existing environmental failure as increment 4
(`test_win_clipboard_roundtrip`, the Windows clipboard unavailable to this
shell; it failed identically on the pre-change baseline). 273 → 284 is AC-5's
eleven new parametrised cases.

**AC-5 — the 77-swap table, and its new limb.** The original
`test_mutation_changes_the_render` is **unchanged and still green** for all
eleven languages. The limb asserts the same swaps also change `chrome`.
Measured across all eleven languages × the eight live postures, exactly **one**
pair of postures collides:

| pair | languages affected | why |
| --- | --- | --- |
| `untinted` ↔ `lattice` | **all 11** | both are full-bleed and frameless — their box is the whole reserved rectangle, so both chromes are nothing but holes |

That pair is **named in the test as `FRAME_TWINS`, not skipped**, and the
assertion runs in both directions: a collision outside the pair fails, and a
collision *inside* it is asserted to still be there, so the exception cannot
silently widen the day a third posture goes frameless by accident. No
language's own posture collides with any other except through that pair.

**AC-3 — the three recaptures, and what each shows.**

| capture | what the picture shows |
| --- | --- |
| `.fast-dev-flow/captures/surface_raster_corgi.png` | `transport=sixel`, `image_box=(1, 1, 54, 24)`. The right pane now carries the orange rule and the `[1] DISPLAY` label **around the Sixel field**. Against the surface batch's version of this same file — where the right pane is bare — this is F-4 opened and closed in one comparison. |
| `.fast-dev-flow/captures/surface_raster_blueprint.png` | `image_box=(0, 1, 56, 24)`. The `360px` span sits above the raster pane and `120px` below it, cyanotype on both sides. Blueprint's chrome is on the pixels. |
| `.fast-dev-flow/captures/surface_raster_swiss.png` | `image_box=(0, 0, 53, 24)`. The hairline rule and the `mbb rho final` caption sit under the raster pane, and the gutter air stands to its right — "never full-bleed" survived the trip to the raster path. |

All three via `PrintWindow`, all three selected by title
(`taskboard-surface-<lang>-over`), one match each. No terminal process killed.

**A layout defect the headless pre-flight caught before any capture was
taken.** The first `around` build put the glass one cell LEFT of its box on
corgi — all three children of the band starting at the same column, the raster
sitting on the very bar it was supposed to be beside. Cause: `#shot { layer:
glass; }` was written unscoped, so it also matched in `around` and took the
widget out of flow. A layer is a property of the composite, not of the widget;
the rules are now scoped to `#over`. Verified after the fix, headless, with
`raster_available` forced true:

| language | image_box | placed `over` | placed `around` |
| --- | --- | --- | --- |
| corgi | (1, 1, 54, 24) | ✓ | ✓ |
| blueprint | (0, 1, 56, 24) | ✓ | ✓ |
| swiss | (0, 0, 53, 24) | ✓ | ✓ |
| industrial | (1, 1, 54, 24) | ✓ | ✓ |
| naught | (0, 0, 56, 26) | ✓ | ✓ |
| darkside | (1, 1, 54, 24) | ✓ | ✓ |

Composite 56×26 in every case — the reserved rectangle is intact in both modes.

**AC-6 — exported (to staging).** `SURFACES.md` regenerated: the paragraph
names `chrome`, `image_box`, `RASTER_HOLE` and U+E000, states that `chrome` is
derived from `rows` and not the reverse, and that a refuser's box is `None`
rather than empty. The generated column, at the frames' own geometry:

    | Naught             | lattice  | 0, 0 116x26 |
    | Corgi Engineering  | display  | 1, 1 114x24 |
    | Swiss              | figure   | 0, 0 113x24 |
    | Ledger / Solari    | refuse   | none        |

**AC-4 — re-verified after BOTH increments.** 22/22 board/gallery `.txt`,
22/22 `surface_*`, 22/22 board/gallery `.svg` — **44/44 of the spec's named
frames, 66/66 of every file the sweep writes**, byte-identical by SHA-256
against the baseline taken before the first edit.

## 5. Findings

**P-3 · TRUE** (see §1). It was a hypothesis and CEILINGS §7 argued against it;
the picture settles it. Both modes work and are pixel-equivalent. **For a still
frame** — `over` depends on the raster being painted after the chrome each
frame, which a still capture cannot distinguish from a guarantee. Anything that
animates over or scrolls past the region should use `around`, which never
overlaps. That is a recommendation from the mechanism, not from a measurement,
and it is labelled as such.

**F-6 · NEW · A DPI-unaware capture process silently grabs a quadrant.** §1.
Fixed here; `tui-demos`' `capture.ps1` has the same shape and is likely to have
the same latent defect. Not touched — that repo is out of bounds for this
batch.

**F-7 · NEW · The three captures the `surface` batch shipped were selected by a
heuristic L-27 had already refuted.** Not a new defect so much as an unapplied
fix: L-27's workaround was recorded in `tui-demos` and never carried into this
repo's harness. It is carried now. The three PNGs it produced were, per L-27's
own note, correct by luck.

**F-5 (from inc 4, still open).** `python prototypes\capture_languages.py`
remains red in its reproducibility check. One-line fix identified, not applied.

**F-1 (carried).** Not triggered in any of this batch's six sweeps.

**An unrelated stall, recorded so it is not mistaken for F-1.** One
`--surface` run, launched inside a backgrounded shell with its output
redirected to `/dev/null`, blocked for twelve minutes having consumed **0.2 s
of CPU** — blocked, not computing, and before its first file write. `settle()`
is bounded and raises, so it could not have been the settle loop. Re-running
the identical command in the foreground completed immediately. It looks like
the backgrounded shell's stdio, not this repo. The one process involved was
stopped by PID after confirming its command line; **no terminal process was
touched.**

## 6. Pending

- **The real export is still blocked, and by inc 3's decision, not by this
  batch.** `export_to_skill.py` was run into `%TEMP%\skillstage2`, not into
  `~/.claude/skills/tui-design/`. Running it for real would still carry the two
  changes inc 3 §6 flagged: the F-2 rewrite of all 20 stale `board_*` frames,
  and the F-3 addition of **prism**, which makes `INDEX.md`'s hand-written "The
  ten languages" wrong. Unchanged by this batch, and still one operator
  decision.
- **`surface_raster_ledger.png` is now an orphan.** AC-3 names corgi, blueprint
  and swiss as the three captures; the surface batch's ledger shot is still in
  `.fast-dev-flow/captures/`, taken with the pre-L-27 harness and showing the
  bare-pane rendering. Left in place — deleting evidence is not mine to do
  unasked. Either delete it or recapture it (`-Lang ledger`, which exercises
  the refusing path: `chrome is rows`, no box, no glass).
- F-5's one-line fix: decision needed.
- F-6 worth porting to `tui-demos`' `capture.ps1`, in that repo's own batch.
- The rich-in-`language.py` judgement from inc 4: operator may veto.
- `.fast-dev-flow/{baseline-f4,after-f4}/` and `.fast-dev-flow/probes/
  surface_raster_corgi_{over,over2,over3,around}.png` are working artefacts.
  `over` and `over2` are the pre-DPI-fix quadrant grabs, kept only as evidence
  for F-6; delete them once F-6 is filed.

## 7. Suggested next task

Close the batch: fill spec §8 with one evidence path per AC (they all exist
now), then settle the two decisions that are older than this batch — inc 3's
prism/export question and F-5's glob — and run the exporter at the real skill.
After that, emersio-lab is the consumer this API was built for, and it can now
ask a language for its frame and its hole separately.
