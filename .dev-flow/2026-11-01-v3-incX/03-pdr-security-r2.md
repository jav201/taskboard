# Inc X — E3 PDR round 2, security re-review (code-free)

Reviewer: `security-reviewer` (Opus). Worktree `taskboard-wt/x-html` at `279356e`. Read-only: no product
file, requirement or graph was changed. Per the skill, this round checks only what round 1 left owed
(S-1 ruling, S-2/S-4/S-5/S-6 records) plus any new defect the corrections introduced.

## Scope reviewed

- `03-pdr-security.md` (round 1), `00-e1-rulings.md` rulings 13, 14, 21 and 22.
- `git show 279356e`: `01-requirements.md`, `01-requirements-ledger.md` (LED-.4 to .11), `e3-addenda.md`,
  `graph-interfaces.cw.md`, `graph-proto-A.cw.md`, `graph-proto-B.cw.md`, `e2-seams.md`, `e2-trace.txt`.
- Source re-read for the leak question: `report_html.extract` 98–174 (every per-task key it emits),
  `report_html.notes_html` 42–57, `report_html.write_reports` / `report_name` 180–222,
  `report_deck._meta` 135–148 and `_notes` 338–352 (every `t[...]` key the deck reads),
  `models.Task` 878–915, `views.valid_url` 273–281, `views.present_note_lines` 6783 ff., `app._open_report` 3038–3051.

## Round-1 items: status

| Item | Ruling | Where it now lives | Status |
|---|---|---|---|
| S-1 task links | 14 | `graph-interfaces` node `present_deck_boards` (shallow task copies, `urls = []`, source never changed); proto-B node and `[Data: Task.urls]`; seam S-1; LLR-4502.7 (Unwanted, 3/3, NC "leave a task URL present in the file: RED"); LLR-4501.3/.4 reworded to "same proxy board with every held task's `urls` cleared"; proto-A TC-4727 "`H`'s deck of the original board keeps it"; LED-.5 | **CLOSED** (design `approved`; tests `planned`) |
| S-1 residual meta | 14 | `e3-addenda.md` known limits: priority and `<n>d in phase` stay | Recorded |
| S-2 proxy shares `path` | 22 | addendum 3: never stored or cached; TC-4710 6/6 and its `board.save()` mutant in the mutant table | Recorded |
| S-4 file name | 22 | addendum 4: `..\..\evil` → `present-evil-<date>.html`, `CON` → `present-con-<date>.html`, parent == resolved `F`; overwrite/collision in known limits | Recorded |
| S-5 symlink/junction | 22 | known limits (BACKLOG) | Recorded |
| S-6(1) `as_uri()` | 22 | proto-A node `_open_report` catches `(OSError, ValueError)`; slice unit 6; LED-.11; addendum 5; TC-4736 (relative path, exact toast, 0 exceptions) | Recorded |
| S-6(2) stale toast | 21/F-12 | the shared `_report_offer` makes the toast true after `esc` | Superseded (verified below) |

Note on ids: the URL requirement with the negative control is **LLR-4502.7**. LLR-4501.15 is the
missing-project fallback (ruling 18); it also carries an NC (`None` in the proxy or the kept missing id → RED).

## Findings

### R2-1 — Done tasks (and folded projects' tasks) reach the bytes in full; the presentation only counts them  [Severity: LOW]
- **What:** ruling 13 rewrote "shown task" as "the tasks the presentation does not hide; its views draw
  the open ones as rows and count the done ones". The proxy holds `present_tasks_m(board, pid)[1]`, done
  tasks included. For each, `extract` emits `title`, `notes_html`, `phase`, `priority`, `age`, `due_word`,
  `blocked`, `mark`, and the deck prints them (`_meta`, `_notes`). The same holds for a project folded on the
  timeline. So a done task's title and full notes are in the client file although the presentation never
  draws them, only a count.
- **Where:** `graph-interfaces.cw.md` node `present_deck_boards`; `01-requirements.md` §2 Definitions
  row "shown task"; `report_deck._notes` 338–352.
- **Why it matters:** this is the same class as S-1's accepted residual (data the screen does not show
  leaves in the file). It is not a hide breach: the user did not hide these tasks, `H` writes the same
  bytes, and byte identity (ruling 8) requires it. Notes are free text and are where a passcode or a
  pasted link is most likely to sit, so the residual is wider than "priority and age".
- **Recommendation:** no design change. Widen the S-1 known-limit line in `e3-addenda.md` (and the
  BACKLOG entry E4 writes) to: "done tasks and tasks of folded projects, with their titles and notes, and
  per-task meta other than URLs, are in the `x` deck". Use the same words in the README sentence of
  LLR-4506.5's lines, so the user knows `space` is the only way to keep a task out of the file.
- **Blocks:** no.
- **Evidence state:** `planned` (text edit in E4).

### R2-2 — "cleared" must mean rebind, never `list.clear()`: one mutant is missing  [Severity: LOW]
- **What:** `graph-interfaces` says each shallow copy gets `urls = []` (rebind; correct). proto-B and
  seam S-1 say the copy's `urls` "is cleared". `copy.copy(task)` shares the `urls` list with the source
  task, so an implementation that calls `t.urls.clear()` empties the source task's list.
