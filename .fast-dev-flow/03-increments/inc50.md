# Increment 50 — `solari_S4`'s band shrinks to its content instead of sliding down the page

**Batch:** `rework-4` · closes `PROTOTYPE-inheritors-2.md` §5 **C3** (and the second half of its §2.6
`solari_S4` block) · **records question F untouched**
**Files:** `taskboard/language.py`, `tests/test_components.py` — **2 source files**, plus 2 regenerated
frame artefacts and this packet.

**inc40 moved solari's announcement off the station's plate and the round measured what that cost: the
band did not shrink, it SLID three rows. It gave back the mode strip, the masthead and the head seam and
it took two more rows of board — `GATE DOING 04` and `FIX LOGIN REDIRECT` — so the surviving schedule
opened on the SEAM of a departure the band had taken, with five task rows under no gate header at all.
The band is now its content: the two empty rows `screens.s4` puts between a title, a body and its answers
are the PAGE's air and not a band's, and `MODAL_BORDER_REFUSED["solari"]` says the word — a BAND. Eight
rows become six, `GATE DOING 04` comes back at its own index, and the orphan seam is gone. The band still
covers `GATE BACKLOG 05`, the gate the confirm names; that is question F and this increment does not take
it.**

---

## 1. Cause

`Kit.overlay` hands every one of the eleven the same six rows, built once in `screens.s4`:

```python
rows = [f"[{c['ink']}]{LG.mark(F.MODAL_TITLE)}[/]", ""]
rows += [f"[{c['mut']}]{LG.mark(b)}[/]" for b in F.MODAL_BODY]
rows += ["", answers(sh)]
```

**Two of those six are empty.** Ten languages draw a lid or a rule around the words and want the air
inside it. Solari draws neither: it posts the words *as a band across the full measure*, and it wrapped
the air in the band. `Solari.overlay_instead` read

```python
block = [bar] + list(rows) + [self.seam(w)]      # 1 + 6 + 1 = eight rows
```

so the band was eight rows deep for four rows of content. inc40 fixed WHERE the block starts
(`schedule_head`, the row after the first full-measure seam) and never looked at how deep it is.

## 2. The exchange, measured

`solari_S4` and `solari_S1` differ only inside the band, so the band's depth is exactly what it costs.
Page rows (1-based) at `8753ac2`:

```
solari_S1   04   GATE BACKLOG 05              STATUS  PROJ  PRI      <- the gate the modal names
            05     21  AUDIT THE THEME TOKENS           ON TIME  LOW
            06     ▁▁▁▁… (seam)
            07     30  DROP THE LEGACY SHIM             ON TIME  NORM
            08     ▁▁▁▁… (seam)
            09   (blank — the air between gates)
            10 ▼ GATE DOING 04                 STATUS  PROJ  PRI
            11 ▼   03  FIX LOGIN REDIRECT               BOARDING HIGH
            12     ▁▁▁▁… (seam of FIX LOGIN REDIRECT)

before      band = rows 04-11 (8)   board resumes at row 12 = an ORPHAN SEAM
after       band = rows 04-09 (6)   board resumes at row 10 = GATE DOING 04
```

**The band now covers exactly the BACKLOG gate's own block** — header, two departures, their two seams,
and the blank that closes the gate — and hands the schedule back at a header. `FIX LOGIN REDIRECT` and
the detail pane's `STATUS`/`OWNER` rows are on the frame again.

```
solari_S4  after   03 ▁▁▁▁▁▁▁… (the plate's seam)
                   04 (the reverse-video bar)
                   05 Delete 3 tasks?
                   06 3 tasks will be removed from BACKLOG.
                   07 This cannot be undone.
                   08 ▔  ▀Delete▄  ▔   ▁   Cancel   ▁
                   09 ▁▁▁▁▁▁▁… (the band's closing seam)
                   10 ▼  GATE DOING 04   STATUS  PROJ  PRI   STATUS ▁▁▁… open
```

## 3. Mechanism, and why it lives at this seat

```python
said = [r for r in rows if visible(r).strip()]
block = [bar] + said + [self.seam(w)]
```

One line. **At `Solari.overlay_instead` and not in `screens.py`**, because the sheet's rows are shared by
all eleven: dropping the air there would have moved ten other frames to fix one. It is the same reasoning
inc40 used to pick this seat over `Kit.overlay` — *"ten languages share it and ten leave their page intact
through it"*.

