# PLAN — taskboard — Batch 2026-10-02-batch-02

> Living plan (flow `templates/plan-template.md`). Mode `core`, language `en`, flow rev98.

## Header

| Field | Value |
|---|---|
| Project | taskboard |
| Batch | 2026-10-02-batch-02 |
| Objective | Batch P (polish): the operator's 12 answers to batch-01's questions (D4 D5 D9 D10 D12 D13 D14 UXV-2 UXV-3 PKT SOON HELP) plus the app-wide colour budget (accent = focus only) and UXV-7 |
| Flow pin | **rev98, pinned** — operator ruling asked 2026-10-02, verbatim: "Fijar el batch a rev98". The declared rev98 bundle (skills commit `48154ab`, "flow rev98 — the bundle regenerated over closefix 6") is extracted read-only to the session scratchpad (`devflow-rev98-48154ab/dev-flow`); the validator runs from that directory as bundle root and the flow's rules are read there. Reason: the flow owner started rev99 today (skills commits `d5e4065` / `15549c0` / `922cfcb`, "flow rev99 L4") and `~/.claude/skills/dev-flow/SKILL.md` was edited without a re-sync — rev99-wip, not declared. `~/.claude` is never edited. |
| Standing authorization | the operator's commission, asked at this batch's kickoff on 2026-10-02 and relayed by the coordinator (this runtime is a delegated sub-agent and cannot prompt), dated 2026-10-02: Gates — "Autónomo, agente Opus": end-to-end autonomous; the agent self-approves each station gate and records every un-asked decision (this plan's decision log, `state.json` `decisions_log`, the close record); a HIGH finding blocks regardless — stop and report back. Git — "Commit + push a main": authorized for the COORDINATOR only; this agent does not commit, push, stash, reset or checkout anything and leaves all changes in the working tree. `merge: false (no PR; coordinator commits+pushes to main)`. |

## Where we are

**P5 closed.** Increments 001–006 approved; P4 approved at iteration 2 (qa PASS-WITH-NOTES, 23/23,
gate re-run 1677 passed); canon folded (23 rows); BACKLOG reconciled; `05-close.md` written; the
closing validator (pinned rev98 bundle) exit 0, 0 block, 18 notice (`evidence/validator-close.txt`).
Every change stays in the working tree for the coordinator's commit.

## Objective

Every view, the key bar, the ribbon and the dialogs spend the accent only on focus roles; the
app speaks English; the gantt says what it is not showing (paged hint, finish toast), folds
predictably (sticky visited, urgent last), shades weekends and clips its echo honestly.

## RC-1 and flow currency

- RC-1: `git fetch origin` → `origin/main` = `a0e7d9a7c76d` = HEAD = merge-base. `base_ref` stamped from it.
- Rollover from `2026-10-02-batch-01` (P5 closed): its `decisions_log` MOVED to `.dev-flow/2026-10-02-batch-01/decisions-log.json`; every single-slot field retired per `stations/shared-batch.md` §Batch rollover (triggers re-evaluated below, artifacts cleared, homes re-pointed, owner re-stamped, authorization re-asked, `base_ref` = HEAD); `mode_history` carried and appended. The increment skeleton is held back until P3 so no packet precedes its increment.
- Flow: rev98 — from 2026-10-02 (after increment 001) the PINNED snapshot of skills commit `48154ab` (header row "Flow pin"); before that the live bundle, then still rev98 (kickoff and P0–P2 runs V7-clean). Validator at kickoff (coordinator, `a0e7d9a`): **0 block · 17 notice**, exit 0 — re-run by this agent before the rollover: same.
- **Inherited NOTICEs declared** (all 17 predate this batch): `V9` ×8 legacy packets (`increment-001..003`, `006..010` in the flat `.dev-flow/03-increments/`) declare no SOURCE count; `V13` ×2 batch-01's IFC address `nav-order` reached by 144 undeclared files, and its computed `task-rows` address; `V22` ×2 batch-01 LLRs never used as an IFC owner (a question per id), and 5 legacy US ids not in the canon; `V23` an unparseable design-review citation in legacy `increment-006.md`; `V26` batch-01's live contract is 62 205 characters (> 54 000); `V30` the bundle derives its floors from a subset (benign on this runtime, `SKILL.md`); `V53` the closed-record census count; `V57` batch-01's close record predates this tree by 1 commit (the coordinator's commit). None is this batch's to fix; a closed record is not re-anchored.
- Not runnable here (`SKILL.md` step 4): `V15`, `V16`, `V17` — `not-run` (no canon tree, no checkout table, no hook settings on a bundle runtime).
- Mechanisms unavailable on this runtime, named once (`SKILL.md` step 5): no slash commands, no hooks, no prompt guard, no operator prompt (the standing authorization above closes the gates). Reviewer roles are **spawned as named sub-agents** of this runtime (`qa-reviewer`, `ux-reviewer`, `code-reviewer`, `security-reviewer`, `tester` where owed), each given its `agents/<role>.md` — independent reviewers, never inline self-review.

