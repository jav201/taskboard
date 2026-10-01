# Review — taskboard — Batch 2026-09-30-batch-01

> Phase 2, two-lens cross-review (core). Lenses: `qa-reviewer` and `ux-reviewer`, each
> spawned as an independent sub-agent with its role file, read-only, over
> `01-requirements.md` as drafted at P1. Security lens: not triggered (no auth, secrets,
> external tools, deploy; a local TUI layout/render change).

## ✅ Verdict (read first)

- **Gate:** both lenses returned `iterate-to-refine`; every finding was folded into the live contract (ledger entries `LED-2026-09-30-batch-01.1`–`.4`) or declared with a disposition below; after the fold → `approve` → Phase 3, under the batch's standing authorization (PLAN header).
- **Out-of-scope findings:** 3 named and routed below (Q-2 owner question, Q-7 partial, UX-9).
- **Findings:** 3 blocker · 13 major · 8 minor
- **shall/should check:** ✓ clean (QA: "no `should` appears in any statement")
- **Two-layer (blockers):** ✓ after fold — every story has an `AT` (US-001: AT-001/002/005; US-002: AT-003/006; US-003: AT-004); ATs drive `TaskboardApp.run_test` or the functions the app calls.
- **Census (change-first):** done — best-effort + gate-confirmed (the full suite at the increment gate is the guarantee).
- **Security:** ✓ no findings (not triggered).
- **Evidence checklists:** QA and UX lens reports summarised in the findings table.

## Detail

### Findings
| ID | Reviewer | Severity | Area / Req | What | Recommendation | Status |
|----|----------|----------|------------|------|----------------|--------|
| Q-1 | qa | blocker | HLR-004 | badges break the AC5/Prism priority-hue law pinned in `tests/test_palette_ration.py` | ledger supersession + list nodes | fixed — LED .1, HLR-004 `Supersedes` |
| Q-2 | qa | blocker | HLR-004 | `++` green is also a project hue; not in A2 | owner accepts or picks other tone | declared — the commission fixes the tone ("same tones `_highlight_markup` uses"); recorded in §6.3 and THE GLYPH HOUSE; routed to owner |
| Q-3 | qa | blocker | HLR-002 | nothing required the preview to render on open | add on-open arm | fixed — LED .3 |
| Q-4 | qa | major | HLR-003 | band semantics unstated (blocked, order, focus, archived) | state each | fixed — LED .4 |
| Q-5 | qa | major | AT-003 | hand-listed default-mode input set | derive from seat tuples; fixture minimum | fixed — LED .4 |
| Q-6 | qa | major | AT-003/004 | surface was render-only | drive the app for walk and badges | fixed — AT-003 walks keys in the app; AT-004 reads the app's board |
| Q-7 | qa | major | LLR-004.2 | legend ghosts under focus / matrix | key on drawn | partial — keyed on visible open cards; focus/matrix ghost is a pre-existing class needing `app.py` plumbing → §6.3 + BACKLOG |
| Q-8 | qa | major | §5.2 | "every new test RED on base" contradicts preservation tests | exempt, use mutations | fixed — §5.2 |
| Q-9 | qa | major | HLR-003 | selected card / priority change / tall column | add arms | fixed (AT-006); tall column declared (UX-9) |
| Q-10 | qa | minor | HLR-001 | no preview floor | numeric floor | fixed — LED .2 |
| Q-11 | qa | minor | LLR-001.1 | threshold unvalued | fix at P3, test ±1 | fixed — statement + threshold |
| Q-12 | qa | minor | LLR-001.2 | hardcoded hex; TextAreas excluded silently | `HEX["accent"]`; justify | fixed |
| Q-13 | qa | minor | HLR-004 | blocked `▲` over beside `!!` over | name it | fixed — §6.3 |
| UX-1 | ux | major | HLR-001 | no tab order | AT with real tab | fixed — AT-005, LED .2 |
| UX-2 | ux | major | HLR-001 | Save visible ≠ operable | tab + enter; esc discards | fixed — AT-005 |
| UX-3 | ux | major | HLR-001 | key hints not observable | painted in full | fixed — LED .2 |
| UX-4 | ux | major | HLR-002 | preview scroll role | keep cursor line in view | fixed — LED .3 |
| UX-5 | ux | major | HLR-003 | cursor identity across reorder | AT | fixed — AT-006 |
| UX-6 | ux | major | LLR-001.2 | style read-back is a pre-paint proxy | painted check | fixed — threshold adds the painted bar |
| UX-7 | ux | minor | HLR-001 | 80×24 margin may be zero | re-measure | P3 measures and reports |
| UX-8 | ux | minor | §6.3 | badge cost figure | correct | fixed |
| UX-9 | ux | minor | HLR-003 | tall column scroll | boundary arm | declared, not tested (mechanism unchanged) |
| UX-10 | ux | minor | D1/D2 | say band is grouped-only | help text | fixed — LLR-004.2 |
| UX-11 | ux | minor | §5 | no non-automated evaluation declared | declare | fixed — §6.1 |

### shall / should check
Clean.

### Census
Change-first over the planned files (`taskboard/modals.py`, `taskboard/taskboard.tcss`,
`taskboard/views.py`): tests asserting on `TaskModal` ids/titles (`tests/test_app.py`,
`tests/test_emoji_picker.py`), on `card_cell`'s `!` (`tests/test_palette_ration.py`,
`tests/test_app.py::test_prio_cycle…`; `tests/test_lanes_grid.py` is the swimlanes view —
unaffected), on the legend ghost law (`tests/test_legend.py`). Best-effort; the increment
gate's full-suite run is the completeness guarantee.
