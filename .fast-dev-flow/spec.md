# Quick Spec — taskboard · batch "harness-hygiene" (three recorded findings, closed or dispositioned)

**Batch:** `2026-09-05-fastflow-14` · **Base:** worktree `kanban-variants`, HEAD `e3f1312` (inc23, the
board builds at the seat it is drawn at), pushed. Predecessor `push-paint` closed 2026-09-05, §8 filled,
archived verbatim to `archive/spec-20260905-push-paint-closed.md`. Language: English.
Increments continue the worktree's single sequence: **inc21 · inc22 · inc23 … inc24 · inc25 · inc26**.

**Input:** three findings this worktree recorded and ran around rather than closing —
`inc21.md` §4g and §6 (F-17), `inc14.md` §7 and `inc20.md` (F-14), `inc20.md` / `race-probe.md` §8 (F-15).

The input in three lines:

1. **F-17 — the language harness rewrites a tracked fixture.** `prototypes/verify_language.py:11592`
   writes `prototypes/out/_fixture_late.json`, dates taken relative to `date.today()`. That file is the
   fixture all 22 committed frames were swept from, so running the harness invalidates the art. It is why
   the last three specs say "`verify_language.py` is **not** run".
2. **F-14 — two reds nobody has diagnosed.** `character: the token is MOTION_STEPS …` and
   `prism: rail renders IFF the language declares layout=rail`, red at HEAD since `kits-learn-2`, carried
   forward in six packets as "pre-existing, unchanged". Nobody has said whether the CHECK is wrong or the
   KIT is.
3. **F-15 — one flake, one observation old.** `tests/test_surface.py::test_lattice_pixels_are_two_colours`
   went red once in six full-suite runs and has never been reproduced or explained.

---

## 1. Objective (1 line)

Close all three: stop the sweep rewriting a tracked fixture, diagnose F-14's two reds to a verdict with the
deciding commitment quoted, and reproduce F-15 or bound it with counts.

---

## 2. User stories

- As **anyone who clones this repo and re-sweeps**, I want the 22 frames to reproduce byte-for-byte no
  matter which harness I ran first, so that "the `.txt` is the art" survives contact with the toolbox.
- As **the next person reading a packet**, I want a carried finding to say *check wrong* or *kit wrong*
  with the evidence, because "2 FAILURE(S) — the two pre-existing ones, unchanged" repeated six times is a
  number being copied, not a fact being checked.
- As **anyone trusting the suite**, I want a named flake either reproduced and cured or bounded by a
  measured count, so a green run means something.

---

## 3. Acceptance criteria (observable)

- [ ] **AC-1 · inc24 · the sweep does not rewrite a tracked fixture.** After a full
  `python -X utf8 prototypes/verify_language.py`, `git status --porcelain prototypes/out/_fixture_late.json`
  is **empty**. The packet says which of the two cures (private gitignored path · pin the date through
  `freeze_clock()`) was taken and why the other was not.
- [ ] **AC-2 · inc24 · the 22 committed frames still reproduce byte-for-byte** after the harness has run —
  hashes compared against `prototypes/gallery/*.txt` at HEAD, all 22 named as matching or as moved.
- [ ] **AC-3 · inc25 · each of F-14's two reds is diagnosed to a verdict**: what the check asserts, what
  the kit renders, and the docstring or commitment that decides. A check defect is fixed in the harness; a
  kit defect is fixed in `taskboard/language.py` **only if ≤ 10 lines and its property test goes
  red-then-green**, else the disposition is recorded with the evidence.
- [ ] **AC-4 · inc25 · the sweep is green after** — tail pasted — or every remaining red is named with its
  reason.
- [ ] **AC-5 · inc26 · F-15 is reproduced or bounded.** 40 isolation runs and 10 full-suite runs, counts
  pasted before and after. If it flakes, what differs between a green and a red run is instrumented and
  the cause (or the assertion's false premise) fixed. **No tolerance is widened without a measured
  reason.**
- [ ] **AC-6 · nothing else moves.** Suite green (`python -X utf8 -m pytest -q`, 692 baseline). The
  `--surface` sweep run plain and alone leaves its 11 frames unchanged. No frame is re-baked unless a hash
  moves, and `export_to_skill.py` runs only if a carried frame moved.

---

## 4. Validation strategy

`python -X utf8 -m pytest -q` is the gate. Baseline at Phase A: **692 passed, 2 skipped**
(`push-paint` §8), plus the documented env-dependent `test_win_clipboard_roundtrip`.

`python -X utf8 prototypes/verify_language.py` is the gate for AC-1/AC-3/AC-4, and it is run in this batch
— it is this batch's subject. ~80 s. Its baseline at Phase A is measured, not inherited: **10854 PASS,
2 FAIL**, the two F-14 names, and `prototypes/out/_fixture_late.json` dirty afterwards (F-17 reproduced;
restored with `git checkout --`).

Headless stdout goes **to a file, never to `DEVNULL`** (L-42). `--surface` is run **plain and alone**
(F-8). No terminal process is ever killed. Git: committed per increment in this worktree and pushed at the
close.

---

## 5. Non-goals (what is OUT)

- **F-8 and F-16.** Untouched. F-8 still requires `--surface` plain and alone; F-16 is closed for
  `TaskCard` and `KanbanBoard` and its remaining surface is not this batch's.
- **Re-baking frames.** The 22 frames are re-swept only to PROVE they are unmoved. If a hash moves, the
  packet says which and why before anything is written.
- **`prototypes/components/`, the skill's prose, pulso, GBL and the course.** Untouched. The skill is
  never hand-edited; `export_to_skill.py` runs only if a carried frame moved.
- **Widening a tolerance to make F-15 green.** Explicitly forbidden by AC-5.

---

## 6. Detected security flags

None fires. The changes are a harness's private scratch path and a harness's own check literals; no
network, no new dependency, no destructive command, no secret. The one path change moves a WRITE off a
tracked file and onto the gitignored scratch yard — strictly less exposure. `freeze_clock()`'s repointing
of `default_board_path` away from `~/.taskboard/board.json` is untouched, and
`tests/test_no_live_board.py` / `tests/test_privacy_sweep.py` stay in the suite gate above.

---

## 7. Batch status

| | |
| --- | --- |
| Phase A (spec) | **done** — this file; predecessor archived verbatim |
| Phase B (implement) | inc24 · F-17 — **pending** · inc25 · F-14 — **pending** · inc26 · F-15 — **pending** |
| Phase C (close) | §8 — **pending** |
| Notes | **<= 5 files, one agent.** `prototypes/verify_language.py` (inc24 + inc25), plus whatever inc26's measurement earns, plus this spec, the archived predecessor and three packets. |

---

## 8. Close (filled in phase C)

_pending_
