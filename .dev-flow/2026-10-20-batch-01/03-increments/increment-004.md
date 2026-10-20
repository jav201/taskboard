# Increment 004 — LLR-2206.1 · `moving a project to another board`

> **Artifact language**
> This template is the canonical **English scaffold**. Generate the artifact in the batch's development
> language — the **prose**, and never a label. **Where that language is declared:**
> `state.json`'s `language` key in `core` and `full`. The normative RULES below are
> language-independent.

> **Owed in.** `core` ✓ · `full` ✓

> **Field guide:** `templates/guides/increment-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

> **Reserved field names.** The **field names and block keywords below are language-independent** — the
> validator parses them literally and they are never translated:
> `SOURCE files` · `Instrument RED-proof` · `Correction population` · `Mutation verdicts` · `Emitted-form assertion` · `Reverse census` · `RED counterfactual` · `Independent review` · `Evidence files` · `Traces to` · `File` · `Kind` · `source` · `test` · `doc` · `config` · `generated` · `fixture` · `⏸ DEFER`
> Everything else on this page — headings, guidance, the prose in every cell — is translated with the batch.
> **One strategy, not two:** the flow ships no alias table, so a translated label is read as an ABSENT one and the rule keyed on it reports a true-sounding silence.
> **And one FLOW-WIDE reserved token, read out of this artifact by `V42` no matter which template minted it:** `⏸ DEFER`. It is a MARKER rather than a field name, which is why it is stated here *and* in `/dev-flow` §Language of artifacts rather than in a per-template list — a deferral can be written in any batch artifact, including the ones that carry no block at all.

> **Where this lives:** the **repo**, next to the diff it describes —
> `.dev-flow/2026-10-20-batch-01/03-increments/increment-001.md`. It is not synced to the vault.

> **Notice convention.** `⚠` yellow = notice: does not block, obliges you to DECLARE the reason here.
> `✗` red = block. `✓` green = satisfied **with its evidence cited**. A notice repeated for three
> consecutive batches becomes a rule or is retired.

> **A table you may delete.** A table whose `| **Field** |` row reads `none — <reason>`, or whose question one line of the gate checklist answers, may be deleted, its field row kept: `stations/core-runbook.md` §*A minimal increment packet* is a one-function change written that way.

| Field | Value |
|---|---|
| Batch | `2026-10-20-batch-01` |
| Increment | `004` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | `HLR-2206` / `LLR-2206.1` |
| Acceptance | `AT-2206` · white-box `TC-2206` · unit: the plan's link classification and its refusals (Layer 0, `TC-2206`) |
| Agent | `software-dev` (the orchestrator, self-implemented; drafted in a scratch worktree, ported here) |
| Date | `2026-10-20` |

---

## 1 · What changed

A project moves to another board. In the projects modal (`P`), `m` offers the cursor's project to the other active boards (`MoveTarget`: each with its colour, name, projects and open tasks); the chosen board is read with `peek_board`, `boards.move_plan` lists the tasks that move, the links kept inside and each crossing link, or refuses — the same file (by path or `samefile`), a missing or unreadable target, team mode on either side sharing the project or with an unreadable `team.json` (read fresh by `app.move_team_ids`), an id that cannot name a folder, an id or image folder the target holds, a phase the target lacks — with `<project> was not moved to <board>: <reason>.`; `MoveConfirm` shows the round's confirmation (the links scrolling, the head and keys always on screen) plus `u cannot undo a move or the edits before it — the backups are the way back.` Confirmed, `boards.move_project` works on deep copies — exclusive byte copies of both files (`<file>.pre-move-<date>[-N]`), the project (its presentation place cleared) and every task of it, the links inside kept and the crossing ones dropped, image references into a moved folder rewritten, the target written then the source (atomically), then the image folders (copied to a temporary name under the target's `images/`, renamed, removed from the source; only from the source's own `images/`), the history lines (appended to the target, the source rewritten), and `move-<date>.json` beside each board (a list; a non-list file left alone) — refusing a target changed since the plan (mtime and size). `app.after_move` opens the new source in place (the undo stack cleared); a failure after the source was written hands the new source over too, so the project is never saved back. The README gains a `## Boards` section, the data files and the command line rows; `BACKLOG.md` the batch's lane (option D OPTIONAL).

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/boards.py` | source | LLR-2206.1 | `MovePlan`, `move_plan`, `_refusal` (with the shared-folder refusal), `_backup`, `_log`, `_stamp`, `_samefile`, `_inside`, `move_project` |
| `taskboard/modals.py` | source | LLR-2206.1 | `MoveTarget`, `MoveConfirm`; `ProjectPicker` `m` and its title, `action_move_board` and callbacks |
| `taskboard/app.py` | source | LLR-2206.1 | `move_team_ids`, `after_move` |
| `taskboard/taskboard.tcss` | source | LLR-2206.1 | `MoveTarget`, `MoveConfirm` in the shared backdrop rule; their boxes |
| `tests/test_boards_move.py` | test | HLR-2206, LLR-2206.1 | new: TC-2206, AT-2206 |
| `README.md` | doc | HLR-2201, HLR-2202, HLR-2204, HLR-2205, HLR-2206 | `## Boards`; data files; command line; the `B` row links the section |
| `.dev-flow/BACKLOG.md` | doc | HLR-2206 | the batch's lane: done, option D OPTIONAL, the operator items, the review notes left open |
| `.dev-flow/2026-10-20-batch-01/evidence/capture.py` | doc | HLR-2204, HLR-2206 | the real-app captures of the shipped code (17 SVGs under `evidence/captures/`) |

