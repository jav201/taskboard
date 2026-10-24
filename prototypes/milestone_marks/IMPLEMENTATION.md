# Milestone marks — implementation commission

Written by the orchestrator on 2026-10-24 for batch `2026-10-24-batch-01`. Branch `feat/milestone-marks` starts from `proto/milestone-marks` (`8c83395`), which sits on `main` `ffb567d`.

## 1. The operator's request and verdict (verbatim)

The request:

> «Necesitamos tener marcadores de figura y color para los milestones... me doy cuenta que hay veces que necesito clasificarlos y esto me ayudaría. Por favor prototipemos primero»

The verdict on `prototypes/milestone_marks/milestone-marks.html`:

```
D1: B
D2: global (recomendada, sin marcar)
1 model: B
2 editor: A (recomendada, sin marcar)
3 legend: B
4 filter: B
notes: (none)
```

The design is the round. `proto.py` holds every chosen variant:

- the variant-B branch of `mark_key`
- `gantt_milestone_cells_m`
- `band_milestone_facts_m`
- `agenda_row_m`
- `legend_strip` and `legend_strip_project`
- `_hide` and `present_tasks_m`
- `matches_m` and `filter_bar_m`
- the editor's variant A, the `alt+m` Select in `#task-chips-what` after `#f-milestone`
- the `#` class manager window

Port these into the real app. The captures in `out/` are the visual oracle for each frame.

## 2. Decisions

Each decision is recorded in the plan with its reason.

- **MM-D1, the encoding (verdict D1 B).** Every milestone, classed or not, follows these rules:
  - Shape and colour say the class. An unclassified milestone keeps `◆` in the neutral `mut` tone.
  - State moves to text. When late, the date beside the mark turns `over` and a chip `▲Nd` follows. When reached, the mark is drawn hollow (`HOLLOW` map in `proto.py`) plus `✓` in `reached`.
  - The round recorded the known costs, and they are accepted:
    - the gantt month ruler shows no lateness;
    - an unclassified milestone loses its red mark;
    - a class colour can resemble a project colour.
- **MM-D2, scope (verdict D2 global).**
  - **Store.** One class directory for all boards, at `~/.taskboard/marks.json` beside `people.json`. It is written exactly like `taskboard/people.py`'s `Directory`: read-modify-write under `boards.file_lock`, an atomic write, and `keep_aside` on an unreadable file.
  - **A class.** A class is `{"id", "name", "shape", "colour", "hidden": false}`.
  - **Ids.** The id is a slug of the name, as `people.handle_for` makes handles. It stays stable on rename.
- **MM-D3, the task field.**
  - **The field.** Add `Task.mark: str | None = None`, the class id. It is written only when set, so a board with no marks keeps its bytes (the `show_in_present` pattern in `Board._to_dict`). It is meaningful only on a milestone.
  - **Unknown or deleted ids.** An unknown id, such as a deleted class or a teammate's class, renders as unclassified `◆`. It is never dropped.
  - **Clearing a milestone.** Unticking `milestone` keeps the field, so the class comes back if the box is ticked again.
  - **Team sync.** The field travels unchanged.
