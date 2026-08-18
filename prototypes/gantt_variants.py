"""Gantt view design variants — PROTOTYPE (throwaway).

Run:      python prototypes/gantt_variants.py
Capture:  python prototypes/capture_gantt.py   (writes .txt + .svg)

Four radically different ways to render the same Gantt data.  Each tries to be
less cluttered than the current shipped view.  The file is self-contained: it
imports only the stable Board/Task model from taskboard.models and copies the
small rendering helpers it needs, so deleting this file leaves the app untouched.
"""
from __future__ import annotations

import sys
from datetime import date, timedelta
from pathlib import Path
from typing import NamedTuple

from rich.cells import cell_len, set_cell_size
from rich.markup import escape
from rich.text import Text

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from taskboard.models import Board, Task  # stable model only


# --- palette (same as taskboard/views.py) ------------------------------------
HEX = {
    "frame": "#334154",
    "mut": "#8b98a5",
    "dim": "#5b6675",
    "ink": "#e6edf3",
    "hd": "#c9d4e0",
    "accent": "#2dd4bf",
    "violet": "#a78bfa",
    "sky": "#38bdf8",
    "amber": "#fbbf24",
    "rose": "#fb7185",
    "green": "#4ade80",
    "orange": "#fb923c",
    "lime": "#a3e635",
    "cyan": "#22d3ee",
    "blue": "#60a5fa",
    "indigo": "#818cf8",
    "fuchsia": "#e879f9",
    "pink": "#f472b6",
    "over": "#f43f5e",
    "ash": "#6b4a3f",
    "bright": "#e6edf7",
    "soon": "#fbbf24",
    "later": "#64748b",
    "done": "#3f9c6d",
}


def c(text: str, key: str, bold: bool = False) -> str:
    """Wrap already-escaped, width-correct text in a palette color."""
    b = "b " if bold else ""
    return f"[{b}{HEX[key]}]{text}[/]"


def vis(s: str) -> int:
    """Visible width in terminal cells; strip markup first."""
    import re
    plain = re.sub(r"\[/?[^\]]*\]", "", s)
    return cell_len(plain)


def fit(s: str, width: int, align: str = "left") -> str:
    """Width-exact plain text; truncates with '…'."""
    if width <= 0:
        return ""
    if vis(s) > width:
        return set_cell_size(s, width - 1) + "…"
    pad = width - vis(s)
    if align == "right":
        return " " * pad + s
    if align == "center":
        left = pad // 2
        return " " * left + s + " " * (pad - left)
    return s + " " * pad


def clip(s: str, width: int) -> str:
    """Truncate with visible ellipsis."""
    if width <= 0:
        return ""
    return s if vis(s) <= width else set_cell_size(s, width - 1) + "…"


def _parse_iso(iso: str | None) -> date | None:
    if not iso:
        return None
    try:
        return date.fromisoformat(iso)
    except ValueError:
        return None


def _day_delta(iso: str | None, today: date) -> int | None:
    d = _parse_iso(iso)
    return (d - today).days if d else None


def _is_done(board: Board, task: Task) -> bool:
    return bool(board.phases) and task.phase == board.phases[-1]


def _project_color(board: Board, task: Task) -> str:
    p = board.project_by_id(task.project_id)
    return p.color if p else "dim"


def _project_name(board: Board, task: Task) -> str:
    p = board.project_by_id(task.project_id)
    return p.name if p else "Inbox"


def _tasks_of(board: Board, project_id: str | None, show_archived: bool = False
              ) -> list[Task]:
    """Sorted: open first by due date, then done by due date."""
    rows = [t for t in board.visible_tasks(show_archived)
            if t.project_id == project_id]
    open_ = sorted([t for t in rows if not _is_done(board, t)],
                   key=lambda t: (_parse_iso(t.due_date) is None,
                                  _parse_iso(t.due_date) or date.max))
    done = sorted([t for t in rows if _is_done(board, t)],
                  key=lambda t: (_parse_iso(t.due_date) is None,
                                 _parse_iso(t.due_date) or date.max))
    return open_ + done


# =============================================================================
# Shared geometry helpers
# =============================================================================
class Geo(NamedTuple):
    width: int
    height: int
    label_w: int
    tail_w: int
    field_w: int
    today_col: int
    cell_days: int
    today: date
    start: date


