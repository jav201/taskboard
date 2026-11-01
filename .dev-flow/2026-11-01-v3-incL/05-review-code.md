# Inc L — E5 independent code review — code-reviewer

**Verdict: PASS-WITH-NOTES.** There is no MAJOR or HIGH finding. The 6 MINOR findings below do not block (4 are `impl`: CR-2..CR-5; 2 are `design-gap`: CR-1 and CR-6). The code implements the approved design as ruled in `03-pdr-rulings.md` and `e4-addenda.md` (A-1..A-6). I found no behaviour that departs from `graph-interfaces.cw.md` or the S/V/D group graphs. In the role file's tokens this is *OK to advance*, with notes.

## Scope reviewed

- **Diff.** `git diff eb411e1 7bac31f -- taskboard/ README.md tests/`: 8 files, +3000/−19. I read the whole diff:
  - `taskboard/models.py` (60 lines changed): `stamp`, `Task.created`, `from_dict`, `_to_dict`, `_serialized`, the seed branch and `add_task`.
  - `taskboard/views.py:9255-9680`: the added-list block.
  - `taskboard/app.py`: `AddedList` at :965-1060, `check_action` at :1390-1410, `action_added_list` and the template stamp at :2121-2130.
  - `taskboard/keymap.py:144-147`.
  - `README.md:136` and `:331`.
  - All of `tests/test_task_created.py`, `tests/test_added_list.py` and `tests/added_list_fixture.py`.
- **Commit check.** HEAD `79cf2b2` is the same as `7bac31f` for `taskboard/` and `tests/`, checked with `git diff --quiet`.
- **Context I read.** `01-requirements.md` (69 active LLRs), `graph-interfaces.cw.md`, the node contracts of `graph-proto-S.cw.md`, `03-pdr-rulings.md`, `e4-addenda.md`, `evidence/green-*.txt` and `guards-1.txt`. For the census I also read these unchanged neighbours: `history.append`/`read`, `board_lanes`, `open_on_board`, `jump_to`, `_bring`, `_on_task_added`, `_on_task_edited`, the undo re-insert, `TeamState.push`/`foreign_tasks`, `_rescue_task` and `snapshot`/`restore`.
- **Probes (read-only).** I ran these with `C:/Users/jjgh8/anaconda3/python.exe`. `taskboard.__file__` = `...\taskboard-wt\capture-proto\taskboard\__init__.py`.
  - `env -u NO_COLOR pytest tests/test_task_created.py tests/test_added_list.py tests/test_keymap.py`: **118 passed** (`executed`).
  - Scratch probes in `%TEMP%\probe_l*.py`, outside the repo: TC-4332b paint time, the first-birth edge (CR-1), and `render_added_list` at widths and heights 10x3, 40x1, 36x5, 1x1 and 0x0, plus `sel=99`. Every size and selection rendered with the right line count and no exception (`executed`).
- **Not my lane.** Mutants (another job, `incL-mut`, not touched), the suite as a whole (qa), and security (SEC-* were closed at PDR).

## Creation-path census (asked explicitly)

| Path | Where | Stamps? | Evidence |
|---|---|---|---|
| Task editor `a` | `app.py:3511` `Task(**data)` → `Board.add_task` | yes, in `add_task` (`models.py:1303-1309`), before `save()`, one clock read shared with the birth `at` | TC-4302, TC-4305, AT-4302 |
| Link picker create row | `app.py:2675` → `add_task` | yes | TC-4304 |
| Template insert `I` | `app.py:2124-2130`, `when = stamp()` once, after the empty-template refusal | yes, one value | TC-4303 (advancing clock), AT-4303 |
| Seeded first board | `models.py:1030-1034`, one `stamp()` in the seed branch | yes, one value | TC-4306 |
| `Board.add_task` with a `created` already set | kept | n/a | TC-4307 |
| Edit, project move (deepcopy), undo re-insert (same object), rescue | unchanged code; no `Task(` and no stamp | keeps or None | TC-4308..4311 |
| Team `foreign_tasks` (`team_sync.py:221`) | `from_dict` for display only, never appended to a board | n/a (not persisted) | read |
| `views.py:7497` `Task(title="")` | a gantt span proxy, never persisted | n/a | read |

