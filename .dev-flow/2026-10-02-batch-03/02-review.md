# Review — taskboard — Batch 2026-10-02-batch-03

> Phase 2, two-lens cross-review (core) plus the security lens (family C fired). Lenses:
> `qa-reviewer`, `ux-reviewer` and `security-reviewer`, each spawned as an independent named
> sub-agent of this runtime and told to follow the pinned bundle's `agents/<role>.md`,
> read-only, over `01-requirements.md` as drafted at P1. Their reports are their final messages
> (this runtime keeps them out of the tree); each is summarised below.

## ✅ Verdict (read first)

- **Gate (iteration 1):** `iterate-to-refine` → Phase 1: qa-reviewer `FAIL` (2 blockers — Q-1 the tag rule contradicts the frame, Q-2 the phantom `+` key; 7 major), ux-reviewer `PASS-WITH-NOTES` (0 blocker, 4 major: UX-1 silent fold, UX-2 cursor on an undrawn done task, UX-3 row 2 below the fold, UX-4 no 80×24 terminal), security-reviewer `PASS-WITH-NOTES` (0 HIGH, 2 MEDIUM, 3 LOW). Every finding folded into the live contract (ledger `.9`–`.13`, §6.5) or routed below. Iteration 2: see §Iteration 2.
- **Out-of-scope findings:** 4 named and routed (S-4 existing L1 → BACKLOG stays; UX-11 header/left-right re-window → P4 walkthrough + BACKLOG; UX-12 done tasks past the cap → declared, D-305; the gantt's filter/nav height gap → BACKLOG, D-312).
- **Findings:** 2 blocker · 13 major · 22 minor/low
- **shall/should check:** ✓ clean (qa: 0 `should`/`must`/`will`/`may` in statements)
- **Two-layer (blockers):** ✓ every story has an AT through `App.run_test`; both chains complete (qa). Surface-reachability gaps (`g`, `s`, `v`, `!`, `]` into Done) folded into AT-302/303/308.
- **Census (change-first):** done — best-effort + gate-confirmed; qa's per-node census (below) is carried into each increment's reverse census.
- **Security:** ⚠ 5 findings, 0 HIGH (S-1, S-2 folded as hostile arms; S-3 an increment review check; S-4 existing L1; S-5 fixed — `evidence/__pycache__` deleted, `redact.py` case-insensitive with the 8.3 and temp forms).
- **Evidence checklists:** each lens's checklist summarised under its findings.

## Detail

### Findings

| ID | Reviewer | Severity | Area / Req | What | Recommendation | Status |
|----|----------|----------|------------|------|----------------|--------|
| Q-1 | qa | blocker | HLR-305, LLR-301.2 | "every high card names its project" vs the shed rule: the frame tags 8 of 9 at 118, 2 of 9 at 80 | tag when it fits, or never shed | fixed — "when the row has room", threshold = the frame's tagged set (LED .11) |
| Q-2 | qa | blocker | HLR-305 surface | `+` is `due_bump(1)`; the priority cycle is `!` | name `!` | fixed |
| Q-3 | qa | major | HLR-301 thresholds | the metric credits header text and 1–2 char hits (~0.46 noise > 0.2 margin) | count drawn titles only; re-measure | fixed — first-word rule over body rows; P-1 7.3/1.0, P-6 11.8/6.2; floors 11.0/12/5.5 (LED .13) |
| Q-4 | qa | major | chrome | header, WIP row, window markers, empty line unstated | an LLR keeping them | fixed — LLR-301.3 (LED .13) |
| Q-5 | qa | major | LLR-301.1 vs HLR-305 | nav over a window contradicts "exactly the drawn cards" | state the exception; 8-phase arm | fixed — nav = the unwindowed drawn set; ⊆ arms |
| Q-6 | qa | major | HLR-304 | `]` into Done below 100 leaves the cursor on an undrawn card | an LLR + AT | fixed — HLR-310, LLR-310.1, AT-308 (with UX-2) |
| Q-7 | qa | major | AT-302/303 | `g`, `s`, `v`, focus never driven off default | drive them | fixed — AT-302 `g` horizon + `v`; AT-303 `g` priority, `s`, `!` |
| Q-8 | qa | major | LLR-301.1 (C-31) | the oracle board has no archived / Inbox task: 30 arms duplicate; no capped arm | guarded board; capped arm | fixed |
| Q-9 | qa | major | §6.2/§6.3 | HLR-007's `✓ N` and the "show every task" law are superseded too | name them | fixed — D-313 |
| Q-10 | qa | minor | LLR-306.1 | `┈` before `+N more ↓`? | state it | fixed — none; executed table |
| Q-11 | qa | minor | counts under the cap | which highs `K high ↑` counts | truth table | fixed — LLR-306.1 table, D-311 |
| Q-12 | qa | minor | HLR-308 | `band` is in the base help | a phrase absent on base | fixed — `band rule` |
| Q-13 | qa | minor | HLR-307 | 0 accent and reverse are true on base | label as pins | fixed |
| Q-14 | qa | minor | LLR-303.1 | `· project` + `due` missing a space | fix | fixed |
| Q-15 | qa | minor | AT-302 | 5 rules not all visible at 30 rows | AT counts what is drawn | fixed |
| Q-16 | qa | minor | rail × group mode | undefined | truth table | fixed — LLR-304.1 |
| Q-17 | qa | minor | LLR-301.2 | no wide-char title; no hostile tag | add | fixed |
| Q-18 | qa | minor | the `Beta release` literal | derived by hand | cite the frame | fixed |
| Q-19 | qa | minor | §6.3 row 2 below the fold | no requirement | write one | fixed — HLR-309 (by construction; a band taller than the panel declared) |
| Q-20 | qa | minor | ledger | stale seed line above entries | leave it (append-only) | noted for close |
| UX-1 | ux | major (operator Q) | D-302 | scrolling with no cue hides Ops & Security; the frame folds whole bands and names them | windowing + fold row | fixed — HLR-309, D-302 (PV-1 is now only the absent detail line) |
| UX-2 | ux | major | D-305 | `]` into a count rail strands the cursor | toast and/or relocation | fixed — HLR-310 (both) |
| UX-3 | ux | major | §6.3 | row 2 below the fold; band rule above | criterion | fixed — HLR-309 threshold |
| UX-4 | ux | major | ATs | no terminal 80×24 | add | fixed — AT-301/307/308 arms, captures |
| UX-5 | ux | minor | HLR-305 | the tag sheds at 80 | declare | fixed (with Q-1) |
| UX-6 | ux | minor | counts | shown vs all | the drawn cards | fixed — D-311 |
| UX-7 | ux | minor | PV list | D-308, D-309 missing | PV-6, PV-7 | fixed |
| UX-8 | ux | minor | PV-5 | first-word collision | two words | fixed — shortest distinguishing run |
| UX-9 | ux | minor | HLR-306 | `]` into a capped column | P4 walkthrough | carried → P4 |
| UX-10 | ux | minor | filter | no-match, normals-only | P4 walkthrough | carried → P4 |
| UX-11 | ux | notice | out of scope | header scroll (solved by windowing); left/right lands at the top | BACKLOG | carried → P4 + BACKLOG |
| UX-12 | ux | notice | HLR-304 | done tasks past the cap not reopenable from the kanban | declare | fixed — D-305 names ≥ 100 cells and the agenda |
| S-1 | security | MEDIUM | LLR-304.1, LLR-305.1 | rail titles and the tag lack an "escaped" clause and a hostile arm | add | fixed |
| S-2 | security | MEDIUM | LLR-301.2 | hostile set misses lone `[`, backslashes, a closing tag on row 2 | add | fixed |
| S-3 | security | LOW | new code | `vis(_strip(...))` over escaped user text leans | review check | carried → each increment's code review |
| S-4 | security | LOW | existing L1 | control chars in names reach the terminal | cite L1 | fixed — §6.4 cites it; BACKLOG item stays |
| S-5 | security | LOW | evidence | `__pycache__` with the home path; case-sensitive redaction | delete; harden | fixed |

### shall / should check
✓ clean (qa).

### Two-layer acceptance review (blockers)

| Story / Req | (a) AT present | (b) deliverable+method named | (c) both chains | (d) black-box pure | Status |
|-------------|----------------|------------------------------|-----------------|--------------------|--------|
| US-301 | AT-301, AT-305 | yes (painted panel) | yes | yes | ✓ |
| US-302 | AT-302, AT-307, AT-308 | yes | yes | yes | ✓ |
| US-303 | AT-303, AT-304 | yes | yes | yes | ✓ (after Q-2) |

### Supersession census (change-first)
qa's best-effort per-node census (carried into increment 001's reverse census; the increment gate is the completeness guarantee). **Will break:** `test_kanban_priority.py::test_band_is_drawn_and_nav_walks_the_draw_order`, `::test_help_example_shows_a_badge_and_says_the_band_is_grouped_only`; `test_app.py::test_kanban_groups_by_project`, `::test_kanban_group_cycles_headers_and_membership`, `::test_kanban_collapse_toggles_the_terminal_phase_and_restores`, `::test_kanban_collapsed_column_shape_and_nav_exclusion`, `::test_kanban_windows_phases_when_they_dont_fit`, `::test_kanban_parity_painted_text_oracle`. **At risk:** `test_kanban_priority.py` cursor/raise/badge nodes; `test_app.py` every-task, blocked, width-exact, custom phases, right/up nav, sort/group parity walks, WIP header ×2, aging token, focus cycle ×2, tiny size, offscreen selection, undo, search; `test_gantt.py::test_filtered_kanban_fits_the_panel_too`; `test_vertical_fill.py`; `test_span_economy.py`; `test_prism_laws.py` (rule crossing, closure); `test_cells.py::test_the_project_name_is_hostile_too`; `test_emoji_picker.py` width; `test_palette_ration.py` priority glyph; `test_legend.py`. **Pins expected green:** `test_colour_budget.py` TC-119/AT-106, `test_colour_budget_app.py` AT-203, `test_english.py` TC-206, the `kanban_order` seat nodes, the `card_cell` unit nodes (lanes keeps `card_cell`).

