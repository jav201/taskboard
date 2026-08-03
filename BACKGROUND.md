# BACKGROUND — what this work is, how it got here, and what is trustworthy

Written for **other agents who will analyse this and continue it**. It assumes no prior context.
Companion documents: `HANDOFF.md` (the next task), `PENDING.md` (open items), `RUN.md` (how to run
the prototype).

---

## 1. What was asked, and what came out

**The original request:** refine two Claude Code skills — `tui-design` and `html-visualizer` —
because *"TUI design so far is very static."* The user wanted terminal interfaces that group and
divide better, are navigable, and are genuinely good UI/UX for humans. He supplied design references
(Jitter UI-element motion templates, and a folder of Nothing-OS-style widget images) and asked for
research into other sources.

**What exists now, after one long session:**

| artifact | where | state |
|---|---|---|
| The refined skill | `~/.claude/skills/tui-design/` | 13 docs + `assets/` (2 modules) + `scripts/cost_probe.py` |
| A validated prototype | `<this worktree>/prototypes/widget_slice/` | 10 modules, runnable, two passing verification suites |
| The real app | `<this worktree>/taskboard/` | **untouched by design work**; `main` still at `b3cc60d` |

`html-visualizer` was deferred in the first message and **never refined** — the TUI work never
ended. It is the largest single outstanding item (`PENDING.md` §C10).

**Nothing has been committed.** The user's standing instruction is no commits, no push, no PR. All
work is local in this worktree.

---

## 2. The central finding: the skill was suppressing its own output

The starting skill had five reference files, all about **render fidelity** — colour quantization,
density mechanisms, frame budget, architecture, verification. It had **zero vocabulary** for
hierarchy, grouping, focus, navigation, or motion. Its motion guidance read, verbatim:
*"Only lever = not rebuilding."*

That is a true cost model that an agent reads as a **prohibition**. The skill was producing
technically honest, completely dead interfaces, and the cause was over-applying its own guards.

The revision names **two failure modes** — the *dishonest* TUI (promises what the medium cannot
render) and the *static* TUI (honest and lifeless) — and states that the second is more common and
usually caused by over-applying the guards against the first.

---

## 3. Measured facts that are load-bearing

Everything below was verified by **running textual 8.2.8 / rich 15.0.0**, not read from docs. In this
project docs were wrong 6 times and docstrings 9 times.

**Cost has three pipeline depths, not one.** Same box, same widget:

| depth | what was invalidated | `DataTable` us/cell |
|---|---|---|
| warm | nothing | ~0.02 |
| style-cold | `_styles_cache` (hover, focus, style animation) | **0.54** |
| content-cold | content caches (new data, resize, per-tick recompute) | **6.34** |

**~12x apart.** Style motion is nearly free; re-deriving data is not. A 16x8 sprite is ~0.35% of a
60fps frame.

**Animation has a built-in accessibility contract nobody uses.** Every `animate()` takes
`level=`, defaulting to `"full"` — which classifies it **decorative** and makes it vanish for anyone
setting `TEXTUAL_ANIMATIONS=basic`. Meaningful motion must pass `level="basic"` explicitly. Verified
truth table in `MOTION.md`.

**`Widget.can_focus` is `False` by default and subclasses inherit it.** Tab focuses nothing, with
**no error**. `assert app.focused is not None` after a Tab is the cheapest test in the skill.

**Width safety is not what everyone assumes.** Measured against `unicodedata.east_asian_width`:

| range | safe (Neutral) | **Ambiguous** |
|---|---|---|
| Braille U+2800-28FF | **256/256** | 0 |
| Sextants U+1FB00-1FB3B | **60/60** | 0 |
| Block Elements U+2580-259F | 12/32 | **20** — incl. `█ ▀ ▄ ▁▂▃▄▅▆▇ ▒ ▓` |
| Box Drawing U+2500-257F | 16/128 | **112** — incl. `─ │ ┌ ┐ └ ┘` |

