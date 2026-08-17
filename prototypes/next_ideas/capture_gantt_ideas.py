"""Headless capture of refined gantt prototypes -> SVG.

    python prototypes/next_ideas/capture_gantt_ideas.py

Creates three low-density renders so the operator can compare the current gantt
against two cleaner directions (B: timeline controls, C: task semantics).
"""
from __future__ import annotations

import contextlib
import io
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from rich.console import Console

from taskboard.models import Board, DEFAULT_PHASES, Project, Task
from taskboard.views import c, clip, fit

OUT = ROOT / "prototypes" / "next_ideas" / "out"
W, H = 86, 22
TODAY = date(2026, 8, 17)
START = date(2026, 8, 1)
CELL_DAYS = 2
FIELD_CELLS = 18
LABEL_W = 16
TAIL_W = W - LABEL_W - FIELD_CELLS - 1


def make_board() -> Board:
    p1 = Project(id="p1", name="Telemetry", color="sky",
                 start_date="2026-08-01", due_date="2026-08-31")
    p2 = Project(id="p2", name="Auth", color="violet",
                 start_date="2026-08-12", due_date="2026-08-25")
    p3 = Project(id="p3", name="Launch", color="lime",
                 start_date="2026-08-28", due_date="2026-08-28")
    tasks = [
        Task(id="t1", title="Ingestion API", project_id="p1", phase="Doing",
             priority="high", start_date="2026-08-04", due_date="2026-08-14"),
        Task(id="t2", title="Dashboard", project_id="p1", phase="Doing",
             priority="normal", start_date="2026-08-10", due_date="2026-08-22"),
        Task(id="t3", title="OAuth flow", project_id="p2", phase="Doing",
             priority="normal", start_date="2026-08-12", due_date="2026-08-25"),
        Task(id="t4", title="Cleanup", project_id="p2", phase="Backlog",
             priority="low", start_date="2026-08-20", due_date="2026-08-25"),
        Task(id="t5", title="Launch v1", project_id="p3", phase="Backlog",
             priority="high", start_date="2026-08-28", due_date="2026-08-28"),
    ]
    return Board([p1, p2, p3], tasks, path=Path("proto.json"),
                 phases=list(DEFAULT_PHASES))


def _cell(d: date | None) -> int | None:
    if d is None:
        return None
    days = (d - START).days
    col = days // CELL_DAYS
    if col < 0:
        return -1
    if col >= FIELD_CELLS:
        return FIELD_CELLS
    return col


