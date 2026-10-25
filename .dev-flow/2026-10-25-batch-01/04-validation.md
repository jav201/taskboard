# Validation — taskboard — Batch 2026-10-25-batch-01

> **Artifact language:** canonical English scaffold; the batch's language is
> `en` (`state.json`). Phase 4 artifact; content owner `qa-reviewer`, who
> evaluates the Phase-1 validation strategy, names who executed each row, and
> returns the rows; the orchestrator writes this file. The ONE complete
> gate-suite run is the orchestrator's (`C-25`).

**`Mode`:** `validation`

## ✅ Verdict (read first)

- **Result:** PASS-WITH-NOTES — returned by `qa-reviewer` (independent, P4), 0
  blocker, 0 major-open, 1 major + 3 minor findings (QA-P4-01..04, all folded in
  this record, §qa-reviewer findings below); the gate run is the orchestrator's
  (consumed, not run, by `qa-reviewer`).
- **Gate run:** `env -u NO_COLOR python -m pytest -q -rs -p no:cacheprovider
  <the files of evidence/suite-p4-files.txt, 112 files in 3 disjoint chunks>`
  — `evidence/suite-p4-chunk00-run.txt` **1440 passed** ·
  `chunk01-run.txt` **959 passed** · `chunk02-run.txt` **859 passed** — total
  **3258 passed, 0 skipped, 0 failed**, each transcript headed by its exact
  command and `git rev-parse HEAD` (`9aaada7` + this record's commit; no
  source changed after the increment), each ending on its `N passed` summary
  line with no failure line · run by the orchestrating chain in three
  SEQUENTIAL chunks, nothing in parallel with any of them · each transcript
  headed `HEAD: d5c9e18` (the DDR-sealed commit; `git diff ce89030 d5c9e18`
  touches `.dev-flow` records and the added AT-2804 node only — no source
  change between the increment and the gate).
- **Baseline reconciliation:** the commission's baseline is 3248 passed + 1
  environmental skip (TC-1902, the clipboard arm) · this batch adds 9 nodes →
  3257 expected · the gate run collected **3258 passed + 0 skipped**: the
  clipboard arm (tests/test_app.py:1312, chunk00) RAN and PASSED — the machine
  allowed `Set-Clipboard` today — so the environmental skip became a pass
  (+1). No other skip, no fail: the commission's «any other skip or fail
  blocks the close» clause is not triggered; the delta is named, not smoothed.
- **Layer 0:** none due — the increment's change is one CSS declaration
  (cyclomatic 1, no module boundary crossed); the unit criterion's evidence
  is the mutation battery (below).
- **Requirements:** 10/10 pass · 0 blocker fails — 4 HLR + 5 LLR + the HLR-2804
  regression pin, each row's nodes inside the green gate run (the 9 new nodes
  are in chunk02's files) and the requirement→node map in the matrix below.
- **Black-box acceptance (Layer B):** ✓ AT-2801 (single-board, both sizes),
  AT-2802 (home `enter`, both sizes), AT-2803 (team mode, both sizes + the
  picker-geometry arm), AT-2804 (the unchanged-paths pin) — each observes its
  outcome through the shipped surface (keys → the composited terminal frame),
  with the vacuity guard (modal-on-top + box located before counting) in every
  node; the mutation battery killed all six parametrized AT arms.
