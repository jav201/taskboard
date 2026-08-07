"""The other views, ported INTO the widget architecture.

The shipped app has five view modes; the first prototype pass kept only the
board and quietly dropped the rest, which made the delivery partial. These are
rebuilt to take the active LANGUAGE's tokens and pixel base, so a view is not a
separate look — it is the same language showing a different cut of the data.

Animated: the gantt carries the shipped app's flow packet, and the agenda's
urgency bars breathe. Both are PRECOMPUTED frames (motion.py), so a tick costs
an index lookup, not a recompute.
"""
from __future__ import annotations

from datetime import date, timedelta

from rich.markup import escape

from taskboard import motion as MO
from taskboard.models import parse_iso


def _days(task, today):
    d = parse_iso(task.due_date)
    return None if d is None else (d - today).days


def _chip(board, t, today, k):
    if board.is_done(t):
        return "done", k["dim"]
    if getattr(t, "blocked", False):
        return "blk", k["alert"]
    d = _days(t, today)
    if d is None:
        return "--", k["dim"]
    if d < 0:
        return f"{-d}d!", k["alert"]
    return f"{d}d", (k["warn"] if d <= 3 else k["mut"])


# ---------------------------------------------------------------------------
# AGENDA — urgency buckets. The bar breathes so "overdue" reads as live.
# ---------------------------------------------------------------------------
BUCKETS = [("OVERDUE", -10**6, -1), ("TODAY", 0, 0), ("THIS WEEK", 1, 7),
           ("LATER", 8, 10**6)]


def render_agenda(board, k, width, height, ticker, selected=None) -> str:
    today = date.today()
    tasks = [t for t in board.visible_tasks(False) if not board.is_done(t)]
    out = list(k.sect("AGENDA", f"{len(tasks)} open", width, height))
    for bi, (name, lo, hi) in enumerate(BUCKETS):
        grp = [t for t in tasks
               if (d := _days(t, today)) is not None and lo <= d <= hi]
        undated = [t for t in tasks if _days(t, today) is None]
        if name == "LATER":
            grp += undated
        num = f"[{k['accent']}]\\[{bi + 1}][/]" if k.numbered else ""
        pad = 7 if k.numbered else 10
        if not grp:
            out.append(num + f"[{k['dim']}]{name:<{pad}} empty[/]")
            continue
        # The bar's LENGTH is data; a travelling highlight is the animation.
        # A first version indexed a breathing PULSE spatially -- but the pulse is
        # a temporal amplitude, so a 2-cell bar sampled the same two entries every
        # frame and sat perfectly still. Only checking motion ACROSS ticks showed
        # it; a single frame looked correct.
        # The bar's MECHANISM is the language's (kit.bar): discrete dots on
        # naught's lattice, LCD segments in corgi, a hairline in swiss...
        span = max(3, min(width - 22, len(grp) * 3))
        live = name in ("OVERDUE", "TODAY")
        head = ticker.frame(MO.build_flow(span, n=span + 4, packet=2)) if live else None
        tone = k["alert"] if name == "OVERDUE" else (
            k["warn"] if name == "TODAY" else k["accent"])
        out.append(num + f"[{k['mut']}]{name:<{pad}}[/]"
                   + k.bar(span, head, tone)
                   + f" [{k['dim']}]{len(grp)}[/]")
        for t in grp[:3]:
            chip, ct = _chip(board, t, today, k)
            sel = t.id == selected
            out.append(f"  [{k['ink'] if sel else k['mut']}]"
                       f"{escape(t.title)[:width - 16]:<{max(1, width - 16)}}[/]"
                       f"[{ct}]{chip:>5}[/]")
        if len(grp) > 3:
            out.append(f"  [{k['dim']}]+{len(grp) - 3} more[/]")
        out.append("")
    return "\n".join(out[:max(1, height)])


