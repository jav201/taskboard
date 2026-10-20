# Batch close — taskboard — Batch 2026-10-20-batch-01

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
| Gate record | `python "C:/Users/jjgh8/.claude/skills/dev-flow/scripts/devflow-validate.py" .` from the project root · exit 0 · no summary line · 2026-10-20 |
| Gated tree | `724cb7a7c4bfa1bed15a504e6e836b2c8b3489e9` · dirty — .dev-flow/2026-10-07-batch-08/evidence/inc001-brief.md, .dev-flow/2026-10-07-batch-09/evidence/inc001-brief.md, .gitattributes, .dev-flow/2026-10-07-batch-05/decisions-log.json, .dev-flow/2026-10-07-batch-06/decisions-log.json, .dev-flow/2026-10-07-batch-06/evidence/gen_verdict_sheet.py, .dev-flow/2026-10-07-batch-06/evidence/kanban-demo.json, .dev-flow/2026-10-07-batch-06/evidence/veredicto-batch06.html, .dev-flow/2026-10-07-batch-06/evidence/veredicto-board.json, .dev-flow/2026-10-07-batch-07/decisions-log.json, .dev-flow/2026-10-07-batch-08/decisions-log.json, .dev-flow/rollover_batchg.py, .dev-flow/rollover_batchh.py, .dev-flow/rollover_batchi.py, .dev-flow/rollover_batchj.py (the close record itself excluded) |
| Requirements canon | `REQUIREMENTS.md` (`repo:REQUIREMENTS.md`) — HLR-2201..2206 and LLR-2201.1..2206.1 folded (close step 1: 12 folded, 0 kept, 0 refused) |

---

## 1 · What changed

The operator can now keep several boards — one per project, discipline or personal list — instead of one mixed board. With more than one board the app opens on a home of board cards (variant C), `B` returns to it from any view, and every view's head row names the open board on its colour. On the home, `n` creates a board, `e` renames and recolours one, `x` archives another; `taskboard --board PATH` adds a file to the boards. In the projects modal, `P` then `m` moves a project with its tasks, history and images to another board, after a confirmation that lists the links it drops, with byte copies of both files first. A one-board user sees nothing new and gets no `boards.json`.

