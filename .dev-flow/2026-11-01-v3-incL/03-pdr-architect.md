# Inc L — PDR round 1 — architect

**Verdict: FAIL** — 1 HIGH (ARCH-1), 2 MEDIUM, 6 MINOR. No MAJOR.

The verdict is FAIL because of ARCH-1 alone. It is a test-design defect: a requirement's declared negative control cannot fire. It is not a defect of the design's structure. The structure (the seams, the creation-path census, the key routing and byte stability) holds against the real callers. ARCH-1 needs one targeted edit to the TC-4364/TC-4365 examples and to the NC text of LLR-4304.4. The other findings can go to E4 as addenda once they are ruled.

## Problem, restated

Inc L adds an optional `Task.created` stamp at every path that persists a new task, and writes it only when it is set. It infers an added moment for old tasks without rewriting them. It also adds a read-only global screen on `N` (AllBoardsAgenda pattern) that lists every task of every board in added order. Each row carries a phase-box column, there is an archived toggle, and a detail pane shows the cursor's task.

## Constraints

- **Source budget:** 4 source files (models, app, views, keymap) — `executed`: the slice table in 01-requirements.md §6 is 10 units in 4 files.
- **No new dependency; history format unchanged** — `executed`: interfaces and groups D, V and S add none.
- **Byte stability of untouched boards** — `executed` by group D on a scratch copy (TC-4315: 1126, 741 and 761 bytes; sha256 fa38dbd0…).
- **Latency of one paint** — `executed` by group V: N = 2 000 rows gives 2 ms, N = 20 000 gives 12 ms.
- **Privacy** — `n/a — security reviewer's lens`. P-D-6 (team push carries `created`) is ruled and left to the security reviewer.
- **Cost ($, tokens)** — `n/a — local TUI, no service`.

## What I checked and found sound (evidence for "no change needed" on these seams)

- **Creation-path census.** `grep "Task(" / tasks.append|insert|extend` over taskboard/ finds exactly these sites:
  - app.py:2018 (template insert), app.py:2565 and app.py:3401 (both go through `Board.add_task`, models.py:1265);
  - models.py:775 (rescue), models.py:1400–1431 (seed), boards.py:813 (move, deepcopy), app.py:2846 (undo filter), views.py:7497 (transient).

  The design stamps the template insert, the seed branch and `add_task`, and leaves move, undo, rescue and edit alone. The census matches baseline-notes.md. Nothing else in taskboard/ or tests/ reads `"created"` today (grep: 0 hits).
- **Seam signatures.** Every call S makes into V matches the interface exactly in name, arity and order:
  - `added_rows(lanes)`, `first_created(rows)` and `added_order(rows, newest, show_archived)`;
  - `render_added_list(rows, sel, newest, show_archived, hidden, unread, first, today, people, width, height)` (graph-proto-S.cw.md:77 against graph-interfaces.cw.md:206–213).

  V's helpers exist at the signatures it cites: `notes_text(text, people)` views.py:3646, `milestone_mark(task, board, today) -> 3-tuple` :2593, `project_color(board, task)` :255, `board_hex(colour)` :696, `mention_names(task, people)` :3619, `fit` :98, `clip` :906. Also `history.append(..., at=)` (history.py:24) already takes the `now` that P-D-4 needs.
