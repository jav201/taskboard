# Validation — taskboard — Batch 2026-10-24-batch-02

> **Artifact language:** canonical English scaffold. Generate in the batch's development language (`state.json` `language`); for Spanish batches **translate the prose, never a label** — the reserved field names are declared in §✅ Verdict and are read literally.
> Phase 4 artifact. Content owner: `qa-reviewer`, who **EVALUATES** the results of the validation strategy fixed in Phase 1, **names who executed each one** and returns the rows; the orchestrator writes `04-validation.md` (`stations/shared-homes-roles.md` §Delegation). The ONE complete gate-suite run is the orchestrator's (`C-25`); a sub-agent consumes the result and never owns the run.

> **Owed in.** `core` ✓ · `full` ✓

> **Field guide:** `templates/guides/validation-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

**`Mode`:** `validation`

## ✅ Verdict (read first)

> **Reserved field names.** The **field names and block keywords below are language-independent** — the
> validator parses them literally and they are never translated:
> `Result` · `Gate run` · `Layer 0` · `Evidence checklist` · `⏸ DEFER`
> Everything else on this page — headings, guidance, the prose in every cell — is translated with the batch.
> **One strategy, not two:** the flow ships no alias table, so a translated label is read as an ABSENT one and the rule keyed on it reports a true-sounding silence.
> **And one FLOW-WIDE reserved token, read out of this artifact by `V42` no matter which template minted it:** `⏸ DEFER`. It is a MARKER rather than a field name, which is why it is stated here *and* in `/dev-flow` §Language of artifacts rather than in a per-template list — a deferral can be written in any batch artifact, including the ones that carry no block at all.
>
> **And so are the three verdict tokens** `PASS` · `PASS-WITH-NOTES` · `FAIL`, which are VALUES and not prose.
> A Spanish batch writes `- **Result:** PASS`, not `- **Resultado:** aprobado`: the label, the tokens and the
> reviewer-identity tokens below are the machine's vocabulary.

- **Result:** PASS-WITH-NOTES — returned by `qa-reviewer` (independent, P4). 0 blocker, 0 major, 8 minor findings (QA-P4-01..08, §qa-reviewer findings below); G-001 itemized, G-002 / qa-m9 carried open. The gate run is the orchestrating chain's (consumed, not run, by `qa-reviewer`); the targeted re-runs named below are `qa-reviewer`'s own, on `32cafd3`
- **Gate run:** `python -m pytest -q -p no:cacheprovider <the files of suite-p4-files.txt>` in 3 sequential chunks (`evidence/suite-p4-chunk00.txt` 1439 passed + 1 skipped · `chunk01` 954 passed · `chunk02` 855 passed), each ending on its `N passed` summary line with no failure line · on `8baf9ad` (the tree under test; no source changed after the increments) · run by the batch's orchestrating chain (the previous implementer), transcripts consumed and verified by this session — NOT by `qa-reviewer`
- **Layer 0:** `6 unit(s) met the criterion (TC-2701 people/marks, TC-2702 people/marks, TC-2703, the D3 node) · all 6 carry a named reddening mutation` — E1..E4 of `mutation-001.txt` (24 arms) and E1..E6 of `mutation-002.txt` (30 arms), each target KILLED; read off the P3 packets, not re-run at P4
- **Requirements:** 23/23 pass · 0 blocker fails — 8 HLR + 15 LLR (the author's "11 LLR" miscounts: Layer A lists all 15, `grep -c '^### LLR-' 01-requirements.md` = 15; QA-P4-08), each row's node inside the green gate run (executed by the orchestrating chain) and the 13 new nodes re-executed by `qa-reviewer` on `32cafd3` (28 passed with the AT-2408/AT-2409/TC-2409 arms)
- **Black-box acceptance (Layer B):** ✓ every story's `AT` observes its outcome through the shipped surface (boundary + negative) — AT-2701..AT-2705 (US-2701) and AT-2706/AT-2707 (US-2702), one on-disk node each (DDR row 4); confirmed by `qa-reviewer`: `grep 'def test_AT_270'` over `tests/` → each of AT-2701..AT-2707 defined exactly once, each driven through the shipped `open_app` by keys (`enter`, `esc`, `q`, `right`, `A`, `B`, `@`, `#`, `e`, `/`), with the two non-key steps of AT-2706 noted (QA-P4-07)
- **Surface-reachability (bidirectional):** ⚠ 2 gaps, both minor — the `/` `#…` input half (G-002 / qa-m9, carried) and the identity picker's position on the deferred-start path (QA-P4-01); every other named input and output reached at the surface (`qa-reviewer`, matrix below)
- **Supersession inspection (read off the P3 packets):** ✓ all surviving refs negative — both packets' census rows: 5 probes each, 0 foreign hits (`increment-001.md` / `increment-002.md` §4 Reverse census)
- **Test ledger:** ✓ reconciles (`base − D + A = post`): 3236 − 0 + 13 = 3249 collected = 3248 passed + 1 skipped
- **Evidence checklist (qa-reviewer):** `qa-reviewer · 5 of 5 rows ✓ with evidence` (record rows) · agent checklist 11 items: 10 ✓, 1 n/a (§Evidence checklist below)

