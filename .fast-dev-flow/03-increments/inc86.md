# inc86 — the exemption an eye grants, the Limit a language keeps, and the programme's rulings in one table

Batch `rework-8c`, increment 2 of 2.

## §0 — the rulings, verbatim

Rulings (orchestrator, 2026-09-07, on the operator's delegation):

- **swiss `•`:** the floor stays at 15 %; swiss's obligation mark is exempt by name (`SEEN_BY_EYE`)
  with round five's eye-read as the evidence and the human session as the review that can revoke it.
  Neither the floor nor the mark moves.
- **Q1 over K6 for marks:** Q1 governs meaning marks (runs of 1–4 cells carrying an A-family role);
  K6 governs text runs. Where a meaning mark is painted in `mut` or `dim` and fails Q1's effective
  contrast at its declared seat, the mark takes `ink` at that seat (inc74's `log_row` precedent),
  never a token move. Decorative seats (Q2's ≥ 8 structure and the named 5–7 table) are untouched.
- **L12:** a hue-only match channel that falls under 3:1 in grey is a Limit of that language, recorded
  in the kit docstring and in `spec.md`, not fixed.

This increment is the **first** and **third**. The second was inc85.

## §1 — cause

Two of the three questions `rework-8` handed back are not defects and cannot be fixed. They are
**dispositions**: a mark that misses a floor and is visible anyway, and a channel a language cannot
widen without becoming a different language. The repo had no shape for either.

**swiss `•`.** inc82 measured it at 14.0 % coverage — one point under Q1's 15 % clause — and wrote the
disagreement down: the round that SET the clause recorded the same mark as visible on the raster
(§2.2 `swiss_S2`) and found `naught ◦` at 13.5 % by eye in §7 of the same document. inc82 refused to
lower the floor and refused to change the mark, on `rework-7c`'s principle, and named it in
`OBLIGATION_UNDER_THE_FLOOR`. **That is a measurement, not an exemption**: nothing in the repo said the
row was ALLOWED, only that it existed.

**L12.** inc84's greyscale capture found round five *right in shape and wrong in degree* — the hue-only
match keeps a luminance step of 1.34 to 2.34, thin rather than absent, and **all four kits are under
3:1**. inc84 said in writing that L12 was *"amended by this table and not closed by it — a step nobody
chose is not a channel a language may claim, and no ruling has said which of the two readings the
corpus is held to."* The ruling is now made, and it is the third reading: **neither claim nor defect —
a Limit.**

## §2 — mechanism

### `SEEN_BY_EYE` — the first exemption granted by a reading

**An instrument re-derives its own numbers every run; an eye cannot.** That one sentence decides the
whole shape. A number in a roster can be checked against the corpus on every run and will go stale
loudly. A READING cannot be re-run, so the roster has to carry the things a re-run would otherwise
supply: who saw it, where they wrote it down, and who can take it back.

```
SEEN_BY_EYE[(kit, family, cell, tone)] = (clause, evidence, review)
```

- **`clause`** — the clause the mark misses, with its measurement, and **only that clause**. A mark
  that starts missing a SECOND clause is a different mark and the exemption does not travel with it.
- **`evidence`** — the reading, with the document and the SECTION, so a reader can go and disagree.
  swiss's cites round five §2.2 `swiss_S2` verbatim, on the raster at Cascadia Mono 16 px in a 9×19
  box, and notes that §7 of the same document finds `naught ◦` at 13.5 % by eye as well.
- **`review`** — the human session, and nothing else. Not an increment, not a re-measurement, and not
  the next round's arithmetic — **because arithmetic is what the exemption exists to overrule.**

### The Limit, in the kit that carries it

The four hue-only kits get a `LIMIT (L12, …)` paragraph in their own class docstring, each with its own
grey number and the disposition spelled out. They are not four copies of one sentence: each says why
this particular language cannot widen the channel.

```
instrument  2.34:1   the highest of the four and the only one over 2:1
prism       1.59:1   the kit that already moved PRIORITY off hue for a nine-unit collision,
                     so the match is the one place left where it asks colour to work alone
swiss       1.52:1   round five's "la peor cifra del corpus" -- and a limit the kit's own
                     founding rule produces: no boxes, no markers, no drawn type means every
                     channel but colour is already spent before the match is reached
nord        1.34:1   the thinnest, and the one kit where the limit is DOCTRINE: base16
                     inherits the user's palette and has by construction no identity of its own
```

## §3 — law

| law | what it binds |
| --- | --- |
| `test_the_eye_exemption_is_named_measured_and_still_needed` | every row is **still under the floor** measured off the shipped pixels (not off `BELOW_THE_FLOOR` — the exemption is checked against the corpus, not against another record of it); the clause it exempts is the clause the corpus actually misses, to the letter; the evidence is ≥ 25 words and cites a `§`; the review is ≥ 12 words; **and the two tables about this mark name the same mark** |
| `test_the_eye_exemption_goes_stale_the_moment_the_mark_passes` | the stale check, in two arms |
| `test_the_hue_only_limit_is_written_into_the_kit_that_carries_it` | exactly the kits whose match channel is HUE carry the paragraph and no other; each carries **its own** number to two decimals, the number `MATCH_IN_GREY` records and inc84's law re-measures off the greyscale PNGs; each says `LIMIT` and `RECORDED AND NOT FIXED`; the four numbers are distinct, so no kit inherited another's |

**The two-tables clause is not tidiness.** `OBLIGATION_UNDER_THE_FLOOR` is inc82's MEASUREMENT of swiss
`•` and `SEEN_BY_EYE` is inc86's EXEMPTION of it. Two tables drifting apart about one row is exactly
the failure `test_the_homoglyph_table_is_one_table_in_two_files` exists against, so every obligation
under the floor must be exempt here and every obligation exempted here must be there.

## §4 — teeth

`test_the_eye_exemption_goes_stale_the_moment_the_mark_passes`, and **the mutant is the MEASUREMENT,
not the roster** — the shape `test_the_obligation_floor_bites_on_the_marks_inc82_replaced` already
uses. `floor_rows` is patched, twice:

1. **the mark PASSING** — the state the corpus would be in if somebody widened `•` the way inc82
   widened instrument's `⠁`. The law must go red, and the red says *retire it* rather than saying
   nothing at all. **This is the arm that makes the exemption expire on its own terms instead of on
   nobody's.**
2. **the mark sliding from `COV` to `COVEFF`** — and this is the arm that matters more. A mark that has
   started missing a second clause **is a mark round five did not read**, and an exemption may not
   cover it by inheritance.

## §5 — what was found by looking

**1. The exemption has to be checked against the PIXELS, not against `BELOW_THE_FLOOR`, and the first
draft did it the other way.** Reading `BELOW_THE_FLOOR[key]` would have made the law a comparison
between two records that inc85 and inc86 both edit — an exemption verified against the table that
records the thing it exempts. `floor_rows(lang)` is the corpus. The difference is invisible while both
agree and total the moment they do not, which is the whole reason the stale check exists.

**2. The four Limits are four different sentences and only one of them is a concession.** Writing them
made that visible: nord's is **doctrine** (base16 inherits the environment, so inventing a second
channel would be leaving the language's founding commitment), swiss's is **produced by the kit's own
founding rule** (no boxes, no markers, no drawn type — every channel but colour is spent before the
match is reached), prism's is **the last one standing** (this kit already moved priority off hue for a
nine-rgb-unit collision), and instrument's is the plain case. A ruling that let all four say "recorded,
not fixed" and stop would have hidden that three of the four are structural.

**3. The programme has issued forty-three rulings and four of them required no code.** That count only
appeared once the table was built. The four — `G vs ruling 10`, `inc60 info to air`, `swiss ╎`,
`solari mut` — are the ones a reader is most likely to re-open, precisely because nothing in the diff
history marks them, and they are now in the same table and the same column as the forty they sit
beside.

**4. `swiss •` is the only row in `SEEN_BY_EYE` and the law asserts the roster is not empty**, which is
worth saying out loud: a roster of exemptions whose non-vacuity arm is missing passes perfectly on an
empty table, and this one has exactly one row to lose.

## §6 — files and frames

| file | change |
| --- | --- |
| `taskboard/language.py` | the `LIMIT (L12, …)` paragraph in `Instrument`, `Swiss`, `Nord` and `Prism` class docstrings — **four docstrings and no code** |
| `tests/test_components.py` | `SEEN_BY_EYE`, two laws over it and the stale check; `test_the_hue_only_limit_is_written_into_the_kit_that_carries_it` |
| `.fast-dev-flow/spec.md` | **§23** — the batch record, the L12 Limits, and §23.6, the programme's forty-three rulings with the packet that carries each |

**Frames changed: ZERO.** `render.py`, `raster.py`, `second_width.py` and `capture_languages.py` were
all re-run and `git status --porcelain` is empty on `prototypes/`. A docstring is not a drawing.

## §7 — deviations, named

- **`OBLIGATION_UNDER_THE_FLOOR` was kept rather than folded into `SEEN_BY_EYE`.** Two tables about one
  row is a drift risk this file has a law against; the answer taken is the cross-check
  (§3) rather than a merge, because the two say different things — one is what the corpus MEASURES and
  one is what the ruling ALLOWS — and inc82's roster is wired into a law and a tooth of its own that
  this increment was not asked to rewrite.
- **`naught ◦` at 13.5 % is NOT in `SEEN_BY_EYE`**, although round five §7 reports finding it by eye.
  The ruling names swiss's obligation and nothing else, and `naught ◦` misses BOTH clauses (14.0 %
  coverage **and** 2.40 effective) — so an eye-read of its visibility does not answer the clause it
  fails second. It stays in `BELOW_THE_FLOOR` as `COVEFF`. Named here so the omission is a decision
  rather than an oversight.
- **The Limit is recorded in the kit docstring and in `spec.md` and NOT in `LANGUAGES.md`.** The ruling
  names two places; `LANGUAGES.md` is a third and is not in this brief.
- **`legibility.txt` gained no section for L12.** Section H already carries the measurement and inc84
  wrote it; a second passage restating the same four numbers with a verdict attached would be the
  instrument holding an opinion about what it measures, which `raster.py`'s docstring refuses from the
  other side.

## §8 — gates

```
pytest -q                1466 passed, 2 skipped, 26 warnings in 43.82s
                         (inc85 1463 -> 1466, +3; ZERO failed --
                          test_win_clipboard_roundtrip passed again)
verify_language.py       ALL PASSED                                     exit 0
render.py                66 .txt + 66 .svg / 330 pairs / 0 hand-drawn    exit 0
                         -- and NOTHING changed on disk
raster.py                132 PNGs identical across two PROCESSES
                         (66 colour + 66 grey)                          exit 0
legibility.py            867 lines · byte-identical across two PROCESSES exit 0
second_width.py          0 rows cut in 0 frames · 330 pairs distinct     exit 0
matrix.py                refusals [] for all eleven                      exit 0
collision_census.py      TOTAL 27 · homoglyph rows 24 (both unchanged)   exit 0
capture_languages.py     22 grids identical across two PROCESSES ·
                         gallery UNCHANGED by this increment             exit 0
export_to_skill.py       11 languages round-trip · every token, doc and
                         family verified · captures 2 WRITTEN / 64 already
                         identical (the two gallery grids inc85 moved) ·
                         SURFACES.md 11 postures                          exit 0
```

The skill repo was **not** committed.

## §9 — pending / next

Batch `rework-8c` is closed; `spec.md` §23 is the record. What goes back to the round:

- **the `darkside o` derivation defect** (inc85 §5.1) — an instrument question, found by this batch and
  deliberately not fixed inside it;
- **the three cursors in `accent`** — instrument `⣿` 2.94, swiss `▮` 2.57, industrial `▶` 2.97: the
  cursor family fails Q1's effective clause as a FAMILY, and the ruling reaches `mut` and `dim` only;
- **`corgi ░` and `ledger *`** — no tier in their own kit clears the clause; only another cell would;
- **the eight seats that miss BOTH clauses** — they want inc82's kind of move, a glyph out of the
  language's own alphabet, and that needs a round;
- **`naught_S2` and `naught_S4`** — L10 and the `DANGER_FORM` frame, the round's oldest open reworks,
  still in no brief.
