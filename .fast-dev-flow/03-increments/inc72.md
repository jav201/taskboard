# Increment 72 — the four reworks: ledger's posting closes, naught's band stops being the danger form, naught's two option rows stop being one drawing, blueprint stops counting dashes

**Batch:** `rework-7a`, increment 1 of 4 · the four `rework` verdicts standing in
`PROTOTYPE-inheritors-4.md` §1 (`ledger_S4`, `naught_S4`, `naught_S2`, `blueprint_S3`).
**Files:** `taskboard/language.py`, `tests/test_components.py`, `prototypes/collision_census.py` —
**3 source files**, plus 10 regenerated component artefacts (`ledger_S4`, `naught_S2`, `naught_S4`,
`blueprint_S3`, `blueprint_S5`), 4 regenerated gallery artefacts (`gallery_naught`,
`gallery_blueprint`) and the regenerated census table.

**Four frames could not answer a question a reader asks out loud, and all four were named in round
three and still standing in round four.** `ledger_S4` opened on a 100-cell rule and closed on
nothing, so the modal's lower limit was the edge of the terminal and `(Delete)` sat on row 32.
`naught_S4` drew its band's two rules in `∙` — the `DANGER_FORM` — so on the one screen where a
reader must find "this destroys data" there were 237 candidates and two right answers, and the 200
largest and most contiguous of them were the frame of the question. `naught_S2` drew its radio row
and its checkbox row from four members of one homoglyph family, two rows apart. `blueprint_S3` told
three horizontals apart by counting dashes inside a 12px cell.

Suite **1249 → 1252**. Census **30 → 29** colliding cells and **26 → 24** homoglyph rows — blueprint
goes to zero on both counts, and they are the first rows in that roster closed by retiring cells
rather than by widening the reader.

---

## 0. Rulings (orchestrator, 2026-09-07, on the operator's delegation)

> **K6:** contrast is measured against the background actually under the run (the second grounds:
> selection bands, plates, match rects), not only the canvas. `ink` and `mut` ≥ 4.5:1 against every
> ground they are painted on; `focus` ≥ 3:1.

> **K7:** `dim` ≥ 3:1 wherever it classifies (a severity rung on a log row, a dash count, a state
> mark); a purely decorative leader or seam is exempt by seat, named. `alert` ≥ 4.5:1 against every
> ground it is painted on, all eleven.

> **Match tier:** `accent` (or the match ink) against `mut` and against `ink` ≥ 3:1, all eleven, so
> raising `mut` cannot silently erase the match.

> **L7 measured:** the `info` rung may be air (blueprint, ledger, doctrine) or drawn; if drawn it
> obeys K7 (≥ 3:1). Nine languages draw it under 2:1: fix each.

> **C8, second half:** corgi's confirm gets walls from its display frame (`▓`, inc67's register
> ruling) with the board still gone; thirty blank rows with no opener or closer is not a modal.

> **swiss `╎`:** stands; consistency with the kit's own dead cell beats one fewer vertical.
> Recorded.

