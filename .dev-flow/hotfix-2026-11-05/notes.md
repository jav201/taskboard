# Hotfix 2026-11-05 — notes

Branch `fix/hotfix-chain-move-paste`. Three operator-driven hotfixes, diagnose →
fix → test → commit. Diagnosis: `hf3-diagnosis.md` in this folder.

## HF-1 — `C`: the critical chain off/on

- New key on the seat (`taskboard/keymap.py`): `C → chain_toggle`, primary layer,
  scoped to the gantt and the chain map (the only views that draw the chain), so
  the bar and `?` name it exactly where the operator looked for it. `c` stays the
  Clocks modal; no other seat key uses `C`.
- State on the board (`taskboard/models.py`): `Board.chain_shown()` /
  `Board.set_chain_shown(on)` — `settings["critical_chain"] = "off"` is the only
  stored form; on pops the key. Default on: a never-toggled board file gains no
  setting and renders byte-identically.
- Draw sites gated in `taskboard/views.py`: the gantt frame, the chain map's
  plan, and both presentation views take an empty chain set when off — which
  removes the heavy `━` reach, the `crit` tone on bars and marks, and the
  `chain N` head/footer counts automatically. The gantt legend, the chain map's
  legend row and the `?` legend say `chain off · C` instead of listing the chain.
- Toast: `Critical chain off · C turns it on` / `Critical chain on · C turns it
  off` — the key is named both ways because discoverability was the defect.
- Not done, per the brief: the pin, the picker, the state band (they belong to
  `feat/critical-chain`).

## HF-2 — `O`: one task to another board

- `taskboard/keymap.py`: `O → task_move_board`, primary layer, live wherever a
  task can be selected (the `L` scoping), shown on the bar and in `?`.
- `taskboard/boards.py`: `task_move_plan` + `move_task` — the project move's
  machinery one task wide: same folder/team/id/image/phase guards, same lock +
  stale-stamp check, same backup order (byte copies → target save → source
  save), images folder moved and references re-pathed, history lines moved,
  `move-DAY.json` written beside both boards with `links_dropped`. The task
  arrives with title, notes, images, `created`, mark/milestone and dates, under
  the chosen project or Inbox. `u` cannot undo it (the confirm says so, and
  `after_move` clears the undo stack, as for a project move).