# ---------------------------------------------------------------------------
# GANTT — an 8-week axis with the shipped app's animated flow packet.
# ---------------------------------------------------------------------------
def render_gantt(board, k, width, height, ticker, selected=None) -> str:
    today = date.today()
    label_w = 20
    span_w = max(10, width - label_w - 2)
    weeks = 8
    day_per_cell = max(1, (weeks * 7) // span_w)
    flow = ticker.frame(MO.build_flow(span_w), speed=1)

    # bar-fill, packet, week-tick, day-tick and due-marker are the LANGUAGE's
    # glyph commitments — a dim lattice under a lit packet in naught, segment
    # bars in corgi, hairlines in swiss (kit.GANTT).
    g_fill, g_pkt, g_week, g_day, g_due = k.GANTT

    out = list(k.sect("GANTT", f"{weeks} weeks · {day_per_cell}d/cell", width,
                      height))
    axis = "".join(g_week if (i * day_per_cell) % 7 == 0 else g_day
                   for i in range(span_w))
    out.append(" " * label_w + f"[{k['dim']}]{axis}[/]")

    for p in board.visible_projects(False):
        items = [t for t in board.visible_tasks(False) if t.project_id == p.id]
        if not items:
            continue
        starts = [parse_iso(t.start_date) or parse_iso(t.due_date) for t in items]
        ends = [parse_iso(t.due_date) for t in items]
        s = min([d for d in starts if d], default=today)
        e = max([d for d in ends if d], default=today)
        a = max(0, min(span_w - 1, (s - today).days // day_per_cell))
        b = max(a, min(span_w - 1, (e - today).days // day_per_cell))
        row = []
        for i in range(span_w):
            if a <= i <= b:
                # the packet is the ONLY animated part; the bar itself is data
                row.append(g_pkt if flow[i] else g_fill)
            else:
                row.append(" ")
        sel = any(t.id == selected for t in items)
        out.append(f"[{k['ink'] if sel else k['mut']}]"
                   f"{escape(p.name)[:label_w - 1]:<{label_w}}[/]"
                   f"[{k['accent'] if sel else k['mut']}]{''.join(row)}[/]")
        for t in items[:2]:
            d = parse_iso(t.due_date)
            if not d:
                continue
            x = max(0, min(span_w - 1, (d - today).days // day_per_cell))
            chip, ct = _chip(board, t, today, k)
            line = [" "] * span_w
            line[x] = g_due
            out.append(f"  [{k['dim']}]{escape(t.title)[:label_w - 3]:<{label_w - 2}}[/]"
                       f"[{ct}]{''.join(line)}[/]")
    return "\n".join(out[:max(1, height)])


# ---------------------------------------------------------------------------
# SWIMLANES — projects x phases, density as a dot lattice.
# ---------------------------------------------------------------------------
def render_swimlanes(board, k, width, height, ticker, selected=None) -> str:
    from taskboard.views import phase_buckets
    tasks = board.visible_tasks(False)
    label_w = 20
    cell_w = max(4, (width - label_w - 8) // max(1, len(board.phases)))
    out = list(k.sect("SWIMLANES",
                      f"{len(board.visible_projects(False))} projects", width,
                      height))
    head = " " * label_w + "".join(p.upper()[:cell_w - 1].ljust(cell_w)
                                   for p in board.phases)
    out.append(f"[{k['mut']}]{head}[/]")
    for p in board.visible_projects(False):
        items = [t for t in tasks if t.project_id == p.id]
        if not items:
            continue
        buckets = phase_buckets(board, items)
        sel = any(t.id == selected for t in items)
        row = f"[{k['ink'] if sel else k['mut']}]" \
              f"{escape(p.name)[:label_w - 2]:<{label_w}}[/]"
        for b in buckets:
            n = len(b)
            if n:
                # density drawn with the language's own quantity mechanism
                span = min(n, cell_w - 1)
                row += k.bar(span) + " " * (cell_w - span)
            else:
                row += f"[{k['dim']}]{'·':<{cell_w}}[/]"
        done = sum(1 for t in items if board.is_done(t))
        row += f" [{k['dim']}]{round(100 * done / max(1, len(items))):>3}%[/]"
        out.append(row)
    return "\n".join(out[:max(1, height)])


VIEWS = {"agenda": render_agenda, "gantt": render_gantt,
         "lanes": render_swimlanes}
