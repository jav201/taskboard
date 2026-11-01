# Inc L — E5 security review (increment gate)

**Verdict: PASS-WITH-NOTES.** The code implements SEC-1, SEC-2, SEC-3 and SEC-4 as the rulings designed them, and probes on crafted synthetic boards confirm each one. The list view wrote nothing in a whole-tree hash, with hostile boards registered. No secret, no new dependency, no network path and no new outbound data are added. There are 5 LOW findings and no HIGH or MEDIUM. Four of the five are inherited from base code or already ruled. None blocks.

## Scope reviewed

- Change: `git diff eb411e1 7bac31f -- taskboard/ README.md` (models.py, app.py, views.py, keymap.py, README.md).
- Design: `03-pdr-security.md`, `03-pdr-security-r2.md`, `03-pdr-rulings.md`, `e4-addenda.md`.
- Probes: `C:/Users/jjgh8/incL-e5sec-probe/test_probe_sec.py`. This is scratch outside the repo, with 28 cases on synthetic data. It ran under `C:/Users/jjgh8/anaconda3/python.exe` (3.12.7) with cwd = the worktree. It printed `taskboard.__file__` = `C:\Users\jjgh8\Github\taskboard-wt\capture-proto\taskboard\__init__.py`. State: `executed`.
- Tests: `pytest -k "4318 or 4372 or 4377 or 4332 or 4335 or 4317"` → 10 passed. State: `executed`.
- I edited no product code or tests and ran no state-changing git. `incL-mut` was not touched.

## SEC-1..SEC-4: verified in the code

| Id | Where | Verified by | State |
|---|---|---|---|
| SEC-1 `created` stays out of the team push | `models.py:1081-1103`: `_to_dict(item, with_created=False)` drops the field (:1097) and `extra["created"]` (:1101), on the dict `asdict` copied. `_serialized` passes True (:1107-1108). `team_sync.py:157` is unchanged and uses the default. | Probe `test_sec1_push`, 7 raw shapes (valid str, `5`, `{"a":1}`, `None`, `[1]`, `True`, `"garbage"`): `_to_dict(t)` has no `created`. `t.extra` is unchanged afterwards. `_serialized` keeps the raw value. The real `TeamState.push` file `board.subject.json` holds no `"created"` text at all. TC-4318 passes. Census: the only `_to_dict` callers are `_serialized` and `team_sync.py:157`, and no other writer uses `asdict(task)`. | executed, approved |
| SEC-2 a bad `history.read` does not crash `N` | `views.py:9340-9343`: `except (OSError, ValueError, RecursionError)` | Probe: a non-UTF-8 line, a 200 000-deep `[` line, a 5 000-deep dict line, and `history.jsonl` as a directory. Each gives `?` rows with no exception. A good file still gives `h`. TC-4372b/c pass. | executed, approved |
| SEC-3 non-str ids | `views.py:9346` (births keyed on str `task` only), `:9353` (lookup only for a str id), `:9607` (str-only `after:` titles) | Probe: ids `["x"]`, `{"k":1}`, `5`, `True`, `1.5`, and `""` (which becomes a fresh id), plus `depends_on` holding a list and a dict (`from_dict` stringifies them). Every order, archived setting and cursor position renders 29 lines with no exception. An odd id gets source `?` or `c`, never `h`. TC-4377 passes. | executed, approved |
| SEC-4 a huge note is cut before the wrap | `views.py:9596-9601`: the note is sliced to `nroom × (rw + 1)` before `notes_text`; `… more lines` is the tail | Probe, 5 MB notes: `lorem ` 1.4 ms per paint, `[b]x[/b] ` 0.8 ms; the tail is shown. TC-4332b/4335b pass. | executed, approved |
| ARCH-3 an offset-aware or garbage `created` is invalid | `views.py:9293-9307` | Probe of 16 values: `+05:00`, `Z`, a 10 MB string, `2026-13-45`, year 1, `9999-12-31T23:59:59.999999`, a date only, `nan`, `""`, padded, `5`, `[1]`, `None`, a dict, ISO week, Arabic-Indic digits. It never raises and the sort never mixes aware and naive datetimes. Aware values give `?` or `h`, never `c`. All work in 0.09 s. | executed |
| Markup / ANSI / control characters | Load door `clean_strings` (`models.py:1042`); the list builds plain `Text.append` pieces; `_one_line` | Probe: a board file whose title, phase, project, note, URL, image name and `created` hold ESC-CSI, raw C1 `\x9b`, BEL, BS, an OSC-8 escape, `[bold red]` and `[link=…]` markup, CR-LF and tab. The board name and person name were cleaned as the registry and people loaders clean them. No C0 or C1 byte reaches `Text.plain`. The ANSI the Rich console prints has only SGR sequences: no OSC-8 hyperlink and no other escape. The markup shows as literal text. | executed |
| The list writes nothing | `AddedList` (`app.py:965-1060`) reads through `board_lanes` → `peek_board`. Its actions only repaint, and `enter` hands off to `open_on_board` (a switch, base behaviour, the same as `A`). | Probe `test_list_writes_nothing_hostile`: sha256 of every file under `Path.home()` (registry, people, every board, every history), before and after `N ↓ ↓ o v v ↑ esc`. The registry holds 4 boards, among them a board with a list id and `created: 7` whose history has non-UTF-8 and deep lines, and a non-JSON board. Result: 0 new files and 0 changed files. See SR-1 for the one edge. | executed |

