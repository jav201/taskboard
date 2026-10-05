# Increment 006 — HLR-501, HLR-502, HLR-505 (LLR-501.2, LLR-502.3, LLR-505.2) · the operator's verdict: D-528, D-529, D-530

> Review packet (flow `templates/increment-template.md`; reserved field names kept literal). Mode
> `core`, language `en`. The batch re-opened after P5 (D-531, the D-422 path): the operator accepted
> PV-1..PV-7 and ruled D-528, D-529, D-530 "Corregirlo antes del push". Revision 2 (frozen r2): code
> review round 1 OK to advance with M1 (MED, product, in the increment under construction — fixed
> RED-first), M2 (MED, tests), M3 (MED, recorded); security delta PASS-WITH-NOTES.

| Field | Value |
|---|---|
| Batch | `2026-10-04-batch-01` |
| Increment | `006` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | LLR-502.3 (A-9), LLR-501.2 (A-10), LLR-505.2 (A-11); D-528..D-534 |
| Acceptance | AT-508 (read-only arm), AT-501 (lanes arm, new law) · TC-504, TC-512, TC-515 |
| Agent | `software-dev` |
| Date | `2026-10-04` |

---

## 1 · What changed

**The waiting task's row stays on screen in the gantt link mode, a lanes card always shows a
readable title, and a read-only board leaves nothing behind.**

- **D-528 (link mode):** the gantt's fold allocation takes an optional pinned group, unfolded like
  the selection; link mode pins the waiter's group and pages it to the waiter. When the candidate's
  and the waiter's groups cannot both be drawn whole they share the rows left (the pinned group
  half); when both are in one over-tall group the page is chosen to hold both whenever one can
  (D-534). The note "‹waiter› is folded — a taller terminal draws the link" remains only as the
  fallback where the rows are genuinely too few — a terminal of 12 rows or fewer, or, in one
  over-tall group, a candidate further from the waiter than one page (seen at 13–20 rows; ux R6-1). Outside link mode
  nothing is pinned: the plain gantt is byte-identical to before (code review, executed sweep).
- **D-529 (lanes):** a lanes card's title keeps 6 cells (5 characters and `…` — the readability
  measure counts a title once its first word shows, and the kg board's median first word is 5)
  before any indicator: `▸` then `◂` are shed first, one at a time, then the other meta from the
  left. Only the lanes pass the floor; every other card keeps the shipped law, so `test_cells.py`
  stands. **Consequence, stated for the operator (D-533): at 118 columns every lanes cell is 19
  cells wide, so lanes paint no `◂`/`▸` at all; the marks appear from about 160 columns.** Waiting
  stays visible in the grouped kanban, the gantt gutter and the details section.
