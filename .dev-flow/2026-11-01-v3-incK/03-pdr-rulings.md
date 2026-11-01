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
