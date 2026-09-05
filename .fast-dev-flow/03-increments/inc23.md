# Increment 23 — the board builds at the seat it is drawn at (F-16's class, asked of the other four)

**Batch:** `push-paint` · **AC-1, AC-2, AC-3, AC-4** · inc22 §5's open risk, named as its next task
(`inc22.md` §6/§7)
**Files:** `prototypes/widget_slice/kanban.py`, `tests/test_board_seat.py` (new) — **2 source files**;
plus `.fast-dev-flow/spec.md` (new batch spec), `.fast-dev-flow/archive/spec-20260905-wedge-closed.md`
(predecessor, archived verbatim) and this packet.

**Two of the four go stale, and they are not the two the risk note named. `Hero` and `Tile` are repainted
by a 12 Hz ticker and come right on their own; `.kb-empty` takes ONE distinct paint over every width the
board can reach. `.col-head` takes 39. It is repaired at the BOARD, because a guard on the head could not
see the change — measured. The fix is 24 lines and it moves no committed frame.**

---

## 1. What changed

`inc22.md` §5 left this open:

> "the same class of defect in any OTHER widget — the hero, the column heads, the tiles — still depends
> on `on_resize` and would go unnoticed in exactly the same way."

Asked with recorders, the four do not answer alike. **`KanbanBoard` now checks its seat in `render()`:**

```python
    def render(self):
        if self._painted_w != self.size.width:
            self._painted_w = self.size.width
            self._rebuild_if_seat_moved()
        return super().render()
```

`on_resize`'s two-line predicate moved into `_rebuild_if_seat_moved()` so both callers share one copy —
that extraction is the whole reason `on_resize` is touched at all. **`_painted_w` is written in
`render()` and nowhere else**, for inc22 §1's reason: a counter stamped inside the paint routine would
let a shadow paint mark a stale widget fresh. `build()` keeps its own `_built_w`, which is what it built
for, and the two are not the same fact.

---

## 2. AC-1 — the four-row table, and how each cell was measured

| widget | composes content for a width? | is `on_resize` its only repair? | stale when deaf? |
| --- | --- | --- | --- |
| `Hero` | **yes** — `HERO.draw(..., width=min(caller_w, self.size.width), max_rows=self.size.height)` (`app.py:170-180`) | **no** — it has no `on_resize`; `TaskboardWidget.redraw()` paints it, and `tick_fast` calls `redraw()` at 12 Hz | **no** |
| `Tile` | **yes** — `w = max(8, (self.size.width or 24) - 2)`, and the KPI gauge only at `w >= 40` (`app.py:216-233`) | **no** — same `redraw()`, same ticker | **no** |
| `.col-head` | **yes** — `k.head(name, count, rw, idx)`; **39 / 48 / 25 distinct paints** over the 48 board widths the app can reach (columns / sections / split) | **yes** — `KanbanBoard.on_resize` → `build()` and nothing else | **YES** |
| `.kb-empty` | **in form yes** — `k.empty(rw)` — but `empty()` has ONE threshold (the mascot, `w >= 14`) and **1 distinct paint** over all 48 widths, in all three layouts | **yes** — same `on_resize` | **no** |

### 2a. The instruments

Three throwaway probes in the gitignored scratch yard, built on `_f16_probe.py`'s widget-agnostic
recorders exactly as `inc22.md` §7 said they could be. Each records and calls the original.

- **`_inc23_probe.py --mode survey`** — the shipped sweep with `Widget._size_updated` and
  `MessagePump.post_message(Resize)` pointed at all four **plus `KanbanBoard`**, which is the thing whose
  event the two Statics' repair actually hangs on, and with paint recorders on `Hero.show`,
  `Tile.refresh_tile`, `KanbanBoard.build` and `row_width` (the last stamps each `.col-head`/`.kb-empty`
  with the measure it was built for, since both are composed BEFORE they are mounted and their own seat
  at paint time is 0 and says nothing).
- **`_inc23_deaf.py`** — the deterministic reproduction, one widget at a time.
- **`_inc23_range.py`** — the distinct-paint count over every board width the app can reach.

### 2b. What the in-process survey establishes, and what it cannot

```
--- board industrial (layout=columns)
    Hero         n=1   seat_changes=2   Resize_posts=2   SILENT=0   paints=8    stale_now=0
    Tile         n=6   seat_changes=12  Resize_posts=12  SILENT=0   paints=48   stale_now=0
    col-head     n=3   seat_changes=4   Resize_posts=4   SILENT=0   paints=3    rw=[53, 28, 17] seats=[56, 32, 21]
    kb-empty     (none on this board)
    KanbanBoard  n=1   seat_changes=2   Resize_posts=2   SILENT=0   paints=4    _built_w=116 seat=116
```

