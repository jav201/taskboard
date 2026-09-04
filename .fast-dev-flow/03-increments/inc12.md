# Increment 12 — L-33 / SCOPE F-1: Corgi's display posture reads the label it documents

Batch `2026-09-04-fastflow-09` ("kits-learn-2") · increment 1 of 2 · base ref `d58fa07`
(branch `kanban-variants`). One agent, 2 source files. **No git operations.**

Scope: *`_surface_display` reads `label`; `display_label()` stops spending a keybinding it does not
own; the refusal that said it should is retracted out loud; the two display frames are recaptured;
SCOPE's suite is run as the consumer check.*

## 1. What changed

**The legend is the caller's and the notation is the language's.**

`Kit.display_label()` documented `idx` and hardcoded nothing else; `_surface_display` took a `label`
argument and threw it away. So **every corgi and industrial display in every app said `[1] DISPLAY`**,
and LANGUAGES.md §3b is explicit that in a TUI *"the numbers ARE the keybindings"* — which means the
kit was not keeping a mark, **it was spending a key on its consumers' behalf.** SCOPE's `[1]` cycles
its SOURCE; the legend reading `DISPLAY` over it was that app's luck, which is exactly how SCOPE's
own F-1 put it.

The rule, one sentence: **`label` is split once on whitespace; an ASCII run of digits in front is the
BINDING and the rest is the WORD; anything else is a word only and the language keeps its own index.**
A `numbered` language letters `[binding] WORD`; one that is not letters `WORD` and **drops** the
binding. No label at all renders exactly what it rendered before.

```
corgi       ''                 -> '┌ [1] DISPLAY ─────────────────────────┐'
corgi       '7 SOURCE'         -> '┌ [7] SOURCE ──────────────────────────┐'
corgi       'mbb rho final'    -> '┌ [1] MBB RHO FINAL ───────────────────┐'
corgi       '3D FIELD'         -> '┌ [1] 3D FIELD ────────────────────────┐'
corgi       '7'                -> '┌ [7] DISPLAY ─────────────────────────┐'
industrial  '7 SOURCE'         -> '▛ [7] SOURCE ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▜'
```

**A refusal was retracted, and the retraction is the finding.** `kits-learn`'s inc8 put `"display"` in
`LABEL_REFUSED` with a commitment: *"the label beside a display belongs to the CONTROL, and the
language numbers it (`display_label`) rather than letting a caller name it — an OP-1 screen's legend is
the machine's."* **That commitment is half wrong, and the consumer is what proved it.** It is true of
the **notation** — the brackets, the casing, the position — and false of the **content**, because the
number inside the brackets is a keybinding. The entry is deleted and a dated comment in its place says
why. A declared-refusal table exists so a refusal *can be wrong out loud*; this is the table being
wrong out loud, which is the mechanism working rather than a reversal to apologise for.

**Why a mini-syntax and not a new parameter** (spec §6.1, three rejected alternatives): a verbatim
label breaks the `numbered` token, the one thing L-33 says must stay in charge; a word-only label
fixes half the defect and leaves `[1]` still spent by the kit; and a new `idx=` on `raster_region`
gives eleven postures a second argument ten of them refuse, to carry an integer already expressible in
the string that was already documented.

## 2. Two things the brief's framing got wrong once I built it

**"Industrial is not `numbered`."** The spec's AC-2 said so and it is **false**:

```
{'naught': False, 'corgi': True, 'instrument': False, 'swiss': False,
 'industrial': True, 'nord': False, 'darkside': False, 'prism': False,
 'ledger': True, 'solari': False, 'blueprint': False}
```

Both languages that use the `display` posture are numbered, so **no shipped language exercises the
unnumbered limb.** Rather than drop the AC or fake it, it is asserted by **swapping the token** — the
idiom `test_mutation_changes_the_render` already uses on this file — because `Kit.numbered` is
`bool(self.t.get("numbered"))`, so a kit with it off is a real kit and not a mock. The correction is
written into spec §3 AC-2 in place, dated, before any edit; §6.2's table moved `surface_industrial.*`
from AC-2's reason to AC-1's at the same time.

**"A mutation test proves a token is READ; only a property test proves it is read CORRECTLY"** — the
brief's rule, and building it showed *why* it bites here specifically.
`test_every_optional_argument_is_read_or_declared_refused` would have gone green the moment `display`
did **anything** different with `label`: lettered it backwards, hashed it, drawn one cell of it. The
property that actually had to hold is narrower — the caller's binding and the caller's word arrive
**intact and adjacent** — and it had to be asserted on **`chrome`**, not on `rows`, because a caller
outside Textual (SCOPE is exactly one) consumes `chrome` and never sees `rows`. Asserting on `rows`
would have passed while the compositor's half of the contract stayed broken.

