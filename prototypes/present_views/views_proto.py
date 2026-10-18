"""HISTORICAL (2026-10-18-batch-02): this round file no longer runs against the
shipped tree -- it imports `views._present_note_lines` and `_present_note_row`, deleted in 2026-10-18-batch-01 (a729f78). It last ran against `9810be6`; the captures in `out/`
and the round page are the record. Not repaired on purpose: its outputs came
from helpers that are gone, so a repaired script would not reproduce them
(`docs/ARCHITECTURE.md` §3, `prototypes` row).

PROTOTYPE renderers for the presentation's content views (throwaway).

    A  gantt  — the shipped frame, unchanged except the dim view word in the head
    B  cards  — every task as a card: title, phase, dates, notes wrapped, links
    C  slide  — one task fills the frame like a deck slide
    D  split  — the shipped gantt rows on top, a reading pane with the FULL notes

Every view draws from `present_tasks`, so a task hidden with `space`
(`Task.show_in_present`) is out of all four. Every row is exactly `width`
cells (`_present_finish` asserts it)."""
from __future__ import annotations

import textwrap
from datetime import date

from taskboard import views as V
from taskboard.models import open_dependents, open_predecessors
from taskboard.wave import FONT_4x7
from taskboard.views import (_md, _pad, _present_brief, _present_counts, _present_finish,
                             _present_note_lines, _present_note_row, _PresentGeo, _strip, c,
                             clip, critical_chain, escape, fit, header, parse_iso,
                             present_span_label, present_tasks, vis)

VIEWS = ("gantt", "cards", "slide", "split")


# --------------------------------------------------------------------------- #
# shared pieces
# --------------------------------------------------------------------------- #
def _setup(board, project_id, cursor_id, today, width):
    proj = board.project_by_id(project_id)
    open_t, tasks = present_tasks(board, project_id)
    wide = width >= 100
    label_w, chip_w, field_w = V._present_cols(width, wide)
    ax = V._present_axis(board, proj, open_t, field_w, today)
    p = _PresentGeo(width, label_w, chip_w, field_w, ax, set(critical_chain(board)),
                    today, wide, proj.color)
    wanted = board.task_by_id(cursor_id)
    cursor = (wanted if wanted in open_t else open_t[0]) if open_t else None
    return proj, open_t, tasks, p, cursor


def _head(proj, open_t, tasks, today, width, view) -> str:
    late, open_n, done = _present_counts(open_t, tasks, today)
    title = (c("◆ PRESENT", "bright", bold=True) + c(" · ", "dim")
             + c(escape(proj.name), proj.color, bold=True)
             + c(f"  {view}", "dim"))             # the one, quiet view word
    right = c(f"{open_n} open", "mut") + c(" · ", "dim") \
        + (c(f"▲{late} past due", "over", bold=True) if late else c(f"{done} done", "done"))
    return header(title, right, width)


def wrap_notes(notes: str, w: int) -> list[tuple[str, str]]:
    """(indent, text) lines: paragraphs kept, `- ` / `1. ` items get a hanging
    indent, runs of blank lines collapse to one."""
    out: list[tuple[str, str]] = []
    for para in (notes or "").strip().split("\n"):
        para = para.rstrip()
        if not para.strip():
            if out and out[-1][1]:
                out.append(("", ""))
            continue
        lead, body = "", para.strip()
        if body[:2] in ("- ", "* ", "• "):
            lead, body = "• ", body[2:]
        elif body[:1].isdigit() and body[1:3] == ". ":
            lead, body = body[:3], body[3:]
        hang = " " * vis(lead)
        rows = textwrap.wrap(body, max(4, w - vis(lead))) or [""]
        out.append((lead, rows[0]))
        out += [(hang, r) for r in rows[1:]]
    return out


def _note_markup(lead: str, txt: str, w: int) -> str:
    return _pad(c(escape(lead), "mut") + c(escape(clip(txt, w - vis(lead))), "ink"), w)


def _due_bits(task, today) -> tuple[str, str]:
    return V._present_due(parse_iso(task.due_date), today)