**The citation.** `MODAL_BORDER_REFUSED["solari"]`: *"a question is posted the way a cancellation is, as a
**BAND IN REVERSE VIDEO** at the head of the schedule, with the rows still legible under it"*. A band is a
contiguous run of rows that say something. A blank row inside one is a second band, and — measured on the
page — it is a row of somebody's departure. Both halves of the doctrine are load-bearing and the second
half is the one that was still false: a schedule whose first row is the underline of a flight that is not
on it is not "the rows still legible under it".

## 4. Law

> **The band is its content.** Its depth is `1 + the rows that say something + 1` — the reverse-video bar,
> the words, the closing seam — and between the first word and the seam there is no empty row.
> **The schedule under it opens on a GATE HEADER**, at its own index, byte for byte the page's — not on a
> seam and not on a task row.
> **It is still an overlay**: every row outside the band is the page's row at the same index (inc40's
> second half, re-asserted, because a "shrink" implemented by INSERTING rows would satisfy the second
> clause and push the whole board down).

`test_solaris_band_is_its_content_and_the_board_under_it_opens_on_a_gate`, measured on the shipped
`solari_S4.txt` against the shipped `solari_S1.txt` — the same evidence base as inc40's laws. A gate
header is matched as a SHAPE (`GATE [A-Z]+ \d\d\s`) rather than compared to this fixture's three gate
names, so the law survives a fixture that renames a gate.

**What the law does NOT say, and it is deliberate.** The band still covers `GATE BACKLOG 05`, which is the
gate the confirm names (*"3 tasks will be removed from BACKLOG"*). **At 100×32 an overlay band at the head
of the schedule cannot avoid it, because the gate header IS the schedule's first row** — the plate's seam
is row 3 and the header is row 4. The three ways out are all design changes: place the band below the
first gate (it is then not at the head of the schedule), insert instead of overlay (it is then not an
overlay), or let the announcement name a gate it does not cover. **That is round question F and it is the
operator's; this increment records it and does not decide it.**

## 5. Teeth

`test_an_unshrunk_band_leaves_the_schedule_opening_on_an_orphan_seam` restores the pre-inc50 body exactly
— `[bar] + list(rows) + [seam]`, `schedule_head` untouched — and hands it **the block `screens.s4` really
hands it**, rebuilt from the shipped frame by `solari_s4_rows()` rather than a three-row stand-in, because
the whole finding is about how many rows the block occupies and a stand-in whose length was chosen in the
test would be the test deciding its own outcome.

It names what goes wrong:

```python
assert len(band) == 8 and band[0] == 3, band          # the head is the same
eaten = [s1[i] for i in band]
assert any("GATE DOING 04" in r for r in eaten), eaten
assert any("FIX LOGIN REDIRECT" in r for r in eaten), eaten
orphan = out[band[-1] + 1]
assert not _GATE_HEAD.search(orphan), orphan
assert set(orphan.strip()) == {"▁"}, orphan           # a seam, not a gate
```

**`band[0] == 3` under both bodies is what says this is a LENGTH finding and not a re-run of inc40's
anchor finding.** The head does not move; the foot does.

**And the law itself was watched fail on the real declaration.** Reverting the one line to
`block = [bar] + list(rows) + [seam]`, re-rendering, and running the law:

```
$ python -X utf8 -m pytest "tests/test_components.py::test_solaris_band_is_its_content_and_the_board_under_it_opens_on_a_gate" -q
>       assert len(band) == len(said) + 1, (band, said)      # +1: the blank bar
E       AssertionError: ([3, 4, 5, 6, 7, 8, ...], [4, 6, 7, 9, 10])
E       assert 8 == (5 + 1)
1 failed in 0.29s
```

`language.py` was restored from a byte copy taken before the edit and `render.py` re-run; the law is green
again and `git diff --stat` is the 26/1 line change plus the two frame artefacts.

## 6. Frames changed

**`solari_S4` only** — `.txt` and `.svg`. Two blank rows leave the band and `GATE DOING 04` /
`FIX LOGIN REDIRECT` come back at their own indices; the frame is still 32 rows. Ink 22.8% → **26.8%**,
which is the board coming back, not the band growing.

**Gallery: 0 of the 22 moved.** `overlay_instead` is not on the board path.

## 7. Gates, verbatim

