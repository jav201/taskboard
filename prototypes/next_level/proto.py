"""Next-level renderers for the three handoff ideas — variants, not recolours.

Idea 1  KANBAN LANES. Sort/group/collapse shipped in batch-04 reshuffle ONE
        axis (what order inside a column, which group headers). The missing
        second axis is the lane GRID: lanes x phases with real cards in every
        cell. 1A lanes by priority (what is urgent, where is it stuck), 1B
        lanes by project (how is each project flowing — the matrix layout but
        with cards instead of counts).
Idea 2  FOCUS FOLLOW-UP. The shipped board SHOWS pinned tasks; the follow-up
        pass is what you DO there. 2A is a review queue (one task full-size,
        the rest a stale-ordered rail, every action an existing key). 2B is
        the shipped tile grid re-ordered stale-first with a pressure strip —
        the board answers "what is rotting" before "what is pinned".
Idea 3  GLOBAL SEARCH `/`. 3A is a live filter bar: the board re-renders on a
        filtered Board, matches reverse-lit (shown on kanban AND gantt). 3B is
        a jump palette: an overlay on the dimmed board, ranked results,
        enter lands the selection. 3C is context dim: nothing is hidden,
        non-matching cards recede, matches keep full colour.

Everything here composes the REAL views (render_kanban / render_gantt /
_focus_tiles) or the real cell builders (card_cell / _windowed_header) over
the shared synthetic fixture, so the SVGs show what the code would draw.
"""
from __future__ import annotations

import copy
import re
from datetime import date

from rich.cells import cell_len
from rich.markup import escape
from rich.style import Style
from rich.text import Text

from taskboard.models import Board, Task, days_in_phase, parse_iso
from taskboard.views import (
    _focus_attachments, _focus_tiles, _highlight_markup, _strip,
    _windowed_header, c, card_cell, clip, date_chip, distribute, fit, header,
    head_rule, project_color, render_gantt, render_kanban, rule_row,
    status_glyph, to_text, urgency, vis,
)

GROUND = (13, 17, 23)          # prism ground #0d1117 — the dimming target
PANEL = "#161b22"              # prism panel — the overlay's solid ground


# ---------------------------------------------------------------------------
# cell-grid compositor: a rendered view -> addressable cells -> a Text again.
# This is how dimming, match highlighting and overlays stay HONEST renders of
# the real view instead of re-drawn mockups.
# ---------------------------------------------------------------------------
def to_grid(text: Text, w: int, h: int, con) -> list[list[list]]:
    """(char, style) cells, exactly h rows x w cols. Wide glyphs occupy their
    second cell as ("", _CONT) so positions never shift."""
    grid: list[list[list]] = []
    for ln in text.split("\n"):
        row: list[list] = []
        for seg in ln.render(con):
            for ch in seg.text:
                if ch == "\n":
                    continue
                row.append([ch, seg.style])
                for _ in range(cell_len(ch) - 1):
                    row.append(["", _CONT])
        grid.append((row + [[" ", None]] * w)[:w])
    while len(grid) < h:
        grid.append([[" ", None]] * w)
    return grid[:h]


_CONT = Style(dim=True)        # sentinel; continuation cells are never drawn


def grid_text(grid: list[list[list]]) -> Text:
    t = Text()
    for ri, row in enumerate(grid):
        run: list[str] = []
        run_st = None
        for ch, st in row + [["", _CONT]]:   # the sentinel flushes the row
            if st is not run_st:             # style change, or the sentinel
                if run:
                    t.append("".join(run), style=run_st)
                run, run_st = ([], None) if st is _CONT else ([ch], st)
            else:
                run.append(ch)
        if ri < len(grid) - 1:
            t.append("\n")
    return t


def _fade(style: Style | None, k: float) -> Style | None:
    """A colour mixed k toward the ground. Bold/reverse are dropped: receded
    content carries no emphasis."""
    if style is None or style.color is None:
        return style if k > 0.5 else None
    tri = style.color.get_truecolor()
    r = int(GROUND[0] + (tri.red - GROUND[0]) * k)
    g = int(GROUND[1] + (tri.green - GROUND[1]) * k)
    b = int(GROUND[2] + (tri.blue - GROUND[2]) * k)
    return Style(color=f"#{r:02x}{g:02x}{b:02x}")


