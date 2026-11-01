# Code-Wire prototype — group D (models.py, keymap.py) — Inc L

Differences from `graph-baseline.cw.md` (eb411e1) only. Group D owns `Task.created` and its persistence (models.py) and the `N` seat entry (keymap.py), plus the README key row. Changed code: 5 nodes (`Task`, `Task.from_dict`, `Board._to_dict`, `Board._serialized`, `Board.load`) and 2 entities (`[Data: models._TASK_KEYS]`, `[Data: keymap.KEYMAP]`). Unchanged code, now traced with `created` / `N` examples: 8 nodes (`_rescue_task`, `seed_data`, `Board.save`, `TeamState.push`, `move_project`, `app_bindings`, `global_keys`, `palette_commands`). `stamp` and `Board.add_task` are defined in `graph-interfaces.cw.md` and are not repeated here; this file cites them and proposes one refinement of `Board.add_task` (P-D-4).

How the examples were checked: a scratch copy of `taskboard/` outside the repo (`%TEMP%/incLD/ref`, `taskboard.__file__` printed = that copy) with exactly the design below applied to models.py. Every example of this file was run there (state `executed`) unless it says `planned`. The guard suites of baseline-notes.md plus test_app.py, test_team_sync.py, test_milestones.py, test_help_keys.py and test_keymap.py were run against that copy: 780 passed, 1 skipped, 1 failed (`test_every_image_the_readme_shows_exists`: the copy holds no `docs/` folder — environment, not design). The `N` seat entry was checked by patching `keymap.KEYMAP` in a pytest plugin against the worktree's own code (tests/test_help_keys.py: 9 passed). Nothing in `taskboard/` or `tests/` of the worktree was edited.

E3 round-1 corrections (03-pdr-rulings round 1: SEC-1, ARCH-2; findings at the end): `Board._to_dict` gains `with_created`, `Board._serialized` becomes a changed node and `TeamState.push` (team_sync.py, code unchanged) is traced. These corrections were NOT run on the scratch copy: every example that names `with_created`, `_serialized`, `TeamState.push`, TC-4318 or TC-4316's birth record is state `planned` (first execution: the E4 tester's RED-on-base run).

TC ids follow the header rule of 01-requirements.md: LLR-4301.n → TC-(4300+n), LLR-4302.n → TC-(4311+n), LLR-4303.n → TC-(4320+n).

### The three synthetic old boards of LLR-4302.4 (fixture text, exact)

> Each file is `json.dumps({"phases": ["Backlog", "Doing", "Review", "Done"], "projects": [PA], "tasks": [...], "settings": {}}, indent=2)` (ensure_ascii default), PA = `{"name": "Alpha", "color": "sky", "status": "on_track", "archived": false, "pinned": false, "start_date": null, "due_date": null, "id": "pa"}`. A canonical task record R(title, id, **over) holds, in this order: title, project_id null, phase "Backlog", priority "normal", start_date null, due_date null, notes "", urls [], images [], archived false, pinned false, blocked false, depends_on [], phase_changed null, milestone false, id — the key order `Board._to_dict` writes for a task with no mark, show_in_present true and no created.
> - **plain**: tasks R("Sync notes", "ta", project_id "pa", phase "Doing"), R("Ship café", "tb") — `1126` bytes, `é` written `é`.
> - **legacy**: one task `{"title": "Old one", "status": "doing", "url": "https://example.com/a", "id": "tl"}` — `449` bytes.
> - **unknown key**: one task `{"zz": 1, **R("Has extra", "tu")}` — the unknown key FIRST, where `_to_dict` writes extra keys — `741` bytes.
> At base and in the design alike: plain and unknown key are byte-equal after `Board.load` + `save()`; legacy is NOT (the status/url migration consumes both keys: 449 → `761` bytes, sha256 `fa38dbd0e977ae0b23c3ecabbd79b3ea68558fc83efb4b93fe8761139c102e54` from both trees). So LLR-4302.4's base oracle (P-D-1 ruling) is: plain and unknown key → the input bytes; legacy → these 761 bytes, a fixed literal held in the test. LLR-4302.5 (TC-4316) runs on the plain board only, with a `history.jsonl` beside it holding ONE birth record for "ta": `{"task": "ta", "from": null, "to": "Doing", "at": "2026-10-20T09:00:00"}` (ARCH-2: something a back-fill mutant could copy into `created`; history is a separate file, so TC-4315's byte oracle of board.json is unaffected).

## Nodes

