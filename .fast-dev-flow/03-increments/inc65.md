# Increment 65 — the band stops eating gate headers, and corgi keeps its mode strip

**Batch:** `rework-6a`, increment 3 of 4 · **F amended** (`solari_S4`, C3') and **C8** (`corgi_S4`),
both new in `PROTOTYPE-inheritors-3.md`.
**Files:** `taskboard/language.py`, `tests/test_components.py` — **2 source files**, plus 4 regenerated
component artefacts (`solari_S4`, `corgi_S4`, `.txt` and `.svg`) and this packet. **0 gallery artefacts.**

**`solari_S4` did not fail to say which gate a task was in — it said the wrong one.** inc55 anchored the
confirm band ON the first gate the confirm does not name, so `GATE DOING 04` and three of its four
departures went under the band and the fourth, `14  REWRITE THE ONBOARDING`, stood under the only header
left above it: `GATE BACKLOG 05`. **`corgi_S4` was the one frame of the sixty-six that could not answer
"which mode is this?"** — thirteen blank rows, the confirm, thirteen more, seven text runs in the whole
`.svg` — under an exemption from inc40's head law that its kit had earned with a sentence about the
BOARD. The anchor moves one row down; the mode strip comes back and the board stays gone. Suite
1147 → 1151.

---

## 0. Rulings (orchestrator, 2026-09-07, on the operator's delegation)

> **E4:** the exporter reads the kit's declared `ground` and `ink`; it never infers them from frequency.

> **F, amended:** the band never covers a gate HEADER row, of any gate; it covers task rows of the first
> gate the confirm does not name, below that gate's header, and goes to the foot of the schedule when no
> such rows exist. A frame must never show a task under a gate it does not belong to.

> **G vs ruling 10:** on S4 the fixture mood is calm; G applies to S2 only. Recorded, no code.

> **inc60 info to air:** doctrine for blueprint and ledger (a line-type ladder where absence is the calm
> state, LANGUAGES.md §11 and #9). Recorded, no code.

> **C, follow-through:** the channel C freed on swiss gets filled: the invalid text field has a wall,
> paper and a closer from swiss's own alphabet.

This increment carries out **F amended** and **C8**.

## 1. The frames, read before anything was written

```
solari_S4, before (f1508ad)                     solari_S4, after
 04    GATE BACKLOG 05   STATUS  PROJ  PRI       04    GATE BACKLOG 05   STATUS  PROJ  PRI
 05     21  AUDIT THE THEME TOKENS  ON TIME      05     21  AUDIT THE THEME TOKENS  ON TIME
 07     30  DROP THE LEGACY SHIM    ON TIME      07     30  DROP THE LEGACY SHIM    ON TIME
 10  <the band's bar -- GATE DOING 04 gone>      10  ▼  GATE DOING 04   STATUS  PROJ  PRI
 11  Delete 3 tasks?                             11  <the band's bar>
 12  3 tasks will be removed from BACKLOG.       12  Delete 3 tasks?
 13  This cannot be undone.                      13  3 tasks will be removed from BACKLOG.
 14  ▔  ▀Delete▄  ▔   ▁   Cancel   ▁             14  This cannot be undone.
 15  <the band's seam>                           15  ▔  ▀Delete▄  ▔   ▁   Cancel   ▁
 16      ▁▁▁▁▁ (an orphan seam)                  16  <the band's seam>
 17      14  REWRITE THE ONBOARDING   <- filed   17      14  REWRITE THE ONBOARDING  <- filed
 18      ▁▁▁▁▁                          BACKLOG  18      ▁▁▁▁▁                        DOING
 20    GATE BLOCKED 00                           20    GATE BLOCKED 00
```

```
corgi_S4, before                                 corgi_S4, after
 01  (blank)                                     01  [1]B O A R D [2]FORM [3]CFG [4]LOG
 02-13 (blank)                                   02-13 (blank)
 14  Delete 3 tasks?                             14  Delete 3 tasks?
 16  3 tasks will be removed from BACKLOG.       16  3 tasks will be removed from BACKLOG.
 17  This cannot be undone.                      17  This cannot be undone.
 19  ▛▛ █Delete█ ▜▜   ▒▒  Cancel  ▒▒             19  ▛▛ █Delete█ ▜▜   ▒▒  Cancel  ▒▒
 20-32 (blank)                                   20-32 (blank)
```

Measured before the change: **ten of the eleven S4 frames keep row 1; corgi did not.** That is inc40's
head law with one exemption in it, and the exemption is the whole finding.

## 2. Cause and mechanism — F amended

**Cause.** `Solari.band_head` (inc55) returned the INDEX OF THE HEADER of the first gate the confirm does
not name:

```python
for i, gate in heads:
    if gate != named:
        return i
```

The band is six rows, so it started on `GATE DOING 04` and ran through three of that gate's departures.
inc55 declared one cost in writing — the band's foot lands inside the gate, so the row under it is an
orphan seam — and that cost is real and still paid. **It did not declare this one**, and this one is
different in kind: the frame stops being silent and starts being wrong. A reader asked "which gate is
`REWRITE THE ONBOARDING` in?" gets `BACKLOG` from the picture and `DOING` from the fixture.

**Mechanism.** Two changes in `band_head`:

- **the anchor is `i + 1`** — the row below the header, so the header stands and the gate a departure
  belongs to is the gate whose header is above it again;
- **the candidate must FIT.** The amendment forbids covering a header *of any gate*, so a gate whose
  block is shorter than the band would push it onto the NEXT gate's header. The next header's index is
  checked (`i + 1 + depth <= nxt`) before the anchor is taken, and a gate that cannot hold the band is
  passed over. With no candidate left, ruling F's own fallback stands: `schedule_foot`.

`about=None` still returns `schedule_head`, so the other ten languages and every caller that says
nothing render byte for byte what they rendered before.

## 3. Cause and mechanism — C8

**Cause.** `Corgi.overlay_instead` wrote `[""] * y + list(rows)` — the page was dropped entirely, on the
strength of `MODAL_BORDER_REFUSED["corgi"]`: *"a dialog floating over a board is two modes at once … so a
confirm is a MODE and the board is gone"*. inc40 read that sentence as covering the head law and wrote
corgi into `MODAL_KEEPS_NOTHING`.

**The sentence is about the BOARD.** Row 1 of this page is `[1]BOARD [2]FORM [3]CFG [4]LOG` — the strip
that says which mode the operator is in. A confirm that erases it is a MODE that has erased the mode
indicator, which is the one thing this doctrine cannot want. And the criterion inc40 wrote its own law
for is *"a destructive confirm is precisely when the operator needs to know which mode the question came
from"* — a criterion corgi failed while holding an exemption from the law that carries it.

**Mechanism.** `overlay_instead` keeps `under[0]` and centres the block below it (`y = max(1, …)`).
Nothing else of the page survives: no panes, no schedule, no detail, no pager, no meter, and no dimmed
backdrop. The refusal's other half is intact and is now asserted where it belongs.

## 4. The laws

**`test_solari_never_files_a_departure_under_the_wrong_gate`** — the amendment's second sentence, over
`solari_S1` **and** `solari_S4`.

- **Membership comes from the fixture, position from the frame.** `fixture.py` is loaded BY PATH
  (`importlib`, not `sys.path` — `fixture` is not a name this test session should own) so a law does not
  carry its own copy of "REWRITE THE ONBOARDING is in DOING" and go on passing after somebody moves it.
- **The gate a row is in is read the way a person reads it**: the nearest header above, found with the
  kit's own `gate_of`, which parses this language's header format rather than the page's English.
- **S1 is the control.** With no band on the page all six departures must file correctly, or the reader
  is wrong rather than the composition.
- **Non-vacuity is asserted, not assumed.** S4 must show exactly three departures and one of them must
  be `Rewrite the onboarding` under `DOING` — the task that was mis-filed. An arm that lost that row
  would prove nothing about the defect and goes red instead.
- **The detail pane is excluded, and that is not tidying.** Row 4 of every solari sheet is
  `GATE BACKLOG 05 … DETAIL  FIX LOGIN REDIRECT`: the gate header and the detail caption share a row, so
  the selected task's title appears on a header line in all six frames. Header rows are skipped, with
  the reason in the reader's docstring. (Found by watching the first version of this law go red on
  `('S4', 'Fix login redirect', None, 'DOING')`.)

**`test_no_gate_header_stands_inside_solaris_band`** — the amendment's absolute half, *of ANY gate*.
Read off the shipped frame against the shipped page: no row the band covers is a header, the row above
the band is one, and it is `DOING`.

**Clause 2 of `test_solaris_band_is_its_content_and_stands_at_a_gates_head` moved with the ruling**:
`inc50` asserted the row BELOW the band is a header, `inc55` the row the band STARTS on is one, and
inc65 asserts the row ABOVE the band is one and no row inside it is. Written into the test rather than
into a commit message, because a clause that quietly got weaker is how a law becomes decoration.

**`test_a_modal_leaves_the_pages_first_row_alone` is asked of all eleven now.** The `MODAL_KEEPS_NOTHING`
branch is deleted; the roster survives, renamed `MODAL_KEEPS_ONLY_THE_HEAD`, and says which language
keeps *only* row 1. The refusal's citation (`"the board is gone"`, word for word) moved with it into
**`test_corgis_confirm_keeps_the_mode_strip_and_nothing_else`**, which asserts both halves: row 0 comes
back at its own index, and no other row of the page appears anywhere in the output.

## 5. Teeth

**`test_the_wrong_gate_law_bites_on_the_anchor_inc55_shipped`** installs inc55's `band_head` body
verbatim (`for i, gate in heads: if gate != named: return i`) on the real kit and runs the real block
over the real page:

```
filed["Rewrite the onboarding"] == ("BACKLOG", "DOING")     # the frame says BACKLOG
[i for i in band if _GATE_HEAD.search(s1[i])] == [band[0]]  # a header, inside the band
```

then undoes the patch and asserts the same task comes back `("DOING", "DOING")`. Not an approximation of
the previous behaviour — it is the previous behaviour.

**The corgi law's teeth are the existing head law**, now with no exemption in it: reverting
`Corgi.overlay_instead` puts `0` back into `modal_band("corgi")` and
`test_a_modal_leaves_the_pages_first_row_alone[corgi]` goes red. Watched by hand before the roster was
renamed — that arm was the first thing to fail when the exemption branch was deleted and the kit had not
yet moved.

## 6. Frames changed

| frame | what moved |
|---|---|
| `solari_S4` `.txt` `.svg` | the band moves from rows 10–15 to 11–16; `GATE DOING 04` is back on the page and `14 REWRITE THE ONBOARDING` is under it |
| `corgi_S4` `.txt` `.svg` | row 1 is `[1]B O A R D [2]FORM [3]CFG [4]LOG` instead of blank; the board is still gone |

**Nothing else, and the reason is checkable:** `band_head` is `Solari`'s and is only reached when a
caller passes `about=`, which only `screens.s4` does; `overlay_instead` is `Corgi`'s and only S4 calls
it. `capture_languages.py` was re-run anyway because `taskboard/language.py` moved —
`git status --porcelain prototypes/gallery/` came back **empty**.

**Gallery 30–51 in the skill:** untouched; `export_to_skill.py` runs at the close of the batch.

## 7. Gate tails, verbatim

```
$ python -X utf8 -m pytest -q
FAILED tests/test_app.py::test_win_clipboard_roundtrip - AssertionError: assert None == 'roundtrip 123 ABC taskboard'
1 failed, 1151 passed, 2 skipped, 4 warnings in 33.85s

$ python -X utf8 prototypes/verify_language.py
ALL PASSED
                                                        (exit 0)

$ python -X utf8 prototypes/components/render.py
  66 .txt + 66 .svg -> ...\prototypes\components
  66 candidates files
  no two frames identical within a screen (330 pairs)
  0 hand-drawn elements declared (0 refused, 0 evoked)
                                                        (exit 0)

$ python -X utf8 prototypes/components/matrix.py
  66 of 66 · refusals [] for all eleven                 (exit 0)

$ python -X utf8 prototypes/collision_census.py
TOTAL                       25
TOTAL homoglyph rows             1
                                                        (exit 0)

$ python -X utf8 prototypes/capture_languages.py
  22 grids identical across two PROCESSES
  22 captures -> ...\prototypes\gallery
  no two boards identical
                                                        (exit 0)

$ git status --porcelain prototypes/gallery/
                                                        (empty)
```

Suite **1147 → 1151** (+2 membership arms, +1 header arm, +1 teeth; one existing test renamed, three
amended). Census **25**, homoglyph rows **1**: no declaration moved.

## 8. Risks

1. **`schedule_foot` is still not header-safe.** F's fallback puts the band at the foot of the schedule,
   and nothing checks that the foot does not land on `GATE DONE 07`. No frame in this repo reaches that
   branch (the fixture's confirm names one of four gates) and the ruling names the foot as the fallback,
   so it is left as the ruling wrote it — **said out loud rather than discovered later**.
2. **The band still ends inside a gate.** The orphan seam inc55 declared is still there, one row lower:
   the row under the band is a departure's seam. That is the price of ruling F and it is unchanged by
   the amendment.
3. **corgi's confirm now shows a row of a page it claims is gone.** The doctrine is split, deliberately,
   between "the board is gone" (kept, and asserted) and "the mode strip is not the board" (new). Anyone
   who reads the refusal as covering the whole page is disagreeing with C8, not with this code.
4. **`tasks_as_filed` matches titles by substring.** Two fixture tasks whose titles were prefixes of one
   another would confuse it. Measured on the six: no title is a substring of another.

## 9. Found by looking, not fixed

- **`corgi_S4`'s focus ring is still the text field's walls.** `▛▛ █Delete█ ▜▜` — the irreversible
  answer is ringed with the pair `corgi_S2`'s normal field and `corgi_S6`'s query field use. Named by the
  round as `corgi_S4`'s second objection; it is a declaration, not a composition, and it is not C8.
- **`solari_S4`'s rows 12–15 still have no air** — `Delete 3 tasks?`, the body and the buttons run
  together, separated only by tier. Declared by inc50 (the band is its content, the page's air is not the
  band's) and named again by round three. Unchanged and still declared.
- **inc40's head law had an exemption for five batches and nobody re-read the sentence under it.** The
  exemption was written correctly, cited correctly and asserted word for word; what nobody asked was
  whether the sentence it cited covered the thing it was exempting. A citation check is not a scope
  check, and this is the second time in this batch that a law was resting on something it had not
  measured (the first was §5 of inc63).
- **`GATE DONE 07` still shows a header with nothing under it** on every solari sheet, and
  `GATE BLOCKED 00` shows `NO DEPARTURES` — the schedule spends two rows per departure, so six of sixteen
  fit. Doctrine, declared, unchanged.

## 10. Pending — not this increment

- **inc66** — the S4 walls (C2, `ledger_S4` and `swiss_S4`) and swiss's freed channel.
- The batch close: `export_to_skill.py`, `spec.md` §16.
- K5, L6, L7, L10, C5–C7, C9, C10, E2, E3, G1, G2 — open.

## 11. Suggested next task

`inc66`, as briefed: both answer buttons in every S4 open and close with the language's declared pair for
their state, at three widths; and swiss's invalid field gets paper and a closer from its own alphabet.

## Evidence checklist

- [x] **Tests/type checks/lint pass — WITH ONE RED, NAMED.** `1151 passed, 2 skipped, 1 failed`
      (inc64 closed at `1147 passed`). The failure is
      `tests/test_app.py::test_win_clipboard_roundtrip`, environment-coupled (spec §10.6) — **reported,
      not counted, not touched.** `verify_language.py` ALL PASSED exit 0. `render.py` 66 frames / 330
      pairs / 0 hand-drawn. `matrix.py` refusals `[]` for all eleven. `capture_languages.py` plain: 22
      captures, 22 grids identical across two processes, **0 artefacts moved**.
      `collision_census.py` both self-checks green, TOTAL 25, homoglyph rows 1.
- [x] **No secrets in code or output** — one anchor moved by one row with a fit check, one overlay
      keeping one row, two laws, one teeth, one roster renamed, three tests amended. No network, no new
      dependency, no path outside the worktree.
- [x] **No destructive commands run without approval** — none.
- [x] **File count within cap** — **2 source files**: `taskboard/language.py`,
      `tests/test_components.py`.
- [x] **Review packet attached** — this document.
