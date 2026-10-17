# Batch close — taskboard — Batch 2026-10-17-batch-01

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
| Gate record | `python "C:/Users/jjgh8/.claude/skills/dev-flow/scripts/devflow-validate.py" .` from the project root · exit 0 · 0 block · 40 notice · 2026-10-17 |
| Gated tree | `28e99607c06b17c1e919f6ebd6fe1a70edc66b5e` · dirty — .dev-flow/2026-10-07-batch-08/evidence/inc001-brief.md, .dev-flow/2026-10-07-batch-09/evidence/inc001-brief.md, .dev-flow/BACKLOG.md, .gitattributes, .dev-flow/2026-10-07-batch-05/decisions-log.json, .dev-flow/2026-10-07-batch-06/decisions-log.json, .dev-flow/2026-10-07-batch-06/evidence/gen_verdict_sheet.py, .dev-flow/2026-10-07-batch-06/evidence/kanban-demo.json, .dev-flow/2026-10-07-batch-06/evidence/veredicto-batch06.html, .dev-flow/2026-10-07-batch-06/evidence/veredicto-board.json, .dev-flow/2026-10-07-batch-07/decisions-log.json, .dev-flow/2026-10-07-batch-08/decisions-log.json, .dev-flow/rollover_batchg.py, .dev-flow/rollover_batchh.py, .dev-flow/rollover_batchi.py, .dev-flow/rollover_batchj.py (the close record itself excluded) |
| Requirements canon | `REQUIREMENTS.md` (`artifact_homes.requirements_canon`) — `devflow-init.py --fold-canon`: 2 folded, 0 kept, 0 refused (HLR-1701, LLR-1701.1); the status cells of the five rows whose scale-label clauses HLR-1701 supersedes (HLR-105, LLR-101.10, LLR-102.2 of 2026-10-02-batch-01; LLR-1601.1, LLR-1602.2 of 2026-10-16-batch-01) rewritten by hand to name the superseded clause (code-review F-1; LED .1/.2) |

---

## 1 · What changed

The tick row's label no longer shows the axis scale (`Mondays · 1 day = 2 cells`) anywhere: in the gantt view (`3`, and link mode `L`) and in the presentation (`R`, and its `x` export) it names the selected task — `selected task ▸` in the echo's tone, the echo's own dates when they do not fit, `selected: no dates` for a dateless selection — and is blank with nothing selected. One function, `views._gantt_tick_label`, holds the rule for both views; `_gantt_scale_label` is deleted.

| Requirement | Version | Verified by | Verdict |
|---|---|---|---|
| `HLR-1701` | v1 (LED .1, amended .2, .3) | `AT-1701` · `TC-1701` | PASS (`suite-p4.txt`) |
| `LLR-1701.1` | v1 (LED .1, amended .2, .3) | `TC-1701` (26 nodes; layer 0 `the_label_function_branches`); 19/19 mutants KILLED | PASS |

---

## 2 · New controls discovered — and where they landed (C-45)

| Control | What failure it closes | Measured origin |
|---|---|---|

| # | Landing | Done? | SHA / path |
|---|---|---|---|
| 1 | the **command** (`commands/…`) — the rule itself | n/a | no control minted |
| 2 | its **artifact** (a template section) — a control with no output degrades to "I thought about it" | n/a | no control minted |
| 3 | the **catalog** entry (`dev-flow-lessons`) with its measured origin | n/a | no control minted |
| 4 | **committed and pushed**, manifest re-hashed and bumped | n/a | no control minted |

- **New controls:** none — the one lesson this batch met (a grep census cannot see a test that measures a screen metric: the dead-cell law moved with the removed label) was caught by the existing C-39 pre-execution of the full suite, which is what that control is for; no new control is needed.

---

## 3 · Working-file reconciliation (C-44)

| File | State | Evidence |
|---|---|---|
| `taskboard/views.py` | ✅ committed on the local branch `gantt-tick-label`, not pushed (push not authorized) | `63c9669` |
| `tests/test_tick_label.py`, `tests/test_gantt.py`, `tests/test_gantt_board.py`, `tests/test_present_room.py`, `tests/test_present_rulers.py` | ✅ committed on `gantt-tick-label`, not pushed | `63c9669` |
| `REQUIREMENTS.md` | ✅ committed on `gantt-tick-label`, not pushed | the deliverable commit (close step 6) |
| `.dev-flow/state.json`, `.dev-flow/2026-10-16-batch-01/decisions-log.json` (the rollover archive) | ✅ committed on `gantt-tick-label`, not pushed | `3cde009`, then each later commit |
| `.dev-flow/2026-10-17-batch-01/**` (contract, ledger, review, packet, validation, plan, evidence: transcripts, harnesses, captures) | ✅ committed on `gantt-tick-label`, not pushed | `3cde009`, `de9c4a2`, `63c9669`, the deliverable commit |
| `.dev-flow/2026-10-17-batch-01/05-close.md`, `.dev-flow/BACKLOG.md` | ✅ committed on `gantt-tick-label`, not pushed | the close commit (close step 8) |
| scratch `git worktree` (`…/scratchpad/probe`, detached at `3cde009`) | 🗑️ removed after the close (`git worktree remove`), outside the repository | the C-39 pre-execution and the mutation battery ran there |

