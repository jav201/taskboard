# PLAN — taskboard — Batch 2026-10-02-batch-04

> Living plan (flow `templates/plan-template.md`). Mode `core`, language `en`, flow rev99 (installed).

## Header

| Field | Value |
|---|---|
| Project | taskboard |
| Batch | 2026-10-02-batch-04 |
| Objective | Batch S (hardening): no user-authored or synced text reaches a Textual widget or notification as markup (S1, with a derived census); control bytes stripped from board and synced text at load and at sync (S2, L1); the TaskDetails info grid paints its cells |
| Flow | **rev99, the installed bundle** (`~/.claude/skills/dev-flow`, `flow_version: 2026-10-02-rev99`) — operator ruling at this batch's kickoff, 2026-10-02, verbatim: "rev99, la instalada". `~/.claude` is never edited. |
| Standing authorization | the operator's commission, asked at this batch's kickoff on 2026-10-02 and relayed by the coordinator (this runtime is a delegated sub-agent and cannot prompt), dated 2026-10-02: Gates — "Autónomo, agente Opus": the agent self-approves each station gate and records every un-asked decision (this plan's decision log, `state.json` `decisions_log`, the close record); a HIGH finding blocks regardless — stop and report back. Git — "Commit + push a main": the COORDINATOR commits and pushes after verification (and after the operator's visual verdict if any user-visible change is provisional); this agent does not commit, push, stash, reset or checkout anything and leaves all changes in the working tree. `merge: false (no PR; coordinator commits+pushes to main)`. **Amendment, asked at the P3 gate on 2026-10-03 — "Sí, solo para HIGH de pruebas":** for the rest of this batch a HIGH that is only in tests/evidence (product code confirmed correct by the reviewer) may be fixed without stopping, recorded (finding, fix, RED-first proof) and re-reviewed; a HIGH in app behaviour, security or data still stops and returns to the operator. |

## Where we are

**P5 re-closed (2026-10-04).** After the operator's visual verdict (PV-1 accepted, UX-3 and UX-4
applied) the batch re-opened to P3 (D-422). Increment 004 moved the blank row under the details
title and narrowed its label column. Gate 2218 passed, exit 0. Light P4: qa PASS-WITH-NOTES, ux PASS.
Security delta pass: PASS-WITH-NOTES. Everything is in the working tree for the coordinator.

## Objective

Bracket text — the operator's or a teammate's — never kills a dialog or a toast; control bytes
never reach the terminal from a board or a synced file; the details view shows its five fields.

## RC-1 and flow currency