`SILENT=0` everywhere, and that is **not** evidence of safety: inc22 §2a measured that 15 sweeps in ONE
interpreter produce no wedge at all, and every in-process arm of race-probe is 0/30. The survey's job is
the other two facts, and it delivers them: **`.col-head` is painted exactly 3 times — once per column, at
`build()` — and never again**, and the measure it was built for (`rw=[53, 28, 17]`) is not its own seat
(`[56, 32, 21]`), which is the fact that decides where the guard has to go. It also records that **the capture fixture has no empty
phase**, so `.kb-empty` never occurs on the shipped sweep and had to be reached another way.

### 2c. The deaf reproduction — the same mechanism `test_card_seat.py::deafen` uses

Settle the real app, replace the handler the widget's repair hangs on with a **recorder**, move the seat,
and ask the rebuild oracle — `board.build()`, i.e. what the present seat composes — whether what is drawn
is what the seat wants. `taskboard.views.phase_buckets` is shimmed to empty the DONE bucket so
`.kb-empty` exists at all; the board's own code path is untouched.

**BEFORE** (`_inc23_deaf_before.txt`):

```
lang        layout    widget    seat move                    deaf_ev  unrepainted  STALE
industrial  -         Hero      114->90                      0        False        False
industrial  -         Tile      17->13                       0        False        False
industrial  columns   col-head  [56, 32, 21]->[56, 32, 21]   1        True         True
industrial  columns   kb-empty  [11]->[11]                   1        True         False
ledger      -         Hero      114->90                      0        True         False
ledger      -         Tile      17->13                       0        False        False
ledger      sections  col-head  [112, 112, 112]->[92, 92, 92] 1        True         True
ledger      sections  kb-empty  [112]->[92]                  1        True         False
nord        -         Hero      112->88                      0        False        False
nord        -         Tile      17->13                       0        True         False
nord        split     col-head  [31, 31, 31]->[31, 31, 31]   1        True         True
nord        split     kb-empty  [31]->[31]                   1        True         False
```

**AFTER** (`_inc23_deaf_after.txt`) — only the three `col-head` rows move, and they move the whole way:

```
industrial  columns   col-head  [56, 32, 21]->[43, 26, 18]   1        False        False
ledger      sections  col-head  [112, 112, 112]->[92, 92, 92] 1        False        False
nord        split     col-head  [31, 31, 31]->[25, 25, 25]   1        False        False
```

`deaf_ev=1` on every board row is the anti-vacuous guard: the resize really arrived at the deafened
handler and really repaired nothing, so the repair after the fix cannot have come from the event.

**`Hero` and `Tile` show `deaf_ev=0`, and that is the finding, not a fixture failure.** Their seat is
moved by shrinking `#ap`, which resizes them without resizing the terminal — so **no resize handler
anywhere runs**, and they still come right. `ledger`'s hero and `nord`'s tile are the demonstrative rows:
`unrepainted=True` immediately after the move, `STALE=False` four ticks later. The repair is
`tick_fast` → `redraw()` at 12 Hz, not an event. A missed `Resize` costs them one frame.

### 2d. Why `.kb-empty` is not repaired, said as a measurement

`k.empty(w)` branches once, on the mascot's `w >= 14`. Over every board width the app can reach:

```
industrial  columns   widths=48 col-head distinct=39  kb-empty distinct=1  kb-empty seats=[6..11]
ledger      sections  widths=48 col-head distinct=48  kb-empty distinct=1  kb-empty seats=[22..117]
nord        split     widths=48 col-head distinct=25  kb-empty distinct=1  kb-empty seats=[25..61]
```

(`_inc23_range.txt` prints every seat it saw; the ranges above are those lists abbreviated to their ends.
The `distinct` counts are verbatim.)

An empty phase in the COLUMNS branch is pinned at `weighted_widths`' floor of 13 (its count is 0, so
nothing else can move it), which puts its measure at 8 for every board width; in SECTIONS and SPLIT the
row is full-width and never falls below 16, because `build()`'s own guard refuses a board narrower than
21. **There is no width on either side of the threshold that the same layout can also produce**, so the
paint cannot change and cannot be stale. The board's rebuild recomposes it anyway; it is simply not the
reason for the rebuild.

### 2e. Why the guard is on the BOARD and not on the head

