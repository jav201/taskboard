# Increment 004 — LLR-102.5, LLR-101.7, LLR-101.10 · the P4 walkthrough's fixes (iterate-to-fix)

> Review packet (flow `templates/increment-template.md`; reserved field names kept literal).
> Lives in the repo next to the diff it describes. Mode `core`, language `en`.

| Field | Value |
|---|---|
| Batch | `2026-10-02-batch-01` |
| Increment | `004` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | LLR-102.5, LLR-101.7, LLR-101.10 (amended, LED .29–.31); LLR-101.8's focused-header seat under decision D7 (no amendment: D7 already keeps the shipped wording); the AT registry of HLR-101, HLR-104, HLR-105 (LED .26–.28) |
| Acceptance | AT-108 through AT-113 (renumbered, one node each) · white-box TC-107, TC-108 (focus fallback), TC-110, TC-116 · unit: TC-107's packet arithmetic |
| Agent | `software-dev` (this runtime's implementing agent) |
| Date | `2026-10-02` |

---

## 1 · What changed

**The P4 walkthrough failed one criterion — the gantt's help was cut mid-word — and this
increment fixes it with two smaller render notes.** The gantt help now prints seven bullets of
at most 44 cells (`▾ abierto, ▸ plegado` restored at code review R2), so every line fits the
48-cell help column; the legend's two longest entries now fit the 56-cell legend column at 118
columns (R1). At half a day per cell the narrow scale label reads `Mondays · .5 d/cell` instead
of clipping. The flow packet starts one cell in when a reach began before the window, so it
never hides the `◂` clip marker. And each acceptance test is now one node (C-18): the second
AT-108 node is AT-113, the four AT-109 nodes are AT-109 to AT-112. Round 3 folds the UX re-check:
a focus that a `/` filter empties keeps the base header wording ` (focused)` (UXV-12, D7 — the
increment-001 header had dropped that fallback), and three help bullets are reworded so `▾`/`▸`
and the bar glyphs read plainly; every bullet is still at most 43 cells.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/views.py` | source | LLR-102.5, LLR-101.7, LLR-101.10, LLR-101.8 (D7) | gantt help wording; legend wording; `.5 d/cell`; packet clear of `◂`; the ` (focused)` header fallback |
| `tests/test_gantt_board.py` | test | HLR-101, HLR-104, HLR-105, LLR-101.7, LLR-101.10, LLR-102.5 | TC-116 help fit (both columns at 118), TC-110 scale label, TC-107 motion, TC-108 focus fallback; AT renames |

| Count | Value |
|---|---|
| **SOURCE files** | **1 / 4** |
| Test files | 1 (uncapped) |
| Doc files | 0 |

## 3 · How to test

```bash
python -m pytest -q tests/test_gantt_board.py -k "help_fits or half_a_day or TC_107 or empties_still or AT_1"
python -m pytest -q
```

## 4 · Test results

| Layer | Owed in | Nodes | Result |
|---|---|---|---|
| **0 · unit** | `core` · `full` | TC-107 (the packet's start and walk over 8 ticks) | 1 passed |
| **A · white-box** `TC-NNN` ↔ LLR | `core` · `full` | TC-116 ×2 (app, both sizes), TC-110 (scale label), TC-107, TC-108 focus fallback | 5 passed |
| **B · black-box** `AT-NNN` ↔ story, through the shipped surface | `core` · `full` | AT-108 through AT-113 (renamed, assertions unchanged) | 6 passed |

P4 gate re-run on the frozen round-3 tree: `python -m pytest -q -p no:cacheprovider` → **1611 passed in 162.76s, exit 0**
(`evidence/full-suite-close.txt`).

### RED counterfactual — executed, not predicted

| Field | Value |
|---|---|
| Mutation applied | the pre-004 tree (increments 002–003 code) for the four new nodes; increment 004's round-1 snapshot for the R1 arm; the round-2 snapshot for the UXV-12 node |
| Where it ran | scratch copies |
| Transcript | `evidence/inc004-red.txt` (4 failed; round 2: the 118×34 arm failed, the 80×24 arm green — that arm measures only the left column; round 3: the UXV-12 node failed on the round-2 snapshot) |
| Restore proven by | the battery's digests: `views.py` back to `38373f7da6c96c01…` after every mutant |
| Bytecode cache | fresh copies, `-p no:cacheprovider` |
| Arms resolved at baseline | 4, then 2, then 1 |
| Verdict granularity | per node (`-rA`) |
| Arms that stayed GREEN | round 2: `test_TC_116_the_gantt_help_fits_its_column[size1]` (80×24 — the right column is out of scope there, BACKLOG) |

| Field | Value |
|---|---|
| **RED counterfactual** | the four new nodes on the pre-004 tree (scratch copy): all RED — help labels 52 cells in a 48-cell column (both sizes), `0.5 d/ce…`, the packet on `◂` · `evidence/inc004-red.txt` · the R1 arm RED on the round-1 snapshot (61 cells in a 56-cell column) · the UXV-12 node RED on the round-2 snapshot (header without ` (focused)`) · restore digests in Mutation verdicts |

| Field | Value |
|---|---|
| **Mutation verdicts** | 5 of 5 KILLED (`evidence/inc004-mutations.txt`, battery re-run on the round-3 tree, harness `evidence/mutate_inc004.py`, restore sha256 `views.py` 38373f7da6c96c01…): H1 a help bullet over the column → 2 of 2 arms red · H2 the leading zero back → 1 of 1 · H3 the packet back on the clip marker → 1 of 1 · H4 a legend line over the legend column → 1 of 2 (the 80×24 arm stays green by design, named) · H5 the ` (focused)` fallback removed → 1 of 1 |

### Instrument RED-proof — every instrument shown able to report FAILURE first

| Instrument | Known-bad input fed to it | The FAILURE it reported |
|---|---|---|
| TC-116's column measure (`label.size.width <= column.content_region.width`) | the increment-003 wording | `52 <= 48` failed (`evidence/inc004-red.txt`) |

| Field | Value |
|---|---|
| **Instrument RED-proof** | 1 instrument, shown failing before its PASS was believed |

### Emitted-form assertion — assert the bytes the producer EMITS (C-42)

| Artifact emitted | The assertion, run against the EMITTED form | What it returned |
|---|---|---|
| the help modal the app paints | TC-116 reads the laid-out `Label` widgets' sizes in the running app | 2 passed |
| the gantt render | TC-110 reads the painted day row; TC-107 the bar cells; TC-108 the rendered header line | 3 passed |

| Field | Value |
|---|---|
| **Emitted-form assertion** | 2 artifacts (4 nodes), each asserted in the form the producer emitted |

### Evidence files — bytes at a declared home, verbatim, hash-verified (C-59)

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| RED proof | `.dev-flow/2026-10-02-batch-01/evidence/inc004-red.txt` | `cbb08d21b98d6d48b4868c1fd0460da5d340c761d21146caf65c62f794a1815c` |
| mutation battery | `.dev-flow/2026-10-02-batch-01/evidence/inc004-mutations.txt` | `73864df42a9adb7c21503bb989cb212f46a41971c18aec962ba4f34a0518ef77` |
| battery harness | `.dev-flow/2026-10-02-batch-01/evidence/mutate_inc004.py` | `6b09eb6b588dc55ffdba4a57a8d2df968d8dcdf4154f8a205a32a581290dfa56` |
| P4 gate run | `.dev-flow/2026-10-02-batch-01/evidence/full-suite-close.txt` | `719e918d5a3474e00637052fc192e7f0d60df7249d41985d23787874ed949a64` |
| gantt at close, 118×30 | `.dev-flow/2026-10-02-batch-01/evidence/captures/close-gantt-118x30.txt` | `02a176966a636167c12eb3123a84b467840c714f22816aa1dd0a6c780e67d568` |
| gantt at close, 80×24 | `.dev-flow/2026-10-02-batch-01/evidence/captures/close-gantt-80x24.txt` | `04a9b2df359a86b184590408281aa20ca80b6512d410c255f33f5fc5e2da4f2c` |
| kanban at close, 118×30 | `.dev-flow/2026-10-02-batch-01/evidence/captures/close-kanban-118x30.txt` | `2c940c98ac69a262b6c0c91691ae5810178e50aa480f854d095d0e2ad3b8cc88` |
| kanban at close, 80×24 | `.dev-flow/2026-10-02-batch-01/evidence/captures/close-kanban-80x24.txt` | `ef6eac0a63ed6144173394f4dbe3ef5b1117fa286cb875ffdbf8347519ae0f84` |

| Field | Value |
|---|---|
| **Evidence files** | 8 artifacts under the declared home, each cited with the digest of its stored bytes (SVG beside each capture) |

### Load-bearing emptiness — what is this resting on that is only true today? (C-55)

| Field | Value |
|---|---|
| Does any claim here rest on the tree holding NO instance of some case? | yes: "no help label is wider than its column" |
| If the result is an ABSENCE, what made the search wide enough | every `Label` in both columns of the running modal, at two terminal sizes |
| Guard labelled as protecting a CONCLUSION, not a behaviour | TC-116's docstring and its inline note on the 80×24 right column |
| Conjunctive criteria: one mutation per conjunct | H1 (usage column) and H4 (legend column) separately |
| Synthetic instance of the absent case | the increment-003 wording on the pre-004 tree |
| **Positive control for every probe that returned an ABSENCE** | the same measure found 52 > 48 and 61 > 56 on the earlier trees (`evidence/inc004-red.txt`) |

### Reverse census — trigger family B

| Probe | Command | Result |
|---|---|---|
| B1 symbols asserted by **other** tests | `grep -rn "help_usage\|_gantt_scale_label\|calendar guide" tests/` | `tests/test_legend.py` and `tests/test_setup_help.py` read `help_usage` generically (all views) — green in the gate run |
| B2 file moved on disk | none | did not fire |
| B3 byte-identical golden captures this source | none | did not fire |
| B4 artifact produced here is consumed elsewhere | the help text → `HelpModal` | its layout is the consumer TC-116 measures |
| A3 | interface consumed by another module changed | none | did not fire |

| Field | Value |
|---|---|
| **Reverse census** | 5 probes: B1 fired (2 files, green), B4 fired (measured by TC-116), B2/B3/A3 did not fire |

### Correction population — enumerated BEFORE the first site was edited

| Correction | Population — the assertion category | Enumeration method (the command) | Count | Sites edited | Sites left, and why |
|---|---|---|---|---|---|
| help text wider than its column | gantt usage bullets and legend entries | `cell_len` of every `help_usage("gantt")` bullet and every gantt legend label in the running modal (TC-116 probe) | 7 + 2 lines | all | the right column below ~118 columns, every view (modal layout) → BACKLOG |
| ATs realised by several nodes | `test_AT_*` functions per AT id | `grep -n "^async def test_AT_\|^def test_AT_" tests/test_gantt_board.py` | 2 ids (6 nodes) | all | none |

| Field | Value |
|---|---|
| **Correction population** | 2 corrections, each enumerated before its first site was edited |

### Signed-balance test ledger

`post = base − deleted + added` → `1611 = 1606 − 0 + 5` ✓ (added: TC-116 ×2, TC-110 scale label,
TC-107, TC-108 focus fallback; the AT renames are in place, net 0).

## 4b · Independent review — the lens the author cannot be

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a named sub-agent with `agents/code-reviewer.md` · round 1 OK to advance, 0 HIGH (the three fixes verified; R1 MEDIUM the legend column overflows at 118, R2 LOW `▾` no longer explained, R3 LOW validation rows) · R1, R2 folded (R1 RED proof appended to `evidence/inc004-red.txt`), R3 handed to the validation re-write · round 2: OK to advance, nothing open; the modal-layout remainder accepted to BACKLOG · round 3 (the UX re-check's UXV-12 fix and three reworded bullets): OK to advance, nothing open — reviewer probed the header at 118×30 (no filter / filter emptying the focus / filter keeping it) and re-measured the bullets ≤ 43 cells; 113 tests green in its scratch copy |

## 5 · Risks

- The help modal's legend column still cuts lines below ~118 columns, in every view (BACKLOG).

## 6 · Pending items / spec deviations

- Help modal layout (BACKLOG); UXV-7, UXV-9 and the walkthrough's operator questions (BACKLOG).

## 7 · Suggested next task

P4 re-validation, then P5 close.

## Increment gate checklist

| # | Item | Owed in | ✓/⚠/✗ | Evidence (node id · command output · file:line) |
|---|---|---|---|---|
| 1 | ≤4 source files, or reason declared | all | ✓ | 1 / 4 |
| 2 | Tests written in this same increment | all | ✓ | 5 new nodes |
| 3 | Layer 0 written where the criterion applies | `core` · `full` | ✓ | TC-107 |
| 4 | **RED counterfactual** declared | `core` · `full` | ✓ | §4 |
| 5 | **Reverse census** declared | `core` · `full` | ✓ | §4 |
| 6 | `code-reviewer` passed | `core` · `full` | ✓ | §4b |
| 7 | No file from another lane touched | all | ✓ | one lane |
| 8 | Frozen interfaces untouched (or returned to the trunk) | all | ✓ | wording, one offset and one header fallback only |
| 9 | Coverage claims verified **on disk**, not from intent | all | ✓ | ids in docstrings |
| 10 | Load-bearing emptiness declared, with its synthetic instance (C-55) | all | ✓ | §4 |
| 11 | **Mutation verdicts** declared | all | ✓ | §4 |
| 12 | **Instrument RED-proof** declared | all | ✓ | §4 |
| 13 | **Correction population** declared | all | ✓ | §4 |
| 14 | **Emitted-form assertion** declared | all | ✓ | §4 |
| 15 | **Independent review** names somebody | all | ✓ | §4b |
| 16 | **Evidence files** declared | all | ✓ | §4 |