- `taskboard/modals.py`: `MoveTarget` now takes a display name+colour (a project
  or a task — its only two callers updated); new `MoveProjectTarget` picker
  (Inbox first, then the target's projects); `MoveConfirm` gained `what="task"`
  (head, counts and the crossing-links "where" line adapt; the `y`/`n` keys, the
  backups sentence and the undo line are unchanged).
- `taskboard/app.py`: `action_task_move_board` → `_task_move_target` →
  `_task_move_project` → `_task_move_confirmed`, mirroring the manager's project
  flow; both new keys are guarded from firing behind a pushed screen.

## HF-3 — copy and paste, the OS clipboard, in the notes and the pad

Root causes (full detail in `hf3-diagnosis.md`): the capture pad had **no**
paste binding, and Textual's native paste reads the app-local clipboard, which
starts empty — so pad paste was impossible. And nothing ever **wrote** the OS
clipboard: Textual's `copy_to_clipboard` is an OSC 52 escape that Windows
Terminal drops, so ctrl+c out of the notes/pad went nowhere. The editor's own
ctrl+v already read the OS clipboard via `grab_clipboard_text` (that path is
unchanged).

- `taskboard/models.py`: `stash_clipboard_text` — the write-side twin of
  `grab_clipboard_text` (Win32 `SetClipboardData` via ctypes with explicit
  64-bit handle types; `pbcopy`/`xclip -i` fixed argv elsewhere; never raises).
- `taskboard/modals.py`: `ClipboardPasteMixin` gained `action_copy_text`; the
  editors (Task, Project, Clock) bind `ctrl+c` beside their `ctrl+v`, so both
  keys go through the OS clipboard and the TextArea's native OSC-52 copy no
  longer wins.
- `taskboard/app.py`: the capture view binds `ctrl+v`/`ctrl+c` with the same two
  actions; the hint row and the key row name them.
- Known limitation, documented in the diagnosis: while the colour palette (a
  pushed screen) is open, ctrl+v/ctrl+c are inert — recolouring and pasting are
  different moments. The pen does not swallow paste (it is lifted first, E5 CR-2).

## Tests added — `tests/test_hotfix_2026_11_05.py` (13)

Each names its RED-before state in the docstring:
HF-1: the setting defaults on and round-trips through save/load; `C` is on the
seat exactly where the chain is drawn; off removes the chain from the gantt,
chain map and presentation (styled-span check there, because the ruler's `⟦━⟧`
echo is not the chain); black-box `C` toggle → setting → toast → chart → `?`
band. HF-2: the plan lists both crossing-link directions and every refusal;
`move_task` carries everything (notes spans, images re-pathed, created, mark,
dates) and drops links with backups, history move and logs on both sides;
black-box `O` through the three screens to a real project, undo stack cleared;
a team-shared task refused with the reason. HF-3: ctrl+v pastes OS text into
the pad; ctrl+c copies the pad's selection out; the editor's ctrl+c writes the
OS clipboard and its ctrl+v still pastes; a win32 round-trip through the real
clipboard (restoring what it found).

## Old tests updated, and why

- `tests/test_modal_keys.py` — INVENTORY gains `MoveProjectTarget` (keys-only
  modal; the law demands the table and the package agree both ways). The
  MoveConfirm `y`/`n` law test is unchanged and still green.
- `tests/test_colour_budget_app.py` — `KEYBAR_BASE` gantt pins (80 primary,
  118 more) re-fitted per the seat's own law: `O` and `C` joined the primary
  layer ("Quit" sheds its word; every key stays) and the more layer at 118
  (words were already all gone, so the overflow count grows +3 → +5). Recorded
  with the same evidence-style comments as the previous additions.
- `tests/test_capture_view.py` — the pad's own key list (`CAPTURE_KEYS`), the
  `HINT` row, and the TC-4410 exact-row pin: the pad gained the ctrl+v / ctrl+c
  pair, so the row now names nine keys (two words lawfully shed at 118). The
  app-side constants move with the app; the assertions follow the fit law.
- `tests/test_report_export_app.py` — TC-3117's wide arm: `O` joined the
  primary layer, so under the fit law the bar sheds words further right and
  `H Report` first fits at 207, not 193; the wide arm now paints at 210
  (verified against `key_bar_plain`, the same law the test cites).
- `README.md` — the key table gains `C` (Chain) and `O` (Move board); the
  capture row names the clipboard pair; the editors' line names Ctrl+C. The
  seat's README law (`test_the_readme_keybinding_table_matches_the_seat`) and
  TC-4413 drive these.

No legend test needed changing: with the setting absent the drawings are
byte-identical, which is exactly what the existing gantt/chainmap legend pins
now prove.

## Verification

Law guards + hotfix tests green; full suite in three sequential chunks,
transcripts in this folder (`suite-chunk-{1,2,3}.log`).

- `never-saved.json` (2026-11-05, Sonnet finishing pass): `test_HF1_off_takes_the_chain_out_of_every_drawing` saved a board to `Path("never-saved.json")` in the cwd; it now uses `tmp_path / "board.json"`, and the stray file was deleted.

- **Full suite (orchestrator, 2026-11-05):** chunk00 1906 passed + 1 failed, chunk01 1199 passed, chunk02 1099 passed. That is 4204 passed and 1 failed. The failure is `tests/test_app.py::test_win_clipboard_roundtrip`, a known machine-global clipboard flake whose own docstring records "failed once inside a full suite run and passed 3/3 in isolation". Re-run alone afterwards it passed 7 of 8, with one more contention failure. The hotfix touches clipboard code (HF-3), so the push decision notes this, and the CI run is checked after any push.
