# Requirements — taskboard — Inc K, the capture view (dev-flow-v3-beta)

> Strict EARS (five forms only), ISO/IEC/IEEE 29148. One `shall` per requirement. Each LLR carries a
> numeric pass threshold and a negative control (*NC*: a mutant that turns its test RED). Ids continue
> the repo's sequence in a fresh block: US-4401, HLR-4401..4409, LLR-4401.n..4409.n, TC-44nn/45nn/46nn,
> AT-4401..4408.
> Base: `545c18a` (branch `feat/capture-list-colour`, Inc C and Inc L done). Commission:
> `.dev-flow/COMMISSION-capture-list-colour.md` §Inc K (K-1..K-6). Rulings: `00-orchestrator-rulings.md`
> (R0-1..R0-11) and the E2a amendments R1-1..R1-6, followed; where E1 proposes a change, see §8 Findings.
> E2 correction pass: the round-0a/0b rulings of `03-pdr-rulings.md` (P-T-*, P-S-*, P-V-*) applied (LED-2026-11-01-incK.3). Design source: the round's
> variant A (`prototypes/capture_round/proto.py` `PadScreen`, `Inbox`, `dump`, `undo_dump`, `hit_text`,
> `options`; `out/png/cap-A*_118x30.png`), variant C's review (`ReviewScreen`, `cap-C-rev_118x30.png`)
> and `prototypes/capture_round/suggest.py`.
> **TC numbering (no collisions):** LLR-4401.n → TC-(4400+n); LLR-4402.n → TC-(4430+n);
> LLR-4403.n → TC-(4460+n); LLR-4404.n → TC-(4500+n); LLR-4405.n → TC-(4540+n);
> LLR-4406.n → TC-(4560+n); LLR-4407.n → TC-(4580+n); LLR-4408.n → TC-(4610+n);
> LLR-4409.n → TC-(4630+n). Each block's n stays below its next block's base (4401: n ≤ 29,
> 4402: ≤ 29, 4403: ≤ 39, 4404: ≤ 39, 4405: ≤ 19, 4406: ≤ 19, 4407: ≤ 29, 4408: ≤ 19, 4409: ≤ 19).
> Overflow (R2): LLR-4407.n with n ≥ 30 → TC-(4640+n), i.e. TC-4670..TC-4699.
> Overflow (E3 round 1): LLR-4408.n with n ≥ 20 → TC-(4630+n), i.e. TC-4650..TC-4669 (unused by 4409, n ≤ 19).
> A second test of one LLR adds a letter (TC-4504b). The block TC-4401..TC-4699 is reserved for Inc K.
> E3 round 1 (`03-pdr-rulings.md` §Round 1, SEC-1..SEC-11, ARCH-1..ARCH-11) applied: LED-2026-11-01-incK.4;
> what changed per finding: `03-e3-corrections.md`. A withdrawn LLR keeps its id with `— Withdrawn (<finding>)` in its heading.

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
| image line | a note line that, stripped, is `img: ` followed by a name that passes the image-name rule |
| image-name rule | 1 to 128 characters; no surrounding whitespace; no `/`, `\`, `:`, no character below U+0020, no U+007F, none in U+0080..U+009F; not `.` or `..`; a lower-case suffix (`os.path.splitext`) in `models.IMAGE_EXTS`; the part before the first `.`, trailing spaces removed, lower-cased, not a Windows reserved name (`con`, `prn`, `aux`, `nul`, `conin$`, `conout$`, `com0`..`com9`, `lpt0`..`lpt9`, `com¹`..`com³`, `lpt¹`..`lpt³`) (P-S-10, SEC-7) |
| title line | the note's first line that is not an image line and whose visible text (`views.highlight_segments` joined, ARCH-8) is not blank |
| store | `inbox.json` beside the boards registry: `app.registry.path.parent / "inbox.json"` (the home's `~/.taskboard/inbox.json`) |
| pad images folder | `inbox-images/` beside the store (R0-9) |
| store stamp | the store file's (mtime, size) as of this app's last read or write of it; the file "changed" when its stamp differs; a read that fails with `OSError` leaves it as it was (SEC-4) |
| unseen entry | a fresh `dumped` entry whose (`task`, `board`) the app's Inbox did not hold at its last read or write of the store (SEC-1) |
| pending record | a dump whose board save succeeded and whose store write failed, held by the app's Inbox (not in the store) and applied to the store at the start of each later pad write; a pending drop is the same for an undo (ARCH-4) |
| pad write | a store write that carries this window's pad text: the debounce, close, exit, dump, undo and attach writes (not `mark_notice`) |
| board order | the order `app.board_lanes` returns the boards in (registry order, the unlisted `--open` board last) |
| readable board | a lane whose board is not None (file present and readable) |
| document | one non-archived project of a readable board, as a bag of weighted stems (K-3) |
| hit | (document, score, why) for one note; score is the cosine, halved on a single shared stem, rounded to 4 decimals |
| cuts | HIGH 0.30, MID 0.16, LOW 0.08 (suggest.py) |
| scored text | a note's title line and notes as `inbox.note_task` gives them (image lines left out), joined by `\n` (P-T-4) |
| document text | a project's name, then, for each of its non-archived tasks in board order, the task's title, notes and milestone mark name; the cap `suggest.DOC_CHARS` (100 000) counts these fields' characters in that order (P-T-5) |
| options | a note's top choice followed by its alternatives (at most 3 entries); `+ new project` is the option None |
| chosen option | the option `alt+o` / `o` currently selects for a note (starts at the top choice), kept as its identity (board path, project id) or the new-project sentinel, never as a list index (ARCH-2) |
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
  Threshold: typing `nNAqjkhlBuv@#?;` (each a global key elsewhere) into an empty pad gives the pad text `nNAqjkhlBuv@#?;` exactly; `app.screen` is still the capture view; 0 board writes; 3/3. *NC:* the pad not focused at open (then `q` quits and the letters reach no text): arm 1 RED (ARCH-5: Textual drops a printable priority binding above a focused TextArea, so a holding-tuple mutant cannot fire). **TC-4403**
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
  Threshold: with the capture view open, `check_action` is False for `add_task`, `delete`, `archive`; `↑` `↓` `←` `→` in the pad move the pad cursor and leave `app.selected_task_id` unchanged; 4/4. *NC:* `CaptureView` missing from the holding tuple: the `archive` arm RED (ARCH-9: `cursor` is refused by the pushed-screen clause anyway, so it is not an arm). **TC-4412**
- **LLR-4401.13 — Ubiquitous.** The README key table pinned to the seat shall carry a row for `n`.
  Threshold: `tests/test_keymap.py::test_the_readme_keybinding_table_matches_the_seat` GREEN with the `n` entry, and the README's main key table holds a line starting `` | `n` | Capture | `` (P-V-4: the home table's `n` row already satisfies the seat test); 2/2. *NC:* no README row: arm 2 RED. **TC-4413**
- **LLR-4401.14 — Event.** When `n` is pressed on the list view (`N`) or on the agenda of every board (`A`), the system shall bring the capture view to the top.
  Threshold: with the boards home not on the stack (LLR-4401.19), from each, `n` → `app.screen` is a capture view and exactly 1 capture view is on the stack (twice `N`,`n`); 3/3. *NC:* `capture` not in `check_action`'s always-allowed tuple: RED. **TC-4414**
- **LLR-4401.15 — Ubiquitous.** The system shall leave the `n` bindings of the boards home, the people directory and the marks manager acting as they act at `545c18a`.
  Threshold: `n` in each opens its own new-board / add-person / add-class form, and no capture view; 3/3. *NC:* the app's `n` made a priority binding: RED. **TC-4415**
- **LLR-4401.16 — Unwanted.** If the pad holds no note, then the rail shall read `no notes yet`.
  Threshold: empty pad → rail plain text `no notes yet`; 1/1. *NC:* blank rail: RED. **TC-4416**
