"""Rendering for the four board views — RESPONSIVE to the viewport size.

Each ``render_*`` takes the current ``width`` (total line width in cells) and
``height`` (available rows) and produces box-art that fills that width and, when
the content is shorter than the viewport, fills the height too. Every line of a
given view is padded to exactly ``width`` cells so the widget's content size
tracks the viewport (and box-drawing stays aligned at any size).

All untrusted text (task titles, urls) is escaped with ``rich.markup.escape``
BEFORE it enters the markup string (pitfall A1). Only width-1 glyphs are used so
alignment survives across monospace fonts (M22 ambiguous-glyph trap).
"""

from __future__ import annotations

from datetime import date, timedelta

from rich.markup import escape
from rich.text import Text

from .models import Board, Task, parse_iso

# --- palette (hexes from the approved mockup; all survive rich quantization) --
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
    "over": "#f43f5e",
    "soon": "#fbbf24",
    "later": "#64748b",
    "done": "#3f9c6d",
}

MIN_WIDTH = 24   # below this we render at MIN_WIDTH and let the terminal clip


def c(text: str, key: str, bold: bool = False) -> str:
    """Wrap already-escaped, width-correct text in a palette color."""
    b = "b " if bold else ""
    return f"[{b}{HEX[key]}]{text}[/]"


# ---------------------------------------------------------------------------
# plain-text fitting (width math happens BEFORE escaping / coloring)
# ---------------------------------------------------------------------------
def fit(s: str, width: int, align: str = "left") -> str:
    if width <= 0:
        return ""
    if len(s) > width:
        return s[: width - 1] + "…"
    pad = width - len(s)
    if align == "right":
        return " " * pad + s
    if align == "center":
        left = pad // 2
        return " " * left + s + " " * (pad - left)
    return s + " " * pad


def distribute(total: int, n: int) -> list[int]:
    """Split `total` cells across `n` columns as evenly as possible."""
    if total < 0:
        total = 0
    base, rem = divmod(total, n)
    return [base + (1 if i < rem else 0) for i in range(n)]


# ---------------------------------------------------------------------------
# glyphs
# ---------------------------------------------------------------------------
def status_glyph(task: Task) -> tuple[str, str]:
    return {
        "done": ("✓", "done"),
        "blocked": ("▲", "over"),
        "active": ("◐", "accent"),
        "backlog": ("○", "dim"),
    }.get(task.status, ("○", "dim"))


def project_color(board: Board, task: Task) -> str:
    p = board.project_by_id(task.project_id)
    return p.color if p else "dim"  # standalone tasks are grey


def has_url(task: Task) -> bool:
    return bool(valid_url(task.url))


def valid_url(url: str | None) -> str | None:
    if not url:
        return None
    u = url.strip()
    if not (u.startswith("http://") or u.startswith("https://")):
        return None
    if any(ch in u for ch in " []\n\t"):
        return None
    return u


def title_markup(task: Task, width: int, selected: bool) -> str:
    """A fixed-`width` task-title cell: escaped, optional OSC-8 link, ↗ glyph."""
    url = valid_url(task.url)
    suffix = " ↗" if url else ""
    text = fit(task.title + suffix, width)   # width math on PLAIN text
    body = escape(text)                       # then escape for markup
    if url:
        body = f"[link={url}]{body}[/link]"
    if selected:
        body = f"[reverse]{body}[/reverse]"
    return body


def progress_bar(done: int, total: int, width: int, color: str) -> str:
    if width <= 0:
        return ""
    if total <= 0:
        return c("░" * width, "dim")
    filled = max(0, min(width, round(width * done / total)))
    return c("▇" * filled, color) + c("░" * (width - filled), "frame")


_SPARK = "▁▂▃▄▅▆▇█"


def sparkline(values: list[int], color: str, width: int = 4) -> str:
    vals = values[: max(0, width)]
    if not vals:
        return ""
    hi = max(vals)
    if hi <= 0:
        return c("▁" * len(vals), "dim")
    out = []
    for v in vals:
        if v <= 0:
            out.append("▁")
        else:  # visibility floor: any nonzero -> at least one level up (A8)
            out.append(_SPARK[max(1, round((len(_SPARK) - 1) * v / hi))])
    return c("".join(out), color)


