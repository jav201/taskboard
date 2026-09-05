# Quick Spec — taskboard · batch "wedge" (F-16: the columns card that never re-renders)

**Batch:** `2026-09-05-fastflow-12` · **Base:** worktree `kanban-variants`, HEAD `2817550` (inc21, the
pinned signature and the re-baked frames), pushed. Predecessor `capture-settle` closed 2026-09-05, §8
filled, archived verbatim to `archive/spec-20260905-capture-settle-closed.md`. Language: English.
Increments continue the worktree's single sequence: **inc20 · inc21 … inc22**.

**Input:** `.fast-dev-flow/03-increments/inc20.md` §5 and §8, and `inc21.md` §7 — the predecessor's own
finding, filed as **F-16** and named there as the next task.

The input in three lines:

1. **The app wedges.** 3 of 30 cross-process sweeps of `capture_languages.py` FAIL LOUD. Always the
   COLUMNS branch (`board instrument`, `board industrial`, `board naught`), always four DOING-column
   `TaskCard`s at one uniform seat, always holding a paint composed at the 20-cell fallback while their
   real seat is 31 or 33.
2. **It is permanent, and that was measured.** A probe kept the loop alive **640 iterations / 19.5 s**
   past the settle bound; the same four cards still read `Design home…` where their seat draws
   `Design homepage moc…`.
3. **`on_mount`'s `call_after_refresh(self.render_card)` and `on_resize` are both meant to correct it
   and neither does.** The old settle WROTE that frame — it is 2 of F-1's 6 drifting frames — and the
   new one refuses it. The refusal is right; the defect is `kanban.py`'s.

---

## 1. Objective (1 line)

Make a `TaskCard` compose at the seat it is drawn at, so the documented sweep finishes every time
instead of nine times in ten — without moving a frame that is already right.

---

## 2. User stories

