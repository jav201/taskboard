VERDICT: PASS-WITH-NOTES

# Security Review — Inc C, multicolour notes (PDR, E3, code-free)

> security-reviewer, 2026-11-01. Read-only review of the Code-Wire design. No product file was edited.
> Counts: HIGH 0 · MEDIUM 3 · LOW 6. No finding blocks under the role's rubric. SEC-1, SEC-2 and SEC-3
> change the design, and they cost little to fix, so I ask that they be ruled on before E4 (build) starts.
> Every mitigation below is `planned`. None is `executed`.

## Scope reviewed

- `.dev-flow/2026-11-01-v3-incC/`: 01-requirements.md, graph-interfaces.cw.md, graph-proto-V.cw.md,
  graph-proto-M1.cw.md, graph-proto-M2.cw.md, graph-baseline.cw.md, baseline-notes.md, 03-pdr-rulings.md.
- Current code (read-only): `taskboard/views.py` (`c`, `_highlight_markup`, `_present_note_markup`),
  `report_html.py` (`notes_html`, `embed_json`), `report.py` (`_e`), `report_workspace.py` (the JS
  `innerHTML` sinks at :608, :692, and `downloadView`), `report_deck.py` (:344), `models.py`
  (`strip_controls`, `clean_strings`, `_MAX_PASTE_CHARS`), `team_sync.py` (`_read_json`).
- Textual 8.2.8 source (anaconda site-packages): `TextArea.__init__` (:638 `_themes` per instance),
  `_build_highlight_map` (:824), `_render_line` (:1494-1508), `document/_document.py::_utf8_encode`.
- Measurements: I ran the V-group scanning algorithm, transcribed exactly, as a stdin script
  (`python -I -`, no file written). The timings below come from that run.

## What I checked and found safe (no finding)

- **Markup injection on the new label surfaces.** `pen_label`, `ColourPalette` rows and the legend
  swatch are either `Text` pieces or `c(<constant>, tone)` built from `PEN_CODES`. The same holds for
  `DETAILS_NOTES_LABEL` (markup built from constants at import), N1-N4 (`notify(..., markup=False)`) and
  the binding action strings (`pick('<code>')`, built from constants). No user text reaches markup on
  any surface this increment adds. The one place where user text does reach Rich markup is the
  unchanged `_highlight_markup`, which escapes it (see SEC-8).
- **HTML class injection.** The `<tone>` in `hl-<tone>` comes from a closed set:
  `_OPENER_RE` = `::([roygbv])::`, its group is looked up in `PEN_CODES`, and the legacy tones are
  constants. No user text can become a class name. `notes_html` escapes every piece with
  `html.escape(quote=True)` and writes only constant tags. That holds for the new spans too:
  `"::b:: <x> ::"` → `<span class="hl-blue">&lt;x&gt;</span>` (TC-4216). The workspace's `innerHTML`
  sinks get only that server-built string, and the export (`downloadView`) re-embeds it through
  `scriptSafe`. If a tone that is not in the set ever appeared, `notes_text`/`c` would raise `KeyError`
  on `HEX[tone]`, so a bad tone fails closed.
- **Theme leak across screens.** I confirmed that `TextArea._themes` is a per-instance dict
  (`_text_area.py:638`). `InkArea.__init__` registers a theme with a fresh `syntax_styles` dict and never
  writes to `get_builtin_theme("css")`. LLR-4204.6 / TC-4247 pin this: the built-in css theme keeps 45
  keys and 0 `pen.` keys, and its object is `is not` the editor's. The prototype's leak is closed by
  this design.
- **Byte offsets in the highlight map.** `b(i) = len(line[:i].encode("utf-8"))` is correct for
  combining marks, emoji and other wide characters, because Textual maps bytes to code points and
  `TextArea` columns are code points. A wrong offset also fails soft: `byte_to_codepoint.get(start, 0)`
  / `.get(end)` mis-paints instead of raising. TC-4246 pins `é … ☕`. The only crash is SEC-6.
- **Palette integrity (LLR-4205.9/.15).** `recolour` rewrites only the target or its span. The
  visible-text check in `_apply_colour` refuses every rewrite that would change what the line shows
  (`std::vector`, `planb::`, `==a::b==`).

## Findings

### SEC-1 [MEDIUM] — `colour_spans` is quadratic in spans per line, and the live ink re-pays that cost on every keystroke

- **What:** In step 1 of the scanning algorithm (graph-proto-V), each loop iteration calls both
  `LEGACY.search(text, pos)` and `OPENER.search(text, pos)` again. When one kind wins repeatedly and the
  other kind has no later match, every iteration rescans the rest of the line, so the cost is
  O(spans × line length). `ink_highlights` adds a second quadratic term: `b(i)` re-slices and
  re-encodes the line prefix for four offsets per span.