# ---------------------------------------------------------------------------
# urgency
# ---------------------------------------------------------------------------
def urgency(task: Task, today: date) -> str:
    if task.status == "done":
        return "done"
    d = parse_iso(task.due_date)
    if d is None:
        return "none"
    delta = (d - today).days
    if delta < 0:
        return "overdue"
    if delta == 0:
        return "today"
    if delta <= 7:
        return "week"
    return "later"


_URG_COLOR = {"overdue": "over", "today": "soon", "week": "later",
              "later": "later", "none": "dim", "done": "done"}
_URG_BRAILLE = {"overdue": "⣿⣿⣤", "today": "⣿⣿⣿", "week": "⣿⣄⡀",
                "later": "⣀⡀ ", "none": "   ", "done": "⣿⣿⣿"}


def date_chip(task: Task, today: date) -> tuple[str, str]:
    u = urgency(task, today)
    if u == "done":
        return "done", "done"
    d = parse_iso(task.due_date)
    if d is None:
        return "—", "dim"
    label = d.strftime("%b %d").replace(" 0", " ")
    delta = (d - today).days
    if delta < 0:
        return f"{label} {delta}d", "over"
    if delta == 0:
        return f"{label} today", "soon"
    return f"{label} +{delta}d", _URG_COLOR[u]


# ---------------------------------------------------------------------------
# frame helpers (all take the OUTER width `w`)
# ---------------------------------------------------------------------------
def _strip(markup: str) -> str:
    import re
    return re.sub(r"\[/?[^\]]*\]", "", markup)


def header(title: str, right: str, w: int) -> str:
    tvis = len(_strip(title))
    rvis = len(_strip(right))
    dash = w - 8 - tvis - rvis            # 8 = "╭─ " + " " + " " + " ─╮"
    dash = max(1, dash)
    return (c("╭─ ", "frame") + title + " " + c("─" * dash, "frame") + " "
            + right + " " + c("─╮", "frame"))


def line(inner: str, w: int | None = None) -> str:
    return c("│", "frame") + inner + c("│", "frame")


def blank_line(w: int) -> str:
    return line(" " * (w - 2))


def _border(left: str, fill: str, right: str, junctions: dict[int, str], w: int) -> str:
    span = w - 2
    chars = [fill] * span
    for pos, ch in junctions.items():
        if 0 <= pos < span:
            chars[pos] = ch
    return c(left + "".join(chars) + right, "frame")


def bottom(junctions: dict[int, str] | None, w: int) -> str:
    return _border("╰", "─", "╯", junctions or {}, w)


def fill_height(lines: list[str], height: int, w: int) -> list[str]:
    """Pad blank body rows so the frame fills the viewport when content is short."""
    if not height or len(lines) >= height:
        return lines
    pad = height - len(lines)
    return lines[:-1] + [blank_line(w)] * pad + [lines[-1]]


def _clamp_width(width: int) -> int:
    return max(MIN_WIDTH, int(width) if width else MIN_WIDTH)


# ---------------------------------------------------------------------------
# view: SWIMLANES  (rows = projects + Inbox, cols = TODO/DOING/DONE)
# ---------------------------------------------------------------------------
def _lane_columns(tasks: list[Task]):
    todo = [t for t in tasks if t.status == "backlog"]
    doing = [t for t in tasks if t.status in ("active", "blocked")]
    done = [t for t in tasks if t.status == "done"]
    return todo, doing, done


