# Increment 80 — the full-measure law is width-bound

**Batch:** `rework-7c`, increment 2 of 2 · inc78 §5, *"the frame is correct and the law is wrong."*
Also closes the batch: `spec.md` section 21.
**Files:** `tests/test_components.py` — **1 source file**, and this packet. No production code, no
frame, no artefact.

**`test_a_confirm_opens_and_closes_on_marks_of_its_own`'s solari arm read `any(w > 800)` as "the band
plate is at full measure."** 800 is `100 cols x 8.4 CW` with a margin — true only at 100 columns. At
80 columns the page itself is 672 units wide, so 800 is *larger than the page*, and the arm read RED
against a frame inc78 confirmed was correct. **The predicate now reads the page's own width off the
frame's own canvas rect, so it asks the same question at every width.** The arm is GREEN at 80x24 and
stays GREEN at 100x32 — the control arm inc78 built runs first and still passes all 53.

---

## 0. The fix

`tests/test_components.py`, inside `test_a_confirm_opens_and_closes_on_marks_of_its_own`'s
`CONFIRM_EDGE_REFUSED` branch:

```python
svg = (FRAMES / f"{lang}_S4.svg").read_text(encoding="utf-8")
runs = [(float(w), f) for _x, _y, w, _h, f in _RECT_RUN.findall(svg)]
page_w = float(_CANVAS_RECT.search(svg).group(1)) - 2 * _PAD
assert any(w >= page_w - 1.0 for w, _f in runs), (lang, page_w, runs[:3])
```

`_CANVAS_RECT` and `_PAD` already existed in this file (§5121, §5251) for `painted_runs()`'s own
ground-lookup — `capture_languages.svg_from_grid()` writes the canvas as the one `<rect>` with no `x`/
`y`, at `pw = cols * CW + 2 * PAD` (read off the exporter's own source, not re-derived: this is the
same "declared here, checked against the exporter" stance `test_this_files_picture_metrics_are_the_exporters`
already takes for the same file). Subtracting `2 * PAD` recovers `cols * CW` — "the page" inc78's own
prose meant when it called 672 "the full measure of the page it is on" — without hard-coding either
`cols` or a per-width constant anywhere. **1.0 unit of tolerance**, not a percentage: every measured
plate in the corpus equals `cols * CW` exactly (checked below), so the tolerance exists only to absorb
`.1f`-rounding noise in the SVG's own text formatting, not to excuse a real defect — a plate short by
even one cell (8.4 units) still fails.

**Measured, not assumed:**

```
              canvas w   canvas h   page_w (canvas - 2*PAD)   plate width
100x32 solari    860.0      564.0                      840.0         840.0
 80x24 solari     692.0      428.0                      672.0         672.0
```

Both plates equal `page_w` exactly — the predicate's `>= page_w - 1.0` passes both with room to spare
and would catch a plate narrowed by as little as one cell.

## 1. What this does NOT fix, and why

**Ruling F still fails for solari at 24 rows, on purpose.** `test_a_solari_confirm_never_covers_the_gate_it_names`
is the other red arm inc78 recorded, and it is a HEIGHT finding (the band has nowhere to go below
`DOING` at 24 rows) wearing a width's clothes — a solari design decision, and the brief for this batch
is explicit: *"Do not fix languages here; the round judges."* Untouched.

**No other law in this file uses a fixed pixel/unit threshold for "full measure."** Grepped
`test_components.py` for `> 800`, `> 840`, and any other bare three-digit comparison against a `w` or
`width` variable near an SVG rect read — this was the only one. Not a pattern needing a wider sweep.

## 2. The recorded set updates, and the test that pins it has teeth

`SECOND_WIDTH_RED` (inc78) drops one entry:

```python
# before
SECOND_WIDTH_RED = {
    ("test_a_solari_confirm_never_covers_the_gate_it_names", None),
    ("test_a_confirm_opens_and_closes_on_marks_of_its_own", "solari"),
}
# after
SECOND_WIDTH_RED = {
    ("test_a_solari_confirm_never_covers_the_gate_it_names", None),
}
```

