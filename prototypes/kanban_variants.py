"""Kanban design variants — PROTOTYPE (sub-shape A: mounted in the real app).

Run:      python prototypes/kanban_variants.py
Capture:  python prototypes/kanban_variants.py --capture   (writes .txt + .svg)

Press  V  to cycle variants, 0 for the shipped baseline. Everything else is the
real taskboard: real board data, real ribbon/footer, real cursor + modals.

This file monkeypatches ``views.render_kanban`` only. It does not modify any
shipped module, so deleting this file returns the app to stock.

The three variants deliberately DISAGREE about structure (tui-design/PROTOTYPE.md):
different layout, different density mechanism, different primary affordance.

  A TRIAGE  — "what do I work on next?"  hero + drawn countdown + ranked queue
  B MATRIX  — "where is everything?"     full-bleed dot-matrix heatmap (Nothing-OS)
  C FLOW    — "is my flow healthy?"      content-weighted columns + WIP health

Baseline failures each variant is answering (measured on the real board:
28 tasks / 4 phases, distribution 24-0-2-5):
  * equal-width columns spend ~60% of the screen on near-empty phases
  * 24 rows of identical weight -> no entry point for the eye
  * titles truncate at ~24 chars while indicator glyphs survive (priority inverted)
  * an empty phase renders as blank cells, indistinguishable from broken
"""
from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from rich.markup import escape
from rich.text import Text

from taskboard import views as V
from taskboard.views import (HEX, blank_line, bottom, c, fill_height, fit,
                             header, line, phase_buckets,
                             sort_by_due, status_glyph, project_color)
from taskboard.models import Board, parse_iso


def _border(left: str, fill: str, right: str, junctions: dict, w: int) -> str:
    """Local copy for the same reason `progress_bar` below is one.

    These variants draw a FRAMED kanban. The app went frameless and replaced
    `_border` with `rule_row`, which has no left/right glyphs -- so calling the
    app's current function here would silently change what the prototype is a
    prototype OF. Copied, not adapted."""
    span = w - 2
    chars = [fill] * span
    for pos, ch in junctions.items():
        if 0 <= pos < span:
            chars[pos] = ch
    return c(left + "".join(chars) + right, "frame")


def progress_bar(done: int, total: int, width: int, color: str) -> str:
    """Local copy, deliberately, and the reason is the merge that needed it.

    This used to be imported from `taskboard.views`. The app's gantt/lanes
    redesign removed it -- correctly, nothing in the app draws this bar any
    more -- and merging this branch onto that app broke every variant here
    with an ImportError. Re-adding a dead function to the SHIPPING module to
    keep a prototype running would be the wrong direction: a prototype pinning
    itself to an application internal is the defect, and 8 more symbols on the
    import line above are still exposed to it.
    """
    if width <= 0:
        return ""
    if total <= 0:
        return c("░" * width, "dim")
    filled = max(0, min(width, round(width * done / total)))
    return c("▇" * filled, color) + c("░" * (width - filled), "frame")

# --------------------------------------------------------------------------
# drawn type: a 3x5 block font. The terminal has no type scale, so large type
# must be DRAWN (tui-design/HIERARCHY.md). Only width-1 glyphs, so alignment
# survives any monospace font (the codebase's M22 ambiguous-glyph rule).
# --------------------------------------------------------------------------
FONT = {
    "0": ("███", "█ █", "█ █", "█ █", "███"),
    "1": ("  █", "  █", "  █", "  █", "  █"),
    "2": ("███", "  █", "███", "█  ", "███"),
    "3": ("███", "  █", "███", "  █", "███"),
    "4": ("█ █", "█ █", "███", "  █", "  █"),
    "5": ("███", "█  ", "███", "  █", "███"),
    "6": ("███", "█  ", "███", "█ █", "███"),
    "7": ("███", "  █", "  █", "  █", "  █"),
    "8": ("███", "█ █", "███", "█ █", "███"),
    "9": ("███", "█ █", "███", "  █", "███"),
    "-": ("   ", "   ", "███", "   ", "   "),
    "!": ("█  ", "█  ", "█  ", "   ", "█  "),
    "?": ("███", "  █", " ██", "   ", " █ "),
    " ": ("   ", "   ", "   ", "   ", "   "),
}


