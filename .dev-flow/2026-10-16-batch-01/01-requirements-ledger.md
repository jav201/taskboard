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

### LED-2026-10-16-batch-01.4 — P2 iteration 1 amendments (P1, iterate-to-refine)
- **Requirement:** HLR-1601, HLR-1602, HLR-1603, LLR-1601.1, LLR-1601.2, LLR-1602.2, LLR-1602.3, LLR-1603.1, LLR-1603.2
- **Date:** 2026-10-16
- **What changed:** HLR-1603 / US-1603 / AT-1603: "no scroll" is owed by the pinned global line only; the Keys band is in the scrolled body, listed whole (architect A-1 blocker — the band cannot fit unscrolled at 80×24). LLR-1603.2: the hint takes its own pinned row; 2 pinned rows at 118×30, 3 at 80×24; entries joined by two spaces (A-2, UX-3). LLR-1603.1: the order arm at 7 keys / 3 columns (QA-4). HLR-1601 / LLR-1601.2: the oracle named `evidence/frames/PRES-R-*.txt` (the batch-04 `PRES-B-*` names were taken); AT-1001 repointed with TC-1001/1002; hand-written literal chips; cross-year format stated (QA-1, QA-2, A-6, A-7). LLR-1601.1: the `over` echo arm and the weekend precondition (QA-8). HLR-1602 split into six numbered clauses with their TCs (A-8); its negative control is AT-1602's base-RED; the export arm (QA-6, QA-7). LLR-1602.2: axis refit, next-task cursor, all-hidden frame, `present_hidden`'s population, `priority=True` for `space`/`a`, the undo interaction (QA-3, UX-4, UX-5, UX-6, A-3, A-4, A-5). LLR-1602.3: the checkbox in the title row, `TASK_CHIPS_ONE_ROW` unchanged, the 80×24 visibility arm (UX-1). §6.3: the cross-check's criterion and the two deltas; the stray-`space` limit (UX-8).
- **Why:** the P2 review of 2026-10-16 (architect, qa-reviewer, ux-reviewer — all `iterate-to-refine`).
- **Evidence:** `02-review.md` §Findings; refuted: QA-9 (`prototypes/present_rulers/` exists — `ls prototypes/present_rulers/app_capture.py`); UX-7 kept the commission's exact narrow hint text.

### LED-2026-10-16-batch-01.5 — P2 iteration 2 minor amendments (P2 gate)
- **Requirement:** HLR-1601, HLR-1603, LLR-1601.1, LLR-1601.2, LLR-1602.2, LLR-1602.3, LLR-1603.2
- **Date:** 2026-10-16
- **What changed:** HLR-1603's title matches its statement (ux N-1); HLR-1601's "empty" and "invalid" catalog entries name the arms that cover them, TC-1601 (no open task) and TC-1602 (unparseable date), and LLR-1601.1/.2's catalogs agree (qa N-1, N-2); the hint count is `len(present_hidden(...))` (architect N-2); `space` with every task hidden writes nothing, as a TC-1604 arm (ux N-4); the editor's tab order after the title is stated (ux N-3); TC-1607 computes its expected row counts from `KEYMAP` (architect N-1, qa N-3); the owed 80-column visual verdict carries the `⏸ DEFER` marker (architect N-3).
- **Why:** the P2 re-review of 2026-10-16: architect `approve`, ux-reviewer `approve`, qa-reviewer `iterate-to-refine` on one remaining catalog inconsistency. The orchestrator approved the gate under the standing authorization: every remaining item is a minor wording or catalog fix that changes no obligation, each applied here and re-read.
- **Evidence:** `02-review.md` §Findings (iteration 2).

### LED-2026-10-16-batch-01.6 — the P2 security lens (C8) minor amendments (P2 gate)
- **Requirement:** HLR-1602, LLR-1602.1
- **Date:** 2026-10-16
- **What changed:** LLR-1602.1: `show_in_present` joins `_TASK_KEYS`; a hand-edited non-boolean loads as shown and is dropped on save; after hide-then-show nothing remains in `extra` (security F1). HLR-1602 / AT-1602: the export arm asserts the hidden task's title is absent and the open count drops, not only the word `hidden` (security F2).
- **Why:** the security-reviewer's P2 return (C8 fired), 2026-10-16: `approve`, two LOW.
- **Evidence:** `models.py:706-709` (`_TASK_KEYS`), `models.py:995` (the `{**extra, **d}` merge); `app.py:255-260` (the export re-renders with the frame's arguments).

### LED-2026-10-16-batch-01.7 — the oracle cross-check's third delta (P3, increment 001)
- **Requirement:** HLR-1601
- **Date:** 2026-10-16
- **What changed:** §6.3 (the cross-check criterion that HLR-1601's threshold rests on). **Before →** "every row must be equal except two listed deltas — row 0's title … and the shipped in-frame keys row". **After →** "… except three listed deltas — D1 …, D2 …, and D3 row 2's label column only …". **Deleted:** `two listed deltas`. **New:** `three listed deltas`, `D3`.
- **Why:** running `evidence/gen_frames.py` at increment 001 showed one row differing beyond D1/D2: the tick row's label column. The prototype `render_b2` labels it `cursor's dates ▸` whenever an echo exists; the commission (decision 1) says "tick row = scale label (or the echo label when it does not fit in the field)", which the shipped renderer follows. The field and chip cells of that row match the prototype byte for byte.
- **Evidence:** `evidence/gen_frames.py` output (`HOLDS (deltas D1, D2, D3 only)` at 118x30 and 80x24). Parent re-read: HLR-1601's statement is unchanged (the ruler's label column is LLR-1601.1's, which already states the commission's rule); TC-1001/TC-1002/AT-1001 unchanged.
