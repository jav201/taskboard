# Inc K — orchestrator rulings before E1 (R0)

The orchestrator wrote these at E0 so E1 and E2 start from one reading of the commission (§Inc K, K-1..K-6).
Each ruling names the commission text it reads and why. E1 may propose a change to any of them as a
finding; only the orchestrator changes a ruling.

| Id | Commission text | Ruling | Why |
|---|---|---|---|
| R0-1 | K-1 "key `n`" | `n` on the main app opens the capture view. It is free in `keymap.KEYMAP` (checked at `545c18a`; `n` exists only as screen-local bindings in BoardsHome, PeopleDirectory, MarksManager). It is declared in `KEYMAP` beside `N`, following `N`'s pattern. | One seat for keys (keymap law). |
| R0-2 | K-4 "`u` undoes the last dump" | Inside the pad (a text field) undo is `alt+u` (as in variant A); in the batch review list (not a text field) it is `u`. Every pad command is `alt+letter`: `alt+d` dump, `alt+o` other, `alt+n` new project, `alt+a` review, `alt+i` image, `alt+u` undo, `alt+enter` divider, `esc` close. | Modal-key law: inside text fields, `alt+letter`; a bare `u` in the pad is typing. |
| R0-3 | K-2 "a line holding only 4 or more underscores" | A divider line is a line whose content, with trailing whitespace removed, is 4 or more `_` and nothing else (leading whitespace is not allowed). The text stays `____…` in the document and in `inbox.json`; the rule is a rendering of it. Notes = the pad split at divider lines; a note whose text is only whitespace is not a note. | Keeps the stored text the user typed; one parse rule for count, rail, review and dump. |
| R0-4 | K-2 "renders as a full-width rule the moment enter is pressed after it" | A divider line is drawn as a full-width rule whenever the cursor is not on that line (pressing `enter` after it moves the cursor off it). While the cursor is on it, the raw underscores show, so it stays editable. | Exact trigger the operator described, and still editable. |
| R0-5 | K-2 "`alt+enter` inserts a divider" | Bind `alt+enter` as specified. RISK recorded: Windows Terminal binds `alt+enter` to toggle fullscreen by default, so the key may never reach the app there; the `____` + `enter` path is the primary one and must work alone. No extra alias is added (scope); the risk goes to the operator in the final report. | Do not silently widen scope; fail loud on the risk. |
| R0-6 | K-2 "a one-time notice" | "One time" persists across sessions: a flag in `inbox.json`. | A notice that returns every session is not one-time. |
| R0-7 | K-3 weights | The commission's weights win over `suggest.py` where they differ (name ×3, titles ×2, `@people` ×2, mark names ×1, notes ×1; single-shared-word score halved; below the medium cut → "+ new project"; ties by board order then name; top + up to 2 alternatives). | The commission is the operator's verdict. |
| R0-8 | K-4 "dump" | A dump creates the task through `Board.add_task` (which stamps `created`, Inc L LLR-4301.5) on the target board, and saves that board through the app's existing save path. The task title is the note's first non-blank line; its notes are the rest (colour spans and `@mentions` verbatim). | Inc L handoff; colour/mentions carry by keeping the text verbatim. |
| R0-9 | K-6 "on dump the image moves into the target board's `images/`" | Pad images wait in a folder beside `inbox.json` (`~/.taskboard/inbox-images/`) and are referenced from the note's text; on dump they move to `Board.images_dir(task_id)` (the per-task folder `<board-dir>/images/<task_id>/`) and the task's `images` list points there. | Matches the existing per-task image layout. |
| R0-10 | K-5 "written exactly like `people.json`" | `taskboard/inbox.py` mirrors `people.Directory`: `_commit(change)` = read-modify-write under `boards.file_lock`, atomic write, `keep_aside` when unreadable, fresh re-read before each change. | The pattern is the repo's tested one. |
| R0-11 | scope | Prefer removing a feature over guarding it (skill E3). Anything not in K-1..K-6 is out. | Skill rule. |

## R1 — after the baseline graph (E2a facts, `baseline-notes.md`)