- **LLR-4401.17 — Unwanted.** If the screen is narrower than 100 cells and the cursor is in no note while the pad holds a note, then the rail shall read `no note under the cursor` (P-V-7).
  Threshold: at 80x24, pad `"a\n____\n"` with the cursor on row 2 → rail plain text `no note under the cursor`; 1/1. *NC:* show the first note: RED. **TC-4417**
- **LLR-4401.18 — Ubiquitous.** The capture view shall bind every pad key (`alt+d`, `alt+o`, `alt+n`, `alt+a`, `alt+i`, `alt+u`, `alt+l`, `esc`, and `tab` of the name field) as a priority binding, so that the terminal form of an `alt+<letter>` key inserts no character (P-V-2).
  Threshold: pad `"abc"` with the cursor in that note, `events.Key("alt+o", "o")` posted through the driver → pad text `"abc"`; `events.Key("alt+u", "u")` on an empty `dumped` → pad text `"abc"` and the notice `Nothing to undo.`; every `CaptureView` binding has `priority=True`; 3/3. *NC:* `alt+o` non-priority: pad `"abco"`: arm 1 RED. **TC-4418**
- **LLR-4401.19 — Unwanted.** If the boards home is on the screen stack, then the system shall refuse the `capture` action (ARCH-3: the open board is not started yet, and a dump would write it before its start-up backup).
  Threshold: a registry of 2 boards (the home on top at start) → `app.check_action("capture", ())` False; `N` from the home, then `n` → no `CaptureView` on the stack and the board file's bytes unchanged; the home closed with `escape` (the board started), `N`, `n` → a capture view; 3/3. *NC:* `capture` answered by the always-allowed branch before the home check: arm 2 RED. **TC-4419**

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
  Threshold: a 3-document fixture → every idf equal to the hand value within 1e-9; a note stem no document holds weighs 0 in the note vector (P-T-2: fixture F's N1 → `Eval harness` 0.4018, not 0.2208); 2/2. *NC:* `ln(N / df)`: arm 1 RED; a df-0 stem weighted `ln(N + 1) + 1`: arm 2 RED. **TC-4466**
- **LLR-4403.7 — Ubiquitous.** The system shall score a note against a document as the cosine of their tf·idf vectors.
  Threshold: the fixture note against `Eval harness` → the hand value within 1e-4; 1/1. *NC:* dot product without norms: RED. **TC-4467**
- **LLR-4403.8 — Unwanted.** If a note and a document share exactly one stem, then the system shall halve that score.
  Threshold: a one-shared-stem pair → score = 0.5 × cosine (within 1e-4); a two-stem pair → not halved; 2/2. *NC:* no halving: arm 1 RED. **TC-4468**
- **LLR-4403.9 — Ubiquitous.** The system shall order a note's hits by score rounded to 4 decimals, highest first, then by board order, then by project name case-folded (`str.casefold`), then by project name as stored, then by the project's position on its board (P-T-3).
  Threshold: equal scores on boards 0 and 1 → board 0 first (even when board 1's name sorts first); equal scores on one board, `Alpha` at position 1 and `Beta` at position 0 → `Alpha` first; `alpha` at position 0 and `Beta` at position 1 → `alpha` first; `beta` at position 0 and `Beta` at position 1 → `Beta` first; 4/4. *NC:* project position before name: arm 2 RED; plain `str` order of the name: arm 3 RED. **TC-4469**
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
  Threshold: 3 notes painted, then 5 characters typed in note 2 and 1.3 s waited → 0 further computations for notes 1 and 3 and exactly 1 for note 2's new text (a spy on the scorer); 1/1. *NC:* no cache: RED. **TC-4481**
- **LLR-4403.22 — Unwanted.** If a note's scored text is longer than `suggest.NOTE_CHARS` (10 000) characters, then the system shall score only its first 10 000 characters (P-T-1: the cap lives in suggest.py).
  Threshold: `"x" × 9 995 + " eval harness"` → only `eval` survives the cut: hits `Eval harness` 0.3128 why `eval`; `eval harness` + 2 000 000 × `z ` → the same hits as its first 10 000 characters, computed in < 1.0 s; 2/2. *NC:* score the whole note: arm 1 RED (`Eval harness` 0.7077 why `eval`, `harness`; ARCH-5: the uncapped long note still scores in 0.51 s, so the time arm is not the control). **TC-4482**
- **LLR-4403.23 — Ubiquitous.** The capture view shall build the documents from every board `board_lanes` returns when it opens.
  Threshold: 2 readable boards → documents from both; 1/1. *NC:* `app.board` only: RED. **TC-4483**
- **LLR-4403.24 — Event.** When a dump, an undo or a review list's batch of dumps changes a board, the system shall rebuild the documents once from the boards as read after that change (ARCH-2, ARCH-6).
  Threshold: after dumping `Rotation plan` into `Eval harness`, a note `rotation` lists `Eval harness` among its hits (it did not before); a batch of 3 dumps → exactly 1 `corpus` call after the batch and 0 between its dumps (spy); 2/2. *NC:* no rebuild: arm 1 RED; a rebuild per dump of the batch: arm 2 RED. **TC-4484**
- **LLR-4403.25 — Unwanted.** If no readable board holds a non-archived project, then every note's top choice shall be `+ new project`.
  Threshold: one board with 0 projects → rail `→ + new project` and `no project shares a word`; 0 exceptions; 2/2. *NC:* index the empty document list: RED. **TC-4485**
- **LLR-4403.26 — Ubiquitous.** The system shall give the same hits for the same note and the same boards on every run.
  Threshold: the scorer run over the fixture's 7 probe notes in 2 subprocesses with `PYTHONHASHSEED` 0 and 1 (NO_COLOR unset, `env -u NO_COLOR`) → equal digests of the (project id, score, why) lists, `d694943ce6d21f09`; 1/1. *NC:* iterate a `set` for the tie order: RED (ARCH-5: runs inside one process share one hash seed, so they cannot see the mutant). **TC-4486**
- **LLR-4403.27 — Unwanted.** If a project's document text is longer than `suggest.DOC_CHARS` (100 000) characters, then the system shall tokenise only its first 100 000 characters (P-T-5).
  Threshold: a project `Ledger alpha` whose one task `Audit log` has notes `"audit " × 20 000 + "zebra"` (120 005 characters) → its document holds no `zebra` and `tf["audit"]` = 16 665 (2 from the title + the 16 663 whole words in the 99 979 characters left after the name's 12 and the title's 9); corpus over it in < 1.0 s; fixture F (under the cap) → the same tf as uncapped; 3/3. *NC:* no cap: `zebra` present: arm 1 RED. **TC-4487**
- **LLR-4403.28 — Ubiquitous.** The system shall score each note on its scored text (title line and notes from `inbox.note_task`, image lines left out) (P-T-4).
  Threshold: fixture F plus a lane `Shots` holding a project `Png board` with no task, note `"Shot\nimg: board-1.png"` → hits `[]`; the AT-4402 note → the same hits (`Module 4 · Volumes` 0.668) with or without its image line; 2/2. *NC:* score the raw part text: `Png board` a hit at 1.0: arm 1 RED. **TC-4488**
- **LLR-4403.29 — Ubiquitous.** The system shall compute the idf, each document's tf·idf vector and its norm once per document build, never per scored note (ARCH-6).
  Threshold: a spy on `suggest._idf` → exactly 1 call for 1 `corpus` build and 7 `suggest` calls over fixture F; the 7 notes' hits equal the per-call computation's (digest `d694943ce6d21f09`); over the stated large fixture (20 boards × 15 projects × 40 tasks × 80 note words of a 5 000-word synthetic vocabulary, seed 7: 300 documents, 734 619 stems) one `suggest` call takes < 20 ms (executed 2.7 ms; per-call idf 139.6 ms); 3/3. *NC:* idf and vectors inside `suggest`: arm 1 RED (8 calls) and arm 3 RED. **TC-4489**
- **LLR-4403.30 — Withdrawn (ARCH-12)** (LED.5): the rail scores on every change (cached corpus, LLR-4403.29), so no debounce pause. Former text: While the pad's text has changed less than 1.0 s ago, the rail shall compute no note's hits (ARCH-6: scoring runs on the debounce, not per keystroke).
  Threshold: pad N1, N2, N3 painted; 10 characters typed into N2 0.05 s apart → 0 scorer calls until 1.0 s after the last key; at 1.3 s exactly 1 call (N2's new text); 2/2. *NC:* score on every paint: 10 calls: arm 1 RED. **TC-4490**
- **LLR-4403.31 — Withdrawn (ARCH-12)** (LED.5): no stale rail lines; withdrawn with LLR-4403.30. Former text: While a note's hits are not computed, the rail shall draw that note's option and reason lines as last drawn for the note at that position in the pad, or none when none was drawn there.
  Threshold: N2's lines drawn (`→ Module 4 · Volumes · Course ▰▰▰`, `why volume · oracle · script`), then `x` typed at its end → within 1.0 s the same 2 lines under N2's title; a fourth note typed after a new divider → its title line only, no `→` line, until 1.0 s after the last key; 2/2. *NC:* draw an uncomputed note as `no project shares a word`: arm 1 RED. **TC-4491**

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
- **LLR-4404.17 — Ubiquitous.** The system shall keep each note's chosen option as the option's identity (board path, project id, or the new-project sentinel) keyed by the note's text, shared by the rail and the review list (ARCH-2).
  Threshold: `alt+o` on note 2, then `alt+a` → row 2 shows the same option; note `Rubric for the pilot` (options `Pilot rollout` 0.2232, `Eval harness` 0.0885) with `alt+o` → `Eval harness`, then 3 dumps of `Rubric review`, `Rubric scoring`, `Pilot judge rubric` into `Eval harness` (its options now `Eval harness` 0.6028, `Pilot rollout` 0.1593) → its chosen option is still `Eval harness`; an identity no longer among the options → the top choice; 3/3. *NC:* keyed by note index, reset by the review: arm 1 RED; the choice kept as a list index: `Pilot rollout`: arm 2 RED. **TC-4517**
- **LLR-4404.18 — Event.** When `alt+d` is pressed with the cursor in a note whose chosen option is `+ new project`, the system shall open the new-project name field for that note.
  Threshold: the field is shown and focused; no board changed; 2/2. *NC:* dump to the best weak hit: RED. **TC-4518**
- **LLR-4404.19 — Event.** When `alt+n` is pressed with the cursor in a note, the system shall open the new-project name field titled `New project for note <k>`.
  Threshold: title exact for k = 3; 1/1. *NC:* unbound: RED. **TC-4519**
- **LLR-4404.20 — Ubiquitous.** The name field's target board shall start as the open board.
  Threshold: the key row reads `↵ create on <open board name> + dump`; 1/1. *NC:* the first registry board: RED (open board = board 2). **TC-4520**
- **LLR-4404.21 — Event.** When `tab` is pressed in the name field, the system shall set its target board to the next readable board in board order, wrapping after the last (P-V-1: a terminal sends `alt+b` as `ESC b`, which Textual 8.2.8 reads as `ctrl+left`).
  Threshold: 3 readable boards: `tab` ×3, posted as `events.Key("tab", "\t")` through the driver → back to the open board, and the name field keeps its value and focus; an unreadable board is skipped; 3/3. *NC:* include unreadable boards: arm 2 RED; `tab` non-priority (focus moves out of the field): arm 1 RED. **TC-4521**
- **LLR-4404.22 — State.** While the name field is open, the key row shall show `↵ create on <board> + dump`, `⇥ board` and `esc back`.
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
- **LLR-4404.34 — Unwanted.** If a note's text will not encode as UTF-8 (a lone surrogate), then the system shall dump nothing and show `This note holds a character that cannot be saved — nothing dumped.` (SEC-2: `Board.save` truncates the file before it fails to encode).
  Threshold: note `"T\ud800x"` (layer 0, `dump_note`) into the open board and into `Course` → ok False, that notice; the open board's file bytes and `len(live.tasks)` unchanged; `Course`'s bytes unchanged; 3/3. *NC:* no encode check: the open board's file left at 0 bytes: arm 1 RED. **TC-4534**

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
- **LLR-4405.10 — Unwanted.** If the dumped task differs in any field from the task its dump wrote (`dataclasses.asdict` of the task against the record rebuilt from the dumped entry: title and notes by `_task_fields`, project, the board's first phase, the image paths, the id, its own `created`, every other field at the `Task` default), then the system shall leave the task, the pad and the store unchanged and show `<title> changed since the dump — undo left it.` (SEC-3).
  Threshold: after the dump, each of: title edited; phase moved to `Doing`; due date set; a URL added; an image added in the editor → board, pad and store bytes unchanged and the notice exact; the task as dumped, reloaded through `peek_board` → undone (no false "changed"); 6/6. *NC:* compare title and notes only: the phase arm RED (executed: the title/notes check sees no change). **TC-4550**
- **LLR-4405.11 — Unwanted.** If the board of an undo cannot be read, locked or saved, then the system shall leave the pad and the store unchanged and show `<board> could not be changed: <error> — nothing undone.`
  Threshold: a held lock → notice prefix exact; pad and store unchanged; 2/2. *NC:* remove the entry first: RED. **TC-4551**
- **LLR-4405.12 — Ubiquitous.** The system shall drop from `dumped`, at every write of the store, each entry whose `at` is more than 7 days (604 800 s) before now or is not a valid stamp.
  Threshold: entries at now − 7 d + 60 s (kept), now − 7 d − 60 s (dropped), `"garbage"` (dropped); 3/3. *NC:* 30 days: arm 2 RED. **TC-4552**
- **LLR-4405.14 — Ubiquitous.** The system shall take a dump's undo from its store entry only, leaving the app's `_undo_stack` unchanged by a dump and by its undo (R1-4).
  Threshold: `len(app._undo_stack)` equal before and after a dump and after `alt+u`; `u` on the board after an open-board dump leaves the dumped task; 3/3. *NC:* push a snapshot on dump: RED. **TC-4554**
- **LLR-4405.13 — State.** While the store keeps at least one dumped entry at most 7 days old, the wide rail shall end with `✓ dumped <n>  ·  alt+u undo  ·  kept 7 days`.
  Threshold: 2 entries → that line with `2`; 0 entries → no such line; 2/2. *NC:* line missing: RED. **TC-4553**
- **LLR-4405.15 — Event.** When a dump is undone and its task removed from its board, the system shall show `Undone: <title> left <board>; the note is back in the pad.` (P-V-12).
  Threshold: the undo of the AT-4402 dump → exactly 1 notification `Undone: Volume lab fails on WSL left Course; the note is back in the pad.`, title `Capture`, `markup=False`; 1/1. *NC:* silent success: RED. **TC-4555**
- **LLR-4405.16 — Unwanted.** If a dumped entry's `board`, normalised as a path string (`os.path.normcase(os.path.abspath(...))`), equals the normalised path of no lane `board_lanes` returns, then the system shall undo nothing, keep the entry and show `<board path> is not a known board — nothing undone.` (P-S-4; SEC-8: the test is on strings, so the store's value reaches no file system call).
  Threshold: the newest entry's `board` edited in `inbox.json` to a board-shaped file outside the registry → that notice; the entry still in `dumped`; that file's bytes and every board file unchanged; `board` set to `\\host\share\board.json` → that notice with 0 `os.stat` / `os.path.samefile` calls on that string (spy); 4/4. *NC:* undo any `board` path: the outside file rewritten: arm 1 RED; `samefile` against the entry's string: arm 4 RED. **TC-4556**
- **LLR-4405.17 — Ubiquitous.** The system shall take the entry `alt+u` undoes from the store file's `dumped` as read at that key press, or from the in-memory store when the file cannot be read (P-S-6).
  Threshold: a second `Inbox` drops the newest entry e after this view opened; `alt+u` here → the entry before e is undone and e's note is not restored a second time; with the file made unparseable → the in-memory newest entry is undone; 2/2. *NC:* read memory only: e's note restored twice: arm 1 RED. **TC-4557**
- **LLR-4405.18 — Ubiquitous.** The system shall take the Inbox's pending records as the newest dumped entries for `alt+u`, after the entries of the store file (ARCH-4).
  Threshold: pad `"a\n____\nb"`, `b` dumped with the store write failing → `alt+u` → `b`'s task leaves its board; with the store writable again, the next write leaves `dumped` without that entry and the pad `"a\n____\nb"` holding `b` once; the entry dumped before it is untouched; 3/3. *NC:* pending records ignored by `alt+u`: the older entry undone instead: RED. **TC-4558**
- **LLR-4405.19 — Unwanted.** If another task of the dumped task's board names it in `depends_on`, then the system shall leave the task, the pad and the store unchanged and show `Another task depends on <title> — undo left it.` (SEC-3: `delete_task` would leave a dangling id).
  Threshold: `tc1` given `depends_on ["t0000001"]` after the dump of `t0000001` (the task itself unchanged) → board, pad and store bytes unchanged; that notice exact; 2/2. *NC:* no dependency check: `t0000001` deleted and `tc1` keeps a dangling id: RED. **TC-4559**

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
- **LLR-4406.17 — Event.** When `d` is pressed in the review list, the system shall fix every checked row's target option before the batch's first dump (ARCH-2).
  Threshold: rows `Rubric review` and `Rubric scoring` (each `o` once → `Eval harness`), `Pilot judge rubric` (top `Eval harness` 0.2889) and `Rubric for the pilot` (top `Pilot rollout` 0.2232), all checked, `d` → the first 3 tasks in `Eval harness` and `Rubric for the pilot`'s task in `Pilot rollout`, the option its row showed; 1/1. *NC:* each row's option resolved after the earlier rows were dumped: `Rubric for the pilot` filed under `Eval harness` (its options then `Eval harness` 0.6028, `Pilot rollout` 0.1593): RED. **TC-4577**

### 4.7 The store (HLR-4407)

- **LLR-4407.1 — Ubiquitous.** The system shall keep the store at `app.registry.path.parent / "inbox.json"`.
  Threshold: a registry in a temporary folder → the store written there after the first change; 1/1. *NC:* beside the open board: RED (board in a subfolder). **TC-4581**
- **LLR-4407.2 — Ubiquitous.** The system shall write the store as a JSON object with `version` (the int 1), `pad` (str), `dumped` (list) and, only once set, `divider_notice` (true), in that key order, as `json.dumps(data, indent=2, ensure_ascii=False)` (ARCH-4: no `flagged` key).
  Threshold: a fixture store written → bytes equal the expected text held in the test; without the flag, no `divider_notice` key; no `flagged` key in any written store; 3/3. *NC:* `ensure_ascii=True`: an `é` in the pad written `\u00e9`: RED. **TC-4582**
- **LLR-4407.3 — Ubiquitous.** The system shall write each dumped entry as an object with `at` (stamp), `text` (the note's text verbatim), `task` (id), `title` (the dumped title), `board` (the board file's path as str), `project` (id), `new_project` (bool) and `images` (list of file names), in that key order.
  Threshold: one dump → the entry's keys and types exactly; 1/1. *NC:* `text` omitted: RED. **TC-4583**
- **LLR-4407.4 — Ubiquitous.** The system shall write the store by applying each change to the store as the file holds it at that moment, while holding `boards.file_lock` on the store.
  Threshold: a second `Inbox` instance adds a dumped entry; this view's next pad write keeps it; the lock file exists during the write (spy); 2/2. *NC:* write the in-memory store: entry lost: RED. **TC-4584**
- **LLR-4407.5 — Ubiquitous.** The system shall write the store through `models.write_atomic`.
  Threshold: a spy sees `write_atomic` called with the store's path; an exception injected inside it leaves the old bytes; 2/2. *NC:* `Path.write_text`: RED. **TC-4585**
- **LLR-4407.6 — Unwanted.** If the store file is missing, then the system shall start with an empty pad and no dumped entries.
  Threshold: no file → pad `""`, `dumped == []`; 0 exceptions; 2/2. *NC:* raise FileNotFoundError: RED. **TC-4586**
- **LLR-4407.7 — Unwanted.** If the store file is unreadable (not JSON, not an object, a `pad` that is not a str, a `dumped` that is not a list), then the system shall copy it aside with `boards.keep_aside` when it first loads it.
  Threshold: 4 corrupt variants → `inbox.json.corrupt` byte-equal to each (fresh folder per variant); 4/4. *NC:* no copy: RED. **TC-4587**
- **LLR-4407.8 — Unwanted.** If the store file is unreadable when first loaded and was copied aside, then the system shall start with an empty pad and show `inbox.json could not be read; it was copied to <backup name> and the pad starts empty.`
  Threshold: notice exact, `markup=False`, severity `warning`; pad empty; 3/3. *NC:* silent: RED. **TC-4588**
- **LLR-4407.9 — Unwanted.** If an unreadable store cannot be copied aside, then the system shall not write over it.
  Threshold: `keep_aside` patched to return None → after a pad change, file bytes unchanged; the save notice holds `was not written`; 2/2. *NC:* overwrite: RED. **TC-4589**
- **LLR-4407.10 — Unwanted.** If a dumped entry is not an object, lacks a field of its type, has a `task` that does not fullmatch `[A-Za-z0-9_-]{1,64}`, an `images` item that fails the image-name rule, a blank `text` or a `new_project` that is not a bool, then the system shall skip that entry (P-S-4: `task` and `images` form file paths).
  Threshold: 3 bad entries (a list, `task` an int, no `at`) + 1 good → 1 entry read; entries with `task` `"../x"`, `images` `["../../a.png"]`, `text` `"  "`, `new_project` `1` → each skipped; 2/2. *NC:* treat the file as unreadable: arm 1 RED; type check only: the `"../x"` entry read: arm 2 RED. **TC-4590**
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
- **LLR-4407.18 — Unwanted.** If the pad is unchanged since its last read or write and the Inbox holds no pending record or pending drop, then the system shall not write the store.
  Threshold: open, move the cursor, wait 1.3 s, `esc` → store bytes and mtime unchanged; with no store, no file created; with a pending record and an unchanged pad, `esc` → exactly 1 store write; 3/3. *NC:* write on close always: arm 1 RED; skip while a record is pending: arm 3 RED. **TC-4598**
- **LLR-4407.19 — Unwanted.** If the store file changed since this app's last read or write when the pad is written, then the system shall write as the pad the fresh pad's notes followed by this window's notes in this window's order, less one copy per fresh-pad note and per unseen entry's `text` of equal text (a multiset, `collections.Counter`), joined by `\n____\n` (note-level union, R2 F-8, SEC-1, ARCH-1).
  Threshold: fresh pad `a|c` with an unseen entry of text `b`, window `a|b|d` → `"a\n____\nc\n____\nd"`; a note deleted here by hand but present in the fresh pad comes back (`a|c`, window `a` → `"a\n____\nc"`); fresh pad `x`, a 3-day-old entry `follow up` this Inbox holds, window `x|follow up` → `"x\n____\nfollow up"` (the re-typed note written); fresh pad `x`, an unseen entry `follow up`, window `x|follow up|follow up` → `"x\n____\nfollow up"` (one copy kept); 4/4. *NC:* last writer wins: `c` lost and `b` back: arm 1 RED; exclude by every fresh `dumped` text: `"x"`: arm 3 RED; exclude by set membership: no copy kept: arm 4 RED. **TC-4599**
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
- **LLR-4407.26 — Withdrawn (ARCH-4)** (LED.4): flagged notes are removed; a failed store write after a dump's board save keeps a pending record instead (LLR-4407.39, LLR-4407.40, LLR-4407.41, LLR-4407.42, LLR-4405.18).
- **LLR-4407.27 — Ubiquitous.** The system shall leave every board file, every `history.jsonl`, `people.json` and `marks.json` byte-identical while the capture view opens, takes typing, writes the pad and closes.
  Threshold: sha256 of 2 board files, their 2 histories, `people.json` and `marks.json` equal before `n` and after typing + 1.3 s + `esc`; 6/6. *NC:* `app.board.save()` on open: RED. **TC-4607**
- **LLR-4407.28 — Event.** When a note is dumped onto a board saved by this version, the system shall write every other task's entry of that board exactly as it was (P-S-19: a load normalisation such as a phase snap is existing behaviour of every save).
  Threshold: a board built with `Board.save` holding tasks without `created` → each old task's `json.dumps(entry, indent=2)` slice equal before and after; n/n. *NC:* back-fill `created` on the other tasks: RED. **TC-4608**
- **LLR-4407.29 — Event.** When a dump, an undo or an image attach changes the pad, the system shall write the store at once (R2 F-7).
  Threshold: after `alt+d`, `alt+u` and `alt+i` each, the stored `pad` equals the pad text with no wait (0 s); 3/3. *NC:* leave it to the 1.0 s debounce: RED. **TC-4609**
- **LLR-4407.30 — Withdrawn (ARCH-4)** (LED.4): the flagged-note notice; the pending record's notice is LLR-4407.40.
- **LLR-4407.31 — Withdrawn (ARCH-4)** (LED.4): the rail's flag line (P-V-8 string) is removed with flagged notes.
- **LLR-4407.32 — Withdrawn (ARCH-4)** (LED.4): no flagged note is left in the pad to refuse (P-V-10 string removed); the note leaves the pad as on success.
- **LLR-4407.33 — Withdrawn (ARCH-4)** (LED.4): the store has no `flagged` key (LLR-4407.2).
- **LLR-4407.34 — Withdrawn (ARCH-4)** (LED.4): no flag to drop; a pending record leaves the Inbox at the first successful pad write (LLR-4407.41).
- **LLR-4407.35 — Unwanted.** If the store file is larger than `STORE_MAX_BYTES` (8 388 608 bytes), then the system shall treat it as unreadable after reading at most 8 388 609 bytes of it (P-S-3).
  Threshold: a store of 8 388 609 bytes → `load_report["unreadable"]` True, the pad empty, at most 8 388 609 bytes read (spy on the read); a store of 8 388 608 valid bytes → read normally; 2/2. *NC:* `read_bytes()` of the whole file: the byte-count arm RED. **TC-4675**
- **LLR-4407.36 — Unwanted.** If an unreadable store file is larger than `STORE_MAX_BYTES`, then the system shall not copy it aside.
  Threshold: a store of 8 388 609 bytes → no `inbox.json.corrupt`; `load_report["backup"]` None; after a pad change the file's bytes unchanged (LLR-4407.9); 3/3. *NC:* `keep_aside` on it: a `.corrupt` copy: RED. **TC-4676**
- **LLR-4407.37 — Unwanted.** If a store write would hold more than `STORE_MAX_BYTES`, then the system shall leave the file and the in-memory store unchanged and show `inbox.json could not be saved: inbox.json would hold <n> bytes, over the 8388608-byte limit, so it was not written`.
  Threshold: a pad of 8 400 000 characters, wait 1.3 s → notice exact (n the would-be byte count); file bytes and `app.inbox.pad` unchanged; 3/3. *NC:* no write cap: a 8.4 MB store written: RED. **TC-4677**
- **LLR-4407.38 — Unwanted.** If the store file is unreadable when first loaded and no copy could be kept, then the system shall start with an empty pad and show `inbox.json could not be read and no copy could be kept; the pad starts empty.` (P-V-6).
  Threshold: `keep_aside` patched to return None on `{"pad": 5}`, and a store of 8 388 609 bytes → that notice, `markup=False`, severity `warning`; pad empty; 2/2. *NC:* the LLR-4407.8 text with `None` as the backup name: RED. **TC-4678**
- **LLR-4407.39 — Unwanted.** If the store write fails after a dump saved its board, then the system shall keep that dump's entry as a pending record of the app's Inbox (ARCH-4).
  Threshold: `write_atomic` failing once, dump N2 → `Course` holds the task; the pad no longer holds N2 (the dump succeeded, LLR-4404.6); `app.inbox.pending` holds 1 record whose `task` is the new task's id; `inbox.json` bytes unchanged; 4/4. *NC:* no pending record: the entry never reaches the store and `alt+u` cannot reach the dump: arm 3 RED. **TC-4679**
- **LLR-4407.40 — Unwanted.** If the store write fails after a dump saved its board, then the system shall show `<project> · <board> got the task, but inbox.json could not be saved: <error> — it is retried at the next save.`
  Threshold: the TC-4679 dump → notice starting `Module 4 · Volumes · Course got the task, but inbox.json could not be saved: ` and ending ` — it is retried at the next save.`, `markup=False`, severity `warning`; 1/1. *NC:* the generic save notice only: RED. **TC-4680**
- **LLR-4407.41 — Ubiquitous.** The system shall apply the Inbox's pending records and pending drops, in the order they were made, to the store as the file holds it at the start of each later pad write.
  Threshold: pad `a|b`, `b` dumped with the write failing, then `x` typed in a new note (window `a|x`) and 1.3 s waited → the stored pad `"a\n____\nx"`, `dumped` holds `b`'s entry, `pending` empty; the same with another window having added `c` before the retry → the stored pad `"a\n____\nc\n____\nx"`; 3/3. *NC:* retry only at the next dump: arm 1 RED. **TC-4681**
- **LLR-4407.42 — Unwanted.** If the Inbox holds a pending record or pending drop when the capture view opens, then the capture view shall fill the pad with the store's pad less the first note equal to each pending record's `text` and with each pending drop's note appended (`Inbox.pad_now`).
  Threshold: dump N2 with the store write failing, `esc` twice (closed unsaved), `n` → the pad lacks N2; 1/1. *NC:* fill from the store's pad: N2 back and a second `alt+d` makes a duplicate task: RED. **TC-4682**
- **LLR-4407.43 — Unwanted.** If a string of the store file will not encode as UTF-8 (a lone surrogate from a JSON escape), then the system shall treat the file as unreadable (SEC-2).
  Threshold: `{"pad": "a\ud800b"}` (the 6-character JSON escape) → `load_report["unreadable"]` True, `inbox.json.corrupt` byte-equal, pad `""`; a store whose `dumped` entry's `text` holds `\udfff` → unreadable; then typing and 1.3 s → 0 exceptions and the store written; 3/3. *NC:* no encode probe at the door: `UnicodeEncodeError` at the first write ends the app: arm 3 RED. **TC-4683**
- **LLR-4407.44 — Unwanted.** If the store text to write will not encode as UTF-8, then the system shall leave the file and the in-memory store unchanged and show `inbox.json could not be saved: inbox.json holds a character that cannot be saved (<reason>), so it was not written` (SEC-2: every caller catches `OSError` only).
  Threshold: an Inbox whose pad is set in the test to `"\ud800"`, then `write_pad` → `OSError` (not `UnicodeEncodeError`) with text `inbox.json holds a character that cannot be saved (surrogates not allowed), so it was not written`; `write_atomic` called 0 times; no `.inbox.json.*.tmp` left; 3/3. *NC:* the encode error escapes as `ValueError`: RED. **TC-4684**
- **LLR-4407.45 — Unwanted.** If reading the store fails with `OSError` at a load or a refresh, then the system shall keep the store stamp it held before that read (SEC-4).
  Threshold: `Inbox._read` patched to raise `OSError` once at load over a store with pad `p` → type `q`, wait 1.3 s → the stored pad `"p\n____\nq"`; a refresh whose read raises once after a second Inbox wrote pad `z` → the next write holds `z` (a union); 2/2. *NC:* take the file's stamp after the failed read: `p` lost: arm 1 RED. **TC-4685**
- **LLR-4407.46 — Unwanted.** If `quit` is pressed while a capture view holds an unsaved pad and the store write fails, then the system shall keep the app running and show `inbox.json could not be saved — quit again exits without saving.` (SEC-5).
  Threshold: a held store lock, `x` typed, `ctrl+q` → the app still runs with the capture view on top; that notice, `markup=False`, severity `warning`; 2/2. *NC:* no guard: the app exits and `x` is lost: RED. **TC-4686**
- **LLR-4407.47 — Event.** When `quit` is pressed again with no other key pressed since that warning, the system shall exit the app.
  Threshold: a second `ctrl+q` → the app exits; a key typed in between → the next `ctrl+q` warns again; 2/2. *NC:* never exits: arm 1 RED. **TC-4687**
- **LLR-4407.48 — Event.** When a dump's entry is written to the store, the system shall remove from the store file's pad, as the file holds it at that moment, the first note whose text equals the entry's `text` (ARCH-1, case D).
  Threshold: this window's pad `a|b`, another window wrote pad `a|b|c`; `b` dumped here (window `a`) → the stored pad `"a\n____\nc"`, `dumped` holds `b`'s entry; on an unchanged file → the stored pad `"a"`; 2/2. *NC:* the typing union for the dump write: `"a\n____\nb\n____\nc"` (`b` back in the pad: a second dump makes a duplicate task): arm 1 RED. **TC-4688**
- **LLR-4407.49 — Event.** When an undo's entry is dropped from the store while the store file's `dumped` holds that entry, the system shall append the restored note to the store file's pad as the file holds it at that moment (ARCH-1, case U).
  Threshold: the file changed by another window to pad `a|c|d`, still holding entry `b`; `b` undone here (window `a|c|b`) → the stored pad `"a\n____\nc\n____\nd\n____\nb"`, `dumped` without `b`; the entry already gone from the file (undone in another window, which restored `b`: fresh pad `a|b`), window `a|b` → the stored pad `"a\n____\nb"` (`b` once); 2/2. *NC:* the typing union for the undo write: `"a\n____\nc\n____\nd"` (`b` lost from the pad, the store and its board): arm 1 RED. **TC-4689**

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
  Threshold: `shutil.copy2` failing on the 2nd image → no `images/<task id>/`, board unchanged, note in the pad; the target's `images/<task id>/` already present (the id source patched to a taken id; ARCH-7, the former LLR-4408.14 case) → this notice, the existing folder and its files untouched, board unchanged; 4/4. *NC:* dump without the image: arm 1 RED; copy into the existing folder: arm 4 RED. **TC-4623**
- **LLR-4408.14 — Withdrawn (ARCH-7)** (LED.4): merged into LLR-4408.13; the exclusive `images/<task id>/` creation already refuses a taken folder, and task ids come from `models._new_id` as on every other creation path.
- **LLR-4408.15 — Unwanted.** If a note names one image file twice, then the system shall move it once and list it once.
  Threshold: `task.images` length 1; 1/1. *NC:* second move raises on the gone source: RED. **TC-4625**
- **LLR-4408.16 — Event.** When a dump with images is undone, the system shall move each of its files from `images/<task id>/` back into the pad images folder, as `<stem>-<k><suffix>` when the name is taken, and name each file as it now is in the restored note's image lines.
  Threshold: files back (bytes equal); a taken name → restored line `img: paste-001-2.png`; 3/3. *NC:* leave the files in the board: the restored lines name missing files: RED. **TC-4626**
- **LLR-4408.17 — Event.** When a dump with images is undone, the system shall remove the emptied `images/<task id>/` folder.
  Threshold: the folder is gone; 1/1. *NC:* folder left: RED. **TC-4627**
- **LLR-4408.18 — Ubiquitous.** The system shall read an image line only when its name passes the image-name rule (§1: 1 to 128 characters, no surrounding whitespace, no `/`, `\`, `:` or control character, not `.` or `..`, a lower-case suffix in `IMAGE_EXTS`, no Windows reserved name in the stem with trailing spaces removed; P-S-10, SEC-7).
  Threshold: `img: a.png` yes; `img: ../a.png`, `img: C:\a.png`, `img: sub/a.png`, `img: a.svg`, `img: a` no; `img: con.png`, `img: a\x07.png`, a 129 × `a` + `.png` name, `img:  a.png` (a leading space in the name) no; `img: con .png`, `img: CONIN$.png`, `img: com0.png`, `img: lpt¹.png` no; `img: console.png`, `img: com10.png` yes; 16/16. *NC:* allow `/`: the traversal arm RED; no device-stem check: the `con.png` arm RED; the stem not right-stripped: the `con .png` arm RED. **TC-4628**
- **LLR-4408.19 — Unwanted.** If a clipboard file's own name fails the image-name rule, then the system shall copy it into the pad images folder as `image<suffix>` (its lower-case suffix; `image-<k><suffix>` when taken) (P-S-10).
  Threshold: a clipboard file `con.png` → the line `img: image.png`, the copy's bytes equal the source's, the source unchanged; with `image.png` present → `img: image-2.png`; 2/2. *NC:* copy under the own name: a line the dump can never read: RED. **TC-4629**
- **LLR-4408.20 — Unwanted.** If the pad images folder or a task's images folder is a symbolic link or a junction, or that task folder does not resolve to a folder directly inside its board's `images` folder, then the system shall copy the dump's or the undo's image files without removing any source file (SEC-6: `move_project`'s link check).
  Threshold: `inbox-images` made a junction to a folder J holding `a.png`, a note with `img: a.png` dumped → the task's copy present and `J/a.png` still present; a dumped task's `images/<id>` made a junction to a folder J2 holding `a.png`, then undone → `a.png` copied into the pad images folder and `J2/a.png` still present; with plain folders → the sources removed as before (LLR-4408.10, LLR-4408.16); 3/3. *NC:* unlink with no link check: `J/a.png` gone: arm 1 RED. **TC-4650**

### 4.9 Colour, mentions and untrusted text (HLR-4409)

- **LLR-4409.1 — Ubiquitous.** The pad shall colour the notes' colour spans live, as the task editor's notes field does (Inc C's `InkArea` highlight map).
  Threshold: `::b:: x ::` → the cells of `x` carry `HEX["blue"]`, the marker cells `HEX["dim"]`; 2/2. *NC:* a plain `TextArea`: RED. **TC-4631**
- **LLR-4409.2 — Ubiquitous.** The system shall keep every colour span and `@mention` of a note byte for byte in the dumped task's notes.
  Threshold: notes equal the expected string; `views.notes_text` of them colours `x` blue; 2/2. *NC:* strip markers from the notes: RED. **TC-4632**
- **LLR-4409.3 — Unwanted.** If a dumped title or notes contain control characters, then the system shall remove them (`models.strip_controls`) before the task is added.
  Threshold: a note titled `"\x1b[2J T"` with notes `"a\x07b"` → title `"[2J T"` (the ESC byte removed), notes `"ab"`; no character below 0x20 other than `\t`/`\n`, no DEL and no C1 byte remains; 2/2. *NC:* raw text: RED. **TC-4633**
- **LLR-4409.4 — Unwanted.** If a note, a project name or a board name holds Rich markup, then the capture view shall draw it as literal text in the rail, the review list, the head row and every notice.
  Threshold: note title `[red]x[/red] [@click=app.quit]q` → literal in the rail row and the review row; a project named `[b]P[/b]` → literal in its rail option, and, created with `alt+n`, in the dump notice (P-V-9: the notice holds no note title); the app still runs; 4/4. *NC:* `Text.from_markup(title)`: RED. **TC-4634**
- **LLR-4409.5 — Ubiquitous.** The system shall write the pad to the store with control characters removed.
  Threshold: a pasted `\x1b` and `\x9b` → absent from the stored `pad`; 2/2. *NC:* raw write: RED. **TC-4635**

## 5. Acceptance tests (black-box, keys and dialogs, Textual pilot)

- **AT-4401** (K-1, K-2) — registry of 2 synthetic boards; `n` → the capture view at 118x30 with an empty pad: the ghost example, the hint row `____ ↵ new note · alt+l divider`, head `CAPTURE  0 notes …`. Type `Golden set answer key`, `enter`, `____`, `enter` → the divider row draws as a rule, the one-time notice shows, head `2 notes`; type `Pilot stores`; `alt+l` (a divider and a new line); `esc`. Store holds the pad verbatim and `divider_notice: true`; board, history, `people.json`, `marks.json` bytes unchanged. Repeat at 80x24: the rail sits below the pad.
- **AT-4402** (K-3, K-4, K-6) — boards `Client A` (projects `Eval harness`, `Pilot rollout`) and `Course` (`Module 4 · Volumes`). Pad `Volume lab fails on WSL\nthe oracle script expects /mnt/c\nimg: board-0938.png` (the image in `inbox-images/`): the rail names `Module 4 · Volumes · Course` with `why volume · oracle · script`; `alt+d` → `Course`'s file holds the task titled `Volume lab fails on WSL`, notes `the oracle script expects /mnt/c`, `created` stamped, the image in `images/<id>/`; the note is gone from the pad; the notice `Dumped → Module 4 · Volumes · Course   ·   alt+u undo`.
- **AT-4403** (K-4) — a note whose best hit is weak: the rail shows `+ new project`; `alt+o` cycles to the weak hit and back; `alt+n`, `tab` → `Course` (P-V-1), type `Contracts pilot`, `enter` → `Course` holds the project and the task in one write; a duplicate name is refused with its notice.
- **AT-4404** (K-4) — two dumps; `alt+u` → the second task leaves its board and the note returns at the pad's end after a divider; `alt+a`, `u` → the first undone too; a third `alt+u` → `Nothing to undo.`; an entry dated 8 days ago is dropped from `dumped` at the next write.
- **AT-4405** (K-1 C) — 4 notes (one new-project); `alt+a` → 4 rows, 3 checked; `space` on the new-project row → refused; `o` on row 1; `d` → 3 tasks on their boards, `Dumped 3 of 3 checked`, the pad holds the 4th note.
- **AT-4406** (K-5) — `inbox.json` holding `{"pad": 5}` → `n` shows the empty pad and the set-aside notice, `inbox.json.corrupt` equals the bad bytes; a held `inbox.json.lock` → typing then waiting gives the save notice and the pad keeps the text; `esc` warns once, `esc` again closes. A store write failing right after a dump → the task is on its board, the note leaves the pad, the notice says the save is retried; the next successful write stores the dumped entry and `alt+u` undoes that dump (ARCH-4: no flagged note).
- **AT-4407** (HLR-4409, K-6) — note `Vendor call\n::b:: ask the vendor :: @username_subject` (P-V-11: the span line is a notes line, not the title) with a clipboard image (patched `grab_clipboard_image`) via `alt+i`; the pad shows `ask the vendor` in blue; dump → the task notes keep the span and mention verbatim; a note titled `[red]x[/red]` shows literally in the rail, and a project named `[b]P[/b]` (made with `alt+n`) literally in the dump notice (P-V-9).
- **AT-4408** (K-5, D1) — a second window (a second `Inbox` instance) dumps note `b` and adds note `c` while this pad (holding `a`, `b`) adds `d`: the next write writes the union `a`, `c`, `d` (`b` is an unseen entry), shows the merge notice, and no task is created twice. ARCH-1 arms, each with the file changed by the second window first: (D) this pad `a|b` dumps `b` while the second window's pad is `a|b|c` → the stored pad `a|c`, `b` never back; (U) this window undoes its dump of `b` over a fresh pad `a|c|d` → the stored pad `a|c|d|b`, the note `b` once; (R) a note `follow up` re-typed here, whose earlier dump this window already knew → kept in the stored pad.

## 6. Slice of functions to change (named and counted)

| # | File | Unit | Change |
|---|---|---|---|
| 1 | inbox.py | constants `INBOX_NAME`, `IMAGES_NAME`, `KEEP_DAYS`, `STORE_MAX_BYTES` (P-S-3), `IMAGE_NAME_MAX`; divider, stamp and task-id regexes (no `SUGGEST_CHARS`: P-T-1 / P-S-13) | new |
| 2 | inbox.py | `is_divider(line)` | new |
| 3 | inbox.py | `parts(text)` → line ranges; `notes(text)`; `note_at(text, row)`; `note_count(text, row)` | new |
| 4 | inbox.py | `note_task(text)` → (title, notes, image names) | new |
| 5 | inbox.py | `without_note(text, part)` / `with_note(text, note)` (pad edits of dump and undo) | new |
| 6 | inbox.py | `union_pads(fresh_pad, unseen_texts, mine)` (R2 F-8; multiset, SEC-1) | new |
| 7 | inbox.py | `Inbox` class: `__init__`, `_hold`, `_stamped`, `load`, `refresh`, `_read`, `_commit`, `_set_aside`, `_prune` | new |
| 8 | inbox.py | `Inbox.write_pad` (record / drop applied to the fresh state, pending records retried, ARCH-1/ARCH-4), `Inbox.pad_now`, `Inbox.last_dump`, `Inbox.mark_notice` (no `Inbox.flag`: ARCH-4) | new |
| 9 | inbox.py | `attach_images(folder, grabbed)` → names or a notice | new |
| 10 | inbox.py | `dump_note(target, project_id, new_name, text, folder, project_name="")` (P-S-1) and `entry_for(outcome, note, board_path, now)` (P-S-15) — open board: `app.board.add_task`; other board: fresh `peek_board` under `file_lock`, stamp check, `models.stamp`, `save_atomic`, birth record; images copy; roll-back | new |
| 11 | inbox.py | `undo_dump(entry, open_board, folder)` — task/project removal (same two board paths), images back | new |
| 12 | suggest.py | `STOP`, `WORD_RE`, weights, cuts, `NOTE_CHARS` (P-T-1), `DOC_CHARS` (P-T-5); `fold`, `stem`, `words` | new |
| 13 | suggest.py | `Doc`, `Hit`, `Corpus`, `corpus(lanes, marks)` (with the 100 000-char document cap; idf, vectors and norms once per build, ARCH-6) | new |
| 14 | suggest.py | `_idf`, `suggest(note, corpus)` (with the 10 000-char cap; ties by name case-folded, P-T-3) | new |
| 15 | suggest.py | `level`, `bars`, `options(hits)` | new |
| 16 | app.py | `PadArea(InkArea)`: divider rule in `render_line`, ghost placeholder | new |
| 17 | app.py | `CaptureView(Screen)`: compose, mount, paint (head, rail, hint, keys), debounce write, close/unmount write, actions dump/other/new/board/review/image/undo/divider, name field | new |
| 18 | app.py | `ReviewList(ModalScreen)`: rows, move, toggle, other, dump, undo, back | new |
| 19 | app.py | `rail_rows(...)`, `hit_text(...)`, `CAPTURE_KEYS`, `REVIEW_KEYS`, `CAPTURE_HINT`, `GHOST` | new |
| 20 | app.py | `TaskboardApp.__init__` (load the `Inbox` beside the registry), `action_capture`, `action_quit` (the unsaved-pad guard, SEC-5) | changed/new |
| 21 | app.py | `TaskboardApp.check_action` (gate `capture`, refused under the home, ARCH-3; the capture view holds the seat) | changed |
| 22 | keymap.py | `KEYMAP` entry `n` | changed |
| — | README.md | key table row for `n` (docs, not a source file) | changed |

Unchanged on purpose (to verify at E2): `Board.add_task` (stamps and writes the birth record; open board only), `history.append`, `Board.image_dir`,
`board_lanes`, `peek_board`, `file_lock`, `keep_aside`, `write_atomic`, `save_pil_image`,
`grab_clipboard_image`, `InkArea`/`ink_highlights`, `visible_text`, `highlight_segments`, `people.py`,
`marks.py`, `models.py`. inbox.py imports no `modals` and no Textual module (ARCH-8): its visible text is
`views.highlight_segments` joined.
**Count: 22 units in 4 source files** (2 new: `taskboard/inbox.py`, `taskboard/suggest.py`; 2 changed:
`taskboard/app.py`, `taskboard/keymap.py`) — within the 4-source-file budget (§8 F-1).

**Proposed file-ownership groups for E2/E4:**
- **G-S (store)** — `taskboard/inbox.py`: units 1–11 (HLR-4402 parse, HLR-4404/4405 board+image operations, HLR-4407, HLR-4408 file side).
- **G-T (suggest)** — `taskboard/suggest.py`: units 12–15 (HLR-4403 layer 0).
- **G-V (view)** — `taskboard/app.py` + `taskboard/keymap.py` + `README.md`: units 16–22 (HLR-4401, HLR-4402 drawing, HLR-4403 rail, HLR-4406, HLR-4409, the key seat).
- Seams the orchestrator fixes first: `Inbox` public API and `note_task`/`notes`/`note_at` signatures (G-S ↔ G-V); `corpus`/`suggest`/`options` signatures and `Hit` (G-T ↔ G-V); `dump_note`/`undo_dump` return shape (result or notice) (G-S ↔ G-V).

## 7. Counts

US 1 · HLR 9 · LLR ids 212, active 205, withdrawn 7 (active by group — 4401: 19, 4402: 18, 4403: 31, 4404: 34, 4405: 19, 4406: 17, 4407: 43, 4408: 19, 4409: 5) · AT 8.
(E2 correction pass, LED-2026-11-01-incK.3: 12 LLRs added — LLR-4401.17, LLR-4401.18, LLR-4403.27, LLR-4403.28, LLR-4405.15, LLR-4405.16, LLR-4405.17, LLR-4407.35, LLR-4407.36, LLR-4407.37, LLR-4407.38, LLR-4408.19; none withdrawn.)
(E3 round 1, LED-2026-11-01-incK.4: 20 LLRs added — LLR-4401.19, LLR-4403.29, LLR-4403.30, LLR-4403.31, LLR-4404.34, LLR-4405.18, LLR-4405.19, LLR-4406.17, LLR-4407.39, LLR-4407.40, LLR-4407.41, LLR-4407.42, LLR-4407.43, LLR-4407.44, LLR-4407.45, LLR-4407.46, LLR-4407.47, LLR-4407.48, LLR-4407.49, LLR-4408.20; 7 withdrawn — LLR-4407.26, LLR-4407.30, LLR-4407.31, LLR-4407.32, LLR-4407.33, LLR-4407.34 (ARCH-4), LLR-4408.14 (ARCH-7).)

## Recorded risks (E3 round 1; the orchestrator moves them to BACKLOG at E5)

- **RISK-ARCH-4 — exit before a retry.** A dump whose board save succeeded and whose store write failed is held only in memory (a pending record). An exit, crash or second esc-close of the app before any successful retry leaves the note in the on-disk pad and no `dumped` entry; dumping it again in a later session makes a second task.
- **RISK-SEC-2 — `Board.save` truncation (pre-existing, `models.py`).** `Board.save` is a plain `Path.write_text`, which truncates the file before it encodes; a board whose own strings carry a lone surrogate is left at 0 bytes by its next save. Inc K keeps surrogates out of its dumps (LLR-4404.34, LLR-4407.43); moving the open board to `save_atomic` is out of scope (S-a).
- **RISK-SEC-9 — large images under another board's lock.** `_dump_other` copies images while holding the target board's lock without the heartbeat `move_project` uses, and `attach_images` has no size cap: a multi-GB file can hold the lock past `LOCK_STALE` (10 s); the final stamp check still refuses the dump, a small window remains and disk use is unbounded.
- **RISK-SEC-10 — pasted control bytes until the debounce (existing behaviour).** A paste into the pad keeps ESC and C1 bytes in the document and its rendered line until the 1.0 s write strips them (the task editor's notes field behaves the same today).
- **RISK-SEC-11 — the rail scores every note (perf).** Wide mode scores every note, drawn or not. Measured cheap after ARCH-6 (0.10 ms per note at 15 documents, 2.7 ms at 300); scoring only the drawn notes is deferred.
- **RISK-P-S-11 — residual link races on the attach paths.** `shutil.copy2` follows a link created between `_free_name`'s check and the open; `models.save_pil_image` checks `exists()`, which is False for a dangling link. SEC-6 (LLR-4408.20) covers the unlink paths of dump and undo only.
- **RISK-P-S-12 — silent leftovers on the image paths.** A pad copy that cannot be removed after the save, a file that cannot be moved back on undo, and a "gone" undo leave files without a notice (BACKLOG: an UndoOutcome `left` list).
- **RISK-P-S-17 — a missing board blocks older undos.** `alt+u` always takes the newest entry; a board on an offline drive answers "could not be changed" for up to 7 days.

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
- **F-8 — a stale pad (two windows).** `people.json`'s merge is per record; a pad is free text, and last-writer-wins would bring back notes dumped in the other window (duplicate tasks). *Proposed:* a three-way merge at note level when the file changed since the base (LLR-4407.19..4407.22); verbatim otherwise. The same note dumped in two windows before either writes still makes two tasks (accepted risk). **Ruling R2: AMENDED** — no 3-way merge: a note-level union of the fresh pad and this window's notes not in the fresh pad nor in a fresh `dumped` entry (LLR-4407.19, LLR-4407.20, LLR-4407.21, LLR-4407.22 reworded). **E3 round 1 (SEC-1, ARCH-1):** only the pad's typing write unions, excluding by multiset the unseen entries only (LLR-4407.19); a dump and an undo are applied to the fresh state (LLR-4407.48, LLR-4407.49).
- **F-9 — undo across sessions.** The newest `dumped` entry may be days old and its task edited since. *Proposed:* undo refuses an edited task (LLR-4405.10); a task that is gone gives the note back only (LLR-4405.8). **Ruling R2: ACCEPT.** **E3 round 1 (SEC-3):** "edited" is any field of the whole record, and a task another task depends on is refused too (LLR-4405.10, LLR-4405.19).
- **F-10 — pens in the pad.** K-4 carries colour spans, but K-1..K-6 do not give the pad Inc C's pen keys. *Proposed:* live colour display only (LLR-4409.1); `alt+1..6`/`alt+c` in the pad are out (R0-11); a backlog item if wanted. **Ruling R2: ACCEPT.**
- **F-11 — options list.** The proto always added `+ new project` as an extra option (4 options). The commission says "top + up to 2 alternatives". *Proposed:* at most 3 options; `+ new project` is an option only as a weak top; `alt+n` always reaches a new project (LLR-4403.13). Archived projects, archived tasks and project-less tasks stay out of the documents (the proto's rule; the commission does not mention them) (LLR-4403.3, LLR-4403.5). **Ruling R2: ACCEPT.**
- **F-12 — a failed write at close loses text.** *Proposed:* the first `esc` after a failed write keeps the view open with a warning; a second `esc` closes (LLR-4407.24, LLR-4407.25). The dump's two writes (board, then store) are not atomic together: a store failure keeps the dump in memory and writes it later (LLR-4407.26); a crash between the two writes leaves the note in the pad (accepted risk). **Ruling R2: ACCEPT** — the board-then-store pair is a recorded risk; a failed store write after the board save keeps the note in the pad, flagged (LLR-4407.26 rewritten; LLR-4407.30, LLR-4407.31, LLR-4407.32, LLR-4407.33, LLR-4407.34 added). **E3 round 1 (ARCH-4): flagged notes removed** — those 6 LLRs withdrawn; a pending record of the app's Inbox replaces them (LLR-4407.39, LLR-4407.40, LLR-4407.41, LLR-4407.42, LLR-4405.18); the exit-before-retry risk is recorded (§Recorded risks).
- **F-13 — exact UI strings are E1 proposals.** The commission fixes only the hint row, and R1-1 changes it to `alt+l divider` (to be flagged to the operator). The head, ghost, notices, review rows and the review's close after `d` follow the proto; UX review at E3 may tune them, and changes go through the ledger. **Ruling R2: ACCEPT** — flag in the final report.
