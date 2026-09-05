# race-probe — the darkside capture race, measured with an instrument

**Base:** worktree `kanban-variants`, HEAD `d47abff`, clean (`git status --porcelain` returned one
line: the new untracked probe). Read-only git only; no state changed. Language: English.

**Disposition in one line: the cause is found, the counts are here, and the fix is a PROPOSAL, not
an edit** — it is ~13 code lines plus a new cross-module import and two docstrings that currently
assert the opposite, which is over the ten-line bar this task set for applying.

---

## 1. What changed

One new file, `prototypes/race_probe.py`. Nothing else on disk was edited — not the kit, not
`capture_languages.py`, not `verify_language.py`, not the committed frames in `prototypes/gallery/`.
Every sweep the probe runs writes into a `TemporaryDirectory`.

The probe has four arms:

| arm | what it does |
| --- | --- |
| default | N darkside board captures, each in a fresh Textual app, instrumented |
| `--sweep` | the same, but with the six preceding languages captured first **in the same process**, so darkside is the seventh of ten as it is in the real sweep |
| `--amplify MS` | delays `TaskCard`'s deferred corrective re-render, the pass-46 falsifiability lever |
| `--cross N` | runs a **whole sweep N times in N fresh interpreters** and diffs all 22 frames — the only arm that can express the defect (see §5) |

`--cross` takes `--engine shipped` (runs `capture_languages.py --sweep-to`) or `--engine self`
(runs the probe's own sweep, which **calls** `CL.settle`, `CL.write`, `CL.freeze_clock` and the
shipped loop, and exposes two knobs: `--stable K`, `--cond-c`). The two engines were verified
byte-identical at `--stable 3`: same 22 hashes.

Per run the probe records the four-check signature, per-iteration settle timings and frame hashes,
the compositor reflow count at capture, every `BOARD_CONTENT` widget the compositor draws with its
painted verdict and its seat width, the `InvokeLater` queue depth on the board and its cards, a
**trace of every `render_card` call with the seat it saw**, and the grid hash at capture and again
after 12 further pauses.

## 2. Files modified

- `prototypes/race_probe.py` — **new**, 1 file, the instrument.
- `.fast-dev-flow/03-increments/race-probe.md` — this packet.
- Evidence written to the gitignored scratch yard `prototypes/out/`:
  `_race_probe_plain.txt/.json`, `_race_probe_amp50.txt`, `_race_probe_sweep.txt`,
  `_race_probe_cross30.txt`, `_race_probe_self_control.txt`, `_race_probe_self_stable8.txt`,
  `_race_probe_self_s8_condc.txt`.

## 3. How to test

```powershell
cd "C:\Users\jjgh8\Github\taskboard\.claude\worktrees\kanban-variants"
$env:PYTHONIOENCODING = "utf-8"

# in-process, darkside alone (30 runs, ~8 s)
python -X utf8 prototypes\race_probe.py -n 30 --tag plain          > prototypes\out\p.txt 2>&1

# darkside as the seventh of a ten-language sweep, one process (~3 min)
python -X utf8 prototypes\race_probe.py -n 30 --sweep --tag sweep  > prototypes\out\s.txt 2>&1

# THE ARM THAT SEES IT: 30 whole sweeps, 30 processes (~4.5 min each arm)
python -X utf8 prototypes\race_probe.py --cross 30 --tag cross30   > prototypes\out\c.txt 2>&1
python -X utf8 prototypes\race_probe.py --cross 30 --engine self --stable 3 --tag ctl  > ...
python -X utf8 prototypes\race_probe.py --cross 30 --engine self --stable 8 --tag s8   > ...
python -X utf8 prototypes\race_probe.py --cross 30 --engine self --stable 8 --cond-c --tag fix > ...

python -X utf8 -m pytest -q
```

Every headless run goes to a **file**, never `DEVNULL` (L-42). No terminal process was killed. No
`--surface` was issued (F-8 untouched).

## 4. Test results

### 4a. In-process: 0/30 on every arm — the historical result, reproduced

