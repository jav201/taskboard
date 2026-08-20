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

import copy
import re
from datetime import date, timedelta
from pathlib import Path
from typing import NamedTuple

from rich.cells import cell_len, set_cell_size
from rich.console import Console
from rich.markup import escape
from rich.style import Style
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
    """Right-aligned indicator glyphs, each rendered as ' <glyph>'.

    Keeps as many as fit within `budget`, dropping from the LEFT (so the
    rightmost/most-important marker survives when space is tight). Returns
    (markup, used_width). `tokens` is [(glyph, color_key), ...]; a token's
    cost is 1 + its own cell width, so a multi-cell token (the aging `·Nd`,
    LLR-006.1) sheds under width pressure exactly like its 1-cell siblings."""
    kept: list[tuple[str, str]] = []
    cost = 0
    for glyph, col in reversed(tokens):
        w = 1 + cell_len(glyph)
        if cost + w <= budget:
            kept.insert(0, (glyph, col))
            cost += w
        else:
            break
    markup = "".join(c(" " + g, col) for g, col in kept)
    return markup, cost


def card_cell(task: Task, board: Board, wc: int, selected: bool, *,
              prefix: str = "", prefix_color: str = "mut",
              allow_priority: bool = True, today: date | None = None) -> str:
    """A width-exact card: `prefix` + truncated title + right indicators
    (↗ ! ▤ ·Nd ▣).

    Title is truncated with … so it can NEVER share a cell with the trailing
    indicators, at any width down to 0. Always returns exactly `wc` cells.
    The `·Nd` aging token (HLR-006, LLR-006.1) is how long the task has sat
    in its current phase — `days_in_phase` off `phase_changed` — shown only
    while the task is NOT done and the stamp is KNOWN (None is unknown, never
    zero: an unstamped card renders no token rather than a lying `·0d`, and
    done work rests — its age is not work-in-progress information)."""
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
    if not board.is_done(task):
        age = days_in_phase(task, today or date.today())
        if age is not None:
            # Age is a FACT about sitting still, not a judgement on it — the
            # quiet dim house (the same house date distances wear), never a
            # severity hue and never a project colour.
            tokens.append((f"·{age}d", "dim"))
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


def focus_tasks(board: Board, show_archived: bool) -> list[Task]:
    """The Focus Board's content: individually pinned tasks plus every task of
    a pinned project. Each task appears once, archived filtered by the viewer."""
    tasks = board.visible_tasks(show_archived)
    pinned_project_ids = {p.id for p in board.visible_projects(show_archived)
                          if p.pinned}
    return [t for t in tasks if t.pinned or t.project_id in pinned_project_ids]


def _focus_sort_key(board: Board, show_archived: bool, t: Task, today: date):
    """Order pinned tasks by project (board order) then due date; Inbox last."""
    projects = board.visible_projects(show_archived)
    p_index = next((i for i, p in enumerate(projects) if p.id == t.project_id),
                   len(projects))
    d = parse_iso(t.due_date)
    return (p_index, d is None, d or date.max)


def stale_order(board: Board, tasks: list[Task], today: date,
                show_archived: bool = False) -> list[Task]:
    """Project groups ordered by their stalest task; tasks stale-first inside
    the group; Inbox last. Unknown `phase_changed` stamps sink — never read
    as zero."""
    def age(t: Task) -> int:
        a = days_in_phase(t, today)
        return a if a is not None else -1

    order: list[str | None] = [p.id for p in board.visible_projects(show_archived)]
    order.append(None)
    groups: dict[str | None, list[Task]] = {key: [] for key in order}
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


def fill_height(lines: list[str], height: int, w: int,
                pinned: int = 0) -> list[str]:
    """Pad blank rows so the view fills the viewport when content is short.

    `pinned` is how many TRAILING rows are an axis that belongs at the bottom of
    the screen; the pad goes above those and everything else stays at the top.

    It used to be assumed rather than passed — the pad always went above the last
    row, "which is the axis every view closes with". Two views close with no axis
    at all, so their last TASK was pinned to the bottom of the viewport with a
    field of blank rows above it: on a real board, 84 swept kanban sizes and 44
    agenda sizes stranded a row that way. The lanes and the gantt do close with an
    axis, which is why they always looked right and the assumption survived. An
    axis is now something a view SAYS it has."""
    lines = [x for x in lines if x != ""]          # a frameless close adds none
    if not height or len(lines) >= height:
        return lines                               # taller than the viewport: it scrolls
    pad = height - len(lines)
    keep = pinned if 0 < pinned <= len(lines) else 0
    if not keep:
        return lines + [blank_line(w)] * pad
    return lines[:-keep] + [blank_line(w)] * pad + lines[-keep:]


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


