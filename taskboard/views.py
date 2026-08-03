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

import re
from datetime import date, timedelta
from typing import NamedTuple

from rich.cells import cell_len, set_cell_size
from rich.markup import escape
from rich.text import Text

from .models import Board, Task, days_in_phase, parse_iso
from .wave import DOT_ROWS, Bitmap, load_curve

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
    "ash": "#6b4a3f",     # the CONSUMED field: days already spent (Prism's 4th house)
    "bright": "#e6edf7",
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
def vis(s: str) -> int:
    """How wide `s` is ON SCREEN, in cells — the only ruler this file may use.

    `len()` counts codepoints and the terminal draws cells, and the two disagree
    constantly: an emoji and a CJK glyph are 2 cells, a combining mark is 0. A
    row measured with `len` leans as soon as a human types one of those into a
    task, and a column layout that leans is the one failure it cannot absorb.
    Pass PLAIN text — strip the markup first (`_strip`) or the tags get counted."""
    return cell_len(s)


def fit(s: str, width: int, align: str = "left") -> str:
    if width <= 0:
        return ""
    if vis(s) > width:
        # `set_cell_size` cuts on a GLYPH boundary (padding a cell when a wide
        # one straddles the cut), so the result is exactly width-1 cells and can
        # never come back holding half a character. '…' is the remaining cell.
        return set_cell_size(s, width - 1) + "…"
    pad = width - vis(s)
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
# the shared day axis and the field
#
# ONE DOT COLUMN = ONE DAY, and every row of a view shares the same axis, so
# `today` sits in the same screen column on every line. The field is drawn with
# the dot engine (`.wave`) and packed to braille; whatever the engine leaves
# unlit is DRAWN as its own lattice — ash behind today, dim ahead — never left
# as void. Pure helpers: no view calls them yet.
# ---------------------------------------------------------------------------
RULE = "╎"        # the today boundary at rest
# THE AMBIENT: the rule breathes, and it does so in the GLYPH, never in colour.
# Four phases on the app's one shared 1 s clock = a 4 s cycle, which clears the
# ≥2 s floor for an always-open surface (the 400-2000 ms band reads as a fault).
RULE_PHASES = ("╎", "╽", "╎", "╿")
LATTICE = "·"
OFF_LEFT, OFF_RIGHT = "◂", "▸"


class FieldGeo(NamedTuple):
    """The geometry every row of the view shares. Ported from the proposal's
    `Geo` (`_tui_prism_proposal/prototype.py:162`)."""
    width: int
    height: int
    large: bool
    label_w: int
    figs_w: int
    field_x: int
    field_w: int
    dot_w: int
    today_dc: int
    today_cell: int
    profile_rows: int


