# Increment 40 — an overlay covers a band; it does not eat the page's head

**Batch:** `rework-1` · `PROTOTYPE-inheritors.md` §2.6 `solari_S4` (*"el defecto más grave de los 42"*), §7 q4
**Files:** `taskboard/language.py`, `tests/test_components.py` — **2 source files.**

**`solari_S4` opened on a blank row. Its announcement band was anchored at screen index 0, so it landed on
the mode strip, the masthead and the head seam and they were gone — the one frame of the sixty-six that
could not answer "which mode is this?". The band still takes the head of the board, which is solari's
declared doctrine; `schedule_head` is what now says WHICH head, by finding the board's own plate instead of
assuming it is not there. Ten of the eleven kept row 1 before this increment and eleven do now, with corgi
exempt by its own citation.**

---

## 1. The round said "shifted"; it was a clobber, and its own evidence proves it

§2.6: *"El modal no se superpuso: **desplazó y descartó**."* The first half is right and the second is
worth correcting, because it changes where the defect lives.

Nothing shifted. `Solari.overlay_instead` read:

```python
block = [bar] + list(rows) + [self.seam(w)]
for i in range(h):
    if i < len(block):
        out.append(block[i])                       # under[i] dropped
    else:
        out.append(self.recede(under[i] ...))      # under[i], at index i
```

Rows `0..len(block)-1` were **replaced in place**; every row below came back **at its own index**. That is
exactly why *"la fila 9 de `S4` es la fila 9 de `S1`, byte a byte"* — the observation the round offered as
proof of a shift is proof there was none. A shift would have moved row 9 to row 17. The page was not
pushed off the top; **its head was written over.**

This matters because a shift would be a bug in the composition (`Kit.overlay`) and a clobber is a bug in
the PLACEMENT (`Solari.overlay_instead`). Measured across the eleven, on the shipped frames:

```
              band (rows S4 changes)   contiguous   row 1 kept
naught             13-20                  yes          yes
corgi               1-31                  yes          NO   <- declared: "the board is gone"
instrument         13-20                  yes          yes
swiss              13-20                  yes          yes
industrial         13-20                  yes          yes
nord               13-20                  yes          yes
darkside           13-20                  yes          yes
prism              13-20                  yes          yes
ledger             26-32                  yes          yes   <- declared: "at the foot"
solari              1-8                   yes          NO   <- the defect
blueprint          11-18                  yes          yes
```

**`Kit.overlay` and `screens.py` are innocent and the table is the proof:** ten languages go through the
same `s4` builder, the same `_under()`, the same `Kit.overlay` dispatch, and ten of them leave a
contiguous band with the page intact around it. Only solari's own override places that band on row 0.

---

## 2. The fix, and why it is a bug fix and not a design change

Solari's doctrine is declared twice and this increment keeps both. `MODAL_BORDER_REFUSED["solari"]`:

> *"a question is posted the way a cancellation is, as a BAND IN REVERSE VIDEO at the head of the schedule,
> **with the rows still legible under it**"*

Both halves are load-bearing and **the second one was false**. The rows above the band were not legible
under anything — they were gone. And the citation says *"at the head of the **schedule**"*, which the code
implemented as *"at the head of the **screen**"*. On this board those are not the same row: the station's
own plate — the mode strip, `BOARD 16 TASKS · 4 PROJECTS`, and the seam that closes them — stands above
the schedule, and an announcement has never covered a station's name on any board that ever hung in a
concourse.

```python
def schedule_head(self, under: list[str]) -> int:
    for i, r in enumerate(under):
        body = visible(r).rstrip()
        if body and set(body) == {self.SEAM}:
            return i + 1
    return 0
```

**The plate is FOUND, not COUNTED.** This language's whole divider vocabulary is the seam, so the plate is
exactly what stands above the first *full-measure* seam — a row that is nothing but `SEAM`, edge to edge.
Reading it off the page rather than typing `3` means a masthead that grows a line does not need this method
edited. On solari's page it returns **3**; the indented row seams (`    ▁▁▁▁…`, row 12) are not
full-measure and are correctly ignored.

The placement then takes the base's own idiom — `y <= i < y + len(block)` — which is also what keeps this an
overlay: **every row outside the band is still `under[i]` at the same index, so nothing shifts.**

