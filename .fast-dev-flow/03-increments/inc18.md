# Increment 18 — `Kit.log_row`: the level is a glyph ladder, not a hue

**Batch:** `kits-learn-3` · **AC-5** · operator ruling 8 of 2026-09-04
**Files:** `taskboard/language.py`, `tests/test_components.py`, `prototypes/components/screens.py` —
**3 source files**.

---

## 1. The defect

`ICONS` carries six **domain** kinds — deadline, overdue, wip, blocked, done, held — and no log level. So
when the PROTOTYPE round drew a monitor screen, all five languages marked ERROR with the same `!!` in the
same alert hue, for the same reason as the invalid field and the danger button: there was nothing
per-language to mark it with, so the frame invented one mark for everybody.

---

## 2. The mechanism

`Kit.log_row(level, time, message, tail=False) -> str` — **a full row contract**, exactly the arguments the
ruling names, and not an `ICONS` entry. The three fields are not independent: the level decides the weight
the message is set in, the time is the only thing in the row that is not the message's, and a level mark
drawn *beside* a row the caller composed would be a mark with no column to sit in.

**`LEVELS` is a glyph ladder** — three shapes of one width per language, so a greyscale eye sorts the rows
and a column of them still aligns:

```
nord/base   ·   !   !!      the terminal's own escalation
naught      ◦◦  ∙◦  ∙∙      how many dots are lit — the only channel it has
corgi       ▁▁  ▄▄  ██      the segment bank's height, which is how the hardware says how much
prism       ⣀⣀  ⣤⣤  ⣿⣿      the ember ramp: how much of the cell has caught
ledger      ␣␣  †␣  ‡␣      THE MARGIN DAGGER
blueprint   ··  ╌╌  ━━      the drawing's own weights: leader, break, heavy
```

**Ledger's is the one to read twice.** An unremarkable posting carries **no mark at all**; a queried one is
daggered and a disputed one double-daggered — the notation this genre has used for exceptions since before
screens. It is the same family as its `INVALID` mark from inc14, and that is not a coincidence: a ledger
annotates, it does not restyle.

**The hue ladder is neutral — dim, mut, ink — and that is a decision with a cost.** Two commitments here
must not break: ledger spends `alert` on literal debt, blueprint on overdue and nothing else ("a calm sheet
carries zero alert"). A log that reached for red on every ERROR would spend the one mark those languages
guard, on the noisiest row on the screen. So severity is **shape plus neutral weight**, in all eleven, and
a caller with its own palette can still tone the message it passes in.

**`tail=True` is the live edge**, drawn with the language's own `DISCLOSE` — the same declaration the
select spends, because it is the same sentence: *there is more*. A select points at a list; a log points at
the line that has not arrived yet. One declaration, two seats.

---

## 3. Files modified

| file | what |
| --- | --- |
| `taskboard/language.py` | `LEVELS` at the base and in 5 languages; `Kit.log_row` |
| `tests/test_components.py` | 6 new laws, 56 new tests |
| `prototypes/components/screens.py` | S5's eight log rows and its tail marker through the kit; `C_LOGROW`, `C_TAIL` and the module-level `LEVEL_MARK` deleted |

---

## 4. The property test, and the second oracle it corrected

`test_the_log_level_reads_with_the_colour_removed` — three levels, three **plain** rows, all eleven
languages. Beside it: one width per ladder (a ladder whose rungs differ moves the message under itself, one
row in three); time and message back byte for byte, including `GET /a[b] 500 in 12ms` (the bracket is the
pitfall-A1 probe); the tail mark present on the tail row and on no other; and five ladders for five
languages.

**`test_a_log_row_spends_no_rationed_hue` had to be restated, and the restatement is a finding.** It first
banned the `warn` and `alert` tokens by value, and blueprint went red on an **info** row: blueprint's
`warn` token **is** its `mut` token — `#7fa8c4` in both. A test that bans a hue by value bans a *neutral*
in the language that decided the two are the same colour, and passes vacuously everywhere else. The law is
now a **whitelist**: the row may spend the neutral family (ink, mut, dim) plus the accent on the live edge,
and nothing else.

That is the third oracle in this batch corrected by the language with the most specific answer (inc16's
menu corners, inc17's box lid, and now this).

---

## 5. Test results

```
python -X utf8 -m pytest -q
614 passed, 2 skipped, 4 warnings in 30.07s          (inc17 left it at 558 — +56)

python prototypes/capture_languages.py --surface     # plain and alone (F-8)
11 surfaces ; no two identical ; moved vs baseline-kits2: the same four as inc14
```

`verify_language.py` not re-run: no state axis, no glyph table, no existing render path changed (spec §4).

---

## 6. The capture (AC-7)

```
python -X utf8 prototypes/components/render.py
36 hand-drawn elements declared (4 refused, 32 evoked)      (inc17 left it at 46)

blueprint_S5  0 candidates      prism_S5  0 candidates      naught_S5  0 candidates
corgi_S5      1 (readout_label, refused)                    ledger_S5  1 (readout_label, refused)
```

Ten elements gone: `log_row` ×5 and `tail` ×5. **Three S5 cells reach `implementa`.** The two that do not
are corgi's and ledger's, and both hold the same declared refusal — **L-33**: *the numbering IS the keymap,
so a readout is LABELLED and never numbered*. Named in spec §6.3 before the batch began; it is a
primitive (`readout_label`) the ten rulings did not cover, not a gap this increment left.

---

## 7. Risks

- **The neutral ladder may be the wrong call for a monitor.** An ERROR row that does not glow is harder to
  find at a glance, and the two languages the rule protects are two of eleven. The trade is stated here
  rather than hidden: a per-language "may I spend alert" declaration would let nine languages glow and two
  abstain, and that is a registry this batch did not add. **A question for the operator.**
- **Ledger's info mark is two spaces.** It is the honest answer (an unremarkable posting is unmarked), and
  it means ledger's log is the only one where the level column is invisible until something is wrong.
  Intentional; worth seeing in a frame before it is called good.
- **`log_row` takes no width and pads nothing**, so a caller with a fixed column has to pad the message
  itself. Deliberate — the row's fields are all content and the contract has no opinion about the column
  they sit in — but it is a difference from `field_row`, which does take `w`.
- **The tail borrows `DISCLOSE`.** One mark, two meanings ("open this list" / "the stream continues"). The
  unification is argued in §2 and it saved six declarations; if the operator wants a distinct tail mark,
  that is a `TAIL` token per language and nothing else changes.

## 8. Pending

- `readout_label` (corgi's and ledger's L-33 refusal) — the last thing between two S5 cells and
  `implementa`, and it belongs in a registry beside `MODAL_BORDER_REFUSED`.
- Five languages inherit the base ladder (`· ! !!`).
- The paused/live footer row is still the caller's words, and `spinner(2)` is a frozen frame in a static
  capture — the motion contract's own caveat, unchanged by this increment.

## 9. For the skill

- **`COMPONENTS.md` needs a log row**, and the six ladders are the exhibit: the level is a *shape*, and the
  five mechanisms are lit dots, segment height, an ember ramp, a margin dagger and a drawing's line
  weights. None of them is a red `!`.
- **"Never colour alone" has a stronger sibling worth naming: "not this colour at all."** When a language
  has rationed a hue by commitment, the component that wants it must find another channel — and the
  neutral weight ladder is the one every terminal has.
- **A test that bans a hue by value is a bug in the test.** Two tokens in one palette can be the same
  colour on purpose; whitelist what a component may spend instead.
