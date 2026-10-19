# PLAN — taskboard — Batch 2026-10-19-batch-01

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
| Batch | 2026-10-19-batch-01 |
| Objective | Present view 3 `all` (variant C, curate rail, of the present-portfolio round): every shown project on one date ruler beside a project rail; hide and show projects and tasks, a persisted presentation-only project order, fold, a `u` picker of hidden items in all three Present views, `x` exporting the timeline without the rail; and the shipped bug of views 1/2 that draws a start-less milestone as a bar from today |
| Last updated | ARQ · 2026-10-19 |
| Standing authorization | standing authorization — the orchestrator's commission of 2026-10-19 (the runtime cannot prompt), relaying the operator's verdict on `prototypes/present_portfolio/` of 2026-10-19: «C: Me parece la mejor opción para mis objetivos.» · «Sí, que persista el orden.» · «Siempre la traigo con (a), pero sería útil tener el seleccionador propuesto con (u)», and the earlier commission «necesito que en el modo presentación pueda tener la vista del gantt con todos los proyectos… esconder tareas o proyectos… reordenar los proyectos en el orden que mejor me convenga.» Quoted from the commission: «Implement a /dev-flow batch … Batch id `2026-10-19-batch-01`, artifact language English», «Cut local branch `feat/present-all` from `main` (2cf17f0)», «you may cherry-pick or merge that prototype commit into your branch», «Do NOT push», «Max 4 SOURCE files per increment (tests uncapped)», decisions D1–D8 «made by the orchestrator under "confío en tu juicio"». Read as: every gate of this batch is autonomous (reviewer roles are spawned sub-agents); commits on the local branch `feat/present-all` are authorized, each ending with the commission's co-author line; **push and merge are NOT authorized**; synthetic data only; the operator's name nowhere (`username_subject`); `.gitattributes`, the two `inc001-brief.md` files and the untracked old `.dev-flow/*` files are not touched or staged. |
| First gate | step 1, on `feat/present-all` at `2cf17f0` before the rollover: exit 1 — 86 block · 42 notice · 63 not applicable; every BLOCK the outgoing closed batch's record against the tree: `V59` ×85 (2026-10-18-batch-03's `base_ref` `620f58c` predates `2cf17f0`, the retirement commit made after its close) and `V2` ×1 (`AT-1905`, whose node `2cf17f0` retired with the round, named by the closed batch's records) — both repaired by the rollover, which re-stamps `base_ref` and makes this batch the active record; `V7`: bundle identical to its manifest both directions, 57 declared files, `2026-10-12-rev102`. Step 3 (after the rollover): exit 0 — 0 block · 64 notice · 47 not applicable (`evidence/gate-step1.txt`, `evidence/gate-step3.txt`). |
| Premises / RC-1 | RC-1 (a): `git fetch origin` → `origin/main` = `2cf17f0cab2738d1c1ae9250eb845d77eb73c300` = local `main`; `git switch -c feat/present-all main`; HEAD equals the origin tip, so no rebase is owed. The round's commit `1132d85` (local branch `proto/present-portfolio`) cherry-picked as `bdf6e9d` (prototype files only — the design input, as the commission allows), and `base_ref` stamped `bdf6e9d54d6e39ef083c2cc8708de5b6943b98e9` so the round is not counted as this batch's work. RC-1 (b): not already shipped — on `origin/main` `PresentScreen` has two views (`views.py:6168` `PRESENT_VIEWS = ("gantt", "split")`), `Project` has no presentation field (`models.py:796-805`), `git grep present_rank taskboard/` → nothing. RC-2: `git ls-remote --exit-code --heads origin` → exit 0. Premises: `01-requirements.md` §2.7 (P-1..P-7, all TRUE, `evidence/premises.txt`). |

## Triggers

The trigger evaluation `state.json`'s `triggers.record` points at: one row per trigger evaluated, fired or not.

| Id | Verdict | Probe output |
|---|---|---|
| A1 | not fired | judged — `docs/ARCHITECTURE.md` §2 · no module created, no boundary moved: the planned source files (`models.py`, `views.py`, `app.py`, `modals.py`) are existing layers'; the new test files sit under `tests` |
| A2 | fired | judged — the planned source files span four layers: `models`, `views`, `app`, `modals` |
| A3 | fired | judged — `docs/ARCHITECTURE.md` §4 · the `board.json` project record gains two keys (consumed by `team_sync`'s pull and other app versions); `Project` gains two fields; new interfaces `render_present_all`, `PRESENT_SCREEN_VIEWS`, `present_hidden_rows`, `present_order`; `present_paths` gains the `all` view |
| A4 | not fired | judged — one lane, increments in order |
| B1 | fired | `grep -rl --include=*.py` over `tests/`: `render_present` → `test_markup_census.py`, `test_present.py`, `test_present_narrow.py`, `test_present_polish.py`, `test_present_room.py`, `test_present_rulers.py`, `test_present_views.py`, `test_tick_label.py`; `_hint` / `present-hint` → `test_present_hide.py`, `test_present_narrow.py`, `test_present_polish.py`, `test_present_views_app.py` (and `test_gantt_polish.py`, `test_link_picker.py`: other screens' own `_hint`); `PRESENT_VIEWS` → `test_present_narrow.py`, `test_present_polish.py`; `1 gantt` → `test_present_hide.py`, `test_present_narrow.py`, `test_present_polish.py`, `test_present_views.py`, `test_present_views_app.py`; `Project.from_dict` → `test_app.py`, `test_palette_ration.py`, `test_sync_fields.py`; `_to_dict` → `test_cascade.py`; `_present_task_row` → none |
| B2 | not fired | no file moves |
| B3 | fired | `ls tests/goldens` → no such directory; the byte oracles of the presentation are batch evidence: the PRES-V3 frames of 2026-10-18-batch-01 and the PRES-V4 gantt-notes frames of 2026-10-18-batch-03 (read by `tests/test_present.py`, `tests/test_present_views.py`, `tests/test_present_views_app.py`, `tests/test_present_polish.py`), over `render_present`, whose task rows increment 001 touches — their boards hold no milestone (`grep milestone tests/present_board.py tests/present_notes_board.py` → nothing), so no drift is expected and the census of increment 001 re-runs them |
| B4 | fired | judged — `x` in view 3 writes `reports/present-board-<date>-all.svg/.png` (read by the presenter and any viewer); the board file gains two project keys read by `Board.load`, `team_sync`'s pull and other app versions |
| C1, C4, C5 | fired | `devflow-scan-spec.py` over `01-requirements.md` (P1): `flags: session, billing, migration`, `security_required: true`, exit 1 (`evidence/scan-p1.txt`) — the words name the in-memory fold state and the synthetic fixture project "Billing Migration"; answered in `01-requirements.md` §6.3; the security-reviewer pass of P2 reads them |
| C2, C3, C6, C7 | not fired | the same scan: no flag in those families |
| C8 | fired | judged — new markup sites over board-file text: project names on the rail and the view-3 headers (`escape(fit(...))` in `views`), names and titles in the picker (plain `Text` pieces in `modals`) |
| D1 | fired | judged — a new view, new keys and a picker the presenter sees and touches; `ux-reviewer` joins P2 and the PDR |
| D2 | not fired | judged — the round ran the real Textual app headless (`app_capture.py`, `export_screenshot`), the target technology |
| E1 | fired | 4 stories (US-2101..US-2104) and 4 planned increments |
| E2 | not fired | judged — no high risk declared: additive keys, a new view, a contained fix |
| E3 | not fired | judged — internal tool, no client deliverable |
| F1 | not fired | `V7`: bundle identical to its manifest at `2026-10-12-rev102` |
| F2 | not fired | judged — `BACKLOG.md` was refreshed at 2026-10-18-batch-03's close and by `2cf17f0` |

## Where we are

ARQ — P0 approved (the batch open by rollover on `bdf6e9d`, triggers evaluated, ARQ/PDR/DDR taken up, the stories READY); the module-map amendment, the requirements and the design proposal are drafted and go to the reviewer lenses (architect · qa-reviewer · ux-reviewer · security-reviewer).

## Objective

Ship variant C of the present-portfolio round as Present view 3 `all` — the portfolio on one ruler with its curate rail, hiding and re-showing projects and tasks, a persisted presentation order, folds, a `u` picker in all three views — and fix the milestone bar of views 1/2.

## Per-story / per-station status

| Story / station | Status | Notes |
|---|---|---|
| US-2101 | READY | increment 001 |
| US-2102 | READY | increment 003 |
| US-2103 | READY | increments 002, 004 |
| US-2104 | READY | increment 004 |
| P0 | done | triggers evaluated; refinement done |
| ARQ | in progress | `docs/ARCHITECTURE.md` amended (drafted) |

## Roadmap + increment plan

- 001 — the milestone row (HLR-2101): `taskboard/views.py` (`_present_task_row`); `tests/test_present_milestone.py` (TC-2101, AT-2101), `tests/present_portfolio_board.py` (the round's board). 1 source file.
- 002 — the model (HLR-2102): `taskboard/models.py`; `tests/test_present_all.py` (TC-2102; AT-2102 lands with 004, which ships the keys it drives). 1 source file.
- 003 — view 3 (HLR-2103, HLR-2104): `taskboard/views.py` (`render_present_all`, `PRESENT_SCREEN_VIEWS`), `taskboard/app.py` (`PresentScreen`); `tests/test_present_all.py` (TC-2103, TC-2104, AT-2103, AT-2104) and the law-driven hint updates. 2 source files.
- 004 — curation and the picker (HLR-2105, HLR-2106, AT-2102): `taskboard/app.py`, `taskboard/modals.py`, `taskboard/views.py` (`present_hidden_rows`); `tests/test_present_all.py`; `README.md`, `.dev-flow/BACKLOG.md` (docs). 3 source files.

## Key decisions

| Date | Decision | Why |
|---|---|---|
| 2026-10-19 | D1 — variant C (curate rail) becomes Present view `3 all`; `tab` cycles 1 → 2 → 3 | the operator's verdict «C» (the commission) |
| 2026-10-19 | D2 — `Project.show_in_present: bool = True` (written only when false) and `Project.present_rank: int | None` (written only as an integer, validated on load); the order is the presentation's own; the board's views keep board order; unranked projects after ranked ones in board order. **This reading of «que persista el orden» is the orchestrator's**: the operator may prefer the board's own order — flagged in the close | «Sí, que persista el orden»; the round's default was a presentation-only order and its before/after showed the board gantt untouched — the operator did not object to that part (the commission) |
| 2026-10-19 | D3 — `space` hides the cursor row (task / project), `a` shows all, `shift+↑/↓` reorders (persisted, dense renumbering of every visible project), `enter` folds, `←/→` move focus between rail and timeline; the rail shows hidden projects `○` and `space` there re-shows one | as prototyped (the commission) |
| 2026-10-19 | D4 — `u` in all three views opens a picker of hidden items | the operator's note (the commission) |
| 2026-10-19 | D5 — the rail is 24 columns and not drawn below 100 columns; keys still work on the timeline; `u` covers re-showing | the round's C was worst at 80×24 (P-4) (the commission) |
| 2026-10-19 | D6 — `x` in view 3 exports the timeline without the rail, files suffixed `-all`; the window fitted to the shown projects' open work; `R` still opens on view 1, view 3's cursor starts on that project | the commission |
| 2026-10-19 | D7 — the milestone bar of views 1/2 fixed in its own increment, RED on base | the round's finding (the commission) |
| 2026-10-19 | D8 — README, the `?` help and the backlog updated. **Deviation:** the `?` help is not changed — it lists the main screen's keys only, the presentation's keys live in its hint row by design (`docs/ARCHITECTURE.md` §5); view 3 and `u` go in the hint row and the README | the help's design (LLR-1603.1; the module map's re-open condition); declared in `01-requirements.md` §6.3 |
| 2026-10-19 | the round's commit cherry-picked as `bdf6e9d` and `base_ref` stamped there, the prototype folder shipping with the feature | the commission allows it; prior rounds kept their folders; the round is design input, not this batch's work (`V59`) |
| 2026-10-19 | the rollover by script with `devflow-init.py`'s own seed helpers (the 2026-10-18-batch-02/03 pattern); the evidence home's `-text` mark a per-directory `evidence/.gitattributes` | the root `.gitattributes` was dirty before the batch and the commission says not to touch it |
| 2026-10-19 | the hint's `u`: the tail ` · u N hidden` (views 1/2) / ` · u P project(s) + T task(s) hidden` (view 3), only when something is hidden; below 36 columns the tail stays ` · N hidden` | the hint's own `<key> <label>` grammar; `u` shown where it acts; +2 cells only when hidden |
| 2026-10-19 | `PRESENT_VIEWS` stays `("gantt", "split")` (the views of `render_present`); the screen's three views are `PRESENT_SCREEN_VIEWS` | view 3 has its own renderer (`docs/ARCHITECTURE.md` §5); the tests that iterate `PRESENT_VIEWS` through `render_present` stay valid |
| 2026-10-19 | the reviewer lenses of ARQ, P2 and the PDR run as one spawned agent per role over the drafted artifacts together (architect · qa-reviewer · ux-reviewer · security-reviewer), each returning per-station findings; the gates are then recorded in station order | the four roles are independent of each other and of the author; one pass per role over the three stations' artifacts avoids re-reading the same contract three times — declared here |
| 2026-10-19 | four increments in the order 001 milestone → 002 model → 003 view 3 → 004 curation + picker | 001 first so view 3 inherits the fixed row; 002 before 003 because view 3 reads the order |

## Risks / watch-items

- the law-driven updates of shipped hint tests (TC-1904, TC-1808, TC-2002, AT-2002, TC-1604, AT-1602) could hide a weakened assertion · medium · each named old → new in packet 003's census, the new values derived from the literal wording strings, never from the code
- the split view's hint at 80 columns drops from the middle wording to the short one (three view names) · certain · declared in `01-requirements.md` §6.3 and the close
- the round's capture script will not reproduce its captures after 003 (it subclasses `PresentScreen`) · certain · frozen evidence (`docs/ARCHITECTURE.md` §3); the folder stays as committed
- a team pull of a NEW project carries its `show_in_present` / `present_rank` from `team.json` · low · an existing project's flags are never touched by a pull; recorded in the module map

## Conventions honored

- synthetic boards only (`tmp_path`; the round's board); English artifacts, code and UI; the operator's name nowhere
- no push, no merge, no reset, no force; commits end with the commission's co-author line; own paths staged by name

## Out-of-scope carries

- variants A and B of the round, B's ticks on folded headers — not chosen
- the `?` help listing the presentation's keys — kept out (D8 deviation), recorded in `BACKLOG.md` for the operator
- the presentation order as the board's own order — the operator's call (D2)

## Gate notices and runtime absences

**Runtime absences (`SKILL.md` gate step 5), named once:** no slash commands, no hooks of the flow's own, no operator prompt (the standing authorization stands in at every gate); reviewer roles run as spawned agents carrying their `agents/<role>.md` role. `V15`, `V16`, `V17`: `not-run` — no canon tree, checkout table or flow hook from a bundle. `/dev-flow-sync`: `not-run` — no deployment record in a bundle install.

**Step 1 (before the rollover):** exit 1 — the BLOCKs are the outgoing closed batch's (`V59` ×85, `V2` ×1, see the header's `First gate`), repaired by the rollover; NOTICEs `V9` ×13, `V13` ×8, `V22` ×5, `V23` ×3, `V42` ×9, `V53` ×1, `V57` ×2, `V30` — historical, over closed batches, and the bundle run.

**P0 (step 3, after the rollover):** 0 block · 64 notice — the step-3 placeholder NOTICEs (`V27`, `V31`–`V34`, `V36`–`V38`, `V41`, `V43`–`V51`, `V54`) over the unfilled seeds; `V30`; the historical NOTICEs above.

**Found before the batch:** tracked and modified — `.gitattributes`, `.dev-flow/2026-10-07-batch-0{8,9}/evidence/inc001-brief.md` (line endings only); untracked — `.dev-flow/2026-10-07-batch-0{5..8}/decisions-log.json`, `.dev-flow/2026-10-07-batch-06/evidence/{gen_verdict_sheet.py,kanban-demo.json,veredicto-batch06.html,veredicto-board.json}`, `.dev-flow/rollover_batch{g,h,i,j}.py`. Not touched.

## Test ledger

| Suite / command | Last run | Result |
|---|---|---|
| `python -m pytest -q -p no:cacheprovider -rs --color=no` on `base_ref` (a worktree at `bdf6e9d`, `NO_COLOR` unset) | 2026-10-19 | 2757 passed, 1 skipped (the clipboard roundtrip, its refusal quoted) — `evidence/suite-base.txt` |
