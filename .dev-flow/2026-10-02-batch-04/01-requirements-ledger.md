# Requirements ledger — taskboard — Batch 2026-10-02-batch-04

> Append-only. Entries are added in chronological order and never rewritten. The live
> contract is `01-requirements.md`; this file records how it came to say what it says.
> Every entry names the requirement it amends; every requirement names its entries. `V26`
> compares the two sets of pairs both ways.

_No entries yet. The first amendment to the live contract writes the first one, in the
shape the field guide's §7 shows (`req-template.md` in the guide directory init prints), and nothing
above this line is ever edited._

### LED-2026-10-02-batch-04.1 — user and synced text never parsed by Textual
- **Requirement:** HLR-401
- **Date:** 2026-10-02
- **What changed:** new requirement: every dialog, picker, select, button and toast paints user and synced text literally; the site population is derived by a census of the code.
- **Why:** BACKLOG S1 (MEDIUM, `2026-09-30-batch-01`: "about 13 other sites in `modals.py`"), S-5 (`2026-10-02-batch-02`: `app.py` notifies ids and exceptions with markup on); the coordinator reproduced the crash on 2026-10-02. The census measured 45 sites, not 13 (P-8).
- **Evidence:** `evidence/p0-probes.txt` §P-1, §P-6, §P-7; `evidence/p1-census-base.txt`.