> The `qa-reviewer` rows were returned on 2026-10-25 (independent reviewer, P4); no row is left pending.

---

## Detail (reference)

### Layer 0 — unit

| Unit | Which criterion | Node id | Result |
|---|---|---|---|
| the `people.py` mtime/size gate | unchanged → None, same dict, 0 parses · same-size edit with moved mtime → True, 1 parse · size-only change with frozen mtime → True | `tests/test_directory_refresh.py::test_TC_2701_refresh_gates_on_mtime_or_size[people]` | passed (`p4-new-nodes.txt`, full run) |
| the same gate in `marks.py` | same three arms | `tests/test_directory_refresh.py::test_TC_2701_refresh_gates_on_mtime_or_size[marks]` | passed |
| failure record, people | corrupt → False and kept · again → None · fixed → True | `tests/test_directory_refresh.py::test_TC_2702_a_failed_refresh_keeps_and_flags_once[people]` | passed |
| failure record, marks | same | `tests/test_directory_refresh.py::test_TC_2702_a_failed_refresh_keeps_and_flags_once[marks]` | passed |
| the started-board record | written only by a completed start; a failed start stays pending; restore writes back the previous id | `tests/test_home_deferred_start.py::test_TC_2703_a_failed_deferred_start_keeps_the_board_pending` | passed |
| `SearchPrompt.on_directory_query` | fires once per prompt, including an initial `@`/`#` query, before that frame draws | `tests/test_directory_refresh.py::test_D3_the_search_query_refreshes_the_directories_once` | passed |

**Measured by mutation, never by line coverage.** For each unit, the mutation applied and the RED, as recorded at P3 (the batteries were not re-run at P4; the transcripts are the evidence):

| Unit | Mutation applied | RED observed? | Transcript |
|---|---|---|---|
| started-board record | E2 no record write; E4 record written before the migration gate | yes — E2 KILLED by AT-2702, AT-2703, TC-2703; E4 by TC-2703 | `evidence/mutation-001.txt` (24 arms, restore digest `89ff66cf…`) |
| deferred start | E1 `on_mount` home branch calls `_open_board(at_mount=True)` (the pre-HD-1 shape) | yes — KILLED by AT-2701, AT-2704, AT-2705 | `evidence/mutation-001.txt`; the F1 fold: `evidence/mutation-001b-f1.txt` (AT-2702 RED) |
| `action_back` | E3 pops without `_open_board()` | yes — KILLED by AT-2703 | `evidence/mutation-001.txt` |
| mtime/size gate | E1 no gate; E2 size arm dropped | yes — KILLED by TC-2701 (E1 also by TC-2702, AT-2707) | `evidence/mutation-002.txt` (30 arms) |
| failure keeps directory | E3 failure empties the dict; E4 no stamp advance | yes — KILLED by TC-2702, AT-2707 | `evidence/mutation-002.txt` |
| the four seats | E5 seats never refresh | yes — KILLED by AT-2706, AT-2707 | `evidence/mutation-002.txt` |
| search seat | E6 callback on every keystroke | yes — KILLED by the D3 node | `evidence/mutation-002.txt` |

### UX walkthrough — only if trigger family D fired

