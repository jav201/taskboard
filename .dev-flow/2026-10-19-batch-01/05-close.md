# Batch close — taskboard — Batch 2026-10-19-batch-01

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
| Gate record | `python "C:/Users/jjgh8/.claude/skills/dev-flow/scripts/devflow-validate.py" .` from the project root · exit 0 · 0 block · 44 notice · 2026-10-20 |
| Gated tree | `b832324ed8bdd1134cf3449cc377886dd6125692` · dirty — .dev-flow/2026-10-07-batch-08/evidence/inc001-brief.md, .dev-flow/2026-10-07-batch-09/evidence/inc001-brief.md, .dev-flow/BACKLOG.md, .gitattributes, .dev-flow/2026-10-07-batch-05/decisions-log.json, .dev-flow/2026-10-07-batch-06/decisions-log.json, .dev-flow/2026-10-07-batch-06/evidence/gen_verdict_sheet.py, .dev-flow/2026-10-07-batch-06/evidence/kanban-demo.json, .dev-flow/2026-10-07-batch-06/evidence/veredicto-batch06.html, .dev-flow/2026-10-07-batch-06/evidence/veredicto-board.json, .dev-flow/2026-10-07-batch-07/decisions-log.json, .dev-flow/2026-10-07-batch-08/decisions-log.json, .dev-flow/rollover_batchg.py, .dev-flow/rollover_batchh.py, .dev-flow/rollover_batchi.py, .dev-flow/rollover_batchj.py (the close record itself excluded) |
| Requirements canon | `REQUIREMENTS.md` (`artifact_homes.requirements_canon`) — `devflow-init.py --fold-canon`: 12 folded, 0 kept, 0 refused (HLR-2101..HLR-2106, LLR-2101.1..LLR-2106.1); LLR-2106.1's row brought to LED .5's statement; the status cells of HLR-1602, HLR-1803, LLR-1803.1, LLR-1803.2, LLR-1803.3, LLR-1903.1, LLR-1904.1, HLR-2002 and LLR-2002.1 marked superseded in part |

---

## 1 · What changed

The presentation (`R`) has a third view, `3 all`: every shown project on one date ruler, a header row per project with its shown open tasks, and from 100 columns a rail listing every project in the presentation's order (`●` shown, `○` hidden) — variant C of the present-portfolio round, the operator's verdict. The presenter hides and re-shows projects and tasks (`space`, `a` with a notice of what came back), moves projects in the presentation's own order (`shift+↑/↓`, saved on the board as `Project.present_rank`; the board's other views keep board order), folds projects (`enter`), moves between rail and timeline (`←/→`), and exports view 3's timeline without the rail (`x`, `present-board-<date>-all`). `u` opens a list of what is hidden in all three views, over the dimmed presentation, its cursor on the first hidden row, bringing items back one by one. A milestone in views 1/2 is now a `◆` on its date, not a bar from today. `Project.show_in_present` / `present_rank` are written only off their defaults, so existing boards keep their bytes, and a team pull never carries them.

| Requirement | Version | Verified by | Verdict |
|---|---|---|---|
| `HLR-2101` | v1 (LED .1, .2) | `AT-2101` · `TC-2101` | PASS (`suite-p4.txt`) |
| `HLR-2102` | v1 (LED .1, .2) | `AT-2102` · `TC-2102` | PASS |
| `HLR-2103` | v1 (LED .1–.3) | `AT-2103` · `TC-2103` | PASS |
| `HLR-2104` | v1 (LED .1, .2) | `AT-2104` · `TC-2104`, `TC-1904`, `TC-1808`, `TC-2002` | PASS |
| `HLR-2105` | v1 (LED .1, .2) | `AT-2105` · `TC-2105` | PASS |
| `HLR-2106` | v1 (LED .1, .2) | `AT-2106` · `TC-2106` | PASS |
| `LLR-2101.1` | v1 | `TC-2101`; M1–M5 KILLED | PASS |
| `LLR-2102.1` | v1 | `TC-2102`; N1–N6 KILLED | PASS |
| `LLR-2103.1` | v1 (LED .4) | `TC-2103`; P1–P6, R1, R2, S3 KILLED | PASS |
| `LLR-2104.1` | v1 | `TC-2104`; Q1–Q4, Q13, Q14, S1, S2 KILLED | PASS |
| `LLR-2105.1` | v1 | `TC-2105`; Q5–Q8, Q11, Q15 KILLED | PASS |
| `LLR-2106.1` | v1 (LED .5) | `TC-2106`; P7, P8, Q9, Q10, Q12 KILLED; `red-005.txt`, `red-006.txt` | PASS |

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

