# Inc X — E2 seams between group A (app.py, keymap.py) and group B (views.py, report_deck.py)

The contracts are frozen in `graph-interfaces.cw.md`. A group that needs a change writes a finding in its own
graph file; only the orchestrator edits the interfaces. `report_html.py` and `modals.py` are not changed.

| # | Caller → callee | Contract | Owner of each side | Examples |
|---|---|---|---|---|
| S-1 | A `PresentScreen.action_export` → B `views.present_deck_boards(lane, project_id)` | `lane` = `(registry id \| None, name, colour, Board)`; `project_id` = None in view 3, else the presented project; returns `[(id, name, colour, proxy)]`, one entry; proxy = shown projects (view 3: presentation order) and shown tasks in board order; never saved | A builds `lane` (`PresentScreen._deck_lane`); B builds the proxy | TC-4705..4709, 4712, 4721..4725, AT-4501, AT-4502 |
| S-2 | A → `report_html.extract(boards, people, marks, today, project=key)` (unchanged) | `key` = None in view 3, else `<lane id or "#0">:<project id>`; `today = date.today()`; B's proxy always holds the keyed project, so `extract` never raises | A builds the key; B guarantees the project is in the proxy | TC-4703, TC-4704, TC-4707 |
| S-3 | A → B `report_deck.present_name(d)` | `present-<project slug or "project">-<meta.today>.html` (scope project) or `present-all-<meta.today>.html` (scope all); pure (ruling 9; LLR-4501.1/.2 as amended by LED-2026-11-01-incX.3) | B | TC-4701, 4701b, 4701c, 4702 |
| S-4 | A → `report_deck.render(d)` (unchanged) | resolved by ruling 8: no `presented` keyword and no cover change; `x` calls the base `render(d)`, so its bytes equal `H` → `c`'s for the same d | B (no change) | TC-4703, TC-4704, TC-4712 |
| S-5 | A keymap `PRESENT_KEYS` row `(("o", "open_export"),)` → A `PresentScreen.action_open_export` | priority binding on PresentScreen; reads and clears `PresentScreen._export_offer`; opens through `TaskboardApp._open_report` | A (both sides; listed because the task names it as a frozen interface) | TC-4732, 4733, 4736, 4763, AT-4503 |
| S-6 | A `PresentScreen.action_export` and A `TaskboardApp._on_report_chosen` → A `TaskboardApp._write_report(write, folder, skipped=0)` | one write → toast tail; returns the first path or None on OSError; stores no offer (each caller stores its own: ruling 6) | A | TC-4731, 4734, 4737, TC_3120 |
| S-7 | B removals ↔ A imports (integration order) | B removes `present_paths`, `save_present_svg`, `_find_msedge`, `save_present_png`, `present_all_export` (and `os`, `shutil`, `subprocess` imports, `_all_timeline`'s `anchor`); A must drop its imports of the four public names in the same integration step, or `import taskboard.app` fails | A and B, joined at the E4 integration step | TC-4743 |
| S-8 | B's proxy ↔ the hide flags A writes | `space` / `a` / `u` / `K` `J` in `R` save the flags at once; `present_deck_boards` reads them at each `x` (no copy taken at open) | A writes, B reads | TC-4726 |

## Seams outside the two groups (for E4, not interfaces)

- **Tests** that call the removed functions or pin the SVG export: listed in `baseline-notes.md` (10 test functions and 1 fixture in 7 files, plus 8 tests that press `x` and read `.svg`); group A's tester also rewrites test_TC_3117 (ruling 7).
- **Docs:** README lines 140, 189, 291, 410 (A, LLR-4506.5); docs/ARCHITECTURE.md Edge/SVG lines (finding P-B-4); the three prototype folders (ruling 5).
- **Canon:** REQUIREMENTS.md LLRs that name the removed functions are superseded at the batch-end fold (finding P-B-4).
