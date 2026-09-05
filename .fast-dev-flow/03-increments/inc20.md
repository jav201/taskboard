# Increment 20 — the settle: A, B and C, with the hero band inside A

**Batch:** `capture-settle` · **AC-1, AC-2, AC-3** · the operator-approved fix from
`.fast-dev-flow/03-increments/race-probe.md` §7
**Files:** `prototypes/capture_languages.py`, `tests/test_capture_settle.py` (new) — **2 source files**;
plus `.fast-dev-flow/spec.md` (new batch spec) and
`.fast-dev-flow/archive/spec-20260905-kits-learn-3-closed.md` (predecessor, archived verbatim).

**F-1's drift is closed: 58.9 % pairwise disagreement → 0.0 %, 6 of 22 frames → 0 of 22, over 30
fresh-interpreter sweeps. And a defect the old settle used to WRITE now stops the sweep instead —
3 of those 30 runs fail loud, on a wedge measured to be permanent.**

---

## 1. What changed

`settle()` asked one question — "is this frame the same as the last one?" — three times, and signed off.
It now asks three:

| | condition | how |
| --- | --- | --- |
| **A** | every content widget the compositor SAYS it is drawing carries ink in its own clipped area | the four classes `KanbanBoard.build()` mounts (`kb-card`, `col-head`, `kb-empty`, `kb-detail`) **plus `#hero`** |
| **B** | the composited frame is identical on **8** consecutive reads (was 3) | `STABLE_READS` |
| **C** | no **drawn** `TaskCard` holds a paint composed at a seat it no longer has | `_stale_paint`, a shadow render with `update` intercepted — it measures, it never repairs |

A and C are one pass over `visible_widgets` (`_not_at_rest`); B is the read counter. A and C are asked
only once B is otherwise satisfied, because they cost a widget walk and a shadow render per drawn card.

**The hero is the seat this file adds over the harness.** `verify_language.py`'s condition A watches
`BOARD_CONTENT`; the hero is `Hero(id="hero")`, mounted beside the board rather than inside it, so it
carries none of those classes and **nothing was watching it** — which is how a frame could satisfy both
of the harness's conditions and still be the one race-probe §5 diffed: `board_darkside.txt` rows 3-12,
the load bar composed 46 cells wide where the settled frame draws 37, the value `2` and the caption
`Fix checkout 500 error` not yet landed.

**Two docstrings rewritten (AC-2), and a third comment that had gone false.** The module header's
"SETTLE IS WEAKER HERE THAN IN THE HARNESS … Condition A is not covered" and `settle()`'s "Condition A …
is deliberately NOT reimplemented here" both argued against the code that now sits under them. Both now
state the settle that exists and cite race-probe.md for every number. The third is the
`TEXTUAL_ANIMATIONS` comment's "filed as F-1, open, and **NOT fixed here**" — same file, made false by
this increment, corrected in the same edit and named here rather than left for a reader to trip over.

---

## 2. Files modified

- `prototypes/capture_languages.py` — `STABLE_READS` 3 → 8; new `BOARD_CONTENT`, `HERO_ID`,
  `_not_at_rest()`, `_stale_paint()`; `settle()` rewritten; three comment blocks rewritten.
- `tests/test_capture_settle.py` — **new**, 3 tests.
- `.fast-dev-flow/spec.md` — the new batch spec (Phase A).
- `.fast-dev-flow/archive/spec-20260905-kits-learn-3-closed.md` — predecessor archived verbatim.
- Evidence in the gitignored scratch yard: `_settle_before_*.txt`, `_settle_after2_*.txt`,
  `_race_after_cross30.txt`, `_race_final_cross30.txt`, `_wedge_*.txt`, `_settle_suite_inc20b.txt`,
  and the three throwaway probes `_stale_probe.py`, `_drawn_probe.py`, `_wedge_probe.py`.

---

## 3. How to test

```powershell
cd "C:\Users\jjgh8\Github\taskboard\.claude\worktrees\kanban-variants"
$env:PYTHONIOENCODING = "utf-8"

python -X utf8 -m pytest -q tests\test_capture_settle.py
python -X utf8 -m pytest -q

# THE GATE (~6 min): 30 whole sweeps in 30 fresh interpreters, all 22 frames diffed
python -X utf8 prototypes\race_probe.py --cross 30 --engine shipped --tag after `
    > prototypes\out\_race_final_cross30.txt 2>&1
