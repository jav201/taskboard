# Batch close — taskboard — Batch 2026-10-21-batch-01

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
| Gate record | `python "C:/Users/jjgh8/.claude/skills/dev-flow/scripts/devflow-validate.py" --brief .` from the project root · exit 0 · 0 block · 2026-10-21 (`evidence/gate-p5.txt`) |
| Gated tree | `67ef2e3` (the P4 commit) · dirty — the close's own writes only: `REQUIREMENTS.md` (the fold), `.dev-flow/BACKLOG.md`, `.dev-flow/state.json`, `PLAN.md`, `05-close.md`, `evidence/gate-p5.txt`; committed together as the close commit |
| Requirements canon | `REQUIREMENTS.md` (`repo:REQUIREMENTS.md`) — HLR-2501..2507 and LLR-2501.1..2507.1 folded (close step 1: 21 folded, 0 kept, 0 refused) |

---

## 1 · What changed

The people round is in the app, as the operator's verdict chose. One directory of people (name, role, note) at `~/.taskboard/people.json` serves every board. In a task's notes, `@` opens a picker under the cursor that narrows by typing and can add a person in place; the note stores `@handle`. `@` opens the people view, titled `PEOPLE · directory`: A's two panes (who needs the operator most | that person's open tasks of every board), C's mentioning note line under each task, and B's box `N late · N today · N open`. `/` then `@` filters the kanban or the gantt to one person's tasks, names only, with `alt+p` opening their page. A mention is drawn `@Name` in pink in the details, on the kanban card and in the presentation. View `9` keeps the team `People` (D4).

Mechanism: `people.Directory` (lock, atomic read-modify-write, corrupt copy via `boards.keep_aside`), the tokeniser (`mention_ids`, `split_mentions`, `handle_for`), `Board.people` (never saved); `modals.pick_rows`, the `TaskModal` picker, `PersonForm`, `SearchPrompt`; `views.render_people_directory`, `progress_box`, `matches`/`filter_bar`, the mention painting; `app.PeopleDirectory`, `board_lanes`/`open_on_board` shared with the agenda.

| Requirement | Version | Verified by | Verdict |
|---|---|---|---|
| HLR-2501 / LLR-2501.1, LLR-2501.2, LLR-2501.3 | LED .1, .2, .3, .7 | AT-2501 · TC-2501 | pass |
| HLR-2502 / LLR-2502.1 | LED .1, .2, .3, .7 | AT-2502 · TC-2502 | pass |
| HLR-2503 / LLR-2503.1, LLR-2503.2 | LED .1, .2, .4, .7 | AT-2503 ×2 · TC-2503 | pass |
| HLR-2504 / LLR-2504.1, LLR-2504.2, LLR-2504.3 | LED .1, .2, .5, .7 | AT-2504 ×2 · TC-2504 · TC-2407 | pass |
| HLR-2505 / LLR-2505.1, LLR-2505.2 | LED .1, .2, .6, .7 | AT-2505 ×2 · TC-2505 · TC-2407 | pass |
| HLR-2506 / LLR-2506.1, LLR-2506.2 | LED .1, .2, .3, .7 | AT-2506 ×2 · TC-2506 | pass |
| HLR-2507 / LLR-2507.1 | LED .1, .2, .3, .7 | AT-2507 · TC-2507 | pass |

All in the Phase-4 gate run: 3152 passed, 0 failed, 0 skipped (`evidence/suite-p4-chunk00..02.txt`, the orchestrator, at `27d155f`).

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

- **New controls:** none — the one HIGH of the batch's gates (QA-DDR-1: several `test_AT_*` defs per AT, each driving part of its threshold) was caught by a control the flow already has (C-18 at the DDR) and folded there (LED .7). A candidate for the operator's flow work, not minted here: C-18 checked per increment (one `test_AT_` def per AT at each packet) would have caught it at P3.

---

## 3 · Working-file reconciliation (C-44)

| File | State | Evidence |
|---|---|---|
| `taskboard/people.py` (new), `models.py`, `boards.py`, `app.py`, `views.py`, `modals.py`, `keymap.py` | ✅ committed on the local branch `feat/people`; push and merge NOT authorized (the commission) | `7c87311`, `caef748`, `6dcbeed`, `b473003`, `d1033b0` |
| `tests/test_people_directory.py`, `test_people_look.py`, `test_people_picker.py`, `test_people_view.py`, `test_people_search.py`, `people_round_fixture.py` (new); `test_modal_keys.py`, `test_keymap.py`, `test_readme.py`, `test_boards_concurrency.py` updated | ✅ committed on `feat/people` | the increments' commits; the DDR's folds `27d155f` |
| `README.md`, `docs/ARCHITECTURE.md`, `REQUIREMENTS.md` | ✅ committed on `feat/people` | `db3d562`, `b473003`, `d1033b0`; the canon in the close commit |
| `.dev-flow/state.json`, the rollover | ✅ committed | `76c6011` and the batch's commits |
| `.dev-flow/2026-10-21-batch-01/**` (plan, contract, ledger, review, design records, packets, validation, evidence, captures) | ✅ committed on `feat/people` | the batch's commits; the close commit |
| `.dev-flow/2026-10-21-batch-01/05-close.md`, `.dev-flow/BACKLOG.md` | ✅ committed on `feat/people` | the close commit |
| the capture harness's synthetic homes (`%TEMP%\p01-cap-*`) and window scripts | 🗑️ removed by the harness after each shot | `evidence/captures/png/capture-log.txt` |
| the orchestrator's scratch (`<scratchpad>/p01/`, the draft tree and helper scripts) and the reviewers' scratch copies | 🗑️ removed at the close | the hand-back |

