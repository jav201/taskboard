# Increment 003 — LLR-604.3 · LLR-604.5 · The editor's date save and the per-project rule

| Field | Value |
|---|---|
| Batch | `2026-10-06-batch-01` |
| Increment | `003` |
| Lane (if the batch forked) | `single lane` |
| Requirement(s) | `LLR-604.3` · `LLR-604.5` |
| Acceptance | black-box `AT-609` · `AT-610` · `AT-611` · regression `TC-632` · `TC-633` · `TC-634` · `TC-635` |
| Agent | `software-dev` — implemented by **DeepSeek V4 Pro via OpenCode** under the coordinator's brief (`evidence/inc003-brief-deepseek.md`); verified, reviewed and folded by the coordinator |
| Date | `2026-10-06` |

---

## 1 · What changed

The editor's date save routes through the cascade (LLR-604.3): a field that changes by a clean
delta moves the chain through `_apply_cascade` (one undo entry, atomic when >1 task, the toast
only when the cascade moved others or `flag` added overlaps — D-629's silence clause via the
seat's new `say_solo` gate); a cleared/junk/undated field keeps what was typed with no delta.
The project editor gains the `Linked dates` select (LLR-604.5): stay / push / together on
screen, stored as `extra["date_links"]` in the engine's strings, read leniently (absent or junk
shows and behaves as the default `push_delta`, never repaired). The select sits OUTSIDE the
pinned `.modal-grid` (test_details_grid TC-411 pins the grid's 10 children) — a declared
deviation, judged right, flagged for the P4 visual verdict alongside D-627.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/app.py` | source | LLR-604.3 · LLR-604.5 | `_on_task_edited` routes date deltas through `_apply_cascade(say_solo=False)` with the restore dance + the TC-633 undo patch; the milestone gate uses the post-canonicalization due delta (TC-634); `_on_project_added` stores `date_links` when chosen; `_apply_cascade` gained `say_solo`; the toast's lead/sort/clause hardening (DS-1/2/3, L, N) |
| `taskboard/modals.py` | source | LLR-604.5 | `DATE_LINKS_LABELS/_VALUES/_DEFAULT`; the `#f-date-links` Select; `_save` emits `date_links`; the `_on_edited` carve-out to `extra` |
| `tests/test_cascade_app.py` | test | AT-609..611 · TC-631..635 · LLR-604.3 · LLR-604.5 | DeepSeek: AT-609, AT-610 · coordinator: AT-611, TC-632, TC-633, TC-634, TC-635, TC-631's DS-3 arm |

| Count | Value |
|---|---|
| **SOURCE files** | **2 / 4** (app · modals) |
| Test files | 1 (uncapped) |
| Doc files | 0 |

## 3 · How to test

```powershell
$env:PYTHONIOENCODING = "utf-8"
python -m pytest tests/test_cascade_app.py -q     # 10 passed
python -m pytest tests -q                         # the increment's gate
```

## 4 · Test results

| Layer | Owed in | Nodes | Result |
|---|---|---|---|
| **0 · unit** | `core` | — | increments 001/002's layers, unchanged |
| **A · white-box** `TC-NNN` ↔ LLR | `core` | TC-631..635 | 5 nodes |
| **B · black-box** `AT-NNN` ↔ story | `core` | AT-609 · AT-610 · AT-611 | 3 nodes |

### RED counterfactual — executed, not predicted

| Field | Value |
|---|---|
| Mutation applied | the increment's wiring absent — DeepSeek captured AT-609's RED (`tm3` unmoved) and AT-610's RED (`NoMatches: #f-date-links`) before implementing (`evidence/inc003-deepseek-run.log`); the coordinator captured K's RED (`evidence/inc003-k-red.txt` — the typed start discarded, a due-less non-canonical milestone); TC-633's arm goes RED if the undo patch loop is removed (battery P4) |
| Instrument | project code: the suite · restore checked by hash |
| Where it ran | **this tree** — no other session |
| Transcript | the DeepSeek run log · `inc003-k-red.txt` · `inc003-folds-red.txt` |
| Restore proven by | `evidence/inc003-frozen.sha256` |
| Bytecode cache | `PYTHONDONTWRITEBYTECODE=1` |
| Arms resolved at baseline | 10 — asserted by the battery's baseline control |
| Verdict granularity | per resolved node id |
| Arms that stayed GREEN | none |

| Field | Value |
|---|---|
| **RED counterfactual** | the absent wiring (AT-609/610 RED) + K's executed RED + the battery's per-mutant REDs · restore digest in `inc003-frozen.sha256` |

| Field | Value |
|---|---|
| **Mutation verdicts** | 9 mutants, 9 KILLED, 0 SURVIVED (P1 editor bypasses the cascade · P2 the silence gate forced off · P3 the milestone zero-delta cascade returns · P4 the undo patch removed · P5 junk repaired · P6 the carve-out setattr'd · P7 the label stored instead of the engine string · P8 the conflicts arm dropped · P9 the empty-title guard removed) · 1 BAD by design (P10) · `inc003-mutations-r3.txt` |

### Instrument RED-proof — every instrument shown able to report FAILURE first

| Instrument | Known-bad input fed to it | The FAILURE it reported |
|---|---|---|
| the suite | revision 1's J violation (editor toasted every date save) | the reviewer's BLOCK-UNTIL, and the suite itself went green only after the gate landed |
| the mutation harness's baseline + anchors | the first battery run's mid-mutant crash (a decode bug) | the harness aborted leaving a mutant applied — detected as a non-green baseline on the next run, and the remnant was restored by hand (recorded in the coordinator's notes) |

| Field | Value |
|---|---|
| **Instrument RED-proof** | 2 instruments, each shown able to report FAILURE |

### Emitted-form assertion — assert the bytes the producer EMITS (C-42)

| Artifact emitted | The assertion, run against the EMITTED form | What it returned |
|---|---|---|
| the toast's rendered text | AT-607/608 (inc-002) plus AT-609/610's `pushed`/`moved`/`flagged Revenue +2d` against `str(t.render())` | all present (suite green) |

| Field | Value |
|---|---|
| **Emitted-form assertion** | carried from increment 002; this increment adds no new emitted surface beyond the same toast channel |

### Evidence files — bytes at a declared home, verbatim, hash-verified (C-59)

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| the external agent's brief | `evidence/inc003-brief-deepseek.md` | (cited by content) |
| the external agent's run + REDs | `evidence/inc003-deepseek-run.log` | (cited by content) |
| K's RED | `evidence/inc003-k-red.txt` | (cited by content) |
| the folds' RED | `evidence/inc003-folds-red.txt` | (cited by content) |
| the targeted run (§3) | `evidence/inc003-targeted.txt` | `d61c5cb1a6a2ed2dbfc57c9a17fe35459fef99eec8739b37c5901b7191fb13c4` |
| mutation battery r3 | `evidence/inc003-mutations-r3.txt` | (cited by content) |
| the second review (DeepSeek Flash) | `evidence/inc001-002-deepseek-review.md` | (cited by content) |
| frozen tree | `evidence/inc003-frozen.sha256` | the file's own lines |

| Field | Value |
|---|---|
| **Evidence files** | 7 artifacts at the declared home |

### Load-bearing emptiness — what is this resting on that is only true today? (C-55)

| Field | Value |
|---|---|
| Does any claim here rest on the tree holding NO instance of some case? | no |

### Reverse census — trigger family B

| Probe | Command | Result |
|---|---|---|
| B1 | `grep -rl "_on_task_edited\|_on_project_added\|ProjectModal" tests/` | test_edit_window, test_links, test_app, test_details_grid — all pass (the `data.pop("date_links", old)` default keeps the direct `_on_task_edited(task, {...})` call in test_links working) |
| B2 | `git status` | no file moved |
| B3 | no `tests/goldens` directory | — |
| B4 | the select's value is consumed by `ProjectPicker._on_edited` and the engine's `resolve_mode`; the payload key is read by no other consumer | — |
| A3 | `grep -rn "date_links" taskboard/` | models (the read seat), modals (the write seat), app (the routing) — one key, three seats, no drift |

| Field | Value |
|---|---|
| **Reverse census** | 5 probes; the B1 hits re-validated by the full suite |

### Correction population — enumerated BEFORE the first site was edited

| Correction | Population | Enumeration method | Count | Sites edited | Sites left |
|---|---|---|---|---|---|
| the editor's toast gate (J) | every caller of `_apply_cascade` | `grep -n "_apply_cascade(" taskboard/app.py` | 4 (bump, m, editor, reviewer-confirmed) | 1 (the seat) + 1 (the editor call) | bump/m keep the default |

| Field | Value |
|---|---|
| **Correction population** | 1 correction, enumerated before its edit |

#### Supersession-completeness inspection (V-3)

| Superseded marker | grep result | All surviving refs negative? | Evidence (file:line) |
|-------------------|-------------|------------------------------|----------------------|
| the unconditional editor toast | `grep -n "say_solo=False" taskboard/app.py` | yes — exactly one, the editor's call | `app.py` |

### Signed-balance test ledger

`post = base − deleted + added` → `2509 = 2504 − 0 + 5` ✓ reconciles (the increment's own gate, `inc003-gate.txt`)

---

## 4b · Independent review — the lens the author cannot be

| Field | Value |
|---|---|
| **Independent review** | TWO lenses. (1) `code-reviewer` (the flow's role, spawned generic) — r1 BLOCK-UNTIL J+K · fixed RED-first · r2 verified K/L/M/N, narrowed J to its milestone sub-case · fixed (one keyword) + pinned by TC-635 · **PASS-WITH-NOTES-equivalent ("OK to advance" on J's residual fix, all checks executed)**. (2) **DeepSeek V4.1 Flash** (a second, model-independent review of the whole 001+002 surface, `evidence/inc001-002-deepseek-review.md`) — DS-1..DS-7, every one executed; the coordinator folded DS-1/2/3/6/7 and scheduled DS-4 (AT-611) and DS-5 in this increment |

---

## 5 · Risks

- The select's placement outside the pinned grid is a visual-design decision the operator has
  not seen — carried to the P4 visual verdict with D-627.
- The toast's start-arm (DS-2) is unreachable through every shipped surface after J's gate;
  it stays as defense-in-depth (one rung of the ladder).
- An explicit project-editor save on a junk-valued project necessarily shows the default and
  a save writes the chosen value — "no silent repair" is pinned for LOAD and silent saves
  (AT-610); an explicit user choice repairing junk is the select's nature, not a repair.

## 6 · Pending items / spec deviations

- P4 (the four lenses re-read the close tree; the captures: the toast at 118/80, the m
  cycle, the project editor's new row — the operator's visual verdict PV-612+).
- DS-5 (LOW, the tested `restore` vs the app's hand-rolled loops) rides to BACKLOG at close.

## 7 · Suggested next task

P4 — validation: the close gate (full suite on the frozen tree), the captures, the four
lenses over the delta, and the operator's visual verdict sheet.

## Increment gate checklist

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | ≤4 source files | ✓ | 2/4 (§2) |
| 2 | Tests written in this same increment | ✓ | test_cascade_app.py in the same pass |
| 3 | Layer 0 written where the criterion applies | ✓ | prior increments' layers |
| 4 | **RED counterfactual** declared | ✓ | §4 (three executed REDs) |
| 5 | **Reverse census** declared | ✓ | §4's five probes |
| 6 | `code-reviewer` passed | ✓ | two lenses; the flow's role + the external second review (§4b) |
| 7 | No file from another lane touched | ✓ | single lane |
| 8 | Frozen interfaces untouched | ✓ | `_on_task_edited`'s contract preserved (test_links' direct call still works) |
| 9 | Coverage claims verified **on disk** | ✓ | the gate transcript |
| 10 | Load-bearing emptiness declared | ✓ | none |
| 11 | **Mutation verdicts** declared | ✓ | 9 KILLED · 1 BAD · 0 SURVIVED |
| 12 | **Instrument RED-proof** declared | ✓ | 2 instruments |
| 13 | **Correction population** declared | ✓ | 1 correction |
| 14 | **Emitted-form assertion** declared | ✓ | carried from 002 |
| 15 | **Independent review** names somebody | ✓ | two named reviewers (§4b) |
| 16 | **Evidence files** declared | ✓ | 7 artifacts |
