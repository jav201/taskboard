# Increment 7 — L-32: the title block takes content as data

Batch `2026-09-04-fastflow-08` ("kits-learn") · increment 1 of 4 · base ref `ea64fdf`.
Scope: *make blueprint's frame mechanism reachable from an app that is not the
board, keep `title_block()`'s signature working as a thin adapter, keep the
board's captures byte-identical.* No git operations. `spec.md` §1–§7 untouched
except AC-6, corrected before implementing (see §5).

## 1. What changed

**`Blueprint.stamp(rows, w, strip=None)` is the mechanism; `title_block()` is
now three lines over it.** The old signature `title_block(options, active, w)`
took a MODE STRIP's options and the mode on screen — taskboard's content, and
a concept a parameter study does not have — so the language's single largest
frame investment was reachable only from an app that happened to have a nav
row. emersio-lab rebuilt the block instead, re-deriving the docking arithmetic
(`bw`, `x`) the kit already computed, and stood up a second copy of the mark
this language is most identified by.

`stamp()` takes the content as **rows of `(caption, value, knocked)` cells** —
the same triple `block_cells()` already built — and the selection as an
**optional extra**. `strip=None` is an app with no mode strip, and it gets no
registration marks: nothing is selected, which is not the same as registering
nothing.

**The narrowing ladder split along the same seam, and that is the design.**
Tier 1 (shed cells, in `TB_DROP` order) stayed with the CALLER — which cell a
sheet can afford to lose is the sheet's own knowledge, and `block_cells()` is
taskboard's answer to it. Tiers 2 and 3 (give up the unselected modes, then
renounce the strip) moved into `stamp()`, because they are the strip's, and
the strip is the mechanism's optional extra.

**One real defect, found by the new test rather than by reading.** Body rows
were never padded to `w`. On ONE body row the arithmetic lands on `w` by
construction (`x = w - bw`, and the ladder runs until the strip fits beside
it), so the pad was zero for the whole life of the board's block and the
rectangle was exact *by luck rather than by rule*. The first two-row stamp came
back with its second row **9 cells short** — a ragged frame, which is the one
thing a reserved rectangle cannot be:

```
E       AssertionError: [116, 116, 107, 116]
```

Fixed by padding on the plain measure (`block_w`), never on the markup — width
math before escaping, this module's rule. Zero change for one-row stamps, which
the byte-identity below confirms.

**`Blueprint.glyphs` — the ten, as data rather than as prose.** The class
docstring enumerates the alphabet and then makes a strong claim about it (*not
one of them is a vertical stroke … so a containing box here is not merely
absent: it is unconstructable*). Stated only in prose that claim was checkable
by reading and by nothing else — which is part of how L-34 came to be asked
for. Each member is read off where it already lives: `━` from the `dimension`
ramp, the hatch from its token, the rest from the class's own constants. It
comes to exactly ten, and `│` is not among them.

## 2. Files modified

| file | source? | what |
| --- | --- | --- |
| `taskboard/language.py` | source | `Blueprint.stamp()` (new mechanism), `title_block()` reduced to an adapter, `glyphs` property |
| `tests/test_frame.py` | source | NEW — 9 tests: the stamp with no strip, registration only when selected, docking, the one knockout, the alphabet, markup injection ×2, the adapter, the ladder |

**2 of 4 source files used.** No new dependency. Nothing else touched.

## 3. How to test

    cd C:\Users\jjgh8\Github\taskboard\.claude\worktrees\kanban-variants
    $env:PYTHONIOENCODING = "utf-8"
    python -m pytest -q
    python prototypes\capture_languages.py

## 4. Test results

**Suite:** `294 passed, 2 skipped, 4 warnings in 27.07s` — baseline at `ea64fdf`
was `285 passed, 2 skipped`, so the 9 new tests are the whole difference and
nothing regressed. (Note: the pre-existing clipboard failure `inc6.md` recorded
did **not** reproduce on this machine today; the baseline run was already green
at 285.)

**`tests/test_frame.py`:** `9 passed in 0.34s`.

**AC-4 — byte identity against the pre-edit baseline.** Baseline swept at
`ea64fdf` before any edit into `.fast-dev-flow/baseline-kits/` (66 files).

| group | identical |
| --- | --- |
| 22 board/gallery `.txt` | 22 / 22 |
| 22 board/gallery `.svg` | 22 / 22 |
| 11 `surface_*.txt` + 11 `surface_*.svg` | 22 / 22 |
| **every file the two sweeps write** | **66 / 66** |
| DIFFER | **none** |

**F-1's count for this increment.** The baseline sweep needed **3 runs** to go
green (run 1 red on `board_instrument.txt`, run 2 red on `board_prism.txt`, run
3 green). The post-increment sweep went green on the **first** run. **2 red in
4 runs** so far this batch.

## 5. Findings

**F-9 · NEW · a one-row mechanism can be exact by luck.** `stamp()`'s body rows
were never padded, and one body row always landed on `w` anyway. The rule that
made it true (`x = w - bw` after the ladder) is not the rule the code was
written to; nothing said "exactly `w` cells" and nothing checked it, so the
invariant held for one caller and broke for the second. **Portable: an
invariant that only one input can violate is untested by every input you have.**

**L-32, met, with one correction to the finding.** The finding says the lab
"re-derived the docking arithmetic (`bw`, `x`) that `title_block()` already
computes". True — and the two derivations are **not** the same: the lab used
`bw = max(len(plain)) + 2` and 3 spaces where the kit's `GAP` is 2. So the
second implementation had already **drifted** from the first, which is a
stronger version of the finding than it states. It is why AC-6 was corrected
*before* implementing: the patched lab cannot come back byte-identical, and
saying so up front is not the same as narrowing an assertion afterwards.

**`title_block()` had no test at all before this increment** — grep across the
repo found zero callers outside `language.py` and zero assertions. That is part
of how it came to have a signature only one app could satisfy: nothing outside
the board ever called it, so nothing outside the board ever noticed that
nothing outside the board *could*.

## 6. Pending

- AC-1 (L-31), AC-3 (L-34), AC-6 (the lab proof), AC-7 (the staged export).
- F-1, open; a fifth frame (`board_instrument.txt`) is implicated as of today.
- F-8, unchanged; `--surface` was run plain and alone.

## 7. Suggested next task

Increment 2 — L-31: `_surface_tint` reads its `label`, the declared-refusal
registry, the optional-argument test, and the two surface recaptures named in
spec §6.2.
