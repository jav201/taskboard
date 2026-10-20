# Validation — taskboard — Batch 2026-10-20-batch-01

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

- **Result:** not-run — the Phase-4 gate run (C-25) has not run; owed by the orchestrator once the operator authorizes it. Proposed once it passes: `PASS-WITH-NOTES` (qa-reviewer); any failure → `FAIL` and `iterate-to-fix` (P3)
- **Gate run:** not-run — `python -m pytest -q -p no:cacheprovider -rs --color=no` in a clean worktree at `b88322d` is owed; it waits on the operator's go-ahead (the host's memory reaper stopped increment 003's run and said not to restart it unasked)
- **Layer 0:** 4 unit(s) met the criterion · 4 carry a named reddening mutation (the registry's load table, the slug and name rules, the due strip's day-and-cell choice, the move plan's link classification and refusals — all KILLED)
- **Requirements:** 12/12 executed at the targeted level (the orchestrator, per-increment runs; the qa-reviewer, the batch's four test files at `b88322d`: 117 passed) · 0 blocker fails · in the gate run: not-run (owed: the orchestrator)
- **Black-box acceptance (Layer B):** ⚠ every story's `AT` observes its outcome through the shipped surface (boundary + negative) — the six AT nodes executed (the orchestrator per increment; the qa-reviewer at `b88322d`); in the gate run: not-run
- **Surface-reachability (bidirectional):** ⚠ every named output observed at the surface; the move's refusals other than the id clash and the changed target driven at `move_plan`, not through the picker (G-1)
- **Supersession inspection (read off the P3 packets):** ✓ all surviving refs negative — each packet's B1 census re-ran green — full runs `suite-001.txt`, `suite-002.txt`; TARGETED runs `suite-003.txt` (391) and `suite-004.txt` (1756) that included the census files (the orchestrator); the round's committed files unchanged (`git diff --stat 783397e -- prototypes/multi_board` empty)
- **Test ledger:** ✓ reconciles at collection (`2819 − 0 + 117 = 2936`; `evidence/collect-p4.txt`, the orchestrator; confirmed by the qa-reviewer at `b88322d`); the passed count: not-run
- **Evidence checklist (qa-reviewer):** qa-reviewer — spawned with agents/qa-reviewer.md · 9 of 11 rows ✓ with evidence, 2 ✗ at review time (the states and executors — folded below; the unfilled Verdict line — folded); the gate run not-run

> If every line is ✓, the Detail below is reference only. Any ⚠/✗ → read the matching part.

---

## Detail (reference)

### Layer 0 — unit

| Unit | Which criterion | Node id | Result |
|---|---|---|---|
| `boards.Registry.load` (the load table) | decision — missing, unreadable, the entry rules, `last` | `tests/test_boards.py::test_TC_2201_*` | executed — the orchestrator (`evidence/mutation-001.txt`, not killed: 0) |
| `boards.slug` / `clean_name` | decision — ASCII, reserved names, the 60 cut, collisions | `tests/test_boards.py::test_TC_2201_*`, `tests/test_boards_forms.py::test_TC_2205_*` | executed — the orchestrator (`evidence/mutation-003.txt`) |
| `views.due_strip` | decision — the day and cell choice at five widths | `tests/test_boards_home.py::test_TC_2204_*` | executed — the orchestrator (`evidence/mutation-002.txt`) |
| `boards.move_plan` / `_refusal` | decision — the link classification and every refusal | `tests/test_boards_move.py::test_TC_2206_*` | executed — the orchestrator (`evidence/mutation-004.txt`) |

**Measured by mutation, never by line coverage.** For each unit, name the mutation and paste the RED:

| Unit | Mutation applied | RED observed? | Transcript |
|---|---|---|---|
| `Registry.load` | unreadable read without a copy · duplicate path · `archived` truthy | yes | `evidence/mutation-001.txt` |
| `slug` / `clean_name` | the reserved suffix dropped · the slug ignoring the disk · an empty name accepted | yes | `evidence/mutation-003.txt` |
| `due_strip` | the week past Sunday · late counted as next | yes | `evidence/mutation-002.txt` |
| `move_plan` | a crossing link kept (both sides) · an inside link dropped · a traversal id, the same file, a hard link, a shared folder, a missing phase accepted | yes | `evidence/mutation-004.txt` |

### UX walkthrough — only if trigger family D fired

| Criterion (when the user does X, they observe Y) | Driven with the REAL mechanism | Painted result asserted | Verdict |
|---|---|---|---|
| with several boards the app opens on the home, as the approved C | `open_app(None)` headless at 160×45, 118×30, 80×24 (AT-2204; `captures/home-*.svg`) | rows 0..h-2 equal the round's `C-*-open.svg`; the key row the shipped keys | executed — the orchestrator (`captures-p4.txt`: 17 same) |
| the open board is named in every view | AT-2203; `captures/switched-160x45.svg`, `switched-gantt-160x45.svg` | the chip first in the head row of views 1–9, 0; none in `R`; none with one board | executed — the orchestrator (`captures-p4.txt`: 17 same) |
| `n` creates a board and opens it | AT-2205; `captures/create-160x45-1-form.svg`, `-2-created.svg`, `create-80x24-form.svg` | the folder, the chip, the form's file line | executed — the orchestrator (`captures-p4.txt`: 17 same) |
| `P`, `m` moves a project and says what breaks | AT-2206; `captures/move-160x45-0..6`, `move-80x24-confirm.svg` | the picker, the confirmation's counts and dropped links, both files after, the notice | executed — the orchestrator (`captures-p4.txt`: 17 same) |
| one board: nothing changes | AT-2201; `captures/single-board-160x45.svg` | no chip, no home, no `boards.json` | executed — the orchestrator (`captures-p4.txt`: 17 same) |

**Mechanism used:** the real app headless (Textual `run_test`, keys through the pilot) — the ATs and `evidence/capture.py` (re-taken on the final code, `evidence/captures-p4.txt`); PNGs rendered with Edge.

| Act | What it is | Performed? |
|---|---|---|
| Automated walkthrough | the criteria above, driven through the REAL mechanism | performed — AT-2201..AT-2206 and `capture.py` |
| Expert inspection | a cognitive walkthrough against declared criteria, by a reviewer and not a user | performed at P2/PDR by the ux-reviewer (UX-1..UX-13 folded); not repeated at P4 |
| Evaluation with users | real users of the system, doing the tasks named in the context of use | not performed — a one-person team; the operator's verdict on the round (variant C) is the human check |

- **Method:** the shipped app headless over the round's four synthetic boards in a temporary home, keys through the pilot, frames read as text and as PNGs.
- **Participants or population:** none — no user evaluation.
- **Evidence of the evaluation:** `evidence/captures/` (17 SVG), `evidence/captures-p4.txt`; PNGs in the session scratchpad `png-mbimpl/`.
- **Limits:** no real terminal font; the board-switch latency on large boards not measured; no second app instance driven (the unlocked registry is a declared risk).

### Layer A — functional (white-box): per-requirement results

| Req | Method | Executed verification | Numeric threshold | Result | Evidence |
|-----|--------|-----------------------|-------------------|--------|----------|
| HLR-2201 | test | AT-2201, TC-2201 ×23 | the load table, no `boards.json` for one board, the `.corrupt` copy | executed — the orchestrator (per increment) + the qa-reviewer (targeted, `b88322d`, 117 passed); gate: not-run | `red-001.txt` (RED = ImportError at collection; per-assertion reddening from the batteries); `mutation-001.txt`, `mutation-ddr.txt` |
| HLR-2202 | test | AT-2202, TC-2202 ×12 | the per-board fields cleared, the timer stopped, `last` recorded, `--board` registered | executed — the orchestrator (per increment) + the qa-reviewer (targeted, `b88322d`, 117 passed); gate: not-run | `red-001.txt` (RED = ImportError at collection; per-assertion reddening from the batteries); `mutation-001.txt`, `mutation-ddr.txt` |
| HLR-2203 | test | AT-2203, TC-2203 ×12 | the head row exactly `w` at 30–160, the chip first, escaped | executed — the orchestrator (per increment) + the qa-reviewer (targeted, `b88322d`, 117 passed); gate: not-run | `red-002.txt`; `mutation-002.txt` |
| HLR-2204 | test | AT-2204, TC-2204 ×20 | the captures' rows, the strip, the seat blocked under the home | executed — the orchestrator (per increment) + the qa-reviewer (targeted, `b88322d`, 117 passed); gate: not-run | `red-002.txt`; `mutation-002.txt`, `mutation-ddr.txt` |
| HLR-2205 | test | AT-2205, TC-2205 ×15 | the folder and empty board, slugs, rollback on a failed save, archive keeps the folder | executed — the orchestrator (per increment) + the qa-reviewer (targeted, `b88322d`, 117 passed); gate: not-run | `red-003.txt` (RED = ImportError at collection; per-assertion reddening from the batteries); `mutation-003.txt`, `mutation-ddr.txt` |
| HLR-2206 | test | AT-2206, TC-2206 ×29 | both files, backups, logs, history, images and references; every refusal with nothing written | executed — the orchestrator (per increment) + the qa-reviewer (targeted, `b88322d`, 117 passed); gate: not-run | `red-004.txt` (RED = ImportError at collection; per-assertion reddening from the batteries); `mutation-004.txt`, `mutation-ddr.txt` |
| LLR-2201.1 | test (unit) | TC-2201 ×23 | the registry, `peek_board` | executed — the orchestrator (per increment) + the qa-reviewer (targeted, `b88322d`); gate: not-run | `evidence/mutation-001.txt` |
| LLR-2202.1 | test (unit) | TC-2202 ×12 | `open_app`, `switch_board` | executed — the orchestrator (per increment) + the qa-reviewer (targeted, `b88322d`); gate: not-run | `evidence/mutation-001.txt` |
| LLR-2203.1 | test (unit) | TC-2203 ×12 | `board_chip`, `header(..., chip=)` | executed — the orchestrator (per increment) + the qa-reviewer (targeted, `b88322d`); gate: not-run | `evidence/mutation-002.txt` |
| LLR-2204.1 | test (unit) | TC-2204 ×20 | `BoardsHome`, the card renders, `B` | executed — the orchestrator (per increment) + the qa-reviewer (targeted, `b88322d`); gate: not-run | `evidence/mutation-002.txt` |
| LLR-2205.1 | test (unit) | TC-2205 ×15 | `BoardForm`, `Registry.create/edit/archive` | executed — the orchestrator (per increment) + the qa-reviewer (targeted, `b88322d`); gate: not-run | `evidence/mutation-003.txt` |
| LLR-2206.1 | test (unit) | TC-2206 ×29 | `move_plan`, `move_project`, the modals | executed — the orchestrator (per increment) + the qa-reviewer (targeted, `b88322d`); gate: not-run | `evidence/mutation-004.txt` |

### Layer B — behavioral (black-box) acceptance

| US | Acceptance test (`AT-NNN`) | Surface driven | Deliverable observed (path / element) | repr · boundary · negative | Result |
|----|----------------------------|----------------|---------------------------------------|----------------------------|--------|
| US-2201 | AT-2201 — `tests/test_boards.py::test_AT_2201_no_registry_and_an_unreadable_one`; AT-2202 — `tests/test_boards_home.py::test_AT_2202_switching_boards_in_place` | `open_app(None)`, `--board`, the home's keys, `[` | `boards.json`, the `.corrupt` copy, each board's `history.jsonl`, the screen | repr: four boards · boundary: one board, an unreadable registry · negative: the base RED is a collection ImportError; the behavioural RED is the mutation kills (AT-2201 ×4, AT-2202 ×2) | executed — the orchestrator; the qa-reviewer re-ran at `b88322d`; gate: not-run |
| US-2202 | AT-2203 — `::test_AT_2203_the_chip_in_every_view`; AT-2204 — `::test_AT_2204_the_home` | views 1–9, 0, `R`, `B`, `3`, `a`, `P`, `?` at 160/118/80 | the head rows, the home's frame against the approved captures | repr: Client · Retail RAG · boundary: 80×24, one board · negative: RED on base (`red-002.txt`: 28 failed, 10 errors) | executed — the orchestrator; the qa-reviewer re-ran at `b88322d`; gate: not-run |
| US-2203 | AT-2205 — `tests/test_boards_forms.py::test_AT_2205_manage_boards_from_the_home` | `n`, `e`, `x`, `tab`, `enter` | the new folder and board, `boards.json`, the chip | repr: a new board · boundary: a blank name, the open board's archive refused · negative: the base RED is a collection ImportError; the behavioural RED is the mutation kills (AT-2205 ×5) | executed — the orchestrator; the qa-reviewer re-ran at `b88322d`; gate: not-run |
| US-2204 | AT-2206 — `tests/test_boards_move.py::test_AT_2206_move_a_project_to_another_board` | `P`, `m`, the picker, the confirmation | both board files, `.pre-move` copies, `move-<date>.json`, `history.jsonl`, `images/` | repr: Retail RAG · pilot · boundary: crossing links both ways · negative: every refusal (TC-2206); the base RED is a collection ImportError, the behavioural RED the mutation kills (AT-2206 ×7) | executed — the orchestrator; the qa-reviewer re-ran at `b88322d`; gate: not-run |

### Bidirectional surface-reachability matrix (extends A-5)

| Direction | US dimension / deliverable | Service param / producer | Reached/observed at surface? | TC / AT | Status |
|-----------|---------------------------|--------------------------|------------------------------|---------|--------|
| input | board count 1 / 4 | `Registry.single` | yes | AT-2201, AT-2204 | ✓ |
| input | registry missing / unreadable / valid | `Registry.load` | yes | AT-2201 | ✓ |
| input | widths 160, 118, 80 (pilot); 30–160 (renderer) | `header(..., chip=)`, `home_card` | yes at the three; 30–159 at the renderer | AT-2203, AT-2204, TC-2203 | ✓ |
| input | `--board PATH` | `open_app` | yes | AT-2202 | ✓ |
| input | the move's refusals | `move_plan` | at the picker for the id clash and the changed target; the rest at `move_plan` | TC-2206 | ⚠ G-1 |
| output | the chip, the home, the forms, the move modals | `board_chip`, `BoardsHome`, `BoardForm`, `MoveTarget`, `MoveConfirm` | yes | AT-2203..AT-2206 | ✓ |
| output | `boards.json`, board folders, `.pre-move` copies, `move-<date>.json`, `history.jsonl`, `images/` | `Registry.save`, `create`, `move_project` | yes, read from disk | AT-2201, AT-2205, AT-2206 | ✓ |

### Signed-balance test ledger

| base | − D | + A | = post | actual collected | passed-lean / full | reconciles? |
|------|-----|-----|--------|------------------|--------------------|-------------|
| 2819 (`suite-base.txt`, 2819 passed on `783397e`) | 0 | 117 (001: 36 · 002: 38 · 003: 16 · 004: 30 · DDR: −3, AT-2204's four nodes joined into one) | 2936 | 2936 (`pytest --collect-only`) | — / not-run (owed: the orchestrator) | yes at collection |

### Gaps detected
| ID | Requirement | Gap | Severity | Proposed action |
|----|-------------|-----|----------|-----------------|
| G-1 | HLR-2206 | the refusals other than the id clash and the changed target are driven at `move_plan`, not through the picker (their notice path is one shared `notify(markup=False)` call) | minor | accept |
| G-2 | HLR-2204 | AT-2204's `?` check reads the word `Boards`, not the `B` key; the node sets `selected_task_id` before `R` (QA-03) | minor | `BACKLOG.md` |
| G-3 | HLR-2206 | an undecodable byte in a kept history line returns as U+FFFD; `history.jsonl` has no pre-move copy (security N1) | minor | `BACKLOG.md` |
| G-4 | — | two app instances are not locked against each other (registry and move) | minor | `BACKLOG.md` (declared risk) |
| G-5 | — | the draft's Verdict block spliced `Result` into the template's guidance | major | fixed — the guidance restored, `Result` on its own line |
| G-6 | — | the draft wrote `pass` with no executor | major | fixed — the seven states and the executor on every row |
| G-7 | ledger | the `--collect-only` count had no transcript | minor | fixed — `evidence/collect-p4.txt` |
| G-8 | HLR-2201, HLR-2202, HLR-2205, HLR-2206 | the base REDs of increments 001, 003, 004 are collection ImportErrors, not per-assertion failures; per-assertion reddening rests on the batteries (every AT ≥ 2 kills) | minor | accept |
| G-9 | HLR-2201 | the suite's home seam patches `Path.home`; `Path(p).expanduser()` in `boards.py` reads `~` from the environment (no test writes a `~` path today — inspection, not a run) | minor | `BACKLOG.md` |
| GATE | all | the whole suite has not run since increment 002; the regression coverage of 003–004 outside the 44 targeted files rests on the gate run | blocker until run | the orchestrator runs it on the operator's go-ahead |


### Escaped-bug regression (if a defect escaped the suite)

none — no defect escaped the suite: the defects the reviews found (002 F1 `ago` on an aware time, 003 F1 no rollback, 004 F1 a shared folder erasing history) were caught before their gates, each with a node RED on the tree that had it (the batteries' arms).

### Evidence checklist — qa-reviewer (full)
> Attach `qa-reviewer`'s completed evidence checklist (items in `agents/qa-reviewer.md`), each marked ✓/✗ with one-line evidence. An unchecked or evidence-less item blocks the gate.

- ✓ Acceptance criteria use Given/When/Then — `01-requirements.md`:89 gives When/then for each AT, the Given as the threshold line's precondition (:149); prose, not labelled clauses.
- ✓ Test cases have explicit Expected — each AT and TC threshold names exact rows, files and counts (`01-requirements.md` §2).
- ✓ Edge cases cover empty, boundary, invalid and error — a blank name (AT-2205), 80×24 and one board (AT-2203/2204), an unreadable registry (AT-2201), every move refusal (TC-2206, `mutation-004.txt`).
- ✓ Regression checklist exists — the per-increment reverse census (DDR row 3), the 44-file targeted run (`suite-004.txt`); the full regression waits on the gate run.
- ✓ Exit criteria stated — `01-requirements.md` §5.2, seven criteria.
- ✓ No real PII or secrets — synthetic boards in a temporary home; the real `~/.taskboard` has no `boards.json` and nothing newer than 2026-10-08 (qa-reviewer, read-only).
- ✓ Mode declared — `**Mode:** validation`.
- ✗ → ✓ Every case carries one of the seven states and names its executor — folded (G-6); the gate row not-run, owed by the orchestrator.
- ✓ Layer B observed through the shipped surface — the real app from `open_app`, headless, keys through the pilot, the screen and the files on disk read, representative + boundary + negative; the gate re-run not-run.
- ⚠ → ✓ Bidirectional surface-reachability — every output observed at the surface; the move's other refusals reached at `move_plan` (G-1, accepted).
- ✗ → ✓ No unfilled template — the Verdict block repaired (G-5).