### LED-2026-10-02-batch-04.2 — control bytes stripped at load and at sync
- **Requirement:** HLR-402
- **Date:** 2026-10-02
- **What changed:** new requirement: every string read from the board file or the shared directory loses its control bytes (tab and newline kept; CR-LF → LF, D-404).
- **Why:** BACKLOG S2 (LOW: ESC/C1 in notes survive `_highlight_markup`) and L1 (ESC in a title reaches the terminal; a teammate's file could inject sequences).
- **Evidence:** `evidence/p0-probes.txt` §P-3, §P-4.

### LED-2026-10-02-batch-04.3 — the details info grid paints
- **Requirement:** HLR-403
- **Date:** 2026-10-02
- **What changed:** new requirement: the details view paints its five info-grid fields one per row (PV-1, D-406).
- **Why:** BACKLOG "`TaskDetails` info grid paints blank (pre-existing)"; diagnosed at P1: an auto-height grid row is one line and the label's top margin consumes it (P-9).
- **Evidence:** `evidence/p0-probes.txt` §P-5; `evidence/p1-grid-minimise.txt`.

### LED-2026-10-02-batch-04.4 — user text as Text pieces; the census judges parsers too
- **Requirement:** HLR-401, LLR-401.1, LLR-401.3
- **Date:** 2026-10-03
- **What changed:** the fix form changes from `_rich` over `escape`d text to `Text` pieces (`Text.assemble` / `Text.append`); a parser call is markup-inert only over an app literal, and every parser call in `modals.py` / `app.py` is censused (TC-406, NEW LLR-401.3); exemptions keyed by the value's source text and the two help-modal swatch/example sites added; the payload set becomes three payloads, per site, each in its own run; the reachable-site table (§5.1) added.
- **Why:** P2 iteration 1 — Q-1 / A-1 / S-2 (blocker: the census trusted any `_rich`), S-4 (escape + parse doubles or eats backslashes and substitutes emoji), Q-2, Q-4, Q-8 / S-7, Q-9, S-6; operator ruling 2 of 2026-10-03, asked at the gate: "Piezas de texto, sin formato".
- **Evidence:** `evidence/p1-census-iter2.txt`, `evidence/p1-pieces-probe.txt`; `02-review.md`.

### LED-2026-10-02-batch-04.5 — one control-byte rule, four doors
- **Requirement:** HLR-402, LLR-402.1, LLR-402.3
- **Date:** 2026-10-03
- **What changed:** the clipboard cleaner shares `strip_controls`; the Setup view's own `team.json` read goes through `_read_json`; the round-trip claim narrowed to "a board file holding no control byte"; the file check reads the parsed strings and the screen check uses ESC and C1; AT-405 becomes the C-12 chain through the app's own save and push.
- **Why:** P2 iteration 1 — A-2 (D-404 was false: the clipboard rule kept CR), A-3, A-4, Q-5, Q-6, Q-7, Q-12; operator ruling 3, asked at the gate: "Sí, todas".
- **Evidence:** `02-review.md`; `evidence/p0-probes.txt` §P-3, §P-4.

### LED-2026-10-02-batch-04.6 — grid values wrap
- **Requirement:** HLR-403, LLR-403.1
- **Date:** 2026-10-03
- **What changed:** the grid label height is automatic, not one row: a long value wraps under itself instead of being cut; thresholds "≥ 1 row, value begins on its label's row"; a long-value and an 80×24 visibility arm; priority `high` in AT-406.
- **Why:** P2 iteration 1 — UX-1 (major: `height: 1` cut a long value silently), UX-5, Q-11; operator ruling 3.
- **Evidence:** the ux-reviewer's renders (`02-review.md`).

### LED-2026-10-02-batch-04.7 — synced project fields pass the loading rule
- **Requirement:** HLR-404, LLR-404.1
- **Date:** 2026-10-03
- **What changed:** new story US-404 and requirement: `apply_config_to_board` sets a project's name, colour, status and dates only through `Project.from_dict`'s values (which gains the name and date checks); the picker shows the status as a text piece.
- **Why:** P2 iteration 1 — security S-1 (HIGH: a teammate's `team.json` status reached the project picker's markup and a click fired an app action) and S-3 (MEDIUM: an unknown colour or a non-text name crashed the views); operator ruling 1 of 2026-10-03, asked at the gate: "Sí, dentro de S".
- **Evidence:** `evidence/p1-sync-fields-probe.txt` (P-12).

### LED-2026-10-02-batch-04.8 — P2 iteration 2 folded
- **Requirement:** HLR-401, HLR-402, HLR-403, HLR-404, LLR-401.1, LLR-401.3, LLR-404.1, LLR-404.2
- **Date:** 2026-10-03
- **What changed:** HLR-401's transition-log toast is compared with the OS error text the failing write produces (it carries the path's repr), a `[B]x` path arm added, keys and the toast-read method stated in §5; LLR-401.1 names its five exemptions, keys them with their binding and plants every remaining sink form; LLR-401.3 constrains piece styles, gains one shared highlight tokeniser in `views.py`, the style pins TC-415 and the bracket titles; HLR-402 narrowed to "a board file the app saved", AT-404's through-app round trip dropped (TC-410 owns it), AT-405 asserts the pushed file; HLR-403's thresholds executed (P-14) with the wrap geometry; HLR-404 judges refusal on the input, applies only present keys, lets `null` clear a date, extends to the roster and duplicate ids (NEW LLR-404.2) and an any-type colour, its picker clause moved to HLR-401's LLR-401.3, AT-407 uses a visible-effect action.
- **Why:** P2 iteration 2 — qa Q2-1 (blocker: `str(path)` never equals the Windows OS error text) and Q2-2..Q2-11, architect A2-1..A2-5, security S2-1..S2-6, ux UX2-1..UX2-5; operator ruling 3 ("Sí, todas").
- **Evidence:** `evidence/p1-grid-threshold.txt`, `evidence/p1-roster-probe.txt`, `evidence/p1-history-probe.txt`; `02-review.md` §Iteration 2.

