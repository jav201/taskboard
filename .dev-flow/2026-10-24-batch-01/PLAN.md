# PLAN — taskboard — Batch 2026-10-24-batch-01

## Header

| Field | Value |
|---|---|
| Project | taskboard |
| Batch | 2026-10-24-batch-01 |
| Objective | Milestone marks per the operator's verdict on prototypes/milestone_marks: one class directory for all boards at ~/.taskboard/marks.json (a class is id, name, shape, colour, hidden; the id a slug of the name, stable on rename); Task.mark carrying the class id, written only when set, kept on untick, travelling unchanged on team sync, an unknown id rendering as unclassified; every milestone mark drawn through one seat (shape and colour say the class, state moves to text: a late date in over plus an ▲Nd chip, a reached mark hollow plus ✓, an unclassified mark ◆ in mut); the # class manager window with its form (n) and the hide toggle (space); alt+m focusing the class Select in the editor after #f-milestone; the legend strip under the gantt ruler and in the presentation with its exports, naming the drawn classes and the hidden count; hidden classes leaving the gantt and all three presentation views and their exports; /#cls search filtering by class; modal keys y/n and alt+<letter> on every modal button; SHAPES = ▲ ■ ⬢ ★ ⬟ ▼ ✦ ⚑ plus ◆, no seeded classes |
| Last updated | P3 · 2026-10-24 |
| Standing authorization | standing authorization — the orchestrator's commission of 2026-10-24 (the runtime cannot prompt), relaying the operator's verdict on the milestone-marks round, verbatim: «D1: B · D2: global (recomendada, sin marcar) · 1 model: B · 2 editor: A (recomendada, sin marcar) · 3 legend: B · 4 filter: B · notes: (none)». Quoted from the commission (`prototypes/milestone_marks/IMPLEMENTATION.md` and the batch brief): «The plan header's Standing authorization cell quotes the commission's verdict. Gates close under that authorization. Do NOT push or merge.», «The design oracle is prototypes/milestone_marks/proto.py together with the captures in prototypes/milestone_marks/out/.», «Port these into the real app.», «Route them all through ONE seat, for example views.milestone_mark(task, board, today) -> (glyph, style, late_chip)», «At most 4 SOURCE files per increment. Tests are uncapped.», «Run env -u NO_COLOR for every pytest», «the full suite only at P4: 3 SEQUENTIAL chunks (baseline 3152 passed) … 0 failed and 0 skipped», «Mutation-check every new test.», «spawn independent agents … one reviewer agent per role at each gate: architect, code-reviewer, qa-reviewer, ux-reviewer, and security-reviewer for marks.py … An author never reviews their own work.», «one agent for the captures, after the code is final», «Every window you open has a unique m01- title and is closed by title right after its shot … Never close any other window … assert that no m01-* window remains.», «Never commit or print secrets. Never write the operator's real name; the placeholder is username_subject. Use synthetic data only.», «End every commit message with: Co-Authored-By: Kimi (kimi-for-coding) via Claude Opus 5.5 orchestration <noreply@anthropic.com>». Read as: every gate of this batch is autonomous (reviewer roles are spawned sub-agents carrying their `agents/<role>.md`); commits on the local branch `feat/milestone-marks` are authorized, each ending with the commission's co-author line; **push and merge are NOT authorized**; synthetic data only; the operator's name nowhere (`username_subject`); tests never touch the real home; scratch lives in `.scratch/` and is deleted at close. |
| First gate | step 1, on `7e66e0e` (`feat/milestone-marks` = `proto/milestone-marks` `8c83395` + the commission `7e66e0e`, on `main` `ffb567d`), before the rollover: exit 1 — 73 block · 138 notice · 61 not applicable, every BLOCK `V59` naming a file of the two prototype commits after the closed batch's `base_ref` `eac7d422` (the round's `prototypes/milestone_marks/`), which no closed packet carries; `V7`: bundle identical to its manifest both directions, 57 declared files, `2026-10-12-rev102` (`evidence/gate-step1.txt`). The rollover re-stamps `base_ref` to `7e66e0e`; step 3 (after it): exit 0 — 0 block · 158 notice · 47 not applicable (`evidence/gate-step3.txt`). |
| Premises / RC-1 | RC-1 (a): `git fetch origin` → `origin/main` = `ffb567d732d476a66018324fc0875541f75027d5`, the merge-base of `feat/milestone-marks` and `origin/main`; the branch is the round on top of that tip, so no rebase; `base_ref` stamped `7e66e0e5cab9a383ac10a37d31dc796984711a47`. RC-1 (b): not already shipped — on `origin/main` no `marks.json`, no `legend_strip`/`milestone_mark`, no `Task.mark` field (only incidental words). RC-2: `git ls-remote --exit-code --heads origin` → exit 0; newest commit on `origin/main` 2026-10-21 14:08 −0600. Premises: `01-requirements.md` §2.7 (P-1.., `evidence/premises.txt`). |