- As **anyone rebuilding the gallery**, I want the documented sweep to finish, so that a re-bake is a
  command and not a retry loop (`inc21.md` §5: "F-16 makes any re-bake a retry loop … a trap for
  anything that automates the sweep without checking the return code").
- As **anyone reading the board at a narrow column**, I want the card to draw the title its seat can
  hold, because a card holding a bake composed for a seat 13 cells narrower is throwing away a third of
  the row it was given.
- As **the next reader of `kanban.py`**, I want the reason `on_resize` is not the repair written where
  the repair is, because "the widget HAS an `on_resize` and it still went stale" is exactly the thing
  that costs the next person an afternoon.

---

## 3. Acceptance criteria (observable)

- [x] **AC-1 · inc22 · the wedge is diagnosed, not guessed.** The packet carries a state dump taken at a
  real wedge: which widget's CONTENT ≠ SHADOW, its `size`/`region`, whether a refresh or a deferred
  callback is pending, the message-queue depths, whether the widget is displayed and drawn, and whether
  the truncated title is the card's OWN render or a stale Strip in the compositor's cache. One
  falsifiable mechanism, named down to the framework lines that produce it.
- [x] **AC-2 · inc22 · the rate moves to zero.** `race_probe.py --cross 30 --engine shipped` — the arm
  that runs the shipped file — reports **30/30 sweeps finished** against the measured **27/30**, and
  **0/22 frames drifting · 0.0 % pairwise**, which must not regress from inc20's result.
- [x] **AC-3 · inc22 · the wedge has a regression test, and the test has teeth.** A test reaches the
  wedged state deterministically — the race needs a fresh interpreter and lands one sweep in ten, but
  the STATE it leaves behind needs no race — and asserts the repair. A second assertion proves the
  fixture still reproduces the defect, so the first cannot pass vacuously. Red-then-green is pasted
  from a real run against the pre-change file, not narrated.
- [x] **AC-4 · only the frames the fix MOVES are re-baked, and each is named.** If a committed frame
  carries a stale bake it moves, and the packet says which cells and why. If none moves, that is the
  result and the 22 frames are left alone — `prototypes/gallery/` is not opened for write.
  No `--surface` sweep is issued by this batch (F-8 stays as it is).

---

## 4. Validation strategy

`python -X utf8 -m pytest -q` in this worktree is the gate, run **after the increment**. Baseline
measured at Phase A, before any edit: **`1 failed, 685 passed, 2 skipped, 4 warnings`** — 686, whose one
failure is the documented environment-dependent `tests/test_app.py::test_win_clipboard_roundtrip`
(PENDING #22, `RUN.md`), which passes or fails with the state of the Windows clipboard.

`python -X utf8 prototypes/race_probe.py --cross 30 --engine shipped` is the gate for AC-2, run BEFORE
the edit for the rate and AFTER it for the verdict, from the one tool, so the two numbers are
comparable. ~6.5 minutes each.

`python prototypes/capture_languages.py` (the full documented command, with its own cross-process
determinism check) is what re-bakes for AC-4 — **and only if a frame moves.** Whether one does is
decided by hashing the 22 frames the 30-sweep arm produces against the committed
`prototypes/gallery/*.txt`, which is a stricter question than one more sweep can answer.

Headless stdout goes **to a file, never to `DEVNULL`** (L-42). No terminal process is ever killed.
`prototypes/verify_language.py` is **not** run: F-17 (`inc21.md` §4g) has it overwriting
`prototypes/out/_fixture_late.json`, which would invalidate the frames this batch is measuring against.
Git: the increment is committed in this worktree and pushed at the close — the operator has been
pushing this worktree.

---

## 5. Non-goals (what is OUT)

- **`capture_languages.py`'s settle.** It is right. Failing loud on a wedged app is the behaviour inc20
  bought; this batch removes the wedge, not the alarm.
- **F-17** (`verify_language.py` rewriting the capture's fixture), **F-14**, **F-15**, **F-8**.
  Untouched — and F-17 is the reason the language harness is not run here.
- **A framework fix.** The missing `Resize` is Textual's map-diff behaviour. This batch makes the widget
  not depend on it: no Textual patch, no version bump, no new dependency.
- **`prototypes/components/`, the skill's prose, and any consumer repo.** Untouched. If the fix moves a
  frame the skill carries, `export_to_skill.py` is run and its output reported — the skill is never
  hand-edited (`kits-learn-3` §5, unchanged).

---

## 6. Detected security flags

None fires. The change is one widget's paint path: no path is read, no file is written, no network, no
new dependency, no destructive command, no secret. `freeze_clock()`'s repointing of
`default_board_path` at the synthetic fixture is untouched, so no capture can print the operator's real
board; `tests/test_no_live_board.py` and `tests/test_privacy_sweep.py` are the standing guards and are
part of the suite gate above.

---

## 7. Batch status

| | |
| --- | --- |
| Phase A (spec) | **done** — this file; predecessor archived verbatim |
| Phase B (implement) | inc22 · the card composes at its seat · AC-1 … AC-4 — **done** |
| Phase C (close) | §8 — **done** |
| Notes | **<= 5 files, one agent.** 2 source files (`prototypes/widget_slice/kanban.py`, `tests/test_card_seat.py`) plus this spec and the archived predecessor: 4. |

---

## 8. Close (filled in phase C)

### What changed

`TaskCard` repaired its paint from EVENTS — `on_mount`, its deferred `call_after_refresh`, and
`on_resize` — and Textual guarantees the re-render but not the event. `Screen._refresh_layout` calls
`_size_updated` on every widget in the compositor's layers, which sets `_size` and dirties the widget,
but posts `Resize` only for `shown | resized` — both derived from a DIFF of the new compositor map
against the previous one. A lazy `Compositor.full_map` rebuild, which a freshly mounted widget causes,
writes the new geometry into that map first; the diff then sees nothing, no `Resize` is posted, and
`on_resize` never fires. The card now composes in `render()`, the one hook the dirtying guarantees.
20 lines in one file.

### How it was tested

- `python -X utf8 prototypes/race_probe.py --cross 30 --engine shipped`, before and after:
  **27/30 → 30/30 sweeps finished**; 0/22 frames drifting and 0.0 % pairwise in both.
- `tests/test_card_seat.py`: **1 failed / 1 passed** against the pre-change file, **2 passed** after.
- `python -X utf8 -m pytest -q`: **688 passed, 2 skipped, 4 warnings in 34.88 s** — 686 + 2 new.
- The 22 frames the 30-sweep arm produced hash **identical to the committed
  `prototypes/gallery/*.txt`**, before AND after the fix, so nothing was re-baked and
  `prototypes/gallery/` was never opened for write.

### Evidence per AC

| AC | verdict | evidence |
| --- | --- | --- |
| AC-1 · the wedge is diagnosed | **met** | `inc22.md` §2 — the state dump and the per-card timeline |
| AC-2 · the rate moves to zero | **met** | `inc22.md` §4a — 30/30 against 27/30; 0/22 and 0.0 % held |
| AC-3 · regression test with teeth | **met** | `inc22.md` §4b — red-then-green, plus the anti-vacuous guard that passes both ways |
| AC-4 · only movers re-baked | **met** | `inc22.md` §4c — 22 of 22 hashes match HEAD's frames; nothing re-baked, nothing exported |

### Open risks / pending

See `inc22.md` §5 and §6. F-8, F-14, F-15 and F-17 are untouched and still open; the fix's own risks —
a repair that runs inside `render()`, and a hazard that is now silent instead of loud — are named there.
