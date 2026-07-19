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
        "doing": ("◐", "accent"),
        "backlog": ("○", "dim"),
    }.get(task.status, ("○", "dim"))


def project_color(board: Board, task: Task) -> str:
    p = board.project_by_id(task.project_id)
    return p.color if p else "dim"  # standalone tasks are grey


def first_valid_url(task: Task) -> str | None:
    """The first URL that passes ``valid_url`` (the OSC-8 link target), else None."""
    for u in task.urls:
        v = valid_url(u)
        if v:
            return v
    return None


def has_url(task: Task) -> bool:
    return first_valid_url(task) is not None


def valid_url(url: str | None) -> str | None:
    if not url:
        return None
    u = url.strip()
    if not (u.startswith("http://") or u.startswith("https://")):
        return None
    if any(ch in u for ch in " []\n\t"):
        return None
    return u


def title_markup(task: Task, width: int, selected: bool, arrow: bool = True) -> str:
    """A fixed-`width` task-title cell: escaped, optional OSC-8 link, ↗ glyph.

    `arrow=False` omits the inline ↗ (used where ↗ is drawn as a separate,
    space-reserved right indicator so it can never collide with the title)."""
    url = first_valid_url(task)          # OSC-8 target = the FIRST valid URL (F6)
    suffix = " ↗" if (url and arrow) else ""
    text = fit(task.title + suffix, width)   # width math on PLAIN text
    body = escape(text)                       # then escape for markup
    if url:
        body = f"[link={url}]{body}[/link]"
    if selected:
        body = f"[reverse]{body}[/reverse]"
    return body


def _fit_indicators(tokens: list[tuple[str, str]], budget: int) -> tuple[str, int]:
    """Right-aligned indicator glyphs, each rendered as ' <glyph>' (2 cells).

    Keeps as many as fit within `budget`, dropping from the LEFT (so the
    rightmost/most-important marker survives when space is tight). Returns
    (markup, used_width). `tokens` is [(glyph, color_key), ...]."""
    kept: list[tuple[str, str]] = []
    cost = 0
    for glyph, col in reversed(tokens):
        if cost + 2 <= budget:
            kept.insert(0, (glyph, col))
            cost += 2
        else:
            break
    markup = "".join(c(" " + g, col) for g, col in kept)
    return markup, cost


def card_cell(task: Task, board: Board, wc: int, selected: bool, *,
              prefix: str = "", prefix_color: str = "mut",
              allow_priority: bool = True) -> str:
    """A width-exact card: `prefix` + truncated title + right indicators (↗ ◉).

    Title is truncated with … so it can NEVER share a cell with the trailing
    indicators, at any width down to 0. Always returns exactly `wc` cells."""
    if wc <= 0:
        return ""
    if wc < len(prefix):
        return c(fit(prefix, wc), prefix_color)
    tokens: list[tuple[str, str]] = []
    if has_url(task):
        tokens.append(("↗", "accent"))
    if allow_priority and task.priority == "high" and task.status != "done":
        tokens.append(("◉", "amber"))
    if task.images:
        tokens.append(("▤", "sky"))     # width-1 image indicator, distinct from ↗/◉
    ind_markup, used = _fit_indicators(tokens, wc - len(prefix))
    title_w = max(0, wc - len(prefix) - used)
    pre = c(prefix, prefix_color) if prefix else ""
    return pre + title_markup(task, title_w, selected, arrow=False) + ind_markup


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
    if dash < 1:                          # too tight -> drop the right content
        right, rvis = "", 0
        dash = w - 8 - tvis
    if dash < 1:                          # still tight -> truncate the title itself
        plain = fit(_strip(title), max(0, w - 6))
        dash2 = max(0, w - 6 - len(plain))
        return (c("╭─ ", "frame") + c(plain, "accent", bold=True) + " "
                + c("─" * dash2, "frame") + c("─╮", "frame"))
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
    doing = [t for t in tasks if t.status in ("doing", "blocked")]
    done = [t for t in tasks if t.status == "done"]
    return todo, doing, done


def render_swimlanes(board, show_archived, selected_id, today=None,
                     width=68, height=0, line_map=None) -> Text:
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
            blocked = t.status == "blocked"
            return card_cell(t, board, colw, t.id == selected_id,
                             prefix="▲ " if blocked else "", prefix_color="over")
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
        if line_map is not None:
            idx = len(lines) - 1
            for bucket in (todo, doing, done):
                if bucket:
                    line_map[bucket[0].id] = idx
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
KCOLS = [("BACKLOG", "backlog"), ("DOING", "doing"),
         ("BLOCKED", "blocked"), ("DONE", "done")]


