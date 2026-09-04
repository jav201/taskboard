# Increment 13 — L-42 / SCOPE F-4: the Sixel capability probe gets a guard and a budget

Batch `2026-09-04-fastflow-09` ("kits-learn-2") · increment 2 of 2 · base ref `d58fa07`
(branch `kanban-variants`). One agent, 3 source files. **No git operations.**

Scope: *probe the terminal only when there is one, bound the answer wait to ≤200 ms, assume no Sixel
on no answer, change no API, edit no consumer.*

## 1. The defect, and what it cost

`taskboard/raster.py` imports `textual_image` at module scope **on purpose** — the library decides its
transport by querying the terminal, and that only works before Textual seizes it. The module docstring
already said so. What it did not say is the price.

`textual_image/renderable/__init__.py` runs a Sixel **device-attributes** query at ITS module scope —
write `ESC[c` to stdout, then read stdin until the answer arrives — gated by nothing but its own
`is_tty = sys.__stdout__ and sys.__stdout__.isatty()`. **On Windows `NUL` is a character device, so
`isatty()` answers True for it.** A process launched with `stdout=subprocess.DEVNULL` believes it is
talking to a terminal, writes the query into the void, and waits for an answer that cannot come.

**Measured here, on the code as it stood at `d58fa07`, before any edit** — because a regression test
that has never been seen to fail is a decoration:

```
stdin=DEVNULL  stdout=DEVNULL -> HUNG (killed at 8s)
stdin=inherit  stdout=DEVNULL -> HUNG (killed at 8s)
```

It cost SCOPE's second increment **two 600-second runs** before `faulthandler.dump_traceback_later`
produced the stack, and the hang looks exactly like a slow numba compile until someone dumps it. The
chain is `taskboard.language → taskboard.raster → textual_image.widget → textual_image.renderable →
sixel.query_terminal_support`, so **every headless consumer of a kit inherits it**: a test runner, a
bench, a CI job, a `--dump-frame` invocation.

## 2. Where the probe actually lives, and what that forced

**The probe is inside the library, at module scope, and cannot be bounded without forking it** — the
case the brief anticipated. `renderable/__init__.py` is a sequence of `if`s executed on import; there
is no function to call, no flag to pass, no lazy seam.

So the guard **wraps the import**, and it does so at the one input the library already reads. Rather
than patch library internals, `raster.py` substitutes a stdout stand-in whose **`isatty()` answers
accurately** for the duration of the import. The library's own `is_tty` then comes out False, it
selects the unicode renderable **without querying anything**, and `get_cell_size()` skips both of its
query branches and falls through to its VT340 defaults. This is not a monkeypatch of a private
function — it is telling the library the one truth `isatty()` cannot carry on Windows.

**The discriminator is `GetConsoleMode`**, named as the brief asked: it succeeds on a console handle
and **fails on `NUL`**, which is exactly the distinction `isatty()` cannot express. On POSIX
`isatty()` is already correct (`/dev/null` is not a tty there) and is the whole test. **Both stdout and
stdin must pass**, because the probe writes to one and reads from the other, and it is the read that
blocks.

**The budget** is `PROBE_BUDGET_S = 0.2`, applied by rebinding `textual_image._terminal.read` — a
module-level attribute, the library's own seam — to a wrapper carrying a deadline across all its calls,
restored in `finally`. The library already passes a 0.1 s per-read timeout; what it has no concept of
is a **total**. On expiry it raises `TimeoutError`, which `query_terminal_support()` and
`get_cell_size()` **already catch** and treat as "no answer" — so the failure mode is the correct one
(assume no Sixel) rather than an exception escaping the import.

**What is still not bounded, said plainly rather than implied:** a single `os.read()` that blocks
*after* `WaitForSingleObject` has returned signalled. There is no non-blocking read behind that call,
so capping it would mean forking the library. **The guard is what removes the reported failure; the
budget caps the answer wait on the path the guard lets through.**

## 3. A latent bug found while rewriting the lookup

The transport was:

```python
TRANSPORT = {None: "none", _Sixel: "sixel", _TGP: "tgp"}.get(_Chosen, "glyph")
```

When `textual_image` is **absent**, the `except` branch sets all four names to `None` — so the dict
literal collapses to `{None: "tgp"}` and the lookup returns **`"tgp"`**. A box with no library
installed reported a real graphics transport and **`raster_available()` answered True**, which is the
exact opposite of that function's stated commitment ("honest by construction"). Nobody had run without
the dependency, so nobody had seen it.

