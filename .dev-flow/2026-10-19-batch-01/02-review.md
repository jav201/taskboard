# Review — taskboard — Batch 2026-10-19-batch-01

> **Artifact language:** canonical English scaffold. Generate in the batch's development language (`state.json` `language`).
> Phase 2 artifact. Reviewers (in parallel): `architect` ∥ `qa-reviewer` ∥ `security-reviewer` by trigger family C (always in `full`).

> **Owed in.** `core` ✓ · `full` ✓

> **Field guide:** `templates/guides/review-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

## ✅ Verdict (read first)

- **Gate:** `approve` — iteration 1 `iterate-to-refine` (architect and qa-reviewer: requirement-defect majors, no blocker) → LED-2026-10-19-batch-01.2; iteration 2 `approve` (architect, qa-reviewer) with two minors folded at once → LED-2026-10-19-batch-01.3; ux-reviewer and security-reviewer `approve with conditions` in iteration 1, every condition carried into the contract (LED .2)
- **Out-of-scope findings:** 3 named and routed below — UX-8 (`shift+arrow` not passed by some terminals) → §6.3 risk; A-10 (archived projects keep their rank) → §6.3 risk; the D8 deviation (`?` help unchanged) → `BACKLOG.md` for the operator
- **Findings:** iteration 1: 0 blocker · 14 major · 28 minor; iteration 2: 0 blocker · 1 major (A-15, the module map's team_sync row — fixed) · 4 minor (fixed)
- **shall/should check:** ✓ clean
- **Two-layer (blockers):** ✓ every story has an `AT` · output reqs name deliverable+observation · both trace chains complete · ATs are genuinely black-box
- **Census (change-first):** done — best-effort + gate-confirmed
- **Security:** ⚠ 7 findings (S-1..S-7: 0 high, 2 medium, 5 low) — every condition carried into the contract (LED .2)
- **Evidence checklists (architect / qa / security):** ✓ all complete (below; ux-reviewer too)

> If gate = `approve` and every line is ✓, the Detail below is reference. Any blocker/⚠ → read the matching part.

---

## Detail (reference)

Reviewers: `architect`, `qa-reviewer`, `ux-reviewer` (D1 fired), `security-reviewer` (C1, C4, C5, C8 fired) — each spawned as a generic agent with its `agents/<role>.md` role, read-only, in parallel, 2026-10-19; each reviewed the ARQ amendment (architect), the requirements (P2) and the design proposal (PDR) in one pass (declared in `PLAN.md` §Key decisions). The qa-reviewer probed the round's renderer over its own board and traced every AT's keys; the architect probed the `-k` selectors and the census; the ux-reviewer measured the hint wordings; the security-reviewer probed `escape` and the load rule's types. None edited a file.

### Findings
| ID | Reviewer | Severity | Area / Req | What | Recommendation | Status |
|----|----------|----------|------------|------|----------------|--------|
| A-1 | architect | minor | ARCHITECTURE §5 | the re-open condition "state the renderer cannot take as an argument" not literally met | restate: `PresentAll`'s shape, a two-kind cursor | fixed — module map |
| A-2 | architect | minor | ARCHITECTURE §2 | `modals` "no persistence" vs the picker's save; `keymap` "every binding of the modals" | the precedent; an interface row | fixed — module map |
| A-3 | architect | minor | ARCHITECTURE §3 | TC-2103 reads the round's C captures | list them | fixed — module map |
| A-4 | architect | minor | ARCHITECTURE §5 | the D8 decline is the operator's call | open decision | fixed — module map; `BACKLOG.md` at the close |
| A-5 | architect | major | ledger | canon supersessions incomplete (HLR-1803 ×2, LLR-1803.1, LLR-1803.3, HLR-1602.1, LLR-1903.1) | name them | fixed — LED .2 |
| A-6 | architect | major | P-5 | AT-1803 pins the two-view wrap | law-driven set | fixed — LED .2 |
| A-7 | architect | major | LLR-2104.1, LLR-2106.1 | the census's exempt key pins `_paint` | keep `update(self._frame_text())`; no new exemption | fixed — LED .2 |
| A-8 | architect | minor | Executed verification | `-k 2102` catches parametrize ids | `-k "TC_210N or AT_210N"` | fixed — LED .2 |
| A-9 | architect | minor | HLR-2104 | entering/leaving view 3 on a hidden project | specify | fixed — LED .2 |
| A-10 | architect | minor | HLR-2102 | archived projects keep an old rank | record | declared — §6.3 |
| A-11 | architect | major | PDR cut | 003 would ship view 3 with the views-1/2 `space`/`a` acting in it; `PRESENT_VIEWS[self._view]` IndexError | inert keys, or re-cut | fixed — re-cut: 003 `views` only, 004 the screen |
| A-12 | architect | minor | PDR cut | `u` advertised before bound | bind with the hint | fixed — re-cut |
| A-13 | architect | minor | PDR §6 | view-3 hint widths | — | superseded by UX-1's fix |
| A-14 | architect | minor | design | `present_hidden_rows` in `views` | acceptable (convention) | noted |
| QA-1 | qa-reviewer | major | TC-2103 | the milestone carve-out hides rows the round already draws as the fix does | drop it | fixed — LED .2 |
| QA-2 | qa-reviewer | major | HLR-2002 | the split view's 80-column hint no longer names `next`/`show all` | supersede HLR-2002 in part; flag | fixed — LED .2; the close |
| QA-3 | qa-reviewer | major | LLR-2104.1 | the view-3 tail under-specified | one count | fixed — LED .2 |
| QA-4 | qa-reviewer | major | TC-2104 | the formula copies the code's rule; AT-1904, TC-1904 overflow missing | literal tables | fixed — LED .2 |
| QA-5 | qa-reviewer | minor | ATs | key sequences unspelled | spell them | fixed — LED .2 (traced in iteration 2) |
| QA-6 | qa-reviewer | minor | AT-2103 | rail strings inexact | exact strings | fixed — LED .2, LED .3 |
| QA-7 | qa-reviewer | minor | HLR-2101 | `◆✓` and off-window arms unreachable; chip check not discriminating | reachable arms; named glyphs | fixed — LED .2 |
| QA-8 | qa-reviewer | minor | ATs | preconditions (frozen date, baselines, picker source) | state them | fixed — LED .2 |
| QA-9 | qa-reviewer | minor | §2.5 | the fixture's field before the field exists | `extra` at 001 | fixed — LED .3 |
| QA-10 | qa-reviewer | minor | AT-2102 | RED file vs increment | `red-004.txt` | fixed — LED .2 |
| QA-11 | qa-reviewer | minor | view-3 hint | terse at 118 | route to ux | fixed — UX-1 |
| QA-12 | qa-reviewer | minor | TC-2103 | sweep size | bound the cursors | fixed — LED .2 |
| QA-13 | qa-reviewer | major | TC-2103 | no ranked board: the order mutant survives | a reverse-ranked board | fixed — LED .2 |
| QA-14 | qa-reviewer | minor | TC-2104 | the export mutation assigned to a test that cannot see it | AT-2104 | fixed — LED .2 |
| QA-15 | qa-reviewer | minor | PDR | ATs' base RED shows absence only | each AT's §5 mutation in `mutate.py` | open — PDR condition PC-1, owed by increments 003/004 |
| UX-1 | ux-reviewer | major | view-3 hint | the tail costs every label at 118 | one count; shorter middle wording | fixed — LED .2 |
| UX-2 | ux-reviewer | major | LLR-2105.1 | rail `space` moved the cursor | toggle in place | fixed — LED .2 |
| UX-3 | ux-reviewer | major | `a` in view 3 | wide unannounced reach | a notice | fixed — LED .2 |
| UX-4 | ux-reviewer | minor | `←/→` | new meaning in view 3 | the AT reads `▶` vs `›` | fixed — AT-2104/2105 read the rail's lead |
| UX-5 | ux-reviewer | minor | keys | inert keys unstated | state them | fixed — LED .2 |
| UX-6 | ux-reviewer | minor | HLR-2104 | hidden project at entry | first drawn row | fixed — LED .2 |
| UX-7 | ux-reviewer | minor | picker | `u` should close; a title | both | fixed — LED .2 |
| UX-8 | ux-reviewer | minor | `shift+↑/↓` | some terminals drop it | fallback or risk | declared — §6.3 |
| UX-9 | ux-reviewer | minor | `space` | timeline hides only | D5 consequence | declared — §6.3 |
| S-1 | security-reviewer | n/a | §6.3 | C1/C4/C5 false positives | confirmed | closed |
| S-2 | security-reviewer | medium | C8 | the census cannot see view 3's `views` sites | `escape(fit())`; payload arms; mutant | fixed — LED .2 (HLR-2103, LLR-2103.1, TC-2103) |
| S-3 | security-reviewer | medium | load rule | bool-as-int, mixed-type sort | the exact rule; the type table | fixed — LED .2 |
| S-4 | security-reviewer | low | team_sync | a team pull could curate this board's presentation | strip the keys | fixed — LED .2 (LLR-2102.1, increment 002) |
| S-5 | security-reviewer | low | picker | an EXEMPT row added to pass | none added | fixed — LED .2 (LLR-2106.1) |
| S-6 | security-reviewer | low | export path | fixed slug | — | closed |
| S-7 | security-reviewer | low | — | (S-2's census reason text) | name `render_present_all` in the exempt reason | open — increment 004 updates the reason text, the key unchanged |

### Iteration 2 (2026-10-19) — the amended contract (LED .2)

Reviewers: architect, qa-reviewer (the same agents, resumed), read-only. Every iteration-1 requirement defect was confirmed resolved; the qa-reviewer traced every AT's keys against the round's board.

| ID | Reviewer | Severity | Area / Req | What | Recommendation | Status |
|----|----------|----------|------------|------|----------------|--------|
| A-15 | architect | major | ARCHITECTURE §4 | the project-record row still says a pull keeps the keys | restate | fixed — module map |
| A-16 | architect | minor | PDR header | `team_sync` missing from "Modules touched" | add | fixed — design proposal |
| QA2-1 | qa-reviewer | minor | AT-2103 | the rail rows have two leading cells | exact strings | fixed — LED .3 |
| QA2-2 | qa-reviewer | minor | §2.5 | QA-9 | `extra` at 001 | fixed — LED .3 |

**Gate:** `approve`

### shall / should check
> Any modal `should` / `debería` inside an HLR/LLR statement is a writing error → blocker.

Clean: `shall` only in the HLR and LLR statements; no `should`, `may` or `will` in any (architect, qa-reviewer).

### Two-layer acceptance review (blockers)
> (a) every story has a black-box `AT`; (b) every output-producing requirement names its observable deliverable + observation method; (c) BOTH traceability chains complete (behavioral US→AT→outcome + functional US→HLR→LLR→TC); (d) each `AT` is genuinely black-box — drives the surface, asserts the outcome, references NO internal symbol.

| Story / Req | (a) AT present | (b) deliverable+method named | (c) both chains | (d) black-box pure | Status |
|-------------|----------------|------------------------------|-----------------|--------------------|--------|
| US-2101 / HLR-2101 | yes (AT-2101) | yes (`#present-frame`) | yes (→HLR-2101→LLR-2101.1→TC-2101) | yes (keys `R`, `2`; the frame) | ✓ |
| US-2102 / HLR-2103, HLR-2104 | yes (AT-2103, AT-2104) | yes (`#present-frame`, `#present-hint`, `reports/*-all.svg`) | yes (→LLR-2103.1, LLR-2104.1→TC-2103, TC-2104) | yes | ✓ |
| US-2103 / HLR-2102, HLR-2105 | yes (AT-2102, AT-2105) | yes (`board.json`, the frame, the notice) | yes (→LLR-2102.1, LLR-2105.1→TC-2102, TC-2105) | yes | ✓ |
| US-2104 / HLR-2106 | yes (AT-2106) | yes (`#picker-rows`, `board.json`, the frame) | yes (→LLR-2106.1→TC-2106) | yes | ✓ |

