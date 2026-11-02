# Inc X — E3 code-free design review (PDR), architect

**Verdict: FAIL** — 3 MAJOR open. BLOCKER 0 · MAJOR 3 · HIGH 0 · MEDIUM 6 · LOW 3 · MINOR 1.

The direction is sound. `x` reuses the existing extraction and renderer, and the scope is filtered through a never-saved proxy that reads the presentation's own hide functions. The removals are dead-end leaves, and `o` gets its own priority binding on the modal. Three things block E4:

- **F-1:** the design and ruling 11 put `present_name` in different files, and the file ruling 11 names cannot import `slug` at module level.
- **F-2:** ruling 2 ("the deck draws exactly what the presentation draws") contradicts LLR-4501.8/.9, and the graph follows the requirements.
- **F-3:** a law guard the commission names, `tests/test_colour_budget_app.py`, goes RED by design, and finding P-A-4 measured the fit wrong.

Reviewed at `82d8d4c` (worktree `C:\Users\jjgh8\Github\taskboard-wt\x-html`). Source under `taskboard/` and `tests/` is unchanged since base `509d444`. Line numbers below are at the head commit.

**Probe E3-P1** (read-only, deleted after use). This was a temp script with cwd = this worktree; `taskboard.__file__` = `…\taskboard-wt\x-html\taskboard\__init__.py`. It swapped `keymap.KEYMAP` in memory for two seats of `H`:

- (a) after `↑`, as the graph designs it;
- (b) at its current seat, with `bar=True, primary=True`.

It printed `fit_bar` / `key_bar_plain` for the 10 main views at 60, 70, 80 and 118 columns. Its results are cited as (E3-P1).

## Findings

### F-1 — MAJOR — `present_name`: the design and ruling 11 disagree on the module, and the module ruling 11 names would make a circular import
- **Seen:**
  - Ruling 11 says `present_name` "lives in `views.py`", with "no edit".
  - The design still puts it in `report_deck.py` in five places:
    - `graph-interfaces.cw.md`, its header ("Group B owns views.py + report_deck.py (ruling 9: the name goes in `report_deck.py`)") and node `present_name`, `module: taskboard/report_deck.py`;
    - `graph-proto-B.cw.md`, its header and node `present_name`;
    - `graph-proto-A.cw.md` node `PresentScreen.action_export` step (5), `report_deck.present_name(d)`;
    - `e2-seams.md` S-3, `report_deck.present_name(d)`.

  Ruling 9 itself does not name a module.
- **Hazard:** the node's slug is `report_html.slug`, and `report_html.py:26` imports `views` at module level. `app.py:23` imports `report_html` first, so a module-level `from .report_html import slug` in `views.py` would run while `report_html` is still half-initialised. `slug` is defined at `report_html.py:177`, after that import, so `import taskboard.app` would fail with an ImportError. Group B, working from ruling 11 alone, would hit this.
- **Also:** the node takes the report dict `d`. That would make `views.py` read the report's schema: `scope.project` and `projects[].name`, the shape `_scope_slugs` reads at `report_html.py:191-199`. `views.py` has no other reason to know that shape.
- **Fix (targeted edits; the orchestrator owns `graph-interfaces.cw.md`):**
  1. Make the node `module: taskboard/views.py`, with `in: str? project_name; date today` and `out: str name`. It returns `present-<slug or "project">-<today>.html` for a name, and `present-all-<today>.html` for `None`.
  2. Take the slug through a function-local `from .report_html import slug`. This is the pattern `report_html.write_reports` uses (`report_html.py:213-218`, "imported here, not at module level: they import this module"), and it keeps one slug rule (TC-3123).
  3. Group A calls it with the presented project's name (view 1/2) or `None` (view 3), and the same `today` that goes to `extract`.
  4. Edit, to match: S-3; proto-A step (5); the headers of interfaces and proto-B; the examples TC-4701/4701b/4701c/4702, whose input becomes a name, not a scope key.

  The source budget is unchanged: 3 files, and `report_deck.py` is untouched, as ruling 11 intends.

