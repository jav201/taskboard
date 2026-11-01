# E4 integration — Inc K (GREEN-1 → GREEN-2)

Input: GREEN-1 (`evidence/green-1.txt`) on code feeac40 + tests 626c3f6: 27 failed / 438 passed.
Output: working-tree fixes (not committed), GREEN-2 in `evidence/green-2.txt`, guards in `evidence/guards-1.txt`.

Classes: **seam 21** (one root cause) · **impl 2** · **test 4** (TC-4675 also needed one fixture line, see its row).

## Fixes

| # | Fix | Class | File:line |
|---|---|---|---|
| F1 | `Color` imported from `textual.color`, not `rich.color`. `ReviewList.on_mount` sets `self.styles.background = Color(13, 17, 23, 0.6)` (graph-proto-V P-V-9). Textual's `styles.background` accepts only a `textual.color.Color` or a str, so a `rich.color.Color` raised `StyleValueError` and every ReviewList mount crashed. No other `Color` use in app.py (base 545c18a had no import). | seam | `taskboard/app.py:17` (uses it at `:2135`) |
| F2 | `action_image` sets `self._text = pad.text` after `pad.insert` and before `self._flush()`. `_flush` → `_unsaved()` reads `self._text`, which `on_text_area_changed` sets only later (that is a posted message), so the attach was never written at once. `_replace_pad` already does this for dump and undo. | impl | `taskboard/app.py:2033` |
| F3 | `Inbox.load` parses the capped bytes it already read (`cls._parse(head)`) instead of calling `_read(path)` a second time. `_read` keeps its contract and delegates to the new `_parse(data)`. Without this, a store over the cap was read twice: 2 × (cap + 1) bytes, against LLR-4407.35. | impl | `taskboard/inbox.py:453`, `:456`, `:502` |
| F4 | Test helper `_edit_task(path, title, /, **fields)`: `title` is now positional-only. The parametrize arm `{"title": "Volume lab fixed"}` collided with the helper's own `title` parameter (`TypeError`), so that arm never reached the app. | test | `tests/test_capture_view.py:1610` |
| F5 | TC-4582 compares the decoded file with `os.linesep` normalised to `\n`. The graph keeps `models.write_atomic` "unchanged on purpose" (graph-proto-S §Called-by). It writes in text mode, so Windows newlines are `\r\n`, as for boards, people and marks. Still asserted: key order, `indent=2`, `ensure_ascii=False` (the C3 A9 bytes, no `é`), no `flagged` key, and `divider_notice` last. | test | `tests/test_inbox_store.py:742` |
| F6 | `capture_fixture.write_store(raw=…)` writes `raw.encode("utf-8")` as bytes. `_store_of_size(n)` promises a file of exactly `n` bytes, but `write_text` added 4 × `\r` on Windows. Once F3 let TC-4675's second arm run, the CAP-byte store became CAP + 4 bytes and read as over the cap. | test (harness) | `tests/capture_fixture.py:280` |
| F7 | TC-4488 scores the raw AT-4402 note (with its image line) over F, and its scored text over F + Shots, as graph-proto-T's TC-4488 / AT-4402 examples state. Over F + Shots the image line's `png`/`board` legitimately hit `Png board`: graph-proto-T line 247 says so, and the test's own NC arm proves it. The extra Shots document shifts idf (0.6678), so that arm compares to 3 places, the graph's own precision (`0.668`). | test | `tests/test_suggest.py:562-565` |
| F8 | TC-4321's expected global-key row gains `n` after `N` (LLR-4401.1: `n` is one global key placed directly after `N`). This test update was known in advance. | test | `tests/test_added_list.py:881` |

## Per failing test

