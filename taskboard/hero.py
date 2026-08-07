"""The DRAWN HERO as a real module — the aperture's signature, extracted from
the widget-slice prototype so the real app's aperture view (aperture.py) can
render it without importing prototype code.

The hero RENDERS its metric (drawn dot-matrix / seven-seg / typographic),
it never labels it (tui-design/HIERARCHY.md: there is no type scale, large
type is drawn). Each language's `hero` token picks a MECHANISM:

  naught7 full-bleed round-dot lattice, numeral AND caption drawn on it,
          7 rows tall, every cell a dot — the DENSE display type
  corgi   TE spec-sheet: seven-seg display + numbered param grid
  dot     drawn numeral through the language's pixel base — which is where
          the DISPLAY TYPE lives, so `base` is as load-bearing as `hero`:
          braille (instrument), quadrant (nord), `slab` (ledger: an engraved
          figure, heavy stems, hairline bars, serif feet on the baseline) and
          `flap` (solari: a split-flap card cut by a hinge, each digit on its
          own face). The last two are drawn by bases.py; the face GROUND that
          a flap card stands on is painted here, by `flap_paint`
  plain   typographic, structure by alignment (swiss, industrial, darkside)
  framed  box-art frame + block cursor (phosphor)
  ansi    double-line box, gradient shoulders (bbs)

At board width the dead columns beside the numeral carry the 8-week load
plot (kit.plot, meter family) with its caption inside the visible row band.
"""
from __future__ import annotations

import re

from taskboard import bases as BS
from taskboard import naught as NA
from taskboard.language import mark

# 4 wide x 7 tall — the LED-numeral proportion (from the prototype's render.py)
HERO_FONT = {
    "0": (".##.", "#..#", "#..#", "#..#", "#..#", "#..#", ".##."),
    "1": ("..#.", ".##.", "..#.", "..#.", "..#.", "..#.", ".###"),
    "2": (".##.", "#..#", "...#", "..#.", ".#..", "#...", "####"),
    "3": ("####", "...#", "..#.", ".##.", "...#", "#..#", ".##."),
    "4": ("...#", "..##", ".#.#", "#..#", "####", "...#", "...#"),
    "5": ("####", "#...", "###.", "...#", "...#", "#..#", ".##."),
    "6": (".##.", "#...", "#...", "###.", "#..#", "#..#", ".##."),
    "7": ("####", "...#", "..#.", "..#.", ".#..", ".#..", ".#.."),
    "8": (".##.", "#..#", "#..#", ".##.", "#..#", "#..#", ".##."),
    "9": (".##.", "#..#", "#..#", ".###", "...#", "...#", ".##."),
    "-": ("....", "....", "....", "####", "....", "....", "...."),
    "?": (".##.", "#..#", "...#", "..#.", ".#..", "....", ".#.."),
    "!": (".#..", ".#..", ".#..", ".#..", ".#..", "....", ".#.."),
    " ": ("....", "....", "....", "....", "....", "....", "...."),
}

_TAGS = re.compile(r"\[[^\[\]]*\]")
NL = chr(10)
PLOT_CAP = "LOAD · 8 WK"


def vis_w(markup: str) -> int:
    """Visible width of one markup row (escaped brackets count as one).

    Public because it is the ONE measure for anything that has to close on a
    panel's edge: the hero's own join uses it, and so does the aperture's
    queue row (whose marker is markup and whose width is per language)."""
    return len(_TAGS.sub("", markup.replace("\\[", "\x00")))


def ambient_load(kit) -> tuple[str, int] | None:
    """The `hero_plot` token: `(tone token, cells per sample)`, or None.

    A language that declares it says the 8-week load is AMBIENT CONTEXT and
    not the panel's headline, so it is drawn as DATAVIZ's one-row `spark`
    primitive in a demoted tier instead of an h-row `plot` in the accent.
    Undeclared, `_beside_plot` renders exactly what it always did — which is
    what keeps the other nine languages byte-identical.
    """
    amb = kit.t.get("hero_plot")
    return (str(amb[0]), int(amb[1])) if amb else None


