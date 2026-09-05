"""Batch close: fill spec §8 and amend the PROTOTYPE packet's matrix."""
import pathlib

spec = pathlib.Path(".fast-dev-flow/spec.md")
s = spec.read_text(encoding="utf-8")

CLOSE = '''## 8. Close (filled in phase C)

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
'''

start = s.index("## 8. Close (filled in phase C)")
s = s[:start] + CLOSE
s = s.replace("| Current phase | B — implementation |", "| Current phase | closed |")
s = s.replace("| Closed | — |", "| Closed | 2026-09-04 |")
spec.write_text(s, encoding="utf-8")

# --- the PROTOTYPE packet's matrix is now historical; say so at the top ----
pk = pathlib.Path("prototypes/components/PROTOTYPE.md")
t = pk.read_text(encoding="utf-8")
NOTE = '''> **AMENDMENT 2026-09-04, after the operator's verdict.** The matrix in §1 and the per-language sections
> below are the record of the PROTOTYPE ROUND and are kept verbatim. The batch that executed the verdict
> is `kits-learn-3` (`.fast-dev-flow/spec.md`, packets `inc14.md`..`inc19.md`), and it moved the matrix
> from **0** cells at `implementa` to **14 of 30**. The `.candidates.md` sidecars beside these frames have
> been RE-RENDERED and now describe the current frames, so where §1 and a sidecar disagree, **the sidecar
> is right and §1 is history**. Re-run `python -X utf8 prototypes/components/matrix.py` for the live table.

'''
if "AMENDMENT 2026-09-04" not in t:
    i = t.index("# PROTOTYPE")
    j = t.index("\n", i) + 1
    t = t[:j] + "\n" + NOTE + t[j:]
    pk.write_text(t, encoding="utf-8")

print("spec §8 filled; PROTOTYPE.md amended")
