"""PROTOTYPE round — the presentation's gantt field has no date ruler.

    python prototypes/present_rulers/proto.py

The shipped `render_present` (PRES-C) draws the field with the today rule and
the week guides but no dates on any row, so the audience cannot read WHEN a bar
is. Three variants put the calendar back; each is composed from the SHIPPED
helpers (`gantt_month_row`, `gantt_day_row`, `_present_*`) on the PRES-C oracle
board, so only the ruler differs from production.

  S  shipped        — the defect, for reference
  A  two-row ruler  — the gantt view's own month band + tick row, above the field
  B  cursor ruler   — A, plus the cursor task's exact dates echoed on the tick row
  C  x-axis below   — one row UNDER the bars, a full date on every guide

Budget kept from PRES-C: accent belongs to the cursor alone, so today is
`bright` on every ruler (the gantt view lights it accent; here it cannot).

Writes SVGs to prototypes/present_rulers/out/ at 118x30 and 80x24.
"""
from __future__ import annotations

import io
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))

from rich.console import Console

import present_board as pb
from taskboard import views as V
from taskboard.views import (HEX, _md, _pad, _present_axis, _present_brief, _present_cols,
                             _present_counts, _present_finish, _present_note_lines,
                             _present_note_row, _present_span_row, _present_task_row,
                             _PresentGeo, c, critical_chain, escape, fit, gantt_day_row,
                             gantt_echo, gantt_month_row, header, present_tasks,
                             render_present, vis)

OUT = Path(__file__).resolve().parent / "out"
SIZES = [(118, 30), (80, 24)]


def _today_bright(fn, *a):
    """Run a shipped ruler builder with `accent` repainted `bright` — the
    present budget: the cursor owns accent. A `cursor` key keeps real accent
    for the one thing allowed to wear it (variant B's echo)."""
    saved, weekend = HEX["accent"], V._on_weekend
    HEX["cursor"] = saved
    HEX["accent"] = HEX["bright"]
    V._on_weekend = lambda m: m      # the present field shades no weekend; its ruler neither
    try:
        return fn(*a)
    finally:
        HEX["accent"], V._on_weekend = saved, weekend


def _ruler_rows(p: _PresentGeo, board, proj, cursor, variant: str) -> list[str]:
    """Variants A/B: the two rows the gantt view draws, re-seated in the
    present columns (label | gutter | field | space+chip)."""
    ax, today = p.ax, p.today
    marks = {}
    if (pd := V.parse_iso(proj.due_date)) and 0 <= ax.cell(pd) < ax.w:
        marks[ax.cell(pd)] = ("◆", proj.color)
    echo = None
    if variant == "B" and cursor is not None:
        echo = gantt_echo(cursor, board, ax, today)
        if echo is not None:
            echo = (echo[0], "cursor", echo[2], echo[3])
    mcells = _today_bright(gantt_month_row, ax, today, marks)
    dcells, meta = _today_bright(gantt_day_row, ax, today, echo)
    mlabel = c(fit(f"today {today:%a} {_md(today)}", p.label_w - 1, "right") + " ", "bright",
               bold=True)
    if echo is not None:
        lab = meta["echo_label"] or "cursor's dates ▸"
        dlabel = c(fit(lab, p.label_w - 1, "right") + " ", "cursor", bold=True)
    else:
        dlabel = c(fit(V._gantt_scale_label(ax.k, meta["cadence"], p.label_w),
                       p.label_w - 1, "right") + " ", "dim")
    tail = " " * (p.chip_w + 1)
    return [_pad(_pad(mlabel, p.label_w) + " " + "".join(mcells) + tail, p.width),
            _pad(_pad(dlabel, p.label_w) + " " + "".join(dcells) + tail, p.width)]


