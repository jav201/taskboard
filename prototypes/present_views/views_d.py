"""HISTORICAL (2026-10-18-batch-02): this round file no longer runs against the
shipped tree -- it imports `views_proto.py`, historical (`views._present_note_lines` and `_present_note_row`, deleted in 2026-10-18-batch-01 (a729f78)). It last ran against `9810be6`; the captures in `out/`
and the round page are the record. Not repaired on purpose: its outputs came
from helpers that are gone, so a repaired script would not reproduce them
(`docs/ARCHITECTURE.md` §3, `prototypes` row).

PROTOTYPE round 2 — D (split) with EVERY shown open task's notes at once.

    D2 stacked — the gantt rows, then one block per task (heading + note),
                 two columns from 100 wide, one below; space shared fairly,
                 the cursor's block gets the surplus first
    D3 columns — the gantt rows, then one column per task with a note; tasks
                 without notes collapse into one dim footer line
    D4 inline  — each note sits UNDER its own gantt row, so the bar and its
                 text read together; the ruler stays on top

All three draw from `present_tasks` (hidden tasks are out), keep the shipped
gantt rows unchanged, and declare every cut (`… +N lines`)."""
from __future__ import annotations

from taskboard import views as V
from taskboard.views import _pad, _present_finish, _strip, c, clip, escape, vis

import views_proto as VP

VIEWS = ("gantt", "stacked", "columns", "inline")


