# Increment 33 — `export_to_skill.py`'s own header said "ten" over eleven kits

**Batch:** `kits-learn-4` · not an AC — a docs/skill-maintenance fix found while folding this batch
into the `tui-design` skill.
**Files:** `prototypes/export_to_skill.py` — **1 source file**.

---

## 1. The defect

`HEADER` (the generated `assets/languages.py`'s own docstring) opened with a literal:

```python
HEADER = '''r"""languages.py -- the ten visual languages, AS IMPLEMENTED.
```

`TH.ORDER` has carried **eleven** kits since Ledger shipped (`kits-learn-3`); the exporter's own
`build()` already interpolates `n=len(langs)` for the closing "Generated ... from {n} kits" line, so
the count existed as data one function away and the opening line typed it anyway. The same literal
also appeared twice more inside `HEADER`'s body ("the ten in the order the app's `t` key cycles
them", "Reference frames for all ten live in..."). This is the exact drift class the file's own
docstring names as its reason to exist ("the app rendered ten languages, the skill listed eight")
committed a second time, one level up, by the generator meant to prevent it.

## 2. The fix

Derived, not typed. `_spell(n)` maps `len(langs)` to a small-number word (`_NUM_WORDS`, 0-15) and
`build()` passes `n_word=_spell(len(langs))` into `HEADER.format(...)`; the three literal "ten"s in
`HEADER` became `{n_word}`. The historical narrative sentence in the file's OWN top docstring
("it listed eight languages where the app rendered ten") was left untouched — that describes a past
event at a specific past count, not the generator's current claim, and making it derived would
misstate history instead of fixing drift.

## 3. Re-run

```
$ PYTHONIOENCODING=utf-8 python prototypes/export_to_skill.py "C:/Users/jjgh8/.claude/skills/tui-design"
  wrote C:\Users\jjgh8\.claude\skills\tui-design\assets\languages.py (22 KB, 11 languages)
  verified: 11 languages, every token, doc and family round-trips
  captures: 0 written, 66 already identical -> C:\Users\jjgh8\.claude\skills\tui-design\assets\languages
  wrote SURFACES.md (11 postures)
```

`assets/languages.py`'s header now reads `"""languages.py -- the eleven visual languages, AS
IMPLEMENTED.` and the two other counts in its body ("the eleven in the order...", "all eleven live
in...") derive the same way. The round-trip assertions in `main()` (`ORDER`, `LANGUAGES`, `DOC`,
`FAMILY` per kit) all passed, so the fix did not touch anything the exporter already checks — only
the count it did not check.

## 4. Files modified

| file | what |
| --- | --- |
| `prototypes/export_to_skill.py` | `_NUM_WORDS` + `_spell()`; `HEADER`'s three literal "ten"s replaced with `{n_word}`; `build()` passes `n_word=_spell(len(langs))` |

## 5. Risks

- **`_spell()` falls back to the digit string past 15.** Fine for this file (eleven kits, and the
  skill is not adding four more before this gets noticed), but a future language count above 15
  would silently switch from a word to a digit mid-prose. Cheap to extend if it ever matters.

## 6. For the skill

- **A generator that interpolates a count in one place and types it in another is the drift it
  exists to prevent, one level up.** `n` was already threaded through `build()`; the bug was that
  `HEADER`'s own opening line was written before `n` existed as a parameter and nobody re-checked it
  when the eleventh language shipped.
