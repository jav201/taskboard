"""Gantt axis/scale prototypes — how to make the lattice read as dates.

Run:      python prototypes/gantt_axis_variants.py
Capture:  python prototypes/capture_axis_variants.py
"""
from __future__ import annotations

import sys
from datetime import date, timedelta
from pathlib import Path

from rich.text import Text

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from taskboard.models import Board
from prototypes.gantt_variants import (
    Geo, _col, _col_value, _geo, _header, _is_flag, _lattice, _parse_iso,
    _priority_hue, _project_color, _project_name, _rule, _row, _scale_row,
    _tasks_of, _to_text, c, clip, fit, vis,
)


def _is_done(board, task):
    return bool(board.phases) and task.phase == board.phases[-1]


# ---------------------------------------------------------------------------
# Shared: build a ruler row that sits between the header and the project lanes.
# ---------------------------------------------------------------------------
def _month_ruler(geo: Geo, today: date) -> str:
    """A top ruler showing month boundaries and mid-month anchors.

    Each cell is `cell_days` wide. Month abbreviations sit on the cell that
    contains the 1st; day-of-month '15' sits on the cell that contains the 15th,
    only when it does not collide with a month name. The goal is a readable
    date scale, not a dense calendar.
    """
    span = geo.field_w
    body = [" "] * span

    def place(text: str, at: int) -> bool:
        if at < 0 or at + len(text) > span:
            return False
        if any(body[at + i] != " " for i in range(len(text))):
            return False
        for i, ch in enumerate(text):
            body[at + i] = ch
        return True

    # month starts and mid-month anchors
    for dc in range(-geo.today_col * geo.cell_days,
                    (span - geo.today_col) * geo.cell_days):
        d = today + timedelta(days=dc)
        col = dc // geo.cell_days + geo.today_col
        if not (0 <= col < span):
            continue
        if d.day == 1:
            place(d.strftime("%b").upper(), col)
        elif d.day == 15 and body[col] == " ":
            place(str(d.day), col)

    out = []
    for i, ch in enumerate(body):
        tone = "mut" if ch != " " else ("ash" if i < geo.today_col else "dim")
        out.append(c(ch, tone))
    return " " * geo.label_w + "".join(out) + " " * geo.tail_w


