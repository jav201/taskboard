# Design proposal — taskboard — Batch 2026-10-21-batch-01

> **Artifact language.** Canonical **English scaffold**; generate in the batch's language
> The normative rules below are language-independent. **Where that language is declared:**
> `state.json`'s `language` key in `core` and `full`.

> **Reserved field names.** The **field names and block keywords below are language-independent** — the
> validator parses them literally and they are never translated:
> `Design proposal` · `7 · Forward-applicability table` · `⏸ DEFER`
> Everything else on this page — headings, guidance, the prose in every cell — is translated with the batch.
> **One strategy, not two:** the flow ships no alias table, so a translated label is read as an ABSENT one and the rule keyed on it reports a true-sounding silence.
> **Why a HEADING is reserved here and a FIELD NAME everywhere else:** `C-49`'s artifact is the §7 TABLE, and a rule that read a summary bullet instead of the rows would be reading a claim about the table rather than the table. `V52` therefore keys on this document's own H1 and on the §7 heading, which is why both are on the machine plane. **And one FLOW-WIDE reserved token, read out of this artifact by `V42` no matter which template minted it:** `⏸ DEFER`.

> **Owed in.** `core` by trigger · `full` ✓
> **Source:** `/dev-flow-init` step 4's seed-by-level table, which is this fact's one home. A level marked `—` **does not owe this artifact, and its absence is not an omission**; `by trigger` means the station exists only when the `triggers` block fired, and `stations_active` in `state.json` is the authority for *this* batch. Where a SECTION or a gate row is owed more narrowly than the artifact, it says so on the row.

> **Where this lives: the VAULT + Drive**, not the repo — it is deliberation, and its traceability to
> code is weak. It is **cited by id** from the repo (`PDR-<batch_id>#D<n>`), never copied.
> What binds code — a frozen interface, a design characteristic — also lands in the **repo**, in the
> requirement or in `docs/ARCHITECTURE.md`. *The vault keeps the deliberation; the repo keeps the commitment.*

> **The forward-applicability rule (ISO/IEC/IEEE 15288).** Everything below must be NAMED as the input
> of a later activity. **If a section of this proposal is nobody's input, delete it — it does not belong
> in the PDR.** That rule is what allows this document to cost half the batch without being waste.

| Field | Value |
|---|---|
| Id | `PDR-2026-10-21-batch-01` |
| Requirements covered | `HLR-2501 v1 · HLR-2502 v1 · HLR-2503 v1 · HLR-2504 v1 · HLR-2505 v1 · HLR-2506 v1 · HLR-2507 v1 · LLR-2501.1 · LLR-2501.2 · LLR-2501.3 · LLR-2502.1 · LLR-2503.1 · LLR-2503.2 · LLR-2504.1 · LLR-2504.2 · LLR-2504.3 · LLR-2505.1 · LLR-2505.2 · LLR-2506.1 · LLR-2506.2 · LLR-2507.1` |
| Modules touched (from `docs/ARCHITECTURE.md`) | `models` (`people.py` new, `models.py`) · `app` (`app.py`) · `views` · `modals` · `keymap` |
| Triggers that fired | `A1 · A2 · A3 · B1 · B4 · C3 · C6 · C8 · D1 · E1` |
| Author / reviewers | `architect` · `qa-reviewer` · `ux-reviewer` (D1) · `security-reviewer` (C3, C6, C8; the new file store) |

---

## 1 · Objective and scope

The round's chosen variants, ported from `prototypes/people_round/proto.py` into the shipped classes, in five increments on one branch (`feat/people`, one lane). The code was drafted in this worktree before the review (the 2026-10-20-batch-02/03 pattern, D-13 there) and is ported increment by increment after the PDR.

