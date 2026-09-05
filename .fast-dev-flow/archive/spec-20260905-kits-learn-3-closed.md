# Quick Spec — taskboard · batch "kits-learn-3" (the component primitives the PROTOTYPE round proposed)

**Batch:** `2026-09-04-fastflow-10` · **Base:** worktree `kanban-variants`, tree carrying the closed prototype
round (`prototypes/components/`, 30 frames + `PROTOTYPE.md`). Predecessor `kits-learn-2` closed 2026-09-04,
§8 filled, archived verbatim to `archive/spec-20260904-kits-learn-2-closed.md`. Language: English.
Increments continue the worktree's single sequence: **inc14 … inc19**.

**Input:** the PROTOTYPE round of 2026-09-04 (`.fast-dev-flow/PROTOTYPE-components.md`, packet
`prototypes/components/PROTOTYPE.md`) and **the operator's ten rulings of 2026-09-04**, reproduced in §6.1
because they are the law this batch executes and nothing here may re-open them.

The round's finding is the input in one line: **thirty frames, zero `implementa` cells.** Five languages
could render all six canonical screens and not one of them could do it out of kit primitives alone —
because twelve primitives are missing in all five at once, and because `STATES` has no `invalid`, so the
premise of a form screen has no seat in the contract at all.

---

## 1. Objective (1 line)

Give the component contract the **six seats** the operator ruled on — a sixth derived state, a caption to
value row, a select/menu pair, an overlay with a **declared refusal registry**, a log row, and a
match/keyhint pair — so that the frames that today draw those elements **by hand** draw them **through the
kit**, each language in its own mechanism, and the 6x5 matrix moves off zero.

---

## 2. User stories

- As **any terminal app with a form**, I want a control to have an `invalid` state the kit derives and draws
  in **shape**, so that five languages stop marking an error with the same red `!` — the palette-swap failure
  at one glyph.
- As **any app with a detail pane, a KPI tile or a settings summary**, I want `Kit.field_row`, so that four
  languages stop borrowing **ledger's dot leaders** for a row they never chose.
- As **a language with a commitment against frames, boxes or silent deletion**, I want my **refusal to be
  code** — declared, falsifiable, with its reason — so that "naught has no overlay" is a thing the suite can
  prove wrong rather than a sentence in a design note.
- As **the operator**, I want every frame whose element becomes a primitive **re-rendered before the commit**,
  so that a sidecar saying `implementado` is a fact about a picture and not a promise.

---

## 3. Acceptance criteria (observable)

Each AC is one increment. Each increment: **<= 4 source files**, **one property test** (not only a mutation
test), **a capture before the commit** (`prototypes/components/render.py`, so the affected sidecars lose the
element), and the worktree suite. Baseline measured at Phase A, **before any edit**: `341 passed, 2 skipped,
4 warnings in 28.50s`.

- [ ] **AC-1 · inc14 · `INVALID` is the sixth derived control state (ruling 1).** `STATES` gains `invalid`;
  `component_states()` **derives** which components take it — no hand list, no component name in the
  derivation. The derivation is stated in §6.2 and its falsifiable consequence is that `bar`, `scrollbar`,
  `button`, `switch`, `checkbox` and `radio` do **not** take it.
  **Property test** (not "is the token read?" but "is it read correctly?"): for **all eleven kits x every
  component whose derived axis contains `INVALID`**, the render's **plain shape** — colour removed at the
  source, `component_cells` glyphs joined — at `INVALID` is **distinct from the shape at every other state
  of that component**. A per-language table that forgot the state falls back to `DEFAULT` and goes red.
- [ ] **AC-2 · inc15 · `Kit.field_row(caption, value, w)` (ruling 2).** A new primitive with a **mechanism per
  language**. **Property test:** the five in-scope languages, handed the **same** `(caption, value, w)`,
  return **five pairwise-different rows**, and every row is **exactly `w` cells** and contains the caption
  and the value **byte for byte**. Pairwise difference is the anti-palette-swap law; byte-for-byte is the
  content law (L-33 / inc12).
