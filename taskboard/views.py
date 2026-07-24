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
    "orange": "#fb923c",
    "lime": "#a3e635",
    "cyan": "#22d3ee",
    "blue": "#60a5fa",
    "indigo": "#818cf8",
    "fuchsia": "#e879f9",
    "pink": "#f472b6",
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
def status_glyph(board: Board, task: Task) -> tuple[str, str]:
    if board.is_done(task):
        return ("✓", "done")
    if task.blocked:
        return ("▲", "over")
    if board.phase_index(task) == 0:
        return ("○", "dim")
    return ("◐", "accent")


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
    if allow_priority and task.priority == "high" and not board.is_done(task):
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
def urgency(task: Task, today: date, board: Board) -> str:
    if board.is_done(task):
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


def date_chip(task: Task, today: date, board: Board) -> tuple[str, str]:
    u = urgency(task, today, board)
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
# view: SWIMLANES  (rows = projects + Inbox, cols = the board's phases)
# ---------------------------------------------------------------------------
def phase_buckets(board: Board, tasks: list[Task]) -> list[list[Task]]:
    """One bucket per board phase, in phase order. A blocked task stays in its
    own phase (blocked is a flag, not a column); an unknown phase falls into the
    first bucket. This is THE grouping every view uses."""
    index = {name: i for i, name in enumerate(board.phases)}
    buckets: list[list[Task]] = [[] for _ in board.phases]
    for t in tasks:
        buckets[index.get(t.phase, 0)].append(t)
    return buckets


def _lane_junctions(label_w: int, cols: list[int], mid: str) -> dict[int, str]:
    """Column-separator positions for the swimlane grid (one before each column)."""
    j, pos = {}, label_w
    for wc in cols:
        j[pos] = mid
        pos += 1 + wc
    return j