### LED-2026-10-02-batch-04.9 — P2 iteration 3 notes folded at the gate
- **Requirement:** HLR-403, HLR-404, LLR-401.3, LLR-404.1, LLR-404.2
- **Date:** 2026-10-03
- **What changed:** LLR-404.2 becomes one roster cleaner `clean_roster` read by `TeamState.roster` and by the Setup view's roster read and republish; LLR-404.1 applies only the first entry of each id (existing projects too), keeps the boolean guard on a synced `archived`, and gains `archived`/`pinned` and start-date arms; HLR-404's AT names the identity states, clicks each status cell, asserts one line per id; TC-415's base flags are recorded before the conversion; AT-406's long name is pinned with the continuation-row x asserted; the file-backed image branches take the bracket payload only; D-412 states the function-local palette import; D-414 accepts synced phases and project extras as cleaned (bounds → BACKLOG).
- **Why:** P2 iteration 3 — architect A3-1 (major: the Setup roster bypassed LLR-404.2), A3-2; security S3-1, S3-2; qa Q3-1 (major: untested `archived`/`pinned`/start clauses), Q3-2..Q3-6; ux UX3-1, UX3-2.
- **Evidence:** `02-review.md` §Iteration 3.

### LED-2026-10-02-batch-04.10 — P3 increment 001 amendments
- **Requirement:** LLR-401.1, LLR-401.3
- **Date:** 2026-10-03
- **What changed:** §6.5 A-1..A-4: the census declares seven sites (the two board repaints added) and trusts a `-> Text` function only when its returns are markup-inert; the details/viewer title is bold as base paints it (the CSS bolds the row); TC-417 and D-415 (an empty highlight no longer crashes the board); `_init_team_mode` named.
- **Why:** increment 001's tester round 1 and code review F1, F2; the `====` crash found while splitting the tokeniser.
- **Evidence:** `evidence/inc001-red-on-base.txt`, `evidence/inc001-red-census-base.txt`; `03-increments/increment-001.md`.

### LED-2026-10-02-batch-04.11 — the second increment, revision 2
- **Requirement:** LLR-402.1, LLR-402.3, LLR-404.1
- **Date:** 2026-10-03
- **What changed:** an empty synced project id is refused (D-416); a file nested deeper than the cleaning can follow is refused at both doors, `team.json` with a visible toast (D-417); Setup stages the first entry with validated values (D-418); `strip_controls` loses its dead CR-LF replace; TC-418, TC-419 and the TC-410 keep-everything-else arm are new.
- **Why:** P3 code review F1 (HIGH: the board grew one project per sync tick), F2, F3, F4; security S4-1 (MEDIUM: a ~1000-level `team.json` crashed every teammate's startup); the battery's equivalent mutant N4; operator ruling at the P3 gate, 2026-10-03: "Corregir todo en el 002".
- **Evidence:** `evidence/inc002-red-r2.txt`; `03-increments/increment-002.md`.

### LED-2026-10-02-batch-04.12 — the details grid's test reaches its address
- **Requirement:** LLR-403.1
- **Date:** 2026-10-03
- **What changed:** IFC Part B `details-info-grid` names `tests/test_details_grid.py` as a consumer (amendment A-6).
- **Why:** increment 003 created the node that asserts on `#details-box .modal-grid`; `V13` reported it as an undeclared file reaching the address.
- **Evidence:** `03-increments/increment-003.md`.

### LED-2026-10-02-batch-04.13 — the operator's visual verdict applied (UX-3, UX-4)
- **Requirement:** HLR-403, LLR-403.1
- **Date:** 2026-10-04
- **What changed:** amendment A-7. *Before:* two blank rows above the details title and none below it; a 20-cell label column (values at x 44 / 26 at 140×40 / 80×24); the 89-character name wrapped over 3 rows at 80×24. *After:* one blank row above the title and one below (the row moved, none added); a 10-cell label column (x 34 / 16); the long name over 2 rows at 80×24. New TC-420 (title gap) and TC-421 (label column). HLR-403's statement is unchanged; its threshold's coordinates and row count follow the rule. D-406 resolved: PV-1 accepted.
- **Why:** the operator's verdict on the provisional captures, 2026-10-04 — PV-1 "Aceptar", UX-3 "Aplicarlo", UX-4 "Aplicarlo" (`evidence/operator-verdict-provisional.json`); the batch re-opened to P3 (D-422).
- **Evidence:** `evidence/inc004-probe.txt`; `03-increments/increment-004.md`.
