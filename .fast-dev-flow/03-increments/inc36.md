# Increment 36 — `pane_split` for the six that inherited it

**Batch:** `inheritors-2` · the second half of `kits-learn-4` §5's declared debt
**Files:** `taskboard/language.py`, `tests/test_components.py` — **2 source files**.

**Six languages were ruling a pane seat with the terminal's `│`, and three of them had committed against
that stroke in writing. `PANE_SPLIT_REFUSED` goes from two entries to five; instrument and industrial draw
their own; nord declares the base. Six drawers, six pairwise-distinct rules. The width sweep the property
came with found a REAL closure defect in blueprint — `w=1` returned two cells for a one-cell seat — which
had been there since inc28 and which no test at the design width could see.**

---

## 1. The state this increment found

```
naught  ◦    corgi  █    ledger ═══/│    blueprint ┤ ├ + air    prism <grey step>
instrument │    swiss │    industrial │    nord │    darkside │    solari │
```

Six languages ruling the base kit's hairline. **Three of the six had already committed against it**, in
`LANGUAGES.md` and in this repo's own registry comment, which named two of them as the batch's debt:

> "SWISS AND DARKSIDE BELONG HERE AND ARE NOT HERE YET. 'No boxes — alignment does the dividing' and
> 'depth by ±1 grey step, never borders' are the same two commitments this table exists for."

---

## 2. The six answers

### The three that joined the registry

| language | § | the commitment, and what it decides |
| --- | --- | --- |
| **swiss** | §2 | *"NO BOXES — alignment does the dividing"*, and the language allows itself **exactly one hairline rule**, which the masthead has already spent. Two panes are two columns of the same grid: the right one starts at the next column and the emptiness IS the division |
| **darkside** | §8 | *"depth by ±1 grey step of background, **never borders**"*. Prism inherited this doctrine **and** the exception written into it (*"borders are RESERVED for modals"*), so the parent refuses here for the reason the child does, one generation earlier |
| **solari** | §10 | *"the structure device is the cell FACE a character is flipped onto, so the language **spends no rule at all** and keeps its strongest divider unspent"* — with *"tabular fields padded to their widest content"* saying what holds two columns apart instead |

**Solari's is the third KIND of refusal in this table.** Blueprint's is ALPHABETIC (the mark does not
exist in its ten), prism's is DOCTRINAL (the mark exists and the language has forbidden itself to spend
it); solari's is **structural** — it *has* a divider, the seam, and it has committed to spending no other
one. That distinction is why this is a registry with a citation per entry and not a flag.

### The two that draw

**instrument — a graticule column, `⠸`.** §1 says "borders almost absent", which is not "no marks": this
language already rules a graticule *across* a field row, and **a graticule is not a border — it was on the
glass before either pane arrived**. It refuses a modal lid (`MODAL_BORDER_REFUSED`) because a lid
*encloses*; a graticule *measures*.

**The column is the right one and that is not decoration.** `⠇` — three dots, left column — is this
language's **error rung** (`⠇⠇`), and a neutral divider wearing the severity ladder's cell would say
"rejected" down the whole gutter to a greyscale reader. `⠸` is the same three dots in the other column and
says nothing else in this alphabet. `test_instruments_graticule_column_is_not_its_error_rung` asserts it
against `LEVELS`, `DISCLOSE` and `DANGER_FORM` at once.

**industrial — two plates, facing: `▌ ▐`.** §3's "boxed groups" makes this **the only one of the eleven
whose commitment asks for a box**, and inc32 already made it draw its modal lid in half-cell plate rather
than the terminal's hairline. A gutter is the same claim: the left pane closes and the right pane opens,
each in its own plate.

**The order is `keyhint`'s, not a new one.** That row plates a key as `▐up▌` — the ink faces the
*content* — so a gutter closes the left pane with `▌` and opens the right with `▐`, and the air between
belongs to the panes. Read the two rows together and it is one convention, which is the whole argument for
a language having an alphabet.

