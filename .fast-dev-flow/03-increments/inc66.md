# Increment 66 — both answers are walled, both confirms close, and swiss's freed channel is filled

**Batch:** `rework-6a`, increment 4 of 4 · **C2** (`ledger_S4`, `swiss_S4`) and **ruling C's
follow-through** (`swiss_S2`).
**Files:** `taskboard/language.py`, `tests/test_components.py` — **2 source files**, plus 6 regenerated
component artefacts (`ledger_S4`, `swiss_S2`, `swiss_S4`), 2 regenerated gallery artefacts
(`gallery_ledger`) and the regenerated census table.

**Three frames could not answer a question a reader asks out loud.** `ledger_S4` row 32 read
`▶  (Delete)  │   │   Cancel   │` — one `▶` and three `│` — because the FOCUSED button closed on the
COLUMN RULE, which is the safe answer's opener and the cell that page draws about forty times.
`swiss_S4` opened on a 100-cell rule and closed on nothing, in a confirm that destroys data, named as
*still open* in `spec.md` §11.3 since `rework-3` and untouched by five batches. And `swiss_S2` row 6 read
`║12/09/26` — one wall and eight characters — because inc52 took `╲` off the rejected field and nothing
moved into the channel that opened. Suite 1151 → 1165. **Census 25 → 26**, and the +1 is named and
explained in §8.

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

This increment carries out **C2** and **C's follow-through**.

## 1. The three frames, read before anything was written

```
ledger_S4  f32   ▶  (Delete)  │   │   Cancel   │          <- the terminal's LAST ROW
swiss_S4   f12   ────────────────────────────────  (100 cells, the modal opens)
swiss_S4   f19   ▪  ╲Delete╱      ▫   Cancel
swiss_S4   f20+  (nothing -- the modal never closes)
swiss_S2   f06   due•          ║12/09/26
```

And the declarations under them:

```
Ledger.button.main   DEFAULT │  │   FOCUSED ▶  │   ACTIVE ▶  ◀   DISABLED ╌  ╌
Swiss.overlay_instead   block = [rule, ""] + list(rows)
Swiss.textfield.main    INVALID "║  "        (wall, blank paper, blank closer)
```

Measured across the eleven before anything moved — `(opener's outer cell, closer's outer cell)` at every
declared button state:

```
same mark      naught ○ ○ · corgi ▒ ▒ · darkside ▬ ▬ ▮ ▮ █ █ · prism ⠿ ⠿ · solari ▁ ▁ ▔ ▔ ▂ ▂
               ledger │ │ · nord ▓ ▓ · blueprint ╎ ╎ · four kits' ╌ ╌
mirror pair    ( ) · [ ] · ├ ┤ · ┣ ┫ · ╞ ╡ · ▐ ▌ · ▛ ▜ · ▶ ◀ · ⠸ ⠇ · ⠼ ⠧ · ⣸ ⣇
no closer      swiss ▫ · ▪ · ■ · (blank)          -- inc38, by name
NEITHER        ledger.focused   ▶ .. │
```

**One seat in eleven languages and thirty-eight declared states closes on a cell that is neither its own
opener nor that opener's mirror, and it is the seat under the cursor in a destructive confirm.**

## 2. Cause and mechanism — ledger's answer pair

**Cause.** `Ledger.PART_GLYPHS["button.main"][FOCUSED]` was `"▶  │"`: the tally pointer on the left and
the column rule on the right. The kit's own comment explained it — *"the tally pointer arrives when the
cursor does, and the press CLOSES the entry on both sides"* — a coherent doctrine in which a focused
entry is still an OPEN entry. It costs the one row of the corpus where two buttons stand side by side:
Delete's closing `│` and Cancel's opening `│` are the same cell, three columns apart, and the only mark
saying where `(Delete)` ends is its own `DANGER_FORM` parenthesis — the mark whose job is to say the
button is dangerous, not where it stops.

**Mechanism.** Focus takes the matched pair and the press takes a different channel:

```
before   DEFAULT │  │   FOCUSED ▶  │   ACTIVE ▶  ◀    DISABLED ╌  ╌
after    DEFAULT │  │   FOCUSED ▶  ◀   ACTIVE ▶──◀    DISABLED ╌  ╌
```

`◀` is already this kit's closing rule at `textfield.main[ACTIVE]` and its BROUGHT BACK stepper
direction, so **no new cell enters the language**. ACTIVE now RULES THE ENTRY THROUGH with `─`, the
solid rule `textfield.main[EDITED]` already takes, and for the kit's own written reason: *"`─` is the
same stroke the bar's fill draws and it carries no meaning anywhere."*