def render_swimlanes(board, show_archived, selected_id, today=None,
                     width=68, height=0, line_map=None) -> Text:
    today = today or date.today()
    w = _clamp_width(width)
    inner = w - 2
    label_w = max(8, min(14, inner // 5))
    n = len(board.phases)
    cols = distribute(inner - label_w - n, n)

    tasks = board.visible_tasks(show_archived)
    open_n = sum(1 for t in tasks if not board.is_done(t))
    due_n = sum(1 for t in tasks if urgency(t, today, board) in ("overdue", "today"))
    right = c(f"{open_n} open · ", "mut") + c(f"{due_n} due", "over", bold=True)

    lines = [header(c("◆ TASKBOARD", "accent", bold=True), right, w)]
    hdr = fit("", label_w)
    for i, name in enumerate(board.phases):
        hdr += (c("│", "frame")
                + c(escape(fit(name.upper(), cols[i])), "hd", bold=True))
    lines.append(line(hdr))
    lines.append(_border("├", "─", "┤", _lane_junctions(label_w, cols, "┼"), w))

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
            return card_cell(t, board, colw, t.id == selected_id,
                             prefix="▲ " if t.blocked else "", prefix_color="over")
        return fit("", colw)

    def meta(items, colw):
        extra = len(items) - 1
        if extra > 0:
            return c(fit(f"{extra} more", colw), "dim")
        return fit("", colw)

    for name, color, rows in lanes:
        buckets = phase_buckets(board, rows)
        l1 = c("▐ ", color) + c(fit(name, label_w - 2), color)
        for i, bucket in enumerate(buckets):
            l1 += c("│", "frame") + cell(bucket, 0, cols[i])
        lines.append(line(l1))
        if line_map is not None:
            idx = len(lines) - 1
            for bucket in buckets:
                if bucket:
                    line_map[bucket[0].id] = idx
        done_n = len(buckets[-1]) if buckets else 0
        l2 = c("▐ ", color) + progress_bar(done_n, len(rows), label_w - 2, color)
        for i, bucket in enumerate(buckets):
            l2 += c("│", "frame") + meta(bucket, cols[i])
        lines.append(line(l2))

    lines.append(bottom(_lane_junctions(label_w, cols, "┴"), w))
    return Text.from_markup("\n".join(fill_height(lines, height, w)))


# ---------------------------------------------------------------------------
# view: COLUMNS  (one column per board phase, in order)
# ---------------------------------------------------------------------------
def render_columns(board, show_archived, selected_id, today=None,
                   width=68, height=0, line_map=None) -> Text:
    today = today or date.today()
    w = _clamp_width(width)
    inner = w - 2
    n = len(board.phases)
    widths = distribute(inner - (n - 1), n)     # n-1 separators between n columns
    last = n - 1

    def junctions(mid):
        j, pos = {}, 0
        for wc in widths[:-1]:
            pos += wc
            j[pos] = mid
            pos += 1
        return j

    tasks = board.visible_tasks(show_archived)
    due_n = sum(1 for t in tasks if urgency(t, today, board) in ("overdue", "today"))
    right = c(f"▲ {due_n} due", "over", bold=True)
    lines = [header(c("COLUMNS", "accent", bold=True) + c(" · board", "mut"), right, w)]

    buckets = phase_buckets(board, tasks)

    def spark_for(items):
        vals = [0, 0, 0, 0]
        for t in items:
            vals[{"overdue": 0, "today": 1, "week": 2}
                 .get(urgency(t, today, board), 3)] += 1
        return vals

    hdr = []
    for i, name in enumerate(board.phases):
        wc = widths[i]
        items = buckets[i]
        label = name.upper()
        cnt = str(len(items))
        tail = len(cnt) + 1                 # mandatory " " + count
        if wc < tail + 1:                   # not even room for "L cnt"
            hdr.append(escape(fit(f"{label} {cnt}"[:wc], wc)))
            continue
        # optional sparkline needs 1 space + >=1 label char reserved
        spk_w = max(0, min(4, wc - tail - 2)) if wc - tail - 2 >= 0 else 0
        lab_w = max(0, wc - tail - (spk_w + 1 if spk_w > 0 else 0))
        cell = c(escape(fit(label, lab_w)), "hd", bold=True) + " " + c(cnt, "dim")
        if spk_w > 0:
            cell += " " + sparkline(spark_for(items),
                                    "green" if i == last else "accent", spk_w)
        hdr.append(cell)
    lines.append(line(c("│", "frame").join(hdr)))
    lines.append(_border("├", "─", "┤", junctions("┼"), w))

    max_rows = max((len(v) for v in buckets), default=0)
    if max_rows == 0:
        lines.append(line(c(fit("  (no tasks — press 'a' to add one)", inner), "dim")))
    for r in range(max_rows):
        card = []
        for i, wc in enumerate(widths):
            items = buckets[i]
            if r >= len(items):
                card.append(fit("", wc))
                continue
            t = items[r]
            sel = t.id == selected_id
            if i == last:
                card.append(card_cell(t, board, wc, sel, prefix="✓ ",
                                      prefix_color="done", allow_priority=False))
            else:
                card.append(card_cell(t, board, wc, sel, prefix="▊ ",
                                      prefix_color=project_color(board, t)))
        lines.append(line(c("│", "frame").join(card)))
        if line_map is not None:
            idx = len(lines) - 1
            for items in buckets:
                if r < len(items):
                    line_map[items[r].id] = idx
        meta = []
        for i, wc in enumerate(widths):
            items = buckets[i]
            if r >= len(items) or i == last:
                meta.append(fit("", wc))
                continue
            t = items[r]
            p_obj = board.project_by_id(t.project_id)
            pname = p_obj.name if p_obj else "—"
            chip_txt, chip_col = date_chip(t, today, board)
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
                sg, sgcol = status_glyph(board, t)
                row_urg = urgency(t, today, board)
                braille = _URG_BRAILLE[row_urg]
                chip_txt, chip_col = date_chip(t, today, board)
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
BAR_DONE = "⣿"     # 8/8 dots — the completed share of a project's span
BAR_TODO = "⢕"     # 4/8 dots — the remaining share; same family, same height


META_FULL_W = 14        # ' 62% due 28d' — percent AND due figure
META_PCT_W = 6          # ' 62%'         — percent alone
META_FULL_INNER = 90    # below this the timeline needs those cells more


def gantt_meta_geometry(inner: int, glabel_w: int, cell: int) -> tuple[int, bool]:
    """Width of the figures column right of the bars, and whether it carries the
    due figure. The due date is the first thing to go on a narrow terminal: it
    costs ~8 cells, which is more than a whole week column of timeline."""
    full = inner >= META_FULL_INNER
    want = META_FULL_W if full else META_PCT_W
    return min(want, max(0, inner - glabel_w - cell)), full


def gantt_meta(project, progress: float, today: date, width: int,
               with_due: bool = True) -> str:
    """The figures right of a project bar: phase progress %, then the distance to
    the project's OWN due date.

    `progress` is the same number that drove the bar, so the two can never
    disagree. We store no phase-transition timestamps, so a velocity/ETA is not
    computable and must not be invented — 'due Nd' is a due-date figure, not a
    forecast. A project without a due date gets a dim placeholder, no number."""
    if width <= 0:
        return ""
    pct = f"{int(round(100 * progress))}%"
    if not with_due:
        return c(fit(pct, width, "right"), project.color, bold=True)
    d = parse_iso(project.due_date)
    if d is None:
        due, due_col = "—", "dim"
    else:
        delta = (d - today).days
        due, due_col = f"due {delta}d", ("over" if delta < 0 else "mut")
    plain = f"{pct} {due}"
    if len(plain) > width:                      # too tight -> the percent alone
        return c(fit(pct, width, "right"), project.color, bold=True)
    return (" " * (width - len(plain)) + c(pct, project.color, bold=True)
            + " " + c(due, due_col))


def render_gantt(board, show_archived, selected_id, today=None,
                 width=68, height=0, line_map=None) -> Text:
    today = today or date.today()
    w = _clamp_width(width)
    inner = w - 2
    glabel_w = max(18, min(30, inner // 3))
    cell = 6
    meta_w, meta_full = gantt_meta_geometry(inner, glabel_w, cell)
    avail = max(0, inner - glabel_w - meta_w)
    weeks = max(1, min(20, avail // cell)) if avail >= cell else 1
    grid = weeks * cell
    trailing = max(0, inner - glabel_w - meta_w - grid)
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

    def project_bar(s_idx, e_idx, color, progress):
        """ONE continuous bar over the project's span: dense glyphs for the
        completed share, half-density for the rest, both full-cell and in the
        project's colour so the bar keeps a constant height end to end. The
        split comes from the phase weights, not from done/total."""
        if (s_idx is None or e_idx is None or e_idx < s_idx
                or e_idx < 0 or s_idx > weeks - 1):
            return " " * grid
        s = max(0, min(weeks - 1, s_idx))
        e = max(0, min(weeks - 1, e_idx))
        start = s * cell
        bar_width = (e - s + 1) * cell - 1
        filled = max(0, min(bar_width, int(round(progress * bar_width))))
        return (" " * start
                + c(BAR_DONE * filled + BAR_TODO * (bar_width - filled), color)
                + " " * (grid - start - bar_width))

    right = c(f"{weeks}w axis", "mut")
    lines = [header(c("GANTT", "accent", bold=True), right, w)]

    axis = c(fit("", glabel_w), "mut")
    for wk in range(weeks):
        lbl = "W" + (chart_start + timedelta(weeks=wk)).strftime("%V")
        axis += c(fit(lbl, cell), "accent" if wk == 0 else "dim", bold=(wk == 0))
    head_txt = "prog   due" if meta_full else "prog"
    meta_head = (c(fit(head_txt, meta_w, "right"), "mut")
                 if meta_w >= len(head_txt) else " " * meta_w)
    lines.append(line(axis + " " * trailing + meta_head))
    marker = (c(fit("", glabel_w), "dim") + c(fit("▲ today", grid + trailing), "accent")
              + " " * meta_w)
    lines.append(line(marker))

    projects = board.visible_projects(show_archived)
    tasks = board.visible_tasks(show_archived)
    scheduled_any = False
    unscheduled: list[Task] = []

    for i, p in enumerate(projects):
        if i:                                   # a divider BETWEEN project blocks
            lines.append(line(c("┈" * inner, "frame")))
        si, ei = week_index(parse_iso(p.start_date)), week_index(parse_iso(p.due_date))
        if si is not None and ei is not None:
            scheduled_any = True
        prog = board.project_progress(p.id, show_archived)
        lines.append(line(c(escape(fit("▐ " + p.name, glabel_w)), p.color, bold=True)
                          + project_bar(si, ei, p.color, prog)
                          + " " * trailing
                          + gantt_meta(p, prog, today, meta_w, meta_full)))
        for t in [t for t in tasks if t.project_id == p.id]:
            ts = week_index(parse_iso(t.start_date) or parse_iso(t.due_date))
            te = week_index(parse_iso(t.due_date) or parse_iso(t.start_date))
            if ts is None and te is None:
                unscheduled.append(t)
                continue
            scheduled_any = True
            sel = t.id == selected_id
            lines.append(line(c("  ", "dim") + title_markup(t, glabel_w - 3, sel) + " "
                              + bar_cells(ts, te, p.color, "▬") + " " * trailing
                              + " " * meta_w))
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
        lines.append(line(c(escape(fit("▐ " + t.title, glabel_w)), "dim")
                          + bar_cells(ts, te, "dim", "▬") + " " * trailing
                          + " " * meta_w))
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
# view: KANBAN  (one column per phase with EVERY task, grouped by project;
#                `tab` switches to a project x phase matrix)
# ---------------------------------------------------------------------------
MIN_COL = 12        # a phase column narrower than this shows nothing useful


def _phase_window(board: Board, grid: int, selected: Task | None,
                  min_col: int = MIN_COL) -> tuple[int, list[int]]:
    """(start, widths) for the phases that fit in `grid` cells at >= `min_col`.

    `grid` includes the 1-cell separators between columns. When not every phase
    fits, the window follows the selected task's phase so navigating into a
    hidden phase brings it on screen."""
    n = len(board.phases)
    fits = max(1, min(n, (grid + 1) // (min_col + 1)))
    if fits >= n:
        start = 0
    else:
        sel = board.phase_index(selected) if selected is not None else 0
        start = max(0, min(n - fits, sel - (fits - 1) // 2))
    return start, distribute(grid - (fits - 1), fits)


def _windowed_header(board: Board, start: int, widths: list[int]) -> list[str]:
    """Phase-name header cells, with `◀ N` / `N ▶` counts for hidden phases."""
    n, end = len(board.phases), start + len(widths)
    cells = []
    for i, wc in enumerate(widths):
        pre = f"◀ {start} " if (i == 0 and start > 0) else ""
        suf = f" {n - end} ▶" if (i == len(widths) - 1 and end < n) else ""
        avail = wc - len(pre) - len(suf)
        if avail < 1:                       # no room for a label -> markers only
            cells.append(c(fit((pre + suf).strip(), wc), "mut"))
            continue
        cells.append(c(pre, "mut")
                     + c(escape(fit(board.phases[start + i].upper(), avail)), "hd", bold=True)
                     + c(suf, "mut"))
    return cells


def _kanban_groups(board, tasks, show_archived) -> list[tuple[str, str, list[Task]]]:
    """(name, color, tasks) per project that owns any of `tasks`, Inbox last."""
    groups = []
    for p in board.visible_projects(show_archived):
        items = [t for t in tasks if t.project_id == p.id]
        if items:
            groups.append((p.name, p.color, items))
    inbox = [t for t in tasks if board.project_by_id(t.project_id) is None]
    if inbox:
        groups.append(("Inbox", "dim", inbox))
    return groups


def _kanban_column_rows(board, tasks, wc, selected_id,
                        show_archived) -> list[tuple[str, str | None]]:
    """(markup, task-id) rows for ONE phase column: a coloured project header
    followed by EVERY one of that project's tasks in this phase."""
    rows: list[tuple[str, str | None]] = []
    for name, color, items in _kanban_groups(board, tasks, show_archived):
        rows.append((c("▐ ", color) + c(escape(fit(name, max(0, wc - 2))), color, bold=True),
                     None))
        for t in items:
            rows.append((card_cell(t, board, wc, t.id == selected_id,
                                   prefix="▲ " if t.blocked else "▊ ",
                                   prefix_color="over" if t.blocked
                                   else project_color(board, t)), t.id))
    return rows


def _col_junctions(widths: list[int], mid: str) -> dict[int, str]:
    j, pos = {}, 0
    for wc in widths[:-1]:
        pos += wc
        j[pos] = mid
        pos += 1
    return j


def _matrix_junctions(label_w: int, widths: list[int], mid: str) -> dict[int, str]:
    j, pos = {}, label_w
    j[pos] = mid
    pos += 1
    for wc in widths:
        pos += wc
        j[pos] = mid
        pos += 1
    return j


def _kanban_grouped(board, show_archived, selected_id, today, w, height, line_map) -> list[str]:
    inner = w - 2
    tasks = board.visible_tasks(show_archived)
    start, widths = _phase_window(board, inner, board.task_by_id(selected_id))
    buckets = phase_buckets(board, tasks)
    sep = c("│", "frame")

    right = c(f"{len(tasks)} tasks", "mut")
    lines = [header(c("KANBAN", "accent", bold=True) + c(" · grouped", "mut"), right, w)]
    lines.append(line(sep.join(_windowed_header(board, start, widths))))
    lines.append(_border("├", "─", "┤", _col_junctions(widths, "┼"), w))

    cols = [_kanban_column_rows(board, buckets[start + i], wc, selected_id, show_archived)
            for i, wc in enumerate(widths)]
    max_rows = max((len(col) for col in cols), default=0)
    if max_rows == 0:
        lines.append(line(c(fit("  (no tasks — press 'a' to add one)", inner), "dim")))
    for r in range(max_rows):
        lines.append(line(sep.join(col[r][0] if r < len(col) else fit("", widths[i])
                                   for i, col in enumerate(cols))))
        if line_map is not None:
            for col in cols:
                if r < len(col) and col[r][1]:
                    line_map[col[r][1]] = len(lines) - 1
    lines.append(bottom(_col_junctions(widths, "┴"), w))
    return lines


def _kanban_matrix(board, show_archived, selected_id, today, w, height, line_map) -> list[str]:
    inner = w - 2
    tasks = board.visible_tasks(show_archived)
    label_w = max(6, min(14, inner // 5))
    prog_w = 5
    selected = board.task_by_id(selected_id)
    start, widths = _phase_window(board, inner - label_w - prog_w - 2, selected)
    sep = c("│", "frame")

    right = c(f"{len(tasks)} tasks", "mut")
    lines = [header(c("KANBAN", "accent", bold=True) + c(" · matrix", "mut"), right, w)]
    lines.append(line(fit("", label_w) + sep
                      + sep.join(_windowed_header(board, start, widths)) + sep
                      + c(fit("prog", prog_w, "right"), "hd", bold=True)))
    lines.append(_border("├", "─", "┤", _matrix_junctions(label_w, widths, "┼"), w))

    rows: list[tuple[str, str, str | None, list[Task]]] = [
        (p.name, p.color, p.id, [t for t in tasks if t.project_id == p.id])
        for p in board.visible_projects(show_archived)]
    inbox = [t for t in tasks if board.project_by_id(t.project_id) is None]
    if inbox:
        rows.append(("Inbox", "dim", None, inbox))
    if not rows:
        lines.append(line(c(fit("  (no projects — press 'p' to add one)", inner), "dim")))

    for name, color, pid, items in rows:
        buckets = phase_buckets(board, items)
        cells = []
        for i, wc in enumerate(widths):
            bucket = buckets[start + i]
            cells.append(c(fit(" " + ("▊" * len(bucket) if bucket else "·"), wc),
                           color if bucket else "dim"))
        pct = (f"{int(round(100 * board.project_progress(pid, show_archived)))}%"
               if pid else "—")
        lines.append(line(c("▐ ", color) + c(escape(fit(name, label_w - 2)), color, bold=True)
                          + sep + sep.join(cells) + sep
                          + c(fit(pct, prog_w, "right"), "accent" if pid else "dim")))
        if line_map is not None:
            for t in items:
                line_map[t.id] = len(lines) - 1

    lines.append(_border("├", "─", "┤", _matrix_junctions(label_w, widths, "┴"), w))
    if selected is None:
        lines.append(line(c(fit("  (no selection)", inner), "dim")))
    else:
        p_obj = board.project_by_id(selected.project_id)
        tail = (f"{p_obj.name if p_obj else 'Inbox'} · {selected.phase} · "
                f"{board.phase_index(selected) + 1}/{len(board.phases)}")
        avail = max(0, inner - 4)
        tail_w = min(len(tail), avail // 2)
        lines.append(line(" " + c("▲" if selected.blocked else "▊",
                                  "over" if selected.blocked else project_color(board, selected))
                          + " " + title_markup(selected, avail - tail_w, False)
                          + " " + c(escape(fit(tail, tail_w)), "mut")))
    lines.append(bottom(None, w))
    return lines


def render_kanban(board, show_archived, selected_id, today=None,
                  width=68, height=0, line_map=None, presentation="grouped") -> Text:
    today = today or date.today()
    w = _clamp_width(width)
    build = _kanban_matrix if presentation == "matrix" else _kanban_grouped
    lines = build(board, show_archived, selected_id, today, w, height, line_map)
    return Text.from_markup("\n".join(fill_height(lines, height, w)))


# ---------------------------------------------------------------------------
# dispatcher
# ---------------------------------------------------------------------------
RENDERERS = {
    "swimlanes": render_swimlanes,
    "columns": render_columns,
    "agenda": render_agenda,
    "gantt": render_gantt,
    "kanban": render_kanban,
}


def render_view(mode, board, show_archived, selected_id, today=None,
                width=68, height=0, line_map=None, presentation="grouped") -> Text:
    if mode == "kanban":
        return render_kanban(board, show_archived, selected_id, today, width, height,
                             line_map, presentation)
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
        return [[t.id for t in bucket] for bucket in phase_buckets(board, tasks)]

    if mode == "kanban":       # same phase columns, but in project-grouped order
        ordered: list[Task] = []
        for _, _, items in _kanban_groups(board, tasks, show_archived):
            ordered += items
        return [[t.id for t in bucket] for bucket in phase_buckets(board, ordered)]

    if mode == "swimlanes":
        lanes = [[t for t in tasks if t.project_id == p.id]
                 for p in board.visible_projects(show_archived)]
        inbox = [t for t in tasks if board.project_by_id(t.project_id) is None]
        if inbox:
            lanes.append(inbox)
        cols: list[list[str]] = [[] for _ in board.phases]   # one per phase
        for lane in lanes:                      # only the first task of each cell shows
            for i, bucket in enumerate(phase_buckets(board, lane)):
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
