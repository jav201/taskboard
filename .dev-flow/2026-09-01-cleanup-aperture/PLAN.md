# cleanup-aperture

## Objective

Remove the aperture/widget feature completely and free the `6` keybinding.

## Scope

- Delete `taskboard/aperture.py`.
- Remove aperture references and the `action_aperture` method from `taskboard/app.py`.
- Remove the `6` → `aperture`/`Widget` binding from `taskboard/keymap.py`.
- Remove the aperture row from `README.md` keybinding table and any prose describing it as a current feature.
- Remove or update tests that assert `6`/aperture behavior.
- Prune dead production modules that are only imported by the aperture chain:
  `hero.py`, `language.py`, `engine.py`, `themes.py`, `motion.py`, `naught.py`, `bases.py`.

## Increments

### Increment 1 — Remove aperture/widget and free key 6

1. Delete `taskboard/aperture.py`.
2. In `taskboard/app.py`:
   - Remove `action_aperture` method.
   - Remove aperture checks in `check_action`.
   - Remove aperture-related comments/docstrings.
3. In `taskboard/keymap.py`:
   - Remove `Key("6", ...)` binding.
   - Clean up obsolete aperture comment.
4. In `README.md`:
   - Remove the `6` Widget/aperture row from the keybinding table.
   - Remove prose describing aperture as a current feature.
5. In tests:
   - Remove aperture-specific tests in `tests/test_app.py`.
   - Update any count assertions that now expect one fewer view/key.
6. Verify import graph and delete dead modules only imported by the aperture chain.

#### Verification

- `python -m pytest tests/ -q` green (excluding known environmental `test_win_clipboard_roundtrip` flake).
- RED-arm mutation evidence recorded below.

## Phase 4 validation

- Full pytest suite run after changes.
- Mutation evidence recorded (at least one RED arm).

## Decision log

| Phase | Date | Decision | Notes |
|-------|------|----------|-------|
| 0 | 2026-09-01 | cleanup-aperture opened | Operator directed removal of aperture/widget and freeing of key 6. |
| 3 | 2026-09-01 | Increment 1 complete | Aperture/widget removed; key 6 freed; dead modules pruned. |
| 4 | 2026-09-01 | Phase 4 validation complete | Full suite green after cleanup; mutation evidence recorded. |
| 6 | 2026-09-01 | Cleanup committed | `git add -A && git commit` performed; push deferred pending operator order. |

## Suite status

`python -m pytest tests/ -q` — **1284 passed** (baseline 1291 passed; 7 removed tests).
The environmental `test_win_clipboard_roundtrip` was re-run alone and passed.

## Mutation evidence

RED arm: temporarily restored the `6` → `aperture`/`Widget` binding in
`taskboard/keymap.py` and ran `tests/test_keymap.py`.

- `test_every_shown_key_has_a_real_action_on_the_app` failed because
  `TaskboardApp.action_aperture` no longer exists.
- `test_the_readme_keybinding_table_matches_the_seat` failed because the
  restored `6` binding is not documented in `README.md`.

Reverting the temporary binding restored green.
