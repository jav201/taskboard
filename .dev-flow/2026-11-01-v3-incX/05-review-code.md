# Code Review — Inc X (E5), `x` writes the HTML deck

Reviewer: `code-reviewer` (independent, read-only, Opus 5.5). Head `f55bb4b`, base `8506cb7`.

**Verdict: PASS-WITH-NOTES.** Nothing blocks. The code follows `graph-proto-A`, `graph-proto-B` and the frozen seams with no silent divergence. The removals are complete. S-R2-2 holds.

Findings: 0 BLOCKER · 0 MAJOR · 0 HIGH · 0 MEDIUM · 3 LOW · 3 MINOR. Of these, 4 are `impl` and 2 are `design-gap`.

## Scope reviewed

- `git diff 8506cb7 f55bb4b -- taskboard/ README.md`, read in full:
  - `taskboard/app.py`: imports at :23 and :52-62; `PresentScreen` docstring; `_deck_lane` at :623-634; `action_export` at :636-664; `action_open_export` at :666-673; `_on_report_chosen` and `_write_report` at :3036-3069; `_open_report` at :3071-3085.
  - `taskboard/keymap.py`: the `H` row at :150-153 and the `PRESENT_KEYS` `x`/`o` rows at :245-246.
  - `taskboard/views.py`: the removed `os`/`shutil`/`subprocess` imports; `present_deck_boards` at :7337-7366; `present_name` at :7369-7378; `_all_timeline` at :7546-7557; the removal of `present_all_export`.
  - `README.md`: rows 140-141 and 189, and the section at 291-298 and 412.
- The callers and helpers I read to check behaviour: `render_present` (views.py:7278-7284), `present_tasks_m`/`present_tasks`/`_present_pool`/`gantt_tasks`, `_all_plan` (:7402), `models.present_order` (:2476), `Board.project_by_id`/`task_by_id` (models.py:1185, no cache), `report_html.extract` (:96-160), `app.board_lanes` (:878), `TaskboardApp.action_open_url` (:4700) and `action_report_export`.
- The tests: `tests/test_present_html_export.py` (all of it), the index and helpers of `tests/test_present_html_at.py`, and the diffs of `test_legend.py`, `test_present_note_highlights.py`, `test_present_views_app.py`, `test_tick_label.py` and `test_markup_census.py`.
- Docs: the diffs of `docs/ARCHITECTURE.md` and `.dev-flow/BACKLOG.md`.

## Checks (evidence state per `/dev-flow` §Evidence states)

