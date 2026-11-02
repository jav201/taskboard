# Requirements ledger — taskboard — Inc X, `x` in the presentation exports the HTML deck

> Append-only. Every entry names the requirements it amends one by one (V26: no ranges).

### LED-2026-11-01-incX.1 — the commission's X-1..X-4 made strict, with the failure paths it left open
- **Requirement:** HLR-4501
- **Requirement:** HLR-4502
- **Requirement:** HLR-4503
- **Requirement:** HLR-4504
- **Requirement:** HLR-4505
- **Requirement:** HLR-4506
- **Date:** 2026-11-01
- **What changed:** the commission text (X-1..X-4) was split into 40 single-`shall` LLRs. Added beyond its words, each as its own requirement: two byte-equality oracles against `H` → `c` (LLR-4501.3, LLR-4501.4), so "the same writer" is tested, not asserted; views 1 and 2 export the presented project whatever its view-3 flag (LLR-4501.5); only the presented board, never every loaded board (LLR-4501.7); folded projects are exported whole (LLR-4501.8); done tasks are exported (LLR-4501.9); `x` writes no board file (LLR-4501.10); an unlisted `--open` board (LLR-4501.11); an empty view 3 (LLR-4501.12); the narrow rule split into its toast and its no-write (LLR-4501.13, LLR-4501.14); archived, archived-project and project-less tasks (LLR-4502.3), hidden-class milestones (LLR-4502.4) and their legend (LLR-4502.5) left out of the bytes; hide flags read at the press (LLR-4502.6); the offer's three dead states share one response (LLR-4503.3); write failure, offer withdrawal, open failure and markup in paths (LLR-4503.4, LLR-4503.5, LLR-4503.6, LLR-4503.7); no external process (LLR-4504.2); the key-bar fit measured as keys kept, at most one word lost, and the word shown where everything fits (LLR-4505.2, LLR-4505.3, LLR-4505.4); `o` gets a row in the presentation's `?` window (LLR-4506.2), and the bindings and hint rows are pinned to base otherwise (LLR-4506.3, LLR-4506.4).
- **Why:** each addition closes a path where the literal commission either leaks what was hidden (an Inbox row, an archived task, a hidden-class milestone, another board), crashes `R` (an unwritable `reports/`, an unlisted board's `None` id), or changes keys X-4 freezes. `o` needs a row in `PRESENT_KEYS` because `PresentScreen` is a `ModalScreen`: the app's non-priority `o` never reaches past it (`app.py:2326-2331`), and the seat law says a bound key is shown.
- **Evidence:** `taskboard/app.py:623-649` (base `action_export`), `app.py:2993-3051` (`H`'s write, toast, offer, open); `taskboard/report_html.py:98-174` (`extract` keeps archived tasks and adds an Inbox row; no hide flag read), `report_html.py:182-188` (`report_name`); `taskboard/views.py:6642-6684` (`present_tasks`, `present_tasks_m`, `present_hidden`), `views.py:7423-7425` (`_all_plan`); `taskboard/models.py:2476-2484` (`present_order`); README.md:189 (hidden classes leave "the presentation views and their exports"); the key-bar probe below.

### LED-2026-11-01-incX.2 — `H` in the key bar: the measured fit
- **Requirement:** LLR-4505.1
- **Requirement:** LLR-4505.2
- **Requirement:** LLR-4505.3
- **Requirement:** LLR-4505.4
- **Date:** 2026-11-01
- **What changed:** X-3's "`H report` shows in the key bar" is pinned as the key `H` in the primary bar of all 10 main views at 80 and 118 columns, with the word `Report` required only where every entry keeps its word (≥ about 201 columns).
- **Why:** measured on `509d444` (`keymap.fit_bar`, `H` appended as the primary layer's last entry): 0/20 cases drop a key, 0/20 lose more than one word, but `H`'s word is the first the fit rule drops, and the primary bar already overflows below 191 columns, so at 80 and 118 `H` is drawn bare. Declared at its current seat position instead, `H` lands before `↓ ↑` (also 0 keys dropped). Declared universal, it keeps its word but 7/20 cases lose two or more view words. The commission's capture "showing `H report`" will show `H` (open question OQ-1).
- **Evidence:** the probe's output in this stage's report (`fit_bar` over 10 views × {80, 118, 140}, three placements); `taskboard/keymap.py:308-325` (`fit_bar`), `keymap.py:284-287` (`global_keys`), `taskboard/modals.py:3391-3397` (the `?` help's band reads `bar_keys`, its global line `global_keys`).

### LED-2026-11-01-incX.3 — `x` gets its own file name, `present-<project slug|all>-<date>.html` (ruling 9)
- **Requirement:** LLR-4501.1
- **Requirement:** LLR-4501.2
- **Requirement:** LLR-4501.11
- **Requirement:** LLR-4504.1
- **Requirement:** AT-4501
- **Requirement:** AT-4502
- **Date:** 2026-11-01
- **What changed:** LLR-4501.1 names the views-1/2 file `present-<project slug>-<date>.html` (an empty slug becomes `project`), and its negative control becomes "write `H`'s `deck-<board slug>-<project slug>-<date>.html` name". LLR-4501.2 names the view-3 file `present-all-<date>.html`, and its negative control becomes "write `H`'s `deck-<date>.html` name". LLR-4501.11 keeps only its cover arm: the board's label is no longer part of the file name, and its threshold checks the views-1 file as `present-<project slug>-<date>.html`. LLR-4504.1's threshold drops "0 `present-*` files" and checks exactly 1 new `present-*.html` per press, beside 0 `.svg` and 0 `.png`. AT-4501's toast reads `Report written: present-<project slug>-<date>.html`. AT-4502's file is `present-all-<date>.html`. Thresholds (2/2, 1/1, 2/2, 3/3) and every other negative control are unchanged.
- **Why:** ruling 9 (00-e1-rulings.md) keeps ruling 3's separate name so that a same-day `x` never overwrites `H`'s `deck-…` files; E2 finding I-2 showed the six texts still named `deck-…`. Ruling 8 drops the cover change, so the file's bytes stay those of `H` → `c`; only the name differs.
- **Evidence:** `graph-interfaces.cw.md` node `present_name` (S-3) and findings I-1, I-2, I-3; `report_html.py:182-188` (`report_name`, `H`'s `deck-…` names).
