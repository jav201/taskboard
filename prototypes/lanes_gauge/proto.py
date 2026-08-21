"""Lanes as project columns — ROUND 2: faceted polygon dials (C family).

Round 1's winner was C (countdown); its circle quantizes badly at 2x4 dots per
cell — a curve becomes an irregular staircase, which is why the gauge "looks
strange". This round replaces the circle with a half-OCTAGON and a
half-HEXAGON: straight edges quantize cleanly on a dot lattice, the vertices
are free tick seats, and a flat brightness per facet gives the relief the user
asked about (a "shader" in a terminal is a brightness tier per face — honest
on a polygon, dither mud on a circle).

THE ALIGNMENT: with the countdown span chosen so the vertices land on
meaningful days, geometry and semantics fuse:
  octagon −7d…+21d  -> vertices at today, +7d, +14d (weekly marks)
  hexagon −7d…+14d  -> vertices at today, +7d
The red overshoot band IS the left facet; "this week" IS the next one.

Dial direction follows the app's law (past left, future right): LATE at the
left end, FULL at the right. The needle pegs against the bezel when it enters
the red. Every open task is a tick on the dial, so the instrument sees the
whole landing pattern, not just the next one (round-1 C's blind spot).

Motion spec unchanged: 4-frame out-cubic sweep on entry; red-parked needles
tremble ±1 dot on the 4 s ambient clock.
"""
from __future__ import annotations

import math
from datetime import date

from rich.markup import escape
from rich.text import Text

from taskboard.models import Board, parse_iso
from taskboard.views import (
    HEX, _clamp_width, bottom, c, clip, fit, header, lanes_of, line, to_text,
    vis, _strip,
)
from taskboard.wave import BRAILLE_BITS

MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")

DIM, ASH, SOON, OVER, ACCENT, MUT = (HEX["dim"], HEX["ash"], HEX["soon"],
                                     HEX["over"], HEX["accent"], HEX["mut"])


def _sh(hex6: str, k: float) -> str:
    """A brightness tier of a hex — the honest 'shader': flat per facet."""
    r = min(255, int(int(hex6[1:3], 16) * k))
    g = min(255, int(int(hex6[3:5], 16) * k))
    b = min(255, int(int(hex6[5:7], 16) * k))
    return f"#{r:02x}{g:02x}{b:02x}"


def _tag(style: str, text: str) -> str:
    return f"[{style}]{text}[/]"


# ---------------------------------------------------------------------------
# dot engine with draw ranks (a cell keeps its highest-rank tone)
# ---------------------------------------------------------------------------
def _set(dots: dict, x: int, y: int, style: str, rank: int) -> None:
    if x < 0 or y < 0:
        return
    cur = dots.get((x, y))
    if cur is None or rank >= cur[1]:
        dots[(x, y)] = (style, rank)


def _line(dots: dict, x0: float, y0: float, x1: float, y1: float,
          style: str, rank: int) -> None:
    steps = max(1, int(2 * max(abs(x1 - x0), abs(y1 - y0))))
    for i in range(steps + 1):
        t = i / steps
        _set(dots, round(x0 + (x1 - x0) * t), round(y0 + (y1 - y0) * t),
             style, rank)


def _pt(cx: int, cy: int, r: float, frac: float) -> tuple[float, float]:
    """The point at fraction `frac` of the semicircle (0 = left, 1 = right)."""
    th = math.pi * (1 - frac)
    return cx + r * math.cos(th), cy - r * math.sin(th)


def _arc(dots, cx, cy, r, f0, f1, style, rank) -> None:
    steps = max(8, int(3.2 * r * abs(f1 - f0)))
    for i in range(steps + 1):
        x, y = _pt(cx, cy, r, f0 + (f1 - f0) * i / steps)
        _set(dots, round(x), round(y), style, rank)
        x, y = _pt(cx, cy, r - 1, f0 + (f1 - f0) * i / steps)
        _set(dots, round(x), round(y), style, rank)


def _facet(dots, cx, cy, r, f0, f1, style, rank) -> None:
    """A STRAIGHT edge between the two vertex fractions, 2 dots thick — the
    polygon's facet, where the arc's curve used to stair-step."""
    x0, y0 = _pt(cx, cy, r, f0)
    x1, y1 = _pt(cx, cy, r, f1)
    _line(dots, x0, y0, x1, y1, style, rank)
    x0, y0 = _pt(cx, cy, r - 1, f0)
    x1, y1 = _pt(cx, cy, r - 1, f1)
    _line(dots, x0, y0, x1, y1, style, rank)


def _needle(dots, cx, cy, r, frac, length=None) -> None:
    th = math.pi * (1 - max(0.0, min(1.0, frac)))
    tip = (r - 2) if length is None else length
    for i in range(tip * 2 + 1):
        d = i / 2
        _set(dots, round(cx + d * math.cos(th)), round(cy - d * math.sin(th)),
             ACCENT, 5)
    for dx in (0, 1):
        for dy in (0, 1):
            _set(dots, cx - 1 + dx, cy - 1 + dy, ACCENT, 5)


def _tick(dots, cx, cy, r, frac, style, rank=2) -> None:
    th = math.pi * (1 - max(0.0, min(1.0, frac)))
    for rr in range(r - 4, r - 1):
        _set(dots, round(cx + rr * math.cos(th)),
             round(cy - rr * math.sin(th)), style, rank)


