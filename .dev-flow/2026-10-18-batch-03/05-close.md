# Batch close — taskboard — Batch 2026-10-18-batch-03

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
| Gate record | `python "C:/Users/jjgh8/.claude/skills/dev-flow/scripts/devflow-validate.py" .` from the project root · exit 0 · 0 block · 41 notice · 2026-10-18 |
| Gated tree | `d573a9fbede8c3272a05f841d2e047ebbd519fd3` · dirty — .dev-flow/2026-10-07-batch-08/evidence/inc001-brief.md, .dev-flow/2026-10-07-batch-09/evidence/inc001-brief.md, .gitattributes, .dev-flow/2026-10-07-batch-05/decisions-log.json, .dev-flow/2026-10-07-batch-06/decisions-log.json, .dev-flow/2026-10-07-batch-06/evidence/gen_verdict_sheet.py, .dev-flow/2026-10-07-batch-06/evidence/kanban-demo.json, .dev-flow/2026-10-07-batch-06/evidence/veredicto-batch06.html, .dev-flow/2026-10-07-batch-06/evidence/veredicto-board.json, .dev-flow/2026-10-07-batch-07/decisions-log.json, .dev-flow/2026-10-07-batch-08/decisions-log.json, .dev-flow/rollover_batchg.py, .dev-flow/rollover_batchh.py, .dev-flow/rollover_batchi.py, .dev-flow/rollover_batchj.py (the close record itself excluded) |
| Requirements canon | `REQUIREMENTS.md` (`artifact_homes.requirements_canon`) — `devflow-init.py --fold-canon`: 6 folded, 0 kept, 0 refused (HLR-2001..HLR-2003, LLR-2001.1..LLR-2003.1); the status cells of LLR-1001.1, HLR-1802, LLR-1801.2, LLR-1802.1, LLR-1803.2, HLR-1904 and LLR-1904.1 updated by hand: superseded in part (LED .1, LED .3) |

---

## 1 · What changed