- **MM-D4, no seeded classes.** `marks.json` starts empty. Classes are the user's own. The round's four examples (Delivery, Payment, Review, Launch) live only in test fixtures and captures.
- **MM-D5, the shapes.** The manager offers the round's verified one-cell set `SHAPES = ▲ ■ ⬢ ★ ⬟ ▼ ✦ ⚑`, plus `◆`.
  - `●` is excluded: it is the gantt's progress dot.
  - Wide or ambiguous glyphs are excluded: `◉ ♦ ⬤ ⬛ ⭐`.
  - Log in BACKLOG that `▲` as a class glyph sits next to the `▲Nd` late chip and the `▲N ◆` fold row (the round's own note). This is not to be fixed now.
- **MM-D6, hide/show (verdict 4 B).**
  - **Where it is set.** In the `#` window, `space` toggles a class's `hidden` flag, persisted in `marks.json` like the presentation's saved order.
  - **Effect.** Hidden classes leave the gantt and the presentation (all three views and their exports).
  - **The legend.** The legend strip says how many classes are hidden.
  - **Search.** The cheap extra from the round, `/#pay` in search, filters tasks by class (`matches_m`).
- **MM-D7, legend (verdict 3 B).**
  - **Placement.** A strip under the ruler in the gantt and in the presentation, with its exports. It lists only the classes drawn in the frame, and none when no classed milestone is in view.
  - **The `?` help.** It names the classes too.
- **MM-D8, keys (the operator's standing standard).**
  - **Modal buttons.** Every modal button gets a direct key that is shown on screen: `y`/`n` in confirmations, `alt+<letter>` beside text fields. `tests/test_modal_keys.py` must cover the `#` manager and its form.
  - **`#` in the main keymap.** It opens the manager. Check that it is free in `taskboard/keymap.py`.
  - **`alt+m` in the editor.** It focuses the class Select, and it joins `TASK_KEYS`.

## 3. Only milestone markers change

`◆` is also a title glyph (`◆ GANTT`, `◆ TASKBOARD`, `◆ FOCUS`, `◆ CHAIN MAP`, the modal headings) and a project-span due mark (`views.py` around lines 2613, 3030 and 3044, `sel_p.color`). **Those stay as they are.**

Change only the milestone sites. In `views.py` today, they are around:

- lines 1107/1113 and 1677/1689 (lanes and focus);
- line 1800 (the bank edge, if it is a milestone);
- line 2037 (kanban/focus glyph);
- lines 2541, 2554, 2643, 2732, 3035, 3078 and 3615;
- the band rule facts, around 5069–5099 and 5310;
- the presentation field row, around 6538;
- the agenda (`A`), the people view, and `app.py`'s notices at 2133/2172/2433 when they show a milestone mark.

Route them all through ONE seat, for example `views.milestone_mark(task, board, today) -> (glyph, style, late_chip)`, so that no site encodes MM-D1 on its own. A test enumerates the sites, so a new frame cannot skip the seat.

## 4. Increments

Each increment touches at most 4 SOURCE files. Tests are uncapped.

| # | Content | Source files (expected) |
|---|---|---|
| 001 | The store and the field. Covers MM-D2, D3 and D4. | `taskboard/marks.py` (new), `models.py`, `app.py` (load it beside `people`), `__main__.py` only if needed |
| 002 | The encoding through one seat. Covers MM-D1 and section 3, in every view. | `views.py`, `app.py` (notices) |
| 003 | The editor Select (verdict 2 A) and the `#` manager with its form and hide toggle. Covers MM-D5, D6 storage and D8. | `modals.py`, `keymap.py`, `app.py`, `taskboard.tcss` |
| 004 | The legend strip (MM-D7) in the gantt, presentation and exports. Hidden classes leave the gantt and presentation (MM-D6). `/#…` search. The `?` help, details line and README. | `views.py`, `app.py`, `README.md` |

## 5. Acceptance

Each acceptance test (AT) has exactly one node. All of them are driven by keys where a user would use keys.

- **AT-a, a class is created and survives.**
  1. In `#`, create a class with `n`, a name, a shape and a colour.
  2. Give a milestone that class with `alt+m` in the editor.
  3. Restart the app.

  The class persists in `marks.json`, and the gantt draws the class glyph in its colour.
- **AT-b, the state shows in text.**
  - A late classed milestone shows its date in `over` plus `▲Nd`.
  - A reached one shows the hollow glyph plus `✓`.
  - An unclassified one shows `◆` in `mut`.
- **AT-c, the store is safe.**
  - **Two windows.** Each adds a class, and both survive (read-modify-write).
  - **Unreadable file.** An unreadable `marks.json` is set aside, never overwritten.
  - **Bytes.** A board with no marks keeps its bytes.
- **AT-d, hide and the legend.**
  - Hiding a class in `#` removes its milestones from the gantt and from all three presentation views and their exports.
  - The legend strip lists the drawn classes and the hidden count.
- **AT-e, search.** `/#pay` filters to that class.
- **AT-f, modal keys.** The modal-key law covers the new modals.
- **AT-g, an unknown id is safe.** A task whose `mark` is unknown renders as unclassified, and the id is kept on save.

## 6. Evidence

- **Captures.** Real full-colour Windows Terminal PNGs of each shipped item at 118x30 and 80x24, using the round's harness (`shoot.ps1`).
- **Capture-window rules.**
  - Each window has a unique `m01-` title, and is closed by title right after its shot.
  - At the end, assert that no `m01-*` window remains. Never close any other window.
  - Launch with `cmd /c 'set NO_COLOR=& set COLORTERM=truecolor& wt.exe -w new --title <t> ...'`.
  - Reject black, fewer-than-8-colour, or wrong-end-state shots, and retry.
- **Tests.** Unset `NO_COLOR` before pytest.
- **Full suite.** The baseline is 3152 passed. Run it in 3 SEQUENTIAL chunks, never in parallel with captures or another suite, with transcripts in the batch evidence.
- **Validator.** At start and at close, `--brief` with 0 BLOCK.
- **Mutation.** Every new test is mutation-checked.
