# Increment 004 — HLR-205, HLR-208, HLR-209, HLR-210 · the gantt field: page hint, urgency, weekends, clip arrows

> Review packet (flow `templates/increment-template.md`; reserved field names kept literal).
> Lives in the repo next to the diff it describes. Mode `core`, language `en`. Flow pinned to rev98.

| Field | Value |
|---|---|
| Batch | `2026-10-02-batch-02` |
| Increment | `004` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | HLR-205 (LLR-205.1), HLR-208 (LLR-207.1, urgency half), HLR-209 (LLR-209.1, amended LED .18), HLR-210 (LLR-210.1) |
| Acceptance | AT-205, AT-208, AT-209, AT-210 · white-box TC-207, TC-209, TC-211, TC-212 |
| Agent | `software-dev` (this runtime's implementing agent) |
| Date | `2026-10-02` |

---

## 1 · What changed

**A paged project now says what is off its page** — one dim row under the page, `▲ 19 above / ▼ 12
below` (each part only when non-zero); pages shrink by that row, and a room of one row pages as
shipped. **Urgent projects are offered rows first**: the fold order counts open tasks due today or
earlier, then the most due today, then the earliest due — so at 80×24 Ops & Security, which holds
the only task due today, now opens on entry (API Platform folds instead). **Weekends are shaded**
on the day row and every body row's field when a cell is at most a day, in `#1a1d22` — a declared
palette key that lands on 256-colour index 234 where the prototype's `#161d27` landed on the field's
own index 16. **The echo's clipped ends draw `◂`/`▸`** instead of a bracket on the window's edge
(UXV-7), in the bracketed and the open-ended forms. Two existing laws caught the first weekend
shape (an undeclared hex; a second tag per cell that defeated `collapse_runs`); both were fixed in
the code, the laws untouched.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/views.py` | source | LLR-205.1, LLR-207.1, LLR-209.1, LLR-210.1 | `_gantt_frame` paging + hint row; `gantt_plan` pressure; `HEX["weekend"]`, `WEEKEND_BG`, `GanttAxis.weekends()`, `_on_weekend`, `_gantt_field` and `gantt_day_row` shading; `gantt_echo` clip arrows |
| `tests/test_gantt_polish.py` | test | HLR-205, HLR-208, HLR-209, HLR-210, LLR-205.1, LLR-207.1, LLR-209.1, LLR-210.1 | NEW: 19 nodes (AT-205, AT-208, AT-209, AT-210; TC-207 ×4, TC-209 ×2, TC-211 ×5, TC-212 ×4) |
| `tests/test_gantt_board.py` | test | HLR-205 | reverse census (qa Q-14): TC-106 pages of 19, in place |

| Count | Value |
|---|---|
| **SOURCE files** | **1 / 4** |
| Test files | 2 (uncapped) |
| Doc files | 0 |

## 3 · How to test

```bash
python -m pytest -q tests/test_gantt_polish.py tests/test_gantt_board.py tests/test_prism_laws.py tests/test_span_economy.py
python -m pytest -q
```

## 4 · Test results

| Layer | Owed in | Nodes | Result |
|---|---|---|---|
| **0 · unit** | `core` · `full` | `GanttAxis.weekends()` (TC-211 k = 0.5), `gantt_echo` forms (TC-212 ×3), `gantt_plan` pressure (TC-209 ×2) | 6 passed |
| **A · white-box** `TC-NNN` ↔ LLR | `core` · `full` | TC-207 ×4, TC-211 ×4 (renders) , TC-212 tw2 | 9 passed |
| **B · black-box** `AT-NNN` ↔ story, through the shipped surface | `core` · `full` | AT-205, AT-208, AT-209, AT-210 | 4 passed |

Gate run on the frozen round-1 tree: `python -m pytest -q -p no:cacheprovider` → **1662 passed in
183.68s, exit 0** (`evidence/inc004-green.txt`).

### RED counterfactual — executed, not predicted

| Field | Value |
|---|---|
| Mutation applied | per feature, the BASE behaviour re-applied on the increment tree (the base tree cannot import `WEEKEND_BG`: a collection error, recorded in `inc004-red.txt`, is not a RED of record); then 15 mutants |
| Where it ran | scratch exports (CRLF, as the checkout stores them) |
| Transcript | `evidence/inc004-mutations.txt`; `evidence/inc004-red.txt` (the collection error, declared) |
| Restore proven by | per-mutant sha256, byte-exact harness `evidence/mutate_bytes.py` (`views.py` `ca9202adea9aa4df…`) |
| Bytecode cache | `-B`, `-p no:cacheprovider` |
| Arms resolved at baseline | 19 + TC-106 |
| Verdict granularity | per node (`-rA`) |
| Arms that stayed GREEN | per mutant, named in the transcript |

| Field | Value |
|---|---|
| **RED counterfactual** | base behaviours re-applied: G1 (pages of the whole room, TC-106 + TC-207 RED), G2 (no hint), G4 (late-only urgency: TC-209 + AT-208 RED), G6 (no shading at k = 1), G7/G8 (body / day row unshaded), G11/G12 (no clip arrows), M1/M2 (open-ended forms) · `evidence/inc004-mutations.txt` · restore digests there |

| Field | Value |
|---|---|
| **Mutation verdicts** | 15 of 15 KILLED (`evidence/inc004-mutations.txt`; specs `mutants_inc004.json` 13/13 + `mutants_inc004_r1.json` 2/2): G1–G2 paging, G3 hint not dim, G4–G5 urgency (late only; tie-break dropped), G6–G8 shading, G9 the prototype hex (256-colour law), G10 `<= 0` (the first-day boundary), G11–G12 clip arrows, G13 a second tag per cell (span-economy law), M1–M2 the open-ended forms (code review) |

### Instrument RED-proof — every instrument shown able to report FAILURE first

| Instrument | Known-bad input fed to it | The FAILURE it reported |
|---|---|---|
| `bg_columns` / `weekend_cells` (TC-211, AT-209) | G6/G7/G8 | missing columns per row |
| the hint check (TC-207, AT-205) | G1/G2/G3 | wrong rows, no hint, not dim |
| `gantt_plan` fold read-back (TC-209) | G4/G5 | A open / Ops folded |
| the 256-colour check | G9 (`#161d27`) | index 16 == 16 |

| Field | Value |
|---|---|
| **Instrument RED-proof** | 4 instruments, each shown failing before its PASS was believed |

### Emitted-form assertion — assert the bytes the producer EMITS (C-42)

| Artifact emitted | The assertion, run against the EMITTED form | What it returned |
|---|---|---|
| the gantt render | plain rows and per-span styles of `render_gantt`'s `Text` (background read off the span style) | TC nodes passed |
| the painted panel | Textual `#board` content spans (`rgb(26,29,34)` form accepted) | AT-205, AT-208, AT-209, AT-210 passed |

| Field | Value |
|---|---|
| **Emitted-form assertion** | 2 artifacts, each asserted in the form the producer emitted |

### Evidence files — bytes at a declared home, verbatim, hash-verified (C-59)

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| base collection error (declared) | `.dev-flow/2026-10-02-batch-02/evidence/inc004-red.txt` | `0f20c3037b29bff85dc9f634342ac80e60c154e96cfacbbcc35d38c6de9c4377` |
| mutation battery | `.dev-flow/2026-10-02-batch-02/evidence/inc004-mutations.txt` | `24bb29bb3b37189ab4fd78c020b379b44705c792b27067731a9c89fbe491c5ba` |
| mutant specs | `.dev-flow/2026-10-02-batch-02/evidence/mutants_inc004.json` | `b6fc38fdd2ce12079df294b3b74dd28fc3bf0ab9e24fc80a62f76cc4aac3c124` |
| mutant specs, review round | `.dev-flow/2026-10-02-batch-02/evidence/mutants_inc004_r1.json` | `0296b12bf2f3216c81af175ed43e4bf820a4abc1a663747a8d3627dadf9c06ec` |
| reverse census run | `.dev-flow/2026-10-02-batch-02/evidence/inc004-reverse-census.txt` | `fa8775a4bfc40c6fa6f33bdf9865068ab4dd2ba4847879cfc3ce024485f5a2bd` |
| gate run | `.dev-flow/2026-10-02-batch-02/evidence/inc004-green.txt` | `058c80323555fa8e7f62bea79804ccbf2aa8bd558d3e828d6522a2af1013b749` |
| gantt, 118×30 | `.dev-flow/2026-10-02-batch-02/evidence/captures/inc004-gantt-118x30.txt` | `388959930d05d501157e8b0337c565e1396c64792bdce42a672b271312c434d3` |
| gantt, 80×24 | `.dev-flow/2026-10-02-batch-02/evidence/captures/inc004-gantt-80x24.txt` | `325198f1b628925c4b8c8e8510d7fbbd04c10d6901451c9addd13c00823b3258` |
| gantt SVG, 118×30 | `.dev-flow/2026-10-02-batch-02/evidence/captures/inc004-gantt-118x30.svg` | `cadededcb778e753c286c9a30f8392d44dc7a566ecf38dedcc7c8e5a63489dc7` |

| Field | Value |
|---|---|
| **Evidence files** | 9 artifacts, each cited with its digest (SVG + text at both sizes) |

### Load-bearing emptiness — what is this resting on that is only true today? (C-55)

| Field | Value |
|---|---|
| Does any claim here rest on the tree holding NO instance of some case? | yes: "no non-weekend cell shaded"; "no row of the wrong width" |
| If the result is an ABSENCE, what made the search wide enough | every span and task row's field at 118×30 against independently recomputed weekend cells; k = 0.5, 1, 2; the reviewer's 5 boards × 5 widths × 6 heights for width |
| Guard labelled as protecting a CONCLUSION, not a behaviour | `assert len(spans) == 5 and len(body) >= 20` in TC-211 |
| Conjunctive criteria: one mutation per conjunct | G7 (body) and G8 (day row) separately |
| Synthetic instance of the absent case | G6–G8 |
| **Positive control for every probe that returned an ABSENCE** | the 22 expected weekend columns are found; the month row asserted empty |

### Reverse census — trigger family B

| Probe | Command | Result |
|---|---|---|
| B1 symbols asserted by **other** tests | full suite after the edit (`evidence/inc004-reverse-census.txt`: 2 failed / 1659 passed) + the targeted run (TC-106, the bar-hue law) | TC-106 (pages of 20) superseded by HLR-205 → rewritten in place (qa Q-14); `test_prism_laws::test_every_lit_field_cell_carries_a_declared_hue` and `test_span_economy::test_collapse_removes_the_redundant_runs` were REAL laws → fixed in the code (LED .18); `test_gantt.py::test_a_bar_never_wears_an_urgency_hue` was briefly relaxed and then REVERTED once the combined tag made it pass unchanged (the file equals HEAD) |
| B2 file moved on disk | none | did not fire |
| B3 byte-identical golden captures this source | none | did not fire |
| B4 artifact produced here is consumed elsewhere | `line_map` → `_scroll_selected_into_view`; `_gantt_frame` → `legend_entries` | the hint row has no `line_map` entry (AT-205); a paged frame leaves no legend row, as before (code review) |
| A3 | interface consumed by another module changed | `HEX` gains a key | no reader enumerates `HEX` except the palette census (green) |

| Field | Value |
|---|---|
| **Reverse census** | 5 probes: B1 fired (1 rewritten, 2 laws kept by fixing the code, 1 relaxation reverted), B4 fired, B2/B3/A3 did not fire |

### Correction population — enumerated BEFORE the first site was edited

| Correction | Population — the assertion category | Enumeration method (the command) | Count | Sites edited | Sites left, and why |
|---|---|---|---|---|---|
| field cells that may carry the weekend background | the markup producers of field cells | read of `_gantt_field` and `gantt_day_row` (the only two) | 2 | 2 | the month row (D-206), labels, chips, hint — never board text under a background |
| echo bracket sites | `ECHO_OPEN` / `ECHO_CLOSE` placements in `gantt_echo` | `grep -n "ECHO_OPEN\|ECHO_CLOSE" taskboard/views.py` | 4 | 4 | none |

| Field | Value |
|---|---|
| **Correction population** | 2 corrections, each enumerated before its first site was edited |

### Signed-balance test ledger

`post = base − deleted + added` → `1662 = 1643 − 0 + 19` ✓ (TC-106 rewritten in place, net 0).

## 4b · Independent review — the lens the author cannot be

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a named sub-agent with `agents/code-reviewer.md` (rev98 snapshot) · round 1 (the set moved mid-review — the two law fixes — and the reviewer re-based on the frozen tree): OK to advance, no HIGH; F1 MEDIUM (the open-ended echo forms untested — its M1/M2 survived), F2–F5 LOW (a test oracle wrong below a day per cell; other-side clips draw edge brackets — unreachable through the app, BACKLOG; requirement names; a stale docstring and long lines); paging, `line_map`, legend rows, width, markup through `collapse_runs`, and an extra urgency mutant (M3, killed) all checked · F1, F2, F4, F5 folded · round 2: OK to advance, M1/M2 killed by the new node alone, nothing open |

## 5 · Risks

- The weekend background is invisible on a 16-colour terminal (D-205, declared).
- `▲` reads as "late" elsewhere on the gantt; the hint row is dim and worded (D-213).

## 6 · Pending items / spec deviations

- Code review F3 (an echo clipped on the opposite side; `drawn` lacks "beyond" for rest-work echoes) → BACKLOG at close.

## 7 · Suggested next task

Increment 005 — the previous group sticky + the finish toast (HLR-206, HLR-207).

## Increment gate checklist

| # | Item | Owed in | ✓/⚠/✗ | Evidence (node id · command output · file:line) |
|---|---|---|---|---|
| 1 | ≤4 source files, or reason declared | all | ✓ | 1 / 4 |
| 2 | Tests written in this same increment | all | ✓ | 19 new nodes |
| 3 | Layer 0 written where the criterion applies | `core` · `full` | ✓ | `weekends()`, `gantt_echo`, `pressure` |
| 4 | **RED counterfactual** declared | `core` · `full` | ✓ | §4 |
| 5 | **Reverse census** declared | `core` · `full` | ✓ | §4 |
| 6 | `code-reviewer` passed | `core` · `full` | ✓ | §4b (round 2) |
| 7 | No file from another lane touched | all | ✓ | one lane |
| 8 | Frozen interfaces untouched (or returned to the trunk) | all | ✓ | signatures unchanged in this increment |
| 9 | Coverage claims verified **on disk**, not from intent | all | ✓ | ids in docstrings |
| 10 | Load-bearing emptiness declared, with its synthetic instance (C-55) | all | ✓ | §4 |
| 11 | **Mutation verdicts** declared | all | ✓ | §4 |
| 12 | **Instrument RED-proof** declared | all | ✓ | §4 |
| 13 | **Correction population** declared | all | ✓ | §4 |
| 14 | **Emitted-form assertion** declared | all | ✓ | §4 |
| 15 | **Independent review** names somebody | all | ✓ | §4b |
| 16 | **Evidence files** declared | all | ✓ | §4 |
