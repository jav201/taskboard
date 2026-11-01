**Verdict: PASS-WITH-NOTES** — HIGH 0 · MAJOR 0 · MEDIUM 0 · LOW 1 · INFO 2

# Inc K — PDR security re-review, round 2 (blocking findings only)

The corrected requirements and graph close SEC-1, SEC-2 and SEC-3 (MAJOR) and SEC-4 and SEC-5 (MEDIUM). The corrections introduce no new HIGH or MAJOR finding. Each mitigation is still `planned`: it lives in the design, not yet in code. I re-check each one at the increment gate against code and a test that turns RED without it.

## Scope reviewed

- **Rulings:** `03-pdr-rulings.md` §Round 1 and §Round 1 correction-pass questions.
- **Corrections:** `03-e3-corrections.md`.
- **Corrected design** at `88c48f3`:
  - Requirements: §1 (`store stamp`, `unseen entry`, `pending record`, `pad write`), LLR-4404.34, LLR-4405.10/.16/.18/.19, LLR-4407.18/.19/.39–.49, LLR-4408.20, AT-4408 arms D/U/R, and §Recorded risks.
  - graph-proto-S: `_read`, `load`, `_stamped`, `refresh`, `_commit`, `write_pad`, `pad_now`, `last_dump`, `union_pads`, `undo_dump`, `_undo_open`, `_undo_other`, `_links_ok`, `_images_back`, `_drop_pad_copies`, `dump_note`.
  - graph-proto-V: `TaskboardApp.action_quit`, `on_text_area_changed`, `_flush`.
- **Base code:** `app.py:667/837` (`quit_app` on the boards home).
- **Probe:** `%TEMP%/incK-pdr-security/r2.py`, run with `-I`. It printed `taskboard.__file__` = `…\taskboard-wt\capture-proto\taskboard\__init__.py`. Synthetic data, temp folders.

## Round-1 findings

| Id | Sev | State | Evidence |
|---|---|---|---|
| SEC-1 | MAJOR | **closed** (design) | LLR-4407.19 and `union_pads` now exclude only the multiset of *unseen* entries, plus the fresh notes, held in a `Counter` budget. `executed`: the specified union gives TC-4599 arm 1 `a\|c\|d`. The R arm (an entry this window has seen, re-typed `follow up`) gives `x\|follow up`, so the note is kept. With two copies against one unseen dump it gives `x\|follow up`, so one copy is kept. |
| SEC-2 | MAJOR | **closed** (design) | The door probe in `_read` is `json.dumps(raw, ensure_ascii=False).encode("utf-8")` inside the `(ValueError, RecursionError)` try (LLR-4407.43). `executed`: a surrogate in the pad gives None (unreadable), a surrogate in an entry's text gives None, and a clean store reads normally. `dump_note` step 0 refuses before any board write (LLR-4404.34). `_commit` turns `UnicodeError` into `OSError` before `write_atomic` runs, so no temp file is left (LLR-4407.44). `on_unmount` catches `(OSError, ValueError)`. The `Board.save` truncation is RISK-SEC-2 (pre-existing, BACKLOG). |
| SEC-3 | MAJOR | **closed** (design) | `_unchanged` compares `dataclasses.asdict` of the task with the record rebuilt from the entry, on both undo paths (LLR-4405.10). `_needed` refuses when another task's `depends_on` names the task (LLR-4405.19). `executed` on the real `Task`/`Board`: equal for the live task after `add_task`, after `Board.load` (an app restart) and after `peek_board`. The phase move is caught. The refusal direction is safe: any mismatch keeps the task. |
| SEC-4 | MEDIUM | **closed** (design) | LLR-4407.45: `load` leaves `_stamp` None after an `OSError` read, and `refresh` keeps the OLD stamp. In both cases the next write sees "changed" and unions with the file instead of writing over it. `read`. |
| SEC-5 | MEDIUM | **closed** (design) | LLR-4407.46/.47 and `TaskboardApp.action_quit` give `ctrl+q`/`q` the same guard as `esc`: flush first, warn on failure, and exit on the second quit. A key or cursor move disarms it. The boards home's own `quit_app` (`app.py:667`) cannot be reached over a capture view, because ARCH-3 refuses `capture` over the home and the view holds the seat. `read`. |

## The corrections themselves (ARCH-1, ARCH-4, the whole-record check): no new HIGH or MAJOR

- **Fresh-state dump and undo (ARCH-1):** each op is applied to the fresh pad under the lock.
  - A record removes the first fresh note equal to its text, and is skipped when `dumped` already holds its (task, board), so a retry is idempotent.
  - A drop appends the restored note only while the fresh `dumped` holds the entry. When the other window already undid it, its pad carries the note, and the budget keeps one copy.
  - My traced cases lose no note text. A note the other window edited stays, because it does not match. A note deleted by hand comes back (resurrection, not loss). The other window's notes are always kept.
- **Pending record (ARCH-4):**
  - `pending` survives `refresh` and is retried first on every pad write.
  - `pad_now` makes reopening consistent with it.
  - `last_dump` counts pending ops, so `alt+u` reaches a dump whose store write failed.
  - An exit before a retry leaves the note in the on-disk pad (a duplicate task on a re-dump). That is recorded as RISK-ARCH-4, and no text is lost.
- **Whole-record check (SEC-3):** false "changed" verdicts only make undo refuse, which is the safe direction. No path deletes more than before.

## New findings

### R2-1 — pending ops are discarded without a warning when quit comes from the main screen  [LOW]
- **Anchor:** `TaskboardApp.action_quit` ("none [no CaptureView on the stack] … → `self.exit()`"); RISK-ARCH-4.
- **What:**
  - After a failed store write, the user can close the view with `esc`, `esc`. The Inbox then still holds `pending`. A quit from the board exits with no further write.
  - For a pending record, nothing is lost (RISK-ARCH-4).
  - For a pending **drop**, the task has already left its board and the restored note is only in memory. The note survives only as the `dumped` entry's `text`. The user gets it back only with `alt+u` (state "gone") within 7 days; after that it is pruned without a message.
  - The user was warned twice before this happens (the failed-write toast, then the `esc` warning), which is why this is LOW.
- **Proposed change:** in `action_quit`, if no view is on the stack and `app.inbox.pending` is non-empty, try `app.inbox.write_pad(app.inbox.pad_now())` and apply the same warn-once rule. That is one branch. If the change is not taken, extend RISK-ARCH-4 to name the pending-drop case.
- **Evidence:** `read`. Mitigation `planned`.

### INFO
- **I-r2-1:** on SEC-4's `OSError`-at-load path, `load` still calls `keep_aside` and shows "could not be read … the pad starts empty", even though the next write brings the stored notes back through the union. Nothing is lost, but the notice overstates it. Optionally, skip `keep_aside` and use a "could not be read now; it is merged at the next save" wording when the read raised `OSError` (as opposed to a parse failure).
- **I-r2-2:** SEC-6..SEC-8 were taken in design (`_links_ok`, the extended `RESERVED_STEMS`, the string lane test). SEC-9..SEC-11 are recorded risks in BACKLOG. This round did not re-review them; I check them at the increment gate.

## Evidence checklist

- [x] Each finding has: what · where · why · recommendation (R2-1). Each closure has its anchor and evidence (table).
- [x] Severities given.
- [x] No secret values in this output.
- [x] The verdict is explicit: PASS-WITH-NOTES. There is no HIGH or MAJOR. Every mitigation is `planned`, and this clearance is not the operator's authorization.
- [x] No new integration and no network surface. The correction pass adds no new dependency.