def to_text(lines: list[str], height: int, w: int, pinned: int = 0) -> Text:
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
    return Text.from_markup(collapse_runs("\n".join(fill_height(lines, height, w, pinned))),
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
    lead would stop being the hero.

    THE CHARGE, AND IT IS ONLY HALF THE MODEL. This bills
    `prof + sum(wrows + min(titles, o)) + n_rest`, but `lead_band` DRAWS
    `prof + 2` -- a head and a tail that `prof` does not count. The missing two
    rows are paid at the call site (`swimlane_plan`), which is where the whole
    identity is written down. Read either half on its own and the model is off
    by two in whichever direction you read it; that mistake, in both directions,
    is what `.dev-flow/05-postmortem.md` is about. `tests/test_row_cost.py`
    pins the two halves together, so neither can move alone."""
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


def _scale_cells(geo: FieldGeo,
                 months: dict[int, str] | None = None) -> tuple[list[str], set[int]]:
    """The axis body as plain cells, plus the columns carrying a month name.

    ONE ROW, TWO SCALES. The day figures answer "how far does this window
    reach?" and the month names answer "reach until WHEN?" — the operator asked
    for the second and the row already carried the first. The day figures are the
    anchors and keep their cells; a month name that cannot stand clear of them
    (with a blank either side) is dropped WHOLE, which is exactly the rule the
    day labels themselves already follow. A half-printed month is a wrong date,
    not a partial one."""
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

    month_cols: set[int] = set()
    for at in sorted(months or {}):
        name = months[at]
        if at < 0 or at + len(name) > span:
            continue
        if any(body[at + i] != " " for i in range(-1, len(name) + 1)
               if 0 <= at + i < span):
            continue
        place(name, at)
        month_cols.update(range(at, at + len(name)))
    return body, month_cols


def _tone_runs(body: list[str], month_cols: set[int]) -> str:
    """The two scales in two tones, coalesced into runs.

    The months take `mut` and the day figures keep `dim`: the calendar is the
    coarse gauge a reader lands on first, the day offsets are the fine print
    under it. Runs are coalesced here rather than per cell so the second tone
    costs a handful of extra spans, not one per column."""
    out, i, n = [], 0, len(body)
    while i < n:
        j, is_month = i, i in month_cols
        while j < n and (j in month_cols) == is_month:
            j += 1
        out.append(c("".join(body[i:j]), "mut" if is_month else "dim"))
        i = j
    return "".join(out)


def _scale_row(geo: FieldGeo, inner: int,
               months: dict[int, str] | None = None) -> str:
    """The axis says what it measures — without it the field is a stripe.
    Exactly `inner` cells. With no `months` this is byte-identical to what the
    views that carry no calendar have always drawn."""
    body, month_cols = _scale_cells(geo, months)
    return (" " * geo.label_w + _tone_runs(body, month_cols)
            + " " * max(0, inner - geo.label_w - geo.field_w))


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
        return to_text(lines, height, w, pinned=1)

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
    return to_text(lines, height, w, pinned=1)


def _scale_with_note(geo: FieldGeo, inner: int, note: str,
                     months: dict[int, str] | None = None) -> str:
    """The axis, plus what the height could not show. A view that drops rows in
    silence is lying about how much work there is.

    The month tone survives the truncation: the mask is by column, so cutting the
    tail drops trailing columns without recolouring what is left."""
    body, month_cols = _scale_cells(geo, months)
    keep = max(0, inner - vis(note) - 1)
    full = ([" "] * geo.label_w + body
            + [" "] * max(0, inner - geo.label_w - geo.field_w))
    full = (full + [" "] * keep)[:keep]
    base = _tone_runs(full, {i + geo.label_w for i in month_cols})
    return base + " " * max(0, inner - keep - vis(note)) + c(note, "mut")


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
# `FIELD_REACH` was `█`, and a full block is what the operator saw as "bloques muy
# grandes": a long project span drew as an unbroken slab that shouted over every
# task bar under it and left no room for the guide to show through. The approved
# prototype (`_prototypes/proto.py:345`) draws the project's reach as a THIN RULE
# in the project's own hue. The three-weight hierarchy is intact — reach still
# outranks progress outranks task — the top weight just stopped shouting, and a
# rule lets the week guide read THROUGH the span instead of being buried by it.
#
# 2026-08-07 — THE SHADED BAND IS GONE AND THE WEIGHTS DROPPED AGAIN. The
# operator, seeing the `━`/`▓▓▓▌` pair shipped above: "las barras de tiempo
# mejoraron pero siguen siendo muy grandes... en vez del cuadro sombreado, opta
# por lo que se prototipó, una línea y el círculo". Approved from a rendered
# prototype (`_prototypes/gantt_line_circle.py`, variant A′).
#
# `FIELD_PROGRESS`/`FIELD_HALF` no longer draw a second row under each project:
# progress is now ONE CELL, `PROGRESS_DOT`, riding on the span itself. They are
# kept because a task's own reach still ends mid-cell and still says so.
#
# THE TWO RULES MUST NOT BE THE SAME RULE. Both were `─` for one commit and
# `test_the_project_reach_is_a_rule_not_a_slab` caught it immediately — "two
# weights collapsed into one". The hierarchy reach > task is load-bearing: a
# project's span has to out-rank the task bars living under it. Solid `─` for
# the span, dashed `╌` for a task, so the rank survives the loss of shading.
#
# Splitting them also paid for itself in the census: `─` is in `_census`'s
# frame set and a task reach is most of the field's cells, so moving tasks off
# it took chrome 5.0 -> 3.1 and `marked` 67.8 -> 69.8, back over its floor,
# with no amendment to the law at all.
FIELD_REACH = "─"     # a project's span            (was ⣿, █, then ━)
FIELD_PROGRESS = "▓"  # how far the work actually got (was ⣤)
FIELD_TASK = "╌"      # a task's reach              (was ⣀, ▒, briefly ─)
FIELD_HALF = "╴"      # ends mid-cell               (was ⡄, then ▌)

# WHERE THE WORK ACTUALLY IS, in one cell instead of a whole row. The gap
# between this and the project's `◆` is the slip, read as a LENGTH — which is
# what the two-row design existed to show, and it shows it in half the rows.
PROGRESS_DOT = "●"

# AND IT BREATHES, BUT ONLY WHEN IT HAS SOMETHING TO SAY.
#
# The gantt was already not still: the flow packet crosses a task's reach one
# cell per tick. A second motion therefore has to earn its place, and an
# ambient that ran on every project would be five circles competing with nine
# packets while carrying no information at all.
#
# So the pulse is RATIONED the way this codebase rations red: a circle breathes
# only where the work sits LEFT of where the calendar says it should be. Motion
# then means "this one is slipping", and a board with nothing behind it is
# completely still.
#
# Four phases on the app's one shared clock, same as `RULE_PHASES`: `●◉◎◉` is a
# breath rather than a blink — weight rises and falls and the cycle closes — and
# 4 x TICK_SECONDS clears the >= 2 s floor below which an ambient reads as a
# fault flashing. Glyph only; the hue never moves.
PULSE_PHASES = ("●", "◉", "◎", "◉")

# THE WEEK GUIDE: the thing the operator said was missing — "no hay gauges de
# semana y mes", a bar measured against nothing.
#
# The prototype rules weeks with `│`. Copying that glyph literally is MEASURED to
# be wrong here: `│` is in the census FRAME set (`tests/test_gantt.py:192`), the
# gantt's chrome is 0.0 % today because the frame was deliberately removed, and
# ~22 guides x ~25 rows would put it near 17 % against a `< 10 %` law. `┆` is a
# dashed vertical that is not a frame character, is quieter than the today rule
# `╎` (which must stay the loudest vertical), and no other view's legend uses it.
#
# It is painted in THE LATTICE'S OWN TONE — the glyph changes, the colour does
# not. That is what keeps it ground rather than data, and it is also why it costs
# ZERO extra runs: `collapse_runs` coalesces by style, not by character.
FIELD_WEEK = "┆"      # the Monday column, drawn in the lattice's tone

# The gutter between a title and the first bar cell. The title is allowed to
# spend empty field (the REV5 #19 ruling) and it spent ALL of it, so a truncated
# title's `…` sat directly against its own bar. Two cells of the field's own
# lattice, which is already `·`, are the prototype's dot leaders exactly.
GUTTER = 2

# The tip that says WHICH PHASE the task is in, in the field's own alphabet.
# `phase_glyph` keeps encoding phase as a CLIMBING DOT — it is still right for
# the lanes, where one cell must carry a SET of phases and dots can be OR'd
# together. A gantt bar carries exactly one, and a braille dot at the end of a
# shaded run reads as the bar fading out rather than as its tip. Same meaning,
# rising fill instead of climbing dot, so the tip belongs to the bar it ends.
# The floor is 3/8, not 1/8: a tip lighter than the bar it ends reads as the
# bar fading out, which is the exact complaint this whole change answers. The
# ceiling stops below `█` so the tip can never be mistaken for a reach cell.
#
# 2026-08-07 — the rising-fill BLOCKS became rising-fill CIRCLES. The bar they
# end is a rule now, not a shaded run, so a block tip reads as a lump on a
# wire; a filling circle is the same "how far through its phases" reading in
# the same one cell, and it rhymes with the project's own `PROGRESS_DOT`
# instead of shouting over it. Order still climbs, so the floor/ceiling
# argument above survives the change of alphabet.
FIELD_PHASE_TIP = ("○", "◔", "◑", "◕")


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


META_FULL_W = 20        # 'Jul 14 → Aug 17' — start/due date chips
META_PCT_W = 6          # ' 62%'              — percent alone, narrow terminals
META_FULL_INNER = 90    # below this the timeline needs those cells more


def gantt_meta_geometry(inner: int, glabel_w: int, cell: int) -> tuple[int, bool]:
    """Width of the figures column right of the bars, and whether it carries the
    date chips. On a narrow terminal the chips drop and the column falls back to
    the progress percent alone."""
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


def _gantt_date_chip(iso: str | None, today: date,
                     spent: bool = False) -> tuple[str, str]:
    """Absolute-date chip: 'Aug 17' and a tone keyed to overdue/today/future.

    Returns (label, color_key). None dates render as a dim em-dash. Spent work
    (done/archived) rests in ash so a finished task never flashes red."""
    if spent:
        d = parse_iso(iso) if iso else None
        label = d.strftime("%b %d").replace(" 0", " ") if d else "—"
        return label, "ash"
    if iso is None:
        return "—", "dim"
    d = parse_iso(iso)
    if d is None:
        return "—", "dim"
    label = d.strftime("%b %d").replace(" 0", " ")
    delta = (d - today).days
    if delta < 0:
        return label, "over"
    if delta == 0:
        return label, "soon"
    return label, "mut"


def _gantt_date_pair(start_iso: str | None, due_iso: str | None, today: date,
                     width: int, spent: bool = False) -> str:
    """Right-aligned 'start → due' chip for the gantt tail.

    Falls back through shorter forms when space is tight: full pair, then only
    the due date, then a truncated due date. The result is always exactly
    `width` visible cells (or empty when width is 0)."""
    if width <= 0:
        return ""
    s_lab, s_tone = _gantt_date_chip(start_iso, today, spent)
    d_lab, d_tone = _gantt_date_chip(due_iso, today, spent)
    candidates = [
        (f"{s_lab} → {d_lab}", c(s_lab, s_tone) + " → " + c(d_lab, d_tone)),
        (f"— → {d_lab}", c("—", "dim") + " → " + c(d_lab, d_tone)),
        (d_lab, c(d_lab, d_tone)),
    ]
    for plain, markup in candidates:
        if vis(plain) <= width:
            return " " * (width - vis(plain)) + markup
    # even the due date alone does not fit: truncate it visibly
    return c(fit(d_lab, width), d_tone)


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
                progress: float, tick: int = 0
                ) -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    """THE SPAN IS THE WAVE, and the answer a gantt exists to give is a LENGTH
    along it.

    The span runs from start to `◆`: ASH for what has elapsed, the project's own
    hue for what remains. `PROGRESS_DOT` marks how far the work actually got.
    THE GAP BETWEEN THE DOT AND THE DIAMOND IS THE SLIP. "Am I behind?" is the
    question a gantt is for, and the old view could not answer it.

    IT USED TO TAKE TWO ROWS AND NOW IT TAKES ONE. `band` was a second field row
    per project, filled with `▓▓▓▌`, and the operator's complaint was both that
    it shouted ("siguen siendo muy grandes") and that the view ran out of room
    ("no puedo ver el resto de tareas"). Those were the same defect: at 104x26
    on the demo board the old shape drew 14 task rows and HID one; this shape
    draws 15, hides none, and has three rows to spare.

    `band` is still returned, and still all blanks, because `band_row` and the
    callers' width arithmetic are written around a (prefix, band, suffix)
    triple. Returning it empty keeps that contract with no width change; the
    caller simply no longer emits a row for it.
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

    # THE TODAY RULE CROSSES THE SPAN. `band_row` paints the rule only into a
    # BLANK cell -- "anything drawn takes the cell first" -- so a long span used
    # to occlude it and the second row was where it still showed through. With
    # that row gone the rule could vanish from the view entirely, and
    # `test_no_entry_describes_a_mark_the_view_is_not_drawing` said so at once:
    # the legend named a mark nobody drew. Blanking one cell of plain span line
    # gives it back, and a calendar boundary crossing a bar is what a gantt is
    # supposed to look like.
    if c0 <= today_cell <= c1 and 0 <= today_cell < geo.field_w:
        span[today_cell] = (" ", "dim")

    reached = c0 + int(round((c1 - c0) * max(0.0, min(1.0, progress))))
    # clamped INTO the span: at progress 0 the dot sits on the start cell and at
    # 1.0 on the `◆`, so it can never float in empty field where it would read
    # as a mark belonging to nothing.
    #
    # The dot is written AFTER the rule's cell is cleared, so when the work has
    # got exactly as far as today the dot wins. That is the right order: the
    # rule says where today is, and the reader can already see that from every
    # other row -- the dot says something only this row knows.
    dot = min(max(reached, c0), min(c1, geo.field_w - 1))
    if 0 <= dot < geo.field_w:
        span[dot] = (_progress_glyph(c0, c1, today_cell, progress, tick), hue)
    return span, band


def _behind(c0: int, c1: int, today_cell: int, progress: float) -> bool:
    """Is the work LEFT of where the calendar says it should be?

    Compared in the span's own coordinates rather than in days, so it answers
    the question the reader is actually asking of THIS row: the dot is behind
    when it sits left of the today rule crossing the same span.

    A project whose span has not started, or has already ended, is never
    behind: `elapsed` clamps to [0, 1] and a zero-length span short-circuits,
    so neither can produce a pulse from arithmetic alone.

    The 0.02 margin is not decoration. Progress and elapsed are both quantised
    to whole cells, so a project exactly on schedule lands within a cell of
    itself and would otherwise flicker in and out of "behind" as the day moves
    — motion that means nothing, which is the one thing the ration exists to
    prevent."""
    if c1 <= c0:
        return False
    elapsed = max(0.0, min(1.0, (today_cell - c0) / (c1 - c0)))
    return progress < elapsed - 0.02


def _progress_glyph(c0: int, c1: int, today_cell: int, progress: float,
                    tick: int) -> str:
    """`PROGRESS_DOT` at rest; a phase of the breath when the work is behind."""
    if not _behind(c0, c1, today_cell, progress):
        return PROGRESS_DOT
    return PULSE_PHASES[tick % len(PULSE_PHASES)]


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


def _priority_hue(priority: str) -> str:
    """Hue for a task bar in the gantt: priority is the primary semantic channel."""
    return {"high": "rose", "normal": "sky", "low": "mut"}.get(priority, "sky")


def _task_reach(task: Task, board: Board, geo: FieldGeo, today: date,
                hue: str, tick: int | None = None) -> list[tuple[str, str]]:
    """A task is a REACH of variable length with its phase glyph at the tip —
    not a five-cell slab. A mark that cannot vary is not a datum (DATAVIZ 13,
    which the old week-resolution bar violated: two different tasks drew the
    same `▬▬▬▬▬`).

    Since batch-06 the bar wears the task's PRIORITY hue (high=rose, normal=sky,
    low=mut). Done/archived tasks still rest in ash. Milestones — tasks whose
    start equals due — render as a single diamond instead of a span."""
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
    tone = "ash" if done else _priority_hue(task.priority)
    # milestone: a single diamond at the date cell
    if s is not None and e is not None and s == e and 0 <= a < geo.field_w:
        cells[a] = ("◆", tone)
        return cells
    for x in range(a, b):
        cells[x] = (FIELD_TASK, tone)
    cells[b] = (FIELD_PHASE_TIP[min(3, board.phase_index(task))], tone)
    if not done and tick is not None and b > a and _flowing(board, task):
        # THE FLOW PACKET, kept from the shipped gantt: work drifts toward its
        # deadline. It rides the task's own reach now instead of a week slab.
        cells[a + (tick % max(1, b - a))] = ("▬", "bright")
    return cells


def gantt_gauge(geo: FieldGeo, today: date) -> tuple[frozenset[int], dict[int, str]]:
    """THE CALENDAR THE BARS ARE MEASURED AGAINST: which field cells begin a week,
    and which begin a month (with that month's name).

    One cell is two days, so a Monday and the today boundary can land in the SAME
    cell. The today rule is full-height by law and outranks everything, so a week
    that collides with it is dropped rather than drawn — two verticals in one
    column would read as one thicker rule, which is a third meaning nobody
    declared."""
    weeks: set[int] = set()
    months: dict[int, str] = {}
    today_cell = geo.today_dc // 2
    for dc in range(min(geo.dot_w, geo.field_w * 2)):
        cell = dc // 2
        d = today + timedelta(days=dc - geo.today_dc)
        if d.weekday() == 0 and cell != today_cell:
            weeks.add(cell)
        if d.day == 1 and cell not in months:
            months[cell] = d.strftime("%b").upper()
    return frozenset(weeks), months


def _band_markup(cells: list[tuple[str, str]], geo: FieldGeo, phase: int = 0,
                 lattice: bool = True, offset: int = 0,
                 weeks: frozenset[int] = frozenset()) -> str:
    """Cells to markup, over the field's own lattice — ash behind today, dim
    ahead — with the today rule where nothing else is drawn.

    `weeks` rules the calendar THROUGH the ground: a week guide replaces the
    lattice dot in its own cell and wears the lattice's tone, so it never
    outranks a datum and never covers one — anything drawn takes the cell first.
    Empty by default, so the views that do not carry a calendar are unchanged."""
    out = []
    for j, (glyph, tone) in enumerate(cells):
        i = j + offset
        past = (2 * i + 1) < geo.today_dc
        if glyph == " ":
            if i == geo.today_dc // 2:
                out.append(c(RULE_PHASES[phase % len(RULE_PHASES)], "accent"))
            elif lattice:
                out.append(c(FIELD_WEEK if i in weeks else LATTICE,
                             "ash" if past else "dim"))
            else:
                out.append(" ")
        else:
            out.append(c(glyph, tone))
    return "".join(out)


def gantt_geometry(inner: int, height: int) -> FieldGeo:
    """The lanes geometry, with a wider figures band: the gantt's row now
    carries start/due date chips when the terminal is wide enough, otherwise
    it falls back to the progress percent alone."""
    g = lane_geometry(inner, height)
    figs_w, _ = gantt_meta_geometry(inner, g.label_w, 8)
    field_w = max(0, inner - g.label_w - figs_w - 1)
    dot_w = field_w * 2
    today_dc = (int(dot_w * 0.30) // 2) * 2
    return g._replace(figs_w=figs_w, field_w=field_w, dot_w=dot_w,
                      today_dc=today_dc, today_cell=g.label_w + today_dc // 2)


def render_gantt(board, show_archived, selected_id, today=None,
                 width=68, height=0, line_map=None, tick=0,
                 focus: str | None = None) -> Text:
    """The gantt on the shared day axis: one cell is two days, and the axis
    INCLUDES THE PAST.

    The old view started its axis on Monday of this week, so a project already
    overdue drew as an empty row with a `◂` — and the more overdue work a board
    held, the emptier the view got. That is why it was the one view where MORE
    data produced LESS used screen (ink fell 23.3 % -> 21.0 % from typical to
    extreme). An axis with a past is the fix.

    `focus` is a project id; when set, only that project (and its tasks) are
    rendered. Inbox rows are hidden while a focus is active.
    """
    today = today or date.today()
    w = _clamp_width(width)
    inner = w
    h = height or 24
    geo = gantt_geometry(inner, h)

    tasks = board.visible_tasks(show_archived)
    late_n = sum(1 for t in tasks
                 if (d := parse_iso(t.due_date)) and d < today and not board.is_done(t))
    focus_name = ""
    if focus:
        proj = board.project_by_id(focus)
        focus_name = f" (focused: {proj.name})" if proj else " (focused)"
    right = (c(f"▲{late_n} past due", "over", bold=True) if late_n
             else c("nothing past due", "dim"))
    title = c("◆ GANTT", "accent", bold=True)
    if focus_name:
        title += c(focus_name, "mut")
    lines = [header(title, right, w)]

    weeks, months = gantt_gauge(geo, today)

    def band_row(prefix: str, cells: list[tuple[str, str]], figures: str,
                 offset: int = 0) -> str:
        # label + field + ONE gap + figures == inner, so the figures stay flush
        # right; without the gap `_pad` appended it and the meter drifted left
        return _pad(prefix + _band_markup(cells, geo, 0, offset=offset,
                                          weeks=weeks)
                    + " " + figures, inner)

    archived_done = sum(1 for t in board.visible_tasks(True)
                        if t.archived and board.is_done(t))

    def lane_sep() -> Row:
        """A full-width horizontal rule that closes one swimlane and opens the
        next. It costs one row, but it is the lane: without it every project runs
        into the next and the eye has no place to rest between groups."""
        return (c("─" * inner, "frame"), None)

    rows: list[Row] = []
    first_block = True
    for p in board.visible_projects(show_archived):
        if focus and p.id != focus:
            continue
        if not first_block:
            rows.append(lane_sep())
        first_block = False
        own = gantt_tasks(board, tasks, p.id)
        prog = board.project_progress(p.id, show_archived)
        span, band = _span_bands(p, geo, today, p.color, prog, tick)
        # the project row has no `over` to borrow from — its label is already
        # exactly `label_w` cells — so its gutter comes out of the name's own
        # clip. `fit` still pads to `label_w - 2`, so the prefix width is
        # unchanged and the last GUTTER cells are blank by construction.
        label = c("▎ ", p.color) + c(escape(fit(clip(p.name,
                                                     geo.label_w - 2 - GUTTER),
                                                geo.label_w - 2)),
                                     p.color, bold=True)
        # DATE CHIPS replace the old percent + due-meter tail: exact start and
        # due dates are more precise than a relative offset, which was the user's
        # request for the gantt scale.
        tail = _gantt_date_pair(p.start_date, p.due_date, today, geo.figs_w,
                                spent=p.status == "completed")
        rows.append((band_row(label, span, tail), None))
        # NO SECOND ROW. `band` used to be emitted here as `▓▓▓▌`; progress now
        # rides the span as one cell, and this line's absence IS the room the
        # tasks got back — the operator's "no puedo ver el resto de tareas".
        del band

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
            # break the one column every row shares.
            #
            # `- GUTTER` is the fix for the collision the operator reported. The
            # title used to spend the empty field right up to the first bar cell,
            # so a truncated title's `…` sat flush against its own reach:
            # `Telemetry_Ingestion_Name…▬▒▒▅`. Giving the cells back to the field
            # costs nothing in width (see `band_row`: prefix grows by `over` and
            # the band shrinks by `over`, for any `over`) and the field already
            # paints them as `·` — the prototype's dot leaders, for free.
            over = max(0, min(_reach_start(t, geo, today),
                              geo.today_dc // 2) - GUTTER)
            tw = geo.label_w - 3 + over
            dep = c("└─►", "mut") if t.depends_on else "   "
            title = title_markup(t, max(0, tw - 3), sel) + dep
            reach = reach[over:]
            # archived work is spent, so its dates rest in ash: nothing is
            # expected of it, so nothing about it can be late.
            tail = _gantt_date_pair(t.start_date, t.due_date, today, geo.figs_w,
                                    spent=done or t.archived)
            rows.append((band_row(spine + " " + title, reach, tail, offset=over), t.id))

    # THE INBOX IS NOT LOST. Tasks with no project were drawn by the old gantt
    # and must not fall out of the new one just because it iterates projects.
    # When a project focus is active, inbox rows are hidden to match kanban focus.
    loose = [t for t in tasks if board.project_by_id(t.project_id) is None]
    if loose and not focus:
        if not first_block:
            rows.append(lane_sep())
        first_block = False
        rows.append((_pad(c("▎ ", "dim")
                          + c(escape(fit("Inbox", geo.label_w - 2)), "dim", bold=True)
                          + _band_markup([(" ", "dim")] * geo.field_w, geo, 0,
                                         weeks=weeks),
                          inner), None))
        for t in (sort_by_due([t for t in loose if not board.is_done(t)])
                  + sort_by_due([t for t in loose if board.is_done(t)])):
            done = board.is_done(t)
            over = max(0, min(_reach_start(t, geo, today),
                              geo.today_dc // 2) - GUTTER)
            reach = _task_reach(t, board, geo, today, "dim", tick)[over:]
            # archived work is spent, so its dates rest in ash: nothing is
            # expected of it, so nothing about it can be late.
            tail = _gantt_date_pair(t.start_date, t.due_date, today, geo.figs_w,
                                    spent=done or t.archived)
            dep = c("└─►", "mut") if t.depends_on else "   "
            rows.append((band_row(
                (c("▏" + ARCHIVED_MARK, "ash") if t.archived
                 else c("▏ ", "dim") if done else c("▎ ", "dim")) + " "
                + title_markup(t, max(0, geo.label_w - 3 + over - 3), t.id == selected_id) + dep,
                reach, tail, offset=over), t.id))

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
    lines.append(line(_pad(_scale_with_note(geo, inner, note, months) if note
                           else _scale_row(geo, inner, months), inner)))
    lines.append(bottom(None, w))
    return to_text(lines, height, w, pinned=1)


# ---------------------------------------------------------------------------
# view: FOCUS  (pinned tasks and tasks of pinned projects, three presentations)
# ---------------------------------------------------------------------------

# Highlight syntax for notes inside the Focus Board. The delimiters are chosen
# to be easy to type and unlikely to collide with ordinary markdown/URLs.
_HIGHLIGHT_RE = re.compile(r"==(.*?)==|!!(.*?)!!|\+\+(.*?)\+\+")


def _highlight_markup(text: str) -> str:
    """Render ==text== (yellow), !!text!! (red), ++text++ (green). The
    non-highlighted text is returned in the 'mut' tone so the caller can use the
    result directly without wrapping it again."""
    parts: list[str] = []
    last = 0
    for m in _HIGHLIGHT_RE.finditer(text):
        if m.start() > last:
            parts.append(c(escape(text[last:m.start()]), "mut"))
        inner = escape(m.group(1) or m.group(2) or m.group(3))
        if m.group(1) is not None:
            parts.append(c(inner, "soon"))
        elif m.group(2) is not None:
            parts.append(c(inner, "over"))
        else:
            parts.append(c(inner, "green"))
        last = m.end()
    if last < len(text):
        parts.append(c(escape(text[last:]), "mut"))
    return "".join(parts) if parts else c(escape(text), "mut")


def _focus_note_snippet(notes: str, width: int) -> str:
    """First non-empty note line with inline highlights; empty -> empty string."""
    if not notes or not notes.strip():
        return ""
    lines = [ln.strip() for ln in notes.splitlines() if ln.strip()]
    if not lines:
        return ""
    text = lines[0]
    if len(lines) > 1:
        text += " …"
    return _highlight_markup(clip(text, width))


def _focus_attachments(task: Task, width: int) -> str:
    """Image / URL counts, or empty when the task has neither."""
    parts: list[str] = []
    if task.images:
        parts.append(c(f"▤ {len(task.images)} image{'s' if len(task.images) != 1 else ''}",
                       "mut"))
    if task.urls:
        parts.append(c(f"↗ {len(task.urls)} url{'s' if len(task.urls) != 1 else ''}",
                       "accent"))
    if not parts:
        return ""
    body = "  ".join(parts)
    # truncate as a unit so counts never read as a lie
    return c(escape(clip(body, width)), "mut") if vis(body) > width else body


def _focus_detail_lines(board: Board, task: Task, today: date, width: int) -> list[str]:
    """Right-pane lines for the inspector presentation. Each line is exactly
    `width` visual cells once markup is stripped."""
    out: list[str] = []
    p = board.project_by_id(task.project_id)
    pname = p.name if p else "Inbox"
    pcol = p.color if p else "dim"

    out.append(c(escape(fit(clip(task.title, width), width)), "ink", bold=True))

    dt, dcol = date_chip(task, today, board)
    sg, sgcol = status_glyph(board, task)
    meta = (c(f"Project: {escape(fit(clip(pname, max(0, width - 24)), max(0, width - 24)))}",
              pcol)
            + "  " + c(dt, dcol) + "  " + c(sg, sgcol))
    out.append(meta + " " * max(0, width - vis(_strip(meta))))

    notes = (task.notes or "").strip()
    out.append(c(escape(fit("Notes", width)), "hd", bold=True))
    if notes:
        for ln in notes.splitlines()[:8]:
            stripped = ln.strip()
            if stripped:
                plain = clip(stripped, width)
                rendered = _highlight_markup(plain)
                out.append(rendered + " " * max(0, width - vis(plain)))
    else:
        out.append(c(escape(fit("No notes", width)), "dim"))

    if task.urls:
        out.append(c(escape(fit("URLs", width)), "hd", bold=True))
        for u in task.urls[:5]:
            out.append(c(escape(fit(clip(u, width), width)), "accent"))

    if task.images:
        out.append(c(escape(fit(f"Images ({len(task.images)})", width)), "hd", bold=True))
        for img in task.images[:5]:
            out.append(c(escape(fit(clip(img, width), width)), "mut"))

    open_boxes = len(re.findall(r"^\s*[-*]\s+\[ \]", notes, re.M))
    done_boxes = len(re.findall(r"^\s*[-*]\s+\[[xX]\]", notes, re.M))
    if open_boxes or done_boxes:
        out.append(c(escape(fit(f"Checklist: {done_boxes}/{open_boxes + done_boxes}",
                                width)),
                     "hd", bold=True))

    return out


def _focus_cards(board: Board, tasks: list[Task], selected_id: str | None,
                 today: date, inner: int, line_map: dict | None) -> list[str]:
    """Card-stream presentation: one vertical card per pinned task."""
    lines: list[str] = []
    if not tasks:
        return [line(c(fit("  (no pinned tasks — press 't' on a task to pin it)",
                           inner), "dim"))]
    for t in tasks:
        sel = t.id == selected_id
        p = board.project_by_id(t.project_id)
        pcol = p.color if p else "dim"
        spine = c("▌" if sel else "▎", pcol)
        lines.append(line(spine + " " + title_markup(t, max(0, inner - 3), sel)))
        if line_map is not None:
            line_map[t.id] = len(lines) - 1

        dt, dcol = date_chip(t, today, board)
        sg, sgcol = status_glyph(board, t)
        meta = c(dt, dcol) + "  " + c(sg, sgcol)
        lines.append(line("  " + meta))

        note = _focus_note_snippet(t.notes, max(0, inner - 4))
        if note:
            lines.append(line("  " + note))

        att = _focus_attachments(t, max(0, inner - 4))
        if att:
            lines.append(line("  " + att))

        lines.append(line(c("─" * max(0, inner), "frame")))
    return lines


def _image_thumbnail_markup(path: str, width: int = 18, height: int = 4) -> str:
    """Render a local image as a tiny half-block thumbnail in Rich markup.

    Returns an empty string for remote URLs, missing files, or any load error.
    The caller decides whether to fall back to a text counter.
    """
    if not path or valid_url(path):
        return ""
    p = Path(path)
    if not p.is_file():
        return ""
    try:
        from PIL import Image as PilImage
        img = PilImage.open(p).convert("RGB")
        img = img.resize((width, height))
    except Exception:          # malformed image, missing codec, etc.
        return ""
    rows: list[str] = []
    for y in range(0, height, 2):
        parts: list[str] = []
        for x in range(width):
            r1, g1, b1 = img.getpixel((x, y))
            if y + 1 < height:
                r2, g2, b2 = img.getpixel((x, y + 1))
            else:
                r2 = g2 = b2 = 0
            fg = f"#{r1:02x}{g1:02x}{b1:02x}"
            bg = f"#{r2:02x}{g2:02x}{b2:02x}"
            parts.append(f"[{fg} on {bg}]▀[/]")
        rows.append("".join(parts))
    return "\n".join(rows)


def _focus_tiles(board: Board, tasks: list[Task], selected_id: str | None,
                 today: date, inner: int, line_map: dict | None,
                 show_project_headers: bool = True) -> list[str]:
    """Tile-grid presentation: large, dense project-framed cards.

    Each tile is 58 cells wide and 11 rows tall, grouped under project headers.
    It shows title, project, priority/status, phase, dates, three note lines
    with highlights, checklist progress, and either a tiny half-block image
    thumbnail or attachment names.
    """
    lines: list[str] = []
    if not tasks:
        return [line(c(fit("  (no pinned tasks — press 't' on a task to pin it)",
                           inner), "dim"))]

    TILE_W = 58
    GAP = 1
    cols = max(1, inner // (TILE_W + GAP))
    content_w = TILE_W - 1          # space left of the right-hand frame/border

    def pad_right(markup: str, width: int) -> str:
        stripped = _strip(markup)
        pad = width - vis(stripped)
        if pad > 0:
            return markup + " " * pad
        return markup

    def tile_lines(t: Task) -> list[str]:
        sel = t.id == selected_id
        p = board.project_by_id(t.project_id)
        pcol = p.color if p else "dim"
        pname = p.name if p else "Inbox"

        top = c("█" * TILE_W, pcol) if sel else c("─" * TILE_W, pcol)
        bottom = c("█" * TILE_W, pcol) if sel else c("━" * TILE_W, pcol)
        spine = c("█" if sel else "▌", pcol)

        title = title_markup(t, content_w - 1, sel, arrow=False)
        title_line = spine + " " + title

        sg, sgcol = status_glyph(board, t)
        flags = [c(sg, sgcol)]
        if t.priority == "high":
            flags.append(c("high", "over"))
        if t.blocked:
            flags.append(c("blocked", "over"))
        if t.archived:
            flags.append(c("arch", "ash"))
        project_line = (spine + " "
                        + pad_right(c(escape(fit(clip(pname, 22), 22)), pcol)
                                    + "  "
                                    + "  ".join(flags), content_w - 1))

        dt, dcol = date_chip(t, today, board)
        date_parts = [c(escape(fit(clip(t.phase or "", 16), 16)), "mut"),
                      c(dt, dcol)]
        if t.start_date:
            date_parts.append(c(f"start {t.start_date}", "dim"))
        if t.due_date:
            date_parts.append(c(f"due {t.due_date}", dcol))
        phase_line = spine + " " + pad_right("  ".join(date_parts), content_w - 1)

        note_rows: list[str] = []
        if t.notes:
            for nl in [ln.strip() for ln in t.notes.splitlines() if ln.strip()][:3]:
                note_rows.append(_highlight_markup(clip(nl, content_w - 2)))
        note_rows += [""] * (3 - len(note_rows))
        note_lines = []
        for nr in note_rows:
            note_lines.append(spine + " "
                              + pad_right(nr if nr else c("·", "dim"),
                                          content_w - 1))

        notes = (t.notes or "").strip()
        open_boxes = len(re.findall(r"^\s*[-*]\s+\[ \]", notes, re.M))
        done_boxes = len(re.findall(r"^\s*[-*]\s+\[[xX]\]", notes, re.M))
        checklist_parts: list[str] = []
        if open_boxes or done_boxes:
            checklist_parts.append(c(f"☑ {done_boxes}/{open_boxes + done_boxes}", "hd"))
            for ln in notes.splitlines():
                m = re.match(r"^\s*[-*]\s+\[ \]\s*(.*)", ln)
                if m:
                    item = m.group(1).strip()
                    checklist_parts.append(c(escape(clip(item, 28)), "mut"))
                    break
        checklist_line = (spine + " "
                          + pad_right("  ".join(checklist_parts) if checklist_parts
                                      else c("·", "dim"), content_w - 1))

        # Try a tiny half-block thumbnail for the first local image; fall back
        # to text counters for URLs / missing files.
        media_lines: list[str] = []
        thumb_rendered = False
        if t.images:
            candidate = Path(t.images[0])
            if not candidate.is_file() and board.path:
                candidate = board.image_dir(t.id) / t.images[0]
            if candidate.is_file():
                thumb = _image_thumbnail_markup(str(candidate), width=18, height=4)
                if thumb:
                    for tl in thumb.splitlines():
                        media_lines.append(spine + " "
                                           + pad_right(tl, content_w - 1))
                    thumb_rendered = True

        if not thumb_rendered:
            attach_lines: list[str] = []
            if t.images:
                attach_lines.append(f"▤ {len(t.images)} image{'s' if len(t.images) != 1 else ''}")
                first_img = Path(t.images[0]).name
                attach_lines.append(escape(fit(clip(first_img, content_w - 4), content_w - 4)))
            elif t.urls:
                attach_lines.append(f"↗ {len(t.urls)} url{'s' if len(t.urls) != 1 else ''}")
                first_url = escape(clip(t.urls[0], content_w - 4))
                attach_lines.append(first_url)
            if attach_lines:
                media_lines.append(spine + " "
                                   + pad_right(c(attach_lines[0], "mut"),
                                               content_w - 1))
                media_lines.append(spine + " "
                                   + pad_right(c(attach_lines[1],
                                                  "accent" if t.urls else "mut"),
                                               content_w - 1))
            else:
                media_lines.append(spine + " "
                                   + pad_right(c("·", "dim"), content_w - 1))

        # keep every tile exactly the same height
        while len(media_lines) < 2:
            media_lines.append(spine + " " + " " * (content_w - 1))

        return [top, title_line, project_line, phase_line,
                note_lines[0], note_lines[1], note_lines[2],
                checklist_line, media_lines[0], media_lines[1], bottom]

    last_project_id = None
    for i in range(0, len(tasks), cols):
        row_tasks = tasks[i:i + cols]
        first = row_tasks[0]

        # project header when the owning project changes
        if show_project_headers and first.project_id != last_project_id:
            p = board.project_by_id(first.project_id)
            pcol = p.color if p else "dim"
            pname = p.name if p else "Inbox"
            header = c(f"▐ {escape(pname)}", pcol, bold=True)
            header_pad = " " * max(0, inner - vis(_strip(header)))
            lines.append(line(header + c(header_pad, "frame")))
            last_project_id = first.project_id

        n = len(row_tasks)
        row_tile_lines = [tile_lines(t) for t in row_tasks]

        # Distribute leftover width as extra space BETWEEN tiles, never as
        # trailing padding. Rich strips trailing spaces on markup lines, which
        # was making the grid ragged on rows that ended with styled text.
        fixed_w = n * TILE_W + (n - 1) * GAP
        slack = max(0, inner - fixed_w)
        gaps = n - 1
        if gaps:
            base, rem = divmod(slack, gaps)
            gap_widths = [GAP + base + (1 if j < rem else 0) for j in range(gaps)]
        else:
            gap_widths = []

        if line_map is not None:
            for t in row_tasks:
                line_map[t.id] = len(lines)
        for r in range(11):
            parts = [tl[r] for tl in row_tile_lines]
            combined = ""
            for j, part in enumerate(parts):
                combined += part
                if j < len(parts) - 1:
                    combined += " " * gap_widths[j]
            lines.append(line(combined))
    return lines


def _focus_review(board: Board, tasks: list[Task], selected_id: str | None,
                  today: date, inner: int, line_map: dict | None) -> list[str]:
    """Review queue: one task full-size left, the rest in a stale-first rail."""
    lines: list[str] = []
    if not tasks:
        return [line(c(fit("  (no pinned tasks — press 't' on a task to pin it)",
                           inner), "dim"))]

    ordered = stale_order(board, tasks, today)
    try:
        idx = next(i for i, t in enumerate(ordered) if t.id == selected_id)
    except StopIteration:
        idx = 0
    t = ordered[idx]
    p = board.project_by_id(t.project_id)
    pcol = p.color if p else "dim"
    pname = p.name if p else "Inbox"

    w_l = min(64, max(24, inner // 2 - 2))
    gap = 3 if inner - w_l - 3 >= 12 else 1
    w_r = max(12, inner - w_l - gap)
    spine = c("█", pcol)

    def pad_m(markup: str, width: int) -> str:
        pad = width - vis(_strip(markup))
        return markup + " " * max(0, pad)

    left_rows: list[str] = [c("█" * w_l, pcol)]
    left_rows.append(spine + " " + c(escape(fit(t.title, w_l - 3)), "ink", bold=True))
    left_rows.append(spine)
    sg, sgcol = status_glyph(board, t)
    flags = [c(sg, sgcol)]
    if t.priority == "high":
        flags.append(c("high", "over"))
    if t.blocked:
        flags.append(c("blocked", "over"))
    left_rows.append(spine + " " + pad_m(
        c(escape(fit(clip(pname, 22), 22)), pcol) + "  " + "  ".join(flags),
        w_l - 1))
    dt, dcol = date_chip(t, today, board)
    when = [c(escape(fit(clip(t.phase or "", 16), 16)), "mut"), c(dt, dcol)]
    if t.start_date:
        when.append(c(f"start {t.start_date}", "dim"))
    if t.due_date:
        when.append(c(f"due {t.due_date}", dcol))
    left_rows.append(spine + " " + pad_m("  ".join(when), w_l - 1))
    left_rows.append(spine)
    note_lines = [ln.strip() for ln in (t.notes or "").splitlines()
                  if ln.strip() and not re.match(r"^\s*[-*]\s+\[", ln)]
    for ln_txt in note_lines[:6]:
        left_rows.append(spine + " " + _highlight_markup(clip(ln_txt, w_l - 3)))
    if not note_lines:
        left_rows.append(spine + " " + c("·", "dim"))
    open_items = [m.group(1).strip()
                  for m in (re.match(r"^\s*[-*]\s+\[ \]\s*(.*)", ln)
                            for ln in (t.notes or "").splitlines()) if m]
    done_n = len(re.findall(r"^\s*[-*]\s+\[[xX]\]",
                            t.notes or "", re.M))
    if open_items or done_n:
        left_rows.append(spine)
        left_rows.append(spine + " " + c(f"☑ {done_n}/{done_n + len(open_items)}", "hd"))
        for item in open_items[:3]:
            left_rows.append(spine + " " + c(escape(clip(item, w_l - 5)), "mut"))
    attach = _focus_attachments(t, w_l - 3)
    if attach:
        left_rows.append(spine)
        left_rows.append(spine + " " + attach)
    left_rows.append(c("━" * w_l, pcol))

    rail_rows: list[tuple[str, str | None]] = [
        (c("QUEUE — stale first", "dim"), None),
        ("", None),
    ]
    for i, q in enumerate(ordered):
        rail_rows.append((card_cell(q, board, w_r, False,
                                    prefix="▸ " if i == idx else "▊ ",
                                    prefix_color="accent" if i == idx
                                    else project_color(board, q),
                                    today=today), q.id))

    title = c("◆ FOCUS", "accent", bold=True) + c(" · review", "mut")
    right = c(f"{idx + 1}/{len(ordered)} · stale first", "mut")
    lines = [header(title, right, inner)]
    selected_line = 1
    n_rows = max(len(left_rows), len(rail_rows))
    for r in range(n_rows):
        lft = pad_m(left_rows[r], w_l) if r < len(left_rows) else " " * w_l
        rgt, tid = rail_rows[r] if r < len(rail_rows) else ("", None)
        lines.append(line(lft + " " * gap + pad_m(rgt, w_r)))
        if line_map is not None:
            if tid and tid != t.id:
                line_map[tid] = len(lines) - 1
    if line_map is not None:
        line_map[t.id] = selected_line
    return lines


def _focus_stale(board: Board, tasks: list[Task], selected_id: str | None,
                 today: date, inner: int, line_map: dict | None) -> list[str]:
    """Stale-first tiles: the shipped tile grid reordered by `stale_order`,
    with a pressure strip and project headers suppressed so the order is honest."""
    lines: list[str] = []
    if not tasks:
        return [line(c(fit("  (no pinned tasks — press 't' on a task to pin it)",
                           inner), "dim"))]

    overdue = [t for t in tasks if urgency(t, today, board) == "overdue"]
    stale = [t for t in tasks
             if (days_in_phase(t, today) or 0) >= 7 and not board.is_done(t)]
    title = c("◆ FOCUS", "accent", bold=True) + c(" · stale first", "mut")
    right = c(f"{len(tasks)} pinned", "mut")
    lines = [header(title, right, inner)]
    lines.append(line(c(f"▲ {len(overdue)} overdue", "over")
                      + c("    ", "dim")
                      + c(f"■ {len(stale)} sitting ≥7d", "soon")
                      + c("    ordered by days in phase", "dim")))
    ordered = stale_order(board, tasks, today)
    lines += _focus_tiles(board, ordered, selected_id, today, inner, line_map,
                          show_project_headers=False)
    return lines


# ---------------------------------------------------------------------------
# view: SEARCH overlay (used by kanban + gantt)
# ---------------------------------------------------------------------------
_SEARCH_CONSOLE = Console(force_terminal=True, color_system="truecolor",
                          width=9999, height=9999)
_SEARCH_CONT = Style(dim=True)


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


def filtered_board(board: Board, query: str, show_archived: bool) -> Board:
    """A shallow Board whose tasks/projects are the query's hits.

    The real views render it untouched; this is the seat of filtering so the
    tally and the hidden lanes stay coherent by construction."""
    q = query.lower()
    proxy = copy.copy(board)
    proxy.tasks = [t for t in board.visible_tasks(show_archived)
                   if matches(t, board, q)]
    keep = {t.project_id for t in proxy.tasks}
    proxy.projects = [p for p in board.visible_projects(show_archived)
                      if p.id in keep]
    return proxy


def filter_bar(query: str, hits: int, total: int, w: int) -> list[str]:
    """The `/` bar: query + cursor left, tally right."""
    left = c("/", "accent", bold=True) + " " + escape(query) + c("▌", "accent")
    right = c(f"{hits}/{total} tasks", "mut") + c(" · esc clears", "dim")
    return [header(left, right, w), head_rule(w)]


def _search_to_grid(text: Text, w: int, h: int) -> list[list[list]]:
    """A rendered Text -> (char, style) grid, one cell per screen column."""
    grid: list[list[list]] = []
    for ln in text.split("\n"):
        row: list[list] = []
        for seg in ln.render(_SEARCH_CONSOLE):
            for ch in seg.text:
                if ch == "\n":
                    continue
                row.append([ch, seg.style])
                for _ in range(cell_len(ch) - 1):
                    row.append(["", _SEARCH_CONT])
        grid.append((row + [[" ", None]] * w)[:w])
    while len(grid) < h:
        grid.append([[" ", None]] * w)
    return grid[:h]


def _search_grid_text(grid: list[list[list]]) -> Text:
    """Grid back to a Text, merging same-style runs."""
    t = Text()
    for ri, row in enumerate(grid):
        run: list[str] = []
        run_st = None
        for ch, st in row + [["", _SEARCH_CONT]]:
            if st is not run_st:
                if run:
                    t.append("".join(run), style=run_st)
                run, run_st = ([], None) if st is _SEARCH_CONT else ([ch], st)
            else:
                run.append(ch)
        if ri < len(grid) - 1:
            t.append("\n")
    return t


def _highlight_grid(grid: list[list[list]], query: str) -> None:
    """Reverse-video every case-insensitive occurrence of `query`."""
    q = query.lower()
    if not q:
        return
    for row in grid:
        s = "".join(ch for ch, _ in row).lower()
        start = 0
        while True:
            i = s.find(q, start)
            if i < 0:
                break
            for j in range(i, min(i + len(q), len(row))):
                ch, st = row[j]
                if st is _SEARCH_CONT:
                    continue
                row[j][1] = (Style.combine([st, Style(reverse=True)])
                             if st else Style(reverse=True))
            start = i + len(q)


def _apply_search_overlay(text: Text, query: str, hits: int, total: int,
                          w: int) -> Text:
    """Insert the `/` bar under the view header and reverse-lit matches."""
    lines = text.split("\n")
    h = len(lines)
    grid = _search_to_grid(text, w, h)
    _highlight_grid(grid, query)
    bar_text = Text.from_markup("\n".join(filter_bar(query, hits, total, w)),
                                emoji=False)
    bar_grid = _search_to_grid(bar_text, w, 2)
    grid = [grid[0]] + bar_grid + grid[1:]
    return _search_grid_text(grid)


def _focus_inspector(board: Board, tasks: list[Task], selected_id: str | None,
                     today: date, inner: int, line_map: dict | None) -> list[str]:
    """Two-pane presentation: list left, detail right."""
    lines: list[str] = []
    if not tasks:
        return [line(c(fit("  (no pinned tasks — press 't' on a task to pin it)",
                           inner), "dim"))]

    ids = {t.id for t in tasks}
    selected = board.task_by_id(selected_id)
    if selected is None or selected.id not in ids:
        selected = tasks[0]

    left_w = max(12, inner // 3)
    right_w = inner - left_w - 1
    sep = c("│", "frame")

    left_rows: list[tuple[str, str]] = []
    for t in tasks:
        sel = t.id == selected.id
        p = board.project_by_id(t.project_id)
        pcol = p.color if p else "dim"
        spine = c("▌" if sel else "▎", pcol)
        left_rows.append((spine + " " + title_markup(t, max(0, left_w - 3), sel),
                          t.id))

    right_lines = _focus_detail_lines(board, selected, today, max(0, right_w))

    max_rows = max(len(left_rows), len(right_lines))
    for i in range(max_rows):
        lpart, tid = left_rows[i] if i < len(left_rows) else (" " * left_w, None)
        rpart = right_lines[i] if i < len(right_lines) else " " * right_w
        lines.append(line(lpart + sep + rpart))
        if tid is not None and line_map is not None:
            line_map[tid] = len(lines) - 1
    return lines


def _focus_image_card(board: Board, t: Task, selected_id: str | None,
                      today: date, inner: int) -> list[str]:
    """A compact card for the image-first presentation."""
    sel = t.id == selected_id
    p = board.project_by_id(t.project_id)
    pcol = p.color if p else "dim"
    spine = c("▌" if sel else "▎", pcol)
    dt, dcol = date_chip(t, today, board)
    title = title_markup(t, max(0, inner - 4 - 6), sel)
    row1 = spine + " " + title + " " + c(fit(dt, 6, "right"), dcol)
    img_text = f"🖼 {len(t.images)} image{'s' if len(t.images) != 1 else ''}"
    row2 = "  " + c(escape(clip(img_text, max(0, inner - 4))), "mut")
    return [line(row1), line(row2)]


def _focus_compact_card(board: Board, t: Task, selected_id: str | None,
                        today: date, inner: int) -> list[str]:
    """A single-line card for image-first tasks without images."""
    sel = t.id == selected_id
    p = board.project_by_id(t.project_id)
    pcol = p.color if p else "dim"
    spine = c("▌" if sel else "▎", pcol)
    dt, dcol = date_chip(t, today, board)
    title = title_markup(t, max(0, inner - 4 - 6), sel)
    return [line(spine + " " + title + " " + c(fit(dt, 6, "right"), dcol))]


def _focus_images(board: Board, tasks: list[Task], selected_id: str | None,
                  today: date, inner: int, line_map: dict | None) -> list[str]:
    """Image-first presentation: tasks with images lead, then compact rows."""
    lines: list[str] = []
    if not tasks:
        return [line(c(fit("  (no pinned tasks — press 't' on a task to pin it)",
                           inner), "dim"))]

    with_img = [t for t in tasks if t.images]
    without = [t for t in tasks if not t.images]

    if with_img:
        label = f" with images ({len(with_img)}) "
        lines.append(line(c(label, "hd")
                          + c("─" * max(0, inner - vis(label)), "frame")))
        for t in with_img:
            base = len(lines)
            for cl in _focus_image_card(board, t, selected_id, today, inner):
                lines.append(cl)
            if line_map is not None:
                line_map[t.id] = base

    if without:
        label = f" without images ({len(without)}) "
        lines.append(line(c(label, "hd")
                          + c("─" * max(0, inner - vis(label)), "frame")))
        for t in without:
            base = len(lines)
            for cl in _focus_compact_card(board, t, selected_id, today, inner):
                lines.append(cl)
            if line_map is not None:
                line_map[t.id] = base

    return lines


def render_focus(board, show_archived, selected_id, today=None,
                 width=68, height=0, line_map=None, presentation="tiles") -> Text:
    """The Focus Board: pinned tasks and tasks of pinned projects.

    Presentations:
      * "tiles"    — responsive tile grid with project-coloured frames
      * "inspector"— two-pane list + detail
      * "images"   — image tasks first, then compact list
      * "review"   — one full-size task + stale-first queue rail
      * "stale"    — tile grid ordered stale-first with a pressure strip
    """
    today = today or date.today()
    w = _clamp_width(width)
    inner = w
    tasks = focus_tasks(board, show_archived)

    if presentation == "review":
        lines = _focus_review(board, tasks, selected_id, today, inner, line_map)
        lines.append(bottom(None, w))
        return to_text(lines, height, w)
    if presentation == "stale":
        lines = _focus_stale(board, tasks, selected_id, today, inner, line_map)
        lines.append(bottom(None, w))
        return to_text(lines, height, w)

    tasks.sort(key=lambda t: _focus_sort_key(board, show_archived, t, today))

    right = c(f"{len(tasks)} pinned", "mut")
    title = c("◆ FOCUS", "accent", bold=True) + c(f" · {presentation}", "mut")
    lines = [header(title, right, w)]

    if presentation == "inspector":
        lines += _focus_inspector(board, tasks, selected_id, today, inner, line_map)
    elif presentation == "images":
        lines += _focus_images(board, tasks, selected_id, today, inner, line_map)
    elif presentation == "tiles":
        lines += _focus_tiles(board, tasks, selected_id, today, inner, line_map)
    else:  # legacy "cards" alias, kept for old tests / external callers
        lines += _focus_cards(board, tasks, selected_id, today, inner, line_map)

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


def _windowed_header(board: Board, start: int, widths: list[int],
                     tasks: list[Task]) -> list[str]:
    """Phase-name header cells, with `◀ N` / `N ▶` counts for hidden phases.

    Every cell ends with the WIP tag (HLR-005, LLR-005.2): ` n/limit` when the
    phase has a limit, bare ` n` when it does not — `n` counted from
    `phase_buckets` over the view's visible tasks. The tag is laid out LAST
    and the phase name is truncated BEFORE it, so the count survives width
    pressure (the tag-last layout of the approved proto). It burns in the
    `over` tone ONLY when strictly over the limit — exactly AT the limit is
    calm (the off-by-one is the cheapest mutation here)."""
    n, end = len(board.phases), start + len(widths)
    buckets = phase_buckets(board, tasks)
    cells = []
    for i, wc in enumerate(widths):
        phase = board.phases[start + i]
        count = len(buckets[start + i])
        limit = board.wip_limit(phase)
        tag = f" {count}/{limit}" if limit is not None else f" {count}"
        tone = "over" if (limit is not None and count > limit) else "mut"
        pre = f"◀ {start} " if (i == 0 and start > 0) else ""
        suf = f" {n - end} ▶" if (i == len(widths) - 1 and end < n) else ""
        avail = wc - len(pre) - len(suf)
        if avail < 1:                       # no room for a label -> markers only
            cells.append(c(fit((pre + suf).strip(), wc), "mut"))
            continue
        name_w = max(0, avail - vis(tag))   # the tag survives width pressure
        cells.append(c(pre, "mut")
                     + c(escape(fit(phase.upper(), name_w)), "hd", bold=True)
                     + c(fit(tag, avail - name_w), tone)
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


# --- THE ONE ordering seat (HLR-003/HLR-004, LLR-003.1) -----------------------
# Sort and group modes are VIEW state, held on the app and passed in. This seat
# answers "in what order do this column's tasks appear" for BOTH the renderer
# and the navigator — the batch's named trap is a second ordering site that
# silently keeps the default, so there is exactly one function and two callers.
_KANBAN_SORT_MODES = ("project", "priority", "due", "recent")
_KANBAN_GROUP_MODES = ("project", "priority", "horizon")
_PRIO_RANK = {"high": 0, "normal": 1, "low": 2}


def _recent_first(tasks: list[Task]) -> list[Task]:
    """`phase_changed` newest first, unknown stamps sunk, ties in board order
    (ISO date stamps sort lexicographically; sorted() is stable, and `reverse`
    does not disturb equal keys). None is UNKNOWN and sinks — never read as 0."""
    return sorted(tasks, key=lambda t: t.phase_changed or "", reverse=True)


def kanban_order(board, tasks, show_archived, *, group="project",
                 sort="project", collapsed=False, focus=None,
                 today=None) -> list[tuple[str, str, list[Task]]]:
    """The ordered `(name, color, tasks)` groups for ONE kanban column, under
    the active group/sort modes. Pure: no I/O, no mutation of `board`/`tasks`.

    Sort (intra-group, ALL modes STABLE — a tie the keys leave open keeps the
    board's pre-sort order, §6.5 AMD-09): `project` = board order as given;
    `priority` = blocked first, then high→normal→low, ties by due (undated
    sink); `due` = `sort_by_due` semantics with blocked first; `recent` =
    `_recent_first`. Group: `project` = `_kanban_groups` verbatim (Inbox
    last); `priority` = High/Normal/Low; `horizon` = Overdue/This week/Later/
    No date by `urgency()`, plus a trailing `Done` group — dim tone, its OWN
    pinned `phase_changed`-desc order regardless of the sort mode (§6.5
    AMD-04/D-11: `urgency()` reports done before reading any date). Empty
    groups are omitted — an empty group header is a ghost mark."""
    if collapsed:            # a collapsed column contributes NOTHING (R-07)
        return []
    if focus is not None:    # a project focus hides every other project (R-08)
        tasks = [t for t in tasks if t.project_id == focus]
    pinned: str | None = None
    if group == "priority":
        groups = [(label, color, [t for t in tasks if t.priority == value])
                  for value, label, color in (("high", "High", "over"),
                                              ("normal", "Normal", "mut"),
                                              ("low", "Low", "dim"))]
        groups = [g for g in groups if g[2]]
    elif group == "horizon":
        today = today or date.today()
        buckets: dict[str, list[Task]] = {"overdue": [], "week": [],
                                          "later": [], "none": [], "done": []}
        for t in tasks:
            u = urgency(t, today, board)
            buckets["week" if u == "today" else u].append(t)
        groups = [(label, color, buckets[key])
                  for key, label, color in (("overdue", "Overdue", "over"),
                                            ("week", "This week", "accent"),
                                            ("later", "Later", "mut"),
                                            ("none", "No date", "dim"))]
        groups = [g for g in groups if g[2]]
        if buckets["done"]:
            pinned = "Done"
            groups.append(("Done", "dim", _recent_first(buckets["done"])))
    else:                    # "project" — today's grouping, Inbox last
        groups = _kanban_groups(board, tasks, show_archived)
    if sort == "project":
        return groups
    if sort == "recent":
        def order(items: list[Task]) -> list[Task]:
            return _recent_first(items)
    elif sort == "priority":
        def order(items: list[Task]) -> list[Task]:
            return sorted(items, key=lambda t: (
                not t.blocked, _PRIO_RANK.get(t.priority, 1),
                parse_iso(t.due_date) is None,
                parse_iso(t.due_date) or date.max))
    else:                    # "due" — sort_by_due semantics, blocked first
        def order(items: list[Task]) -> list[Task]:
            return sorted(items, key=lambda t: (
                not t.blocked, parse_iso(t.due_date) is None,
                parse_iso(t.due_date) or date.max))
    return [(name, color, items if name == pinned else order(items))
            for name, color, items in groups]


def _kanban_column_rows(board, tasks, wc, selected_id,
                        show_archived, *, group="project", sort="project",
                        collapsed=False, focus=None,
                        today=None) -> list[tuple[str, str | None]]:
    """(markup, task-id) rows for ONE phase column: a coloured group header
    followed by EVERY one of that group's tasks in this phase, in THE shared
    seat's order (`kanban_order` — never a second ordering). A COLLAPSED
    column (LLR-007.1: only ever THE LAST phase, §6.5 AMD-02) emits exactly
    one `(markup, None)` summary row — `✓ N`, N the phase's visible task
    count — the existing non-selectable row convention, no new row kind.
    The flag still goes THROUGH the seat: collapsed, `kanban_order` returns
    no groups, so the loop below contributes zero rows and the summary is
    the only one."""
    rows: list[tuple[str, str | None]] = []
    for name, color, items in kanban_order(board, tasks, show_archived,
                                           group=group, sort=sort,
                                           collapsed=collapsed, focus=focus,
                                           today=today):
        rows.append((c("▐ ", color) + c(escape(fit(name, max(0, wc - 2))), color, bold=True),
                     None))
        for t in items:
            rows.append((card_cell(t, board, wc, t.id == selected_id,
                                   prefix="▲ " if t.blocked else "▊ ",
                                   prefix_color="over" if t.blocked
                                   else project_color(board, t),
                                   today=today), t.id))
    if collapsed:
        # `✓` is the done mark and the done house is its only honest home —
        # and on the terminal phase every visible task IS done, so the mark
        # never lies (HLR-007).
        rows.append((c(fit(f"✓ {len(tasks)}", wc), "done"), None))
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


def _kanban_grouped(board, show_archived, selected_id, today, w, height, line_map,
                    *, sort="project", group="project", collapsed=False,
                    focus=None) -> list[str]:
    inner = w
    tasks = board.visible_tasks(show_archived)
    focused = board.project_by_id(focus) if focus is not None else None
    if focused is not None:
        # The cards are filtered by the seat (kanban_order); scoping the
        # INPUT here keeps the header counts and the task tally describing
        # what the board actually draws — a tally of hidden cards is a lie.
        tasks = [t for t in tasks if t.project_id == focus]
    start, widths = _phase_window(board, inner, board.task_by_id(selected_id))
    buckets = phase_buckets(board, tasks)
    sep = c("│", "frame")

    right = c(f"{len(tasks)} tasks", "mut")
    mode = c(" · grouped", "mut")
    if sort != "project":        # a non-default mode is NAMED (LLR-003.2) —
        mode += c(f" · sort: {sort}", "mut")     # an unnamed mode is a lie
    if group != "project":
        mode += c(f" · group: {group}", "mut")
    if focused is not None:      # the focus is a mode too: it is NAMED (R-08),
        mode += (c(" · focus: ", "mut")          # with the user's own text
                 + c(escape(focused.name), "mut"))  # escaped like everywhere
    lines = [header(c("KANBAN", "accent", bold=True) + mode, right, w)]
    lines.append(line(sep.join(_windowed_header(board, start, widths, tasks))))
    lines.append(rule_row(_col_junctions(widths, "┼"), w))

    last = len(board.phases) - 1
    cols = [_kanban_column_rows(board, buckets[start + i], wc, selected_id,
                                show_archived, group=group, sort=sort,
                                collapsed=collapsed and start + i == last,
                                focus=focus, today=today)
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
                      + sep.join(_windowed_header(board, start, widths, tasks)) + sep
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


def _kanban_cell_order(board, tasks, sort, today):
    """Flat ordering for the cards inside ONE lane×phase cell."""
    if sort == "project":
        return list(tasks)
    if sort == "recent":
        return _recent_first(tasks)
    if sort == "priority":
        return sorted(tasks, key=lambda t: (
            not t.blocked, _PRIO_RANK.get(t.priority, 1),
            parse_iso(t.due_date) is None,
            parse_iso(t.due_date) or date.max))
    # "due" — sort_by_due semantics, blocked first
    return sorted(tasks, key=lambda t: (
        not t.blocked, parse_iso(t.due_date) is None,
        parse_iso(t.due_date) or date.max))


def _kanban_lanes(board, show_archived, selected_id, today, w, height, line_map,
                  *, sort="project", group="project", collapsed=False,
                  focus=None) -> list[str]:
    """Third kanban presentation: lanes (one per active group) × phase columns.

    The lane is the current `kanban_group` (`project`, `priority` or `horizon`).
    Empty lanes are omitted, overflowing cells close with `+N more`, and every
    card keeps the real `card_cell` indicators."""
    inner = w
    tasks = board.visible_tasks(show_archived)
    focused = board.project_by_id(focus) if focus is not None else None
    if focused is not None:
        tasks = [t for t in tasks if t.project_id == focus]
    selected = board.task_by_id(selected_id)
    label_w = 18
    grid_w = max(0, inner - label_w - 1)
    start, widths = _phase_window(board, grid_w, selected)
    n_ph = len(widths)
    sep = c("│", "frame")
    juncs = _matrix_junctions(label_w, widths, "┼")
    feet = {k: "┴" for k in juncs}

    lanes = kanban_order(board, tasks, show_archived, group=group, sort=sort,
                         collapsed=collapsed, focus=focus, today=today)

    right = c(f"{len(tasks)} tasks", "mut")
    mode = c(" · lanes", "mut")
    if group != "project":
        mode += c(f" · group: {group}", "mut")
    if sort != "project":
        mode += c(f" · sort: {sort}", "mut")
    if focused is not None:
        mode += (c(" · focus: ", "mut")
                 + c(escape(focused.name), "mut"))
    lines = [header(c("KANBAN", "accent", bold=True) + mode, right, w)]
    lines.append(line(" " * label_w + sep
                      + sep.join(_windowed_header(board, start, widths, tasks))))
    lines.append(rule_row(juncs, w))

    ph_idx = {ph: i for i, ph in enumerate(board.phases)}
    max_needed = 0
    lane_buckets: list[list[list[Task]]] = []
    for _name, _color, lane_tasks in lanes:
        buckets: list[list[Task]] = [[] for _ in range(n_ph)]
        for t in lane_tasks:
            pidx = ph_idx.get(t.phase, 0) - start
            if 0 <= pidx < n_ph:
                buckets[pidx].append(t)
        for b in buckets:
            b[:] = _kanban_cell_order(board, b, sort, today)
            max_needed = max(max_needed, len(b))
        lane_buckets.append(buckets)

    chrome = 4  # header + phase header + rule + bottom rule
    if height <= chrome or not lanes:
        lane_h = max(1, max_needed)
    else:
        avail = max(0, height - chrome - (len(lanes) - 1))
        lane_h = max(1, avail // max(1, len(lanes)))

    for li, ((name, color, _lane_tasks), buckets) in enumerate(zip(lanes, lane_buckets)):
        def cell_rows(bucket: list[Task], wc: int) -> list[tuple[str, str | None]]:
            cap = lane_h
            shown = bucket if len(bucket) <= cap else bucket[:cap - 1]
            rows: list[tuple[str, str | None]] = [
                (card_cell(t, board, wc, t.id == selected_id,
                           prefix="▊ ",
                           prefix_color=project_color(board, t),
                           today=today), t.id)
                for t in shown]
            if len(bucket) > cap:
                rows.append((c(fit(f"+{len(bucket) - cap + 1} more", wc), "dim"), None))
            rows += [(" " * wc, None)] * (lane_h - len(rows))
            return rows[:lane_h]

        cells = [cell_rows(buckets[i], widths[i]) for i in range(n_ph)]
        for r in range(lane_h):
            if r == 0:
                label = (c("▐ ", color)
                         + c(escape(fit(name.upper(), label_w - 2)), color, bold=True))
            elif r == 1:
                label = c(fit(f"  {len(_lane_tasks)}", label_w), "dim")
            else:
                label = " " * label_w
            row = label + sep + sep.join(cells[i][r][0] for i in range(n_ph))
            lines.append(line(row))
            if line_map is not None:
                for i in range(n_ph):
                    tid = cells[i][r][1]
                    if tid:
                        line_map[tid] = len(lines) - 1
        if li < len(lanes) - 1:
            lines.append(rule_row(juncs, w))

    lines.append(rule_row(feet, w))
    return lines


def render_kanban(board, show_archived, selected_id, today=None,
                  width=68, height=0, line_map=None, presentation="grouped",
                  sort="project", group="project", collapsed=False,
                  focus=None) -> Text:
    today = today or date.today()
    w = _clamp_width(width)
    if presentation == "matrix":     # matrix presentation sorting: out of scope
        lines = _kanban_matrix(board, show_archived, selected_id, today, w,
                               height, line_map)
    elif presentation == "lanes":
        lines = _kanban_lanes(board, show_archived, selected_id, today, w,
                              height, line_map, sort=sort, group=group,
                              collapsed=collapsed, focus=focus)
    else:
        lines = _kanban_grouped(board, show_archived, selected_id, today, w,
                                height, line_map, sort=sort, group=group,
                                collapsed=collapsed, focus=focus)
    return to_text(lines, height, w)


# ---------------------------------------------------------------------------
# dispatcher
# ---------------------------------------------------------------------------
RENDERERS = {
    "swimlanes": render_swimlanes,
    "agenda": render_agenda,
    "gantt": render_gantt,
    "kanban": render_kanban,
    "focus": render_focus,
}


def render_view(mode, board, show_archived, selected_id, today=None,
                width=68, height=0, line_map=None, presentation="grouped", tick=0,
                kanban_sort="project", kanban_group="project",
                kanban_collapsed=False, kanban_focus=None,
                gantt_focus=None, focus_presentation="cards",
                search_query: str | None = None) -> Text:
    query = (search_query or "").strip()
    w = _clamp_width(width)
    if mode == "focus":
        return render_focus(board, show_archived, selected_id, today, width, height,
                            line_map, presentation=focus_presentation)
    if mode == "kanban":
        if query:
            fb = filtered_board(board, query, show_archived)
            total = len(board.visible_tasks(show_archived))
            hits = len(fb.visible_tasks(show_archived))
            text = render_kanban(fb, show_archived, selected_id, today, width, height,
                                 line_map, presentation, sort=kanban_sort,
                                 group=kanban_group, collapsed=kanban_collapsed,
                                 focus=kanban_focus)
            if line_map is not None:
                for tid in list(line_map.keys()):
                    line_map[tid] += 2
            return _apply_search_overlay(text, query, hits, total, w)
        return render_kanban(board, show_archived, selected_id, today, width, height,
                             line_map, presentation, sort=kanban_sort,
                             group=kanban_group, collapsed=kanban_collapsed,
                             focus=kanban_focus)
    if mode == "gantt":
        if query:
            fb = filtered_board(board, query, show_archived)
            total = len(board.visible_tasks(show_archived))
            hits = len(fb.visible_tasks(show_archived))
            text = render_gantt(fb, show_archived, selected_id, today, width, height,
                                line_map, tick=tick, focus=gantt_focus)
            if line_map is not None:
                for tid in list(line_map.keys()):
                    line_map[tid] += 2
            return _apply_search_overlay(text, query, hits, total, w)
        return render_gantt(board, show_archived, selected_id, today, width, height,
                            line_map, tick=tick, focus=gantt_focus)
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
    twice with different numbers is how a cursor ends up on an undrawn task.

    THE ROW COST MODEL, in one place, because it was derived three times and
    disagreed with itself each time:

        PANEL (h rows)                 BODY
          1  header                      lead    = prof + 2   [only when active]
          B  body                        stack_i = wrows + min(titles, nameable_i)
          A  absence line, A in {0,1}    rest    = n_rest
          1  axis
          0  close -- `bottom()` returns "", the view being frameless

        room = h - 2 - 2*[active]      need = prof + sum(...) + n_rest
        BODY == need + 2*[active]      2 + BODY + A == h

    THE TWO `2`s ARE NOT THE SAME `2`. The `h - 2` is the panel's OWN CHROME --
    the header and the axis. The `- 2*[active]` is THE LEAD BAND'S head and
    tail, the two rows `allocate` never bills for. Collapse them in either
    direction and the panel overflows (shedding work it should have drawn) or
    pads (on a view whose whole design is that it does not).

    REGIME -- the identity holds when a lane is active AND an allocation fits.
    Outside it two things happen, both documented and neither a defect: with NO
    active lane, `prof` is billed for a bench nothing draws and the view PADS;
    with no feasible allocation, the renderer sheds blocks and says `+N not
    shown`. `tests/test_row_cost.py` pins all three cases."""
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
              height: int = 0, *, selected_id: str | None = None,
              kanban_sort="project",
              kanban_group="project", kanban_collapsed=False,
              kanban_focus=None, gantt_focus=None,
              presentation="grouped", focus_presentation="cards") -> list[list[str]]:
    today = today or date.today()
    tasks = board.visible_tasks(show_archived)

    if mode == "focus":
        pinned = focus_tasks(board, show_archived)
        if focus_presentation in ("review", "stale"):
            ordered = stale_order(board, pinned, today, show_archived)
            return [[t.id for t in ordered]]
        pinned.sort(key=lambda t: _focus_sort_key(board, show_archived, t, today))
        return [[t.id for t in pinned]]

    if mode == "kanban":       # the phase columns, in THE shared seat's order
        # The matrix presentation renders through `_kanban_matrix`, which does
        # NOT consume the modes (render_kanban routes it before the seat): if
        # nav honored sort/group/collapse/focus there, the cursor could park
        # on a task the screen does not draw — the F-3 trap, carried three
        # times (sort/group Inc-006, collapse Inc-008, focus Inc-009) and
        # ruled at Phase 4: in matrix BOTH seats ignore the modes, so the nav
        # walks exactly what the matrix draws.
        if presentation == "matrix":
            kanban_sort, kanban_group = "project", "project"
            kanban_collapsed, kanban_focus = False, None
        # A collapsed terminal phase is ABSENT from the nav model — not an
        # empty column (LLR-007.1): a column that IS there but holds nothing
        # is still a place the horizontal walk can reason about; the collapsed
        # one no longer exists. The flag goes through the seat here too —
        # and so does the focus (R-08): a filter that hid cards from the
        # render but left them in the nav model would park the cursor on a
        # task the board does not draw.
        if presentation == "lanes":
            label_w = 18
            grid_w = max(0, width - label_w - 1)
            selected = board.task_by_id(selected_id)
            start, widths = _phase_window(board, grid_w, selected)
            lanes = kanban_order(board, tasks, show_archived,
                                 group=kanban_group, sort=kanban_sort,
                                 collapsed=kanban_collapsed, focus=kanban_focus,
                                 today=today)
            ph_idx = {ph: i for i, ph in enumerate(board.phases)}
            cols = [[] for _ in widths]
            for _name, _color, lane_tasks in lanes:
                buckets = [[] for _ in widths]
                for t in lane_tasks:
                    pidx = ph_idx.get(t.phase, 0) - start
                    if 0 <= pidx < len(widths):
                        buckets[pidx].append(t)
                for i, bucket in enumerate(buckets):
                    bucket = _kanban_cell_order(board, bucket, kanban_sort, today)
                    cols[i].extend(t.id for t in bucket)
            return cols

        cols = []
        last = len(board.phases) - 1
        for i, bucket in enumerate(phase_buckets(board, tasks)):
            is_collapsed = kanban_collapsed and i == last
            groups = kanban_order(board, bucket, show_archived,
                                  group=kanban_group, sort=kanban_sort,
                                  collapsed=is_collapsed, focus=kanban_focus,
                                  today=today)
            if is_collapsed:
                continue
            cols.append([t.id for _name, _color, items in groups
                         for t in items])
        return cols

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
            if gantt_focus is not None and p.id != gantt_focus:
                continue
            for t in gantt_tasks(board, tasks, p.id):
                (order if _is_dated(t) else unscheduled).append(t.id)
        loose = [t for t in tasks if board.project_by_id(t.project_id) is None]
        if gantt_focus is None:
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
        # the progress mark only exists once something HAS progressed. It was a
        # whole second row (`▓▓▌`) and the legend described it as such; the row
        # is gone and the legend has to stop naming a mark nobody draws — which
        # is exactly what `test_no_entry_describes_a_mark_the_view_is_not_drawing`
        # said the moment the row went.
        if any(board.project_progress(p.id, False) > 0 for p in f["projects"]):
            out.append((c(PROGRESS_DOT, hue), "how far the work actually got"))
            out.append((c(FIELD_REACH + PROGRESS_DOT + FIELD_REACH, hue)
                        + c("◆", hue),
                        "the gap from the dot to ◆: the slip, as a length"))
        if f["project_due"]:
            out.append((c("◆", hue), "the project's own due date"))
        out.append((c(RULE, "accent"), "today"))
        # THE GAUGE. A bar measured against nothing is what the operator called
        # disorder, so the legend has to name what it is measured against.
        #
        # Both entries are derived from the SAME functions the view draws with,
        # at this exact size, so a ghost mark is impossible by construction
        # rather than by a promise: if the geometry stops placing week guides or
        # drops every month name, the entry disappears with it. A hard-coded
        # `"AUG"` would also have passed the ghost test — on the `G` and the `A`
        # in the header's own `◆ GANTT` — which is a check that cannot fail.
        ggeo = gantt_geometry(_clamp_width(width), height or 24)
        gweeks, gmonths = gantt_gauge(ggeo, today)
        if gweeks:
            out.append((c(LATTICE + FIELD_WEEK + LATTICE, "dim"),
                        "the week guide: every dashed rule is a monday"))
        drawn = _scale_cells(ggeo, gmonths)[1]
        if drawn:
            first = min(drawn)
            out.append((c("".join(_scale_cells(ggeo, gmonths)[0]
                                  [first:first + 3]), "mut"),
                        "the month, on the axis under the field"))
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
    if mode == "focus":
        pinned = focus_tasks(board, show_archived)
        if pinned:
            out.append((c("▎", hue), "project spine (colour = project)"))
            out.append((c("==text==", "soon"), "highlight: yellow / warning"))
            out.append((c("!!text!!", "over"), "highlight: red / attention"))
            out.append((c("++text++", "green"), "highlight: green / resolved"))
            if any(t.images for t in pinned):
                out.append((c("▤", "mut"), "task has images"))
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
