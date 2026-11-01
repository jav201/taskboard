# Code-Wire prototype — group G-S: `taskboard/inbox.py` (Inc K, E2b)

New file; no baseline node changes. The interface nodes of `graph-interfaces.cw.md` with `module: taskboard/inbox.py` keep their contracts there; each is listed again here ONLY with what the interface leaves open (caps, order, failure handling, exact texts) and the examples that cover every LLR of this group. Private nodes are new. No code was written.

E2 correction pass (round 0b, `03-pdr-rulings.md`): every finding below carries its ruling; P-S-1, P-S-2, P-S-3, P-S-4, P-S-5, P-S-6, P-S-7, P-S-8, P-S-9, P-S-10, P-S-14 and P-S-15 are applied in the nodes (new LLRs LLR-4405.17, LLR-4407.35, LLR-4407.36, LLR-4407.37, LLR-4407.38, LLR-4408.19; LED-2026-11-01-incK.3).

Fixture S (G-S's layer-0 fixture for tests/test_inbox_store.py, tests/test_capture_dump.py and tests/test_capture_images.py; synthetic, as graph-interfaces: the same two boards, lanes, phases and project names as G-T/G-V's fixture F; its ids, colours and paths are its own and are not mixed with F's): clock now 2026-11-01T10:02:00. Store folder `S` (the registry's folder); store `S/inbox.json`; pad images folder `F` = `S/inbox-images`. Boards: `A` = `S/a/board.json` "Client A" (the open board, lane 0, phases ["Backlog", "Doing", "Done"], projects `pe` "Eval harness" colour "lime", `pp` "Pilot rollout" colour "green"); `C` = `S/c/board.json` "Course" (lane 1, phases ["Todo", "Doing", "Done"], project `pm` "Module 4 · Volumes" colour "sky", task `tc1` "Old one" in `pm`). New task ids come from `taskboard.models._new_id`, patched in the tests to yield "t0000001", "t0000002", … (dump_note calls it through the module at call time, because `Task`'s default factory is bound at class creation and a patch would not reach `Task()`: probe `%TEMP%/incK-probe-S/p1.py`, "Task() id after patch: 8ab9052d").

Untrusted inputs and their caps (security brief): (1) the store file — read at most `STORE_MAX_BYTES` + 1 bytes; over the cap it is not parsed, not copied aside and never written over; any JSON shape is validated field by field, every string through `clean_strings`, entries of the wrong shape skipped, and the two path-forming fields (`task`, `images`) checked against a strict pattern so no store entry can name a path outside `images/<id>/` or `F`; (2) note text — every pass is linear (no regex backtracking, no per-offset re-encode), controls removed before a title or notes reach a board (`strip_controls`), markup never interpreted here (G-V draws literal text); (3) image names — a bare name only (`_image_ok`), symlinks and non-regular files never followed on the move paths (`os.lstat` + `S_ISREG`), a taken name never overwritten (`os.path.lexists`, so a dangling symlink counts as taken), task folders created exclusively.

## Nodes

_image_ok
req: LLR-4408.18, LLR-4408.3
in: str name
out: bool ok
func: True exactly when all hold: 1 ≤ len(name) ≤ `IMAGE_NAME_MAX` (128); name == name.strip(); no character in `/`, `\`, `:` and none below U+0020, U+007F, or in U+0080..U+009F; name not in (".", ".."); `os.path.splitext(name)[1].lower()` in `models.IMAGE_EXTS` (so ".png" alone, whose splitext suffix is "", is refused); the part before the first "." lower-cased is not a Windows device stem (`con`, `prn`, `aux`, `nul`, `com1`..`com9`, `lpt1`..`lpt9`). Pure, linear in len(name). The full rule is LLR-4408.18 and requirements §1 "image-name rule" (P-S-10 ruled ACCEPT)
module: taskboard/inbox.py
examples: (TC-4628) name "a.png" → ok `True`; name "A.PNG" → ok `True`
examples: (TC-4628) name "../a.png" → ok `False`; name "C:\a.png" → ok `False`; name "sub/a.png" → ok `False`; name "a.svg" → ok `False`; name "a" → ok `False`; name ".png" → ok `False`
examples: (TC-4628) name "con.png" → ok `False`; name "a\x07.png" → ok `False`; name 129 × "a" + ".png" → ok `False`

image_name
req: LLR-4408.18
in: str line
out: str? name
func: INTERFACE + exact parse: s = line.strip(); s must start with the 5 characters "img: "; name = s[5:]; returns name when `_image_ok(name)`, else None. "img:a.png" (no space) and "IMG: a.png" are not image lines. Linear
module: taskboard/inbox.py
examples: (TC-4628) line "  img: a.png  " → name "a.png"
examples: (TC-4628) line "img: C:\a.png" → name `None`; line "img: sub/a.png" → name `None`; line "img: a.svg" → name `None`; line "img: a" → name `None`
examples: (TC-4628) line "img:a.png" → name `None`; line "img:  a.png" → name `None` (the name would start with a space)

is_divider
req: LLR-4402.1
in: str line
out: bool divider
func: INTERFACE; implemented as `DIVIDER_RE.fullmatch(line.rstrip())` with `DIVIDER_RE = re.compile("_{4,}")` (no backtracking: one character class); a 10 MB line is one linear scan
module: taskboard/inbox.py
examples: (TC-4431) line "____" → divider `True`; line "________" → divider `True`
examples: (TC-4431) line "___" → divider `False`; line "____x" → divider `False`; line "__ __" → divider `False`

note_parts
req: LLR-4402.2, LLR-4402.3, LLR-4402.4, LLR-4402.5
in: str text
out: list[Part] parts
func: INTERFACE + boundaries: lines = text.split("\n") (text "" is one line ""). A part with no line (two adjacent dividers, or a divider as the last line) is Part(start = the index after the divider, end = start − 1, text "", is_note False). "Blank" = `line.strip() == ""`. Part.text = the part's lines from the first non-blank to the last non-blank, joined by "\n" (inner lines verbatim, trailing spaces of inner lines kept). The pad never holds "\r" (store strings and written pads pass `strip_controls`), so no CR handling is needed
module: taskboard/inbox.py
examples: (TC-4432) text "a\nb\n____\nc" → parts Part(0, 1, "a\nb", True), Part(3, 3, "c", True)
examples: (TC-4432) text "a\n____\n____\nb" → parts `3`: Part(0, 0, "a", True), Part(2, 1, "", False), Part(3, 3, "b", True)
examples: (TC-4435) text "\n\na\n\n____" → parts Part(0, 3, "a", True), Part(5, 4, "", False)
examples: (TC-4433) text "a\n\nb\n____\nc" → notes `2`, the first "a\n\nb"
examples: (TC-4434) text "____\n \t\n____\na" → parts Part(0, -1, "", False), Part(1, 1, "", False), Part(3, 3, "a", True): `1` note

note_count
req: LLR-4402.8
in: str text
out: int count
func: INTERFACE; "the last part holds at least one line" = last.end ≥ last.start; "follows a divider" = len(parts) > 1
module: taskboard/inbox.py
examples: (TC-4438) text "a\n____\n\n____\nb" → count `2`
examples: (TC-4438) text "a" → count `1`
examples: (TC-4438) text "" → count `0`

note_at
req: LLR-4404.30, LLR-4404.28, LLR-4408.8
in: str text; int row
out: Part? part
func: INTERFACE + edges: a row outside 0..len(lines) − 1 → None; on a divider line the part directly above it is taken, and None when that part is not a note (the search does not go further up)
module: taskboard/inbox.py
examples: (TC-4530) text "a\n____\nb", row `2` → part text "b"
examples: (TC-4530) text "____\na", row `0` → part `None`
examples: (TC-4528) text "a\n____\n  ", row `2` → part `None`
examples: (TC-4618) text "", row `0` → part `None` (G-V shows "No note under the cursor."; `0` files written)

_title_row
req: LLR-4404.2, LLR-4404.29
in: list[str] lines
out: int? row
func: the index of the first line for which `image_name(line)` is None and `strip_controls(modals.visible_text(line)).strip()` is not ""; None when no line qualifies. `visible_text` is `highlight_segments` joined (linear, LLR-4201.10). Each line is tested once
module: taskboard/inbox.py
examples: (TC-4502) lines ["img: a.png", "Title", "x"] → row `1`
examples: (TC-4529) lines ["::b:: ::"] → row `None`

_task_fields
req: LLR-4404.2, LLR-4404.3, LLR-4408.12, LLR-4409.2, LLR-4409.3, LLR-4405.10
in: str text; set[str] moved
out: tuple(str title, str notes)
func: the title and notes a dump writes, given the image names whose files it moved (`moved`, compared by `os.path.normcase`). lines = text.split("\n"); r = _title_row(lines); title = strip_controls(visible_text(lines[r])).strip() ("" when r is None). notes = every line except row r and except the image lines whose name is in `moved`, in order, verbatim (colour markers, `@mentions`, inner blank lines and an image line whose file was NOT moved stay as text), leading and trailing blank lines removed, then `strip_controls`. One function for the dump (moved = the names copied) and for the undo's "changed" check (moved = the entry's `images`), so a note with a missing image is not seen as edited (finding P-S-2)
module: taskboard/inbox.py
examples: (TC-4503) text "T\n\nask @username_subject ::r:: now ::\n\nsecond\nimg: a.png\n", moved {"a.png"} → title "T", notes "ask @username_subject ::r:: now ::\n\nsecond"
examples: (TC-4622) text "T\nx\nimg: gone.png", moved `{}` → title "T", notes "x\nimg: gone.png"
examples: (TC-4632) text "T\n::b:: x :: @username_subject", moved `{}` → notes "::b:: x :: @username_subject" (byte for byte)
examples: (TC-4633) text "\x1b[2J T\na\x07b", moved `{}` → title "[2J T", notes "ab"

note_task
req: LLR-4404.2, LLR-4404.3, LLR-4404.29, LLR-4409.2, LLR-4409.3
in: str text
out: NoteTask task
func: INTERFACE; title, notes = _task_fields(text, moved = every image name of the note) — the notes as written when every image is found; images = the image names in line order, each once (the first spelling kept; duplicates by `os.path.normcase`, so "A.png" and "a.png" are one name on every system). G-V's rail count `▣ n` counts image LINES, not this list (see Seams)
module: taskboard/inbox.py
examples: (TC-4502) text "img: a.png\nTitle\nx" → title "Title", notes "x", images "a.png"
examples: (TC-4625) text "T\nimg: a.png\nimg: a.png" → images ["a.png"] (`1` name)
examples: (TC-4632) text "Golden set\n::b:: ask the vendor :: @username_subject" → title "Golden set", notes "::b:: ask the vendor :: @username_subject"
examples: (TC-4633) text "\x1b[2J T\na\x07b" → title "[2J T", notes "ab"; no character below U+0020 other than "\t" and "\n", no U+007F and no U+0080..U+009F in either
examples: (TC-4529) text "::b:: ::" → title ""

without_note
req: LLR-4404.6
in: str text; Part part
out: tuple(str text, int row)
func: INTERFACE + the removed span is lines part.start..part.end (the part's own blank lines included); the adjacent divider is line part.end + 1 when it exists and `is_divider`, else line part.start − 1 when ≥ 0 and `is_divider`, else none. Removing the only note gives "" and row `0`
module: taskboard/inbox.py
examples: (TC-4506) text "a\n____\nb\n____\nc", part of "c" (4, 4) → text "a\n____\nb", row `2`
examples: (TC-4506) text "a\n____\nb\n____\nc", part of "a" (0, 0) → text "b\n____\nc", row `0`
examples: (TC-4506) text "a\n____\n\nb\n\n____\nc", part (2, 4) → text "a\n____\nc"

with_note
req: LLR-4405.3
in: str text; str note
out: str text
func: INTERFACE + trailing handling (finding P-S-14): lines = text.split("\n") with the trailing blank lines dropped (they belong to no note); none left → `note`; the last kept line a divider → kept lines + note (the note fills the part being started); else kept lines + "____" + note; joined by "\n". Every kept line byte-identical
module: taskboard/inbox.py
examples: (TC-4543) text "a\n", note "b" → text "a\n____\nb"
examples: (TC-4543) text "a\n____\n", note "b" → text "a\n____\nb"

union_pads
req: LLR-4407.19
in: str fresh_pad; list[str] fresh_dumped; str mine
out: str pad
func: INTERFACE; note texts are Part.text of `note_parts` with is_note True; membership by exact string equality (sets built once: linear); duplicates inside `mine` that pass are all kept; no notes at all → ""
module: taskboard/inbox.py
examples: (TC-4599) fresh_pad "a\n____\nc", fresh_dumped `[]`, mine "a" → pad "a\n____\nc" (a note deleted here but present in the fresh pad comes back)

prune_dumped
req: LLR-4405.12
in: list[DumpedEntry] entries; datetime now
out: list[DumpedEntry] kept
func: INTERFACE + validity: `at` must fullmatch `STAMP_RE` `\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d` and parse with `datetime.fromisoformat` (ValueError → dropped), which makes it naive; kept when (now − at).total_seconds() ≤ `KEEP_SECONDS` (604 800); an `at` later than now is kept (harmless: it is only ever the last undo candidate by position)
module: taskboard/inbox.py
examples: (TC-4552) entries at "2026-10-25" and "2026-10-25T10:03:00+00:00", now 2026-11-01T10:02:00 → kept `[]` (date only and aware stamps are not stamps)
examples: (TC-4552) entries at "2026-10-25T10:02:00" (exactly 604 800 s), now 2026-11-01T10:02:00 → kept the entry

entry_for
req: LLR-4407.3, LLR-4407.33
in: DumpOutcome outcome; str note; Path board; datetime now
out: DumpedEntry entry
func: public helper (P-S-15 ruled ACCEPT; graph-interfaces amended): the dumped entry G-V passes to `Inbox.write_pad(record=…)` and to `Inbox.flag`, built in the key order of LLR-4407.3: {"at": stamp(now), "text": note (the Part.text, verbatim), "task": outcome.task.id, "title": outcome.task.title, "board": str(board), "project": outcome.project_id, "new_project": outcome.new_project, "images": list(outcome.images)}
module: taskboard/inbox.py
examples: (TC-4583) the AT-4402 dump into Course → keys ["at", "text", "task", "title", "board", "project", "new_project", "images"] exactly, types str, str, str, str, str, str, bool, list; task "t0000001", project "pm", new_project `False`
examples: (TC-4583) the same outcome, now 2026-11-01T10:02:00 → at "2026-11-01T10:02:00", text "Volume lab fails on WSL\nthe oracle script expects /mnt/c"

Inbox.__init__
req: LLR-4407.1, LLR-4408.1
in: Path path
out: None
func: path = Path(path); images_dir = path.parent / `IMAGES_NAME` ("inbox-images"); pad ""; dumped []; flagged []; divider_notice False; load_report {}; `_stamp` None; `_unsaved_flags` [] (flags not yet written, P-S-7). Creates nothing on disk
module: taskboard/inbox.py
modify: [Data: Inbox state] (replace)
examples: (TC-4611) path "S/inbox.json" → images_dir "S/inbox-images"; exists `False`

Inbox._read
req: LLR-4407.7, LLR-4407.10, LLR-4407.11, LLR-4407.12, LLR-4402.15, LLR-4407.35
in: Path path
out: dict? state
func: static. Opens `path` "rb" and reads at most STORE_MAX_BYTES + 1 bytes (an OSError raises: the caller decides). More than STORE_MAX_BYTES (8 388 608) read → None (too large; `_too_big` says why). Else inside one `try` catching (ValueError, RecursionError) — UnicodeDecodeError and the 4300-digit int limit are ValueErrors — `raw = clean_strings(json.loads(data.decode("utf-8")))`. None when raw is not a dict, or `pad` is present and not a str, or `dumped` / `flagged` is present and not a list. Otherwise {"pad": raw.get("pad", ""), "dumped": [Inbox._entry(e, DUMPED) …, skipping None], "flagged": [Inbox._entry(e, FLAGGED) …, skipping None], "divider_notice": raw.get("divider_notice") is True}. `version` and unknown keys are ignored (not kept, as people.json)
module: taskboard/inbox.py
examples: (TC-4591) file {"pad": "a\u001b[31mb\u0007"} → state pad "a[31mb" (no "\x1b", no "\x07")
examples: (TC-4592) file {"pad": "", "divider_notice": "yes"} → divider_notice `False`; {"divider_notice": 1} → `False`; {"divider_notice": true} → `True`
examples: (TC-4587) file "[1, 2]" → state `None`; file {"pad": "", "flagged": "x"} → state `None`
examples: (TC-4675) file of 8 388 609 bytes → state `None`, read `8388609` bytes at most (spy on the read); file of 8 388 608 bytes holding a valid store → state read normally

Inbox._entry
req: LLR-4407.10, LLR-4407.11
in: object item; tuple fields
out: dict? entry
func: static. DUMPED fields = (at str, text str, task str, title str, board str, project str, new_project bool, images list); FLAGGED = the first six. None unless: item is a dict; every field present with that exact type (`type(v) is bool` for new_project, so 0/1 are refused); `task` fullmatches `ID_RE` `[A-Za-z0-9_-]{1,64}` (it forms the path `images/<task>/`); `board` non-empty; `text.strip()` non-empty; every `images` item is a str with `_image_ok` true. Returns a NEW dict holding only those fields in that order (unknown keys dropped), so a hostile store can name no path outside `F` or a board's `images/<id>/` (finding P-S-4)
module: taskboard/inbox.py
examples: (TC-4590) dumped [[1], {…good, "task": 5}, {…good without "at"}, good] → `1` entry read, the good one
examples: (TC-4590) a dumped entry with task "../x" → entry `None`; with images ["../../a.png"] → entry `None`; with new_project `1` → entry `None`

Inbox._too_big
req: LLR-4407.7, LLR-4407.9, LLR-4407.36
in: Path path
out: bool big
func: `os.stat(path).st_size > STORE_MAX_BYTES`; an OSError → False. Asked before `keep_aside`, which reads the WHOLE file into memory: a too-large store is not copied aside (backup None) and therefore never written over (finding P-S-3)
module: taskboard/inbox.py
examples: (TC-4676) a store of 8 388 609 bytes → big `True`; of 8 388 608 bytes → big `False`

Inbox.load
req: LLR-4407.1, LLR-4407.6, LLR-4407.7, LLR-4407.8, LLR-4407.10, LLR-4407.11, LLR-4407.12, LLR-4402.15, LLR-4407.35, LLR-4407.36, LLR-4407.38
in: Path path
out: Inbox inbox
func: INTERFACE + order: inbox = Inbox(path). try: missing, or the capped read is blank after `.strip()` → empty, `_stamped()`, return (nothing written). state = `_read(path)` (OSError → None). None → backup = None when `_too_big(path)` else `keep_aside(path)`; load_report = {"unreadable": True, "backup": str(backup) or None}; empty state. Else `_hold(state)`. Then `_stamped()`. Never raises. G-V words the notice: "inbox.json could not be read; it was copied to <Path(backup).name> and the pad starts empty." (LLR-4407.8), or, backup None, "inbox.json could not be read and no copy could be kept; the pad starts empty." (LLR-4407.38, the P-V-6 wording ruled for P-S-3's case)
module: taskboard/inbox.py
modify: [Data: Inbox state] (replace); [I/O: inbox.json.corrupt] (append)
examples: (TC-4587) store "{not json" → `S/inbox.json.corrupt` byte-equal "{not json"; store "[1, 2]" → the copy byte-equal; store {"pad": 5} → the copy byte-equal; store {"pad": "", "dumped": {}} → the copy byte-equal; store {"pad": "", "flagged": "x"} → the copy byte-equal (5/5, fresh folder each)
examples: (TC-4588) store {"pad": 5} → pad "", load_report "unreadable" `True`, backup ends with "inbox.json.corrupt"
examples: (TC-4676) a store of 8 388 609 bytes → load_report "unreadable" `True`, backup `None`, no `S/inbox.json.corrupt`
examples: (TC-4675) a store of 8 388 609 bytes → pad "", load_report "unreadable" `True` (read up to the cap + 1 byte only)
examples: (TC-4678) store {"pad": 5} with keep_aside patched to return `None` → load_report {"unreadable": `True`, "backup": `None`} (G-V shows the LLR-4407.38 notice)
examples: (TC-4590) store with dumped [[1], {"task": 5, …}, {no "at", …}, one good entry] → dumped `1` entry, load_report `{}`
examples: (TC-4445) store {"version": 1, "pad": "", "dumped": [], "divider_notice": true} → divider_notice `True`
examples: (TC-4581) path "S/inbox.json" missing → pad "", no file in `S`

Inbox._hold
req: LLR-4407.6
in: dict state
out: None
func: sets pad, dumped, flagged, divider_notice from `state` (lists copied)
module: taskboard/inbox.py
modify: [Data: Inbox state] (replace)
examples: (TC-4586) state pad "" dumped `[]` → pad "", dumped `[]`

Inbox._stamped
req: LLR-4407.13, LLR-4407.20
in:
out: None
func: `_stamp` = (st_mtime_ns, st_size) of `os.stat(path)`; OSError (missing) → `_stamp` = None. Taken after every load, refresh and successful write (mark_notice: see there)
module: taskboard/inbox.py
modify: [Data: Inbox._stamp] (replace)
examples: (TC-4593) after load of an existing store → _stamp holds its size

Inbox.refresh
req: LLR-4407.13, LLR-4407.14, LLR-4407.26
in: Inbox self
out: bool? changed
func: INTERFACE + two rules. (1) stat OSError (the file gone) → None, state kept. (2) A changed and parsed file replaces pad, dumped and divider_notice, and flagged = the file's flagged + each entry of `_unsaved_flags` whose (task, board) the file lacks: a flag made after a failed write survives a re-read until a write succeeds (P-S-7 ruled ACCEPT; without it the note becomes dumpable again: a duplicate task). A too-large file counts as unparseable (no read past the cap). The stamp is taken in every changed case
module: taskboard/inbox.py
modify: [Data: Inbox state] (replace); [Data: Inbox._stamp] (replace)
examples: (TC-4593) store unchanged since load → changed `None`, `0` calls of Inbox._read (spy)
examples: (TC-4606) Inbox.flag(entry of "Volume lab fails on WSL") with no write since, then a second Inbox writes pad "x" → changed `True`, pad "x", flagged still holds `1` entry
examples: (TC-4594) the file made "{not json", refresh → `False`; refresh again with the file unchanged → `None` (reported once)

Inbox._set_aside
req: LLR-4407.9
in:
out: bool kept
func: people's `_set_aside` plus the cap: `_too_big(path)` → False; read OSError → False; empty bytes → True; the same bytes as `load_report["backup"]` → True (no second copy); else `keep_aside(path) is not None`
module: taskboard/inbox.py
modify: [I/O: inbox.json.corrupt] (append)
examples: (TC-4589) `keep_aside` patched to return `None`, store "{not json" → kept `False`
examples: (TC-4587) a store loaded from "{not json" (copy made at load), same bytes now → kept `True`, still one "inbox.json.corrupt"

Inbox._shape
req: LLR-4407.2, LLR-4407.3, LLR-4407.33
in: dict state
out: str text
func: `json.dumps(data, indent=2, ensure_ascii=False)` where data = {"version": 1, "pad": state.pad, "dumped": [each entry re-built in DUMPED key order]}, then "flagged": [FLAGGED key order] only when non-empty, then "divider_notice": True only when set — in that key order. No trailing newline (as people.json)
module: taskboard/inbox.py
examples: (TC-4582) state pad "é\n____\nb", dumped `[]`, no flag → text "{\n  \"version\": 1,\n  \"pad\": \"é\\n____\\nb\",\n  \"dumped\": []\n}"; the bytes hold C3 A9 for "é", not "\u00e9" (probe p2)
examples: (TC-4582) the same state with divider_notice `True` → the text ends ",\n  \"divider_notice\": true\n}"; with flagged `[]` → no "flagged" key
examples: (TC-4673) one flagged entry → its keys ["at", "text", "task", "title", "board", "project"] exactly, types all str

Inbox._commit
req: LLR-4407.4, LLR-4407.5, LLR-4407.9, LLR-4407.23, LLR-4405.12, LLR-4407.37
in: (Callable) dict,bool->dict change
out: dict written
func: the read-modify-write shared by write_pad and mark_notice (people's `_commit` shape, R0-10): `path.parent.mkdir(parents=True, exist_ok=True)`; `with file_lock(path, "inbox.json")`: before = stat stamp (None when missing); fresh = None; if the file exists: fresh = `_read(path)` (an OSError raises); fresh None and not `_set_aside()` → raise OSError "inbox.json cannot be read and could not be copied aside, so it was not written" (too large: "inbox.json is larger than 8388608 bytes, so it was not written"). base = fresh, or the in-memory state when fresh is None (missing, or set aside). changed = fresh is not None and before != `_stamp`. new = change(base, changed); new.dumped = prune_dumped(new.dumped, now); text = `_shape(new)`; len(text.encode("utf-8")) > STORE_MAX_BYTES → raise OSError "inbox.json would hold <n> bytes, over the 8388608-byte limit, so it was not written"; `models.write_atomic(path, text)`. Any OSError leaves memory unchanged (it propagates before the hold). The caller holds the result. The lock label makes the busy text "inbox.json is busy — another taskboard is writing it; try again in a few seconds (<lock>)"
module: taskboard/inbox.py
modify: [Data: inbox.json] (replace); [I/O: inbox.json.lock] (replace)
examples: (TC-4584) during write_atomic (spy) → "S/inbox.json.lock" exists `True`; after → exists `False`
examples: (TC-4585) write_atomic (spy) called `1` time with path "S/inbox.json"; write_atomic patched to raise OSError("disk full") → OSError "disk full", the file's old bytes and the in-memory pad unchanged
examples: (TC-4603) a fresh foreign "S/inbox.json.lock" → OSError after `2.0` s holding "inbox.json is busy"; pad and dumped in memory unchanged
examples: (TC-4677) change giving pad "a" × 8 400 000 on a store with no entries and no flag → OSError "inbox.json would hold 8400047 bytes, over the 8388608-byte limit, so it was not written"; write_atomic called `0` times; file bytes and memory unchanged

Inbox.write_pad
req: LLR-4407.2, LLR-4407.3, LLR-4407.4, LLR-4407.5, LLR-4407.9, LLR-4407.18, LLR-4407.19, LLR-4407.20, LLR-4407.23, LLR-4407.26, LLR-4407.27, LLR-4407.33, LLR-4407.34, LLR-4405.4, LLR-4405.12, LLR-4402.16, LLR-4409.5
in: Inbox self; str pad; DumpedEntry? record = None; DumpedEntry? drop = None
out: WriteResult result
func: INTERFACE, made exact. pad = strip_controls(pad) first (LLR-4409.5). Skip (written False, pad self.pad, union False, nothing read or locked) when pad == self.pad and record and drop are None and `_unsaved_flags` is empty. Else `_commit(change)` with change(base, changed): written = pad when not changed or base.pad == pad, else union_pads(base.pad, [e.text for e in base.dumped], pad); dumped = base.dumped minus every entry whose (task, board) equals drop's, plus record appended; flagged = base.flagged + each in-memory flag whose (task, board) base lacks, then only those whose text is a note text of `written`; divider_notice = base's or self's. After the write: `_hold(new)`, `_unsaved_flags` = [], `_stamped()`. Returns WriteResult(True, written, union = changed and written != pad). When written != pad for any reason (union or stripped controls) G-V replaces its text; the merge notice only when union (P-S-8 ruled ACCEPT; graph-interfaces WriteResult amended). Writes no file but `inbox.json` (+ its lock and temp)
module: taskboard/inbox.py
modify: [Data: inbox.json] (replace); [Data: Inbox state] (replace); [Data: Inbox._unsaved_flags] (clear)
examples: (TC-4600) pad "a\n________\n\nb  \n" on an unchanged file → the file's pad "a\n________\n\nb  \n" byte-identical, union `False`
examples: (TC-4446) pad "a\n______\nb" on an unchanged file → the file's pad "a\n______\nb", result pad "a\n______\nb"
examples: (TC-4581) no store in S, pad "x" → the file "S/inbox.json" exists `True`, pad "x"
examples: (TC-4582) pad "é\n____\nb" on a missing store → the file's text equals Inbox._shape's TC-4582 text byte for byte
examples: (TC-4584) Inbox X and Inbox Y loaded from one empty store; Y.write_pad("", record=e1) then X.write_pad("x") → the file's dumped holds e1 (`1` entry), pad "x", union `False`
examples: (TC-4599) the file changed by a second Inbox to pad "a\n____\nc" with dumped text "b"; this pad "a\n____\nb\n____\nd" → result pad "a\n____\nc\n____\nd", union `True`
examples: (TC-4544) dumped [e1, e2], drop e2 → the file's dumped [e1] (`1` entry), no entry with e2's task
examples: (TC-4552) the file holding an entry at "2026-10-24T10:00:00", pad "y", now 2026-11-01T10:02:00 → the file's dumped `[]`
examples: (TC-4589) a store loaded from "{not json" with keep_aside patched to `None`, pad "x" → OSError holding "was not written", the file bytes "{not json"
examples: (TC-4603) a held store lock, pad "x" → OSError "inbox.json is busy …", self.pad "" and self.dumped as before
examples: (TC-4606) Inbox.flag(entry with text "Volume lab fails on WSL"), then pad "Volume lab fails on WSL" → the file's flagged holds that text (`1` entry), its dumped `[]`
examples: (TC-4674) flagged entry text "b", pad "a" → the file has no "flagged" key; flagged entry text "b", pad "a\n____\nb" → flagged kept (`1`)
examples: (TC-4635) pad "a\x1bb\x9bc" → the file's pad "abc", result pad "abc"
examples: (TC-4598) pad equal to the stored pad, no record → result written `False`, store mtime unchanged
examples: (TC-4607) any successful write → every file in S other than inbox.json (2 board files, 2 history.jsonl, people.json, marks.json) keeps its sha256

Inbox.flag
req: LLR-4407.26
in: Inbox self; DumpedEntry entry
out: None
func: INTERFACE + input: accepts the DumpedEntry of `entry_for` (or a FlaggedEntry) and stores its FLAGGED projection (at, text, task, title, board, project) in `flagged` and in `_unsaved_flags` (finding P-S-15); an entry with the same (task, board) already flagged is not added twice
module: taskboard/inbox.py
modify: [Data: Inbox state] (append); [Data: Inbox._unsaved_flags] (append)
examples: (TC-4606) entry_for(the AT-4402 outcome) → flagged[0] keys ["at", "text", "task", "title", "board", "project"]; called twice → still `1` entry

Inbox.flag_for
req: LLR-4407.31, LLR-4407.32
in: Inbox self; str text
out: FlaggedEntry? entry
func: INTERFACE; first entry of `flagged` whose text == text (exact)
module: taskboard/inbox.py
examples: (TC-4672) after Inbox.flag(entry_for(the AT-4402 outcome)), text "Volume lab fails on WSL" → entry task "t0000001", board ends with "board.json" (G-V refuses alt+d with "This note is already on Course; delete it from the pad.")
examples: (TC-4671) text "Pilot stores" with only "Volume lab fails on WSL" flagged → entry `None`

Inbox.last_dump
req: LLR-4405.1, LLR-4405.7, LLR-4405.17
in: Inbox self; datetime now
out: DumpedEntry? entry
func: INTERFACE (P-S-6 ruled ACCEPT): "newest" = the last by list position (the store appends) of prune_dumped(entries, now), where entries = `_read(path)["dumped"]` read fresh at the call (no lock, no change to state or `_stamp`); the file missing, unreadable or over the cap (`_read` None or OSError) → the in-memory `dumped`
module: taskboard/inbox.py
examples: (TC-4541) dumped [e1 at "2026-11-01T10:00:00", e2 at "2026-11-01T10:01:00"], now 2026-11-01T10:02:00 → entry e2; after write_pad(drop=e2) → entry e1
examples: (TC-4547) dumped `[]` → entry `None`
examples: (TC-4557) memory [e1, e2]; a second Inbox wrote the file with dumped [e1] (e2 undone there) → entry e1; self.dumped still [e1, e2] and `_stamp` unchanged
examples: (TC-4557) memory [e1, e2]; the file made "{not json" → entry e2 (memory)

Inbox.mark_notice
req: LLR-4402.14
in: Inbox self
out: None
func: INTERFACE + stamp rule: the file's flag already true → divider_notice = True, no write. Else `_commit` with change(base, changed) = base with divider_notice True (pad = the FILE's pad, not the window's). After the write: divider_notice, dumped and flagged held; pad and `_stamp` held ONLY when changed is False — when another window had changed the file, the old stamp stays so the next write_pad unions with that window's pad instead of overwriting it (P-S-5 ruled ACCEPT)
module: taskboard/inbox.py
modify: [Data: inbox.json] (replace); [Data: Inbox state] (replace)
examples: (TC-4444) a store with pad "a\n____" → the file holds "divider_notice": `True` and pad "a\n____"
examples: (TC-4444) a second Inbox wrote pad "z" before mark_notice → the file's pad "z"; this window's next write_pad("a\n____\nb") → union `True`, pad "z\n____\na\n____\nb"

attach_images
req: LLR-4408.1, LLR-4408.2, LLR-4408.3, LLR-4408.5, LLR-4408.6, LLR-4408.7, LLR-4408.19
in: Path folder; object grabbed
out: AttachResult result
func: INTERFACE + rules. grabbed None, an empty list or any type that is neither a list nor a PIL image → notice "No image found in the clipboard.". A PIL image (`hasattr(grabbed, "mode")`) → `save_pil_image(folder, grabbed)` → names [dest.name]; any Exception → notice "The image could not be saved: <exc>". A list → candidates = items that are str, whose `Path(p).suffix.lower()` is in IMAGE_EXTS and `os.path.isfile(p)` (the user's own copied file; a link to a file is copied by content); none → "Clipboard holds no image files."; for each: base = Path(p).name, or "image" + suffix.lower() when `_image_ok(base)` fails; name = `_free_name(folder, base)`; `folder.mkdir(parents=True, exist_ok=True)`; `shutil.copy2(p, folder / name)`; an OSError stops the loop → AttachResult(names so far, "The image could not be saved: <exc>"). The source is only read
module: taskboard/inbox.py
modify: [I/O: inbox-images] (append)
examples: (TC-4611) grabbed a 2x2 PIL image, folder "S/inbox-images" empty → names ["paste-001.png"], the file "S/inbox-images/paste-001.png" exists
examples: (TC-4612) grabbed a PIL image, "paste-001.png" present → names ["paste-002.png"], paste-001.png bytes unchanged
examples: (TC-4613) grabbed ["U/shot.png"], "shot.png" in folder → names ["shot-2.png"]; "U/shot.png" still exists, sha256 equal to the copy's
examples: (TC-4615) grabbed `None` → names `[]`, notice "No image found in the clipboard."; grabbed `[]` → the same notice
examples: (TC-4616) grabbed ["U/a.txt", "U/b.svg"] (both exist) → names `[]`, notice "Clipboard holds no image files.", folder holds `0` files
examples: (TC-4617) shutil.copy2 patched to raise OSError("read-only") → names `[]`, notice "The image could not be saved: read-only"
examples: (TC-4629) grabbed ["U/con.png"] → names ["image.png"] (renamed by the name rule, P-S-10); the copy's sha256 equal to "U/con.png"'s, the source unchanged
examples: (TC-4629) grabbed ["U/con.png"] with "image.png" already in folder → names ["image-2.png"]

_free_name
req: LLR-4408.3, LLR-4408.16
in: Path folder; str name
out: str free
func: name when not `os.path.lexists(folder / name)` (a dangling symlink counts as taken: never written through); else the first `<stem>-<k><suffix>` for k = 2, 3, … that is free, stem/suffix by `os.path.splitext`. Bounded: at k > 9999 raises OSError "no free name for <name>"
module: taskboard/inbox.py
examples: (TC-4613) folder holding "shot.png" → free "shot-2.png"; holding "shot.png" and "shot-2.png" → "shot-3.png"
examples: (TC-4626) folder holding "paste-001.png", name "paste-001.png" → free "paste-001-2.png"

_file_stamp
req: LLR-4404.33, LLR-4405.2
in: Path path
out: tuple? stamp
func: (st_mtime_ns, st_size) of `os.stat(path)`, None on OSError; G-S's own copy of boards' private `_stamp` (no private import across modules)
module: taskboard/inbox.py
examples: (TC-4533) an existing board file of 812 bytes → stamp holds `812`

_new_task_id
req: LLR-4408.14
in: Board board
out: str id
func: up to `ID_TRIES` (20) times: tid = `models._new_id()` (through the module); return tid when `board.task_by_id(tid)` is None and not `os.path.lexists(board.image_dir(tid))`. 20 misses → OSError "no free task id"
module: taskboard/inbox.py
examples: (TC-4624) `_new_id` yields "t0000001" then "t0000002", "C/images/t0000001/" exists → id "t0000002"
examples: (TC-4624) `_new_id` yields "tc1" (a task of Course) then "t0000003" → id "t0000003"

_new_colour
req: LLR-4404.24
in: Board board
out: str colour
func: the first of `models.PROJECT_COLORS` that no project of the board (archived included) has as `color`; all 8 used → `PROJECT_COLORS[len(board.projects) % 8]`
module: taskboard/inbox.py
examples: (TC-4524) projects coloured "lime", "green" → colour "sky"
examples: (TC-4524) 9 projects using all 8 hues → colour "green"

_name_refusal
req: LLR-4404.25, LLR-4404.26
in: Board board; str name; str board_name
out: str? notice
func: the duplicate check of a new project's (already cleaned) name: a project of `board` (archived included) whose `name.strip().casefold()` equals `name.casefold()` → "<board_name> already has a project named <name>." (the submitted name as cleaned); else None. The empty-name check is done before any board is read (dump_note step 2)
module: taskboard/inbox.py
examples: (TC-4526) board Client A, name "eval HARNESS" → notice "Client A already has a project named eval HARNESS."
examples: (TC-4526) board Course, name "Eval harness" → notice `None`

_copy_images
req: LLR-4408.10, LLR-4408.11, LLR-4408.12, LLR-4408.13, LLR-4408.15
in: Path folder; list[str] names; Path dest_dir
out: tuple(list[str] moved, list[str] missing, list[str] paths)
func: for each name (already once each): src = folder / name; `os.lstat(src)` OSError or not `stat.S_ISREG` (a symlink, a folder) → missing. moved non-empty → `dest_dir.parent.mkdir(parents=True, exist_ok=True)` then `dest_dir.mkdir()` (exclusive: an existing folder raises); each `shutil.copy2(src, dest_dir / name)`; paths = `str((dest_dir / name).resolve())` in line order. Any OSError → `shutil.rmtree(dest_dir, ignore_errors=True)` (only a folder this call created) and re-raise. Nothing in `folder` changes here
module: taskboard/inbox.py
modify: [I/O: task images] (append)
examples: (TC-4620) F holding "paste-001.png" and "shot.png", names both, dest "C/images/t0000001" → moved both, missing `[]`, paths end with "t0000001\\paste-001.png" and "t0000001\\shot.png"; both still in F
examples: (TC-4622) names ["gone.png"] absent from F → moved `[]`, missing ["gone.png"], no "C/images/t0000001" folder
examples: (TC-4622) F holding a symlink "link.png" → missing ["link.png"] (not followed)
examples: (TC-4623) shutil.copy2 raising OSError("boom") on the 2nd name → OSError "boom", "C/images/t0000001" exists `False`

_drop_pad_copies
req: LLR-4408.10, LLR-4408.11
in: Path folder; list[str] names
out: None
func: after the board save only: `(folder / name).unlink()` for each moved name; an OSError (a viewer holds the file on Windows) is ignored — the board already holds its copy, so nothing is lost and the leftover is a plain file in F (finding P-S-12)
module: taskboard/inbox.py
modify: [I/O: inbox-images] (clear)
examples: (TC-4620) names ["paste-001.png", "shot.png"] → F holds neither

dump_note
req: HLR-4404, LLR-4404.1, LLR-4404.4, LLR-4404.5, LLR-4404.8, LLR-4404.9, LLR-4404.10, LLR-4404.11, LLR-4404.12, LLR-4404.13, LLR-4404.14, LLR-4404.15, LLR-4404.23, LLR-4404.24, LLR-4404.25, LLR-4404.26, LLR-4404.29, LLR-4404.31, LLR-4404.32, LLR-4404.33, LLR-4407.28, LLR-4408.10, LLR-4408.11, LLR-4408.12, LLR-4408.13, LLR-4408.14, LLR-4408.15
in: DumpTarget target; str? project_id; str? new_name; str note; Path folder; str project_name = ""
out: DumpOutcome outcome
func: INTERFACE, ordered. `project_name` (P-S-1 ruled ACCEPT; graph-interfaces amended) is used only for the LLR-4404.12 refusal. Both or neither of project_id / new_name → ValueError (a caller bug, not a refusal). (1) nt = note_task(note); nt.title == "" → refusal "This note has no text line for a title.". (2) new_name: clean = strip_controls(new_name).strip(); "" → "A project needs a name.". (3) `not target.path.exists()` → "<name>'s file is missing — nothing dumped." (before any lock, so no `.lock` and no file is created beside a missing board). (4) target.live set → `_dump_open`, else `_dump_other`. Every refusal: ok False, nothing written, `folder` unchanged. The task is `Task(title, project_id, phase = board.phases[0], notes, images = paths, id = _new_task_id(board))`, every other field at the Task default (priority "normal", no dates, not archived, urls [], depends_on [], milestone False, mark None). Other tasks are never touched: the board is re-serialized as Board.load read it (finding P-S-19). After ok: `_drop_pad_copies(folder, moved)`. Never writes the store, never touches the pad
module: taskboard/inbox.py
modify: [Data: board file] (replace); [Data: history.jsonl] (append); [I/O: inbox-images] (clear); [I/O: task images] (append)
examples: (TC-4501) target Course (live `None`), project_id "pm", note "Volume lab fails on WSL\nthe oracle script expects /mnt/c" → ok `True`; C's task ids ["tc1", "t0000001"]; the new task's project_id "pm"
examples: (TC-4529) note "img: a.png" → ok `False`, notice "This note has no text line for a title."; `0` files written
examples: (TC-4525) new_name "   " → ok `False`, notice "A project needs a name.", C's projects `1`; new_name "\x07\t" → the same notice
examples: (TC-4510) target path "S/gone/board.json" (missing) → ok `False`, notice "Course's file is missing — nothing dumped."; "S/gone/board.json" and "S/gone/board.json.lock" exist `False`
examples: (TC-4531) the TC-4501 dump → priority "normal", start_date `None`, due_date `None`, archived `False`, urls `[]`, depends_on `[]`, images `[]`
examples: (TC-4504) the TC-4501 dump and the TC-4508 dump → each `created` fullmatches "\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d", within [t0, t1] of the call
examples: (TC-4620) note "T\nimg: paste-001.png\nimg: shot.png" into Course → task.images the 2 resolved paths under "C/images/t0000001", in that order; outcome images ["paste-001.png", "shot.png"]; F holds neither; bytes equal
examples: (TC-4622) note "T\nimg: gone.png" → ok `True`, notes "img: gone.png", missing ["gone.png"], task.images `[]`
examples: (TC-4625) note "T\nimg: a.png\nimg: a.png" → task.images `1` path; "a.png" copied once
examples: (AT-4402) note "Volume lab fails on WSL\nthe oracle script expects /mnt/c\nimg: board-0938.png", project "pm" → title "Volume lab fails on WSL", notes "the oracle script expects /mnt/c", the image in "C/images/t0000001"

_dump_open
req: LLR-4404.8, LLR-4404.4, LLR-4404.11, LLR-4404.12, LLR-4404.14, LLR-4404.15, LLR-4404.23, LLR-4404.26, LLR-4408.11, LLR-4408.13
in: DumpTarget target; NoteTask nt; str? project_id; str? clean_name; str project_name; Path folder
out: DumpOutcome outcome
func: the open board, through `live = target.live` and the app's save path (R0-8, S-a: no lock, no stamp). `live.load_report.get("file_unreadable")` → "<name>'s file cannot be read — nothing dumped." (P-S-9 ruled ACCEPT: both checks on both paths). project_id not on live → "<project_name> is no longer on <name> — nothing dumped."; clean_name taken (`_name_refusal`) → that notice. tid = `_new_task_id(live)`; moved, missing, paths = `_copy_images(folder, nt.images, live.image_dir(tid))` (OSError → "An image could not be moved: <exc> — nothing dumped."); title, notes = `_task_fields(note, moved)`; new project → `Project(clean_name, color=_new_colour(live))` appended to `live.projects` (NOT add_project: one save, LLR-4404.23); `live.add_task(task)` (stamps created, writes the birth record, one `save()`). OSError from it → `live.tasks.remove(task)` when present, the new project removed, `shutil.rmtree(live.image_dir(tid), ignore_errors=True)`, → "<name> could not be saved: <exc> — nothing dumped." (LLR-4404.15; the birth line add_task wrote before its save stays: recorded risk F-2)
module: taskboard/inbox.py
modify: [Data: Board.tasks] (append); [Data: Board.projects] (append); [Data: board file] (replace); [Data: history.jsonl] (append)
examples: (TC-4508) target Client A (live app.board), project_id "pe", note "Golden set answer key" → ok `True`; live.tasks[-1].id "t0000001"; A's file holds "t0000001"
examples: (TC-4523) target Client A, new_name "Contracts pilot" → live.projects[-1] name "Contracts pilot", colour "sky", the task's project_id equals its id; `Board.save` called `1` time (spy), `Board.add_project` `0` times
examples: (TC-4515) `Board.save` patched to raise OSError("disk full"), new_name "Contracts pilot" → ok `False`, notice "Client A could not be saved: disk full — nothing dumped."; len(live.tasks) and len(live.projects) as before; "A/images/t0000001" exists `False`
examples: (TC-4532) the TC-4508 dump → A's history.jsonl gains exactly `1` line with task "t0000001", from `None`, to "Backlog", at equal to the task's created
examples: (TC-4505) target Client A → phase "Backlog" (A's first phase)

_dump_other
req: LLR-4404.9, LLR-4404.4, LLR-4404.5, LLR-4404.10, LLR-4404.11, LLR-4404.12, LLR-4404.13, LLR-4404.14, LLR-4404.23, LLR-4404.26, LLR-4404.32, LLR-4404.33, LLR-4407.28, LLR-4408.11, LLR-4408.13
in: DumpTarget target; NoteTask nt; str? project_id; str? clean_name; str project_name; Path folder
out: DumpOutcome outcome
func: move_project's pattern (R1-3), in this order: `with file_lock(target.path, target.name)` (OSError → its text as the notice, LLR-4404.13); inside: path missing → missing notice; s0 = `_file_stamp(path)`; fresh = `peek_board(path)` (OSError → unreadable notice); s1 = `_file_stamp(path)`; `fresh.load_report.get("file_unreadable")` → "<name>'s file cannot be read — nothing dumped."; s1 != s0 → "<name> changed while dumping — nothing dumped."; project gone → "<project_name> is no longer on <name> — nothing dumped."; name taken → `_name_refusal`; now = datetime.now(); tid = `_new_task_id(fresh)`; `_copy_images` into `fresh.image_dir(tid)` (OSError → the image notice); task with created = `models.stamp(now)`, phase fresh.phases[0]; new project appended to fresh.projects; task appended to fresh.tasks; `_file_stamp(path)` != s0 → rmtree the copies, the changed notice (LLR-4404.33); `fresh.save_atomic()` (OSError → rmtree the copies, "<name> could not be saved: <exc> — nothing dumped."); then `history.append(path, {"task": tid, "from": None, "to": phase}, at=now)` (a None return is not a failure: the board is saved); lock released. Never `Board.save`, never `add_task` (its plain save)
module: taskboard/inbox.py
modify: [Data: board file] (replace); [Data: history.jsonl] (append); [I/O: board.json.lock] (replace)
examples: (TC-4509) target Course → at the save "C/board.json.lock" exists `True` (spy on save_atomic); `Board.save_atomic` called `1` time and `Board.save` `0` times
examples: (TC-4509) a task "tw1" appended to C's file by another writer after the view opened → after the dump C's task ids ["tc1", "tw1", "t0000001"]
examples: (TC-4511) C's file "{not json" → ok `False`, notice "Course's file cannot be read — nothing dumped."; C's bytes unchanged; no "C/board.json.corrupt"
examples: (TC-4512) project "pm" removed from C's file after the view opened, project_name "Module 4 · Volumes" → ok `False`, notice "Module 4 · Volumes is no longer on Course — nothing dumped."; C's bytes unchanged
examples: (TC-4513) a fresh foreign "C/board.json.lock" → ok `False`, notice holds "Course is busy"; C's bytes unchanged; F unchanged
examples: (TC-4514) C's file read-only → ok `False`, notice starts "Course could not be saved: [Errno 13] Permission denied" and ends " — nothing dumped."
examples: (TC-4533) peek_board wrapped to append a task "tx1" to C's file right after its read (a lock-ignoring writer) → ok `False`, notice "Course changed while dumping — nothing dumped."; C's bytes equal that writer's
examples: (TC-4523) new_name "Contracts pilot" into Course → C's projects ["pm", <new id>] with the new one coloured "lime", the task's project_id = <new id>; `save_atomic` called `1` time
examples: (TC-4524) the TC-4523 dump → the new project's color "lime" (Course uses only "sky")
examples: (TC-4505) target Course → phase "Todo"
examples: (TC-4532) the TC-4501 dump → C's history.jsonl gains exactly `1` line {"task": "t0000001", "from": null, "to": "Todo", "at": <created>}, appended after save_atomic returned (spy order)
examples: (TC-4608) C saved by the app with tasks "tc1" and "tc2" without created → after the dump each one's `json.dumps(entry, indent=2)` slice is byte-equal
examples: (TC-4621) save_atomic patched to raise OSError, note with 2 images → both still in F; "C/images/t0000001" exists `False`
examples: (TC-4623) shutil.copy2 failing on the 2nd image → ok `False`, notice "An image could not be moved: boom — nothing dumped."; C's bytes unchanged; F unchanged
examples: (TC-4624) "C/images/t0000001/x.png" present before the dump → task id "t0000002"; "C/images/t0000001/x.png" unchanged

undo_dump
req: HLR-4405, LLR-4405.2, LLR-4405.5, LLR-4405.6, LLR-4405.8, LLR-4405.10, LLR-4405.11, LLR-4408.16, LLR-4408.17
in: DumpedEntry entry; Board? live; Path folder
out: UndoOutcome outcome
func: INTERFACE, ordered. The entry is shaped (`Inbox._entry`): its task id fullmatches ID_RE and its image names pass `_image_ok`. title, notes = `_task_fields(entry.text, moved = set(entry.images))` — the task as its dump wrote it (P-S-2 ruled ACCEPT; graph-interfaces amended). G-V calls undo_dump only when `entry.board` is samefile with a lane of `board_lanes` (P-S-4 ruled, LLR-4405.16: G-V's refusal otherwise). live set → `_undo_open`, else `_undo_other`. State "undone" → `_images_back`, then `os.rmdir(board.image_dir(entry.task))` (OSError ignored: a folder that still holds other files stays, LLR-4408.17); note_text = `_renamed(entry.text, renames)`. States "gone" and "changed" change no file (images stay where they are; the restored lines may name files not in F: finding P-S-12); note_text = entry.text. "failed": notice = the error text only; G-V words "<board> could not be changed: <error> — nothing undone."
module: taskboard/inbox.py
modify: [Data: board file] (replace); [I/O: inbox-images] (append); [I/O: task images] (clear)
examples: (TC-4542) entry of the TC-4501 dump, live `None` → state "undone"; C's file holds no "t0000001"
examples: (TC-4542) entry of the TC-4508 dump, live app.board → state "undone"; A's file and app.board hold no "t0000001"
examples: (TC-4545) entry new_project `True`, project "pX", no other task in "pX" → C's projects lack "pX"
examples: (TC-4546) entry new_project `True`, project "pX", task "tc2" also in "pX" → "pX" kept; tc2's project_id "pX"
examples: (TC-4548) task "t0000001" deleted from C after the dump → state "gone", note_text equal to entry.text; C's bytes unchanged
examples: (TC-4550) the task's title edited to "Volume lab fixed" → state "changed"; C's bytes unchanged
examples: (TC-4622) entry text "T\nx\nimg: gone.png", images `[]`, the task's notes "x\nimg: gone.png" → state "undone" (not "changed")
examples: (TC-4551) a fresh foreign "C/board.json.lock" → state "failed", notice holds "Course is busy"; C's bytes unchanged
examples: (TC-4626) entry images ["paste-001.png"], F already holding "paste-001.png" → "F/paste-001-2.png" bytes equal the board copy; note_text holds "img: paste-001-2.png"
examples: (TC-4627) the TC-4626 undo → "C/images/t0000001" exists `False`

_undo_open
req: LLR-4405.2, LLR-4405.5, LLR-4405.6, LLR-4405.8, LLR-4405.10, LLR-4405.11
in: DumpedEntry entry; Board live; str title; str notes
out: UndoOutcome outcome
func: task = live.task_by_id(entry.task); None → "gone". task.title != title or task.notes != notes → "changed". Else i = index; `live.tasks.pop(i)`; when entry.new_project and no task of live has project_id entry.project → that project popped (its index kept); `live.save()` (the app's save path, LLR-4405.2); OSError → task and project re-inserted at their indexes, state "failed", notice str(exc). `_undo_stack` is never read or written here (LLR-4405.14 is G-V's)
module: taskboard/inbox.py
modify: [Data: Board.tasks] (replace); [Data: Board.projects] (replace); [Data: board file] (replace)
examples: (TC-4551) `Board.save` patched to raise OSError("disk full") → state "failed", notice "disk full"; live.tasks still holds "t0000001" at its index

_undo_other
req: LLR-4405.2, LLR-4405.5, LLR-4405.6, LLR-4405.8, LLR-4405.10, LLR-4405.11
in: DumpedEntry entry; str title; str notes
out: UndoOutcome outcome
func: path = Path(entry.board); missing → "failed", notice "its file is missing" (before any lock; a missing board blocks older undos: finding P-S-17). `with file_lock(path, Path(path).parent.name)` (OSError → "failed", its text); s0, fresh = peek_board, s1; unreadable → "failed" "its file cannot be read"; s1 != s0 → "failed" "it changed while it was read"; then the same gone / changed / remove steps as `_undo_open` on `fresh`; `_file_stamp` != s0 → "failed" "it changed while undoing"; `fresh.save_atomic()` (OSError → "failed", str(exc)); no history line is written
module: taskboard/inbox.py
modify: [Data: board file] (replace); [I/O: board.json.lock] (replace)
examples: (TC-4542) a task "tw1" another writer appended to C's file after the dump → after the undo C's task ids ["tc1", "tw1"]
examples: (TC-4551) entry board "S/gone/board.json" (missing) → state "failed", notice "its file is missing"

_images_back
req: LLR-4408.16
in: Path src_dir; Path folder; list[str] names
out: dict[str, str] renames
func: after the board save. `folder.mkdir(parents=True, exist_ok=True)`; for each name: src = src_dir / name; `os.lstat` not a regular file → skipped (its line keeps its name); free = `_free_name(folder, name)`; `shutil.copy2(src, folder / free)` then `src.unlink()` (copy then remove: the board and the store may sit on two drives, where `os.replace` fails); an OSError stops the loop (the file stays in the board; silent, finding P-S-12). renames[name] = free for every moved file
module: taskboard/inbox.py
modify: [I/O: inbox-images] (append); [I/O: task images] (clear)
examples: (TC-4626) names ["paste-001.png"], F holding "paste-001.png" → renames "paste-001.png": "paste-001-2.png"; "C/images/t0000001/paste-001.png" exists `False`

_renamed
req: LLR-4408.16
in: str text; dict[str, str] renames
out: str text
func: each line whose `image_name` is a key of `renames` with a different value becomes "img: <new>"; every other line byte-identical
module: taskboard/inbox.py
examples: (TC-4626) text "T\nimg: paste-001.png", renames "paste-001.png": "paste-001-2.png" → text "T\nimg: paste-001-2.png"

## Entities

[Data: inbox constants]
in: module constants
desc: `INBOX_NAME = "inbox.json"`, `IMAGES_NAME = "inbox-images"`, `KEEP_DAYS = 7`, `KEEP_SECONDS = 604_800`, `STORE_MAX_BYTES = 8_388_608`, `IMAGE_NAME_MAX = 128`, `ID_TRIES = 20`, `DIVIDER_RE = re.compile("_{4,}")`, `STAMP_RE = re.compile(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d")`, `ID_RE = re.compile(r"[A-Za-z0-9_-]{1,64}")`, `DUMPED` and `FLAGGED` field tuples. `SUGGEST_CHARS` is NOT here (P-S-13 ruled as P-T-1: the cap is `suggest.NOTE_CHARS`)

[Data: Inbox._stamp]
in: tuple[int, int]?
desc: the store stamp (st_mtime_ns, st_size) as of this Inbox's last read or write; None when the file did not exist then. `_commit` compares it with the file's stamp under the lock to decide verbatim vs union

[Data: Inbox._unsaved_flags]
in: list[FlaggedEntry]
desc: flags made by `Inbox.flag` since the last successful write; kept across `refresh`, cleared by a successful `write_pad` (P-S-7)

[I/O: inbox.json.lock]
desc: `S/inbox.json.lock`, boards.file_lock's lock for the store (label "inbox.json")

[I/O: inbox.json.corrupt]
desc: `keep_aside`'s byte copy of an unreadable store (`.corrupt`, `.corrupt-2`, …); never made for a store over STORE_MAX_BYTES

[I/O: board.json.lock]
desc: the lock of another board's file, held by `_dump_other` and `_undo_other` from the existence check to the save (label = the board's display name)

[Data: Board.tasks]
in: list[Task]
desc: the open board's live list (`target.live` / `live`), changed only by `_dump_open` (through `add_task`) and `_undo_open`, and rolled back by them on a failed save

[Data: Board.projects]
in: list[Project]
desc: as [Data: Board.tasks]; a new project is appended directly (never `add_project`, which saves on its own)

## Edges

_image_ok ──▶ image_name
_image_ok ──▶ attach_images
_image_ok ──▶ Inbox._entry
image_name ──▶ _title_row
image_name ──▶ _task_fields
image_name ──▶ _renamed
_title_row ──▶ _task_fields
_task_fields ──▶ note_task
_task_fields ──▶ _dump_open
_task_fields ──▶ _dump_other
_task_fields ──▶ undo_dump
is_divider ──▶ without_note
is_divider ──▶ with_note
note_parts ──▶ union_pads
note_parts ──▶ Inbox.write_pad
Inbox._entry ──▶ Inbox._read
Inbox._too_big ──▶ Inbox.load
Inbox._too_big ──▶ Inbox._set_aside
Inbox._read ──▶ Inbox.load
Inbox._read ──▶ Inbox.refresh
Inbox._read ──▶ Inbox._commit
Inbox._set_aside ──▶ Inbox._commit
Inbox._shape ──▶ Inbox._commit
prune_dumped ──▶ Inbox._commit
Inbox._commit ──▶ Inbox.write_pad
Inbox._commit ──▶ Inbox.mark_notice
Inbox._commit ──▶ [Data: inbox.json]
Inbox._commit ──▶ [I/O: inbox.json.lock]
Inbox.load ──▶ [I/O: inbox.json.corrupt]
Inbox._set_aside ──▶ [I/O: inbox.json.corrupt]
Inbox._stamped ──▶ [Data: Inbox._stamp]
[Data: Inbox._stamp] ──▶ Inbox._commit
[Data: Inbox._stamp] ──▶ Inbox.refresh
Inbox.flag ──▶ [Data: Inbox._unsaved_flags]
[Data: Inbox._unsaved_flags] ──▶ Inbox.refresh
[Data: Inbox._unsaved_flags] ──▶ Inbox.write_pad
Inbox.write_pad ──▶ [Data: Inbox._unsaved_flags]
entry_for ──▶ Inbox.write_pad
entry_for ──▶ Inbox.flag
[Data: inbox constants] ──▶ Inbox._read
[Data: inbox constants] ──▶ prune_dumped
[Data: inbox constants] ──▶ is_divider
_free_name ──▶ attach_images
_free_name ──▶ _images_back
_file_stamp ──▶ _dump_other
_file_stamp ──▶ _undo_other
_new_task_id ──▶ _dump_open
_new_task_id ──▶ _dump_other
_new_colour ──▶ _dump_open
_new_colour ──▶ _dump_other
_name_refusal ──▶ _dump_open
_name_refusal ──▶ _dump_other
_copy_images ──▶ _dump_open
_copy_images ──▶ _dump_other
_copy_images ──▶ [I/O: task images]
_dump_open ──▶ dump_note
_dump_other ──▶ dump_note
_drop_pad_copies ──▶ [I/O: inbox-images]
dump_note ──▶ _drop_pad_copies
_dump_open ──▶ [Data: Board.tasks]
_dump_open ──▶ [Data: Board.projects]
_dump_open ──▶ [Data: board file]
_dump_open ──▶ [Data: history.jsonl]
_dump_other ──▶ [I/O: board.json.lock]
_dump_other ──▶ [Data: board file]
_dump_other ──▶ [Data: history.jsonl]
[Data: board file] ──▶ _dump_other
[Data: board file] ──▶ _undo_other
[I/O: inbox-images] ──▶ _copy_images
_undo_open ──▶ undo_dump
_undo_other ──▶ undo_dump
_undo_open ──▶ [Data: Board.tasks]
_undo_open ──▶ [Data: board file]
_undo_other ──▶ [I/O: board.json.lock]
_undo_other ──▶ [Data: board file]
_images_back ──▶ undo_dump
_images_back ──▶ [I/O: inbox-images]
_renamed ──▶ undo_dump
[I/O: task images] ──▶ _images_back

## Findings

finding P-S-1 dump_note cannot word LLR-4404.12's refusal: it has no project name
anchor: dump_note
seen: LLR-4404.12 shows "<project> is no longer on <board> — nothing dumped." when the project is gone from the fresh board; graph-interfaces' dump_note gets only `project_id`, and the fresh board no longer holds the project, so its name is nowhere in G-S's inputs (TC-4512)
effect: the refusal would show an id ("pm is no longer on Course") or G-V would have to re-word a notice G-S composes
decision: ruled — ACCEPT (round 0b): `dump_note(..., project_name: str = "")`, used only for the LLR-4404.12 notice; graph-interfaces amended. Applied: dump_note

finding P-S-2 the undo's "changed" check misreads a dump that had a missing image (MAJOR)
anchor: undo_dump
seen: graph-interfaces says "Title or notes differ from note_task(entry.text) → changed". LLR-4408.12 keeps a missing image's line in the task's notes, but note_task drops every image line, so for entry text "T\nx\nimg: gone.png" the task holds notes "x\nimg: gone.png" while note_task gives "x"
effect: every undo of a dump that reported "1 image(s) not found" is refused with "changed since the dump — undo left it." although nothing was edited (TC-4622 vs TC-4550)
decision: ruled — ACCEPT (MAJOR, round 0b): undo's changed-check uses `_task_fields(entry.text, moved=set(entry.images))`; graph-interfaces undo_dump amended. Applied: undo_dump, TC-4622 arm

finding P-S-3 no requirement caps the store's size; LLR-4407.8 has no wording for "no copy" (MAJOR)
anchor: Inbox.load
seen: HLR-4407 names the store untrusted but no LLR caps it. `Directory._read` and `keep_aside` (boards.py:69) both `read_bytes()` the whole file, so a 4 GB `inbox.json` is read into memory at every load, refresh and write; a pad pasted large enough would make a store the next load cannot hold. LLR-4407.8's notice has only "it was copied to <backup name>", but `keep_aside` can return None (people/marks already word that case: "no copy could be kept", app.py:1594)
effect: unbounded memory at app start on a hostile or runaway store; a notice with "None" in it
decision: ruled — ACCEPT (MAJOR, round 0b): `STORE_MAX_BYTES = 8 388 608`; an over-cap store read = unreadable, not copied aside, never written over; an over-cap write raises the worded OSError and changes nothing. New LLR-4407.35 (TC-4675), LLR-4407.36 (TC-4676), LLR-4407.37 (TC-4677); the backup-None notice takes P-V-6's wording as LLR-4407.38 (TC-4678), LLR-4407.8 now covers the copied case only. Applied: Inbox._read, Inbox._too_big, Inbox.load, Inbox._commit

finding P-S-4 a store entry's `task` and `images` form file paths (MAJOR, security)
anchor: Inbox._entry
seen: undo moves files from `Board.image_dir(entry.task) / name` into F for each name of `entry.images`; both come from `inbox.json`, which any process of the user can write. LLR-4407.10 checks only "a field of its type". `task` "../../x" or images ["..\\..\\a.png"] would move files from outside `images/<id>/` into F (and F names from outside F). `entry.board` names the board file undo reads, locks and `save_atomic`s
effect: path traversal on undo; a crafted entry could also make undo rewrite any board-shaped JSON file
decision: ruled — ACCEPT (MAJOR, security, round 0b): entry validation (`task` fullmatches `[A-Za-z0-9_-]{1,64}`, images pass the name rule, text non-blank, `new_project` a bool) — LLR-4407.10 reworded; undo only when `entry.board` is samefile with a lane of `board_lanes`, else the worded notice and the entry kept — new LLR-4405.16 (G-V's CaptureView.action_undo, TC-4556). Applied: Inbox._entry, undo_dump

finding P-S-5 mark_notice must not adopt another window's stamp (MAJOR, data loss)
anchor: Inbox.mark_notice
seen: graph-interfaces' mark_notice writes "the pad as the file holds it" and then, as `_commit` does, holds the state and takes the stamp. If another window had changed the pad, this window's in-memory stamp would then equal the file's, and its next write_pad would see "unchanged" and write its own pad verbatim over the other window's notes
effect: R2 F-8 ("no note text is ever dropped silently") broken by the first divider of a session
decision: ruled — ACCEPT (MAJOR, round 0b): `mark_notice` holds pad/stamp only when the file was unchanged before it. Applied: Inbox.mark_notice (TC-4444 arm 2)

finding P-S-6 alt+u reads the in-memory `dumped`, which another window may have undone already
anchor: Inbox.last_dump
seen: the store is re-read only when the capture view opens (LLR-4407.13). Window 2 undoes entry e (note restored there, entry dropped from the file); window 1's memory still holds e; window 1's `alt+u` → undo_dump finds the task gone → state "gone" → the note is restored a second time
effect: a duplicate NOTE in the merged pad (no duplicate task: the second undo changes no board)
decision: ruled — ACCEPT the fresh read (round 0b): `last_dump` reads the file's `dumped` fresh (no state/stamp change; unparseable → memory); graph-interfaces amended; new LLR-4405.17 (TC-4557). Applied: Inbox.last_dump

finding P-S-7 a refresh drops a flag that has not been written yet (MAJOR, duplicate task)
anchor: Inbox.refresh
seen: Inbox.flag only changes memory ("the next write_pad writes it"). graph-interfaces' refresh replaces the state on a changed file. Dump ok → write_pad fails → flag → `esc` twice (LLR-4407.25) → reopen after another window wrote the store → refresh replaces `flagged` with the file's (without the flag)
effect: the note is in the pad unflagged and `alt+d` dumps it again: the duplicate task LLR-4407.32 exists to prevent
decision: ruled — ACCEPT (MAJOR, round 0b): `_unsaved_flags` survive refresh until a write succeeds. Applied: Inbox.refresh, Inbox.write_pad (TC-4606 arm)

finding P-S-8 WriteResult tells G-V to replace its text only on a union
anchor: Inbox.write_pad
seen: write_pad strips control characters (LLR-4409.5) before writing, so the written pad can differ from the window's text with union False; the interface entity says "union True → G-V replaces the pad text"
effect: the window keeps the control byte while the store does not; the next write sees pad != self.pad and writes again on every debounce
decision: ruled — ACCEPT (round 0b): G-V replaces its text whenever `result.written and result.pad != text`; merge notice only when `union`; graph-interfaces WriteResult amended. Applied: Inbox.write_pad; G-V CaptureView._flush / _dump / action_undo

finding P-S-9 LLR-4404.10 and LLR-4404.11 applied to the open board too
anchor: _dump_open
seen: the two LLRs say "the target board's file" without excluding the open board; the open board's live object exists even when its file was deleted or loaded as unreadable (Board.load quarantines and shows an empty board)
effect: without the checks a dump would re-create a deleted file or overwrite a quarantined one from the empty live board
decision: ruled — ACCEPT (round 0b): both checks on both paths. Applied: _dump_open, _dump_other

finding P-S-10 the image-name rule needs more than LLR-4408.18 lists
anchor: _image_ok
seen: §1's definition of "image line" also bars control characters, LLR-4408.18 does not. Windows opens `con.png`, `nul.png` as devices on many builds; names with trailing spaces or dots are rewritten by Win32; a 10 000-character name fails at the file system with an OSError mid-copy. Explorer-copied files may carry a name that fails the rule (attach must still produce a readable line)
effect: an attach whose line the dump can never read, or a device opened instead of a file
decision: ruled — ACCEPT (round 0b): image-name rule widened (no control chars, no surrounding whitespace, ≤ 128 chars, no Windows device stem) — LLR-4408.18 reworded and the rule defined in requirements §1; a failing source name saves as `image<suffix>` — new LLR-4408.19 (TC-4629). Applied: _image_ok, image_name, attach_images

finding P-S-11 residual link races on the attach paths (accepted risk)
anchor: attach_images
seen: `_free_name` uses `lexists`, so a planted dangling symlink is "taken", but `shutil.copy2` opens the chosen name with "wb", which follows a link created between the check and the open; `models.save_pil_image` (unchanged on purpose) uses `exists()`, which is False for a dangling link, and then saves through it; `inbox-images` itself may be a link or junction
effect: a process of the same user that can write `~/.taskboard/` can redirect one pasted image's bytes to another path of that user
decision: ruled — ACCEPT as recorded risk (BACKLOG, round 0b); no node change

finding P-S-12 silent leftovers on the image paths
anchor: _images_back
seen: a pad copy that cannot be removed after the dump's save (`_drop_pad_copies`), a file that cannot be moved back on undo (`_images_back`), and the "gone" undo (images left in the board folder, LLR-4405.8 "without changing any board") have no notice in any LLR; DumpOutcome and UndoOutcome have no field for them
effect: nothing is lost (each file still exists once), but a restored `img:` line can name a file not in F, which the next dump reports as "not found"
decision: ruled — ACCEPT (round 0b); BACKLOG item (UndoOutcome `left` list); no node change

finding P-S-13 SUGGEST_CHARS belongs to suggest.py
anchor: Inbox._read
seen: §6 slice row 1 lists `SUGGEST_CHARS` among inbox.py's constants, but the 10 000-character cap is applied by G-T's `suggest` (graph-interfaces), and G-T never imports inbox
effect: a constant defined where nothing uses it, or an import G-T may not make
decision: ruled — same as P-T-1 (round 0b): suggest.py `NOTE_CHARS`; inbox.py defines no SUGGEST_CHARS (requirements §6 row 1 amended). Applied: [Data: inbox constants]

finding P-S-14 with_note on a pad ending in blank lines or in a divider
anchor: with_note
seen: LLR-4405.3 gives "a" → "a\n____\n<text>" and "" → "<text>" only; a pad "a\n" or "a\n____\n" (the note being started) would give "a\n\n____\nb" or an empty part "a\n____\n\n____\nb"
effect: stray blank lines and empty parts after each undo
decision: ruled — ACCEPT (round 0b). Applied: with_note (TC-4543 arms)

finding P-S-15 who builds the dumped and flagged entries
anchor: entry_for
seen: graph-interfaces passes `record=entry` to write_pad and a FlaggedEntry to Inbox.flag but names no builder; LLR-4407.3 / LLR-4407.33 fix key order and types
effect: G-V would build store records whose shape G-S then has to trust
decision: ruled — ACCEPT (round 0b): public `entry_for(outcome, note, board_path, now)` in inbox.py; graph-interfaces amended (node entry_for). Applied: entry_for, Inbox.flag; G-V CaptureView._dump calls it

finding P-S-17 an undo whose board is missing blocks every older undo
anchor: _undo_other
seen: LLR-4405.11 makes a read failure "nothing undone" with the entry kept; alt+u always takes the newest entry, so a board on an offline drive keeps answering "could not be changed" for up to 7 days
effect: older dumps cannot be undone meanwhile
decision: ruled — ACCEPT as recorded risk (round 0b); no node change

finding P-S-19 a dump re-serializes the target board as Board.load read it
anchor: _dump_other
seen: probe `%TEMP%/incK-probe-S/p2.py`: a board whose task "tc1" had phase "Backlog" not in its phases ["Todo", "Doing", "Done"] → peek_board snaps it to "Todo" and save_atomic writes "phase": "Todo" for tc1 (diff printed by the probe)
effect: LLR-4407.28 ("every other task's entry exactly as it was") holds only for a board the current serializer wrote; any load normalization (phase snap, rescue) is written by the dump, as by any save of the app
decision: ruled — ACCEPT (round 0b): LLR-4407.28 reads "a board saved by this version"; normalisation is existing behaviour. Applied: _dump_other TC-4608 example (fixture built with `Board.save`)

finding P-S-21 a target project archived after the view opened still receives the dump
anchor: _dump_other
seen: documents hold only non-archived projects (LLR-4403.3), but no LLR says what a dump does when its project was archived between the suggestion and `alt+d`
effect: the task lands in an archived project and is hidden on the board
decision: ruled — ACCEPT (round 0b): no archived check (prefer simpler); LLR-4404.12 unchanged; no node change

### Seams
> Called by G-V into G-S: `is_divider` (PadArea's rule); `note_parts`, `note_count`, `note_at` (head row, rail, cursor's note, review rows); `note_task(text).title` (rail title, review row); the rail's `▣ n` counts image LINES `sum(image_name(l) is not None for l in text.split("\n"))`, not `note_task(text).images` (deduplicated); `without_note` and `with_note` (pad edits after dump / undo; in a batch, G-V re-finds each note's Part by its text after every removal); `prune_dumped(inbox.dumped, now)` (the rail's `✓ dumped <n>` line, LLR-4405.13); `Inbox.load` (TaskboardApp.__init__, path `registry.path.parent / INBOX_NAME`), `Inbox.refresh` (capture view open), `Inbox.write_pad` (debounce, close, exit, dump with `record=entry_for(...)`, undo with `drop=entry`, attach), `Inbox.flag(entry_for(...))` when write_pad raises after an ok dump, `Inbox.flag_for` (rail flag line, alt+d / review refusal), `Inbox.last_dump(now)`, `Inbox.mark_notice` (first rule drawn); `attach_images(inbox.images_dir, grab_clipboard_image())`; `dump_note(DumpTarget(...), project_id, new_name, note, inbox.images_dir, project_name)` (P-S-1); `entry_for(outcome, part.text, board_path, now)` for the `record` and the flag (P-S-15); `undo_dump(entry, live, inbox.images_dir)` only for an entry whose `board` is a lane's file (P-S-4); `note_task(text)` also gives G-V the scored text `title + "\n" + notes` it passes to suggest (P-T-4).
> Notices G-V words from G-S values: LLR-4407.8 from `load_report` (`Path(backup).name`), LLR-4407.38 for backup None (P-V-6 wording); LLR-4407.37 and LLR-4407.23 from write_pad's OSError text; LLR-4407.14 from `refresh() is False`; LLR-4407.23 / LLR-4407.30 from write_pad's OSError text; LLR-4405.9 from `entry.title` and the board's display name; LLR-4405.11 from UndoOutcome.notice; LLR-4408.12 from DumpOutcome.missing. DumpOutcome.notice is already the full refusal text (LLR-4404.10..4404.14, .25, .26, .29, .33, LLR-4408.13); G-V shows it as is, `markup=False`.
> Called by G-S into other modules (unchanged on purpose): `boards.file_lock`, `boards.keep_aside`, `boards.peek_board`; `models.write_atomic`, `Board.save_atomic`, `Board.add_task`, `Board.save`, `Board.image_dir`, `Board.task_by_id`, `Board.project_by_id`, `models.stamp`, `models._new_id`, `models.save_pil_image`, `models.strip_controls`, `models.clean_strings`, `models.IMAGE_EXTS`, `models.PROJECT_COLORS`; `history.append`; `modals.visible_text`. G-S imports neither `app` nor `suggest`.
> Nothing from G-T is called by G-S.
