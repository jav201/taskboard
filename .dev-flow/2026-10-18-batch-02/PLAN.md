# PLAN — taskboard — Batch 2026-10-18-batch-02

> **Artifact language.** Canonical **English scaffold**; generate in the batch's language.
> **Owed in.** `core` ✓ · `full` ✓
> Seeded by `/dev-flow-init` step 4 at both levels; the living plan is owed at every gate
> that follows (`/dev-flow` §Living plan is the rule's home).

> **Field guide:** `templates/guides/plan-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.
> **Two header labels are read literally and are never translated:** `Standing authorization` and `Last updated`; the field guide names their readers.

The living compendium of this batch: where-we-are · objective · per-story/per-station status ·
roadmap + increment plan · key decisions · risks/watch-items · conventions honored ·
out-of-scope carries · test ledger · decision log (the human-readable mirror of `state.json`).
**Create at batch open and update at every gate and significant checkpoint** — the
orchestrator presents the full plan in-conversation at each phase gate.

## Header

| Field | Value |
|---|---|
| Project | taskboard |
| Batch | 2026-10-18-batch-02 |
| Objective | Backlog fixes: the two standup tests (the scrubbed fixture name against the 12-cell name column), the clipboard test (an environment refusal skips, a roundtrip mismatch fails), the presentation at any width >= 0 and its hint row's fallback below 58 columns, the two stale prototype scripts marked historical; a prototype round, no production change, for the dim view word and cut marks, the 80-column hint and the gantt view's 3-row note cap |
| Last updated | P5 · 2026-10-18 |
| Standing authorization | standing authorization — the coordinator's commission of 2026-10-18 (the runtime cannot prompt), relaying the operator's words (translated): «Continue with the backlog: fix the Standup tests and the other missing items.» Quoted from the commission: «Open a NEW dev-flow batch in `C:\Users\jjgh8\Github\taskboard` … Create a local branch `backlog-fixes` from main … follow `stations/core-runbook.md`», «No push, merge, reset or force», «At most 4 SOURCE files per increment», «Never rewrite oracle frames whose hashes were recorded; new frames go in new files», «An independent `code-reviewer` per increment, spawned», «P4 and P5 close». Read as: every gate of this batch is autonomous (reviewer roles are spawned sub-agents); commits on the local branch `backlog-fixes` are authorized, each ending with the commission's co-author line; **push and merge are NOT authorized**; synthetic data only; the operator's name nowhere (`username_subject`); the three PROTOTYPE items get a prototype round only — no production change before the operator's verdict (the operator's standing rule for TUI design changes). |
| First gate | step 1, on `main` `9e82b10` before the branch: exit 0 — 0 block · 40 notice · 65 not applicable; `V7`: bundle identical to its manifest both directions, 57 declared files, `2026-10-12-rev102`. Step 3 (after the rollover): exit 0 — 0 block · 62 notice · 47 not applicable. |
| Premises / RC-1 | RC-1 (a): `git fetch origin` → `origin/main` = `9e82b10acb94514e10a10c2f6efe799dc920a17e` = local `main` (the previous batch's branch was merged upstream); `git switch -c backlog-fixes main`; HEAD equals the origin tip, so no rebase is owed; `base_ref` = `9e82b10acb94514e10a10c2f6efe799dc920a17e`. RC-1 (b): not already shipped — the standup tests fail on `origin/main` (`python -m pytest tests/test_team_views.py` → 2 failed, 251 passed); `render_present` on `origin/main` asserts below 36 columns (`views.py:6464`; the sweep in `01-requirements.md` §2.7); `PresentScreen._hint` has two wordings and no fallback (`app.py:275-293`); `test_win_clipboard_roundtrip` asserts on its own setup (`tests/test_app.py:1215-1217`). RC-2: `git ls-remote --exit-code --heads origin` → exit 0; newest `origin/main` commit 2026-10-18 12:27 -0600. Premises: `01-requirements.md` §2.7. |

## Triggers

The trigger evaluation `state.json`'s `triggers.record` points at: one row per trigger evaluated, fired or not.

| Id | Verdict | Probe output |
|---|---|---|
| A1 | not fired | judged — `docs/ARCHITECTURE.md` §2 · no module created, no boundary moved: the planned source files (`taskboard/views.py`, `taskboard/app.py`) are existing modules'; the tests and the prototype folder sit under the declared `tests` and `prototypes` modules |
| A2 | fired | judged — the planned source files are `taskboard/views.py` (module `views`) and `taskboard/app.py` (module `app`): two modules |
| A3 | fired | judged — `render_present`'s interface row (`docs/ARCHITECTURE.md` §4, consumed by `app.PresentScreen`) gains its width domain: every width ≥ 0 returns a frame, where below 36 it raised; `PresentScreen` reads `PRESENT_MIN_WIDTH` (its narrow mode) |
| A4 | not fired | judged — one lane, increments in order |
| B1 | fired | `grep -rl` over `tests/`: `render_present` → `test_markup_census.py`, `test_present.py`, `test_present_room.py`, `test_present_rulers.py`, `test_present_views.py`, `test_tick_label.py`; `present-hint` → `test_present_hide.py`, `test_present_views_app.py`; `_hint` → those two plus `test_gantt_polish.py`, `test_link_picker.py` (other screens' own `_hint`); `PresentScreen` → `test_markup_census.py`, `test_markup_sites.py`, `test_present.py`, `test_present_hide.py`, `test_present_views_app.py`, `test_report.py`; `render_standup` → `test_team_views.py`; `grab_clipboard_text` / `test_win_clipboard_roundtrip` → `test_app.py`; `prototypes/present` → `present_board.py`, `present_notes_board.py`, `test_present_rulers.py`, `test_present_views.py` (docstrings citing the rounds) |
| B2 | not fired | no file moves |
| B3 | fired | `ls tests/goldens` → no such directory; the byte oracle the presentation tests read is batch evidence (`PRES-V3-*` of 2026-10-18-batch-01, read by `tests/test_present.py` and `tests/test_present_views.py`) at 118×30 and 80×24 — above the 36-column floor, with the hint outside the frame, so no frame is expected to drift; named in the census and re-run in every suite |
| B4 | fired | judged — the presentation's `x` export writes the frame on screen (`save_present_svg` / `save_present_png` over `render_present`); below 36 columns it now writes the narrow frame where the app raised before |
| C1–C7 | not fired | `devflow-scan-spec.py` over `01-requirements.md` (P1) — recorded there; no auth, secret, external integration, sensitive data, DB, network or new input surface |
| C8 | not fired | judged — the narrow frame's text and the hint's wordings are fixed strings and counts; no board-file text enters a new markup row (the hint is a Rich `Text` built with `append`, never markup) |
| D1 | fired | judged — the narrow frame and the hint's fallback change what the user sees; `ux-reviewer` joins P2 and the PDR; the prototype round is a design artifact for the operator |
| D2 | not fired | judged — the prototype round runs the real Textual app headless (`export_screenshot`), the target technology |
| E1 | fired | 3 stories (US-1901..US-1903) and 3 planned increments |
| E2 | not fired | judged — no high risk declared: test fixes, a crash guard, a wording fallback, a prototype round |
| E3 | not fired | judged — internal tool, no client deliverable |
| F1 | not fired | `V7`: bundle identical to its manifest at `2026-10-12-rev102` |
| F2 | not fired | judged — `BACKLOG.md` was refreshed at 2026-10-18-batch-01's close (`ce62176`, `9e82b10`) |

## Where we are

Closed (P5, 2026-10-18) — ARQ approved after one iterate; P1/P2 approved after one iterate-to-refine; the PDR sealed approved with conditions (PC-1..PC-6); increments 001 (`2c6ac76`), 002 (`1ba8c3f`) and 003 (`627b19d`) implemented, reviewed (code-reviewer OK, 0 HIGH, each re-read after its folds) and committed; the DDR approved after DDR-C1 was discharged by exercise (`7e849dc`); P4 PASS-WITH-NOTES (2740 passed, 0 failed); the canon folded; the batch is closed on the local branch `backlog-fixes`, not pushed (the commission forbids a push). The three polish items await the operator's verdict on `prototypes/backlog_polish/backlog-polish-prototype.html`.

## Objective

Make the suite tell the truth (0 failures; the clipboard test skips with a reason when the machine refuses its setup), keep the presentation alive and honest at any terminal width, mark the prototype scripts that no longer run, and put the three open polish items in front of the operator as a prototype round with real-app captures — without changing production for them.

## Backlog inventory (P0 classification)

The open items of the `BACKLOG.md` lanes after 2026-10-16-batch-01, 2026-10-17-batch-01 and 2026-10-18-batch-01, plus the commission's items.

| # | Item (lane) | Class | Disposition |
|---|---|---|---|
| 1 | the two failing standup tests (16) | FIX | increment 001 — HLR-1901 |
| 2 | `test_win_clipboard_roundtrip` fails on its own setup (16, G-001) | FIX | increment 001 — HLR-1902 |
| 3 | `render_present` asserts below ~36 columns (18) | FIX | increment 002 — HLR-1903 |
| 4 | the short hint clipped below 58 columns (18, code-review F2) | FIX | increment 002 — HLR-1904 |
| 5 | `present_rulers/app_capture.py` and `present_views/views_proto.py` no longer import (commission) | FIX | increment 001 — a `HISTORICAL` header note on each round file that no longer imports: the two named plus the four that fail with them — `present_rulers/proto.py` (imported by `app_capture.py`; broken since 2026-10-17-batch-01), `present_views/views_d.py` and `app_capture.py` (they import `views_proto`), `app_capture2.py` (it imports `app_capture` and `views_d`) — probed by importing every `.py` of both rounds on `base_ref` (doc) |
| 6 | stale comments naming PRES-C / PRES-R / "hybrid" (16, G-005): the presentation section header in `views.py`, the TC-1001 banner in `tests/test_present.py` | FIX | increment 002 (comment-only) |
| 7 | the `*_presc_frame_*` test names (16, G-005) | DECLINE | renaming nodes breaks the citations the sealed batch records hold; their docstrings already name PRES-V3 |
| 8 | the dim view word and cut marks at ~3:1 (18, UX4-2) | PROTOTYPE | increment 003 — `prototypes/backlog_polish/` |
| 9 | the terse 80-column hint (18, UX4-3) | PROTOTYPE | increment 003 |
| 10 | the gantt view's 3-row note cap (18, UX4-4) | PROTOTYPE | increment 003 |
| 11 | the tick-row label `selected: no dates` (16/17) | OPERATOR | approved "for now" (2026-10-17); left open and listed |
| 12 | round 1's Slide view (18) | OPERATOR | an optional future view: a prototype against the shipped split view first; not commissioned |
| 13 | page snapping to an item's start; headings scrolling with the area (18, UX-2/UX-3) | OPERATOR | a paging-behaviour change: by the standing rule it needs a prototype round, which this commission does not list |
| 14 | round 1's Cards view (18) | DECLINE | dropped by the operator's verdict (2026-10-17/18); kept only so it is not re-proposed |
| 15 | `present_note_lines` wraps by code points (18, S-3) | DECLINE | already shipped: `_wrap_cells` (2026-10-18-batch-01 increment 001, code-review F1), pinned by `tests/test_present_views.py` (the wide-glyph arm); the backlog line is stale and is marked done |
| 16 | `_present_ruler` repeats the gantt ruler block (16, F3) | DECLINE | a refactor of the gantt view's frame code for no behaviour change, under byte oracles (PRES-V3, C-2b); not commissioned |
| 17 | the PNG export asserted only as file-or-toast (16, G-004) | DECLINE | asserting raster content needs Edge on the test host — an environment dependence the suite avoids; the batches' captures are the visual record |
| 18 | `mutate.py` prints mutants truncated (16, G-007) | DECLINE | that script is sealed evidence of 2026-10-16-batch-01; this batch's harness prints each edit whole |

## Per-story / per-station status

| Story / station | Status | Notes |
|---|---|---|
| US-1901 | DONE | increment 001 · AT-1901, AT-1902 pass |
| US-1902 | DONE | increment 002 · AT-1903, AT-1904 pass |
| US-1903 | DONE | increment 003 · AT-1905 passes; the three items await the operator's verdict |
| ARQ | approved | `docs/ARCHITECTURE.md` amended (one iterate: F1, F2 folded) |
| P1 | approved (one iterate-to-refine) | 5 HLR, 5 LLR, AT-1901..1905, TC-1901..1904 (LLR-1905.1 by inspection), premises P-1..P-9; scan flags `truncate`, `escape` answered |
| P2 | approved | iteration 1 iterate-to-refine (9 majors → LED .2), iteration 2 approve (7 minors → LED .3) |
| P4 | PASS-WITH-NOTES | `04-validation.md`, gate run `evidence/suite-p4.txt` (2740 passed) |
| P5 | closed | `05-close.md` |
| DDR | approved | `design/DDR-2026-10-18-batch-02.md` (architect: with condition DDR-C1, discharged by the notice capture; qa: approved) |
| PDR | approved with conditions | `design/PDR-2026-10-18-batch-02.md`; PC-1..PC-6 (PC-1..PC-3 as LED .4) |
| P3 | done | increment 001 done (0 source files; RED 2+1 on base; 12/12 mutants KILLED; 2733 passed, 0 failed; code-reviewer OK, 0 HIGH); increment 002 done (2 source files; RED 5/6 on base, the 6th a pin; 19/20 mutants KILLED, N15 a declared pin; 2739 passed, 0 failed on run 2 — run 1 had a HelpModal timing flake; code-reviewer OK after F1-F3); increment 003 done (0 source files; 45 (+1 at the DDR) real-app captures, the page; AT-1905 RED on base and on 8 corrupted copies; 2740 passed, 0 failed; code-reviewer OK after F1-F4, LED .8); P3 complete |

## Roadmap + increment plan

- 001 — the suite tells the truth: `tests/test_team_views.py` (standup), `tests/test_app.py` and a new guard test (clipboard), `HISTORICAL` header notes on the six round files that no longer import. 0 source files.
- 002 — the presentation at any width: `taskboard/views.py` (the narrow frame; the stale section comment), `taskboard/app.py` (`PresentScreen._hint` fallback); renderer and app tests. 2 source files.
- 003 — the prototype round: `prototypes/backlog_polish/` (capture script, captures, page) and its acceptance test. 0 source files.

## Key decisions

| Date | Decision | Why |
|---|---|---|
| 2026-10-18 | branch `backlog-fixes` from `main` `9e82b10` = `origin/main`; no rebase | HEAD equals the origin tip |
| 2026-10-18 | rollover by script with `devflow-init.py`'s own seed helpers (the 2026-10-18-batch-01 pattern); the evidence home's `-text` mark is a per-directory `evidence/.gitattributes` | the root `.gitattributes` was dirty before the batch and the commission says to leave it alone |
| 2026-10-18 | the stale prototype files get a `HISTORICAL` header note, not repaired imports | the cheaper option and the honest one: those rounds captured the deleted helpers' behaviour (flattened notes) on a renderer that has since moved (the view word, the PRES-V3 note), so a "repaired" script would not reproduce its own recorded outputs; their `out/` captures stay the record |

## Risks / watch-items

- the narrow frame and the hint fallback are wording the operator has not seen · medium · fixed text, captured from the real app in the evidence, named in the close for the operator; the commission classed both as FIX
- the clipboard test now skips where it failed · medium · the skip is limited to "the machine never let the sample be seeded and confirmed"; a confirmed-held sample our reader does not return still FAILs — both arms proven with a patched `_ps`

## Conventions honored

- synthetic boards only (`tmp_path`; the PRES-C oracle board and its notes overlay); English artifacts, code and UI; the operator's name nowhere (`username_subject` is the fixture's placeholder)
- no push, no merge, no reset, no force; commits end with the commission's co-author line; own paths staged by name

## Out-of-scope carries

- the OPERATOR and DECLINE rows of the inventory above — recorded in `BACKLOG.md` at the close
- the three PROTOTYPE items' implementation — after the operator's verdict on `prototypes/backlog_polish/`

## Gate notices and runtime absences

**Runtime absences (`SKILL.md` gate step 5), named once:** no slash commands, no hooks of the flow's own, no operator prompt (the standing authorization stands in at every gate); reviewer roles run as spawned agents carrying their `agents/<role>.md` role. `V15`, `V16`, `V17`: `not-run` — no canon tree, checkout table or flow hook from a bundle. `/dev-flow-sync`: `not-run` — no deployment record in a bundle install.

**Step 1 (on `main`):** 0 block · 40 notice — `V9` ×13 (old packets' source counts), `V13` ×8, `V22` ×5, `V23` ×1, `V42` ×9, `V53` ×1 (historical, over closed batches), `V30` (bundle run), `V57` ×2 (2026-10-18-batch-01's close record predates `9e82b10` by 1 commit; the tree dirty with the files found before the batch).

**P0 (step 3, after the rollover):** 0 block · 62 notice — the step-3 placeholder NOTICEs (`V27`, `V31`–`V34`, `V36`–`V38`, `V41`, `V43`–`V51`, `V54`) over the unfilled seeds; `V30`; the historical NOTICEs above unchanged.

**ARQ … PDR gates:** 0 block at every gate. `V62` between each `--station` move and this plan's rewrite (P1 after the iterate) — cleared here. `V23` on the seeded design records' template placeholders (`PDR-<batch_id>`, `PDR-…#D1`) and on the design proposal's preamble (`PDR-<batch_id>#D<n>`, the template's own grammar line) — the DDR record's leave when it is filled; the preamble line stays (template text). `V53` on `tests/test_app.py::_clipboard_roundtrip` (named by LLR-1902.1 before increment 001 writes it). **The PDR panel was one spawned agent applying the architect, qa-reviewer and ux-reviewer role files in turn** — the three lenses were not independent of each other (the P2 and ARQ lenses were separate agents); recorded in the PDR record's Participants.

**P3 (increment 001 gate):** 0 block from the packet; `V2` BLOCKs for AT-1903, AT-1904, AT-1905 — the station-expected red of `commands/dev-flow.md` §*Two-layer validation model* (their nodes land with increments 002 and 003); `V27` until the increment's decision; `V53` cleared (`_clipboard_roundtrip` now on disk).

**DDR / P4:** the architect's DDR lens returned `approved with conditions` (DDR-C1: PC-5's `not exercised` is no discharge); the round gained the notice capture after increment 003's review — `prototypes/backlog_polish/capture.py`, `build_html.py`, the page, `out/manifest.json` and `out/narrow-current-narrow-30x12-x.{svg,png}`, `doc`/`generated` rows added to packet 003 (no product code; `p3-implementation.md`'s one exception to the review order is for the close, so this is declared here instead); the DDR sealed `approved`.

