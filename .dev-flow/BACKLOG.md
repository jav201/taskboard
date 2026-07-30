# BACKLOG — taskboard (canonical, cross-batch)

Shared by `/dev-flow` and `/fast-dev-flow`. Every open item lives here exactly once.
No `docs/engineering-rules.md` exists in this repo, so this is the default location.

**Base ref:** `b3cc60d` (main) · **Last refresh:** 2026-07-30

## Shipped

- **DONE** · Prism increment 1 — the colour ration: four colliding project hues
  retired (amber 0.0 / cyan 48.3 / orange 51.0 / rose 63.8 from a reserved hue),
  deterministic injective remap on load, high-priority marker moved from the amber
  `◉` to the neutral glyph `!`. 15 new tests, 152 green, 4 mutants killed.
  (this batch — see `.fast-dev-flow/spec.md`)

## Open — Prism roadmap (`_tui_prism_proposal/PROPOSAL.md` §9)

| # | item | files (est.) | note |
|---|---|---|---|
| 2 | Shared day axis + field lattice as pure helpers in `views.py` | 2 | no view changes yet |
| 3 | The new project row (horizon + phase glyph + figures + chip + status mark) | 2 | replaces the 2 rows of `render_swimlanes` |
| 4 | Leader's bench + pressure ranking + resting row + height allocator | 4 | port the 21 laws of `verify_prism.py` into `tests/` |
| 5 | Momentum — needs a model change (`phase_changed` on `Task`) | 4 | do NOT start before 2-4; old tasks must read *unknown*, never zero |
| 6 | Ambient — 700 ms interval rotating the today rule in lanes | 3 | 2800 ms cycle; no cell but the rule may change |

## Open — findings raised while shipping increment 1

- **`ribbon.py:49` paints the ISO week number in `amber` (#fbbf24)** — the reserved
  *due today* hue worn by a mark that is neither identity nor severity. Same class
  of collision the ration just fixed, one file away. Small, self-contained.
- **`views.py:177` paints the image indicator `▤` in `sky`** — `sky` is an
  *identity* hue (a project colour), so a task attribute is wearing the house that
  names projects. Decide: move it to a neutral tone, or accept and document.
- **The `!` marker is per-card only.** The proposal's `!N` aggregate (count of
  high-priority open tasks per project) belongs to the new lanes row — increment 3.
- **Columns / agenda / gantt render no priority at all.** Not a regression (they
  never did), but if priority matters at a glance, three of five views omit it.
- **`sky` survives the ration by 7.4 units** (62.4 vs the 55 accent band). If
  `accent` #2dd4bf is ever retuned, re-run the oracle in `tests/test_palette_ration.py`.
- **`modals.py:322-324` would raise `InvalidSelectValueError`** if an in-memory
  `Project` ever carried a retired hue (only reachable by constructing `Project`
  directly in code — the loader always returns a lawful hue). Left unguarded on
  purpose; revisit if any code path starts building projects from raw data.
- **`.venv` cannot run the suite** — `ModuleNotFoundError: No module named 'PIL'`
  makes 5 image tests error there; the suite is green under system python. Either
  install Pillow into `.venv` or mark those tests as requiring it.

## Housekeeping

- Untracked in the working tree, pre-existing and NOT part of this batch:
  `_tui_prism_proposal/` (a concurrent design agent owns it), `.claude/`, `.s19tool/`.
  Decide what to commit / ignore.
