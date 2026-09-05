# Increment 17 — `Kit.overlay`, and a refusal registry with teeth

**Batch:** `kits-learn-3` · **AC-4** · operator rulings 4, 5 and 10 of 2026-09-04
**Files:** `taskboard/language.py`, `tests/test_components.py`, `prototypes/components/screens.py` —
**3 source files**.

---

## 1. The defect

S4 was the screen where the five languages' answers were furthest apart, and the prototype had to write
**five separate builders** to say so — four of which existed to draw the *absence* of a frame. Four
languages had a commitment against a box and no way to say it in code, so "naught has no overlay" was a
sentence in a design note: true, unenforced, and unfalsifiable.

---

## 2. The mechanism

### The registry is READ, not printed

```python
MODAL_BORDER_REFUSED = {"corgi": ..., "blueprint": ..., "naught": ..., "ledger": ...}
```

`Kit.overlay` consults it **before it draws anything**. A language named there never reaches the box code,
whatever it did or did not override — it gets `overlay_instead`, which is what the language does with a
question when it may not put a surface in front of the page.

That makes the table falsifiable **in both directions**, which is the whole difference between declaring a
refusal and describing one, and there is a test that runs the mutation:

- delete `"naught"` → naught draws the terminal's lid, violating one of its four commitments;
- add `"prism"` → the one language whose doctrine *licenses* the border stops drawing it.

Neither language's code is touched in either direction. **The table is what decides.**

**Prism is absent on purpose.** "Depth by one grey step, never borders — borders are RESERVED for modals"
is the only commitment in the eleven that names this component as its exception.

### Six answers to "a question in front of a page"

