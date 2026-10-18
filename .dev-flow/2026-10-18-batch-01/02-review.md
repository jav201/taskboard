# Review — taskboard — Batch 2026-10-18-batch-01

> **Artifact language:** canonical English scaffold. Generate in the batch's development language (`state.json` `language`).
> Phase 2 artifact. Reviewers (in parallel): `architect` ∥ `qa-reviewer` ∥ `security-reviewer` by trigger family C (always in `full`).

> **Owed in.** `core` ✓ · `full` ✓

> **Field guide:** `templates/guides/review-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

## ✅ Verdict (read first)

- **Gate:** `approve` → PDR — after one `iterate-to-refine` (iteration 1: 1 blocker, 4 majors across architect, qa-reviewer and ux-reviewer; amended in LED-2026-10-18-batch-01.2). Iteration 2: architect `approve`, qa-reviewer `approve`, ux-reviewer `approve`; their minors folded in LED-2026-10-18-batch-01.3 and re-read.
- **Out-of-scope findings:** 2 named and routed below (S-3, the cell-width wrap → `BACKLOG.md`; UX-2, snapping a page to an item's start → `BACKLOG.md`)

- **Findings:** iteration 1: 1 blocker · 4 major · 21 minor (incl. 3 security LOW); iteration 2: 0 blocker · 0 major · 4 minor · 2 notice
- **shall/should check:** ✓ clean
- **Two-layer (blockers):** ✓ every story has an `AT` · output reqs name deliverable+observation · both trace chains complete · ATs drive keys and assert the painted frame and the files on disk (after LED .2: QA-2 literal export paths; QA-8 the `view_mode` read declared a seam)
- **Census (change-first):** done — best-effort + gate-confirmed
- **Security:** ✓ `security-reviewer` `approve` — 0 HIGH · 0 MEDIUM · 3 LOW (C8 fired)
- **Evidence checklists (architect / qa / ux / security):** ✓ all complete (below)

> If gate = `approve` and every line is ✓, the Detail below is reference. Any blocker/⚠ → read the matching part.

---

## Detail (reference)

Reviewers: `architect`, `qa-reviewer`, `ux-reviewer` (D1 fired), `security-reviewer` (C8 fired) — each `spawned — generic agent with agents/<role>.md`, read-only, in parallel, 2026-10-18. A draft implementation was on the working tree; the lenses used it to verify claims, and the reviewed artifact was the contract.

### Findings
| ID | Reviewer | Severity | Area / Req | What | Recommendation | Status |
|----|----------|----------|------------|------|----------------|--------|
| UX-1 | ux-reviewer | blocker | LLR-1801.3, HLR-1803 | a fixed 5-row scroll step over a 4-row cursor window skips note rows no offset paints (item `2.` never on screen at 80×24) | a page = the window's rows; a TC arm that paging shows every row | fixed — LED .2 (page-based tiling; TC-1806 paging-coverage arm, M14) |
| A-1 | architect | major | LLR-1801.3 | traced to HLR-1801, whose statement says nothing of scrolling; HLR-1803 did not cover the area scroll | retrace to HLR-1803 and state both cases there | fixed — LED .2 |
| QA-1 | qa-reviewer | major | HLR-1801 / LLR-1801.2 | below a row per note the share gives the cursor 0 rows and the overflow is silent | the cursor keeps a row; declare the overflow | fixed — LED .2 (`max(min(1, ns[cur]), …)`, `↓ N more lines`), M15 |
| QA-3 | qa-reviewer | major | AT-1803 | "a different frame" after the last `pgup` compared with the top, not the last page | compare with the last page | fixed — LED .2 |
| QA-4 | qa-reviewer | major | TC-1804 | the guard's edge (exactly a row per note, and below) not exercised | add 80×19, 80×18, 118×15, 80×11 | fixed — LED .2 |
| QA-2 | qa-reviewer | minor (blocker in the draft test, owned by increment 002) | AT-1803 | the export arm asked `present_paths` where the file is | literal paths; export both views | fixed — LED .2 |
| A-2 | architect | minor | LLR-1803.1 | "both reset on a view change" contradicts `2` → `view(1)` | only `_scroll` resets | fixed — LED .2 |
| A-3 | architect | minor | LLR-1801.1 | the wrapper is HLR-1802's mechanism too | trace to both | fixed — LED .2 |
| A-4 | architect | minor | LLR-1803.2 | `w` undefined | the screen width | fixed — LED .2 |
| A-5 | architect | minor | LLR-1801.2 | `PRESENT_VIEWS` and `floor_n` not in a statement | state them | fixed — LED .2 |
| A-6 | architect | minor | HLR-1801 | the all-hidden case unspecified | nothing under the rule | fixed — LED .2 (M17) |
| A-7 | architect | minor | LLR-1801.2/.3 | "blocks alone" ambiguous | one wording | fixed — LED .2 |
| A-8 | architect | minor | TC-1805 / §1.2 | `[link=…]` claimed, not asserted; README/backlog unowned | align; declare documentation deliverables | fixed — LED .2 |
| QA-5 | qa-reviewer | minor | TC-1804 | the cut check was frame-wide | per note, in its block | fixed — LED .2 |
| QA-6 | qa-reviewer | minor | TC-1802 | no row for the cursor on the no-notes task or below the floor | add two rows | fixed — LED .2 |
| QA-7 | qa-reviewer | minor | AT-1801 | the last cursor position never checked; the accent not asserted | check after each press | fixed — LED .2 |
| QA-8 | qa-reviewer | minor | AT-1801/1803 | the ATs read internal state | words from the fixture; `view_mode` declared a seam | fixed — LED .2 |
| QA-9 | qa-reviewer | minor | AT-1803 | only two key words checked in the SVG | all seven, both SVGs | fixed — LED .2 |
| QA-10 | qa-reviewer | minor | TC-1808 | the 99/100 boundary never rendered | add the widths | fixed — LED .2; this arm found a real overflow (107 cells in 98 at 100 columns): the long wording is now chosen by fit (N11) |
| QA-11 | qa-reviewer | minor | TC-1805 | an `or view == "gantt"` disjunct | drop it; assert `[link=…]` | fixed — LED .2 |
| UX-2 | ux-reviewer | minor | LLR-1801.3 | a page can start on an item's continuation row | snap to item starts | declared (§6.3) → `BACKLOG.md` |
| UX-3 | ux-reviewer | minor | LLR-1801.3 | in the area scroll the headings scroll away | pin or declare | declared (§6.3) |
| UX-4 | ux-reviewer | minor | LLR-1801.2 | ` … +N` has no unit and stacks on the clip's `…` | ` … +N lines`, no second `…` | fixed — LED .2 (D2 in `gen_frames.py`, M16) |
| UX-5 | ux-reviewer | minor | HLR-1801 | the all-hidden outcome unwritten | write it | fixed — LED .2 (with A-6) |
| UX-6 | ux-reviewer | minor | LLR-1803.2 | `shift+tab` on no screen; `pgdn` shown when nothing is cut | README names `⇧⇥`; declare | declared (§6.3); README in increment 002 |
| UX-7 | ux-reviewer | minor (notice) | HLR-1802 | dim words on a screen share unchecked | judge on the 118 PNGs | owned by P4 (the capture review) |
| S-1 | security-reviewer | minor (LOW) | `present_paths` | `view` enters the file name unvalidated | raise on an unknown view | declined (§6.3): every caller passes a `PRESENT_VIEWS` constant; internal callers are trusted |
| S-2 | security-reviewer | minor (LOW) | TC-1805 | the one-row cut, a paged note, a hostile cursor heading, `\` and `\[` unreached | add the cases | fixed — LED .2 (the second TC-1805 node) |
| S-3 | security-reviewer | minor (LOW) | `present_note_lines` | `textwrap` counts code points; wide glyphs wrap wide | cell-width wrap or declare | declared (§6.3) → `BACKLOG.md` |

### shall / should check
> Any modal `should` / `debería` inside an HLR/LLR statement is a writing error → blocker.

Clean: `shall` only in the HLR and LLR statements; no `should` in any (architect, qa-reviewer).

### Two-layer acceptance review (blockers)
> (a) every story has a black-box `AT`; (b) every output-producing requirement names its observable deliverable + observation method; (c) BOTH traceability chains are complete (behavioral US→AT→outcome + functional US→HLR→LLR→TC); (d) each `AT` is genuinely black-box — drives the surface, asserts the outcome, references NO internal symbol.

| Story / Req | (a) AT present | (b) deliverable+method named | (c) both chains | (d) black-box pure | Status |
|-------------|----------------|------------------------------|-----------------|--------------------|--------|
| US-1801 / HLR-1801 | yes (AT-1801) | yes (`#present-frame`, the PRES-V3 split frames) | yes (US-1801→AT-1801; →HLR-1801→LLR-1801.1, .2→TC-1801..1805) | yes after LED .2 (words from the fixture, QA-8) | ✓ |
| US-1802 / HLR-1802 | yes (AT-1802) | yes (`#present-frame`, the PRES-V3 gantt-notes frames) | yes (→HLR-1802→LLR-1802.1, LLR-1801.1→TC-1807, TC-1801, TC-1001/1002) | yes | ✓ |
| US-1803 / HLR-1803 | yes (AT-1803) | yes (`#present-frame`, `#present-hint`, `reports/*.svg` by literal path) | yes (→HLR-1803→LLR-1801.3, 1803.1..3→TC-1806, TC-1808..1810) | yes after LED .2 (QA-2; `view_mode` a declared seam — the board behind is not on screen) | ✓ |

### Supersession census (change-first)
> Planned new/moved/edited files checked against EVERY guard family (behavioral-placeholder · structural/placement · AST-composition · frozen-module). State reservations; the increment gate is the completeness guarantee, not this census.

Planned files: `taskboard/views.py`, `taskboard/app.py` (edited); `tests/test_present_views.py`, `tests/test_present_views_app.py`, `tests/present_notes_board.py` (new); `tests/test_present.py`, `tests/test_present_hide.py`, `tests/test_markup_census.py` (edited); `README.md`; the batch evidence. Reverse grep over `tests/` (B1, PLAN §Triggers): **must change** — `test_present.py` TC-1001/TC-1002/AT-1001 (PRES-R2 → PRES-V3-gantt: the header word, and at 80 the note wrap width `width − 6`), `test_present_hide.py` TC-1604's hint arm (the view switch opens the hint), `test_markup_census.py` TC-402's `PresentScreen._paint` exemption key (the call moved into `_frame_text`); **read and survive** — `test_present_room.py`, `test_present_rulers.py`, `test_tick_label.py` (the ruler, the chips, the tick label and the SVG writer, unchanged; their frames carry no header-word assertion), `test_markup_sites.py`, `test_report.py` (`R` opens `PresentScreen`, read-only); outside `tests/`: `prototypes/present_rulers/app_capture.py` and `present_views/views_proto.py` import the deleted note helpers (ARCHITECTURE §3, frozen evidence). Goldens (B3): no `tests/goldens`; the PRES-R / PRES-R2 frames stay untouched, the new PRES-V3 frames are new files. Pre-executed (C-39): the draft's targeted files run green (58 passed, qa-reviewer, iteration 2); the full suite is owed per increment. No frozen modules are declared in this repo. Reservations: best-effort; the increment gate confirms.

### Security review summary
`security-reviewer` (C8 fired; spawned with `agents/security-reviewer.md`): **approve**, 0 HIGH · 0 MEDIUM · 3 LOW. Every board-file string on a new row is escaped after clipping (`_present_note_markup`, the one-row cut, `_present_heading`, the gantt note rows); the rest of the markup is fixed text or computed numbers; control bytes are stripped at load (`models.strip_controls`); widths measured with `vis`; the export suffix is a `PRESENT_VIEWS` constant and the slug is the shipped one; the board is still written only by `space`/`a`. S-1 declined (internal callers), S-2 fixed, S-3 declared.

### Evidence checklists (full) — architect · qa-reviewer · ux-reviewer · security-reviewer
> Attach each reviewer's completed evidence checklist (items in their agent files), ✓/✗ + one-line evidence.

**architect (iteration 1):** ✓ constraints stated (§2.4) · ✓ alternatives (design proposal §6) · ✓ rationale tied to constraints · ✗ derivation — LLR-1801.3's parent (A-1) · ✓ premises P-1..P-8 re-run on `6ddea9f` · ✓ map consistency · ✓ two-layer (a)–(d).

**qa-reviewer (iteration 1, mode plan):** ✓ Given/When/Then · ✓ explicit expected · ✗ edge cases — the floor edge and the task count (QA-1, QA-4) · ✓ regression (§5.2 B1) · ✓ exit criteria · ✓ no PII · ✓ mode declared · ✓ results `planned` · ✗ layer B — QA-2, QA-3 · ✓ surface reachability · ✓ no unfilled template.

**ux-reviewer (iteration 1):** ✓ context of use (§2.3) · ✓ observable criteria · ✗ interaction — the scroll skipped rows (UX-1) · ✓ fidelity to the prototype at both sizes · ✗ evaluation with users — not performed (one-person team); expert inspection performed, renderer frames inspected, the key walkthrough `planned` at P4.

**security-reviewer:** ✓ escaping (S1) · ✓ control bytes and widths · ✓ export path · ✓ writes · ✓ secrets n/a · ✓ no new dependency.

### Iteration 2 (2026-10-18) — the amended contract (LED .2)

Reviewers: architect, qa-reviewer, ux-reviewer (the same agents, resumed), read-only. Every iteration-1 finding was confirmed resolved or declared.

| ID | Reviewer | Severity | Area / Req | What | Recommendation | Status |
|----|----------|----------|------------|------|----------------|--------|
| A2-1 | architect | minor | §1.2 | the README / backlog line not found | add it | already present — §1.2 carries it since LED .2 ("documentation deliverables of increment 002 and of the close, not requirements"); re-read |
| QA2-1 | qa-reviewer | minor | TC-1804 below-floor arm | the arm could not fail if the cursor's note dropped to 0 rows; the cursor's block could be windowed out | assert the cursor's block on screen | fixed — LED .3: the page-0 window keeps the cursor's block in view (`_present_window`), the arm asserts its note's first words, M18 |
| QA2-2 | qa-reviewer | minor | LLR-1801.2 | no arm asserts the page-0 edge mark as such | covered by QA2-1 | fixed — LED .3 |
| QA2-3 | qa-reviewer | minor | TC-1805 | an invalid escape in a string literal | `a\\[b]` | fixed — LED .3 |
| UX2-1 | ux-reviewer | notice | LLR-1801.3 | a 4-row cursor window pages 2 new rows a press | optional | declared — nothing is lost |
| UX2-2 | ux-reviewer | notice | LLR-1801.3 | the last page overlaps by one row | none | correct as written |

**Gate:** `approve`
