# Validation — taskboard — Batch 2026-10-06-batch-01

> Phase 4 (P4) — the four lenses re-read the WHOLE delta on the final tree, cross-increment
> threads pulled, the coverage gaps pinned, the captures taken. The per-increment gates each
> passed before this; P4 is the cross-increment read + the operator's visual verdict setup.

## ✅ Verdict (read first)

**PASS-WITH-NOTES — all four lenses.** qa-reviewer PASS-WITH-NOTES (0 HIGH/MEDIUM) ·
architect PASS-WITH-NOTES (0 gate-blocking) · security-reviewer PASS-WITH-NOTES (0 HIGH, 0
MEDIUM) · ux-reviewer PASS-WITH-NOTES (0 blockers/majors). The full suite on the final tree:
the close-gate run (evidence below; the lenses' own runs agreed — 2509 collected, the single
failure in dirty environments is the declared G-011 clipboard flake, and the NO_COLOR
incident below). **No finding iterates to P1.**

## What P4 verified (cross-increment threads, executed by three lenses independently)

1. **The undo stack's mixed shapes** (cascade / milestones / migration / single-task):
   disjoint dispatch keys, every interleaving replays to byte-identical board state, `m`
   refuses verbatim on every non-cascade top, a purge mid-entry skips and survivors restore.
2. **`m` parity** — the bump and the editor push the IDENTICAL entry shape; `m` re-applies
   either surface under the next mode (pinned now by TC-637).
3. **The toast ladder** at 118/80/60/40/24…: fits everywhere, names→count→suffix narrowing
   per §1.3; below ~60 the cascade information degrades by design (the contract pins 118/80).
4. **Team sync (D-630)** — existing projects merge only name/color/status/dates/archived; a
   project first seen in a push imports `date_links` whole (S-4, lenient); cascade-moved
   dates ride the shipped task sync untouched.
5. **The shipped laws** — TC-401 (zero `markup=True` package-wide), TC-411 (the select sits
   outside the pinned grid, the declared deviation), KEYBAR (m in the more layer), README
   table, the kanban help bullets (ASCII minus after QA4-2).

## Folds at this gate (the standing authorization, P4's minors)

| Finding | Fold |
|---|---|
| UX4-1 / ARCH4-1 / SEC4-1 — the stale "bump_due seat" docstring + the "single-task snapshots" undo header/docstring | reworded (comment-only; behavior untouched) |
| QA4-2 — the only U+2212 `−` glyph in views.py | ASCII `+/-` |
| ARCH4-2 — `DATE_LINKS_DEFAULT` duplicates the engine's default | a leash comment in modals.py naming `CASCADE_DEFAULT_MODE` |
| QA4-1 / SEC4-2 — D-634's atomicity unpinned | **TC-636** (a spy pins `save_atomic` on the apply AND the undo's restore) |
| ARCH4-5/6, GAP-1/2 — `m` after an editor save + the refusal after an intervening action unpinned | **TC-637** |
| SEC4-4 — the select's display-default unpinned | **TC-638** |
| QA4-4 — the architect's probe file residue | confirmed deleted before close (the ledger reconciles at 2509 + 3) |

## Carried (BACKLOG at close)

DS-5 (the tested `models.restore` vs the app's hand-rolled loops) · ARCH4-3 (`Plan.conflicts`
consumed by nobody) · ARCH4-4/SEC4-6 (`bump_due` without a production caller; its today-base
re-implemented in `plan_move`) · SEC4-3 (the C-5 gate's vanished-task arm unreachable through
the UI by construction) · GAP-3 (toast rungs below 80 unpinned, degrade by design).

## The environment incident (declared, twice-learned)

Three of four lenses first ran with `NO_COLOR` present-but-empty (exported, not unset) — Textual
forced greyscale and 10 colour-census tests reddened. With `NO_COLOR` truly unset (`env -u
NO_COLOR` in Git Bash) they pass. The runbook's prescription is exact: **unset**, not empty.

## The operator's visual verdict

`evidence/veredicto-b2b.html` — the seven close captures inlined (the bump toast at 118 and
80, the `m` cycle, the project editor's row, the kanban before) and five questions:
PV-612 (the toast), PV-613 (`m`'s re-apply semantics), PV-614 (the 80-column form), PV-615
(the select's placement — the D-627 re-siting), UXV-6 (the rule's visibility before batch C).
The D-627 re-siting and the select-outside-the-grid both ride on the operator's eyes.

## Evidence

| Artifact | Where |
|---|---|
| the close suite | `evidence/inc003-gate.txt` + this station's final run (below) |
| the captures | `evidence/captures/close-*.svg/.txt` (7 surfaces) |
| the verdict sheet | `evidence/veredicto-b2b.html` |
| the second review (DeepSeek Flash) | `evidence/inc001-002-deepseek-review.md` |
| the P4 pins | TC-636/637/638 in `tests/test_cascade_app.py` |

## Signed-balance test ledger

`post = base − deleted + added` → `2512 = 2486 − 0 + 26` ✓ reconciles (23 engine/app nodes + 3 P4 pins).

## Human review ledger

human:Javier — the commission and the split by authorization; **the visual verdict pending
(the sheet above)**; the code machine-reviewed only.