| Test (GREEN-1) | Class | Root cause | Fix |
|---|---|---|---|
| test_inbox_store::TC-4582 | test | Platform newlines from the unchanged `write_atomic` | F5 |
| test_inbox_store::TC-4609 | impl | `_text` stale at the attach's `_flush` | F2 |
| test_inbox_store::TC-4675 | impl (+ harness) | `load` read the file twice; then the fixture's text-mode `raw` write made the CAP file CAP + 4 bytes | F3, F6 |
| test_suggest::TC-4488 | test | The raw-with-image arm was run over F + Shots, not F | F7 |
| test_capture_view::TC-4517 | seam | ReviewList mount crash (rich vs textual `Color`) | F1 |
| test_capture_view::TC-4550b[edit0] | test | Helper kwarg `title` collision | F4 |
| test_capture_view::TC-4634 | seam | ReviewList mount crash: the review row was empty | F1 |
| test_capture_view::AT-4404 | seam | ReviewList mount crash | F1 |
| test_capture_view::TC-4561 | seam | ReviewList mount crash | F1 |
| test_capture_view::TC-4562 | seam | ReviewList mount crash | F1 |
| test_capture_view::TC-4563 | seam | ReviewList mount crash | F1 |
| test_capture_view::TC-4564 | seam | ReviewList mount crash | F1 |
| test_capture_view::TC-4565 | seam | ReviewList mount crash | F1 |
| test_capture_view::TC-4566 | seam | ReviewList mount crash | F1 |
| test_capture_view::TC-4567 | seam | ReviewList mount crash | F1 |
| test_capture_view::TC-4568 | seam | ReviewList mount crash | F1 |
| test_capture_view::TC-4569 | seam | ReviewList mount crash | F1 |
| test_capture_view::TC-4570 | seam | ReviewList mount crash | F1 |
| test_capture_view::TC-4571 | seam | ReviewList mount crash | F1 |
| test_capture_view::TC-4572 | seam | ReviewList mount crash | F1 |
| test_capture_view::TC-4573 | seam | ReviewList mount crash | F1 |
| test_capture_view::TC-4575 | seam | ReviewList mount crash | F1 |
| test_capture_view::TC-4576 | seam | ReviewList mount crash | F1 |
| test_capture_view::TC-4577 | seam | ReviewList mount crash | F1 |
| test_capture_view::TC-4484c | seam | ReviewList mount crash | F1 |
| test_capture_view::AT-4405 | seam | ReviewList mount crash | F1 |
| test_added_list::TC-4321 | test | `n` is now a global key after `N` | F8 |

## Left as is

- **DEV-S-2** (`c is busy` vs `Course is busy`): no requirement fixes the board's display name in the lock label. The tester asserts only `is busy`. Not touched.

## Risk raised for a ruling (not fixed)

- **Store bytes on Windows (R-E4-1).** LLR-4407.37 counts the store as `len(json.dumps(...).encode())`, which TC-4677 pins at 8 400 047. `write_atomic` writes `\r\n`, so the file on disk is larger by the number of JSON lines (about 4 + 12 per dumped entry). Suppose a write lands within that margin under the cap: on disk it is over the cap, so the next `load` treats it as unreadable (LLR-4407.35) and does not copy it aside (LLR-4407.36), and the pad starts empty. Either fix changes a shared function or a pinned example, so neither is applied here:
  - (a) `write_atomic` writes `newline="\n"`. This changes the bytes of every board, people and marks file on Windows.
  - (b) The store is written as bytes through a store-only path. The tester's `write_atomic(path, text)` spies would need to follow.

## Resumed conductor (after the integration agent's hand-back)

| # | Fix | Class | File:line |
|---|---|---|---|
| F9 | TC-4685 arm 1 injects the load's OSError at the OPEN of `inbox.json` (`_fail_open`, a sharing violation) instead of patching `Inbox._read`: after F3, `load` reads the file once itself and parses with `_parse`, so the `_read` patch no longer reached it (GREEN-2 first run: `p` loaded). Behaviour unchanged: a failed read at load keeps the stamp None. NC re-proven: `inbox._stamped()` taken after a failed read → arm 1 RED. The refresh arms still patch `_read` (refresh reads through it). | test (seam after F3) | `tests/test_inbox_store.py` `_fail_open`, TC-4685 |
| R-E4-1 | Ruled (03-pdr-rulings.md): `Inbox._commit` counts the bytes on disk, `len(data) + text.count("\n") * (len(os.linesep) - 1)`; `write_atomic` unchanged. TC-4677's count per platform; new TC-4677c (real filesystem, `os.path.getsize` at CAP and CAP + 1), RED before the fix (`DID NOT RAISE`). | design-gap | `taskboard/inbox.py` `_commit`; `tests/test_inbox_store.py` TC-4677, TC-4677c |

Note: the first GREEN-2 re-run overlapped with the integration agent's own run in the same worktree; GREEN-2 below is the clean re-run after F9.
