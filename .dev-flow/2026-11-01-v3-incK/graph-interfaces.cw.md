# Inc K — shared interfaces (owned by the orchestrator; agents PROPOSE changes in their group file, never edit here)

> The seams between the three prototype groups. **G-S** owns `taskboard/inbox.py`: note parsing, the
> `Inbox` store, image files, and every write to a board file (the open board through the live `Board`
> object G-V hands it, another board by `move_project`'s pattern). **G-T** owns `taskboard/suggest.py`:
> pure functions over the lanes `board_lanes` returns. **G-V** owns `taskboard/app.py` + `taskboard/keymap.py`
> + `README.md`: the screens, the keys, every notice text except the refusals G-S words (P-V-13: the
> `notice` of DumpOutcome and AttachResult is G-S's full text, which G-V shows verbatim with `markup=False`),
> the debounce, the hit cache, the choice of the target (`live` is `app.board` exactly when the target path
> is the open board's), `refresh_view`.
> E2 correction pass (round 0b, `03-pdr-rulings.md`): P-S-1, P-S-2, P-S-3, P-S-4, P-S-6, P-S-8, P-S-15, P-V-1,
> P-V-13, P-T-1, P-T-3, P-T-4 and P-T-5 applied to the nodes below.
> E3 round 1 (`03-pdr-rulings.md` §Round 1, LED-2026-11-01-incK.4, `03-e3-corrections.md`): ARCH-1 (dump and undo applied
> to the fresh state; only the typing write unions) with SEC-1 (multiset of unseen entries), ARCH-2 (option identity, batch
> targets fixed), ARCH-3 (`capture` refused under the home), ARCH-4 (flagged notes removed: `Inbox.flag`, `Inbox.flag_for`,
> FlaggedEntry and the `flagged` key are gone; pending records in the Inbox), ARCH-6 (`Corpus`), ARCH-7 (no `_new_task_id`),
> ARCH-8 (inbox.py imports no `modals`), SEC-2..SEC-8 applied below. Executed references: `%TEMP%\incK-e3fix\`.
> Placement rule: no group reads another group's private state. G-S never imports `app`; G-T never imports
> `app` or `inbox`; G-V reads only the public names below. A refusal is a value (`notice`), never an
> exception, except `Inbox.write_pad` / `Inbox.mark_notice`, which raise `OSError` like `Directory._commit`.
> Times are local naive `datetime`. Fixture clock: now 2026-11-01T10:02:00. Fixture boards (synthetic):
> `Client A` (projects `Eval harness`, `Pilot rollout`) at lane 0, the open board; `Course` (project
> `Module 4 · Volumes`) at lane 1. Store folder `S` = the registry's folder.
> E2c: the suggestion and view examples share ONE fixture, G-T's executed fixture F (graph-proto-T §Fixture F:
> files `S/boards/client-a/board.json`, `S/boards/course/board.json`; project ids `pe`, `pr`, `pv`; project
> colours blue, indigo, violet; board colours sky, violet; its tasks and marks), plus the phases Client A
> ["Backlog", "Doing", "Done"] and Course ["Todo", "Doing", "Done"]; G-T's executed scores win. G-S's
> layer-0 examples use their own fixture S (graph-proto-S head), with the same boards, phases and project names.

## Nodes

is_divider
req: LLR-4402.1
in: str line
out: bool divider
func: `line.rstrip()` is 4 or more `_` and nothing else; leading whitespace is not allowed (R0-3).
module: taskboard/inbox.py
examples: (TC-4431) line "____  " → divider `True`
examples: (TC-4431) line " ____" → divider `False`

note_parts
req: LLR-4402.2, LLR-4402.3, LLR-4402.4, LLR-4402.5
in: str text
out: list[Part] parts
func: splits `text.split("\n")` at divider lines into Parts in order (a divider line belongs to no part); each Part keeps its first and last line index and its text with leading and trailing blank lines removed; `is_note` is True when that text holds a non-whitespace character. Never raises; linear in len(text).
module: taskboard/inbox.py
examples: (TC-4433) text "a\n\nb\n____\nc" → parts Part(0, 2, "a\n\nb", True), Part(4, 4, "c", True)
examples: (TC-4434) text "____\n  \n____\na" → parts with is_note `False` for the middle part and one note "a"

note_count
req: LLR-4402.8
in: str text
out: int count
func: the notes of note_parts, plus 1 when the last part holds at least one line, holds only whitespace and follows a divider line (the note being started, R2 F-4).
module: taskboard/inbox.py
examples: (TC-4438) text "a\n____" → count `1`
examples: (TC-4438) text "a\n____\n" → count `2`

note_at
req: LLR-4404.30, LLR-4404.28
in: str text; int row
out: Part? part
func: the note Part holding `row`; on a divider line the note Part above it; None when the row's part is not a note or nothing is above.
module: taskboard/inbox.py
examples: (TC-4530) text "a\n____\nb", row `1` → part text "a"
examples: (TC-4528) text "", row `0` → part `None`

image_name
req: LLR-4408.18
in: str line
out: str? name
func: for a line that, stripped, is `img: <name>` with a name that passes the image-name rule (requirements §1, P-S-10, SEC-7: 1..128 characters, no surrounding whitespace, no `/`, `\`, `:` or control character, not `.` or `..`, a lower-case suffix in `models.IMAGE_EXTS`, no Windows reserved name in the stem before the first `.` with trailing spaces removed: con, prn, aux, nul, conin$, conout$, com0..com9, lpt0..lpt9, com¹..com³, lpt¹..lpt³) → the name; otherwise None.
module: taskboard/inbox.py
examples: (TC-4628) line "img: a.png" → name "a.png"
examples: (TC-4628) line "img: ../a.png" → name `None`
examples: (TC-4628) line "img: con .png" → name `None`; line "img: console.png" → name "console.png" (executed, sec_fix.py)

note_task
req: LLR-4404.2, LLR-4404.3, LLR-4404.29, LLR-4409.3
in: str text
out: NoteTask task
func: title = `strip_controls(visible(line)).strip()` of the title line (`visible` = `"".join(seg for seg, _ in views.highlight_segments(line))`: inbox.py imports no `modals` and no Textual module, ARCH-8) (the first line that is not an image line and whose visible text is not blank), "" when there is none; notes = the other non-image lines verbatim (markers and mentions kept), outer blank lines removed, control characters removed; images = the image names in line order, each once.
module: taskboard/inbox.py
examples: (TC-4502) text "::b:: Golden set ::\nmore" → title "Golden set", notes "more"
examples: (TC-4529) text "img: a.png" → title "", images "a.png"

without_note
req: LLR-4404.6
in: str text; Part part
out: tuple(str text, int row)
func: the pad text without the part's lines and one adjacent divider line (the one after it, else the one before); every other line byte-identical; row = the line index where the part began, clamped into the new text.
module: taskboard/inbox.py
examples: (TC-4506) text "a\n____\nb\n____\nc", part of "b" → text "a\n____\nc"

with_note
req: LLR-4405.3
in: str text; str note
out: str text
func: `note` appended at the end; when `text` holds a non-whitespace character, after a new line `____` (no blank line added).
module: taskboard/inbox.py
examples: (TC-4543) text "a", note "b" → text "a\n____\nb"
examples: (TC-4543) text "", note "b" → text "b"

union_pads
req: LLR-4407.19
in: str fresh_pad; list[str] unseen; str mine
out: str pad
func: the notes of fresh_pad in their order, then each note of `mine`, in mine's order, less one copy per fresh-pad note and per `unseen` text of equal text (a multiset: budget = Counter(fresh notes) + Counter(unseen); a note of mine with budget > 0 spends one, else it is written); joined by "\n____\n". `unseen` = the `text` of each fresh `dumped` entry whose (task, board) the Inbox did NOT hold at its last read or write (SEC-1), never the whole 7-day list. Called by Inbox.write_pad only when the file changed (R2 F-8), on the fresh pad AFTER the write's record/drop/pending ops were applied to it (ARCH-1).
module: taskboard/inbox.py
examples: (TC-4599) fresh_pad "a\n____\nc", unseen ["b"], mine "a\n____\nb\n____\nd" → pad "a\n____\nc\n____\nd"
examples: (TC-4599) fresh_pad "x", unseen `[]` (the 3-day-old "follow up" entry is held by this Inbox), mine "x\n____\nfollow up" → pad "x\n____\nfollow up"; with unseen ["follow up"] and mine "x\n____\nfollow up\n____\nfollow up" → pad "x\n____\nfollow up" (one copy kept) (executed, store_fix.py; the NC "exclude every fresh dumped text" gives "x")

prune_dumped
req: LLR-4405.12
in: list[DumpedEntry] entries; datetime now
out: list[DumpedEntry] kept
func: the entries whose `at` parses (`datetime.fromisoformat`, naive) to a moment no more than 604 800 s before now, in their order.
module: taskboard/inbox.py
examples: (TC-4552) entries at "2026-10-25T10:03:00" and "2026-10-25T10:01:00" and "garbage", now 2026-11-01T10:02:00 → kept the first only

Inbox.load
req: LLR-4407.1, LLR-4407.6, LLR-4407.7, LLR-4407.8, LLR-4407.10, LLR-4407.11, LLR-4407.12, LLR-4407.35, LLR-4407.36, LLR-4407.43, LLR-4407.45
in: Path path
out: Inbox inbox
func: `people.Directory.load`'s shape: never raises; missing or blank → empty (pad "", no entries, nothing written); unparseable (not JSON, not an object, `pad` not a str, `dumped` not a list, or any string that will not encode as UTF-8 — a lone surrogate from a JSON escape, SEC-2) → `keep_aside` + empty; a read that raises OSError keeps the store stamp None (SEC-4: the next write then unions with whatever the file holds) + `load_report {"unreadable": True, "backup": <str or None>}`; larger than `STORE_MAX_BYTES` (8 388 608) → read up to the cap + 1 byte only, unreadable, NOT copied aside (backup None) and never written over (P-S-3); strings through `clean_strings`; bad entries skipped, an entry's shape checked (`task` fullmatches `[A-Za-z0-9_-]{1,64}`, every `images` item passes the image-name rule, `text` non-blank, `new_project` a bool: P-S-4); `divider_notice` only the boolean true; the store stamp (mtime_ns, size) kept. G-V words the notice from `load_report` (backup None → the LLR-4407.38 text, P-V-6).
module: taskboard/inbox.py
modify: [Data: Inbox state] (replace)
examples: (TC-4587) a store holding `{"pad": 5}` → pad "", load_report "unreadable" `True`, `inbox.json.corrupt` written
examples: (TC-4586) no file → pad "", no file created
examples: (TC-4676) a store of 8 388 609 bytes → load_report "unreadable" `True`, backup `None`, no `inbox.json.corrupt`
examples: (TC-4683) a store `{"pad": "a\ud800b"}` (the JSON escape) → load_report "unreadable" `True`, `inbox.json.corrupt` byte-equal, pad "" (executed, sec_fix.py: the encode probe raises UnicodeEncodeError)

Inbox.refresh
req: LLR-4407.13, LLR-4407.14, LLR-4407.45
in: Inbox self
out: bool? changed
func: the batch 2026-10-24-batch-02 re-read: stamp unchanged → None (no parse); changed and parsed → state replaced, True; unparseable → False, state kept, the new stamp kept so the same bad file is reported once; a read that raises OSError → False, state AND the old stamp kept (SEC-4: the next write unions). The Inbox's pending records survive every refresh (they are not store state, ARCH-4).
module: taskboard/inbox.py
modify: [Data: Inbox state] (replace)
examples: (TC-4593) a second Inbox wrote pad "x" → changed `True`, pad "x"
examples: (TC-4594) the file made "{not json" → changed `False`, pad as loaded
examples: (TC-4685) a second Inbox wrote pad "z", `_read` raising OSError once → changed `False`, the stamp as before; the next write_pad("p") → union `True`, pad "z\n____\np"

Inbox.write_pad
req: LLR-4407.2, LLR-4407.3, LLR-4407.4, LLR-4407.5, LLR-4407.9, LLR-4407.18, LLR-4407.19, LLR-4407.20, LLR-4407.37, LLR-4407.39, LLR-4407.41, LLR-4407.44, LLR-4407.48, LLR-4407.49, LLR-4405.4, LLR-4405.12
in: Inbox self; str pad; DumpedEntry? record = None; DumpedEntry? drop = None
out: WriteResult result
func: `Directory._commit`'s shape under `file_lock(path)`: re-read NOW (unparseable and not set aside → OSError, nothing written). The change is applied to the FRESH state (ARCH-1, `people.Directory._commit`'s shape): ops = the Inbox's pending records and drops in the order made, then this call's `record`, then its `drop`; a record → skipped when the fresh `dumped` already holds its (task, board), else the first fresh-pad note equal to `record.text` is removed and the entry appended (LLR-4407.48); a drop (`drop.text` = the restored note: G-V passes `dict(entry, text=out.note_text)`) → its entry removed by (task, board) and, only when the fresh `dumped` held it, `with_note(fresh pad, drop.text)` (LLR-4407.49). Pad written = `pad` verbatim when the file's stamp equals the store stamp, else union_pads(the op'd fresh pad, unseen texts, pad) — the only union, the window's typing (SEC-1). dumped = prune_dumped(op'd dumped, now); `write_atomic(json.dumps({version, pad, dumped[, divider_notice]}, indent=2, ensure_ascii=False))`; then state held, pending cleared, stamp taken. Skips the write (returns written False) when pad, record and drop change nothing and nothing is pending. A text over `STORE_MAX_BYTES` raises OSError "inbox.json would hold <n> bytes, over the 8388608-byte limit, so it was not written" (P-S-3); a text that will not encode raises OSError "inbox.json holds a character that cannot be saved (<reason>), so it was not written" (SEC-2). A failed write raises OSError and changes no store state in memory; a `record` or `drop` it carried is appended to the Inbox's pending list first, so the next pad write retries it (ARCH-4).
module: taskboard/inbox.py
modify: [Data: inbox.json] (replace); [Data: Inbox state] (replace)
examples: (TC-4600) pad "a\n________\n\nb  " on an unchanged file → result pad "a\n________\n\nb  ", union `False`
examples: (TC-4599) the file changed by a second Inbox → result union `True`, pad "a\n____\nc\n____\nd"
examples: (TC-4598) pad equal to the stored pad, no record, nothing pending → result written `False`
examples: (TC-4677) pad "a" × 8 400 000 on a store with no entries → OSError "inbox.json would hold 8400047 bytes, over the 8388608-byte limit, so it was not written", file and memory unchanged
examples: (TC-4688) memory pad "a\n____\nb", a second Inbox wrote pad "a\n____\nb\n____\nc"; pad "a", record e(b) → result pad "a\n____\nc", the file's dumped holds e(b) (executed, store_fix.py; the old typing union gave "a\n____\nb\n____\nc")
examples: (TC-4689) a second Inbox wrote pad "a\n____\nc\n____\nd" with dumped [e(b)]; pad "a\n____\nc\n____\nb", drop e(b) → result pad "a\n____\nc\n____\nd\n____\nb", the file's dumped `[]` (executed; the old union gave "a\n____\nc\n____\nd": b lost)
examples: (TC-4681) write_atomic failing once on record e(b) over pad "a\n____\nb" → OSError, pending holds e(b), the file unchanged; then pad "a\n____\nx" on the unchanged file → result pad "a\n____\nx", the file's dumped [e(b)], pending `[]` (executed)

Inbox.pad_now
req: LLR-4407.42
in: Inbox self
out: str pad
func: the store pad as held (`self.pad`) with the pending ops applied as write_pad applies them (each pending record's first equal note removed; each pending drop's note appended when its entry is held); `self.pad` itself unchanged. G-V fills the pad from it at open (ARCH-4: a dump whose store write failed does not come back into the pad).
module: taskboard/inbox.py
examples: (TC-4682) pad "a\n____\nb", pending [record e(b)] → pad "a"

Inbox.last_dump
req: LLR-4405.1, LLR-4405.7, LLR-4405.17, LLR-4405.18
in: Inbox self; datetime now
out: DumpedEntry? entry
func: the newest (last by position) entry of prune_dumped(entries, now), else None, where entries = the store FILE's `dumped` read fresh at the call (`_read`, no lock; no state and no stamp change), or the in-memory `dumped` when the file is missing or cannot be parsed (P-S-6), followed by the Inbox's pending records not in it (ARCH-4: a dump whose store write failed is still the newest undo).
module: taskboard/inbox.py
examples: (TC-4547) one entry 8 days old → entry `None`
examples: (TC-4557) memory [e1, e2], a second Inbox dropped e2 from the file → entry e1
examples: (TC-4558) the file's dumped [e1], pending [record e2] → entry e2

Inbox.mark_notice
req: LLR-4402.14
in: Inbox self
out: None
func: a `_commit` that sets `divider_notice` true (the pad as the file holds it); raises OSError like write_pad; not a pad write: it applies no pending op (they wait for the next write_pad).
module: taskboard/inbox.py
modify: [Data: inbox.json] (replace)
examples: (TC-4444) → the file holds "divider_notice": `True`

attach_images
req: LLR-4408.1, LLR-4408.2, LLR-4408.3, LLR-4408.5, LLR-4408.6, LLR-4408.7
in: Path folder; object grabbed
out: AttachResult result
func: `grabbed` is `models.grab_clipboard_image()`'s value, read by G-V. A PIL image → `save_pil_image(folder, img)` (paste-NNN.png); a list of paths → each regular file with an IMAGE_EXTS suffix COPIED into `folder` (`shutil.copy2`), its name or `<stem>-<k><suffix>` when taken; None → notice "No image found in the clipboard."; a list with no image → "Clipboard holds no image files."; an OSError → "The image could not be saved: <error>" with the names saved before it kept. Never moves or changes the source.
module: taskboard/inbox.py
modify: [I/O: inbox-images] (append)
examples: (TC-4613) grabbed a list holding "C:/u/shot.png" with "shot.png" already in folder → names "shot-2.png", the source still present

entry_for
req: LLR-4407.3
in: DumpOutcome outcome; str note; Path board_path; datetime now
out: DumpedEntry entry
func: public builder of the store record of an ok dump (P-S-15): {"at": stamp(now), "text": note (the Part text, verbatim), "task": outcome.task.id, "title": outcome.task.title, "board": str(board_path), "project": outcome.project_id, "new_project": outcome.new_project, "images": list(outcome.images)} in the LLR-4407.3 key order. G-V passes it to `Inbox.write_pad(record=…)`; when that write raises, write_pad keeps it as a pending record (ARCH-4). G-V never builds an entry itself.
module: taskboard/inbox.py
examples: (TC-4583) the AT-4402 dump into Course, now 2026-11-01T10:02:00 → keys ["at", "text", "task", "title", "board", "project", "new_project", "images"], at "2026-11-01T10:02:00", images ["board-0938.png"], new_project `False`

dump_note
req: HLR-4404, LLR-4404.1, LLR-4404.4, LLR-4404.5, LLR-4404.8, LLR-4404.9, LLR-4404.10, LLR-4404.11, LLR-4404.12, LLR-4404.13, LLR-4404.14, LLR-4404.15, LLR-4404.23, LLR-4404.24, LLR-4404.25, LLR-4404.26, LLR-4404.29, LLR-4404.31, LLR-4404.32, LLR-4404.33, LLR-4404.34, LLR-4408.10, LLR-4408.11, LLR-4408.12, LLR-4408.13, LLR-4408.15, LLR-4408.20
in: DumpTarget target; str? project_id; str? new_name; str note; Path folder; str project_name = ""
out: DumpOutcome outcome
func: `project_name` (P-S-1) is the chosen hit's `doc.project_name` ("" for a new project), used only for the LLR-4404.12 refusal "<project_name> is no longer on <board> — nothing dumped.". First `note.encode("utf-8")` (UnicodeEncodeError → refusal "This note holds a character that cannot be saved — nothing dumped.", before any board write, SEC-2). note_task(note) (title "" → refusal). Task ids come from `models._new_id()` (ARCH-7: no retry loop; a taken `images/<id>/` makes the exclusive folder creation refuse the dump). The pad copies are removed after the save only when neither the pad images folder nor the task folder is a link or junction (SEC-6, LLR-4408.20). Exactly one of project_id / new_name. Open board (`target.live` set): checks on the live object, images copied, `live.add_task(task)` (stamps created, writes the birth record, saves); an OSError → task and new project removed from `live`, copies removed, refusal. Other board: `file_lock(target.path, target.name)` held; missing → refusal; `peek_board` fresh, unreadable → refusal; project gone / name blank / name taken → refusal; stamp (mtime, size) taken; task built with `created = models.stamp(now)`, phase = phases[0], new project (colour rule) appended in memory; images copied to `image_dir(task.id)` (created exclusively); stamp re-checked → refusal on change; `save_atomic`; then `history.append(path, birth, at=now)`; then pad copies removed. Never writes the store and never touches the pad.
module: taskboard/inbox.py
modify: [Data: board file] (replace); [Data: history.jsonl] (append); [I/O: inbox-images] (clear); [I/O: task images] (append)
examples: (TC-4509) target `Course` (live `None`), project "Module 4 · Volumes", note "Volume lab fails on WSL\nthe oracle script expects /mnt/c" → outcome ok `True`, title "Volume lab fails on WSL", the board file holds the task
examples: (TC-4510) target path missing → outcome ok `False`, notice "Course's file is missing — nothing dumped."
examples: (TC-4533) the file rewritten between the read and the save → outcome ok `False`, notice "Course changed while dumping — nothing dumped."
examples: (TC-4534) note "T\ud800x" into the open board → outcome ok `False`, notice "This note holds a character that cannot be saved — nothing dumped.", the board file's bytes unchanged (executed, sec_fix.py: the note does not encode)

undo_dump
req: HLR-4405, LLR-4405.2, LLR-4405.5, LLR-4405.6, LLR-4405.8, LLR-4405.10, LLR-4405.11, LLR-4405.19, LLR-4408.16, LLR-4408.17, LLR-4408.20
in: DumpedEntry entry; Board? live; Path folder
out: UndoOutcome outcome
func: G-V calls it only when `os.path.normcase(os.path.abspath(entry.board))` equals that string of a lane `board_lanes` returns (a string test: the store's value reaches no file system call, SEC-8); otherwise G-V shows "<board path> is not a known board — nothing undone." and keeps the entry (P-S-4, LLR-4405.16). "changed" (SEC-3) = `dataclasses.asdict(task) != dataclasses.asdict(expected)`, expected = `Task(title, project_id=entry.project, phase=board.phases[0], notes=notes, images=[str((board.image_dir(entry.task) / n).resolve()) for n in entry.images], id=entry.task, created=task.created)` (title, notes from `_task_fields`, every other field at its default); a task of the board other than it holding `entry.task` in `depends_on` → state "needed" (nothing changes, LLR-4405.19). The moved image files go back by copy, and their board copies are unlinked only when neither folder is a link or junction (SEC-6). `live` is the open board when `entry.board` is its file (G-V decides), else None and the board is read fresh under `file_lock` with the stamp check and `save_atomic`. Task id absent → state "gone" (no board change). The task differs from `expected` — its title and notes from `_task_fields(entry.text, moved=set(entry.images))`, a missing image's line kept as text (P-S-2) — → state "changed" (nothing changes). Else the task removed (and the project when `new_project` and no other task holds it), saved, its image files moved back to `folder` (renamed `<stem>-<k>` when taken), the emptied `image_dir` removed → state "undone". A read, lock or save failure → state "failed" with the error text. note_text = entry.text with each moved image line naming the file as it now is.
module: taskboard/inbox.py
modify: [Data: board file] (replace); [I/O: inbox-images] (append); [I/O: task images] (clear)
examples: (TC-4548) the task deleted after the dump → outcome state "gone", note_text holds "Volume lab fails on WSL"
examples: (TC-4550) the task title edited → outcome state "changed"
examples: (TC-4550) the task's phase moved to "Doing" (title and notes untouched) → outcome state "changed"; the task as dumped, reloaded by `peek_board` → state "undone" (executed, sec_fix.py over a real save_atomic round trip; the title/notes-only check sees no change for the phase)
examples: (TC-4559) task "tc1" given depends_on ["t0000001"] → outcome state "needed", the board bytes unchanged (executed)
examples: (TC-4626) "paste-001.png" taken in folder → note_text holds "img: paste-001-2.png"

words
req: LLR-4403.1, LLR-4403.2
in: str text
out: list[tuple[str, str]] pairs
func: (stem, surface) for each word that counts: accents folded, lower case, `@handle` or `[a-z0-9]+`, length ≥ 3, not a bare number, not in STOP; stem: `ies`→`y` (len > 4), final `s` not `ss` dropped (len > 3), cut to 6; a handle unstemmed.
module: taskboard/suggest.py
examples: (TC-4461) text "Golden SET: 12 Questions @username_subject de la Café" → pairs ("questi", "questions") and ("@username_subject", "@username_subject"), no "12"

corpus
req: LLR-4403.3, LLR-4403.4, LLR-4403.5, LLR-4403.23, LLR-4403.24, LLR-4403.27, LLR-4403.29
in: list[tuple[str, str, Board?, str]] lanes; dict marks
out: Corpus corpus
func: returns `Corpus(docs, idf)`: `idf = _idf(docs)` once, and each Doc carries its tf·idf vector `vec` and its norm `norm`, computed once per build (ARCH-6); one Doc per non-archived project of each lane whose board is not None, lane order then project position; tf weights name ×3, titles of its non-archived tasks ×2, `@handle` in their notes ×2, the `marks[t.mark].name` of each milestone with a known mark ×1, other note words ×1; tasks with no project are skipped. Each document's text is cut at `DOC_CHARS` (100 000) characters before tokenising: the fields are consumed in the order name, then per task title, notes, mark name, each sliced to the characters left (P-T-5). `lanes` is `board_lanes(app)[0]`, `marks` is `app.marks.marks`. Pure; reads no file.
module: taskboard/suggest.py
examples: (TC-4464) project "Eval harness", task "Answer key", notes "ask @username_subject key", milestone mark "payment" named "Payment" → tf "eval" `3`, "key" `3`, "@username_subject" `2`, "paymen" `1`
examples: (TC-4463) 3 live projects and 1 archived over 2 lanes → docs `3`
examples: (TC-4489) fixture F → `1` call of `_idf` for the build; corpus.idf "questi" 1.6931471805599454

suggest
req: LLR-4403.6, LLR-4403.7, LLR-4403.8, LLR-4403.9, LLR-4403.10, LLR-4403.14, LLR-4403.22, LLR-4403.26, LLR-4403.28, LLR-4403.29
in: str note; Corpus corpus
out: list[Hit] hits
func: `note` is the note's scored text: G-V passes `nt.title + "\n" + nt.notes` of `inbox.note_task(part.text)` (image lines left out, P-T-4); suggest.py imports no inbox. The first `NOTE_CHARS` (10 000, a suggest.py constant, P-T-1) characters of note; idf = ln((N+1)/(df+1)) + 1 read from `corpus.idf` and each document's vector and norm from its Doc (never recomputed per call, ARCH-6), a note stem no document holds weighs 0; score = cosine of tf·idf, halved on exactly one shared stem, rounded to 4 decimals; hits with score ≥ LOW (0.08), ordered by (−score, lane, project name casefolded, project name, position) (P-T-3), at most 3; why = the note's surface words of the shared stems, largest contribution first, ties by stem. Deterministic; [] for no docs.
module: taskboard/suggest.py
examples: (TC-4474) note "Golden set: 12 questions still have no answer key ask @username_subject" → hit "Eval harness" first, why "questions", "@username_subject", "key"
examples: (TC-4485) a corpus with docs `[]` → hits `[]`
examples: (TC-4489) the 7 probe notes over fixture F's corpus → the same hits as idf computed per call, digest "d694943ce6d21f09" (executed, suggest_fix.py)

options
req: LLR-4403.11, LLR-4403.12, LLR-4403.13
in: list[Hit] hits
out: list[Hit?] opts
func: hits[0] scores ≥ MID (0.16) → hits (≤ 3); else [NEW_PROJECT] + hits[:2]. NEW_PROJECT is None. At most 3 entries; the first is the top choice.
module: taskboard/suggest.py
examples: (TC-4473) hit scores 0.40, 0.20, 0.10 → opts the three hits
examples: (TC-4473) hit scores 0.12, 0.09 → opts `None` then the two hits

bars
req: LLR-4403.16
in: float score
out: str cue
func: "▰▰▰" at or above HIGH 0.30, "▰▰▱" at or above MID 0.16, "▰▱▱" at or above LOW 0.08, "▱▱▱" below.
module: taskboard/suggest.py
examples: (TC-4476) score 0.2 → cue "▰▰▱"

PadArea
req: LLR-4402.6, LLR-4402.7, LLR-4402.12, LLR-4402.18, LLR-4409.1
in: str text
out: TextArea area
func: an `InkArea` subclass (Inc C's live colour unchanged); its line render draws a divider line (is_divider) as `─` across the content width while the cursor row is another row (R1-5: line render, not the highlight map); placeholder = the four ghost lines. Owned by G-V.
module: taskboard/app.py
examples: (TC-4436) text "a\n____\nb", cursor on row 2 → row 1 renders `─` only

CaptureView
req: HLR-4401, LLR-4401.4, LLR-4401.5, LLR-4401.6, LLR-4401.7, LLR-4401.8, LLR-4401.9, LLR-4401.10, LLR-4403.15, LLR-4403.21, LLR-4403.30, LLR-4403.31, LLR-4407.15, LLR-4407.16, LLR-4407.17, LLR-4407.29, LLR-4407.42
in:
out: Screen screen
func: app.py Screen[None]: on open `app.inbox.refresh()`, lanes/ids = board_lanes(app), docs = corpus(lanes, app.marks.marks) (a Corpus), a hit cache `dict[str, list[Hit]]` keyed by the Part text, filled by `suggest(nt.title + "\n" + nt.notes, docs)` (P-T-4), cleared with every new docs; the rail computes hits only once the pad has been still for 1.0 s (the debounce), and while a note's hits are not computed it draws the option lines last drawn at that note's position (ARCH-6); an action (`alt+d`, `alt+o`, `alt+a`) computes the hits it needs at once; pad = PadArea(inbox.pad_now()) (ARCH-4). The chosen option per note text is stored as the option's identity `(str(doc.board_path), doc.project_id)` or the new-project sentinel, never as an index (ARCH-2). Dump: target = DumpTarget(path, name, live=app.board when the path is the open board's file, else None) → dump_note(…, project_name=hit.doc.project_name) → on ok: without_note, entry = entry_for(out, part.text, path, now), inbox.write_pad(pad, record=entry) (OSError → the Inbox keeps a pending record; the pad still loses the note; the LLR-4407.40 notice), refresh_view, docs rebuilt (once per batch). After any write G-V replaces its pad text whenever `result.written and result.pad != text`, and shows the merge notice only when `result.union` (P-S-8). Undo: inbox.last_dump(now) → (entry.board a lane's path by normalised string, else the P-S-4 refusal) → undo_dump → with_note + write_pad(drop=dict(entry, text=out.note_text)). Every notice is shown with `markup=False`; G-S's refusal texts verbatim (P-V-13).
module: taskboard/app.py
examples: (TC-4402) app with 2 registry boards, press n → app.screen is a CaptureView

ReviewList
req: HLR-4406, LLR-4406.1, LLR-4406.8, LLR-4406.9, LLR-4406.16, LLR-4406.17
in: list[str] notes
out: ModalScreen screen
func: one row per note; the chosen option per note text is the CaptureView's dict (shared, by identity); `d` first fixes every checked row's target option (ARCH-2), then calls the CaptureView's one dump path per checked row in pad order with those targets and no docs rebuild, counts the oks, and rebuilds the docs once after the batch (LLR-4403.24).
module: taskboard/app.py
examples: (TC-4568) 3 of 4 checked → 3 dump_note calls
examples: (TC-4577) rows "Rubric review" and "Rubric scoring" (`o` → Eval harness), "Pilot judge rubric" (top Eval harness 0.2889), "Rubric for the pilot" (top Pilot rollout 0.2232), all checked, `d` → 3 tasks in Eval harness and "Rubric for the pilot" in Pilot rollout (executed, suggest_fix.py: re-resolved per row it would land in Eval harness, 0.6028)

TaskboardApp.action_capture
req: LLR-4401.2, LLR-4401.14, LLR-4401.19
in: TaskboardApp self
out: None
func: `self._bring(CaptureView, CaptureView)`, as action_added_list; `capture` is added to check_action's always-allowed tuple and CaptureView to its holding tuple (R1-6); `capture` is refused while a BoardsHome is on the stack (ARCH-3: the open board has not started yet).
module: taskboard/app.py
examples: (TC-4414) N, n → exactly one CaptureView in app.screen_stack and it is app.screen
examples: (TC-4419) 2 registry boards, the home on top at start: `N`, `n` → no CaptureView on the stack

## Entities

[Data: Part]
in: NamedTuple(int start, int end, str text, bool is_note)
desc: inbox.py; start/end are the part's first and last line indices in the pad (divider lines excluded); text has outer blank lines removed.

[Data: NoteTask]
in: NamedTuple(str title, str notes, list[str] images)
desc: inbox.py; title "" means "no title line" (LLR-4404.29).

[Data: DumpTarget]
in: NamedTuple(Path path, str name, Board? live)
desc: inbox.py; built by G-V. `live` is `app.board` exactly when `path` is the open board's file (samefile), else None. `name` is the board's display name for notices and the lock label.

[Data: DumpOutcome]
in: NamedTuple(bool ok, Task? task, str project_id, str project_name, bool new_project, list[str] images, list[str] missing, str? notice)
desc: inbox.py; ok False → `notice` holds G-S's full refusal text (G-V shows it verbatim, P-V-13) and nothing was written; ok True → `images` lists the FILE NAMES moved, in line order (what `entry_for` records; the resolved paths are `task.images`, P-V-13), `missing` lists image names not found (their lines stay in the notes; G-V words "<k> image(s) not found: <names>").

[Data: UndoOutcome]
in: NamedTuple(str state, str note_text, str? notice)
desc: inbox.py; state ∈ {"undone", "gone", "changed", "needed", "failed"} ("needed": another task depends on it, SEC-3); G-V restores note_text to the pad for "undone" and "gone" and words the notices; `notice` carries the error text for "failed".

[Data: WriteResult]
in: NamedTuple(bool written, str pad, bool union)
desc: inbox.py; `pad` is what the file now holds; G-V replaces its pad text whenever `written and pad != the text it passed` (a union, or stripped control characters), and shows the merge notice only when `union` is True (P-S-8).

[Data: AttachResult]
in: NamedTuple(list[str] names, str? notice)
desc: inbox.py; G-V inserts one `img: <name>` line per name after the cursor's note, then write_pad.

[Data: DumpedEntry]
in: dict(str at, str text, str task, str title, str board, str project, bool new_project, list[str] images)
desc: one item of inbox.json `dumped`, keys in that order (LLR-4407.3); `board` is the board file's path as str.

[Data: Inbox state]
in: Inbox(Path path, str pad, list[DumpedEntry] dumped, list[tuple[str, DumpedEntry]] pending, bool divider_notice, dict load_report, tuple? stamp)
desc: public read-only attributes `path`, `pad`, `dumped`, `pending` (("record" | "drop", entry) in the order made, never written to the store, ARCH-4), `divider_notice`, `load_report`, `images_dir` (= path.parent / "inbox-images"); G-V changes them only through write_pad and mark_notice, and reads the pad to show through `pad_now()`. The app holds one Inbox, loaded in TaskboardApp.__init__ beside the registry, so pending records survive closing the view.

[Data: inbox.json]
in: {"version": 1, "pad": str, "dumped": list, "divider_notice"?: true}
desc: `json.dumps(indent=2, ensure_ascii=False)`, written only by Inbox.write_pad and Inbox.mark_notice under `file_lock`, through `write_atomic`.

[Data: Doc]
in: NamedTuple(int lane, str board_name, str board_colour, Path board_path, str project_id, str project_name, str project_colour, int position, Counter tf, dict vec, float norm)
desc: suggest.py; the board chip data (name, colour) and the target path G-V turns into a DumpTarget; `vec` (stem → tf·idf) and `norm` are set once by corpus (ARCH-6).

[Data: Corpus]
in: NamedTuple(list[Doc] docs, dict[str, float] idf)
desc: suggest.py; what corpus returns and suggest reads; built at open and once after each board-changing dump, undo or batch (ARCH-6); `Corpus([], {})` when no readable board holds a live project.

[Data: Hit]
in: NamedTuple(Doc doc, float score, list[str] why)
desc: suggest.py; the option None is NEW_PROJECT (`+ new project`); `why` holds surface words, G-V shows at most 3.

[Data: board file]
in: board.json
desc: written by dump_note and undo_dump only (open board via `live.add_task` / `live.save`; another board via `save_atomic` under `file_lock` with the stamp check).

[Data: history.jsonl]
in: lines {"task", "from", "to", "at"}
desc: dump appends one birth record (open board inside add_task; another board after save_atomic).

[I/O: inbox-images]
desc: the pad images folder beside inbox.json; written by attach_images and undo_dump, emptied of a dump's files by dump_note after its save.

[I/O: task images]
desc: `Board.image_dir(task_id)` on the target board.

[Interface: capture keys]
desc: CaptureView bindings (priority): alt+d dump, alt+o other, alt+n new project, alt+a review, alt+i image, alt+u undo, alt+l divider, escape close; name field: enter, tab (board cycle, shown `⇥ board`; `alt+b` arrives as `ctrl+left` from a terminal, P-V-1), escape. No alt+enter (R1-1).
offers: (TC-4402) "n" → TaskboardApp.action_capture
offers: (TC-4501) "alt+d" → dump_note
offers: (TC-4541) "alt+u" → undo_dump

[Interface: review keys]
desc: ReviewList bindings: up/down move, space include, o other, d dump checked, u undo, escape back.
offers: (TC-4568) "d" → dump_note
offers: (TC-4571) "u" → undo_dump

## Edges

is_divider ──▶ note_parts
note_parts ──▶ note_count
note_parts ──▶ note_at
image_name ──▶ note_task
note_task ──▶ dump_note
note_task ──▶ undo_dump
note_task ──▶ CaptureView
[Data: DumpOutcome] ──▶ entry_for
entry_for ──▶ [Data: DumpedEntry]
entry_for ──▶ Inbox.write_pad
union_pads ──▶ Inbox.write_pad
with_note ──▶ Inbox.write_pad
[Data: Inbox state] ──▶ Inbox.pad_now
Inbox.pad_now ──▶ CaptureView
prune_dumped ──▶ Inbox.write_pad
prune_dumped ──▶ Inbox.last_dump
Inbox.load ──▶ [Data: Inbox state]
Inbox.refresh ──▶ [Data: Inbox state]
Inbox.write_pad ──▶ [Data: inbox.json]
Inbox.write_pad ──▶ [Data: Inbox state]
Inbox.mark_notice ──▶ [Data: inbox.json]
[Data: inbox.json] ──▶ Inbox.load
[Data: inbox.json] ──▶ Inbox.refresh
[Data: Inbox state] ──▶ CaptureView
attach_images ──▶ [I/O: inbox-images]
[I/O: inbox-images] ──▶ dump_note
dump_note ──▶ [Data: board file]
dump_note ──▶ [Data: history.jsonl]
dump_note ──▶ [I/O: task images]
undo_dump ──▶ [Data: board file]
undo_dump ──▶ [I/O: inbox-images]
[Data: DumpTarget] ──▶ dump_note
dump_note ──▶ [Data: DumpOutcome]
undo_dump ──▶ [Data: UndoOutcome]
[Data: DumpOutcome] ──▶ CaptureView
[Data: UndoOutcome] ──▶ CaptureView
[Data: WriteResult] ──▶ CaptureView
words ──▶ corpus
words ──▶ suggest
corpus ──▶ [Data: Doc]
corpus ──▶ [Data: Corpus]
[Data: Doc] ──▶ [Data: Corpus]
[Data: Corpus] ──▶ suggest
suggest ──▶ [Data: Hit]
[Data: Hit] ──▶ options
options ──▶ CaptureView
bars ──▶ CaptureView
note_parts ──▶ CaptureView
note_count ──▶ CaptureView
note_at ──▶ CaptureView
without_note ──▶ CaptureView
with_note ──▶ CaptureView
PadArea ──▶ CaptureView
CaptureView ──▶ ReviewList
TaskboardApp.action_capture ──▶ CaptureView
