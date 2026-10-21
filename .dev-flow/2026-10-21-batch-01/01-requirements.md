# Requirements Document — taskboard — Batch 2026-10-21-batch-01

> **Artifact language**
> This template is the canonical **English scaffold**. Generate the artifact in the batch's development language (`state.json` `language`). For Spanish batches, translate the **prose** — section headers and guidance — **and never a label**, and use `deberá` as the normative keyword (≡ `shall`). The normative RULES in this preamble are **language-independent** and enforced regardless of artifact language.

> **Owed in.** `core` ✓ · `full` ✓

> **Field guide:** `templates/guides/req-template.md` and its part 2, `templates/guides/req-template.part2.md`, explain each field below and the rules that read it. It ships with the flow and is not copied into this batch.

> **Reserved field names.** The **field names and block keywords below are language-independent** — the
> validator parses them literally and they are never translated:
> `Validation` · `Acceptance test(s)` · `Boundary catalog` · `Negative control` · `Premise evaluation` · `Fork preconditions` · `Ledger` · `Requirement` · `⏸ DEFER`
> Everything else on this page — headings, guidance, the prose in every cell — is translated with the batch.
> **One strategy, not two:** the flow ships no alias table, so a translated label is read as an ABSENT one and the rule keyed on it reports a true-sounding silence.
> **And one FLOW-WIDE reserved token, read out of this artifact by `V42` no matter which template minted it:** `⏸ DEFER`. It is a MARKER rather than a field name, which is why it is stated here *and* in `/dev-flow` §Language of artifacts rather than in a per-template list — a deferral can be written in any batch artifact, including the ones that carry no block at all.

---

## 1. Introduction

### 1.1 Purpose
The live contract for batch 2026-10-21-batch-01: the four items of the people round (`prototypes/people_round/people-round.html`) as the operator's verdict chose them — a directory of people for every board, `@` mentions in the notes, a view per person, search by person, and how a mention looks — with the round's five decisions (D1–D5) and its recommended storage form.

### 1.2 Scope
In: `models` — `taskboard/people.py` (NEW: the directory, the mention tokeniser), `taskboard/models.py` (`Board.people`, set by the app, never saved); `app` — `taskboard/app.py` (the directory loaded at start and handed to every board, the people view `PeopleDirectory` and `@`, the editor and the filter given the directory); `views` — `taskboard/views.py` (mentions drawn in the kanban card and the presentation, the people view's pure render, the person filter and its bar); `modals` — `taskboard/modals.py` (the notes preview, the `@` picker in `TaskModal`, `PersonForm`, `SearchPrompt`); `keymap` — `taskboard/keymap.py` (`@` in `KEYMAP`); the tests and `tests/people_round_fixture.py` (the round's synthetic boards and people, copied so no test imports a prototype); `README.md`, `docs/ARCHITECTURE.md`, `.dev-flow/BACKLOG.md` (docs). Out: removing a person from the directory; mentions in the views the verdict did not name (the focus snippet, the swimlanes, the HTML report keep the stored handle text); merging the team roster with the directory (D4: a later round); the presentation's split view drawing `!!…!!` and `++…++` raw (pre-existing, logged in `BACKLOG.md`); pushing or merging.

