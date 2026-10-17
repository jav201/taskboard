# PLAN — taskboard — Batch 2026-10-16-batch-01

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
| Batch | 2026-10-16-batch-01 |
| Objective | Present view v2: a date ruler (variant B) and start-end chips on the R field, a per-task persisted 'show in presentation' flag (space hides, a shows all), and the ? help modal's Keys band plus a pinned global-keys line |
| Last updated | P5 · 2026-10-17 |
| Standing authorization | standing authorization — the operator's commission, 2026-10-16 (Spanish, quoted): «Que se guarde en la tarea, una bandera basta. … 2. Se ve mejor en acento … Arranca el batch» and «Ok, implementa la recomendación con los keys.» Verdict page `prototypes/present_rulers/present-rulers-prototype.html`: variant B + start–end chips + a persisted hide flag + the `?` legend fix. Read as: every gate of this batch is autonomous (the runtime cannot prompt; reviewer roles are spawned sub-agents); commits on the batch branch are authorized; **push is NOT authorized**; synthetic boards only; three increments as commissioned. |
| First gate | step 1, before rollover, on the stale local `main` (`e017ade`): exit 1 — 33 block (32 × `V59` naming the untracked `prototypes/present_rulers/**` files, which are this batch's prototype evidence and enter increment 001's §2; 1 × `V10` on the closed batch-09 contract's IFC placeholder, a record the rollover retires) · 39 notice; `V7`: bundle identical to its manifest both directions, 57 declared files, `2026-10-12-rev102`. After rollover on `origin/main`: 0 block · 59 notice. |
| Premises / RC-1 | RC-1 (a): `git fetch origin` → `origin/main` = `64443beeb1c0a9921b4969262bfecfd75ae0137d`; local `main` (`e017ade`) shares NO merge-base with it (`git merge-base` empty; `198 ahead / 199 behind`) — origin was rewritten 2026-10-11 to scrub personal names (every author `username_subject`); `git diff --stat HEAD origin/main -- taskboard` empty. A rebase across unrelated histories is not possible, so the batch branches from the origin tip: `git switch -c present-v2 origin/main`; `base_ref` = `64443be`; local `main` untouched. RC-1 (b): no story is already shipped — `git grep -n "show_in_present\|present_span_label\|global_keys" origin/main` → no hit. RC-2: `git ls-remote --exit-code --heads origin` answered (newest commit 2026-10-11). Premises P-1..P-5: `01-requirements.md` §2.7, all TRUE with executed evidence. |

## Triggers

The trigger evaluation `state.json`'s `triggers.record` points at: one row per trigger evaluated, fired or not.

| Id | Verdict | Probe output |
|---|---|---|
| A1 | not fired | judged — `docs/ARCHITECTURE.md` (seeded this batch) · no new module, no boundary moved: every planned file is an existing module's |
| A2 | fired | judged — the planned files are `views.py`, `app.py`, `models.py`, `modals.py`, `keymap.py`: five modules of the package |
| A3 | fired | judged — `Task` gains a field another module consumes (`app._on_task_edited`, `team_sync` push via `Board._to_dict`); `board.json` gains an optional key; `gantt_day_row` gains a keyword |
| A4 | not fired | judged — one lane, increments in order |
| B1 | fired | `grep -rl` over `tests/`: `render_present` → `test_markup_census.py`, `test_present.py`; `HelpModal` → `test_cleanup.py`, `test_gantt_board.py`, `test_legend.py`, `test_markup_census.py`, `test_setup_help.py`; `TaskModal` → `test_app.py`, `test_edit_window.py`, `test_emoji_picker.py`, `test_markup_sites.py`, `test_milestones.py`; `_to_dict` → `test_cascade.py` (batch-04 and earlier owners) |
| B2 | not fired | no file moves |
| B3 | not fired | `ls tests/goldens` → no such directory; the only byte oracles are the PRES-C frames (a batch evidence file, re-captured here — named in the census) |
| B4 | fired | `grep -rln "_to_dict\|board.json" taskboard/` → `team_sync.py` pushes `Board._to_dict`, so the new key reaches the shared folder; the SVG/PNG export carries the new frame |
| C1–C7 | not fired | `devflow-scan-spec.py` over `01-requirements.md` (P1) — recorded there; no auth, secret, external integration, sensitive data, DB, network or new input surface |
| C8 | fired | judged — the presentation and the help compose Rich markup over board-file text (titles, project names, dates); the S1 escape law applies to the new rows |
| D1 | fired | judged — every story changes what the user sees; `ux-reviewer` joins P2 and PDR |
| D2 | not fired | judged — the prototype ran the real Textual app (`app_capture.py`), the target technology |
| E1 | fired | 3 stories, 3 increments |
| E2 | not fired | judged — no high risk declared at intake |
| E3 | not fired | judged — internal tool, no client deliverable |
| F1 | not fired | `V7`: bundle identical to its manifest at `2026-10-12-rev102` |
| F2 | not fired | judged — `BACKLOG.md` was refreshed at batch-09's close (`5121fb0`) |

## Where we are

Closed (P5, 2026-10-17) — increments 001 (`ea002aa`), 002 (`d30aa8e`), 003 (`2292e63`) and 004 (the operator's verdict on the handoff, 2026-10-17: tick label `selected task ▸`, no ` — hybrid`, no in-frame keys row) implemented, reviewed (code-reviewer PASS/PASS-with-notes, no HIGH) and committed; DDR approved; P4 PASS-WITH-NOTES; the batch is closed on the local branch `present-v2`, not pushed (the commission forbids a push).

## Objective

Make the presentation readable in time (ruler + chips), let the presenter leave tasks out of it persistently, and make `?` show every key.

## Per-story / per-station status

| Story / station | Status | Notes |
|---|---|---|
| US-1601 | DONE | increments 001, 004 · AT-1601 pass |
| US-1602 | DONE | increment 002 · AT-1602 pass |
| US-1603 | DONE | increment 003 · AT-1603 pass |
| DDR | approved | `design/DDR-2026-10-16-batch-01.md` |
| P4 | PASS-WITH-NOTES | `04-validation.md`, gate run `evidence/suite-p4.txt` |
| P5 | closed | `05-close.md` |

## Roadmap + increment plan

- 001 — ruler B + chips: `views.py`; new oracle frames; tests.
- 002 — the flag: `models.py`, `app.py` (`PresentScreen`), `modals.py` (task editor), `views.py` (filter).
- 003 — `?` Keys band + pinned global line: `modals.py`, `keymap.py`.
- 004 — the operator's verdict on the handoff (2026-10-17): the tick label names the selected task; no ` — hybrid`, no in-frame keys row: `views.py`; PRES-R frames regenerated; TC-1608.

## Key decisions

| Date | Decision | Why |
|---|---|---|
| 2026-10-16 | branch `present-v2` from `origin/main`; local `main` untouched | RC-1: no merge-base with the rewritten origin; the source is identical; extending the pre-rewrite history would carry personal names forward |
| 2026-10-16 | batch id `2026-10-16-batch-01`, not the brief's suggested `2026-10-16-batch-10` | `devflow-init.py` `_batch_id` numbers per day; the suggestion was a suggestion |
| 2026-10-16 | ruler variant B; today `accent`, echo `bright` | operator verdict «Se ve mejor en acento»; matches the gantt view and the field's bright cursor bar |
| 2026-10-16 | start–end chips, chip 13 at every width, label 30/20 | prototype round 2: 12 clipped `Aug 21–Oct 10` at 80 |
| 2026-10-16 | the hide flag is `Task.show_in_present`, omitted from `board.json` when on | «una bandera basta»; byte-identity of boards with nothing hidden |
| 2026-10-16 | `space` hides, `a` shows all; `h` stays cursor-left | `h` is bound (P-3) |
| 2026-10-16 | hidden count in the hint row only | the frame is what the room sees and what `x` exports |
| 2026-10-16 | `?`: Keys as a full-width grid band; globals pinned at the bottom, derived from `KEYMAP` | the 118×40 capture clipped the left-column block exactly at `R` and `S` |
| 2026-10-16 | the oracle frames are re-captured into this batch's evidence; the batch-04 frames stay untouched | brief item 5 |
| 2026-10-17 | local `main` reset to `origin/main` by the coordinator, backup branch `backup/main-pre-reset-2026-10-17` | the operator's verdict on the handoff, item 1 — recorded, not done by this batch |
| 2026-10-17 | the tick row's label reads `selected task ▸` (echo tone, bold) when the echo fits; the echo's full text when it does not; the scale only with no selection | operator: «"Mondays · 1 day = 2 cells" means nothing to a meeting audience»; coordinator: the label names the thing whose dates are echoed, "cursor" is engineer jargon in a meeting |
| 2026-10-17 | a selected task with no date: `selected: no dates` (dim) | orchestrator's decision — the verdict did not name the case; the label still names the selection and never shows the scale while one exists |
| 2026-10-17 | the header drops ` — hybrid`; the in-frame keys row is removed | operator: both are visible to the room and reach the `x` export; the hint row below the frame carries the keys |
| 2026-10-17 | at 80×24 the `?` Keys band scrolls; only the Global line is guaranteed unscrolled | operator: accepted — the app normally runs larger |

## Risks / watch-items

- the re-captured oracle comes from the shipped renderer · medium · cross-checked row by row against the prototype's `render_b2` (`evidence/gen_frames.py`); after increment 004 one delta remains (D3, the tick label)
- the editor's measured chip-row thresholds (`TASK_CHIPS_ONE_ROW`) may move with a new checkbox · medium · place the box where the 80-column sweep holds; stop and report if no place does
- the global line cannot be one line at 80 columns · certain · wraps at an entry boundary; named in LLR-1603.2

## Conventions honored

- synthetic boards only (`tmp_path`; the PRES-C oracle board); English artifacts, code and UI; no personal names in code/tests/records
- no push; commits end with the commission's co-author line

## Out-of-scope carries

- ~~the header's ` — hybrid` suffix and the in-frame keys row~~ — resolved by the operator's verdict (2026-10-17), removed in increment 004
- undo of the hide flag — not an undo step (declared)

## Gate notices and runtime absences

**Runtime absences (`SKILL.md` gate step 5), named once:** no slash commands, no hooks of the flow's own, no operator prompt (the standing authorization stands in at every gate); reviewer roles run as spawned generic sub-agents carrying `agents/<role>.md` (`spawned — generic agent with agents/<role>.md`). `V15`, `V16`, `V17`: `not-run` — no canon tree, checkout table or flow hook from a bundle. `/dev-flow-sync`: `not-run` — no deployment record in a bundle install.

**P0 (after rollover):** 0 block · 59 notice — the step-3 placeholder NOTICEs (`V9`, `V27`, `V31`–`V34`, `V36`–`V38`, `V41`–`V51`, `V54`) over the unfilled seeds; `V25`/`V30` as tabled; historical NOTICEs over closed batches (`V13`, `V22`, `V23`, `V42`, `V53`) unchanged from batch-09.

**P3 gates:** `V2` BLOCKed AT-1602/AT-1603 at increments 001/002 — the station-expected red for nodes owed by later increments (`commands/dev-flow.md` §Two-layer validation model), cleared at 003; `V9` NOTICEs at 4 source files (increment 002, reason declared in §2) and on the historical root-level packets; `V27` between each packet and its decision; `V56` none. **Gate at the end of P3: 0 block.**

**P3 increment 004 (2026-10-17):** `V41` BLOCKed twice on increment 001's evidence rows after the PRES-R frames were regenerated in place — resolved by restoring PRES-R and writing the re-capture as `PRES-R2-*` (packet 004 §6); `V26` BLOCKed once at the DDR on a ledger pairing (LLR-1601.2 → LED .8) — removed, LED .9 carries it. **DDR / P4 / P5 gates:** 0 block; the NOTICEs left are historical over closed batches (`V13`, `V22`, `V23` on `.dev-flow/03-increments/increment-006.md`, `V42` on batch 2026-10-02-batch-03 and on this batch's `HANDOFF.md:81` and `03-increments/increment-004.md:93` (short repeats of the 80-column-frame deferral, which the backlog lane carries in full), `V53`), `V25` does not apply (origin exists), `V30` (bundle run); at close step 5 `V57` (the `Gated tree` placeholder) and at the final gate `V57` (record predates the tree by 1 commit) — both expected by the runbook. **Gate notices at the close:** declared in this section.

**Found before the batch:** `.gitattributes` (two evidence marks of batches 08/09 never committed) and, through it, `.dev-flow/2026-10-07-batch-0{8,9}/evidence/inc001-brief.md` read as modified (line endings only); untracked `.dev-flow/2026-10-07-batch-0{5..8}/decisions-log.json`, `.dev-flow/2026-10-07-batch-06/evidence/{gen_verdict_sheet.py,kanban-demo.json,veredicto-batch06.html,veredicto-board.json}`, `.dev-flow/rollover_batch{g,h,i,j}.py`. Not touched.

## Test ledger

| Suite / command | Last run | Result |
|---|---|---|
| `python -m pytest -q -p no:cacheprovider` (baseline, local `main` `e017ade`, source identical to `origin/main`) | 2026-10-16 | 2592 passed in 564.80s |
| the same on `origin/main` `64443be` (test files differ by the name scrub) | 2026-10-16 | 2 standup tests fail on base (`evidence/preexisting-base-failures.txt`) |
| full suite after increment 001 (`evidence/suite-001.txt`) | 2026-10-16 | 2 failed, 2603 passed |
| full suite after increment 002 (`evidence/suite-002.txt`) | 2026-10-16 | 2 failed, 2616 passed |
| full suite after increment 003 (`evidence/suite-003.txt`) | 2026-10-16 | 2 failed, 2625 passed |
| full suite after increment 004 (`evidence/suite-004.txt`) | 2026-10-17 | 2 failed, 2632 passed |
| P4 gate run on `8cd8dbd` (`evidence/suite-p4.txt`) | 2026-10-17 | 3 failed, 2631 passed — the 2 pre-existing + `test_win_clipboard_roundtrip` (environment, `evidence/p4-clipboard-env.txt`) |
