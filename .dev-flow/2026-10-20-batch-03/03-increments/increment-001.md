# Increment 001 — LLR-2406.1, LLR-2407.1 · `a direct, shown key for every modal button`

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
> `.dev-flow/2026-10-20-batch-03/03-increments/increment-001.md`. It is not synced to the vault.

> **Notice convention.** `⚠` yellow = notice: does not block, obliges you to DECLARE the reason here.
> `✗` red = block. `✓` green = satisfied **with its evidence cited**. A notice repeated for three
> consecutive batches becomes a rule or is retired.

> **A table you may delete.** A table whose `| **Field** |` row reads `none — <reason>`, or whose question one line of the gate checklist answers, may be deleted, its field row kept: `stations/core-runbook.md` §*A minimal increment packet* is a one-function change written that way.


| Field | Value |
|---|---|
| Batch | `2026-10-20-batch-03` |
| Increment | `001` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | `HLR-2406`, `HLR-2407` / `LLR-2406.1`, `LLR-2407.1` |
| Acceptance | `AT-2406`, `AT-2407` · white-box `TC-2406`, `TC-2407` · unit: `key_line`'s fit (words before keys) and the inventory law (Layer 0: the fit's three branches; the law over every `ModalScreen`) |
| Agent | `software-dev` (the orchestrator, self-implemented; drafted in the scratch worktree, ported here) |
| Date | `2026-10-20` |

---

## 1 · What changed

