# Inc X — E5 security review (code)

Reviewer: `security-reviewer` (Opus). Worktree `taskboard-wt/x-html` at `f55bb4b`. Change under review:
`git diff 8506cb7 f55bb4b -- taskboard/` (`app.py`, `keymap.py`, `views.py`). Read-only toward the
product: no source, test, requirement or graph was changed.

**Verdict: PASS-WITH-NOTES.** HIGH 0, MEDIUM 0, LOW 3, INFO 7. Nothing blocks.

## Scope reviewed

- The diff above, plus the code it calls: `report_html.extract` / `slug` / `notes_html`,
  `views.present_tasks_m` / `_present_pool` / `_hidden_class_ids`, `models.present_order`,
  `Board.project_by_id` / `task_by_id` / `visible_projects`, `models.Task` (dataclass, `urls` a plain
  list field), `app._open_report`, every `_report_offer` read and write.
- The bindings: `03-pdr-security.md`, `03-pdr-security-r2.md`, `00-e1-rulings.md` (rulings 12–22),
  `e3-addenda.md` (A-R2-*, S-R2-1, S-R2-2), `e4-deviations.md`, `e4-tests.md` (mutant table),
  `e4-integration.md`. Also the BACKLOG and README additions in `git diff 8506cb7 f55bb4b`.

## Runs

| Run | Result | Evidence |
|---|---|---|
| `env -u NO_COLOR python -m pytest -q tests/test_present_html_export.py tests/test_present_html_at.py` in the worktree. `taskboard.__file__` was checked first and resolves to the worktree, not the main checkout. | 172 passed, 0 failed | this file (the run was not saved to `evidence/`) |
| Direct probe: a board with a hidden task, a hidden project with a task, a milestone of a hidden class, an archived task, a person mentioned only in hidden notes, and a shown task that holds a URL and depends on the hidden task and the hidden milestone. It runs `present_deck_boards` → `extract` → `report_deck.render` for views 1/2 and 3. | 0 occurrences of any hidden title, id, class name, person name or URL. The held task is `main:a1` only. The source `urls` list is the same object and unchanged. The board's lists keep 5 tasks and 2 projects. | temp dir, deleted after the run |
| Mutant `t2.urls = []` → `t2.urls.clear()` (S-R2-2), in a `git archive` copy of the tree, never the worktree. `__file__` was checked first and resolves to the copy. | KILLED 3/3 by TC-4727, at its "source urls unchanged" assertion. TC-4703 and TC-4704 still pass. | temp dir, deleted after the run |
| `present_name` probe: `..\..\evil`, `a/b`, `CON`, NUL plus control characters plus U+202E, `İstanbul`, `Ⅻ²`, 300 × `x`, 40 astral characters, `""`, `...`, `C:`, a lone surrogate | every result is `present-<alnum and ->-<date>.html`. The longest is 64 characters (184 UTF-8 bytes, 104 UTF-16 units). The output has no separator, dot, colon, control character, surrogate or device-name stem. | same temp dir |

## Verification of the seven points

