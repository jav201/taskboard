# Quick Spec — taskboard · batch "push-paint" (F-16's class, asked of the other widgets)

**Batch:** `2026-09-05-fastflow-13` · **Base:** worktree `kanban-variants`, HEAD `4f05649` (inc22, the
card that composes at the seat it is drawn at), pushed. Predecessor `wedge` closed 2026-09-05, §8 filled,
archived verbatim to `archive/spec-20260905-wedge-closed.md`. Language: English.
Increments continue the worktree's single sequence: **inc20 · inc21 · inc22 … inc23**.

**Input:** `.fast-dev-flow/03-increments/inc22.md` §5 and §6, named as the next task in §7:

> "A hazard that was loud is now silent. … the same class of defect in any OTHER widget — the hero, the
> column heads, the tiles — still depends on `on_resize` and would go unnoticed in exactly the same way.
> Only `TaskCard` is fixed here, because only `TaskCard` had the measurement."

The input in three lines:

1. **F-16 is a hole in an EVENT, not in a widget.** `Screen._refresh_layout` sets a widget's `_size` and
   dirties it, but posts `Resize` only for the ones the compositor's map DIFF calls new or resized, and a
   lazy `Compositor.full_map` rebuild can absorb the new geometry into that map first (`inc22.md` §2c).
2. **`TaskCard` is repaired; four push-painted surfaces are not.** `Hero`, `Tile`, `.col-head` and
   `.kb-empty` each compose content for a width and each depend on something else's `on_resize`.
3. **Nobody has measured which of them can actually go stale**, and the answer decides whether this is
   one 10-line repair, four, or none.

---

## 1. Objective (1 line)

Ask F-16's question of `Hero`, `Tile`, `.col-head` and `.kb-empty` with recorders rather than reasoning,
and repair the ones that answer yes — without moving a frame that is already right.

---

## 2. User stories

- As **the next person to touch a board surface**, I want to know which push-painted widgets are exposed
  to a missing `Resize` and which are not, so that "it has an `on_resize`" stops being read as "it is
  safe".
- As **anyone resizing the terminal**, I want the column heads to carry the measure the column actually
  has, because a head composed for a board 24 cells wider draws its rule past the edge of its column.
- As **anyone rebuilding the gallery**, I want the class of defect that stopped the sweep closed at the
  level where it lives, not one widget at a time.

---

## 3. Acceptance criteria (observable)

- [x] **AC-1 · inc23 · every one of the four is ASKED, and the answers are measured.** The packet carries
  a four-row table — widget · composes for a width? · is `on_resize` its only repair? · stale when deaf? —
  each cell backed by a run, not by reading the source. The deaf reproduction is the mechanism
  `tests/test_card_seat.py::deafen` uses: replace the handler its repair hangs on with a recorder, move
  the seat with no event reaching it, ask the rebuild oracle.
- [x] **AC-2 · inc23 · every widget that goes stale gets the same painted-width repair**, a guard in
  `render()` with the counter stamped in `render()` and nowhere else (`inc22.md` §1), each with a
  regression test in the `test_card_seat.py` pattern: red against the pre-fix class quoted in the test,
  green after, pasted from a real run.
- [x] **AC-3 · inc23 · the gate does not move.** `race_probe.py --cross 30 --engine shipped` reports
  **30/30 sweeps finished · 0/22 frames drifting · 0.0 % pairwise**, and sweep time is unchanged.
- [x] **AC-4 · only the frames the fix MOVES are re-baked, and each is named.** Decided by hashing the 22
  frames the 30-sweep arm produces against the committed `prototypes/gallery/*.txt`. If none moves,
  `prototypes/gallery/` is not opened for write and `export_to_skill.py` is not run. No `--surface` sweep
  (F-8 stays as it is).

---

## 4. Validation strategy

`python -X utf8 -m pytest -q` in this worktree is the gate, run after the increment. Baseline at Phase A:
**688 passed, 2 skipped** (`inc22.md` §4d).

`python -X utf8 prototypes/race_probe.py --cross 30 --engine shipped` is the gate for AC-3. ~6.5 minutes.

The diagnosis instruments are throwaway probes in the gitignored scratch yard, built on `_f16_probe.py`'s
widget-agnostic recorders as `inc22.md` §7 said they could be.

Headless stdout goes **to a file, never to `DEVNULL`** (L-42). No terminal process is ever killed.
`prototypes/verify_language.py` is **not** run: F-17 has it overwriting `prototypes/out/_fixture_late.json`,
which would invalidate the frames this batch measures against. Git: committed in this worktree and pushed
at the close — the operator has been pushing this worktree.

---