> **industrial `/`:** the value's separators and the field paper may not be one glyph: the paper
> becomes a cell that no value can contain (cite industrial's alphabet), the invalid marks at
> slider.knob/stepper.step stay.

This increment carries out **the four reworks**. K6, the match tier, K7/L7, C8's second half and
industrial's paper are inc73–inc75.

---

## 1. The four frames, read before anything was written

```
ledger_S4     f26  ──────────────────────────────────────  (100 cells, the posting opens)
              f32  ▶  (Delete)  ◀   │   Cancel   │          <- the terminal's LAST ROW, nothing under it

naught_S4     f13  ∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙…  (100 cells of the DANGER_FORM)
              f19  ○  ∙Delete∙  ○   ◦   Cancel   ◦
              f20  ∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙…  (100 more)          `∙` on this sheet: 237

naught_S2     f09    priority      ○ low  ○ norm  ⊙ high
              f11    tags          ◦ api  ◉ ui  ◉ urgent      four cells, ONE homoglyph family

blueprint_S3  f03    notify on overdue         ├─┤            on
              f05    sound                     ├┤·            off
              f06    sync to remote            ├╎┈            dead   -- `╌` 2 dashes, `┄` 3, `┈` 4
```

And the declarations under them:

```
Ledger.overlay_instead     out = under[:keep] + [rule] + rows          -- one rule, no second
Naught.overlay_instead     band = [ink NA.ON*w] + rows + [ink NA.ON*w] -- NA.ON is the DANGER_FORM
Naught.radio.main/knob     DEFAULT  ○ / ⊙        Naught.checkbox      DEFAULT  ◦ / ◉
Blueprint.LEVELS           info "  "  warn "╌╌"  error "━━"
Blueprint.main/indicator   DISABLED ┈ / ┄
```

`HOMOGLYPH_FAMILIES` reads `◦ o ○ ◎ ◉ ⊙ ⊛ O` as ONE drawing and `╌ ┄ ┈` as one drawing. Both of
naught's option controls and all three of blueprint's horizontals are inside a family.

---

## 2. Cause and mechanism — ledger's posting closes, and the destructive answer leaves the last row

**Cause.** `Ledger.overlay_instead` composed `under[:keep] + [rule] + rows`. One rule, at the head
of the posting, and nothing at the foot — so what said where the question ended was the terminal.
inc66 gave `Swiss.overlay_instead` its second rule in the same increment and **left this one alone**,
and round three had already written that ledger's was the graver of the two (*"below `(Delete)`
there is nothing, not a pager and not a seam, so the modal's lower limit is the edge of the
terminal"*). Round four's §7.5 is the disagreement: *"the fix exists, it is written, and it is four
lines from the one that was made."*

**Mechanism.** The block is built first and the page is cut to fit it, which is what moves the
answers as well as closing the band:

```python
rule = self.rule_line(w) or ""
block = [rule] + list(rows) + [rule]
keep = max(0, h - len(block))
out = [under[i] if i < len(under) else "" for i in range(keep)] + block
```

```
before  f26 ────…  f27 Delete 3 tasks?  …  f32 ▶  (Delete)  ◀   │   Cancel   │
after   f25 ────…  f26 Delete 3 tasks?  …  f31 ▶  (Delete)  ◀   │   Cancel   │   f32 ────…
```

**The page pays one row and it is a blank one.** `keep` falls from 25 to 24, and `under[24]` (the
old row 25) was blank on this frame — no gate header and no task is lost, which is the thing
`swiss_S4` did lose when it closed (inc66 §9 records `Rate-limit the API 2d!` going).

**Two rules of the same weight is not a box**, which is this language's refusal
(`MODAL_BORDER_REFUSED`): the backdrop is still at full strength, nothing is dimmed and nothing
turns a corner. A ledger rules a posting off at its foot the way it rules it on at its head.

## 3. Cause and mechanism — naught's band is bounded by the ground, not by the danger form

**Cause.** `NA.ON` (`∙`) is `DANGER_FORM[0]` and `[1]`, `LEVELS["error"]` and `LEVELS["warn"]`'s
first cell. The band's two rules were `NA.ON * w`, so a confirm that destroys data framed itself in
the mark that means destruction, 200 cells of it. Round four: *"237 candidates, two correct, and the
200 largest and most contiguous cells on the screen are the modal's frame"* — and it is the one
`rework` of round three that **no increment of the nine touched or named**.

**Mechanism.** `NA.ON * w` → `NA.OFF * w`, still painted at `c['ink']`.

`NA.OFF` is the UNLIT lattice dot, and it is not a mark: `THE_GROUND_IS_NOT_A_MARK` says so by name,
one language and one cell, citing LANGUAGES.md §0 (*"the unlit grid is visible … that faint lattice
IS the signature"*). **The doctrine gets more literal rather than less.** `overlay_instead`'s own
docstring says the separation *"is the same lattice, at two charges, and the question is where the
current is"* — and the bound is now the lattice itself, charged, instead of a severity rung standing
in for it.

**Measured on the shipped frame:** `∙` **237 → 37**, and inside the band — the rows drawn at full
charge — **exactly 2**, which is `len("".join(DANGER_FORM))`. The other 35 are on the receded page at
`dim`. The round's criterion (*"point at the cells that mean irreversible"*) answers.

## 4. Cause and mechanism — naught's two option rows stop being one drawing

**Cause.** L10. The kit's own comment made the argument and took the wrong half of it: *"naught's
entire vocabulary is the lattice dot … so the distinction it can afford is WITHIN the family"* — and
`HOMOGLYPH_FAMILIES` reads that family as ONE drawing at six diameters and fills. Rows 9 and 11 of
`naught_S2` were `○`/`⊙` against `◦`/`◉`: four members of it, two rows apart.

**Mechanism.** The radio's DEFAULT and FOCUSED cells **trade places** at both of its parts:

```
before  radio.main {DEFAULT ○, FOCUSED ◌, ACTIVE ◦, DISABLED ⋅}
        radio.knob {DEFAULT ⊙, FOCUSED ⊚, ACTIVE ●, DISABLED ⊗}
after   radio.main {DEFAULT ◌, FOCUSED ○, ACTIVE ◦, DISABLED ⋅}
        radio.knob {DEFAULT ⊚, FOCUSED ⊙, ACTIVE ●, DISABLED ⊗}
```

`◌` (dotted ring) and `⊚` (ring inside a ring) are members of **no** homoglyph family; `◦` and `◉`
are members of the ring family. So the channel between the two rows is SHAPE, not diameter:

```
before  f09  ○ low  ○ norm  ⊙ high        after  f09  ◌ low  ◌ norm  ⊚ high
        f11  ◦ api  ◉ ui  ◉ urgent               f11  ◦ api  ◉ ui  ◉ urgent
```

**Nothing new enters the alphabet.** Both cells were this part's own FOCUSED cells; the ladder is the
same six cells it always was, and the census is unmoved at 3 colliding cells and 12 homoglyph rows.

**And the state roster does NOT move, which is stated here because the first draft of the comment
claimed it did.** `STATES_TOLD_APART_BY_SIZE["naught"]` is still **8**: `○`/`◦` at `radio.main` is
still a row, at FOCUSED-against-ACTIVE instead of DEFAULT-against-ACTIVE. What moved is the pair of
cells a FORM draws — the unticked box and the unchosen well — which is what L10 was raised about.
Closing the roster is still *"a second channel for this alphabet, which is a language-level
increment"*, in that roster's own words, and it is not this one.

## 5. Cause and mechanism — blueprint stops counting dashes, and it took two moves

**Cause.** K4 in the frame. `╌` (two dashes), `┄` (three), `┈` (four): three horizontals told apart
by a count nobody can make at 12px, and round four measured all three at **1.24:1** in `dim`.
inc68 built the instrument (`state_channel`, the census's two blueprint homoglyph rows) and the frame
did not move — *"the only `rework` of the corpus whose instrument was built and whose frame was not
touched."*

**Mechanism, and the first draft was wrong in a way worth recording.** The obvious move — send both
dead runs to the dashed VERTICAL, `╎` and `╏`, and keep `LEVELS["warn"]` on `╌` — went **RED three
times** in `verify_language.py`:

```
3 FAILURE(S): ['blueprint: the disabled knob differs in SHAPE from both the fill and the track …',
               'blueprint: the disabled knob differs in SHAPE from both the fill and the track',
               'blueprint: the checked+disabled knob differs in SHAPE from both the fill and the track']
```

`knob[DISABLED]` is already `╎`, so the switch's dead TRACK and its dead GRIP had collapsed onto one
cell — **the same failure inc60 hit from the other direction**, and the reason it invented the dash
count. The sheet needs THREE distinct dead cells (track, fill, grip) and has only TWO dashed
verticals, so the third has to be the dashed horizontal `╌`. Which means the meaning on `╌` has to
move, because inc60's ruling (ii) stands: **a dead thing is not a meaning.**

So, two moves:

```
LEVELS       info "  "  warn "╌╌" error "━━"   ->   info "  "  warn "━ "  error "━━"
main         DISABLED ┈  ->  ╌       (the dead GROUND: the broken rule, this sheet's CLIP flag)
indicator    DISABLED ┄  ->  ╏       (the dead EXTENT: the dashed vertical)
knob         DISABLED ╎  ->  ╎       (unchanged -- the dead GRIP, a third cell again)
checkbox.knob  ╎┄╎ -> ╎╏╎     radio.knob  ╏┄╏ -> ╏╎╏
textfield.main ╎┈╎ -> ╎╌╎     stepper.main ┈┈ -> ╌╌
```

**`┄` and `┈` leave the kit entirely.** What separates the two dead runs is DIRECTION — ruling D's
fourth channel, and the one this sheet already spends on `╱` HELD against `╲` REFUSED. What separates
a dead datum from its own terminators is that it is never the cell its walls wear, at all three
walled seats. Nothing new enters the alphabet.

**And the severity ladder counts CELLS DRAWN.** `"  "` / `"━ "` / `"━━"` — nothing, half the run
ruled, the whole run ruled. That is COUNT, the channel `state_channel` reads first as *"the coarsest
thing an eye resolves in a run"*, and it is this sheet's own doctrine carried one step further:
`LEVELS["info"]` is air because *"a drawing office does not rule a line to say there is nothing to
note"*, so a note is half a rule and a fault is a whole one. **No cell gains a family** — `━` was
already `LEVELS["error"]` and the `DANGER_FORM`. The run grows to the RIGHT so the log's severity
gutter is one column wide, which is what the other ten do (`* `/`**`, `! `/`!!`, `o `/`O `).

```
blueprint_S3  f06  ├╎┈  ->  ├╎╌      blueprint_S5  f10  09:41:09    ->  09:41:09 ━
                                                   f12  09:41:18 ━━  ->  09:41:18 ━━
```

---

## 6. The laws

**`test_ledgers_confirm_is_posted_on_the_page_that_stays_legible`** — extended, not replaced. It
already asserted the backdrop stays at full strength; it now also asserts that the block's FIRST and
LAST rows are the same rule at full measure, that the question follows the opening rule, and that
**the destructive answer is not on the sheet's last row**. Both halves of C2 in one place.

**`test_every_confirm_says_where_it_ends`** — ledger's by-name clause changes from `"Cancel" in
ends["ledger"]` to `set(ends["ledger"]) == {"─"}`. The weak law is unchanged for the other ten; what
changed is that ledger no longer closes on its answers.

**`test_naughts_separation_is_charge_and_not_a_frame`** — the bound rows are read off `NA.OFF`
instead of `NA.ON`, they must still be at `ink` and full measure, and a fourth clause counts the
`DANGER_FORM` cell INSIDE the band and asserts it equals what the question itself spends. That clause
is the one that would have caught this six batches ago.

**`test_naughts_two_option_controls_do_not_rest_on_one_drawing`** — new, L10. Neither cell a radio
RESTS on may be a checkbox's resting cell **nor that cell's homoglyph**, asked of the kit; and the two
option rows of the shipped `naught_S2.txt` may share no cell at all. Asked of the RESTING pair and not
of every state, deliberately: what a form draws is the unticked box and the unchosen well, and closing
the whole table is the roster's language-level increment.

**`test_blueprints_dead_runs_turn_instead_of_counting_dashes`** — new, replacing
`test_blueprints_dash_ladder_is_monotone_in_its_count`. Four clauses: `┄` and `┈` appear in no
declared table and `╌` is the only dashed horizontal left; the two dead runs are the roster's cells
and the dead track, fill and grip are three distinct cells; no dead run is the warn rung or a cell of
its family (inc60's ruling (ii), unchanged); and at the three walled seats the dead datum is not its
own walls. Plus: the severity ladder is one width and its drawn-cell counts are `[0, 1, 2]`.

**The law it replaces asserted the ladder was MONOTONE** — *"if a reader can count at all, counting
gives the right answer"* — and that was the honest limit of what inc60 could assert. Round four
answered it by measuring the three runs at 1.24:1: **a count you cannot resolve is not a channel
however well it is ordered.**

## 7. Teeth

**`test_the_option_control_law_bites_on_the_declaration_naught_shipped`** puts `○` back at
`radio.main[DEFAULT]` and `⊙` back at `radio.knob[DEFAULT]` **one at a time**, because the two halves
of the defect are different (the well's ring was the box's ring at another diameter; the chosen mark
was the ticked mark at another diameter) and restoring either alone must go red.

**`test_the_dead_run_law_bites_on_the_declaration_blueprint_shipped`** restores inc60's dash-count
ladder and the old `LEVELS["warn"]`, asserts that **the old law's own assertion is still true of it**
(the counts are `[2, 3, 4]`, monotone), and then asserts the new law goes red anyway. An ordering law
could never have caught this, and the teeth say so in arithmetic.

**`test_both_seat_laws_go_red_on_the_two_meanings_inc60_moved` had to be re-measured, and the
measurement is the finding of this increment.** Two of its five pre-inc60 tables (`main`,
`stepper.main`) are now **byte-identical** to what the kit ships, because the dead ground went back to
`╌` once the warn rung left it. So:

```
BLUEPRINT_TABLES_WORTH   (1, 8)  ->  (0, 0)
BLUEPRINT_SHEET_BEFORE   REQUIRED "├"   (8, 12) -> (7, 4)
                         LEVELS pre-60  (13, 12) -> (13, 12)   UNCHANGED
```

**The same cells at the same seats are worth eight rows or none depending on where one meaning
sits.** That is inc60's ruling (ii) stated as arithmetic, and the comment above the constant records
both readings and why each was right when it was taken. The end point is unchanged at `(13, 12)`:
with both meanings put back the sheet is exactly as bad as it was before inc60, which is what an end
point is for.

**The confirm-closing teeth are the frames themselves**: `ledger_S4`'s last changed row was the
answers and is a rule; `naught_S4`'s band rows were 200 `∙` and are 200 `◦`.

## 8. The census went 30 → 29 and 26 → 24, and blueprint went to zero on both

```
                        4089eda   inc72
BLUEPRINT colliding        2        1      -- `╌` [LEVELS[warn] + scrollbar.main(disabled)] closes
BLUEPRINT homoglyph        2        0      -- `╌`/`┄` and `╌`/`┈` close: the cells are retired
NAUGHT    colliding        3        3      -- unchanged
NAUGHT    homoglyph       12       12      -- unchanged
-----------------------------------------------------------------------------------
TOTAL colliding cells     30       29
TOTAL homoglyph rows      26       24  (6 languages, was 7)
```

**`╌` stops being a colliding cell because it stops carrying a meaning**, and `━` — which gains the
warn rung — was already a colliding cell at 4 families, so no new row opens. **These are the first
rows in the homoglyph roster closed by RETIRING CELLS rather than by widening the reader**, and the
roster's own note now says so.

**naught does not move and that is expected**: the radio's resting cells left the ring family, but the
family still holds every other state of both controls, and the census reads the DECLARED table.
`naught_S2` is the frame that improved; the roster is the table that did not.

## 9. Frames changed

| frame | txt | svg | what moved |
|---|---|---|---|
| `ledger_S4` | ✓ | ✓ | the block shifts up one row and **closes on a rule at row 32**; `▶  (Delete)  ◀` moves from row 32 to row 31 |
| `naught_S2` | ✓ | ✓ | row 9: `○ low  ○ norm  ⊙ high` → `◌ low  ◌ norm  ⊚ high` |
| `naught_S4` | ✓ | ✓ | rows 13 and 20: 100 `∙` → 100 `◦`, each. `∙` on the sheet 237 → 37, inside the band 202 → 2 |
| `blueprint_S3` | ✓ | ✓ | row 6: `├╎┈` → `├╎╌` |
| `blueprint_S5` | ✓ | ✓ | row 10: the `warn` rung appears — `09:41:09    3 tasks overdue` → `09:41:09 ━  3 tasks overdue` |
| `gallery_naught` | ✓ | ✓ | the radio's three live rows: `○ lo  ⊙ mid  …` → `◌ lo  ⊚ mid  …` |
| `gallery_blueprint` | ✓ | ✓ | the switch and slider disabled rows: `├╎┈  ├┄╎  ╎ ╎  ╎┄╎` → `├╎╌  ├╏╎  ╎ ╎  ╎╏╎`; `╏┄╏ mid` → `╏╎╏ mid` |

**The other 61 `.txt` and 61 `.svg` are byte-identical**, and the other 18 gallery artefacts are too.

**Gallery 30–51 in the skill:** not run in this increment — the batch close runs
`export_to_skill.py` (§13).

## 10. Gate tails, verbatim

```
$ python -X utf8 -m pytest -q
FAILED tests/test_app.py::test_win_clipboard_roundtrip - AssertionError: assert None == 'roundtrip 123 ABC taskboard'
1 failed, 1252 passed, 2 skipped, 4 warnings in 33.71s

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
self-check  1 of the 5 collisions the round found by hand still come back out of the census; 4 are asserted CLOSED and cannot grow back
self-check  the homoglyph roster is exact for all eleven (24 rows, 6 languages)
NAUGHT   3 colliding cells   (LEVELS ◦◦/∙◦/∙∙  DANGER ∙∙  REQUIRED ⊛  CUR ●)
BLUEPRINT   1 colliding cells   (LEVELS   /━ /━━  DANGER ━━  REQUIRED ═  CUR ┌)
TOTAL                       29
TOTAL homoglyph rows            24
                                                        (exit 0)

$ python -X utf8 prototypes/capture_languages.py
  22 grids identical across two PROCESSES
  22 captures -> ...\prototypes\gallery
  no two boards identical
                                                        (exit 0)
```

Suite **1249 → 1252** (+1 blueprint teeth, +1 naught option law, +1 naught option teeth; one law
replaced one law).

## 11. Risks

1. **blueprint's warn rung is `━`, and `━` is the `DANGER_FORM`.** The ladder is now COUNT of the
   same mark, so a reader tells a note from a fault by how far the rule reaches rather than by which
   mark it is. That is a real narrowing, taken deliberately: the alternative was leaving three
   horizontals told apart by a count measured at 1.24:1 for a fourth round. `━` gains a family in the
   census and stays one cell; it does not become a new row.
2. **blueprint's dead ground is `╌` again**, byte for byte the pre-inc60 spelling, and it is also the
   CLIP flag (`BREAK`), `DISCLOSE`, `ERROR_FILL` and `GANTT[1]`. None of those is in the census's
   A-family set, so the cell stays chrome — but it is now this sheet's most-spent dashed mark and a
   future meaning landing on it would reopen exactly what inc60 closed. The law's clause 3 is the
   guard.
3. **naught's radio DEFAULT is `◌`, which is also `checkbox.main[ACTIVE]` and `knob[DISABLED]`.**
   All chrome, no meaning, census unmoved — but it is a third seat for one cell in a kit that
   `spec.md` §11.5 already records as having "no unspent cell left".
4. **`ledger_S4` gives up one row of the page.** It was blank on this fixture; on a page whose row 25
   carries an entry the posting would cover it. The band is composed before the page is cut, so the
   cost is structural rather than incidental, and `test_a_modal_changes_one_contiguous_band_of_the_
   page[ledger]` is what would go red if it ever covered something.
5. **`naught_S4`'s band is bounded by the cell the receded page is also drawn in.** `◦` at `ink`
   against `◦` at `dim` is a TIER channel, not a cell channel — which is exactly ruling 4's argument
   ("the separation is charge") but means the bound is invisible with colour stripped. Named here
   because it is the shape of an objection round five can make.

## 12. Found by looking, not fixed

- **`naught_S2`'s row 4 still draws `⊛`, `○` and `◉` in one line** — `title⊛        ○Fix login◉
  redirect…○` — and `⊛` (`REQUIRED`) is a member of the same ring family as the field's walls and its
  caret. That is four of naught's twelve homoglyph rows and it is a MEANING against CHROME, which is
  a heavier reading than L10's chrome-against-chrome. No ruling covers it.
- **`STATES_TOLD_APART_BY_SIZE["naught"]` is 8 and unmoved**, §4. Six seats still tell two states
  apart with a ring at another size or fill.
- **blueprint's sparkline draws `╌ ─ ━`** (`blueprint_S5` row 5), and `━` is now the warn rung as well
  as the error rung and the `DANGER_FORM`. L6 in a language that did not have it before this
  increment.
- **`─` is `indicator[DEFAULT]`, the live switch track, and the warn rung is one cell away from it in
  weight.** blueprint now has swiss's standing finding (inc66 §12: *"`─` is `LEVELS["warn"]` in swiss
  and is what both of the confirm's rules are drawn with"*) in a milder form.
- **`ledger_S4`'s rows 27–32 still start in column 1 while rows 1–25 start in column 3** — round
  four's third objection to that frame, untouched.

## 13. Pending — not this increment

- inc73 (K6 and the match tier), inc74 (K7 and L7), inc75 (C8's second half and industrial's paper).
- The batch close: `export_to_skill.py`, `spec.md` §19.
- Everything §5 of round four lists as open.

## 14. Suggested next task

inc73: the law that walks every painted run in the 66 `.svg`, reads the ground under each run from
`cell_grid`, and asserts by tier — and **the failing runs reported by language and tier BEFORE any
token moves**, which is the half of it that cannot be undone once `themes.py` is edited.

## Evidence checklist

- [x] **Tests/type checks/lint pass — WITH ONE RED, NAMED.** `1252 passed, 2 skipped, 1 failed`
      (baseline `1249 passed`). The failure is `tests/test_app.py::test_win_clipboard_roundtrip`,
      environment-coupled (spec §10.6) — **reported, not counted, not touched.**
      `verify_language.py` ALL PASSED exit 0 (and it went RED three times on the first draft of the
      blueprint fix, §5). `render.py` 66 `.txt` + 66 `.svg` / 330 pairs / 0 hand-drawn.
      `matrix.py` refusals `[]` for all eleven. `collision_census.py` both self-checks green,
      **TOTAL 30 → 29**, homoglyph rows **26 → 24**. `capture_languages.py` plain: 22 captures, 22
      grids identical across two processes, 4 artefacts moved.
- [x] **No secrets in code or output** — two overlay compositions, four kit tables, one `LEVELS`,
      three laws, two teeth, one roster constant. No network, no new dependency, no path outside the
      worktree.
- [x] **No destructive commands run without approval** — none.
- [x] **File count within cap** — **3 source files**: `taskboard/language.py`,
      `tests/test_components.py`, `prototypes/collision_census.py`.
- [x] **Review packet attached** — this document.