def draw_text(s: str) -> list[str]:
    """Render `s` as 5 rows of block glyphs. Unknown chars become spaces."""
    rows = []
    for r in range(5):
        rows.append(" ".join(FONT.get(ch, FONT[" "])[r] for ch in s))
    return rows


def days_left(task, today: date) -> int | None:
    d = parse_iso(task.due_date)
    return None if d is None else (d - today).days


def urgency_key(board: Board, task, today: date) -> tuple:
    """Sort key for the triage queue: blocked first, then soonest due."""
    dl = days_left(task, today)
    return (0 if task.blocked else 1,
            0 if dl is not None else 1,
            dl if dl is not None else 9999)


def _all_visible(board: Board, show_archived: bool):
    return board.visible_tasks(show_archived)


# ==========================================================================
# VARIANT A — TRIAGE.  affordance: decide what to do next.
# layout: drawn hero + ranked queue.  density: block type (hero) + plain rows.
# ==========================================================================
def render_variant_a(board, show_archived, selected_id, today=None,
                     width=68, height=0, line_map=None, presentation="grouped") -> Text:
    today = today or date.today()
    w = V._clamp_width(width)
    inner = w - 2
    tasks = [t for t in _all_visible(board, show_archived) if not board.is_done(t)]
    queue = sorted(tasks, key=lambda t: urgency_key(board, t, today))
    hero = next((t for t in queue if t.id == selected_id), queue[0] if queue else None)

    lines = [header(c("TRIAGE", "accent", bold=True),
                    c(f"{len(queue)} open", "mut"), w)]

    if hero is None:
        lines.append(line(fit("  Nothing open. Press  a  to add a task.", inner)))
        lines.append(bottom(None, w))
        return Text.from_markup("\n".join(fill_height(lines, height, w)))

    # --- hero: the countdown is DRAWN, not labelled (the signature rule) ---
    dl = days_left(hero, today)
    if hero.blocked:
        glyph, tone, cap = "!", "over", "BLOCKED"
    elif dl is None:
        glyph, tone, cap = "?", "mut", "NO DUE DATE"
    elif dl < 0:
        glyph, tone, cap = str(min(99, -dl)), "over", "DAYS OVERDUE"
    elif dl == 0:
        glyph, tone, cap = "0", "amber", "DUE TODAY"
    else:
        glyph, tone, cap = str(min(99, dl)), ("amber" if dl <= 3 else "accent"), "DAYS LEFT"

    proj = board.project_by_id(hero.project_id)
    pname = proj.name if proj else "Inbox"
    pcol = project_color(board, hero)
    big = draw_text(glyph)
    bw = max(len(r) for r in big)
    title = escape(hero.title)
    meta = [
        (c("▐ ", pcol) + c(fit(pname, inner - bw - 8), "hd")),
        (c(fit(title, inner - bw - 8), "ink", bold=True)),
        "",
        (c(fit(f"{hero.phase}   {cap.lower()}", inner - bw - 8), "mut")),
        (c(fit(f"e edit   enter details   x archive", inner - bw - 8), "dim")),
    ]
    for i in range(5):
        left = c(big[i], tone)
        pad = " " * 3
        right = meta[i] if i < len(meta) else ""
        vis = bw + 3 + len(V._strip(right))
        lines.append(line(" " + left + pad + right + " " * max(0, inner - vis - 1)))
    if line_map is not None:
        line_map[hero.id] = len(lines) - 1

    lines.append(_border("├", "─", "┤", {}, w))

    # --- the queue: dense, dim, ranked. one row per task. ---
    lines.append(line(c(fit("  UP NEXT", inner), "mut")))
    body = height - len(lines) - 2 if height else 12
    for t in queue[: max(0, body)]:
        if t.id == hero.id:
            continue
        d = days_left(t, today)
        chip = ("blk" if t.blocked else
                ("--" if d is None else (f"{-d}d!" if d < 0 else f"{d}d")))
        tone_t = ("over" if t.blocked or (d is not None and d < 0)
                  else ("amber" if d is not None and d <= 3 else "dim"))
        sel = t.id == selected_id
        pc = project_color(board, t)
        txt = fit(escape(t.title), inner - 12)
        row = (c(" ▊ " if sel else "   ", pc)
               + c(txt, "ink" if sel else "mut", bold=sel)
               + c(fit(chip, 7, "right"), tone_t) + "  ")
        lines.append(line(row))
        if line_map is not None:
            line_map[t.id] = len(lines) - 1

    lines.append(bottom(None, w))
    return Text.from_markup("\n".join(fill_height(lines, height, w)))