```

Every headless run goes to a **file**, never `DEVNULL` (L-42). No terminal process was killed. No
`--surface` was issued (F-8 untouched). `prototypes/gallery/` was **not** written by this increment —
every sweep here went to a `TemporaryDirectory` or to `prototypes/out/_settle_scratch/`.

---

## 4. Test results

### 4a. The gate — cross-process drift, 30 sweeps, the SHIPPED file

| arm | frames drifting | sweeps non-modal | pairwise | sweeps that finished |
| --- | --- | --- | --- | --- |
| **before** (B, 3 reads) — race-probe.md §4b | **6 / 22** | — | **58.9 %** (256/435) | 30 / 30 |
| **after** (A + B@8 + C) | **0 / 22** | **0 / 27** | **0.0 %** (0/351) | **27 / 30** |

```
  CROSS-PROCESS DRIFT: 0/22 frames over 30 sweeps -> []
  sweeps that are non-modal on >=1 frame: 0/27 []
  PAIRWISE DISAGREEMENT (what the shipped determinism check asks): 0/351 pairs = 0.0 %
```

Before, per frame (race-probe.md §4b, shipped engine, 30 sweeps):

```
board_instrument.txt    {'88494f8eeac1': 29, 'fab9f5e4e0af': 1}
board_swiss.txt         {'73c284a4ac2b': 29, 'a749764b213f': 1}
board_industrial.txt    {'23088c4ecb80': 28, '06784aefff28': 2}
board_prism.txt         {'d20aff65d020': 29, '91e7104baa53': 1}
board_solari.txt        {'bd55f71d5c2b': 29, '1bdf21b9b4d1': 1}
gallery_blueprint.txt   {'3e5e9e26463b': 25, 'ebedeb2bd3c7': 5}
```

After, the same six frames — one grid each, no second hash anywhere in the 22:

```
board_instrument.txt        |       1        | {'88494f8eeac1': 27}
board_swiss.txt             |       1        | {'73c284a4ac2b': 27}
board_industrial.txt        |       1        | {'23088c4ecb80': 27}
board_prism.txt             |       1        | {'d20aff65d020': 27}
board_solari.txt            |       1        | {'bd55f71d5c2b': 27}
gallery_blueprint.txt       |       1        | {'3e5e9e26463b': 27}
```

Note **which** hash survived: it is the modal one from the before run in every case. The new settle did
not pick a different frame — it stopped picking the wrong one.

### 4b. Sweep time — stated, not buried

| | mean | min | max |
| --- | --- | --- | --- |
| before (`--sweep-to`, 3 runs) | **7.92 s** | 7.69 | 8.15 |
| after (`--sweep-to`, 8 runs) | **11.71 s** | 11.30 | 12.08 |

**+3.79 s, +48 %.** The `--cross 30` arm's own per-sweep line agrees (10.7-12.1 s). race-probe.md §7
predicted "+35 %"; the measured figure is higher because that estimate was for condition C alone and
this settle also waits eight reads and walks the widget tree.

### 4c. The test — red then green, run against both files

New file `tests/test_capture_settle.py`, three tests. Against **HEAD `16792b5`'s**
`capture_languages.py` (installed with `git show HEAD:… > …`, then restored from a copy):

```
FAILED tests/test_capture_settle.py::test_settle_waits_for_the_hero_band - AssertionError: settle signed off before the hero band painted -- '        ...
FAILED tests/test_capture_settle.py::test_settle_names_the_widget_it_gave_up_on - AssertionError: settle returned on an unpainted hero band
2 failed, 1 passed in 0.38s
```

Against the new file:

```
3 passed in 1.59s
```

**The one that passes in both is the point.** `test_the_old_settle_signs_off_on_a_blank_hero_band`
asserts the OLD condition's behaviour — three identical reads returning a frame whose `#hero` band is
empty — and it is what stops the other two being vacuous: a fixture whose hero fills early would satisfy
"the new settle returns a painted band" without proving anything.