Mechanism: a registry `~/.taskboard/boards.json` (one folder per board, today's board as `Main` in place, read without failing, written atomically) in the new `taskboard/boards.py`; switching in place in `app.switch_board`; the chip through `header(..., chip=)`; the home a `Screen` with pure card renders in `views`; the move on deep copies, target saved before source, refusals on doubt.

| Requirement | Version | Verified by | Verdict |
|---|---|---|---|
| HLR-2201 / LLR-2201.1 | LED .1–.3 | AT-2201 · TC-2201 ×23 | pass |
| HLR-2202 / LLR-2202.1 | LED .1–.3 | AT-2202 · TC-2202 ×12 | pass |
| HLR-2203 / LLR-2203.1 | LED .1–.2 | AT-2203 · TC-2203 ×12 | pass |
| HLR-2204 / LLR-2204.1 | LED .1–.3 | AT-2204 · TC-2204 ×20 | pass |
| HLR-2205 / LLR-2205.1 | LED .1–.3 | AT-2205 · TC-2205 ×15 | pass |
| HLR-2206 / LLR-2206.1 | LED .1–.5 | AT-2206 · TC-2206 ×29 | pass |

All in the Phase-4 gate run: 2936 passed, 0 failed, 0 skipped (`evidence/suite-p4-chunk00..02.txt`, the orchestrator).

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

- **New controls:** none — what this batch found was caught by controls the flow already has: C-18 (AT-2204 realised in parts, found at the DDR), C-40 (the §5 AT-row mutations armed late, QA-01), the code and security reviews (the shared-folder history loss, the stale target). Candidate for the operator's flow work, not minted here: the packet's mutation list should name the node that killed each mutant, so an AT-row mutation killed only at a TC is visible at the increment gate rather than at the DDR (qa QA-01).

---

## 3 · Working-file reconciliation (C-44)

| File | State | Evidence |
|---|---|---|
| `taskboard/boards.py` (new), `taskboard/app.py`, `taskboard/__main__.py`, `taskboard/models.py`, `taskboard/views.py`, `taskboard/keymap.py`, `taskboard/modals.py`, `taskboard/taskboard.tcss` | ✅ committed on the local branch `feat/multi-board`; landing (push and merge) by the orchestrator on the operator's word «si todo pasa haz push y merge» | `e522eac`, `dc643e4`, `6eefdac`, `9ddabe8` |
| `tests/test_boards.py`, `tests/test_boards_home.py`, `tests/test_boards_forms.py`, `tests/test_boards_move.py`, `tests/multi_board_fixture.py`, `tests/conftest.py`, the law-driven `tests/test_colour_budget_app.py`, `tests/test_report.py` | ✅ committed on `feat/multi-board`; landing by the orchestrator | the increment commits; `b88322d` (AT-2204 joined) |
| `prototypes/multi_board/**` (the round, cherry-picked from `74bbe4d`) | ✅ committed on `feat/multi-board` as `783397e` (the batch's `base_ref`), unchanged since | `git diff --stat 783397e -- prototypes/multi_board` empty |
| `README.md`, `docs/ARCHITECTURE.md`, `REQUIREMENTS.md` | ✅ committed on `feat/multi-board`; landing by the orchestrator | `9ddabe8`, `b88322d`; the canon in the deliverable commit |
| `.dev-flow/state.json`, `.dev-flow/2026-10-19-batch-01/decisions-log.json` (the rollover archive) | ✅ committed on `feat/multi-board` | `ff1f023`; the deliverable commit |
| `.dev-flow/2026-10-20-batch-01/**` (contract, ledger, review, design records, packets, validation, plan, evidence: transcripts, batteries, captures) | ✅ committed on `feat/multi-board` | the batch's commits; the deliverable commit (close step 6) |
| `.dev-flow/2026-10-20-batch-01/05-close.md`, `.dev-flow/BACKLOG.md` | ✅ committed on `feat/multi-board` | the close commit (close step 8) |
| scratch worktrees `…/scratchpad/wt-dev`, `wt-base`, `wt-prev`, `wt-seam`, `wt-p4` | 🗑️ removed (`git worktree remove`, `git worktree prune`); `git worktree list` holds none of them | this table |
| scratch drafts, fold scripts, diffs and the PNGs in the session scratchpad (`png-mbimpl` is the commission's PNG folder; `suite-p4/` the orchestrator's run, copied into evidence) | kept for the orchestrator's review; outside the repository | the hand-back |

- **Found before the batch:** `.dev-flow/2026-10-07-batch-08/evidence/inc001-brief.md @ a751d73fdcddc239d01f02a2dfcb9ec042222110` `.dev-flow/2026-10-07-batch-09/evidence/inc001-brief.md @ 737b913e5559b8337969790137c4bda87fac2788` `.gitattributes @ 5650216ed19fb4d68b5ae282a0bd5042024dc222`

Also found before the batch, untracked and left alone: `.dev-flow/2026-10-07-batch-0{5,6,7,8}/decisions-log.json`, `.dev-flow/2026-10-07-batch-06/evidence/{gen_verdict_sheet.py,kanban-demo.json,veredicto-batch06.html,veredicto-board.json}`, `.dev-flow/rollover_batch{g,h,i,j}.py`. Worktrees found registered and left alone: `.claude/worktrees/{kanban-variants,kg-mejoras,present-e}`, `…/ds-units/name-taskboard`.

### Conditional-gate discharge

- **Conditional-gate discharge:** 5 condition(s) · ✅ all discharged — the PDR's `approved with conditions` (PC-1..PC-5): PC-4 and PC-5 at the seal, PC-1..PC-3 re-read at the DDR (`design/DDR-2026-10-20-batch-01.md` §B), PC-3 after QA-01's arms.

| Condition | Discharged? | The artifact line that proves it |
|---|---|---|
| PC-1 the key-bar words `B Boards` costs, per width and layer | ✓ | `evidence/keybar-words.txt` lines 3–54, cited from `03-increments/increment-002.md` §4 |
| PC-2 `BLOCK-UNTIL: S-1, S-2` at increment 004 | ✓ | `03-increments/increment-004.md` §4b (security-reviewer APPROVE); `tests/test_boards_move.py:98-132, 235-298, 367-387`; `tests/test_markup_census.py` |
| PC-3 the §5 mutations killed per increment | ✓ after QA-01 | `evidence/mutation-001..004.txt`; `evidence/mutation-ddr.txt` (9 AT-row arms, 9/9 KILLED) |
| PC-4 the conftest seam's blast radius | ✓ at the seal | `evidence/suite-seam.txt` (2819 passed) |
| PC-5 the frames oracle re-rendered at `783397e` | ✓ at the seal | `evidence/frames_base.py` docstring |

---

## 4 · Backlog reconciliation — the carry-over contract

| Item | Move | Reference |
|---|---|---|
| several boards, not one mixed board (the operator's request; variant C, P1–P4) | ✓ done | `e522eac`, `dc643e4`, `6eefdac`, `9ddabe8` |
| option D, an "all boards" agenda | added — OPTIONAL | `BACKLOG.md` |
| no chip in the presentation (D3); `--board PATH` registers the path | added — OPERATOR | `BACKLOG.md` |
| `ConfirmModal`'s focused box (`tab`, `enter`); start-up modals over the home (UX-5); the due strip under 40 columns; `enter` on an unreadable card | added | `BACKLOG.md` |
| the review notes left open: 003 N1/N2 (`test_boards_forms.py`), 004 N2 (`_move_target`'s unused `_boards`), security N1 (U+FFFD, no history backup) | added | `BACKLOG.md`; the packets' §4b |
| QA-03 (AT-2204's `?` check), G-9 (`expanduser` beside the home seam), two instances unlocked | added | `BACKLOG.md`; `04-validation.md` |
| the earlier lanes' items | carried, unchanged | `BACKLOG.md` |

---

## 5 · Batch metrics — the 13 keys of `core`

Extract, do not invent: a key the artifacts did not record goes `null`, and the key is never dropped.

```yaml
type: dev-flow-batch
project: taskboard
batch_id: 2026-10-20-batch-01
mode: core
verdict: pass
increments: 4
source_files_max: 4              # every increment (declared in each packet's §2)
notices_raised: null             # PLAN.md declares NOTICEs per gate as ids and counts, not one id per line
rework_returns: 2                # P1/P2 iterate-to-refine twice (LED .2, .3); review HIGHs folded inside their increments
triggers_fired: "A1,A2,A3,B1,B2,B3,B4,C1,C5,C6,C8,D1,E1"
tests_base_to_post: "2819 -> 2936"
new_control: none
open_items_next: 14              # the 2026-10-20-batch-01 lane
```

---

## 6 · Human review ledger — what a human audited, at what depth

| Artifact | Machine verdict (citation) | Human review | Depth | Deliberately NOT reviewed |
|---|---|---|---|---|
| the multi-board round (the design) | the round's captures and verdict page | ✅ the operator's verdict «VARIANTE ELEGIDA: C · Sin objeciones: acepto P1–P4 como están», relayed by the orchestrator, 2026-10-20 | `light` | |
| the Phase-4 gate run | 2936 passed (`suite-p4-chunk00..02.txt`) | ✅ the operator's go-ahead to run it («Puedes tú correr las pruebas?»), relayed by the orchestrator | `none — authorised, not read` | the transcripts |
| `01-requirements.md` / ledger | P2 review (3 iterations), `V26` read | ❌ | `none — reviewed by the architect, qa, ux and security agents, not by a human` | |
| Code and tests | code-reviewer per increment (three BLOCK-UNTIL, resolved), security APPROVE at 004; 22 + 27 + 23 + 33 + 12 mutants KILLED | ❌ | `none — agent review only` | not audited line by line |
| `04-validation.md` and the captures | qa-reviewer PASS-WITH-NOTES (proposed, then the gate run passed) | ❌ | `none — the captures are produced for the operator's look` | |

- **Human perimeter:** the operator owns whether the presentation should name the board (D3), whether `--board` should register a copy, option D, the board layout on a real terminal font (no user evaluation was run), and running two app instances at once (not locked).
- **Human review ledger:** human:operator — 2 artifact(s) reviewed, 0 rigorous · 3 declared not-reviewed
