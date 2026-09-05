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
| Phase B (implement) | inc24 · F-17 **closed** · inc25 · F-14 **closed** · inc26 · F-15 **bounded and detected, not reproduced** |
| Phase C (close) | §8 — **done** |
| Notes | **3 source files, one agent.** `prototypes/verify_language.py` (inc24 + inc25), `tests/test_no_live_board.py` (inc24), `tests/test_surface.py` (inc26); plus this spec, the archived predecessor and three packets. |

---

## 8. Close (filled in phase C)

### What changed

**Two of the three findings are closed. The third is not, and the packet says so in its title.**

**F-17 — closed.** `verify_language.py` derived a probe fixture straight onto
`prototypes/out/_fixture_late.json`, the one name under `prototypes/out/` that `.gitignore` names back in
and the fixture all 22 committed frames were swept from. Its dates came from `date.today()`, so running
the language harness re-dated the art's input — measured at +33 days on 12 of 16 tasks, which is
`date.today()` − `FROZEN`. The two derived fixtures are probes and now say so (`_verify_late.json`,
`_verify_calm.json`, both ignored). Not a frozen clock: pinning the date would have made the write
idempotent and left the name collision standing, and would have dragged `freeze_clock()` across 10854
checks measured against a live clock to fix a filename. **And the finding under the finding:** the tracked
fixture's `phase`/`blocked` fields are this harness's own derivation, so the committed file was never a
designed input — it is a byproduct that was committed once and then kept being overwritten by the thing
that produced it. Its bytes are unchanged; it now has no writer at all.

**F-14 — closed, and both reds were the CHECK.** Neither kit was wrong, and both checks were wrong the
same way: a hand-typed literal standing for the language axis that never learned prism, the eleventh
language. `MOTION_STEPS` compared an eleven-key dict against a ten-key pin — every pinned value still
matched, and the failure was one extra key, printed with no detail at all, which is why it survived six
packets. The rail check asked all eleven languages for **darkside's** glyph while prism declares
`layout: rail` and draws its own heavier stroke — the "one class stands for the axis" defect the check's
own comment forbids, committed by the checker. Both commitments are argued at their definitions in
`taskboard/language.py` and both stand, so **that file was not touched**. The sweep now reports
`ALL PASSED`.

**F-15 — not reproduced, and not claimed as fixed.** 80 isolation runs, 27 full-suite runs and 4865
per-test evaluations, all green. What the increment established instead: the assertion is a pure function
of five theme tokens and a constant image; its failure map says the only state that reddens it is a
mutated token; and the assertion replayed against all nine commits from `kits-learn-2` to here is green
with identical tokens — so the red state has never existed in a commit. The only thing standing behind
"and no test leaks one" was a human reading eight `finally` blocks; an autouse fixture now asserts it at
every seat and errors on the **leaking** test rather than the distant victim. Two literal restores — the
one latent path to the symptom — were closed alongside. No tolerance was widened.

**F-18 — new, found by the same runs.** `tests/test_board_seat.py:205` samples the widget tree one
`pilot.pause()` after a resize and can catch both generations of `.col-head` — six heads where a board has
three. 1 red in 40 isolated runs, 1 in 27 full-suite runs. It is the test's observation point, not
inc23's repair. Recorded with its rate, not fixed.

### How it was tested

- `python -X utf8 prototypes/verify_language.py` — **`ALL PASSED`, 10857 PASS, 0 FAIL, exit 0**
  (baseline at Phase A: 10854 PASS, 2 FAIL; +3 checks, −2 failures, none deleted or suppressed).
- `git status --porcelain -- prototypes/out/_fixture_late.json` after that run: **empty**.
- `python -X utf8 prototypes/race_probe.py --cross 3 --engine shipped`: `0/22 frames drifting, 0.0 %
  pairwise`, and each swept grid hashed against the committed frame — **22/22 byte-identical**.
- Anti-vacuity probe for F-14: 7 arms; ARM 6 is the gain — same tree, same stray glyph, old check green
  and new check red.
- Anti-vacuity for the F-15 detector: a planted leak produces 1 error naming the culprit test and the
  drifted token, plus the 3 distant failures a reader would otherwise be left with.
- `python prototypes/capture_languages.py --surface`, **plain and alone** (F-8): 11 surfaces, no two
  identical, and `git status --porcelain -- prototypes/gallery/` **empty** — all 33 frames byte-identical
  to HEAD.
- `python -X utf8 -m pytest -q`: **693 passed, 2 skipped, 4 warnings in 31.18s** (692 baseline + 1 new
  test).

**No frame was re-baked** — no hash moved, `prototypes/gallery/` was never opened for write by this batch,
and `export_to_skill.py` was not run because no carried frame moved.

### Evidence per AC

| AC | verdict | evidence |
| --- | --- | --- |
| AC-1 · the sweep does not rewrite a tracked fixture | **met** | `inc24.md` §4a — empty `git status` after a full harness run; the cure and the rejected alternative argued in §2 |
| AC-2 · the 22 frames still reproduce byte-for-byte | **met** | `inc24.md` §4b — 22/22 MATCH against the committed hashes, 0/22 drift over 3 fresh sweeps |
| AC-3 · each red diagnosed to a verdict | **met** | `inc25.md` §2 and §3 — what each check asserts, what each kit renders, the deciding docstring quoted; both are check defects, `language.py` untouched |
| AC-4 · the sweep is green after | **met** | `inc25.md` §5a — `ALL PASSED`, 10857 PASS, 0 FAIL |
| AC-5 · F-15 reproduced or bounded | **met, as bounded** | `inc26.md` §2, §3, §4 — counts before and after, the failure map, the nine-commit replay, 4865 audited evaluations, the detector red-then-green. Not reproduced; no cause claimed; no tolerance widened |
| AC-6 · nothing else moves | **met** | suite 693/2; `--surface` plain and alone leaves all 33 frames byte-identical; nothing re-baked, nothing exported |

### Open risks / pending

- **F-18 (new)** — the `test_board_seat.py` observation-point race, with its rate. `inc26.md` §5 and §8.
- **F-8** — unchanged. `--surface` still has to be run plain and alone.
- **F-15 is closed without a cause.** If it returns, the new fixture will name the culprit — unless the
  mechanism was never a theme leak, in which case `inc26.md` §2's whole argument is wrong and the return
  will say so.
- **`RUN.md` is stale in two places**: "flake-free since the forty-sixth pass" (F-15 and F-18 both
  contradict it) and "`verify_language.py` … 2178 checks" against a run that now reports 10857.
- **`export_to_skill.py:copy_captures`'s docstring** still describes F-17's symptom in the present tense.
- **The committed fixture has no writer now.** If it ever needs regenerating, nothing in the repo says
  how. `inc24.md` §1a and §6.
- Each increment's own risk section: `inc24.md` §5, `inc25.md` §6, `inc26.md` §7.
