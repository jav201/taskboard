# Quick Spec — taskboard · batch "surface" — the eighth axis becomes a renderer

**Batch:** `2026-09-03-fastflow-06` · **Base ref:** `9e94013` (branch `kanban-variants`, remote branch is gone —
commits stay local) · Predecessor `2026-08-07-fastflow-05` archived to `archive/spec-20260903-prev-closed.md`.
Language: English. Operator approved 2026-09-03 ("Sí, completa").

---

## 1. Objective (1 line)

Make the `surface` posture declared for every language in `tui-design/LANGUAGES.md` **alive in the kits** — a
`raster_region` primitive dispatched on the token, so that mutating the token changes the render — and prove it
with the same test image through all ten kits.

---

## 2. User stories

- As the skill's reader, I want each language's Surface posture to be *rendered*, not described, so that
  `LANGUAGES.md`'s own rule ("a language definition is code, not a manifest") holds for the axis it just added.
- As the emersio-lab implementer, I want Corgi's **display region** and Blueprint's **tint + measure** to exist as
  callable kit primitives, so that the lab can offer two languages instead of inventing its own chrome.
- As the operator, I want a capture per language of the *same* image so that the ten postures can be compared
  the way the ten boards already are.

---

## 3. Acceptance criteria (observable)

- [ ] **AC-1 · The token is dispatched, not decorative.** `Kit.raster_region(img: PIL.Image, w: int, h: int) ->
  RenderResult` exists on the base kit and resolves its mechanism through a registry keyed on the language token
  (`SURFACES[t["surface"]]`), the same pattern `METERS[t["meter"]]` uses. Test: for each of the ten languages,
  swapping `surface` to a *different* posture changes the rendered bytes for the same input image; swapping it
  back restores them byte-for-byte.
