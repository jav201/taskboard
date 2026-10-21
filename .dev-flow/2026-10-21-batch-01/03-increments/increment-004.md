# Increment 004 — LLR-2504.1, LLR-2504.2, LLR-2504.3 · `the people view on @`

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
| Increment | `004` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | `HLR-2504` / `LLR-2504.1`, `LLR-2504.2`, `LLR-2504.3` |
| Acceptance | `AT-2504` · white-box `TC-2504`, `TC-2407` (the modal law over `PersonForm`) · unit: `person_items`, `people_by_urgency`, `progress_box`, `_scroll_tasks`, `render_people_directory` (Layer 0) |
| Agent | `software-dev` (the orchestrator; ported from the frozen draft) |
| Date | `2026-10-21` |

---

## 1 · What changed

`@` opens the people view, the round's item 1 composed as the operator's objection asks. The base is A's two panes. On the left are the directory's people, most late first, then most due today, then most open, each with `▲late ●today open` and their role. On the right is the chosen person: name, role and note, then B's box (`█` per open task, red late, amber today, grey the rest, and `N late · N today · N open`), then their open tasks of every board in bands. Under each task sits C's quote: the note line that mentions them. The view is titled `PEOPLE · directory`, apart from view 9's team `People` (D4). `↑↓` move and `⇥`/`←→` switch panes. On the people pane `↵` goes to that person's tasks; on a task it opens it on its board (D-7). `/` finds a name, `n` adds a person, `e` edits one (`PersonForm`, D-6), and `esc` or `@` closes the view. The key row says what `↵` does on the current pane. The tasks pane keeps the cursor's task and its quote on screen and says how many tasks lie below. The agenda and this view share `board_lanes` and `open_on_board`. `@` and `A` bring an existing screen back to the top instead of stacking another. The README documents `@`, mentions and `people.json`.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/views.py` | source | LLR-2504.1 | `PersonItem`, `PERSON_BANDS`, `person_items`, `person_counts`, `people_by_urgency`, `_band_head`, `_person_when`, `_line`, `progress_box`, `_task_rows`, `_scroll_tasks`, `PEOPLE_TITLE`, `render_people_directory`; the import of `mention_line` |
| `taskboard/app.py` | source | LLR-2504.2, LLR-2504.3 | `board_lanes`, `open_on_board` (the agenda's code, moved), `people_keys`, `PeopleDirectory`, `_bring`, `action_people_directory`, `action_agenda_all` through `_bring`, `check_action`; `AllBoardsAgenda.compose`/`action_jump` reading the shared helpers |
| `taskboard/keymap.py` | source | LLR-2504.2 | `Key("at", "@", "people_directory", "People directory", bar=False)` |
| `taskboard/modals.py` | source | LLR-2504.3 | `PersonForm` |
| `README.md` | doc | HLR-2504 | the `@` key row; mentions in the notes; `people.json`, `people.json.corrupt` |
| `tests/test_people_view.py` | test | HLR-2504, LLR-2504.1, LLR-2504.2, LLR-2504.3 | new: TC-2504, AT-2504, D4 |
| `tests/test_modal_keys.py` | test | LLR-2504.3 | the law's inventory, forms and button lists gain `PersonForm` |
| `tests/test_keymap.py`, `tests/test_readme.py` | test | LLR-2504.2 | the README laws spell `@` (`at`) — law-driven |
| `.dev-flow/2026-10-21-batch-01/evidence/mutate-004.py` | doc | HLR-2504 | the increment's battery |

| Count | Value |
|---|---|
| **SOURCE files** | **4 / 4** — at the cap: the pure render (`views`), the screen and its key gating (`app`), the key seat (`keymap`), the person form (`modals`); one screen whose parts live in four layers by the module map's rules |
| Test files | 4 (uncapped) |

## 3 · How to test

`python -m pytest -q -p no:cacheprovider tests/test_people_view.py` (with `NO_COLOR` unset); the targeted set of `suite-004.txt`; `python .dev-flow/2026-10-21-batch-01/evidence/mutate-004.py`.

## 4 · Test results

| Layer | Nodes | Result |
|---|---|---|
| 0, A and B | `tests/test_people_view.py` — 32 nodes: TC-2504 (the bands, done/archived not owed, the urgency order, today outranking a longer list, the box, widths 116/78/40, the quotes under their tasks, the strings, the scroll — the cursor's pair always shown and the marker's count, never a quote without its task — the tones, the wide head), D4, AT-2504 (`@` from the home at both sizes and from the main screen, the pane-aware key row, the jump across boards, `enter` on the people pane, `n`/`e`/`/`, the errors, the seat keys, `@` over a modal and the presentation, `@ A @` never piling up); `tests/test_modal_keys.py` (`PersonForm`) | passed with the touched files' suites in `suite-004.txt` (the agenda, the home, help keys, legend, `test_app.py`, the markup census and sites, the English law, the README laws, the modal law, the other people suites) |
| full suite | owed at the P4 gate run | not-run |

| Field | Value |
|---|---|
| **RED counterfactual** | on increment 003's commit `6dcbeed` (this increment's tests copied in, its source not): `tests/test_people_view.py` a collection error (`ImportError` of `PeopleDirectory`); the law files: 3 failed (`PersonForm` absent from the package), 60 passed (`red-004.txt`); each assertion's own RED is the battery |
| **Mutation verdicts** | 19 arms, one run, each restore proven by digest: a done/archived task owed · KILLED; the urgency without today · KILLED; the quote dropped · KILLED; an orphan quote shown · KILLED; no marker · KILLED; `read-only` without `tasks` · KILLED; one `↵` word for both panes (UX-1) · KILLED; `enter` on the people pane opening a task (D-7) · KILLED; the seat keys acting behind the view · KILLED; `@` refused on the home · KILLED; `@` unbound · KILLED; the find silent · KILLED; a blank name saved · KILLED; the today block grey (UX-2) · KILLED; the jump leaving the home · KILLED; a failed write silent · KILLED; the window a row short of the cursor's quote (CR-1) · KILLED; the marker counting what is shown · KILLED; `@`/`A` piling up (CR-2) · KILLED — arms that stayed GREEN: none (`mutation-004.txt`; the first run printed SURVIVED for three arms — the fixture's tie, the 80-column head, a size where no orphan arose — each met by a new arm) |
| **Instrument RED-proof** | 1 instrument: `evidence/mutlib.py` (its RED seen in this increment: three SURVIVED arms before the new arms) |
| **Emitted-form assertion** | 1 artifact: `people.json` after `n` and `e` — read back as JSON, the record whole, the handle kept (AT-2504) |
| **Reverse census** | 5 probes: B1 `grep -rln "AllBoardsAgenda\|action_agenda_all\|check_action\|KEYMAP" tests/` → `test_all_agenda.py`, `test_boards_home.py`, `test_help_keys.py`, `test_legend.py`, `test_keymap.py`, `test_readme.py`, `test_app.py`, the other `KEYMAP` readers of the PLAN's census — the first seven rerun in `suite-004.txt`, green; the README laws spelled `@` (law-driven, the only foreign edits); A3 `board_lanes`/`open_on_board` — the agenda's behaviour unchanged (`tests/test_all_agenda.py` green, `A` now through `_bring`); B4 `people.json` written only through `Directory` — 2 law-driven foreign hits |
| **Evidence files** | the table under §4 *Evidence files*: each artifact's path and SHA-256 |
| **Correction population** | 2 law-driven edits enumerated before the first site: the README key-table spellings in `tests/test_keymap.py` (`"at": "@"`) and `tests/test_readme.py` (`"@": "at"`) — no assertion weakened |

