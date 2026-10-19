"""PROTOTYPE renderers for Present view 3 `all` — every shown project on one
date ruler (throwaway; nothing under taskboard/ is edited).

    A  stacked   — a header row per shown project, then its shown open tasks;
                   when rows run out, the projects furthest from the cursor fold
                   to their header
    B  summary   — ONE span row per shown project (its tasks' dues as ticks on
                   the span); only the projects the presenter unfolds (enter)
                   show their tasks
    C  rail      — a left rail lists every project in order (● shown, ○ hidden,
                   position number); the timeline on the right is A's, and it
                   is what `x` exports (the rail never is)

Shared by all three: ONE axis fitted to the open work of every SHOWN project
(`gantt_axis`, the window rule of `gantt_window`), the present ruler (today in
the month label, the cursor's exact dates echoed on the tick row), start-end
chips, project hues. Reused unchanged from taskboard.views: `gantt_axis`,
`gantt_month_row`, `gantt_day_row`, `gantt_echo`, `_gantt_tick_label`,
`_gantt_span`, `_gantt_bar` (via `_present_task_row`), `_present_field`,
`_present_chip`, `_present_due`, `gantt_milestone_cells`, `gantt_dep_mark`,
`present_tasks`, `present_hidden`, `header`, `_present_finish`.

Project presentation state lives in `Project.extra` for the prototype:
`show_in_present` (False hides) and `present_rank` (int, the presentation's
own order). A real build would make both model fields."""
from __future__ import annotations

from datetime import timedelta
from types import SimpleNamespace

from taskboard import views as V
from taskboard.models import critical_chain, parse_iso
from taskboard.views import (FIELD_REACH, HEX, _pad, _strip, c, escape, fit, header, vis)

VARIANTS = ("A", "B", "C")
NAMES = {"A": "stacked", "B": "summary", "C": "rail"}
TICK = "▪"                      # B: a task's due on its project's summary span


# --------------------------------------------------------------------------- #
# project state (prototyped in Project.extra)
# --------------------------------------------------------------------------- #
def shown(p) -> bool:
    return p.extra.get("show_in_present", True) is not False


def ordered(board) -> list:
    """Every visible project in the PRESENTATION's order: `present_rank` first,
    board order for the unranked (and as the tie-break)."""
    ps = board.visible_projects(False)
    idx = {p.id: i for i, p in enumerate(ps)}
    return sorted(ps, key=lambda p: (p.extra.get("present_rank", 10 ** 6), idx[p.id]))


def set_order(board, ids: list[str]) -> None:
    for i, pid in enumerate(ids):
        board.project_by_id(pid).extra["present_rank"] = i


def hidden_counts(board) -> tuple[int, int]:
    ps = board.visible_projects(False)
    np_ = sum(1 for p in ps if not shown(p))
    nt = sum(len(V.present_hidden(board, p.id)) for p in ps if shown(p))
    return np_, nt


# --------------------------------------------------------------------------- #
# geometry
# --------------------------------------------------------------------------- #
def _plan(board):
    """(project, shown open tasks) for every shown project, in order."""
    return [(p, V.present_tasks(board, p.id)[0]) for p in ordered(board) if shown(p)]


def _axis(board, plan, field_w, today):
    """`gantt_window`'s rule over the shown projects only."""
    open_t = [t for _, ts in plan for t in ts]
    dues = [d for t in open_t if (d := parse_iso(t.due_date))]
    starts = [d for t in open_t if (d := parse_iso(t.start_date))]
    pdues = [d for p, ts in plan if ts and (d := parse_iso(p.due_date))]
    m = timedelta(days=V.GANTT_MARGIN)
    lo = min(dues + [today]) - m
    hi = max(dues + pdues + [today]) + m
    return V.gantt_axis(field_w, today, lo, hi, min(starts + [lo]))


class Geo(SimpleNamespace):
    pass


def geo(board, width, today):
    plan = _plan(board)
    wide = width >= 100
    label_w, chip_w, field_w = V._present_cols(width, wide)
    ax = _axis(board, plan, field_w, today)
    return Geo(plan=plan, width=width, wide=wide, label_w=label_w, chip_w=chip_w,
               field_w=field_w, ax=ax, chain=set(critical_chain(board)), today=today)


def _pgeo(g, hue):
    return V._PresentGeo(g.width, g.label_w, g.chip_w, g.field_w, g.ax, g.chain,
                         g.today, g.wide, hue)


