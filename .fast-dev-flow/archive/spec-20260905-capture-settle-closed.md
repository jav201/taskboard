# Quick Spec — taskboard · batch "capture-settle" (F-1 closed, and the frames made reproducible)

**Batch:** `2026-09-05-fastflow-11` · **Base:** worktree `kanban-variants`, HEAD `16792b5` (the race
probe), pushed. Predecessor `kits-learn-3` closed 2026-09-04, §8 filled, archived verbatim to
`archive/spec-20260905-kits-learn-3-closed.md`. Language: English. Increments continue the worktree's
single sequence: **inc20 … inc21**.

**Input:** `.fast-dev-flow/03-increments/race-probe.md` — the instrument (`prototypes/race_probe.py`),
the measurement, and the PROPOSAL it deliberately did not apply. The operator has approved the
proposal. This batch applies it and files the second finding the probe turned up.

The input in two lines:

1. **F-1 is a settle defect and it is measured.** `prototypes/capture_languages.py:settle()` implements
   condition B only (three identical composited reads). Across 30 fresh-interpreter sweeps that leaves
   **6 of 22 frames drifting** and **58.9 % pairwise disagreement** — the rate the operator actually
   sees, because `main()`'s determinism check compares one sweep against one control sweep. The probe's
   §5 diffs say what drifts: the **hero band**, which no condition was watching, and the DOING column's
   **stale card bake**, which condition C exists to catch and which this file never had.
2. **The committed frames cannot be reproduced on a fresh checkout.** `taskboard/engine.py:sig_board_file`
   ages the board file with `p.stat().st_mtime`. `freeze_clock()` pins `time.time()`; it cannot pin a
   file's mtime, which git does not carry. The eleven committed `board_*.txt` were taken at `f -98` and
   this tree now renders `f -46982`, deterministically, in every run.

---

## 1. Objective (1 line)

Make one sweep of `capture_languages.py` produce the same 22 grids as any other sweep, on any checkout —
by settling on a frame the app has actually finished composing, and by pinning the last input to the
capture that a clone does not carry.

---

## 2. User stories

- As **anyone rebuilding the gallery**, I want two sweeps of unchanged code to agree, so that
  `main()`'s determinism check means "the capture is a picture of a design" rather than "the capture is a
  picture of a moment" — which is the claim the file's own header already makes and could not keep.
- As **anyone who clones this repo**, I want `prototypes/gallery/*.txt` to be the frames my own sweep
  produces, so that the house rule "the `.txt` is the art" survives contact with a fresh checkout.
- As **the next reader of `capture_languages.py`**, I want its docstrings to state the settle it HAS.
  Two long paragraphs currently argue that condition A is deliberately not implemented; after inc20 they
  would be arguing against the code beneath them, which is worse than no comment at all.

---

## 3. Acceptance criteria (observable)

- [x] **AC-1 · inc20 · the settle waits for a composed frame.** `settle()` requires **eight** identical
  composited reads (was three) **and** two widget conditions before it signs off:
  **A** — every content widget the compositor says it is drawing carries ink inside its own clipped area,
  where "content widget" is the four classes `KanbanBoard.build()` mounts (`kb-card`, `col-head`,
  `kb-empty`, `kb-detail`) **plus `#hero`**, the band race-probe §5 named as unwatched;
  **C** — no `TaskCard` holds a paint composed at a seat it no longer has, asked as a shadow render with
  `update` intercepted so the check measures and never repairs.
  **Measured, not asserted:** `race_probe.py --cross 30 --engine shipped` — the arm that runs the
  shipped file — must report **0 of 22 frames drifting** and **0.0 % pairwise disagreement**, against the
  6/22 and 58.9 % of the input. The sweep-time cost is **stated**, not hidden.
