"""Rendering for the four board views.

Each ``render_*`` returns a ``rich.text.Text`` built with markup. All untrusted
text (task titles, urls) is escaped with ``rich.markup.escape`` BEFORE it enters
the markup string (pitfall A1), and only color/link wrappers are added around
already-width-correct plain segments so visible width stays exact.
"""

from __future__ import annotations

from datetime import date

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

WIDTH = 64  # inner width between the frame borders


def c(text: str, key: str, bold: bool = False) -> str:
    """Wrap already-escaped, width-correct text in a palette color."""
    b = "b " if bold else ""
    return f"[{b}{HEX[key]}]{text}[/]"


# ---------------------------------------------------------------------------
# plain-text fitting (width math happens BEFORE escaping / coloring)
# ---------------------------------------------------------------------------
def fit(s: str, width: int, align: str = "left") -> str:
    if len(s) > width:
        return s[: max(0, width - 1)] + "…" if width >= 1 else ""
    pad = width - len(s)
    if align == "right":
        return " " * pad + s
    if align == "center":
        left = pad // 2
        return " " * left + s + " " * (pad - left)
    return s + " " * pad


# ---------------------------------------------------------------------------
# glyphs
# ---------------------------------------------------------------------------
def status_glyph(task: Task) -> tuple[str, str]:
    """(glyph, color-key) for a task's status."""
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
    """Return the url only if it is a safe http(s) link with no markup breakers."""
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
    text = fit(task.title + suffix, width)  # width math on PLAIN text
    body = escape(text)                      # then escape for markup
    if url:
        body = f"[link={url}]{body}[/link]"
    if selected:
        body = f"[reverse]{body}[/reverse]"
    return body


def progress_bar(done: int, total: int, width: int, color: str) -> str:
    if total <= 0:
        return c("░" * width, "dim")
    filled = round(width * done / total)
    filled = max(0, min(width, filled))
    return c("▇" * filled, color) + c("░" * (width - filled), "frame")


_SPARK = "▁▂▃▄▅▆▇█"


def sparkline(values: list[int], color: str) -> str:
    hi = max(values) if values else 0
    if hi <= 0:
        return c("▁" * len(values), "dim")
    out = []
    for v in values:
        if v <= 0:
            out.append("▁")
        else:  # visibility floor: any nonzero -> at least one level up (A8)
            lvl = max(1, round((len(_SPARK) - 1) * v / hi))
            out.append(_SPARK[lvl])
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
    """(text, color-key) short due-date chip."""
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
# frame helpers
# ---------------------------------------------------------------------------
def _border(left: str, fill: str, right: str, junctions: dict[int, str]) -> str:
    chars = [fill] * WIDTH
    for pos, ch in junctions.items():
        if 0 <= pos < WIDTH:
            chars[pos] = ch
    return c(left + "".join(chars) + right, "frame")


def header(title: str, right: str) -> str:
    # Width math uses VISIBLE lengths (markup stripped); total line == WIDTH + 2.
    tvis = len(_strip(title))
    rvis = len(_strip(right))
    dash = (WIDTH + 2) - 8 - tvis - rvis   # 8 = "╭─ " + " " + " " + " ─╮"
    dash = max(1, dash)
    return (
        c("╭─ ", "frame") + title + " " + c("─" * dash, "frame") + " "
        + right + " " + c("─╮", "frame")
    )


def _strip(markup: str) -> str:
    """Visible length of a small markup fragment (tags removed)."""
    import re
    return re.sub(r"\[/?[^\]]*\]", "", markup)


def line(inner_markup: str) -> str:
    return c("│", "frame") + inner_markup + c("│", "frame")


def bottom(junctions: dict[int, str] | None = None) -> str:
    return _border("╰", "─", "╯", junctions or {})


# ---------------------------------------------------------------------------
# view: SWIMLANES  (rows = projects + Inbox, cols = TODO/DOING/DONE)
# ---------------------------------------------------------------------------
LABEL_W = 10
COL_W = 17


def _lane_columns(tasks: list[Task]):
    todo = [t for t in tasks if t.status == "backlog"]
    doing = [t for t in tasks if t.status in ("active", "blocked")]
    done = [t for t in tasks if t.status == "done"]
    return todo, doing, done