def dial(cells_w: int, rows: int, build) -> list[str]:
    dots: dict = {}
    cx, cy = cells_w, rows * 4 - 1
    r = min(cells_w * 2 - 3, rows * 4 - 3)
    build(dots, cx, cy, r)
    out = []
    for r0 in range(0, rows * 4, 4):
        parts = []
        for c0 in range(0, cells_w * 2, 2):
            bits = 0
            best = None
            for dr in range(4):
                for dc in range(2):
                    cell = dots.get((c0 + dc, r0 + dr))
                    if cell:
                        bits |= BRAILLE_BITS[(dr, dc)]
                        if best is None or cell[1] >= best[1]:
                            best = cell
            parts.append(_tag(best[0], chr(0x2800 + bits)) if best else " ")
        out.append("".join(parts))
    return out


# ---------------------------------------------------------------------------
# task rows / column chrome (unchanged from round 1)
# ---------------------------------------------------------------------------
def _chip(t, today: date) -> tuple[str, str]:
    d = parse_iso(t.due_date)
    if d is None:
        return "—", "dim"
    txt = f"{MONTHS[d.month - 1]} {d.day}"
    delta = (d - today).days
    if delta < 0:
        return txt, "over"
    if delta == 0:
        return txt, "accent"
    if delta <= 7:
        return txt, "soon"
    return txt, "mut"


def _task_row(t, board: Board, lane, wc: int, selected: bool, today: date,
              with_chip: bool) -> str:
    prefix = "▲ " if t.blocked else "▊ "
    pcol = "over" if t.blocked else lane.hue
    right: list[tuple[str, str]] = [_chip(t, today)] if with_chip else []
    rw = sum(vis(t) for t, _ in right) + len(right)
    title_w = max(0, wc - len(prefix) - rw - 1)
    shown = clip(t.title, title_w)
    body = escape(shown)
    if selected:
        body = f"[reverse]{body}[/reverse]"
    right_markup = " ".join(c(t, k) for t, k in right)
    pad = " " * max(0, wc - len(prefix) - vis(shown) - rw - 1)
    return (c(prefix, pcol) + c(body, "mut") + pad
            + (" " + right_markup if right else ""))


def _col_header(lane, wc: int) -> str:
    return c("▐ ", lane.hue) + c(escape(fit(clip(lane.name.upper(), wc - 2),
                                            wc - 2)), lane.hue, bold=True)