- [x] **AC-2 · inc20 · the two docstrings state the settle that exists.** The module header's
  "SETTLE IS WEAKER HERE THAN IN THE HARNESS" paragraph and `settle()`'s "Condition A … is deliberately
  NOT reimplemented here" paragraph are rewritten to state the new design and to cite
  `.fast-dev-flow/03-increments/race-probe.md` for the numbers. A third block — the `TEXTUAL_ANIMATIONS`
  comment's "filed as F-1, open, and NOT fixed here" — is in the same file and becomes false at inc20;
  it is corrected in the same edit and named in the packet.
- [x] **AC-3 · inc20 · the hero wait has a test, and the test has teeth.** `tests/test_capture_settle.py`
  drives a fixture app whose hero band fills through `call_after_refresh` several refresh cycles late.
  Two assertions, and the first is what stops the second being vacuous: **(a)** the OLD condition
  (B alone, three reads — quoted in the test) signs the frame off with the hero band **blank**;
  **(b)** `CL.settle` returns a frame whose hero band carries ink. Red-then-green is pasted in the packet
  from a real run against the pre-change file, not narrated.
- [x] **AC-4 · inc21 · the capture no longer reads a timestamp git does not carry.** `sig_board_file`'s
  input is pinned for the capture, the mechanism is named with its reason, and a fresh checkout of this
  worktree reproduces the committed frames. Observable: two sweeps taken at two different fixture mtimes
  produce byte-identical `board_*.txt`.
- [x] **AC-5 · inc21 · the 22 frames are re-baked and every mover is named.** `prototypes/gallery/`'s 22
  board/gallery frames are re-swept with the new settle and the pinned signature and committed. The
  packet lists **which frames changed and why** — the two predicted causes are the hero/load-bar seats
  (AC-1) and the `-98` → pinned board-file signal (AC-4). A frame that moved for a third reason is a
  finding, not a footnote.
- [x] **AC-6 · nothing else moves.** The 11 `surface_*.txt` frames stay byte-identical to
  `.fast-dev-flow/baseline-kits2/`. The surface sweep is run **plain and alone** (F-8). The 30 component
  frames under `prototypes/components/` are untouched — no increment here reaches them.

---

## 4. Validation strategy