- **`hidden` / `unread` / `first` / `today`.** Each is computed in one place (S's `_paint`/`compose`) and only consumed by V. `first` comes from the unfiltered rows, `today` is frozen at compose as in AllBoardsAgenda (app.py:913), and `unread` counts the None lanes `board_lanes` already produces (app.py:843–869).
- **Key routing (Textual 8.2.8).** The App's priority keys are only `tab` and the arrows/hjkl (keymap.py:128, :168–171), so the screen's priority `escape,N`/`o`/`v`/`enter` win over the App's non-priority `N`/`open_url`/`toggle_archived`/`details`. This is the same mechanism AllBoardsAgenda uses for `escape,A`/`enter` (app.py:894–899).

  `added_list` must sit in the modal-gate tuple and not only in SEAT_ACTIONS. If it did not, the holding tuple would refuse it, and `N` from an agenda over the list could not return to the list (app.py:1296–1306). So that placement is functional and not speculative.

  On resize: the screen directly beneath the top screen is always in `App._background_screens`, so a list under the agenda still gets `Resize` (textual/app.py `_background_screens`, `_check_resize`).
- **The list never writes.** `board_lanes` only peeks and sets `board.marks` in memory. `added_rows` only calls `history.read`. There is no `save` on any S node.
- **Byte stability.** The `_to_dict` drop sits beside the existing `mark`/`present_rank` drops (models.py:1056–1066). A Project has no field, so the guard is inert there. Field placement before `extra` keeps every positional `Task(...)` in seed_data (models.py:1403–1431) valid.
- **Performance.** O(N log N) sorts, called 1–3 times per key (`action_archived` sorts twice and paints once). The pane is built for one row only. `history.read` runs once per board at compose. None of this needs a cache.

## Findings

### ARCH-1 — HIGH — the tie-break negative controls of LLR-4304.4 / LLR-4304.5 cannot fire
- **Anchor:** `added_order` (graph-interfaces.cw.md:178–185; graph-proto-V.cw.md:193–202)
- **Seen:** `added_rows` emits rows "in lane order then file position" (graph-interfaces.cw.md:159), and Python's `sorted` is stable. A mutant that sorts dated rows by `at` alone, and leaves the unknown rows unsorted, therefore gives exactly the correct order for any input that `added_rows` produces. Swapping the registry swaps the input order too, so "RED in 1 of 2 runs with boards swapped" (LLR-4304.4 NC) is false.

  The interface's own TC-4364 input (A, B, C, D, E) is already in (lane, pos) order within each tie. Probe `executed` (pure Python, the interface keys):

  | Input | Correct order | Mutant order |
  |---|---|---|
  | TC-4364 input as given | A B E C D | A B E C D |
  | lane-major (`added_rows` order) | A B E C D | A B E C D |
  | permuted, E D C B A | A B E C D | B A E D C (RED) |

  V's TC-4364/TC-4365 examples build their rows through the F-V lanes, which is lane-major again.
- **Why it matters:** two LLRs (board order, then file position, for ties and for unknown rows) stay unverified while their tests are GREEN. P-S-1 (round 0, MAJOR) was the same class: a threshold that passes under its own NC.
- **Proposal:**
  1. TC-4364 and TC-4365 call `added_order` with a hand-permuted input: equal-moment rows in reverse (lane, pos), and unknown rows reversed. For example, give the interface's five rows as E, D, C, B, A, with the same expected output A, B, E, C, D.
  2. Rewrite LLR-4304.4's NC as "sort by moment only, with the input given in reverse (lane, pos) order: RED", and add the same arm to LLR-4304.5.
  3. Keep the explicit keys in the code. They make the order independent of the `added_rows` contract, which costs one tuple.

### ARCH-2 — MEDIUM — HLR-4302's "back-fill on save" NC names a test that never saves; TC-4316's fixture has nothing to back-fill
- **Anchor:** `Board.save` TC-4316 (graph-proto-D.cw.md:94); HLR-4302 (01-requirements.md:194–201)
- **Seen:** HLR-4302's NC is "a mutant that back-fills an inferred `created` on save: AT-4305 RED". AT-4305 is `N`, the arrows and `escape`, with hashes taken after the home's `escape` (P-S-4). Nothing is saved inside its window, so a save-time back-fill never runs.

  LLR-4302.5's TC-4316 runs on the plain board only (P-D-1 ruling), and that board has no `history.jsonl`. A mutant that back-fills from birth records therefore writes nothing and survives. Only AT-4302 kills it, by accident of the S fixture: `ta2` has a birth record in Alpha's history (graph-proto-S.cw.md:12, :18).
- **Why it matters:** D3, "old tasks are never rewritten", is the operator's core promise. Its declared control points at a test that cannot catch it, and the LLR-level test cannot either.
- **Proposal:**
  1. Give TC-4316's plain fixture a `history.jsonl` with one birth record for `ta`. The byte oracle is unaffected because history is a separate file. TC-4316 then fails under the back-fill mutant.
  2. Re-point HLR-4302's NC to TC-4316 and AT-4302.

### ARCH-3 — MEDIUM — remove the offset-aware conversion instead of guarding it (LLR-4304.13, LLR-4304.16)
- **Anchor:** `added_moment` (graph-interfaces.cw.md:167–176; graph-proto-V.cw.md:183–191)
- **Seen:**
  - The app never writes an aware value: `stamp` and `history.append` both write local naive time (history.py:33). An aware `created` can only come from a hand edit or another tool.
  - Converting it with `.astimezone()` brings in a Windows-only failure (OSError before 1970, OverflowError at the year bounds). That failure needed a MAJOR finding (P-V-2) and a new LLR (4304.16) to guard.
  - TC-4373's oracle is the code's own formula, "on a UTC−6 machine". On a UTC runner (the GitHub CI default) `astimezone()` is the identity, so the mutant "drop tzinfo without converting" passes TC-4373 there (`planned`, reasoned: not run on a UTC machine).
- **Why it matters:** this is a guard added around a speculative feature, and its test is machine-dependent. The commission says to prefer removing a feature over guarding it.
- **Proposal:**
  1. `added_moment` returns None for any parsed value whose `tzinfo` is not None. The task then falls to history or `?`, which is honest about a value the app did not write.
  2. LLR-4304.13 becomes "If a `created` carries a UTC offset, then the system shall treat it as not valid", with threshold `"2026-10-31T18:20:00+00:00"` giving source `h`/`?`, 0 exceptions, and NC "compare aware with naive: TypeError".
  3. Delete LLR-4304.16 and TC-4373b.

  The parse stays in one `try … except ValueError`.

### ARCH-4 — MINOR — group S's node examples carry no evidence state
- **Anchor:** graph-proto-S.cw.md:5–7 (header)
- **Seen:** D and V state that every example was run on a scratch reference (`executed`). S states only probes S-1 (modal chain) and S-2 (`key_line`). Its roughly 45 node examples are therefore `planned`. These include `N` over BoardsHome (TC-4324 arm 3), compose-once under `_bring` (TC-4323) and the `v`/`o`/`enter` precedence.
- **Why it matters:** the claims rest on the same mechanism as AllBoardsAgenda, so the risk is low. But the record reads as if they were checked.
- **Proposal:** mark S's examples `planned` in the header. The E4 tester's RED-on-base run then counts as their first execution. No design change.

### ARCH-5 — MINOR — the list does not repaint when it is resumed
- **Anchor:** `AddedList.on_mount` / `on_resize` (graph-proto-S.cw.md:48–62)
- **Seen:** `@` or `#` pushed over the list can rename a person or a mark class (`_refresh_directories`, app.py:1418). `N` or `escape` then returns via `_bring` or `pop_screen`, but `#al-body` keeps the Text of the last paint, so the old names show until the next key. AllBoardsAgenda has the same exposure (app.py:919–923), which is pre-existing.
- **Proposal:** add `def on_screen_resume(self) -> None: self._paint()` (one line, state `planned`) and open a backlog note for the agenda. Alternatively, rule it out of scope as conformance with the agenda.

### ARCH-6 — MINOR — LLR-4302.6's subject is the whole system, but timers write while the list is open
- **Anchor:** `AddedList.compose` TC-4317; LLR-4302.6 (01-requirements.md:278–279)
- **Seen:** "While the list view is open, the system shall write no board file and no history.jsonl". In team mode `_team_sync_tick` (app.py:1729, :1738) runs under any screen, calling `team_state.sync(self.board)` and `apply_config_to_board`. `_tick` also renews the presence marker (app.py:1813–1815). The test fixture has no team mode, so TC-4317 passes, but the statement is false in team mode.
- **Proposal:** change the subject to "the list view shall write no board file and no history.jsonl", meaning its own code paths. The threshold and NC are unchanged.

### ARCH-7 — MINOR — `Task.from_dict` can take a str `created` out of `extra` instead of extending `_TASK_KEYS`
- **Anchor:** `Task.from_dict`, `[Data: models._TASK_KEYS]` (graph-proto-D.cw.md:30–42, :137–139)
- **Seen:** the design adds `"created"` to `_TASK_KEYS`, then appends a non-str value back to the END of `extra`. On a hand-edited record such as `{"created": 5, "zz": 1, …}`, that reorders unknown keys relative to base, where both stay in file order.
- **Proposal:** leave `_TASK_KEYS` as it is and write `created = extra.pop("created") if isinstance(extra.get("created"), str) else None`. A non-str value is then exactly base behaviour, with one branch fewer. TC-4313 and TC-4314 hold unchanged.

### ARCH-8 — MINOR — LLR-4304.11/.15 say "no listed task", but `first_created` reads all rows, archived included
- **Anchor:** `first_created` (graph-interfaces.cw.md:187–194); LLR-4304.11, LLR-4304.15
- **Seen:** the Definitions say the first created date covers "all tasks the list read (archived included)", and S passes the unfiltered rows (graph-proto-S.cw.md:39). Suppose the only stamped task is archived and hidden. Then no listed task has a valid created, which by the literal LLR text calls for `BEFORE ANY RECORD`. The design shows `BEFORE OCT 30`.
- **Proposal:** reword both LLRs to "If no task the list read has a valid created". The design is right; only the text contradicts it.

### ARCH-9 — MINOR — the key row drops the agenda's read-only tail
- **Anchor:** `AddedList._paint` (graph-proto-S.cw.md:77)
- **Seen:** AllBoardsAgenda, the named pattern, appends `("·", "read-only: nothing here edits a task")` and drops it first when narrow (app.py:936–938). S writes "no read-only tail" for an equally read-only screen.
- **Proposal:** either adopt the tail, which is dropped before any key so LLR-4303.19 is unaffected, or record the divergence in the rulings. Either outcome is acceptable; it should not be silent.

## Risks (not findings)

- **Future creation paths.** The stamp is enforced at `Board.add_task` plus two explicit sites. A future path that appends to `board.tasks` directly (as the template insert does) will silently not stamp, and no structural guard exists. Mitigation: Inc K must go through `add_task` (LLR-4301.5 seam). The risk is accepted.
- **"Before <first created date>" is an inference.** It does not hold for rescued entries, which get a fresh task with created None at any time, or for tasks added by an older build after the first stamp. The editable install points at the main checkout until merge (baseline-notes.md:5). The `?` keeps it honest, and the wording is the operator's own (commission L-5).
- **Seed stamping.** The seed now writes 16 `created` keys. Byte-comparing tests over seeded boards were grepped (test_home_deferred_start, test_cleanup, test_boards_forms, test_boards_backlog_round, test_link_migration): none compares two seeded files. The full battery at batch end is the backstop (`planned`).

## What would change this review

- A permuted-input arm in TC-4364/TC-4365 closes ARCH-1, and the verdict would then be PASS-WITH-NOTES.
- If the operator wants aware values converted (a real other tool that writes UTC), ARCH-3 reverses: keep the conversion with LLR-4304.16, and pin TC-4373 to a fixed offset by monkeypatching the local zone.

## Evidence checklist

- [x] Constraints stated, each with a state (`executed` / `n/a — reason`) — §Constraints.
- [x] 2+ alternatives where a real decision exists. ARCH-3 compares converting with treating as invalid, and ARCH-7 compares `_TASK_KEYS` with `extra.pop`. Otherwise `n/a — the design is fixed by the AllBoardsAgenda pattern (app.py:887) and the operator's verdict`.
- [x] Constraints that do not apply are marked `n/a` (privacy, cost).
- [x] Each recommendation is tied to a constraint (verifiability for ARCH-1/2/3, simplicity for ARCH-3/7, conformance for ARCH-5/9).
- [x] Risks listed (§Risks; the security lens is left to the security reviewer).
- [x] Latency estimated: group V's measurement, which I re-derived as O(N log N) at 1–3 sorts per key.
- [x] Diagram: `n/a — the flows are the Code-Wire graphs under review`.
- [x] What would change the recommendation — §What would change this review.
- [x] Two-layer requirements: US-4301 → AT-4301..4305 (behavioural) and US-4301 → HLR-4301..4306 → 68 LLR → TC (e2-trace.txt: traced 68/68).
