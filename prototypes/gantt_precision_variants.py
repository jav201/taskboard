"""Gantt date-precision prototypes — combining A and D and adding labels.

Run:      python prototypes/gantt_precision_variants.py
Capture:  python prototypes/capture_precision_variants.py
"""
from __future__ import annotations

import sys
from datetime import date, timedelta
from pathlib import Path

from rich.text import Text

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from taskboard.models import Board
from prototypes.gantt_axis_variants import _month_ruler
from prototypes.gantt_variants import (
    Geo, _col, _col_value, _geo, _header, _is_done, _parse_iso,
    _priority_hue, _rule, _scale_row, _tasks_of, _to_text, c, clip, fit, vis,
)
from rich.markup import escape


def _month_bands(geo: Geo, today: date) -> list[str]:
    """Lattice with a subtle tone shift per month."""
    cells = []
    for i in range(geo.field_w):
        if i == geo.today_col:
            cells.append(c("╎", "accent"))
            continue
        mid = geo.start + timedelta(days=i * geo.cell_days + geo.cell_days // 2)
        band = "mut" if mid.month % 2 == 0 else "dim"
        past = mid < geo.today
        cells.append(c("·", "ash" if past else band))
    return cells


def _dense_ruler(geo: Geo, today: date) -> str:
    """Top ruler with month names and 1st/15th anchors."""
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


def _date_labels(geo: Geo, today: date) -> list[str]:
    """Floating day-of-month labels (1st and 15th only) on the lattice."""
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

    for dc in range(-geo.today_col * geo.cell_days,
                    (span - geo.today_col) * geo.cell_days):
        d = today + timedelta(days=dc)
        col = dc // geo.cell_days + geo.today_col
        if not (0 <= col < span) or col == geo.today_col:
            continue
        if d.day in (1, 15):
            place(str(d.day), col)

    cells = []
    for i, ch in enumerate(body):
        if i == geo.today_col:
            cells.append(c("╎", "accent"))
        elif ch != " ":
            cells.append(c(ch, "mut"))
        else:
            mid = geo.start + timedelta(days=i * geo.cell_days + geo.cell_days // 2)
            cells.append(c("·", "ash" if mid < geo.today else "dim"))
    return cells


def _date_chip(d: date | None, today: date) -> tuple[str, str]:
    if d is None:
        return "—", "dim"
    delta = (d - today).days
    label = d.strftime("%b %d").replace(" 0", " ")
    tone = "over" if delta < 0 else "soon" if delta == 0 else "mut"
    return label, tone


def _render_base(board: Board, selected_id, today: date, width: int, height: int,
                 lattice_fn, ruler_fn=None, date_chips: bool = False) -> Text:
    # wider tail when showing date chips
    tail_w = 20 if date_chips else 10
    geo = _geo(width, height, today, cell_days=2, label_w=15, tail_w=tail_w)
    tasks = board.visible_tasks(False)
    late_n = sum(1 for t in tasks
                 if (d := _parse_iso(t.due_date)) and d < today and not _is_done(board, t))
    right = (c(f"▲{late_n}", "over", bold=True) if late_n else c("ok", "dim"))
    lines = [
        _header(c("GANTT", "accent", bold=True) + "  precision", right, geo.width),
        _rule(geo.width),
    ]
    if ruler_fn:
        lines.append(ruler_fn(geo, today))

    first = True
    for p in board.visible_projects(False):
        if not first:
            lines.append(c("─" * geo.width, "frame"))
        first = False

        s = _parse_iso(p.start_date)
        e = _parse_iso(p.due_date)
        cells = [c(" ", "dim")] * geo.field_w
        sc = _col(s, geo)
        ec = _col(e, geo)
        a, b = _col_value(sc), _col_value(ec)
        if b < a:
            a, b = b, a
        for x in range(a, b + 1):
            cells[x] = c("▬", p.color)
        cells[b] = c("◆", p.color)
        if a <= geo.today_col <= b:
            cells[geo.today_col] = c("╎", "accent")

        if date_chips:
            s_lab, s_tone = _date_chip(s, today)
            e_lab, e_tone = _date_chip(e, today)
            tail_plain = f"{s_lab} → {e_lab}"
            tail = fit(tail_plain, geo.tail_w, "right")
            tail = c(s_lab, s_tone) + " → " + c(e_lab, e_tone)
            # re-pad to exact width after markup
            tail = " " * max(0, geo.tail_w - vis(tail_plain)) + tail
        else:
            dd = (e - today).days if e else None
            tail = "—" if dd is None else c(f"{dd}d", "over" if dd and dd < 0 else "mut")
            tail = fit(tail, geo.tail_w, "right")

        label = c("▌", p.color) + " " + c(escape(fit(p.name, geo.label_w - 2)), p.color, bold=True)
        lines.append(label + " " + "".join(cells) + tail)

        own = _tasks_of(board, p.id)
        for t in own:
            cells = lattice_fn(geo)
            ts = _parse_iso(t.start_date)
            te = _parse_iso(t.due_date)
            sc = _col(ts, geo)
            ec = _col(te, geo)
            a, b = _col_value(sc), _col_value(ec)
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

            if date_chips:
                s_lab, s_tone = _date_chip(ts, today)
                e_lab, e_tone = _date_chip(te, today)
                tail_plain = f"{s_lab} → {e_lab}"
                tail = c(s_lab, s_tone) + " → " + c(e_lab, e_tone)
                tail = " " * max(0, geo.tail_w - vis(tail_plain)) + tail
            else:
                dd = (te - today).days if te else None
                tail = "—" if dd is None else c(f"{dd}d", "over" if dd and dd < 0 else "mut")
                tail = fit(tail, geo.tail_w, "right")
            lines.append(label + " " + "".join(cells) + tail)

    lines.append(_scale_row(geo))
    return _to_text(lines, height or len(lines) + 1, geo.width)


# --- variants ----------------------------------------------------------------
def render_prec_a(board: Board, selected_id, today: date,
                  width: int = 86, height: int = 26) -> Text:
    """E: month bands + dense ruler (months + 1/5/10/15/20/25)."""
    return _render_base(board, selected_id, today, width, height,
                        lambda geo: _month_bands(geo, today), ruler_fn=_dense_ruler)


def render_prec_b(board: Board, selected_id, today: date,
                  width: int = 86, height: int = 26) -> Text:
    """F: 1st/15th labels floating on every row + month ruler."""
    return _render_base(board, selected_id, today, width, height,
                        lambda geo: _date_labels(geo, today), ruler_fn=_month_ruler)


def render_prec_c(board: Board, selected_id, today: date,
                  width: int = 86, height: int = 26) -> Text:
    """G: exact start/due date chips in the right tail."""
    return _render_base(board, selected_id, today, width, height,
                        lambda geo: _month_bands(geo, today),
                        ruler_fn=_month_ruler, date_chips=True)


if __name__ == "__main__":
    from rich.console import Console
    ROOT = Path(__file__).resolve().parents[1]
    fixture = ROOT / "prototypes" / "out" / "_fixture_late.json"
    board = Board.load(fixture)
    tasks = board.visible_tasks(False)
    sel = tasks[len(tasks) // 3].id if tasks else None
    today = date(2026, 8, 17)
    con = Console(legacy_windows=False, color_system="truecolor")
    for name, fn in [("E month bands + dense ruler", render_prec_a),
                     ("F 1st/15th labels + ruler", render_prec_b),
                     ("G date chips on bars", render_prec_c)]:
        con.print(f"\n=== {name} ===")
        con.print(fn(board, sel, today, 86, 30))
