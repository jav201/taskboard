# Increment 001 — HLR-601 (LLR-601.1, LLR-601.2, LLR-601.3) · a task can be a milestone

> **Where this lives:** the repo, next to the diff — `.dev-flow/2026-10-04-batch-02/03-increments/increment-001.md`.
> Template `templates/increment-template.md` (rev100); notice convention `⚠` notice · `✗` block · `✓` with evidence.

| Field | Value |
|---|---|
| Batch | `2026-10-04-batch-02` |
| Increment | `001` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | HLR-601; LLR-601.1, LLR-601.2, LLR-601.3 (amended LED .5, .6) |
| Acceptance | AT-601 · white-box TC-601..TC-608 · unit TC-601/602/603 tables |
| Agent | `software-dev` (this runtime) |
| Date | `2026-10-04` |

---

## 1 · What changed

**A task can now be a milestone: one date, its due.** `M` on the selected task (lanes, agenda,
gantt, kanban, focus) makes it one — the start becomes the due, or the due the start when only a
start exists — or a task again; a task with no date is refused with "a milestone needs a date —
give it a due date first" and nothing is written. The toast says the date, the start it replaced
and where the milestone shows ("on the ‹project› band" / "shown on the gantt"); `u` undoes it as one
step. The editor (`e`) has a `milestone` box beside priority; the box is applied after every other
field, so a new due in the same save is the milestone's date, a replaced start is said when the task
becomes a milestone or the user changed the start, and a box ticked with no date leaves a task and
says so. `+`/`-` move a milestone whole. The details view's phase row ends ` · ◆ milestone`. The flag
is saved as `"milestone"` (read only as the boolean true), pushed and pulled by team sync, and kept
by archive, search and links. The editor's one-row chip threshold is 137 columns (measured; was 122).

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/models.py` | source | LLR-601.1 | `Task.milestone` (after `phase_changed`), `from_dict` `is True`, `_TASK_KEYS`; `MILESTONE_NEEDS_DATE`, `set_milestone`; `bump_due` moves a milestone whole |
| `taskboard/app.py` | source | LLR-601.2, LLR-601.3 | `action_milestone_toggle`, `_milestone_where`, `_apply_editor_milestone`; `_UNDO_FIELDS` + `start_date`, `milestone`; the add and edit handlers; `milestone_toggle` a board action; `_md` |
| `taskboard/modals.py` | source | LLR-601.3 | `#f-milestone` box and payload key; `TaskDetails` phase row; `TASK_CHIPS_ONE_ROW` 137 |
| `taskboard/keymap.py` | source | LLR-601.2 | `M` → `milestone_toggle`, five views, task group |
| `README.md` | doc | | the `M` key row; a Milestones section |
| `tests/test_milestones.py` | test | HLR-601, LLR-601.1, LLR-601.2, LLR-601.3 | NEW: TC-601..TC-608, AT-601 (41 nodes) |
| `tests/kg_board.py` | fixture | HLR-601, HLR-602, HLR-603, HLR-605 | `one_day`, `milestones`, `ONE_DAY`, `ADDED_MILESTONES`, `MILESTONE_IDS` (the round-5 boards, §5) |
| `tests/test_edit_window.py` | test | LLR-601.3 | `CONTRACT_IDS`, `TAB_ORDER`, `FOCUS_MARKED` gain `f-milestone` (canon LLR-001.3: 18 ids) |
| `tests/test_app.py` | test | LLR-601.2 | the undo snapshot's field set gains `start_date`, `milestone` |
| `tests/test_colour_budget_app.py` | test | LLR-601.2 | the pinned gantt 118 more-layer bar, read from `key_bar_plain`: `M` added, the word "More" shed |

| Count | Value |
|---|---|
| **SOURCE files** | **4 / 4** |
| Test files | 5 (uncapped; one is a fixture module) |
| Doc files | 1 (outside the count) |