`.col-head` is composed for `row_width(column seat)` — a number derived from the **board's** seat. Its own
seat is a different number, and in the columns branch it does not move at all, because `build()` pins each
column with `col.styles.width = cw`. Measured directly (`_inc23_rcheck.py`, before the fix):

```
industrial  layout=columns   board.render calls=1 head.render calls=0 deaf_events=1 board seat=94 _built_w=116 head seats [56, 32, 21] -> [56, 32, 21]
ledger      layout=sections  board.render calls=1 head.render calls=6 deaf_events=1 board seat=94 _built_w=114 head seats [112, 112, 112] -> [92, 92, 92]
```

**A painted-width guard on the head would never fire in the columns branch: its seat does not change and
its `render()` is not called.** The board's `render()` IS called, in both branches, on the seat change the
deafened event dropped. After the fix, the same probe:

```
industrial  layout=columns   board.render calls=2 head.render calls=7  deaf_events=1 board seat=94 _built_w=94 head seats [56, 32, 21] -> [0, 0, 0]
ledger      layout=sections  board.render calls=2 head.render calls=11 deaf_events=1 board seat=94 _built_w=94 head seats [112, 112, 112] -> [0, 0, 0]
```

`_built_w` follows the seat with the event still going in the bin. The `-> [0, 0, 0]` is the probe holding
references to the PREVIOUS build's heads, which the rebuild removed; `_inc23_deaf.py` re-queries after the
move and reports the live ones (§2c).

---

## 3. Files modified

- `prototypes/widget_slice/kanban.py` — `KanbanBoard.__init__` gains `_painted_w`; new
  `KanbanBoard.render`; `on_resize`'s body extracted to `_rebuild_if_seat_moved()` so `render` and the
  event share one predicate. **24 insertions, 0 deletions** (`git diff --stat`).
- `tests/test_board_seat.py` — **new**, 4 tests (two branches × two arms).
- `.fast-dev-flow/spec.md` — the new batch spec (Phase A), predecessor archived verbatim to
  `.fast-dev-flow/archive/spec-20260905-wedge-closed.md`.
- Evidence in the gitignored scratch yard: `_inc23_probe.py`, `_inc23_deaf.py`, `_inc23_range.py`,
  `_inc23_rcheck.py`, and their logs `_inc23_survey1.txt`, `_inc23_deaf_before.txt`,
  `_inc23_deaf_after.txt`, `_inc23_range.txt`, `_inc23_rcheck_after.txt`, `_inc23_red.txt`,
  `_inc23_suite.txt`, `_race_inc23_after.txt`, plus `_kanban_inc23.py.bak` (the copy the red arm restored
  from).

---

## 4. How to test, and the results

```powershell
cd "C:\Users\jjgh8\Github\taskboard\.claude\worktrees\kanban-variants"
$env:PYTHONIOENCODING = "utf-8"

python -X utf8 -m pytest -q tests\test_board_seat.py
python -X utf8 -m pytest -q

python -X utf8 prototypes\out\_inc23_deaf.py  > prototypes\out\_inc23_deaf_after.txt 2>&1
python -X utf8 prototypes\out\_inc23_range.py > prototypes\out\_inc23_range.txt      2>&1

# THE GATE (~6 min): 30 whole sweeps in 30 fresh interpreters, all 22 frames diffed
python -X utf8 prototypes\race_probe.py --cross 30 --engine shipped --tag inc23_after `
    > prototypes\out\_race_inc23_after.txt 2>&1
```

Every headless run went to a **file**, never `DEVNULL` (L-42). No terminal process was killed. No
`--surface` was issued (F-8 untouched). `prototypes/verify_language.py` was **not** run (F-17 would
rewrite the fixture the frames are measured against). `prototypes/gallery/` was never opened for write.

### 4a. AC-3 — the gate, unmoved

```
  CROSS-PROCESS DRIFT: 0/22 frames over 30 sweeps -> []
  sweeps that are non-modal on >=1 frame: 0/30 []
  PAIRWISE DISAGREEMENT (what the shipped determinism check asks): 0/435 pairs = 0.0 %
