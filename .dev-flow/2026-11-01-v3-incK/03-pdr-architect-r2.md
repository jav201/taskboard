**Verdict: PASS-WITH-NOTES** — closed: HIGH 1/1, MAJOR 4/4 · new: HIGH 0, MAJOR 0, MEDIUM 1 (ARCH-12), MINOR 1 (ARCH-13)

# Inc K — PDR round 2 (blocking-only re-review) — architect

Scope: whether ARCH-1..ARCH-5 are closed by commit 88c48f3 (`03-pdr-rulings.md` §Round 1, `03-e3-corrections.md`), and whether the corrections added a new HIGH or MAJOR. Evidence marks: `executed` = a probe ran (`%TEMP%/incK-pdr-architect/`, `anaconda3/python.exe -I`); `read` = from the text cited.

## Round-1 blocking findings

| Finding | State | Evidence |
|---|---|---|
| ARCH-1 (HIGH) union loses/returns notes | **closed** | `executed`: `p6_union_r2.py` is a line-for-line reference of the corrected `Inbox.write_pad` (graph-proto-S: ops on the fresh state, then the typing union with unseen entries as a multiset). Results below the table. LLR-4407.19, .48, .49, TC-4599 arms, TC-4688, TC-4689 and AT-4408 (D, U, R) pin each case, and each NC names the old behaviour. |
| ARCH-2 (MAJOR) choice by index, batch rebuild | **closed** | `read`: `options_for`'s `key`/`chosen` is identity-based and falls back to the top choice. `action_other` stores `key(next)`. `ReviewList.action_dump` fixes `targets` before the loop and calls `dump_part(…, target=…, rebuild=False)`, then one `_rebuild_docs`. TC-4517 arm 2 and TC-4577 reuse the round-1 probe values. |
| ARCH-3 (MAJOR) capture over the deferred home | **closed** | `read`: `check_action` returns False for `capture` with a BoardsHome on the stack, checked before the always-allowed branch (LLR-4401.19, TC-4419). LLR-4401.14's threshold is taken off the home. |
| ARCH-4 (MAJOR, scope) flagged notes | **closed** | `read`: LLR-4407.26/.30–.34 are withdrawn, the `flagged` key and `Inbox.flag`/`flag_for`/`_unsaved_flags` are gone, and an app-level `Inbox.pending` holds a record or drop. It is retried first at every later pad write (LLR-4407.41) and shown on reopen through `pad_now` (LLR-4407.42). Undo can reach it (LLR-4405.18, TC-4558). `executed`: a pending record followed by an undo over a changed file gives `a\|c\|b`, with `b` once. The exit-before-retry risk is recorded (RISK-ARCH-4). |
| ARCH-5 (MAJOR, test design) vacuous NCs | **closed** | `read`: TC-4403's NC is now "the pad not focused at open"; it fires because `N` then pushes AddedList over the view. TC-4482's control arm is the deterministic `"x"×9 995 + " eval harness"` → 0.3128 vs 0.7077. TC-4486 runs 2 subprocesses with `PYTHONHASHSEED` 0 and 1. TC-4412 swaps `cursor` for `archive` plus an arrow-key arm (ARCH-9 too). |

`p6_union_r2.py` results (ARCH-1):

| Case | Stored pad | `dumped` |
|---|---|---|
| D | `a\|c` | `[b]` |
| D, with unsaved typing | `a\|c\|x` | — |
| U | `a\|c\|d\|b` | `[]` |
| U, already undone elsewhere | `a\|b` (`b` once) | — |
| R | `x\|follow up` | — |
| AT-4408 | `a\|c\|d` | — |

The round-1 failures are gone. The ruled "a dump/undo write also carries the unsaved typing" step adds no new loss path (case "D, with unsaved typing").

## New on the corrected design

### ARCH-12 — MEDIUM — LLR-4403.30/.31 can show one option and dump another, and after LLR-4403.29 they are no longer needed
- **Anchor:** LLR-4403.30, LLR-4403.31; graph-proto-V `CaptureView._paint` (`score`, `_drawn` keyed by note POSITION), `on_text_area_changed` (`_idle`), `options_for` (called on demand by `alt+d`/`alt+o`/`alt+n`/`alt+a`).
- **What is wrong:** for up to 1.0 s after an edit, an uncomputed note shows the option lines last drawn at its position. Those can belong to the note's previous text, or to another note once a new divider shifts positions. `alt+d` pressed in that second dumps to the freshly computed option, not the one on screen. This is the same shown-vs-used gap as ARCH-2, bounded to 1 s. The `Dumped →` notice names the real target and `alt+u` reverts it, so this is not MAJOR.
- **Why the feature can go:** with LLR-4403.29 (idf, vectors and norms once per build), one `suggest` call costs 2.7 ms at 300 documents (TC-4489, executed by the correction pass). Scoring on every keystroke is then far under a frame.
- **Proposed change (prefer removing):** withdraw LLR-4403.30 and LLR-4403.31 together with `_drawn`/`score`/`_idle` scoring, and score on paint as in round 1. TC-4489's < 20 ms threshold already guards the cost.
- **If the operator keeps the pause:** draw an uncomputed note's option line as a neutral `→ …`, never another position's lines.

### ARCH-13 — MINOR (pre-existing, not introduced) — an explicit pick is lost on any edit of its note
- **Anchor:** LLR-4404.17 (`choice` keyed by the note's exact text).
- **What is wrong:** `alt+o`, then one typed character, resets the note to its top choice. This was in round 1 too; ARCH-2's fix covers rebuilds, not edits.
- **Proposed change:** none required. Either note it for the operator, or carry the key across an edit of the cursor's note (same position, previous text's key).

### Checked, no new finding
- **Pending ops order and dedup:** a record already held is skipped, and a failed call appends only the `record`/`drop` it was given, so a retry never duplicates (graph-proto-S `Inbox.write_pad`). `read` + `executed`.
- **An edited copy in another window:** that window turned `b` into `b2`, then this window dumped `b`. The stored pad keeps `b2`, so there is no loss and no exact duplicate (`executed`, "D edited elsewhere"). INFO only.
- **SEC-5 quit-retry (`action_quit`):** it touches the key seat only through `quit`, which the holding tuple already allows. `read`.
