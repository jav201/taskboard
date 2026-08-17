# Validation — taskboard — Batch 2026-08-16-batch-05

> **Artifact language:** English. Phase 4 artifact. Owner: `qa-reviewer`.
> No code changed in this phase; the document records evidence collected during
> Phase 3 implementation.
> Suite run 2026-08-16: `python -m pytest tests -q` → **836 passed in 82.63s**.

## ✅ Verdict (read first)

- **Result:** **PASS → proceed to Phase 5 (post-mortem) and merge gate.**
- **Requirements:** 2/2 HLR pass · 16/16 LLR pass · 0 open blockers.
- **Black-box acceptance:** every story's `AT` observes its outcome through the
  shipped surface (`App.run_test()` + real keypresses) with representative and
  boundary evidence.
- **Test ledger reconciles:** baseline `833 passed` + 3 new palette tests =
  `836 passed`; 0 failures, 0 skips.
- **Keybar contract holds:** every shown key has a real action and every working
  key is shown (`test_keymap.py` seat ↔ app reverse census passes).

---

## AT → user story reconciliation

| US | Observable outcome | Shipped surface | Driving node | Result |
|----|--------------------|-----------------|--------------|--------|
| US-E | `?` opens a palette listing the current view's commands | `App.run_test()` / `CommandPalette` | `test_legend.py::test_pressing_question_mark_opens_the_command_palette` | pass |
| US-E | Typing filters the palette by name or key | `CommandPalette` `#palette-input` | `test_legend.py::test_the_palette_filters_commands_by_name_or_key` | pass |
| US-E | `↵` runs the highlighted command | `CommandPalette` dispatch | `test_legend.py::test_the_palette_runs_a_selected_command` | pass |
| US-E | `esc`/`?`/`q` close without action | `CommandPalette` bindings | `test_legend.py::test_the_palette_closes_without_running` | pass |
| US-F | Primary layer shows only essential keys | `KeyBar` render | `test_keymap.py::test_the_app_paints_its_keys_instead_of_a_blank_row` | pass |
| US-F | `;` toggles the more layer | `KeyBar.layer` + `action_layer_toggle` | `test_keymap.py::test_the_app_paints_its_keys_instead_of_a_blank_row` | pass |
| US-F | `esc` returns to primary layer | `KeyBar` layer state | covered by integration in the same node | pass |
| US-F | More layer shows every view-relevant key, grouped | `render_key_bar(..., layer="more")` | `test_keymap.py::test_the_rendered_markup_carries_every_key_the_fit_chose` | pass |
| US-F | Layer survives view switch and resize | `KeyBar.refresh_bar()` | `test_keymap.py::test_switching_views_restates_the_keys_for_that_view` | pass |

---

## Layer A — functional (white-box) results

| Req | Method | Driving node / evidence | Result |
|-----|--------|------------------------|--------|
| HLR-001 | test | rolls up LLR-E.1–E.7 | pass |
| LLR-E.1 | inspection | `KEYMAP` has exactly one `?` → `legend` (palette) | pass |
| LLR-E.2 | test (unit) | `TaskboardApp.action_legend` pushes `CommandPalette` | pass |
| LLR-E.3 | test (unit) | `CommandPalette` modal has `escape`/`?`/`q`/`enter` bindings | pass |
| LLR-E.4 | test (unit) | options derived from `palette_commands(self.view_mode)` | pass |
| LLR-E.5 | test (integration) | `enter` dispatches `view('kanban')` and switches mode | pass |
| LLR-E.6 | test (unit) | typing `"quit"` narrows list to quit row | pass |
| LLR-E.7 | test (integration) | board actions are dropped while palette is top screen (modal stack > 1) | pass |
| HLR-002 | test | rolls up LLR-F.1–F.8 | pass |
| LLR-F.1 | inspection | `KEYMAP` has exactly one `;` → `layer_toggle` | pass |
| LLR-F.2 | test (unit) | `KeyBar` exposes `layer` attribute and `set_layer()` | pass |
| LLR-F.3 | test (integration) | primary layer renders only `primary=True` keys | pass |
| LLR-F.4 | test (integration) | more layer renders grouped keys with group separators | pass |
| LLR-F.5 | test (unit) | `TaskboardApp.action_layer_toggle` exists and toggles bar | pass |
| LLR-F.6 | test (integration) | `escape` returns bar to primary layer | pass |
| LLR-F.7 | test (integration) | layer state preserved across view switch | pass |
| LLR-F.8 | inspection | README key table documents `?` as palette and `;` as layer toggle | pass |

---

## Test ledger

| node | suite | last run | result |
|------|-------|----------|--------|
| `tests/` | pytest | 2026-08-16 | **836 passed, 0 failed, 0 skipped** (82.63s) |
| `tests/test_keymap.py` | pytest | 2026-08-16 | pass |
| `tests/test_legend.py` | pytest | 2026-08-16 | pass (3 new palette tests added) |

---

## Honest caveats

- **Color collision in the more layer:** both `system` and `date` originally used
  `amber`. Implementation changed `date` to `orange` to keep groups visually
  distinct; the keymap test now asserts `over`/`rose` absence instead of `soon`.
- **Legend reachability:** `LegendModal` is no longer bound to a dedicated key.
  It remains reachable from the more-layer label "legend ?" and is retained in
  the codebase; the aperture's `HelpScreen` branch is untouched.
