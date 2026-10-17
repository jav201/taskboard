# PLAN — taskboard — Batch 2026-10-17-batch-01

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
| Batch | 2026-10-17-batch-01 |
| Objective | Gantt tick label: remove the scale label (e.g. 'Mondays · 1 day = 2 cells') everywhere it is painted; the gantt view's tick-row label follows the presentation's rule (selected task ▸ / the echo's own text / selected: no dates / blank), and the presentation's no-selection fallback becomes blank |
| Last updated | P3 · 2026-10-17 |
| Standing authorization | standing authorization — the operator's commission, 2026-10-17 (Spanish, quoted): «Es la etiqueta de Mondays y cells? Si es así, hay que quitarla. No agrega valor» — referring to the scale label `_gantt_scale_label(...)` (e.g. `Mondays · 1 day = 2 cells`) left of the tick row in the gantt view (`taskboard/views.py` ~3001–3006) and the presentation (`_present_ruler`, ~6222–6227). The coordinator relayed the commission with its decisions (scale label removed everywhere; the gantt view's tick label follows the presentation's rule; the presentation's no-cursor fallback becomes blank; `_gantt_scale_label` deleted if nothing else calls it; no prototype round). Read as: every gate of this batch is autonomous (the runtime cannot prompt; reviewer roles are spawned sub-agents); commits on the local branch `gantt-tick-label` are authorized; **push, merge, reset and force are NOT authorized**; synthetic boards only; at most 4 source files per increment. |
| First gate | step 1, on `main` `d79a33e` before the branch: exit 0 — 0 block · 40 notice · 65 not applicable; `V7`: bundle identical to its manifest both directions, 57 declared files, `2026-10-12-rev102`. Step 3 (after the rollover): exit 0 — 0 block · 62 notice. |
| Premises / RC-1 | RC-1 (a): `git fetch origin` → `origin/main` = `d79a33e51d2d7509a9ff5d64b9098027665d7d72` = local `main`; `git switch -c gantt-tick-label main`, `git rebase --autostash origin/main` → `up to date`; `base_ref` = `d79a33e`. RC-1 (b): not already shipped — `git grep -n "_gantt_scale_label" origin/main -- taskboard` → `views.py:2849` (def), `:3005` (the gantt view's tick label), `:6230` (the presentation's no-cursor fallback). RC-2: `git ls-remote --exit-code --heads origin` → exit 0; newest `origin/main` commit 2026-10-17 09:09 -0600. Premises P-1..P-4: `01-requirements.md` §2.7. |

## Triggers

The trigger evaluation `state.json`'s `triggers.record` points at: one row per trigger evaluated, fired or not.

| Id | Verdict | Probe output |
|---|---|---|
| A1 | not fired | judged — `docs/ARCHITECTURE.md` · no module created, no boundary moved: the change is inside `taskboard/views.py` |
| A2 | not fired | judged — one source module planned (`taskboard/views.py`); the rest are tests |
| A3 | not fired | judged — `_gantt_scale_label` is private; `git grep -n _gantt_scale_label -- taskboard` → `views.py` only (def + 2 calls); `gantt_day_row`'s signature and `meta` are unchanged |
| A4 | not fired | judged — one lane, one increment |
| B1 | fired | `grep -rl "_gantt_scale_label\|d/cell\|1 cell = 1 day\|1 day = 2 cells" tests/` → `test_gantt_board.py` (AT-104, TC-110: batch 2026-10-02-batch-01), `test_present_rulers.py` (TC-1601), `test_present_room.py` (TC-1608 (c): batch 2026-10-16-batch-01) |
| B2 | not fired | no file moves |
| B3 | fired | `ls tests/goldens` → no such directory; but `views.py` is captured byte-for-byte by the PRES-R2 frames (`tests/test_present.py` TC-1001/TC-1002) and the C-2b frames (`tests/test_chainmap.py`); `grep -l "cell" .dev-flow/2026-10-16-batch-01/evidence/frames/PRES-R2-*` → none (both frames have a cursor), so no drift is expected — named in the census |
| B4 | fired | judged — the presentation's `x` export (SVG/PNG) carries the frame, so a frame with no selection exports a blank label; TC-1701 reads the SVG |
| C1–C7 | not fired | `devflow-scan-spec.py` over `01-requirements.md` (P1) — recorded there; no auth, secret, external integration, sensitive data, DB, network or new input surface |
| C8 | not fired | judged — the new label text is fixed strings and `gantt_echo`'s date text (formatted dates); no board-file text enters it |
| D1 | fired | judged — the tick row's label is what the user sees |
| D2 | not fired | judged — no prototype round (coordinator's decision); the evidence is the real app |
| E1 | not fired | 1 story, 1 increment |
| E2 | not fired | judged — a removal, low risk |
| E3 | not fired | judged — internal tool |
| F1 | not fired | `V7`: bundle identical to its manifest at `2026-10-12-rev102` |
| F2 | not fired | judged — `BACKLOG.md` was refreshed at batch 2026-10-16-batch-01's close (`d79a33e`) |

## Where we are

P3 — P0 closed (`3cde009`); P1 contract (1 US, 1 HLR, 1 LLR; AT-1701, TC-1701); P2 iteration 1 `iterate-to-refine` → LED .2; P2 iteration 2 `approve` (architect, qa-reviewer, ux-reviewer), minors folded in LED .3. Next: increment 001 — the helper, the deleted scale label, TC-1701/AT-1701 in `tests/test_tick_label.py`, the law-driven updates to five pinned tests (QA2-1 included), RED, mutants, `code-reviewer`.

## Objective

The tick row's label never shows the scale text; in both views it names the selected task (or carries the echo's own dates, or says the task has none) and is blank with nothing selected.

