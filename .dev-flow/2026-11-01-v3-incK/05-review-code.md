# Inc K — E5 independent code review — code-reviewer

**Verdict: PASS-WITH-NOTES.** No finding is HIGH or MAJOR. There are 8 findings: 1 MEDIUM and 7 MINOR. 3 are `impl` (CR-3, CR-5, CR-6) and 5 are `design-gap` (CR-1, CR-2, CR-4, CR-7, CR-8). The code follows the approved graph and the rulings ARCH-1..ARCH-8, SEC-1..SEC-8, A-1..A-4 and R-E4-1. The MEDIUM finding, CR-1, is a hole in the design: `mark_notice` holds the fresh `dumped` while keeping its stale pad. That defeats SEC-1's unseen-entry multiset, and a probe confirms it. It is a one-line fix and I recommend it before merge. It does not block, because it needs two windows plus a first-ever divider render in between, and the result is a duplicate the user can see, not a silent loss. In the role file's tokens this is *OK to advance*, with notes.

## Scope reviewed

- **Diff.** `git diff 545c18a f931070 -- taskboard/ README.md tests/`: 11 files, +8503/−11. The working tree equals `f931070` for `taskboard/` and `tests/` (`git diff --quiet`). I read:
  - all of `taskboard/inbox.py` (1171 lines) and all of `taskboard/suggest.py` (256 lines);
  - `taskboard/app.py` at `f931070`: imports :8-47, the capture block :1307-2210 (`GHOST`, `CAPTURE_KEYS`, `RailNote`, `ReviewRow`, `hit_text`, `capture_head`, `capture_hint`, `rail_rows`, `review_rows`, `PadArea`, `CaptureView`, `ReviewList`), `TaskboardApp.__init__` :2243-2250, `check_action` :2313-2340, `action_capture`, `_retry_pending_once`, `action_quit` :2472-2503, and `_bring` / `board_lanes` for context;
  - `taskboard/keymap.py:148-149` and `README.md:137`;
  - the one-line test edits in `tests/test_added_list.py` and `tests/test_modal_keys.py`.
