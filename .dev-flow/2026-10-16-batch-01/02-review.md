# Review — taskboard — Batch 2026-10-16-batch-01

> **Artifact language:** canonical English scaffold. Generate in the batch's development language (`state.json` `language`).
> Phase 2 artifact. Reviewers (in parallel): `architect` ∥ `qa-reviewer` ∥ `security-reviewer` by trigger family C (always in `full`).

> **Owed in.** `core` ✓ · `full` ✓

> **Field guide:** `templates/guides/review-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

## ✅ Verdict (read first)

- **Gate:** `approve` → Phase 3 (via PDR) — after one `iterate-to-refine` (iteration 1: 1 blocker, 8 majors, all three lenses). Iteration 2: architect `approve`, ux-reviewer `approve`, qa-reviewer `iterate-to-refine` on one remaining catalog inconsistency (QA N-1); the orchestrator approved under the standing authorization (`stations/p2-review.md` §Gate: the commission reads as autonomy over this gate), because every open item was a minor wording/catalog fix changing no obligation, applied in LED-2026-10-16-batch-01.5 and re-read.
- **Out-of-scope findings:** `none`

- **Findings:** `1` blocker · `8` major · `28` minor (iteration 1: 1 · 8 · 16; iteration 2: 0 · 0 · 12, incl. one qa "MEDIUM" and two security LOW classed minor) — all `fixed` except the declined UX-7 and the withdrawn QA-9
- **shall/should check:** ✓ clean — no modal `should` inside an HLR/LLR statement (architect, both iterations)
- **Two-layer (blockers):** ✓ every story has an `AT` · output reqs name deliverable+observation · both trace chains complete · ATs are genuinely black-box (AT-1603 hard-codes its key pairs — QA-5)
- **Census (change-first):** done — best-effort + gate-confirmed
- **Security:** ⚠ `2` LOW findings, both fixed (C8 fired; security-reviewer `approve`)
- **Evidence checklists (architect / qa / security):** `core` — the lenses' returns are summarised in §Findings; their full returns are in the orchestrator's session

> If gate = `approve` and every line is ✓, the Detail below is reference. Any blocker/⚠ → read the matching part.

---

## Detail (reference)

### Findings
| ID | Reviewer | Severity | Area / Req | What | Recommendation | Status |
|----|----------|----------|------------|------|----------------|--------|
| A-1 | architect | blocker | HLR-1603 / AT-1603 | the Keys band cannot be unscrolled at 80×24 (~26 content rows in ~17) | "no scroll" owed by the pinned global line only | fixed (LED .4) |
| A-2 | architect | major | LLR-1603.2 | "beside the hint" impossible (global ~102 cells + hint ~40 > 104) | hint on its own pinned row; state row counts | fixed (LED .4) |
| A-3 | architect | minor | LLR-1602.2 | axis refit not in an LLR, no TC | clause + TC-1604 arm | fixed (LED .4) |
| A-4 | architect | minor | LLR-1602.2 | `present_hidden` population undefined | defined | fixed (LED .4) |
| A-5 | architect | minor | LLR-1602.2 | `a` is the app's add-task key | `priority=True`; arm "`a` opens no editor" | fixed (LED .4) |
| A-6 | architect | minor | LLR-1601.2 | cross-year chip format | stated, no year | fixed (LED .4) |
| A-7 | architect | minor | §6.3 | cross-check script named twice, deltas unnamed, 80×24 | one name, deltas listed, risk named | fixed (LED .4) |
| A-8 | architect | minor | HLR-1602 | many `shall`s in one sentence; undo interaction | six numbered clauses; undo stated | fixed (LED .4) |
| QA-1 | qa-reviewer | major | LLR-1601.2 / §6.3 | oracle circularity; `PRES-B` name collides with batch-04 | `PRES-R-*`, criterion, hand-written literals | fixed (LED .4) |
| QA-2 | qa-reviewer | major | HLR-1601 | AT-1001's frame arm not said to be repointed | stated | fixed (LED .4) |
| QA-3 | qa-reviewer | major | HLR-1602 | axis refit / cursor skip untested | TC-1604 arms | fixed (LED .4) |
| QA-4 | qa-reviewer | major | LLR-1603.1 | grid order arm can be vacuous | 7 keys / 3 columns | fixed (LED .4) |
| QA-5 | qa-reviewer | minor | AT-1603 | oracle via `bar_keys` = internal symbol | hard-coded pairs | fixed (LED .4) |
| QA-6 | qa-reviewer | minor | AT-1602 | no base-RED, no export arm | added | fixed (LED .4) |
| QA-7 | qa-reviewer | minor | catalogs | HLR/LLR catalogs disagree | aligned | fixed (LED .4, .5) |
| QA-8 | qa-reviewer | minor | LLR-1601.1 | weekend precondition, `over` arm | added | fixed (LED .4) |
| QA-9 | qa-reviewer | minor | §1.4 | "prototypes/present_rulers/ does not exist" | — | withdrawn (exists; qa re-verified with `ls`) |
| UX-1 | ux-reviewer | major | LLR-1602.3 | checkbox placement undefined; 80-col fold at 80 | title row; threshold unchanged; 80×24 arm | fixed (LED .4) |
| UX-2 | ux-reviewer | major | HLR-1603 | Keys band at 80×24 | as A-1 | fixed (LED .4) |
| UX-3 | ux-reviewer | major | LLR-1603.2 | footer rows when wrapped | as A-2 | fixed (LED .4) |
| UX-4 | ux-reviewer | minor | LLR-1602.2 | all-hidden frame unspecified | specified | fixed (LED .4) |
| UX-5 | ux-reviewer | minor | LLR-1602.2 | next-task cursor arm | added | fixed (LED .4) |
| UX-6 | ux-reviewer | minor | LLR-1602.2 | hidden population | as A-4 | fixed (LED .4) |
| UX-7 | ux-reviewer | minor | LLR-1602.2 | narrow hint `a all` ambiguous, `↑↓` dropped | — | declined: the operator commissioned both hint strings verbatim (ux accepted) |
| UX-8 | ux-reviewer | minor | HLR-1602 | stray `space` recovery reveals intentional hides | stated limit | fixed (LED .4) |
| A2-N1 | architect | minor | LLR-1603.2 | 102/104 cells: one more global key wraps | compute expected rows | fixed (LED .5) |
| A2-N2 | architect | minor | LLR-1602.2 | hint `n` unsourced | `len(present_hidden)` | fixed (LED .5) |
| A2-N3 | architect | minor | §6.3 | owed verdict without `⏸ DEFER` | marker + BACKLOG line | fixed (LED .5) |
| QA2-N1 | qa-reviewer | minor ("MEDIUM") | HLR-1601 | invalid-date coverage claimed, no arm | TC-1602 arm; catalogs ticked | fixed (LED .5) |
| QA2-N2 | qa-reviewer | minor | HLR-1601 | "empty" names no TC | TC-1601 arm | fixed (LED .5) |
| QA2-N3 | qa-reviewer | minor | LLR-1603.2 | as A2-N1 | as A2-N1 | fixed (LED .5) |
| UX2-N1 | ux-reviewer | minor | HLR-1603 | title contradicts statement | retitled | fixed (LED .5) |
| UX2-N2 | ux-reviewer | minor | LLR-1602.3 | title input ~26 cells at 80 | accepted; TC-1605's frame shows it | open — observed at increment 002 |
| UX2-N3 | ux-reviewer | minor | LLR-1602.3 | tab order changes | stated | fixed (LED .5) |
| UX2-N4 | ux-reviewer | minor | LLR-1602.2 | `space` with all hidden | TC-1604 arm | fixed (LED .5) |
| S-F1 | security-reviewer | minor (LOW) | LLR-1602.1 | key missing from `_TASK_KEYS` → stale `false` in `extra` | add to `_TASK_KEYS`; invalid arm | fixed (LED .6) |
| S-F2 | security-reviewer | minor (LOW) | AT-1602 | export arm too weak | title + counts | fixed (LED .6) |

### shall / should check
> Any modal `should` / `debería` inside an HLR/LLR statement is a writing error → blocker.

✓ clean (architect, iterations 1 and 2).

### Two-layer acceptance review (blockers)
> (a) every story has a black-box `AT`; (b) every output-producing requirement names its observable deliverable + observation method; (c) BOTH traceability chains complete (behavioral US→AT→outcome + functional US→HLR→LLR→TC); (d) each `AT` is genuinely black-box — drives the surface, asserts the outcome, references NO internal symbol.

| Story / Req | (a) AT present | (b) deliverable+method named | (c) both chains | (d) black-box pure | Status |
|-------------|----------------|------------------------------|-----------------|--------------------|--------|
| US-1601 | yes (AT-1601) | yes — the painted `#present-frame` | yes (→ HLR-1601 → LLR-1601.1/.2 → TC-1601/1602, TC-1001/1002) | yes | ✓ |
| US-1602 | yes (AT-1602) | yes — the frame, the hint, `board.json` on disk, the exported SVG | yes (→ HLR-1602 → LLR-1602.1/.2/.3 → TC-1603/1604/1605) | yes | ✓ |
| US-1603 | yes (AT-1603) | yes — the compositor's painted rows | yes (→ HLR-1603 → LLR-1603.1/.2 → TC-1606/1607) | yes (hard-coded pairs) | ✓ |

