# Batch close — taskboard — Batch 2026-10-24-batch-01

> **Artifact language.** Canonical **English scaffold**; generate in the batch's language — the **prose**,
> and never a label.

> **Owed in.** `core` ✓ · `full` —

> **Field guide:** `templates/guides/close-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

> **Reserved field names.** The **field names and block keywords below are language-independent** — the validator parses them literally and they are never translated:
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
| Gate record | `python "C:/Users/jjgh8/.claude/skills/dev-flow/scripts/devflow-validate.py" --brief .` from the project root · exit 0 · 0 block · 2026-10-24 (`evidence/gate-p5.txt`) |
| Gated tree | `4a12f07` (the Phase-4 commit) + the close's own writes, committed together as the close commit |
| Requirements canon | `REQUIREMENTS.md` (`repo:REQUIREMENTS.md`) — HLR-2601..2608 and LLR-2601.1..2608.2 folded (close step 1: 25 folded, 0 kept, 0 refused) |

---

## 1 · What changed

The milestone-marks round is in the app, as the operator's verdict chose. One directory of milestone classes (name, shape, colour, hidden) at `~/.taskboard/marks.json` serves every board. A milestone's editor gains the class Select after `#f-milestone` (`alt+m`, the round's variant A). `#` opens the MarksManager — the classes each as their shape in their colour with live counts, `n` a MarkForm (name, shape, colour, live preview), `␣` hiding a class from the gantt and the presentation (the strip counts it `N hidden`). Every milestone mark renders through one seat, `views.milestone_mark(task, board, today)`: the class glyph in its colour, the late date in `over` with the `▲Nd` chip, reached milestones the hollow twin with `✓`, unclassified the plain `◆`. A legend strip under the gantt and presentation rulers names the drawn classes; `/#cls` filters the kanban or the gantt to one class, the bar naming it; `?`, the details line and the README name the classes.

Mechanism: `marks.Directory` (the `people.py` pattern: `file_lock` + `write_atomic` read-modify-write, the `.corrupt` keep-aside, LED .29/.40 validation, `SHAPES`/`COLOURS`, prefix-only `find`, `handle_for` reused); `models.Task.mark` written only when set, `Board.marks` the app's one live dict, never saved; `views.milestone_mark` + `render_marks` (the ARQ's A-1 fold), `legend_strip`/`legend_strip_project`, `_hide`/`present_tasks_m`, `matches_m`/`filter_bar_m`; `modals.TaskModal`'s Select and `MarkForm`; `app.MarksManager`; `keymap`'s `#` (addition only). 14 full-colour captures (`evidence/captures/png/`) are the visual confirmation, all seven scenes at 118×30 and 80×24.

| Requirement | Version | Verified by | Verdict |
|---|---|---|---|
| HLR-2601 / LLR-2601.1, LLR-2601.2, LLR-2601.3 | LED .1 + .29, .30, .39, .40, .44 | AT-2601 · AT-2602 · TC-2601 · TC-2603 | pass |
| HLR-2602 / LLR-2602.1, LLR-2602.2 | LED .2, .12 | AT-2607 · TC-2602 | pass |
| HLR-2603 / LLR-2603.1, LLR-2603.2 | LED .3 + .14, .15, .36 | AT-2602 · TC-2603 | pass |
| HLR-2604 / LLR-2604.1, LLR-2604.2 | LED .4 + .26, .27, .28, .37, .38, .42 | AT-2603 · TC-2604 | pass |
| HLR-2605 / LLR-2605.1 | LED .5 + .33, .34, .41 | AT-2601 (editor arm) · TC-2605 | pass |
| HLR-2606 / LLR-2606.1, LLR-2606.2, LLR-2606.3 | LED .6 + .19, .21, .35, .45, .46 | AT-2604 · TC-2606 | pass |
| HLR-2607 / LLR-2607.1, LLR-2607.2 | LED .7 + .22, .31, .32 | AT-2605 · TC-2607 | pass |
| HLR-2608 / LLR-2608.1, LLR-2608.2 | LED .8 + .24, .25 | AT-2606 · TC-2608 | pass |