- **Where:** `colour_spans` (graph-proto-V, scanning note steps 1-3) and `ink_highlights` (graph-proto-M1).
  Per keystroke, `InkArea._build_highlight_map` runs over the whole document, `notes_preview` runs over
  the whole text, and `_pen_follow` runs on the current row.
- **Evidence (concrete inputs, measured):**
  - Pasting one line of `"::b::x::" * 12500` (100 000 characters, exactly `_MAX_PASTE_CHARS`):
    `colour_spans` takes 918 ms and `ink_highlights` 1 103 ms.
  - So one keystroke on that line costs about 3 s (ink, then preview, then `_pen_follow`).
  - Doubling the input from 5k to 10k spans raises the scan from 142 ms to 572 ms (×4).
  - `"!!" + "::b::x::"*10000` (one unclosed legacy opener) takes 566 ms.
  - `"é::b::x::"*10000` takes 1 951 ms in the ink alone.
  - Base `finditer` on 100k characters takes 3 ms.
  - A 5k-line note of short lines takes 26 ms, so line count is not the problem; long lines are.
  - The same note synced from a teammate makes details, presentation and reports stall for everyone
    who views it.
  - Not ReDoS in the strict sense: both regexes are linear per call, and 10k bare colons take 0.1 ms.
- **Smallest fix:**
  1. Keep `lm` and `om` across iterations, and search again only when `pos > cached.start()`. Once a
     search returns `None`, never search for that kind again. This is safe: a match found from p1 at s
     is the same match when searched from any p2 with p1 ≤ p2 ≤ s.
  2. Find the inner end with `str.find("::")` and `str.find("\n")` instead of the per-character loop.
  3. In `ink_highlights`, use the identity offsets when `line.isascii()`. Otherwise run one cumulative
     pass over the line (or encode once and map), never `line[:i].encode()` per offset.

  Measured with fix 1: 100k characters in 27 ms, linear.
- **Proposed threshold (new LLR under HLR-4201/4204):** the scanner and the ink shall be linear.
  - Ratio gate: `t(2n)/t(n) ≤ 2.5` for n = 50k on the three inputs above.
  - Absolute gate: a 100 000-character line (`_MAX_PASTE_CHARS`) tokenises in ≤ 100 ms and inks in ≤ 150 ms.
- **State:** `planned`.

### SEC-2 [MEDIUM] — a pen insert can fuse with neighbouring text and silently change what the user's existing text shows

- **What:** `action_pen` inserts `::<code>::  ::` at any plain-text cursor. The pair's trailing `::`
  plus text after the cursor that starts with `<code>::` forms a new opener. Likewise, text before the
  cursor that ends with `::<code>`, plus the pair's leading `::`, forms an opener. In both cases the
  user's own characters turn into markers. The text is saved and synced in that state. Nothing checks
  for this: LLR-4203.12/.13 test only "inside a span" and "selection", and the visible-text invariant
  of LLR-4205.15 covers only the palette.
- **Where:** `TaskModal.action_pen` step (4) (graph-proto-M1). Data integrity in the spirit of
  LLR-4205.9/.15.
- **Evidence (reference scanner):**
  - Notes `"b:: x"`, cursor (0, 0), `alt+1` → `"::r::  ::b:: x"`. The visible text goes from `b:: x` to
    ` x`: the user's `b::` becomes an opener. The pen's inner is `" "`, which is not empty, so `alt+0`
    keeps the corruption.
  - Notes `"C::b"` (C++), cursor at the end, `alt+1` → `"C::b::r::  ::"`. The visible text goes from
    `C::b` to `Cr  ::`. The pen's span is never parsed, so `_pen_follow` turns the pen off on the
    first queued SelectionChanged, and the user is left with corrupted text and no pen.
  - Notes `"note y::"`, cursor (0, 5) → visible `"note  "`.