def load_width(kit, series) -> int:
    """Cells the ambient load row reserves: its samples plus its caption.

    The whole row has to be reserved or it WRAPS — the hero's oldest trap
    (a frame built wider than its widget doubles every line). The old chart
    reserved only its own columns because its caption sat on a row of its own.
    """
    amb = ambient_load(kit)
    return 0 if not amb else len(series) * amb[1] + 1 + len(PLOT_CAP)


def _beside_plot(kit, text: str, w_main: int, plot_w: int, series,
                 max_rows: int) -> str:
    """Join the load to the numeral's right. Width math runs on VISIBLE cells;
    the caption lands INSIDE the visible band (short heroes grow empty rows
    first — DATAVIZ.md law 7)."""
    rows = text.split(NL)
    amb = ambient_load(kit)
    if amb:
        # ONE ROW, IN THE AMBIENT TIER — the hero panel's first-fixation cure
        # (PENDING item 0e). Measured on nord at 118x30: the 6-row chart held
        # 36 ink cells of `accent` (the identity/interaction hue, and 6.2:1
        # against the ground) beside a headline numeral of 28 cells that the
        # panel was clipping. HIERARCHY.md ranks by area and brightness, so
        # the chart out-ranked the metric it was supporting.
        #
        # The mechanism stays the language's — `spark` is the same meter
        # family as `plot` (DATAVIZ's dispatch law), and level still rides on
        # SHAPE ('░▂▅█'), so greyscale still carries the data. What changes is
        # the TIER: the accent is swapped for the declared ambient tone for
        # the duration of the call, because a chart drawn in the identity hue
        # is spending the screen's boldness on context.
        tone_tok, per = amb
        saved = kit.c["accent"]
        kit.c["accent"] = kit.c[tone_tok]
        try:
            sp = kit.spark(series, len(series) * per)
        finally:
            kit.c["accent"] = saved
        i = len(rows) - 1
        rows[i] = (rows[i] + " " * max(0, w_main - vis_w(rows[i]))
                   + "  " + sp + f" [{kit.c['dim']}]{PLOT_CAP}[/]")
        return NL.join(rows)
    while len(rows) < min(7, max_rows):
        rows.append("")
    # THE BAND IS DATA ROWS *PLUS* ITS CAPTION, and both stand in rows this
    # panel already has. `len(rows) - 1` reserved the caption a SECOND time
    # (`kit.plot` is then asked for `ph - 1`), so at a 7-row hero the load drew
    # 5 data rows + caption in a panel that afforded 6 + caption and the bottom
    # visible row went empty — measured on the shipped aperture at 118x34,
    # industrial (pass 44's finding; the trim ORDER was never the cause, see
    # below). 7 is the band's own cap, not a budget.
    ph = min(7, len(rows))
    if ph < 4:
        return text
    prows = kit.plot(series, plot_w, ph - 1)
    prows.append(f"[{kit.c['dim']}]{PLOT_CAP}[/]")
    out = []
    for i, r in enumerate(rows):
        if i < len(prows):
            pad = " " * max(0, w_main - vis_w(r))
            r = r + pad + "  " + prows[i]
        out.append(r)
    return NL.join(out)