# --------------------------------------------------------------------------- #
# rows
# --------------------------------------------------------------------------- #
def _late(ts, today):
    return sum(1 for t in ts if (d := parse_iso(t.due_date)) and d < today)


def _label(p, ts, g, on, caret):
    """`▾ ■ Name   5 open ▲2 in 18d` — the bits the label has room for, shed
    right to left (the gantt group label's rule)."""
    hue = p.color
    late = _late(ts, g.today)
    due, dtone = V._present_due(parse_iso(p.due_date), g.today)
    # (text, tone, shed order): the countdown goes first, the open count next,
    # the late count last — it is the one a presenter must not lose
    bits = [(f"{len(ts)} open" if g.wide else f"{len(ts)}", "mut", 1)]
    if late:
        bits.append((f"▲{late}", "over", 2))
    if g.wide:
        bits.append((due, dtone, 0))
    lead = 4                                       # "▾ ■ "
    want = min(vis(p.name), 16)                    # the name keeps 16 cells first
    while bits and g.label_w - lead - vis(" ".join(b[0] for b in bits)) - 2 < want:
        bits.remove(min(bits, key=lambda b: b[2]))
    bits = [(t, k) for t, k, _ in bits]
    plain = " ".join(t for t, _ in bits)
    name_w = g.label_w - lead - vis(plain) - (2 if bits else 1)
    tone = "accent" if on else hue
    head = (c("⟦", "accent", bold=True) if on else c(caret, hue)) + " " + c("■", hue) + " "
    body = c(escape(fit(p.name, max(0, name_w))), tone, bold=True)
    tail = (" " + " ".join(c(t, k) for t, k in bits)) if bits else ""
    return _pad(head + body + tail, g.label_w)


def _echo_span(cells, on):
    if not on:
        return cells
    lo = next((x for x, (gl, _) in enumerate(cells) if gl != " "), None)
    hi = next((x for x in range(len(cells) - 1, -1, -1) if cells[x][0] != " "), None)
    if lo is None:
        return cells
    out = list(cells)
    for x in range(lo, hi + 1):
        out[x] = ("━", "accent")
    out[lo], out[hi] = ("⟦", "accent"), ("⟧", "accent")
    return out


def head_row(board, p, ts, g, on, folded, ticks=False):
    cells = V._gantt_span(p, g.ax, board.project_progress(p.id), 0)
    if ticks:                          # B: the ticks stay under the cursor
        cells = _ticks(board, cells, ts, g)
    else:
        cells = _echo_span(cells, on)
    chip = " " + V._present_chip(p.start_date, p.due_date, g.today, g.chip_w)
    return _pad(_label(p, ts, g, on, "▸" if folded else "▾") + " "
                + V._present_field(cells, g.ax) + chip, g.width)


def _ticks(board, cells, ts, g):
    """B's summary: every shown open task's due on its project's span — `◆` a
    milestone, `▪` any other task, `over` when late, else its priority hue; the
    project's own `◆` due and `●` progress are never covered."""
    out = list(cells)
    rank = {"over": 3, "rose": 2, "sky": 1, "mut": 0}
    for t in ts:
        d = parse_iso(t.due_date)
        if d is None:
            continue
        x = g.ax.cell(d)
        if not 0 <= x < g.ax.w:
            continue
        if out[x][0] in ("◆", V.PROGRESS_DOT) and out[x][1] != "over" and not t.milestone:
            continue
        tone = "over" if d < g.today else (V.milestone_tone(t, board, g.today) if t.milestone
                                           else V._priority_hue(t.priority))
        glyph = "◆" if t.milestone else TICK
        prev = out[x]
        if prev[0] in ("◆", TICK) and rank.get(prev[1], 1) > rank.get(tone, 1):
            continue
        out[x] = (glyph, tone)
    return out


def task_row(board, t, p, g, on):
    pg = _pgeo(g, p.color)
    if not t.milestone:
        return V._present_task_row(t, board, pg, cursor=on)
    tone = V.milestone_tone(t, board, g.today)
    cells = V.gantt_milestone_cells(t, board, g.ax, g.today, tone)
    if on:
        cells = [("◆", "accent") if gl == "◆" else (gl, tn) for gl, tn in cells]
    ttl = (c("⟦", "accent", bold=True) if on else " ")
    label = (" " + ttl + c("▎", p.color) + " " + c("◆", tone) + " "
             + V._present_title(t, g.label_w - 6))
    gut = V.gantt_dep_mark(t, board, g.chain)
    chip = " " + V._present_chip(None, t.due_date, g.today, g.chip_w)
    return _pad(_pad(label, g.label_w) + gut + V._present_field(cells, g.ax) + chip, g.width)