- **Smallest fix:** Apply the one invariant the palette already uses. In `action_pen`, compute the new
  line first. If the joined segments of `highlight_segments(new_line)` differ from those of `line`
  (the pair's inner is empty, so they must be equal), or if `colour_spans(new_line)` holds no span of
  that code starting at `col`, then insert nothing and notify N4. This is one check, it reuses N4, and
  it adds no new syntax. Add an LLR-4203.16 with the three inputs above as its threshold.
  (The alternative, an escape syntax for `::`, is a new feature. I recommend against it.)
- **State:** `planned`.

### SEC-3 [MEDIUM] — the private-API override is not fail-safe on a Textual upgrade, and `pyproject.toml` leaves Textual unpinned

- **What:** `InkArea._build_highlight_map` overrides a private method and writes `_highlights` and
  `_line_cache`. `pyproject.toml` declares `"textual"` with no version, and only `requirements.txt`
  pins 8.2.8. A fresh `pip install .` or `pip install -U` can therefore pull a Textual version where:
  - `_build_highlight_map` is renamed: the ink silently disappears. That is fail-safe.
  - `_line_cache` or `_highlights` is renamed: `AttributeError` is raised inside `TextArea.__init__`
    (via `_set_document`), so the editor cannot open and the app crashes. It is also raised inside
    `edit()`, so the crash loses the unsaved edit.
  - The tuple shape `_render_line` expects changes: `_render_line` raises on every paint.

  The guard test ruled in P-M1-7 runs only in the developer's test suite. It does not protect a user's
  machine after an upgrade.
- **Where:** `InkArea._build_highlight_map` and `InkArea.__init__` (graph-proto-M1). `pyproject.toml:13`.
- **Evidence:** In the Textual 8.2.8 source, `_build_highlight_map` is called from `_set_document`
  during `__init__`, from `edit()` (:1700), and from undo and redo. `_render_line` reads
  `self._highlights` and unpacks 3-tuples (:1494-1508). Neither name is public API.
- **Smallest fix (preferred, removes the feature):** Drop HLR-4204 (the live ink). The `#task-preview`
  pane already paints the same colours live beside the field: it is the base behaviour, and the base
  test `test_the_preview_follows_the_typing_to_the_last_line` covers it. Dropping the ink also removes:
  - SEC-6;
  - half of SEC-1's per-keystroke cost;
  - the byte-offset code;
  - three private names.

  The operator decides the UX trade-off.
- **Fallback if the ink stays:**
  - (a) Pin `textual>=8.2.8,<8.3` in `pyproject.toml`. That is one line in a config file, not in the
    4-source budget, so I ask that the backlog ruling of P-M1-7 be reconsidered.
  - (b) Wrap the override body in `try/except Exception`. The except branch clears the map, if one
    exists, and falls back to `super()._build_highlight_map()`, which gives a plain field with no ink.
  - Add a test that monkeypatches `_line_cache` away and asserts that the editor still opens and saves.
- **State:** `planned`.

### SEC-4 [LOW] — `_pen_at` can go stale and delete an unrelated empty span, with no visible-text check on the deletion

- **What:** `_pen_at` is written only while `_pen_follow` finds the pen's span. The design never resets
  it when a new pen is set or when a pen goes off. In the `"C::b"` case of SEC-2, and after an undo
  under a pen, the pen's span is never found. A stale `_pen_at` left by an earlier pen session on the
  same row can then match a different empty span of the same code at the same start, and that span is
  deleted. Deleting an empty span normally shows the same text, but deletion can join neighbours into a
  new marker. For example, `"==a=::y::::=x"` shows `==a==x` before the deletion and `a` (in soon) + `x`
  after it.
- **Where:** `TaskModal._pen_follow` (a) and `[Data: TaskModal._pen_at]` (graph-proto-M1). `_lift_pen`
  is the same kind of deletion.
- **Smallest fix:**
  - Set `_pen_at = (row, col)` in `action_pen` step (4), and set it to `None` wherever the pen is set
    to `None`.
  - Guard both deletions (`_pen_follow`, `_lift_pen`) with the same visible-text invariant as SEC-2:
    skip the delete if it would change the joined segments.
- **State:** `planned`.

### SEC-5 [LOW] — the palette callback re-reads the line and can raise inside a callback

- **What:** `_apply_colour` reads `notes.document.get_line(row)` at pick time, but `(row, a, b)` was
  computed at palette open. `recolour` "raises ValueError … on a target that partly overlaps a span".
  An exception raised in a `push_screen` callback crashes the app and loses the unsaved editor. Nothing
  known changes the notes while the modal is on top, so this is defence in depth.
- **Where:** `TaskModal.action_colour`, `TaskModal._apply_colour` and `recolour` (graph-proto-M2).
- **Smallest fix:**
  - Carry the line text from palette open in the `partial`. If the current line differs, notify and
    change nothing.
  - Make `recolour` return `(line, None)` instead of raising.
- **State:** `planned`.

### SEC-6 [LOW] — a lone surrogate in a note crashes the editor once any line has ink

- **What:** `strip_controls` keeps U+D800-U+DFFF, and `json.loads` turns `"\ud800"` into a lone
  surrogate. Both `ink_highlights` (`line[:i].encode("utf-8")`) and Textual's own `_render_line`
  (`_utf8_encode(line.plain)`, strict) raise `UnicodeEncodeError`. Textual runs that encode on every
  visible line as soon as `_highlights` is non-empty. At base `_highlights` is always empty, so this
  path never ran.
- **Evidence:** a board file whose note is `"::b:: x ::\ud800"` (JSON escape). Opening the editor
  raises inside `TextArea.__init__` (via `_build_highlight_map`). I did not verify whether base already
  fails to paint lone surrogates elsewhere (the terminal writer encodes strictly), so this rates LOW.
- **Where:** `ink_highlights` and `InkArea._build_highlight_map`.
- **Smallest fix:**
  - If SEC-3's preferred fix is taken, this finding goes away.
  - Otherwise, in the override, leave `_highlights` empty when `"\n".join(lines)` does not encode as
    strict UTF-8.
  - Add the input above as a test.
- **State:** `planned`.

### SEC-7 [LOW] — keystroke ordering around priority bindings (unverified)

- **What:** `alt+<n>` and `alt+c` are priority bindings that run in the App's task. Typed characters
  are forwarded to the TextArea's own queue. Under fast input, a character typed just before `alt+5`
  may land after the pair is inserted, that is, inside the span. That changes the colour, not the
  characters. The same pattern exists at base for `alt+s` (the last keystroke could be missing from
  the save). I have not reproduced this.
- **Where:** `[Outside: key alt+1..alt+6]` and `[Outside: key alt+c]` (graph-proto-M1/M2).
- **Smallest fix:** A pilot test that sends `"a"`, `"alt+5"`, `"b"` in one `press()` call and asserts
  `"a::b:: b ::"`. If the test shows the race, the action should first `await` until the TextArea's
  queue is drained.
- **State:** `not-run`.

### SEC-8 [LOW] — `rich.markup.escape` mishandles three or more trailing backslashes, and the new syntax adds segment edges where they occur (pre-existing)

- **What:** `_highlight_markup` (unchanged) writes `c(escape(seg), tone)`, which produces `[#hex]…[/]`.
  In rich 15.0.0, `escape("a\\\\\\")` (three backslashes) is not fixed, so the closing `[/]` is escaped.
  The tone then bleeds into the rest of the line and `[/]` shows as literal text. Two backslashes
  render as one. This corrupts the display only: it raises no `MarkupError` and injects nothing.
- **Evidence:** `render("[#60a5fa]" + escape("a\\\\\\") + "[/][#8b98a5]tail[/]").plain` is
  `'a\\[/]tail'`, with blue over the whole span. The new trigger is the note `::b:: a\\\ :: tail`. At
  base the trigger was `==a\\\==`.
- **Where:** `views._highlight_markup` (unchanged reader). It is called by `_focus_note_snippet`,
  `_focus_detail_lines`, `_focus_tiles` and `_focus_review`.
- **Smallest fix:** Backlog (out of this increment's slice). Escape with a helper that doubles a
  trailing backslash run of any length, or build these focus pieces as `Text`.
- **State:** `planned` (backlog).

### SEC-9 [LOW] — the HTML class invariant rests on an implementation detail, and no test pins it

- **What:** `notes_html` is "unchanged" and trusts `highlight_segments` to emit only known tones. The
  design is safe as written. A later edit, for example an opener like `::(\w)::` with an `f"…"` tone,
  would turn user letters into class names, and no test would notice.
- **Where:** `colour_spans` and `report_html.notes_html`.
- **Smallest fix:** Extend TC-4209. Over the derived set, every emitted tone must be in
  `{tone of PEN_CODES} ∪ {soon, over, green, mut}`. Every `class="…"` in `notes_html` output must match
  `hl-(mut|over|orange|soon|green|blue|violet)( mention)?`.
- **State:** `planned`.

## Verdict (role tokens)

- [x] **OK to ship (design stage)** with notes. No HIGH. The MEDIUMs (SEC-1, SEC-2, SEC-3) need a ruling
  in `03-pdr-rulings.md` and their mitigations folded into the graphs before E4. I re-verify them at
  the increment gate as `executed`.
- [ ] `BLOCK-UNTIL:` none.
- [ ] Block: none.

This clearance is not the operator's authorisation for anything.

## Evidence checklist

- ✓ Each finding has what · where · why (impact) · recommendation: SEC-1..SEC-9 above.
- ✓ Each finding has a severity: 0 HIGH, 3 MEDIUM, 6 LOW.
- ✓ No secret values appear in this output. None were found in scope; no credential surface is touched.
- ✓ The verdict is explicit (PASS-WITH-NOTES / "OK to ship, design stage"). No HIGH exists.
- ✓ New tool or integration: `n/a — no new dependency, connector or external call`. The Textual
  private-API dependency is covered in SEC-3.
