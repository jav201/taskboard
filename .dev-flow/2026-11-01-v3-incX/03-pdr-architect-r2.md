# Inc X — E3 code-free design review (PDR), architect, round 2

**Verdict: PASS-WITH-NOTES.** BLOCKER 0 · MAJOR 0 · HIGH 0 · MEDIUM 2 · LOW 2 · MINOR 2.

All three round-1 MAJORs (F-1, F-2, F-3) are resolved as rulings 12, 13 and 15 direct. The six MEDIUMs are resolved as rulings 16–21 direct, and so are the LOW and MINOR fixes. The two new LLRs are EARS, have a threshold and a negative control, and are traced. All three graphs lint clean. Six new findings remain, none blocking:

- **R2-1 (MEDIUM):** HLR-4502's statement still says "does not draw". This is the last trace of F-2.
- **R2-2 (MEDIUM):** the URL-cleared oracle of LLR-4501.3/.4 can be read as a tautology.

Fix both with targeted text edits before the E4 hand-off. Neither needs a round 3.

Reviewed at `279356e` (worktree `C:\Users\jjgh8\Github\taskboard-wt\x-html`). `git diff 509d444 HEAD -- taskboard tests` is empty, so the source is still at base. Scope, per the skill's E3: round 1's blocking findings, the MEDIUMs, and any new defect the correction brought in.

**Probe E3-P2.** This was a read-only temp script, deleted after use. It ran with `taskboard.__file__` = `…\taskboard-wt\x-html\taskboard\__init__.py`. It swapped `keymap.KEYMAP` in memory to put `H` at its current seat with `bar=True, primary=True`. It then measured `fit_bar` and `key_bar_plain` over 10 views × {80, 118} × {primary, more}, and ran the negative controls of LLR-4505.2 and LLR-4505.3.

## Round-1 findings, re-checked

| Finding | Ruling | State | Evidence |
|---|---|---|---|
| F-1 MAJOR `present_name` module / import cycle | 12 | ✓ resolved | `graph-interfaces.cw.md` node `present_name`: `module: taskboard/views.py`, `in: str? project_name; date today`, with a function-local `from .report_html import slug`. The same in proto-B. `e2-seams.md` S-3 and §6 row 8 match. A grep for `report_deck\.present_name` gives 0 hits. The only remaining mention is in the resolved finding I-4. |
| F-2 MAJOR deck scope vs ruling 2 | 13 | ✓ resolved, one remnant (R2-1) | The Definitions row "shown task" (`01-requirements.md:33`) now reads "the tasks the presentation does not hide; its views draw the open ones as rows and count the done ones". Ledger LED-…incX.4 names LLR-4501.8 and LLR-4501.9. `present_deck_boards` uses `present_tasks_m(board, p.id)[1]`, and "Folds (`_folded`) are not read". |
| F-3 MAJOR law guard RED by design | 15 | ✓ resolved | §6 (`01-requirements.md:251-254`) names `test_colour_budget_app.py` (`KEYBAR_BASE`) and TC-4321 with their new values. `e3-addenda.md` item 1 gives the two exact strings. E3-P2 reproduces both byte for byte: gantt 80 primary `… d  L  H  ↓  ↑`, gantt 118 more `… /  H  ↓ +3`. |
| F-4 MEDIUM `H` seat | 16 | ✓ | §6 row 15, the `fit_bar` node and LED-…incX.9 put `H` at its current seat. E3-P2 reproduces every cell of the `e3-addenda.md` table: primary 0 violations of LLR-4505.1–.3 over 20/20 cases, and `H Report` first fits at 193 columns. The NCs reproduce as well: promoting all globals makes 10/20 RED (LLR-4505.2); `H` universal makes 7/20 lose 2+ words (LLR-4505.3). The false sentence in `fit_bar` is gone. |
| F-5 MEDIUM byte-identity While clauses | 17 | ✓ | LLR-4501.3 now reads "While the presented board is in the registry and …". LLR-4501.4 now says "… or a milestone of a hidden class". Both are recorded in LED-…incX.5, and P-A-6 is resolved. |
| F-6 MEDIUM missing / archived presented project | 18 | ✓ | `present_deck_boards` falls back "exactly as `render_present`". LLR-4501.15 is new. The archived case is in the BACKLOG list of `e3-addenda.md`. One gap remains (R2-4). |
| F-7 MEDIUM slice under-count | 19 | ✓ | §6 has 16 rows: 5 removed (9–13), 5 new (2, 4, 5, 7, 8) and 6 changed (1, 3, 6, 14, 15, 16). That matches the count line. It has an ARCHITECTURE.md row. `__init__` correctly falls out, because there is no `_export_offer` (F-12). |
| F-8 MEDIUM superseded canon | 20 | ✓ | LED-…incX.8 names every id I listed. It adds LLR-1905.1 and LLR-2104.1, and both exist (`REQUIREMENTS.md:229`, `:245`). |
| F-9 MEDIUM unruled proposals | 21 | ✓ | `grep "decision: proposed" graph-*.cw.md` gives 0 hits. Every P-A-n and P-B-n reads "resolved" with its ruling. |
| F-10 LOW | 21 | ✓ | LLR-4504.1's threshold uses the addendum wording. |
| F-11 LOW | 21 | ✓ | LLR-4501.2, AT-4502, `present_name` and TC-4702 read `present-<date>.html`. The `present-all` hits that remain are in the historical ledger entry LED-…incX.3 only, and the ledger is append-only. |
| F-12 LOW | 21 | ✓ | `[Data: TaskboardApp._report_offer]` is shared. `action_open_export` reads it and clears it. After `esc`, the main screen's `o` consumes the same slot (`app.py:4667-4674`, unchanged), so the toast stays true. One wording gap remains (R2-3). |
| F-13 MINOR | 21 | ✓ | `e3-addenda.md` item 7. HLR-4501's NC is fixed. |