**P4 / P5:** `V47`–`V49` cleared with `04-validation.md`; at close step 5 `V57` (the `Gated tree` placeholder) and at the final gate `V57` (the record predates the tree by 1 commit) — both expected by the runbook. `V2` cleared once AT-1903..1905 existed. **Gate notices at the close:** declared in this section.

**Found before the batch:** tracked and modified — `.gitattributes`, `.dev-flow/2026-10-07-batch-0{8,9}/evidence/inc001-brief.md` (line endings only); untracked — `.dev-flow/2026-10-07-batch-0{5..8}/decisions-log.json`, `.dev-flow/2026-10-07-batch-06/evidence/{gen_verdict_sheet.py,kanban-demo.json,veredicto-batch06.html,veredicto-board.json}`, `.dev-flow/rollover_batch{g,h,i,j}.py`. Not touched.

## Test ledger

| Suite / command | Last run | Result |
|---|---|---|
| `python -m pytest -q -p no:cacheprovider tests/test_team_views.py` on `backlog-fixes` = `9e82b10` | 2026-10-18 | 2 failed, 251 passed — the 2 standup failures |
| full suite after increment 001, working tree (`evidence/suite-001.txt`) | 2026-10-18 | 0 failed, 2733 passed — `test_win_clipboard_roundtrip` passed |
| full suite after increment 002, working tree (`evidence/suite-002.txt`, run 2) | 2026-10-18 | 0 failed, 2739 passed; run 1 (`suite-002-run1.txt`) 1 failed — a HelpModal paint-timing flake, 5/5 green alone (`flake-002.txt`) |
| full suite after increment 003, working tree (`evidence/suite-003.txt`) | 2026-10-18 | 0 failed, 2740 passed — `test_win_clipboard_roundtrip` passed |
| P4 gate run in a clean worktree at `7e849dc` (`evidence/suite-p4.txt`) | 2026-10-18 | 0 failed, 2740 passed, 0 skipped — `test_win_clipboard_roundtrip` passed |
