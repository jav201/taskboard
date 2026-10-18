# Review — taskboard — Batch 2026-10-18-batch-03

> **Artifact language:** canonical English scaffold. Generate in the batch's development language (`state.json` `language`).
> Phase 2 artifact. Reviewers (in parallel): `architect` ∥ `qa-reviewer` ∥ `security-reviewer` by trigger family C (always in `full`).

> **Owed in.** `core` ✓ · `full` ✓

> **Field guide:** `templates/guides/review-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

## ✅ Verdict (read first)

- **Gate:** `approve` — iteration 1 `iterate-to-refine` (6 requirement-defect majors, no blocker) → LED-2026-10-18-batch-03.2, .3; iteration 2 `approve` (architect, qa-reviewer, ux-reviewer) with 1 minor (A2-1 = QA2-1), owed by increment 003
- **Out-of-scope findings:** 2 named and routed below — UX-1 (the gantt note can show more than the split view) → `BACKLOG.md` for the operator; UX-2 (the hint's inactive view name at 3.25:1) → `BACKLOG.md`
- **Findings:** iteration 1: 0 blocker · 6 major · 11 minor; iteration 2: 0 blocker · 0 major · 1 minor
- **shall/should check:** ✓ clean
- **Two-layer (blockers):** ✓ every story has an `AT` · output reqs name deliverable+observation · both trace chains complete · ATs are genuinely black-box
- **Census (change-first):** done — best-effort + gate-confirmed
- **Security:** ✓ no findings — family C did not fire (the P1 scan: `flags: none`, `security_required: false`); no `security-reviewer` owed in `core`
- **Evidence checklists (architect / qa / ux):** ✓ all complete (below)

> If gate = `approve` and every line is ✓, the Detail below is reference. Any blocker/⚠ → read the matching part.

---

## Detail (reference)

Reviewers: `architect`, `qa-reviewer`, `ux-reviewer` (D1 fired) — each spawned with its `agents/<role>.md` role, read-only, in parallel, 2026-10-18. The architect re-ran the premises with an exec'd port of `views.py` (13,440 frames) and the qa-reviewer probed every literal width; neither edited a file.

### Findings
| ID | Reviewer | Severity | Area / Req | What | Recommendation | Status |
|----|----------|----------|------------|------|----------------|--------|
| A-1 | architect | major | LED .1, HLR-2002 | canon supersessions missing: HLR-1802 ("at most three rows", "one dim word"), HLR-1904 ("four wordings"), LLR-1001.1 ("capped at 3 lines", its PRES-V3 notes oracle) | name them; restate HLR-2002's "every other rule" | fixed — LED .3 |
| A-2 | architect | minor | LED .1 | the cut marks' `dim` attributed to LLR-1802.1; it is LLR-1801.2's | correct | fixed — LED .3 |
| A-3 | architect | major | HLR-2002, HLR-2003, LLR-2002.1 | the Executed verification commands select nothing (pytest keeps the last `-k` and filters every file: 0 of 48, 0 of 18) | one command per `-k` | fixed — LED .3 |
| A-4 | architect | major | LLR-2001.1 | "the frames' plain text equals `base_ref`'s" is false once increment 003 lands | unchanged by this LLR | fixed — LED .3 |
| A-5 | architect | major | LLR-2003.1 | the note count cannot hold where the header and briefs alone overflow | restrict to `height ≥ L + 3` or state it pre-finish | fixed — LED .2 (`height ≥ L + min(n, 3)`), LED .3 |
| A-6 | architect | minor | `render_present`'s docstring | "expanded to 3 rows", "byte-faithful to PRES-V3" go stale | update with increment 003 | open — owed by increment 003 (PLAN roadmap) |
| QA-1 | qa-reviewer | major | HLR-2001, LLR-2001.1 | at 36 `header()` paints the whole title bold `bright`: the view word cannot be `reached` there | "where the header keeps its tones" | fixed — LED .2 |
| QA-2 | qa-reviewer | major | LLR-2003.1 | heights 5 and 12 cut the frame before the note: 0 rows, not 3 | state the overflow case | fixed — LED .2 |
| QA-3 | qa-reviewer | minor | HLR-2003, LLR-2003.1 | the room-equals-note and one-row-more boundaries are claimed, not reached | a seen-set or explicit heights | fixed — LED .2 (explicit heights `L + n`, `L + n - 1`, `L + 1` and a seen-set) |
| QA-4 | qa-reviewer | minor | HLR-2001 | `no project to present` kept `dim` but never checked | a case or drop the clause | fixed — LED .2 (TC-2001's no-project arm) |
| QA-5 | qa-reviewer | minor | TC-1604 | at 80 the 0-hidden hint is the middle wording, with 2 hidden the short one: two expected strings | name it in the census | open — owed by increment 002 |
| QA-6 | qa-reviewer | minor | TC-1808, TC-1904 | five TC-1808 cells change; its docstring; TC-1904 gains a middle tier | rewrite law-driven, keep monotonicity | open — owed by increment 002 |
| QA-7 | qa-reviewer | minor | TC-1807 | moves to the V4 frames: 9 / 11 note rows, the cut check at 80 only, the line-break checks kept | rewrite law-driven | open — owed by increment 003 |
| QA-8 | qa-reviewer | minor | §2.7 P-2 | `capture.py:63` → `:70` | correct | fixed — LED .2 |
| UX-1 | ux-reviewer | minor | HLR-2003 | the gantt view now shows more of the cursor's note than the split view (80×25: 9 rows vs 3) | declare | declared — §6.3; `BACKLOG.md` at the close |
| UX-2 | ux-reviewer | minor | §1.2 | the hint's inactive view name stays `#5b6675` (3.25:1) | name it out of scope | fixed — LED .2 (§1.2) |
| UX-3 | ux-reviewer | minor | AT-2001 | colour read from `Text` spans, a structural read | the P4 walkthrough names the capture comparison for the visual claim | open — owed by P4 |