- **Found before the batch:** `none — no tracked file was modified when the batch began`

Increment 004's packet §2 was re-written at the close to name `tests/test_keymap.py` and `tests/test_readme.py` one row each (the content unchanged; `V59` reads one file per cell).

### Conditional-gate discharge

- **Conditional-gate discharge:** 4 condition(s) · ✅ all discharged — the PDR's `approved with conditions` (PC-1..PC-4), re-read at the DDR (`design/DDR-2026-10-21-batch-01.md` §B); PC-1's hand-over to the operator is this close's (§6).

| Condition | Discharged? | The artifact line that proves it |
|---|---|---|
| PC-1 real captures of each shipped item, item 1's composed frame among them; UX-9 named | ✓ | `evidence/captures/png/` (30 PNGs), the composed frame `pv_118x30.png`, `pv_80x24.png`; UX-9 on `evidence/captures/README.md` |
| PC-2 security S-1 re-checked at increment 001 | ✓ | `03-increments/increment-001.md` §4b (security-reviewer APPROVE) |
| PC-3 each increment green on its own and touched suites | ✓ | `suite-001..005.txt`; the P4 gate run over the whole tree (`suite-p4-*`) |
| PC-4 RED and mutation battery per increment | ✓ | `red-001..005.txt`, `mutation-001..005.txt` (`not killed: 0` each) |

---

## 4 · Backlog reconciliation — the carry-over contract

| Item | Move | Reference |
|---|---|---|
| the people round (items 1–4, D1–D5, the storage verdict `handle`) | ✓ done | `BACKLOG.md` §*Open — after `2026-10-21-batch-01`* (the done line); the batch's commits |
| the presentation's split view drawing `!!…!!` / `++…++` raw (logged, NOT fixed, as commissioned) | added | the same section |
| `PersonForm` clipped at 80×24 (UX-DDR-1); the acceptance arms still setting some state directly (QA-DDR-2, QA-DDR-4) | added | the same section |
| deleting a person; mentions in the focus snippet, swimlanes and HTML report; the team roster apart (D4); `handle_for`'s NFKD limit; S-2, S-3, S-5, CR-7/N-1; UX-11; A-7 | added | the same section |
| OPERATOR — the composed people view's verdict (the box's order `late · today · open` vs the spoken «late open today», D-3; D-6; D-7) | added | the same section; `evidence/captures/README.md` |
| every other item of the earlier sections | carried, unchanged | `BACKLOG.md` |

---

## 5 · Batch metrics — the 13 keys of `core`

Extract, do not invent: a key the artifacts did not record goes `null`, and the key is never dropped.

```yaml
type: dev-flow-batch
project: taskboard
batch_id: 2026-10-21-batch-01
mode: core
verdict: pass
increments: 5
source_files_max: 4              # increments 001 and 004 (declared in their packets' §2)
notices_raised: null             # PLAN.md declares NOTICEs per gate as ids and counts, not one id per line
rework_returns: 3                # increment 003 FIX FIRST (LED .4); increment 004 FIX FIRST (LED .5); the DDR's folds (LED .7)
triggers_fired: "A1,A2,A3,B1,B4,C3,C6,C8,D1,E1"
tests_base_to_post: "3025 -> 3152"
new_control: none
open_items_next: 13              # the new BACKLOG section's open items
```

---

## 6 · Human review ledger — what a human audited, at what depth

| Artifact | Machine verdict (citation) | Human review | Depth | Deliberately NOT reviewed |
|---|---|---|---|---|
| the round's verdict (D1–D5, storage, items 1–4, item 1's objection) | — | ✅ the operator's verdict on `prototypes/people_round/`, relayed in the commission of 2026-10-21 | `light` | |
| `01-requirements.md` / ledger | P2 review, `V26` read | ❌ | `none — reviewed by the architect, qa, ux and security agents, not by a human` | |
| Code and tests | code-reviewer per increment (OK to advance ×5), security APPROVE at 001 and 002; 17 + 14 + 13 + 19 + 13 + 2 mutants KILLED | ❌ | `none — agent review only` | not audited line by line |
| the real captures (`evidence/captures/png/`), the composed people view `pv_*.png` | ux-reviewer at the DDR | ❌ | `none — handed to the operator for the verdict (PC-1)` | the composed frame A + C + B was never rendered in the round |
| the Phase-4 gate run and `04-validation.md` | 3152 passed; qa-reviewer PASS-WITH-NOTES | ❌ | `none — run under the standing authorization` | the transcripts |

- **Human perimeter:** the operator owns whether to push and merge `feat/people`; the verdict on the composed people view (`evidence/captures/png/pv_118x30.png`, `pv_80x24.png`) and the box's order (D-3); D-6 (`n`/`e`/`/` act), D-7 (`enter` goes to the tasks); whether `PersonForm`'s 80×24 clip is fixed next; the logged split-view markers.
- **Human review ledger:** human:username_subject — 1 artifact(s) reviewed, 0 rigorous · 4 declared not-reviewed
