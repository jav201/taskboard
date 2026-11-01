# Inc C: PDR (E3), architect review

VERDICT: FAIL

**Summary.** The tokeniser, the readers, the report CSS and the C-4 palette are sound. Every LLR-4201 example passes a scratch reference scanner built from graph V's algorithm, and so does every recolour, target and placement example in M2. The verdict is FAIL because of the pen keys. On Textual 8.2.8, a terminal using the legacy key encoding never delivers `alt+1`..`alt+6` or `alt+0` as those keys. The pilot-based test plan cannot detect this, so HLR-4203 could ship green and not work. Two HIGH findings come from the same cause: the gap between pilot keys and terminal keys (ARCH-2), and the alt+c target under a pen, which is only right by coincidence (ARCH-3).

**What would flip the verdict.** It becomes PASS-WITH-NOTES if a real Windows Terminal probe shows `alt+5` arriving as `alt+5` (ARCH-1), and ARCH-2 and ARCH-3 are applied to the graph.

Counts: MAJOR 1 · HIGH 2 · MEDIUM 4 · MINOR 6.

Scratch evidence (outside the repo): `C:\Users\jjgh8\AppData\Local\Temp\incC-arch\` holds four scripts.
- `ref.py`: the reference scanner.
- `t1.py`: the tokeniser. It checks 40 example checks, LLR-4201.3 over 1 112 inputs (0 differences) and LLR-4201.9 over 11 110 inputs (0 invariant breaks).
- `t2.py`: the palette. It checks 22 recolour cases, 14 target cases and 4 placement cases.
- `t3.py`: the pens. It runs 21 checks in a pen-editor model.

All are `executed`, with 0 FAIL on the graph's own examples.

---

## Findings

### ARCH-1 [MAJOR] The pen keys never reach their bindings on a terminal that uses the legacy key encoding
- **Where:** graph-proto-M1.cw.md:216-220 (`[Outside: key alt+1..alt+6]`, `alt+0`), `TaskModal.action_pen` (:63-83), and every pilot test of HLR-4203 (TC-4230..TC-4257, AT-4201).
- **Evidence (executed):**
  - `textual/_ansi_sequences.py:384-394` maps ESC+digit to macOS Option characters: `"\x1b1": "¡"` … `"\x1b5": "∞"` … `"\x1b0": "º"`.
  - Probe: `XTermParser().feed("\x1b5")` gives `Key('infinity', '∞')`, and `"\x1b0"` gives `Key('º', 'º')`.
  - The Windows driver feeds VT input to that same parser (`drivers/win32.py:179, 230, 289`). So `alt+5` in the notes types `∞` into the text and opens no pen.
  - The pilot does not take that path: `app.py:2059-2064` builds `Key("alt+5", None)` directly. Every pen test is therefore green on a dead feature.
  - The keys work only if the terminal honours the kitty request `\x1b[>1u` (`drivers/windows_driver.py:99`). Windows Terminal + ConPTY support for it: `not-run`.
  - Baseline note "alt+0 … alt+9 are FREE everywhere" (baseline-notes.md:17) is consistent with this: no one uses them because they do not arrive.
  - The commission's standing rule says "inside text fields, use `alt+letter`" (COMMISSION:89).
- **Fix (smallest):**
  1. E4 entry gate: in a real Windows Terminal window, a 10-line Textual key logger records what `alt+5` and `alt+0` produce. Close the window by title afterwards.
  2. If the logger shows `infinity`/`º`, this needs an operator ruling to remap the pens to `alt+<letter>` keys that are probe-verified. Two constraints:
     - Free in TaskModal: `alt+r`, `alt+o`, `alt+y`, `alt+g`, `alt+v`, `alt+x`. The grep of modals.py shows only `alt+c/d/h/i/m/n/p/s/t` in use.
     - **Not `alt+b`**: `"\x1bb"` is `ctrl+left` (`_ansi_sequences.py:275`). Probe: `Key('ctrl+left')`.

     Do **not** bind the glyph key names instead: `¡` and `º` are plain keys on Spanish and LatAm layouts, and `£` is `shift+3` on UK layouts.
  3. Add one layer-0 test that feeds the terminal's bytes to `XTermParser` and asserts the key name the binding uses. It is the only test that can go RED on this.

### ARCH-2 [HIGH] A denied gate lets alt+c fall through as a printable character, and the pilot cannot see it
- **Where:** graph-interfaces.cw.md:53 (`check_action`, the one notes-focus gate for `pen`/`colour`); LLR-4205.16 (01-requirements.md:222-223), LLR-4203.10 (:165).
- **Evidence (executed):**
  - In legacy encoding, `"\x1bc"` gives `Key('alt+c', 'c')`, and `is_printable` is True.
  - With the focus in `#f-title`, `check_action("colour")` returns False, so `run_action` returns False (`app.py:4245-4248`). The key then goes to the focused Input.
  - `Input._on_key` inserts `event.character` (`widgets/_input.py:746-751`). The title gains `c`.
  - TC-4284 uses the pilot (character None), so it stays green.
  - The same leak exists at base for `alt+m` when no `#f-mark` is composed. That is out of scope; backlog it.
- **Fix:**
  - For `pen` and `colour`, `check_action` returns True. Each action returns at once when `#f-notes` lacks the focus, which consumes the key.
  - Keep the deny only on `pen_enter`, where the fall-through to the newline is wanted.
  - TC-4240 and TC-4284 post the terminal's event, `events.Key("alt+c", "c")`, instead of `pilot.press`.

### ARCH-3 [HIGH] alt+c under a pen targets "the word ending at the cursor", not the pen's span
- **Where:** graph-proto-M2.cw.md:17 (`action_colour`: lift, then `colour_target` on the cursor), :25 (TC-4274), :33 (rule 2); LLR-4205.14 (01-requirements.md:224-225, "target = the pen's span").
- **Evidence (executed, t2.py):**
  - The lift puts the cursor at `s.end`, just after the closer. The word "ending at col" is then the closer `::` itself. That is inside the span only when whitespace or the line end follows the closer.
  - The threshold example passes by this coincidence.
  - Counter-example: notes `now`, cursor (0, 0), `alt+5`, type `go` gives `::b:: go ::now`. Then `alt+c`: the lift puts the cursor at (0, 11), the word is `::now` (9..14), and it overlaps the span 0..11. Result: notice N2 "The selection crosses a colour edge…", and no palette.
  - Same result for `::b:: ab ::, more` (a pen opened before a comma).
- **Fix:** `action_colour` reads `s = self._pen_span()` **before** `_lift_pen()`. If `s` has inner text, the target is `(row, s.inner_start, s.inner_end)`; the lift does not change the text in that case. If `s` is empty or None, use the current path. Add `::b:: go ::now` to TC-4274 and to the LLR-4205.14 threshold. Then `_pen_span`'s note "used by M2" (graph-interfaces.cw.md:44) is also true.

### ARCH-4 [MEDIUM] The word target swallows span markers
- **Where:** graph-proto-M2.cw.md:33 (`colour_target` rule 2: the word is a maximal run of non-whitespace).
- **Evidence (executed):**
  - LLR-4203.3's own result is `::b:: abc ::d`. With the cursor on `d` at (0, 12), `alt+c` takes the word `::d` (10..13). It overlaps the span 0..12, so the editor shows N2 and opens nothing.
  - The user selected nothing, yet the notice speaks of "the selection".
- **Fix:** take the word as the non-whitespace run inside the region (a gap, or a span's inner range) that holds the cursor. A cursor on a span's markers targets that span, which keeps TC-4261 `(0, 9, 11)`.
  - Example to add: `::b:: abc ::d`, (0, 12) → target (0, 12, 13).
  - Recolouring `d` green then gives `::b:: abc ::::g:: d ::`, with the visible text unchanged (checked).

### ARCH-5 [MEDIUM] The details label in graph M2 contradicts ruling C-2
- **Where:** graph-proto-M2.cw.md:191-193, 223 (`TaskDetails.compose`, TC-4276: plain text `Notes  r o y g b v`, "holds no … `::`") against 03-pdr-rulings.md:46 (C-2: keep `Notes  ::c:: … ::  r o y g b v`).
- **Evidence:** a tester who writes TC-4276 from the graph writes a RED test against the label that E4 builds.
- **Fix:** amend the M2 node, TC-4276 and the `[Interface: TaskDetails Notes label]` entity to the C-2 form before E4. Drop "no `::`" and keep 6/6 tone hexes.

### ARCH-6 [MEDIUM] AT-4202's key script selects the wrong text
- **Where:** 01-requirements.md:243 (AT-4202: "`shift+left`×5 from (0,8)… select `plan`").
- **Evidence (executed):** from (0, 8), five presses select (0, 3)..(0, 8), which is ` plan`. The design then writes `the::y::  plan :: works` (the visible text is unchanged, so it is allowed), not the AT's `the ::y:: plan :: works`. The AT fails on a correct build.
  - AT-4201 also says "(`enter`/`v` as the app binds)", which is not a key script.
- **Fix:** `shift+left`×4. In AT-4201, name the one key that opens the details.

### ARCH-7 [MEDIUM] Simplicity: nothing requires the wide Notes-label form
- **Where:** graph-proto-M1.cw.md:31-61 (`_fit_width` → `_notes_w`, `pen_label` wide/narrow, PEN_LABEL_WIDE `54`), :181-183 (`[Data: TaskModal._notes_w]`).
- **Evidence:**
  - The narrow form is at most 38 cells. It fits 39 (80x24) and 58 (118x30), and it names the pen in the chip.
  - LLR-4203.9 asks only for the keys, `0`, `alt+c` and the state at both sizes, plus the pen's name at 118x30. The narrow form gives all of them.
  - The wide form adds a state variable, a resize dependency and 7 more width examples.
- **Fix:** keep one form. Drop `_notes_w`, PEN_LABEL_WIDE and the `_fit_width` hook. `_pen_label` runs on mount and after each pen write.

### ARCH-8 [MINOR] Pen decisions can read stale state when the next key overtakes the editor's own SelectionChanged
- **Where:** graph-proto-M1.cw.md:99 ("Each action body runs whole before Textual handles any queued message…"), :185-187 (`_pen_at` written only by `_pen_follow`); graph-interfaces.cw.md:53 (the `pen_enter` arm checks only `pen` is on).
- **Evidence (analysis, `not-run`):**
  - The claim holds for the action's own messages, not for the next key.
  - The insert's SelectionChanged reaches TaskModal only after bubbling through `#task-edit`, `#task-split` and `#task-box`. A `home` that follows is handled by the TextArea in one hop.
  - If `home` lands first, `_pen_follow` sees the pen on, the cursor outside and `_pen_at` None. The empty span stays, and the editor later saves `x::y::  ::`, which is the NC of LLR-4203.11 and LLR-4203.14.
  - It is unlikely at typing speed and possible with paste or key repeat.
- **Fix (3 lines):**
  - `action_pen` sets `_pen_at = (row, col)` when it opens the span.
  - `action_pen_enter` sets `_pen_at = (row + 1, 0)`.
  - The `pen_enter` arm requires `_pen_span() is not None`.

### ARCH-9 [MINOR] TC-4245 names two different tests
- **Where:** graph-interfaces.cw.md:47 (`_pen_span`, cursor (0, 12) → None) and graph-proto-M1.cw.md:142-144 (`ink_highlights`).
- **Fix:** renumber the interface example to a free M1 id: TC-4253 (unused) or TC-4249/TC-4251 (dropped).

### ARCH-10 [MINOR] alt+0 on a pen span with no closer leaves the cursor inside
- **Where:** graph-interfaces.cw.md:34 (`_lift_pen`: "else put the cursor at s.end").
- **Evidence (executed, t3.py):**
  - Steps: pen on `::b:: ab ::` at (0, 8), then `delete` ×3. M1 itself says a forward delete only extends the span. The text is now `::b:: ab`, and `s.end == s.inner_end == 8`.
  - `alt+0`, then type `d`: the result is `::b:: abd`, with `d` blue. LLR-4203.3's "just after that span's closer" has no closer to go after.
- **Fix:** when `s.end == s.inner_end`, `_lift_pen` inserts ` ::` first. Alternatively, pin the current behaviour with an example.

### ARCH-11 [MINOR] Inside an open span, `:::b::` is read as a closer plus literal text
- **Where:** graph-proto-V.cw.md:11-12 (step 3a checks `OPENER.match(text, j)` only).
- **Evidence (executed):**
  - `::r:: a :::b:: c ::` gives `[("a","over"),(":b:: c ::","mut")]`.
  - LLR-4201.6 ("end it where the next opener starts", 01-requirements.md:112-113) and the out-of-span choice of P-M2-7 (TC-4229) both read it as `[("a :","over"),("c","blue")]`.
  - Only hand-typed text reaches this case. Pens and recolour write spaced closers.
- **Fix:** pin one reading with an example. Either also try `OPENER.match(text, j + 1)` when `text[j:j+3] == ":::"`, or reword LLR-4201.6.

### ARCH-12 [MINOR] Graph V's count for LLR-4201.3 does not match the set it cites
- **Where:** graph-proto-V.cw.md:55 ("scratch run: 1 463 inputs").
- **Evidence:** `PIECES` × up to 3 in tests/test_highlight_segments.py:48-50 is 2 + 10 + 100 + 1 000 = **1 112** inputs. My run: 1 112 inputs, 0 differences from base.
- **Fix:** correct the number, or name the set that was run.

### ARCH-13 [MINOR] Typing `::` into a fresh pen gives ` ::`
- **Where:** `_pen_follow` (graph-proto-M1.cw.md:99) on top of P-M1-5.
- **Evidence (executed, t3.py):**
  - On `::b::  ::` at (0, 6), type `:` `:`. The first typed `::` is the closer, so the span is empty and the cursor is past it.
  - `_pen_follow` then deletes `::b:: ::`, and the line reads ` ::`, cursor (0, 0).
  - This is new evidence beyond P-M1-5: the removal of the empty span also eats the user's two colons.
- **Fix:** pin the result as an example in TC-4250 and add it to the README sentence. No code change.

---

## Checks requested by the brief

| Check | State | Evidence |
|---|---|---|
| `colour_spans` vs every LLR-4201 example | executed ✓ | t1.py: 4201.1–.9 thresholds, all graph-V and interface span examples 0 FAIL; LLR-4201.3: 1 112 inputs, 0 differences; LLR-4201.9: 11 110 inputs, 0 breaks. One gap: ARCH-11 |
| Seam consistency (names, contracts, callers, TC ids) | executed, 3 gaps | ARCH-5 (C-2 not applied), ARCH-9 (TC-4245), ARCH-3 (`_pen_span` "used by M2" untrue today). `_lift_pen`/`_pen_follow` split per C-1 is consistent across files; PEN_CODES and Span identical in V and interfaces |
| Priority bindings on `enter` | executed ✓ | `binding.py:207` appends same-key bindings in order; `app.py:3984-3987` tries each and `run_action` returns False on a denied `check_action` (`:4245-4248`), so `drop_pick` → `pen_enter` → TextArea newline holds |
| `check_action` | executed, fails in real terminal | ARCH-2 |
| SelectionChanged vs the editor's inserts | executed ✓ / 1 race | Live reads make the action's own queued messages harmless (`_watch_selection` posts only on change, `_text_area.py:897-898`); ARCH-8 for the next-key race |
| Private highlight-map override | executed ✓ | `_highlights` (:662) and `_line_cache` (:689) exist before `_set_document` (:691) calls `_build_highlight_map`, so the override is safe in `__init__`; `edit` rebuilds before `Changed` (:1700-1701); `_render_line` byte→codepoint and end `0` → None (:1494-1508) as M1 says; guard tests per P-M1-7 |
| Theme isolation | executed ✓ | `register_theme` writes the per-instance `_themes` (:638, :1068); `_set_theme` shallow-copies (:1021); `apply_css` per render (:1333) fills cursor/selection on the copy; LLR-4204.6 design holds |
| 80x24 label fit | executed ✓ | `#task-box` padding 0 1, two `1fr` columns (taskboard.tcss:155-160, 254-260): 39 cells; narrow form ≤ 38. Wide form unnecessary (ARCH-7) |
| Palette vs modal-key law and inventory | executed ✓ | No Button; INVENTORY row `"ColourPalette": {}` satisfies `test_TC_2407_every_modal_is_in_the_inventory` (tests/test_modal_keys.py:326-336); keys shown on its rows. ModalScreen has no `align` (screen.py DEFAULT_CSS), and the shared `align: center middle` rule (taskboard.tcss) does not list ColourPalette, so `styles.offset` places the box as `palette_offset` computes. The pens break the law's "alt+letter" (ARCH-1) |
| 4-source-file budget | executed ✓ | views.py, modals.py, report_deck.py, report_workspace.py; palette CSS fits the DEFAULT_CSS pattern already used in modals.py (:439, :2104); README and tests/test_modal_keys.py are not source |
| Simplicity | executed | ARCH-7 (remove the wide label). Nothing else speculative: `_pen_at`, the visible-text check, legacy ink are ruled (P-M1-4, P-M2-2, P-M1-1) |
| Examples concrete enough for a RED test | executed, 2 gaps | ARCH-6 (AT-4202 off by one, AT-4201 vague key); LLR-4205.14 needs ARCH-3's example |
| C-4 palette numbers | executed ✓ | Recomputed with rich: 8-bit 203/209/214/78/75/141, HLS s ≥ 0.692, CR on #0d1117 ≥ 5.15, deck light ≥ 5.03 — matches graph V |

## Architect evidence checklist

- ✓ **Constraints stated.**
  - 4 source files: `executed`.
  - No new dependency: `executed`.
  - Textual 8.2.8 pinned only in requirements.txt: `executed`, backlog per P-M1-7.
  - Privacy: `n/a`. Notes stay local plain text and no new data path is added.
  - $ cost: `n/a`. No paid service is used.
- ✓ **2+ alternatives where a real decision exists.**
  - The key encoding is the one open decision (ARCH-1): alt+letter remap, glyph aliases (rejected: they hijack ¡/º/£ typing), or a kitty-only requirement.
  - Every other decision is `n/a`, already ruled in 03-pdr-rulings.md.
- ✓ **Constraints that do not apply are marked `n/a — <reason>`** (above).
- ✓ **Recommendation tied to constraints.** Fix ARCH-1 first: the operator's terminal is Windows Terminal (COMMISSION:90-94).
- ✓ **Risks listed.**
  - Operational: ARCH-1, ARCH-2.
  - Private-API lock-in: P-M1-7, accepted with guard tests.
  - Security: `n/a` (no new input surface; notes are never parsed as markup).
- ✓ **Latency estimated.** A full ink rebuild over 200 lines of 71 chars takes 1.41 ms per keystroke (reference scanner, `executed`), before byte conversion. Acceptable.
- ✓ **Diagram:** `n/a`. The flows are already in M1's `sequence:` blocks.
- ✓ **What would change the verdict** is stated at the top.
- ✓ **Two-layer requirements.** US-4201 → AT-4201..4204 and → HLR-4201..4206 → 61 LLR → TC. HLR-4206 has no AT, by design (analysis). AT-4202 needs ARCH-6.