## Triggers

The trigger evaluation `state.json`'s `triggers.record` points at: one row per trigger evaluated, fired or not.

| Id | Verdict | Probe output |
|---|---|---|
| A1 | fired | judged — a new module `taskboard/marks.py` in the `models` layer and a new file in the home (`marks.json`): `docs/ARCHITECTURE.md` gains rows (the ARQ amendment) |
| A2 | fired | judged — the planned source files span `models` (`marks.py`, `models.py`), `app`, `views`, `modals`, `keymap` |
| A3 | fired | judged — new interfaces consumed across modules: `marks.*` (by `app`, `views`, `modals`), `Task.mark`, `Board._to_dict`'s field, `views.milestone_mark` (the seat), the editor Select and the `#` manager |
| A4 | not fired | judged — one lane, increments in order |
| B1 | fired | `git grep -l` over `tests/` on `7e66e0e`: `TaskModal\|#f-milestone` → `test_app.py`, `test_edit_window.py`, `test_emoji_picker.py`, `test_milestones.py`, `test_modal_keys.py`, `test_tick_label.py`; `milestone` → `test_agenda.py`, `test_all_agenda.py`, `test_gantt_board.py`, `test_gantt_polish.py`, `test_milestones.py`, `test_present_views.py`, `test_report.py`, `test_swimlanes.py` and more; `KEYMAP` → `test_app.py`, `test_archive.py`, `test_boards_home.py`, `test_dependencies.py`, `test_help_keys.py`, `test_keymap.py`, `test_legend.py`, `test_modal_keys.py`, `test_readme.py`; `filter_bar\|matches(\|filtered_board\|action_search` → `test_app.py`, `test_colour_budget_app.py`, `test_gantt_board.py`, `test_gantt_polish.py`, `test_kanban_readable.py`, `test_milestones.py`; `legend` → `test_legend.py`, `test_present_views.py`; `_to_dict` → `test_boards_home.py`, `test_tick_label.py` |
| B2 | not fired | judged — no file changes its location |
| B3 | not fired | `ls tests/goldens` → no such directory |
| B4 | fired | judged — `~/.taskboard/marks.json` (read by every later start and by another window), `marks.json.lock`, `marks.json.corrupt`; the presentation's exports consume the legend strip |
| C1, C2, C4, C5, C7 | not fired | judged — no auth, secret, sensitive third-party data, destructive DB or network surface: `marks.json` stores only the user's own class labels (names, shapes, colours) |
| C3 | not fired | judged — no external integration; the corrupt copy only adds a file |
| C6 | fired | judged — `marks.json` read as input at start; the manager form's fields; `/#cls` search input |
| C8 | fired | judged — new screens draw directory and board text (class names, the legend, titles); each a plain Text piece |
| D1 | fired | judged — every item alters what the operator sees or touches; `ux-reviewer` joins P2, the PDR and the DDR |
| D2 | not fired | judged — the round's prototype is the real `TaskboardApp` with subclasses and new screens, the target's own technology |
| E1 | fired | 4 increments (001..004) and 7 acceptance tests (AT-a..AT-g) |
| E2 | not fired | judged — no high risk at intake; the board file gains only an optional field written when set (bytes preserved when unset), no format break |
| E3 | not fired | judged — internal tool, no client deliverable |
| F1 | not fired | `V7`: bundle identical to the manifest at `2026-10-12-rev102` (a bundle cannot recompute `flow_hash`) |
| F2 | not fired | judged — `BACKLOG.md` was refreshed at 2026-10-21-batch-01's close |

## Where we are