| Check | State | Evidence |
|---|---|---|
| Graph conformance: `action_export` steps (1)-(7) | executed | app.py:636-664 matches proto-A step by step. `self._view < 2` is the same predicate as `not _all()` (e4-deviations). `today = date.today()` at the press (P-A-5). |
| Graph conformance: `present_deck_boards` | executed | views.py:7337-7366 does `copy.copy(board)`. It assigns new `projects` and `tasks` lists, takes the held tasks from `present_tasks_m(board, p.id)[1]` in board order, and does no `save` and no caching. |
| Graph conformance: `present_name` | executed | It does a function-local `from .report_html import slug`. `None` gives `present-<date>.html`, and an empty slug gives `project` (P-B-2, F-11). |
| Graph conformance: `_deck_lane`, `_write_report`, `_on_report_chosen`, `_open_report`, keymap rows | executed | All match proto-A. `_write_report` stores no offer, and both callers set or clear `_report_offer` (F-12). `_open_report` catches `(OSError, ValueError)` (S-6). |
| Removals complete, no dead imports | executed | `pyflakes` on `app.py`, `views.py` and `keymap.py` compared with base: the only new warning is F1. TC-4743's pattern has 0 hits in `taskboard/*.py`. `Console`, `Path` and `Text` are still used in views.py. |
| Scope: hide flags (task, project, milestone class), archived, projectless | executed | `present_tasks_m` → `visible_tasks(False)` + `show_in_present` + `_hidden_class_ids`. View 3 = `present_order` ∩ `show_in_present`, the same population as `_all_plan`. No inbox reaches `extract` (each held task's project is in `proxy.projects`). |
| Order: view 3 | executed | `extract` iterates `board.projects`, which is `present_order`, so the slides follow the presentation. TC-4706 pins the slides and the overview. |
| Missing-project fallback | executed (probe) | The project resolves as `render_present` does (`visible_projects(False)[0]`). The tasks diverge from the frame: see F3. |
| File name, offer, `o` | executed | Views 1/2 give `present-<slug>-<date>.html` and view 3 gives `present-<date>.html`. The offer is `(path, clock+10)`, single-use, with a strict `<` expiry, and is shared with the app-level `o` (TC-4733/4733b). |
| S-R2-2: URLs rebound on copies, source never mutated | executed (probe) | views.py:7361-7364 has `t2 = copy.copy(t); t2.urls = []`. A probe in this worktree (`taskboard.__file__` is the worktree's) gave: source urls `['https://e.test/u']`, proxy `[]`, `proxy_task is src_task` False, `proxy.projects is board.projects` False, `proxy.tasks is board.tasks` False. TC-4727 is the negative control: it turns RED for `t.urls.clear()`, `t.urls[:] = []` or a rebind on the source task. |
| Tests encode WHY, none vacuous | executed | See *Tests* below. |
| Mutant table (E5) | not-run | Outside this lane (`qa-reviewer` / orchestrator). By reading only: TC-4710 kills a `proxy.save()` mutant in views 1/2, because the proxy drops `pB`/`b1`, so `board.json` changes. |
| Full suite | n/a — batch end per E5 | GREEN-2 evidence: 527 passed (`evidence/green-2.txt`). I did not re-run it. |

## Findings

### F1 — dead local `w` in `action_export` [LOW] [impl]
- **What:** `w = self.size.width or 0` is still assigned, but nothing reads it any more. The SVG/PNG branch was its only reader. It is the one new `pyflakes` warning against base.
- **Where:** `taskboard/app.py:637`.
- **Why it matters:** It is dead state left by the removal. A reader may think the export depends on the width (it does not; only `_narrow()` does).
- **Suggested fix:** Delete the line.
- **State:** executed (pyflakes `local variable 'w' is assigned to but never used`).

### F2 — stale and false comments left by the removal [LOW] [impl]
- **What:** Some comments and docstrings still describe the removed frame export, and one was rewritten to say something false.
  - `views.py:7548`, `_all_timeline` docstring. Proto-B says the `anchor` "docstring go[es]". The implementer replaced it with "The export draws no cursor but folds as the screen does". No export calls `_all_timeline` any more, so this sentence is false.
  - `app.py:293-294`, `_frame_text` docstring: "what is painted and what `x` exports (view 3 exports its timeline, `action_export`)".
  - `views.py:6651` (`present_tasks_m`: "the presentation's three views and their exports"), `views.py:6665` (`legend_strip_project`: "carried by their exports") and `views.py:7220` ("with the frame's export").
  - `docs/ARCHITECTURE.md:114`: `render_present`'s consumers still say "(paint, export, the scroll clamp)".
- **Why it matters:** These are the same class of stale text F-13 and P-B-4 set out to remove, in the files this increment edited. A reader is told the frame is still exported.
- **Suggested fix:** Delete the `_all_timeline` docstring sentence (or say "The cursor's project anchors the layout"). Cut "and what `x` exports (…)" from `_frame_text`. Drop "and their exports" / "carried by their exports" / "with the frame's export". In ARCHITECTURE.md:114 read "(paint, the scroll clamp)".
- **Note:** `PresentAll.timeline` and `timeline_w` (views.py:7395-7396) are now read only by tests. Proto-B keeps them on purpose ("the field stays: tests read it"). This is not a finding, only recorded.
- **State:** executed (grep).

### F3 — missing-project fallback: the deck holds tasks the frame does not draw [LOW] [design-gap]
- **What:** For a presented id that no longer resolves, `render_present` takes the first visible project for the header (`proj = projects[0]`). It still calls `present_tasks_m(board, project_id)` with the UNRESOLVED id, so the frame draws Alpha's header with none of its tasks. `present_deck_boards` resolves the same project, as ruling 18 asks, but reads `present_tasks_m(board, p.id)`, so the deck holds Alpha's shown tasks.
- **Where:** `taskboard/views.py:7278-7284` (frame, pre-existing) against `views.py:7353-7364` (deck, as designed).
- **Evidence (probe):** `render_present(b, "missing", …)` has "Alpha" True and "ALPHA-ONE" False. `present_deck_boards(lane, "missing")` holds `['ALPHA-ONE']`.
- **Why it matters:** Ruling 2 makes "the presentation the oracle", and ruling 18 aligned only the project resolution. There is no leak: the extra tasks are not hidden by any flag, so ruling 13 is met, and the deck is arguably the correct one. The case is rare: it needs a stale `focused_project_id` or a task with a dangling `project_id`. TC-4715 pins only the slide name, so it cannot see this.
- **Suggested fix:** Send it to BACKLOG. Either `render_present` passes `proj.id` to `present_tasks_m` (a one-token change to the frame, outside this slice), or the canon records that the deck follows the resolved project.
- **State:** executed (probe).

### F4 — redundant branches in `action_export` [MINOR] [design-gap]
- **What:** `project_name = self._project_name if self._board.project_by_id(pid) is not None else project.name`. `project` is the same `Project` object the board holds, because the proxy shares Project objects. So `project.name` is always the right name, and the conditional exists only to keep `_project_name` in use (F-13). Beside it, `self._view < 2` and `self._all()` test the same thing in two forms, and the key rule `'#0'` repeats `extract`'s `bkey` rule a third time (after `H` at app.py:3028).
- **Where:** `taskboard/app.py:643-649`.
- **Why it matters:** It costs only readability. Proto-A step (4) prescribes this text verbatim, so it is not an `impl` divergence.
- **Suggested fix:** None for this increment. At the canon fold, consider `project_name = project.name` and `if not self._all():`.
- **State:** n/a — readability only.

### F5 — RED-phase residue in the new tests [MINOR] [impl]
- **What:** The autouse fixture still patches the removed `views._find_msedge` (`raising=False`, a no-op now). Its comment says "while these design tests diagnose the missing HTML behavior". TC-4742 patches it again. `test_present_html_at.py:43` has `_never_launch_edge`.
- **Where:** `tests/test_present_html_export.py:46-48` and `:650`; `tests/test_present_html_at.py:42-45`.
- **Why it matters:** These are harmless no-ops, but the comment describes a state that no longer exists. TC-4742 still has a reason to exist: it is a regression guard on `subprocess.run`/`Popen`, and it can fail if a process start returns.
- **Suggested fix:** Drop the `_find_msedge` patches and the comment, or reword the comment as "guard: the deleted Edge arm must not return".
- **State:** executed (read).

### F6 — TC-4734's oracle is bound only inside `except` [MINOR] [impl]
- **What:** `expected` is assigned only when `folder.mkdir(...)` raises. On a platform where it does not, the test fails with `NameError`, not with a readable assertion.
- **Where:** `tests/test_present_html_export.py:547-551`.
- **Why it matters:** The test still fails, which is correct. Only the diagnosis is poor.
- **Suggested fix:** Use `with pytest.raises(OSError) as exc: folder.mkdir(...)`, then `expected = f"Report not (fully) written: {exc.value}"`.
- **State:** executed (read).

## Tests (intent, vacuity)

- **Byte identity (TC-4703/4704)** follows A-R2-2. `H` runs on a separate fixture built with `urls=[]`, and `x` runs on the fixture with URLs. Nothing is compared with itself. The board order differs from the gantt order (a1, a2, a3 against a1, a3, a2), so a deck in the wrong order turns it RED.
- **Scope negatives** discriminate:
  - TC-4721 (a hidden task, title and id), TC-4722 (a hidden project in view 3), TC-4723 (archived, archived project, projectless, "Inbox"), TC-4724 (a hidden class) and TC-4725 (a class used only by a hidden task).
  - TC-4726 reads the hide flags at each press.
  - TC-4705 shows the project's own flag is ignored in view 1, and TC-4707 shows only the presented board reaches the deck.
- **S-R2-2 (TC-4727)** checks three things: the URL is absent from the file in all 3 views, the live board's `urls` are unchanged, and the next `save()` writes the original URL. It kills every in-place mutation of the source.
- **The offer (TC-4732/4733/4733b/4735)** covers no offer, expiry at exactly +10 s, single use, survival across `esc` (and the main `o` opens the report, not the task URL), and a failed write withdrawing an earlier offer.
- **The file-set oracle (TC-4741)** hashes the whole board folder: exactly one changed path, the deck, and no `.svg` or `.png`.
- **The key bar (TC-4751..4755)** compares with a monkeypatched base seat, so these tests measure the change instead of restating constants.
- **The legacy deletions** (`AT-2903` SVG escaping, `TC-1809` SVG names, and the SVG arms of TC-2607/2608, AT-2605, AT-1803 and TC-1701) remove only assertions about removed artefacts. Their frame halves stay. The escaping that AT-2903 guarded for the old export is covered for the deck by `report_deck`'s own tests (the renderer is unchanged, S-7). I hand that judgment to `security-reviewer`.
- None of the reviewed tests is vacuous. TC-4742 and TC-4743 are regression guards, not present-behaviour tests, and both can fail.

## Hand-offs

- `security-reviewer`: deck escaping now rests on `report_deck`'s tests alone, since AT-2903 is deleted. F3 is not a leak by my reading; confirm.
- `qa-reviewer`: the E5 mutant table, including addendum 3's `board.save()`-in-export mutant and an S-R2-2 `t.urls.clear()` mutant against TC-4727, has not been run (`not-run`).

## Evidence checklist

- [x] The diff was read in full: app.py :23, :52-62, :215-227, :623-673, :3036-3085; keymap.py :142-153, :245-246; views.py :16-24, :7337-7378, :7395, :7546-7557, and the removed blocks; README 137-141, 186-189, 288-298, 412.
- [x] Correctness pass: scope, hide flags, order, view 3, fallback (F3), name, offer, `o`, `ValueError` path, OSError path.
- [x] Simplicity pass: one shared `_write_report`, no new abstraction beyond the graph. F4 is noted.
- [x] Reuse: `report_html.slug`, `_report_offer`, `_open_report`, `present_tasks_m`, `present_order` and `report_deck.render` are reused. No new slug rule and no new HTML sink (S-7).
- [x] Tests reviewed for intent, see above. F5 and F6 are noted.
- [x] The verdict is explicit, PASS-WITH-NOTES, and no HIGH finding exists.

## §4b `Independent review` cell

`code-reviewer` · PASS-WITH-NOTES (0 BLOCKER/MAJOR/HIGH/MEDIUM; 3 LOW, 3 MINOR) · no HIGH to resolve. F1 and F2 are open LOW `impl` items: a dead local and stale comments, fixable in the corrective pass or sent to BACKLOG. F3 is a LOW `design-gap`: the frame and the deck disagree for a missing presented id, so it goes to BACKLOG. F4, F5 and F6 are MINOR and go to BACKLOG.