`python -X utf8 -m pytest -q` in this worktree is the gate, run **after every increment**. Baseline
measured at Phase A, before any edit: **`1 failed, 681 passed, 2 skipped, 4 warnings in 32.06s`** — 682,
the recorded baseline, whose one failure is the documented environment-dependent
`tests/test_app.py::test_win_clipboard_roundtrip` (PENDING #22, `RUN.md`).

`python -X utf8 prototypes/race_probe.py --cross 30 --engine shipped` is the gate for AC-1. It is the
only arm that can express F-1: the defect is a disagreement BETWEEN PROCESSES, and the probe's own §4a
shows every in-process arm at 0/30. ~4.5 minutes.

`python prototypes/capture_languages.py` (the full documented command, including its own cross-process
determinism check) is what re-bakes the frames for AC-5.

`python prototypes/capture_languages.py --surface`, **plain and alone** (F-8), for AC-6.

`python -X utf8 prototypes/verify_language.py` is run at the close. **F-14's two pre-existing reds stay
recorded, not fixed** — unless the AC-4 pin happens to move one, which the packet then says out loud.

Headless stdout goes **to a file, never to `DEVNULL`** (L-42). No terminal process is ever killed.
Git: each increment is committed in this worktree and the batch is pushed at the close — the operator
has been pushing this worktree.

---

## 5. Non-goals (what is OUT)

- **`verify_language.py`.** Its settle already has A, B and C and is not the defect. F-14's two reds are
  not this batch's to fix; fixing a sweep while changing what it measures is how a green run stops
  meaning anything.
- **F-15.** One observation old, untouched, still unexplained.
- **The `sig_board_file` signal as shipped.** AC-4 pins what the CAPTURE feeds it. It does not change
  what the signal means for a running app — a capture photographs the shipping code, which is the rule
  `freeze_clock()`'s own docstring already states.
- **Committing `prototypes/race_probe.py` differently, or extending it.** It is the instrument, already
  committed at `16792b5`, and it is used here as-is so the before and after numbers come from one tool.
- **`prototypes/components/`, the skill's prose, and any consumer repo.** Untouched. If the re-bake moves
  a frame the skill carries, `export_to_skill.py` is run and its output reported — the skill is never
  hand-edited (`kits-learn-3` §5, unchanged).

---

## 6. Detected security flags

One flag fires, and it is the one AC-4 exists to close: `sig_board_file` **stats a path** and prints its
size and save-time into a published frame. `freeze_clock()` already repoints `default_board_path` at the
synthetic fixture for exactly this reason (the capture must never print the size or save-time of the
operator's real board). AC-4 works inside that repointing and must not widen it: whatever it pins, it
pins about `prototypes/out/_fixture_late.json`, never about `~/.taskboard/board.json`.

No secrets, no network, no new dependency, no destructive command. `tests/test_no_live_board.py` and
`tests/test_privacy_sweep.py` are the standing guards and are part of the suite gate above.

---

## 7. Batch status

| | |
| --- | --- |
| Phase A (spec) | **done** — this file; predecessor archived |
| Phase B (implement) | inc20 · the settle · AC-1, AC-2, AC-3 — **done** (`7462881`) |
| | inc21 · reproducible frames · AC-4, AC-5, AC-6 — **done** |
| Phase C (close) | §8 — **done** |
| Notes | **<= 5 files per increment, one agent, sequential.** The 22 re-baked frames of inc21 are data, not source: inc21 touches **one** source file. |

---

## 8. Close (filled in phase C)

### What changed

`prototypes/capture_languages.py`'s `settle()` implemented condition B alone — three identical
composited reads — and a widget waiting on a deferred re-render produces a genuinely static frame while
it waits. It now asks three conditions: **A** (every content widget the compositor is drawing carries ink
in its own clipped area — the four classes `build()` mounts **plus `#hero`**), **B** (eight identical
reads, was three), **C** (no drawn `TaskCard` holds a paint composed at a seat it no longer has, asked as
a shadow render that measures and never repairs). And `freeze_clock()` now pins the one input it had left
unpinned: the fixture's own mtime, which `sig_board_file` subtracts from the frozen clock and which git
does not carry.

The 22 committed frames were re-baked through the documented command and every mover is named.

### How it was tested

- `python -X utf8 prototypes/race_probe.py --cross 30 --engine shipped` — 30 whole sweeps in 30 fresh
  interpreters, all 22 frames diffed. **0/22 drifting, 0.0 % pairwise** (was 6/22 and 58.9 %).
- `python prototypes/capture_languages.py` — clean, and its own cross-process determinism check reported
  **22 grids identical across two PROCESSES**.
- Two sweeps taken at fixture mtimes 99 days apart: **22 frames, 0 differ**.
- `python prototypes/capture_languages.py --surface`, plain and alone (F-8): the 11 surface frames are
  **byte-identical to HEAD**.
- `python -X utf8 prototypes/verify_language.py`: **2 failures, F-14's two, unmoved.**
- `python -X utf8 -m pytest -q`: `1 failed, 685 passed, 2 skipped in 33.49s` — 682 baseline + 4 new; the
  one failure is the documented environment-dependent clipboard test.

### Evidence per AC

| AC | verdict | evidence |
| --- | --- | --- |
| AC-1 · the settle waits for a composed frame | **met** | `inc20.md` §4a — 0/22 frames, 0/351 pairs, against 6/22 and 58.9 % |
| AC-2 · the two docstrings state the settle that exists | **met** | `inc20.md` §1; the third block (`TEXTUAL_ANIMATIONS`'s "NOT fixed here") corrected in the same edit and named |
| AC-3 · the hero wait has a test with teeth | **met** | `inc20.md` §4c — 2 failed / 1 passed against HEAD, 3 passed after; the one that passes both is the anti-vacuous guard |
| AC-4 · the capture no longer reads a checkout timestamp | **met** | `inc21.md` §4a — 22 frames identical across two mtimes; `test_the_board_file_signal_does_not_read_the_checkout_clock` |
| AC-5 · the 22 frames re-baked, every mover named | **met** | `inc21.md` §4c — 11 boards on the signal cell, 11 sheets on the scroll-bar thumb, 2 of them also gaining a row |
| AC-6 · nothing else moves | **met** | `inc21.md` §4d — `git status` on `surface_*` is empty; the two deltas vs `baseline-kits2` already differed at HEAD |

### Open risks / pending

- **F-16 (new, and the batch's own finding): a `TaskCard` in a column can permanently hold a paint
  composed at a narrower seat.** Four cards at once, COLUMNS branch only, ~10 % of sweeps, measured still
  stale **640 iterations / 19.5 s** past the settle bound. `on_mount`'s `call_after_refresh` and
  `on_resize` are both supposed to correct it and neither does. The old settle WROTE that frame — it is 2
  of F-1's 6 drifting frames — and the new one fails loud instead. It belongs to
  `prototypes/widget_slice/kanban.py` and it is the next task.
- **Two published component sheets were missing a control state and nothing caught it.** `gallery_darkside`
  and `gallery_solari` had no `invalid` row — the sixth derived state `kits-learn-3` shipped — because the
  old settle signed off before the sheet finished composing. Nothing in the suite asserts that a published
  FRAME carries every state its registry derives; `tests/test_components.py` asserts the KIT. That gap is
  still open.
- **The documented sweep now fails loud about one run in ten** (`main()` runs two sweeps, so ~19 % per
  invocation). Better than the 58.9 % silent failure it replaces — nothing wrong is written — but new.
- **Condition A on `#hero` is an ink check, not a seat check.** A hero composed at a stale seat that still
  carries ink would pass it; there is no shadow-render oracle for the hero, because `Hero.show` needs data
  only the app has. What covers it today is the eight reads — 30 sweeps of evidence, not proof.
- **`FIXTURE_AGE_S` is a second constant the frames depend on**, alongside `FROZEN`, and the capture now
  writes metadata to the fixture. A read-only checkout would fail the sweep where it used to produce wrong
  art.
- **F-17 (new, found at the close): `verify_language.py:11592` OVERWRITES `prototypes/out/_fixture_late.json`.**
  It derives its two probe fixtures relative to `date.today()` and writes them over the capture's fixture,
  so running the language harness moves every date in the 22 frames — measured today at +33 days
  (`2026-09-05 − FROZEN`). The symptom is already in `export_to_skill.py`'s own docstring; the culprit was
  not. Restored from HEAD, the re-bake proved reproducible against it, and it is **not fixed** — the
  harness is a declared non-goal. It defeats the same contract AC-4 exists to protect, and it means this
  batch's validation ORDER (re-bake, then verify) was load-bearing rather than deliberate.
- **F-14** — `verify_language.py`'s two pre-existing reds, re-measured and unmoved. **F-15** — untouched.
- **F-8** — obeyed, not fixed.

### Security flags — handling

The one flag §6 named is closed rather than widened. The mtime pin stamps
`prototypes/out/_fixture_late.json` and nothing else, inside `freeze_clock()`'s existing repointing away
from `~/.taskboard/board.json`; `sig_board_file` is unchanged, so the shipped app still reports the real
board's age for its real user. `tests/test_no_live_board.py` and `tests/test_privacy_sweep.py` green. No
secrets, no network, no new dependency, no destructive command, no terminal process killed, every headless
run captured to a file rather than to `DEVNULL` (L-42) — with `--surface` run plain and alone, as F-8
requires.
