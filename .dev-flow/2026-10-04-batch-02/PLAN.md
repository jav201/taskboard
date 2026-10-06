# PLAN — taskboard — Batch 2026-10-04-batch-02

> Living plan (flow `templates/plan-template.md`). Mode `core`, language `en`, flow **rev100**, the
> installed bundle (skills commit `1d3c364`, "flow rev100 closefix 1 — the bundle re-synced").

## Header

| Field | Value |
|---|---|
| Project | taskboard |
| Batch | 2026-10-04-batch-02 |
| Objective | Batch B2 of the `kg_mejoras` plan. Commissioned: milestones as a task flag (gantt M-1 with the AX-2 ruler marks, kanban M-2 band rule, a key and the editor), moving linked dates (round 6), and the one-time M-3 milestone offer as a migration. Run under the pre-authorized split (D-601): **B2a** = milestones (US-601, US-602, US-603, US-605); **B2b** = moving linked dates (US-604) → `BACKLOG.md`. |
| Flow | **rev100, the installed bundle** — operator ruling at kickoff: "rev100, la instalada". `~/.claude/skills` HEAD `1d3c364` = the last declared rev100 commit. Contingency (commission): if the installed bundle starts failing `V7` mid-batch, continue from a read-only `git archive` snapshot of `1d3c364` in the session scratchpad and record it here as the pin. `~/.claude` is never edited. |
| Standing authorization | the operator's commission, asked at this batch's kickoff and relayed by the coordinator (this runtime is a delegated sub-agent and cannot prompt), dated 2026-10-04: **Gates — "Autónomo + ambas excepciones":** end-to-end autonomous, self-approve each gate, record every un-asked decision. A HIGH ONLY in tests/evidence (reviewer confirms product correct) OR a HIGH in the increment UNDER CONSTRUCTION (not yet approved) may be fixed without stopping, with a RED-first proof, recorded and re-reviewed. STOP and report: a HIGH in code already approved or shipped, any security HIGH, any HIGH touching the operator's data (migrations). **Git — "Commit + push tras tu veredicto visual":** the COORDINATOR commits/pushes after verification and the operator's visual verdict; this agent does NOT commit, push, stash, reset or checkout anything; `merge: false (no PR; coordinator commits+pushes to main after the operator's visual verdict)`. **Migration safeguard — "Sí: respaldo + registro + deshacer":** the one-time milestone offer converts NOTHING the operator didn't choose in the picker; whatever it converts is backed up first, logged, revertible with `u`, never offered twice. Never open, read or write the operator's real board — tests and synthetic boards only. Also in `state.json` `standing_authorization`. |
| First gate | kickoff run by the coordinator @`4b2c13a`: exit 0, **0 block · 31 notice**; re-run by this agent before the rollover: exit 0, 0 block · 31 notice; `V7` clean (no `V7` line: the bundle's bytes match its manifest). After the rollover: exit 0, 0 block · 43 notice (the 31 inherited + the new batch's seeded placeholders and an empty ledger, `V27`). |
| Premises / RC-1 | RC-1 (a): `git fetch origin` → `origin/main` = HEAD = merge-base = `4b2c13ae6ab2`; nothing to rebase; `base_ref` stamped from it. RC-2: `git ls-remote --exit-code --heads origin` answered (5 heads, exit 0); `origin/main`'s newest commit 2026-10-04 19:06 −0600. RC-1 (b): no story already shipped on `origin/main` (`evidence/p0-probes.txt` §RC-1 (b): `milestone`, `date_links`, `push_delta`, `◆✓`, the move keys — 0 hits). Premise table: `01-requirements.md` §2.7. |

## Triggers

Evaluated 2026-10-04 at P0 (`devflow-init.py --fired … --not-fired …`); probes in `evidence/p0-probes.txt`.

