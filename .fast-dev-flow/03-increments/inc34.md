# Increment 34 — F-18: the test's observation point, measured against the screen's

**Batch:** `observe-once` · `inc26.md` §5/§8 (F-18), named there as the next task
**Files:** `tests/test_board_seat.py` — **1 source file**.

**F-18 reproduced at 4 reds in 60 isolated runs and it is NOT a defect in `build()`. The DOM does hold
two generations of `.col-head` for one beat — six heads where the board has three, 2 of 30 runs — and the
COMPOSITOR never draws more than three, 0 of 30. A user cannot see six heads. The repair is where the test
LOOKS, and it now waits for the condition it means instead of for one `pilot.pause()`. Isolated: 4/60 red
→ 0/60. The screen's half of the finding is a new test, not a sentence.**

---

## 1. Reproduction, with counts

`prototypes/out/_f18_loop.sh` — one pytest process per run, the tail summary line and rc recorded, every
red's full stdout kept in a `.red` sidecar. Headless stdout to a file, never `DEVNULL` (L-42).

### Before (at `c3e1760`, this batch's base)

```
tests/test_board_seat.py, isolated, 60 runs  ->  4 red   (runs 5, 13, 18, 43)
full suite, 10 runs                          ->  0 red   (10 x "878 passed, 2 skipped")
```

**All four are the same test, the same line and the same shape** inc26 §5 named —
`test_the_next_paint_builds_at_the_new_seat_columns`, `tests/test_board_seat.py:205`, with `got` holding
six head rows where the board has three (colour stripped here; the `.red` sidecars carry them verbatim):

```
E  AssertionError: a rebuild at the same seat composes something else:
   ['▐▌ [1]TODO                 [ 3]',      <- the WIDE measure
    '▐▌ [2]DOING                [ 3]',
    '▐▌ [3]DONE                 [ 3]',
    '▐▌ [1]TODO   [ 3]',                    <- the NARROW measure
    '▐▌ [2]DOING  [ 3]',
    '▐▌ [3]DONE   [ 3]']
```

The sections branch never went red in 60 runs; the columns branch went red four times. Both are repaired,
because both sample the same way.

**6.7 % isolated, 0 % in ten full suites.** inc26 measured 1 in 40 isolated and 1 in 27 full-suite; the
isolated rate is higher on this machine and the full-suite rate is lower, which is what a race that
depends on scheduler pressure does. It reproduces in isolation, so it is timing and not order.

---

## 2. WHEN the old generation is gone — the probe

`prototypes/out/_f18_lifetime.py`, 30 runs (15 per branch), reads **two** numbers after every one of the
first twelve pauses following the resize:

- **tree** — `len(board.query(".col-head"))`, which is what the test reads
- **drawn** — how many of those the **compositor** says it is drawing with a clip that has area, from
  `app.screen._compositor.visible_widgets`. The same instrument, and for the same stated reason, that
  `capture_languages._not_at_rest` uses: a widget's own `region` is in screen space and keeps growing
  past the fold, so a raw slice reads whatever is at those coordinates.

```
industrial cols=3 built_w=70 tree/drawn per pause: 3/3 3/3 3/3 3/3 ...
industrial cols=3 built_w=70 tree/drawn per pause: 6/0 3/3 3/3 3/3 ...   <- BOTH generations in the tree
industrial cols=3 built_w=70 tree/drawn per pause: 3/0 3/3 3/3 3/3 ...   <- one generation, NOTHING drawn
ledger     cols=3 built_w=70 tree/drawn per pause: 3/0 3/3 3/3 3/3 ...
...
runs                                  30
pause 1: TREE holds > one generation   2
pause 1: COMPOSITOR draws > one gen    0
```

**Three facts, and they decide the seam:**

1. **The tree doubles.** 2 of 30 runs read six heads at the first pause. That is F-18's mechanism,
   confirmed at the level of counts rather than inferred from a failure message.
2. **The screen never does.** 0 of 30. When the tree held six, the compositor was drawing **zero** —
   the new generation is mounted but not yet laid out, and the old one is already out of the map.
3. **One pause after a resize is not a settled frame at all.** In **8 of 30** runs the compositor was
   drawing no column head whatever at the first pause (`3/0` and `6/0` rows). By the **second** pause
   every run of both branches reads `3/3`, and stays there for the remaining ten.

### Why `build()` cannot await the removal, and why it does not need to