## New LLRs (LLR-4501.15 missing project, LLR-4502.7 URL strip)

The brief names them the other way round: LLR-4501.15 is the missing project and LLR-4502.7 is the URL strip.

- **LLR-4501.15.**
  - Form: Unwanted, "If … then the system shall …", with one `shall`.
  - Threshold: 1/1. It tells the two projects apart (Alpha held, Beta not) and expects 0 exceptions.
  - NC: "None in the proxy or keep the missing id".
  - Traced in the interfaces and in proto-A/B (TC-4715, `e2-trace.txt:20`).
  - The case is reachable: `present_project_id` returns a focused id or a selected task's `project_id` without checking that the project exists (`views.py:6633-6637`).
- **LLR-4502.7.**
  - Form: Unwanted, with one `shall`.
  - Threshold: 3/3 views.
  - Traced (TC-4727, `e2-trace.txt:27`).
  - The NC is not vacuous. `extract` emits `t.urls` (`report_html.py:153`) and the deck renders them (`report_deck.py:341`). The proto-A example also asserts that `H`'s deck of the original board keeps the URL, which is the positive control. The NC's wording is weak (R2-6).

## Findings

### R2-1 — MEDIUM — HLR-4502's statement still says "does not draw", against ruling 13
- **Seen:** `01-requirements.md:63` reads "The system shall leave out of the deck's bytes every project and task the presentation **does not draw**."
  - The presentation does not draw done tasks as rows. It only counts them (round 1, F-2).
  - LLR-4501.9 and ruling 13 hold those tasks in the deck.
  - So the parent HLR still contradicts its children. The HLR's title, "what the presentation hides …", is correct. The statement is not.
- **Why not MAJOR:** HLR-4502's threshold is the sentinels of LLR-4502.1..7, and those follow ruling 13. No test is written to the HLR's sentence alone.
- **Fix:** "… every project and task the presentation hides" (or "does not show", per the Definitions row). Record it in one ledger line that names HLR-4502 under ruling 13.

### R2-2 — MEDIUM — the URL-cleared oracle of LLR-4501.3/.4 can be read as comparing the proxy with itself
- **Seen:**
  - LLR-4501.3/.4 compare with "the deck `H` writes … from **the same proxy board** with every held task's `urls` cleared".
  - Proto-B's TC-4703 example says "the deck's bytes equal `H`'s over the same proxy".
  - If the tester builds the reference from `present_deck_boards`'s output, both sides run `render(extract(proxy, key))`. The test can then catch only a wrong key, wrong people or marks, a wrong date or a wrong write mode.
  - It can no longer catch a proxy that changes something other than URLs: for example notes dropped, or a task field altered by the copy. Catching that was the point of byte identity with `H`. The While clauses ("nothing hidden …") only make sense against the real board.
- **Fix (text only):** in LLR-4501.3/.4, TC-4703/TC-4704 and the `_on_report_chosen` examples, write the reference as "`H` → `c` over **the same board saved with every task's `urls` emptied**". That is an independent fixture copy, built without calling `present_deck_boards`. Optionally add an NC: "the proxy copy clears the notes as well: RED".

### R2-3 — LOW — the "after `esc`" arm of the shared offer has no requirement, and is filed under the wrong node
- **Seen:**
  - The `action_open_export` node's TC-4733 example and `e3-addenda.md` item 6 test `x`, `esc`, `o` → 1 call.
  - After `esc` the key goes to `TaskboardApp.action_open_url` (`app.py:4667-4674`), not to `action_open_export`.
  - LLR-4503.2/.3 say "in the presentation". LED-…incX.10 says the LLRs cover the case "including after leaving `R`", but their text was not changed.
