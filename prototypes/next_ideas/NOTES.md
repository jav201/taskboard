# Prototype notes — next_ideas

**Question.** How would the batch-05 carries and several gantt improvements look?

**Location.** `prototypes/next_ideas/out/next-ideas.html` — open in browser.

**Generation.**
- `capture_gantt_ideas.py` renders the gantt variants with Rich and saves SVGs.
- `build_html.py` inlines those SVGs into a single switchable HTML file.

**Variants.**
- **A** — Immediate batch-05 carries: "Open legend" palette entry, fuzzy-search highlight, and a narrow-terminal more-layer with overflow count.
- **Baseline** — Current gantt, same data, kept for comparison.
- **B** — Gantt timeline controls (refined): zoom levels (1d / 2d / 7d), horizontal pan arrows, a vertical "today" marker, and lighter task status dots instead of full meters.
- **C** — Gantt task semantics (refined): priority-colored bars, dependency indicator, and milestone diamonds.

**Status.** Concept-only, not wired to the real app. Use the floating switcher or arrow keys to compare variants.