`KanbanBoard.build()` calls `remove_children()` — asynchronous, and this repo already paid for that
knowledge: the `_detail` reference in `__init__` exists **because** "for a beat the board holds the
previous build's `#kb-detail` too", measured at 4–7 permanent blanks in 30 runs. It then mounts the new
generation without awaiting the removal, and **it cannot await it**: `build()`'s other caller is
`render()` (inc23's F-16 repair), which is synchronous. Making the removal awaited would mean making
`build()` a coroutine and taking the seat repair back out of `render()` — undoing the previous batch's
acceptance criterion to fix a window the compositor demonstrably never shows.

`pilot.pause()` does **not** drain the removal reliably: one pause leaves it pending in 2 of 30 runs.
Two pauses drained it in 30 of 30 — but a count of pauses is a guess about a scheduler, which is exactly
what this increment is replacing.

---

## 3. What changed

**`settled_heads(app, pilot, board, what, also=None)`** — one helper, and every place the file samples the
widget tree goes through it. It returns the head row only when

- the tree holds exactly `NHEADS` heads (`len(StubBoard.phases)`, named rather than typed as `3`), **and**
- it read the *same* row on the previous pass — which is what rules out sampling the OLD three before the
  new three have landed, the failure mode a bare count cannot see, **and**
- the caller's own predicate holds (`_built_w == NARROW` at the one site that means it).

It is bounded at `SETTLE_FRAMES = 60` and **raises** on the bound, naming the condition and the last read.
A settle that gives up silently would hand back the bad sample it exists to prevent. Sixty is two orders
of margin over the only number anyone measured (§2: every run settled on pause 2).

`narrow()` keeps its single pause — delivering the resize is all it does; **waiting for what the resize
causes is now a separate act with a name.**

The four sample points, all of them exposed to the same window and all of them now settled:

| where | was | is |
| --- | --- | --- |
| `start()` — the first explicit build | `await pilot.pause()` | `settled_heads(...)` |
| `_stale_when_deaf` — the oracle rebuild | `pause` then `heads(board) != wide` | `after = settled_heads(...)` |
| `_repaired_at_next_paint` — **the F-18 site** | `narrow()` then `got = heads(board)` | `got = settled_heads(..., also=lambda: board._built_w == NARROW)` |
| `_repaired_at_next_paint` — the oracle rebuild | `pause` then `heads(board) == got` | `again = settled_heads(...)` |

Only the third has ever been seen red. The other three are the same exposure and were left standing in
inc23; two of them could only fail *vacuously* (a `!=` that passes because it read six rows instead of
three), which is worse than a red.

### 3a. The predicate is passed, not asserted after

`board._built_w == NARROW` was already asserted three lines below the sample. It is now *also* the
condition the wait is on, so a board that rebuilds at the wrong seat times out **naming the seat** instead
of failing on a head row that is merely a symptom of it. The assertion below is kept: it is the one that
says what went wrong when the board never rebuilds at all.

### 3b. And the screen's half is a test

**`test_the_screen_never_shows_two_generations_of_heads_{columns,sections}`** — the finding that decided
the seam, asserted rather than trusted. It walks **every** frame of the resize (not the one frame the
probe sampled) and requires `drawn <= NHEADS` on all of them, printing the whole per-frame trace on
failure. If `build()` ever does put two generations on screen, this is the test that says so and the
repair moves into `kanban.py`.

**The tree count is recorded beside it and deliberately NOT asserted.** An assertion that the DOM never
doubles would be a claim about Textual's removal scheduling — which this repo does not own, and which the
fixture the same file relies on would have to fight.

---

## 4. The fixture still has teeth

A settle can hide the defect it was written beside, so it was planted against. `render()`'s seat guard —
inc23's entire F-16 repair — was removed from `prototypes/widget_slice/kanban.py` and the file re-run:

```
E  AssertionError: the board never settled in 60 frames: a rebuild at the new seat (70);
   last read 3 heads where the board mounts 3: ['[#1c1a15] 1 TODO ····…[/] [#6b6558]3 entries[/]…']

FAILED tests/test_board_seat.py::test_the_next_paint_builds_at_the_new_seat_columns
FAILED tests/test_board_seat.py::test_the_next_paint_builds_at_the_new_seat_sections
2 failed, 4 passed in 5.42s
```

**Read the message, because it is the argument for the change.** The regression is caught, it is caught by
the *acceptance* pair and not by the new screen test, and the failure now says *the board never rebuilt at
the new seat* — the defect — where before it said *a rebuild composes something else*, which is a
symptom. `kanban.py` was restored from a copy taken immediately before the plant
(`prototypes/out/_f18_kanban_backup.py`) and `git status --short` shows one modified file, the test.

---

## 5. Test results — the counts, after

```
tests/test_board_seat.py, isolated, 60 runs  ->  60 x "6 passed"        0 red
full suite, 10 runs                          ->  8 x "880 passed, 2 skipped"
                                                 2 x "1 failed, 879 passed"
                                                     -> tests/test_app.py::test_win_clipboard_roundtrip
                                                        BOTH times, and nothing else
```

| | before | after |
| --- | --- | --- |
| `test_board_seat.py` isolated, 60 runs | **4 red** | **0 red** |
| full suite, 10 runs — `board_seat` red | 0 | **0** |
| full suite, 10 runs — other red | 0 | 2, both `test_win_clipboard_roundtrip` |
| suite total | 878 passed, 2 skipped | **880 passed, 2 skipped** (+2, §3b) |

**The two full-suite reds are the documented environment-dependent clipboard test** (PENDING #22,
`RUN.md`: "fails if the clipboard is busy") — the same test inc26 §5 discounted for the same reason. It is
named rather than filtered out, and it is not this increment's.

**0 of 60 is not proof of absence at a 6.7 % rate — it is one-sided evidence, and §7 says so with a
number.**

---

## 6. Risks

- **0 red in 60 runs bounds the rate, it does not zero it.** At the before-rate of 4/60, the chance of
  seeing zero in 60 runs by luck is about `(1 - 4/60)^60 ≈ 1.6 %`. That is the honest strength of the
  claim: the race is gone or it is at least ~60× rarer, and this packet cannot tell those apart.
- **The stability read costs a pause the old code did not spend.** `settled_heads` requires two identical
  reads, so a settled board still pays one extra `pilot.pause()` per sample. Measured: the file runs at
  1.65–1.75 s against ~0.95 s before — but on 6 tests instead of 4, so the per-test cost is not separated
  out here. Full-suite median moved 33.9 s → 33.1 s, i.e. inside the run-to-run spread and in the wrong
  direction to be this change; the honest statement is that the cost is not visible at suite scale.
- **`NHEADS` is `len(StubBoard.phases)` and both branches this file drives mount one head per phase.**
  The split branch does not, and if this file ever drives a split kit the constant becomes wrong. It is
  derived from the fixture rather than typed, which is as far as a constant can protect itself.
- **The bound is a bound, not a proof.** 60 frames is ~30× the settle anyone measured, but a machine
  slow enough to exceed it turns a flaky red into a *deterministic* red with a clear message. That is the
  intended direction, and it is still a red.
- **The screen test asserts `<=`, so it cannot catch a generation that is drawn where the old one was.**
  It counts heads the compositor draws; two generations occupying the same three seats would read as
  three. The seat assertions in the acceptance pair are what cover that, and they were already there.
- **The double-generation DOM window is unfixed and stays unfixed by choice.** §2 argues it is
  unreachable from the screen and that fixing it would undo inc23. If that argument is wrong, §3b's test
  is where it will show up.

## 7. Pending

- **F-18 is closed at the test's seam.** The `build()` window it exposed is recorded as measured
  behaviour, not as a defect, with the test that would reopen it.
- **`test_win_clipboard_roundtrip`** — PENDING #22, unchanged, 2 of 10 this increment.
- **F-8** — `--surface` plain and alone. Run at the batch close, not here.
- **`RUN.md` is still stale on "flake-free since the forty-sixth pass"** (inc26 §8 named it; F-18 was the
  live counter-example and is now closed, which makes the line *more* wrong, not less — the suite has
  a documented environment-dependent red in it).

## 8. Suggested next task

`inheritors-2` — `required` and `pane_split` for the six inheriting languages (spec §5's declared debt).

---

## Evidence checklist

- [x] **Tests/type checks/lint pass** — `tests/test_board_seat.py`: `6 passed` (§4). Full suite:
      `880 passed, 2 skipped` in 8 of 10 runs; the other two are the named, documented clipboard test and
      nothing else (§5). The fixture is red-then-green against a planted removal of inc23's repair (§4).
- [x] **No secrets in code or output** — one test file. No path outside the worktree, no network, no new
      dependency, no I/O the file did not already do.
- [x] **No destructive commands run without approval** — no `rm` outside the gitignored scratch yard, no
      force, no terminal process killed. The planted regression was written to
      `prototypes/widget_slice/kanban.py` and restored from a copy taken immediately before
      (`prototypes/out/_f18_kanban_backup.py`), verified by `git status --short` showing the test file
      alone and by re-running the file green.
- [x] **File count within cap** — 1 source file, plus this packet: 2.
- [x] **Review packet attached** — this document.