def render_columns(board, show_archived, selected_id, today=None,
                   width=68, height=0, line_map=None) -> Text:
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
        tail = len(cnt) + 1                 # mandatory " " + count
        if wc < tail + 1:                   # not even room for "L cnt"
            hdr.append(fit(f"{label} {cnt}"[:wc], wc))
            continue
        # optional sparkline needs 1 space + >=1 label char reserved
        spk_w = max(0, min(4, wc - tail - 2)) if wc - tail - 2 >= 0 else 0
        lab_w = max(0, wc - tail - (spk_w + 1 if spk_w > 0 else 0))
        cell = c(fit(label, lab_w), "hd", bold=True) + " " + c(cnt, "dim")
        if spk_w > 0:
            cell += " " + sparkline(spark_for(items),
                                    "green" if key == "done" else "accent", spk_w)
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
                card.append(card_cell(t, board, wc, sel, prefix="✓ ",
                                      prefix_color="done", allow_priority=False))
            else:
                card.append(card_cell(t, board, wc, sel, prefix="▊ ",
                                      prefix_color=project_color(board, t)))
        lines.append(line(c("│", "frame").join(card)))
        if line_map is not None:
            idx = len(lines) - 1
            for _, key, wc in cols:
                items = buckets[key]
                if r < len(items):
                    line_map[items[r].id] = idx
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
            # width-exact: 2 lead spaces + pname(<=4) + gap + chip, all within wc
            lead = min(2, wc)
            remain = wc - lead
            pname_w = min(4, remain)
            gap = 1 if remain - pname_w >= 1 else 0
            chip_w = max(0, remain - pname_w - gap)
            meta.append(c(" " * lead, "dim") + c(escape(fit(pname, pname_w)), "dim")
                        + (" " if gap else "")
                        + c(escape(fit(chip_txt, chip_w)), chip_col))
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
                  width=68, height=0, line_map=None) -> Text:
    today = today or date.today()
    w = _clamp_width(width)
    inner = w - 2
    # full row has fixed cols (dot/proj/glyph/braille/chip = 32); when there's
    # not enough width for a usable title, fall back to a compact dot+title row.
    title_w = inner - 32
    compact = title_w < 6

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
            if compact:                      # narrow: dot + title only (width-exact)
                row = " " + c("●", pcol) + " " + title_markup(t, inner - 3, sel)
            else:
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
            if line_map is not None:
                line_map[t.id] = len(lines) - 1

    if not any_rows:
        lines.append(line(c(fit("  (nothing scheduled — press 'a' to add a task)", inner), "dim")))
    lines.append(bottom(None, w))
    return Text.from_markup("\n".join(fill_height(lines, height, w)))


# ---------------------------------------------------------------------------
# view: GANTT  (weeks as columns; project + task bars; today marker)
# ---------------------------------------------------------------------------
def render_gantt(board, show_archived, selected_id, today=None,
                 width=68, height=0, line_map=None) -> Text:
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
            if line_map is not None:
                line_map[t.id] = len(lines) - 1

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
        if line_map is not None:
            line_map[t.id] = len(lines) - 1

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
            if line_map is not None:
                line_map[t.id] = len(lines) - 1

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
                width=68, height=0, line_map=None) -> Text:
    fn = RENDERERS.get(mode, render_swimlanes)
    return fn(board, show_archived, selected_id, today, width, height, line_map)


# ---------------------------------------------------------------------------
# navigation model — the ON-SCREEN order of each view, so cursor moves follow
# what the user sees (never board/data order). Returns a list of columns; each
# column is an ordered list of task-ids. Linear views return a single column.
# ---------------------------------------------------------------------------
def _is_dated(task: Task) -> bool:
    return (parse_iso(task.start_date) or parse_iso(task.due_date)) is not None


def nav_model(mode, board, show_archived, today=None) -> list[list[str]]:
    today = today or date.today()
    tasks = board.visible_tasks(show_archived)

    if mode == "columns":
        return [[t.id for t in tasks if t.status == key] for _, key in KCOLS]

    if mode == "swimlanes":
        lanes = [[t for t in tasks if t.project_id == p.id]
                 for p in board.visible_projects(show_archived)]
        inbox = [t for t in tasks if board.project_by_id(t.project_id) is None]
        if inbox:
            lanes.append(inbox)
        cols: list[list[str]] = [[], [], []]   # TODO / DOING / DONE
        for lane in lanes:                      # only the first task of each cell shows
            for i, bucket in enumerate(_lane_columns(lane)):
                if bucket:
                    cols[i].append(bucket[0].id)
        return cols

    if mode == "agenda":
        by = {g[1]: [] for g in AGENDA_GROUPS}
        for t in tasks:
            by[agenda_bucket(t, today)].append(t)
        order: list[str] = []
        for _, gkey, _ in AGENDA_GROUPS:
            order += [t.id for t in by[gkey]]
        return [order]

    if mode == "gantt":
        order, unscheduled = [], []
        for p in board.visible_projects(show_archived):
            for t in [t for t in tasks if t.project_id == p.id]:
                (order if _is_dated(t) else unscheduled).append(t.id)
        for t in tasks:
            if board.project_by_id(t.project_id) is not None:
                continue
            (order if _is_dated(t) else unscheduled).append(t.id)
        return [order + unscheduled]

    return [[t.id for t in tasks]]
