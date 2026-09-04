# Quick Spec — taskboard · batch "kits-learn-2" (L-33/F-1, L-42)

**Batch:** `2026-09-04-fastflow-09` · **Base ref:** `d58fa07` (branch `kanban-variants`, tree clean at Phase A) ·
Predecessor `kits-learn` closed 2026-09-04, §8 filled, archived to `archive/spec-archive-kits-learn.md` —
verbatim except one dated amendment recording that `inc11.md` closed **F-12** after §8 was written.
Language: English. Increments continue the worktree's single sequence: **inc12**, **inc13**.

**Input:** two defects that **real consumer apps found by running**, both approved by the operator on
2026-09-04. Where `kits-learn` learned from a lab that *read* the kit, this batch learns from three demo
apps that *shipped* on it — SCOPE, ATLAS, LOOM — and one of the two cost 1200 seconds of wall clock
before anyone knew what it was.

- **`tui-demos/.fast-dev-flow/LIMITS.md` L-33** and **`apps/scope/.fast-dev-flow/03-increments/inc1.md`
  §7 item 1 (F-1)** — the display posture drops the argument it documents.
- **`tui-demos/.fast-dev-flow/LIMITS.md` L-42** and **`apps/scope/.../inc2.md` §7 items 1–2 (F-4)** — the
  Sixel capability probe at import hangs any Windows process whose stdout is `NUL`.

---

## 1. Objective (1 line)

Stop the reference kit from **claiming a keybinding it does not own** (a display legend hardcoded to
`[1] DISPLAY` in every app) and from **hanging its own consumers at import** (a terminal probe fired at
a character device that never answers), so that SCOPE's two recorded-not-fixed findings become fixed in
the kit rather than worked around in every app that ever imports it.

---

## 2. User stories

- As **any app that draws a corgi display**, I want the legend beside the glass to say what MY control
  does and to carry the key I actually bound it to, so that the kit stops spending `[1]` on my behalf.
- As **a headless consumer** — a test runner, a bench, a CI job, a `--dump-frame` invocation — I want to
  `import taskboard.language` and get control back, so that "the kit is also a library" is true rather
  than aspirational.
- As **the operator**, I want the eleven kits' unlabelled renders to be exactly what they were, and every
  frame that moves to be named in this file before it moves.

---

## 3. Acceptance criteria (observable)

- [ ] **AC-1 · L-33/F-1 · the display posture reads `label`, and the caller's mark reaches the chrome.**
  `_surface_display` passes `label` to `display_label()`, which letters the caller's legend into the
  language's own notation. Observable, and it is a **property test rather than a mutation test**:
  `raster_region(img, w, h, label="7 SOURCE").chrome` for corgi contains the substring `[7] SOURCE` —
  the caller's binding AND the caller's word, in the chrome the compositor draws. A test that only
  asserted `told != bare` would prove the token is READ; only this proves it is read **correctly**.
  With **no** label the render is byte-identical to `d58fa07` for all eleven languages.
- [ ] **AC-2 · the `numbered` token stays in charge.** A language whose `numbered` token is **off**,
  handed the same `"7 SOURCE"`, draws `SOURCE` and **no bracket** — the binding is dropped rather than
  lettered, because a language with no notation for a keybinding must not grow one from a caller's
  string. This is **L-33's tie working**, and it is asserted, not assumed.

  **CORRECTION TO THE ACCEPTANCE AS FIRST WRITTEN (Phase B, before any edit).** This AC originally said
  *"industrial shares `display` and is not `numbered`"*. **That is false.** `numbered` is True for corgi,
  industrial **and** ledger, and the two languages that use the `display` posture are corgi and
  industrial — so **both are numbered** and no shipped language exercises the unnumbered limb. The AC is
  therefore asserted by **swapping the token**, exactly the idiom `test_mutation_changes_the_render`
  already uses on this file: `numbered` is a plain theme token (`Kit.numbered` is
  `bool(self.t.get("numbered"))`), so a kit with it turned off is a real kit and not a mock. Recorded
  here rather than quietly re-scoped, and it changes §6.2: `surface_industrial.*` moves for **AC-1**'s
  reason like corgi's, not for AC-2's.
- [ ] **AC-3 · the refusal that is now false is retracted, out loud.** `LABEL_REFUSED["display"]` is
  **deleted**, and the deletion is the finding: `kits-learn`'s inc8 declared display's refusal on the
  commitment *"the label beside a display belongs to the CONTROL, and the language numbers it rather
  than letting a caller name it"*. The consumer proved that commitment **half wrong** — it is true of the
  *notation* and false of the *content*, because the number is a keybinding and a keybinding is the
  caller's. `test_every_optional_argument_is_read_or_declared_refused` then requires display's render to
  move, and `test_the_declared_refusals_name_postures_that_exist` still passes.
