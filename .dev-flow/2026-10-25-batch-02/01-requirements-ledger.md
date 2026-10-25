# Requirements ledger — taskboard — Batch 2026-10-25-batch-02

> Append-only. Entries are added in chronological order and never rewritten. The live
> contract is `01-requirements.md`; this file records how it came to say what it says.
> Every entry names the requirement it amends; every requirement names its entries. `V26`
> compares the two sets of pairs both ways.

### LED-2901 — the IFC gains the _paint_marks node; the changing LLRs declare their symbols
- **Date:** 2026-10-25
- **Requirement:** LLR-2901.1, LLR-2902.1
- **Amends:** IFC Part A node list; LLR-2901.1, LLR-2902.1 statements
- **Reason:** Phase-2 round-1 majors A1 (the IFC omitted `_paint_marks`, a symbol the fix changes — the P3 reverse census keyed on Part A would have missed it) and A2 (C-26 asks each changing LLR to declare its touched symbols; the LLRs named only symbols that stay unchanged). Folded by iterate-to-refine, P1 iteration 1.
- **Content:** Part A gains the `_paint_marks` node (owner LLR-2901.1, LLR-2901.2); LLR-2901.1 declares `present_note_lines`, `_present_note_markup`, `_paint_marks`; LLR-2902.1 declares `_present_cut`.

### LED-2901.2 — the escape seats, the close-tag payload, the ANSI pin
- **Date:** 2026-10-25
- **Requirement:** LLR-2901.2
- **Amends:** LLR-2901.2 statement, executed verification, threshold; §6.3
- **Reason:** Phase-2 round-1 security minors 1-3, 5: the `k == 1` cut path composes plain text today and is the seat where the escape could be dropped; the hostile payload set lacked the unbalanced close tag `[/]` (which raises MarkupError unescaped); the ANSI payload's fate was unasserted; §6.3 claimed no open residual while the control was still planned.
- **Content:** the cut path is named an escape seat; `a [/] b` joins the hostile note asserting literal rendering with no exception; the pin is 0 `\x1b` bytes in the painted row (restated to the observed replacement glyph only if the P3 probe shows one); §6.3 records the arms as P3-minted, execution owed at the increment gate.

### LED-2901.3 — editorial: the rose collision, the marker-run predicate, the per-arm negative control
- **Date:** 2026-10-25
- **Requirement:** HLR-2901, HLR-2902, HLR-2904, LLR-2901.2
- **Amends:** §1.3 definitions; HLR-2901 threshold; HLR-2902 negative control; HLR-2904 threshold and negative control
- **Reason:** Phase-2 round-1 minors A3 (the word "rose" collides with the HEX key `rose` = `#fb7185`, a different colour), Q3 ("marker characters in marker positions" is not a mechanical predicate), Q4 (two of AT-2904's three arms hold at base_ref by design — the negative control must say which arm has an executed P1 red), Q6 (the evidence paraphrase said `word ==tail==`; the bytes say `word word ==tail==`).
- **Content:** §1.3 drops "rose"; AT-2901's predicate is "no run of `==`, `!!`, `++`" with fixtures free of literal `= ! +`; HLR-2904's negative control names the per-arm red sides; HLR-2902 quotes the evidence verbatim.

### LED-2903 — the PNG limb scoped; the SVG escape assertion
- **Date:** 2026-10-25
- **Requirement:** HLR-2903, LLR-2903.1
- **Amends:** HLR-2903 statement, boundary catalog, threshold
- **Reason:** Phase-2 round-1 minors Q2 (the statement promised PNG parity the threshold never asserts — PNG rendering is Edge-dependent) and S4 (the SVG sink's HTML-escaping was inherited analysis, not evidence).
- **Content:** the PNG limb is scoped to where the headless Edge renderer exists, else `n/a — no Edge`; AT-2903 asserts the exported SVG escapes `<`, `&`, `<script>` (0 raw `<script` bytes) from a hostile note.

### LED-2905 — the named oracle casualty and the style pin
- **Date:** 2026-10-25
- **Requirement:** HLR-2905
- **Amends:** HLR-2905 statement and threshold
- **Reason:** Phase-2 round-1 major Q1 (the known-in-advance oracle casualty was not named: `tests/people_round_fixture.py` holds `++sign-off by the sponsor++` in task c5's notes and `tests/test_people_look.py:182-186` asserts the split frame's `.plain` — after the fix that frame loses the `++`) and minor Q7 (the existing byte oracles compare `text.plain` only; a style-only regression on marker-free rows would stay green).
- **Content:** `test_people_look.py` is the named, expected update with a P3 re-scan owed; a new arm pins a pre-existing marker-free cursor-note row at `#e6edf3`; the exact baseline integer is executed at P3 (3 chunks) and pinned in `04-validation.md` for the P4 comparison.

### LED-2905.1 — the casualty claim corrected: c7, not c5, and no marker-keyed oracle exists
- **Date:** 2026-10-25
- **Requirement:** HLR-2905
- **Amends:** HLR-2905 statement
- **Reason:** Phase-2 round-2 major R2-1 — LED-2905 named test_people_look.py as the expected oracle casualty on both a wrong task id (c5; the `++` note is task c7's N_EVAL, c5 holds N_GOLDEN's `!!…!!`) and a wrong oracle kind (the test asserts mention membership, not marker bytes — it stays green; no test asserts any marker string)
- **Content:** the contract now states the grep-verified absence and owes the casualty list to the P3 census + suite run. Folded by iterate-to-refine, P1 iteration 2.
