# Increment 31 — `Kit.readout_label`: L-33 stops being an `if` in a frame

**Batch:** `kits-learn-4` · **AC-4, AC-6**
**Files:** `taskboard/language.py`, `tests/test_components.py`,
`prototypes/components/screens.py` — **3 source files**.

**The matrix reaches 30 of 30. Zero hand-drawn elements in the whole sweep.**

---

## 1. The defect

```python
if k.numbered:
    sh.row("  " + f"[{c['mut']}]{LG.mark(pad(F.RATE_LABEL, 12))}[/]" + bar)
    sh.note(Cand("the readout's label -- LABELLED, never numbered", "refused", ...))
else:
    sh.row("  " + f"[{c['mut']}]{LG.mark(pad(F.RATE_LABEL, 12))}[/]" + bar)
```

**Both branches draw the same row.** The `if` exists only to file a refusal — a language's commitment
living in a frame's control flow, which is exactly the shape `s1_blueprint` had before inc28. L-33 was
measured on a real app, quoted verbatim in LANGUAGES.md §3b, and enforced by nothing.

---

## 2. The mechanism

`Kit.readout_label(label) -> str` is **`display_label` with the binding refused**, and the difference
between the two seats *is* L-33:

```
corgi       display_label(1, "5 rate") -> "[5] RATE"      the control, numbered
            readout_label("5 rate")    ->  "RATE"         the readout, labelled
```

LANGUAGES.md §3b, verbatim: *"because the numbering IS the keymap, this language has no notation for a
passive readout. A `[5]` over a chart nobody can act on is the decorative numbering §3b defines itself
against. Readouts are LABELLED; controls are NUMBERED."*

**`READOUT_NUMBER_REFUSED` is the fourth registry of the shape, and the only one whose keys are
DERIVABLE.** It must name exactly the languages whose `numbered` token is set — a language that numbers
nothing has no numbering to refuse, and a language that numbers everything must say why this component is
exempt:

| | the commitment |
| --- | --- |
| **corgi** | the numbering IS the keymap; the right response to wanting a numbered readout is to notice |
| **ledger** | the folio numbers a **posting** — something someone made and someone else can trace. A rate meter is not posted, so a number over it is a reference to nothing |
| **industrial** | *"everything is numbered and labelled"* and the numbers are the **modes** — the same keymap corgi's are, reached from a different product. A plate over a readout promises a control that is not there |

**Industrial is the language this increment found.** The PROTOTYPE round rendered five languages and
measured the refusal in two; industrial is the third `numbered` language and it would have numbered a
readout the day anything asked it to. The derivable-keys test is what surfaced it, and it is why that
test is written as `set(registry) == set(numbered)` rather than as a literal list.

**The word is the caller's and the register is the language's**, which is `display_label`'s ruling — and
this method is deliberately its twin, because a readout's legend and a display's legend are the same
object and a contract that lettered them differently would be answering one question twice.

---

## 3. Files modified

| file | what |
| --- | --- |
| `taskboard/language.py` | `Kit.readout_label` + `READOUT_NUMBER_REFUSED` (3 entries) |
| `tests/test_components.py` | 5 new laws, 27 new tests |
| `prototypes/components/screens.py` | `legend()` is three lines with no branch; the `Cand` and the `k.numbered` `if` are gone |

---

## 4. The property test

`test_no_language_numbers_a_readout` is L-33 asked of all eleven, with a caller string that **opens with
a binding** (`"5 rate"`) — the input a numbering language would letter it from.

Beside it, the four that make the seat a mechanism: the registry's keys **equal** the numbered set (so a
new numbered kit cannot slip in unlabelled); the two seats **diverge** in the same language on the same
string (`"[5] RATE"` vs `"RATE"`); the word is the caller's and an empty label is `READOUT`; and **the
teeth** — take ledger out of the registry and it spends a key on a bar nobody can press, with the
language's own code untouched.

**And the teeth test states this table's honest limit**, which the other three do not have: it can only
be wrong in one direction. A false entry for a language that numbers nothing changes nothing, because
there was no notation there to withhold.

---

## 5. Test results

```
python -X utf8 -m pytest -q
835 passed, 2 skipped, 4 warnings in 35.09s        (inc30 left it at 808 — +27)

python -X utf8 prototypes/verify_language.py
10857 PASS · ALL PASSED                            (baseline unmoved)
```

---

## 6. The capture — the matrix closes

```
python -X utf8 prototypes/components/render.py
0 hand-drawn elements declared (0 refused, 0 evoked)     (inc30 left it at 2)
no two frames identical within a screen (60 pairs)
30 candidates files                                      — all thirty now say
                                                           "Nothing was drawn by hand"
```

```
              S1              S2              S3              S4              S5              S6
corgi     implementa      implementa      implementa      implementa      implementa      implementa
blueprint implementa      implementa      implementa      implementa      implementa      implementa
prism     implementa      implementa      implementa      implementa      implementa      implementa
naught    implementa      implementa      implementa      implementa      implementa      implementa
ledger    implementa      implementa      implementa      implementa      implementa      implementa
```

**30 of 30**, from 0 at the PROTOTYPE round and 14 at the close of `kits-learn-3`. Every refusal that used
to be a sidecar note is now an entry in a table the mechanism reads: `MODAL_BORDER_REFUSED` (4),
`PANE_SPLIT_REFUSED` (2), `READOUT_NUMBER_REFUSED` (3).

**A frame that legitimately moved, said out loud:** the S5 readout legend now reads `EVENTS/S` in all five
where it read `events/s` before. That is `display_label`'s register applied to its twin, and it is the
only text this increment changed in a frame.

---

## 7. Risks

- **The register is `display_label`'s, and `display_label`'s is not per-language.** All eleven letter a
  legend in capitals, including darkside, whose `display_cap` override is explicitly *"quiet lowercase"*.
  That tension predates this increment and is inherited rather than introduced — but a reader comparing
  `field_row`'s caption (which prism and nord pass through unchanged) with this one will find two
  registers in one contract.
- **`READOUT_NUMBER_REFUSED` can only be wrong in one direction.** Stated at the table and in the test.
- **The `numbered` branch in `readout_label` is unreachable in shipped code** — the derivable-keys test
  keeps it so. It is not dead code: it is the falsifiable path, and the teeth test is the only caller
  that ever takes it.
- **`display_label`'s known edge is inherited**: a legend that legitimately opens with a number
  (`"2 PASS"`) has that number read as a binding and dropped.

## 8. Pending

- inc32 — the six inheriting languages.
- `required` and `pane_split` for those six — spec §5.

## 9. For the skill

- **A refusal living in a caller's `if` is not a refusal, it is a coincidence.** Both branches of this one
  drew the same row; the only thing the `if` did was file a note. COMPONENTS.md should say that a
  language's "no" belongs in a table the component reads, and give the four tables as the worked pattern.
- **The strongest registry is one whose keys are derivable from a token.** This one must equal the set of
  `numbered` languages, so a language added later cannot silently number a readout — and the test that
  says so is what found the third refuser nobody had noticed.
- **L-33 has a general form worth stating: a component with no affordance may not wear an affordance's
  notation.** Corgi's numbers, ledger's folio and industrial's plates are three different products
  arriving at the same law from the same direction.