All in the Phase-4 gate run: 3235 passed + 1 environmental skip = 3236 collected, 0 failed (`evidence/suite-p4-chunk00..02.txt`, the orchestrator, at `512813d`; the skip is TC-1902's designed machine-refusal arm — G-001, the operator's decision).

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

- **New controls:** none — the batch's findings were caught by controls the flow already has: the half-landed-fold class (a fold that fixes its target but not its downstream consumers — twice at P2, once hunted again at the DDR's cross-increment census) is already catalogued in `dev-flow-lessons`; C-18 at the DDR held the one-node-per-AT line. A candidate for the operator's flow work, not minted here: C-18 checked per increment (one `test_AT_` def per AT at each packet's gate), the people round's close named the same.

---

## 3 · Working-file reconciliation (C-44)

| File | State | Evidence |
|---|---|---|
| `taskboard/marks.py` (new), `models.py`, `app.py`, `views.py`, `modals.py`, `keymap.py`, `taskboard.tcss` | ✅ committed on the local branch `feat/milestone-marks`; push and merge NOT authorized (the commission) | `f363a75`, `6fc2637`, `12b7a11`, `1cae9c6` |
| `tests/test_marks_directory.py`, `test_marks_manager.py`, `test_milestone_marks.py`, `milestone_marks_fixture.py` (new); `test_legend.py`, `test_modal_keys.py`, `test_readme.py` updated | ✅ committed on `feat/milestone-marks` | the increments' commits; the suite ledgers in the packets and `04-validation.md` |
| `README.md`, `docs/ARCHITECTURE.md`, `REQUIREMENTS.md` | ✅ committed | `1cae9c6`, `512813d` (the DDR's map folds), the close commit (the canon fold) |
| `.dev-flow/2026-10-24-batch-01/**` (plan, contract, ledger, review, the PDR/DDR records, the four packets, `04-validation.md`, the evidence, the 14 captures) | ✅ committed on `feat/milestone-marks` | `9873674`, `19a8f9c`, `d3516d4`, `512813d`, `4a12f07`, the close commit |
| `PLAN.md` (this batch's), `.dev-flow/BACKLOG.md`, `.dev-flow/state.json`, `05-close.md` | ✅ committed on `feat/milestone-marks` | the close commit |
| the capture harness's synthetic homes (`%TEMP%\m01-cap-*`) and the `m01-` windows | 🗑️ removed by the harness after each shot; the no-`m01-`-window assertion passed | `evidence/captures/png/capture-log.txt`, `assert-no-m01.ps1` |

- **Found before the batch:** `none — no tracked file was modified when the batch began` (the previous session's only residue was the untracked captures, committed as `d3516d4`)

The `modals.py` regeneration mishap of increment 003 is reconciled at the DDR, not here: `git diff ffb567d -- taskboard/modals.py` is exactly this batch's intended +230/−9 with every deleted line an increment-003 rewrite — no lost upstream line (`design/DDR-2026-10-24-batch-01.md`, the orchestrator's check).

### Conditional-gate discharge

- **Conditional-gate discharge:** none — no gate closed conditionally at the close. The gates upstream closed conditionally and discharged at their own seals: the PDR's PC-1..PC-5 (folded at seal, re-read at the DDR ✓) and the DDR's C-1 (discharged by amendment D-5, re-read by the same role ✓) — both cited below.

| Condition | Discharged? | The artifact line that proves it |
|---|---|---|
| the PDR's PC-1..PC-5 (folded at seal) | ✓ re-read at the DDR | `design/DDR-2026-10-24-batch-01.md` §B row 8 (each fold's artifact line cited) |
| the DDR's C-1 (the MarkForm runtime reach vs the frozen boundary) | ✓ at the DDR | `design/design-proposal.md` §2 amendment D-5; the architect's re-read verdict APPROVE |

---

## 4 · Backlog reconciliation — the carry-over contract

| Item | Move | Reference |
|---|---|---|
| the milestone-marks round (items 1–4, D1/D2's global verdict, the storage ruling) | ✓ done | `BACKLOG.md` §*Open — after `2026-10-24-batch-01`* (the done line); the batch's commits |
| MM-D5's ▲ ambiguity (logged, NOT fixed, as commissioned) | added | the same section |
| MM-D1's accepted costs (the unclassified red mark, the month ruler's lateness, the colour resemblance) | added (recorded, not fixed, as commissioned) | the same section; the shipped `README.md:191-193` |
| the prefix-`find` rule's two homes; fold F4's dropped deferral; the dead `milestone_tone`; the `check_action` refusal change (disclosed, asserted); the search tally / doubled census notices | added | the same section |
| the P4 clipboard environmental skip (G-001: re-run chunk 00 when the machine's clipboard recovers, or accept) | added | the same section; `04-validation.md` G-001, `evidence/suite-p4-clipboard-probe.txt` |
| every other item of the earlier sections | carried, unchanged | `BACKLOG.md` |

---

## 5 · Batch metrics — the 13 keys of `core`

Extract, do not invent: a key the artifacts did not record goes `null`, and the key is never dropped.

```yaml
type: dev-flow-batch
project: taskboard
batch_id: 2026-10-24-batch-01
mode: core
verdict: pass
increments: 4
source_files_max: 4          # increment 003: app.py, keymap.py, modals.py, taskboard.tcss (at the cap, the PDR's PC-5)
notices_raised: 171          # distinct NOTICE ids declared at P1's validator run (PLAN.md §Test ledger)
rework_returns: 0            # no item came back: every gate closed on its first pass after its folds
triggers_fired: "A1,A2,A3,B1,B4,C6,C8,D1,E1"   # PLAN.md §Key decisions D-2 (C3 does not fire)
tests_base_to_post: "3152 -> 3236"
new_control: none
open_items_next: 8           # BACKLOG.md §Open — after 2026-10-24-batch-01 (▲ ambiguity, MM-D1 costs, prefix-find, F4, milestone_tone, check_action, tally/census, the clipboard G-001)
```

---

## 6 · Human review ledger — what a human audited, at what depth

| Artifact | Machine verdict (citation) | Human review | Depth | Deliberately NOT reviewed |
|---|---|---|---|---|
| `01-requirements.md` / the contract | P1 gate 0 block · `V26` family green | ❌ | `none — the standing authorization names no human reader` | |
| `design/PDR-2026-10-24-batch-01.md` | three spawned roles' verdicts folded at seal | ❌ | `none` | |
| the four increment packets | each code-review PASS (F1-F4 folded, re-read verified) | ❌ | `none` | |
| `design/DDR-2026-10-24-batch-01.md` | three spawned roles; no HIGH; C-1 discharged and re-read; the modals.py regeneration check | ❌ | `none` | |
| Test cases / ATs | 3235 passed + 1 env skip; mutants 81/81 KILLED; the +84 ledger reconciled | ❌ | `none` | |
| the 14 captures | full-colour verified, the ux-reviewer's scene-by-scene read | ❌ | `none — expert inspection by the spawned ux-reviewer, not a user` | real-user evaluation (declared: none exists) |
| Evidence view | validator `--brief` 0 block at the close | ❌ | `none` | |
| Code | gates + reviewer verdicts `APPROVE` | ❌ | `none` | not audited line by line by a human |

- **Human perimeter:** the operator owns the verdicts this batch cannot take: the one environmental skip (G-001 — accept or re-run chunk 00 when the clipboard recovers), MM-D5's ▲ ruling, MM-D1's accepted costs at the next visual verdict, and the behaviour change to `#`/`@`/`A` over modals. Push and merge stay the operator's.
- **Human review ledger:** none — the batch ran autonomously under the commission's standing authorization; every audit above is a machine gate or a spawned reviewer role, and the human-decision items are queued in `BACKLOG.md` for the operator.