## Findings

### SR-1 — `N` (and `A`) can write a `board.json.corrupt` sidecar  [LOW · design-gap, inherited]
- **What:** `peek_board` checks readability with `json.loads` only (`boards.py:621-624`). `Board.load` then runs `clean_strings` (`models.py:1042`), which is plain Python recursion with a limit of 1 000. A file nested between about 1 000 and the C decoder's limit parses but fails the cleaning, so `Board.load` writes `board.json.corrupt` through `_quarantine_corrupt_file` (`models.py:1048`).
- **Seen:** at depths 1 100 and 1 400, the home already writes the sidecar at start. If the sidecar is gone when `N` or `A` opens (the file turned corrupt after start, or the user removed the sidecar), `N` or `A` writes it again. That breaks LLR-4302.6 in this edge. TC-4317 cannot see it, because it hashes four named files (`tests/test_added_list.py:857-862`), not the tree.
- **Risk:** low. The write is a byte copy of the user's own file, placed beside it. Nothing is lost and nothing leaves the machine. But the docstring of `peek_board` ("A board read without writing") is false in this case.
- **Fix (backlog, beside L-BL-3):** put `clean_strings` inside `peek_board`'s guarded check, or give `Board.load` a no-quarantine mode for peeks. Widen TC-4317 to hash the whole tree.

### SR-2 — the mention scan is still unbounded by note length  [LOW · design-gap, ruled A-6 / L-BL-4]
- **What:** `_added_meta` calls `mention_names(t, people)` over the uncut note on every paint (`views.py:9547`).
- **Seen again on the shipped code:** 5 MB `@ana lorem ` costs 198 ms per paint; 5 MB of `@` costs 75 ms.
- **Risk:** a crafted board makes the list sluggish. There is no crash and no effect on data.
- **Fix:** as ruled (L-BL-4): compute the mentions once per cursor change. Nothing more is owed in this increment.

### SR-3 — `enter` on a non-str-id task crashes the app on the board switch  [LOW · design-gap, inherited]
- **What:** SEC-3 holds inside the list: the odd-id task is listed and drawn. But `enter` → `open_on_board` → `switch_board` → `_migrate_links` → `run_link_migration` raises `TypeError: unhashable type: 'list'` (`app.py:1714`), and the app exits.
- **Seen:** the same board, opened at start, already crashes in the base `render_swimlanes` (`views.py:1898`). So this is base behaviour that `N` now gives one more way to reach (as the home and `A` already do).
- **Risk:** the app exits on a hand-crafted file. The probe found no data change. Not a confidentiality issue.
- **Fix (backlog):** normalise the id at the load door. In `Task.from_dict` (`models.py:949`), turn a non-str id into a fresh id and keep the raw value in `extra`, so every view is safe, not only the list.

### SR-4 — bidi and zero-width characters reach the list  [LOW · design-gap, inherited]
- **What:** `strip_controls` keeps every code point from U+00A0 up (`models.py:525-535`). U+202E (RLO) and U+200B in a title or note reach the list rows and the pane. The probe confirmed both are kept.
- **Risk:** in a terminal that applies bidi, a title could be shown spoofed. This is the same in every base view, and it is not new to this increment.
- **Fix (backlog):** drop the bidi controls U+202A–U+202E and U+2066–U+2069 in `strip_controls`.

### SR-5 — the backlog items named by the rulings are not in the backlog  [LOW · impl (process)]
- **What:** `03-pdr-rulings.md` and `e4-addenda.md` A-6 name L-BL-2, L-BL-3 and L-BL-4. `.dev-flow/BACKLOG.md` holds none of them at `79cf2b2`.
- **Risk:** the deferred mitigations for SEC-2's source fix, SEC-5 and SEC-R2-1 can be lost at close.
- **Fix:** before the batch closes, write L-BL-2..4 and SR-1, SR-3 and SR-4 into `.dev-flow/BACKLOG.md`.

## Evidence checklist
- ✓ Each finding has what, where, why and a fix: SR-1..SR-5 above.
- ✓ Each finding has a severity and a tag: all five are LOW; four are design-gap (SR-2 already ruled) and one is impl.
- ✓ No secret values appear in this output: the diff scan for keys, tokens and personal data found none, and the fixtures use `username_subject`.
- ✓ The verdict is explicit: PASS-WITH-NOTES. There is no HIGH. The SEC-1..4 mitigations are applied and were verified by me (`executed`).
- ✓ No new tool or integration is added. No new data leaves the machine: `created` stays out of `board.<user>.json`, and only the local board file holds it.