def ruler(board, g, cursor):
    """The present ruler for the whole portfolio: the month row marks the
    cursor's project due `◆`; the tick row echoes the cursor's exact dates — a
    task's (`_gantt_tick_label`, the shipped rule) or, on a header, its
    project's span (`project span ▸`, new)."""
    ax, today = g.ax, g.today
    kind, obj, proj = cursor if cursor else (None, None, None)
    marks = {}
    if proj is not None and (pd := parse_iso(proj.due_date)) and 0 <= ax.cell(pd) < ax.w:
        marks[ax.cell(pd)] = ("◆", proj.color)
    if kind == "task":
        echo = V.gantt_echo(obj, board, ax, today)
    elif kind == "proj":
        echo = V.gantt_echo(SimpleNamespace(start_date=obj.start_date, due_date=obj.due_date,
                                            phase="", archived=False), board, ax, today)
    else:
        echo = None
    mcells = V.gantt_month_row(ax, today, marks)
    dcells, meta = V.gantt_day_row(ax, today, echo, shade_weekends=False)
    mlabel = c(fit(f"today {today:%a} {V._md(today)}", g.label_w - 1, "right") + " ", "accent")
    if kind == "task":
        dlabel = V._gantt_tick_label(obj, echo, meta, g.label_w)
    elif kind == "proj":
        txt = (meta["echo_label"] or "project span") + " ▸" if echo else "project: no dates"
        dlabel = c(fit(txt, g.label_w - 1, "right") + " ", echo[1] if echo else "dim",
                   bold=echo is not None)
    else:
        dlabel = ""
    tail = " " * (g.chip_w + 1)
    return [_pad(_pad(mlabel, g.label_w) + " " + "".join(mcells) + tail, g.width),
            _pad(_pad(dlabel, g.label_w) + " " + "".join(dcells) + tail, g.width)]


def head(board, g, variant):
    open_t = [t for _, ts in g.plan for t in ts]
    late = _late(open_t, g.today)
    title = (c("◆ PRESENT", "bright", bold=True) + c(" · ", "dim")
             + c(f"{len(g.plan)} projects", "bright", bold=True) + c("  all", "reached"))
    right = c(f"{len(open_t)} open", "mut") + c(" · ", "dim") \
        + (c(f"▲{late} past due", "over", bold=True) if late else c("nothing past due", "dim"))
    return header(title, right, g.width)


# --------------------------------------------------------------------------- #
# the timeline (A, C) and the summary (B)
# --------------------------------------------------------------------------- #
def _resolve(board, cur):
    """Cursor key -> (kind, object, project)."""
    if cur is None:
        return None
    kind, oid = cur
    if kind == "proj":
        p = board.project_by_id(oid)
        return ("proj", p, p) if p else None
    t = board.task_by_id(oid)
    return ("task", t, board.project_by_id(t.project_id)) if t else None


def layout(board, g, variant, cur, folded, unfolded, height):
    """Which projects draw their tasks, and the nav stops in screen order.
    A/C: unfolded unless folded by hand (enter); B: folded unless unfolded by
    hand. Then, while the rows overflow, the projects furthest from the cursor's
    fold to their header (the cursor's own never)."""
    body = height - 3
    plan = g.plan
    cur_pid = None
    if cur is not None:
        r = _resolve(board, cur)
        cur_pid = r[2].id if r else None
    open_ = {p.id: (p.id not in folded) if variant != "B" else (p.id in unfolded)
             for p, _ in plan}
    ci = next((i for i, (p, _) in enumerate(plan) if p.id == cur_pid), 0)

    def need(gap):
        return sum(1 + (len(ts) if open_[p.id] else 0) for p, ts in plan) + (
            len(plan) - 1 if gap else 0)

    auto = set()
    for i in sorted(range(len(plan)), key=lambda i: (-abs(i - ci), -i)):
        if need(False) <= body:
            break
        p = plan[i][0]
        if p.id != cur_pid and open_[p.id] and plan[i][1]:
            open_[p.id] = False
            auto.add(p.id)
    gap = need(True) <= body - (1 if variant == "B" else 0)
    nav = []
    for p, ts in plan:
        nav.append(("proj", p.id))
        if open_[p.id]:
            nav += [("task", t.id) for t in ts]
    return open_, auto, gap, nav


