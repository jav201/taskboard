# Inc K — orchestrator rulings (E2/E3)

## Round 0a — interface seams (before the group prototypes)

| Seam | Ruling | Why |
|---|---|---|
| S-a: an open-board dump saves through `live.add_task` + the app's plain `save()` (no lock, no stamp check) | ACCEPT. Recorded risk: same as every other edit of the open board today (`Board.save` is plain `write_text` app-wide). | Consistent with the app's existing writes of the open board; changing the open-board save path is out of scope. |
| S-b: the in-memory rollback of `live` on a failed dump (LLR-4404.15) | ACCEPT in G-S. `dump_note` already mutates `live` through `add_task`; one owner for the dump's all-or-nothing. | Keep the undo of a mutation beside the mutation. |
| S-c: the review list's choice dict lives in CaptureView (G-V) | ACCEPT. | No group boundary crossed. |

## Round 0b — group prototype findings

| Finding | Ruling |
|---|---|
| P-T-1 | ACCEPT. The note cap lives in suggest.py as `NOTE_CHARS` (10 000). |
| P-T-2 | ACCEPT the prototype: a note word no board holds weighs 0. |
| P-T-3 | AMEND: ties on project name sort by `name.casefold()`, then `name`. |
| P-T-4 | AMEND: G-V passes `suggest` the note's title + "\n" + notes from `inbox.note_task` (image lines already removed); suggest.py stays free of inbox imports. |
| P-T-5 | ACCEPT a cap: each project document is cut at 100 000 characters before tokenising (deterministic). |
| P-S-1 | ACCEPT: `dump_note(..., project_name: str = "")`, used only for the LLR-4404.12 notice. Interface amended. |
| P-S-2 | ACCEPT (MAJOR): undo's changed-check uses `_task_fields(entry.text, moved=set(entry.images))`. Interface amended. |
| P-S-3 | ACCEPT (MAJOR): `STORE_MAX_BYTES = 8 388 608`; over-cap store read = unreadable, not copied aside, never written over; an over-cap write raises the worded OSError and changes nothing. New LLRs in HLR-4407. |
| P-S-4 | ACCEPT (MAJOR, security): entry validation (`task` fullmatches `[A-Za-z0-9_-]{1,64}`, images pass the name rule, text non-blank, `new_project` a bool); undo only when `entry.board` is samefile with a lane of `board_lanes`, else the worded notice and the entry kept. |
| P-S-5 | ACCEPT (MAJOR): `mark_notice` holds pad/stamp only when the file was unchanged before it. |
| P-S-6 | ACCEPT the fresh read: `last_dump` reads the file's `dumped` fresh (no state/stamp change; unparseable → memory). |
| P-S-7 | ACCEPT (MAJOR): `_unsaved_flags` survive refresh until a write succeeds. |
| P-S-8 | ACCEPT: G-V replaces its text whenever `result.written and result.pad != text`; merge notice only when `union`. |
| P-S-9 | ACCEPT: both checks on both paths. |
| P-S-10 | ACCEPT: image-name rule widened (no control chars, no surrounding whitespace, ≤ 128 chars, no Windows device stem); a failing source name saves as `image<suffix>`. |
| P-S-11 | ACCEPT as recorded risk (BACKLOG). |
| P-S-12 | ACCEPT; BACKLOG item (UndoOutcome `left` list). |
| P-S-13 | Same as P-T-1 (suggest.py `NOTE_CHARS`). |
| P-S-14 | ACCEPT. |
| P-S-15 | ACCEPT: public `entry_for(outcome, note, board_path, now)` in inbox.py. Interface amended. |
| P-S-17 | ACCEPT as recorded risk. |
| P-S-19 | ACCEPT: LLR-4407.28 reads "a board saved by this version"; normalisation is existing behaviour. |
| P-S-21 | ACCEPT (no archived check; prefer simpler). |
| P-V-1 | ACCEPT (MAJOR; orchestrator probe confirms `ESC b` → `ctrl+left`; `ESC a/d/i/l/n/o/u` → `alt+<letter>`): the name field's board cycle is `tab`, shown `⇥ board`. LLR-4404.21/22 reworded. |
| P-V-2 | ACCEPT: every CaptureView pad key is a priority binding; a test posts the terminal form `events.Key("alt+d", "d")` and asserts the pad text unchanged. |
| P-V-3 | ACCEPT. |
| P-V-4 | ACCEPT: TC-4413 asserts the README row `| \`n\` | Capture |`. |
| P-V-5 | ACCEPT: the tester adds `"ReviewList": {}` to `tests/test_modal_keys.py` INVENTORY. |
| P-V-6 | ACCEPT the wording. |
| P-V-7 | ACCEPT. |
| P-V-8 | AMEND: names resolved as proposed; the wide-rail flag line is shortened to `⚑ on <board> — delete it here`; the LLR-4407.30 notice keeps the full sentence. |
| P-V-9 | ACCEPT. |
| P-V-10 | ACCEPT. |
| P-V-11 | ACCEPT: AT-4407's note is `Vendor call\n::b:: ask the vendor :: @username_subject`. |
| P-V-12 | AMEND: a successful undo shows `Undone: <title> left <board>; the note is back in the pad.` (new LLR in HLR-4405). A silent success is a missed state. |
| P-V-13 | ACCEPT: G-S words the dump_note / attach refusals; G-V shows `notice` verbatim and owns every other text; G-V reads moved files from `out.task.images`. Interface amended. |
| P-V-14 | ACCEPT. |
| E2c | The correction pass checks that G-V's example hit scores equal G-T's executed examples; G-T's executed values win on a mismatch. |

