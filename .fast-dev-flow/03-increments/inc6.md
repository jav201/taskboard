# Increment 6 — F-5: the documented sweep command runs green again

Batch `2026-09-04-fastflow-07` ("chrome-on-raster", F-4) · follow-up increment,
one file, requested by the coordinator after increment 5. Scope: *apply the F-5
fix, make `python prototypes\capture_languages.py` run again, record F-1's
count, confirm the 44 named frames, correct the header's animation claim.*
No git operations. `spec.md` §1–§7 untouched.

## 1. What changed

**F-5, and it was one line's worth of meaning rather than one line.** The
determinism check in `main()` read

    first = {p.name: p.read_text(...) for p in sorted(OUT.glob("*.txt"))}

— *every text capture in the output directory*. That stopped being this
sweep's output when the `surface` batch added a `--surface` entry point writing
`surface_*.txt` into the same directory. The control arm (`--sweep-to`) runs
`sweep()` alone and writes 22 files; the check demanded 33. So the DOCUMENTED
command died inside its own determinism check with a `FileNotFoundError` on
`surface_blueprint.txt` — a traceback that reads like a missing input and was
in fact the two arms sweeping different things.

The frames are now **named, not discovered**:

```
+#: the sheets `sweep()` writes for each language, in the order it writes them.
+#: This is the BOARD sweep's own output and nothing else -- the `--surface`
+#: entry point writes `surface_*` into the same directory, from a separate run,
+#: and the reproducibility check below must not confuse the two (F-5).
+#:
+#: It has to match the `write()` names in `sweep()`.  It is not derived from
+#: them because they are produced inside a Textual session that has to run to
+#: produce anything, and a check that had to sweep in order to learn what a
+#: sweep produces could not be used to decide whether the sweep was complete.
+#: A rename that forgets this constant fails LOUD on the next run -- `main()`
+#: reads these names directly, so a missing one raises there rather than
+#: quietly narrowing the check to the files that happen to exist.
+BOARD_SHEETS = ("board", "gallery")
+
+
+def board_frames() -> list[str]:
+    """Every `.txt` one `sweep()` produces, named rather than discovered."""
+    return [f"{sheet}_{lang}.txt"
+            for lang in TH.ORDER for sheet in BOARD_SHEETS]
+
+
 async def sweep() -> list[dict]:
```

```
-    first = {p.name: p.read_text(encoding="utf-8")
-             for p in sorted(OUT.glob("*.txt"))}
+    # THE SET IS NAMED, NOT GLOBBED, AND THAT WAS A BUG (F-5).  This line read
+    # `OUT.glob("*.txt")` and therefore meant "every text capture in the output
+    # directory" -- which stopped being this sweep's output the moment the
+    # `--surface` entry point started writing `surface_*.txt` beside it.  The
+    # control arm below runs `sweep()` alone, so it never writes those, and the
+    # comparison demanded a control file that could not exist: the DOCUMENTED
+    # command died in its own determinism check with a FileNotFoundError on
+    # `surface_blueprint.txt`.  Naming the frames makes the two arms agree by
+    # construction instead of by whatever happens to be on disk.
+    first = {n: (OUT / n).read_text(encoding="utf-8") for n in board_frames()}
```

**And the missing file is now reported as what it is**, in
`check_reproducible()`. A narrowed check that silently skipped absent control
files would be the vacuous-check failure this function's own docstring is
written against, so the absence is an error — with the message pointing at the
one place a rename has to be recorded:

```
+        # A FILE THE CONTROL ARM DID NOT WRITE IS A DISAGREEMENT ABOUT WHAT A
+        # SWEEP PRODUCES, and it is reported as one rather than as whatever
+        # error `read_text` happens to raise.  That is how F-5 presented: a
+        # bare FileNotFoundError traceback, which reads like a missing input
+        # and was in fact the two arms sweeping different things.
+        missing = [n for n in first if not (Path(td) / n).exists()]
+        if missing:
+            raise RuntimeError(
+                f"the control sweep did not write {missing} -- the two arms "
+                f"disagree about what a sweep produces. If a sheet was renamed "
+                f"or added, BOARD_SHEETS is the place that says so.")
         return [n for n, t in first.items()
                 if (Path(td) / n).read_text(encoding="utf-8") != t]
```

**The header no longer credits `TEXTUAL_ANIMATIONS=none` with a cure it did not
deliver.** The note ended on "the determinism check at the bottom of this file
is what keeps that claim honest" — and that check is precisely what refutes it.
Appended, without touching the correct part above it:

```
+# AND IT DID NOT CURE THE STALL.  This comment used to stop at the line above,
+# which reads as if the setting settled the matter.  It did not, and the check
+# that was supposed to keep the claim honest is what says so: `board_solari.txt`
+# still drifts intermittently on the SAME row this note is about (`DAYS
+# OVERDUE`), and `gallery_blueprint.txt` on a switch caught at `▅▅` vs `▁▁`.
+# Both were observed on control sweeps with every `surface` token popped, so
+# neither is caused by the batch that recorded them.  It makes this sweep exit
+# red about one run in three -- filed as F-1, open, and NOT fixed here.  The
+# setting is still correct and still worth having; it is simply not sufficient,
+# and a reader who trusted the paragraph above would go looking for the cause
+# somewhere else.
 os.environ["TEXTUAL_ANIMATIONS"] = "none"