## Triggers (evaluated 2026-10-02, P0)

| id | Verdict | Probe / evidence |
|---|---|---|
| B1 | fired | per-symbol `grep -rlE <sym> tests/` (qa P2 Q-15): `▬` → test_motion, test_gantt, test_gantt_board, test_app; accent → test_team_views, test_keymap, test_cells; Spanish → test_setup_help, test_flow_view; `reldue_token` → test_colour_budget, test_cells; `update_clock` → test_palette_ration; folds/paging → test_gantt_board TC-103, TC-106 → reverse census measured per increment |
| B2 | not fired | no file moves; new files only (`tests/test_colour_budget_app.py`, `tests/test_english.py`, `tests/test_gantt_polish.py`) |
| B3 | not fired | `ls tests/goldens` → no such directory |
| B4 | fired | the gantt's `line_map` → `app._scroll_selected_into_view`; `legend_entries` → `HelpModal`; `help_usage` → `HelpModal`; `probe_setup_health` → `render_setup` → AT through the app |
| A | not fired (judged) | no `docs/ARCHITECTURE.md`; the `taskboard` package is one module, as batch-01 ruled (D-215) |
| C | fired | `devflow-scan-spec.py` → `security_required: true` (flags `token`, `role`); the toast prints a file-derived title through `notify` (C-17) → security-reviewer at P2 and on increment 005 |
| D | fired | user-visible on every view → ux-reviewer at P2/P4, captures 118×30 / 80×24 |
| E | fired | 5 stories, 5 planned increments |
| F | F2 fired | `BACKLOG.md` header base ref `57a6075` ≠ HEAD `a0e7d9a` → reconciled at close; F1 not fired: `V7` clean |

## Per-story / per-station status

| Story / station | Status | Notes |
|---|---|---|
| P0 intake | done | rollover; US-201..205 READY; D13 a decision, not a story |
| P1 requirements | done | 10 HLR, 12 LLR, AT-201..210; scan run |
| P2 review, iteration 1 | iterate-to-refine | 1 blocker (UX-1), 17 major; all folded or carried (`02-review.md`) |
| P2 review, iteration 2 | approved | qa + ux PASS-WITH-NOTES; N-1..N-3, UX-11, UX-12 folded (LED .15) |
| P3 increment 001 | done | `views.py`; code-reviewer 3 rounds (R2-F1 HIGH folded); 21/21 mutants killed; 1630 passed |
| P3 increment 002 | done | 4 SOURCE (cap); code-reviewer 2 rounds (F1 HIGH folded; F3 pre-existing toggle bug fixed, D-218); 16/16 killed; 1634 passed |
| P3 increment 003 | done | 3 SOURCE; code-reviewer 2 rounds (F1 HIGH: lexicon blind, folded with a derived vocabulary); 14/14 killed; 1643 passed |
| P3 increment 004 | done | `views.py`; 2 laws fixed in code; code-reviewer 2 rounds OK; 15/15 killed; 1662 passed |
| P3 increment 005 | done | 3 SOURCE; code-reviewer 2 rounds OK; security PASS-WITH-NOTES; 16/16 killed; 1677 passed |
| P4 validation, iteration 1 | iterate-to-fix | qa FAIL G-001..G-003 (AT-207 on two nodes; a false kill claim; HLR-203 wording); ux PASS-WITH-NOTES |
| P3 increment 006 | done | 0 SOURCE; AT-207 one node; record corrected; code-reviewer PASS-WITH-NOTES ×2 |
| P4 validation, iteration 2 | approved | gate re-run 1677 passed; qa PASS-WITH-NOTES 23/23, 11/11 |
| P5 close | done | `05-close.md`; canon 23; privacy sweep 0 board strings; validator 0 block |

## Roadmap + increment plan

1. Increment 001 — colour budget on the seven views, Setup rows keep their styles, SOON + PKT (HLR-201, HLR-203; LLR-201.1, 201.2, 201.3, 203.1; AT-201, AT-203). SOURCE: `views.py`.
2. Increment 002 — colour budget on the chrome (HLR-202; LLR-202.1, 202.2; AT-202). SOURCE: `keymap.py`, `ribbon.py`, `app.py`, `taskboard.tcss` (⚠ 4 — the chrome lives in four files).
3. Increment 003 — English (HLR-204; LLR-204.1; AT-204). SOURCE: `views.py`, `team_sync.py`, `modals.py`.
4. Increment 004 — gantt field: paged hint, urgency order, weekends, clip arrows (HLR-205, 208, 209, 210; LLR-205.1, 207.1 (urgency half), 209.1, 210.1; AT-205, 208, 209, 210; census carries TC-106, Q-14). SOURCE: `views.py`.
5. Increment 005 — previous group sticky + finish toast (HLR-206, 207; LLR-206.1, 207.1 (previous), 207.2; AT-206, 207); security-reviewer over the toast. SOURCE: `views.py`, `app.py`, `modals.py`.