- **New controls:** none — the lessons met were caught by existing controls: a crash on a path no test drove (a resize across the rail's threshold) found by the independent code review and pinned by a node RED on the crashing tree (C-40); a UI trap (the picker's cursor on a shown project) found by the walkthrough driving the real mechanism, not by the ATs that pressed `down` first; a capture defect (the picker over a blank screen) found by looking at the evidence, not by any assertion — each closed with a node RED on the tree that had it. Re-citing an evidence file a later increment rewrote was caught by `V41` (fixed by keeping the cited versions).

---

## 3 · Working-file reconciliation (C-44)

| File | State | Evidence |
|---|---|---|
| `taskboard/views.py`, `tests/test_present_milestone.py`, `tests/present_portfolio_board.py` | ✅ committed on the local branch `feat/present-all`, not pushed (push not authorized) | `85281a6`, `231e56b`, `6d9f344`, `fc55d3a` |
| `taskboard/models.py`, `taskboard/team_sync.py`, `tests/test_present_all.py` | ✅ committed on `feat/present-all`, not pushed | `1c601bc`, then 003–006 |
| `taskboard/app.py`, `taskboard/modals.py`, `taskboard/taskboard.tcss`, the law-driven test files, `tests/test_markup_census.py`, `README.md` | ✅ committed on `feat/present-all`, not pushed | `6d9f344`, `fc55d3a`, `7c4140a`, `91d1f8c` |
| `prototypes/present_portfolio/**` (the round, cherry-picked from `1132d85`) | ✅ committed on `feat/present-all` as `bdf6e9d` (the batch's `base_ref`), unchanged since | `git diff bdf6e9d -- prototypes/present_portfolio` empty |
| `docs/ARCHITECTURE.md`, `REQUIREMENTS.md` | ✅ committed on `feat/present-all`, not pushed | `23c3b9e`, `91d1f8c`; the canon in the deliverable commit |
| `.dev-flow/state.json`, `.dev-flow/2026-10-18-batch-03/decisions-log.json` (the rollover archive) | ✅ committed on `feat/present-all`, not pushed | `d1b1b16`, then each later commit |
| `.dev-flow/2026-10-19-batch-01/**` (contract, ledger, review, design records, packets, validation, plan, evidence: transcripts, batteries, the hint widths, the captures) | ✅ committed on `feat/present-all`, not pushed | the batch's commits; the deliverable commit (close step 6) |
| `.dev-flow/2026-10-19-batch-01/05-close.md`, `.dev-flow/BACKLOG.md` | ✅ committed on `feat/present-all`, not pushed | the close commit (close step 8) |
| scratch worktrees `…/scratchpad/wt-base`, `wt-002`…`wt-006`, `wt-final` | 🗑️ removed by the orchestrator (`git worktree remove`, `git worktree prune`); `git worktree list` holds none of them | this table |
| scratch drafts, captures and PNGs in the session scratchpad (`inc`, `devflow`, `cap-*`, `png-impl`) | kept for the orchestrator's review (`png-impl` is the commission's PNG folder); outside the repository | the hand-back |

- **Found before the batch:** `.dev-flow/2026-10-07-batch-08/evidence/inc001-brief.md @ a751d73fdcddc239d01f02a2dfcb9ec042222110` `.dev-flow/2026-10-07-batch-09/evidence/inc001-brief.md @ 737b913e5559b8337969790137c4bda87fac2788` `.gitattributes @ 5650216ed19fb4d68b5ae282a0bd5042024dc222`

Also found before the batch, untracked and left alone: `.dev-flow/2026-10-07-batch-0{5,6,7,8}/decisions-log.json`, `.dev-flow/2026-10-07-batch-06/evidence/{gen_verdict_sheet.py,kanban-demo.json,veredicto-batch06.html,veredicto-board.json}`, `.dev-flow/rollover_batch{g,h,i,j}.py`. Worktrees found registered and left alone: `.claude/worktrees/{kanban-variants,kg-mejoras,present-e}`, `…/ds-units/name-taskboard`.

### Conditional-gate discharge

- **Conditional-gate discharge:** 4 condition(s) · ✅ all discharged — the PDR's `approved with conditions` (PC-1..PC-4), each re-read at the DDR (`design/DDR-2026-10-19-batch-01.md` §B), PC-1 with four declared substitutions.

