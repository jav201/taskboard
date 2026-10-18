# Batch close — taskboard — Batch 2026-10-18-batch-01

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
| Gated tree | `6bb313008a69ed9725c07ccff71b460feb7e44ed` · dirty — .dev-flow/2026-10-07-batch-08/evidence/inc001-brief.md, .dev-flow/2026-10-07-batch-09/evidence/inc001-brief.md, .dev-flow/BACKLOG.md, .gitattributes, .dev-flow/2026-10-07-batch-05/decisions-log.json, .dev-flow/2026-10-07-batch-06/decisions-log.json, .dev-flow/2026-10-07-batch-06/evidence/gen_verdict_sheet.py, .dev-flow/2026-10-07-batch-06/evidence/kanban-demo.json, .dev-flow/2026-10-07-batch-06/evidence/veredicto-batch06.html, .dev-flow/2026-10-07-batch-06/evidence/veredicto-board.json, .dev-flow/2026-10-07-batch-07/decisions-log.json, .dev-flow/2026-10-07-batch-08/decisions-log.json, .dev-flow/rollover_batchg.py, .dev-flow/rollover_batchh.py, .dev-flow/rollover_batchi.py, .dev-flow/rollover_batchj.py (the close record itself excluded) |
| Requirements canon | `REQUIREMENTS.md` (`artifact_homes.requirements_canon`) — `devflow-init.py --fold-canon`: 10 folded, 0 kept, 0 refused (HLR-1801..HLR-1803, LLR-1801.1..LLR-1803.3); the status cells of the three rows this batch supersedes in part (LLR-1001.1's oracle, LLR-1601.1's header row, LLR-1602.2 (j)'s hint texts) updated by hand |

---

## 1 · What changed

`R` has two views. `1` gantt is the shipped presentation, its header now naming the view and its cursor note keeping line breaks, bullets and numbered steps. `2` split is the prototype's D2 · stacked: the gantt rows on top and, below them, every shown open task's notes at once — a heading and the note per task, two columns from 100 wide, the fair share with every cut declared, `no notes` for an empty note. `tab`/`shift+tab` cycle the views, `pgdn`/`pgup` page the split view's notes (tiled pages, no skipped row, never back; the whole area when no cursor note can scroll), `R` always opens on gantt, the cursor and hidden tasks are shared, `x` exports the view on screen (`-split` files), and the keys live only in the hint row. The README's Presentation section describes both views.

| Requirement | Version | Verified by | Verdict |
|---|---|---|---|
| `HLR-1801` | v1 (LED .1, amended .2, .3) | `AT-1801` · `TC-1801`..`TC-1806` | PASS (`suite-p4.txt`) |
| `HLR-1802` | v1 (LED .1, .2) | `AT-1802` · `TC-1807`, `TC-1001`, `TC-1002` | PASS |
| `HLR-1803` | v1 (LED .1, .2) | `AT-1803` · `TC-1806`, `TC-1808`..`TC-1810` | PASS |
| `LLR-1801.1` | v1 (LED .1, .2, .6) | `TC-1801`; M1–M3, M20 KILLED | PASS |
| `LLR-1801.2` | v1 (LED .1–.4) | `TC-1802`..`TC-1805`; M4–M8, M15–M18 KILLED | PASS |
| `LLR-1801.3` | v1 (LED .1–.4) | `TC-1806`; M9–M11, M14, M19 KILLED | PASS |
| `LLR-1802.1` | v1 (LED .1) | `TC-1807`, `TC-1001`, `TC-1002`; M12, M13 KILLED | PASS |
| `LLR-1803.1` | v1 (LED .1, .2, .5) | `TC-1810`; N1–N3, N8, N12 KILLED | PASS |
| `LLR-1803.2` | v1 (LED .1, .2) | `TC-1808`, `TC-1604` hint arm; N4, N5, N11 KILLED | PASS |
| `LLR-1803.3` | v1 (LED .1) | `TC-1809`, AT-1803 export arm; N6, N7, N9 KILLED | PASS |

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

- **New controls:** none — the lessons this batch met were caught by existing controls: a paging rule that skips rows (UX-1) by the P2 ux lens over rendered frames; two mutants that a named test did not redden (M5) by the PDR's tester lens running the battery (C-40); a hint that overflowed at 100 columns by a boundary row QA-10 asked for (C-31).

---

## 3 · Working-file reconciliation (C-44)

| File | State | Evidence |
|---|---|---|
| `taskboard/views.py` | ✅ committed on the local branch `present-v3`, not pushed (push not authorized) | `a729f78` |
| `taskboard/app.py`, `README.md` | ✅ committed on `present-v3`, not pushed | `038b5f2` |
| `tests/test_present_views.py`, `tests/present_notes_board.py`, `tests/test_present.py` | ✅ committed on `present-v3`, not pushed | `a729f78` |
| `tests/test_present_views_app.py`, `tests/test_present_hide.py`, `tests/test_markup_census.py` | ✅ committed on `present-v3`, not pushed | `038b5f2` |
| `prototypes/present_views/**` (sources, SVGs, the page; the PNGs locally excluded) | ✅ committed on `present-v3`, not pushed | `a729f78` |
| `docs/ARCHITECTURE.md` | ✅ committed on `present-v3`, not pushed | `92aafe0` |
| `REQUIREMENTS.md` | ✅ committed on `present-v3`, not pushed | the deliverable commit (close step 6) |
| `.dev-flow/state.json`, `.dev-flow/2026-10-17-batch-01/decisions-log.json` (the rollover archive) | ✅ committed on `present-v3`, not pushed | `3369900`, then each later commit |
| `.dev-flow/2026-10-18-batch-01/**` (contract, ledger, review, design records, packets, validation, plan, evidence: transcripts, frames, harnesses, captures) | ✅ committed on `present-v3`, not pushed | `3369900`, `92aafe0`, `9810be6`, `a729f78`, `038b5f2`, the deliverable commit |
| `.dev-flow/2026-10-18-batch-01/05-close.md`, `.dev-flow/BACKLOG.md` | ✅ committed on `present-v3`, not pushed | the close commit (close step 8) |
| scratch `git worktree`s (`…/scratchpad/wt1`, `wt2`, `wt3`) and the scratch copies (`base`, `probe1`, `probe2`) | 🗑️ removed after the close (`git worktree remove`), outside the repository | the suites, the RED runs and the batteries ran there |
| `.git/info/exclude` (local, unversioned) | one line added: `prototypes/present_views/out/*.png` | rollover decision, PLAN §Key decisions |

- **Found before the batch:** `.dev-flow/2026-10-07-batch-08/evidence/inc001-brief.md @ a751d73fdcddc239d01f02a2dfcb9ec042222110` `.dev-flow/2026-10-07-batch-09/evidence/inc001-brief.md @ 737b913e5559b8337969790137c4bda87fac2788` `.gitattributes @ 5650216ed19fb4d68b5ae282a0bd5042024dc222`

Also found before the batch, untracked and left alone: `.dev-flow/2026-10-07-batch-0{5,6,7,8}/decisions-log.json`, `.dev-flow/2026-10-07-batch-06/evidence/{gen_verdict_sheet.py,kanban-demo.json,veredicto-batch06.html,veredicto-board.json}`, `.dev-flow/rollover_batch{g,h,i,j}.py`.

### Conditional-gate discharge

- **Conditional-gate discharge:** 1 conditional gate — the PDR, `approved with conditions` (PC-A1, PC-A2, PC-Q1, PC-Q2, PC-U1, PC-U2), each re-read at the DDR or P4.

| Condition | Discharged? | The artifact line that proves it |
|---|---|---|
| PC-A1 the gauntlet controls and who pays | ✓ re-read by the architect at the DDR | `design/design-proposal.md` §5b |
| PC-A2 the security lens | ✓ re-read by the architect at the DDR | `design/design-proposal.md` §5c |
| PC-Q1 M5 reddened by a binding alloc row | ✓ re-read by the qa-reviewer at the DDR | `tests/test_present_views.py` TC-1802 `[ns8-0-6-want8]`; `evidence/mutation-001.txt` M5 |
| PC-Q2 M5 not claimed by TC-1804 | ✓ re-read by the qa-reviewer at the DDR | `evidence/mutate.py` M5 nodes |
| PC-U1 no backward jump on the first page down | ✓ re-read by both at the DDR | `taskboard/views.py` `_present_stack`; TC-1806; M19 |
| PC-U2 the hint's fit on the real `#present-hint` | ✓ at P4 (ux walkthrough UX4-1) | TC-1808; `04-validation.md` UX walkthrough |

---

## 4 · Backlog reconciliation — the carry-over contract

| Item | Move | Reference |
|---|---|---|
| Present v3: several views during the presentation, the task content readable | ✓ done in this batch | `a729f78`, `038b5f2` |
| round 1's Slide view (C) | added — optional future item, kept by the operator's verdict | `BACKLOG.md` (2026-10-18-batch-01 lane) |
| round 1's Cards view (B) | added — recorded as dropped | `BACKLOG.md` (2026-10-18-batch-01 lane) |
| page snapping to item starts; headings in the area scroll (UX-2, UX-3) | added | `02-review.md` |
| the short hint clipped below ~60 columns (code-review F2) | added | packet 002 §4b |
| the 80-column hint's key words; the gantt note's 3-row cap; the dim words' contrast (UX4-3, UX4-4, UX4-2) | added | `04-validation.md` G-4 |
| `render_present` asserts below ~36 columns (pre-existing on `base_ref`) | added | packet 001 §6 |
| the 2 standup tests failing since the 2026-10-11 rewrite | carried, unchanged | `suite-p4.txt` |
| `test_win_clipboard_roundtrip` environment failure | carried; it passed in every full run of this batch | `suite-001.txt`, `suite-002.txt`, `suite-p4.txt` |

---

## 5 · Batch metrics — the 13 keys of `core`

Extract, do not invent: a key the artifacts did not record goes `null`, and the key is never dropped.

```yaml
type: dev-flow-batch
project: taskboard
batch_id: 2026-10-18-batch-01
mode: core
verdict: pass
increments: 2
source_files_max: 1              # increment 001 (taskboard/views.py), increment 002 (taskboard/app.py)
notices_raised: null             # PLAN.md declares NOTICEs as ranges and counts per gate, not one id per line
rework_returns: 1                # P2 iterate-to-refine (iterations_per_station P1 = 1)
triggers_fired: "A2,A3,B1,B3,B4,C8,D1,E1"
tests_base_to_post: "2663 -> 2723"
new_control: none
open_items_next: 9               # the 2026-10-18-batch-01 lane (9 items: 2 optional views, 7 optional or pre-existing)
```

---

## 6 · Human review ledger — what a human audited, at what depth

| Artifact | Machine verdict (citation) | Human review | Depth | Deliberately NOT reviewed |
|---|---|---|---|---|
| the prototype round `prototypes/present_views/` (round 2, D2 · stacked) | — | ✅ the operator's verdicts, 2026-10-17/18 (relayed in the commission) | `light` | |
| `01-requirements.md` / ledger | P2 review (2 iterations), `V26` green | ❌ | `none — reviewed by the architect, qa, ux and security agents, not by a human` | |
| Code (`taskboard/views.py`, `taskboard/app.py`) and tests | code-reviewer OK to advance, 0 HIGH (each increment, re-read after its fold); 30/30 and 16/16 mutants KILLED | ❌ | `none — agent review only` | not audited line by line |
| `04-validation.md` | qa-reviewer PASS-WITH-NOTES | ❌ | `none` | |
| the captures `evidence/captures/app-002-*` | AT-1801..AT-1803 assert the painted frames; ux-reviewer walkthrough pass-with-notes | ❌ | `none — produced for the operator's review, not yet seen` | |

- **Human perimeter:** the operator owns whether the split view reads well to a room (no user evaluation was done), the visual check of this batch's captures against the prototype, the contrast of the dim words on a screen share (UX4-2), and the push/merge of `present-v3` (not authorized here).
- **Human review ledger:** human:operator — 1 artifact(s) reviewed, 0 rigorous · 4 declared not-reviewed
