VERDICT: FAIL

# Security Review — Inc MR-a, a project's milestones share one gantt row (PDR, E3, code-free)

> security-reviewer, 2026-11-06. This is a read-only review of the Code-Wire design at `02b4a87`. I edited no
> product file.
> Counts: HIGH 1 · MEDIUM 2 · LOW 2. **SEC-1 blocks.** Its fix is an amendment to the frozen contract, not new
> code, and E4 waits for it. Every mitigation below is `planned`. None is `executed`.

## Scope reviewed

- `.dev-flow/2026-11-06-v3-incMR/`: 01-requirements.md, 00-e1-rulings.md, graph-interfaces.cw.md,
  graph-proto-V.cw.md, graph-proto-S.cw.md, e2-seams.md.
- Current code, read-only: `views.py` `c` (:75), `collapse_runs` (:789), the render seat
  `Text.from_markup(collapse_runs(...), emoji=False)` (:869), `title_markup`/`_literal` (:281), `_gantt_field`
  (:2877), `milestone_mark` (:2600), `_hide` (:3148), `filtered_board` (:4172); `app.py` selection reconcile
  (:3325-3392), `_view_board` (:4132); `marks.py` allowlists (:34-36, :142-144); `tests/test_markup_census.py`.
- Oracle: `prototypes/milestone_row/proto.py` `lane_cells`.`put` (:245-266), `lane_label` (:269).
- I measured with a probe script run from outside the worktree (`python -I`, rich + textual 8.2.8). It
  composed `c()` cells and parsed them through the real seat. The numbers are quoted in SEC-1 and SEC-2.

## Checked, no finding

- **Markup census law.** The increment adds no Textual sink in `app.py`, because `action_hmove` only writes
  `selected_task_id`. `render_view` keeps its signature (SEAM-6: no new parameter), so the two EXEMPT keys
  (`test_markup_census.py:79-85`) still name live sites. `views.py` stays outside the census (D-405), and its
  seat is Rich markup built with `escape`/`_literal`. That seat is what SEC-1 is about.
- **Label column (`gantt_lane_label`).** The title goes through `title_markup` (the escaped seat, cut by
  `fit`), and the counts and `i/N` are app text. Safe.