- [ ] **AC-4 · L-42 · importing the kit with `stdout=DEVNULL` returns.** A **subprocess** test runs
  `python -c "import taskboard.language"` with `stdout=subprocess.DEVNULL` and asserts it returns within
  **2 s**. This is the test that would have hung: it is the exact invocation that cost SCOPE two 600 s
  runs. The probe fires only when stdout **and** stdin are real consoles — on Windows decided by
  **`GetConsoleMode`** succeeding on the stream's handle (`NUL` is a character device, so `isatty()`
  answers True for it and `GetConsoleMode` does not), on POSIX by `isatty()` alone (`/dev/null` is not a
  tty there). On no answer, **no Sixel**.
- [ ] **AC-5 · a real console still gets its capability.** A test drives the same selection path with the
  console check and the library import **mocked** (named explicitly in the packet), and asserts the
  transport comes back `"sixel"` — so the guard is proved to gate the probe rather than to kill it.
  Plus the bound: the answer wait is capped at **≤200 ms** (`PROBE_BUDGET_S`).
- [ ] **AC-6 · no API change, consumers untouched.** `TRANSPORT`, `raster_available()` and `AutoImage`
  keep their names and meanings. `tui-demos` is **not edited**. `raster_available() == (TRANSPORT in
  ("sixel","tgp"))` still holds and its existing test still passes.
- [ ] **AC-7 · nothing else moves.** The 66 frames are byte-identical to the baseline swept at `d58fa07`
  **before any edit** (`.fast-dev-flow/baseline-kits2/`), **except** the frames named in §6.2.
- [ ] **AC-8 · the consumer check.** `python -X utf8 -m pytest apps/scope/tests -q` is run from the
  `tui-demos` root, **read-only**, and its verbatim last line is in the packet. If SCOPE's frame would
  change once it passes a label, the packet says so — the gallery's collector detects the drift by sha,
  which is **the mechanism working** and not a regression.

---

## 4. Validation strategy

`python -X utf8 -m pytest -q` in this worktree is the gate for AC-1/2/3/4/5/6. Baseline at `d58fa07`:
**327 passed, 2 skipped, 4 warnings**. *The brief warned of a pre-existing environmental clipboard
failure; it did not appear in the Phase-A baseline run, and that is recorded rather than assumed away.*
AC-7 is a byte comparison against `.fast-dev-flow/baseline-kits2/`, refreshed by
`python prototypes\capture_languages.py --surface` run **plain and alone** (F-8 blocks `--surface` when
its output is redirected inside a compound command; F-1 makes the board sweep red about one run in
three). AC-8 is a read-only pytest run in the other repo. No test is skipped silently; the two
already-skipping tests are the numpy/`.npy` sweep-image pair and they are named.

---

## 5. Non-goals (what is OUT)

- **Forking `textual_image`.** The probe is inside the library, at `textual_image.renderable`'s module
  scope. This batch guards the *entry* to it and bounds the *wait*; it does not vendor or patch the
  library's internals beyond the one documented seam, and §6.3 says exactly what stays unbounded.
- **A new `raster_region` parameter.** The operator's decision for L-42 is explicitly *no API change*,
  and AC-1 keeps `label: str` for the same reason: a second parameter would be a second thing every one
  of the eleven postures has to have an answer for.