## 3. Implementation

`taskboard/language.py`:
- `display_label(self, idx=1, label="")` — the split rule above, with the reasoning and the known
  edge in the docstring. `head.isascii() and head.isdigit()` guards the `int()`: `"²".isdigit()` is
  True and `int("²")` raises, and this argument is caller text.
- `_surface_display` — `k.display_label(label=label)`. **The width math is untouched**: `len(lab)` on
  the plain string, `mark(lab)` on the way out, in that order. Pitfall A1 says escaping changes a
  string's character count and not its cell count, so padding an escaped string returns a rectangle one
  cell short. The existing order was already right and was preserved rather than re-derived.
- `LABEL_REFUSED` — the `"display"` entry deleted, replaced by the dated retraction comment.

`tests/test_surface.py` — `DISPLAY_LANGS` (derived from `THEMES`, not spelled) and four parametrized
tests, 8 cases:
- `test_the_display_legend_is_the_callers_mark_and_reaches_the_chrome` — the property test: `[7]
  SOURCE` in `chrome[0]`.
- `test_an_unnumbered_display_drops_the_binding_it_has_no_notation_for` — the token swap; asserts the
  word survives and neither `7` nor `[` appears.
- `test_a_legend_with_no_binding_keeps_the_languages_own_index` — pins `[1] MBB RHO FINAL`, the exact
  string the sweep produces, so the `numbered` token stays visible in the shipped artefact.
- `test_an_untold_display_still_says_what_it_always_said` — the default, so a future edit that moves it
  fails here naming the reason instead of as 62 mystery frame diffs.

## 4. Files modified

| file | source? | what |
| --- | --- | --- |
| `taskboard/language.py` | source | `display_label()`, `_surface_display`, `LABEL_REFUSED` retraction |
| `tests/test_surface.py` | source | `DISPLAY_LANGS` + 4 parametrized tests (8 cases) |
| `prototypes/gallery/surface_{corgi,industrial}.{txt,svg}` | artefact | recaptured, see §5 |
| `.fast-dev-flow/spec.md` | flow artefact | AC-2 correction + §6.2 table, dated |
| `.fast-dev-flow/baseline-kits2/**` | flow artefact | 66-frame pre-edit baseline |

**2 source files.** No new dependency.

## 5. Test results and the capture

```
$ python -X utf8 -m pytest -q
335 passed, 2 skipped, 4 warnings in 28.65s
```

327 baseline + 8 new. No regressions, no new skips. **The pre-existing environmental clipboard failure
the brief warned about did not appear** — not in the Phase-A baseline run and not here. Recorded as
not-observed rather than assumed away; the environment may simply differ from the one that saw it.