def _span(task) -> str:
    return present_span_label(parse_iso(task.start_date), parse_iso(task.due_date))


def _prio(task) -> tuple[str, str]:
    return {"high": ("high", "soon"), "low": ("low", "dim")}.get(task.priority, ("normal", "mut"))


# --------------------------------------------------------------------------- #
# A — gantt (the shipped render_present, plus the view word in the head)
# --------------------------------------------------------------------------- #
def render_gantt(board, project_id, cursor_id, today, width, height, scroll=0):
    proj, open_t, tasks, p, cursor = _setup(board, project_id, cursor_id, today, width)
    lines = [_head(proj, open_t, tasks, today, width, "gantt")]
    lines += V._present_ruler(proj, board, p, cursor)
    lines.append(V._present_span_row(proj, board, p))
    for t in open_t:
        lines.append(V._present_task_row(t, board, p, cursor=cursor is not None and t.id == cursor.id))
    lines.append(_pad(c("─" * width, "frame"), width))
    for t in open_t:
        on = cursor is not None and t.id == cursor.id
        lines.append(_present_brief(t, p, on, width))
        if on:
            for ln in _present_note_lines(t.notes, width - 4, 3):
                lines.append(_present_note_row(ln, width, width - 4))
    return _present_finish(lines, height, width)


# --------------------------------------------------------------------------- #
# B — cards
# --------------------------------------------------------------------------- #
def _card(task, board, today, w: int, on: bool, hue: str) -> list[str]:
    """A card is a left bar down its whole height (no box): the bar is the
    project hue, the cursor's bar and title the accent."""
    bar = c("▌ ", "accent") if on else c("▎ ", hue)
    iw = w - 2
    rows = [bar + _pad(c(escape(clip(task.title, iw)), "accent" if on else "bright", bold=True), iw)]
    due, dtone = _due_bits(task, today)
    pr, ptone = _prio(task)
    left = c(escape(task.phase), "mut") + c(" · ", "dim") + c(pr, ptone)
    right = c(escape(_span(task)), "mut") + " " + c(due, dtone)
    gap = iw - vis(_strip(left)) - vis(_strip(right))
    if gap < 1:
        right = c(due, dtone)
        gap = iw - vis(_strip(left)) - vis(_strip(right))
    rows.append(bar + left + " " * max(1, gap) + right)
    notes = wrap_notes(task.notes, iw)
    body = [_note_markup(l, t, iw) for l, t in notes] or [_pad(c("no notes", "dim"), iw)]
    foot = []
    preds = open_predecessors(board, task)
    if preds or task.blocked:
        txt = ("blocked · " if task.blocked else "") + (
            "waits on " + ", ".join(p.title for p in preds) if preds else "")
        foot.append(_pad(c(escape(clip(txt.rstrip(" ·"), iw)), "over" if task.blocked else "mut"), iw))
    att = []
    if task.urls:
        att.append(f"↗ {len(task.urls)} link" + ("s" if len(task.urls) > 1 else ""))
    if task.images:
        att.append(f"▣ {len(task.images)} image" + ("s" if len(task.images) > 1 else ""))
    if att:
        foot.append(_pad(c("  ·  ".join(att), "dim"), iw))
    return rows, body, [bar + f for f in foot], bar


def _fit_card(parts, h: int, iw: int) -> list[str]:
    head, body, foot, bar = parts
    room = max(1, h - len(head) - len(foot))
    if len(body) > room:
        more = len(body) - room + 1
        body = body[:room - 1] + [_pad(c(f"… +{more} lines", "dim"), iw)]
    rows = head + [bar + b for b in body] + foot
    return rows + [" " * (iw + 2)] * (h - len(rows))


