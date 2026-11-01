**Verdict: FAIL** — HIGH 1 (ARCH-1) · MAJOR 4 (ARCH-2, ARCH-3, ARCH-4, ARCH-5) · MEDIUM 1 (ARCH-6) · MINOR/LOW 3 (ARCH-7, ARCH-8, ARCH-9) · INFO 2 (ARCH-10, ARCH-11)

# Inc K — PDR round 1 — architect

The structure holds. It has three groups and clean one-way seams: G-T is pure, G-S never imports `app`, and G-V reads public names only. The two board-write paths (open board through `app.board`, another board on `move_project`'s pattern) are the right reuse of base code, and the Textual mechanics the design relies on are feasible (probed below).

The verdict is FAIL for four reasons:

- **ARCH-1:** the two-window merge rule, which exists to stop text loss and duplicate tasks, causes both when a dump or an undo meets a changed store.
- **ARCH-2:** a batch dump can file a note under a project other than the one shown.
- **ARCH-3:** the capture view can write the open board before its deferred start, which breaks that start's "first write" rule.
- **ARCH-4 and ARCH-5:** one feature (flagged notes) is heavier than a simpler mirror the design already has, and three declared negative controls cannot fire.

Evidence marks: `executed` = a probe ran (scripts under `%TEMP%/incK-pdr-architect/`, interpreter `anaconda3/python.exe -I`, cwd = the worktree, each prints `taskboard.__file__` = `C:\Users\jjgh8\Github\taskboard-wt\capture-proto\taskboard\__init__.py`); `read` = from the text cited.

## Problem, restated

`n` opens a full-screen pad stored in one global `~/.taskboard/inbox.json`. Lines of four or more `_` split the pad into notes. Each note gets a TF-IDF project suggestion from every board, and `alt+d` turns the cursor's note into a task on the chosen project, whichever board it is on. The task is removed from the pad and can be undone for 7 days. `alt+a` reviews and dumps notes in a batch, and images move from a pad folder into the task's folder. The store is shared by every window of the app, so two windows can write it.

## Constraints

| Constraint | State | Evidence |
|---|---|---|
| Source budget: 4 files (inbox.py, suggest.py, app.py, keymap.py) + README row | `executed` (count) | 01-requirements §6: 22 units in 4 files; F-1/R2 keep the screens in app.py |
| No new dependency | `read` | graph-proto-T head (stdlib only); graph-proto-S seams (stdlib + existing modules) |
| Textual 8.2.8 key routing | `executed` | p3_consume.py (below) |
| Typing latency of the rail | `executed` | p4_cost.py → ARCH-6 |
| Two windows sharing one store (D1) | `executed` | p2_union.py → ARCH-1 |
| Privacy | `read` | plaintext meeting notes in `~/.taskboard/`; a dumped note's text is kept 7 days (K-4) → ARCH-11; the rest is the security reviewer's lens |
| Cost ($, tokens, calls) | `n/a — local TUI, no service, no model call` | — |
| Alternatives | `n/a` for the module split (decided by F-1/R2 and R0-10). Real alternatives are given where a finding proposes a change (ARCH-1, ARCH-3, ARCH-4) | — |

## Findings

### ARCH-1 — HIGH — the union merge loses a restored note and brings back a dumped one
- **Anchor:** graph-proto-S `Inbox.write_pad` (change: `union_pads(base.pad, [e.text for e in base.dumped], pad)`), graph-interfaces `union_pads`; LLR-4407.19; R2 F-8 ("No note text is ever dropped silently").
- **What is wrong:** the union is computed against the FRESH file's `dumped` list, before this write's `record`/`drop` are applied. It also always keeps every fresh-pad note. When the store changed since this window's last sync (another window wrote it), three things happen:
  - **(U) Undo loses the note.** The note restored by the undo is still the text of a fresh `dumped` entry (the one being dropped), so the union removes it from "mine". `undo_dump` has already removed the task from its board. The written pad lacks the note, `dumped` lacks the entry, and G-V replaces its text with `res.pad` (P-S-8), all while it shows "Undone: … the note is back in the pad." The text is gone from the pad, the store and the board.
  - **(D) A dumped note comes back.** The other window's pad still holds the note this window just dumped. The union keeps every fresh-pad note, so the note comes back into this pad while also being in `dumped`. That is the duplicate-task path F-8 was written to close.
  - **(R) A re-typed note is dropped.** A note re-typed with the same text as any entry dumped in the last 7 days (for example "follow up") is excluded from "mine" and dropped silently.
- **Evidence (`executed`):** `p2_union.py` is a line-for-line reference of `union_pads` and `write_pad`'s change as specified.
  - The spec example AT-4408 gives `'a\n____\nc\n____\nd'`, as designed.
  - **UNDO + changed:** written pad `'a\n____\nc\n____\nd'` with `dumped` `[]`. The restored note `b` is lost.
  - **DUMP + changed:** written pad `'a\n____\nb\n____\nc'` with `dumped` `['b']`. Note `b` is back in the pad.
  - **RETYPE + changed:** written pad `'x'`. The re-typed note `follow up` is dropped.
- **Test-design gap:** TC-4599 and AT-4408 test only the case where the OTHER window dumped. TC-4599's threshold ("a window note deleted here but present in the fresh pad comes back") states rule (D) as intended behaviour, which is wrong when the deletion was a dump.
- **Proposed change (preferred):** follow `people.Directory._commit`, the way R0-10 and LLR-4407.4 already word it ("applying each change to the store as the file holds it at that moment").
  - A dump becomes an operation on the fresh state: remove the first fresh-pad note equal to `record.text`, then append `record`.
  - An undo becomes: drop the entry, then append its note to the fresh pad (`with_note`).
  - Only the debounced typing write needs a union. Its exclusion set must be the texts of fresh `dumped` entries this Inbox did NOT hold at its last sync (dumped elsewhere since), never the whole 7-day list.
  - Add TC arms (U), (D) and (R) to TC-4599 and to AT-4408.
- **Alternative:** keep the union, but compute exclusion = (fresh entries unknown to this Inbox) ∪ {record.text} − {drop.text}, and remove `record.text` once from the fresh notes. This is equivalent but harder to state.

### ARCH-2 — MAJOR — the chosen option is an INDEX, and docs are rebuilt between dumps of a batch
- **Anchor:** graph-proto-V `CaptureView.options_for` / `chosen` (`opts[self.choice.get(text, 0) % len(opts)]`), `CaptureView._dump` (`self._rebuild_docs()` after every dump), `ReviewList.action_dump` (`dump_part(part, quiet=True)` per checked row, which calls `chosen()` again); LLR-4404.17, LLR-4406.8, LLR-4403.24.
- **What is wrong:** every successful dump rebuilds the corpus, so the next note's hit list can reorder. Its choice is stored as an index, so the same index then points at another project.
  - **In the batch:** row k is dumped into whatever is at its index after rows 1..k−1 changed the documents, not the option the row showed and the user checked.
  - **In the pad:** the same thing happens after `alt+o` on one note and `alt+d` on another. The rail repaints, but the user's explicit pick has moved.
- **Evidence (`executed`):** `p1b.py` runs G-T's reference over fixture F. The note `Rubric for the pilot` has options before `[('Pilot rollout', 0.2232), ('Eval harness', 0.0885)]`. After three earlier rows (`Rubric review`, `Rubric scoring`, `Rubric pilot check`) are dumped into Eval harness, its options are `[('Eval harness', 0.6238), ('Pilot rollout', 0.1593)]`. The row checked as "→ Pilot rollout" is dumped into Eval harness.
- **Proposed change:**
  - Key the choice by option identity, `(board_path, project_id)` or None, not by index. On a rebuild, fall back to the top choice only when that identity is no longer among the options.
  - In `ReviewList.action_dump`, resolve every checked row's target once, before the loop, and dump to those targets. `dump_note` already refuses a project that is gone.
  - Rebuild the docs once after the batch, not per row. This also helps ARCH-6.
  - Add a TC: a batch whose earlier dumps would reorder a later row's hits still files that row under the option it showed.

### ARCH-3 — MAJOR — `n` reaches the capture view over the home, before the open board's deferred start
- **Anchor:** graph-proto-V `TaskboardApp.check_action` (`capture` in the always-allowed tuple: allowed whenever no ModalScreen is up) and `CaptureView._dump` (open board → `app.board.add_task`, a save); base `app.py:1558-1576` `_open_board`, whose comment reads "FIRST, before any other write: the backup must hold the file as the user left it (LLR-505.3)"; HD-1 (the home defers the board's start); base `open_on_board` (app.py:876-890), which starts a deferred board before acting on it.
- **What is wrong:**
  - **Reachable over the home:** with more than one board, the home is on top at start and the open board is mounted but not started. `A` and `N` are allowed over the home, and `n` from either one opens the capture view (LLR-4401.14 requires it).
  - **Effect:** a dump into the open board then saves its file before `_migrate_links`' backup, the sweep, presence and team start. The backup no longer holds "the file as the user left it", and the presence warning ("already open in another window") never ran for a board this window is writing.
  - **Missed in the design:** none of the graphs mention the home case.
- **Evidence (`read`):** app.py:1398-1401 (the always-allowed branch returns before the holding branch that lists BoardsHome), app.py:1426-1432 (home pushed, board not started), app.py:1563-1567.
- **Proposed change (removal):** refuse `capture` while BoardsHome is on the stack. It is one condition in the always-allowed branch, plus a TC: home on the stack, `N`, `n` → no CaptureView. This matches the home's posture ("the home holds the keys"): the sub-screens allowed over it are read-only, and the capture view writes. On the home itself, `n` already means "new board".
- **Alternative:** start the board first, as `open_on_board` does. That is heavier, because the start can push modals (the milestone offer, the identity picker) under the pad.

### ARCH-4 — MAJOR (scope) — "flagged notes" is a second, heavier mechanism for a failure the design already handles more simply in the mirror case
- **Anchor:** LLR-4407.26, LLR-4407.30, LLR-4407.31, LLR-4407.32, LLR-4407.33, LLR-4407.34; the `flagged` key in LLR-4407.2, LLR-4407.7 and LLR-4407.10; graph-proto-S `Inbox.flag`, `Inbox.flag_for`, `_unsaved_flags`, the special case in `Inbox.refresh` (P-S-7); graph-proto-V `_flag_pending`, the rail `⚑` line, `dump_part` / `action_new` / `ReviewList.action_toggle` refusals.
- **What is wrong:**
  - **Not in the commission:** none of K-1..K-6 asks for it (R2 F-12 added it).
  - **It persists a deliberately inconsistent state:** the next successful write stores the pad WITH the dumped note plus a flag. It then guards that state in four places (the rail, `alt+d`, `alt+n`, the review list) and adds a second untrusted list to validate in the store.
  - **The simpler mirror already exists:** for the undo's failed store write, the design keeps a pending drop (`_pending_drop`) and retries it at the next write.
  - **Two patterns for one failure:** the same failure is handled two different ways (rule 7: surface conflicts, do not average them).
- **Evidence (`read`):** graph-proto-V `CaptureView._dump` (OSError branch → `app.inbox.flag(entry)`) against `CaptureView.action_undo` (OSError branch → `self._pending_drop = entry`).
- **Proposed change (prefer removing over guarding):** delete `flagged`. When the store write fails after the board save:
  - remove the note from the pad as on success;
  - keep the entry as a pending record in the app-level `Inbox` (beside the pending drop, so it survives closing the view), and apply both at the next successful write;
  - show one warning: `<project> · <board> got the task, but inbox.json could not be saved: <error>`.
  
  The protection is equal or better:
  - **Crash:** a crash loses the in-memory state either way.
  - **Next successful write:** that write stores a consistent pad plus the dumped entry, so the dump can be undone; a flag cannot.
  - **Reopen in the same session:** reopening after `esc` twice shows `inbox.pad` minus the pending notes, provided the Inbox exposes the pad with pending records applied.
  
  This retires 6 LLRs, one store key and P-S-7.

### ARCH-5 — MAJOR (test design) — three declared negative controls cannot fire
1. **TC-4403 (LLR-4401.3).**
   - **The declared NC:** "CaptureView left out of check_action's holding tuple so the priority j/k reach cursor: arm 1 RED".
   - **Why it cannot fire:** Textual removes a binding on a printable key from every namespace above the focused TextArea (`Screen._binding_chain` → `check_consume_key(key, key_to_character(key))`, textual screen.py:426-437, text_area.py:803-822). `cursor` is also refused by the existing third clause (`len(screen_stack) > 1`) whatever the holding tuple holds.
   - **Evidence (`executed`):** `p3_consume.py`, a pushed Screen with a focused TextArea under an app priority `j` binding. With `check_action` returning True, the text is `'jk'` and the calls are `['cursor']`: only `down` reached the action and `j` was typed. The NC therefore leaves TC-4403 GREEN.
   - **Proposed change:** use an NC that does fire, such as "the pad not focused at open" (then `q` quits and the letters reach nothing). Add an arm for `↑↓←→`, which are NOT filtered: they must move the pad cursor and leave `app.selected_task_id` unchanged.
2. **TC-4482 (LLR-4403.22).**
   - **Why the time arm cannot fire:** without the cap, the 4 000 013-character note scores in 0.50 s (`executed`, `p5_nc.py`), under the 1.0 s threshold, with the same hits (`Eval harness 0.7077`). The single-letter `z` words are dropped by length.
   - **Proposed change:** make the NC arm the deterministic example graph-proto-T already executed: `"x" × 9 995 + " eval harness"` → only `eval` survives (0.3128). Without the cap the result is `eval harness` (0.7077), so the arm turns RED. Keep the time arm, but not as the control.
3. **TC-4486 (LLR-4403.26).**
   - **Why it cannot fire:** "3 runs over the fixture" in one process share one string-hash seed, so a set-order mutant gives identical lists in all three runs.
   - **Proposed change:** run the scorer in 2 subprocesses with `PYTHONHASHSEED=0` and `1` (and `env -u NO_COLOR`) and compare digests, as graph-proto-T's own probe did (`d694943ce6d21f09`).

### ARCH-6 — MEDIUM — `suggest` recomputes idf, every document vector and its norm on every call, and the corpus is rebuilt per dump
- **Anchor:** graph-proto-T scoring steps 2-4 (`_idf(docs)`, `dv`, `|d|` inside `suggest`); graph-proto-V `_rebuild_docs` after every dump/undo; LLR-4403.21 (one call per distinct note text, so one call per keystroke in the edited note).
- **Evidence (`executed`):** `p4_cost.py`, worst-case synthetic vocabulary.

  | Docs | Stems | Corpus build | suggest per call |
  |---|---|---|---|
  | 15 | 9 536 | 12 ms | 2.3 ms |
  | 100 | 138 758 | 175 ms | 28 ms |
  | 300 | 734 482 | 1 080 ms | 138 ms |

  At 300 documents a 10-row batch spends about 11 s rebuilding (plus re-peeking every board), and typing lags by about 140 ms per key. Real boards have fewer distinct stems, so this is an upper bound.
- **Proposed change:** compute idf, `dv` and `|d|` once per corpus (store them on the Doc or in a corpus object), so a call costs O(|note stems| + docs). Rebuild once after a batch (ARCH-2). Add a latency threshold on a stated large fixture.

### ARCH-7 — MINOR (scope) — LLR-4408.14 / `_new_task_id` guards a case another node already refuses
- **Anchor:** graph-proto-S `_new_task_id` (ID_TRIES 20, `task_by_id` check), `_copy_images` (`dest_dir.mkdir()` exclusive).
- **What is wrong:** an existing `images/<id>/` already makes `_copy_images` raise, and `dump_note` turns that into the "could not be moved — nothing dumped" refusal, so nothing is ever written into a foreign folder. A uuid4-hex[:8] collision is not guarded on any other creation path of the app.
- **Proposed change:** remove LLR-4408.14 and `_new_task_id`; use `models._new_id` as the other paths do. If the operator wants the guard kept, keep it, but as the refusal it already is, not as a retry loop.

### ARCH-8 — MINOR — inbox.py imports `modals` (a Textual UI module) for `visible_text`
- **Anchor:** graph-proto-S seams ("`modals.visible_text`"), `_title_row`; base `modals.py:28-51` (imports Textual widgets, boards, people, keymap, views).
- **What is wrong:** the store layer it mirrors, `people.py`, imports only `boards` and `models` (people.py:27-28). `visible_text` is just `"".join(seg for seg, _ in views.highlight_segments(line))` (modals.py:596-599).
- **Proposed change:** import `highlight_segments` from `views` (or inline the join), so inbox.py stays free of any Textual import.

### ARCH-9 — LOW — TC-4412's `cursor` arm is vacuous
- **Anchor:** LLR-4401.12.
- **What is wrong:** `check_action("cursor")` is False with any pushed screen (the third clause), so this arm cannot fail on the declared NC. The `add_task` and `delete` arms do carry it.
- **Proposed change:** replace `cursor` with a seat action no other clause covers (for example `archive`), or drop the arm.

### ARCH-10 — INFO — the rule depends on `TextArea.get_line` returning a longer Text than the document line
- **Anchor:** graph-proto-V `PadArea.get_line`.
- **What it depends on:** `get_line` is public and documented for stylizing (text_area.py:1315-1328), and `_render_line` is its only caller (text_area.py:1440). The cache key holds the whole selection only under `soft_wrap=True` (text_area.py:1370-1394, `read`), which is why the rule redraws when the cursor leaves the line. This holds on 8.2.8 (the V probe P-V-1, `executed` by G-V).
- **Proposed change:** add an assertion in TC-4436 that `pad.soft_wrap is True`, so a later change to `soft_wrap` or a Textual upgrade fails a test instead of leaving a stale `____`.

### ARCH-11 — INFO (privacy, for the security reviewer and the operator) — a dumped note's text outlives its task
- **What it is:** `dumped[].text` keeps the note verbatim for 7 days (K-4), even after the user deletes the task from its board. This is commission-mandated. It belongs in the operator's final report, not in a design change.

## Checked and sound (coverage)

- **G-T purity and seam.** `corpus` takes `board_lanes(app)[0]` lanes `(name, colour, board|None, state)`, exactly what app.py:847-875 returns. The open board is the live `app.board`, and peeked boards are never saved. suggest.py imports no taskboard module (graph-proto-T head). `read`.
- **Open-board dump through `Board.add_task`.** add_task stamps `created`, appends the birth record with the same `now`, then does a plain `save()` (models.py:1301-1310). This matches R0-8 and how the app saves today (app.py:3507-3515). The orphan birth line on a failed save is recorded (F-2). `read`.
- **Other-board dump.** It follows move_project's lock → stamp check → `save_atomic` order (boards.py:760-781). `peek_board` writes nothing for an existing file and never seeds a missing one (boards.py:614-630). `history.append(path, record, at=now)` matches history.py:24. The stamp re-check before `save_atomic` closes the read-to-save window against lock-respecting writers; plain saves from another window still win (the existing posture, F-2). `read`.
- **The store mirrors `people.Directory._commit`.** It reads fresh under `file_lock`, writes atomically, and copies an unreadable file aside with `keep_aside` (people.py:216-252, boards.py:69-90); the 8 MB cap is checked before `keep_aside` reads the whole file. Apart from ARCH-1, the change-application shape is correct. `read`.
- **check_action wiring.** `capture` joins `SEAT_ACTIONS` through KEYMAP. Adding CaptureView to the holding tuple refuses the seat actions that arrive through non-printable keys and the command palette. The app's priority bindings run first (textual app.py:3978-3987), and a refused action falls through to the screen's own priority bindings (the AddedList precedent). `read` + `executed` (p3).
- **Priority alt+letter bindings.** `key_to_character("alt+o")` is None (textual keys.py:321-325), so the pad never filters them. The priority screen binding fires before `TextArea._on_key` would type the letter that terminals send (P-V-3, executed by G-V). The name field's `tab` priority binding is reached because neither the Input nor the TextArea consumes `"\t"` (text_area.py:818-822; Input consumes printable characters only). `read`.
- **The `n` key.** It is free in KEYMAP. The home, people directory and marks manager keep their screen-local `n`, because a non-priority app binding is checked after the screen's (TC-4415's NC does fire). The label `Capture` is unique (`grep`: no other `Capture` in keymap.py or app.py). P-V-4's extra README assertion is needed and present: the seat test collects backticked keys from the home table too (tests/test_keymap.py:404-431, README.md:327). `read`.
- **The modal inventory.** ReviewList must join `tests/test_modal_keys.py` INVENTORY (line 268, assertion at 332). This is ruled (P-V-5). `read`.
- **Notes parse.** `note_parts`, `note_at`, `without_note`, `with_note` and `note_count` agree with R0-3, R0-4 and F-4 on the interface and S examples I traced by hand. The edge cases (adjacent dividers, a trailing divider, blank lines inside a note) are covered. `read`.
- **Images.** Files are copied into the target before the board save and the pad copies removed only after it. The task folder is created exclusively. Symlinks are not followed on the move paths. `read`.
- **Budget.** The design stays within 4 source files and the README row, and adds no new dependency. `read`.

## What would change this verdict

- **ARCH-1 drops to MEDIUM** if the operator rules that two windows never have the capture view in use at once. D1 ("one global inbox") and AT-4408 say the opposite.
- **ARCH-3 is void** if the orchestrator confirms the capture view should be unreachable over the home anyway.
- **PASS-WITH-NOTES:** ARCH-1..ARCH-5 fixed as proposed, or ruled, with ARCH-4 retired or explicitly kept by the operator.

## Evidence checklist

- [x] Constraints stated, each `executed`, `read` or `n/a — reason` — §Constraints.
- [x] 2+ alternatives where a real decision exists — ARCH-1 (operation-based vs corrected union), ARCH-3 (refuse vs start first), ARCH-4 (pending record vs flag); module split `n/a — decided by F-1/R2, R0-10`.
- [x] Non-applying constraints marked `n/a` — cost, module-split alternatives.
- [x] Recommendation tied to constraints — each finding's proposed change cites the rule it serves (R0-10, R0-11, F-8, HD-1).
- [x] Risks listed — ARCH-1 (data loss), ARCH-2 (wrong project), ARCH-3 (backup invariant), ARCH-6 (latency), ARCH-10 (upgrade), ARCH-11 (privacy).
- [x] Cost/latency estimated — ARCH-6 table (`executed`).
- [x] Diagram — `n/a — the graphs are the diagram; each finding names its nodes`.
- [x] What would change the recommendation — §above.
- [x] Two-layer requirements — US-4401 → AT-4401..AT-4408 and US-4401 → HLR-4401..4409 → 192 LLR → TC (e2-trace.txt: 192/192, 8/8); ARCH-1 and ARCH-2 each add arms, not new chains.