```

`grep -c 'FAILED rc='` on the after log: **0**, so 30/30 sweeps finished — inc22's result held, which was
the point of running it: a change that broke the board would show up here as the wedge coming back.

| arm | sweeps finished | frames drifting | non-modal | pairwise | per-sweep |
| --- | --- | --- | --- | --- | --- |
| inc22 (HEAD `4f05649`) | 30 / 30 | 0 / 22 | 0 / 30 | 0.0 % (0/435) | 11.6-13.5 s |
| **inc23 (this change)** | **30 / 30** | 0 / 22 | 0 / 30 | 0.0 % (0/435) | **11.1-12.6 s** |

**Sweep time is unchanged.** The guard costs one integer comparison per board paint, and the rebuild
behind it is gated a second time by `_built_w`, so a seat change that does not cross `max(20, w)` costs
nothing at all.

### 4b. AC-2 — the tests, red then green, run against both files

`tests/test_board_seat.py`, four tests: `_stale_when_deaf` (the anti-vacuous arm) and
`_repaired_at_next_paint` (the fix), each run against **`industrial` (columns)** and **`ledger`
(sections)** — the branch where a board resize does NOT move the head's own seat, and the branch where it
does. Against **HEAD `4f05649`'s** `kanban.py` (installed with `git show HEAD:… > …`, restored from a copy
in the same command, verified by `git diff --stat`):

```
FAILED tests/test_board_seat.py::test_the_next_paint_builds_at_the_new_seat_columns
  AssertionError: the board is still built for 110, seat is 70
  assert 110 == 70
FAILED tests/test_board_seat.py::test_the_next_paint_builds_at_the_new_seat_sections
  AssertionError: the board is still built for 110, seat is 70