def render_swimlanes(board: Board, show_archived: bool, selected_id: str | None,
                     today: date | None = None) -> Text:
    today = today or date.today()
    tasks = board.visible_tasks(show_archived)
    open_n = sum(1 for t in tasks if t.status != "done")
    due_n = sum(1 for t in tasks if urgency(t, today) in ("overdue", "today"))
    right = c(f"{open_n} open · ", "mut") + c(f"{due_n} due", "over", bold=True)

    lines = [header(c("◆ TASKBOARD", "accent", bold=True), right)]
    # column headers
    hdr = (fit("", LABEL_W) + c("│", "frame")
           + c(fit("TODO", COL_W), "hd", bold=True) + c("│", "frame")
           + c(fit("DOING", COL_W), "hd", bold=True) + c("│", "frame")
           + c(fit("DONE", COL_W), "hd", bold=True))
    lines.append(line(hdr))
    junc = {LABEL_W: "┼", LABEL_W + 1 + COL_W: "┼", LABEL_W + 2 + 2 * COL_W: "┼"}
    lines.append(_border("├", "─", "┤", junc))

    # build lane list: each project, then Inbox for standalone tasks
    lanes: list[tuple[str, str, list[Task]]] = []
    for p in board.visible_projects(show_archived):
        rows = [t for t in tasks if t.project_id == p.id]
        lanes.append((p.name, p.color, rows))
    inbox = [t for t in tasks if board.project_by_id(t.project_id) is None]
    if inbox:
        lanes.append(("Inbox", "dim", inbox))

    if not lanes:
        lines.append(line(c(fit("  (no projects — press 'p' to add one)", WIDTH), "dim")))

    for name, color, rows in lanes:
        todo, doing, done = _lane_columns(rows)
        done_n = len(done)
        total_n = len(rows)

        def cell(items, idx):
            if idx < len(items):
                t = items[idx]
                sel = t.id == selected_id
                pr = " ◉" if t.priority == "high" and t.status != "done" else ""
                mark = "▲ " if t.status == "blocked" else ""
                w = COL_W - len(pr) - len(mark)
                body = (c(escape(mark), "over") if mark else "") + title_markup(t, w, sel)
                if pr:
                    body += c(escape(pr), "amber")
                return body
            return c(fit("", COL_W), "dim")

        # line 1: label bar + name, first item of each bucket
        l1 = (c("▐ ", color) + c(fit(name, LABEL_W - 2), color) + c("│", "frame")
              + cell(todo, 0) + c("│", "frame")
              + cell(doing, 0) + c("│", "frame")
              + cell(done, 0))
        lines.append(line(l1))
        # line 2: progress bar + remaining meta
        bar = c("▐ ", color) + progress_bar(done_n, total_n, LABEL_W - 2, color)

        def meta(items, kind):
            extra = len(items) - 1
            if extra > 0:
                return c(fit(f"{extra} more", COL_W), "dim")
            return c(fit("", COL_W), "dim")

        l2 = (bar + c("│", "frame")
              + meta(todo, "todo") + c("│", "frame")
              + meta(doing, "doing") + c("│", "frame")
              + meta(done, "done"))
        lines.append(line(l2))

    lines.append(bottom({LABEL_W: "┴", LABEL_W + 1 + COL_W: "┴",
                         LABEL_W + 2 + 2 * COL_W: "┴"}))
    return Text.from_markup("\n".join(lines))


# ---------------------------------------------------------------------------
# view: COLUMNS  (BACKLOG / ACTIVE / BLOCKED / DONE)
# ---------------------------------------------------------------------------
# widths sum to 61; + 3 column separators = 64 inner (matches the frame)
KCOLS = [("BACKLOG", "backlog", 15), ("ACTIVE", "active", 14),
         ("BLOCKED", "blocked", 14), ("DONE", "done", 18)]


def _kanban_junctions(mid: str) -> dict[int, str]:
    junc, pos = {}, 0
    for _, _, w in KCOLS[:-1]:
        pos += w
        junc[pos] = mid
        pos += 1
    return junc


