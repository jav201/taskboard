# Increment 24 — the language harness stops writing the capture's fixture (F-17 closed)

**Batch:** `harness-hygiene` · **AC-1, AC-2** · `inc21.md` §4g and §6
**Files:** `prototypes/verify_language.py`, `tests/test_no_live_board.py` — **2 source files**.

**Two different artefacts wore one filename. They do not any more, and the 22 committed frames now
reproduce byte-for-byte after the language harness has run — which is exactly what they could not do
before.**

---

## 1. The defect, measured rather than inherited

`prototypes/verify_language.py:11592` derived a probe fixture from the standard seed and wrote it to
`prototypes/out/_fixture_late.json`, with its dates taken relative to `date.today()`.

That path is **the one name under `prototypes/out/` that `.gitignore` names back in**:

```
prototypes/out/*
!prototypes/out/_fixture_late.json          <- the capture's committed fixture
!prototypes/out/kanban-*.svg
```

It is the fixture `capture_languages.py:143` sweeps all 22 frames from, and the one
`verify_ink.py`, `verify_variants.py`, `verify_widget.py`, `capture.py` and two tests read. So running
the language harness re-dated the art's input, and every frame in `prototypes/gallery/` stopped
reproducing.

**Reproduced at HEAD before any edit**, not taken on `inc21.md`'s word:

```
$ git status --porcelain prototypes/out/_fixture_late.json     # clean
$ python -X utf8 prototypes/verify_language.py                 # 10854 PASS, 2 FAIL (F-14)
$ git status --porcelain
 M prototypes/out/_fixture_late.json
```

and the diff, task by task rather than "the file changed":

```
tasks differing: 12 of 16
  Design homepage mockups   ('2026-08-03', 'Doing',   False) -> ('2026-09-05', 'Doing',   False)
  Fix checkout 500 error    ('2026-08-01', 'Backlog', True)  -> ('2026-09-03', 'Backlog', True)
  Optimize image assets     ('2026-08-09', 'Doing',   False) -> ('2026-09-11', 'Doing',   False)
  ...
```

**+33 days on every one**, which is `date.today()` − `capture_languages.FROZEN` = `2026-09-05` −
`2026-08-03`. `inc21.md` §4g measured the same number and named the culprit; this is that measurement
repeated at this HEAD so the fix has a before.

### 1a. And the committed fixture is this harness's own output, which nobody had said

`phase` and `blocked` in the tracked file already carry the derivation this function performs —
`Fix checkout 500 error` sits in `Backlog` with `blocked: True`, which is
`t["phase"] = "Backlog"; t["blocked"] = (i == 0)` at line 11603, not anything the seed produces. The
committed fixture **is** a `verify_language.py` run, frozen on the day `FROZEN` names.

That is the finding under the finding: the file was never a designed input. It is a byproduct that was
committed once, then kept being overwritten by the thing that produced it. Its bytes are unchanged here —
what changes is that it now has **no writer at all**.

---

## 2. The decision: a private path, not a frozen clock

Both cures were on the table (`inc21.md` §4g named them). The choice is the private path.

- **Pinning `date.today()` through `freeze_clock()`** would make the write *idempotent* and leave the
  **collision** in place. The harness would still own a tracked file it has no business owning, one edit
  to either concept away from the same defect — and the next person to add a probe fixture would land in
  the same trap with no sign that it is one. It also drags `freeze_clock()` — which rebinds `datetime`
  and `date` in every imported module, repoints `default_board_path` and stamps an mtime — across
  **10854 checks that were all measured against a live clock**, to fix a filename. That is a change to
  this harness's contract, in a batch whose whole point is that harnesses should not have surprising
  contracts.
- **The private path** says the true thing: these two files are *probes*, rebuilt every run, read by
  nothing else. Probes belong in the scratch yard under names nothing else reads.

```python
fl = W / "prototypes" / "out" / "_verify_late.json"      # was _fixture_late.json
fc = W / "prototypes" / "out" / "_verify_calm.json"      # was _fixture_calm.json
```

`_fixture_calm.json` was renamed too, and it is not padding. It is created by the same three lines as its
twin, it is what `PENDING.md` records someone reaching for from outside, and leaving one of a pair
`_fixture_*` while the other is `_verify_*` hides the very distinction the fix exists to draw. Its two
mentions in this file's comments moved with it. Neither new name is negated in `.gitignore`, so both fall
under `prototypes/out/*` and cannot be staged — asserted by `tests/test_scratch_cannot_be_committed.py`,
which is green in §4d.

**`.gitignore` is untouched.** `_fixture_late.json` must stay committable and stay committed; only its
writer goes away.

---