def dim_grid(grid, k: float = 0.32, rows: set[int] | None = None) -> None:
    """Fade cells toward the ground. `rows` limits the fade to those rows."""
    for ri, row in enumerate(grid):
        if rows is not None and ri not in rows:
            continue
        for cell in row:
            if cell[1] is not _CONT:
                cell[1] = _fade(cell[1], k)


def highlight_grid(grid, query: str, rows: set[int] | None = None) -> None:
    """Reverse-video every case-insensitive occurrence of `query`."""
    q = query.lower()
    if not q:
        return
    for ri, row in enumerate(grid):
        if rows is not None and ri not in rows:
            continue
        s = "".join(ch for ch, _ in row).lower()
        start = 0
        while True:
            i = s.find(q, start)
            if i < 0:
                break
            for j in range(i, min(i + len(q), len(row))):
                ch, st = row[j]
                row[j][1] = (Style.combine([st, Style(reverse=True)])
                             if st else Style(reverse=True))
            start = i + len(q)


def overlay_grid(grid, con, top: int, left: int, rows: list[str],
                 width: int) -> None:
    """Splice a solid panel-ground box of markup rows over the grid."""
    bg = Style(bgcolor=PANEL)
    for i, markup in enumerate(rows):
        cells = to_grid(Text.from_markup(markup, emoji=False), width, 1, con)[0]
        for j in range(width):
            ch, st = cells[j]
            if st is _CONT:
                continue
            st = Style.combine([st, bg]) if st else bg
            grid[top + i][left + j] = [ch, st]


# ---------------------------------------------------------------------------
# search model (shared by the three idea-3 variants)
# ---------------------------------------------------------------------------
def matches(task: Task, board: Board, q: str) -> str | None:
    """Why a task matches, strongest first: title > project > notes."""
    p = board.project_by_id(task.project_id)
    if q in task.title.lower():
        return "title"
    if p is not None and q in p.name.lower():
        return "project"
    if q in (task.notes or "").lower():
        return "notes"
    return None


def filtered_board(board: Board, query: str) -> Board:
    """A shallow Board whose task list is the query's hits — the real views
    render it untouched, which is the whole point of the prototype."""
    q = query.lower()
    proxy = copy.copy(board)
    proxy.tasks = [t for t in board.tasks if matches(t, board, q)]
    keep = {t.project_id for t in proxy.tasks}
    proxy.projects = [p for p in board.projects if p.id in keep]
    return proxy


def filter_bar(query: str, hits: int, total: int, w: int,
               mode: str = "") -> list[str]:
    """The `/` bar: query + cursor left, tally right. A non-default view state
    is NAMED (the repo's own LLR-003.2), so `mode` is shown when set."""
    left = c("/", "accent", bold=True) + " " + escape(query) + c("▌", "accent")
    if mode:
        left += c(f" · {mode}", "mut")
    right = c(f"{hits}/{total} tasks", "mut") + c(" · esc clears", "dim")
    return [header(left, right, w), head_rule(w)]


def search_view(render_fn, board: Board, query: str, today: date,
                w: int, h: int, con, selected_id=None, mode: str = "",
                **kw) -> Text:
    """3A — the real view on the filtered board, bar under its header, every
    match reverse-lit. The view is rendered 2 rows shorter so the bar takes
    real rows from the SAME height budget."""
    proxy = filtered_board(board, query)
    total = len(board.visible_tasks(False))
    hits = len(proxy.visible_tasks(False))
    text = render_fn(proxy, False, selected_id, today=today,
                     width=w, height=h - 2, **kw)
    grid = to_grid(text, w, h - 2, con)
    highlight_grid(grid, query)
    bar = to_grid(Text.from_markup(
        "\n".join(filter_bar(query, hits, total, w, mode)), emoji=False),
        w, 2, con)
    return grid_text([grid[0]] + bar + grid[1:])