A page with **no** full-measure seam has no plate to protect and the band takes the top: the pre-inc40
behaviour, kept as the honest answer to "nobody said". `tests/test_components.py`'s synthetic `UNDER` is
such a page, which is why the seven inc17 overlay laws are untouched — asserted, not assumed
(`assert k.schedule_head(UNDER) == 0`).

### The frame

```
before                                  after
 1| (blank)                              1| BOARD  form  cfg  log
 2| Delete 3 tasks?                      2| BOARD  16 TASKS  ·  4 PROJECTS
 3| (blank)                              3| ▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁
 4| 3 tasks will be removed from BACK…   4| (the announcement band)
 5| This cannot be undone.               5| Delete 3 tasks?
 6| (blank)                              6| (blank)
 7| ▔  ▀Delete▄  ▔   ▁   Cancel   ▁      7| 3 tasks will be removed from BACK…
 8| ▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁       8| This cannot be undone.
 9| PRIORITY ▁▁▁▁▁▁                      9| (blank)
                                        10| ▔  ▀Delete▄  ▔   ▁   Cancel   ▁
                                        11| ▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁
                                        12| (the schedule, from row 12 on)
```

---

## 3. The laws

`tests/test_components.py`, four tests.

**`test_a_modal_changes_one_contiguous_band_of_the_page`** (all eleven, off the frames) — the rows S4
changes relative to the page form ONE contiguous run. A composition that wrote the question and then
appended the page would return `h` rows of plausible-looking board with every row below the question one
off, and `test_an_overlay_returns_the_rectangle_it_was_asked_for` would stay green through it.

**`test_a_modal_leaves_the_pages_first_row_alone`** (all eleven) — the head law. Row 1 is where every one
of these languages puts the mode strip, and a destructive confirm is precisely when the operator needs to
know which mode the question came from.

**The exemption is named and its citation is checked**, which is the shape inc38 established:

```python
MODAL_KEEPS_NOTHING = ("corgi",)
...
assert "the board is gone" in LG.MODAL_BORDER_REFUSED[lang]
assert 0 in modal_band(lang)          # and the exemption does work
```

corgi has declared that a confirm is a MODE and the board is gone; solari has declared the opposite, so it
does not get the exemption. Ledger, which posts at the foot, passes without needing one.

**`test_solaris_announcement_takes_the_head_of_the_schedule_not_the_screen`** — the unit law, asked against
solari's own shipped page rather than a synthetic backdrop, because the claim is about a real masthead.

**`test_anchoring_solaris_band_at_row_zero_eats_the_boards_own_plate`** — the teeth. `schedule_head → 0`
**is** the pre-inc40 body (`if i < len(block)` is `0 <= i < len(block)`), so the arm restores the defect
exactly rather than approximating it, and it reproduces the round's own evidence:

```python
assert out[0].rstrip() != raw[0].rstrip()
assert not any(raw[0].strip() in r for r in out)     # the mode strip is GONE
assert out[8].rstrip() == raw[8].rstrip()            # ... and row 9 is row 9
```

The same arm asserts the other ten are untouched, which is what says the fix is solari's and not the base's.

### One thing the tests had to learn: a page is markup, not text

Feeding the raw `.txt` rows as `under` went red on industrial. `recede()` calls `visible()`, and a page
with a literal `[` in it (industrial's `[21d]`, nord's `[x]`) has those runs read as style tags and eaten
— the module's own **pitfall A1, from the caller's side**. The tests pass the page through `LG.mark()`,
which is what a sheet does. Worth recording: any future law that hands a frame back to a kit has the same
trap.

---

## 4. Frames changed

```
 M prototypes/components/solari_S4.svg      28 +++----
 M prototypes/components/solari_S4.txt       6 +-
```

**Two files, and no others.** `solari_S4` is the only frame whose composition changed; `render.py` re-swept
all 66 and the other 64 came back byte-identical.

---

## 5. Gates, verbatim

