# Validation — taskboard — Batch 2026-10-20-batch-02

> **Artifact language:** canonical English scaffold. Generate in the batch's development language (`state.json` `language`); for Spanish batches **translate the prose, never a label** — the reserved field names are declared in §✅ Verdict and are read literally.
> Phase 4 artifact. Content owner: `qa-reviewer`, who **EVALUATES** the results of the validation strategy fixed in Phase 1, **names who executed each one** and returns the rows; the orchestrator writes `04-validation.md` (`stations/shared-homes-roles.md` §Delegation). The ONE complete gate-suite run is the orchestrator's (`C-25`); a sub-agent consumes the result and never owns the run.

> **Owed in.** `core` ✓ · `full` ✓

> **Field guide:** `templates/guides/validation-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

**`Mode`:** `validation`

## ✅ Verdict (read first)


- **Result:** `PASS-WITH-NOTES`
- **Gate run:** `python -m pytest -q -p no:cacheprovider --color=no -rs <chunk files>` over `ls tests/test_*.py | sort` (97 files) in three sequential chunks · exit 0, 0, 0 · `0206fcd` (a clean worktree, 0 changed files, `NO_COLOR` unset) · the orchestrator — 1377 + 827 + 758 = 2962 passed, 0 failed, 0 skipped, equal to the 2962 collected (`evidence/suite-p4-chunk00..02.txt`, `evidence/suite-p4-summary.txt`, `evidence/collect-p4.txt`)
- **Layer 0:** 3 unit(s) met the criterion (`file_lock`, `_expand_home`, the unarchive rank rule; `_commit` by the boundary criterion) · 3 carry a named reddening mutation (M1–M6, M16, N1–N4)
- **Requirements:** 14/14 pass · 0 blocker fails
- **Black-box acceptance (Layer B):** ✓ every story's `AT` observes its outcome through the shipped surface (boundary + negative)
- **Surface-reachability (bidirectional):** ✓ all named inputs AND outputs/deliverables reached/observed at the surface
- **Supersession inspection (read off the P3 packets):** ✓ all surviving refs negative — each packet's B1 census green in its targeted run, and the whole suite green at the gate
- **Test ledger:** ✓ reconciles (`2936 − 0 + 26 = 2962`)
- **Evidence checklist (qa-reviewer):** `qa-reviewer · 14 of 14 rows ✓ with evidence` (an evaluation of the orchestrator's gate run; the qa-reviewer did not run the suite)


---

## Detail (reference)

Evaluated by `qa-reviewer` (a spawned agent with its role file) from the orchestrator's transcripts; the rows below are its return, written by the orchestrator. Each result's state: `executed`, by the orchestrator (the gate run, the REDs on the base, the batteries).

### Layer 0 — unit

| Unit | Which criterion | Node id | Result |
|---|---|---|---|
| `boards.file_lock` | decision (wait / stale / release / token) | `tests/test_boards_concurrency.py::test_TC_2301_the_lock_is_exclusive_and_released`, `…a_stale_lock_is_taken_over_and_a_fresh_one_is_not`, `…a_lock_whose_token_cannot_be_written_is_removed`, `…a_taken_over_holder_never_removes_the_new_lock` | pass |
| `boards._expand_home` | boundary (a path read from the registry) | `tests/test_boards_concurrency.py::test_TC_2305_tilde_is_the_seam_home` | pass |
| `ProjectPicker._do_archive_toggle`'s rank rule | decision (tie / no tie / no rank) | `tests/test_present_all.py::test_TC_2304_the_unarchive_rank_rule` | pass |

**Measured by mutation, never by line coverage.** For each unit, name the mutation and paste the RED:

| Unit | Mutation applied | RED observed? | Transcript |
|---|---|---|---|
| `file_lock` | M1 O_EXCL dropped; M2 release removed; M3 stale inverted; M4 `abs` dropped; M5 release not owner-checked; M6 token-less lock left | yes — KILLED ×6 | `evidence/mutation-001.txt`, `evidence/mutation-ddr-001.txt` |
| `_expand_home` | M16 `expanduser` back at `_key`; M17 the stored path raw | yes — KILLED ×2 | the same |
| the rank rule | N1 the rank kept on a tie; N2 always re-ranked; N3 archived ranks counted; N4 its own rank counted | yes — KILLED ×4 | `evidence/mutation-002.txt` |

### UX walkthrough — only if trigger family D fired

| Criterion (when the user does X, they observe Y) | Driven with the REAL mechanism | Painted result asserted | Verdict |
|---|---|---|---|
| when the operator creates a board while another taskboard holds the registry, they read `The board was not created: boards.json is busy …` and nothing changes | AT-2301 (Textual `run_test`, keys) | the notice's text; the files' bytes | pass |
| when a move's target is busy, they read `The move stopped: <board> is busy … Done: nothing.` with no backups claim | AT-2302 | the notice's text | pass |
| when the presenter unarchives a project whose rank was taken, view 3 lists it last | AT-2304 | view 3's timeline rows | pass |

**Mechanism used:** `a UI test driver` (Textual's headless `run_test`, the real app built by `open_app`/`TaskboardApp`)

| Act | What it is | Performed? |
|---|---|---|
| Automated walkthrough | the criteria above, driven through the REAL mechanism | performed |
| Expert inspection | a cognitive walkthrough against declared criteria, by a reviewer and not a user | performed — ux-reviewer at P2/PDR (UX-1..UX-9) |
| Evaluation with users | real users of the system, doing the tasks named in the context of use | not performed — a one-person team; the operator's own use after the batch |

- **Method:** the ATs above, in the gate run; the ux-reviewer's walkthrough of create/edit/archive/move/unarchive against the contract.
- **Participants or population:** none (no user evaluation).
- **Evidence of the evaluation:** `evidence/suite-p4-chunk00..02.txt`; `02-review.md` (UX-1..UX-9).
- **Limits:** two taskboards are simulated by the shipped `Registry` and lock files acting from the test, not two processes; no real user sat with the app.

### Layer A — functional (white-box): per-requirement results

| Req | Method | Executed verification | Numeric threshold | Result | Evidence |
|-----|--------|-----------------------|-------------------|--------|----------|
| HLR-2301 | test | AT-2301 | as in §3 | pass · RED on base · M7b, M8b KILLED | `red-001.txt`, `mutation-001.txt`, the gate run |
| LLR-2301.1 | test (unit) | TC-2301 (lock nodes) | as in §4 | pass · M1–M6 KILLED | the same |
| LLR-2301.2 | test (unit) | TC-2301 (registry nodes) | as in §4 | pass · M7–M10, M19–M21, M22 KILLED | `mutation-001.txt`, `mutation-ddr-001.txt` (26/26) |
| HLR-2302 | test | AT-2302 | as in §3 | pass · M13b, M18 KILLED | `mutation-001.txt` |
| LLR-2302.1 | test (unit) | TC-2302 | as in §4 | pass · M13–M15 KILLED (M14 the QA-8 arm) | the same |
| HLR-2303 | test | AT-2303 | as in §3 | pass · M11b KILLED | the same |
| LLR-2303.1 | test (unit) | TC-2303 | as in §4 | pass · M11, M12 KILLED | the same |
| HLR-2304 | test | AT-2304 | as in §3 | pass · RED on base (the tie, `pcp: 0`) · N1b KILLED | `red-002.txt`, `mutation-002.txt` |
| LLR-2304.1 | test (unit) | TC-2304 | as in §4 | pass · N1–N4 KILLED | the same |
| HLR-2305 | test | AT-2305 | as in §3 | pass · RED on base · M17 KILLED | `red-001.txt`, `mutation-001.txt` |
| LLR-2305.1 | test (unit) | TC-2305 | as in §4 | pass · M16 KILLED | the same |
| HLR-2306 | test | AT-2306 | as in §3 | pass · RED on 002's commit · H5–H7 KILLED | `red-003.txt`, `mutation-003.txt` |
| LLR-2306.1 | test (unit) | TC-2306 | as in §4 | pass · N5 KILLED | `red-002.txt`, `mutation-002.txt` |
| LLR-2306.2 | test | the hardened AT-2204, AT-2104, AT-2106, AT-2102 | as in §4 | pass · H1–H4 KILLED (and after the DDR folds) · `_all_cur` reads 14 → 12 | `mutation-003.txt`, `mutation-ddr-003.txt` |

### Layer B — behavioral (black-box) acceptance

| US | Acceptance test (`AT-NNN`) | Surface driven | Deliverable observed (path / element) | repr · boundary · negative | Result |
|----|----------------------------|----------------|---------------------------------------|----------------------------|--------|
| US-2301 | AT-2301 | `open_app`, the home's `n`, the name typed | `boards.json` lists `other-desk` and `fresh`; the home's two cards; no `*.lock` after exit | repr (another instance's board kept) · boundary (the lock removed after) · negative (the lock held: the notice, the bytes unchanged, no folder, the test's lock untouched) | pass |
| US-2301 | AT-2302 | `P`, `m`, the target, the confirmation | the notice `The move stopped: Client · Retail RAG is busy … Done: nothing.`; every file of the home byte-identical | repr (the retry moves) · boundary (no lock left) · negative (the busy target writes nothing) | pass |
| US-2302 | AT-2303 | `P`, `m`, the target, `enter` | `history.jsonl.pre-move-2026-10-20` holds the original bytes (`\xff\xfe` included); none in the target | repr · boundary (an undecodable byte) · negative (no copy in the target) | pass |
| US-2303 | AT-2304 | `R` `3` `shift+down`, `P` `x`, again, `P` `x`, `R` `3` | view 3 lists Customer Portal last; the file's ranks pairwise distinct | repr · boundary (a rank taken while archived) · negative (no tie) | pass |
| US-2304 | AT-2305 | the home's `right`, `enter` | the board view holds `Seam task`, not `Env task`; the environment's folder byte-identical | repr · boundary (`~/`) · negative (the environment's home never read) | pass |
| US-2304 | AT-2306 | the suite (`pytest`) | the hygiene law | repr · negative (H5–H7) | pass |

### Bidirectional surface-reachability matrix (extends A-5)

| Direction | US dimension / deliverable | Service param / producer | Reached/observed at surface? | TC / AT | Status |
|-----------|---------------------------|--------------------------|------------------------------|---------|--------|
| input | a board created / renamed / archived / registered | `Registry.create/edit/archive/register` | yes (the home's keys; `--board` through `main()`) | AT-2301, TC-2301 | ✓ |
| input | a move confirmed | `move_project` | yes (`P`, `m`, `enter`) | AT-2302, AT-2303 | ✓ |
| input | an unarchive | `_do_archive_toggle` | yes (`P`, `x`) | AT-2304 | ✓ |
| input | a `~` registry path | `Registry.load` / `_expand_home` | yes (the registry file, the home's `enter`) | AT-2305 | ✓ |
| output | `boards.json`, the lock files | `_commit`, `file_lock` | yes | AT-2301 | ✓ |
| output | both board files, `history.jsonl.pre-move-<date>` | `move_project`, `_backup` | yes | AT-2302, AT-2303 | ✓ |
| output | `present_rank` in the board file; view 3's order | `_do_archive_toggle`, `present_order` | yes | AT-2304 | ✓ |
| output | the notices | `BoardsHome._created`, `ProjectPicker._move_confirmed`, `__main__.main` | yes | AT-2301, AT-2302, TC-2301 | ✓ |

### Signed-balance test ledger

| base | − D | + A | = post | actual collected | passed-lean / full | reconciles? |
|------|-----|-----|--------|------------------|--------------------|-------------|
| 2936 | 0 | 26 | 2962 | 2962 | — / 2962 | yes |

### Gaps detected
| ID | Requirement | Gap | Severity | Proposed action |
|----|-------------|-----|----------|-----------------|
| G-1 | LLR-2306.2 | AT-2204's QA-12 fold checks that the presentation's head row names a project of the Personal board, not the project of the task `down` moved to | minor | `BACKLOG.md`: assert that specific project |
| G-2 | HLR-2301 | a plain board save still takes no lock (out of scope, §1.2) | minor | accepted; `BACKLOG.md` |
| G-3 | HLR-2301 | a stale lock can be taken over while its owner still writes past 10 s (§6.3) | minor | accepted |

### Escaped-bug regression (if a defect escaped the suite)

| Regression id (`AT-NNN` / `TC-NNN`) | Pre-fix run (evidence it FAILED) | Pre-fix RED kind (value / shape) | Post-fix value-discriminating? (QC-2) | Post-fix result | Reconciled node |
|-------------------------------------|----------------------------------|----------------------------------|----------------------------------------|-----------------|-----------------|
| none — no defect escaped the suite in this batch | | | | | |

### Evidence checklist — qa-reviewer (full)

In the qa-reviewer's return (P4): the chunk lists' 97 unique files equal `ls tests/test_*.py`; each chunk's exit 0; the total equals the collection; each requirement's RED and mutation transcript read; the evidence state and the executor named on each row.