## 3. The guard, and why it is a `git status` and not a hash

`tests/test_no_live_board.py::test_the_fixture_is_the_bytes_git_carries_not_the_bytes_a_harness_left`.

That file already asserts the fixture is *tracked* and that its contents are *synthetic*. What was
missing is the law that actually broke: **the working tree must not drift from the index.** A hash pinned
in the test would also go red the day someone deliberately re-bakes the fixture and commits it — a
legitimate act no law here should refuse. `git status --porcelain` on that one path answers the real
question and nothing else, and it catches **any** future writer, not just the one that was found.

It is cheap (a `git status` on one path, inside a file that already shells out to `git ls-files`) and it
fires at the end of the very suite run that follows a harness run.

---

## 4. Test results

### 4a. AC-1 — the observable

```
$ python -X utf8 prototypes/verify_language.py        # full run, 10854 PASS
$ git status --porcelain -- prototypes/out/_fixture_late.json
(no output)

$ ls -la prototypes/out/_verify_*.json
-rw-r--r--  5033  Sep  5 16:56  prototypes/out/_verify_calm.json
-rw-r--r--  5036  Sep  5 16:56  prototypes/out/_verify_late.json
```

The harness ran to completion, wrote its two probes, and left the tracked fixture alone. The check count
is **10854 PASS, unchanged from the baseline run** — the rename moved a path, not a law.

### 4b. AC-2 — the 22 frames still reproduce, AFTER the harness has run

`python -X utf8 prototypes/race_probe.py --cross 3 --engine shipped`, run against the tree the harness had
just finished on. Three fresh interpreters, three full sweeps into temporary directories, nothing written
to `prototypes/gallery/`:

```
CROSS-PROCESS DRIFT: 0/22 frames over 3 sweeps -> []
sweeps that are non-modal on >=1 frame: 0/3 []
PAIRWISE DISAGREEMENT: 0/3 pairs = 0.0 %
```

and each swept grid hashed against the **committed** frame, which is the half `--cross` does not do on its
own (it compares sweeps to each other):

```
  MATCH  board_naught.txt        committed 5a1d2ef3fad9  swept ['5a1d2ef3fad9']
  MATCH  board_corgi.txt         committed f062c4cc8414  swept ['f062c4cc8414']
  MATCH  board_instrument.txt    committed ed09ad3678a5  swept ['ed09ad3678a5']
  MATCH  board_swiss.txt         committed eb1f4d87b34c  swept ['eb1f4d87b34c']
  MATCH  board_industrial.txt    committed 0182fbd7cdb1  swept ['0182fbd7cdb1']
  MATCH  board_nord.txt          committed b6a12c0eec2e  swept ['b6a12c0eec2e']
  MATCH  board_darkside.txt      committed 74d57555a62f  swept ['74d57555a62f']
  MATCH  board_prism.txt         committed d45582ef5a51  swept ['d45582ef5a51']
  MATCH  board_ledger.txt        committed e03fb54b910d  swept ['e03fb54b910d']
  MATCH  board_solari.txt        committed 799edff293b5  swept ['799edff293b5']
  MATCH  board_blueprint.txt     committed 3f65e538325a  swept ['3f65e538325a']
  MATCH  gallery_naught.txt      committed 0c0902a0df4c  swept ['0c0902a0df4c']
  MATCH  gallery_corgi.txt       committed f96cdd5469ea  swept ['f96cdd5469ea']
  MATCH  gallery_instrument.txt  committed 6d68206da412  swept ['6d68206da412']
  MATCH  gallery_swiss.txt       committed 9c87b7599ce5  swept ['9c87b7599ce5']
  MATCH  gallery_industrial.txt  committed 76ab454c72a4  swept ['76ab454c72a4']
  MATCH  gallery_nord.txt        committed 06984a8dcc8f  swept ['06984a8dcc8f']
  MATCH  gallery_darkside.txt    committed 30c0b9682fd9  swept ['30c0b9682fd9']
  MATCH  gallery_prism.txt       committed 0f2b5254cfb0  swept ['0f2b5254cfb0']
  MATCH  gallery_ledger.txt      committed 57819721f84c  swept ['57819721f84c']
  MATCH  gallery_solari.txt      committed a544c6df77b0  swept ['a544c6df77b0']
  MATCH  gallery_blueprint.txt   committed 3e5e9e26463b  swept ['3e5e9e26463b']

AC-2: 22/22 frames reproduce byte-for-byte across 3 fresh sweeps; 0 moved
```

**Nothing was re-baked.** `prototypes/gallery/` was never opened for write, and `export_to_skill.py` was
not run — no carried frame moved.

