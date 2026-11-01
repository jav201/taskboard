VERDICT: PASS-WITH-NOTES

# Security Review — Inc C, multicolour notes (E5, validate the change)

> security-reviewer, 2026-11-01. Read-only: no product or test file was edited.
> Scope: `git diff 0a8dfaa..HEAD -- taskboard README.md` (modals.py +484, views.py +119, report_deck.py,
> report_workspace.py, README.md), checked against 03-pdr-security.md, 03-pdr-security-r2.md,
> 03-pdr-rulings.md and e4-addenda.md.
> Counts: HIGH 0 · MEDIUM 1 · LOW 2. Every accepted SEC item is implemented and I verified each one by
> running it (table below). The three findings are new.
> Every probe ran from the worktree with `env -u NO_COLOR C:/Users/jjgh8/anaconda3/python.exe` and
> `PYTHONPATH` set to the worktree. I printed `taskboard.__file__` to confirm the worktree's `src` was
> the one imported. The scratch scripts live outside the repo, in
> `C:\Users\jjgh8\AppData\Local\Temp\secrev-incC\` (t_perf, t_fuzz, t_pilot, t_ansi, t_misc, t_keylat,
> t_prof). The full suite was not run.

## Accepted SEC items: are they implemented? (state: `executed` and `approved` unless noted)

| Id | Where | Evidence (run) | State |
|---|---|---|---|
| SEC-1 linear scanner and ink offsets | `views.colour_spans`: the match of each kind is cached, and the inner end uses `str.find`. `modals._byte_offsets` makes one pass. | Going from 10k to 100k chars multiplies the time by 8.5 to 11.4 on 15 hostile shapes, including the round-1 worst case `"!!"+"::b::x::"*n`, openers with no closer, `:::b::`, unclosed `==` and `!!` inside spans, é, ☕/漢 and combining e+U+0301. At 100k chars: `colour_spans` ≤ 17.6 ms, `ink_highlights` ≤ 34.9 ms, `notes_html` ≤ 38.5 ms, `_highlight_markup` ≤ 40 ms, `notes_preview` ≤ 72.8 ms. A 5k-line note (115k chars): spans 10 ms, ink 16 ms, html 20 ms, preview 48 ms. A 5k-line note of 200-char lines (1M chars): spans 169 ms, ink 204 ms. Everything scales linearly. | executed, approved. The paint path is a separate problem: see SR-1. |
| SEC-2 pen insert keeps the visible text | `TaskModal.action_pen`: a joined-segments check, then N4. | Fuzz of 90k random lines over `: b y r space a = ! + x \ [ ] /`, at every allowed column and with three codes. 0 inserts changed the visible text or the tone of any visible char, and every inserted pair parsed as an empty span of its code at `col`. | executed, approved |
| SEC-3 override fails safe | `InkArea._build_highlight_map`: `try/except Exception` → `super()`. | Pilot: a raising `modals.colour_spans`. The editor opens, typing `y` works, and the save writes `'::b:: x ::y'`. A raising `ink_highlights` leaves the map `{}` and raises nothing. With the real function restored, the ink comes back. | executed, approved |
| SEC-4 `_pen_at` lifecycle | Set in `action_pen` and `action_pen_enter`, refreshed in `_pen_follow`, set to `None` on every lift or pen-off. The delete runs only on an empty span of the pen's code. | Implemented as ruled. **Undo** breaks the round-2 premise that "the empty span at `_pen_at` is always the inserted pair": see SR-2. | executed. Residual SR-2. |
| SEC-5 palette re-validates | `_apply_colour` compares the row with `line_at_open`, else N5. `recolour` no longer raises at all. | Read the code. The fuzz ran `recolour` on every target `colour_target` hands out (cursor and selections, codes r/b/0): 0 raises, and 0 tone changes outside the target. | executed, approved |
| SEC-6 lone surrogate | `_byte_offsets` uses `surrogatepass`. The override empties the map when the text does not encode as UTF-8. | Pilot with a board file whose notes are `::b:: x ::\ud800` (JSON escape). The editor opens and paints, and `alt+5` then `x` works. The save writes `'::b:: x ::::b:: x ::\ud800'`. | executed, approved |
| SEC-9 class names from a closed set | Tones come from `PEN_CODES` / legacy constants. `notes_html` uses `html.escape`. TC-4209 asserts the set. | Fuzz: every `class="…"` matched `hl-(mut\|over\|orange\|soon\|green\|blue\|violet)( mention)?`, 0 misses. Hostile note `::b:: <script>… "q" 's' & :: ==<img onerror>== ::v::</span><b>`: every piece came out escaped (`&lt;` `&quot;` `&#x27;` `&amp;`), and only constant tags were emitted. Both report stylesheets add only constant `--orange/--blue/--violet` and `.hl-*` rules. | executed, approved |
| SEC-R2-1 `ANSI_SEQUENCES_KEYS` | `_unshadow_alt_digits`: pops a key only when it holds its 8.2.8 glyph, inside `try/except Exception`, run at import. | Import removes exactly 7 entries (338 → 331); `\x1b7` is kept. A second call and `importlib.reload` change nothing. A foreign value (`"X"`) is kept. With a `MappingProxyType` table, a missing table attribute, or a table whose `.get` raises, the call raises nothing. The parser still holds the same dict object (`_xterm_parser` imports the name), so the change takes effect. `ESC 5` → `Key("alt+5","5")`, `ESC s` → `alt+s` (base), `ESC [1;3A` → `alt+up` (base). | executed, approved |
| Markup on the new surfaces | `pen_label`, `_palette_rows`: Text pieces. `DETAILS_NOTES_LABEL` and the legend row are built from constants only. N1–N5 use `markup=False`. | `DETAILS_NOTES_LABEL` holds only `[#hex]` tags and constant text. Fuzz: `Text.from_markup(_highlight_markup(line))` never raised over 90k lines including `\ [ ] /`. A pilot recolour of `::b:: [bold]x[/] [link=file:///c:/] \\ :: ==[/]== @x` stored the text verbatim and parsed none of it. | executed, approved |
| Theme isolation | `InkArea.__init__` registers `taskboard-ink` on the instance. | Pilot: an `InkArea` and a plain `TextArea` side by side. The plain one's theme is `css`, it has no `taskboard-ink` in `_themes`, and its highlights are `{}`. The built-in css theme keeps its key count and holds 0 `pen.*` keys. | executed, approved |