- ⚠ **At exactly 4 source files:** the key (`keymap.py`), its action (`app.py`), the flag and its date rule (`models.py`) and the editor box (`modals.py`) are one user-visible capability; any one left out ships a flag nobody can set or a key with nothing to set (PLAN.md, P1).

## 3 · How to test

```bash
python -m pytest -q -p no:cacheprovider tests/test_milestones.py
python -m pytest -q -p no:cacheprovider tests/test_edit_window.py tests/test_keymap.py tests/test_readme.py
python -m pytest -q -p no:cacheprovider          # the gate
```

## 4 · Test results

| Layer | Owed in | Nodes | Result |
|---|---|---|---|
| **0 · unit** | `core` · `full` | TC-601 (7 + 1), TC-602 (7), TC-603 | passed |
| **A · white-box** `TC-NNN` ↔ LLR | `core` · `full` | TC-604 (12), TC-605 (8), TC-606, TC-607, TC-608 | passed |
| **B · black-box** `AT-NNN` ↔ story | `core` · `full` | AT-601 | passed |

Gate run on frozen r3: `python -m pytest -q -p no:cacheprovider` → **2346 passed, 1 failed** in 452.81 s — the one failure is `test_win_clipboard_roundtrip`, the known environmental clipboard flake (its own SETUP, `Set-Clipboard` refused; G-011) (`.dev-flow/2026-10-04-batch-02/evidence/inc001-gate-r3.txt`). r2 (superseded by the F2-1 fold): 2345 passed, 1 failed (the same flake) (`inc001-gate-r2.txt`). The larger failure counts in the cited evidence come from the deliberately failing transcripts: the mutation batteries (one failure set per KILLED mutant, e.g. `9 failed` in `inc001-mutations-r2.txt`) and the RED captures — never from a gate run.

### RED counterfactual — executed, not predicted