| Id | Fact | Ruling | Why |
|---|---|---|---|
| R1-1 (amends R0-5) | Probe at 545c18a: Textual 8.2.8 `XTermParser` reads the legacy `ESC CR` as plain `enter`; only the kitty form `ESC[13;3u` gives `alt+enter`, which Windows Terminal does not send (it also binds `alt+enter` to fullscreen). `ESC -` parses as `en_dash`, so `alt+-` is unreliable too. | The divider key is **`alt+l`** ("line"); `alt+enter` is NOT bound. The hint row reads `____ ↵ new note · alt+l divider`. Deviation from the commission's verbatim text, flagged to the operator in the final report. | Keymap law: every key shown works. A key the terminal cannot deliver would be a shown key that never works. |
| R1-2 (amends R0-9) | The method is `Board.image_dir(task_id)` (singular, models.py:1018). The editor's `alt+i` is a clipboard paste. | Pad `alt+i` mirrors the editor's clipboard paste; the pad's waiting folder stays `~/.taskboard/inbox-images/`; on dump files move to `Board.image_dir(task_id)`. | Same meaning as the editor (no key clash in meaning). |
| R1-3 | `Board.save` is a plain `write_text`; the only cross-board write is `move_project` (fresh `peek_board`, `file_lock` + stamp check, `save_atomic`). | A dump into the OPEN board goes through `app.board` and the app's save path; a dump into ANOTHER board follows `move_project`'s pattern (fresh read under `file_lock`, stamp check, `save_atomic`). | Avoid last-save-wins between two Board objects on one file. |
| R1-4 | `_undo_stack` covers the open board only; a task add pushes nothing; `switch_board` clears it. | Undo of a dump uses its own record: the last entry of `inbox.json` `dumped` (board path, task id, note text, image names). | The existing stack cannot carry a cross-board dump. |
| R1-5 | Live colour overrides `InkArea._build_highlight_map` (recolours text only). | The divider rule is drawn by a separate mechanism (a TextArea subclass's line render), not the highlight map; colour reuses Inc C's highlighter. | The highlight hook cannot replace a line's glyphs. |
| R1-6 | `check_action` has two hand-written tuples (app.py:1398, 1403-1405); the README key table is test-pinned. | The new action/screen is added to both tuples and to the README row for `n`. | Keys gate and pinned docs. |

## R2 — rulings on the E1 findings (01-requirements.md §8)

| Finding | Ruling |
|---|---|
| F-1 | ACCEPT. Screens live in app.py; 4 source files: inbox.py, suggest.py, app.py, keymap.py (+ README row). |
| F-2 | ACCEPT. Open board: `Board.add_task` + the app's save. Other board: fresh read under `file_lock`, `models.stamp` for `created`, stamp check, `save_atomic`, birth record after the save. |
| F-3 | ACCEPT. Title = visible text (colour markers removed) of the first non-blank, non-image line; the notes keep their markers verbatim. |
| F-4 | ACCEPT. The count includes the empty segment after a final divider (the note being started); review and dump list only non-empty notes. |
| F-5 | ACCEPT. The dumped task takes the target board's first phase. |
| F-6 | ACCEPT. Attach COPIES (or writes a bitmap) into `inbox-images/`; never moves the user's own file. Note text refers by a bare `img: <name>` line. On dump the inbox copy moves to `Board.image_dir(task_id)`. |
| F-7 | ACCEPT. Pad stored as one string; write after 1 s idle, on close, on exit, on dump/undo/attach; never when unchanged. |
| F-8 | AMEND — no 3-way merge (prefer simpler). On a write, re-read fresh; if the file changed since our last read, the pad written is the fresh pad's notes followed by our notes whose exact text is neither in the fresh pad nor in a fresh `dumped` entry (note-level union, our order kept). No note text is ever dropped silently. |
| F-9 | ACCEPT. Undo acts on the last `dumped` entry; task gone → the note returns to the pad only; task changed since the dump (title or notes differ) → refused with a toast, nothing changes. |
| F-10 | ACCEPT. Out: pens/palette in the pad. In: live colour display. |
| F-11 | ACCEPT. |
| F-12 | ACCEPT; the non-atomic board-then-store pair is a recorded risk (store write after the board save; a failed store write after a successful board save is reported, and the note stays in the pad flagged — the operator can delete it). |
| F-13 | ACCEPT; flag in the final report. |