def render_columns(board: Board, show_archived: bool, selected_id: str | None,
                   today: date | None = None) -> Text:
    today = today or date.today()
    tasks = board.visible_tasks(show_archived)
    due_n = sum(1 for t in tasks if urgency(t, today) in ("overdue", "today"))
    right = c(f"▲ {due_n} due", "over", bold=True)
    lines = [header(c("KANBAN", "accent", bold=True) + c(" · board", "mut"), right)]

    buckets = {key: [t for t in tasks if t.status == key] for _, key, _ in KCOLS}

    # throughput sparkline = how a column's tasks spread across due-buckets
    def spark_for(items):
        vals = [0, 0, 0, 0]
        for t in items:
            u = urgency(t, today)
            vals[{"overdue": 0, "today": 1, "week": 2}.get(u, 3)] += 1
        return vals

    # header row: label + WIP count + sparkline, each cell exactly `w` wide
    hdr_parts = []
    for label, key, w in KCOLS:
        items = buckets[key]
        cnt = str(len(items))
        spk = sparkline(spark_for(items), "green" if key == "done" else "accent")
        avail = max(1, w - 6 - len(cnt))          # 1(sp)+len(cnt)+1(sp)+4(spark)
        cell = (c(fit(label, avail), "hd", bold=True) + " " + c(cnt, "dim") + " " + spk)
        hdr_parts.append(cell)
    lines.append(line(c("│", "frame").join(hdr_parts)))
    lines.append(_border("├", "─", "┤", _kanban_junctions("┼")))

    max_rows = max((len(v) for v in buckets.values()), default=0)
    if max_rows == 0:
        lines.append(line(c(fit("  (no tasks — press 'a' to add one)", WIDTH), "dim")))
    for r in range(max_rows):
        # card row
        card = []
        for label, key, w in KCOLS:
            items = buckets[key]
            if r >= len(items):
                card.append(fit("", w))
                continue
            t = items[r]
            sel = t.id == selected_id
            col = project_color(board, t)
            if key == "done":
                card.append(c("✓ ", "done") + title_markup(t, w - 2, sel))
            else:
                pr = t.priority == "high" and t.status != "done"
                if pr:
                    card.append(c("▊ ", col) + title_markup(t, w - 4, sel)
                                + " " + c("◉", "amber"))
                else:
                    card.append(c("▊ ", col) + title_markup(t, w - 2, sel))
        lines.append(line(c("│", "frame").join(card)))
        # meta row (project + due chip), done column left blank
        meta = []
        for label, key, w in KCOLS:
            items = buckets[key]
            if r >= len(items) or key == "done":
                meta.append(fit("", w))
                continue
            t = items[r]
            p_obj = board.project_by_id(t.project_id)
            pname = p_obj.name if p_obj else "—"
            chip_txt, chip_col = date_chip(t, today)
            avail = max(0, w - 7)                  # 2(sp)+4(pname)+1(sp)+avail
            meta.append(c("  ", "dim") + c(escape(fit(pname, 4)), "dim") + " "
                        + c(escape(fit(chip_txt, avail)), chip_col))
        lines.append(line(c("│", "frame").join(meta)))

    lines.append(bottom(_kanban_junctions("┴")))
    return Text.from_markup("\n".join(lines))


# ---------------------------------------------------------------------------
# view: AGENDA  (grouped by urgency)
# ---------------------------------------------------------------------------
AGENDA_GROUPS = [("OVERDUE", "overdue", "over"), ("TODAY", "today", "soon"),
                 ("THIS WEEK", "week", "mut"), ("LATER", "later", "later"),
                 ("NO DATE", "none", "dim")]


def agenda_bucket(task: Task, today: date) -> str:
    """Which agenda group a task falls in, by DUE DATE (done tasks included)."""
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


def render_agenda(board: Board, show_archived: bool, selected_id: str | None,
                  today: date | None = None) -> Text:
    today = today or date.today()
    tasks = board.visible_tasks(show_archived)
    overdue_n = sum(1 for t in tasks if urgency(t, today) == "overdue")
    today_n = sum(1 for t in tasks if urgency(t, today) == "today")
    right = c(f"▲ {overdue_n} overdue", "over", bold=True) + c(" · ", "mut") + c(f"{today_n} today", "soon")
    lines = [header(c("AGENDA", "accent", bold=True), right)]

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
        dash = WIDTH - len(label)
        lines.append(line(c(label, gcol, bold=(gkey in ("overdue", "today")))
                          + c("─" * max(0, dash), "frame")))
        for t in rows:
            sel = t.id == selected_id
            pcol = project_color(board, t)
            p_obj = board.project_by_id(t.project_id)
            pname = p_obj.name if p_obj else "Inbox"
            sg, sgcol = status_glyph(t)
            row_urg = urgency(t, today)  # done tasks styled 'done', not by date bucket
            braille = _URG_BRAILLE[row_urg]
            chip_txt, chip_col = date_chip(t, today)
            # fixed columns: dot(1) title(24) project(9) glyph(1) braille(3) chip(remainder)
            row = (" " + c("●", pcol) + " "
                   + title_markup(t, 22, sel) + " "
                   + c(fit(escape(pname[:8]), 8), "dim") + " "
                   + c(sg, sgcol) + " " + c(braille, _URG_COLOR[row_urg]) + "  "
                   + c(escape(fit(chip_txt, 12)), chip_col))
            # pad to WIDTH
            plain_len = 1 + 1 + 1 + 22 + 1 + 8 + 1 + 1 + 1 + 3 + 2 + 12
            row += " " * max(0, WIDTH - plain_len)
            lines.append(line(row))

    if not any_rows:
        lines.append(line(c(fit("  (nothing scheduled — press 'a' to add a task)", WIDTH), "dim")))
    lines.append(bottom())
    return Text.from_markup("\n".join(lines))


# ---------------------------------------------------------------------------
# view: GANTT  (weeks as columns; project bars + task bars; today marker)
# ---------------------------------------------------------------------------
GLABEL_W = 16
GWEEKS = 8
GCELL = 6  # chars per week column  -> 8*6 = 48 ; 16 + 48 = 64


