# Increment 001 — <REQ-ID> · `<Short title>`

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
> `.dev-flow/2026-10-20-batch-02/03-increments/increment-001.md`. It is not synced to the vault.

> **Notice convention.** `⚠` yellow = notice: does not block, obliges you to DECLARE the reason here.
> `✗` red = block. `✓` green = satisfied **with its evidence cited**. A notice repeated for three
> consecutive batches becomes a rule or is retired.

> **A table you may delete.** A table whose `| **Field** |` row reads `none — <reason>`, or whose question one line of the gate checklist answers, may be deleted, its field row kept: `stations/core-runbook.md` §*A minimal increment packet* is a one-function change written that way.

| Field | Value |
|---|---|
| Batch | `2026-10-20-batch-02` |
| Increment | `001` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | `HLR-2301`, `HLR-2302`, `HLR-2303`, `HLR-2305` / `LLR-2301.1`, `LLR-2301.2`, `LLR-2302.1`, `LLR-2303.1`, `LLR-2305.1` |
| Acceptance | `AT-2301`, `AT-2302`, `AT-2303`, `AT-2305` · white-box `TC-2301`, `TC-2302`, `TC-2303`, `TC-2305` · unit: `file_lock`'s wait/stale/release paths, `_expand_home`'s forms, `_commit`'s fresh-or-copy and adoption (Layer 0, `TC-2301`, `TC-2305`) |
| Agent | `software-dev` (the orchestrator, self-implemented; drafted in a scratch worktree outside the branch, ported here after the PDR) |
| Date | `2026-10-20` |

---

## 1 · What changed

