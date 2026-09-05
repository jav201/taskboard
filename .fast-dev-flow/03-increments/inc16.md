# Increment 16 — `Kit.select` / `Kit.menu`, and severity as a SHAPE on a control

**Batch:** `kits-learn-3` · **AC-3** · operator rulings 7 and 6 of 2026-09-04
**Files:** `taskboard/language.py`, `tests/test_components.py`, `prototypes/components/screens.py` —
**3 source files**.

**S3 is the first screen to reach `implementa` in all five languages.** `0 candidates` on every one of
`corgi_S3`, `blueprint_S3`, `prism_S3`, `naught_S3`, `ledger_S3`.

---

## 1. Two defects, one screen

**The select was drawn as a stepper**, because the stepper was the nearest thing the contract had. They
answer different questions, and drawing one as the other is a lie about the keyboard: a stepper shows
**the two ways OFF a value** — its steps are the ± of a set you move through in place; a select shows
**the one way INTO a list**, and its disclosure is a door. A user who sees a stepper reaches for the arrow
keys expecting the setting to change. In a select they do not change it; they open it.

**The destructive button had no severity channel at all** — the contract had never had one — so the
prototype announced it with a hand-drawn red word `DANGER` above an ordinary button. And the hue was
unavailable before it was even considered: ledger spends `alert` on literal debt, blueprint on overdue.
Ledger's frame therefore **refused** the control outright.

---

## 2. The mechanism

### `select` — a field you do not type into

`Kit.select(options, selected, w=0, state=DEFAULT) -> str`. The ground is the **text field's**, and that
is an anatomy argument rather than a shortcut: a select holds one value, it has walls, it takes the
control states — everything a text field is **except the caret**. So it borrows `field_form()` and the
parts registry grows nothing, which is this contract's rule for a shape that is an existing anatomy in a
new job.

What is new is one declared mark per language, `DISCLOSE`:

```
nord/base ▾   naught ◍   corgi ▄   prism ⣶   ledger ┊   blueprint ╌
```

`◍` is a dot with more charge behind it; `▄` the bank below the segment; `⣶` the field continuing; `┊` the
column carrying on below; `╌` the break line — the view continues off-sheet. Six answers to "there is more
here", each already in its own alphabet.

The word is content and the field is reserved for the **widest option in the set** (Bodmer T2), so
choosing another option cannot move the control's edges. The index is the **group's**: `select` reaches
`group_states` exactly as `stepper` and `radio_group` do, so an out-of-range index **raises** in one seat
for three mechanisms.

### `menu` — a list, not a surface

`Kit.menu(options, selected, w=0, state=DEFAULT) -> list[str]`. **A menu is not a modal**, which is the
decision that keeps this method out of the overlay argument entirely: no language draws a frame here,
including the one whose commitment licenses a border — prism's borders are reserved for *modals*, and a
dropdown is not one. What separates the open list from the page is what separates any selected row from
its neighbours: the language's own cursor and tones. Rows, not a joined string, because the caller places
them.

### `danger=True` — severity by shape, and no hue at all

`Kit.button(label, w=0, state=DEFAULT, danger=False)`, with one declared pair per language,
`DANGER_FORM`, bracketing the label **inside the walls**:

```
nord/base  [   !Delete!   ]      the terminal's own shout
naught     ◦   ∙Delete∙   ◦      two lit dots — and not the one red
corgi      ▁▁  ▄Delete▄  ▁▁      the key's shoulders swollen, engraved
prism      ⣿⣀  ⣿Delete⣿  ⣀⣿      nothing left to burn
ledger     │   (Delete)   │      THE CONTRA ENTRY
blueprint  ├   ━Delete━   ┤      the heavy weight, this alphabet's loudest mark
```

**Ledger's is the ruling made visible.** A ledger writes a reversing figure **in parentheses** — the
notation its own genre has used for centuries for an amount that takes something away. So the destructive
control is neither refused nor tinted: it wears the form the genre already has for undoing a posting. The
prototype's refusal is **retracted**, `s3_ledger` is deleted, and ledger's settings screen now renders the
generic danger zone in its own hand.

**No colour moves.** Not "hue plus a glyph" — *no hue*, which is stronger than the law requires and is the
only version that survives contact with a language whose alert is already spent. A test asserts the tone
tokens of an ordinary and a dangerous button are byte-identical.

---

## 3. Files modified

