"""Variant C — the presentation/handout deck.

The presentation's gantt re-built as REAL vector HTML: a self-contained slide
deck with a title slide, an overview slide (the 'all' view: every project of
every board on one timeline) and one slide per project. Each project slide is
an SVG gantt with selectable <text>, a today rule, phase colouring, milestone
class shapes (Delivery ▲ / Billing ■ / Launch ★), dependency arrows between
bars and the visible tasks' notes rendered with ==!!++ highlights and @Name
mentions. Arrow keys page the deck (only when not typing); on-screen buttons
serve phones.

All data is synthetic (prototypes/html_report/fixture.py). Reads taskboard
read-only; writes one HTML file. Same honesty laws as taskboard/report.py:
counts and dates only, everything user-authored escaped, direct labels on
every figure.
"""
from __future__ import annotations

import html
import importlib.util
import re
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
_spec = importlib.util.spec_from_file_location(
    "hr_fixture", ROOT / "prototypes" / "html_report" / "fixture.py")
fixture = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(fixture)

from taskboard.models import days_in_phase, parse_iso   # noqa: E402
from taskboard.people import split_mentions             # noqa: E402
from taskboard.views import HEX, highlight_segments, lanes_of, sitting  # noqa: E402

TODAY = fixture.TODAY
BOARDS = fixture.all_boards()
PEOPLE = fixture.PEOPLE
MARKS = fixture.MARKS
PHASES = fixture.PHASES

MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
OUT = ROOT / "prototypes" / "html_report" / "out" / "c-report.html"


def esc(text: object) -> str:
    return html.escape(str(text), quote=True)


def due_word(days: int | None, closed: bool = False) -> str:
    """The shipped report's ruling, replicated: a distance, never a verdict
    on closed work."""
    if days is None:
        return "no date"
    if closed:
        return f"{days:+d}d"
    if days < 0:
        return f"{-days}d overdue"
    if days == 0:
        return "due today"
    return f"in {days}d"


def _due(task):
    return parse_iso(task.due_date)


def _start(task):
    return parse_iso(task.start_date)


# ---------------------------------------------------------------------------
# notes → HTML (==!!++ highlights + @mentions), mirrors views' tokenisers
# ---------------------------------------------------------------------------

_CB = re.compile(r"^\s*[-*]\s+\[([ xX])\]\s*(.*)$")
_TONE_CLS = {"mut": "n", "soon": "s", "over": "o", "green": "g"}


def note_html(note: str) -> str:
    """One task's notes as <p> lines: checkboxes, highlight tones, mentions
    resolved to the directory's names. Escaped throughout."""
    out = []
    for line in (note or "").splitlines():
        s = line.rstrip()
        if not s.strip():
            continue
        box = ""
        m = _CB.match(s)
        if m:
            box = "\u2611 " if m.group(1).lower() == "x" else "\u2610 "
            s = m.group(2)
        pieces = []
        for seg, tone in highlight_segments(s):
            for txt, handle in split_mentions(seg):
                if not txt:
                    continue
                if handle and handle in PEOPLE:
                    p = PEOPLE[handle]
                    nm = p.name.replace(" ", "\u00a0")
                    pieces.append(f'<span class="men" title="{esc(p.role)}">'
                                  f"@{esc(nm)}</span>")
                else:
                    pieces.append(f'<span class="t{_TONE_CLS[tone]}">'
                                  f"{esc(txt)}</span>")
        out.append(f'<p class="nl">{box}{"".join(pieces)}</p>')
    return "".join(out)


# ---------------------------------------------------------------------------
# gantt geometry
# ---------------------------------------------------------------------------

_TICK_STEPS = (1, 2, 3, 5, 7, 10, 14, 21, 30, 60)
_svg_n = 0


def _x(d: date, lo: date, hi: date, x0: float, x1: float) -> float:
    span = max(1, (hi - lo).days)
    return x0 + (d - lo).days / span * (x1 - x0)


