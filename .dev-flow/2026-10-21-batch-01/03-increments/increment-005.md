# Increment 005 — LLR-2505.1, LLR-2505.2 · `search by person`

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
| Increment | `005` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | `HLR-2505` / `LLR-2505.1`, `LLR-2505.2` |
| Acceptance | `AT-2505` · white-box `TC-2505`, `TC-2407` (the modal law over `SearchPrompt`, read along a modal's bases) · unit: `matches`'s person rule, `filter_bar` (Layer 0) |
| Agent | `software-dev` (the orchestrator; ported from the frozen draft) |
| Date | `2026-10-21` |

---

## 1 · What changed

Search by person (the round's item 3, variant A). `/` in the kanban or the gantt opens `SearchPrompt`, a `TextPrompt` with the directory. Plain text filters the tasks as before, and the line under the field says `text filters tasks · @ starts a person`. Text that starts with `@` turns that line into `PEOPLE · names only`: the first 6 people found, with no `+ add`. `↑↓` choose, `↵ / alt+s` filter to that person's tasks (`@handle`), `alt+p` opens their page in the people view, `esc` cancels. An `@` query is always an exact handle (`views.matches`). It lights no text, and its bar reads `/ @Name  role · tasks that mention them`. Reopened on a person's filter, the list shows that person. The modal-key law now reads a modal's buttons and bindings along its bases inside the package, and lists `SearchPrompt`. The README names `/` then `@`. `BACKLOG.md` gains the batch's section.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/views.py` | source | LLR-2505.1 | `matches`'s `@handle` rule; `filter_bar(…, people)` and the person bar; `_apply_search_overlay(…, people)` lighting no text for a person; `render_view` passing `board.people` |
| `taskboard/modals.py` | source | LLR-2505.2 | `SEARCH_TEXT_KEYS`, `SEARCH_PERSON_KEYS`, `SearchPrompt` |
| `taskboard/app.py` | source | LLR-2505.2 | `action_search` pushes `SearchPrompt` with `people` and `open_person` (the people view) |
| `README.md` | doc | HLR-2505 | `/` then `@` in the notes section |
| `.dev-flow/BACKLOG.md` | doc | HLR-2501, HLR-2504, HLR-2505, HLR-2506 | the batch's section: done; the split view's raw markers (the commission); the logged findings |
| `tests/test_people_search.py` | test | HLR-2505, LLR-2505.1, LLR-2505.2 | new: TC-2505, AT-2505 (both sizes, `@` alone, `alt+p`, no one, the gantt, the reopen) |
| `tests/test_modal_keys.py` | test | LLR-2505.2 | `_own`: a modal's package bases; `_bound` and the button check read them; `SearchPrompt` in the inventory, forms and button lists |
| `.dev-flow/2026-10-21-batch-01/evidence/mutate-005.py` | doc | HLR-2505 | the increment's battery |

| Count | Value |
|---|---|
| **SOURCE files** | **3 / 4** |
| Test files | 2 (uncapped) |

## 3 · How to test

`python -m pytest -q -p no:cacheprovider tests/test_people_search.py tests/test_modal_keys.py` (with `NO_COLOR` unset); the targeted set of `suite-005.txt`; `python .dev-flow/2026-10-21-batch-01/evidence/mutate-005.py`.

## 4 · Test results

| Layer | Nodes | Result |
|---|---|---|
| 0, A and B | `tests/test_people_search.py` — 8 nodes: `test_TC_2505_a_person_query_matches_exactly_their_mentions`, `test_TC_2505_the_bar_names_the_person_and_their_role`, `test_AT_2505_at_lists_names_only_and_enter_filters_to_their_tasks[size0|size1]`, `test_AT_2505_at_alone_lists_everyone_and_arrows_choose`, `test_AT_2505_alt_p_opens_their_page`, `test_AT_2505_no_one_by_that_name_and_text_still_filters`, `test_AT_2505_the_gantt_filters_by_person_too`; `tests/test_modal_keys.py` (`SearchPrompt`, the law along the bases) | 641 passed with the touched files' suites in `suite-005.txt` (the filter's existing suites: `test_app.py`, the gantt, kanban, colour-budget, milestones, tick-label suites; the markup census; the README laws; the people view) |
| full suite | owed at the P4 gate run | not-run |

| Field | Value |
|---|---|
| **RED counterfactual** | on increment 004's commit `b473003` (this increment's tests copied in, its source not): 11 failed, 29 passed — every search node and the law's three `SearchPrompt` nodes (`red-005.txt`); each assertion's own RED is the battery |
| **Mutation verdicts** | 13 arms, one run, each restore proven by digest: the person rule falling through to text · KILLED; a partial handle matching · KILLED; the bar not naming the person · KILLED; the kanban's bar without people · KILLED; the gantt's bar without people (QA-4) · KILLED; the list capped at 8 (QA-1) · KILLED; `+ add` offered · KILLED; `enter` filtering by the typed text · KILLED; `alt+p` opening nothing · KILLED; the law reading only a modal's own source · KILLED; `SearchPrompt` without its base's keys · KILLED; `/` reopened listing no one (CR-1) · KILLED; the bar's lookup case-sensitive (CR-3) · KILLED — arms that stayed GREEN: none (`mutation-005.txt`; an earlier run printed SURVIVED for the `check_action` gate on `move`/`page`: unobservable, the gate removed — LED .6) |
| **Instrument RED-proof** | 1 instrument: `evidence/mutlib.py` (its RED seen here: two BAD anchors after the review's fixes and one SURVIVED arm) |
| **Emitted-form assertion** | none — this increment emits no artifact (the filter lives in the session) |
| **Reverse census** | 4 probes: B1 `git grep -l "filter_bar\|matches(\|filtered_board\|action_search\|\"slash\"" eac7d42 -- tests` → `test_app.py`, `test_colour_budget_app.py`, `test_gantt_board.py`, `test_gantt_polish.py`, `test_kanban_readable.py`, `test_milestones.py`, `test_tick_label.py` — all rerun in `suite-005.txt`, green (their queries carry no `@`); `TextPrompt` users of `"Filter tasks"` → the app only; A3 `filter_bar`'s new parameter defaults to the old bar; the law change (`_own`) can only make the inventory stricter — 0 foreign hits |
| **Evidence files** | the table under §4 *Evidence files*: each artifact's path and SHA-256 |
| **Correction population** | 1 law edit enumerated before its site: `tests/test_modal_keys.py`'s `_bound` and button check read a modal's package bases (`_own`) — stricter, no assertion weakened |

### Evidence files

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| suite-005.txt | .dev-flow/2026-10-21-batch-01/evidence/suite-005.txt | 1bb1395e5be5b1634e4749943760aeadf348257757088753b84ffb6280356981 |
| red-005.txt | .dev-flow/2026-10-21-batch-01/evidence/red-005.txt | 824db93758d886ffd86b538bb716d652603ed2631e6fda31d44d5b0ff766cafe |
| mutation-005.txt | .dev-flow/2026-10-21-batch-01/evidence/mutation-005.txt | 61988d1ed23b306f8c91fce7ba46594233459576d376a70a30ba66d715002bf3 |
| mutate-005.py | .dev-flow/2026-10-21-batch-01/evidence/mutate-005.py | 896f6be628e86ac43d271122cc807658b9ad10570f63e87ecd543a11658076b9 |
| inc005.diff | .dev-flow/2026-10-21-batch-01/evidence/inc005.diff | a2fbf3341df219ad67abd468c257f25307b77d284a9c4220a6d5ac7f01beb139 |

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a generic agent with agents/code-reviewer.md · **OK to advance**, 0 HIGH; CR-1 MEDIUM (`/` reopened on a person's filter said `no one by that name`) fixed with an AT step; CR-2 MEDIUM (the contract's «text filter as before» against the code's exact handle) → the contract amended to the code's behaviour (LED .6); CR-3 LOW (the bar's lookup case) fixed and pinned |

## 5 · Risks

`/` stays in the kanban and the gantt only (the round's note). A teammate's handle meaning someone else here filters to this operator's person (D4, accepted).

## 6 · Pending items / spec deviations

The full suite is owed at P4. `UX-11` (the filter window's button `Save`) logged.

## 7 · Suggested next task

The DDR (`stations/p4-validation.md` §DDR) with the real Windows Terminal captures (PDR PC-1), then P4.

## Increment gate checklist

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | SOURCE budget | ✓ | §2: 3 source files |
| 2 | Tests in this increment | ✓ | `tests/test_people_search.py`, the law |
| 3 | Layer 0 where it applies | ✓ | `matches`, `filter_bar` |
| 4 | RED counterfactual | ✓ | §4, `red-005.txt` |
| 5 | Reverse census | ✓ | §4: 4 probes, 0 foreign hits |
| 6 | `code-reviewer` passed | ✓ | §4b |
| 7 | No file from another lane | ✓ | one lane |
| 8 | Frozen interfaces untouched | ✓ | none frozen |
| 9 | Coverage verified on disk | ⚠ | `suite-005.txt` (targeted); the full run owed at P4 |
| 10 | Load-bearing emptiness | ✓ | the census's greps quoted |
| 11 | Mutation verdicts | ✓ | §4: 13/13 KILLED |
| 12 | Instrument RED-proof | ✓ | §4 |
| 13 | Correction population | ✓ | §4: 1 enumerated |
| 14 | Emitted-form assertion | ✓ | §4: none, declared |
| 15 | Independent review | ✓ | §4b |
| 16 | Evidence files | ✓ | §4: the digests |