- [ ] **AC-2 · Every posture in LANGUAGES.md has a mechanism.** The registry implements at least: `refuse`
  (renders the language's exhibit-or-nothing per its entry — Ledger's ruled exhibit, Solari's nothing),
  `lattice` (dither to the round-dot lattice at the kit's `gap`), `display` (Corgi/Industrial: framed screen
  region, everything else stays label), `tint` (Blueprint: cyanotype + dimension spans; Phosphor's variant is
  documented but has no kit and is NOT required), `frame` (brutalist heavy box, hard edge), `depth` (Darkside:
  ±1 grey step, no border), `figure` (Swiss: one image, hairline + caption), `untinted` (nord/base16: as-is).
  Naught and Instrument share `lattice`; Corgi and Industrial share `display` with their own frames.
- [ ] **AC-3 · Two surfaces, one token.** Each mechanism produces (a) a **glyph-side** rendering (half-block or
  the kit's base, per DENSITY.md) that works on any terminal, and (b) when `textual_image` reports a raster
  transport, the **true-raster** rendering through `textual_image`'s widget, with the *same* posture applied to
  the pixels (Blueprint tints the pixels; Naught dithers them; Ledger still refuses). The layout **reserves a
  fixed rectangle** for the region in both cases (CEILINGS §7: the compositor knows the image's size, never
  its content — z-order and scroll over it cannot be correct, so nothing overlaps it).
- [ ] **AC-4 · The same image through all ten.** `prototypes/capture_languages.py` gains a `--surface` sweep
  that renders **one fixed test image** — the MBB density field, `tui-demos/lab/mbb_rho_final.npy` rendered
  to 360×120 px via the R1 colormap — through every implemented kit, producing `surface_<lang>.txt` (the
  glyph-side frame, headless, 118×34 like the boards) into `assets/languages/` of the skill via
  `export_to_skill.py`. Evidence: ten `.txt` files that **differ pairwise outside the image rectangle's
  chrome** (the acceptance boundary LANGUAGES.md already uses for boards: mask the hero, diff the rest).
- [ ] **AC-5 · True raster, captured where it can be.** For **Corgi and Blueprint** at minimum, one PNG capture
  each of the true-raster rendering in Windows Terminal (Sixel through `textual_image`), taken with the
  self-closing-window procedure (`tui-demos/.fast-dev-flow/LIMITS.md` L-19: no terminal process is ever
  killed). If `textual_image` cannot animate or place the region correctly under ConPTY, that is a **finding**
  — record it in §8 with the capture that shows it, and the glyph-side rendering stands as the shipped one.
- [ ] **AC-6 · Nothing else moved.** The existing ten `board_*.txt` and `gallery_*.txt` captures re-render
  **byte-identical** after the change (the surface region is only drawn where a screen asks for it; no
  existing screen does). `export_to_skill.py` re-run; `assets/languages.py` header still says generated.
- [ ] **AC-7 · Phosphor and BBS stay honest.** Their postures are in the registry's docstring as documented,
  with `NotImplemented` behaviour that says so — not silently mapped to another posture.

---

## 4. Validation strategy

Unit: registry dispatch (AC-1 mutation test, ten languages × one swap each), one test per mechanism on a
synthetic 8×8 image asserting the posture's defining property (lattice → only lattice glyphs; refuse → no
image glyphs at all; display → frame bars present; tint → the cyanotype palette and at least one dimension
span). Integration: the `--surface` sweep runs headless and produces ten files (AC-4), plus the byte-identity
check on the twenty existing captures (AC-6). Evidence: the ten `.txt`, the ≥2 PNG (AC-5), the pytest
transcript, and the pairwise-diff table. Batch closes when §8 names the evidence path for every AC.

### Premise table (C-43, compressed)

| Premise | Tier | Verdict | Evidence |
| --- | --- | --- | --- |
| P-1 `language.py`'s kits dispatch meters through a token-keyed registry today | premise | ✅ TRUE per LANGUAGES.md ("`METERS[t['meter']]`") — **verify at `class Kit` (line ~1214) before building on it** | LANGUAGES.md §"A language definition is code" |
| P-2 `textual_image` is a dependency and used | premise | ✅ TRUE | `pyproject.toml`, `taskboard/modals.py` |
| P-3 `capture_languages.py` runs headless on Windows python (Textual 8.2.8) | premise | ⚠ UNVERIFIED — the twenty captures exist, so it ran once; **re-run it first, before any change, and keep that output as the AC-6 baseline** | `assets/languages/INDEX.md` |
| P-4 `textual_image` places a Sixel region correctly inside a Textual layout under WT/ConPTY | hypothesis | ⚠ UNVERIFIED — AC-5 measures it; L-16 says cursor sync after an inline image breaks under ConPTY *for raw writers*; whether `textual_image` compensates is unknown | LIMITS L-16 |
| P-5 The surface token can be added to every language dict without a renderer reading an unrelated key | premise | ✅ TRUE by construction (new key) — but AC-1's mutation test is what proves it is read | — |
| E-1 (emptiness) no existing screen renders a surface region, so AC-6 must hold with zero diffs | PREMISE | asserted by the byte-identity check | — |

---

## 5. Non-goals (OUT)

- Wiring a surface region into any *existing* taskboard screen — the primitive and its sweep only. emersio-lab
  is the first consumer, in its own batch.
- Kitty / iTerm2 — WT + Sixel is the only true-raster target here (L-15).
- Phosphor / BBS kits — catalogue-only stays catalogue-only.
- Any edit to `tui-design/LANGUAGES.md` prose — the skill side is done; this batch produces the *assets* it
  points at (`languages.py`, `assets/languages/surface_*.txt`, INDEX.md rows) through the exporter.
- Re-thinking any posture. If one proves unimplementable as written, **report it** for the skill to amend.

---

## 6. Detected security flags

- [ ] Auth   - [ ] Secrets   - [ ] External integrations   - [ ] Sensitive data   - [ ] Destructive DB
- [ ] Input / attack surface   - [ ] Network / exposure

**`security_required`:** false.

---

## 7. Batch status

| Field | Value |
| --- | --- |
| Current phase | A → B (delegated 2026-09-03) |
| Started | 2026-09-03 |
| Closed | — |
| Promoted to /dev-flow | no |
| Notes | **≤ 4 source files per increment.** Inc 1: base primitive + registry + `lattice`/`display`/`tint` (Naught, Corgi, Blueprint) + the AC-1 mutation test. Inc 2: the remaining mechanisms and kits (`refuse`, `frame`, `depth`, `figure`, `untinted`). Inc 3: `--surface` sweep, AC-5 captures, export, INDEX.md, AC-6 byte-identity. One agent, sequential — `language.py` is one file. |

---

## 8. Close (filled in phase C)

### What changed
—

### How it was tested
—

### Evidence per AC
—
