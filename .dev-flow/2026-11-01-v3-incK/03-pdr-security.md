**Verdict: FAIL** — HIGH 0 · MAJOR 3 · MEDIUM 2 · LOW 6 · INFO 4

# Inc K — PDR security review (E3 round 1, security-reviewer)

FAIL because three MAJOR findings are open (SEC-1, SEC-2, SEC-3). Each one loses user data on a path the design describes, and each has a small fix. Two of the fixes remove behaviour instead of adding guards. Every mitigation below is `planned`. I re-check them at the E3 re-gate, and again at the increment gate against code and tests.

## Scope reviewed

- Commission §Inc K (K-1..K-6), `00-orchestrator-rulings.md` (R0, R1, R2), `03-pdr-rulings.md` (rounds 0a..0c, which override older text), `01-requirements.md` (192 LLRs, 8 ATs), `graph-interfaces.cw.md`, `graph-proto-S.cw.md`, `graph-proto-V.cw.md` (painters, `_flush`, `_dump`, `action_undo`, `on_unmount`, markup rule), with `graph-proto-T.cw.md` and `e2-trace.txt` skimmed.
- Base code read at the worktree head (base code `545c18a`):
  - `boards.py`: `keep_aside`, `file_lock`, `move_project` with its junction check at :791-796 and its heartbeat at :784, and `peek_board`.
  - `models.py`: `IMAGE_EXTS` and its startfile comment at :495, `strip_controls`, `clean_strings`, `_clean_clipboard_text`, `save_pil_image`, `write_atomic`, `Task`, `Board.load`, `Board.save`, `save_atomic`, `add_task`, `delete_task`.
  - `people.py`: `load`, `refresh`, `_read`, `_commit`, `_set_aside`.
  - `modals.py`: `InkArea` and its SEC-6 surrogate guard.
  - `keymap.py`: `key_line`, and `q` → `quit`.
  - The Textual 8.2.8 win32 driver, at :288-291.
- Probes: read-only, run with `C:/Users/jjgh8/anaconda3/python.exe -I` (3.12.7) from `%TEMP%/incK-pdr-security/` (p1..p5). Each one printed `taskboard.__file__` = `C:\Users\jjgh8\Github\taskboard-wt\capture-proto\taskboard\__init__.py`. They used temp folders and synthetic data only.

## Findings

### SEC-1 — the union drops a re-typed note whose text equals ANY dumped entry kept for 7 days  [MAJOR]
- **Anchor:** `union_pads` (graph-interfaces; graph-proto-S `union_pads`). `Inbox.write_pad` calls it as `union_pads(base.pad, [e.text for e in base.dumped], pad)`. LLR-4407.19. Ruling R2 F-8: "No note text is ever dropped silently."
- **What is wrong:** the union suppresses this window's note when its exact text equals the `text` of any fresh `dumped` entry. `dumped` holds the last 7 days of dumps, including entries this window already knew about. Recurring notes are common: `follow up`, `call vendor`, `send minutes`. Take a note dumped on Monday. On Thursday the user types the same text again as a new note. If any other window wrote the store in between (any keystroke there is enough), the next write removes Thursday's note. The pad text is replaced and the merge notice says the notes were "merged".
- **Evidence:** `executed`. p4.py is a reference implementation of the specified `union_pads`. It reproduces TC-4599 (`'a\n____\nc\n____\nd'`). In the scenario fresh pad `x`, dumped `["follow up"]`, window `x\n____\nfollow up`, it returns `'x'`, so the note is gone.
- **Proposed change:** only suppress a note when the other window dumped it, which is what the rule is for (AT-4408).
  - `write_pad` passes `fresh_new = [e.text for e in base.dumped if (e.task, e.board) not in {(m.task, m.board) for m in self.dumped}]`. These are the entries this window has not seen.
  - `union_pads` removes mine's notes by multiset count (`collections.Counter`), not by set membership. Two typed copies against one foreign dump then keep one copy.
  - AT-4408 still passes, because `b`'s entry is unknown to this window.
  - New arm for TC-4599: this window holds entry e (`follow up`, 3 days old), the file changed, and this window's pad holds the note `follow up` → the note is written. *NC:* suppress by every fresh `dumped` text → RED.
  - Reword LLR-4407.19: "…nor the `text` of a fresh `dumped` entry that this window's store did not hold…".