### F-2 — MAJOR — what the deck holds: ruling 2 says "what the presentation draws", but LLR-4501.8/.9 and the graph hold folded and done tasks
- **Seen:**
  - Every view of the presentation draws only open tasks as rows:
    - `render_present`'s docstring says "only the shown open tasks" (`views.py:7263-7265`);
    - its rows iterate `open_t` (`views.py:7287-7310`), and done tasks appear only as the count `N done`;
    - view 3's `_all_plan` takes `present_tasks_m(...)[0]`, the open tasks (`views.py:7423-7425`);
    - `enter` folds a project's rows away.
  - Ruling 2 says: "The deck draws exactly what the presentation draws … The presentation is the oracle. Each test compares the deck's set of tasks against the presentation's set of shown tasks."
  - LLR-4501.9 holds done tasks in views 1 and 3. Its negative control is literally "open tasks only (view 3's frame population): RED".
  - LLR-4501.8 holds folded projects whole.
  - The Definitions row "shown task … the tasks the presentation's views draw, open and done" is factually wrong: the views draw open tasks only.
  - The graph follows the LLRs (`present_deck_boards`: "open and done"; TC-4708, TC-4709).
- **Effect:** read literally, ruling 2 drops done and folded tasks. That breaks ruling 8's byte identity with `H` → `c`: fixture X's done task `a2` is in `H`'s deck. Testers given ruling 2 and testers given the LLRs would write opposite oracles.
- **Fix (orchestrator ruling, then targeted edits):** rule that the deck's scope is **what the presentation does not hide**, meaning:
  - the saved hide flags: task, project and milestone class;
  - archived tasks, tasks of archived projects and tasks without a project, which the presentation never draws.

  The drawing state stays out of the scope: the open/done split, folds, the cursor and timeline overflow.

  Reasons:
  - It is the only reading under which ruling 8's byte identity holds.
  - The privacy promise of X-1 ("hidden … excluded from the bytes") is about the hide flags. `u` lists hidden tasks "open or done" (`present_hidden`, `views.py:6680-6683`).
  - Folds are per-presentation, unsaved state (`app.py:263`).

  Then:
  1. Amend ruling 2's oracle to "`present_tasks_m(board, pid)[1]` per held project, not the frame's rows".
  2. Fix the Definitions row to read: "the tasks the presentation does not hide; its views draw the open ones as rows and count the done ones".
  3. Write one ledger entry naming LLR-4501.8 and LLR-4501.9.

### F-3 — MAJOR — a named law guard is RED by design, and P-A-4's measure is wrong
- **Seen:**
  - `tests/test_colour_budget_app.py:467-484` (`KEYBAR_BASE`, used by TC-203/204) pins two exact bars:
    - `("gantt", 80, "primary")` = `"… d  L  ↓  ↑"`;
    - `("gantt", 118, "more")` = `"… /  ↓  ↑ +2"`.
  - With `H` on the bar, the first gains `H` in either seat (E3-P1).
  - The second becomes `"… /  ↓  ↑ +3"` with seat (a) and `"… /  H  ↓ +3"` with seat (b). Kanban at 118 "more" goes from 6 dropped to 7.
  - Finding P-A-4 says "at 118 nothing is dropped either way" and "no test pins `+12`". It measured swimlanes only.
  - The commission lists `tests/test_colour_budget*.py` among the E5 law guards. §6's list of touched tests does not name this file.
  - `tests/test_added_list.py:880-881` (TC-4321) pins `global_keys("gantt")` with `"H"` between `"n"` and `"@"`. §6 does not name it either: "any key-bar test that pins `H` as `bar=False`" does not cover it.
- **Fix:**
  1. Re-measure P-A-4 over the 10 views × {80, 118} × {primary, more}, and record the table.
  2. Add both tests to §6's list with their new expected values.
  3. E4 updates `KEYBAR_BASE` in that file's own convention: a "batch … added `H` (Report): …, law-driven" comment and an evidence file, as the `B` entry at `:470-472`/`:480-482` does. That is a recorded re-baseline with its cause, not a weakened guard.
  4. TC-4321's expected list drops `"H"`, and the packet justifies the change.

### F-4 — MEDIUM — `H`'s seat: moving it after `↑` is a larger change than needed, and its stated benefit is false
- **Seen:** the design's stated benefit is false, and the design gives no reason for the move beyond it.
  - The graph moves the `H` row after `Key("up,k", …)` (`keymap.py:175`), "so … its word goes first and it is never dropped while a key left of it stands".
  - `fit_bar` drops keys **from the right** (`entries.pop()`, `keymap.py:318-321`), so the last entry is the **first** key to go.
