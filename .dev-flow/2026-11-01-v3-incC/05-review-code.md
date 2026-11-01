VERDICT: PASS-WITH-NOTES

# Code Review — Inc C, multicolour notes (E5, code-reviewer)

## Scope reviewed
- `git diff 0a8dfaa..HEAD -- taskboard README.md tests` (commits 66e29f6, 09493fd, 7d95677): every changed line was read.
  - `taskboard/views.py` (PEN_CODES, Span, colour_spans, highlight_segments, legend_entries)
  - `taskboard/modals.py` (all Inc C units; the base mention picker and check_action arms they touch)
  - `taskboard/report_deck.py`, `taskboard/report_workspace.py`, `README.md:247`
  - `tests/test_colour_notes.py`, `tests/test_colour_palette.py`, `tests/test_colour_pens.py`, `tests/test_modal_keys.py`
- Read against: 01-requirements.md, graph-interfaces.cw.md, graph-proto-V/M1/M2.cw.md, 03-pdr-rulings.md, e4-addenda.md.
- How I ran probes: scratch pytest files in `C:\Users\jjgh8\scratch\incC-cr\`, which is outside the repo. The command was `PYTHONPATH="<wt>;<wt>/tests" env -u NO_COLOR C:/Users/jjgh8/anaconda3/python.exe -m pytest -s -o asyncio_mode=auto test_probe_cr*.py`. A probe confirmed that `taskboard.__file__` resolves to the worktree. The full suite was NOT run (not my lane); evidence state for the suite is `not-run`.

## Conformance to the graph and rulings (summary)
The implementation follows the approved graph node by node. These were checked and match:
- `colour_spans`: leftmost-first; a next opener ends a span; the `:::<c>::` case (ARCH-11); the closer takes one preceding space, never the opener's; nothing crosses `\n`; linear, with cached matches.
- `highlight_segments` is derived from `colour_spans` and has no regex of its own.
- `_unshadow_alt_digits` is guarded by A-1.
- `pen_label` uses one form ≤ 38 cells.
- `ink_highlights` uses one-pass byte offsets with surrogatepass.
- `InkArea`: its own registered theme; the fail-safe override; empty ink on a lone surrogate (R1-1).
- `_pen_span`, `_lift_pen` (ARCH-10), `action_pen` (steps 0–4, N4), `action_pen_enter` (no P-M1-9 branch), `_pen_follow` (SEC-4 guarded delete, explicit cursor shift).
- `check_action`: one gated arm, `pen_enter`; `pen` and `colour` are always allowed (ARCH-2).
- `colour_target` / `_word_at` (ARCH-4), `palette_offset`, `ColourPalette` (keys only), `_apply_colour` (SEC-5 re-validation, then the visible-text check).
- `DETAILS_NOTES_LABEL` (C-2/A-2), the deck and workspace CSS, the INVENTORY row, and the README sentence.

One divergence was found: CR-4.

## Regression checks (no defect found)
- **Mention picker under a pen (probe Q1):** I typed `@an` with pen `b` on, then pressed `enter`. `drop_pick` wins and writes `::b:: ask @ana.ruiz  ::` with the pen still on. A second `enter` takes the `pen_enter` arm, and `tab` moves to `#f-urls`. Evidence state: `executed`.
- **`enter` and `up`/`down`/`tab`:** `drop_move`/`drop_pick`/`drop_field` keep their base arms. The `drop_*` body moved into `_drop_gate()` unchanged. With no pen, `enter` still falls through to the field's newline (TC-4237 and the base TC-2503 example).
- **`alt+s`/`m`/`i`/`t`/`d`:** the bindings are untouched. `alt+c` was free in `TaskModal`; MarkForm's `alt+c` sits on a different screen.
- **Modal-key law:** `ColourPalette` has no `Button(` and is added to INVENTORY (`tests/test_modal_keys.py:288`).
- **Undo after a pen (probe P5):** `alt+5 a` then `ctrl+z` gives `x::b::  ::` with the pen on. A second `ctrl+z` gives `x` with the pen off. Clean.

## Findings

### CR-1 [MEDIUM] [design-gap] A legacy closer typed under a pen pairs with an earlier `==` and swallows the pen's span
- **Where:** `taskboard/views.py` `colour_spans` (the starts-first rule, LLR-4201.7) as reached from `taskboard/modals.py:955` `action_pen` / `:1001` `_pen_follow`. LLR-4203.2 lists only `::` as an exception.
- **Evidence (probe R1, pilot):** notes `if a == b`, cursor at the end, `alt+5`.
  - The SEC-2 check passes: `if a == b::b::  ::` with pen 4.
  - Then I typed ` then c == d`.
  - Actual: `'if a == b::b::  then c == d ::'`, pen `None`, segments `[('if a ','mut'), (' b::b::  then c ','soon'), (' d ::','mut')]`.
  - The blue is gone, the opener and closer show as text, and ` d` lands outside the span.
  - Expected under LLR-4203.2: every typed character stays blue inside the pen's span.