- [ ] **AC-3 · inc16 · `Kit.select` and `Kit.menu` (ruling 7), and `danger=True` by SHAPE (ruling 6).**
  `select` is its own primitive (closed state: the chosen value among several); `menu` is the open state;
  `stepper` is **untouched**. `Kit.button(..., danger=True)` grows a **shape** mechanism per language.
  **Property test:** for all eleven kits, (a) `select` != `stepper` for the same options — two controls, two
  renders; (b) the **plain** `danger` button differs from the plain ordinary button of the same label and
  width, i.e. the severity survives with the colour removed, in **every** language including the two whose
  alert hue is already spent (ledger on debt, corgi on the segment).
- [ ] **AC-4 · inc17 · `Kit.overlay` and the refusal registry (rulings 4, 5, 10).** Only **prism** draws a
  modal border. **corgi, blueprint, naught and ledger refuse**, each declared in a registry on the
  `LABEL_REFUSED` pattern with **its own reason**, and each refusal **renders what the language does
  instead**: corgi a numbered MODE, blueprint registration marks with the knockout moved to the default
  answer (`Kit.knockout_cell`, ruling 10), naught the **lattice charge** (backdrop drops charge, the dialog
  is the only full-charge region — no overlay), ledger the reversing entry.
  **Property test:** every name in the refusal registry is a **real language**, every refusing language's
  `overlay()` returns a render that carries **no box lid** and no vertical stroke, and prism's **does**.
  Falsifiable both ways: delete a refusal and the box appears; add a false one and the registry check names it.
- [ ] **AC-5 · inc18 · `Kit.log_row(level, time, message, tail=False)` (ruling 8).** A **full row contract**,
  not an `ICONS` entry. **Property test:** for all eleven kits and all three levels, the **plain** row (colour
  removed) carries a level mark that is **distinct per level**, and the message comes back **byte for byte**.
  The level must be legible with colour removed — that is the ruling, and it is asserted on the plain string.
- [ ] **AC-6 · inc19 · `Kit.match(text, query)` (ruling 9) and `Kit.keyhint` (rulings 3, 9).** `match` returns
  the text **byte for byte** with the match marked: **recasing is forbidden in that row for every language**,
  including the three that upper-case titles. `keyhint` owns the **notation**; every key is the caller's.
  **Property test:** for all eleven kits and a text whose case the language would normally change,
  `plain(match(text, q)) == text` — byte identity, not "contains" — and the marked span is exactly the
  query's span. Plus **ruling 3**: no kit's `button()` output contains a digit the caller did not pass, so
  corgi's numbers stay the parameter keymap (L-33) and its labels stay letters.
- [ ] **AC-7 · every affected frame is re-rendered before its commit.** After each increment, the frames whose
  element that increment implements are re-captured through `render.py`, and the element **disappears from
  the sidecar**. A frame still drawing the element by hand is **not done** — this AC is what makes that
  checkable rather than remembered.
- [ ] **AC-8 · the matrix moves, and its arithmetic is derived.** `matrix.py` is re-run at the end and the new
  6x5 table is reported with the count of `implementa` cells. The table is derived from the same `Sheet`
  objects the frames come from, so it cannot disagree with them. **The batch does not claim a number in
  advance**; §6.3 names the four primitives that stay hand-drawn and therefore which cells **cannot** reach
  `implementa` in this batch.
- [ ] **AC-9 · nothing else moves.** The 66 surface frames stay byte-identical to `.fast-dev-flow/baseline-kits2/`
  unless an increment names the mover in advance. The surface sweep is run **plain and alone** (F-8).

---

## 4. Validation strategy

`python -X utf8 -m pytest -q` in this worktree is the gate for AC-1 through AC-6, run **after every
increment**; baseline `341 passed, 2 skipped, 4 warnings`. New tests live in `tests/test_components.py` (new
file — the component contract has never had a seat in the pytest suite; it was asserted only by
`prototypes/verify_language.py`, which pytest does not run).

