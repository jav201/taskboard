# Increment 42 — the suite stops rewriting itself, and the "stale" bake turns out to be a calendar

**Batch:** `rework-2` · closes `spec.md` §9.5 items 1 and 2
**Files:** `pyproject.toml`, `tests/test_components.py`, `prototypes/gallery/gallery_darkside.{txt,svg}`
— **4 source files.**

**Two findings, and the second one inverts. (a) `pytest -q` mutated its own suite because
`prototypes/out/_b37_test.py` matched pytest's default `python_files`; collection ran its module body,
which appends. Closed twice — `testpaths = ["tests"]` and a rename — and proved closed by an md5 that does
not move across a full run. Three duplicate copies removed from `tests/test_components.py`, 995 collected
before and 995 after, which is the arithmetic that shows the duplicate `def`s were shadowing rather than
adding. (b) `gallery_darkside` is NOT stale. `Darkside.wordmark()` calls `doodle()`, which is
`PHASES[date.today().day % 6]`. The frame was baked on 2026-09-05 — day 5, `PHASES[5] = "(.)"` — and
re-baked today, day 6, `PHASES[0] = "( )"`. It was one day old, not four months. The re-bake is committed
as instructed and it closes nothing: tomorrow is day 7 and the cell goes back to `(.)`.**

---

## 1. The mutation: cause, and why the fix is two locks

`prototypes/out/_b37_test.py` was inc37's one-shot edit script, left in the scratch yard. Its name matched
pytest's default `python_files = test_*.py *_test.py`, and **pytest runs a module's body in order to
collect it**, so `pytest` from the repo root executed:

```python
p = pathlib.Path("tests/test_components.py")
s = p.read_text(encoding="utf-8")
...
s = s.rstrip("\n") + "\n" + tail
p.write_text(s, encoding="utf-8")
```

`assert s.count(anchor) == 1` did not stop the re-fire: the anchor is the three-line prefix of its own
replacement, so it survives the substitution and the guard is satisfied on every run.

**Both locks, because they fail differently.**

| lock | what it stops | what it does not stop |
| --- | --- | --- |
| `testpaths = ["tests"]` in `pyproject.toml` | collection ever leaving the suite directory, for this probe and any future one | `pytest prototypes/` typed by hand |
| rename `_b37_test.py` → `_b37_probe.py` | this file being collected under any invocation | the next probe someone names `test_*.py` |

`prototypes/out/*` is `.gitignore`d (five named exceptions), so **the rename is a working-tree act and does
not appear in the diff.** The committed half of the fix is the one line in `pyproject.toml`. Stated here
because a reader of the commit cannot see the other half.

**One offender, and only one — asserted rather than assumed:**

```
$ find . -name "test_*.py" -o -name "*_test.py" | grep -v .git | grep -v __pycache__
./prototypes/out/_b37_test.py          <- the probe
./tests/test_app.py  ... ./tests/test_surface.py   (12, all in tests/)
```

**Proof the mutation is closed**, taken before the dedupe so the duplicates were still there to be added
to:

```
md5 tests/test_components.py   before a full run   ee4942f089c42d4be20ceacbb379c939
$ python -X utf8 -m pytest -q
993 passed, 2 skipped, 4 warnings in 32.13s
md5 tests/test_components.py   after  a full run   ee4942f089c42d4be20ceacbb379c939
```

Every gate run in `rework-1` had to be followed by a hand restore. That ends here.

## 2. The dedupe, and the count that proves nothing was lost

HEAD carried **three byte-identical copies** of the inc37 block (2651 chars each, verified equal before
removal) and three of the `FRAMES` assignment:

```
FRAMES = ...              lines 31, 35, 39
inc37 block               offsets 97560-100211, 100213-102864, 110630-113281
```

The first block is kept — it sits after inc41's section and before inc38's, which is where the original
append landed — and the second and third are cut with their trailing blank lines, then the inc38 seam
restored to two blank lines.

```
$ python -X utf8 -m pytest --collect-only -q | tail -1
995 tests collected in 0.40s      <- before, with all three copies
995 tests collected in 0.41s      <- after, with one
```