def _weekend_lattice(geo: Geo, today: date) -> list[str]:
    """A lattice where cells that contain a weekend day are left blank.

    One cell is two days, so a weekend cell is any cell whose two-day window
    touches Saturday or Sunday. The result is a weekly rhythm of solid and
    empty bands, making the date scale legible without extra labels.
    """
    cells = []
    for i in range(geo.field_w):
        if i == geo.today_col:
            cells.append(c("╎", "accent"))
            continue
        d0 = geo.start + timedelta(days=i * geo.cell_days)
        d1 = d0 + timedelta(days=geo.cell_days - 1)
        touches_weekend = any(d.weekday() >= 5 for d in (d0, d1))
        mid = d0 + timedelta(days=geo.cell_days // 2)
        if touches_weekend:
            # weekend cells are left visually empty so weeks read as bands
            cells.append(" ")
        else:
            cells.append(c("·", "ash" if mid < geo.today else "dim"))
    return cells


def _week_ticks(geo: Geo, today: date) -> list[str]:
    """Prominent Monday ticks on every row, plus a small 'W' band."""
    cells = []
    for i in range(geo.field_w):
        if i == geo.today_col:
            cells.append(c("╎", "accent"))
        else:
            d = geo.start + timedelta(days=i * geo.cell_days + geo.cell_days // 2)
            if d.weekday() == 0:
                cells.append(c("├", "mut"))   # Monday tick
            elif d.weekday() == 6:
                cells.append(c("┤", "ash"))   # Sunday tick
            else:
                mid_day = geo.start + timedelta(days=i * geo.cell_days + geo.cell_days // 2)
                cells.append(c("·", "ash" if mid_day < geo.today else "dim"))
    return cells


def _render_base(board: Board, selected_id, today: date, width: int, height: int,
                 lattice_fn, show_ruler: bool = False) -> Text:
    geo = _geo(width, height, today, cell_days=2, label_w=15, tail_w=10)
    tasks = board.visible_tasks(False)
    late_n = sum(1 for t in tasks
                 if (d := _parse_iso(t.due_date)) and d < today and not _is_done(board, t))
    right = (c(f"▲{late_n}", "over", bold=True) if late_n else c("ok", "dim"))
    lines = [
        _header(c("GANTT", "accent", bold=True) + "  swimlanes", right, geo.width),
        _rule(geo.width),
    ]
    if show_ruler:
        lines.append(_month_ruler(geo, today))

    first = True
    for p in board.visible_projects(False):
        if not first:
            lines.append(c("─" * geo.width, "frame"))
        first = False

        # project lane header
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
        dd = (_parse_iso(p.due_date) - today).days if p.due_date else None
        tail = ("—" if dd is None else c(f"{dd}d", "over" if dd < 0 else "mut"))
        label = c("▌", p.color) + " " + c(escape(fit(p.name, geo.label_w - 2)), p.color, bold=True)
        lines.append(label + " " + "".join(cells) + fit(tail, geo.tail_w, "right"))

        # tasks inside the lane
        own = _tasks_of(board, p.id)
        if own:
            for t in own:
                cells = lattice_fn(geo)
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

    # scale at the bottom
    lines.append(_scale_row(geo))
    return _to_text(lines, height or len(lines) + 1, geo.width)


# --- variants ----------------------------------------------------------------
def render_axis_a(board: Board, selected_id, today: date,
                  width: int = 86, height: int = 26) -> Text:
    """A: default lattice + a top ruler row with months and week numbers."""
    return _render_base(board, selected_id, today, width, height,
                        lambda geo: _lattice(geo), show_ruler=True)


def render_axis_b(board: Board, selected_id, today: date,
                  width: int = 86, height: int = 26) -> Text:
    """B: prominent Monday/Sunday ticks on every row, no extra ruler."""
    return _render_base(board, selected_id, today, width, height,
                        lambda geo: _week_ticks(geo, today), show_ruler=False)


def render_axis_c(board: Board, selected_id, today: date,
                  width: int = 86, height: int = 26) -> Text:
    """C: weekend-aware lattice + top ruler. Blank-ish cells on weekends make
    the weekly rhythm visible across the whole field."""
    return _render_base(board, selected_id, today, width, height,
                        lambda geo: _weekend_lattice(geo, today), show_ruler=True)


def render_axis_d(board: Board, selected_id, today: date,
                  width: int = 86, height: int = 26) -> Text:
    """D: month bands — alternating lattice tone by month."""
    geo = _geo(width, height, today, cell_days=2, label_w=15, tail_w=10)
    tasks = board.visible_tasks(False)
    late_n = sum(1 for t in tasks
                 if (d := _parse_iso(t.due_date)) and d < today and not _is_done(board, t))
    right = (c(f"▲{late_n}", "over", bold=True) if late_n else c("ok", "dim"))
    lines = [
        _header(c("GANTT", "accent", bold=True) + "  month bands", right, geo.width),
        _rule(geo.width),
    ]

    first = True
    for p in board.visible_projects(False):
        if not first:
            lines.append(c("─" * geo.width, "frame"))
        first = False

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
        dd = (_parse_iso(p.due_date) - today).days if p.due_date else None
        tail = ("—" if dd is None else c(f"{dd}d", "over" if dd < 0 else "mut"))
        label = c("▌", p.color) + " " + c(escape(fit(p.name, geo.label_w - 2)), p.color, bold=True)
        lines.append(label + " " + "".join(cells) + fit(tail, geo.tail_w, "right"))

        own = _tasks_of(board, p.id)
        for t in own:
            row_cells = []
            for i in range(geo.field_w):
                if i == geo.today_col:
                    row_cells.append(c("╎", "accent"))
                    continue
                mid = geo.start + timedelta(days=i * geo.cell_days + geo.cell_days // 2)
                # alternate tone by month
                band = "mut" if mid.month % 2 else "dim"
                past = mid < geo.today
                row_cells.append(c("·", "ash" if past else band))
            s = _col(_parse_iso(t.start_date), geo)
            e = _col(_parse_iso(t.due_date), geo)
            a, b = _col_value(s), _col_value(e)
            if b < a:
                a, b = b, a
            tone = "ash" if _is_done(board, t) else _priority_hue(t.priority)
            if a == b and 0 <= a < geo.field_w:
                row_cells[a] = c("●", tone)
            else:
                for x in range(a, b):
                    row_cells[x] = c("▬", tone)
                if 0 <= b < geo.field_w:
                    row_cells[b] = c("●", tone)
            if a <= geo.today_col <= b:
                row_cells[geo.today_col] = c("╎", "accent")
            sel = t.id == selected_id
            plain = fit(clip(t.title, geo.label_w - 3), geo.label_w - 3)
            title = f"[reverse]{escape(plain)}[/reverse]" if sel else escape(plain)
            label = "   " + title
            lines.append(label + " " + "".join(row_cells) + " " * geo.tail_w)

    lines.append(_month_ruler(geo, today))
    return _to_text(lines, height or len(lines) + 1, geo.width)


from rich.markup import escape


if __name__ == "__main__":
    from rich.console import Console
    ROOT = Path(__file__).resolve().parents[1]
    fixture = ROOT / "prototypes" / "out" / "_fixture_late.json"
    board = Board.load(fixture)
    tasks = board.visible_tasks(False)
    sel = tasks[len(tasks) // 3].id if tasks else None
    today = date(2026, 8, 17)
    con = Console(legacy_windows=False, color_system="truecolor")
    for name, fn in [("A top ruler", render_axis_a),
                     ("B week ticks", render_axis_b),
                     ("C day grid", render_axis_c),
                     ("D month bands", render_axis_d)]:
        con.print(f"\n=== {name} ===")
        con.print(fn(board, sel, today, 86, 28))