- **001 — the directory (HLR-2501, HLR-2502, HLR-2507).** `taskboard/people.py` (new: `Person`, `Directory` — `load`, `find`, `named`, `add`, `edit`, `_commit` on `boards.file_lock` + `models.write_atomic` —, the tokeniser `MENTION_RE`/`mention_ids`/`split_mentions`/`mention_line`, `fold`, `handle_for`); `Board.people` (`models.py`); the app loads it beside the registry and hands it to every board (`app.py`). 3 source files; tests `tests/test_people_directory.py` (new), `tests/people_round_fixture.py` (the round's fixture, copied).
- **002 — the look (HLR-2506; item 4 A).** `views.notes_text`, `mention_names`, `present_mentions`, `mention_marks`, `_card_meta`'s token, the presentation's note rows; `modals.notes_preview` returns `notes_text`, `TaskModal`/`TaskDetails` pass the board's people. 2 source files (`views.py`, `modals.py`); tests `tests/test_people_look.py` (new).
- **003 — the picker (HLR-2503; item 2 A).** `modals.MENTION_AT`, `pick_rows`, `MentionDrop`, `TaskModal`'s picker (the round's `EditorInline`), `TaskModal(…, people=)`; the app passes its directory. 2 source files (`modals.py`, `app.py`); tests `tests/test_people_picker.py` (new).
- **004 — the people view (HLR-2504; item 1 A + C + B, D4).** `views.PersonItem`, `person_items`, `person_counts`, `people_by_urgency`, `progress_box`, `render_people_directory`, `PEOPLE_TITLE`; `app.board_lanes`, `open_on_board` (the agenda's code, shared), `PeopleDirectory`, `action_people_directory`, `check_action`; `keymap` `@`; `modals.PersonForm`. 4 source files (`views.py`, `app.py`, `keymap.py`, `modals.py`); tests `tests/test_people_view.py` (new), the modal law's row (`tests/test_modal_keys.py`), the README laws' `@` spelling (`tests/test_keymap.py`, `tests/test_readme.py`); `README.md`.
- **005 — search by person (HLR-2505; item 3 A).** `views.matches`'s person rule, `filter_bar`'s person bar, `_apply_search_overlay`; `modals.SearchPrompt` (the round's `SearchAt`); `app.action_search`. 3 source files (`views.py`, `modals.py`, `app.py`); tests `tests/test_people_search.py` (new), the modal law read along the bases (`tests/test_modal_keys.py`); `docs/ARCHITECTURE.md`'s last pass, `.dev-flow/BACKLOG.md`.

Out: deleting a person; mentions in the other views; the team roster merge (D4); the split view's raw `!!`/`++` (logged).

## 2 · Modules and boundaries

| Module | What it owns here | What it exposes | What it must NOT reach into |
|---|---|---|---|
| `models` (`people.py`, new file in the layer) | the directory file, the tokeniser, the handle | `Person`, `Directory`, `PEOPLE_NAME`, `MENTION_RE`, `mention_ids`, `split_mentions`, `mention_line`, `fold`, `handle_for` | any widget, markup, key; any team folder |
| `models` (`models.py`) | `Board.people` (memory only) | the attribute | the directory's file |
| `views` | pure renders: the notes' pieces, the card token, the presentation's names, the people view, the person filter | `notes_text`, `mention_names`, `present_mentions`, `mention_marks`, `PersonItem`, `person_items`, `person_counts`, `people_by_urgency`, `progress_box`, `render_people_directory`, `PEOPLE_TITLE`; `filter_bar(…, people)` | reading keys; writing the directory |
| `modals` | the picker inside `TaskModal`, `PersonForm`, `SearchPrompt` | `pick_rows`, `MentionDrop`, `PersonForm`, `SearchPrompt`; `TaskModal(…, people=)` | `app` (the people view is opened through a callback `open_person`) |
| `keymap` | `@` in the seat | `KEYMAP` | — |
| `app` | the directory's load and its hand-off, `PeopleDirectory`, the lanes shared with the agenda | `PeopleDirectory`, `board_lanes`, `open_on_board`, `TaskboardApp.people` | rendering (views) |

New import edges inside the layering: `views` → `models` (`people.py`), `modals` → `models` (`people.py`), `app` → `models` (`people.py`) — all allowed by §3; `people.py` → `boards.py`, `models.py` (inside the layer; it reuses `boards._keep_aside`, a private name of the same layer). `modals` never imports `app`: `SearchPrompt` gets `open_person`.

## 3 · Diagrams

```
people.json (~/.taskboard)  ◄── Directory._commit: file_lock ─► re-read ─► change ─► write_atomic
      │ load (never raises; unreadable → .corrupt + notice)
      ▼
app.people (Directory) ── .people (one live dict handle → Person) ──► board.people (every board opened)
      │                                                                  │
      │ TaskModal(people=)  @ at a word start → MentionDrop (list | add)  │ views.notes_text / _card_meta /
      │   ↵ → "@handle " in the notes; + add → Directory.add             │ present_mentions → "@Name" pink
      │ SearchPrompt(people=, open_person=)  "/@an" → names only          │ matches("@handle") / filter_bar
      │ PeopleDirectory: board_lanes ─► person_items × people ─► render_people_directory
      ▼                    ┌─ left: people by urgency (▲late ●today open) ─┬─ right: name, role, note
team push (unchanged): notes as typed (@handle), never board.people        │  ╭ box: ███ 1 late · 1 today · 5 open ╮
                                                                           │  LATE / TODAY / … bands: task row
                                                                           │     “the note line that mentions them”
```

## 4 · Interfaces that change — and which ones FREEZE

| Interface | Current | After | Consumers | **Frozen for the fork?** |
|---|---|---|---|---|
| `people.*` (new module) | — | LLR-2501.1, LLR-2501.2, LLR-2502.1 | `app`, `views`, `modals`, tests | no — one lane |
| `Board.people` | — | `{}` default, the live directory dict when the app opens a board | `views`, `modals`, the app | no |
| `modals.notes_preview(text)` | one parameter | `(text, people=None)`, returns `views.notes_text` | `TaskModal`, `TaskDetails`, the markup suites | no |
| `views.present_note_lines(notes, w)`, `_present_note_markup(row, w)`, `_present_cut(rows, k, w)` | — | `+ people` / `+ marks`, defaults keep the old output | `render_present`, `tests/test_present_views.py`, `tests/test_present_polish.py` | no |
| `views._card_meta` | its tokens | + `@First+n` before the due | `kanban_card`, the kanban suites | no |
| `views.matches`, `filter_bar(query, hits, total, w)` | text only | `@handle` → `person`; `+ people` | `filtered_board`, `render_view` | no |
| `TaskModal(board, task=None)` | two parameters | `+ people=None` | `app` (`a`, `e`), the editor suites | no |
| `modals.PersonForm`, `SearchPrompt`, `pick_rows`, `MentionDrop` (new) | — | LLR-2504.3, LLR-2505.2, LLR-2503.1 | `app`, tests | no |
| `KEYMAP` | 57 keys | + `@` (`people_directory`, `bar=False`) | `app_bindings`, `?`'s map, the palette, the README laws | no |
| `AllBoardsAgenda.compose` | builds its lanes | reads `board_lanes(app)`; its jump `open_on_board` | the agenda suite | no |

## 5 · Proposed test cases

| Id | Layer (0 unit / A white / B black / UX) | What it asserts | **The mutation that would turn it RED** |
|---|---|---|---|
| TC-2501 | 0/A | the load's table (missing, mixed, four unreadable forms); `add`/`edit`; two windows; the lock; a failed write; an unkeepable file | the re-read under the lock dropped; the lock dropped; memory updated before the write; a repeated handle kept; the cap dropped |
| AT-2501 | B | `open_app`: 8 people from the home's file, the same dict on every board, no board file holds them; the unreadable notice; no file without a registry | `_label_board` not setting `people`; `Board._to_dict` writing it |
| TC-2502 | 0 | the tokeniser's and the handle's tables; `find`'s order | the look-behind dropped; a trailing `.` allowed; `find`'s role rule before the name rule |
| TC-2503 / AT-2503 | 0 / B | `pick_rows`; `@an ↵`, arrows, `esc`, `+ add` with `tab`, a refused add, no picker in a word or on a handle, no directory | `check_action` allowing `enter` while closed; `tab` losing `focus_next`; `esc` cancelling the editor with the list open; `+ add` for `@` alone |
| TC-2504 / AT-2504 | 0/A / B | items, bands, urgency, the box, widths, the quote under each task; `@`, `tab`, `down`, `enter` lands on Client A's task; `n`/`e`/`/`; the seat keys dead; `@` over a modal | a done task owed; `today` dropped from the urgency key; the quote dropped; `check_action` letting the seat act |
| TC-2505 / AT-2505 | 0 / B | the person rule; the bar; `@an ↵`, `@ ↓ ↵`, `alt+p`, `@zz`, text unchanged | the person rule falling through to text; `alt+p` acting on text; `_save` dismissing the typed `@an` |
| TC-2506 / AT-2506 | 0 / B | the preview's pieces and tones; the card token's place; NBSP names; the split view; details/kanban/presentation in the app | the mention drawn outside its segment; the token after the due; NBSP → space |
| TC-2507 / AT-2507 | A / B | the push holds handles and nothing of the directory; malformed foreign mentions draw | `board.people` added to the pushed record |
| TC-2407 (extended) | A | `PersonForm` and `SearchPrompt` in the modal law, buttons read along the bases | `alt+s` unbound on `PersonForm`; the law reading only the class's own source |

**5b · The gauntlet controls that apply, and who pays:** C-40 (each new assertion RED on `base_ref` — a clean worktree at `eac7d42` — or by a recorded mutation; the orchestrator, `mutate-00N.py` beside its transcript); C-19 (one complete run per gate; the whole suite in three sequential chunks at P4); C-42 (the ATs read the screen's text, the notices and the files); B1's reverse census in each packet; the law-driven test updates (`test_modal_keys.py`, `test_keymap.py`, `test_readme.py`) named in their packets.

## 6 · Risks and rejected alternatives

| Alternative considered | Why it was rejected |
|---|---|
| a directory per board (inside each `board.json`) | D1: one person across boards; the people view reads every board |
| the link form `@[Name](p:id)` or text + list (S1, S2) | the verdict chose the handle (S3); the link form is still read |
| a task field `people: [...]` | two sources of truth; the board format would change (D3's S2 consequences) |
| the picker as a centred window (item 2 B) | the operator chose A |
| `alt+s` to confirm the new person's role | it is the task's Save in the editor (D5's finding) |
| `enter` on the people pane opening the first task (the round's) | an unseen task opens; `enter` goes to the tasks pane instead, one more `enter` opens |
| the progress box beside the name | the right pane at 80 columns has 51 cells; stacked it fits at both sizes |
| the box's words `X late X open X today` in the objection's order | B's rendered order `late · today · open` is what the operator saw and named; the order is read most-urgent first |
| renaming view 9 instead (D4's second option) | the page's first proposal — the new view titled `PEOPLE · directory` — is concrete and leaves the team's view and its tests alone |
| a mutable module-level directory (the round's `DIR`) | hundreds of apps per suite; the attribute `Board.people`, like `Board.label`, is per app |
| `SearchPrompt` importing the people view | `modals` → `app` is forbidden (§3); a callback `open_person` |

Risks: `tab`'s binding in `TaskModal` replaces the screen's — the picker calls `focus_next` itself when closed (the editor's tab-walk test holds it); `peek_board` of every board at open (as `A`); a teammate's handle meaning someone else here (D4, accepted); the directory written by two windows at once (the lock; TC-2501).

## 7 · Forward-applicability table — **the section that makes this document honest**

| Output of this PDR | Named consumer downstream | Where the consumer will read it |
|---|---|---|
| design characteristics | the Phase-3 increments | §1 (the five increments and their files), §4 |
| enablers (fixtures, data, scaffolding, env) | Phase 3 and validation | `tests/people_round_fixture.py` (the round's boards and people); the seam home; `evidence/captures/` harness |
| proposed test cases | layers 0/A/B and the DDR | §5 → `01-requirements.md`'s thresholds and the increments' batteries |
| design → requirement traceability | the matrix and the DDR | the Requirements covered row; each increment's packet §2 |

- ⚠ Any row whose consumer column is empty: **remove the output, or explain why it is being produced.**

## 8 · Parallelisation plan *(only if the batch forks)*

Not applicable — one lane.