def _scale(tasks):
    """Timeline window from the dated tasks, padded; today stays in view."""
    pts = [d for t in tasks for d in (_start(t), _due(t)) if d]
    if not pts:
        return TODAY - timedelta(days=7), TODAY + timedelta(days=7)
    lo, hi = min(pts), max(pts)
    pad = max(2, (hi - lo).days // 12)
    lo -= timedelta(days=pad)
    hi += timedelta(days=pad)
    if lo <= TODAY <= hi:
        return lo, hi
    return (TODAY - timedelta(days=10), hi) if TODAY < lo else \
        (lo, TODAY + timedelta(days=10))


def _ticks(lo, hi):
    span = (hi - lo).days
    step = next((s for s in _TICK_STEPS if span // s <= 8), 90)
    d = lo + timedelta(days=(step - lo.toordinal() % step) % step)
    out = []
    while d <= hi:
        out.append(d)
        d += timedelta(days=step)
    return out


def _frame(lo, hi, x0, x1, top, bottom, w):
    """Weekend bands, grid lines, date ticks, the today rule. Shared by both
    gantt layouts."""
    p = []
    span = max(1, (hi - lo).days)
    dw = (x1 - x0) / span
    d = lo
    while d <= hi:
        if d.weekday() >= 5:
            p.append(f'<rect x="{_x(d, lo, hi, x0, x1):.1f}" y="{top}" '
                     f'width="{dw:.1f}" height="{bottom - top}" class="wk"/>')
        d += timedelta(days=1)
    for t in _ticks(lo, hi):
        x = _x(t, lo, hi, x0, x1)
        p.append(f'<line x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{bottom}" '
                 f'class="gl"/>')
        if x + 3 <= w - 46:
            p.append(f'<text x="{x + 3:.1f}" y="{top - 8}" class="m" '
                     f'font-size="10">{MONTHS[t.month - 1]} {t.day}</text>')
    if lo <= TODAY <= hi:
        x = _x(TODAY, lo, hi, x0, x1)
        p.append(f'<line x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{bottom}" '
                 f'class="today"/>')
        p.append(f'<text x="{x + 3:.1f}" y="{bottom - 5}" class="td" '
                 f'font-size="10">today</text>')
    return "".join(p)


def _trunc(text: str, maxc: int) -> str:
    return text if len(text) <= maxc else text[:max(1, maxc - 1)] + "\u2026"


def _meta(board, task):
    """(text, cls) parts for the meta line beside a task title."""
    parts = [(task.phase, None)]
    if task.priority == "high":
        parts.append(("high", None))
    d = _due(task)
    if d is not None:
        n = (d - TODAY).days
        cls = "mo" if n < 0 and not board.is_done(task) else None
        parts.append((due_word(n), cls))
    else:
        parts.append(("no date", None))
    if task.blocked:
        parts.append(("blocked", "mo"))
    age = days_in_phase(task, TODAY)
    if age is not None:
        parts.append((f"{age}d in phase", None))
    if task.milestone and task.mark in MARKS:
        mk = MARKS[task.mark]
        parts.append((f"{mk.shape} {mk.name}", "mk"))
    return parts


def _meta_svg(board, task, x, y, fs):
    tsp = []
    for i, (txt, cls) in enumerate(_meta(board, task)):
        if i:
            tsp.append(f'<tspan class="m" font-size="{fs}"> \u00b7 </tspan>')
        c = f' class="{cls}"' if cls else ' class="m"'
        tsp.append(f"<tspan{c} font-size=\"{fs}\">{esc(txt)}</tspan>")
    return (f'<text x="{x}" y="{y}">' + "".join(tsp) + "</text>")


def _task_rows(board, tasks):
    """Open dated by due, then open undated, then done — the deck's reading
    order: what needs attention first, finished work last."""
    def dated(t):
        return _start(t) or _due(t)

    def key(t):
        d = _due(t) or _start(t) or date.max
        return (d, _start(t) or d)

    open_ = [t for t in tasks if not board.is_done(t)]
    done = [t for t in tasks if board.is_done(t)]
    od = sorted([t for t in open_ if dated(t)], key=key)
    ou = [t for t in open_ if not dated(t)]
    dn = sorted(done, key=lambda t: (_due(t) or date.min), reverse=True)
    return od + ou + dn


def _arrow(p, x1, y1, x2, y2, sid):
    c = 16 if x2 >= x1 else -16
    p.append(f'<path d="M{x1:.1f},{y1:.1f} C{x1 + c:.1f},{y1:.1f} '
             f"{x2 - c:.1f},{y2:.1f} {x2 - 2:.1f},{y2:.1f}\" class=\"arrow\" "
             f'marker-end="url(#ah{sid})"/>')


def _mark_cls(task):
    d = _due(task)
    if d is not None and d < TODAY:
        return "msr"
    return f"mk-{MARKS[task.mark].colour}"


def _defs(sid):
    return (f'<defs><marker id="ah{sid}" viewBox="0 0 10 10" refX="8" refY="5" '
            'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            '<path d="M0,0L10,5L0,10z" class="ahd"/></marker></defs>')


def _ms_label(p, cls, text, cx, yc, fs, W):
    """The class label beside a milestone diamond — flips to the left side
    when the right edge would clip it."""
    tw = len(text) * fs * 0.58 + 4
    if cx + 12 + tw > W - 6:
        p.append(f'<text x="{cx - 12:.1f}" y="{yc + 4}" class="{cls}" '
                 f'font-size="{fs}" text-anchor="end">{esc(text)}</text>')
    else:
        p.append(f'<text x="{cx + 12:.1f}" y="{yc + 4}" class="{cls}" '
                 f'font-size="{fs}">{esc(text)}</text>')


def _bar_cls(board, t):
    if board.is_done(t):
        return "done"
    return f"ph{PHASES.index(t.phase)}" if t.phase in PHASES else "ph0"


def gantt_project(board, tasks) -> str:
    """The project slide's gantt — wide layout plus the phone reflow, swapped
    by CSS at the breakpoint. Text is real, selectable <text>."""
    global _svg_n
    _svg_n += 1
    sid = _svg_n
    rows = _task_rows(board, tasks)
    lo, hi = _scale(tasks)
    out = []

    # ---- wide layout -------------------------------------------------------
    W, X0, X1, TOP, RH, BH = 1000, 208, 986, 30, 38, 18
    H = TOP + len(rows) * RH + 12
    p = [f'<svg class="g g-wide" viewBox="0 0 {W} {H}" role="img" '
         f'aria-label="gantt of project tasks">', _defs(sid)]
    p.append(_frame(lo, hi, X0, X1, TOP, H - 4, W))
    anchors = {}
    for i, t in enumerate(rows):
        y = TOP + i * RH
        p.append(f'<line x1="4" y1="{y + RH - 1}" x2="{W - 4}" y2="{y + RH - 1}" '
                 f'class="rl"/>')
        title = _trunc(t.title, 30)
        if board.is_done(t):
            title = "\u2713 " + title
        if t.blocked:
            title = "\u26d4 " + title
        p.append(f'<text x="8" y="{y + 14}" class="t" font-size="12.5">'
                 f"{esc(title)}</text>")
        p.append(_meta_svg(board, t, 8, y + 27, 9.5))
        s, d = _start(t), _due(t)
        yc = y + 17
        if t.milestone and s == d and d is not None:
            cx = _x(d, lo, hi, X0, X1)
            p.append(f'<path d="M{cx:.1f},{yc - 9} L{cx + 9:.1f},{yc} '
                     f'{cx:.1f},{yc + 9} L{cx - 9:.1f},{yc} Z" '
                     f'class="{_mark_cls(t)}"/>')
            mk = MARKS[t.mark]
            _ms_label(p, _mark_cls(t), f"{mk.shape} {mk.name}", cx, yc, 11, W)
            anchors[t.id] = (cx, yc)
        elif s is None and d is None:
            p.append(f'<rect x="{X0}" y="{yc - 7}" width="{X1 - X0}" height="14" '
                     f'class="undated"/>')
            p.append(f'<text x="{X0 + 6}" y="{yc + 4}" class="m" font-size="10">'
                     f"no dates</text>")
            anchors[t.id] = (None, yc)
        else:
            s = s or d
            d = d or s
            xs = _x(s, lo, hi, X0, X1)
            xe = _x(d, lo, hi, X0, X1)
            if xe - xs < 4:
                xe = xs + 4
            blk = " blk" if t.blocked else ""
            p.append(f'<rect x="{xs:.1f}" y="{yc - BH // 2}" '
                     f'width="{xe - xs:.1f}" height="{BH}" rx="3" '
                     f'class="bar {_bar_cls(board, t)}{blk}"/>')
            anchors[t.id] = (xe, yc)
    for t in rows:
        x2, y2 = anchors.get(t.id, (None, 0))
        for dep in t.depends_on:
            if dep not in anchors or anchors[dep][0] is None or x2 is None:
                continue
            xt = _x(_start(t) or _due(t) or TODAY, lo, hi, X0, X1)
            _arrow(p, anchors[dep][0], anchors[dep][1], xt, y2, sid)
    p.append("</svg>")
    out.append("".join(p))

    # ---- narrow layout (phones) --------------------------------------------
    W, X0, X1, TOP, RH, BH = 420, 8, 412, 26, 46, 13
    H = TOP + len(rows) * RH + 10
    p = [f'<svg class="g g-narrow" viewBox="0 0 {W} {H}" role="img" '
         f'aria-label="gantt of project tasks">', _defs(sid)]
    p.append(_frame(lo, hi, X0, X1, TOP, H - 4, W))
    anchors = {}
    for i, t in enumerate(rows):
        y = TOP + i * RH
        p.append(f'<line x1="4" y1="{y + RH - 1}" x2="{W - 4}" y2="{y + RH - 1}" '
                 f'class="rl"/>')
        title = _trunc(t.title, 64)
        if board.is_done(t):
            title = "\u2713 " + title
        if t.blocked:
            title = "\u26d4 " + title
        p.append(f'<text x="8" y="{y + 12}" class="t" font-size="11.5">'
                 f"{esc(title)}</text>")
        p.append(_meta_svg(board, t, 8, y + 24, 8.8))
        s, d = _start(t), _due(t)
        yc = y + 34
        if t.milestone and s == d and d is not None:
            cx = _x(d, lo, hi, X0, X1)
            p.append(f'<path d="M{cx:.1f},{yc - 8} L{cx + 8:.1f},{yc} '
                     f'{cx:.1f},{yc + 8} L{cx - 8:.1f},{yc} Z" '
                     f'class="{_mark_cls(t)}"/>')
            mk = MARKS[t.mark]
            _ms_label(p, _mark_cls(t), f"{mk.shape} {mk.name}", cx, yc, 10, W)
            anchors[t.id] = (cx, yc)
        elif s is None and d is None:
            p.append(f'<rect x="{X0}" y="{yc - 6}" width="{X1 - X0}" height="12" '
                     f'class="undated"/>')
            p.append(f'<text x="{X0 + 6}" y="{yc + 4}" class="m" font-size="9">'
                     f"no dates</text>")
            anchors[t.id] = (None, yc)
        else:
            s = s or d
            d = d or s
            xs = _x(s, lo, hi, X0, X1)
            xe = _x(d, lo, hi, X0, X1)
            if xe - xs < 3:
                xe = xs + 3
            blk = " blk" if t.blocked else ""
            p.append(f'<rect x="{xs:.1f}" y="{yc - BH // 2}" '
                     f'width="{xe - xs:.1f}" height="{BH}" rx="3" '
                     f'class="bar {_bar_cls(board, t)}{blk}"/>')
            anchors[t.id] = (xe, yc)
    for t in rows:
        x2, y2 = anchors.get(t.id, (None, 0))
        for dep in t.depends_on:
            if dep not in anchors or anchors[dep][0] is None or x2 is None:
                continue
            xt = _x(_start(t) or _due(t) or TODAY, lo, hi, X0, X1)
            _arrow(p, anchors[dep][0], anchors[dep][1], xt, y2, sid)
    p.append("</svg>")
    out.append("".join(p))
    return "".join(out)


def gantt_overview(entries) -> str:
    """The 'all' view: one row per project across every board. `entries` is
    [(board, lane, tasks)], already grouped and ordered."""
    global _svg_n
    _svg_n += 1
    sid = _svg_n
    all_tasks = [t for _, _, ts in entries for t in ts]
    lo, hi = _scale(all_tasks)
    out = []

    def bars(p, board, tasks, y, lo, hi, x0, x1, bh):
        for t in tasks:
            s, d = _start(t), _due(t)
            if t.milestone and s == d and d is not None:
                cx = _x(d, lo, hi, x0, x1)
                p.append(f'<path d="M{cx:.1f},{y - 7} L{cx + 7:.1f},{y} '
                         f'{cx:.1f},{y + 7} L{cx - 7:.1f},{y} Z" '
                         f'class="{_mark_cls(t)}"/>')
            elif s is not None or d is not None:
                s = s or d
                d = d or s
                xs = _x(s, lo, hi, x0, x1)
                xe = _x(d, lo, hi, x0, x1)
                if xe - xs < 3:
                    xe = xs + 3
                p.append(f'<rect x="{xs:.1f}" y="{y - bh // 2}" '
                         f'width="{xe - xs:.1f}" height="{bh}" rx="2" '
                         f'class="bar {_bar_cls(board, t)}"/>')

    # ---- wide ---------------------------------------------------------------
    W, X0, X1, TOP = 1000, 208, 986, 30
    HH, RH = 20, 30
    board_heads = sum(1 for b in {id(e[0]) for e in entries})
    H = TOP + board_heads * HH + len(entries) * RH + 12
    p = [f'<svg class="g g-wide" viewBox="0 0 {W} {H}" role="img" '
         f'aria-label="all projects on one timeline">']
    p.append(_frame(lo, hi, X0, X1, TOP, H - 4, W))
    y = TOP
    last_board = None
    for board, lane, tasks in entries:
        if board is not last_board:
            p.append(f'<text x="8" y="{y + 13}" class="bd" font-size="11">'
                     f"{esc(board_label(board))}</text>")
            y += HH
            last_board = board
        p.append(f'<line x1="4" y1="{y + RH - 1}" x2="{W - 4}" y2="{y + RH - 1}" '
                 f'class="rl"/>')
        name = _trunc(lane.name, 28)
        p.append(f'<text x="8" y="{y + 13}" class="t" font-size="12">'
                 f"{esc(name)}</text>")
        st = "" if lane.status == "on_track" else f" \u00b7 {lane.status}"
        p.append(f'<text x="8" y="{y + 25}" class="m" font-size="9.5">'
                 f"open {len(lane.open)}{esc(st)} \u00b7 "
                 f"{esc(due_word(lane.due_in, lane.closed))}</text>")
        bars(p, board, tasks, y + 15, lo, hi, X0, X1, 10)
        y += RH
    p.append("</svg>")
    out.append("".join(p))

    # ---- narrow -------------------------------------------------------------
    W, X0, X1, TOP = 420, 8, 412, 26
    HH, RH = 18, 40
    H = TOP + board_heads * HH + len(entries) * RH + 10
    p = [f'<svg class="g g-narrow" viewBox="0 0 {W} {H}" role="img" '
         f'aria-label="all projects on one timeline">']
    p.append(_frame(lo, hi, X0, X1, TOP, H - 4, W))
    y = TOP
    last_board = None
    for board, lane, tasks in entries:
        if board is not last_board:
            p.append(f'<text x="8" y="{y + 11}" class="bd" font-size="10.5">'
                     f"{esc(board_label(board))}</text>")
            y += HH
            last_board = board
        p.append(f'<line x1="4" y1="{y + RH - 1}" x2="{W - 4}" y2="{y + RH - 1}" '
                 f'class="rl"/>')
        name = _trunc(lane.name, 56)
        st = "" if lane.status == "on_track" else f" \u00b7 {lane.status}"
        p.append(f'<text x="8" y="{y + 12}" class="t" font-size="11">'
                 f"{esc(name)}</text>")
        p.append(f'<text x="8" y="{y + 23}" class="m" font-size="8.8">'
                 f"open {len(lane.open)}{esc(st)} \u00b7 "
                 f"{esc(due_word(lane.due_in, lane.closed))}</text>")
        bars(p, board, tasks, y + 32, lo, hi, X0, X1, 9)
        y += RH
    p.append("</svg>")
    out.append("".join(p))
    return "".join(out)


# ---------------------------------------------------------------------------
# slides
# ---------------------------------------------------------------------------

def lane_map(board):
    return {ln.name: ln for ln in lanes_of(board, False, TODAY)}


def archived_tasks(board, project_id):
    all_t = board.visible_tasks(True)
    vis = board.visible_tasks(False)
    vis_ids = {id(t) for t in vis}
    return [t for t in all_t if t.project_id == project_id and id(t) not in vis_ids]


def legend() -> str:
    ph = "".join(f'<span class="lg"><span class="sw ph{i}"></span>{esc(n)}</span>'
                 for i, n in enumerate(PHASES))
    mk = "".join(f'<span class="lg"><span class="sw mk-{esc(m.colour)}"></span>'
                 f"{esc(m.shape)} {esc(m.name)}</span>" for m in MARKS.values())
    return (f'<p class="legend">{ph}{mk}'
            f'<span class="lg"><span class="sw msr"></span>reached</span></p>')


def project_slide(board, lane, tasks) -> str:
    hue = HEX.get(lane.hue, HEX["mut"])
    status = "" if lane.status == "on_track" else f" \u00b7 {esc(lane.status)}"
    late = (f'<span class="over">{len(lane.late)} overdue</span>'
            if lane.late else "0 overdue")
    worst = f" (worst {lane.worst}d)" if lane.late else ""
    momentum = sitting(lane, TODAY) or "nothing open"
    head = (f'<h2><span class="chip" style="background:{hue}"></span>'
            f"{esc(lane.name)}{status}</h2>"
            f'<p class="sub">{esc(board_label(board))} \u00b7 open {len(lane.open)}'
            f" \u00b7 done {lane.done_n} \u00b7 high {lane.high} \u00b7 {late}{worst}"
            f" \u00b7 due {esc(due_word(lane.due_in, lane.closed))}"
            f" \u00b7 momentum: {esc(momentum)}</p>")
    notes = []
    for t in tasks:
        if t.notes or t.urls:
            body = note_html(t.notes)
            for u in t.urls:
                body += (f'<p class="nl"><a href="{esc(u)}" class="url">'
                         f"{esc(u.replace('https://', ''))}</a></p>")
            notes.append(f'<div class="note"><p class="nt">{esc(t.title)}</p>'
                         f"{body}</div>")
    notes_html = (f'<h3>Notes on the visible tasks</h3><div class="notes">'
                  + "".join(notes) + "</div>") if notes else ""
    arch = archived_tasks(board, tasks[0].project_id if tasks else None)
    arch_html = ""
    if arch:
        items = " \u00b7 ".join(
            f"{esc(t.title)} (done, {_fmt_range(t)})" for t in arch)
        arch_html = f'<p class="arch"><strong>Archived:</strong> {items}</p>'
    return (f'<section class="slide">{head}'
            f"{gantt_project(board, tasks)}{legend()}{notes_html}{arch_html}"
            f"</section>")


def _fmt_range(t) -> str:
    s, d = _start(t), _due(t)
    if s and d:
        return f"{MONTHS[s.month - 1]} {s.day} \u2013 {MONTHS[d.month - 1]} {d.day}"
    if d:
        return MONTHS[d.month - 1] + " " + str(d.day)
    return "undated"


def board_label(board) -> str:
    # fixture boards carry a scratch path; the deck names them by the round's key
    for name, b in BOARDS.items():
        if b is board:
            return name
    return board.path.stem


def title_slide(lanes_by_board) -> str:
    tiles = []
    total = {"boards": 0, "projects": 0, "open": 0, "done": 0, "overdue": 0}
    board_lines = []
    for name, board in BOARDS.items():
        lanes = lanes_by_board[name]
        open_n = sum(len(ln.open) for ln in lanes)
        done_n = sum(ln.done_n for ln in lanes)
        late_n = sum(len(ln.late) for ln in lanes)
        total["boards"] += 1
        total["projects"] += len(lanes)
        total["open"] += open_n
        total["done"] += done_n
        total["overdue"] += late_n
        arch = sum(1 for t in board.visible_tasks(True) if t.archived)
        board_lines.append(
            f"<tr><td>{esc(name)}</td><td class=\"n\">{len(lanes)}</td>"
            f"<td class=\"n\">{open_n}</td><td class=\"n\">{done_n}</td>"
            f"<td class=\"n\">{late_n}</td><td class=\"n\">{arch}</td></tr>")
    tiles.append(("boards", total["boards"]))
    tiles.append(("projects", total["projects"]))
    tiles.append(("open", total["open"]))
    tiles.append(("done", total["done"]))
    tiles.append(("overdue", total["overdue"]))
    tile_html = "".join(f'<div class="tile"><div class="n">{v}</div>'
                        f'<div class="k">{esc(k)}</div></div>'
                        for k, v in tiles)
    return f"""
<section class="slide cover">
<h1>taskboard &middot; project deck</h1>
<p class="sub">Generated {esc(TODAY.isoformat())} from the boards' own data &middot;
counts and dates only, nothing here is a forecast.</p>
<div class="tiles">{tile_html}</div>
<table><thead><tr><th>board</th><th class="n">projects</th><th class="n">open</th>
<th class="n">done</th><th class="n">overdue</th><th class="n">archived</th></tr>
</thead><tbody>{''.join(board_lines)}</tbody></table>
{legend()}
<p class="hint">Page with \u2190 \u2192 (PageUp / PageDown, Home / End) or the
buttons below &middot; prints as one slide per page &middot; every figure is
labelled directly &mdash; colour never carries meaning alone.</p>
</section>"""


def overview_slide(entries) -> str:
    return (f'<section class="slide"><h2>All projects &mdash; the overview</h2>'
            f'<p class="sub">Every project of every board on one timeline, the '
            f'presentation\u2019s \u2018all\u2019 view. Bars wear their phase; '
            f'diamonds are milestones with their class.</p>'
            f"{gantt_overview(entries)}{legend()}</section>")


# ---------------------------------------------------------------------------
# CSS / JS / assembly
# ---------------------------------------------------------------------------

CSS = """
:root { color-scheme: light dark;
  --bg: #0d1117; --panel: #161b22; --ink: #e6edf3; --mut: #8b98a5;
  --line: #21262d; --frame: #334154; --accent: #2dd4bf; --over: #f43f5e;
  --weekend: #151a22; --done: #3f9c6d;
  --ph0: #64748b; --ph1: #60a5fa; --ph2: #a78bfa; --ph3: #fb923c; --ph4: #3f9c6d;
  --mk-rose: #fb7185; --mk-amber: #fbbf24; --mk-lime: #a3e635;
  --msr: #7a828c; --soon: #fbbf24; --soonbg: rgba(251,191,36,.16);
  --overt: #fb7185; --overbg: rgba(244,63,94,.14);
  --green: #4ade80; --greenbg: rgba(74,222,128,.13); }
@media (prefers-color-scheme: light) {
  :root { --bg: #ffffff; --panel: #f6f8fa; --ink: #1f2328; --mut: #59636e;
    --line: #d8dee4; --frame: #c8d0da; --weekend: #edf1f5; --done: #2f8f5b;
    --ph0: #94a3b8; --ph1: #1f6feb; --ph2: #8250df; --ph3: #bf6106; --ph4: #2f8f5b;
    --mk-rose: #d5234a; --mk-amber: #9a6700; --mk-lime: #4d7c0f;
    --msr: #8a919b; --soon: #8a5a00; --soonbg: rgba(154,103,0,.12);
    --overt: #c81e4f; --overbg: rgba(200,30,79,.09);
    --green: #1a7f37; --greenbg: rgba(26,127,55,.10); }
}
* { box-sizing: border-box; }
body { margin: 0; padding: 1.2rem .9rem 6rem;
       font: 15px/1.55 ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
       background: var(--bg); color: var(--ink); }
.slide { display: none; max-width: 1100px; margin: 0 auto; }
.slide.on { display: block; }
h1 { font-size: 2rem; margin: 1rem 0 .3rem; letter-spacing: -.01em; }
h2 { font-size: 1.2rem; margin: .6rem 0 .2rem; font-weight: 650;
      display: flex; align-items: center; gap: .5rem; flex-wrap: wrap; }
h3 { font-size: .95rem; margin: 1.6rem 0 .4rem; color: var(--mut);
      text-transform: uppercase; letter-spacing: .06em; font-weight: 600; }
.sub { color: var(--mut); margin: 0 0 1rem; font-size: .9rem; }
.chip { display: inline-block; width: .75rem; height: .75rem; border-radius: 3px; }
.tiles { display: flex; flex-wrap: wrap; gap: .7rem; margin: .4rem 0 1.2rem; }
.tile { flex: 1 1 7rem; background: var(--panel); border: 1px solid var(--line);
        border-radius: 8px; padding: .65rem .8rem; }
.tile .n { font-size: 1.5rem; font-weight: 650; }
.tile .k { color: var(--mut); font-size: .75rem; text-transform: uppercase;
           letter-spacing: .06em; }
table { border-collapse: collapse; width: 100%; margin: .4rem 0 1rem;
        font-size: .9rem; }
th, td { text-align: left; padding: .4rem .6rem;
         border-bottom: 1px solid var(--line); vertical-align: top; }
th { color: var(--mut); font-weight: 600; font-size: .75rem;
     text-transform: uppercase; letter-spacing: .06em; }
td.n, th.n { text-align: right; font-variant-numeric: tabular-nums; }
.over { color: var(--over); font-weight: 600; }
.g { display: block; width: 100%; height: auto; background: var(--panel);
     border: 1px solid var(--line); border-radius: 10px; margin: .6rem 0; }
.g-narrow { display: none; }
svg text { font-family: inherit; }
.t { fill: var(--ink); } .m { fill: var(--mut); } .mo { fill: var(--over); }
.mk { fill: var(--accent); } .td { fill: var(--accent); } .bd { fill: var(--mut); }
.ts { fill: var(--soon); } .to { fill: var(--overt); } .tg { fill: var(--green); }
.wk { fill: var(--weekend); } .gl { stroke: var(--line); stroke-width: 1; }
.rl { stroke: var(--line); stroke-width: 1; opacity: .55; }
.today { stroke: var(--accent); stroke-width: 1.5; }
.ahd { fill: var(--mut); }
.arrow { stroke: var(--mut); stroke-width: 1.3; fill: none; opacity: .9; }
.bar { opacity: .92; }
.bar.blk { stroke: var(--over); stroke-width: 1.6; stroke-dasharray: 4 2; }
.bar.ph0 { fill: var(--ph0); } .bar.ph1 { fill: var(--ph1); }
.bar.ph2 { fill: var(--ph2); } .bar.ph3 { fill: var(--ph3); }
.bar.ph4, .bar.done { fill: var(--done); }
.undated { fill: none; stroke: var(--frame); stroke-width: 1.2;
           stroke-dasharray: 5 3; }
.mk-rose { fill: var(--mk-rose); } .mk-amber { fill: var(--mk-amber); }
.mk-lime { fill: var(--mk-lime); } .msr { fill: var(--msr); }
.legend { display: flex; flex-wrap: wrap; gap: .4rem 1rem; color: var(--mut);
          font-size: .82rem; margin: .8rem 0 0; }
.lg { display: inline-flex; align-items: center; gap: .35rem; }
.sw { display: inline-block; width: .7rem; height: .7rem; border-radius: 2px; }
.sw.ph0 { background: var(--ph0); } .sw.ph1 { background: var(--ph1); }
.sw.ph2 { background: var(--ph2); } .sw.ph3 { background: var(--ph3); }
.sw.ph4 { background: var(--ph4); }
.sw.mk-rose { background: var(--mk-rose); } .sw.mk-amber { background: var(--mk-amber); }
.sw.mk-lime { background: var(--mk-lime); } .sw.msr { background: var(--msr); }
.notes { display: grid; grid-template-columns: repeat(auto-fill, minmax(17rem, 1fr));
         gap: .6rem; }
.note { background: var(--panel); border: 1px solid var(--line);
        border-radius: 8px; padding: .55rem .75rem; }
.nt { margin: 0 0 .25rem; font-weight: 600; font-size: .88rem; }
.nl { margin: .12rem 0; font-size: .86rem; }
.men { color: var(--accent); font-weight: 600; }
span.ts { color: var(--soon); background: var(--soonbg); border-radius: 3px;
          padding: 0 .2em; }
span.to { color: var(--overt); background: var(--overbg); border-radius: 3px;
          padding: 0 .2em; }
span.tg { color: var(--green); background: var(--greenbg); border-radius: 3px;
          padding: 0 .2em; }
.url { color: var(--accent); font-size: .82rem; word-break: break-all; }
.arch { color: var(--mut); font-size: .85rem; margin: 1.2rem 0 0; }
.hint { color: var(--mut); font-size: .85rem; margin-top: 1.4rem; }
.bar-nav { position: fixed; left: 0; right: 0; bottom: 0; z-index: 9;
           display: flex; align-items: center; justify-content: center;
           gap: 1rem; padding: .55rem; background: var(--panel);
           border-top: 1px solid var(--line); }
.bar-nav button { font: inherit; font-size: 1.05rem; min-width: 3rem;
                  min-height: 2.6rem; border-radius: 8px; cursor: pointer;
                  background: var(--bg); color: var(--ink);
                  border: 1px solid var(--frame); }
.bar-nav button:disabled { opacity: .35; cursor: default; }
#cnt { font-variant-numeric: tabular-nums; color: var(--mut); min-width: 4rem;
       text-align: center; }
@media (max-width: 700px) {
  .g-wide { display: none; } .g-narrow { display: block; }
  body { padding: .7rem .5rem 6rem; }
  h1 { font-size: 1.5rem; }
  th, td { padding: .3rem .35rem; }
  table { font-size: .82rem; }
}
@media print {
  body { background: #fff; color: #000; padding: 0; }
  .bar-nav { display: none; }
  .slide { display: block !important; page-break-after: always;
           max-width: none; }
  .g-narrow { display: none !important; } .g-wide { display: block !important; }
  .note, .tile, .g { border-color: #bbb; background: #fff; }
}
"""

JS = """
(function () {
  var slides = [].slice.call(document.querySelectorAll('.slide'));
  var cur = 0;
  var cnt = document.getElementById('cnt');
  var prev = document.getElementById('prev');
  var next = document.getElementById('next');
  function show(n) {
    cur = Math.min(slides.length - 1, Math.max(0, n));
    slides.forEach(function (s, i) { s.classList.toggle('on', i === cur); });
    cnt.textContent = (cur + 1) + ' / ' + slides.length;
    prev.disabled = cur === 0;
    next.disabled = cur === slides.length - 1;
    window.scrollTo(0, 0);
  }
  prev.addEventListener('click', function () { show(cur - 1); });
  next.addEventListener('click', function () { show(cur + 1); });
  document.addEventListener('keydown', function (e) {
    var t = e.target;
    if (t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' ||
              t.tagName === 'SELECT' || t.isContentEditable)) { return; }
    if (e.key === 'ArrowLeft' || e.key === 'PageUp') { show(cur - 1); e.preventDefault(); }
    else if (e.key === 'ArrowRight' || e.key === 'PageDown') { show(cur + 1); e.preventDefault(); }
    else if (e.key === 'Home') { show(0); e.preventDefault(); }
    else if (e.key === 'End') { show(slides.length - 1); e.preventDefault(); }
  });
  show(0);
})();
"""


def build() -> str:
    lanes_by_board = {name: lanes_of(board, False, TODAY)
                      for name, board in BOARDS.items()}
    entries = []
    for name, board in BOARDS.items():
        lmap = {ln.name: ln for ln in lanes_by_board[name]}
        for project in board.visible_projects(False):
            lane = lmap.get(project.name)
            if lane is None:
                continue
            tasks = [t for t in board.visible_tasks(False)
                     if t.project_id == project.id]
            entries.append((board, lane, tasks))
    slides = [title_slide(lanes_by_board), overview_slide(entries)]
    slides += [project_slide(b, ln, ts) for b, ln, ts in entries]
    nav = ('<div class="bar-nav"><button id="prev" type="button" '
           'aria-label="Previous slide">&#9664;</button>'
           '<span id="cnt" aria-live="polite"></span>'
           '<button id="next" type="button" '
           'aria-label="Next slide">&#9654;</button></div>')
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>taskboard &middot; project deck</title>
<style>{CSS}</style></head>
<body>
{''.join(slides)}
{nav}
<script>{JS}</script>
</body></html>
"""


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build(), encoding="utf-8")
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