### Security review summary
security-reviewer PASS-WITH-NOTES, 0 HIGH: escaping each piece after the split is the right order (splitting an escaped string left `[/link]` literal and the link open, probed on rich 15.0.0); S-1..S-5 above. Checklist 5/5 ✓.

### Evidence checklists (full) — qa-reviewer · ux-reviewer · security-reviewer
- **qa-reviewer:** ✓ no `should`; n/a Given/When/Then (EARS + thresholds); ✓ expected values (except Q-6/Q-7, folded); ✗→fixed edge-case sets (Q-8, Q-17); ✗→fixed regression checklist (census above); ✓ exit criteria; ✓ no PII; ✓ mode declared; ✓ results `planned`; ✓ Layer B; ✗→fixed surface reachability (Q-6, Q-7); ✓ no unfilled template.
- **ux-reviewer:** ✓ context of use; ✗→fixed environment (UX-4); ✓ criteria observable (✗→fixed UX-1..3); ✓ real mechanism; ✓ painted result; ✓ verdicts mapped (✗→fixed PV-1); ✓ states (✗→carried UX-10); ✓ three evaluation acts; ✗→fixed PV list (UX-7).
- **security-reviewer:** ✓ what/where/why/recommendation; ✓ severities; ✓ no secret values; ✓ explicit verdict; ✓ no new tool or integration.

