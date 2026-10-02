# Review — taskboard — Batch 2026-10-02-batch-02

> Phase 2, two-lens cross-review (core) plus the security lens (family C fired). Lenses:
> `qa-reviewer`, `ux-reviewer` and `security-reviewer`, each spawned as an independent named
> sub-agent of this runtime with its role file (`agents/<role>.md`), read-only, over
> `01-requirements.md` as drafted at P1 iteration 1. Their reports are their final messages
> (this runtime keeps them out of the tree); each is summarised below.

## ✅ Verdict (read first)

- **Gate:** `approve` → Phase 3 at iteration 2 (qa and ux PASS-WITH-NOTES, 0 blocker, 0 HIGH). Iteration 1 was `iterate-to-refine` → P1: qa-reviewer `PASS-WITH-NOTES` (0 blocker, 13 major incl. 2 carried to P3), ux-reviewer `FAIL` (1 blocker UX-1, 4 major), security-reviewer `PASS-WITH-NOTES` (0 HIGH, 1 MEDIUM, 4 LOW). Every finding folded into the live contract (ledger `.11`–`.14`, §6.5) or routed below. Iteration 2 re-dispatched over the amended items — see §Iteration 2.
- **Out-of-scope findings:** 3 named and routed (S-5 pre-existing `notify` sites → BACKLOG; UX-9 answers carry no notes → close record; Q-14/Q-15 → P3 increment 004 / every increment's census).
- **Findings:** 1 blocker · 17 major · 13 minor/low
- **shall/should check:** ✓ clean (qa)
- **Two-layer (blockers):** ✓ every story has an AT through `App.run_test`; both chains complete (qa). Viability defects (AT-208, AT-210, AT-201, AT-204) folded.
- **Census (change-first):** done — best-effort + gate-confirmed; qa's per-symbol grep recorded in Q-15 and carried; each increment re-runs it from its touched-symbol list.
- **Security:** ⚠ 5 findings, 0 HIGH (S-2 MEDIUM fixed: the evidence transcript redacted; S-1 folded; S-3 deleted; S-4 fixture path; S-5 BACKLOG).
- **Evidence checklists:** each lens's checklist summarised under its findings.

## Detail

### Findings

| ID | Reviewer | Severity | Area / Req | What | Recommendation | Status |
|----|----------|----------|------------|------|----------------|--------|
| UX-1 | ux | blocker | HLR-201, LLR-201.2, D-207/208 | Setup rows are built from `str()` of styled Text: 0 style spans on the body rows; cursor, chips, checks painted plain | bring the style loss in scope or drop the arms | fixed — LLR-201.3, P-13, LED .11 |
| UX-2 | ux | major | LLR-203.1, D-209 | `DUE_METER` does not exist; `HEAT` unread; `due_meter` today is accent | name the real seat or drop | fixed — clause deleted, P-14, LED .12 |
| Q-1 | qa | major | HLR-203 | same as UX-2 (C-36) | — | fixed — LED .12 |
| Q-2 | qa | major | HLR-203 | `+8d` is `dim`, not `mut` | correct the threshold | fixed — P-15 |
| UX-3 | ux | major (operator question) | D-204, HLR-208 | the frame the operator complained about stays folded under weight alone | due-today tie-break, or say so plainly | fixed — tie-break adopted, D-204, LED .14 |
| Q-5 | qa | major | HLR-208 | same as UX-3 | — | fixed — AT on the oracle board at 80×24 |
| UX-4 | ux | major (operator question) | D-203 | a session-long visited list erodes UXV-3; previous-group stickiness measures the same | bound to the previous group | fixed — HLR-207, D-203, LED .13 |
| Q-6 | qa | major | HLR-207 | "the highlight does not jump" — 2 residual upward moves | mark the residual for the operator | fixed — D-203, D-216 |
| UX-5 | ux | major (operator question) | D-205, D-208, D-211, key bar | four visual changes the operator never saw rendered | captures + provisional, quieter options | folded — chips bold/mut (not reverse), ribbon cities `mut`/`hd`, weekend hex kept (commission requires 256-colour survival) and flagged provisional; key-bar hues per commission; captures at every gate (D-216) |
| Q-3 | qa | major | HLR-210, AT-210 | the right-clip branch cannot be reached on the oracle board | synthetic board | fixed — `k = 7` board at panel 60×20 |
| Q-4 | qa | major | AT-208 | the entry selection unfolds A or B first | third group C holds the selection; name the size | fixed — terminal 80×14 |
| Q-7 | qa | major | HLR-201 (C-31) | presentation guard `≥ 12` too weak; tuples are literals in `app.py` | `== 16`, derived by AST | fixed |
| Q-8 | qa | major | AT-201 (C-10a) | only `5`+`tab` driven; no team fixture | tab through every presentation, team dir | fixed |
| Q-10 | qa | major | HLR-204 (C-31) | hand-listed lexicon; false-positive words; filter never cycled | guarded lexicon; cycle `f` | fixed |
| Q-14 | qa | major (carried) | HLR-205 | `test_TC_106_a_tall_group_pages_and_keeps_its_count` pins pages of 20 | name it in increment 004's census | carried → increment 004 |
| Q-9 | qa | minor | AT-201 | detector must be positional | one column per view for rule glyphs; mutation arm | fixed |
| Q-11 | qa | minor | LLR-204.1 | fit law only on the gantt | every view | fixed |
| Q-12 | qa | minor | HLR-202 | "0 group hues" contradicts `mut`; plain strings need a frozen base | hexes ⊆ {bright, mut, dim}; freeze | fixed |
| Q-13 | qa | minor | HLR-205/207/209/203/206 | no middle-page fixture; `tm2`→`tm6`; dead reverse-video clause; no packet guard; `✓n` semantics | add / correct | fixed |
| Q-15 | qa | minor (carried) | PLAN B1 | census list inaccurate | re-run per increment | carried → every increment; PLAN B1 corrected |
| Q-16 | qa | minor | D-213 | "al borde" read as under the page | record the reading | fixed — D-213 |
| UX-6 | ux | minor | HLR-206 | toast wraps at 80×24, stale after `u`; other finish paths silent | P4; declare scope | folded — §1.2, D-214, P4 |
| UX-7 | ux | minor | HLR-205 | page flip moves the highlight up | P4 | P4 walkthrough item |
| UX-8 | ux | minor | D-209 | amber's third meaning on cards (`==` badge) | P4 | P4 walkthrough item |
| UX-9 | ux | minor | answers | all twelve are the recommended option, empty notes | note in the close | D-216, close record |
| UX-10 | ux | minor | §2.3 | colour depth not stated | one line | fixed |
| S-1 | security | LOW | LLR-206.1 | `markup=False` closes C-17; escaping as well shows `\[` | raw title + `markup=False`; hostile payloads | fixed — LLR-206.1, HLR-206 |
| S-2 | security | MEDIUM | §6.4 | `evidence/base-suite.txt` held a home path | redact; sweep each gate | fixed — redacted (the shell's heredoc had collapsed the pattern's backslashes); home-path sweep at each gate |
| S-3 | security | LOW | hygiene | a `__pycache__` under `evidence/` embeds the path (git-ignored) | delete, run with `-B` | fixed — deleted |
| S-4 | security | LOW | HLR-204 | a failing Setup note prints the OSError, which may hold the home path | fixture path outside the home | fixed — fixtures use `D:/team` (absent) |
| S-5 | security | LOW (pre-existing) | `app.py` `notify` sites with prompt text, markup on | BACKLOG | → BACKLOG at close |

### shall / should check
✓ clean — every Statement uses `shall`; no `should` (qa).

### Two-layer acceptance review (blockers)

| Story | (a) AT | (b) deliverable + method | (c) both chains | (d) black-box | Status |
|---|---|---|---|---|---|
| US-201 | AT-201..203 | painted strips | yes | yes | ✓ |
| US-202 | AT-204 | painted modal / views | yes | yes | ✓ |
| US-203 | AT-205, AT-206 | painted rows, notification | yes | yes | ✓ |
| US-204 | AT-207, AT-208 | painted fold marks | yes | yes | ✓ |
| US-205 | AT-209, AT-210 | painted background, echo | yes | yes | ✓ |

### Supersession census (change-first)
qa's per-symbol grep (Q-15): `▬` → `test_motion`, `test_gantt`, `test_gantt_board`, `test_app`; `modal-title` → `test_edit_window`, `test_emoji_picker`; accent → `test_team_views:62-63`, `test_keymap:295`; Spanish → `test_setup_help:118,119,257,262`, `test_flow_view:77,98`; `reldue_token` → `test_colour_budget:116`, `test_cells:290`; `update_clock` → `test_palette_ration:313`; folds → `test_gantt_board` TC-103, TC-106 (Q-14); `status_glyph` → `test_archive`. Best-effort + gate-confirmed: each increment's packet carries the measured census.

### Security review summary
PASS-WITH-NOTES, 0 HIGH. Textual 8.2.8 `App.notify(markup=True)` by default; `markup=False` exists and renders `Content(message)`. The weekend wrap goes only around constant glyph cells (14 hostile titles simulated through `render_view`'s parse: literal, background on the weekend cells only).

### Evidence checklists
- qa-reviewer (mode `plan`): 8 ✓, 3 ✗ at iteration 1 (edge-case fixtures, AT viability, surface reachability) — the three ✗ are Q-3, Q-4, Q-8, Q-10, Q-13, all folded.
- ux-reviewer: context of use ✓ (colour depth added); observability ✗ (UX-1, UX-2 — folded); walkthrough planned for P4; expert inspection performed; user evaluation not performed (D-216 routes the visual decisions to the operator).
- security-reviewer: 5/5 ✓.

## Iteration 2

qa-reviewer and ux-reviewer were resumed over the amended items (security's findings were all
folded or routed; it reviews the toast again at increment 005). Both re-ran the new numbers.

- **qa-reviewer: PASS-WITH-NOTES**, 0 blocker. Confirmed by execution: AT-208's panel 80×12 (body 9, 5 rows left, base unfolds A → RED); the 50-task middle page `tb19..tb37`, `▲ 19 above / ▼ 12 below`; the `k = 7` board at 60×20 (`field_w` 32 = 224 days; a due at +230 lands past the window; base clamps `⟧` → RED); the oracle 80×24 entry frame (Website, Ops, Data `▾`; Mobile, API `▸`); the HLR-203 guards non-vacuous. Checklist: edge cases, Layer B and reachability rows flip to ✓.
- **ux-reviewer: PASS-WITH-NOTES**, UX-1..UX-10 closed or declared. Confirmed by execution: 2 upward moves at 80×24 and 1 at full size over the walk; Mobile stays `▾` at `ta1`. P4 walkthrough list: items 1–13 (recorded in `04-validation.md` when it is written).

| ID | Reviewer | Severity | What | Status |
|----|----------|----------|------|--------|
| N-1 | qa | minor | `None` meant both "no previous" and "the Inbox" | fixed — `INBOX_GROUP` constant, Inbox arm (LED .15) |
| N-2 | qa | minor | "a group visited earlier gains nothing" had no fixture | fixed — synthetic four-group TC, `ta1` arm |
| N-3 | qa | minor | Setup plain text needs frozen base strings | fixed — LLR-201.3 |
| UX-11 | ux | minor (operator question) | "urgent fold last" false mid-walk under skip-and-continue | fixed — HLR-208 reworded "offered rows first"; D-217 for the operator (LED .15) |
| UX-12 | ux | minor | LLR-201.2's negative control and boundary lines had slipped under LLR-201.3 | fixed |
| (notice) | ux | — | `today` and `+1d..+7d` share amber on kanban (D-209); the provisional visual decisions ship before the operator's verdict on captures | declared — repeated in the close |
| (pin) | qa | — | the `k = 7` fixture must reach past +224 days | fixed — +230 pinned in HLR-210 |

**Gate (iteration 2): `approve` → Phase 3**, under the standing authorization: 0 blocker, 0 HIGH, every
new note folded. The AT set changed after the plan was cut, so the increment plan was re-derived
(C-21): every AT-201..210 keeps an owning increment (`PLAN.md` §Roadmap).