- **Why it matters:** technical notes hold `==` (comparisons) often. The SEC-2 / LLR-4205.15 invariant is checked only at the moment of insertion, never while the user types under the pen. The pen then turns off silently, because its span vanished.
- **Smallest fix:** rule it "as designed", like P-M1-5. Add a README sentence ("a `==`, `!!` or `++` typed under a pen can pair with an earlier one and end the pen") and one pinning test. If the operator wants a guard instead: in `_pen_follow`, when `_pen_span()` is None but `_pen_at` still holds the literal opener text `::<code>::` at `start0`, notify N4 once.

### CR-2 [MINOR] [design-gap] A multi-line paste under a pen leaves the next line's closer literal
- **Where:** `taskboard/modals.py:335-347` `action_paste_text` (`target.insert(text)`); no pen handling exists (LLR-4203.7 covers only `enter`).
- **Evidence (probe Q2, pilot):** `grab_clipboard_text` monkeypatched to return `"ab\ncd"`, then `alt+5` and `ctrl+v`.
  - Actual: `'::b:: ab\ncd ::'`, pen `None`; line 2 tokenises `[('cd ::','mut')]`.
  - Expected (by analogy with LLR-4203.7): `::b:: ab ::\n::b:: cd ::`.
- **Smallest fix:** while a pen is on and `_pen_span()` holds the cursor, have `action_paste_text` replace each `\n` in the pasted text with ` ::\n::<code>:: ` before inserting. Otherwise record it as a known limit in the README.

### CR-3 [MINOR] [design-gap] `_lift_pen` ignores `_pen_at`, so a lift that runs before the leave's SelectionChanged orphans the empty span
- **Where:** `taskboard/modals.py:926-936` (`if s is None:` only sets the pen to None). Its callers are `_save` (`:1293`), `action_pen` on a switch (`:974`) and `action_colour` (`:1043`). The ARCH-8 race fix lives only in `_pen_follow`.
- **Evidence:**
  - Probe P2, deterministic: notes `x`; `scr.action_pen(2)`; `ta.move_cursor((0,0))`; `scr._save()`. Saved notes are `'x::y::  ::'`. Expected `'x'` (LLR-4203.11 / .14).
  - Probe P3b: the same, then `scr.action_pen(4)`. The result is `'::b::  ::x::y::  ::'`; the empty `y` span is orphaned.
  - Reachability is only partly shown. A driver burst of `alt+3, home, alt+s` (P1) saved `'x'`, so the save path was NOT reproduced through key events.
  - A burst of `alt+3, home, alt+5` (P3) did show key reordering: the result was `'x'` with pen `None`, and the user's `alt+5` was lost. The priority binding ran before the TextArea handled `home`.
- **Smallest fix:** in `_lift_pen`, when `s is None`, run `_pen_follow`'s guarded `_pen_at` delete (branch (a)) before `pen = None`. One shared private helper serves both callers. Evidence state: P2/P3b `executed` (direct calls); P1 `executed` (not reproduced).

### CR-4 [MINOR] [impl] `recolour` never raises the ValueError its docstring and graph contract promise
- **Where:** `taskboard/modals.py:638-651`; the graph-proto-M2 `recolour` node says "It raises ValueError only on a target that partly overlaps a span".
- **Evidence (probe P7, pure):** `recolour("::b:: ab :: cd", 7, 13, "r")` returns `('::b:: a::r:: b :: c ::d', 22)` with no exception. That is a nested, corrupt line. The defect cannot be reached today, for two reasons: `colour_target` never hands back such a target, and `_apply_colour`'s visible-text check would refuse it.
- **Smallest fix:** after the `s` lookup, add `if any(a < sp.end and b > sp.start for sp in colour_spans(line)): raise ValueError("target overlaps a span")` on the plain path. Alternatively, delete the sentence from the docstring and the graph.

### CR-5 [MINOR] [impl] Duplicated invariant and notice strings
- **Where:**
  - The visible-text check is written twice: `modals.py:981-982` and `:1075-1076`.
  - `"Pens write new text…"` is written twice (`:964`, `:970`).
  - N3 is written twice (`:583`, `:1048`), and N4 twice (`:983`, `:1077`).
  - `colour_target` calls `colour_spans(line)` and then `_word_at` calls it again on the same line (`:600`, `:607`).