| Field | Value |
|---|---|
| **RED counterfactual** | the new tests on the base product (`git archive 4b2c13a` + this increment's tests): collection `ImportError` (`MILESTONE_NEEDS_DATE` absent) — `evidence/inc001-red-on-base.txt`; with the two new imports stubbed, AT-601 fails on its first read after `M` (`KeyError: 'milestone'`: `M` changed nothing) — `evidence/inc001-at601-red-on-base.txt` (code review F-5); the folds RED-first: F-4 `inc001-f4-red.txt`, F2-1 `inc001-f2-1-red.txt`. Base product bytes untouched (an export, not the working tree) |

| Field | Value |
|---|---|
| **Mutation verdicts** | **19 of 19 KILLED** across r3 (`evidence/inc001-mutations-r3.txt`, spec `mutants_inc001_r3.json`) and r3b (`inc001-mutations-r3b.txt`, `mutants_inc001_r3b.json`), each in a scratch export, per resolved node, every restore hash OK: M1 `from_dict` reads `bool()` · M2 the start wins over the due · M3 bump moves only the due · M4 an undated task flagged anyway · M5 `from_dict` drops the field · M6 snapshot after the change · M7 `start_date` not restored · M8 a refusal still pushes and saves · M9 "on the band" everywhere · M10 the edit handler ignores the box · M11 the replaced start not said · M12 the payload drops the box · M13 no details mark · M14 `M` scoped everywhere · M15 the threshold not re-measured · MB ‹where› ignores open · MC a refused box keeps an existing flag · MD the start toast for an untouched start · ME the start toast ignores a task becoming a milestone. r1 (15/15, `inc001-mutations.txt`) and r2 (18/18, `inc001-mutations-r2.txt`) are the earlier revisions' batteries |

### Instrument RED-proof

| Field | Value |
|---|---|
| **Instrument RED-proof** | 2 instruments: the battery (its BAD verdict fired for a moved anchor — r3's M10/M11 — before re-anchoring, `inc001-mutations-r3.txt`); the chip-threshold probe `p3_chip_threshold.py` reported clipping at every width 120..136 before reporting the fit at 137 (`inc001-chip-threshold.txt`) |

### Emitted-form assertion (C-42)

| Field | Value |
|---|---|
| **Emitted-form assertion** | 3 artifacts in their emitted form: the saved board file (re-read JSON: `milestone`, `start_date`, `due_date`), the pushed `board.jav.json` (re-read JSON), the rendered toasts (`Toast.render()` text) |

### Evidence files — bytes at a declared home, verbatim, hash-verified (C-59)

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| inc001-red-on-base.txt | .dev-flow/2026-10-04-batch-02/evidence/inc001-red-on-base.txt | 60bc23366f6ff0988d32d033073b49a0086ac1ea92393338b21ed04a48395058 |
| inc001-at601-red-on-base.txt | .dev-flow/2026-10-04-batch-02/evidence/inc001-at601-red-on-base.txt | a5504799a57d52a63c02e0df0c3f938d483a25f188f279b1a5227ed942177d44 |
| inc001-f4-red.txt | .dev-flow/2026-10-04-batch-02/evidence/inc001-f4-red.txt | 7c32038dbe3d0baa386a64b37ca97b7d1439aba0f1cf57bc073f02e8a6b59a93 |
| inc001-f4-green.txt | .dev-flow/2026-10-04-batch-02/evidence/inc001-f4-green.txt | 7810dd4a09fa9fafdc4b3f6c6bdf9faf0871ef4842f7265c6e06f228d4d02936 |
| inc001-f2-1-red.txt | .dev-flow/2026-10-04-batch-02/evidence/inc001-f2-1-red.txt | 1547fddf41e972bb2cba0f7571a4e300de02287750e1d379f01e1720b5ec740f |
| inc001-f2-1-green.txt | .dev-flow/2026-10-04-batch-02/evidence/inc001-f2-1-green.txt | bbc5e3382faa5ab7fec3905be1ff2948f448e28cb0d4a4496ad37f13f4a063fa |
| inc001-mutations.txt | .dev-flow/2026-10-04-batch-02/evidence/inc001-mutations.txt | ae4b99c32a3733f54771cb4031c178b62fe293a28a8c0489e20b658fccd5f871 |
| inc001-mutations-r2.txt | .dev-flow/2026-10-04-batch-02/evidence/inc001-mutations-r2.txt | c4b1cc7ffdd8713a62b6a6cfd85aeec0876ed8d5a9c30090198195f32e69c405 |
| inc001-mutations-r3.txt | .dev-flow/2026-10-04-batch-02/evidence/inc001-mutations-r3.txt | b62c49458d19ca7ba39725ed65295f75c9f504f84fd86184c9a26c877bcc0b0a |
| inc001-mutations-r3b.txt | .dev-flow/2026-10-04-batch-02/evidence/inc001-mutations-r3b.txt | 8f6061dbc8dc1f3af3985ffd187a887ab7cb1915fc697f89bca5951d34bf5bd9 |
| mutants_inc001.json | .dev-flow/2026-10-04-batch-02/evidence/mutants_inc001.json | 6c8b2fddf922a6ce7418a295df6b483833e6d826825dfd05c6e3d81383ed2739 |
| mutants_inc001_r2.json | .dev-flow/2026-10-04-batch-02/evidence/mutants_inc001_r2.json | 35334bb133d8bcc3025eefc36ac1e0a5909119c1ecd67d9bb27d25aa798373c7 |
| mutants_inc001_r3.json | .dev-flow/2026-10-04-batch-02/evidence/mutants_inc001_r3.json | 63a9291006bcbe8b764bfba2e5f76717ac9f8affa350eb15badca49d71bc2621 |
| mutants_inc001_r3b.json | .dev-flow/2026-10-04-batch-02/evidence/mutants_inc001_r3b.json | 419f87c3ffc86289ca09cd8c5e1d9718f764acb39107841763aaeffb423c4de2 |
| battery.py | .dev-flow/2026-10-04-batch-02/evidence/battery.py | a84222ed67665884e0a77f30fd6d4e91e9785cf4d57030fb006fc8ccc42491cb |
| make_export.sh | .dev-flow/2026-10-04-batch-02/evidence/make_export.sh | 2de30a0c31d7a484499ad4226cf49417f619ccf616a3978dcbbcb4c32d1fe57a |
| p3_chip_threshold.py | .dev-flow/2026-10-04-batch-02/evidence/p3_chip_threshold.py | 7a1a67c4d94ced1a2dd663f3509640d3d23215039fc36b628484a67a2fe81b2f |
| inc001-chip-threshold.txt | .dev-flow/2026-10-04-batch-02/evidence/inc001-chip-threshold.txt | a9d7905a4831201cc340bd3ac9593b9dd675b99d3c9e09f27fb0241d91ac8a57 |
| inc001-frozen-r1.sha256 | .dev-flow/2026-10-04-batch-02/evidence/inc001-frozen-r1.sha256 | 5ecd0edc55597651bd0ae1e6fb2d6b31ee12fdfc4ffae3bc039d19d39bf46b12 |
| inc001-frozen-r2.sha256 | .dev-flow/2026-10-04-batch-02/evidence/inc001-frozen-r2.sha256 | b6030e340feabf47d31d9f574354f24a752fd3fc7704638db61e58f157bde889 |
| inc001-frozen-r3.sha256 | .dev-flow/2026-10-04-batch-02/evidence/inc001-frozen-r3.sha256 | e74806b4b7f18b8e6fffce7bcca888b5da8d2738b487bb583b25f474fe2fcd6d |
| inc001-gate-r2.txt | .dev-flow/2026-10-04-batch-02/evidence/inc001-gate-r2.txt | de82fe01022e4c049b850aba059823a028349f36868ab0f7c911eb6800793c3b |
| inc001-gate-r3.txt | .dev-flow/2026-10-04-batch-02/evidence/inc001-gate-r3.txt | 6327f1a9460c7673139f630b18d6079c4afe696fb039c8a09e2ad1c3907a6732 |

| Field | Value |
|---|---|
| **Evidence files** | 23 artifacts at `artifact_homes.evidence`, cited with the digests of their stored bytes (home paths redacted before hashing) |

### Load-bearing emptiness (C-55)

| Field | Value |
|---|---|
| Does any claim here rest on the tree holding NO instance of some case? | yes: "no positional `Task(...)` call reaches the new field" (the reviewer's AST scan: 0 calls with ≥ 5 positional arguments) |
| If the result is an ABSENCE, what made the search wide enough | the reviewer's AST walk over `tests/`, `taskboard/` and the `.dev-flow` scripts |
| Synthetic instance of the absent case | the field sits before `extra`/`id`, after every positional field the seed uses (`Task("…", None, "Doing", "normal", …)`) |
| **Positive control for every probe that returned an ABSENCE** | the same scan finds the 4-positional seed calls in `models.seed_data` |

### Reverse census — trigger family B

| Field | Value |
|---|---|
| **Reverse census** | 5 probes. B1 `grep -rl "_UNDO_FIELDS\|TASK_CHIPS_ONE_ROW\|from_dict\|TaskModal\|TaskDetails\|KEYMAP\|key_bar_plain" tests/` → `test_app.py` (the undo snapshot field set — updated), `test_edit_window.py` (chip sweep, tab order, ids — updated), `test_colour_budget_app.py` (the pinned bar — updated), `test_keymap.py`/`test_readme.py` (green with the README row), `test_sync_fields.py`, `test_rescue.py`, `test_palette_ration.py`, `test_details_*`, `test_markup_sites.py` (green); the full-suite pre-check found exactly the two pins. B2 not fired: no file moved. B3 not fired: `ls tests/goldens` → none. B4: the saved board and the pushed team file are consumed by the next load and a teammate's pull — AT-601 and TC-607 re-read them. A3 judged: `Task` gains a field every consumer reads through `from_dict`/`asdict` (the reviewer: `_to_dict` consumers are `_serialized` and `team_sync.push`) |

### Correction population

| Field | Value |
|---|---|
| **Correction population** | 1 correction: "the editor has 17 widget ids" (canon LLR-001.3) → 18 — population `grep -rn "f-pinned" tests/`: `CONTRACT_IDS`, `TAB_ORDER`, `FOCUS_MARKED` in `test_edit_window.py` — all three edited; the canon row's status is amended at close |

### Signed-balance test ledger

`post = base − deleted + added` → `2347 = 2306 − 0 + 41` ✓ (41 new nodes in `test_milestones.py`; no node removed; the changed nodes are rewritten in place).

---

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a named agent with `agents/code-reviewer.md` · OK-WITH-NOTES at r3, 0 HIGH open. r1 OK-WITH-NOTES: F-1, F-2 MEDIUM (test gaps; its mutants B, C survived) and F-3 LOW folded as tests; F-4 LOW (product: the start toast on an untouched start) folded RED-first with LED .5; F-5 LOW folded (a behavioural RED of AT-601 on base); F-7 NIT folded; F-6 NIT accepted, not folded; F-8 no action. r2 BLOCK-UNTIL F2-1 (HIGH, product, the increment under construction: the F-4 fold silenced the toast when a task becomes a milestone, so an editor save dropped its start unsaid) — fixed without stopping under the standing authorization's second exception, RED-first (`inc001-f2-1-red.txt` → `inc001-f2-1-green.txt`), LED .6, re-frozen r3 and re-reviewed: DISCHARGED (the reviewer re-read the diff, re-ran its ta4 probe and its mutant E). The P2 security carry (AT-601's team folder under `tmp_path`) verified by the reviewer |

---

## 5 · Risks

- The gantt more-layer bar at 118 columns now sheds its word "More" (the `;` key stays) — the bar's own contract (labels go before keys).
- A milestone saved by an older app (flag kept in `extra`) may carry start ≠ due; every view reads its due (D-613).
- `M` in the kanban makes the card leave the columns only from increment 003 on; until then it stays a card.

## 6 · Pending items / spec deviations

- LED .5, .6: LLR-601.3's start-toast wording amended twice in this increment (code review F-4, F2-1).
- Code review F-6 (NIT): a third copy of the `Mon D` formatter (`_md` in `models.py`, `views.py`, now `app.py`) — not folded; BACKLOG at close.
- Canon LLR-001.3 ("17 widget ids") amended to 18 at close.

## 7 · Suggested next task

Increment 002 — the gantt (US-602): `GanttGroup.rows`, the milestone row, ruler marks, legend, `_notify_folded`.

---

## Increment gate checklist

| # | Item | Owed in | ✓/⚠/✗ | Evidence |
|---|---|---|---|---|
| 1 | ≤4 source files | all | ⚠ | 4 / 4 — the reason in §2 |
| 2 | Tests written in this same increment | all | ✓ | `tests/test_milestones.py` (41) |
| 3 | Layer 0 where the criterion applies | `core` · `full` | ✓ | `set_milestone` (3 paths): TC-602's 7-row table; `from_dict`: TC-601 |
| 4 | **RED counterfactual** | `core` · `full` | ✓ | §4 |
| 5 | **Reverse census** | `core` · `full` | ✓ | §4 |
| 6 | `code-reviewer` passed | `core` · `full` | ✓ | §4b |
| 7 | No file from another lane touched | all | ✓ | one lane |
| 8 | Frozen interfaces untouched | all | ✓ | none declared |
| 9 | Coverage claims verified on disk | all | ✓ | `pytest --collect-only tests/test_milestones.py` → 41 nodes |
| 10 | Load-bearing emptiness declared | all | ✓ | §4 |
| 11 | **Mutation verdicts** | all | ✓ | 19/19 KILLED |
| 12 | **Instrument RED-proof** | all | ✓ | §4 |
| 13 | **Correction population** | all | ✓ | §4 |
| 14 | **Emitted-form assertion** | all | ✓ | §4 |
| 15 | **Independent review** names somebody | all | ✓ | §4b |
| 16 | **Evidence files** | all | ✓ | §4 |