Trigger D1 fired (PLAN §Triggers). The criteria are driven through the REAL mechanism: the shipped `TaskboardApp` in a real Windows Terminal, keys played through `App._press_keys`, the end state asserted in-process before the grab (the READY file), the pixels kept. The DDR's `ux-reviewer` reviewed the design; the rows below are the P4 captures it asked for. The verdict column is left for the independent reviewer.

| Criterion (when the user does X, they observe Y) | Driven with the REAL mechanism | Painted result asserted | Verdict |
|---|---|---|---|
| At launch with several boards the user sees the boards home and nothing else: no modal, no toast, no write (ux-2, the quiet-home frame) | `shoot_real.py live home` in WT, 118x30 and 80x24 | READY `OK`: 0 toasts, the default board's bytes unchanged, no marker of this window; `home_118x30.png`, `home_80x24.png` | approved (`qa-reviewer`, read off both PNGs): the home and its two cards only — no modal, no toast; the key bar at 80x24 clips `q quit` to `q`, outside this batch's diff (QA-P4-05) |
| `enter` on the default board shows the milestone offer over that board, not over the home (ux-1) | `live offer` (`enter` through the key path) | READY `OK`: top screen `MilestoneOffer`, no `BoardsHome` on the stack, a board screen below; `offer_118x30.png`, `offer_80x24.png` | approved with note (`qa-reviewer`): the offer carries the `Personal` chip and the stack is right (READY + AT-2705); but the backdrop around the offer is empty at both sizes, and a `qa-reviewer` probe shows the same empty backdrop on the unchanged single-board start — D-12's visible symptom is not removed, only its cause (QA-P4-04) |
| `enter` with another window's fresh marker and a sweepable old task shows the open-twice warning AND the archived-old-work notice over the board (ux-2 worst-case stack; ux-M1) | `live start` | READY `OK`: exactly one of each title, the archive saved, the bytes changed; `start_118x30.png`, `start_80x24.png` | approved (`qa-reviewer`): the board paints beneath; `Archived old work` and `Boards · open twice` each shown once, legible at both sizes; at 80x24 they cover the Fitness lane's lower rows and the clock tail — toast overlay by design |

**Mechanism used:** `a UI test driver` — the real app in Windows Terminal driven through its own key path, plus the pixel capture (`evidence/captures/`).

| Act | What it is | Performed? |
|---|---|---|
| Automated walkthrough | the criteria above, driven through the REAL mechanism | performed — 6 shots, all on try 1 (`captures/png/capture-log.txt`) |
| Expert inspection | a cognitive walkthrough against declared criteria, by a reviewer and not a user | performed at the DDR by `ux-reviewer` (PASS with conditions, `design/DDR-2026-10-24-batch-02.md`); the P4 reading of the 6 captures performed by `qa-reviewer` (verdicts in the table above) |
| Evaluation with users | real users of the system, doing the tasks named in the context of use | not performed — single-operator tool; the operator reviews the captures at the merge decision |

- **Method:** three scenes at two sizes, each a fresh Windows Terminal window with a unique `h01-` title, a synthetic two-board home in a temporary folder, closed by title after its shot.
- **Participants or population:** none — no users; synthetic data only.
- **Evidence of the evaluation:** `.dev-flow/2026-10-24-batch-02/evidence/captures/` (`README.md`, `png/`, `png/capture-log.txt`, `shoot.ps1`, `shoot_real.py`, `assert-no-h01.ps1`).
- **Limits:** the board beneath the offer is not legible in the shot (the in-process READY check proves it); the `start` scene shows the two-toast stack, not the five-toast maximum (the other notices need their own preconditions); the footer clock is the machine's real clock; one machine, one terminal theme.

### Layer A — functional (white-box): per-requirement results

