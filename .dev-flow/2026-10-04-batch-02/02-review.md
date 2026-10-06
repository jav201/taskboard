# Review — taskboard — Batch 2026-10-04-batch-02

> Phase 2 artifact (flow `templates/review-template.md`, rev100). Reviewers in parallel, each spawned
> as an independent named sub-agent told to follow the bundle's `agents/<role>.md`: `architect` ∥
> `qa-reviewer` ∥ `security-reviewer` (family C: C5, C6, C8) ∥ `ux-reviewer` (family D). Their probes
> ran on synthetic boards in the session scratchpad; no repo file was changed by a reviewer. The
> orchestrator alone writes this record from the rows they returned.

## ✅ Verdict (read first) — iteration 1

- **Gate:** `iterate-to-refine` → Phase 1 (2 blockers: Q-1, A-1; requirement-defect majors). **No HIGH**: security PASS-WITH-NOTES, 0 HIGH (5 MEDIUM, 4 LOW). The fold is self-approved under the standing authorization; every disposition is recorded below and in the contract's §6.2 (D-611..D-625).
- **Out-of-scope findings:** 3 named and routed → `BACKLOG.md` at close: S-4's same pattern in `run_link_migration`; S-9 (a non-string title crashes the shipped app); A-14 (B2b notes).
- **Findings:** 2 blocker · 21 major · 32 minor (architect 1/3/10, qa 1/12/12, security 0/0/9 = 5 MEDIUM + 4 LOW, ux 0/4/10).
- **Verdicts:** architect FAIL · qa-reviewer FAIL · security-reviewer PASS-WITH-NOTES · ux-reviewer FAIL.
- **shall/should check:** ✓ clean (qa: 0 modal `should` in HLR/LLR statements).
- **Two-layer (blockers):** ✓ every story has an `AT`; ✗ A-1: AT-601's sync arm observes no shipped surface; ✗ Q-1: AT-603's band literal cannot be produced at 118 columns.
- **Census (change-first):** best-effort + gate-confirmed; extended by A-4 (`_notify_folded`, `_select_first`), A-5 (every `GanttGroup.open` reader), Q-24/A-10 (byte/mtime observers of the board after an app start).
- **Security:** ⚠ 9 findings (5 MEDIUM, 4 LOW), 0 HIGH.
- **Evidence checklists:** ✓ all four reviewers attached theirs (summarised below).

## Detail

### Findings and dispositions (iteration 1)

"Folded" = written into the iteration-2 contract (`01-requirements.md`, ledger LED .2).