## Iteration 2

- **qa-reviewer iteration 2:** `FAIL` — N-1 **blocker** (Backlog holds 4 highs, 11 rows: the half-body cap capped the approved 80×24 frame), N-2 major (nav claims vs windowing), N-3 major (§1.2 still put windowing out; D-310 said `views.py` only), N-4..N-7 minor. All iteration-1 findings re-read discharged except Q-5 (half, = N-2).
- **ux-reviewer iteration 2:** `FAIL` — UX-15 **blocker** (the fold row clipped the `▼` side at 80, hiding Ops & Security again), UX-14 major (a `down` into a visible band re-flowed the board), UX-13 major / operator question (relocation to the top of the column), UX-16..UX-18 minor (UX-16: the PV list was updated after the reviewer's read).
- **Folds:** the cap → `R = max(5, 2·(h − 3) // 3)` (LED .16, D-303) keeps the approved frames uncapped; the window starts at the earliest band that keeps the selection drawn, the fold row keeps every folded side's count (LED .14, D-314); after `]` the cursor takes the neighbour (LED .15 — the gantt's neighbour precedent, so UX-13 is answered, not left open); nav claims scoped to h 0; §1.2, D-310 re-judged (family A stays not fired: one package); tag rule cites the shed order, asserted exactly; §5 updated; word-wise tags.
- **Discharge re-read** (qa-reviewer, a fresh spawn, read-only): `DISCHARGED` — all 12 ids ✓, the cap arithmetic re-derived (R, K, the h ≤ 19 boundary, both oracle frames uncapped); three minor defects the folds introduced (F-1 the R floor lost its arm → h 11 added; F-2 the fold-row statement vs the one-sided oracle → "each side that folds"; F-3 the `]` oracle had two answers → `ta6` named) folded at once; an observation for ux: `up` into a drawn band can re-flow (only `down` was asked) → P4 walkthrough.
- **Gate:** `approve` → Phase 3 under the standing authorization: 0 blocker open, 0 HIGH; the soft iteration cap (3) not reached (P2 iteration 2, P1 iteration 3 of refining folded within it). Increment plan re-cut once (C-21, after iteration 1); unchanged by iteration 2 (no AT added or split).