### 4c. The guard, red then green

Red — the fixture put back to the bytes the *pre-fix* harness left on this machine:

```
$ cp prototypes/out/_hh_late_AFTER_VL.json prototypes/out/_fixture_late.json
$ python -X utf8 -m pytest -q tests/test_no_live_board.py

E  AssertionError: _fixture_late.json differs from the bytes git carries
   ('M prototypes/out/_fixture_late.json'). Every frame in prototypes/gallery/ was
   swept from the committed bytes, so a sweep taken now would not reproduce them.
   Restore with `git checkout -- prototypes/out/_fixture_late.json` and find what
   wrote it -- F-17 was prototypes/verify_language.py

1 failed, 9 passed in 1.10s
```

Green — restored:

```
$ git checkout -- prototypes/out/_fixture_late.json
$ python -X utf8 -m pytest -q tests/test_no_live_board.py
10 passed in 1.04s
```

**The red arm is the real defect's real bytes**, not a synthetic edit: that file is a copy taken off this
tree immediately after the pre-fix harness run in §1.

### 4d. Suite

```
python -X utf8 -m pytest -q
693 passed, 2 skipped, 4 warnings in 31.39s
```

**692 baseline + 1 new test.** `test_win_clipboard_roundtrip` passed on this run; it is the documented
env-dependent one and is green or red with the clipboard, not with this change.
`tests/test_no_live_board.py` and `tests/test_privacy_sweep.py` — the standing privacy guards — are inside
that number, and `tests/test_scratch_cannot_be_committed.py` confirms the two new probe names stay
un-stageable.

---

## 5. Risks

- **The new guard is red for a legitimate uncommitted edit of the fixture.** Anyone deliberately re-baking
  `_fixture_late.json` sees a red suite until they commit it. That is the intended shape — the frames are
  stale in exactly that window — but it is a test that talks about the working tree, which is unusual, and
  it will surprise someone.
- **It needs a git checkout to answer.** In a source export with no `.git`, `git status` fails and the test
  errors on `r.returncode == 0` rather than skipping. Every other law in this file already shells out to
  git, so the exposure is not new, but it is now on one more test.
- **Nothing stops the NEXT harness from writing a tracked path.** The guard catches the symptom on the
  next suite run; it does not make the scratch yard write-only-to-ignored-names. A rule of that shape
  would need `.gitignore`'s negation list to be readable by the writers, which no script does today.
- **The two renamed probe files are recreated on every run**, so an old `_fixture_calm.json` from before
  this increment is now orphaned scratch that nothing rewrites. Harmless (the yard is ignored) and worth
  knowing when reading a stale file's mtime.

## 6. Pending

- **F-14** — `verify_language.py`'s two reds, still exactly two after this run. inc25.
- **F-15** — the lattice flake. inc26.
- **F-8** — `--surface` still has to be run plain and alone. Untouched.
- **`export_to_skill.py:copy_captures`'s docstring still describes the symptom in the present tense**
  ("`_fixture_late.json` was edited after the sweep that produced them, and every board frame in the skill
  now differs from a fresh sweep"). It is now history rather than a live hazard. Not edited here: it is a
  third file, and §4b is the measurement that would justify rewriting it.
- **The committed fixture has no writer now** (§1a). If it ever needs regenerating, nothing in the repo
  says how — the code that produced it has been pointed elsewhere. Recorded, not solved.

## 7. Suggested next task

**inc25 · F-14.** The sweep is green apart from two checks that have been carried as "pre-existing,
unchanged" through six packets without anyone saying whether the check or the kit is wrong.

---

## Evidence checklist

- [x] **Tests/type checks/lint pass** — `693 passed, 2 skipped in 31.39s` (§4d), 692 baseline + 1 new;
      `verify_language.py` re-run in full at §4a (10854 PASS, and F-14's two reds unchanged, which is
      inc25's).
- [x] **No secrets in code or output** — the change moves a WRITE off a tracked path onto the gitignored
      scratch yard: strictly less exposure. `freeze_clock()`'s repointing away from
      `~/.taskboard/board.json` is untouched; `test_no_live_board.py` (10 passed, §4c) and
      `test_privacy_sweep.py` green inside §4d.
- [x] **No destructive commands run without approval** — no `rm`, no force, no terminal process killed.
      The only writes are the two source files, the two gitignored probe fixtures the harness rebuilds,
      and scratch logs under `prototypes/out/`. `git checkout --` was used once, on the one file this
      increment exists to protect, to restore it from the index after the red arm.
- [x] **File count within cap** — 2 source files, plus this packet, the new spec and the archived
      predecessor: 5.
- [x] **Review packet attached** — this document.