def render_swimlanes(board, show_archived, selected_id, today=None,
                     width=68, height=0) -> Text:
    today = today or date.today()
    w = _clamp_width(width)
    inner = w - 2
    label_w = max(8, min(14, inner // 5))
    c0, c1, c2 = distribute(inner - label_w - 3, 3)

    tasks = board.visible_tasks(show_archived)
    open_n = sum(1 for t in tasks if t.status != "done")
    due_n = sum(1 for t in tasks if urgency(t, today) in ("overdue", "today"))
    right = c(f"{open_n} open · ", "mut") + c(f"{due_n} due", "over", bold=True)

    lines = [header(c("◆ TASKBOARD", "accent", bold=True), right, w)]
    hdr = (fit("", label_w) + c("│", "frame")
           + c(fit("TODO", c0), "hd", bold=True) + c("│", "frame")
           + c(fit("DOING", c1), "hd", bold=True) + c("│", "frame")
           + c(fit("DONE", c2), "hd", bold=True))
    lines.append(line(hdr))
    j = {label_w: "┼", label_w + 1 + c0: "┼", label_w + 2 + c0 + c1: "┼"}
    lines.append(_border("├", "─", "┤", j, w))

    lanes: list[tuple[str, str, list[Task]]] = []
    for p in board.visible_projects(show_archived):
        lanes.append((p.name, p.color, [t for t in tasks if t.project_id == p.id]))
    inbox = [t for t in tasks if board.project_by_id(t.project_id) is None]
    if inbox:
        lanes.append(("Inbox", "dim", inbox))

    if not lanes:
        lines.append(line(c(fit("  (no projects — press 'p' to add one)", inner), "dim")))

    def cell(items, idx, colw):
        if colw <= 0:
            return ""
        if idx < len(items):
            t = items[idx]
            sel = t.id == selected_id
            pr = " ◉" if t.priority == "high" and t.status != "done" else ""
            mark = "▲ " if t.status == "blocked" else ""
            wt = colw - len(pr) - len(mark)
            body = (c(escape(mark), "over") if mark else "") + title_markup(t, wt, sel)
            if pr:
                body += c(escape(pr), "amber")
            return body
        return fit("", colw)

    def meta(items, colw):
        extra = len(items) - 1
        if extra > 0:
            return c(fit(f"{extra} more", colw), "dim")
        return fit("", colw)

    for name, color, rows in lanes:
        todo, doing, done = _lane_columns(rows)
        l1 = (c("▐ ", color) + c(fit(name, label_w - 2), color) + c("│", "frame")
              + cell(todo, 0, c0) + c("│", "frame")
              + cell(doing, 0, c1) + c("│", "frame")
              + cell(done, 0, c2))
        lines.append(line(l1))
        l2 = (c("▐ ", color) + progress_bar(len(done), len(rows), label_w - 2, color)
              + c("│", "frame") + meta(todo, c0) + c("│", "frame")
              + meta(doing, c1) + c("│", "frame") + meta(done, c2))
        lines.append(line(l2))

    jb = {label_w: "┴", label_w + 1 + c0: "┴", label_w + 2 + c0 + c1: "┴"}
    lines.append(bottom(jb, w))
    return Text.from_markup("\n".join(fill_height(lines, height, w)))


# ---------------------------------------------------------------------------
# view: COLUMNS  (BACKLOG / ACTIVE / BLOCKED / DONE)
# ---------------------------------------------------------------------------
KCOLS = [("BACKLOG", "backlog"), ("ACTIVE", "active"),
         ("BLOCKED", "blocked"), ("DONE", "done")]


def render_columns(board, show_archived, selected_id, today=None,
                   width=68, height=0) -> Text:
    today = today or date.today()
    w = _clamp_width(width)
    inner = w - 2
    widths = distribute(inner - 3, 4)     # 3 separators between 4 columns
    cols = [(label, key, widths[i]) for i, (label, key) in enumerate(KCOLS)]

    def junctions(mid):
        j, pos = {}, 0
        for _, _, wc in cols[:-1]:
            pos += wc
            j[pos] = mid
            pos += 1
        return j

    tasks = board.visible_tasks(show_archived)
    due_n = sum(1 for t in tasks if urgency(t, today) in ("overdue", "today"))
    right = c(f"▲ {due_n} due", "over", bold=True)
    lines = [header(c("KANBAN", "accent", bold=True) + c(" · board", "mut"), right, w)]

    buckets = {key: [t for t in tasks if t.status == key] for _, key in KCOLS}

    def spark_for(items):
        vals = [0, 0, 0, 0]
        for t in items:
            vals[{"overdue": 0, "today": 1, "week": 2}.get(urgency(t, today), 3)] += 1
        return vals

    hdr = []
    for label, key, wc in cols:
        items = buckets[key]
        cnt = str(len(items))
        spk_w = max(0, min(4, wc - 4 - len(cnt)))
        if spk_w > 0:
            lab = fit(label, max(1, wc - 2 - len(cnt) - spk_w))
            cell = (c(lab, "hd", bold=True) + " " + c(cnt, "dim") + " "
                    + sparkline(spark_for(items), "green" if key == "done" else "accent", spk_w))
        else:
            lab = fit(label, max(1, wc - 1 - len(cnt)))
            cell = c(lab, "hd", bold=True) + " " + c(cnt, "dim")
        hdr.append(cell)
    lines.append(line(c("│", "frame").join(hdr)))
    lines.append(_border("├", "─", "┤", junctions("┼"), w))

    max_rows = max((len(v) for v in buckets.values()), default=0)
    if max_rows == 0:
        lines.append(line(c(fit("  (no tasks — press 'a' to add one)", inner), "dim")))
    for r in range(max_rows):
        card = []
        for label, key, wc in cols:
            items = buckets[key]
            if r >= len(items):
                card.append(fit("", wc))
                continue
            t = items[r]
            sel = t.id == selected_id
            if key == "done":
                card.append(c("✓ ", "done") + title_markup(t, wc - 2, sel))
            elif t.priority == "high" and t.status != "done":
                card.append(c("▊ ", project_color(board, t))
                            + title_markup(t, wc - 4, sel) + " " + c("◉", "amber"))
            else:
                card.append(c("▊ ", project_color(board, t)) + title_markup(t, wc - 2, sel))
        lines.append(line(c("│", "frame").join(card)))
        meta = []
        for label, key, wc in cols:
            items = buckets[key]
            if r >= len(items) or key == "done":
                meta.append(fit("", wc))
                continue
            t = items[r]
            p_obj = board.project_by_id(t.project_id)
            pname = p_obj.name if p_obj else "—"
            chip_txt, chip_col = date_chip(t, today)
            avail = max(0, wc - 7)
            meta.append(c("  ", "dim") + c(escape(fit(pname, 4)), "dim") + " "
                        + c(escape(fit(chip_txt, avail)), chip_col))
        lines.append(line(c("│", "frame").join(meta)))

    lines.append(bottom(junctions("┴"), w))
    return Text.from_markup("\n".join(fill_height(lines, height, w)))


# ---------------------------------------------------------------------------
# view: AGENDA  (grouped by urgency)
# ---------------------------------------------------------------------------
AGENDA_GROUPS = [("OVERDUE", "overdue", "over"), ("TODAY", "today", "soon"),
                 ("THIS WEEK", "week", "mut"), ("LATER", "later", "later"),
                 ("NO DATE", "none", "dim")]


def agenda_bucket(task: Task, today: date) -> str:
    d = parse_iso(task.due_date)
    if d is None:
        return "none"
    delta = (d - today).days
    if delta < 0:
        return "overdue"
    if delta == 0:
        return "today"
    if delta <= 7:
        return "week"
    return "later"


def render_agenda(board, show_archived, selected_id, today=None,
                  width=68, height=0) -> Text:
    today = today or date.today()
    w = _clamp_width(width)
    inner = w - 2
    title_w = max(6, inner - 32)   # fixed cols: dot/proj/glyph/braille/chip = 32

    tasks = board.visible_tasks(show_archived)
    overdue_n = sum(1 for t in tasks if agenda_bucket(t, today) == "overdue")
    today_n = sum(1 for t in tasks if agenda_bucket(t, today) == "today")
    right = (c(f"▲ {overdue_n} overdue", "over", bold=True) + c(" · ", "mut")
             + c(f"{today_n} today", "soon"))
    lines = [header(c("AGENDA", "accent", bold=True), right, w)]

    by_group: dict[str, list[Task]] = {g[1]: [] for g in AGENDA_GROUPS}
    for t in tasks:
        by_group[agenda_bucket(t, today)].append(t)

    any_rows = False
    for gname, gkey, gcol in AGENDA_GROUPS:
        rows = by_group[gkey]
        if not rows:
            continue
        any_rows = True
        label = f" {gname} "
        lines.append(line(c(label, gcol, bold=(gkey in ("overdue", "today")))
                          + c("─" * max(0, inner - len(label)), "frame")))
        for t in rows:
            sel = t.id == selected_id
            pcol = project_color(board, t)
            p_obj = board.project_by_id(t.project_id)
            pname = p_obj.name if p_obj else "Inbox"
            sg, sgcol = status_glyph(t)
            row_urg = urgency(t, today)
            braille = _URG_BRAILLE[row_urg]
            chip_txt, chip_col = date_chip(t, today)
            row = (" " + c("●", pcol) + " " + title_markup(t, title_w, sel) + " "
                   + c(escape(fit(pname[:8], 8)), "dim") + " "
                   + c(sg, sgcol) + " " + c(braille, _URG_COLOR[row_urg]) + "  "
                   + c(escape(fit(chip_txt, 12)), chip_col))
            lines.append(line(row))

    if not any_rows:
        lines.append(line(c(fit("  (nothing scheduled — press 'a' to add a task)", inner), "dim")))
    lines.append(bottom(None, w))
    return Text.from_markup("\n".join(fill_height(lines, height, w)))


# ---------------------------------------------------------------------------
# view: GANTT  (weeks as columns; project + task bars; today marker)
# ---------------------------------------------------------------------------
def render_gantt(board, show_archived, selected_id, today=None,
                 width=68, height=0) -> Text:
    today = today or date.today()
    w = _clamp_width(width)
    inner = w - 2
    glabel_w = max(10, min(16, inner // 4))
    avail = max(0, inner - glabel_w)
    cell = 6
    weeks = max(1, min(20, avail // cell)) if avail >= cell else 1
    grid = weeks * cell
    trailing = max(0, inner - glabel_w - grid)
    chart_start = today - timedelta(days=today.weekday())   # Monday of this week

    def week_index(d):
        return None if d is None else (d - chart_start).days // 7

    def bar_cells(s_idx, e_idx, color, char):
        active = [False] * weeks
        if s_idx is not None and e_idx is not None:
            s, e = max(0, min(weeks - 1, s_idx)), max(0, min(weeks - 1, e_idx))
            if e >= s and e_idx >= 0 and s_idx <= weeks - 1:
                for i in range(s, e + 1):
                    active[i] = True
        out = ""
        for i in range(weeks):
            out += c(char * (cell - 1) + " ", color) if active[i] else " " * cell
        return out

    right = c(f"{weeks}w axis", "mut")
    lines = [header(c("GANTT", "accent", bold=True), right, w)]

    axis = c(fit("", glabel_w), "mut")
    for wk in range(weeks):
        lbl = "W" + (chart_start + timedelta(weeks=wk)).strftime("%V")
        axis += c(fit(lbl, cell), "accent" if wk == 0 else "dim", bold=(wk == 0))
    lines.append(line(axis + " " * trailing))
    marker = c(fit("", glabel_w), "dim") + c(fit("▲ today", grid + trailing), "accent")
    lines.append(line(marker))

    projects = board.visible_projects(show_archived)
    tasks = board.visible_tasks(show_archived)
    scheduled_any = False
    unscheduled: list[Task] = []

    for p in projects:
        si, ei = week_index(parse_iso(p.start_date)), week_index(parse_iso(p.due_date))
        if si is not None and ei is not None:
            scheduled_any = True
        lines.append(line(c(fit("▐ " + p.name, glabel_w), p.color, bold=True)
                          + bar_cells(si, ei, p.color, "█") + " " * trailing))
        for t in [t for t in tasks if t.project_id == p.id]:
            ts = week_index(parse_iso(t.start_date) or parse_iso(t.due_date))
            te = week_index(parse_iso(t.due_date) or parse_iso(t.start_date))
            if ts is None and te is None:
                unscheduled.append(t)
                continue
            scheduled_any = True
            sel = t.id == selected_id
            lines.append(line(c("  ", "dim") + title_markup(t, glabel_w - 3, sel) + " "
                              + bar_cells(ts, te, p.color, "▬") + " " * trailing))

    for t in tasks:
        if board.project_by_id(t.project_id) is not None:
            continue
        ts = week_index(parse_iso(t.start_date) or parse_iso(t.due_date))
        te = week_index(parse_iso(t.due_date) or parse_iso(t.start_date))
        if ts is None and te is None:
            unscheduled.append(t)
            continue
        scheduled_any = True
        lines.append(line(c(fit("▐ " + t.title, glabel_w), "dim")
                          + bar_cells(ts, te, "dim", "▬") + " " * trailing))

    if not scheduled_any:
        lines.append(line(c(fit("  (nothing dated — add start/due dates)", inner), "dim")))

    if unscheduled:
        lbl = " UNSCHEDULED "
        lines.append(line(c(lbl, "later", bold=True)
                          + c("─" * max(0, inner - len(lbl)), "frame")))
        for t in unscheduled:
            sel = t.id == selected_id
            lines.append(line(" " + c("○", project_color(board, t)) + " "
                              + title_markup(t, inner - 3, sel)))

    lines.append(bottom(None, w))
    return Text.from_markup("\n".join(fill_height(lines, height, w)))


# ---------------------------------------------------------------------------
# dispatcher
# ---------------------------------------------------------------------------
RENDERERS = {
    "swimlanes": render_swimlanes,
    "columns": render_columns,
    "agenda": render_agenda,
    "gantt": render_gantt,
}


def render_view(mode, board, show_archived, selected_id, today=None,
                width=68, height=0) -> Text:
    fn = RENDERERS.get(mode, render_swimlanes)
    return fn(board, show_archived, selected_id, today, width, height)