### Evidence files

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| suite-004.txt | .dev-flow/2026-10-21-batch-01/evidence/suite-004.txt | 4f2fad45ba3f10d7eba22965f878a5a34301ccf90fa43529a4b713c969d5bd0e |
| red-004.txt | .dev-flow/2026-10-21-batch-01/evidence/red-004.txt | 741bdcb01d9871fa40cd02e3343151b4e7739f05a1cd468e749cbf0721e5353a |
| mutation-004.txt | .dev-flow/2026-10-21-batch-01/evidence/mutation-004.txt | 0503482538a8a790e32440bdb24905c2faf493ca18e999e976f7610d4c324667 |
| mutate-004.py | .dev-flow/2026-10-21-batch-01/evidence/mutate-004.py | 6181a82864b76072c8b255aaa327ed0ceb4d2a55ec0f68dae305944bd780b5c2 |
| inc004.diff | .dev-flow/2026-10-21-batch-01/evidence/inc004.diff | 288633fe4b4640947c2b15a7e2de6692e47a05fe44b461f0595b8202700957e9 |

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a generic agent with agents/code-reviewer.md · first pass **FIX FIRST** (BLOCK-UNTIL CR-1): CR-1 HIGH (the scroll moved its top up to dodge an orphan quote and cut the cursor's own quote under `↓ 0 more below`, reproduced at 78×20 and by a fuzz) → the window ends on the cursor's pair, an orphan blanked, the marker counting the tasks below, two new arms; CR-2 MEDIUM (`@ A @ A …` stacked screens without limit) → `_bring`, an AT; CR-3 LOW docstrings fixed; CR-4 LOW (`Text.assemble` around a Text) declined: the markup census trusts only a Text builder or a censused `-> Text` at a sink (reason accepted); **re-read: OK to advance** — CR-1 verified by the reviewer's `real.py` (the cursor's quote now shown at 78×20) and `scroll2.py` (0 failures over every-task-quoted shapes, from 50k cut quotes and 13k zero markers), CR-2 by `stack.py` (the stack never grows); LOW notes recorded: at a task pane of 1–2 rows the window can show only the blanked quote; a `↓ 0` marker is reachable only with an unquoted task, which real data cannot produce |