- **E3-P1, both seats:** both meet LLR-4505.1–.3 at 80 and 118 columns: `H` drawn 20/20, at most 1 base word lost, no key dropped. They differ in four ways:

  | | Seat (a), after `↑` | Seat (b), current seat |
  |---|---|---|
  | `H` drawn at 60 columns | 0/10 views | 4/10 views |
  | `H Report` with its word | from 201 columns | from 193 columns |
  | "more" layer and `?` band | `↓ ↑ H ← →`: `H` splits the arrows | `… / H ↓ ↑ ← →` |
  | Palette order | changes | unchanged |
- **Fix:**
  1. Keep `H` at `keymap.py:152` and flip it to `bar=True, primary=True`, a one-row diff. Update its comment, which says "global, off the bar"; the `N` comment at `:144-146` also names "H Report".
  2. Re-measure TC-4753/TC-4754 for seat (b).
  3. Ruling 1's "about 201 columns" becomes "about 193". The wide capture at ≥ 201 columns still shows `H Report`.

  If the orchestrator keeps seat (a), the false sentence in `fit_bar`'s `func:` must still be corrected.

### F-5 — MEDIUM — LLR-4501.3 and LLR-4501.4 claim byte identity in states where the bytes differ
- **Seen:**
  - LLR-4501.4's While clause does not exclude hidden milestone classes. `x` drops their milestones (`present_tasks_m`, `views.py:6651-6662`). `H`'s `extract` keeps them: `report_html.py:136` checks only `t.mark in marks`, never `hidden`.
  - LLR-4501.3's While clause does not exclude an unlisted (`--open`) board. `H` keys that board `#<pos>`, where pos comes after every loaded registry board (`app.py:876-879`, `:3005-3009`); `x` keys it `#0`. The key reaches the bytes as `data-project` (finding P-A-6, still "proposed").
- **Fix:**
  1. Add "and no milestone of a hidden class" to LLR-4501.4's While clause.
  2. Add "and the presented board is in the registry" to LLR-4501.3's.
  3. Write one ledger entry naming both. P-A-6 is then resolved by the amendment.

### F-6 — MEDIUM — views 1/2 when the presented project is not on the board (crash), or is archived
- **Seen:**
  - `action_present` anticipates a missing project (`proj.name if proj else None`, `app.py:2988-2991`).
  - `render_present` then falls back to the first visible project (`views.py:7281-7286`).
  - `present_deck_boards` sets `proxy.projects = [board.project_by_id(project_id)]`, which is `[None]` in that case. `extract`'s `for p in board.projects: … p.id` (`report_html.py:105-106`) then raises AttributeError inside `R`.
  - An archived presented project is drawn by the frame, but the deck keeps no slide for an archived project (baseline P-4), so its deck would be empty.