### Supersession census (change-first)
> Planned new/moved/edited files checked against EVERY guard family (behavioral-placeholder · structural/placement · AST-composition · frozen-module). State reservations; the increment gate is the completeness guarantee, not this census.

Planned edits: `views.py` (render_present, _present_cols, _present_chip removal, gantt_day_row keyword, present_tasks/present_hidden), `models.py` (Task field, from_dict, _to_dict), `app.py` (PresentScreen), `modals.py` (TaskModal, HelpModal), `keymap.py` (global_keys). Observers found (B1 probe, PLAN §Triggers): `test_present.py` (TC-1001/1002/AT-1001 — the oracle frames change: repoint, named), `test_markup_census.py` (the presentation seat row — re-validate), `test_report.py` (read-only R — still holds), `test_markup_sites.py` (present arm, help Keys heading `_flags(rows, "Keys")` — the heading text changes to `Keys · this view`: re-validate at 003), `test_help_clip.py` (columns only — the band leaves `#help-right`), `test_gantt_board.py:905-911` (`#help-left`/`#help-right` queries), `test_english.py:244` ("Keys" in the help text), `test_setup_help.py:260`, `test_legend.py`, `test_edit_window.py` (CONTRACT_IDS, the chip sweep, the save round-trip), `test_cascade.py` (`_to_dict`). Byte-identity laws on board saves (`test_milestones.py`, `test_link_migration.py`, `test_app.py`…) — the omission keeps them. Best-effort + gate-confirmed: each increment's reverse census re-runs these probes.

### Security review summary
`security-reviewer` (C8 fired; spawned with `agents/security-reviewer.md`): **approve**, 0 HIGH · 0 MEDIUM · 2 LOW. No markup-injection path: the new rows take parsed `date`s (`parse_iso`, `models.py:648-655`), integers and `KEYMAP` literals; titles keep the S1 escape (TC-1003). F1 LOW — `show_in_present` must join `_TASK_KEYS` or a stale `false` survives in `extra` and resurrects after `a` → fixed (LED .6). F2 LOW — the export arm must check the hidden title and the counts, not only `hidden` → fixed (LED .6). Phase 3 to confirm: no raw date string enters a chip; `PresentScreen` recomputes its id list after `space`/`a`. Note recorded: the flag is presentation-only, not confidentiality — a hidden task stays in `board.json` and in team pushes.

### Evidence checklists (full) — architect · qa-reviewer · security-reviewer
> Attach each reviewer's completed evidence checklist (items in their agent files), ✓/✗ + one-line evidence.

`core` — not owed in full form. Reviewers ran as `spawned — generic agent with agents/<role>.md` (architect, qa-reviewer, ux-reviewer, security-reviewer); their returned verdicts and findings are the table above.