### Supersession census (change-first)
> Planned new/moved/edited files checked against EVERY guard family (behavioral-placeholder · structural/placement · AST-composition · frozen-module). State reservations; the increment gate is the completeness guarantee, not this census.

Planned files: `taskboard/views.py`, `taskboard/models.py`, `taskboard/team_sync.py`, `taskboard/app.py`, `taskboard/modals.py` (edited); `tests/present_portfolio_board.py`, `tests/test_present_milestone.py`, `tests/test_present_all.py` (new); `tests/test_present_narrow.py`, `tests/test_present_polish.py`, `tests/test_present_views_app.py`, `tests/test_present_hide.py` (law-driven: TC-1904 and its overflow arm, AT-1904, TC-1808, TC-2002, AT-2002, TC-1604, AT-1602, AT-1803); `tests/test_markup_census.py` (the exempt key's reason text only); `docs/ARCHITECTURE.md`, `README.md`, `.dev-flow/BACKLOG.md`. Reverse grep over `tests/` (B1, PLAN §Triggers). Behavioural placeholders: none planned. Structural: the new test files under `tests/`, the fixture copied, never imported from `prototypes/`. AST composition: the markup census walks `app.py` and `modals.py` — `_paint`'s key kept, the picker fed by `Text` only. Frozen modules: none; the round's folder is frozen evidence and is not edited. Reservation: the round's `app_capture.py` subclasses `PresentScreen` and will not reproduce its captures after 004 (declared, PDR §6).

### Security review summary
`security-reviewer` (C1, C4, C5 by the scan's words; C8 judged): approve with conditions, 0 high. S-1 confirms C1/C4/C5 as false positives (the fold state; the synthetic project name). The conditions: every view-3 board-file string through `escape(fit(...))`; the four markup payloads in a name and a title with a mutant; the census exempt key unchanged and no new exemption; the picker of `Text` pieces; the exact load rule and its type table; the team pull stripping the two keys. All carried into LED .2; each re-checked at its increment's gate.

### Evidence checklists (full) — architect · qa-reviewer · security-reviewer

**architect (iteration 1 and 2):** ✓ constraints (§2.4) · ✓ alternatives (PDR §6) · ✓ risks — completed in iteration 2 (A-6, A-7, A-11 folded) · n/a cost/latency · ✓ diagram (PDR §3) · ✓ two-layer traceability.

**qa-reviewer (iteration 1 and 2, mode plan):** ✓ Given/When/Then · ✓ explicit expected (after QA-5, QA-6) · ✓ edge cases (after QA-7) · ✓ regression list (after QA-4) · ✓ exit criteria (§5.2) · ✓ no PII · ✓ Layer B through the shipped surface · ✓ every AT's keys traced.

**security-reviewer:** ✓ each finding what/where/why · ✓ severities · ✓ no secrets · ✓ verdict explicit, no HIGH · ✓ no new external tool; the team-sync radius covered (S-4).

**ux-reviewer:** ✓ context of use (§2.3) · UX-1..UX-9 · expert inspection `performed` (documents, the round's code; the C captures not opened) · evaluation with users `not performed` (one-person team; the operator's verdict on the round is the only user evidence).