## Per-story / per-station status

| Story / station | Status | Notes |
|---|---|---|
| US-1701 | READY → P3 | P2 approved (iteration 2) |
| P2 | approve | `02-review.md` (2 iterations) |

## Roadmap + increment plan

- 001 — one tick-label rule for both views; `_gantt_scale_label` deleted; pinned tests updated law-driven (AT-104, TC-110 deleted, TC-1601, TC-1608 (c), the dead-cell law); TC-1701 / AT-1701 in `tests/test_tick_label.py`: 1 source file (`taskboard/views.py`).

## Key decisions

| Date | Decision | Why |
|---|---|---|
| 2026-10-17 | branch `gantt-tick-label` from `main` (= `origin/main` `d79a33e`) | the commission |
| 2026-10-17 | the scale label is removed everywhere it is painted | operator: «hay que quitarla. No agrega valor» |
| 2026-10-17 | the gantt view's tick label follows the rule the presentation ships (inc 004 of 2026-10-16-batch-01): `selected task ▸` (echo tone, bold) when the echo fits; the echo's full text + ` ▸` when it does not; `selected: no dates` (dim) for a dateless selection; blank with no selection | coordinator: the operator judged the scale text worthless, and one rule in both views avoids two dialects |
| 2026-10-17 | the presentation's no-cursor fallback becomes blank | coordinator's decision, same reason |
| 2026-10-17 | `_gantt_scale_label` is deleted with its test (TC-110) | coordinator: delete it if nothing else calls it — `git grep` finds only the two painting sites |
| 2026-10-17 | no prototype round | coordinator: a removal the operator decided directly; the visible result is shown by real-app captures |
| 2026-10-17 | both sites call one helper, `_gantt_tick_label` | one rule in code too, so the two views cannot drift into two dialects again |
| 2026-10-17 | the evidence home's `-text` mark is a nested `evidence/.gitattributes` (`** -text`), not a line in the root `.gitattributes` | the root `.gitattributes` is a pre-existing dirty file the commission says to leave alone; `git check-attr text` on a path in the home → `unset` |
| 2026-10-17 | P2 iteration 1 → `iterate-to-refine`; amended in LED-2026-10-17-batch-01.2 | 1 blocker (QA-1: the AT's selection states not reachable as written) and 8 requirement-defect majors; a requirement defect goes back to P1 (`stations/p2-review.md` §Gate) |
| 2026-10-17 | P2 iteration 2 → `approve`; minors in LED .3; QA2-1 carried into increment 001 | all three lenses approve; every remaining item a minor fix changing no obligation (`stations/p2-review.md` §Gate, the commission reads as autonomy over the gate) |
| 2026-10-17 | the dead-cell law (`tests/test_gantt.py:287`) is rebaselined to `<= 25.5` = 25 + 100·15/2880 | the 15 cells are the ink of the scale text the operator removed (base 24.58 %, patched 25.10 %); derived from the rule, not the new measurement (qa-reviewer, architect) |
| 2026-10-17 | the README hero image (`docs/taskboard-gantt.svg`, `Mondays · 1 d/cell`) stays out of scope, carried to `BACKLOG.md` | a static file generated by 2026-10-02-batch-01's `make_readme_gantt.py`, not painted by the app; regenerating it re-renders every change since then — a docs change outside the commission (architect A-3) |
| 2026-10-17 | asked at the gate — the operator's verdict on batch 2026-10-16-batch-01's captures, relayed by the coordinator: «Ya vi las capturas, se ven todo en orden.» (including `app-004-80x25-present-open.svg`) approves the 80-column Present frame and the increment-004 captures; it discharges that batch's backlog item "the operator's visual verdict on the 80-column oracle frame" (marked resolved in `BACKLOG.md`; batch-01's closed records untouched) | the operator reviewed the captures |

## Risks / watch-items

- the gantt view's label column is narrower below 60 columns (`max(6, width // 3)`), so `selected task ▸` is cut with `…` there · certain below 48 columns · the same `fit` the presentation uses; named in LLR-1701.1
- pinned tests of earlier batches assert the scale text (B1) · certain · updated law-driven and named in the packet

## Conventions honored

- synthetic boards only (`tmp_path`, `kg_board`, `present_board`); English artifacts, code and UI; no personal names (placeholder `username_subject`)
- no push, merge, reset or force; commits end with the commission's co-author line; only this batch's paths staged

## Out-of-scope carries

- the presentation ruler's repeated layout lines (backlog: code review F3 of 2026-10-16-batch-01) — only the label rule is shared here
- the operator's approval of `selected: no dates` (backlog item of 2026-10-16-batch-01) — this batch reuses the shipped text; the item stays open

## Gate notices and runtime absences

**Runtime absences (`SKILL.md` gate step 5), named once:** no slash commands, no hooks of the flow's own, no operator prompt (the standing authorization stands in at every gate); reviewer roles run as spawned generic sub-agents carrying `agents/<role>.md` (`spawned — generic agent with agents/<role>.md`). `V15`, `V16`, `V17`: `not-run` — no canon tree, checkout table or flow hook from a bundle. `/dev-flow-sync`: `not-run` — no deployment record in a bundle install.

**Step 1 (before the batch):** 0 block · 40 notice — historical NOTICEs over closed batches (`V9` on old packets, `V13`, `V22`, `V23` on `.dev-flow/03-increments/increment-006.md`, `V42` on batch 2026-10-02-batch-03 and on 2026-10-16-batch-01's `HANDOFF.md:81` / `increment-004.md:93`, `V53` the closed-record census), `V30` (bundle run), `V57` on 2026-10-16-batch-01's close (1 commit after it; the pre-existing dirty files).

**Step 3 / P0:** 0 block · 62 notice — the step-3 placeholder NOTICEs (`V27`, `V31`–`V34`, `V36`–`V38`, `V41`, `V43`–`V51`, `V54`) over the unfilled seeds, leaving as rows fill them; the historical NOTICEs above; `V30`. `V25` does not apply (origin exists).

**P1 gate:** 0 block · 57 notice — the step-3 placeholders still unfilled at P1 (`V31`, `V32`, `V36`–`V38`, `V41`, `V43`, `V44`, `V47`–`V51`, `V54` on the packet, validation and close seeds), the historical NOTICEs, `V30`; `V62` at the P1 gate until this rewrite.

**P2 iteration 1 → P1 (LED .2) gate:** 0 block · 57 notice — as at P1; `V62` until the plan named P1/P2.

**P2 gate (iteration 2):** 0 block · 56 notice — the remaining step-3 placeholders (packet, validation, close seeds), the historical NOTICEs, `V30`.

**Found before the batch:** `.gitattributes`, `.dev-flow/2026-10-07-batch-0{8,9}/evidence/inc001-brief.md` (modified), untracked `.dev-flow/2026-10-07-batch-0{5..8}/decisions-log.json`, `.dev-flow/2026-10-07-batch-06/evidence/{gen_verdict_sheet.py,kanban-demo.json,veredicto-batch06.html,veredicto-board.json}`, `.dev-flow/rollover_batch{g,h,i,j}.py`. Not touched.

## Test ledger

| Suite / command | Last run | Result |
|---|---|---|
| C-39 pre-execution: `python -m pytest -q -p no:cacheprovider` on the patched tree in a scratch worktree (no new tests) | 2026-10-17 | 8 failed, 2626 passed in 492.52s — the 2 standup base failures + `test_gantt_board.py::test_AT_104…`, `::test_TC_110…`, `test_present_room.py::test_TC_1608_no_selected…` ×2, `test_present_rulers.py::test_TC_1601…`, `test_gantt.py::test_emptiness_is_bounded…` (QA2-1) |
