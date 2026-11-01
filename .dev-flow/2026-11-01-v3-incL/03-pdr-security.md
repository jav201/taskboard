# Inc L — PDR security review (E3, security-reviewer)

**Verdict: PASS-WITH-NOTES** — 0 HIGH · 3 MEDIUM · 2 LOW. No HIGH, so nothing blocks the design gate. The three MEDIUM findings are `planned` mitigations. Each one needs its change in the E4 build and a test that fails without the change. I re-check them at the increment gate.

## Scope reviewed

- `01-requirements.md` (68 LLRs), `03-pdr-rulings.md` round 0 (it overrides older text), `graph-interfaces.cw.md`, `graph-proto-D.cw.md`, `graph-proto-V.cw.md`, `graph-proto-S.cw.md`, `baseline-notes.md`.
- Base code read at `966020f` (base `eb411e1` plus design files only): `models.py` (`Task.from_dict`, `Board.load`, `_to_dict`, `strip_controls`/`clean_strings`, `_quarantine_corrupt_file`), `history.py`, `boards.py` (`peek_board`), `app.py` (`board_lanes`, `open_on_board`, `check_action`, `PresentScreen`), `team_sync.py` (`push`, `foreign_tasks`).
- Probes: read-only, `C:/Users/jjgh8/anaconda3/python.exe -I`, scratch scripts in `%TEMP%/incL-sec/`. Each printed `taskboard.__file__` = `…\taskboard-wt\capture-proto\taskboard\__init__.py`. Synthetic data only, temp folders, `Path.home` redirected. State: `executed`.

## Findings

### SEC-1 — `created` goes out in the team push and no teammate code reads it (P-D-6 reopened)  [MEDIUM]
- **Anchor:** `Board._to_dict` (graph-proto-D.cw.md:53, finding P-D-6 at :212). Ruling P-D-6 (03-pdr-rulings.md:14).
- **Seen:** `team_sync.py:157`: `record = board._to_dict(t)` for every team task, written to `<shared_dir>/board.<user>.json`. With the design, every stamped team task's record gains `"created": "YYYY-MM-DDTHH:MM:SS"`. That is local time to the second, with no offset. The ruling calls this "no new class of data". I disagree.
  - `phase_changed` is a **date** only (models.py:1261).
  - `start_date`/`due_date` are **planned** dates.
  - `pushed_at` is one UTC value. Each periodic daemon push overwrites it (app.py:1729).
  - `created` is different: a permanent, per-task, second-precision record of when the person was working. It accumulates into a log of their activity hours. A file like `board.<user>.json` typically sits in a synced folder (SharePoint, Drive or git, per the team_sync docstring), so this data leaves the machine.
  - No consumer exists. `foreign_tasks` (team_sync.py:221) parses it into transient Tasks. Nothing reads a foreign task's `created`, and the list view lists registry boards only. The README sentence the design plans ("teammates read it as they read its title…", graph-proto-D.cw.md:156) is therefore not true either.
- **Risk:** personal data with no purpose leaves the system. This is a data-minimisation problem under GDPR / LFPDPPP (the jurisdiction is not declared; the operator should say which applies). The team can profile working hours from it. Once pushed and synced, it cannot be taken back.
- **Proposal (remove, not document):** keep `created` out of the push. This needs no 5th source file.
  - `Board._to_dict(item, with_created=False)` drops `created` unless asked.
  - `Board._serialized` (models.py:1068) passes `with_created=True` for tasks.
  - `team_sync.push` keeps calling `_to_dict(t)` unchanged, so it never sends the field.
  - Key position on disk is unchanged (the key just before `id`). LLR-4302.1's threshold moves from `_to_dict` to the saved record.
  - Add one test, uncapped: a pushed record of a stamped team task has no `"created"` key. NC: the default `with_created=True` turns it RED.
  - Drop the planned README team-mode sentence.
  - L-BL-1 becomes "opt-in, if a teammate feature ever needs it".
  - A non-str `created` kept in `extra` still travels, as every unknown key already does at base. Acceptable.