- **Found before the batch:** `.dev-flow/2026-10-07-batch-08/evidence/inc001-brief.md @ a751d73fdcddc239d01f02a2dfcb9ec042222110` `.dev-flow/2026-10-07-batch-09/evidence/inc001-brief.md @ 737b913e5559b8337969790137c4bda87fac2788` `.gitattributes @ 5650216ed19fb4d68b5ae282a0bd5042024dc222`

Also found before the batch, untracked and left alone: `.dev-flow/2026-10-07-batch-0{5,6,7,8}/decisions-log.json`, `.dev-flow/2026-10-07-batch-06/evidence/{gen_verdict_sheet.py,kanban-demo.json,veredicto-batch06.html,veredicto-board.json}`, `.dev-flow/rollover_batch{g,h,i,j}.py`.

### Conditional-gate discharge

- **Conditional-gate discharge:** none — no gate closed conditionally (P2 approved in iteration 2 with its minors folded in LED .3; QA2-1 was an implementation finding, discharged in increment 001: `tests/test_gantt.py:287`; P4 PASS-WITH-NOTES with three minor gaps, each accepted or routed).

| Condition | Discharged? | The artifact line that proves it |
|---|---|---|

---

## 4 · Backlog reconciliation — the carry-over contract

| Item | Move | Reference |
|---|---|---|
| the operator's visual verdict on the 80-column oracle frame (batch 2026-10-16-batch-01) | ✓ resolved — the operator's verdict «Ya vi las capturas, se ven todo en orden.», recorded asked at the gate | `BACKLOG.md` (marked at `3cde009`), PLAN §Key decisions, `decisions_log` |
| the gantt view's own tick label (batch 2026-10-16-batch-01, code review F1) | ✓ done in this batch | `63c9669` |
| the README hero image `docs/taskboard-gantt.svg` still shows `Mondays · 1 d/cell` | added (new lane) | LED .2 (Out of scope), 04-validation G-003, code review F-2 |
| `views._present_ruler` repeats the gantt ruler's layout lines (batch-01 F3) | carried, narrowed: the label rule is now shared; the layout lines are not | `_gantt_tick_label` |
| the operator's approval of `selected: no dates` | carried, widened: the text now also appears in the gantt view | HLR-1701 |
| the 2 standup tests failing since the 2026-10-11 rewrite | carried, unchanged | `suite-p4.txt` |
| `test_win_clipboard_roundtrip` environment failure | carried; it passed in both of this batch's full runs | `suite-001.txt`, `suite-p4.txt` |

---

## 5 · Batch metrics — the 13 keys of `core`

Extract, do not invent: a key the artifacts did not record goes `null`, and the key is never dropped.

```yaml
type: dev-flow-batch
project: taskboard
batch_id: 2026-10-17-batch-01
mode: core
verdict: pass
increments: 1
source_files_max: 1              # increment 001 (taskboard/views.py)
notices_raised: null             # PLAN.md declares NOTICEs as ranges and counts per gate, not one id per line
rework_returns: 1                # P2 iterate-to-refine (iterations_per_station P1 = 1)
triggers_fired: "B1,B3,B4,D1"
tests_base_to_post: "2634 -> 2663"
new_control: none
open_items_next: 7               # the 2026-10-16-batch-01 lane (6 still open) + the 2026-10-17-batch-01 lane (1)
```

---

## 6 · Human review ledger — what a human audited, at what depth

| Artifact | Machine verdict (citation) | Human review | Depth | Deliberately NOT reviewed |
|---|---|---|---|---|
| batch 2026-10-16-batch-01's increment-004 captures (incl. `app-004-80x25-present-open.svg`) | — | ✅ the operator's verdict, 2026-10-17: «Ya vi las capturas, se ven todo en orden.» | `light` | |
| `01-requirements.md` / ledger | P2 review (2 iterations), `V26` green | ❌ | `none — reviewed by the architect, qa and ux agents, not by a human` | |
| Code (`taskboard/views.py`) and tests | code-reviewer PASS-with-notes, 0 HIGH; 19/19 mutants KILLED | ❌ | `none — agent review only` | not audited line by line |
| `04-validation.md` | qa-reviewer PASS-WITH-NOTES | ❌ | `none` | |
| the captures `evidence/captures/app-001-*.svg`, `app-001-118x31-gantt-selected.png` | TC-1701 asserts the painted text and tone; fills read from the SVG | ❌ | `none — produced for the operator's review, not yet seen` | |

- **Human perimeter:** the operator owns whether `selected task ▸` / `selected: no dates` read well in the gantt view (no user evaluation was done), the visual check of this batch's captures, whether to regenerate the README hero image, and the push/merge of `gantt-tick-label` (not authorized here).
- **Human review ledger:** human:operator — 1 artifact(s) reviewed, 0 rigorous · 4 declared not-reviewed
