# Increment 002 — HLR-108 · the colour budget on the kanban (and its census over both views)

> Review packet (flow `templates/increment-template.md`; reserved field names kept literal).
> Lives in the repo next to the diff it describes. Mode `core`, language `en`.

| Field | Value |
|---|---|
| Batch | `2026-10-02-batch-01` |
| Increment | `002` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | HLR-108; LLR-103.1, LLR-103.3 (LLR-103.2, the gantt's chain, landed in increment 001 and is pinned here) |
| Acceptance | AT-106 · white-box TC-117, TC-118, TC-119 · unit: none (one-line tone choices; no unit with ≥ 3 paths) |
| Agent | `software-dev` (this runtime's implementing agent) |
| Date | `2026-10-02` |

---

## 1 · What changed

**On the kanban and gantt panels the accent now marks only the `/` filter field and today's
marks** — the round-7 colour budget, scoped by D10. Five kanban sites left the accent: the
`KANBAN` titles (now bold bright, in every layout), the card's `↗` link token (`mut`), the
≤7-day `+Nd` due token (`mut`), the horizon grouping's "This week" (`hd`, D11), and the
matrix percent (`hd`). `header()` gained a `tone` so a title too wide for its panel is clipped
in its own colour instead of falling back to the accent (code review F1); the kanban and gantt
pass `bright`, the other seven views keep the default (D10). The gantt's focused header now
escapes its whole `(focused: …)` text once, so a name ending in `\` is painted as typed (F3).

The two shared helpers (`card_cell`'s `↗`, `reldue_token`'s within-the-week tone) also reach
the Focus review rail, People and Agenda — the same tokens change there too (D10, accepted).

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/views.py` | source | HLR-108, LLR-103.1, LLR-103.3, LLR-101.8 | five tone sites; `header(…, tone=)`; focused-header escape |
| `tests/test_colour_budget.py` | test | HLR-108, LLR-103.1, LLR-103.2, LLR-103.3 | AT-106; TC-117, TC-118, TC-119 (14 nodes) |
| `tests/test_cells.py` | test | LLR-103.3 | the `+4d` arm: `mut`, not accent |
| `tests/test_gantt_board.py` | test | LLR-101.8 | the trailing-backslash header node (F3) |

| Count | Value |
|---|---|
| **SOURCE files** | **1 / 4** |
| Test files | 3 (uncapped) |
| Doc files | 0 |

## 3 · How to test

```bash
python -m pytest -q tests/test_colour_budget.py tests/test_cells.py
python -m pytest -q                       # the whole suite
python .dev-flow/2026-10-02-batch-01/evidence/capture.py <out> inc002 kanban,gantt
```

## 4 · Test results

| Layer | Owed in | Nodes | Result |
|---|---|---|---|
| **0 · unit** | `core` · `full` | n/a — no changed unit has ≥ 3 paths or crosses a module boundary (five tone literals and one keyword) | — |
| **A · white-box** `TC-NNN` ↔ LLR | `core` · `full` | TC-117 ×4, TC-118, TC-119 ×8 (kanban census over 180 combinations, non-vacuity, shared tokens, gantt ×5 widths) | 13 passed |
| **B · black-box** `AT-NNN` ↔ story, through the shipped surface | `core` · `full` | AT-106 (keys `4`, `Tab`, `Tab`, `3`, `/` in the running app) | 1 passed |

Full suite: `python -m pytest -q -p no:cacheprovider` → **1606 passed in 167.58 s, exit 0**
(`evidence/inc002-green.txt`).

### RED counterfactual — executed, not predicted

| Field | Value |
|---|---|
| Mutation applied | the increment-001 tree (the five sites in their accent form) for the first nodes; the round-1 snapshot for the review-fold nodes |
| Where it ran | scratch copies only |
| Transcript | `evidence/inc002-red.txt` (7 failed / 3 passed); `evidence/inc002-review-red.txt` (3 failed / 6 passed) |
| Restore proven by | the battery's per-mutant digest: `views.py` back to `d61c192f…` |
| Bytecode cache | fresh copies, `-p no:cacheprovider` |
| Arms resolved at baseline | 10 (first run); 9 (review-fold run) |
| Verdict granularity | per node (`-rA`) |
| Arms that stayed GREEN | first run: the census's non-vacuity arm (by design), TC-117 gantt and TC-118 (increment 001's gantt budget, pinned here); review run: the gantt census at 118/80/60/40 (the fallback only bites at 24) and the two arms unaffected by the header |

| Field | Value |
|---|---|
| **RED counterfactual** | the five kanban sites reverted to their increment-001 accent (scratch copy of the tree): 7 of 10 nodes RED — the kanban census, the shared-token arm, three kanban title arms, AT-106 and the `+4d` arm · `evidence/inc002-red.txt` · the copy was rebuilt, not mutated in place; the battery's restore digest is `views.py` `d61c192f…` (Mutation verdicts) |

| Field | Value |
|---|---|
| **Mutation verdicts** | 6 of 6 KILLED (`evidence/inc002-mutations.txt`, harness `evidence/mutate_inc002.py`, restore sha256 `views.py` d61c192f…): K1 `↗` back to accent → 2 of 2 arms red · K2 `+Nd` back to accent → 3 of 3 · K3 "This week" back to accent → 1 of 1 · K4 matrix percent back to accent → 2 of 2 · K5 grouped title back to accent → 2 of 5 (the lanes, matrix and gantt title arms stay green, named) · K6 clipped title falls back to accent → 2 of 8 (the kanban census and the gantt 24×10 arm; the wider gantt arms stay green, named) |

### Instrument RED-proof — every instrument shown able to report FAILURE first

| Instrument | Known-bad input fed to it | The FAILURE it reported |
|---|---|---|
| `accent_runs` (the census detector) | the app's painted Content, whose `Style` spells colour `rgb(45,212,191)` | first run: `assert any(...)` failed in AT-106 — the detector could not see the accent in the app; fixed to read both spellings |
| `accent_runs` on the render `Text` | the increment-001 tree (accent kanban title) | `test_TC_119_the_kanban_paints_no_accent` RED (`evidence/inc002-red.txt`) |

| Field | Value |
|---|---|
| **Instrument RED-proof** | 2 instruments (the detector in both of its readings), each shown reporting a FAILURE before a PASS was believed |

### Emitted-form assertion — assert the bytes the producer EMITS (C-42)

| Artifact emitted | The assertion, run against the EMITTED form | What it returned |
|---|---|---|
| the kanban and gantt panels the app paints | AT-106 reads `app.query_one("#board").render()` spans, in Textual's own `rgb()` spelling | 1 passed |
| the render `Text` | TC-117/119 read rich span styles (`#2dd4bf`) | 13 passed |

| Field | Value |
|---|---|
| **Emitted-form assertion** | 2 artifacts, each asserted on the producer's own spans |

### Evidence files — bytes at a declared home, verbatim, hash-verified (C-59)

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| RED on the increment-001 tree | `.dev-flow/2026-10-02-batch-01/evidence/inc002-red.txt` | `03614470fa52a73fa884a71172c142ed39b9ed6d396e90c9b8071dbe556b8598` |
| review-fold RED proof | `.dev-flow/2026-10-02-batch-01/evidence/inc002-review-red.txt` | `236f376180a4a687656fcec2da5341a66eaf0eaeefb830e28d7842b9a9443b8f` |
| mutation battery | `.dev-flow/2026-10-02-batch-01/evidence/inc002-mutations.txt` | `6e84e582704b6562901939ab959f47eebf78670d6ce3b7b83e68a215d1d554b8` |
| battery harness | `.dev-flow/2026-10-02-batch-01/evidence/mutate_inc002.py` | `bb450551f4885e2e9a2f41c590d013fdf0e9a02bfa372b2933cb267ba585d36a` |
| suite run | `.dev-flow/2026-10-02-batch-01/evidence/inc002-green.txt` | `cd93df9841952c81cc143f980ae4e6e6f7751367427610ef8795af5b69bada62` |
| kanban before, 118×30 | `.dev-flow/2026-10-02-batch-01/evidence/captures/base-kanban-118x30.txt` | `2c940c98ac69a262b6c0c91691ae5810178e50aa480f854d095d0e2ad3b8cc88` |
| kanban before, 80×24 | `.dev-flow/2026-10-02-batch-01/evidence/captures/base-kanban-80x24.txt` | `ef6eac0a63ed6144173394f4dbe3ef5b1117fa286cb875ffdbf8347519ae0f84` |
| kanban after, 118×30 | `.dev-flow/2026-10-02-batch-01/evidence/captures/inc002-kanban-118x30.txt` | `2c940c98ac69a262b6c0c91691ae5810178e50aa480f854d095d0e2ad3b8cc88` |
| kanban after, 80×24 | `.dev-flow/2026-10-02-batch-01/evidence/captures/inc002-kanban-80x24.txt` | `ef6eac0a63ed6144173394f4dbe3ef5b1117fa286cb875ffdbf8347519ae0f84` |

| Field | Value |
|---|---|
| **Evidence files** | 9 artifacts under the declared home, each cited with the digest of its stored bytes (colour lives in the `.svg` beside each capture) |

### Load-bearing emptiness — what is this resting on that is only true today? (C-55)

| Field | Value |
|---|---|
| Does any claim here rest on the tree holding NO instance of some case? | yes: "the kanban paints no accent" is an absence |
| If the result is an ABSENCE, what made the search wide enough | the census spans 3 layouts × 3 groups × 2 sorts × focus on/off × 5 widths (180 renders, all asserted reached) on a board carrying every P-4 site (a URL card, near dues, horizon groups, the matrix) |
| Guard labelled as protecting a CONCLUSION, not a behaviour | `test_TC_119_the_census_can_see_the_accent` — its docstring says it proves the empty census means none |
| Conjunctive criteria: one mutation per conjunct | one mutant per site (K1–K6) |
| Synthetic instance of the absent case | the oracle board plus the URL card `tw6` |
| **Positive control for every probe that returned an ABSENCE** | the same detector finds today's rule on the gantt and the filter field on a filtered kanban (non-vacuity node); it found the increment-001 tree's accent title (RED run) |

### Reverse census — trigger family B

| Probe | Command | Result |
|---|---|---|
| B1 symbols asserted by **other** tests | full suite on a scratch copy with the five edits (pre-measured) + `grep -rn "accent" tests/` | 1 node: `test_cells.py::test_card_cell_shows_the_deadline_countdown_on_every_dated_card` (the `+4d` arm), rewritten; `header()` callers in 9 views — the default keeps 7 unchanged (suite green) |
| B2 file moved on disk | none moved | did not fire |
| B3 byte-identical golden captures this source | `ls tests/goldens` → none | did not fire |
| B4 artifact produced here is consumed elsewhere | `card_cell` / `reldue_token` → Focus rail, People, Agenda | consumed; the shared-token arm asserts their new tone; D10 |
| A3 | interface consumed by another module changed | `header()` gained an optional keyword with the old default | did not break a caller (suite green) |

| Field | Value |
|---|---|
| **Reverse census** | 5 probes: B1 fired (1 node rewritten), B4 fired (shared tokens, asserted), B2/B3/A3 did not fire with their probes named |

### Correction population — enumerated BEFORE the first site was edited

| Correction | Population — the assertion category | Enumeration method (the command) | Count | Sites edited | Sites left, and why |
|---|---|---|---|---|---|
| non-focus accent on the kanban/gantt panels | accent-painted runs in rendered kanban/gantt | the P-4 census over rendered spans (`evidence/p0-probes.txt`) | 9 kinds of site | all | none; titles of other views left by D10 |
| clipped titles in accent | callers of `header()` | `grep -n "header(" taskboard/views.py` | 9 views | the 4 kanban/gantt calls | 7 other views keep the default (D10) |

| Field | Value |
|---|---|
| **Correction population** | 2 corrections, each enumerated before its first site was edited |

### Signed-balance test ledger

`post = base − deleted + added` → `1606 = 1588 − 0 + 18` ✓ against the run's own figure (added:
14 in `tests/test_colour_budget.py`, 1 trailing-backslash node, and 3 README nodes increment 003
added to the tree in the same interval; `test_cells.py` rewritten in place, net 0).