def _center(markup: str, wc: int) -> str:
    pad = max(0, wc - vis(_strip(markup)))
    return " " * (pad // 2) + markup + " " * (pad - pad // 2)


def _list_order(lane) -> list:
    dated = [t for t in lane.open if parse_iso(t.due_date)]
    undated = [t for t in lane.open if not parse_iso(t.due_date)]
    return sorted(dated, key=lambda t: parse_iso(t.due_date)) + undated


# ---------------------------------------------------------------------------
# dial builds
# ---------------------------------------------------------------------------
def _task_ticks(dots, cx, cy, r, lane, today: date, frac_of) -> tuple[int, int]:
    """One tick per dated open task; returns (off_left, off_right) counts —
    work off the dial is FLAGGED at its own end, never silently dropped."""
    off_l = off_r = 0
    for t in lane.open:
        d = parse_iso(t.due_date)
        if d is None:
            continue
        f = frac_of((d - today).days)
        if f < 0:
            off_l += 1
            continue
        if f > 1:
            off_r += 1
            continue
        tone = (OVER if d < today else ACCENT if d == today
                else HEX.get(lane.hue, MUT))
        _tick(dots, cx, cy, r, f, tone, 4 if d < today else 2)
    return off_l, off_r


def _build_a(lane, today: date, sweep: float):
    """Round-1 pressure gauge, kept for the record."""
    if lane.open:
        late_frac = len(lane.late) / len(lane.open)
        dues = [(parse_iso(t.due_date) - today).days
                for t in lane.open if parse_iso(t.due_date)]
        prox = (21 - max(-7, min(21, min(dues)))) / 28 if dues else 0.0
        target = 0.6 * late_frac + 0.4 * prox
    else:
        target = 0.0

    def build(dots, cx, cy, r):
        _arc(dots, cx, cy, r, 0.0, 1.0, DIM, 1)
        _arc(dots, cx, cy, r, 0.55, 0.8, SOON, 3)
        _arc(dots, cx, cy, r, 0.8, 1.0, OVER, 4)
        _needle(dots, cx, cy, r, target * sweep)
    hub, _days = _c_hub(lane, today)
    return build, hub, None


def _build_b(lane, today: date, sweep: float, start, due):
    """Round-1 project clock, kept for the record."""
    span_ok = start and due and due > start
    pos = (today - start).days / (due - start).days if span_ok else None

    def build(dots, cx, cy, r):
        if pos is None:
            _arc(dots, cx, cy, r, 0.0, 1.0, DIM, 1)
            _needle(dots, cx, cy, r, 0.0)
            return
        elapsed = max(0.0, min(1.0, pos))
        _arc(dots, cx, cy, r, 0.0, 1.0, DIM, 1)
        if elapsed:
            _arc(dots, cx, cy, r, 0.0, elapsed, ASH, 1)
        for t in lane.open:
            d = parse_iso(t.due_date)
            if d is None:
                continue
            f = (d - start).days / (due - start).days
            if 0 <= f <= 1:
                _tick(dots, cx, cy, r, f,
                      OVER if d < today else ACCENT if d == today
                      else HEX.get(lane.hue, MUT),
                      4 if d < today else 2)
        _needle(dots, cx, cy, r, elapsed * sweep)
    return build, None, None


# --- the C family: countdown ------------------------------------------------
def _c_hub(lane, today: date):
    """(hub markup, next-due offset or None) — shared by the whole family.
    Column-tight: the count rides as a bare `·N`, the word is noise."""
    dues = [(parse_iso(t.due_date) - today).days
            for t in lane.open if parse_iso(t.due_date)]
    if not dues:
        return c(f"{len(lane.open)} open · no dates", "dim"), None
    days = min(dues)
    nxt = min((t for t in lane.open if parse_iso(t.due_date)),
              key=lambda t: parse_iso(t.due_date))
    d = parse_iso(nxt.due_date)
    chip = f"{MONTHS[d.month - 1]} {d.day}"
    hub = (_tag(OVER, chip) + c(f" ▲{-days}d", "over") if days < 0
           else c(chip, "accent" if days == 0 else "mut"))
    return hub + c(f" ·{len(lane.open)}", "dim"), days


def _build_c_round(lane, today: date, sweep: float):
    """The round countdown, this time WITH the task ticks it lacked."""
    span = (-7, 21)
    frac_of = lambda d: (d - span[0]) / (span[1] - span[0])   # noqa: E731
    hub, days = _c_hub(lane, today)
    today_f = frac_of(0)
    target = frac_of(max(span[0], min(span[1], days))) if days is not None else None

    def build(dots, cx, cy, r):
        _arc(dots, cx, cy, r, 0.0, 1.0, DIM, 1)
        _arc(dots, cx, cy, r, today_f, frac_of(7), SOON, 3)
        _arc(dots, cx, cy, r, 0.0, today_f, OVER, 4)
        off = _task_ticks(dots, cx, cy, r, lane, today, frac_of)
        if target is not None:
            pegged = target < today_f
            _needle(dots, cx, cy, r, target * sweep,
                    length=r if pegged else None)
        else:
            _needle(dots, cx, cy, r, 0.0)
        build.off = off
    labels = (c(f"{span[0]}d", "dim"), c(f"+{span[1]}d", "dim"))
    return build, hub, labels


def _build_c_poly(lane, today: date, sweep: float, sides: int):
    """The faceted countdown: sides=4 octagon, sides=3 hexagon. The vertices
    land on meaningful days by construction, so each FACET is a zone."""
    if sides == 4:
        span = (-7, 21)            # vertices at today, +7d, +14d
        facet_k = (1.00, 1.22, 0.90, 0.72)     # light from the top-left
    else:
        span = (-7, 14)            # vertices at today, +7d
        facet_k = (1.00, 1.20, 0.78)
    frac_of = lambda d: (d - span[0]) / (span[1] - span[0])   # noqa: E731
    hub, days = _c_hub(lane, today)
    today_f = frac_of(0)
    target = frac_of(max(span[0], min(span[1], days))) if days is not None else None
    edges = [(i / sides, (i + 1) / sides) for i in range(sides)]

    def build(dots, cx, cy, r):
        for i, (f0, f1) in enumerate(edges):
            zone = OVER if f1 <= today_f else SOON if f0 < frac_of(7) else DIM
            _facet(dots, cx, cy, r, f0, f1, _sh(zone, facet_k[i]),
                   4 if zone is OVER else 3 if zone is SOON else 1)
        off_ticks = _task_ticks(dots, cx, cy, r, lane, today, frac_of)
        if target is not None:
            pegged = target < today_f
            _needle(dots, cx, cy, r, target * sweep,
                    length=r if pegged else None)
        else:
            _needle(dots, cx, cy, r, 0.0)
        build.off = off_ticks
    labels = (c(f"{span[0]}d", "dim"), c(f"+{span[1]}d", "dim"))
    return build, hub, labels


# ---------------------------------------------------------------------------
# the view
# ---------------------------------------------------------------------------
def render_gauge_board(board: Board, show_archived, selected_id, today: date,
                       width: int, height: int, variant: str,
                       sweep: float = 1.0) -> Text:
    today = today or date.today()
    w = _clamp_width(width)
    inner = w - 2
    h = height or 24
    lanes = list(lanes_of(board, show_archived, today))
    proj_dates = {p.name: (parse_iso(p.start_date), parse_iso(p.due_date))
                  for p in board.visible_projects(show_archived)}

    n_cols = max(1, inner // 19)
    col_w = (inner - (n_cols - 1)) // n_cols
    shown, hidden = lanes[:n_cols], lanes[n_cols:]

    live = [t for t in board.visible_tasks(show_archived) if not t.archived]
    open_n = sum(1 for t in live if not board.is_done(t))
    due_n = sum(1 for t in live if (d := parse_iso(t.due_date)) is not None
                and (d - today).days <= 0 and not board.is_done(t))
    right = c(f"{open_n} open · ", "mut") + c(f"{due_n} due", "over", bold=True)
    if hidden:
        right = c(f"+{len(hidden)} lanes ", "dim") + right
    mode = {"a": "pressure", "b": "clock", "round": "countdown · round",
            "oct": "countdown · octagon", "hex": "countdown · hexagon",
            "torus": "countdown · torus 3d",
            "wash": "countdown · torus wash",
            "sand": "hourglass", "mercury": "mercury",
            "sediment": "sediment bar"}[variant]
    lines = [header(c("◆ TASKBOARD", "accent", bold=True)
                    + c(f" · {mode}", "mut"), right, w)]

    DIAL_ROWS = 5
    columns: list[list[str]] = []
    for lane in shown:
        if variant in ("torus", "wash"):
            rows3, (off_l, off_r), hub, labels = _build_c_torus(
                lane, today, sweep, variant, col_w, DIAL_ROWS)
            col = [_col_header(lane, col_w)] + list(rows3)
        elif variant == "sand":
            start, due = proj_dates.get(lane.name, (None, None))
            build, hub, labels, srows = _build_sand(lane, today, start, due,
                                                    col_w, sweep)
            col = [_col_header(lane, col_w)]
            col += dial(col_w, srows, build)
            off_l, off_r = getattr(build, "off", (0, 0))
        elif variant == "sediment":
            srows, (off_l, off_r), hub, labels = _sediment_rows(
                lane, today, col_w, sweep)
            col = [_col_header(lane, col_w)] + list(srows)
        elif variant == "mercury":
            start, due = proj_dates.get(lane.name, (None, None))
            if start and due and due > start:
                left_n = (due - today).days
                hub = (c(f"▲{-left_n}d over", "over") if left_n < 0
                       else c(f"{left_n}d left", "mut"))
                hub += c(f" ·{len(lane.open)}", "dim")
            else:
                hub = c(f"{len(lane.open)} open · no dates", "dim")
            labels = None
            off_l = off_r = 0
            col = [_col_header(lane, col_w - 3), _center(hub, col_w - 3)]
            for t in _list_order(lane):
                col.append(_task_row(t, board, lane, col_w - 3,
                                     t.id == selected_id, today,
                                     with_chip=True))
            columns.append(col)
            continue
        else:
            if variant == "a":
                build, hub, labels = _build_a(lane, today, sweep)
            elif variant == "b":
                start, due = proj_dates.get(lane.name, (None, None))
                build, hub, labels = _build_b(lane, today, sweep, start, due)
                if due is None or start is None:
                    hub = c(f"{len(lane.open)} open · no dates", "dim")
                    labels = None
                else:
                    left_n = (due - today).days
                    hub = (c(f"▲{-left_n}d over", "over") if left_n < 0
                           else c(f"{left_n}d left", "mut"))
                    labels = (c(f"{MONTHS[start.month - 1]} {start.day}", "dim"),
                              c(f"{MONTHS[due.month - 1]} {due.day}", "dim"))
            elif variant == "round":
                build, hub, labels = _build_c_round(lane, today, sweep)
            else:
                build, hub, labels = _build_c_poly(lane, today, sweep,
                                                   4 if variant == "oct" else 3)
            col = [_col_header(lane, col_w)]
            col += dial(col_w, DIAL_ROWS, build)
            off_l, off_r = getattr(build, "off", (0, 0))
        col.append(_center(hub, col_w))
        if labels:
            lft, rgt = labels
            if off_l:
                lft = c("◂ ", "mut") + lft     # work fell off the past end
            if off_r:
                rgt = rgt + c(" ▸", "mut")     # work lands beyond the dial
            gap = " " * max(1, col_w - vis(_strip(lft)) - vis(_strip(rgt)))
            col.append(lft + gap + rgt)
        else:
            col.append(" " * col_w)
        for t in _list_order(lane):
            col.append(_task_row(t, board, lane, col_w,
                                 t.id == selected_id, today,
                                 with_chip=True))
        columns.append(col)

    footers = [c(f"{ln.done_n}/{ln.total} done", "dim") for ln in shown]
    sep = c("│", "frame")
    body_rows = h - 2
    for r_ in range(body_rows):
        parts = []
        for ci, col in enumerate(columns):
            if variant == "mercury":
                start, due = proj_dates.get(shown[ci].name, (None, None))
                prefix = _mercury_prefix(shown[ci], today, r_, body_rows,
                                         sweep, start, due)
                if r_ == body_rows - 1:
                    content = footers[ci]
                elif r_ < len(columns[ci]):
                    content = columns[ci][r_]
                else:
                    content = ""
                parts.append(prefix + " " + _pad_c(content, col_w - 3))
            elif r_ == body_rows - 1:
                parts.append(_pad_c(footers[ci], col_w))
            elif r_ < len(col):
                parts.append(_pad_c(col[r_], col_w))
            else:
                parts.append(" " * col_w)
        lines.append(line(sep.join(parts)))
    lines.append(bottom(None, w))
    return to_text(lines, h, w)


def _pad_c(markup: str, wc: int) -> str:
    return markup + " " * max(0, wc - vis(_strip(markup)))


# ---------------------------------------------------------------------------
# ROUND 3 — the circle is back, as a 3D TORUS (M21 applied)
#
# Analytic annular-tube shading, no triangle z-buffer: the dial face-on is an
# annulus, the tube's normal at radial offset t=(rho-R)/rt is exact, and a
# small tilt sells the depth. M21's law is respected: light stays near
# top-down (ambient floor 0.35) so the zone hues survive the multiply.
# Two honest takes: "torus" folds to half-block (true gradient, coarse shape),
# "wash" keeps braille resolution and averages the shade per cell (crisp
# shape, one ink per cell).
# ---------------------------------------------------------------------------
def _rgb(hex6: str) -> tuple[int, int, int]:
    return tuple(int(hex6[i:i + 2], 16) for i in (1, 3, 5))


def _hex(rgb) -> str:
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(v))) for v in rgb)