`python -X utf8 prototypes/verify_language.py` — the language axis, **2178 checks**, ~80 s — is run whenever
an increment changes the state axis or a glyph table, because that is where the greyscale and mutation laws
live. It is **not** silently allowed to go red: inc14 changes it on purpose (the axis it hard-asserts grows
by one) and the packet says which checks moved.

`python prototypes/capture_languages.py --surface` is run **plain and alone** (F-8 blocks `--surface` when
its output is redirected inside a compound command) for AC-9.

`python -X utf8 prototypes/components/render.py` is the capture for AC-7; `matrix.py` for AC-8. Headless
stdout goes **to a file, never to `DEVNULL`** (L-42). No terminal process is ever killed. No git command that
changes state is run in this batch.

---

## 5. Non-goals (what is OUT)

- **The four primitives the rulings did not cover**: `pane_split`, `required`, `textarea`, `readout_label`.
  They stay hand-drawn and declared, and §6.3 says which cells they hold back. Proposing them is the next
  round's business, not this batch's.
- **The six remaining languages' screens.** All eleven kits get every new primitive (a contract seat with six
  implementations is a hand list waiting to happen), but only the five prototyped languages get frames.
- **Editing `~/.claude/skills/tui-design/` by hand.** `export_to_skill.py` writes it; the gallery selection
  and its Limit lines are **reported** for the operator, not installed.
- **`tui-demos` or any consumer repo.** Read-only, untouched.
- **Form-level validity.** A required-but-empty group is a fact about a FORM, not about a control — see §6.2.
  This batch does not grow a form object to hold it.
- **F-1 / F-8.** Recorded, run around, as in the last three batches.

---

## 6. Detected security flags

- [ ] Auth / identity · [ ] Secrets / config · [ ] External integrations · [ ] Sensitive data
- [ ] Destructive DB · [x] Input / attack surface · [ ] Network / exposure

**`security_required`:** `true` (one flag, narrow — the same row as the last two batches)

**Risk summary:** four of the six new primitives interpolate **caller text** into a markup row
(`field_row`'s caption and value, `log_row`'s message, `match`'s text, `keyhint`'s words). This module's
documented pitfall A1 applies to every one of them: `mark()` escapes `[` as an escaped bracket, which changes
a string's *character* count and not its *cell* count, so padding an escaped string hands back a rectangle
one cell short. **Every new primitive does its width math on the plain string and marks on the way out**, the
order the existing seats already use, and each increment's test asserts the returned row is exactly `w`
cells with a caller string containing a bracket. No secrets, no network, no new dependency, no destructive
command, no git state changed.

### 6.1 · The operator's ten rulings (2026-09-04) — the law of this batch

1. `invalid` enters `STATES` as the sixth derived state; `component_states()` derives it; it survives greyscale.
2. `Kit.field_row(caption, value, w)` is a new primitive with a mechanism per language.
3. Corgi **labels** form buttons (letters/words), never numbers: numbers stay the parameter keymap (L-33).
4. Naught's modal answer is to change the **lattice charge** — no overlay.
5. Only **prism** may draw a modal border; corgi, blueprint, naught, ledger **refuse**, declared and falsifiable.
6. Ledger accepts `danger=True` with a **shape** mechanism (a reversing-entry form), never a colour.
7. `Kit.select` is its own primitive; `Kit.menu` is the open state; `stepper` stays what it is.
8. `Kit.log_row(level, time, message, tail=False)` is a full row contract; the level reads with colour removed.
9. `Kit.match(text, query)` returns the text byte for byte with the match marked; **recasing is forbidden**.
10. Blueprint's knockout may **move** from the title block to the default answer in a confirm — exactly one per view.

### 6.2 · The `INVALID` derivation, and the one thing it deliberately excludes

**The rule:** a component takes `INVALID` **iff it takes `EDITED`** — it has an actuator, it has an interior,
and it is not checkable. *What the arrows can change, the form can reject.* Both terms are registry facts
already declared; no new tuple, no component name, nothing hand-listed. The falsifiable consequence: `slider`,
`textfield` and `stepper` take it; `bar` and `scrollbar` have no actuator, `button` has no interior, and
`switch`, `checkbox` and `radio` are **CHECKABLE**.

