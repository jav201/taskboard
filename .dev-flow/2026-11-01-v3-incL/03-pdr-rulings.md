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