| Req | Method | Executed verification | Numeric threshold | Result | Evidence |
|-----|--------|-----------------------|-------------------|--------|----------|
| HLR-2701 | test | AT-2701 (with the `q` beat) | 0 open-twice notices, 0 own markers, the default board byte-identical | pass | `p4-new-nodes.txt`; full run |
| LLR-2701.1 | test | AT-2701 | as HLR-2701 | pass | same |
| LLR-2701.2 | test | AT-2701's `q` variant | as HLR-2701 | pass | same |
| HLR-2702 | test | AT-2702, AT-2703 | the deferred start runs exactly once on every path | pass | same |
| LLR-2702.1 | test | AT-2702, AT-2703, TC-2703 | the record is written only by a completed start | pass | same |
| LLR-2702.2 | test | AT-2702 (`enter`), AT-2703 (`esc`, `B`/`esc`) | once across paths | pass | same |
| LLR-2702.3 | test | AT-2702 (the same-board branch) | the start runs from the same-board early return | pass | same |
| LLR-2702.4 | test | TC-2703 | a failed start stays pending, retried on the next exit | pass | same |
| HLR-2703, LLR-2703.1 | test | AT-2704 | the default board's bytes equal; the old task not archived when another board is picked | pass | same |
| HLR-2704, LLR-2704.1 | test | AT-2705 | the offer is over the chosen board (stack assertions) | pass | same; `captures/png/offer_*` |
| HLR-2705, LLR-2705.1 | test | AT-2702's notice clause + the updated AT-2408/AT-2409 arms | notice byte-identical, fired at the start only | pass | same; `captures/png/start_*` |
| HLR-2706 | test | AT-2706 | the person, the class, the Select options and the `/` `@` completion all name the other window's additions | pass | same |
| LLR-2706.1, LLR-2706.2 | test (unit) | TC-2701 (people, marks) | 0 parses unchanged · 1 on mtime · 1 on size | pass | same |
| LLR-2706.3 | test | AT-2706 + the D3 node | the four seats and the search seat refresh before they show | pass | same |
| HLR-2707, LLR-2707.1 | test | AT-2707, TC-2702 (people, marks) | exactly one `People` warning, directory kept, no re-notify while bad | pass | same |
| HLR-2708, LLR-2708.1, LLR-2708.2 | test (regression pin) | the permitted-diff arms of `test_boards.py` and `test_boards_backlog_round.py` + the full suite | the named arms re-timed, not weakened; 0 failures across 111 files | pass | `suite-p4-chunk00..02.txt` |

### Layer B — behavioral (black-box) acceptance

| US | Acceptance test (`AT-NNN`) | Surface driven | Deliverable observed (path / element) | repr · boundary · negative | Result |
|----|----------------------------|----------------|---------------------------------------|----------------------------|--------|
| US-2701 | AT-2701 `test_AT_2701_the_home_touches_nothing` | the shipped app, `BoardsHome` first | no notice, no marker file, board bytes unchanged; `q` writes nothing | two boards · a default that is sweepable AND foreign-marked · nothing fires | pass |
| US-2701 | AT-2702 `test_AT_2702_enter_runs_the_deferred_start` | `enter` on the default card, plus the agenda/people jump | open-twice notice, marker, sweep, once | `enter` · five start paths · no second start | pass |
| US-2701 | AT-2703 `test_AT_2703_escape_runs_the_start_once` | `esc`, then `B`/`esc`; the `--open` arm | one start, none repeated | the re-entry runs nothing | pass |
| US-2701 | AT-2704 `test_AT_2704_another_board_never_writes_the_default` | pick the other board | the default's bytes equal, its old task un-archived | the default is never written | pass |
| US-2701 | AT-2705 `test_AT_2705_the_offer_opens_over_the_board` | `enter`, the `milestone_offer` seam | the offer over a board screen, no home beneath | one candidate board | pass |
| US-2702 | AT-2706 `test_AT_2706_the_directories_stay_fresh` | the other window adds a person and a class | `@`, `#`, `alt+m` Select, `/` `@` all name them | four seats | pass |
| US-2702 | AT-2707 `test_AT_2707_a_failed_re_read_keeps_the_directory` | corrupt the directory file | one warning, the directory kept | no re-notify | pass |

### Bidirectional surface-reachability matrix (extends A-5)