**The fixture's clock is the read count, and that was measured rather than chosen.** Chaining
`call_after_refresh` was the first attempt and does not delay anything: one `pilot.pause()` drains about
**twenty thousand** chained callbacks (measured), because the chain is a busy loop and not a wait. So the
hero arms on the fifth read — `settle` reads the composited frame exactly once per iteration — and the
fill itself still lands through `call_after_refresh`. Read 5 is past the old condition's three and far
inside `MAX_SETTLE`, so neither assertion depends on how fast this machine is.

### 4d. Suite

```
python -X utf8 -m pytest -q
1 failed, 684 passed, 2 skipped, 4 warnings in 32.31s
FAILED tests/test_app.py::test_win_clipboard_roundtrip - AssertionError: assert None == 'roundtrip 123 ABC taskboard'
```

**684 + 1 = 685 = the 682 baseline + 3 new tests.** The single failure is the documented
environment-dependent clipboard test (PENDING #22, `RUN.md`), and it fails identically on the pre-edit
tree — measured at Phase A: `1 failed, 681 passed, 2 skipped, 4 warnings in 32.06s`.

---

## 5. The finding this increment turned up: the wedge is real, and it is permanent

Three of the thirty sweeps did **not** finish. All three were the COLUMNS branch — `board instrument`
(×2), `board naught`, `board industrial` — and all three raised the same timeout:

```
RuntimeError: board instrument: never settled after 40 frames; not settled:
  kb-card@60,21 STALE PAINT (composed at a seat it no longer has; seat is now 31), ... (x4)
```

**Measured, not assumed.** `MAX_SETTLE` is 40 pauses ≈ 40 ms, which is less than one `tick_fast`
interval (`motion.FPS = 12` → 83 ms), so "gave up too early" was a live hypothesis. A probe kept
pausing **600 iterations past the bound** and caught it once in 10 sweeps:

```
=== board instrument: would TIME OUT here (1209 ms) ===
  seat=28 region=Region(x=59, y=20, width=30, height=2)
    CONTENT |'... Design home…[/]... ⠒⡗⠒⠒⠒⠒⠒⠒┊⠒⠒ ...'|
    SHADOW  |'... Design homepage moc…[/]... ⠒⡗⠒⠒⠒⠒⠒⠒┊⠒⠒⠒⠒⠒⠒┊⠒⠒⠒ ...'|
  board instrument: STILL not settled after 640 iterations (19490 ms) -- WEDGED
```

**19.5 seconds and it never corrects.** That is not a settle being impatient; the card is holding a
paint composed at a narrower seat and nothing in the app re-renders it. And it is **the same cells**
race-probe.md §5 named for these three languages: "`⣿ Design home… 0d` where the good grid has
`⣿ Design homepage moc… 0d`, gauges `⠒⣿⣿⣿⣿⣿⣿⠒┊⠒⠒` where the good grid has `⠒⣿⣿⣿⣿⣿⣿⠒┊⠒⠒⠒⠒⠒⠒┊⠒⠒⠒`."

So the old settle **wrote this frame** — it is 2 of the 6 drifting frames — and the new one refuses it.
The refusal is the change working. The wedge itself is a `kanban.py` defect, it is now named and
reproducible, and it is **out of this increment's scope**: filed below.

---

## 6. Two things that had to be measured before they could be written

**(1) Resetting `stable` on a widget-condition failure was wrong, and cost 1 sweep in 3.** The first
version reset the run of identical reads whenever A or C was red, reasoning that the frame must be
stable *after* the last widget comes to rest. It must — and the read counter already delivers that for
free, because a widget that finishes painting CHANGES the composited frame and `stable` drops to 0 by
itself on the next read. Resetting as well only spent the `MAX_SETTLE` budget: every failed check threw
away a seven-read run-up, and `board industrial` timed out in **1 of 3** sweeps on a screen that was
perfectly fine. Removed; the comment in the code says why.

**(2) Condition C is asked about DRAWN cards, not every card in the tree.** `verify_language.py` asks it
inside its `visible_widgets` loop; the first version here asked `app.query(TaskCard)`. The tree is wider
than the frame — measured on this fixture, **3 to 9 of the 15 cards are in the DOM but not drawn in every
one of the eleven languages**, at seats belonging to a layout no longer on screen (50, 55, 107, 111) —
because `KanbanBoard.build()`'s `remove_children()` is **asynchronous** and says so in its own comment.
A card the compositor is not drawing contributes no cells and cannot make the capture wrong.

**Honest note on (2): it did not change the failure rate.** 3/30 before the restriction, 3/30 after, and
the failing cards turned out to be drawn ones (§5). The restriction is still right — it removes a class
of false positive by construction and matches the harness — but it was not the cure I expected when I
made it, and 20 diagnostic in-process sweeps failed to reproduce the wedge at all before the
past-the-bound probe caught it.

---

## 7. Risks

- **The documented command now fails loud about one run in ten** (and `main()` runs two sweeps, so ~19 %
  per invocation). That is a better failure than the 58.9 % silent one it replaces — nothing wrong gets
  written — but it is a real change in how the sweep behaves and the next operator will meet it.
- **+48 % sweep time.** Cheap here (11.7 s); it is a per-language cost and would grow with the roster.
- **`_stale_paint` is a fifth copy of a shadow render** that also lives in `verify_language.py` and
  `race_probe.py`. It is duplicated rather than shared because `verify_language.py` has no
  `if __name__ == "__main__"` guard and importing it runs 9923 checks. Named, not hidden.
- **Condition A on `#hero` is an INK check, not a seat check.** It catches a blank band (solari's
  unpainted `DAYS OVERDUE` row) and it caught the darkside hero in the measurement — but a hero composed
  at a stale seat that still carries ink would pass A. There is no shadow-render oracle for the hero:
  `Hero.show(signal, reading, width, series)` needs data only the app has. What covers it today is the
  eight reads, which is evidence (30 sweeps) and not proof.
- **The 30-sweep numbers are a measurement, not a gate.** race-probe.md §10's warning still stands: a
  1/30 frame is one observation, and no frame should be declared safe from this table.

---

## 8. Pending

- **F-16 (new): a `TaskCard` in a column can permanently hold a paint composed at a narrower seat.**
  ~10 % of sweeps, COLUMNS branch only, four cards at once, measured stale for 19.5 s. `on_mount`'s
  `call_after_refresh(self.render_card)` and `on_resize` are both supposed to correct it and neither
  does. This is F-1's remainder and it belongs to `prototypes/widget_slice/kanban.py`.
- **F-1's capture half is closed**; the app half is F-16.
- **F-8, F-14, F-15 untouched** — no `--surface` sweep, no `verify_language.py` run in this increment.
- **AC-4, AC-5, AC-6 are inc21's.** The 22 committed frames are NOT re-baked here and
  `prototypes/gallery/` was never opened for write.

---

## 9. Suggested next task

inc21: pin `sig_board_file`'s mtime input so a fresh checkout reproduces the frames, then re-bake the 22
and name every mover.

---

## Evidence checklist

- [x] **Tests/type checks/lint pass** — `1 failed, 684 passed, 2 skipped in 32.31s`; 682 baseline + 3
      new; the one failure is the documented env-dependent `test_win_clipboard_roundtrip`, red on the
      pre-edit tree too (§4d).
- [x] **No secrets in code or output** — no new path is read; `freeze_clock()`'s existing repointing of
      `default_board_path` at the synthetic fixture is untouched, so no capture can print the operator's
      real board. `tests/test_no_live_board.py` and `tests/test_privacy_sweep.py` green in the suite.
- [x] **No destructive commands run without approval** — no `rm`, no terminal process killed, no git
      command that changes state beyond the increment's own commit. Every sweep wrote to a
      `TemporaryDirectory` or the gitignored scratch yard; `prototypes/gallery/` was never written.
      The one file swapped in place (HEAD's `capture_languages.py`, for §4c's red run) was restored from
      a copy in the same command, verified by `git diff --stat`.
- [x] **File count within cap** — 2 source files (`capture_languages.py`, `tests/test_capture_settle.py`)
      plus the batch spec and the archived predecessor: 4, under the 5 the spec sets.
- [x] **Review packet attached** — this document.