The presentation (`R`) now shows what the operator approved in the polish round, variant A of all three items: its view word and the marks that say a note or a column was cut (`… +N lines`, `↑ N lines above`, `↓ N more lines`) are painted `reached` (4.87:1 on the background, was `dim` at 3.25:1), still quieter than titles and dates; at 80 columns the hint row names `next` and `show all` through a middle wording between the long and the short one; and the gantt view's cursor note uses every row left under the brief list (3 at least) instead of stopping at 3, still declaring its cut. Mechanism: four tone literals and one row count in `taskboard/views.py`, one wording in `taskboard/app.py`; each ported from the round's own fork and compared with it — the round's capture code re-run on `620f58c`, its A forks composed, against the real app's captures: 9 of 10 SVGs equal, the tenth differing by one declared glyph (the gantt cut row's `· ` lead stays `dim`). Also: the help modal's timing flake (AT-1603) hardened, for the commission's 0-failure target.

| Requirement | Version | Verified by | Verdict |
|---|---|---|---|
| `HLR-2001` | v1 (LED .1–.4) | `AT-2001` · `TC-2001` | PASS (`suite-p4.txt`) |
| `HLR-2002` | v1 (LED .1, .3) | `AT-2002` · `TC-2002`, `TC-1904` | PASS |
| `HLR-2003` | v1 (LED .1, .3) | `AT-2003` · `TC-2003`, `TC-1807` | PASS |
| `LLR-2001.1` | v1 (LED .1–.3) | `TC-2001`; M1–M6 KILLED | PASS |
| `LLR-2002.1` | v1 (LED .1, .3, .5) | `TC-2002`, `TC-1904`; N1–N4 KILLED | PASS |
| `LLR-2003.1` | v1 (LED .1–.3) | `TC-2003`, `TC-1807`, `AT-1802`; K1–K4 KILLED | PASS |

---

## 2 · New controls discovered — and where they landed (C-45)

| Control | What failure it closes | Measured origin |
|---|---|---|

**The four landings — record which ones actually happened. Command-but-not-template is *half-encoded*, and the missing half is the enforceable one:**

| # | Landing | Done? | SHA / path |
|---|---|---|---|
| 1 | the **command** (`commands/…`) — the rule itself | n/a | no control minted |
| 2 | its **artifact** (a template section) — a control with no output degrades to "I thought about it" | n/a | no control minted |
| 3 | the **catalog** entry (`dev-flow-lessons`) with its measured origin | n/a | no control minted |
| 4 | **committed and pushed**, manifest re-hashed and bumped | n/a | no control minted |

- **New controls:** none — the lessons met were caught by existing controls: an AT that never observed a mutated site (the PDR's executed battery, C-40: M4 survived AT-2001 → `pgdn`); a mutant counted on a node already red (PDR PC-2 → the harness's pre-check, shown refusing in `precheck-redproof.txt`); a correction population taken from the review's census instead of a command (C-14: the full suite found AT-1802 on the old frames — declared in packet 003); a fork's capture differing from its stated design by a span-merge artefact (the round comparison itself, `compare-001.txt`).

---

## 3 · Working-file reconciliation (C-44)

| File | State | Evidence |
|---|---|---|
| `taskboard/views.py`, `tests/test_present_polish.py` | ✅ committed on the local branch `present-polish`, not pushed (push not authorized) | `e72a316`, `984ba8e` |
| `taskboard/app.py`, `tests/test_present_narrow.py`, `tests/test_present_views_app.py`, `tests/test_present_hide.py`, `tests/test_help_keys.py` | ✅ committed on `present-polish`, not pushed | `b12e563` (and `984ba8e` for `tests/test_present_views_app.py`) |
| `tests/test_present_views.py` | ✅ committed on `present-polish`, not pushed | `984ba8e` |
| `docs/ARCHITECTURE.md` | ✅ committed on `present-polish`, not pushed | `bf6f4bb`, `984ba8e` |
| `REQUIREMENTS.md` | ✅ committed on `present-polish`, not pushed | the deliverable commit (close step 6) |
| `.dev-flow/state.json`, `.dev-flow/2026-10-18-batch-02/decisions-log.json` (the rollover archive) | ✅ committed on `present-polish`, not pushed | `89140b7`, then each later commit |
| `.dev-flow/2026-10-18-batch-03/**` (contract, ledger, review, design records, packets, validation, plan, evidence: transcripts, the battery, the oracle frames and expected captures, the real-app captures) | ✅ committed on `present-polish`, not pushed | `89140b7` … `fdc83e3`, the deliverable commit |
| `.dev-flow/2026-10-18-batch-03/05-close.md`, `.dev-flow/BACKLOG.md` | ✅ committed on `present-polish`, not pushed | the close commit (close step 8) |
| scratch worktrees `…/scratchpad/wt-base` (at `620f58c`) and `wt-p4` (at `984ba8e`) | 🗑️ removed by the orchestrator (`git worktree remove`); `git worktree list` holds no scratch worktree | this table |
| scratch copies and transcripts in the session scratchpad (`mut`, `round-A`, `upto-1..3`, `port-1..2`, drafts) | 🗑️ removed at the session's end | the hand-back |

- **Found before the batch:** `.dev-flow/2026-10-07-batch-08/evidence/inc001-brief.md @ a751d73fdcddc239d01f02a2dfcb9ec042222110` `.dev-flow/2026-10-07-batch-09/evidence/inc001-brief.md @ 737b913e5559b8337969790137c4bda87fac2788` `.gitattributes @ 5650216ed19fb4d68b5ae282a0bd5042024dc222`

Also found before the batch, untracked and left alone: `.dev-flow/2026-10-07-batch-0{5,6,7,8}/decisions-log.json`, `.dev-flow/2026-10-07-batch-06/evidence/{gen_verdict_sheet.py,kanban-demo.json,veredicto-batch06.html,veredicto-board.json}`, `.dev-flow/rollover_batch{g,h,i,j}.py`. A stale `.git/worktrees/clipboard-fix` entry that `git worktree prune` could not delete (`Permission denied`) — not this batch's; in `BACKLOG.md`.

### Conditional-gate discharge

- **Conditional-gate discharge:** 6 condition(s) · ✅ all discharged — the PDR's `approved with conditions` (PC-1..PC-4) and the DDR qa lens's C1, C2, each re-read at the DDR (`design/DDR-2026-10-18-batch-03.md` §B).

| Condition | Discharged? | The artifact line that proves it |
|---|---|---|
| PC-1 AT-2001 observes `_present_mark` | ✓ re-read by the qa-reviewer | `tests/test_present_polish.py` AT-2001 (`pagedown`, a `↑`/`↓` mark); `evidence/mutation-001.txt` M4 KILLED |
| PC-2 TC-1904's middle tier; the harness pre-check | ✓ re-read by the qa-reviewer | `tests/test_present_narrow.py` (the middle tier); `evidence/mutation-002.txt`; `evidence/precheck-redproof.txt` |
| PC-3 K4 at `[80-24]` | ✓ re-read by the architect | `evidence/mutation-003.txt` K4 KILLED |
| PC-4 `Path`; the stdout encoding | ✓ re-read by the architect | `tests/test_present_polish.py` import; `evidence/mutate.py` |
| C1 the pre-check's RED-proof | ✓ by exercise | `evidence/precheck-redproof.txt` (`NOT GREEN`, the battery stops) |
| C2 the post-suite re-runs | ✓ re-cited | packets 001/002 cite `evidence/suite-003.txt` (0 failed) |

---

## 4 · Backlog reconciliation — the carry-over contract

| Item | Move | Reference |
|---|---|---|
| the dim view word and cut marks (UX4-2 of 2026-10-18-batch-01) | ✓ done — variant A | `e72a316` |
| the terse 80-column hint (UX4-3) | ✓ done — variant A | `b12e563` |
| the gantt view's 3-row note cap (UX4-4) | ✓ done — variant A | `984ba8e` |
| the help modal's timing flake (AT-1603) | ✓ done — hardened | `b12e563`; `evidence/flake-002.txt` |
| the tick-row label `selected: no dates` | carried — OPERATOR, unchanged | `BACKLOG.md` |
| round 1's Slide view | carried — OPERATOR, unchanged | `BACKLOG.md` |
| page snapping to an item's start; the scrolling headings | carried — OPERATOR, unchanged | `BACKLOG.md` |
| the round's retirement (AT-1905's rule) | added — OPERATOR (no deletion commissioned) | `BACKLOG.md` |
| the cut row's `· ` lead (a declared deviation from the capture) | added — OPERATOR | `BACKLOG.md`; `evidence/compare-001.txt` |
| UX-1 (gantt shows more of a note than split), UX-2 (the inactive view name at 3.25:1), UX4-1 (bare `esc`) | added — OPERATOR / watch | `BACKLOG.md` |
| G-1 the separators unasserted; G-2 the export's contents by inspection | added | `04-validation.md`; `BACKLOG.md` |
| the stale `.git/worktrees/clipboard-fix` entry | added — the operator's | `BACKLOG.md` |

