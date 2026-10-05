# Batch close — taskboard — Batch 2026-10-04-batch-01

> **Artifact language.** Canonical **English scaffold**; generate in the batch's language — the **prose**,
> and never a label.

> **Owed in.** `core` ✓ · `full` —

> **Field guide:** `templates/docs/close-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

> **Reserved field names.** The **field names and block keywords below are language-independent** — the
> validator parses them literally and they are never translated:
> `Conditional-gate discharge` · `New controls` · `Human perimeter` · `Human review ledger` · `Gated tree` · `Found before the batch` · `⏸ DEFER`
> **And the §6 DEPTH tokens — cell VALUES rather than field names, reserved for the same reason:**
> `light` · `rigorous` · `spot-check` · `none` · `✅` · `❌`. A CLOSED set.
> Everything else on this page is translated with the batch.

> **Notice convention.** `⚠` yellow = declare and continue · `✗` red = block · `✓` green = satisfied
> **with its citation**.

---

## 0 · Gate record — which tree this close gated

| Field | Value |
|---|---|
| Gate record | Second re-close, 2026-10-04 (D-535): `cd <rev99 snapshot>/dev-flow && python scripts/devflow-validate.py <repo>` from the read-only rev99 snapshot (`1154c8a`, `state.json` `flow_pin`), exit 0, **0 block · 31 notice · 60 not applicable** (`evidence/validator-reclose2.txt`); the re-close (D-531) and the first close gave the same, 0 block · 31 notice (`evidence/validator-reclose.txt`, `evidence/validator-close.txt`). This batch's own notices, declared: `V26` (the live contract ~60k characters against the 54k budget — amendments A-1..A-12 kept in it), `V13` ×3 (the canon quotes three IFC addresses after the fold), `V57` (the tree is dirty: the coordinator commits). Every other notice is inherited from closed batches or the legacy `.dev-flow/03-increments/` |
| Gated tree | `0447070ba1547f2d4b01e217cc2abcf7a98fa1e0` · dirty: every change is still in the working tree, waiting for the coordinator's commit (standing authorization: the coordinator commits and pushes after the operator's visual verdict; this agent does not commit). Files: `taskboard/models.py`, `taskboard/app.py`, `taskboard/views.py`, `taskboard/modals.py`, `taskboard/keymap.py`, `README.md`, `REQUIREMENTS.md`, `.gitattributes`, `tests/kg_board.py`, `tests/test_app.py`, `tests/test_colour_budget_app.py`, `tests/test_dependencies.py`, `tests/test_gantt_board.py`, `tests/test_gantt_polish.py`, `tests/test_kanban_readable.py`, `tests/test_markup_census.py`, `tests/test_markup_sites.py`, new `tests/test_links.py`, `tests/test_link_migration.py`, `tests/test_link_picker.py`, `tests/test_details_links.py`, `tests/test_gantt_link.py`; records `.dev-flow/state.json`, `.dev-flow/BACKLOG.md`, `.dev-flow/2026-10-02-batch-04/decisions-log.json` (rollover), `.dev-flow/2026-10-04-batch-01/` |
| Requirements canon | `REQUIREMENTS.md` (`artifact_homes.requirements_canon`), folded with the rev99 snapshot's `devflow-init.py --fold-canon`: 18 folded, 0 refused at the first close (`evidence/p5-fold-canon.txt`); at each re-close this batch's own 18 uncommitted rows were removed and folded again from the amended statements, 18 folded, then 0 (`evidence/p5-fold-canon-reclose.txt`, `evidence/p5-fold-canon-reclose2.txt`) |

---

## 1 · What changed

**Second re-close (D-535).** Asked at the gate: D-533 "Dejar ◂ solo, quitar la edad antes" — in lanes
the age `·Nd` now drops first, then `▸`, then other meta, and `◂` stays while the title keeps its 6
cells (increment 007, A-12): at 118 columns every waiting lanes card shows `◂N` again; at 80 the due
goes before `◂` (an overdue chip too — ux N-1, BACKLOG). Every other view byte-identical. D-532
"Sí, en todas las plataformas" — the read-only refusal stays cross-platform, recorded as ruled.

**Re-close (D-531, the D-422 path).** The operator's visual verdict (`evidence/operator-verdict-provisional.json`):
PV-1..PV-7 accepted; D-528, D-529, D-530 "Corregirlo antes del push". Increment 006 landed all three:
in the gantt link mode the waiting task's group stays unfolded (pinned in the fold allocation, paged
to the waiter, the rows shared with the candidate's group; one page holds both when it can); a lanes
card keeps 6 cells of title before any mark; a read-only board leaves nothing beside it and the app
still exits fail-closed. (At this re-close the lanes painted no `◂`/`▸` at 118 — D-533, since ruled
and changed by increment 007.) On Linux/macOS a read-only board is now refused too (D-532, ruled).

**A link now means "this task waits on that one", apart from the outside block; the board shows
who waits and who is waited on, says when a task becomes ready, links with `L` from a picker or
on the gantt itself, refuses loops, lists and edits a task's links in its details, will not archive
or delete work others wait on, and an existing board's links were migrated once, with a backup, a
log and `u` to undo.** Cards paint `◂N` (waits on N open tasks) and `▸N` (N open tasks wait on
this) in the muted tone where `⛓` stood; `b` is only the outside block; finishing a task's last
predecessor toasts "‹task› is ready". `L` opens a picker (same project first, by due, a timing hint
per row, loops disabled with their path) or, in the gantt, a link mode drawn on the chart (the
connector from the candidate's due, the overlap days as `═`, `⟲` on loop rows; it says when the
waiter's row is folded). The details view has a Dependencies section (`Waits on`, `Unblocks` down
the chain, conflict lines; `L` `tab` `x` `↵`). Archive and delete — `x`, `d`, the editor's box,
the project manager — are refused with the reason while an open task outside waits on the work. At
start, before the first paint, a board written by the old `b` is migrated once: backup
`‹board›.pre-links-migration`, log `‹board›.links-migration-log`, an atomic save, a version mark so
it never runs again, a toast with `u undo`, and a fail-closed exit that leaves the file untouched.

| Requirement | Version | Verified by | Verdict |
|---|---|---|---|
| HLR-501 | v1 | AT-501 · TC-501..506, TC-518 | pass |
| LLR-501.1 | v1 (A-2) | TC-501 · TC-502 · TC-503 · TC-518 | pass |
| LLR-501.2 | v1 (A-3, A-10, A-12) | TC-504 · AT-501 | pass |
| LLR-501.3 | v1 | TC-505 | pass |
| LLR-501.4 | v1 | TC-506 | pass |
| HLR-502 | v1 | AT-502 · AT-503 · TC-507..512 | pass |
| LLR-502.1 | v1 | TC-507 · TC-508 | pass |
| LLR-502.2 | v1 (A-6) | TC-509 · TC-510 | pass |
| LLR-502.3 | v1 (A-7, A-8, A-9) | TC-511 · TC-512 | pass |
| LLR-502.4 | v1 | `test_readme.py` · `test_keymap.py` | pass |
| HLR-503 | v1 | AT-504 · TC-513 | pass |
| LLR-503.1 | v1 (A-5, A-6) | TC-513 | pass |
| HLR-504 | v1 (A-4) | AT-505 · TC-517 | pass |
| LLR-504.1 | v1 (A-4) | TC-517 | pass |
| HLR-505 | v1 | AT-506 · AT-507 · AT-508 | pass |
| LLR-505.1 | v1 | TC-514 | pass |
| LLR-505.2 | v1 (A-1, A-2, A-11) | TC-515 · AT-508 | pass |
| LLR-505.3 | v1 (A-1) | TC-516 | pass |

Tests: 2218 → 2306. The gate run on the final product (increment 007 frozen r1): **2306 passed in
432.92 s, exit 0** (`evidence/inc007-gate-r1.txt`); after increment 006: 2306 passed in 414.80 s
(`evidence/inc006-gate-r2.txt`). At the first close (increment 005 frozen r3): 2295 passed, 1
failed — `test_win_clipboard_roundtrip`, the Windows clipboard environment flake (G-011; it fails
in its own SETUP, before any product code) — in 444.93 s (`evidence/inc005-gate-r3.txt`). P4: qa
PASS-WITH-NOTES, ux PASS-WITH-NOTES; the light P4 after each re-open: qa PASS-WITH-NOTES, ux
PASS-WITH-NOTES (`04-validation.md`).

**Security close pass (mandatory): `security-reviewer` PASS-WITH-NOTES, no HIGH, no MEDIUM.**
- S1 holds: every new sink in increments 002–005 takes board text as Text pieces or escaped
  markup; toasts `markup=False`; the new census exemption (the link-mode frame, the views seat,
  D-405) is justified — probed with markup payloads at 80 and 118, nothing styled or raised.
- The migration's safeguard is byte-identical to what it passed at increment 001, except
  `save_atomic`'s mode copy (the N1 fold).
- **F1 (LOW):** on Windows a read-only board leaves one read-only temp file per launch (the mode copy
  makes `os.replace` and the cleanup fail; the board, backup and log stay intact). It is in the
  approved migration save path: routed to the operator and BACKLOG, not changed at close (D-530).
- The evidence directory holds no secret and no account path.
- **Re-open delta (increment 006): PASS-WITH-NOTES.** The `save_atomic` delta reviewed (the access
  check is a clearer error, not a boundary; symlinked boards resolved; the cleanup `chmod` touches only
  its own temp file; a cleanup error never masks the save's). F1 is fixed. S1 (a home path in a mutant
  spec) redacted and re-verified. N1–N4 informational (a race still names the temp file; a failed
  unlink can leave one temp file of the board's own mode; POSIX read-only boards now refused).

**Migration safeguard ("Respaldo automático + deshacer") — evidence.** Backup before any change
(AT-506: the backup's bytes equal the pre-start file; a taken name falls through to `.1`); every
change logged (the log lists exactly the changed tasks); revertible (`u` restores every changed task
in one step and keeps the mark, D-517); never twice (a second start leaves board, backup and log
byte-identical, AT-507); fail closed (a failed backup leaves the board untouched and unmarked and the
app exits with a message holding no folder path, AT-508). Re-run at the re-open by `security-reviewer`
on synthetic boards — backup bytes, `.1`, the log, `u` (one step, mark kept), run-once, fail-closed —
all executed and holding, plus the read-only board: three launches, each "board.json: Permission
denied", nothing beside the board, bytes unchanged, unmarked (AT-508 read-only, TC-515 ×2). Only
synthetic boards were used; the operator's real board was never opened.

---

## 2 · New controls discovered — and where they landed (C-45)

| Control | What failure it closes | Measured origin |
|---|---|---|

**The four landings — record which ones actually happened.**

| # | Landing | Done? | SHA / path |
|---|---|---|---|
| 1 | the **command** (`commands/…`) — the rule itself | n/a — no control minted | — |
| 2 | its **artifact** (a template section) | n/a — no control minted | — |
| 3 | the **catalog** entry (`dev-flow-lessons`) | n/a — no control minted | — |
| 4 | **committed and pushed**, manifest re-hashed and bumped | n/a — no control minted | — |

- **New controls:** none — every failure here was caught by an existing control: the product HIGHs (002 F2, 003 F1, 004 F1) by the independent code review; the vacuous or self-referential tests (004 F2's order oracle; the three redundant F1 guards; 005's dead clause) by the mutation batteries (C-40) and positive controls (C-55); a capture that showed the wrong view (E-1) by the ux walkthrough. One stack lesson for the record: rich's `Text.truncate` measures cells, `len()` does not — every clip near a key row is by cells.

---

## 3 · Working-file reconciliation (C-44)

| File | State | Evidence |
|---|---|---|
| every file in §0 *Gated tree* | 📋 ready to commit — the coordinator commits and pushes after the operator's visual verdict (standing authorization "Commit + push tras tu veredicto visual", `merge: false`); this agent does not | `git status --short` |
| `~/.claude` | not touched by this batch (flow pinned to the read-only rev99 snapshot) | — |
| scratch exports, batteries, probes, the rev99 snapshot | outside the repo (session scratchpad), not part of the record | — |

- **Found before the batch:** `none — no tracked file was modified when the batch began`

### Conditional-gate discharge

- **Conditional-gate discharge:** 13 condition(s) · ✅ all discharged

| Condition | Discharged? | The artifact line that proves it |
|---|---|---|
| P2 iteration 1 iterate-to-refine (Q-1, A-1) | ✅ | `02-review.md` §Iteration 2 — four PASS-WITH-NOTES |
| increment 001 code review R2-F1 (HIGH, tests) | ✅ | `03-increments/increment-001.md` §4b |
| increment 002 code review F1 (HIGH, tests) and F2 (HIGH, product — operator "Corregir en el 002") | ✅ | `03-increments/increment-002.md` §4b; `evidence/inc002-f2-red.txt` |
| increment 003 code review F1 (HIGH, product — operator "Corregir en el 003") and T1, T2 (HIGH, tests) | ✅ | `03-increments/increment-003.md` §4b; `evidence/inc003-f1-red.txt` |
| increment 003 R2-2 (the one-phase guard untested) | ✅ | `03-increments/increment-004.md` — the R2-2 arm, mutant Q16 KILLED |
| increment 004 code review F1 (HIGH, product, increment under construction — amendment "Sí, solo en el incremento en curso") | ✅ | `03-increments/increment-004.md` §4b; `evidence/inc004-f1-red.txt` |
| increment 004 F2 (MED, tests) | ✅ | `03-increments/increment-004.md` — Q24 KILLED |
| ux F4 (MED) and qa G-002 | ✅ | `03-increments/increment-005.md`; `04-validation.md` §Orchestrator fold |
| ux E-1 (lanes captures showed the matrix) | ✅ | `evidence/captures/{base,close}-kanban-lanes-*` re-shot with `4 tab tab` |
| the operator's D-528, D-529, D-530 "Corregirlo antes del push" | ✅ | `03-increments/increment-006.md`; `evidence/inc006-red.txt` |
| increment 006 code review M1 (MED, product) | ✅ | `03-increments/increment-006.md` §4b; `evidence/inc006-m1-red.txt` |
| security delta S1 (a home path in the evidence) | ✅ | `03-increments/increment-006.md` §4b — re-verified by the reviewer's grep |
| the operator's D-533 "Dejar ◂ solo, quitar la edad antes" | ✅ | `03-increments/increment-007.md`; `evidence/inc007-red.txt`, `evidence/inc007-identity.txt` |

---

## 4 · Backlog reconciliation — the carry-over contract

| Item | Move | Reference |
|---|---|---|
| Batch B (kg_mejoras): waits-on links, `L`, details section, guard, migration (B1) | done | HLR-501..505 |
| Batch B2: milestones, moving linked dates, the M-3 offer | added | D-501 |
| The gantt link mode can fold the waiter's row — the fold rule | added, then done at the re-open | ux F4, D-528, increment 006 (A-9) |
| A lanes card can lose its whole title | added, then done at the re-open | ux U-2, D-529, increment 006 (A-10) |
| A read-only board on Windows leaves a temp file per launch | added, then done at the re-open | security close F1, D-530, increment 006 (A-11) |
| Present a whole project (gantt, tasks and their text; export SVG or an image) | added — a prototype round first | the operator's request with the verdict |
| Lanes show no link marks below about 140 columns | added, then done at the second re-open | ux R6-3, D-533, increment 007 (A-12) |
| At 80 columns an overdue waiting lanes card loses its overdue chip | added | ux N-1 (007) |
| Lanes test and wording details | added | qa G-009, G-010; ux N-2, N-3 (007) |
| Link-mode paging details ("folded" for a paged-out waiter; the shared group's pager) | added | ux R6-1, R6-2 |
| The read-only exit advice names the folder | added | ux R6-4 |
| `python -m taskboard` exits 0 after a fail-closed stop | added | ux R6-5 (pre-existing) |
| `critical_chain` recursive and exponential | added | security S-6 (pre-existing) |
| An unreadable board is saved over by the renumber notice | added | security S-13 (pre-existing) |
| Render cost on boards of thousands of tasks | added | code review 002 F8 |
| `◂` carries several meanings | added | ux UX-22, PV-1 |
| Both `L` surfaces start on a linked candidate | added | ux U-3 |
| Link-mode details (`═` past the waiter's due; the waiter's selection mark) | added | ux U-4, U-5 |
| 80-column details (grouped `◂`, picker rows, toast and legend clips) | added | ux U-6, U-7, N-5, N-6 |
| Wording seams between the two `L` surfaces and the toasts | added | ux N-1..N-4, N-7 |
| The picker lists every open task | added | increment 003 risk |
| A comment overstates the line-map rule | added | code review 005 NIT |
| Base ref + refresh date | bumped to `0447070` · 2026-10-04 | `BACKLOG.md` header |

### Visual decisions — the operator's verdict (2026-10-04, `evidence/operator-verdict-provisional.json`)

Each is the most conservative reversible reading where the verdict frames left a detail open
(`PLAN.md`). Captures under `evidence/captures/` (`.svg` + `.txt`, 118×30 and 80×24; base from
`0447070`, close from the product as first closed; `close2-*` after increment 006 — `close2-kanban-lanes-{118x30,80x24}` (D-529), `close2-gantt-link-{118x30,80x24,118x20}` (D-528; at 118×20 the waiter's row now drawn where it folded); `close3-kanban-lanes-{118x30,80x24}` after increment 007 (D-533: `◂N` on every waiting card)).

| Id | Decision | Captures (before → after) | ux recommendation → operator verdict |
|---|---|---|---|
| PV-1 | card marks `▸M ◂N` muted where `⛓M` stood, `▸` shed first; `◂` also the conflict prefix, the details heading and the gantt off-window glyph (on cards always with a count) | `base-kanban-118x30` → `close-kanban-118x30`; `base-kanban-80x24` → `close-kanban-80x24`; `base-kanban-lanes-118x30` → `close-kanban-lanes-118x30`; `base-kanban-lanes-80x24` → `close-kanban-lanes-80x24` | keep for grouped; change for lanes — a card's title can be shed to nothing (U-2, D-529: a fix conflicts with shipped width contracts) → **accepted** (2026-10-04) |
| PV-2 | the gantt keeps its one-cell `↳` gutter on the open-predecessor rule; no `◂N▸N` in the gantt label | `base-gantt-118x30` → `close-gantt-118x30`; `base-gantt-80x24` → `close-gantt-80x24` | keep → **accepted** (2026-10-04) |
| PV-3 | the picker: a centred modal — title, filter, count, "linked now", create row, two sections of two-line options, keys line | — → `close-picker-118x30`, `close-picker-80x24` | keep (U-3, U-7 to BACKLOG) → **accepted** (2026-10-04) |
| PV-4 | the dependency section in the details view after the info grid; keys on its heading (A-5) | `base-details-118x30` → `close-details-118x30`; `base-details-80x24` → `close-details-80x24` | keep → **accepted** (2026-10-04) |
| PV-5 | link mode: a full-screen gantt with the candidate as the selection; bright connector from its due; `═` over-tone overlap on the waiter's row; three status rows (A-7); the folded-row note (A-8) | — → `close-gantt-link-118x30`, `close-gantt-link-80x24` | keep the design; change the fold rule (F4 — the waiter's group can fold; D-528) → **accepted** (2026-10-04) |
| PV-6 | the migration, guard and ready toasts' wording | — → `close-migration-*`, `close-guard-*`, `close-ready-*` | keep (N-3, N-5 to BACKLOG) → **accepted** (2026-10-04) |
| PV-7 | a start ON the predecessor's due day is a 1-day conflict; "overlaps Nd" | `base-gantt-*` → `close-gantt-*`; `close-picker-*` | keep → **accepted** (2026-10-04) |

---

## 5 · Batch metrics — the 13 keys of `core`

```yaml
type: dev-flow-batch
project: taskboard
batch_id: 2026-10-04-batch-01
mode: core
verdict: pass
increments: 7
source_files_max: 4
notices_raised: 31
rework_returns: 10               # P2 iterate-to-refine; 001 R2-F1; 002 F1 + F2 (stop); 003 F1 (stop) + T1/T2; 004 F1; the P4 fold (increment 005); the re-opens (increments 006, 007)
triggers_fired: "B1,B4,C,D,E,F2"
tests_base_to_post: "2218 -> 2306"
new_control: none
open_items_next: 19
```

---

## 6 · Human review ledger — what a human audited, at what depth

| Artifact | Machine verdict (citation) | Human review | Depth | Deliberately NOT reviewed |
|---|---|---|---|---|
| Increment 002 code-review HIGH F2 (Setup `x`) and D-515, D-517 | `03-increments/increment-002.md` §4b | ✅ operator rulings "Corregir en el 002", "Sí, conservarla", "Sí, no vuelve a correr" | `spot-check` | the diff |
| Increment 003 code-review HIGH F1 and the authorization amendment | `03-increments/increment-003.md` §4b | ✅ operator rulings "Corregir en el 003", "Sí, solo en el incremento en curso" | `spot-check` | the diff |
| The B1/B2 split (D-501) | `01-requirements.md` | ✅ confirmed by the operator | `spot-check` | — |
| D-532, D-533 (the re-close side effects) | `05-close.md` §1 | ✅ asked at the gate: "Sí, en todas las plataformas", "Dejar ◂ solo, quitar la edad antes" | `spot-check` | the code |
| PV-1..PV-7 and D-528..D-530 on the captures | `04-validation.md` UX walkthrough | ✅ the operator's verdict, 2026-10-04: PV-1..PV-7 "Aceptar"; D-528, D-529, D-530 "Corregirlo antes del push" (`evidence/operator-verdict-provisional.json`) | `spot-check` | the code |

- **Human perimeter:** the operator (Javier) owns: the look of the `close2-*` and `close3-*` results, whether overdue should outrank `◂` at 80 columns (ux N-1), the first start of the new version on the real board (backup `‹board›.pre-links-migration`, `u` to undo; a read-only board stops with its name), the prototype round for the presentation feature, and the commit and push.
- **Human review ledger:** human:Javier — 5 decision points reviewed (rulings at the P3 gates; the split; the visual verdict; the re-close rulings), 0 rigorous · 0 declared not-reviewed
