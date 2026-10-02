# Increment 001 — HLR-201, HLR-203 · the colour budget on the seven views, Setup's styles, soon and the packet

> Review packet (flow `templates/increment-template.md`; reserved field names kept literal).
> Lives in the repo next to the diff it describes. Mode `core`, language `en`.

| Field | Value |
|---|---|
| Batch | `2026-10-02-batch-02` |
| Increment | `001` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | HLR-201 (LLR-201.1, LLR-201.2, LLR-201.3), HLR-203 (LLR-203.1) |
| Acceptance | AT-201, AT-203 · white-box TC-201, TC-202, TC-205, TC-213 |
| Agent | `software-dev` (this runtime's implementing agent) |
| Date | `2026-10-02` |

---

## 1 · What changed

**Teal now means a focus role on every view.** The seven views batch-01 left (lanes, agenda,
focus, flow, standup, people, Setup) draw their titles bold bright, and their non-focus marks
leave the accent: the in-progress `◐` is `hd`, URL marks `mut`, the operator spine `bright`,
the throughput bar `hd`, the team filter's chosen segment bold bright, Setup's sections and hint
keys bold bright and its passing check `done`. Today's marks, the `/` filter, the Focus review
rail's `▸` and Setup's `>` cursor keep the accent. **Setup's rows are painted with their styles
again**: they were built from `str()` of styled Text, so the cursor, the on/off chips and the
checks were plain (P2 UX-1); a new `_fit_text` fits styled Text exactly as `fit` fits plain text
(189 renders of every view: 0 plain-text differences). **Soon-due tokens (+1..+7 days) are amber;
the gantt's moving packet is `mut`.** Code review folded: a long folder and project name are cut
in their columns with their styles; a colour `team.json` spells wrong is drawn `mut` instead of
crashing Textual (a regression this diff exposed, F9); `census()` returns a deep copy.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/views.py` | source | LLR-201.1, LLR-201.2, LLR-201.3, LLR-203.1 | titles, `header` default tone, non-focus re-tones, legend swatches, Setup rows via `_fit_text`, Setup colour guard, `reldue_token` soon, packet `mut` |
| `tests/test_colour_budget_app.py` | test | HLR-201, HLR-203, LLR-201.1, LLR-201.2, LLR-201.3, LLR-203.1 | NEW: AT-201, AT-203, TC-201 ×2 (sizes), TC-202 ×4, TC-205 ×2, TC-213 ×9 (2 on/off, 4 cursor sections, long value, passing check, bad colour) — 19 nodes (corrected at P4, qa G-004) |
| `tests/kg_board.py` | fixture | HLR-201 | NEW `TEAM`, `SETUP`, `census()` (URL cards, pinned tasks, history, team dir, Setup state) |
| `tests/test_cells.py` | test | HLR-203 | reverse census: +4d is `soon` (rewritten in place) |
| `tests/test_colour_budget.py` | test | HLR-203 | reverse census: +4d is `soon` (rewritten in place) |
| `tests/test_team_views.py` | test | HLR-201 | reverse census: the chosen segment is bold bright, never accent, and it is `equipo` |

| Count | Value |
|---|---|
| **SOURCE files** | **1 / 4** |
| Test files | 5 (uncapped) |
| Doc files | 0 |

## 3 · How to test

```bash
python -m pytest -q tests/test_colour_budget_app.py tests/test_team_views.py tests/test_colour_budget.py
python -m pytest -q
```

## 4 · Test results

| Layer | Owed in | Nodes | Result |
|---|---|---|---|
| **0 · unit** | `core` · `full` | TC-213 long value (`_fit_text`'s cut), TC-205 token boundaries | 2 passed |
| **A · white-box** `TC-NNN` ↔ LLR | `core` · `full` | TC-201 ×2, TC-202 ×3, TC-205 ×2, TC-213 ×6 | 13 passed |
| **B · black-box** `AT-NNN` ↔ story, through the shipped surface | `core` · `full` | AT-201, AT-203 | 2 passed |

Gate run on the frozen round-2 tree: `python -m pytest -q -p no:cacheprovider` → **1630 passed in
173.42s, exit 0** (`evidence/inc001-green.txt`).

### RED counterfactual — executed, not predicted

| Field | Value |
|---|---|
| Mutation applied | the base tree (`git archive HEAD`) with the new tests overlaid; then 21 mutants on the increment tree |
| Where it ran | scratch exports, never the live checkout |
| Transcript | `evidence/inc001-red-on-base.txt` (12 failed, 1 passed — the census-set guard, green by design); `evidence/inc001-mutations.txt` |
| Restore proven by | the battery's per-mutant sha256 check (`views.py` restored to `010991ae17a762a5…`) |
| Bytecode cache | `-B`, `-p no:cacheprovider` |
| Arms resolved at baseline | 13 on base (the round-1 nodes RED through their mutants) |
| Verdict granularity | per node (`-rA`) |
| Arms that stayed GREEN | `test_TC_202_the_census_set_is_complete` on base (a guard of the input set, not of the change) |

| Field | Value |
|---|---|
| **RED counterfactual** | the 12 behaviour nodes on the base tree, all RED for the specified reason (lanes title `bold #2dd4bf`; `◆ TASKBOARD` off-role; Setup's cursor unpainted; throughput swatch accent; `+1d` `mut`; packet `#e6edf7`) · `evidence/inc001-red-on-base.txt` · the round-1/2 nodes RED by mutants X12, X13, X17, F9, F2, M9b · restore digests in `evidence/inc001-mutations.txt` |

| Field | Value |
|---|---|
| **Mutation verdicts** | 21 of 21 KILLED (`evidence/inc001-mutations.txt`, harness `evidence/mutate.py`, specs `mutants_inc001.json` + `mutants_inc001_r1.json`, run on the round-2 tree): M1–M15 each site back to the accent / the packet bright / the token grey / `< 7` / `str()` rows / chip not distinct / legend swatch accent; X12 no `…`, X13 cut one cell wide, X17 chrome always `todo`, F9 colour guard reverted, F2 `str()` rows against the every-section node alone, M9b passing check `mut` against the restored node alone |

### Instrument RED-proof — every instrument shown able to report FAILURE first

| Instrument | Known-bad input fed to it | The FAILURE it reported |
|---|---|---|
| `off_role` (positional focus-role detector) | a forged second accent `╎` column appended to a lanes render | the extra column reported (`test_TC_202_the_census_can_see_the_accent`) |
| `accent_cells` | the base tree | `◆ TASKBOARD` reported off-role (`inc001-red-on-base.txt`) |
| `styled_columns` | the base Setup rows | False on every row (mutant F2 KILLED) |
| the Static paint in the bad-colour node | the pre-fix colour code | `MissingStyle` (mutant F9 KILLED) |

| Field | Value |
|---|---|
| **Instrument RED-proof** | 4 instruments, each shown failing before its PASS was believed |

### Emitted-form assertion — assert the bytes the producer EMITS (C-42)

| Artifact emitted | The assertion, run against the EMITTED form | What it returned |
|---|---|---|
| every view's rendered `Text` | spans' styles and the plain text at each span's offsets | 13 TC nodes passed |
| the painted board panel in the running app | `#board` `render()` spans (Textual's `rgb(…)` form accepted) | AT-201, AT-203 passed |
| the Setup render painted by Textual | a `Static` painting it in `run_test` | passed (RED before the F9 guard) |

| Field | Value |
|---|---|
| **Emitted-form assertion** | 3 artifacts, each asserted in the form the producer emitted |

### Evidence files — bytes at a declared home, verbatim, hash-verified (C-59)

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| RED on base | `.dev-flow/2026-10-02-batch-02/evidence/inc001-red-on-base.txt` | `059b4c49bc6e3f829fdb63d88606404acd1127f9507a6a5e11d74bb65e372a6b` |
| mutation battery | `.dev-flow/2026-10-02-batch-02/evidence/inc001-mutations.txt` | `00c0cfb21fd8b2b055b9d49d184ff7bdeba360e24615bd279e62c3b94b5dc73b` |
| battery harness | `.dev-flow/2026-10-02-batch-02/evidence/mutate.py` | `6571ff2deec5d373d166e9ce3c6c92a40915e42121e258f8fcc71e9434270dec` |
| mutant specs | `.dev-flow/2026-10-02-batch-02/evidence/mutants_inc001.json` | `ee3983f65790fab08bdd54da08a620c71cb579804d0f8e500976f344b28ba437` |
| mutant specs, review rounds | `.dev-flow/2026-10-02-batch-02/evidence/mutants_inc001_r1.json` | `701c70119842d67cd953484b9c96beb7ee3def49a095ec250d75c77e217dff9a` |
| plain-text invariance | `.dev-flow/2026-10-02-batch-02/evidence/inc001-plain-diff.txt` | `b1b3cc71835501007e9a7741c7cc9093e9e60da3048a212599e4e3a2647316ad` |
| reverse census run | `.dev-flow/2026-10-02-batch-02/evidence/inc001-reverse-census.txt` | `ae0a06fcf30f34779f23ae9d7265ef1e7074503e9e632e8fd92adfe536b99fb0` |
| gate run | `.dev-flow/2026-10-02-batch-02/evidence/inc001-green.txt` | `e67274e7d42fb4dd9155d1fb61c7b8b29e2ddbdfc17ea430ace77db62b8ef05b` |
| Setup at 118×30 | `.dev-flow/2026-10-02-batch-02/evidence/captures/inc001-setup-118x30.txt` | `c08c5d0e4760be21f10ef0322be825d7bb35b4a8fade137a4f68e9182b5e2c47` |
| Setup at 80×24 | `.dev-flow/2026-10-02-batch-02/evidence/captures/inc001-setup-80x24.txt` | `4a381278520e6c74c66483f6f2fca613373c8aa1ea7941f45c30bd809d1ee22b` |
| standup at 118×30 | `.dev-flow/2026-10-02-batch-02/evidence/captures/inc001-standup-118x30.txt` | `946e9f9c481e631163b8290d9ef84dc186e6adc148434bbd9b1cf1649534ebf7` |
| agenda at 118×30 | `.dev-flow/2026-10-02-batch-02/evidence/captures/inc001-agenda-118x30.txt` | `1ac3dc850f48a06fc698fcdfe398e6c933fa1ab8e80d769226ccbef644c80334` |

| Field | Value |
|---|---|
| **Evidence files** | 12 artifacts under the declared home, each cited with the digest of its stored bytes; every changed view also captured as SVG + text at 118×30 and 80×24 (`captures/inc001-*`, base in `captures/base-*`) |

### Load-bearing emptiness — what is this resting on that is only true today? (C-55)

| Field | Value |
|---|---|
| Does any claim here rest on the tree holding NO instance of some case? | yes: "no accent run outside a focus role" over 16 view × presentation pairs × 3 sizes |
| If the result is an ABSENCE, what made the search wide enough | the pair set derived from `VIEW_ORDER` and the tuples parsed from `app.py`, guarded `== 16`; a board with URL cards, pinned tasks, history, team mode, a task due today |
| Guard labelled as protecting a CONCLUSION, not a behaviour | `test_TC_202_the_census_set_is_complete` |
| Conjunctive criteria: one mutation per conjunct | one mutant per re-toned site (M1–M15) |
| Synthetic instance of the absent case | the forged accent column; every mutant |
| **Positive control for every probe that returned an ABSENCE** | the census finds today's rule, the filter field and Setup's `>` (`test_TC_202_the_census_can_see_the_accent`) |

### Reverse census — trigger family B

| Probe | Command | Result |
|---|---|---|
| B1 symbols asserted by **other** tests | full suite after the edit (`evidence/inc001-reverse-census.txt`: 3 failed / 1621 passed) | 3 nodes pin superseded tones: `test_cells.py::test_card_cell_shows_the_deadline_countdown_on_every_dated_card` (+4d `mut` → `soon`, HLR-203), `test_colour_budget.py::test_TC_119_the_shared_card_tokens_left_the_accent_everywhere` (same), `test_team_views.py::test_team_filter_chrome_highlights_active_segment` (accent chip → bold bright, HLR-201) — each rewritten in place, its law kept |
| B2 file moved on disk | none | did not fire |
| B3 byte-identical golden captures this source | `ls tests/goldens` | did not fire |
| B4 artifact produced here is consumed elsewhere | the rendered views → the app's `#board`; `legend_entries` → `HelpModal` | AT-201 reads the painted panel; the legend node checks the swatches |
| A3 | interface consumed by another module changed | `header`'s default tone (all callers in `views.py`) | no signature change |

| Field | Value |
|---|---|
| **Reverse census** | 5 probes: B1 fired (3 nodes rewritten in place), B4 fired (AT-201, legend node), B2/B3/A3 did not fire |

### Correction population — enumerated BEFORE the first site was edited

| Correction | Population — the assertion category | Enumeration method (the command) | Count | Sites edited | Sites left, and why |
|---|---|---|---|---|---|
| non-focus accent | every `"accent"` / `HEX["accent"]` site in `views.py` | `grep -n '"accent"\|HEX\[.accent.\]' taskboard/views.py` + the P-1 rendered census | 59 sites | 33 | 26 kept: today marks, the `/` filter, the `▸`/`>` cursors, `HEX`'s own key, the dead `HEAT` table (BACKLOG) — classified one by one, confirmed by code review |
| styles lost to `str()` | `str(` over a styled `Text` in `render_setup` | read of `render_setup.row` | 3 | 3 | none |

| Field | Value |
|---|---|
| **Correction population** | 2 corrections, each enumerated before its first site was edited |

### Signed-balance test ledger

`post = base − deleted + added` → `1630 = 1611 − 0 + 19` ✓ (the 3 reverse-census rewrites are in place, net 0).

## 4b · Independent review — the lens the author cannot be

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a named sub-agent with `agents/code-reviewer.md` · round 1: OK to advance, 0 HIGH, 3 MEDIUM (F1 `_fit_text`'s cut untested, F2 the span arm vacuous on base, F3 sections not covered) and 6 LOW (F4 which segment, F5 selection-less renders, F6 AT arm, F7/F8 docstrings, F9 a bad `team.json` colour crashes Textual) — its own 17-mutant battery (14 killed, X12/X13/X17 survived) · all folded · round 2: `BLOCK-UNTIL: R2-F1` (HIGH: the F9 splice deleted the passing-check node; mutant M9b survived) · folded (node restored, battery re-run on that tree) · round 3: OK to advance, R2-F1 discharged by re-reading the file and re-running M9b, nothing open |

## 5 · Risks

- The provisional visual decisions (D-208 chips bold/mut, D-211 to come) ship before the operator's verdict on captures (D-216).
- Rich tolerates an unknown style and Textual does not: any styled Text built from file data must stay on known colours (F9 fixed for Setup; other sites already map through `HEX`).

## 6 · Pending items / spec deviations

- `HEAT` (dead `week ▒ accent` table) → BACKLOG at close. Unifying the word `today`'s tone across views → BACKLOG (D-209).

## 7 · Suggested next task

Increment 002 — the chrome: key bar, ribbon, modal titles, help key map (HLR-202).

## Increment gate checklist

| # | Item | Owed in | ✓/⚠/✗ | Evidence (node id · command output · file:line) |
|---|---|---|---|---|
| 1 | ≤4 source files, or reason declared | all | ✓ | 1 / 4 |
| 2 | Tests written in this same increment | all | ✓ | 19 new nodes |
| 3 | Layer 0 written where the criterion applies | `core` · `full` | ✓ | `_fit_text` (2 paths): TC-213 long value; `reldue_token` boundaries |
| 4 | **RED counterfactual** declared | `core` · `full` | ✓ | §4 |
| 5 | **Reverse census** declared | `core` · `full` | ✓ | §4 |
| 6 | `code-reviewer` passed | `core` · `full` | ✓ | §4b (round 3) |
| 7 | No file from another lane touched | all | ✓ | one lane |
| 8 | Frozen interfaces untouched (or returned to the trunk) | all | ✓ | no signature changed |
| 9 | Coverage claims verified **on disk**, not from intent | all | ✓ | ids in docstrings; 19 nodes collected |
| 10 | Load-bearing emptiness declared, with its synthetic instance (C-55) | all | ✓ | §4 |
| 11 | **Mutation verdicts** declared | all | ✓ | §4 |
| 12 | **Instrument RED-proof** declared | all | ✓ | §4 |
| 13 | **Correction population** declared | all | ✓ | §4 |
| 14 | **Emitted-form assertion** declared | all | ✓ | §4 |
| 15 | **Independent review** names somebody | all | ✓ | §4b |
| 16 | **Evidence files** declared | all | ✓ | §4 |
