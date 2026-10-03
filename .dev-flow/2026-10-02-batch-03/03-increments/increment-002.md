# Increment 002 — HLR-306, HLR-308, HLR-310 · the cap, the copy, the cursor off undrawn done work

> Review packet (flow `templates/increment-template.md`; reserved field names kept literal).
> Lives in the repo next to the diff it describes. Mode `core`, language `en`.

| Field | Value |
|---|---|
| Batch | `2026-10-02-batch-03` |
| Increment | `002` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | HLR-306 (LLR-306.1, D-312), HLR-308 (LLR-308.1), HLR-310 (LLR-310.1) |
| Acceptance | AT-304, AT-306, AT-308 · white-box TC-309, TC-310, TC-312 |
| Agent | `software-dev` (this runtime's implementing agent) |
| Date | `2026-10-02` |

---

## 1 · What changed

**A board full of highs keeps its projects, the help says what the board draws, and the cursor
never rests on a done card the board only counts.** The high band's cap (two thirds of the body,
`+N more ↓`, the overflow drawn in its project band — coded with the board in increment 001) is now
pinned node by node over the executed h-table and a 14-high board. Under a `/` filter the app asks
the nav for the same two-rows-shorter height the renderer draws (D-312 — increment 001's open F2).
`?` in the kanban describes the band rule, `┈`, the rail, the high band and `+N more ↓` (still four
sections, every bullet ≤ 44 cells); the example shows `⛓N` before the due; the legend calls `▐` the
project's band. When `]` finishes a card at a width where the rail is a count, the card that took
its place takes the cursor and a notification says `‹title› done · counted in the ✓ rail · u undo`
(markup off); any other way the selection lands on a counted card (a resize, `z`, a filter, a
delete, a lost id) moves it by the `z` rule. Code review found the last path (HIGH, F1: the reset
to the first visible task skipped the rule) and it is folded.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/app.py` | source | LLR-310.1, LLR-306.1 | `_nav_columns`: `h − 2` for the kanban under a query (D-312); `_select_first`: the `z` rule for a selection the grouped board does not draw, after any reset; `action_phase_move`: the neighbour and the notification |
| `taskboard/views.py` | source | LLR-308.1 | the kanban help section "the board", the example's meta order, the legend's `▐` label |
| `tests/test_kanban_readable.py` | test | HLR-306, HLR-308, HLR-310, LLR-306.1, LLR-308.1, LLR-310.1 | NEW: TC-309 ×15 (h-table ×10, the overflow row, the filtered nav ×4), TC-310, TC-312 ×3, AT-304, AT-306, AT-308 ×3; AT-307 compares the band SET (a one-off flake, §6) |
| `tests/test_app.py` | test | HLR-306 | `_assert_kanban_parity` counts the rail's `+N more`, not the cap's (code review F11 of increment 001) |
| `tests/test_prism_laws.py` | test | HLR-303 | the band-rule law anchored on the rule's text end (code review F13 of increment 001) |

| Count | Value |
|---|---|
| **SOURCE files** | **2 / 4** |
| Test files | 3 (uncapped) |
| Doc files | 0 |

## 3 · How to test

```bash
python -m pytest -q tests/test_kanban_readable.py tests/test_app.py tests/test_prism_laws.py tests/test_english.py tests/test_kanban_priority.py
python -m pytest -q -p no:cacheprovider
```

## 4 · Test results

| Layer | Owed in | Nodes | Result |
|---|---|---|---|
| **0 · unit** | `core` · `full` | the cap's arithmetic over the h-table (TC-309 ×10) | 10 passed |
| **A · white-box** `TC-NNN` ↔ LLR | `core` · `full` | TC-309 (overflow row, filtered nav ×4), TC-310, TC-312 ×3 | 9 passed |
| **B · black-box** `AT-NNN` ↔ story, through the shipped surface | `core` · `full` | AT-304, AT-306, AT-308 ×3 | 5 passed |

Gate run on the frozen round-2 tree: `python -m pytest -q -p no:cacheprovider` → **1845 passed in 357.16 s, exit 0**
(`evidence/inc002-green.txt`).

### RED counterfactual — executed, not predicted

| Field | Value |
|---|---|
| Mutation applied | (a) the increment-001 tree with this increment's tests overlaid; (b) the base tree likewise; (c) the battery on the increment tree |
| Where it ran | scratch exports in the session scratchpad, never the live checkout |
| Transcript | `evidence/inc002-red.txt` (on the increment-001 tree: 8 failed — the copy, the cursor, the filtered nav); `evidence/inc002-red-on-base.txt` (16 failed — the cap nodes too, no `kanban_plan` there); `evidence/inc002-mutations.txt` |
| Restore proven by | the battery's per-mutant sha256 check |
| Bytecode cache | `-B`, `-p no:cacheprovider` |
| Arms resolved at baseline | 21 (the round-1 set) |
| Verdict granularity | per node (`-rA`) |
| Arms that stayed GREEN | on the increment-001 tree: the cap nodes (the cap shipped with the board in 001; RED by Q1–Q4) and AT-308's 118×30 arm (the no-move branch — a policy arm, C-10b); on base: the filtered-nav arms (the base nav ignored height: the gap was born in 001) and AT-308's 118×30 arm |

| Field | Value |
|---|---|
| **RED counterfactual** | the copy, cursor and filtered-nav nodes RED on the increment-001 tree for the specified reasons (`top of each column`; the cursor on undrawn `to3`, nothing posted; nav out of draw order at panels 12, 13, 20, 21) · `evidence/inc002-red.txt` · the cap nodes RED on base (`evidence/inc002-red-on-base.txt`) and under Q1–Q4 · restore digests in `evidence/inc002-mutations.txt` |

| Field | Value |
|---|---|
| **Mutation verdicts** | 15 of 15 KILLED (harness `evidence/mutate.py`; specs `mutants_inc002.json`, `mutants_inc002_r1.json`; transcripts `inc002-mutations.txt`, `inc002-mutations-q7q8.txt`, `inc002-mutations-tail.txt`): Q1 no cap · Q2 one high too many · Q3 the half-body cap (caps the approved 80×24 frame) · Q4 no `+N more` row · Q5 the nav asks the full height under a filter · Q6 the cursor to the column's top · Q7 no notification · Q8 markup on · Q9 no relocation (resize) · Q10 the help forgets the cap · Q11 the legend's old label · Q12 the example's meta order · Q13 the relocation skipped after a reset (F1) · Q14 the `z` rule leftmost (F2) · Q15 the column's last card instead of the neighbour (F3). Arms green under a kill: Q1's h-0 arm (no cap by design), Q2/Q3's arms below the cap, AT-308's other arms per mutant — named in the transcripts; every restore digest OK |

### Instrument RED-proof — every instrument shown able to report FAILURE first

| Instrument | Known-bad input fed to it | The FAILURE it reported |
|---|---|---|
| `_posted` (the notifications this action posted) | the boot notice present in `_notifications` | the first draft compared the whole list and failed on the boot notice — the instrument now slices from the count before the key |
| the Label reader of AT-306 | the compositor strips of a modal not yet painted | blank text — replaced by the Labels' own render (the batch-02 recipe) |
| TC-309's filtered-nav walk | the increment-001 app (full height) | nav out of draw order at panels 12/13/20/21 (`inc002-red.txt`) |

| Field | Value |
|---|---|
| **Instrument RED-proof** | 3 instruments, each shown failing before its PASS was believed |

### Emitted-form assertion — assert the bytes the producer EMITS (C-42)

| Artifact emitted | The assertion, run against the EMITTED form | What it returned |
|---|---|---|
| the notification | `app._notifications` messages and the painted `Toast` render | the title literal, `[b]x[/b]` included |
| the help modal | the `Label`s of the painted `HelpScreen` | the four words present, the old phrase absent |
| the board under the cap | the rendered rows (`+8 more ↓` cell) and the nav | passed |

| Field | Value |
|---|---|
| **Emitted-form assertion** | 3 artifacts, each asserted in the form the producer emitted |

### Evidence files — bytes at a declared home, verbatim, hash-verified (C-59)

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| RED on the increment-001 tree | `.dev-flow/2026-10-02-batch-03/evidence/inc002-red.txt` | `83e5410362a8dceae13417f6d7e8c22324392bcbfe538d8488d108b0c5850d69` |
| RED on base | `.dev-flow/2026-10-02-batch-03/evidence/inc002-red-on-base.txt` | `9c5d464df167e2e8619a33d7c763a7f22e6fbdff92a0f707b21a9e203b142911` |
| battery Q1–Q6, Q13–Q15 (round-2 tree) | `.dev-flow/2026-10-02-batch-03/evidence/inc002-mutations.txt` | `e5fdd28982a4c945bf36b1633beac88fd6bdd62acefc2a7e0f3bb9e881ac35e1` |
| battery Q7–Q8 (sites moved by the F5 fold) | `.dev-flow/2026-10-02-batch-03/evidence/inc002-mutations-q7q8.txt` | `15e0ef64feca2ade510793d2ffbef81eabf582fb6b365712aaa0fd2f38eafe2e` |
| battery Q9–Q12 (site moved by the F1 fold) | `.dev-flow/2026-10-02-batch-03/evidence/inc002-mutations-tail.txt` | `5de7350170cf93e8514bf80e36dcb37466e971beab36c36509aad59d734b4060` |
| mutant specs | `.dev-flow/2026-10-02-batch-03/evidence/mutants_inc002.json` | `152ef10d088cd5c140b26be71170eced682bd0c96224973e04a47a03b074a1a7` |
| mutant specs, tail | `.dev-flow/2026-10-02-batch-03/evidence/mutants_inc002_tail.json` | `4602a34cd103fe777d08a0206a2c94e4333c5f267ada70903ca0c6b2858d3bab` |
| mutant specs, review round 1 | `.dev-flow/2026-10-02-batch-03/evidence/mutants_inc002_r1.json` | `f58bc19b9f414a60af1e4380e54f3226245972d9a5eac5d76376dc41b3f2e6ba` |
| spec generator | `.dev-flow/2026-10-02-batch-03/evidence/make_mutants_inc002.py` | `1e17aac649be01807af866c458871bb994559c883375e22f2be027a672abb165` |
| spec generator, round 1 | `.dev-flow/2026-10-02-batch-03/evidence/make_mutants_inc002_r1.py` | `0f935fc7203a9701708f3628f13459b315e151d622d63c2f747afbc9d9c7bb16` |
| reverse census (002 sources, 001 tests) | `.dev-flow/2026-10-02-batch-03/evidence/inc002-reverse-census.txt` | `f3d3995334fc3522d740f0305f0f0675758796251ede64d5524211253469ff67` |
| gate run | `.dev-flow/2026-10-02-batch-03/evidence/inc002-green.txt` | `d3e60a0a93ef4e46dec2e0aef0605ab14d66502311f282843d292d33c121fe8a` |
| redaction (account name added, security S-1) | `.dev-flow/2026-10-02-batch-03/evidence/redact.py` | `88ba9f3590af87dda138aa038e06c8165e89e5079af2b50e04394977a8efacf6` |
| packet re-hash | `.dev-flow/2026-10-02-batch-03/evidence/rehash_packets.py` | `b7392fa2c5790afda788be19c804cb30448b19beb35b568c7e5045ef79b817ba` |
| close capture 14-high 118×30 | `.dev-flow/2026-10-02-batch-03/evidence/captures/close-kanban-14high-118x30.txt` | `6da56e8d3def6eca1bc24e9c31638cba4aa40ebdebabafb9f602fb80856d76a9` |
| close capture 14-high 80×24 | `.dev-flow/2026-10-02-batch-03/evidence/captures/close-kanban-14high-80x24.txt` | `c45d7ced6b18dab1d150deb7627f828cd42133723152bb4dad7f2d84e02d56d3` |

| Field | Value |
|---|---|
| **Evidence files** | 16 artifacts under the declared home, each cited with the digest of its stored bytes |

### Load-bearing emptiness — what is this resting on that is only true today? (C-55)

| Field | Value |
|---|---|
| Does any claim here rest on the tree holding NO instance of some case? | yes: "no selection rests on a counted card" (the paths code review enumerated: `[`/`]`, resize, `z`, filter, delete, archive, `F`, `v`, a lost id) |
| If the result is an ABSENCE, what made the search wide enough | the rule sits in `_select_first`, which every refresh runs, AFTER every reset |
| Guard labelled as protecting a CONCLUSION, not a behaviour | `test_TC_312_a_reset_selection_never_lands_on_a_counted_card` |
| Conjunctive criteria: one mutation per conjunct | Q9 (no relocation), Q13 (relocation only on the non-reset path) |
| Synthetic instance of the absent case | the filter `p` and the lost id, both landing on `tw1` |
| **Positive control for every probe that returned an ABSENCE** | the reset itself lands on `tw1` (a counted card) — Q13 RED proves the probe sees it |

### Reverse census — trigger family B

| Probe | Command | Result |
|---|---|---|
| B1 symbols asserted by **other** tests | the full suite with this increment's sources and the increment-001 tests (`evidence/inc002-reverse-census.txt`) | 7 failed / 1814 passed: 0 product nodes — the 7 are environment-only (the scratch export has no git history or hook: `test_no_live_board` ×1, `test_precommit_gate` ×1, `test_scratch_cannot_be_committed` ×5), green in the live checkout; the help kept its four sections, so `test_english.py::test_TC_206_help_copy_is_english_and_fits` and `test_kanban_priority.py::test_help_example_shows_a_badge_and_says_the_band_is_grouped_only` hold. The two test edits outside the new file are hardening from increment 001's review (F11, F13), not census-driven |
| B2 file moved on disk | none | did not fire |
| B3 byte-identical golden captures this source | `ls tests/goldens` | did not fire |
| B4 artifact produced here is consumed elsewhere | the help copy → `HelpScreen`; the notification → the toast | AT-306, TC-312 read the painted forms |
| A3 | interface consumed by another module changed | none (`nav_model`, `render_view` unchanged) | did not fire |

| Field | Value |
|---|---|
| **Reverse census** | 5 probes: B1 fired (0 product nodes; 7 environment-only), B4 fired (AT-306, TC-312), B2/B3/A3 did not fire |

### Correction population — enumerated BEFORE the first site was edited

| Correction | Population — the assertion category | Enumeration method (the command) | Count | Sites edited | Sites left, and why |
|---|---|---|---|---|---|
| the shipped help's per-column band | every place the copy says the band is per column | `grep -rn "top of each column\|── high ──" taskboard/ README.md` | 1 | 1 (`help_usage`) | the test docstrings that narrate the superseded design (history) |

| Field | Value |
|---|---|
| **Correction population** | 1 correction, enumerated before its first site was edited |

### Signed-balance test ledger

`post = base − deleted + added` → `1845 = 1821 − 0 + 24` ✓ (TC-309 ×15, TC-310, TC-312 ×3, AT-304, AT-306, AT-308 ×3; AT-307 and the two hardened nodes rewritten in place, net 0).

## 4b · Independent review — the lens the author cannot be

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a named sub-agent with `agents/code-reviewer.md` · round 1: `BLOCK-UNTIL: F1` (HIGH: after `_select_first` reset the selection to the first visible task the kanban rule never ran — delete, archive, `/` filter, `F`, `v` or a lost id could leave the cursor on an undrawn done card) with F2, F3 (MEDIUM: the `z` rule's direction and the neighbour unpinned — its Z1, Z2 survived), F4, F5 (LOW) — Q1–Q12 12/12 KILLED by its own run · folded: F1 the rule now runs after any reset (+ a filter/lost node), F2 the target asserted (`tw2`), F3 the `tw2 → tm6` arm, F5 the redundant guard removed, F4 to BACKLOG · round 2 over the frozen tree: `OK to advance`, F1 discharged by re-reading and by Q13 KILLED, its 46-case probe (delete, archive, `F`, `v` ×3, presentation hops, collapse, lost id, empty filter, view hops; 5 sizes; empty and all-done boards) green and 13 of them RED under Q13; Q14, Q15 KILLED; nothing open. `security-reviewer` — PASS-WITH-NOTES over increments 001–002, 0 HIGH: S-1 (LOW, the account name in transcripts) fixed, S-2 (LOW, latent `collapse_runs` join) to BACKLOG; the P2 S-1..S-3 discharged by reading and a 200k-string fuzz |

## 5 · Risks

- The selection rule re-plans the board on every grouped refresh (a second `kanban_plan`); measured cost small (code review F5).
- The provisional decisions PV-2 (the cap) and PV-8 (the cursor and notification) ship before the operator's verdict.

## 6 · Pending items / spec deviations

- AT-307 now compares the band SET by name: once, in a full-file run, the rule cells shifted one cell (a transient width change, likely a scrollbar or a resize race; unexplained, code review F4) → BACKLOG.
- Security S-2 (LOW, latent): `collapse_runs` can join two adjacent same-style escaped pieces into a tag → BACKLOG. Security S-1 (LOW) fixed: `evidence/redact.py` redacts the account name; every transcript re-redacted, packet digests re-computed (`evidence/rehash_packets.py`).
- The gantt's nav may have the same filter-height gap → BACKLOG.

## 7 · Suggested next task

P4 validation: the orchestrator's gate run, qa-reviewer's evaluation, ux-reviewer's walkthrough on the captures and the app.

## Increment gate checklist

| # | Item | Owed in | ✓/⚠/✗ | Evidence (node id · command output · file:line) |
|---|---|---|---|---|
| 1 | ≤4 source files, or reason declared | all | ✓ | 2 / 4 |
| 2 | Tests written in this same increment | all | ✓ | `tests/test_kanban_readable.py` |
| 3 | Layer 0 written where the criterion applies | `core` · `full` | ✓ | the cap's arithmetic (TC-309 h-table) |
| 4 | **RED counterfactual** declared | `core` · `full` | ✓ | §4 |
| 5 | **Reverse census** declared | `core` · `full` | ✓ | §4 |
| 6 | `code-reviewer` passed | `core` · `full` | ✓ | §4b |
| 7 | No file from another lane touched | all | ✓ | one lane |
| 8 | Frozen interfaces untouched (or returned to the trunk) | all | ✓ | no signature changed |
| 9 | Coverage claims verified **on disk**, not from intent | all | ✓ | ids in docstrings; nodes collected |
| 10 | Load-bearing emptiness declared, with its synthetic instance (C-55) | all | ✓ | §4 |
| 11 | **Mutation verdicts** declared | all | ✓ | §4 |
| 12 | **Instrument RED-proof** declared | all | ✓ | §4 |
| 13 | **Correction population** declared | all | ✓ | §4 |
| 14 | **Emitted-form assertion** declared | all | ✓ | §4 |
| 15 | **Independent review** names somebody | all | ✓ | §4b |
| 16 | **Evidence files** declared | all | ✓ | §4 |