- **Tests, sampled for intent.** `tests/test_inbox_store.py` (TC-4444, 4599, 4600, 4688, 4689, 4628, 4622c, 4677c, 4681/4681b, 4682/4682b), `tests/test_capture_view.py` (TC-4419, 4577, 4484c), `tests/test_suggest.py` (TC-4489, 4489b) and `tests/capture_fixture.py` (`need`, `write_store`). I did not read every one of the 267 test functions line by line. I scanned the whole of all three files for skips, `except Exception` and conditional asserts.
- **Design read.** `graph-interfaces.cw.md` in full. The `Inbox.*` contracts of `graph-proto-S.cw.md` (:226-334). `CaptureView._paint` in `graph-proto-V.cw.md`. `03-pdr-rulings.md` including R-E4-1, `00-orchestrator-rulings.md`, `e4-addenda.md`, `e4-deviations.md` (DEV-S-1, DEV-S-2: both acceptable) and `e4-integration.md` F1-F9. In `01-requirements.md`, I read only the LLRs cited below.
- **Probes (read-only).** Interpreter `C:/Users/jjgh8/anaconda3/python.exe -I` (3.12.7), `env -u NO_COLOR`, scratch in `%TEMP%\incK_cr\` (deleted afterwards). `taskboard.__file__` = `C:\Users\jjgh8\Github\taskboard-wt\capture-proto\taskboard\__init__.py`.
  - ARCH-8: after `import taskboard.inbox`, no `textual*` module is in `sys.modules` (`executed`).
  - CR-1 reproduction (`executed`, see CR-1).
  - I did not run the suite. `evidence/green-2.txt` reads 466 passed, 0 skipped.
- **Not my lane.** Mutants (`../incK-mut`, not touched), the suite as a whole (qa), security (closed at PDR), and the captures.

## Design conformance (asked explicitly)

| Ruling | Where | State | Evidence |
|---|---|---|---|
| ARCH-1: dump and undo apply to the FRESH state, and only typing unions | `inbox.py:626-647`: `change` applies pending, then record, then drop, to `base` (the fresh read under `file_lock`). A record removes the first equal fresh note (`_remove_first_note`); a drop appends with `with_note` only when the entry was held. `union_pads(p_after_ops, unseen, pad)` runs only when `changed`. | conforms (`executed` by reading; TC-4688 / TC-4689 cover cases D and U, each with its NC) | the code reads like `people.Directory._commit` (`people.py:216-236`): mkdir, then lock, then fresh read, then set-aside, then change, then `write_atomic`, then hold |
| SEC-1: unseen = fresh entries this Inbox did not hold (multiset) | `inbox.py:640-642`, `union_pads` :313-327 (`Counter` budget) | conforms, except for the `mark_notice` hold (CR-1) | TC-4599 arms 1-4 |
| ARCH-2: choice keyed by `(board path, project id)` / `NEW_KEY`, batch targets fixed | `app.py` `_key`, `chosen` (falls back to the top, never an index); `ReviewList.action_dump` builds `targets` before the loop, uses `rebuild=False`, and rebuilds once when `k > 0` | conforms | TC-4577 (NC is the re-resolved 0.6028), TC-4484c (1 `corpus` call) |
| ARCH-3: `capture` refused under the home | `check_action` :2316, before the always-allowed tuple | conforms | TC-4419 (`check_action` arm plus the board bytes unchanged) |
| ARCH-4: pending records retried; `flagged` gone | `write_pad` puts its record or drop in `pending` on any OSError and clears it only after a successful write; `pad_now` and `last_dump` apply pending; `_unsaved` counts pending; `_retry_pending_once` and `action_quit` (A-3) | conforms, except the home's `q` path (CR-3) | TC-4681/4681b, TC-4682/4682b, TC-4558 |
| ARCH-6: corpus cached | `suggest.corpus` computes `_idf`, `vec` and `norm` once; `suggest` reads them; the view's `_hits` keyed by note text is cleared on each rebuild | conforms; the cache has no eviction (CR-4) | TC-4489 (`_idf` spy = 1 call), TC-4489b |
| ARCH-7: no `_new_task_id` retry | `_dump_open` / `_dump_other` call `models._new_id()` once; `dest_dir.mkdir()` is exclusive | conforms | read |
| ARCH-8: inbox.py imports no UI module | `inbox.py:33-36`: `history`, `models`, `views`, `boards`. `views` pulls in rich only. | conforms | probe: no `textual` in `sys.modules` |
| SEC-2: encode probe | `_parse` probes at the door, `dump_note` refuses before any board write, `_commit` turns `UnicodeError` into `OSError` | conforms | TC-4683/4684/4534 (read) |
| SEC-3: whole-record changed-check, plus `needed` | `_unchanged` compares `asdict` of the task against `expected`; `_needed` | conforms | TC-4550 ×N, TC-4559 |
| SEC-4: a failed read keeps the old stamp | `load` (`read_failed`), `refresh` | conforms | TC-4685 (F9) |
| SEC-6: no unlink through a link or junction | `_links_ok` (`islink`, `is_junction`; Python ≥ 3.12 per `pyproject.toml`) and the resolve-parent check, the same rule as `move_project`'s `img_src` filter (`boards.py:792-796`) | conforms (a re-statement, not a shared helper: `move_project` inlines it, so there is no helper to reuse) | TC-4622c (symlink), junction arm (not skipped in green-2) |
| SEC-8: undo lane test by normalised string | `CaptureView.action_undo` and `_where` (`normcase(abspath(...))`) | conforms | read |
| R-E4-1: cap counts the bytes on disk | `inbox.py:601-606`, `len(data) + text.count("\n") * (len(os.linesep) - 1)`. This is exact: `json.dumps` escapes every newline inside a string, so each raw `\n` in `text` is a structural one. `write_atomic` is unchanged. | conforms | TC-4677, TC-4677c (`os.path.getsize`) |
| `write_atomic` / `file_lock` / `keep_aside` / `peek_board` reuse | all imported, none re-implemented. `_file_stamp` is a deliberate copy of `boards._stamp`: it returns None on any OSError, where the original raises, and it avoids a private import. | conforms | read |

## Findings

### CR-1 — `mark_notice` holds the fresh `dumped` with a stale pad, so another window's dump comes back  [MEDIUM · design-gap · `executed`]

- **Where:** `taskboard/inbox.py:714` (`self.dumped = list(new["dumped"])`, which runs even when `changed`). The design states it in `graph-proto-S.cw.md:328`: "After the write: divider_notice and dumped held; pad and `_stamp` held ONLY when changed is False".
- **What:** SEC-1's unseen set is "fresh entries whose (task, board) this Inbox did NOT hold". When the file changed, P-S-5 rightly keeps `mark_notice` from adopting the pad and the stamp. It still adopts `dumped`. So the next typing write treats another window's fresh dump as already seen, while this window's stale pad still holds that note. The union then keeps the note.
- **Probe:** a store holds pad `x|b`, and windows X and Y load it. Y dumps `b` (`write_pad("x", record=e(b))`). Then X calls `mark_notice()`, and X's next typing write is `write_pad("x\n____\nb\n____\nd")`.
  - As shipped: the stored pad is `x\n____\nb\n____\nd` with `union=False`. `b` is back, the user gets no merge notice, and a later `alt+d` makes a second task.
  - With `dumped` not held: `x\n____\nd`, `union=True`.
- **Why:** SEC-1 and ARCH-1 were rated MAJOR because of this exact outcome. The window is narrow: X must draw its first-ever divider rule after Y wrote and before X's own next write, and `divider_notice` must still be false in X's memory. So I grade it MEDIUM, not MAJOR.
- **Fix:** hold `dumped` with the pad, only when the file was unchanged:
  ```python
  new, changed = self._commit(change)
  self.divider_notice = new["divider_notice"]
  if not changed:
      self.pad = new["pad"]
      self.dumped = list(new["dumped"])
      self._stamped()
  ```
  Add a TC-4444 arm that reproduces the probe and asserts the stored pad `x\n____\nd` (NC: the current line 714). Then amend `graph-proto-S` `Inbox.mark_notice` to read "divider_notice held; pad, dumped and `_stamp` held only when changed is False".

### CR-2 — The store stamp is taken outside the lock (and after the read in `load`)  [MINOR · design-gap · `not-run`]

- **Where:** `taskboard/inbox.py:660`: `write_pad` calls `self._stamped()` after `_commit` has released `file_lock`. `inbox.py:497-514`: `load` reads first and stats afterwards. `mark_notice` :717 does the same as `write_pad`.
- **What:** in the Inbox, the stamp decides between "write my pad verbatim" and "union". Suppose another window completes a write between our `write_atomic` and our `os.stat` (or, in `load`, between the read and the stat). We then hold its stamp with our own content, and our next write overwrites its notes verbatim. `people.Directory` has the same shape, but there the stamp only gates a reload; every write re-reads fresh, so nothing is lost.
- **Why:** the window is microseconds wide, but a hit loses a note silently. The design (`graph-proto-S.cw.md:226`, "taken after every … successful write") copies Directory's order without noting that the stamp's role changed.
- **Fix:** take the stamp inside the lock. `_commit` returns `_file_stamp(self.path)` read right after `write_atomic`, before the `with` block exits, and `write_pad` / `mark_notice` assign it. In `load`, stat before reading, as `refresh` already does. A change between the stat and the read then shows up as "changed", which is the safe direction.

### CR-3 — The home's `q` exits without A-3's pending retry  [MINOR · impl · `executed` (read)]

- **Where:** `taskboard/app.py:674` (`BoardsHome` binds `q` → `quit_app`) and `:844-845` (`self.app.exit()`). A-3 lives in `TaskboardApp.action_quit` :2486-2503 only.
- **What:** A-3 says "`action_quit`, from any screen, first retries a held pending store write once". Here is one way to reach it: a dump's store write fails, so a record is pending. The close-time write in `on_unmount` fails too and is swallowed. The user goes to the boards home with `B` and presses `q`. No retry happens. The note stays recoverable by `alt+u`, which matches A-3's recorded risk, but the promised retry is skipped. `ctrl+q` is fine: it reaches `action_quit`.
- **Fix:** `BoardsHome.action_quit_app` calls `self.app._retry_pending_once()` before `self.app.exit()`, or delegates to `await self.app.action_quit()`. Add a pilot arm to TC-4681b: pending record, then home, then `q` → the store holds the entry.

### CR-4 — The hit cache grows by one entry per keystroke  [MINOR · design-gap · `executed` (read)]

- **Where:** `taskboard/app.py:1634-1643` (`options_for`), called for every note on each `_paint`. Each `TextArea.Changed` triggers a `_paint`.
- **What:** `_hits` is keyed by the note's full text and is cleared only by `_rebuild_docs` (open, dump, undo, batch). Typing a note of n characters leaves about n keys whose lengths add up to about n²/2 characters. A 5 000-character note typed in one session holds about 12.5 M characters of dead keys. ARCH-6 asked for a cache keyed by text and did not bound it.
- **Fix:** in `_paint`, after the loop, keep only the current texts:
  `live = {p.text for p in notes}; self._hits = {t: h for t, h in self._hits.items() if t in live}`.
  This keeps one dict pass per paint and preserves the "computed at most once per distinct text while it stays in the pad" behaviour that LLR-4403.21's tests check.

### CR-5 — `mark_notice` writes when the file's flag is already true  [MINOR · impl · `executed` (read)]

- **Where:** `taskboard/inbox.py:700-712`.
- **What:** `graph-proto-S.cw.md:328` says "the file's flag already true → divider_notice = True, no write". The code returns early only on the in-memory flag. Otherwise it always runs `_commit`, which rewrites the file with the same flag. The extra write is harmless today: it bumps the file's stamp, so other windows union on their next write. But it is a write the design said would not happen.
- **Fix:** inside `change`, there is no cheap way to skip the write. Instead, before `_commit`, read the file (`state = self._read(self.path)`, in a try) and, when `state` is not None and `state["divider_notice"]` is true, set `self.divider_notice = True` and return. Or record the deviation in `e4-deviations.md`, if the orchestrator prefers the simpler code.

### CR-6 — The pending-op step is written twice; the view's write-result handling three times  [MINOR · impl · `executed` (read)]

- **Where:**
  - `taskboard/inbox.py:629-639` (`write_pad.change`) and `:667-678` (`pad_now`) hold the same record/drop loop. `last_dump` :692-697 holds a third, entries-only variant.
  - `taskboard/app.py`: `_flush` :1749-1759, `_dump` :1897-1905 and `action_undo` :2078-2087 each repeat `self._saved = res.pad; if res.pad != pad.text: replace; if res.union: notify(<the same merge sentence>)`.
  - `KEEP_DAYS` (`inbox.py:40`) is defined and never used.
- **Why:** `pad_now` must apply the ops "as write_pad applies them" (LLR-4407.42). Two hand-kept copies can drift, and no test pins them against each other on a mixed record+drop sequence; TC-4682 covers records only. The merge sentence appears three times.
- **Fix:** add `def _apply_ops(pad, dumped, ops) -> tuple[str, list]` in inbox.py and use it in both `change` and `pad_now`. Add `def _took(self, res, pad, row=None)` in CaptureView for the three result sites. Delete `KEEP_DAYS`, or use it in `KEEP_SECONDS = KEEP_DAYS * 86_400`.

### CR-7 — The narrow rail is cut at a fixed 78 cells  [MINOR · design-gap · `not-run`]

- **Where:** `taskboard/app.py:1688` (`48 if wide else 78`). The value comes from the graph-proto-V `_paint` func.
- **What:** below 100 columns the rail is `1fr` wide, so its content width is `w − 2`. On a terminal narrower than 80 columns, the 78-cell rows are longer than the Static. The outer `Text` is not `no_wrap`, so they wrap, and the 7-row narrow rail (LLR-4401.8) loses its lower lines. The operator's standing rule is to derive layouts for any width.
- **Fix:** `rail_rows(..., 48 if wide else max(1, w - 2), ...)`, plus a TC-4408 arm at 60x24 that asserts no rail row wraps.

### CR-8 — A failed open-board dump leaves an orphan birth record  [MINOR · design-gap · `executed` (read)]

- **Where:** `taskboard/inbox.py:899` → `models.Board.add_task` (`models.py:1301-1310`). That method appends the history birth before `self.save()`.
- **What:** when `save()` raises, `_dump_open` correctly removes the task, the new project and the copies (LLR-4404.15). But `history.jsonl` keeps a birth line for an id that exists on no board. The design text ("`live.add_task(task)` (stamps created, writes the birth record, saves); an OSError → task and new project removed …") does not mention the line. Inc L's added list reads births by task id, so the orphan is inert there, but it is a write the refusal says did not happen ("nothing dumped").
- **Fix:** I lean towards recording it as a known risk in `e4-deviations.md`. `history` is append-only, and changing `add_task`'s order touches Inc L's P-D-4 single-clock rule. If a code fix is preferred: in `_dump_open`, stamp `task.created` and call `live.tasks.append(task); live.save()` yourself, then `history.append(...)` after the save, mirroring `_dump_other`.

## Notes (not findings)

- **Simplicity.** Both new modules are proportionate to the design. The parsing helpers are single-purpose and linear. `suggest.py` is pure: it imports only the standard library and reads attributes only. The two board-write paths (`_dump_open` / `_dump_other`, `_undo_open` / `_undo_other`) are deliberately separate per R1-3 and S-a, and I would not merge them.
- **DEV-S-1 / DEV-S-2.** Both are acceptable. DEV-S-1's extra `note` parameter is needed to keep a missing image's line. DEV-S-2's lock label `c is busy` is cosmetic, and the tester asserts `is busy` only.
- **`union` is False when the union changed nothing.** `WriteResult.union = changed and written != pad` (`inbox.py:661`) suppresses the merge notice when the merge was a no-op. That follows proto-S, and it is why CR-1's resurrection is silent.
- **Undo of an unreadable registered board** reads "`<path>` is not a known board" (`app.py` `action_undo`), because the lane test skips lanes whose board is None. The wording is slightly off; it is harmless.
- **UI-thread lock waits.** `_notice_divider` → `mark_notice` and every `_flush` take `file_lock` synchronously, up to `LOCK_WAIT`, inside `_paint` or an action. This is the same as every other store write in the app, so it is not a finding.
- **Test intent.** Each sampled TC names its LLR, the reason it matters, and an NC that is reachable and stated in the docstring. Examples: TC-4688/4689, whose NC is the typing union; TC-4599 arms 3-4, whose NCs are "exclude every dumped text" and set membership; TC-4577, whose NC is re-resolving after earlier dumps; TC-4489, a spy call count. I found no vacuous asserts. TC-4419 presses `escape` a second time conditionally, but the screen it depends on is asserted afterwards, so it cannot pass vacuously. The two `pytest.skip` paths (Pillow missing, symlink privilege) did not fire in green-2. Two gaps have no test: CR-1's two-window `mark_notice` case and CR-3's home-`q` path.

## Evidence checklist

- ✓ Diff read in full for source: `inbox.py` 1-1171, `suggest.py` 1-256, `app.py` :8-47, :1307-2210, :2243-2250, :2313-2340, :2472-2503, `keymap.py:148-149`, `README.md:137`. Tests sampled as listed under *Scope*.
- ✓ Correctness pass: the conformance table, plus the edge, None and error paths of `_commit`, `load`, `refresh`, the dump and undo branches, and `action_quit`. CR-1 was reproduced by probe; CR-2, CR-3 and CR-8 were found by reading.
- ✓ Simplicity pass: no premature abstraction. The duplication is in CR-6.
- ✓ Reuse checked: `write_atomic`, `file_lock`, `keep_aside`, `peek_board`, `history.append`, `strip_controls`, `clean_strings`, `save_pil_image`, `IMAGE_EXTS`, `PROJECT_COLORS`, `board_lanes`, `_bring`, `key_line`, `InkArea` and `views.highlight_segments` are all reused. Nothing is re-implemented except the intentional `_file_stamp`.
- ✓ Tests reviewed for intent: see Notes. There are no false-confidence tests, and the two gaps are in CR-1 and CR-3.
- ✓ Verdict explicit: PASS-WITH-NOTES. No HIGH was found, so none needs applied-and-verified evidence.

## §4b `Independent review` cell

`code-reviewer` · OK to advance (PASS-WITH-NOTES: 0 HIGH, 0 MAJOR, 1 MEDIUM, 7 MINOR — CR-1, CR-2, CR-4, CR-7, CR-8 design-gap; CR-3, CR-5, CR-6 impl; CR-1 recommended before merge) · no HIGH to resolve
