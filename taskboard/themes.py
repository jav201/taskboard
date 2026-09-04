"""Visual languages for the widget — switchable, so the choice is the user's.

Each entry is a full commitment (tui-design/LANGUAGES.md), not a recolour: the
chroma budget, what carries severity, and the STRUCTURE every widget renders
with all change together. Every chromatic value was checked against the HLS
s<0.15 quantization cliff; none of these palettes lose a hue on the 256-colour
path.

A language definition is code, not a manifest: every key below is read by a
renderer — the hero (app), or the language's structure kit
(taskboard/language.py), or the theme stylesheet (tcss() here). The check is
`prototypes/verify_language.py`: mutate any structural token and the render
must change; strip colour from two languages and they must differ.

Structural tokens:
  hero      which hero mechanism app.Hero draws (corgi/naught7/dot/plain/
            framed/ansi). naught7 = the DENSE display type: numeral and
            caption drawn 7 and 5 rows tall on one full-bleed lattice, with
            no plain cell inside the glyph field
  base      the pixel base the hero numeral is drawn through (bases.py).
            Under hero="dot" this token IS the display type, not a resolution
            setting: block2/quadrant/braille subdivide the cell, while `slab`
            (ledger) and `flap` (solari) give the SAME bitmap a different
            STROKE LOGIC — slab draws heavy stems, hairline horizontals and
            serif feet on the baseline (the engraved figure a ledger prints at
            the head of an account); flap draws each digit on its own card,
            cut at the middle by a hinge row. A `flap` hero also reads the
            `flap` and `seam` colour tokens, because a card's FACE is a ground
            and a ground is the one thing a glyph cannot carry
  frame     the structure device: none · rule · single · grid · double ·
            flaps (there is no rule at all: structure is the CELL FACE every
            character is flipped onto, so the token both turns the faces on
            and denies the language a rule line) · titleblock (the frame
            stops CONTAINING and becomes the sheet's TITLE BLOCK, a 3-row
            stamp docked to the bottom corner: nothing on the page is boxed,
            and the block's two rules are the only strokes the sheet owns)
  layout    the board's INTERNAL structure device: flow (cards stand on the
            ground — what every language did before) · rail (a passive left
            rail carries the card stack under its head) · ruled (the entries
            are posted between vertical money-column rules) · lattice (head
            and cards are composed on the visible dot grid) · panel (the head
            rule is gone; head and cards are FUNCTION PLATES — solid
            plate-toned row blocks, each card carrying a two-digit code) ·
            editorial (the spread is set on a type GRID of `columns`
            columns; ONE hairline for the whole spread, not one per head) ·
            split (MASTER/DETAIL: a narrow list of compact rows drives a wide
            detail pane holding one task, and the pane's title is the screen's
            first fixation — HIERARCHY.md's sidebar+detail pattern) · trace
            (the board is a SCOPE: every phase head carries a labelled DAY
            RETICLE and every task hangs a braille trace sample off it, drawn
            from the same origin on the same cells) · strip (the board is ONE
            FULL-WIDTH MODE SURFACE: a numbered MODE STRIP names every mode
            and lights the one on screen, and the board mode under it is a
            single spec sheet whose values stand in engraved slots that align
            down the whole page — "each mode takes over the screen") ·
            schedule (the board is ONE DEPARTURE TABLE: task = row, phase =
            GATE and the gate is the reverse-video BAND that heads its block,
            state is a WORD in a status column, and every row closes with a
            seam — the only divider on the surface) · field (the board is a
            DRAWING SHEET: items lie on an open field, quantity is a
            DIMENSION SPAN `├─ 03D ─┤` whose figure stands on the span, and
            metadata hangs off each item on an EXTENSION LEADER — no
            containing box anywhere, at any width)
  hatch     the stroke a HELD item's span is filled with (blueprint). Hatching
            is a SHAPE, so "blocked" reads with the colour stripped away and
            costs the language none of its rationed chroma
  knockout  the emphasised element reverses to a pale ground with dark ink
            (blueprint). There is exactly ONE per view and it is the sheet's
            first fixation, which is why it is a token and not a style: a
            second knockout is a defect the acceptance test can name
  flap      the cell FACE a solari digit is flipped onto (solari). Passive
            structure, one step off the ground — never the accent
  seam      the ▁ that closes every schedule row (solari). It is the whole
            divider vocabulary of that language, so it is never the accent
            and no rule glyph stands beside it
  columns   how many columns the editorial grid takes at its widest (swiss).
            The grid DROPS columns rather than crushing them: a column
            narrower than a legible title measure is renounced, never wrapped
  split     (master_floor, detail_floor) in CELLS for layout="split" (nord).
            Both are read by `Nord.panes()`, which is the one geometry seat
            the renderer and the acceptance checks share, and both are
            emitted as real `min-width` rules by `Nord.composition()`. Their
            sum plus the gutter IS the width below which the board degrades
            to master-only — the split is renounced, never wrapped
  hero_fit  (sx, sy) the drawn numeral's own pixel scale for the HERO SEAT,
            overriding `bases.BASE_SCALE` (nord). A base's global scale knows
            nothing about the panel it lands in: quadrant's (3, 3) draws a
            seven-row font as ELEVEN cell rows, two past the aperture's
            nine-row hero, so the figure was trimmed of its own baseline and
            its caption never drew. The token buys the rows back by spending
            them on WIDTH, which is also where a ~1:2 cell wants them
  hero_plot (tone token, cells per sample) — the 8-week load beside the hero
            is AMBIENT CONTEXT (nord). Declared, it renders as DATAVIZ's
            one-row `spark` in the named tier instead of an h-row `plot` in
            the accent: same meter family, same shape-carries-the-data law,
            one rank down. Undeclared, the chart renders exactly as before
  rail      the rail's grey. Passive structure is NEVER the accent
  plate     the ground a function plate is stamped on (industrial). Passive
            structure, one grey step above the panel — never the accent
  rule      the ruling's ink (ledger). Passive structure, never the accent
  tick      the RETICLE's stroke — origin, week ticks and graticule lines
            (instrument). Passive structure: a graticule is never the signal,
            so it is never the accent
  unit      the ink of a reading and of the axis's unit labels (instrument).
            A label is not a datum, so it sits one step under the ink
  band      the BAND treatment. Two languages declare it and each declares
            its own payload, because a band is a ROLE (a full-width tinted
            row) and not one glyph: ledger names the HEX its every-5th line
            is tinted with; solari names the MECHANISM its heads take
            ("reverse" — ink ground, ground ink, and never a rule)
  tally     the counted mark of the tally meter — it must NOT be mistakable
            for the column rule that stands beside it (ledger)
  meter     the quantity mechanism (language.METERS)
  surface   the RASTER POSTURE (language.SURFACES) — what the language does
            when a region can be REAL PIXELS (LANGUAGES.md's eighth axis,
            added 2026-09-03): refuse | lattice | display | tint | frame |
            depth | figure | untinted. Every language must answer and several
            answer no, so a missing token is not a default it is a gap. NOTE
            the name collides with `Kit.surface()`, which is a DIFFERENT axis
            (the TCSS ground a language draws on); the token is read through
            `Kit.posture` for exactly that reason
  numbered  params/heads/rows carry functional [n] numbering
  airy      the plain hero spends rows on emptiness (swiss)
  pitch     rows per card slot — swiss spends a blank row where others ink
  dot_w     cells per lit dot on naught's lattice
  gap       cells of AIR between naught's lattice dots (0 = dense LED panel;
            round glyphs carry their own air, so adjacency stays legible)
  sel       the focus border STYLE — selection chrome is part of the language
  tempo     motion pace in ms — industrial snaps, phosphor decays
  easing    motion curve — linear is mechanical, out_expo is CRT persistence
"""
from __future__ import annotations