**`▶··◀` was the first answer and was measured out.** The dot leader is ledger's `field.leader` and
already carries **six** families in the census; a button's middle would have taken that row to seven for
nothing. `─` carries none, and ledger's census count is unmoved at 2.

## 3. Cause and mechanism — swiss's confirm closes

**Cause.** `Swiss.overlay_instead` composed `[rule, ""] + list(rows)`. One rule, no second one. The
docstring called it *"the SINGLE HAIRLINE this language allows itself"*, and a band closed at one end is
not a band — it is a rule with text after it, so everything below the question read as part of it.

**Mechanism.** `block = [rule, ""] + list(rows) + ["", rule]`. Two rules of the same weight, the full
measure, no vertical and no corner: still not a box, which is the commitment (`MODAL_BORDER_REFUSED`).
Two rules around a block is the editorial device for a band, which is what this language calls it.

## 4. Cause and mechanism — swiss's freed channel

**Cause.** inc52 (ruling C) took `╲` — half swiss's `DANGER_FORM` — off `textfield.main[INVALID]`'s wall
and put the doubled stroke `║` there. Correct, and nothing moved into the channel that opened: the seat
stayed `"║  "`, a wall over blank paper with a blank closer, so `swiss_S2` row 6 was one wall and eight
characters. **The frame lost a wrong answer and gained none** — §7.6 of round three, verbatim.

**Mechanism.** `INVALID` becomes `"║┆║"` — the one field in this language that spends all three cells:

```
before   due•          ║12/09/26
after    due•          ║12/09/26┆┆┆┆┆┆┆┆┆┆┆┆┆┆┆┆┆┆┆┆┆┆┆┆┆┆║
```

Every cell is a stroke weight the kit already owns (`┆ │ ┃ █` and the doubled `║`): the walls are the
doubled rule on BOTH sides — a value struck out is bracketed, not merely marked — and the paper is `┆`,
the lightest stroke in the ladder, so the walls stand above their own ground. **EXTENT is the channel**,
which is the thing the round measured missing (*"decir hasta dónde llega el campo de fecha. Sin
respuesta."*), and it is said in the only ornament this language has.

## 5. The laws

**`test_both_answers_of_a_confirm_are_walled_by_their_declared_pair`**, over the eleven, **at three
widths** (8, 12, 20 — the round judged the whole corpus at ONE measure, §8.2, and `inc54.md` §7 wrote
that the destructive seat grew from 8 cells to 12 with nothing in the repo rendering S4 below 100):

1. each answer opens with the first half and closes with the second half of its own declared slot,
   asked of the **kit**, so a sheet cannot satisfy it with walls of its own;
2. the outer cell each answer closes on is a PAIR with the one it opens on — **the same mark, or that
   mark's declared mirror** (`WALL_MIRRORS`, derived once from the eleven and written down).

**Clause 2's first draft was "different from the next button's opener" and it was measured wrong.**
prism closes on `⠿` and opens on `⠿` — `⠿⠛ ⣿Delete⣿ ⠛⠿   ⠿⠉  Cancel  ⠉⠿` — so the two seats' adjacent
cells ARE the same mark and the row reads perfectly, because each seat is symmetric about its own word.
**Symmetry closes a seat; difference from a neighbour does not**, and the draft went red on prism for
doing the right thing. That is in the test's docstring, not only here.

**One exemption, named, with its citation asserted.** swiss declares no closing wall at all
(`BUTTON_HAS_NO_CLOSER`, inc38: *"no wall around a button at any width"* — in a language whose divider is
alignment, a control's extent is the next column's job). The arm asserts the closer really IS blank, so
a language cannot slip out of clause 2 by accident.

**`test_every_confirm_says_where_it_ends`** — C2's other half, over the eleven, read off the shipped
frames: the last row a confirm changes must SAY something. **Deliberately weak**: eleven languages close
a question eleven ways and a law demanding a rule would be one language's taste imposed on the other ten.
ledger's end is checked by name (its confirm closes on its own answers row, because this language posts
the question at the foot of the page) and swiss's is asserted to be a rule. **corgi is exempt with its
citation** — a confirm with no page behind it has no extent to close, and its refusal is asserted here
and in `test_corgis_confirm_keeps_the_mode_strip_and_nothing_else`.

**`test_swisss_rejected_field_has_a_wall_paper_and_a_closer`** — the follow-through, asserted as the
thing a reader does: the row has a first cell, a last cell and something between them that is neither the
value nor air; all three cells come from weights this language already spends **at this very part**; and
none of them touches the `DANGER_FORM` (ruling C, still).