## 5. Non-goals (what is OUT)

- **A framework fix.** The missing `Resize` is Textual's map-diff behaviour; this batch makes the widgets
  not depend on it. No Textual patch, no version bump, no new dependency.
- **F-17, F-14, F-15, F-8.** Untouched — and F-17 is the reason the language harness is not run here.
- **`capture_languages.py`'s settle.** Unchanged; it is the alarm, not the defect.
- **`prototypes/components/`, the skill's prose, and any consumer repo.** Untouched. If the fix moves a
  frame the skill carries, `export_to_skill.py` is run and its output reported — the skill is never
  hand-edited.

---

## 6. Detected security flags

None fires. The change is one container's paint path: no path is read, no file is written, no network, no
new dependency, no destructive command, no secret. `freeze_clock()`'s repointing of `default_board_path`
at the synthetic fixture is untouched; `tests/test_no_live_board.py` and `tests/test_privacy_sweep.py` are
the standing guards and are part of the suite gate above.

---

## 7. Batch status

| | |
| --- | --- |
| Phase A (spec) | **done** — this file; predecessor archived verbatim |
| Phase B (implement) | inc23 · the board builds at the seat it is drawn at · AC-1 … AC-4 — **done** |
| Phase C (close) | §8 — **done** |
| Notes | **<= 5 files, one agent.** 2 source files (`prototypes/widget_slice/kanban.py`, `tests/test_board_seat.py`) plus this spec, the archived predecessor and the packet: 5. |

---

## 8. Close (filled in phase C)

### What changed

Two of the four answered no, and not the two the risk note would have guessed.

`Hero` and `Tile` are repainted by `TaskboardWidget.redraw()`, which the 12 Hz `tick_fast` calls on every
frame. Moved with **no resize handler running at all**, both come right within one tick. Their repair does
not hang on an event and there was nothing to fix.

`.col-head` IS composed for a width and `KanbanBoard.on_resize` then `build()` is its only repair: over
the 48 board widths the app can reach it takes **39 / 48 / 25 distinct paints** in the columns / sections /
split branches. `.kb-empty` is composed for a width too, but `k.empty(w)` has a single threshold (the
mascot, at `w >= 14`) and every width the board can hand it sits on one side of that threshold: **one
distinct paint over all 48 widths, in all three layouts.** It cannot go stale.

So one repair, and it is on `KanbanBoard` rather than on the head — because `.col-head` is composed for a
width derived from the BOARD's seat, not its own. Measured, columns branch: shrinking the board 24 cells
leaves the heads' own seats at 56/32/21, exactly where `build()` pinned them, and their `render()` is
never called. A guard on the head would be blind there; the board's `render()` sees every one of those
changes, and its rebuild repairs all three board surfaces at once. 24 lines in one file.

### How it was tested

- `prototypes/out/_inc23_deaf.py`, the deterministic reproduction, before and after: `col-head`
  **STALE=True to False** in all three layouts; `Hero`, `Tile`, `kb-empty` False in both arms.
- `prototypes/out/_inc23_range.py`: the distinct-paint counts above, over 48 board widths.
- `tests/test_board_seat.py`: **2 failed / 2 passed** against the pre-change file, **4 passed** after.
- `python -X utf8 -m pytest -q`: **692 passed, 2 skipped, 4 warnings** — 688 + 4 new.
- `python -X utf8 prototypes/race_probe.py --cross 30 --engine shipped`: **30/30 sweeps finished,
  0/22 frames drifting, 0.0 % pairwise**, sweep time unmoved.
- The 22 frames the 30-sweep arm produced hash **identical to the committed `prototypes/gallery/*.txt`**,
  so nothing was re-baked and `prototypes/gallery/` was never opened for write.

### Evidence per AC

| AC | verdict | evidence |
| --- | --- | --- |
| AC-1 · all four asked, answers measured | **met** | `inc23.md` §2 — the four-row table and the three probes behind it |
| AC-2 · the stale one repaired, with a test | **met** | `inc23.md` §3 and §4b — the guard, red-then-green, plus the anti-vacuous guard that passes both ways |
| AC-3 · the gate does not move | **met** | `inc23.md` §4a — 30/30, 0/22, 0.0 %, sweep time unchanged |
| AC-4 · only movers re-baked | **met** | `inc23.md` §4c — 22 of 22 hashes match HEAD's frames; nothing re-baked, nothing exported |

### Open risks / pending

See `inc23.md` §5 and §6. F-8, F-14, F-15 and F-17 are untouched and still open. The fix's own risks — a
rebuild that runs from a render path, and `Hero`/`Tile` resting on a ticker rather than on a guarantee —
are named there.
