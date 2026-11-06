VERDICT: PASS-WITH-NOTES

# Security Review, E5: Inc MR-a implementation (`154e260..8e3272e`, `taskboard/`)

> security-reviewer, 2026-11-06. This review is read-only. I edited no product file.
> Counts: HIGH 0 · MEDIUM 0 · LOW 2 (1 `impl`, 1 `design-gap`). **Nothing blocks.**

## Scope reviewed

- The diff `git diff 154e260 8e3272e -- taskboard/`, which touches `app.py` (`action_hmove`, import) and
  `views.py` (`gantt_plan` lanes and `_hide` seat, `gantt_lane`, `_lane_marks`, `gantt_milestone_row`,
  `gantt_lane_label`, `_gantt_field` run and `rev:` paths, `_gantt_frame` lane row and `line_map`).
- The design reports `03-pdr-security.md` (SEC-1..5) and `03-pdr-security-r2.md` (SEC-6, SEC-7).
- I probed the real render seat, `render_gantt` (`collapse_runs` → `Text.from_markup(…, emoji=False)`). The
  scripts were in `.scratch/`, run with `python -I` against the worktree's `taskboard`, and the folder is now
  deleted. I also ran the existing tests: TC-4820, the TC-484x tests and the markup census gave 33 passed,
  0 failed.

## Verification

| Check | Result | Evidence (`executed`) |
|---|---|---|
| SEC-1 / R-7: hostile titles reach Textual escaped | ✓ | I ran 11 titles × 7 due offsets (edge-left to edge-right) × widths 118 and 80, **154 renders**. The titles were `a]b[/]`, `[@click=app.quit]x`, `\`, `[bold]`, `里程碑审查会议`, a 300-char title mixing `[b]`/`\`/`[@click…]`, `]`, `[`, `中`, `review a]b[/] plan go` and a 0-cell title. Results: 0 exceptions, 0 spans carrying meta or link, and every rendered line exactly `W` cells. Where the field draws the title, it is the exact title or a `fit` cut ending in `…`. The label column always holds the exact title or its cut. |
| Nothing unescaped goes into cells | ✓ | `put_label` (views.py, pass 2/3) is the only writer of label text. It runs `fit` on the plain text, then `_literal` once on the whole piece, then puts one run plus `""` cells. Dates, `▲Nd`, `✓`, counts and `◂▸` are app text. Glyphs and `rev:<style>` come from allowlisted `milestone_mark` constants. `gantt_lane_label` uses `title_markup` (escaped). |
| Field title left out in 12/154 renders | by design | The roomier side had fewer than 6 cells (LLR-4603.2), and the label column still carried the title. This is not an escape gap. |
| SEC-6: a 0-cell label leaves the row at the field width | ✓ | `gantt_milestone_row` → `_gantt_field` → parse gives `cell_len == ax.w` (79 at 118, 52 at 80) for `U+0301 U+200B`, `U+200B`, `U+0301`, `a+U+0301` and `中`. The guard is `put_label` `if n <= 0: return`. |
| R-4: no hidden-class milestone is reachable or revealed | ✓ | I hid Review on MR-F. At 118 and 80, with m3, m2, m4 or store selected: neither "Steering go/no-go" nor "Rubric sign-off" appears in the plain output, and `tm2`/`tm3` are absent from `line_map`. `gantt_lane(…, "tm3")` is `()`, the lane of `tm4` is `[tm1, tm4, tm5]`, and the plan lanes hold no Review id. `gantt_plan(done_rows=True)` applies `_hide` itself (N-5), so `action_hmove` → `gantt_lane(_view_board())` can only walk filtered ids. The TC-4842 and TC-4843* keypath tests pass. |
| New sinks, I/O, deps, secrets | none | The diff adds no Textual sink in `app.py`, no file or network I/O, no dependency and no secret. |

## Findings

### SEC-8: The 0-cell guard (SEC-6) is not pinned by any test  [Severity: LOW] [`impl`]
- **What:** the guard `put_label` `if n <= 0: return` works (probe above). But TC-4820's `DANGER` set has no
  0-cell title, and the "SEC-6" note on TC-4822 covers the no-room case, not a 0-cell label. If the guard is
  removed, the 0-cell piece lands in a 1-glyph cell and draws 0 cells, so the row comes out `w-1` cells. I
  expect no current test to fail in that case. I inferred this and did not run the mutation.
- **Where:** `views.py` `gantt_milestone_row.put_label`; `tests/test_milestone_row.py` TC-4820 `DANGER`.
- **Recommendation:** add `"​"` (or `"́​"`) to TC-4820's titles, or add a TC-4822 variant that
  asserts the field's `cell_len == ax.w`. Then confirm it goes RED with the guard removed.
- **State:** `planned`.

### SEC-9: `_gantt_field` tells an escaped run apart by `len(glyph) > 1`  [Severity: LOW] [`design-gap`]
- **What:** a cell whose glyph has more than one character is painted as already escaped, and a 1-character
  label goes down the constant-glyph path without being escaped. That is safe today: `_literal` turns every
  character that needs escaping (`[`, `\`) into 2 or more characters, and the probe drew `]`, `[` and `中`
  literally. But the invariant is implicit. A future row builder that puts a raw multi-character string
  into cells would skip escaping without any error.
- **Where:** `views.py` `_gantt_field` (`if len(glyph) > 1`).
- **Recommendation:** mark label runs explicitly, for example with a tone prefix such as `run:` or a
  sentinel, the same way `rev:` is marked. Or add the rule "only `put_label` may emit multi-character
  glyphs" to the docstring and the markup census. This is not required for MR-a.
- **State:** `planned`.

Notes from the design rounds: SEC-1 is closed in code (`executed`, re-verified above). SEC-2 (wide glyphs)
and SEC-3 (a 2-cell mark at `w-1`) gave no over-wide line in 154 renders. SEC-7 is covered by the `LONG`
titles in TC-4820.

## Verdict

- [x] **PASS-WITH-NOTES.** There is no HIGH or MEDIUM finding. SEC-1's mitigation is applied, and I verified
  it on the real seat. SEC-8 and SEC-9 are LOW notes, and neither blocks.
- This is a security clearance only. It authorises no merge or deploy, and it is not the operator's approval.

## Evidence checklist

- [x] Each finding has what · where · why · recommendation (SEC-8, SEC-9).
- [x] Each finding has a severity and a tag: 2 LOW, one `impl` and one `design-gap`.
- [x] No secret values appear in this report. The diff touches no secret.
- [x] The verdict is explicit: PASS-WITH-NOTES, with no HIGH open.
- [x] New tool or integration: none.