- **Evidence state:** finding `executed` (code read). Mitigation `planned`.

### SEC-2 — one deeply nested line in any board's `history.jsonl` crashes `N`  [MEDIUM]
- **Anchor:** `added_rows` (graph-interfaces.cw.md:28–32; graph-proto-V.cw.md:170–174), which guards `history.read` with `except (OSError, ValueError)` only. `AddedList.compose` (graph-proto-S.cw.md:39) says "No try/except … added_rows is total".
- **Seen:** probe `p3.py`. A `history.jsonl` holding one line of 200 000 `[` makes `history.read` raise **RecursionError**. RecursionError is neither an `OSError` nor a `ValueError`. `history.read` catches only `json.JSONDecodeError` per line (history.py:66), even though its docstring promises "never raise".
  - The house rule elsewhere already names this case: `peek_board` (boards.py:623), `Board.load` (models.py:1018) and `team_sync._read_json` all catch `RecursionError` (the S4-1 lesson).
  - The list view reads the history of **every** registry board. At base only the open board's Flow view reads one.
- **Risk:** someone hand-edits or crafts a history file, or a synced folder corrupts one, in any registered board folder. The exception comes out of `compose`, Textual ends the app, and every later `N` does it again. No data is lost, but the view cannot be used.
- **Proposal:** widen the guard in `added_rows` to `except (OSError, ValueError, RecursionError)` → no births for that board.
  - Extend LLR-4304.12's threshold with a third arm (TC-4372c: a 200 000-`[` line → rows built, 0 exceptions).
  - Add a BACKLOG item: fix it at the source, in `history.read`, so a RecursionError line counts as skipped. The Flow view has the same crash today. history.py is out of this increment's scope.
- **Evidence state:** finding `executed` (probe). Mitigation `planned`.

### SEC-3 — a non-string task id on another board crashes `N` and the pane  [MEDIUM]
- **Anchor:** `added_rows`: `births.get(task.id)` (graph-interfaces.cw.md:32). `_added_pane`: `titles = {t.id: t.title for t in row.board.tasks}` (graph-proto-V.cw.md:135).
- **Seen:** `Task.from_dict` keeps `id=d.get("id") or _new_id()` with any JSON type (models.py:929). Probe `p2.py` (pilot, two-board registry): one task on a peeked board with `"id": [1, 2]`.
  - At base, `A` and `@` open and close cleanly.
  - The design's lookups on the same `board_lanes` output raise `TypeError: unhashable type: 'list'`. The first one runs in compose, so the app crashes. The second runs on every paint of a task with `depends_on`.
  - A dict id behaves the same way. An int id is harmless.
- **Risk:** the same crash class as SEC-2. The view newly reads other boards' data in a way the existing views do not.
- **Proposal (remove the hashing of untrusted ids, not wrap it):**
  - `added_rows`: look up births only for `isinstance(task.id, str)`. Birth keys are always str, so any other id can never match and gets source `?`.
  - `_added_pane`: build `titles` from str ids only. `depends_on` is already coerced to str.
  - New LLR under HLR-4304 (Unwanted: "If a task's id is not a str, then the system shall …"), TC: a peeked board with ids `[1,2]` and `{"x":1}`, plus a waiter → `N` opens, both rows source `?`, the pane renders, 0 exceptions. NC: an unguarded `births.get` turns it RED.
- **Evidence state:** finding `executed` (probe). Mitigation `planned`.

### SEC-4 — a huge note re-wraps on every paint  [LOW]
- **Anchor:** `_added_pane` (graph-proto-V.cw.md:135) wraps the whole note. `render_added_list` then keeps `room − 1` lines and counts the rest (ruling P-V-7). The V performance note measures N rows, not note size.
- **Seen:** probe `p2.py`: `notes_text` + `Text.wrap(rw=67)` costs 0.17 s for a 1 MB note and 0.92 s for 5 MB. The cost repeats on every key and resize while the cursor is on that task.
  - Related, also measured: `history.read` of 500 000 lines takes 0.84 s per board, once at open. That is acceptable.
