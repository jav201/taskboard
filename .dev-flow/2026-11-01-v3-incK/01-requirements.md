# Requirements — taskboard — Inc K, the capture view (dev-flow-v3-beta)

> Strict EARS (five forms only), ISO/IEC/IEEE 29148. One `shall` per requirement. Each LLR carries a
> numeric pass threshold and a negative control (*NC*: a mutant that turns its test RED). Ids continue
> the repo's sequence in a fresh block: US-4401, HLR-4401..4409, LLR-4401.n..4409.n, TC-44nn/45nn/46nn,
> AT-4401..4408.
> Base: `545c18a` (branch `feat/capture-list-colour`, Inc C and Inc L done). Commission:
> `.dev-flow/COMMISSION-capture-list-colour.md` §Inc K (K-1..K-6). Rulings: `00-orchestrator-rulings.md`
> (R0-1..R0-11) and the E2a amendments R1-1..R1-6, followed; where E1 proposes a change, see §8 Findings. Design source: the round's
> variant A (`prototypes/capture_round/proto.py` `PadScreen`, `Inbox`, `dump`, `undo_dump`, `hit_text`,
> `options`; `out/png/cap-A*_118x30.png`), variant C's review (`ReviewScreen`, `cap-C-rev_118x30.png`)
> and `prototypes/capture_round/suggest.py`.
> **TC numbering (no collisions):** LLR-4401.n → TC-(4400+n); LLR-4402.n → TC-(4430+n);
> LLR-4403.n → TC-(4460+n); LLR-4404.n → TC-(4500+n); LLR-4405.n → TC-(4540+n);
> LLR-4406.n → TC-(4560+n); LLR-4407.n → TC-(4580+n); LLR-4408.n → TC-(4610+n);
> LLR-4409.n → TC-(4630+n). Each block's n stays below its next block's base (4401: n ≤ 29,
> 4402: ≤ 29, 4403: ≤ 39, 4404: ≤ 39, 4405: ≤ 19, 4406: ≤ 19, 4407: ≤ 29, 4408: ≤ 19, 4409: ≤ 19).
> Overflow (R2): LLR-4407.n with n ≥ 30 → TC-(4640+n), i.e. TC-4670..TC-4699.
> A second test of one LLR adds a letter (TC-4504b). The block TC-4401..TC-4699 is reserved for Inc K.

## 1. Scope