## 5 · Risks

The view reads every board once at open (as `A`); a person another window adds shows after a restart (A-7). D-7 departs from the round: `enter` on the people pane goes to the tasks (the key row says so).

## 6 · Pending items / spec deviations

The full suite is owed at P4. The real Windows Terminal captures of the composed frame are owed at the DDR (PDR PC-1). D-6 (`n`/`e`/`/` implemented) and D-7 are the orchestrator's decisions, to be named on the capture page for the operator.

## 7 · Suggested next task

Increment 005 — search by person (HLR-2505).

## Increment gate checklist

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | SOURCE budget | ✓ | §2: 4 source files, at the cap, the reason declared |
| 2 | Tests in this increment | ✓ | `tests/test_people_view.py` and the law files |
| 3 | Layer 0 where it applies | ✓ | the items, the order, the box, the scroll |
| 4 | RED counterfactual | ✓ | §4, `red-004.txt` and the battery |
| 5 | Reverse census | ✓ | §4: 5 probes, 2 law-driven foreign edits |
| 6 | `code-reviewer` passed | ✓ | §4b |
| 7 | No file from another lane | ✓ | one lane |
| 8 | Frozen interfaces untouched | ✓ | none frozen |
| 9 | Coverage verified on disk | ⚠ | `suite-004.txt` (targeted); the full run owed at P4 |
| 10 | Load-bearing emptiness | ✓ | the census's greps quoted |
| 11 | Mutation verdicts | ✓ | §4: 19/19 KILLED |
| 12 | Instrument RED-proof | ✓ | §4 |
| 13 | Correction population | ✓ | §4: 2 enumerated |
| 14 | Emitted-form assertion | ✓ | §4 |
| 15 | Independent review | ✓ | §4b |
| 16 | Evidence files | ✓ | §4: the digests |
