# PLAN — taskboard — Batch 2026-10-18-batch-03

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
| Batch | 2026-10-18-batch-03 |
| Objective | Present polish (the operator's verdict of 2026-10-18 on the backlog polish round, variant A of all three items): the dim view word and the cut and edge marks of the presentation in the reached tone (~4.9:1) instead of dim (~3:1); a middle hint wording between the long and the short one, which the 80-column hint takes; the gantt view's cursor note filling the frame's free rows instead of stopping at 3 |
| Last updated | P5 · 2026-10-18 |
| Standing authorization | standing authorization — the coordinator's commission of 2026-10-18 (the runtime cannot prompt), relaying the operator's verdict of 2026-10-18: «Si, apruebo.» (variant A of all three items of `prototypes/backlog_polish/backlog-polish-prototype.html`). Quoted from the commission: «Open a NEW dev-flow batch in `C:\Users\jjgh8\Github\taskboard` … Create the local branch `present-polish` from main … follow `stations/core-runbook.md`», «Port each A faithfully from that round's code and captures», «No push, merge, reset or force», «At most 4 SOURCE files per increment», «Never rewrite oracle frames whose hashes are recorded; new frames go in new files», «An independent `code-reviewer` per increment», «Run P4 and the P5 close». Read as: every gate of this batch is autonomous (reviewer roles are spawned sub-agents); commits on the local branch `present-polish` are authorized, each ending with the commission's co-author line; **push and merge are NOT authorized**; synthetic data only; the operator's name nowhere (`username_subject`); no deletion is commissioned, so the round folder stays (§*Key decisions*). |
| First gate | step 1, on `main` `620f58c` before the branch: exit 0 — 0 block · 42 notice · 64 not applicable; `V7`: bundle identical to its manifest both directions, 57 declared files, `2026-10-12-rev102`. Step 3 (after the rollover): exit 0 — 0 block · 63 notice · 47 not applicable. |
| Premises / RC-1 | RC-1 (a): `git fetch origin` → `origin/main` = `620f58c787f855d4d2ad4942c79c5a7cecb55baa` = local `main`; `git switch -c present-polish main`; HEAD equals the origin tip, so no rebase is owed; `base_ref` = `620f58c787f855d4d2ad4942c79c5a7cecb55baa`. RC-1 (b): not already shipped — on `origin/main` the view word and the cut and edge marks are `dim` (`views.py:6243`, `:6244`, `:6277`, `:6511`), `_hint` holds no middle wording (`app.py:297-302`), the gantt note is cut at 3 rows (`views.py:6541`). RC-2: `git ls-remote --exit-code --heads origin` → exit 0; newest `origin/main` commit 2026-10-18 16:39 -0600. Premises: `01-requirements.md` §2.7. |

## Triggers

The trigger evaluation `state.json`'s `triggers.record` points at: one row per trigger evaluated, fired or not.

| Id | Verdict | Probe output |
|---|---|---|
| A1 | not fired | judged — `docs/ARCHITECTURE.md` §2 · no module created, no boundary moved: the planned source files (`taskboard/views.py`, `taskboard/app.py`) are existing modules'; the new test file sits under the declared `tests` module |
| A2 | fired | judged — the planned source files are `taskboard/views.py` (module `views`) and `taskboard/app.py` (module `app`): two modules |
| A3 | not fired | judged — `docs/ARCHITECTURE.md` §4 · no interface row changes shape: the `render_present` row's contract text gains the note fill and the `reached` marks (ARQ amendment), while its signature, its `height`×`width` frame for every width ≥ 0 and `Frozen? no` hold, and the only consumers byte-tied to the note's row count are tests (the PRES-V3 gantt-notes frames drift, B3) and frozen evidence; `_hint` and `_present_cut` are not interfaces (no row; `_present_cut` is read only by the frozen round, the `prototypes` row of §3) |
| A4 | not fired | judged — one lane, increments in order |
| B1 | fired | `grep -rl --include=*.py` over `tests/`: `render_present` → `test_markup_census.py`, `test_present.py`, `test_present_narrow.py`, `test_present_room.py`, `test_present_rulers.py`, `test_present_views.py`, `test_tick_label.py`; `_hint` → `test_present_hide.py`, `test_present_narrow.py`, `test_present_views_app.py` (and `test_gantt_polish.py`, `test_link_picker.py`: other screens' own `_hint`); `present-hint` → `test_present_hide.py`, `test_present_narrow.py`, `test_present_views_app.py`; `lines above` / `more lines` / `lines"` → `test_present_views.py`, `test_present_views_app.py`, `test_row_cost.py`; `_present_cut`, `_present_mark` → none |
| B2 | not fired | no file moves |
| B3 | fired | `ls tests/goldens` → no such directory; the byte oracles the presentation tests read are batch evidence: `PRES-V3-*` of 2026-10-18-batch-01 (plain text, read by `tests/test_present.py`, `tests/test_present_views.py`, `tests/test_present_views_app.py`) — the two `PRES-V3-gantt-notes-*` frames drift with HLR-2003 (the note fills the free rows), the others do not (tones are not in plain text); new frames `PRES-V4-gantt-notes-*` go in this batch's evidence, the PRES-V3 files stay |
| B4 | fired | judged — the presentation's `x` export writes the frame on screen (`save_present_svg` / `save_present_png` over `render_present`): the exported SVG carries the new tones and the filled note |
| C1–C7 | not fired | `devflow-scan-spec.py` over `01-requirements.md` (P1): `flags: none`, `security_required: false`, exit 0 |
| C8 | not fired | judged — no new markup site over board-file text: the gantt note's extra rows go through the shipped escaped `_present_note_markup`; the tones are fixed tone names; the hint is a Rich `Text` built with `append` |
| D1 | fired | judged — all three changes alter what the presenter sees; `ux-reviewer` joins P2 and the PDR |
| D2 | not fired | judged — the round ran the real Textual app headless (`export_screenshot`), the target technology |
| E1 | fired | 3 stories (US-2001..US-2003) and 3 planned increments |
| E2 | not fired | judged — no high risk declared: four tone sites, one wording, one row count |
| E3 | not fired | judged — internal tool, no client deliverable |
| F1 | not fired | `V7`: bundle identical to its manifest at `2026-10-12-rev102` |
| F2 | not fired | judged — `BACKLOG.md` was refreshed at 2026-10-18-batch-02's close (`c8e9c75`) |

## Where we are

Closed (P5, 2026-10-18) — ARQ approved after one iterate; P1/P2 approved after one iterate-to-refine; the PDR sealed approved with conditions (PC-1..PC-4) and the DDR approved (all discharged); increments 001 (`e72a316`), 002 (`b12e563`) and 003 (`984ba8e`) implemented, reviewed (code-reviewer OK, 0 HIGH) and committed; P4 PASS-WITH-NOTES (2759 passed, 0 failed); the canon folded; the batch is closed on the local branch `present-polish`, not pushed (the commission forbids a push).

## Objective

Ship variant A of the three polish items the operator approved — the quiet marks in `reached`, the middle hint wording, the gantt note filling its free rows — ported from the round's own code, with the real app's captures compared against the round's.

## Per-story / per-station status

| Story / station | Status | Notes |
|---|---|---|
| US-2001 | DONE | increment 001 · AT-2001 passes |
| US-2002 | DONE | increment 002 · AT-2002 passes |
| US-2003 | DONE | increment 003 · AT-2003 passes |
| P0 | done | triggers evaluated; refinement done |
| ARQ | approved | `docs/ARCHITECTURE.md` amended (one iterate: A-1..A-4 folded) |
| P1 | approved after one iterate-to-refine | LED .2, LED .3 folded |
| P2 | approved | iteration 1 iterate-to-refine (6 majors → LED .2, .3), iteration 2 approve (1 minor owed by increment 003) |
| PDR | approved with conditions | PC-1, PC-3, PC-4 at the seal; PC-2 harness at the seal, its TC-1904 tier at increment 002 |
| P3 | done | increments 001, 002, 003 committed |
| DDR | approved | architect approved; qa-reviewer C1/C2 discharged before the seal |
| P4 | PASS-WITH-NOTES | `04-validation.md`, gate run `evidence/suite-p4.txt` (2759 passed) |
| P5 | closed | `05-close.md` |

## Roadmap + increment plan

- 001 — the quiet marks in `reached`: `taskboard/views.py` (four tone literals); `tests/test_present_polish.py` (TC-2001, AT-2001). 1 source file.
- 002 — the middle hint wording: `taskboard/app.py` (`_hint`); `tests/test_present_polish.py` (TC-2002, AT-2002) and the law-driven updates of TC-1808, TC-1904 and the 80-column hint arm of `tests/test_present_hide.py`. 1 source file.
- 003 — the gantt note fills the free rows: `taskboard/views.py` (the cap; `render_present`'s docstring); `tests/test_present_polish.py` (TC-2003, AT-2003), TC-1807 re-pointed at the new `PRES-V4-gantt-notes-*` frames; `docs/ARCHITECTURE.md` (doc). 1 source file.

## Key decisions

| Date | Decision | Why |
|---|---|---|
| 2026-10-18 | branch `present-polish` from `main` `620f58c` = `origin/main`; no rebase | HEAD equals the origin tip |
| 2026-10-18 | rollover by script with `devflow-init.py`'s own seed helpers (the 2026-10-18-batch-02 pattern); the evidence home's `-text` mark is a per-directory `evidence/.gitattributes` | the root `.gitattributes` was dirty before the batch and the commission says to leave it alone |
| 2026-10-18 | the oracle for the port is the round's own code: its capture script re-run on `base_ref` in a scratch worktree, its variant-A forks composed cumulatively per increment, compared with the real app's captures on the branch (normalised SVG); the new oracle frames `PRES-V4-gantt-notes-*` are the round's `cap_fork("fill")` output on `base_ref` | «Port each A faithfully from that round's code and captures»: an oracle the port did not write; the round's own committed A captures check the re-run first (P-6) |
| 2026-10-18 | the round folder and `tests/test_backlog_polish_round.py` stay; their retirement (AT-1905's rule) goes to the operator in `BACKLOG.md` | the commission authorizes no deletion and the round is the comparison's oracle; deleting tracked deliverables the operator has seen is the operator's call — a declared deviation |
| 2026-10-18 | three increments, one per item, in the round's order | each item gets its own RED, mutants and review |

## Risks / watch-items

- the law-driven updates of shipped tests (TC-1807, TC-1808, TC-1904, TC-1604's hint arm) could hide a weakened assertion · medium · each is named in its packet's census with old → new, the new value taken from the round's measured design (P-3) or the round's own frames, never from the code under test
- the round's `capture.py` re-run on the branch would double-apply its forks · low · the round is frozen to its commit (`docs/ARCHITECTURE.md` §3); this batch re-runs it only on `base_ref`, and records that in the module map

## Conventions honored

- synthetic boards only (`tmp_path`; the notes board); English artifacts, code and UI; the operator's name nowhere
- no push, no merge, no reset, no force; commits end with the commission's co-author line; own paths staged by name

## Out-of-scope carries

- the OPERATOR rows of `BACKLOG.md`: the tick-row label `selected: no dates`, round 1's Slide view, page snapping and the scrolling headings — left open
- the round's retirement — handed to the operator

## Gate notices and runtime absences

**Runtime absences (`SKILL.md` gate step 5), named once:** no slash commands, no hooks of the flow's own, no operator prompt (the standing authorization stands in at every gate); reviewer roles run as spawned agents carrying their `agents/<role>.md` role. `V15`, `V16`, `V17`: `not-run` — no canon tree, checkout table or flow hook from a bundle. `/dev-flow-sync`: `not-run` — no deployment record in a bundle install.

**Step 1 (on `main`):** 0 block · 42 notice — `V9` ×13 (old packets' source counts), `V13` ×8, `V22` ×5, `V23` ×2, `V42` ×9, `V53` ×1, `V56` ×1 (historical, over closed batches; `V56` on 2026-10-18-batch-02's packet 003), `V30` (bundle run), `V57` ×2 (2026-10-18-batch-02's close record predates `620f58c` by 1 commit; the tree dirty with the files found before the batch).

**P0 (step 3, after the rollover):** 0 block · 63 notice — the step-3 placeholder NOTICEs (`V27`, `V31`–`V34`, `V36`–`V38`, `V41`, `V43`–`V51`, `V54`) over the unfilled seeds; `V30`; the historical NOTICEs above unchanged.

**Found before the batch:** tracked and modified — `.gitattributes`, `.dev-flow/2026-10-07-batch-0{8,9}/evidence/inc001-brief.md` (line endings only); untracked — `.dev-flow/2026-10-07-batch-0{5..8}/decisions-log.json`, `.dev-flow/2026-10-07-batch-06/evidence/{gen_verdict_sheet.py,kanban-demo.json,veredicto-batch06.html,veredicto-board.json}`, `.dev-flow/rollover_batch{g,h,i,j}.py`. Not touched.

## Test ledger

| Suite / command | Last run | Result |
|---|---|---|
| `python -m pytest -q -p no:cacheprovider -rs --color=no` on `base_ref` | 2026-10-18 | running — `evidence/suite-base.txt` |