## Key decisions

| Date | Decision | Why |
|---|---|---|
| 2026-10-02 | Ids in a disjoint `2xx` range | `0xx`/`1xx` taken in the record and canon |
| 2026-10-02 | D-201 today keeps the accent, selection reverse (D4 keep) · D-202 `━` stays shared (D13 keep) | operator answers |
| 2026-10-02 | D-203 only the previous group is sticky (P2 UX-4) | a session-long list let quiet groups outrank urgent ones; same measured benefit |
| 2026-10-02 | D-204 urgency weight = late + due-today, ties by due-today count (P2 UX-3/Q-5) | the frame the operator complained about now unfolds Ops & Security |
| 2026-10-02 | D-216 the visual decisions (D-203/204/205/208/211) flagged for the operator's verdict on captures | all 12 answers are the recommended option with no notes (UX-9) |
| 2026-10-02 | P2 iteration 1 → iterate-to-refine; folds LED .11–.14 | `02-review.md` |
| 2026-10-02 | D-217 "fold last" = offered rows first, skip-and-continue kept (UX-11); P2 approved at iteration 2 | blank rows otherwise; for the operator |
| 2026-10-02 | D-205 `WEEKEND_BG = #1a1d22` (prototype `#161d27` quantises onto the field) · D-206 shade day row + body field | P-4 measurement; prototype |
| 2026-10-02 | D-207 focus roles kept · D-208 re-tones · D-209 SOON wherever `reldue_token` paints (`date_chip` (the Focus tiles, cards, image and compact cards, the detail pane and the review layout's selected-task line) is outside — LED .19) · D-210 packet `mut` · D-211 ribbon tones | `01-requirements.md` §6.2 |
| 2026-10-02 | D-212 internal keys stay; D-213 hint wording as chosen; D-214 toast only for `]` reaching done, markup off; D-215 A not fired | §6.2 |
| 2026-10-02 | Evidence transcripts redact the home path (`<home>`) | the record must not leak it |
| 2026-10-02 | D-218 the key bar's `;` layer toggle (pre-existing bug, code review F3) fixed in increment 002 | one token in a file already in the set; HLR-202's `more` layer was otherwise invisible |
| 2026-10-02 | D-219 the help names only shipped keys (`t` pins; the filter has no key) | found while translating (LED .17) |
| 2026-10-02 | **Batch pinned to rev98** (operator: "Fijar el batch a rev98"; bundle = skills `48154ab`, read-only snapshot) | `~/.claude/skills/dev-flow` became rev99-wip mid-batch; `evidence/validator-p3-inc001.txt`'s V7 block was that wip bundle (its `SKILL.md` hash), not the project — re-run from the pinned bundle: V7 clean, 8 × V2 only |

## Risks / watch-items

- Sticky unfolding lowers, not removes, upward moves (P-12: 3 → 2 at panel 80×22).
- Shared helpers (`reldue_token`, `header`, `status_glyph`) are pinned by other batches' tests — reverse census per increment.
- Translating help copy must keep every gantt help line ≤ 44 cells (TC-116).

## Conventions honored

- Test docstrings in the house style (field report · law · RED), AT/TC ids in docstrings.
- No new dependency; Textual 8.2.8 / rich 15.0.0 pins; prototype code re-derived, not pasted.

## Out-of-scope carries

- Everything else in `BACKLOG.md` (Batch A2, help right-column layout, `_strip` F5, Setup's interval, screenshots, S-8, S-5).

## Security scan

`python <flow>/scripts/devflow-scan-spec.py .dev-flow/2026-10-02-batch-02/01-requirements.md` →
`security_required: true`, flags `token`, `role` (controls 5/5 ok); answered in
`01-requirements.md` §6.4.

## Test ledger

| Suite / command | Last run | Result |
|---|---|---|
| `python -m pytest -q -p no:cacheprovider` (base `a0e7d9a`) | 2026-10-02 | 1611 passed in 176.37 s (`evidence/base-suite.txt`) |
| same, after increment 001 | 2026-10-02 | 1630 passed in 173.42 s (`evidence/inc001-green.txt`) |
| same, after increment 002 | 2026-10-02 | 1634 passed in 201.05 s (`evidence/inc002-green.txt`) |
| same, after increment 003 | 2026-10-02 | 1643 passed in 183.38 s (`evidence/inc003-green.txt`) |
| same, after increment 004 | 2026-10-02 | 1662 passed in 183.68 s (`evidence/inc004-green.txt`) |
| same, after increment 005 | 2026-10-02 | 1677 passed in 190.36 s (`evidence/inc005-green.txt`) |
| P4 gate run (C-25), iteration 1 | 2026-10-02 | 1677 passed in 183.75 s (`evidence/p4-gate.txt`) |
| P4 gate re-run after increment 006 | 2026-10-02 | 1677 passed in 182.11 s (`evidence/p4-gate2.txt`) |

## Decision log

Mirrors `state.json` `decisions_log`.
