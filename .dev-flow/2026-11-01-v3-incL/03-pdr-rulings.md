# Inc L — rulings (orchestrator, Opus)

Rulings override every older text in the requirements, the interfaces and the group graphs.

## Round 0 — the E2b prototype's findings (28: D 10, V 10, S 8)

| Id | Sev | Ruling | Applied to |
|---|---|---|---|
| P-D-1 | MAJOR | **Accept.** The legacy arm of LLR-4302.4 compares against the bytes `eb411e1` writes for the same file (a fixed oracle held in the test), not the input bytes: the migration rewrites a legacy board at base too. LLR-4302.5 runs on the plain fixture. | LLR-4302.4, LLR-4302.5 text (LED.3); graph-proto-D examples |
| P-D-2 | minor | Accept: the unknown-key fixture puts the key first in its record (where the app writes it). | D examples |
| P-D-3 | minor | Accept as designed: a non-`str` `created` moves to the front of its record on the first save; its value round-trips. Stated in LLR-4302.3's threshold (values, not bytes). | D, LLR-4302.3 |
| P-D-4 | minor | **Accept.** `Board.add_task` reads the clock once: `now = datetime.now()`, `task.created = stamp(now)` when None, `history.append(..., at=now)`, so the birth record and `created` agree to the second. | interfaces `Board.add_task` |
| P-D-5 | minor | Accept: the seed stamp is applied in `Board.load`'s seed branch; `seed_data()` is unchanged. | D |
| P-D-6 | MAJOR | **Accept as designed, documented.** The team push already sends each team task's title, notes and dates to `board.<user>.json`; `created` (the add moment) adds no new class of data within the same team. Dropping it would need a 5th source file (team_sync.py). README gets one line under the team section; backlog item L-BL-1 for an opt-out. The security reviewer may reopen it at PDR. | README note (E4 group D); BACKLOG L-BL-1 |
| P-D-7 | minor | Accept: label `Added list` (unique). | D |
| P-D-8 | minor | Accept: the `?` help's global line grows to 4 rows at 80x24; its tests stay GREEN (guard). | D |
| P-D-9 | minor | Accept in part: README gets the `N` row in the key table (:135) and in the home/global table (:329) if that table lists `A`; the history.jsonl paragraph (:400) is left (it describes history, which this increment does not change). | D |
| P-D-10 | minor | Accept: TC-4303/TC-4306 use a clock that advances 1 s per call (monkeypatched `models.datetime`), so a stamp-per-task mutant fails. | tester brief |
| P-V-1 | MAJOR | **Accept.** `added_rows` guards `history.read` with `except (OSError, ValueError)` (a non-UTF-8 byte raises `UnicodeDecodeError`). LLR-4304.12 widened; TC-4372b. | LLR-4304.12 (LED.3); interfaces `added_rows`; V |
| P-V-2 | MAJOR | **Accept.** `added_moment` returns None when `astimezone()` raises (`OSError` before 1970 on Windows, `OverflowError`/`ValueError` at the bounds). New LLR-4304.16; TC-4373b. | LLR-4304.16 (LED.3); interfaces `added_moment`; V |
| P-V-3 | minor | Accept V's proposal (meta pieces and source line wrap inside the pane at 80x24 instead of clipping). | V |
| P-V-4 | minor | Accept: no `%-d`; the day number is formatted as `str(d.day)`. | V, LLR-4303.9/4304.10 examples |
| P-V-5 | minor | Accept: one header per day; ` ≈` only when every row of that day has source `h`. LLR-4303.9 already says "a day known only from history". | V |
| P-V-6 | minor | Accept V's degrade order for the head row (drop `every board`, then the legend; the order word and counts stay). | V |
| P-V-7 | minor | Accept: a full pane ends with `… k more lines` in `HEX["dim"]`. | V |
| P-V-8 | minor | Accept: the scroll window is stateless (computed from `sel` each paint), as the agenda's. | V |
| P-V-9 | minor | Accept: tab and newline in a title/project/board name are drawn as one space. | V |
| P-V-10 | minor | Accept: `render_added_list` req list gains the 3 LLRs V named. | interfaces |
| P-S-1 | MAJOR | **Accept.** Textual cuts the non-priority binding chain at the first modal, so a key test of LLR-4303.21 cannot fail. TC-4341 asserts `app.check_action("added_list", ())` is False with a `ModalScreen` on the stack (and True without); a pilot arm checks that `N` in the task editor opens no list. LLR-4303.21 threshold rewritten. | LLR-4303.21 (LED.3); S |
| P-S-2 | minor | Accept (same clock as P-D-10). | tester brief |
| P-S-3 | minor | **Accept.** New LLR-4303.24: `enter` on an archived task while the main screen hides archived shows the existing `jump_to` notice (`<title> is archived — v shows it`) and selects nothing. | LLR-4303.24 (LED.3); S |
| P-S-4 | minor | Accept: LLR-4302.6's hashes are taken after leaving the home (`escape`), before `N`. | S, tester brief |
| P-S-5 | minor | Accept: interface examples renamed TC-4302 → TC-4302b (stamp format), TC-4366 → TC-4366b (pure reverse). | interfaces |
| P-S-6 | minor | Accept: the offer for `escape` names `AddedList.action_back`. | interfaces |
| P-S-7 | minor | Accept: `AddedList` has no `in: app` (it reads `self.app`). | interfaces |
| P-S-8 | minor | Accept: the cursor keeps its task by `(lane, pos)` (ids can repeat across boards). LLR-4306.4 "same task" means the same `(lane, pos)`. | S |

