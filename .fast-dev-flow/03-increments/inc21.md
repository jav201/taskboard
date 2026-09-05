# Increment 21 — the signature is pinned, and the 22 frames are re-baked

**Batch:** `capture-settle` · **AC-4, AC-5, AC-6** · race-probe.md §8, the second finding
**Files:** `prototypes/capture_languages.py`, `tests/test_capture_settle.py` — **2 source files**; plus
the 22 re-baked frames (and their 22 SVG pictures) in `prototypes/gallery/`, which are data.

**A capture in this repo was a function of a timestamp git does not carry. It no longer is: two sweeps
taken 99 days apart in fixture mtime now produce 22 byte-identical grids.**

---

## 1. The defect

`taskboard/engine.py:sig_board_file` ages the board file with
`age_min = (time.time() - p.stat().st_mtime) / 60`. `freeze_clock()` pins the first term. **Nothing
pinned the second**, and git does not carry mtimes — so the signal read whatever minute the fixture
happened to land on *this* disk.

The committed frames were taken at `f -98`. This tree, whose `_fixture_late.json` is byte-identical to
HEAD, rendered **`f -46982`**, deterministically, in every run. Eleven of the twenty-two frames carry
that cell. Anyone who cloned the repo and re-swept got eleven different grids and no way to tell why.

---

## 2. The decision: pinned through `freeze_clock()`, not derived from content

Both cures were on the table and race-probe.md §8 named them as such. The choice is the second, and the
reason is what `sig_board_file` **means**:

