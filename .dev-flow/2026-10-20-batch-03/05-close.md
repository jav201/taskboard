# Batch close — taskboard — Batch 2026-10-20-batch-03

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
| Gate record | `<the validator command, the exit code THAT run printed, and 0 block · date>` |
| Gated tree | `<the 40-hex HEAD at the gate · clean — or: dirty — the files>` |
| Requirements canon | `REQUIREMENTS.md` (`repo:REQUIREMENTS.md`) — HLR-2401..2410 and LLR-2401.1..2410.2 folded (close step 1: 24 folded, 0 kept, 0 refused) |

---

## 1 · What changed

The backlog round's nine verdicted items are in the app. Every modal now has a direct key per button, written on the modal: a confirmation answers `y`/`n` with a key line under its whole (wrapped) message; forms with text fields take `alt+<letter>` (`alt+s` save, `alt+t`/`alt+d` the calendars, `alt+i` paste image), `esc` cancels, and a law over every `ModalScreen` keeps it so. The presentation opens its hint row with the board's chip, lists its keys from one seat with `?`, exports view 3 without the cursor and cut at its content, and reorders with `K`/`J`. The start-up modals name their board; opening a board another window holds says so once (presence markers under `~/.taskboard/open/`, stale after 120 s); `taskboard --open PATH` opens a board file without registering it. `A` shows every board's week in one read-only screen and `enter` opens a task on its board.

Mechanism: `keymap.key_line`, `PRESENT_KEYS`/`present_bindings`; `modals.ButtonKeysMixin.action_press_button`, `PresentKeys`, the forms' key lines (docked at the box's foot); `views.board_chip_text`, `present_all_export`, `all_agenda`/`render_all_agenda`; `app.AllBoardsAgenda`, `PresentScreen._hint`, the presence lifecycle; `boards.announce`/`renew`/`withdraw`/`open_elsewhere`; `__main__` `--open`.

| Requirement | Version | Verified by | Verdict |
|---|---|---|---|
| HLR-2401 / LLR-2401.1, LLR-2401.2 | LED .1–.3, .7, .8 | AT-2401 · TC-2401 ×5 | pass |
| HLR-2402 / LLR-2402.1 | LED .1–.3 | AT-2402 · TC-2402 | pass |
| HLR-2403 / LLR-2403.1, LLR-2403.2 | LED .1–.3, .5 | AT-2403 · TC-2403 | pass |
| HLR-2404 / LLR-2404.1 | LED .1–.3 | AT-2404 ×2 · TC-2404 | pass |
| HLR-2405 / LLR-2405.1 | LED .1–.3, .5, .8 | AT-2405 · TC-2405 | pass |
| HLR-2406 / LLR-2406.1 | LED .1–.4 | AT-2406 ×2 · TC-2406 · the inventory law | pass |
| HLR-2407 / LLR-2407.1 | LED .1–.4, .8 | AT-2407 ×2 · TC-2407 | pass |
| HLR-2408 / LLR-2408.1 | LED .1–.3 | AT-2408 · TC-2408 | pass |
| HLR-2409 / LLR-2409.1, LLR-2409.2 | LED .1–.3, .6 | AT-2409 · TC-2409 ×2 | pass |
| HLR-2410 / LLR-2410.1, LLR-2410.2 | LED .1–.3, .6, .8, .9 | AT-2410 · TC-2410 ×4 | pass |

All in the Phase-4 gate run: 3025 passed, 0 failed, 0 skipped (`evidence/suite-p4-chunk00..02.txt`, the orchestrator, at `8f0fe85`).

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