### nord — §6, and it declares

`PANE_RULE`, `pane_split_rule` and `pane_split_instead` join
`test_nord_declares_the_environment_and_the_declaration_is_checked`. The base kit's docstring already says
"BASE (nord) IS THE TERMINAL'S OWN: a hairline rule at the dim tier"; that sentence is now walked in the
MRO rather than believed.

---

## 3. The defect the property test found

`test_the_closure_law_holds_on_every_pane_seat_at_every_width` asks `w ∈ {1, 2, 3, 4, 7, 12}` and
`h ∈ {0, 1, 5}` of all eleven. It went red on the first run:

```
FAILED tests/test_components.py::test_the_closure_law_holds_on_every_pane_seat_at_every_width[blueprint]
E   AssertionError: ('blueprint', 1, ['┤├'])
```

**Blueprint's registration pair was written unconditionally**, so at `w=1` it returned TWO cells for a
one-cell seat — the one thing `pane_split`'s own contract forbids, because a row that is not `w` wide moves
the right pane down the page. It has been there since inc28 and the existing test could not see it: that
test asks one width, 3, which is the width every caller happens to use.

**The fix is one predicate and it is the language's own argument.** The docstring already said "one row of
declaration and `h-1` rows of nothing is a DIMENSION — it states an extent and then stops"; below two
cells there is no extent to state, so the declaration row is not drawn at all. The honest degradation for
a language whose refusal *is* air is more air.

Industrial's new mechanism was written with the same guard from the start (it draws two marks and falls
back to one below two cells), which is why the sweep found the old defect and not a new one.

---

## 4. The eleven, measured

```
naught      draws    ' ◦ ' | ' ◦ ' | ' ◦ ' | ' ◦ '
corgi       draws    ' █ ' | ' █ ' | ' █ ' | ' █ '
instrument  draws    ' ⠸ ' | ' ⠸ ' | ' ⠸ ' | ' ⠸ '
industrial  draws    '▌ ▐' | '▌ ▐' | '▌ ▐' | '▌ ▐'
nord        draws    ' │ ' | ' │ ' | ' │ ' | ' │ '
ledger      draws    '═══' | ' │ ' | ' │ ' | ' │ '
swiss       refuses  '   ' | '   ' | '   ' | '   '
darkside    refuses  '   ' | '   ' | '   ' | '   '   (+ a grey ground in markup)
prism       refuses  '   ' | '   ' | '   ' | '   '   (+ a grey ground in markup)
solari      refuses  '   ' | '   ' | '   ' | '   '
blueprint   refuses  '┤ ├' | '   ' | '   ' | '   '
```

**Six drawers, six distinct rules.** The distinctness law is asked of the drawers and not of all eleven,
and the reason is stated in the test rather than assumed: four of the five refusals answer with air, and
two of those four are a grey STEP of *background* which a cell grid cannot show. A distinctness law over
eleven would be a law about that limit rather than about a design.
`test_darkside_and_prism_step_the_ground_and_swiss_and_solari_do_not` is the test that keeps the four
apart where they differ — in the markup — and states the limit where they do not.

---

## 5. The property tests

| test | what it holds |
| --- | --- |
| `test_every_language_that_draws_a_pane_rule_draws_a_different_one` | **6 / 6 distinct** among the drawers, on the plain cells. `DRAWERS` is derived from the registry, so a language changing sides moves this list with it |
| `test_the_closure_law_holds_on_every_pane_seat_at_every_width` (×11) | `h` rows of exactly `w` cells at six widths and three heights — §3's finding |
| `test_the_three_new_refusals_are_read_and_not_printed` (×3) | delete swiss/darkside/solari's entry and each goes **straight back to `│`**, the stroke it committed against, with no other line of its code touched |
| `test_a_false_entry_silences_any_language_that_draws` (×6) | a false entry silences **any** of the six that draw, not just naught. A table that only bites the languages already in it decides nothing for the ones that are not |
| `test_a_refusing_language_rules_no_stroke` (now ×5) | parametrised off the registry instead of a typed pair, so a new entry is tested the moment it is added |
| `test_industrial_closes_one_pane_and_opens_the_next_in_its_own_chrome` | `▌ ▐`, the `DISPLAY_BOX` glyphs it claims, at `w=5`, and the one-cell degradation |
| `test_instruments_graticule_column_is_not_its_error_rung` | `⠸`, and not in `LEVELS`, `DISCLOSE` or `DANGER_FORM` |
| `test_nord_declares_the_environment…` (+3 attrs) | nord's `PANE_RULE`, `pane_split_rule` and `pane_split_instead` are owned by `Kit` |