- **Glyphs and tones.** A class shape and colour are allowlisted on load and on edit (`marks.py:142-144`,
  `:205-208`). Because of that, `<glyph>`, `<hollow>` and the `rev:<style>` key come only from constants.
  Dates (`Mon D`), `▲Nd`, `✓`, `◂▸` and the chip are app text. The contract forbids registering HEX keys at
  run time (the prototype's `_skey`). Safe.
- **R-4, hidden classes.** The nav column (`nav_model`), the lane (`gantt_lane`) and the frame all read
  `_hide(...)` of the same board. `_hide` and `filtered_board` are `copy.copy` proxies that keep `marks`, so a
  `/` query does not drop the class filter. The gantt reconcile (`app.py:3349`, `_nav_flat`) moves a selection
  that is not in the nav column, and under R-4 a hidden milestone is never in it. The cursor cannot reach a
  hidden class's milestone. See SEC-5 for the missing pin.

## Findings

### SEC-1 — Title text in the field reaches the markup parser cell by cell, unescaped  [Severity: HIGH]
- **What:** Pass 2 of `gantt_milestone_row` writes the selected milestone's title (full, or cut with `…`) into
  the field as one `(char, tone)` cell per character. `_gantt_field` paints each cell as `c(glyph, tone)` with
  no escape. Its docstring says "every cell here is a constant glyph", and that was true until now. Neither
  the frozen contract (`graph-interfaces.cw.md` `gantt_milestone_row`) nor SEAM-7/8 says who escapes the
  title. The designated oracle (`proto.py:245` `put`) does not escape it. Escaping each character does not
  help either: `collapse_runs` merges same-style neighbours back into one run before Rich parses it.
- **Where:** `gantt_milestone_row` pass 2 → `_gantt_field` (:2886) → `collapse_runs` → `Text.from_markup` (:869).
- **Why it matters:** These probe results came from the real seat, with per-cell `c()`, escaped or not:
  - `[b]bold` draws as bold `bold`.
  - `[@click=app.quit]x[/]` is consumed as a tag that carries a `@click` meta, which is the S-1 HIGH class of
    the 2026-09-30 batch.
  - `a]b[/]` raises `MarkupError: closing tag '[/]' … has nothing to close`, so a teammate's synced title
    kills the board repaint.
  - `x\` draws `x[/]`, 2 cells wider than measured.

  When the same titles go in as one run, `c(_literal(piece), tone)` or `c(escape(piece), tone)`, all four
  round-trip exactly.
- **Recommendation:** amend the frozen `gantt_milestone_row` contract and SEAM-8 before E4:
  - A label (title or date) is one piece, escaped once as a whole with `_literal` (the codebase's rule for cut
    pieces, P3/TC-302). It is never split into per-character cells. For example: the label's first cell
    carries the escaped run and a run tone, the cells it covers are marked consumed, and `_gantt_field` emits
    the run as given.
  - `_gantt_field` keeps its constant-glyph invariant for every other tone.
  - Add a TC (e.g. TC-4825b) that sets TC-302's hostile titles as the selected milestone's title. It covers
    the after, before and `…`-cut placements, and it asserts: no exception; `plain` holds the exact title or
    its cut; no span carries `@click`/meta; the line's `cell_len` equals the width.
- **State:** `planned`. I re-verify the amended graph and the TC's design before the block lifts.

### SEC-2 — Field labels are measured with `len`, so a wide-character title widens the row  [Severity: MEDIUM]
- **What:** The oracle places and sizes labels by `len(text)`, one character per cell (`proto.py:246-262`).
  A CJK or emoji title takes 2 terminal cells per character, so the row comes out wider than `w` and the
  Static wraps it. That is the wrapped-date complaint again. The probe measured `wide中文`: `len` 6, 8 cells.
  The thresholds of LLR-4603.5 and LLR-4603.9 run only on MR-F, whose titles are ASCII, so their tests
  cannot fail on this.
- **Where:** `gantt_milestone_row` pass 2 and 3, room and placement; TC-4825, TC-4829.
- **Recommendation:** in the contract, measure room, placement and occupancy with `vis`, and cut with `fit`
  (which counts cells). Add a wide-character title and a combining-mark title to TC-4829's frames (max
  `cell_len` ≤ width, line count unchanged).
- **State:** `planned`.

### SEC-3 — A 2-cell token at the field's last cell has no stated placement  [Severity: MEDIUM]
- **What:** `<glyph>N`, `<glyph>+` and `<hollow>✓` each take 2 cells, but the contract only places them
  starting at the mark's cell. The `▸` rule covers a due after the window. It does not cover a due ON the
  window's last day (cell `w-1`), such as a reached milestone or a same-day pair there. In that case the second
  cell lands at index `w`: either an IndexError, or a row one cell too wide.
- **Where:** `gantt_milestone_row` pass 1 (LLR-4602.2–.4, .6).
- **Recommendation:** state that a 2-cell token whose mark falls at `w-1` starts at `w-2`, the same inward
  shift `▸` uses. Add the case to TC-4813 or TC-4816.
- **State:** `planned`.

### SEC-4 — A shared cell can mis-attribute its count, its date or its lateness at narrow widths  [Severity: LOW]
- **What:** Below 1 cell per day, one cell covers several days. The mark counts its members per cell
  (`■3`), but ` i/N` counts per day (`proto.py:273`: `due_date ==`), so the same cell can read `■3` and
  `1/2`. The cell's date label is the lead's alone (F-1), so `Oct 24` can stand over members due Oct 25–26.
  A late member that is not the lead shows no `▲` in the field, although the label column's `▲L` still
  counts it at rest. Board text cannot inject anything here. The risk is that the row says something untrue.
- **Recommendation:** define "share one cell" once and use it for both the count and `i/N`. When ruling F-1,
  say that the shared cell's date is the lead's. Optionally give the cell `▲` when any member is late.
- **State:** `planned`.

### SEC-5 — R-4's "selected, then hidden" path has no test  [Severity: LOW]
- **What:** The design is sound (see above), but its safety depends on the reconcile path, and no TC pins
  that. TC-4843b and TC-4843c start with the class already hidden.
- **Recommendation:** add TC-4843d. Select m3, hide Review in `#`, and assert three things: the selection
  leaves m3; `enter` and `]` do not act on m3; and neither the label column nor the ruler echo shows m3.
- **State:** `planned`.

## Verdict

- [ ] OK to ship
- [x] **FAIL — BLOCK-UNTIL: SEC-1.** The block lifts when `graph-interfaces.cw.md` names the label's escape
  seat (one `_literal` run, no per-character cells) and the hostile-title TC is in the design, and I have
  re-verified both. SEC-2 and SEC-3 are recommended before E4, and they cost little in the same amendment.
  SEC-4 and SEC-5 are notes. This verdict authorises nothing, and it is not the operator's approval.

## Evidence checklist

- [x] Each finding has what · where · why · recommendation. See SEC-1..SEC-5.
- [x] Each finding has a severity: 1 HIGH, 2 MEDIUM, 2 LOW.
- [x] No secret values appear in this report. The increment touches no secret.
- [x] The verdict is explicit: FAIL, BLOCK-UNTIL SEC-1. The one HIGH carries no applied mitigation, so it
  stays open.
- [x] New tool or integration: none. The increment adds no file I/O, no network and no dependency
  (01-requirements §1).
