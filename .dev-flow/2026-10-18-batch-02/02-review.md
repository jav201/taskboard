# Review — taskboard — Batch 2026-10-18-batch-02

> **Artifact language:** canonical English scaffold. Generate in the batch's development language (`state.json` `language`).
> Phase 2 artifact. Reviewers (in parallel): `architect` ∥ `qa-reviewer` ∥ `security-reviewer` by trigger family C (always in `full`).

> **Owed in.** `core` ✓ · `full` ✓

> **Field guide:** `templates/guides/review-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

## ✅ Verdict (read first)

- **Gate:** `approve` — iteration 1 `iterate-to-refine` (9 requirement-defect majors, no blocker) → LED-2026-10-18-batch-02.2; iteration 2 `approve` (architect, qa-reviewer, ux-reviewer) with 7 minors → LED .3
- **Out-of-scope findings:** none — every finding is a requirement defect folded into the contract
- **Findings:** iteration 1: 0 blocker · 9 major · 18 minor; iteration 2: 0 blocker · 0 major · 7 minor
- **shall/should check:** ✓ clean
- **Two-layer (blockers):** ✓ every story has an `AT` · output reqs name deliverable+observation · both trace chains complete · after LED .2 no AT patches a product symbol (A-2)
- **Census (change-first):** done — best-effort + gate-confirmed
- **Security:** ✓ no findings — family C did not fire (the P1 scan's `truncate`/`escape` flags answered in `01-requirements.md` §6.3); no `security-reviewer` owed in `core`
- **Evidence checklists (architect / qa / ux):** ✓ all complete (below)

> If gate = `approve` and every line is ✓, the Detail below is reference. Any blocker/⚠ → read the matching part.

---

## Detail (reference)

Reviewers: `architect`, `qa-reviewer`, `ux-reviewer` (D1 fired) — each spawned with its `agents/<role>.md` role, read-only, in parallel, 2026-10-18. A probe of the design was on a scratch worktree of `base_ref`; the lenses read its diff to judge feasibility, and the reviewed artifact was the contract.

### Findings
| ID | Reviewer | Severity | Area / Req | What | Recommendation | Status |
|----|----------|----------|------------|------|----------------|--------|
| A-1 | architect | major | AT-1904 | the 25-column arm fails a correct build: `1 gantt 2 split esc` (19 cells) fits the 23-cell row, the fixture hides nothing | move below 21 or hide tasks | fixed — LED .2 (three hidden, 50/40/30/15 columns) |
| A-2 | architect | major | AT-1902 (b) | patches `models.grab_clipboard_text`, an internal product symbol, and duplicates TC-1902 | drop arm (b) | fixed — LED .2 |
| QA-1 | qa-reviewer | major | AT-1903 | `2` at 30 columns, then "the gantt frame returns" at 118 contradicts itself | compare with the frame kept before the narrowing; give heights | fixed — LED .2 |
| QA-2 | qa-reviewer | major | HLR-1902 | 5× contention became a SKIP, so a reader that disturbs the clipboard would pass as one | skip only on refusal; contention fails | fixed — LED .2 (+ the disturbing-reader arm) |
| UX-1 | ux-reviewer | major | HLR-1903 wording | `present needs 36+ columns` gives no action and its cut loses the number first | a ladder keeping the number and the action | fixed — LED .2 (`PRESENT_NARROW`, five rungs) |
| UX-2 | ux-reviewer | major | HLR-1903 tone | `dim` (~3.2:1) for the only content on screen | `mut` (~6.4:1) | fixed — LED .2 |
| UX-3 | ux-reviewer | major | HLR-1904 order | the cut drops the hidden count and `esc` first, keeps the view names | `esc` and the count survive longest; no names below 36 | fixed — LED .2 (`esc leave` + count below 36) |
| UX-4 | ux-reviewer | major | process | the narrow frame and hint ship without a prototype round | add them to the round or record the waiver | fixed — LED .2: they ship under the commission's FIX class (the commission names both items as FIX: «Make it degrade without crashing», «Give it an honest fallback»), and HLR-1905 shows them in the round for the operator's review |
| UX-5 | ux-reviewer | major | HLR-1903 `x` | below 36 `x` writes an SVG holding only the message | refuse with a notice | fixed — LED .2 (`Widen the terminal to 36+ columns to export`) |
| A-3 | architect | minor | §2.7 P-6, PLAN | 59/66 off by one; "below 60" | 58/65 | fixed — LED .2 |
| A-4 | architect | minor | §2.7 P-9 | `:6239` is not a dim literal | `:6240`, `:6241`, `:6273` | fixed — LED .2 |
| A-5 | architect | minor | HLR-1902 | "the last refusal" vs contention | align | fixed — LED .2 (contention now fails) |
| A-6 | architect | minor | HLR-1903 | "every key working" ambiguous below 36 | state what the keys do | fixed — LED .2 (no key but `esc` acts) |
| A-7 | architect | minor | §5.2 | no criterion for the HISTORICAL notes and the stale comments | two inspection lines | fixed — LED .2 |
| A-8 | architect | minor | LLR-1903.1 | "no row at width 0" vs `height` empty rows | every row empty | fixed — LED .2 |
| A-9 | architect | minor | PLAN | width domain "≥ 1" vs "≥ 0" | "≥ 0" | fixed — PLAN Objective, A3 row |
| A-10 | architect | minor | PLAN | "TC-1901..1905" | TC-1901..TC-1904 | fixed — PLAN |
| A-11 | architect | minor | HLR-1903 | `space` below 36 hides a task the presenter cannot see | ux to judge | fixed — LED .2, with UX-7 |
| QA-3 | qa-reviewer | minor | AT-1902 | the fake must answer `Get-Clipboard` and the restore; `_ps` is not named a seam | name `_ps`; record the commands | fixed — LED .2 |
| QA-4 | qa-reviewer | minor | TC-1901 | the prefix locator underspecified | the 12-cell name cell equals `fit(name, 12)`; 12/13-cell arm | fixed — LED .2 |
| QA-5 | qa-reviewer | minor | TC-1904 | recomputing the wordings is a tautology; 3 vs 6 hidden | the literal threshold table; 0/3/10 hidden | fixed — LED .2 (P-7 re-probed) |
| QA-6 | qa-reviewer | minor | AT-1905 | no recommendation token; PNGs not tied to SVGs; only one RED arm; `inspection` | `data-recommend`, a manifest, three RED arms, `test` | fixed — LED .2 |
| QA-7 | qa-reviewer | minor | AT-1905 | a permanent test over a throwaway folder | a retirement rule | fixed — LED .2 (they leave together) |
| QA-8 | qa-reviewer | minor | C-39 | AT-1901/1902/1905 REDs promised, not run | mark `planned`, gate on the files | fixed — LED .2 (§5.2) |
| QA-9 | qa-reviewer | minor | AT-1903 | `space` at 30 columns | ux to judge | fixed — LED .2, with UX-7 |
| UX-6 | ux-reviewer | minor | HLR-1904 | from ~58 to ~22 the keys vanish at once | a compact wording | fixed — LED .2 (`⇥ ←→ ␣ x esc`) |
| UX-7 | ux-reviewer | minor | HLR-1903 | `space`/`a` act with nothing to confirm them | say so, or no-ops | fixed — LED .2 (no-ops below 36) |
| UX-8 | ux-reviewer | minor | AT-1903/1904 | tone and bold claims not asserted | assert the spans | fixed — LED .2 (TC-1903 `mut` markup; AT-1904 the bold span) |
| UX-9 | ux-reviewer | minor | AT-1904 | no hidden-task scene, no split view | add them | fixed — LED .2 |

### shall / should check
> Any modal `should` / `debería` inside an HLR/LLR statement is a writing error → blocker.

Clean: `shall` only in the HLR and LLR statements; no `should`, `may` or `will` in any (architect).

### Two-layer acceptance review (blockers)
> (a) every story has a black-box `AT`; (b) every output-producing requirement names its observable deliverable + observation method; (c) BOTH traceability chains are complete (behavioral US→AT→outcome + functional US→HLR→LLR→TC); (d) each `AT` is genuinely black-box — drives the surface, asserts the outcome, references NO internal symbol.

| Story / Req | (a) AT present | (b) deliverable+method named | (c) both chains | (d) black-box pure | Status |
|-------------|----------------|------------------------------|-----------------|--------------------|--------|
| US-1901 / HLR-1901 | yes (AT-1901) | yes (`#board` in standup mode) | yes (→HLR-1901→LLR-1901.1→TC-1901) | yes (key `8`, painted rows) | ✓ |
| US-1901 / HLR-1902 | yes (AT-1902) | yes (the pytest outcome and reason) | yes (→HLR-1902→LLR-1902.1→TC-1902) | yes after LED .2 (only the machine, `_ps`, is faked — A-2) | ✓ |
| US-1902 / HLR-1903 | yes (AT-1903) | yes (`#present-frame`, the notification, `reports/`) | yes (→HLR-1903→LLR-1903.1→TC-1903) | yes (keys, `resize_terminal`) | ✓ |
| US-1902 / HLR-1904 | yes (AT-1904) | yes (`#present-hint`) | yes (→HLR-1904→LLR-1904.1→TC-1904) | yes | ✓ |
| US-1903 / HLR-1905 | yes (AT-1905) | yes (the page, the captures, the manifest) | yes (→HLR-1905→LLR-1905.1, inspection) | yes (files on disk) | ✓ |