- **Risk:** a crafted board (in any registered folder) makes the list sluggish. No crash, no data effect.
- **Proposal:** before `notes_text`, cut the note to the first `room × rw` characters. That is all the pane can ever show. When the note was cut, end the pane with `… more lines` instead of an exact `k`. TC: a 5 MB note → one paint under 50 ms.
- **Evidence state:** finding `executed` (probe). Mitigation `planned`.

### SEC-5 — reading other boards adds no new kind of path, but the base race is inherited  [LOW]
- **Anchor:** `AddedList.compose` → `board_lanes` → `peek_board`. `added_rows` reads `history_path(board.path)`.
- **Seen:**
  - The list reads the same registry paths the agenda already reads, plus `history.jsonl` in the same folders. So UNC paths, symlinks, FIFOs and unreadable files are the same exposure the agenda already has, and not a new one.
  - One inherited gap: `peek_board` parses the file, then calls `Board.load`, which parses it again (boards.py:622/630). If the file becomes unreadable between the two parses (for example during a sync), `Board.load` runs `_quarantine_corrupt_file` (models.py:1023), and that **writes** a `board.json.corrupt` copy in the other board's folder. This breaks LLR-4302.6's "writes nothing" in that narrow window. It is pre-existing for `A` and `@`.
- **Risk:** low. The write is a backup copy, not the board file and not history. The window is tiny.
- **Proposal:** no change in this increment. Add a BACKLOG item: `peek_board` should build the Board from the bytes it already parsed, read once, rather than call `Board.load`. That removes both the second read and the quarantine path. LLR-4302.6 stays as written: its test checks the board files and histories, which are untouched.
- **Evidence state:** finding `executed` (code read). Mitigation `n/a — backlog`.

## Checked, no finding (evidence)

- **No markup injection:** the body and pane are built only from `Text.append` pieces. `notes_text` builds Text by hand (views.py:3651). `Static.update(Text)` parses no markup. LLR-4303.20 / TC-4340 pin this.
- **No control or ANSI characters:**
  - Board files pass `clean_strings` at the load door. That covers peeked boards too, through `Board.load`.
  - The registry and people files are cleaned (boards.py:246, people.py:177).
  - Tab and newline are flattened by `_one_line` (P-V-9).
  - `history.jsonl` strings are never drawn. Only `at` is parsed and reformatted, and `task` is used only as a dict key; `history.read` guarantees both are str.
- **Parsing untrusted `created` / `at`:**
  - A raw `created` string is never drawn. Only the parsed datetime is formatted.
  - Probes: a 10 MB string is rejected in 5 ms; ISO week and basic formats parse.
  - `+23:59` / `-23:59` offsets at year 1 and year 9999 raise OSError in `astimezone()`. LLR-4304.16 covers this (ruling P-V-2).
  - `strftime` of `%a %b %d · %H:%M` works for years 1, 999 and 9999 on this Windows machine.
  - A non-str `created` never reaches `added_moment` (it sits in `extra`).
- **Old data is never rewritten:**
  - A non-str `created` round-trips by value (LLR-4302.3).
  - `added_rows` never sets `task.created`.
  - The list view saves nothing: compose and paint only read (LLR-4302.6, TC-4317 sha256 over 4 files).
- **Presentation:** `PresentScreen` is a `ModalScreen` (app.py:198), so `added_list` is refused under it. The list cannot open over a client-facing presentation and show other boards' notes and URLs.
- **Secrets / PII in the design files:** none. All fixtures are synthetic (example.com URLs, names like "Ana Ruiz"). No new dependency and no network access.

## Evidence checklist

- ✓ Each finding has what, where, why and recommendation: SEC-1..5 each carry anchor, seen, risk and proposal.
- ✓ Each finding has a severity: 3 MEDIUM, 2 LOW.
- ✓ No secret values appear in this output: none exist in scope; fixtures are synthetic.
- ✓ The verdict is explicit: PASS-WITH-NOTES, with no HIGH present.
- ✓ The new data flow (team push) was checked for scope and blast radius: SEC-1. No new tool or integration is added.