The blocks and frames every TUI uses are safe **by terminal convention, not by Unicode guarantee**.
Adjacent codepoints disagree (`▐` Neutral, `▌` Ambiguous).

**Colour is not the risk.** The `s<0.15` quantization cliff is **HLS**, not HSV, and real palettes
clear it comfortably: Solarized 9/9 hues kept, Nord 11/11, ANSI 12/12, Gruvbox 8/8, phosphor 4/4.
Only **near-neutral tints** are punished.

---

## 4. Claims I made and later had to retract — read these before trusting anything

This section exists because the failures are more instructive than the successes, and because an
analysing agent should know which parts of the history were wrong.

**"There is an ~11x cost spread between machines."** False, and it was **motivated reasoning**: the
convenient conclusion (fast box → motion is affordable) was adopted, and the inconvenient hypothesis
was never tested. The real cause was a bug in my own probe — `clear_cache()` listed `_render_cache`
(a namedtuple with no `.clear()`) and `_content_cache` (does not exist), and a `hasattr` guard
skipped both **silently**. Its "cold" was really style-cold. The instrument was never
mutation-tested, which is the exact discipline the skill preaches. Corrected: the gap is **pipeline
depth**, reproducible on one machine.

**"Monochrome + one accent is technically correct, not just fashionable."** False. Taste dressed as
physics, reasoning from the true fact that greys quantize faithfully. It collapsed every design onto
one road and is what made the user ask for alternatives in the first place. Retracted; the measured
rule is narrow (*don't build a palette out of near-neutral tints*) and `LANGUAGES.md` now offers nine
visual languages instead.

**"Block glyphs are unambiguously narrow."** False — see the EAW table above.

**Eight "languages" that were mostly recolours.** Declared a `base=` design token on every language
and **wired none of them**; the pixel-base library shipped seven renderers and the app called one
function. Two languages rendered **byte-identically**. This is the failure the skill's own rules
forbid, committed while writing those rules.

**And after I "fixed" it, it was still a palette swap — the user caught that too.** His verdict:
*"los temas o lenguajes de diseño se sienten todavía como cambio de paleta de colores únicamente.
Sólo modificas el número que se presenta de frente."* Mechanically provable: **every live structural
token was consumed inside the Hero widget**. Cards, column heads, agenda, gantt, swimlanes, footer
and chrome rendered identically across all eight languages. Wiring `base=` to the hero numeral moved
the defect; it did not remove it.

This is the single sharpest finding of the session, and it came from the user looking at the screen,
not from any test or review. **Resolved 2026-07-26 by the follow-up session**: `taskboard/language.py`
defines a real structure KIT per language (head, card, tile, meter, agenda/gantt/lanes bars, section
headers, calendar cells, queue markers, focus chrome), and `prototypes/verify_language.py` proves it
with 121 checks — a greyscale pair test over all 28 pairs **with the hero region masked**, plus
mutation of every structural token. The decisive assertion reads *"mutating `swiss.frame` changes the
board outside the hero"*. Verified passing.

**Surfaces that were 61-79% blank** while the engine computed six live signals per tick and
displayed one integer. At the widest size class the signal tiles showed six labels and **zero
values** — cropped by width math.

---

## 5. What actually caught these — the methodology worth reusing

No amount of careful writing found the defects. Three things did:

1. **Adversarial review by a different model.** Three separate Fable-model reviews, each given the
   files and told to refute rather than confirm. Every one found real defects that green test suites
   had missed — including the probe bug above.
2. **Looking at rendered output**, not at code. Frames that wrapped and doubled every line, headers
   in a staircase, a hero clipped mid-glyph, an LCD digit in disconnected blobs — all invisible in
   source, all obvious in one render.
3. **Mutation-testing the instruments, not just the asserts.** The corrected cost probe was
   mutation-tested (control 9.5x → mutated 1.1x, reproducing the original bug exactly).

**A caution the next agent should internalise:** in this session, **test-selection bugs outnumbered
app bugs**. Three separate "failures" were the test picking the wrong row, shadowing a variable, or
asserting a stale glyph model — not the code under test. Verify the probe before believing the
verdict.

---

## 6. The product thesis (why the prototype looks the way it does)

taskboard's own README calls it a **"frameless kanban desktop-widget"** — pin it always-on-top and it
floats on the desktop. The code was **four full-screen dashboard views behind number keys**.

The user's refinement made it sharper: *a widget is an aperture, not a scope*. The analogy he gave:
a clock widget that is also an astronomical tracker — small surface, arbitrarily deep engine, with
views to configure it.

So the prototype is three layers: an **aperture** that reads its own width and decides what it can
afford to show (glance <46 cols / widget <80 / board), an **expansion** by progressive disclosure,
and a **signal engine** — six providers on two worker groups, four board-derived and two looking
outside (time-of-day budget, board-file watcher), each with a user-tunable cadence and threshold.

**The identity question is what a design intake exists to catch**, and it surfaced by accident at
turn 12 instead of turn 1. That is why the revised skill opens with `INTAKE.md` as step 0, whose
highest-leverage question is the **posture**: is this glanced at, operated, or read?

---

## 7. Structural lesson worth carrying into any TUI work

**Do not keep a navigation model alongside the drawing.** The most expensive bug class here was a
render that got patched while `nav_model()` did not — the cursor walked a screen that no longer
existed. It is a structural mistake, not a coding one: if "what is on screen" is stored twice, the
two will drift.

The fix is to make items **real widgets** and derive movement from the widget tree, so the drawn
order *is* the model and they cannot diverge. This also buys focus, hover and per-widget motion —
none of which a single box-art widget can express.

---

## 8. Current state

- **The app is untouched.** `main` at `b3cc60d`, no remote branches, nothing committed.
- **The prototype runs:** `python prototypes\widget_slice\app.py` (see `RUN.md` for keys).
- **Two verification suites pass:** `prototypes\verify_widget.py` and `prototypes\verify_board.py`
  — cursor/render coherence, exact frame width at 80/100/140/200 columns, animation verified to move
  across ticks, degraded-motion path, budget headroom.
- **A second session has moved the prototype modules into `taskboard/`** and implemented the
  language axis as real structure kits (`taskboard/language.py`). Four suites green:
  137 pytest · `verify_widget` · `verify_board` · `verify_language`. Files may still be in flux.

**Known-weak spots.** Several claims I published here were re-measured by the follow-up session and
corrected — treat `PENDING.md` as the measured record where the two disagree:

- **My ink-fraction numbers were the wrong size class.** I reported "`nord` 20%, `instrument` 22%
  fail the glance floor", implying two failures. Re-measured with `prototypes/verify_ink.py`: at
  h=26 **all eight languages fail** the 35% glance floor (14-29%), and my figures match the *widget*
  column, not glance. **Screen height dominates the result**, which means the skill's 35% floor is
  unfalsifiable until `DENSITY.md` states the geometry it is measured at — a gap in the skill, not
  just the app.
- **Run-to-run variance of several points** was observed on the board class and **not explained**
  (animation phase is the suspicion, unverified). Pin this before treating any ink number as an
  acceptance threshold.
- Still open: the hero's ~100 dead columns at board size (a braille sparkline was designed, never
  built), and `action_cycle_size` having no route back to automatic sizing.

Full, current list in `PENDING.md`.

---

## 9. Constraints that still apply

- **No commits, push, or PR** without explicit instruction.
- **Supervised increments:** propose → approval → ≤5 files → review packet → stop at the boundary.
- **Spanish** for conversation, **English** for code and technical artifacts.
- Facts are measured against **textual 8.2.8 / rich 15.0.0**; absolutes are one-box and meaningless
  without their pipeline depth. Re-calibrate with `~/.claude/skills/tui-design/scripts/cost_probe.py`.
