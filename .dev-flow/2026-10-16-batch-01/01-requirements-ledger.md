# Requirements ledger — taskboard — Batch 2026-10-16-batch-01

> Append-only. Entries are added in chronological order and never rewritten. The live
> contract is `01-requirements.md`; this file records how it came to say what it says.
> Every entry names the requirement it amends; every requirement names its entries. `V26`
> compares the two sets of pairs both ways.

_No entries yet. The first amendment to the live contract writes the first one, in the
shape the field guide's §7 shows (`req-template.part2.md` in the guide directory init prints), and nothing
above this line is ever edited._

### LED-2026-10-16-batch-01.1 — the presentation ruler and chips (P1)
- **Requirement:** HLR-1601, LLR-1601.1, LLR-1601.2
- **Date:** 2026-10-16
- **What changed:** new requirements: a two-row date ruler (variant B) above the presentation's field and start–end chips on every field row. They supersede the PRES-C oracle frames of LLR-1001.1 (batch 2026-10-07-batch-04): TC-1001/TC-1002 are repointed to frames re-captured into this batch's evidence (`evidence/frames/PRES-B-*.txt`); the batch-04 frames stay on disk untouched.
- **Why:** the operator's verdict on `prototypes/present_rulers/` (2026-10-16): variant B, «Se ve mejor en acento» (today stays accent), plus start–end chips.
- **Evidence:** `prototypes/present_rulers/out/app-118-1-open.svg`, `app-80-1-open.svg` (the approved captures); `views.py:2727-2844` (the reused builders).

### LED-2026-10-16-batch-01.2 — the persisted "show in presentation" flag (P1)
- **Requirement:** HLR-1602, LLR-1602.1, LLR-1602.2, LLR-1602.3
- **Date:** 2026-10-16
- **What changed:** new requirements: a per-task flag, `space` / `a` in the presentation, the editor checkbox. They narrow LLR-1001.2's read-only clause (batch 2026-10-07-batch-04): the presentation now writes exactly this one flag, on `space` and `a`; opening, moving, exporting and leaving still write nothing.
- **Why:** «Que se guarde en la tarea, una bandera basta.»
- **Evidence:** `prototypes/present_rulers/out/app-118-3-hidden.svg`, `app-118-4-show-all.svg`; `models.py:991-995` (P-2).

### LED-2026-10-16-batch-01.3 — the `?` Keys band and pinned global line (P1)
- **Requirement:** HLR-1603, LLR-1603.1, LLR-1603.2
- **Date:** 2026-10-16
- **What changed:** new requirements: the Keys list becomes a full-width grid band; the palette-only global keys are pinned at the bottom of the modal, derived from `KEYMAP`.
- **Why:** «Ok, implementa la recomendación con los keys.» — the capture `out/legend-shipped.svg` shows the Keys list cut and `R`/`S` absent; `out/legend-proposed.svg` at 118×40 clipped a left-column block exactly at `R` and `S`.
- **Evidence:** `prototypes/present_rulers/out/legend-*.svg`; `keymap.py:182-189` (P-4).
