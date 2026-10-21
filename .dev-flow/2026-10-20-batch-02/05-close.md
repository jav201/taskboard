# Batch close — taskboard — Batch 2026-10-20-batch-02

> **Artifact language.** Canonical **English scaffold**; generate in the batch's language — the **prose**,
> and never a label.

> **Owed in.** `core` ✓ · `full` —

> **Field guide:** `templates/guides/close-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

> **Reserved field names.** The **field names and block keywords below are language-independent** — the
> validator parses them literally and they are never translated:
> `Conditional-gate discharge` · `New controls` · `Human perimeter` · `Human review ledger` · `Gated tree` · `Found before the batch` · `⏸ DEFER`
> **And the §6 DEPTH tokens — cell VALUES rather than field names, reserved for the same reason:**
> `light` · `rigorous` · `spot-check` · `none` · `✅` · `❌`. A CLOSED set, declared closed by the first
> revision that ships it — so the vocabulary a later promotion of `V54` to BLOCK will need already exists,
> instead of being introduced over a free-text field that six authors have by then written six ways.
> Everything else on this page — headings, guidance, the prose in every cell — is translated with the batch.
> **One strategy, not two:** the flow ships no alias table, so a translated label is read as an ABSENT one and the rule keyed on it reports a true-sounding silence.
> **And one FLOW-WIDE reserved token, read out of this artifact by `V42` no matter which template minted it:** `⏸ DEFER`. It is a MARKER rather than a field name, which is why it is stated here *and* in `/dev-flow` §Language of artifacts rather than in a per-template list — a deferral can be written in any batch artifact, including the ones that carry no block at all.

> **Notice convention.** `⚠` yellow = declare and continue · `✗` red = block · `✓` green = satisfied
> **with its citation**.

---

## 0 · Gate record — which tree this close gated

| Field | Value |
|---|---|
| Gate record | `python "C:/Users/jjgh8/.claude/skills/dev-flow/scripts/devflow-validate.py" .` from the project root · exit 0 · 0 block · 50 notice · 2026-10-20 |
| Gated tree | `f299cdad239d2a423f6a61a49f56ab41509df276` · dirty — .dev-flow/BACKLOG.md (the close record itself excluded) |
| Requirements canon | `REQUIREMENTS.md` (`repo:REQUIREMENTS.md`) — HLR-2301..2306 and LLR-2301.1..2306.2 folded (close step 1: 14 folded, 0 kept, 0 refused) |

---

## 1 · What changed

Two taskboards open at once no longer lose each other's boards, and a move can no longer overwrite what another taskboard just wrote into its target. Every registry write (create, rename/recolour, archive, `--board`, the opening recorded at start or at a switch) re-reads `boards.json` under a short lock file and applies only its own change; a move holds its target board's lock from its last check to the target's save, and keeps a byte copy of the source's `history.jsonl` beside it. A busy lock is said in the existing notices (`… is busy — another taskboard is writing it; try again in a few seconds (<lock path>)`), a stopped move no longer claims backups it never made, and `taskboard --board` with the registry busy exits with the message. An unarchived project never ties a presentation rank. `~` in the registry is the home the suite's seam names. The suite reads the screen where it shows the answer, and a hygiene law keeps the reviewers' findings fixed.

Mechanism: `boards.file_lock` (exclusive create with a token, owner-checked release, a stale lock taken over after 10 s, a 2 s bounded wait, a heartbeat) and `Registry._commit` (fresh read, set-aside of an unparseable file, in-place adoption) in `taskboard/boards.py`; `move_project`'s `ExitStack` lock and `_backup` of the history; `ProjectPicker._do_archive_toggle`'s rank rule and `_move_target(proj, bid)` in `taskboard/modals.py`; `__main__.main`'s exit.

| Requirement | Version | Verified by | Verdict |
|---|---|---|---|
| HLR-2301 / LLR-2301.1, LLR-2301.2 | LED .1–.2 | AT-2301 · TC-2301 ×9 | pass |
| HLR-2302 / LLR-2302.1 | LED .1–.2 | AT-2302 · TC-2302 ×4 | pass |
| HLR-2303 / LLR-2303.1 | LED .1–.2 | AT-2303 · TC-2303 ×3 | pass |
| HLR-2304 / LLR-2304.1 | LED .1–.3 | AT-2304 · TC-2304 | pass |
| HLR-2305 / LLR-2305.1 | LED .1–.2 | AT-2305 · TC-2305 | pass |
| HLR-2306 / LLR-2306.1, LLR-2306.2 | LED .1–.2 | AT-2306 · TC-2306 · the hardened AT-2204, AT-2104, AT-2106, AT-2102 | pass |

All in the Phase-4 gate run: 2962 passed, 0 failed, 0 skipped (`evidence/suite-p4-chunk00..02.txt`, the orchestrator).

---

## 2 · New controls discovered — and where they landed (C-45)

| Control | What failure it closes | Measured origin |
|---|---|---|

**The four landings — record which ones actually happened. Command-but-not-template is *half-encoded*, and the missing half is the enforceable one:**

| # | Landing | Done? | SHA / path |
|---|---|---|---|
| 1 | the **command** (`commands/…`) — the rule itself | n/a — no control minted | |
| 2 | its **artifact** (a template section) — a control with no output degrades to "I thought about it" | n/a — no control minted | |
| 3 | the **catalog** entry (`dev-flow-lessons`) with its measured origin | n/a — no control minted | |
| 4 | **committed and pushed**, manifest re-hashed and bumped | n/a — no control minted | |

- **New controls:** none — what this batch found was caught by controls the flow already has: the P2 lenses (A-1, the `~` fix at the wrong sites; QA-1, an AT green on the base; S-1, a registry written over without a copy), C-40's mutation battery (M20 survived once: the node was strengthened), and the DDR's re-read. A candidate for the operator's flow work, not minted here: a test that drives the live TUI through `main()` must stub `App.run` — one such node hung the RED run on the base for its whole timeout.

---

## 3 · Working-file reconciliation (C-44)

| File | State | Evidence |
|---|---|---|
| `taskboard/boards.py`, `taskboard/modals.py`, `taskboard/__main__.py` | ✅ committed on the local branch `fix/backlog-boards`; push and merge NOT authorized (the commission) — landing is the orchestrator's, on the operator's word | `d7c3dea`, `9cec898` |
| `tests/test_boards_concurrency.py` (new), `tests/test_hygiene.py` (new), `tests/test_present_all.py`, `tests/test_boards_home.py`, `tests/test_boards_forms.py` | ✅ committed on `fix/backlog-boards` | `d7c3dea`, `9cec898`, `e1c936d`, `0206fcd` |
| `docs/ARCHITECTURE.md`, `REQUIREMENTS.md` | ✅ committed on `fix/backlog-boards` | `a794b8c`, `0206fcd`; the canon in the deliverable commit |
| `.dev-flow/state.json`, `.dev-flow/2026-10-20-batch-01/decisions-log.json` (the rollover archive) | ✅ committed on `fix/backlog-boards` | `a794b8c`; the deliverable commit |
| `.dev-flow/2026-10-20-batch-02/**` (contract, ledger, review, design records, packets, validation, plan, evidence) | ✅ committed on `fix/backlog-boards` | the batch's commits; the deliverable commit (close step 6) |
| `.dev-flow/2026-10-20-batch-02/05-close.md`, `.dev-flow/BACKLOG.md` | ✅ committed on `fix/backlog-boards` | the close commit (close step 8) |
| the scratch worktree `…/scratchpad/wt-dev` | 🗑️ removed (`git worktree remove`); `git worktree list` holds it no more | this table |
| scratch drafts, fold scripts and probes in the session scratchpad | kept for the orchestrator's review; outside the repository | the hand-back |

- **Found before the batch:** `none — no tracked file was modified when the batch began`

The worktree was cut fresh from `main` (`b1b71e4`), so the main checkout's dirty `.gitattributes`, the two `inc001-brief.md` files and its untracked old `.dev-flow/*` files are not in this tree and were not touched. Worktrees found registered and left alone: `.claude/worktrees/{kanban-variants,kg-mejoras,present-e}`, `…/ds-units/name-taskboard`, `taskboard-wt/backlog-proto`.

### Conditional-gate discharge

- **Conditional-gate discharge:** 4 condition(s) · ✅ all discharged — the PDR's `approved with conditions` (PC-1..PC-4), re-read at the DDR (`design/DDR-2026-10-20-batch-02.md` §B).

| Condition | Discharged? | The artifact line that proves it |
|---|---|---|
| PC-1 QA-8's arm, QA-9's per-call asserts | ✓ | `tests/test_boards_concurrency.py::test_TC_2302_a_target_rewritten_while_the_move_waited_is_refused` (M14 KILLED, `evidence/mutation-001.txt`); `test_TC_2301_a_failed_write_changes_nothing` |
| PC-2 S-6, S-7, S-8 | ✓ | `03-increments/increment-001.md` §4b (security-reviewer APPROVE); `taskboard/boards.py` `file_lock`, `move_project` |
| PC-3 UX-8's node | ✓ | `test_TC_2301_a_busy_registry_at_start_is_a_message_not_a_traceback` (M19 KILLED) |
| PC-4 UX-9's wording | ✓ | `01-requirements.md` HLR-2304's title (LED .3) |

---

## 4 · Backlog reconciliation — the carry-over contract

| Item | Move | Reference |
|---|---|---|
| G-9 (`~` from the environment), the history without a pre-move copy, two instances unlocked, `_move_target`'s `_boards`, `test_boards_forms`'s `PAYLOADS`/`Text`/`_border_title`, AT-2204's `?` check (QA-03) | ✓ done | `BACKLOG.md` (marked `✓ done in 2026-10-20-batch-02`); `d7c3dea`, `9cec898`, `e1c936d` |
| AT-2104's tick row and `_all_cur` (G-2), `u` in view 2 (G-4), the archived project's tied `present_rank` (A-10) | ✓ done | `BACKLOG.md`; `9cec898`, `e1c936d` |
| a plain board save unlocked and the source history rewritten outside any lock; a team pull's unarchive; adoption by id (A-7); AT-2204's head-row check (G-1); the event-loop wait and the "busy" wording for an unwritable folder, with the visual round's notes | added | `BACKLOG.md` §*Open — after `2026-10-20-batch-02`* |
| every other item of the two sections and the earlier lanes | carried, unchanged | `BACKLOG.md` |

---

## 5 · Batch metrics — the 13 keys of `core`

Extract, do not invent: a key the artifacts did not record goes `null`, and the key is never dropped.

```yaml
type: dev-flow-batch
project: taskboard
batch_id: 2026-10-20-batch-02
mode: core
verdict: pass
increments: 3
source_files_max: 3              # increment 001 (declared in its packet's §2)
notices_raised: null             # PLAN.md declares NOTICEs per gate as ids and counts, not one id per line
rework_returns: 1                # P2 iterate-to-refine once (LED .2); review findings folded inside their increments and at the DDR
triggers_fired: "A2,A3,B1,B4,C5,C6,D1,E1"
tests_base_to_post: "2936 -> 2962"
new_control: none
open_items_next: 5               # the new BACKLOG section's items
```

---

## 6 · Human review ledger — what a human audited, at what depth

| Artifact | Machine verdict (citation) | Human review | Depth | Deliberately NOT reviewed |
|---|---|---|---|---|
| the commission (which backlog items, non-visual) | — | ✅ the operator's «Haz lo del backlog por favor.», scoped by the orchestrator, relayed 2026-10-20 | `light` | |
| `01-requirements.md` / ledger | P2 review (2 iterations), `V26` read | ❌ | `none — reviewed by the architect, qa, ux and security agents, not by a human` | |
| Code and tests | code-reviewer per increment (OK to advance ×3), security APPROVE at 001; 25 + 6 + 7 mutants KILLED, 26 + 7 at the DDR | ❌ | `none — agent review only` | not audited line by line |
| the Phase-4 gate run and `04-validation.md` | 2962 passed; qa-reviewer PASS-WITH-NOTES | ❌ | `none — run under the standing authorization` | the transcripts |

- **Human perimeter:** the operator owns whether to push and merge `fix/backlog-boards`; whether two windows editing one board should be locked too (a plain board save is not); the visual round's notices (a waiting indicator, "another taskboard is running"); the behaviour on a real second process and a network drive (simulated here by the shipped code acting from the test).
- **Human review ledger:** human:username_subject — 1 artifact(s) reviewed, 0 rigorous · 3 declared not-reviewed
