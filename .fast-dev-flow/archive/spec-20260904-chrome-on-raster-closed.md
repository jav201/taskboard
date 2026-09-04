# Quick Spec — taskboard · batch "chrome-on-raster" (F-4)

**Batch:** `2026-09-04-fastflow-07` · **Base ref:** `5b48313` (branch `kanban-variants`, on the remote again as of 2026-09-04) ·
Predecessor `surface` closed 2026-09-03, archived to `archive/spec-20260904-surface-closed.md`. Language: English.
Operator direction 2026-09-04: "armar el plan detallado y delegar implementación a agentes opus5".

---

## 1. Objective (1 line)

Make a language's **chrome reach the raster path** — so a consumer that renders true pixels through `raster_region()`
can also draw the posture's frame (Corgi's `[1] DISPLAY` box, Blueprint's dimension spans, Swiss's hairline and
caption) around them, from the same primitive, without re-deriving it.

---

## 2. User stories

- As emersio-lab, I want `raster_region()` to hand me the posture's chrome **separately** from the glass, so that I can
  place a Sixel field inside Corgi's display box or under Blueprint's spans instead of inventing my own frame.
- As the skill's reader, I want the true-raster captures to show the *whole* posture — frame and pixels — so that
  `surface_raster_corgi.png` stops contradicting `surface_corgi.txt` about what the language looks like.
- As the operator, I want nothing that already renders to move.

---

## 3. Acceptance criteria (observable)

- [ ] **AC-1 · The result carries its chrome apart from its glass.** `RenderResult` gains a third member alongside
  `rows` (fused glyph rendering) and `pixels` (glass alone): **`chrome`** — the posture's frame as a glyph rendering
  of the *same* reserved rectangle with the image cells **transparent** (a documented sentinel cell that a compositor
  treats as "do not paint"), plus `image_box: (col, row, w, h)` naming where the glass goes inside it. Test: for every
  language, `chrome` is exactly `rows` with the image cells replaced by the sentinel — asserted cell-by-cell against
  the shipped `surface_<lang>.txt`.
- [ ] **AC-2 · `refuse` has no image box, and says so.** For `ledger` and `solari`, `chrome` is `rows` unchanged and
  `image_box is None`. A consumer asking a refusing language for a box gets `None`, never a zero-size rectangle.
- [ ] **AC-3 · The raster captures show the posture.** `prototypes/capture_surface_raster.py` composites `chrome`
  around the `textual_image` widget: Corgi's orange box and `[1] DISPLAY` label frame the raster pane; Blueprint's
  `360px`/`120px` spans sit over it; Swiss's hairline and caption below it. Three recaptures in Windows Terminal via
  the title-selector harness (never kill a terminal process — `tui-demos` LIMITS L-19, L-27), replacing the three
  existing PNGs in `.fast-dev-flow/captures/`.
- [ ] **AC-4 · Nothing that renders moved.** The 22 board/gallery captures and the 22 `surface_*` frames re-render
  **byte-identical** — `rows` is untouched; `chrome` is derived from it, not the other way round.
- [ ] **AC-5 · The mutation test still holds, and gains a limb.** The 77-swap table from the `surface` batch passes
  unchanged, and for each language swapping the token also changes `chrome` (except between two postures that
  share a frame, which the test names explicitly rather than skipping).
- [ ] **AC-6 · Exported.** `export_to_skill.py` re-run; `assets/languages/SURFACES.md` documents `chrome` and
  `image_box` in its "two surfaces, one token" paragraph (generated text — edit the exporter, not the file).

---

## 4. Validation strategy

Unit: the cell-by-cell `chrome == rows with image cells → sentinel` assertion per language (AC-1), the `None` box for
refusers (AC-2), the mutation limb (AC-5). Integration: byte-identity of 44 existing frames against the pre-change
baseline captured **first** (AC-4). Evidence: the three recaptures (AC-3) and the pytest transcript. Batch closes when
§8 names one evidence path per AC.

### Premise table (C-43, compressed)

| Premise | Tier | Verdict | Evidence |
| --- | --- | --- | --- |
| P-1 `rows` already contains the chrome for every non-refusing posture (the glyph side draws the frame) | premise | ✅ TRUE by the surface captures — Corgi's box and Blueprint's spans are visible in `surface_*.txt` | `SURFACES.md`, `inc3.md` F-4 |
| P-2 The image cells inside `rows` are identifiable (the primitive knows where it painted the glass) | premise | ⚠ UNVERIFIED — **read `raster_region()` first**; if the fused rendering does not keep the image rectangle, the fix is to have it keep one, which is inside the ≤4-file cap | `taskboard/language.py` |
| P-3 A transparent-cell sentinel can be composited around a `textual_image` widget in a Textual layout | hypothesis | ⚠ UNVERIFIED — AC-3 is the test; the fallback is to render `chrome` as a bordering widget set *around* the reserved rectangle rather than over it, and say so | CEILINGS §7: the region is opaque to the compositor |
| E-1 (emptiness) no existing screen or frame changes | PREMISE | asserted by AC-4's byte-identity | — |

---

## 5. Non-goals (OUT)

- Wiring the chrome into any taskboard screen — emersio-lab is the consumer, in its own batch.
- New postures, new languages, Phosphor/BBS kits.
- Fixing the capture harness's one-in-three flakiness (F-1) — separate fix; if it bites, re-run and record the count.
- Any edit to `tui-design/*.md` prose by hand — assets change through the exporter only.

---

## 6. Detected security flags

None. **`security_required`:** false.

---

## 7. Batch status

| Field | Value |
| --- | --- |
| Current phase | A → B (delegated 2026-09-04) |
| Started | 2026-09-04 |
| Closed | — |
| Promoted to /dev-flow | no |
| Notes | **≤ 4 source files per increment.** Inc 1: `RenderResult.chrome` + `image_box` + the sentinel + AC-1/AC-2 tests + AC-4 baseline. Inc 2: the raster compositing in `capture_surface_raster.py` + the three recaptures (AC-3) + AC-5 limb + export (AC-6). One agent, sequential. |

---

## 8. Close (filled in phase C)

### What changed
—

### How it was tested
—

### Evidence per AC
—