---

## 5 · Batch metrics — the 13 keys of `core`

Extract, do not invent: a key the artifacts did not record goes `null`, and the key is never dropped.

```yaml
type: dev-flow-batch
project: taskboard
batch_id: 2026-10-18-batch-03
mode: core
verdict: pass
increments: 3
source_files_max: 1              # each increment: views.py, app.py, views.py
notices_raised: null             # PLAN.md declares NOTICEs as ranges and counts per gate, not one id per line
rework_returns: 1                # P2 iterate-to-refine (iterations_per_station P1 = 1); the ARQ iterate folded in place
triggers_fired: "A2,B1,B3,B4,D1,E1"
tests_base_to_post: "2740 -> 2759"
new_control: none
open_items_next: 10              # the 2026-10-18-batch-03 lane
```

---

## 6 · Human review ledger — what a human audited, at what depth

| Artifact | Machine verdict (citation) | Human review | Depth | Deliberately NOT reviewed |
|---|---|---|---|---|
| the polish round's three variants (the design) | AT-1905 (2026-10-18-batch-02) | ✅ the operator's verdict «Si, apruebo.», relayed by the coordinator, 2026-10-18 | `light` | |
| `01-requirements.md` / ledger | P2 review (2 iterations), `V26` green | ❌ | `none — reviewed by the architect, qa and ux agents, not by a human` | |
| Code (`taskboard/views.py`, `taskboard/app.py`) and tests | code-reviewer OK to advance, 0 HIGH (each increment); 10/10, 8/8, 11/11 mutants KILLED | ❌ | `none — agent review only` | not audited line by line |
| `04-validation.md` and the captures | qa-reviewer PASS-WITH-NOTES; ux walkthrough pass-with-notes; `compare-003.txt` 9 EQUAL + 1 declared | ❌ | `none — the captures are produced for the operator's look` | |

- **Human perimeter:** the operator owns the look of the shipped polish on a real projector (no user evaluation and no projector were used — contrast is computed), the one-glyph deviation from the round's capture, the round's retirement, the OPERATOR items left open, and the push/merge of `present-polish` (not authorized here).
- **Human review ledger:** human:operator — 1 artifact(s) reviewed, 0 rigorous · 3 declared not-reviewed
