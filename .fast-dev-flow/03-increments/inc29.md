# Increment 29 — `Kit.error` and `Kit.required`: the rejection has a notation, the obligation has a mark

**Batch:** `kits-learn-4` · **AC-2**
**Files:** `taskboard/language.py`, `tests/test_components.py`,
`prototypes/components/screens.py` — **3 source files**.

---

## 1. The defect

Two lines in `screens.py`, and both are the same failure inc14 already paid for once:

```python
req = f"[{c['alert']}]{LG.mark('*')}[/]"
sh.row(" " * (lab + 2) + f"[{c['alert']}]{LG.mark(F.FORM_DUE_ERROR)}[/]", C_ERROR)
```

A bare `*` in the alert hue and a message in the alert hue, in five languages at once. `C_REQUIRED`'s own
commitment said so before this batch started — *"it may NOT be a bare `*` in five languages, which is the
palette-swap failure at one glyph"* — and `C_ERROR`'s named the three notations that were missing:
*"ledger's leaders, corgi's segment legend, blueprint's revision note."*

**And it spends a rationed hue twice.** Ledger's alert is literal debt; blueprint's is overdue and nothing
else (*"a calm sheet carries zero alert"*). Both of those commitments are already guarded in `log_row`,
and this row walked straight through them.

---

## 2. The mechanism

### `Kit.error(msg, w) -> str`

**The mark is the language's own `LEVELS` ladder, not a new table.** That is the whole design decision.
`LEVELS` already carries three shapes of one width per language, already survives the colour being taken
away (operator ruling 8), and already says ERROR in this language's alphabet. A second severity table
beside it would be two answers to one question — and an inline validation failure and a log line at ERROR
are *the same claim about the same severity*, made about a field instead of about an event.

**The message is CONTENT** — byte for byte, never recased, never cut, at any `w`. `w` is `field_row`'s
minimum, and the one string in a form that must not be trimmed to fit is the one that says what is wrong.

**Two small constants carry the rest**, each doing one thing:

| | what it is | who moves it |
| --- | --- | --- |
| `ERROR_FILL` | the remainder of the line, after the words | naught `◦` · ledger `·` · blueprint `╌` |
| `ERROR_TONE` | which tier the mark is set in | ledger `ink` · blueprint `ink` |

`ERROR_TONE` exists because inc18's answer — take the hue away from all eleven — is right for a *stream*
of rows and too much for one row that is the whole point of the screen. So the tier is a per-language
decision, which is what it actually is: nine languages shout, the two that ration do not.

```
corgi       ██ expected YYYY-MM-DD                       the bank fully lit, then bare panel
naught      ∙∙ expected YYYY-MM-DD ◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦   two lit dots over the unlit ground
ledger      ‡  expected YYYY-MM-DD ·····················  a footnote, ruled out to the margin
prism       ⣿⣿ expected YYYY-MM-DD                       the ember at full strength; airy
blueprint   ━━ expected YYYY-MM-DD ╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌   a REVISION NOTE on a dashed extension
```

### `Kit.required() -> str`