THEMES: dict[str, dict] = {
    # CORGI ENGINEERING — after Teenage Engineering's product language.
    # Verified traits: five colours (orange #ff6600 taken from industrial safety
    # equipment, black, white, aluminium, screen-green); monospace exclusively;
    # brutalist grids with 1-unit gutters and NO rounded corners; all-caps
    # letterspaced labels; parameters as NUMBERED controls [1][2][3][4]; and
    # "each mode takes over the screen" -- no persistent navigation chrome.
    #
    # `layout="strip"` is that last trait taken literally, and it corrects the
    # half of it this codebase had wrong. A TE panel shows its numbered
    # BUTTONS at all times and commits ONE SCREEN to the mode they select;
    # corgi previously renounced both, so three of the four modes were
    # invisible and the board mode was three scrolling columns that cut every
    # title at 80 cells. Now: a numbered mode strip that lights the mode on
    # screen, and under it ONE full-width spec sheet whose values stand in
    # engraved slots aligned down the whole page.
    "corgi": dict(
        surface='display',
        hero="corgi", frame="grid", meter="lcd", numbered=True, base="segment",
        layout="strip",                        # the board IS one mode surface
        label="Corgi Engineering", note="numbered params · 7-seg display · safety orange",
        ground="#0d0d0d", ink="#f2f2f2", mut="#9a9a9a", dim="#3a3a3a",
        accent="#ff6600",                      # identity: safety orange
        warn="#ffb000", alert="#d92b1a",       # severity now EXISTS (TE record red)
        screen="#6fe36f",                      # the OLED/LCD green
        alu="#9a9a9a",                         # aluminium: the RULE colour
        sel="solid",                           # square corners, never round
        tempo=80, easing="linear",  # motion: pace + curve
        panel="#1c1c1c", focus="#2a2a2a",
    ),
    # 0 — NAUGHT: the Nothing OS language taken seriously. Everything on one
    # dot lattice, unlit dots VISIBLE, labels drawn too, one red spent only on
    # live state.
    "naught": dict(
        surface='lattice',
        base="block2",
        hero="naught7", frame="none", meter="dotgrid", dot_w=1, gap=0,
        layout="lattice",                      # the board IS the dot grid
        label="Naught", note="round-dot lattice · mono · red only for alarm",
        ground="#000000", ink="#f5f5f5", mut="#8a8a8a", dim="#242424",
        accent="#d71921", warn="#d71921", alert="#d71921",
        calm="#f5f5f5",   # CALM/NOTICE severity renders INK, not red — red is
                          # rationed to alarm states + the focus edge (the one
                          # element of interest), per the Nothing sheets
        sel="outer",                           # the red edge marks THE focus
        tempo=120, easing="linear",  # motion: pace + curve
        panel="#0a0a0a", focus="#141414",
    ),
    # 1 — mono + one accent, drawn dot-matrix. Clinical instrument. The board
    # is a SCOPE (`layout="trace"`): the phase head carries a labelled DAY
    # RETICLE and every task hangs a braille trace sample off it from the same
    # origin, on the same cells, at ONE cell per day in every column — so two
    # columns of different widths stay comparable (DATAVIZ.md law 2) and a
    # narrow column shows a shorter HORIZON rather than a squeezed scale.
    #
    # Why the reticle is BOX DRAWING while the trace stays braille: DENSITY.md
    # measures braille as the only fully width-safe density mechanism, and
    # DATAVIZ.md law 1 requires shape (not colour) to carry the data. Splitting
    # the channels — box drawing for STRUCTURE, braille for DATA — keeps a tick
    # from ever being mistaken for a sample. The box-drawing half is safe by
    # convention, the same assumption `─` and `│` already carry here.
    #
    # The ground stays #0a0d12 against the source spec's #080c14: see PENDING's
    # twenty-ninth-pass entry — the darker value is not measurably better on
    # any check the suite runs, and this ground is verified identity.
    "instrument": dict(
        surface='lattice',
        base="braille",
        hero="dot", frame="none", meter="braille",
        layout="trace",                        # the board IS a scope screen
        tick="#333c47",                        # the graticule, never the accent
        unit="#6b7785",                        # readings and axis unit labels
        label="Instrument", note="round-dot scope · braille numerals · clinical",
        ground="#0a0d12", ink="#e8edf2", mut="#6b7785", dim="#333c47",
        accent="#2dd4bf", warn="#fbbf24", alert="#f43f5e",
        sel="outer",
        tempo=160, easing="out_cubic",  # motion: pace + curve
        panel="#0e131a", focus="#16202b",
    ),
    # 2 — structure by whitespace and alignment; ONE hairline rule. The board
    # is an EDITORIAL SPREAD (`layout="editorial"`): entries are set on a
    # 3-column type grid — subject · byline · figure — and the single hairline
    # is the masthead rule under the LEADING phase, not one rule per head.
    # The grid is what makes the promise in `note` true: before this the board
    # printed one rule per phase and spent ~70% of its measure on nothing.
    "swiss": dict(
        surface='figure',
        base="ascii",
        hero="plain", frame="rule", meter="hairline", airy=True, pitch=2,
        layout="editorial", columns=3,         # the type grid, not the flow
        label="Swiss", note="airy · plain type · one rule · structure by alignment",
        ground="#101010", ink="#f4f4f4", mut="#8a8a8a", dim="#3d3d3d",
        accent="#e2231a", warn="#e2231a", alert="#e2231a",
        sel="solid",
        tempo=240, easing="in_out_cubic",  # motion: pace + curve
        panel="#171717", focus="#1f1f1f",
    ),
    # 3 — flat functional colour on grey; everything labelled, and structure
    # is a FUNCTION PLATE, not a box. The head rule is gone: a phase is a
    # plate legend, and every task is a plate stamped with its two-digit code.
    #
    # Why selection is NOT "the plate turns accent", against the source spec:
    # `accent` and `alert` are the SAME hex here (#ff4b1f — the language's one
    # loud colour does identity AND severity), so an accent-ground plate would
    # be indistinguishable from an overdue one. Selection therefore stays the
    # `sel` border (HIERARCHY.md ranks a border as the mechanism RESERVED for
    # focus), and the plate stays passive structure.
    "industrial": dict(
        surface='display',
        base="block",
        hero="plain", frame="single", meter="boxed", numbered=True,
        layout="panel",                        # plates, not boxes
        label="Industrial", note="5 flat colours on grey · colour codes function",
        ground="#1a1a1a", ink="#f2f2f2", mut="#8f8f8f", dim="#4a4a4a",
        plate="#2e2e2e",                       # the plate's ground, never accent
        accent="#ff4b1f", warn="#ffd400", alert="#ff4b1f",
        sel="solid",
        tempo=60, easing="linear",  # motion: pace + curve
        panel="#232323", focus="#2e2e2e",
    ),
    # 4 — the terminal's own idiom, on purpose (base16 doctrine) — and the
    # board is a MASTER/DETAIL split (`layout="split"`). Measured reason, not
    # taste: colour-stripped at 118x30 nord had NO first fixation. The hero's
    # own load plot out-inked the hero numeral 61 cells to 25 inside the same
    # panel, and the brightest ink on screen belonged to TEN repeated card
    # titles. The split gives the eye one subject: the detail pane's title is
    # the only bold ink on the board and the widest single element there.
    #
    # (The hero's numeral-vs-plot imbalance is a SEPARATE defect and is still
    # open — this token cures the board, not the hero.)
    "nord": dict(
        surface='untinted',
        base="quadrant",
        hero="dot", frame="rule", meter="blocks",
        layout="split", split=(28, 34),         # (master floor, detail floor)
        # THE HERO PANEL'S FIRST FIXATION (PENDING item 0e). The split cured
        # the board; inside the panel the load chart still out-inked and
        # out-shone the headline numeral, which the row budget was clipping.
        hero_fit=(5, 2),                        # 10x7 cells, aspect 0.71
        hero_plot=("mut", 2),                   # ambient spark, 2 cells/week
        label="Nord (base16)", note="full scheme · inherits the terminal's world",
        ground="#2e3440", ink="#eceff4", mut="#7b88a1", dim="#4c566a",
        accent="#88c0d0", warn="#ebcb8b", alert="#bf616a",
        sel="round",
        tempo=140, easing="out_cubic",  # motion: pace + curve
        panel="#3b4252", focus="#434c5e",
    ),
    # DARKSIDE — Moonshot's language, ported from the Kimi fork (its themes.py
    # says the values were verified against their production CSS). Commitments:
    # achromatic greys; KMBlue is spent EXCLUSIVELY on interactive affordances
    # (knob, switch state, active tab) — passive data is grey STEPS; depth is
    # a background grey-step, never a border; lowercase register; identity is
    # a date-driven moon doodle on a deliberately recessive wordmark.
    "darkside": dict(
        surface='depth',
        base="ascii",
        hero="plain", frame="none", meter="step", layout="rail",
        label="Darkside", note="achromatic · accent = interaction only · moon doodle",
        ground="#000000", ink="#f5f5f5", mut="#737373", dim="#262626",
        rail="#262626",                        # passive structure, never blue
        accent="#1783ff",                      # KMBlue — interactivity ONLY
        warn="#ffd230", alert="#ff4f42",       # semantic, never decoration
        calm="#f5f5f5",                        # calm severity renders ink
        wordmark="#3a3a3a",                    # display type at ~42% opacity
        sel="solid",
        tempo=300, easing="in_out_cubic",      # a slow breath, never a snap
        panel="#121212", focus="#1f1f1f",
    ),
    # PRISM — Darkside's descendant, and the only language here that was
    # carried by a whole app before it was written down.  It is NOT Darkside
    # recoloured: Darkside spends its one accent on interactivity and keeps
    # everything else grey, while Prism spends colour TWICE, on two systems
    # with a written border between them.  Every hex below is taken from
    # `taskboard/views.py` on main, where Prism already ships.
    #
    #   IDENTITY hues NAME (which project this is) -- the twelve below.
    #   SEVERITY hues JUDGE (`alert` overdue, `warn` due today).
    #   `accent` CALLS ATTENTION (today's rule, focus, keys).
    #
    # No mark may wear two of those jobs.  That is a measured law, not a
    # slogan: `tests/test_palette_ration.py` on main computes euclidean rgb
    # distance across the whole palette, so re-adding a colliding hue turns it
    # red whatever the hue is called.  `amber` used to be a project colour AND
    # the due-today colour at the identical hex -- the same mark meaning two
    # things in five views -- and that collision is why the border exists.
    "prism": dict(
        surface='depth',
        base="braille",
        hero="ember", frame="none", meter="ember", layout="rail",
        label="Prism", note="two colour systems, one written border · carved ember",
        ground="#0d1117", ink="#e6edf3", mut="#8b98a5", dim="#5b6675",
        accent="#2dd4bf",                      # attention: today, focus, keys
        warn="#fbbf24", alert="#f43f5e",       # JUDGE: due today / overdue
        ash="#6b4a3f",                         # the CONSUMED field -- 4th house
        bright="#e6edf7", later="#64748b", done="#3f9c6d",
        sel="solid",
        tempo=300, easing="in_out_cubic",
        panel="#161b22", focus="#1f2630",
        # the twelve that NAME.  Order is the assignment order on main.
        # The twelve that NAME, as HEXES taken from `views.HEX` on main.  They
        # are values and not colour names on purpose: a name would have to be
        # resolved against a table this module does not own, and an
        # unresolvable name falls back to grey -- which is exactly how an
        # identity system dies quietly.
        ident="#a3e635 #4ade80 #38bdf8 #60a5fa #a78bfa #22d3ee "
              "#fb7185 #fb923c #fbbf24 #818cf8 #e879f9 #f472b6",
    ),
    # LEDGER — double-entry bookkeeping, and the ONE language printed on a
    # LIGHT ground. That single decision is what makes it unmistakable with
    # the colour stripped away: seven languages glow, this one is read.
    # Structure is ruled MONEY COLUMNS, never boxes; every gap between a name
    # and its figure closes with dot leaders (on a ledger page an open gap is
    # where a figure could be forged); quantity is tally marks in fives.
    #
    # Why `accent` is NOT the red, against the source spec: this codebase
    # spends `accent` on chrome that carries no meaning — the footer key
    # glyphs, the config cursor, the focus edge. An accent-red ledger would
    # therefore print red on decoration, and the hue would stop meaning
    # "owed" (HIERARCHY.md: a reserved semantic hue is used for nothing
    # else). So the accent is the clerk's blue-black pen and the RED PEN is
    # reserved for debt — overdue entries and nothing else.
    "ledger": dict(
        surface='refuse',
        base="slab",                           # the ENGRAVED figure, drawn
        hero="dot", frame="ruled", meter="tally", layout="ruled",
        numbered=True, pitch=1,
        label="Ledger", note="paper ground · dot leaders · red = overdue only",
        ground="#e9e1cf", ink="#1c1a15", mut="#6b6558", dim="#c4b99f",
        rule="#8a8272",                        # the ruling: grey ink
        band="#e0d7c2",                        # every 5th line of the page
        tally="▪",                             # the counted mark
        accent="#2b3a67",                      # the blue-black pen
        warn="#a8261f", alert="#a8261f",       # the RED pen: debt only
        calm="#1c1a15",                        # a calm reading is ink on paper
        sel="none",                            # selection is a MARGIN
        tempo=200, easing="linear",            # a clerk's steady hand
        panel="#f2ecdd", focus="#ded4bc",
    ),
    # SOLARI — the split-flap airport departure board. The product becomes ONE
    # SCHEDULE: a task is a ROW, a phase is a GATE, and the task's state is a
    # WORD in a status column. Commitments:
    #
    # * QUANTITY IS DIGITS, never a bar. `meter="odometer"` is the one
    #   mechanism in the set that renders a figure instead of a length — a
    #   departure board has never drawn a bar in its life, and DATAVIZ.md's
    #   greyscale law is satisfied by construction (a 3 and a 7 differ in
    #   shape without any colour at all);
    # * the SEAM is the entire divider vocabulary. No rules, no boxes, no
    #   frames: `frame="flaps"` says the structure device is the cell FACE,
    #   and every row closes with one `▁` in the `seam` tone;
    # * headers are BANDS in reverse video (`band="reverse"`), exactly as wide
    #   as the seams under them — a band one cell wider than the seam grid is
    #   the defect, so the two share one geometry seat (`Solari.fields`);
    # * AMBER IS RATIONED to selection and to values in flight (a task inside
    #   its boarding window). A calm page carries none. Red is narrower
    #   still: it appears on LATE and nowhere else.
    #
    # Why `sel="none"` against the spec's `sel="band"`: `sel` is emitted
    # verbatim as a Textual BORDER STYLE by `tcss()` below, and "band" is not
    # one — it would raise on the stylesheet, not render a band. The band is
    # not a border in any case (that is the point of it), so this language
    # spends no border and carries selection on the row's own ground, which
    # is the ledger precedent.
    "solari": dict(
        surface='refuse',
        base="flap",                           # the hero is a BANK OF CELLS
        hero="dot",
        frame="flaps", meter="odometer", numbered=False, pitch=1,
        layout="schedule",                     # the board IS the departure table
        band="reverse",                        # heads reverse, never ruled
        label="Solari", note="flap cells · reverse bands · digits, never bars",
        ground="#0b0b0c", ink="#f0ede4", mut="#6e6a60", dim="#1f1f22",
        flap="#17171a",                        # the cell face, one step off
        seam="#1f1f22",                        # the ONLY divider
        accent="#f5a300",                      # amber: selection + in flight
        warn="#f5a300", alert="#e03a2f", calm="#f0ede4",
        sel="none",                            # the band is not a border
        tempo=40, easing="linear",             # a flap snaps, it never eases
        panel="#17171a", focus="#f5a300",
    ),
    # BLUEPRINT — the cyanotype technical drawing, and the one language whose
    # FRAME MEASURES instead of containing. Commitments:
    #
    # * QUANTITY IS A DIMENSION SPAN (`meter="dimension"`). Every figure on
    #   the sheet stands ON a span between two terminators — `├─ 03D ─┤` —
    #   drawn on a SHARED, CONSTANT scale (14 days · 12 items), so two spans
    #   anywhere on the page are comparable without either knowing the other
    #   exists (DATAVIZ.md law 2 satisfied by construction rather than by a
    #   caller remembering to pass `hi`);
    # * NOTHING IS BOXED. `layout="field"` lays items on an open field with
    #   EXTENSION LEADERS carrying their metadata; `frame="titleblock"` moves
    #   the entire frame budget into a 3-row stamp docked to the bottom
    #   corner. There is no vertical stroke and no rectangle junction on the
    #   board at any width, which is a measurable law and not a taste;
    # * EMPHASIS IS KNOCKOUT, so chroma stays near zero. Exactly ONE element
    #   per view reverses to pale-ground/dark-ink — the title block's STATE
    #   cell, the only seat in this codebase that sees the whole board — and
    #   it is the sheet's first fixation. `ink`, `mut` and `dim` are all one
    #   cyan family; the silhouette is carried by spans, leaders and the
    #   block, never by hue;
    # * HELD IS HATCHED, NEVER COLOURED. A blocked item's span fills with
    #   `hatch`, which reads with the colour stripped away;
    # * ALERT IS SPENT ON OVERDUE AND NOTHING ELSE. A calm sheet carries zero
    #   `#ff7a5c`;
    # * THE DISPLAY TYPE IS A STENCILLED DRAWING NUMBER (`base="stencil"`).
    #   The figure is HOLLOW — a stroke is drawn as its edges and the inside
    #   is ground, because on a sheet the figure is the CUT — and every closed
    #   counter is broken by a BRIDGE, the uncut strip that would hold the
    #   island in a real stencil. Nothing it draws is a solid block, and
    #   nothing it draws is a box-drawing codepoint: the ten-glyph law above
    #   allows no vertical stroke and no junction, so a display type built out
    #   of `║` and `╬` would break the language it belongs to. The base is
    #   also what `Kit.mascot` renders through, so the creature is cut from
    #   the same sheet.
    #
    # Why `sel="none"` against the spec's `sel="registration"`: `sel` is
    # emitted VERBATIM as a Textual BORDER STYLE by `tcss()` below, and
    # "registration" is not one — it would raise on the stylesheet rather
    # than render a mark. Registration corners are not a border in any case
    # (that is the point of them), so they are a real mechanism instead: the
    # `┌ ┐ └ ┘` that bracket the mode on screen inside the title block. Same
    # reasoning, and the same deviation, as solari's `sel="band"`.
    "blueprint": dict(
        surface='tint',
        base="stencil",                        # the CUT figure, drawn
        hero="dot",
        frame="titleblock", meter="dimension", numbered=False, pitch=1,
        layout="field",                        # the board IS a drawing sheet
        knockout=True,                         # emphasis reverses, never glows
        hatch="╱",                             # held is HATCHED, not coloured
        label="Blueprint", note="cyanotype · dimension spans · knockout emphasis",
        ground="#123a5c", ink="#eef4f8", mut="#7fa8c4", dim="#24486b",
        accent="#eef4f8",                      # identity IS the pale ink: this
                                               # language spends no hue on
                                               # itself, only on overdue
        warn="#7fa8c4", alert="#ff7a5c",       # warn is the cyan grey — the
                                               # near-due step is BRIGHTNESS
        calm="#eef4f8",
        sel="none",                            # registration is not a border
        tempo=180, easing="out_cubic",
        panel="#0e2f4a", focus="#1a4a72",
    ),
}