### SEC-2 — a lone surrogate in `inbox.json` crashes every store write and can truncate the open board file to 0 bytes  [MAJOR]
- **Anchor:** `Inbox._read` (the load door), `Inbox._commit`, `_dump_open`; G-V `_flush`, `_dump`, `on_unmount`.
- **What is wrong:**
  - JSON lets the escape `"\ud800"` through. `clean_strings` and `strip_controls` keep it, because it is above U+00A0. So the pad, an entry's `text`, and therefore a dumped title or notes can hold a lone surrogate.
  - Store write: `_commit` runs `len(text.encode("utf-8"))` and raises `UnicodeEncodeError`. That is a `ValueError`, not an `OSError`. Every G-V guard is `except OSError` (`_flush`, `_dump`, `on_unmount`), so the exception escapes a timer or key handler, Textual ends the app, and the unsaved pad is lost. This repeats on every launch until the file is edited by hand.
  - Dump into the open board: `live.add_task` → `Board.save` → `Path.write_text` opens the file with `"w"` (which truncates it) and then fails to encode. `_dump_open` catches only `OSError`, so there is no rollback, the app crashes, and the open board's file is left at 0 bytes.
  - Typed and pasted text cannot carry a surrogate, because the win32 driver decodes UTF-16 strictly (textual/drivers/win32.py:290). The store is the new inflow. The repo already treats `\ud800` from a file as reachable (SEC-6, `test_colour_pens.py::TC-4246`).
- **Evidence:** `executed`. p1.py:
  - pad after `clean_strings` = `'a\ud800b'`;
  - encode raises `UnicodeEncodeError`, `isinstance(e, OSError)` False;
  - an existing 46-byte `board.json` is **0 bytes** after `write_text` raises;
  - `write_atomic` raises a non-OSError and leaves `.inbox.json.*.tmp` behind, because its cleanup is `except OSError` only.
- **Proposed change:** remove the surrogate at the door instead of guarding every sink.
  1. In `Inbox._read`, inside the same `try`, add `json.dumps(raw, ensure_ascii=False).encode("utf-8")` and catch `UnicodeEncodeError`. On failure the file counts as unreadable: it is set aside, the pad starts empty, and nothing is lost because `.corrupt` holds the bytes.
  2. As a backstop, `dump_note` refuses a note whose `text.encode("utf-8")` fails, before any write, with `This note holds a character that cannot be saved — nothing dumped.`. `_commit` converts `UnicodeError` into the worded `OSError`, so every G-V `except OSError` holds.
  3. New LLR in HLR-4407: TC `{"pad": "a\ud800b"}` (JSON escape) → `load_report["unreadable"]`, `.corrupt` byte-equal, pad `""`, 0 exceptions on a pad write. *NC:* no encode probe → `UnicodeEncodeError`: RED. New LLR in HLR-4404 for the dump refusal, where the open board's bytes stay unchanged.
  4. BACKLOG, pre-existing and out of scope (`models.py`): `Board.save` truncates any board whose own file carries a surrogate on its next save.

### SEC-3 — undo deletes a task edited in every field but title and notes, up to 7 days later, with no confirmation and no way back  [MAJOR]
- **Anchor:** `undo_dump` / `_undo_open` / `_undo_other` changed-check. LLR-4405.10 ("title or notes differ"). R2 F-9.
- **What is wrong:**
  - `alt+u` works across sessions on the newest entry up to 7 days old. It removes the task unless its title or notes changed.
  - These edits are deleted silently: phase moves (work marked Done), priority, start and due dates, URLs, images attached later in the editor, milestone and mark, archived, pinned, blocked, show_in_present.
  - Other tasks' `depends_on` keep a dangling id, because `delete_task` does not clean them up (models.py:1316).
  - The capture undo is not on `_undo_stack` (LLR-4405.14), so nothing restores the task afterwards. Only the note text comes back.
  - This is an irreversible destructive action, and its only guard ignores most of the record.
- **Evidence:** `read`. The `Task` fields come from p5.py (`executed`): 20 fields, 2 of them compared.
- **Proposed change:** compare the whole record and refuse on any difference. Prefer removing reach over adding prompts.
  - Change the check: `expected = Task(title, project_id=entry.project, phase=board.phases[0], notes, images=[str((board.image_dir(entry.task) / n).resolve()) for n in entry.images], id=entry.task, created=task.created)`, where `title` and `notes` come from `_task_fields`. "changed" ⇔ `dataclasses.asdict(task) != dataclasses.asdict(expected)`, **or** any other task of the board has `entry.task` in `depends_on`.
  - No new store field is needed.
  - Reword LLR-4405.10 to "differs in any field from what its dump wrote, or another task depends on it".
  - TC-4550 arms: phase moved; due date set; a URL added; an image added through the editor; another task depending on it → each `changed`, with board bytes unchanged. *NC:* the title/notes-only check makes the phase arm RED.