| Count | Value |
|---|---|
| **SOURCE files** | **4 / 4** ⚠ — the move function, its two modals and `m`, the app's after-move hook and team ids, the modals' backdrop: the move cannot be reached, shown or adopted without all four (planned so at the PDR) |
| Test files | 1 (uncapped) |

## 3 · How to test

`python -m pytest -q -p no:cacheprovider tests/test_boards_move.py`; the battery: `python .dev-flow/2026-10-20-batch-01/evidence/mutate-004.py 004 0 10` and `… 004 14 99` (the first slice `004 0 14`); the captures: `PYTHONUTF8=1 python .dev-flow/2026-10-20-batch-01/evidence/capture.py <png dir>`.

## 4 · Test results

| Layer | Nodes | Result |
|---|---|---|
| 0, A and B | `tests/test_boards_move.py` — TC-2206 (29 nodes), AT-2206 (1) — 30 nodes | executed: 30 passed, 0 skipped (`-rs`: the hard-link and directory-link nodes ran) · targeted run of 44 test files, 1756 passed · `suite-004.txt` |
| full suite | not run at this increment: the host stopped increment 003's full run for memory and said not to start it again; the whole suite is owed at the P4 gate run | blocked |

| Field | Value |
|---|---|
| **RED counterfactual** | on increment 003's commit `6eefdac` (a clean worktree; the test file copied in) RED at collection — `move_plan` cannot be imported — a RED of absence; on `base_ref` the file cannot import `taskboard.boards` at all; the per-arm proof is the battery · `.dev-flow/2026-10-20-batch-01/evidence/red-004.txt` |
| **Mutation verdicts** | 28 mutants over 33 arms (one fresh run after the review folds, in two slices of the same harness on the same tree, arms 0–13 and 14–27, each restore proven by digest): a crossing link kept on the source side · KILLED; on the moving side · KILLED; an inside link dropped · KILLED ×2; a backup clobbering an earlier one · KILLED; the source saved before the target · KILLED; the live boards changed (no copies) · KILLED ×2; a refusal still writing · KILLED; references not rewritten · KILLED ×2; a traversal id accepted · KILLED; the target's team side ignored · KILLED; the same file accepted · KILLED; a stale target accepted · KILLED; a missing phase accepted · KILLED ×2; the source not handed over after its save · KILLED; the history lines left behind · KILLED ×2; the log overwritten · KILLED; `m` unbound · KILLED; the undo stack kept · KILLED; the trailing blank line of the links · KILLED (the capture comparison); the review folds — a shared folder accepted · KILLED; a hard-linked target accepted · KILLED; undecodable history bytes raising · KILLED; deep nesting raising · KILLED; a non-string task matched · KILLED; the newline lead dropped · KILLED; a non-OSError not handed over · KILLED; a linked image folder moved and its refs rewritten · KILLED; the picker's stale target used · KILLED · arms that stayed GREEN: none · `.dev-flow/2026-10-20-batch-01/evidence/mutation-004.txt` (harness `evidence/mutate-004.py`). Not armed: the folder-containment check before an image folder moves — unreachable once the id rule refuses every id that is not `[A-Za-z0-9_-]+` (S-1's guarantee is that rule, whose arm is killed) |
| **Instrument RED-proof** | 2 instruments: `evidence/mutate-004.py` (anchors once, edits applied; its twin for 003 reported a survivor); `evidence/capture.py` (its first draft run opened the wrong board for `move-…-6-client-after` — the frame showed Course · Docker — so it shows what it opens) |
| **Emitted-form assertion** | 4 artifacts: both board files (`json.loads` of their bytes), the `.pre-move` copies (their bytes against the bytes taken before `enter`), the move logs (`json.loads`), the confirmation as Textual exports it (`export_screenshot()` box rows against the round's capture rows) |
| **Reverse census** | 5 probes: B1 `grep -rln "ProjectPicker\|Projects\[/b\]\|move_board" tests/` → `test_markup_sites.py` (its `ProjectPicker` label site: the title stays an app literal — green), `test_archive.py`, `test_app.py` (the picker's `e`/`x`/`d` — green in the targeted run) · B2 the move relocates image folders and history lines at run time: the readers `Board.image_dir`, `task.images` (rewritten), `history.read` (the target's file) — AT-2206 reads each · B3 the round's `move-160-3-confirm.svg` is the confirmation's oracle (TC-2206) · B4 both board files, their copies, the logs — read by the app (`Board.load`) and the operator · A3 the interface rows amended at ARQ — 0 foreign hits |
| **Correction population** | none — no shipped assertion changed |

### Evidence files

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| suite-004.txt | .dev-flow/2026-10-20-batch-01/evidence/suite-004.txt | 888735badb59386b0d45bc6fdb5cf792e73d9c354a5fb1a9a11c1dec6b323cc9 |
| red-004.txt | .dev-flow/2026-10-20-batch-01/evidence/red-004.txt | 0aedcd3752dad39a50add150d5a47b68262a1006f0a385b87b904c248562f8f6 |
| mutation-004.txt | .dev-flow/2026-10-20-batch-01/evidence/mutation-004.txt | 773b6179999c93ed4061783c0b421db4c079d16eb1f67c9313bb5b5bb62e1977 |
| mutate-004.py | .dev-flow/2026-10-20-batch-01/evidence/mutate-004.py | 21ad30a578f8fc10687b7e685c09d2facc78951b88923c0fba6c1376ed92728a |
| inc004.diff | .dev-flow/2026-10-20-batch-01/evidence/inc004.diff | 509a3ff617b7943777fcc44721c5f9cf33b43dbf9f891e0254061061d631b8ee |
| capture.py | .dev-flow/2026-10-20-batch-01/evidence/capture.py | fcf94fafc3997a71085b00d4a13b82a6a7cc093cdd8f0a3617cd1f8fd1f20190 |

| Field | Value |
|---|---|
| **Evidence files** | 6 artifacts, each at the declared home with the digest of its stored bytes |

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` · first pass BLOCK-UNTIL F1 (two boards in one folder: the move erased the moved project's history lines), F2–F5 MEDIUM, F6–F7 LOW · all folded (shared-folder refusal; any error past the source save handed over; history read with `errors="replace"`, a str task, RecursionError caught; refs rewritten only into folders that move; the target re-read when chosen; the hard link tested; a newline lead) · re-review **PASS-WITH-NOTES**: F1 discharged by re-read, F2–F6 verified (30 passed, 33/33 killed), F7 record-only (LED .4), N1 LOW (README did not name the shared-folder refusal — folded), N2 LOW (`_move_target` keeps an unused `_boards` parameter — left open, recorded) · `security-reviewer` · first pass APPROVE-WITH-CONDITIONS (S-1, S-2 lifted at re-read; F1 stale target = code F4, F2 non-OSError, F3 `copytree(symlinks=True)`) · re-review **APPROVE**, N1 LOW informational (an undecodable byte in a kept history line returns as U+FFFD when the source history is rewritten; `history.jsonl` has no pre-move backup) — BACKLOG |

## 5 · Risks

A move between two app instances is not locked; undecodable bytes in a kept history line are rewritten as U+FFFD (no pre-move copy of `history.jsonl`) (the target is re-checked by mtime and size just before writing); a move fails part-way only after both files are written, and then the notice names what was done and the backups.

## 6 · Pending items / spec deviations

The full suite of this increment is owed at the P4 gate run (the host's memory reaper, increment 003). Spec deviation (code review F7): LLR-2206.1 named `MoveTarget`/`MoveConfirm` signatures that the code does not have (the code has `MoveTarget(project, n_tasks, entries, boards)` and `MoveConfirm(plan, project, src_board, src_entry, dst_entry, day)`); the LLR text is corrected at P3 with ledger entry LED .4, the code unchanged. Shipped beyond the LLR's refusal list after review: two boards in one folder are refused, and the target is re-read when it is chosen — both recorded in LED .4. Open LOW notes: code N2 (unused `_boards` parameter), security N1 (U+FFFD in kept undecodable history lines) — in BACKLOG.

## 7 · Suggested next task

The DDR, then Phase 4.

## Increment gate checklist

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | SOURCE budget | ⚠ | §2: 4 source files, the reason declared |
| 2 | Tests in this increment | ✓ | `tests/test_boards_move.py` |
| 3 | Layer 0 where it applies | ✓ | the plan's classification and refusals |
| 4 | RED counterfactual | ✓ | §4, `red-004.txt` (absence) + the battery |
| 5 | Reverse census | ✓ | §4: 5 probes, 0 foreign hits |
| 6 | `code-reviewer` passed | ✓ | §4b |
| 7 | No file from another lane | ✓ | one lane |
| 8 | Frozen interfaces untouched | ✓ | none frozen |
| 9 | Coverage verified on disk | ⚠ | `suite-004.txt` (targeted); the full run owed at P4 |
| 10 | Load-bearing emptiness | ✓ | the census's greps quoted |
| 11 | Mutation verdicts | ✓ | §4: 33/33 KILLED |
| 12 | Instrument RED-proof | ✓ | §4 |
| 13 | Correction population | ✓ | §4: none, declared |
| 14 | Emitted-form assertion | ✓ | §4 |
| 15 | Independent review | ✓ | §4b |
| 16 | Evidence files | ✓ | §4: the digests |