**The four failures that came first, and were predicted in writing before the edit** (spec §6.2, "stated
in advance"):

```
FAILED tests/test_surface.py::test_chrome_preserves_the_frame_the_shipped_capture_shows[corgi]
FAILED tests/test_surface.py::test_chrome_preserves_the_frame_the_shipped_capture_shows[industrial]
FAILED tests/test_surface.py::test_check_box_matches_shipped_is_green_for_all_eleven_frames[corgi]
FAILED tests/test_surface.py::test_check_box_matches_shipped_is_green_for_all_eleven_frames[industrial]
```

That is **`inc11`'s F-12 check catching a stale frame on its first real occasion** — the increment
before this one, working on this one. It was not debugged; it was answered by recapturing.

**The capture** — `python -X utf8 prototypes/capture_languages.py --surface`, run plain and alone
(F-8), one run, green first time:

```
image mbb_rho_final.npy | viewport 118x34 | 11 languages | animations off
  corgi       display   118x34  78.6% ink   raster (360, 120)
  industrial  display   118x34  78.6% ink   raster (360, 120)
  11 surfaces -> ...\prototypes\gallery
  no two identical (55 pairs)
```

**What a person sees, before and after** — row 3 of each sheet, the only row that moved:

```
corgi       BEFORE   ┌ [1] DISPLAY ───────────────────────────────────────────────────┐
corgi       AFTER    ┌ [1] MBB RHO FINAL ─────────────────────────────────────────────┐
industrial  BEFORE   ▛ [1] DISPLAY ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▜
industrial  AFTER    ▛ [1] MBB RHO FINAL ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▜
```

(shown trimmed to fit this page; the real rows are 118 cells). **The box did not move** — the rule
shortened by exactly the characters the legend gained, which is the A1 width math holding, and
`test_a_label_cannot_inject_markup_or_steal_a_cell` now genuinely exercises these two languages for the
first time: until this increment display refused the label, so that test was asserting nothing about
them.

**AC-7, byte comparison against the pre-edit baseline:**

```
identical: 62 / 66
MOVED: surface_corgi.svg surface_corgi.txt surface_industrial.svg surface_industrial.txt
```

Exactly the four named in §6.2 in advance, no more. No board frame moved — the board never calls
`raster_region`, so the F-1-flaky board sweep was not run at all.

**AC-8, the consumer check** — `tui-demos` read-only, from its root:

```
$ python -X utf8 -m pytest apps/scope/tests -q
44 passed in 32.84s
```

**SCOPE's frame does NOT change today, and that is the default-preserved commitment holding at a real
consumer**: `scope.py:129` is `k.raster_region(Image.new("L", (2, 2), 0), TR_W, TR_H)` — no label — so
it still renders `[1] DISPLAY` byte for byte. **It will change the moment SCOPE passes
`label="1 SOURCE"`**, and the gallery collector will detect that drift by sha. That is the mechanism
working, not a regression, and SCOPE now has the primitive its packet said it lacked.

## 6. Risks

- **The mini-syntax's known edge.** A legend that legitimately opens with a number — `"2 PASS"` meaning
  two passes — is read as a binding. `"3D FIELD"` is safe because `"3D"` is not a run of digits, and
  the word is the caller's so it can write `"PASS 2"`. Documented in the docstring and in spec §6.1
  rather than defended against, because the alternative (a second parameter) costs eleven postures an
  argument ten of them refuse.
- **The unnumbered limb has no shipped language.** It is asserted by token swap, which is a real kit but
  not a shipped one. If a future language adopts `display` without `numbered`, that test is what already
  describes its behaviour.
- **`LABEL_REFUSED` is now five entries, not six.** Anything that counted them will be off by one; a
  grep for `LABEL_REFUSED` found no such counter.
- **A concurrent agent is editing `tui-demos`** (see §8). The 44-passed result is a snapshot of a tree
  that was being written to at 11:17–11:25 by someone else; `apps/scope/scope.py` was modified 8 minutes
  before the run, though line 129's call is unchanged (verified). **This increment wrote nothing there.**

## 7. Pending

- **inc13** — L-42, the Sixel probe guard and budget. Next, and sequential.
- F-1, F-8 — untouched, run around rather than investigated (spec §5).
- The real export to `~/.claude/skills/tui-design/` — the orchestrator's call, as in every increment.
  `assets/languages.py` and the two `surface_{corgi,industrial}.*` captures in the skill are now stale
  by exactly the four frames above; **not exported.**
- `LANGUAGES.md` §3b — L-33's own "For the skill" asks for one added sentence there. **Not written.**
  It is a hand-written skill file and the same orchestrator's call as §11 was in `kits-learn`.

## 8. For the skill

1. **A declared refusal is a claim, and a consumer is what falsifies it.** `kits-learn` added
   `LABEL_REFUSED` so that "I decided not to" could be told from "I forgot to". One batch later a real
   app proved one of those declarations wrong. **The value of the table was not that its entries were
   right — it was that a wrong one could be found and dated.** General form: *a registry of deliberate
   omissions earns its keep the first time one of them is retracted, not the day it is written.*
2. **Distinguish a mechanism's NOTATION from its CONTENT before refusing an argument on principle.**
   The retracted commitment was true of the brackets and false of what went inside them, and it read as
   one sentence. *When a refusal cites "this mark is the language's", ask which part of the mark —
   the notation is usually the language's and the content usually is not.*
3. **A mark that encodes a binding belongs to whoever owns the keymap.** Never the library. This is
   SCOPE's own general form and it generalises past legends to status lines, footers, help rows, and
   any chrome that prints a key.
4. **A property test and a mutation test answer different questions, and the difference is where the
   bug hides.** A mutation test asks *is this token read?*; a property test asks *is it read
   correctly?* Here the mutation test would have gone green on a posture that lettered the label
   backwards. *Pair them: mutation for aliveness, property for correctness — and assert the property on
   the surface the CONSUMER reads (`chrome`), not the one the framework reads (`rows`).*
5. **A verification check earns its cost the first time it fires on someone else's change.** F-12's
   `check_box_matches_shipped` was written in inc11 against a bug already fixed; in inc12 it caught two
   stale frames it had never seen, before any human looked. *A check written against a closed finding is
   an investment in the next one.*
6. **Verify the premise of an acceptance criterion before implementing it.** AC-2 asserted a fact about
   the codebase (`industrial is not numbered`) that was false, and one three-line probe found it. *An AC
   that names a specific existing behaviour is a claim to check in Phase B, not a given.*
7. **A concurrently-edited read-only dependency is a reportable condition, not a detail.** Running a
   consumer's suite while another agent writes to that repo makes the result a snapshot with a
   timestamp. *Say which files moved, when, and whether the line your finding depends on is among them.*