- **Surface-reachability (bidirectional):** ✓ every named input reaches the
  surface at the gate (the full suite's own arms) plus the real-terminal
  captures below; the picker and the offer are each captured in a real window.
- **Supersession inspection:** ✓ the packet's reverse census: 5 probes, B1's 21
  hits all re-validated (suites 001/002 + one scoped edit, justified in the
  packet §6), 0 foreign hits.
- **Test ledger:** ✓ reconciles: 3248 − 0 + 9 = 3257 new-node expectation; the
  gate collected 3258 = 3257 + the skip-turned-pass, named above.
- **Evidence checklist (qa-reviewer):** `qa-reviewer · 9 of 9 rows ✓ with evidence (record rows) · the four notes QA-P4-01..04 below are record-accuracy folds, none touching the green run`

> The `qa-reviewer` rows were returned on 2026-10-25 (independent reviewer,
> P4); no row is left pending.

---

## Detail (reference)

### Layer 0 — unit

None due (the change is one stylesheet declaration). The mechanism evidence is
the P3 mutation battery, read off the packet, not re-run at P4:

| Unit | Mutation applied | RED observed? | Transcript |
|---|---|---|---|
| the backdrop declaration (LLR-2801.1) | the declaration deleted | yes — KILLED by all six AT arms (AT-2801/2802/2803 × 118x30/80x24); SURVIVED by the geometry arm (inert for this mutant, named) and TC-2801 (pin by design) | `evidence/mutation-001.txt`, restore digest `4ed77a16…` |

### Layer A — white-box

| LLR | Node | Result |
|---|---|---|
| LLR-2801.3 (the picker half of the quit-while-open pin) | `tests/test_startup_backdrop.py::test_TC_2801_quitting_with_the_picker_open_writes_nothing` | passed (chunk02; a pin, not a gate — a stylesheet cannot change writes) |
| LLR-2801.1's resolved-style probe | superseded by the emitted-form render assertion + the mutation battery (code review F1) — declared in the packet §4 | n/a |

### Layer B — black-box

| AT | Story | Node | Result |
|---|---|---|---|
| AT-2801 | US-001 | `test_AT_2801_the_offer_opens_over_the_painted_board[size0|size1]` | passed (chunk02) |
| AT-2802 | US-001 | `test_AT_2802_enter_on_the_home_opens_the_offer_over_the_chosen_board[size0|size1]` | passed (chunk02) |
| AT-2803 | US-001 | `test_AT_2803_team_mode_shows_the_board_behind_both_modals_in_todays_order[size0|size1]` · `test_AT_2803_the_picker_keeps_its_pre_batch_geometry` | passed (chunk02) |
| AT-2804 | US-001 (pin) | `test_AT_2804_the_unchanged_start_paths_stay_unchanged` + the whole gate suite | passed (chunk02) |

### The mutation battery (C-40), read off the P3 transcripts

8 arms, one pytest invocation each, per-arm exit-code verdicts; the RED
counterfactual is AT-2801's declaration-delete (both sizes RED); restore
proven by hash. See the packet §4 and `evidence/mutation-001.txt`.

### The flake arm (PDR condition 3), read off its transcript

`evidence/flake-2801.txt`: 50 sequential runs of AT-2801 at 80x24, 0 failures;
50 in-process renders, minimum outside-box rows 4 above / 3 below (threshold
≥ 3). PASS.

### The real-terminal captures (the commission's Evidence clause)

Six shots, all accepted (`evidence/captures/README.md` is the page; `png/capture-log.txt`
the machine log): the single-board start's offer and the home path's offer at 118x30 and
80x24 (the commission's two scenes), plus the picker alone over the dimmed board at both
sizes (ux C3). Every window carried a unique `b01-<scene>-<size>-<n>` title, was closed by
that title right after its shot and verified gone; the final `assert-no-b01.ps1`
(its own command) printed `no b01-* window left open`; no `b01-cap-*` temp home remains.
The content-check mechanism (ux C2) is scripted: the READY check computes the live app's
composited full-stack render at capture time and requires > 0 board rows outside the modal's
box — a merely non-black shot cannot pass; a human read of all six PNGs agrees. Colour/byte
floors held (grab ≥ 9 colours, PNG ≥ 19 colours, ≥ 22 KB each); every READY end state `OK`.

### Requirements × validation matrix

| Requirement | Method | Executed verification (who ran it) | Result |
|---|---|---|---|
| HLR-2801 | test | AT-2801 both sizes (orchestrator's gate run) | pass |
| HLR-2802 | test | AT-2802 both sizes (gate run) | pass |
| HLR-2803 | test | AT-2803 both sizes + geometry arm (gate run) | pass |
| HLR-2804 (pin) | test | AT-2804 + the full suite (gate run) | pass |
| LLR-2801.1 | test | the six killed AT arms + the emitted-form probe (P3 battery; gate run) | pass |
| LLR-2801.2 | inspection | the increment's diff is the declaration + tests, nothing else (packet §2; `git show ce89030 --stat`) | pass |
| LLR-2801.3 | test | TC-2801 + the re-run offer suite (gate run) | pass |
| LLR-2802.1 | test | AT-2802 + the home suites (gate run) | pass |
| LLR-2803.1 | test | AT-2803 + the D-615 stack assertion (gate run) | pass |

### DDR conditions at P4

| # | Condition | Discharged? |
|---|---|---|
| C-2 (ux) | the captures name their content-check mechanism per shot | ✓ — scripted: the live app's composited render must show > 0 board rows outside the box at capture time (README's «The content check, named»); a human read of all six PNGs agrees |
| C-1/C-3 | carry to P5 (BACKLOG: the picker-placement item; the dimness hardening note) | pending — owned by the close gate |

### qa-reviewer findings (P4)

| id | severity | finding | disposition |
|---|---|---|---|
| QA-P4-01 | major | the Layer A/B tables cited chunk01 for the new nodes; they ran in chunk02 (`test_startup_backdrop.py` is in `suite-p4-chunk02.txt`) | folded — the six citations corrected to chunk02; substance unaffected (the nodes are inside a green chunk of the same sequential run) |
| QA-P4-02 | minor | the verdict cited HEAD `9aaada7`; the transcripts are headed `d5c9e18` (the DDR-sealed commit, immediately before the runs) | folded — the gate-run line now names `d5c9e18` and the no-source-change diff to the increment commit |
| QA-P4-03 | minor | the clipboard node is at `test_app.py:1220`, not :1312 | folded |
| QA-P4-04 | minor | the no-leftover assertion's output was not persisted | folded — re-run as its own command, output at `evidence/captures/assert-no-b01.txt` (`no b01-* window left open`, exit 0) |

### Evidence checklist

| Row | Evidence | ✓/⚠ |
|---|---|---|
| gate chunk 00 | `evidence/suite-p4-chunk00-run.txt` (1440 passed, headed by command + HEAD) | ✓ |
| gate chunk 01 | `evidence/suite-p4-chunk01-run.txt` (959 passed) | ✓ |
| gate chunk 02 | `evidence/suite-p4-chunk02-run.txt` (859 passed) | ✓ |
| chunk file lists | `evidence/suite-p4-files.txt` + `chunk00/01/02.txt` (112 files, disjoint — `sort | uniq -d` = 0) | ✓ |
| mutation battery | `evidence/mutation-001.txt` (+ runner) | ✓ |
| flake arm | `evidence/flake-2801.txt` (+ runner) | ✓ |
| P1 RED probe | `evidence/red-p1.txt` | ✓ |
| captures | `evidence/captures/png/` + `capture-log.txt` + `assert-no-b01.txt` (the no-leftover assertion's persisted output) | ✓ |

### Gate run

`env -u NO_COLOR python -m pytest -q -rs -p no:cacheprovider <chunk files>` × 3,
sequential · exit 0 on each chunk · on `d5c9e18` · run by the batch's
orchestrating chain (this session) · transcripts `evidence/suite-p4-chunk00/01/02-run.txt`.