def render_cards(board, project_id, cursor_id, today, width, height, scroll=0):
    proj, open_t, tasks, p, cursor = _setup(board, project_id, cursor_id, today, width)
    lines = [_head(proj, open_t, tasks, today, width, "cards"), " " * width]
    ncol = 3 if width >= 100 else 2
    gap = 3
    cw = (width - 4 - gap * (ncol - 1)) // ncol
    parts = [_card(t, board, today, cw, cursor is not None and t.id == cursor.id, proj.color)
             for t in open_t]
    grid = [parts[i:i + ncol] for i in range(0, len(parts), ncol)]
    avail = height - len(lines)
    nat = [max(len(h) + len(b) + len(f) for h, b, f, _ in row) for row in grid]
    hs = list(nat)
    # a card keeps its head, two note lines (or its "+N" line) and its foot
    floor = [max(len(h) + min(2, len(b)) + len(f) for h, b, f, _ in row) for row in grid]
    cur_r = next((i // ncol for i, t in enumerate(open_t) if cursor and t.id == cursor.id), -1)
    while hs and sum(hs) + (len(hs) - 1) > avail:
        # shrink the tallest row first; the cursor's row gives way last
        others = [r for r in range(len(hs)) if r != cur_r and hs[r] > floor[r]]
        pool = others or [r for r in range(len(hs)) if hs[r] > floor[r]]
        if not pool:
            break
        r = max(pool, key=lambda k: hs[k])
        hs[r] -= 1
    for r, row in enumerate(grid):
        cols = [_fit_card(pt, hs[r], cw - 2) for pt in row]
        cols += [[" " * cw] * hs[r]] * (ncol - len(cols))
        for y in range(hs[r]):
            lines.append(_pad("  " + (" " * gap).join(col[y] for col in cols), width))
        if r < len(grid) - 1:
            lines.append(" " * width)
    return _present_finish(lines, height, width)


# --------------------------------------------------------------------------- #
# C — slide per task
# --------------------------------------------------------------------------- #
FONT = dict(FONT_4x7, **{"-": ("....", "....", "....", "####", "....", "....", "....")})


def _drawn(text: str) -> list[str]:
    """Digits drawn in half blocks from wave.FONT_4x7: 7 dot rows -> 4 cell rows."""
    rows = []
    for r in range(0, 8, 2):
        out = []
        for ch in text:
            g = FONT.get(ch, FONT[" "])
            cell = ""
            for x in range(4):
                top = g[r][x] == "#"
                bot = r + 1 < 7 and g[r + 1][x] == "#"
                cell += "█" if top and bot else "▀" if top else "▄" if bot else " "
            out.append(cell)
        rows.append(" ".join(out))
    return rows


def _hero(task, today) -> tuple[list[str], str, str]:
    """The slide's drawn figure: how many days late / left, or TODAY."""
    d = parse_iso(task.due_date)
    if d is None:
        return [], "NO DUE DATE", "dim"
    n = (d - today).days
    if n == 0:
        return [], "DUE TODAY", "soon"
    if n < 0:
        return _drawn(str(-n)), "DAYS LATE" if n < -1 else "DAY LATE", "over"
    return _drawn(str(n)), "DAYS LEFT" if n > 1 else "DAY LEFT", "bright"


def _spaced(title: str) -> str:
    """Display type without a font: spaced capitals, three cells between words."""
    return "   ".join(" ".join(word.upper()) for word in title.split())


def _phase_meter(task, board, w: int) -> str:
    phases = board.phases
    i = phases.index(task.phase) if task.phase in phases else -1
    out = []
    for k, ph in enumerate(phases):
        if k < i:
            out.append(c("● " + escape(ph), "mut"))
        elif k == i:
            out.append(c("◉ " + escape(ph.upper()), "bright", bold=True))
        else:
            out.append(c("○ " + escape(ph), "dim"))
    return _pad(c(" ──── ", "frame").join(out), w)


def _phase_dots(task, board) -> str:
    phases = board.phases
    i = phases.index(task.phase) if task.phase in phases else -1
    dots = " ".join(c("●", "mut") if k < i else c("◉", "bright", bold=True) if k == i
                    else c("○", "dim") for k in range(len(phases)))
    return dots + "  " + c(escape(task.phase.upper()), "bright", bold=True)


def render_slide(board, project_id, cursor_id, today, width, height, scroll=0):
    proj, open_t, tasks, p, t = _setup(board, project_id, cursor_id, today, width)
    lines = [_head(proj, open_t, tasks, today, width, "slide"), " " * width]
    if t is None:
        return _present_finish(lines + [_pad(c("  nothing to present", "dim"), width)],
                               height, width)
    m = 4 if width >= 100 else 2
    iw = width - 2 * m
    pad = " " * m

    def row(markup: str) -> str:
        return _pad(pad + markup, width)

    fig, cap, ftone = _hero(t, today)
    hw = max([vis(x) for x in fig] + [vis(cap)]) if (fig or cap) else 0
    tw = iw - hw - 4
    big = _spaced(t.title)
    tl = textwrap.wrap(big, tw, break_on_hyphens=False) if vis(big) <= tw * 2 else None
    if not tl or len(tl) > 2:                                  # too long: plain caps
        tl = [clip(x, tw) for x in textwrap.wrap(t.title.upper(), tw)[:2]]
    left = [c(escape(ln), "bright", bold=True) for ln in tl]
    left.append(c("━" * min(tw, max(vis(x) for x in tl)), "accent"))      # the cursor
    pr, ptone = _prio(t)
    left += [" ",
             c(escape(_span(t)), "bright", bold=True)
             + c("   ·   ", "dim") + c(f"{pr} priority", ptone)
             + (c("   ·   ", "dim") + c("◆ milestone", proj.color) if t.milestone else "")]
    meter = _phase_meter(t, board, 0)
    if vis(_strip(meter)) > tw:                 # narrow: the dots alone, then the phase
        meter = _phase_dots(t, board)
    left.append(meter)
    right = [c(x, ftone, bold=True) for x in fig] + [c(cap, ftone if not fig else "mut")]
    for y in range(max(len(left), len(right))):
        lm = _pad(left[y], tw) if y < len(left) else " " * tw
        rm = right[y] if y < len(right) else ""
        lines.append(row(lm + "    " + _pad(rm, hw)))

    preds, deps = open_predecessors(board, t), open_dependents(board, t)
    if t.blocked:
        lines.append(row(c("BLOCKED", "over", bold=True)))
    if preds:
        txt = ", ".join(f"{q.title} ({_due_bits(q, today)[0]})" for q in preds)
        lines.append(row(c("waits on  ", "dim") + c(escape(clip(txt, iw - 10)), "mut")))
    if deps:
        txt = ", ".join(q.title for q in deps)
        lines.append(row(c("unblocks  ", "dim") + c(escape(clip(txt, iw - 10)), "mut")))
    for u in t.urls[:2]:
        lines.append(row(c("↗ ", "dim") + c(escape(clip(u.split("://", 1)[-1], iw - 2)), "mut")))
    if len(t.urls) > 2:
        lines.append(row(c(f"↗ +{len(t.urls) - 2} more links", "dim")))
    if t.images:
        names = ", ".join(i.rsplit("/", 1)[-1] for i in t.images)
        lines.append(row(c(f"▣ {len(t.images)} image{'s' if len(t.images) > 1 else ''}  ", "dim")
                         + c(escape(clip(names, iw - 12)), "mut")))
    lines.append(row(c("─" * iw, "frame")))

    measure = min(iw, 88)                     # a readable line length, not the full width
    notes = wrap_notes(t.notes, measure)
    room = height - len(lines) - 2            # 2: blank + the position strip
    body = [_note_markup(l, x, measure) for l, x in notes] or [c("no notes", "dim")]
    lines += _scrolled(body, room, scroll, row, measure)

    while len(lines) < height - 1:
        lines.append(" " * width)
    lines = lines[:height - 1] + [_strip_row(open_t, t, width)]
    return _present_finish(lines, height, width)


def _scrolled(body: list[str], room: int, scroll: int, row, w: int) -> list[str]:
    """`room` rows of `body` from `scroll`; the edge rows say what is out of
    view instead of cutting silently."""
    if room <= 0:
        return []
    if len(body) <= room:
        return [row(b) for b in body]
    scroll = max(0, min(scroll, len(body) - room + 1))
    above = scroll
    view_n = room - (1 if above else 0)
    shown = body[scroll:scroll + view_n]
    below = len(body) - scroll - len(shown)
    if below > 0:
        shown = shown[:-1]
        below += 1
    out = [row(c(f"↑ {above} lines above", "dim"))] if above else []
    out += [row(b) for b in shown]
    if below > 0:
        out.append(row(c(f"↓ {below} more lines", "dim")))
    return out


def _strip_row(open_t, t, width: int) -> str:
    """The deck's position strip: a dot per task, the position, prev and next."""
    i = open_t.index(t)
    dots = " ".join(c("●", "accent", bold=True) if k == i else c("○", "dim")
                    for k in range(len(open_t)))
    pos = c(f"  {i + 1} / {len(open_t)}", "mut")
    side = (width - 4 - vis(_strip(dots + pos))) // 2 - 3
    prev = c("◂ " + escape(clip(open_t[i - 1].title, side - 2)), "dim") if i > 0 else ""
    nxt = c(escape(clip(open_t[i + 1].title, side - 2)) + " ▸", "dim") if i + 1 < len(open_t) else ""
    mid = dots + pos
    lpad = (width - vis(_strip(mid))) // 2
    left = _pad("  " + prev, lpad)
    rest = width - lpad - vis(_strip(mid))
    return left + mid + " " * max(0, rest - vis(_strip(nxt)) - 2) + nxt + "  "


# --------------------------------------------------------------------------- #
# D — split: the shipped gantt rows, then a reading pane
# --------------------------------------------------------------------------- #
def render_split(board, project_id, cursor_id, today, width, height, scroll=0):
    proj, open_t, tasks, p, t = _setup(board, project_id, cursor_id, today, width)
    lines = [_head(proj, open_t, tasks, today, width, "split")]
    lines += V._present_ruler(proj, board, p, t)
    lines.append(V._present_span_row(proj, board, p))
    for x in open_t:
        lines.append(V._present_task_row(x, board, p, cursor=t is not None and x.id == t.id))
    lines.append(_pad(c("─" * width, "frame"), width))
    if t is None:
        return _present_finish(lines, height, width)

    side_w = 28 if width >= 100 else 22
    nw = width - side_w - 3 - 2                        # 2 left margin, 3 gutter
    due, dtone = _due_bits(t, today)
    pr, ptone = _prio(t)
    side = [c(escape(clip(t.title, side_w)), "accent", bold=True),
            c(escape(_span(t)), "bright") + "  " + c(due, dtone, bold=True),
            c(escape(t.phase), "mut") + c(" · ", "dim") + c(pr, ptone)]
    if t.blocked:
        side.append(c("BLOCKED", "over", bold=True))
    preds = open_predecessors(board, t)
    if preds:
        side.append(c("waits on", "dim"))
        side += [c("  " + escape(clip(q.title, side_w - 2)), "mut") for q in preds]
    deps = open_dependents(board, t)
    if deps:
        side.append(c("unblocks", "dim"))
        side += [c("  " + escape(clip(q.title, side_w - 2)), "mut") for q in deps]
    if t.urls:
        side.append(c("links", "dim"))
        side += [c("↗ " + escape(clip(u.split("://", 1)[-1], side_w - 2)), "mut") for u in t.urls]
    if t.images:
        side.append(c(f"▣ {len(t.images)} image{'s' if len(t.images) > 1 else ''}", "dim"))

    room = height - len(lines)
    notes = wrap_notes(t.notes, nw)
    body = [_note_markup(l, x, nw) for l, x in notes] or [_pad(c("no notes", "dim"), nw)]
    pane = _scrolled(body, room, scroll, lambda m: _pad(m, nw), nw)
    for y in range(room):
        s = _pad(side[y], side_w) if y < len(side) else " " * side_w
        n = pane[y] if y < len(pane) else " " * nw
        lines.append(_pad("  " + s + c(" │ ", "frame") + n, width))
    return _present_finish(lines, height, width)


RENDER = {"gantt": render_gantt, "cards": render_cards,
          "slide": render_slide, "split": render_split}