`test_the_frame_laws_at_eighty_by_twenty_four_are_the_ones_recorded` asserts the ACTUAL red set at
80x24 equals `SECOND_WIDTH_RED` exactly (`assert red == SECOND_WIDTH_RED, red`), so it is the gate that
would have caught a stale entry on its own. **Checked by hand, not left as an inference**: restored the
old two-entry set on a scratch copy and re-ran this one test — RED, with the extra entry named in the
diff (`AssertionError: {('test_a_solari_confirm_never_covers_the_gate_it_names', None)}` on the left,
the stale pair as the extra item on the right) — then reverted. The set now correctly names **one** red
arm out of 79, and both of the two docstrings that said "two arms" (`SECOND_WIDTH_RED`'s own comment
block and `test_the_frame_laws_at_eighty_by_twenty_four_are_the_ones_recorded`'s docstring) are updated
to say one, with the fixed arm's history kept rather than deleted.

## 3. Teeth on the predicate itself

Confirmed the new predicate is not vacuously true by construction:

1. **At both widths, the assertion passes** — shown in §0's table, both plates equal `page_w` exactly.
2. **A plate short by one full cell would fail** — `page_w - 1.0` tolerance is under one `CW` (8.4
   units), so a genuinely narrowed plate (the defect this law exists to catch) still reads red; only
   sub-pixel formatting noise is absorbed.
3. **The recorded-set test (§2) is itself teeth for "did the fix actually flip the arm green"** — it
   reads the REAL 80x24 corpus through the REAL law, not a restatement, and a fix that didn't work would
   leave the old entry in `SECOND_WIDTH_RED` correctly matching a still-red arm; the mismatch only
   appears once the fix is real AND the recorded set is updated, which is exactly what §2's manual
   check demonstrated in both directions.

## 4. Gate tails, verbatim

```
$ python -X utf8 -m pytest -q
FAILED tests/test_app.py::test_win_clipboard_roundtrip - AssertionError: assert None == 'roundtrip 123 ABC taskboard'
1 failed, 1371 passed, 2 skipped, 4 warnings in 44s

$ python -X utf8 -m pytest -q tests/test_components.py -k "confirm_opens_and_closes or frame_laws_at_eighty or ruling_F"
13 passed, 1004 deselected

$ python -X utf8 prototypes/verify_language.py
  [PASS] settle() keeps headroom under its bound ...  worst 4 of 40 over 155 captures
ALL PASSED
                                                        (exit 0)

$ python -X utf8 prototypes/components/render.py
  66 .txt + 66 .svg -> ...\prototypes\components
  66 candidates files
  no two frames identical within a screen (330 pairs)
  0 hand-drawn elements declared (0 refused, 0 evoked)
$ git status --porcelain prototypes/components/*.txt prototypes/components/*.svg     (empty)

$ python -X utf8 prototypes/components/raster.py
  66 PNGs identical across two PROCESSES
  66 .png + 66 .json -> ...\prototypes\components\png
  every raster is 100x32 cells of 9x19 px  (2522 KB total)
$ git status --porcelain prototypes/components/png     (empty)

$ python -X utf8 prototypes/components/second_width.py
  no two frames identical within a screen (330 pairs)
  66 .txt + .svg + .png + .json -> ...\prototypes\components\w80
  ink 13.9% .. 58.4%
$ git status --porcelain prototypes/components/w80     (empty)

$ python -X utf8 prototypes/components/matrix.py
naught [] corgi [] instrument [] swiss [] industrial [] nord []
darkside [] prism [] ledger [] solari [] blueprint []
                                                        (exit 0)

$ python -X utf8 prototypes/collision_census.py
TOTAL                       28
TOTAL homoglyph rows            24
                                                        (exit 0)
```

Suite **1371 → 1371** (net zero — no test added or removed, three assertions and two docstrings
changed inside existing tests). Census **28 / 24** unchanged. No production file touched; every
regenerated artefact directory is byte-identical to before this increment (this increment does not
even change `ink()`'s callers, so this is expected rather than newly verified — re-run anyway, per the
batch's gate list).

## 5. Risks

1. **The tolerance (`1.0` unit) is a judgment call, not a derived number.** It is small relative to one
   cell (8.4 units) and every observed plate is exact, so it currently makes no practical difference —
   named so a future width where rounding is larger does not silently pass a narrowed plate.
2. **This predicate is now coupled to `svg_from_grid`'s canvas-rect format** (`<rect width="{pw}"
   height="{ph}" fill="{ground}"/>`, the one with no `x`/`y`) via `_CANVAS_RECT`, which already existed
   and is already load-bearing for `painted_runs()`. Not a new coupling, just a second reader of it.
3. **Only one law in the corpus had this defect** (§1) — this increment does not claim to have swept
   every width-dependent assumption in the suite, only the one inc78 named.

## 6. Batch `rework-7c` — closed

Two increments, one agent, both touching only files already in this batch's scope. Nothing rendered,
nothing re-baked: `spec.md` §21 records the close.

## 7. Pending — not this batch

- Solari's ruling-F failure at 24 rows — a design decision, for the round (inc78 §2, restated §1 above).
- The legibility floor (inc77 §4) — three questions written for a ruling.
- `collision_census.py`'s and `test_components.py`'s own `BLANKS` definitions are correct and
  independent of `capture_languages.ink()`'s (inc79 §6.2) — not unified in this batch.
- The fifth round itself, against `png/`, `w80/` and `legibility.txt` — this batch (`rework-7b` +
  `rework-7c`) built and repaired the instrument; nobody has run the round yet.

## 8. Suggested next task

The fifth round, as `rework-7b`'s own close already suggested: judge the corpus against
`prototypes/components/png/`, `prototypes/components/w80/` and `prototypes/out/legibility.txt`, with
solari's ruling-F failure and the legibility floor as its first two questions.

## Evidence checklist

- [x] **Tests/type checks/lint pass — WITH ONE RED, NAMED.** `1371 passed, 2 skipped, 1 failed`
      (unchanged from inc79's `1371 passed` — this increment fixes assertions inside existing tests,
      adds none). The failure is `tests/test_app.py::test_win_clipboard_roundtrip`, environment-coupled
      (spec §10.6) — reported, not counted, not touched. `verify_language.py` ALL PASSED exit 0.
      `render.py` 66/330/0. `matrix.py` refusals `[]` for all eleven. `collision_census.py` TOTAL 28,
      homoglyph rows 24 — unchanged. `raster.py` byte-identical across two processes. `second_width.py`
      0 rows cut, 330 pairs distinct.
- [x] **No secrets in code or output** — one test-file predicate, one recorded-set entry, two docstring
      updates. No network, no new dependency, no path outside the worktree.
- [x] **No destructive commands run without approval** — none. The two manual mutation checks (§2, §3)
      ran on the working file and were reverted before the next command, verified byte-identical by
      diff each time.
- [x] **File count within cap** — **1 source file**: `tests/test_components.py`.
- [x] **Review packet attached** — this document.