---

## 6. Test results

```
python -X utf8 -m pytest -q tests/test_components.py    576 passed in 0.78s      (was 546)
python -X utf8 -m pytest -q                             930 passed, 2 skipped   (was 900)
python -X utf8 prototypes/verify_language.py            10857 PASS · ALL PASSED (baseline 10857)
python -X utf8 prototypes/components/render.py          30 frames · 0 hand-drawn · 60 pairs, none identical
git status --short                                      M language.py · M test_components.py
```

`render.py` rewrote all 30 frames and 30 sidecars and **none changed on disk** — the five prototyped
languages' splits are untouched, blueprint's `w=1` fix moves nothing because no caller asks for `w=1`, and
the six that changed render in no frame until inc37.

---

## 7. Risks

- **Blueprint's `w=1` was live for eight increments and nothing noticed.** The fix is right; the finding
  worth carrying is that the *only* width anyone tested was the only width anyone calls. The same shape
  may exist in the other seats that take a `w` — `error`, `textarea`, `overlay` — and this increment did
  not sweep them.
- **Four refusals read identically in the `.txt`.** Swiss, solari, darkside and prism are three different
  commitments and two different mechanisms collapsed to `w` spaces in a cell grid. The `.svg` separates
  darkside and prism from the other two; nothing separates swiss from solari, and nothing should —
  air is genuinely both their answers.
- **Darkside duplicates prism's four lines.** Deliberate (prism is `Kit`'s child, not darkside's, and
  making one call the other would assert a class relationship the file does not have) — but it is
  duplication, and a change to one will not reach the other.
- **`⠸` has never been photographed.** Its distinctness from `⠇` is asserted as a cell, and whether a
  reader can tell a right-column graticule from a left-column error rung at 100×32 is a question inc37's
  frames can answer and this increment cannot.
- **`▌ ▐` spends two cells of a three-cell gutter.** At the seat's design width that leaves one cell of
  air between two plates; at `w=2` there is none at all, which is legal and dense. Industrial is the
  language that would want it that way, but nobody has looked.
- **The registry is five of eleven.** Every entry is cited, and the counter-risk is real: a table this
  large starts to look like the default. `test_every_language_that_draws_a_pane_rule_draws_a_different_one`
  is what keeps the other six honest.

## 8. Pending

- **The six render in no frame** — inc37, and it is the increment that can falsify §7's last four bullets.
- **The `w` sweep for the other seats that take a width** — not done, named here.
- **F-8** (`--surface` plain and alone) and the export — at the batch close.

## 9. Suggested next task

inc37 — the six screens through the six inheriting languages: 36 new frames, the matrix at 11×6.

---

## Evidence checklist

- [x] **Tests/type checks/lint pass** — `930 passed, 2 skipped` (§6). `verify_language.py` **ALL PASSED**
      at 10857. `render.py` green and no frame moved. The three new registry entries are red-then-green
      against a deleted entry, and all six drawers against a false one (§5).
- [x] **No secrets in code or output** — three registry entries, two render methods, one class constant,
      one predicate, and tests. No network, no dependency, no path outside the worktree.
- [x] **No destructive commands run without approval** — none run.
- [x] **File count within cap** — 2 source files, plus this packet: 3.
- [x] **Review packet attached** — this document.