- **Why it matters:** the graph calls this "the one visible-text check". Two copies can drift, and a notice reworded in one place is missed in the other.
- **Smallest fix:** add `def _visible(line): return "".join(s for s, _ in highlight_segments(line))` and module constants `N1`..`N5` / `NOTICE_PEN`. Pass the spans into `_word_at`.

### CR-6 [MINOR] [impl] Convention nits
- `modals.py:619`, `:629`: the loop variable `re` shadows the imported module `re` inside `_word_at`. It is harmless today, but a trap for the next edit. Rename it to `re_` or `rend`.
- `views.py:3671`: the `_highlight_markup` docstring still says "Render ==text== (yellow), !!text!! (red), ++text++ (green)". It now renders the six colour codes too. Update it, as was done for `highlight_segments`.

### CR-7 [MINOR] [design-gap] Tests assert Textual privates beyond the P-M1-7 guard, because the thresholds name them
- **Where:**
  - `tests/test_colour_pens.py:858`: `assert not any(ta._highlights.values())` (LLR-4204.9: "the highlight map is empty").
  - `tests/test_colour_pens.py:883`, `:891-892`: `_theme.syntax_styles` (LLR-4204.6).
- **Why it matters:** these arms break on a Textual upgrade that keeps the behaviour, and P-M1-7 ruled ONE guard test for that. The same tests already carry cell-based arms that encode the intent: `x` not blue, and the URLs field paints no blue.
- **Smallest fix:** amend LLR-4204.6/.9 to observable thresholds (rendered cells). Keep the private reads only in `test_P_M1_7_…`.

### CR-8 [MINOR] [impl] A graph example of TC-4251 has no test
- **Where:** graph-proto-M1 `InkArea._build_highlight_map`, example "(TC-4251) `InkArea._line_cache` deleted before an edit → the edit lands, the field shows plain text, 0 uncaught exceptions". `tests/test_colour_pens.py:894` covers only the `colour_spans`-raises arm.
- **Why it matters:** the except-path's own fallback, which calls `super()._build_highlight_map()` on renamed privates, is never exercised. If that fallback itself raises, nothing catches it.
- **Smallest fix:** add the second arm: `del ta._line_cache` (or monkeypatch `_highlights` to an object without `.update`), type `y`, and assert that the text changed and the screen is still `TaskModal`.

## Counts
MAJOR 0 · HIGH 0 · MEDIUM 1 (CR-1) · MINOR 7 (CR-2..CR-8). impl: 4 (CR-4, CR-5, CR-6, CR-8) · design-gap: 4 (CR-1, CR-2, CR-3, CR-7).

## Evidence checklist
- ✓ Diff read in full. The diff covers views.py:3501-3611 and 8819-8824, modals.py:15-78, 481-727, 737-747, 768-771, 843-848, 905-1110, 1290-1293 and 3006-3009, report_deck.py:379-440, report_workspace.py:14-90, README.md:247, and the three new test files.
- ✓ Correctness pass: 20 tokeniser edge inputs probed (probe_pure.py); pen, picker, paste, undo, race and recolour probes run (CR-1..CR-4).
- ✓ Simplicity pass: no speculative abstraction; the duplication is noted (CR-5).
- ✓ Reuse: one scanner. `highlight_segments`, `ink_highlights`, `_word_at`, `colour_target`, `recolour` and `action_pen` all read `colour_spans`; there is no second regex.
- ✓ Tests reviewed for intent: no vacuous asserts found. The NC arms are real (TC-4240/4284 post the terminal's printable event; TC-4249 has a read-only-table arm with a read counter; TC-4245 and TC-4209 use an independent reference scanner; AT-4204 uses a frozen base oracle). Gaps: CR-7, CR-8.
- ✓ Verdict explicit; no HIGH open.

## Evidence states
- Probes R1, Q1, Q2, P1–P8, probe_pure: `executed`.
- Full suite: `not-run` (qa-reviewer's lane).
- Real Windows Terminal key path (ARCH-14): `not-run` (not my lane).

## §4b `Independent review` cell (for the orchestrator)
`code-reviewer` · OK to advance (PASS-WITH-NOTES) · no HIGH raised; 1 MEDIUM (CR-1 legacy `==` typed under a pen swallows its span, design-gap: rule or README+test) and 7 MINOR (CR-2..CR-8) recommended, none blocking.