| file | what |
| --- | --- |
| `taskboard/language.py` | `DISCLOSE` and `DANGER_FORM` declared at the base and in 5 languages; `select` and `menu` added; `button` grows `danger` |
| `tests/test_components.py` | 11 new laws, 101 new tests |
| `prototypes/components/screens.py` | S3's selects, menu, danger zone through the kit; `C_SELECT`, `C_MENU`, `C_DANGER` and `s3_ledger` deleted |

---

## 4. The property test, and what it caught

`test_a_select_is_not_a_stepper` (all eleven) and `test_danger_survives_greyscale_in_every_language` (all
eleven, plain, against the **ordinary button of the same label and width** — "it differs from a checkbox"
would prove nothing).

Around them: the edges do not move when the choice does; the chosen word comes back byte for byte; an
out-of-range index raises; a menu is one row per option with exactly one marked; the label survives
`danger=True` byte for byte; the five danger forms are five (a `!` in five languages is the same defect as
a red `!` in five languages); and ledger's is `(Delete)`.

**One test was wrong and the code was right.** `test_a_menu_is_a_list_and_not_a_surface` first asserted
that no menu row contains a **corner glyph**, and blueprint went red: blueprint's cursor **is** a
registration corner (`┌`), because four corners that never join is that language's whole selection
mechanism. A corner is not a box. The law was restated on what actually makes a box — **a lid** (a run of
rule) **or a wall** (a vertical stroke) — which is the thing four of these eleven languages have a
commitment against. The finding is worth more than the test: *an oracle written from the shape of the
common case will flag the language that had the most specific answer.*

---

## 5. Test results

```
python -X utf8 -m pytest -q
525 passed, 2 skipped, 4 warnings in 34.04s        (inc15 left it at 424 — +101)
```

```
python prototypes/capture_languages.py --surface    # plain and alone (F-8)
11 surfaces ; no two identical (55 pairs) ; moved vs baseline-kits2: the same four as inc14
```

`verify_language.py` not re-run: no state axis and no glyph table changed (spec §4).

---

## 6. The capture (AC-7)

```
python -X utf8 prototypes/components/render.py
53 hand-drawn elements declared (8 refused, 45 evoked)     (inc15 left it at 68 — 9 refused)

corgi_S3      0 candidates      blueprint_S3  0 candidates      prism_S3   0 candidates
naught_S3     0 candidates      ledger_S3     0 candidates
```

**Fifteen elements gone and one refusal retracted.** `select` ×5, `menu` ×5 and `danger` ×5 leave the
sidecars; ledger's S3 refusal is not "resolved", it is **withdrawn by ruling**, which is a different thing
and is why the frame changed rather than the count alone.

---

## 7. Risks

- **`DANGER_FORM` widens the control by two cells.** `w` is a minimum for the *bracketed* word, so a row
  of buttons where only one is dangerous will not align on its walls. Visible in `ledger_S3`, accepted:
  the alternative is eating the label's own cells, which would truncate content to make room for
  notation.
- **Five languages inherit the base's `!`** (instrument, swiss, industrial, darkside, solari) — the same
  bounded gap `field_row` has, and the same pending item.
- **`select` borrows the field's ground**, so a language that later gives its text field a mechanism the
  select should not have inherits it silently. The anatomy argument is written at the seat; the coupling
  is real.
- **Ledger's parentheses are ASCII**, so a caller whose label already ends in `)` gets `((x))`-shaped
  output. Not defended against: the label is content and the kit does not edit it.

## 8. Pending

- Per-language `menu` rows. Today the mechanism is the cursor and the tones, both already the language's,
  but no language *chose* its open-list treatment.
- Five languages' own `DISCLOSE` / `DANGER_FORM`.
- `Kit.select`'s **invalid** state: a required select left unset is exactly the case §6.2 of the spec
  excluded (no interior → no `INVALID`). A select has a value and no interior, so it sits precisely on the
  line the operator may want moved.

## 9. For the skill

- **`COMPONENTS.md` should carry the sentence, not the widget**: *a stepper shows the two ways off a
  value; a select shows the one way into a list.* That is the distinction the census is missing, and it is
  what makes the two controls impossible to confuse.
- **Severity on a control belongs in the state matrix as a FORM, not a hue** — with ledger's contra
  parentheses as the worked example, because it is the case that proves the rule: the language whose genre
  refused the control outright had the oldest notation for it.
- **A menu is a list, not a surface.** The frame question belongs to the overlay; keeping it out of the
  dropdown is what lets four languages with no boxes have a working select at all.
