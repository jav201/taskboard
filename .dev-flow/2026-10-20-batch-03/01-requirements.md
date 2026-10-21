# Requirements Document — taskboard — Batch 2026-10-20-batch-03

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
The live contract for batch 2026-10-20-batch-03: the nine items of the backlog round (`prototypes/backlog_round/backlog-round.html`) as the operator's verdict chose them — an all-boards agenda, four presentation items, a direct key for every modal button, the board's name on the start-up modals, a notice when a board is open twice, and a way to open a board without registering it.

### 1.2 Scope
In: `app` — `taskboard/app.py` (the agenda screen and `A`, the presentation's hint chip, `?`, `K`/`J` and export, the presence lifecycle and its notice, an unlisted board's start), `taskboard/__main__.py` (`--open`); `views` — `taskboard/views.py` (the agenda's pure render, the clean view-3 export, `board_chip_text`); `modals` — `taskboard/modals.py` (every modal's button keys and key lines, `ConfirmModal`, the presentation keys window, the start-up modals' chip, the unlisted board's move refusal); `keymap` — `taskboard/keymap.py` (`A` in `KEYMAP`, the presentation's key seat `PRESENT_KEYS`); `models` — `taskboard/boards.py` (the presence markers); `taskboard/taskboard.tcss` (the confirmation's wrap, the editor's key line); the tests, a new `tests/backlog_round_fixture.py` (the round's boards, copied so no test imports a prototype); `README.md`, `docs/ARCHITECTURE.md`, `.dev-flow/BACKLOG.md` (docs). Out: the black window real Windows Terminal shows on opening the `Personal`/`Course` boards (`prototypes/backlog_round/out/png/black/`; investigated separately); the blank screen behind the start-up modals (logged); a lock on plain board saves; the agenda's editing; pushing or merging.

### 1.3 Definitions, acronyms, abbreviations
| Term | Definition |
|------|------------|
| the round | `prototypes/backlog_round/` (commit `36bba10`, cherry-picked as `1fd667b`) and its verdict |
| chip | the open board's name on its colour, as the head rows draw it (`views.board_chip`, batch 2026-10-20-batch-01) |
| the agenda | the all-boards screen behind `A` (item 1, variant C) |
| bucket | one column of the agenda: `LATE` (due before today), then each day from today to Sunday |
| key line | one row that names a modal's keys in the key bar's style: key bold bright, word muted |
| presence marker | a file `~/.taskboard/open/<file hash>-<token>.json` a window keeps while a board is open |
| unlisted board | a board file opened with `--open`: no entry in `boards.json` |

### 1.4 References
- The operator's commission (2026-10-20): «Haz lo del backlog por favor.», and the round's verdict, verbatim: «1 agenda: C · 2 chip: B · 3 help: A · 4 export: limpia · 5 reorder: A · 6 confirm: B · OBJECIÓN: «Esa opción debería ser el estandar para todas las aplicaciones TUI que tenemos. Para tener un acceso directo a los botones. (y cuando hay bloques de entrada de texto usar una combinación específica)» · 7 startup: A · 8 twice: A · 9 register: A · notes: (none)».
- The round's code, the spec of each chosen variant: `prototypes/backlog_round/proto.py` (`AgendaRuler`, `PresentChipHint`, `PresentKeys`/`PresentHelpModal`, `_export`, `PresentReorderKJ`, `ConfirmKeys`, `OfferNamedA`/`IdentityNamedA`, `warn_twice`, `opened_unlisted`); its captures `out/png/*-{C,B,A}*`, `out/export/clean_*`.
- The backlog entries this batch closes: `.dev-flow/BACKLOG.md` lines 144 (a notice that another taskboard is running), 149–153, 167, 170, 173.
- The shipped code: `taskboard/app.py` (`PresentScreen` 190–631, `_hint` 332–385, `action_export` 605–628, `BoardsHome` 638–820, `check_action` 893–910, `on_mount` 919–926, `_label_board` 928–933, `_open_board` 958–978, `switch_board` 993–1039, `_offer_milestones` 1047–1059, `_init_team_mode` 1169–1197, `_tick` 1295), `taskboard/modals.py` (`TaskModal` 362–557, `ProjectModal` 560–640, `ProjectPicker.action_move_board` 771–784, `TemplateEditor` 1064–1108, `MilestoneOffer` 1111–1231, `TeamIdentityPicker` 1465–1505, `ClockModal` 1508–1545, `ConfirmModal` 1548–1571, `TextPrompt` 1574–1610), `taskboard/views.py` (`board_chip` 672–679, `_all_timeline` 6817–6854, `render_present_all` 6879–6901), `taskboard/keymap.py`, `taskboard/boards.py`, `taskboard/__main__.py`.

### 1.5 Document overview
§2 the stories, premises and fork preconditions; §3 ten HLRs; §4 the LLRs and the information-flow contract; §5 the validation strategy; §6 the decisions and open risks.

---

## 2. Overall description

### 2.1 Product perspective
The several-boards batches left the operator's boards readable one at a time, the presentation's keys known only to its hint row, confirmations reachable by `tab`, `enter` alone, the start-up modals silent about their board, two windows on one board unaware of each other, and `--board` as the only way to open a file. This batch ports the round's chosen variants into the app; every chosen variant was already the real `TaskboardApp` with a subclass, so the port moves that subclass's code into the shipped class.

### 2.2 Product functions
1. `A` shows every board's dues for the week, a lane per board and the chosen day's tasks, and `enter` opens a task on its board.
2. The presenter sees the board's name on the hint row; the room and the export never do.
3. `?` inside the presentation lists its keys, generated from the one seat that binds them.
4. The view-3 export carries no cursor and ends at its last row of content.
5. `K`/`J` reorder like `shift+↑/↓`.
6. Every modal button has a direct key, written on the screen: `y`/`n` in a confirmation, `alt+<letter>` beside text fields; a confirmation's message is never cut.
7. The start-up modals name the board they answer for.
8. Opening a board another window holds says so once.
9. `--open PATH` opens a board without adding it to the boards.

### 2.3 User characteristics
The operator alone (`username_subject`), keyboard only, presenting to a room from a terminal, with several boards and sometimes two terminals; Windows Terminal at 118×30 and 80×24.

### 2.4 Constraints
Standard library and the shipped dependencies only; Windows-safe; no key of the main screen moves (`A` is free: P-1); every new screen text from a board file is a Text piece, never markup (S1); the key bar's law — every key shown works, every key that works is shown — extends to the presentation's seat and to the modals' key lines; the presence markers never block a start and never touch a board file; synthetic data only; the operator's name nowhere; tests never touch the real home.

### 2.5 Assumptions and dependencies
Textual 8.2.8 reads `ESC` + a letter as `alt+<letter>` (P-10) and Windows Terminal sends `alt+<letter>` so; an `App` subclass's `on_unmount` runs at exit (P-11). Two windows run on one machine and one home folder. The calendar is frozen in the tests as the round's (Tuesday 2026-10-20).

### 2.6 Source user stories

| ID | User Story | Source | DoR status |
|----|------------|--------|------------|
| US-2401 | As the operator with several boards, I want one screen with every board's late, today's and this week's dues, a lane per board and the chosen day's tasks, so that I know what to do today without opening each board. | the round's item 1 (variant C); BACKLOG line 149 | READY |
| US-2402 | As the presenter, I want the board's name on my hint row, `?` listing the presentation's keys, and `K`/`J` to reorder where `shift+arrow` does not reach, so that I present from the right board and find every key. | items 2 (B), 3 (A), 5 (A); BACKLOG lines 150, 167, 173 | READY |
| US-2403 | As the presenter, I want the view-3 export without my cursor and cut to its content, so that it reads as a slide. | item 4 (clean); BACKLOG line 170 | READY |
| US-2404 | As the operator, I want every modal button to have a direct key that the modal shows — a letter where nothing is typed, `alt+<letter>` beside text fields — and a confirmation's whole message on screen, so that no button needs `tab` and `enter`. | item 6 (B) and its objection; BACKLOG line 152 | READY |
| US-2405 | As the operator with several boards, I want the start-up modals to name their board, so that I answer for the right one. | item 7 (A); BACKLOG line 153 | READY |
| US-2406 | As the operator with two terminals, I want to be told when I open a board another window has open, so that I close one before the last save wins. | item 8 (A); BACKLOG line 144 | READY |
| US-2407 | As the operator, I want to open a board file without adding it to my boards, so that looking at a copy or a backup does not clutter the home. | item 9 (A); BACKLOG line 151 | READY |

#### Refinement log (one block per story)

**US-2401 — the agenda**
- **INVEST:** I ✓ · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality (V, N):** user = the operator · outcome = `A` opens the agenda (variant C); read-only; `enter` jumps · why = item 1 · out of scope = editing from the agenda; a scrolling lane strip
- **Feasibility (E, S):** `AgendaRuler` of the round moved into `app.py` (screen) and `views.py` (render) · fits one batch? = yes, increment 004, 3 source files
- **Evaluability (T) — behavioral, black-box:** When the operator presses `A` on the round's boards, the screen shows three lanes and today's two dues; `down`, `enter` opens `Golden question set` selected on `Client A` (AT-2401).
- **Open questions:** none. · **Classification:** `READY`.

**US-2402 — the presenter's keys and board**
- **INVEST:** I ✓ · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality (V, N):** user = the presenter · outcome = the chip on the hint row (B); `?` opens the keys window (A) generated from `PRESENT_KEYS`; `K`/`J` (A) · why = items 2, 3, 5 · out of scope = the chip in the frame (variant C, rejected)
- **Feasibility (E, S):** `PresentScreen` (app), `PresentKeys` (modals), `PRESENT_KEYS` (keymap) · fits one batch? = yes, increment 002
- **Evaluability (T) — behavioral, black-box:** `R` on Client A: the hint row opens with ` Client A `, the frame and the export do not hold it (AT-2402); `?` in view 3 opens `PRESENTATION KEYS · view all` and `?` closes it (AT-2403); `down`, `K` moves `Eval harness` first and the file's ranks follow (AT-2405).
- **Open questions:** none. · **Classification:** `READY`.

