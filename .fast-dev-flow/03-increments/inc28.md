# Increment 28 — `Kit.pane_split`: the last composition primitive, and the third refusal registry

**Batch:** `kits-learn-4` · **AC-1**
**Files:** `taskboard/language.py`, `tests/test_components.py`,
`prototypes/components/screens.py` — **3 source files**.

**S1 and S4 reach `implementa` in all five. Nine cells, one primitive.**

---

## 1. The defect, in one cell

```python
split = f"[{c['dim']}]│[/]"
for i in range(room):
    sh.row(pad(l, left) + " " + split + " " + r, C_SPLIT)
```

Five languages, one `│`. It is the same shape as the red `!` inc14 removed and the borrowed dot leader
inc15 removed — **the terminal's own convention generalised into four languages that never chose it** —
and it is the one COMPONENTS.md warns about by name: *composition is the last palette-swap.*

Blueprint could not even be drawn that way, so the file carried a whole per-language builder
(`s1_blueprint`) whose entire body was a `str.replace` putting the `│` back to a space. **A frame
correcting a kit is the defect wearing a fix.**

---

## 2. The mechanism

`Kit.pane_split(h, w=3) -> list[str]` — `h` rows of **exactly** `w` cells. The width is a **seat**, not a
suggestion: the panes sit either side of it on every line, so a row that came back short would move the
right pane down the page.

**Three methods, and the split is deliberate:**

| method | who overrides it | why |
| --- | --- | --- |
| `pane_split` | **nobody** | it consults `PANE_SPLIT_REFUSED` before anything else |
| `pane_split_rule` | languages that draw | `PANE_RULE` is the whole decision for most of them |
| `pane_split_instead` | languages that refuse | what they do when they may not rule a stroke |

The first version of this seat had corgi, naught and ledger overriding **`pane_split` itself**, and it
was wrong for a reason the registry's own teeth test found in one run: *a language that overrides the
entry point never consults the table*, so a false entry against it would go undetected and the table
would be a comment with a dict around it. That is `overlay`'s shape (nobody overrides `overlay`; four
languages override `overlay_instead`), reached the hard way.

**Six seats, six answers**, same `(h=4, w=3)`:

```
nord/base    │  │  │  │       the terminal's own hairline, air each side
corgi        █  █  █  █       the DISPLAY FRAME — "framed by SOLID BARS" (§3b)
naught       ◦  ◦  ◦  ◦       the lattice, one charge down — the GROUND, not a frame
ledger      ═══ │  │  │       a ruled money column, OPENED at its head rule
prism       (a grey step of background, three cells wide)
blueprint   ┤ ├                two datums that never join, then air
```

- **corgi** — LANGUAGES.md §3b verbatim: *"a display REGION, visually separate from the chrome … framed
  by SOLID BARS. Everything inside it is machine output; everything outside is a label."* Two panes are
  exactly that boundary. **And it does not contradict `SLOT_GAP`**, whose comment says a rule glyph
  between slots "would be `Ledger.RULE_V`" — that is true *inside* one panel, where this language
  separates by air. This is the display's **edge**, and an edge is a bar.
- **naught** — *"no frames at all"* forbids a rule and does not forbid this: the lattice is not a frame,
  it is the **ground**, and it was under both panes before either was drawn. Same argument operator
  ruling 4 accepted for its overlay, where the separation is **charge**.
- **ledger** — *"structure is RULED MONEY COLUMNS, never boxes"*, so this language does own the stroke
  the other four spend differently. What separates its `│` from the terminal's is **row 0**: `cols_frame`
  opens a column at the head rule and rules **down** from it, and a column rule starting in mid-air would
  be a stroke this page never posted. Nord rules because a terminal rules; ledger rules because the
  column was *opened*.
- **prism** — in the registry on a **doctrinal** refusal: *"depth by ±1 grey step of background, never
  borders"*, with the one exception its doctrine names (*"borders are RESERVED for modals"*) — a licence
  for the modal and a prohibition everywhere else. It draws what `recede` draws: `depth_ground()`.
- **blueprint** — in the registry on an **alphabetic** refusal: none of its ten marks is a vertical
  stroke. What a drawing office does with two views on one sheet is give each its own **datum**, so the
  left field terminates (`┤`) and the right field opens (`├`), **once**, and the rest is air. They never
  join, which is the registration pair's own law. One row of declaration and `h-1` of nothing is a
  *dimension*: it states an extent and stops.

**The two refusals are not the same refusal**, which is why a registry and not a flag: blueprint's mark
does not exist, prism's exists and is forbidden. A language can leave one and not the other.

---

## 3. Files modified

| file | what |
| --- | --- |
| `taskboard/language.py` | `_split_cell` + `pane_split` / `pane_split_rule` / `pane_split_instead` at the base; `PANE_SPLIT_REFUSED`; `PANE_RULE` on naught and corgi; `pane_split_rule` on ledger; `pane_split_instead` on prism and blueprint |
| `tests/test_components.py` | 7 new laws, 19 new tests |
| `prototypes/components/screens.py` | S1's divider through the kit; `C_SPLIT` and the whole `s1_blueprint` builder deleted; `BUILDERS["S1"]` is empty |