No other `Task(`, `tasks.append/insert/extend` or `from_dict` site exists in `taskboard/`. `grep` covered every module; there is no subpackage. **Nothing rewrites old tasks.** `created=None` is dropped in `_to_dict`, a non-str value round-trips through `extra`, and no code path back-fills (TC-4315 ×3, TC-4316). **The list writes nothing.** `compose`/`_paint`/actions only read: `board_lanes` uses `peek_board` and `added_rows` uses `history.read`. Writes after `enter` come from `switch_board`, which runs after `open_on_board` has popped the list (TC-4317, AT-4301 and AT-4305 hash both boards and both histories). **The team push** leaves `created` out through the default `with_created=False`, and `_serialized` is the only save serializer (`models.py:1104-1119`). `_to_dict` has no other caller (TC-4318).

## Textual behaviour (asked explicitly)

- **Bindings.** The screen's priority `escape,N`, `o`, `v`, `enter`, `up,k`, `down,j` win over the App's non-priority `N`/`o`/`v`/`enter`. App priority arrow bindings are refused by `check_action` (the holding tuple), and lookup then falls through to the screen's bindings, so TC-4334 passes (`executed`).
- **`check_action`.** `added_list` is gated by the modal test before the seat test, as `A`/`@`/`#` are, and `AddedList` is in the holding tuple (TC-4341, TC-4342).
- **Screen stack.** `_bring(AddedList, AddedList)` brings back the same instance. The list's `N` pops it (TC-4323, TC-4324 ×2, TC-4342).
- **Resize.** `on_resize` repaints; `lw` follows `w − 2` (TC-4327 pilot with `resize_terminal`).
- **Resume.** `on_screen_resume` repaints without re-reading the snapshot (A-1, TC-4331b). It also fires on the first push, which is harmless: compose has finished by then and the pilots show no exception.

## Findings

### CR-1 — An invalid first birth record hides a later valid one  [MINOR · design-gap · `executed`]

- **Where:** `taskboard/views.py:9345-9347` (`births.setdefault(r["task"], r["at"])`, validated afterwards at :9353).
- **What:** `added_rows` keeps the FIRST birth record per id and only then checks it with `added_moment`. If that first record's `at` is offset-aware or unparseable, the task becomes `?`, even when a later birth record is valid. Probe: births `2026-10-28T10:30:00+00:00` then `2026-10-29T10:30:00` gave `[('?', None)]`.
- **Why:** LLR-4304.13 says "a birth `at` with an offset → not a birth". Read literally, the next birth record should then count (source `h`). The graph-interfaces `added_rows` func specifies "first, then validate", so the code follows the design, and the two texts disagree. The impact is negligible: the app writes only naive stamps, so only a hand-edited history reaches this.
- **Fix (choose one, then record it):** (a) count only valid births: `if r.get("from") is None and isinstance(r.get("task"), str) and added_moment(r["at"]) is not None: births.setdefault(r["task"], r["at"])`, plus one arm in TC-4373; or (b) keep the code and amend LLR-4304.13's threshold to "the first birth record decides; an invalid one gives `?`".

### CR-2 — The `check_action` comment does not name `N`  [MINOR · impl · `executed`]

- **Where:** `taskboard/app.py:1399-1401`.
- **What:** The docstring now names `added_list`/`N`, but the inline comment right under it still reads "so `A`, `@` and `#` never reach past one".
- **Why:** The comment disagrees with the line it annotates, which now holds four actions.
- **Fix:** Change it to "`A`, `@`, `#` and `N` never reach past one", and add Inc L to the batch list.

### CR-3 — The `views.py` header says "seven" interface nodes but lists six  [MINOR · impl · `executed`]

- **Where:** `taskboard/views.py:9264-9266`.
- **What:** "The seven interface nodes (`added_rows`, `added_moment`, `added_order`, `first_created`, `state_boxes`, `render_added_list`)" names six.
- **Why:** The count does not match the list. `AddedRow` is the `[Data:]` entity, not a node.
- **Fix:** "The six interface nodes (…) and the `AddedRow` entity".

### CR-4 — TC-4306 asserts the same count twice  [MINOR · impl (test) · `executed`]

- **Where:** `tests/test_task_created.py:215` and `:219`.
- **What:** `_text(path).count('"created":') == 16` appears twice. The second copy adds nothing: no write happens between them.
- **Fix:** Delete line 219. If a re-read was intended, replace it with a check that a second `Board.load(path)` keeps the 16 values.

### CR-5 — TC-4332b's cut-before-wrap oracle is wall-clock only  [MINOR · impl (test) · `executed`]

