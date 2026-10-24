# Requirements Document — taskboard — Batch 2026-10-24-batch-01

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
The live contract for batch 2026-10-24-batch-01: the milestone-marks round (`prototypes/milestone_marks/`) as the operator's verdict chose it — shape-and-colour classes for milestones: one class directory for every board, a task field carrying the class, one rendering seat for every milestone mark, the editor's class Select, the `#` class manager, the legend strip, hide/show and `/#cls` search — with the round's eight decisions (MM-D1..MM-D8) and `proto.py` as the design oracle.

### 1.2 Scope
In: `models` — `taskboard/marks.py` (NEW: the class directory), `taskboard/models.py` (`Task.mark`, written only when set); `app` — `taskboard/app.py` (the directory loaded at start beside `people.json` and handed to every board, `MarksManager`, the notices routed through the seat); `views` — `taskboard/views.py` (`milestone_mark` the one seat, `render_marks` the manager's pure frame, `legend_strip`/`legend_strip_project`, `_hide`/`present_tasks_m`, `matches_m`/`filter_bar_m`); `modals` — `taskboard/modals.py` (the class `Select` in `TaskModal`, `MarkForm`); `keymap` — `taskboard/keymap.py` (`#` in `KEYMAP`); `taskboard.tcss`; the tests and `tests/milestone_marks_fixture.py` (the round's synthetic boards and its four example classes, copied so no test imports a prototype); `README.md`, `docs/ARCHITECTURE.md` (already amended by the ARQ), `.dev-flow/BACKLOG.md` (docs). Out: class deletion (not offered); the `▲` ambiguity fix (MM-D5's log ruling, to `BACKLOG.md` at close); the gantt month ruler's lateness, the unclassified milestone's red mark and the class/project colour resemblance (MM-D1's accepted costs); the legend in the agenda and people views (the strip's placement is the gantt and the presentation); the round's variant C (the class band), variant A/C encodings and the `↵ only this` solo mode; the editor Select's `+ new class…` option (proto.py:567-568) — adding a class is the manager's job (`n`), the Select only picks; pushing or merging.

### 1.3 Definitions, acronyms, abbreviations
| Term | Definition |
|------|------------|
| the round | `prototypes/milestone_marks/` (commit `8c83395`) and the operator's verdict on it |
| a class | one milestone class of the directory: `id`, `name`, `shape`, `colour`, `hidden` |
| the directory | `marks.json` beside the boards registry — `~/.taskboard/marks.json` for the app `taskboard` opens — holding every class; one for all boards |
| the seat | `views.milestone_mark(task, board, today) -> (glyph, style, late_chip)` — the one function every milestone mark renders through |
| the manager | the screen behind `#`: the classes listed, `n` the class form, `space` the hide toggle |
| the legend strip | one row under the gantt's ruler and in the presentation naming the classes drawn in the frame and the hidden count |
| `HOLLOW` | the reached-state map shape → hollow glyph (`◆→◇`, `▲→△`, …), proto.py:83 |
| `SHAPES` | the manager's one-cell shape set `▲ ■ ⬢ ★ ⬟ ▼ ✦ ⚑` (proto.py:85) — the form's shape row is over these alone (LED .46); `◆` is NOT a member, it is the unclassified mark's glyph shown in the Select's `none` option and the manager frame, so the load validation (LLR-2601.1) never drops a saved class |
| `mark` | a task's class field: the class id, `str \| None`, written only when set, meaningful only on a milestone |
| unclassified | a milestone whose `mark` is unset or names a class the directory does not hold: drawn `◆` in `mut` |

### 1.4 References
- The operator's commission (2026-10-24, `prototypes/milestone_marks/IMPLEMENTATION.md`), relayed by the orchestrator, and the round's verdict, verbatim: «D1: B · D2: global (recomendada, sin marcar) · 1 model: B · 2 editor: A (recomendada, sin marcar) · 3 legend: B · 4 filter: B · notes: (none)».
- The round's code, the spec of each chosen variant: `prototypes/milestone_marks/proto.py` (`mark_key`'s variant-B branch :119-120, `gantt_milestone_cells_m` :148, `band_milestone_facts_m` :186, `agenda_row_m` :206, `legend_strip` :246, `_hide` :294, `legend_strip_project` :353, `present_tasks_m` :367, `matches_m` :505, `filter_bar_m` :512, `EditorSelect` the variant-A Select mounted after `#f-milestone` :560-577, `MarkForm` :774, `MarksWindow` the `#` manager :852, `HOLLOW` :83, `SHAPES` :85); its captures (`out/`) are the visual oracle.
- The round's decisions as the commission states them (`IMPLEMENTATION.md` §2): MM-D1 the encoding (shape+colour say the class, state moves to text, hollow = reached); MM-D2 the global store (one directory, slug ids stable on rename); MM-D3 the task field (written only when set, unknown ids unclassified and kept, untick keeps the field, sync travels it unchanged); MM-D4 no seeded classes; MM-D5 the shapes (`●` excluded — the gantt's progress dot; wide/ambiguous glyphs excluded; the `▲` ambiguity logged, not fixed); MM-D6 hide/show (`space` in `#`, persisted; hidden classes leave the gantt and the presentation; the legend counts them; `/#cls` search); MM-D7 the legend (under the gantt ruler and in the presentation with its exports, only the drawn classes, none when none in view; `?` names the classes); MM-D8 the keys (every modal button a direct shown key, `#` opens the manager, `alt+m` focuses the Select and joins `TASK_KEYS`).
- The batch plan: `.dev-flow/2026-10-24-batch-01/PLAN.md` (D-1..D-4; the ARQ's A-1 folded as D-4: `views.render_marks` ships in increment 002).
- The amended module map: `docs/ARCHITECTURE.md` (the marks rows, `docs/ARCHITECTURE.md`:41,66-70,128-134,175).
- The shipped code this batch touches: `taskboard/boards.py` (`file_lock`, `keep_aside`), `taskboard/models.py` (`write_atomic`, `clean_strings`, `Board._to_dict` :1045-1053, the `show_in_present` written-only-when-set pattern :1049-1050), `taskboard/people.py` (`Directory`, `handle_for` :248 — the reuse pattern), `taskboard/views.py` (the section-3 sites, §4 below), `taskboard/modals.py` (`ButtonKeysMixin` :322, `TASK_KEYS` :378, `#task-chips-what` :501, `#f-milestone` :513), `taskboard/keymap.py` (`KEYMAP` :55-202 — `#` free, premise P-4), `taskboard/app.py` (the directory load :1102, `board.people` :1208, the unreadable notice :1312-1315, the notices :2133/:2172 (and :2433 only while it shows a milestone mark — today it is a project-span due mark, LLR-2604.2's exclusion list), `present_tasks` :47/:390), `taskboard/team_sync.py` (`TeamState.push` :143, `board._to_dict(t)` :157), `tests/conftest.py` (:26-35, the home seam).

### 1.5 Document overview
§2 the stories, premises and fork preconditions; §3 eight HLRs; §4 seventeen LLRs and the information-flow contract; §5 the validation strategy; §6 the decisions and open risks.

---

## 2. Overall description

### 2.1 Product perspective
taskboard draws every milestone as `◆` tinted by its state, in eleven-plus sites that each encode the mark on their own; there is no way to say what kind of milestone it is. This batch adds one directory of classes (shape + colour + a hidden flag) shared by every board, a task field carrying the class, and one rendering seat through which every milestone mark is drawn — classifying at a glance, hiding a class everywhere with one toggle, and filtering by class with `/#cls` — porting the round's chosen variants; each was the real `TaskboardApp` with patched functions, so the port moves that code into the shipped classes.

### 2.2 Product functions
1. One directory of milestone classes (id, name, shape, colour, hidden) for every board, in the home beside `people.json`, written safely beside a second window; starts empty.
2. A task's `mark` field carrying the class id, written only when set, kept when `milestone` is unticked, travelling unchanged on team sync; an unknown id renders unclassified and is never dropped.
3. Every milestone mark drawn by one seat: shape and colour say the class; a late date turns `over` with an `▲Nd` chip; a reached mark is hollow with `✓` in `reached`; an unclassified mark is `◆` in `mut` — in the lanes, focus, bank, kanban, gantt, band rules, presentation, agenda, people view and the app's notices.
4. The editor's variant A: an `alt+m` Select in the chip row after `milestone`; `#` opens the manager where `n` adds a class (name, shape, colour) and `space` hides one.
5. The legend strip under the gantt ruler and in the presentation naming the drawn classes and the hidden count; hidden classes gone from the gantt, the presentation views and their exports; `/#pay` filters to a class.

### 2.3 User characteristics
The operator alone (`username_subject`), keyboard only, at a meeting or presenting to a room; several boards; Windows Terminal at 118×30 and 80×24.

### 2.4 Constraints
Standard library and the shipped dependencies only; Windows-safe; the directory written with the registry's lock-and-atomic-write pattern (`boards.file_lock`, `models.write_atomic`, `boards.keep_aside`, batch 2026-10-20-batch-02 / 2026-10-21-batch-01); at most 4 SOURCE files per increment (tests uncapped); every class string — name above all — drawn as an explicit-style `Text` piece, never markup (C-17); every new modal button has a direct shown key (`tests/test_modal_keys.py`'s law); team sync never carries the directory; synthetic data only (the round's four example classes live only in test fixtures and captures); the operator's name nowhere; tests never touch the real home; `marks.json` starts empty — no seeded classes.

### 2.5 Assumptions and dependencies
Textual names the `#` key `number_sign` and `#` is bound nowhere in the app (P-4); one home folder per operator; `people.py`'s `Directory` is the reuse pattern for `marks.py` (P-3); the editor's `#task-chips-what` / `#f-milestone` mount points hold (P-5); the conftest seam keeps tests off the real home (P-6); the suite's baseline is 3152 passed, re-measured at P4 (P-8). The calendar is frozen in the tests as the round's fixture.

### 2.6 Source user stories

| ID | User Story | Source | DoR status |
|----|------------|--------|------------|
| US-2601 | As the operator, I want one directory of milestone classes — a name, a shape, a colour, a hidden flag — shared by every board and safe from a second window, and a task field carrying the class, so that a class is written once and classifies anywhere. | MM-D2, MM-D3, MM-D4; AT-a, AT-c (store side), AT-g | READY |
| US-2602 | As the operator, I want every milestone mark drawn by one rule — the shape and colour say the class, lateness and reached state move to text beside the mark — in every view and notice, so that I classify milestones at a glance and no frame drifts. | MM-D1; section 3; AT-b | READY |
| US-2603 | As the operator editing a milestone, I want `alt+m` to open the class Select and `#` to open the manager where `n` adds a class and `space` hides one, so that classifying is two keys and the modal law holds. | MM-D5, MM-D6 (storage), MM-D8; AT-a, AT-f | READY |
| US-2604 | As the operator, I want the legend strip under the gantt ruler and in the presentation naming the drawn classes and the hidden count, hidden classes gone from the gantt and every presentation view and export, and `/#cls` to filter, so that the classification reads in the frame and filters like anything else. | MM-D6, MM-D7; AT-d, AT-e | READY |

**The chains, one line each:** US-2601 → HLR-2601, HLR-2602, HLR-2603 → AT-2601, AT-2602, AT-2607 · US-2602 → HLR-2604 → AT-2603 · US-2603 → HLR-2605, HLR-2606 → AT-2601, AT-2604 · US-2604 → HLR-2607, HLR-2608 → AT-2605, AT-2606 (set at P1; the commission's AT-a..AT-g map onto AT-2601..AT-2607).

#### Refinement log (one block per story)

**US-2601 — the store and the field**
- **INVEST:** I ✓ · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality (V, N):** user = the operator · outcome = `~/.taskboard/marks.json` read at start beside `people.json`, written under its lock; a task's `mark` field · why = MM-D2, MM-D3 · out of scope = seeded classes (MM-D4); class deletion (not offered)
- **Feasibility (E, S):** a new `taskboard/marks.py` in the `models` layer reusing `boards.file_lock`, `keep_aside` and the atomic-write pattern of `people.py`; `Task.mark` in `models.py` written only when set · fits one batch? = yes, increment 001
- **Evaluability (T) — behavioral, black-box:** `open_app` on the round's boards: a class added in `#` survives a restart in `marks.json`; two windows each add a class and both survive; an unreadable `marks.json` is set aside never overwritten; a board with no marks keeps its bytes; a task whose `mark` is unknown renders unclassified and keeps the id on save.
- **Open questions:** none. · **Classification:** `READY`.

**US-2602 — the encoding through one seat**
- **INVEST:** I ✓ (after 001) · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality (V, N):** user = the operator · outcome = every milestone mark in every view drawn by `views.milestone_mark(task, board, today)` — class glyph+colour, late date in `over` plus `▲Nd`, reached hollow plus `✓`, unclassified `◆` in `mut` · why = MM-D1 · out of scope = the title glyphs and the project-span due marks (section 3's exclusions); the gantt ruler's lateness (accepted cost)
- **Feasibility (E, S):** one seat in `views.py`; every site listed in section 3 routed through it; `app.py`'s notices at 2133/2172 (2433 is a project-span due mark — excluded, the ARCH-1 fold) · fits one batch? = yes, increment 002
- **Evaluability (T) — behavioral, black-box:** on the round's boards: a late classed milestone shows its date in `over` with `▲3d`; a reached one the hollow glyph with `✓`; an unclassified one `◆` in `mut`; a test enumerates the sites so a new frame cannot skip the seat.
- **Open questions:** none. · **Classification:** `READY`.

**US-2603 — the editor Select and the `#` manager**
- **INVEST:** I ✓ (after 001) · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality (V, N):** user = the operator · outcome = the editor's variant A: an `alt+m` Select in `#task-chips-what` after `#f-milestone`; the `#` manager window listing the classes, `n` opening its form (name, shape, colour), `space` toggling `hidden`; `#` free in `keymap.py` and `alt+m` in `TASK_KEYS` · why = MM-D5, MM-D6 (storage), MM-D8 · out of scope = class deletion; the ▲ ambiguity fix (MM-D5's log ruling)
- **Feasibility (E, S):** `modals.py` (the Select and `MarksManager` + the form), `keymap.py` (`#`), `app.py` (the screen), `taskboard.tcss` · fits one batch? = yes, increment 003, 4 source files
- **Evaluability (T) — behavioral, black-box:** `#`, `n`, a name, a shape, a colour, `alt+s`: the class is in `marks.json`; `e` on a milestone, `alt+m`, `down`, `↵`: the task carries the class and the gantt draws the class glyph; `tests/test_modal_keys.py` covers the manager and its form; unticking `milestone` keeps the field.
- **Open questions:** none. · **Classification:** `READY`.

**US-2604 — the legend, hide, search and help**
- **INVEST:** I ✓ (after 002) · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality (V, N):** user = the operator · outcome = the legend strip under the gantt ruler and in the presentation with its exports, naming only the drawn classes and the hidden count; hidden classes leave the gantt and all three presentation views and exports; `/#pay` filters by class; `?` names the classes · why = MM-D6, MM-D7 · out of scope = the legend in the agenda and people views (the strip's placement is the gantt and the presentation)
- **Feasibility (E, S):** `views.legend_strip` of the round; `matches_m`/`filter_bar_m`; `app.py` the help · fits one batch? = yes, increment 004, 3 source files
- **Evaluability (T) — behavioral, black-box:** on the round's boards: the gantt's strip names the drawn classes and `1 hidden`; after `space` in `#`, that class's milestones are gone from the gantt and all three presentation views and their exports; `/`, `#pay`, `↵` filters to that class.
- **Open questions:** none. · **Classification:** `READY`.

### 2.7 Premise evaluation (C-43) — MANDATORY, one row per premise

| # | Premise, as a truth-apt proposition | Tier (axiom · hypothesis · premise) | Verdict | Executed evidence (command output / `file:line` — **NOT** a citation of another document) | Disposition |
|---|---|---|---|---|---|
| P-1 | The round's chosen variants exist in `prototypes/milestone_marks/proto.py` at the cited lines: `HOLLOW` :83, `SHAPES` :85, `mark_key`'s variant-B branch :119-120, `gantt_milestone_cells_m` :148, `band_milestone_facts_m` :186, `agenda_row_m` :206, `legend_strip` :246, `_hide` :294, `legend_strip_project` :353, `present_tasks_m` :367, `matches_m` :505, `filter_bar_m` :512, the variant-A `EditorSelect` with its Select mounted after `#f-milestone` :560-577, `MarkForm` :774, the `#` manager `MarksWindow` :852 | premise | TRUE | `evidence/premises.py`: `` P-1 … all found: True `` (`evidence/premises.txt`) | the design oracle every view/editor/manager LLR ports |
| P-2 | The commission's section-3 milestone sites still hold on this tree (base_ref `7e66e0e` + the two prototype commits): lanes :1107/:1113, focus :1677/:1689, the bank edge :1800, the kanban/focus glyph :2037, the gantt :2541/:2554/:2643/:2732/:3035/:3078/:3615, the band facts :5069-5099 and the fold row :5310, the presentation field row :6538-6547, the agenda's `_agenda_row` :7146 (draws no `◆` today — the round adds it), the people view's `_task_rows` :8433, and `app.py`'s milestone notices :2133/:2172 (`:2433` is a project-span due mark — `{pn} +{over}d past ◆` — not a milestone seat site; it moved to the exclusion list at the P2 fold, ARCH-1); the exclusions stand untouched: the title glyphs (:1225 and siblings), the project-span due marks (:2613/:3030/:3044/:6579) and the slip notice (:2433) | premise | TRUE | `` P-2 … notice reached @2133 \| notice milestone @2172 \| all found: True \|\| exclusions stay: title glyph @1225 \| project due @2613 \| sel_p due @3030 \| mlabel due @3044 \| present proj due @6579 \| app slip notice (project-span, excluded) @2433 `` (`evidence/premises.txt`) | the seat's site list (LLR-2604.2) and its exclusion list |
| P-3 | `taskboard/people.py`'s `Directory` provides the reuse pattern: `file_lock, keep_aside` (:27), `write_atomic` (:28), `PEOPLE_NAME` (:30), `Directory.load` (:119) with `keep_aside` on the unreadable (:130), `_commit` under `file_lock` (:187) with `write_atomic` (:198), `handle_for` (:248) | premise | TRUE | `` P-3 … all found: True `` (`evidence/premises.txt`) | `marks.py` mirrors it (LLR-2601.1/.2) |
| P-4 | `#` is free as a key: no `number_sign` and no quoted `#` key in `keymap.py` (`KEYMAP`, :55-202), none in `app.py` | premise | TRUE | `` P-4 '#' free as a KEY: number_sign in keymap.py: False \| a quoted '#' key in keymap.py: False \| number_sign in app.py: False `` (`evidence/premises.txt`) | `#` opens the manager (LLR-2606.1) |
| P-5 | The modal-keys law's parts exist: `ButtonKeysMixin` (`modals.py:322`), `TASK_KEYS` (`modals.py:378`), `#task-chips-what` (`modals.py:501`), `#f-milestone` (`modals.py:513`), `tests/test_modal_keys.py` | premise | TRUE | `` P-5 modal law + editor seats: ButtonKeysMixin @322 \| TASK_KEYS @378 \| #task-chips-what @501 \| #f-milestone @513 \| test_modal_keys.py: True `` (`evidence/premises.txt`) | the editor Select (LLR-2605.1) and the law (AT-2604) |
| P-6 | The conftest seam keeps tests off the real home: `tests/conftest.py` monkeypatches `Path.home` (:26-35) | premise | TRUE | `` P-6 conftest seam: Path.home monkeypatched: True \| line @35 `` (`evidence/premises.txt`) | every AT/TC runs under a temp home |
| P-7 | The app already loads a directory beside the registry and hands it to boards: `Directory.load(self.registry.path.parent / PEOPLE_NAME)` (`app.py:1102`), `self.board.people = self.people.people` (:1208), the unreadable-file notice (:1312-1315), `present_tasks` consumed by the presentation (:390) | premise | TRUE | `` P-7 … all found: True `` (`evidence/premises.txt`) | the marks directory loads and travels the same way (LLR-2601.3); the presentation's hide wrapper (LLR-2608.1) |
| P-8 | The suite's scale: `tests/` holds 106 test files with 1469 test functions (static AST count); the commission records the full-suite baseline as 3152 passed | hypothesis | TRUE | `` P-8 tests/ static count: 106 files, 1469 test functions … `` (`evidence/premises.txt`); the 3152 baseline is re-measured at P4 (three sequential chunks) | §5.2's suite criterion |

- **Premise evaluation:** 8 premise(s) · ✅ TRUE ×8

### 2.8 Fork preconditions (C-52) — MANDATORY, and the declared empty when the batch does not fork

- **Fork preconditions:** none — this batch runs one lane: four increments in order on one branch (`feat/milestone-marks`), one owner (the orchestrator) holds the trunk.

---

## 3. High-level requirements (HLR)

### HLR-2601 — One marks directory for every board
- **Traceability:** US-2601
- **Ledger:** LED-2026-10-24-batch-01.1, LED-2026-10-24-batch-01.30, LED-2026-10-24-batch-01.39, LED-2026-10-24-batch-01.44
- **Statement:** The system shall keep one directory of milestone classes in `marks.json` beside the boards registry (`~/.taskboard/marks.json` for the app `taskboard` opens; beside `people.json` — one directory for every board), each class an `id`, a `name` (1–60 characters, one line, no control characters), a `shape` (one of the manager's shapes), a `colour` and `hidden` (`false` on creation); the `id` shall be a slug of the name made as `people.handle_for` makes handles (`people.py:248`) and shall never change when the class is renamed; the file shall start empty — no seeded classes; the system shall read the file at start without ever raising — a missing, empty or blank file an empty directory, nothing written and nothing said; an unreadable one (a failed read, not JSON, not an object holding a `marks` list) an empty directory after a byte copy at `marks.json.corrupt` (`boards.keep_aside`, never replacing an earlier copy) and one warning notice `marks.json could not be read; a copy was kept at <path>. The marks directory starts empty.` — `…; no copy could be kept. …` when the copy failed; an entry with a malformed or repeated id, no name, an unknown shape or colour, or a field of the wrong type, is skipped; the system shall write the file only when a class is added, edited or hidden, atomically, under `marks.json.lock`, as a read-modify-write of what the file holds then (another window's classes kept); a window reads the file at start and after its own writes only, so a class another window adds shows here after a restart or this window's next write (accepted).
- **Rationale (informative):** MM-D2 (one directory for every board; a class is id/name/shape/colour/hidden; the id a slug of the name, stable on rename) and MM-D4 (`marks.json` starts empty — the round's four examples live only in test fixtures and captures).
- **Validation:** `test`
- **Executed verification:** `env -u NO_COLOR python -m pytest -q -p no:cacheprovider tests/test_marks_directory.py`
- **Numeric pass threshold:** AT-2601: the round's boards (`tests/milestone_marks_fixture.py`, NEW) under the seam home, `open_app(None)` at 118×30: `#`, `n`, a name, a shape, a colour, `alt+s` → the file `<home>/.taskboard/marks.json` exists on disk and holds the class with `hidden: false` (read back from disk, not through the app); restart the app → the class still there; the gantt draws the class glyph in its colour beside the milestone's title and on its date; an entry named 61 characters is cut to 60, 60 kept whole; a class renamed keeps its id (the file's id unchanged, the name new); `?` lists the manager.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** one set of classes on every board; a class written once in `#` is there after a restart; a broken file never stops the app and is kept.
  - **Shipped surface:** `taskboard` → `#`, `n`; `~/.taskboard/marks.json`.
  - **Acceptance test(s):** AT-2601 — realised by ONE node, `tests/test_marks_manager.py::test_AT_2601_a_class_is_created_and_survives` (NEW — created in Phase 3, provisional per V-5); the threshold's other clauses are TC-2601 arms driven through the same surface.
  - **Boundary catalog (QC-3):** ☑ boundary (a name of 60 / 61 characters) ☑ empty (no file: an empty directory, nothing written) ☑ invalid (bad entries skipped; control bytes stripped; an unreadable file kept aside) ☑ error (the lock held: `busy`, nothing changed; a failed write: nothing changed in memory)
  - **Negative control:** on `base_ref` AT-2601 is RED: `taskboard.marks` does not exist (`evidence/red-p1.txt` — executed: `ModuleNotFoundError`); the node-minted RED and mutation battery land in the increment's evidence at P3 (C-40).

### HLR-2602 — A task carries the class, and the field never degrades
- **Traceability:** US-2601
- **Ledger:** LED-2026-10-24-batch-01.2
- **Statement:** The system shall give every task a `mark` field — `str | None`, the class id — meaningful only on a milestone; the field shall be written to the board file only when set, in the `show_in_present` pattern of `Board._to_dict` (`models.py:1045-1053`: a default dropped, an absent key read back as the default), so a board with no marks keeps its bytes; an unknown id — a deleted class, or a teammate's class this directory does not hold — shall render as unclassified in every view and shall never be dropped or rewritten on save; unticking `milestone` in the editor shall keep the field, so the class returns when the box is ticked again; team sync shall carry the field unchanged — a push writes the task's own dict (`team_sync.py:157`), a pull stores what the teammate's file holds; the directory itself shall never travel.
- **Rationale (informative):** MM-D3 (the field, unknown ids, untick keeps, sync travels) and its consequence: a teammate without my directory sees the id render unclassified, kept — so no frame may encode the class locally.
- **Validation:** `test`
- **Executed verification:** `env -u NO_COLOR python -m pytest -q -p no:cacheprovider tests/test_marks_directory.py tests/test_milestone_marks.py -k 2602`
- **Numeric pass threshold:** AT-2607: a board file with a task whose `mark` names a class no directory holds → opened, drawn (`◆` in `mut`), edited and saved → the file still holds the id byte-for-byte; a board whose tasks carry no `mark` → loaded and saved → the file byte-identical; a task with a class, `milestone` unticked, saved → `mark` kept; a pushed board file carries the id, none of the directory's names.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** classifying a milestone is one field; boards without marks are untouched; a teammate's class never breaks a frame.
  - **Shipped surface:** the task editor (`e`); the board file (`board.json`); the team folder.
  - **Acceptance test(s):** AT-2607 — realised by ONE node, `tests/test_milestone_marks.py::test_AT_2607_an_unknown_id_is_safe` (NEW — created in Phase 3, provisional per V-5); and AT-2601 (the field set through the editor)
  - **Boundary catalog (QC-3):** ☑ boundary (a mark set while `milestone` is unticked: kept, drawn nowhere) ☑ empty (no mark: the file gains no key) ☑ invalid (an unknown id: unclassified, kept) ☑ error (a save with the board lock held: unchanged, said)
  - **Negative control:** on `base_ref` the field does not exist (`Task.mark` absent — `evidence/red-p1.txt` executes the absence at the module level); the round-trip RED (an id dropped by a save) is minted with the node at P3 (C-40).

### HLR-2603 — The store is safe beside a second window
- **Traceability:** US-2601
- **Ledger:** LED-2026-10-24-batch-01.3, LED-2026-10-24-batch-01.36
- **Statement:** The system shall write `marks.json` safely beside a second window: every write a read-modify-write under `boards.file_lock` (`marks.json.lock`) — the file re-read as it holds now, the change applied to that, the write atomic through `models.write_atomic` — so two windows each adding a class both survive; an unparseable file shall be kept aside before it is replaced and shall never be written over when it cannot be copied aside; a failed write shall change nothing in memory and raise to its caller, which says so.
- **Rationale (informative):** MM-D2's «written exactly like `taskboard/people.py`'s `Directory`» and the commission's AT-c (two windows, the unreadable file, the bytes).
- **Validation:** `test`
- **Executed verification:** `env -u NO_COLOR python -m pytest -q -p no:cacheprovider tests/test_marks_directory.py -k "AT_2602 or TC_2603"`
- **Numeric pass threshold:** AT-2602: two `Directory` objects on one `marks.json` (the code a second process runs) each add a class → both in the file and in each object's live dict after its own write; `marks.json` = `{oops` → one notice, `marks.json.corrupt` holds `{oops`, the file unchanged, the directory empty; the corrupt copy never replaced by a later unreadable file; a board whose tasks carry no `mark` → loaded and saved → byte-identical; the lock held (`LOCK_WAIT` 0.2) → `OSError` naming `busy`, no file, memory unchanged.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** two windows adding classes lose nothing; a broken `marks.json` is kept, never overwritten; boards without marks keep their bytes.
  - **Shipped surface:** `~/.taskboard/marks.json`, `marks.json.lock`, `marks.json.corrupt`; any board file.
  - **Acceptance test(s):** AT-2602 — realised by ONE node, `tests/test_marks_directory.py::test_AT_2602_the_store_is_safe` (NEW — created in Phase 3, provisional per V-5); the two-window arm is the rule-(d) file-as-surface exception, recorded: two `Directory` objects are the code a second process runs, and the observable surface the test asserts is `marks.json` on disk — both classes in the file after each window's add
  - **Boundary catalog (QC-3):** ☑ boundary (two writers, no interleaving loss) ☑ empty (no file: nothing written until the first add) ☑ invalid (`{oops`, `[]`, bad bytes: kept aside) ☑ error (the lock; a failed `write_atomic`; an unkeepable file)
  - **Negative control:** on `base_ref` AT-2602 is RED: no `marks.py` (`evidence/red-p1.txt` — executed); the two-window RED (a write that skips the re-read erases the first class) is minted with the node at P3 (C-40).

### HLR-2604 — One seat draws every milestone mark
- **Traceability:** US-2602
- **Ledger:** LED-2026-10-24-batch-01.4, LED-2026-10-24-batch-01.26, LED-2026-10-24-batch-01.37, LED-2026-10-24-batch-01.42
- **Statement:** The system shall draw every milestone mark in every view and notice through one seat, `views.milestone_mark(task, board, today) -> (glyph, style, late_chip)`: the class's shape and colour say the class — an unclassified milestone (no mark, or an id the directory does not hold) keeps `◆` in the neutral `mut` tone; when late, the date beside the mark turns `over` and an `▲Nd` chip follows; when reached, the mark is drawn hollow (`HOLLOW`, proto.py:83) plus `✓` in `reached`; the sites routed through it: the lanes and focus title markers (`views.py:1107`/`:1113`, `:1677`/`:1689`), the bank edge (`:1800`), the kanban/focus field glyph (`:2037`), the gantt's title prefix `_milestone_title` (`:2541`), `gantt_milestone_cells` (`:2545`-`:2576`), the one-date bars (`:2643`, `:2732`), the ruler milestones (`:3035`), the row label (`:3078`), the chain map's label (`:3613`-`:3617`), the band rule facts `band_milestone_facts` (`:5053`-`:5099`) and the `▲N ◆` fold row (`:5310`), the presentation's field row `_present_task_row` (`:6537`-`:6547`), the agenda's row (`_agenda_row`, `:7146` — today it draws no `◆`; the round adds the mark before the title, proto.py:206), the people view's task rows (`_task_rows`, `:8433`-`:8467`) and `app.py`'s notices when they show a milestone mark (`:2133`, `:2172` — the commission's §3 words; `:2433` qualifies only while it shows one, which today it does not: it is a project-span due mark, `{pn} +{over}d past ◆`, and stays as it is); a test shall enumerate the sites so a new frame cannot skip the seat; the title glyphs (`◆ TASKBOARD`, `◆ GANTT`, …) and the project-span due marks (`views.py:2613`, `:3030`, `:3044`, `:6579`, `:6856`, and `app.py:2433` among the notices) stay as they are.
- **Rationale (informative):** MM-D1 (verdict D1 B) and the commission's §3: «Route them all through ONE seat … so that no site encodes MM-D1 on its own. A test enumerates the sites.» The accepted costs recorded by the round: the gantt month ruler shows no lateness; an unclassified milestone loses its red mark; a class colour can resemble a project colour.
- **Validation:** `test`
- **Executed verification:** `env -u NO_COLOR python -m pytest -q -p no:cacheprovider tests/test_milestone_marks.py`
- **Numeric pass threshold:** AT-2603: the round's boards at 118×30 and 80×24: a late classed milestone (due 3 days past, open) shows its date in `over` with `▲3d` beside the class glyph in the class colour; a reached one the hollow glyph plus `✓` in `reached`; an unclassified one `◆` in `mut`; the same three in the kanban card marker, the gantt cells and label, the band rule facts, the presentation field row, the agenda row, the people view's rows and the two notices (`:2133`, `:2172` — the slip notice at `:2433` stays as it is); a classed milestone's glyph is its class's shape in every one of those frames; the site-enumeration test lists every site of the statement above and fails when a milestone mark is drawn outside the seat.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** the classification reads the same in every frame; no view drifts.
  - **Shipped surface:** every view (`1`-`8`, `A`, the presentation) and the milestone/done notices.
  - **Acceptance test(s):** AT-2603 — realised by ONE node, `tests/test_milestone_marks.py::test_AT_2603_the_state_shows_in_text` (NEW — created in Phase 3, provisional per V-5); the threshold's other clauses are TC-2604 arms through the same surface.
  - **Boundary catalog (QC-3):** ☑ boundary (due today: not late, no chip; a milestone with no due draws nothing in the gantt cells) ☑ empty (no classes: every milestone draws unclassified — `◆` in `mut`, its state in text; an unclassified milestone loses its red mark, MM-D1's accepted cost) ☑ invalid (an unknown id: unclassified, never an error) ☑ error (none — a seat is pure)
  - **Negative control:** on `base_ref` the seat does not exist (`AttributeError: … no attribute 'milestone_mark'` — `evidence/red-p1.txt`, executed); the enumeration test goes RED when a site encodes the mark on its own (minted with the node at P3, C-40).

### HLR-2605 — The editor's class Select (variant A)
- **Traceability:** US-2603
- **Ledger:** LED-2026-10-24-batch-01.5, LED-2026-10-24-batch-01.34
- **Statement:** While the task editor is open, the system shall offer the class Select of variant A: a `Select` mounted in `#task-chips-what` directly after `#f-milestone` (`modals.py:501`, `:513`; the round's `EditorSelect`, proto.py:560-577), its options `none` and every class of the directory — each option its shape, name and colour as explicit-style `Text` pieces — the task's current class selected; `alt+m` shall focus the Select and shall be listed in `TASK_KEYS` (`modals.py:378`) beside the field; choosing `none` shall save the task with no `mark` (the field is written only when set); with an empty directory (the app always loads one, possibly empty) the editor shall draw no Select — a change from before.
- **Rationale (informative):** The verdict's item 2 A (recommended, unmarked): the class sits in the chip row beside `milestone`, like project/phase/priority; MM-D8's `alt+m` beside the field, and D5's standing standard that the key is shown.
- **Validation:** `test`
- **Executed verification:** `env -u NO_COLOR python -m pytest -q -p no:cacheprovider tests/test_marks_manager.py -k "AT_2601 or TC_2605"`
- **Numeric pass threshold:** AT-2601's editor arm: `e` on a milestone → the Select in the chip row after `milestone`, `alt+m` on the key line; `alt+m`, `down`, `enter` → the task carries the class; `alt+m`, `up` to `none`, `enter`, `alt+s` → the task saved with no `mark`; the tab walk of `tests/test_edit_window.py` unchanged; the Select's options are Text pieces — a class named `[b]x[/b]` printed as typed (C-17).
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** classifying a milestone is `alt+m` and an arrow, in the editor the operator already knows.
  - **Shipped surface:** `taskboard` → `e` / `a`, the chip row.
  - **Acceptance test(s):** AT-2601 (realised by `tests/test_marks_manager.py::test_AT_2601_a_class_is_created_and_survives`, NEW) and AT-2603's editor arms
  - **Boundary catalog (QC-3):** ☑ boundary (the first/last option; a chip row folded narrow at 80×24) ☑ empty (an empty directory: no Select — the app always loads one, possibly empty; a change from before) ☑ invalid (markup-looking class names printed as typed) ☑ error (a save refused by the board lock: said, the editor kept)
  - **Negative control:** on `base_ref` there is no Select and `alt+m` is unbound (`evidence/red-p1.txt` executes the absence class); the focused-gesture RED (`.focus()` in place of `alt+m`) is barred by driving the real key (C-16) and minted at P3.

### HLR-2606 — `#` opens the marks manager
- **Traceability:** US-2603
- **Ledger:** LED-2026-10-24-batch-01.6, LED-2026-10-24-batch-01.35, LED-2026-10-24-batch-01.45, LED-2026-10-24-batch-01.46
- **Statement:** When the operator presses `#` on the main screen or the home, the system shall open the marks manager — a screen listing every class of the directory, its frame a pure render `views.render_marks(directory, sel, w, h)` (increment 002, the ARQ's A-1 fold), one row per class: its shape, name, colour, open/all milestone counts, and its hidden state dimmed; `n` shall open the class form — `modals.MarkForm` with the name field, the shape row (`SHAPES` = `▲ ■ ⬢ ★ ⬟ ▼ ✦ ⚑`, proto.py:85, over the round's `ShapeRow` — NO `◆` choice: the unclassified glyph is not a class shape and a saved class can never carry it, LED .45; `◆` lives in the editor Select's `none` option and the manager's `◆ (no class)` row — the code-review F1 fold, LED .46) and the colour row — and a saved form shall add the class to the directory (HLR-2601) and show how the gantt draws it in each state; `e` on a class shall open the same form on it, its id kept (HLR-2601); `space` shall toggle the class's `hidden` flag, persisted in `marks.json` like any other write and the board refreshed; the manager and its form shall obey the modal-keys law — every button a direct key it shows (`y`/`n` in confirmations, `alt+<letter>` beside fields) — as the inventory of `tests/test_modal_keys.py` reads them; `#` shall close it too; the manager shall be listed by `?` and the palette; class deletion shall not be offered.
- **Rationale (informative):** MM-D8 (`#` in the main keymap; the modal law; `tests/test_modal_keys.py` covers the manager and its form), MM-D5 (the shape set; `●` excluded — the gantt's progress dot; wide/ambiguous glyphs excluded), MM-D6's storage side (`space` toggles `hidden`, persisted), and D-4 (the manager's frame pure in `views`, the people view's pattern, so increment 003 keeps 4 source files).
- **Validation:** `test`
- **Executed verification:** `env -u NO_COLOR python -m pytest -q -p no:cacheprovider tests/test_marks_manager.py tests/test_modal_keys.py`
- **Numeric pass threshold:** AT-2601's manager arm: `#` → the manager over the main screen at 118×30 and 80×24, every class listed with its shape and colour, the key row naming `↑↓ move   ␣ hide/show   n new   e edit   esc close`; `n` → the form with the name focused, the shape row and the colour row, a live preview of the mark open/late/reached; a name, `alt+h`, `right`, `alt+c`, `left`, `alt+s` → the class in `marks.json` with the chosen shape and colour; `e` → the form on the class, the id kept after `alt+s`; `space` on a class → its row dimmed, `marks.json` holds `hidden: true`, the gantt refreshed; the law's inventory lists the manager and the form. AT-2604: every button of both reached by its shown key.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** the classes are managed in one window — added, edited, hidden — with two keys each and the key line always naming them.
  - **Shipped surface:** `taskboard` → `#`.
  - **Acceptance test(s):** AT-2601 (realised by `tests/test_marks_manager.py::test_AT_2601_a_class_is_created_and_survives`, NEW) and AT-2604 — realised by ONE node, `tests/test_modal_keys.py::test_AT_2604_the_marks_manager_and_its_form_obey_the_modal_key_law` (an addition to the existing file, NEW node)
  - **Boundary catalog (QC-3):** ☑ boundary (an empty directory: the manager says so and `n` still works; a class name of 60/61 characters) ☑ empty (no classes) ☑ invalid (markup-looking names printed as typed, in the manager and the form) ☑ error (a refused write: `The marks directory was not saved: <reason>`, the form kept)
  - **Negative control:** on `base_ref` `#` is unbound and no manager exists (`evidence/red-p1.txt` — executed); the law's RED side (a button without a direct key) is minted with the inventory addition at P3 (C-40).

### HLR-2607 — The legend strip names the drawn classes
- **Traceability:** US-2604
- **Ledger:** LED-2026-10-24-batch-01.7, LED-2026-10-24-batch-01.31
- **Statement:** The system shall draw a legend strip under the gantt's ruler and in the presentation with its exports (`render_present`, `views.py:6622`, and the export writer), naming only the classes drawn in the frame — each its shape, name and colour — then how many classes are hidden (`N hidden`); when no classed milestone is in view the strip shall draw nothing; the `?` help shall name the classes too; the `?` help, the view's details line and the README shall say what a class mark is.
- **Rationale (informative):** MM-D7 (verdict 3 B): the classification reads in the frame, only what is drawn, none when none is in view; the hidden count keeps the toggle honest.
- **Validation:** `test`
- **Executed verification:** `env -u NO_COLOR python -m pytest -q -p no:cacheprovider tests/test_legend.py tests/test_readme.py -k "AT_2605 or TC_2607 or readme"`
- **Numeric pass threshold:** AT-2605's legend arm: the round's boards, the gantt at 118×30 and 80×24 → the strip under the ruler names exactly the classes drawn in the frame, each `shape name` in the class colour, and `1 hidden` after one class is hidden; with every class hidden or no classed milestone in view → no strip row; the presentation's gantt and split views and the exported file carry the same strip; `?` names the classes.
- **Priority:** medium
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** the frame says which classes it shows and how many it hides.
  - **Shipped surface:** `taskboard` → `3` (gantt), `R` (presentation) and its export; `?`.
  - **Acceptance test(s):** AT-2605 — realised by ONE node, `tests/test_legend.py::test_AT_2605_hide_and_the_legend` (an addition to the existing file, NEW node)
  - **Boundary catalog (QC-3):** ☑ boundary (80×24: the strip cut, names from the right) ☑ empty (no classed milestone in view: no strip) ☑ invalid (markup-looking class names printed as typed) ☑ error (none — a render is pure)
  - **Negative control:** on `base_ref` there is no strip (`grep: 0` for `legend_strip` — `evidence/red-p1.txt`, executed); the RED side (the strip listing a class not drawn) is minted with the node at P3 (C-40).

### HLR-2608 — Hide and search
- **Traceability:** US-2604
- **Ledger:** LED-2026-10-24-batch-01.8
- **Statement:** When a class's `hidden` flag is set, the system shall leave that class's milestones out of the gantt and the presentation — all three views and their exports (`views._hide`/`present_tasks_m` of the round, proto.py:294/:367, wrapping `views.present_tasks`, `views.py:6179`, consumed by `app.py:390` and the export writer); the legend strip shall say how many classes are hidden; when the operator types `/#cls` in the filter, the system shall keep exactly the tasks whose milestone bears that class and the bar shall name the class (`views.matches_m`/`filter_bar_m`, proto.py:505/:512); a `#cls` query naming no class keeps no task; a text query filters exactly as before.
- **Rationale (informative):** MM-D6 (verdict 4 B): the hide toggle set in `#`, its effect everywhere the marks appear, the count in the legend; the round's cheap extra — `/#pay` filters like anything else.
- **Validation:** `test`
- **Executed verification:** `env -u NO_COLOR python -m pytest -q -p no:cacheprovider tests/test_legend.py tests/test_milestone_marks.py -k "AT_2605 or AT_2606"`
- **Numeric pass threshold:** AT-2605: after `space` on a class in `#`, that class's milestones are gone from the gantt (cells, title markers, band facts) and from the presentation's three views and their exports, at 118×30 and 80×24; the strip names the drawn classes and `1 hidden`; unhitting `space` brings them back. AT-2606: `/`, `#pay`, `enter` in the kanban and the gantt → only that class's milestones, the bar `/ ■ Payment  milestones of this class only` with the tally; `/#zzz` keeps nothing and names nothing.
- **Priority:** medium
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** one toggle clears a class from every frame; the filter finds a class's milestones exactly.
  - **Shipped surface:** `taskboard` → `#` (`space`), `/` (`/#pay`); the presentation's export file.
  - **Acceptance test(s):** AT-2605 (realised by `tests/test_legend.py::test_AT_2605_hide_and_the_legend`, NEW node) and AT-2606 — realised by ONE node, `tests/test_milestone_marks.py::test_AT_2606_hash_pay_filters_to_that_class` (NEW — created in Phase 3, provisional per V-5)
  - **Boundary catalog (QC-3):** ☑ boundary (a partial name `#pa` resolves like the round's `find_class`; a case mismatch, per the round's lower-case match) ☑ empty (`/#zzz`: no task, no crash) ☑ invalid (a text query starting `#` that names no class keeps nothing, nothing invented) ☑ error (none — a filter is pure)
  - **Negative control:** on `base_ref` `/#pay` filters as plain text and hides nothing (`evidence/red-p1.txt` executes the absence of the wrappers); the RED side (a hidden class still drawn in one export) is minted with the node at P3 (C-40).

---

## 4. Low-level requirements (LLR)

> Each LLR decomposes an HLR into a verifiable property at the implementation level.
> Same regime: EARS syntax owed in `full`, recommended in `core`. ID format: `LLR-<HLR>.<M>`.
> Symbols flagged `NEW — created in Phase 3` are minted by the increment named; every other symbol is cited `file:line` as it holds on this tree (verified 2026-10-24, premise P-2's tree).

### LLR-2601.1 — `marks.Directory.load`
- **Traceability:** HLR-2601
- **Ledger:** LED-2026-10-24-batch-01.9, LED-2026-10-24-batch-01.29, LED-2026-10-24-batch-01.40
- **Statement:** `taskboard/marks.py` (NEW — created in Phase 3, increment 001) shall provide `Mark(id, name, shape, colour, hidden=False)`, `MARKS_NAME = "marks.json"`, `SHAPES` (the eight glyphs of `proto.py:85` plus `◆` — `◆` is not a member of `SHAPES`; it is the unclassified mark's glyph), `COLOURS` (the app's defined colour set, NEW — created in Phase 3, mirroring `SHAPES`), and `Directory(path, marks=None, load_report=None)` holding `marks: dict[str, Mark]` (one live dict, cleared and refilled in place); `Directory.load(path)` shall never raise: missing → empty; a failed read or an unparseable file → empty with `load_report = {"unreadable": True, "backup": <boards.keep_aside's copy or None>}` (the `people.Directory.load` pattern, `people.py:119`-`:134`); an empty or blank file → empty, no report; each entry cleaned with `models.clean_strings` and flattened to one line as `people._clean` does it (`people.py:60`-`:64`: every whitespace run — newlines and tabs included — becomes a single space), its name capped at 60, skipped unless its `id` fully matches the slug pattern `people.handle_for` produces, is not repeated, has a name, its `shape` is in `SHAPES`, its `colour` is in `COLOURS`, and every field is of its expected type (a non-string name, shape or colour an entry skipped); `hidden` shall be coerced to `bool`; it shall provide `find(q)` — prefix only, lower case, mirroring the round's `find_class` (`proto.py:500`-`:503`) — as the manager and the search use it.
- **Validation:** `test (unit)`
- **Executed verification:** `env -u NO_COLOR python -m pytest -q -p no:cacheprovider tests/test_marks_directory.py -k TC_2601`
- **Numeric pass threshold:** TC-2601: a missing file → empty, no file written; the mixed file (one good entry, one repeated id, one no-name, one bad shape, one bad colour, one non-string name, a name of 61 characters, a name with an embedded newline) → only the good entries, the long name 60, the newline name one line; each of `{not json`, `[]`, `{"marks": {}}`, `\xff\xfe` → empty, `unreadable`, the backup's bytes equal the file's, the file unchanged, the earlier corrupt copy kept; an empty or blank file → no notice, no copy; a name carrying control bytes/ANSI (`\x1b[31m`) loads without error and renders with no style leak (control bytes stripped at load).
- **Negative control:** TC-2601 goes RED when a repeated id is kept, the cap is dropped, or the unreadable file is not copied aside (increment 001's mutation battery, executed at its gate — C-40).
- **Boundary catalog:** ☑ boundary (the 60-character cap) ☑ empty (no file; a blank file) ☑ invalid (bad entries, bad bytes) ☑ error (none — a load never raises)

### LLR-2601.2 — `Directory.add`, `edit`, `set_hidden`, `_commit`
- **Traceability:** HLR-2601
- **Ledger:** LED-2026-10-24-batch-01.10
- **Statement:** `Directory.add(name, shape, colour)`, `Directory.edit(id, name, shape, colour)` and `Directory.set_hidden(id, hidden)` shall clean their fields as `load` does, raise `ValueError` for a name with nothing left, and write through `_commit(change)`: under `boards.file_lock(self.path)` (`people.py:187`), read the file as it holds now — a failed read raises; an unparseable file is kept aside first and, when it cannot be copied aside, never written over (the in-memory classes the base) — apply `change`, then `models.write_atomic` `{"version": 1, "marks": [...]}` with `ensure_ascii=False` (`people.py:198`), and refill `marks` in place; `add` shall derive the id with `people.handle_for(name, taken)` (`people.py:248`) against the file's ids and the memory's; `edit` shall never change the id; a raised `OSError` leaves memory unchanged.
- **Validation:** `test (unit)`
- **Executed verification:** `env -u NO_COLOR python -m pytest -q -p no:cacheprovider tests/test_marks_directory.py -k TC_2601`
- **Numeric pass threshold:** TC-2601: `add("Payment", "■", "pink")` → `payment`, then `payment2` for a second of the same name; two directories on one file → both classes kept (the two-window arm, AT-2602); `edit` renames and keeps the id, writing back a class the file lost; `set_hidden` flips only `hidden`; the file holds `version` 1, no `.tmp` or `.lock` left; the lock held with `LOCK_WAIT` 0.2 → `OSError` naming `busy`, no file; `write_atomic` failing → memory unchanged; an unparseable file → kept at `.corrupt`, then replaced.
- **Negative control:** TC-2601 goes RED when the write skips the re-read (the second window erases the first's class), when the lock is dropped, or when memory updates before the write (increment 001's battery — executed at its gate).
- **Boundary catalog:** ☑ boundary (the 60-character cap; a duplicate name → `payment2`) ☑ empty (a blank name refused) ☑ invalid (control bytes stripped) ☑ error (the lock; the write; the unkeepable file)

### LLR-2601.3 — the app holds the directory; `Board.marks`
- **Traceability:** HLR-2601
- **Ledger:** LED-2026-10-24-batch-01.11
- **Statement:** `taskboard/models.py` shall give `Board` an attribute `marks` (`{}` by default, set by the app, never saved — the `Board.people` pattern) and `taskboard/app.py` shall load `self.marks = marks.Directory.load(self.registry.path.parent / MARKS_NAME)` in `TaskboardApp.__init__` (the `people` load's pattern, `app.py:1102`), set `self.board.marks = self.marks.marks` beside `self.board.people = self.people.people` in `_label_board` (`app.py:1208`, so at mount and every switch), carry it in `after_move`, and warn once at mount with HLR-2601's notice (`markup=False`, the `app.py:1312`-`:1315` pattern) when the load reported the file unreadable.
- **Validation:** `test (unit)`
- **Executed verification:** `env -u NO_COLOR python -m pytest -q -p no:cacheprovider tests/test_marks_directory.py -k AT_2601`
- **Numeric pass threshold:** as AT-2601; `app.marks.path` is `<home>/.taskboard/marks.json`; `app.board.marks` is `app.marks.marks` before and after a board switch; no board file holds `marks`; with `marks.json` = `{oops` the notice above is shown and `marks.json.corrupt` holds `{oops`.
- **Negative control:** AT-2601 goes RED when `_label_board` does not set `marks` (a switched board draws unclassified) or when `Board._to_dict` writes it (increment 001's battery — executed at its gate).
- **Boundary catalog:** ☐ boundary — none ☑ empty (a directory never written: no `marks.json` at all) ☑ invalid (an unreadable file: the notice, the empty directory) ☑ error (none)

### LLR-2602.1 — `Task.mark` on the model and through the editor
- **Traceability:** HLR-2602
- **Ledger:** LED-2026-10-24-batch-01.12
- **Statement:** `taskboard/models.py` shall give `Task` a field `mark: str | None = None` (a NEW field on the Task record, `models.py:894`-`:943` its from_dict/`_TASK_KEYS` :705-708 neighbourhood): `Task.from_dict` reads it when present; `Board._to_dict` drops it when `None`, in the `show_in_present` pattern (`models.py:1049`-`:1051`), so a board with no marks keeps its bytes; an id the directory does not hold passes through every load and save untouched; `taskboard/modals.py`'s save (`modals.py:789` its task-field assembly) shall carry the Select's value into the saved task only when a class is chosen, and shall keep `mark` when the `milestone` checkbox is unticked.
- **Validation:** `test (unit)`
- **Executed verification:** `env -u NO_COLOR python -m pytest -q -p no:cacheprovider tests/test_marks_directory.py tests/test_milestone_marks.py -k 2602`
- **Numeric pass threshold:** TC-2602: a task dict with `"mark": "payment"` round-trips; a task without the key saves with no `mark` key (the board file byte-identical when nothing changed); a task with an unknown id round-trips the id byte-for-byte; untick `milestone`, save → `mark` kept; a board with marks on some tasks → saved → only those tasks gain the key.
- **Negative control:** TC-2602 goes RED when `None` is written into the file or an unknown id is dropped on save (increment 001's battery — executed at its gate).
- **Boundary catalog:** ☑ boundary (a mark set on a non-milestone: kept, drawn nowhere) ☑ empty (no key: nothing written) ☑ invalid (an unknown id: kept) ☑ error (none — serialisation is pure)

### LLR-2602.2 — team sync carries the field, never the directory
- **Traceability:** HLR-2602
- **Ledger:** LED-2026-10-24-batch-01.13, LED-2026-10-24-batch-01.43
- **Statement:** A push shall write a task's record with its `mark` as held — `TeamState.push` serialises `board._to_dict(t)` (`team_sync.py:143`-`:157`), unchanged; a pull shall store a teammate's `mark` as held and the task shall draw in every view without error; no module but `marks.py` shall read or write `marks.json`, and no write to the team folder shall name the directory or a class's name, shape or colour.
- **Validation:** `test (unit)`
- **Executed verification:** `env -u NO_COLOR python -m pytest -q -p no:cacheprovider tests/test_marks_directory.py -k 2607`
- **Numeric pass threshold:** TC-2607: a pushed board file holds the id and none of the directory's names (`grep` the pushed JSON for a class name → 0); a pulled task with an unknown id draws unclassified in the kanban, the gantt and the presentation; `rg "marks\.json" taskboard/team_sync.py` → no hit.
- **Negative control:** TC-2607 goes RED when a push writes a class name or the directory (a mutation adding either to the record — increment 001's battery, executed at its gate).
- **Boundary catalog:** ☐ boundary — none ☐ empty — none ☑ invalid (a teammate's unknown id) ☑ error (none)

### LLR-2603.1 — two windows add a class, both survive
- **Traceability:** HLR-2603
- **Ledger:** LED-2026-10-24-batch-01.14
- **Statement:** Two `Directory` objects on one `marks.json` — the code a second process runs — shall each keep the other's classes: every write re-reads the file under `boards.file_lock` and applies its change to that, so a class the other window added survives this window's add.
- **Validation:** `test (unit)`
- **Executed verification:** `env -u NO_COLOR python -m pytest -q -p no:cacheprovider tests/test_marks_directory.py -k TC_2603`
- **Numeric pass threshold:** TC-2603: directory A adds `payment`, directory B (opened on the same file before A's add) adds `review` → the file holds both, A's live dict gains `review` after its next write, B's gains `payment`; 10 interleaved adds on one file → 10 classes in the file, none lost.
- **Negative control:** TC-2603 goes RED when the write skips the re-read (the second window erases the first's class — the mutation executed in `evidence/mutation-001.txt` at P3).
- **Boundary catalog:** ☑ boundary (10 interleaved adds) ☑ empty (the second window's file appears mid-session) ☑ invalid — none ☑ error (the lock held: the second add refused, said)

### LLR-2603.2 — the unreadable file is kept, never overwritten; the bytes hold
- **Traceability:** HLR-2603
- **Ledger:** LED-2026-10-24-batch-01.15
- **Statement:** An unreadable `marks.json` shall be copied aside by `boards.keep_aside` before any write and never written over when the copy fails; a later unreadable file shall never replace an earlier `marks.json.corrupt`; a board whose tasks carry no `mark` shall keep its bytes through a load and a save; `marks.json` shall start empty — no file exists until the first class is added.
- **Validation:** `test (unit)`
- **Executed verification:** `env -u NO_COLOR python -m pytest -q -p no:cacheprovider tests/test_marks_directory.py -k TC_2603`
- **Numeric pass threshold:** TC-2603: `{oops` → one notice, `.corrupt` holds `{oops`, the file unchanged; a second unreadable file with `keep_aside` already present → the first copy kept; a board file's bytes hashed before and after a no-op load/save → equal; a fresh home has no `marks.json` after `open_app` alone.
- **Negative control:** TC-2603 goes RED when the corrupt copy is overwritten or a no-mark board gains bytes (increment 001's battery — executed at its gate).
- **Boundary catalog:** ☐ boundary — none ☑ empty (no file; nothing written) ☑ invalid (bad bytes kept aside) ☑ error (the copy failing: no write over the file)

### LLR-2604.1 — `views.milestone_mark`, the one seat
- **Traceability:** HLR-2604
- **Ledger:** LED-2026-10-24-batch-01.16, LED-2026-10-24-batch-01.28
- **Statement:** `taskboard/views.py` shall provide `milestone_mark(task, board, today) -> (glyph, style, late_chip)` (NEW — created in Phase 3, increment 002) reading the class from `board.marks` (the app's live directory, `LLR-2601.3`): the class's `shape` as the glyph and its `colour` as the style — an unset or unknown id gives `("◆", "mut")`; when the task is open and its due is past `today`, the date's style is `over` and `late_chip` is `▲Nd` (`N` the days); when `board.is_done(task)`, the glyph is `HOLLOW.get(glyph, glyph)` (the map of proto.py:83) and the chip carries `✓` in `reached`; a non-empty `late_chip` shall imply the milestone's date renders in `over` at every site — one channel out of the seat, no site re-deriving lateness; the existing tone seat `milestone_tone` (`views.py:2523`) is replaced by it at every site.
- **Validation:** `test (unit)`
- **Executed verification:** `env -u NO_COLOR python -m pytest -q -p no:cacheprovider tests/test_milestone_marks.py -k TC_2604`
- **Numeric pass threshold:** TC-2604: the truth table — classed+late → `(shape, colour, "▲3d")`; classed+reached → `(hollow(shape), colour, "✓")`; classed+open → `(shape, colour, "")`; unclassified (no mark / unknown id) → `("◆", "mut", "")`; unclassified+late → `("◆", "mut", "▲3d")` with the date style `over`; no directory (`board.marks` `{}`) → `("◆", "mut", "")` — every cell of HLR-2604's boundary catalog.
- **Negative control:** TC-2604 goes RED when the state moves back into the glyph (a colour = state) or the hollow map is dropped (increment 002's battery — executed at its gate).
- **Boundary catalog:** ☑ boundary (due today: no chip; `N` = 1 → `▲1d`) ☑ empty (no directory) ☑ invalid (an unknown id) ☑ error (none — pure)

### LLR-2604.2 — every site routed through the seat
- **Traceability:** HLR-2604
- **Ledger:** LED-2026-10-24-batch-01.17, LED-2026-10-24-batch-01.27, LED-2026-10-24-batch-01.38
- **Statement:** Every milestone site of HLR-2604 shall take its `(glyph, style, late_chip)` from the seat and none shall encode MM-D1 on its own: the lanes/focus title markers (`views.py:1107`/`:1113`, `:1677`/`:1689`), the bank edge (`:1800`), the kanban/focus field glyph (`:2037`), the gantt's title prefix `_milestone_title` (`:2541`), `gantt_milestone_cells` (`:2545`-`:2576`), the one-date bars (`:2643`, `:2732`), the ruler milestones (`:3035`), the row label (`:3078`), the chain map's label (`:3613`-`:3617`), the band rule facts `band_milestone_facts` (`:5053`-`:5099`) and the fold row (`:5310`), the presentation's field row `_present_task_row` (`:6537`-`:6547`), the agenda's `_agenda_row` (`:7146`, the mark added before the title as the round's `agenda_row_m`, proto.py:206), the people view's `_task_rows` (`:8433`-`:8467`) and `app.py`'s notices when they show a milestone mark (`:2133`, `:2172`); a test shall enumerate these sites and fail when a milestone mark is drawn outside the seat; the exclusions shall stay byte-identical in behaviour: the title glyphs (`:1225`, `:1884`, `:3015`, `:3670`, `:3699`, `:3970`, `:6095`), the project-span due marks (`:2613`, `:3030`, `:3044`, `:6579`, `:6856`), the slip notice at `app.py:2433` (`{pn} +{over}d past ◆` — a project-span due mark, not a milestone seat site; the seat is keyed by task) and the gantt month ruler's lateness (the accepted cost).
- **Validation:** `test (unit)`
- **Executed verification:** `env -u NO_COLOR python -m pytest -q -p no:cacheprovider tests/test_milestone_marks.py -k sites`
- **Numeric pass threshold:** TC-2604: the enumeration test lists every site above (20 sites — one line-ref = one site; the gantt echo folds into the one-date bars at `:2732`) and greps each draw for the seat's call — a NEW milestone site added to `views.py`/`app.py` without the seat fails it; the exclusion list asserts the title glyphs and project due marks do not call the seat.
- **Negative control:** the enumeration test goes RED when any site hard-codes a glyph or tone for a milestone (a site edited back to `c("◆", …)` — increment 002's battery, executed at its gate).
- **Boundary catalog:** ☐ boundary — none ☑ empty (a view with no milestone: nothing to route) ☑ invalid (an unknown id at every site: `◆` in `mut`) ☑ error (none)

### LLR-2605.1 — `TaskModal`'s class Select (variant A)
- **Traceability:** HLR-2605
- **Ledger:** LED-2026-10-24-batch-01.18, LED-2026-10-24-batch-01.33, LED-2026-10-24-batch-01.41
- **Statement:** `taskboard/modals.py`'s `TaskModal` shall compose the class Select of variant A (NEW — created in Phase 3, increment 003): a `Select` mounted in `#task-chips-what` directly after `#f-milestone` (`modals.py:501`, `:513`; the round's mount, proto.py:570), its options `none` and every class of the directory the app passes in — each option a `Text.assemble` of the shape in the class colour and the name in the ink tone, never markup (C-17) — the task's current class selected, and no `+ new class…` option (that is the manager's job, `n`; the Select only picks); `alt+m` (a priority binding, `Binding("alt+m", "mark")`, the round's proto.py:562) shall focus the Select and open it; `TASK_KEYS` (`modals.py:378`) shall gain `("alt+m", "mark")` after the milestone key; the saved task carries the chosen class id, or no `mark` when `none`; with an empty directory (the app always loads one) the modal composes no Select.
- **Validation:** `test (unit)`
- **Executed verification:** `env -u NO_COLOR python -m pytest -q -p no:cacheprovider tests/test_marks_manager.py -k TC_2605`
- **Numeric pass threshold:** TC-2605: `e` on a classed milestone → the Select after `milestone` with the class selected; `alt+m` → the Select focused and open, the key on the key line; `down`, `enter` → the next class; `up` to `none`, `enter`, `alt+s` → no `mark` key in the saved task; a class named `[b]x[/b]` shown as typed in the overlay; an empty directory → no Select, the tab walk of `tests/test_edit_window.py` green.
- **Negative control:** TC-2605 goes RED when `alt+m` acts while the editor is closed or the Select writes markup (increment 003's battery — executed at its gate).
- **Boundary catalog:** ☑ boundary (the overlay at 80×24, wholly inside the screen) ☑ empty (an empty directory; `none` chosen) ☑ invalid (markup-looking names) ☑ error (a save refused: said, the editor kept)

### LLR-2606.1 — keymap `#` and `app.MarksManager`
- **Traceability:** HLR-2606
- **Ledger:** LED-2026-10-24-batch-01.19
- **Statement:** `taskboard/keymap.py` shall declare `Key("number_sign", "#", "marks_manager", "Milestone classes", group="misc", bar=False)` (NEW — created in Phase 3, increment 003; `#` verified free, premise P-4) in `KEYMAP` (`keymap.py:55`), global and off the bar like `@`; `taskboard/app.py` shall provide `MarksManager(Screen)` (NEW — created in Phase 3, increment 003; the `PeopleDirectory` pattern) whose frame is `views.render_marks` (LLR-2606.3) with priority bindings `escape,number_sign` (close), `up,k`/`down,j` (move), `space` (hide), `n` (new), `e` (edit); `TaskboardApp.action_marks_manager` shall push it; `check_action` shall let `marks_manager` act as it lets the other global keys and refuse every seat action but `quit` while the manager is on the stack; `?` and the palette shall list it.
- **Validation:** `test (unit)`
- **Executed verification:** `env -u NO_COLOR python -m pytest -q -p no:cacheprovider tests/test_marks_manager.py -k "AT_2601 or TC_2606"`
- **Numeric pass threshold:** as AT-2601's manager arm; `KEYMAP` holds `#` labelled `Milestone classes` off the bar; `#` from the main screen and the home opens the manager; with the manager open `a`, `d`, `1`, `B`, `4` change nothing; `#` and `esc` close it; `?` lists it.
- **Negative control:** AT-2601 goes RED when the seat keys act behind the manager or `#` acts over a modal (increment 003's battery — executed at its gate).
- **Boundary catalog:** ☐ boundary — none ☑ empty (an empty directory: the frame says so, `n` still works) ☑ invalid (markup-looking names in the frame) ☑ error (a refused write: said)

### LLR-2606.2 — `modals.MarkForm` and the modal law
- **Traceability:** HLR-2606
- **Ledger:** LED-2026-10-24-batch-01.20
- **Statement:** `taskboard/modals.py` shall provide `MarkForm(cls_id=None)` (NEW — created in Phase 3, increment 003; `ModalScreen[str | None]`, `ButtonKeysMixin` at `modals.py:322`): the name `Input`, the shape row over `SHAPES` (the round's `ShapeRow`, proto.py:778-807 — no `◆`, the F1 fold LED .46: a saved class must survive the load validation, which `◆` would not) and the colour row, a live preview of the mark open/late/reached under the encoding, `Save`/`Cancel` buttons and the key line `alt+n name   alt+c colour   alt+h shape   alt+s save   esc cancel`; `alt+n`/`alt+c`/`alt+h` focus their rows, `alt+s` saves, `esc` cancels; a save calls `Directory.add`/`edit` (LLR-2601.2) and a failed write says `The marks directory was not saved: <reason>`, the form kept; the form and the manager shall be listed in `tests/test_modal_keys.py`'s inventory, every button reached by its shown key.
- **Validation:** `test (unit)`
- **Executed verification:** `env -u NO_COLOR python -m pytest -q -p no:cacheprovider tests/test_marks_manager.py tests/test_modal_keys.py -k "TC_2606 or AT_2604"`
- **Numeric pass threshold:** as AT-2601's form arm and AT-2604: the inventory lists `MarksManager` and `MarkForm`; each of the form's buttons pressed by its shown key; the key line painted holds `alt+s` and `esc cancel`.
- **Negative control:** AT-2604 goes RED when the form loses `alt+s` or a button lacks a direct key (increment 003's battery — executed at its gate).
- **Boundary catalog:** ☐ boundary — none ☑ empty (a blank name: refused with `A class needs a name.`, the form kept) ☑ invalid (markup-looking names in the preview) ☑ error (the directory write refused: said)

### LLR-2606.3 — `space` persists the toggle; `views.render_marks` the pure frame
- **Traceability:** HLR-2606
- **Ledger:** LED-2026-10-24-batch-01.21
- **Statement:** The manager's `space` shall call `Directory.set_hidden(id, hidden)` (LLR-2601.2) — persisted in `marks.json` like any other write — then redraw the frame and refresh the board beneath; `taskboard/views.py` shall provide `render_marks(directory, sel, w, h) -> Text` (NEW — created in Phase 3, increment 002; the ARQ's A-1 fold, `docs/ARCHITECTURE.md`:133): one row per class — its shape in its colour, its name, the open/all milestone counts, `hidden` dimmed — the chosen row marked `▶` and shaded, a `◆ (no class)` row for the plain milestone, every row exactly `w` cells of explicit-style `Text` pieces, the people view's pattern (`render_people_directory`, `views.py:8511`).
- **Validation:** `test (unit)`
- **Executed verification:** `env -u NO_COLOR python -m pytest -q -p no:cacheprovider tests/test_marks_manager.py -k TC_2606`
- **Numeric pass threshold:** TC-2606: `render_marks` on the round's directory at widths 76, 60, 40 → every row exactly `w` cells, the chosen row shaded, a hidden class dimmed with `hidden: gantt + present` beside it (per the round's frame, proto.py:882-905); `space` in the manager → `marks.json` holds `hidden: true`, the frame redrawn, the board refreshed; at 40 cells the counts drop before the names.
- **Negative control:** TC-2606 goes RED when the toggle is not persisted or the frame row exceeds `w` cells (increment 002/003's battery — executed at its gate).
- **Boundary catalog:** ☑ boundary (widths 76/60/40) ☑ empty (an empty directory: one `No classes yet.` line and the hint) ☑ invalid (markup-looking names as typed) ☑ error (a refused `set_hidden`: said, the frame unchanged)

### LLR-2607.1 — `views.legend_strip` / `legend_strip_project`
- **Traceability:** HLR-2607
- **Ledger:** LED-2026-10-24-batch-01.22
- **Statement:** `taskboard/views.py` shall provide `legend_strip(board, w)` and `legend_strip_project(board, proj, w)` (NEW — created in Phase 3, increment 004; the round's, proto.py:246/:353) naming only the classes drawn in the frame — each its shape in its colour and its name — then `N hidden` counting the hidden classes; the gantt's frame shall draw the strip under the ruler (`_gantt_frame`, `views.py:2973`, an extra row the frame packs in, the round's `gantt_frame_m`, proto.py:267-291) and `render_present` (`views.py:6622`) shall draw it with its export, per project in the all-boards presentation; when no classed milestone is in view the strip shall draw nothing.
- **Validation:** `test (unit)`
- **Executed verification:** `env -u NO_COLOR python -m pytest -q -p no:cacheprovider tests/test_legend.py -k TC_2607`
- **Numeric pass threshold:** TC-2607: the gantt's strip lists exactly the classes of the milestones in the frame; a class hidden → `1 hidden`; the presentation's gantt and split views and the exported file carry the same strip; a frame with no classed milestone has no strip row; at 80 cells the strip is cut with names from the right.
- **Negative control:** TC-2607 goes RED when the strip names a class not drawn or omits the hidden count (increment 004's battery — executed at its gate).
- **Boundary catalog:** ☑ boundary (80 columns) ☑ empty (no classed milestone in view) ☑ invalid (markup-looking names) ☑ error (none — pure)

### LLR-2607.2 — the `?` help, the details line and the README name the classes
- **Traceability:** HLR-2607
- **Ledger:** LED-2026-10-24-batch-01.23, LED-2026-10-24-batch-01.32
- **Statement:** The `?` help shall name the classes: `help_usage`/`legend_entries` (`views.py:7866`/`:8027`) gain the manager and the class entries; the gantt's details line shall say what a class mark is (the seat of the details line: `assumed — verify in Phase 3` — increment 004 names it, and its gate shall confirm `_gantt_legend` (`views.py:2929`) is that operator-visible line; if it is not, the gate names the true seat and a ledger entry records the amendment); `README.md` shall document the directory, the seat's encoding, the manager's keys and the `/#cls` filter.
- **Validation:** `test (unit)`
- **Executed verification:** `env -u NO_COLOR python -m pytest -q -p no:cacheprovider tests/test_legend.py tests/test_readme.py -k "help or readme or TC_2607"`
- **Numeric pass threshold:** TC-2607: `?` on the main screen and in the gantt lists `# Milestone classes`; `?` names the `/#cls` filter; the gantt's legend (`_gantt_legend`, `views.py:2929` — the details-line seat named in the statement, confirmed at the increment-004 gate) names `◆ milestone` beside the class entries; `tests/test_readme.py` green with the new paragraphs.
- **Negative control:** TC-2607 goes RED when `?` omits the manager (increment 004's battery — executed at its gate).
- **Boundary catalog:** ☐ boundary — none ☑ empty (no classes: `?` names the manager only) ☑ invalid — none ☑ error (none)

### LLR-2608.1 — `_hide` / `present_tasks_m` drop hidden classes everywhere
- **Traceability:** HLR-2608
- **Ledger:** LED-2026-10-24-batch-01.24
- **Statement:** `taskboard/views.py` shall provide `_hide(board)` and `present_tasks_m(board, project_id)` (NEW — created in Phase 3, increment 004; the round's, proto.py:294/:367): `_hide` a shallow board proxy whose task list drops the milestones of hidden classes, applied to the gantt's frame (`_gantt_frame`, `views.py:2973`); `present_tasks_m` wrapping `views.present_tasks` (`views.py:6179`) — consumed by the presentation screen (`app.py:390`) and the export writer — so hidden-classed milestones leave all three presentation views and their exports; the legend strip keeps the hidden count (LLR-2607.1).
- **Validation:** `test (unit)`
- **Executed verification:** `env -u NO_COLOR python -m pytest -q -p no:cacheprovider tests/test_legend.py -k TC_2608`
- **Numeric pass threshold:** TC-2608: with one class hidden, its milestones are absent from the gantt's cells, title markers, band facts and fold counts; from the presentation's gantt view, split view and all-boards view at 118×30 and 80×24; from the exported file's bytes; the board object itself is untouched (a save writes what it held).
- **Negative control:** TC-2608 goes RED when a hidden class still draws in one export (increment 004's battery — executed at its gate).
- **Boundary catalog:** ☐ boundary — none ☑ empty (no hidden classes: the wrappers are the identity) ☑ invalid — none ☑ error (none — pure wrappers)

### LLR-2608.2 — `matches_m` / `filter_bar_m`, the `/#cls` query
- **Traceability:** HLR-2608
- **Ledger:** LED-2026-10-24-batch-01.25
- **Statement:** `taskboard/views.py` shall provide `matches_m(task, board, q)` and `filter_bar_m(query, hits, total, w, people=None)` (NEW — created in Phase 3, increment 004; the round's, proto.py:505/:512) wired into the filter seats `matches` (`views.py:3720`) and `filter_bar` (`views.py:3751`) and the filtered render (`render_view`, `views.py:7385`): a query starting `#` keeps exactly the open or done milestones whose `mark` is the class `find_class` resolves for the rest of the query (the directory's `find`, lower case, a prefix of the name — the round's rule, proto.py:500-503), returning the `"class"` kind; the bar reads `/ <shape> <Name>  milestones of this class only` with the tally and `esc clears`; a `#cls` naming no class keeps no task; a text query filters exactly as before.
- **Validation:** `test (unit)`
- **Executed verification:** `env -u NO_COLOR python -m pytest -q -p no:cacheprovider tests/test_milestone_marks.py -k "AT_2606 or TC_2608"`
- **Numeric pass threshold:** TC-2608: `/#pay` in the kanban and the gantt → only that class's milestones, the bar as above with `n/total tasks`; `/#PaY` matches like `/#pay` (lower case); `/#zzz` keeps nothing, the bar names nothing; `/pay` (no `#`) filters as text, unchanged; the overlay lights no text for a class query.
- **Negative control:** TC-2608 goes RED when the class rule falls through to the text rules or the bar omits the class (increment 004's battery — executed at its gate).
- **Boundary catalog:** ☑ boundary (a partial name `#pa`; case) ☑ empty (`/#zzz`) ☑ invalid (a text query that merely starts with `#`) ☑ error (none — pure)

### Information Flow Contract (IFC) — C-54

> Part A in every batch; Part B when the system's boundary has components a consumer can address independently. The block syntax, its fields and the rules that read them are in `templates/ifc-template.md`, which ships with the flow and is not copied into this batch.

- **Part A — flows:**

```
FLOW: the marks directory, from marks.json to every board the app opens
  SOURCE : taskboard start; n / e / space in the # manager
  NODES  :
    - fn    : marks.Directory.load
      owner : LLR-2601.1
    - fn    : marks.Directory.add, edit, set_hidden, _commit
      owner : LLR-2601.2
    - fn    : app.TaskboardApp.__init__, _label_board, after_move, the mount notice; models.Board.marks
      owner : LLR-2601.3
  SINK   : ~/.taskboard/marks.json; board.marks (memory only); the unreadable notice
```

```
FLOW: a task's mark, from the editor and the team folder to every view and notice
  SOURCE : the editor's class Select (alt+m); a teammate's pulled board file
  NODES  :
    - fn    : models.Task.mark, Board._to_dict; modals.TaskModal (the Select, the milestone checkbox)
      owner : LLR-2602.1
    - fn    : team_sync.TeamState.push, pull (unchanged)
      owner : LLR-2602.2
    - fn    : views.milestone_mark
      owner : LLR-2604.1
    - fn    : every milestone site of section 3 (views.py and app.py's notices)
      owner : LLR-2604.2
  SINK   : board.json (the mark, only when set); the team folder's record; every view, export and notice
```

```
FLOW: the hidden flag, from the # manager to the gantt and the presentation
  SOURCE : space in the # manager (MarksManager)
  NODES  :
    - fn    : marks.Directory.set_hidden (persisted in marks.json)
      owner : LLR-2601.2
    - fn    : views._hide, present_tasks_m
      owner : LLR-2608.1
    - fn    : views.legend_strip, legend_strip_project (the hidden count)
      owner : LLR-2607.1
  SINK   : the gantt frame; the presentation's three views and their exports; the legend's "N hidden"
```

```
FLOW: a class query, from / to the filtered view
  SOURCE : / in the kanban or gantt, then #cls
  NODES  :
    - fn    : views.matches_m, filter_bar_m (wired into matches, filter_bar, render_view)
      owner : LLR-2608.2
  SINK   : the filtered kanban / gantt and its bar
```

- **Part B — boundary decomposition:** `no — every flow is the app's own, addressed through its keys and its files`

---

## 5. Validation strategy

### 5.1 Methods

> **Two layers** (per the Two-layer validation rule). Every batch declares BOTH:
> - **Layer A — white-box / functional (`TC-NNN`):** validates the HLR/LLR mechanism (the HOW). Methods: `test`, `inspection`, `analysis`.
> - **Layer B — black-box / behavioral acceptance (`AT-NNN`):** validates the user story's outcome through the shipped surface (the WHAT). Method: `acceptance`.

Layer 0: the directory's reads and writes, the slug, `Task.mark`'s round-trip, the seat's truth table, `render_marks`, the strips, the hide wrappers, the filter (TC-2601..TC-2608). Layer A: TC-2601..TC-2608 at the function and screen level. Layer B: AT-2601..AT-2607 drive the real app headless (`run_test`, keys — the real mechanism, never a proxy per C-16) built by the shipped `open_app` on the round's synthetic boards and classes (`tests/milestone_marks_fixture.py`, NEW) under the seam home, reading the screen's text, the notices and the files; style and colour claims (`over`, `mut`, a class colour) are asserted on Textual's styled-segment export from the headless driver — the machine oracle for tone assertions; the commissioned full-colour `m01-` Windows Terminal captures are the visual confirmation; "another window" is a second `Directory` on the same file — the code a second process runs. Real-app captures at 118×30 and 80×24 of each shipped item go to `evidence/captures/` (Windows Terminal PNGs, the commission's capture method: unique `m01-` titles, closed by title, never another window, full colour). **Executed-verification file paths, `-k` selectors and node ids are all provisional-until-Phase-3; the implemented names are reconciled from the real tree at Phase 4 (V-5). `V53` NOTICEs the not-yet-existing nodes until Phase 3 mints them — expected.** Every `Executed verification` command in this contract carries the `env -u NO_COLOR ` prefix — the commission's rule («Run `env -u NO_COLOR` for every pytest»): without it the colour tests fail.

### 5.2 Batch acceptance criteria
- every LLR has a passing TC; every story a passing AT through its surface;
- every new assertion RED on `base_ref` (pre-state probes in `evidence/red-p1.txt`) or by a recorded mutation; mutants KILLED on the new logic;
- the full suite in three sequential chunks: 0 failures; transcripts under the batch's evidence; 3152 + the new nodes;
- no test reads or writes the real home; no test leaves a `marks.json.lock`.

---

## 6. Appendices (optional)

### 6.1 Extended glossary
### 6.2 Relevant design decisions
See `PLAN.md` §Key decisions (D-1..D-4) and the commission's MM-D1..MM-D8; `docs/ARCHITECTURE.md` (amended by the ARQ: `taskboard/marks.py`, `marks.json`, `Task.mark`, `Board.marks`, `views.milestone_mark`, `views.render_marks`, the legend strips, the hide wrappers, the class filter, `app.MarksManager`, the editor's Select and `MarkForm`, the `#` key — `docs/ARCHITECTURE.md`:41,66-70,128-134,175).
### 6.3 Open risks
- **Security questions (the P1 scan):** `devflow-scan-spec.py` over this document, 2026-10-24: exit 1 — the scanner's security-required verdict (its controls all passed; four pattern flags fired), `security_required: true`, flags `session`, `payment`, `form`, `escape` (`evidence/scan-p1.txt`), answered here. `session` — «mid-session» in LLR-2603.1's boundary row: two app processes sharing one home folder, no server session, token or credential exists or is introduced (the lock file's random token is the registry's reviewed pattern, unchanged). `payment` — the synthetic example class of the round's fixtures (`Payment`/`payment`, the `▲`/`■` test data), not a payment surface: this batch adds no money, checkout or billing anything. `form` — `MarkForm`'s fields (the class name, the shape and colour rows): user-supplied text stored as data in `marks.json`, never executed or parsed as markup — flattened to one line as `people._clean` does it (`people.py:60`-`:64`: every whitespace run, newlines and tabs included, becomes a single space) and capped at 60; the one-line flattening is the form's and the load's own step, because `clean_strings`/`strip_controls` keeps tab and newline by design (`models.py:534`-`:535`). `escape` — the `esc` key closing the manager and its form (priority bindings), and, for markup, every class string drawn as an explicit-style `Text` piece — there is no markup-interpreted render of any field read from `marks.json` or a board file. **C6 (new input surface):** `marks.json` is read at every start and by another window — it is read without ever raising, an unreadable file copied aside (`keep_aside`), and none of its fields is ever markup-interpreted: every class string — the name above all — is rendered as an explicit-style `Text` piece (the manager's frame `render_marks`, the legend strips, the editor Select's options, the filter bar), and the notices are `markup=False`; hostile-payload TC arms (a class name of `[b]x[/b]`, bracket and ANSI bytes) are owed in Phase 3 — rendered literally, no parse error, no style leak. **C8 (new screens draw loaded text):** the manager and its form draw the directory's user-supplied text — every piece explicit-style (C-17); the form's fields are cleaned of control bytes and line breaks, capped, stored as data. The security-reviewer reviews `marks.py` at increment 001's gate (the commission). `marks.json` holds only the operator's own class labels — no third-party personal data (D-2); no network, credential or permission change. The class id is a slug of the name and travels on team sync with the task by design (MM-D3); its sensitivity equals the synced task titles, and no personal data is involved (D-2).
- **The `▲` ambiguity** (MM-D5): a class shaped `▲` sits beside the `▲Nd` late chip and the `▲N ◆` fold row — accepted, logged to `BACKLOG.md` at close.
- **MM-D1's accepted costs:** the gantt month ruler shows no lateness; an unclassified milestone loses its red mark; a class colour can resemble a project colour.
- **A teammate's class id is unknown here** — it renders unclassified and is kept (AT-2607); a teammate without my directory sees the id render plain.
- **Another window's new class** shows here after a restart or this window's next write: accepted (the `people` batch's A-7 ruling, same mechanism).
- **Class deletion is not offered** — a class can only be hidden; the directory grows monotonically.
### 6.4 Phase-1 reconciliation log — moved to the ledger (§7)

### 6.5 Requirement amendments — moved to the ledger (§7)

---

## 7. The ledger — authored as a SEPARATE FILE

The fence below is the ledger's seed: `devflow-init.py` writes it to `01-requirements-ledger.md`. The shape of an entry is in the field guide.

```markdown
# Requirements ledger — taskboard — Batch 2026-10-24-batch-01

> Append-only. Entries are added in chronological order and never rewritten. The live
> contract is `01-requirements.md`; this file records how it came to say what it says.
> Every entry names the requirement it amends; every requirement names its entries. `V26`
> compares the two sets of pairs both ways.

_No entries yet. The first amendment to the live contract writes the first one, in the
shape the field guide's §7 shows (`req-template.part2.md` in the guide directory init prints), and nothing
above this line is ever edited._
```