def timeline_lines(board, width, height, today, variant, cur, folded, unfolded,
                   rail=False):
    g = geo(board, width, today)
    open_, auto, gap, nav = layout(board, g, variant, cur, folded, unfolded, height)
    if rail and cur not in nav:        # C, rail focus on a hidden project
        cur = None
    elif cur not in nav:                 # a task folded away: its project header
        r = _resolve(board, cur)
        cur = ("proj", r[2].id) if r and ("proj", r[2].id) in nav else (nav[0] if nav else None)
    rc = _resolve(board, cur)
    lines = [head(board, g, variant)] + ruler(board, g, rc)
    for i, (p, ts) in enumerate(g.plan):
        if gap and i:
            lines.append(" " * width)
        lines.append(head_row(board, p, ts, g, cur == ("proj", p.id), not open_[p.id],
                              ticks=variant == "B"))
        if open_[p.id]:
            lines += [task_row(board, t, p, g, cur == ("task", t.id)) for t in ts]
    if variant == "B" and len(lines) < height:
        lines += [" " * width] * (height - 1 - len(lines))
        lines.append(_legend(width))
    return lines, nav, cur


def _legend(width):
    items = [(TICK, "sky", "task due"), ("◆", "mut", "milestone"), ("▪", "over", "late"),
             ("●", "mut", "progress"), ("◆", "violet", "project due")]
    out = " " + c(" · ", "dim").join(c(gl, k) + " " + c(t, "dim") for gl, k, t in items)
    while vis(_strip(out)) > width and items:
        items = items[:-1]
        out = " " + c(" · ", "dim").join(c(gl, k) + " " + c(t, "dim") for gl, k, t in items)
    return _pad(out, width)


def _fit_lines(lines, height, width):
    """`_present_finish`'s overflow rule, kept as rows (for the rail join)."""
    if len(lines) > height:
        over = len(lines) - height
        lines = lines[:height - 1] + [
            _pad(c(escape(fit(f"  +{over} more rows not shown", width)), "dim"), width)]
    return lines + [" " * width] * (height - len(lines))


# --------------------------------------------------------------------------- #
# C — the rail
# --------------------------------------------------------------------------- #
def rail_w(width):
    return 24 if width >= 100 else 18


def rail_lines(board, rw, height, cur_pid, focus_rail):
    ps = ordered(board)
    lines = [_pad(c("PROJECTS", "hd", bold=True), rw), " " * rw, " " * rw]
    for i, p in enumerate(ps):
        on = p.id == cur_pid
        mark = c("●", p.color) if shown(p) else c("○", "dim")
        num = c(f"{i + 1:>2}", "accent" if on else "dim")
        lead = c("▶", "accent", bold=True) if on and focus_rail else (
            c("›", "accent") if on else " ")
        tone = ("accent" if on else ("ink" if shown(p) else "dim"))
        name = c(escape(fit(p.name, rw - 8)), tone, bold=on)
        lines.append(_pad(lead + num + " " + mark + " " + name, rw))
    np_, nt = hidden_counts(board)
    lines.append(" " * rw)
    lines.append(_pad(c(fit(f" {len(ps) - np_} shown · {np_} hidden", rw), "mut"), rw))
    if nt:
        lines.append(_pad(c(fit(f" {nt} task{'s' if nt > 1 else ''} hidden", rw), "dim"), rw))
    return _fit_lines(lines, height, rw)


def render(board, width, height, today, variant, cur, folded, unfolded, focus_rail=True):
    """(frame Text, nav stops, the cursor as drawn, the timeline Text for C's
    export or None)."""
    if width < V.PRESENT_MIN_WIDTH:
        return V.render_present(board, None, None, today, width, height), [], cur, None
    if variant != "C":
        lines, nav, cur = timeline_lines(board, width, height, today, variant, cur,
                                         folded, unfolded)
        return V._present_finish(lines, height, width), nav, cur, None
    rw = rail_w(width)
    tw = width - rw - 1
    lines, nav, cur2 = timeline_lines(board, tw, height, today, "C", cur, folded, unfolded,
                                      rail=focus_rail)
    tl = _fit_lines(lines, height, tw)
    rc = _resolve(board, cur)
    pid = rc[2].id if rc else None
    rl = rail_lines(board, rw, height, pid, focus_rail)
    joined = [rl[y] + c("│", "frame") + tl[y] for y in range(height)]
    return (V._present_finish(joined, height, width), nav, cur if focus_rail else cur2,
            V._present_finish(tl, height, tw))