## 6. One existing law had to be repaired, and the repair is a strengthening

`test_a_modal_changes_one_contiguous_band_of_the_page[swiss]` went **RED** the moment swiss's confirm
gained its closing rule:

```
AssertionError: ('swiss', [11, 12, 13, 14, 15, 16, 18, 20])
```

`modal_band` reads the rows that DIFFER from the page, which is the only thing a shipped frame can be
asked. The closing rule shifted the block up by one, and its two air rows landed on the page's own air
(rows 17 and 19) — **identical on both sides, so invisible to the reader, so the run came back with two
holes in it.** The composition was right and the proxy was wrong.

Repaired by measuring the run **end to end** and asserting that every row inside it which did not change
is blank on BOTH sides. The half that carries the meaning of "overlay" — every row OUTSIDE the run is
the page's own row at the same index — is untouched. The law is now stricter than it was: it used to
accept any contiguous run, and it now also says what a hole in one is allowed to be.

## 7. Teeth

**`test_the_answer_pair_law_bites_on_the_declaration_ledger_shipped`** puts `▶  │` back on the real
`Ledger.PART_GLYPHS` and sweeps all eleven at all four states: the red list is
**`[("ledger", "focused")]` and nothing else**. It then renders the row and asserts the round's own
count — `▶` once and `│` three times — and, after `monkeypatch.undo()`, `│` twice and `◀` once.

**The confirm-closing law's teeth are the frames themselves**: `swiss_S4`'s last changed row was blank
before this increment and is a rule after it, and the arm asserts the rule (`set(ends["swiss"]) == {"─"}`)
rather than merely that something is there.

## 8. The census went 25 → 26, and here is the whole of it

```
SWISS   2 colliding cells  ->  3
+  ┆   [5 families]  INVALID textfield.main mid  ·  checkbox.knob open (checked+disabled,disabled)
                     ·  checkbox.main open (…)  ·  stepper.step close/open (disabled)
                     ·  switch.knob mark (…)  ·  textfield.main open (disabled)
```

**The paper is the reason, and the cost is unavoidable for any paper at all.** `┆` was already spent at
six of swiss's control seats and carried no A-family, so it sat in the "shared between two CONTROLS only
(alphabet, not counted)" bucket. Giving the rejected field a paper adds the `invalid` A-family to it, and
the census counts a cell as colliding as soon as it carries an A-family plus anything else. **Every
candidate cell in swiss's declared alphabet is already spent somewhere**, so any paper at all costs
exactly this one row; the only zero-cost option was to paper the field in `║` itself, which is not a
third weight and not what the ruling asked for.