| arm | runs | C1 settled | C2 painted | C3 fresh paint | C4 final frame | distinct grids |
| --- | --- | --- | --- | --- | --- | --- |
| darkside alone | 30 | 0 fail | 0 fail | 0 fail | 0 fail | **1** |
| darkside alone, `--amplify 50` (blocking sleep) | 30 | 0 | 0 | 0 | 0 | **1** |
| darkside alone, `--amplify 50` (`set_timer`) | 30 | 0 | 0 | 0 | 0 | **1** |
| darkside 7th of ten, one process (`--sweep`) | 30 | 0 | 0 | 0 | 0 | **1** |

The four checks are: **C1** settle returned, not blank, no timeout · **C2** every `BOARD_CONTENT`
widget the compositor draws carries ink (verify_language's condition A) · **C3** no `TaskCard`
holds a paint composed at a seat it no longer has (condition C, asked as a shadow render with
`update` intercepted — it measures, it never repairs) · **C4** the frame settle signed off on is
still the frame 12 pauses later.

Settle used **3-6 of 40** iterations, 125-430 ms. Board and card `InvokeLater` queues were **0** at
every capture.

**The 18-cell bake is real and is always corrected in time.** The `render_card` seat trace:

```
darkside alone   : {0: 90, 112: 30, 111: 15}
darkside 7th/ten : {0: 811, 112: 75, 20: 12, 30: 38, 55: 27, 54: 18, 18: 6, 26: 12, 47: 27,
                    111: 30, 28: 27, 51: 27, 50: 9, 108: 45, 107: 15, 31: 4, 56: 9, 32: 46}
```

Seat `0` is the pass-46 fallback (`max(8, (0 or 20) - 2)` = an 18-cell row) and it is composed
90-811 times per run. The intermediate seats (18, 26, 47, 30, 55…) are the previous theme's column
layout still in force when the new theme's cards mount. Every one of them was corrected before the
capture in all 120 in-process runs.

**Two negative results worth keeping.** (1) `--amplify` with a **blocking** `time.sleep` in the
deferred callback proves nothing: it blocks the event loop, so `pilot.pause()` cannot return a frame
during the delay and settle trivially waits it out — 0/30, settle 1.7-3.2 s per run instead of
0.2 s. The lever had to be a `set_timer`, which yields. (2) Even the yielding lever is 0/30 on this
posture.

### 4b. Cross-process: the defect, on the first pair

| arm | settle condition | frames drifting | sweeps non-modal | pairwise disagreement |
| --- | --- | --- | --- | --- |
| **shipped `capture_languages.py`** | B, 3 identical reads | **6 of 22** | — (metric added after this arm) | — |
| probe sweep, control (byte-identical) | B, 3 identical reads | **4 of 22** | **11 / 30** | **256 / 435 = 58.9 %** |
| probe sweep | B, **8** identical reads | 2 of 22 | 2 / 30 | 57 / 435 = 13.1 % |
| probe sweep | B, 8 reads **+ condition C** | **0 of 22** | **0 / 30** | **0 / 435 = 0.0 %** |

Pairwise disagreement is the number the operator actually sees: `main()` compares ONE sweep against
ONE control sweep, so its red rate is the chance that two independent sweeps differ anywhere.
**58.9 %** is consistent with `inc6.md`'s "3 red in 6 runs" and wider than `inc3.md`'s one-in-three.

Per-frame counts, shipped engine, 30 sweeps:

```
board_instrument.txt    {'88494f8eeac1': 29, 'fab9f5e4e0af': 1}
board_swiss.txt         {'73c284a4ac2b': 29, 'a749764b213f': 1}
board_industrial.txt    {'23088c4ecb80': 28, '06784aefff28': 2}
board_prism.txt         {'d20aff65d020': 29, '91e7104baa53': 1}
board_solari.txt        {'bd55f71d5c2b': 29, '1bdf21b9b4d1': 1}
gallery_blueprint.txt   {'3e5e9e26463b': 25, 'ebedeb2bd3c7': 5}
board_darkside.txt      {'58e1a364fb7b': 30}          <- 0/30 on this arm
```

Per-frame counts, probe engine at the same setting, 30 sweeps:

```
board_swiss.txt         {'73c284a4ac2b': 29, 'a749764b213f': 1}
board_industrial.txt    {'23088c4ecb80': 28, '06784aefff28': 2}
board_darkside.txt      {'58e1a364fb7b': 25, '0b0dceb4689d': 5}   <- 5/30
gallery_blueprint.txt   {'3e5e9e26463b': 25, 'ebedeb2bd3c7': 5}
```

**Darkside drifts 5 of 30 — but only in the cross-process arm, and it did not drift in the other
30-sweep run of the same code.** The frame that drifts is not fixed; the mechanism is.

## 5. The diff of the bad grids — WHICH cells, and therefore which widget

### board_darkside — rows 3-12, the HERO band. Not the cards.

```
row  3 MODAL   |  │                                            │
row  3 VARIANT |  │████                                        │
row  4 MODAL   |  │2                                           │
row  4 VARIANT |  │                                            │
row  5 MODAL   |  │Fix checkout 500 error                      │
row  5 VARIANT |  │                               ████         │
row  8 MODAL   |  │                                            │
row  8 VARIANT |  │████████                                    │
row 11 MODAL   |  █████▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁  13%
row 11 VARIANT |  ██████████████▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁
row 12 MODAL   |  █▄▄ flow
row 12 VARIANT |  ▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁
```

The bad grid's load band is **46 cells wide and two rows tall** where the good grid's is **37 cells
and one row**, the `13%` readout has not been placed, the hero's own value (`2`) and caption
(`Fix checkout 500 error`) have not landed, and row 12's `█▄▄ flow` label is still load-bar. This is
the hero/load band composed at a seat it no longer has — the same *class* as the card bake, one
widget family up.

**That is why PENDING's exclusion was right and still is.** Every `BOARD_CONTENT` widget (`kb-card`,
`col-head`, `kb-empty`, `kb-detail`) is painted in every one of the 120 in-process runs, and no card
is stale. The hero is **not** a `BOARD_CONTENT` widget, so neither condition A nor condition C is
watching it — which is exactly how a frame can pass both and still be wrong.