- **New controls:** none minted — the two escaped regressions (an increment-001 stylesheet order that failed TC-204, found by the DDR's targeted run, LED .8; an increment-003 notice in the second person, found by the P4 gate run's first pass, LED .9) were caught by controls the flow already has (the DDR's census run and the full gate run). A candidate for the operator's flow work, not minted here (qa G-1, G-2): a targeted run includes the project-wide source laws (`test_prism_laws.py`, `test_colour_budget_app.py`, the markup census) whenever an increment changes a printed string or a stylesheet. And a harness lesson, applied in this batch's capture script: a real-terminal capture closes its own window and verifies it is gone (`evidence/captures/png/capture-log.txt`).

---

## 3 · Working-file reconciliation (C-44)

| File | State | Evidence |
|---|---|---|
| `taskboard/keymap.py`, `modals.py`, `taskboard.tcss`, `views.py`, `app.py`, `boards.py`, `__main__.py` | ✅ committed on the local branch `feat/backlog-round`; push and merge NOT authorized (the commission) | `fab1206`, `5d50baa`, `b05799c`, `8ba1161`, `1647442`, `8f0fe85` |
| `tests/test_modal_keys.py`, `test_present_backlog_round.py`, `test_boards_backlog_round.py`, `test_all_agenda.py`, `backlog_round_fixture.py` (new); 9 suites updated by law | ✅ committed on `feat/backlog-round` | the same |
| `README.md`, `docs/ARCHITECTURE.md`, `REQUIREMENTS.md` | ✅ committed on `feat/backlog-round` | `ee7a285`, `8ba1161`, `1647442`; the canon in the close commit |
| `.dev-flow/state.json`, the rollover archive | ✅ committed | `cc8176c` and the batch's commits |
| `.dev-flow/2026-10-20-batch-03/**` (contract, ledger, review, design records, packets, validation, plan, evidence, captures) | ✅ committed on `feat/backlog-round` | the batch's commits; the close commit |
| `.dev-flow/2026-10-20-batch-03/05-close.md`, `.dev-flow/BACKLOG.md` | ✅ committed on `feat/backlog-round` | the close commit |
| the scratch worktrees `…/scratchpad/b03/wt-dev`, `wt-base`, `wt-p4` | 🗑️ removed at the close (`git worktree remove`) | the hand-back |
| the capture harness's synthetic homes (`%TEMP%\b03-cap-*`) | 🗑️ removed; the harness now removes each shot's own | `capture-log.txt` |

- **Found before the batch:** `none — no tracked file was modified when the batch began`

The worktree was cut from `fix/backlog-boards` with the round's prototype commit cherry-picked (`1fd667b`), so the main checkout's dirty `.gitattributes`, the two `inc001-brief.md` files and its untracked old `.dev-flow/*` files are not in this tree and were not touched. A misfire of the rollover script once wrote into `taskboard-wt/backlog-fix`; it was reverted there the same hour (declared in `PLAN.md`), and that worktree is clean. Worktrees left alone: `.claude/worktrees/{kanban-variants,kg-mejoras,present-e}`, `…/ds-units/name-taskboard`, `taskboard-wt/backlog-proto`, `taskboard-wt/backlog-fix`.

### Conditional-gate discharge

- **Conditional-gate discharge:** 5 condition(s) · ✅ all discharged — the PDR's `approved with conditions` (PC-1..PC-5), re-read at the DDR (`design/DDR-2026-10-20-batch-03.md` §B); PC-1's hand-over of the unverdicted key lines is this close's (§6).

| Condition | Discharged? | The artifact line that proves it |
|---|---|---|
| PC-1 real captures of the key lines the round never rendered | ✓ | `evidence/captures/png/` (`confirm_*`, `move-confirm_*`, `task-editor_*`, `project-form_*`, `clocks_*`, `identity_*`); UX-DDR-1/2 folded and re-shot |
| PC-2 `MoveConfirm` `enter` → `y` updates named | ✓ | `03-increments/increment-001.md` §2, §4 |
| PC-3 AT-2401's byte identity kept, its RED shown | ✓ | `tests/test_all_agenda.py::test_AT_2401_one_screen_for_every_board`; `evidence/mutation-ddr.txt` D4 KILLED |
| PC-4 security S-1..S-3 re-read | ✓ | `03-increments/increment-003.md` §4b (security-reviewer APPROVE) |
| PC-5 no black capture as evidence | ✓ | the ux-reviewer (DDR) and the qa-reviewer (P4) read the PNGs: none black |

---

## 4 · Backlog reconciliation — the carry-over contract

| Item | Move | Reference |
|---|---|---|
| the backlog round's nine items; ConfirmModal's clipped message (fixed by the confirm work) | ✓ done | `BACKLOG.md` §*Open — after `2026-10-20-batch-03`* (done lines); the batch's commits |
| the blank screen behind the start-up modals; the black window on `Personal`/`Course` in real Windows Terminal (logged, NOT fixed, as commissioned) | added | the same section |
| OPERATOR items: D-14 (`? keys` vs HLR-2002's 80-column wording), the unverdicted key lines (PC-1), a read-only `--open`, the dialog-keys standard for the other TUI repos, the `--open` notice's voice (LED .9) | added | the same section |
| code review CR-4 (the agenda's silent jump on an id-less file), CR-5 (001's inventory reads source text), QA-15, S-3 (`--report --board` pre-existing), the agenda's uncapped lanes, R-1/R-2, the DDR's ux minors UX-DDR-3..8 | added | the same section |
| every other item of the earlier sections | carried, unchanged | `BACKLOG.md` |

---

## 5 · Batch metrics — the 13 keys of `core`

Extract, do not invent: a key the artifacts did not record goes `null`, and the key is never dropped.

```yaml
type: dev-flow-batch
project: taskboard
batch_id: 2026-10-20-batch-03
mode: core
verdict: pass
increments: 4
source_files_max: 4              # increments 002 and 003 (declared in their packets' §2)
notices_raised: null             # PLAN.md declares NOTICEs per gate as ids and counts, not one id per line
rework_returns: 3                # P1 iterate-to-refine once (LED .2, .3); the DDR's folds (LED .8); the P4 second pass (LED .9)
triggers_fired: "A2,A3,B1,B4,C5,C6,C8,D1,E1"
tests_base_to_post: "2962 -> 3025"
new_control: none
open_items_next: 14              # the new BACKLOG section's open items
```

---

## 6 · Human review ledger — what a human audited, at what depth

| Artifact | Machine verdict (citation) | Human review | Depth | Deliberately NOT reviewed |
|---|---|---|---|---|
| the round's verdict (nine items, item 6's objection) | — | ✅ the operator's verdict on `prototypes/backlog_round/backlog-round.html`, relayed 2026-10-20 with «Haz lo del backlog por favor.» | `light` | |
| `01-requirements.md` / ledger | P2 review (2 iterations), `V26` read | ❌ | `none — reviewed by the architect, qa, ux and security agents, not by a human` | |
| Code and tests | code-reviewer per increment (OK to advance ×4), security APPROVE at 003; 17 + 16 + 24 + 15 + 7 mutants KILLED | ❌ | `none — agent review only` | not audited line by line |
| the real captures (`evidence/captures/png/`) | ux-reviewer at the DDR; qa-reviewer at P4 | ❌ | `none — handed to the operator as not yet verdicted (PC-1)` | the key lines the round never rendered |
| the Phase-4 gate run and `04-validation.md` | 3025 passed; qa-reviewer PASS-WITH-NOTES | ❌ | `none — run under the standing authorization` | the transcripts |

- **Human perimeter:** the operator owns whether to push and merge `feat/backlog-round`; the verdict on the key lines the round never rendered (the forms, the editor's last row, the confirmations — `evidence/captures/png/`); D-14; the `--open` notice's wording; whether the dialog-keys standard goes to the other TUI repos; the two logged visual defects.
- **Human review ledger:** human:username_subject — 1 artifact(s) reviewed, 0 rigorous · 4 declared not-reviewed
