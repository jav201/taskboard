# Increment 003 — LLR-2503.1, LLR-2503.2 · `the @ picker in the editor's notes`

> **Artifact language**
> This template is the canonical **English scaffold**. Generate the artifact in the batch's development
> language — the **prose**, and never a label. **Where that language is declared:**
> `state.json`'s `language` key in `core` and `full`. The normative RULES below are
> language-independent.

> **Owed in.** `core` ✓ · `full` ✓

> **Field guide:** `templates/guides/increment-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

> **Reserved field names.** The **field names and block keywords below are language-independent** — the
> validator parses them literally and they are never translated:
> `SOURCE files` · `Instrument RED-proof` · `Correction population` · `Mutation verdicts` · `Emitted-form assertion` · `Reverse census` · `RED counterfactual` · `Independent review` · `Evidence files` · `Traces to` · `File` · `Kind` · `source` · `test` · `doc` · `config` · `generated` · `fixture` · `⏸ DEFER`
> Everything else on this page — headings, guidance, the prose in every cell — is translated with the batch.
> **One strategy, not two:** the flow ships no alias table, so a translated label is read as an ABSENT one and the rule keyed on it reports a true-sounding silence.
> **And one FLOW-WIDE reserved token, read out of this artifact by `V42` no matter which template minted it:** `⏸ DEFER`. It is a MARKER rather than a field name, which is why it is stated here *and* in `/dev-flow` §Language of artifacts rather than in a per-template list — a deferral can be written in any batch artifact, including the ones that carry no block at all.

> **Where this lives:** the **repo**, next to the diff it describes —
> `.dev-flow/2026-10-21-batch-01/03-increments/increment-001.md`. It is not synced to the vault.

> **Notice convention.** `⚠` yellow = notice: does not block, obliges you to DECLARE the reason here.
> `✗` red = block. `✓` green = satisfied **with its evidence cited**. A notice repeated for three
> consecutive batches becomes a rule or is retired.

> **A table you may delete.** A table whose `| **Field** |` row reads `none — <reason>`, or whose question one line of the gate checklist answers, may be deleted, its field row kept: `stations/core-runbook.md` §*A minimal increment packet* is a one-function change written that way.

| Field | Value |
|---|---|
| Batch | `2026-10-21-batch-01` |
| Increment | `003` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | `HLR-2503` / `LLR-2503.1`, `LLR-2503.2` |
| Acceptance | `AT-2503` · white-box `TC-2503` · unit: `pick_rows` (Layer 0) |
| Agent | `software-dev` (the orchestrator; ported from the frozen draft) |
| Date | `2026-10-21` |

---

## 1 · What changed

The `@` picker in the task editor's notes (the round's item 2, variant A). With the directory, an `@` at a word start opens a dropdown under the cursor. It lists the people the typed text finds (name starts, then inside the name, then the role), then `+ add '<typed>'`. `↑`/`↓` move, `↵` writes `@handle `, `esc` leaves the text as typed. `+ add` turns the dropdown into a small form: the name is prefilled, the role is focused, `⇥` switches between the two fields, `↵` adds the person to the directory and writes the mention, and `esc` goes back to the list. The new person's role is confirmed with `↵`, never `alt+s`, which keeps saving the task. The picker closes whenever the focus leaves it. A held handle followed by sentence punctuation opens nothing. With no one listed, `↵` is a new line. While the picker is closed, every key does what it did before.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/modals.py` | source | LLR-2503.1, LLR-2503.2 | `MENTION_AT`, `DROP_W`, `DROP_ROWS`, `PICK_KEYS`, `ADD_KEYS`, `pick_rows`, `MentionDrop`; `TaskModal(…, people=)`, its picker bindings, `check_action`, `on_descendant_focus`, `_scan`, `_draw_drop`, `_close_drop`, `_insert_mention`, `action_drop_move`, `action_drop_field`, `action_drop_pick`, `action_cancel`'s step back; `import re` |
| `taskboard/app.py` | source | LLR-2503.2 | `a` and `e` pass `people=self.people` to `TaskModal` |
| `tests/test_people_picker.py` | test | HLR-2503, LLR-2503.1, LLR-2503.2 | new: TC-2503, AT-2503 (both sizes; the `tab` path; the flip-up; the add form; the refused add; the focus leaving; the trailing dot; no directory; an empty list) |
| `.dev-flow/2026-10-21-batch-01/evidence/mutate-003.py` | doc | HLR-2503 | the increment's battery |

