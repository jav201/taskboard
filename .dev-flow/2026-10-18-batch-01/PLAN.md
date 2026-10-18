# PLAN — taskboard — Batch 2026-10-18-batch-01

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
| Batch | 2026-10-18-batch-01 |
| Objective | Present v3: two views inside R -- the gantt view as shipped, its cursor note keeping line breaks and list items, and the split view (prototype D2 stacked: the gantt rows on top, every shown open task's notes below at once, two columns from 100 wide); 1/2 and tab/shift+tab switch, pgdn/pgup scroll the notes; R always opens on the gantt view |
| Last updated | P0 · 2026-10-18 |
| Standing authorization | standing authorization — the coordinator's commission of 2026-10-18 (the runtime cannot prompt): «Open a NEW dev-flow batch in `C:\Users\jjgh8\Github\taskboard` and implement the approved presentation design … Create a new local branch `present-v3` from main … follow the runbook … Run P4 and the P5 close.» Hard rules quoted from it: «No push, merge, reset or force», «At most 4 SOURCE files per increment», «Never rewrite oracle frames whose hashes earlier increments recorded», «An independent `code-reviewer` per increment, spawned». Read as: every gate of this batch is autonomous (reviewer roles are spawned sub-agents); commits on `present-v3` are authorized, each ending with the commission's co-author line; **push and merge are NOT authorized**; synthetic data only; the operator's design verdicts of 2026-10-17/18 on `prototypes/present_views/` (round 2, D2 · stacked) are the design authority. |
| First gate | step 1, on `main` `6ddea9f` before the branch: exit 1 — 85 block, all `V59` naming the untracked `prototypes/present_views/**` files (this batch's prototype evidence: committed by increment 001 and named in its §2; the regenerable PNGs, embedded in the prototype page, go to `.git/info/exclude`) · 41 notice; `V7`: bundle identical to its manifest both directions, 57 declared files, `2026-10-12-rev102`. Step 3 (after the rollover): exit 0 — 0 block · 62 notice. |
| Premises / RC-1 | RC-1 (a): `git fetch origin` → `origin/main` = `e97e6e6466e708cd2dac37b19c2260950bc34b51`; `git merge-base main origin/main` = `e97e6e6` = the origin tip, local `main` 1 ahead / 0 behind (`6ddea9f`, a backlog-only commit) — no rebase is owed; `git switch -c present-v3 main`; `base_ref` = `6ddea9f726f87edfb1152abc152e999cf31d9f04`. RC-1 (b): not already shipped — `git grep -n "PRESENT_VIEWS\|present_alloc\|present_note_lines" origin/main -- taskboard` → no hit; `render_present` on `origin/main` takes no `view` (`views.py:6263-6264`). RC-2: `git ls-remote --exit-code --heads origin` → exit 0; newest `origin/main` commit 2026-10-17 18:02 -0600. Premises P-1..P-8: `01-requirements.md` §2.7. |

## Triggers

The trigger evaluation `state.json`'s `triggers.record` points at: one row per trigger evaluated, fired or not.

| Id | Verdict | Probe output |
|---|---|---|
| A1 | not fired | judged — `docs/ARCHITECTURE.md` §2 · no new module, no boundary moved: every planned file (`views.py`, `app.py`) is an existing module's |
| A2 | fired | judged — the planned source files are `taskboard/views.py` (module `views`) and `taskboard/app.py` (module `app`): two modules |
| A3 | fired | judged — `render_present` (consumed by `app.PresentScreen`, `docs/ARCHITECTURE.md` §4) gains `view` and `scroll`; `present_paths` gains `view`; `views` exports `PRESENT_VIEWS` / `PRESENT_SCROLL_STEP` to `app` |
| A4 | not fired | judged — one lane, increments in order |
| B1 | fired | `grep -rl` over `tests/`: `render_present` → `test_markup_census.py`, `test_present.py`, `test_present_room.py`, `test_present_rulers.py`, `test_tick_label.py`; `PresentScreen` → `test_markup_census.py`, `test_markup_sites.py`, `test_present.py`, `test_present_hide.py`, `test_report.py`; `present-hint` → `test_present_hide.py`; `present-frame` → `test_present.py`, `test_present_hide.py`, `test_present_rulers.py`, `test_tick_label.py`; `save_present_svg` → `test_present_room.py`, `test_tick_label.py`; `_present_note_lines` / `_present_note_row` → no test (the prototypes `present_rulers/` and `present_views/views_proto.py` import them) |
| B2 | not fired | no file moves |
| B3 | fired | `ls tests/goldens` → no such directory; the byte oracle the presentation tests read is batch evidence: `PRES-R2-118x30.txt` / `PRES-R2-80x24.txt` (`tests/test_present.py`, TC-1001/TC-1002/AT-1001). The header's view word and the note fix change the gantt frame, so new `PRES-V3-*` frames are written in this batch's evidence and the tests repointed; PRES-R / PRES-R2 stay untouched |
| B4 | fired | the `x` export writes the current view's frame (`save_present_svg` / `save_present_png` over `render_present`); the split view's export is a new file name (`-split`) beside the gantt view's |
| C1–C7 | not fired | `devflow-scan-spec.py` over `01-requirements.md` (P1) — recorded there; no auth, secret, external integration, sensitive data, DB, network or new input surface |
| C8 | fired | judged — the split view composes Rich markup over board-file text (note bodies, titles, dates) in new rows; the S1 escape law applies to every new row |
| D1 | fired | judged — every story changes what the user sees or touches; `ux-reviewer` joins P2 and the PDR |
| D2 | not fired | judged — the prototype ran the real Textual app headless (`prototypes/present_views/app_capture.py`, `app_capture2.py`), the target technology |
| E1 | fired | 3 stories (US-1801..US-1803) |
| E2 | not fired | judged — no high risk declared |
| E3 | not fired | judged — internal tool, no client deliverable |
| F1 | not fired | `V7`: bundle identical to its manifest at `2026-10-12-rev102` |
| F2 | not fired | judged — `BACKLOG.md` was refreshed at 2026-10-17-batch-01's close (`e6da610`) and after it (`6ddea9f`) |

## Where we are

P0 — the batch is open on `present-v3` by rollover from 2026-10-17-batch-01; three stories READY; triggers A2/A3 fired, so ARQ is next, then P1.

## Objective

Give the presentation a second, switchable view that shows every shown open task's notes at once under the gantt rows, keep the gantt view's note structure, and make the switch one key that never loses the presenter's place or writes anything new.

## Per-story / per-station status

| Story / station | Status | Notes |
|---|---|---|
| US-1801 | READY | the split view |
| US-1802 | READY | the gantt note's line breaks |
| US-1803 | READY | keys, scroll, shared state |

## Roadmap + increment plan

- 001 — the renderer: `taskboard/views.py` (the split view, the shared note wrapper, the gantt note fix, the header's view word); the PRES-V3 oracle frames; renderer tests. 1 source file.
- 002 — the screen: `taskboard/app.py` (`PresentScreen`: keys, view and scroll state, hint row, export of the current view), `taskboard/views.py` (`present_paths` view suffix); app-level tests; README. 2 source files.

## Key decisions

| Date | Decision | Why |
|---|---|---|
| 2026-10-18 | branch `present-v3` from local `main` `6ddea9f`; no rebase | `main` already contains `origin/main` (merge-base = origin tip); the commission names `main` |
| 2026-10-18 | rollover by script (the 2026-10-07 `rollover_batchj.py` pattern, using `devflow-init.py`'s own seed helpers); the evidence home's `-text` mark is a per-directory `evidence/.gitattributes` | the root `.gitattributes` was dirty before the batch and the commission says to leave it alone (the 2026-10-17-batch-01 precedent) |
| 2026-10-18 | the prototype's PNGs go to `.git/info/exclude`; its sources, SVGs and page are committed by increment 001 | the page embeds every PNG (6 MB) and `app_capture*.py` regenerate them; the 2026-10-16-batch-01 precedent committed the round's sources and SVGs |

## Risks / watch-items

- the oracle frames come from the shipped renderer · medium · cross-checked row by row against the prototype's own renderer (`views_d.py`) at every frame by `evidence/gen_frames.py`
- the area-scroll rule is the brief's addition, not in the prototype · medium · stated in an LLR with its own tests; scroll-0 frames are byte-equal to the prototype

## Conventions honored

- synthetic boards only (`tmp_path`; the PRES-C oracle board and its notes overlay); English artifacts, code and UI; the operator's name nowhere (`username_subject` is the fixture's placeholder)
- no push, no merge; commits end with the commission's co-author line; own paths staged by name

## Out-of-scope carries

- round 1's "Slide" view (C) — kept as an optional future item in `BACKLOG.md`; "Cards" (B) — dropped, recorded in `BACKLOG.md`
- remembering the last view — refused by the brief (the presentation writes only `show_in_present`)

## Gate notices and runtime absences

**Runtime absences (`SKILL.md` gate step 5), named once:** no slash commands, no hooks of the flow's own, no operator prompt (the standing authorization stands in at every gate); reviewer roles run as spawned generic sub-agents carrying `agents/<role>.md` (`spawned — generic agent with agents/<role>.md`). `V15`, `V16`, `V17`: `not-run` — no canon tree, checkout table or flow hook from a bundle. `/dev-flow-sync`: `not-run` — no deployment record in a bundle install.

**P0 (step 3, after the rollover):** 0 block · 62 notice — the step-3 placeholder NOTICEs (`V9`, `V27`, `V31`–`V34`, `V36`–`V38`, `V41`, `V43`–`V51`, `V54`) over the unfilled seeds; `V30` (bundle run); historical NOTICEs over closed batches (`V9` on old packets, `V13`, `V22`, `V23`, `V42`, `V53`) unchanged from 2026-10-17-batch-01.

**Found before the batch:** tracked and modified — `.gitattributes`, `.dev-flow/2026-10-07-batch-0{8,9}/evidence/inc001-brief.md` (line endings only); untracked — `.dev-flow/2026-10-07-batch-0{5..8}/decisions-log.json`, `.dev-flow/2026-10-07-batch-06/evidence/{gen_verdict_sheet.py,kanban-demo.json,veredicto-batch06.html,veredicto-board.json}`, `.dev-flow/rollover_batch{g,h,i,j}.py`. Not touched.

## Test ledger

| Suite / command | Last run | Result |
|---|---|---|
| `python -m pytest -q -p no:cacheprovider` on `base_ref` | — | owed at increment 001 (`evidence/suite-base.txt`) |