**In:** a full-screen capture view on `n` (pad + suggestion rail, A); the `____` divider, its rule
rendering, the note count, the divider key `alt+l` (R1-1), the hint row, the ghost example and the one-time notice (K-2);
deterministic TF-IDF project suggestions over every board (K-3); dump of the cursor's note, the
alternatives cycle, the inline new project, undo, the 7-day keep of dumped notes (K-4); the batch review
list on `alt+a` (C); the global store `inbox.json` written like `people.json` (K-5); images attached to a
note and moved on dump (K-6); colour spans shown live in the pad and carried into the task; the key-seat
wiring (`keymap.py`, `check_action`, README row).
**Not in:** pens or the colour palette inside the pad (`alt+1..6`, `alt+c`: Inc C's editor keys, not in
K-1..K-6 — §8 F-10); any change to `Board.add_task`, `history.jsonl`, the board file format, `people.json`
or `marks.json`; atomic board writes for the open board (the app's existing `save()` path stays); a
any `alt+enter` binding (R1-1: Windows Terminal cannot deliver it to Textual 8.2.8); a dump into a board that is not in the registry and not open; any
new dependency.

**Definitions.**

| Term | Meaning |
|---|---|
| capture view | the screen `n` opens (working name `CaptureView`), a `Screen`, not a modal |
| pad | the capture view's text area (working name `PadArea`, an `InkArea` subclass) |
| divider line | a pad line whose text, trailing whitespace removed, is 4 or more `_` and nothing else (R0-3) |
| part | the lines between two divider lines, or between a divider line and the pad's start or end |
| note | a part holding at least one non-whitespace character; its text is the part's lines with leading and trailing blank lines removed |
| cursor's note | the note holding the cursor's line; on a divider line, the note above it; none when the cursor's part is not a note |
| image line | a note line that, stripped, is `img: ` followed by a name with no `/`, `\`, `:` or control character, not `.` or `..`, whose lower-case suffix is in `models.IMAGE_EXTS` |
| title line | the note's first line that is not an image line and whose visible text (`modals.visible_text`) is not blank |
| store | `inbox.json` beside the boards registry: `app.registry.path.parent / "inbox.json"` (the home's `~/.taskboard/inbox.json`) |
| pad images folder | `inbox-images/` beside the store (R0-9) |
| store stamp | the store file's (mtime, size) as of this app's last read or write of it; the file "changed" when its stamp differs |
| flagged note | a note whose dump saved its board but whose store write then failed (R2 F-12); kept in the pad, marked, never dumped again |
| board order | the order `app.board_lanes` returns the boards in (registry order, the unlisted `--open` board last) |
| readable board | a lane whose board is not None (file present and readable) |
| document | one non-archived project of a readable board, as a bag of weighted stems (K-3) |
| hit | (document, score, why) for one note; score is the cosine, halved on a single shared stem, rounded to 4 decimals |
| cuts | HIGH 0.30, MID 0.16, LOW 0.08 (suggest.py) |
| options | a note's top choice followed by its alternatives (at most 3 entries); `+ new project` is the option None |
| chosen option | the option `alt+o` / `o` currently selects for a note (starts at the top choice) |
| dump | turning one note into one task on its chosen option's project and board |
| dumped entry | the record of a dump kept in the store's `dumped` list |
| stamp | `models.stamp()`: local time, `YYYY-MM-DDTHH:MM:SS` |

## 2. Source user story

**US-4401.** As the board's owner (`username_subject`), I want one key that opens a focused notes pad where
I type during a meeting, separate notes with a `____` line, and turn each note into a task in the project
the pad suggests — with the words that matched, on any board, or in a new project made right there — so
that what I jot down reaches the taskboard without a setup dialog. (Operator verdict 1: A + C in its own
focused view, plus the `____` divider; D1 one global inbox; D2 TF-IDF explained.)

## 3. High-level requirements

### HLR-4401 — a focused capture view on `n` (K-1, variant A)
- **Traceability:** US-4401 · K-1 · verdict 1 · R0-1 · R0-2
- **Ledger:** LED-2026-11-01-incK.1
- **Statement:** When `n` is pressed on the main screen, the system shall open a full-screen capture view that holds the pad and the suggestion rail.
- **Validation:** `test` — `tests/test_capture_view.py` (pilot)
- **Numeric pass threshold:** all LLR-4401.n thresholds at 118x30 and 80x24.
- **Acceptance test(s):** AT-4401
- **Negative control:** base has no `n` binding: AT-4401 RED.

### HLR-4402 — the `____` divider and its three hints (K-2)
- **Traceability:** US-4401 · K-2 · R0-3 · R0-4 · R1-1 · R0-6 · R1-5
- **Ledger:** LED-2026-11-01-incK.1
- **Statement:** The system shall split the pad into notes at divider lines and draw each divider line the cursor is not on as a full-width rule.
- **Validation:** `test` — `tests/test_capture_divider.py` (layer 0 + pilot)
- **Numeric pass threshold:** all LLR-4402.n thresholds.
- **Acceptance test(s):** AT-4401
- **Negative control:** split at blank lines (the proto's rule): TC-4433 RED.

### HLR-4403 — deterministic suggestions over every board (K-3, D2)
- **Traceability:** US-4401 · K-3 · D2 · R0-7
- **Ledger:** LED-2026-11-01-incK.1
- **Statement:** The system shall suggest, for each note, the project of any readable board whose TF-IDF document best matches the note, with the matched words as the reason.
- **Validation:** `test` — `tests/test_suggest.py` (layer 0) + `tests/test_capture_view.py -k rail` (pilot)
- **Numeric pass threshold:** all LLR-4403.n thresholds; identical output on 3 repeated runs over the fixture.
- **Acceptance test(s):** AT-4402
- **Negative control:** name weight ×2 instead of ×3: TC-4464 RED.

### HLR-4404 — dump, alternatives and the inline new project (K-4)
- **Traceability:** US-4401 · K-4 · R0-2 · R0-8 · R1-3
- **Ledger:** LED-2026-11-01-incK.1
- **Statement:** When `alt+d` is pressed with the cursor in a note, the system shall turn that note into one task on its chosen option's project, stamped with `created`, and remove the note from the pad.
- **Validation:** `test` — `tests/test_capture_dump.py` (layer 0 + pilot)
- **Numeric pass threshold:** all LLR-4404.n thresholds.
- **Acceptance test(s):** AT-4402, AT-4403
- **Negative control:** save the target board from the snapshot read at open: TC-4509 RED.

### HLR-4405 — undo and the 7-day keep of dumped notes (K-4)
- **Traceability:** US-4401 · K-4 · R0-2 · R1-4
- **Ledger:** LED-2026-11-01-incK.1
- **Statement:** When `alt+u` is pressed in the pad, the system shall undo the newest dump that the store keeps.
- **Validation:** `test` — `tests/test_capture_dump.py -k undo`
- **Numeric pass threshold:** all LLR-4405.n thresholds.
- **Acceptance test(s):** AT-4404
- **Negative control:** undo the oldest entry: TC-4541 RED.

### HLR-4406 — the batch review list (K-1, variant C)
- **Traceability:** US-4401 · K-1 · verdict 1 · R0-2
- **Ledger:** LED-2026-11-01-incK.1
- **Statement:** When `alt+a` is pressed in the pad, the system shall open a review list with one row per note from which the checked notes are dumped together.
- **Validation:** `test` — `tests/test_capture_review.py` (pilot)
- **Numeric pass threshold:** all LLR-4406.n thresholds.
- **Acceptance test(s):** AT-4405
- **Negative control:** `d` dumps unchecked rows too: TC-4568 RED.

### HLR-4407 — the inbox store (K-5, D1)
- **Traceability:** US-4401 · K-5 · D1 · R0-6 · R0-10
- **Ledger:** LED-2026-11-01-incK.1
- **Statement:** The system shall keep the pad, the dumped entries and the divider-notice flag in the store, written as `people.json` is written: read-modify-write under `boards.file_lock`, atomic, set aside with `boards.keep_aside` when unreadable, re-read fresh when changed.
- **Validation:** `test` — `tests/test_inbox_store.py` (layer 0 + pilot)
- **Numeric pass threshold:** all LLR-4407.n thresholds.
- **Acceptance test(s):** AT-4406, AT-4408
- **Negative control:** write the in-memory store without the fresh read: TC-4584 RED.

### HLR-4408 — images on a note (K-6)
- **Traceability:** US-4401 · K-6 · R0-9 · R1-2
- **Ledger:** LED-2026-11-01-incK.1
- **Statement:** When `alt+i` is pressed with the cursor in a note, the system shall attach the clipboard's image to that note, and when the note is dumped, the system shall move its images into the task's folder on the target board.
- **Validation:** `test` — `tests/test_capture_images.py`
- **Numeric pass threshold:** all LLR-4408.n thresholds.
- **Acceptance test(s):** AT-4402, AT-4407
- **Negative control:** move the user's own clipboard file instead of copying it: TC-4613 RED.

> HLR-4408 holds two `shall`s joined by the K-6 sentence; its LLRs split them (attach: LLR-4408.2..4408.7;
> move: LLR-4408.10..4408.17). Self-check note, LED-2026-11-01-incK.1.

### HLR-4409 — colour, mentions and untrusted text carried safely
- **Traceability:** US-4401 · K-4 ("images, `@mentions` and colour spans carry over") · Inc C
- **Ledger:** LED-2026-11-01-incK.1
- **Statement:** The system shall carry every colour span and `@mention` of a note into the dumped task's notes verbatim and draw all note, project and board text as literal text.
- **Validation:** `test` — `tests/test_capture_view.py -k colour or markup`
- **Numeric pass threshold:** all LLR-4409.n thresholds.
- **Acceptance test(s):** AT-4407
- **Negative control:** `Text.from_markup(title)` in the rail: TC-4634 RED.

## 4. Low-level requirements

### 4.1 The view and its keys (HLR-4401)

- **LLR-4401.1 — Ubiquitous.** The keymap shall declare `n` as one global key (action `capture`, label `Capture`, `bar=False`, no `views` scope) placed directly after the `N` entry.
  Threshold: exactly 1 `KEYMAP` entry whose `keys` is `"n"`; `bar is False`; `views is None`; its index = index of `N` + 1; the key-law tests in `tests/test_keymap.py` stay GREEN; 5/5. *NC:* entry missing: RED. **TC-4401**
- **LLR-4401.2 — Event.** When `n` is pressed on the main screen, the system shall open the capture view.
  Threshold: `isinstance(app.screen, CaptureView)` after `n`; 1/1. *NC:* unbound: RED. **TC-4402**
- **LLR-4401.3 — Event.** When a printable key is typed in the pad, the system shall insert that character at the cursor.
  Threshold: typing `nNAqjkhlBuv@#?;` (each a global key elsewhere) into an empty pad gives the pad text `nNAqjkhlBuv@#?;` exactly; `app.screen` is still the capture view; 0 board writes; 3/3. *NC:* `CaptureView` left out of `check_action`'s holding tuple so the priority `j`/`k` reach `cursor`: arm 1 RED. **TC-4403**
- **LLR-4401.4 — Event.** When `esc` is pressed in the pad while the new-project name field is closed, the system shall close the capture view.
  Threshold: the main screen is `app.screen`; 1/1. *NC:* `esc` unbound: RED. **TC-4404**
- **LLR-4401.5 — Ubiquitous.** The capture view shall focus the pad with the cursor at the end of its text when it opens.
  Threshold: `app.focused` is the pad; `cursor_location == document.end`; 2/2. *NC:* cursor at (0, 0): arm 2 RED. **TC-4405**
- **LLR-4401.6 — Ubiquitous.** The capture view shall fill the pad with the store's `pad` text when it opens.
  Threshold: store `pad` = `"a\n____\nb"` → pad text equal; 1/1. *NC:* start empty: RED. **TC-4406**
- **LLR-4401.7 — State.** While the screen is at least 100 cells wide, the capture view shall place the rail in a 50-cell column to the right of the pad.
  Threshold: at 118x30 the rail's region has `x = 68` and `width = 50`, the pad's region `x = 0`; 2/2. *NC:* rail below the pad: RED. **TC-4407**
- **LLR-4401.8 — State.** While the screen is narrower than 100 cells, the capture view shall place the rail below the pad, 7 rows high, showing the cursor's note only.
  Threshold: at 80x24 the rail's region starts below the pad's last row, `height = 7`, and holds exactly 1 note title (the cursor's) out of 3 notes; 3/3. *NC:* all notes in the narrow rail: RED. **TC-4408**
- **LLR-4401.9 — Ubiquitous.** The capture view's head row shall read `CAPTURE  <n> notes · suggestions read every board` (`1 note` for one), clipped to the width.
  Threshold: 3 notes → that plain text exactly at 118x30; 1 note → `CAPTURE  1 note · suggestions read every board`; 2/2. *NC:* fixed `notes`: arm 2 RED. **TC-4409**
- **LLR-4401.10 — Ubiquitous.** The capture view's key row shall show `alt+d dump`, `alt+o other`, `alt+n new project`, `alt+a review`, `alt+i image`, `alt+u undo` and `esc close`, fitted by `keymap.key_line` (words go first, keys never).
  Threshold: at 80x24 all 7 key glyphs present; at 118x30 all 7 words present; 2/2. *NC:* omit `alt+u`: RED. **TC-4410**
- **LLR-4401.11 — Unwanted.** If a modal screen is on the screen stack, then the system shall refuse the `capture` action.
  Threshold: `app.check_action("capture", ())` is False with a `ModalScreen` on the stack and True with none; `n` typed in the task editor's title opens no capture view; 3/3. *NC:* `capture` not gated: arm 1 RED. **TC-4411**
- **LLR-4401.12 — State.** While a capture view is on the screen stack, the system shall refuse every action of the key seat except `quit`, `agenda_all`, `people_directory`, `marks_manager`, `added_list` and `capture`.
  Threshold: with the capture view open, `check_action` is False for `add_task`, `delete`, `cursor`; 3/3. *NC:* `CaptureView` missing from the holding tuple: RED. **TC-4412**
- **LLR-4401.13 — Ubiquitous.** The README key table pinned to the seat shall carry a row for `n`.
  Threshold: `tests/test_keymap.py::test_the_readme_keybinding_table_matches_the_seat` GREEN with the `n` entry; 1/1. *NC:* no README row: that test RED. **TC-4413**
- **LLR-4401.14 — Event.** When `n` is pressed on the list view (`N`) or on the agenda of every board (`A`), the system shall bring the capture view to the top.
  Threshold: from each, `n` → `app.screen` is a capture view and exactly 1 capture view is on the stack (twice `N`,`n`); 3/3. *NC:* `capture` not in `check_action`'s always-allowed tuple: RED. **TC-4414**
- **LLR-4401.15 — Ubiquitous.** The system shall leave the `n` bindings of the boards home, the people directory and the marks manager acting as they act at `545c18a`.
  Threshold: `n` in each opens its own new-board / add-person / add-class form, and no capture view; 3/3. *NC:* the app's `n` made a priority binding: RED. **TC-4415**
- **LLR-4401.16 — Unwanted.** If the pad holds no note, then the rail shall read `no notes yet`.
  Threshold: empty pad → rail plain text `no notes yet`; 1/1. *NC:* blank rail: RED. **TC-4416**

### 4.2 The divider and its hints (HLR-4402)

- **LLR-4402.1 — Ubiquitous.** The system shall treat a pad line as a divider line exactly when that line, with trailing whitespace removed, is four or more `_` characters and nothing else.
  Threshold: `____`, `________`, `____  ` → divider; `___`, ` ____`, `____x`, `__ __` → not; 7/7. *NC:* `_{3,}`: arm `___` RED. **TC-4431**
- **LLR-4402.2 — Ubiquitous.** The system shall split the pad into parts at its divider lines.
  Threshold: `"a\nb\n____\nc"` → parts `["a\nb", "c"]`; `"a\n____\n____\nb"` → 3 parts, the middle one empty; 2/2. *NC:* keep divider lines inside parts: RED. **TC-4432**
- **LLR-4402.3 — Ubiquitous.** The system shall keep blank lines inside a note.
  Threshold: `"a\n\nb\n____\nc"` → 2 notes, the first `"a\n\nb"`; 1/1. *NC:* blank line splits (proto `split_topics`): 3 notes: RED. **TC-4433**
- **LLR-4402.4 — Unwanted.** If a part holds only whitespace, then the system shall not count it as a note.
  Threshold: `"____\n  \n____\na"` → 1 note; 1/1. *NC:* every part a note: RED. **TC-4434**
- **LLR-4402.5 — Ubiquitous.** The system shall take a note's text as its part's lines with leading and trailing blank lines removed.
  Threshold: `"\n\na\n\n____"` → note text `"a"`; 1/1. *NC:* no trim: RED. **TC-4435**
- **LLR-4402.6 — State.** While the cursor is not on a divider line, the pad shall draw that line as a rule of `─` across the pad's full content width.
  Threshold: at 118x30 and at 80x24, the screen row of that line holds `─` in every content cell of the pad (count = the pad's content width) and no `_`; 2/2. *NC:* draw the raw underscores: RED. **TC-4436**
- **LLR-4402.7 — State.** While the cursor is on a divider line, the pad shall draw that line's raw text.
  Threshold: cursor on the line → its row holds `____` and no `─`; 1/1. *NC:* always the rule: RED. **TC-4437**
- **LLR-4402.8 — Ubiquitous.** The note count shall count every note plus the pad's last part when that part holds at least one line, holds only whitespace and follows a divider line (the note being started, R2 F-4).
  Threshold: `"a\n____"` → 1; after `enter` (`"a\n____\n"`) → 2; `"a\n____\n\n____\nb"` → 2 (an inner empty part is not counted); `"a"` → 1; empty pad → 0; 5/5. *NC:* count notes only: arm 2 RED. **TC-4438**
- **LLR-4402.9 — Event.** When `alt+l` is pressed in the pad, the system shall insert a divider line `____` after the cursor's line and put the cursor at the start of a new empty line after it.
  Threshold: `"abc"`, cursor (0, 1), `alt+l` → text `"abc\n____\n"`, cursor (2, 0); with a following line `"abc\nd"` → `"abc\n____\n\nd"`, cursor (2, 0); 2/2. *NC:* insert at the cursor, splitting the line: RED. **TC-4439**
- **LLR-4402.10 — Unwanted.** If the cursor's line is blank when `alt+l` is pressed, then the system shall write `____` on that line and put the cursor at the start of a new empty line after it.
  Threshold: `"a\n"`, cursor (1, 0) → `"a\n____\n"`, cursor (2, 0); 1/1. *NC:* a blank line kept above the divider: RED. **TC-4440**
- **LLR-4402.11 — Ubiquitous.** The capture view shall show one hint row whose plain text is `____ ↵ new note · alt+l divider` (R1-1; the commission's `alt+↵` cannot reach the app) in every state of the view.
  Threshold: the row's plain text equals that string at 118x30 and 80x24, with an empty pad, with 3 notes and with the name field open; 4/4. *NC:* hide the row once a divider exists: RED. **TC-4441**
- **LLR-4402.12 — State.** While the pad is empty, the pad shall show the ghost example as four dimmed placeholder lines: `first line → the task's title`, `next lines → its notes`, 24 `─`, `____ ↵ starts the next note`.
  Threshold: empty pad → the 4 lines present in that order; after typing one character → none of them; 2/2. *NC:* no rule line: arm 1 RED. **TC-4442**
- **LLR-4402.13 — Event.** When a divider line is first drawn as a rule while the store's divider-notice flag is not set, the system shall show the notice `That ____ line divides notes: the text above and below it dump as two tasks. alt+l inserts one.`
  Threshold: exactly 1 notification with that text, title `Capture`, `markup=False`; a second divider in the same session → still 1; 2/2. *NC:* notice on every divider: arm 2 RED. **TC-4443**
- **LLR-4402.14 — Event.** When the divider notice is shown, the system shall set `divider_notice` to true in the store.
  Threshold: the store read back holds `"divider_notice": true`; 1/1. *NC:* a session flag only: RED. **TC-4444**
- **LLR-4402.15 — Unwanted.** If the store's `divider_notice` is true, then the system shall not show the divider notice.
  Threshold: a new app instance on a store with the flag, a divider made → 0 notices; 1/1. *NC:* ignore the stored flag: RED. **TC-4445**
- **LLR-4402.16 — Ubiquitous.** The system shall keep a divider line's text as typed, in the pad and in the store.
  Threshold: `______` typed → pad text and stored `pad` both hold `______`; 1/1. *NC:* normalise to `____`: RED. **TC-4446**
- **LLR-4402.17 — Ubiquitous.** The capture view shall bind no `alt+enter` key.
  Threshold: no binding of `CaptureView`, `PadArea` or `ReviewList` names `alt+enter`; `alt+enter` pressed in the pad (pilot) inserts no divider line; 2/2. *NC:* `alt+enter` bound as an alias: arm 1 RED. **TC-4447**
- **LLR-4402.18 — Ubiquitous.** The pad shall draw the divider rule by its own line rendering, never through the colour highlight map (R1-5).
  Threshold: `PadArea`'s highlight map holds no entry for a divider row; the rule's cells are `─` glyphs, not styled `_`; 2/2. *NC:* a highlight style on the underscores: arm 2 RED (the row still reads `____`). **TC-4448**

### 4.3 Suggestions (HLR-4403)

- **LLR-4403.1 — Ubiquitous.** The system shall reduce a text to words by folding accents, lower-casing, and taking each `@handle` or run of `[a-z0-9]`, dropping words shorter than 3 characters, bare numbers and the stop words of `suggest.STOP` (the prototype's list).
  Threshold: `Golden SET: 12 Questions @username_subject de la Café` → surface words `golden`, `set`, `questions`, `@username_subject`, `cafe`; 1/1. *NC:* keep numbers: `12` present: RED. **TC-4461**
- **LLR-4403.2 — Ubiquitous.** The system shall stem a word by turning a final `ies` into `y` when the word is longer than 4, dropping a final `s` that is not `ss` when the word is longer than 3, and cutting the result to 6 characters; a handle is not stemmed.
  Threshold: `questions`→`questi`, `stories`→`story`, `class`→`class`, `@username_subject`→unchanged; 4/4. *NC:* cut to 5: RED. **TC-4462**
- **LLR-4403.3 — Ubiquitous.** The system shall build one document per non-archived project of every readable board.
  Threshold: 2 boards holding 3 live projects and 1 archived → 3 documents; 1/1. *NC:* archived included: 4: RED. **TC-4463**
- **LLR-4403.4 — Ubiquitous.** The system shall weight a document's stems: the project name ×3, each title of its non-archived tasks ×2, each `@handle` in those tasks' notes ×2, the mark name of each of those tasks that is a milestone with a mark the marks directory holds ×1, each other word of those tasks' notes ×1.
  Threshold: project `Eval harness` with one task `Answer key`, notes `ask @username_subject key`, milestone mark `payment` named `Payment` → tf `{eval: 3, harnes: 3, answer: 2, key: 3, @username_subject: 2, paymen: 1}` exactly; 1/1. *NC:* name ×2: RED. **TC-4464**
- **LLR-4403.5 — Ubiquitous.** The system shall leave tasks with no project out of every document.
  Threshold: a project-less task titled `zebra` → no document holds `zebra`; 1/1. *NC:* a `None` project document: RED. **TC-4465**
- **LLR-4403.6 — Ubiquitous.** The system shall weight each stem by `idf = ln((N + 1) / (df + 1)) + 1`, N the document count and df the documents holding the stem.
  Threshold: a 3-document fixture → every idf equal to the hand value within 1e-9; 1/1. *NC:* `ln(N / df)`: RED. **TC-4466**
- **LLR-4403.7 — Ubiquitous.** The system shall score a note against a document as the cosine of their tf·idf vectors.
  Threshold: the fixture note against `Eval harness` → the hand value within 1e-4; 1/1. *NC:* dot product without norms: RED. **TC-4467**
- **LLR-4403.8 — Unwanted.** If a note and a document share exactly one stem, then the system shall halve that score.
  Threshold: a one-shared-stem pair → score = 0.5 × cosine (within 1e-4); a two-stem pair → not halved; 2/2. *NC:* no halving: arm 1 RED. **TC-4468**
- **LLR-4403.9 — Ubiquitous.** The system shall order a note's hits by score rounded to 4 decimals, highest first, then by board order, then by project name, then by the project's position on its board.
  Threshold: equal scores on boards 0 and 1 → board 0 first (even when board 1's name sorts first); equal scores on one board, `Alpha` at position 1 and `Beta` at position 0 → `Alpha` first; 2/2. *NC:* project position before name: arm 2 RED. **TC-4469**
- **LLR-4403.10 — Ubiquitous.** The system shall keep at most 3 hits per note, each scoring at least LOW (0.08).
  Threshold: 5 scoring documents → 3 hits; a 0.07 document absent; 2/2. *NC:* `k = 4`: RED. **TC-4470**
- **LLR-4403.11 — Ubiquitous.** The system shall make a note's top choice its best hit when that hit scores at least MID (0.16).
  Threshold: best 0.40 → top is that project; 1/1. *NC:* cut at HIGH: RED. **TC-4471**
- **LLR-4403.12 — Unwanted.** If a note has no hit scoring at least MID, then the system shall make `+ new project` its top choice.
  Threshold: best 0.12 → top None; no hit at all → top None; 2/2. *NC:* weak hit as top: arm 1 RED. **TC-4472**
- **LLR-4403.13 — Ubiquitous.** The system shall make a note's alternatives the next up to 2 hits after its top choice, or its first up to 2 hits when the top choice is `+ new project`.
  Threshold: hits [0.40, 0.20, 0.10] → options [0.40, 0.20, 0.10]; hits [0.12, 0.09] → options [None, 0.12, 0.09]; 2/2. *NC:* always append None (the proto's 4th option): RED. **TC-4473**
- **LLR-4403.14 — Ubiquitous.** The system shall give each hit's reason as the note's surface words of the shared stems, largest contribution first, ties by stem.
  Threshold: the fixture → `["questions", "@username_subject", "key"]`; 1/1. *NC:* alphabetical: RED. **TC-4474**
- **LLR-4403.15 — Ubiquitous.** The rail shall show, for each note in pad order, a line with its number and title, a line `→ ` with its chosen option, and a line `why ` with up to 3 reason words joined by ` · `.
  Threshold: 3-note fixture at 118x30 → rail plain lines equal the graph example (9 lines + spacers); 1/1. *NC:* reason words joined by `, `: RED. **TC-4475**
- **LLR-4403.16 — Ubiquitous.** The rail shall draw a project option as the project name in its project hue, ` · `, the board name in the board's hue and a confidence cue: `▰▰▰` at or above HIGH, `▰▰▱` at or above MID, `▰▱▱` at or above LOW.
  Threshold: 3 scores (0.41, 0.20, 0.09) → 3/3 cues; the name cells carry the project's `HEX` hue; 4/4. *NC:* no board name: RED. **TC-4476**
- **LLR-4403.17 — State.** While the cursor is in a note, the rail shall show under that note's reason line `or ` and its other options joined by `  ·  `.
  Threshold: the cursor's note shows the `or` line with 2 options; the 2 other notes show none; 2/2. *NC:* `or` line on every note: RED. **TC-4477**
- **LLR-4403.18 — Unwanted.** If a note's chosen option is `+ new project` and the note has no hit, then its reason line shall read `no project shares a word`.
  Threshold: 1/1 exact. *NC:* blank: RED. **TC-4478**
- **LLR-4403.19 — Unwanted.** If a note's chosen option is `+ new project` and the note has hits, then its reason line shall read `weak: <w1> · <w2> (<best hit's project>)`.
  Threshold: 1/1 exact. *NC:* `no project shares a word`: RED. **TC-4479**
- **LLR-4403.20 — Unwanted.** If a board's file is missing or unreadable, then the head row shall end with ` · <n> board not read` (`boards` for n > 1).
  Threshold: 1 missing → `· 1 board not read`; 2 → `· 2 boards not read`; the suggestions skip those boards; 3/3. *NC:* silent skip: RED. **TC-4480**
- **LLR-4403.21 — Ubiquitous.** The system shall compute a note's hits at most once per distinct note text while the documents are unchanged.
  Threshold: 3 notes painted, then 5 characters typed in note 2 → 0 further computations for notes 1 and 3 (a spy on the scorer); 1/1. *NC:* no cache: RED. **TC-4481**
- **LLR-4403.22 — Unwanted.** If a note is longer than 10 000 characters, then the system shall score only its first 10 000 characters.
  Threshold: `eval harness` + 2 000 000 × `z ` → the same hits as the first 10 000 characters, computed in < 1.0 s; 2/2. *NC:* score the whole note: the time arm RED. **TC-4482**
- **LLR-4403.23 — Ubiquitous.** The capture view shall build the documents from every board `board_lanes` returns when it opens.
  Threshold: 2 readable boards → documents from both; 1/1. *NC:* `app.board` only: RED. **TC-4483**
- **LLR-4403.24 — Event.** When a dump or an undo changes a board, the system shall rebuild the documents from the boards as read after that change.
  Threshold: after dumping `Rotation plan` into `Eval harness`, a note `rotation` lists `Eval harness` among its hits (it did not before); 1/1. *NC:* no rebuild: RED. **TC-4484**
- **LLR-4403.25 — Unwanted.** If no readable board holds a non-archived project, then every note's top choice shall be `+ new project`.
  Threshold: one board with 0 projects → rail `→ + new project` and `no project shares a word`; 0 exceptions; 2/2. *NC:* index the empty document list: RED. **TC-4485**
- **LLR-4403.26 — Ubiquitous.** The system shall give the same hits for the same note and the same boards on every run.
  Threshold: 3 runs over the fixture → identical hit lists (ids, scores, reasons); 1/1. *NC:* iterate a `set` for the tie order: RED (under `PYTHONHASHSEED` 0 vs 1). **TC-4486**

### 4.4 Dump, alternatives, new project (HLR-4404)

- **LLR-4404.1 — Event.** When `alt+d` is pressed with the cursor in a note whose chosen option is a project, the system shall add one task built from that note to that project on its board.
  Threshold: the target board's task count +1; the new task's `project_id` is that project's id; 2/2. *NC:* dump to the open board always: RED (target on board 2). **TC-4501**
- **LLR-4404.2 — Ubiquitous.** The system shall take a dumped task's title as the visible text, stripped, of the note's title line.
  Threshold: `"::b:: Golden set ::\nmore"` → `Golden set`; `"img: a.png\nTitle\nx"` → `Title`; 2/2. *NC:* the raw first line: `::b::` in the title: RED. **TC-4502**
- **LLR-4404.3 — Ubiquitous.** The system shall take a dumped task's notes as the note's lines other than its title line and its image lines, verbatim, with leading and trailing blank lines removed.
  Threshold: `"T\n\nask @username_subject ::r:: now ::\n\nsecond\nimg: a.png\n"` → `"ask @username_subject ::r:: now ::\n\nsecond"`; 1/1. *NC:* drop inner blank lines: RED. **TC-4503**
- **LLR-4404.4 — Event.** When a note is dumped, the system shall set its task's `created` to a stamp (`models.stamp`).
  Threshold: for an open-board and an other-board dump, `created` matches `^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d$` within [t0, t1]; 2/2. *NC:* no stamp on the other-board path: arm 2 RED. **TC-4504**
- **LLR-4404.5 — Ubiquitous.** The system shall put a dumped task in the target board's first phase.
  Threshold: target phases `["Todo", "Doing"]` → `phase == "Todo"`; 1/1. *NC:* the dataclass default `Backlog`: RED. **TC-4505**
- **LLR-4404.6 — Event.** When a dump succeeds, the system shall remove the note's lines and one adjacent divider line (the one after it, else the one before) from the pad.
  Threshold: `"a\n____\nb\n____\nc"`: dump `b` → `"a\n____\nc"`; dump `c` → `"a\n____\nb"`; every other line byte-identical; 3/3. *NC:* leave the divider: `"a\n____\n____\nc"`: RED. **TC-4506**
- **LLR-4404.7 — Event.** When a dump succeeds, the system shall show the notice `Dumped → <project> · <board>   ·   alt+u undo`.
  Threshold: exact text, `markup=False`, title `Capture`; 1/1. *NC:* no `alt+u` hint: RED. **TC-4507**
- **LLR-4404.8 — Event.** When the target board is the open board, the system shall add the task through `app.board.add_task` (the app's save path) and refresh the board view.
  Threshold: `app.board` holds the task; the board file holds it; the board view's render holds its title after `esc`; 3/3. *NC:* add to a fresh copy: `app.board` lacks it: RED. **TC-4508**
- **LLR-4404.9 — Event.** When the target board is not the open board, the system shall read that board fresh (`peek_board`), add the task and save it with `save_atomic`, all while holding `boards.file_lock` on its file (`move_project`'s pattern, R1-3).
  Threshold: the lock file exists at the save (spy); `save_atomic` called once and `Board.save` never on that board (spy); a task another writer appended to that file after the view opened is still in the file after the dump; 3/3. *NC:* save the board read at open: the other writer's task lost: RED. **TC-4509**
- **LLR-4404.10 — Unwanted.** If the target board's file is missing, then the system shall leave the note in the pad and show `<board>'s file is missing — nothing dumped.`
  Threshold: notice exact; pad unchanged; no file created at that path; 3/3. *NC:* `Board.load` seeds and saves sample data: RED. **TC-4510**
- **LLR-4404.11 — Unwanted.** If the target board's file cannot be read, then the system shall leave the note in the pad and show `<board>'s file cannot be read — nothing dumped.`
  Threshold: notice exact; file bytes unchanged; 2/2. *NC:* write an empty board over it: RED. **TC-4511**
- **LLR-4404.12 — Unwanted.** If the target project is not on the freshly read board, then the system shall leave the note in the pad and show `<project> is no longer on <board> — nothing dumped.`
  Threshold: project removed from the file after the view opened → notice exact; board bytes unchanged; 2/2. *NC:* add a task with a dangling `project_id`: RED. **TC-4512**
- **LLR-4404.13 — Unwanted.** If the target board's lock cannot be taken within `boards.LOCK_WAIT`, then the system shall leave the note in the pad and show the lock's error text.
  Threshold: a held lock file → the notice holds `is busy`; pad and board bytes unchanged; 3/3. *NC:* write without the lock: RED. **TC-4513**
- **LLR-4404.14 — Unwanted.** If saving the target board raises `OSError`, then the system shall leave the note in the pad and show `<board> could not be saved: <error> — nothing dumped.`
  Threshold: a read-only board file → notice prefix exact; pad unchanged; 2/2. *NC:* unguarded save: exception: RED. **TC-4514**
- **LLR-4404.15 — Unwanted.** If saving the open board raises `OSError` during a dump, then the system shall leave `app.board` holding neither the task nor a project that dump created.
  Threshold: `len(app.board.tasks)` and `len(app.board.projects)` equal their values before the dump; 2/2. *NC:* no roll-back: RED. **TC-4515**
- **LLR-4404.16 — Event.** When `alt+o` is pressed with the cursor in a note, the system shall make that note's next option its chosen option, wrapping after the last.
  Threshold: 3 options: `alt+o` ×3 → back to the top choice; the rail's `→` line follows; 2/2. *NC:* no wrap: RED. **TC-4516**
- **LLR-4404.17 — Ubiquitous.** The system shall keep each note's chosen option keyed by the note's text, shared by the rail and the review list.
  Threshold: `alt+o` on note 2, then `alt+a` → row 2 shows the same option; 1/1. *NC:* keyed by note index, reset by the review: RED. **TC-4517**
- **LLR-4404.18 — Event.** When `alt+d` is pressed with the cursor in a note whose chosen option is `+ new project`, the system shall open the new-project name field for that note.
  Threshold: the field is shown and focused; no board changed; 2/2. *NC:* dump to the best weak hit: RED. **TC-4518**
- **LLR-4404.19 — Event.** When `alt+n` is pressed with the cursor in a note, the system shall open the new-project name field titled `New project for note <k>`.
  Threshold: title exact for k = 3; 1/1. *NC:* unbound: RED. **TC-4519**
- **LLR-4404.20 — Ubiquitous.** The name field's target board shall start as the open board.
  Threshold: the key row reads `↵ create on <open board name> + dump`; 1/1. *NC:* the first registry board: RED (open board = board 2). **TC-4520**
- **LLR-4404.21 — Event.** When `alt+b` is pressed in the name field, the system shall set its target board to the next readable board in board order, wrapping after the last.
  Threshold: 3 readable boards: `alt+b` ×3 → back to the open board; an unreadable board is skipped; 2/2. *NC:* include unreadable boards: RED. **TC-4521**
- **LLR-4404.22 — State.** While the name field is open, the key row shall show `↵ create on <board> + dump`, `alt+b board` and `esc back`.
  Threshold: plain text exact at 118x30; 1/1. *NC:* the pad's key row kept: RED. **TC-4522**
- **LLR-4404.23 — Event.** When `enter` is pressed in the name field holding a name, the system shall create a project of that name on the target board and dump the note into it in one board write.
  Threshold: the file holds the project and the task (project id = task's `project_id`); `Board.save`/`save_atomic` called once (spy); 3/3. *NC:* `add_project` then `add_task`: 2 saves: RED. **TC-4523**
- **LLR-4404.24 — Ubiquitous.** The system shall give a new project the first `models.PROJECT_COLORS` hue no project of the target board uses, else `PROJECT_COLORS[len(projects) % 8]`.
  Threshold: a board using `lime`, `green` → `sky`; a board of 9 projects using all 8 → `PROJECT_COLORS[1]`; 2/2. *NC:* always `violet`: RED. **TC-4524**
- **LLR-4404.25 — Unwanted.** If the submitted name is empty once control characters and surrounding whitespace are removed, then the system shall create nothing and show `A project needs a name.`
  Threshold: `"   "` → 0 projects added; field still open; notice exact; 3/3. *NC:* `Untitled` project: RED. **TC-4525**
- **LLR-4404.26 — Unwanted.** If the target board holds a project whose name equals the submitted name ignoring case and surrounding whitespace, then the system shall create nothing and show `<board> already has a project named <name>.`
  Threshold: `eval HARNESS ` vs `Eval harness` → 0 projects added; notice exact; 2/2. *NC:* a second same-named project: RED. **TC-4526**
- **LLR-4404.27 — Event.** When `esc` is pressed in the name field, the system shall close the field and focus the pad.
  Threshold: field hidden; `app.focused` is the pad; boards and store unchanged; 3/3. *NC:* `esc` closes the view: RED. **TC-4527**
- **LLR-4404.28 — Unwanted.** If `alt+d`, `alt+o` or `alt+n` is pressed while the cursor is in no note, then the system shall show `No note under the cursor.`
  Threshold: on an empty pad, each key → that notice; 0 changes; 3/3. *NC:* act on the last note (proto `cur()`): RED. **TC-4528**
- **LLR-4404.29 — Unwanted.** If the cursor's note has no title line, then the system shall dump nothing and show `This note has no text line for a title.`
  Threshold: note `"img: a.png"` and note `"::b:: ::"` → notice; 0 tasks; 2/2. *NC:* a task titled `img: a.png`: RED. **TC-4529**
- **LLR-4404.30 — Ubiquitous.** The system shall take the cursor's note as the note holding the cursor's line, or the note above when the cursor is on a divider line.
  Threshold: `"a\n____\nb"`: cursor row 1 → note `a`; row 2 → note `b`; 2/2. *NC:* divider → the note below: RED. **TC-4530**
- **LLR-4404.31 — Ubiquitous.** The system shall leave a dumped task's other fields at the `Task` defaults.
  Threshold: priority `normal`, no dates, not archived, no URLs, no links; 5/5. *NC:* copy the note's first URL into `urls`: RED. **TC-4531**
- **LLR-4404.32 — Event.** When a dump saves its board, the system shall append to that board's `history.jsonl` one birth record `{"task": <id>, "from": null, "to": <phase>}` whose `at` equals the task's `created`.
  Threshold: for an open-board and an other-board dump, exactly 1 birth record for the id with `at == created`; on the other board it is appended after `save_atomic` returned; 3/3. *NC:* no record on the other-board path (no `add_task` there): arm 2 RED. **TC-4532**
- **LLR-4404.33 — Unwanted.** If another board's file changes (mtime or size) between the fresh read and the save of a dump, then the system shall save nothing and show `<board> changed while dumping — nothing dumped.`
  Threshold: a write by a lock-ignoring writer injected between the read and the save → board bytes equal that writer's; the note stays in the pad; notice exact; 3/3. *NC:* no stamp check: the other writer's change lost: RED. **TC-4533**

### 4.5 Undo and the 7-day keep (HLR-4405)

- **LLR-4405.1 — Event.** When `alt+u` is pressed in the pad, the system shall undo the newest dumped entry that is at most 7 days old.
  Threshold: 2 dumps, `alt+u` → the 2nd task gone, the 1st kept; `alt+u` → the 1st gone; 2/2. *NC:* undo the oldest: RED. **TC-4541**
- **LLR-4405.2 — Event.** When a dump is undone, the system shall remove its task from its board (the open board through `app.board` and the app's save path; another board read fresh, stamp-checked and saved with `save_atomic` under its lock, R1-3).
  Threshold: the board file no longer holds the task id, for an open-board and an other-board dump; 2/2. *NC:* other board saved from a stale read: RED (a concurrent task lost). **TC-4542**
- **LLR-4405.3 — Event.** When a dump is undone, the system shall append the note's text to the pad, after a new divider line when the pad holds text.
  Threshold: pad `"a"` → `"a\n____\n<text>"`; empty pad → `"<text>"`; 2/2. *NC:* no divider: the note merges into `a`: RED. **TC-4543**
- **LLR-4405.4 — Event.** When a dump is undone, the system shall remove its entry from the store's `dumped`.
  Threshold: the file's `dumped` length −1, the entry's `task` absent; 2/2. *NC:* keep the entry: a second `alt+u` undoes it again: RED. **TC-4544**
- **LLR-4405.5 — Event.** When an undone dump created its project and no other task of that board belongs to that project, the system shall remove that project.
  Threshold: 1/1. *NC:* keep the empty project: RED. **TC-4545**
- **LLR-4405.6 — Unwanted.** If another task of that board belongs to the project the undone dump created, then the system shall keep that project.
  Threshold: 1/1. *NC:* always remove it: the other task loses its project: RED. **TC-4546**
- **LLR-4405.7 — Unwanted.** If the store keeps no dumped entry at most 7 days old, then `alt+u` shall show `Nothing to undo.`
  Threshold: empty `dumped` and one 8-day-old entry → that notice; 0 changes; 2/2. *NC:* IndexError: RED. **TC-4547**
- **LLR-4405.8 — Unwanted.** If the dumped task is no longer on its board, then the system shall restore the note to the pad without changing any board.
  Threshold: task deleted after the dump → pad gains the note; entry removed; board bytes unchanged; 3/3. *NC:* raise on the missing id: RED. **TC-4548**
- **LLR-4405.9 — Unwanted.** If the dumped task is no longer on its board, then the system shall show `<title> is no longer on <board>: the note is back in the pad.`
  Threshold: 1/1 exact. *NC:* silent: RED. **TC-4549**
- **LLR-4405.10 — Unwanted.** If the dumped task's title or notes differ from what its dump wrote, then the system shall leave the task, the pad and the store unchanged and show `<title> changed since the dump — undo left it.`
  Threshold: title edited after the dump → board, pad, store bytes unchanged; notice exact; 2/2. *NC:* delete the edited task: RED. **TC-4550**
- **LLR-4405.11 — Unwanted.** If the board of an undo cannot be read, locked or saved, then the system shall leave the pad and the store unchanged and show `<board> could not be changed: <error> — nothing undone.`
  Threshold: a held lock → notice prefix exact; pad and store unchanged; 2/2. *NC:* remove the entry first: RED. **TC-4551**
- **LLR-4405.12 — Ubiquitous.** The system shall drop from `dumped`, at every write of the store, each entry whose `at` is more than 7 days (604 800 s) before now or is not a valid stamp.
  Threshold: entries at now − 7 d + 60 s (kept), now − 7 d − 60 s (dropped), `"garbage"` (dropped); 3/3. *NC:* 30 days: arm 2 RED. **TC-4552**
- **LLR-4405.14 — Ubiquitous.** The system shall take a dump's undo from its store entry only, leaving the app's `_undo_stack` unchanged by a dump and by its undo (R1-4).
  Threshold: `len(app._undo_stack)` equal before and after a dump and after `alt+u`; `u` on the board after an open-board dump leaves the dumped task; 3/3. *NC:* push a snapshot on dump: RED. **TC-4554**
- **LLR-4405.13 — State.** While the store keeps at least one dumped entry at most 7 days old, the wide rail shall end with `✓ dumped <n>  ·  alt+u undo  ·  kept 7 days`.
  Threshold: 2 entries → that line with `2`; 0 entries → no such line; 2/2. *NC:* line missing: RED. **TC-4553**

### 4.6 The review list (HLR-4406)

- **LLR-4406.1 — Event.** When `alt+a` is pressed in the pad, the system shall open the review list over the capture view with one row per note, in pad order.
  Threshold: 4 notes → 4 rows; it is a `ModalScreen`; 2/2. *NC:* rows from the store's last write: RED (a note typed 0.2 s ago is missing). **TC-4561**
- **LLR-4406.2 — Ubiquitous.** The review list shall draw each row as: `▶ ` on the cursor's row (else two spaces), `[x] ` or `[ ] `, the note's title, the chosen option drawn as in LLR-4403.16, and on a second line `why ` with the reason words or, for `+ new project`, `needs a name: alt+n in the pad`.
  Threshold: the 4-row fixture's plain lines equal the graph example at 118x30; 1/1. *NC:* no second line: RED. **TC-4562**
- **LLR-4406.3 — Ubiquitous.** The review list shall open each row checked when its chosen option is a project and unchecked when it is `+ new project`.
  Threshold: 3 project rows `[x]`, 1 new-project row `[ ]`; 2/2. *NC:* all checked: RED. **TC-4563**
- **LLR-4406.4 — Event.** When `↓` or `↑` is pressed in the review list, the system shall move the cursor one row down or up, clamped to the first and last rows.
  Threshold: `↑` at row 0 stays 0; `↓` ×9 on 4 rows ends at 3; 2/2. *NC:* no clamp: RED. **TC-4564**
- **LLR-4406.5 — Event.** When `space` is pressed in the review list on a row whose chosen option is a project, the system shall toggle that row's check.
  Threshold: `[x]` → `[ ]` → `[x]`; 2/2. *NC:* one-way: RED. **TC-4565**
- **LLR-4406.6 — Unwanted.** If `space` is pressed on a row whose chosen option is `+ new project`, then the system shall keep the row unchecked and show `Needs a name: alt+n in the pad.`
  Threshold: row stays `[ ]`; notice exact; 2/2. *NC:* checkable: RED. **TC-4566**
- **LLR-4406.7 — Event.** When `o` is pressed in the review list, the system shall make the cursor row's next option its chosen option, as `alt+o` does.
  Threshold: the row's option changes and, after `esc`, the rail shows the same option for that note; 2/2. *NC:* review-local choice: arm 2 RED. **TC-4567**
- **LLR-4406.8 — Event.** When `d` is pressed in the review list, the system shall dump every checked row's note, in pad order, as `alt+d` dumps one.
  Threshold: 3 of 4 checked → 3 tasks on their boards; the pad holds the unchecked note only; 2/2. *NC:* unchecked rows dumped too: RED. **TC-4568**
- **LLR-4406.9 — Event.** When the review list's batch dump ends, the system shall close the review list.
  Threshold: `app.screen` is the capture view after `d`; 1/1. *NC:* list stays open: RED. **TC-4569**
- **LLR-4406.10 — Unwanted.** If one checked row's dump fails, then the system shall leave that note in the pad and go on with the next checked row.
  Threshold: 3 checked, the 2nd row's board missing → rows 1 and 3 dumped, note 2 in the pad, notice `Dumped 2 of 3 checked`; 3/3. *NC:* stop at the first failure: RED. **TC-4570**
- **LLR-4406.11 — Event.** When `u` is pressed in the review list, the system shall undo the newest dump as `alt+u` does and rebuild the rows.
  Threshold: a dump undone → its note appears as a new row; 2/2. *NC:* `u` unbound: RED. **TC-4571**
- **LLR-4406.12 — Event.** When `esc` is pressed in the review list, the system shall close it.
  Threshold: `app.screen` is the capture view; boards and store unchanged; 2/2. *NC:* `esc` closes the view too: RED. **TC-4572**
- **LLR-4406.13 — Ubiquitous.** The review list's key row shall show `↑↓ move`, `␣ include`, `o other`, `d dump <k> checked`, `u undo` and `esc back`, fitted by `keymap.key_line`.
  Threshold: `k` follows the checks (3 → 2 after one `space`); at 80x24 all 6 key glyphs present; 2/2. *NC:* fixed `dump checked`: arm 1 RED. **TC-4573**
- **LLR-4406.14 — Unwanted.** If the pad holds no note when `alt+a` is pressed, then the system shall show `No notes to review.` and open no review list.
  Threshold: notice exact; `app.screen` is the capture view; 2/2. *NC:* empty modal: RED. **TC-4574**
- **LLR-4406.15 — State.** While the review list is open, the system shall leave the pad's text unchanged by typed keys.
  Threshold: typing `x` and `a` in the review list → pad text unchanged; 1/1. *NC:* review list not modal: RED. **TC-4575**
- **LLR-4406.16 — Event.** When the review list's batch dump ends, the system shall show `Dumped <k> of <n> checked`.
  Threshold: notice exact (`Dumped 3 of 3 checked`), `markup=False`; 1/1. *NC:* no notice: RED. **TC-4576**

### 4.7 The store (HLR-4407)

- **LLR-4407.1 — Ubiquitous.** The system shall keep the store at `app.registry.path.parent / "inbox.json"`.
  Threshold: a registry in a temporary folder → the store written there after the first change; 1/1. *NC:* beside the open board: RED (board in a subfolder). **TC-4581**
- **LLR-4407.2 — Ubiquitous.** The system shall write the store as a JSON object with `version` (the int 1), `pad` (str), `dumped` (list), `flagged` (list, only while non-empty) and, only once set, `divider_notice` (true), in that key order, as `json.dumps(data, indent=2, ensure_ascii=False)`.
  Threshold: a fixture store written → bytes equal the expected text held in the test; without the flag, no `divider_notice` key; with no flagged note, no `flagged` key; 3/3. *NC:* `ensure_ascii=True`: an `é` in the pad written `\u00e9`: RED. **TC-4582**
- **LLR-4407.3 — Ubiquitous.** The system shall write each dumped entry as an object with `at` (stamp), `text` (the note's text verbatim), `task` (id), `title` (the dumped title), `board` (the board file's path as str), `project` (id), `new_project` (bool) and `images` (list of file names), in that key order.
  Threshold: one dump → the entry's keys and types exactly; 1/1. *NC:* `text` omitted: RED. **TC-4583**
- **LLR-4407.4 — Ubiquitous.** The system shall write the store by applying each change to the store as the file holds it at that moment, while holding `boards.file_lock` on the store.
  Threshold: a second `Inbox` instance adds a dumped entry; this view's next pad write keeps it; the lock file exists during the write (spy); 2/2. *NC:* write the in-memory store: entry lost: RED. **TC-4584**
- **LLR-4407.5 — Ubiquitous.** The system shall write the store through `models.write_atomic`.
  Threshold: a spy sees `write_atomic` called with the store's path; an exception injected inside it leaves the old bytes; 2/2. *NC:* `Path.write_text`: RED. **TC-4585**
- **LLR-4407.6 — Unwanted.** If the store file is missing, then the system shall start with an empty pad and no dumped entries.
  Threshold: no file → pad `""`, `dumped == []`; 0 exceptions; 2/2. *NC:* raise FileNotFoundError: RED. **TC-4586**
- **LLR-4407.7 — Unwanted.** If the store file is unreadable (not JSON, not an object, a `pad` that is not a str, a `dumped` or `flagged` that is not a list), then the system shall copy it aside with `boards.keep_aside` when it first loads it.
  Threshold: 5 corrupt variants → `inbox.json.corrupt` byte-equal to each (fresh folder per variant); 5/5. *NC:* no copy: RED. **TC-4587**
- **LLR-4407.8 — Unwanted.** If the store file is unreadable when first loaded, then the system shall start with an empty pad and show `inbox.json could not be read; it was copied to <backup name> and the pad starts empty.`
  Threshold: notice exact, `markup=False`, severity `warning`; pad empty; 3/3. *NC:* silent: RED. **TC-4588**
- **LLR-4407.9 — Unwanted.** If an unreadable store cannot be copied aside, then the system shall not write over it.
  Threshold: `keep_aside` patched to return None → after a pad change, file bytes unchanged; the save notice holds `was not written`; 2/2. *NC:* overwrite: RED. **TC-4589**
- **LLR-4407.10 — Unwanted.** If a dumped or flagged entry is not an object or lacks a field of its type, then the system shall skip that entry.
  Threshold: 3 bad entries (a list, `task` an int, no `at`) + 1 good → 1 entry read; 1/1. *NC:* treat the file as unreadable: RED. **TC-4590**
- **LLR-4407.11 — Ubiquitous.** The system shall remove control characters (`models.clean_strings`) from every string it reads from the store.
  Threshold: `pad` holding `\x1b[31m` and `\x07` → pad without either; 2/2. *NC:* raw read: RED. **TC-4591**
- **LLR-4407.12 — Unwanted.** If `divider_notice` is anything but the boolean true, then the system shall treat the divider notice as not shown.
  Threshold: `"yes"`, `1` → notice shown on the first divider; 2/2. *NC:* truthiness: RED. **TC-4592**
- **LLR-4407.13 — Event.** When the capture view opens, the system shall re-read the store if its mtime or size changed since this app last read or wrote it.
  Threshold: a second `Inbox` writes pad `"x"` → reopen shows `"x"`; an unchanged file → 0 parses (spy); 2/2. *NC:* read once at mount: arm 1 RED. **TC-4593**
- **LLR-4407.14 — Unwanted.** If that re-read cannot parse the file, then the system shall keep the in-memory store and show once `inbox.json could not be read; the pad as loaded is kept.`
  Threshold: 1 notice; the pad as loaded; a second open with the file unchanged → no second notice; 3/3. *NC:* empty the pad: RED. **TC-4594**
- **LLR-4407.15 — Event.** When the pad's text has not changed for 1.0 s after a change, the system shall write the pad to the store.
  Threshold: type, wait 1.3 s → stored `pad` equals the text; 10 keys 0.05 s apart then 1.3 s → exactly 1 write (spy); 2/2. *NC:* write per keystroke: 10 writes: RED. **TC-4595**
- **LLR-4407.16 — Event.** When the capture view closes with a pad change not yet written, the system shall write the pad before closing.
  Threshold: type then `esc` at once → stored `pad` equals the text; 1/1. *NC:* rely on the debounce: RED. **TC-4596**
- **LLR-4407.17 — Event.** When the app exits with the capture view open and a pad change not yet written, the system shall write the pad.
  Threshold: type, `app.exit()` → stored `pad` equals the text; 1/1. *NC:* no unmount write: RED. **TC-4597**
- **LLR-4407.18 — Unwanted.** If the pad is unchanged since its last read or write, then the system shall not write the store.
  Threshold: open, move the cursor, wait 1.3 s, `esc` → store bytes and mtime unchanged; with no store, no file created; 2/2. *NC:* write on close always: RED. **TC-4598**
- **LLR-4407.19 — Unwanted.** If the store file changed since this app's last read or write, then the system shall write as the pad the fresh pad's notes followed by this window's notes whose exact text is neither a note of the fresh pad nor the `text` of a fresh `dumped` entry, in this window's order, joined by `\n____\n` (note-level union, R2 F-8).
  Threshold: fresh pad `a|c` with a fresh `dumped` entry of text `b`, window `a|b|d` → `"a\n____\nc\n____\nd"`; a window note deleted here but present in the fresh pad comes back (no note text dropped silently); 2/2. *NC:* last writer wins: `c` lost and `b` back: arm 1 RED. **TC-4599**
- **LLR-4407.20 — Ubiquitous.** The system shall write this window's pad verbatim when the store file is unchanged since this app's last read or write.
  Threshold: a pad with `________`, blank lines and trailing spaces → stored byte-identical; 1/1. *NC:* always normalise through the union: RED. **TC-4600**
- **LLR-4407.21 — Event.** When a union was written, the system shall replace the pad's text with the written text.
  Threshold: pad text equals the written text; the cursor's row clamped into the text; 2/2. *NC:* keep the window's text: the next write unions again: RED. **TC-4601**
- **LLR-4407.22 — Event.** When a union was written, the system shall show `inbox.json changed in another window: its notes were merged into the pad.`
  Threshold: 1/1 exact. *NC:* silent: RED. **TC-4602**
- **LLR-4407.23 — Unwanted.** If a store write fails (lock busy or `OSError`), then the system shall keep the pad and the dumped entries in memory and show `inbox.json could not be saved: <error>`.
  Threshold: a held store lock → notice prefix exact; pad and in-memory `dumped` intact; 2/2. *NC:* clear memory: RED. **TC-4603**
- **LLR-4407.24 — Unwanted.** If the pad holds unsaved changes after a failed write when `esc` is pressed, then the system shall keep the capture view open and show `inbox.json could not be saved — esc again closes without saving.`
  Threshold: view still on top; notice exact; 2/2. *NC:* close and lose the text: RED. **TC-4604**
- **LLR-4407.25 — Event.** When `esc` is pressed again with no other key pressed since that warning, the system shall close the capture view.
  Threshold: 1/1; a typed key in between → the next `esc` warns again; 2/2. *NC:* never closes: RED. **TC-4605**
- **LLR-4407.26 — Unwanted.** If the store write fails after a dump saved its board, then the system shall keep that note in the pad as a flagged note (R2 F-12).
  Threshold: `write_atomic` failing once → the board holds the task; the pad still holds the note; the in-memory `flagged` holds `{text, task, board}` of it; the next successful write → the file's `flagged` holds it and `dumped` does not; 4/4. *NC:* remove the note from the pad with no store record: the note is lost on a crash: RED. **TC-4606**
- **LLR-4407.27 — Ubiquitous.** The system shall leave every board file, every `history.jsonl`, `people.json` and `marks.json` byte-identical while the capture view opens, takes typing, writes the pad and closes.
  Threshold: sha256 of 2 board files, their 2 histories, `people.json` and `marks.json` equal before `n` and after typing + 1.3 s + `esc`; 6/6. *NC:* `app.board.save()` on open: RED. **TC-4607**
- **LLR-4407.28 — Event.** When a note is dumped onto an old board, the system shall write every other task's entry of that board exactly as it was.
  Threshold: each old task's `json.dumps(entry, indent=2)` slice equal before and after; n/n. *NC:* back-fill `created` on the other tasks: RED. **TC-4608**
- **LLR-4407.29 — Event.** When a dump, an undo or an image attach changes the pad, the system shall write the store at once (R2 F-7).
  Threshold: after `alt+d`, `alt+u` and `alt+i` each, the stored `pad` equals the pad text with no wait (0 s); 3/3. *NC:* leave it to the 1.0 s debounce: RED. **TC-4609**
- **LLR-4407.30 — Unwanted.** If the store write fails after a dump saved its board, then the system shall show `<project> · <board> got the task, but inbox.json could not be saved: <error> — the note stays in the pad, flagged ⚑.`
  Threshold: notice prefix exact, `markup=False`, severity `warning`; 1/1. *NC:* the generic save notice only: RED. **TC-4670**
- **LLR-4407.31 — State.** While a note is flagged, the rail shall show, in place of that note's suggestion and reason lines, `⚑ already dumped → <project> · <board> — delete it here`.
  Threshold: 1 flagged note of 3 → that line under its title; no `→` option line for it; 2/2. *NC:* the normal suggestion lines: RED. **TC-4671**
- **LLR-4407.32 — Unwanted.** If `alt+d` is pressed, or the review list's `d` reaches a flagged note, then the system shall dump nothing for it and show `This note is already on <board>; delete it from the pad.`
  Threshold: `alt+d` on a flagged note → 0 tasks added, notice exact; in the review list its row opens unchecked and a batch counts it as not dumped; 3/3. *NC:* dump it again: a duplicate task: RED. **TC-4672**
- **LLR-4407.33 — Ubiquitous.** The system shall write each flagged entry as an object with `at` (stamp), `text` (the note's text verbatim), `task` (id), `title`, `board` (the board file's path as str) and `project` (id), in that key order.
  Threshold: one flagged note written → the entry's keys and types exactly; 1/1. *NC:* `text` omitted (the flag cannot find its note): RED. **TC-4673**
- **LLR-4407.34 — Event.** When a flagged entry's `text` is no longer a note of the pad at a store write, the system shall drop that entry.
  Threshold: the flagged note deleted by hand → the next write holds no `flagged` key; a flagged note still present → kept; 2/2. *NC:* flags never cleared: arm 1 RED. **TC-4674**

### 4.8 Images (HLR-4408)

- **LLR-4408.1 — Ubiquitous.** The system shall keep pad images in the folder `inbox-images` beside the store.
  Threshold: an attached bitmap lands at `<store dir>/inbox-images/paste-001.png`; 1/1. *NC:* inside a board's `images/`: RED. **TC-4611**
- **LLR-4408.2 — Event.** When `alt+i` is pressed and the clipboard holds a bitmap, the system shall save it as the next free `paste-NNN.png` in the pad images folder through `models.save_pil_image`.
  Threshold: with `paste-001.png` present → `paste-002.png`; 1/1. *NC:* overwrite `paste-001.png`: RED. **TC-4612**
- **LLR-4408.3 — Event.** When `alt+i` is pressed and the clipboard holds files, the system shall copy each regular file whose lower-case suffix is in `IMAGE_EXTS` into the pad images folder, under its own name or `<stem>-<k><suffix>` (k = 2, 3, …) when that name is taken.
  Threshold: the source file still exists byte-identical; the copy's bytes equal; a taken name → `shot-2.png`; 3/3. *NC:* move the user's file: source gone: RED. **TC-4613**
- **LLR-4408.4 — Event.** When images are added to a note, the system shall insert one line `img: <name>` per image after that note's last line.
  Threshold: note `"T\nx"` + 2 images → `"T\nx\nimg: paste-001.png\nimg: shot.png"`; 1/1. *NC:* insert at the cursor mid-line: RED. **TC-4614**
- **LLR-4408.5 — Unwanted.** If the clipboard holds no image and no files, then the system shall show `No image found in the clipboard.`
  Threshold: 1/1 exact; pad unchanged. *NC:* silent: RED. **TC-4615**
- **LLR-4408.6 — Unwanted.** If the clipboard holds files of which none is an image, then the system shall show `Clipboard holds no image files.`
  Threshold: a `.txt` and a `.svg` → that notice; 0 copies; 2/2. *NC:* copy the `.svg`: RED. **TC-4616**
- **LLR-4408.7 — Unwanted.** If saving or copying an attached image fails, then the system shall add no image line for it and show `The image could not be saved: <error>`.
  Threshold: a read-only pad images folder → notice prefix exact; pad unchanged; 2/2. *NC:* line added for a missing file: RED. **TC-4617**
- **LLR-4408.8 — Unwanted.** If `alt+i` is pressed while the cursor is in no note, then the system shall show `No note under the cursor.`
  Threshold: empty pad → notice; 0 files written; 2/2. *NC:* start a note holding only the image line: RED. **TC-4618**
- **LLR-4408.9 — Ubiquitous.** The rail shall show `▣ <n>` after the title of a note holding n image lines.
  Threshold: 1 image line → `▣ 1`; none → no `▣`; 2/2. *NC:* no count: RED. **TC-4619**
- **LLR-4408.10 — Event.** When a note with image lines is dumped, the system shall move each named file from the pad images folder into the target board's `images/<task id>/` and list its resolved path in the task's `images`, in line order.
  Threshold: sources gone; destination bytes equal; `task.images` equals the 2 resolved paths in order; 3/3. *NC:* copy without removing the source: RED. **TC-4620**
- **LLR-4408.11 — Ubiquitous.** The system shall copy every image of a dump into the target before saving the board, and remove the pad copies only after that save succeeded.
  Threshold: a board save failure → every source still in the pad images folder and no `images/<task id>/` folder left; 2/2. *NC:* move before save: sources gone after a failed save: RED. **TC-4621**
- **LLR-4408.12 — Unwanted.** If a named image file is missing or is not a regular file, then the system shall keep its image line in the task's notes as text and show `<k> image(s) not found: <names>`.
  Threshold: `img: gone.png` → task notes hold that line; notice `1 image(s) not found: gone.png`; 2/2. *NC:* drop the line silently: RED. **TC-4622**
- **LLR-4408.13 — Unwanted.** If copying an image into the target fails, then the system shall remove what it copied for that dump, dump nothing and show `An image could not be moved: <error> — nothing dumped.`
  Threshold: `shutil.copy2` failing on the 2nd image → no `images/<task id>/`, board unchanged, note in the pad; 3/3. *NC:* dump without the image: RED. **TC-4623**
- **LLR-4408.14 — Unwanted.** If the target board's `images/<task id>/` already exists, then the system shall give the task a new id until that folder does not exist.
  Threshold: the id source patched to yield a taken id first → the task holds the second id; the existing folder untouched; 2/2. *NC:* write into the existing folder: RED. **TC-4624**
- **LLR-4408.15 — Unwanted.** If a note names one image file twice, then the system shall move it once and list it once.
  Threshold: `task.images` length 1; 1/1. *NC:* second move raises on the gone source: RED. **TC-4625**
- **LLR-4408.16 — Event.** When a dump with images is undone, the system shall move each of its files from `images/<task id>/` back into the pad images folder, as `<stem>-<k><suffix>` when the name is taken, and name each file as it now is in the restored note's image lines.
  Threshold: files back (bytes equal); a taken name → restored line `img: paste-001-2.png`; 3/3. *NC:* leave the files in the board: the restored lines name missing files: RED. **TC-4626**
- **LLR-4408.17 — Event.** When a dump with images is undone, the system shall remove the emptied `images/<task id>/` folder.
  Threshold: the folder is gone; 1/1. *NC:* folder left: RED. **TC-4627**
- **LLR-4408.18 — Ubiquitous.** The system shall read an image line only when its name has no `/`, `\` or `:`, is not `.` or `..`, and has a lower-case suffix in `IMAGE_EXTS`.
  Threshold: `img: a.png` yes; `img: ../a.png`, `img: C:\a.png`, `img: sub/a.png`, `img: a.svg`, `img: a` no; 6/6. *NC:* allow `/`: the traversal arm RED. **TC-4628**

### 4.9 Colour, mentions and untrusted text (HLR-4409)

- **LLR-4409.1 — Ubiquitous.** The pad shall colour the notes' colour spans live, as the task editor's notes field does (Inc C's `InkArea` highlight map).
  Threshold: `::b:: x ::` → the cells of `x` carry `HEX["blue"]`, the marker cells `HEX["dim"]`; 2/2. *NC:* a plain `TextArea`: RED. **TC-4631**
- **LLR-4409.2 — Ubiquitous.** The system shall keep every colour span and `@mention` of a note byte for byte in the dumped task's notes.
  Threshold: notes equal the expected string; `views.notes_text` of them colours `x` blue; 2/2. *NC:* strip markers from the notes: RED. **TC-4632**
- **LLR-4409.3 — Unwanted.** If a dumped title or notes contain control characters, then the system shall remove them (`models.strip_controls`) before the task is added.
  Threshold: a note titled `"\x1b[2J T"` with notes `"a\x07b"` → title `"[2J T"` (the ESC byte removed), notes `"ab"`; no character below 0x20 other than `\t`/`\n`, no DEL and no C1 byte remains; 2/2. *NC:* raw text: RED. **TC-4633**
- **LLR-4409.4 — Unwanted.** If a note, a project name or a board name holds Rich markup, then the capture view shall draw it as literal text in the rail, the review list, the head row and every notice.
  Threshold: note title `[red]x[/red] [@click=app.quit]q` → literal in the rail row, the review row and the dump notice; the app still runs; 4/4. *NC:* `Text.from_markup(title)`: RED. **TC-4634**
- **LLR-4409.5 — Ubiquitous.** The system shall write the pad to the store with control characters removed.
  Threshold: a pasted `\x1b` and `\x9b` → absent from the stored `pad`; 2/2. *NC:* raw write: RED. **TC-4635**

## 5. Acceptance tests (black-box, keys and dialogs, Textual pilot)

- **AT-4401** (K-1, K-2) — registry of 2 synthetic boards; `n` → the capture view at 118x30 with an empty pad: the ghost example, the hint row `____ ↵ new note · alt+l divider`, head `CAPTURE  0 notes …`. Type `Golden set answer key`, `enter`, `____`, `enter` → the divider row draws as a rule, the one-time notice shows, head `2 notes`; type `Pilot stores`; `alt+l` (a divider and a new line); `esc`. Store holds the pad verbatim and `divider_notice: true`; board, history, `people.json`, `marks.json` bytes unchanged. Repeat at 80x24: the rail sits below the pad.
- **AT-4402** (K-3, K-4, K-6) — boards `Client A` (projects `Eval harness`, `Pilot rollout`) and `Course` (`Module 4 · Volumes`). Pad `Volume lab fails on WSL\nthe oracle script expects /mnt/c\nimg: board-0938.png` (the image in `inbox-images/`): the rail names `Module 4 · Volumes · Course` with `why volume · oracle · script`; `alt+d` → `Course`'s file holds the task titled `Volume lab fails on WSL`, notes `the oracle script expects /mnt/c`, `created` stamped, the image in `images/<id>/`; the note is gone from the pad; the notice `Dumped → Module 4 · Volumes · Course   ·   alt+u undo`.
- **AT-4403** (K-4) — a note whose best hit is weak: the rail shows `+ new project`; `alt+o` cycles to the weak hit and back; `alt+n`, `alt+b` → `Course`, type `Contracts pilot`, `enter` → `Course` holds the project and the task in one write; a duplicate name is refused with its notice.
- **AT-4404** (K-4) — two dumps; `alt+u` → the second task leaves its board and the note returns at the pad's end after a divider; `alt+a`, `u` → the first undone too; a third `alt+u` → `Nothing to undo.`; an entry dated 8 days ago is dropped from `dumped` at the next write.
- **AT-4405** (K-1 C) — 4 notes (one new-project); `alt+a` → 4 rows, 3 checked; `space` on the new-project row → refused; `o` on row 1; `d` → 3 tasks on their boards, `Dumped 3 of 3 checked`, the pad holds the 4th note.
- **AT-4406** (K-5) — `inbox.json` holding `{"pad": 5}` → `n` shows the empty pad and the set-aside notice, `inbox.json.corrupt` equals the bad bytes; a held `inbox.json.lock` → typing then waiting gives the save notice and the pad keeps the text; `esc` warns once, `esc` again closes. A store write failing right after a dump → the task is on its board, the note stays in the pad flagged `⚑`, and `alt+d` on it is refused.
- **AT-4407** (HLR-4409, K-6) — note `::b:: ask the vendor :: @username_subject` with a clipboard image (patched `grab_clipboard_image`) via `alt+i`; the pad shows `ask the vendor` in blue; dump → the task notes keep the span and mention verbatim; a note titled `[red]x[/red]` shows literally in the rail and the notice.
- **AT-4408** (K-5, D1) — a second window (a second `Inbox` instance) dumps note `b` and adds note `c` while this pad (holding `a`, `b`) adds `d`: the next write writes the union `a`, `c`, `d` (`b` is in the fresh `dumped`), shows the merge notice, and no task is created twice.

## 6. Slice of functions to change (named and counted)

| # | File | Unit | Change |
|---|---|---|---|
| 1 | inbox.py | constants `INBOX_NAME`, `IMAGES_NAME`, `KEEP_DAYS`, `SUGGEST_CHARS`; divider and image-line regexes | new |
| 2 | inbox.py | `is_divider(line)` | new |
| 3 | inbox.py | `parts(text)` → line ranges; `notes(text)`; `note_at(text, row)`; `note_count(text, row)` | new |
| 4 | inbox.py | `note_task(text)` → (title, notes, image names) | new |
| 5 | inbox.py | `without_note(text, part)` / `with_note(text, note)` (pad edits of dump and undo) | new |
| 6 | inbox.py | `union_pads(fresh_pad, fresh_dumped_texts, mine)` (R2 F-8) | new |
| 7 | inbox.py | `Inbox` class: `__init__`, `_hold`, `_stamped`, `load`, `refresh`, `_read`, `_commit`, `_set_aside`, `_prune` | new |
| 8 | inbox.py | `Inbox.write_pad`, `Inbox.record_dump`, `Inbox.drop_dump`, `Inbox.flag`, `Inbox.mark_notice` | new |
| 9 | inbox.py | `attach_images(folder, grabbed)` → names or a notice | new |
| 10 | inbox.py | `dump_note(target, project_or_new, text, folder)` — open board: `app.board.add_task`; other board: fresh `peek_board` under `file_lock`, stamp check, `models.stamp`, `save_atomic`, birth record; images copy; roll-back | new |
| 11 | inbox.py | `undo_dump(entry, open_board, folder)` — task/project removal (same two board paths), images back | new |
| 12 | suggest.py | `STOP`, `WORD_RE`, weights, cuts; `fold`, `stem`, `words` | new |
| 13 | suggest.py | `Doc`, `Hit`, `corpus(lanes, marks)` | new |
| 14 | suggest.py | `_idf`, `suggest(note, docs)` (with the 10 000-char cap) | new |
| 15 | suggest.py | `level`, `bars`, `options(hits)` | new |
| 16 | app.py | `PadArea(InkArea)`: divider rule in `render_line`, ghost placeholder | new |
| 17 | app.py | `CaptureView(Screen)`: compose, mount, paint (head, rail, hint, keys), debounce write, close/unmount write, actions dump/other/new/board/review/image/undo/divider, name field | new |
| 18 | app.py | `ReviewList(ModalScreen)`: rows, move, toggle, other, dump, undo, back | new |
| 19 | app.py | `rail_rows(...)`, `hit_text(...)`, `CAPTURE_KEYS`, `REVIEW_KEYS`, `CAPTURE_HINT`, `GHOST` | new |
| 20 | app.py | `TaskboardApp.__init__` (load the `Inbox` beside the registry), `action_capture` | changed/new |
| 21 | app.py | `TaskboardApp.check_action` (gate `capture`; the capture view holds the seat) | changed |
| 22 | keymap.py | `KEYMAP` entry `n` | changed |
| — | README.md | key table row for `n` (docs, not a source file) | changed |

Unchanged on purpose (to verify at E2): `Board.add_task` (stamps and writes the birth record; open board only), `history.append`, `Board.image_dir`,
`board_lanes`, `peek_board`, `file_lock`, `keep_aside`, `write_atomic`, `save_pil_image`,
`grab_clipboard_image`, `InkArea`/`ink_highlights`, `visible_text`, `highlight_segments`, `people.py`,
`marks.py`, `models.py`.
**Count: 22 units in 4 source files** (2 new: `taskboard/inbox.py`, `taskboard/suggest.py`; 2 changed:
`taskboard/app.py`, `taskboard/keymap.py`) — within the 4-source-file budget (§8 F-1).

**Proposed file-ownership groups for E2/E4:**
- **G-S (store)** — `taskboard/inbox.py`: units 1–11 (HLR-4402 parse, HLR-4404/4405 board+image operations, HLR-4407, HLR-4408 file side).
- **G-T (suggest)** — `taskboard/suggest.py`: units 12–15 (HLR-4403 layer 0).
- **G-V (view)** — `taskboard/app.py` + `taskboard/keymap.py` + `README.md`: units 16–22 (HLR-4401, HLR-4402 drawing, HLR-4403 rail, HLR-4406, HLR-4409, the key seat).
- Seams the orchestrator fixes first: `Inbox` public API and `note_task`/`notes`/`note_at` signatures (G-S ↔ G-V); `corpus`/`suggest`/`options` signatures and `Hit` (G-T ↔ G-V); `dump_note`/`undo_dump` return shape (result or notice) (G-S ↔ G-V).

## 7. Counts

US 1 · HLR 9 · LLR 180 (4401: 16, 4402: 18, 4403: 26, 4404: 33, 4405: 14, 4406: 16, 4407: 34, 4408: 18, 4409: 5) · AT 8.

Convention (as Inc L's LLR-4303.24): an `If … then` refusal that "leaves X unchanged and shows the notice N" is
one response — the refusal and its message — and is not split further; any other compound is split (LLR-4406.9 /
LLR-4406.16, LLR-4405.8 / LLR-4405.9, LLR-4407.21 / LLR-4407.22, LLR-4404.14 / LLR-4404.15).

## 8. Findings (contradictions, gaps, risks — each with a proposed decision)

- **F-1 — budget vs a separate screen module.** A `capture.py` for the screens would make 5 source files (over the 4-file budget). *Proposed:* the screens live in `app.py` as `AddedList` does; suggestions and the store are their own new modules (4 files). A fifth file needs the operator's approval. **Ruling R2: ACCEPT.**
- **F-2 — R0-8 vs R1-3 on a non-open board.** R0-8: a dump creates the task through `Board.add_task`; R1-3: another board is saved with `save_atomic` under `file_lock`. `add_task` always calls the plain `save()`, so both cannot hold on that path without changing `models.py`. *Proposed:* open board → `app.board.add_task` (R0-8); other board → `models.stamp()` (its docstring allows a direct call), append, `save_atomic`, then the birth record through `history.append` with the same moment (LLR-4404.4, LLR-4404.9, LLR-4404.32, LLR-4404.33). Writing the record after the save also avoids, on that path, the orphan birth line `add_task` leaves when its save fails (pre-existing on the open board, Inc L; backlog). Risk kept: the target open in another window, whose app saves without the lock — the stamp check refuses a dump when that write lands between read and save; a later write by that window still wins (the existing posture). **Ruling R2: ACCEPT.**
- **F-3 — colour markers in a title.** R0-8: title = the first non-blank line verbatim. Titles do not render colour, so `::b::` would show literally, and a first line of only `img:` would become the title. *Proposed:* title = visible text of the first non-image line that has visible text (LLR-4404.2, LLR-4404.29); notes stay verbatim. **Ruling R2: ACCEPT.**
- **F-4 — "the note count updates when enter is pressed" vs R0-3.** Under R0-3 alone, the empty part after a new divider is not a note, so `enter` changes no count. *Proposed:* the count also counts the cursor's empty part when it follows a divider (LLR-4402.8). **Ruling R2: ACCEPT** — the count adds the empty last part after a final divider (LLR-4402.8 reworded, LED.2).
- **F-5 — task phase.** `Task`'s default `Backlog` may not be a phase of the target board. *Proposed:* the target board's first phase (LLR-4404.5). **Ruling R2: ACCEPT.**
- **F-6 — "the image moves" vs clipboard files.** The editor references Explorer-copied files where they are; moving them at dump would move the user's own file. *Proposed:* copy into `inbox-images/` at attach, and move only those copies at dump (LLR-4408.3, LLR-4408.10). Reference format `img: <name>` (the proto's), restricted to a bare name (LLR-4408.18, no traversal). **Ruling R2: ACCEPT.**
- **F-7 — when the pad is written, and in what shape.** The commission does not say. *Proposed:* `pad` is one string (keeps R0-3's verbatim text); written after 1.0 s idle, on close and on app exit, never when unchanged (LLR-4407.15..4407.18); unknown top-level keys are not kept (mirrors `people.json`). **Ruling R2: ACCEPT** — plus an immediate write on dump, undo and attach (LLR-4407.29).
- **F-8 — a stale pad (two windows).** `people.json`'s merge is per record; a pad is free text, and last-writer-wins would bring back notes dumped in the other window (duplicate tasks). *Proposed:* a three-way merge at note level when the file changed since the base (LLR-4407.19..4407.22); verbatim otherwise. The same note dumped in two windows before either writes still makes two tasks (accepted risk). **Ruling R2: AMENDED** — no 3-way merge: a note-level union of the fresh pad and this window's notes not in the fresh pad nor in a fresh `dumped` entry (LLR-4407.19, LLR-4407.20, LLR-4407.21, LLR-4407.22 reworded).
- **F-9 — undo across sessions.** The newest `dumped` entry may be days old and its task edited since. *Proposed:* undo refuses an edited task (LLR-4405.10); a task that is gone gives the note back only (LLR-4405.8). **Ruling R2: ACCEPT.**
- **F-10 — pens in the pad.** K-4 carries colour spans, but K-1..K-6 do not give the pad Inc C's pen keys. *Proposed:* live colour display only (LLR-4409.1); `alt+1..6`/`alt+c` in the pad are out (R0-11); a backlog item if wanted. **Ruling R2: ACCEPT.**
- **F-11 — options list.** The proto always added `+ new project` as an extra option (4 options). The commission says "top + up to 2 alternatives". *Proposed:* at most 3 options; `+ new project` is an option only as a weak top; `alt+n` always reaches a new project (LLR-4403.13). Archived projects, archived tasks and project-less tasks stay out of the documents (the proto's rule; the commission does not mention them) (LLR-4403.3, LLR-4403.5). **Ruling R2: ACCEPT.**
- **F-12 — a failed write at close loses text.** *Proposed:* the first `esc` after a failed write keeps the view open with a warning; a second `esc` closes (LLR-4407.24, LLR-4407.25). The dump's two writes (board, then store) are not atomic together: a store failure keeps the dump in memory and writes it later (LLR-4407.26); a crash between the two writes leaves the note in the pad (accepted risk). **Ruling R2: ACCEPT** — the board-then-store pair is a recorded risk; a failed store write after the board save keeps the note in the pad, flagged (LLR-4407.26 rewritten; LLR-4407.30, LLR-4407.31, LLR-4407.32, LLR-4407.33, LLR-4407.34 added).
- **F-13 — exact UI strings are E1 proposals.** The commission fixes only the hint row, and R1-1 changes it to `alt+l divider` (to be flagged to the operator). The head, ghost, notices, review rows and the review's close after `d` follow the proto; UX review at E3 may tune them, and changes go through the ledger. **Ruling R2: ACCEPT** — flag in the final report.