**That equality is the whole point.** Python binds `def` names last-wins, so three definitions of
`test_every_language_has_a_frame_for_every_screen` collect as one. The count staying at 995 says the
duplicates were dead text; had it dropped, something other than a duplicate had been removed.

```
tests/test_components.py   2328 -> 2212 lines   (-116)
```

## 3. `gallery_darkside` was never stale — and the probe that "proved" it was, proved the opposite

`spec.md` §9.5 and inc41 §8 both record: *"The gallery was last baked at inc21, and `language.py` has been
edited in at least a dozen increments since. Somebody changed a glyph and never re-baked."* **That is
wrong, and the evidence offered for it is the evidence against it.**

inc39 checked `taskboard/language.py` out at the pre-batch commit `8604607`, re-ran the capture, and got
**the identical diff**. The conclusion drawn was "not this batch's doing". The conclusion available was
**the source is not involved at all** — because if reverting the source does not move the render, the
render is not reading the source's change.

It is reading the clock:

```python
class Darkside(Kit):
    PHASES = ("( )", "(.)", "(o)", "(O)", "(o)", "(.)")

    def doodle(self) -> str:
        from datetime import date
        return self.PHASES[date.today().day % len(self.PHASES)]

    def wordmark(self, text):
        wm = self.t.get("wordmark", self.c["mut"])
        return [f"[{wm}]{self.doodle()} {text.lower()}[/]"]
```

*"identity is a date-driven moon doodle on a deliberately recessive wordmark"* — `Darkside.__doc__`, the
last clause. It is doctrine, and it is doing exactly what it says.

The arithmetic closes it with nothing left over:

```
gallery_darkside.txt last written
  2817550  2026-09-05  "capture-settle inc21: pin the signature, re-bake the 22 frames"
  day 5  ->  5 % 6 = 5  ->  PHASES[5] = "(.)"     the committed cell
today
  2026-09-06
  day 6  ->  6 % 6 = 0  ->  PHASES[0] = "( )"     the re-baked cell
```

**One day old, not four months.** The diff is one glyph in one cell, in the wordmark and nowhere else:

```
-                              │  (.) gal
+                              │  ( ) gal
-<text x="287.2" y="91.3" fill="#3a3a3a">(.) gal</text>
+<text x="287.2" y="91.3" fill="#3a3a3a">( ) gal</text>
```

**Why the re-bake moved darkside and nothing else** — the answer the round asked for. Every other capture
in the sweep is a pure function of `language.py` and `_fixture_late.json`; darkside is the only kit that
reads `date.today()`, and the only screen that renders its wordmark is the gallery sheet. `board_darkside`
carries `(O)board  ( )lanes` — that is the view-selector radio, which happens to spend the same glyphs and
is not the doodle — so it did not move. **Gallery files moved: `gallery_darkside.txt`,
`gallery_darkside.svg`. The other twenty captures the plain sweep writes are byte-identical, and the
twenty-two `surface_*` files are not written by a plain run at all (`--surface` writes those) so they were
neither touched nor expected to be.**

**And the 66 component frames are safe, checked rather than assumed.** `( )` and `(O)` appear in all six
darkside frames and in `nord_S2`, but as the RADIO's off/on parts — `screens.py` builds a component sheet
and never calls `wordmark`. `render.py` re-swept all 66 in this increment and moved none.

**The re-bake does not close the item.** It re-stamps today's day-of-month onto a cell that changes six
times a month; on 2026-09-07 the committed frame is wrong again. Closing it needs the capture to pin a
date the way it already pins a synthetic fixture, or the doodle cell exempted from the comparison — **a
design change to the capture harness or to a language's identity mechanism, so it is named and left for
the operator** and carried into `spec.md` §9.5 as a live item with its real cause.

## 4. Export

```
$ python -X utf8 prototypes/export_to_skill.py                                   exit 0
  wrote C:\Users\jjgh8\.claude\skills\tui-design\assets\languages.py (22 KB, 11 languages)
  verified: 11 languages, every token, doc and family round-trips
  captures: 2 written, 64 already identical -> ...\tui-design\assets\languages
  wrote SURFACES.md (11 postures)
```