The batch is CLOSED (2026-10-24). All stations green: P0, ARQ, P1, P2, PDR, the four increments (001 `f363a75`, 002 `6fc2637`, 003 `12b7a11`, 004 `1cae9c6`), the captures (`d3516d4`), the DDR (`512813d` — one condition discharged in the artifact, re-read by the same role), Phase 4 (`4a12f07` — the full suite in three sequential chunks, qa-reviewer PASS-WITH-NOTES) and the close (this PLAN's fold, `05-close.md`, the BACKLOG section, the final validator). The commission's "0 failed and 0 skipped" holds except one environmental skip (TC-1902's designed machine-refusal arm — the machine's clipboard broken OS-wide at gate time, G-001 in `04-validation.md`, probe persisted; the operator decides). No push, no merge.

## Objective

Port the round's chosen variants into the app — the store and the field (MM-D2, D3, D4), the encoding through one seat (MM-D1, section 3), the editor Select and the `#` manager (MM-D5, D6 storage, D8), the legend, hide, `/#` search, help and README (MM-D6, D7) — with the accepted costs of D1 and the ▲ ambiguity of D5 logged.

## Per-story / per-station status

| Story / station | Status | Notes |
|---|---|---|
| increment 001 | done | the store and the field (MM-D2, D3, D4): `taskboard/marks.py` (new), `taskboard/models.py`, `taskboard/app.py` |
| increment 002 | done | 6fc2637, code-reviewer OK (F1-F4 folded, re-read verified) the encoding through one seat (MM-D1, section 3): `taskboard/views.py`, `taskboard/app.py` |
| increment 003 | done | 12b7a11, code-reviewer approved (F1 folded as LED .46, discharged); a mishap reverted modals.py and the implementer regenerated it byte-equivalent | the editor Select and the `#` manager (MM-D5, D6 storage, D8): `taskboard/modals.py`, `taskboard/keymap.py`, `taskboard/app.py`, `taskboard/tcss` |
| increment 004 | done | 1cae9c6, code-reviewer PASS; all seven ATs minted; the 14 captures `d3516d4` | the legend, hide, search, help, README (MM-D6, D7): `taskboard/views.py`, `taskboard/app.py`, `README.md` |
| P0 | done | triggers evaluated; refinement done |
| P3 | done | increments 001 (f363a75) 002 (6fc2637) 003 (12b7a11) 004 (1cae9c6) committed, each code-review PASS; the 14 captures committed (d3516d4) |
| ARQ | approved with conditions | A-1 folded as D-4 (`render_marks` in 002; the map amended) |
| P1 | approved | 8 HLRs, 17 LLRs, 7 ATs, 8 premises TRUE, the IFC, scan answered (LED .1-.25 + .26-.45 at P2) |
| P2 | approved | three iterations; 5 majors + 22 minors folded (LED .26-.45); the last pass clean (`02-review.md`) |
| PDR | approved with conditions | PC-1..PC-5 folded at seal, none open; COLOURS=SWATCH; `_gantt_legend` seat; `_hide` proxy (`design/PDR-2026-10-24-batch-01.md`) |
| DDR | approved with conditions → all discharged | three independent roles (architect, qa-reviewer, ux-reviewer); no HIGH; C-1 discharged by amendment D-5 and re-read by the same role (final APPROVE); the +84 ledger reconciles exactly; the modals.py regeneration verified (`design/DDR-2026-10-24-batch-01.md`, `512813d`) |
| P4 | PASS-WITH-NOTES | the full suite in three sequential chunks on 512813d: 3235 passed + 1 environmental skip (TC-1902, G-001) = 3236; qa-reviewer evaluated, its three corrections folded (`04-validation.md`, `4a12f07`) |

## Roadmap + increment plan

- 001 — the store and the field (MM-D2, D3, D4): `taskboard/marks.py` (new), `taskboard/models.py`, `taskboard/app.py` (`__main__.py` only if needed). 3 source files.
- 002 — the encoding through one seat (MM-D1, section 3), every view and `app.py`'s notices, plus the `#` manager's pure render `views.render_marks` (the ARQ's A-1 fold): `taskboard/views.py`, `taskboard/app.py`. 2 source files.
- 003 — the editor Select (verdict 2 A) and the `#` manager with its form and hide toggle (MM-D5, D6 storage, D8): `taskboard/modals.py`, `taskboard/keymap.py`, `taskboard/app.py`, `taskboard.tcss`. 4 source files.
- 004 — the legend strip (MM-D7) in the gantt, presentation and exports; hidden classes leave the gantt and presentation (MM-D6); `/#…` search; the `?` help, details line and README: `taskboard/views.py`, `taskboard/app.py`, `README.md`. 3 source files.

## Key decisions

| Date | Decision | Why |
|---|---|---|
| 2026-10-24 | D-1 — the rollover by script with `devflow-init.py`'s own seed helpers (`evidence/rollover.py`, the 2026-10-21-batch-01 pattern), `ROOT` checked to be this worktree before it ran; `owner` this worktree | the commission's worktree; `V40` |
| 2026-10-24 | D-2 — triggers A1 A2 A3 B1 B4 C6 C8 D1 E1 fire (ARQ, PDR, DDR up); C3 does not fire: `marks.json` holds only the user's own class labels, no third-party personal data | the trigger probes; unlike the people round there is no personal data |
| 2026-10-24 | D-3 — four sequential increments exactly as the commission tables them (001→004), at most 4 source files each, tests uncapped | the commission |
| 2026-10-24 | D-4 — the ARQ's A-1 fold: the `#` manager's frame is a pure render `views.render_marks(directory, sel, w, h)` shipped in increment 002 (a file it already owns, still 2 source files), so the manager in 003 keeps the people view's pattern without exceeding the cap; the commission's increment table is untouched — its source files are «expected», and the re-cut is recorded here and in the map | the spawned architect's A-1 (A-1a); `docs/ARCHITECTURE.md` |

## Risks / watch-items

- two windows add a class at once · low · the lock and the re-read (AT-c)
- a class colour resembling a project colour · accepted · MM-D1's recorded cost
- an unclassified milestone loses its red mark; the gantt month ruler shows no lateness · accepted · MM-D1's recorded costs
- `▲` as a class glyph beside the `▲Nd` late chip and the `▲N ◆` fold row · accepted, logged · MM-D5
- a teammate's unknown class id · low · renders unclassified, the id kept (AT-g)

## Conventions honored

- synthetic data only (the round's fixture boards and its four example classes live only in test fixtures and captures); English artifacts, code and UI; the operator's name nowhere (`username_subject`)
- no push, no merge, no reset of shared state, no force; commits end with the commission's co-author line; own paths staged by name
- no test touches the real home (the conftest seam)
- the full suite in three sequential chunks, `NO_COLOR` unset; captures in unique `m01-` windows only

## Out-of-scope carries

- `▲`'s ambiguity with the late chip and the fold row (MM-D5's log ruling) → `BACKLOG.md` at the close
- the gantt month ruler's lateness, the unclassified milestone's red mark, the class/project colour resemblance (MM-D1's accepted costs) — recorded, not fixed

## Gate notices and runtime absences

**Runtime absences (`SKILL.md` gate step 5), named once:** no slash commands, no hooks of the flow's own, no operator prompt (the standing authorization stands in at every gate); reviewer roles run as spawned agents carrying their `agents/<role>.md` role. `V15`, `V16`, `V17`: `not-run` — no canon tree, checkout table or flow hook from a bundle. `/dev-flow-sync`: `not-run` — no deployment record in a bundle install.

**Step 1:** exit 1 on `7e66e0e` before the rollover — 73 `V59` BLOCKs over the two prototype commits after the closed batch's `base_ref` `eac7d422`, cleared by the rollover's re-stamp; the NOTICEs historical over closed batches (`V9`, `V13`, `V23`, `V42`, `V53`), `V30` (the bundle run).

**Step 3 (batch open):** exit 0 — 0 block · 158 notice · 47 not applicable (`evidence/gate-step3.txt`). Expected seed NOTICEs per the runbook's table: `V9`, `V27`, `V31`–`V38`, `V41`, `V43`–`V51`, `V54` over the seeded placeholders (each leaves when its row fills); `V30` at every gate from a bundle; `V53` over the closed records (371 resolved anchors, 4 self-file misses, 2 no-file — historical, declared); `V23` design citations inside the closed 2026-10-21 batch (historical, declared); `V42` deferral markers in closed batches (historical, declared); `V27` leaves with the first dated `--decision`. No `V25` — this tree has an `origin` remote.

## Test ledger

| Suite / command | Last run | Result |
|---|---|---|
| validator `--brief` (step 3) | 2026-10-24 | 0 block · 158 notice · 47 n/a (`evidence/gate-step3.txt`) |
| validator `--brief` (P1) | 2026-10-24 | 0 block · 171 notice · 48 n/a |
| P4 chunk 00 (40 files, `suite-p4-chunk00.txt`) | 2026-10-24 | 1258 passed · 1 skipped (TC-1902 environmental, G-001) · exit 0 |
| P4 chunk 01 (39 files, `suite-p4-chunk01.txt`) | 2026-10-24 | 1071 passed · 0 failed · 0 skipped · exit 0 |
| P4 chunk 02 (39 files, `suite-p4-chunk02.txt`) | 2026-10-24 | 906 passed · 0 failed · 0 skipped · exit 0 |
| P4 total | 2026-10-24 | 3235 passed + 1 environmental skip = 3236 collected = 3152 + 84 · qa-reviewer PASS-WITH-NOTES |

**P3 (increment gates):** `V2` BLOCKs for `AT-2603`/`AT-2604`/`AT-2605`/`AT-2606` stand from increment 001's gate until their increments land their nodes — the station-expected red of `commands/dev-flow.md` §Two-layer validation model read through the PDR's AT-realisation map (AT-2603 → 002, AT-2604 → 003, AT-2605/AT-2606 → 004); walked past at 001's gate, expected green from increment 004's gate onward and at every gate after.
