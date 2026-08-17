# Validation — 2026-08-17-batch-06

## Acceptance tests executed

| AT | command | result |
|---|---|---|
| Full suite | `python -m pytest tests/ -q` | **841 passed** in 66.49 s |
| Gantt contract | `python -m pytest tests/test_gantt.py -q` | **27 passed** |
| App/keymap contract | `python -m pytest tests/test_app.py tests/test_keymap.py -q` | passed |
| Syntax check | `python -m py_compile taskboard/app.py taskboard/views.py taskboard/keymap.py` | OK |

## What changed

- `taskboard/models.py`: `Task.depends_on: list[str]` persisted round-trip.
- `taskboard/views.py`:
  - `_task_reach` uses priority hue (high=rose, normal=sky, low=mut), milestone diamond.
  - `render_gantt` draws `└─►` dependency indicator and supports `focus`.
  - `nav_model` honours `gantt_focus`.
- `taskboard/app.py`: `F`/`esc` active in kanban and gantt; `gantt_focus` passed through.
- `taskboard/keymap.py`: `F`/`esc` views updated to `("kanban", "gantt")`.
- `README.md`: key table documents `F`/`esc` for kanban and gantt.
- `tests/test_gantt.py`: new ATs for priority hue, milestone, dependency, focus; updated width pins.
- `tests/test_app.py`: updated focus scope oracle; fixed stale `3` → `2` for URL arrow test.
- `tests/test_archive.py`: date mock for purge AC1 to keep it deterministic across real calendar drift.

## Out-of-scope notes

- No UI editor for `depends_on` in this batch; ids are persisted and rendered only.
- Task due meters remain on gantt rows (contrary to the early prototype draft).
- The dependency indicator reserves 3 cells on every task row, visible or blank, to keep the field aligned.