### The other five frames — the same shape, different widgets

- **board_instrument · board_industrial · board_naught** — the DOING column's cards composed at a
  **narrower** seat: `⣿ Design home… 0d` where the good grid has `⣿ Design homepage moc… 0d`, gauges
  `⠒⣿⣿⣿⣿⣿⣿⠒┊⠒⠒` where the good grid has `⠒⣿⣿⣿⣿⣿⣿⠒┊⠒⠒⠒⠒⠒⠒┊⠒⠒⠒`, and industrial's meta row losing
  `[DUE:0D]` entirely. **This is the pass-46 stale card bake, verbatim, in the sweep that never got
  condition C.**
- **board_prism** — the pixel hero composed at ~44 cells instead of ~77, the load bar at 36 instead
  of 110, and the signal captions truncated (`Nea`, `Ove`, `Wor` for `Nearest de`, `Overdue co`).
- **board_swiss** — hero rows and load bar at the wrong width, and the signal row in the *opposite*
  direction: `Nearest d  Overdue c  Work in f` (captions, no values) where the good grid has
  `Near   2  Over   2  Work   4` (values). Composed at a **wider** seat, then re-composed narrow.
- **board_solari** — the `DAYS OVERDUE` label row **blank**. The split-flap label, unpainted. This is
  the one F-1 named first (`inc1.md`), and it is condition A's shape, not condition C's.
- **gallery_blueprint** — one switch segment, `▇▇` vs `▄▄`. An animation step, with
  `TEXTUAL_ANIMATIONS=none` already set. 5 of 30, the highest single rate in the sweep.

**One mechanism covers all seven frames: `settle()` signs off on a frame the app has not finished
composing.** Sometimes that is a card, sometimes a hero, sometimes a label that has not painted,
sometimes an animation step. Condition B — three identical composited reads — is satisfied by all
of them, because a widget waiting on a deferred re-render produces a genuinely static frame while it
waits.