def jump_palette(board: Board, query: str, today: date, w: int, h: int,
                 con, selected_id=None) -> Text:
    """3B — the gantt dimmed to a backdrop, a solid overlay with ranked hits.
    The box is frameless like the rest of the app: the panel ground IS the
    container, no border row is spent."""
    text = render_gantt(board, False, selected_id, today=today,
                        width=w, height=h)
    grid = to_grid(text, w, h, con)
    dim_grid(grid)

    q = query.lower()
    hits = [(t, matches(t, board, q)) for t in board.visible_tasks(False)]
    hits = [(t, why) for t, why in hits if why]
    rank = {"title": 0, "project": 1, "notes": 2}
    hits.sort(key=lambda x: rank[x[1]])

    bw = 64
    inner = bw - 2
    tally = f"{len(hits)} matches"
    head = (" " + c("/", "accent", bold=True) + " " + escape(query)
            + c("▌", "accent"))
    head += fit("", max(0, inner - vis(_strip(head)) - vis(tally)))
    head += c(tally, "mut")
    rows = [head, ""]
    for i, (t, why) in enumerate(hits[:7]):
        p = board.project_by_id(t.project_id)
        pcol = p.color if p else "dim"
        due = parse_iso(t.due_date)
        due_s = due.strftime("%b %d") if due else "—"
        row = (c(" ▸ " if i == 0 else "   ", "accent" if i == 0 else "dim")
               + c(escape(fit(t.title, 24)), "ink")
               + " " + c(escape(fit(p.name if p else "Inbox", 11)), pcol)
               + " " + c(fit(t.phase, 7), "mut")
               + " " + c(fit(due_s, 6), "dim")
               + " " + c(why, "dim"))
        row += " " * max(0, inner - vis(_strip(row)))
        if i == 0:
            row = f"[reverse]{row}[/reverse]"
        rows.append(row)
    rows += ["", c(" ↵ jump to card · j/k move · esc close", "dim")]
    overlay_grid(grid, con, 3, (w - bw) // 2, rows, bw)
    return grid_text(grid)


def context_dim(board: Board, query: str, today: date, w: int, h: int, con,
                selected_id=None) -> Text:
    """3C — nothing is hidden: non-matching CARD rows fade, matching rows keep
    full colour and the query is reverse-lit. `line_map` from the real
    renderer names each task's row, so the fade needs no re-layout."""
    proxy_q = query.lower()
    total = len(board.visible_tasks(False))
    hit_ids = {t.id for t in board.visible_tasks(False)
               if matches(t, board, proxy_q)}
    line_map: dict[str, int] = {}
    text = render_kanban(board, False, selected_id, today=today,
                         width=w, height=h - 2, line_map=line_map)
    grid = to_grid(text, w, h - 2, con)
    miss_rows = {ri for tid, ri in line_map.items() if tid not in hit_ids}
    hit_rows = {ri for tid, ri in line_map.items() if tid in hit_ids}
    dim_grid(grid, 0.30, rows=miss_rows)
    highlight_grid(grid, query, rows=hit_rows)
    bar = to_grid(Text.from_markup("\n".join(filter_bar(
        query, len(hit_ids), total, w, "context")), emoji=False), w, 2, con)
    return grid_text([grid[0]] + bar + grid[1:])


# ---------------------------------------------------------------------------
# idea 1 — kanban lanes (the second axis: lanes x phases with real cards)
# ---------------------------------------------------------------------------
def kanban_lanes(board: Board, lanes: list[tuple[str, str, list[Task]]],
                 selected_id, today: date, w: int, h: int,
                 mode_name: str) -> Text:
    """One row-band per lane, one column per phase, card_cell cards per cell.

    Empty lanes are omitted (a header with no cards is a ghost mark — the same
    law kanban_order already follows for groups). A cell that overflows its
    band closes with a `+N` count row, never a clipped card."""
    label_w = 18
    n_ph = len(board.phases)
    sep = c("│", "frame")
    col_ws = distribute(w - label_w - 1 - (n_ph - 1), n_ph)
    junc = {}
    pos = label_w
    junc[pos] = True
    pos += 1
    for wc in col_ws[:-1]:
        pos += wc
        junc[pos] = True
        pos += 1
    crosses = {p: "┼" for p in junc}
    feet = {p: "┴" for p in junc}

    all_tasks = board.visible_tasks(False)
    lines = [header(c("KANBAN", "accent", bold=True)
                    + c(f" · lanes: {mode_name}", "mut"),
                    c(f"{len(all_tasks)} tasks", "mut"), w)]
    lines.append(" " * label_w + sep
                 + sep.join(_windowed_header(board, 0, col_ws, all_tasks)))
    lines.append(rule_row(crosses, w))

    chrome = 3 + 1                     # header + heads + rule + bottom rule
    avail = h - chrome - (len(lanes) - 1)
    lane_h = max(1, avail // max(1, len(lanes)))

    def cell_lines(tasks: list[Task], wc: int) -> list[str]:
        cap = lane_h
        shown = tasks if len(tasks) <= cap else tasks[:cap - 1]
        rows = [card_cell(t, board, wc, t.id == selected_id,
                          prefix="▊ ", prefix_color=project_color(board, t),
                          today=today) for t in shown]
        if len(tasks) > cap:
            rows.append(c(fit(f"+{len(tasks) - cap + 1} more", wc), "dim"))
        rows += [" " * wc] * (lane_h - len(rows))
        return rows[:lane_h]

    for li, (name, color, tasks) in enumerate(lanes):
        buckets = [[] for _ in range(n_ph)]
        idx = {ph: i for i, ph in enumerate(board.phases)}
        for t in tasks:
            buckets[idx.get(t.phase, 0)].append(t)
        cells = [cell_lines(buckets[i], col_ws[i]) for i in range(n_ph)]
        for r in range(lane_h):
            if r == 0:
                label = (c("▐ ", color)
                         + c(escape(fit(name.upper(), label_w - 2)), color,
                             bold=True))
            elif r == 1:
                label = c(fit(f"  {len(tasks)}", label_w), "dim")
            else:
                label = " " * label_w
            lines.append(label + sep + sep.join(cell[r] for cell in cells))
        if li < len(lanes) - 1:
            lines.append(rule_row(crosses, w))
    lines.append(rule_row(feet, w))
    return to_text(lines, h, w)


def priority_lanes(board: Board) -> list[tuple[str, str, list[Task]]]:
    """The shipped group='priority' seat's tones, worn by lanes instead."""
    tasks = board.visible_tasks(False)
    lanes = []
    for value, name, color in (("high", "High", "over"),
                               ("normal", "Normal", "mut"),
                               ("low", "Low", "dim")):
        items = [t for t in tasks if t.priority == value]
        if items:
            lanes.append((name, color, items))
    return lanes


def project_lanes(board: Board) -> list[tuple[str, str, list[Task]]]:
    tasks = board.visible_tasks(False)
    lanes = []
    for p in board.visible_projects(False):
        items = [t for t in tasks if t.project_id == p.id]
        if items:
            lanes.append((p.name, p.color, items))
    inbox = [t for t in tasks if board.project_by_id(t.project_id) is None]
    if inbox:
        lanes.append(("Inbox", "dim", inbox))
    return lanes


# ---------------------------------------------------------------------------
# idea 2 — focus follow-up
# ---------------------------------------------------------------------------
def stale_order(board: Board, tasks: list[Task], today: date) -> list[Task]:
    """Project groups ordered by their STALEST task, tasks stale-first inside
    a group, Inbox last. Unknown stamps (None) sink — never read as zero."""
    def age(t: Task) -> int:
        a = days_in_phase(t, today)
        return a if a is not None else -1

    groups: dict[str | None, list[Task]] = {}
    order: list[str | None] = []
    for p in board.visible_projects(False):
        order.append(p.id)
    order.append(None)
    for t in tasks:
        key = t.project_id if board.project_by_id(t.project_id) else None
        groups.setdefault(key, []).append(t)
    keyed = [(max((age(t) for t in groups[k]), default=-1), k)
             for k in order if groups.get(k)]
    keyed.sort(key=lambda x: (-x[0], x[1] is None))
    out: list[Task] = []
    for _, k in keyed:
        out.extend(sorted(groups[k], key=age, reverse=True))
    return out


def focus_stale(board: Board, tasks: list[Task], selected_id, today: date,
                w: int, h: int) -> Text:
    """2B — the SHIPPED tile grid, re-ordered stale-first, under a pressure
    strip. Overdue wears `over`; sitting wears `soon`. Both are counts of the
    pinned set, so the strip can never disagree with the grid below it."""
    overdue = [t for t in tasks if urgency(t, today, board) == "overdue"]
    stale = [t for t in tasks
             if (days_in_phase(t, today) or 0) >= 7 and not board.is_done(t)]
    lines = [header(c("◆ FOCUS", "accent", bold=True)
                    + c(" · stale first", "mut"),
                    c(f"{len(tasks)} pinned", "mut"), w),
             (c(f"▲ {len(overdue)} overdue", "over")
              + c("    ", "dim")
              + c(f"■ {len(stale)} sitting ≥7d", "soon")
              + c("    ordered by days in phase", "dim"))]
    lines += _focus_tiles(board, stale_order(board, tasks, today),
                          selected_id, today, w, None)
    return to_text(lines, h, w)


def focus_review(board: Board, tasks: list[Task], idx: int, today: date,
                 w: int, h: int) -> Text:
    """2A — the review queue: ONE task full-size left, the rest a rail right.
    Every key on the hint row already exists in the app — nothing here needs
    a new binding, a new field, or a new mode."""
    tasks = stale_order(board, tasks, today)
    if not tasks:
        return to_text([header(c("◆ FOCUS", "accent", bold=True)
                               + c(" · review", "mut"),
                               c("0/0", "mut"), w),
                        c("  (queue empty — pin tasks with 't')", "dim")],
                       h, w)
    idx = max(0, min(idx, len(tasks) - 1))
    t = tasks[idx]
    p = board.project_by_id(t.project_id)
    pcol = p.color if p else "dim"
    pname = p.name if p else "Inbox"

    w_l, gap = 64, 3
    x_rail = w_l + gap
    w_r = w - x_rail
    spine = c("█", pcol)

    left: list[str] = [c("█" * w_l, pcol)]
    left.append(spine + " " + c(escape(fit(t.title, w_l - 3)), "ink",
                                bold=True))
    left.append(spine)
    sg, sgcol = status_glyph(board, t)
    flags = [c(sg, sgcol)]
    if t.priority == "high":
        flags.append(c("high", "over"))
    if t.blocked:
        flags.append(c("blocked", "over"))
    left.append(spine + " " + c(escape(fit(pname, 22)), pcol)
                + "  " + "  ".join(flags))
    dt, dcol = date_chip(t, today, board)
    when = [c(escape(fit(clip(t.phase or "", 16), 16)), "mut"), c(dt, dcol)]
    if t.start_date:
        when.append(c(f"start {t.start_date}", "dim"))
    if t.due_date:
        when.append(c(f"due {t.due_date}", dcol))
    left.append(spine + " " + "  ".join(when))
    left.append(spine)
    note_lines = [ln.strip() for ln in (t.notes or "").splitlines()
                  if ln.strip() and not re.match(r"^\s*[-*]\s+\[", ln)]
    for ln_txt in note_lines[:6]:
        left.append(spine + " " + _highlight_markup(clip(ln_txt, w_l - 3)))
    if not note_lines:
        left.append(spine + " " + c("·", "dim"))
    open_items = [m.group(1).strip()
                  for m in (re.match(r"^\s*[-*]\s+\[ \]\s*(.*)", ln)
                            for ln in (t.notes or "").splitlines()) if m]
    done_n = len(re.findall(r"^\s*[-*]\s+\[[xX]\]",
                            t.notes or "", re.M))
    if open_items or done_n:
        left.append(spine)
        left.append(spine + " "
                    + c(f"☑ {done_n}/{done_n + len(open_items)}", "hd"))
        for item in open_items[:3]:
            left.append(spine + " " + c(escape(clip(item, w_l - 5)), "mut"))
    attach = _focus_attachments(t, w_l - 3)
    if attach:
        left.append(spine)
        left.append(spine + " " + attach)
    while len(left) < h - 4:
        left.append(spine)
    left.append(c(escape("j/k queue · t unpin · [/] phase · ↵ open · esc board"),
                  "dim"))
    left.append(c("━" * w_l, pcol))

    rail: list[str] = [c("QUEUE — stale first", "dim")]
    rail.append("")
    for i, q in enumerate(tasks):
        rail.append(card_cell(q, board, w_r, False,
                              prefix="▸ " if i == idx else "▊ ",
                              prefix_color="accent" if i == idx
                              else project_color(board, q),
                              today=today))

    n_rows = max(len(left), len(rail))

    def pad_m(m: str, width: int) -> str:
        return m + " " * max(0, width - vis(_strip(m)))

    lines = [header(c("◆ FOCUS", "accent", bold=True) + c(" · review", "mut"),
                    c(f"{idx + 1}/{len(tasks)} · stale first", "mut"), w)]
    for r in range(n_rows):
        lft = pad_m(left[r], w_l) if r < len(left) else " " * w_l
        rgt = pad_m(rail[r], w_r) if r < len(rail) else ""
        lines.append(lft + " " * gap + rgt)
    return to_text(lines, h, w)