def _axis_below(p: _PresentGeo) -> str:
    """Variant C: one x-axis row under the bars. Every guide gets `╵` and, where
    it fits with a blank either side, its full date (`Sep 21`); today's column
    gets `╎today`, which wins any collision."""
    ax, w = p.ax, p.ax.w
    glyph: list = [None] * w

    def free(a: int, b: int) -> bool:
        return a >= 0 and b <= w and all(glyph[i] is None for i in range(max(0, a - 1), min(w, b + 1)))

    def put(x: int, s: str, key: str, bold=False):
        for i, ch in enumerate(s):
            glyph[x + i] = (ch, key, bold)

    tc = ax.tc
    if 0 <= tc < w:
        lab = "╎today"
        x = tc if tc + len(lab) <= w else tc - len(lab) + 1
        put(x, lab if x == tc else "today╎", "bright", True)
    for x in sorted(ax.guides()):
        d = next(d for d in ax.days_in(x) if ax.cell(d) == x)
        lab = "╵" + _md(d)
        if free(x, x + len(lab)):
            put(x, lab, "mut")
        elif glyph[x] is None:
            put(x, "╵", "dim")
    cells = "".join(c(" ", "dim") if g is None else c(g[0], g[1], bold=g[2]) for g in glyph)
    label = c(fit(V._gantt_scale_label(ax.k, V.gantt_cadence(ax)[0], p.label_w),
                  p.label_w - 1, "right") + " ", "dim")
    return _pad(_pad(label, p.label_w) + " " + cells + " " * (p.chip_w + 1), p.width)


def render_variant(board, variant: str, w: int, h: int, cursor_id=pb.CURSOR):
    if variant == "S":
        return render_present(board, pb.PROJECT_ID, cursor_id, pb.TODAY, w, h)
    today = pb.TODAY
    proj = board.project_by_id(pb.PROJECT_ID)
    open_t, tasks = present_tasks(board, pb.PROJECT_ID)
    late, open_n, done = _present_counts(open_t, tasks, today)
    wide = w >= 100
    label_w, chip_w, field_w = _present_cols(w, wide)
    ax = _present_axis(board, proj, open_t, field_w, today)
    p = _PresentGeo(w, label_w, chip_w, field_w, ax, set(critical_chain(board)), today, wide,
                    proj.color)
    wanted = board.task_by_id(cursor_id)
    cursor = (wanted if wanted in open_t else open_t[0]) if open_t else None
    title = (c("◆ PRESENT", "bright", bold=True) + c(" · ", "dim")
             + c(escape(proj.name), proj.color, bold=True) + c(" — hybrid", "mut"))
    right = c(f"{open_n} open", "mut") + c(" · ", "dim") \
        + (c(f"▲{late} past due", "over", bold=True) if late else c(f"{done} done", "done"))
    lines = [header(title, right, w)]
    if variant in "AB":
        lines += _ruler_rows(p, board, proj, cursor, variant)
    lines.append(_present_span_row(proj, board, p))
    for t in open_t:
        lines.append(_present_task_row(t, board, p, cursor=cursor is not None and t.id == cursor.id))
    if variant == "C":
        lines.append(_axis_below(p))
    lines.append(_pad(c("─" * w, "frame"), w))
    for t in open_t:
        on = cursor is not None and t.id == cursor.id
        lines.append(_present_brief(t, p, on, w))
        if on:
            for ln in _present_note_lines(t.notes, w - 4, 3):
                lines.append(_present_note_row(ln, w, w - 4))
    lines.append(_pad(c(escape(fit(" ←→  move the cursor · the cursor'd task's notes expand", w)),
                        "dim"), w))
    return _present_finish(lines, h, w)


def svg(text, w: int, title: str) -> str:
    con = Console(width=w, record=True, file=io.StringIO(), color_system="truecolor",
                  legacy_windows=False)
    con.print(text, overflow="crop", no_wrap=True, soft_wrap=False)
    out = con.export_svg(title=title)
    return re.sub(r"@font-face\s*\{[^}]*\}", "", out)


def main() -> None:
    import tempfile
    OUT.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp())
    board = pb.build(tmp / "board.json")
    names = {"S": "shipped", "A": "two-row ruler", "B": "cursor ruler", "C": "x-axis below"}
    for v in "SABC":
        for w, h in SIZES:
            t = render_variant(board, v, w, h)
            (OUT / f"present-{v}-{w}x{h}.svg").write_text(svg(t, w, f"{v} · {names[v]} · {w}x{h}"),
                                                         encoding="utf-8")
            (OUT / f"present-{v}-{w}x{h}.txt").write_text(t.plain, encoding="utf-8")
    # B follows the cursor: one more frame with the cursor on a later task
    later = [t.id for t in present_tasks(board, pb.PROJECT_ID)[0]][-2]
    t = render_variant(board, "B", 118, 30, cursor_id=later)
    (OUT / "present-B2-118x30.svg").write_text(svg(t, 118, "B · cursor moved"), encoding="utf-8")
    (OUT / "present-B2-118x30.txt").write_text(t.plain, encoding="utf-8")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