**US-2403 — the clean export**
- **INVEST:** I ✓ · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality (V, N):** user = the presenter · outcome = view 3's `x` writes the timeline without cursor, cut to its last row of content · why = item 4 · out of scope = views 1/2's exports (unchanged)
- **Feasibility (E, S):** `views.present_all_export`; `PresentScreen.action_export` · fits one batch? = yes, increment 002
- **Evaluability (T) — behavioral, black-box:** `R`, `3`, `x` on Client A at 118×30 writes an SVG of 21 rows holding neither `⟦` nor `project span` (AT-2404).
- **Open questions:** none. · **Classification:** `READY`.

**US-2404 — a key per button**
- **INVEST:** I ✓ · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality (V, N):** user = the operator · outcome = `ConfirmModal` `y`/`n` and its key line (B), its message wrapped; every modal with a text field: `alt+s` save, `alt+i` paste image, `alt+t`/`alt+d` the calendars, `esc` cancel, on a key line; an inventory law over every modal · why = item 6 and its objection (D-6) · out of scope = other TUI applications (the objection's "all our TUI apps" is a standard this repo now follows; other repos are not this batch's)
- **Feasibility (E, S):** `modals.py`, `taskboard.tcss` · fits one batch? = yes, increment 001
- **Evaluability (T) — behavioral, black-box:** the home's `x` shows the whole archive message and `y archive   n / esc cancel   ⇥ the buttons`; `enter` does nothing, `y` archives (AT-2406); `a`, a title, `alt+s` saves the task; `s` typed into a field is text (AT-2407).
- **Open questions:** none. · **Classification:** `READY`.

**US-2405 — the start-up modals' board**
- **INVEST:** I ✓ · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality (V, N):** user = the operator · outcome = the chip opens the milestone offer's and the identity picker's titles (A) · why = item 7 · out of scope = the blank screen behind them (logged)
- **Feasibility (E, S):** `MilestoneOffer`, `TeamIdentityPicker` (modals), their pushes (app) · fits one batch? = yes, increment 003
- **Evaluability (T) — behavioral, black-box:** a start on the round's boards with Client A's offer unanswered shows the offer titled ` Client A  ◆ Milestones · …` (AT-2408).
- **Open questions:** none. · **Classification:** `READY`.

**US-2406 — open twice**
- **INVEST:** I ✓ · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality (V, N):** user = the operator · outcome = a presence marker per open board per window, one warning notice on opening a board another live window holds (A) · why = item 8 · out of scope = blocking, a lasting mark (variant B), a lock on board saves
- **Feasibility (E, S):** `boards.py` (markers), `app.py` (lifecycle) · fits one batch? = yes, increment 003
- **Evaluability (T) — behavioral, black-box:** a second app on Client A shows `Client A is already open in another taskboard window (since 09:30). …`; after the first exits, a third start shows nothing (AT-2409).
- **Open questions:** none. · **Classification:** `READY`.

**US-2407 — open without registering**
- **INVEST:** I ✓ · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality (V, N):** user = the operator · outcome = `--open PATH` (A); `--board` unchanged · why = item 9 · out of scope = listing unlisted files anywhere
- **Feasibility (E, S):** `__main__.py`, `app.py`, `modals.py` (the move refusal) · fits one batch? = yes, increment 003
- **Evaluability (T) — behavioral, black-box:** `taskboard --open elsewhere/board-copy.json` leaves `boards.json`'s bytes unchanged, shows the chip `board-copy · not listed` and the notice, no home; `B` lists the three boards (AT-2410).
- **Open questions:** none. · **Classification:** `READY`.

### 2.7 Premise evaluation (C-43) — MANDATORY, one row per premise

| # | Premise, as a truth-apt proposition | Tier (axiom · hypothesis · premise) | Verdict | Executed evidence (command output / `file:line` — **NOT** a citation of another document) | Disposition |
|---|---|---|---|---|---|
| P-1 | `A` is bound nowhere: not in `KEYMAP`, the home or the presentation | premise | TRUE | `evidence/premises.py` on `base_ref`: `` P-1 `A` in KEYMAP: False \| in the home: False \| in R: False `` (`evidence/premises.txt`) | `A` opens the agenda (HLR-2401) |
| P-2 | The presentation names its board neither on the hint row nor in the frame | premise | TRUE | `P-2 label ('Main', 'fuchsia') \| hint holds the board name: False \| frame holds it: False` | the hint chip (HLR-2402) |
| P-3 | `?` inside the presentation does nothing | premise | TRUE | `` P-3 `?` in view 3 changes the screen stack: False `` | the keys window (HLR-2403) |
| P-4 | The view-3 export is cut at the frame's height and carries the cursor and its echoed span | premise | TRUE | `` P-4 view-3 export: 29 rows x 93 cells \| `⟦` in it: True \| 'project span' in it: True ``; `` P-4b Client A view-3 export: 29 rows x 93 cells, 8 of them blank at the end \| `⟦` in it: True `` | the clean export (HLR-2404) |
| P-5 | `K`/`J` are bound neither in the presentation nor in `KEYMAP`; `shift+↑/↓` is the only reorder | premise | TRUE | `P-5 K/J bound in R: False \| in KEYMAP: False \| reorder keys in R: ['shift+down', 'shift+tab', 'shift+up']` | `K`/`J` (HLR-2405) |
| P-6 | `ConfirmModal` answers neither `y` nor `enter`, and a long message is one row cut by its box | premise | TRUE | `` P-6 message rows on screen: 1 for 128 chars in a 128-cell label \| `y` answers: False \| `enter` answers: False \| buttons: ['yes', 'no'] `` | `y`/`n`, the key line, the wrap (HLR-2406) |
| P-7 | The identity picker's title does not name the board | premise | TRUE | `P-7 label ('Personal', 'green') \| identity picker title names the board: False \| MilestoneOffer.__init__ takes ['board', 'candidates', 'today']` | the chip in the titles (HLR-2408) |
| P-8 | A second window on one board says nothing and leaves no trace | premise | TRUE | `P-8 second window on one board: notices [] \| files under the home besides the boards: []` | the presence notice (HLR-2409) |
| P-9 | `--board PATH` adds the file to `boards.json`; the CLI has no `--open` | premise | TRUE | `` P-9 --board PATH registers: [… 'main'] -> [… 'main', 'board-copy'] \| `--open` in the CLI: False `` | `--open` (HLR-2410) |
| P-10 | Textual 8.2.8's parser reads `ESC s` as `alt+s` | premise | TRUE | `P-10 ESC s read by Textual 8.2.8's parser as: ['alt+s']` | `alt+<letter>` keys (HLR-2407) |
| P-11 | An `App` subclass's `on_unmount` runs at exit | premise | TRUE | `P-11 an App subclass's on_unmount runs at exit: True` | the marker withdrawn at exit (HLR-2409) |

- **Premise evaluation:** 11 premise(s) · ✅ TRUE ×11

### 2.8 Fork preconditions (C-52) — MANDATORY, and the declared empty when the batch does not fork

- **Fork preconditions:** none — this batch runs one lane: four increments in order on one branch (`feat/backlog-round`), one owner (the orchestrator) holds the trunk.

---

## 3. High-level requirements (HLR)