def field_geometry(width: int, height: int) -> FieldGeo:
    large = width >= 88 and height >= 26
    label_w = 15 if large else 12
    figs_w = 13 if large else 11
    field_w = max(8, width - label_w - figs_w - 1)
    dot_w = field_w * 2
    # today lands on an EVEN dot column so no cell straddles the boundary
    today_dc = (int(dot_w * 0.30) // 2) * 2
    return FieldGeo(width=width, height=height, large=large, label_w=label_w,
                    figs_w=figs_w, field_x=label_w, field_w=field_w, dot_w=dot_w,
                    today_dc=today_dc, today_cell=label_w + today_dc // 2,
                    profile_rows=4 if large else 2)


def day_col(d: date, today: date, geo: FieldGeo) -> int | tuple[str, int]:
    """The dot column of a date — or ``("L"|"R", clamped)`` when it falls
    outside the window. CLIP AND FLAG: a date beyond the window is never
    silently pinned to the edge, because a mark at the edge and a mark past it
    would then be the same picture."""
    x = geo.today_dc + (d - today).days
    if x < 0:
        return ("L", 0)
    if x >= geo.dot_w:
        return ("R", geo.dot_w - 1)
    return x


def off_window_glyph(col: int | tuple[str, int]) -> str:
    """The mark a flagged column earns, or "" for one that fits. This is the
    half `Geo.day_dc` never had: it returned the flag and every caller in the
    proposal dropped it (`prototype.py:218`), so nothing was ever drawn."""
    if isinstance(col, tuple):
        return OFF_LEFT if col[0] == "L" else OFF_RIGHT
    return ""


def field_rows(bm: Bitmap, geo: FieldGeo, hue: str, *,
               off_left: bool = False, off_right: bool = False,
               phase: int = 0) -> list[str]:
    """Pack a dot bitmap to cells and colour them: the figure in `hue` (ash once
    it is behind today), the unlit ground as the lattice, and the today rule in
    the attention hue. Every row is EXACTLY `geo.field_w` cells.

    `off_left`/`off_right` replace the edge cell with `◂`/`▸` — something is out
    there that this window cannot show. The mark is neutral: it judges nothing
    and names nothing, it reports the window."""
    rows = []
    for chars in bm.to_braille():
        cells = list(chars[:geo.field_w])
        cells += [" "] * (geo.field_w - len(cells))
        out = []
        for i, ch in enumerate(cells):
            past = (2 * i + 1) < geo.today_dc
            if ch == " ":
                if i == geo.today_dc // 2:
                    out.append(c(RULE_PHASES[phase % len(RULE_PHASES)], "accent"))
                else:
                    out.append(c(LATTICE, "ash" if past else "dim"))
            else:
                out.append(c(ch, "ash" if past else hue))
        if off_left:
            out[0] = c(OFF_LEFT, "mut")
        if off_right:
            out[-1] = c(OFF_RIGHT, "mut")
        rows.append("".join(out))
    return rows


# ---------------------------------------------------------------------------
# glyphs
# ---------------------------------------------------------------------------
# ARCHIVED IS A STATE, AND IT NEEDED A SEAT. Archived work is SPENT, so it takes
# the spent house — `ash`, the same tone the field uses for days already gone and
# the gantt for work at rest. It may not take a hue (a hue NAMES a project) and it
# may not take `over`/`soon` (those JUDGE, and nothing is expected of archived
# work, so nothing about it can be late).
#
# The glyph is `▣`: a box with its contents put away, which is what archiving is.
# It is not `✓` — that is DONE, a different fact, and a task can be archived
# without ever having been finished. Geometric Shapes is the block the app already
# draws a width-1 indicator from (`▤`, images), so it costs one cell like the rest.
ARCHIVED_MARK = "▣"


def status_glyph(board: Board, task: Task) -> tuple[str, str]:
    if task.archived:
        # ahead of `done` and `blocked` on purpose: archived is TERMINAL. A task
        # that is both archived and overdue is not overdue — it is put away.
        return (ARCHIVED_MARK, "ash")
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
    """A width-exact card: `prefix` + truncated title + right indicators (↗ !).

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
        # THE GLYPH HOUSE. High priority used to be a ◉ in `amber` — the exact hex
        # (#fbbf24) the app uses for "due today". Two meanings, one colour, so the
        # mark could not be read. Severity keeps that seat (it is worn by dates:
        # date_chip / reldue_token); priority is carried by the SHAPE `!` in the
        # neutral ink tone, which claims neither the identity nor the judging house.
        tokens.append(("!", "ink"))
    if task.images:
        # `mut`, not `sky`: an attachment is an ATTRIBUTE of one task, and `sky`
        # is an offered PROJECT hue. An identity tone worn by a task attribute
        # says "this task belongs to the sky project" to anyone reading the
        # board by colour. Its siblings already sit in neutral houses (↗ accent,
        # ! ink); this is the quietest of the three and takes the quietest tone.
        tokens.append(("▤", "mut"))     # width-1 image indicator, distinct from ↗/!
    if task.archived:
        # LAST in the list so it is the last thing shed under width pressure —
        # it is the only token here that says the row is not live work.
        tokens.append((ARCHIVED_MARK, "ash"))
    ind_markup, used = _fit_indicators(tokens, wc - len(prefix))
    title_w = max(0, wc - len(prefix) - used)
    pre = c(prefix, prefix_color) if prefix else ""
    return pre + title_markup(task, title_w, selected, arrow=False) + ind_markup


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


# The columns view renders each task's urgency as ONE block-ramp cell (the "heat"
# glyph). Kept as a module-level dict so the mapping (glyph + palette key) is
# testable on its own. ``urgency`` already returns "done" for last-phase tasks,
# so a done card wins the ✓ without any extra check here.
HEAT = {
    "overdue": ("█", "over"),
    "today":   ("▓", "soon"),
    "week":    ("▒", "accent"),
    "later":   ("░", "dim"),
    "none":    ("·", "dim"),
    "done":    ("✓", "done"),
}


def reldue_token(task: Task, today: date, board: Board) -> tuple[str, str]:
    """A short relative-due token + color-key: '-2d' / 'today' / '+5d', or ''
    when the task has no due date (or is done). Colored by the same urgency."""
    u = urgency(task, today, board)
    d = parse_iso(task.due_date)
    if d is None or u in ("none", "done"):
        return "", "dim"
    delta = (d - today).days
    if delta < 0:
        return f"{delta}d", "over"        # the minus sign is already in the number
    if delta == 0:
        return "today", "soon"
    if delta <= 7:
        return f"+{delta}d", "accent"
    return f"+{delta}d", "dim"


def sort_by_due(tasks: list[Task]) -> list[Task]:
    """A COPY of `tasks` ordered by due date (soonest first); undated tasks sink
    to the bottom. Stable within a group; never mutates the input list."""
    return sorted(tasks, key=lambda t: (parse_iso(t.due_date) is None,
                                        parse_iso(t.due_date) or date.max))


_URG_COLOR = {"overdue": "over", "today": "soon", "week": "later",
              "later": "later", "none": "dim", "done": "done"}


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
    """THE HEAD ROW. No box: this design commits with RULES, not boxes — the
    prototype's closure law, which the frame was the last thing failing.

    The row carries facts (what the view is, what it counts) across its whole
    width; `head_rule` under it is the only box-drawing left, and it is one row
    rather than a border on all four sides."""
    tvis, rvis = vis(_strip(title)), vis(_strip(right))
    if tvis + rvis + 3 > w:               # too tight -> the right content goes
        right, rvis = "", 0
    if tvis + 2 > w:                      # still tight -> truncate the title
        return c(fit(_strip(title), w), "accent", bold=True)
    gap = max(1, w - tvis - rvis - 1)
    return title + " " * gap + right + " "


def head_rule(w: int) -> str:
    return c("─" * max(0, w), "frame")


def line(inner: str, w: int | None = None) -> str:
    """A body row IS its content now — there are no side borders to add."""
    return inner


def blank_line(w: int) -> str:
    return " " * w


def rule_row(junctions: dict[int, str], w: int) -> str:
    """The rule under a set of columns, in the SAME coordinates as the columns.

    This replaces a framed builder that reserved column 0 for a `├` and column
    w-1 for a `┤`, and therefore wrote every junction one cell to the RIGHT of
    the `│` it was supposed to sit under. That was invisible while the design had
    side borders and became a visible lean the moment it went frameless: measured
    at 120 cells, the kanban headers separated at 30·60·90 and the rule crossed
    at 31·61·91, with two stray corner glyphs the other rows do not have.

    A rule is a body row like any other here — it spends the full width and it
    owns no edges. `_col_junctions`/`_matrix_junctions` already return content
    coordinates, so they are used as-is."""
    chars = ["─"] * w
    for pos, ch in junctions.items():
        if 0 <= pos < w:
            chars[pos] = ch
    return c("".join(chars), "frame")


def bottom(junctions: dict[int, str] | None, w: int) -> str:
    """Kept as a seam for callers, but a frameless view closes with nothing."""
    return ""


def fill_height(lines: list[str], height: int, w: int) -> list[str]:
    """Pad blank rows so the view fills the viewport when content is short. The
    pad goes ABOVE the last row, which is the axis every view closes with."""
    lines = [x for x in lines if x != ""]          # a frameless close adds none
    if not height or len(lines) >= height:
        return lines                               # taller than the viewport: it scrolls
    pad = height - len(lines)
    return lines[:-1] + [blank_line(w)] * pad + [lines[-1]]


def _clamp_width(width: int) -> int:
    return max(MIN_WIDTH, int(width) if width else MIN_WIDTH)


# ---------------------------------------------------------------------------
# span economy: say the same colors with fewer runs
# ---------------------------------------------------------------------------
# `c()` wraps EVERY cell it colors, so a 60-cell band of one tone leaves 60
# `[#hex]…[/]` pairs where one would do. That redundancy is not cosmetic: each
# run becomes its own rich Span, then its own Segment, and Textual stamps a
# per-run `{"offset": (x, y)}` into each Segment's style meta
# (textual/content.py). rich's `Style.__hash__` includes `_meta`, so two
# segments that look identical NEVER compare equal — which means
# `Strip.simplify()` can merge none of them. The run count we emit is the run
# count we pay, all the way to the terminal. So we pay it once, here.
_TAGS = re.compile(r"((\\*)\[([a-z#/@][^[]*?)])")


def _tag_name(content: str) -> str:
    """The name rich matches a closing tag against ('link' of 'link=url')."""
    return content.partition("=")[0].strip()


def collapse_runs(markup: str) -> str:
    """Drop a close tag that is immediately followed by re-opening the SAME
    style. Purely syntactic: the rendered text and every character's style are
    unchanged (tests/test_span_economy.py fixes that), only the run count drops.

    Anything this does not understand is left exactly as it was found — the
    optimization may under-collapse, but it may never alter what is drawn."""
    if "[" not in markup:
        return markup
    out: list[str] = []
    stack: list[str] = []          # open tag CONTENTS, outermost first
    pending: str | None = None     # a close tag held back, awaiting its neighbour
    pos = 0

    def flush() -> None:
        """Emit the held close and retire the tag it closes."""
        nonlocal pending
        if pending is None:
            return
        name = _tag_name(pending[1:])
        if not name:                                   # bare '[/]' closes the top
            if stack:
                stack.pop()
        else:                                          # named close: innermost match
            for i in range(len(stack) - 1, -1, -1):
                if _tag_name(stack[i]) == name:
                    stack.pop(i)
                    break
        out.append(f"[{pending}]")
        pending = None

    for m in _TAGS.finditer(markup):
        start, end = m.span()
        full, escapes, content = m.groups()
        if start > pos:                                # literal text between tags
            flush()
            out.append(markup[pos:start])
        if escapes and len(escapes) % 2:               # '\[' -> an escaped brace,
            flush()                                    # literal text, not a tag
            out.append(full)
            pos = end
            continue
        if escapes:                                    # even backslashes: real tag,
            flush()                                    # but the slashes are text
            out.append(escapes)
        if content.startswith("/"):
            flush()                                    # a close ends any held close
            pending = content
        else:
            # THE ONE COLLAPSE: the held close retires exactly this style, and
            # this reopens it verbatim -> both tags are noise. Only when the
            # closed tag is the one on top, so nesting order is never rewritten.
            if pending is not None and stack and stack[-1] == content:
                closing = _tag_name(pending[1:])
                if not closing or closing == _tag_name(content):
                    pending = None                     # cancel the pair, keep the
                    pos = end                          # style open across the seam
                    continue
            flush()
            out.append(f"[{content}]")
            stack.append(content)
        pos = end

    flush()
    out.append(markup[pos:])
    return "".join(out)


def to_text(lines: list[str], height: int, w: int) -> Text:
    """The ONE seam where a view's markup becomes a Text. Every view closes
    through here so span economy is not something a new view can forget.

    `emoji=False` is LOAD-BEARING, not a tuning knob. With it on, rich rewrites
    `:bug:` into a 2-cell glyph INSIDE this call — after every width the row
    builders computed. `fit` measured 5 cells and the terminal drew 2, so the
    row came out 3 short and leaned against every other row (measured: 93 in a
    96-cell view). No amount of correct measuring can reach a substitution that
    happens downstream of all measuring, so the substitution goes. Emoji still
    work — you type the glyph itself, which is a real character `vis()` can
    measure, and the picker inserts exactly that."""
    return Text.from_markup(collapse_runs("\n".join(fill_height(lines, height, w))),
                            emoji=False)


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


# --- the lane row's own vocabulary ------------------------------------------
# A project's status is a ONE-CELL mark, and `on_track` has none — so what is
# marked is the exception the eye should find.
STATUS_MARK = {"paused": "‖", "cancelled": "╳", "completed": "✓"}

# the phase glyph: one cell, the dot CLIMBS as the task advances
_PHASE_DOTS = [0xC0, 0x24, 0x12, 0x09]          # bottom row -> top row, full width


def phase_glyph(rows: set[int]) -> str:
    m = 0
    for r in rows:
        m |= _PHASE_DOTS[max(0, min(3, r))]
    return chr(0x2800 + m)


def clip(s: str, w: int) -> str:
    """Truncate with a VISIBLE mark — silent truncation is a lie about width."""
    if w <= 0:
        return ""
    if w <= 0:
        return ""
    return s if vis(s) <= w else set_cell_size(s, w - 1) + "…"


class LaneFacts(NamedTuple):
    """What the view reads about one project. Ported from the proposal's `Lane`
    minus its ranking (that arrives with the allocator)."""
    name: str
    hue: str
    status: str
    tasks: list
    open: list
    late: list
    done_n: int
    total: int
    today_n: int
    high: int
    due_in: int | None
    worst: int

    @property
    def resting(self) -> bool:
        return not self.open

    @property
    def closed(self) -> bool:
        return self.status in ("completed", "cancelled")


def lane_facts(board: Board, today: date, name: str, hue: str, status: str,
               due_date: str | None, rows: list[Task]) -> LaneFacts:
    """`rows` are already this lane's tasks — the Inbox is a lane too, and its
    tasks are the ones whose project is missing, not the ones with a matching id."""
    # ARCHIVED WORK IS NOT OPEN WORK. Nothing is expected of it, so nothing
    # about it can be late, it exerts no pressure on the ranking, and it is not
    # counted among what is still to do. Before this, turning `v` on silently
    # re-ranked the board and hung a ▲ severity chip on work that was put away.
    open_ = [t for t in rows if not board.is_done(t) and not t.archived]
    late = [t for t in open_
            if (d := parse_iso(t.due_date)) is not None and d < today]
    pd = parse_iso(due_date)
    due_in = (pd - today).days if pd else None
    worst = max(((today - parse_iso(t.due_date)).days for t in late), default=0)
    if due_in is not None and due_in < 0 and open_:
        worst = max(worst, -due_in)
    return LaneFacts(
        name=name, hue=hue, status=status,
        tasks=rows, open=open_, late=late, done_n=len(rows) - len(open_),
        total=len(rows),
        today_n=sum(1 for t in open_ if parse_iso(t.due_date) == today),
        high=sum(1 for t in open_ if t.priority == "high"),
        due_in=due_in, worst=worst)


def lane_pressure(lane: LaneFacts) -> tuple:
    """What puts a project at the top: how much of it is already late, how late
    the worst of it is, how much falls due today, and how close its own date is.
    THE ORDER IS THE HIERARCHY — the view does not ask the reader to scan for
    the project that needs them."""
    return (-len(lane.late), -lane.worst, -lane.today_n,
            lane.due_in if lane.due_in is not None else 9999)


def lanes_of(board: Board, show_archived: bool, today: date) -> list[LaneFacts]:
    """Every project as a lane, then the Inbox if it has anything — RANKED by
    pressure. Work with nothing open sinks to the bottom, and so does work
    nobody expects anything from (cancelled, completed)."""
    tasks = board.visible_tasks(show_archived)
    out = [lane_facts(board, today, p.name, p.color, p.status, p.due_date,
                      [t for t in tasks if t.project_id == p.id])
           for p in board.visible_projects(show_archived)]
    inbox = [t for t in tasks if board.project_by_id(t.project_id) is None]
    if inbox:
        out.append(lane_facts(board, today, "Inbox", "dim", "on_track", None, inbox))
    return sorted(out, key=lambda ln: (ln.resting, ln.closed, lane_pressure(ln)))


def allocate(geo: FieldGeo, opens: list[int], n_rest: int,
             room: int) -> tuple[int, int, int]:
    """(titles per stacked project, rows for the lead's bench, wave rows each).

    Space is INFORMATION-PROPORTIONAL IN BOTH DIRECTIONS: the search maximises
    rows actually used, breaking ties toward titles first (a named task outranks
    a taller curve on a mission-control surface) and toward a taller LEAD before
    taller stack waves — five equal waves would be a tie of near-equals, and the
    lead would stop being the hero."""
    floor = geo.profile_rows
    # The bench ceiling is the HERO'S DESIGNED SIZE and stays a constant. The
    # wave cap of 2 was the arbitrary one, and it is why a CALM board exhausted
    # the ladder with a third of the panel still void: everything was named,
    # resolution was at its cap, and eleven rows had nothing they were allowed
    # to buy. Rung two now stops where it runs out of ROOM or of LEAD, not at a
    # round number someone typed.
    ceil = 10 if geo.large else 6
    # Rung one's ceiling is INFORMATION, not a constant: naming beyond the
    # fullest lane buys nothing, and stopping short of it strands the reader.
    # The old cap of 3 was a hole — a lane with 8 open tasks could name 3, and
    # the prohibition then froze the field at one row, so the rest went void.
    most = max(opens, default=0)
    best, best_score = (0, floor, 1), (-1, -1, -1)
    for titles in range(0, most + 1):
        unnamed = sum(max(0, o - titles) for o in opens)
        for prof in range(floor, ceil + 1):
            # THE PROHIBITION. The field may NOT grow while a task is still
            # unnamed: a task the reader cannot see is the most expensive
            # absence on the screen, and buying resolution first is decoration
            # paid for with information they never get to read. Name, then
            # resolve, then say what is not there — in that order and no other.
            #
            # And THE LEAD STAYS THE HERO: a stack wave may never reach the
            # lead's own bench. That is what bounds the field once the room
            # stops bounding it — five equal waves would be a tie of near-equals.
            top = 1 if unnamed else max(1, prof - 1)
            for wrows in range(1, top + 1):
                need = prof + sum(wrows + min(titles, o) for o in opens) + n_rest
                if need <= room and (need, titles, prof) > best_score:
                    best_score, best = (need, titles, prof), (titles, prof, wrows)

    # RUNG FOUR — the hero absorbs what nothing else can use. Rungs one and two
    # answer to information, so on a CALM board they both saturate with rows to
    # spare: everything is named and the wave has reached the lead. Those rows
    # cannot buy anything, and a taller hero is worth more than void — but ONE
    # row is left unspent, because rung three still has to say what is not there
    # and rung four must never outbid a rung above it.
    # It needs no guard against firing while work is unnamed: if anything were
    # unnamed then some lane has more open work than `titles`, so buying one
    # more title would RAISE `need` — and the search maximises `need`. Surplus
    # and unnamed work cannot coexist. The order is enforced by the search, not
    # by a condition, and a condition that cannot be false is not a safeguard.
    titles, prof, wrows = best
    if best_score[0] > 0:
        prof += max(0, room - best_score[0] - 1)
    return titles, prof, wrows


def lane_titles(lane: LaneFacts, limit: int) -> list[Task]:
    """The open work this lane NAMES, soonest first, undated last. One source of
    truth: the renderer draws these and `nav_model` walks these."""
    undated = [t for t in lane.open if parse_iso(t.due_date) is None]
    dated = sorted([t for t in lane.open if parse_iso(t.due_date)],
                   key=lambda t: parse_iso(t.due_date))
    # archived work is named LAST when there is room left: it is spent, so live
    # work outranks it for the naming the allocator paid for
    put_away = [t for t in lane.tasks if t.archived]
    return (dated + undated + put_away)[:max(0, limit)]


def pressure_chip(lane: LaneFacts) -> tuple[str, str]:
    """SEVERITY'S ONE SEAT: the `▲Nd` chip, and it is worn by a DATE-DISTANCE.
    A cancelled or completed project is never judged — nothing is expected of
    it, so nothing about it can be late."""
    if lane.closed:
        return (f"{lane.due_in:+d}d" if lane.due_in is not None else "—"), "dim"
    if lane.late:
        return f"▲{lane.worst}d", "over"
    if lane.due_in is not None and lane.due_in < 0 and lane.open:
        return f"▲{-lane.due_in}d", "over"
    if lane.today_n:
        return "today", "accent"
    if lane.due_in is not None:
        return f"+{lane.due_in}d", "mut"
    return "—", "dim"


def due_token(task: Task, today: date) -> tuple[str, str]:
    d = parse_iso(task.due_date)
    if d is None:
        return "—", "dim"
    n = (d - today).days
    if n < 0:
        return f"▲{-n}d", "over"
    if n == 0:
        return "today", "accent"
    return f"+{n}d", "mut"


METER_W = 6            # the right edge of a row, in cells

# The due meter's categories, and the length each one draws. LENGTH IS THE TIME
# THAT REMAINS, so a SHORT bar means act now — triage without reading a number.
# The scale is categorical, not linear: a linear one spends all its resolution
# on a distant future where nothing is decided.
_METER_FILL = {"overdue": 0, "today": 1, "week": 2, "month": 4, "later": 6}


def days_until(iso: str | None, today: date) -> int | None:
    d = parse_iso(iso)
    return (d - today).days if d else None


def _right(cells: list[tuple[str, str]], width: int,
           pad_tone: str = "ash") -> list[tuple[str, str]]:
    """Right-align the reading in the edge's `width` cells, over the board's own
    ground rather than over blanks.

    The bar this replaced filled its unlit cells with `·`, and the occupancy law
    counts them: padding with spaces instead would have quietly emptied six cells
    on every row of the board — the exact dead space the design spent a whole
    pass removing."""
    cells = cells[:width]
    return [("·", pad_tone)] * (width - len(cells)) + cells


def due_meter(task_or_lane_days: int | None, done: bool, width: int = METER_W
              ) -> list[tuple[str, str]]:
    """The six-cell right edge, as (glyph, tone) cells. IT SAYS THE NUMBER.

    This was a BAR whose length stood for a band of urgency, on the argument
    that triage is pre-attentive and nobody reads a number to tell overdue from
    distant. Reversed after living with it: the bar could not tell 4 days from
    5 — both landed in the same `week` band and drew the same two cells — so the
    one column whose entire job is "how long have I got" answered in buckets.
    A number costs the same six cells and is exact.

    It still answers WHEN, never WHOSE: identity travels in the spine at the
    other end of the row, so this edge stays in neutral tones whatever the board
    holds. Severity keeps its single seat — overdue lights the `▲` cap, and the
    count beside it does not."""
    if width <= 0:
        return []
    if done:                                    # spent, complete, and wordless
        return _right([(ch, "ash") for ch in "done"], width, "ash")
    if task_or_lane_days is None:               # no date: nothing to measure
        return _right([("—", "dim")], width, "dim")
    d = task_or_lane_days
    if d < 0:
        # the cap wears the severity hue; the number beside it stays neutral, so
        # `over` keeps meaning exactly one thing on this row
        return _right([("▲", "over")] + [(ch, "mut") for ch in _days(-d, width - 1)],
                      width)
    if d == 0:
        return _right([(ch, "accent") for ch in "today"], width)
    return _right([(ch, "mut") for ch in _days(d, width)], width)


def _days(n: int, room: int) -> str:
    """`Nd`, and it never silently truncates: a distance too wide for the edge
    comes back capped with a `+` so the reading stays true rather than short."""
    text = f"{n}d"
    if len(text) <= room:
        return text
    cap = 10 ** max(1, room - 2) - 1            # room for the digits, 'd' and '+'
    return f"{cap}d+"




def meter_markup(cells: list[tuple[str, str]]) -> str:
    return "".join(c(g, tone) for g, tone in cells)


def lane_due_days(lane: LaneFacts) -> int | None:
    """What the lane's meter measures: its own due date if it has one, else the
    soonest thing it still owes."""
    if lane.due_in is not None:
        return lane.due_in
    return None


def _figures(lane: LaneFacts, width: int) -> str:
    """The row's right edge: the due meter, and nothing else.

    `n/N` is gone at the root — the project's own wave already draws its
    progress, and a figure repeating the field beside it is exactly the
    duplication this edge exists to remove. `!N` moved to the leader's band,
    where a digit earns its cells."""
    if width <= 0:
        return ""
    # A CLOSED project is never judged — nothing is expected of it, so nothing
    # about it can be late. Its edge is the spent form whatever its dates say.
    cells = due_meter(None if lane.closed else lane_due_days(lane),
                      done=lane.closed, width=min(METER_W, width))
    pad = " " * max(0, width - len(cells))
    return pad + meter_markup(cells)


def _lane_label(lane: LaneFacts, label_w: int) -> str:
    """Spine · name · status mark, in exactly `label_w` cells."""
    if label_w < 6:
        return c(fit("▎" + lane.name, label_w), lane.hue)
    body = fit(clip(lane.name, label_w - 5), label_w - 5)
    return (c("▎", lane.hue) + " " + c(escape(body), lane.hue) + " "
            + c(STATUS_MARK.get(lane.status, " "), "dim") + " ")


def _scale_row(geo: FieldGeo, inner: int) -> str:
    """The axis says what it measures — without it the field is a stripe.
    Exactly `inner` cells."""
    span = geo.field_w
    body = [" "] * span
    left, right = f"-{geo.today_dc}d", f"+{geo.dot_w - 1 - geo.today_dc}d"

    def place(text: str, at: int) -> None:
        for i, ch in enumerate(text):
            if 0 <= at + i < span:
                body[at + i] = ch

    # Labels are dropped whole rather than allowed to collide: two numbers run
    # together ("-8today") is worse than one number missing.
    mid = geo.today_dc // 2 - 2
    if 0 <= mid and mid + 5 <= span:
        place("today", mid)
        if len(left) < mid:
            place(left, 0)
        if span - len(right) >= mid + 6:
            place(right, span - len(right))
    elif len(left) + len(right) + 1 <= span:
        place(left, 0)
        place(right, span - len(right))
    return (" " * geo.label_w + c("".join(body), "dim")
            + " " * max(0, inner - geo.label_w - span))


def wave_edge(lane: LaneFacts, geo: FieldGeo, today: date) -> int:
    """The last dot column the bank may occupy: the project's OWN due date.
    Past it there is no more life to spend, so a plateau running to the right
    edge would be saying nothing."""
    if lane.due_in is not None:
        col = day_col(today + timedelta(days=lane.due_in), today, geo)
        edge = col[1] if isinstance(col, tuple) else col
    else:
        dues = [day_col(d, today, geo) for d in
                (parse_iso(t.due_date) for t in lane.open) if d]
        edge = max((cl[1] if isinstance(cl, tuple) else cl for cl in dues),
                   default=geo.today_dc)
    return max(geo.today_dc, min(max(0, geo.dot_w - 1), edge))


def project_wave(lane: LaneFacts, geo: FieldGeo, today: date, rows: int,
                 carve_count: bool = False) -> Bitmap:
    """The project's own cumulative bank, with time CARVED into it: a notch per
    day that fell due and did not land, and today as a hole through every wave.

    `carve_count` cuts the open count out of the field as digits — a figure the
    field gives up, never a label printed on top of it."""
    bm = Bitmap(geo.dot_w, rows * DOT_ROWS)
    cols = []
    for t in lane.open:
        d = parse_iso(t.due_date)
        if d is None:
            continue
        col = day_col(d, today, geo)
        cols.append(col[1] if isinstance(col, tuple) else col)
    steps = [sum(1 for cl in cols if cl <= x) for x in range(geo.dot_w)]
    edge = wave_edge(lane, geo, today)
    load_curve(bm, steps, max(1, lane.total), edge)
    for t in lane.late:
        col = day_col(parse_iso(t.due_date), today, geo)
        bm.carve_notch(col[1] if isinstance(col, tuple) else col, 2)
    if carve_count and rows >= 3 and lane.open:
        txt = str(len(lane.open))
        gw = len(txt) * 5
        x = max(geo.today_dc + 2, edge - gw - 1)
        if bm.ink_at(x) >= 7:                  # only carve where there IS field
            bm.carve_text(txt, x, (bm.h - 7) // 2)
    bm.carve_col(geo.today_dc)
    return bm


def _off_window(lane: LaneFacts, geo: FieldGeo, today: date) -> tuple[bool, bool]:
    """Does this project have work the window cannot show? Marked, never crushed."""
    left = right = False
    dates = [d for d in (parse_iso(t.due_date) for t in lane.open) if d]
    if lane.due_in is not None:
        dates.append(today + timedelta(days=lane.due_in))
    for d in dates:
        flag = off_window_glyph(day_col(d, today, geo))
        left = left or flag == OFF_LEFT
        right = right or flag == OFF_RIGHT
    return left, right


LANE_TITLES = 2      # the allocator's default when no height is known


def lane_geometry(inner: int, height: int) -> FieldGeo:
    """`field_geometry` is a faithful port and its `field_w` has a floor of 8,
    so below 32 columns its parts add up to more than the width. The VIEW is
    the place that has to fit: here the label and figures give way first, and
    the field takes exactly what is left."""
    g = field_geometry(inner, height)
    label_w = min(g.label_w, max(6, inner // 3))
    # THE BAND THE METER FREED. The port reserves 13 (L) / 11 (S) for the old
    # `n/N !N ▲Nd` group; the meter needs six cells and a space, and the rest
    # goes to the field — measured at +6 cells (L) and +4 (S).
    figs_w = min(METER_W + 1, max(4, inner // 3))
    field_w = max(0, inner - label_w - figs_w - 1)
    if (label_w, figs_w, field_w) == (g.label_w, g.figs_w, g.field_w):
        return g
    dot_w = field_w * 2
    today_dc = (int(dot_w * 0.30) // 2) * 2
    return g._replace(label_w=label_w, figs_w=figs_w, field_x=label_w,
                      field_w=field_w, dot_w=dot_w, today_dc=today_dc,
                      today_cell=label_w + today_dc // 2)


def _pad(markup: str, width: int) -> str:
    """Pad a composed row out to `width` visible cells. Never truncates: every
    piece is built to its own exact width, so a short row is a rounding gap and
    a long one is a bug the width tests must catch, not hide."""
    return markup + " " * max(0, width - vis(_strip(markup)))


Row = tuple[str, "str | None"]      # (markup, the task this row names)


def lattice_tail(geo: FieldGeo, from_col: int, to_col: int, phase: int = 0) -> str:
    """The field's own lattice, drawn behind a row that is mostly text.

    NAMING WAS COSTING EMPTINESS: a title row was nearly blank while a field row
    is lattice, so trading field rows for title rows RAISED dead space — the
    ladder was right and the result was worse. The cure is that a named row
    carries the field too, on the same geometry.

    It also buys something nobody asked for: the today boundary becomes ONE
    CONTINUOUS VERTICAL LINE down the whole panel instead of appearing only on
    the rows that draw a wave."""
    out = []
    rule_col = geo.label_w + geo.today_dc // 2
    for col in range(max(geo.label_w, from_col), max(geo.label_w, to_col)):
        i = col - geo.label_w
        if col == rule_col:
            out.append(c(RULE_PHASES[phase % len(RULE_PHASES)], "accent"))
        else:
            past = (2 * i + 1) < geo.today_dc
            out.append(c(LATTICE, "ash" if past else "dim"))
    return "".join(out)


def _title_row(task: Task, board: Board, lane: LaneFacts, today: date,
               inner: int, selected: bool, geo: FieldGeo) -> Row:
    """A named task: spine, its phase glyph, its title — and the FIELD behind
    the tail, which is what keeps naming from costing emptiness."""
    due = parse_iso(task.due_date)
    days = (due - today).days if due else None
    # archived work is SPENT: its meter is the spent form and its title drops to
    # the spent tone, so a row that is not live work never reads as live work
    cells = due_meter(None if task.archived else days,
                      done=board.is_done(task) or task.archived)
    title_w = max(0, inner - 5 - len(cells) - 1)
    shown = clip(task.title, title_w)
    body = escape(shown)
    if selected:
        body = f"[reverse]{body}[/reverse]"
    tail_from = 5 + vis(shown)
    tail_to = max(tail_from, inner - len(cells) - 1)
    gap = " " * max(0, min(geo.label_w, tail_to) - tail_from)
    glyph, gcol = ((ARCHIVED_MARK, "ash") if task.archived
                   else (phase_glyph({min(3, board.phase_index(task))}), lane.hue))
    return ((c("▎", "ash" if task.archived else lane.hue) + "  "
             + c(glyph, gcol) + " "
             + c(body, "ash" if task.archived else "mut") + gap
             + lattice_tail(geo, tail_from, tail_to) + " "
             + meter_markup(cells)), task.id)


def stack_block(lane: LaneFacts, geo: FieldGeo, board: Board, today: date,
                inner: int, titles: int, wrows: int, selected_id,
                phase: int = 0) -> list[Row]:
    """A project: its own wave in its own hue, then its next-due work named."""
    offl, offr = _off_window(lane, geo, today)
    field = field_rows(project_wave(lane, geo, today, wrows), geo, lane.hue,
                       off_left=offl, off_right=offr, phase=phase)
    gap = " " * max(0, inner - geo.label_w - geo.field_w - geo.figs_w)
    rows: list[Row] = [(_lane_label(lane, geo.label_w) + field[0] + gap
                        + _figures(lane, geo.figs_w), None)]
    for extra in field[1:]:
        rows.append((c("▎", lane.hue) + " " * (geo.label_w - 1) + extra, None))
    for t in lane_titles(lane, titles):
        rows.append(_title_row(t, board, lane, today, inner,
                               t.id == selected_id, geo))
    return rows


def resting_row(lane: LaneFacts, geo: FieldGeo, inner: int) -> Row:
    """Nothing open. This is the state a repeated element spends most of its
    life in, so it is DESIGNED rather than inherited: a thin spine, everything
    on the quiet step, no field — and it still says what it is."""
    word = {"completed": "completed", "cancelled": "cancelled",
            "paused": "paused"}.get(lane.status, "nothing open")
    body = list(" " * geo.field_w)
    for i in range(0, geo.field_w, 2):
        body[i] = LATTICE
    done = f" {lane.done_n}/{lane.total} done "
    body[:len(done)] = list(done[:geo.field_w])
    label = (c("▏", "dim") + " " + c(escape(fit(clip(lane.name, geo.label_w - 5),
                                                geo.label_w - 5)), "mut") + " "
             + c(STATUS_MARK.get(lane.status, " "), "dim") + " ")
    # A resting row carries NO meter, so its word is not squeezed into the six
    # cells the meter would have taken — it is right-aligned across everything
    # the row has left. (`completed` is 9 characters; the band is 7.)
    span = max(0, inner - geo.label_w)
    body = set_cell_size("".join(body[:geo.field_w]), max(0, span - vis(word) - 1))
    return (label + c(body, "dim") + " " * max(0, span - vis(body) - vis(word))
            + c(word, "dim"), None)


def sitting(lane: LaneFacts, today: date) -> str:
    """How long the lead's most stagnant open task has sat in its phase.

    THE ONE HONEST FORM THIS CAN TAKE. The board stores a phase-change date
    only from the moment that field existed, so a task that has never moved
    since has no age — and `views.py` already ruled for the gantt that a figure
    the data cannot support must not be invented. So: a number only when every
    named-in-this-figure task is dated, and the word `unaged` when the board
    simply does not know. Never a zero standing in for a blank."""
    if not lane.open:
        return ""
    ages = [days_in_phase(t, today) for t in lane.open]
    known = [a for a in ages if a is not None]
    if not known:
        return "unaged"
    worst = max(known)
    unknown = len(ages) - len(known)
    return f"{worst}d in phase" + (f" · {unknown} unaged" if unknown else "")


def _rights_w(rights: list[tuple[str, str]]) -> int:
    """Visible width of a right-hand block joined by two spaces."""
    return sum(len(t) for t, _ in rights) + 2 * max(0, len(rights) - 1)


def lead_band(lane: LaneFacts, geo: FieldGeo, today: date, inner: int,
              prof: int, phase: int = 0) -> list[Row]:
    """The one project that needs you now, given a DRAWN, CARVED field: its own
    bank several rows tall, ending in `◆` — its own due date — so the air left
    ABOVE the curve before that diamond is the work that cannot land in time."""
    chip, chip_key = pressure_chip(lane)
    # The head is width-exact by construction, and it sheds from the LEFT of the
    # right-hand block: momentum goes first (it is context), then the open count,
    # and the chip goes last because it is the only one that says anything is
    # wrong. [PROPOSAL 4.2, the order of loss]
    rights = [(t, k) for t, k in ((sitting(lane, today), "dim"),
                                  (f"!{lane.high}" if lane.high else "", "ink"),
                                  (f"{len(lane.open)} open", "mut"),
                                  (chip, chip_key)) if t]
    while rights and 2 + 4 + _rights_w(rights) > inner:
        rights.pop(0)
    rw = _rights_w(rights)
    name_w = max(0, inner - 3 - rw)
    shown = clip(lane.name.upper(), name_w)
    # the hero's own row carries the field too, so the today line runs the FULL
    # height of the panel rather than stopping just below the top
    head_w = 2 + vis(shown)
    tail_to = max(head_w, inner - rw - 1)
    gap = " " * max(0, min(geo.label_w, tail_to) - head_w)
    head = (c("▌ ", lane.hue) + c(escape(shown), lane.hue, bold=True) + gap
            + lattice_tail(geo, head_w, tail_to) + " "
            + "  ".join(c(t, k) for t, k in rights))
    rows: list[Row] = [(head, None)]

    bm = project_wave(lane, geo, today, prof, carve_count=True)
    offl, offr = _off_window(lane, geo, today)
    field = field_rows(bm, geo, lane.hue, off_left=offl, off_right=offr,
                       phase=phase)
    edge_cell = min(geo.field_w - 1, wave_edge(lane, geo, today) // 2 + 1)
    for i, row in enumerate(field):
        body = row
        if i == 0 and 0 <= edge_cell < geo.field_w:
            body = _put_cell(row, edge_cell, c("◆", lane.hue))
        rows.append((" " * geo.label_w + body, None))

    # the lead's tail NAMES a task, so it carries the field behind it too —
    # otherwise it is the one row that breaks the today line
    if lane.late:
        worst = sorted(lane.late, key=lambda t: parse_iso(t.due_date))[0]
        d = (today - parse_iso(worst.due_date)).days
        tok, tid = f"▲{d}d", worst.id
        label = escape(clip(worst.title, max(0, inner - vis(tok) - 4)))
        shown, tone = label, "mut"
    else:
        tok, tid = "", None
        shown, tone = escape("nothing late"), "dim"
    head_w = 2 + vis(_strip(shown))
    tail_to = max(head_w, inner - vis(tok) - 1)
    gap = " " * max(0, min(geo.label_w, tail_to) - head_w)
    rows.append(("  " + c(shown, tone) + gap
                 + lattice_tail(geo, head_w, tail_to) + " "
                 + (c(tok, "over") if tok else ""), tid))
    return rows


def _put_cell(row_markup: str, index: int, replacement: str) -> str:
    """Swap ONE visible cell of an already-composed row. The field is built as
    `[hex]x[/]` segments of one cell each, so a cell is a segment."""
    parts = row_markup.split("[/]")
    if 0 <= index < len(parts) - 1:
        parts[index] = replacement.rsplit("[/]", 1)[0]
    return "[/]".join(parts)


def absence_line(lanes: list[LaneFacts], today: date, inner: int) -> str:
    """STEP 3 OF THE SPEND LADDER: when naming is exhausted and resolution is
    bought, the cells left say WHAT IS NOT THERE.

    A calm board is not an empty screen — it is a board with little to report,
    and the difference has to be stated. Every clause is a fact about the world
    (`nothing late`), never about the reader and never a compliment."""
    n_p = len(lanes)
    open_n = sum(len(ln.open) for ln in lanes)
    late = sum(len(ln.late) for ln in lanes)
    week = sum(1 for ln in lanes for t in ln.open
               if (d := parse_iso(t.due_date)) and 0 <= (d - today).days <= 7)
    parts = [f"{n_p} project{'s' if n_p != 1 else ''}",
             f"{open_n} open" if open_n else "nothing open",
             f"{late} late" if late else "nothing late",
             f"{week} due this week" if week else "nothing due this week"]
    body = " · ".join(parts)
    if vis(body) + 4 > inner:
        return ""
    pad = (inner - vis(body) - 4) // 2
    return (" " * pad + c("· ", "frame") + c(body, "mut") + c(" ·", "frame"))


def render_swimlanes(board, show_archived, selected_id, today=None,
                     width=68, height=0, line_map=None, tick=0) -> Text:
    """Lanes: projects RANKED by pressure on one shared axis of days. The one
    that needs you now gets a drawn field; the rest get a row each; the ones
    with nothing open rest at the bottom. Nothing is ever dropped in silence —
    what does not fit is counted."""
    today = today or date.today()
    w = _clamp_width(width)
    inner = w
    h = height or 24
    lanes, geo, titles, prof, wrows = swimlane_plan(
        board, show_archived, today, w, h)

    tasks = board.visible_tasks(show_archived)
    # the same law the lanes obey: archived work is not open and is never due,
    # so pressing `v` may not change what the header says is still to do
    live = [t for t in tasks if not t.archived]
    open_n = sum(1 for t in live if not board.is_done(t))
    due_n = sum(1 for t in live if urgency(t, today, board) in ("overdue", "today"))
    right = c(f"{open_n} open · ", "mut") + c(f"{due_n} due", "over", bold=True)
    lines = [header(c("◆ TASKBOARD", "accent", bold=True), right, w)]

    if not lanes:
        lines.append(line(c(fit("  (no projects — press 'p' to add one)", inner), "dim")))
        lines.append(line(_pad(_scale_row(geo, inner), inner)))
        lines.append(bottom(None, w))
        return to_text(lines, height, w)

    active = [ln for ln in lanes if not ln.resting]
    resting = [ln for ln in lanes if ln.resting]
    stack = active[1:]

    blocks: list[list[Row]] = []
    if active:
        blocks.append(lead_band(active[0], geo, today, inner, prof, tick))
    blocks += [stack_block(ln, geo, board, today, inner, titles, wrows,
                           selected_id, tick)
               for ln in stack]
    blocks += [[resting_row(ln, geo, inner)] for ln in resting]

    body: list[Row] = []
    shed = 0
    for i, blk in enumerate(blocks):
        if len(body) + len(blk) > max(0, h - 2):
            shed = len(blocks) - i
            break
        body += blk

    for markup, tid in body:
        lines.append(line(_pad(markup, inner)))
        if tid is not None and line_map is not None:
            line_map[tid] = len(lines) - 1

    # the ladder's third step, and only when the first two are exhausted:
    # nothing was shed, and there are cells the body did not want
    if not shed and h - len(lines) - 2 >= 0:
        absence = absence_line(lanes, today, inner)
        if absence:
            lines.append(line(_pad(absence, inner)))
    scale = (_scale_with_note(geo, inner, f"+{shed} not shown") if shed
             else _scale_row(geo, inner))
    lines.append(line(_pad(scale, inner)))
    lines.append(bottom(None, w))
    return to_text(lines, height, w)


def _scale_with_note(geo: FieldGeo, inner: int, note: str) -> str:
    """The axis, plus what the height could not show. A view that drops rows in
    silence is lying about how much work there is."""
    base = set_cell_size(_strip(_scale_row(geo, inner)), max(0, inner - vis(note) - 1))
    return c(base, "dim") + " " * max(0, inner - vis(base) - vis(note)) + c(note, "mut")


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
    """A due dot-plot: every task with a due date is a ● on ONE shared day-axis
    (1 cell = 1 day) with a full-height teal today rule ┃. Distance from the rule
    is urgency; a vertical stack of dots at one column is a crunch day. Rows are
    sorted by due, so no OVERDUE/TODAY/THIS-WEEK sub-headers are needed. Tasks
    with no due date collect under a 'no date' group at the bottom."""
    today = today or date.today()
    w = _clamp_width(width)
    inner = w

    tasks = board.visible_tasks(show_archived)
    # archived work is never overdue and never due today: nothing is expected of
    # it, so pressing `v` may not change what this header says is wrong
    judged = [t for t in tasks if not t.archived]
    overdue_n = sum(1 for t in judged if agenda_bucket(t, today) == "overdue")
    today_n = sum(1 for t in judged if agenda_bucket(t, today) == "today")
    right = (c(f"▲ {overdue_n} overdue", "over", bold=True) + c(" · ", "mut")
             + c(f"{today_n} today", "soon"))
    lines = [header(c("AGENDA", "accent", bold=True), right, w)]

    dated = sort_by_due([t for t in tasks if parse_iso(t.due_date) is not None])
    undated = [t for t in tasks if parse_iso(t.due_date) is None]

    # geometry: a row is chip(2) title(TW) proj(8) state(1) axis(AX) due(6) with
    # single-space gaps (21 fixed cells); TW + AX share the rest. Below ~budget 20
    # there is no room for a usable axis, so fall back to a compact chip+title row.
    PROJ_W, DUE_W = 8, 6
    budget = inner - 21
    axis_w = max(12, min(44, (budget * 6) // 10)) if budget >= 20 else 0
    title_w = budget - axis_w
    compact = axis_w < 12 or title_w < 8
    today_col = max(1, min(axis_w - 2, round((axis_w - 1) * 14 / 43))) if not compact else 0

    def cells_markup(cells: list[tuple[str, str | None]]) -> str:
        """Merge a per-cell [(char, color-key|None), ...] list into markup,
        coalescing runs of the same colour. Visible width == len(cells)."""
        sentinel = object()
        out: list[str] = []
        run: list[str] = []
        key: object = sentinel
        for ch, k in cells:
            if k == key:
                run.append(ch)
            else:
                if run:
                    s = escape("".join(run))
                    out.append(s if key is None else c(s, key))  # type: ignore[arg-type]
                run, key = [ch], k
        if run:
            s = escape("".join(run))
            out.append(s if key is None else c(s, key))  # type: ignore[arg-type]
        return "".join(out)

    _DOT_KEY = {"overdue": "over", "today": "soon", "week": "hd",
                "later": "hd", "done": "done"}

    def axis_markup(t: Task, has_due: bool) -> str:
        cells: list[tuple[str, str | None]] = [(" ", None)] * axis_w
        cells[today_col] = ("┃", "accent")           # teal rule, every row, one column
        if has_due:
            delta = (parse_iso(t.due_date) - today).days
            col = today_col + delta
            clamp_l, clamp_r = col < 0, col > axis_w - 1
            col = max(0, min(axis_w - 1, col))
            lo, hi = (col, today_col) if col < today_col else (today_col, col)
            for i in range(lo + 1, hi):               # thin tail rule->dot (not the rule)
                if cells[i][0] == " ":
                    cells[i] = ("─", "dim")
            glyph = "◂" if clamp_l else "▸" if clamp_r else "●"
            cells[col] = (glyph, _DOT_KEY[urgency(t, today, board)])
        return cells_markup(cells)

    def due_tok(t: Task) -> tuple[str, str]:
        if t.archived:
            return "archived", "ash"      # spent: it reports no distance to a date
        if board.is_done(t):
            return "done", "done"
        txt, col = reldue_token(t, today, board)
        return (txt, col) if txt else ("—", "dim")

    def row_markup(t: Task, has_due: bool) -> str:
        sel = t.id == selected_id
        pcol = project_color(board, t)
        dtxt, dcol = due_tok(t)
        if compact:                                   # narrow: chip + title + due
            return (c("▊", pcol) + " " + title_markup(t, inner - 9, sel) + " "
                    + c(fit(dtxt, DUE_W, "right"), dcol))
        p_obj = board.project_by_id(t.project_id)
        pname = p_obj.name if p_obj else "Inbox"
        sg, sgcol = status_glyph(board, t)
        return (c("▊", pcol) + " " + title_markup(t, title_w, sel) + " "
                + c(escape(fit(pname, PROJ_W)), "dim") + " "
                + c(sg, sgcol) + " " + axis_markup(t, has_due) + " "
                + c(fit(dtxt, DUE_W, "right"), dcol))

    if not compact and (dated or undated):            # a small date scale over the axis
        scale: list[tuple[str, str | None]] = [(" ", None)] * axis_w

        def put(idx: int, text: str, k: str) -> None:
            for j, ch in enumerate(text):
                if 0 <= idx + j < axis_w:
                    scale[idx + j] = (ch, k)

        put(0, f"-{today_col}d", "mut")
        rlbl = f"+{axis_w - 1 - today_col}d"
        put(axis_w - len(rlbl), rlbl, "mut")
        if axis_w >= 24:
            put(max(0, today_col - 2), "today", "accent")
        lines.append(line(" " * (title_w + 14) + cells_markup(scale) + " " * 7))

    for t in dated:
        lines.append(line(row_markup(t, True)))
        if line_map is not None:
            line_map[t.id] = len(lines) - 1

    if undated:
        label = " no date "
        lines.append(line(c(label, "dim")
                          + c("─" * max(0, inner - vis(label)), "frame")))
        for t in undated:
            lines.append(line(row_markup(t, False)))
            if line_map is not None:
                line_map[t.id] = len(lines) - 1

    if not dated and not undated:
        lines.append(line(c(fit("  (nothing scheduled — press 'a' to add a task)", inner), "dim")))
    lines.append(bottom(None, w))
    return to_text(lines, height, w)


# ---------------------------------------------------------------------------
# view: GANTT  (weeks as columns; project + task bars; today marker)
# ---------------------------------------------------------------------------
BAR_DONE = "⣿"     # 8/8 dots — the completed share of a project's span
BAR_TODO = "⢕"     # 4/8 dots — the remaining share; same family, same height

# --------------------------------------------------------------------------- #
# the GANTT FIELD's texture — shade, not scatter
# --------------------------------------------------------------------------- #
# The field used braille for its bars: reach 8/8 `⣿`, progress 4/8 `⣤`, a task
# 2/8 `⣀`. Braille buys SUB-CELL RESOLUTION, and a curve needs it — which is why
# the lanes wave keeps it. A gantt bar is a SPAN: it has a start, an end, and
# nothing in between to resolve. So the field was paying braille's scatter and
# buying nothing with it, and the row that pays most is the task row, the most
# numerous one on screen: 2 dots of 8 read as a dotted line, not as duration.
#
# Shade blocks cover the whole cell, so a bar reads as one continuous run, and
# they keep the three-weight hierarchy the design encodes (reach > progress >
# task) as three densities instead of three dot-counts. Vocabulary borrowed from
# s19_app's bands (`█` filled / `░` gap / the ▁▂▃▄▅▆▇█ ramp).
#
# `FIELD_HALF` keeps the half-day precision the braille caps carried: a bar that
# ends mid-cell still says so.
FIELD_REACH = "█"     # a project's span            (was ⣿)
FIELD_PROGRESS = "▓"  # how far the work actually got (was ⣤)
FIELD_TASK = "▒"      # a task's reach              (was ⣀)
FIELD_HALF = "▌"      # ends mid-cell               (was ⡄)

# The tip that says WHICH PHASE the task is in, in the field's own alphabet.
# `phase_glyph` keeps encoding phase as a CLIMBING DOT — it is still right for
# the lanes, where one cell must carry a SET of phases and dots can be OR'd
# together. A gantt bar carries exactly one, and a braille dot at the end of a
# shaded run reads as the bar fading out rather than as its tip. Same meaning,
# rising fill instead of climbing dot, so the tip belongs to the bar it ends.
# The floor is 3/8, not 1/8: a tip lighter than the bar it ends reads as the
# bar fading out, which is the exact complaint this whole change answers. The
# ceiling stops below `█` so the tip can never be mistaken for a reach cell.
FIELD_PHASE_TIP = ("▃", "▅", "▆", "▇")


def gantt_tasks(board: Board, tasks: list[Task], project_id: str | None) -> list[Task]:
    """One project's tasks in the order the gantt lists them: WORK STILL OPEN
    FIRST, finished work at the tail, each group by due date (soonest first,
    undated last).

    Was: raw board order, so a task finished in May sat between two live ones.
    The renderer and `nav_model` both call this, so the cursor cannot walk an
    order the screen does not show."""
    rows = [t for t in tasks if t.project_id == project_id]
    return (sort_by_due([t for t in rows if not board.is_done(t)])
            + sort_by_due([t for t in rows if board.is_done(t)]))


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


def _gantt_day_col(d, chart_start, weeks, cell):
    """Column of date `d` INSIDE the timeline grid (0-based), reusing the same
    week/day math as `week_index`. Returns an int when `d` is on-screen, a
    ('clampL'|'clampR', col) tuple when it falls off the left/right edge, or
    None when there is no date."""
    if d is None:
        return None
    days = (d - chart_start).days
    wk = days // 7
    if wk < 0:
        return ("clampL", 0)
    if wk >= weeks:
        return ("clampR", weeks * cell - 1)
    dow = days - wk * 7                       # 0..6 within the week
    return wk * cell + min(cell - 1, dow * cell // 7)


def _overlay_cells(markup: str, width: int, cells: dict[int, str]) -> str:
    """Overwrite specific VISIBLE columns of a markup string in place.

    `markup` renders to exactly `width` cells; `cells` maps {visible_col:
    replacement_markup} where each replacement is balanced, single-cell markup.
    The replacement is injected in place of the character at that column, so the
    total visible width never changes (this is what keeps every gantt row
    width-exact). Rich's style stack makes an inner `[c]…[/]` inside an outer
    span reopen the outer colour after it closes, so overwriting a coloured bar
    cell is safe."""
    if not cells:
        return markup
    out, vis, i, n = [], 0, 0, len(markup)
    while i < n:
        ch = markup[i]
        if ch == "\\" and i + 1 < n and markup[i + 1] == "[":   # escaped literal '['
            out.append(cells.get(vis, markup[i:i + 2]))
            i, vis = i + 2, vis + 1
        elif ch == "[":                                          # a markup tag (0 width)
            j = markup.index("]", i)
            out.append(markup[i:j + 1])
            i = j + 1
        else:                                                    # one visible char
            out.append(cells.get(vis, ch))
            i, vis = i + 1, vis + 1
    return "".join(out)


def _flowing(board: Board, task: Task) -> bool:
    """A task is "in progress" — worth animating a flow packet on — when it
    has left the first phase, is not done, and is not blocked."""
    # and NOT archived: a bar that animates is claiming to be work in motion,
    # which is the one thing put-away work is not
    return (not board.is_done(task) and not task.blocked and not task.archived
            and board.phase_index(task) > 0)


def _span_bands(project, geo: FieldGeo, today: date, hue: str,
                progress: float) -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    """THE SPAN IS THE WAVE, in two bands, and the answer a gantt exists to give
    comes out of the DIFFERENCE between them.

    top    — the span from start to `◆`: ASH for what has elapsed, the project's
             own hue for what remains. The old view already measured "how much
             of the span is gone" and this language already paints "spent": same
             cut, no new mechanism.
    bottom — how far the work actually got.

    So THE GAP BETWEEN THE TWO FRONTIERS IS THE SLIP, read as a length. "Am I
    behind?" is the question a gantt is for, and the old one could not answer it.
    """
    span = [(" ", "dim")] * geo.field_w
    band = [(" ", "dim")] * geo.field_w
    s = parse_iso(project.start_date)
    e = parse_iso(project.due_date)
    if s is None and e is None:
        return span, band

    def cell_of(d: date) -> tuple[int, bool]:
        col = day_col(d, today, geo)
        flagged = isinstance(col, tuple)
        dc = col[1] if flagged else col
        return min(geo.field_w - 1, max(0, dc // 2)), flagged

    c0, l_off = cell_of(s or today)
    c1, r_off = cell_of(e or today)
    if c1 < c0:
        c0, c1 = c1, c0
    today_cell = geo.today_dc // 2
    for x in range(c0, c1 + 1):
        span[x] = (FIELD_REACH, "ash" if x < today_cell else hue)
    if e is not None and not r_off:
        span[c1] = ("◆", hue)
    if l_off:
        span[0] = (OFF_LEFT, "mut")
    if r_off:
        span[geo.field_w - 1] = (OFF_RIGHT, "mut")

    reached = c0 + int(round((c1 - c0) * max(0.0, min(1.0, progress))))
    for x in range(c0, min(reached, geo.field_w)):
        band[x] = (FIELD_PROGRESS, hue)
    if reached > c0:
        band[min(reached, geo.field_w - 1)] = (FIELD_HALF, hue)
    return span, band


def _reach_start(task: Task, geo: FieldGeo, today: date) -> int:
    """The first field cell this task's reach occupies — everything left of it
    is empty field the TITLE may spend (REV5 #19's ruling, kept)."""
    s = parse_iso(task.start_date)
    e = parse_iso(task.due_date)
    if s is None and e is None:
        return geo.field_w

    def cell_of(d):
        col = day_col(d, today, geo)
        dc = col[1] if isinstance(col, tuple) else col
        return min(geo.field_w - 1, max(0, dc // 2))

    return min(cell_of(s or today), cell_of(e or today))


def _task_reach(task: Task, board: Board, geo: FieldGeo, today: date,
                hue: str, tick: int | None = None) -> list[tuple[str, str]]:
    """A task is a REACH of variable length with its phase glyph at the tip —
    not a five-cell slab. A mark that cannot vary is not a datum (DATAVIZ 13,
    which the old week-resolution bar violated: two different tasks drew the
    same `▬▬▬▬▬`)."""
    cells = [(" ", "dim")] * geo.field_w
    s = parse_iso(task.start_date)
    e = parse_iso(task.due_date)
    if e is None and s is None:
        return cells

    def cell_of(d: date) -> int:
        col = day_col(d, today, geo)
        dc = col[1] if isinstance(col, tuple) else col
        return min(geo.field_w - 1, max(0, dc // 2))

    a = cell_of(s or today)
    b = cell_of(e or today)
    if b < a:
        a, b = b, a
    done = board.is_done(task)
    tone = "ash" if done else hue
    for x in range(a, b):
        cells[x] = (FIELD_TASK, tone)
    cells[b] = (FIELD_PHASE_TIP[min(3, board.phase_index(task))], tone)
    if not done and tick is not None and b > a and _flowing(board, task):
        # THE FLOW PACKET, kept from the shipped gantt: work drifts toward its
        # deadline. It rides the task's own reach now instead of a week slab.
        cells[a + (tick % max(1, b - a))] = ("▬", "bright")
    return cells


def _band_markup(cells: list[tuple[str, str]], geo: FieldGeo, phase: int = 0,
                 lattice: bool = True, offset: int = 0) -> str:
    """Cells to markup, over the field's own lattice — ash behind today, dim
    ahead — with the today rule where nothing else is drawn."""
    out = []
    for j, (glyph, tone) in enumerate(cells):
        i = j + offset
        past = (2 * i + 1) < geo.today_dc
        if glyph == " ":
            if i == geo.today_dc // 2:
                out.append(c(RULE_PHASES[phase % len(RULE_PHASES)], "accent"))
            elif lattice:
                out.append(c(LATTICE, "ash" if past else "dim"))
            else:
                out.append(" ")
        else:
            out.append(c(glyph, tone))
    return "".join(out)


def gantt_geometry(inner: int, height: int) -> FieldGeo:
    """The lanes geometry, with a wider figures band: the gantt's project row
    carries its progress percent BESIDE the meter, so it needs the percent's
    cells plus the meter's six. Lanes needs only the meter."""
    g = lane_geometry(inner, height)
    want = METER_W + 5                       # ' 20%' + gap + the six-cell meter
    figs_w = min(want, max(g.figs_w, inner // 5))
    field_w = max(0, inner - g.label_w - figs_w - 1)
    dot_w = field_w * 2
    today_dc = (int(dot_w * 0.30) // 2) * 2
    return g._replace(figs_w=figs_w, field_w=field_w, dot_w=dot_w,
                      today_dc=today_dc, today_cell=g.label_w + today_dc // 2)


def render_gantt(board, show_archived, selected_id, today=None,
                 width=68, height=0, line_map=None, tick=0) -> Text:
    """The gantt on the shared day axis: one cell is two days, and the axis
    INCLUDES THE PAST.

    The old view started its axis on Monday of this week, so a project already
    overdue drew as an empty row with a `◂` — and the more overdue work a board
    held, the emptier the view got. That is why it was the one view where MORE
    data produced LESS used screen (ink fell 23.3 % -> 21.0 % from typical to
    extreme). An axis with a past is the fix.
    """
    today = today or date.today()
    w = _clamp_width(width)
    inner = w
    h = height or 24
    geo = gantt_geometry(inner, h)

    tasks = board.visible_tasks(show_archived)
    late_n = sum(1 for t in tasks
                 if (d := parse_iso(t.due_date)) and d < today and not board.is_done(t))
    right = (c(f"▲{late_n} past due", "over", bold=True) if late_n
             else c("nothing past due", "dim"))
    lines = [header(c("◆ GANTT", "accent", bold=True), right, w)]

    def band_row(prefix: str, cells: list[tuple[str, str]], figures: str,
                 offset: int = 0) -> str:
        # label + field + ONE gap + figures == inner, so the figures stay flush
        # right; without the gap `_pad` appended it and the meter drifted left
        return _pad(prefix + _band_markup(cells, geo, 0, offset=offset)
                    + " " + figures, inner)

    archived_done = sum(1 for t in board.visible_tasks(True)
                        if t.archived and board.is_done(t))
    rows: list[Row] = []
    for p in board.visible_projects(show_archived):
        own = gantt_tasks(board, tasks, p.id)
        prog = board.project_progress(p.id, show_archived)
        span, band = _span_bands(p, geo, today, p.color, prog)
        label = c("▎ ", p.color) + c(escape(fit(clip(p.name, geo.label_w - 2),
                                                geo.label_w - 2)), p.color, bold=True)
        pct = f"{int(round(100 * prog))}%"
        pct_w = max(0, geo.figs_w - METER_W)
        pct = pct if pct_w >= len(pct) else ""      # it drops whole, never "…"
        meter = meter_markup(due_meter(days_until(p.due_date, today),
                                       done=p.status == "completed",
                                       width=min(METER_W, geo.figs_w)))
        rows.append((band_row(label, span,
                              c(fit(pct, pct_w, "right"), "mut") + meter), None))
        rows.append((band_row(" " * geo.label_w, band, " " * geo.figs_w), None))

        for t in own:
            sel = t.id == selected_id
            done = board.is_done(t)
            reach = _task_reach(t, board, geo, today, "ash" if t.archived
                                else p.color, tick)
            # a finished task rests: thin spine, ash, no chip and no severity.
            # an ARCHIVED one rests harder — it also wears the mark, because
            # "put away" is a state the reader has to be able to see, and ash
            # alone is already what elapsed days look like.
            spine = (c("▏" + ARCHIVED_MARK, "ash") if t.archived
                     else c("▏ ", "dim") if done else c("▎ ", p.color))
            # the title stops at the today rule as well as at its own reach:
            # the rule is full-height by law, and a title that crossed it would
            # break the one column every row shares
            over = max(0, min(_reach_start(t, geo, today), geo.today_dc // 2))
            tw = geo.label_w - 3 + over
            title = title_markup(t, tw, sel)
            reach = reach[over:]
            due = parse_iso(t.due_date)
            # archived work is spent, so its meter is the spent form: nothing is
            # expected of it, so nothing about it can be late
            spent = done or t.archived
            mcells = due_meter(None if spent else ((due - today).days if due else None),
                               done=spent, width=min(METER_W, geo.figs_w))
            rows.append((band_row(spine + " " + title, reach,
                                  " " * max(0, geo.figs_w - len(mcells))
                                  + meter_markup(mcells), offset=over), t.id))

    # THE INBOX IS NOT LOST. Tasks with no project were drawn by the old gantt
    # and must not fall out of the new one just because it iterates projects.
    loose = [t for t in tasks if board.project_by_id(t.project_id) is None]
    if loose:
        rows.append((_pad(c("▎ ", "dim")
                          + c(escape(fit("Inbox", geo.label_w - 2)), "dim", bold=True)
                          + _band_markup([(" ", "dim")] * geo.field_w, geo, 0),
                          inner), None))
        for t in (sort_by_due([t for t in loose if not board.is_done(t)])
                  + sort_by_due([t for t in loose if board.is_done(t)])):
            done = board.is_done(t)
            over = max(0, min(_reach_start(t, geo, today), geo.today_dc // 2))
            reach = _task_reach(t, board, geo, today, "dim", tick)[over:]
            due = parse_iso(t.due_date)
            # archived work is spent, so its meter is the spent form: nothing is
            # expected of it, so nothing about it can be late
            spent = done or t.archived
            mcells = due_meter(None if spent else ((due - today).days if due else None),
                               done=spent, width=min(METER_W, geo.figs_w))
            rows.append((band_row(
                (c("▏" + ARCHIVED_MARK, "ash") if t.archived
                 else c("▏ ", "dim") if done else c("▎ ", "dim")) + " "
                + title_markup(t, geo.label_w - 3 + over, t.id == selected_id),
                reach, " " * max(0, geo.figs_w - len(mcells)) + meter_markup(mcells),
                offset=over), t.id))

    if not rows:
        lines.append(line(c(fit("  (nothing scheduled — press 'a' to add a task)",
                                inner), "dim")))

    body = rows[:max(0, h - 2)]
    shed = len(rows) - len(body)
    for markup, tid in body:
        lines.append(line(markup))
        if tid is not None and line_map is not None:
            line_map[tid] = len(lines) - 1

    if not shed and h - len(lines) - 2 >= 0:
        absence = absence_line([ln for ln in lanes_of(board, show_archived, today)],
                               today, inner)
        if absence:
            lines.append(line(_pad(absence, inner)))
    note = "  ".join(x for x in (
        f"+{shed} not shown" if shed else "",
        f"{archived_done} done archived" if archived_done else "") if x)
    lines.append(line(_pad(_scale_with_note(geo, inner, note) if note
                           else _scale_row(geo, inner), inner)))
    lines.append(bottom(None, w))
    return to_text(lines, height, w)


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
    inner = w
    tasks = board.visible_tasks(show_archived)
    start, widths = _phase_window(board, inner, board.task_by_id(selected_id))
    buckets = phase_buckets(board, tasks)
    sep = c("│", "frame")

    right = c(f"{len(tasks)} tasks", "mut")
    lines = [header(c("KANBAN", "accent", bold=True) + c(" · grouped", "mut"), right, w)]
    lines.append(line(sep.join(_windowed_header(board, start, widths))))
    lines.append(rule_row(_col_junctions(widths, "┼"), w))

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
    inner = w
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
    lines.append(rule_row(_matrix_junctions(label_w, widths, "┼"), w))

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

    lines.append(rule_row(_matrix_junctions(label_w, widths, "┴"), w))
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
    return to_text(lines, height, w)


# ---------------------------------------------------------------------------
# dispatcher
# ---------------------------------------------------------------------------
RENDERERS = {
    "swimlanes": render_swimlanes,
    "agenda": render_agenda,
    "gantt": render_gantt,
    "kanban": render_kanban,
}


def render_view(mode, board, show_archived, selected_id, today=None,
                width=68, height=0, line_map=None, presentation="grouped", tick=0) -> Text:
    if mode == "kanban":
        return render_kanban(board, show_archived, selected_id, today, width, height,
                             line_map, presentation)
    if mode == "gantt":
        return render_gantt(board, show_archived, selected_id, today, width, height,
                            line_map, tick=tick)
    if mode == "swimlanes":
        return render_swimlanes(board, show_archived, selected_id, today, width,
                                height, line_map, tick=tick)
    fn = RENDERERS.get(mode, render_swimlanes)
    return fn(board, show_archived, selected_id, today, width, height, line_map)


# ---------------------------------------------------------------------------
# navigation model — the ON-SCREEN order of each view, so cursor moves follow
# what the user sees (never board/data order). Returns a list of columns; each
# column is an ordered list of task-ids. Linear views return a single column.
# ---------------------------------------------------------------------------
def _is_dated(task: Task) -> bool:
    return (parse_iso(task.start_date) or parse_iso(task.due_date)) is not None


def swimlane_plan(board, show_archived, today: date, width: int,
                  height: int) -> tuple[list[LaneFacts], FieldGeo, int, int, int]:
    """(lanes ranked, geometry, titles, lead rows, wave rows) — the single answer
    both the renderer and navigation work from. The allocator spends the space
    it is actually given, so the answer depends on BOTH dimensions; asking it
    twice with different numbers is how a cursor ends up on an undrawn task."""
    h = height or 24
    geo = lane_geometry(_clamp_width(width) - 2, h)
    lanes = lanes_of(board, show_archived, today)
    active = [ln for ln in lanes if not ln.resting]
    # what the ladder pays to NAME is what the view can name: with `v` on the
    # reader has asked to see archived work, so it becomes nameable and rung one
    # buys rows for it. With `v` off it is not on screen and costs nothing.
    nameable = [len(ln.open) + sum(1 for t in ln.tasks if t.archived)
                for ln in active[1:]]
    titles, prof, wrows = allocate(
        geo, nameable,
        len([ln for ln in lanes if ln.resting]), h - 2 - (2 if active else 0))
    return lanes, geo, titles, prof, wrows


def swimlane_nav(board, show_archived, today: date, width: int,
                 height: int) -> list[str]:
    """The task ids the lanes view NAMES, in the order it draws them."""
    lanes, _geo, titles, _prof, _wrows = swimlane_plan(
        board, show_archived, today, width, height)
    active = [ln for ln in lanes if not ln.resting]
    out: list[str] = []
    if active and active[0].late:
        out.append(sorted(active[0].late, key=lambda t: parse_iso(t.due_date))[0].id)
    for lane in active[1:]:
        out += [t.id for t in lane_titles(lane, titles)]
    return out


def nav_model(mode, board, show_archived, today=None, width: int = 68,
              height: int = 0) -> list[list[str]]:
    today = today or date.today()
    tasks = board.visible_tasks(show_archived)

    if mode == "kanban":       # same phase columns, but in project-grouped order
        ordered: list[Task] = []
        for _, _, items in _kanban_groups(board, tasks, show_archived):
            ordered += items
        return [[t.id for t in bucket] for bucket in phase_buckets(board, ordered)]

    if mode == "swimlanes":
        # ONE column: the view is a stack of lanes, and the only selectable
        # things in it are the tasks it NAMES, in the order it names them — the
        # lead's worst late task first, then each stacked lane's titles. The
        # allocator decides how many, so the height is part of the question.
        return [swimlane_nav(board, show_archived, today, width, height)]

    if mode == "agenda":       # dated (sorted by due), then undated — matches render
        dated = [t for t in tasks if parse_iso(t.due_date) is not None]
        undated = [t for t in tasks if parse_iso(t.due_date) is None]
        return [[t.id for t in sort_by_due(dated)] + [t.id for t in undated]]

    if mode == "gantt":
        order, unscheduled = [], []
        for p in board.visible_projects(show_archived):
            for t in gantt_tasks(board, tasks, p.id):
                (order if _is_dated(t) else unscheduled).append(t.id)
        loose = [t for t in tasks if board.project_by_id(t.project_id) is None]
        for t in (sort_by_due([t for t in loose if not board.is_done(t)])
                  + sort_by_due([t for t in loose if board.is_done(t)])):
            (order if _is_dated(t) else unscheduled).append(t.id)
        return [order + unscheduled]

    return [[t.id for t in tasks]]


# ---------------------------------------------------------------------------
# the legend — what `?` explains, per view
#
# THREE COMMITMENTS, and they are what make it impossible for this to lie:
#   1. every swatch is drawn by CALLING the same function that draws the mark in
#      the view, so there is no second copy of the art to drift;
#   2. it is per view — the gantt's legend is not the lanes';
#   3. it explains ONLY what is on screen. If this board has no cancelled
#      project, the `╳` entry does not appear: sending the reader to look for an
#      absent mark is another way of lying. (The proposal's own law caught seven
#      such ghost marks in its first version.)
#
# Register: it DESCRIBES MARKS. It never addresses the reader and never judges
# the work — "overdue" is a fact about a date.
# ---------------------------------------------------------------------------
def _legend_board_facts(board: Board, today: date) -> dict:
    tasks = board.visible_tasks(False)
    projects = board.visible_projects(False)
    open_ = [t for t in tasks if not board.is_done(t)]
    dues = [(parse_iso(t.due_date), t) for t in tasks]
    return {
        "projects": projects,
        "tasks": tasks,
        "statuses": {p.status for p in projects},
        "phases": {min(3, board.phase_index(t)) for t in open_},
        "high": any(t.priority == "high" for t in open_),
        "done": any(board.is_done(t) for t in tasks),
        "overdue": any(d and d < today and not board.is_done(t) for d, t in dues),
        "today": any(d == today and not board.is_done(t) for d, t in dues),
        "week": any(d and 0 < (d - today).days <= 7 for d, t in dues),
        "later": any(d and (d - today).days > 7 for d, t in dues),
        "undated": any(d is None for d, _t in dues),
        "project_due": any(p.due_date for p in projects),
        "blocked": any(t.blocked for t in open_),
    }


def _meter_swatch(days, done=False) -> str:
    return meter_markup(due_meter(days, done=done))


def legend_entries(mode: str, board: Board, today: date | None = None,
                   width: int = 96, height: int = 30,
                   show_archived: bool = False) -> list[tuple[str, str]]:
    """(swatch, what it means) for the marks THIS view is currently drawing.

    The size is part of the question: the lanes allocator decides how many tasks
    are NAMED, and a phase glyph only exists on a named row. Explaining a phase
    the screen never draws is the same ghost as explaining an absent status."""
    today = today or date.today()
    f = _legend_board_facts(board, today)
    hue = f["projects"][0].color if f["projects"] else "violet"
    out: list[tuple[str, str]] = []

    # The spine has two forms and the view chooses by rank: the leader wears the
    # heavy one, the stacked lanes the thin one. A board whose only project leads
    # draws no thin spine at all — so neither does its legend.
    active = [p for p in f["projects"]
              if any(t.project_id == p.id and not board.is_done(t) for t in f["tasks"])]
    if mode == "kanban" and f["projects"]:
        # kanban draws the project header with ▐ and each card with ▊ — the
        # lanes spine ▎ is a different view's glyph and does not belong here
        out.append((c("▐", hue), "project header, by colour"))
        if f["tasks"]:
            out.append((c("▊", hue), "a task card, in its project's colour"))
    if mode == "swimlanes":
        if active:
            out.append((c("▌", active[0].color), "the project under most pressure"))
        if len(active) > 1:
            out.append((c("▎", hue), "spine: the project, by colour"))
        if len(active) < len(f["projects"]):
            out.append((c("▏", "dim"), "a project with nothing open, at rest"))
        out.append((c(LATTICE, "ash") + c(LATTICE, "dim") + c(RULE, "accent"),
                    "field: ash spent · dim still to spend · ╎ today"))
        if f["project_due"]:
            out.append((c("◆", hue), "the project's own due date"))
        for st in ("paused", "cancelled", "completed"):
            if st in f["statuses"]:
                out.append((c(STATUS_MARK[st], "dim"), f"project {st}"))
        lanes, _geo, titles, _prof, _wr = swimlane_plan(board, False, today,
                                                        width, height)
        named = [t for lane in [ln for ln in lanes if not ln.resting][1:]
                 for t in lane_titles(lane, titles)]
        for i in sorted({min(3, board.phase_index(t)) for t in named}):
            out.append((c(phase_glyph({i}), hue),
                        f"task in phase {i + 1}: the dot climbs as it advances"))
        if f["high"]:
            out.append((c("!N", "ink"), "high-priority work still open"))
    if mode == "gantt":
        # REGENERATED for the field: the span IS the wave, and the answer a
        # gantt exists to give comes out of the difference between two bands.
        if f["projects"]:
            out.append((c(FIELD_REACH * 2, "ash") + c(FIELD_REACH * 2, hue),
                        "the span: ash is elapsed, colour is what remains"))
        # the progress band only exists once something HAS progressed
        if any(board.project_progress(p.id, False) > 0 for p in f["projects"]):
            out.append((c(FIELD_PROGRESS * 2 + FIELD_HALF, hue),
                        "how far the work actually got"))
            out.append((c(FIELD_HALF, hue) + c("··", "ash"),
                        "the gap between the two bands: the slip, as a length"))
        if f["project_due"]:
            out.append((c("◆", hue), "the project's own due date"))
        out.append((c(RULE, "accent"), "today"))
        if f["tasks"]:
            out.append((c(FIELD_TASK * 2, hue) + c(FIELD_PHASE_TIP[1], hue),
                        "a task's reach, tipped by its phase"))
        if f["done"]:
            out.append((c("▏", "dim") + c(FIELD_TASK + FIELD_PHASE_TIP[2], "ash"),
                        "finished work, at rest in ash"))
    if mode == "agenda":
        out.append((c("●", "over"), "a task's due date, on the shared day axis"))
        out.append((c("─", "dim"), "its reach: from today to that date"))
        out.append((c("┃", "accent"), "today"))
        if f["blocked"]:
            out.append((c("▲", "over"), "blocked"))
    if mode in ("swimlanes", "gantt"):
        for present, days, label in (("overdue", -1, "days overdue — ▲ is the only alert"),
                                     ("today", 0, "due today"),
                                     ("week", 3, "due this week"),
                                     ("later", 40, "due later")):
            if f[present]:
                out.append((_meter_swatch(days), label))
        if f["done"]:
            out.append((_meter_swatch(None, done=True), "finished, and no longer counting down"))
        if f["undated"]:
            out.append((_meter_swatch(None), "no date to count down to"))
    if mode == "kanban" and f["high"]:
        out.append((c("!", "ink"), "high-priority task"))
    # THE NO-GHOST LAW, and archived is its clearest case: the mark exists on
    # screen only while `v` is on AND something is actually archived. Explaining
    # a mark the reader cannot see is the same fault as hiding one they can.
    if show_archived and any(t.archived for t in board.visible_tasks(True)):
        drawn = True
        if mode == "swimlanes":
            # the lanes view NAMES a bounded set, and the lead band names only
            # its worst-late task — so a board whose only archived work sits in
            # the lead draws no mark at all, and must not be told about one.
            # Same test the phase-glyph entries above already apply.
            lanes_, _g, tt, _pf, _wr = swimlane_plan(board, True, today, width, height)
            act = [ln for ln in lanes_ if not ln.resting]
            drawn = any(t.archived for ln in act[1:] for t in lane_titles(ln, tt))
        if drawn:
            out.append((c(ARCHIVED_MARK, "ash"),
                        "archived: put away, not deleted — x brings it back"))
    return out