- **Where:** `tests/test_added_list.py:577-592` (`best < 0.05`).
- **What:** The `… more lines` assertion cannot catch a mutant that wraps the WHOLE note and still reports `cut`; only the 50 ms timing arm does. I measured the shipped paint at 0.8-2.6 ms (min of 10) against the 0.92 s uncut wrap. That is a ~20-60× margin, so flake risk is low but not zero under coverage or a loaded runner. The oracle is also indirect.
- **Why:** SEC-4/A-3 promise that "at most `room × (rw + 1)` characters reach `notes_text`". That is a deterministic contract, and the test can check it directly.
- **Fix:** Add a spy arm, `monkeypatch.setattr(views, "notes_text", spy)`, recording `len(text)`, and assert `≤ (room − header lines) × (rw + 1)` (≤ 27 × 68 at 116x29). Keep the timing arm as a secondary check, optionally loosened to ~0.2 s, which is still 4× below the uncut cost.

### CR-6 — The home's key row does not name `N`  [MINOR · design-gap · `executed`]

- **Where:** `taskboard/views.py:7708` (`HOME_KEYS` names `A all boards`). `README.md:331` now documents `N` on the home.
- **What:** `N` works on the home (TC-4324b), and the README home table lists it, but the home's own key row does not. P-D-9 covered the README only.
- **Why:** This is discoverability only: `A`, its sibling, is shown on the home. No LLR asks for it, so this is not an impl departure.
- **Fix:** No change this increment. Backlog it, or decide in a later UX pass whether `N added` joins `HOME_KEYS`. `home_keys` already drops words first at 80 columns.

## Notes (not findings)

- **N-1, the `_to_dict(with_created=False)` default.** It is fail-unsafe for any future save path that forgets the flag: `created` would be silently dropped, and it is never back-filled. This was ruled at PDR (SEC-1, A-5) to keep `team_sync.py` out of the 4-file budget. The docstring states the rule, and TC-4312/TC-4305 pin the current `_serialized` path. A backlog idea: make the flag keyword-only with no default, and have `TeamState.push` pass `with_created=False` the next time `team_sync.py` is touched.
- **N-2, the open board's lane holds the live `app.board` objects.** That matches `board_lanes`' agenda contract and is harmless while the list holds the seat; every `enter` path pops the list first.
- **Simplicity and reuse.** The code reuses `board_lanes`, `open_on_board`, `jump_to`, `_bring`, `key_line`, `fit`/`clip`/`vis`, `_md`, `notes_text`, `mention_names`, `milestone_mark`, `project_color`, `board_hex` and `_SEARCH_CONSOLE`. The scroll formula repeats the agenda's one-liner (`views.py:7857`), and I would not factor it. No dead code: every new import and name is used, and `AddedRow.bcolour`/`bname` feed the pane. Every user-visible string is built as `Text` pieces (spans, not markup). The E4 seam fix (`Text.assemble` for headers) is right: a base style on the left `Text` would run on into the separator and the pane appended to it.
- **Test intent.** Each TC's docstring names its LLR, the reason it matters, and its NC. The NCs are reachable: hand-shuffled inputs (ARCH-1), the advancing clock (P-D-10), the history birth to back-fill from (ARCH-2), the direct `check_action` arm (P-S-1), and exact 29- and 23-line captures with per-cell colour and bold checks. I found no vacuous asserts. TC-4315 and TC-4316 are declared guards that pass on base. Pilot waits are `pilot.pause()` plus a 0.3 s settle in `open_list`, with no assertion on elapsed time. TC-4332b is the only timing-based assert (CR-5).

## Evidence checklist

- ✓ Diff read in full: `models.py`, `views.py:9255-9680`, `app.py:840-1060`, `:1390-1410`, `:1540-1546`, `:2121-2130`, `keymap.py:144-147`, `README.md:136` and `:331`, and the 3 test files end to end.
- ✓ Correctness pass: the census table above; edge sizes, `sel` clamp, empty list, non-str id and unreadable history probed. One spec ambiguity found (CR-1).
- ✓ Simplicity pass: no premature abstraction, and helpers are single-purpose (Notes).
- ✓ Reuse checked against existing utils (Notes). No re-implementation found.
- ✓ Tests reviewed for intent: CR-4 and CR-5 are the only weaknesses.
- ✓ Verdict explicit: PASS-WITH-NOTES. No HIGH was found, so none needs applied-and-verified evidence.

## §4b `Independent review` cell

`code-reviewer` · OK to advance (PASS-WITH-NOTES: 0 MAJOR, 0 HIGH, 6 MINOR — CR-1 and CR-6 design-gap, CR-2..CR-5 impl) · no HIGH to resolve