## 4b · Independent review — the lens the author cannot be

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a named sub-agent with `agents/code-reviewer.md` · round 1 BLOCK-UNTIL F1 (1 HIGH: a title too wide for its panel fell back to the accent on both views — 160 kanban configurations at 60/24 columns) · F1, F2, F3 folded with RED proof (`evidence/inc002-review-red.txt`) · round 2: OK to advance, 0 HIGH; the reviewer adds that the `_strip` width bug (F5 of increment 001) also reaches header rows — added to that BACKLOG entry |

## 5 · Risks

- Titles differ by view until the app-wide pass (D10; operator question UX-6).
- The `↗` and `+Nd` tokens changed in the Focus rail, People and Agenda too (shared helpers, D10).

## 6 · Pending items / spec deviations

- App-wide colour budget (other titles, keybar hints, ribbon clock, setup hints) — BACKLOG.
- F5 now also covers header rows with bracketed focus names — BACKLOG.

## 7 · Suggested next task

Increment 003 — README.md and RUN.md (HLR-109).

## Increment gate checklist

| # | Item | Owed in | ✓/⚠/✗ | Evidence (node id · command output · file:line) |
|---|---|---|---|---|
| 1 | ≤4 source files, or reason declared | all | ✓ | 1 / 4 |
| 2 | Tests written in this same increment | all | ✓ | `tests/test_colour_budget.py` |
| 3 | Layer 0 written where the criterion applies | `core` · `full` | ✓ | n/a — no unit meets the criterion (§4) |
| 4 | **RED counterfactual** declared | `core` · `full` | ✓ | §4; `evidence/inc002-red.txt` |
| 5 | **Reverse census** declared | `core` · `full` | ✓ | §4 |
| 6 | `code-reviewer` passed | `core` · `full` | ✓ | §4b: round 2 OK, 0 HIGH |
| 7 | No file from another lane touched | all | ✓ | one lane |
| 8 | Frozen interfaces untouched (or returned to the trunk) | all | ✓ | `header()` keyword is optional with the old default |
| 9 | Coverage claims verified **on disk**, not from intent | all | ✓ | AT/TC ids in the docstrings of `tests/test_colour_budget.py` |
| 10 | Load-bearing emptiness declared, with its synthetic instance (C-55) | all | ✓ | §4 |
| 11 | **Mutation verdicts** declared | all | ✓ | §4; 6/6 |
| 12 | **Instrument RED-proof** declared | all | ✓ | §4 |
| 13 | **Correction population** declared | all | ✓ | §4 |
| 14 | **Emitted-form assertion** declared | all | ✓ | §4 |
| 15 | **Independent review** names somebody | all | ✓ | §4b |
| 16 | **Evidence files** declared | all | ✓ | §4 |
