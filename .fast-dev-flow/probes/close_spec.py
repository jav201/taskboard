"""One-shot: fill spec.md section 8 for kits-learn-2. Run from the worktree root."""
import pathlib

p = pathlib.Path(".fast-dev-flow/spec.md")
s = p.read_text(encoding="utf-8")

OLD = """## 8. Close (filled in phase C)

*(unfilled — this batch is open)*
"""

NEW = """## 8. Close (filled in phase C)

### What changed

The reference kit stopped taking two things from its consumers that were never its to take:
**a keybinding** and **control of the process**.

`Kit.display_label()` hardcoded `[1] DISPLAY`, and `_surface_display` threw away the `label`
it documented. Since §3b makes this language's numbers *keybindings*, the kit was spending
`[1]` on behalf of every app that drew a display. It now takes the legend from the caller —
**an ASCII run of digits in front is the BINDING, the rest is the WORD** — while the language
keeps the notation, so a `numbered` language letters `[7] SOURCE` and one that is not letters
`SOURCE` and drops the binding it has no notation for. `LABEL_REFUSED["display"]` was
**retracted**: its commitment was true of the notation and false of the content, and a
consumer is what falsified it.

`taskboard/raster.py` ran a Sixel device-attributes probe at import, and on Windows `NUL`
answers `isatty()`, so any process with `stdout=DEVNULL` queried the void and blocked forever.
The probe now fires **only when both stdout and stdin are real consoles** — decided by
**`GetConsoleMode`**, which fails on `NUL` where `isatty()` lies — with the answer wait bounded
at **200 ms** and no answer meaning no Sixel. `modals.py` was the second door and now takes its
widget from `raster.py`. **From 600 s to 0.4 s, with no API change and no consumer edited.**

### How it was tested

- `python -X utf8 -m pytest -q` — **341 passed, 2 skipped, 4 warnings** (baseline at `d58fa07`:
  327 passed). 14 new tests: 8 for inc12, 6 for inc13, all in `tests/test_surface.py`.
- **Both defects were measured on the pre-edit code before either was fixed**, so neither
  regression test is a decoration: the DEVNULL import hung at 8 s in both stdin modes, and the
  four stale-frame failures appeared exactly where §6.2 predicted them in writing.
- The surface sweep was re-run **plain and alone** (F-8), green on the first run; 66 frames
  byte-compared against `.fast-dev-flow/baseline-kits2/`, swept **before any edit**.
- `apps/scope/tests` was run from the `tui-demos` root as the consumer check, **read-only**.

### Evidence per AC

| AC | verdict | evidence |
| --- | --- | --- |
| AC-1 · label reaches chrome | **met** | `inc12.md` §1, §3 — `test_the_display_legend_is_the_callers_mark_and_reaches_the_chrome` asserts `[7] SOURCE` in `chrome[0]`, on `chrome` because that is what a non-Textual caller reads |
| AC-2 · `numbered` in charge | **met, premise corrected** | `inc12.md` §2 — the AC's claim "industrial is not numbered" was **false**; both display languages are numbered, so the limb is asserted by token swap. Correction dated in §3 above before any edit |
| AC-3 · refusal retracted | **met** | `inc12.md` §1 — `LABEL_REFUSED["display"]` deleted with a dated comment; `test_every_optional_argument_is_read_or_declared_refused` now requires display's render to move, and does |
| AC-4 · DEVNULL import returns | **met** | `inc13.md` §1, §5 — `HUNG (killed at 8s)` before, `rc=0 in 0.39s` after, both stdin modes; `timeout=2` is the assertion |
| AC-5 · real console keeps capability | **met** | `inc13.md` §5 — `_detect()` maps Sixel/TGP/other correctly with **`_import_textual_image` mocked and nothing else**; `PROBE_BUDGET_S <= 0.2` |
| AC-6 · no API change | **met** | `inc13.md` §4 — `TRANSPORT`, `raster_available()`, `AutoImage` unchanged; `tui-demos` never written to (§6) |
| AC-7 · nothing else moves | **met** | `62 / 66` identical; MOVED = the four `surface_{corgi,industrial}.{txt,svg}` named in §6.2 in advance |
| AC-8 · consumer check | **met** | `44 passed in 33.91s`; SCOPE's frame does **not** move today because it passes no label, and its L-42 workaround is now deletable — proved at `0.69s` without editing it |

### Open risks / pending

- **One blocking `os.read()` after a signalled wait is still unbounded** and cannot be bounded
  without forking `textual_image`. Named in `inc13.md` §2 and §7 rather than implied.
- **F-13** (new): the transport dict literal `{None: "none", _Sixel: "sixel", _TGP: "tgp"}`
  collapsed to `{None: "tgp"}` when the library was absent, so a box with no `textual_image`
  reported a TGP transport and `raster_available()` answered True. Fixed here with three `is`
  tests and a regression; **not written into `tui-demos`' LIMITS**, which is read-only.
- **L-42's entry still says "WORKAROUND, applied in the tests, not in the kit."** Out of date.
  Updating it, and deleting SCOPE's file-redirect workaround, are the orchestrator's call.
- **`LANGUAGES.md` §3b's added sentence** (L-33's own ask) — **not written**. Hand-written skill
  file, same call as `kits-learn`'s §11.
- **The real export** — orchestrator's call. The live skill is stale by inc12's four frames.
- **A concurrent agent was editing `tui-demos`** during this batch (11:17–11:25, an `infra-1`
  increment). Nothing was written there by this batch; the 44-passed result is a timestamped
  snapshot and `scope.py:129` — the line the finding depends on — was verified unchanged.
- **The pre-existing clipboard failure did not appear** in any of the three full runs. Recorded
  as not-observed, not as fixed.
- **F-1**, **F-8** — untouched. No board sweep was run at all, because no board frame moves.

### Security flags — handling

One flag fired (input / attack surface) and it was the only one. inc12 interpolates caller text
into a markup row that already carries a literal `[1]`: the width math stays on the **plain**
string with `mark()` on the way out, the order pitfall A1 requires, **preserved rather than
re-derived**. `test_a_label_cannot_inject_markup_or_steal_a_cell` now genuinely exercises corgi
and industrial for the first time — until this batch display refused the label, so that test was
asserting nothing about them — and the recaptured frames confirm the box did not move by a cell.
inc13 **reduces** attack surface: the process no longer writes an escape sequence to, or reads
bytes from, a handle it has not established is a terminal. No secrets, no external calls, no
destructive commands, no new dependency, no git state changed.

### Suggested commit message

```
kits-learn-2(L-33,L-42): the kit stops taking a keybinding and the process

display_label() takes the caller's legend: an ASCII run of digits in front is
the BINDING, the rest is the WORD, and the language keeps the notation -- so a
numbered language letters [7] SOURCE and one that is not letters SOURCE. The
kit was spending [1] on every consumer's behalf, because in a TUI the numbers
ARE the keybindings and a keybinding belongs to whoever owns the keymap.

LABEL_REFUSED["display"] is retracted. Its commitment was true of the notation
and false of the content, and a consumer is what falsified it -- which is the
declared-refusal table working, not a reversal to apologise for.

The Sixel probe fires only when stdout AND stdin are real consoles, decided by
GetConsoleMode because NUL is a character device and isatty() answers True for
it. The answer wait is bounded at 200 ms; no answer means no Sixel. modals.py
was the second door and now takes its widget from raster.py. 600s -> 0.4s, no
API change, no consumer edited.

Also fixes a latent collapse: {None:"none", _Sixel:"sixel", _TGP:"tgp"} became
{None:"tgp"} with the library absent, so a box with no textual_image reported a
graphics transport.

Moved on purpose: surface_{corgi,industrial}.{txt,svg} (the legend row).
62/66 frames byte-identical against a baseline swept before any edit.
```
"""

assert s.count(OLD) == 1, "section 8 anchor"
s = s.replace(OLD, NEW)
s = s.replace("| Current phase | B — implementation |", "| Current phase | closed |")
s = s.replace("| Closed | — |", "| Closed | 2026-09-04 |")
p.write_text(s, encoding="utf-8")
print("spec section 8 closed")