- **Deriving the value from the file's bytes** would make it a different signal wearing the same label.
  It watches for edits made OUTSIDE this process — that is its docstring and its whole reason for
  living in the slow worker group — and a content hash cannot say *when* one happened. Changing it would
  also change the shipped app, and this file's standing rule is that a capture **photographs the shipping
  code, not a variant of it** (`freeze_clock`'s own docstring).
- **Pinning the input** is what `freeze_clock()` already exists to do. It pins the present (`FROZEN`), it
  pins `time.time()` for the engine, and it repoints `default_board_path` at the synthetic fixture. A
  file's timestamp is an input of exactly that kind, so it is pinned in the same seat, and
  `sig_board_file` is left untouched.

```python
FIXTURE_AGE_S = 450
...
_t = fixed.timestamp() - FIXTURE_AGE_S
os.utime(FIXTURE, (_t, _t))
```

**450 and not 420, and that is not fussiness.** `int(age_min)` is what reaches the grid, so a pin landing
exactly on a minute boundary can be flipped to the minute below by the sub-microsecond error of a float
timestamp round-tripping through the filesystem's own resolution. Seven and a **half** minutes renders
`7` from either side of that error.

**What it costs, said plainly:** the capture now writes *metadata* (never content) to
`prototypes/out/_fixture_late.json`. That is the same file this function already repoints every reader
at, the write is idempotent, and git carries neither the before nor the after.

**Security:** the pin stays strictly inside the existing repointing. It stamps the synthetic fixture and
never `~/.taskboard/board.json` — which is the reason `default_board_path` was repointed in the first
place (a published frame must not print the size or save-time of the operator's real board).
`tests/test_no_live_board.py` and `tests/test_privacy_sweep.py` are green in the suite below.

---

## 3. How to test

```powershell
cd "C:\Users\jjgh8\Github\taskboard\.claude\worktrees\kanban-variants"
$env:PYTHONIOENCODING = "utf-8"

python -X utf8 -m pytest -q tests\test_capture_settle.py     # 4 tests, one of them the pin
python prototypes\capture_languages.py                        # re-bake + its own 2-process check
python prototypes\capture_languages.py --surface              # plain and alone (F-8)
python -X utf8 prototypes\verify_language.py
python -X utf8 -m pytest -q
```

Headless stdout to a file, never `DEVNULL` (L-42) — except `--surface`, which is run **plain and alone**
because F-8 blocks it when its output is redirected inside a compound command. No terminal process was
killed.

---

## 4. Test results

### 4a. AC-4 — the observable: two mtimes, one set of grids

Two full sweeps into two temporary directories, the fixture stamped **now** for the first and **99 days
ago** for the second:

```
run 0: fixture mtime set to Sat Sep  5 08:17:33 2026
   sweep failed (F-16 wedge), retrying: RuntimeError: board naught: never settled after 40 frames ...
run 1: fixture mtime set to Fri May 29 08:17:33 2026
AC-4: 22 frames compared across two different fixture mtimes -> 0 differ []
```

Before the pin the same experiment moved eleven frames. (The retry line is F-16, inc20 §5 — recorded
rather than hidden, because it is now a normal event in any loop that sweeps.)

And the cell itself, asked of a fresh interpreter that first stamps the fixture with the current time:

```
value='7' caption='min since save' detail='5 KB on disk' sev=0
```

`tests/test_capture_settle.py::test_the_board_file_signal_does_not_read_the_checkout_clock` asserts that
line. It runs in a **subprocess** on purpose: `freeze_clock()` rebinds `datetime`/`date` inside every
imported taskboard module and swaps a shim over `engine.time`, and leaving that in the pytest process
would run the other 685 tests against a frozen clock.

### 4b. AC-5 — the re-bake, and its own determinism check

`python prototypes/capture_languages.py`, clean on the first attempt:

```
fixture _fixture_late.json | viewport 118x34 | 11 languages | animations off
  naught      board 118x34  35.6% ink   gallery 118x34  14.1% ink
  ...
  blueprint   board 118x34  20.5% ink   gallery 118x34  11.7% ink

  re-sweeping in a fresh process to check reproducibility...
  22 grids identical across two PROCESSES

  22 captures -> ...\prototypes\gallery
  no two boards identical
```

**That middle line is the one that matters.** It is the check race-probe.md measured failing 58.9 % of
the time.

### 4c. Which frames moved, and why — all 22, each named

**The eleven boards: one line each, and it is the board-file signal.**

| frame | line | change |
| --- | --- | --- |
| board_naught · board_corgi | 16 | the signal tile row |
| board_instrument · board_swiss · board_industrial · board_nord · board_darkside · board_prism | 17 | the signal tile row |
| board_ledger · board_blueprint | 15 | the signal tile row |
| board_solari | 14 | the signal tile row |

```
- d   2  !!   2  w   4   x   1  $   9   f -98        (darkside)
+ d   2  !!   2  w   4   x   1  $   9   f   7

-     Near   2  Over   2  Work   4  Bloc   1  Work   9  Boar -98      (swiss)
+     Near   2  Over   2  Work   4  Bloc   1  Work   9  Boar   7
```

**Cause: §2's pin, and nothing else.** No board frame moved for a settle reason — the hero band did not
shift in any of the eleven, which is worth saying out loud: race-probe.md's darkside hero drift is
intermittent, and the frame that happened to be committed was one of the good ones.

**The eleven component sheets: the scroll-bar thumb, plus a missing control state in two of them.**

| frame | lines | change | why |
| --- | --- | --- | --- |
| gallery_naught · gallery_corgi · gallery_instrument | 11-12 | thumb moves up a row (`▇▇` → `▁▁` one line higher) | settle |
| gallery_swiss | 12-13 | same | settle |
| gallery_industrial · gallery_blueprint | 12 | `▅▅` → `▇▇` | settle |
| gallery_nord | 11 | `▂▂` → `▃▃` | settle |
| gallery_prism | 12 | `▆▆` → blank | settle |
| gallery_ledger | 12 | blank → `▂▂` | settle |
| **gallery_darkside** | 5, 13, **27-29** | `(o)` → `(.)`, thumb `▄▄` → `▇▇`, **and the `invalid` row appears** | settle |
| **gallery_solari** | 13, **29-30** | thumb `▄▄` → `▇▇`, **and the `invalid` row appears** | settle |

The thumb is the symptom race-probe.md §5 filed under `gallery_blueprint` — "one switch segment, `▇▇` vs
`▄▄`. An animation step, with `TEXTUAL_ANIMATIONS=none` already set" — and it turns out to be the
component sheet's **scroll bar**, caught before it settled, in all eleven languages rather than one.

**Darkside and solari are not cosmetic and they are the finding of this increment.** The committed sheets
were missing a row:

```
  OLD (darkside, rows 27-29)          NEW (rows 27-29)
    ╌task╌╌╌╌╌╌╌   disabled             Øtask      Ø   invalid
    ▬title     ▬   placeholder          ╌task╌╌╌╌╌╌╌   disabled
    ▮t windows◆▮   window               ▬title     ▬   placeholder
```

`invalid` is the sixth derived control state `kits-learn-3` shipped (its AC-1). **The old settle wrote a
component sheet that had not finished composing, and the row went missing from the published art.** The
sheet is COMPONENTS.md's canary; the canary was one row short in two languages and nothing caught it,
because the only check on these frames was "do two runs agree" and both runs were wrong the same way
often enough to pass.

### 4d. AC-6 — nothing else moved

```
$ git status --short prototypes/gallery/surface_*
(no output)
```

The 11 `surface_*.txt` (and their SVGs) are **byte-identical to HEAD** after the `--surface` sweep, which
was run plain and alone. `prototypes/components/` was never opened.

Against `.fast-dev-flow/baseline-kits2/`, two surface frames differ — `surface_corgi.txt` and
`surface_industrial.txt` — and both **already differed at HEAD** (measured with `git show HEAD:…`). They
are the pre-existing movers `kits-learn-3`'s close recorded as "`kits-learn-2`'s, not this batch's".
Neither is this increment's.

### 4e. Suite

```
python -X utf8 -m pytest -q
1 failed, 685 passed, 2 skipped, 4 warnings in 33.49s
FAILED tests/test_app.py::test_win_clipboard_roundtrip - AssertionError: assert None == 'roundtrip 123 ABC taskboard'
```

**685 + 1 = 686 = the 682 baseline + 4 new tests** (3 from inc20, 1 here). The single failure is the
documented environment-dependent clipboard test, red on the pre-batch tree too (Phase A measured
`1 failed, 681 passed, 2 skipped in 32.06s`).

### 4f. `verify_language.py` — F-14's two reds, unchanged

```
2 FAILURE(S): ['character: the token is `MOTION_STEPS` and it governs FIVE events, ...',
               'prism: rail renders IFF the language declares layout=rail']

== THE GATE ITSELF: settle headroom
  [PASS] settle() keeps headroom under its bound (a gate near its limit is a gate about to rot)
         worst 4 of 40 over 155 captures
```

**Exactly F-14's two, and the pin moved neither** — the spec's §4 asked this question in advance
("unless the AC-4 pin happens to move one, which the packet then says out loud") and the answer is no.
Both are the reds `kits-learn-3` measured on the pre-batch tree; they stay recorded, not fixed.

The last line is `verify_language.py`'s OWN settle, not this file's, and it is worth reading beside
inc20: that gate uses 4 of its 40 iterations at worst over 155 captures, because it settles a single
themed board rather than a sweep. The capture's settle is the one that meets F-16.

### 4g. A THIRD determinism defect, found at the close: `verify_language.py` rewrites the fixture

Running the language harness left a tracked file dirty:

```
$ git diff -- prototypes/out/_fixture_late.json
-{"phases": [...], "projects": [{"name": "Website Redesign", ..., "start_date": "2026-07-14", "due_date": "2026-08-17", ...
+{"phases": [...], "projects": [{"name": "Website Redesign", ..., "start_date": "2026-08-16", "due_date": "2026-09-19", ...
```

`prototypes/verify_language.py:11592` **overwrites the capture's fixture**. It derives two probe fixtures
from a seed and writes them to `prototypes/out/_fixture_late.json` and `_fixture_calm.json`, with the
dates taken relative to `date.today()` — so the shift is exactly **+33 days**, which is
`2026-09-05 − 2026-08-03`, today minus `FROZEN`.

**This is the same defect family as §1 and it is worse:** §1 moved one signal cell, this moves the DATA.
Every days-left value, every overdue count and every severity in all 22 frames is a function of this
file, and a tool the batch's own §4 tells you to run rewrites it. The symptom is already recorded in
`export_to_skill.py:copy_captures`'s docstring — "`prototypes/out/_fixture_late.json` was edited after the
sweep that produced them, and every board frame in the skill now differs from a fresh sweep of unmodified
code" — but the culprit was never named. It is named now.

**What was done about it here, exactly:** the rewritten file was copied to
`prototypes/out/_fixture_late_REWRITTEN_BY_VERIFY.json.bak` (gitignored, so nothing was lost), the
tracked file was restored with `git checkout -- prototypes/out/_fixture_late.json`, and the sweep was run
again. `git status --short -- prototypes/gallery/` then showed every frame **staged-modified and
working-tree clean** — i.e. a fresh sweep off HEAD's fixture reproduces the 22 frames this increment
commits, byte for byte. That is the proof the re-bake was taken before the rewrite and is unaffected.

**Not fixed.** `verify_language.py` is a declared non-goal of this batch (§5 of the spec), the two probe
fixtures exist for laws the standard seed genuinely cannot prove, and the cure — write them to a private
path, or restore after — is a change to that harness's contract. Filed as **F-17**.

---

## 5. Risks

- **The capture writes to the fixture's mtime.** Metadata only, idempotent, and to a file the capture
  already owns — but it is a side effect where there was none, and a read-only checkout would now fail
  the sweep with a `PermissionError` instead of producing wrong art. That is the better failure, and it
  is a new one.
- **`FIXTURE_AGE_S` is a free parameter.** 450 s was chosen for the int-boundary reason in §2, not from
  the domain; the frames now say "7 min since save" about a fixture that has no save time at all. That
  is honest for a synthetic fixture and it is still a number someone picked.
- **Two published sheets were wrong and nobody noticed for eleven passes.** The missing `invalid` row was
  found by re-baking, not by a check. Nothing in the suite asserts that a component sheet contains every
  state its registry derives — `tests/test_components.py` asserts the KIT, and the FRAME is a separate
  artefact. That gap is still open after this increment.
- **F-16 makes any re-bake a retry loop.** One sweep in ten fails loud. Fine for a human at a terminal,
  and a trap for anything that automates the sweep without checking the return code.
- **F-17 (§4g) means the ORDER of this batch's own validation strategy was load-bearing.** The re-bake
  ran before `verify_language.py`; had it run after, these 22 frames would carry a fixture 33 days out
  from the one in git and nothing would have said so. That is luck, not process.

---

## 6. Pending

- **F-16 — the columns-branch card wedge** (inc20 §5). Untouched here; it is `kanban.py`'s.
- **F-17 (new) — `verify_language.py:11592` overwrites `prototypes/out/_fixture_late.json`**, relative to
  `date.today()`, so running the language harness invalidates the committed frames (§4g). Restored and
  proved reproducible here; not fixed, and it defeats the same contract AC-4 was written to protect.
- **F-14 — `verify_language.py`'s two pre-existing reds.** Recorded, not fixed, as the spec's §4 said
  they would be. The mtime pin did **not** move either of them: see §4f.
- **F-15** — untouched, still one observation old.
- **No check asserts that a published component sheet carries every derived state** (§5). That is the
  hole through which darkside's and solari's `invalid` row fell.
- **`FIXTURE_AGE_S`** is now a second constant that the frames depend on, alongside `FROZEN`. Both are
  documented at their definitions; neither is asserted anywhere but in the new test.

---

## 7. Suggested next task

**F-16.** It is the only thing standing between this sweep and a command that always finishes: a
`TaskCard` in a column that permanently holds a paint composed at a narrower seat, four at a time, one
sweep in ten, measured stale for 19.5 s. `on_mount`'s `call_after_refresh(self.render_card)` and
`on_resize` are both meant to correct it and neither does — and the probe that proves it
(`race_probe.py`, plus the past-the-bound loop in inc20 §5) is already written.

---

## Evidence checklist

- [x] **Tests/type checks/lint pass** — `1 failed, 685 passed, 2 skipped in 33.49s` (§4e), 682 baseline
      + 4 new; the one failure is the documented env-dependent clipboard test. `verify_language.py`
      re-run at §4f.
- [x] **No secrets in code or output** — the pin stamps `prototypes/out/_fixture_late.json` only, inside
      `freeze_clock()`'s existing repointing away from `~/.taskboard/board.json` (§2). `test_no_live_board`
      and `test_privacy_sweep` green.
- [x] **No destructive commands run without approval** — no `rm`, no terminal process killed, no force,
      no push without the operator's standing instruction for this worktree. The only writes outside the
      scratch yard are the 44 gallery files this increment exists to re-bake and the two source files.
- [x] **File count within cap** — 2 source files; the 44 re-baked gallery artefacts are data produced by
      the documented command, named frame by frame in §4c.
- [x] **Review packet attached** — this document.
