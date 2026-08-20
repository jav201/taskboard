# PLAN — 2026-08-18-batch-08 · taskboard "next-level" interactions

**Batch objective.** Ship the three interaction improvements captured in
`handoff-next-level.md`: Kanban lanes (a second axis), Focus Board follow-up
presentations, and a global live search/filter — without changing the model.

**Mode:** `core` (new presentations + interaction change). Language: `en`.

## Verified at intake

- Base currency: `main` @ `a93b17e` (batch-07 merged).
- Suite green: `python -m pytest tests/ -q -k "not test_win_clipboard_roundtrip"` → 849 passed.
- Prototype approved: `prototypes/next_level/out/next-level.html` (variants 1A/1B, 2A/2B, 3A/3B/3C).

## Stories — INVEST

| id | story | status | observable outcome |
|---|---|---|---|
| R-01 | **Kanban lanes.** As a user, I want a lane × phase grid so I can see how each project/priority group flows across phases. | DONE | `Tab` in kanban cycles `grouped → matrix → lanes`; lanes use the active `kanban_group`; empty lanes are omitted; overflow shows `+N more`. |
| R-02 | **Focus review queue.** As a user, I want one pinned task full-size with a stale-first rail so I can review follow-ups. | DONE | Focus `Tab` reaches `review`; the queue is ordered by `stale_order`; selected task is full-size left, rail right. |
| R-03 | **Focus stale-first tiles.** As a user, I want the tile grid reordered by staleness with a pressure strip. | DONE | Focus `Tab` reaches `stale`; pressure strip shows overdue count and sitting ≥7d count. |
| R-04 | **Global search `/`.** As a user, I want to filter kanban/gantt by title/project/notes and see hits highlighted. | DONE | `/` opens a prompt; the board re-renders filtered; `esc` clears the query before clearing project focus. |

## Increment plan

| inc | content | source files |
|---|---|---|
| 1 | Kanban lanes: `_kanban_lanes`, `tab` cycle, 2D nav, tests | `taskboard/views.py`, `taskboard/app.py`, `tests/test_app.py` |
| 2 | Focus follow-up: `stale_order`, `_focus_review`, `_focus_stale`, tab cycle, nav, tests | `taskboard/views.py`, `taskboard/app.py`, `tests/test_focus.py` |
| 3 | Live search: `matches`, `filtered_board`, search overlay, `/` binding, `esc` precedence, tests | `taskboard/views.py`, `taskboard/app.py`, `taskboard/keymap.py`, `README.md`, `tests/test_app.py` |

## Validation

- Full suite: `python -m pytest tests/ -q -k "not test_win_clipboard_roundtrip"` → **860 passed**.
- New tests cover: lanes rendering/navigation, review/stale presentations, `stale_order`, search matching/filtering, `esc` precedence, README keymap contract.

## Risks / watch-items

- Lanes navigation is 2D; `nav_model` and `_kanban_lanes` must agree on windowing and ordering.
- Search filtering can hide the selected task; `_select_first` and `_nav_columns` now use `_view_board()` to stay consistent.
- `escape` has three precedence levels now: clear search → clear focus → no-op.

## Decision log

| date | decision | by |
|---|---|---|
| 2026-08-18 | Batch opened; variants chosen from `handoff-next-level.md`: unified kanban lanes, Focus review + stale-first, live search filter (3A) | orchestrator (auto-approved plan) |
| 2026-08-18 | `search_query` kept session-level and never persisted | implementation |
| 2026-08-18 | `filtered_board` returns a shallow Board copy so real renderers draw the filter unchanged | implementation |
| 2026-08-18 | README keybinding table updated for `/`, `esc` precedence, and expanded `Tab` cycle | implementation |