| Condition | Discharged? | The artifact line that proves it |
|---|---|---|
| PC-1 each AT's §5 mutation killed | ✓ with four declared substitutions | `design/DDR-2026-10-19-batch-01.md` §B (the substitutions named); `evidence/mutation-00N*.txt` |
| PC-2 the markup payload arms RED without `escape` | ✓ | `evidence/mutation-003.txt` P5, P6; `mutation-004.txt` Q10 |
| PC-3 the census key unchanged, no new exemption | ✓ | `tests/test_markup_census.py:79-80` |
| PC-4 literal hint tables measured outside the code | ✓ | `evidence/hint-widths.txt`, `hint_widths.py`; the four test files |

---

## 4 · Backlog reconciliation — the carry-over contract

| Item | Move | Reference |
|---|---|---|
| the gantt of every project in the presentation, hide tasks or projects, reorder projects (the operator's request) | ✓ done — Present view `3 all`, variant C | `6d9f344`, `fc55d3a`, `91d1f8c` |
| the milestone bar of views 1/2 (the round's finding) | ✓ done | `85281a6` |
| the presentation order is presentation-only (D2, the orchestrator's reading) | added — OPERATOR | `BACKLOG.md` |
| the `?` help keeps the main screen's keys only (D8 deviation) | added — OPERATOR | `BACKLOG.md` |
| the split view's 80-column hint (HLR-2002 superseded in part) | added — OPERATOR | `BACKLOG.md` |
| view 3 under ~14 rows; `shift+arrow` the only reorder key; an archived project's stale rank | added | `BACKLOG.md` |
| the round's capture script no longer reproduces its captures; the round folder's retirement | added — OPERATOR | `BACKLOG.md` |
| UX4-4 (80×24 hint glyphs only), UX4-5 (the export carries the cursor and empty rows), G-2/G-4 (AT gaps) | added | `BACKLOG.md`; `04-validation.md` |
| the earlier OPERATOR items (`selected: no dates`, the Slide view, page snapping) | carried, unchanged | `BACKLOG.md` |

---

## 5 · Batch metrics — the 13 keys of `core`

Extract, do not invent: a key the artifacts did not record goes `null`, and the key is never dropped.

```yaml
type: dev-flow-batch
project: taskboard
batch_id: 2026-10-19-batch-01
mode: core
verdict: pass
increments: 6
source_files_max: 3              # increment 004 (app.py, modals.py, views.py)
notices_raised: null             # PLAN.md declares NOTICEs per gate as ids and counts, not one id per line
rework_returns: 1                # P2 iterate-to-refine (iterations_per_station P1 = 1)
triggers_fired: "A2,A3,B1,B3,B4,C1,C4,C5,C8,D1,E1"
tests_base_to_post: "2758 -> 2819"
new_control: none
open_items_next: 11              # the 2026-10-19-batch-01 lane
```

---

## 6 · Human review ledger — what a human audited, at what depth

| Artifact | Machine verdict (citation) | Human review | Depth | Deliberately NOT reviewed |
|---|---|---|---|---|
| the present-portfolio round (the design) | the round's captures and verdict page | ✅ the operator's verdict «C», «Sí, que persista el orden», «sería útil tener el seleccionador propuesto con (u)», relayed by the orchestrator, 2026-10-19 | `light` | |
| the capture `seq-160x45-4-picker` | — | ✅ the coordinator's review, 2026-10-20 (the blank backdrop) | `light` | |
| `01-requirements.md` / ledger | P2 review (2 iterations), `V26` read | ❌ | `none — reviewed by the architect, qa, ux and security agents, not by a human` | |
| Code and tests | code-reviewer per increment (one BLOCK-UNTIL, resolved); 5 + 6 + 8 + 15 + 2 + 3 + 1 + 2 mutants KILLED | ❌ | `none — agent review only` | not audited line by line |
| `04-validation.md` and the captures | qa-reviewer PASS-WITH-NOTES; ux walkthrough pass-with-notes | ❌ | `none — the captures are produced for the operator's look` | |

- **Human perimeter:** the operator owns the presentation-only order (D2), the `?` help deviation (D8), the split view's 80-column hint, the 80×24 frame without the rail (never shown in the round — `captures/view3-80x24.svg`), the round's retirement, and the look on a real projector (no user evaluation was run).
- **Human review ledger:** human:operator — 1 artifact(s) reviewed, 0 rigorous · human:coordinator — 1 artifact(s) reviewed, 0 rigorous · 3 declared not-reviewed
