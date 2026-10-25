# Batch close — taskboard — Batch 2026-10-24-batch-02

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
| Gate record | `python "C:/Users/jjgh8/.claude/skills/dev-flow/scripts/devflow-validate.py" .` from the project root · exit 0 · 0 block · 152 notice · 2026-10-25 |
| Gated tree | `0e57a0c91197a4501cd866b78cccfd5e2481d05c` · dirty — .dev-flow/BACKLOG.md, .dev-flow/2026-10-24-batch-02/evidence/gate-p5.txt (the close record itself excluded) |
| Requirements canon | `REQUIREMENTS.md` (`repo:REQUIREMENTS.md`) — HLR-2701..2708 and LLR-2701.1..2708.2 folded (close step 1: 23 folded, 0 kept, 0 refused) |

---

## 1 · What changed

The home no longer starts a board nobody opened, and the directories no longer go stale. With several boards, `BoardsHome` shows at start and now touches nothing: no migration, sweep, presence marker, team start or milestone offer, no write to any board file, and so no false «open in another window» notice. The default board's start runs exactly once when the user leaves the home onto it (`enter`, `esc`, the agenda/people jump, `switch_board`); another board picked from the home starts as before and the default board's file is never written. The team identity picker and the milestone offer now open over the chosen board, with the home off the stack. The task editor, the people view, the marks manager and an `@`/`#` search re-read `people.json` and `marks.json` when the file's mtime or size changed, so a person or class another window added appears without a restart; a failed re-read keeps the directory and warns once. Single-board, `--open PATH` and later-`B` paths behave as before.

Not cured: the blank screen behind the start-up modals (BACKLOG D-12). The offer still opens over an unpainted backdrop, also on a single-board start (QA-P4-04, probe `{'home->offer': 0, 'single->offer MilestoneOffer': 0}`); this batch fixed the stack, not what the user sees. D-12 stays open in `BACKLOG.md`.

Mechanism: `app.py` splits `on_mount` into the read-only start work and a deferred start gated by a started-record (one board id, written only on a completed start, restored by `switch_board` on a failed switch), run from `BoardsHome.action_open`/`action_back`, `switch_board`'s same-board branch and `open_on_board`; `_enter_presence` is called only inside a board start. `people.Directory.refresh()` and `marks.Directory.refresh()` (mtime/size-gated, in-place swap through `_hold`, the stamp set at load and after each own write) are driven by `TaskboardApp._refresh_directories()` at the four seats, and by `SearchPrompt(on_directory_query=…)` for the `/` search. 6 real Windows Terminal captures (`evidence/captures/png/`): the quiet home, the offer over the board, the open-twice + sweep stack, at 118×30 and 80×24.

| Requirement | Version | Verified by | Verdict |
|---|---|---|---|
| HLR-2701 / LLR-2701.1, LLR-2701.2 | P1 contract, three P2 rounds | AT-2701 | pass |
| HLR-2702 / LLR-2702.1, .2, .3, .4 | same | AT-2702 · AT-2703 · TC-2703 | pass |
| HLR-2703 / LLR-2703.1 | same | AT-2704 | pass |
| HLR-2704 / LLR-2704.1 | same | AT-2705 (the identity-picker half: QA-P4-01, bounded) | pass |
| HLR-2705 / LLR-2705.1 | same | AT-2702's notice clause · AT-2408/AT-2409 arms | pass |
| HLR-2706 / LLR-2706.1, .2, .3 | same | AT-2706 · TC-2701 (people, marks) · the D3 node (the `/ #…` half: G-002) | pass |
| HLR-2707 / LLR-2707.1 | same | AT-2707 · TC-2702 (people, marks) (the empty-parse boundary: QA-P4-03) | pass |
| HLR-2708 / LLR-2708.1, .2 | same | the permitted-diff arms of `test_boards.py` and `test_boards_backlog_round.py` · the full suite | pass |