- **D-530 (migration save):** `save_atomic` refuses a read-only board before anything is written
  (the error names the board: "board.json: Permission denied"); on any failure its temp file is
  removed, a copied read-only bit cleared first, and a cleanup error never masks the save's own.
  The migration still fails closed (the app exits; backup and log removed). On Linux/macOS a
  read-only board is now refused too, where a rename used to replace it silently (D-532).

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/views.py` | source | LLR-502.3, LLR-501.2 | `gantt_plan(pinned=)`, `_gantt_frame(pinned_id=)` with the shared rows and the two-row page; `gantt_link_frame` pins the waiter; `CARD_TITLE_FLOOR`, `card_cell(title_floor=)`, the lanes call |
| `taskboard/models.py` | source | LLR-505.2 | `Board.save_atomic`: the read-only refusal and the temp file's cleanup |
| `tests/test_gantt_link.py` | test | LLR-502.3 | NEW the pin test (118×20, 118×14, the shipped rule untouched), the one-page test; the fallback test moved to 118×12 |
| `tests/test_links.py` | test | LLR-501.2 | NEW TC-504 ×3 (titles readable in lanes at 118×30, 80×24, 118×40), the marks-first unit test, the 160×40 exact-counts arm; AT-501's lanes arm to the new law |
| `tests/test_link_migration.py` | test | LLR-505.2 | NEW TC-515 read-only, AT-508 read-only, the failed-swap cleanup arm |

| Count | Value |
|---|---|
| **SOURCE files** | **2 / 4** |
| Test files | 3 (uncapped) |
| Doc files | 0 (records: A-9..A-11, D-528..D-534, LED .20–.22; BACKLOG) |

## 3 · How to test

```bash
python -m pytest -q -p no:cacheprovider tests/test_gantt_link.py tests/test_links.py tests/test_link_migration.py tests/test_cells.py
python -m pytest -q -p no:cacheprovider          # the gate
```

## 4 · Test results

| Layer | Owed in | Nodes | Result |
|---|---|---|---|
| **0 · unit** | `core` · `full` | the marks-first unit test; TC-515 read-only, the cleanup arm; the one-page test | passed |
| **A · white-box** `TC-NNN` ↔ LLR | `core` · `full` | TC-504 ×5, TC-512 ×2, TC-515 ×2 | passed |
| **B · black-box** `AT-NNN` ↔ story | `core` · `full` | AT-508 read-only; AT-501 (lanes arm) | passed |

Gate run on frozen r2: `python -m pytest -q -p no:cacheprovider` → **2306 passed in 414.80 s**, exit 0 (`.dev-flow/2026-10-04-batch-01/evidence/inc006-gate-r2.txt`; r1: 2304 passed, `inc006-gate-r1.txt`) — the clipboard test passed in both runs.

### RED counterfactual — executed, not predicted

| Field | Value |
|---|---|
| **RED counterfactual** | the first arms on the product as closed (increment 005 frozen r3): 6 FAILED — TC-515 and AT-508 read-only (a `.board.json.<random>.tmp` left; the error named it), the pin test (the waiter's group folded at 118×20), TC-504 ×3 (`▊ ++  ▸1 ◂1 +6d`, a card with no title) (`evidence/inc006-red.txt`); M1's test FAILED on r1 — (11, tw3, tw4) paged apart (`evidence/inc006-m1-red.txt`); the marks-first, cleanup and 160×40 arms are pinned by mutants S2, S10, S8/S9 |

| Field | Value |
|---|---|
| **Mutation verdicts** | **12 of 12 KILLED** on r2 (`evidence/inc006-mutations-r2.txt`, spec `mutants_inc006_r2.json`): S1 no read-only check · S2 the cleanup keeps the read-only bit · S3 the save's error swallowed · S4 the pin ignored · S5 the pinned group not paged to the waiter · S6 no sharing of the rows · S7 link mode does not pin · S8 floor 3 · S9 the lanes pass no floor · S10 marks not shed first · S11 no floor in the budget · S12 the page not chosen to hold both (M1). r1: 11/11 (`inc006-mutations-r1.txt`) |

### Instrument RED-proof

| Field | Value |
|---|---|
| **Instrument RED-proof** | 1 instrument: the battery's per-node RED/GREEN listing named which arm killed each mutant (e.g. S2 only by the Windows cleanup arm) |

### Emitted-form assertion (C-42)

| Field | Value |
|---|---|
| **Emitted-form assertion** | 3 artifacts in their emitted form: the painted screen (lanes and link mode, compositor strips), the files beside the board (directory listing after each run), the error string the app prints on exit (`capsys`) |

### Evidence files — bytes at a declared home, verbatim, hash-verified (C-59)

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| `inc006-red.txt` | `.dev-flow/2026-10-04-batch-01/evidence/inc006-red.txt` | `fd01a004d504da174cda1a7ee9cbad26242403d78783ae0511946a84db797f30` |
| `inc006-m1-red.txt` | `.dev-flow/2026-10-04-batch-01/evidence/inc006-m1-red.txt` | `a1dc2aadf7207bab5f8a71408018fc9b9a078ee1246e70f80f86a6aa899a8df2` |
| `mutants_inc006_r1.json` | `.dev-flow/2026-10-04-batch-01/evidence/mutants_inc006_r1.json` | `8b13eb6558f808a2f0a2628fb96689177ac96e57a8877bfe5775730f29291c02` |
| `inc006-mutations-r1.txt` | `.dev-flow/2026-10-04-batch-01/evidence/inc006-mutations-r1.txt` | `d6b6880c33c10a58689067682652e568664adc34e8eff90b8d789d0fce885ac9` |
| `mutants_inc006_r2.json` | `.dev-flow/2026-10-04-batch-01/evidence/mutants_inc006_r2.json` | `2bbc03ac96d41b614c813e1dcf5e641d37ed738e90a06285186de83c22d27717` |
| `inc006-mutations-r2.txt` | `.dev-flow/2026-10-04-batch-01/evidence/inc006-mutations-r2.txt` | `c594847d38dba18c761a4ca94c7bc81e2bd183cf596c69cc13be08260efc7de2` |
| `inc006-frozen-r1.sha256` | `.dev-flow/2026-10-04-batch-01/evidence/inc006-frozen-r1.sha256` | `5e08d25a4ea691e3d4ec31aa4a47c78a3be43705741022222cd88e6db181a8cd` |
| `inc006-frozen-r2.sha256` | `.dev-flow/2026-10-04-batch-01/evidence/inc006-frozen-r2.sha256` | `cdd2620a32c7a5e7d3ddde13fc6f71e79f87c31463fbab7a73e28992236b85ad` |
| `inc006-gate-r1.txt` | `.dev-flow/2026-10-04-batch-01/evidence/inc006-gate-r1.txt` | `be3eefe837e04782d81135e417096293bd2d1cab9ff5ff870f2324ac9ddb89c3` |
| `inc006-gate-r2.txt` | `.dev-flow/2026-10-04-batch-01/evidence/inc006-gate-r2.txt` | `c6bd6d74d585145cb03ead4fd1ea86cd2dacb1b4d8af583df758131804b561ef` |
| `battery.py` | `.dev-flow/2026-10-04-batch-01/evidence/battery.py` | `a84222ed67665884e0a77f30fd6d4e91e9785cf4d57030fb006fc8ccc42491cb` |

| Field | Value |
|---|---|
| **Evidence files** | 11 artifacts at `artifact_homes.evidence`, cited with the digests of their stored bytes (home paths redacted before hashing) |

### Load-bearing emptiness (C-55)

| Field | Value |
|---|---|
| Does any claim here rest on the tree holding NO instance of some case? | yes: "nothing is left beside a read-only board", "no lanes card paints a title under 5 characters", "the plain gantt is unchanged" |
| If the result is an ABSENCE, what made the search wide enough | the directory listing after two runs and after an app start; every lanes card cell at 118×30, 80×24, 118×40; the reviewer's byte-hash sweep of the plain gantt over every selection, both archive settings and seven sizes |
| Synthetic instance of the absent case | S1, S2 (a temp file left), S8, S9, S11 (a short title), S4–S7 KILLED |
| **Positive control for every probe that returned an ABSENCE** | S1, S2, S8, S9, S11 |

### Reverse census — trigger family B

| Field | Value |
|---|---|
| **Reverse census** | 4 probes: B1 `grep -rln "card_cell\|gantt_plan\|_gantt_frame\|save_atomic" tests/` → `test_cells.py` (the shipped width law — unchanged, the floor is the lanes' only), `test_kanban_readable.py`, the gantt suites (green: no pin outside link mode), `test_links.py` AT-501 (its lanes arm pinned all 8 `◂` at 118×40 — superseded by the operator's D-529, rewritten to the new law with the reason in its docstring, and a 160×40 exact arm added), `test_link_migration.py` (green); B4 the board file and its folder (listing asserted) |

### Correction population

| Field | Value |
|---|---|
| **Correction population** | 1 correction: "lanes paint every mark" → "lanes shed the marks before a title drops below 6 cells" — population `grep -rn "lanes" tests/test_links.py tests/test_kanban_readable.py README.md`: AT-501's lanes arm (rewritten); README describes `◂N`/`▸N` without a lanes claim (unchanged) |

### Signed-balance test ledger

`post = base − deleted + added` → `2306 = 2296 − 0 + 10` ✓ (3 in `test_link_migration.py`, 2 in `test_gantt_link.py`, 5 in `test_links.py` — TC-504 ×3 parametrized, the marks-first unit, the 160×40 arm).

---

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — round 1 (r1) OK to advance, no HIGH: the plain gantt byte-identical to base over every selection × archive setting × previous × seven sizes (executed); M1 MED (product: same-group pages left the waiter out although both fit — fixed RED-first, D-534), M2 MED (tests: AT-501's lanes arm vacuous at 118 — the 160×40 exact arm added), M3 MED (the read-only refusal is cross-platform — recorded, D-532), L1 LOW noted; the lanes consequence stated for the operator (D-533) · round 2 (r2) OK to advance: M1 verified on the diff (the page start always holds both rows when the aligned page misses one; inert without a pin — the plain gantt still byte-identical over the 1,218-frame sweep (2 archive settings × 29 selections × 3 previous × 7 sizes, line map and plan hashed too)); same-group misses at 118 fell by exactly the 52 "both fit" cases; M2's arm present; D-532..D-534 accepted · `security-reviewer` delta: PASS-WITH-NOTES — the `save_atomic` delta reviewed (TOCTOU, symlinks, cleanup chmod only on its own temp file, no masked error), the safeguard re-run on synthetic boards (backup before, `.1`, log exact, `u` one step with the mark kept, run-once byte-identical, fail-closed, read-only ×3 launches nothing left), S1 (a home path in a mutant spec) redacted and re-verified, N1–N4 INFO |

---

## 5 · Risks

- D-533: at the common 118 width the lanes show no link marks; they appear from about 160 columns.
- D-532: on Linux/macOS a read-only board is now refused (it used to be replaced through the folder).
- The fallback note says "folded" also when the waiter's group is unfolded but paged (≤ 12-row terminals).

## 6 · Pending items / spec deviations

- A-9, A-10, A-11.

## 7 · Suggested next task

Light P4 (qa, ux, security delta — done above), re-close P5.

---

## Increment gate checklist

| # | Item | Owed in | ✓/⚠/✗ | Evidence |
|---|---|---|---|---|
| 1 | ≤4 source files | all | ✓ | 2 / 4 |
| 2 | Tests written in this same increment | all | ✓ | 10 new nodes |
| 3 | Layer 0 where the criterion applies | `core` · `full` | ✓ | §4 |
| 4 | **RED counterfactual** | `core` · `full` | ✓ | §4 |
| 5 | **Reverse census** | `core` · `full` | ✓ | §4 |
| 6 | `code-reviewer` passed | `core` · `full` | ✓ | OK to advance |
| 7 | No file from another lane | all | ✓ | one lane |
| 8 | Frozen interfaces untouched | all | ✓ | none frozen |
| 9 | Coverage on disk | all | ✓ | `pytest --collect-only` on the three files |
| 10 | Load-bearing emptiness | all | ✓ | §4 |
| 11 | **Mutation verdicts** | all | ✓ | 12/12 |
| 12 | **Instrument RED-proof** | all | ✓ | 1 |
| 13 | **Correction population** | all | ✓ | 1 |
| 14 | **Emitted-form assertion** | all | ✓ | 3 |
| 15 | **Independent review** | all | ✓ | `code-reviewer`, `security-reviewer` |
| 16 | **Evidence files** | all | ✓ | 11 |