Structural invariants (fuzz, 90k lines): `start ≤ inner_start ≤ inner_end ≤ end`, spans in order and
non-overlapping, no `\n` inside a span. 0 violations. `_lift_pen`'s ARCH-10 ` ::` insert and the
`action_pen_enter` split changed neither the visible text nor any tone (0 / 0).
SEC-8 (rich escape) and SEC-R2-2 (paint-time shape) are backlogged by ruling, and I do not reopen them.

## Findings

### SR-1 [MEDIUM] [design-gap] — the ink makes each keystroke on a long note line about 5× slower (2.6 s at the paste cap): Textual repaints every highlight on every wrapped row

- **What:** our code is linear, which SEC-1 verified. The highlight map then feeds Textual 8.2.8's
  `_render_line`. For each **visual** (soft-wrapped) row, `_render_line` applies **every** highlight
  of the whole document line (`line.stylize` per highlight), then `Text.divide`s the line. A long line
  dense with spans costs (visible rows × spans in the line) on every repaint. Every keystroke, the
  editor opening, and scrolling all repaint. At base `_highlights` was always empty, so this path
  never ran.
- **Where:** `modals.InkArea._build_highlight_map` / `ink_highlights` (the map has no size bound) →
  `textual/widgets/_text_area.py:1494-1508`.
- **Evidence:** t_keylat.py. A real `TaskboardApp` at 118×30, editor opened with `e`, five keystrokes
  timed with the pilot. The no-ink column replaces `modals.ink_highlights` with `lambda l: {}`.

  | one notes line | with ink | no ink |
  |---|---|---|
  | `"::b::x::"*625` (5k chars) | 178–245 ms | 66–152 ms |
  | `"::b::x::"*2500` (20k chars) | 479–669 ms | 149–202 ms |
  | `"::b::x::"*12500` (100k chars, `_MAX_PASTE_CHARS`) | **2 611–2 668 ms** | 484–516 ms |
  | `"é::b::x::"*11111` (100k chars) | **3 004–3 378 ms** | — |

  - cProfile of one keystroke at 100k chars: 599 984 `Text.stylize` calls and 18 `Text.divide` calls
    take 1.86 s, under 16 `_render_line` calls (3.64 s cumulative).
    `build_byte_to_codepoint_dict` takes only 12 ms.
  - The round-1 absolute gate ("inks in ≤ 150 ms") was set on `ink_highlights` alone, and it passes,
    so the paint path was never budgeted.
  - Impact: availability only. Nothing crashes and no data is lost. One note line, pasted or arriving
    by team sync, makes the editor nearly unusable for whoever opens that task.
