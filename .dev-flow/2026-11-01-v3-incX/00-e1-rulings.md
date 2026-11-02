# Orchestrator rulings on the E1 open questions (2026-11-01)

These rulings answer the E1 author's four open questions, at commit `4f9aef0`.

1. **The key bar's fit rules stand.**
   - At widths of about 201 columns or more, the bar shows `H Report`. Below that it shows a bare `H`, the same way it treats every other key.
   - Discoverability rests on two more things: the `?` help lists `H report`, and the presentation's hint and `?` window name the export as HTML.
   - The capture shows the bar as the fit rules draw it. Take it at 118x30 and 80x24, plus one wide frame (≥ 201 columns) where `H Report` appears.
2. **The view 3 deck mirrors what the presentation shows.**
   - The deck draws exactly what the presentation draws. Done tasks are included when the presentation draws them.
   - Hidden projects, hidden tasks and hidden milestone classes are excluded from the bytes.
   - The presentation is the oracle. Each test compares the deck's set of tasks against the presentation's set of shown tasks.
3. **Names and the cover.** The `x` export gets its own file name, so it never overwrites `H`'s files: `present-<project-slug|all>-<YYYY-MM-DD>.html`, written to the same `reports/` folder. The cover states what was presented, for example `Presented · 3 projects` or the project's name, instead of "All loaded boards (1)". A minimal change to `report_deck.py` / `report_html.py` is allowed to support this.

   Source budget: `app.py`, `views.py`, `keymap.py`, `report_deck.py`. That is 4 files. README is docs and does not count toward the budget. If `report_html.py` is also needed, the cover/name support goes there instead of `views.py`, and the 4-file cap still holds.
4. **The `?` window and `o`.** X-4 is widened: the presentation's `?` window gains the `o open export` row, and its export row reads HTML. Nothing else in `R` changes.

## Rulings on the E2 baseline facts (2026-11-01, commit `dde7fbe`)

5. **Prototype scripts.** Three prototype scripts call the functions being removed. They are frozen design evidence, not product code, and no test collects them. Leave them as they are. One line in the README of each prototype folder, or in BACKLOG, says they no longer run after this change. This follows the 2026-10-18 precedent of marking such scripts HISTORICAL.
6. **`o` inside `R`.** The presentation is a modal screen, so the app-level keys do not reach it. `o` therefore binds on `PresentScreen` itself, and the export offer lives there. `H` stays app-level and works outside `R` only. The `R` hint names `x` (HTML), not `H`.
7. **`test_TC_3117`.** This test pins `H` as `bar=False`. Rewrite it to pin X-3, with its reason recorded in the packet.
