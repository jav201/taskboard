# Increment 25 — F-14's two reds diagnosed: both are the CHECK, and the sweep goes green

**Batch:** `harness-hygiene` · **AC-3, AC-4** · `inc14.md` §7, carried in `inc17`, `inc19`, `inc20`,
`inc21`, `inc22`, `inc23`
**Files:** `prototypes/verify_language.py` — **1 source file**.

**`ALL PASSED`. 10857 checks, 0 failures. Neither kit was wrong; both checks were, and both were wrong
in the same way — a hand-typed literal that stood for an axis and never learned the eleventh language.**

---

## 1. What was carried, and for how long

Two names, red since `kits-learn-2`, reported verbatim in six packets as "the two pre-existing ones,
unchanged":

```
2 FAILURE(S): ['character: the token is `MOTION_STEPS` and it governs FIVE events, ...',
               'prism: rail renders IFF the language declares layout=rail']
```

Re-measured at this batch's HEAD before any edit — `10854 PASS, 2 FAIL`, exactly those two
(`.fast-dev-flow/spec.md` §4). Nobody had asked which side was wrong. Both are, and the answer is the
same both times: **prism, the eleventh language, arrived and two checks did not notice.**

---

## 2. Red one — `MOTION_STEPS`. The check is wrong.

**What the check asserts.** That the token is not called `FLIP_STEPS` any more, and that every
language's motion budget equals a hand-typed table:

```python
{n: LG.kit(n).MOTION_STEPS for n in TH.ORDER}
== {"naught": 3, "corgi": 1, "instrument": 3, "swiss": 0,
    "industrial": 1, "nord": 1, "darkside": 3, "ledger": 1,
    "solari": 3, "blueprint": 2}                              # TEN entries
```

**What the kit renders.** `TH.ORDER` has **eleven**:

```
['naught','corgi','instrument','swiss','industrial','nord','darkside','prism','ledger','solari','blueprint']
{'naught':3,'corgi':1,'instrument':3,'swiss':0,'industrial':1,'nord':1,'darkside':3,
 'prism':3,'ledger':1,'solari':3,'blueprint':2}
```

Every pinned value still matches. The dict comparison fails on **one extra key**, and on nothing else.

**What decides.** Prism's own `MOTION_STEPS = 3` in `taskboard/language.py` is argued at its definition,
and the argument is a commitment, not a default:

> "Four was tried first, reasoning that a braille cell has four dot-rows … The harness refused it and was
> right: the switch's knob has THREE SEATS, so a 4-step budget repeats a frame … Sharing the value 3 with
> four other languages costs nothing — what the laws compare is the FRAME LIST, and Prism's is drawn in
> its own ramp and its own half-cell grip."

The kit was reasoned into its number *by this harness refusing an earlier one*. The table was simply
never extended. **Check defect.**

**The fix, and the one thing it does not do.** `"prism": 3` is added to the pin. It is **not** derived —
every other rotted literal in this file became `len(...)` off its own derivation (`inc14.md` §5), and this
one cannot: the entire purpose of a typed table is that re-tuning any language's motion budget is a red
line a human has to walk up to. What is added instead is the **detail string**, because the reason this
red survived six packets is that a `==` between two eleven-key dicts printed no detail at all:

```
before:  [FAIL] character: the token is `MOTION_STEPS` and it governs FIVE events, …
after:   [PASS] character: the token is `MOTION_STEPS` … off the pin: [] · pinned but gone: []
red:     off the pin: ['prism: pinned 3, declares 2']
```

The next language costs one reading instead of six packets.

---

## 3. Red two — `prism: rail renders IFF layout=rail`. The check is wrong, and it was committing the
defect it warns about.

**What the check asserts.** Its own comment states the law:

```python
# DISPATCH: the mechanism must follow the token, not the class name —
# a hardcoded rail would make `layout` dead metadata (VERIFY.md)
RAIL = LG.KITS["darkside"].RAIL                    # '▏'
for name in TH.ORDER:
    check(f"{name}: rail renders IFF the language declares layout=rail",
          any(RAIL in r for r in rows) == (TH.THEMES[name].get("layout") == "rail"))
```

It asks **all eleven languages for darkside's `▏`**.

**What the kit renders.**

```
darkside   layout='rail'   RAIL='▏'   rail_prefix='[#262626]▏[/]  '
prism      layout='rail'   RAIL='▎'   rail_prefix='[#a3e635]▎[/]  '
(the other nine: no RAIL attribute at all)
```