| language | what it composes | what it refuses |
| --- | --- | --- |
| **nord / base** | a box, centred, over a page dropped to the dim tier | — (the environment's convention) |
| **prism** | the same box, over a page stepped back by **one grey step of BACKGROUND** (`recede` override) | — (licensed) |
| **naught** | the page keeps every dot and **loses its charge**; the question is the only lit region, bounded by the lattice at full charge | the frame — ruling 4 |
| **corgi** | the rows, **centred on an empty panel** — the backdrop argument accepted and dropped | the superposition: "the mode takes over the screen" |
| **ledger** | the question **posted at the foot, under a rule, with the page above at FULL STRENGTH** | the surface in front: a ledger has no such thing |
| **blueprint** | **registration marks, four corners that never join**, air where a stroke would be, sheet receding behind | the box: no vertical stroke exists in its ten marks |

**Ledger's is the one that inverts the others.** Every other answer dims what is behind; ledger keeps it at
full strength, because dimming the postings would be the language claiming they are less true while a
question is open, and they are not.

### `knockout_cell`, and ruling 10

The inversion had been inline in blueprint's `stamp()`. It now has **one seat**, and blueprint's title
block calls it — which is what makes ruling 10's move legal: *a mark that can move needs somewhere to move
to, and two copies of it spelled the same way is not that.*

**Why the move is affordable, arithmetically.** `_state_cell` spends the reverse on the **`alert` mood
alone**, so a calm sheet carries no knockout at all. The prototype's S4 sheet is calm, so its single
knockout is **unspent** and the confirm may take it with the title block losing nothing. "Exactly one
element per view" holds by arithmetic rather than by promise.

---

## 3. Files modified

| file | what |
| --- | --- |
| `taskboard/language.py` | `visible()` (a markup→cells helper the module never had); `MODAL_BORDER_REFUSED`; `Kit.overlay`, `Kit.overlay_instead`, `Kit.recede`, `Kit.knockout_cell`; 4 refusal answers + prism's `recede`; `stamp()` routed through `knockout_cell` |
| `tests/test_components.py` | 10 new laws, 33 new tests |
| `prototypes/components/screens.py` | **five S4 builders collapse into one** + a thin blueprint override for the knockout; `C_SCRIM` deleted; `carry()` decides backdrop candidates by looking at the composed rows |

---

## 4. The property test

`test_the_registry_is_read_and_not_printed` is the load-bearing one — the mutation in both directions,
described above. Around it: the registry names languages that exist and carries a *reason* for each (a
declared refusal with an empty string is a comment with a dict around it); every language returns exactly
`h` rows (a composition that returned fewer would push the screen up); the four refusers draw **no lid**;
prism draws one.

**`has_lid` is written on what actually makes a box** — two corner marks with a *run of rule* between them
— and not on corner glyphs, because blueprint's cursor **is** a corner and ledger rules a line across the
whole measure on every page. The oracle had to learn the same lesson inc16's did: *a law written from the
shape of the common case flags the language with the most specific answer.*

Then the three positive laws, one per refusal that has content rather than absence: corgi's screen contains
**none** of the backdrop; ledger's `out[0]` is `under[0]` **byte for byte** (not receded); naught's has
exactly **two** fully-lit lattice rules and a backdrop in the dim tier.

---

## 5. Test results

```
python -X utf8 -m pytest -q
558 passed, 2 skipped, 4 warnings in 32.65s          (inc16 left it at 525 — +33)

python -X utf8 prototypes/verify_language.py
2 FAILURE(S)  — the two pre-existing ones (F-14), unchanged; the title block's
               knockout now comes from `knockout_cell` and every stamp check stayed green

python prototypes/capture_languages.py --surface     # plain and alone (F-8)
11 surfaces ; no two identical ; moved vs baseline-kits2: the same four as inc14
```

The language sweep **was** re-run here (spec §4) because `stamp()` is a render path it checks hard, and
routing an inversion through a new seat is exactly the kind of change that moves a frame by one cell.

---

## 6. The capture (AC-7)

```
python -X utf8 prototypes/components/render.py
46 hand-drawn elements declared (4 refused, 42 evoked)      (inc16 left it at 53, 8 refused)

corgi_S4      0 candidates
blueprint_S4  1 (pane_split, refused)   prism_S4  1   naught_S4  1   ledger_S4  1   (pane_split)
```

Seven elements gone: `overlay` ×5 and `knockout_cell`, plus the backdrop's own carry for corgi. The four
remaining S4 candidates are **all `pane_split`**, carried in from the S1 backdrop — named in spec §6.3
before the batch started as the reason those cells cannot reach `implementa`. corgi's is gone for a reason
worth stating: its answer discards the backdrop, so the backdrop's hand-drawn divider is **not on the
screen**, and `carry()` decides that by looking at the composed rows rather than by a list of language
names.

---

## 7. Risks

- **corgi_S4 is 2.7 % ink**, and that is the increment's real finding rather than a bug. A refusal that
  discards the backdrop leaves the FRAME owing content: five rows of a dialog's words, centred on a
  100×32 panel, is not a mode — it is a dialog with its box and its page taken away. The kit is right and
  the frame is thin. **A mode-takeover needs its own layout** (a header, the mode's number, the panel's
  furniture), and no kit method can invent it from `rows`.
- **The knockout does not survive the `.txt`.** An inversion is a background; the cell grid shows the word
  and not the emphasis. The house convention is that the `.txt` is the work — here it is not enough, which
  the PROTOTYPE packet already recorded and this increment does not fix.
- **`overlay` centres vertically and cannot scroll.** A dialog taller than the screen is clipped by the
  caller. No language declares an answer for that.
- **`visible()` is a fifth copy of the same twelve lines** (screens.py, the sweep, two verify scripts).
  It is now in the module the others import, but nothing was deleted from them: consolidating is a
  refactor and this batch is not it.

## 8. Pending

- The five unruled languages' `overlay_instead` (they take the base box: instrument, swiss, industrial,
  darkside, solari, plus nord which IS the base).
- `pane_split` — the last thing standing between four S4 cells and `implementa`, and the same for all five
  S1 cells. It is the obvious first item of the next round.
- A per-language answer for **corgi's mode furniture** (see §7).

## 9. For the skill

- **`COMPONENTS.md`'s "dialog / sheet" row should carry all six compositions**, because the spread is the
  lesson: two languages draw a box, one drops the page's charge, one takes the screen, one posts the
  question on the page and keeps it at full strength, one draws four corners that never join.
- **A refusal registry is a mechanism, not a note** — and the test that proves it is the mutation in both
  directions. That pattern (`LABEL_REFUSED`, now `MODAL_BORDER_REFUSED`) is the most exportable thing in
  this batch: it is how a design language says *no* in code.
- **Dimming is not the only way to say "behind".** Ledger's refusal to dim is a real design position with
  a reason a reader can check: the entries above a question are not less true while it is open.