| Count | Value |
|---|---|
| **SOURCE files** | **2 / 4** |
| Test files | 1 (uncapped) |

## 3 · How to test

`python -m pytest -q -p no:cacheprovider tests/test_people_picker.py` (with `NO_COLOR` unset); the targeted set of `suite-003.txt`; `python .dev-flow/2026-10-21-batch-01/evidence/mutate-003.py`.

## 4 · Test results

| Layer | Nodes | Result |
|---|---|---|
| 0, A and B | `tests/test_people_picker.py` — 19 nodes: `test_TC_2503_rows_list_the_finds_then_add_when_no_name_matches`, `test_TC_2503_a_name_that_looks_like_markup_is_a_text_piece`, `test_AT_2503_at_an_enter_writes_the_handle_and_the_preview_the_name[size0|size1]`, `test_AT_2503_arrows_choose_and_esc_leaves_plain_text`, `test_AT_2503_add_a_person_in_place_for_every_board`, `test_AT_2503_esc_in_the_new_person_goes_back_to_the_list`, `test_AT_2503_a_failed_add_says_so_and_keeps_the_form`, `test_TC_2503_no_picker_inside_a_word_or_on_a_known_handle[×4]`, `test_TC_2503_without_a_directory_at_is_plain_text`, `test_AT_2503_reached_by_tab_the_list_opens_inside_the_screen_and_flips_up`, `test_AT_2503_tab_leaves_the_notes_and_the_mention_as_typed`, `test_TC_2503_closed_the_arrows_move_the_cursor`, `test_AT_2503_the_form_left_for_the_notes_closes_and_writes_nothing`, `test_TC_2503_with_no_one_listed_enter_is_a_new_line`, `test_AT_2503_a_click_away_closes_the_list` | 363 passed with the touched files' suites (`suite-003.txt`: the editor's tab walk `tests/test_edit_window.py`, the modal-key law, the emoji picker, `test_app.py`, the markup census and sites, milestones, the presentation's hide) |
| full suite | owed at the P4 gate run | not-run |

| Field | Value |
|---|---|
| **RED counterfactual** | on increment 002's commit `caef748` (this increment's test file as first written, copied in): collection error, `ImportError` of `MentionDrop` (`red-003.txt`); each assertion's own RED is the battery |
| **Mutation verdicts** | 13 arms, one run, each restore proven by digest: `+ add` for an exact name and `@` alone · KILLED; the picker's keys live while closed · KILLED; the list kept open when a click leaves the notes · KILLED; a known handle reopening the list · KILLED; never flipped up · KILLED; the mention without its space · KILLED; `esc` on the list cancelling the editor · KILLED; a refused add swallowed · KILLED; the app handing no directory · KILLED; `tab` in the form losing the role · KILLED; the form neither gated nor closed when the focus leaves (CR-1) · KILLED; a sentence-final dot reopening the list (CR-2) · KILLED; an empty list swallowing `enter` (CR-4) · KILLED — arms that stayed GREEN: none (`mutation-003.txt`; earlier runs: a SURVIVED focus arm made redundant by the focus rule, re-cut onto that rule; the redundant `tab` close removed with its arm) |
| **Instrument RED-proof** | 1 instrument: `evidence/mutlib.py` (its RED seen in this increment: two SURVIVED arms before the re-cut) |
| **Emitted-form assertion** | 1 artifact: `people.json` after an add — read back as JSON, the new person's record whole (AT-2503) |
| **Reverse census** | 4 probes: B1 `grep -rln "TaskModal(" tests/` → `test_app.py`, `test_edit_window.py`, `test_emoji_picker.py`, `test_markup_sites.py`, `test_milestones.py`, `test_modal_keys.py`, `test_present_hide.py` — all rerun in `suite-003.txt`, green (their editors have no directory, so no picker); the `tab` binding replacing the screen's → `tests/test_edit_window.py::test_tab_walks_the_editor_and_save_works_from_the_keys` green at both sizes; A3 `TaskModal`'s new keyword defaults to None; B4 `people.json` written only through `Directory.add` — 0 foreign hits |
| **Evidence files** | the table under §4 *Evidence files*: each artifact's path and SHA-256 |
| **Correction population** | none — no shipped assertion changed |