Prism declares `layout: rail`, draws a rail, and draws `▎`. The check's left side is `False`, its right
side is `True`. Red.

**What decides.** Prism's `RAIL` in `taskboard/language.py` carries the commitment in capitals, and it
names this exact check:

> "NOT DARKSIDE'S STROKE. `▏` is that language's rail and the suite holds a NEGATIVE law over it — no
> other language may carry it — because a shared structure device is a shared language wearing two names.
> Prism's is a HEAVIER stroke in the project's own hue: darkside's rail is passive grey that groups, this
> one NAMES while it groups."

So the kit is doing the declared thing, and **the check was making one class stand for the axis — which is
precisely what its own comment forbids, committed by the checker instead of by a kit.** Check defect.

**The fix.** Both halves are asserted over the SET of declared strokes:

```python
RAILS = {g for g in (getattr(LG.KITS.get(n, LG.Kit), "RAIL", None) for n in TH.ORDER) if g}
...
own   = getattr(LG.KITS.get(name, LG.Kit), "RAIL", None)
drawn = {g for g in RAILS if any(g in r for r in rows)}
want  = {own} if TH.THEMES[name].get("layout") == "rail" else set()
```

A rail language draws **its own** stroke and no other's; a non-rail language draws **none of them**. That
second clause is a strengthening, not a translation: the old form could only see `▏`, so prism's `▎` could
have appeared on any of the other ten languages' rows and nothing here would have said so.

Plus a self-check, because a set that came back empty would have passed the loop vacuously for all eleven:

```
[PASS] the rail is a set of DECLARED strokes, one per rail language
       (probe self-check — an empty set would pass the loop below vacuously)  ['▎', '▏']
```

`len(RAILS) == the number of rail languages` also **is** the negative law: two rail languages sharing one
stroke collapse the set and redden it.

---

## 4. Nothing was changed in `taskboard/language.py`

The gate said a kit defect would be fixed there only if ≤ 10 lines with its property test red-then-green.
**Neither red was a kit defect**, so nothing there was touched. Both commitments — prism's motion budget
and prism's stroke — are argued at their definitions and both stand.

---

## 5. Test results

### 5a. The sweep — AC-4

```
python -X utf8 prototypes/verify_language.py

== THE GATE ITSELF: settle headroom
  [PASS] settle() keeps headroom under its bound (a gate near its limit is a gate about to rot)
         worst 4 of 40 over 155 captures

ALL PASSED

PASS: 10857   FAIL: 0   (exit 0)
```

Baseline at this batch's HEAD: `10854 PASS, 2 FAIL`. **+3 checks and −2 failures**: the two that were red
are green, and the third is the new self-check. No check was deleted or suppressed.

The two, in full:

```
[PASS] character: the token is `MOTION_STEPS` and it governs FIVE events …
       off the pin: [] · pinned but gone: []
[PASS] the rail is a set of DECLARED strokes, one per rail language …  ['▎', '▏']
[PASS] darkside: rail renders IFF … OWN stroke, never another's  drawn=['▏'] want=['▏'] layout='rail'
[PASS] prism:    rail renders IFF … OWN stroke, never another's  drawn=['▎'] want=['▎'] layout='rail'
[PASS] naught … drawn=[] want=[] layout='lattice'          (and the other eight, each with its layout)
```

**No remaining red.** This is the first `ALL PASSED` this worktree has recorded from
`verify_language.py`.

### 5b. The anti-vacuity probe — the green can go back to red

A green check that was red for the wrong reason is only a fix if the green is falsifiable.
`prototypes/out/_hh_f14_probe.py` drives both rewritten expressions, copied verbatim, against a mutated
tree:

```
== ARM 1: the tree as it ships — both checks must be GREEN
  [PASS] MOTION_STEPS pin  off the pin: []
  [PASS] rails self-check  ['▎', '▏'] vs 2 rail language(s)
  [PASS] rail loop, all eleven  red: []

== ARM 2: prism re-tunes its motion budget 3 -> 2
  [PASS] MOTION_STEPS pin CAN go red  off the pin: ['prism: pinned 3, declares 2']
  [PASS] ... and it comes back  off the pin: []

== ARM 3: prism adopts DARKSIDE's stroke (the negative law)
  [PASS] rails self-check CAN go red  ['▏'] vs 2 rail language(s)
  [PASS] ... and it comes back  ['▎', '▏'] vs 2 rail language(s)

== ARM 4: naught DECLARES layout=rail without drawing one (dead metadata)
  [PASS] naught CAN go red  drawn=[] want=[None]
  [PASS] ... and it comes back  drawn=[] want=[]

== ARM 5: DARKSIDE's stroke strays into ledger (the limb the OLD check could also see)
  [PASS] new check goes red  drawn=['▏'] want=[]
  [PASS] old check would ALSO have gone red (so this is not the fix's gain)

== ARM 6: PRISM's stroke strays into ledger — the limb the old check was BLIND to
  [PASS] new check goes red  drawn=['▎'] want=[]
  [PASS] old check would have PASSED — the hole this fix closes

== ARM 7: and with no stray, ledger is green under both
  [PASS] no stray, new check green  drawn=[] want=[]
```

**ARM 6 is the fix's actual gain, measured**: the same tree, the same stray glyph, old check green and new
check red.

**And one arm was wrong and is recorded as wrong rather than deleted.** The first ARM 5 flipped darkside's
`layout` to `flow` and expected a red. It got a pass, correctly: flipping that token flips *both* sides of
the IFF, because the kit reads `self.layout` to decide whether to draw a rail at all. The old check had the
same property. That is the mechanism following the token — the thing being asserted — not a hole, and the
probe now says so in a comment where the bad arm stood.

### 5c. Suite, and the fixture

```
python -X utf8 -m pytest -q
693 passed, 2 skipped, 4 warnings in 32.93s          (unchanged from inc24)

git status --porcelain -- prototypes/out/_fixture_late.json
(no output)
```

`verify_language.py` is not imported by any test, so the suite is unmoved by design; it is run to say so.
The fixture line is inc24's guarantee holding across a second full harness run.

---

## 6. Risks

- **The pin will rot again on language twelve**, by construction. That is the trade §2 makes on purpose —
  a typed table is a red line — and the only thing this increment buys is that the failure now *names the
  entry*. Someone will still have to walk up to it.
- **`RAILS` is derived from a class attribute that only two kits define.** A language that drew a rail
  without declaring a `RAIL` attribute — building the stroke inline in `rail_prefix()`, say — would be
  invisible to both halves of the new loop. Nothing prevents that today; the two that exist both declare
  it.
- **The stray-glyph limb is asserted over `card_rows` + `head` only.** A rail stroke reaching some other
  surface of a non-rail language is not covered here. The old check had the same reach; it is not made
  worse, and it is not made complete.
- **The self-check couples two laws in one assertion** (`len(RAILS) == rail language count`): it fires both
  when a rail language loses its glyph and when two share one. The detail string distinguishes them; the
  label does not.

## 7. Pending

- **F-15** — the lattice flake. inc26, and it has not reproduced yet (40 isolation runs and 10 full-suite
  runs green at this HEAD).
- **F-8** — `--surface` still has to be run plain and alone. Untouched; it is run once at the batch close.
- **`export_to_skill.py:copy_captures`'s docstring** still describes F-17's symptom in the present tense
  (inc24 §6).
- **`RUN.md` says `verify_language.py` reports "2178 checks"** and this run reports 10857. That number has
  been stale for many passes and is not this increment's to move, but it is now the only place in the repo
  that describes this harness by a wrong size.

## 8. Suggested next task

**inc26 · F-15**, then the batch close: `--surface` plain and alone, and §8 of the spec.

---

## Evidence checklist

- [x] **Tests/type checks/lint pass** — `verify_language.py`: **ALL PASSED, 10857 PASS, 0 FAIL, exit 0**
      (§5a). Suite `693 passed, 2 skipped in 32.93s` (§5c). Anti-vacuity probe: 7 arms, all as expected
      (§5b).
- [x] **No secrets in code or output** — two check expressions in a harness; no path, no network, no
      dependency. The tracked fixture is clean after the run (§5c), and `test_no_live_board.py` /
      `test_privacy_sweep.py` are inside the suite number.
- [x] **No destructive commands run without approval** — no `rm`, no force, no terminal process killed.
      Writes: one source file and scratch logs under the gitignored `prototypes/out/`.
- [x] **File count within cap** — 1 source file, plus this packet: 2.
- [x] **Review packet attached** — this document.