def dense_type(text: str, on_c: str, off_c: str, width: int,
               dot_w: int = 1, gap: int = 0, sx: int = 2) -> list[str]:
    """One band of naught's DISPLAY TYPE (`hero="naught7"`): a word drawn
    through the 3x5 dot alphabet, standing on the full-bleed lattice — every
    cell of the band is a dot, lit or unlit, never a space.

    The narrow form (`naught.label`) puts BLANK cells between letters and
    pads the band with spaces, so the type floats in void. User verdict
    2026-07-27: it read "separated" and would not resolve. `sx` is the
    horizontal pixel: at 2 it gives the cell's 1:2 aspect back and every
    stroke is 2 cells wide, which is the form to spend rows on; at 1 the
    letters are half as wide but still stand on the continuous lattice,
    which is the tier a narrow hero can still afford.
    """
    sprite = BS.scale(
        BS.from_font(text.upper(), NA._ALPHA, gap=NA.GLYPH_GAP), sx, 1)
    return NA.field(width, NA.ALPHA_ROWS, sprite, on_c, off_c,
                    dot_w=dot_w, gap=gap)


def _wrap(cap: str, dot_w: int, gap: int, sx: int, width: int) -> list[str]:
    """Wrap a caption to the drawn band by MEASURING it, not by counting
    characters. The alphabet's advances are per glyph now (a digit steps 5
    columns where a letter steps 4), so `4 * sx` per character — the old
    arithmetic here — is a fork of the metrics that happens to be right only
    for letters. `plain_width` is the one seat that answers this."""
    out: list[str] = []
    cur = ""
    for wd in cap.split():
        cand = (cur + " " + wd).strip()
        if NA.plain_width(cand, dot_w, gap, sx, True) <= width:
            cur = cand
            continue
        if cur:
            out.append(cur)
        while wd and NA.plain_width(wd, dot_w, gap, sx, True) > width:
            wd = wd[:-1]
        cur = wd
    if cur:
        out.append(cur)
    return out


def flap_paint(rows: list[str], faces, seam_row: int, face_c: str,
               seam_c: str, hinge_c: str, ink_c: str) -> list[str]:
    """Colour a `flap` render: every face gets its own GROUND, and the hinge
    row gets a different one.

    The base draws the hinge as a SHAPE, so a caller that paints nothing still
    renders a flap board; this is the second channel. Three grounds, and the
    middle one is the whole point: the face is `flap`, the ground between two
    cards stays the screen's, and the seam row is a BAND in the `seam` tone
    running edge to edge across the card — the numeral included, because a
    hinge is physical and cuts what is printed on it.

    Why the hinge LINE is `mut` and not `seam`: measured on solari, `seam`
    (#1f1f22) against the face (#17171a) is 1.06:1 — the token is defined one
    step off the GROUND, and on a lit face it is invisible. So `seam` is spent
    where it can be seen (the band) and the line on it is `mut`, 3.2:1. The
    numeral keeps the severity tone throughout, so a calm figure is calm ink
    standing on a card, never an amber one.
    """
    out = []
    for r, row in enumerate(rows):
        segs: list[tuple[str, str, str]] = []      # (text, fg, bg)
        for i, ch in enumerate(row):
            if not any(a <= i <= b for a, b in faces):
                fg, bg = ink_c, ""
            elif r == seam_row:
                fg = hinge_c if ch == BS.FLAP_SEAM_FACE else ink_c
                bg = seam_c
            else:
                fg, bg = ink_c, face_c
            if segs and segs[-1][1] == fg and segs[-1][2] == bg:
                segs[-1] = (segs[-1][0] + ch, fg, bg)
            else:
                segs.append((ch, fg, bg))
        out.append("".join(
            f"[{fg}{' on ' + bg if bg else ''}]{t}[/]" for t, fg, bg in segs))
    return out


def dense_rule(width: int, off_c: str, dot_w: int = 1, gap: int = 0) -> str:
    """The band separator: one UNLIT lattice row. A blank row here would put
    plain cells inside the glyph field and cut the panel in two."""
    return NA.field(width, 1, [], off_c, off_c, dot_w=dot_w, gap=gap)[0]