### Evidence files

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| suite-003.txt | .dev-flow/2026-10-21-batch-01/evidence/suite-003.txt | 6ae9a28b6fb84730f7b524723d1f9180273ef54323d4dbc7384d0159e34596b3 |
| red-003.txt | .dev-flow/2026-10-21-batch-01/evidence/red-003.txt | 0d4723af97c75cec851be373cdce75da712a68d67be847d246670243c2c1c348 |
| mutation-003.txt | .dev-flow/2026-10-21-batch-01/evidence/mutation-003.txt | 8772ea82335eaec8f29d67e93157f613c0cb512f81c25a4100a4f94479d310cc |
| mutate-003.py | .dev-flow/2026-10-21-batch-01/evidence/mutate-003.py | d414226080be45ca06ccd223b8265ee64b59bf905d2292c155365e247be368c2 |
| inc003.diff | .dev-flow/2026-10-21-batch-01/evidence/inc003.diff | 627c9137ff717eef7a4989bd5896231aaa880fe3e2c68de8047accdb4dd6c2bb |

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a generic agent with agents/code-reviewer.md · first pass **FIX FIRST** (BLOCK-UNTIL CR-1, CR-2), both reproduced on the real editor: CR-1 HIGH (the new person's form kept acting after `shift+tab`: `enter` in the notes added a person and replaced the operator's text) and CR-2 HIGH (`@ana.ruiz.` reopened the picker and created `ana.ruiz2`); resolved by the focus rule, the span guard and the punctuation check, with three new arms and the battery's M12, M13; CR-3, CR-4 (LOW) fixed; **re-read: OK to advance** — both repro probes fail to reproduce (the notes intact, no person added; `@ana.ruiz.` opens nothing); one LOW residual accepted: the list's keys no longer check the notes' focus themselves and rely on `on_descendant_focus` (a focus moving to nothing fires none), the span guard keeping the notes safe |

## 5 · Risks

The picker's `tab` binding replaces the screen's own: it calls `focus_next` when the picker is closed (the tab walk is held). `esc` then a letter typed fast is read as `alt+<letter>` by the parser (2026-10-20-batch-03's accepted risk).

## 6 · Pending items / spec deviations

The full suite is owed at P4.

## 7 · Suggested next task

Increment 004 — the people view on `@` (HLR-2504).

## Increment gate checklist

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | SOURCE budget | ✓ | §2: 2 source files |
| 2 | Tests in this increment | ✓ | `tests/test_people_picker.py` |
| 3 | Layer 0 where it applies | ✓ | `pick_rows` |
| 4 | RED counterfactual | ✓ | §4, `red-003.txt` and the battery |
| 5 | Reverse census | ✓ | §4: 4 probes, 0 foreign hits |
| 6 | `code-reviewer` passed | ✓ | §4b |
| 7 | No file from another lane | ✓ | one lane |
| 8 | Frozen interfaces untouched | ✓ | none frozen |
| 9 | Coverage verified on disk | ⚠ | `suite-003.txt` (targeted); the full run owed at P4 |
| 10 | Load-bearing emptiness | ✓ | the census's greps quoted |
| 11 | Mutation verdicts | ✓ | §4: 13/13 KILLED |
| 12 | Instrument RED-proof | ✓ | §4 |
| 13 | Correction population | ✓ | §4: none, declared |
| 14 | Emitted-form assertion | ✓ | §4 |
| 15 | Independent review | ✓ | §4b |
| 16 | Evidence files | ✓ | §4: the digests |