2 failed, 2 passed in 0.99s
```

Against the new file:

```
4 passed in 1.10s
```

**The two that pass in both are the point**, and it is inc20 §4c's and inc22 §4b's device.
`test_a_board_rebuilt_only_from_events_keeps_the_wide_build_*` drives `PreFixBoard` — `KanbanBoard` with
`render = Vertical.render`, the paint path as it stood at `4f05649`, quoted in the test rather than
reached for through git — and asserts it DOES hold the wide build. It then calls `build()` itself and
asserts the heads MOVE, so a kit whose head ignored its width could not satisfy it silently.

Three things had to be measured before the fixture could be written:

- **The board must be built explicitly at mount.** The real app does this (`app.py:start_widget` calls
  `kb.build()`); with `on_resize` deafened and no explicit build, `PreFixBoard` would never build at all
  and the test would compare two empty lists. `start()` in the test does what the app does, and says so.
- **The deafening goes on `KanbanBoard` itself, not on a subclass** — `test_card_seat.py` measured that
  Textual dispatches the handler of every class in the MRO, so a subclass override still runs the base's.
- **`on_resize` could not stay the fix's entry point.** A first draft had `render()` call `self.on_resize()`;
  that reads well until the test deafens `on_resize` and takes the fix with it. Hence
  `_rebuild_if_seat_moved()`: the event-side repair can be removed while the paint-side one stands, which
  is the only arrangement in which the test proves anything.

### 4c. AC-4 — which frames moved: none, and that is a measurement

The 22 frames the 30-sweep arm produced, hashed against the committed `prototypes/gallery/*.txt`:

```
after : 22 frames compared against prototypes/gallery/ -> 0 differ (22 identical, 0 missing)
```

Every hash also matches inc22's arm — `board_industrial.txt 0182fbd7cdb1` ×30, `board_darkside.txt
74d57555a62f` ×30, and so on for the other 20.

**Why nothing moved, said plainly:** the capture sweep runs at one fixed viewport (118×34) and never
resizes it, so the board builds once at the seat it keeps. The head was never composed for a width it did
not have IN THE CAPTURE; the exposure is a resize, and the capture does not resize. A re-bake would have
rewritten 44 files with identical bytes, so `prototypes/gallery/` was not opened and `export_to_skill.py`
was not run: **no frame the skill carries moved.** The corollary belongs in §5: the gate cannot see this
class of defect, and did not.

### 4d. Suite

```
python -X utf8 -m pytest -q
692 passed, 2 skipped, 4 warnings in 33.60s
```

**688 + 4 = 692**, the 688 baseline plus this increment's four tests. The baseline's
environment-dependent `tests/test_app.py::test_win_clipboard_roundtrip` (PENDING #22, `RUN.md`) is green
on this run, as it was on inc22's; it passes or fails with the state of the Windows clipboard and this
increment touches neither. Recorded, not claimed as an improvement.

---

## 5. Risks

- **The repair runs `build()` from a render path, and `build()` is much heavier than `render_card()`.**
  It calls `remove_children()` — asynchronous, the hazard the `_detail` reference comment in `__init__`
  already documents — and mounts a whole tree. It is bounded the same way inc22's is: `_painted_w` is
  stamped BEFORE the rebuild, and `_built_w` gates it a second time, so at most one rebuild per seat
  change and the next render finds nothing to do. Measured: 30/30 with the sweep time unmoved, suite
  green. It is still a heavier thing to do from `render()` than the card does, and the next person adding
  a third of these should know that.
- **The gate cannot see this class of defect** (§4c). `capture_languages.py` never resizes its viewport,
  so a stale `.col-head` could not have shown up in 30 sweeps and did not. What guards it is
  `tests/test_board_seat.py` and nothing else — and that test pins the invariant, not the framework
  behaviour that makes the event go missing. If Textual changes how `send_resize` is computed, the test
  stays green and the hole stops existing without anyone noticing.
- **`Hero` and `Tile` rest on a ticker, not on a guarantee.** They are correct today because
  `tick_fast` calls `redraw()` twelve times a second. Anything that stops or slows that ticker — a paused
  worker group, a lower `MO.FPS`, a future decision to redraw only on change — reopens F-16 for both of
  them, and nothing in the code says so. This increment did not add a guard there, because adding one
  would have been a repair with no measured defect behind it.
- **`.kb-empty`'s verdict is a claim about reachable widths, not about the function.** `k.empty(w)` DOES
  branch on width; the finding is that no layout can hand it widths on both sides of the branch (§2d). A
  change to `weighted_widths`' floor, or to `build()`'s `w > 20` guard, could make that false — and
  nothing would fail. The board's rebuild covers it either way; the note is here so the reasoning is not
  mistaken for "the empty seat does not care about width".
- **`_painted_w` and `_built_w` are two counters about the same seat.** They are correct only because
  each has one writer: `render()` and `build()` respectively. A future `build()` that stamped
  `_painted_w` would silently re-open this, exactly as inc22 §5 says of the card's.

---

## 6. Pending

- **inc22 §5's open item is closed for `.col-head` and answered for the other three.** `Hero` and `Tile`
  are repaired by the ticker; `.kb-empty` cannot go stale at any reachable width.
- **F-8, F-14, F-15 untouched** — no `--surface` sweep, no `verify_language.py` run in this increment.
- **F-17 open** (`verify_language.py:11592` overwrites `prototypes/out/_fixture_late.json` relative to
  `date.today()`). It is the reason the language harness was not run here, so this increment did not
  re-check F-14's two pre-existing reds either.
- **No check asserts a published component sheet carries every derived state** — inc21 §5's hole, still
  open.
- **Nothing in the suite resizes the app and looks at the board.** §5's first two risks are both really
  this one. A test that drove a terminal resize through `TaskboardWidget` and asserted every board surface
  against its seat would cover `Hero`, `Tile`, the heads and the cards in one place.

---

## 7. Suggested next task

**Give the ticker's dependents a guard, or prove they do not need one.** `Hero` and `Tile` are correct
only for as long as `tick_fast` runs at 12 Hz (§5), and that is a property of the app's cadence, not of
the widgets. The measurement is cheap and the instrument exists: run `_inc23_deaf.py`'s Hero/Tile arms
with the ticker suppressed and see what the frame looks like. If they hold a stale bake — and §2c's
`unrepainted=True` rows say they will for at least one frame — then the same `render()` guard applies,
and this time it can go on the widget, because both compose against their OWN seat.

---

## Evidence checklist

- [x] **Tests/type checks/lint pass** — `692 passed, 2 skipped, 4 warnings in 33.60s` (§4d); 688 baseline
      + 4 new. Red-then-green pasted from real runs against both files (§4b). The baseline's
      environment-dependent clipboard test is green on this run and is recorded as such rather than
      claimed.
- [x] **No secrets in code or output** — the change is one container's paint path: no path is read, no
      file written, no network. `freeze_clock()`'s repointing of `default_board_path` at the synthetic
      fixture is untouched, so no capture can print the operator's real board.
      `tests/test_no_live_board.py` and `tests/test_privacy_sweep.py` are green in the suite.
- [x] **No destructive commands run without approval** — no `rm`, no terminal process killed, no force, no
      `git` command that discards work. The one file swapped in place (HEAD's `kanban.py`, for §4b's red
      run) was restored from a copy in the same command and verified with `git diff --stat`
      (`24 insertions`, the fix and nothing else). Every sweep wrote to a `TemporaryDirectory` or to the
      gitignored scratch yard; `prototypes/gallery/` was never opened for write.
- [x] **File count within cap** — 2 source files (`prototypes/widget_slice/kanban.py`,
      `tests/test_board_seat.py`) plus the batch spec, the archived predecessor and this packet: 5, at the
      5 the spec sets.
- [x] **Review packet attached** — this document.