- RC-1 (a): `git fetch origin` → `origin/main` = `56a1b10cc466` = HEAD = merge-base; nothing to rebase. `base_ref` stamped from it.
- RC-2: `git ls-remote --exit-code --heads origin` answered (exit 0); `origin/main`'s newest commit 2026-10-02 21:08 −0600 (`56a1b10`).
- RC-1 (b): no story already shipped on `origin/main` (`01-requirements.md` §2.6, P-3, P-4, P-5, P-8).
- Rollover from `2026-10-02-batch-03` (P5 closed): its `decisions_log` MOVED to `.dev-flow/2026-10-02-batch-03/decisions-log.json` (10 entries); every single-slot field retired per `stations/shared-batch.md` §Batch rollover (triggers re-evaluated below, artifacts cleared, homes re-pointed, owner re-stamped, authorization re-recorded from this batch's commission, `base_ref` = HEAD, `created_at` re-stamped); `mode_history` carried and appended. Seeds from the installed bundle's `devflow-init.py` run in a scratch tree (it refuses an initialised `.dev-flow/`), batch id substituted; `.gitattributes` gains this batch's `evidence/** -text`; the build caches were already in `.git/info/exclude`. The increment skeleton is held back until P3 so no packet precedes its increment.
- Flow: rev99 (`flow_hash 16c4f1a047699996`); `V7` clean. From P4 (2026-10-03 13:24) the installed `SKILL.md` carries rev100 work by another session and fails `V7`; the validator runs from a read-only snapshot of the rev99 commit `1154c8a` (D-420). Validator at kickoff (coordinator, `56a1b10`): **0 block · 26 notice**, exit 0 — re-run by this agent before the rollover: same.
- **Inherited NOTICEs declared** (all 26 predate this batch): `V9` ×8 legacy packets (`increment-001..003`, `006..010` in the flat `.dev-flow/03-increments/`) declare no SOURCE count, ×1 batch-02's `increment-002.md` 4-source warning; `V13` ×2 batch-01's IFC address `nav-order` reached by undeclared files, and batch-03's computed addresses; `V22` ×3 LLRs of batches 01/02 never used as an IFC owner and 5 legacy US ids not in the canon; `V23` an unparseable design-review citation in legacy `increment-006.md`; `V26` batch-03's live contract over its size budget; `V30` the bundle derives its floors from a subset (benign on this runtime, `SKILL.md`); `V42` ×7 deferral markers in batch-03's record without a keyed backlog entry; `V53` the closed-record census count; `V57` batch-03's close record predates this tree by 1 commit (the coordinator's commit). None is this batch's to fix; a closed record is not re-anchored.
- Not runnable here (`SKILL.md` step 4): `V15`, `V16`, `V17` — `not-run` (no canon tree, no checkout table, no hook settings on a bundle runtime).
- Mechanisms unavailable on this runtime, named once (`SKILL.md` step 5): no slash commands, no hooks, no prompt guard, no operator prompt (the standing authorization above closes the gates). Reviewer roles are **spawned as named sub-agents** of this runtime (`qa-reviewer`, `architect`, `security-reviewer`, `ux-reviewer`, `code-reviewer`, `tester`), each told to follow the installed bundle's `agents/<role>.md` — independent reviewers, never inline self-review.

## Triggers (evaluated 2026-10-02, P0) {#triggers}

| id | Verdict | Probe / evidence |
|---|---|---|
| B1 | fired | `grep -l` over `tests/` for the touched symbols (base): `ConfirmModal` → test_app, test_archive; `TextPrompt` → test_app, test_dependencies, test_setup_help; `TeamIdentityPicker` → test_team_sync; `BlockerPicker` → test_dependencies; `PhaseEditor`, `StandupModal`, `CalendarModal` → test_app; `HelpModal` → test_gantt_board, test_legend, test_setup_help; `CommandPalette` → test_colour_budget_app, test_legend, test_setup_help; `EmojiPicker` → test_emoji_picker; `#details-box` → test_details_markup; `already exists`, `Team sync failed`, `_read_json`, `ProjectPicker` → none → reverse census measured per increment |
| B2 | not fired | no file moves; new files only (`tests/test_markup_census.py`, `tests/test_markup_sites.py`, `tests/test_control_bytes.py`, `tests/test_details_grid.py`) |
| B3 | not fired | `ls tests/goldens` → no such directory |
| B4 | fired | `Board.save` writes what `Board.load` cleaned, and `TeamState.push` writes what a teammate's `_read_json` reads → output-then-consume AT-405 (C-12) |
| A | not fired (judged) | no `docs/ARCHITECTURE.md`; the `taskboard` package is one module, as batches 01–03 ruled (D-401) |
| C | fired | `devflow-scan-spec.py` → `security_required: true` (flags `form`, `escape`); file-derived and synced text rendered by Textual (C-17) → hostile-input ATs; security-reviewer at P2 and close (also commissioned) |
| D | fired | user-visible (the details grid; toasts) → ux-reviewer at P2/P4, captures 140×40 / 80×24 |
| E | fired | 3 stories, 3 planned increments |
| F | F2 fired | `BACKLOG.md` header base ref `13745f6` ≠ HEAD `56a1b10` → reconciled at close; F1 not fired: `V7` clean |

## Per-story / per-station status

| Story / station | Status | Notes |
|---|---|---|
| P0 intake | done | rollover; US-401..403 READY |
| P1 requirements | done | 3 HLR, 6 LLR, AT-401..406, TC-401..410; scan run |
| P1 refine (iteration 2) | done | US-404, HLR-404, LLR-401.3, LLR-404.1; AT-407; TC-406, TC-411..TC-414 |
| P2 review, iteration 2 | iterate-to-refine | qa FAIL (Q2-1), architect/security/ux PASS-WITH-NOTES; no HIGH |
| P1 refine (iteration 3) | done | LLR-404.2, TC-415, TC-416; P-14..P-16; D-410..D-413 |
| P2 review, iteration 3 | approved | four PASS-WITH-NOTES, 0 blocker, 0 new HIGH; notes folded (LED .9) |
| P3 increment 001 | done | 3 SOURCE; code-reviewer 3 rounds, 0 HIGH; 18/18 mutants killed; 1888 passed + clipboard env; amendments A-1..A-4 |
| P3 increment 002 | done (revision 4) | 3 SOURCE; F1 HIGH folded after the operator's ruling; code-reviewer 4 rounds OK; security CLOSED S-1, S4-1; 30/30 mutants |
| P3 increment 003 | done (revision 2) | 1 SOURCE; F1 test-only HIGH folded after the ruling; code-reviewer round 2 OK; battery 3/3 |
| P4 validation | approved | gate run 2214 passed (`evidence/p4-gate.txt`); qa + ux PASS-WITH-NOTES |
| P5 close | closed, then re-opened (D-422) | canon folded (13); BACKLOG reconciled (+14 open, 5 done); `05-close.md` |
| P3 increment 004 | done (revision 2, frozen r4) | UX-3 + UX-4 after the operator's verdict; 1 SOURCE (`taskboard.tcss`); code-reviewer 2 rounds OK, no HIGH (F1 MEDIUM test pin folded); battery 6/6 + 1 equivalent |
| P5 re-close | closed | security delta PASS-WITH-NOTES (S7-1 → BACKLOG); `05-close.md` refreshed |
| P4 light re-validation | approved | gate r3 2218 passed, exit 0; qa PASS-WITH-NOTES (N1–N6 folded); ux PASS |
| P2 review, iteration 1 | iterate-to-refine (stopped on HIGH S-1; operator ruled 2026-10-03) | qa FAIL (Q-1), security FAIL (S-1 HIGH, S-2), architect + ux PASS-WITH-NOTES; `02-review.md` |

## Roadmap + increment plan

Re-cut after P2 iteration 1 (C-21: AT-407 added, AT-401..406 redefined):

1. Increment 001 — S1 + the picker status: every Textual sink fed a markup-inert value, user text as `Text` pieces (titles, grid values, notes highlights, picker lines, selects, confirms), toasts `markup=False`; the census TC-401..406; `tester` authors AT-401..403 (and TC-412) RED on base first; `test_details_markup.py` payload set extended. Supersedes (A-7): `test_archive.py:557-577`, `test_app.py:300-313`, `test_app.py:2052-2059`. SOURCE: `modals.py`, `app.py`, `views.py` (the shared highlight tokeniser, D-411).
2. Increment 002 — S2 + S-1/S-3 validation: `strip_controls` / `clean_strings`, the load door, the sync doors (incl. the Setup view's `team.json` read), the clipboard rule, `Project.from_dict` name/date checks, `apply_config_to_board` through it (TC-407..410, 413, 414; AT-404, 405; `tester` authors AT-407). SOURCE: `models.py`, `team_sync.py` (with `clean_roster`, A3-1), `app.py` (the Setup roster and `team.json` reads).
3. Increment 003 — the details grid rule (TC-411, AT-406); `test_details_markup.py`'s project/phase arms read the painted screen; captures before/after. SOURCE: `taskboard.tcss`.
4. Increment 004 (after the re-open, D-422) — UX-3 and UX-4: one blank row under the details title instead of two above it, the details label column 10 cells (TC-420, TC-421; TC-411's long-name arm 2 rows at 80×24); captures `after2-details-*`. SOURCE: `taskboard.tcss`.

## Key decisions

| Date | Decision | Why |
|---|---|---|
| 2026-10-04 | Asked at the gate — operator visual verdict: PV-1 "Aceptar", UX-3 "Aplicarlo", UX-4 "Aplicarlo" (`evidence/operator-verdict-provisional.json`) | operator, 2026-10-04 |
| 2026-10-04 | D-422: re-open by iterate-to-refine to P3 (increment 004, amendment A-7), light P4, re-close P5 | the verdict changes product code after P5 |
| 2026-10-04 | Increment 004 approved (revision 2); light P4 approved; P5 re-closed (validator 0 block) | `03-increments/increment-004.md`, `04-validation.md`, `05-close.md` |
| 2026-10-04 | D-423: the canon row of LLR-403.1 updated by hand (the fold never rewrites an existing row) | `REQUIREMENTS.md` |
| 2026-10-02 | Batch id `2026-10-02-batch-04` | the operator's local date is still 2026-10-02 (commission) |
| 2026-10-02 | Ids in a disjoint `4xx` range | `0xx`..`3xx` taken |
| 2026-10-03 | Asked at the gate — ruling 1, scope: "Sí, dentro de S" (S-1, S-3 in; US-404, HLR-404) | operator, 2026-10-03 |
| 2026-10-03 | Asked at the gate — ruling 2, fix form: "Piezas de texto, sin formato" (Text pieces, never parsed; LLR-401.3) | operator, 2026-10-03 |
| 2026-10-03 | Asked at the gate — ruling 3, folds: "Sí, todas" (02-review.md §Iteration-1 fold; D-407..D-410) | operator, 2026-10-03 |
| 2026-10-03 | D-420: validator from a read-only snapshot of rev99 (skills `1154c8a`) — the installed bundle's `SKILL.md` took rev100 work at 13:24 (V7) | `PLAN.md` §RC-1 |
| 2026-10-03 | Increment 003 approved (revision 2); P3 closed | `03-increments/increment-003.md` |
| 2026-10-03 | Asked at the gate — "Sí, corregir y seguir" (fold F1 into the details-grid increment, one more review, then P4 and P5) | operator, 2026-10-03 |
| 2026-10-03 | Asked at the gate — "Sí, solo para HIGH de pruebas" (standing-authorization amendment: a tests/evidence-only HIGH is fixed without stopping, recorded and re-reviewed) | operator, 2026-10-03 |
| 2026-10-03 | Asked at the gate — "Corregir todo en el 002" (fold F1 HIGH, S4-1, F2, F3, F4, N4 into increment 002) | operator, 2026-10-03 |
| 2026-10-03 | Increment 002 approved (revision 4, autonomous after the ruling); D-416..D-419 | `03-increments/increment-002.md` |
| 2026-10-03 | Increment 001 approved (autonomous): code review 3 rounds, 0 HIGH; H1/H2 census limits → BACKLOG; D-415 | `03-increments/increment-001.md` |
| 2026-10-03 | P2 iteration 3 approved (autonomous): four PASS-WITH-NOTES; A3-1, Q3-1 and the minors folded at the gate; D-414 | `02-review.md` §Iteration 3, LED .9 |
| 2026-10-03 | P2 iteration 2 → iterate-to-refine (Q2-1); P1 iteration 3 approved; iteration cap reached on P1, continuing (root cause: oracles drafted as predictions) | `02-review.md` §Iteration 2, LED .8 |
| 2026-10-03 | P1 iteration 2 approved (standing authorization): HLR-404, LLR-401.3, LLR-404.1; P-11..P-13 TRUE | `01-requirements.md`, ledger LED .4–.7 |
| 2026-10-02 | P2 iteration 1 → iterate-to-refine; batch stopped on the security HIGH S-1 (standing authorization: a HIGH blocks regardless) | `02-review.md` |
| 2026-10-02 | D-401..D-406 (A not fired; three exempt app-constant sites; `_rich`/`Text`/`markup=False` forms; CR-LF → LF and DEL removed; `collapse_runs` stays in BACKLOG; one row per grid field) | `01-requirements.md` §6.2 |

## Provisional visual decisions (for the operator, with the captures to compare)

| Id | Decision | Captures (before → after) |
|---|---|---|
| PV-1 | **accepted 2026-10-04.** The details info grid draws one row per field, no blank row between fields, long values wrap (UX-1); the edit modals untouched (D-406). UX-3 (a gap under the title) and UX-4 (a 10-cell label column) **applied** in increment 004 → `after2-details-*` | `evidence/captures/` base-details-140x40 → after-details-140x40; base-details-80x24 → after-details-80x24; and the `-long` pair of each (`.svg` + `.txt`) |

## Risks / watch-items

- The census rule is syntactic; a sink hidden behind a helper that returns a `str` passes only if the helper's result reaches a sink as a bound name (then it is flagged) — the method and attribute sink names are a declared list (§6.3).
- Converting Textual-parsed app markup to Rich-parsed (`_rich`) could shift a style; the help, standup and calendar nodes pin their text.

## Conventions honored

- Test docstrings in the house style (field report · law · RED), AT/TC ids in docstrings and names.
- No new dependency; Textual 8.2.8 / Rich 15.0.0.

## Out-of-scope carries

- `collapse_runs` S-2 (D-405); everything else in `BACKLOG.md`.

## Security scan

`python <flow>/scripts/devflow-scan-spec.py .dev-flow/2026-10-02-batch-04/01-requirements.md` →
`security_required: true`, flags `session`, `form`, `escape` at iteration 2 (controls 5/5 ok); answered in
`01-requirements.md` §6.3 (`evidence/p1-security-scan.txt`).

## Test ledger

| Suite / command | Last run | Result |
|---|---|---|
| `python -m pytest -q -p no:cacheprovider` (base `56a1b10`) | 2026-10-02 | 1854 passed, 1 failed (clipboard environment, G-011) in 217.28 s (`evidence/base-suite.txt`) |
| increment-004 gate run (frozen r3) | 2026-10-04 | 2218 passed in 398.62 s, exit 0 (`evidence/inc004-gate-r3.txt`); frozen r4 (docstring only) details files 91 passed |
| P4 gate run (final tree) | 2026-10-03 | 2214 passed in 306.98 s, exit 0 (`evidence/p4-gate.txt`) |
| same, after increment 002 (frozen r4, grid file deselected) | 2026-10-03 | 2206 passed, 1 failed (clipboard environment) in 351.84 s (`evidence/inc002-green.txt`) |
| same, after increment 001 (frozen r3) | 2026-10-03 | 1888 passed, 1 failed (clipboard environment) in 274.84 s (`evidence/inc001-green.txt`) |

## Decision log

Mirrors `state.json` `decisions_log`.