Replaced with three `is` tests, which cannot collapse, plus
`test_an_absent_library_reports_no_transport_rather_than_tgp` as the regression. **Recorded as F-13.**

## 4. Files modified

| file | source? | what |
| --- | --- | --- |
| `taskboard/raster.py` | source | `PROBE_BUDGET_S`, `_is_a_real_console`, `_NotATerminal`, `_budgeted`, `_import_textual_image`, `_transport`, `_detect` |
| `taskboard/modals.py` | source | takes `AutoImage` from `.raster` instead of importing the library again |
| `tests/test_surface.py` | source | 5 tests, 6 cases |
| `.fast-dev-flow/probes/patch_*.py` | artefact | the one-shot patch scripts actually applied |

**3 source files.** No new dependency; `importlib`, `sys`, `time`, `ctypes`, `msvcrt` are stdlib and
`ctypes`/`msvcrt` are imported inside the Windows branch only.

**`modals.py` mattered.** It imported `textual_image.widget` at module scope too, so the probe had
**two doors** and the guard would only have covered whichever module Python happened to load first.
It now re-exports `raster.AutoImage`, verified identical object:

```
modals.AutoImage is not None: True
same object as raster.AutoImage: True
```

**No API change.** `TRANSPORT`, `raster_available()` and `AutoImage` keep their names, types and
meanings, and `test_transport_is_reported_honestly` still passes untouched.

## 5. Test results

```
$ python -X utf8 -m pytest -q
341 passed, 2 skipped, 4 warnings in 29.22s
```

335 after inc12 + 6 new. No regressions, no new skips. **The pre-existing environmental clipboard
failure the brief warned about did not appear in any of the three full runs this batch** — recorded as
not-observed, not as fixed; the environment may differ from the one that saw it.

**The fix, measured the same way as the defect:**

```
stdin=DEVNULL  stdout=DEVNULL -> rc=0 in 0.39s
stdin=inherit  stdout=DEVNULL -> rc=0 in 0.41s
```

From "killed at 8 s" (and 600 s in SCOPE's real runs) to **0.4 s**.

The five tests:
- `test_importing_the_kit_with_stdout_devnull_returns[devnull|inherit]` — the subprocess test, `timeout=2`
  **is** the assertion. 2 s is ~5x the measured 0.4 s, chosen as headroom rather than to pass.
- `test_the_guard_reads_the_console_and_not_merely_isatty` — the discriminator on the **real OS**: opens
  `os.devnull`, asserts on Windows that it *does* answer `isatty()` (the premise of L-42) and that
  `_is_a_real_console` rejects it anyway.
- `test_a_real_console_still_gets_its_capability_when_the_terminal_answers` — **what is mocked, exactly:
  `RS._import_textual_image`, i.e. the terminal's ANSWER and the library that reads it. Nothing else.**
  Asserts `_detect()` maps a library that chose Sixel onto `"sixel"`, TGP onto `"tgp"`, and anything
  else onto `"glyph"`. It cannot use a real console because pytest never has one.
- `test_an_absent_library_reports_no_transport_rather_than_tgp` — §3's regression.
- `test_the_probe_answer_wait_is_bounded` — `PROBE_BUDGET_S <= 0.2`, the operator's number.

**Frames: nothing moved.** This increment changes no rendering, and the byte comparison confirms it:

```
identical: 62 / 66
MOVED: surface_corgi.svg surface_corgi.txt surface_industrial.svg surface_industrial.txt
```

— the same four inc12 moved and named in spec §6.2 in advance, and no more. **No new capture was
needed or taken for this increment**, because nothing a person sees changed: the only observable is
that a headless import now returns.

## 6. The consumer check, and a workaround that is now deletable

`tui-demos` **read-only**, from its root:

```
$ python -X utf8 -m pytest apps/scope/tests -q
44 passed in 33.91s
```

SCOPE's suite carries the L-42 **workaround** — every child process's stdout is sent to a regular
file rather than to `NUL` (`test_inc2.py:45-48`, `test_inc3.py:35-38`, and the bench's
`# stdout is a PIPE, never NUL: see inc2 F-4`). That workaround is now **unnecessary**, proved by
running SCOPE's own import chain the way that used to hang, **without editing anything there**:

```
SCOPE import, stdout=DEVNULL -> rc=0 in 0.69s
stderr tail: ok
```

**0.69 s for the invocation that cost two 600-second runs.** Deleting the workaround is SCOPE's call,
not this batch's; the kit no longer requires it.

## 7. Risks

- **A single blocking `os.read()` after a signalled wait is still unbounded** (§2). It cannot be fixed
  without forking `textual_image`. The guard means it is only reachable from a real console, where the
  terminal is expected to answer.
- **`_NotATerminal` is installed on `sys.__stdout__` during the import.** It is restored in `finally`,
  and it only ever answers `isatty()` itself — everything else delegates. But it IS a global mutation
  for the duration of an import, and a library that captured `sys.__stdout__` by reference during that
  window would keep the shim. None of the four imported modules does (they read `sys.__stdout__`
  freshly at each use).
- **`_is_a_real_console` swallows exceptions and answers False.** A console that somehow raised on
  `fileno()` would be treated as headless and lose Sixel. Losing a capability is the safe direction;
  hanging is not.
- **The Windows branch is untestable on POSIX and vice versa**, so CI on another platform exercises
  only the `isatty()` half. Stated rather than papered over with a mock that would assert nothing.
- **`raster_available()` may now answer False where it previously answered True** on a box with no
  `textual_image` — that is §3's fix, and it is a behaviour change in the honest direction.

## 8. Pending

- **F-13** (§3) is fixed here but **not written into `tui-demos/.fast-dev-flow/LIMITS.md`** — that file
  belongs to the other repo and this batch is read-only there.
- **L-42's own entry** still reads "Disposition: WORKAROUND, applied in the tests, not in the kit."
  That is now out of date. Updating it, and deleting SCOPE's workaround, are both the orchestrator's
  call in the other repo.
- The real export to `~/.claude/skills/tui-design/` — the orchestrator's call. Stale by inc12's four
  frames; **not exported**.
- `LANGUAGES.md` §3b's one added sentence (L-33's ask) — **not written**, same reason.
- F-1, F-8 — untouched.