## Round 0c — correction-pass questions

| Question | Ruling |
|---|---|
| G-S keeps "Fixture S" (same boards, phases, project names as F; own ids/paths) | ACCEPT. |
| P-V-8 string used in narrow rail and review row too | ACCEPT (one string everywhere). |
| P-V-7 → LLR-4401.17, P-V-2 → LLR-4401.18, P-T-2/P-V-10/P-V-9 text | ACCEPT. |
| `tab` priority binding inert with the name field closed | ACCEPT (the pad never moves focus by tab). |

## Round 1 — PDR (architect, security)

### Security (03-pdr-security.md: FAIL, 3 MAJOR, 2 MEDIUM, 6 LOW)

| Finding | Ruling |
|---|---|
| SEC-1 (MAJOR) | ACCEPT: `union_pads` suppresses only the fresh `dumped` entries this window has NOT seen, as a multiset (an entry this window saw does not suppress a re-typed note). |
| SEC-2 (MAJOR) | ACCEPT: a store whose strings will not encode as UTF-8 (lone surrogates) is unreadable at the door; `dump_note` refuses note text that will not encode (backstop, worded notice); `_commit` turns `UnicodeError` into `OSError`. The pre-existing `Board.save` truncate-before-fail → BACKLOG. |
| SEC-3 (MAJOR) | ACCEPT: undo's changed-check compares the whole task record (`dataclasses.asdict`) against the expected record rebuilt from the dump entry; any difference → refused. Undo also refuses when another task's `depends_on` names the task. Worded notices. |
| SEC-4 (MEDIUM) | ACCEPT: a failed read (OSError) at load/refresh keeps the OLD stamp, so the next write takes the union path. |
| SEC-5 (MEDIUM) | ACCEPT: `quit` while the capture view holds an unsaved pad tries the write first; on failure it behaves like `esc` (warning, view stays; a second `quit` exits). |
| SEC-6 (LOW) | ACCEPT: the image move/unlink paths reuse `move_project`'s junction/link check. |
| SEC-7 (LOW) | ACCEPT: the full reserved-name list (CON, PRN, AUX, NUL, COM0-9, LPT0-9, incl. superscript digits) — defence in depth. |
| SEC-8 (LOW) | ACCEPT: lane test by normalised path string first; `samefile` only against lane paths. |
| SEC-9 (LOW) | ACCEPT as recorded risk (BACKLOG). |
| SEC-10 (LOW) | ACCEPT as existing behaviour (BACKLOG). |
| SEC-11 (LOW) | ACCEPT as BACKLOG (perf, measured cheap). |

### Architect (03-pdr-architect.md: FAIL, 1 HIGH, 4 MAJOR, 1 MEDIUM, 3 MINOR/LOW, 2 INFO)

