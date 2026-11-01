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
func: for a line that, stripped, is `img: <name>` with a name that passes the image-name rule (requirements §1, P-S-10: 1..128 characters, no surrounding whitespace, no `/`, `\`, `:` or control character, not `.` or `..`, a lower-case suffix in `models.IMAGE_EXTS`, no Windows device stem) → the name; otherwise None.
module: taskboard/inbox.py
examples: (TC-4628) line "img: a.png" → name "a.png"
examples: (TC-4628) line "img: ../a.png" → name `None`

note_task
req: LLR-4404.2, LLR-4404.3, LLR-4404.29, LLR-4409.3
in: str text
out: NoteTask task
func: title = `strip_controls(visible_text(line)).strip()` of the title line (the first line that is not an image line and whose visible text is not blank), "" when there is none; notes = the other non-image lines verbatim (markers and mentions kept), outer blank lines removed, control characters removed; images = the image names in line order, each once.
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
in: str fresh_pad; list[str] fresh_dumped; str mine
out: str pad
func: the notes of fresh_pad in their order, then each note of `mine`, in mine's order, whose exact text is neither a note of fresh_pad nor in `fresh_dumped` (the `text` of every fresh `dumped` entry); joined by "\n____\n". Called by Inbox.write_pad only when the file changed (R2 F-8).
module: taskboard/inbox.py
examples: (TC-4599) fresh_pad "a\n____\nc", fresh_dumped "b", mine "a\n____\nb\n____\nd" → pad "a\n____\nc\n____\nd"

prune_dumped
req: LLR-4405.12
in: list[DumpedEntry] entries; datetime now
out: list[DumpedEntry] kept
func: the entries whose `at` parses (`datetime.fromisoformat`, naive) to a moment no more than 604 800 s before now, in their order.
module: taskboard/inbox.py
examples: (TC-4552) entries at "2026-10-25T10:03:00" and "2026-10-25T10:01:00" and "garbage", now 2026-11-01T10:02:00 → kept the first only

Inbox.load
req: LLR-4407.1, LLR-4407.6, LLR-4407.7, LLR-4407.8, LLR-4407.10, LLR-4407.11, LLR-4407.12, LLR-4407.35, LLR-4407.36
in: Path path
out: Inbox inbox
func: `people.Directory.load`'s shape: never raises; missing or blank → empty (pad "", no entries, nothing written); unparseable (not JSON, not an object, `pad` not a str, `dumped` or `flagged` not a list) → `keep_aside` + empty + `load_report {"unreadable": True, "backup": <str or None>}`; larger than `STORE_MAX_BYTES` (8 388 608) → read up to the cap + 1 byte only, unreadable, NOT copied aside (backup None) and never written over (P-S-3); strings through `clean_strings`; bad entries skipped, an entry's shape checked (`task` fullmatches `[A-Za-z0-9_-]{1,64}`, every `images` item passes the image-name rule, `text` non-blank, `new_project` a bool: P-S-4); `divider_notice` only the boolean true; the store stamp (mtime_ns, size) kept. G-V words the notice from `load_report` (backup None → the LLR-4407.38 text, P-V-6).
module: taskboard/inbox.py
modify: [Data: Inbox state] (replace)
examples: (TC-4587) a store holding `{"pad": 5}` → pad "", load_report "unreadable" `True`, `inbox.json.corrupt` written
examples: (TC-4586) no file → pad "", no file created
examples: (TC-4676) a store of 8 388 609 bytes → load_report "unreadable" `True`, backup `None`, no `inbox.json.corrupt`

Inbox.refresh
req: LLR-4407.13, LLR-4407.14
in: Inbox self
out: bool? changed
func: the batch 2026-10-24-batch-02 re-read: stamp unchanged → None (no parse); changed and parsed → state replaced, True; unparseable → False, state kept, the new stamp kept so the same bad file is reported once.
module: taskboard/inbox.py
modify: [Data: Inbox state] (replace)
examples: (TC-4593) a second Inbox wrote pad "x" → changed `True`, pad "x"
examples: (TC-4594) the file made "{not json" → changed `False`, pad as loaded

Inbox.write_pad
req: LLR-4407.2, LLR-4407.3, LLR-4407.4, LLR-4407.5, LLR-4407.9, LLR-4407.18, LLR-4407.19, LLR-4407.20, LLR-4407.26, LLR-4407.33, LLR-4407.34, LLR-4407.37, LLR-4405.4, LLR-4405.12
in: Inbox self; str pad; DumpedEntry? record = None; DumpedEntry? drop = None
out: WriteResult result
func: `Directory._commit`'s shape under `file_lock(path)`: re-read NOW (unparseable and not set aside → OSError, nothing written); pad written = `pad` verbatim when the file's stamp equals the store stamp, else union_pads(fresh pad, fresh dumped texts, pad); dumped = prune_dumped(fresh dumped + [record] − [drop by task id], now); flagged = in-memory flagged ∪ fresh flagged, minus entries whose text is no longer a note of the written pad; `write_atomic(json.dumps({version, pad, dumped[, flagged][, divider_notice]}, indent=2, ensure_ascii=False))`; then state held and stamp taken. Skips the write (returns written False) when pad, record, drop and the flags change nothing. A text over `STORE_MAX_BYTES` raises OSError "inbox.json would hold <n> bytes, over the 8388608-byte limit, so it was not written" (P-S-3). A failed write raises OSError and changes nothing in memory.
module: taskboard/inbox.py
modify: [Data: inbox.json] (replace); [Data: Inbox state] (replace)
examples: (TC-4600) pad "a\n________\n\nb  " on an unchanged file → result pad "a\n________\n\nb  ", union `False`
examples: (TC-4599) the file changed by a second Inbox → result union `True`, pad "a\n____\nc\n____\nd"
examples: (TC-4598) pad equal to the stored pad, no record → result written `False`
examples: (TC-4677) pad "a" × 8 400 000 on a store with no entries and no flag → OSError "inbox.json would hold 8400047 bytes, over the 8388608-byte limit, so it was not written", file and memory unchanged

Inbox.flag
req: LLR-4407.26
in: Inbox self; FlaggedEntry entry
out: None
func: appends the entry to the in-memory flagged list (no write; the next write_pad writes it). G-V calls it when write_pad raises after dump_note succeeded.
module: taskboard/inbox.py
modify: [Data: Inbox state] (append)
examples: (TC-4606) entry text "Volume lab fails on WSL" → flagged holds `1` entry

Inbox.flag_for
req: LLR-4407.31, LLR-4407.32
in: Inbox self; str text
out: FlaggedEntry? entry
func: the flagged entry whose `text` equals the note's text, else None.
module: taskboard/inbox.py
examples: (TC-4672) text "Volume lab fails on WSL" after Inbox.flag → entry board holds "board.json" of Course

Inbox.last_dump
req: LLR-4405.1, LLR-4405.7, LLR-4405.17
in: Inbox self; datetime now
out: DumpedEntry? entry
func: the newest (last by position) entry of prune_dumped(entries, now), else None, where entries = the store FILE's `dumped` read fresh at the call (`_read`, no lock; no state and no stamp change), or the in-memory `dumped` when the file is missing or cannot be parsed (P-S-6).
module: taskboard/inbox.py
examples: (TC-4547) one entry 8 days old → entry `None`
examples: (TC-4557) memory [e1, e2], a second Inbox dropped e2 from the file → entry e1

Inbox.mark_notice
req: LLR-4402.14
in: Inbox self
out: None
func: a `_commit` that sets `divider_notice` true (the pad as the file holds it); raises OSError like write_pad.
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
req: LLR-4407.3, LLR-4407.33
in: DumpOutcome outcome; str note; Path board_path; datetime now
out: DumpedEntry entry
func: public builder of the store record of an ok dump (P-S-15): {"at": stamp(now), "text": note (the Part text, verbatim), "task": outcome.task.id, "title": outcome.task.title, "board": str(board_path), "project": outcome.project_id, "new_project": outcome.new_project, "images": list(outcome.images)} in the LLR-4407.3 key order. G-V passes it to `Inbox.write_pad(record=…)`, and to `Inbox.flag` when that write raises (flag keeps its FLAGGED projection). G-V never builds an entry itself.
module: taskboard/inbox.py
examples: (TC-4583) the AT-4402 dump into Course, now 2026-11-01T10:02:00 → keys ["at", "text", "task", "title", "board", "project", "new_project", "images"], at "2026-11-01T10:02:00", images ["board-0938.png"], new_project `False`

dump_note
req: HLR-4404, LLR-4404.1, LLR-4404.4, LLR-4404.5, LLR-4404.8, LLR-4404.9, LLR-4404.10, LLR-4404.11, LLR-4404.12, LLR-4404.13, LLR-4404.14, LLR-4404.15, LLR-4404.23, LLR-4404.24, LLR-4404.25, LLR-4404.26, LLR-4404.29, LLR-4404.31, LLR-4404.32, LLR-4404.33, LLR-4408.10, LLR-4408.11, LLR-4408.12, LLR-4408.13, LLR-4408.14, LLR-4408.15
in: DumpTarget target; str? project_id; str? new_name; str note; Path folder; str project_name = ""
out: DumpOutcome outcome
func: `project_name` (P-S-1) is the chosen hit's `doc.project_name` ("" for a new project), used only for the LLR-4404.12 refusal "<project_name> is no longer on <board> — nothing dumped.". note_task(note) (title "" → refusal). Exactly one of project_id / new_name. Open board (`target.live` set): checks on the live object, images copied, `live.add_task(task)` (stamps created, writes the birth record, saves); an OSError → task and new project removed from `live`, copies removed, refusal. Other board: `file_lock(target.path, target.name)` held; missing → refusal; `peek_board` fresh, unreadable → refusal; project gone / name blank / name taken → refusal; stamp (mtime, size) taken; task built with `created = models.stamp(now)`, phase = phases[0], new project (colour rule) appended in memory; images copied to `image_dir(task.id)` (a new id while that folder exists); stamp re-checked → refusal on change; `save_atomic`; then `history.append(path, birth, at=now)`; then pad copies removed. Never writes the store and never touches the pad.
module: taskboard/inbox.py
modify: [Data: board file] (replace); [Data: history.jsonl] (append); [I/O: inbox-images] (clear); [I/O: task images] (append)
examples: (TC-4509) target `Course` (live `None`), project "Module 4 · Volumes", note "Volume lab fails on WSL\nthe oracle script expects /mnt/c" → outcome ok `True`, title "Volume lab fails on WSL", the board file holds the task
examples: (TC-4510) target path missing → outcome ok `False`, notice "Course's file is missing — nothing dumped."
examples: (TC-4533) the file rewritten between the read and the save → outcome ok `False`, notice "Course changed while dumping — nothing dumped."

undo_dump
req: HLR-4405, LLR-4405.2, LLR-4405.5, LLR-4405.6, LLR-4405.8, LLR-4405.10, LLR-4405.11, LLR-4408.16, LLR-4408.17
in: DumpedEntry entry; Board? live; Path folder
out: UndoOutcome outcome
func: G-V calls it only when `entry.board` is the file (samefile) of a lane `board_lanes` returns; otherwise G-V shows "<board path> is not a known board — nothing undone." and keeps the entry (P-S-4, LLR-4405.16). `live` is the open board when `entry.board` is its file (G-V decides), else None and the board is read fresh under `file_lock` with the stamp check and `save_atomic`. Task id absent → state "gone" (no board change). Title or notes differ from `_task_fields(entry.text, moved=set(entry.images))` — the title and notes the dump wrote, a missing image's line kept as text (P-S-2) — → state "changed" (nothing changes). Else the task removed (and the project when `new_project` and no other task holds it), saved, its image files moved back to `folder` (renamed `<stem>-<k>` when taken), the emptied `image_dir` removed → state "undone". A read, lock or save failure → state "failed" with the error text. note_text = entry.text with each moved image line naming the file as it now is.
module: taskboard/inbox.py
modify: [Data: board file] (replace); [I/O: inbox-images] (append); [I/O: task images] (clear)
examples: (TC-4548) the task deleted after the dump → outcome state "gone", note_text holds "Volume lab fails on WSL"
examples: (TC-4550) the task title edited → outcome state "changed"
examples: (TC-4626) "paste-001.png" taken in folder → note_text holds "img: paste-001-2.png"

words
req: LLR-4403.1, LLR-4403.2
in: str text
out: list[tuple[str, str]] pairs
func: (stem, surface) for each word that counts: accents folded, lower case, `@handle` or `[a-z0-9]+`, length ≥ 3, not a bare number, not in STOP; stem: `ies`→`y` (len > 4), final `s` not `ss` dropped (len > 3), cut to 6; a handle unstemmed.
module: taskboard/suggest.py
examples: (TC-4461) text "Golden SET: 12 Questions @username_subject de la Café" → pairs ("questi", "questions") and ("@username_subject", "@username_subject"), no "12"

corpus
req: LLR-4403.3, LLR-4403.4, LLR-4403.5, LLR-4403.23, LLR-4403.24, LLR-4403.27
in: list[tuple[str, str, Board?, str]] lanes; dict marks
out: list[Doc] docs
func: one Doc per non-archived project of each lane whose board is not None, lane order then project position; tf weights name ×3, titles of its non-archived tasks ×2, `@handle` in their notes ×2, the `marks[t.mark].name` of each milestone with a known mark ×1, other note words ×1; tasks with no project are skipped. Each document's text is cut at `DOC_CHARS` (100 000) characters before tokenising: the fields are consumed in the order name, then per task title, notes, mark name, each sliced to the characters left (P-T-5). `lanes` is `board_lanes(app)[0]`, `marks` is `app.marks.marks`. Pure; reads no file.
module: taskboard/suggest.py
examples: (TC-4464) project "Eval harness", task "Answer key", notes "ask @username_subject key", milestone mark "payment" named "Payment" → tf "eval" `3`, "key" `3`, "@username_subject" `2`, "paymen" `1`
examples: (TC-4463) 3 live projects and 1 archived over 2 lanes → docs `3`

suggest
req: LLR-4403.6, LLR-4403.7, LLR-4403.8, LLR-4403.9, LLR-4403.10, LLR-4403.14, LLR-4403.22, LLR-4403.26, LLR-4403.28
in: str note; list[Doc] docs
out: list[Hit] hits
func: `note` is the note's scored text: G-V passes `nt.title + "\n" + nt.notes` of `inbox.note_task(part.text)` (image lines left out, P-T-4); suggest.py imports no inbox. The first `NOTE_CHARS` (10 000, a suggest.py constant, P-T-1) characters of note; idf = ln((N+1)/(df+1)) + 1, a note stem no document holds weighs 0; score = cosine of tf·idf, halved on exactly one shared stem, rounded to 4 decimals; hits with score ≥ LOW (0.08), ordered by (−score, lane, project name casefolded, project name, position) (P-T-3), at most 3; why = the note's surface words of the shared stems, largest contribution first, ties by stem. Deterministic; [] for no docs.
module: taskboard/suggest.py
examples: (TC-4474) note "Golden set: 12 questions still have no answer key ask @username_subject" → hit "Eval harness" first, why "questions", "@username_subject", "key"
examples: (TC-4485) docs `[]` → hits `[]`

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
req: HLR-4401, LLR-4401.4, LLR-4401.5, LLR-4401.6, LLR-4401.7, LLR-4401.8, LLR-4401.9, LLR-4401.10, LLR-4403.15, LLR-4403.21, LLR-4407.15, LLR-4407.16, LLR-4407.17, LLR-4407.29
in:
out: Screen screen
func: app.py Screen[None]: on open `app.inbox.refresh()`, lanes/ids = board_lanes(app), docs = corpus(lanes, app.marks.marks), a hit cache `dict[str, list[Hit]]` keyed by the Part text, filled by `suggest(nt.title + "\n" + nt.notes, docs)` (P-T-4), cleared with every new docs; pad = PadArea(inbox.pad). Dump: target = DumpTarget(path, name, live=app.board when the path is the open board's file, else None) → dump_note(…, project_name=hit.doc.project_name) → on ok: without_note, entry = entry_for(out, part.text, path, now), inbox.write_pad(pad, record=entry) (OSError → inbox.flag(entry) + the flagged notice), refresh_view, docs rebuilt. After any write G-V replaces its pad text whenever `result.written and result.pad != text`, and shows the merge notice only when `result.union` (P-S-8). Undo: inbox.last_dump(now) → (entry.board a lane's file, else the P-S-4 refusal) → undo_dump → with_note + write_pad(drop=entry). Every notice is shown with `markup=False`; G-S's refusal texts verbatim (P-V-13).
module: taskboard/app.py
examples: (TC-4402) app with 2 registry boards, press n → app.screen is a CaptureView

ReviewList
req: HLR-4406, LLR-4406.1, LLR-4406.8, LLR-4406.9, LLR-4406.16
in: list[str] notes
out: ModalScreen screen
func: one row per note; the chosen option per note text is the CaptureView's dict (shared); `d` calls the CaptureView's one dump path per checked row in pad order and counts the oks.
module: taskboard/app.py
examples: (TC-4568) 3 of 4 checked → 3 dump_note calls

TaskboardApp.action_capture
req: LLR-4401.2, LLR-4401.14
in: TaskboardApp self
out: None
func: `self._bring(CaptureView, CaptureView)`, as action_added_list; `capture` is added to check_action's always-allowed tuple and CaptureView to its holding tuple (R1-6).
module: taskboard/app.py
examples: (TC-4414) N, n → exactly one CaptureView in app.screen_stack and it is app.screen

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
desc: inbox.py; state ∈ {"undone", "gone", "changed", "failed"}; G-V restores note_text to the pad for "undone" and "gone" and words the notices; `notice` carries the error text for "failed".

[Data: WriteResult]
in: NamedTuple(bool written, str pad, bool union)
desc: inbox.py; `pad` is what the file now holds; G-V replaces its pad text whenever `written and pad != the text it passed` (a union, or stripped control characters), and shows the merge notice only when `union` is True (P-S-8).

[Data: AttachResult]
in: NamedTuple(list[str] names, str? notice)
desc: inbox.py; G-V inserts one `img: <name>` line per name after the cursor's note, then write_pad.

[Data: DumpedEntry]
in: dict(str at, str text, str task, str title, str board, str project, bool new_project, list[str] images)
desc: one item of inbox.json `dumped`, keys in that order (LLR-4407.3); `board` is the board file's path as str.

[Data: FlaggedEntry]
in: dict(str at, str text, str task, str title, str board, str project)
desc: one item of inbox.json `flagged`, keys in that order (LLR-4407.33); written only while the list is non-empty.

[Data: Inbox state]
in: Inbox(Path path, str pad, list[DumpedEntry] dumped, list[FlaggedEntry] flagged, bool divider_notice, dict load_report, tuple? stamp)
desc: public read-only attributes `path`, `pad`, `dumped`, `flagged`, `divider_notice`, `load_report`, `images_dir` (= path.parent / "inbox-images"); G-V changes them only through write_pad, flag and mark_notice. The app holds one Inbox, loaded in TaskboardApp.__init__ beside the registry.

[Data: inbox.json]
in: {"version": 1, "pad": str, "dumped": list, "flagged"?: list, "divider_notice"?: true}
desc: `json.dumps(indent=2, ensure_ascii=False)`, written only by Inbox.write_pad and Inbox.mark_notice under `file_lock`, through `write_atomic`.

[Data: Doc]
in: NamedTuple(int lane, str board_name, str board_colour, Path board_path, str project_id, str project_name, str project_colour, int position, Counter tf)
desc: suggest.py; the board chip data (name, colour) and the target path G-V turns into a DumpTarget.

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
entry_for ──▶ Inbox.flag
union_pads ──▶ Inbox.write_pad
prune_dumped ──▶ Inbox.write_pad
prune_dumped ──▶ Inbox.last_dump
Inbox.load ──▶ [Data: Inbox state]
Inbox.refresh ──▶ [Data: Inbox state]
Inbox.write_pad ──▶ [Data: inbox.json]
Inbox.write_pad ──▶ [Data: Inbox state]
Inbox.mark_notice ──▶ [Data: inbox.json]
Inbox.flag ──▶ [Data: Inbox state]
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
[Data: Doc] ──▶ suggest
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
