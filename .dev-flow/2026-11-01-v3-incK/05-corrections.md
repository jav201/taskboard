# Inc K — E5 corrective pass (the one pass ruled in `03-pdr-rulings.md` §E5)

**Result.** Every item ruled FIX is fixed, each behind a test that was RED first. Two items had no behavioural RED on `f931070`, so each was proved RED under a temporary mutant: K-SEC-3 (the main-screen retry already worked, only its test was missing) and M48 (the code was right, the test could not fail). Nothing was left for BACKLOG. CR-2 stayed local to `inbox.py`. K-SEC-5 is a one-line clamp. Source files: 2 of 4 (`taskboard/inbox.py`, `taskboard/app.py`). Tests: `tests/test_inbox_store.py`, `tests/test_capture_view.py`. RED/GREEN lines: `evidence/red-e5.txt`. Full-file run: `evidence/green-3.txt`. Requirements: `LED-2026-11-01-incK.6` adds 3 LLRs and rewords 5 (`01-requirements.md`, `01-requirements-ledger.md`). Graph contracts amended in place: `graph-proto-S.cw.md` (`Inbox.load`, `Inbox._stamped` removed, `Inbox._commit`, `Inbox.write_pad`, `Inbox.mark_notice`, `_free_name`, `_images_back`) and `graph-proto-V.cw.md` (`TaskboardApp.action_quit`, `CaptureView.on_mount`, `CaptureView._paint`).

| Item | Finding | Tag | Fix (file:line) | Test | RED reason | GREEN |
|---|---|---|---|---|---|---|
| 1 | CR-1 (MEDIUM): `mark_notice` held the file's `dumped` with its stale pad, so another window's dump came back | design-gap | `taskboard/inbox.py:716-719`: `dumped` is held with pad and stamp only when `changed` is False | TC-4444c (new, LLR-4402.14) | f931070: stored pad `x\|b\|d` instead of `x\|d` (the dumped `b` came back) | PASSED |
| 2 | CR-2: stamp taken after the lock / after the read | design-gap | `taskboard/inbox.py:602` (`_commit` stats under the lock right after `write_atomic` and returns the stamp), `:645/:655` (`write_pad`), `:714/:719` (`mark_notice`), `:484` and `:526` (`load` stats BEFORE the read). `Inbox._stamped` had no caller left, so it was removed | TC-4599b, TC-4599c (new, LLR-4407.19) | f931070: another window's `z` overwritten: `a\|q` / `p\|q` instead of `a\|z\|q` / `p\|z\|q` | PASSED |
| 3 | CR-3 + K-SEC-3: home `q` skipped A-3's retry; no test for A-3 | impl | `taskboard/app.py:844-845`: `BoardsHome.action_quit_app` awaits `self.app.action_quit()` (one quit path) | TC-4691 ×4 (new, LLR-4407.51): main/home × retry succeeds/fails | home arms on f931070: 3 store writes, not 4, and no entry. Main arms GREEN on f931070, and RED under the mutant that skips `_retry_pending_once` | PASSED ×4 |
| 4 | CR-5: `mark_notice` wrote when the file's flag was already true | impl | `taskboard/inbox.py:702-708`: `_read` first; flag already true → hold True, return (no write) | TC-4444d (new, LLR-4402.14) | f931070: 1 `write_atomic` call | PASSED |
| 5 | CR-7: narrow rail cut at a fixed 78 | design-gap | `taskboard/app.py:1692`: `max(1, w - 2)` | TC-4408b (new, LLR-4401.8) at 60x24 | f931070: a 76-cell row in a 58-cell rail | PASSED |
| 6 | K-SEC-1: `undo_dump` could raise after the board save | impl | `taskboard/inbox.py:1104-1108` (mkdir guarded: OSError → no renames) and `:1118` (`_free_name` inside the guarded step). A leftover stays silent per RISK-P-S-12 | TC-4651 (new, LLR-4408.21), with `inbox-images` a regular file: one arm without an image, one with | f931070: `FileExistsError` from `undo_dump` | PASSED |
| 7 | K-SEC-2: OSError at load showed "no copy could be kept" | impl | `taskboard/inbox.py:503` (`load_report["read_failed"]`); `taskboard/app.py:1594-1597` show A-4's wording | TC-4690 (new, LLR-4407.50) | f931070: the LLR-4407.38 notice was shown | PASSED |
| 8 | M48 test gap: no arm could tell a capped read from a whole-file read | impl (test) | no product change | TC-4675: new arm with a valid store of CAP + 4096 bytes, ≤ CAP + 1 bytes read | GREEN on f931070 (correct code). RED under M48 (`head = fh.read()`): 8 392 704 bytes read | PASSED |
| 9 | K-SEC-5: `_free_name` could yield a 130-char name | impl | `taskboard/inbox.py:731`: stem cut to `IMAGE_NAME_MAX − len(suffix) − len(str(k)) − 1` (one line) | TC-4613b (new, LLR-4408.3) | f931070: a 130-char name that fails `image_name` | PASSED |

## Notes

- **The TC-4690 expectation was corrected after GREEN.** The test first asserted pad `""`. The view's open refresh re-reads the file once it is readable, so the pad shows `p`. That is the intended no-loss outcome (A-4: "its notes merge back"). The RED on f931070 was at the notice assertion, which comes before the pad assertion.
- **TC-4691 counts the close path as it is.** `esc` with a failed flush warns and arms. A second `esc` closes, and its `on_unmount` write is the third failed write. The retry at `q` is the fourth.
- **Both mutants were restored before any fix.** `git diff --stat taskboard/` was empty after the restore (red-e5.txt).
- **The count line was stale.** In `01-requirements.md` §7 it still showed active 205, from before LED.5's two withdrawals. It now reads active 206, which includes the 3 new LLRs.

## Left / not in this pass

- **None of the 9 items is left.** CR-4, CR-6, CR-8 and K-SEC-4 stay BACKLOG, as ruled in `03-pdr-rulings.md` §E5. I-1..I-3 are handled at close.

## GREEN-3

`executed`: the 7 files gave **478 passed**, 0 failed, 0 skipped, exit code 0, in 301.75 s (2026-11-01T14:06:45Z → 14:11:49Z). GREEN-2 had 466; the 12 extra are the new test cases. Source: `evidence/green-3.txt`. The full suite was not run, as instructed.