| Finding | Ruling |
|---|---|
| ARCH-1 (HIGH) | ACCEPT the preferred change, merged with SEC-1: dump and undo are operations on the FRESH state under the lock (`people.Directory._commit` shape). Dump: remove the first fresh-pad note equal to the record's text, append the record. Undo: drop the entry, append its note to the fresh pad (`with_note`). Only the debounced typing write uses a union, whose exclusion set is the multiset of fresh `dumped` entries this Inbox had NOT seen at its last sync (SEC-1). TC arms (U), (D), (R) added to TC-4599 and AT-4408. TC-4599's threshold sentence (D) is corrected. |
| ARCH-2 (MAJOR) | ACCEPT: a note's chosen option is stored as a key `(board path, project id)` (or the new-project sentinel), never a list index; the batch fixes every row's target before the loop and rebuilds suggestions once after it. |
| ARCH-3 (MAJOR) | ACCEPT: `capture` is refused (check_action False) while the boards home is on the screen stack — the view is unreachable over the home. |
| ARCH-4 (MAJOR, scope) | ACCEPT — REMOVE flagged notes (the LLRs, the `flagged` store key, `Inbox.flag`, `_unsaved_flags`, the rail flag line, P-V-8/P-V-10 strings). Replacement: when the board save succeeded and the store write failed, the app-level `Inbox` keeps the dump as a pending record (with the note already removed from the in-memory pad); every later write (debounce, close, exit) retries it first; the toast says the store write failed and will be retried. Recorded risk: an exit before any successful retry leaves the note in the on-disk pad (a re-dump makes a second task). Prefer removing over guarding. |
| ARCH-5 (MAJOR, test design) | ACCEPT each control the finding names (TC-4403, TC-4482, TC-4486). |
| ARCH-6 (MEDIUM) | ACCEPT: idf, document vectors and norms are computed once per corpus build (at open and after a dump/new project); a note's hits are cached by note text; scoring runs on the debounce, not per keystroke. |
| ARCH-7 (MINOR) | ACCEPT: remove the redundant `_new_task_id` guard (LLR-4408.14 withdrawn or merged). |
| ARCH-8 (MINOR) | ACCEPT: inbox.py never imports `modals` (or any UI module); `visible_text` comes from a non-UI module (views/models) or a local copy of the marker rule taken from `views.highlight_segments` semantics. |
| ARCH-9 (LOW) | ACCEPT: drop or fix TC-4412's vacuous `cursor` arm. |
| ARCH-10 (INFO) | Noted; the probe in graph-proto-V stands as evidence. |
| ARCH-11 (INFO) | Noted; flagged to the operator in the final report (dumped text outlives its task for 7 days, commission-mandated). |

### Round 1 correction-pass questions

| Question | Ruling |
|---|---|
| A dump/undo store write also carries the window's unsaved typing (typing union applied after the op) | ACCEPT — otherwise unsaved typing is lost when a dump meets a changed file. |
| LLR-4403.30/.31 (no scoring inside the 1 s debounce; the rail keeps the last drawn lines meanwhile) | ACCEPT — they are the visible face of ARCH-6; the E5 captures show them. |

## Round 2 — blocking-only re-review

| Finding | Ruling |
|---|---|
| ARCH-1..ARCH-5 | CLOSED (03-pdr-architect-r2.md, PASS-WITH-NOTES). |
| ARCH-12 (MEDIUM, new) | ACCEPT — WITHDRAW LLR-4403.30 and LLR-4403.31 (prefer removing): with the cached corpus (2.7 ms per call, LLR-4403.29) the rail scores on every change, so the rail never shows an option `alt+d` would not use. E4 addendum A-1. |
| ARCH-13 (MINOR) | ACCEPT as designed: an edited note is a new note, so an `alt+o` pick resets; recorded in addenda A-2 (no change). |
| SEC-1..SEC-5 | CLOSED in the design (03-pdr-security-r2.md, PASS-WITH-NOTES); mitigations re-checked in code at E5. |
| R2-1 (LOW, new) | ACCEPT the fix: `action_quit` (from any screen) retries a held pending store write once before exiting; on failure it exits anyway and the note stays recoverable with `alt+u` (recorded risk). E4 addendum A-3. |

**E3 verdict: PASS-WITH-NOTES** (architect and security, round 2). Addenda A-1..A-3 go to E4.