- **Smallest fix:** bound the ink per line in `ink_highlights`.
  - A line longer than a cap (for example 2 000 chars), or holding more than a cap of spans (for
    example 128), gets no ink. That line shows plain in the field, and the preview beside it still
    colours it.
  - One constant, one `continue`.
  - Add a pilot latency test: the 100k-char line above, with the ink overhead per keystroke at most
    about 1.5× the no-ink run. NC: remove the cap → RED.
- **State:** `planned`.

### SR-2 [LOW] [design-gap] — `ctrl+z` right after a pen insert lets `_pen_follow` delete the user's own empty span, and that can change the visible text that gets saved

- **What:** SEC-4 round 2 accepted a delete with no visible-text check. Its premise was that an empty
  span of the pen's code at `_pen_at` is always the pair the pen inserted. Undo breaks that premise:
  - `ctrl+z` removes the inserted pair but leaves `pen` and `_pen_at` set.
  - The `SelectionChanged` that follows finds no pen span.
  - `_pen_follow` then deletes whatever empty span of that code now starts at `_pen_at`, which is the
    user's own text.
- **Where:** `modals.TaskModal._pen_follow`, the delete branch (the `target` loop and `notes.replace`).
- **Evidence:** t_pilot.py, real app, keys pressed through the pilot, then `alt+s`. The board file was
  read back.
  - `==a=::b::  ::=x`, cursor (0,4), `alt+5`, `ctrl+z` → `'==a==x'`.
    - Before, the visible text was `==a==x` (plain).
    - After, it is `a` in yellow plus `x`.
    - The save writes `'==a==x'`. The user's characters became legacy markers.
  - `keep ::b::  :: me`, cursor (0,5), `alt+5`, `ctrl+z` → `'keep  me'`. Visible text is unchanged,
    but 9 characters the user wrote are deleted and saved that way.
  - It needs an empty span of the same code exactly at the cursor, so it is rare. The blast radius is
    one line of one note.
- **Smallest fix:**
  - Record the row's text wherever `_pen_at` is written (`_pen_line`).
  - Delete only when `notes.document.get_line(row0) == _pen_line`. A cursor move leaves the line
    equal, so the LLR-4203.14 cleanup still runs. Undo, redo, paste or any other edit makes it
    differ, so nothing is deleted.
  - Add the two inputs above to TC-4257. NC: drop the equality check → RED.
- **State:** `planned`.

### SR-3 [LOW] [design-gap] — the global unshadowing makes `alt+0`..`alt+6` type the digit into every other text field

- **What:** the ARCH-1 change is process-wide. Outside `TaskModal`, whose priority pen bindings consume
  the key, `ESC <digit>` now arrives as `Key("alt+5", "5")` with `is_printable == True`. Textual's
  `Input._on_key` (`_input.py:746-753`) and `TextArea` (`_text_area.py:1841`) insert a printable
  character, so `alt+5` in a project name or a search field types `5` where it typed `∞` at base. That
  matches how base already treats `alt+<letter>`, and it widens no input path. The ruling records only
  the macOS WezTerm trade-off, not this one.
- **Where:** `modals._unshadow_alt_digits` (import time), affecting every screen.
- **Evidence:** t_ansi.py: the parser output above, plus the Textual source lines cited.
- **Smallest fix:** no code. Add one sentence to the ARCH-1 trade-off in `03-pdr-rulings.md`: "outside
  the editor, alt+digit types the digit, as alt+letter types the letter".
- **State:** `planned` (record only).

## Verdict (role tokens)

- [x] **PASS-WITH-NOTES.** No HIGH. Every accepted SEC mitigation (SEC-1..6, SEC-9, SEC-R2-1) is applied
  and was verified here (`executed`, `approved`). SR-1 (MEDIUM) is recommended before merge. It does not
  block under the role's rubric: it is a contained availability cost, with no data loss and no crash.
  SR-2 and SR-3 are LOW.
- [ ] `BLOCK — BLOCK-UNTIL:` none. [ ] Block: none.

This clearance is not the operator's authorisation for anything.

## Evidence checklist

- ✓ Each finding has what · where · evidence (a concrete input that was run) · smallest fix: SR-1..SR-3.
- ✓ Each finding has a severity and a tag: SR-1 MEDIUM design-gap, SR-2 LOW design-gap, SR-3 LOW design-gap.
- ✓ No secret values appear here. The diff touches no credential surface.
- ✓ The verdict is explicit (PASS-WITH-NOTES). No HIGH exists.
- ✓ New tool or integration: `n/a`. No dependency was added. The private Textual surfaces
  (`ANSI_SEQUENCES_KEYS`, `_build_highlight_map`/`_highlights`) were reviewed in the table above.