Task
req: LLR-4301.1, HLR-4301
in: str title; str? created = None
out: Task task
func: changed from baseline: the dataclass gains `created: str | None = None` declared after `show_in_present` and before `extra` (fields: title, project_id, phase, priority, start_date, due_date, notes, urls, images, archived, pinned, blocked, depends_on, phase_changed, milestone, mark, show_in_present, created, extra, id). A plain default `None`, never a `default_factory` (a factory stamp would stamp every load and every transient Task). Positional construction `Task(title, project_id, phase, priority, …)` (seed_data, tests) is unaffected because the new field follows every field that is passed positionally. A comment above it in the house style: "when the task was first added (`stamp()`, local time to the second); None on every task older than the field and on rescued entries — unknown, never back-filled; written only when set (`Board._to_dict`)".
module: taskboard/models.py
modify: [Data: Task.created] (replace)
examples: (TC-4301) Task("x") → created `None`
examples: (TC-4301) Task("x", created="2026-10-31T18:20:00") → created "2026-10-31T18:20:00"
examples: (TC-4301) Task("Design", "pid", "Doing", "high") → priority "high", created `None` (positional fields keep their meaning)

Task.from_dict
req: LLR-4302.2, LLR-4302.3, LLR-4301.11, HLR-4302
in: dict d
out: Task task
func: changed from baseline: "created" joins `_TASK_KEYS`, so `_extra_keys` no longer copies it. Inside the existing `try`: `extra = _extra_keys(d, _TASK_KEYS)`; `if "created" in d and not isinstance(d["created"], str): extra["created"] = d["created"]` (the raw value, `None` included, kept verbatim so it round-trips, LLR-4302.3); and `cls(..., extra=extra, ..., created=d["created"] if isinstance(d.get("created"), str) else None)`. A `str` is taken as is: no `strip`, no `fromisoformat` (validity is the list's concern, `added_moment`, LLR-4304.8). Never raises: the `isinstance` guards cannot throw; a non-dict still goes to `_rescue_task` (created `None`). Key order consequence: a non-str value now lives in `extra`, and `_to_dict` writes extra keys FIRST, so on the first save that key moves to the front of its record (values equal; the second save is a fixed point) — the same thing base does to every unknown key placed elsewhere (P-1b); a `str` value is written just before `id` (P-D-3)
module: taskboard/models.py
examples: (TC-4313) d "title" "a", "created" "2026-10-30T08:10:00" → created "2026-10-30T08:10:00", extra `{}`
examples: (TC-4313) d "title" "a", "created" "not a date" → created "not a date", extra `{}`
examples: (TC-4314) d "title" "a", "created" `5`, "id" "t5" → created `None`, extra "created": `5`
examples: (TC-4314) d "title" "a", "created" `None`, "id" "t5" → created `None`, extra "created": `None` (the key present with JSON null)
examples: (TC-4314) d "title" "a", "created" `True` → created `None`, extra "created": `True` (a bool is not a str)
examples: (TC-4314) d "title" "a", "id" "t6" (no created key) → created `None`, extra `{}` (nothing invented)
examples: (TC-4311) d ["x"] → title "(recovered task)", created `None`

_rescue_task
req: LLR-4301.11
in: object entry; str reason
out: Task task
func: unchanged from baseline: builds `Task(title=…, notes=…, extra={"_rescued", "_rescue_reason"})`, so created takes the default `None`; a `created` string inside the unreadable entry is preserved only inside the rescued notes text (its raw dump), never as the field
module: taskboard/models.py
examples: (TC-4311) entry ["x"], reason "not a JSON object" (via Task.from_dict) → created `None`, extra "_rescued": `True`
examples: (TC-4311) entry "title" "Bad", "created" "2026-10-01T09:00:00", reason "TypeError" → title "Bad", created `None`

Board._to_dict
req: LLR-4302.1, LLR-4302.3, LLR-4302.4, LLR-4302.7, HLR-4302
in: Task | Project item; bool with_created = False
out: dict record
func: changed from baseline (SEC-1 ruling, round 1): `d = asdict(item)` (a deep copy: `item.extra` is never mutated); the `show_in_present` / `mark` / `present_rank` drops as at base; then one more drop: `if "created" in d and (d["created"] is None or not with_created): del d["created"]` (written only when set, LLR-4302.1, and only when asked, LLR-4302.7); `extra = d.pop("extra", {})`; `if not with_created: extra.pop("created", None)` (a non-str raw value in extra stays out of the push too); `return {**extra, **d}` as at base. With `with_created=True` (the board file, via `_serialized`) a set created is written in field position: after milestone / mark / show_in_present, just before `id`, and a non-str created from the file (it sits in `extra`, field None) is written FIRST with its raw value. The default `False` is what `TeamState.push` gets: it keeps calling `board._to_dict(t)` unchanged (team_sync.py:157, no 5th source file), so no push record carries `created`. A Project has no created field; an unknown "created" key in a project's extra is kept by `_serialized` (it passes `with_created=True` for projects too) and is left out only of a call that never happens for projects (the push sends tasks only). Callers (census, `grep -rn "_to_dict" taskboard/`, state `executed`): models.py:1071 and :1072 (`_serialized`, the only path to `save` and `save_atomic`), team_sync.py:157 (`TeamState.push`); nothing else in taskboard/ calls it, and no taskboard/ code other than `_serialized` needs `created` in the record. Tests that call it directly (tests/test_cascade.py:42 `_dump` compares a board's tasks before/after with the same call on both sides; tests/test_marks_directory.py:254, :263 read `mark`; tests/test_boards_move.py:188 a project) need no `created` (reasoned, `planned` for the E4 guard run)
module: taskboard/models.py
examples: (TC-4312) Task("x", id="t1") → no "created" key; keys end "phase_changed", "milestone", "id" (with_created `False` or `True`)
examples: (TC-4312) Task("x", id="t1", created="2026-11-01T08:10:00"), with_created `True` → "created": "2026-11-01T08:10:00"; keys end "milestone", "created", "id" (`planned`: the with_created form)
examples: (TC-4314) the task of d "title" "a", "created" `5`, "id" "t5", with_created `True` → record "created": `5`; keys start "created", "title" and end "milestone", "id"
examples: (TC-4314) the task of d "title" "a", "created" `None`, "id" "t5", with_created `True` → record "created": `None` (JSON null written back, key first)
examples: (TC-4318) Task("x", id="t1", created="2026-11-01T08:10:00"), default call `Board._to_dict(task)` (the push's call) → no "created" key; keys end "milestone", "id" (`planned`)
examples: (TC-4318) the task of d "title" "a", "created" `5`, "id" "t5" (raw value in extra), default call → no "created" key, and the task's `extra` still holds "created": `5` afterwards (`planned`)
examples: (TC-4312) Project("Alpha", "sky", "on_track") → keys "name", "color", "status", "archived", "pinned", "start_date", "due_date", "id" (as at base)

Board._serialized
req: LLR-4302.7, LLR-4302.1, LLR-4302.3, LLR-4302.4, HLR-4302
in:
out: str text
func: changed from baseline (SEC-1 ruling): the two list comprehensions call `self._to_dict(p, with_created=True)` and `self._to_dict(t, with_created=True)`; everything else as at base (`json.dumps({phases, projects, tasks, settings}, indent=2)`). The one path to the board file (`save` and `save_atomic`), so every byte law of HLR-4302 holds exactly as with the round-0 design; LLR-4302.1's "with a value, the key holds it" is observed here, on the saved record
module: taskboard/models.py
modify: [I/O: board.json] (replace)
examples: (TC-4318) a board holding the stamped task "t1" (created "2026-11-01T08:10:00") and the task "t5" whose raw "created" `5` sits in extra → `json.loads(board._serialized())["tasks"]` holds "created": "2026-11-01T08:10:00" for "t1" (before "id") and "created": `5` for "t5" (first key) (`planned`; NC `_serialized` without `with_created=True`: both keys missing, RED)

TeamState.push
req: LLR-4302.7
in: Board board
out: bool written
func: unchanged from baseline (team_sync.py:143): for every task of a team project, `record = board._to_dict(t)` (the DEFAULT `with_created=False`), `record["owner"] = user_id`, written to `<shared_dir>/board.<user>.json` with `pushed_at`. No edit in team_sync.py: the drop lives in `_to_dict`'s default (SEC-1)
module: taskboard/team_sync.py
modify: [I/O: board.<user>.json] (replace)
examples: (TC-4318) a team board (tests/test_team_sync.py's set-up) with one team task added through `Board.add_task` (so stamped) and one whose file entry held "created" `5` → the pushed `board.<user>.json` records hold no "created" key (`0`/`2`), every other key as before (`planned`; NC `_to_dict`'s default `with_created=True`: RED)

Board.load
req: LLR-4301.6, LLR-4302.2, LLR-4302.4, HLR-4301
in: str | Path path
out: Board board
func: changed from baseline, the missing-file (seed) branch only: `projects, tasks = seed_data()`; `at = stamp()` (ONE clock read); `for t in tasks: t.created = at`; then `cls(projects, tasks, path=path, settings={"migrations": …})` and `save()` as at base. No history line is written for seeded tasks (as at base; scope: no change to which paths write history). The stamp is applied here, not inside `seed_data()`, so `seed_data()` stays a pure content function for its other callers (P-D-5). The existing-file branch is unchanged: per-entry `Task.from_dict` reads created
module: taskboard/models.py
modify: [Data: Board.tasks] (replace); [Data: Task.created] (replace)
examples: (TC-4306) path to a missing file, `models.datetime.now()` advancing `1` s per call from 2026-11-01T08:10:00 → `16` tasks, every created "2026-11-01T08:10:00" (`1` distinct value), the file holds `16` `"created":` keys, history.jsonl not written (`False`)
examples: (TC-4306) the same advancing clock → `1` distinct value (the NC "stamp per task" gives 16 and is RED; P-D-10 ruling: this advancing clock is the one TC-4306 uses)
examples: (TC-4313) an existing file whose task holds "created": "2026-10-30T08:10:00" → that task's created "2026-10-30T08:10:00"; nothing written

seed_data
req: LLR-4301.6
in:
out: tuple(list[Project] projects, list[Task] tasks)
func: unchanged from baseline: the 6 projects and 16 tasks, each built with `Task(...)` and so created `None`; Board.load stamps them. Callers: `Board.load` (models.py:1009) is the only one in taskboard/; `.fast-dev-flow/probes/_probe_gantt.py:26` and `_probe_premises.py` call it for synthetic boards (tooling, untouched)
module: taskboard/models.py
examples: (TC-4306) seed_data() → `16` tasks, every created `None`

Board.save
req: LLR-4302.4, LLR-4302.5, LLR-4301.5, LLR-4301.7, HLR-4302
in:
out: None
func: unchanged from baseline (`json.dumps(…, indent=2)`, `write_text`); its bytes change only through `_to_dict`. Traced here because the byte laws of HLR-4302 and the file side of the add stamp are observed at the save
module: taskboard/models.py
modify: [I/O: board.json] (replace)
examples: (TC-4315) the plain old board (fixture note above), Board.load + save → bytes equal `True`, `1126` bytes, no "created" in the file
examples: (TC-4315) the unknown-key old board, Board.load + save → bytes equal `True`, `741` bytes, "zz" still first in its record
examples: (TC-4315) the legacy old board, Board.load + save → `761` bytes with sha256 "fa38dbd0e977ae0b23c3ecabbd79b3ea68558fc83efb4b93fe8761139c102e54", byte-equal to the base oracle (the bytes eb411e1 writes, a literal held in the test), no "created" (P-D-1 ruling; NOT byte-equal to the 449 bytes read, at base or here)
examples: (TC-4316) the plain old board (LLR-4302.5 runs on this fixture only, P-D-1 ruling), then Board.add_task(Task("New one", id="tn")) at clock 2026-11-01T08:10:00 → `json.dumps(entry, indent=2)` of entries 0 ("ta") and 1 ("tb") equal before and after (`2`/`2`); entry 2 "tn" ends "milestone": `False`, "created": "2026-11-01T08:10:00", "id": "tn"
examples: (TC-4316) the same board with its `history.jsonl` holding the birth record of "ta" at "2026-10-20T09:00:00" (ARCH-2 fixture) → after the add, entry 0 ("ta") still holds no "created" key and its slice is equal before and after (`planned`; NC a save-time back-fill from birth records: "ta" gains "created": "2026-10-20T09:00:00", RED — HLR-4302's NC names this test)
examples: (TC-4305) a board holding "to", Board.add_task(Task("a", id="tn")) at clock 2026-11-01T08:10:00 → the file's "tn" record holds "created": "2026-11-01T08:10:00" before "id"; history.jsonl gains "task": "tn", "from": `None`, "to": "Backlog", "at": "2026-11-01T08:10:00" (one `now` read by add_task: created = stamp(now), history `at=now`, the corrected interface, P-D-4 ruling)
examples: (TC-4307) then Board.add_task(Task("b", id="tp", created="2026-10-01T09:00:00")) → the file's "tp" record holds "created": "2026-10-01T09:00:00"

move_project
req: LLR-4301.9
in: Board src; Board dst; str project_id; MovePlan plan; str day; tuple[str, str] names
out: tuple(Board new_src, list[str] steps)
func: unchanged from baseline: `copy.deepcopy` of both boards carries `Task.created` (a plain str field) with every other field; `new_dst.tasks.extend(moving)` then `save_atomic()` writes each moved record through `_to_dict`, so a set created is kept and a None one writes no key; nothing re-stamps (the moved tasks never pass `Board.add_task`); their history lines move as at base
module: taskboard/boards.py
modify: [Data: Board.tasks] (append); [I/O: history.jsonl] (append)
examples: (TC-4309) src projects pm, ps; tasks m1 (pm, created "2026-10-30T09:00:00"), s1 (ps), m2 (pm, created `None`); dst d1; move "pm" → refusal `None`; dst file order "d1", "m1", "m2"; m1's record "created": "2026-10-30T09:00:00" (keys end "created", "id"); m2's record has no "created" key (keys end "milestone", "id")

app_bindings
req: LLR-4303.1, LLR-4303.23
in:
out: list[Binding] bindings
func: unchanged from baseline (one Binding per KEYMAP entry); the new seat entry `Key("N", "N", "added_list", "Added list", group="misc", bar=False)` becomes `Binding("N", "added_list", "Added list", priority=False)` on TaskboardApp.BINDINGS with no other edit. Not priority, like `A`: on the list view the screen's own priority `escape,N` wins (group S)
module: taskboard/keymap.py
oracle: README.md, section "Keys": the key table carries one row per seat key (tests/test_keymap.py::test_the_readme_keybinding_table_matches_the_seat)
examples: (TC-4321) KEYMAP → exactly `1` entry whose keys is "N"; its bar `False`, views `None`, priority `False`, action "added_list", label "Added list", group "misc"
examples: (TC-4321) app_bindings() → one binding key "N", action "added_list"; `len(TaskboardApp.BINDINGS) == len(KEYMAP)` (test_every_binding_the_app_has_comes_from_the_seat) stays GREEN
examples: (TC-4343) README.md holds a line that starts "| `N` |" inside the "## Keys" table, right after the "| `A` | All boards |" row → test_the_readme_keybinding_table_matches_the_seat GREEN; without that line it fails "N (Added list) is bound but the README never mentions it"

global_keys
req: LLR-4303.1
in: str view
out: list[Key] keys
func: unchanged from baseline: the live `bar=False` keys in seat order; `N` sits right after `A` in KEYMAP (declared beside it, with a comment in the house style naming this increment), so the `?` help's global line and the palette read "… A All boards  N Added list  H Report …"
module: taskboard/keymap.py
examples: (TC-4321) view "gantt" → shows "o", "i", "p", "P", "f", "c", "R", "A", "N", "H", "@", "#", "I", "S" in that order (`14`, was 13)
examples: (TC-4321) the `?` help on the gantt at 80x24 (box content width `69`) → global line of `4` rows (was 3) holding "R Present", "A All boards  N Added list  H Report" and "S Standup" unscrolled; at 118x30 (width `103`) still `2` rows (executed with the seat patched: tests/test_help_keys.py 9 passed)

palette_commands
req: LLR-4303.1
in: str view
out: list[tuple[str, str, str]] commands
func: unchanged from baseline: every live key, universal first; the `N` entry appears as ("N", "Added list", "added_list") in every view's palette, which runs `action_added_list` (group S)
module: taskboard/keymap.py
examples: (TC-4321) view "swimlanes" → holds ("N", "Added list", "added_list") exactly once

## Entities

[Data: models._TASK_KEYS]
in: set[str]
desc: changed from baseline: "created" added (models.py:706-709), so `_extra_keys` never copies a created key into extra; the non-str case is put back into extra explicitly by Task.from_dict (LLR-4302.3)

[Data: Task dataclass fields]
desc: changed from baseline: title, project_id, phase, priority, start_date, due_date, notes, urls, images, archived, pinned, blocked, depends_on, phase_changed, milestone, mark, show_in_present, created, extra, id; on disk a set created is written after milestone/mark/show_in_present and before id

[Data: Task.extra]
in: dict
desc: changed from baseline: also holds "created" when the file's value is not a str (`5`, null, a list, a bool), raw, written first in the record; never holds a str created

[I/O: board.json]
desc: changed from baseline: a task record holds "created" only when the task's created is set: every task added from this increment on (add_task, template insert, link create, seed) and none older; an old board keeps its bytes through load + save (P-1, TC-4315) except where base already rewrites it (legacy keys, an unknown key placed after another key)

[I/O: board.<user>.json]
desc: the team push file in the shared folder (team_sync.py); written by `TeamState.push` from `Board._to_dict(t)` records; never holds a "created" key (LLR-4302.7, SEC-1), neither the field nor a raw non-str value from extra

[Data: keymap.KEYMAP]
in: tuple[Key, ...]
desc: changed from baseline: one entry `Key("N", "N", "added_list", "Added list", group="misc", bar=False)` declared right after the `A` entry; keys "N" and show "N" are free (P-7); uppercase letters in use become A B F H I L M N P R S T X; label "Added list" is used by no other entry (labels "Focus" and "Standup" already occur twice; the seat test does not check labels, P-D-7)

[I/O: README.md key table]
desc: the "## Keys" table (README.md:101-143); test_the_readme_keybinding_table_matches_the_seat collects every backticked token of the FIRST cell of every README line that starts with "| `" (any table) and requires each seat key in its README spelling (`N` → "N"); it pins only that token, in one direction (seat → README). The row text proposed, after README.md:135: "| `N` | Added list | Every task of every board in the order you added it, newest first (`o` flips it): when it was added (`≈` from history, `?` unknown), a box per phase, and the cursor's task in full beside the list; `v` shows archived tasks, `enter` opens a task on its board, `esc` or `N` closes. Nothing here edits a task |" — every word after the first cell is unpinned. One more README edit, group D's at E4 (docs only, unpinned): P-D-9 ruling, the "On the home:" table: after README.md:329 "| `A` | The agenda of every board (see `A` above) |" the row "| `N` | Every task of every board in the order you added it (see `N` above) |" (`N` is live over BoardsHome: graph-proto-S TC-4324 arm 3); README.md:400 (the history.jsonl row of "## Data files") is left as it is. No README edit in "## Team mode": the P-D-6 team note is withdrawn (SEC-1 ruling, round 1: the push no longer carries `created`, so there is nothing to document)

[Outside: key N]
desc: changed from baseline: bound by KEYMAP (app level, not priority) to `added_list`; still free in every Screen's BINDINGS except the list view's own priority `escape,N` (group S); lowercase `n` unchanged (BoardsHome, PeopleDirectory, MarksManager, ConfirmModal, MoveConfirm)

## Edges

[Data: models._TASK_KEYS] ──▶ Task.from_dict
[I/O: board.json] ──▶ Board.load
Board.load ──▶ [Data: Task.created]
Task.from_dict ──▶ [Data: Task.created]
Task.from_dict ──▶ [Data: Task.extra]
Task ──▶ [Data: Task.created]
[Data: Task.created] ──▶ Board._to_dict
[Data: Task.extra] ──▶ Board._to_dict
Board._to_dict ──▶ Board._serialized
when: with_created=True (tasks and projects)
Board._serialized ──▶ Board.save
Board.save ──▶ [I/O: board.json]
Board._to_dict ──▶ TeamState.push
when: the default with_created=False: no created in the record (SEC-1)
TeamState.push ──▶ [I/O: board.<user>.json]
[Data: Task.created] ──▶ move_project
seed_data ──▶ Board.load
stamp ──▶ Board.load
[Data: keymap.KEYMAP] ──▶ app_bindings
[Data: keymap.KEYMAP] ──▶ global_keys
[Data: keymap.KEYMAP] ──▶ palette_commands
[Outside: key N] ──▶ TaskboardApp.check_action
when: no ModalScreen is on the stack (LLR-4303.21); then TaskboardApp.action_added_list runs (group S)

## Findings

finding P-D-1 LLR-4302.4's legacy arm (and LLR-4302.5 on a legacy board) cannot pass, at base or with any design of this increment
anchor: Board.save
seen: the legacy fixture (status "doing", url, 449 bytes) after Board.load + save is 761 bytes, the same sha256 fa38dbd0… from eb411e1 and from the design copy: `Task.from_dict` consumes `status`/`url` (they are in `_TASK_KEYS`) and the save writes phase/urls instead (baseline func of Task.from_dict). An add on that board rewrites its old entry the same way ("vs original file" False at base too)
effect: TC-4315 arm 2 and any LLR-4302.5 test on a legacy board are RED whatever this increment does; the legacy migration is out of scope
decision: ruling (03-pdr-rulings round 0): "Accept. The legacy arm of LLR-4302.4 compares against the bytes eb411e1 writes for the same file (a fixed oracle held in the test), not the input bytes. LLR-4302.5 runs on the plain fixture." Applied: fixture note (the base oracle per board), Board.save TC-4315 legacy arm (761 bytes, sha256 fa38dbd0…), Board.save TC-4316 (plain board only)

finding P-D-2 the unknown-key arm is byte-stable only when the key comes first in its record
anchor: Board.save
seen: `{"zz": 1, …}` → equal (741 bytes); the same record with "zz" after "id" → not equal at base (P-1b: the key moves to the front)
decision: ruling (03-pdr-rulings round 0): "Accept: the unknown-key fixture puts the key first in its record (where the app writes it)." Applied: fixture note (unknown key board), Board.save TC-4315 unknown-key arm

finding P-D-3 a non-str created moves to the front of its record on the first save
anchor: Task.from_dict
seen: "created": `5` or null anywhere in a record → written back with the same value as the record's first key (design copy); the second save is a fixed point
cause: the raw value lives in `extra`, and `_to_dict` writes extra keys first (base rule, shared with every unknown key)
effect: LLR-4302.3's threshold is by value ("round-trip … to the same values"), so it holds; byte stability holds only for a file the app wrote. HLR-4302 speaks of tasks that hold no created; an entry with `"created": null` holds the key, so it is outside HLR-4302's byte law
decision: ruling (03-pdr-rulings round 0): "Accept as designed: a non-str created moves to the front of its record on the first save; its value round-trips. Stated in LLR-4302.3's threshold (values, not bytes)." Applied: Task.from_dict func, Board._to_dict TC-4314 (value asserted, key first)

finding P-D-4 Board.add_task should read the clock once for the stamp and the birth record
anchor: Board.add_task
seen: graph-interfaces' add_task func stamps with `stamp()` and then calls `history.append` "as at base", which reads `datetime.now()` again (history.py:33); TC-4305 shows both values "2026-11-01T08:10:00", which two reads cannot guarantee across a second boundary. models.py imports only `date, timedelta` (models.py:19)
decision: ruling (03-pdr-rulings round 0): "Accept. Board.add_task reads the clock once: now = datetime.now(), task.created = stamp(now) when None, history.append(..., at=now)." Applied: graph-interfaces Board.add_task (orchestrator); here Board.save TC-4305 (created and `at` from one `now`), Seams. Implementation notes kept: models.py imports `datetime` (`from datetime import date, datetime, timedelta`); `history.append` already takes `at` (history.py:24); tests monkeypatch `taskboard.models.datetime`; with a preset created (LLR-4301.7) the birth `at` is the add moment, as at base

finding P-D-5 the seed stamp goes in Board.load, not in seed_data
anchor: Board.load
seen: `seed_data()` callers: models.py:1009 (Board.load) only in taskboard/; `.fast-dev-flow/probes/_probe_gantt.py:26` and `_probe_premises.py` call it for synthetic boards; tests reach it only through Board.load (test_app.py:722)
decision: ruling (03-pdr-rulings round 0): "Accept: the seed stamp is applied in Board.load's seed branch; seed_data() is unchanged." Applied: Board.load func and TC-4306, seed_data TC-4306

finding P-D-6 the team push now carries `created` to the shared folder
anchor: Board._to_dict
seen: team_sync.py:157 `record = board._to_dict(t)` for every pushed team task, so a stamped team task's record in `board.<user>.json` gains "created": "<local time of day>"; team_sync.foreign_tasks (team_sync.py:221) reads it back into teammates' `Task.created`. No test pins the push record's keys: test_team_sync.py:85-113, test_milestones.py:395-410 and test_marks_directory.py:400-412 assert single keys or absent strings only (all GREEN on the design copy). report.py / report_html.py build their own dicts and never call `asdict(task)`; no other `asdict` of a Task exists outside `_to_dict`
effect: privacy — one new piece of metadata (when the owner added a shared task, local time to the second) goes to teammates; same class as phase_changed, which already travels. Unstamped tasks push no key
decision: ruling (03-pdr-rulings round 0): "Accept as designed, documented. README gets one line under the team section; backlog item L-BL-1 for an opt-out. The security reviewer may reopen it at PDR." Applied: [I/O: README.md key table] edit (2) — section "## Team mode", new paragraph after README.md:265 with the exact text given there (group D, E4); team_sync.py untouched; L-BL-1 is the orchestrator's BACKLOG entry, not in this file. SUPERSEDED by SEC-1 (round 1, below): the push no longer carries `created`, and the README team note is withdrawn

finding P-D-7 the seat duplicate test checks keys and shows, not labels
anchor: [Data: keymap.KEYMAP]
seen: tests/test_keymap.py:116-119 asserts `len(set(k.keys))` and `len(set(k.show))` only; labels "Focus" (5, F) and "Standup" (8, S) already occur twice in KEYMAP
decision: ruling (03-pdr-rulings round 0): "Accept: label Added list (unique)." Applied: [Data: keymap.KEYMAP], app_bindings TC-4321

finding P-D-8 the `?` help's global line grows by one row at 80x24
anchor: global_keys
seen: global_lines at box width 69: 3 rows → 4 rows with "N Added list"; at width 103: 2 rows → 2 rows. AT-1603 and the rest of tests/test_help_keys.py: 9 passed with the seat patched
decision: ruling (03-pdr-rulings round 0): "Accept: the ? help's global line grows to 4 rows at 80x24; its tests stay GREEN (guard)." Applied: global_keys TC-4321 help example (4 rows at 80x24, 2 at 118x30)

finding P-D-9 README rows beside the key row
anchor: [I/O: README.md key table]
seen: README.md:400 says history.jsonl is read by "the Flow view" — the list view reads it too; README.md:329 (home table) names `A` "also on the home", and `N` reaches the home the same way through check_action (no ModalScreen), unless group S rules otherwise
decision: ruling (03-pdr-rulings round 0): "Accept in part: README gets the N row in the key table (:135) and in the home/global table (:329) if that table lists A; the history.jsonl paragraph (:400) is left." Applied: [I/O: README.md key table] — the key-table row after :135 and edit (1), the home-table row after :329 (it lists `A`, and `N` is live over BoardsHome); :400 unchanged

finding P-D-10 TC-4306 needs a clock that moves to catch a per-task stamp
anchor: Board.load
seen: with a frozen or real clock, a mutant that calls `stamp()` once per seeded task almost always yields 1 distinct value (16 calls inside one second), so the "1 distinct value" arm is not a negative control for it
decision: ruling (03-pdr-rulings round 0): "Accept: TC-4303/TC-4306 use a clock that advances 1 s per call (monkeypatched models.datetime), so a stamp-per-task mutant fails." Applied: Board.load TC-4306 arm 2 (advancing clock: 1 value, the per-task NC 16); TC-4303 is group S's (graph-proto-S _on_template_picked, same clock)

finding SEC-1 MEDIUM: `created` goes out in the team push and no teammate code reads it (P-D-6 reopened at PDR)
anchor: Board._to_dict
seen: (03-pdr-security.md SEC-1) team_sync.py:157 `record = board._to_dict(t)` for every team task; with the round-0 design each stamped team task's record in `board.<user>.json` carries a per-task, second-precision local time — a log of working hours in a synced folder, with no consumer (`foreign_tasks` builds transient Tasks; nothing reads their `created`)
effect: personal data with no purpose leaves the machine; once synced it cannot be taken back
decision: ruling (03-pdr-rulings round 1): "Accept — reverses P-D-6. Remove the data from the push rather than document it: Board._to_dict(item, with_created=False) leaves out created (the field and any extra["created"]); _serialized passes with_created=True. team_sync keeps calling _to_dict(t) unchanged (no 5th file). New LLR-4302.7, TC-4318. The README team note is dropped." Applied: Board._to_dict (in, func, req LLR-4302.7, TC-4312/TC-4314 arms now `with_created=True`, TC-4318 arms 1–2), new changed node Board._serialized (TC-4318 arm 3), traced node TeamState.push (TC-4318 push arm), entity [I/O: board.<user>.json], edges; caller census in Board._to_dict's func (taskboard/: `_serialized` and `TeamState.push` only; no other caller needs `created`); P-D-6's README team note removed from [I/O: README.md key table]; Seams line. Not changed here: LLR-4302.1's threshold text still reads "`Board._to_dict(Task("x"))` … with a value, the key holds it", which under the new default holds only with `with_created=True` or on the saved record (reported to the orchestrator)

finding ARCH-2 MEDIUM: HLR-4302's back-fill NC named a test that never saves; TC-4316's fixture had nothing to back-fill
anchor: Board.save
seen: (03-pdr-architect.md ARCH-2) TC-4316 ran on the plain board with no history.jsonl, so a mutant that back-fills `created` from birth records on save writes nothing and survives
decision: ruling (03-pdr-rulings round 1): "Accept. TC-4316's plain board gains one birth record in history.jsonl (something to back-fill from); HLR-4302's NC names TC-4316." Applied: fixture note (the history.jsonl line for "ta" at 2026-10-20T09:00:00), Board.save TC-4316 arm 2 (the back-fill NC)

finding ARCH-7 MINOR: `Task.from_dict` could pop a str `created` out of extra instead of extending `_TASK_KEYS`
anchor: Task.from_dict
seen: (03-pdr-architect.md ARCH-7) the `_TASK_KEYS` design re-appends a non-str value at the END of extra, reordering unknown keys relative to base on a hand-edited record
decision: ruling (03-pdr-rulings round 1): "Reject (style): D's _TASK_KEYS design stands; SEC-1 touches _to_dict anyway and both are equally small." Applied: none (Task.from_dict and [Data: models._TASK_KEYS] unchanged)

### Seams

> Called by group D into the interfaces: `stamp(now=None) -> str` (graph-interfaces; defined in models.py, i.e. in this group's file) from Board.load (seed) and Board.add_task. `Board.add_task` is implemented in models.py by this group to the corrected interfaces' contract (one `now`: created = stamp(now), history `at=now`; P-D-4 ruling).
> Offered to group S (app.py): `Board.add_task` stamps every task whose created is None, so `_on_task_added` and `_create_and_link` need no edit (LLR-4301.2, LLR-4301.4); `stamp()` for `_on_template_picked` (one call per insert, assigned to every inserted task, LLR-4301.3), which appends without add_task; the seat entry `N` → `added_list`: S must add `TaskboardApp.action_added_list` (else tests/test_keymap.py::test_every_shown_key_has_a_real_action_on_the_app is RED), name `added_list` beside agenda_all / people_directory / marks_manager in check_action's modal gate, and add AddedList to the holding tuple (LLR-4303.21, LLR-4303.22). `added_list` enters `SEAT_ACTIONS` automatically (it is built from KEYMAP).
> Offered to group V (views.py): `Task.created` is `str | None`, any str (valid or not, aware or naive) — V's `added_moment` validates; a non-str stored value is NOT on the field (it is in `task.extra["created"]`), so V never sees a non-str there; `Board.phases` and file order are unchanged.
> Shared files: models.py (D only), keymap.py (D only). README.md (docs, D writes the `N` row). team_sync.py untouched (SEC-1: `TeamState.push` keeps calling `_to_dict(t)`, whose default now leaves `created` out; P-D-6's README note is withdrawn).
