# Inc C — rulings (orchestrator, Opus)

> Every proposal from the prototype groups (E2) and the design review (E3) gets one ruling here.
> Bias: prefer removing a feature over guarding it. Ids: P-V-n, P-M1-n, P-M2-n (E2), then the PDR ids.

## Round 0 — E2 prototype findings and seams (2026-11-01)

| Id | Proposal | Ruling | Applied in |
|---|---|---|---|
| P-V-1 | orange sits 51 RGB from `soon` (inside the retired band); b/v are also project hues | **Keep** `HEX["orange"]`, `blue`, `violet` for note text. The palette-ration bands govern *project* hues on the board; a note tone is read with its name in the legend/pen chip, and the 256-colour numbers stay distinct (209 vs 214). No new HEX key. | rulings only |
| P-V-2 | LLR-4201.7 contradicts LLR-4201.6 | **Accept.** LLR-4201.7 reworded: markers inside a legacy span, and legacy markers inside a colour span, stay literal. | 01-requirements, LED.3 |
| P-V-3 | HLR-4206 says 0.15, LLR says 0.20 | **Accept.** HLR text: 0.15 is the cliff, 0.20 the gate. | 01-requirements, LED.3 |
| P-V-4 | `::b:: std::vector ::` closes at `std::` | **Accept as designed**; pinned by TC-4227; README sentence. | graph V, README |
| P-V-5 | TC-4213/4215 used by the interface file | **Rename** the interface's `_lift_pen` examples to TC-4258, TC-4259 (M1 range, free). | graph-interfaces |
| P-V-6 | focus legend shows syntax whenever a task is pinned | **Backlog** (base behaviour, not this increment). | BACKLOG |
| P-V-7 | focus snippet clips the raw line (markers eat width) | **Backlog.** | BACKLOG |
| P-M1-1 | ink should paint legacy spans too | **Accept.** LLR-4204.1/.2 say "span" (colour or legacy). | 01-requirements, LED.3 |
| P-M1-2 | enter gate = "picker offers no pick" | **Accept.** LLR-4203.7 reworded. | 01-requirements, LED.3 |
| P-M1-3 | `alt+n` inside an existing span or over a selection corrupts | **Remove the case:** if the pen is off and the cursor is inside a span (start < col < end) or the selection is non-empty, `alt+n` inserts nothing and notifies `Pens write new text — use alt+c to recolour.` New LLR-4203.12 (inside a span), LLR-4203.13 (selection). No "continue in span" feature. | 01-requirements, graph M1 |
| P-M1-4 | leaving an empty pen span leaves `::y::  ::` | **Accept.** New LLR-4203.14. | 01-requirements, graph M1 |
| P-M1-5 | typing `::` under a pen closes the span | **Accept as designed**; LLR-4203.2 states the exception; README sentence. | 01-requirements |
| P-M1-6 | the column is 39, not 37 | **Accept** (measured from tcss). Narrow form ≤ 38. | graph M1 |
| P-M1-7 | live ink rests on 3 Textual privates | **Accept guard tests** (one test that fails if `TextArea._build_highlight_map`/`_highlights`/`_line_cache` change shape). Pinning Textual in pyproject → **backlog** (out of scope). | tests, BACKLOG |
| P-M1-8 | same pen key while that pen is on | **Accept:** changes nothing. New LLR-4203.15. | 01-requirements |
| P-M1-9 | enter at the inner start moves the whole span down | **Reject** (special case for a cosmetic empty span; the general LLR-4203.7 path is enough). Remove the `col == s.inner_start` branch from `action_pen_enter`. | graph M1 |
| P-M1-10 | `_lift_pen` uses `_pen_span`; no span → only pen=None | **Accept.** | graph-interfaces |
| P-M2-1 | a selection holding a whole span plus other text | **Accept:** LLR-4205.11 → "overlaps a span without lying inside it" (refuse). | 01-requirements, LED.3 |
| P-M2-2 | rewrite that would change the visible text (`std::vector`, `==a::b==`) | **Accept** as a single invariant check: if the visible text (joined segments) of the line after the rewrite differs from before, change nothing and notify. New LLR-4205.15. | 01-requirements, graph M2 |
| P-M2-3 | a whitespace-only selection = nothing to colour | **Accept** (LLR-4205.12 amended). | 01-requirements |
| P-M2-4 | "unchanged" reference point | **Accept:** compared with the notes at the moment the palette opened (after the lift). LLR-4205.7/.8 amended. | 01-requirements |
| P-M2-5 | details label: drop the legacy listing | **Accept.** The label lists the six codes only; legacy notes still render. | graph M2 |
| P-M2-6 | M1 and M2 both edit `check_action` | **Accept:** `TaskModal.check_action` moves into graph-interfaces with ONE notes-focus gate for `pen`, `pen_enter`, `colour`. New LLR-4205.16 (alt+c without notes focus changes nothing). | graph-interfaces |
| P-M2-7 | example `"a:::b:: plan ::"` | **Accept.** | graph V |
| P-M2-8 | unlisted palette keys do nothing; recolour inside a span recolours the whole span | **Accept as decisions.** | rulings only |
| P-M2-9 | measure for "next to the target" | **Accept:** box top row = anchor row + 1, or box bottom row = anchor row − 1 when it would not fit below. LLR-4205.13 amended. | 01-requirements |

