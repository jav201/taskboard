# E5 mutants — Inc L new arms (mechanical task)

Run each mutant below in the COPY `C:/Users/jjgh8/Github/taskboard-wt/incL-mut` (a detached worktree of
`7bac31f`). NEVER edit the main worktree `capture-proto` except to write the result file named at the end.
Interpreter: `C:/Users/jjgh8/anaconda3/python.exe` (never the shell's `python`). Run every pytest with
`env -u NO_COLOR`, cwd = `C:/Users/jjgh8/Github/taskboard-wt/incL-mut`, and first print
`taskboard.__file__` once to prove the copy is imported.

For each mutant: apply the ONE edit to the copy's source, run
`env -u NO_COLOR C:/Users/jjgh8/anaconda3/python.exe -m pytest -q -x -p no:cacheprovider tests/test_task_created.py tests/test_added_list.py tests/test_keymap.py`,
record KILLED (≥ 1 failure; give the first failing test id) or SURVIVED, then restore the file with
`git -C C:/Users/jjgh8/Github/taskboard-wt/incL-mut checkout -- <file>` and confirm `git -C … status --short`
is empty before the next mutant. If an edit cannot be applied as written (the code differs), apply the
closest equivalent and say what you did in Notes.

| M | Where | Edit |
|---|---|---|
| M01 | models.Task | give `created` a `default_factory` that returns `stamp()` |
| M02 | models.Board.add_task | remove the `task.created = stamp(now)` line |
| M03 | models.Board.add_task | stamp unconditionally (drop the `is None` check) |
| M04 | models.Board.add_task | move the stamp after `self.save()` |
| M05 | models.Board.add_task | call `history.append` without `at=now` |
| M06 | models.Board.load (seed branch) | remove the seed stamping |
| M07 | models.Board.load (seed branch) | call `stamp()` once per task instead of once (inside the loop) |
| M08 | models.Board._to_dict | always write `created` (do not delete it when None) |
| M09 | models.Board._to_dict | ignore `with_created` (keep `created` on the push path) |
| M10 | models.Board._to_dict | do not pop `extra["created"]` on the push path |
| M11 | models.Board._serialized | call `_to_dict` without `with_created=True` for tasks |
| M12 | models.Task.from_dict | drop a non-`str` `created` instead of keeping it in `extra` |
| M13 | models._rescue_task / from_dict | set `created=stamp()` on the rescued task |
| M14 | app._on_template_picked | remove `created=when` (no stamp on template insert) |
| M15 | app._on_template_picked | `created=stamp()` per task inside the loop |
| M16 | app.check_action | remove `"added_list"` from the modal-gated tuple |
| M17 | app.check_action | remove `AddedList` from the screens that hold the seat |
| M18 | app.AddedList.__init__ | `show_archived = self.app.show_archived` (inherit) — or `True` if `self.app` is not reachable there |
| M19 | app.AddedList.action_order | keep `sel` instead of resetting it to 0 |
| M20 | app.AddedList.action_archived | always reset the cursor to 0 |
| M21 | app.AddedList BINDINGS | remove `N` from the back binding (`escape` only) |
| M22 | app.AddedList.action_jump | remove the `if not rows: return` guard (or equivalent empty guard) |
| M23 | app.AddedList.on_screen_resume | delete the method |
| M24 | views.added_moment | accept offset-aware values (return them with tzinfo stripped) |
| M25 | views.added_moment | `except ValueError` removed (unparseable str raises) |
| M26 | views.added_rows | use the LAST birth record per id instead of the first |
| M27 | views.added_rows | narrow the history guard to `except OSError` |
| M28 | views.added_rows | drop the `isinstance(task.id, str)` check before the births lookup |
| M29 | views.added_rows | prefer the birth record over a valid `created` |
| M30 | views.added_order | sort dated rows by `at` only (no lane/pos tie-break) |
| M31 | views.added_order | put unknown rows after dated rows in oldest-first order |
| M32 | views.added_order | do not filter archived rows when `show_archived` is False |
| M33 | views.first_created | include source `"h"` rows in the minimum |
| M34 | views.state_boxes | exclusive fill (`i` boxes instead of `i + 1`) |
| M35 | views.state_boxes | no 8-box cap (draw `n` boxes when n > 8) |
| M36 | views._added_row | no padding of the state column to the widest count |
| M37 | views._added_row | state-column filled boxes in `HEX["sky"]` instead of `HEX["ink"]` |
| M38 | views._added_row | archived title not dimmed (use the normal title style) |
| M39 | views.added_time_label | drop the `≈` prefix for source `h` |
| M40 | views.added_source_line | omit ` · #<n> in <board>'s board file` for source `?` |
| M41 | views._added_plan | no ` ≈` suffix on a history-only day |
| M42 | views._added_head | omit the `archived hidden` / `archived shown` tail |
| M43 | views._added_pane | render notes with `Text(task.notes)` instead of `notes_text` |
| M44 | views._added_pane | omit the `after:` line |
| M45 | views._added_pane | build the `after:` lookup over all ids (no str filter) |
| M46 | views._added_pane | no note cut before the wrap |
| M47 | views.render_added_list | `lw = 46` at every width |
| M48 | views._added_top | always `top = 0` (no scroll window) |
| M49 | views._one_line | return the text unchanged (no flattening) |
| M50 | keymap.KEYMAP | remove the `N` entry |

Write the table to `C:/Users/jjgh8/Github/taskboard-wt/capture-proto/.dev-flow/2026-11-01-v3-incL/05-mutants.md`
as `| M | Where | Edit applied | Req | Result | First failing test / Notes |` (Req = the LLR the mutant
attacks; find it in `.dev-flow/2026-11-01-v3-incL/01-requirements.md` by the NC lines), then a totals line
`killed K / N`, and save the full transcript of all runs to `.dev-flow/2026-11-01-v3-incL/evidence/mutants-run.txt`.
At the end the copy must be clean (`git status --short` empty). Return ≤ 6 lines: totals, every SURVIVED id.