One cell — so a caption's column does not move when a field becomes obligatory — in the **ink** tier: a
required field is a *property* of the field, not an alarm about it, so it sits one weight step above the
`mut` caption beside it (HIERARCHY.md's dim/normal/bright ladder) and spends no rationed hue.

```
nord    *    the terminal's own convention, and the base kit is the terminal
corgi   ▀    the UPPER bank lit — `DISCLOSE` is the bank BELOW; two banks, two meanings
naught  ∙    a dot at full charge: the seat must carry a value
ledger  †    footnote ORDER: `†` must be made, `‡` was refused — and `‡` is the wall
             its invalid field is daggered with, so row and field make one claim
prism   ⡀    the ember's leading cell — a field the value has not reached yet
blueprint ├  an OPENING TERMINATOR: an unfigured dimension is a REFERENCE, a figured
             one is required. `━` was the other candidate and is spent twice already
```

**None of them is a digit**, in any of the eleven. L-33 again, on the mark most likely to reach for one.

---

## 3. Files modified

| file | what |
| --- | --- |
| `taskboard/language.py` | `ERROR_FILL` / `ERROR_TONE` / `error()` and `REQUIRED` / `required()` at the base; 5 fills, 2 tones, 5 marks |
| `tests/test_components.py` | 9 new laws, 40 new tests |
| `prototypes/components/screens.py` | S2's message row and required marker through the kit; `C_ERROR` and `C_REQUIRED` deleted |

---

## 4. The property test

`test_five_languages_explain_a_rejection_five_ways` — same message, same width, five rows that differ as
cells, compared on the plain text.

Beside it: the message comes back byte for byte at `w = 8`, `44` and `200` and with
`"Q3 -1,204.55 [ref] AbCd"` in it (the `mark()` escaping pitfall, A1); every row **starts with** the
language's own `LEVELS["error"]`, and that rung differs from its other two, which is "survives greyscale"
asserted rather than promised; **ledger and blueprint spend no `alert`** on either the row or the marker;
the marker is exactly one cell in all eleven; it is not `*` in any of the five and the five are distinct;
**no language numbers it**; and ledger's two daggers are an *order*, checked across three seats —
`required()`, `LEVELS["error"]` and `field_form(INVALID)`.

---

## 5. Test results

```
python -X utf8 -m pytest -q
751 passed, 2 skipped, 4 warnings in 36.31s        (inc28 left it at 711 — +40)

python -X utf8 prototypes/verify_language.py
10857 PASS · ALL PASSED                            (baseline unmoved)
```

---

## 6. The capture

```
python -X utf8 prototypes/components/render.py
7 hand-drawn elements declared (2 refused, 5 evoked)     (inc28 left it at 17)
no two frames identical within a screen (60 pairs)
```

**Ten elements gone**: `Kit.error` ×5 and `Kit.required()` ×5. S2 is down to one candidate per language
(`Kit.textarea`), and the matrix is at **23 of 30** with S2 at `evoca 1E` in all five.

---

## 7. Risks

- **A validation message no longer reads red in ledger or blueprint.** That is the ration being honoured
  and it is a real legibility trade: those two rows are carried by shape alone. Both languages' error
  rungs (`‡`, `━━`) are the widest-contrast marks they own, which is why the trade is affordable — but it
  is a trade, not a free win.
- **`ERROR_FILL` runs to `w` and `w` is the caller's.** A caller passing a large `w` gets a long run of
  leaders. `field_row` has the same property and the same reason.
- **The six inheriting languages get `!!` and `*`.** `LEVELS` moves for them in inc32, which moves `error`
  with it; `required` does not, and is spec §5's declared debt.
- **`error` reads `LEVELS["error"]` and nothing enforces that the ladder stays three rungs.** A language
  that dropped the key would raise; a language that made ERROR equal WARN would pass `error`'s own tests
  and fail the greyscale one, which is where it should fail.

## 8. Pending

- `Kit.textarea` (inc30) and `Kit.readout_label` (inc31).
- `required` for the six inheriting languages — spec §5.

## 9. For the skill

- **A component's severity mark should be READ OFF the language's existing ladder, never declared twice.**
  An inline error and a log line at ERROR are one claim in two places. COMPONENTS.md should say so at the
  form row, because writing a second table there is the obvious move and it is the wrong one.
- **"Never colour alone" has a second half nobody states: some languages cannot spend the colour at all.**
  A rationed accent is a commitment, so the tier is a per-language decision and not a contract-wide one —
  and a contract that hardcodes `alert` on its error row silently breaks every language that rations it.
- **A required marker is a property, not an alarm.** One cell, one weight step above the caption, no
  rationed hue, and never a digit in a language whose numbers are its keymap.