- **Fix:** move that arm to a `TaskboardApp.action_open_url` example (UNCHANGED node), traced to LLR-4503.1 ("o opens it (10 s)": the toast's promise). Alternatively, widen LLR-4503.2's event to "When `o` is pressed while an offer is live" and record the change in the ledger.

### R2-4 — LOW — views 1/2 with no project at all take view 3's file name and scope
- **Seen:**
  - Proto-A step (4) sets `key = None` and `project_name = None` when the proxy holds no project. That happens when the id is missing and no project is visible.
  - `present_name(None)` returns view 3's `present-<date>.html`.
  - `extract(project=None)` then writes a deck scoped "All loaded boards".
  - LLR-4501.1 does not cover this state. It is reachable, rarely: through a dangling focused or selected id on a board whose projects are all archived (`views.py:6633-6639`).
- **Fix (cheapest):** in views 1/2, pass `project_name = project.name if project else ""`. `present_name("")` then gives `present-project-<date>.html`, the empty-slug rule, so view 3's file is never overwritten. Record the "All loaded boards" cover of this state as a BACKLOG known limit.

### R2-5 — MINOR — `project_name`'s conditional exists only to keep `_project_name` alive
- **Seen:**
  - Step (4) reads `self._project_name if self._board.project_by_id(pid) is not None else project.name`.
  - When `project_by_id(pid)` is not None, `project` is that project, and `_project_name` was set from `proj.name` at `app.py:2988-2991`. Both arms therefore give the same value.
  - The second lookup adds nothing.
- **Fix:** use `project.name` (with R2-4's `""`), and log `_project_name` as write-only in BACKLOG. That is the other option F-13 offered. `e3-addenda.md` item 7 then changes to match.

### R2-6 — MINOR — LLR-4502.7's NC names the symptom, not a mutant
- **Seen:** "leave a task URL present in the file" restates the failure.
- **Fix:** "copy the held tasks without clearing `urls`: RED" (the mutant of `present_deck_boards`).

## Consistency checks that pass (evidence)

- **Lint:** `codewire_lint.py` reports:

  | File | Nodes | Entities | Edges | Findings | not read | exit |
  |---|---|---|---|---|---|---|
  | `graph-interfaces.cw.md` | 5 | 3 | 7 | 4 | 0 | 0 |
  | `graph-proto-A.cw.md` | 12 | 6 | 8 | 7 | 0 | 0 |
  | `graph-proto-B.cw.md` | 8 | 4 | 4 | 4 | 0 | 0 |

- **Trace:** I extracted the script embedded in `e2-trace.txt` and re-ran it on this head. It exits 0, and its output is identical to the committed listing (`diff --strip-trailing-cr`): 42/42 LLRs and 6/6 ATs traced.
- **Counts:** §7 says LLR 42 (15+7+7+3+5+5), which matches §4. §6 has 16 units in 3 source files.
- **No stale design text:** these terms give 0 hits outside resolved findings and historical ledger entries:
  - `report_deck.present_name`
  - `_export_offer`
  - `13 units`
  - `present-all` as a live name
  - `after ↑`
- **No identity hazard in the shallow task copies:** `Board.project_by_id` and `task_by_id` are linear scans over `self.projects` and `self.tasks` (`models.py:1185-1193`), with no cached index. A `copy.copy(board)` with new lists therefore resolves to the copies.
- **The `--open` key path still matches `H` where LLR-4501.3 applies:**
  - `H` builds `bid if bid is not None else '#<pos>'` (`app.py:3005-3009`).
  - `x` uses `#0` only for an unlisted board, which the new While clause excludes.

## Evidence checklist (architect)

| Item | State | Evidence |
|---|---|---|
| Constraints stated | ✓ executed | the 4-source-file budget (3 used, §6); X-4 freeze; rulings 12–22 |
| 2+ alternatives where a real decision exists | ✓ | R2-3 (move the arm vs widen the LLR). Every other decision: `n/a — already ruled in 12–22` |
| Non-applicable constraints marked | ✓ | cost and latency: `n/a — local file write, no network, no model call`; lock-in: `n/a — the Edge dependency removed, none added` |
| Recommendation tied to constraints | ✓ | each fix cites a ruling, an LLR or a code line |
| Risks listed | ✓ | a tautological oracle (R2-2); a name collision (R2-4); an HLR/LLR contradiction (R2-1) |
| Cost / latency | `n/a — no runtime cost change` | |
| Diagram | `n/a — the three graphs are the diagram; no new flow` | |
| What would change the verdict | ✓ | R2-1 or R2-2 left unfixed when E4 starts → treat as FAIL at E5. R2-3..R2-6 may go as E4 addenda |
| Two-layer requirements | ✓ executed | US-4501 → AT-4501..4506; US-4501 → HLR-4501..4506 → 42 LLR → TC-47nn; `e2-trace.txt` re-run, 42/42 and 6/6 |
