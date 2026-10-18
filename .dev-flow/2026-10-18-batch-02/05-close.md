# Batch close — taskboard — Batch 2026-10-18-batch-02

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
| Gate record | `python "C:/Users/jjgh8/.claude/skills/dev-flow/scripts/devflow-validate.py" .` from the project root · exit 0 · 0 block · 58 notice · 2026-10-18 |
| Gated tree | `09033b250911665e000bb274370e2a5b9c14a786` · dirty — .dev-flow/2026-10-07-batch-08/evidence/inc001-brief.md, .dev-flow/2026-10-07-batch-09/evidence/inc001-brief.md, .dev-flow/BACKLOG.md, .gitattributes, .dev-flow/2026-10-07-batch-05/decisions-log.json, .dev-flow/2026-10-07-batch-06/decisions-log.json, .dev-flow/2026-10-07-batch-06/evidence/gen_verdict_sheet.py, .dev-flow/2026-10-07-batch-06/evidence/kanban-demo.json, .dev-flow/2026-10-07-batch-06/evidence/veredicto-batch06.html, .dev-flow/2026-10-07-batch-06/evidence/veredicto-board.json, .dev-flow/2026-10-07-batch-07/decisions-log.json, .dev-flow/2026-10-07-batch-08/decisions-log.json, .dev-flow/rollover_batchg.py, .dev-flow/rollover_batchh.py, .dev-flow/rollover_batchi.py, .dev-flow/rollover_batchj.py (the close record itself excluded) |
| Requirements canon | `REQUIREMENTS.md` (`artifact_homes.requirements_canon`) — `devflow-init.py --fold-canon`: 10 folded, 0 kept, 0 refused (HLR-1901..HLR-1905, LLR-1901.1..LLR-1905.1); the status cell of LLR-1803.2 (the hint's two wordings, 2026-10-18-batch-01) updated by hand: superseded in part by LLR-1904.1 |

---

## 1 · What changed

The suite now reports 0 failures: the two standup tests that broke in the 2026-10-11 name scrub encode their intent again (the scrub put the 16-cell placeholder `username_subject` into the standup's 12-cell name column, which paints it `username_su…`; the tests searched for the whole name — the source was right), and `test_win_clipboard_roundtrip` skips, quoting the refusal, when Windows refuses `Set-Clipboard` on every attempt, while a real roundtrip mismatch or a clipboard that never holds the sample still fails. The presentation (`R`) no longer kills the app below 36 columns: the frame names the width it needs (the longest of five rungs that fits, in `mut`), no key but `esc`/`q` acts there, `x` says why it writes nothing, and widening restores the frame; the hint row shortens in four steps and cuts with a visible `…`. The six prototype round files that no longer import say so in a `HISTORICAL` header. The three polish items (the dim view word and cut marks, the terse 80-column hint, the gantt view's 3-row note cap) are a prototype round for the operator's verdict, with no production change.

| Requirement | Version | Verified by | Verdict |
|---|---|---|---|
| `HLR-1901` | v1 (LED .1–.3) | `AT-1901` · `TC-1901` | PASS (`suite-p4.txt`) |
| `HLR-1902` | v1 (LED .1, .2) | `AT-1902` · `TC-1902` | PASS |
| `HLR-1903` | v1 (LED .1–.4, .6) | `AT-1903` · `TC-1903` | PASS |
| `HLR-1904` | v1 (LED .1, .2) | `AT-1904` · `TC-1904` | PASS |
| `HLR-1905` | v1 (LED .1, .2, .8) | `AT-1905` | PASS |
| `LLR-1901.1` | v1 (LED .1–.3, .5) | `TC-1901`; M1–M3 KILLED | PASS |
| `LLR-1902.1` | v1 (LED .1, .2, .4) | `TC-1902`; M4–M8 KILLED | PASS |
| `LLR-1903.1` | v1 (LED .1–.3, .7) | `TC-1903`; N1–N4, N10–N14 KILLED (N15 an equivalent mutant) | PASS |
| `LLR-1904.1` | v1 (LED .1, .2, .4) | `TC-1904`; N5–N9 KILLED | PASS |
| `LLR-1905.1` | v1 (LED .1–.3, .8) | inspection (`red-003.txt`) | PASS |

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

- **New controls:** none — the lessons met were caught by existing controls: a helper mutant that survived seven planned arms (the PDR's executed mutant, C-40); key pairs that undid each other in an AT (the battery: N12/N13 SURVIVED, C-40); a "not exercised" discharge refused at the DDR, which found `run_test` hides toasts (the conditional-gate re-read, V50's rule); a contract literal off by one cell (TC-1901's first run, C-36).

---

## 3 · Working-file reconciliation (C-44)

| File | State | Evidence |
|---|---|---|
| `tests/test_team_views.py`, `tests/test_app.py`, the six `prototypes/present_{rulers,views}/*.py` round files | ✅ committed on the local branch `backlog-fixes`, not pushed (push not authorized) | `2c6ac76` |
| `taskboard/views.py`, `taskboard/app.py`, `tests/test_present_narrow.py`, `tests/test_present.py` | ✅ committed on `backlog-fixes`, not pushed | `1ba8c3f` |
| `prototypes/backlog_polish/**` (scripts, page, manifest, 46 SVG/PNG pairs), `tests/test_backlog_polish_round.py` | ✅ committed on `backlog-fixes`, not pushed | `627b19d`, `7e849dc` |
| `docs/ARCHITECTURE.md` | ✅ committed on `backlog-fixes`, not pushed | `369cf58`, `fb728e4` |
| `REQUIREMENTS.md` | ✅ committed on `backlog-fixes`, not pushed | the deliverable commit (close step 6) |
| `.dev-flow/state.json`, `.dev-flow/2026-10-18-batch-01/decisions-log.json` (the rollover archive) | ✅ committed on `backlog-fixes`, not pushed | `a641d67`, then each later commit |
| `.dev-flow/2026-10-18-batch-02/**` (contract, ledger, review, design records, packets, validation, plan, evidence: transcripts, the battery) | ✅ committed on `backlog-fixes`, not pushed | `a641d67` … `7e849dc`, the deliverable commit |
| `.dev-flow/2026-10-18-batch-02/05-close.md`, `.dev-flow/BACKLOG.md` | ✅ committed on `backlog-fixes`, not pushed | the close commit (close step 8) |
| 12 stale captures `prototypes/backlog_polish/out/hint80-*-split-hidden-*` (the round's first capture run) | 📋 left on purpose, git-excluded (`.git/info/exclude`): their removal was refused by the runtime's safety check and is the operator's | `BACKLOG.md` (2026-10-18-batch-02 lane) |
| the `tmp*` board directories of the first two capture runs, in the user temp folder | 📋 left on purpose, outside the repository; the operator's removal | `BACKLOG.md` |
| scratch `git worktree`s (`…/scratchpad/wt`, `base`, `p4`) and scratch copies (`red1`, `red2`, `red3`, `mut`, `mut2`) | 📋 left in the session scratchpad, outside the repository (the worktrees registered in `.git/worktrees`); `git worktree remove` is the operator's call (the commission forbids nothing there, but a removal needs approval here) | the RED runs, the batteries and the gate run ran there |
| `.git/info/exclude` (local, unversioned) | two lines added: a comment and `prototypes/backlog_polish/out/hint80-*-split-hidden-*` | this table |

- **Found before the batch:** `.dev-flow/2026-10-07-batch-08/evidence/inc001-brief.md @ a751d73fdcddc239d01f02a2dfcb9ec042222110` `.dev-flow/2026-10-07-batch-09/evidence/inc001-brief.md @ 737b913e5559b8337969790137c4bda87fac2788` `.gitattributes @ 5650216ed19fb4d68b5ae282a0bd5042024dc222`

Also found before the batch, untracked and left alone: `.dev-flow/2026-10-07-batch-0{5,6,7,8}/decisions-log.json`, `.dev-flow/2026-10-07-batch-06/evidence/{gen_verdict_sheet.py,kanban-demo.json,veredicto-batch06.html,veredicto-board.json}`, `.dev-flow/rollover_batch{g,h,i,j}.py`.

### Conditional-gate discharge

- **Conditional-gate discharge:** 7 condition(s) · ✅ all discharged — the PDR's `approved with conditions` (PC-1..PC-6) and the DDR architect lens's DDR-C1, each re-read at the DDR (the table below).

| Condition | Discharged? | The artifact line that proves it |
|---|---|---|
| PC-1 the skip keyed on the last attempt | ✓ re-read by the qa-reviewer at the DDR | `tests/test_app.py` arm `contended-then-refused-x4`; `evidence/mutation-001.txt` M4 KILLED |
| PC-2 the wide-path truncate reachable | ✓ re-read by the architect | `tests/test_present_narrow.py::test_TC_1904_an_overflowing_count_is_cut_visibly`; N7 KILLED |
| PC-3 a reddening mutant per narrow-key guard | ✓ re-read by the architect | AT-1903's keys; N10–N14 KILLED; N15 an equivalent mutant, declared |
| PC-4 AT-1905's corrupted copies; TC-1901's mutant | ✓ re-read by the qa-reviewer | `tests/test_backlog_polish_round.py` (8 arms); M3 KILLED |
| PC-5 the notice seen painted | ✓ by exercise after DDR-C1 | `prototypes/backlog_polish/out/narrow-current-narrow-30x12-x.png` |
| PC-6 `esc`/`q`, the page, the enablers | ✓ re-read by the architect | `design/design-proposal.md` §3, §7; `docs/ARCHITECTURE.md` §4 |
| DDR-C1 PC-5 exercised, not declared | ✓ re-read by the orchestrator | the same capture; `design/DDR-2026-10-18-batch-02.md` §B |

---

## 4 · Backlog reconciliation — the carry-over contract

| Item | Move | Reference |
|---|---|---|
| the 2 standup tests failing since the 2026-10-11 scrub | ✓ done | `2c6ac76` |
| `test_win_clipboard_roundtrip`'s environment failure | ✓ done | `2c6ac76` |
| `render_present` asserts below ~36 columns | ✓ done | `1ba8c3f` |
| the short hint clipped below ~60 columns | ✓ done | `1ba8c3f` |
| the stale PRES-C/PRES-R/"hybrid" comments | ✓ done (the node renames declined) | `1ba8c3f` |
| the two stale prototype scripts (commission) | ✓ done — six round files marked `HISTORICAL` | `2c6ac76` |
| `present_note_lines` wraps by code points (S-3) | ✓ marked done — it had shipped in 2026-10-18-batch-01 | `BACKLOG.md` |
| UX4-2, UX4-3, UX4-4 | → prototyped, awaiting the operator's verdict | `prototypes/backlog_polish/`; `BACKLOG.md` |
| the narrow frame and hint (shipped as FIX) | added — for the operator's review (UX2-2, UX5-1, UX5-2) | `BACKLOG.md` |
| the tick-row label `selected: no dates` | carried — OPERATOR, unchanged | `BACKLOG.md` |
| round 1's Slide view; paging snaps (UX-2/UX-3) | carried — OPERATOR | `BACKLOG.md` |
| Cards view; `_present_ruler` refactor; PNG content assert; the sealed `mutate.py`; `*_presc_frame_*` renames | declined, recorded | `BACKLOG.md` |
| the clipboard restore unchecked (code-review L4) | added | packet 001 §4b |
| the help-modal timing flake | added | `evidence/flake-002.txt` |
| AT-1905's `url(`/`@import` arms; the bold-span mutant (G-5, G-3) | added | `04-validation.md` |
| the stale captures and temp boards; the older `verify_*.py` prototypes | added | packet 003 §6; `PLAN.md` inventory |

---

## 5 · Batch metrics — the 13 keys of `core`

Extract, do not invent: a key the artifacts did not record goes `null`, and the key is never dropped.

```yaml
type: dev-flow-batch
project: taskboard
batch_id: 2026-10-18-batch-02
mode: core
verdict: pass
increments: 3
source_files_max: 2              # increment 002 (taskboard/views.py, taskboard/app.py)
notices_raised: null             # PLAN.md declares NOTICEs as ranges and counts per gate, not one id per line
rework_returns: 2                # P2 iterate-to-refine (iterations_per_station P1 = 1); the ARQ iterate folded in place
triggers_fired: "A2,A3,B1,B3,B4,D1,E1"
tests_base_to_post: "2723 -> 2740"
new_control: none
open_items_next: 9               # the 2026-10-18-batch-02 lane
```

---

## 6 · Human review ledger — what a human audited, at what depth

| Artifact | Machine verdict (citation) | Human review | Depth | Deliberately NOT reviewed |
|---|---|---|---|---|
| the commission's item list and classes | — | ✅ the operator's commission (relayed by the coordinator), 2026-10-18 | `light` | |
| `01-requirements.md` / ledger | P2 review (2 iterations), `V26` green | ❌ | `none — reviewed by the architect, qa and ux agents, not by a human` | |
| Code (`taskboard/views.py`, `taskboard/app.py`) and tests | code-reviewer OK to advance, 0 HIGH (each increment, re-read after its folds); 12/12 and 19/20 mutants KILLED | ❌ | `none — agent review only` | not audited line by line |
| `04-validation.md` | qa-reviewer PASS-WITH-NOTES; ux walkthrough pass-with-notes | ❌ | `none` | |
| the prototype round `prototypes/backlog_polish/backlog-polish-prototype.html` | AT-1905; code-reviewer OK | ❌ | `none — produced for the operator's verdict, not yet seen` | |

- **Human perimeter:** the operator owns the verdict on the three polish items and the review of the shipped narrow frame and hint (the round's page), whether the presentation reads well to a room (no user evaluation was done), the removal of the stale captures, temp boards and scratch worktrees, and the push/merge of `backlog-fixes` (not authorized here).
- **Human review ledger:** human:operator — 1 artifact(s) reviewed, 0 rigorous · 4 declared not-reviewed
