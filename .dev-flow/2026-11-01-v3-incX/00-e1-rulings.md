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

## Rulings on the E2 findings (2026-11-01, commit `9186362`)

These rulings settle the conflicts between ruling 3 / rulings 1 and 6 and the E1 requirements. The design is simplified: removing a feature wins over guarding it.

8. **The cover is dropped from ruling 3.** The `x` deck stays BYTE-IDENTICAL to what `H` → `c` writes for the same scope. The E2 probe already matches it byte for byte. No change to the cover text, and no change to `report_deck.py`'s rendering. LLR-4501.3/.4 stand as written.
9. **The separate file name is kept from ruling 3.** It prevents same-day overwrites of `H`'s files. The name is `present-<project-slug|all>-<YYYY-MM-DD>.html` in `reports/`, built by a name helper (S-3 `present_name`), and the file bytes do not change.

   Amend LLR-4501.1, LLR-4501.2, LLR-4501.11, LLR-4504.1, AT-4501 and AT-4502 to this name with targeted edits. Each amendment gets one ledger entry that names each id.
10. **The hint row keeps its current wording,** and the hint parts of rulings 1 and 6 are withdrawn. LLR-4506.4 stands. HTML is named in the presentation's `?` window (ruling 4) and in the README, not in the hint row.

11. **I-4 (2026-11-01, commit `113482e`) is resolved with no edit.**
    - `present_name` lives in `views.py`, beside `present_deck_boards`, so `report_deck.py` is unchanged and the requirements' §1/§6 statement (13 units, 3 source files) is correct.
    - HLR-4501's negative control names `deck-*.html` deliberately: a mutant that writes `H`'s name must turn the test RED.

## E3 round 1 rulings (2026-11-01): architect FAIL `8d884ac`, security PASS-WITH-NOTES `d0ff4f1`

12. **F-1 — accepted as proposed.**
    - `present_name(project_name: str | None, today) -> str` lives in `views.py`.
    - It imports `slug` inside the function (`from .report_html import slug`), the pattern `write_reports` already uses.
    - `report_deck.py` stays untouched.
    - S-3 is resolved by this ruling.
13. **F-2 — accepted. Ruling 2 is amended.** The deck holds **what the presentation does not hide**:
    - Excluded: the saved hide flags (task, project, milestone class); archived tasks; tasks of archived projects; tasks without a project.
    - Not used to decide scope: the drawing state (open/done split, folds, cursor, overflow).
    - Oracle: `present_tasks_m(board, pid)[1]` for each held project.
    - Fix the Definitions row, and add one ledger entry that names LLR-4501.8 and LLR-4501.9.
14. **S-1 — the `x` deck strips task URLs.**
    - The audience file carries no links the presentation never draws.
    - The proxy board clears each held task's `urls` before `extract`. The deck renderer is not changed.
    - `H`'s reports keep their URLs.
    - Byte identity (LLR-4501.3/.4) becomes: identical to `H` → `c`'s deck of the same proxy board with URLs cleared.
    - Add one new LLR, an Unwanted-form requirement, with a negative control: a task URL present in the file → RED.
    - Leave any other per-task meta the presentation does not draw unchanged, and record it in BACKLOG as a known limit.
15. **F-3 — accepted.**
    - Re-measure the bar over 10 views × {80, 118} × {primary, more}, and record the table.
    - In E4, re-baseline `KEYBAR_BASE` in `test_colour_budget_app.py` following its own convention (a comment plus an evidence file). This is a recorded re-baseline, not a weakened law.
    - TC-4321 drops `"H"`, with the justification written in the packet.
16. **F-4 — accepted: `H` keeps its seat** (`keymap.py:152`), flipped to `bar=True, primary=True`.
    - This amends ruling 1's threshold to about 193 columns.
    - Fix the comments that say it is "off the bar".
17. **F-5 — accepted.** Add "and no milestone of a hidden class" to LLR-4501.4, and "and the presented board is in the registry" to LLR-4501.3, recorded in one ledger entry. P-A-6 is resolved by this ruling.
18. **F-6 — accepted.** `present_deck_boards` resolves the project exactly as `render_present` does. Add one new Unwanted-form LLR. An archived presented project goes to BACKLOG as a known limit.
19. **F-7 — accepted.** Correct the slice (§6) to the true unit count with targeted edits and one ledger entry. Ruling 11's "13 units" claim is withdrawn.
20. **F-8 — accepted.** Add one ledger entry that names each canon id superseded by HLR-4504, so the batch-end canon fold is mechanical.
21. **F-9 to F-13 — the architect's proposed fixes are adopted as written**, with these specifics:
    - **F-10:** take the E4 addendum ("after each press, `reports/` holds that scope's `present-*.html`, 0 `.svg`, 0 `.png`, and no other file is new or changed").
    - **F-11:** view 3's file is named `present-<date>.html`. It can never equal `present-<slug>-<date>.html`. This amends ruling 9.
    - **F-12:** `x`'s offer uses the existing `TaskboardApp._report_offer`, and `PresentScreen.action_open_export` consumes it. This amends ruling 6.
    - **F-13:** a list of E4 addenda.
22. **Security S-2, S-4, S-5 and S-6 — the reviewer's proposed fixes are adopted.**
    - S-6: `_open_report` also catches `ValueError` from `as_uri()`.
    - Each LOW that the reviewer marked "accept" goes to BACKLOG.

The design correction is ONE agent making targeted edits (the skill's rule). That agent is **Kimi K3.1 Pro**, at the operator's request of 2026-11-01: «Intenta usar kimi 3.1 para el diseño y 2.8 para la implementación.» E3 round 2 follows, with the Opus architect and Opus security reviewer.