**Seams fixed by the orchestrator (graph-interfaces.cw.md):** `colour_spans`, `Span`, `PEN_CODES` (V → M1, M2);
`_lift_pen` and `_pen_span` (M1 → M2); `TaskModal.check_action` (shared, one gate); the Notes label carries
`alt+c` (M1 renders, M2's key).

### Round 0 addendum — after the correction pass

| Id | Point | Ruling |
|---|---|---|
| C-1 | at leave time `_pen_span()` is None, so `_lift_pen` cannot remove the empty span (LLR-4203.14) | **Accept the correction agent's seam:** `_pen_follow` removes the empty span itself from `[Data: TaskModal._pen_at]` (where the pen's span was before the move), with the cursor shift it describes (TC-4256, TC-4257). LLR-4203.14 leaves `_lift_pen`'s req. |
| C-2 | details label reduced to `Notes  r o y g b v` | **Partly undo:** keep the syntax hint — `Notes  ::c:: … ::  r o y g b v`, each code letter in its tone (≈ 30 cells, fits the 56-cell box). Legacy listing stays dropped. E4 addendum. |
| C-3 | notice N4 generalised to "That colour would change the text you see: nothing changed." | **Accept.** |

## Round 1 — PDR (architect FAIL: 1 MAJOR, 2 HIGH, 4 MEDIUM, 6 MINOR; security PASS-WITH-NOTES: 3 MEDIUM, 6 LOW)

**Orchestrator probe for ARCH-1 (executed):** in Windows Terminal 1.24.12741.0 a script wrote `CSI ? u` (kitty
flags query) then `CSI c`; the terminal answered only the DA (`evidence/wt-kitty-query.log`:
`'\x1b[?61;4;6;7;14;21;22;23;24;28;32;42;52c'`). No kitty protocol, so `alt+5` arrives as `ESC 5`, which
Textual 8.2.8's table (`_ansi_sequences.py:384-394`) turns into `∞`. ARCH-1 is real. Key injection into the
window (SendKeys/keybd_event) delivered nothing on this desktop, so the end-to-end key path is proven at the
parser level only.

| Id | Ruling |
|---|---|
| ARCH-1 MAJOR | **Accept; keep the operator's keys.** At import, modals.py removes the seven entries `"\x1b0"`..`"\x1b6"` from `textual._ansi_sequences.ANSI_SEQUENCES_KEYS` (they exist only for WezTerm-on-macOS Option-digit glyphs), so `ESC <digit>` takes the parser's generic alt path → `Key("alt+5", "5")`, as `alt+s` does today. Alternatives rejected: glyph aliases (`¡`, `º` are typed on Spanish keyboards), alt+letter pens (`alt+b` = `ESC b` = ctrl+left; breaks the r-o-y-g-b-v mnemonic and the operator's verdict). Trade-off recorded: a macOS WezTerm user's Option+digit no longer types `∞`. New LLR-4203.16 (parser level). |
| ARCH-2 HIGH | **Accept.** `check_action` allows `pen` and `colour` always; the actions return early (consuming the key) when `#f-notes` lacks the focus. Only `pen_enter` stays gated. Tests post `events.Key("alt+c", "c")` / `Key("alt+5", "5")`. |
| ARCH-3 HIGH | **Accept.** `action_colour` reads `_pen_span()` BEFORE `_lift_pen()`; a non-empty pen span is the target (its inner range); an empty one is removed by the lift and the call ends with the "nothing to colour" notice. Example `::b:: go ::now` added. |
| ARCH-4 | **Accept** the architect's fix (word = non-whitespace run inside the gap or span-inner region holding the cursor; a cursor on markers targets that span). |
| ARCH-5 | **Accept** (= C-2). |
| ARCH-6 | **Accept.** AT-4202 uses `shift+left`×4; AT-4201 names the details key. |
| ARCH-7 | **Accept: remove the wide label form** (one form ≤ 38 cells; no `_notes_w`, no resize hook). |
| ARCH-8 | **Accept** the 3-line fix (`_pen_at` set by `action_pen` and `action_pen_enter`; `pen_enter` arm requires `_pen_span()`). |
| ARCH-9 | **Accept:** interface example TC-4245 → TC-4253. |
| ARCH-10 | **Accept:** `_lift_pen` on a span with no closer (`end == inner_end`) inserts ` ::` before moving past it. |
| ARCH-11 | **Accept the consistent reading:** inside an open span, at `:::<c>::` the opener at j+1 wins (span text keeps the `:`), matching TC-4229 outside spans. Example `::r:: a :::b:: c ::` → `("a :","over"),("c","blue")`. |
| ARCH-12 | **Accept:** the count is 1 112. |
| ARCH-13 | **Accept:** pin the ` ::` result in TC-4250 and the README sentence; no code. |
| SEC-1 | **Accept:** linear scanner (cache each kind's next match) and one-pass byte offsets. New LLR-4201.10, LLR-4204.7. |
| SEC-2 | **Accept:** the pen insert gets the visible-text check and notice N4. New LLR-4203.17. |
| SEC-3 | **Keep HLR-4204** — the commission (C-2) asks for live colour IN the TextArea; the preview does not meet it. Make it fail-safe: the override catches any exception and falls back to the base map (no ink, no crash). New LLR-4204.8. Pinning Textual in pyproject → BACKLOG. |
| SEC-4 | **Accept with ARCH-8:** `_pen_at` is reset whenever a pen is set or lifted; `_pen_follow` deletes only if the text at `_pen_at` is still an empty span of the pen's code. |
| SEC-5 | **Accept (E4 addendum):** the palette callback re-validates the target; if the line changed it does nothing and notifies. |
| SEC-6 | **Accept:** byte offsets via `encode("utf-8", "surrogatepass")`. New LLR-4204.9. |
| SEC-7 | Covered by the ARCH-1/ARCH-2 parser-level tests. |
| SEC-8 | Pre-existing rich escape bug → BACKLOG. |
| SEC-9 | **Accept (E4 addendum):** TC-4209 also asserts every emitted tone ∈ {mut, soon, over, green, orange, blue, violet}. |
