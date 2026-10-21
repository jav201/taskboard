# Increment 002 — LLR-2506.1, LLR-2506.2, LLR-2507.1 · `how a mention looks`

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
| Increment | `002` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | `HLR-2506`, `HLR-2502` (AT-2502), `HLR-2507` (render side) / `LLR-2506.1`, `LLR-2506.2`, `LLR-2507.1` |
| Acceptance | `AT-2506`, `AT-2502` · white-box `TC-2506`, `TC-2507` · unit: `notes_text`'s pieces, the card's tokens, the presentation's rows (Layer 0) |
| Agent | `software-dev` (the orchestrator; ported from the frozen draft) |
| Date | `2026-10-21` |

---

## 1 · What changed

How a mention looks (the round's item 4, variant A). `views.notes_text` builds the notes as Text pieces: each highlight segment, and inside it each mention of someone in the directory as `@Name`, bold pink. An unknown handle stays as typed, dimmed. `modals.notes_preview` returns it, and the editor's preview and the details pass the board's people. With no directory, or an empty one, everything draws as before. The kanban card gains `@First+N` in pink just before the due token, so it goes first when the row is tight. The presentation's notes write `@Name` with non-breaking spaces before wrapping and paint each whole mention bold pink in every row, the one-row cut included. The pattern is compiled once per directory.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/views.py` | source | LLR-2506.1, LLR-2506.2, LLR-2507.1 | `NBSP`, `mention_names`, `present_mentions`, `mention_marks`, `notes_text`; `_card_meta`'s token; `present_note_lines(…, people)`, `_marks_re`, `_paint_marks`, `_present_note_markup(…, marks)`, `_present_cut(…, marks)`, `_present_column(…, people)`, `_present_stack(…, marks)`, `render_present` passing `board.people`; `import functools` |
| `taskboard/modals.py` | source | LLR-2506.1 | `notes_preview(text, people=None)` → `views.notes_text`; `TaskModal` and `TaskDetails` pass the board's people; the views import |
| `tests/test_people_look.py` | test | HLR-2506, HLR-2502, HLR-2507, LLR-2506.1, LLR-2506.2, LLR-2507.1 | new: TC-2506, AT-2506 (both sizes, and Course's details), AT-2502, TC-2507 (foreign mentions, crafted notes) |
| `.dev-flow/2026-10-21-batch-01/evidence/mutate-002.py` | doc | HLR-2506 | the increment's battery |

| Count | Value |
|---|---|
| **SOURCE files** | **2 / 4** |
| Test files | 1 (uncapped) |

## 3 · How to test

`python -m pytest -q -p no:cacheprovider tests/test_people_look.py` (with `NO_COLOR` unset); the targeted set of `suite-002.txt`; `python .dev-flow/2026-10-21-batch-01/evidence/mutate-002.py`.

## 4 · Test results

| Layer | Nodes | Result |
|---|---|---|
| 0, A and B | `tests/test_people_look.py` — 19 nodes: `test_TC_2506_the_preview_draws_a_known_mention_as_its_name_in_pink`, `test_TC_2506_an_unknown_handle_stays_as_typed_and_dimmed`, `test_TC_2506_without_a_directory_the_preview_is_unchanged[none|empty]`, `test_TC_2506_a_name_that_looks_like_markup_is_printed_as_typed`, the card's two, the presentation's four (`…never_split_it`, `…paints_each_mention_pink_bold`, `…cut_to_one_row…`, `…split_view_shows_names`), `test_AT_2506_details_card_and_presentation_name_the_people[size0|size1]`, `test_AT_2506_another_board_draws_the_same_people`, `test_AT_2502_a_renamed_person_draws_the_new_name_and_the_note_keeps_the_handle`, `test_TC_2507_foreign_tasks_with_mentions_draw_in_the_team_view`, `test_TC_2507_a_crafted_note_draws_in_linear_time[×3]` | passed with the touched files' suites in `suite-002.txt` (the presentation, kanban, markup, details, editor, team sync and modal-key suites) |
| full suite | owed at the P4 gate run | not-run |

| Field | Value |
|---|---|
| **RED counterfactual** | on increment 001's commit `7c87311` (this increment's test file copied in, its source not): 19 failed, 0 passed (`red-002.txt`); each arm's own RED is the battery |
| **Mutation verdicts** | 14 arms, one run, each restore proven by digest: a known mention drawn as typed · KILLED; drawn outside its highlight · KILLED; an unknown handle not dimmed · KILLED; the card's token after the due · KILLED; the `+N` dropped · KILLED; NBSP a plain space · KILLED; the presentation's marks unpainted · KILLED; the split view given no people · KILLED; the details given no people · KILLED; the name read from the stored text (a rename lost) · KILLED; an empty directory dimming every `@word` (CR-1) · KILLED; a mark inside a longer word (CR-3) · KILLED; the one-row cut unpainted (CR-4) · KILLED; the card's token read as markup (CR-2) · KILLED — arms that stayed GREEN: none (`mutation-002.txt`; its first run printed SURVIVED for the CR-3 arm: the test used a two-word name, re-cut with `Ana` alone) |
| **Instrument RED-proof** | 1 instrument: `evidence/mutlib.py`, increment 001's (its RED seen there and here: one SURVIVED arm before the test was re-cut) |
| **Emitted-form assertion** | 1 artifact: the presentation's note rows (Rich markup) — parsed back with `Text.from_markup`, their plain text and spans asserted (TC-2506) |
| **Reverse census** | 4 probes: B1 `grep -rln "notes_preview\|_card_meta\|kanban_card\|present_note_lines\|_present_note_markup\|_present_cut\|TaskDetails" tests/` → `test_markup_census.py`, `test_markup_sites.py`, `test_kanban_readable.py`, `test_links.py`, `test_present_polish.py`, `test_present_views.py`, the details and editor suites — all rerun in `suite-002.txt`, green, no pin changed (their fixtures hold no mention and their boards no people); A3 `notes_preview`'s new parameter defaults to the old output; B4 none — 0 foreign hits |
| **Evidence files** | the table under §4 *Evidence files*: each artifact's path and SHA-256 |
| **Correction population** | none — no shipped assertion changed |

### Evidence files

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| suite-002.txt | .dev-flow/2026-10-21-batch-01/evidence/suite-002.txt | 5330ffcfbb7b33eea8aaae5147fbcc23a668bdb81f97785127728fc6d91ee9ab |
| red-002.txt | .dev-flow/2026-10-21-batch-01/evidence/red-002.txt | 666c08efb8d6c7412d5fe43cb1eddf5f68bd2e86df417d458bbf120abb01c637 |
| mutation-002.txt | .dev-flow/2026-10-21-batch-01/evidence/mutation-002.txt | 4b89731d0c12405d0f88ac14f54e82681fd22463158f947d9fc058af6e6a0a39 |
| mutate-002.py | .dev-flow/2026-10-21-batch-01/evidence/mutate-002.py | c57e8ca35be3b3d6b66b0e9e6a18fe6a6f9dda68692327e10b835d8238fae7dc |
| inc002.diff | .dev-flow/2026-10-21-batch-01/evidence/inc002.diff | 2f25a253b3c5b315ee903af40be967af2d4f9bd4b47e198fde111dd31193d45f |

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a generic agent with agents/code-reviewer.md · **OK to advance**, 0 HIGH; CR-1 (an empty directory dimmed every `@word` in the preview) and CR-2 (no test of a markup-looking name on the card or the presentation) MEDIUM, both fixed and pinned; CR-3 (a mark painted inside `@Anabel`), CR-4 (the one-row cut unpainted) fixed; CR-5 (the timing bound vs the contract) → the contract amended (LED .3); CR-6 (`Text.assemble` around `notes_text`) kept — `tests/test_markup_census.py` trusts only a censused module's `-> Text` or a Text builder at a sink, and `views` is not censused; CR-7 (a lone `\[` loses its backslash in the presentation, pre-existing) → `BACKLOG.md`. `security-reviewer` (render side of S-1) — spawned with agents/security-reviewer.md · **APPROVE**: the crafts through every render path in 0.016–0.094 s; no markup injection over hostile names at four widths; N-1 (a name ending `\\` drawn with one backslash, cosmetic) accepted → `BACKLOG.md`; N-2 (the alternation rebuilt per row) fixed (`_marks_re`, cached); the test gap (the full note, the colouring) closed |

## 5 · Risks

The presentation paints by the written `@Name` form (S-4, accepted): a teammate's literal `@Ana Ruiz` with non-breaking spaces is painted too. Mentions in the views the verdict did not name (focus snippet, swimlanes, report) keep the stored handle.

## 6 · Pending items / spec deviations

The full suite is owed at P4. CR-6 declined with its reason (§4b). CR-7 and N-1 logged.

## 7 · Suggested next task

Increment 003 — the `@` picker in the editor (HLR-2503).

## Increment gate checklist

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | SOURCE budget | ✓ | §2: 2 source files |
| 2 | Tests in this increment | ✓ | `tests/test_people_look.py` |
| 3 | Layer 0 where it applies | ✓ | the pieces, tokens, rows |
| 4 | RED counterfactual | ✓ | §4, `red-002.txt` |
| 5 | Reverse census | ✓ | §4: 4 probes, 0 foreign hits |
| 6 | `code-reviewer` passed | ✓ | §4b |
| 7 | No file from another lane | ✓ | one lane |
| 8 | Frozen interfaces untouched | ✓ | none frozen |
| 9 | Coverage verified on disk | ⚠ | `suite-002.txt` (targeted); the full run owed at P4 |
| 10 | Load-bearing emptiness | ✓ | the census's greps quoted |
| 11 | Mutation verdicts | ✓ | §4: 14/14 KILLED |
| 12 | Instrument RED-proof | ✓ | §4 |
| 13 | Correction population | ✓ | §4: none, declared |
| 14 | Emitted-form assertion | ✓ | §4 |
| 15 | Independent review | ✓ | §4b |
| 16 | Evidence files | ✓ | §4: the digests |