`s1_blueprint` is the **fifth per-language builder this sweep has deleted**, and like the four before it,
its body was a language's mechanism living in the frame.

---

## 4. The property test

`test_five_languages_split_five_ways` — same height, same width, five splits that differ **as cells**,
compared on the plain text (two splits differing only in a colour token are two recolours).

Beside it: every language returns exactly `h` rows of exactly `w` cells including the two that refuse
(a refusal is **air at the same width**, never a missing row); neither refuser emits any of
`│┃║╎╏┆┇┊┋|`; ledger's row 0 is `RULE_HEAD` and nord's is not; blueprint's row 0 is `┤ ├` and every row
after it is air; the registry names only real languages with reasons over 40 characters; and **the teeth,
both ways** — delete blueprint's entry and it rules a stroke its alphabet cannot construct, add a false
entry for naught and the language whose answer *is* the lattice loses it, with neither language's code
touched.

---

## 5. Test results

```
python -X utf8 -m pytest -q
711 passed, 2 skipped, 4 warnings in 35.43s        (inc27 left it at 692 + 1 env — +19)

python -X utf8 prototypes/verify_language.py
10857 PASS · ALL PASSED                            (baseline 10857, unmoved)
prototypes/out/ clean afterwards                   (F-17 stays closed)
```

The env-dependent `test_win_clipboard_roundtrip` passed on this run; it is the documented flake
(PENDING #22) and its state is not this increment's.

---

## 6. The capture (AC-1, AC-6)

```
python -X utf8 prototypes/components/render.py
17 hand-drawn elements declared (2 refused, 15 evoked)      (inc19 left it at 26)
no two frames identical within a screen (60 pairs)          — the closure law, on every frame
```

**Nine elements gone**: `pane_split` ×5 on S1 and ×4 on S4 (corgi's S4 was already clean because its
mode takes the screen and there is no backdrop to carry). The matrix:

```
              S1              S2              S3              S4              S5              S6
corgi     implementa      evoca 3E      implementa      implementa    rehusa 1R/0E    implementa
blueprint implementa      evoca 3E      implementa      implementa      implementa    implementa
prism     implementa      evoca 3E      implementa      implementa      implementa    implementa
naught    implementa      evoca 3E      implementa      implementa      implementa    implementa
ledger    implementa      evoca 3E      implementa      implementa    rehusa 1R/0E    implementa
```

**23 of 30**, from 14. Blueprint's S1 and S4 moved from `rehúsa` to `implementa` **without the language
changing its mind** — the refusal moved from a sidecar into a table the mechanism reads, which is the
whole difference between a design answer and a note about one.

Measured in the frames: `blueprint_S1.txt` row 2 carries `┤ ├` immediately left of `DETAIL` and nothing
below it; `prism_S1.svg` carries 27 `<rect … fill="#1f2630"/>` at `x=514` — a three-cell column of
`depth_ground()` — and `prism_S1.txt` carries three spaces there.

---

## 7. Risks

- **Prism's split does not survive the `.txt`.** A background is not a cell. That is the third mark in
  this contract with the limit, after blueprint's knockout and every language's match emphasis, and the
  house convention says the `.txt` is the work. It *does* survive greyscale, which is the law that
  actually applies to it.
- **Ledger's rule and nord's rule are the same glyph.** They differ at row 0 and in nothing else, so a
  reader who crops the head sees two languages agreeing. Declared rather than designed around: the
  alternative was giving ledger a stroke it does not own.
- **Five languages inherit the base `│`** — instrument, swiss, industrial, darkside, solari. Two of them
  (swiss: *"no boxes — alignment does the dividing"*; darkside: *"never borders"*) have the commitment
  that puts them in `PANE_SPLIT_REFUSED`, and the registry's comment says so. Out of scope by spec §5,
  recorded as this batch's own inheritance debt.
- **`w` defaults to 3 and every caller passes 3.** A language wanting a two-cell seat has the parameter
  and no caller exercising it.

## 8. Pending

- `Kit.error`, `Kit.required`, `Kit.textarea` (S2's three) and `Kit.readout_label` (S5's) — inc29..inc31.
- `pane_split` and `required` for the six inheriting languages — spec §5.

## 9. For the skill

- **Composition is the last palette-swap, and this is the worked example.** A divider is the only
  primitive that draws a *relation* rather than a thing, and it was the last one five languages agreed on.
- **A refusal registry must be consulted by a method no language overrides.** Otherwise the override
  silently opts out of the table and the table decides nothing for exactly the languages that care most.
  It cost one run of the teeth test to find and it is worth stating in COMPONENTS.md as a rule of the
  pattern, not a detail of this seat.
- **Two refusals of the same component can have different kinds.** Alphabetic ("the mark does not exist
  in this language") and doctrinal ("the mark exists and I have forbidden it"). A registry keyed by
  language carries both; a boolean flag on the component carries neither.