- **Any edit to `tui-demos`.** Read-only. AC-8 runs its suite and reads its packets; it writes nothing.
- **The real export to `~/.claude/skills/tui-design/`** — the orchestrator's call, as in every batch.
- **Fixing F-1** (this repo's flaky board sweep) or **F-8**. Recorded, run around.
- **The remaining LIMITS findings.** L-43–L-46 are `tui-demos`' capture harness and budget, not this
  repo's kits.

---

## 6. Detected security flags

- [ ] Auth / identity · [ ] Secrets / config · [ ] External integrations · [ ] Sensitive data
- [ ] Destructive DB · [x] Input / attack surface · [ ] Network / exposure

**`security_required`:** `true` (one flag, narrow)

**Risk summary:** the same surface `kits-learn` flagged, on a **new row**. `_surface_display` starts
interpolating caller text into a markup row that already carries a literal `[1]` — this module's
documented pitfall A1: escaping changes a string's *character* count and not its *cell* count, so
padding an escaped string hands back a rectangle one cell short. The existing code already does width
math on the plain string and `mark()`s on the way out, and that order is **preserved, not re-derived**.
`test_a_label_cannot_inject_markup_or_steal_a_cell` is parameterised over every language and will now
genuinely exercise corgi and industrial for the first time — until this batch, display refused the
label, so that test was asserting nothing about it. The Sixel guard *reduces* attack surface: it stops
the process writing an escape sequence to, and reading bytes from, a handle it has not established is a
terminal.

### 6.1 · The L-33/F-1 decision — the legend is the caller's, the notation is the language's

SCOPE's own general form (`inc1.md` §7 item 1) is the requirement: *a language mechanism that draws a
keymap-bound mark must take the binding from its caller, because the caller owns the keymap.*

**The rule:** `label` is split once on whitespace. If the first token is a run of digits it is the
**binding**; the rest is the **word**. Otherwise the whole label is the word and the language keeps its
own index. A `numbered` language letters `[binding] WORD`; one that is not numbered letters `WORD` and
drops the binding on the floor. No label at all → the language's own default, unchanged.

**Why a mini-syntax and not a second parameter.** Three alternatives were considered and rejected:
(a) *the label replaces the legend verbatim* — then an unnumbered language handed `[7] SOURCE` draws
brackets it has no notation for, which breaks the `numbered` token, the one thing L-33 says must stay in
charge; (b) *the label is only the word, the index stays the kit's* — fixes half the defect and leaves
`[1]` still spent by the kit, which is the half SCOPE named first; (c) *a new `idx` parameter on
`raster_region`* — eleven postures each needing an answer for an argument ten of them refuse, to carry
one integer that is already expressible in the string. The mini-syntax is one rule, it keeps the token
authoritative, and it makes both halves reachable through the parameter that was already documented.

**Cost of being wrong:** an app whose legend legitimately starts with a number (`"3D FIELD"`) gets it
read as a binding. `"3D"` is not a run of digits, so that exact case is safe; a label of `"2 PASS"`
meaning "two passes" is not. Recorded as the known edge, and the mitigation is that the word is the
caller's and it can write `"PASS 2"`.

### 6.2 · Frames that move on purpose (named in advance)

| frame | why | which AC |
| --- | --- | --- |
| `surface_corgi.txt` | the sweep passes `label="mbb rho final"`; the legend becomes `[1] MBB RHO FINAL` | AC-1 |
| `surface_corgi.svg` | same render, other transport | AC-1 |
| `surface_industrial.txt` | same label; industrial is `numbered` too → `[1] MBB RHO FINAL` | AC-1 |
| `surface_industrial.svg` | same render, other transport | AC-1 |

**Four frames, and they cannot not move.** The surface sweep hands every language
`SURFACE_LABEL = "mbb rho final"`, so a display posture that reads its label renders differently **by
definition** — that is the whole content of the finding. `"mbb rho final"` has no leading integer, so
corgi keeps index 1 and the `numbered` notation is still visible in the shipped frame. The other **62**
frames stay byte-identical. No **board** frame moves: the board never calls `raster_region`.

**Downstream, stated in advance:** `check_box_matches_shipped()` (inc11) compares the shipped frame
against a fresh `raster_region(..., label=SHEET_LABEL)`, so it stays green **only if the recapture is
done**. Skipping the recapture turns AC-7 into a `SurfaceIndexMismatch`, which is that check doing its job.

### 6.3 · The L-42 decision — guard at the entry, bound at the seam, and say what is left

The probe is **not ours**. The chain is `taskboard.raster → textual_image.widget →
textual_image.renderable → sixel.query_terminal_support()`, and it runs at
`textual_image/renderable/__init__.py` **module scope**, gated by that module's own
`is_tty = sys.__stdout__ and sys.__stdout__.isatty()`.

**The guard** is therefore placed where the library already reads: `raster.py` substitutes a stdout shim
whose `isatty()` answers **accurately** for the duration of the import, so on `NUL` the library's own
`is_tty` is False and it selects the unicode renderable without querying anything. This is not a
monkeypatch of library internals — it is telling the library the truth that `isatty()` cannot express on
Windows. `modals.py` imports the same widget at module scope, so it takes its `AutoImage` from
`raster.py` and the second door closes with it.

**The bound** is `PROBE_BUDGET_S = 0.2`, applied at `textual_image._terminal.read` — a module-level
attribute, the library's own seam, restored afterwards — capping the **sum of the waits** the probe
performs.

**What stays unbounded, said plainly:** a single `os.read()` that blocks *after* `WaitForSingleObject`
has returned signalled cannot be bounded without forking the library, because there is no non-blocking
read behind that call. The guard is what removes the reported failure; the budget caps the answer wait.
This is the case the brief anticipated, and this paragraph is the packet saying so.

---

## 7. Batch status

| Field | Value |
|-------|-------|
| Current phase | closed |
| Started | 2026-09-04 |
| Closed | 2026-09-04 |
| Promoted to /dev-flow | no |
| Notes | **≤ 4 source files per increment, one agent, sequential.** **inc12:** AC-1/2/3 — `display_label()` takes the legend, `_surface_display` passes it, `LABEL_REFUSED["display"]` retracted, the property test, the four recaptures, SCOPE's suite as the consumer check. **inc13:** AC-4/5/6 — the console guard and the probe budget in `raster.py`, `modals.py` taking its widget from it, the DEVNULL subprocess test and the mocked-console test. |

---

## 8. Close (filled in phase C)

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
