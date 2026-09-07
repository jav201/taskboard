# Increment 62 — close the batch (phase C)

**Batch:** `rework-5c`, closing increment
**Files:** `.fast-dev-flow/spec.md` (§15), `prototypes/components/PROTOTYPE-inheritors-2.md` (decision
**A** marked RULED) and this packet. **No source file touched** — this increment re-runs every gate,
records what four increments did, and installs nothing new.

**All eleven languages are ZERO on both seat rosters. The three laws pass 11 of 11 each — 33
parametrised arms — on two exemptions, both by name and both cited. Census TOTAL 33 → 25, homoglyph
rows 4 → 1. Suite 1099 → 1111. `export_to_skill.py` idempotent on re-run. The skill repo was not
committed and `49_darkside-modal-rounded-lid` is stale for the fourth batch running, for reasons no
increment of this batch created.**

---

## 1. The three laws, re-run

```
$ python -X utf8 -m pytest -q -p no:randomly tests/test_components.py \
    -k "meaning_marks_do_not_share_a_cell or meaning_never_stands or no_control_opens"
33 passed, 724 deselected in 0.20s
```

Three laws × eleven languages. **11 of 11 each, and no law is scoped to the languages that already
obey it.**

```
$ python -X utf8 prototypes/out/_roster.py
=== naught      opener=0  named=0        === darkside    opener=0  named=0
=== corgi       opener=0  named=0        === prism       opener=0  named=0
=== instrument  opener=0  named=0        === ledger      opener=0  named=0
=== swiss       opener=0  named=0        === solari      opener=0  named=0
=== industrial  opener=0  named=0        === blueprint   opener=0  named=0
=== nord        opener=0  named=0
```

**Every exemption is by name with a citation, and there are exactly two:**

| exemption | who | citation | granted |
| --- | --- | --- | --- |
| `DANGER_IS_THE_TOP_RUNG` | naught `∙∙`, corgi `██`, prism `⣿⣿`, blueprint `━━` | each kit's own line, e.g. *"`██` — LEVELS[error]; the segment driven to full height"* | inc45, untouched by this batch |
| `THE_GROUND_IS_NOT_A_MARK` | naught `◦` (`NA.OFF`) | LANGUAGES.md §0, *"the unlit grid is visible … that faint lattice IS the signature"* — it is `BLANKS` extended, not the rule bent | **inc61** |

The second is **priced** (`GROUND_EXEMPTION_IS_WORTH = (7, 2)`, asserted with its own law) and
**derived** (read from `LG.NA.OFF`, so a kit that moves its unlit pixel moves the exemption with it).

## 2. Gates, verbatim

```
$ python -X utf8 -m pytest -q -p no:randomly
FAILED tests/test_app.py::test_win_clipboard_roundtrip - AssertionError: assert None == 'roundtrip 123 ABC taskboard'
1 failed, 1111 passed, 2 skipped, 4 warnings in 36.72s

$ python -X utf8 prototypes/verify_language.py
ALL PASSED                                             (exit 0)

$ python -X utf8 prototypes/components/render.py
  66 .txt + 66 .svg -> ...\prototypes\components
  66 candidates files
  no two frames identical within a screen (330 pairs)
  0 hand-drawn elements declared (0 refused, 0 evoked)

$ python -X utf8 prototypes/components/matrix.py
  --- refusals, by language ---
  naught [] corgi [] instrument [] swiss [] industrial [] nord []
  darkside [] prism [] ledger [] solari [] blueprint []          (66 of 66, exit 0)

$ python -X utf8 prototypes/capture_languages.py plain
  22 grids identical across two PROCESSES
  22 captures -> ...\prototypes\gallery
  no two boards identical                              (exit 0, nothing moved)

$ python -X utf8 prototypes/collision_census.py -o prototypes/out/collision_census.txt
TOTAL                       25
zero collisions: NONE -- all eleven overload at least one cell
TOTAL homoglyph rows             1                     (both self-checks green, exit 0)

$ python -X utf8 prototypes/export_to_skill.py
  wrote ...\assets\languages.py (22 KB, 11 languages)
  verified: 11 languages, every token, doc and family round-trips
  captures: 12 written, 54 already identical
  wrote SURFACES.md (11 postures)

$ python -X utf8 prototypes/export_to_skill.py          # re-run
  captures: 0 written, 66 already identical
```

**`render.py` and `capture_languages.py` moved NOTHING in this increment** — the four implementation
increments each re-rendered, so the tree was already at rest. That is the check, not the absence of one.

**`test_win_clipboard_roundtrip` is red and was red at the baseline `067400c` and in every gate run of
all five increments.** Environment-coupled (spec §10.6). Reported, not counted, not touched.

## 3. Gallery 44–51, compared byte for byte

```
44_instrument-list-graticule   identical
45_industrial-list-plate       identical
46_swiss-list-next-column      identical
47_solari-list-gate-seam       identical
48_industrial-modal-plate-lid  identical
49_darkside-modal-rounded-lid  DIFFERS from darkside_S4
50_solari-form-printed-severity identical
51_instrument-monitor-dot-ladder identical
```