- **Where:** `graph-proto-B.cw.md` node `present_deck_boards` ("its copy's `urls` is cleared");
  `e2-seams.md` S-1 ("with `urls` cleared").
- **Why it matters:** the hide toggles in `R` (`space`, `a`, `u`, `K`, `J`) save the board at once (seam
  S-8). After an `x` with `.clear()`, the next toggle writes `board.json` with the URLs of every exported
  task erased. That loss is silent and irreversible. TC-4710's sha256 control would not see it, because
  the export itself does not save.
- **Control that already exists:** TC-4727 asserts "source a1 urls unchanged" (graph-interfaces and
  proto-B examples). That assertion catches the defect, but it is not in LLR-4502.7's threshold and is
  not listed as a mutant.
- **Recommendation (E4 addendum):** (a) the implementation rebinds (`copy.urls = []`, or
  `dataclasses.replace(t, urls=[])`); (b) the mutant table gets `t.urls.clear()` in
  `present_deck_boards`, which must turn TC-4727's source-unchanged assertion RED; (c) optionally,
  TC-4727 also runs one `space` after `x` and checks that `board.json` still holds the URL.
- **Blocks:** no. The frozen interface states the correct rebind, and an example would catch the defect.
- **Evidence state:** `planned`.

### R2-3 — LLR-4502.7's wording covers URL text in notes, which the design keeps  [Severity: INFO]
- **What:** the statement reads "with no task URL in its bytes". `notes_html` renders note text as escaped
  text, so a URL a user typed into notes is in the bytes. The presentation draws the same notes, so this is
  correct behaviour. The fixture passes because a1's notes are "ask @ana.ruiz".
- **Recommendation:** at the batch-end canon fold, reword to "with no entry of a task's `urls` (no link
  and no text from that field)". No change to the threshold or the NC.
- **Evidence state:** `n/a — wording only`.

### R2-4 — The shared offer opens only a file the app just wrote  [Severity: INFO]
- **What (F-12):** `_report_offer` is set only from the path that `write()` returned. For `x` that is
  `folder / present_name(...)`. For `H` it is the first path of `write_reports`, whose names come only from
  `report_name` (`workspace-`/`deck-`, slug, ISO date, `.html`). A failed write by either caller sets
  `None`. `action_open_export` reads the slot, clears it, checks the clock and calls `_open_report`. It has
  no URL fallback and no other path source. A file name that is all `.html` and fixed words cannot resolve
  to an executable association through `os.startfile`.
- **Residual:** `H` on the main screen, then `R` and `o` within 10 s, opens `H`'s file. That file was
  also just written by the app, and its toast was on screen. This is accepted.
- **What F-11 adds:** `present_name(None, today)` → `present-<ISO date>.html`. The name has only fixed
  characters, digits and `-`. It cannot equal `present-<slug>-<date>.html`, because an empty slug becomes
  `project`. It has no separator and no device-name stem. Views 1/2 on a board with no project fall
  through to `project_name = None` and write the same view-3 name, which holds an empty project list.
  That is harmless. The S-4 traversal test (addendum 4) still covers the slug path.
- **Evidence state:** `executed` (design and code read).

### R2-5 — Leak sweep: no other per-task field reaches the bytes  [Severity: INFO]
- **What:** these `Task` fields never reach `extract`'s output: `images`, `extra`, `pinned`, `created`,
  `show_in_present`, `phase_changed` (only as `age`) and `depends_on` (only ids in `in_scope`). The deck
  reads 19 task keys, and `urls` is the only one that becomes a link (`_notes`, `safe_href`). With
  `urls = []` on the copy, `_notes` emits no `<a class="url">`. The remaining keys are covered by R2-1 and
  by round 1's S-1 residual. No new sink was added: `render` is unchanged and `x` writes through
  `report_deck.render` only (addendum 9).
- **Evidence state:** `executed` (code read).

## Verdict

- [x] **PASS-WITH-NOTES**
  - **Counts:** HIGH 0, MEDIUM 0, LOW 2 (R2-1, R2-2), INFO 3 (R2-3, R2-4, R2-5).
  - **Blocking findings:** none. S-1 is closed by ruling 14 in the design. S-2, S-4, S-5 and S-6 are
    recorded as ruled.
  - **To E4:** the R2-1 text widening and the R2-2 rebind plus `.clear()` mutant.
- This review clears a design risk. It authorises no merge, push or deploy. The mitigations are
  `planned` until E4's tests run.

## Evidence checklist

- [x] Each finding has what · where · why · recommendation: R2-1..R2-5.
- [x] Each finding has a severity rating: the R2-1..R2-5 headers.
- [x] No secret values in this output. The only URL quoted is the synthetic fixture `example.test`.
- [x] The verdict is explicit (PASS-WITH-NOTES). No HIGH was found.
- [x] New tool or integration: none. The OS opener's scope is unchanged and limited to the just-written path (R2-4).