All in the Phase-4 gate run: 3248 passed + 1 environmental skip = 3249 collected, 0 failed (`evidence/suite-p4-chunk00..02.txt`, the orchestrating chain, at `8baf9ad`; the skip is TC-1902's machine-refusal arm, G-001, itemized by the qa-reviewer and closed as environmental). The independent qa-reviewer's verdict is PASS-WITH-NOTES: 0 blocker, 0 major, 8 minor (`04-validation.md`).

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

- **New controls:** none — the batch's findings were caught by controls the flow already has: increment 001's `open_on_board` pending-start hole (F1) by the code-reviewer's first round and its discharge by a named mutation; the three P2 rounds by the two lenses. A candidate for the operator's flow work, not minted here: the gate transcripts should carry the command line and the commit (QA-P4-06).

---

## 3 · Working-file reconciliation (C-44)

| File | State | Evidence |
|---|---|---|
| `taskboard/app.py`, `taskboard/modals.py`, `taskboard/people.py`, `taskboard/marks.py` | ✅ committed on the local branch `fix/home-deferred-start`; push and merge NOT authorized (the commission) | `9a843c4` (app.py, increment 001), `bfe4e64` (all four, increment 002) |
| `tests/test_home_deferred_start.py`, `tests/test_directory_refresh.py` (new); `tests/test_boards.py`, `tests/test_boards_backlog_round.py` (re-timed, named in the packets) | ✅ committed on `fix/home-deferred-start` | `9a843c4`, `bfe4e64` |
| `docs/ARCHITECTURE.md`, `REQUIREMENTS.md` | ✅ committed | `e7cf037` (the ARQ map), the close commit (the canon fold) |
| `.dev-flow/2026-10-24-batch-02/**` (plan, contract, ledger, review, PDR/DDR, the two packets, `04-validation.md`, the evidence, the 6 captures) | ✅ committed on `fix/home-deferred-start` | `8e3990e`, `a420d50`, `e441827`, `9c614bc`, `8baf9ad`, `0b16ae4`, `10ce766`, `df6fa9b`, `32cafd3`, `99d44b0`, the close commit |
| `.dev-flow/BACKLOG.md`, `.dev-flow/state.json`, `PLAN.md`, `05-close.md` | ✅ committed on `fix/home-deferred-start` | the close commit |
| `.scratch/` (rollover and probe scripts) | 🗑️ deleted at close (git-excluded; nothing running) | removed before the commit |
| the capture harness's synthetic homes and `h01-` windows | 🗑️ removed by the harness after each shot | `evidence/captures/capture-log.txt` |

- **Found before the batch:** `none — no tracked file was modified when the batch began`

### Conditional-gate discharge

- **Conditional-gate discharge:** 3 condition(s) · ⚠ 1 outstanding, named below (qa-m9, a declared LOW carry; no gate closed conditionally on it)

| Condition | Discharged? | The artifact line that proves it |
|---|---|---|
| the DDR's ux-1 (offer-over-board captures at 118×30 and 80×24) | ✓ at P4 | `04-validation.md` §DDR conditions that land at P4, ux-1 row |
| the DDR's ux-2 (the quiet-home frame and the toast-stack frame) | ✓ at P4 | the same table, ux-2 row |
| the DDR's qa-m9 (the `/` `#…` half has no named assertion) | ✗ carried open, declared | `04-validation.md` G-002; `BACKLOG.md` §*Open — after `2026-10-24-batch-02`* |

---

## 4 · Backlog reconciliation — the carry-over contract

| Item | Move | Reference |
|---|---|---|
| the false open-twice notice on the home (HD-3) | ✓ done | `BACKLOG.md` §*Open — after `2026-10-24-batch-02`*; `9a843c4` |
| the directories not refreshing across windows (A-7 of the people round; HD-5) | ✓ done | the A-7 line, marked done in place; `bfe4e64` |
| the home defers the board's start (the commission) | ✓ done | the section's first line; `9a843c4` |
| D-12, the blank screen behind the start-up modals | open, reworded — the stack moved onto the chosen board, the blank backdrop NOT cured (QA-P4-04) | the D-12 line, reworded in place |
| QA-P4-01, 02, 03, 05, 06, 07 | added as open LOW items | the new section |
| QA-P4-08 (the LLR count) | n/a — corrected in `04-validation.md` at the return | `04-validation.md` Requirements line |
| G-002 / qa-m9 | carried open (LOW) | the new section |
| G-001 (the TC-1902 clipboard skip, fired again) | closed as environmental at P4; the re-run note kept | the new section |
| every other item of the earlier sections | carried, unchanged | `BACKLOG.md` |

---

## 5 · Batch metrics — the 13 keys of `core`

Extract, do not invent: a key the artifacts did not record goes `null`, and the key is never dropped.

```yaml
type: dev-flow-batch
project: taskboard
batch_id: 2026-10-24-batch-02
mode: core
verdict: pass
increments: 2
source_files_max: 4          # increment 002: people.py, marks.py, app.py, modals.py (the fourth declared in its packet: the PDR-#D3 search seat)
notices_raised: null         # not tallied in PLAN.md for this batch
rework_returns: 2            # P2 round 1 iterate-to-refine; increment 001's code-review round 1 (F1)
triggers_fired: "A2,B1,D1"   # PLAN.md §Triggers
tests_base_to_post: "3236 -> 3249"
new_control: none
open_items_next: 9           # BACKLOG.md §Open — after 2026-10-24-batch-02: D-12, QA-P4-01/02/03/05/06/07, G-002, the clipboard re-run
```

---

## 6 · Human review ledger — what a human audited, at what depth

| Artifact | Machine verdict (citation) | Human review | Depth | Deliberately NOT reviewed |
|---|---|---|---|---|
| `01-requirements.md` / the contract | P1 gate 0 block; P2 final round both lenses PASS | ❌ | `none` | |
| `design/PDR-2026-10-24-batch-02.md` | the architect's verdict folded at seal | ❌ | `none` | |
| the two increment packets | code-reviewer PASS (F1 folded and re-read); mutation batteries 24 + 30 arms KILLED | ❌ | `none` | |
| `design/DDR-2026-10-24-batch-02.md` | qa + ux roles, approved with conditions | ❌ | `none` | |
| Test cases / ATs | 3248 passed + 1 env skip; the ledger 3236 + 13 = 3249 reconciled | ❌ | `none` | |
| the 6 captures | the qa-reviewer read all 6 (three verdicts) | ❌ | `none — expert inspection by a spawned role, not a user` | real-user evaluation (none exists) |
| Evidence view | validator `--brief` 0 block at the close | ❌ | `none` | |
| Code | gates + reviewer verdicts | ❌ | `none` | not audited line by line by a human |

- **Human perimeter:** the operator owns the verdicts this batch cannot take: whether D-12 stays open (the orchestrator ruled it open; the blank backdrop is what the user sees), the clipboard skip (G-001, accepted as environmental), and the merge. Push and merge stay the operator's.
- **Human review ledger:** none — the batch ran autonomously under the commission's standing authorization; every audit above is a machine gate or a spawned reviewer role, and the human-decision items are queued in `BACKLOG.md`.