| ID | Reviewer | Sev | Req | What | Disposition |
|---|---|---|---|---|---|
| Q-1 | qa | blocker | HLR-603 / AT-603 / LLR-603.2 | AT-603's Website Redesign literal (68 cells) cannot fit the room the shipped band facts leave at 118 (56 cells; 18 at 80) | Folded: the room is defined (`w − facts − 4 − 2`), the segments re-executed with the prototype's layout at the shipped rooms of every band at 118 and 80 (`evidence/p1-thresholds-shipped.txt`), the AT literal is that output; TC-613 adds the real rooms |
| A-1 | architect | blocker | HLR-601 / AT-601 | the sync arm ("`"yes"` → not a milestone") has no shipped surface: teammates' tasks show only in the people view, which draws no milestone mark | Folded: the arm leaves AT-601; TC-601 (`"yes"` arm) and TC-607 (push writes `true`, pull reads `true` and refuses `"yes"`) cover it white-box |
| Q-2 | qa | major | AT-603 | the Ops & Security band is below the fold at 118×30 | Folded: the Ops arm runs at 118×50, measured to draw every band (`p1-thresholds-shipped.txt`) |
| Q-3 | qa | major | AT-602 | two arms pass on base (the Launch `◆` = the project due's cell; `Oct 10` is already the chip) | Folded: the discriminating ruler arm selects `Revenue model signed off` (+18 vs Data Warehouse due +60); the date arm reads field cells only, `Mon D` of today+10 |
| Q-4 | qa | major | AT-602 | "`↓` from the row above `Mockups approved`" is a header | Folded: "`↑` from `Build component library` selects `Mockups approved`; `↓` returns" |
| Q-6 | qa | major | LLR-605.4 / AT-604 | initial highlight and `space` on a heading unstated; converted set unnamed | Folded: the first row is highlighted at open; `space` on a heading does nothing; the converted set is {`ta3`, `tw5`, `tm5`, `to3`} minus what the AT unchecks (Q-8) |
| Q-7 | qa | major | AT-604 (C-12) | no fresh app reads the converted file before `u`; B4 wording wrong | Folded: after `↵`, a fresh app on the saved file shows no offer and draws the converted milestones (`3`: label ` ◆ Launch new homepage`); B4 wording corrected (the backup is the operator's manual restore; `u` uses the session's undo entry) |
| Q-8 | qa | major | AT-604 (C-10) | nothing unchecks a pre-checked row | Folded: AT-604 unchecks `ta3` (`space`) and checks `to3`; `ta3` stays a plain one-day task in file and log |
| Q-9 / A-10 / Q-24 | qa, architect | major / minor / minor | §5 seam / D-611 | the seam's mechanism and self-control are unstated; it writes a mark at every app start | Folded (D-611): `tests/conftest.py` autouse fixture patches the app module's reference `taskboard.app.milestones_marked` to answer True unless the test is marked `milestone_offer` — the base suite's file I/O is unchanged (no extra save at 541 starts); two seam controls in `test_milestone_offer.py`; after increment 004 the census is re-run; why not fixture marks: 27 files write their own boards |
| Q-10 / UX-5 | qa, ux | major / minor | HLR-603 vs M-2 | the frame's header says `31 tasks` while its columns sum to 25 | Folded: PV-610 — the header excludes milestones (the frame's columns win over its header), for the operator's verdict |
| Q-11 | qa | major | C-36 | literals neither constants nor NEW | Folded: §1.6 lists every NEW literal and constant |
| Q-12 | qa | major | HLR-601 / AT-601 | the "kept by search, archive, links" clause has no arm; no positive sync arm | Folded: TC-608 (archive/unarchive keeps the flag, search finds it, links survive); TC-607 positive and negative sync |
| Q-13 | qa | major | AT-603 (C-10) | the grouping control `g` is never driven | Folded: AT-603 presses `g` (priority): no `◆` on any rule, counts unchanged |
| A-2 / S-3 / Q-16 | architect, security, qa | major / MEDIUM / minor | HLR-605 | "pre-start bytes" vs the backup taken after the renumber, sweep and link saves | Folded (D-612): the backup holds the board file's bytes read once, immediately before the conversion's own write, in the same run; the AT board carries the renumber key, the links mark and no sweepable task (pre-start = pre-conversion); TC-615 arm where an earlier write happened (bytes read after mount) |
| A-3 | architect | major | D-605 / LLR-601.3 | an edited start of a milestone is silently reset; no writer census; a stored start ≠ due | Folded (D-613): the due is the date; a ticked box with a typed start ≠ due → the start follows the due and the toast says so; writers enumerated (set_milestone, bump_due, editor apply, the add path pops the key; load and pull never normalize; B2b later); a stored milestone with start ≠ due is read by its due everywhere and never rewritten on load |
| A-4 / UX-1 | architect, ux | major / major | LLR-602.1, LLR-603.1 | `_notify_folded` lies for a reached milestone row; `_select_first` lets the kanban selection rest on an undrawn milestone (F-3) | Folded (D-614): `]` on a milestone that stays drawn says "‹title› reached · ◆✓ · u undo", not "folded"; in the kanban (every presentation) the selection is never a milestone — it moves to the nearest drawn card by the grouped z rule; `app.py` joins increments 002 and 003; AT-603 arm: `M` on a card leaves the selection on a drawn card and the next `]` moves THAT card |
| UX-2 | ux | major | LLR-605.4 | `esc` "not now" promises a later chance | Folded (PV-608): keys row `space toggle  ·  ↵ convert N  ·  esc not now — won't ask again`; the "Not now" toast 30 s |
| UX-3 | ux | major | LLR-605.4 | the fit with 30+ candidates at 80×24 unstated | Folded: the box stays inside the screen, the title and keys row stay painted, the list scrolls the highlighted row into view, long titles cut with `…` before the meta; TC-617 boundary with 34 candidates at 80×24 |
| UX-4 | ux | major | PV-604 | appended legend items never show at 80 | Folded (PV-604): `◆ milestone · ◆✓ reached` sit right after `selected` (the frame's order); asserted at 118 and 80 (`assumed — verify in Phase 3`: the 80-col legend width) |
| Q-5 | qa | minor | AT-602 | "when in window" makes an arm vacuous | Folded: asserted unconditionally (premise: the window starts before today−12, base capture) |
| Q-14 / UX-6 | qa, ux | minor | HLR-603 | band `N open` / `N high ↑` and the fold row's counts | Folded: they exclude milestones; the gantt's `N open` counts open milestones (D-606) — stated so it does not read as a bug |
| Q-15 | qa | minor | AT-606 | fault injection unstated | Folded: the stdlib `open` refuses names holding `.pre-milestones` (B1 AT-508 precedent) |
| Q-17 | qa | minor | LLR-601.3 | `-k` deselects test_edit_window | Folded: two commands |
| Q-18 | qa | minor | §5 | TC-607, TC-608 unassigned | Folded: TC-607 (sync), TC-608 (field kept by archive/search/links) |
| Q-19 | qa | minor | LLR-602.1 | "followed by" vs merged | Folded: "merged by due (stable)" |
| Q-20 | qa | minor | HLR-605 | nothing checked + `↵`; unreadable load; both migrations on one start | Folded: TC-616 arms — `↵ convert 0` = `esc`; no offer on an unreadable load; link migration and offer on one start: two toasts, two undo entries, `u` reverts the offer first |
| Q-21 | qa | minor | C-39 | the count threshold lacked its command | Folded: re-run as `p1_thresholds_shipped.py` |
| Q-22 | qa | minor | LLR-601.3 | the fold boundary named 121/122 | Folded: N−1 / N of the re-measured `TASK_CHIPS_ONE_ROW` |
| Q-23 | qa | minor | captures | unshifted board sweeps `tw1` and drifts 4 days | Folded: `capture_b2.py` uses `kg_board.shifted`; the base captures re-taken (still base product bytes) |
| Q-25 | qa | minor | PV-608 | keys row spacing | Folded: the frame's double spacing |
| A-5 | architect | minor | LLR-602.1 | `GanttGroup.open` readers unlisted | Folded: LLR-602.1 lists the readers that move to `rows` and those that stay on `open` |
| A-6 | architect | minor | LLR-605.3 | the undo entry shape | Folded: its own key `milestones` with its own toast |
| A-7 / UX-14 / S-7a | architect, ux, security | minor | LLR-605.3 | order vs `_init_team_mode`; quit with the offer open | Folded (D-615): the offer is `on_mount`'s last step (after the identity picker, which it covers until answered); teammates see conversions at the next push; quitting unanswered leaves the board unmarked → offered again (TC-616 arm) |
| A-8 / S-8 | architect, security | minor / LOW | LLR-605.3 | a read-only board would say "offer stopped" at every start for an offer never shown | Folded (D-616): a mark-only write that fails when no offer was shown is silent; the failure toast is said only for an answered offer |
| A-9 | architect | minor | LLR-605.3 | a simpler seat for a created board | Folded (D-617): `Board.load` seeds a new board already carrying both marks (`links`, `milestones`) — new-model data, as `kg_board.build`; no "created" branch |
| A-11 / UX-11 | architect, ux | minor | HLR-603 | a project whose only open items are milestones has no band; search counts | Folded: stated in HLR-603 (no band, its milestones not in the kanban — PV-605); the `/` filter counts keep counting milestones (unchanged); BACKLOG for a rule-only band |
| A-12 / A-13 | architect | minor | D-603 | field position; the synced-format consequence | Folded: after `phase_changed`; every saved/pushed task now carries `"milestone": false` (additive; older apps keep it in `extra`) |
| A-14 | architect | minor | B2b | cascade notes | Routed: BACKLOG B2b entry (the cascade wraps `bump_due`/`set_milestone`; the due is authoritative; re-derive against `Task.milestone`) |
| S-1 | security | minor · MEDIUM | LLR-602.2 | no S1 arm on the gantt label | Folded: the title through the views' escape; TC-610 arm `[b]x[/b]`, `[/]`, a trailing `\` paint literally |
| S-2 | security | minor · LOW | LLR-605.4 | project names come from `team.json` too | Folded: TC-617 S1 arm on a project name |
| S-4 | security | minor · MEDIUM | LLR-605.2 | cleanup `unlink` inside the handler can raise and skip the restore | Folded: memory and the mark restored first; removing created files best-effort, errors swallowed; the first error returned; TC-615 arm with a failing unlink; the same pattern in `run_link_migration` → BACKLOG |
| S-5 | security | minor · MEDIUM | LLR-605.2/605.4 | a repeated chosen id; a non-string id lost in a string option id | Folded: conversion iterates the candidates (each at most once); the screen returns the candidates' own ids by option index, never a re-parsed string; TC arms |
| S-6 | security | minor · MEDIUM | HLR-605 | a sync tick can make a checked task ineligible | Folded: the conversion re-reads the candidates at answer time; the toast counts what was converted and adds `· K no longer eligible` |
| S-7b/c | security | minor · LOW | HLR-605 | restoring the backup re-offers; a replaced malformed mark unlogged | Folded: stated (README/log); replacing a present non-1 mark value forces the backup and log, the log keeping the replaced value (B1 S2-2) |
| S-9 | security | minor (pre-existing) · LOW | — | a non-string title crashes the shipped app | Folded: candidates exclude a non-`str` title; the crash → BACKLOG |
| UX-7 | ux | minor | LLR-601.2 | "more layer lists `M Milestone`" cannot pass at 118 | Folded: the `?` Keys section lists `M  Milestone` in the five views; the bar shows the key or counts it in `+N` |
| UX-8 | ux | minor | LLR-601.2 | where the task went | Folded: the toast says `· on the ‹project› band` (grouped, project grouping) or `· shown on the gantt` |
| UX-9 | ux | minor | HLR-601 | a moved start is silent; refusal severity | Folded: `· start was Mon D` when the start moved; refusal `severity="warning"` |
| UX-10 | ux | minor | PV-602 | every reached milestone is a row | Folded: PV-602 says all, by date |
| UX-12 | ux | minor | PV-609 | `◆` carries three meanings | Folded: the label prefix asserted; noted for the operator |
| UX-13 | ux | minor | LLR-602.3/603.2 | kanban help/legend silent; `today` tone | Folded: a kanban help bullet and legend entry; `today` in the soon tone |

### shall / should check
✓ clean — 0 modal `should` in HLR/LLR statements (qa grep).

### Two-layer acceptance review (blockers)

| Story / Req | (a) AT present | (b) deliverable+method named | (c) both chains | (d) black-box pure | Status |
|---|---|---|---|---|---|
| US-601 | yes (AT-601) | yes | yes | no — the sync arm (A-1) | blocker → folded |
| US-602 | yes (AT-602) | yes | yes | yes | ✓ (Q-3/Q-4 majors folded) |
| US-603 | yes (AT-603) | yes | yes | yes | blocker Q-1 → folded |
| US-605 | yes (AT-604..606) | yes | yes | yes | ✓ (Q-6..Q-8 folded) |

### Supersession census (change-first)
Planned edits: `models.py`, `app.py`, `modals.py`, `keymap.py`, `views.py`, `tests/kg_board.py`, `tests/conftest.py` (NEW), four new test files. Families: B1 symbols (`p0-probes.txt` §B1), plus `_notify_folded`, `_select_first`, every `GanttGroup.open` reader (A-5), `CONTRACT_IDS` in `test_edit_window.py` (canon LLR-001.3: the editor's widget ids — amended by LLR-601.3), the key bar width tests, the README key table. Best-effort; each increment gate's reverse census is the completeness guarantee.

### Security review summary
`security-reviewer` PASS-WITH-NOTES, 0 HIGH: S-1, S-3, S-4, S-5, S-6 MEDIUM; S-2, S-7, S-8, S-9 LOW. Checked closed: the synced flag read only as `True`; teammates' tasks never enter `board.tasks` (the offer, gantt and kanban read `board.tasks` only); settings are never synced (a teammate cannot set or clear the mark); backup/log names never match the pull's `board.*.json`; exclusive create; the read-only refusal; toasts `markup=False`. Probes: keys cannot change the board behind a modal (only timers can — S-6).

### Evidence checklists — architect · qa-reviewer · security-reviewer · ux-reviewer
- architect: constraints ✓; alternatives weighed (D-603, A-9, A-10) ✓; n/a with reasons ✓; rationale ✗ for D-605 and the backup timing (A-2, A-3 → folded); risks ✓; what would change D-609/D-611 ✗ (→ §6.2); two-layer ✗ (A-1 → folded).
- qa-reviewer: plan-mode, all `planned`; observable outcomes ✓; arms that cannot go RED ✗ (Q-3..Q-5 → folded); exact values ✗ (Q-1, Q-6 → folded); edge arms ✗ (Q-8, Q-20 → folded); regression census ✓; no PII ✓ (synthetic); Layer B ✗ (Q-7, Q-12 → folded); reachability ✗ (Q-2, Q-13 → folded); unfilled ids ✗ (Q-18 → folded).
- security-reviewer: what/where/why/fix ✓; severities ✓; no secrets ✓; verdict explicit, 0 HIGH ✓; new tool n/a — no integration.
- ux-reviewer: context of use ✓ (added to §2.3); observable criteria ✓; declared limits: text captures and frames only, no live walkthrough, no colour read from renders, UX-1/UX-7 from code, no user evaluation (single-operator product).

## ✅ Verdict — iteration 2 (the same four lenses re-read the amended contract)

- **Gate:** `iterate-to-refine` → Phase 1 (0 blocker; 3 requirement-defect majors — a major is never folded in place). **No HIGH.**
- **Verdicts:** architect FAIL (one major, A2-1) · qa-reviewer PASS-WITH-NOTES (3 majors) · security-reviewer PASS-WITH-NOTES (0 HIGH, no new finding) · ux-reviewer PASS-WITH-NOTES (4 new minors).
- **Iteration-1 discharge (re-read by each lens):** architect 13 DISCHARGED, A-11 PARTIAL; qa 21 DISCHARGED, Q-9, Q-11 PARTIAL (minor), Q-12 PARTIAL (major); security 8 DISCHARGED, S-7 PARTIAL (b, LOW); ux 13 DISCHARGED, UX-10 PARTIAL.
- **Findings:** 0 blocker · 3 major · 9 minor.

| ID | Reviewer | Sev | Req | What | Disposition |
|---|---|---|---|---|---|
| A2-1 / Q2-2 | architect, qa | major | LLR-602.1 / HLR-602 | `]` on `Launch new homepage` (Backlog) moves it one phase, never to Done: no reached toast | Folded: `]` pressed until it reaches Done (four presses), the reached toast at the last; a reached arm added to AT-602 |
| Q2-1 / A2-2 | qa, architect | major | HLR-601 / AT-601 | after `M` in the kanban the milestone can never be re-selected there | Folded: AT-601 runs in the gantt (`3`), reaching `Rate limiting` with `↓` |
| Q-12 | qa | major (partial) | HLR-601 / AT-601 | no AT reads the pushed `board.<user>.json` | Folded: AT-601 team arm — a tmp team folder, a short sync interval, `M`, the pushed file re-read holds `"milestone": true` |
| A2-3 | architect | minor | LLR-603.1 | the z rule's column index in the lanes window | Folded: "the nearest drawn column at or left of its phase, in the presentation's own column order"; TC-612 arm on a lanes window not starting at Backlog |
| A2-4 / A-11 | architect | minor | HLR-603 | the `/` filter's counts | Folded: HLR-603 says the filter's counts keep counting milestones (unchanged) |
| Q-9 | qa | minor (partial) | §5 | the census re-run has no pass condition | Folded: ≥ 274 suppressed starts and 0 offer screens in unmarked nodes |
| Q-11 | qa | minor (partial) | §1.6 | "the title cut at 40" | Folded: §1.6 row (the shipped `clip(…, 40)` toast convention) |
| Q2-3 | qa | minor | P-18 | "render height 30" reads as a terminal size | Folded: "render height 30 (the kanban panel; a 118×40 terminal; at a 118×30 terminal Ops folds below)" |
| UX2-1 | ux | minor | LLR-601.2 | ‹where› untrue for the last open card of a project or an Inbox milestone | Folded: ‹where› is "on the ‹project› band" only when a band will carry it (a `Project` with an open non-milestone card), else "shown on the gantt"; TC-604 arms |
| UX2-2 | ux | minor | HLR-603 / PV-605 | at a 118×30 terminal the late Ops milestone is below the fold | Folded: stated in PV-605; a fold-row late marker → BACKLOG |
| UX2-3 | ux | minor | PV-607 | stale toast wording | Folded: PV-607 points to §1.6 |
| UX2-4 | ux | minor | LLR-603.1 | the replacement selection can jump far | Folded: named in PV-611 |
| UX-10 | ux | minor (partial) | PV-602 | no capture with ≥ 3 reached milestones | Folded: a close capture `close-gantt-reached-*` with three reached milestones in one group |
| S-7b | security | LOW (partial) | HLR-605 | "a restored backup is offered again" not in a requirement | Folded: LLR-605.2 — the log states it (a `note` field), checked by TC-615 |

## ✅ Verdict — iteration 3 (the four lenses re-read the delta, LED .3)

- **Gate:** `approve` → Phase 3. 0 blocker · 0 major · 4 minor, folded at the gate (LED .4). **No HIGH.**
- **Verdicts:** architect PASS (A2-1..A2-4, A-11 DISCHARGED) · ux-reviewer PASS (UX-10, UX2-1..UX2-4 DISCHARGED; UX3-1 minor) · qa-reviewer PASS-WITH-NOTES (Q2-1..Q2-3, Q-9, Q-11, Q-12 DISCHARGED; Q3-1..Q3-3 minor) · security-reviewer PASS-WITH-NOTES (S-7b PARTIAL LOW, no new finding; carried to increment 001's gate: the AT's team folder is `tmp_path`, never a default path).

| ID | Reviewer | Sev | Req | What | Disposition |
|---|---|---|---|---|---|
| Q3-1 | qa | minor | AT-601 | no stated wait for the push | Folded: polled for at most 5 s |
| Q3-2 / UX3-1 | qa, ux | minor | HLR-603 | the filter-count clause had no arm and contradicted the exclusion list | Folded: the kanban's `/` `N of M` excludes milestones; TC-612 arm `0 of 25` |
| Q3-3 / S-7b | qa, security | minor · LOW | LLR-605.2 | the log's `note` unchecked | Folded: the threshold asserts it |
