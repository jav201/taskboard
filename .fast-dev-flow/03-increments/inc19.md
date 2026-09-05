# Increment 19 — `Kit.match` (the content law, byte for byte) and `Kit.keyhint` (the keymap is the caller's)

**Batch:** `kits-learn-3` · **AC-6** · operator rulings 9 and 3 of 2026-09-04
**Files:** `taskboard/language.py`, `tests/test_components.py`, `prototypes/components/screens.py` —
**3 source files**.

**S6 reaches `implementa` in all five languages.**

---

## 1. The defect

The command palette's result row was composed by hand from a precomputed span, and the hint row was
assembled from the fixture's pairs with the frame choosing the notation. Two rulings meet here:

- **ruling 9** — a result row must return the text **byte for byte**, and three of these languages letter
  their titles in capitals everywhere else;
- **ruling 3** — corgi **labels** its buttons and **numbers** its keymap, which is the same finding L-33
  cost a consumer app 1200 seconds to discover: *a mark that encodes a binding belongs to whoever owns the
  keymap. Never the library.*

---

## 2. The mechanism, and the one place a mark cannot be a shape

`Kit.match(text, query) -> str`. The kit finds the query (case-insensitively) and marks the run **at the
text's own bytes** — `RE` typed against `redirect` marks `re`, because the row shows the TEXT and the query
only says where to look. No match is a **case**, not an error: the text comes back unmarked, which is what
a result row should look like while a query is still being typed past it.

**And the emphasis cannot be a glyph.** Every other mark in this file adds a cell — a wall, a dagger, a
dot, a terminator — and adding a cell *here* would break the byte identity that is the whole ruling. What
is left is the **style** channel:

```
nord/base   bold {accent}        naught  bold {ink}       corgi  bold {ink}
prism       bold {accent}        ledger  underline {ink}  blueprint  bold {ink}
```

**Ledger's is the one with a reason older than terminals**: a ledger *rules under* a referenced figure. It
is not a hue, and it points at an amount without restyling it — exactly what ruling 9 asks for.

`bold`, `underline` and `reverse` are not hues, so "never colour alone" holds in a real terminal. **They
do not survive a cell grid**, so a `.txt` of a result row has no emphasis in it at all. That is recorded at
the seat, asserted in a test, and it is the same limit the PROTOTYPE packet already found in blueprint's
knockout: *the `.txt` is the work, and for two marks in this contract it is not enough.*

`Kit.keyhint(pairs, w=0) -> str` — the kit owns the notation, the caller owns every key:

```
nord        ↑↓ move   enter run   esc close
naught      ↑↓∙move   enter∙run   esc∙close          the lattice's own bullet
corgi       [↑↓] MOVE   [enter] RUN   [esc] CLOSE    the bracket — its keybinding notation
prism       ↑↓⣶move   enter⣶run   esc⣶close          the ember frontier at one cell
ledger      ↑↓··MOVE   enter··RUN   esc··CLOSE       leaders, like every other gap on the page
blueprint   ↑↓──MOVE   enter──RUN   esc──CLOSE       an extension line from the key to what it does
```

**Ruling 3 is both halves of one sentence.** The numbers are not banned, they are **placed**: `button()`
never prints a digit the caller did not pass (asserted over all eleven languages, on four different
buttons), and corgi's bracket is spent on the row that says which key does what — where §3b's *"in a TUI
the numbers ARE the keybindings"* makes it functional rather than decorative.

---

## 3. Files modified

| file | what |
| --- | --- |
| `taskboard/language.py` | `MATCH_STYLE` + `Kit.match` + `Kit.keyhint` at the base; 5 per-language styles and 5 keyhint notations |
| `tests/test_components.py` | 8 new laws, 68 new tests |
| `prototypes/components/screens.py` | S6's result rows and hint row through the kit; corgi's S4 hint row too; `C_MATCH`, `C_HINT` and the whole `s6_corgi` override deleted |

`s6_corgi` existed only to letter the hint row in corgi's own notation. That notation is `keyhint` now, so
the override is gone — **the fourth per-language builder this batch has deleted from the prototype**, and
every one of them was a language's mechanism living in the frame instead of in the kit.

---

## 4. The property test

`test_match_returns_the_text_byte_for_byte` asserts with `==` on the plain row, not `in`: an emphasis that
added a single cell goes red, and so does any recasing, in all eleven languages, for `re`, for `RE`, and
for `MiXeD CaSe Title`.

Beside it: the marked run is the text's bytes at the query's position; a query that no longer matches comes
back with no style token at all; every `MATCH_STYLE` carries a weight/underline/reverse word (the "not a
hue alone" law, asserted rather than promised); `keyhint` prints the key it was handed; **no button
numbers itself**; corgi's numbering *does* appear in the hint row; and five languages letter five hint
rows.

---

## 5. Test results

```
python -X utf8 -m pytest -q
682 passed, 2 skipped, 4 warnings in 29.18s          (inc18 left it at 614 — +68)

python -X utf8 prototypes/verify_language.py
2 FAILURE(S)  — the two pre-existing ones (F-14), unchanged

python prototypes/capture_languages.py --surface     # plain and alone (F-8)
11 surfaces ; moved vs baseline-kits2: the same four as inc14
```

---

## 6. The capture (AC-7)

```
python -X utf8 prototypes/components/render.py
26 hand-drawn elements declared (4 refused, 22 evoked)      (inc18 left it at 36)

corgi_S6  0    blueprint_S6  0    prism_S6  0    naught_S6  0    ledger_S6  0
corgi_S4  0     (its hint row was the last hand-drawn thing on that frame)
```

Ten elements gone: `match` ×5 and `keyhint` ×5. **S6 is `implementa` in all five**, and corgi's S4 joins
it for the same reason.

---

## 7. Risks

- **The match emphasis is invisible in the `.txt`.** Two of this batch's marks now live only in the SVG
  (blueprint's knockout, every language's match). A review that reads only cell grids will not see either,
  and the house convention says the `.txt` is the work.
- **`match` finds the FIRST occurrence.** A palette that highlights every hit needs a different signature;
  this one answers the question the ruling asked.
- **Case-insensitive `find` is ASCII-shaped.** `str.lower()` is Unicode-aware, but a language with
  case-folding subtleties (Turkish dotted `İ`) can produce an index that is right for the folded string
  and wrong for the original. Not defended against; recorded.
- **Five languages inherit the base hint row and the base match style.**

## 8. Pending

- `pane_split` and `readout_label` — the last two primitives holding cells back (spec §6.3).
- `required`, `textarea`, `Kit.error` — S2's three, none of them ruled on.
- A `TAIL` mark of its own, if the operator wants the log's live edge distinct from a select's disclosure.

## 9. For the skill

- **The content law has a corollary worth stating: a mark that must not add a cell has only the style
  channel, and the style channel does not survive a cell grid.** That is a real constraint on TUI search
  UIs and it is not obvious until you try to write the test.
- **`COMPONENTS.md`'s search row should say what may NOT happen to the text** — no recasing, no
  truncation, no ellipsis — because every language here has a habit that would otherwise apply.
- **The keymap belongs to the caller, and the notation to the language.** Corgi is the worked example in
  both directions: brackets on the hint row, words on the button.