| Direction | US dimension / deliverable | Service param / producer | Reached/observed at surface? | TC / AT | Status |
|-----------|---------------------------|--------------------------|------------------------------|---------|--------|
| input | `enter` on a home card | `switch_board` same-board branch | yes | AT-2702 | ✓ |
| input | `esc` / back from the home | `BoardsHome.action_back` | yes | AT-2703 | ✓ |
| input | `q` from the home | quit | yes | AT-2701 | ✓ |
| input | another board's card | `switch_board` | yes | AT-2704 | ✓ |
| input | the agenda / people jump | `open_on_board` | yes | AT-2702 (fifth-path beat) | ✓ |
| input | `@` / `#` query, the `alt+m` Select, the people view, the marks manager | `_refresh_directories` | yes for `@`, `#` (manager), the editor's Select (options read, `alt+m` not pressed) and `/` `@`; the `/` `#…` half has no named assertion | AT-2706, D3 | ✓ / gap — minor (G-002 / qa-m9) |
| output | the identity picker over the board (HD-2) | `_init_team_mode` in the deferred start | no named node on the deferred-start path: AT-2705 has no team mode; AT-2408 asserts only the top screen after `B` → Course | AT-2408 (partial) | gap — minor (QA-P4-01) |
| output | the open-twice notice | `announce` + notify | yes (frame and toast) | AT-2702; `start_*` shots | ✓ |
| output | the archived-old-work notice | the sweep | yes | AT-2702; `start_*` shots | ✓ |
| output | the milestone offer over the board | `milestone_offer` | yes | AT-2705; `offer_*` shots | ✓ |
| output | the quiet home | `BoardsHome` | yes | AT-2701; `home_*` shots | ✓ |

### Signed-balance test ledger

| base | − D | + A | = post | actual collected | passed-lean / full | reconciles? |
|------|-----|-----|--------|------------------|--------------------|-------------|
| 3236 (batch-01: 3235 passed + 1 skipped) | 0 | 13 (6 + 7 collected nodes) | 3249 | 3249 (111 files, three disjoint chunks: 1440 + 954 + 855) | 3248 passed + 1 skipped (no lean/full split: no slow marker in use) | yes |

DDR row 5 expected 3246 by counting 11 node ids; the collected count is 13 because TC-2701 and TC-2702 are each parametrized over two directories. 3235 + 13 = 3248 passed, matching the run. The chunk file list (`suite-p4-files.txt`) equals `ls tests/test_*.py` (111 files), and no file appears in two chunks (checked with `sort | uniq -d`: 0).

### Gaps detected

| ID | Requirement | Gap | Severity | Proposed action |
|----|-------------|-----|----------|-----------------|
| G-001 | batch-01 carry | one skip: the clipboard arm (TC-1902) — the machine refuses `Set-Clipboard`. Environmental, accepted in the baseline. The transcript's summary line (`1 skipped`, chunk00) is the only per-skip record: the node was not itemized with `-rs`, so naming it TC-1902 is the baseline's attribution, not read off this transcript. **Itemized by `qa-reviewer`** (targeted re-run, not the gate run): `env -u NO_COLOR python -m pytest -q -rs tests/test_app.py tests/test_boards_move.py` on `32cafd3` → `199 passed, 1 skipped`, `SKIPPED [1] tests\test_app.py:1270: Set-Clipboard refused the sample on all 5 attempts (the machine, not the code under test)` — the TC-1902 clipboard roundtrip; the other skip sites of chunk00 (`test_boards_move.py:509/557`) ran | minor | discharge as environmental; the gate run itself still names no node (a `-rs` on the next gate run closes it in-transcript) |
| G-002 | HLR-2706 (m9 / qa-m9) | the `#` half of the search predicate has no named assertion; bounded by the shared per-seat call and the `#` manager/editor arms | minor | carried open (DDR condition below) |

### Escaped-bug regression (if a defect escaped the suite)

n/a — no defect escaped the suite in this batch. BACKLOG D-12 and A-7 are pre-image defects with their P1 RED probes at `base_ref` (`evidence/red-p1.txt`), not escapes.

### DDR conditions that land at P4

| # | Condition | Discharged? | The artifact line that proves it |
|---|---|---|---|
| ux-1 | P4 delivers the offer-over-board captures at 118x30 and 80x24 | discharged | `evidence/captures/png/offer_118x30.png`, `offer_80x24.png`; READY `OK` for both; `captures/README.md` §Results |
| ux-2 | the quiet-home frame and the worst-case toast-stack frame | discharged | `png/home_118x30.png`, `home_80x24.png` (quiet home) and `png/start_118x30.png`, `start_80x24.png` (open-twice + archived-old-work stack, READY `OK`); the stack is the two-toast one — see the captures README for the limit |
| qa-m9 | the `#` half of the search predicate has no named assertion — carried open | open (declared) — not closed at P4, carried to P5 / BACKLOG | G-002 above; `increment-002.md` §5 |

