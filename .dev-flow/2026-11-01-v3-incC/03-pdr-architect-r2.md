# Inc C: PDR (E3) round 2, architect re-review

VERDICT: PASS-WITH-NOTES

**Summary.** ARCH-1, ARCH-2 and ARCH-3 are closed, and the evidence for each was re-run. The corrections for ARCH-4 to ARCH-13 are applied, and no seam is broken. One MINOR note is new: the alt+digit key path still has no end-to-end check in a real terminal, and one TC id has two meanings.

Counts of new or still-open findings: MAJOR 0 · HIGH 0 · MEDIUM 0 · MINOR 1.

## Blocking findings: closed

### ARCH-1 (MAJOR): closed, executed
- **Orchestrator evidence.** `evidence/wt-kitty-query.log` shows Windows Terminal 1.24.12741 answering only the DA query, with no kitty flags. So the terminal does send `ESC <digit>`.
- **The ruling works.** I ran the parser with the seven entries `"\x1b0".."\x1b6"` removed:

  | Input | Key | Character |
  |---|---|---|
  | `"\x1b5"` | `alt+5` | `5` |
  | `"\x1b0"` | `alt+0` | `0` |
  | `"\x1b1"` | `alt+1` | `1` |
  | `"\x1b7"` | `pilcrow_sign` | `¶` (unchanged, as intended) |
  | `"\x1bs"` | `alt+s` | `s` (unchanged) |
  | `"\x1b[A"` | `up` | — (unchanged) |
  | `"\x1b"` | `escape` | — (unchanged) |

- **No stale cache.** Removing the entries also works for a parser that was built before the removal. The parser's `lru_cache` sits only on `_parse_extended_key`, so it holds nothing stale.
- **The test recipe holds.** TC-4249 flushes with `p.feed("")`. I re-ran that recipe and got the results the node lists.
- **Traceability holds.** LLR-4203.16 has a concrete threshold and a negative control that turns RED on the base table.

### ARCH-2 (HIGH): closed
- In graph-interfaces, `check_action` now always allows `pen` and `colour`. `action_pen` (M1:69, step 0) and `action_colour` (M2:18, step 0) return early and consume the key.
- Only `pen_enter` stays gated, and it now also requires `_pen_span()`.
- TC-4240 and TC-4284 post the event the terminal really sends (`Key("alt+5","5")`, `Key("alt+0","0")`, `Key("alt+c","c")`), each with a negative control ("T0" / "Tc" turns it RED).

### ARCH-3 (HIGH): closed
- `action_colour` reads `_pen_span()` before `_lift_pen()` and uses the span's inner range as the target (M2:18).
- TC-4274 now carries the counter-example `::b:: go ::now` → palette for 6..8, with a negative control.
- The offsets stay valid when the span has no closer, because ARCH-10's ` ::` is inserted after `inner_end`.

## ARCH-4 to ARCH-13: applied, seams consistent

- **ARCH-4:** `colour_target` now picks the word inside the region that holds the cursor.
  - Examples `::b:: abc ::d` → (0, 12, 13) and `x::b::y::` → (0, 0, 1).
  - TC-4261 keeps `(0, 9, 11)` for a cursor on the markers.
- **ARCH-5:** TC-4276 uses the C-2 label `Notes  ::c:: … ::  r o y g b v`.
- **ARCH-6:** AT-4202 uses `shift+left`×4. AT-4201 names the details key.
- **ARCH-7:** the wide label form is gone. Nothing outside the finding text still refers to `_notes_w`.
- **ARCH-8:** `action_pen` and `action_pen_enter` now write `_pen_at` themselves, and the `pen_enter` arm requires `_pen_span()` (TC-4237, second arm).
- **ARCH-9:** the interface example is now TC-4253.
- **ARCH-10:** `_lift_pen` handles a span with no closer (TC-4258, two new arms). I checked `::b:: x ::r:: y ::` → `::b:: x  ::::r:: y ::`: the visible text is unchanged and the cursor is at 11.
- **ARCH-11:** the scanner's new step a′ was added to my reference. Every tokeniser, recolour and pen example still passes:
  - LLR-4201.3: 1 112 inputs, 0 differences.
  - LLR-4201.9: 11 110 inputs, 0 invariant breaks.
  - `::r:: a :::b:: c ::` → `("a :","over"),("c","blue")`.
- **ARCH-12:** the count now reads 1 112.
- **ARCH-13:** TC-4250 pins the ` ::` result.

## New or still-open findings

### ARCH-14 [MINOR] The alt+digit key path is checked only at the parser, and TC-4249 now names two things
- **Where:** graph-proto-M1.cw.md:13-23 (`_unshadow_alt_digits`), :335 (the round-0 finding text "the old TC-4249 … is dropped"); 03-pdr-rulings.md Round 1 ("SendKeys … delivered nothing").
- **Evidence:**
  - The chain is tested in two pieces: bytes → key name (TC-4249), and key event → action (TC-4240 and the pen TCs). The Windows driver's own record filter (`drivers/win32.py:273-277`) is in neither piece. Its end-to-end state is `not-run`.
  - Indirect evidence: `alt+s` (`ESC s`) takes the same route and is in daily use.
  - The fix also adds a second private-API dependency: a global change to `textual._ansi_sequences`. TC-4249's `alt+5` arm acts as its guard on an upgrade.
  - `TC-4249` is used again for the parser test, while line 335 still says the old TC-4249 was dropped.
- **Fix:**
  - One manual line in the E5/operator review: in Windows Terminal, open the editor, press `alt+5`, type `x`, and check that `x` is blue.
  - Reword line 335 to "the old same-code TC was dropped; TC-4249 now names the parser test", or move the parser test to a free id.
  - Add `textual._ansi_sequences` beside P-M1-7 in the Textual-pin backlog item.