**2 written** are exactly `gallery_darkside.txt` and `gallery_darkside.svg`; **64 already identical** is
every other capture. The export agrees with the git diff on which files moved, from the other side.

## 5. Gates, verbatim

```
$ python -X utf8 -m pytest -q                                                    exit 0
993 passed, 2 skipped, 4 warnings in 33.75s
```
**Unchanged from inc41's 993/2, and that is the correct result** — the duplicates never contributed a
test. Collected count 995 before the dedupe and 995 after (§2).

```
$ python -X utf8 prototypes/verify_language.py                                   exit 0
ALL PASSED

$ python -X utf8 prototypes/components/render.py                                 exit 0
  66 .txt + 66 .svg -> ...\prototypes\components
  66 candidates files
  no two frames identical within a screen (330 pairs)
  0 hand-drawn elements declared (0 refused, 0 evoked)

$ python -X utf8 prototypes/components/matrix.py                                 exit 0
11 rows x 6 screens, every cell `implementa -`
per screen: no primitive missing in any language; refusals, by language: all []

$ python -X utf8 prototypes/capture_languages.py                                 exit 0
  22 grids identical across two PROCESSES
  22 captures -> ...\prototypes\gallery
  no two boards identical
```

**Frames changed: 0 of 66.** **Gallery files changed: 2 of 44 written by the plain sweep.**

## 6. Risks

- **The rename is invisible to the repository.** `prototypes/out/` is ignored, so a fresh clone has no
  probe and `testpaths` alone carries the fix. On this machine both hold; on another machine only one is
  even applicable. Said in the `pyproject.toml` comment so the next reader is not surprised.
- **`testpaths` narrows collection for everyone.** If a test is ever placed outside `tests/`, a bare
  `pytest` will not find it and will not say so. That is the trade taken; the suite has lived in `tests/`
  for its whole history.
- **The committed `gallery_darkside` frames are wrong on five days out of six.** Committing them was
  instructed and is done; it buys nothing durable, and §3 says why in full rather than letting the next
  round rediscover it as "stale".
- **The dedupe was a text operation on a 2300-line file.** It is defended by the collected count either
  side and by the full suite, not by reading.

## 7. Pending — carried, with corrected causes

- **`gallery_darkside` is calendar-dependent, not stale** (§3). Live. Needs a pinned date or an exempt
  cell — operator's, because it touches either the capture doctrine or a language's identity mechanism.
- **`blueprint_S4`'s destructive control has no danger mark and no focus mark in either tier** (inc41 §8).
  Untouched here.
- The sixteen language-level `rework` frames of `spec.md` §9.4. Untouched here; inc44's census annotates
  them.

## 8. Suggested next task

inc43 — teach `svg_from_grid` the style tier (`bold`, `underline`, `reverse`), which is the limit inc41
asserted as a fact and `PROTOTYPE-inheritors.md` §7 q9 puts to the operator.

---

## Evidence checklist

- [x] **Tests/type checks/lint pass** — `993 passed, 2 skipped`, exit 0 (§5). `verify_language.py`
      **ALL PASSED** exit 0. `render.py` 66 frames / 330 pairs / 0 hand-drawn, exit 0, 0 frames moved.
      `matrix.py` 66 of 66, exit 0. `capture_languages.py` 22 grids identical across two processes,
      exit 0.
- [x] **No secrets in code or output** — one config line, a text dedupe, and two re-baked captures of the
      synthetic `_fixture_late.json`. No network, no dependency, no new path.
- [x] **No destructive commands run without approval** — one `mv` inside the ignored scratch yard
      (`_b37_test.py` → `_b37_probe.py`, contents intact, quoted in §1). No deletion, no reset, no force.
- [x] **File count within cap** — 4 source files (`pyproject.toml`, `tests/test_components.py`,
      `gallery_darkside.txt`, `gallery_darkside.svg`) plus this packet: 5.
- [x] **Review packet attached** — this document.
