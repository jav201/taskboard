VERDICT: PASS-WITH-NOTES

# Security Review, round 2: Inc MR-a field labels (PDR, E3, code-free)

> security-reviewer, 2026-11-06. This is a read-only re-review of the correction `6c2891f` against round 1's
> blocking finding, SEC-1, and ruling R-7. I edited no product file.
> Counts: HIGH 0 · MEDIUM 0 · LOW 2 (new, non-blocking). **SEC-1 is closed at design level.** The
> implementation evidence stays `planned` until E4 runs TC-4820.

## Scope reviewed

- `01-requirements.md` LLR-4603.11 / TC-4820, and `graph-interfaces.cw.md` `gantt_milestone_row` LABEL PATH.
- In the same file, the edges `gantt_milestone_row → fit → _literal → [Data: field label run] → _gantt_field`.
- `graph-proto-V.cw.md` `_gantt_field`, `e2-seams.md` SEAM-7/8, and `e3-addenda.md` A-8..A-11.
- Current code, read-only: `views.py` `c`, `vis`/`fit` (:84-108), `_literal` (:290-312), `collapse_runs`
  (:789), and `_gantt_field` (:2877).

## SEC-1 re-verification (each point checked against the design)

| Check | Result | Where |
|---|---|---|
| The escape covers the whole label before any cell is cut | ✓. Step order (1) measure in cells, (2) `fit` cuts the PLAIN label, (3) one `_literal` on the cut piece, (4) lay the run. The edge `fit ──▶ _literal` says "BEFORE any cell is written". | graph-interfaces LABEL PATH; edges :77-82 |
| Joined runs carry only escaped content | ✓. The first cell holds the whole escaped run, and the covered cells hold `""`. "No cell ever holds an unescaped label character." `_gantt_field` paints the run as given and never splits it (SEAM-8). | graph-interfaces; graph-proto-V `_gantt_field`; SEAM-8 |
| Width is measured with `cell_len`, and a cut ends in `…` | ✓. Room is measured with `vis`/`cell_len`, never `len`. The cut uses `fit`, which goes through `set_cell_size` and adds `…`. The consumed cells number `cell_len(piece) − 1`. | LABEL PATH steps 1-2, 4; TC-4820 example `里程碑 …` |
| The negative controls cover `a]b[/]`, `[@click=…]`, `\` and a wide glyph | ✓. These are the 5 titles × 3 placements, plus NC 1 (one character per cell → `MarkupError`) and NC 2 (room measured with `len` → too wide). A combining-mark title is added. | LLR-4603.11 |

**Probe** (scratch, outside the worktree, `python -I`, real `c`/`fit`/`_literal`/`collapse_runs` and
`Text.from_markup(…, emoji=False)`):

- I built the cells exactly as the LABEL PATH says, with 8 hostile titles in 3 placements: the 5 titles of
  TC-4820, plus `a\[b]`, `\[/]` and `[b]bold`. Result: **24/24**, with 0 exceptions, plain text = the title or
  its cut, 0 spans carrying `@click` or meta, and every line exactly the width.
- NC 1 (per-character cells for `a]b[/]`) raises `MarkupError`, so it goes RED as designed.
- I also put the escaped run right next to a same-tone `bright` neighbour (`2`, `+`, `■`, `▸`) on either side,
  so that `collapse_runs` merges the two. Titles were `x\`, `a]b[/]`, `[@click=app.quit]x`, `\` and `\\`, and
  all came out exact. For example, `x\` joined with `2` becomes `[#…][none]x\\[/none]2[/]`. `_literal` closes
  its trailing backslash run with a tag of its own, so the merged run still parses right.

The fix order is sound. Doing the cut, then the escape, then laying the run is the same order that P3 and
TC-302 already enforce for the title column.

## New notes (LOW, non-blocking)

### SEC-6: A label 0 cells wide leaves the row one cell short  [LOW]
- **What:** a title made only of combining marks or zero-width characters (U+0301, U+200B) has `cell_len` 0.
  Step 4 then lays `cell_len − 1 = −1` consumed cells, and the run's own cell prints nothing, so the row is
  `w − 1` cells. The row comes out shorter, not wider, and nothing is injected.
- **Recommendation:** state in the LABEL PATH that a label of 0 cells is not drawn. TC-4820's assertion
  `cell_len == width` already catches this if one zero-width title is added.
- **State:** `planned`.

### SEC-7: TC-4820's cut placement cannot be reached for the short titles  [LOW]
- **What:** pass 2 cuts only when the title fits on neither side AND the roomier side has 6 cells or more.
  `x\` (2 cells), `étape` (5) and `a]b[/]` (6) are never cut at a room of 6 or more. So 3 of the 15 cases
  cannot happen as written, and the 15/15 threshold invites a vacuous count.
- **Recommendation (E4 tester):** lengthen these 3 titles so that the hostile part sits at the cut point, for
  example `review a]b[/] plan` or `abcde\[b] launch`. Then each cut case really cuts through or right next to
  the brackets or backslash. If that is not done, restate the threshold with the real count.
- **State:** `planned`.

## Round-1 non-blocking findings, as seen in `6c2891f`

These are not re-reviewed in depth.

- **SEC-2:** folded into LLR-4603.11, with the wide-glyph and combining-mark titles and NC 2.
- **SEC-3:** LLR-4602.8 now says a 2-cell mark at `w-1` starts at `w-2`. AT-4607 now covers it.
- **SEC-4:** R-6 now defines *share one cell* and *lead* once.
- **SEC-5:** TC-4843d is added.

## Verdict

- [x] **PASS-WITH-NOTES.** SEC-1's block lifts: the amended graph, SEAM-8 and TC-4820's design have been
  re-verified, as A-11 requires. SEC-6 and SEC-7 are notes for E4.
- This is a design clearance only. TC-4820 is `planned` until it runs at E4 through the real seat (A-8). This
  verdict authorises no merge or deploy, and it is not the operator's approval.

## Evidence checklist

- [x] Each finding has what · where · why · recommendation (SEC-6, SEC-7).
- [x] Each finding has a severity: 2 LOW.
- [x] No secret values appear in this report. The increment touches no secret.
- [x] The verdict is explicit: PASS-WITH-NOTES, with no HIGH open. SEC-1's mitigation is applied in the
  design and verified by the probe (24/24, NC RED).
- [x] New tool or integration: none.
