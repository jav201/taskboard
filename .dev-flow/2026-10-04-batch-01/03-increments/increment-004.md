# Increment 004 — HLR-502 (LLR-502.3) · the gantt link mode (D-A)

> Review packet (flow `templates/increment-template.md`; reserved field names kept literal). Mode
> `core`, language `en`. Revision 3 (frozen r3): code review round 1 BLOCK-UNTIL F1 (HIGH, product,
> in the increment under construction — fixed without stopping under the amended standing
> authorization "Sí, solo en el incremento en curso", RED-first, re-reviewed); round 2 OK to
> advance; r3 strengthens one test after the r2 battery (test-only).

| Field | Value |
|---|---|
| Batch | `2026-10-04-batch-01` |
| Increment | `004` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | HLR-502, LLR-502.3; LLR-502.1 (the one-phase create guard, R2-2); amendment A-7; D-527 |
| Acceptance | AT-503 · white-box TC-511, TC-512 · the R2-2 arm |
| Agent | `software-dev` |
| Date | `2026-10-04` |

---

## 1 · What changed

**In the gantt, `L` keeps the chart on screen and draws the proposed link on it.** `GanttLinkMode`
paints the gantt with the candidate as the selection (its group unfolds) and the waiter's group kept
open, the header "◆ GANTT · LINK" with "N candidates · ⟲K would loop", `⟲` in the gutter of each row
that would loop, and on the field only: a connector (`╮ │ ╯`, bright tone, background cells only)
from the cell after the candidate's due to the waiter's row, and the overlap days as `═` (over tone)
on the waiter's row — none for a waiter with no start. Three status rows (A-7): "LINK ‹waiter› waits
on… ‹candidate›" with the filter and "✓ linked"; the candidate's timing hint (the picker's one
measure); the keys "↑↓ choose · type to filter · ↵ link · esc cancel" ("↵ unlink" for a linked one),
then the loop legend "⟲ loop: this → ‹path› → this" in the room left. ↑/↓ walk the open tasks in the
chart's order and skip loops and filter misses; printable keys filter, `backspace` edits; ↵ on no
match does nothing; ↵ links or unlinks through the app's path (one undo step, the same toast); esc
cancels. Every board text is a Text piece; the frame repaint is the census's one EXEMPT entry (the
views seat, D-405). Outside the gantt `L` still opens the picker.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/views.py` | source | LLR-502.3 | `LINK_BACKGROUND`, `_cell_index`, `gantt_link_order`, `gantt_link_frame`, `gantt_link_overlay` (appended block, CRLF like the file) |
| `taskboard/modals.py` | source | LLR-502.3 | `GanttLinkMode`; the `.views` import |
| `taskboard/app.py` | source | LLR-502.3 | `action_link` routes the gantt to `GanttLinkMode`; import |
| `tests/test_gantt_link.py` | test | HLR-502, LLR-502.3, LLR-502.1 | NEW: TC-511 ×6, TC-512 ×4, AT-503 ×2, R2-2 ×1 |
| `tests/test_markup_census.py` | test | LLR-502.3 | the EXEMPT entry for the frame repaint |

| Count | Value |
|---|---|
| **SOURCE files** | **3 / 4** |
| Test files | 2 (uncapped) |
| Doc files | 0 (records: A-7, D-527, LED .18) |

## 3 · How to test

```bash
python -m pytest -q -p no:cacheprovider tests/test_gantt_link.py tests/test_markup_census.py
python -m pytest -q -p no:cacheprovider          # the gate
```

Manual: `taskboard --board <a copy>` → `3` → select a task with dates → `L`; type a few letters,
↑/↓, ↵; `u` undoes.

## 4 · Test results

| Layer | Owed in | Nodes | Result |
|---|---|---|---|
| **0 · unit** | `core` · `full` | TC-511 ×6 (the frame and overlay functions directly) | passed |
| **A · white-box** `TC-NNN` ↔ LLR | `core` · `full` | TC-511 ×6, TC-512 ×4, R2-2 | 11 passed |
| **B · black-box** `AT-NNN` ↔ story | `core` · `full` | AT-503 ×2 | 2 passed |

Gate run on frozen r3: `python -m pytest -q -p no:cacheprovider` → **2294 passed, 1 failed in 576.52 s** (`evidence/inc004-gate-r3.txt`); the one failure is `test_win_clipboard_roundtrip`, whose SETUP message names the environment — the known flake (G-011), not this code.

### RED counterfactual — executed, not predicted

| Field | Value |
|---|---|
| **RED counterfactual** | increment 004's tests on increment 003's frozen r2 product (`app.py`, `modals.py`, `models.py`, `keymap.py` hashes = `inc003-frozen-r2`; `views.py` = `inc002-frozen-r2`, unchanged in 003): collection fails on `GanttLinkMode`; with an empty stand-in class every node of TC-511, TC-512 and AT-503 FAILED and the census's TC-402 FAILED (the exemption names no live site); the R2-2 arm PASSED — it covers increment 003's existing guard, and its RED is mutant Q16 (`evidence/inc004-red-on-inc003.txt`). F1's arms FAILED on r1 (`evidence/inc004-f1-red.txt`) |

| Field | Value |
|---|---|
| **Mutation verdicts** | **25 of 25 KILLED.** r1 21/21 (`evidence/inc004-mutations.txt`, spec `mutants_inc004.json`); r2 22/25 (`inc004-mutations-r2.txt`, spec `mutants_inc004_r2.json`): Q22 row guard removed, Q22b clip by `len()`, Q23 filter unclipped SURVIVED — each F1 guard alone kept the keys painted; the test was strengthened (r3) and all three KILLED (`inc004-mutations-r3.txt`, spec `mutants_inc004_r3.json`). Q1 overlay in the label · Q2 `═` a day too many · Q3 connector over bars · Q4 `═` with no start · Q5 loop selectable · Q6 filter ignored · Q7 cursor start · Q8 ↵ on no match · Q9 linked linked again · Q10 keys clipped · Q11 S1 · Q12 gantt opens the picker · Q13 `⟲` dropped · Q14 header · Q15 backspace · Q16 one-phase guard (R2-2) · Q17 connector a day late · Q18 esc links · Q19 count · Q20 legend · Q21 "✓ linked" · Q24 cycle not in gantt order (F2) |

### Instrument RED-proof

| Field | Value |
|---|---|
| **Instrument RED-proof** | 2 instruments: the battery reported three SURVIVED mutants at r2 (Q22, Q22b, Q23 — the instrument can say no); TC-512's order oracle, rebuilt from the shipped gantt's paint (F2), turned the reviewer's sorted-by-title mutant from GREEN to RED (Q24) |

### Emitted-form assertion (C-42)

| Field | Value |
|---|---|
| **Emitted-form assertion** | 3 artifacts asserted in their emitted form: the painted screen (compositor strips — frame, gutter marks, status rows, at 118×30 and 80×24), the toasts (`str(toast.render())`), the saved board file (AT-503) |

### Evidence files — bytes at a declared home, verbatim, hash-verified (C-59)

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| `battery.py` — the mutation battery (unchanged since 003) | `.dev-flow/2026-10-04-batch-01/evidence/battery.py` | `a84222ed67665884e0a77f30fd6d4e91e9785cf4d57030fb006fc8ccc42491cb` |
| `inc004-red-on-inc003.txt` — RED of 004's tests on 003's product | `.dev-flow/2026-10-04-batch-01/evidence/inc004-red-on-inc003.txt` | `9bf88d1e720fe37aa97e3c2127f8a5748f65139f95938206b3e1e6b3f5681693` |
| `inc004-f1-red.txt` — F1's arms RED on r1 | `.dev-flow/2026-10-04-batch-01/evidence/inc004-f1-red.txt` | `18c14c9da462cfbeb867e1af7259189b07cc57ac397205874010ddfb03c754df` |
| `mutants_inc004.json` — r1 mutant spec | `.dev-flow/2026-10-04-batch-01/evidence/mutants_inc004.json` | `06def0d24f607159fe26067938301e232707f6e93506c2a0f8cb1cb07d9d224a` |
| `inc004-mutations.txt` — r1 battery, 21/21 | `.dev-flow/2026-10-04-batch-01/evidence/inc004-mutations.txt` | `5448497cfba5309cfa235f796758e4f69b3581955416540e6325341b9527cca0` |
| `mutants_inc004_r2.json` — r2 mutant spec | `.dev-flow/2026-10-04-batch-01/evidence/mutants_inc004_r2.json` | `e446ddf733f66ae34f3b165d30a9fc08b11d1aa4525f565da0f6c3a7e4887c96` |
| `inc004-mutations-r2.txt` — r2 battery, 22/25 | `.dev-flow/2026-10-04-batch-01/evidence/inc004-mutations-r2.txt` | `ee539eb27132c09ffec1d039aad109d8626705a681f04a3aa005de32a9f5a26f` |
| `mutants_inc004_r3.json` — r3 spec (the three survivors) | `.dev-flow/2026-10-04-batch-01/evidence/mutants_inc004_r3.json` | `73c14a8a564b256cc3115ed0135f56d9ba0bb74f59e686358fb5254055cbe8e4` |
| `inc004-mutations-r3.txt` — r3 battery, 3/3 | `.dev-flow/2026-10-04-batch-01/evidence/inc004-mutations-r3.txt` | `03a8c6dc2448b632eddda98fe4df8d1c3848f7e6d41b2a83ddb08c7645b3d291` |
| `inc004-frozen-r1.sha256` — freeze r1 | `.dev-flow/2026-10-04-batch-01/evidence/inc004-frozen-r1.sha256` | `924d9131f04ebe4971fa6582ff08b1eef833c181900937c91162769c2b5d0ef3` |
| `inc004-frozen-r2.sha256` — freeze r2 | `.dev-flow/2026-10-04-batch-01/evidence/inc004-frozen-r2.sha256` | `953fa86c1e080761f6c6bf7c0c4d5748e708785766ad52d905b27be40d7f5404` |
| `inc004-frozen-r3.sha256` — freeze r3 | `.dev-flow/2026-10-04-batch-01/evidence/inc004-frozen-r3.sha256` | `925813cb3a15c7a6197636cc62ac0cc11f0beb6010d45fc24723586934fe25c3` |
| `inc004-gate-r3.txt` — the gate run on r3 | `.dev-flow/2026-10-04-batch-01/evidence/inc004-gate-r3.txt` | `6867a767a4e2ab0f28e18ec8a3353d42d104309e521d28950f22f89668d65b5a` |

| Field | Value |
|---|---|
| **Evidence files** | 13 artifacts at `artifact_homes.evidence`, cited with the digests of their stored bytes (home paths redacted before hashing) |

### Load-bearing emptiness (C-55)

| Field | Value |
|---|---|
| Does any claim here rest on the tree holding NO instance of some case? | yes: "no overlay cell in the label or gutter", "no key dropped at 80 columns" |
| If the result is an ABSENCE, what made the search wide enough | the overlay: every written cell is collected in `facts` and checked against `label_w` for six waiter/candidate pairs (above, below, due off the window, no start, no due); the keys: wide-glyph titles, a 90-character filter, widths 24/40/80 |
| Synthetic instance of the absent case | Q1 (overlay into the label), Q10, Q22, Q22b, Q23 KILLED |
| **Positive control for every probe that returned an ABSENCE** | Q1, Q10, Q22, Q22b, Q23 |

### Reverse census — trigger family B

| Field | Value |
|---|---|
| **Reverse census** | 4 probes: B1 `grep -rln "action_link\|LinkPicker\|gantt_plan\|_gantt_frame" tests/` — `test_link_picker.py`, `test_links.py`, `test_details_links.py` (press `4`, kanban: unaffected; green), the gantt suites (`_gantt_frame` unchanged; green), `test_markup_census.py` (the new sink — found by running it: TC-401 RED until the EXEMPT entry); B2 0 moves; B3 no goldens; B4 the saved board (AT-503 re-reads it); A3 `gantt_link_frame`, `gantt_link_order` read only by `modals.py` |

### Correction population

| Field | Value |
|---|---|
| **Correction population** | 1 correction: "`L` in the gantt opens the link mode, not the picker" — population `grep -rn 'press("3")' tests/ \| xargs grep -l '"L"'` before the edit: none (every picker test drives kanban); README already described link mode (increment 003) |

### Signed-balance test ledger

`post = base − deleted + added` → `2295 = 2282 − 0 + 13` ✓ (13 in `test_gantt_link.py`; 2295 = 2294 passed + the clipboard flake).

---

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — round 1 BLOCK-UNTIL F1: F1 HIGH (product: at 80 columns a wide-glyph title or a long filter wrapped the first status row and pushed the keys out — `len()` for cells, an unclipped filter) → fixed in the increment under construction without stopping (amended authorization), RED-first (`inc004-f1-red.txt`); F2 MED (tests: TC-512's order oracle came from the code under test) → rebuilt from the gantt's paint; F3 LOW (a task in a hidden archived project is in the picker, not in link mode) → ruled D-527 (A-7); F4 LOW (frame ≤ 15 rows: the waiter's group folds, the overlay vanishes) → ux-reviewer at P4; F5 NIT (filter not stripped) → fixed · round 2 (frozen r2) OK to advance: F1 verified on the diff with the r1 repro, F2's mutant RED · r3 (test-only strengthening after the battery) confirmed sound by the reviewer (literal oracles; its own Q22b KILLED) — verdict stays OK to advance · no HIGH open |

---

## 5 · Risks

- F4: in a terminal 18 rows or shorter the waiter's group may not unfold and the overlay is not visible (the status rows still say what is linked); for ux-reviewer.
- Link mode lists the open tasks the gantt draws; a task the view hides is linked from the picker (D-527).

## 6 · Pending items / spec deviations

- A-7: three status rows instead of two; legend after the keys in the picker's form.
- Contract size: ~56k characters vs the 54k budget (`V26` notice, declared at close).

## 7 · Suggested next task

P4 — the orchestrator's gate run, qa-reviewer evaluation, ux-reviewer walkthrough over the close captures.

---

## Increment gate checklist

| # | Item | Owed in | ✓/⚠/✗ | Evidence |
|---|---|---|---|---|
| 1 | ≤4 source files | all | ✓ | 3 / 4 |
| 2 | Tests written in this same increment | all | ✓ | 13 new nodes |
| 3 | Layer 0 where the criterion applies | `core` · `full` | ✓ | TC-511 |
| 4 | **RED counterfactual** | `core` · `full` | ✓ | §4 |
| 5 | **Reverse census** | `core` · `full` | ✓ | §4 |
| 6 | `code-reviewer` passed | `core` · `full` | ✓ | round 2 OK to advance |
| 7 | No file from another lane | all | ✓ | one lane |
| 8 | Frozen interfaces untouched | all | ✓ | none frozen |
| 9 | Coverage on disk | all | ✓ | `pytest --collect-only tests/test_gantt_link.py` → 13 |
| 10 | Load-bearing emptiness | all | ✓ | §4 |
| 11 | **Mutation verdicts** | all | ✓ | 25/25 |
| 12 | **Instrument RED-proof** | all | ✓ | 2 |
| 13 | **Correction population** | all | ✓ | 1 |
| 14 | **Emitted-form assertion** | all | ✓ | 3 |
| 15 | **Independent review** | all | ✓ | `code-reviewer` |
| 16 | **Evidence files** | all | ✓ | 13 |