def _mul(hex6: str, k: float) -> str:
    return _hex(tuple(v * k for v in _rgb(hex6)))


_LIGHT = (-0.45, -0.60, 0.66)            # toward the viewer, upper-left
_AMB = 0.35                              # M21: keep shade near 1 — hues live


def _torus_buf(cells_w: int, rows: int, sx: int, sy: int, span,
               tilt: float = 0.28):
    """Splat the tube into a z-buffer at (cells_w*sx) x (rows*sy) subpixels.
    Returns (buf, geo) with buf[(x,y)] = (z, hexcolor) and geo the needle's
    frame: (cx, cy, R, rt)."""
    W, H = cells_w * sx, rows * sy
    cx, cy = W / 2, H - 1
    R = min(W / 2 - 2, H - 3)
    rt = max(1.6, R * 0.30)
    ln = math.sqrt(sum(v * v for v in _LIGHT))
    lx, ly, lz = (v / ln for v in _LIGHT)
    ct, st = math.cos(tilt), math.sin(tilt)
    buf: dict = {}
    n_th = 90 * sx
    n_ro = 10 * sx
    for i in range(n_th + 1):
        th = math.pi * i / n_th                    # pi = left, 0 = right
        days = span[0] + (span[1] - span[0]) * (1 - i / n_th)
        zone = OVER if days < 0 else SOON if days < 7 else DIM
        co, si = math.cos(th), math.sin(th)
        for j in range(n_ro + 1):
            t = -1 + 2 * j / n_ro                  # tube coordinate
            zsq = 1 - t * t
            if zsq <= 0.02:
                continue
            z = rt * math.sqrt(zsq)                # the front of the tube
            rho = R + rt * t
            px = cx + rho * co
            py = -rho * si                         # screen-up is negative y
            # normal of the tube surface, before tilt
            nx, ny, nz = t * co, -t * si, z / rt
            # tilt around the X axis: top of the dial leans away
            py, pz = py * ct - z * st, py * st + z * ct
            ny, nz = ny * ct - nz * st, ny * st + nz * ct
            shade = max(_AMB, nx * lx + ny * ly + nz * lz)
            key = (round(px), round(cy + py))
            if key not in buf or pz > buf[key][0]:
                buf[key] = (pz, _mul(zone, shade))
    return buf, (cx, cy, R, rt)