```
$ python -X utf8 -m pytest -q
979 passed, 2 skipped, 4 warnings in 34.30s
```
(inc39's 955 + 24: eleven contiguity cases, eleven head cases, the solari unit law, the teeth.)

```
$ python -X utf8 prototypes/verify_language.py                                   exit 0
ALL PASSED
```

```
$ python -X utf8 prototypes/components/render.py                                 exit 0
  66 .txt + 66 .svg -> ...\prototypes\components
  66 candidates files
  no two frames identical within a screen (330 pairs)
  0 hand-drawn elements declared (0 refused, 0 evoked)
```

```
$ python -X utf8 prototypes/components/matrix.py                                 exit 0
11 rows x 6 screens, every cell `implementa -`; no missing primitives, no refusals
```

`capture_languages.py` was **not** run: no kit's board rendering changed. `overlay_instead` is reached only
from `Kit.overlay`, whose only call sites are `screens.s4` and `screens.s4_blueprint`.

---

## 6. Risks

- **The band still covers `GATE BACKLOG`.** Any 8-row band at the head of the schedule does. The round's
  second criterion — *"de qué gate se borra"* — is now answerable only from the modal's own words
  (`3 tasks will be removed from BACKLOG.`), not from the board behind it. Moving the band anywhere else
  would contradict solari's citation, so **this is §7 q4's remainder and it is the operator's**: either
  "the announcement takes the head of the schedule" stands and the gate header is an acceptable casualty,
  or the band goes where ledger's goes and the doctrine is rewritten.
- **`schedule_head` reads the page.** It is a heuristic over content, not a contract — the first
  full-measure seam. A page that opened with a seam would put the band at row 2; a page that ruled its
  masthead with something other than `SEAM` would fall back to row 0 and the defect would return silently.
  The fallback is documented and asserted, but it is a fallback, and nothing forces a solari page to have
  a head seam.
- **`schedule_head` is a new public seat on one language.** No other kit has it and nothing calls it but
  solari's own `overlay_instead`. If a second language ever needs "where does my content start", this is
  the wrong shape for it and it should move to `Kit`.
- **The head law is asked of the frames, not of the mechanism.** A language could satisfy it on the
  shipped `S4` and violate it on a page nobody photographed. The solari unit law and its teeth run against
  the real kit, but the other ten are held only by their frames.

## 7. Pending — found by looking, not fixed

- **The announcement band is invisible in the `.txt`.** `bar` is `mark(' ' * w)` under a colour tag, so in
  the artefact the house calls the work it is an **empty row** — row 4 of `solari_S4.txt` is blank. Solari's
  modal signature, the thing its whole refusal is built on, does not exist in the `.txt` at all. This is the
  same class of finding as blueprint's knockout (§10 of `PROTOTYPE.md`, and inc41) and it belongs with
  §7 q10, not here.
- **`overlay_instead` builds its band by hand instead of calling `band_row`.** `Solari.band_row` exists,
  is documented as *"the one treatment a flap board uses to head a block"*, and takes text — and
  `overlay_instead` reimplements it inline **with a different background**: `band_row` reverses on
  `c['ink']`, the overlay's `bar` reverses on `c['accent']`. Two treatments for one declared mark. Not
  touched: unifying them changes a colour in a frame, which is a design call.
- **`prototypes/out/_b37_test.py` still makes `pytest -q` mutate the suite** (inc39 §9). Neutralised by
  hand again for this commit.

## 8. Suggested next task

inc41 — `blueprint_S4`'s knockout: whether the `.txt` and the `.svg` disagreeing about which control is
the knockout is a defect or a documented consequence of the exporter, and a law that the tier a control
carries in the `.svg` is the tier the kit declared for it.

---

## Evidence checklist

- [x] **Tests/type checks/lint pass** — `979 passed, 2 skipped` (§5). `verify_language.py` **ALL PASSED**,
      exit 0. `render.py` 66 frames / 330 pairs / 0 hand-drawn, exit 0. `matrix.py` 66 of 66, exit 0.
      Teeth run: the pre-inc40 placement loses the mode strip and returns row 9 as row 9 (§3).
- [x] **No secrets in code or output** — one method added, one rewritten, four tests. No network, no
      dependency, no path outside the worktree.
- [x] **No destructive commands run without approval** — none. `solari_S4.{txt,svg}` were rewritten by
      `render.py`, which owns them. `tests/test_components.py` restored from a snapshot after `pytest` to
      undo the self-append of inc39 §9.
- [x] **File count within cap** — 2 source files (`taskboard/language.py`, `tests/test_components.py`)
      plus this packet: 3. Frames are generated artefacts.
- [x] **Review packet attached** — this document.