### Supersession census (change-first)
> Planned new/moved/edited files checked against EVERY guard family (behavioral-placeholder · structural/placement · AST-composition · frozen-module). State reservations; the increment gate is the completeness guarantee, not this census.

Planned files: `taskboard/views.py`, `taskboard/app.py` (edited); `tests/test_team_views.py`, `tests/test_app.py`, `tests/test_present.py` (comment) (edited); `tests/test_present_narrow.py`, `tests/test_backlog_polish_round.py` (new); the six round files (a header note each); `prototypes/backlog_polish/**` (new); `docs/ARCHITECTURE.md`. Reverse grep over `tests/` (B1, PLAN §Triggers): **must change** — the two standup nodes (their locator); `test_win_clipboard_roundtrip` (its loop moved into the helper); **read and survive** — every `render_present` reader (`test_present.py`, `test_present_room.py`, `test_present_rulers.py`, `test_present_views.py`, `test_tick_label.py`, `test_markup_census.py`) renders at 36 columns or more, so the narrow branch never reaches them; `#present-hint` readers (`test_present_hide.py` TC-1604, `test_present_views_app.py` TC-1808) read 80–118 columns, where the long and short wordings are unchanged (P-7: short from 58, long from 84); `test_markup_census.py` / `test_markup_sites.py` read `PresentScreen` markup sites — the hint is a `Text` built with `append`, the narrow line escapes a fixed string; outside `tests/`: the six round files (doc). Goldens (B3): no `tests/goldens`; the PRES-V3 frames are read at 118×30 and 80×24, unchanged. Pre-executed (C-39): P-7 (`78 passed` in the presentation tests on the probe). No frozen modules are declared in this repo. Reservations: best-effort; the increment gate confirms.