- **Uncertainty:** I did not prove the dangling id is reachable. It needs a selected task or focus that names a deleted project.
- **Fix:**
  1. `present_deck_boards` resolves the project exactly as `render_present` does: `project_by_id`, else the first visible project, else none (an empty projects list, which LLR-4501.12's sentence already covers).
  2. Add one Unwanted LLR with an example: "If the presented project is not on the board, then the deck holds the project the frame shows".
  3. Record the archived case as a known limit in BACKLOG. A guard for it is not worth the code.

### F-7 — MEDIUM — the slice (§6) under-counts, and ruling 11's "13 units is correct" does not hold
- **Seen:**
  - §6 has 13 rows and "2 new". The graph has five new units: `PresentScreen.action_open_export`, `views.present_deck_boards`, `present_name`, `PresentScreen._deck_lane` and `TaskboardApp._write_report`. Row 3 only describes the last of these; it is not named. `PresentScreen.__init__` also changes (`_export_offer = None`).
  - `docs/ARCHITECTURE.md` (:42, :48, :70, :117, :122, :131; Edge as an outside system) is in no row. P-B-4 proposes editing it.
  - The touched-tests list misses the two tests named in F-3.
- **Fix:** targeted edits to §6, with one ledger entry:
  - add rows for the three unnamed new units and for `__init__`;
  - correct the count line to "16 units in 3 source files — 5 removed, 5 new, 6 changed";
  - add a docs row for `docs/ARCHITECTURE.md`;
  - add the tests from F-3.

### F-8 — MEDIUM — the requirements canon that X-2 overrides is not named
- **Seen:** `REQUIREMENTS.md` still holds active requirements that X-2 contradicts:
  - HLR-2404 and LLR-2404.1 (`:277`, `:289`);
  - HLR-2903 and LLR-2903.1 (`:378`, `:384`: "save_present_svg, present_paths and present_all_export shall stay byte-unchanged");
  - LLR-1803.3 (`:219`);
  - LLR-3107.5 (`:412`: "No change shall reach views.present_paths, views.save_present_svg, …");
  - the "with its exports" clause of HLR-2607 (`:325`).

  P-B-4 defers all of this to the batch-end fold, unruled.
- **Fix:** add one ledger entry now that names each id as superseded by HLR-4504 (HLR-2607: only its export clause, now carried by the deck's legend, LLR-4502.5). The batch-end fold then becomes mechanical, and the E5 reviewers can see the conflict is intended.

### F-9 — MEDIUM — E2 proposals that are still unruled
- **Seen:** P-A-2, P-A-3, P-A-5, P-A-6, P-A-7, P-B-1, P-B-3 and P-B-4 are all `decision: proposed`. E3 requires a ruling on every proposal, and the commission says to record decisions in `03-pdr-rulings.md`.
- **Recommendation:**

  | Proposal | Recommended ruling |
  |---|---|
  | P-A-2 | accept: action `open_export`, words per LLR-4506.2 |
  | P-A-3 | accept: no width check on `o`, since nothing on screen changes |
  | P-A-5 | accept: `date.today()` at the press, as `H` |
  | P-A-6 | resolved by F-5 |
  | P-A-7 | accept |
  | P-B-1 | accept, no guard: TC-4710 (sha256) and `test_TC_3101_extract_never_writes_a_board` cover it; the security reviewer confirms |
  | P-B-3 | accept the lane signature, and amend §6 row 5 to match |
  | P-B-4 | accept, with F-7 (ARCHITECTURE.md) and F-8 (canon) |

### F-10 — LOW — LLR-4504.1's "exactly 1 new file per press" contradicts LLR-4501.1 and AT-4501
- **Seen:** views 1 and 2 write the same file (LLR-4501.1). AT-4501 is "`2`, `x` → the same file, rewritten", so the second press creates **no** new file. A literal test of TC-4741 in one session is RED by design.
- **Fix (E4 addendum):** "after each press, `reports/` holds that scope's `present-*.html`, 0 `.svg` and 0 `.png`, and no other file is new or changed".

### F-11 — LOW — the name `present-all-<date>.html` collides with a project named "All"
- **Seen:** P-B-2. Ruling 9 accepted the collision: `slug("All")` = `all`.
- **Fix (optional, operator's call):** name view 3's file `present-<date>.html`. It can never equal `present-<slug>-<date>.html`, because a non-empty slug always adds a segment. Otherwise keep ruling 9 as it stands.

### F-12 — LOW — `x`'s offer dies with `R`, while its toast lives on
- **Seen:**
  - The toast says "o opens it (10 s)".
  - If the presenter leaves with `esc` inside those 10 s, `o` on the main screen opens the selected task's URLs instead (`app.py:4667-4683`): the `PresentScreen._export_offer` slot has died with the screen.
- **Fix (simplification, for the orchestrator; it revises ruling 6's second clause):** store `x`'s offer in the existing `TaskboardApp._report_offer`, and let `PresentScreen.action_open_export` consume that same slot.

  This removes the entity `[Data: PresentScreen._export_offer]`, leaves one offer and one expiry rule, and keeps the toast true after `esc`. The cost: an `H` offer still live when `R` opens becomes usable from `R`, which does no harm. LLR-4503.5 then withdraws the app's slot.

  If ruling 6 stands, record this as a known limit.

### F-13 — MINOR — stale text and dead state left by the change (E4 addenda)
- **Stale text:**
  - the `PresentKeys` docstring "Never exported: `x` writes the frame only." (`modals.py:2133`; `modals.py` is outside the slice, so it goes to BACKLOG, not a 4th source file);
  - the census reason "shared with the x export" (`tests/test_markup_census.py:91`);
  - HLR-4501's negative control "(no `deck-*.html`)": at base TC-4701 is RED because no `present-*.html` exists. Ruling 11 calls the parenthetical deliberate, but the NC it describes is "base `x` writes an `.svg`".
- **Dead state:** `PresentScreen._project_name` (`app.py:257`, `:466`) becomes write-only once `present_paths` goes. Either feed it to `present_name` (F-1) or log it in BACKLOG. Removing it would change the constructor and its tests, which is scope creep.

## Checks that pass (evidence)

- **Removals are safe, with one ordering condition.**
  - grep `save_svg|msedge|--screenshot|present_paths|present_all_export` over `taskboard/*.py` finds 13 hits, all in `app.py` and `views.py`. `__main__.py`, `report.py`, `modals.py` and `report_html.py` have none.
  - In `views.py`, `os.` (`:7360`, `:7370-7371`), `shutil.` (`:7376`) and `subprocess.` (`:7394-7395`) are used only inside the removed functions. `Console` stays, for `_SEARCH_CONSOLE` (`:4135`).
  - `_all_timeline`'s `anchor` has the single caller `views.py:7665`.
  - No test patches `views.os`, `views.shutil` or `views.subprocess`.
  - The ordering condition is S-7: the `app.py` imports at `:55`, `:57`, `:59` and `:61` must go in the same integration step as the removals.
- **The deck writes nothing to the board.** The proxy is `copy.copy` with new lists only, the pattern of `_hide` at `views.py:3151-3160`. `extract` is read-only, and LLR-4501.10 is the sha256 oracle for it.
- **No leaks through dependencies or notes.** `extract` builds deps only from `in_scope` (`report_html.py:148`), and mentions and notes only from the held tasks. Hidden tasks do not reach the bytes through dependencies, chains, people or marks (`used` at `:159`).
- **`o` inside the modal works.** The `PRESENT_KEYS` bindings are all `priority=True` (`keymap.py:250-253`), and the app's `o` is not priority (`keymap.py:134`), so the screen's `o` wins while `R` is the top screen. Above `R`, `PresentKeys`/`PresentHiddenPicker` hold their own keys, so `x`/`o` cannot fire beneath them. TC-3120's "`o` over another screen" arm uses `?`, not `R` (`tests/test_report_export_app.py:395-399`), and is unaffected. The `?` window lists the `o` row through `PresentKeys.lines`, with no code change (`modals.py:2146-2161`).
- **Presentation scope.** View 3 uses `present_order` filtered by `show_in_present` (`models.py:2476-2484`). Views 1/2 hold the presented project whatever its own flag (LLR-4501.5). Hidden classes are dropped through `present_tasks_m`. The legend follows the held tasks (`report_html.py:159-171`). Hide flags are read at the press (S-8).
- **The deck's bytes.** `x` writes with `path.write_text(render(d), encoding="utf-8")`, the same call as `write_reports` (`report_html.py:220`), so the newline handling matches as well (ruling 8).
- **The file name** cannot overwrite `H`'s `deck-…`/`workspace-…` files (`report_html.py:182-188`). The slug is alphanumeric and `-` only, so it cannot carry a path through the name.
- **Narrow rule and hint row.** The narrow rule is unchanged (LLR-4501.13/.14), and so is the hint row (ruling 10, LLR-4506.4).

## Evidence checklist (architect)

| Item | State | Evidence |
|---|---|---|
| Constraints stated | ✓ executed | the commission's budget of 4 source files (3 used); X-4 freeze; the Textual modal binding chain (baseline P-6) |
| 2+ alternatives where a real decision exists | ✓ executed | `H` seat (a) vs (b), measured (F-4); offer slot on the screen vs the app (F-12); `present_name` placement (F-1). The deck writer itself: `n/a — decided by X-1 ("the same writer `H` → `c` uses")` |
| Non-applicable constraints marked | ✓ | cost and latency: `n/a — local file write, no network, no model call`; vendor lock-in: `n/a — the Edge dependency is removed, none added` |
| Recommendation tied to constraints | ✓ | each fix cites a ruling, an LLR or a code line |
| Risks listed | ✓ | crash path (F-6); circular import (F-1); law-guard RED (F-3); stale canon (F-8) |
| Diagram | `n/a — the graph files are the diagram; the change adds no new flow beyond the S-1..S-8 seams` |
| What would change the verdict | ✓ | rulings plus targeted edits for F-1, F-2 and F-3 → PASS-WITH-NOTES, with F-4..F-9 ruled and F-10..F-13 as E4 addenda |
| Two-layer requirements | ✓ executed | US-4501 → AT-4501..4506 (behavioural) and US-4501 → HLR-4501..4506 → 40 LLR → TC-47nn (functional); `e2-trace.txt`: 40/40 LLRs and 6/6 ATs traced |