```
$ python -X utf8 -m pytest -q
1 failed, 1042 passed, 2 skipped, 4 warnings in 34.36s
FAILED tests/test_app.py::test_win_clipboard_roundtrip - AssertionError: assert None == 'roundtrip 123 ABC taskboard'

$ python -X utf8 prototypes/verify_language.py                                        exit 0
ALL PASSED

$ python -X utf8 prototypes/components/render.py                                      exit 0
  66 .txt + 66 .svg -> ...\prototypes\components
  66 candidates files
  no two frames identical within a screen (330 pairs)
  0 hand-drawn elements declared (0 refused, 0 evoked)

$ python -X utf8 prototypes/components/matrix.py                                      exit 0
  11 x 6 = 66 cells, every one `implementa`; refusals [] for all eleven

$ python -X utf8 prototypes/capture_languages.py                                      exit 0
  22 grids identical across two PROCESSES
  22 captures -> ...\prototypes\gallery
  no two boards identical
  -> 0 of the 22 moved

$ python -X utf8 prototypes/collision_census.py                                       exit 0
  TOTAL  47 -> 47      (no declaration changed; this is a composition increment)
```

**`1040 → 1042`:** the law and its teeth. The clipboard red is `test_win_clipboard_roundtrip`,
environment-coupled (spec §10.6), red at `a8a7a5d` before this batch began — **reported, not counted, not
touched**.

## 8. Risks

- **The title lost its air.** `Delete 3 tasks?` now sits directly above the body, separated by tier
  (`ink` against `mut`) and by nothing else. On a board where everything is caps and every divider is the
  same seam, that is one channel where there were two. The defence is the doctrine — a cancellation band
  is a solid strip — but it is a real trade and it is the operator's to reject in one line.
- **The band lands exactly on the BACKLOG gate's block (6 rows for 6 rows), and that is measured, not
  constructed.** Nothing in the code makes the band's foot land on a gate boundary; the law ASSERTS it and
  the teeth prove the assertion is caused by this change. A fixture with a different number of departures
  in its first gate would go red on clause 2 — which is the law working, and it is worth knowing that the
  answer would then be a design question (does the band take whole gates?) and not a one-line fix.
- **Question F is untouched and the frame still shows it.** The confirm says `3 tasks will be removed from
  BACKLOG` and `GATE BACKLOG 05` is under the band. Nothing here makes that better or worse; it is two
  rows nearer the reader than it was, because the band is shorter.

## 9. Found by looking, not fixed

- **`screens.s4`'s two empty rows are the page's air and ten languages depend on them.** They are now
  dropped by exactly one kit, at that kit's own seat. If a second language ever wants the same, the
  honest move is a kit-level predicate and not a second copy of this line — named here so the copy does
  not happen silently.
- **`solari_S4`'s ink went UP by 4 points** (22.8 → 26.8) while the modal got smaller. Density on this
  language is a board-coverage measure, not a modal one, which is worth remembering the next time a
  density figure is read as a verdict.

## 10. Pending — not this increment

- **K3, the stepper's law** — inc51.
- **Decisions A, C, D, E, F, G and finding C1** are the operator's and untouched. **F is the one this
  increment came closest to** and §4 records exactly why it stopped.
- **C2 (`swiss_S4`'s modal opens and never closes)**, **C4**, **C5**, **C6**, **C7** — the other
  composition findings of §5, none of them on this batch's list.

## 11. Suggested next task

**inc51 — the stepper's law, and `Kit.PART_GLYPHS["stepper.step"][INVALID] = "]["`** (K3).

---

## Evidence checklist

- [x] **Tests/type checks/lint pass — WITH ONE RED, NAMED.** `1042 passed, 2 skipped, 1 failed`; the
      failure is `tests/test_app.py::test_win_clipboard_roundtrip`, environment-coupled (spec §10.6),
      red before this batch began — reported, not counted, not touched. `verify_language.py` ALL PASSED
      exit 0. `render.py` 66/330/0. `matrix.py` 66 of 66. `capture_languages.py` 22 captures, 0 moved.
      `collision_census.py` 47 → 47.
- [x] **No secrets in code or output** — one list comprehension in a kit method and one test block. No
      network, no new dependency, no path outside the worktree.
- [x] **No destructive commands run without approval** — none. No checkout, no reset, no delete, no
      force, no process killed. The revert-and-watch-it-fail experiment used a byte copy of
      `language.py` and restored from it; `git diff --stat` confirms the tree.
- [x] **File count within cap** — 2 hand-written source files (`taskboard/language.py`,
      `tests/test_components.py`); the 2 frame artefacts are written by `render.py`.
- [x] **Review packet attached** — this document.
