# Increment 30 — `Kit.textarea`: the field over a rectangle, and it declares nothing per-language

**Batch:** `kits-learn-4` · **AC-3**
**Files:** `taskboard/language.py`, `tests/test_components.py`,
`prototypes/components/screens.py` — **3 source files**.

**S2 reaches `implementa` in all five. The only cells left in the matrix are S5's two refusals.**

---

## 1. The defect

```python
op, rune, cl = k.field_form(DEFAULT, "textfield")
for i, line in enumerate(F.NOTES):
    sh.row("  " + head + f"[{c['dim']}]{LG.mark(op)}[/]"
           + f"[{c['ink']}]{LG.mark(pad(line, 34))}[/]"
           + f"[{c['dim']}]{LG.mark(cl)}[/]", C_TEXTAREA)
```

The frame reaching into `field_form` and composing a component out of its parts. It is closer to right
than the `│` or the `*` were — it *does* ask each language for its walls — but it is still a component
being assembled by a caller, with the caller deciding that a rectangle has no caret, no wrap behaviour
and no unlit remainder except the one it pads by hand.

---

## 2. The mechanism, and the finding is what it did NOT need

`Kit.textarea(lines, caret, w, h, state) -> list[str]`.

**Not one per-language constant was added, and that is the increment's result rather than a shortcut.**
Every mark this component needs is already a seat:

| what | where it already lived |
| --- | --- |
| the walls and the paper | `field_form(state, "textfield")` |
| the caret's glyph and tone | the `caret` part in `PART_GLYPHS` / `part_tone` |
| the lit / unlit tiers | `check_tone`, `part_tone("main", …)` |
| the wrap mark | `DISCLOSE` |

**A language that answered the one-line field has already answered this one.** A `TEXTAREA_*` table
beside those would have been eleven restatements of six existing decisions — and the property test says
so out loud: if `test_five_languages_paper_five_rectangles` ever goes red, a language has lost its
`field_form` or its caret part, not its textarea.

```
corgi       ▔▔ship the kit▁▁▁▁▁▁▁▁▔▔        ▔▔check▌ the sweep▁▁▁▁▔▔
blueprint   ╞ship the kit╌╌╌╌╌╌╌╌╡          ╞check╪ the sweep╌╌╌╌╡
prism       ⣿ship the kit⣤⣤⣤⣤⣤⣤⣤⣤⣿          ⣿check⡆ the sweep⣤⣤⣤⣤⣿
naught      ○ship the kit∙∙∙∙∙∙∙∙○          ○check◉ the sweep∙∙∙∙○
ledger      ▶ship the kit∙∙∙∙∙∙∙∙│          ▶check▏ the sweep∙∙∙∙│
```

**Three decisions the seat does make:**

- **The caret takes a column of its own, on ONE row.** `caret` is `(row, col)` — a field has exactly one
  insertion point, and a mark on every row would draw a state the model cannot be in. The column is the
  one-line seat's law for the one-line seat's reason: a block caret *on* a character hides it, and the
  only way to keep it readable underneath is reverse video, which is colour.
- **The line breaks are the caller's.** It passes `lines`; a kit does not know where this app's
  paragraphs end.
- **The wrap mark is `DISCLOSE`, the third component to spend it.** A select points at a list, a log's
  tail at the line that has not arrived, a wrapped row at the text that did not fit. Same declaration.

**And that is the one place the bytes stop.** A one-line field moves its *window* sideways; a rectangle's
rows cannot. An over-long line shows its own leading bytes, in order, unrecased, and says with a mark
that there are more. Nothing is substituted and nothing is silently dropped — but "byte for byte" holds
for the lines that **fit**, and that is written at the seat rather than found in a frame.

---

## 3. Files modified

| file | what |
| --- | --- |
| `taskboard/language.py` | `Kit.textarea` — one method, no per-language line |
| `tests/test_components.py` | 7 new laws, 57 new tests |
| `prototypes/components/screens.py` | S2's notes rectangle through the kit; `C_TEXTAREA` deleted |