| # | Point | Result on the code | Evidence |
|---|---|---|---|
| 1 | Hidden projects, tasks and milestone classes never reach the bytes | **Holds.** `proxy.projects` is either the presented project or `present_order(board)` filtered by `show_in_present`. `present_order` excludes archived projects. `proxy.tasks` is the union of `present_tasks_m(board, p.id)[1]` over those projects only. `present_tasks_m` drops hidden tasks, archived tasks (through `visible_tasks(False)`) and the milestones of hidden classes. `extract` reads only `board.projects` and `board.tasks`. `deps` is filtered by `in_scope`. `people` and `marks` are emitted only when used. The inbox is empty by construction. | views.py:7337–7365; report_html.py:98–174; probe; TC-4721..4726 |
| 2 | URLs absent; rebound on copies; the source is untouched | **Holds.** `t2 = copy.copy(t); t2.urls = []` rebinds the copy's field. The diff adds no `.clear()` (the only `.clear()` in views.py/app.py is `line_map.clear()` at views.py:6361, which is unrelated). No board list is mutated: `proxy.projects` and `proxy.tasks` are new lists, and `pos` is a local dict. | views.py:7360–7364; probe (same list object); `.clear()` mutant KILLED |
| 3 | File name from the project name | **Safe.** It calls `report_html.slug`, the only slug rule (S-3 closed), and no local copy of it. Only `str.isalnum()` characters and `-` survive. The output is cut to 40 characters, and an empty slug becomes `project`. The `present-` prefix prevents a device-name stem, and the name always ends in `.html`. | views.py:7369–7378; probe; TC-4701b (`..\..\evil`, `CON`, `!!!`, parent == resolved `reports/`) |
| 4 | Writing into `reports/`: overwrites and symlinks | **As ruled.** A same-day file is overwritten, and a planted link is followed. This is the same posture as `H`, and BACKLOG records both (S-4, S-5). `mkdir` / `write_text` raising `OSError` (for example when `reports` is a file) is caught by `_write_report`. One non-`OSError` path escapes: see E5-S3. | app.py:654–664, 3052–3069; BACKLOG known-limits line |
| 5 | `o` opens only the file just written; `ValueError` caught | **Holds.** `_report_offer` is written only at app.py:664 and 3050, from the return value of `_write_report` (the path `write()` returned), or set to `None` on failure. `action_open_export` reads the slot, clears it, checks the monotonic clock and calls `_open_report`. It has no URL fallback. `_open_report` catches `(OSError, ValueError)`. | app.py:664–673, 3071–3084; TC-4732/4733/4733b/4735/4736/4736b |
| 6 | Board text in the deck is escaped | **Holds.** `report_deck.py` and `report_html.py` are unchanged in the diff, and `x` writes only through `report_deck.render` (addendum S-7). Every toast added or changed is `markup=False`, including the folder path and `{e}`. | diff stat (3 files); app.py:640, 3062, 3068, 3084; TC-4737 |
| 7 | Edge subprocess and the `os`/`shutil`/`subprocess` imports gone | **Holds.** views.py has no `import os/shutil/subprocess` and no `os.`/`shutil.`/`subprocess.` use. No `msedge`, `_find_msedge`, `save_present_*`, `present_paths` or `present_all_export` remains in `taskboard/`. The only `subprocess` in the package is the pre-existing clipboard helper (models.py:621, fixed argv, off the `x` path). The test references to the removed names are `raising=False` monkeypatches and TC-4743's guard regex. | grep over `taskboard/*.py`; TC-4742, TC-4743 |

## Findings

### E5-S1 — S-R2-1's documentation widening is only half applied  [Severity: LOW] `impl`
- **What:** addendum S-R2-1 asks for two things: widen the BACKLOG S-1 known-limit line, and say in the README that done and folded tasks' **titles and notes** reach the file. Neither is done in full.
  - The BACKLOG line still reads "priority and `<n>d in phase`".
  - The README says "done tasks and folded projects included". It does not name their notes, and it does not say that `space` is the only way to keep a task out of the file.
- **Where:** `.dev-flow/BACKLOG.md` (the "Inc X — E3 known limits" line); `README.md` (the `x` paragraph).
- **Why it matters:** free-text notes are where a passcode or a pasted link is most likely to sit (R2-1). The user should learn from the docs, not from the client, that done tasks' notes are in the deck.
- **Recommendation:** in the BACKLOG line, replace "(priority and `<n>d in phase`)" with "done tasks and tasks of folded projects, with their titles and notes, and per-task metadata other than URLs (priority, `<n>d in phase`)". In the README, after "done tasks and folded projects included", add "— with their notes; `space` keeps a task out". Docs only: no source budget, no retest beyond TC-4765.
- **Blocks:** no. **Evidence state:** `planned`.

### E5-S2 — The S-R2-2 `.clear()` mutant is missing from the mutant table  [Severity: LOW] `impl`
- **What:** S-R2-2 (marked MUST) requires a negative control: a mutant that empties the source `urls` must turn the test RED. In `e4-tests.md`, row 4502.7 lists only "Leave task URLs in the deck", and `e4-integration.md` does not run that mutant either.
- **Where:** `e4-tests.md` §Mutant table, row 4502.7.
- **Why it matters:** with `.clear()`, the next `space`/`a`/`K`/`J` in `R` would save `board.json` with every exported task's URLs erased. The loss is silent and irreversible. TC-4710's hashes cannot see it.
- **Done in this review:** I ran the mutant in a copy of the tree. It is **KILLED 3/3 by TC-4727** (the `{t.id: t.urls …} == original` assertion). The control works.
- **Recommendation:** add the row `4502.7 (S-R2-2) | t2.urls = [] → t2.urls.clear() | TC-4727 (3 views): KILLED` to the E5 mutant table in `04-validation.md`, and cite this file as its evidence.
- **Blocks:** no. **Evidence state:** `executed` (mutant run); record `planned`.