### Security review summary
Not run — trigger family C did not fire in this `core` batch (PLAN §Triggers C1–C8; the P1 scan's flags `truncate` and `escape` are Rich's `Text.truncate` of a fixed wording and `escape` of a fixed message, answered in `01-requirements.md` §6.3).

### Evidence checklists (full) — architect · qa-reviewer · ux-reviewer
> Attach each reviewer's completed evidence checklist (items in their agent files), ✓/✗ + one-line evidence.

**architect (iteration 1):** ✓ every cited line checked but one (A-4) · ✓ shall/should scan · ✓ US→HLR→LLR complete · ✓ the probe diff matches the LLRs · ✓ the map covers the change · ✗ AT-1904's 25-column arm (A-1) · ✗ AT-1902 (b) a product symbol (A-2).

**qa-reviewer (iteration 1, mode plan):** ✓ validation methods · ✗ AT-1903 self-contradiction (QA-1) · ✗ HLR-1902's skip over-breadth (QA-2) · ✓ AT-1902 (a) can go RED on base · ✗ TC-1904 tautology risk (QA-5) · ✗ AT-1905 oracles (QA-6) · ✓ results recorded `planned`, not `executed`.

**ux-reviewer (iteration 1):** ✓ context of use (§2.3) · ✗ the narrow message's action and tone (UX-1, UX-2) · ✗ the hint's survival order (UX-3) · ✗ the process rule (UX-4) · automated walkthrough `not performed` (owed at P4) · expert inspection `performed` (documents and probe diff) · evaluation with users `not performed` (one-person team; legibility inferred from contrast ratios).

### Iteration 2 (2026-10-18) — the amended contract (LED .2)

Reviewers: architect, qa-reviewer, ux-reviewer (the same agents, resumed), read-only. Every iteration-1 finding was confirmed resolved.

| ID | Reviewer | Severity | Area / Req | What | Recommendation | Status |
|----|----------|----------|------------|------|----------------|--------|
| A2-1 | architect | minor | HLR-1903, LLR-1903.1 | `q` is bound with `escape` and leaves; `h j k l` not named | "`esc`/`q`"; "every key bound to `move`" | fixed — LED .3 |
| A2-2 | architect | minor | LLR-1905.1 | `inspection` while HLR-1905 is `test` | state the split | fixed — LED .3 |
| QA2-1 | qa-reviewer | minor | AT-1903 | `a` with nothing hidden and `pagedown` in gantt cannot go RED; the narrow frame is always the rung | hide a task, open split before narrowing; compare at 118 | fixed — LED .3 (`pagedown` declared a regression pin: a resize resets the page) |
| QA2-2 | qa-reviewer | minor | P-7 vs TC-1904 | `esc leave · 10 hidden` "at 25" vs whole from 23 | state the first width | fixed — LED .3 (11 / 22 / 23) |
| QA2-3 | qa-reviewer | minor | LLR-1901.1 | padding before the spine unstated | the stripped row | fixed — LED .3 |
| UX2-1 | ux-reviewer | minor | §2.6 US-1902 log | still "every key still works", three wordings, `x` writes | restate | fixed — LED .3 |
| UX2-2 | ux-reviewer | minor | HLR-1903 | `esc leave` in both the 32–35 rung and the hint | leave it, or drop it from the rung | declared — the operator sees it in the round |

**Gate:** `approve`