## 6. The hypothesis, made falsifiable, and its result

> **H:** `capture_languages.settle()` implements condition B only (its own docstring says so), and
> three identical reads is short enough that a pending deferred re-render is still outstanding. If
> that is the cause, **waiting longer must drive the drift down**, and adding the one condition that
> catches a static-but-wrong frame (condition C, the shadow render) must drive it to **zero**. If the
> cause were something else — the fixture, the clock, the theme order, the process — none of these
> levers would move the rate at all.

Run, same engine, same 22 frames, 30 fresh-process sweeps per arm:

| settle | frames drifting | sweeps non-modal | pairwise |
| --- | --- | --- | --- |
| B, 3 reads (**the shipped condition**) | 4 / 22 | 11 / 30 | **58.9 %** |
| B, 8 reads | 2 / 22 | 2 / 30 | 13.1 % |
| B, 8 reads + condition C | **0 / 22** | **0 / 30** | **0.0 %** |

**Confirmed, and the residual named its own cure.** Raising the read count alone leaves exactly two
frames — and both residual diffs are card-title truncations, i.e. the stale bake, i.e. precisely the
thing condition C exists to catch. Adding it takes 13.1 % to 0.0 %.

## 7. The proposal (NOT applied)

In `prototypes/capture_languages.py`:

```python
STABLE_READS = 8                      # was 3

def _stale_paint(card) -> bool:       # verify_language.py:322, lifted verbatim
    got = []
    card.update = got.append
    try:
        card.render_card()
    finally:
        del card.update
    return bool(got) and got[0] != card.content

# inside settle(), after `if stable < STABLE_READS - 1: continue`
from kanban import TaskCard
if any(_stale_paint(c) for c in app.query(TaskCard)):
    stable = 0
    continue
```

**Why it is proposed and not applied**, said plainly:

