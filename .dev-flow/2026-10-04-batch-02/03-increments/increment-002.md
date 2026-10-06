# Increment 002 — HLR-602 (LLR-602.1, LLR-602.2, LLR-602.3) · the gantt draws milestones as dates, not bars

> **Where this lives:** the repo, next to the diff — `.dev-flow/2026-10-04-batch-02/03-increments/increment-002.md`.
> Template `templates/increment-template.md` (rev100); notice convention `⚠` notice · `✗` block · `✓` with evidence.

| Field | Value |
|---|---|
| Batch | `2026-10-04-batch-02` |
| Increment | `002` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | HLR-602; LLR-602.1, LLR-602.2, LLR-602.3; D-606, D-614, D-624 |
| Acceptance | AT-602 · white-box TC-609, TC-610, TC-611 |
| Agent | `software-dev` (this runtime) |
| Date | `2026-10-04` |

---

## 1 · What changed

**The gantt draws a milestone as a date (M-1).** Its row reads ` ◆ title`, its field a `◆` on its
date with `Mon D` beside it and no bar, its chip `in Nd`, `today` (soon), `▲Nd` (over) or `✓ done`. An
upcoming milestone wears its project's hue, a late one the over tone, a reached one is `◆✓` with its
label and date in ash and stays a row among its group's open rows, by date, while the group has open
work (it still counts in `✓n`). The ruler's month row marks the selected project's milestones `◆` in
those tones (AX-2). The legend row names `◆ milestone · ◆✓ reached` right after the selection item
(the M-1 frames' order — kept at 80 columns); the `?` map and the gantt help name them. `]` that
finishes a milestone left drawn says "‹title› reached · ◆✓ · u undo" instead of "folded". The arrows
walk every drawn row. A one-day task that is not a milestone keeps the shipped single `◆` (PV-609).

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/views.py` | source | LLR-602.1, LLR-602.2, LLR-602.3 | `GanttGroup.rows`; `gantt_plan` unfolds by rows; `milestone_tone`, `gantt_milestone_cells`, `gantt_milestone_chip`; `_gantt_field`'s drawn space; the milestone row in `_gantt_frame`; month-row marks; `_gantt_legend` items; frame paging/pin/selection by rows; `nav_model("gantt")` by rows; `legend_entries` / `help_usage` gantt; `gantt_link_order` docstring |
| `taskboard/app.py` | source | LLR-602.1 | `_notify_folded`: the reached toast for a milestone left drawn |
| `README.md` | doc | | the gantt paragraph of the Milestones section |
| `tests/test_gantt_milestones.py` | test | HLR-602, LLR-602.1, LLR-602.2, LLR-602.3 | NEW: TC-609..TC-611, AT-602 (29 nodes) |

| Count | Value |
|---|---|
| **SOURCE files** | **2 / 4** |
| Test files | 1 (uncapped) |
| Doc files | 1 (outside the count) |

## 3 · How to test

```bash
python -m pytest -q -p no:cacheprovider tests/test_gantt_milestones.py
python -m pytest -q -p no:cacheprovider tests/test_gantt.py tests/test_gantt_board.py tests/test_gantt_link.py tests/test_gantt_polish.py tests/test_legend.py
python -m pytest -q -p no:cacheprovider          # the gate
```

## 4 · Test results

| Layer | Owed in | Nodes | Result |
|---|---|---|---|
| **0 · unit** | `core` · `full` | TC-610 (chips/tones ×6, cells ×5, today/no due/Inbox, last column) | passed |
| **A · white-box** `TC-NNN` ↔ LLR | `core` · `full` | TC-609 (7), TC-610 (S1 ×3), TC-611 (5) | passed |
| **B · black-box** `AT-NNN` ↔ story | `core` · `full` | AT-602 | passed |

Gate run on frozen r2: `python -m pytest -q -p no:cacheprovider` → **2375 passed, 1 failed** in 456.72 s — the one failure is `test_win_clipboard_roundtrip`, the known environmental clipboard flake (G-011) (`.dev-flow/2026-10-04-batch-02/evidence/inc002-gate-r2.txt`). r1 (superseded by the G-1/G-2 folds): 2372 passed, 1 failed (the same flake) (`inc002-gate-r1.txt`) — this agent first said r1 had finished before its result was on disk (code review G2-1); the transcript now holds it. The larger failure counts in the cited evidence come from the deliberately failing transcripts (the batteries and the RED captures), never from a gate run.

### RED counterfactual — executed, not predicted

| Field | Value |
|---|---|
| **RED counterfactual** | the increment-002 tests on the increment-001 tree (`views.py` at `4b2c13a`, `app.py` without the 002 hunk), the three new helper names stubbed to raise so every arm runs: 24 of 26 arms RED (`evidence/inc002-red-on-inc001.txt`); the 2 GREEN arms are labelled regression pins (C-40 corollary): "a selected reached milestone unfolds its group" (the shipped seat already unfolds a selection's group) and "a project without milestones marks only its due" (a negative control). The folds RED-first: G-2 `inc002-g2-red.txt` → `inc002-g2-green.txt` |

| Field | Value |
|---|---|
| **Mutation verdicts** | **16 of 16 KILLED** (`evidence/inc002-mutations-r2.txt`, spec `mutants_inc002_r2.json`, built by `mk_mutants_inc002.py`), per resolved node, every restore hash OK: G1 reached milestones never rows · G2 appended, not merged by due · G3 reached rows without open work · G4 nav walks `open` · G5 a reached milestone in its hue · G6 today chipped late · G7 a milestone drawn as a bar · G8 legend items appended last · G9 ruler marks from every project · G10 a reached title not ash · G11 `]` says folded · G12 an unescaped title · G13 the off-window `◆` covers the edge glyph · G14 no space before the date · GR the frame's selection test reads `open` (the reviewer's mutant R) · GE the last-column clamp (G-2). r1: 14/14 (`inc002-mutations.txt`) |

### Instrument RED-proof

| Field | Value |
|---|---|
| **Instrument RED-proof** | 1 instrument: the battery (r1's GR survivor surfaced by the reviewer was added and is KILLED at r2 — the harness reports per node, so a survivor is visible as `SURVIVED`) |

### Emitted-form assertion (C-42)

| Field | Value |
|---|---|
| **Emitted-form assertion** | 2 artifacts in their emitted form: the painted gantt (compositor strips: per-cell glyph and foreground hex, 118×30 and 80×24) and the rendered frame (`render_gantt(...).plain` and its spans) |

### Evidence files — bytes at a declared home, verbatim, hash-verified (C-59)

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| inc002-red-on-inc001.txt | .dev-flow/2026-10-04-batch-02/evidence/inc002-red-on-inc001.txt | 615141371aa89784ec0b10ddd09b11d85ae287bde74b736f66c9fd322fcbdf40 |
| inc002-g2-red.txt | .dev-flow/2026-10-04-batch-02/evidence/inc002-g2-red.txt | 9e9f555c2efe0d3b6fcf5a1b5da9c621bdb386b99a6e46ec8bc031cc25e3cdc4 |
| inc002-g2-green.txt | .dev-flow/2026-10-04-batch-02/evidence/inc002-g2-green.txt | 4bb08fb62ce2faa986a1b13ec55af4d6900c9ac264d3d3c16f400500a0da7525 |
| inc002-mutations.txt | .dev-flow/2026-10-04-batch-02/evidence/inc002-mutations.txt | 12404d7a1331c50cb490eaf8a85294f06f905e770d3a9fe9cc38fec0332b75ac |
| inc002-mutations-r2.txt | .dev-flow/2026-10-04-batch-02/evidence/inc002-mutations-r2.txt | 6342aff089b3bc0174390d134406944c74a95d1d481d91b7ab00351e025f0a07 |
| mutants_inc002.json | .dev-flow/2026-10-04-batch-02/evidence/mutants_inc002.json | 4e2f2a1398082fd367455d47fc86cbd235a9c6d0ad35bbb06b86fe5e8f2ce77e |
| mutants_inc002_r2.json | .dev-flow/2026-10-04-batch-02/evidence/mutants_inc002_r2.json | 5e1efb0eddfd07adf174279124009b704f711345127f5daf43aa0de02c4adb76 |
| mk_mutants_inc002.py | .dev-flow/2026-10-04-batch-02/evidence/mk_mutants_inc002.py | 7e3591986ed18bb519734be60242a3ab6f4a246a74fe52ede9465147830feecb |
| battery.py | .dev-flow/2026-10-04-batch-02/evidence/battery.py | a84222ed67665884e0a77f30fd6d4e91e9785cf4d57030fb006fc8ccc42491cb |
| make_export.sh | .dev-flow/2026-10-04-batch-02/evidence/make_export.sh | 2de30a0c31d7a484499ad4226cf49417f619ccf616a3978dcbbcb4c32d1fe57a |
| inc002-frozen-r1.sha256 | .dev-flow/2026-10-04-batch-02/evidence/inc002-frozen-r1.sha256 | 6737e18c4a4f273bdb92cb3439d6e89b11cf8c9864c7e910d5ba0189281d1190 |
| inc002-frozen-r2.sha256 | .dev-flow/2026-10-04-batch-02/evidence/inc002-frozen-r2.sha256 | b33a802756ff79b7c016f9a230cd1dfd34d88ecb99aefd65aa41e66a38ac4e77 |
| inc002-gate-r1.txt | .dev-flow/2026-10-04-batch-02/evidence/inc002-gate-r1.txt | ca2f764fe934fc4bb7fd28f5a7efe6dfb15c7549df846d4333bd9a917f1dea36 |
| inc002-gate-r2.txt | .dev-flow/2026-10-04-batch-02/evidence/inc002-gate-r2.txt | 01506109576124b4d4e723a59366599b6b1de74938d3c353c6448ed542030aa6 |

| Field | Value |
|---|---|
| **Evidence files** | 14 artifacts at `artifact_homes.evidence`, cited with the digests of their stored bytes (home paths redacted before hashing) |

### Load-bearing emptiness (C-55)

| Field | Value |
|---|---|
| Does any claim here rest on the tree holding NO instance of some case? | yes: "groups without milestones keep their order" (`sort_by_due(o)` is the identity because `gantt_tasks` already orders by due) |
| If the result is an ABSENCE, what made the search wide enough | the reviewer's 1,550-case sweep (118 and 80 wide, heights 6–30, every selection): nav order equals draw order everywhere; the full suite's gantt files unchanged |
| Synthetic instance of the absent case | the kg milestone board (a group WITH a reached milestone): TC-609's merge arm |
| **Positive control for every probe that returned an ABSENCE** | G2 (appended, not merged) is KILLED by TC-609 |

### Reverse census — trigger family B

| Field | Value |
|---|---|
| **Reverse census** | 4 probes. B1 `grep -rln "gantt_plan\|GanttGroup\|_gantt_legend\|_gantt_bar\|legend_entries\|help_usage\|nav_model\|_notify_folded\|folded into" tests/` → `test_app.py`, `test_gantt.py`, `test_gantt_board.py`, `test_gantt_link.py`, `test_gantt_polish.py`, `test_legend.py`, `test_english.py`, `test_archive.py`, `test_vertical_fill.py`, `test_span_economy.py`, `test_colour_budget_app.py`, `test_markup_census.py`, `test_kanban_*`, `test_lanes_grid.py`, `test_swimlanes.py`, `test_team_views.py`, `test_flow_view.py` — run: 297 passed in the gantt/legend files, the full suite below; no node changed. B2 not fired. B3 not fired (no goldens). A3 judged: `GanttGroup` gains a defaulted field (no positional constructor outside `gantt_plan`; the reviewer read every `.open` reader against LLR-602.1's list) |

### Correction population

| Field | Value |
|---|---|
| **Correction population** | none — no claim corrected |

### Signed-balance test ledger

`post = base − deleted + added` → `2376 = 2347 − 0 + 29` ✓ (29 new nodes in `test_gantt_milestones.py`).

---

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a named agent with `agents/code-reviewer.md` · OK-WITH-NOTES at r2, 0 HIGH. r1 OK-WITH-NOTES: G-1 MEDIUM (tests only: its mutant R — the frame's selection test reading `open` — survived with an observable change at 118×7/80×6) folded as a TC-609 arm; G-2 LOW (product: a reached milestone on the last column drawn a day early) folded RED-first; G-3 LOW and G-4 NIT folded. r2: G-1..G-4 DISCHARGED (mutant R KILLED, the edge re-probed exact); G2-1 LOW (evidence: the r1 gate transcript was cited before its result was on disk) — corrected in §4 |

---

## 5 · Risks

- Every reached milestone of a group with open work is a row: a long-lived project accumulates ash rows (PV-602; a close capture with three reached milestones, ux UX-10).
- `◆` now carries three meanings on the gantt (project due on the span, a plain one-day task, a milestone); the label's `◆` prefix and the chip tell a milestone (PV-609).
- A reached milestone due on the last column drops its `✓` (G-2); the chip still says `✓ done`.

## 6 · Pending items / spec deviations

- none — no requirement amended in this increment.

## 7 · Suggested next task

Increment 003 — the kanban (US-603): `kanban_work`, `band_milestones`, the band-rule layout, `_select_first`.

---

## Increment gate checklist

| # | Item | Owed in | ✓/⚠/✗ | Evidence |
|---|---|---|---|---|
| 1 | ≤4 source files | all | ✓ | 2 / 4 |
| 2 | Tests written in this same increment | all | ✓ | `tests/test_gantt_milestones.py` (29) |
| 3 | Layer 0 where the criterion applies | `core` · `full` | ✓ | `gantt_milestone_cells` (edges, placement), `gantt_milestone_chip` (5 paths), `milestone_tone`: TC-610 |
| 4 | **RED counterfactual** | `core` · `full` | ✓ | §4 |
| 5 | **Reverse census** | `core` · `full` | ✓ | §4 |
| 6 | `code-reviewer` passed | `core` · `full` | ✓ | §4b |
| 7 | No file from another lane touched | all | ✓ | one lane |
| 8 | Frozen interfaces untouched | all | ✓ | none declared |
| 9 | Coverage claims verified on disk | all | ✓ | `pytest --collect-only tests/test_gantt_milestones.py` → 29 |
| 10 | Load-bearing emptiness declared | all | ✓ | §4 |
| 11 | **Mutation verdicts** | all | ✓ | 16/16 |
| 12 | **Instrument RED-proof** | all | ✓ | §4 |
| 13 | **Correction population** | all | ✓ | none |
| 14 | **Emitted-form assertion** | all | ✓ | §4 |
| 15 | **Independent review** names somebody | all | ✓ | §4b |
| 16 | **Evidence files** | all | ✓ | §4 |