def _needle3(buf: dict, geo, frac: float, pegged: bool) -> None:
    """The raised bar: lit face full accent, the shadow edge at x0.45 —
    relief on the needle itself. Sits above the ring (z = inf)."""
    cx, cy, R, rt = geo
    th = math.pi * (1 - max(0.0, min(1.0, frac)))
    tip = R if pegged else R - 1
    co, si = math.cos(th), math.sin(th)
    for i in range(int(tip * 2) + 1):
        d = i / 2
        x, y = round(cx + d * co), round(cy - d * si)
        buf[(x, y)] = (1e9, ACCENT)
        buf[(x + 1, y + 1)] = (1e9 - 1, _mul(ACCENT, 0.45))
    for dx in (0, 1):
        for dy in (0, 1):
            buf[(round(cx) - 1 + dx, round(cy) - 1 + dy)] = (1e9, ACCENT)


def _studs3(buf: dict, geo, lane, today: date, frac_of) -> tuple[int, int]:
    """Task landings as small studs standing off the tube's inner rim."""
    cx, cy, R, rt = geo
    off_l = off_r = 0
    for t_ in lane.open:
        d = parse_iso(t_.due_date)
        if d is None:
            continue
        f = frac_of((d - today).days)
        if f < 0:
            off_l += 1
            continue
        if f > 1:
            off_r += 1
            continue
        tone = (OVER if d < today else ACCENT if d == today
                else HEX.get(lane.hue, MUT))
        th = math.pi * (1 - f)
        co, si = math.cos(th), math.sin(th)
        for rr in (R - rt - 2, R - rt - 1):
            buf[(round(cx + rr * co), round(cy - rr * si))] = (1e9, tone)
    return off_l, off_r


def _fold_halfblock(buf: dict, cells_w: int, rows: int) -> list[str]:
    """1x2 subpixels per cell: upper -> bg, lower -> fg, glyph ▄ (M17's law)."""
    out = []
    for r0 in range(rows):
        parts = []
        for c0 in range(cells_w):
            up = buf.get((c0, 2 * r0))
            lo = buf.get((c0, 2 * r0 + 1))
            if up and lo:
                parts.append(f"[{lo[1]} on {up[1]}]▄[/]")
            elif lo:
                parts.append(_tag(lo[1], "▄"))
            elif up:
                parts.append(_tag(up[1], "▀"))
            else:
                parts.append(" ")
        out.append("".join(parts))
    return out


def _fold_wash(buf: dict, cells_w: int, rows: int) -> list[str]:
    """Braille-res shape; each cell's ink is the mean color of its lit dots."""
    out = []
    for r0 in range(0, rows * 4, 4):
        parts = []
        for c0 in range(0, cells_w * 2, 2):
            bits = 0
            acc = [0.0, 0.0, 0.0]
            n = 0
            for dr in range(4):
                for dc in range(2):
                    hit = buf.get((c0 + dc, r0 + dr))
                    if hit:
                        bits |= BRAILLE_BITS[(dr, dc)]
                        for k in range(3):
                            acc[k] += _rgb(hit[1])[k]
                        n += 1
            if bits:
                parts.append(_tag(_hex(tuple(v / n for v in acc)),
                                  chr(0x2800 + bits)))
            else:
                parts.append(" ")
        out.append("".join(parts))
    return out