def alloc(ns: list[int], cur: int, room: int, floor_n: int = 2) -> list[int]:
    """Note lines per task: everything when it fits. Otherwise the cursor's note
    is promised up to half the room, every other note `floor_n` lines (1 when
    even that does not fit: its first line and the cut count), then the cursor
    takes what is left first and the rest share it round-robin. An empty note
    gets 0 (its heading says `no notes`)."""
    if sum(ns) <= room:
        return list(ns)
    has_cur = 0 <= cur < len(ns)
    want_c = min(ns[cur], max(floor_n, room // 2)) if has_cur else 0
    ks = [0 if i == cur else min(n, floor_n) for i, n in enumerate(ns)]
    while sum(ks) + want_c > room and max(ks, default=0) > 1:
        ks[ks.index(max(ks))] -= 1
    if has_cur:
        ks[cur] = max(0, min(want_c, room - sum(ks)))
    left = room - sum(ks)
    if has_cur:
        add = min(left, ns[cur] - ks[cur])
        ks[cur] += add
        left -= add
    while left > 0:
        grew = False
        for i in range(len(ns)):
            if left and ks[i] < ns[i]:
                ks[i] += 1
                left -= 1
                grew = True
        if not grew:
            break
    return ks


def _clipped(body: list[str], k: int, w: int) -> list[str]:
    """`k` rows of a note; the last says how much is out when it does not fit.
    At one row: the note's first line, cut, with the count beside it."""
    if k >= len(body):
        return body
    if k <= 0:
        return []
    if k == 1:
        tag = f" … +{len(body) - 1}"
        first = _strip(body[0]).rstrip()
        return [_pad(c(escape(clip(first, w - len(tag))), "ink") + c(tag, "dim"), w)]
    return body[:k - 1] + [_pad(c(f"… +{len(body) - k + 1} lines", "dim"), w)]


def _body(task, w: int) -> list[str]:
    return [VP._note_markup(l, x, w) for l, x in VP.wrap_notes(task.notes, w)]


def _heading(task, w: int, on: bool, hue: str, today, empty: bool) -> str:
    """`▌ Title ··· Sep 24–28 ▲2d` — the accent bar and title are the cursor."""
    bar = c("▌ ", "accent") if on else c("▎ ", hue)
    due, dtone = VP._due_bits(task, today)
    right = c(escape(VP._span(task)), "mut") + " " + c(due, dtone)
    if empty:
        right = c("no notes", "dim") + c("  ·  ", "dim") + right
    rw = vis(_strip(right))
    tw = max(4, w - 2 - rw - 1)
    title = c(escape(clip(task.title, tw)), "accent" if on else "bright", bold=True)
    return _pad(bar + _pad(title, tw) + " " + right, w)


def _top(board, project_id, cursor_id, today, width, view):
    proj, open_t, tasks, p, t = VP._setup(board, project_id, cursor_id, today, width)
    lines = [VP._head(proj, open_t, tasks, today, width, view)]
    lines += V._present_ruler(proj, board, p, t)
    lines.append(V._present_span_row(proj, board, p))
    rows = [V._present_task_row(x, board, p, cursor=t is not None and x.id == t.id)
            for x in open_t]
    return proj, open_t, p, t, lines, rows


# --------------------------------------------------------------------------- #
# D2 — stacked blocks
# --------------------------------------------------------------------------- #
def _stack_column(tasks, t, room, w, hue, today, scroll) -> list[str]:
    bodies = [_body(x, w - 2) for x in tasks]
    heads = len(tasks)
    cur = next((i for i, x in enumerate(tasks) if t is not None and x.id == t.id), -1)
    ks = alloc([len(b) for b in bodies], cur, max(0, room - heads))
    out = []
    for i, x in enumerate(tasks):
        on = i == cur
        bar = c("▌ ", "accent") if on else c("▎ ", hue)
        out.append(_heading(x, w, on, hue, today, not bodies[i]))
        if on and scroll and ks[i] < len(bodies[i]):
            seg = VP._scrolled(bodies[i], ks[i], scroll, lambda m: _pad(m, w - 2), w - 2)
        else:
            seg = _clipped(bodies[i], ks[i], w - 2)
        out += [_pad(bar + s, w) for s in seg]
    return out[:room] + [" " * w] * (room - len(out))


def render_stacked(board, project_id, cursor_id, today, width, height, scroll=0):
    proj, open_t, p, t, lines, rows = _top(board, project_id, cursor_id, today, width, "split")
    lines += rows + [_pad(c("─" * width, "frame"), width)]
    room = height - len(lines)
    if width >= 100:
        half = (len(open_t) + 1) // 2
        cw = (width - 2 - 3) // 2
        a = _stack_column(open_t[:half], t, room, cw, proj.color, today, scroll)
        b = _stack_column(open_t[half:], t, room, cw, proj.color, today, scroll)
        for y in range(room):
            lines.append(_pad(" " + a[y] + c(" │ ", "frame") + b[y], width))
    else:
        col = _stack_column(open_t, t, room, width - 2, proj.color, today, scroll)
        lines += [_pad(" " + r, width) for r in col]
    return _present_finish(lines, height, width)


# --------------------------------------------------------------------------- #
# D3 — one column per task
# --------------------------------------------------------------------------- #
def render_columns(board, project_id, cursor_id, today, width, height, scroll=0):
    proj, open_t, p, t, lines, rows = _top(board, project_id, cursor_id, today, width, "split")
    lines += rows + [_pad(c("─" * width, "frame"), width)]
    with_notes = [x for x in open_t if (x.notes or "").strip()]
    bare = [x for x in open_t if not (x.notes or "").strip()]
    room = height - len(lines) - (1 if bare else 0)
    ncol = max(1, min(len(with_notes), width // 28))
    # the window of columns that holds the cursor (a task without notes keeps the
    # window where it was: the first page)
    ci = next((i for i, x in enumerate(with_notes) if t is not None and x.id == t.id), 0)
    start = min(max(0, ci - ncol + 1), max(0, len(with_notes) - ncol))
    shown = with_notes[start:start + ncol]
    gap = 3
    cw = (width - 2 - gap * (len(shown) - 1)) // max(1, len(shown)) if shown else width
    cols = []
    for x in shown:
        on = t is not None and x.id == t.id
        bar = c("▌ ", "accent") if on else c("▎ ", proj.color)
        iw = cw - 2
        due, dtone = VP._due_bits(x, today)
        head = [bar + _pad(c(escape(clip(x.title, iw)), "accent" if on else "bright", bold=True), iw),
                bar + _pad(c(escape(VP._span(x)), "mut") + " " + c(due, dtone), iw)]
        body = _body(x, iw)
        nroom = room - len(head)
        if on and scroll and len(body) > nroom:
            seg = VP._scrolled(body, nroom, scroll, lambda m: _pad(m, iw), iw)
        else:
            seg = _clipped(body, nroom, iw)
        col = head + [bar + s for s in seg]
        cols.append(col + [" " * cw] * (room - len(col)))
    more_l, more_r = start, len(with_notes) - start - len(shown)
    for y in range(room):
        row = (" " * gap).join(col[y] for col in cols) if cols else ""
        lines.append(_pad(" " + row, width))
    if more_l or more_r:                       # the window is honest about its edges
        tag = "  ".join(s for s in (f"◂ {more_l} more" if more_l else "",
                                    f"{more_r} more ▸" if more_r else "") if s)
        lines[-1] = _pad(" " * (width - vis(tag) - 1) + c(tag, "dim"), width)
    if bare:
        names = ", ".join(x.title for x in bare)
        lines.append(_pad(" " + c("no notes  ", "dim") + c(escape(clip(names, width - 12)), "mut"), width))
    return _present_finish(lines, height, width)


# --------------------------------------------------------------------------- #
# D4 — inline: each note under its own gantt row
# --------------------------------------------------------------------------- #
def render_inline(board, project_id, cursor_id, today, width, height, scroll=0):
    proj, open_t, p, t, lines, rows = _top(board, project_id, cursor_id, today, width, "split")
    room = height - len(lines) - len(rows)
    ind = 4                                   # under the title, past the project bar
    nw = width - ind - 2
    bodies = [_body(x, nw) for x in open_t]
    cur = next((i for i, x in enumerate(open_t) if t is not None and x.id == t.id), -1)
    ks = alloc([len(b) for b in bodies], cur, max(0, room), floor_n=2)
    for i, x in enumerate(open_t):
        lines.append(rows[i])
        on = i == cur
        bar = c("▌", "accent") if on else c("┊", "frame")
        if on and scroll and ks[i] < len(bodies[i]):
            seg = VP._scrolled(bodies[i], ks[i], scroll, lambda m: _pad(m, nw), nw)
        else:
            seg = _clipped(bodies[i], ks[i], nw)
        lines += [_pad("  " + bar + " " + s, width) for s in seg]
    return _present_finish(lines, height, width)


def render_gantt(board, project_id, cursor_id, today, width, height, scroll=0):
    """A, with the accepted fix: the cursor's note keeps its line breaks and
    list items (still at most 3 lines)."""
    proj, open_t, p, t, lines, rows = _top(board, project_id, cursor_id, today, width, "gantt")
    lines += rows + [_pad(c("─" * width, "frame"), width)]
    for x in open_t:
        on = t is not None and x.id == t.id
        lines.append(V._present_brief(x, p, on, width))
        if on:
            body = _clipped(_body(x, width - 6), 3, width - 6)
            lines += [_pad("  " + c("· ", "dim") + b, width) for b in body]
    return _present_finish(lines, height, width)


SCROLLS = ("stacked", "columns", "inline")
RENDER = {"gantt": render_gantt, "stacked": render_stacked,
          "columns": render_columns, "inline": render_inline}