**And the row exists because the CENSUS counts the invalid RUNE as a meaning while the LAW does not.**
`_invalid_marks` has excluded the rune by name since inc52 — *"a field's glyph is wall, RUNE, wall, and
the rune is the paper the value lies on in every state, so counting it would have turned 'what a field is
made of here' into 'your value is wrong'"* — and `spec.md` §15.5 already names this discrepancy as
*"the one row five languages have left"*. swiss becomes the sixth. **The LAW's number is unchanged: live
meaning × meaning pairs are still 0** (the suite's own reader, green). What moved is one line of the
instrument's report, and the day the census adopts the law's rune exclusion all six rows go at once.

Reported rather than avoided, and rather than paying for it by not filling the channel the ruling said to
fill.

## 9. Frames changed

| frame | what moved |
|---|---|
| `ledger_S4` `.txt` `.svg` | row 32: `▶  (Delete)  │   │   Cancel   │` → `▶  (Delete)  ◀   │   Cancel   │` |
| `swiss_S4` `.txt` `.svg` | the band moves up one row and **closes on a rule at row 21** |
| `swiss_S2` `.txt` `.svg` | row 6: `║12/09/26` → `║12/09/26┆…┆║` |
| `gallery_ledger` `.txt` `.svg` | the component sheet's button row: `▶ ok │` → `▶ ok ◀` (focused), `▶ ok ◀` → `▶─ok─◀` (active) |

**`gallery_swiss` did not move**, and that is checkable rather than lucky: the component sheet is cut at
118×34 before its invalid-field row, which `spec.md` §12.5 already records for the stepper.

**Gallery 30–51 in the skill:** the batch close runs `export_to_skill.py`; see `spec.md` §16.

## 10. Gate tails, verbatim

```
$ python -X utf8 -m pytest -q
FAILED tests/test_app.py::test_win_clipboard_roundtrip - AssertionError: assert None == 'roundtrip 123 ABC taskboard'
1 failed, 1165 passed, 2 skipped, 4 warnings in 37.69s

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
swiss                        3
ledger                       2
TOTAL                       26
TOTAL homoglyph rows             1
                                                        (exit 0)

$ python -X utf8 prototypes/capture_languages.py
  22 grids identical across two PROCESSES
  22 captures -> ...\prototypes\gallery
  no two boards identical
                                                        (exit 0)
```

Suite **1151 → 1165** (+11 wall arms, +1 teeth, +1 confirm-end, +1 swiss field). Homoglyph rows **1**,
unchanged.

## 11. Risks

1. **The census went up.** §8 is the whole accounting. The law's number did not move; the instrument's
   report did, on a discrepancy that has a name and five other instances.
2. **swiss now draws four hairlines on `S4`** — the masthead's, the schedule's, and the confirm's two.
   The round's standing objection to `swiss_S1` is that a language committed to "one hairline" draws
   three; this makes the confirm sheet four. Taken deliberately: a destructive question that cannot say
   where it ends is a worse defect than a rule count, and C2 is the older objection.
3. **ledger's ACTIVE button changed shape**, not only its walls: `▶──◀` rules the word through where
   `▶  ◀` bracketed it. It is drawn in `gallery_ledger` and nowhere else, so one artefact carries the
   whole visible cost.
4. **`WALL_MIRRORS` is a written table.** It is derived from the eleven kits and every entry is a pair
   some kit already declares at this seat, but a language reaching for a new asymmetric pair has to add
   a row and say why — which is the point, and is also the thing that will look like friction later.

## 12. Found by looking, not fixed

- **`ledger_S4`'s destructive answer is still on the terminal's last row.** The confirm now closes — its
  last changed row says something — but what it closes on is the answers themselves, because this
  language posts at the foot. The round's *"below `(Delete)` there is nothing, not a pager and not a
  seam, so the modal's lower limit is the edge of the terminal"* is answered only in the weak sense the
  law asserts. A confirm that reserved a row under its answers would be a composition change in
  `Ledger.overlay_instead` and is not C2.
- **swiss's `Save` is still air** (L2, open for three rounds and six batches). The freed channel got
  filled at the FIELD; the disabled button next to a `Cancel` that has a mark is a different seat.
- **`─` is `LEVELS["warn"]` in swiss and is what both of the confirm's rules are drawn with.** The band
  that closes the question is drawn in the warn rung, twice, on a screen with a destructive answer on it.
  Named here rather than left: `rule_color` and the rung share a cell, the census counts `─` as
  colliding for swiss already, and no ruling covers it.
- **The mirror table has eleven entries and the corpus has eleven languages, which is a coincidence.**
  Six kits close on a mark identical to their opener and never need it.

## 13. Pending — not this increment

- The batch close: `export_to_skill.py`, `spec.md` §16.
- K5, K2, K4, L2, L6, L7, L10, C5, C6, C7, C9, C10, E2, E3, G1, G2 — open.
- The census's rune discrepancy (§8), now six languages.

## 14. Suggested next task

Close the batch: run `export_to_skill.py`, record which of the skill's gallery 30–51 changed byte-wise,
and write `spec.md` §16 for `rework-6a` with the five rulings, the frames changed and the census
accounting.

## Evidence checklist

- [x] **Tests/type checks/lint pass — WITH ONE RED, NAMED.** `1165 passed, 2 skipped, 1 failed`
      (inc65 closed at `1151 passed`). The failure is
      `tests/test_app.py::test_win_clipboard_roundtrip`, environment-coupled (spec §10.6) — **reported,
      not counted, not touched.** `verify_language.py` ALL PASSED exit 0. `render.py` 66 frames / 330
      pairs / 0 hand-drawn. `matrix.py` refusals `[]` for all eleven. `capture_languages.py` plain: 22
      captures, 22 grids identical across two processes, 2 artefacts moved (`gallery_ledger`).
      `collision_census.py` both self-checks green, **TOTAL 25 → 26** with the +1 accounted for in §8,
      homoglyph rows 1.
- [x] **No secrets in code or output** — two kit declarations, one overlay block, three laws, one teeth,
      one existing law strengthened. No network, no new dependency, no path outside the worktree.
- [x] **No destructive commands run without approval** — none.
- [x] **File count within cap** — **2 source files**: `taskboard/language.py`,
      `tests/test_components.py`.
- [x] **Review packet attached** — this document.