```

## 2. Files modified

| file | source? | what |
| --- | --- | --- |
| `prototypes/capture_languages.py` | source | `BOARD_SHEETS`, `board_frames()`, the named comparison set in `main()`, the missing-control-file error in `check_reproducible()`, the corrected animation note |

**1 of 4 source files used.** No new dependency. Nothing else touched.

## 3. How to test

    cd C:\Users\jjgh8\Github\taskboard\.claude\worktrees\kanban-variants
    $env:PYTHONIOENCODING = "utf-8"
    python prototypes\capture_languages.py       # the DOCUMENTED command
    python -m pytest -q

The precondition matters: the fix is only exercised when `surface_*.txt`
already exist in `prototypes\gallery\`. There were **22** of them on disk for
every run below, so each run met the exact condition that used to kill it.

## 4. Test results

**The fix — verified where it failed.** Before, the documented command aborted
before the check finished. After, it runs the check to completion and reports
its real verdict:

    22 grids identical across two PROCESSES
    22 captures -> ...\prototypes\gallery
    no two boards identical

`22`, not 33 — the two arms now agree about what a sweep produces. **No run
raised `FileNotFoundError` again.**

**F-1's count, over nine consecutive runs of the documented command.**

| run | exit | verdict |
| --- | --- | --- |
| 1 | 1 | `NON-REPRODUCIBLE CAPTURES: ['board_darkside.txt', 'board_prism.txt']` |
| 2 | 0 | green |
| 3 | 0 | green |
| 4 | 1 | `NON-REPRODUCIBLE CAPTURES: ['gallery_blueprint.txt']` |
| 5 | 1 | `NON-REPRODUCIBLE CAPTURES: ['board_solari.txt', 'gallery_blueprint.txt']` |
| 6 | 0 | green |

**3 red in 6 runs — 50 %, worse than the one-in-three on record**, though six
runs cannot separate 33 % from 50 % and the honest reading is "consistent with
F-1, not a measurement of its rate".

**F-1 is broader than `inc3.md` recorded, and that is the new information
here.** It named `board_solari.txt` and `gallery_blueprint.txt`. Both appeared
again — and so did **`board_darkside.txt` and `board_prism.txt`**, which had
not been implicated before. Those two are the `depth` languages, and they
share a board layout; whatever is unsettled is not confined to solari's
split-flap label. Recorded, **not** investigated: F-1 is explicitly not this
increment's scope.

**AC-4 — the 44 named frames, against the increment-4 baseline.** Taken from
run 6's own output (the green run, so the gallery holds a sweep that verified
against a second process), plus a `--surface` sweep into the same directory:

| group | identical |
| --- | --- |
| 22 board/gallery `.txt` | **22 / 22** |
| 22 `surface_*` `.txt` + `.svg` | **22 / 22** |
| **the spec's 44 named frames** | **44 / 44** |
| 22 board/gallery `.svg` | 22 / 22 |
| **every file the sweep writes** | **66 / 66** |
| DIFFER | none |

**Suite:**

    1 failed, 284 passed, 2 skipped, 4 warnings in 29.02s

Unchanged from increment 5, including the same pre-existing environmental
clipboard failure. No test imports `capture_languages`, so this is a
no-regression check rather than coverage of the fix; the fix's evidence is the
command's own output above.

Sanity check on the new helper:

    BOARD_SHEETS = ('board', 'gallery')
    board_frames() -> 22 names, e.g. ['board_naught.txt', 'gallery_naught.txt', 'board_corgi.txt']

## 5. Findings

**F-5 · CLOSED.** The documented command completes its determinism check. It
still exits red when F-1 bites, which is the check working rather than failing.

**F-1 · open, and widened.** Now observed on `board_darkside.txt` and
`board_prism.txt` as well as the two already on record. Not fixed here.

**F-8 · NEW · `--surface` blocks when its output is redirected inside a
compound shell command.** Seen twice now, identically: a
`python prototypes\capture_languages.py --surface <dir>` with `>/dev/null 2>&1`
inside a chained command sat for 10+ minutes having consumed **0.2 s of CPU** —
blocked, not computing, and before its first file write. `settle()` is bounded
and raises, so it cannot be the settle loop. The identical command with its
output left alone completes in seconds, every time. Two occurrences make it a
pattern rather than a hiccup, so it is filed. It is a harness/shell interaction
and touches nothing this batch shipped. Both stalled processes were stopped by
PID after confirming their command lines; **no terminal process was touched.**

## 6. Pending

- F-1, still open and now with four implicated frames rather than two. The
  sweep's `settle()` needs the real harness's condition A, per `inc3.md` §7.
- F-8, unfiled anywhere but here.
- Everything already listed in `inc5.md` §6 — the blocked real export (inc 3's
  prism decision), the orphaned `surface_raster_ledger.png`, F-6's port to
  `tui-demos`, and the rich-in-`language.py` judgement.

## 7. Suggested next task

Close the batch: fill `spec.md` §8 with one evidence path per AC. F-1 is the
one thing that should not be carried much further — with the sweep now
completing its own check, F-1 is the only reason the documented command is
still a coin flip, and it is costing a re-run every other invocation.