## 9. For the skill

1. **A capability probe at import is a load-bearing constraint on every consumer, not an
   implementation detail.** SCOPE's own §7 said this and it is the general form: *if a module queries
   the world at import, every process that transitively imports it inherits that query — including ones
   with no world to query.* The docstring that explains WHY the import is eager must also state what it
   costs a headless caller.
2. **`isatty()` is not "am I on a terminal" on Windows.** `NUL` is a character device and answers True.
   The discriminator is **`GetConsoleMode`**, which fails on it. *Any code that gates terminal I/O on
   `isatty()` alone has a Windows null-device bug waiting.*
3. **Guard the ENTRY when you cannot bound the CALL.** When the hazard is inside a dependency at its
   module scope, there is no seam to time out — but there is usually an INPUT the dependency reads to
   decide. Correcting that input is smaller, more honest and more durable than a thread watchdog or a
   fork. *Ask what the library asks before deciding to patch what it does.*
4. **Say which half of the timeout you actually got.** "Guard + timeout" sounds complete; here the
   guard is total and the timeout is partial, and one blocking read remains unbounded. *A packet that
   claims a bound it did not achieve is worse than one that names the gap.*
5. **Prove the regression test can fail, and paste the failure.** This one was measured against the
   pre-fix code in both stdin modes before the fix was written. *A hang test that has only ever passed
   is indistinguishable from a test that does not run.*
6. **A dict literal keyed on values that can all be the same is a collapse waiting to happen.**
   `{None: a, x: b, y: c}` silently becomes `{None: c}` when `x` and `y` are `None`. It shipped, and
   it made an "honest by construction" function dishonest in exactly the case it existed for.
   *Prefer explicit `is` tests over a lookup whose keys are runtime objects that may coincide.*
7. **Count the doors.** The guard would have been useless if `modals.py` had kept its own direct
   import — whichever module loaded first would decide. *When you guard an import, grep for every other
   place that performs it.*
8. **Fixing a kit deletes work in its consumers, and that is worth measuring.** SCOPE's file-redirect
   workaround is now unnecessary, proved by running the invocation that used to hang — from a
   read-only checkout, changing nothing. *A kit fix's real acceptance test is the consumer's workaround
   becoming deletable.*