| Id | Verdict | Probe output |
|---|---|---|
| B1 | fired | reverse census: `gantt_plan` → test_app, test_gantt, test_gantt_board, test_gantt_link, test_gantt_polish; `_gantt_bar` → test_app, test_gantt, test_gantt_board; `kanban_plan`/`_band_rule` → test_kanban_readable; `kanban_order` → 4 files; `nav_model` → 9 files; `TaskModal` → 4 files; `TaskDetails` → 5 files; `KEYMAP` → 11 files; `from_dict` → 4 files; `legend_entries` → 8 files; `◆` → 6 files — re-validated per increment |
| B2 | not fired | no file moves; new files only (tests) |
| B3 | not fired | `ls tests/goldens` → no such directory |
| B4 | fired | the milestone offer writes the board file the next start and the next load consume (AT-604's fresh app), and a backup and a log for the operator's manual restore (`u` uses the session's undo entry, qa Q-7) → output-then-consume AT (C-12) |
| A1–A4 | not fired (judged, D-602) | `docs/ARCHITECTURE.md` absent (no module map to probe); no module is created or moved — the flag and the offer sit beside the shipped seats in `models.py` (`Task`, the B1 migration seat), the renderers in `views.py`; the same judgement as batches 2026-10-02-01..04 and 2026-10-04-01 (D-502) |
| C5 | fired | the offer rewrites the operator's board file (convert, mark) — a data write with a backup, a log and a revert |
| C6 | fired | a new synced field (`milestone`) read from teammates' `board.<user>.json` |
| C8 | fired | new surfaces paint file-derived text (milestone titles on the gantt rows, the ruler label, the kanban band rule, the offer's rows) → S1 Text pieces; scan at P1 |
| C1–C4, C7 | not fired | no auth, secret, external service, sensitive personal data or network surface added |
| D1 | fired | user-visible: gantt rows, ruler, legend, kanban band rule, editor, details, the offer picker, a key → ux-reviewer at P2/P4; captures 118×30 and 80×24, base and close |
| D2 | fired | the verdict frames come from a rich-rendered prototype, not Textual: the picker's keys (`space`, `↵`, `esc`) and `M` are verified through the real app (C-16) |
| E1 | fired | 5 commissioned stories (4 run) |
| E2, E3 | not fired | no high risk declared at intake beyond the migration, which family C covers; not a client deliverable |
| F2 | fired | `BACKLOG.md` header base ref `0447070` ≠ HEAD `4b2c13a` → reconciled at close |
| F1 | not fired | `V7` clean on the installed rev100 bundle |

## Where we are

**P5 (2026-10-05).** P1 and P2 took three iterations each. Increments 001–004 are approved:
- 001: r3; F2-1 HIGH fixed under the second exception.
- 002: r2.
- 003: r2.
- 004: r2.

P4 has the qa, ux and security verdicts: APPROVE-WITH-NOTES, APPROVE-WITH-NOTES and PASS-WITH-NOTES, 0 HIGH. Three MEDIUM test and evidence defects were folded (F-1, F-2, UXV-1).

Close gate: 2485 passed, 1 failed (G-011 flake).

Next: the coordinator commits and pushes after the operator's visual verdict on PV-601..PV-611 and the P4 notes below.

**Verdict received 2026-10-06** (`taskboard-veredicto-b2a.json`): PV-601..PV-611 all **accepted**. UXV-5 decided **"Aclararlo a un gris legible (~4.5:1)"** — applied: new palette tone `reached` `#7a828c` (4.9:1 on `#0d1117`, measured) at every reached-milestone seat; the consumed field keeps `ash`. LED-2026-10-04-batch-02.11. UXV-2, UXV-4, UXV-7, UX-12 carried no change request.

## Objective

A milestone is a task with one date: the gantt draws it as a `◆` with its date and a chip instead of
a bar, the ruler marks the selected project's milestones, the kanban lifts it out of the columns onto
its project's band rule, `M` and the editor set it, team sync carries it; and an existing board that
holds one-day or due-only tasks is offered, once, to convert the ones the user picks — backed up,
logged and undoable.

## Per-story / per-station status

| Story / station | Status | Notes |
|---|---|---|
| P0 intake | approved | rollover; triggers; D-601 split |
| P1 requirements | approved (iteration 3) | LED .1–.4; D-601..D-625; 19 premises TRUE |
| P2 review | approved (iteration 3) | it.1 FAIL ×3 (Q-1, A-1 blockers); it.2 majors A2-1, Q2-1, Q-12; it.3 PASS / PASS-WITH-NOTES, 0 HIGH |
| P3 increment 001 | done (revision 3) | 4 SOURCE; 19/19 mutants; code review F2-1 HIGH fixed (2nd exception); gate 2346 passed + clipboard flake |
| P3 increment 002 | done (revision 2) | 2 SOURCE; 16/16 mutants; gate 2375 passed + flake |
| P3 increment 003 | done (revision 2) | 3 SOURCE; 19/19 mutants; gate 2446 passed + flake |
| P3 increment 004 | done (revision 2) | 3 SOURCE; 23/23 mutants; code OK-WITH-NOTES, security PASS; gate 2485 passed + flake |
| P4 validation | PASS-WITH-NOTES | qa, ux APPROVE-WITH-NOTES; F-1, F-2, UXV-1 folded (V2 RED → KILLED); close gate 2485 passed + flake |
| P5 close | closed | security close PASS-WITH-NOTES (S5-1 folded); canon folded; BACKLOG updated |
| US-601 milestone flag (key, editor, sync) | DONE | increment 001 |
| US-602 gantt M-1 + AX-2 marks | DONE | increment 002 |
| US-603 kanban M-2 | DONE | increment 003 |
| US-604 moving linked dates | OUT → BACKLOG (B2b) | D-601 |
| US-605 one-time milestone offer (M-3) | DONE | increment 004 |

## Roadmap + increment plan

1. Increment 001 — the flag (US-601): `Task.milestone`, `set_milestone`, `bump_due`; `M`; undo fields; the editor box and the add/edit apply; the details mark; README. TC-601..606; AT-601. SOURCE: `models.py`, `app.py`, `modals.py`, `keymap.py` (⚠ at the cap: the key, the action, the model and the editor are one user-visible capability; any one left out ships a flag nobody can set).
2. Increment 002 — the gantt (US-602): `GanttGroup.rows`, the milestone row, ruler marks, legend, help. TC-609..611; AT-602. SOURCE: `views.py`, `app.py` (`_notify_folded`, D-614).
3. Increment 003 — the kanban (US-603): `kanban_work`, `band_milestones`, the band-rule layout. TC-612, TC-613; AT-603. SOURCE: `views.py`, `app.py` (`_select_first`, D-614).
4. Increment 004 — the offer (US-605): candidates, `run_milestone_offer`, the seeded marks, the on-mount step, undo, `MilestoneOffer`; `tests/conftest.py` seam. TC-614..617; AT-604..606. SOURCE: `models.py`, `app.py`, `modals.py`.

The offer comes last: no earlier increment reads a board with a different meaning (unlike B1's links), and it needs the flag (001).

## Key decisions

| Date | Decision | Why |
|---|---|---|
| 2026-10-04 | Batch id `2026-10-04-batch-02` (operator's local date 2026-10-04 at open); ids in the disjoint `6xx` range | commission; `0xx`..`5xx` taken (`grep` over `REQUIREMENTS.md` and `.dev-flow/**`: 0 `6xx` ids) |
| 2026-10-04 | D-601: run B2a (US-601, 602, 603, 605); US-604 moving linked dates → `BACKLOG.md` as B2b | the pre-authorized split; P0 feasibility: no gantt move/edit mode exists (`evidence/p0-probes.txt` §US-4: no `shift+`/`alt+` binding, no `date_links`, `cascade` only in a docstring), so US-604 alone is a move mode + a cascade engine + a synced per-project setting + bump toasts; B1 needed 7 increments for 5 stories; B2a alone is 4 increments over 5 SOURCE files |
| 2026-10-04 | D-602: trigger family A judged not fired | as above (Triggers) |
| 2026-10-04 | P0 approved under the standing authorization | `01-requirements.md` §2.6 |
| 2026-10-04 | P1 iterations 2–3 and P2 iterations 1–3: every finding folded; D-611..D-625 | `02-review.md`; LED .2–.4 |
| 2026-10-04 | Increment 001 approved (revision 3): F-4 → LED .5; F2-1 (HIGH, product, under construction) fixed without stopping, RED-first, re-reviewed → LED .6 | `03-increments/increment-001.md` |

## Provisional visual decisions (for the operator, with the captures to compare)

Listed at P1, captured at P3, closed at P5 (`05-close.md`). Each is the most conservative reversible reading where the verdict frames leave a detail open.

| Id | Decision | Captures (before → after, `evidence/captures/`) |
|---|---|---|
| PV-601 | Gantt milestone row as M-1: label ` ◆ title` (the `◆` in the milestone's tone), field `◆` with ` Mon D` beside it (left of it when no room), chip `in Nd` / `today` / `▲Nd` / `✓ done`; tones: project hue upcoming, over late, ash reached (`◆✓`, label and date ash) | `base-gantt-*` → `close-gantt-*` |
| PV-602 | Every reached milestone is a row among its group's open rows by date (all of them, not only the latest), only while the group has open work; it counts in `✓n`; an open milestone counts in `N open` (the M-1 frame's counts) | `base-gantt-*` → `close-gantt-*`; `close-gantt-reached-*` (three reached milestones in one group, ux UX-10) |
| PV-603 | The ruler's month row marks the selected project's milestones `◆` in their tone, drawn after the project's due (a milestone on the due's cell shows the milestone's tone) | `base-gantt-*` → `close-gantt-*` |
| PV-604 | The gantt legend row places `◆ milestone` and `◆✓ reached` right after the selection item (the M-1 frames' order, so they survive at 80); the `?` map and help name them | — → `close-legend-gantt-*` |
| PV-605 | Band-rule layout (M-2): ` ── ◆ Mon D Title · in Nd`, separated by `──`, titles cut (≥ 8 cells each) before they drop, dates only next, then `── +N ◆` (reached never counted), `+N ◆` alone when no date fits (D-619); a project whose only open items are milestones draws no band (D-623); at a 118×30 terminal the high band pushes Ops & Security's late milestone below the fold (a fold-row marker → BACKLOG, ux UX2-2) | `base-kanban-*` → `close-kanban-*` |
| PV-606 | Matrix, lanes and the priority/horizon groupings show no milestone at all (not a card; no band rule carries them there) | `base-kanban-lanes-*`, `base-kanban-matrix-*` → `close-*` |
| PV-607 | Editor: a `milestone` box in the project/phase/priority half; details: the phase row ends ` · ◆ milestone`; `M`'s toasts as §1.6 of the contract states them (set, clear, refusal, editor start and refusal) | `base-editor-*`, `base-details-*` → `close-*` |
| PV-608 | The offer per M-3: centred box, title and count, the explanation line, two headings, rows `▣`/`□ title  Project · Mon D · N waits on it`, keys row `space toggle  ·  ↵ convert N  ·  esc not now — won't ask again` (the frame's double spacing; "won't ask again" added, D-618); toasts "Milestones: N converted · backup ‹name› · u undo" / "Not now — this offer won't show again; M makes any task a milestone." | — → `close-offer-*` |
| PV-610 | The kanban header excludes milestones (`25 tasks`): the M-2 frame's header reads 31 while its columns sum to 25 — the columns win (D-622) | `base-kanban-*` → `close-kanban-*` |
| PV-611 | Ruler/band/toast wording for where a milestone went: `M` says "on the ‹project› band" or "shown on the gantt"; `]` on a milestone left drawn says "reached · ◆✓"; after `M` in the kanban the selection jumps to the first card of the nearest drawn column (it may be in another band, ux UX2-4) | — → close toasts (AT) |
| PV-609 | A one-day task that is NOT a milestone keeps the shipped single `◆` in its priority hue (unchanged); only the label's `◆` prefix and the chip tell a milestone | `base-gantt-*` → `close-gantt-*` |

**Raised at P4 for the same verdict** (ux-reviewer, LOW):
- UXV-2: after `M` in the kanban, the selection jumps across bands (PV-611).
- UXV-4: the matrix `prog` column and the lanes per-project counts change because they no longer count milestones (Website 42%→50%, lanes 6→5).
- UXV-5: the reached ash `#6b4a3f` on `#0d1117` is about 2.4:1 by estimate. It reads "quiet" but is close to illegible (PV-601/605).
- UXV-7: a ruler `◆` shortens "September" to "Sep" (PV-603).
- UX-12: `◆` still means the project due, a one-day task and a milestone (PV-609).

The close editor and details captures were re-shot after UXV-1, and now show the milestone.

## Risks / watch-items

- The offer is a modal at start: every app-driven test board holding a candidate would open it (census at P1, seam in increment 004).
- The editor's chip row gains a control: the one-row threshold (canon LLR-001.1) is re-measured.
- Gantt rows: reached milestones become drawn rows — every gantt paging, fold and nav path reads the group's rows.

## Conventions honored

- Test docstrings in the house style (field report · law · RED), AT/TC ids in docstrings and names.
- User text as Text pieces only (S1); toasts `markup=False`.
- Colour budget: accent = focus/today only.
- No new dependency; Textual 8.2.8 / Rich 15.0.0.

## Out-of-scope carries

- US-604 (B2b, D-601); batch C (`6`, the chain map); batch D (flow templates, milestone steps); batch E (presentation); everything else in `BACKLOG.md`.

## Test ledger

| Suite / command | Last run | Result |
|---|---|---|
| increment-001 gate run (frozen r3) | 2026-10-04 | 2346 passed, 1 failed (clipboard environment flake) in 452.81 s (`evidence/inc001-gate-r3.txt`) |
| close gate (004 r2 + P4 test folds) | 2026-10-05 | 2485 passed, 1 failed (clipboard environment flake) in 476.36 s (`evidence/close-gate.txt`) |
| increment-004 gate run (frozen r2) | 2026-10-05 | 2485 passed, 1 failed (flake) in 470.77 s (`evidence/inc004-gate-r2.txt`) |
| `python -m pytest -q -p no:cacheprovider` (base `4b2c13a`) | 2026-10-04 | 2306 passed in 450.07 s, exit 0 (`evidence/base-suite.txt`) |

## Decision log

Mirrors `state.json` `decisions_log`.