**And 49 does not differ for a reason this batch created.** `git log 067400c..HEAD` over all eight
sources returns **zero commits for every one of them**:

```
instrument_S1 0 · industrial_S1 0 · swiss_S1 0 · solari_S1 0
industrial_S4 0 · darkside_S4 0 · solari_S2 0 · instrument_S5 0
```

49 has been stale since `rework-5a` (§13.6: the danger form `ØDeleteØ` → `▚Delete▞`, and the six
field-row leaders `◦` → `▔`) and gained a third staleness in `rework-5b` (§14.5: the active tab
`(O)` → `(●)`). **Stale for the fourth batch running.** `export_to_skill.py` copies
`prototypes/gallery/*` into `assets/languages/` and does not touch `assets/gallery/`; the batch's
constraint is *"the skill is edited only through `export_to_skill.py`"*, so the copy was again not
made. **Somebody has to re-install it by hand or teach the exporter that directory.**

## 4. What was written

- **`spec.md` §15** — the batch record: the ruling verbatim, the two frame measurements that refused
  the blanket exemption, the four rulings with the kit sentence each one widened, the roster and census
  tables per increment, the declared costs, and ten found-by-looking items.
- **`PROTOTYPE-inheritors-2.md` §6 A — marked RULED (2026-09-06, `rework-5c`)**, in the round's own
  Spanish, with what it decided, what it measured, and the one thing it did not close.

**Decision A was the last of the seven §6 put to the operator.** C, D and C1 closed in `rework-5a`;
E, F and G in `rework-5b`; A here. §6 has no open question left.

## 5. Risks

- **Two exemptions now carry eleven zeroes.** A reader who sees "all eleven at zero" and does not read
  §15.3 will not know that naught's zero rests on nine seats being exempted, five of which inc61 put
  there. The mitigation is the priced constant and its law; the risk is that a summary travels further
  than a packet.
- **The census still counts the field RUNE and the test law still excludes it** (§15.5). Five languages'
  last row is that one disagreement. Not closed here, and it is the batch's top pending item.
- **The skill repo is dirty and uncommitted across three batches now** (`rework-5a`, `-5b`, `-5c`).
  `export_to_skill.py` is idempotent so the state is reconstructible, but nobody has committed it.
- **Nothing in this batch was judged by a person.** Four languages' control alphabets were rewritten on
  the orchestrator's rulings under a delegation. Every ruling is one table of declarations in one file,
  so any of them is one edit to reverse — that is deliberate and it is stated in each packet's Risks.

## 6. Pending — carried out of the batch

1. **The rune, in `collision_census.py`** — one function; closes the last row of five languages.
2. **`49_darkside-modal-rounded-lid`** — hand-install, or teach the exporter `assets/gallery/`.
3. **Marks outside every instrument**: `Corgi.PANE_RULE` (`█`, the danger form ×16 on `corgi_S1`),
   `Corgi.DISCLOSE`/`LIT`, **`Blueprint.ERROR_FILL`** (the warn rung on the error row — the sharpest),
   `Blueprint.REG`, `Prism.SPIN`.
4. **prism's `REQUIRED` against its `FIELD_LEAD`** — exempted with a citation the increment argues
   against in writing.
5. **K2** — the laws compare code points. This batch is the third crack in it: `▔`/`▀` and `▁`/`▂` left
   corgi's alphabet as a side effect, `╌`/`┄`/`┈` are three dashed runs told apart by COUNT, and `⋅`/`∙`
   is not in `HOMOGLYPHS` while `·`/`∙` is.
6. Still open and untouched: **K4**, **L1–L6**, **C2**, **C4**–**C7**, **E2**, **E3** (measured a third
   time, fired for the first).

## 7. Suggested next task

**The rune.** Teach `collision_census.py` the exclusion `_invalid_marks` has carried since inc52, with
the counterfactual printed both ways the way inc57 printed `IDENT_GLYPHS`'s. It is one function, it
makes the corpus's two instruments agree for the first time, and it is the only thing standing between
this census and a table of exempted rows only.

---

## Evidence checklist

- [x] **Tests/type checks/lint pass — WITH ONE RED, NAMED.** `1111 passed, 2 skipped, 1 failed`; the
      failure is `tests/test_app.py::test_win_clipboard_roundtrip`, environment-coupled (spec §10.6),
      red at the baseline and in all five increments — **reported, not counted, not touched.** Every
      other gate quoted verbatim in §2, all exit 0.
- [x] **No secrets in code or output** — two documents. No source file was touched by this increment.
- [x] **No destructive commands run without approval** — none.
- [x] **File count within cap** — **2 documents**: `.fast-dev-flow/spec.md`,
      `prototypes/components/PROTOTYPE-inheritors-2.md`, plus this packet. Zero source files.
- [x] **Review packet attached** — this document.
