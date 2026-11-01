# Code-Wire prototype — group V (views.py, report_deck.py, report_workspace.py) — Inc C

Differences from `graph-baseline.cw.md` (0a8dfaa) only. Group V owns the one scanner `colour_spans`, the derived `highlight_segments`, the focus legend row, and the two report style sheets. New: 1 node (`colour_spans`). Changed code: 4 nodes (`highlight_segments`, `legend_entries`, `report_deck.render` through its CSS, `report_workspace.render` through its CSS). Unchanged code, now traced with new-tone examples: 4 reader nodes (`notes_text`, `_highlight_markup`, `present_note_lines`, `notes_html`; `_notes_text` is in a note because it is a one-line join). Every example below was run against a scratch reference scanner outside the repo (the readers through a monkeypatched `highlight_segments`, real reader code at 0a8dfaa); no product code or test was edited. The two page builders are both named `render`, so their nodes carry the module stem (`report_deck.render`, `report_workspace.render`): with two bare `render` nodes the linter keeps one (checked: 8 nodes instead of 9). The recorder must map these two names to the module functions, not to a class.

### Scanning algorithm of colour_spans (precise)

> OPENER = `::([roygbv])::( ?)` built from PEN_CODES (lower case only). LEGACY = `views._HIGHLIGHT_RE` unchanged (`==(.*?)==|!!(.*?)!!|\+\+(.*?)\+\+`, lazy, `.` never matches `\n`).
> 1. pos = 0. Loop: lm = LEGACY.search(text, pos); om = OPENER.search(text, pos). Neither → stop.
> 2. Precedence: the match with the smaller start wins (a tie cannot happen: the first characters differ). If lm wins: emit Span(lm.start, start of its group, end of its group, lm.end, tone soon/over/green by group 1/2/3, code None); pos = lm.end; loop.
> 3. If om wins: start = om.start, inner_start = om.end (the one optional space belongs to the opener). Scan j from inner_start to the first index where text[j] == "\n", or text[j:j+2] == "::", or j == len(text).
>    a. text[j:j+2] == "::" and OPENER.match(text, j) → the next opener ends the span: inner_end = end = j (no space dropped).
>    b. text[j:j+2] == "::" otherwise → a closer: inner_end = j-1 if j-1 >= inner_start and text[j-1] == " " else j; end = j+2 (the closer never takes the opener's space).
>    c. "\n" or end of text → inner_end = end = j (the `\n` is not consumed; no space dropped).
>    Emit Span(start, inner_start, inner_end, end, PEN_CODES tone, code); pos = end; loop.
> Inside an open colour span only an opener, `::` or `\n` is looked at, so `==`, `!!`, `++` are inner text; inside a legacy span everything up to its closer is inner text. A `::` that is not an opener while no colour span is open is never looked at, so it stays in the `mut` gap. For every input with no opener the loop is exactly `LEGACY.finditer` (LLR-4201.3).

## Nodes

colour_spans
req: LLR-4201.1, LLR-4201.2, LLR-4201.4, LLR-4201.5, LLR-4201.6, LLR-4201.7, LLR-4201.8, LLR-4201.9, LLR-4204.4, HLR-4201
in: str text
out: list[Span] spans
func: the one scanner (algorithm in the note above): repeatedly the leftmost of the next legacy match and the next opener; an open colour span ends at the next opener (no space dropped), at a closer `::` (one preceding space taken as marker, never the opener's), or at `\n` / the end (no space dropped); spans in order, non-overlapping, never holding `\n`; str offsets start <= inner_start <= inner_end <= end; code None for a legacy span
module: taskboard/views.py
examples: (TC-4201) text "::v:: x ::" → one span start `0`, inner_start `6`, inner_end `7`, end `10`, tone "violet", code "v" (same shape for each of r o y g b, tones "over" "orange" "soon" "green" "blue")
examples: (TC-4202) text "a ::b:: x :: c" → spans start `2`, inner_start `8`, inner_end `9`, end `12`, tone "blue", code "b"
examples: (TC-4202) text "::b::  x  ::" → one span inner_start `6`, inner_end `9`, end `12` (inner " x ": one space dropped on each side)
examples: (TC-4203) text "==late==" → one span start `0`, inner_start `2`, inner_end `6`, end `8`, tone "soon", code `None`
examples: (TC-4204) text "::r:: open" → one span start `0`, inner_start `6`, inner_end `10`, end `10`, tone "over"
examples: (TC-4204) text "::r:: a\nb" → one span inner_start `6`, inner_end `7`, end `7` (stops before the line break)
examples: (TC-4205) text "std::vector" → spans `[]`
examples: (TC-4205) text "::bb:: t ::" → spans `[]`
examples: (TC-4206) text "::b:: x ::r:: y ::" → span 1 inner "x " (inner_start `6`, inner_end `8`, end `8`, tone "blue"); span 2 start `8`, inner_start `14`, inner_end `15`, end `18`, tone "over"
examples: (TC-4207) text "::b:: ==a== ::" → one span start `0`, inner_start `6`, inner_end `11`, end `14`, tone "blue"
examples: (TC-4207) text "==a ::b:: c==" → one span start `0`, inner_start `2`, inner_end `11`, end `13`, tone "soon", code `None`
examples: (TC-4208) text "a::b::::c" → one span start `1`, inner_start `6`, inner_end `6`, end `8`, tone "blue"
examples: (TC-4208) text "::b::  ::" (the fresh pen of LLR-4203.1) → one span inner_start `6`, inner_end `6`, end `9` (empty inner text)
examples: (TC-4227) text "::b:: std::vector ::" → one span inner_start `6`, inner_end `9`, end `11` (the first `::` inside an open span closes it; see P-V-4)
examples: (TC-4229) text "a:::b:: plan ::" → one span start `2`, inner_start `8`, inner_end `12`, end `15`, tone "blue", code "b" (OPENER.search skips the `::` at 1, which is no opener, and finds `::b::` at 2; the visible text "a:plan" is kept, P-M2-7)
examples: (TC-4228) text "é ::b:: café ☕ ::" → one span start `2`, inner_start `8`, inner_end `14`, end `17` (str offsets, not bytes)
examples: (TC-4228) over the derived set of TC-4209 (11 110 inputs) → every span has start <= inner_start <= inner_end <= end, no `\n` inside text[start:end], spans non-overlapping: 0 exceptions

highlight_segments
req: LLR-4201.1, LLR-4201.2, LLR-4201.3, LLR-4201.4, LLR-4201.5, LLR-4201.6, LLR-4201.7, LLR-4201.8, LLR-4201.9, HLR-4201
in: str text
out: list[tuple[str, str]] segments
func: derived from colour_spans (no regex of its own): each non-empty gap text[last:start] as "mut", each span's text[inner_start:inner_end] in its tone (an empty span still gives an empty segment, as base D-415 does for "!!!!"), the tail as "mut"; signature and docstring role unchanged
module: taskboard/views.py
examples: (TC-4201) text "::b:: x ::" → segments ("x", "blue") only; the same for "::r::" "over", "::o::" "orange", "::y::" "soon", "::g::" "green", "::v::" "violet" (6/6)
examples: (TC-4202) text "a ::b:: x :: c" → segments ("a ", "mut"), ("x", "blue"), (" c", "mut")
examples: (TC-4202) text "::b::x::" → segments ("x", "blue")
examples: (TC-4202) text "::b::  x  ::" → segments (" x ", "blue")
examples: (TC-4203) text "==y== !!r!!" → segments ("y", "soon"), (" ", "mut"), ("r", "over") as at base
examples: (TC-4203) text "==a== !!b!! ++c++ std::vector" → segments ("a", "soon"), (" ", "mut"), ("b", "over"), (" ", "mut"), ("c", "green"), (" std::vector", "mut"), byte-equal to base (AT-4204)
examples: (TC-4203) over `PIECES` × up to 3 of tests/test_highlight_segments.py (inputs with no `::`) → `0` differences from the base function (scratch run: 1 463 inputs, 0 differences)
examples: (TC-4204) text "::r:: open" → segments ("open", "over")
examples: (TC-4204) text "::r:: a\nb" → segments ("a", "over"), ("\nb", "mut")
examples: (TC-4205) text "a :: b" → segments ("a :: b", "mut"); "::x:: t ::", "::B:: t ::", "::bb:: t ::", "std::vector" each one "mut" segment equal to the input (5/5)
examples: (TC-4206) text "::b:: x ::r:: y ::" → segments ("x ", "blue"), ("y", "over")
examples: (TC-4206) text "::r:: ab ::::b:: x ::" (the pen switch of LLR-4203.5) → segments ("ab", "over"), ("x", "blue")
examples: (TC-4207) text "::b:: ==a== ::" → segments ("==a==", "blue")
examples: (TC-4207) text "==a ::b:: c==" → segments ("a ::b:: c", "soon")
examples: (TC-4208) text "a::b::::c" → segments ("a", "mut"), ("", "blue"), ("c", "mut"); joined "ac", no segment holds ":"
examples: (TC-4209) over pieces "ab", " ", "::b::", "::r::", "::", "==y==", "!!", "::z::", "é", "\n" × up to 4 (11 110 inputs) → 0 exceptions; joined texts equal the reference scanner's marker-free text for 100 %
examples: (TC-4227) text "::b:: std::vector ::" → segments ("std", "blue"), ("vector ::", "mut")

legend_entries
req: LLR-4202.8, HLR-4202
in: str mode; Board board; date? today = None; int width = 96; int height = 30; bool show_archived = False; TeamState? team_state = None; str team_filter = "equipo"; str? selected_id = None; str? gantt_focus = None; str? gantt_previous = None; str kanban_presentation = "grouped"; str kanban_group = "project"; str? kanban_focus = None
out: list[tuple[str, str]] entries
func: changed only in mode `focus` with any pinned task (the base condition, P-V-6): after the project spine, one new row — swatch `c("::", "mut")` + the six codes of PEN_CODES joined by " ", each `c(code, tone)`, + `c("::", "mut")` (plain "::r o y g b v::"), meaning "colour: ::code:: text ::" — then the three legacy rows exactly as at base
module: taskboard/views.py
examples: (TC-4219) mode "focus", one pinned task → entries hold one row whose swatch holds `#f43f5e`, `#fb923c`, `#fbbf24`, `#4ade80`, `#60a5fa`, `#a78bfa` and "::" (6/6 tones), meaning "colour: ::code:: text ::"; then "highlight: yellow / warning", "highlight: red / attention", "highlight: green / resolved" unchanged
examples: (TC-4219) mode "focus", no pinned task → entries empty, as at base
oracle: README.md line ~247 (the syntax sentence, proposed text in the README note below)

notes_text
req: LLR-4202.2, LLR-4202.3, LLR-4206.1, LLR-4206.2, LLR-4206.3, LLR-4206.4, HLR-4202, HLR-4206
in: str text; dict? people = None
out: Text note
func: UNCHANGED code: indexes `HEX[tone]`, and `orange`, `blue`, `violet` already are keys of views.HEX (#fb923c, #60a5fa, #a78bfa); it paints whatever tones highlight_segments gives; this node is the terminal seat of the six tones, so the C-4 checks hang here
module: taskboard/views.py
examples: (TC-4211) text "::v:: idea ::" → note "idea" with one span `#a78bfa`
examples: (TC-4212) text "::b:: ask @ana ::", people "ana" → Person("ana", "Ana Ruiz") → note "ask @Ana Ruiz": "ask " in `#60a5fa`, "@Ana Ruiz" in `b #f472b6`
examples: (TC-4220) for code r o y g b v the span styles are `#f43f5e`, `#fb923c`, `#fbbf24`, `#4ade80`, `#60a5fa`, `#a78bfa`: HLS saturation 0.892, 0.960, 0.964, 0.692, 0.939, 0.917, each >= 0.20 (6/6)
examples: (TC-4221) the same six hexes: contrast on #0d1117 5.15, 8.36, 11.34, 10.86, 7.44, 6.95 and on #0b111a 5.16, 8.36, 11.34, 10.86, 7.45, 6.96, each >= 4.5 (12/12)
examples: (TC-4222) the same six hexes under rich Color.downgrade(ColorSystem.EIGHT_BIT) → numbers 203, 209, 214, 78, 75, 141: 6 distinct, none in 232–255, none on the cube's grey diagonal (16, 59, 102, 145, 188, 231)
examples: (TC-4223) none of the six hexes equals the accent #2dd4bf (0/6)
oracle: tui-design PALETTE.md (s >= 0.15, AA 4.5:1, 256-colour downgrade); WCAG 2.x relative luminance contrast

_highlight_markup
req: LLR-4202.1, HLR-4202
in: str text
out: str markup
func: UNCHANGED code: `c(escape(segment), tone)` per segment of highlight_segments; `c` indexes HEX[tone], so the three new tones need no change
module: taskboard/views.py
examples: (TC-4210) text "::b:: x ::" → markup "[#60a5fa]x[/]"
examples: (TC-4210) text "::o:: x ::" → markup "[#fb923c]x[/]"; text "::v:: x ::" → markup "[#a78bfa]x[/]" (3/3)
examples: (TC-4203) text "==a== !!b!! ++c++ std::vector" → markup "[#fbbf24]a[/][#8b98a5] [/][#f43f5e]b[/][#8b98a5] [/][#4ade80]c[/][#8b98a5] std::vector[/]" as at base

present_note_lines
req: LLR-4202.4, HLR-4202
in: str notes; int w; dict? people = None
out: list[tuple[str, list[tuple[str, str]]]] rows
func: UNCHANGED code: tokenises each paragraph (one line) before the wrap and walks the tones onto the rows; any tone other than `mut` passes through, and `_present_note_markup` paints it with `c(…, tone)`
module: taskboard/views.py
examples: (TC-4214) notes "- ::b:: alpha :: bravo", w `40` → rows lead "• ", pieces "alpha" `blue`, " bravo" `ink`
examples: (TC-4214) notes "::b:: word00 word01 … word08 ::" (71 chars, a 62-char span), w `20` → 3 rows "word00 word01 word02", "word03 word04 word05", "word06 word07 word08", every piece `blue`

notes_html
req: LLR-4202.5, HLR-4202
in: str text; dict people
out: str html
func: UNCHANGED code: writes `class="hl-<tone>"` from the tone name, so the three new tones become `hl-orange`, `hl-blue`, `hl-violet`; the CSS rules for them are added in report_deck.render and report_workspace.render
module: taskboard/report_html.py
examples: (TC-4216) text "::b:: <x> ::", people `{}` → html "<span class=\"hl-blue\">&lt;x&gt;</span>"
examples: (TC-4216) text "::v:: idea :: and ::o:: risk ::" → html holds "hl-violet\">idea", "hl-mut\"> and ", "hl-orange\">risk" (AT-4203)
examples: (TC-4212) text "::b:: ask @ana ::", people "ana" → html "<span class=\"hl-blue\">ask </span><span class=\"hl-blue mention\">@Ana Ruiz</span>"

report_deck.render
req: LLR-4202.6, LLR-4206.5, HLR-4202, HLR-4206
in: dict d
out: str html
func: UNCHANGED function; its embedded CSS changes: `LIGHT` gains `--orange:#bc4c00;--blue:#0969da;--violet:#8250df;` (used by the light media query and by print), the dark `:root` gains `--orange:#fb923c;--blue:#60a5fa;--violet:#a78bfa;`, and line 439 gains `.hl-orange{color:var(--orange)} .hl-blue{color:var(--blue)} .hl-violet{color:var(--violet)}`
module: taskboard/report_deck.py
examples: (TC-4217) any d → html holds ".hl-orange{color:var(--orange)}", ".hl-blue{color:var(--blue)}", ".hl-violet{color:var(--violet)}" (3/3) and "--orange:#fb923c", "--blue:#60a5fa", "--violet:#a78bfa", "--orange:#bc4c00", "--blue:#0969da", "--violet:#8250df" (6/6, each var in both theme blocks)
examples: (TC-4224) the six deck tone vars on their theme's --bg: dark (#0d1117) soon 11.34, over 5.15, green 10.86, orange 8.36, blue 7.44, violet 6.95; light (#ffffff) soon #8a5a00 5.93, over #c81e4f 5.59, green #1a7f37 5.08, orange #bc4c00 5.03, blue #0969da 5.19, violet #8250df 5.05: 12/12 >= 4.5 (the NC light #60a5fa gives 2.54)
examples: (TC-4217, AT-4203) a board whose note is "::v:: idea :: and ::o:: risk ::" → the deck html holds "hl-violet" and "hl-orange" spans and both CSS rules

report_workspace.render
req: LLR-4202.7, HLR-4202, HLR-4206
in: dict d
out: str html
func: UNCHANGED function; its embedded CSS changes: the dark `:root` gains `--orange:#fb923c;--blue:#60a5fa;--violet:#a78bfa;` (the light block stays without tone vars, LED-2026-11-01-incC.2), and after `.hl-green` three rules in its exact form: `.hl-orange{background:color-mix(in srgb,var(--orange) 22%,transparent);border-radius:3px;padding:0 .15em}`, same for `.hl-blue` / `--blue` and `.hl-violet` / `--violet`
module: taskboard/report_workspace.py
examples: (TC-4218) any d → html holds ".hl-orange{background:color-mix(in srgb,var(--orange) 22%", ".hl-blue{background:color-mix(in srgb,var(--blue) 22%", ".hl-violet{background:color-mix(in srgb,var(--violet) 22%" (3/3) and "--orange:#fb923c", "--blue:#60a5fa", "--violet:#a78bfa" in `:root` (3/3)
examples: (TC-4218) ink on the 22 % tint (analysis): dark ink #e6edf3 on over 12.66, orange 10.97, soon 9.95, green 10.03, blue 11.03, violet 11.27; light ink #1f2328 on over 11.83, orange 13.24, soon 14.07, green 13.86, blue 13.06, violet 12.94 (all >= 4.5)

### C-4 analysis (computed 2026-11-01, scratch script, rich from anaconda python)

> | code | tone | hex | hue | HLS s | CR #0d1117 | CR #0b111a | 8-bit | deck light | CR #ffffff |
> |---|---|---|---|---|---|---|---|---|---|
> | r | over | #f43f5e | 350 | 0.892 | 5.15 | 5.16 | 203 | #c81e4f (base) | 5.59 |
> | o | orange | #fb923c | 27 | 0.960 | 8.36 | 8.36 | 209 | #bc4c00 (new) | 5.03 |
> | y | soon | #fbbf24 | 43 | 0.964 | 11.34 | 11.34 | 214 | #8a5a00 (base) | 5.93 |
> | g | green | #4ade80 | 142 | 0.692 | 10.86 | 10.86 | 78 | #1a7f37 (base) | 5.08 |
> | b | blue | #60a5fa | 213 | 0.939 | 7.44 | 7.45 | 75 | #0969da (new) | 5.19 |
> | v | violet | #a78bfa | 255 | 0.917 | 6.95 | 6.96 | 141 | #8250df (new, = deck --ph2 light) | 5.05 |
> LLR-4206.1 6/6 (min 0.692), LLR-4206.2 12/12 (min 5.15, over), LLR-4206.3 6 distinct non-grey, LLR-4206.4 0/6 accent, LLR-4206.5 12/12 (min 5.03, light orange). Rejected light candidates: deck --ph3 #bf6106 4.26 (fails), --ph1 #1f6feb 4.63 (passes with thin margin; #0969da kept). NCs reproduce: #8b98a5 s 0.126; #5b6675 3.25:1 on #0d1117; light #60a5fa 2.54:1.
> Near pairs (euclidean rgb, the ration's metric): orange–soon 51, blue–violet 76, over–orange 90; every other pair > 100. The 8-bit numbers keep them apart, but orange sits inside soon's 70 band (P-V-1).
> Guards: no HEX entry changes, so tests/test_colour_budget.py, tests/test_colour_budget_app.py and tests/test_palette_ration.py see the same palette; their boards hold no `::` notes, so no new tone is painted in their renders (0 edits). tests/test_legend.py ghost-mark law: full/bare boards pin nothing, so the focus legend stays empty there.

### Unchanged readers (verified by reading the code and by a scratch run with the new scanner patched in)

> - `notes_text` (views.py:3558): `HEX[tone]` per segment; `"::v:: idea ::"` → "idea" `#a78bfa`. No change.
> - `notes_preview` (modals.py, M group's file): `Text.assemble(notes_text(...))`, so it follows notes_text. No change.
> - `_highlight_markup` (views.py:3582): `"::b:: x ::"` → "[#60a5fa]x[/]". No change. Its caller `_focus_note_snippet` clips the raw line before the markup: `"::b:: a long blue note ::\nsecond"`, width 14 → "[#60a5fa]a long …[/]" (P-V-7).
> - `present_note_lines` (views.py:6695): `"- ::b:: alpha :: bravo"`, w 40 → lead "• ", ("alpha","blue"), (" bravo","ink"). No change.
> - `report_html.notes_html` (report_html.py:44): `"::b:: <x> ::"` → `<span class="hl-blue">&lt;x&gt;</span>`. No change; only the CSS rules are new.
> - `report_html._notes_text` (report_html.py:60): joins segment texts; `"::b:: x :: and ==y==\n::r:: z"` → "x and y\nz". No change (TC-4225).

### README (doc, line ~247)

> Proposed replacement of "- In notes, `==text==`, `!!text!!` and `++text++` are highlighted yellow, red and green.":
> "- In notes, `::b:: text ::` colours text: `r` red, `o` orange, `y` yellow, `g` green, `b` blue, `v` violet. A span with no closing `::` ends at the line end, and a new `::<code>::` ends the open one. Inside a colour span the first `::` closes it, so `::b:: std::vector ::` shows `std` in blue and `vector ::` plain. `==text==`, `!!text!!` and `++text++` still highlight yellow, red and green; markers inside a span of the other kind stay literal. In the task editor, `alt+1`..`alt+6` pick a pen, `alt+0` lifts it, `alt+c` recolours the selection or the word. A `::` typed under a pen closes the pen's span, and the pen turns off." (The editor sentences are M1/M2 behaviour; V only writes the line. P-V-4 ruling: the `std::vector` sentence; P-M1-5 ruling: the typed `::` sentence; the legacy-marker clause follows the reworded LLR-4201.7.)

### Seams (what M1 and M2 consume from V)

> - `[Data: PEN_CODES]`: (code, tone, name) in pen order 1..6. M1: pen label keys and chip, `alt+<n>` → code, live-ink tones. M2: the palette's 8 rows, digit → code.
> - `colour_spans(line)` → `[Span]` with str offsets: M1 `_lift_pen` (find the pen's span at the cursor; empty = inner_start == inner_end), enter handling and the cursor-leave check (cursor outside [inner_start, inner_end]), live ink (inner range in HEX[tone], marker ranges text[start:inner_start] and text[inner_end:end] in HEX["dim"]; str → byte conversion is M1's job, see TC-4228). M2: the span holding the target, overlap refusal (a target that overlaps start..end of a span without lying inside it, LLR-4205.11), recolour = replace the markers, uncolour = delete them.
> - The spaced written form `::<code>:: ` + text + ` ::` round-trips: "::b:: plan ::" → inner "plan"; the fresh pen "::b::  ::" is one empty span (TC-4208); "::r:: ab ::::b:: x ::" and "::b:: ab ::\n::b:: cd ::" tokenise as M1 expects (TC-4206, LLR-4203.7 shape).
> - `highlight_segments(text)` keeps its signature; every reader is unchanged.

## Entities

[Data: PEN_CODES]
in: tuple[tuple[str, str, str], ...]
desc: NEW, views.py, as in graph-interfaces.cw.md: ("r","over","red"), ("o","orange","orange"), ("y","soon","yellow"), ("g","green","green"), ("b","blue","blue"), ("v","violet","violet"); every tone a key of views.HEX (TC-4226: 6/6 keys, order r o y g b v)

[Data: Span]
in: NamedTuple(int start, int inner_start, int inner_end, int end, str tone, str? code)
desc: NEW, views.py, as in graph-interfaces.cw.md; str offsets of one line

[Data: views._OPENER_RE]
in: re.Pattern
desc: NEW, views.py, `::([roygbv])::( ?)` with the code class built from PEN_CODES; group 2 is the one optional space that belongs to the opener

[Data: views._HIGHLIGHT_RE]
in: re.Pattern
desc: UNCHANGED pattern; now read by colour_spans instead of highlight_segments (tests/test_highlight_segments.py still imports it as the frozen-oracle input)

[Data: views.HEX]
in: dict[str, str]
desc: UNCHANGED; already holds orange #fb923c, blue #60a5fa, violet #a78bfa

[Interface: focus legend]
desc: CHANGED: one new row after the spine: swatch "::r o y g b v::" with each code in its tone and the colons in mut, meaning "colour: ::code:: text ::"; the three legacy rows unchanged

[I/O: deck CSS]
desc: CHANGED: LIGHT + `--orange:#bc4c00;--blue:#0969da;--violet:#8250df;`; dark :root + `--orange:#fb923c;--blue:#60a5fa;--violet:#a78bfa;`; `.hl-orange{color:var(--orange)} .hl-blue{color:var(--blue)} .hl-violet{color:var(--violet)}` beside `.hl-green`

[I/O: workspace CSS]
desc: CHANGED: dark :root + `--orange:#fb923c;--blue:#60a5fa;--violet:#a78bfa;`; `.hl-orange`, `.hl-blue`, `.hl-violet` in the `.hl-soon` form (22 % color-mix background); light block unchanged

[I/O: report task dict]
desc: UNCHANGED shape; `notes_html` may now hold `hl-orange`, `hl-blue`, `hl-violet` spans

## Edges

[Data: PEN_CODES] ──▶ colour_spans
[Data: PEN_CODES] ──▶ legend_entries
[Data: views._OPENER_RE] ──▶ colour_spans
[Data: views._HIGHLIGHT_RE] ──▶ colour_spans
[Data: views.HEX] ──▶ legend_entries
[Data: views.HEX] ──▶ notes_text
[Data: views.HEX] ──▶ _highlight_markup
colour_spans.spans ──▶ highlight_segments.text
legend_entries ──▶ [Interface: focus legend]
notes_html ──▶ [I/O: report task dict].notes_html
[I/O: report task dict].notes_html ──▶ [I/O: deck CSS]
[I/O: report task dict].notes_html ──▶ [I/O: workspace CSS]
report_deck.render ──▶ [I/O: deck CSS]
report_workspace.render ──▶ [I/O: workspace CSS]

## Findings

finding P-V-1 proposal: the `o` tone is a retired hue inside soon's band, and `b`/`v` are project identity hues
anchor: notes_text
seen: (TC-4222) every C-4 threshold passes, but models.DROPPED_PROJECT_COLORS retires `orange` because it measured inside soon's 70 band (rgb distance orange–soon 51, hue 27 vs 43); tests/test_palette_ration.py::test_no_view_paints_an_identity_in_a_retired_hue says orange is "gone from the screen entirely" and passes only because its board has no `::o::` note; `blue` and `violet` are PROJECT_COLORS, and violet is the default project hue, so a violet note line can stand beside a violet spine in Focus (base already does this with `++` green)
cause: the commission maps the six pens to existing HEX keys; the ration law was written for identity and judgement marks, not user ink
effect: a note in orange can read as "due today" at a glance; the guard cannot see it
decision: ruling (03-pdr-rulings round 0): "Keep `HEX["orange"]`, `blue`, `violet` for note text. The palette-ration bands govern project hues on the board; a note tone is read with its name in the legend/pen chip, and the 256-colour numbers stay distinct (209 vs 214). No new HEX key." No graph change

finding P-V-2 proposal: LLR-4201.7's wording contradicts LLR-4201.6
anchor: colour_spans
seen: (TC-4206, TC-4207) LLR-4201.7 says every marker inside a span stays literal; LLR-4201.6 makes an opener inside an open colour span end it, and a `::` closes it
cause: the statement was written for the legacy markers only
effect: an implementer who follows .7 literally fails TC-4206
decision: ruling (03-pdr-rulings round 0): "Accept. LLR-4201.7 reworded: markers inside a legacy span, and legacy markers inside a colour span, stay literal." The graph already followed it (scanning note, TC-4207); nothing here relies on the old wording

finding P-V-3 proposal: HLR-4206 cites saturation 0.15, LLR-4206.1 sets 0.20
anchor: notes_text
seen: (TC-4220) HLR-4206 validation "(tui-design PALETTE.md: s ≥ 0.15 …)" and LLR-4206.1 "≥ 0.20"; the six tones' minimum is 0.692, so both pass
cause: the LLR tightened the PALETTE.md floor without saying so
effect: two thresholds for one property
decision: ruling (03-pdr-rulings round 0): "Accept. HLR text: 0.15 is the cliff, 0.20 the gate." Applied in 01-requirements; TC-4220 gates at 0.20

finding P-V-4 proposal: inside an open colour span the first `::` always closes it
anchor: colour_spans
seen: (TC-4227) "::b:: std::vector ::" gives ("std","blue"), ("vector ::","mut")
cause: the closer definition (`::` with ≤1 space) has no context; LLR-4201.5 covers `::` only while no span is open
effect: code-like text with `::` cannot sit inside a colour span; not covered by any LLR threshold
decision: ruling (03-pdr-rulings round 0): "Accept as designed; pinned by TC-4227; README sentence." TC-4227 pins "::b:: std::vector ::" in colour_spans and highlight_segments; the README note carries the sentence

finding P-V-5 proposal: TC-4213 and TC-4215 of V's range are used in graph-interfaces.cw.md for M1's _lift_pen
anchor: colour_spans
seen: graph-interfaces.cw.md TaskModal._lift_pen examples cite (TC-4213) and (TC-4215); V was given TC-4201..TC-4229
cause: the range split and the interface examples were written apart
effect: two tests could take one id
decision: ruling (03-pdr-rulings round 0): "Rename the interface's `_lift_pen` examples to TC-4258, TC-4259 (M1 range, free)." Done in graph-interfaces; TC-4213 and TC-4215 are free again for V (still unused here)

finding P-V-6 proposal: the focus legend lists the syntax for any pinned task, whatever the notes hold
anchor: legend_entries
seen: (TC-4219) base P-2: the highlight rows show with one pinned task even when no note holds a highlight; the new colour row follows the same condition; LLR-4202.8 states no condition
cause: base behaviour; the ghost-mark law in tests/test_legend.py is weak for these swatches (any glyph passes)
effect: the legend can name marks the view does not draw
decision: ruling (03-pdr-rulings round 0): "Backlog (base behaviour, not this increment)." legend_entries keeps the base condition

finding P-V-7 proposal: the Focus snippet clips the raw line, markers included
anchor: _highlight_markup
seen: `_focus_note_snippet("::b:: a long blue note ::\nsecond", 14)` → "[#60a5fa]a long …[/]": 14 raw cells, 8 visible; a colour span costs up to 9 marker cells, a legacy span 4
cause: base clips before tokenising (pre-existing)
effect: shorter snippets for coloured notes; the tone stays right because a cut closer leaves the span open to the line end (LLR-4201.4)
decision: ruling (03-pdr-rulings round 0): "Backlog." _focus_note_snippet unchanged