### Evidence checklist — qa-reviewer (full)

Returned by `qa-reviewer` (independent; it authored none of the batch). The record's five rows first, then the agent checklist (`agents/qa-reviewer.md`).

| # | Item | ✓/✗ | Evidence it reads |
|---|---|---|---|
| 1 | Gate suite counts read from the transcripts | ✓ — tails 1439+1s / 954 / 855, 0 failure lines; the 5 SHA-256 below recomputed and equal; `suite-p4-files.txt` = `ls tests/test_*.py` (111); no source differs between `8baf9ad` and `32cafd3` (`git diff --stat 8baf9ad HEAD -- . ':!.dev-flow'` empty); executor: the orchestrating chain | `suite-p4-chunk00..02.txt` tails (SHA-256 below) |
| 2 | Layer A rows reconcile to collected nodes | ✓ — 13 PASSED in `p4-new-nodes.txt`; re-executed by `qa-reviewer` on `32cafd3`: 28 passed (the 13 + the AT/TC arms of `test_boards_backlog_round.py`); count fix QA-P4-08 | `p4-new-nodes.txt` (13 passed) |
| 3 | Layer B: each AT in exactly one node, boundary + negative | ✓ — one `def` each; negatives present (AT-2701 nothing fires, AT-2704 default never written, AT-2702/2703 no second start, AT-2707 no re-notify); missing boundaries noted: QA-P4-02, QA-P4-03 | DDR row 4; the Layer B table |
| 4 | UX walkthrough verdicts on the captures | ✓ — 6 PNGs read; 3 verdicts above; QA-P4-04, QA-P4-05 | `evidence/captures/` |
| 5 | Ledger reconciliation and the skip's disposition | ✓ — 3236 − 0 + 13 = 3249 = 1440 + 954 + 855; the skip itemized (G-001) | the signed-balance table; G-001 |

**Agent checklist (`agents/qa-reviewer.md`), validation mode:**

| Item | ✓/✗ | Evidence |
|---|---|---|
| Acceptance criteria use Given/When/Then | n/a — P4 evaluates results | the ATs are statement + numeric threshold in `01-requirements.md` §3, fixed at P1/P2 |
| Test cases have explicit Expected | ✓ | each Layer A row carries a numeric threshold; each AT node asserts exact values (notice text, marker count, byte equality) |
| Edge cases include empty, boundary, invalid, error | ✓ with gaps | error: AT-2707, TC-2702, TC-2703; boundary size-only / mtime-only: TC-2701; missing: legitimate-empty re-read (QA-P4-03), `/ #…` (G-002) |
| Regression checklist exists | ✓ | HLR-2708 + the named permitted-diff arms; full gate run 0 failures |
| Exit criteria stated | ✓ | `01-requirements.md` §5.2 |
| No real PII / secrets | ✓ | synthetic fixture (`multi_board_fixture.py`), placeholder `username_subject`, temp homes |
| Mode declared | ✓ | `Mode: validation`, line 10 |
| Every case carries a result or a state, each executed result names its executor | ✓ | gate run: the orchestrating chain; the 13 nodes + arms and the `-rs` itemization: `qa-reviewer` (targeted, `32cafd3`); captures: the orchestrating chain (`capture-log.txt`); mutation batteries: executed at P3, consumed, not re-run |
| Layer B through the shipped surface, boundary + negative | ✓ | `open_app` + keys in every AT; real WT captures for the three UX scenes |
| Bidirectional surface-reachability | ✓ with 2 minor gaps | QA-P4-01, G-002 |
| No unfilled template | ✓ | no `PENDING qa-reviewer` left after this return |

### qa-reviewer findings