def _lattice_cell(i: int) -> str:
    today_col = _cell(TODAY)
    if i == today_col:
        return c("╎", "accent")
    past = (i * CELL_DAYS + CELL_DAYS // 2) < (TODAY - START).days
    return c("·", "ash" if past else "dim")


def _empty_field() -> list[str]:
    return [_lattice_cell(i) for i in range(FIELD_CELLS)]


def _set_span(cells: list[str], start: int, end: int, glyph: str, hue: str,
              tip: str | None = None, dot_col: int | None = None) -> None:
    start = max(0, min(FIELD_CELLS - 1, start))
    end = max(0, min(FIELD_CELLS - 1, end))
    if end < start:
        start, end = end, start
    for x in range(start, end + 1):
        cells[x] = c(glyph, hue)
    if tip is not None:
        cells[end] = c(tip, hue)
    if dot_col is not None and start <= dot_col <= end:
        cells[dot_col] = c("●", hue)


def _fmt_row(label: str, cells: list[str], tail: str = "") -> str:
    left = fit(clip(label, LABEL_W - 2), LABEL_W - 2)
    line = f" {left:<{LABEL_W - 2}} " + "".join(cells)
    if tail:
        line += " " + tail
    return line


def _progress(project) -> float:
    # synthetic progress for the prototype
    if project.name == "Telemetry":
        return 0.55
    if project.name == "Auth":
        return 0.30
    return 0.0


def _is_late(task: Task) -> bool:
    d = task.due_date
    if not d:
        return False
    return date.fromisoformat(d) < TODAY and task.phase != "Done"


def render_baseline(board: Board) -> str:
    lines: list[str] = []
    late = sum(1 for t in board.tasks if _is_late(t))
    right = c(f"▲{late} past due", "over", bold=True) if late else c("nothing past due", "dim")
    header = f" {c('◆ GANTT', 'accent', bold=True)}" + " " * (W - 13 - len(right)) + right
    lines.append(header)
    lines.append("")

    for p in board.projects:
        cells = _empty_field()
        s = _cell(date.fromisoformat(p.start_date)) if p.start_date else 0
        e = _cell(date.fromisoformat(p.due_date)) if p.due_date else FIELD_CELLS - 1
        prog = _progress(p)
        dot = s + int(round((e - s) * prog))
        _set_span(cells, s, e, "─", p.color, tip="◆", dot_col=dot)
        tail = f"{int(prog * 100)}%  " + c("due " + str((date.fromisoformat(p.due_date) - TODAY).days) + "d",
                                            "over" if date.fromisoformat(p.due_date) < TODAY else "mut")
        lines.append(_fmt_row(p.name, cells, tail))

        for t in board.tasks:
            if t.project_id != p.id:
                continue
            cells = _empty_field()
            s = _cell(date.fromisoformat(t.start_date)) if t.start_date else _cell(TODAY)
            e = _cell(date.fromisoformat(t.due_date)) if t.due_date else FIELD_CELLS - 1
            _set_span(cells, s, e, "╌", p.color,
                      tip="○◔◑◕"[min(3, board.phase_index(t))])
            tail = c("late", "over") if _is_late(t) else "normal"
            lines.append(_fmt_row("  " + t.title, cells, tail))
    return "\n".join(lines)


def render_variant_b(board: Board) -> str:
    """Timeline controls: zoom + pan + a quieter today marker."""
    lines: list[str] = []
    controls = c("[", "mut") + c("2d", "ink") + c("]", "mut") + " " + c("[1d] [7d]", "mut") + "  " + c("← →", "accent")
    header = f" {c('◆ GANTT', 'accent', bold=True)}" + " " * (W - 13 - len(controls)) + controls
    lines.append(header)
    lines.append("")

    for p in board.projects:
        cells = _empty_field()
        s = _cell(date.fromisoformat(p.start_date)) if p.start_date else 0
        e = _cell(date.fromisoformat(p.due_date)) if p.due_date else FIELD_CELLS - 1
        prog = _progress(p)
        dot = s + int(round((e - s) * prog))
        _set_span(cells, s, e, "─", p.color, tip="◆", dot_col=dot)
        due_delta = (date.fromisoformat(p.due_date) - TODAY).days
        tail = c(f"due {due_delta}d", "over" if due_delta < 0 else "mut")
        lines.append(_fmt_row(p.name, cells, tail))

        for t in board.tasks:
            if t.project_id != p.id:
                continue
            cells = _empty_field()
            s = _cell(date.fromisoformat(t.start_date)) if t.start_date else _cell(TODAY)
            e = _cell(date.fromisoformat(t.due_date)) if t.due_date else FIELD_CELLS - 1
            _set_span(cells, s, e, "╌", p.color,
                      tip="○◔◑◕"[min(3, board.phase_index(t))])
            if _is_late(t):
                tail = c("▲", "over")
            elif s == e:
                tail = c("◆", "accent")
            else:
                tail = c("●", "dim")
            lines.append(_fmt_row("  " + t.title, cells, tail))
    return "\n".join(lines)


def render_variant_c(board: Board) -> str:
    """Task semantics: priority hue, dependency hint, milestone glyph."""
    lines: list[str] = []
    header = f" {c('◆ GANTT', 'accent', bold=True)}  {c('(focused: Telemetry)', 'mut')}"
    lines.append(header)
    lines.append("")

    priority_hue = {"low": "mut", "normal": "sky", "high": "rose"}
    dep_map = {"t4": "t3"}  # Cleanup depends on OAuth flow

    for p in board.projects:
        cells = _empty_field()
        s = _cell(date.fromisoformat(p.start_date)) if p.start_date else 0
        e = _cell(date.fromisoformat(p.due_date)) if p.due_date else FIELD_CELLS - 1
        _set_span(cells, s, e, "─", p.color, tip="◆")
        lines.append(_fmt_row(p.name, cells))

        for t in board.tasks:
            if t.project_id != p.id:
                continue
            cells = _empty_field()
            s = _cell(date.fromisoformat(t.start_date)) if t.start_date else _cell(TODAY)
            e = _cell(date.fromisoformat(t.due_date)) if t.due_date else FIELD_CELLS - 1
            hue = priority_hue.get(t.priority, "ink")
            if s == e:
                # milestone
                cells[s] = c("◆", hue)
                tip = None
            else:
                tip = "○◔◑◕"[min(3, board.phase_index(t))]
                _set_span(cells, s, e, "╌", hue, tip=tip)
            tail = ""
            if t.id in dep_map:
                tail = c("└─►", "mut")
            lines.append(_fmt_row("  " + t.title, cells, tail))
    return "\n".join(lines)


def _save(label: str, markup: str, slug: str) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    con = Console(record=True, width=W + 2, force_terminal=True,
                  legacy_windows=False, color_system="truecolor")
    # redirect_stdout keeps the prints off the user's terminal while the record
    # buffer still captures them for save_svg.
    with contextlib.redirect_stdout(io.StringIO()):
        for line in markup.splitlines():
            con.print(line if line.strip() else " ")
    path = OUT / f"gantt-{slug}.svg"
    con.save_svg(str(path), title=f"taskboard gantt — {label}")
    return path


def main() -> None:
    board = make_board()
    baseline = render_baseline(board)
    var_b = render_variant_b(board)
    var_c = render_variant_c(board)

    paths = [
        _save("current", baseline, "current"),
        _save("timeline controls", var_b, "variant-b"),
        _save("task semantics", var_c, "variant-c"),
    ]
    for p in paths:
        print("wrote", p)


if __name__ == "__main__":
    main()