### 1.3 Definitions, acronyms, abbreviations
| Term | Definition |
|------|------------|
| the round | `prototypes/people_round/` (commit `eac7d42`) and its verdict |
| the directory | `people.json` beside the boards registry — `~/.taskboard/people.json` for the app `taskboard` opens — holding every person: handle, name, role, note |
| handle | a person's stable id and the stored form of a mention: lowercase letters and digits in words joined by `.`, `_` or `-` (`ana.ruiz`), derived from the name when the person is added, never changed |
| mention | `@handle` at a word start in a task's notes (the link form `@[Name](p:handle)` is read too) |
| the picker | the dropdown under the notes' cursor that an `@` opens in the task editor (item 2 A) |
| the people view | the screen behind `@` (item 1: A's two panes, C's note line, B's progress box) |

### 1.4 References
- The operator's commission (2026-10-21), relayed by the orchestrator, and the round's verdict, verbatim: «D1: de acuerdo · D2: de acuerdo · D3: de acuerdo · D4: de acuerdo · D5: de acuerdo · formato (storage): handle · 1 view: A · OBJECIÓN: «Estoy de acuerdo con A y robar de C el contexto, pero también robar de B el recuadro de progreso que dice X late X open X today.» · 2 picker: A · 3 search: A · 4 look: A · notes: (none)».
- The round's code, the spec of each chosen variant: `prototypes/people_round/proto.py` (`PeoplePanes`, `PersonPage.body`'s context line, `PeopleCards.body`'s bar, `EditorInline`, `MentionDrop`, `SearchAt`, `matches_m`, `filter_bar_m`, `notes_preview_m`, `card_meta_m`, `present_note_lines_m`, `present_note_markup_m`); its captures (`people-round.html`, `pv-A`, `pv-B`, `pv-C`, `mt-A*`, `sr-A*`, `m-A-*`).
- The round's decisions as the page states them (`build_html.py` `DECISIONS`): D1 one directory for every board; D2 a person is name + role (+ an optional note); D3 `@` at a word start opens the picker, the note keeps a stable reference; D4 the team roster stays apart and the new view is titled `PEOPLE · directory` on screen; D5 every window button has a shown key, the inline add confirms its role with `↵`, not `alt+s`.
- The shipped code: `taskboard/boards.py` (`file_lock`, `keep_aside`, `Registry._commit`), `taskboard/models.py` (`write_atomic`, `clean_strings`, `strip_controls`, `Board.__init__`), `taskboard/modals.py` (`notes_preview`, `TaskModal`, `TextPrompt`, `TaskDetails`), `taskboard/views.py` (`highlight_segments`, `_card_meta`, `present_note_lines`, `_present_note_markup`, `_present_cut`, `matches`, `filter_bar`, `_apply_search_overlay`, `render_people`), `taskboard/app.py` (`AllBoardsAgenda`, `action_search`, `_label_board`, `after_move`, `check_action`), `taskboard/keymap.py`, `taskboard/team_sync.py` (`TeamState.push`).

### 1.5 Document overview
§2 the stories, premises and fork preconditions; §3 seven HLRs; §4 the LLRs and the information-flow contract; §5 the validation strategy; §6 the decisions and open risks.

---

## 2. Overall description

### 2.1 Product perspective
taskboard has no notion of a person outside team mode: «what do I owe Ana?» is answered by reading task after task, and `/ana` also finds «Canary release plan». This batch adds a directory shared by every board, mentions written in the notes, a view per person and a person filter, porting the round's chosen variants; each was the real `TaskboardApp` with a subclass or a new screen, so the port moves that code into the shipped classes.

### 2.2 Product functions
1. One directory of people (handle, name, role, note) for every board, in the home, written safely beside a second window.
2. `@` in a task's notes opens a picker under the cursor; `↵` writes `@handle`; `+ add` creates a person in place.
3. `@` on the main screen opens the people view: who needs the operator most, the chosen person's open tasks of every board with what was written about them, a `late · today · open` box; `enter` opens a task on its board; `n`/`e`/`/` add, edit, find a person.
4. `/` then `@` lists names only and filters to the tasks that mention one person; `alt+p` opens their page.
5. A mention is drawn `@Name` in pink in the details, on the kanban card and in the presentation.

### 2.3 User characteristics
The operator alone (`username_subject`), keyboard only, at a meeting or presenting to a room; several boards; Windows Terminal at 118×30 and 80×24.

### 2.4 Constraints
Standard library and the shipped dependencies only; Windows-safe; the directory written with the registry's lock-and-atomic-write pattern (batch 2026-10-20-batch-02); no board file gains a field (a task's people are read from its notes); every name, role and note drawn as a Text piece, never markup (S1); every new modal button has a direct shown key (`tests/test_modal_keys.py`'s law); team sync never carries the directory; synthetic data only; the operator's name nowhere; tests never touch the real home.

### 2.5 Assumptions and dependencies
Textual 8.2.8 names the `@` key `at` (P-1); a priority binding refused by `check_action` lets the key through to the focused widget (the round's `EditorInline` relies on it); one home folder per operator. The calendar is frozen in the tests as the round's (Tuesday 2026-10-20).

### 2.6 Source user stories

| ID | User Story | Source | DoR status |
|----|------------|--------|------------|
| US-2501 | As the operator, I want one directory of the people I work with — name, role, a note — shared by every board and safe from a second window, so that a person is written once and mentioned anywhere. | D1, D2, D3 (storage: handle) | READY |
| US-2502 | As the operator writing a task's notes, I want `@` to open a picker under my cursor that I narrow by typing and that can add a new person in place, so that a mention is one more word, not a dialog. | item 2 (A); D5 | READY |
| US-2503 | As the operator in a meeting, I want one screen with who needs me most and, for the chosen person, their open tasks of every board by urgency, what I wrote about them, and a late/today/open box, so that I answer «what do I owe them?» and jump to a task. | item 1 (A, with C's context and B's box: the objection); D4 | READY |
| US-2504 | As the operator, I want `/` to find a person's tasks exactly — `@` starting a person, names only — and to open their page, so that the filter has no false positives. | item 3 (A) | READY |
| US-2505 | As the operator and the room, I want a mention drawn as the person's current name in one tone in the details, on the kanban card and in the presentation, so that I read names, not handles. | item 4 (A) | READY |

**The chains, one line each (architect A-4):** US-2501 → HLR-2501, HLR-2502, HLR-2507 → AT-2501, AT-2502, AT-2507 · US-2502 → HLR-2503 → AT-2503 · US-2503 → HLR-2504 → AT-2504 · US-2504 → HLR-2505 → AT-2505 · US-2505 → HLR-2506 → AT-2506. A story's number and its HLR's differ: the HLRs are numbered by mechanism, and US-2501 owns three.

#### Refinement log (one block per story)

**US-2501 — the directory**
- **INVEST:** I ✓ · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality (V, N):** user = the operator · outcome = `~/.taskboard/people.json` read at start, written under its lock; the handle form · why = D1–D3 · out of scope = deleting a person; merging the team roster (D4)
- **Feasibility (E, S):** a new `taskboard/people.py` in the `models` layer reusing `boards.file_lock`, `keep_aside` and `models.write_atomic` · fits one batch? = yes, increment 001
- **Evaluability (T) — behavioral, black-box:** `open_app` on the round's boards: the app holds 8 people from `~/.taskboard/people.json`, every board it opens draws from them, no board file holds them; an unreadable file is said and kept aside (AT-2501); a push to the team folder carries `@ana.ruiz` and no name, role or note (AT-2507).
- **Open questions:** none. · **Classification:** `READY`.

**US-2502 — the picker**
- **INVEST:** I ✓ · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality (V, N):** user = the operator · outcome = `EditorInline` + `MentionDrop` of the round in `TaskModal` · why = item 2 A · out of scope = the centred window (B)
- **Feasibility (E, S):** `modals.TaskModal`, `app` passes the directory · fits one batch? = yes, increment 003
- **Evaluability (T) — behavioral, black-box:** `e` on «Steering committee», `↵`, `Ask @an`, `↵`, `about the stores`, `alt+s`: the saved notes end `Ask @ana.ruiz about the stores` and the preview read `@Ana Ruiz` (AT-2503).
- **Open questions:** none. · **Classification:** `READY`.

**US-2503 — the people view**
- **INVEST:** I ✓ · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality (V, N):** user = the operator · outcome = `@` opens `PEOPLE · directory`: A's panes + C's quote under each task + B's box · why = item 1 and its objection; D4 · out of scope = deleting a person; editing a task from the view
- **Feasibility (E, S):** `views.render_people_directory` (pure), `app.PeopleDirectory`, `keymap` `@`, `modals.PersonForm` · fits one batch? = yes, increment 004, 4 source files
- **Evaluability (T) — behavioral, black-box:** on Personal, `@`: Ana first with `1 late · 1 today · 5 open` and `“Waiting on @Ana Ruiz…”`; `tab`, `down`, `enter` opens «Golden question set» on Client A (AT-2504).
- **Open questions:** none. · **Classification:** `READY`.

**US-2504 — search by person**
- **INVEST:** I ✓ · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality (V, N):** user = the operator · outcome = `SearchAt` of the round as `SearchPrompt`; `@handle` filter; the bar names the person · why = item 3 A · out of scope = `/` in views other than kanban and gantt (the round's note)
- **Feasibility (E, S):** `views.matches`/`filter_bar`, `modals.SearchPrompt`, `app.action_search` · fits one batch? = yes, increment 005
- **Evaluability (T) — behavioral, black-box:** kanban, `/`, `@an`, `↵`: the bar reads `/ @Ana Ruiz  Client A PM · tasks that mention them`, «Canary release plan» is gone (AT-2505).
- **Open questions:** none. · **Classification:** `READY`.

**US-2505 — how a mention looks**
- **INVEST:** I ✓ · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality (V, N):** user = the operator and the room · outcome = `@Name` bold pink in the details/preview, `@Ana+1` on the card before the due, `@Ana Ruiz` in the presentation's notes · why = item 4 A · out of scope = other views
- **Feasibility (E, S):** `views.notes_text`, `_card_meta`, `present_note_lines`, `_present_note_markup`; `modals.notes_preview` · fits one batch? = yes, increment 002
- **Evaluability (T) — behavioral, black-box:** «Golden question set»: `enter` shows `@Ana Ruiz` and `@Andrés Lima`; `4` shows `@Ana+1` at 118; `R`, `2` shows `@Ana Ruiz` (AT-2506).
- **Open questions:** none. · **Classification:** `READY`.

### 2.7 Premise evaluation (C-43) — MANDATORY, one row per premise

| # | Premise, as a truth-apt proposition | Tier (axiom · hypothesis · premise) | Verdict | Executed evidence (command output / `file:line` — **NOT** a citation of another document) | Disposition |
|---|---|---|---|---|---|
| P-1 | Textual names the `@` key `at`, and `at` is bound nowhere in the app | premise | TRUE | `evidence/premises.py` on `base_ref`: `` P-1 Textual names the `@` key 'at' \| `at` in KEYMAP: False \| a Binding on "at" anywhere in app/modals: False `` (`evidence/premises.txt`) | `@` opens the people view (HLR-2504) |
| P-2 | No people directory exists: nothing names `people.json`, no `taskboard/people.py` | premise | TRUE | `` P-2 `people.json` named in taskboard/: False \| a module taskboard/people.py: False `` | the directory is new (HLR-2501) |
| P-3 | `@` in the editor's notes is plain text: no widget reacts to it | premise | TRUE | `P-3 notes end with 'Ask @an' \| screen TaskModal \| a widget whose id names a mention: False \| widgets 55` | the picker (HLR-2503) |
| P-4 | The text filter `ana` matches «Canary release plan» (a false positive), while `@ana.ruiz` text matches by substring only | premise | TRUE | `P-4 / ana on Client A matches ['Canary release plan', 'Chunking experiments', 'Eval report v1', 'Golden question set', 'Steering committee'] \| `@ana.ruiz` filter matches […4 titles…]` | the exact person filter (HLR-2505) |
| P-5 | View 9 is the team's `People` (its key label `People`, its head row `PEOPLE`) | premise | TRUE | `P-5 view 9's key label: ['People'] \| its render: 'The V2 people-lanes view: one lane per roster member.' \| its head row writes 'PEOPLE': True` | D4: the new view is titled apart (HLR-2504) |
| P-6 | Team sync pushes only the board's task dicts (`_to_dict`) and names no directory | premise | TRUE | `P-6 team push writes the board's own dict (`_to_dict`): True \| names people.json: False` | the directory never travels (HLR-2507) |
| P-7 | `@` on the main screen does nothing today | premise | TRUE | `` P-7 `@` on the main screen changes the screen stack: False `` | the people view (HLR-2504) |
| P-8 | The registry's lock and atomic write exist to reuse | premise | TRUE | `P-8 boards.file_lock: True \| models.write_atomic: True` | the directory's writes (HLR-2501) |

- **Premise evaluation:** 8 premise(s) · ✅ TRUE ×8

### 2.8 Fork preconditions (C-52) — MANDATORY, and the declared empty when the batch does not fork

- **Fork preconditions:** none — this batch runs one lane: five increments in order on one branch (`feat/people`), one owner (the orchestrator) holds the trunk.

---

## 3. High-level requirements (HLR)

### HLR-2501 — One people directory for every board
- **Traceability:** US-2501
- **Ledger:** LED-2026-10-21-batch-01.1, LED-2026-10-21-batch-01.2, LED-2026-10-21-batch-01.3
- **Statement:** The system shall keep one directory of people in `people.json` beside the boards registry (`~/.taskboard/people.json` for the app `taskboard` opens; beside the board only for an app built without a registry — a test seam: `taskboard` always passes the home's registry, architect A-8), each person a handle, a name (1–60 characters), a role (≤ 60) and a note (≤ 200), every field one line without control characters; it shall read the file at start without ever raising — a missing, empty or blank file an empty directory, nothing written and nothing said; an unreadable one (a failed read, not JSON, not an object holding a `people` list) an empty directory after a byte copy at `people.json.corrupt` (`boards.keep_aside`, never replacing an earlier copy) and one warning notice `people.json could not be read; a copy was kept at <path>. The people directory starts empty.` — `…; no copy could be kept. …` when the copy failed; an entry with a malformed or repeated handle or no name skipped; it shall write the file only when a person is added or edited, atomically, under `people.json.lock`, as a read-modify-write of what the file holds then (another window's people kept), never over an unparseable file it could not copy aside; a failed write shall change nothing in memory and raise to its caller, which says so; every board the app opens shall draw mentions from this one directory, and no board file shall hold it; a window reads the file at start and after its own writes only, so a person another window adds shows here after a restart or this window's next add or edit (accepted, architect A-7).
- **Rationale (informative):** D1 (one directory for every board), D2 (name + role + note), the commission's «One directory for all boards at `~/.taskboard/people.json`, written with batch-02's lock/atomic-write pattern».
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_people_directory.py`
- **Numeric pass threshold:** AT-2501: the round's boards (`tests/people_round_fixture.py`) under the seam home, `open_app(None)` at 118×30: `app.people.path` is `<home>/.taskboard/people.json` with 8 people; `app.board.people` is `app.people.people` before and after `switch_board("course")`; a person added then shows on the open board at once; after a save no board file holds `people` or the added name; with `people.json` = `{oops` the notice above is shown and `people.json.corrupt` holds `{oops`; an app built with `TaskboardApp(board_path=…)` alone never writes a `people.json`; with `keep_aside` failing the notice says `no copy could be kept`; an empty or blank `people.json` gives no notice and no copy; the round's boards opened on Course: «Guest talk: RAG in retail»'s details draw `Guest talk by @Ana Ruiz` and `@Juana Soto` (qa QA-9); names of 61 and notes of 201 characters are cut to 60 and 200, 60 and 200 kept whole (QA-7).
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** the same people on every board; a broken file never stops the app and is kept.
  - **Shipped surface:** `taskboard` → the start, `~/.taskboard/people.json`.
  - **Acceptance test(s):** AT-2501
  - **Boundary catalog (QC-3):** ☑ boundary (name 60, role 60, note 200 characters; a taken handle `ana.ruiz2`) ☑ empty (no file: an empty directory, nothing written) ☑ invalid (bad entries skipped; control bytes stripped; an unreadable file kept aside) ☑ error (the lock held: `busy`, nothing changed; a failed write: nothing changed in memory)
  - **Negative control:** on `base_ref` AT-2501 is RED: `TaskboardApp` has no `people` (P-2; `evidence/red-001.txt` — planned).

### HLR-2502 — A mention is `@handle`, and a handle never changes
- **Traceability:** US-2501
- **Ledger:** LED-2026-10-21-batch-01.1, LED-2026-10-21-batch-01.2, LED-2026-10-21-batch-01.3
- **Statement:** The system shall read a mention as `@` at a word start (not after a letter, digit, `.` or `@`, so `ana@x.com` is no mention) followed by a handle — lowercase letters and digits in words joined by `.`, `_` or `-`, never ending in one of them — and shall also read the link form `@[Name](p:handle)`; a task's people shall be read from its notes and nowhere else; a new person's handle shall be the name's letters and digits, accents folded, its words joined by `.` (`Andrés Lima` → `andres.lima`; `person` when nothing is left), with `2`, `3`, … appended while it is taken in the file or in memory; editing a person shall never change their handle.
- **Rationale (informative):** D3 and the storage verdict `handle` (S3): short, typeable, legible without the directory, stable across renames; the link form is read because the round's tokeniser reads it.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_people_directory.py -k TC_2502`
- **Numeric pass threshold:** TC-2502 (unit, Layer 0): the tokeniser's table (`Ask @ana.ruiz about the stores.` → `ana.ruiz`; `mail ana@x.com or @@ana` → none; `@Sofia` → none; `(@elena.vidal)` → `elena.vidal`; a mention inside `==…==`; the link form; repeated handles once); the handle table (`O'Brien-Smith Jo` → `o.brien.smith.jo`, `李` → `person`, `R2 D2` → `r2.d2`), each handle read back as a mention; a taken handle → `ana.ruiz3`; `find("an")` → Ana, Andrés, Juana, Marta.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** the note holds a word anyone can read (`@ana.ruiz`); a rename changes what is drawn, not what is stored.
  - **Shipped surface:** the notes' text (`board.json`), the directory's `id`, the details.
  - **Acceptance test(s):** AT-2502 (Ana renamed `Ana Ruiz Prieto`: «Golden question set»'s details draw `@Ana Ruiz Prieto`, its notes still begin `Review the 40 questions with @ana.ruiz`), AT-2503
  - **Boundary catalog (QC-3):** ☑ boundary (a trailing `.`: not part of the handle) ☑ empty (no mention) ☑ invalid (`ana@x.com`, `@@ana`, `@Sofia`, an unclosed link) ☐ error — none
  - **Negative control:** TC-2502 goes RED when the look-behind is dropped (an e-mail becomes a mention) or the handle may end in `.` (increment 001's battery — planned).

### HLR-2503 — `@` in the notes opens a picker under the cursor
- **Traceability:** US-2502
- **Ledger:** LED-2026-10-21-batch-01.1, LED-2026-10-21-batch-01.2, LED-2026-10-21-batch-01.4
- **Statement:** While the task editor is open with the directory and the notes' cursor follows an `@` at a word start and the text typed after it (no space, no `@`; not already a handle the directory holds), the system shall show a dropdown under the cursor, inside the screen: a head `@<typed>▌   mention a person`, at most 5 people `find` returns for the typed text (name starts, then inside the name, then the role) as `name  role` rows with the first highlighted, then `+ add '<typed>'  new person` when the typed text is not already someone's name (none for `@` alone), `type a name` when there is nothing, and the key line `↑↓   ↵ pick   esc plain text`; `↑`/`↓` shall move the highlight; `enter` shall replace `@<typed>` with `@<handle> ` and close it; `enter` on `+ add` shall turn it into the new person's form — head `New person  · for every board`, the name field prefilled with the typed text, the role field focused, key line `↵ add + mention   ⇥ name / role   esc back` — where `tab` moves between the two fields, `enter` adds the person to the directory (HLR-2501) and writes the mention, and `esc` goes back to the list; `esc` on the list shall close it leaving the typed text as typed; the focus leaving the picker — the notes for the list, the form for the new person, by `tab`, `shift+tab` or a click — shall close it, leaving the typed text as typed, and typing in the notes with the form open closes the form (architect A-5, code review CR-1 of increment 003); the mention shall replace only `@<typed>` where it still stands; a mention of someone the directory holds followed by sentence punctuation (`@ana.ruiz.`) opens nothing (CR-2); with no one listed `enter` is the notes' new line (CR-4); a failed add shall say `The person was not added: <reason>` and keep the form; while the dropdown is closed `enter`, the arrows, `tab` and `esc` shall do what they did before (a new line, the cursor, the next field, cancel); the new person's role shall be confirmed with `enter`, never `alt+s`, which keeps saving the task; the picker shall write the directory only through an add and the task only through the editor's save.
- **Rationale (informative):** item 2 A (`EditorInline` + `MentionDrop`); D5's finding (`alt+s` is the task's Save).
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_people_picker.py`
- **Numeric pass threshold:** AT-2503: on the round's boards, `e` on «Steering committee» (`tc8`), the notes' end, typing `↵ Ask @an`: the dropdown shows Ana Ruiz before Andrés Lima before `+ add 'an'` and lies inside the screen at 118×30 and 80×24; at 80×24, the notes reached by `tab` from the title and the cursor six lines down, the list opens above the cursor, wholly inside the screen (ux UX-3, qa QA-2); `@an`, `tab` → closed, the notes end `Ask @an`, `enter` writes no mention; closed, `up` moves the notes' cursor (QA-11); `enter`, `about the stores`, `alt+s` → the saved notes end `Ask @ana.ruiz about the stores` and the preview read `Ask @Ana Ruiz about the stores`; `@an`, `down`, `down`, `up`, `enter` → `@andres.lima `; `@ma`, `esc` → closed, `@ma` kept, the editor open; `enter` then adds a new line and `esc` cancels the editor; `Call @Sofia`, `enter` → the form with `Sofia` and the role focused; `tab`, ` Vega`, `tab`, `Legal counsel`, `enter` → `people.json` holds `{"id": "sofia.vega", "name": "Sofia Vega", "role": "Legal counsel", "note": ""}`, the notes `Call @sofia.vega `, the editor still open; the lock held → `The person was not added: … busy …`; `mail ana@x`, `@ana.ruiz`, `word@an` open nothing; an editor built without the directory treats `@` as text.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** a mention is typed without leaving the note; a new person is added once, for every board.
  - **Shipped surface:** `taskboard` → `e` / `a`, the notes.
  - **Acceptance test(s):** AT-2503
  - **Boundary catalog (QC-3):** ☑ boundary (5 rows then `+ add`; an exact name: no `+ add`; the dropdown at the screen's edge) ☑ empty (`@` alone: no add row; an empty directory: `type a name`) ☑ invalid (a name that looks like markup printed as typed; inside a word: no picker) ☑ error (the lock held: the add refused, said, the form kept)
  - **Negative control:** on `base_ref` AT-2503 is RED: no dropdown (P-3; `evidence/red-003.txt` — planned).

### HLR-2504 — `@` opens the people view
- **Traceability:** US-2503
- **Ledger:** LED-2026-10-21-batch-01.1, LED-2026-10-21-batch-01.2
- **Statement:** When the operator presses `@` on the main screen or on the home, the system shall show, read-only for tasks, the people view: a head row (`◆ PEOPLE · directory  who do I owe what · every board`, at the right `<n> in the directory · tasks read-only`, or `<n> people · tasks read-only` when that does not fit — and then, still too wide, the subtitle `who do I owe what` alone — `person` singular); then two panes split by `│`: on the left every person of the directory ordered by most late, then most due today, then most open, then name — two rows each, the name with `▲<late>` (red) `●<today>` (amber) and the open count, the role dimmed under it, the chosen person marked `▶` and shaded (its `▶` dimmed while the tasks pane holds the cursor, ux UX-6); on the right the chosen person's name (pink) and role, their note (or `no note`), a progress box — `╭─╮`/`│ <a block per open task: red late, amber today, grey the rest> <late> late · <today> today · <open> open │`/`╰─╯`, the words for zero late or today left out, `nothing open` when there is none — then their open tasks (neither done nor archived) of every active board and of an unlisted open board, whose notes mention them, in bands `LATE`, `TODAY`, `THIS WEEK · to Sun <d>`, `LATER`, `NO DATE`, each task a row (the cursor `▶`, the board's chip, the title, the project from a 78-cell pane, the due `▲Nd`/`today`/`Wed 21`/`—`) with, under it, the first note line that mentions the person between `“` and `”`, mentions drawn as in HLR-2506, cut with `…`; and a key row in the key bar's style `↑↓ move   ⇥ panes   ↵ their tasks   / find   n add   e edit person   esc back` while the people pane holds the cursor and `… ↵ open task …` while the tasks pane does (ux UX-1, UX-4: whole at 80 columns; words dropped from the right first when narrower); every board shall be read once when it opens; `↑`/`↓` (`k`/`j`) move in the focused pane; `tab`, `←`/`→` (`h`/`l`) switch panes (to the tasks only when there are some); `enter` on the people pane goes to that person's tasks, on a task closes the view (and the home beneath it), opens the task's board in place when it is another (a switch, with a switch's writes) and selects the task; the tasks pane scrolls by whole tasks to keep the cursor's task and its quote on screen, never opening on a quote without its task, its last row `↓ <n> more below` when tasks lie under it (ux UX-5); `/` asks `Find a name` and moves to the first person `find` returns (`No one in the directory matches '<q>'.` otherwise); `n` opens `PersonForm` empty and `e` with the chosen person — title `Edit person @<handle>`, fields `Name`, `Role`, `Note` each labelled, `Save`/`Cancel` with `↵ / alt+s save   ⇥ next field   esc cancel` (ux UX-8) — and a save adds or edits the person (HLR-2501), the list re-ordered with the cursor on them, a refused name saying `A person needs a name.`, a failed write `The directory was not saved: <reason>`; `escape` or `@` close the view; with an empty directory it shall say `No one in the directory yet.` and `n adds a person · an @ in a task's notes mentions one`; `@` shall not act over a modal or the presentation, and no other key of the main screen shall act while the view is open; `@` shall be listed by `?`'s map and the palette as `People directory` (`KEYMAP`, off the bar), apart from view `9`'s `People`.
- **Rationale (informative):** item 1 A (`PeoplePanes`) with the operator's objection — «robar de C el contexto» (`PersonPage`'s quote under each task) and «de B el recuadro de progreso que dice X late X open X today» (`PeopleCards`' bar and words, drawn boxed, in B's order late · today · open); D4's proposal on the page — the new view titled `PEOPLE · directory` on screen — applied. `enter` on the people pane goes to the tasks rather than opening an unseen first task (the round opened the first one).
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_people_view.py`
- **Numeric pass threshold:** AT-2504: the round's boards opened on Personal, `@` ON THE HOME at 118×30 and 80×24 → `PeopleDirectory` over `BoardsHome` (qa QA-3); the screen holds `◆ PEOPLE · directory`, `▶ Ana Ruiz`, `1 late · 1 today · 5 open`, `“Waiting on @Ana Ruiz`, the last row is `↑↓ move   ⇥ panes   ↵ their tasks   / find   n add   e edit person   esc back`; `tab` → it holds `↵ open task` and `esc back`; `down`, `enter` → one screen (the home closed too), Client A open, `tc5` («Golden question set») selected; `@` from the main screen opens it too (architect A-11); with Client A's file removed, `enter` on its task → the missing-file notice, Personal still open; with the lock held, `n`, `Zoe`, `alt+s` → `The directory was not saved: …`, `people.json` byte-identical (qa QA-5); `/`, `zz` → `No one in the directory matches 'zz'.`; `n`, `alt+s` → `A person needs a name.`, the form kept; `e` → `Edit person @sofia.vega`, the rename typed (QA-6, QA-9); `down`, `down` → Marta Gil, `enter` → the tasks pane showing «Invoice October»; `esc` and `@` each close it; `n`, `Sofia Vega`, `tab`, `Legal`, `alt+s` → the cursor on `sofia.vega`; `e`, name `Sofia Vega Ruiz`, `enter` → renamed, handle kept, the file holds it; `/`, `marta`, `enter` → Marta; with the view open `a`, `d`, `1`, `B`, `4` change nothing — the view mode, the board, its task count and the selection unchanged (QA-8); `@` over a `ConfirmModal` and over the presentation does nothing; TC-2504's tones: the box's blocks `over`/`soon`/`later`, `1 late` bold `over`, `1 today` bold `soon`, the counts' `▲1`/`●1` likewise and the chosen name pink (ux UX-2); the people pane at 78×22 ends `↓ 2 more below`; the tasks pane on the fifth task opens on no quote.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** from one screen the operator sees who needs them, what they owe one person across every board and what they wrote about it, and lands on a task with one key.
  - **Shipped surface:** `taskboard` → `@`.
  - **Acceptance test(s):** AT-2504
  - **Boundary catalog (QC-3):** ☑ boundary (80 columns: the project column gone, quotes cut with `…`; more tasks than rows: the pane scrolls) ☑ empty (an empty directory; a person with nothing open: `nothing open`, `enter` stays) ☑ invalid (names, roles, notes and titles that look like markup printed as typed; a missing or unreadable board: no tasks from it) ☑ error (`enter` on a task whose board file vanished: the switch's missing-file notice; a failed directory write: said, nothing changed)
  - **Negative control:** on `base_ref` AT-2504 is RED: `@` does nothing (P-7; `evidence/red-004.txt` — planned).

### HLR-2505 — `/` then `@` filters to one person's tasks
- **Traceability:** US-2504
- **Ledger:** LED-2026-10-21-batch-01.1, LED-2026-10-21-batch-01.2
- **Statement:** When the operator presses `/` in the kanban or the gantt, the system shall show the filter window (`Filter tasks`) with, under its field, `text filters tasks · @ starts a person` and the key line `↵ / alt+s filter   esc cancel`; when the field starts with `@` it shall instead list under it `PEOPLE · names only` and the first 6 of the directory's people `find` returns for what follows the `@` (for `@` alone, the first 6 by name; no `+ add` row; `no one by that name` when none, qa QA-1), the first highlighted, with the key line `↑↓   ↵ / alt+s filter   alt+p their page   esc cancel` (ux UX-7); `↑`/`↓` move the highlight; `enter` or `alt+s` with a person highlighted shall set the filter `@<handle>`, which keeps exactly the tasks whose notes mention that handle, lights no text, and whose bar reads `/ @<Name>  <role> · tasks that mention them` (the role and its ` · ` left out when empty) with the tally; with no person listed, `enter` filters by the typed text as before; `alt+p` with a person highlighted shall close the window and open the people view on them (HLR-2504); a text query shall filter exactly as before.
- **Rationale (informative):** item 3 A (`SearchAt`, `matches_m`, `filter_bar_m`): the same `@` as the notes, exact, no mode to remember; `/` stays in the kanban and the gantt (the round's note).
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_people_search.py`
- **Numeric pass threshold:** AT-2505: Client A, `4`, `/`, `@an` at 118×30 and 80×24 → `PEOPLE · names only`, `▶ Ana Ruiz`, no `+ add`, `esc cancel` and `alt+p their page` on screen; `enter` → `search_query` `@ana.ruiz`, `/ @Ana Ruiz` on screen, «Steering», «Golden», «Chunking» shown, «Canary» and «Invoice» not; `/`, `@` → Ana Ruiz … Luis Mora shown, Marta Gil and Pablo Ortiz not (the first 6 by name); `down`, `enter` → `@andres.lima`; the gantt (`3`), `/`, `@an`, `enter` → `/ @Ana Ruiz  Client A PM · tasks that mention them`, no «Canary» (qa QA-4); `/`, `@mar`, `alt+p` → the people view on Marta Gil, no filter set; `/`, `@zz` → `no one by that name`, `alt+p` nothing, `enter` → the text filter `@zz`; `/`, `ana` → `text filters tasks · @ starts a person`, `↵ / alt+s filter`, `enter` → «Canary» shown (text unchanged).
- **Priority:** medium
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** a person's tasks, exactly, from the filter the operator already knows.
  - **Shipped surface:** `taskboard` → `/` in kanban and gantt.
  - **Acceptance test(s):** AT-2505
  - **Boundary catalog (QC-3):** ☑ boundary (6 rows; `@` alone lists everyone) ☑ empty (`@zz`: no one; an empty directory: no one) ☑ invalid (a partial handle `@ana` typed and `enter` with no one listed: a text filter, nothing invented) ☐ error — none
  - **Negative control:** on `base_ref` AT-2505 is RED: `@an` lists nothing and the filter `ana` keeps «Canary» (P-4; `evidence/red-005.txt` — planned).

### HLR-2506 — A mention is drawn `@Name` in pink
- **Traceability:** US-2505
- **Ledger:** LED-2026-10-21-batch-01.1, LED-2026-10-21-batch-01.2, LED-2026-10-21-batch-01.3
- **Statement:** Where a task's notes are shown in the details (`enter`) or the editor's preview, the system shall draw each mention of a person the directory holds as `@<current name>` bold in the `pink` tone, inside any highlight of its line, and a mention of a handle the directory does not hold as typed, dimmed; on the kanban card it shall add, just before the due token (so it goes first when the row is tight), `@<first name of the first person mentioned>` with `+<n>` for the others, in `pink`; in the presentation's notes (the split view and the gantt view's cursor note) it shall write each such mention `@<Name>`, its spaces non-breaking so a wrap never splits it, bold pink; with no directory, or an empty one (`Board.people` is `{}` until someone is added), every place shall draw the notes exactly as before (code review CR-1 of increment 002); a mark is painted only where a whole mention was written — typed text that merely starts like a name (`@Anabel` for `Ana`) stays as typed (CR-3) — in every row of the presentation's note, the one-row cut included (CR-4).
- **Rationale (informative):** item 4 A (`notes_preview_m`, `card_meta_m`, `present_note_lines_m`, `present_note_markup_m` with style A): one tone, no width change, visible in the three places; the room reads names.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_people_look.py`
- **Numeric pass threshold:** AT-2506: the round's boards, «Golden question set» (`tc5`) at 118×30 and 80×24: `enter` → `@Ana Ruiz` and `@Andrés Lima`, no `@ana.ruiz`; `escape`, `4` → `@Ana+1` at 118 (at 80 the card keeps `today` and drops the mention, as the round's capture); `R`, `2` → `@Ana Ruiz`, no `@ana.ruiz`.
- **Priority:** medium
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** names, not handles, in the three places the operator and the room read.
  - **Shipped surface:** `taskboard` → `enter`, `4`, `R`.
  - **Acceptance test(s):** AT-2506
  - **Boundary catalog (QC-3):** ☑ boundary (a tight card: the mention goes before the due) ☑ empty (no directory: unchanged) ☑ invalid (an unknown handle dimmed; a name that looks like markup printed as typed) ☐ error — none
  - **Negative control:** on `base_ref` AT-2506 is RED: the details show `@ana.ruiz` (`evidence/red-002.txt` — planned).

### HLR-2507 — Team sync carries a mention as its handle and nothing of the directory
- **Traceability:** US-2501
- **Ledger:** LED-2026-10-21-batch-01.1, LED-2026-10-21-batch-01.2, LED-2026-10-21-batch-01.3
- **Statement:** The system shall never write the directory or any of its names, roles or notes to the team folder: a push shall carry a task's notes as typed (a mention as `@handle`), as before; a teammate's pulled task whose notes hold mentions — known, unknown or malformed — shall draw in every view without error, a known handle drawn as this operator's directory names it; a note of 100 000 characters crafted against the tokeniser (`@[` repeated) shall be read in linear time (security S-1: the link form's name is bounded to 60 characters).
- **Rationale (informative):** D4's consequence «the teammate without my directory sees `@ana.ruiz`»; the commission's «Team sync must not leak or break on mentions»; the directory holds what the operator wrote about real people.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_people_directory.py tests/test_people_look.py -k 2507`
- **Numeric pass threshold:** AT-2507: Client A pushed with the directory loaded → the team folder holds only `board.u1.json`, which holds `@ana.ruiz` and `@elena.vidal` and none of `Ana Ruiz`, `Client A PM`, `Prefers a written agenda`, `Elena Vidal`, `Steering committee chair`, `people`; TC-2507: five pulled tasks with the notes `with @ana.ruiz`, `@[x](p:`, `@@@ @`, `@[Ana](p:ana.ruiz)`, `@` + 500 letters draw in view 9, their card tokens and previews (`@Ana` for the first and fourth only); TC-2507: `"@[" * 50000`, `"@[" + "x" * 99000` and `"a@" * 50000` and 40 000 distinct handles each go through `mention_ids`, `split_mentions`, `mention_line`, `notes_text`, `_card_meta`, the full note's `present_note_lines` and its rows' colouring in under 2 s of CPU time (unbounded: ~25 s; quadratic dedupe: ~6 s) — CPU time, not wall-clock, so a loaded host never fails it (code review CR-2 of increment 001).
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** what the operator wrote about a person stays on their machine; a teammate's mentions never break a view.
  - **Shipped surface:** the team folder; view 9.
  - **Acceptance test(s):** AT-2507
  - **Boundary catalog (QC-3):** ☐ boundary — none ☐ empty — none ☑ invalid (malformed mentions from a teammate) ☐ error — none
  - **Negative control:** AT-2507 goes RED when a push writes `board.people` (a mutation adding it to the record — increment 001's battery, planned).

---

## 4. Low-level requirements (LLR)

> Each LLR decomposes an HLR into a verifiable property at the implementation level.
> Same regime: EARS syntax owed in `full`, recommended in `core`. ID format: `LLR-<HLR>.<M>`.

### LLR-2501.1 — `people.Directory.load`
- **Traceability:** HLR-2501
- **Ledger:** LED-2026-10-21-batch-01.1, LED-2026-10-21-batch-01.2
- **Statement:** `taskboard/people.py` (NEW — created in increment 001) shall provide `Person(id, name, role="", note="")`, `PEOPLE_NAME = "people.json"` and `Directory(path, people=None, load_report=None)` holding `people: dict[str, Person]` (one live dict, cleared and refilled in place); `Directory.load(path)` shall never raise: missing → empty; a failed read or an unparseable file → empty with `load_report = {"unreadable": True, "backup": <boards.keep_aside's copy or None>}` (`keep_aside`, the registry's copy made public, architect A-3); an empty or blank file → empty, no report; each entry cleaned with `models.clean_strings`, its fields made one line and capped (`NAME_MAX` 60, `ROLE_MAX` 60, `NOTE_MAX` 200), skipped unless its `id` fully matches the handle pattern, is not repeated and has a name; `find(q)` and `named(name)` as HLR-2503 uses them.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_people_directory.py -k TC_2501`
- **Numeric pass threshold:** TC-2501: a missing file → empty, no file; the mixed file → `ana.ruiz` and `esc` only, the note one line, the role 60 `r`s; each of `{not json`, `[]`, `{"people": {}}`, `\xff\xfe` → empty, `unreadable`, the backup's bytes equal the file's, the file unchanged.
- **Negative control:** TC-2501 goes RED when a repeated handle is kept, the cap is dropped, or the unreadable file is not copied (increment 001's battery — planned).
- **Boundary catalog:** ☑ boundary (the caps) ☑ empty (no file) ☑ invalid (bad entries, bad bytes) ☐ error — none

### LLR-2501.2 — `Directory.add` and `Directory.edit`
- **Traceability:** HLR-2501
- **Ledger:** LED-2026-10-21-batch-01.1, LED-2026-10-21-batch-01.2, LED-2026-10-21-batch-01.3
- **Statement:** `Directory.add(name, role="", note="")` and `Directory.edit(handle, name, role, note)` shall clean their fields as `load` does, raise `ValueError` for a name with nothing left, and write through `_commit(change)`: under `boards.file_lock(path)`, read the file as it is now (a failed read raises; an unparseable file is kept aside first — never written over when it cannot be — else the memory's people are the base), apply `change`, `models.write_atomic` `{"version": 1, "people": [...]}` with `ensure_ascii=False`, then refill `people` in place; `add` derives the handle with `handle_for(name, taken)` against the file's handles and the memory's; a raised `OSError` leaves memory unchanged.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_people_directory.py -k TC_2501`
- **Numeric pass threshold:** TC-2501: `add("  Ana   Ruiz ", "Client A PM")` → `ana.ruiz`, then `ana.ruiz2`, `andres.lima`, the live dict the same object, the file `version` 1 with the three ids, no `.tmp` or `.lock` left; two directories on one file → both people kept; `edit` keeps `luis.mora`, writes back a person the file lost and refuses a string that is not a handle (code review CR-5); an unparseable file: kept at `.corrupt` then replaced; with `keep_aside` failing: `OSError`, the file unchanged; the lock held with `LOCK_WAIT` 0.2 → `OSError` naming `busy`, no file; `write_atomic` failing → memory unchanged.
- **Negative control:** TC-2501 goes RED when the write skips the re-read (the second window erases the first's person), when the lock is dropped, when memory is updated before the write (increment 001's battery — planned).
- **Boundary catalog:** ☐ boundary — none ☑ empty (a blank name refused) ☐ invalid — none ☑ error (the lock, the write, the unkeepable file)

### LLR-2501.3 — the app holds the directory; `Board.people`
- **Traceability:** HLR-2501
- **Ledger:** LED-2026-10-21-batch-01.1, LED-2026-10-21-batch-01.2
- **Statement:** `taskboard/models.py` shall give `Board` an attribute `people` (`{}` by default) that the app sets and the file never holds; `taskboard/app.py` shall load `self.people = Directory.load(self.registry.path.parent / PEOPLE_NAME)` in `TaskboardApp.__init__`, set `self.board.people = self.people.people` in `_label_board` (so at mount and at every switch), carry it in `after_move`, and warn once at mount with HLR-2501's notice (`markup=False`) when the load reported it unreadable.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_people_directory.py -k AT_2501`
- **Numeric pass threshold:** as AT-2501.
- **Negative control:** AT-2501 goes RED when `_label_board` does not set `people` (a switched board draws handles) or when `Board._to_dict`/`save` writes it (increment 001's battery — planned).
- **Boundary catalog:** ☐ boundary — none ☑ empty (an app without a registry) ☑ invalid (an unreadable file) ☐ error — none

### LLR-2502.1 — `people.MENTION_RE`, `mention_ids`, `split_mentions`, `mention_line`, `handle_for`, `fold`
- **Traceability:** HLR-2502
- **Ledger:** LED-2026-10-21-batch-01.1, LED-2026-10-21-batch-01.2, LED-2026-10-21-batch-01.3
- **Statement:** `taskboard/people.py` shall provide `MENTION_RE` (`(?<![\w.@])@(?:\[([^\]\n]{1,60})\]\(p:(<handle>)\)|(<handle>))` with `<handle>` = `[a-z0-9]+(?:[._-][a-z0-9]+)*`), `mention_ids(text)` (the handles in order, each once; no scan of a text without `@`), `split_mentions(text)` (`(piece, handle | None)` pairs whose pieces join back to the text), `mention_line(notes, handle)` (the first line mentioning it, its `-`/`*`/`•` mark dropped), `fold(s)` (lower case, accents dropped) and `handle_for(name, taken)` as HLR-2502 states.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_people_directory.py -k TC_2502`
- **Numeric pass threshold:** TC-2502 as HLR-2502's threshold, and `split_mentions` joining back to the text.
- **Negative control:** as HLR-2502.
- **Boundary catalog:** ☑ boundary (a trailing `.`) ☑ empty (`""`) ☑ invalid (e-mails, `@@`, capitals) ☐ error — none

### LLR-2503.1 — `modals.pick_rows`
- **Traceability:** HLR-2503
- **Ledger:** LED-2026-10-21-batch-01.1, LED-2026-10-21-batch-01.2
- **Statement:** `taskboard/modals.py` shall provide `pick_rows(people, q, sel, w, limit) -> (rows, opts)`: `opts` the first `limit` people of `people.find(q)` as `("p", Person)`, then `("add", q.strip())` when `q` is not blank and `people.named(q)` is None; each row exactly `w` cells of Text pieces (the cursor `▶ `, the name in 14 cells — pink when highlighted — and the role muted; or `+ add '<q>'  new person`), the highlighted row shaded; `  type a name` when `opts` is empty.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_people_picker.py -k TC_2503`
- **Numeric pass threshold:** TC-2503: `an` → Ana, Andrés, Juana, Marta, `+ add 'an'`, every row 44 cells; `ana ruiz` → one person, no add; `""` → 5 people, no add; an empty directory → `type a name`; a name `[b]Bold[/b]` printed as typed.
- **Negative control:** TC-2503 goes RED when `+ add` shows for an exact name or for `@` alone (increment 003's battery — planned).
- **Boundary catalog:** ☑ boundary (the limit) ☑ empty (no people) ☑ invalid (markup-looking names) ☐ error — none

### LLR-2503.2 — `TaskModal`'s picker
- **Traceability:** HLR-2503
- **Ledger:** LED-2026-10-21-batch-01.1, LED-2026-10-21-batch-01.2, LED-2026-10-21-batch-01.4
- **Statement:** `TaskModal.__init__` shall take `people: Directory | None = None` (the app passes `self.people` for `a` and `e`); `TaskModal` shall compose a `MentionDrop` (`overlay: screen`, absolute, 48 cells, hidden) and bind `up`/`down` (`drop_move`), `enter` (`drop_pick`) as priority bindings that `check_action` lets act only while the picker is open, and `tab` (`drop_field`) — between the form's two fields while it is open; otherwise the list closed and the screen's `focus_next` (this binding replaces the screen's own `tab`); `drop_move`/`drop_pick` act on the form only while it holds the focus and on the list only while it lists someone; `on_descendant_focus` closes the picker when the focus leaves it; `_insert_mention` replaces the stored span (`_row`, `_at`, `_q`) only while it still reads `@<typed>`; on a notes change (unless the form is open) and on a cursor move while the list is open it shall re-read the text before the cursor with `MENTION_AT` (`(?:^|(?<=\s))@([^\s@]*)$`) and open, narrow or close the list; `action_cancel` steps back (form → list → closed) before cancelling the editor; an add calls `people.add` and notifies `The person was not added: <reason>` (`markup=False`) on `OSError`/`ValueError`.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_people_picker.py`
- **Numeric pass threshold:** as AT-2503, and `tests/test_edit_window.py`'s tab walk unchanged.
- **Negative control:** AT-2503 goes RED when `check_action` lets `enter` act while closed (no new line), when `tab` loses `focus_next`, when `esc` cancels the editor with the list open (increment 003's battery — planned).
- **Boundary catalog:** ☑ boundary (the screen's edges) ☐ empty — none ☑ invalid (inside a word; a known handle) ☑ error (the add refused)

### LLR-2504.1 — `views.person_items`, `people_by_urgency`, `progress_box`, `render_people_directory`
- **Traceability:** HLR-2504
- **Ledger:** LED-2026-10-21-batch-01.1, LED-2026-10-21-batch-01.2
- **Statement:** `taskboard/views.py` shall provide `PersonItem(band, lane, board_name, colour, task, project, due)`, `person_items(lanes, handle, today)` over the agenda's plain lanes (`is_open` tasks mentioning the handle, banded and sorted by band, due, lane, board order), `person_counts(items) -> (late, today, open)`, `people_by_urgency(people, items)`, `notes_text(text, people)` (the Text-piece notes of HLR-2506, which `modals.notes_preview` returns), `progress_box(items, w)` (three rows), `_scroll_tasks` (whole tasks, the `↓ N more below` row), `PEOPLE_TITLE = "PEOPLE · directory"` and `render_people_directory(people, items, sel, pane, row, today, width, height, directory) -> Text` drawing HLR-2504's rows exactly `width` cells each (the left pane 32 cells from 100, else 24; the chip 10 cells from a 70-cell pane, else 9; the project from 78), every string a Text piece.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_people_view.py -k TC_2504`
- **Numeric pass threshold:** TC-2504: Ana's five items in the bands late, today, week, later, later; counts (1, 1, 5); the urgency order Ana, Diego, Marta, Luis, Andrés, Elena, Juana, Pablo; an archived or done task not owed; an empty box `│ nothing open │`; at widths 116, 78, 40 every one of 29 rows is the width, `1 late · 1 today · 5 open` and the quote from 78, the project only at 116; each task's next row is its quote; markup-looking strings as typed; the empty directory's two lines; the tasks pane scrolled to the fifth task.
- **Negative control:** TC-2504 goes RED when a done task is owed, when the urgency key drops `today`, when the quote is not under its task (increment 004's battery — planned).
- **Boundary catalog:** ☑ boundary (widths, scrolling) ☑ empty (no people; nothing open) ☑ invalid (markup-looking strings; a missing board) ☐ error — none

### LLR-2504.2 — `app.PeopleDirectory` and `@`
- **Traceability:** HLR-2504
- **Ledger:** LED-2026-10-21-batch-01.1, LED-2026-10-21-batch-01.2
- **Statement:** `taskboard/keymap.py` shall declare `Key("at", "@", "people_directory", "People directory", group="misc", bar=False)`; `taskboard/app.py` shall provide `board_lanes(app)` (the agenda's lanes and ids, which `AllBoardsAgenda` now reads too) and `open_on_board(app, bid, task_id)` (pop every screen, `switch_board` when another, `jump_to` when there), `people_keys(pane)` (the key row per pane), and `PeopleDirectory(Screen)` with priority bindings `escape,at` (back), `up,k`/`down,j` (move), `left,h,right,l,tab` (pane), `enter`, `slash` (find), `n`, `e`; `TaskboardApp.action_people_directory` pushes it; `check_action` lets `people_directory` act as it lets `agenda_all`, and refuses every seat action but `quit` while it is on the stack.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_people_view.py -k "AT_2504 or D4"`
- **Numeric pass threshold:** as AT-2504; `KEYMAP` holds `@` labelled `People directory` off the bar and `9` labelled `People`; `tests/test_all_agenda.py` unchanged.
- **Negative control:** AT-2504 goes RED when the seat keys act behind the view or `@` acts over a modal (increment 004's battery — planned).
- **Boundary catalog:** ☐ boundary — none ☐ empty — none ☐ invalid — none ☑ error (the board missing at `enter`)

### LLR-2504.3 — `modals.PersonForm`, `n`, `e`, `/`
- **Traceability:** HLR-2504
- **Ledger:** LED-2026-10-21-batch-01.1, LED-2026-10-21-batch-01.2
- **Statement:** `taskboard/modals.py` shall provide `PersonForm(person=None)` (`ModalScreen[tuple[str, str, str] | None]`, `ButtonKeysMixin`, `escape` cancel and `alt+s` = `press_button('save')`, inputs `#f-name`, `#f-role`, `#f-note` under the labels `Name`, `Role`, `Note`, buttons `save`/`cancel`, the key line `↵ / alt+s save   ⇥ next field   esc cancel`, `enter` in a field saves), listed in `tests/test_modal_keys.py`'s inventory; `PeopleDirectory` shall add or edit through the directory on its result and find with `TextPrompt("Find a name")`.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_people_view.py tests/test_modal_keys.py`
- **Numeric pass threshold:** as AT-2504's `n`/`e`/`/` arms; TC-2407's law over `PersonForm`.
- **Negative control:** TC-2407 goes RED when `PersonForm` loses `alt+s` (increment 004's battery — planned).
- **Boundary catalog:** ☐ boundary — none ☑ empty (a blank name refused) ☐ invalid — none ☑ error (a failed write said)

### LLR-2505.1 — `views.matches`, `filter_bar`, `_apply_search_overlay`
- **Traceability:** HLR-2505
- **Ledger:** LED-2026-10-21-batch-01.1, LED-2026-10-21-batch-01.2
- **Statement:** `views.matches(task, board, q)` shall return `"person"` for a query `@<handle>` when the notes mention that handle and None otherwise, before any text rule; `filter_bar(query, hits, total, w, people=None)` shall write HLR-2505's person bar when the handle is in `people`; `_apply_search_overlay(..., people=None)` shall light no text for a person's query and pass `board.people` to the bar from both `render_view` branches.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_people_search.py -k TC_2505`
- **Numeric pass threshold:** TC-2505: `@ana.ruiz` on Client A → the four mentioning tasks, `person` or None only; `@ana` → none; `ana` keeps «Canary release plan»; the bar `/ @Ana Ruiz  Client A PM · tasks that mention them` … `3/11 tasks · esc clears`; `@zz` → `/ @zz▌`.
- **Negative control:** TC-2505 goes RED when the person rule falls through to the text rules (increment 005's battery — planned).
- **Boundary catalog:** ☐ boundary — none ☑ empty (an unknown handle) ☑ invalid (a partial handle) ☐ error — none

### LLR-2505.2 — `modals.SearchPrompt` and `/`
- **Traceability:** HLR-2505
- **Ledger:** LED-2026-10-21-batch-01.1, LED-2026-10-21-batch-01.2
- **Statement:** `taskboard/modals.py` shall provide `SearchPrompt(TextPrompt)` with keyword arguments `people` and `open_person`, priority bindings `up`/`down` (`move`) and `alt+p` (`page`) that `check_action` lets act only while the field starts with `@`, a `#sp-list` Static under the field, and `_save` dismissing `@<handle>` for a highlighted person; `TaskboardApp.action_search` shall push it with `open_person` pushing `PeopleDirectory(handle)`; `tests/test_modal_keys.py`'s law shall read a modal's buttons and bindings along its package bases, and list `SearchPrompt` with `TextPrompt`'s two buttons.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_people_search.py tests/test_modal_keys.py`
- **Numeric pass threshold:** as AT-2505; TC-2407's law over `SearchPrompt` (its painted key line holds `alt+s` and `esc cancel`).
- **Negative control:** AT-2505 goes RED when `alt+p` acts on a text query or `enter` sets the text `@an` (increment 005's battery — planned).
- **Boundary catalog:** ☑ boundary (6 rows) ☑ empty (no one) ☐ invalid — none ☐ error — none

### LLR-2506.1 — the preview, the details and the card
- **Traceability:** HLR-2506
- **Ledger:** LED-2026-10-21-batch-01.1, LED-2026-10-21-batch-01.2, LED-2026-10-21-batch-01.3
- **Statement:** `modals.notes_preview(text, people=None)` shall return `views.notes_text(text, people)` as one Text (with `people` None the pieces of before); `TaskModal` and `TaskDetails` shall pass their board's `people`; `views.mention_names(task, people)` shall give the names a task mentions and `_card_meta` shall append `(f"@{first name}{'+n' if more}", "pink")` before the archived mark and the due token.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_people_look.py -k TC_2506`
- **Numeric pass threshold:** TC-2506: the preview `Review with @Ana Ruiz` / `- send to @Diego Paz now` with both names `b #f472b6` and `send to ` in `soon`; `@an`, `@sofia.vega` dimmed; `None` → one `mut` piece; the card's last two tokens `@Ana+1`, `today`; a 12-cell card keeps `today` and drops `@Marta`.
- **Negative control:** TC-2506 goes RED when the mention is drawn outside its highlight segment or after the due (increment 002's battery — planned).
- **Boundary catalog:** ☑ boundary (a tight card) ☑ empty (no directory) ☑ invalid (unknown handles; markup-looking names) ☐ error — none

### LLR-2506.2 — the presentation's notes
- **Traceability:** HLR-2506
- **Ledger:** LED-2026-10-21-batch-01.1, LED-2026-10-21-batch-01.2, LED-2026-10-21-batch-01.3
- **Statement:** `views.present_mentions(text, people)` shall write known mentions `@Name` with NBSP for spaces; `present_note_lines(notes, w, people=None)` shall wrap that text; `mention_marks(people)` shall list the written forms longest first; `_present_note_markup(row, w, marks=())`, `_present_cut(..., marks=())`, `_present_stack(..., marks=())` and `_present_column(..., people=None)` shall paint each mark bold pink; `render_present` shall pass `board.people` and its marks in the split view and the gantt view's cursor note.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_people_look.py -k "TC_2506 and present or split"`
- **Numeric pass threshold:** TC-2506: at 24 cells `@Ana Ruiz` stays whole on one row; the split frame of Eval harness holds `@Ana Ruiz` and `@Andrés Lima`, not `@ana.ruiz`, and with no directory `@ana.ruiz`; a row's marks `bold #f472b6`.
- **Negative control:** TC-2506 goes RED when the NBSP is a space (a wrap splits the name) (increment 002's battery — planned).
- **Boundary catalog:** ☑ boundary (a narrow column) ☑ empty (no directory) ☐ invalid — none ☐ error — none

### LLR-2507.1 — nothing of the directory leaves
- **Traceability:** HLR-2507
- **Ledger:** LED-2026-10-21-batch-01.1, LED-2026-10-21-batch-01.2, LED-2026-10-21-batch-01.3
- **Statement:** `Board.people` shall stay out of `Board._to_dict` and every saved or pushed record; no module but `people.py` shall read or write `people.json`; mention parsing of pulled notes shall be total (the tokeniser never raises; an unknown handle draws as typed).
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_people_directory.py tests/test_people_look.py -k 2507`
- **Numeric pass threshold:** as HLR-2507's.
- **Negative control:** as HLR-2507's.
- **Boundary catalog:** ☐ boundary — none ☐ empty — none ☑ invalid (malformed mentions) ☐ error — none

### Information Flow Contract (IFC) — C-54

> Part A in every batch; Part B when the system's boundary has components a consumer can address independently. The block syntax, its fields and the rules that read them are in `templates/ifc-template.md`, which ships with the flow and is not copied into this batch.

- **Part A — flows:**

```
FLOW: the directory, from people.json to every board the app opens
  SOURCE : taskboard start; n / e in the people view; + add in the picker
  NODES  :
    - fn    : people.Directory.load
      owner : LLR-2501.1
    - fn    : people.Directory.add, edit, _commit
      owner : LLR-2501.2
    - fn    : app.TaskboardApp.__init__, _label_board, after_move, _warn_registry; models.Board.people
      owner : LLR-2501.3
  SINK   : ~/.taskboard/people.json; board.people (memory only); the unreadable notice
```

```
FLOW: a mention, from the notes' cursor to the stored handle and the drawn name
  SOURCE : @ typed in the task editor's notes
  NODES  :
    - fn    : people.MENTION_RE, mention_ids, split_mentions, handle_for
      owner : LLR-2502.1
    - fn    : modals.pick_rows
      owner : LLR-2503.1
    - fn    : modals.TaskModal (_scan, _draw_drop, action_drop_pick, action_cancel)
      owner : LLR-2503.2
    - fn    : views.notes_text; modals.notes_preview; views._card_meta
      owner : LLR-2506.1
    - fn    : views.present_mentions, present_note_lines, _present_note_markup
      owner : LLR-2506.2
  SINK   : board.json (the notes' text, @handle); the preview, the details, the card, the presentation
```

```
FLOW: a person's work, from every board to the people view
  SOURCE : @ on the main screen or the home; alt+p in the filter
  NODES  :
    - fn    : views.person_items, people_by_urgency, progress_box, render_people_directory
      owner : LLR-2504.1
    - fn    : app.board_lanes, open_on_board, PeopleDirectory; keymap.KEYMAP
      owner : LLR-2504.2
    - fn    : modals.PersonForm; app.PeopleDirectory (find, new, edit)
      owner : LLR-2504.3
  SINK   : the screen; on enter the main screen with the task's board open; people.json on n / e
```

```
FLOW: a person's filter, from / to the filtered view
  SOURCE : / in kanban or gantt, then @
  NODES  :
    - fn    : modals.SearchPrompt; app.TaskboardApp.action_search
      owner : LLR-2505.2
    - fn    : views.matches, filter_bar, _apply_search_overlay
      owner : LLR-2505.1
  SINK   : the filtered kanban / gantt and its bar; the people view on alt+p
```

```
FLOW: a mention through team sync
  SOURCE : the team timer's push and pull
  NODES  :
    - fn    : team_sync.TeamState.push, pull, foreign_tasks (unchanged); models.Board._to_dict
      owner : LLR-2507.1
  SINK   : the team folder's board.<user>.json; view 9
```

- **Part B — boundary decomposition:** `no — every flow is the app's own, addressed through its keys and its files`

---

## 5. Validation strategy

### 5.1 Methods

> **Two layers** (per the Two-layer validation rule). Every batch declares BOTH:
> - **Layer A — white-box / functional (`TC-NNN`):** validates the HLR/LLR mechanism (the HOW). Methods: `test`, `inspection`, `analysis`.
> - **Layer B — black-box / behavioral acceptance (`AT-NNN`):** validates the user story's outcome through the shipped surface (the WHAT). Method: `acceptance`.

Layer 0: the tokeniser, the handle, the directory's reads and writes, `pick_rows`, `person_items`, the renders, `matches`/`filter_bar` (TC-2501..TC-2507). Layer A: TC-2501..TC-2507 at the function and screen level. Layer B: AT-2501..AT-2507 drive the real app headless (`run_test`, keys) built by the shipped `open_app` on the round's synthetic boards and people under the seam home, reading the screen's text (Textual's SVG, row by row), the notices and the files; "another window" is a second `Directory` on the same file — the code a second process runs. Real-app captures at 118×30 and 80×24 of each item go to `evidence/captures/` (Windows Terminal PNGs, the round's capture method), item 1's composed frame among them for the operator.

### 5.2 Batch acceptance criteria
- every LLR has a passing TC; every story a passing AT through its surface;
- every new assertion RED on `base_ref` or by a recorded mutation; mutants KILLED on the new logic;
- the full suite in three sequential chunks: 0 failures; transcripts under the batch's evidence; 3025 + the new nodes;
- no test reads or writes the real home; no test leaves a `people.json.lock`.

---

## 6. Appendices (optional)

### 6.1 Extended glossary
### 6.2 Relevant design decisions
See `PLAN.md` §Key decisions and `docs/ARCHITECTURE.md` (amended by this batch: `taskboard/people.py`, `people.json`, `Board.people`, the people view).
### 6.3 Open risks
- **Security questions (the P1 scan):** `devflow-scan-spec.py` over this document, 2026-10-21: `flags: token, role, form, escape`, `security_required: true`, exit 1 (`evidence/scan-p1.txt`). The answers: `token` — the mention tokeniser (a regular expression over the notes, total, never a secret) and `boards.file_lock`'s random lock token (uniqueness of the holder, reused unchanged); `role` — a person's job title in the directory (free text, drawn as a Text piece), never an access role: nothing in this batch grants or checks a permission; `form` — `PersonForm` and the picker's name/role fields (input cleaned of control bytes and line breaks, capped, stored as data, never executed or parsed as markup); `escape` — the `esc` key's step-back and, for markup, every name, role, note and title drawn as a plain Text piece (S1), the new notices `markup=False`. The directory holds personal data about third parties (names, roles, a free note): it lives in the operator's home only, is written by `write_atomic` (a new file in `mkstemp`'s owner-only mode, an existing one keeping its own mode; the `.corrupt` copy `keep_aside` makes follows the umask on POSIX — accepted and logged, security S-2 — and a still-unreadable file gets one more copy per start until it is replaced — accepted and logged, S-3), is never pushed (HLR-2507), and every string read from it is cleaned of control bytes and drawn as a Text piece; the lock and the corrupt copy follow the registry's reviewed pattern; no network, credential or permission change.
- **A teammate sees handles** (D4): a mention travels as `@ana.ruiz`; the teammate's own directory may name another person by the same handle. Accepted (the round's consequence).
- **A strong rename leaves the old handle in the raw text** (`@luis.mora` for «Luis Moreno»): accepted (the storage verdict).
- **A mention of a removed or unknown handle** is drawn as typed, dimmed; no person can be removed in this batch.
- **The people view reads every board at open** (`peek_board`), like `A`: once, no latency criterion.
- **Mentions in other views** (focus snippet, swimlanes, report) keep the stored handle: out of the verdict's three places.
- **`tab` in the editor**: the picker's `tab` binding replaces the screen's and calls `focus_next` itself when the picker is closed (the tab walk is held by `tests/test_edit_window.py`).
- **The split view's raw `!!…!!`/`++…++`** (pre-existing): logged in `BACKLOG.md`, not fixed.
- **Another window's new person** shows here after a restart or this window's next write (architect A-7): accepted.
- **The presentation paints by name** (security S-4): a literal `@Ana Ruiz` with non-breaking spaces typed by a teammate is painted like a mention; cosmetic, escaped — accepted.
- **Format characters in names** (U+200B–U+200F, U+202A–U+202E) survive `strip_controls` (S-5, pre-existing rule; handles cannot carry them): accepted, logged.

### 6.4 Phase-1 reconciliation log — moved to the ledger (§7)

### 6.5 Requirement amendments — moved to the ledger (§7)

---

## 7. The ledger — authored as a SEPARATE FILE

The fence below is the ledger's seed: `devflow-init.py` writes it to `01-requirements-ledger.md`. The shape of an entry is in the field guide.

```markdown
# Requirements ledger — taskboard — Batch 2026-10-21-batch-01

> Append-only. Entries are added in chronological order and never rewritten. The live
> contract is `01-requirements.md`; this file records how it came to say what it says.
> Every entry names the requirement it amends; every requirement names its entries. `V26`
> compares the two sets of pairs both ways.

_No entries yet. The first amendment to the live contract writes the first one, in the
shape the field guide's §7 shows (`req-template.part2.md` in the guide directory init prints), and nothing
above this line is ever edited._
```