## Round 1 — PDR (architect FAIL: 1 HIGH, 2 MEDIUM, 6 MINOR; security PASS-WITH-NOTES: 3 MEDIUM, 2 LOW)

| Id | Sev | Ruling | Applied to |
|---|---|---|---|
| ARCH-1 | HIGH | **Accept.** TC-4364/TC-4365 feed `added_order` a hand-shuffled input (not lane/pos order), so a mutant that drops the tie-break or puts unknowns last turns RED. LLR-4304.4/.5 NC text rewritten. | LLR-4304.4, LLR-4304.5 (LED.4); interfaces `added_order` examples |
| ARCH-2 | MEDIUM | **Accept.** TC-4316's plain board gains one birth record in `history.jsonl` (something to back-fill from); HLR-4302's NC names TC-4316. | HLR-4302, LLR-4302.5 (LED.4); D examples |
| ARCH-3 | MEDIUM | **Accept — remove, not guard.** An offset-aware `created` or `at` is not valid (`added_moment` → None); no conversion. LLR-4304.13 rewritten; LLR-4304.16 withdrawn (P-V-2's guard has nothing left to guard). The app only ever writes naive local stamps. | LLR-4304.13, LLR-4304.16 (LED.4); interfaces `added_moment`; V |
| ARCH-4 | MINOR | Accept: the tester runs every S example; none is claimed `executed` before E4. | tester brief |
| ARCH-5 | MINOR | Accept: `AddedList.on_screen_resume` repaints (people/marks renamed under `@`/`#` show at once). Example under LLR-4303.11 (TC-4331b). | addendum A-1 |
| ARCH-6 | MINOR | Accept: LLR-4302.6's subject becomes "the list view". | LLR-4302.6 (LED.4) |
| ARCH-7 | MINOR | Reject (style): D's `_TASK_KEYS` design stands; SEC-1 touches `_to_dict` anyway and both are equally small. | — |
| ARCH-8 | MINOR | Accept: LLR-4304.11/.15 say "no task the list read (archived included)". | LLR-4304.11, LLR-4304.15 (LED.4) |
| ARCH-9 | MINOR | Accept (conformance): the key row adds the agenda's tail `· read-only: nothing here edits a task` when it fits whole, else drops it first (AllBoardsAgenda._paint). | addendum A-2; LLR-4303.19 example |
| SEC-1 | MEDIUM | **Accept — reverses P-D-6.** Remove the data from the push rather than document it: `Board._to_dict(item, with_created=False)` leaves out `created` (the field and any `extra["created"]`); `_serialized` passes `with_created=True`. `team_sync` keeps calling `_to_dict(t)` unchanged (no 5th file). New LLR-4302.7, TC-4318. The README team note is dropped. | LLR-4302.7 (LED.4); D; interfaces |
| SEC-2 | MEDIUM | **Accept.** `added_rows` guards `history.read` with `(OSError, ValueError, RecursionError)`; TC-4372c (one deeply nested line). Backlog L-BL-2: fix `history.read` at the source (Flow view crashes today). | LLR-4304.12 (LED.4); interfaces; BACKLOG |
| SEC-3 | MEDIUM | **Accept.** Birth lookups and the `after:` title lookup use only `str` ids; a non-`str` id gets no birth record and resolves no link. New LLR-4304.17, TC-4377. | LLR-4304.17 (LED.4); V |
| SEC-4 | LOW | Accept: the pane wraps at most `room × (rw + 1)` characters of the cursor's note; when cut, the tail reads `… more lines` (no count). | addendum A-3 |
| SEC-5 | LOW | Backlog L-BL-3 (inherited `peek_board` race). | BACKLOG |

Round 2 (blocking-only re-review): architect re-checks ARCH-1..3; security re-checks SEC-1..3.