# ==========================================================================
# VARIANT B — MATRIX.  affordance: scan where everything is.
# layout: full-bleed grid.  density: dot-matrix (Nothing-OS), monochrome+accent.
# ==========================================================================
DOTS = "·▪▊█"          # 4 density levels, width-1 each


def render_variant_b(board, show_archived, selected_id, today=None,
                     width=68, height=0, line_map=None, presentation="grouped") -> Text:
    today = today or date.today()
    w = V._clamp_width(width)
    inner = w - 2
    tasks = _all_visible(board, show_archived)
    projects = list(board.visible_projects(show_archived))

    lines = [header(c("MATRIX", "accent", bold=True),
                    c(f"{len(tasks)} tasks · {len(board.phases)} phases", "mut"), w)]

    label_w = 18
    meter_w = 12
    grid_w = inner - label_w - meter_w - 2
    cellw = max(3, grid_w // max(1, len(board.phases)))

    # phase header row
    head = " " * label_w + " "
    for ph in board.phases:
        head += fit(ph.upper()[: cellw - 1], cellw)
    head += fit("PROGRESS", meter_w + 1, "right")
    lines.append(line(c(fit(head, inner), "mut")))

    rows = [(p.name, p.color, [t for t in tasks if t.project_id == p.id])
            for p in projects]
    loose = [t for t in tasks if board.project_by_id(t.project_id) is None]
    if loose:
        rows.append(("Inbox", "dim", loose))

    for name, colr, items in rows:
        buckets = phase_buckets(board, items)
        done = sum(1 for t in items if board.is_done(t))
        sel_here = any(t.id == selected_id for t in items)
        row = c("▐ ", colr) + c(fit(escape(name), label_w - 2),
                                "ink" if sel_here else "hd", bold=sel_here) + " "
        for bucket in buckets:
            n = len(bucket)
            if n == 0:
                row += c(fit("·", cellw), "frame")
            else:
                lvl = DOTS[min(3, (n - 1) // 3 + 1)]
                shown = min(n, cellw - 2)
                bar = lvl * shown
                has_sel = any(t.id == selected_id for t in bucket)
                row += c(fit(bar, cellw), "accent" if has_sel else colr)
        pct = 0 if not items else round(100 * done / len(items))
        row += " " + progress_bar(done, max(1, len(items)), meter_w - 5, colr)
        row += c(fit(f"{pct:>3}%", 5, "right"), "mut")
        lines.append(line(fit_markup(row, inner)))
        if line_map is not None and items:
            for t in items:
                line_map.setdefault(t.id, len(lines) - 1)

    lines.append(_border("├", "─", "┤", {}, w))

    # Drill-down: the grid answers "where is everything", this answers "what is
    # in the thing I'm pointing at". It also FILLS the remaining height — the
    # first draft left ~22 blank rows, reproducing the baseline's worst flaw.
    sel = next((t for t in tasks if t.id == selected_id), None)
    if sel is None:
        lines.append(line(c(fit("  no selection — ↑↓←→ to move, enter for details",
                                inner), "dim")))
        lines.append(bottom(None, w))
        return Text.from_markup("\n".join(fill_height(lines, height, w)))

    # Group every task by project, SELECTED project first, then fill the pane
    # until the height is used. Padding with blanks would just re-create the
    # baseline's empty-screen problem one level down.
    groups: list[tuple[str, str, list]] = []
    for p in board.visible_projects(show_archived):
        items = [t for t in tasks if t.project_id == p.id]
        if items:
            groups.append((p.name, p.color, items))
    loose2 = [t for t in tasks if board.project_by_id(t.project_id) is None]
    if loose2:
        groups.append(("Inbox", "dim", loose2))
    groups.sort(key=lambda g: 0 if any(t.id == selected_id for t in g[2]) else 1)

    avail = max(1, (height - len(lines) - 1) if height else 12)
    colw = inner // 2
    used = 0
    for gname, gcol, items in groups:
        if used >= avail:
            break
        lines.append(line(c(" ▐ ", gcol)
                          + c(fit(escape(gname), inner - 22), "hd", bold=True)
                          + c(fit(f"{len(items)} tasks", 18, "right"), "mut") + " "))
        used += 1
        ordered = sorted(items, key=lambda t: urgency_key(board, t, today))
        for i in range(0, len(ordered), 2):
            if used >= avail:
                break
            row = ""
            for t in ordered[i:i + 2]:
                d = days_left(t, today)
                chip = ("blk" if t.blocked else
                        ("--" if d is None else (f"{-d}d!" if d < 0 else f"{d}d")))
                g, gt = status_glyph(board, t)
                is_sel = t.id == selected_id
                row += (c(" " + g + " ", gt)
                        + c(fit(escape(t.title), colw - 9),
                            "ink" if is_sel else "mut", bold=is_sel)
                        + c(fit(chip, 6, "right"), "dim"))
                if line_map is not None:
                    line_map[t.id] = len(lines)
            lines.append(line(fit_markup(row, inner)))
            used += 1

    lines.append(bottom(None, w))
    return Text.from_markup("\n".join(fill_height(lines, height, w)))


def fit_markup(markup: str, width: int) -> str:
    """Pad an already-coloured markup string to `width` visible cells."""
    vis = len(V._strip(markup))
    if vis < width:
        return markup + " " * (width - vis)
    return markup


# ==========================================================================
# VARIANT C — FLOW.  affordance: navigate/compare columns, spot flow problems.
# layout: columns WEIGHTED by content.  density: plain text, 3 brightness tiers.
# ==========================================================================
def render_variant_c(board, show_archived, selected_id, today=None,
                     width=68, height=0, line_map=None, presentation="grouped") -> Text:
    today = today or date.today()
    w = V._clamp_width(width)
    inner = w - 2
    tasks = _all_visible(board, show_archived)
    buckets = phase_buckets(board, tasks)
    counts = [len(b) for b in buckets]
    total = max(1, sum(counts))

    lines = [header(c("FLOW", "accent", bold=True),
                    c(" ".join(f"{n}" for n in counts) + "  wip", "mut"), w)]

    # --- the fix for the baseline's fatal flaw: width PROPORTIONAL to content,
    #     with a floor so an empty phase still shows its (informative) emptiness.
    floor = 12
    free = inner - floor * len(counts)
    widths = [floor + (round(free * n / total) if free > 0 else 0) for n in counts]
    widths[-1] += inner - sum(widths)          # absorb rounding into the last col

    hdr = ""
    for ph, n, cw in zip(board.phases, counts, widths):
        load = "" if n == 0 else ("▁▂▃▄▅▆▇█"[min(7, n // 3)])
        hdr += c(fit(f" {ph.upper()[:cw-6]} {n}{load}", cw), "hd", bold=n > 0)
    lines.append(line(fit_markup(hdr, inner)))
    lines.append(_border("├", "─", "┤",
                           {sum(widths[:i]): "┬" for i in range(1, len(widths))}, w))

    cols: list[list[str]] = []
    for ph, bucket, cw in zip(board.phases, buckets, widths):
        cells: list[str] = []
        if not bucket:
            # a real empty state — never a blank cell (tui-design/NAVIGATION.md).
            # Kept short so it survives the narrow width an empty phase earns.
            cells.append(c(fit(" empty", cw), "dim"))
            cells.append(c(fit(" —", cw), "frame"))
        else:
            last_proj = None
            # sort by PROJECT first, then due date — sorting by due alone makes
            # the group header reappear on every change (measured: 6 repeats of
            # the same two projects in one column, ~8 wasted rows).
            def _grp(t):
                p = board.project_by_id(t.project_id)
                return (p.name if p else "￿Inbox",)
            ordered = sorted(sort_by_due(bucket), key=_grp)
            for t in ordered:
                proj = board.project_by_id(t.project_id)
                pn = proj.name if proj else "Inbox"
                if pn != last_proj:                    # group header = bright tier
                    cells.append(c(fit(" " + escape(pn)[: cw - 2], cw),
                                   project_color(board, t), bold=True))
                    last_proj = pn
                sel = t.id == selected_id
                d = days_left(t, today)
                mark = "!" if t.blocked else ("•" if d is not None and d <= 3 else " ")
                txt = fit(f" {mark}{escape(t.title)}", cw)
                cells.append(c(txt, "ink" if sel else "mut", bold=sel))
        cols.append(cells)

    body = (height - len(lines) - 1) if height else max(len(x) for x in cols)
    body = max(1, body)
    for r in range(body):
        row = ""
        for ci, (cells, cw) in enumerate(zip(cols, widths)):
            row += cells[r] if r < len(cells) else " " * cw
        lines.append(line(fit_markup(row, inner)))
    lines.append(bottom({sum(widths[:i]): "┴" for i in range(1, len(widths))}, w))

    if line_map is not None:                    # column-major -> first row of each
        for bucket in buckets:
            for t in bucket:
                line_map.setdefault(t.id, len(lines) - body - 1)
    return Text.from_markup("\n".join(fill_height(lines, height, w)))


# ==========================================================================
# the switcher — a reactive variant key cycled by a binding (PROTOTYPE.md)
# ==========================================================================
VARIANTS = [
    ("0 baseline", None),
    ("A triage", render_variant_a),
    ("B matrix", render_variant_b),
    ("C flow", render_variant_c),
]
_BASELINE = V.render_kanban
_state = {"i": 1}


def _dispatch(board, show_archived, selected_id, today=None,
              width=68, height=0, line_map=None, presentation="grouped"):
    name, fn = VARIANTS[_state["i"] % len(VARIANTS)]
    if fn is None:
        return _BASELINE(board, show_archived, selected_id, today, width, height,
                         line_map, presentation)
    return fn(board, show_archived, selected_id, today, width, height,
              line_map, presentation)


def install() -> None:
    """Point the app's kanban at the variant dispatcher. CALLED, not implicit.

    This ran at import time and that made merely importing this module rewrite
    a function inside the shipping package for the rest of the process. It
    surfaced as 22 unrelated failures in `tests/test_vertical_fill.py` -- green
    when that file ran alone, red once anything had imported this one, with an
    error naming a symbol the app removed. A prototype may replace app
    behaviour for its own runnable demo; it may not do so as a side effect of
    being read.
    """
    V.render_kanban = _dispatch


def build_app():
    install()
    from textual.binding import Binding
    from taskboard.app import TaskboardApp

    class VariantApp(TaskboardApp):
        # Textual resolves CSS_PATH relative to the module defining the class,
        # so a subclass living in prototypes/ would look for the stylesheet
        # there. Pin it to the shipped one.
        CSS_PATH = str(Path(__file__).resolve().parents[1]
                       / "taskboard" / "taskboard.tcss")
        BINDINGS = TaskboardApp.BINDINGS + [
            Binding("V", "cycle_variant", "Variant", priority=True),
        ]

        def on_mount(self) -> None:
            super().on_mount()
            self.view_mode = "kanban"
            self.refresh_view()
            self._announce()

        def _announce(self) -> None:
            name, _ = VARIANTS[_state["i"] % len(VARIANTS)]
            self.notify(f"kanban variant: {name}   (V to cycle)",
                        timeout=2.5)

        def action_cycle_variant(self) -> None:
            _state["i"] = (_state["i"] + 1) % len(VARIANTS)
            self.refresh_view()
            self._announce()

    return VariantApp


if __name__ == "__main__":
    if "--capture" in sys.argv:
        from capture import capture_all      # noqa: E402  (sibling module)
        capture_all()
    else:
        build_app()().run()