**The exclusion, said out loud rather than discovered later.** `CHECKABLE` declares that a control's RANGE is
boolean, and a boolean cannot be out of range: both of its values are legal. "This checkbox is required and
unticked" is therefore **not** a fact about the checkbox — it is a fact about the FORM, which is a group of
controls and has no seat in a per-component state axis. Growing one is §5's non-goal, and this paragraph is
where the operator can overturn the call knowing exactly what it costs (a form object, or `CHECKABLE`
gaining an `INVALID` limb and eleven languages gaining a checkbox and a radio mark).

**Colour is not spent.** `part_tone` is **not** touched by `INVALID`: the state rides shape alone. Two of the
five languages have already spent their alert hue on something that would break if a control borrowed it
(ledger on debt, blueprint on overdue), so "never colour alone" is here enforced as "no colour at all", and
the caller's error *message* keeps whatever hue the caller gives it.

### 6.3 · What cannot reach `implementa` in this batch, named in advance

| screen | primitive still hand-drawn | consequence |
| --- | --- | --- |
| S1 | `pane_split` (x5, one a refusal) | no S1 cell can reach `implementa` |
| S2 | `required` (x5), `textarea` (x5), `Kit.error` (the message's notation) | no S2 cell can reach `implementa` |
| S4 | `pane_split`, carried in from the S1 backdrop by prism / naught / blueprint | those three S4 cells cannot |
| S5 | `readout_label` — corgi's and ledger's L-33 refusal, still declared in the prototype | those two S5 cells cannot |

Everything else is in scope and is expected to reach `implementa`. The batch reports the measured table, not
this prediction.

### 6.4 · Frames that move on purpose

**All thirty component frames may move**, and they move by design — that is AC-7. They are prototype output,
not shipped gallery frames, and they carry no byte-comparison baseline. The **66 surface frames** and the
board frames carry one and must **not** move (AC-9); the only thing that could move them is the `INVALID`
state reaching the live component gallery, and that is checked rather than assumed.

---

## 7. Batch status

| Field | Value |
|-------|-------|
| Current phase | closed |
| Started | 2026-09-04 |
| Closed | 2026-09-04 |
| Promoted to /dev-flow | no |
| Notes | **<= 4 source files per increment, one agent, sequential.** inc14 AC-1 · inc15 AC-2 · inc16 AC-3 · inc17 AC-4 · inc18 AC-5 · inc19 AC-6. AC-7 rides every increment; AC-8 and AC-9 are the close. |

---

## 8. Close (filled in phase C)

### What changed

The component contract gained **six seats, two registries and one state**, and the thirty prototype
frames stopped drawing them by hand. The headline is the matrix: **0 → 14 of 30 cells reach
`implementa`**, and every cell that does not is held back by a primitive the ten rulings did not cover
(§6.3 named all four before the batch started).

| | S1 | S2 | S3 | S4 | S5 | S6 |
|---|---|---|---|---|---|---|
| **corgi** | evoca 1E | evoca 3E | **implementa** | **implementa** | rehúsa 1R | **implementa** |
| **blueprint** | rehúsa 1R | evoca 3E | **implementa** | rehúsa 1R | **implementa** | **implementa** |
| **prism** | evoca 1E | evoca 3E | **implementa** | evoca 1E | **implementa** | **implementa** |
| **naught** | evoca 1E | evoca 3E | **implementa** | evoca 1E | **implementa** | **implementa** |
| **ledger** | evoca 1E | evoca 3E | **implementa** | evoca 1E | rehúsa 1R | **implementa** |

Hand-drawn elements: **76 → 26**, refusals **9 → 4**. What is left is exactly four primitives:
`pane_split` (S1 ×5, S4 ×4), `required` / `textarea` / `Kit.error` (S2 ×5), `readout_label` (S5 ×2).

- **inc14 · `INVALID`** — the sixth derived control state, one term in `component_states`
  (*what the arrows can change, the form can reject*), 33 declared marks. The five languages' identical
  red `!` is gone: a daggered entry, a mis-seated segment bank, a reversed dimension, a half-charged dot,
  a broken block.
- **inc15 · `Kit.field_row`** — the most reused shape in the six screens, with six mechanisms. The
  `hasattr(k, "LEAD")` line that handed ledger's leaders to four languages that never chose them is
  deleted.
- **inc16 · `Kit.select` / `Kit.menu` / `danger=True`** — a stepper shows the two ways OFF a value, a
  select shows the one way INTO a list; severity is a SHAPE and ledger's is the **contra entry**
  (ruling 6 retracts its refusal).
- **inc17 · `Kit.overlay` + `MODAL_BORDER_REFUSED`** — a refusal registry that is **read, not printed**,
  falsifiable in both directions, with six compositions behind it: a box, a box over a grey step, a
  lattice at two charges, a mode that takes the screen, a question posted on a page that stays legible,
  and four registration corners that never join.
- **inc18 · `Kit.log_row`** — the level is a glyph ladder, neutral in hue, because two languages ration
  their alert by commitment.
- **inc19 · `Kit.match` / `Kit.keyhint`** — the text back byte for byte (so the emphasis cannot be a
  shape, which is stated at the seat), and the keymap back to the caller.

Four per-language builders were **deleted from the prototype** (`s3_ledger`, `s4_prism`, `s4_corgi`,
`s4_naught`, `s4_ledger`, `s6_corgi`) — every one of them a language's mechanism living in the frame
instead of in the kit.

### How it was tested

- `python -X utf8 -m pytest -q` after **every** increment. Baseline `341 passed`; final
  **`682 passed, 2 skipped, 4 warnings in 29.18s`** — **341 new tests**, all in the new
  `tests/test_components.py`, the component contract's first seat in the pytest gate.
- Each increment carries **one property test** (not only a mutation test) and inc14's and inc17's were
  **proved falsifiable before they were believed** — a glyph deleted, a registry entry deleted and a
  false one added.
- `python -X utf8 prototypes/verify_language.py` at inc14, inc17 and the close: **2 failures, the same
  two the pre-batch tree already had** (F-14, measured by installing `git show HEAD:taskboard/language.py`
  and sweeping it).
- `python prototypes/capture_languages.py --surface`, **plain and alone** (F-8), after every increment:
  **62 / 66 byte-identical**, the four movers being the ones `kits-learn-2` §6.2 named.
- `python -X utf8 prototypes/components/render.py` before every packet: 30 `.txt` + 30 `.svg` + sidecars,
  no two frames identical within a screen.

### Evidence per AC

| AC | verdict | evidence |
| --- | --- | --- |
| AC-1 · `INVALID` derived, greyscale | **met** | `inc14.md` §2, §4 — 11 languages × 3 components, pairwise distinct with colour removed; the mutation `del PART_GLYPHS['textfield.main']['invalid']` goes red |
| AC-2 · `field_row`, five mechanisms | **met** | `inc15.md` §2 — five pairwise-different rows for one input; `test_no_language_borrows_ledgers_leaders` |
| AC-3 · `select`/`menu`, danger by shape | **met** | `inc16.md` §2 — `select != stepper` in 11; plain danger ≠ plain ordinary in 11; ledger's `(Delete)` |
| AC-4 · overlay + refusal registry | **met** | `inc17.md` §2, §4 — the registry is consulted before the box is drawn, and the both-ways mutation test proves it |
| AC-5 · `log_row`, level in a glyph | **met** | `inc18.md` §2 — three levels, three shapes, one width, all 11; hue whitelist |
| AC-6 · `match` byte for byte, `keyhint` | **met** | `inc19.md` §4 — `plain(match(t, q)) == t` with `==`; no button prints a digit the caller did not pass |
| AC-7 · capture before every commit | **met** | every packet's §6; 76 → 26 hand-drawn elements, each drop named |
| AC-8 · the matrix moves, derived | **met** | the table above, from `matrix.py`, which reads the same `Sheet` objects the frames come from |
| AC-9 · nothing else moves | **met** | 62/66 identical after each increment; the four movers are `kits-learn-2`'s, not this batch's |

### Open risks / pending

- **F-14 (new, not ours):** `prototypes/verify_language.py` was **already red at HEAD** on two checks —
  `character: the token is MOTION_STEPS…` and `prism: rail renders IFF the language declares layout=rail`.
  Measured on the pre-batch tree, run around, **not fixed**: fixing a sweep while changing what it
  measures is how a green run stops meaning anything.
- **Six languages inherit base mechanisms** for `field_row`, `DISCLOSE`, `DANGER_FORM`, `LEVELS`,
  `MATCH_STYLE`, `keyhint` and `overlay`. They have the seat; they have not chosen an answer. That is the
  next round's work and it is the same shape of gap the batch just closed.
- **Two marks do not survive the `.txt`**: blueprint's knockout and every language's match emphasis, both
  because they are backgrounds/styles rather than glyphs. Recorded at the seats; the house convention
  that "the `.txt` is the work" does not hold for them.
- **corgi_S4 is 2.7 % ink.** A refusal that discards the backdrop leaves the FRAME owing content. The kit
  is right and the prototype's shared dialog rows are not a mode. Named in `inc17.md` §7.
- **The log's neutral hue ladder** protects two languages' rations at the cost of nine languages' glow.
  A question for the operator (`inc18.md` §7).
- **`INVALID` excludes checkables** — a required-but-unticked box is a fact about a FORM. §6.2 says what
  overturning it costs.
- **The export is a no-op for everything this batch built.** `export_to_skill.py` projects tokens, class
  docstrings, families and surface postures — not primitives, not registries, not component frames. The
  six new seats and the two registries have **no export path at all**, and `COMPONENTS.md` is hand-written
  prose. Reported, not fixed (§5 non-goal).
- **F-15 (new): one flake observed in `tests/test_surface.py`.** On the sixth full-suite run of this
  batch, `test_lattice_pixels_are_two_colours` failed on
  `len(set(res.pixels.getdata())) == 2`; the file passes 159/159 in isolation and the full suite then ran
  **three consecutive times at 682 passed**. Nothing in this batch touches `taskboard/raster.py` or the
  lattice posture. `RUN.md` claims the suite has been flake-free since the forty-sixth pass — that claim
  is now one observation old. Recorded with its numbers rather than re-run until green and forgotten.
- **A stale-sidecar defect was found at the close and fixed.** `render.py` wrote a `.candidates.md` only
  when a frame HAD candidates, so the fourteen frames that became clean during this batch kept their
  round-one sidecars on disk — files still claiming elements the kit now draws. `candidates_md()` already
  had the empty case written; the guard is gone and every frame writes its sidecar. **A sidecar that
  survives the thing it describes is worse than no sidecar**, because it is the file the matrix's readers
  trust.
- **`visible()` is now a fifth copy** of the same markup-width logic. It is in the module the others
  import; nothing was deleted from them.

### Security flags — handling

One flag fired (input / attack surface), the same row as the last two batches. Four of the six new
primitives interpolate caller text (`field_row`, `log_row`, `match`, `keyhint`). Every one does its width
arithmetic on the **plain** string and `mark()`s on the way out — pitfall A1's order, preserved rather than
re-derived — and the tests assert exactly `w` cells with caller strings containing `[`
(`a[b]c`, `GET /a[b] 500 in 12ms`). No secrets, no network, no new dependency, no destructive command, no
git command that changes state, no terminal process killed, every headless run captured to a file rather
than to `DEVNULL` (L-42).

### Suggested commit message

```
kits-learn-3: six component primitives, two refusal registries, a sixth control state

INVALID enters STATES derived (what the arrows can change, the form can reject);
Kit.field_row, select/menu, overlay + MODAL_BORDER_REFUSED, log_row, match/keyhint.
Six mechanisms per seat, no shared glyph, no rationed hue spent. 341 new tests.
The 6x5 component matrix moves 0 -> 14 of 30 cells at `implementa`.
```
