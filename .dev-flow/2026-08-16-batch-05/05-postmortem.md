# Post-mortem — taskboard — Batch 2026-08-16-batch-05

> **Artifact language:** English. Phase 5 artifact. Owner: `orchestrator`.
> Batch objective: improve key-binding discoverability via the operator-approved
> **E + F** proposal (command palette + layered keybar).

## Summary

- **Result:** delivered and validated. Merge gate approved by operator.
- **Final test count:** `836 passed` (`+3` new palette tests; `0` failures, `0` skips).
- **Stories delivered:** 2/2 (US-E command palette, US-F layered keybar).
- **Source files touched:** `taskboard/keymap.py`, `taskboard/app.py`,
  `taskboard/modals.py`, `tests/test_keymap.py`, `tests/test_legend.py`,
  `README.md`, plus deliberation artifacts in `prototypes/keybar_ideas/`.

## What went well

- **Prototypes drove the decision.** The E + F proposal was chosen after the
  operator reviewed colored terminal-rendered prototypes, so the implementation
  target was unambiguous.
- **Seat-first design kept the contract intact.** Adding `primary` and `group`
  fields to the existing `Key` tuple meant the keybar continued to be the single
  source of truth; no parallel table was needed.
- **Tests caught real issues.** The three new palette tests immediately surfaced:
  1. an `Enter` key handler gap when the `Input` had focus,
  2. a parameterized-action dispatch bug (`self.action` does not exist on `App`),
  3. a docstring syntax typo from an embedded Unicode arrow.
  All were fixed before validation.
- **Layer integration was cheap.** Because `KeyBar.refresh_bar()` already
  re-rendered on view switches, preserving `layer` across those events required
  only storing the state on the widget.

## What cost more than expected

- **Palette action dispatch.** The first attempt manually parsed
  parameterized action strings like `view('kanban')` and tried to call
  `self.action(name, (value,))`. That method does not exist on Textual's `App`;
  the correct path is `await self.run_action(action)`, which parses the action
  string exactly as normal bindings do. `_on_palette_run` was made async so it
  could await the dispatch.
- **Color collisions in the more layer.** Two unrelated groups (`system`, `date`)
  originally mapped to `amber`. The fix was a one-line hue change for `date` to
  `orange`, but it required updating the keymap test's color oracle.

## Decisions recorded

| # | Decision | Why |
|---|----------|-----|
| D-1 | `?` repurposed for palette | Operator-approved E + F; natural discovery key. |
| D-2 | `;` as layer toggle | Unused, home-row-adjacent, matched prototype. |
| D-3 | `LegendModal` kept but unbound | Reachable from palette/more-layer; avoids wasting a key. |
| D-4 | `Key.group` drives more-layer grouping | Keeps `KEYMAP` as the single seat. |
| D-5 | `_on_palette_run` is async | `App.run_action` is a coroutine in Textual 8.2.8. |

## Carries / backlog items

- **Legend command in palette:** add a dedicated "Open legend" palette entry
  that launches `LegendModal`, so the legend is reachable without reading the
  more-layer label.
- **Palette scoring:** current filter is substring-only; could be upgraded to
  fuzzy scoring if the command list grows.
- **More-layer width stress:** very narrow terminals still drop grouped keys
  behind `+N`; verify behavior at 60 columns with custom phases.

## Metrics

- Files changed: 6 tracked files + batch artifacts + deliberation dir.
- Tests added: 3 (palette behavior).
- Tests updated: `tests/test_keymap.py` (layer oracles), `tests/test_legend.py`
  (palette replaces old `?` behavior).
- Pre-batch baseline: 833 passed. Post-batch: 836 passed.

## Merge status

Approved by operator. Commit and push to `origin/main` authorized.

**Batch closed:** 2026-08-16.
