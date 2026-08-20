# Prototype notes — next_level

**Question.** The handoff (`handoff-three-prototypes.md`) listed three ideas. Two of
them were already shipped when the repo was checked — kanban sort/group/collapse/focus
(batch-04) and the focus board with tiles/inspector/images (batch-07). So this round is
the three ideas AT THE NEXT LEVEL: what would each become now?

**Location.** `prototypes/next_level/out/next-level.html` — open in browser. Switch
variants with ←/→ or the floating bar; keys 1/2/3 jump to each idea's first variant.

**Generation.**
- `proto.py` — the variant renderers. They compose the REAL views
  (`render_kanban` / `render_gantt` / `_focus_tiles`) or the real cell builders
  (`card_cell`, `_windowed_header`) over a cell-grid compositor, so dimming, match
  highlighting and the overlay are honest renders, not redrawn mockups.
- `capture.py` — loads the shared synthetic fixture, renders all nine figures to
  SVG + one `next-level.txt`. Fixture is enriched IN MEMORY ONLY: six pins, five
  note bodies with `==`/`!!`/`++` highlight syntax, and `phase_changed` stamps —
  without those the focus variants would render empty. The fixture file is never
  written.
- `build_html.py` — inlines the SVGs into the switchable page.

**Variants.**
- **Baseline** — the shipped kanban, same data, for comparison.
- **1A / 1B** — kanban lanes × phases with real cards in every cell, lanes by
  priority (1A) or by project (1B). The second axis sort/group doesn't give.
- **2A** — focus as a review queue: one task full-size, the rest a stale-first
  rail. Only existing keys (`j/k t [ ] ↵ esc`), no model change.
- **2B** — the shipped tile grid ordered stale-first under a pressure strip
  (`▲ overdue · ■ ≥7d`).
- **3A** — `/` live filter bar on the REAL kanban and gantt (filtered Board proxy;
  gantt also drops project lanes left empty), matches reverse-lit.
- **3B** — jump palette: solid frameless overlay on the dimmed gantt, ranked
  results (title > project > notes), enter lands the selection.
- **3C** — context dim: nothing hidden, non-matching cards fade to 30 %.

**Model changes required: none.** No new Task fields, no new bindings that don't
already exist (`/` would be the one new key for idea 3). If the user later wants a
`reviewed_at` stamp or a snooze, that's a model conversation to have FIRST — per
the handoff's rule.

**Status.** Concept-only, not wired to the real app. Viewport 118×30, demo query
`api` (matches 3/15 tasks: one by title, three by project — overlap included).