### SEC-4 — a read that fails with `OSError` adopts the file's stamp without its content, so the next write overwrites the stored pad  [MEDIUM]
- **Anchor:** `Inbox.load` ("`_read` OSError → None" → unreadable → `_stamped()`), `Inbox.refresh` (graph-interfaces: "unparseable → False, state kept, the new stamp kept"; `people.refresh` maps a read `OSError` to that same branch), `Inbox._commit` (`changed = fresh is not None and before != _stamp`).
- **What is wrong:**
  - The verbatim-versus-union choice rests only on the stamp, and `people.json` has no such rule because it merges per record.
  - At load, the read is not under the lock. A transient `OSError` (sharing or AV lock, another window's replace in flight) gives an empty pad with "no copy could be kept". The stamp of the valid file is taken anyway. The first write then finds the file parseable and its stamp equal, so it writes this window's pad over the whole stored pad, and every stored note is lost.
  - In refresh, a transient `OSError` adopts the new stamp but keeps the old state. The next write then overwrites the other window's notes without a union.
- **Evidence:** `read` (the order is traced from the graph text; no probe).
- **Proposed change:**
  - After a load that did not parse, keep `_stamp = None`. A later write to a file that has meanwhile become parseable then unions (nothing is lost). A still-corrupt file is set aside and written as today.
  - In `refresh`, adopt a new stamp only when the parse succeeded. Keep the "report once" rule on a separate `_bad_stamp`.
  - TC: `_read` patched to raise `OSError` once at load, with a valid store holding pad `p` → type `q`, wait 1.3 s → the stored pad holds both `p` and `q`. *NC:* stamp taken → `p` lost: RED.

### SEC-5 — `quit` from the capture view after a failed write discards the pad with no warning  [MEDIUM]
- **Anchor:** `TaskboardApp.check_action` (LLR-4401.12 keeps `quit` allowed), `CaptureView.on_unmount` ("OSError swallowed"), LLR-4407.24/.25 (the esc-twice guard covers `esc` only).
- **What is wrong:** while the store write fails (busy lock, over the cap, unreadable store), `esc` warns once. `q` (keymap.py:59) or `ctrl+q` exits the app instead. `on_unmount` tries once and swallows the error, so everything typed since the failure is lost with no notice.
- **Evidence:** `read`.
- **Proposed change:**
  - Route `quit` through the same guard. While a capture view is on the stack and `_unsaved()` follows a failed write, the first quit shows `inbox.json could not be saved — quit again exits without saving.` and the second one exits. One extra branch in `check_action` / `action_quit_app`.
  - Widen `on_unmount`'s except to `(OSError, ValueError)` (see SEC-2).
  - New LLR and TC: a held store lock, type, `q` → the app still runs and the notice is shown; `q` again → it exits. *NC:* no guard → exits: RED.

### SEC-6 — the image moves skip `move_project`'s junction check and can unlink files outside the app's folders  [LOW]
- **Anchor:** `_images_back` (copy, then `src.unlink()`), `_drop_pad_copies` (`unlink`), `_copy_images`. Baseline: `move_project` moves only `image_dir(tid)` whose `resolve().parent == (board dir / "images").resolve()` ("a junction or link elsewhere stays", boards.py:791-796).
- **What is wrong:** `lstat` + `S_ISREG` checks only the last component. If `images/<tid>/` or `inbox-images/` is a junction to another folder, undo copies the named photos into F and **deletes the originals** there, and a dump deletes F's targets after copying them. The precondition is a same-user process planting the junction, which is why this is LOW. The repo already defends against this case, so the gap is a parity gap.
- **Evidence:** `read`. `Path.is_junction` exists on 3.12 (`executed`, p5.py).
- **Proposed change:**
  - Before any unlink, require that `folder` is neither a link nor a junction, and that `board.image_dir(tid).resolve().parent == (board.path.parent / "images").resolve()`. Otherwise copy only and never unlink.
  - Extend P-S-11's recorded risk with this note.

### SEC-7 — the device-stem rule misses names older Windows still maps  [LOW]
- **Anchor:** `_image_ok`, LLR-4408.18, requirements §1 image-name rule.
- **What is wrong:** the rule lists `con prn aux nul com1-9 lpt1-9`. Microsoft's reserved list also has `com0`, `lpt0`, `com¹²³`, `lpt¹²³` and `conin$` / `conout$`, and Windows 10 ignores trailing spaces in the stem (`con .png`).
- **Evidence:** `executed`, p3.py. On this build (10.0.26300), `GetFullPathNameW` maps none of the forms that carry an extension, `con.png` included. The rule is defence in depth for Windows 10.
- **Proposed change:** `stem = name.split(".")[0].rstrip(" ").lower()`. Add `com0`, `lpt0`, `com¹`..`com³`, `lpt¹`..`lpt³`, `conin$` and `conout$`. Add one TC-4628 arm for `con .png` and one for `conin$.png`.

### SEC-8 — `entry["board"]` from the store reaches the filesystem before the lane test  [LOW]
- **Anchor:** `CaptureView.action_undo` (samefile against each lane), and `_where(flag["board"], …)` for flagged notes.
- **What is wrong:** `os.path.samefile` stats the store's string. A value of `\\host\share\board.json` makes `alt+u` open an SMB connection, which sends NTLM authentication to that host, before the refusal. The precondition is a same-user write to `inbox.json`.
- **Evidence:** `read`.
- **Proposed change:** test membership first by `os.path.normcase(os.path.abspath(entry["board"]))` against the lane paths, as strings. Call `samefile` only for a lane that matches (or skip it). Apply the same lookup to flags.

### SEC-9 — large images are copied while holding another board's lock, with no heartbeat  [LOW]
- **Anchor:** `_dump_other` (`_copy_images` inside `file_lock`), `attach_images` (no size cap).
- **What is wrong:** `move_project` calls `beat()` after each copy ("a copy can take a while", security S-2/S-8, boards.py:784). `_dump_other` does not. A multi-GB clipboard file saved as `.png` (attach copies any size) can hold the lock past `LOCK_STALE` (10 s), and another taskboard then takes the lock over. The final stamp check still refuses the dump. A small window remains, and the disk use is unbounded.
- **Evidence:** `read`.
- **Proposed change:** keep the heartbeat `file_lock` yields and call it after each copy. Optionally refuse attached files over a cap with a worded notice; the operator can set the value.

### SEC-10 — a paste into the pad keeps ESC and C1 bytes in the rendered line until the debounce write  [LOW]
- **Anchor:** `PadArea` (inherits Textual's `TextArea` paste).
- **What is wrong:** the pasted text goes into the document raw. Its ESC and C1 `\x9b` bytes reach the segments `render_line` produces (Rich drops BEL), and the clean-up comes only with the 1 s write (P-S-8). The task editor's notes field behaves the same today (pre-existing). The pad is where large meeting pastes land, and an uncapped paste also drives the 8 MB store-cap failure path.
- **Evidence:** `executed`, p2.py: after `Paste("p\x1b[2Jq\x07r\x9bs")` the text holds `\x1b` and `\x9b`, and the render segments hold ESC.
- **Proposed change:** `PadArea._on_paste` inserts `models._clean_clipboard_text(event.text)` (`strip_controls` + the existing 100 000-character cap) and stops the event. That is two lines, using the repo's clipboard-text rule. Add a TC with the p2 paste: the pad text holds no `\x1b` with no wait.

### SEC-11 — the rail scores every note, drawn or not  [LOW]
- **Anchor:** `CaptureView` hit cache and `rail_rows` (wide mode lists every note; the rail has about 28 rows).
- **What is wrong:** an 8 MB store or a big paste of tiny notes means one `suggest` call per note at open, and again after each rebuild of the documents. The UI freezes on the user's own data.
- **Evidence:** `read`.
- **Proposed change:** score only the notes the rail can draw (the cursor's note plus those that fit the height), lazily, through the cache that already exists.

### INFO
- **I-1 Retention.** A dumped note's verbatim text (meeting notes can hold personal data or pasted secrets) stays in `inbox.json` for 7 days, even after its task is deleted. An entry stamped in the future is never pruned. `.corrupt` copies are never pruned. Everything is local. Suggest one README sentence ("dumped notes are kept in `~/.taskboard/inbox.json` for 7 days") and dropping `at` values later than now plus a margin.
- **I-2 Public repo.** `jav201/taskboard` is PUBLIC. The design files carry the local profile path (`C:\Users\jjgh8\…`), as earlier batches do. They hold no real name: `username_subject` is used throughout. Synthetic fixtures only. No secrets in any design file (grep: none).
- **I-3 Two windows pressing `alt+u` on the same newest entry** restore the note twice. No duplicate task results. Accept, as P-S-6.
- **I-4 Pre-existing, BACKLOG.** `Board.save` is a plain `write_text`, which truncates the file before encoding (SEC-2 shows it). Moving the open board to `save_atomic` is out of scope (S-a).

## Checked and sound

- **Store size:** the read is capped at `STORE_MAX_BYTES + 1`. An oversized store is not copied aside (`keep_aside` reads the whole file) and is never written over. An oversized write raises the worded `OSError` and leaves memory unchanged. `RecursionError` and `ValueError` (including the int-digit limit) are caught in one `try`. `keep_aside` precedes no write.
- **Entry shape:** `task` must match `ID_RE`, every `images` item must pass `_image_ok`, `type(v) is bool` is required, `text` must not be blank, and unknown keys are dropped. No store value can name a path outside F or a board's `images/<id>/`, so the traversal through the store (P-S-4) is closed.
- **Board scope:** undo runs only for an entry whose `board` is a lane (LLR-4405.16). A dump target is always a lane: `Doc.board_path` comes from `board_lanes`, and the name field cycles over readable lanes only. No dump reaches an unregistered path.
- **Cross-board write:**
  - The existence check comes before the lock, so no `.lock` or seeded file is made beside a missing board.
  - Reads go through `peek_board`, never the seeding `Board.load`.
  - The stamp is checked at s0/s1 and again before the save. The save uses `save_atomic`. The birth record is written after the save.
  - Neither `Board.save` nor `add_task` is used on that path.
  - The open board gets the `file_unreadable` check (P-S-9) and an in-memory rollback on `OSError` (but see SEC-2 for non-OS errors).
- **Images:**
  - The name rule blocks `/`, `\`, `:` (so alternate data streams), `.`/`..`, control characters and lengths over 128.
  - The suffix allowlist is `IMAGE_EXTS`, which excludes `.svg`; task images are opened with the OS handler (models.py:495).
  - On a move, the source must be a regular file (`lstat` + `S_ISREG`), a name is "taken" if anything exists at it including a dangling link (`lexists`), and the destination folder is created exclusively.
  - `_new_task_id` skips an existing folder. Files are copied before the save and the source is removed only after it.
  - Attach copies and never moves the user's file. A name that fails the rule becomes `image<suffix>`.
- **Markup:**
  - Every painter returns `Text` built with `append`. `key_line` returns `Text`. Every `notify` passes `markup=False`, and there is no `from_markup`.
  - The existing `tests/test_markup_census.py` covers the new sites.
  - TC-4634 / AT-4407 pin `[red]x[/red]`, `[@click=app.quit]q` and `[b]P[/b]` as literal text.
- **Control characters:**
  - Titles and notes go through `strip_controls`. Store strings go through `clean_strings`. The pad written goes through `strip_controls`, and G-V adopts the written text (P-S-8).
  - The reason words are `[a-z0-9@]` only.
- **Byte stability:** opening, typing and closing leave both board files, both histories, `people.json` and `marks.json` unchanged (LLR-4407.27). Other tasks survive a dump byte for byte (LLR-4407.28, "saved by this version"). `inbox.py` never writes `people.json` or `marks.json`. `Inbox.load` writes nothing except `.corrupt` for an unreadable store.
- **Lock and atomic write:** the `people.json` pattern is kept: `_commit` reads fresh under `file_lock`, writes through `write_atomic`, and never writes over an unreadable store that was not set aside. Hidden duplicate-task risks are covered: `mark_notice` does not adopt a foreign stamp (P-S-5), `_unsaved_flags` survive refresh (P-S-7), and `last_dump` reads fresh (P-S-6).
- **No new dependency, no network, no secret.** The `alt+enter` removal (R1-1) leaves no key that the terminal cannot deliver. `check_action` refuses `capture` under a modal.

## Evidence states

| Id | Finding | Mitigation |
|---|---|---|
| SEC-1 | `executed` (p4) | `planned` |
| SEC-2 | `executed` (p1) | `planned` |
| SEC-3 | `read` (+ p5 `executed`) | `planned` |
| SEC-4 | `read` | `planned` |
| SEC-5 | `read` | `planned` |
| SEC-6 | `read` (+ p5) | `planned` |
| SEC-7 | `executed` (p3) | `planned` |
| SEC-8 | `read` | `planned` |
| SEC-9 | `read` | `planned` |
| SEC-10 | `executed` (p2) | `planned` |
| SEC-11 | `read` | `planned` |

## Evidence checklist

- [x] Each finding has: what · where · why · recommendation (SEC-1..SEC-11 above).
- [x] Each finding has a severity rating (header line of each).
- [x] No secret values appear in this output (none exist; probes used synthetic text only).
- [x] The verdict is explicit: **FAIL**. There is no HIGH. The three open MAJORs (SEC-1, SEC-2, SEC-3) are `planned`, so this is block-until SEC-1, SEC-2, SEC-3 at the re-gate. That authorises nothing.
- [x] New integration: none. No MCP server, connector or network call. The new local surfaces are scoped: the store, `inbox-images/` and lane boards (above).