Two taskboards no longer lose each other's registry changes, and a move holds its target. `boards.file_lock(path, label=None)` takes `<resolved path>.lock` exclusively (a random token inside), retries every 0.05 s for `LOCK_WAIT` (2 s) and then raises `OSError("<label or name> is busy — another taskboard is writing it; try again in a few seconds (<lock path>)")`; a regular lock file more than `LOCK_STALE` (10 s) from now, past or future, unchanged at a second `lstat` (mtime and inode), is taken over; the lock is removed on exit only while it still holds its token; a token that cannot be written removes the lock; it yields a heartbeat. Every registry writer (`register`, `create`, `edit`, `archive`, `touch`) is now a change applied by `Registry._commit` to `boards.json` read fresh under that lock (`_read`, split out of `load`): a failed read raises with nothing written, unparseable bytes are set aside first (`_set_aside`: empty, the load's own copy, or `_keep_aside` now — else nothing written), then `save()`, then the result adopted in place (the same `BoardEntry` objects, memory-only entries kept). `move_project` holds `file_lock(target, target name)` from the stale-plan check to the target's save, renewing it after each copy, and copies the source's `history.jsonl` (streamed, `history.jsonl.pre-move-<date>`, a partial copy removed) with the board files. `~` in a registry path is normalised once at load through `Path.home()` (`_expand_home`; `_key`, `register` too). The stopped-move notice drops its backups sentence when nothing was done (`modals.py`), and `taskboard --board` with the registry busy exits 1 with the message (`__main__.py`).

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/boards.py` | source | LLR-2301.1, LLR-2301.2, LLR-2302.1, LLR-2303.1, LLR-2305.1 | `LOCK_WAIT`, `LOCK_STALE`, `_lock_token`, `file_lock`, `_expand_home`; `Registry._read`, `_commit`, `_set_aside`, `_carry`; `register`, `create`, `edit`, `archive`, `touch` as committed changes; `_backup` streamed; `move_project`'s lock and history copy |
| `taskboard/modals.py` | source | LLR-2302.1 | `ProjectPicker._move_confirmed`: the backups sentence only when `exc.steps` is not empty |
| `taskboard/__main__.py` | source | LLR-2301.2 | `main`: an `OSError` from `open_app` → `parser.exit(1, "taskboard: <reason>")` |
| `tests/test_boards_concurrency.py` | test | HLR-2301, HLR-2302, HLR-2303, HLR-2305, LLR-2301.1, LLR-2301.2, LLR-2302.1, LLR-2303.1, LLR-2305.1 | new: TC-2301 (9 nodes), AT-2301, TC-2302 (4), AT-2302, TC-2303 (3), AT-2303, TC-2305, AT-2305 — 22 nodes |
| `.dev-flow/2026-10-20-batch-02/evidence/mutate-001.py` | doc | HLR-2301, HLR-2302, HLR-2303, HLR-2305 | the increment's mutation battery |

| Count | Value |
|---|---|
| **SOURCE files** | **3 / 4** |
| Test files | 1 (uncapped) |

## 3 · How to test

`python -m pytest -q -p no:cacheprovider tests/test_boards_concurrency.py` (with `NO_COLOR` unset); the targeted set of `suite-001.txt`; the battery: `python .dev-flow/2026-10-20-batch-02/evidence/mutate-001.py` from the project root.

## 4 · Test results

| Layer | Nodes | Result |
|---|---|---|
| 0, A and B | `tests/test_boards_concurrency.py` — TC-2301, TC-2302, TC-2303, TC-2305, AT-2301, AT-2302, AT-2303, AT-2305 — 22 nodes | executed: 199 passed in the targeted run of the board, archive, markup-site, README and no-live-board files (`suite-001.txt`) |
| full suite | owed at the P4 gate run (three sequential chunks, the host's memory) | not-run |

| Field | Value |
|---|---|
| **RED counterfactual** | on `base_ref` `b1b71e4` (a clean worktree, `taskboard/` untouched, the test file copied in): 20 failed, 1 passed — the ATs RED for their stated reasons: AT-2301 `boards.json` lacks `other-desk` (the app wrote its memory over it), AT-2302 no `The move stopped` notice (the move ignored the lock), AT-2303 no `history.jsonl.pre-move-2026-10-20`, AT-2305 the board view lacks `Seam task` (the `~` entry read relative); the F5 node, added after the review, has its RED in arm M21; the passing node is the one-board no-write arm, true on the base too · `.dev-flow/2026-10-20-batch-02/evidence/red-001.txt` |
| **Mutation verdicts** | 25 arms over 21 mutants, one fresh run, each restore proven by digest: O_EXCL dropped · KILLED; the release removed · KILLED; the stale test inverted · KILLED; `abs` dropped (a future time) · KILLED; the release not owner-checked · KILLED; a token-less lock left · KILLED; the commit ignoring the file · KILLED ×2 (TC, AT-2301); the commit taking no lock · KILLED ×2 (TC, AT-2301); adoption replacing objects · KILLED; the copy-aside skipped · KILLED; the history copy removed · KILLED ×2 (TC, AT-2303); a partial copy kept · KILLED; the move taking no lock · KILLED ×2 (TC, AT-2302); the stale-plan check before the lock · KILLED (QA-8); the lock held past the target's save · KILLED; `expanduser` back at `_key` · KILLED; the stored path left raw · KILLED (AT-2305); the backups sentence always · KILLED (AT-2302); the busy start a traceback · KILLED; `create`'s id from memory and disk only · KILLED (code review F1: it SURVIVED the first fold's arm, so the node was strengthened and the arm re-run); `register` ignoring memory's ids · KILLED (F5) · arms that stayed GREEN: none · `.dev-flow/2026-10-20-batch-02/evidence/mutation-001.txt` (its `·` printed through the console code page) |
| **Instrument RED-proof** | 1 instrument: `evidence/mutate-001.py` — it refuses an anchor found other than once (`BAD`), proves each restore by SHA-256, and counts its arms (`arms: 25`); its own RED was seen: a first run reported `M6 … BAD (anchor found 0 times)` after the S-11 fold moved the anchor, and a second crashed on the console code page and was made to decode UTF-8 — both discarded, the third is the transcript; M20 SURVIVED once and is KILLED here |
| **Emitted-form assertion** | 4 artifacts: `boards.json` (`json.loads` of its bytes, and its bytes against those taken before), the lock files (their bytes: the test's marker kept, none left), `history.jsonl.pre-move-<date>` (its bytes against the history's), the board files (`json.loads`, and every file of the home hashed before/after a refused move) |
| **Reverse census** | 5 probes: B1 `grep -rln "Registry\|move_project\|registry\.\|The move stopped" tests/` → `test_boards.py`, `test_boards_forms.py` (`Registry.save` and `_unique_id` patched — green: the commit writes through `fresh.save()`, `create` picks its id with `self._unique_id`), `test_boards_move.py` (the steps of a move with no history and the stopped-move notice at line 294 — green), `test_boards_home.py`, `test_markup_sites.py` — all in `suite-001.txt`, 198 passed · B2 no file moves · B3 no golden capture renders a notice of this increment · B4 `history.jsonl.pre-move-<date>` and `*.lock` — read by the operator and by another instance's `file_lock` (AT-2302, AT-2303) · A3 the interface rows amended at ARQ (`docs/ARCHITECTURE.md` §4) — 0 foreign hits |
| **Correction population** | none — no shipped assertion changed |

### Evidence files

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| suite-001.txt | .dev-flow/2026-10-20-batch-02/evidence/suite-001.txt | 4672d78c046dc5a3806641e1545b1c9f6f3ca1d54aed2fc0ff527788c87e3e7b |
| red-001.txt | .dev-flow/2026-10-20-batch-02/evidence/red-001.txt | c13fc6ef867e4316a8e40ecde3adad0e5f91140d290565d0df26b62deae4834e |
| mutation-001.txt | .dev-flow/2026-10-20-batch-02/evidence/mutation-001.txt | ad6ea831b6b842f9c5b08be8fee964d3e7496ac93f0e03ba7c1e967a934f0a4c |
| mutate-001.py | .dev-flow/2026-10-20-batch-02/evidence/mutate-001.py | 0a2ee081e633350720a734363ab21e7545196d7810a7e6cb686c1d9d5092bae4 |
| inc001.diff | .dev-flow/2026-10-20-batch-02/evidence/inc001.diff | 9a2c8a8261f046350281bcd15b2daaa257b2f1c53c0baddb00970272f1e6e9db |

| Field | Value |
|---|---|
| **Evidence files** | 5 artifacts, each at the declared home with the digest of its stored bytes |

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` · first pass PASS-WITH-NOTES (F1, F2 MEDIUM — test strength and timing; F3–F6 LOW) · F1, F2, F5 folded (M20, M21 added) and re-read: **OK to advance** · no HIGH; F3, F6 accepted in §6.3; F4 declined with reason (TC-2205's injection reaches `self._unique_id`) · `security-reviewer` · first pass APPROVE (PC-2 discharged: S-6 `boards.py:118-125`, S-7 the `st_ino` re-check, S-8 a beat after each copy; S-10, S-11 LOW) · S-11 folded, S-10 closed by `_refusal`'s missing-target refusal (fails safe, `Done: nothing`) · re-read: **APPROVE**, no HIGH/MEDIUM, unlinks limited to `*.lock` and the copies this call created |

## 5 · Risks

A lock wait blocks the event loop for up to 2 s (§6.3); a plain board save takes no lock; the source history is rewritten outside any lock; a stale lock taken over while its owner still writes (narrowed by the token, the re-check and the heartbeat); an unwritable folder reads as busy (S-9).

## 6 · Pending items / spec deviations

The full suite is owed at P4. No spec deviation. PDR conditions PC-1 (QA-8's arm and QA-9's per-call asserts: `test_TC_2302_a_target_rewritten_while_the_move_waited_is_refused`, `test_TC_2301_a_failed_write_changes_nothing`), PC-2 (S-6, S-7, S-8: `file_lock`, `move_project`) and PC-3 (UX-8: `test_TC_2301_a_busy_registry_at_start_is_a_message_not_a_traceback`) are met in this increment and re-read by the reviewers (§4b): PC-1, PC-2, PC-3 discharged. Review notes left open: F3/S-9/A-8 (a permission error reads as busy) and F6/UX-6 (the event-loop wait), accepted in §6.3; A-7 → `BACKLOG.md` at the close.

## 7 · Suggested next task

Increment 002 — the unarchive rank and `_move_target(proj, bid)` (`taskboard/modals.py`).

## Increment gate checklist

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | SOURCE budget | ✓ | §2: 3 source files |
| 2 | Tests in this increment | ✓ | `tests/test_boards_concurrency.py` |
| 3 | Layer 0 where it applies | ✓ | `file_lock`, `_expand_home`, `_commit` |
| 4 | RED counterfactual | ✓ | §4, `red-001.txt` |
| 5 | Reverse census | ✓ | §4: 5 probes, 0 foreign hits |
| 6 | `code-reviewer` passed | ✓ | §4b: OK to advance, no HIGH; security APPROVE |
| 7 | No file from another lane | ✓ | one lane |
| 8 | Frozen interfaces untouched | ✓ | none frozen |
| 9 | Coverage verified on disk | ⚠ | `suite-001.txt` (targeted); the full run owed at P4 |
| 10 | Load-bearing emptiness | ✓ | the census's greps quoted |
| 11 | Mutation verdicts | ✓ | §4: 23/23 KILLED |
| 12 | Instrument RED-proof | ✓ | §4 |
| 13 | Correction population | ✓ | §4: none, declared |
| 14 | Emitted-form assertion | ✓ | §4 |
| 15 | Independent review | ✓ | §4b |
| 16 | Evidence files | ✓ | §4: the digests |