| ID | Severity | Finding | Evidence | Proposed action |
|---|---|---|---|---|
| QA-P4-01 | minor | HD-2's identity-picker half has no node on the deferred-start path. AT-2705 sets no team mode, so HLR-2704's "(and no identity picker)" clause holds vacuously; AT-2408 reaches the picker via `B` → Course and asserts only the top screen, not `BoardsHome` off the stack. Bounded: the same `_open_board` call pushes the picker before the offer, so the offer arm's ordering covers it structurally | `tests/test_home_deferred_start.py:252-269`; `tests/test_boards_backlog_round.py:139-144`; `taskboard/app.py` `_open_board` | one assertion (`BoardsHome` off the stack) in AT-2408's picker beat, or a team-mode arm in AT-2705 — BACKLOG |
| QA-P4-02 | minor | AT-2705 drives `esc`; HLR-2704's threshold names `enter`. The `enter` path to the offer is asserted only by the capture harness READY check (`live offer`) and a `qa-reviewer` probe, not by a suite node | HLR-2704 threshold; `test_AT_2705`, line 266 | parametrize AT-2705 over `enter` / `escape` — BACKLOG |
| QA-P4-03 | minor | HLR-2707's boundary "a re-read file that parses to an empty directory empties it with no notice" has no node (its boundary box is unchecked in `01-requirements.md`) | `01-requirements.md` HLR-2707 boundary catalog | one TC arm — BACKLOG |
| QA-P4-04 | minor (UX) | The offer's backdrop is empty at both sizes. A `qa-reviewer` probe (a temporary test file, removed; `export_screenshot` rows above the offer box) found 0 text rows above the box on the deferred `enter` path AND on the unchanged single-board start. So D-12's visible symptom ("an empty background") persists: HD-2 fixes the stack (board beneath, home gone), not what the user sees. Not a regression | `offer_118x30.png`, `offer_80x24.png`; probe result `{'home->offer': 0, 'single->offer MilestoneOffer': 0}` | the operator decides at merge whether D-12 closes on the stack fix or stays open for the offer's backdrop |
| QA-P4-05 | minor (out of scope) | The home's key bar at 80x24 clips `q quit` to `q` | `home_80x24.png`; the batch's `app.py` diff touches no key bar | BACKLOG, not this batch |
| QA-P4-06 | minor | The gate transcripts record neither the command line nor the commit; `8baf9ad` and the command are the record's statement. Mitigated: no non-`.dev-flow` file differs between `8baf9ad` and `32cafd3` | `suite-p4-chunk0?.txt` heads | next gate run: write the command and `git rev-parse HEAD` into each transcript |
| QA-P4-07 | minor | AT-2706 has two non-key steps: it sets `app.selected_task_id` and calls `refresh_view()` before `e`, and reads the `#f-mark` Select's options without pressing `alt+m` | `tests/test_directory_refresh.py`, AT-2706 | select by cursor keys and open the Select with `alt+m` — BACKLOG |
| QA-P4-08 | minor | The Requirements line counted 11 LLR; there are 15, all in Layer A | `grep -c '^### LLR-' 01-requirements.md` = 15 | corrected in this return |


### Evidence files

| Evidence artifact | Path | SHA-256 |
|---|---|---|
| gate suite, chunk 00 | `.dev-flow/2026-10-24-batch-02/evidence/suite-p4-chunk00.txt` | `4700c2dafe5dacd04042a003c30c8d4847121531bc29a6a3e79fbe4b2b2b9b9a` |
| gate suite, chunk 01 | `.dev-flow/2026-10-24-batch-02/evidence/suite-p4-chunk01.txt` | `a253429d626d325945dcbc1f8272f286c50d984af367f99e8c2d096f23936a62` |
| gate suite, chunk 02 | `.dev-flow/2026-10-24-batch-02/evidence/suite-p4-chunk02.txt` | `2a58542447e610ff6e272430f7866432798be51d26cd0ecd5a313f8bcda9b631` |
| chunk file list | `.dev-flow/2026-10-24-batch-02/evidence/suite-p4-files.txt` | `2bf2717da7c6c126d07fd6d5244fc4c41a69c6aa13df8aaa6cfb2aaa04bf6ab5` |
| new nodes, verbose run | `.dev-flow/2026-10-24-batch-02/evidence/p4-new-nodes.txt` | `ef8842f790f7ca14bc6d2308ea697f8bd5fef4a4f34306e9b9bdd8f0e811d764` |
| captures | `.dev-flow/2026-10-24-batch-02/evidence/captures/` | 6 PNGs + `capture-log.txt` (digests not recorded) |