def _geo(width: int, height: int, today: date, cell_days: int = 2,
         label_w: int = 14, tail_w: int = 10) -> Geo:
    w = max(40, width)
    h = height or 24
    field_w = max(8, w - label_w - tail_w - 1)
    start = today - timedelta(days=(field_w * cell_days) // 3)
    today_col = (field_w // 3)
    return Geo(width=w, height=h, label_w=label_w, tail_w=tail_w,
               field_w=field_w, today_col=today_col, cell_days=cell_days,
               today=today, start=start)


def _col(d: date | None, geo: Geo) -> int | tuple[str, int]:
    """Field column for a date; returns ('L'|'R', clamped) when off-window."""
    if d is None:
        return geo.today_col
    days = (d - geo.start).days
    col = days // geo.cell_days
    if col < 0:
        return ("L", 0)
    if col >= geo.field_w:
        return ("R", geo.field_w - 1)
    return col


def _is_flag(col: int | tuple[str, int]) -> bool:
    return isinstance(col, tuple)


def _col_value(col: int | tuple[str, int]) -> int:
    return col[1] if isinstance(col, tuple) else col


def _lattice(geo: Geo) -> list[str]:
    """Empty field lattice with today rule."""
    cells = []
    for i in range(geo.field_w):
        if i == geo.today_col:
            cells.append(c("╎", "accent"))
        else:
            mid_day = geo.start + timedelta(days=i * geo.cell_days + geo.cell_days // 2)
            cells.append(c("·", "ash" if mid_day < geo.today else "dim"))
    return cells


def _header(title: str, right: str, width: int) -> str:
    tvis, rvis = vis(title), vis(right)
    gap = max(1, width - tvis - rvis - 1)
    if tvis + rvis + 1 > width:
        right = ""
        gap = max(1, width - tvis - 1)
    if tvis > width:
        return c(fit(title, width), "accent", bold=True)
    return title + " " * gap + right + " "


def _rule(width: int) -> str:
    return c("─" * max(0, width), "frame")


def _scale_row(geo: Geo) -> str:
    """Compact day-offset scale row."""
    span = geo.field_w
    body = [" "] * span

    def place(text: str, at: int) -> None:
        for i, ch in enumerate(text):
            if 0 <= at + i < span:
                body[at + i] = ch

    left = f"-{geo.today_col * geo.cell_days}d"
    right = f"+{(geo.field_w - 1 - geo.today_col) * geo.cell_days}d"
    mid = geo.today_col - 2
    if 0 <= mid and mid + 5 <= span:
        place("today", mid)
        if len(left) < mid:
            place(left, 0)
        if span - len(right) >= mid + 6:
            place(right, span - len(right))
    out = []
    i = 0
    while i < span:
        j = i
        # crude month band: every ~4 cells shift tone
        while j < span and ((j // 4) == (i // 4)):
            j += 1
        tone = "mut" if (i // 4) % 2 else "dim"
        out.append(c("".join(body[i:j]), tone))
        i = j
    return " " * geo.label_w + "".join(out) + " " * geo.tail_w


def _row(label: str, cells: list[str], tail: str = "", geo: Geo | None = None,
         label_tone: str = "ink") -> str:
    """Assemble a full width-exact row."""
    assert geo is not None
    left = c(fit(clip(label, geo.label_w), geo.label_w), label_tone)
    body = "".join(cells)
    if tail:
        tail_vis = vis(tail)
        pad = max(0, geo.tail_w - tail_vis)
        right = " " * pad + tail
    else:
        right = " " * geo.tail_w
    return left + " " + body + right


def _to_text(lines: list[str], height: int, width: int) -> Text:
    """Pad to height and return rich Text."""
    while len(lines) < height:
        lines.append(" " * width)
    return Text.from_markup("\n".join(lines[:height]), emoji=False)


# =============================================================================
# VARIANT A · Minimal timeline
# Project rows only.  Thin bars, no meta band, no task rows, no meters.
# =============================================================================
def render_variant_a(board: Board, selected_id: str | None, today: date,
                     width: int = 86, height: int = 22) -> Text:
    geo = _geo(width, height, today, cell_days=2, label_w=16, tail_w=8)
    tasks = board.visible_tasks(False)
    late_n = sum(1 for t in tasks
                 if (d := _parse_iso(t.due_date)) and d < today and not _is_done(board, t))
    right = (c(f"▲{late_n}", "over", bold=True) if late_n
             else c("ok", "dim"))
    lines = [
        _header(c("GANTT", "accent", bold=True) + "  minimal", right, geo.width),
        _rule(geo.width),
    ]

    projects = board.visible_projects(False)
    for p in projects:
        cells = _lattice(geo)
        s = _col(_parse_iso(p.start_date), geo)
        e = _col(_parse_iso(p.due_date), geo)
        a, b = _col_value(s), _col_value(e)
        if b < a:
            a, b = b, a
        for x in range(a, b + 1):
            cells[x] = c("─", p.color)
        cells[b] = c("◆", p.color)
        if _is_flag(s):
            cells[0] = c("◂", "mut")
        if _is_flag(e):
            cells[-1] = c("▸", "mut")
        # today rule re-applied if covered
        if a <= geo.today_col <= b:
            cells[geo.today_col] = c("╎", "accent")
        dd = _day_delta(p.due_date, today)
        tail = ("—" if dd is None else
                c(f"{dd}d", "over" if dd and dd < 0 else "mut"))
        lines.append(_row(p.name, cells, tail, geo, p.color))

    lines.append(_scale_row(geo))
    return _to_text(lines, height or len(lines) + 1, geo.width)


# =============================================================================
# VARIANT B · Card-style Gantt
# Each project/task is a card strip: title, date chips, status dot.
# =============================================================================
def render_variant_b(board: Board, selected_id: str | None, today: date,
                     width: int = 86, height: int = 26) -> Text:
    geo = _geo(width, height, today, cell_days=3, label_w=18, tail_w=22)
    tasks = board.visible_tasks(False)
    late_n = sum(1 for t in tasks
                 if (d := _parse_iso(t.due_date)) and d < today and not _is_done(board, t))
    right = c(f"{len(tasks)} tasks", "mut")
    lines = [
        _header(c("GANTT", "accent", bold=True) + "  cards", right, geo.width),
        _rule(geo.width),
    ]

    def date_chip(iso: str | None) -> str:
        d = _parse_iso(iso)
        if d is None:
            return c("—", "dim")
        delta = (d - today).days
        label = d.strftime("%b %d").replace(" 0", " ")
        tone = "over" if delta < 0 else "soon" if delta == 0 else "mut"
        return c(f"{label}", tone)

    for p in board.visible_projects(False):
        # project card strip
        prog = board.project_progress(p.id, False)
        pct = f"{int(round(100 * prog))}%"
        dd = _day_delta(p.due_date, today)
        due_chip = ("—" if dd is None else
                    c(f"due {dd}d", "over" if dd < 0 else "mut"))
        meta = f"{pct}  {due_chip}"
        cells = _lattice(geo)
        s = _col(_parse_iso(p.start_date), geo)
        e = _col(_parse_iso(p.due_date), geo)
        a, b = _col_value(s), _col_value(e)
        if b < a:
            a, b = b, a
        for x in range(a, b):
            cells[x] = c("━", p.color)
        if 0 <= b < geo.field_w:
            cells[b] = c("◆", p.color)
        if a <= geo.today_col <= b:
            cells[geo.today_col] = c("╎", "accent")
        label = c("▌", p.color) + " " + c(escape(fit(p.name, geo.label_w - 2)), p.color, bold=True)
        lines.append(label + " " + "".join(cells) + fit(meta, geo.tail_w, "right"))

        # task strips
        for t in _tasks_of(board, p.id):
            sel = t.id == selected_id
            cells = _lattice(geo)
            s = _col(_parse_iso(t.start_date), geo)
            e = _col(_parse_iso(t.due_date), geo)
            a, b = _col_value(s), _col_value(e)
            if b < a:
                a, b = b, a
            tone = "ash" if _is_done(board, t) else _priority_hue(t.priority)
            if a == b and 0 <= a < geo.field_w:
                cells[a] = c("◆", tone)
            else:
                for x in range(a, b):
                    cells[x] = c("─", tone)
                if 0 <= b < geo.field_w:
                    tip = ("✓" if _is_done(board, t) else
                           "○◔◑◕"[min(3, board.phase_index(t))])
                    cells[b] = c(tip, tone)
            if a <= geo.today_col <= b:
                cells[geo.today_col] = c("╎", "accent")
            plain = fit(clip(t.title, geo.label_w - 4), geo.label_w - 4)
            title = f"[reverse]{escape(plain)}[/reverse]" if sel else escape(plain)
            date_chips = f"{date_chip(t.start_date)} → {date_chip(t.due_date)}"
            blocked_mark = c("▲", "over") if t.blocked else ""
            tail = fit(date_chips + (" " + blocked_mark if t.blocked else ""),
                       geo.tail_w, "right")
            label = "  " + c("▏", tone) + " " + title
            lines.append(label + " " + "".join(cells) + " " + tail)

    lines.append(_scale_row(geo))
    return _to_text(lines, height or len(lines) + 1, geo.width)


def _priority_hue(priority: str) -> str:
    return {"high": "rose", "normal": "sky", "low": "mut"}.get(priority, "sky")


# =============================================================================
# VARIANT C · Compact horizon
# Hide distant past/future; focus on today ± N weeks.  Off-window work is
# collapsed to edge markers rather than empty rows.
# =============================================================================
def render_variant_c(board: Board, selected_id: str | None, today: date,
                     width: int = 86, height: int = 24) -> Text:
    weeks = 3  # ±3 weeks horizon
    cell_days = 1  # one cell = one day for this zoom
    geo = _geo(width, height, today, cell_days=cell_days,
               label_w=14, tail_w=12)
    # override start so horizon is centred on today
    horizon_days = geo.field_w * cell_days
    start = today - timedelta(days=geo.today_col * cell_days)
    geo = geo._replace(start=start)
    horizon_end = today + timedelta(days=(geo.field_w - 1 - geo.today_col) * cell_days)

    tasks = board.visible_tasks(False)
    late_n = sum(1 for t in tasks
                 if (d := _parse_iso(t.due_date)) and d < today and not _is_done(board, t))
    right = c(f"±{weeks}w", "mut")
    lines = [
        _header(c("GANTT", "accent", bold=True) + "  horizon", right, geo.width),
        _rule(geo.width),
    ]

    for p in board.visible_projects(False):
        # skip project if entirely outside horizon and not active
        ps = _parse_iso(p.start_date)
        pe = _parse_iso(p.due_date)
        if pe and pe < today - timedelta(weeks=weeks):
            continue
        if ps and ps > today + timedelta(weeks=weeks):
            continue

        cells = _lattice(geo)
        s = _col(ps, geo)
        e = _col(pe, geo)
        a, b = _col_value(s), _col_value(e)
        if b < a:
            a, b = b, a
        for x in range(a, b + 1):
            cells[x] = c("━", p.color)
        cells[b] = c("◆", p.color)
        if a <= geo.today_col <= b:
            cells[geo.today_col] = c("╎", "accent")
        dd = _day_delta(p.due_date, today)
        tail = ("—" if dd is None else
                c(f"{dd}d", "over" if dd < 0 else "mut"))
        lines.append(_row(p.name, cells, tail, geo, p.color))

        for t in _tasks_of(board, p.id):
            ts = _parse_iso(t.start_date)
            te = _parse_iso(t.due_date)
            # hide tasks fully outside horizon
            if te and te < today - timedelta(weeks=weeks):
                continue
            if ts and ts > today + timedelta(weeks=weeks):
                continue
            cells = _lattice(geo)
            s = _col(ts, geo)
            e = _col(te, geo)
            a, b = _col_value(s), _col_value(e)
            if b < a:
                a, b = b, a
            sel = t.id == selected_id
            tone = "ash" if _is_done(board, t) else _priority_hue(t.priority)
            if a == b and 0 <= a < geo.field_w:
                cells[a] = c("◆", tone)
            else:
                for x in range(a, b + 1):
                    cells[x] = c("━", tone)
            if a <= geo.today_col <= b:
                cells[geo.today_col] = c("╎", "accent")
            plain = fit(clip(t.title, geo.label_w - 4), geo.label_w - 4)
            title = f"[reverse]{escape(plain)}[/reverse]" if sel else escape(plain)
            label = "  " + c("▏", tone) + " " + title
            dd = _day_delta(t.due_date, today)
            tail = ("—" if dd is None else
                    c(f"{dd}d", "over" if dd and dd < 0 else "mut"))
            lines.append(label + " " + "".join(cells) + fit(tail, geo.tail_w, "right"))

    lines.append(_scale_row(geo))
    return _to_text(lines, height or len(lines) + 1, geo.width)


# =============================================================================
# VARIANT D · Swimlane Gantt
# Tasks grouped by project with clean separators; one compact lane per project.
# =============================================================================
def render_variant_d(board: Board, selected_id: str | None, today: date,
                     width: int = 86, height: int = 26) -> Text:
    geo = _geo(width, height, today, cell_days=2, label_w=15, tail_w=10)
    tasks = board.visible_tasks(False)
    late_n = sum(1 for t in tasks
                 if (d := _parse_iso(t.due_date)) and d < today and not _is_done(board, t))
    right = (c(f"▲{late_n}", "over", bold=True) if late_n
             else c("ok", "dim"))
    lines = [
        _header(c("GANTT", "accent", bold=True) + "  swimlanes", right, geo.width),
        _rule(geo.width),
    ]

    for p in board.visible_projects(False):
        # lane header
        cells = [c(" ", "dim")] * geo.field_w
        s = _col(_parse_iso(p.start_date), geo)
        e = _col(_parse_iso(p.due_date), geo)
        a, b = _col_value(s), _col_value(e)
        if b < a:
            a, b = b, a
        for x in range(a, b + 1):
            cells[x] = c("▬", p.color)
        cells[b] = c("◆", p.color)
        if a <= geo.today_col <= b:
            cells[geo.today_col] = c("╎", "accent")
        dd = _day_delta(p.due_date, today)
        tail = ("—" if dd is None else
                c(f"{dd}d", "over" if dd and dd < 0 else "mut"))
        label = c("▌", p.color) + " " + c(escape(fit(p.name, geo.label_w - 2)), p.color, bold=True)
        lines.append(label + " " + "".join(cells) + fit(tail, geo.tail_w, "right"))

        # tasks inside the lane, compact, one row each
        own = _tasks_of(board, p.id)
        if own:
            for t in own:
                cells = [c(" ", "dim")] * geo.field_w
                s = _col(_parse_iso(t.start_date), geo)
                e = _col(_parse_iso(t.due_date), geo)
                a, b = _col_value(s), _col_value(e)
                if b < a:
                    a, b = b, a
                tone = "ash" if _is_done(board, t) else _priority_hue(t.priority)
                if a == b and 0 <= a < geo.field_w:
                    cells[a] = c("●", tone)
                else:
                    for x in range(a, b):
                        cells[x] = c("▬", tone)
                    if 0 <= b < geo.field_w:
                        cells[b] = c("●", tone)
                if a <= geo.today_col <= b:
                    cells[geo.today_col] = c("╎", "accent")
                sel = t.id == selected_id
                plain = fit(clip(t.title, geo.label_w - 3), geo.label_w - 3)
                title = f"[reverse]{escape(plain)}[/reverse]" if sel else escape(plain)
                label = "   " + title
                lines.append(label + " " + "".join(cells) + " " * geo.tail_w)
        # lane separator
        lines.append(c("─" * geo.width, "frame"))

    # replace last separator with scale
    if lines and lines[-1] == c("─" * geo.width, "frame"):
        lines[-1] = _scale_row(geo)
    else:
        lines.append(_scale_row(geo))
    return _to_text(lines, height or len(lines) + 1, geo.width)


# ---------------------------------------------------------------------------
# Live preview (optional)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    from rich.console import Console
    from taskboard.models import Board

    ROOT = Path(__file__).resolve().parents[1]
    fixture = ROOT / "prototypes" / "out" / "_fixture_late.json"
    board = Board.load(fixture)
    tasks = board.visible_tasks(False)
    sel = tasks[len(tasks) // 3].id if tasks else None
    today = date(2026, 8, 17)
    con = Console(legacy_windows=False, color_system="truecolor")
    for name, fn in [("A minimal", render_variant_a),
                     ("B cards", render_variant_b),
                     ("C horizon", render_variant_c),
                     ("D swimlanes", render_variant_d)]:
        con.print(f"\n=== {name} ===")
        con.print(fn(board, sel, today, 86, 24))