1. It is **~13 code lines**, over the ten-line bar this task set for applying a fix in place.
2. It adds an import of `kanban` to a file that today imports only `taskboard.themes` and `app`, and
   it **contradicts two long docstrings** (the module header's "Condition A is not covered" and
   `settle()`'s "Condition A … is deliberately NOT reimplemented here"). Those paragraphs are the
   file's stated design; rewriting them is a decision, not a patch.
3. Cost: the sweep goes from ~8.5 s to ~11.5 s per run (+35 %), measured.
4. It would make the next sweep **rewrite the 22 committed frames in `prototypes/gallery/`** — which
   the live batch's AC-9 forbids without naming the mover in advance.
5. Condition C covers the card residual but **not** solari's unpainted label or blueprint's
   animation step; those went green at 8 reads alone, on 30 sweeps, which is evidence and not proof.

## 8. A second finding: the committed frames cannot be reproduced on any fresh checkout

The probe's darkside grid differs from the committed `prototypes/gallery/board_darkside.txt` in
**exactly one cell region**, deterministically, in all 30 runs:

```
row 16 DISK  |   d   2  !!   2  w   4   x   1  $   9   f -98
row 16 PROBE |   d   2  !!   2  w   4   x   1  $   9   f
```

`taskboard/engine.py:sig_board_file` computes `age_min = (time.time() - p.stat().st_mtime) / 60`.
`freeze_clock()` pins `time.time()`; it cannot pin the **file's mtime**. The fixture's content is
byte-identical to HEAD (`git diff --stat -- prototypes/out/_fixture_late.json` is empty) but its
mtime is now `2026-09-05 00:02`, so `age_min` is **-46982** instead of the `-98` the committed
frames were taken with, and the value overflows its seat and is dropped from the row entirely.

So a capture in this repo is a function of a timestamp git does not carry. Anyone who re-clones and
re-sweeps gets different frames in every language whose hero band shows the board-file signal —
including `board_swiss.txt` (`B -46982`) and `board_prism.txt` (`f -46982`) in this run's own output.
Reported, not fixed: the cure (pin the mtime alongside the clock, or point `sig_board_file` at a
fixed instant) is a change to the capture contract and belongs to whoever owns it.

## 9. Suite

```
python -X utf8 -m pytest -q
1 failed, 681 passed, 2 skipped, 4 warnings in 32.57s
FAILED tests/test_app.py::test_win_clipboard_roundtrip - AssertionError: assert None == 'roundtrip 123 ABC taskboard'
```

**681 + 1 = 682, the recorded baseline.** The single failure is the documented environment-dependent
clipboard test (PENDING item #22, RUN.md: "fails if the clipboard is busy"), **pre-existing** — no
shipped file was edited in this increment. `tests/test_surface.py::test_lattice_pixels_are_two_colours`
(**F-15**) **passed** on this run; F-15 remains one observation old and unexplained.

## 10. Risks

- **The probe's `--cross` arm is a measurement, not a gate.** Its rates are over 30 sweeps; a 1/30
  frame is one observation and the two 30-sweep runs of the same code implicated **different**
  frames (shipped: instrument/swiss/industrial/prism/solari/blueprint; probe: swiss/industrial/
  **darkside**/blueprint). The *mechanism* is stable across both; the *frame list* is not, and no
  frame should be declared safe from this table.
- **`--cond-c` monkeypatches nothing but calls `card.render_card()` on every card at every settle
  iteration.** It is a shadow render (`update` intercepted) so it cannot repair, but it is not free:
  it is the +35 % in §7.
- **The probe imports `capture_languages`** and mutates `CL.OUT` / `CL.STABLE_READS` for the duration
  of a `--sweep-to`. Restored in a `finally`. It never points `CL.OUT` at `prototypes/gallery/`.
- The three `--amplify` numbers say the pass-46 lever does **not** reproduce this on darkside. That
  is a negative result about the lever, not evidence the bake is absent — the seat trace shows it
  happening 90-811 times a run.

## 11. Pending

- **F-1: cause found, fix proposed, not applied.** §7 is the change; it needs a decision on the two
  docstrings and on regenerating the 22 committed frames (AC-9).
- **The mtime dependency (§8) is unfiled anywhere but here.** It is a determinism defect independent
  of F-1 and it defeats the `.txt`-is-the-art contract on any fresh checkout.
- **F-15 untouched** — this increment did not run `test_surface.py` in isolation, and one green
  full-suite run is not a diagnosis.
- **F-8 untouched** — no `--surface` sweep was issued.
- `prototypes/race_probe.py` **stays as the instrument** whatever is decided about the fix. It is
  untracked and gitignored output aside; committing it is a separate call.

## 12. Suggested next task

Take the §7 proposal to a decision: either apply it with the two docstrings rewritten and the 22
frames re-swept and named as movers, or record the measured rate in `RUN.md` — whose claim that
"the suite has been flake-free since the forty-sixth pass" is about `verify_language.py` and is read
by this file's users as though it covered the sweep, which §4b measures at **58.9 % pairwise
disagreement**.

---

## Evidence checklist

- [x] **Tests/type checks/lint pass** — `1 failed, 681 passed, 2 skipped in 32.57s`; the one failure
      is the documented env-dependent `test_win_clipboard_roundtrip` and is pre-existing (no shipped
      file was edited). §9.
- [x] **No secrets in code or output** — the probe reads `prototypes/out/_fixture_late.json` only;
      `freeze_clock()` already repoints `default_board_path` away from `~/.taskboard/board.json`, and
      the probe calls it rather than reimplementing it. No path outside the worktree is written.
- [x] **No destructive commands run without approval** — no `rm`, no terminal process killed, no git
      command that changes state (`git status --porcelain`, `git diff --stat`, `git log -1` only).
      Every sweep wrote into a `TemporaryDirectory`; `prototypes/gallery/` was never opened for write.
- [x] **File count within cap** — 2 files: `prototypes/race_probe.py` (new) and this packet.
- [x] **Review packet attached** — this document.