# phosphor and bbs were RETIRED 2026-07-26 (user curation: "horribles").
# Their lessons stay: brightness-as-channel and decay/gradient mechanisms
# live on in language.METERS and the skill's laws; the kits are gone.
ORDER = ["naught", "corgi", "instrument", "swiss", "industrial",
         "nord", "darkside", "prism", "ledger", "solari", "blueprint"]


def tcss(name: str) -> str:
    """Theme-dependent rules, applied as an app-level stylesheet override.

    Inline styles sit ABOVE the whole TCSS cascade (ARCHITECTURE.md), so these
    are pushed as a stylesheet rather than per-widget styles — otherwise nothing
    in widget.tcss could ever override them again.

    Selection chrome is structural: the `sel` token decides the BORDER STYLE of
    focus, not just its colour — square in corgi, an outer edge in naught,
    round in nord.
    """
    t = THEMES[name]
    sel = t.get("sel", "round")
    return f"""
    Screen {{ background: {t['ground']}; color: {t['ink']}; }}
    #hero {{ background: {t['ground']}; }}
    #hero:hover {{ background: {t['panel']}; }}
    #hero:focus {{ border: {sel} {t['accent']}; }}
    .tile {{ background: {t['ground']}; }}
    .tile:hover {{ background: {t['panel']}; }}
    .tile:focus {{ background: {t['panel']}; border-left: {sel} {t['accent']}; }}
    .kb-card {{ background: {t['ground']}; }}
    .kb-card:hover {{ background: {t['panel']}; }}
    .kb-card:focus {{ background: {t['focus']}; border-left: {sel} {t['accent']}; }}
    Footer {{ background: {t['panel']}; color: {t['mut']}; }}
    FooterKey .footer-key--key {{ color: {t['accent']}; }}
    #help-box {{ background: {t['panel']}; border: {sel} {t['accent']}; }}
    #gallery-box {{ background: {t['panel']}; border: {sel} {t['accent']}; }}
    """
