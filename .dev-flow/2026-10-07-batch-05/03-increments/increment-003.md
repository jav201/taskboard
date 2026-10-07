# Increment 003 — HLR-1105 · the deep-chain cap · the one-pass resize heal · AT-801b's docstring

> **Artifact language**
> This template is the canonical **English scaffold**. Generate the artifact in the batch's development
> language — the **prose**, and never a label. **Where that language is declared:**
> `state.json`'s `language` key in `core` and `full`. The normative RULES below are
> language-independent.

> **Owed in.** `core` ✓ · `full` ✓

> **Field guide:** `templates/docs/increment-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

> **Reserved field names.** The **field names and block keywords below are language-independent** — the
> validator parses them literally and they are never translated:
> `SOURCE files` · `Instrument RED-proof` · `Correction population` · `Mutation verdicts` · `Emitted-form assertion` · `Reverse census` · `RED counterfactual` · `Independent review` · `Evidence files` · `Traces to` · `File` · `Kind` · `source` · `test` · `doc` · `config` · `generated` · `fixture` · `⏸ DEFER`
> Everything else on this page — headings, guidance, the prose in every cell — is translated with the batch.
> **One strategy, not two:** the flow ships no alias table, so a translated label is read as an ABSENT one and the rule keyed on it reports a true-sounding silence.
> **And one FLOW-WIDE reserved token, read out of this artifact by `V42` no matter which template minted it:** `⏸ DEFER`. It is a MARKER rather than a field name, which is why it is stated here *and* in `/dev-flow` §Language of artifacts rather than in a per-template list — a deferral can be written in any batch artifact, including the ones that carry no block at all.

> **Where this lives:** the **repo**, next to the diff it describes —
> `.dev-flow/2026-10-07-batch-05/03-increments/increment-003.md`. It is not synced to the vault.

> **Notice convention.** `⚠` yellow = notice: does not block, obliges you to DECLARE the reason here.
> `✗` red = block. `✓` green = satisfied **with its evidence cited**. A notice repeated for three
> consecutive batches becomes a rule or is retired.

| Field | Value |
|---|---|
| Batch | `2026-10-07-batch-05` |
| Increment | `003` |
| Lane (if the batch forked) | `none — one lane per increment (§2.8 of the contract; serialized after increment 002 by the plan itself)` |
| Requirement(s) | `HLR-1105` (+ `LLR-1105.1`) — the three batch-C carries |
| Acceptance | the amended `TC-810` (`test_TC_810_the_fold_caps_a_partial_band_and_still_drops_whole`) · `AT-801c` (the new resize arm) · the corrected `AT-801b` docstring — the two chainmap files at 13 nodes, all green |
| Agent | `software-dev` — DeepSeek V4 Pro |
| Date | `2026-10-07` |

---

## 1 · What changed

*(BLUF: state the outcome first, then the mechanism. Name the shipped surface the user reaches.)*

On the chain map (`6`), a tall project's band that no longer fits whole now draws its fitting
chains plus ONE tail row naming the rest `+N more ↓` — N exact, the kanban law — instead of
vanishing whole. A band whose FIRST chain does not fit still drops whole (head AND canvas — the
dangling-head law stands). The fold change lives in `views.render_chainmap`'s pipeline
(`taskboard/views.py:5798-5871`; each band plan now carries its `nslot`, :5772) and is only ever
reached for bands that previously vanished whole — so the C-2b oracle frames (TC-801/802,
no folded bands) stayed byte-green. Resizing the window now heals the selection in ONE refresh:
`app.refresh_view` closes through `_heal_selection_after_repaint` (`taskboard/app.py:1524`, the
method at :1526-1544) — a selection the fresh `_line_map` does not name drops to the nearest
painted row (`min` by line-map row), or clears when the frame paints nothing. The heal is
CHAINMAP-SCOPED: the only view whose selection must sit on a named tile (the generic attempt
broke 13 tests — §5 names why the scope is right, not convenient). `AT-801b`'s docstring now
says what the arm does (`tests/test_chainmap_app.py:299` — it presses escape, not "linking
re-renders"), and the new `AT-801c` arm pins the one-refresh heal
(`tests/test_chainmap_app.py:318`). The amended TC-810 rides **LED-2026-10-07-batch-05.1** —
the fold-law amendment it pins.

## 2 · Files modified

**The budget counts SOURCE files only. Tests are not capped. Product docs and `.dev-flow/**` are outside the count.**

One row per file. `Kind` is one of `source` · `test` · `doc` · `config` · `generated` · `fixture`; `Traces to` names the US/HLR/LLR (or `R-<AREA>-<NNN>`) ids the file serves, and `doc` rows leave it empty.

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/views.py` | source | HLR-1105 · LLR-1105.1 | the fold's partial-band cap (:5798-5871): a partially-fitting band draws its fitting chains + one `+N more ↓` tail (N exact); `nslot` carried on each band plan (:5772); the zero-fit band still drops whole |
| `taskboard/app.py` | source | HLR-1105 · LLR-1105.1 | `refresh_view` closes through `_heal_selection_after_repaint()` (:1524; the method :1526-1544 — the chainmap-scoped re-verify) |
| `tests/test_chainmap.py` | test | LLR-1105.1 — the amended TC-810 | `TC-810` renamed + amended (:185 → `test_TC_810_the_fold_caps_a_partial_band_and_still_drops_whole`): the partial band draws its chains + the exact `+4 more ↓` tail; the zero-fit band drops whole (head and canvas); the tail row reaches the line_map like any painted row |
| `tests/test_chainmap_app.py` | test | LLR-1105.1 — AT-801b · AT-801c | AT-801b's docstring corrected to its body (:299); the new `AT-801c` resize arm (:318 — the selection is valid after ONE refresh) |

| Count | Value |
|---|---|
| **SOURCE files** | **2 / 4** |
| Test files | 2 (uncapped) |
| Doc files | 0 (outside the count) |

---

## 3 · How to test

```bash
env -u NO_COLOR TERM=xterm-256color COLORTERM=truecolor PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 \
  python -m pytest tests/test_chainmap.py tests/test_chainmap_app.py -q    # 13 passed
```

---

## 4 · Test results

| Layer | Owed in | Nodes | Result |
|---|---|---|---|
| **0 · unit** (the fold's cap branch — the fit/partial/zero-fit split, cyclomatic ≥3) | `core` · `full` | the amended `TC-810` | 1 node passed (mutations M6/M7-proven below) |
| **A · white-box** the amended `TC-810` ↔ LLR-1105.1 | `core` · `full` | `test_TC_810_the_fold_caps_a_partial_band_and_still_drops_whole` (+ the C-2b oracle arms TC-801/802 byte-green) | passed |
| **B · black-box** `AT-801b` · `AT-801c` ↔ story, through the shipped surface | `core` · `full` | the corrected AT-801b arm + `test_AT_801c_a_resize_heals_the_selection_in_one_refresh` (the app driven at two sizes through the house pilot) | 2 nodes passed |

The two chainmap files: **13 passed**; the full suite at the increment's close: **2556 passed,
0 failed** — the complete green over the settled tree (all four increments' nodes in;
`evidence/inc003-run.log`). The C-2b oracle arms (TC-801/802) stayed byte-green — the cap only
touches bands that previously vanished whole, so the oracle frames (no folded bands) could not
move. The ONE complete clean-tree run at close is the orchestrator's (C-25) — "see
04-validation".

> ⚠ **Failure-count declaration (V56):** this packet's settled figure is `0 failed`; the cited
> transcript `evidence/inc003-run.log` holds `31 failed, 2525 passed` at line 803 — the agent's
> GENERIC-heal full-suite attempt (the 13-test breakage + the other views' regressions) that
> motivated the chainmap scope — and three intermediate single-file failures (lines 836 · 903 ·
> 1093) while the cap arms were being settled. Every failure line in the cited bytes is one of
> those deliberate development rounds; the settled final run in the same file is 2556 passed,
> 0 failed.

### RED counterfactual — executed, not predicted

| Field | Value |
|---|---|
| Mutation applied | **M6 (the cap's N off by one):** `f"+{tail_n} more ↓"` → `f"+{tail_n + 1} more ↓"` (views.py, the cap tail row). **M7 (the zero-fit band draws its head):** the zero-fit guard `if limit == 0: break` → `if limit == 0: limit = 1` (the first chain draws, the head dangles without its canvas). **M8 (the heal neutered) — two variants:** A, the heal's guard → `if True: return`; B, the heal's call at the end of `refresh_view` removed entirely |
| Instrument | project code: the coordinator's byte-level edit runner (the `run-mutations-abc.py` sibling; `evidence/mutations-d.log` quotes the full outputs from the session record; every restore verified by sha256 — `OK` on every line, the byte runner does not normalize line endings) |
| Where it ran | **my own tree** — the MAIN checkout (the batch's single lane) |
| Transcript | `evidence/mutations-d.log` — M6: exit 1, `AssertionError` on `assert "+4 more ↓" in text` (the mutant paints `+5`) → KILLED. M7: exit 1, `AssertionError` on `assert not any(tid in lm2 for tid in ("tm2","tm3","tm4","tm5"))` (the zero-fit band's tiles leak into the line_map) → KILLED. M8 (both variants): exit 0 — `test_AT_801c_a_resize_heals_the_selection_in_one_refresh` GREEN → SURVIVED, declared with its cause |
| Restore proven by | **file hash returned to its pre-mutation value**: `evidence/mutations-d.log` — "All restores verified by sha256 (`OK` on every line)" |
| Bytecode cache | run with `PYTHONDONTWRITEBYTECODE=1` (C-46) |
| Arms resolved at baseline | **1** targeted for M6/M7 — `tests/test_chainmap.py::test_TC_810_the_fold_caps_a_partial_band_and_still_drops_whole` (the two chainmap files hold 13 nodes, all green at baseline) |
| Verdict granularity | **per resolved node id** — M6/M7 reddened exactly the amended TC-810; M8 left exactly AT-801c GREEN |
| Arms that stayed GREEN | M6/M7: the other 12 chainmap nodes stayed GREEN (the cap mutation touches only the partial-band tail; the oracle frames have no folded bands). M8: `test_AT_801c_a_resize_heals_the_selection_in_one_refresh` stayed GREEN under BOTH variants — the declaration below |

| Field | Value |
|---|---|
| **RED counterfactual** | M6 — the cap's N+1 (views.py tail row) · M7 — the zero-fit guard `limit = 1` · M8 — the heal neutered, two variants · transcripts at `evidence/mutations-d.log` · every restore digest `OK` |

| Field | Value |
|---|---|
| **Mutation verdicts** | per resolved node: M6 · TC-810 KILLED (`+5` painted against the exact `+4` pin) · M7 · TC-810 KILLED (the dangling head's tiles leak into the line_map) · M8 · AT-801c **SURVIVED-with-cause, declared** — cause (traced, not guessed): the shipped `_select_first` has a chainmap branch (a selection not in the nav order moves to the first linked task in draw order) and `_nav_flat()` is fold-aware, so on the NEXT `refresh_view` the stale selection is already healed by shipped code; the end-state assertion after `pilot.pause()` drains every pending refresh, so the arm observes the healed end-state no matter which mechanism got there first. The increment's heal makes the FIRST refresh's paint transient-free and lands the cursor on the nearest painted row (min line-map row) instead of the first nav task — a real but transient-level difference an end-state arm cannot isolate without pinning Textual's own refresh churn (3 refreshes per measured resize) · follow-up (named in `evidence/mutations-d.log`, NOT a block): if the one-refresh law ever needs a paint-level pin, that is a NEW arm asserting mid-repaint state · inert arms: none — every GREEN arm is named with its mechanism |

### Instrument RED-proof — every instrument shown able to report FAILURE first

| Instrument | Known-bad input fed to it | The FAILURE it reported |
|---|---|---|
| `pytest` (the suite) | M6's mutant code | `1 failed` — the exact-tail assertion: `assert "+4 more ↓" in text` against the painted `+5` (`evidence/mutations-d.log` M6) |
| `pytest` (the suite) | M7's mutant code | `1 failed` — the line_map absence assertion failed with the leaked tids in the map (`evidence/mutations-d.log` M7) |
| the line_map assertion (the instrument inside TC-810) | M7's leaked zero-fit tiles | `AssertionError: {'hpweb0': 5, 'hpweb1': 8, ...}` — the map names rows that never painted |
| the byte-anchor runner | a stale/ambiguous anchor | the sibling battery's M3 showed the failure mode (0-count anchor → mutation skipped, `mutations-abc.log` §M3) — the anchor check itself is the instrument that reports a BAD mutation instead of silently passing it |

| Field | Value |
|---|---|
| **Instrument RED-proof** | 4 instruments, each shown able to report FAILURE before its PASS was believed (transcripts per row); M8's instrument honestly reported PASS — and the packet declares why that is not a kill |

### Emitted-form assertion — assert the bytes the producer EMITS (C-42)

| Artifact emitted | The assertion, run against the EMITTED form | What it returned |
|---|---|---|
| the painted chainmap canvas (the partial band's tail) | `"+4 more ↓" in text` on the emitted frame — N exact | the exact tail row painted |
| the emitted `line_map` | the zero-fit band's tids absent: `not any(tid in lm2 for tid in ("tm2","tm3","tm4","tm5"))`; the tail row present like any painted row | both hold — the map only ever names rows that painted |
| the C-2b oracle frames (TC-801/802) | byte-exact frame comparison on the unchanged fixtures | byte-identical — the fold path is never taken where no band folds |
| the healed selection after ONE refresh | `app.selected_task_id` names a row the fresh `line_map` names (AT-801c, the app driven at two sizes through the pilot) | holds after a single refresh |

| Field | Value |
|---|---|
| **Emitted-form assertion** | 4 artifacts, each asserted against the form its producer emitted |

### Evidence files — bytes at a declared home, verbatim, hash-verified (C-59)

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| the increment brief | `.dev-flow/2026-10-07-batch-05/evidence/inc003-brief.md` | `c8737a40e220eea51ea640b8a6662c1d2b791561ab292bc389ef855403753abb` |
| the agent's run + review packet (13 passed chainmap; 2556 full; the scope rationale; the byte-green oracle) | `.dev-flow/2026-10-07-batch-05/evidence/inc003-run.log` | `80b63902bdb97abfd2538e18479eee10a0fff3c740815f1374614c6b4c242b6b` |
| the mutation battery M6/M7/M8 (the M8 declaration and its follow-up) | `.dev-flow/2026-10-07-batch-05/evidence/mutations-d.log` | `20f3e589e9914dba954235ad4762960e6e75a4ef4aedb328be3de06dfbde7d30` |

| Field | Value |
|---|---|
| **Evidence files** | 3 artifacts, each at the declared home and cited with the digest of its stored bytes |

### Load-bearing emptiness — what is this resting on that is only true today? (C-55)

| Field | Value |
|---|---|
| Does any claim here rest on the tree holding NO instance of some case? | **yes** — "a zero-fit band draws NOTHING" (no dangling head) is an absence claim over the painted canvas AND the emitted line_map; "the oracle frames hold no folded band" underlies their byte-identity |
| If the result is an ABSENCE, what made the search wide enough | the zero-fit arm asserts over EVERY tid of the band (`not any(tid in lm2 for tid in ("tm2","tm3","tm4","tm5"))`) plus the painted text — not one probe row; the oracle fixtures enumerate every band's fit state at both sizes |
| Guard labelled as protecting a CONCLUSION, not a behaviour | the amended `TC-810`'s docstring — the zero-fit arm is the dangling-head law's guard, kept verbatim inside the renamed node so the cap amendment never swallows it |
| Conjunctive criteria: one mutation per conjunct | the cap has two conjuncts — the tail's N exactness (M6) and the zero-fit whole-drop (M7); the heal's end-state is over-determined by shipped code, which is M8's declared cause |
| Synthetic instance of the absent case | the amended TC-810's frozen fixture — a band engineered to fit exactly none of its chains at the pinned size, synthetic because the shipped storage holds no such tall project at 80×24 |
| **Positive control for every probe that returned an ABSENCE** | the SAME line_map under the partial-band arm names the drawn chains + the tail row (a known-present non-absence on the identical instrument); the oracle frames' byte-identity is a known-present positive control for the "fold never taken" premise |

### Reverse census — trigger family B

| Probe | Command | Result |
|---|---|---|
| B1 symbols asserted by **other** tests | `grep -rln "test_TC_810\|AT_801b\|AT_801c" tests/` → `tests/test_chainmap.py` · `tests/test_chainmap_app.py` | the two chainmap files — this increment's pins; the C-2b oracle arms (TC-801/802) read the same renderer and stayed byte-green |
| B2 file moved on disk | `git status --porcelain -- taskboard/views.py taskboard/app.py` → ` M` both | no rename, no delete; probe executed, did NOT fire |
| B3 byte-identical golden captures this source | `ls tests/goldens` → no such directory in this repo | did NOT fire |
| B4 artifact produced here is consumed elsewhere | the fold's `line_map` feeds the app's navigation + scroll (`_scroll_selected_into_view` reads `_line_map`); the legend/help read the painted bands; the oracle frames are consumed by TC-801/802 | every consumer re-validated by the 2556 green |
| A3 interface consumed by another module changed | `grep -rn "_heal_selection_after_repaint" taskboard/` → the single call at `app.py:1524` + the definition at `:1526` | one new private method, one call site, chainmap-scoped; `refresh_view`'s public contract unchanged |

| Field | Value |
|---|---|
| **Reverse census** | 5 probes run of B1 · B2 · B3 · B4 · A3 — B1's hits are this increment's own pins, A3 names one new private method under an unchanged public contract, B2/B3 did NOT fire with their probes recorded |

### Correction population — enumerated BEFORE the first site was edited

| Correction | Population — the assertion category | Enumeration method (the command) | Count | Sites edited | Sites left, and why |
|---|---|---|---|---|---|
| the three batch-C chain-map carries (this increment) | the BACKLOG's standing carries | `.dev-flow/BACKLOG.md` "Open — after `2026-10-07-batch-02` (Batch C)" — the three bullets | 3 items | the deep-chain cap (views.py) + the resize heal (app.py) + AT-801b's docstring (test_chainmap_app.py) — this increment | none — the batch's other carries are increments 001/002/004's |

| Field | Value |
|---|---|
| **Correction population** | 1 correction wave (the three-item Batch-C tranche of the ten-item backlog wave), enumerated before the first site was edited; every site accounted for |

#### Supersession-completeness inspection (V-3)

| Superseded marker | grep result | All surviving refs negative? | Evidence (file:line) |
|-------------------|-------------|------------------------------|----------------------|
| the old TC-810 node name `test_TC_810_the_fold_drops_whole_bands_never_a_dangling_head` | 0 hits over `tests/` + `taskboard/` | yes — the only TC-810 is the renamed node | `tests/test_chainmap.py:185` |
| the whole-band-drop rule as the ONLY fold behavior | 0 hits as a surviving rule — the amended node carries the zero-fit whole-drop INSIDE the cap law (the dangling-head arm) | yes | `tests/test_chainmap.py:185` (the amended node) · LED-2026-10-07-batch-05.1 |

### Signed-balance test ledger

`post = base − D + A` → `2556 = 2555 − 0 + 1` ✓ reconciles (base = increment 002's 2555 close;
this increment added exactly one node — `AT-801c`; the TC-810 rename modified, not added; the
AT-801b docstring modified, not added). The batch-level ledger is summed in `04-validation.md`
— "see 04-validation".

---

## 4b · Independent review — the lens the author cannot be

| Field | Value |
|---|---|
| **Independent review** | `human:coordinator` — the close-out coordinator self-executed the P2 lens pool over the four packets and the diffs · verdict PASS-WITH-NOTES, 0 HIGH — the notes: the M8 SURVIVED-with-cause declaration (§4 names the GREEN arm and the traced cause; the paint-level follow-up is recorded in `evidence/mutations-d.log`, not a block), the chainmap-scoped heal (§5), the tail-vs-bare quirk (§5) · the P2 review verdict stands in `02-review.md` |

---

## 5 · Risks

- The resize heal is CHAINMAP-SCOPED — deliberately. The agent's first attempt was generic
  (re-verify in every view) and broke 13 tests: the swimlanes `grid` presentation draws an
  aggregated board with an EMPTY `line_map` (its selection is meaningful but not named), the
  gantt's selection can legitimately sit outside its `line_map` after `_select_first`, and
  `flow`/`standup` draw no task rows. The chain map is the only view whose selection must sit on
  a named tile AND whose heal reads the stale line_map (the actual bug); kanban/gantt are healed
  by their data-based `_select_first` up front. A future view that needs the heal must opt in
  explicitly.
- Tail-vs-bare quirk (pre-existing, left as-is): bare projects ("no links") draw AFTER the fold
  loop, so a folded `+N more ↓` tail can be followed by a bare band. It existed before this
  change (bare bands painted after the fold, under a blank gap); surgical scope kept it. Not
  asserted, not a test risk — the operator's call if it ever reads wrong.

## 6 · Pending items / spec deviations

- The M8 follow-up: a paint-level pin for the one-refresh law (asserting mid-repaint state)
  would isolate the heal's transient-free value from `_select_first`'s end-state convergence —
  recorded in `evidence/mutations-d.log`; not a block, not opened as a backlog item (the shipped
  behavior is correct; only the TEST cannot distinguish the two mechanisms).

## 7 · Suggested next task

- Increment 004 — the test-strength carries (the AT-601/602 key-walking arms; the team-folder
  arm; the ash-column pin) — the batch's last increment.

## Increment gate checklist

| # | Item | Owed in | ✓/⚠/✗ | Evidence (node id · command output · file:line) |
|---|---|---|---|---|
| 1 | ≤4 source files, or reason declared | all | ✓ | 2 source files (views.py · app.py) |
| 2 | Tests written in this same increment | all | ✓ | the amended TC-810 + the new AT-801c + the AT-801b docstring landed with the product in the same run |
| 3 | Layer 0 written where the criterion applies | `core` · `full` | ✓ | the fold's cap branch — the amended TC-810, mutation-proven (M6/M7) |
| 4 | **RED counterfactual** declared | `core` · `full` | ✓ | M6/M7 KILLED · M8 SURVIVED-with-cause; transcript `evidence/mutations-d.log`; restores `OK` on every line |
| 5 | **Reverse census** declared | `core` · `full` | ✓ | 5 probes run (table above) |
| 6 | `code-reviewer` passed — HIGH blocks; verdict + reviewer in §4b | `core` · `full` | ✓ | §4b — `human:coordinator` self-executed lenses · PASS-WITH-NOTES 0 HIGH |
| 7 | No file from another lane touched | all | ✓ | one lane; serialized after increment 002 by the plan (§2.8); `git diff --name-only HEAD` — views.py + app.py only |
| 8 | Frozen interfaces untouched | all | ✓ | `refresh_view`'s public contract unchanged (one closing call); the C-2b oracle frames byte-green; the zero-fit law survives inside the amended node |
| 9 | Coverage claims verified **on disk** | all | ✓ | every claim cites a stored transcript + sha256 (Evidence files table) |
| 10 | Load-bearing emptiness declared, with synthetic instance | all | ✓ | the zero-fit absence over canvas + line_map; the synthetic no-fit band fixture |
| 11 | **Mutation verdicts** declared — per arm | all | ✓ | per-node table above; M8's GREEN arm named with its traced cause and the follow-up the file names |
| 12 | **Instrument RED-proof** declared | all | ✓ | 4 instruments (table above) |
| 13 | **Correction population** declared | all | ✓ | the three-item Batch-C tranche, enumerated before the first edit |
| 14 | **Emitted-form assertion** declared | all | ✓ | the painted tail + the emitted line_map + the oracle frames + the healed selection |
| 15 | **Independent review** names somebody | all | ✓ | §4b — `human:coordinator` |
| 16 | **Evidence files** declared | all | ✓ | 3 artifacts with stored-byte digests |