### E5-S3 — A lone surrogate in board text crashes the export instead of toasting  [Severity: LOW] `design-gap`, pre-existing
- **What:** `_write_report` catches only `OSError`. When a title or note holds a lone surrogate (a `\ud800` escape in `board.json` loads as one), `write_text(..., encoding="utf-8")` raises `UnicodeEncodeError`. That error is a `ValueError`, not an `OSError`. It escapes the action handler and leaves a 0-byte `present-*.html`. I reproduced this on `present_deck_boards` → `extract` → `render` → `write_text`. The board is not touched, because the proxy never saves.
- **Where:** app.py:3052–3069 (`_write_report`); LLR-4503.4 names only `OSError`.
- **Why it matters:** robustness, not confidentiality. The input needs a hand-edited or foreign-written `board.json`. `H` had the same failure before this increment (`write_reports`), and so did the removed SVG writer. The increment neither introduces nor widens it.
- **Recommendation:** BACKLOG item. `_write_report` should catch `(OSError, UnicodeError)` with the same toast, or the writers should use `errors="replace"`. In both cases LLR-4503.4 gains the case. The fix is not owed by Inc X.
- **Blocks:** no. **Evidence state:** `executed` (reproduced); fix `n/a — backlog`.

### Informational (verified, no action)

- **E5-I1** — the hide filter is complete (point 1). This confirms S-0 and R2-5 on the real code.
- **E5-I2** — URLs are rebound, never cleared (point 2). S-R2-2 is honoured, and the mutant is killed.
- **E5-I3** — `present_name` is traversal-, device-name- and length-safe (point 3). S-3 and S-4 are closed; TC-4701b pins them.
- **E5-I4** — the posture of the `reports/` writer matches `H` (point 4). S-4 and S-5 are recorded in BACKLOG.
- **E5-I5** — the shared offer opens only a path the app wrote, and `ValueError` is caught (point 5). S-6(1) is closed. The residual "H's file through `R` → `o`" stays accepted (R2-4).
- **E5-I6** — no new HTML sink, and every changed toast is `markup=False` (point 6).
- **E5-I7** — the Edge rasteriser and its imports are gone, and nothing calls them (point 7). S-8 is closed.
- **Not checked:** the proxy-lifetime rule (S-2). I read `action_export` and found no `self.`/`self.app.` store of `boards` or `proxy`. The proxy-lifetime clause of the `board.save()` mutant (row 4501.10) belongs to the E5 mutant run, and I did not run it.

## Verdict

- [ ] OK to ship
- [ ] BLOCK-UNTIL
- [ ] Block
- **E5 security: PASS-WITH-NOTES.**
  - **Counts:** HIGH 0, MEDIUM 0, LOW 3 (E5-S1 `impl`, E5-S2 `impl`, E5-S3 `design-gap`), INFO 7.
  - **Blocking findings:** none.
  - **Corrective pass (docs and records only, no source):** E5-S1 (BACKLOG and README text) and E5-S2 (the mutant-table row).
  - **To BACKLOG:** E5-S3.
- This review clears the increment's security risk at `f55bb4b`. It authorises no merge, push or deploy.

## Evidence checklist

- [x] Each finding has what · where · why · recommendation: E5-S1..S3, with E5-I1..I7 cross-referenced to the verification table.
- [x] Each finding has a severity and an `impl`/`design-gap` tag: the E5-S1..S3 headers.
- [x] No secret values appear in this output. The only URLs are synthetic fixtures (`example.test`, `secret.example`).
- [x] The verdict is explicit (PASS-WITH-NOTES), and no HIGH is open: none was found.
- [x] New tool or integration: none. One external process (headless Edge) is removed, and its removal is verified (point 7). The scope of the OS opener is unchanged: only the path the app just wrote.