def _build_c_torus(lane, today: date, sweep: float, mode: str,
                   cells_w: int, rows: int):
    """The countdown torus. mode 'torus' = half-block fold, 'wash' = braille
    wash. Returns (markup rows, off_left, off_right, hub, labels)."""
    span = (-7, 21)
    frac_of = lambda d: (d - span[0]) / (span[1] - span[0])   # noqa: E731
    hub, days = _c_hub(lane, today)
    today_f = frac_of(0)
    target = frac_of(max(span[0], min(span[1], days))) if days is not None else None
    sx, sy = (1, 2) if mode == "torus" else (2, 4)
    buf, geo = _torus_buf(cells_w, rows, sx, sy, span)
    offs = _studs3(buf, geo, lane, today, frac_of)
    if target is not None:
        _needle3(buf, geo, target * sweep, target < today_f)
    rows_out = (_fold_halfblock if mode == "torus" else _fold_wash)(
        buf, cells_w, rows)
    labels = (c(f"{span[0]}d", "dim"), c(f"+{span[1]}d", "dim"))
    return rows_out, offs, hub, labels


# ---------------------------------------------------------------------------
# ROUND 4 — instruments that play TO the medium (textures, straight edges,
# vertical resolution), not against its quantization
# ---------------------------------------------------------------------------
def _noise(x: int, y: int) -> float:
    """Deterministic per-dot hash in [0,1) — the sand grain."""
    n = (x * 374761393 + y * 668265263) & 0xFFFFFFFF
    n = (n ^ (n >> 13)) * 1274126177 & 0xFFFFFFFF
    return ((n ^ (n >> 16)) & 0xFFFF) / 65536