### Iteration 2 (2026-10-18) — the amended contract (LED .2, LED .3)

Reviewers: architect, qa-reviewer, ux-reviewer (the same agents, resumed), read-only. Every iteration-1 requirement defect was confirmed resolved; A-6, QA-5..QA-7 and UX-3 stay with their owners.

| ID | Reviewer | Severity | Area / Req | What | Recommendation | Status |
|----|----------|----------|------------|------|----------------|--------|
| A2-1 / QA2-1 | architect, qa-reviewer | minor | TC-2003 | the one-row-longer boundary (`height - L = n - 1`, `… +2 lines`) exists only for a note of 4+ rows | record it from such a note | open — owed by increment 003 (the sweep adds those heights only for `n > 3`) |

**Gate:** `approve`

### shall / should check
> Any modal `should` / `debería` inside an HLR/LLR statement is a writing error → blocker.

Clean: `shall` only in the HLR and LLR statements; no `should`, `may` or `will` in any (architect, qa-reviewer).

### Two-layer acceptance review (blockers)
> (a) every story has a black-box `AT`; (b) every output-producing requirement names its observable deliverable + observation method; (c) BOTH traceability chains complete (behavioral US→AT→outcome + functional US→HLR→LLR→TC); (d) each `AT` is genuinely black-box — drives the surface, asserts the outcome, references NO internal symbol.

| Story / Req | (a) AT present | (b) deliverable+method named | (c) both chains | (d) black-box pure | Status |
|-------------|----------------|------------------------------|-----------------|--------------------|--------|
| US-2001 / HLR-2001 | yes (AT-2001) | yes (`#present-frame`'s `Text` spans) | yes (→HLR-2001→LLR-2001.1→TC-2001) | yes (keys `R`, `→`, `2`; the painted frame) | ✓ |
| US-2002 / HLR-2002 | yes (AT-2002) | yes (`#present-hint`) | yes (→HLR-2002→LLR-2002.1→TC-2002) | yes | ✓ |
| US-2003 / HLR-2003 | yes (AT-2003) | yes (`#present-frame`, against the round's frame file) | yes (→HLR-2003→LLR-2003.1→TC-2003) | yes | ✓ |

### Supersession census (change-first)
> Planned new/moved/edited files checked against EVERY guard family (behavioral-placeholder · structural/placement · AST-composition · frozen-module). State reservations; the increment gate is the completeness guarantee, not this census.

Planned files: `taskboard/views.py`, `taskboard/app.py` (edited); `tests/test_present_polish.py` (new); `tests/test_present_views.py` (TC-1807), `tests/test_present_views_app.py` (TC-1808), `tests/test_present_narrow.py` (TC-1904), `tests/test_present_hide.py` (TC-1604) (law-driven updates); `docs/ARCHITECTURE.md`; evidence under `.dev-flow/2026-10-18-batch-03/`. Reverse grep over `tests/` (B1, PLAN §Triggers): **must change** — the four nodes above (QA-5..QA-7 name their cells); **must stay green unchanged** — TC-1001/1002 (the PRES-V3 gantt frames: their cursor's note is 2 rows, whole under the cap and under the fill), the split-view PRES-V3 nodes (plain text unchanged by tones), `test_markup_census.py`, `test_present_room.py`, `test_present_rulers.py`, `test_tick_label.py`, `test_row_cost.py`. No frozen module; no placement guard reaches `tests/test_present_polish.py`. Reservation: the increment gate confirms by the full suite.

### Security review summary
Not run — trigger family C did not fire in this `core` batch (PLAN §Triggers C1–C8; the P1 scan `flags: none`).

### Evidence checklists (full) — architect · qa-reviewer · ux-reviewer
> Attach each reviewer's completed evidence checklist (items in their agent files), ✓/✗ + one-line evidence.

**architect (iteration 1):** ✓ premises re-run (P-1, P-3; P-2/P-4 by an exec'd port over 13,440 frames, 0 differ in text and spans) · ✓ `HINT_A` verbatim · ✓ the PRES-V4 frames · ✗ canon supersessions (A-1) · ✗ verification commands (A-3) · ✗ TC-2001 text clause (A-4) · ✗ the overflow count (A-5) · ✓ the ARCHITECTURE amendment.

**qa-reviewer (iteration 1, mode plan):** ✓ P-3's 24 widths · ✓ AT-2002's cell counts · ✓ P-1 · ✓ the PRES-V4 80×24 frame · ✓ oracles outside the code under test · ✗ the view word at 36 (QA-1) · ✗ the overflow count (QA-2) · ✗ boundaries reached (QA-3) · ✗ `no project to present` unchecked (QA-4) · ✓ the law-driven updates safe if QA-5..QA-7 are honoured.

**ux-reviewer (iteration 1):** ✓ the three looks carried faithfully (the four `_QUIET` sites, `HINT_A` verbatim with its gap, the fill formula; hint80-A-gantt-hidden's fallback) · ✓ no effect below 36 · ✓ hidden count and paging · ✓ context of use (§2.3) · UX-1, UX-2 declared · expert inspection `performed` (documents and the round's captures) · evaluation with users `not performed` (one-person team) · contrast on a real projector `not performed`.
