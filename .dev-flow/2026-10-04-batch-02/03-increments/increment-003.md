# Increment 003 — HLR-603 (LLR-603.1, LLR-603.2) · the kanban carries milestones on the band rule, never as cards

> **Where this lives:** the repo, next to the diff — `.dev-flow/2026-10-04-batch-02/03-increments/increment-003.md`.
> Template `templates/increment-template.md` (rev100); notice convention `⚠` notice · `✗` block · `✓` with evidence.

| Field | Value |
|---|---|
| Batch | `2026-10-04-batch-02` |
| Increment | `003` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | HLR-603; LLR-603.1, LLR-603.2 (amended LED .7, .8); D-607, D-614, D-619, D-622, D-623 |
| Acceptance | AT-603 · white-box TC-612, TC-613 |
| Agent | `software-dev` (this runtime) |
| Date | `2026-10-04` |

---

## 1 · What changed

**A milestone is never a kanban card (M-2).** One seat, `kanban_work`, drops milestones from what
every presentation lays out — grouped, matrix, lanes — and from the nav, the header's `N tasks`, the
column counts and WIP tags, the bands' `N open`/`N high ↑`, the fold row and the `/` filter's
`N/M tasks`. A milestone left selected (from the gantt, or by `M` on a card) moves to the first card
of the nearest drawn column at or left of its phase. In the grouped presentation with the project
grouping, each project's band rule carries its milestones after its facts — late ones first in the
over tone, then the upcoming ones by date in the project hue, then the most recently reached one with
`✓` in ash — laid out by the prototype's ladder at the room the rule leaves (titles of ≥ 8 cells cut
before they drop, then dates only, then `── +N ◆`), and `+N ◆` alone when not one date fits (D-619).
One seat, `band_rule_facts`, builds a rule's facts for both the renderer and the `?` legend, which
names `◆` exactly when a rule draws one; the kanban help says what `◆` on a rule is.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/views.py` | source | LLR-603.1, LLR-603.2 | `kanban_work` and its readers (`kanban_plan`, `_kanban_matrix`, `_kanban_lanes`, `nav_model` kanban, `render_view`'s kanban counts); `band_milestones`, `band_milestone_facts`, `band_rule_facts`; `_kanban_grouped`; `legend_entries("kanban")` (takes presentation, grouping, focus); `help_usage("kanban")` |
| `taskboard/app.py` | source | LLR-603.1, LLR-603.2 | `_select_first`: a kanban milestone selection → the nearest drawn column; `action_legend` passes the kanban's presentation, grouping and focus |
| `taskboard/modals.py` | source | LLR-603.2 | `HelpModal` forwards the kanban's presentation, grouping and focus to `legend_entries` |
| `README.md` | doc | | the kanban paragraph of the Milestones section |
| `tests/test_kanban_milestones.py` | test | HLR-603, LLR-603.1, LLR-603.2 | NEW: TC-612, TC-613, AT-603 (71 nodes) |

| Count | Value |
|---|---|
| **SOURCE files** | **3 / 4** |
| Test files | 1 (uncapped) |
| Doc files | 1 (outside the count) |

## 3 · How to test

```bash
python -m pytest -q -p no:cacheprovider tests/test_kanban_milestones.py
python -m pytest -q -p no:cacheprovider tests/test_kanban_readable.py tests/test_kanban_priority.py tests/test_legend.py tests/test_links.py
python -m pytest -q -p no:cacheprovider          # the gate
```

## 4 · Test results

| Layer | Owed in | Nodes | Result |
|---|---|---|---|
| **0 · unit** | `core` · `full` | TC-613 layout (21 rooms), order (5 + mixed kinds), tones | passed |
| **A · white-box** `TC-NNN` ↔ LLR | `core` · `full` | TC-612 (27 modes + counts, filter, selection ×4, derived set), TC-613 (help, legend ×4, done band, S1, grouping) | passed |
| **B · black-box** `AT-NNN` ↔ story | `core` · `full` | AT-603 | passed |

Gate run on frozen r2: `python -m pytest -q -p no:cacheprovider` → **2446 passed, 1 failed** in 462.08 s — the one failure is `test_win_clipboard_roundtrip`, the known environmental clipboard flake (G-011) (`.dev-flow/2026-10-04-batch-02/evidence/inc003-gate-r2.txt`). r1 (superseded by the K folds): 2440 passed, 1 failed (the same flake) (`inc003-gate-r1.txt`). The larger failure counts in the cited evidence come from the deliberately failing transcripts (the batteries and the RED captures), never from a gate run.

### RED counterfactual — executed, not predicted

| Field | Value |
|---|---|
| **RED counterfactual** | the increment-003 tests on the increment-002 tree (this increment's hunks inverse-applied from its own edit script), the two new helpers stubbed to raise and `kanban_work` restated as the oracle's rule: 62 of 64 arms RED (`evidence/inc003-red-on-inc002.txt`); the 2 GREEN arms are labelled pins: the derived-presentation-set guard (C-31) and "priority grouping carries no milestone" (base draws none). The K folds RED-first on the r1 product restored byte-exact (`inc003-k-red.txt`: 5 of 6 RED; the help arm is a deletion pin) |

| Field | Value |
|---|---|
| **Mutation verdicts** | **19 of 19 KILLED** (`evidence/inc003-mutations-r3.txt`, spec `mutants_inc003_r3.json`; r1/r2 specs built by `mk_mutants_inc003.py`), per resolved node, every restore hash OK: K1 `kanban_work` filters nothing · K2 the grouped plan · K3 the matrix · K4 the lanes · K5 the nav · K6 the filter counts · K7 late after upcoming · K8 every reached listed · K9 reached counted in `+N` · K10 no `+N ◆` fallback · K11 the rule carries nothing · K12 the selection jumps to the first task · K13 the farthest column · K14 today not soon · K15 an upcoming `◆` in over · K16 titles cut below 8 · KL1 the legend blind to presentation/grouping · KL2 the help bullet deleted · KL3 the legend keyed on an open card. r1: K7, K8 SURVIVED (`inc003-mutations.txt`: no fixture project held a late AND an upcoming milestone, or two reached — an input-set gap, C-31) → a synthetic mixed-kinds arm; r2 16/16 (`inc003-mutations-r2.txt`) |

### Instrument RED-proof

| Field | Value |
|---|---|
| **Instrument RED-proof** | 2 instruments: the battery reported `SURVIVED` for K7/K8 at r1 before the input set was widened; the C-31 guard on the derived presentation set (`_presentations()` parses `render_kanban`) asserts `{grouped, matrix, lanes}` ⊆ the derived set |

### Emitted-form assertion (C-42)

| Field | Value |
|---|---|
| **Emitted-form assertion** | 3 artifacts in their emitted form: the painted kanban (compositor strips, per-cell glyph and hex), the rendered frame (`render_kanban(...).plain`), the filter bar's row (`/ … N/M tasks · esc clears`) — asserting it exposed the contract's phantom `0 of 25` (LED .7) |

### Evidence files — bytes at a declared home, verbatim, hash-verified (C-59)

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| inc003-red-on-inc002.txt | .dev-flow/2026-10-04-batch-02/evidence/inc003-red-on-inc002.txt | f9173f1dca7add0626c7cb759461d2c75ee1550a1f583d0209690049ea580e55 |
| inc003-k-red.txt | .dev-flow/2026-10-04-batch-02/evidence/inc003-k-red.txt | e0a53369e4ac8068d28f9fd3f530e0a89c5803062b60ea59189647c5ff92a03b |
| inc003-mutations.txt | .dev-flow/2026-10-04-batch-02/evidence/inc003-mutations.txt | 67c7ab5f8e33bf6def3b467268974847f4f69966786fba10e354cb7ca753e9f1 |
| inc003-mutations-r2.txt | .dev-flow/2026-10-04-batch-02/evidence/inc003-mutations-r2.txt | 3183d05f3e194bbe44705f31b91b39929167134dced609a645241db16f30bbee |
| inc003-mutations-r3.txt | .dev-flow/2026-10-04-batch-02/evidence/inc003-mutations-r3.txt | 0afbc50f05c1ca09d9fd613b6a7f9b4ba3b98108bf08c0f112afa39eb6f78a2a |
| mutants_inc003.json | .dev-flow/2026-10-04-batch-02/evidence/mutants_inc003.json | 78be94b8a411d27131593650a8675e44c324339a24aa2a01aa88471c41db2d6b |
| mutants_inc003_r2.json | .dev-flow/2026-10-04-batch-02/evidence/mutants_inc003_r2.json | 45699dfb2731fd50059babd2068b5e8c26cb70527055bc78045030a33a65ef9c |
| mutants_inc003_r3.json | .dev-flow/2026-10-04-batch-02/evidence/mutants_inc003_r3.json | 86ef47c11de2627f37b685e1680aac4969dc5e31e5498d17f50fe10692d717b7 |
| mk_mutants_inc003.py | .dev-flow/2026-10-04-batch-02/evidence/mk_mutants_inc003.py | b13d5b99a55e578a31d965516037996cc5328fa5dc049d3746f5c8dbacddd26f |
| battery.py | .dev-flow/2026-10-04-batch-02/evidence/battery.py | a84222ed67665884e0a77f30fd6d4e91e9785cf4d57030fb006fc8ccc42491cb |
| make_export.sh | .dev-flow/2026-10-04-batch-02/evidence/make_export.sh | 2de30a0c31d7a484499ad4226cf49417f619ccf616a3978dcbbcb4c32d1fe57a |
| p1-thresholds.txt | .dev-flow/2026-10-04-batch-02/evidence/p1-thresholds.txt | 50d0b9e83ebf3331b4678d28b8827c0d735a52ccec3c49bc9ddbce862d9dbca3 |
| p1-thresholds-shipped.txt | .dev-flow/2026-10-04-batch-02/evidence/p1-thresholds-shipped.txt | 2d062c01c89a0cdee0a21a8ea3cbe22d5a3d9e4de0f4e3744cc9b6ac820a55ce |
| inc003-frozen-r1.sha256 | .dev-flow/2026-10-04-batch-02/evidence/inc003-frozen-r1.sha256 | 6f0438e994410df06c1e2b591db22e8c2aede812b0a7e3232bd428b2d4f603d2 |
| inc003-frozen-r2.sha256 | .dev-flow/2026-10-04-batch-02/evidence/inc003-frozen-r2.sha256 | 13ad63459c7ee377c3eed74dd4869f00c60fe2074875cf922f83dda4316dc6d8 |
| inc003-gate-r1.txt | .dev-flow/2026-10-04-batch-02/evidence/inc003-gate-r1.txt | 2c840cce9451549f14fa3bb3e993704576843dca016c0b6746aeb66beaeb91e5 |
| inc003-gate-r2.txt | .dev-flow/2026-10-04-batch-02/evidence/inc003-gate-r2.txt | ab40c78aaf7c05054fe31586ec58a757df52ef30bb1db9a4bbd10a0e7367b7aa |

| Field | Value |
|---|---|
| **Evidence files** | 17 artifacts at `artifact_homes.evidence`, cited with the digests of their stored bytes (home paths redacted before hashing) |

### Load-bearing emptiness (C-55)

| Field | Value |
|---|---|
| Does any claim here rest on the tree holding NO instance of some case? | yes: "no presentation lays out a milestone" — over the three presentations `render_kanban` branches on |
| If the result is an ABSENCE, what made the search wide enough | the presentation set is DERIVED from `render_kanban`'s source (C-31) and guarded non-shrinking; 27 mode combinations swept |
| Synthetic instance of the absent case | the mixed-kinds project (late + upcoming + two reached) for K7/K8 |
| **Positive control for every probe that returned an ABSENCE** | K2, K3, K4, K5 each reintroduce a milestone into one presentation and are KILLED |

### Reverse census — trigger family B

| Field | Value |
|---|---|
| **Reverse census** | 4 probes. B1 `grep -rln "kanban_plan\|kanban_order\|_band_facts\|_band_rule\|_kanban_matrix\|_kanban_lanes\|nav_model\|legend_entries\|help_usage\|HelpModal\|_select_first\|tasks ·\|N tasks" tests/` → `test_kanban_readable.py`, `test_kanban_priority.py`, `test_app.py`, `test_legend.py`, `test_english.py`, `test_dependencies.py`, `test_links.py`, `test_lanes_grid.py`, `test_focus.py`, `test_markup_census.py`, `test_colour_budget_app.py`, `test_archive.py`, `test_team_views.py` — 508 passed before the K folds, 87 (kanban + legend) after; no node changed. B2 not fired. B3 not fired. A3: `legend_entries` and `HelpModal` gain defaulted keyword arguments (every existing caller unchanged) |

### Correction population

| Field | Value |
|---|---|
| **Correction population** | 2 corrections: (1) the filter literal `0 of 25` → `0/25 tasks` (LED .7) — population `grep -rn "of 25\|N of M" .dev-flow/2026-10-04-batch-02/01-requirements.md tests/`: HLR-603, LLR-603.1 and the TC-612 arm — all edited; (2) "a project whose only open items are milestones draws no band" → "no card, open or done" (LED .8) — population `grep -rn "only open items" .dev-flow/2026-10-04-batch-02/`: HLR-603, D-623 — both edited (PLAN.md's PV-605 says "a band with no card", unchanged) |

### Signed-balance test ledger

`post = base − deleted + added` → `2447 = 2376 − 0 + 71` ✓ (71 new nodes in `test_kanban_milestones.py`).

---

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a named agent with `agents/code-reviewer.md` · OK-WITH-NOTES at r2, 0 HIGH. r1 OK-WITH-NOTES: K-1 MEDIUM (product: the `?` legend's `◆` entry keyed on a different rule from the drawing — a ghost in matrix/lanes/other groupings, silent for a done-cards band) folded with the one seat `band_rule_facts` and the D-623 wording (LED .8); K-2 MEDIUM (tests: no node pinned the help and legend; its deletion mutant survived) folded as TC-613 arms, KL1–KL3 KILLED; K-3 LOW folded. r2: K-1..K-3 DISCHARGED; K2-1 LOW (product, pre-existing pattern: the kanban legend reads the unfiltered board under `/`, and counts bands folded off screen) — routed to BACKLOG, not folded |

---

## 5 · Risks

- After `M` in the kanban the cursor may jump to another band's card (the nearest column's first card; PV-611).
- A project whose only open items are milestones and that has no done card draws no band: its milestones are not in the kanban (D-623; BACKLOG for a rule-only band).
- At a 118×30 terminal the high band can push a late milestone's band below the fold (PV-605, ux UX2-2; BACKLOG).

## 6 · Pending items / spec deviations

- LED .7 (the filter literal), LED .8 (D-623 wording; the legend's seat).
- Code review K2-1 (LOW): the kanban `?` legend reads the unfiltered board and counts bands folded off screen — BACKLOG.

## 7 · Suggested next task

Increment 004 — the one-time offer (US-605).

---

## Increment gate checklist

| # | Item | Owed in | ✓/⚠/✗ | Evidence |
|---|---|---|---|---|
| 1 | ≤4 source files | all | ✓ | 3 / 4 |
| 2 | Tests written in this same increment | all | ✓ | `tests/test_kanban_milestones.py` (71) |
| 3 | Layer 0 where the criterion applies | `core` · `full` | ✓ | `band_milestone_facts` (ladder, 4 exits), `band_milestones`: TC-613 |
| 4 | **RED counterfactual** | `core` · `full` | ✓ | §4 |
| 5 | **Reverse census** | `core` · `full` | ✓ | §4 |
| 6 | `code-reviewer` passed | `core` · `full` | ✓ | §4b |
| 7 | No file from another lane touched | all | ✓ | one lane |
| 8 | Frozen interfaces untouched | all | ✓ | none declared |
| 9 | Coverage claims verified on disk | all | ✓ | `pytest --collect-only tests/test_kanban_milestones.py` → 71 |
| 10 | Load-bearing emptiness declared | all | ✓ | §4 |
| 11 | **Mutation verdicts** | all | ✓ | 19/19 |
| 12 | **Instrument RED-proof** | all | ✓ | §4 |
| 13 | **Correction population** | all | ✓ | §4 |
| 14 | **Emitted-form assertion** | all | ✓ | §4 |
| 15 | **Independent review** names somebody | all | ✓ | §4b |
| 16 | **Evidence files** | all | ✓ | §4 |