---

## 4. The property test

`test_a_three_line_text_renders_three_rows_with_a_visible_caret_row` — the operator's own wording, and it
is two claims in one sentence: **three lines, three rows** (row `i` is line `i`, nothing reflowed
underneath), and **exactly one visible caret row** (`marked == [1]`, not "at least one"). The line's bytes
are asserted with the caret glyph removed, because the caret's column *splits* its row — that is the
mechanism, not a defect.

Beside it: the rectangle comes back at `h` rows of `w` cells between the walls for no lines, three lines
and twelve lines; a line that fits comes back byte for byte including `"Q3 -1,204.55 [ref]"` and
`"AbCd  eF"`; an over-long line ends in the language's `DISCLOSE` **and** still carries its leading bytes;
the wrap mark is that same `DISCLOSE` in all eleven; the five rectangles differ as cells; and
`caret=None` draws no caret anywhere — which is S2's own case.

---

## 5. Test results

```
python -X utf8 -m pytest -q
808 passed, 2 skipped, 4 warnings in 32.67s        (inc29 left it at 751 — +57)

python -X utf8 prototypes/verify_language.py
10857 PASS · ALL PASSED                            (baseline unmoved)
```

---

## 6. The capture

```
python -X utf8 prototypes/components/render.py
2 hand-drawn elements declared (2 refused, 0 evoked)     (inc29 left it at 7)
no two frames identical within a screen (60 pairs)
```

**Zero evoked elements remain in the whole sweep.** The five that are gone are `Kit.textarea` ×5, and the
matrix is at **28 of 30**:

```
              S1              S2              S3              S4              S5              S6
corgi     implementa      implementa      implementa      implementa    rehusa 1R/0E    implementa
blueprint implementa      implementa      implementa      implementa      implementa    implementa
prism     implementa      implementa      implementa      implementa      implementa    implementa
naught    implementa      implementa      implementa      implementa      implementa    implementa
ledger    implementa      implementa      implementa      implementa    rehusa 1R/0E    implementa
```

The only two cells left are corgi's and ledger's S5, and both are the **same refusal**: L-33, the readout
that is labelled and never numbered.

---

## 7. Risks

- **No frame photographs the caret row.** S2's caret is in `title`, and a form with two insertion points
  is a state the model cannot be in — so the notes rectangle is drawn in `DEFAULT` with `caret=None`, and
  the caret row is exercised only by the property test across all eleven. That is a real gap in a round
  whose artefact is frames, and the honest fix is a screen that focuses a textarea, which S2 is not.
- **Blueprint's wrap mark and its EDITED paper are the same glyph** (`╌`). They are toned differently
  (accent vs ground), which is a colour-only distinction and this contract's own least favourite kind. It
  only ever appears after a letter rather than after paper, so the row still reads — recorded, not
  designed around.
- **"Byte for byte" is now conditional.** It holds for lines that fit. Every other seat in this contract
  states it unconditionally, and a reader who carries the rule across will be wrong here.
- **`w` is the room between the walls, and corgi's walls are two cells each.** A caller sizing a column
  by `w` alone under-counts corgi by four. `textfield` has the same property; nothing enforces it.

## 8. Pending

- `Kit.readout_label` (inc31) — the last two cells.
- The six inheriting languages (inc32).

## 9. For the skill

- **The best outcome for a new primitive is that it needs no new per-language declaration.** A component
  library that keeps growing its per-language tables is a library whose parts do not compose. This one is
  a rectangle of an existing component and it should cost exactly what a rectangle costs.
- **COMPONENTS.md should name the three seats a multi-line field reuses** — walls/paper, the caret part,
  the disclosure mark — so the next person writing one does not open a fourth table.
- **State where the content law stops.** "The value comes back byte for byte" is a promise a rectangle
  cannot keep for a line wider than its rows, and the mechanism that says so is the same disclosure mark
  the rest of the language already spends.