def draw(kit, value: str, caption: str, detail: str, tone: str,
         width: int, max_rows: int, series=None, source: str = "") -> str:
    """One hero frame as markup. `kit` is the language's structure kit
    (language.kit); `tone` the severity colour (calm arrives as the theme's
    `calm` token — a language may refuse red on a quiet day)."""
    st, c = kit.t, kit.c
    ink, mut, dim, accent = c["ink"], c["mut"], c["dim"], c["accent"]
    style = st.get("hero", "dot")
    plot_w = 0
    if series is not None and width >= 72:
        plot_w = load_width(kit, series) or min(36, width // 3)
        width -= plot_w + 3
    val, cap = value[:2], caption.upper()[:width]
    det = detail
    if det and len(det) > width:
        det = det[: max(0, width - 1)] + "…"
    # `detail` is the nearest deadline's TITLE (engine.sig_deadline), i.e. user
    # text, so it is escaped for BOTH parsers: rich's `escape` left `[URGENT]`
    # alone and Textual ate it out of swiss, industrial and darkside's hero.
    det = mark(det) if det else ""

    def C(s, col):
        return f"[{col}]{s}[/]"

    lines: list[str] = []

    if style == "ember":
        # PRISM'S HERO: the numeral is the HOLE, not the drawing.
        #
        # Every other hero here PAINTS its figure onto a ground. This one fills
        # the panel with a solid ember field and CARVES the digits out of it,
        # so the value exists as the absence of fire. Two things fall out of
        # that, and both are why it is a mechanism rather than a look:
        #
        #   * each cell is field or figure and never both, so the
        #     two-colours-per-cell law is satisfied BY COMPOSITION instead of
        #     being policed after the fact;
        #   * the burnt part of the field is `ash` and the live part is the
        #     accent, so the hero states the SAME quantity its meter does, in
        #     the same vocabulary, at a glance and to the digit.
        from taskboard import wave as WV
        # the caption and the detail are rows the FIELD may not spend --
        # a hero that eats its own caption is the oldest trap in this file
        reserved = (1 if cap else 0) + (1 if det else 0)
        rows_c = max(2, min(max_rows - reserved, 7))
        dots_h = rows_c * WV.DOT_ROWS
        glyph = [WV.FONT_4x7.get(ch, WV.FONT_4x7[" "]) for ch in val]
        gw = sum(len(g[0]) for g in glyph) + max(0, len(glyph) - 1)
        scale = max(1, min(3, (width * WV.DOT_COLS) // max(1, gw * 2)))
        dots_w = width * WV.DOT_COLS

        bm = WV.Bitmap(dots_w, dots_h)
        for x in range(dots_w):                 # the field, solid
            bm.fill_to(x, dots_h)

        # carve: turn the glyph's lit dots OFF, centred
        gh = len(glyph[0]) if glyph else 0
        y0 = max(0, (dots_h - gh * scale) // 2)
        x0 = max(0, (dots_w - gw * scale) // 2)
        cx = x0
        for g in glyph:
            for r, line in enumerate(g):
                for cch, ch in enumerate(line):
                    if ch != "#":
                        continue
                    for dy in range(scale):
                        for dx in range(scale):
                            yy, xx = y0 + r * scale + dy, cx + cch * scale + dx
                            if 0 <= yy < dots_h and 0 <= xx < dots_w:
                                bm.px[yy][xx] = 0
            cx += (len(g[0]) + 1) * scale

        ash = st.get("ash", dim)
        cells = bm.to_braille()
        for row in cells:
            lines.append("".join(
                C(ch, tone if ch != " " else ash) if ch != " "
                else C("░", ash) for ch in row))
        lines.append(C(cap, mut))
        if det:
            lines.append(C(det, dim))
        return chr(10).join(lines[:max_rows])

    if style == "corgi":
        scr, alu = st.get("screen", tone), st.get("alu", mut)
        inner = max(12, width - 2)
        ncol = 4
        cw = max(5, (inner - (ncol - 1)) // ncol)
        cols = [cw] * ncol
        cols[-1] += inner - (sum(cols) + ncol - 1)

        def rule(l, m, r, parts):
            return l + m.join("─" * n for n in parts) + r

        def row(cells):
            return C("│", alu) + C("│", alu).join(cells) + C("│", alu)

        seg = BS.seven_seg(val.rjust(2), w=4)
        segw = max((len(x) for x in seg), default=0)
        pad = max(0, (inner - segw) // 2)
        lines = [C(rule("┌", "─", "┐", [inner]), alu)]
        for x in seg[:7]:
            lines.append(row([C((" " * pad + x).ljust(inner)[:inner], scr)]))
        lines.append(C(rule("├", "─", "┤", [inner]), alu))
        lines.append(row([C((" " + " ".join(cap)).ljust(inner)[:inner], mut)]))
        lines.append(C(rule("├", "┬", "┤", cols), alu))
        det0 = (det.split(" - ")[0] if det else "--")
        params = [("1", "PHASE", det0), ("2", "DUE", val + "D"),
                  ("3", "MODE", "TRIAGE"), ("4", "SRC", source.upper())]
        lines.append(row([C(f"[{n}]", accent)
                          + C(f" {lab}".ljust(w - 3)[:w - 3], mut)
                          for (n, lab, _), w in zip(params, cols)]))
        lines.append(row([C(f" {v}".ljust(w)[:w], ink)
                          for (_, _, v), w in zip(params, cols)]))
        lines.append(C(rule("└", "┴", "┘", cols), alu))

    elif style == "naught7":
        dw, lg = int(st.get("dot_w", 1)), int(st.get("gap", 0))
        sprite = BS.scale(BS.from_font(val, HERO_FONT, gap=1), 2, 1)
        body_rows = max(7, min(9, max_rows - 6))
        rows = NA.field(width, body_rows, sprite, tone, dim, dot_w=dw, gap=lg)
        lines = [NL.join(rows)]
        # PROGRESSIVE DISPLAY TYPE: x2 dense -> x1 dense -> typographic. The
        # wrap is MEASURED through the alphabet's metrics (`_wrap`), because
        # the glyphs no longer share one box.
        # ALL OR NOTHING per tier: a band costs its separator + 5 rows, and
        # drawing only the lines that fit silently DROPS the rest (at 92 cells
        # "DAYS OVERDUE" wraps and the hero read "DAYS", a different fact).
        used, band = body_rows, 1 + NA.ALPHA_ROWS
        chosen: tuple[int, list[str]] | None = None
        for sx in (2, 1):
            wrapped = _wrap(cap, dw, lg, sx, width)
            if wrapped and len(wrapped) * band <= max_rows - used:
                chosen = (sx, wrapped)
                break
        if chosen:
            sx, wrapped = chosen
            for ln in wrapped:
                lines.append(dense_rule(width, dim, dw, lg))
                lines.append(NL.join(
                    dense_type(ln, mut, dim, width, dw, lg, sx)))
                used += band
        elif cap:
            lines += ["", C(cap.center(max(width, 1)), mut)]
            used += 2
        if det and used + 2 <= max_rows:
            lines += ["", C(det.center(max(width, 1)), dim)]

    elif style == "dot":
        pbase = st.get("base", "block2")
        fit = st.get("hero_fit")
        if fit:
            # THE FIGURE IS DRAWN TO THE PANEL IT STANDS IN, not to the base's
            # global scale (PENDING item 0e). `BASE_SCALE` is one number per
            # base, shared by every seat, and nord's quadrant (3, 3) produces
            # ELEVEN rows for a seven-row font — two more than the aperture's
            # nine-row hero budget. The trim at the end of this function then
            # cut the figure's own baseline off (a `2` lost its bottom bar and
            # read as a fragment) AND dropped the caption entirely, so the
            # panel's headline was an illegible mark with nothing naming it.
            #
            # `hero_fit` is the language's own (sx, sy) for this seat: it buys
            # the missing rows back by spending them on WIDTH instead, which
            # is also the honest direction — a terminal cell is ~1:2, and at
            # (3, 3) the figure's visual aspect was 0.27 against the drawn-type
            # bracket of [0.55, 0.80]. Declared per language, so every base
            # that already fits its budget is untouched.
            rows = BS.render(BS.scale(BS.from_font(val, HERO_FONT, gap=1),
                                      *fit), pbase)
        else:
            rows = BS.draw_numeral(val, pbase, HERO_FONT)
        nw = max((len(r) for r in rows), default=0)
        pad = max(0, (width - nw) // 2)
        if pbase == "flap":
            # the FACE is a ground, and a ground is the one thing a glyph
            # cannot carry: the base draws the hinge, this paints the cards
            body = NL.join(" " * pad + r for r in flap_paint(
                rows, BS.flap_faces(val, HERO_FONT), BS.flap_seam(len(rows)),
                st.get("flap", dim), st.get("seam", dim), mut, tone))
        else:
            body = C(NL.join(" " * pad + r for r in rows), tone)
        lines = [body, "", C(cap.center(max(width, 1)), mut)]
        if det:
            lines.append(C(det.center(max(width, 1)), dim))

    elif style == "plain":
        airy = st.get("airy", False)
        label = kit.display_cap(caption)[:width]
        lines = ([""] if airy else []) + [
            C(label, mut),
            "",
            C(val, tone) + C("   " + (st.get("unit", "")), dim),
        ]
        if airy:
            lines.append("")
        if det:
            lines.append(C(det, dim))
        if airy:
            lines += ["", C("─" * width, dim)]

    elif style == "framed":
        rows = BS.draw_numeral(val, st.get("base", "block"), HERO_FONT)
        inner = max(4, width - 2)
        pad = max(0, (inner - max((len(r) for r in rows), default=0)) // 2)
        tl, hz, tr, bl, br = (("╔", "═", "╗", "╚", "╝")
                              if st.get("frame") == "double"
                              else ("┌", "─", "┐", "└", "┘"))
        body = ["│" + (" " * pad + r).ljust(inner)[:inner] + "│" for r in rows]
        lines = ([C(tl + hz * inner + tr, dim)]
                 + [C(b, tone) for b in body]
                 + [C(bl + hz * inner + br, dim), ""])
        lines.append(C((cap + " █").center(max(width, 1)), mut))
        if det:
            lines.append(C(det.center(max(width, 1)), dim))

    else:  # "ansi"
        rows = BS.draw_numeral(val, st.get("base", "half"), HERO_FONT)
        inner = max(4, width - 2)
        pad = max(0, (inner - max((len(r) for r in rows), default=0)) // 2)
        side = max(0, (inner - len(cap) - 2) // 2)
        fill = ("░▒▓" * inner)[:side]
        head = ("╔" + fill + " " + cap + " " + fill).ljust(inner + 1, "═") + "╗"
        bot = "╚" + "═" * inner + "╝"
        body = ["║" + (" " * pad + r).ljust(inner)[:inner] + "║" for r in rows]
        lines = ([C(head[:width + 2], accent)]
                 + [C(b, tone) for b in body] + [C(bot, accent)])
        if det:
            lines.append(C(det.center(max(width, 1)), mut))

    # trim VISUAL rows, not entries: a naught entry holds a 7-row field, so
    # slicing `lines` lets a "9-row" hero render 21 rows and push everything
    # below it off-screen (found by the aperture's row budget, region-measured)
    #
    # The trim runs BEFORE the join on purpose, and moving it after would be a
    # NO-OP: `_beside_plot` never returns more rows than it was given (it pads
    # only up to `min(7, max_rows)`), so the join already sees the panel's
    # post-trim height. Pass 44 read the renounced plot row as a trim-order
    # defect; it was the join's own arithmetic, cured there.
    text = NL.join(NL.join(lines).split(NL)[:max_rows])
    if plot_w:
        text = _beside_plot(kit, text, width, plot_w, series, max_rows)
    return text