Every modal button now has a direct key written on the modal (the operator's objection to the round's item 6, D-6). `ConfirmModal` confirms on `y` and cancels on `n`/`esc` — both press its buttons — shows `y <word>   n / esc cancel   ⇥ the buttons` under them, and wraps its message instead of cutting it (D-7: the round's «…its folder is not» finding is fixed); a stray `enter` still answers nothing. `MoveConfirm` takes the same standard: `y` moves, `n`/`esc` cancel, `enter` no longer moves (ux UX-2). Beside text fields the buttons take `alt+<letter>`: `alt+s` Save in the task, project, template, clocks and text-prompt forms, `alt+i` Paste image, `alt+t`/`alt+d` the start/due calendars — each bound to `press_button(<id>)`, so the key and the button are one path (architect A-7) — and each form shows a key line (`↵ / alt+s save` where `enter` already saves); the full-screen task editor gains a last row whose words go before its keys when narrow. `keymap.key_line` draws every key line in the key bar's style.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/keymap.py` | source | LLR-2406.1 | `key_line` (new) |
| `taskboard/modals.py` | source | LLR-2406.1, LLR-2407.1 | `ButtonKeysMixin` (new); the forms' `alt` keys and key lines; `#task-keys`; `ConfirmModal`'s `y`/`n` and key line; `MoveConfirm`'s `y`/`n`, no `enter`, its key line |
| `taskboard/taskboard.tcss` | source | LLR-2406.1, LLR-2407.1 | `#confirm-box .modal-title { width: 100% }`; `#task-keys { height: 1 }` |
| `tests/test_modal_keys.py` | test | HLR-2406, HLR-2407, LLR-2406.1, LLR-2407.1 | new: TC-2406, AT-2406, TC-2407 (the inventory law), AT-2407 |
| `tests/backlog_round_fixture.py` | fixture | HLR-2406 | new: the round's boards, copied from `prototypes/backlog_round/fixture.py` |
| `tests/test_boards_move.py` | test | HLR-2406 | law-driven: a move confirmed with `y` (was `enter`); the round's box row `↵ move … esc cancel` read as `y move … n / esc cancel` (PDR PC-2) |
| `tests/test_boards_concurrency.py` | test | HLR-2406 | law-driven: the moves of AT-2302 and AT-2303 confirmed with `y` (PDR PC-2) |
| `.dev-flow/2026-10-20-batch-03/evidence/mutate-001.py` | doc | HLR-2406, HLR-2407 | the increment's mutation battery |

| Count | Value |
|---|---|
| **SOURCE files** | **3 / 4** |
| Test files | 5 (uncapped) |

## 3 · How to test

`python -m pytest -q -p no:cacheprovider tests/test_modal_keys.py` (with `NO_COLOR` unset); the targeted set of `suite-001.txt`; `python .dev-flow/2026-10-20-batch-03/evidence/mutate-001.py`.

## 4 · Test results

| Layer | Nodes | Result |
|---|---|---|
| 0, A and B | `tests/test_modal_keys.py` — 28 nodes: `test_TC_2406_key_line_is_the_key_bar_style_and_keeps_its_keys`, `test_TC_2406_a_confirmation_answers_y_and_n_and_not_enter[4]`, `test_TC_2406_the_message_wraps_and_is_whole`, `test_TC_2406_the_move_confirms_on_y_never_on_enter`, `test_AT_2406_a_confirmation_is_one_written_key[118x30, 80x24]`, `test_TC_2407_alt_s_does_what_save_does[5]`, `test_TC_2407_alt_t_and_alt_d_open_the_calendars[4]`, `test_TC_2407_alt_i_pastes_an_image`, `test_TC_2407_every_modal_is_in_the_inventory`, `test_TC_2407_every_button_has_its_key[6]`, `test_AT_2407_alt_s_saves_and_letters_type[118x30, 80x24]` | executed: 579 passed in the targeted run of the new file and every suite B1 names, after the code review's fixes (`suite-001.txt`) |
| full suite | owed at the P4 gate run | not-run |

| Field | Value |
|---|---|
| **RED counterfactual** | on `base_ref`'s code (the branch at `ee7a285`, `taskboard/` untouched, the two new test files copied in): 26 failed, 2 passed — the two passing are the boundary arms `escape` and `enter` (TC-2406), which already answer False / nothing · `.dev-flow/2026-10-20-batch-03/evidence/red-001.txt` |
| **Mutation verdicts** | 17 arms over 13 mutants, one run, each restore proven by digest: `y` unbound · KILLED ×2 (TC, AT); the wrap rule dropped · KILLED ×2; a key dropped before the words · KILLED; the slash styled as a key · KILLED; `alt+s` pressing Cancel · KILLED ×2 (TC, AT); `alt+t` opening the due calendar · KILLED; `alt+i` unbound · KILLED; the project form without its date keys · KILLED; `ConfirmModal`'s key line emptied · KILLED; the editor's key line emptied · KILLED; `MoveConfirm` confirming on `enter` again · KILLED ×2; `TextPrompt`'s line without `alt+s` · KILLED; a button key unbound (the law) · KILLED · arms that stayed GREEN: none · `.dev-flow/2026-10-20-batch-03/evidence/mutation-001.txt` |
| **Instrument RED-proof** | 1 instrument: `evidence/mutate-001.py` — batch 2026-10-20-batch-02's harness (its RED seen there: a `BAD` anchor and a `SURVIVED` arm) with this increment's arms; `arms: 17` |
| **Emitted-form assertion** | none — this increment emits no artifact (the modals answer their callers; the move's files are batch-02's, re-asserted unchanged by its suites) |
| **Reverse census** | 4 probes: B1 `grep -rln "ConfirmModal\|MoveConfirm\|TaskModal\|ProjectModal\|TextPrompt\|ClockModal\|TemplateEditor\|KEYMAP" tests/` → `test_app.py`, `test_archive.py`, `test_boards_home.py`, `test_links.py`, `test_markup_census.py`, `test_markup_sites.py`, `test_boards_move.py`, `test_boards_concurrency.py`, `test_details_grid.py`, `test_edit_window.py`, `test_emoji_picker.py`, `test_link_picker.py`, `test_milestones.py`, `test_present_hide.py`, `test_setup_help.py`, `test_template_new.py`, `test_template_save_app.py`, `test_keymap.py`, `test_help_keys.py` — the move pair updated (law-driven, §2), the rest green unchanged in `suite-001.txt` but for `test_milestones.py`, `test_present_hide.py` and `test_link_picker.py`, which only open the forms (green at P4) · B2 no file moves · B3 no golden capture (the round's `move-160-3-confirm.svg` is a read box the test now compares with the keys row re-worded) · B4 none — no artifact written · 0 foreign hits |
| **Correction population** | 1 correction: the confirmation of a move by `enter`, enumerated by `grep -n '"enter"\|↵ move' tests/test_boards_move.py tests/test_boards_concurrency.py` before the first edit — 8 sites: `test_boards_move.py` 290 and 449 (`enter` → `y`), 364 and 445 (`↵ move` → `y move`), the round-box comparison (its keys row re-worded); `test_boards_concurrency.py` 448, 454, 535 (`enter` → `y`) |

### Evidence files

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| suite-001.txt | .dev-flow/2026-10-20-batch-03/evidence/suite-001.txt | a175da682b590745ea12fc0e9050f612e964c8a1b65af7b7def9c27ef1c784ec |
| red-001.txt | .dev-flow/2026-10-20-batch-03/evidence/red-001.txt | 837b49e5a55da695c00467198be41d46e73f1a9d3cdbc7b49050ddd605429380 |
| mutation-001.txt | .dev-flow/2026-10-20-batch-03/evidence/mutation-001.txt | 6b9305dfb2cf02ebcfba20636494825859adde9d7221e4d15ff74fa9bafe6db7 |
| mutate-001.py | .dev-flow/2026-10-20-batch-03/evidence/mutate-001.py | 76d4edd6794ba7d17c681b129716827ef027fe9806efbcb936554cc60fcb8597 |
| inc001.diff | .dev-flow/2026-10-20-batch-03/evidence/inc001.diff | 4e95031978645f2037bc356cd19c344cf5ebddec0bebe131a1bbd8dae836adf0 |

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a generic agent with agents/code-reviewer.md · **OK to advance** · no HIGH; MEDIUM CR-1 (the project form's key line dropped `cancel`) fixed — shorter words, the law requires `esc cancel`; MEDIUM CR-2 (AT-2407 drove part of its threshold) fixed — the clocks, the template, the notes' height and the cancelled edit's bytes added; LOW CR-3 (a phantom `PresentKeys` row) fixed, CR-4 (`_fold_chips` renamed `_fit_width`) fixed, CR-5 (the law finds buttons by source text) recorded |

## 5 · Risks

`alt+<letter>` arrives as `ESC` + the letter: `esc` then `s` typed inside one read would save rather than cancel (§6.3, accepted). The project form scrolls at 80×24 (as at `base_ref`), its key line under the buttons. The key lines are design the round never rendered: real captures go to the operator at the close (PDR PC-1).

## 6 · Pending items / spec deviations

The full suite is owed at P4. AT-2406's move arm opens the move with `escape`, `P`, `down`, `m`, `enter` (the contract wrote `P`, `m`, `enter`: the projects modal's cursor starts on its heading, so `down` selects the project — a drift of the threshold's keys, recorded in LED .4 at this gate). PC-2 (the `enter` → `y` test updates named here) discharged by §2.

## 7 · Suggested next task

Increment 002 — the presentation (HLR-2402..HLR-2405).

## Increment gate checklist

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | SOURCE budget | ✓ | §2: 3 source files |
| 2 | Tests in this increment | ✓ | `tests/test_modal_keys.py` |
| 3 | Layer 0 where it applies | ✓ | `key_line`'s fit; the inventory law |
| 4 | RED counterfactual | ✓ | §4, `red-001.txt` |
| 5 | Reverse census | ✓ | §4: 4 probes |
| 6 | `code-reviewer` passed | ✓ | §4b |
| 7 | No file from another lane | ✓ | one lane |
| 8 | Frozen interfaces untouched | ✓ | none frozen |
| 9 | Coverage verified on disk | ⚠ | `suite-001.txt` (targeted); the full run owed at P4 |
| 10 | Load-bearing emptiness | ✓ | the census's greps quoted |
| 11 | Mutation verdicts | ✓ | §4: 17/17 KILLED |
| 12 | Instrument RED-proof | ✓ | §4 |
| 13 | Correction population | ✓ | §4: 1, enumerated |
| 14 | Emitted-form assertion | ✓ | §4: none, declared |
| 15 | Independent review | ✓ | §4b |
| 16 | Evidence files | ✓ | §4: the digests |