### HLR-2401 — An agenda of every board
- **Traceability:** US-2401
- **Ledger:** LED-2026-10-20-batch-03.1, LED-2026-10-20-batch-03.2, LED-2026-10-20-batch-03.3, LED-2026-10-20-batch-03.7, LED-2026-10-20-batch-03.8
- **Statement:** When the operator presses `A` on the main screen or on the home, the system shall show, read-only, the agenda of every active board — a head row (`◆ ALL BOARDS`, `<n> boards · read-only` where `<n>` counts the lanes, `1 board` singular; at the right `▲<late> late · <today> today · <week> to Sun <day>`), a bucket row (`LATE`, `TODAY`, then each day to Sunday written `Wed 21`, the chosen bucket marked `▼` and shaded), one lane per active board in the registry's order — and, when the open board is unlisted (`--open`), a last lane for it under its chip's name — (`▌` and the name in the board's colour, a `●` per open task with a due date in each bucket, `·` where none; a board whose file is missing or unreadable drawn with its name dimmed and, from 100 cells, `file missing` / `file unreadable`), a rule, the chosen bucket's head (`<BUCKET> · <n> due across <m> boards`, singular `1 due`, `1 board`) and its tasks (the board's bar and name, from 100 cells the project, the title, and `▲Nd` / `today` / `Wed 21`), ordered by due date then lane, and a key row in the key bar's style (`←→ day   ↑↓ task   ↵ open on its board   esc back` then `· read-only: nothing here edits a task`, the tail dropped first and the words before any key when the row is narrow); it shall open on `TODAY`; `←`/`→` (`h`/`l`) choose the bucket, `↑`/`↓` (`k`/`j`) the task; `enter` shall close it (and the home beneath it), open the task's board in place when it is another — a switch, with a switch's own writes — and select the task; `escape` or `A` shall close it; the agenda itself shall write nothing; `A` shall not act over a modal or the presentation, and no other key of the main screen shall act while the agenda is open; `A` shall be listed by `?`'s map and the palette (`KEYMAP`, off the main bar) and on the home's key row (`A all boards`).
- **Rationale (informative):** item 1, variant C (`AgendaRuler`), opened from the home as the round's scene was (ux UX-1); a lane per board answers "which board carries which day" at a glance. The list's order changes from the capture the operator saw (by board name) to lane order (declared, to be said at the close).
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_all_agenda.py`
- **Numeric pass threshold:** AT-2401: the round's boards (`tests/backlog_round_fixture.py`, `last` Client A) under the seam home, the calendar frozen at 2026-10-20, `open_app(None)` at 118×30 → the home; `A` (on the home) → the screen's text holds `◆ ALL BOARDS`, `3 boards · read-only`, `▲3 late · 2 today · 8 to Sun 25`, the bucket row `LATE`, `▼ TODAY`, `Wed 21` … `Sun 25`, the lanes `Personal`, `Client A`, `Course` in that order, `TODAY · 2 due across 2 boards`, then `Week 3 plan` (Personal) before `Golden question set` (Client A); `enter` → the main screen (no home), the head row's chip ` Personal ` and `Week 3 plan` on the highlighted row (the board switched); `A`, `down`, `enter` → the chip ` Client A ` and `Golden question set` highlighted; at 80×24 the home's key row ends `A all boards  esc back  q` — the multi-board round's own C capture, `quit`'s word dropped, its key kept (ux UX-24 asked `q quit`; the approved capture wins) and the agenda's key row keeps every key (qa QA-23); the fixture's boards are already migrated and clean, so every board file is byte-identical to the build (`boards.json` aside: the switch records the opening). The same at 80×24 without the project column.
- **Priority:** medium
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** one screen shows which board carries which day and what is due on it; `enter` lands on the task.
  - **Shipped surface:** `taskboard` → `A`.
  - **Acceptance test(s):** AT-2401
  - **Boundary catalog (QC-3):** ☑ boundary (Sunday: `LATE` and `TODAY` only; `→` past `Sun` and `←` past `LATE` stay; a bucket with no task: `nothing due`, `enter` does nothing; lanes are not capped — with many boards at 24 rows the list keeps fewer rows, a declared limit) ☑ empty (one board: one lane, `1 board`; no dues at all) ☑ invalid (a board whose file is missing or unreadable: its lane dimmed, `file missing`; a title holding `[b]x[/b]` printed as typed) ☑ error (`enter` on a board whose file vanished: the home's notice, the agenda closed, nothing opened)
  - **Negative control:** on `base_ref` AT-2401 is RED: `A` does nothing (P-1; `evidence/red-004.txt` — planned).

### HLR-2402 — The board's chip on the presentation's hint row
- **Traceability:** US-2402
- **Ledger:** LED-2026-10-20-batch-03.1, LED-2026-10-20-batch-03.2, LED-2026-10-20-batch-03.3
- **Statement:** While the open board has a chip (`Board.label` set: more than one active board, or an unlisted board), the presentation's hint row shall open with the open board's chip (` <name> ` in bold board-background ink on the board's colour, the name cut to 24 cells) and one space, the rest of the hint fitted to what is left; the frame, and every file `x` exports, shall never carry it; with no label the hint is unchanged.
- **Rationale (informative):** item 2, variant B (`PresentChipHint`): the frame and the export never name the board (on a mirrored terminal the room can read the hint row, chip included — ux UX-20).
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_present_backlog_round.py -k 2402`
- **Numeric pass threshold:** AT-2402: the round's boards, Client A open, 118×30, `escape`, `R` → the hint row's text starts ` Client A  1 gantt`; the frame's text holds no `Client A`; `x` → the exported SVG's text holds no `Client A` (an SVG's text is read row by row: `&#160;` unescaped to a space, the `<text>` pieces of each `line-N` joined — qa QA-2); `3`, `x` → the same; a one-board app's hint starts `1 gantt`.
- **Priority:** low
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** the presenter reads the board's name under the frame; the slide never shows it.
  - **Shipped surface:** `R`; the hint row; `reports/present-*.svg`.
  - **Acceptance test(s):** AT-2402
  - **Boundary catalog (QC-3):** ☑ boundary (a 30-character name: cut to 24 cells; 80 columns: the hint takes a shorter wording) ☑ empty (one board: no chip) ☐ invalid — none ☐ error — none
  - **Negative control:** on `base_ref` AT-2402 is RED: the hint starts `1 gantt` (P-2; `evidence/red-002.txt` — planned).

### HLR-2403 — `?` lists the presentation's keys from one seat
- **Traceability:** US-2402
- **Ledger:** LED-2026-10-20-batch-03.1, LED-2026-10-20-batch-03.2, LED-2026-10-20-batch-03.3, LED-2026-10-20-batch-03.5
- **Statement:** The presentation's key bindings shall be generated from one seat, `keymap.PRESENT_KEYS` (rows of keys, the keys as shown, the words, a group and the one view a row acts in, if any); when the presenter presses `?` at `PRESENT_MIN_WIDTH` columns or more, the system shall open a window titled `PRESENTATION KEYS · view <name>` that lists every row of the seat under its group (`VIEWS`, `MOVE`, `CURATE`, `OUT`), a row that acts in the current view or in every view in the bright key style, another view's row dimmed with `(<view>)`, and a last line `? / esc close · dim = another view's key`; `?`, `escape` or `q` shall close it, the frame as it was; the hint row shall end with `? keys` at every width from `PRESENT_MIN_WIDTH` (below it the hint is `esc leave` alone, as today), the rest of the hint chosen and cut as before in the room left (so each wording's first width moves 8 columns up — at 80 columns the gantt view takes the short wording, superseding HLR-2002's middle one there: D-14); the window is never exported.
- **Rationale (informative):** item 3, variant A (`PresentKeys`); the seat the round asked for so the window and the bindings cannot drift (BACKLOG line 167).
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_present_backlog_round.py -k 2403`
- **Numeric pass threshold:** AT-2403: the round's boards, Client A, 118×30, `escape`, `R`, `3`, `?` → the window's text holds `PRESENTATION KEYS · view all`, the four group heads, `⇧↑↓ K J` beside `move a project up / down` in the bright style, `pgdn pgup` dimmed with `(split)`; `?` → the presentation again, the frame's text equal to before; `1`, `?` → `view gantt`, the reorder row dimmed with `(all)`; `escape` closes it; at 118×30 and at 80×24 every view's hint ends `? keys`. TC-2403: the set of (key, action) pairs `PresentScreen.BINDINGS` binds equals the set the seat declares, and every seat row is a row of the window.
- **Priority:** medium
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** `?` in the presentation shows every key it has, the current view's bright.
  - **Shipped surface:** `R` → `?`.
  - **Acceptance test(s):** AT-2403
  - **Boundary catalog (QC-3):** ☑ boundary (80×24: the window fits; below `PRESENT_MIN_WIDTH`: `?` does nothing, as every key but `esc`/`q`) ☐ empty — none ☐ invalid — none ☐ error — none
  - **Negative control:** on `base_ref` AT-2403 is RED: `?` does nothing (P-3; `evidence/red-002.txt` — planned).

### HLR-2404 — The view-3 export has no cursor and ends at its content
- **Traceability:** US-2403
- **Ledger:** LED-2026-10-20-batch-03.1, LED-2026-10-20-batch-03.2, LED-2026-10-20-batch-03.3
- **Statement:** When the presenter presses `x` in view 3, the system shall export the timeline (without the rail) laid out as on screen — the folds of this presentation, and the overflow folds anchored on the cursor's project as the screen's are — but drawn with no cursor — no `⟦`, and the ruler's tick row echoing no project or task — its rows cut after the last row that holds anything but blanks (a row with content never cut); the SVG and the PNG shall be that many rows tall; the screen keeps its cursor; views 1 and 2 export as before.
- **Rationale (informative):** item 4, "limpia" (`proto._export`): the export is for other people.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_present_backlog_round.py -k 2404`
- **Numeric pass threshold:** AT-2404: the round's boards, Client A, the PNG rasteriser stubbed (no Edge in the suite), 118×30, `escape`, `R`, `3`, `x` → `reports/present-board-2026-10-20-all.svg` holds 21 rows of text (its highest `line-N` reference + 1 — Rich defines one clip path fewer than its rows, qa QA-3), and its text, read as HLR-2402 reads it, holds neither `⟦` nor `project span` and holds every shown project name of Client A; the frame on screen still holds `⟦`; the rasteriser was asked for 93 × 21 cells; at 80×24 21 rows of 80 cells. TC-2404: `views.present_all_export` on a board whose timeline fills the frame keeps every row (the `+N more rows not shown` row included); on an overflowing board with the cursor on its last project, the export's folded projects equal the screen's (architect A-1).
- **Priority:** medium
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** the exported timeline reads as a slide: no cursor, no empty tail.
  - **Shipped surface:** `R` → `3` → `x`; `reports/present-*-all.svg|png`.
  - **Acceptance test(s):** AT-2404
  - **Boundary catalog (QC-3):** ☑ boundary (a timeline taller than the frame: every row kept, the overflow row included) ☑ empty (no shown project: the head and the ruler only) ☐ invalid — none ☐ error — none (the PNG's absence is today's notice)
  - **Negative control:** on `base_ref` AT-2404 is RED: the rasteriser asked for 93 × 29, `⟦` and `project span` in the SVG's text (P-4; `evidence/red-002.txt` — planned).

### HLR-2405 — `K`/`J` reorder beside `shift+↑/↓`
- **Traceability:** US-2402
- **Ledger:** LED-2026-10-20-batch-03.1, LED-2026-10-20-batch-03.2, LED-2026-10-20-batch-03.3, LED-2026-10-20-batch-03.5, LED-2026-10-20-batch-03.8
- **Statement:** In view 3, `K` and `J` shall do what `shift+↑` and `shift+↓` do (the cursor's project one place up / down, saved); the hint's wordings shall name them: `⇧↑↓/K J reorder` (long), `K J order` (middle), `K J` (glyphs).
- **Rationale (informative):** item 5, variant A (`PresentReorderKJ`); `[`/`]` rejected (the main screen's phase keys).
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_present_backlog_round.py -k 2405`
- **Numeric pass threshold:** AT-2405: the round's boards, Client A, 118×30, `escape`, `R`, `3`, `down`, `K` → the rail lists `Eval harness` first, the board file's `present_rank` puts it first; `J` → back second; at 118×30 view 3's hint holds `K J`; at 80×24 too.
- **Priority:** low
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** a terminal that drops `shift+arrow` can still reorder.
  - **Shipped surface:** `R` → `3` → `K`/`J`.
  - **Acceptance test(s):** AT-2405
  - **Boundary catalog (QC-3):** ☑ boundary (`K` on the first project and `J` on the last: nothing) ☐ empty — none ☐ invalid — none ☐ error — none
  - **Negative control:** on `base_ref` AT-2405 is RED: `K` does nothing (P-5; `evidence/red-002.txt` — planned).

### HLR-2406 — A confirmation answers `y` and `n`, says so, and shows its whole message
- **Traceability:** US-2404
- **Ledger:** LED-2026-10-20-batch-03.1, LED-2026-10-20-batch-03.2, LED-2026-10-20-batch-03.3, LED-2026-10-20-batch-03.4
- **Statement:** `ConfirmModal` shall confirm on `y` and cancel on `n` or `escape` (`y`/`n` pressing its buttons); `enter` alone shall do nothing while the box holds the focus (as today); under its buttons a key line shall read `y <the confirm word, lower case>   n / esc cancel   ⇥ the buttons` (the `/` dim); its message shall wrap inside the box, never cut. The move's confirmation (`MoveConfirm`, the most destructive) shall follow the same standard (ux UX-2): `y` moves, `n` or `escape` cancel, `enter` does nothing, its key line `y move[ and drop N links]   n / esc cancel`.
- **Rationale (informative):** item 6, variant B (`ConfirmKeys`); the wrap fixes the round's finding (the message cut at «…its folder is not»), which the key line sits under.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_modal_keys.py -k 2406`
- **Numeric pass threshold:** AT-2406: the round's boards at 118×30, the home, `left` (Personal), `x` → the box's text holds every word of `Archive Personal? It leaves the home; its folder is not touched. taskboard --board <its path> brings it back.` and `y archive   n / esc cancel   ⇥ the buttons`; `enter` → still the confirmation; `n` → the home, Personal active; `x`, `y` → `Archived Personal …`, the home without Personal; on the main screen a task's `d`, `y` deletes it. The same at 80×24. The message is read inside the box's region (a path wider than the box breaks inside itself, so its characters are compared in order, whitespace aside — qa QA-11). On a fresh app over the same fixture, the move (`escape`, `P`, `down`, `m`, `enter` on the first target) → the confirmation's key line `y move …   n / esc cancel`; `enter` → still the confirmation; `y` → moved.
- **Priority:** medium
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** a confirmation is one key, written on it, and says all it means.
  - **Shipped surface:** every `ConfirmModal` (the home's archive, `d`, `X`, the projects' delete) and `MoveConfirm`.
  - **Acceptance test(s):** AT-2406
  - **Boundary catalog (QC-3):** ☑ boundary (a message longer than three rows at 80×24: the box scrolls, no word cut) ☐ empty — none ☐ invalid — none ☑ error (`enter` on the box: nothing; `tab` then `enter` on a button: as today)
  - **Negative control:** on `base_ref` AT-2406 is RED: `y` does nothing and the message is one cut row (P-6; `evidence/red-001.txt` — planned).

### HLR-2407 — Every button of a modal with a text field has an `alt+<letter>` key on a key line
- **Traceability:** US-2404
- **Ledger:** LED-2026-10-20-batch-03.1, LED-2026-10-20-batch-03.2, LED-2026-10-20-batch-03.3, LED-2026-10-20-batch-03.4, LED-2026-10-20-batch-03.8
- **Statement:** Every modal holding a text field shall bind keys that press its buttons (one routing: the key presses the button) — `alt+s` its Save button (`TaskModal`, `ProjectModal`, `TemplateEditor`, `ClockModal`, `TextPrompt`), `alt+i` to `Paste image` (`TaskModal`), `alt+t` and `alt+d` to the start and due calendars (`TaskModal`, `ProjectModal`), and keep `escape` for Cancel; each shall show a key line of those keys, three spaces between pairs (`alt+s save`, `alt+i paste image`, `alt+t start date`, `alt+d due date`, `esc cancel`; in the 62-cell project form `alt+t start`, `alt+d due`, so `esc cancel` keeps its word; `↵ / alt+s save` where `enter` in the field saves, `TextPrompt`) — in the four boxed modals under the buttons, in the full-screen task editor as its last row, whose words go from the right before any key when the row is too narrow; a plain letter typed in a field stays text. Every modal of the app shall reach each of its buttons by a direct key it shows, and a law shall hold every `ModalScreen` subclass of the package (found by walking `taskboard.modals` and `taskboard.app`) to its inventory row. Checkboxes and selects are fields, reached by `tab` as today (qa QA-15); the editor keeps its title's `ctrl+e emoji` and its preview's `ctrl+v paste · esc cancel` as they are (ux UX-14, a decision at the captures).
- **Rationale (informative):** the objection to item 6 (D-6): «un acceso directo a los botones … cuando hay bloques de entrada de texto usar una combinación específica»; no modal saves with `ctrl+s` today, so none is kept.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_modal_keys.py -k 2407`
- **Numeric pass threshold:** AT-2407: a one-board app at 118×30: `a`, `Draft s`, `alt+s` → a task `Draft s` saved (the `s` typed, not a save); `e` on it, `alt+d` → the calendar, `escape`, `escape` → the board unchanged; `p`, `Site`, `alt+s` → a project `Site`; the editor's last row reads `alt+s save   alt+i paste image   alt+t start date   alt+d due date   esc cancel` (whole at 118; at 80 words go before keys — ux UX-22); at 80×24 every key of that row is still on it and the notes area is at most one row shorter than at `base_ref`, nothing clipped (ux UX-3); `c`, `alt+s` saves the clocks; `I`, `enter` on `New template...` (the `TemplateEditor`), a name, `alt+s` → the editor saves the template. TC-2407: the inventory law — every `ModalScreen` subclass in `taskboard.modals` and `taskboard.app` is in the law's table; a modal whose source yields a `Button` has a row naming each button's key; composed, its buttons are exactly the row's; pressing each key gives what pressing its button gives; its screen names every key; and `TextPrompt`'s `alt+s` equals its Save.
- **Priority:** medium
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** no button needs `tab`; the keys are written on the modal.
  - **Shipped surface:** `a`/`e` (task), `p` (project), `c` (clocks), `I` → new template, every `TextPrompt`.
  - **Acceptance test(s):** AT-2407
  - **Boundary catalog (QC-3):** ☑ boundary (80×24: the editor's key line drops words, never keys; the boxed project form scrolls at 80×24 as it does today, its key line below the buttons) ☐ empty — none ☑ invalid (a plain `s`, `i`, `t`, `d` typed: text) ☐ error — none
  - **Negative control:** on `base_ref` AT-2407 is RED: `alt+s` does nothing (`evidence/red-001.txt` — planned).

### HLR-2408 — The start-up modals name their board
- **Traceability:** US-2405
- **Ledger:** LED-2026-10-20-batch-03.1, LED-2026-10-20-batch-03.2, LED-2026-10-20-batch-03.3
- **Statement:** While the open board has a chip (`Board.label` set), the milestone offer's title and the team identity picker's title shall open with the open board's chip and one space, both titles wrapping in their box rather than cut (ux UX-16); with no label they are unchanged. The identity picker shall show a key line `↵ pick   esc cancel` (ux UX-16, D-6).
- **Rationale (informative):** item 7, variant A (`OfferNamedA`, `IdentityNamedA`).
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_boards_backlog_round.py -k 2408`
- **Numeric pass threshold:** AT-2408: the round's boards with Client A's offer unanswered (`milestone_offer` marker), `open_app(None)` at 118×30 → the offer's title text starts ` Client A  ◆ Milestones · convert one-day tasks?`; Course set in team mode (a synthetic team folder with `team.json` listing `username_subject` and `Teammate B`, no identity chosen) opened from the home → the picker's title starts ` Course ` and holds `Operator identity`, the key line `↵ pick   esc cancel`; a one-board start's offer title starts `◆ Milestones`.
- **Priority:** low
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** the operator reads which board the start-up question is about.
  - **Shipped surface:** the start (and a switch) of a board with the offer or team mode pending.
  - **Acceptance test(s):** AT-2408
  - **Boundary catalog (QC-3):** ☑ boundary (a 30-character name: cut to 24 cells) ☑ empty (one board: no chip) ☐ invalid — none ☐ error — none
  - **Negative control:** on `base_ref` AT-2408 is RED: the titles start `◆ Milestones` / `Operator identity` (P-7; `evidence/red-003.txt` — planned).

### HLR-2409 — One notice when a board is open in another window
- **Traceability:** US-2406
- **Ledger:** LED-2026-10-20-batch-03.1, LED-2026-10-20-batch-03.2, LED-2026-10-20-batch-03.3, LED-2026-10-20-batch-03.6
- **Statement:** While a board is open, the window shall keep a presence marker for it — `open/<the first 16 hex digits of the SHA-256 of the board file's key (`boards._key`: resolved, case-normalised)>-<a random 32-hex token>.json` in the home's `~/.taskboard/` (Main's folder, beside `boards.json`; never another board's folder), holding `{"since": <local time, minutes>, "pid": <process id>}` — renewed every 30 s of the app's clock and removed when that board is left (a switch) or the app exits; when the operator opens a board (at start, from the home, from the agenda, with `--open`) and another fresh marker of that file exists, the system shall show one warning notice (`markup=False`, 30 s) titled `Boards · open twice`: `<board name> is already open in another taskboard window (since <HH:MM of the earliest>). Both save the same file: the last save wins. Close one of them.` (`… in <n> other taskboard windows (the first since …)` when more than one; without `(since …)` when it cannot be read; `<HH:MM>` as `%H:%M`, or `Oct 19 09:12` when not today); a marker is read only as a regular file (`os.lstat`, `S_ISREG`) whose whole name matches this board's pattern, its age taken from its modification time only (never its `since`), `since` read from at most its first 4096 bytes and anything but a JSON object with a parseable string `since` counted with no time; a regular marker file more than 120 s from now (past or future) is a dead window's: ignored and removed after a second `lstat` shows it unchanged; a marker whose JSON cannot be written is removed at once; a marker that cannot be written, read or removed never stops a start, a switch or an exit; nothing else changes.
- **Rationale (informative):** item 8, variant A (`warn_twice`), on batch-02's lock design (stale-tolerant, owner-token, regular files only); a marker per window keeps two windows from erasing each other's.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_boards_backlog_round.py -k 2409`
- **Numeric pass threshold:** AT-2409: the round's boards, the clock frozen at 09:30, a first app on Client A running at 118×30 → its notices hold no `open twice`, one marker under `open/`; a second app on Client A → one notice `Client A is already open in another taskboard window (since 09:30). Both save the same file: the last save wins. Close one of them.`, two markers; the second exits → one marker; the first switches to Course (home, `enter`) → no notice, its Client A marker gone, a Course marker; it exits → no marker; a third app on Client A → no `open twice`. TC-2409: a marker aged 121 s is ignored and removed, one aged 119 s counts; a directory or a foreign file name under `open/` is neither read nor removed; `[]`, `{"since": 5}`, `{"since": null}` and a 10 MB file each count with no time, nothing raised; a write failing after the create leaves no file; two spellings of one file (relative and absolute; letter case) share one pattern; `open/` unwritable → the board opens, no marker, no notice; two others → `in 2 other taskboard windows (the first since …)`; a registry name `[/b]` → the notice holds `[/b]` as typed, nothing raised; a second window opening the board with `--open` warns too (qa QA-8).
- **Priority:** medium
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** the second window on a board says so once, at opening; nothing blocks.
  - **Shipped surface:** `taskboard` (start), the home's `enter`, the agenda's `enter`; `~/.taskboard/open/`.
  - **Acceptance test(s):** AT-2409
  - **Boundary catalog (QC-3):** ☑ boundary (a marker 119 s / 121 s old; 121 s in the future) ☑ empty (no `open/` folder: made) ☑ invalid (not JSON, the wrong shape, oversize: counted, no `since`; a directory at a marker's name: skipped; markup-looking names) ☑ error (`open/` unwritable: no marker, no notice, the start goes on; a failed write: no file left)
  - **Negative control:** on `base_ref` AT-2409 is RED: the second window shows no notice and no marker exists (P-8; `evidence/red-003.txt` — planned).

### HLR-2410 — `--open PATH` opens a board without registering it
- **Traceability:** US-2407
- **Ledger:** LED-2026-10-20-batch-03.1, LED-2026-10-20-batch-03.2, LED-2026-10-20-batch-03.3, LED-2026-10-20-batch-03.6, LED-2026-10-20-batch-03.8, LED-2026-10-20-batch-03.9
- **Statement:** When `taskboard --open PATH` names an existing board file (a regular file, after a leading `~` is read as `Path.home()`, that parses to a JSON object), the system shall open it without writing `boards.json` (no entry, no `last`): the board's chip shall read `<name> · not listed` (the file's name as a registered board would be named — `boards.name_for`, its control characters stripped (security S-11) — on `pink`) whatever the number of boards, the home shall not open at start, a notice (`markup=False`, 15 s) shall say `Opened <PATH> without adding it to your boards (--open). B lists your <n> boards; this file is not one of them.` (`1 board` singular), `B` shall list the registered boards, a project moved out of it (`P`, `m`) shall be refused with `This board is not listed (--open): open it with --board to move its projects.`, and it shall be no move target; the file itself opens read-write and its start writes as any board's does (the one-time migrations, the renumber notice's mark, the sweep of old done work; architect A-2 — a read-only `--open` is an item for the operator); once the operator switches away from it, it is not reachable again in that session; when PATH is not such a file the system shall exit with status 2 and `taskboard: no board file at <PATH> (--open opens an existing one)` on stderr, checked right after the arguments are read, before `--report` and before anything is built, writing nothing; `<PATH>` is printed with its control characters stripped; `--open` and `--board` together shall be refused by the argument parser (`not allowed with argument`); `--board PATH` is unchanged; `--report` reads `--open`'s file as it reads `--board`'s.
- **Rationale (informative):** item 9, variant A (`opened_unlisted`); a missing file is refused because the loader would seed and save sample data there.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_boards_backlog_round.py -k 2410`
- **Numeric pass threshold:** AT-2410: the round's boards (`last` Client A) with `elsewhere/board-copy.json`, `main()` with `--open <that path>` building the app (the TUI run captured) at 118×30 → `boards.json`'s bytes unchanged after the app exits; the screen is the main screen (no home), the head row's chip ` board-copy · not listed `, the notice `Opened … without adding it to the boards (--open). B lists the 3 boards; this file is not one of them.`; `B` → three cards `Personal`, `Client A`, `Course`; `escape`, `P`, `m` → the refusal notice; `--open <missing path>` → `SystemExit(2)`, the message on stderr, no file at the path; `--open <missing> --report` → the same, no file; `--open <a folder>` and `--open <a text file>` → `SystemExit(2)`; `--open X --board Y` → `SystemExit(2)` with `not allowed with argument` on stderr.
- **Priority:** medium
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** looking at a copy leaves the boards as they were, and the screen says the copy is not one of them.
  - **Shipped surface:** `taskboard --open PATH`; `boards.json`.
  - **Acceptance test(s):** AT-2410
  - **Boundary catalog (QC-3):** ☑ boundary (`--open` of a registered board's own path: that board, `last` unchanged, no `not listed`; `~/…`) ☑ empty (no `boards.json`: one board known, `1 board`, the chip still shown) ☑ invalid (a missing path, a folder, a file that is not a board, both options) ☐ error — none beyond the loader's own
  - **Negative control:** on `base_ref` AT-2410 is RED: `--open` is an unknown option (exit 2) (P-9; `evidence/red-003.txt` — planned).

---

## 4. Low-level requirements (LLR)

> Each LLR decomposes an HLR into a verifiable property at the implementation level.
> Same regime: EARS syntax owed in `full`, recommended in `core`. ID format: `LLR-<HLR>.<M>`.

### LLR-2401.1 — `views.all_agenda` and `views.render_all_agenda`
- **Traceability:** HLR-2401
- **Ledger:** LED-2026-10-20-batch-03.1, LED-2026-10-20-batch-03.2, LED-2026-10-20-batch-03.3
- **Statement:** `taskboard/views.py` (NEW symbols — created in increment 004) shall provide `AgendaItem(bucket, lane, board_name, colour, task, project, due)`, `agenda_buckets(today) -> list[(key, label)]` (`("late", "LATE")`, `(today, "TODAY")`, then each later day to Sunday as `f"{d:%a} {d.day}"` — never `%-d`, which Windows refuses), `all_agenda(lanes, today) -> list[AgendaItem]` over plain lanes `[(name, colour, board | None, state)]` (`state` `""`, `"file missing"` or `"file unreadable"`; no registry type reaches `views` — architect A-4) — every task with `is_open` and a due date on or before Sunday, `late` before today — sorted by (due, lane index, board order), and `render_all_agenda(lanes, items, day, row, today, width, height) -> Text` drawing HLR-2401's rows exactly `width` cells each, every board-file string a plain Text piece cut with `fit`, the project column only from 100 cells, the list scrolled to keep `row` on screen, `nothing due` for an empty bucket, a lane with a `state` dimmed and its state shown from 100 cells; the key row is built by the screen with `keymap.key_line`.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_all_agenda.py -k TC_2401`
- **Numeric pass threshold:** TC-2401: on the round's boards at 2026-10-20 `agenda_buckets` has 7 entries ending `Sun 25`, at Sunday 2026-10-25 two; `all_agenda` → 3 late, 2 today, 8 to Sunday, `Week 3 plan` before `Golden question set`; every rendered row at 118 and 80 is the width in cells; the 80-cell render holds no project name; a task titled `[b]x[/b]` renders those 8 characters; a lane whose board is None draws `·` in every bucket.
- **Negative control:** TC-2401 goes RED when the sort drops the lane order, when a done or archived task is listed, when Sunday is excluded, when the project column shows at 80 (increment 004's battery — planned).
- **Boundary catalog:** ☑ boundary (Sunday; a due on Sunday) ☑ empty (no dues) ☑ invalid (a markup-looking title) ☐ error — none

### LLR-2401.2 — `app.AllBoardsAgenda` and `A`
- **Traceability:** HLR-2401
- **Ledger:** LED-2026-10-20-batch-03.1, LED-2026-10-20-batch-03.2, LED-2026-10-20-batch-03.3, LED-2026-10-20-batch-03.7
- **Statement:** `taskboard/keymap.py` shall declare `Key("A", "A", "agenda_all", "All boards", group="misc", bar=False)`; `taskboard/app.py` (NEW — created in increment 004) shall provide `AllBoardsAgenda(Screen)` whose lanes are `registry.active()` each with the app's board for the open one, `peek_board` for an existing file, else None (`file missing`; an unreadable one `file unreadable`), plus the open unlisted board last, read once at open; priority bindings `left,h`/`right,l` (bucket), `up,k`/`down,j` (row), `enter` (jump), `escape,A` (close); `TaskboardApp.action_agenda_all` pushes it; `check_action` lets `agenda_all` act — on the main screen and on the home, which are screens; a pushed modal (the presentation, the home's own modals among them) holds its keys, so `A` never reaches past one (Textual's modal binding chain; architect A-17) — and refuses, while the agenda is on the stack, every seat action but `quit`, as it does for the home; the home's key row shows `A all boards` (`views.HOME_KEYS`, words dropped from the right, keys never); the jump pops the agenda and the home under it, calls `switch_board` when the item's board is another and, when the open board is then the item's, `jump_to` the task.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_all_agenda.py -k TC_2401`
- **Numeric pass threshold:** TC-2401 (app): `A` over a `ConfirmModal` and the presentation leaves the stack as it was; `A` on the home opens the agenda over it and `enter` leaves neither; with the agenda open `a`, `d`, `1`, `B` change nothing; `enter` on an item whose board file was removed after the agenda opened → the home's missing-file notice and the open board unchanged; `A` closes it.
- **Negative control:** TC-2401 goes RED when `check_action` lets `A` act over a modal, when the seat keys act behind the agenda, when the jump does not switch (increment 004's battery — planned).
- **Boundary catalog:** ☐ boundary — none ☐ empty — none ☐ invalid — none ☑ error (the jump's board missing)

### LLR-2402.1 — `PresentScreen._hint` opens with the chip
- **Traceability:** HLR-2402
- **Ledger:** LED-2026-10-20-batch-03.1, LED-2026-10-20-batch-03.2, LED-2026-10-20-batch-03.3
- **Statement:** `taskboard/views.py` shall provide `board_chip_text(label) -> Text` (the `board_chip` of a Text: ` <name cut to 24> ` bold `#0d1117` on `board_hex(colour)`, then a space; empty for no label); `PresentScreen._hint(w)` shall, when `self._board.label` is set and `w` is at least `PRESENT_MIN_WIDTH`, return the chip and the hint fitted to `w` minus the chip's cells.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_present_backlog_round.py -k TC_2402`
- **Numeric pass threshold:** TC-2402: `_hint(118)` with label (`Client A`, `sky`) → plain starts ` Client A  1 gantt` and is at most 116 cells; the chip's span is bold on `HEX["sky"]`; a 30-character name → 24 cells of name; label None → no chip.
- **Negative control:** TC-2402 goes RED when the chip is dropped, when it is added to the frame (increment 002's battery — planned).
- **Boundary catalog:** ☑ boundary (24 cells) ☑ empty (no label) ☐ invalid — none ☐ error — none

### LLR-2403.1 — `keymap.PRESENT_KEYS` and `present_bindings`
- **Traceability:** HLR-2403, HLR-2405
- **Ledger:** LED-2026-10-20-batch-03.1, LED-2026-10-20-batch-03.2, LED-2026-10-20-batch-03.3
- **Statement:** `taskboard/keymap.py` (NEW symbols — created in increment 002) shall provide `PresentKey(binds: tuple[tuple[str, str], ...], show, label, group, view=None)` and `PRESENT_KEYS` — VIEWS: `1`/`2`/`3` → `view(0..2)` `1 2 3` `gantt · split · all`; `tab`/`shift+tab` → `cycle(±1)` `⇥ ⇧⇥` `next / previous view`; MOVE: `up,k`/`down,j` → `move(∓1)` `↑↓` `move the cursor`; `left,h`/`right,l` → `side(∓1)` `←→` `move · in all: rail ↔ timeline`; `pageup`/`pagedown` → `scroll(∓1)` `pgdn pgup` `scroll the notes`, view `split`; CURATE: `space` → `hide` `␣` `hide the cursor's row`; `a` → `show_all` `a` `show everything hidden`; `u` → `hidden_picker` `u` `list what is hidden`; `shift+up,K`/`shift+down,J` → `reorder(∓1)` `⇧↑↓ K J` `move a project up / down`, view `all`; `enter` → `fold` `enter` `fold a project`, view `all`; OUT: `x` → `export` `x` `export this view · SVG + PNG`; `escape,q` → `close` `esc q` `leave`; `question_mark` → `keys` `?` `these keys` — and `present_bindings() -> list[Binding]`, one priority binding per (keys, action); `PresentScreen.BINDINGS = present_bindings()`.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_present_backlog_round.py -k TC_2403`
- **Numeric pass threshold:** TC-2403: `{(key, action)}` over `PresentScreen.BINDINGS` (aliases split) equals the seat's; every binding is priority; the existing presentation suites pass with the generated bindings.
- **Negative control:** TC-2403 goes RED when a binding is added to `PresentScreen` outside the seat or a seat row is not bound (increment 002's battery — planned).
- **Boundary catalog:** ☐ boundary — none ☐ empty — none ☑ invalid (a key bound twice) ☐ error — none

### LLR-2403.2 — `modals.PresentKeys` and `PresentScreen.action_keys`
- **Traceability:** HLR-2403
- **Ledger:** LED-2026-10-20-batch-03.1, LED-2026-10-20-batch-03.2, LED-2026-10-20-batch-03.3, LED-2026-10-20-batch-03.5
- **Statement:** `taskboard/modals.py` (NEW — created in increment 002) shall provide `PresentKeys(ModalScreen[None])(view)` rendering HLR-2403's window from `PRESENT_KEYS` (60 cells wide at most, scrolling when taller than the screen) with priority bindings `escape,question_mark,q` → close; `PresentScreen.action_keys` shall push it with the current view's name unless `_narrow()`; `_hint` shall end every wording at `PRESENT_MIN_WIDTH` or more with `  ? keys`, fitted with the rest; `PresentScreen.action_keys` is a no-op below it.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_present_backlog_round.py -k TC_2403`
- **Numeric pass threshold:** TC-2403 (window): for view `split` the `pgdn pgup` row is bright and the reorder row dim with `(all)`; every seat row's `show` appears once; `PresentKeys` never reaches the export (the exported SVG after `?`, `?`, `x` equals the one before).
- **Negative control:** TC-2403 goes RED when the live/dim rule is inverted, when a seat row is skipped (increment 002's battery — planned).
- **Boundary catalog:** ☑ boundary (80×24) ☐ empty — none ☐ invalid — none ☐ error — none

### LLR-2404.1 — `views.present_all_export`
- **Traceability:** HLR-2404
- **Ledger:** LED-2026-10-20-batch-03.1, LED-2026-10-20-batch-03.2, LED-2026-10-20-batch-03.3
- **Statement:** `taskboard/views.py` (NEW — created in increment 002) shall provide `present_all_export(board, today, width, height, folded, anchor) -> tuple[Text, int, int]`: the timeline width view 3 draws (`width - PRESENT_RAIL_W - 1` from `PRESENT_RAIL_MIN`, else `width`), `_all_timeline` laid out around `anchor` (the cursor's project as the screen draws it, so the overflow folds match the screen's) and drawn with no cursor, its rows cut after the last whose plain text is not blank, returned as the Text, the width and the rows; `PresentScreen.action_export` shall, in view 3, export that with its row count as the height.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_present_backlog_round.py -k TC_2404`
- **Numeric pass threshold:** TC-2404: Client A at 118×29 → 93 cells × 21 rows, no `⟦`, no `project span`, the last row not blank; a folded project exports folded; the main board of `multi_board_fixture` at 118×29 → 29 rows (it fills the frame); an overflowing board anchored on its last project → the same projects folded as the screen with the cursor there.
- **Negative control:** TC-2404 goes RED when the cut drops a content row, when the cursor is kept, when the height passed is the frame's (increment 002's battery — planned).
- **Boundary catalog:** ☑ boundary (a full frame) ☑ empty (no shown project) ☐ invalid — none ☐ error — none

### LLR-2405.1 — the `K`/`J` hint wordings
- **Traceability:** HLR-2405
- **Ledger:** LED-2026-10-20-batch-03.1, LED-2026-10-20-batch-03.2, LED-2026-10-20-batch-03.3, LED-2026-10-20-batch-03.5
- **Statement:** view 3's wordings in `PresentScreen._hint` shall read, with the rail: `⇥ next · ↑↓ move · ←→ rail/timeline · ␣ hide · ⇧↑↓/K J reorder · enter fold · a show all · x export · esc leave`, `⇥ · ↑↓ · ←→ rail · ␣ hide · K J order · enter fold · a all · x · esc`, `⇥ ↑↓ ←→ ␣ K J enter a x esc`, `esc`; without it the same with `⇥ next · ←→ ↑↓ move` / `⇥ · ←→ ↑↓` / `⇥ ←→ ↑↓` in place of the moves; the bindings are the seat's (LLR-2403.1).
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_present_backlog_round.py -k TC_2405`
- **Numeric pass threshold:** TC-2405: with no label, at 160 columns view 3's hint holds `⇧↑↓/K J reorder`, at 118 `K J order`, at 80 `K J`; with the label (`Client A`, `sky`) each width's wording holds `K J` too (architect A-14).
- **Negative control:** TC-2405 goes RED when a wording drops `K J` (increment 002's battery — planned).
- **Boundary catalog:** ☑ boundary (each wording's width) ☐ empty — none ☐ invalid — none ☐ error — none

### LLR-2406.1 — `ConfirmModal`'s keys, key line and wrap
- **Traceability:** HLR-2406
- **Ledger:** LED-2026-10-20-batch-03.1, LED-2026-10-20-batch-03.2, LED-2026-10-20-batch-03.3, LED-2026-10-20-batch-03.4
- **Statement:** `ConfirmModal.BINDINGS` shall hold `escape` → `no` and the priority bindings `y` → `press_button('yes')` and `n` → `press_button('no')`; its compose shall yield, after the buttons, `Label(key_line([("y", confirm.lower()), ("n / esc", "cancel"), ("⇥", "the buttons")]), id="confirm-keys")`; `#confirm-box .modal-title` shall be `width: 100%` so the message wraps; `MoveConfirm` shall bind `y` → `yes`, `n`/`escape` → `no` and no `enter`, its foot ending with `key_line([("y", "move[ and drop N links]"), ("n / esc", "cancel")])`; `taskboard/keymap.py` (NEW — created in increment 001) shall provide `key_line(pairs, width=None) -> Text` (each key bold bright, its word muted, pairs three spaces apart, a ` / ` between alternative keys dim; with a width, words dropped from the right, then keys, until it fits) — in `keymap` because the agenda's key row (`app`) and the modals both read it, and `views` may not import `modals`.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_modal_keys.py -k TC_2406`
- **Numeric pass threshold:** TC-2406: `key_line([("y", "archive"), ("n / esc", "cancel")]).plain == "y archive   n / esc cancel"`, the keys' spans bold bright; `key_line(pairs, 20)` keeps every key; the 128-character message at 118×30 takes at least 2 rows and its last word is in the box's text; `y` → True, `n` → False, `escape` → False, `enter` → no answer.
- **Negative control:** TC-2406 goes RED when `y` is unbound, when the wrap rule is dropped, when `key_line` drops a key before every word (increment 001's battery — planned).
- **Boundary catalog:** ☑ boundary (a width under the keys' own) ☐ empty (no pairs: empty) ☐ invalid — none ☐ error — none

### LLR-2407.1 — the form modals' `alt` keys and key lines
- **Traceability:** HLR-2407
- **Ledger:** LED-2026-10-20-batch-03.1, LED-2026-10-20-batch-03.2, LED-2026-10-20-batch-03.3, LED-2026-10-20-batch-03.4, LED-2026-10-20-batch-03.8
- **Statement:** `taskboard/modals.py` (NEW — created in increment 001) shall provide `ButtonKeysMixin.action_press_button(button_id)` (presses that button: the key and the button share one path — architect A-7); `TaskModal`, `ProjectModal`, `TemplateEditor`, `ClockModal` and `TextPrompt` shall bind `alt+s` → `press_button('save')`; `TaskModal` `alt+i` → `press_button('paste-img')`; `TaskModal` and `ProjectModal` `alt+t` → `press_button('cal-f-start')`, `alt+d` → `press_button('cal-f-due')` — all priority (a design choice; no field of Textual 8.2.8 binds `alt+<letter>`, so the priority is not observable — qa QA-13); the four boxed modals shall yield `Label(key_line(...), classes="modal-keys")` after their buttons; `TaskModal` shall yield a one-row `Static(id="task-keys")` last in `#task-box`, its `key_line` fitted to the screen's width on mount and resize; the inventory law (`tests/test_modal_keys.py`) shall enumerate `ModalScreen` subclasses of `taskboard.modals` and `taskboard.app` and hold each to its table row.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_modal_keys.py -k TC_2407`
- **Numeric pass threshold:** TC-2407: each of the five modals pushed alone: `alt+s` dismisses with what pressing Save returns; `TaskModal`'s `alt+i` calls the paste (stubbed clipboard: the `No image found` notice); `alt+t`, `alt+d` push `CalendarModal`; the law's table covers every subclass found (a subclass missing from it fails the law); for each row its composed buttons are exactly the row's, each key's result equals its button's, and the modal's screen names every key (ux UX-21).
- **Negative control:** TC-2407 goes RED when a key is unbound, when the key line is dropped, when a modal is missing from the table (increment 001's battery — planned).
- **Boundary catalog:** ☑ boundary (80 columns) ☐ empty — none ☑ invalid (plain letters typed) ☐ error — none

### LLR-2408.1 — the chip in the start-up modals' titles
- **Traceability:** HLR-2408
- **Ledger:** LED-2026-10-20-batch-03.1, LED-2026-10-20-batch-03.2, LED-2026-10-20-batch-03.3
- **Statement:** `MilestoneOffer`'s title shall be `Text.assemble(board_chip_text(board.label), ("◆ Milestones", "bold"), …)` from its `board` (`board_chip_text` carries the one space after the chip — ux UX-23), its title `width: 100%`; `TeamIdentityPicker(roster, label=None)` shall open its title with `board_chip_text(label)`, its words as today, the title `width: 100%` (it wraps) and a key line `key_line([("↵", "pick"), ("esc", "cancel")])` under its list; `TaskboardApp._init_team_mode` shall pass `self.board.label`.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_boards_backlog_round.py -k TC_2408`
- **Numeric pass threshold:** TC-2408: `MilestoneOffer` of a board labelled (`Client A`, `sky`) → its title plain starts ` Client A  ◆ Milestones`; label None → starts `◆ Milestones`; `TeamIdentityPicker(roster, ("Course", "violet"))` → ` Course  Operator identity`; a name holding `[b]` is printed as typed.
- **Negative control:** TC-2408 goes RED when the chip is dropped or the app passes no label (increment 003's battery — planned).
- **Boundary catalog:** ☐ boundary — none ☑ empty (no label) ☑ invalid (a markup-looking name) ☐ error — none

### LLR-2409.1 — `boards` presence markers
- **Traceability:** HLR-2409
- **Ledger:** LED-2026-10-20-batch-03.1, LED-2026-10-20-batch-03.2, LED-2026-10-20-batch-03.3, LED-2026-10-20-batch-03.6
- **Statement:** `taskboard/boards.py` (NEW symbols — created in increment 003) shall provide `PRESENCE_STALE = 120.0`, `name_for(path)` (the public name of `_name_for`, architect A-8), `presence_dir() -> Path` (`default_board_path().parent / "open"`), `announce(path, now) -> Path | None` (the folder made, the marker created with `os.open(O_CREAT | O_EXCL | O_WRONLY)` and its JSON written — on a failed write closed and removed — None on any `OSError`), `renew(marker) -> bool` (`os.utime`; False when it is gone), `withdraw(marker)` (removes that one file; errors ignored) and `open_elsewhere(path, mine=None) -> list[datetime | None]` (for each entry of the folder whose whole name `re.fullmatch`es `<this file's 16-hex hash>-<32 hex>.json` and is not `mine`: `os.lstat`, skipped unless `S_ISREG`; more than `PRESENCE_STALE` from now (`abs(time.time() - st_mtime)`) → removed after a second `lstat` shows the same `(st_mtime_ns, st_ino)`, errors ignored; else its `since` from at most 4096 bytes, None for anything but a JSON object holding a parseable string `since` without an offset (an offset-aware time could not be ordered beside the others: security S-13) — `OSError`, `ValueError`, `TypeError`, `AttributeError`, `RecursionError` all read as None; a missing folder → `[]`).
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_boards_backlog_round.py -k TC_2409`
- **Numeric pass threshold:** TC-2409: `announce` twice → two files, distinct tokens, each `{"since": "2026-10-20T09:30", "pid": …}`; `open_elsewhere(p, first)` → `[09:30]`; aged 121 s → `[]` and removed; aged 119 s → counted; future-dated by 121 s → stale; a non-JSON marker, `[]`, `{"since": 5}`, `{"since": null}`, a 10 MB file → `[None]` each; a directory and `other.json` under `open/` untouched; `withdraw` removes only its file; `announce` with `os.open` raising `PermissionError` → None; with `os.write` raising → None and no file; `name_for` equals the registry's naming.
- **Negative control:** TC-2409 goes RED when staleness is ignored, when `mine` is counted, when another board's marker is counted, when a stale marker is kept (increment 003's battery — planned).
- **Boundary catalog:** ☑ boundary (119/121 s; a future time) ☑ empty (no folder) ☑ invalid (not JSON; a directory; a foreign name) ☑ error (unwritable)

### LLR-2409.2 — the presence lifecycle and the notice
- **Traceability:** HLR-2409
- **Ledger:** LED-2026-10-20-batch-03.1, LED-2026-10-20-batch-03.2, LED-2026-10-20-batch-03.3
- **Statement:** `TaskboardApp` shall hold `_presence: Path | None`; at the end of a successful `_open_board` it shall read `open_elsewhere(board.path)`, withdraw its previous marker, `announce` the board and, when others exist, notify HLR-2409's text with `markup=False`, `severity="warning"`, `timeout=30` (the board's name: its registry entry's, else `boards.name_for` of the file; `f"{t:%H:%M}"` of the earliest `since`, `f"{t:%b} {t.day} {t:%H:%M}"` when not today); `_tick` shall `renew` the marker every 30 ticks and `announce` again when it is gone; `on_unmount` shall `withdraw` it.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_boards_backlog_round.py -k TC_2409`
- **Numeric pass threshold:** TC-2409 (app): a failed switch (its migration stopped) keeps the old board's marker; 30 ticks after its marker is deleted by hand, a new one exists; the notice's severity is `warning` and its title `Boards · open twice`; the suites that run two apps on one board in one process are censused for notices they now see (`grep -n "_notifications\|notify"`, architect A-12).
- **Negative control:** TC-2409 goes RED when the marker is not withdrawn at exit or at a switch, when the notice is shown with no other marker (increment 003's battery — planned).
- **Boundary catalog:** ☐ boundary — none ☐ empty — none ☐ invalid — none ☑ error (the failed switch)

### LLR-2410.1 — `__main__` `--open`
- **Traceability:** HLR-2410
- **Ledger:** LED-2026-10-20-batch-03.1, LED-2026-10-20-batch-03.2, LED-2026-10-20-batch-03.3
- **Statement:** `main()` shall add `--open PATH` in a mutually exclusive group with `--board`; right after `parse_args()`, before the `--report` branch, it shall refuse a `--open` path that is not a regular file parsing to a JSON object (`~` read through `boards.expand_home`, the public name of `_expand_home` — architect A-19) with `parser.exit(2, "taskboard: no board file at <PATH, control characters stripped> (--open opens an existing one)\n")`; `open_app(board, unlisted=None)` shall, for `unlisted`, load the registry and build `TaskboardApp(board_path=<the expanded path>, registry=registry)` with no `register` and no `touch`; `--report` shall read `args.board or args.open`.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_boards_backlog_round.py -k TC_2410`
- **Numeric pass threshold:** TC-2410: `open_app(None, copy)` leaves `boards.json`'s bytes; `main()` with a missing `--open` path → exit 2, the message, nothing created; with `--report` too → the same; a folder or a text file → exit 2; a path holding an `ESC` byte → printed without it; both options → exit 2 with `not allowed with argument`.
- **Negative control:** TC-2410 goes RED when `open_app` registers or touches, when the missing path is opened (increment 003's battery — planned).
- **Boundary catalog:** ☑ boundary (a registered path) ☐ empty — none ☑ invalid (missing; both) ☐ error — none

### LLR-2410.2 — the unlisted board in the app
- **Traceability:** HLR-2410
- **Ledger:** LED-2026-10-20-batch-03.1, LED-2026-10-20-batch-03.2, LED-2026-10-20-batch-03.3, LED-2026-10-20-batch-03.6, LED-2026-10-20-batch-03.8, LED-2026-10-20-batch-03.9
- **Statement:** with `board_id` None (no registry entry for the open file), `_label_board` shall set the label `(<boards.name_for(path)> · not listed, "pink")`, `on_mount` shall not push the home and shall notify HLR-2410's text with `markup=False`, `timeout=15` (the path with its control characters stripped), and `ProjectPicker.action_move_board` shall refuse with HLR-2410's text before listing targets.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_boards_backlog_round.py -k TC_2410`
- **Numeric pass threshold:** TC-2410 (app): the label of an app built on an unlisted file is (`board-copy · not listed`, `pink`) with one or three active boards; `switch_board` from it to Personal works and the label becomes `Personal`'s; an unlisted file named `[x]copy.json` (a `/` cannot name a Windows file) → the label and the notice hold `[x]copy` as typed, the notice `markup=False`, nothing raised; `--open` of a registered board's own file → that board, its own chip, `boards.json` unchanged.
- **Negative control:** TC-2410 goes RED when the label is None, when the home opens at start, when the move is offered (increment 003's battery — planned).
- **Boundary catalog:** ☐ boundary — none ☑ empty (one registered board) ☐ invalid — none ☐ error — none

### Information Flow Contract (IFC) — C-54

> Part A in every batch; Part B when the system's boundary has components a consumer can address independently. The block syntax, its fields and the rules that read them are in `templates/ifc-template.md`, which ships with the flow and is not copied into this batch.

- **Part A — flows:**

```
FLOW: every board's dues, from the board files to the agenda screen
  SOURCE : A on the main screen
  NODES  :
    - fn    : views.agenda_buckets, all_agenda, render_all_agenda
      owner : LLR-2401.1
    - fn    : app.AllBoardsAgenda, TaskboardApp.action_agenda_all, check_action; keymap.KEYMAP
      owner : LLR-2401.2
  SINK   : the screen; on enter the main screen with the task's board open
```

```
FLOW: a presentation key, from the seat to the screen and the export
  SOURCE : R, then a key
  NODES  :
    - fn    : views.board_chip_text; app.PresentScreen._hint
      owner : LLR-2402.1
    - fn    : keymap.PRESENT_KEYS, present_bindings
      owner : LLR-2403.1
    - fn    : modals.PresentKeys; app.PresentScreen.action_keys
      owner : LLR-2403.2
    - fn    : views.present_all_export; app.PresentScreen.action_export
      owner : LLR-2404.1
    - fn    : app.PresentScreen._hint (view 3's wordings)
      owner : LLR-2405.1
  SINK   : the hint row, the keys window, reports/present-*-all.svg|png, board.json (present_rank)
```

```
FLOW: a modal's button, from a key to its action
  SOURCE : y, n, alt+s, alt+i, alt+t, alt+d, esc inside a modal
  NODES  :
    - fn    : modals.key_line, ConfirmModal
      owner : LLR-2406.1
    - fn    : modals.TaskModal, ProjectModal, TemplateEditor, ClockModal, TextPrompt
      owner : LLR-2407.1
  SINK   : the modal's answer to its caller
```

```
FLOW: a board opened, from the start or a switch to the notices and the presence folder
  SOURCE : taskboard (--open PATH), the home's enter, the agenda's enter
  NODES  :
    - fn    : modals.MilestoneOffer, TeamIdentityPicker; app.TaskboardApp._init_team_mode
      owner : LLR-2408.1
    - fn    : boards.announce, renew, withdraw, open_elsewhere
      owner : LLR-2409.1
    - fn    : app.TaskboardApp._open_board, _tick, on_unmount
      owner : LLR-2409.2
    - fn    : __main__.main, open_app
      owner : LLR-2410.1
    - fn    : app.TaskboardApp._label_board, on_mount; modals.ProjectPicker.action_move_board
      owner : LLR-2410.2
  SINK   : the start-up modals' titles, the notices, ~/.taskboard/open/, boards.json (untouched by --open)
```

- **Part B — boundary decomposition:** `no — every flow is the app's own, addressed through its keys and its command line`

---

## 5. Validation strategy

### 5.1 Methods

> **Two layers** (per the Two-layer validation rule). Every batch declares BOTH:
> - **Layer A — white-box / functional (`TC-NNN`):** validates the HLR/LLR mechanism (the HOW). Methods: `test`, `inspection`, `analysis`.
> - **Layer B — black-box / behavioral acceptance (`AT-NNN`):** validates the user story's outcome through the shipped surface (the WHAT). Method: `acceptance`.

Layer 0: `key_line`'s fit, `agenda_buckets`/`all_agenda`, `present_all_export`'s cut, the presence functions (TC-2401, TC-2404, TC-2406, TC-2409). Layer A: TC-2401..TC-2410 at the screen and function level. Layer B: AT-2401..AT-2410 drive the real app headless (`run_test`, keys) built by the shipped `open_app`/`main` or `TaskboardApp` on the round's synthetic boards under the seam home, reading the screen's text, the notices and the files; "another window" is a second `TaskboardApp` in the same process on the same files — the code a second process runs. Real-app captures at 118×30 and 80×24 of each item go to `evidence/captures/` (Windows Terminal PNGs, the round's capture method).

### 5.2 Batch acceptance criteria
- every LLR has a passing TC; every story a passing AT through its surface;
- every new assertion RED on `base_ref` or by a recorded mutation; mutants KILLED on the new logic;
- the full suite in three sequential chunks: 0 failures; transcripts under the batch's evidence; 2962 + the new nodes;
- no presence marker left by any test that let its app exit;
- no test reads or writes the real home.

---

## 6. Appendices (optional)

### 6.1 Extended glossary
### 6.2 Relevant design decisions
See `PLAN.md` §Key decisions (D-1..D-12) and `docs/ARCHITECTURE.md` (amended by this batch: the agenda screen, the presentation's key seat, the presence markers, `--open`).
### 6.3 Open risks
- **Security questions (the P1 scan):** `devflow-scan-spec.py` over this document, 2026-10-20: 65 patterns, 5 control rows ok, `flags: token, hash, migration, form, escape`, `security_required: true`, exit 1 (`evidence/scan-p1.txt`). The answers: `token` and `hash` (C5, C6) — the presence marker's name is a SHA-256 prefix of the board file's key (a name, not a secret: it only groups one file's markers) and a random `os.urandom` token (uniqueness, not authentication; a marker grants nothing and is read only to warn); the marker holds the local time and the process id, never a path, a board's content or the operator's name. `migration` names the existing link migration a failed switch keeps (no new migration). `form` names the modal forms that gain keys (no new field, no new input path; `alt+<letter>` keys act on what their buttons already do). `escape` (C6/C8) — every new screen text read from a board or the registry (the agenda's titles, projects and names, the chips in the hint row and the start-up titles) is a plain Text piece cut with `fit`, never parsed as markup (S1); a markup-looking title is printed as typed (TC-2401, TC-2408); the two new notices are `markup=False` (TC-2409, TC-2410). The batch's real file and input surfaces, judged with it: the presence folder `~/.taskboard/open/` — the app creates its own marker exclusively, removes only its own by path, and removes another window's only when it is a regular file of this board's name pattern not renewed for 120 s (C5: an `unlink` of a marker name only, never of a board, registry, history or lock file); `--open PATH` reads a file the operator names, as `--board` does, refuses a missing one instead of letting the loader seed it, and writes `boards.json` never. No credential, network, permission or schema change. The security-reviewer reads the markers and `--open` at P2 and at increment 003.
- **The black window (logged, not fixed):** real Windows Terminal draws a black window after opening `Personal` or `Course` (`prototypes/backlog_round/out/png/black/`); the agenda's `enter` can land there. The orchestrator investigates it apart; captures that land on those boards may show it.
- **A presence marker outlives a crash for up to 120 s**: a window opened in that time warns of a window that is gone. Accepted (the stale rule; no liveness probe on Windows).
- **A window suspended longer than 120 s** (a sleeping laptop) stops renewing: a second window opened then is not warned. Accepted.
- **`alt+<letter>` in terminals that send `alt` as a menu key**: Windows Terminal passes it (P-10 reads the parser, not the terminal); the key line keeps `esc` and the buttons reachable by `tab` as today.
- **The agenda reads every board at open** (`peek_board`): with many large boards the open costs one read each, once (no latency criterion).
- **`esc` then a letter typed fast** is read by the parser as `alt+<letter>` (P-10's rule): in a form `esc`, `s` inside one read would save instead of cancel (architect A-15, ux). Rare with human typing; accepted.
- **Caps Lock in the presentation:** `k`/`j` become `K`/`J` and reorder in front of the room (saved; the opposite key undoes it), and `a` becomes `A` on the main screen (ux UX-19). Accepted.
- **Lanes are not capped** (ux UX-10): with very many boards the agenda's list keeps few rows at 24 rows; a scrolling lane strip is out of scope.
- **`--open` opens read-write** (architect A-2): its start may write the file (the migrations' marks); a read-only open is an item for the operator in `BACKLOG.md`.
- **`--report --board <missing>` seeds a board at that path** (security S-3, pre-existing): logged in `BACKLOG.md`; `--open` refuses it.

### 6.4 Phase-1 reconciliation log — moved to the ledger (§7)

### 6.5 Requirement amendments — moved to the ledger (§7)

---

## 7. The ledger — authored as a SEPARATE FILE

The fence below is the ledger's seed: `devflow-init.py` writes it to `01-requirements-ledger.md`. The shape of an entry is in the field guide.

```markdown
# Requirements ledger — taskboard — Batch 2026-10-20-batch-03

> Append-only. Entries are added in chronological order and never rewritten. The live
> contract is `01-requirements.md`; this file records how it came to say what it says.
> Every entry names the requirement it amends; every requirement names its entries. `V26`
> compares the two sets of pairs both ways.

_No entries yet. The first amendment to the live contract writes the first one, in the
shape the field guide's §7 shows (`req-template.part2.md` in the guide directory init prints), and nothing
above this line is ever edited._
```
