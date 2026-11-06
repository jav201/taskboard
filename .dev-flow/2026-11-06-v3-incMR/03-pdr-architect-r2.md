# E3 PDR round 2 — architect — Inc MR-a

> Reviewer: architect (Opus), read-only. Tree: `ms-row-proto` at `6c2891f`. Scope: what was blocking in
> `03-pdr-architect.md`, plus any new defect the correction brought in. Read: `git show 6c2891f`, R-6..R-8 in
> `00-e1-rulings.md`, `views.py` 75-108, 280-312 and 2877-2895, and `proto.py` 70-99 and 207-240.
> Ran: `codewire_lint.py` on the 3 graphs and `trace_check.py --req 01-requirements.md`. No product test was run.

**Verdict: PASS-WITH-NOTES.** 0 MAJOR open (5 of 5 closed), 3 new MINOR findings (N-8..N-10). None of them
blocks E4.

## 1. The blocking findings

| Finding | Ruled | State | Evidence |
|---|---|---|---|
| F-1 shared-cell date, day vs cell | R-6 | closed | §1 adds *share one cell* and *lead*. LLR-4603.3, .4 and .7 restated. TC-4823 dates `■2` by its lead m3. LLR-4602.2's glyph rule matches *lead* |
| F-2 h1 hue | R-6 | closed | LLR-4602.1 threshold and TC-4811 read `mut` (the seat) |
| F-3 unreachable `▸` | R-6 | closed | LLR-4602.6, AT-4607 and TC-4816 use a reached milestone 90 days ahead, `<hollow>✓▸`. The drawn cell is the bucket (`<glyph>2▸`). A-1 sends it through `render_gantt` and adds the `ctx` caveat |
| F-5 dependency gutter | R-6 | closed | LLR-4601.8 (TC-4808) is cited by AT-4601. `task_row` adds no `waits` or `early`. A-3 re-baselines `↳` and lists the loss in the packet |
| N-1 markup and width in the field | R-7 | closed | LABEL PATH in `graph-interfaces` runs in this order: cells, `fit` on the PLAIN text, `_literal` once and whole, then one run plus `""` consumed cells. The edges are `fit → _literal → [Data: field label run] → _gantt_field`. `_gantt_field` paints `""` as `c("", tone)`, which prints nothing (`views.py:2887-2888`). `_literal` closes a trailing backslash with `[none]…[/none]` (`views.py:308-311`), so a joined neighbour run stays safe. `fit` cuts on a glyph boundary in cells (`views.py:95-104`) |

F-4 and N-2..N-7 were adopted under R-6 and R-8 and are in §6, the graphs or `e3-addenda.md`. Each was checked
present.

## 2. The new LLRs (EARS, threshold, negative control)

| LLR | Form | Threshold | NC | TC |
|---|---|---|---|---|
| 4601.8 | Ubiquitous ✓ | 4/4 gutters blank; no `waits` or `early` from a milestone row ✓ | draw the stop's `↳` → RED ✓ | TC-4808, by the rule |
| 4602.8 | Unwanted ✓ | `w-2`–`w-1`, row exactly `w` cells, 0 exceptions, 2/2 ✓ | start at `w-1` → IndexError or `w+1` cells → RED ✓ | TC-4818, by the rule |
| 4603.11 | Unwanted ✓ | 5 titles × 3 placements, 15/15, 0 exceptions, no `@click` or meta span ✓ | per-character `c()` → `MarkupError`; `len` measure → line too wide ✓✓ | TC-4820, a recorded exception (LED .5); the slot is free |

## 3. Trace and lint

- **Lint:** `not read=0` on all three graphs (interfaces 2 nodes, V 6, S 2). `executed`.
- **Trace:** `e2-trace.txt` holds 50 of 50 (43 LLR + 7 AT). The requirements file has 43 LLRs and the trace
  names 43 distinct LLRs. `trace_check.py`: 1 US, 50 active, 0 withdrawn. Its 52 gaps are 50 `TEST`, 1 `CASE`
  and 1 `EVID`. All of them are artifacts that E4 and E5 produce, so none is a design gap. `executed`.

## 4. New findings (MINOR, E4 addenda)

- **N-8: a two-cell mark can overwrite a neighbour.**
  - LLR-4602.8 moves a 2-cell mark back to start at `w-2`. If a lone mark already sits at `w-2`, the oracle
    overwrites it (`proto.py:230-232`, `x0 = min(x, W - len(seq))`). That contradicts LLR-4602.1, which
    draws each mark in its cell.
  - The same clash exists for any `<glyph>N` or `<hollow>✓` whose second cell is the next mark's cell, and
    for `◂<hollow>✓` over an in-window mark at cell 1 or 2. I missed this case in round 1.
  - **Fix:** a TC case per collision (the two marks at `w-2` and `w-1`, and two adjacent cells). The rule is
    one sentence in `gantt_milestone_row`: a member whose cell falls inside an earlier mark's footprint joins
    that bucket. This follows the drawn-cell rule of F-3.
- **N-9: the weekend ground under a label run.**
  - The board gantt passes `weekends` (`views.py:3312`), and `_gantt_field` applies `_on_weekend` per cell
    index (`views.py:2893`).
  - A single run sitting in its first cell takes that cell's ground across all the cells it covers. The
    covered cells lose their own ground, or gain one they should not have.
  - **Fix:** split the PLAIN cut piece at ground boundaries and `_literal` each segment as a whole. Joined
    `_literal` outputs stay safe (see F-1, N-1 above). The alternative is to accept the loss and tell the UX
    reviewer. It is cosmetic.
- **N-10: two threshold details.**
  - LLR-4603.11 asks for every line's `cell_len` to EQUAL the frame width, while LLR-4603.9 asks only for
    ≤ width. That holds only if every frame line is padded, which I have not checked (`not-run`). **Fix:**
    assert `=` on the milestone row and `≤` on every other line.
  - LLR-4601.8 needs m3 to wait on `store`, but MR-F has no dependency (`proto.py:79-99`). **Fix:** the
    tester builds the MR-F variant, and the NC must show base drawing `↳` on it.

## 5. PDR §A checklist (round-2 delta)

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | Proposal complete | ✓ | F-1, F-2, F-3, F-5 and N-1 closed (§1) |
| 4 | Every requirement has foreseen coverage | ✓ | 50/50, lint 0 (§3) |
| 5 | Test cases observable and non-vacuous | ✓ | 3 new LLRs each with a threshold and an NC (§2); N-8 and N-10 add cases |
| 7 | Frozen interfaces listed | ✓ | SEAM-7 narrowed to `gantt_milestone_row`, and `gantt_lane_label` moved to V (N-6) |
| 10 | Security lens | ⚠ | the structure is sound (§1 N-1); A-11 leaves the SEC-1 lift to the security reviewer |

Rows 2, 3, 6, 8 and 9 have not changed since round 1.

**Verdict: PASS-WITH-NOTES.** N-8, N-9 and N-10 ride to E4 as addenda.