def render_gantt(board: Board, show_archived: bool, selected_id: str | None,
                 today: date | None = None) -> Text:
    from datetime import timedelta
    today = today or date.today()
    chart_start = today - timedelta(days=today.weekday())  # Monday of this week

    def week_index(d: date | None) -> int | None:
        if d is None:
            return None
        return (d - chart_start).days // 7

    right = c(f"{GWEEKS}w from today", "mut")
    lines = [header(c("GANTT", "accent", bold=True), right)]

    # axis header: week labels
    axis = fit("", GLABEL_W)
    axis_markup = c(fit("", GLABEL_W), "mut")
    for w in range(GWEEKS):
        wk = (chart_start + timedelta(weeks=w))
        lbl = "W" + wk.strftime("%V")  # ISO week number, zero-padded
        col_col = "accent" if w == 0 else "dim"
        axis_markup += c(fit(lbl, GCELL), col_col, bold=(w == 0))
    lines.append(line(axis_markup))
    # today marker line under W0
    marker = c(fit("", GLABEL_W), "dim") + c("▲ today", "accent") + c(fit("", GWEEKS * GCELL - 7), "dim")
    lines.append(line(marker))

    def bar_cells(s_idx: int | None, e_idx: int | None, color: str, char: str) -> str:
        cells = [" "] * GWEEKS
        if s_idx is not None and e_idx is not None:
            s = max(0, min(GWEEKS - 1, s_idx))
            e = max(0, min(GWEEKS - 1, e_idx))
            if e >= s and e_idx >= 0 and s_idx <= GWEEKS - 1:
                for i in range(s, e + 1):
                    cells[i] = char
        # render each week cell GCELL wide
        out = ""
        for i in range(GWEEKS):
            block = cells[i] * (GCELL - 1) + " " if cells[i] != " " else " " * GCELL
            out += c(block, color) if cells[i] != " " else block
        return out

    projects = board.visible_projects(show_archived)
    tasks = board.visible_tasks(show_archived)
    scheduled_any = False
    unscheduled: list[Task] = []

    for p in projects:
        s_idx = week_index(parse_iso(p.start_date))
        e_idx = week_index(parse_iso(p.due_date))
        if s_idx is None or e_idx is None:
            # project without a range still shows its (dated) tasks
            pass
        else:
            scheduled_any = True
        label = c(fit("▐ " + p.name, GLABEL_W), p.color, bold=True)
        lines.append(line(label + bar_cells(s_idx, e_idx, p.color, "█")))
        for t in [t for t in tasks if t.project_id == p.id]:
            ts = week_index(parse_iso(t.start_date) or parse_iso(t.due_date))
            te = week_index(parse_iso(t.due_date) or parse_iso(t.start_date))
            if ts is None and te is None:
                unscheduled.append(t)
                continue
            scheduled_any = True
            sel = t.id == selected_id
            tl = title_markup(t, GLABEL_W - 3, sel)
            lbl = c("  ", "dim") + tl + " "
            lines.append(line(lbl + bar_cells(ts, te, p.color, "▬")))

    # standalone tasks
    for t in tasks:
        if board.project_by_id(t.project_id) is not None:
            continue
        ts = week_index(parse_iso(t.start_date) or parse_iso(t.due_date))
        te = week_index(parse_iso(t.due_date) or parse_iso(t.start_date))
        if ts is None and te is None:
            unscheduled.append(t)
            continue
        scheduled_any = True
        sel = t.id == selected_id
        lbl = c(fit("▐ " + t.title, GLABEL_W), "dim")
        lines.append(line(lbl + bar_cells(ts, te, "dim", "▬")))

    if not scheduled_any:
        lines.append(line(c(fit("  (nothing dated — add start/due dates)", WIDTH), "dim")))

    if unscheduled:
        lbl = " UNSCHEDULED "
        lines.append(line(c(lbl, "later", bold=True) + c("─" * (WIDTH - len(lbl)), "frame")))
        for t in unscheduled:
            sel = t.id == selected_id
            pcol = project_color(board, t)
            row = " " + c("○", pcol) + " " + title_markup(t, WIDTH - 3, sel)
            lines.append(line(row))

    lines.append(bottom())
    return Text.from_markup("\n".join(lines))


# ---------------------------------------------------------------------------
# dispatcher
# ---------------------------------------------------------------------------
RENDERERS = {
    "swimlanes": render_swimlanes,
    "columns": render_columns,
    "agenda": render_agenda,
    "gantt": render_gantt,
}


def render_view(mode: str, board: Board, show_archived: bool,
                selected_id: str | None, today: date | None = None) -> Text:
    fn = RENDERERS.get(mode, render_swimlanes)
    return fn(board, show_archived, selected_id, today)