def _build_sand(lane, today: date, start, due, col_w: int, sweep: float):
    """E1 · the hourglass. Straight glass edges quantize CLEANLY in braille —
    the circle's failure mode is absent by construction. The sand carries the
    texture the user liked: grain noise + a light wash, hue for the time that
    remains, ash for the time spent — and the pile turns `over` and backs up
    the funnel when the project's date has passed. Task landings are studs on
    the left wall; a late task's stud sits in the spent sand, red."""
    rows = 8

    def build(dots, _cx, _cy, _r):
        W, H = col_w * 2, rows * 4
        cx, neck = W // 2, H // 2
        half = max(4, min(W // 2 - 2, neck - 2))
        _line(dots, cx - half, 0, cx, neck, DIM, 1)
        _line(dots, cx + half, 0, cx, neck, DIM, 1)
        _line(dots, cx - half, H - 1, cx, neck, DIM, 1)
        _line(dots, cx + half, H - 1, cx, neck, DIM, 1)
        _line(dots, cx - half, 0, cx + half, 0, DIM, 1)
        _line(dots, cx - half, H - 1, cx + half, H - 1, DIM, 1)
        if not (start and due and due > start):
            build.off = (0, 0)
            return
        span = (due - start).days
        tf = max(0.0, (today - start).days / span) * sweep
        hue = HEX.get(lane.hue, MUT)
        # upper sand: what remains
        rem = max(0.0, 1.0 - tf)
        y_s = neck - rem * (neck - 1)
        for y in range(max(1, round(y_s)), neck):
            xw = half * (1 - y / neck)
            for x in range(round(cx - xw) + 1, round(cx + xw)):
                if _noise(x, y) < 0.8:
                    _set(dots, x, y, _mul(hue, 0.72 + 0.38 * _noise(y, x)), 2)
        # the stream
        ef = min(tf, 1.35)
        apex = (H - 1) - ef * (H - 2 - neck)
        for y in range(neck + 1, max(neck + 2, round(apex)), 2):
            _set(dots, cx, y, hue, 3)
        # lower pile: what is spent — red when the date has passed
        tone_lo = OVER if tf > 1 else ASH
        for y in range(neck + 1, H - 1):
            xw = half * (1 - (H - 1 - y) / (H - 1 - neck))
            for x in range(round(cx - xw) + 1, round(cx + xw)):
                if y > apex + abs(x - cx) * 0.55 and _noise(x, y * 3) < 0.8:
                    _set(dots, x, y, _mul(tone_lo, 0.75 + 0.3 * _noise(x, y)), 2)
        # studs on the left wall at each task's date height
        off_l = off_r = 0
        for t in lane.open:
            d = parse_iso(t.due_date)
            if d is None:
                continue
            f = (d - start).days / span
            if not (0 <= f <= 1):
                off_r += 1 if f > 1 else 0
                off_l += 1 if f < 0 else 0
                continue
            y = round(f * (H - 1))
            xe = (round(cx - half + half * (y / neck)) if y <= neck
                  else round(cx - half * ((H - 1 - y) / (H - 1 - neck))))
            tone = OVER if d < today else ACCENT if d == today else hue
            _set(dots, xe - 1, y, tone, 4)
        build.off = (off_l, off_r)

    if start and due and due > start:
        left_n = (due - today).days
        hub = (c(f"▲{-left_n}d over", "over") if left_n < 0
               else c(f"{left_n}d left", "mut")) + c(f" ·{len(lane.open)}", "dim")
        labels = (c(f"{MONTHS[start.month - 1]} {start.day}", "dim"),
                  c(f"{MONTHS[due.month - 1]} {due.day}", "dim"))
    else:
        hub = c(f"{len(lane.open)} open · no dates", "dim")
        labels = None
    return build, hub, labels, rows


def _mercury_prefix(lane, today: date, r: int, body_rows: int,
                    sweep: float, start, due) -> str:
    """E2 · the vertical gauge: the strip maps the project's OWN window
    (start at the bottom, due at the top), and the mercury — time already
    consumed — rises from the bottom with the grain-noise texture. Overdue
    turns the whole column `over` and puts a ▲ cap on the rail. Landings are
    notches on the rail at their date height. ~100 levels of resolution in
    the dimension the column actually HAS."""
    top, bot = 2, body_rows - 2
    if r < top or r > bot:
        return "  "
    if not (start and due and due > start):
        return " " + c("│", "dim")
    span = (due - start).days
    f = 1 - (r - top) / max(1, bot - top)         # 1 = bottom (start), 0 = top (due)
    f_today = 1 - ((today - start).days / span) * sweep
    hue = lane.hue
    rail, rail_tone = "│", "dim"
    for t in lane.open:
        d = parse_iso(t.due_date)
        if d is None:
            continue
        ft = 1 - (d - start).days / span
        if abs(ft - f) * max(1, bot - top) < 1.0:
            rail, rail_tone = "▪", ("over" if d < today else
                                    "accent" if d == today else hue)
    if f_today < 0:                                # overdue: red, and a cap
        if r == top:
            return _tag(OVER, "▲") + c(rail, rail_tone)
        return _tag(_mul(OVER, 0.85 + 0.2 * _noise(r, 7)), "█") + c(rail,
                                                                    rail_tone)
    if f >= f_today - 1e-9:                        # below the today line: spent
        return _tag(_mul(HEX.get(hue, MUT), 0.85 + 0.2 * _noise(r, 7)), "█") \
            + c(rail, rail_tone)
    if abs(f - f_today) * max(1, bot - top) < 1.0:
        return " " + c("╎", "accent")              # the today line
    return " " + c(rail, rail_tone)


def _sediment_rows(lane, today: date, col_w: int, sweep: float):
    """E3 · the sediment bar: the countdown window as a 2-row textured band.
    The fill (consumed runway up to the next landing) is a grain ramp with
    noise; zone tints underneath; today is the accent rule; landings are
    studs in the second row."""
    span = (-7, 21)
    frac_of = lambda d: (d - span[0]) / (span[1] - span[0])   # noqa: E731
    hub, days = _c_hub(lane, today)
    target = (frac_of(max(span[0], min(span[1], days))) * sweep
              if days is not None else None)
    today_i = round(frac_of(0) * (col_w - 1))
    bar, studs = [], [" "] * col_w
    off_l = off_r = 0
    for i in range(col_w):
        f = i / (col_w - 1)
        d = span[0] + (span[1] - span[0]) * f
        zone = OVER if d < 0 else SOON if d < 7 else DIM
        if i == today_i:
            bar.append(c("╎", "accent"))
        elif target is not None and f <= target:
            n = _noise(i, 11)
            g = "▓" if n < 0.34 else "▒" if n < 0.67 else "░"
            bar.append(_tag(_mul(zone, 0.9 + 0.35 * _noise(i, 5)), g))
        else:
            bar.append(c("·", "dim"))
    for t in lane.open:
        d = parse_iso(t.due_date)
        if d is None:
            continue
        f = frac_of((d - today).days)
        if not (0 <= f <= 1):
            off_l += 1 if f < 0 else 0
            off_r += 1 if f > 1 else 0
            continue
        tone = ("over" if d < today else "accent" if d == today
                else lane.hue)
        studs[round(f * (col_w - 1))] = c("▄", tone)
    labels = (c(f"{span[0]}d", "dim"), c(f"+{span[1]}d", "dim"))
    return ["".join(bar), "".join(studs)], (off_l, off_r), hub, labels


# ---------------------------------------------------------------------------
# ROUND 5 — the grid: fewer columns, stacked layers, roomier panels.
# Mercury (the instrument the user liked) keeps the project's window on the
# panel's spine; the sediment bar (the time measurement) gets a full panel
# width; the task rows get their text back.
# ---------------------------------------------------------------------------
def _task_row_full(t, board: Board, lane, wc: int, selected: bool,
                   today: date) -> str:
    """The roomier row: prefix, title, then the right group — indicators
    (! ▤ ↗) AND the absolute date chip, which is what the narrow columns had
    to sacrifice."""
    prefix = "▲ " if t.blocked else "▊ "
    pcol = "over" if t.blocked else lane.hue
    right: list[tuple[str, str]] = []
    if t.priority == "high" and not board.is_done(t):
        right.append(("!", "ink"))
    if t.images:
        right.append(("▤", "mut"))
    if t.urls:
        right.append(("↗", "accent"))
    right.append(_chip(t, today))
    rw = sum(vis(x) for x, _ in right) + len(right)
    title_w = max(0, wc - len(prefix) - rw - 1)
    shown = clip(t.title, title_w)
    body = escape(shown)
    if selected:
        body = f"[reverse]{body}[/reverse]"
    pad = " " * max(0, wc - len(prefix) - vis(shown) - rw - 1)
    return (c(prefix, pcol) + c(body, "mut") + pad + " "
            + " ".join(c(x, k) for x, k in right))


def _panel_rows(lane, board: Board, today: date, wc: int, n_rows: int,
                selected_id, sweep: float) -> list[str]:
    """One panel's content rows (WITHOUT the mercury prefix): header, sediment
    bar + studs, hub, tasks, footer pinned to the last row."""
    bar_rows, (off_l, off_r), hub, labels = _sediment_rows(lane, today, wc,
                                                           sweep)
    start_d = None
    head = (_col_header(lane, wc - 5)
            + c(fit(f"{len(lane.open)}", 4, "right"), lane.hue))
    rows = [head] + bar_rows + [_center(hub, wc)]
    if labels:
        lft, rgt = labels
        if off_l:
            lft = c("◂ ", "mut") + lft
        if off_r:
            rgt = rgt + c(" ▸", "mut")
        rows.append(lft + " " * max(1, wc - vis(_strip(lft))
                                       - vis(_strip(rgt))) + rgt)
    tasks = _list_order(lane)
    room = n_rows - len(rows) - 1                    # footer is pinned
    shown_t = tasks if len(tasks) <= room else tasks[:max(0, room - 1)]
    for t in shown_t:
        rows.append(_task_row_full(t, board, lane, wc, t.id == selected_id,
                                   today))
    if len(tasks) > len(shown_t):
        rows.append(c(fit(f"+{len(tasks) - len(shown_t)} more", wc), "dim"))
    rows = rows[:n_rows - 1]
    rows += [""] * (n_rows - 1 - len(rows))          # the tally anchors the
    rows.append(c(f"{lane.done_n}/{lane.total} done", "dim"))   # panel's foot
    return rows


def _mercury_cell(lane, today: date, r: int, n_rows: int, sweep: float,
                  start, due) -> str:
    """The panel spine, 2 cells per panel row: same semantics as E2 —
    start at the bottom, due at the top, mercury = time consumed, red with a
    ▲ cap when overdue, notches for landings."""
    if r == 0:
        return "  "
    if not (start and due and due > start):
        return " " + c("│", "dim")
    span = (due - start).days
    top, bot = 1, n_rows - 1
    f = 1 - (r - top) / max(1, bot - top)
    f_today = 1 - ((today - start).days / span) * sweep
    rail, rail_tone = "│", "dim"
    for t in lane.open:
        d = parse_iso(t.due_date)
        if d is None:
            continue
        ft = 1 - (d - start).days / span
        if abs(ft - f) * max(1, bot - top) < 1.0:
            rail, rail_tone = "▪", ("over" if d < today else
                                    "accent" if d == today else lane.hue)
    if f_today < 0:
        if r == top:
            return _tag(OVER, "▲") + c(rail, rail_tone)
        return _tag(_mul(OVER, 0.85 + 0.2 * _noise(r, 7)), "█") \
            + c(rail, rail_tone)
    if f >= f_today - 1e-9:
        return _tag(_mul(HEX.get(lane.hue, MUT), 0.85 + 0.2 * _noise(r, 7)),
                    "█") + c(rail, rail_tone)
    if abs(f - f_today) * max(1, bot - top) < 1.0:
        return " " + c("╎", "accent")
    return " " + c(rail, rail_tone)


def render_grid_board(board: Board, show_archived, selected_id, today: date,
                      width: int, height: int, cols: int,
                      sweep: float = 1.0) -> Text:
    """The grid: `cols` panels per layer, as many stacked layers as the board
    needs. Each panel: mercury spine + header + sediment bar + hub + tasks +
    done tally."""
    today = today or date.today()
    w = _clamp_width(width)
    inner = w - 2
    h = height or 24
    lanes = list(lanes_of(board, show_archived, today))
    proj_dates = {p.name: (parse_iso(p.start_date), parse_iso(p.due_date))
                  for p in board.visible_projects(show_archived)}

    n_cols = max(1, min(cols, inner // 19))
    col_w = (inner - (n_cols - 1)) // n_cols
    layers_n = max(1, -(-len(lanes) // n_cols))
    cap = n_cols * layers_n
    shown, hidden = lanes[:cap], lanes[cap:]

    live = [t for t in board.visible_tasks(show_archived) if not t.archived]
    open_n = sum(1 for t in live if not board.is_done(t))
    due_n = sum(1 for t in live if (d := parse_iso(t.due_date)) is not None
                and (d - today).days <= 0 and not board.is_done(t))
    right = c(f"{open_n} open · ", "mut") + c(f"{due_n} due", "over", bold=True)
    if hidden:
        right = c(f"+{len(hidden)} lanes ", "dim") + right
    lines = [header(c("◆ TASKBOARD", "accent", bold=True)
                    + c(f" · grid {n_cols}×{layers_n}", "mut"), right, w)]

    body = h - 1                                     # rows after the header
    panel_h = (body - (layers_n - 1)) // layers_n    # minus inter-layer rules
    sep = c("│", "frame")
    pw = col_w - 3                                   # content width per panel

    for li in range(layers_n):
        chunk = shown[li * n_cols:(li + 1) * n_cols]
        panels = []
        for lane in chunk:
            start, due = proj_dates.get(lane.name, (None, None))
            rows = _panel_rows(lane, board, today, pw, panel_h, selected_id,
                               sweep)
            panels.append((lane, start, due, rows))
        for r_ in range(panel_h):
            parts = []
            for lane, start, due, rows in panels:
                prefix = _mercury_cell(lane, today, r_, panel_h, sweep,
                                       start, due)
                content = rows[r_] if r_ < len(rows) else ""
                parts.append(prefix + " " + _pad_c(content, pw))
            for _ in range(n_cols - len(panels)):    # empty grid slots
                parts.append(" " * (col_w - 1))
            lines.append(line(sep.join(parts)))
        if li < layers_n - 1:
            lines.append(line(c("─" * inner, "frame")))
    lines.append(bottom(None, w))
    return to_text(lines, h, w)
