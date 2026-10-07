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
import math
import os
import re
import shutil
import subprocess
import textwrap
import unicodedata
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import NamedTuple

from rich.cells import cell_len, set_cell_size
from rich.console import Console
from rich.markup import escape
from rich.style import Style
from rich.table import Table
from rich.text import Text

from . import history
from .models import (Board, CASCADE_DEFAULT_MODE, CASCADE_MODES, Project, Task,
                     critical_chain, days_in_phase, link_conflicts, link_marks,
                     open_predecessors, parse_iso, unblocks_count)
from .team_sync import TeamState, sync_tone
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
    "reached": "#7a828c",  # a reached milestone: quiet but legible — 4.9:1 on #0d1117
                           # (operator verdict UXV-5: the ash was ~2.4:1, near illegible)
    "bright": "#e6edf7",
    "soon": "#fbbf24",
    "later": "#64748b",
    "done": "#3f9c6d",
    "weekend": "#1a1d22",  # a background only: weekends on the gantt field (HLR-209)
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
    return ("◐", "hd")


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
    suffix = " ↗" if (first_valid_url(task) and arrow) else ""
    return _title_piece(task, fit(task.title + suffix, width), selected)


def _literal(text: str) -> str:
    """Markup that prints `text` exactly — a cut piece of a title or a name.

    `escape` escapes only TAG-shaped brackets and assumes a tag follows, so a
    cut piece prints wrong in two ways (P3, TC-302's hostile titles): rich
    drops the backslash before ANY bracket (backslash-bracket-ellipsis prints
    bracket-ellipsis), and a trailing backslash prints twice when spaces
    follow. Rich's rule, measured on 15.0: before a tag-shaped `[` a run of k
    backslashes prints k // 2, before any other `[` it prints k - 1. So each
    `[` gets the run that prints the k it had, and a trailing run is doubled
    and closed by a tag."""
    out, i = [], 0
    for m in re.finditer(r"(\\*)\[", text):
        k = len(m.group(1))
        tag = re.match(r"\[[a-z#/@][^[]*?]", text[m.end() - 1:]) is not None
        out.append(text[i:m.start()] + "\\" * (2 * k + 1 if tag else k + 1) + "[")
        i = m.end()
    out.append(text[i:])
    body = "".join(out)
    tail = len(text) - len(text.rstrip("\\"))
    if tail:
        body = f"[none]{body}{chr(92) * tail}[/none]"
    return body


def _title_piece(task: Task, text: str, selected: bool) -> str:
    """A piece of `task`'s title already cut to its cells: escaped AFTER the cut
    (escaping first and cutting after can split an escape and open a tag), linked
    to the task's first valid URL, reverse when selected."""
    url = first_valid_url(task)          # OSC-8 target = the FIRST valid URL (F6)
    body = _literal(text)
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
    markup = "".join(c(" " + _literal(g), col) for g, col in kept)   # a tag is user text
    return markup, cost


# The kanban priority badge (owner verdict 2026-09-30, "el uso de insignias,
# reusando !!, == y ++ para 3 colores"): the notes highlight vocabulary, worn in
# reverse video by every OPEN kanban card. Same tokens and tones as
# `_highlight_markup`, so the board speaks one colour language.
PRIORITY_BADGE = {"high": ("!!", "over"), "normal": ("==", "soon"),
                  "low": ("++", "green")}


def _link_tokens(task: Task, board: Board,
                 marks: dict[str, tuple[int, int]] | None) -> list[tuple[str, str]]:
    """`▸M` then `◂N` (each only when ≥ 1) in the muted tone the `⛓` wore
    (D-506). Only a BOARD task carries them: a teammate's task — the same id
    or not — is not in the board, so it paints none (A-11, S-8)."""
    if board.task_by_id(task.id) is not task:
        return []
    waits, unblocks = (marks if marks is not None else link_marks(board)).get(task.id, (0, 0))
    out = []
    if unblocks:
        out.append((f"▸{unblocks}", "mut"))
    if waits:
        out.append((f"◂{waits}", "mut"))
    return out


# The lanes' title floor (operator D-529): 5 characters and `…`. The kanban
# readability measure counts a title only once its first word shows
# (`kg_board._visible_chars`), and the kg board's median first word is 5.
CARD_TITLE_FLOOR = 6


def card_cell(task: Task, board: Board, wc: int, selected: bool, *,
              prefix: str = "", prefix_color: str = "mut",
              allow_priority: bool = True, today: date | None = None,
              marks: dict[str, tuple[int, int]] | None = None,
              readonly: bool = False, badge: bool = False,
              title_floor: int = 0) -> str:
    """A width-exact card: `prefix` + [badge] + truncated title + right
    indicators (↗ ! ▤ ·Nd ▸N ◂N +Nd ▣).

    `badge=True` (the kanban) puts the PRIORITY_BADGE of an open card between
    the prefix and the title and drops the `!` token, which the badge replaces;
    a done or archived card wears neither. The badge costs 3 cells and is shed
    when the cell cannot hold it.

    Title is truncated with … so it can NEVER share a cell with the trailing
    indicators, at any width down to 0. Always returns exactly `wc` cells.
    The `·Nd` aging token (HLR-006, LLR-006.1) is how long the task has sat
    in its current phase — `days_in_phase` off `phase_changed` — shown only
    while the task is NOT done and the stamp is KNOWN (None is unknown, never
    zero: an unstamped card renders no token rather than a lying `·0d`, and
    done work rests — its age is not work-in-progress information).

    `marks` is `link_marks(board)` — ``{task_id: (◂, ▸)}`` — computed once per
    render, so a pass pays for the links once, not per card (O(tasks²) trap).
    When it is omitted the helper derives it (unit tests).

    `title_floor` (the lanes pass CARD_TITLE_FLOOR): the title keeps that many
    cells (or its whole length) before any indicator is kept — the age is shed
    first, then `▸M`, then the rest from the left, and `◂N` last (D-533). 0
    (every other caller) keeps the shipped law: an indicator is kept the moment
    its cells fit."""
    if wc <= 0:
        return ""
    if wc < len(prefix):
        return c(fit(prefix, wc), prefix_color)
    tokens: list[tuple[str, str]] = []
    if has_url(task):
        tokens.append(("↗", "mut"))       # a link affordance, not focus (round-7 budget)
    if readonly:
        # Foreign team cards are merged read-only; the mark sits in the quiet
        # mut house so it never competes with urgency or project colour.
        tokens.append(("◦", "mut"))
    # THE GLYPH HOUSE. High priority used to be a ◉ in `amber` — the exact hex
    # (#fbbf24) the app uses for "due today". Two meanings, one colour, so the
    # mark could not be read; priority moved to the SHAPE `!` in the neutral ink
    # tone, which claims neither the identity nor the judging house. That is
    # still the mark wherever `badge` is off (the Focus rail, People).
    #
    # 2026-09-30, the owner's choice after the kanban priority round: on kanban
    # cards priority is the reverse-video PRIORITY_BADGE, REUSING the notes
    # highlight colours on purpose — one vocabulary for "this matters" across
    # notes and cards. Known conflicts, ALL accepted by the owner on 2026-09-30:
    # `==` wears `soon`, the due-today amber family; `!!` wears `over`, the hue
    # of the overdue `-Nd` chip (and of the blocked `▲` beside it); `++` wears
    # `green`, which is also an offered PROJECT hue, so on a green project the
    # stripe and the low badge share a colour. The tokens differ, so no meaning
    # rests on colour alone.
    badge_markup, badge_w = "", 0
    if (badge and not board.is_done(task) and not task.archived
            and wc - len(prefix) >= 3):
        token, tone = PRIORITY_BADGE.get(task.priority, PRIORITY_BADGE["normal"])
        badge_markup, badge_w = f"[b reverse {HEX[tone]}]{token}[/] ", 3
    if (allow_priority and not badge and task.priority == "high"
            and not board.is_done(task)):
        tokens.append(("!", "ink"))
    if task.images:
        # `mut`, not `sky`: an attachment is an ATTRIBUTE of one task, and `sky`
        # is an offered PROJECT hue. An identity tone worn by a task attribute
        # says "this task belongs to the sky project" to anyone reading the
        # board by colour. Its siblings already sit in neutral houses (↗ accent,
        # ! ink); this is the quietest of the three and takes the quietest tone.
        tokens.append(("▤", "mut"))     # width-1 image indicator, distinct from ↗/!
    age_token = None
    if not board.is_done(task):
        age = days_in_phase(task, today or date.today())
        if age is not None:
            # Age is a FACT about sitting still, not a judgement on it — the
            # quiet dim house (the same house date distances wear), never a
            # severity hue and never a project colour.
            age_token = (f"·{age}d", "dim")
            tokens.append(age_token)
    # the links (batch 2026-10-04-batch-01, HLR-501): ▸N = N open tasks wait on
    # this one, ◂N = it waits on N open tasks. Before the due token, so under
    # width pressure ▸ goes first, then ◂, and the deadline is kept longest.
    link_tokens = _link_tokens(task, board, marks)
    tokens.extend(link_tokens)
    if not task.archived:
        # The deadline countdown (operator, 2026-08-24): days until the due
        # date rides EVERY dated card, the last phase included — a done card
        # keeps the FACT in the quiet dim house, never a judging hue
        # (reldue_token's include_done seat). Listed after the link marks, so
        # they are shed before it. Put-away work shows nothing: an archived
        # task has no live deadline.
        dtok, dcol = reldue_token(task, today or date.today(), board,
                                  include_done=True)
        if dtok:
            tokens.append((dtok, dcol))
    if task.archived:
        # LAST in the list so it is the last thing shed under width pressure —
        # it is the only token here that says the row is not live work.
        tokens.append((ARCHIVED_MARK, "ash"))
    room = wc - len(prefix) - badge_w
    budget = room - max(0, min(title_floor, room, cell_len(task.title)))
    if title_floor:
        # operator D-533 "Dejar ◂ solo, quitar la edad antes" (A-12): under the
        # floor the age goes first, then `▸`, then the other meta from the left;
        # `◂` (waits on N open) is the last to go
        waits = [tk for tk in link_tokens if tk[0].startswith("◂")]
        order = ([age_token] if age_token in tokens else []) + \
            [tk for tk in link_tokens if tk not in waits] + \
            [tk for tk in tokens if tk != age_token and tk not in link_tokens] + waits
        for tk in order:
            if sum(1 + cell_len(g) for g, _ in tokens) <= budget:
                break
            tokens.remove(tk)
    ind_markup, used = _fit_indicators(tokens, budget)
    title_w = max(0, wc - len(prefix) - badge_w - used)
    pre = c(prefix, prefix_color) if prefix else ""
    return (pre + badge_markup + title_markup(task, title_w, selected, arrow=False)
            + ind_markup)


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


def reldue_token(task: Task, today: date, board: Board, *,
                 include_done: bool = False) -> tuple[str, str]:
    """A short relative-due token + color-key: '-2d' / 'today' / '+5d', or ''
    when the task has no due date (or is done). Colored by the same urgency.

    `include_done` (kanban cards, operator 2026-08-24): a DONE task keeps the
    FACT of its deadline but not the JUDGEMENT — the same text in the quiet
    dim house, never over/soon/mut, because nothing is expected of
    finished work. The default keeps the old law: done returns ''."""
    u = urgency(task, today, board)
    d = parse_iso(task.due_date)
    if d is None or u == "none" or (u == "done" and not include_done):
        return "", "dim"
    delta = (d - today).days
    resting = u == "done"
    if delta < 0:
        return f"{delta}d", ("dim" if resting else "over")
    if delta == 0:
        return "today", ("dim" if resting else "soon")
    if delta <= 7:
        return f"+{delta}d", ("dim" if resting else "soon")  # soon: amber, not focus
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
    r"""The visible text of a markup row — rich's own parse, never a regex.

    A regex cannot tell a style tag from a bracket the user printed: `_literal`
    (the hostile-text exact-print escape) emits runs rich prints as literal
    `[bold]`, and the old `\[/?[^\]]*\]` deletion ate those as if they were
    tags — undercounting the row, so `_pad` over-padded and the frame grew
    past its width while `_present_finish`'s assert agreed with the wrong
    number (found by TC-1003, batch 2026-10-07-batch-04). `emoji=False` is
    load-bearing like at `to_text`: with it on, rich rewrites a `:bug:`
    shortcode to a 2-cell glyph inside the measure while the painters priced
    it as 5 literal cells (the test_cells width law)."""
    try:
        return Text.from_markup(markup, emoji=False).plain
    except Exception:
        return markup


def header(title: str, right: str, w: int, tone: str = "bright") -> str:
    """THE HEAD ROW. No box: this design commits with RULES, not boxes — the
    prototype's closure law, which the frame was the last thing failing.

    The row carries facts (what the view is, what it counts) across its whole
    width; `head_rule` under it is the only box-drawing left, and it is one row
    rather than a border on all four sides."""
    tvis, rvis = vis(_strip(title)), vis(_strip(right))
    if tvis + rvis + 3 > w:               # too tight -> the right content goes
        right, rvis = "", 0
    if tvis + 2 > w:                      # still tight -> truncate the title
        # in the title's own tone: every title is bold `bright` (the colour
        # budget, batches 2026-10-02-batch-01 and -02)
        return c(fit(_strip(title), w), tone, bold=True)
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
    owns no edges. `_matrix_junctions` (and the kanban's own separators) return content
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
    start_in: int | None
    worst: int

    @property
    def resting(self) -> bool:
        return not self.open

    @property
    def closed(self) -> bool:
        return self.status in ("completed", "cancelled")


def lane_facts(board: Board, today: date, name: str, hue: str, status: str,
               due_date: str | None, rows: list[Task], *,
               start_date: str | None = None) -> LaneFacts:
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
    ps = parse_iso(start_date)
    start_in = (ps - today).days if ps else None
    worst = max(((today - parse_iso(t.due_date)).days for t in late), default=0)
    if due_in is not None and due_in < 0 and open_:
        worst = max(worst, -due_in)
    return LaneFacts(
        name=name, hue=hue, status=status,
        tasks=rows, open=open_, late=late, done_n=len(rows) - len(open_),
        total=len(rows),
        today_n=sum(1 for t in open_ if parse_iso(t.due_date) == today),
        high=sum(1 for t in open_ if t.priority == "high"),
        due_in=due_in, start_in=start_in, worst=worst)


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
                      [t for t in tasks if t.project_id == p.id],
                      start_date=p.start_date)
           for p in board.visible_projects(show_archived)]
    inbox = [t for t in tasks if board.project_by_id(t.project_id) is None]
    if inbox:
        out.append(lane_facts(board, today, "Inbox", "dim", "on_track", None,
                              inbox, start_date=None))
    return sorted(out, key=lambda ln: (ln.resting, ln.closed, lane_pressure(ln)))


# ---------------------------------------------------------------------------
# Lanes grid presentation (variant G2) — ported from prototypes/lanes_gauge
# ---------------------------------------------------------------------------
GRID_MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")


def _shade_hex(hex6: str, k: float) -> str:
    """A brightness tier of a hex — the honest 'shader': flat per facet."""
    r = min(255, int(int(hex6[1:3], 16) * k))
    g = min(255, int(int(hex6[3:5], 16) * k))
    b = min(255, int(int(hex6[5:7], 16) * k))
    return f"#{r:02x}{g:02x}{b:02x}"


def _noise(x: int, y: int) -> float:
    """Deterministic per-dot hash in [0,1) — the sand grain."""
    n = (x * 374761393 + y * 668265263) & 0xFFFFFFFF
    n = (n ^ (n >> 13)) * 1274126177 & 0xFFFFFFFF
    return ((n ^ (n >> 16)) & 0xFFFF) / 65536


def _grid_chip(t: Task, today: date) -> tuple[str, str]:
    d = parse_iso(t.due_date)
    if d is None:
        return "—", "dim"
    txt = f"{GRID_MONTHS[d.month - 1]} {d.day}"
    delta = (d - today).days
    if delta < 0:
        return txt, "over"
    if delta == 0:
        return txt, "accent"
    if delta <= 7:
        return txt, "soon"
    return txt, "mut"


def _grid_list_order(lane: LaneFacts) -> list[Task]:
    dated = [t for t in lane.open if parse_iso(t.due_date)]
    undated = [t for t in lane.open if not parse_iso(t.due_date)]
    return sorted(dated, key=lambda t: parse_iso(t.due_date)) + undated


def _grid_c_hub(lane: LaneFacts, today: date) -> tuple[str, int | None]:
    """(hub markup, next-due offset or None) — shared by the whole family."""
    dues = [(parse_iso(t.due_date) - today).days
            for t in lane.open if parse_iso(t.due_date)]
    if not dues:
        return c(f"{len(lane.open)} open · no dates", "dim"), None
    days = min(dues)
    nxt = min((t for t in lane.open if parse_iso(t.due_date)),
              key=lambda t: parse_iso(t.due_date))
    d = parse_iso(nxt.due_date)
    chip = f"{GRID_MONTHS[d.month - 1]} {d.day}"
    hub = (c(chip, "over") + c(f" ▲{-days}d", "over") if days < 0
           else c(chip, "accent" if days == 0 else "mut"))
    return hub + c(f" ·{len(lane.open)}", "dim"), days


def _grid_sediment_rows(lane: LaneFacts, today: date, col_w: int,
                        sweep: float = 1.0):
    """E3 · the sediment bar: the countdown window as a 2-row textured band."""
    span = (-7, 21)
    frac_of = lambda d: (d - span[0]) / (span[1] - span[0])   # noqa: E731
    hub, days = _grid_c_hub(lane, today)
    target = (frac_of(max(span[0], min(span[1], days))) * sweep
              if days is not None else None)
    today_i = round(frac_of(0) * (col_w - 1))
    bar, studs = [], [" "] * col_w
    off_l = off_r = 0
    for i in range(col_w):
        f = i / (col_w - 1)
        d = span[0] + (span[1] - span[0]) * f
        zone = HEX["over"] if d < 0 else HEX["soon"] if d < 7 else HEX["dim"]
        if i == today_i:
            bar.append(c("╎", "accent"))
        elif target is not None and f <= target:
            n = _noise(i, 11)
            g = "▓" if n < 0.34 else "▒" if n < 0.67 else "░"
            bar.append(f"[{_shade_hex(zone, 0.9 + 0.35 * _noise(i, 5))}]{g}[/]")
        else:
            bar.append(c("·", "dim"))
    for t in lane.open:
        d = parse_iso(t.due_date)
        if d is None:
            continue
        f = frac_of((d - today).days)
        if not (0 <= f <= 1):
            off_l += 1 if f < 0 else 0
            off_r += 1 if f > 1 else 0
            continue
        tone = ("over" if d < today else "accent" if d == today
                else lane.hue)
        studs[round(f * (col_w - 1))] = c("▄", tone)
    labels = (c(f"{span[0]}d", "dim"), c(f"+{span[1]}d", "dim"))
    return ["".join(bar), "".join(studs)], (off_l, off_r), hub, labels


def _grid_task_row(t: Task, board: Board, lane: LaneFacts, wc: int,
                   selected: bool, today: date) -> str:
    """The roomier row: prefix, title, then indicators AND the absolute date."""
    prefix = "▲ " if t.blocked else "▊ "
    pcol = "over" if t.blocked else lane.hue
    right: list[tuple[str, str]] = []
    if t.priority == "high" and not board.is_done(t):
        right.append(("!", "ink"))
    if t.images:
        right.append(("▤", "mut"))
    if t.urls:
        right.append(("↗", "mut"))
    right.append(_grid_chip(t, today))
    rw = sum(vis(x) for x, _ in right) + len(right)
    title_w = max(0, wc - len(prefix) - rw - 1)
    shown = clip(t.title, title_w)
    body = escape(shown)
    if selected:
        body = f"[reverse]{body}[/reverse]"
    pad = " " * max(0, wc - len(prefix) - vis(shown) - rw - 1)
    return (c(prefix, pcol) + c(body, "mut") + pad + " "
            + " ".join(c(x, k) for x, k in right))


def _grid_col_header(lane: LaneFacts, wc: int) -> str:
    return (c("▐ ", lane.hue)
            + c(escape(fit(clip(lane.name, wc - 2), wc - 2)),
                lane.hue, bold=True))


def _grid_center(markup: str, wc: int) -> str:
    pad = max(0, wc - vis(_strip(markup)))
    return " " * (pad // 2) + markup + " " * (pad - pad // 2)


def _grid_panel_rows(lane: LaneFacts, board: Board, today: date, wc: int,
                     n_rows: int, selected_id: str | None,
                     sweep: float = 1.0) -> list[Row]:
    """One panel's content rows (WITHOUT the mercury prefix)."""
    bar_rows, (off_l, off_r), hub, labels = _grid_sediment_rows(
        lane, today, wc, sweep)
    head = (_grid_col_header(lane, wc - 5)
            + c(fit(f"{len(lane.open)}", 4, "right"), lane.hue))
    rows: list[Row] = [(head, None)]
    rows += [(r, None) for r in bar_rows]
    rows.append((_grid_center(hub, wc), None))
    if labels:
        lft, rgt = labels
        if off_l:
            lft = c("◂ ", "mut") + lft
        if off_r:
            rgt = rgt + c(" ▸", "mut")
        rows.append((lft + " " * max(1, wc - vis(_strip(lft))
                                       - vis(_strip(rgt))) + rgt, None))
    tasks = _grid_list_order(lane)
    room = n_rows - len(rows) - 1                    # footer is pinned
    shown_t = tasks if len(tasks) <= room else tasks[:max(0, room - 1)]
    for t in shown_t:
        rows.append((_grid_task_row(t, board, lane, wc, t.id == selected_id,
                                    today), t.id))
    if len(tasks) > len(shown_t):
        rows.append((c(fit(f"+{len(tasks) - len(shown_t)} more", wc), "dim"),
                     None))
    rows = rows[:n_rows - 1]
    rows += [("", None)] * (n_rows - 1 - len(rows))
    rows.append((c(f"{lane.done_n}/{lane.total} done", "dim"), None))
    return rows


def _grid_mercury_cell(lane: LaneFacts, today: date, r: int, n_rows: int,
                       sweep: float = 1.0) -> str:
    """The panel spine, 2 cells per panel row: start bottom, due top."""
    start = (today + timedelta(days=lane.start_in)) if lane.start_in is not None else None
    due = (today + timedelta(days=lane.due_in)) if lane.due_in is not None else None
    if r == 0:
        return "  "
    if not (start and due and due > start):
        return " " + c("│", "dim")
    span = (due - start).days
    top, bot = 1, n_rows - 1
    f = 1 - (r - top) / max(1, bot - top)
    f_today = 1 - ((today - start).days / span) * sweep
    rail, rail_tone = "│", "dim"
    for t in lane.open:
        d = parse_iso(t.due_date)
        if d is None:
            continue
        ft = 1 - (d - start).days / span
        if abs(ft - f) * max(1, bot - top) < 1.0:
            rail, rail_tone = "▪", ("over" if d < today else
                                    "accent" if d == today else lane.hue)
    if f_today < 0:
        if r == top:
            return f"[{HEX['over']}]▲[/]" + c(rail, rail_tone)
        return (f"[{_shade_hex(HEX['over'], 0.85 + 0.2 * _noise(r, 7))}]█[/]"
                + c(rail, rail_tone))
    if f >= f_today - 1e-9:
        return (f"[{_shade_hex(HEX.get(lane.hue, HEX['mut']), 0.85 + 0.2 * _noise(r, 7))}]█[/]"
                + c(rail, rail_tone))
    if abs(f - f_today) * max(1, bot - top) < 1.0:
        return " " + c("╎", "accent")
    return " " + c(rail, rail_tone)


def _grid_render(board: Board, show_archived: bool,
                 selected_id: str | None, today: date,
                 width: int, height: int, sweep: float = 1.0,
                 line_map: dict[str, int] | None = None) -> Text:
    """The grid: 2×3 panels with mercury spine + sediment bar + task rows."""
    today = today or date.today()
    w = _clamp_width(width)
    inner = w
    h = height or 24
    lanes = list(lanes_of(board, show_archived, today))

    n_cols = max(1, min(2, inner // 19))
    col_w = (inner - (n_cols - 1)) // n_cols
    layers_n = max(1, -(-len(lanes) // n_cols))
    cap = n_cols * layers_n
    shown, hidden = lanes[:cap], lanes[cap:]

    tasks = board.visible_tasks(show_archived)
    live = [t for t in tasks if not t.archived]
    open_n = sum(1 for t in live if not board.is_done(t))
    due_n = sum(1 for t in live
                if (d := parse_iso(t.due_date)) is not None
                and (d - today).days <= 0 and not board.is_done(t))
    right = c(f"{open_n} open · ", "mut") + c(f"{due_n} due", "over", bold=True)
    if hidden:
        right = c(f"+{len(hidden)} lanes ", "dim") + right
    lines = [header(c("◆ TASKBOARD", "bright", bold=True)
                    + c(f" · grid {n_cols}×{layers_n}", "mut"), right, w)]

    body = h - 1
    panel_h = (body - (layers_n - 1)) // layers_n
    sep = c("│", "frame")
    pw = col_w - 3

    for li in range(layers_n):
        chunk = shown[li * n_cols:(li + 1) * n_cols]
        panels: list[tuple[LaneFacts, list[Row]]] = []
        for lane in chunk:
            rows = _grid_panel_rows(lane, board, today, pw, panel_h,
                                    selected_id, sweep)
            panels.append((lane, rows))
        for r_ in range(panel_h):
            parts = []
            for lane, rows in panels:
                prefix = _grid_mercury_cell(lane, today, r_, panel_h, sweep)
                markup, tid = rows[r_] if r_ < len(rows) else ("", None)
                parts.append(prefix + " " + _pad(markup, pw))
            for _ in range(n_cols - len(panels)):
                parts.append(" " * (col_w - 1))
            lines.append(line(_pad(sep.join(parts), inner)))
            if line_map is not None:
                for lane, rows in panels:
                    _, tid = rows[r_] if r_ < len(rows) else ("", None)
                    if tid is not None:
                        line_map[tid] = len(lines) - 1
        if li < layers_n - 1:
            lines.append(line(c("─" * inner, "frame")))
    lines.append(bottom(None, w))
    return to_text(lines, h, w, pinned=0)


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
                     width=68, height=0, line_map=None, tick=0,
                     presentation="waves") -> Text:
    """Lanes: projects RANKED by pressure on one shared axis of days. The one
    that needs you now gets a drawn field; the rest get a row each; the ones
    with nothing open rest at the bottom. Nothing is ever dropped in silence —
    what does not fit is counted.

    Presentations:
      * "waves" — the classic stacked lanes (default).
      * "grid"  — 2×3 panel grid with mercury spine + sediment bar.
    """
    today = today or date.today()
    if presentation == "grid":
        return _grid_render(board, show_archived, selected_id, today,
                            width, height, line_map=line_map)
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
    lines = [header(c("◆ TASKBOARD", "bright", bold=True), right, w)]

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
    lines = [header(c("AGENDA", "bright", bold=True), right, w)]

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
# view: GANTT  (the whole board on a fitted window; a date ruler on top)
# ---------------------------------------------------------------------------

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
# `FIELD_PROGRESS` no longer draws a second row under each project: progress is
# now ONE CELL, `PROGRESS_DOT`, riding on the span itself. The constant stays as
# the name of the weight the hierarchy test keeps distinct (2026-10-02: the
# half-cell `FIELD_HALF` went with the 2-day axis that needed it).
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


def _flowing(board: Board, task: Task) -> bool:
    """A task is "in progress" — worth animating a flow packet on — when it
    has left the first phase, is not done, is not blocked and waits on no open
    task (D-519: before the links had a meaning of their own, a waiting task
    was always blocked, so its stillness is unchanged)."""
    # and NOT archived: a bar that animates is claiming to be work in motion,
    # which is the one thing put-away work is not
    return (not board.is_done(task) and not task.blocked and not task.archived
            and board.phase_index(task) > 0 and not open_predecessors(board, task))


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


def _priority_hue(priority: str) -> str:
    """Hue for a task bar in the gantt: priority is the primary semantic channel."""
    return {"high": "rose", "normal": "sky", "low": "mut"}.get(priority, "sky")


GANTT_SCALES = (0.5, 1, 2, 3, 7)        # days per cell; the smallest that fits wins
GANTT_MARGIN = 2                         # days of air either side of the open work
GANTT_RULER_ROWS = 2                     # month row + day row, pinned under the header
CRITICAL_REACH = "━"                     # the critical chain: structure, not hue
# Weekends, shaded at a day per cell or finer (answer D5; the round-5 frames).
# The prototype's #161d27 quantises to the field's own 256-colour index (16), so
# it vanished on a 256-colour terminal; #1a1d22 keeps its luminance and lands on
# index 234 (measured, batch 2026-10-02-batch-02 P-4 / D-205).
WEEKEND_BG = HEX["weekend"]
ECHO_OPEN, ECHO_FILL, ECHO_CLOSE = "⟦", "━", "⟧"


class GanttAxis:
    """A day axis of `k` days per cell from `start`, `w` cells wide.

    The shipped axis was two days per cell with today pinned at 30 % of the
    field, whatever the board held. A fitted window needs a variable `k`, so
    the cell arithmetic lives here instead of in `day_col`."""

    def __init__(self, start: date, k: float, w: int, today: date):
        self.start, self.k, self.w, self.today = start, k, w, today
        self.tc = self.cell(today)

    def cell(self, d: date) -> int:
        return math.floor((d - self.start).days / self.k)

    def end_cell(self, d: date) -> int:
        """The LAST cell a day occupies — a day is two cells at k = 0.5."""
        return self.cell(d) + max(0, int(round(1 / self.k)) - 1)

    def day(self, x: int) -> date:
        return self.start + timedelta(days=math.floor(x * self.k))

    def days_in(self, x: int) -> list[date]:
        a = self.day(x)
        return [a + timedelta(days=i) for i in range(max(1, (self.day(x + 1) - a).days))]

    def window_days(self) -> list[date]:
        """Every day whose cell is inside the field, in order."""
        out, d = [], self.start
        while self.cell(d) < self.w:
            if self.cell(d) >= 0:
                out.append(d)
            d += timedelta(days=1)
        return out

    def weekends(self) -> frozenset[int]:
        """The field cells whose days are all Saturday or Sunday, while a cell
        is at most a day (k <= 1); none at coarser scales, where a cell mixes
        weekdays and weekend."""
        if self.k > 1:
            return frozenset()
        return frozenset(x for x in range(self.w)
                         if all(d.weekday() >= 5 for d in self.days_in(x)))

    def guides(self) -> frozenset[int]:
        """The calendar ruled through the ground: Mondays while a week is at
        least a few cells wide (k <= 2), the 1st of each month above that.
        Never on the today column, which the today rule owns."""
        out = set()
        for x in range(self.w):
            if x == self.tc:
                continue
            ds = self.days_in(x)
            if self.k <= 2:
                if any(d.weekday() == 0 and self.cell(d) == x for d in ds):
                    out.add(x)
            elif any(d.day == 1 for d in ds):
                out.add(x)
        return frozenset(out)


def gantt_axis(field_w: int, today: date, lo: date, hi: date, ctx: date) -> GanttAxis:
    """THE FITTED WINDOW: the smallest days-per-cell that holds [lo, hi]; the
    cells left over buy PAST context back to `ctx` (where the open work began),
    never more than that, and the rest is left on the right. A week-per-cell
    window starts on a Monday so its guides fall on whole weeks."""
    w = max(1, field_w)
    need = (hi - lo).days + 1
    k = next((s for s in GANTT_SCALES if need <= w * s), GANTT_SCALES[-1])
    spare = int(w * k) - need
    start = lo - timedelta(days=max(0, min(spare, (lo - ctx).days)))
    if k == 7:
        start -= timedelta(days=start.weekday())
        if math.floor((hi - start).days / k) >= w:     # the Monday shift spent
            start = lo - timedelta(days=lo.weekday())  # the context: give it back
        if math.floor((hi - start).days / k) >= w:     # and if even lo's Monday
            start = lo                                 # cannot hold hi, keep lo
    return GanttAxis(start, k, w, today)


def gantt_columns(width: int) -> tuple[int, int, int]:
    """(label_w, chip_w, field_w): label + gutter(1) + field + space + chip == width."""
    if width >= 100:
        label_w, chip_w = 30, 7
    elif width >= 60:
        label_w, chip_w = 20, 6
    else:
        label_w, chip_w = max(6, width // 3), (6 if width >= 40 else 0)
    field_w = width - label_w - 1 - (chip_w + 1 if chip_w else 0)
    return label_w, chip_w, max(1, field_w)


class GanttGroup(NamedTuple):
    project: object | None          # None = the Inbox
    open: list[Task]
    rest: list[Task]
    late: int
    unfolded: bool
    # what the group DRAWS (LLR-602.1): its open work and, while it has any, its
    # reached milestones, merged by due. `open` and `rest` keep their counts.
    rows: tuple = ()


# The Inbox's key as a gantt group, beside the project ids (None means "no
# previous group"): the two must never collide (batch 2026-10-02-batch-02, qa N-1).
INBOX_GROUP = ""


def group_key(project) -> str:
    """A gantt group's key: its project's id, or the Inbox's."""
    return project.id if project is not None else INBOX_GROUP


def gantt_group_key(board: Board, t: Task) -> str:
    """The gantt group a task is drawn in: its project's id, or the Inbox."""
    return group_key(board.project_by_id(t.project_id))


def _gantt_open(board: Board, t: Task) -> bool:
    return not board.is_done(t) and not t.archived


def gantt_plan(board: Board, show_archived: bool, selected_id: str | None,
               today: date, body_rows: int,
               focus: str | None = None, previous: str | None = None,
               pinned: str | None = None) -> list[GanttGroup]:
    """THE ONE SEAT for what the gantt draws and in what order — the renderer
    and `nav_model` both read it, so the cursor cannot walk an order the screen
    does not show (F-3).

    Every group gets its span row. The selected task's group unfolds first;
    the others unfold most-URGENT first — open tasks due today or earlier, then
    the most due today, then the earliest open due (batch 2026-10-02-batch-02,
    HLR-208: due today counts) — while ALL of a group's open rows still fit.
    `previous` is the group the selection was in before its current one: it is
    offered rows right after the selected group, so walking into the next
    project does not fold the one just left (answer UXV-2, HLR-207).
    Rest work (done or archived) never draws a row: it is the `✓n` on its span
    row (G-A: "done folds to ✓n")."""
    tasks = board.visible_tasks(show_archived)
    raw: list[tuple[object | None, list[Task], list[Task]]] = []
    for p in board.visible_projects(show_archived):
        if focus and p.id != focus:
            continue
        own = gantt_tasks(board, tasks, p.id)
        raw.append((p, [t for t in own if _gantt_open(board, t)],
                    [t for t in own if not _gantt_open(board, t)]))
    loose = [t for t in tasks if board.project_by_id(t.project_id) is None]
    if loose and not focus:
        raw.append((None, sort_by_due([t for t in loose if _gantt_open(board, t)]),
                    [t for t in loose if not _gantt_open(board, t)]))

    def late_n(ts):
        return sum(1 for t in ts if (d := parse_iso(t.due_date)) and d < today)

    # a reached milestone is a row among its group's open rows, by date, while the
    # group has open work (D-606, M-1: "◆✓ reached")
    rows = [tuple(sort_by_due(o + [t for t in r if t.milestone and board.is_done(t)
                                   and not t.archived])) if o else ()
            for _p, o, r in raw]

    sel = board.task_by_id(selected_id) if selected_id else None
    sel_i = next((i for i, (p, o, r) in enumerate(raw)
                  if sel is not None and sel in o + r), None)
    left = body_rows - len(raw)
    unfold = [False] * len(raw)
    if sel_i is not None:
        unfold[sel_i] = True
        left -= len(rows[sel_i])
    # `pinned` (the gantt link mode's waiter, D-528) unfolds like the selection:
    # the link is drawn between two rows, so neither may fold. None elsewhere.
    pin_i = next((i for i, (p, o, r) in enumerate(raw)
                  if pinned is not None and group_key(p) == pinned), None)
    if pin_i is not None and pin_i != sel_i:
        unfold[pin_i] = True
        left -= len(rows[pin_i])

    def pressure(i):
        ts = raw[i][1]
        dues = [d for t in ts if (d := parse_iso(t.due_date))]
        urgent = sum(1 for d in dues if d <= today)
        due_today = sum(1 for d in dues if d == today)
        return (previous is None or group_key(raw[i][0]) != previous,
                -urgent, -due_today, min(dues or [date.max]))

    for i in sorted((i for i in range(len(raw)) if i not in (sel_i, pin_i)), key=pressure):
        n = len(rows[i])
        if n and n <= left:
            unfold[i] = True
            left -= n
    return [GanttGroup(p, o, r, late_n(o), unfold[i], rows[i])
            for i, (p, o, r) in enumerate(raw)]


def gantt_window(groups: list[GanttGroup], today: date
                 ) -> tuple[date, date, date]:
    """(lo, hi, ctx): the open work's dues and its projects' committed dues,
    today always inside, two days of air either side; ctx is where the open
    work STARTED, which the spare cells may spend as past context."""
    open_t = [t for g in groups for t in g.open]
    dues = [d for t in open_t if (d := parse_iso(t.due_date))]
    starts = [d for t in open_t if (d := parse_iso(t.start_date))]
    pdues = [d for g in groups if g.project is not None and g.open
             and (d := parse_iso(g.project.due_date))]
    margin = timedelta(days=GANTT_MARGIN)
    lo = min(dues + [today]) - margin
    hi = max(dues + pdues + [today]) + margin
    return lo, hi, min(starts + [lo])


def gantt_due_chip(due_iso: str | None, today: date, width: int) -> str:
    """One right-aligned due chip, exactly `width` cells: `▲3d` past due,
    `today`, `Oct 6`, or `no due`. Only open work is ever chipped."""
    if width <= 0:
        return ""
    d = parse_iso(due_iso)
    if d is None:
        lab, tone = "no due", "dim"
    elif d < today:
        lab, tone = f"▲{(today - d).days}d", "over"
    elif d == today:
        lab, tone = "today", "soon"
    else:
        lab, tone = f"{d:%b} {d.day}", "mut"
    return c(fit(lab, width, "right"), tone)


def gantt_dep_mark(task: Task, board: Board, chain: set[str]) -> str:
    """The dependency mark, in its own one-cell gutter so it never covers a
    label or a bar: a task that waits on an OPEN predecessor (archived ones are
    closed — LLR-501.3). `over` when a predecessor's due overlaps its plan by a
    day or more (the one measure, D-503: a start ON the due day conflicts); bold
    bright on the critical chain (structure, not hue); muted otherwise; blank
    when nothing open is waited on."""
    if not open_predecessors(board, task):
        return " "
    if link_conflicts(board, task):
        return c("↳", "over")
    if task.id in chain:
        return c("↳", "bright", bold=True)
    return c("↳", "mut")


def milestone_tone(task: Task, board: Board, today: date) -> str:
    """A milestone's tone (LLR-602.2): the reached grey once reached, over late,
    else its project's hue (dim in the Inbox) — identity, not urgency, until it is
    late."""
    if board.is_done(task):
        return "reached"
    d = parse_iso(task.due_date)
    if d is not None and d < today:
        return "over"
    return project_color(board, task)


def gantt_milestone_cells(task: Task, board: Board, ax: GanttAxis, today: date,
                          tone: str) -> list[tuple[str, str]]:
    """A milestone's field (M-1): `◆` on its date (`◆✓` reached) and the date
    beside it — after it, or before it when it does not fit — never a bar. Off the
    window: the edge glyph and the `◆` beside it. No due: nothing."""
    cells = [(" ", "dim")] * ax.w
    d = parse_iso(task.due_date)
    if d is None or ax.w < 3:
        return cells
    marks = [("◆", tone)] + ([("✓", "reached")] if board.is_done(task) else [])
    x = ax.cell(d)
    if x < 0:
        cells[0] = (OFF_LEFT, "mut")
        x = 1
    elif x >= ax.w:
        cells[-1] = (OFF_RIGHT, "mut")
        x = ax.w - 1 - len(marks)
    elif x + len(marks) > ax.w:
        marks = marks[:1]          # the last cell keeps its day; the chip says ✓ (G-2)
    x = max(0, min(x, ax.w - len(marks)))
    for i, m in enumerate(marks):
        cells[x + i] = m
    key = "reached" if board.is_done(task) else ("over" if tone == "over" else "mut")
    lab = _md(d)
    after, before = x + len(marks) + 1, x - 1 - len(lab)
    at = after if after + len(lab) <= ax.w else (before if before >= 0 else None)
    if at is not None:
        for i, ch in enumerate(lab):
            cells[at + i] = (ch, key) if ch != " " else (" ", "gap")
        cells[at - 1 if at == after else at + len(lab)] = (" ", "gap")   # `◆ Oct 10`
    return cells


def gantt_milestone_chip(task: Task, board: Board, today: date, width: int) -> str:
    """A milestone's chip (LLR-602.2): how far it is, not a date — `in Nd`,
    `today`, `▲Nd` late, `✓ done` reached, `no due`."""
    if width <= 0:
        return ""
    d = parse_iso(task.due_date)
    if board.is_done(task):
        lab, tone = "✓ done", "reached"
    elif d is None:
        lab, tone = "no due", "dim"
    elif d < today:
        lab, tone = f"▲{(today - d).days}d", "over"
    elif d == today:
        lab, tone = "today", "soon"
    else:
        lab, tone = f"in {(d - today).days}d", "mut"
    return c(fit(lab, width, "right"), tone)


def _gantt_span(project, ax: GanttAxis, progress: float, tick: int
                ) -> list[tuple[str, str]]:
    """The project span on the fitted axis: ash behind today, hue ahead, `◆`
    on the committed due, `●` where the work got to (breathing only while it
    is behind — the shipped ration, `_progress_glyph`)."""
    cells = [(" ", "dim")] * ax.w
    s, e = parse_iso(project.start_date), parse_iso(project.due_date)
    if s is None and e is None:
        return cells
    c0, c1 = ax.cell(s or ax.today), ax.cell(e or ax.today)
    if c1 < c0:
        c0, c1 = c1, c0
    a, b = max(0, c0), min(ax.w - 1, c1)
    for x in range(a, b + 1):
        cells[x] = (FIELD_REACH, "ash" if x < ax.tc else project.color)
    if e is not None and 0 <= c1 < ax.w:
        cells[c1] = ("◆", project.color)
    if c0 < 0:
        cells[0] = (OFF_LEFT, "mut")
    if c1 >= ax.w:
        cells[-1] = (OFF_RIGHT, "mut")
    if a <= ax.tc <= b and cells[ax.tc][0] == FIELD_REACH:
        cells[ax.tc] = (" ", "dim")            # the today rule crosses the span
    dot = c0 + int(round((c1 - c0) * max(0.0, min(1.0, progress))))
    if dot < 0:
        cells[0] = (OFF_LEFT, project.color)   # progress is out there, left
    elif a <= b:
        dot = min(max(dot, a), b)
        cells[dot] = (_progress_glyph(c0, c1, ax.tc, progress, tick), project.color)
    return cells


def _gantt_bar(task: Task, board: Board, ax: GanttAxis, chain: set[str],
               tick: int) -> list[tuple[str, str]]:
    """An open task's reach on the fitted axis, its phase tip at the due, in
    its priority hue — or as heavy bright structure on the critical chain. A
    one-date task is a `◆`. In-progress work carries the flow packet."""
    cells = [(" ", "dim")] * ax.w
    s, e = parse_iso(task.start_date), parse_iso(task.due_date)
    if s is None and e is None:
        return cells
    crit = task.id in chain
    tone = "crit" if crit else _priority_hue(task.priority)
    if s is not None and e is not None and s == e:
        x = ax.cell(e)
        if 0 <= x < ax.w:
            cells[x] = ("◆", tone)
        return cells
    a, b = ax.cell(s or ax.today), ax.end_cell(e or ax.today)
    if b < a:
        a, b = b, a
    for x in range(max(0, a), min(ax.w, b)):
        cells[x] = (CRITICAL_REACH if crit else FIELD_TASK, tone)
    if 0 <= b < ax.w:
        cells[b] = (FIELD_PHASE_TIP[min(3, board.phase_index(task))], tone)
    if a < 0:
        cells[0] = (OFF_LEFT, "mut")
    if b >= ax.w:
        cells[-1] = (OFF_RIGHT, "mut")
    lo, hi = max(0, a) + (1 if a < 0 else 0), min(ax.w - 1, b)   # clear of `◂`
    if hi > lo and _flowing(board, task):
        cells[lo + tick % (hi - lo)] = ("▬", "mut")
    return cells


def _on_weekend(cell: str) -> str:
    """One field cell's markup (`[style]g[/]`) with the weekend background in
    the SAME tag — `[style on #bg]g[/]` — so neighbouring cells of one style
    still collapse into a single run (the span-economy law); a second wrapping
    tag per cell would not."""
    close = cell.index("]")
    return f"{cell[:close]} on {WEEKEND_BG}{cell[close:]}"


def _gantt_field(cells: list[tuple[str, str]], ax: GanttAxis,
                 guides: frozenset[int], weekends: frozenset[int] = frozenset()) -> str:
    """Cells to markup over the field's own ground: lattice `·` (ash behind
    today, dim ahead), the calendar guide `┆`, and the today rule `╎` in any
    cell nothing else took; a weekend cell carries the weekend background
    under whatever it holds (every cell here is a constant glyph)."""
    out = []
    for x, (glyph, tone) in enumerate(cells):
        if tone == "gap":                      # a space inside a written date
            m = c(" ", "dim")
        elif glyph != " ":
            m = (c(glyph, "bright", bold=True) if tone == "crit" else c(glyph, tone))
        elif x == ax.tc:
            m = c(RULE, "accent")
        else:
            m = c(FIELD_WEEK if x in guides else LATTICE, "ash" if x < ax.tc else "dim")
        out.append(_on_weekend(m) if x in weekends else m)
    return "".join(out)


# --------------------------------------------------------------------------- #
# the ruler (AX-2): months and day numbers on top, answering for the selection
# --------------------------------------------------------------------------- #
GANTT_CADENCES = {
    "daily": lambda d: True,
    "Mondays": lambda d: d.weekday() == 0,
    "1st/15th": lambda d: d.day in (1, 15),
    "1st": lambda d: d.day == 1,
}


def gantt_cadence(ax: GanttAxis) -> tuple[str, list[tuple[date, int]]]:
    """THE CADENCE RULE: every day at >= 3 cells per day, Mondays at >= 1,
    the 1st and 15th while every gap between them stays >= 3 cells (two
    digits and a blank), else the 1st alone. Returns the name and the
    (day, cell) of every tick it schedules inside the window."""
    days = ax.window_days()
    cpd = 1 / ax.k
    if cpd >= 3:
        name = "daily"
    elif cpd >= 1:
        name = "Mondays"
    else:
        xs = [ax.cell(d) for d in days if d.day in (1, 15)]
        name = "1st/15th" if all(b - a >= 3 for a, b in zip(xs, xs[1:])) else "1st"
    pred = GANTT_CADENCES[name]
    return name, [(d, ax.cell(d)) for d in days if pred(d)]


def _md(d: date) -> str:
    return f"{d:%b} {d.day}"


def gantt_echo(task: Task, board: Board, ax: GanttAxis, today: date):
    """The selection on the ruler, EXACT dates only (never a cell's rounded
    date): (cells {x: glyph}, tone, label options in preference order, the
    full text for the label column). None when the task has no date."""
    s, e = parse_iso(task.start_date), parse_iso(task.due_date)
    if s is None and e is None:
        return None
    w = ax.w
    tone = "over" if (e and e < today and _gantt_open(board, task)) else "bright"
    if s is not None and e is not None and s == e:
        x = min(max(ax.cell(e), 0), w - 1)
        lab = _md(e)
        return ({x: "◆"}, tone, [[(x + 2, lab)], [(x - 1 - len(lab), lab)]],
                f"◆ {lab}")
    if s is not None and e is not None:
        a = min(max(ax.cell(s), 0), w - 1)
        b = min(max(ax.end_cell(e), 0), w - 1)
        if b <= a:
            b = min(w - 1, a + 1)
        cells = {x: ECHO_FILL for x in range(a + 1, b)}
        # a clipped end says so, as the bars do (UXV-7): the bracket would claim
        # the task starts (or ends) on the window's edge
        cells[a] = OFF_LEFT if ax.cell(s) < 0 else ECHO_OPEN
        cells[b] = OFF_RIGHT if ax.end_cell(e) >= w else ECHO_CLOSE
        L, R = _md(s), _md(e)
        both = f"{L}–{e.day}" if (s.year, s.month) == (e.year, e.month) else f"{L}–{R}"
        return (cells, tone,
                [[(a - 1 - len(L), L), (b + 2, R)],
                 [(a - 1 - len(both), both)],
                 [(b + 2, both)]],
                f"{L} → {R}")
    if e is not None:
        b = min(max(ax.end_cell(e), 0), w - 1)
        txt = f"no start · due {_md(e)}"
        close = OFF_RIGHT if ax.end_cell(e) >= w else ECHO_CLOSE
        return ({b: close}, tone, [[(b + 2, txt)], [(b - 1 - len(txt), txt)]], txt)
    a = min(max(ax.cell(s), 0), w - 1)
    txt = f"starts {_md(s)} · no due"
    opening = OFF_LEFT if ax.cell(s) < 0 else ECHO_OPEN
    return ({a: opening}, tone, [[(a + 2, txt)], [(a - 1 - len(txt), txt)]], txt)


def _ruler_cell(ch: str, key: str, bold: bool = False, reverse: bool = False) -> str:
    style = ("b " if bold else "") + ("reverse " if reverse else "") + HEX[key]
    return f"[{style}]{escape(ch)}[/]"


def gantt_day_row(ax: GanttAxis, today: date, echo) -> tuple[list[str], dict]:
    """The day row's field cells (markup, one per cell) and what was placed.

    Layers, in order: the echo, then each tick where it and one blank either
    side are free (a tick ends on its own cell at the right edge), then the
    today rule where today's column is still blank — or today's tick, lit."""
    w = ax.w
    glyph: list = [None] * w
    owner = [""] * w
    meta: dict = {"ticks": [], "echo": None, "echo_label": None}

    def free(lo: int, hi: int, gap: int) -> bool:
        return 0 <= lo and hi <= w and all(
            owner[i] == "" for i in range(max(0, lo - gap), min(w, hi + gap)))

    def write(pos: int, text: str, key: str, who: str, bold: bool = False) -> None:
        for i, ch in enumerate(text):
            glyph[pos + i] = (ch, key, bold)
            owner[pos + i] = who

    if echo is not None:
        cells, tone, options, full = echo
        for x, g in cells.items():
            glyph[x] = (g, tone, True)
            owner[x] = "echo"
        chosen = next((opt for opt in options
                       if all(free(p, p + len(t), 0) for p, t in opt)), None)
        if chosen is None:
            meta["echo_label"] = full
        else:
            for p, t in chosen:
                write(p, t, tone, "echo", True)
        meta["echo"] = [t for _, t in chosen] if chosen else [full]

    meta["cadence"], ticks = gantt_cadence(ax)
    for d, x in ticks:
        lab = str(d.day)
        p = x if x + len(lab) <= w else w - len(lab)
        if free(p, p + len(lab), 1):
            write(p, lab, "mut", "tick")
            meta["ticks"].append((d, x, p))
        else:
            meta["ticks"].append((d, x, None))

    tc = ax.tc
    if 0 <= tc < w:
        if glyph[tc] is None:
            glyph[tc] = (RULE, "accent", False)
        elif owner[tc] == "tick":
            for d, _x, p in meta["ticks"]:
                if p is not None and p <= tc < p + len(str(d.day)):
                    write(p, str(d.day), "accent", "tick", True)
    guides, weekends = ax.guides(), ax.weekends()
    out = []
    for x in range(w):
        if glyph[x] is None:
            near = any(owner[i] != "" for i in (x - 1, x + 1) if 0 <= i < w)
            m = c(FIELD_WEEK if x in guides and not near else " ", "frame")
        else:
            ch, key, bold = glyph[x]
            m = _ruler_cell(ch, key, bold)
        out.append(_on_weekend(m) if x in weekends else m)
    return out, meta


def gantt_month_row(ax: GanttAxis, today: date,
                    marks: dict[int, tuple[str, str]]) -> list[str]:
    """Month bands: `┃` on each month's first cell after the window's first,
    the project's `◆` marks next (never covered), today's number lit on or
    hugging the today column, then each band's name in its first free run —
    the full name with the year on the first band and on January, the full
    name, or the three-letter form, whichever fits first."""
    w = ax.w
    keys = [(ax.day(x).year, ax.day(x).month) for x in range(w)]
    starts = [0] + [x for x in range(1, w) if keys[x] != keys[x - 1]]
    bands = [(keys[s], s, (starts + [w])[i + 1]) for i, s in enumerate(starts)]
    glyph: list = [None] * w
    for _ym, x0, _x1 in bands:
        if x0 > 0:
            glyph[x0] = ("┃", "frame", False, False)
    for x, (g, key) in marks.items():
        if 0 <= x < w:
            glyph[x] = (g, key, True, False)
    tlab, tc = str(today.day), ax.tc
    for p in (tc, tc - len(tlab) + 1, tc + 1, tc - len(tlab)):
        if 0 <= p and p + len(tlab) <= w and all(glyph[i] is None
                                                  for i in range(p, p + len(tlab))):
            for j, ch in enumerate(tlab):
                glyph[p + j] = (ch, "accent", True, True)
            break
    for i, ((y, m), x0, x1) in enumerate(bands):
        d1 = date(y, m, 1)
        forms = ([f"{d1:%B} {y}"] if (i == 0 or m == 1) else []) + [f"{d1:%B}", f"{d1:%b}"]
        first = x0 + (1 if x0 > 0 else 0)
        runs, x = [], first
        while x < x1:
            if glyph[x] is None:
                e = x
                while e < x1 and glyph[e] is None:
                    e += 1
                runs.append((x + (1 if x > first else 0), e))
                x = e
            else:
                x += 1
        placed = None
        for rs, re_ in runs:
            room = re_ - rs - (0 if re_ in (w, x1) else 1)
            f = next((f for f in forms if len(f) <= room), None)
            if f:
                placed = (rs, f)
                break
        if placed:
            rs, f = placed
            key = "ink" if (y, m) == (today.year, today.month) else "hd"
            for j, ch in enumerate(f):
                glyph[rs + j] = (ch, key, True, False)
    out = [" " if g is None else _ruler_cell(*g) for g in glyph]
    return out


def _gantt_scale_label(k: float, name: str, label_w: int) -> str:
    if label_w >= 26:
        scale = {0.5: "1 day = 2 cells", 1: "1 cell = 1 day"}.get(k, f"1 cell = {k:g} days")
        return f"{name} · {scale}"
    return f"{name} · {f'{k:g}'.lstrip('0')} d/cell"     # `.5`: fits a 20-cell label


# --------------------------------------------------------------------------- #
# labels and the renderer
# --------------------------------------------------------------------------- #
def _gantt_group_label(g: GanttGroup, label_w: int, paged: bool = False) -> str:
    """`▾ name  ▲2 ✓1` unfolded, `▸ name  4 open ✓1` folded — the counts the
    folded rows no longer show, in the cells the name does not need."""
    wide = label_w >= 26
    bits: list[tuple[str, str]] = []
    if not g.unfolded or paged:
        bits.append((f"{len(g.open)} open" if wide else f"{len(g.open)}", "mut"))
    if g.late:
        bits.append((f"▲{g.late}", "over"))
    if g.rest and wide:
        bits.append((f"✓{len(g.rest)}", "done"))
    while bits and label_w - 2 - vis(" ".join(t for t, _ in bits)) - 2 < 1:
        bits.pop()                        # a narrow label sheds ✓n, then ▲n, then N
    plain = " ".join(t for t, _ in bits)
    name_w = label_w - 2 - vis(plain) - (2 if bits else 1)
    hue = g.project.color if g.project is not None else "dim"
    name = g.project.name if g.project is not None else "Inbox"
    head = c("▾ " if g.unfolded else "▸ ", hue)
    body = c(escape(fit(name, max(0, name_w))), hue, bold=True)
    tail = (" " + " ".join(c(t, k) for t, k in bits)) if bits else ""
    return _pad(head + body + tail, label_w)


def _gantt_legend(width: int, drawn: set[str]) -> str:
    """One row naming the marks this frame draws — only those — when the
    height has a row to spare."""
    wide = width >= 100
    items = [("⟦━⟧", "bright", "selected, exact dates", "selected"),
             # right after the selection, as the M-1 frames place them (D-624)
             ("◆", "mut", "milestone", "milestone"),
             ("◆✓", "reached", "reached", "reached"),
             ("↳", "mut", "waits on open work" if wide else "waits", "waits"),
             ("↳", "over", "starts before its dependency is due" if wide else "starts early",
              "early"),
             (CRITICAL_REACH, "crit", "critical chain" if wide else "chain", "crit"),
             ("●", "mut", "progress", "progress"),
             ("◆", "mut", "committed due" if wide else "due", "due"),
             ("◂▸", "mut", "beyond window", "beyond")]
    items = [it for it in items if it[3] in drawn]
    while items:
        out = " " + c(" · ", "dim").join(
            (c(g, "bright", bold=True) if k == "crit" else c(g, k)) + " " + c(t, "dim")
            for g, k, t, _ in items)
        if vis(_strip(out)) <= width:
            return _pad(out, width)
        items = items[:-1]
    return ""


def render_gantt(board, show_archived, selected_id, today=None,
                 width=68, height=0, line_map=None, tick=0,
                 focus: str | None = None, previous: str | None = None) -> Text:
    """The gantt as the app paints it: `_gantt_frame`'s rows, closed by the
    one-line legend when a row is spare (LLR-101.10)."""
    lines, drawn, _groups, _ax = _gantt_frame(board, show_archived, selected_id, today,
                                              width, height, line_map, tick, focus,
                                              previous)
    w = _clamp_width(width)
    pinned = 0
    if len(lines) < (height or 24):
        legend = _gantt_legend(w, drawn)
        if legend:
            lines.append(legend)
            pinned = 1
    return to_text(lines, height, w, pinned=pinned)


def _gantt_frame(board, show_archived, selected_id, today=None, width=68, height=0,
                 line_map=None, tick=0, focus: str | None = None,
                 previous: str | None = None, pinned_id: str | None = None):
    """THE WHOLE BOARD, FITTED (G-A), WITH A RULER THAT ANSWERS (AX-2).

    The shipped gantt laid every board on two days per cell with today at 30 %
    of the field and drew rows until the height ran out — "+9 not shown" on the
    board the operator judged it on, a whole project invisible. Now the window
    is fitted to the open work, projects fold to one span row when rows run
    out (the selected task's first, then the most urgent), finished work folds to
    `✓n`, and the dates sit on a two-row ruler at the top instead of an axis
    that dropped the month you were in.

    `focus` is a project id; when set only that project is drawn, and the
    Inbox is hidden, as in the kanban. Returns the rows (header, ruler, body),
    the marks they draw, the plan and the axis — the legend asks THIS frame
    what it shows (LLR-102.5)."""
    today = today or date.today()
    w = _clamp_width(width)
    h = height or 24
    label_w, chip_w, field_w = gantt_columns(w)
    body_rows = max(0, h - 1 - GANTT_RULER_ROWS) if height else 10 ** 6
    pinned_t = board.task_by_id(pinned_id) if pinned_id else None
    groups = gantt_plan(board, show_archived, selected_id, today, body_rows, focus,
                        previous, gantt_group_key(board, pinned_t) if pinned_t else None)
    ax = gantt_axis(field_w, today, *gantt_window(groups, today))
    guides, weekends = ax.guides(), ax.weekends()
    chain = set(critical_chain(board))
    sel = board.task_by_id(selected_id) if selected_id else None
    drawn: set[str] = set()

    def row(label: str, gut: str, cells: list[tuple[str, str]], chip: str) -> str:
        if any(g in (OFF_LEFT, OFF_RIGHT) for g, _ in cells):
            drawn.add("beyond")
        out = _pad(label, label_w) + gut + _gantt_field(cells, ax, guides, weekends)
        if chip_w:
            out += " " + chip
        return _pad(out, w)

    # the head: what is late, and how long the critical chain is
    late_n = sum(g.late for g in groups)
    focus_p = board.project_by_id(focus) if focus else None
    title = c("◆ GANTT", "bright", bold=True)
    if focus_p is not None:
        title += c(escape(" (focused: " + clip(focus_p.name, 40) + ")"), "mut")
    elif focus:                    # the focused project is not on this (filtered) board
        title += c(" (focused)", "mut")
    right_bits = [c(f"▲{late_n} past due", "over", bold=True) if late_n
                  else c("nothing past due", "dim")]
    if chain:
        right_bits.append(c(f"chain {len(chain)}", "hd"))
    lines = [header(title, c(" · ", "dim").join(right_bits), w, tone="bright")]

    # the ruler
    marks: dict[int, tuple[str, str]] = {}
    sel_p = board.project_by_id(sel.project_id) if sel is not None else None
    if sel_p is not None and (pd := parse_iso(sel_p.due_date)) and 0 <= ax.cell(pd) < ax.w:
        marks[ax.cell(pd)] = ("◆", sel_p.color)
    if sel_p is not None:          # the project's milestones on the ruler (AX-2, M-1)
        for t in board.visible_tasks(show_archived):
            if (t.project_id == sel_p.id and t.milestone and not t.archived
                    and (md_ := parse_iso(t.due_date)) and 0 <= ax.cell(md_) < ax.w):
                marks[ax.cell(md_)] = ("◆", milestone_tone(t, board, today))
    echo = gantt_echo(sel, board, ax, today) if sel is not None else None
    if echo is not None:
        drawn.add("selected")
    mcells = gantt_month_row(ax, today, marks)
    dcells, dmeta = gantt_day_row(ax, today, echo)
    if sel_p is not None:
        tag = "◆ dates · " if label_w >= 16 else "◆ "
        name = fit(sel_p.name, max(0, label_w - 1 - len(tag)))
        mlabel = (" " * max(0, label_w - 1 - len(tag) - vis(name)) + c("◆", sel_p.color)
                  + c(tag[1:], "dim") + c(escape(name), sel_p.color, bold=True) + " ")
    else:
        mlabel = c(fit(f"today {today:%a} {_md(today)}", label_w - 1, "right") + " ", "accent")
    if dmeta["echo_label"]:
        dlabel = c(fit(dmeta["echo_label"] + " ▸", label_w - 1, "right") + " ",
                   echo[1], bold=True)
    else:
        dlabel = c(fit(_gantt_scale_label(ax.k, dmeta["cadence"], label_w),
                       label_w - 1, "right") + " ", "dim")
    tail = " " * (chip_w + 1) if chip_w else ""
    lines.append(_pad(_pad(mlabel, label_w) + " " + "".join(mcells) + tail, w))
    lines.append(_pad(_pad(dlabel, label_w) + " " + "".join(dcells) + tail, w))

    # the body
    def span_row(g: GanttGroup, paged: bool = False) -> str:
        if g.project is not None:
            prog = board.project_progress(g.project.id, show_archived)
            cells = _gantt_span(g.project, ax, prog, tick)
            if any(gl == "◆" for gl, _ in cells):
                drawn.add("due")
            if any(gl == PROGRESS_DOT or gl in PULSE_PHASES for gl, _ in cells):
                drawn.add("progress")
            chip = (gantt_due_chip(g.project.due_date, today, chip_w) if g.open
                    else " " * chip_w)
        else:
            cells, chip = [(" ", "dim")] * ax.w, " " * chip_w
        return row(_gantt_group_label(g, label_w, paged), " ", cells, chip)

    def task_row(t: Task) -> str:
        mark = gantt_dep_mark(t, board, chain)
        if "↳" in mark:
            drawn.add("early" if HEX["over"] in mark else "waits")
        if t.milestone:            # one date, no bar (M-1, LLR-602.2)
            tone = milestone_tone(t, board, today)
            drawn.add("reached" if board.is_done(t) else "milestone")
            title = title_markup(t, label_w - 4, t.id == selected_id)
            if board.is_done(t):           # reached: the label goes quiet too (M-1)
                title = c(title, "reached")
            label = " " + c("◆", tone) + " " + title + " "
            return row(label, mark, gantt_milestone_cells(t, board, ax, today, tone),
                       gantt_milestone_chip(t, board, today, chip_w))
        cells = _gantt_bar(t, board, ax, chain, tick)
        if any(tone == "crit" for _, tone in cells):
            drawn.add("crit")
        label = "  " + title_markup(t, label_w - 3, t.id == selected_id) + " "
        return row(label, mark, cells, gantt_due_chip(t.due_date, today, chip_w))

    rows: list[tuple[str, str | None]] = []
    sel_g = next((i for i, g in enumerate(groups) if g.unfolded
                  and any(t.id == selected_id for t in g.open + g.rest)), None)
    sel_open = sel_g is not None and sel in groups[sel_g].rows
    if len(groups) > body_rows or (len(groups) == body_rows and sel_open):
        # the span rows alone fill the body (D8): the page of groups that
        # holds the selection, its selected task under its span, and a count
        # of the rest — every row of it inside the body, so the selection is
        # always drawn (F-3)
        if body_rows <= 2:                 # no room for a page: the selection
            if sel_open:
                rows = ([(span_row(groups[sel_g]), None)] if body_rows == 2 else [])
                rows.append((task_row(sel), sel.id))
            else:
                rows = [(span_row(g), None) for g in groups[:body_rows]]
        else:
            keep = body_rows - 2
            i0 = 0 if sel_g is None else (sel_g // keep) * keep    # page-aligned
            page = range(i0, min(len(groups), i0 + keep))
            for i in page:
                rows.append((span_row(groups[i]), None))
                if i == sel_g and sel_open:
                    rows.append((task_row(sel), sel.id))
            rows.append((_pad(c(f"  +{len(groups) - len(page)} not shown", "mut"), w),
                         None))
    else:
        # the link mode's pin (D-528): when the selected group and the pinned one
        # cannot both be drawn whole, they share the rows left — the pinned group
        # half, the selection the rest — instead of each counting the other whole
        share: dict[int, int] = {}
        pin_g = next((i for i, g in enumerate(groups) if g.unfolded and pinned_id
                      and any(t.id == pinned_id for t in g.rows)), None)
        avail = body_rows - len(groups)
        if (pin_g is not None and sel_g is not None and pin_g != sel_g
                and len(groups[pin_g].rows) + len(groups[sel_g].rows) > avail):
            share[pin_g] = min(len(groups[pin_g].rows), max(0, avail // 2))
            share[sel_g] = avail - share[pin_g]
        for gi, g in enumerate(groups):
            shown, paged, hint = (list(g.rows) if g.unfolded else []), False, ""
            if g.unfolded:
                room = share.get(gi, body_rows - len(groups) - sum(
                    len(x.rows) for x in groups if x.unfolded and x is not g))
                if len(shown) > room:     # the selected group, taller than the body
                    if room < 1:          # only when groups == body and the
                        shown, paged = [], True   # selection is rest work: no row owed
                    else:
                        # pages of the rows left, less one for the hint row
                        # under the page (answer D9) when there are two or more
                        size = room - 1 if room >= 2 else room
                        ids = [t.id for t in shown]       # the page holds the selection,
                        i = (ids.index(selected_id) if selected_id in ids     # else the
                             else ids.index(pinned_id) if pinned_id in ids else 0)  # pin
                        first = (i // size) * size
                        if (selected_id in ids and pinned_id in ids
                                and abs(ids.index(pinned_id) - i) < size):
                            # the link's two rows in one group: a page that
                            # holds both, whenever one can (code review 006 M1)
                            hi = max(i, ids.index(pinned_id))
                            lo = min(i, ids.index(pinned_id))
                            if not first <= lo or not hi < first + size:
                                first = hi - size + 1
                        above, below = first, max(0, len(shown) - first - size)
                        shown, paged = shown[first:first + size], True
                        if room >= 2:
                            hint = " / ".join(p for p in (above and f"▲ {above} above",
                                                          below and f"▼ {below} below") if p)
            rows.append((span_row(g, paged), None))
            rows.extend((task_row(t), t.id) for t in shown)
            if hint:
                rows.append((_pad(c(escape(fit("  " + hint, w)), "dim"), w), None))

    if not groups:
        lines.append(_pad(c("  (nothing scheduled — press 'a' to add a task)", "dim"), w))
    for markup, tid in rows:
        lines.append(markup)
        if tid is not None and line_map is not None:
            line_map[tid] = len(lines) - 1
    return lines, drawn, groups, ax


# ---------------------------------------------------------------------------
# view: FOCUS  (pinned tasks and tasks of pinned projects, three presentations)
# ---------------------------------------------------------------------------

# Highlight syntax for notes inside the Focus Board. The delimiters are chosen
# to be easy to type and unlikely to collide with ordinary markdown/URLs.
_HIGHLIGHT_RE = re.compile(r"==(.*?)==|!!(.*?)!!|\+\+(.*?)\+\+")


def highlight_segments(text: str) -> list[tuple[str, str]]:
    """The one tokeniser of the notes' highlight syntax: ==text== `soon`,
    !!text!! `over`, ++text++ `green`, everything else `mut` — as (segment,
    tone) pairs, markers dropped. The board's markup (`_highlight_markup`) and
    the details / editor preview's Text pieces (`modals.notes_preview`) both read
    it, so the two seats cannot disagree on what a note highlights (D-411)."""
    out: list[tuple[str, str]] = []
    last = 0
    for m in _HIGHLIGHT_RE.finditer(text):
        if m.start() > last:
            out.append((text[last:m.start()], "mut"))
        if m.group(1) is not None:
            out.append((m.group(1), "soon"))
        elif m.group(2) is not None:
            out.append((m.group(2), "over"))
        else:
            out.append((m.group(3), "green"))
        last = m.end()
    if last < len(text):
        out.append((text[last:], "mut"))
    return out


def _highlight_markup(text: str) -> str:
    """Render ==text== (yellow), !!text!! (red), ++text++ (green). The
    non-highlighted text is returned in the 'mut' tone so the caller can use the
    result directly without wrapping it again."""
    parts = [c(escape(segment), tone) for segment, tone in highlight_segments(text)]
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
                       "mut"))
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
            out.append(c(escape(fit(clip(u, width), width)), "mut"))

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
                                                  "mut"),
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
    marks = link_marks(board)
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
                                    today=today,
                                    marks=marks), q.id))

    title = c("◆ FOCUS", "bright", bold=True) + c(" · review", "mut")
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
    title = c("◆ FOCUS", "bright", bold=True) + c(" · stale first", "mut")
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
    title = c("◆ FOCUS", "bright", bold=True) + c(f" · {presentation}", "mut")
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
# view: FLOW  (cycle time, heatmap, throughput — derived from history.jsonl)
# ---------------------------------------------------------------------------
_FLOW_WEEKS = 8
_FLOW_RAMP = (" ", "░", "▒", "▓", "█")


def _flow_parse_at(value: str) -> datetime | None:
    """Parse an ISO timestamp from the log; a malformed one is ignored."""
    try:
        return datetime.fromisoformat(value)
    except (ValueError, TypeError):
        return None


def _flow_week_key(d: date) -> str:
    """ISO week key used for every bucket: ``2026-W33``."""
    return d.strftime("%G-W%V")


def _flow_last_weeks(today: date, n: int = _FLOW_WEEKS) -> list[str]:
    """The last ``n`` ISO weeks ending at ``today``, current rightmost."""
    weeks: list[str] = []
    d = today
    for _ in range(n):
        weeks.append(_flow_week_key(d))
        d -= timedelta(weeks=1)
    weeks.reverse()
    return weeks


def _flow_intervals(records: list[dict]) -> dict[str, list[tuple[str, datetime, datetime | None]]]:
    """Per task, ordered list of (phase, start, end) intervals.

    A record opens an interval in its ``to`` phase; the task's next record
    closes it.  The final interval is open and closes at "now"."""
    by_task: dict[str, list[dict]] = {}
    for r in records:
        by_task.setdefault(r.get("task", ""), []).append(r)
    intervals: dict[str, list[tuple[str, datetime, datetime | None]]] = {}
    for tid, recs in by_task.items():
        recs = [r for r in recs if _flow_parse_at(r.get("at", "")) is not None]
        recs.sort(key=lambda r: _flow_parse_at(r["at"]))  # type: ignore[arg-type]
        task_intervals: list[tuple[str, datetime, datetime | None]] = []
        for i, r in enumerate(recs):
            start = _flow_parse_at(r["at"])
            end = _flow_parse_at(recs[i + 1]["at"]) if i + 1 < len(recs) else None
            task_intervals.append((r.get("to", ""), start, end))  # type: ignore[arg-type]
        intervals[tid] = task_intervals
    return intervals


def _flow_cycle_times(intervals: dict[str, list[tuple[str, datetime, datetime | None]]],
                      phases: list[str]) -> dict[str, tuple[float | None, int]]:
    """Median whole days per phase over closed intervals; open-count when none.

    Returns ``{phase: (median_days, open_count)}``.  ``median_days`` is ``None``
    when the phase has no closed interval; ``open_count`` is then the number of
    still-open intervals (so the view can say "open n=N")."""
    closed: dict[str, list[int]] = {p: [] for p in phases}
    open_n: dict[str, int] = {p: 0 for p in phases}
    for task_intervals in intervals.values():
        for phase, start, end in task_intervals:
            if phase not in closed:
                continue
            if end is None:
                open_n[phase] += 1
            else:
                days = (end.date() - start.date()).days
                if days >= 0:
                    closed[phase].append(days)
    result: dict[str, tuple[float | None, int]] = {}
    for phase in phases:
        vals = sorted(closed[phase])
        if vals:
            n = len(vals)
            median = float(vals[n // 2]) if n % 2 else (vals[n // 2 - 1] + vals[n // 2]) / 2.0
            result[phase] = (median, 0)
        else:
            result[phase] = (None, open_n[phase])
    return result


def _flow_heatmap(intervals: dict[str, list[tuple[str, datetime, datetime | None]]],
                  phases: list[str], weeks: list[str]) -> dict[str, list[float]]:
    """Task-days per phase per ISO week over the last ``_FLOW_WEEKS`` weeks."""
    values: dict[str, list[float]] = {p: [0.0] * len(weeks) for p in phases}
    index = {w: i for i, w in enumerate(weeks)}
    now = datetime.now()
    for task_intervals in intervals.values():
        for phase, start, end in task_intervals:
            if phase not in values:
                continue
            end_dt = end or now
            d = start.date()
            last = end_dt.date()
            while d <= last:
                wk = _flow_week_key(d)
                if wk in index:
                    values[phase][index[wk]] += 1.0
                d += timedelta(days=1)
    return values


def _flow_throughput(records: list[dict], terminal_phase: str,
                     weeks: list[str]) -> list[int]:
    """Tasks whose ``to`` phase is the current terminal phase, per week."""
    counts = [0] * len(weeks)
    index = {w: i for i, w in enumerate(weeks)}
    for r in records:
        if r.get("to") != terminal_phase:
            continue
        at = _flow_parse_at(r.get("at", ""))
        if at is None:
            continue
        wk = _flow_week_key(at.date())
        if wk in index:
            counts[index[wk]] += 1
    return counts


def _flow_ramp_char(value: float, max_val: float) -> str:
    """One of the four block-ramp glyphs, or a space for zero."""
    if max_val <= 0 or value <= 0:
        return _FLOW_RAMP[0]
    ratio = value / max_val
    if ratio < 0.25:
        return _FLOW_RAMP[1]
    if ratio < 0.5:
        return _FLOW_RAMP[2]
    if ratio < 0.75:
        return _FLOW_RAMP[3]
    return _FLOW_RAMP[4]


def _flow_format_median(median: float) -> str:
    """Even-n median keeps one decimal; odd-n renders as an integer."""
    if median == int(median):
        return f"{int(median)}d"
    return f"{median:.1f}d"


def render_flow(board, show_archived, selected_id, today=None,
                width=68, height=0, line_map=None) -> Text:
    """A read-only dashboard of work movement: cycle time, heatmap, throughput.

    Derived entirely from the append-only ``history.jsonl`` sidecar.  With no
    history the body states the fact honestly in one sentence and draws no
    metric glyphs; with even a single transition it renders all three artifacts.
    Phase labels are untrusted input — intersected with ``board.phases`` and
    escaped at render."""
    today = today or date.today()
    w = _clamp_width(width)
    inner = w

    records, _skipped = history.read(board.path)
    known = {t.id for t in board.visible_tasks(True)}
    records = [r for r in records if r.get("task") in known]

    lines = [header(c("FLOW", "bright", bold=True), "", w)]
    lines.append(head_rule(w))

    if not records:
        msg = "no history yet — it builds from today"
        lines.append(line(c(fit(escape(msg), inner), "mut")))
        lines.append(bottom(None, w))
        return to_text(lines, height, w)

    # phases that actually appear in history, in the board's declared order
    history_phases = {r.get("to") for r in records}
    phases = [p for p in board.phases if p in history_phases]
    if not phases:
        phases = list(board.phases)

    weeks = _flow_last_weeks(today)
    intervals = _flow_intervals(records)
    cycle = _flow_cycle_times(intervals, phases)
    heatmap = _flow_heatmap(intervals, phases, weeks)
    terminal = board.phases[-1] if board.phases else ""
    throughput = _flow_throughput(records, terminal, weeks)

    # ---- cycle time ---------------------------------------------------------
    lines.append(line(c(fit("CYCLE", inner), "hd", bold=True)))
    cycle_label_w = max(8, inner - 17)  # leaves room for "open n=N"
    for phase in phases:
        median, open_n = cycle.get(phase, (None, 0))
        if median is not None:
            value = _flow_format_median(median)
            value_col = "ink"
        elif open_n:
            value = f"open n={open_n}"
            value_col = "mut"
        else:
            value = "—"
            value_col = "dim"
        left = "  " + fit(phase, cycle_label_w)
        right_w = max(4, inner - vis(left) - 1)
        right = fit(value, right_w, "right")
        lines.append(line(c(left, "ink") + " " + c(right, value_col)))

    # ---- heatmap ------------------------------------------------------------
    lines.append(line(c(fit("HEATMAP", inner), "hd", bold=True)))
    max_val = max((v for vals in heatmap.values() for v in vals), default=0)
    label_w = min(10, max(4, inner // 5))
    data_start = label_w + 1
    data_w = max(0, inner - data_start)
    if data_w >= _FLOW_WEEKS:
        # week-number header ("26 27 ...") if it fits
        if data_w >= _FLOW_WEEKS * 2 - 1:
            nums = [wk.split("-W")[1] for wk in weeks]
            parts = []
            pos = 0
            for i, num in enumerate(nums):
                parts.append(num)
                pos += 2
                if i < len(nums) - 1 and pos < data_w:
                    parts.append(" ")
                    pos += 1
            header_row = " " * data_start + "".join(parts)
            lines.append(line(c(fit(header_row, inner), "mut")))
        for phase in phases:
            vals = heatmap.get(phase, [0.0] * len(weeks))
            cells = []
            pos = 0
            for i, v in enumerate(vals):
                cells.append(_flow_ramp_char(v, max_val))
                pos += 1
                if i < len(vals) - 1 and pos < data_w:
                    cells.append(" ")
                    pos += 1
            row = fit(phase, label_w) + " " + "".join(cells)
            lines.append(line(c(fit(row, inner), "mut")))

    # ---- throughput ---------------------------------------------------------
    lines.append(line(c(fit("THROUGHPUT", inner), "hd", bold=True)))
    total = sum(throughput)
    max_tp = max(throughput) if throughput else 0
    if data_w >= _FLOW_WEEKS:
        nums = [wk.split("-W")[1] for wk in weeks]
        parts = []
        pos = 0
        for i, num in enumerate(nums):
            parts.append(num)
            pos += 2
            if i < len(nums) - 1 and pos < data_w:
                parts.append(" ")
                pos += 1
        header_row = " " * data_start + "".join(parts)
        lines.append(line(c(fit(header_row, inner), "mut")))
        count_cells = []
        pos = 0
        for i, n in enumerate(throughput):
            s = str(n)
            count_cells.append(s)
            pos += len(s)
            if i < len(throughput) - 1 and pos < data_w:
                count_cells.append(" ")
                pos += 1
        count_row = " " * data_start + "".join(count_cells)
        lines.append(line(c(fit(count_row, inner), "ink")))
        bar_cells = []
        pos = 0
        for i, n in enumerate(throughput):
            bar_cells.append(_flow_ramp_char(float(n), float(max_tp)) if max_tp else " ")
            pos += 1
            if i < len(throughput) - 1 and pos < data_w:
                bar_cells.append(" ")
                pos += 1
        bar_row = " " * data_start + "".join(bar_cells)
        lines.append(line(c(fit(bar_row, inner), "hd")))
    summary = f"total {total}"
    lines.append(line(c(fit(summary, inner, "right"), "mut")))

    lines.append(bottom(None, w))
    return to_text(lines, height, w)


# ---------------------------------------------------------------------------
# team classification filter chrome (V2/V3)
# ---------------------------------------------------------------------------
TEAM_FILTER_MODES = ("todo", "equipo", "personal")
# what each stored mode is CALLED on screen (batch 2026-10-02-batch-02, HLR-204):
# the values are data and stay as they are; only the painted word is English
TEAM_FILTER_LABELS = {"todo": "all", "equipo": "team", "personal": "personal"}


def render_team_filter_chrome(active: str) -> str:
    """The segmented control `all · team · personal` as markup.

    The active segment is bold `bright`; the others wear the quiet dim
    house (the colour budget: the accent marks focus, not a chosen value).
    The separator is neutral so the three segments read as one control.

    Semantics of each mode when applied to a member's task list:

    * ``todo`` — every visible task, regardless of project.
    * ``equipo`` — only tasks whose ``project_id`` is in the authoritative
      ``team.json`` shared project list.
    * ``personal`` — only tasks whose ``project_id`` is NOT in the shared
      project list (including Inbox / project-less tasks).
    """
    out: list[str] = []
    for mode in TEAM_FILTER_MODES:
        label = TEAM_FILTER_LABELS[mode]
        out.append(c(label, "bright", bold=True) if mode == active else c(label, "dim"))
    return " · ".join(out)


def _member_tasks_for_filter(board: Board, team_state: TeamState,
                             uid: str, team_filter: str):
    """The tasks that belong to ``uid`` after applying the classification filter.

    The operator's own tasks come from the local ``board``; everyone else's come
    from ``team_state.foreign_tasks()`` filtered by owner.  The filter semantics
    are documented in ``render_team_filter_chrome``.
    """
    team_ids = team_state.team_project_ids()
    if uid == team_state.user_id:
        tasks = list(board.tasks)
    else:
        tasks = [t for t, owner in team_state.foreign_tasks() if owner == uid]
    if team_filter == "todo":
        return tasks
    if team_filter == "equipo":
        return [t for t in tasks if t.project_id in team_ids]
    if team_filter == "personal":
        return [t for t in tasks if t.project_id not in team_ids]
    return tasks


def _self_sync_age_minutes(team_state: TeamState) -> int | None:
    """Minutes since the operator's own last push, or None if never pushed."""
    pushed_at = team_state.last_push_at
    if not isinstance(pushed_at, str):
        return None
    try:
        from datetime import datetime, timezone
        dt = datetime.fromisoformat(pushed_at.replace("Z", "+00:00"))
        return int((datetime.now(timezone.utc) - dt).total_seconds() // 60)
    except ValueError:
        return None


def _format_sync_age(age: int | None) -> str:
    """A short, width-honest age label."""
    if age is None:
        return "—"
    if age < 60:
        return f"{age}m"
    return f"{age // 60}h{age % 60:02d}"


# ---------------------------------------------------------------------------
# view: STANDUP  (V3 team home — one row per roster member)
# ---------------------------------------------------------------------------
def render_standup(board, show_archived, selected_id, today=None,
                   width=68, height=0, line_map=None,
                   team_state: TeamState | None = None,
                   team_filter: str = "equipo") -> Text:
    """The V3 team home: one row per roster member.

    Each row shows the member name, a load bar (``▰▱``) of open team tasks
    against a sensible maximum, the member's top open task title + phase, and
    the sync age. The operator's own row carries a bright spine. Stale rows
    wear the ``over`` tone; fresh rows wear ``mut``.

    When team mode is off ``team_state`` is ``None`` and the body says so.
    """
    today = today or date.today()
    w = _clamp_width(width)
    inner = w

    chrome = render_team_filter_chrome(team_filter)
    lines = [header(c("STANDUP", "bright", bold=True) + c(" · ", "mut") + chrome,
                    "", w)]
    lines.append(head_rule(w))

    if team_state is None:
        msg = "team mode off — set a shared directory"
        lines.append(line(c(fit(escape(msg), inner), "mut")))
        lines.append(bottom(None, w))
        return to_text(lines, height, w)

    roster = team_state.roster()
    if not roster:
        msg = "no roster — check team.json"
        lines.append(line(c(fit(escape(msg), inner), "mut")))
        lines.append(bottom(None, w))
        return to_text(lines, height, w)

    names = team_state.member_names()
    hues = team_state.member_hues()
    max_load = 5
    load_bar_w = max_load

    for member in roster:
        uid = member["id"]
        name = escape(names.get(uid, uid))
        hue = hues.get(uid, "mut")
        is_self = uid == team_state.user_id

        tasks = _member_tasks_for_filter(board, team_state, uid, team_filter)
        open_tasks = [t for t in tasks if not board.is_done(t)]
        load = min(len(open_tasks), max_load)
        bar = "▰" * load + "▱" * (max_load - load)

        # top task: first open task by due date, or first task overall if none open
        candidates = sort_by_due(open_tasks) if open_tasks else sort_by_due(tasks)
        top = candidates[0] if candidates else None

        if uid == team_state.user_id:
            age = _self_sync_age_minutes(team_state)
        else:
            age = team_state.sync_age(uid)
        age_text = _format_sync_age(age)

        tone = sync_tone(team_state, uid)
        # the operator's own row is identifiable by a bright spine
        prefix = c("▌", "bright") + " " if is_self else c("▎", hue) + " "
        prefix_w = 2

        # right side: sync age, with a little breathing room
        right = c(age_text, "over" if tone == "over" else "dim")
        right_w = vis(age_text)

        # name column: generous but not greedy
        name_w = min(12, max(4, inner - prefix_w - load_bar_w - 1 - right_w - 1 - 1))
        name_field = c(fit(name, name_w), tone, bold=is_self)

        # task column fills the rest
        task_x = prefix_w + name_w + 1 + load_bar_w + 1
        task_w = max(0, inner - task_x - right_w - 1)
        if top is not None:
            phase = escape(str(top.phase))
            tail = f" · {phase}"
            tail_w = vis(tail)
            title_w = max(0, task_w - tail_w)
            title = escape(fit(top.title, title_w))
            task_field = c(title, tone) + c(tail, "dim")
        else:
            task_field = c(fit("—", task_w), "dim")

        row = prefix + name_field + " " + c(bar, "mut") + " " + task_field
        # pad to inner exactly, then append right with one space
        row_vis = vis(_strip(row))
        pad = max(0, inner - row_vis - right_w - 1)
        if pad:
            row += " " * pad
        row += " " + right
        lines.append(line(row))

    lines.append(bottom(None, w))
    return to_text(lines, height, w)


# ---------------------------------------------------------------------------
# view: PEOPLE  (V2 people lanes — axis is WHO, not project)
# ---------------------------------------------------------------------------
def render_people(board, show_archived, selected_id, today=None,
                  width=68, height=0, line_map=None,
                  team_state: TeamState | None = None,
                  team_filter: str = "equipo") -> Text:
    """The V2 people-lanes view: one lane per roster member.

    Each lane header names the member and shows their sync age; the operator's
    own lane carries a bright spine and a bold label. Cards below the header
    are drawn with ``card_cell``; foreign cards carry the read-only ``◦`` mark
    in the quiet mut house. The classification filter changes which tasks are
    visible in each lane without touching the merged model.
    """
    today = today or date.today()
    w = _clamp_width(width)
    inner = w
    marks = link_marks(board)            # board tasks only; a teammate's paint none

    chrome = render_team_filter_chrome(team_filter)
    lines = [header(c("PEOPLE", "bright", bold=True) + c(" · ", "mut") + chrome,
                    "", w)]
    lines.append(head_rule(w))

    if team_state is None:
        msg = "team mode off — set a shared directory"
        lines.append(line(c(fit(escape(msg), inner), "mut")))
        lines.append(bottom(None, w))
        return to_text(lines, height, w)

    roster = team_state.roster()
    if not roster:
        msg = "no roster — check team.json"
        lines.append(line(c(fit(escape(msg), inner), "mut")))
        lines.append(bottom(None, w))
        return to_text(lines, height, w)

    names = team_state.member_names()
    hues = team_state.member_hues()
    prefix_w = 2

    for member in roster:
        uid = member["id"]
        name = escape(names.get(uid, uid))
        hue = hues.get(uid, "mut")
        is_self = uid == team_state.user_id

        tasks = _member_tasks_for_filter(board, team_state, uid, team_filter)
        tasks = sort_by_due(tasks)

        if uid == team_state.user_id:
            age = _self_sync_age_minutes(team_state)
        else:
            age = team_state.sync_age(uid)
        age_text = _format_sync_age(age)
        tone = sync_tone(team_state, uid)

        # lane header: spine + name + sync age
        prefix = c("▌", "bright") + " " if is_self else c("▎", hue) + " "
        right = c(age_text, "over" if tone == "over" else "dim")
        right_w = vis(age_text)
        name_w = max(0, inner - prefix_w - 1 - right_w)
        name_field = c(fit(name, name_w), tone, bold=is_self)
        header_row = prefix + name_field + " " + right
        lines.append(line(header_row))

        if not tasks:
            lines.append(line("  " + c(fit("—", max(0, inner - prefix_w)), "dim")))
        else:
            for t in tasks:
                readonly = not is_self
                card = card_cell(t, board, max(0, inner - prefix_w),
                                 t.id == selected_id, today=today,
                                 readonly=readonly, marks=marks)
                lines.append(line("  " + card))
                if line_map is not None:
                    line_map[t.id] = len(lines) - 1

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
                     tasks: list[Task], n: int | None = None) -> list[str]:
    """Phase-name header cells, with `◀ N` / `N ▶` counts for hidden phases.

    Every cell ends with the WIP tag (HLR-005, LLR-005.2): ` n/limit` when the
    phase has a limit, bare ` n` when it does not — `n` counted from
    `phase_buckets` over the view's visible tasks. The tag is laid out LAST
    and the phase name is truncated BEFORE it, so the count survives width
    pressure (the tag-last layout of the approved proto). It burns in the
    `over` tone ONLY when strictly over the limit — exactly AT the limit is
    calm (the off-by-one is the cheapest mutation here)."""
    n = len(board.phases) if n is None else n   # the phases a window can hide
    end = start + len(widths)
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


def kanban_work(tasks: list[Task]) -> list[Task]:
    """The kanban lays out WORK: a milestone is never a card, a count or a WIP
    tag in any presentation (LLR-603.1, D-607) — it rides its project's band
    rule. ONE seat, read by every presentation, the nav and the `/` counts."""
    return [t for t in tasks if not t.milestone]


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
_KANBAN_SORT_MODES = ("project", "priority", "due", "recent", "unblock")
_KANBAN_GROUP_MODES = ("project", "priority", "horizon")
_PRIO_RANK = {"high": 0, "normal": 1, "low": 2}


def _recent_first(tasks: list[Task]) -> list[Task]:
    """`phase_changed` newest first, unknown stamps sunk, ties in board order
    (ISO date stamps sort lexicographically; sorted() is stable, and `reverse`
    does not disturb equal keys). None is UNKNOWN and sinks — never read as 0."""
    return sorted(tasks, key=lambda t: t.phase_changed or "", reverse=True)


# The name of the band group `kanban_order(band=True)` puts first. NUL-led so
# no user-typed project name can equal it; only the grouped renderer reads it,
# and it draws the band's own divider instead of a group header.
KANBAN_BAND = "\x00high-band"


def kanban_order(board, tasks, show_archived, *, group="project",
                 sort="project", collapsed=False, focus=None,
                 today=None, band=False) -> list[tuple[str, str, list[Task]]]:
    """The ordered `(name, color, tasks)` groups for ONE kanban column, under
    the active group/sort modes. Pure: no I/O, no mutation of `board`/`tasks`.

    Sort (intra-group, ALL modes STABLE — a tie the keys leave open keeps the
    board's pre-sort order, §6.5 AMD-09): `project` = board order as given;
    `priority` = blocked first, then high→normal→low, ties by due (undated
    sink); `due` = `sort_by_due` semantics with blocked first; `recent` =
    `_recent_first`; `unblock` = unblocked tasks with the most dependents first,
    blocked tasks sink. Group: `project` = `_kanban_groups` verbatim (Inbox
    last); `priority` = High/Normal/Low; `horizon` = Overdue/This week/Later/
    No date by `urgency()`, plus a trailing `Done` group — dim tone, its OWN
    pinned `phase_changed`-desc order regardless of the sort mode (§6.5
    AMD-04/D-11: `urgency()` reports done before reading any date). Empty
    groups are omitted — an empty group header is a ghost mark.

    `band=True` (K4, owner verdict 2026-09-30) lifts the column's OPEN high
    cards — not done, not archived, blocked included — out of their groups into
    a first group named KANBAN_BAND, after the focus filter and sorted like any
    group. Only the grouped presentation asks for it (renderer AND navigator,
    so the cursor walks what is drawn); with group=priority the High group
    already is the band, so none is added."""
    if collapsed:            # a collapsed column contributes NOTHING (R-07)
        return []
    if focus is not None:    # a project focus hides every other project (R-08)
        tasks = [t for t in tasks if t.project_id == focus]
    band_items: list[Task] = []
    if band and group != "priority":
        band_items = [t for t in tasks if t.priority == "high"
                      and not board.is_done(t) and not t.archived]
        lifted = {id(t) for t in band_items}
        tasks = [t for t in tasks if id(t) not in lifted]
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
                                            ("week", "This week", "hd"),
                                            ("later", "Later", "mut"),
                                            ("none", "No date", "dim"))]
        groups = [g for g in groups if g[2]]
        if buckets["done"]:
            pinned = "Done"
            groups.append(("Done", "dim", _recent_first(buckets["done"])))
    else:                    # "project" — today's grouping, Inbox last
        groups = _kanban_groups(board, tasks, show_archived)
    if band_items:
        groups.insert(0, (KANBAN_BAND, "ink", band_items))
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
    elif sort == "unblock":
        # board-wide dependency counts, computed once per call
        counts = {t.id: unblocks_count(board, t)
                  for t in board.tasks
                  if not board.is_done(t) and not t.archived}

        def order(items: list[Task]) -> list[Task]:
            return sorted(items, key=lambda t: (
                t.blocked, -counts.get(t.id, 0)))
    else:                    # "due" — sort_by_due semantics, blocked first
        def order(items: list[Task]) -> list[Task]:
            return sorted(items, key=lambda t: (
                not t.blocked, parse_iso(t.due_date) is None,
                parse_iso(t.due_date) or date.max))
    return [(name, color, items if name == pinned else order(items))
            for name, color, items in groups]


# --- the readable board (batch 2026-10-02-batch-03: K-A + R-1b) -------------
# The grouped presentation draws BANDS across the columns: a band rule names a
# group ONCE, the group's cards sit under it column by column, two rows each,
# and the last phase is a narrow rail on the right. The open high cards ride ONE
# band above every other, capped at two thirds of the body. Renderer and navigator both
# read `kanban_plan` — one seat, so the cursor walks what is drawn (F-3).
KANBAN_RAIL_WIDE = 16       # the rail drawing done titles, from KANBAN_WIDE cells
KANBAN_RAIL_NARROW = 7      # the rail as a count (narrower, or collapsed)
KANBAN_WIDE = 100
KANBAN_HEAD_ROWS = 3        # the head row, the phase row, the rule


class KanbanBand(NamedTuple):
    name: str
    color: str
    project: object          # the band's Project, or None (Inbox, another group mode)
    cols: list               # per open phase: the band's cards, in seat order
    done: list               # every done task of the band, newest first
    rail: list               # the done tasks the rail draws as titles
    n_open: int              # the group's open cards, its highs in the high band included
    n_high: int              # the group's cards drawn in the high band


class KanbanPlan(NamedTuple):
    tasks: list              # the visible tasks, after the focus
    start: int               # the first open phase drawn
    widths: list             # the drawn open columns' widths
    rail_w: int
    rail_titles: bool        # done tasks drawn as selectable titles
    high: list               # per open phase: the high band's cards
    overflow: list           # per open phase: open highs the cap left in their bands
    bands: list


def _cell_rows(n: int) -> int:
    """The rows `n` stacked two-row cards take, a `┈` row between each two."""
    return 3 * n - 1 if n else 0


def _kanban_widths(room: int, desired: list[int]) -> list[int]:
    """`room` cells over the columns by what their titles want (LLR-302.1): in
    proportion to the wants (the approved frames' rule), the remainder to the
    widest wants first; when that leaves a column under MIN_COL, every column
    gets MIN_COL first and the rest goes by the want above it. Sums to `room`."""
    k = len(desired)
    if room < k * MIN_COL:
        return distribute(room, k)

    def split(total: int, weights: list[int]) -> list[int]:
        if not sum(weights):
            return distribute(total, k)
        shares = [total * x // sum(weights) for x in weights]
        for i in sorted(range(k), key=lambda i: (-desired[i], i))[:total - sum(shares)]:
            shares[i] += 1
        return shares

    widths = split(room, desired)
    if min(widths) >= MIN_COL:
        return widths
    return [MIN_COL + s for s in split(room - k * MIN_COL, [d - MIN_COL for d in desired])]


def kanban_plan(board, show_archived, selected_id, today, width, height, *,
                sort="project", group="project", collapsed=False,
                focus=None) -> KanbanPlan:
    """THE seat of the grouped kanban (LLR-301.1): which cards each band holds
    per column, the high band and its cap, the rail and the column window —
    all through `kanban_order`, never a second ordering."""
    today = today or date.today()
    w = _clamp_width(width)
    tasks = kanban_work(board.visible_tasks(show_archived))
    if focus is not None and board.project_by_id(focus) is not None:
        tasks = [t for t in tasks if t.project_id == focus]
    n_open = len(board.phases) - 1
    buckets = phase_buckets(board, tasks)
    seat = {"group": group, "sort": sort, "focus": focus, "today": today}
    cap = max(5, 2 * (height - KANBAN_HEAD_ROWS) // 3) if height else None  # LLR-306.1
    high, overflow, rest = [], [], []
    for bucket in buckets[:n_open]:
        groups = kanban_order(board, bucket, show_archived, band=True, **seat)
        lifted = groups[0][2] if groups and groups[0][0] == KANBAN_BAND else []
        shown = lifted
        if cap is not None and _cell_rows(len(lifted)) > cap:
            shown = lifted[:cap // 3]
        high.append(shown)
        overflow.append(len(lifted) - len(shown))
        drawn = {id(t) for t in shown}
        rest.append([t for t in bucket if id(t) not in drawn])

    def keyed(items_by_group) -> dict:
        """The seat's groups by identity — two projects may share a name."""
        out: dict = {}
        for name, color, items in items_by_group:
            p = board.project_by_id(items[0].project_id) if group == "project" else None
            out.setdefault((name, p.id if p else None), (color, p, []))[2].extend(items)
        return out

    cols = [keyed(kanban_order(board, r, show_archived, **seat)) for r in rest]
    done = keyed(kanban_order(board, buckets[-1], show_archived, **seat)) if buckets else {}
    in_high = keyed(kanban_order(board, [t for col in high for t in col],
                                 show_archived, **seat))
    rail_titles = w >= KANBAN_WIDE and not collapsed
    bands = []
    for key, (color, project, _all) in keyed(kanban_order(board, tasks, show_archived,
                                                          **seat)).items():
        band_cols = [c_.get(key, (None, None, []))[2] for c_ in cols]
        band_done = _recent_first(done.get(key, (None, None, []))[2])
        if not any(band_cols) and not band_done:
            continue
        rail = band_done if rail_titles else []
        room = max([_cell_rows(len(c_)) for c_ in band_cols] + [3])
        if 2 * len(rail) > room:
            rail = rail[:(room - 1) // 2]
        n_high = len(in_high.get(key, (None, None, []))[2])
        bands.append(KanbanBand(key[0], color, project, band_cols, band_done, rail,
                                sum(1 for c_ in band_cols for t in c_ if not t.archived)
                                + n_high, n_high))
    rail_w = KANBAN_RAIL_WIDE if rail_titles else KANBAN_RAIL_NARROW
    if not n_open:                  # one phase: nothing is open, the rail is the board
        rail_w = w
    start, widths = 0, []
    if n_open:
        grid = w - rail_w - 1                  # the open columns and their `│`s
        fits = max(1, min(n_open, (grid + 1) // (MIN_COL + 1)))
        if fits < n_open:                      # the shipped window: follow the selection
            sel = board.task_by_id(selected_id)
            s = min(board.phase_index(sel), n_open - 1) if sel is not None else 0
            start = max(0, min(n_open - fits, s - (fits - 1) // 2))
        desired = [max([MIN_COL] + [vis(t.title) + 5 for t in buckets[i]])
                   for i in range(start, start + fits)]
        widths = _kanban_widths(grid - (fits - 1), desired)
    return KanbanPlan(tasks, start, widths, rail_w, rail_titles, high, overflow, bands)


def kanban_nav(plan: KanbanPlan) -> list[list[str]]:
    """The arrow-key columns: one per open phase, then the rail when it draws
    titles — every card the board draws when nothing is windowed, in draw order
    (the window follows the selection, as the phase window always has)."""
    cols = [[t.id for t in plan.high[i]] + [t.id for b in plan.bands for t in b.cols[i]]
            for i in range(len(plan.high))]
    if plan.rail_titles:
        cols.append([t.id for b in plan.bands for t in b.rail])
    return cols


def _wrap_title(title: str, w: int) -> tuple[str, str]:
    """(head, rest): the title cut on a word boundary at `w` cells. A first word
    wider than `w` is cut with `…` and leaves no rest."""
    if vis(title) <= w:
        return title, ""
    words, head = title.split(" "), ""
    for i, word in enumerate(words):
        cand = f"{head} {word}" if head else word
        if vis(cand) > w:
            break
        head = cand
    if not head:
        return fit(title, w), ""
    return head, " ".join(words[i:])


def _card_meta(task, board, today, marks, tag) -> list[tuple[str, str]]:
    """Row 2's tokens, the least needed first: `_fit_indicators` sheds from the
    left, so the due token is the last to go (LLR-301.2)."""
    toks: list[tuple[str, str]] = []
    if has_url(task):
        toks.append(("↗", "mut"))
    if task.images:
        toks.append(("▤", "mut"))
    if not board.is_done(task):
        age = days_in_phase(task, today)
        if age is not None:
            toks.append((f"·{age}d", "dim"))
    # the link marks go before the project tag (shed first): the high band's
    # tag says whose card it is, an accepted mark (A2 R-1b) — amendment A-3
    toks.extend(_link_tokens(task, board, marks))
    if tag:
        toks.append(tag)
    if task.archived:
        toks.append((ARCHIVED_MARK, "ash"))
    else:
        dtok, dcol = reldue_token(task, today, board, include_done=True)
        if dtok:
            toks.append((dtok, dcol))
    return toks


def kanban_card(task, board, wc, selected, *, today, marks=None,
                tag=None) -> tuple[str, str]:
    """A kanban card as two rows of exactly `wc` cells (LLR-301.2): the title
    across the column on row 1 (after the shipped badge), its rest and the
    meta strip on row 2. Widths are measured on PLAIN text; each title piece is
    escaped after it is cut."""
    if wc <= 0:
        return "", ""
    hue = project_color(board, task)
    spine1 = c("▲", "over") if task.blocked else c("▊", hue)
    if wc == 1:
        return spine1, c("▊", hue)
    badge, bw = "", 0
    if not board.is_done(task) and not task.archived and wc >= 9:
        token, tone = PRIORITY_BADGE.get(task.priority, PRIORITY_BADGE["normal"])
        badge, bw = f"[b reverse {HEX[tone]}]{token}[/] ", 3
    tw = wc - 2 - bw
    head, rest = _wrap_title(task.title, tw)
    tokens = _card_meta(task, board, today, marks, tag)
    keep = tw - (1 + cell_len(tokens[-1][0]) if tokens else 0)
    if rest and keep < 2:
        # no room for the rest beside the last fact: row 1 says the title goes
        # on (`…`) and row 2 keeps the due token (LLR-301.2)
        head, rest = fit(task.title, tw), ""
    row1 = spine1 + " " + badge + _title_piece(task, fit(head, tw), selected)
    if rest:
        if vis(rest) > keep:
            rest = fit(rest, keep)
        room = tw - vis(rest)
        meta, used = _fit_indicators(tokens, room)
        row2 = (c("▊", hue) + " " + " " * bw + _title_piece(task, rest, selected)
                + meta + " " * (room - used))
    else:
        meta, used = _fit_indicators(tokens, wc - 1)
        row2 = c("▊", hue) + meta + " " * (wc - 1 - used)
    return row1, row2


def _project_tags(board) -> dict:
    """{project id: tag}: the shortest run of leading words of the name that no
    other visible project's name starts with (D-307), the whole name if none."""
    names = {p.id: p.name for p in board.visible_projects(True)}
    out = {}
    for pid, name in names.items():
        words = name.split(" ")
        others = [n for q, n in names.items() if q != pid]
        out[pid] = next((" ".join(words[:k]) for k in range(1, len(words))
                         if not any(o.split(" ")[:k] == words[:k] for o in others)),
                        name)
    return out


def _kanban_cell(cards, board, wc, selected_id, today, marks,
                 tags=None) -> list[tuple[str, str | None]]:
    """One band's rows in one column: its cards, one `┈` row between each two."""
    rows: list[tuple[str, str | None]] = []
    for k, t in enumerate(cards):
        if k:
            rows.append((c("┈" * wc, "frame"), None))
        tag = None
        if tags is not None:
            p = board.project_by_id(t.project_id)
            tag = (tags.get(p.id, p.name), p.color) if p else ("Inbox", "dim")
        r1, r2 = kanban_card(t, board, wc, t.id == selected_id, today=today,
                             marks=marks, tag=tag)
        rows += [(r1, t.id), (r2, None)]
    return rows


def _due_fact(d: date, today: date) -> tuple[str, str]:
    n = (d - today).days
    if n < 0:
        return f"{-n}d late", "over"
    if n == 0:
        return "due today", "soon"
    return f"due +{n}d", "soon" if n <= 7 else "dim"


def _band_rule(facts: list[tuple], seps: list[int], w: int) -> str:
    """A band rule (LLR-303.1): `(text, tone[, bold])` facts left to right,
    clipped at `w`, then a `─` rule with `┼` under each column separator past
    the text."""
    out, used = [], 0
    for text, tone, *bold in facts:
        if used >= w:
            break
        text = fit(text, w - used) if vis(text) > w - used else text
        out.append(c(_literal(text), tone, bool(bold) and bold[0]))
        used += vis(text)
    if used < w:
        tail = ["─"] * (w - used - 1)
        for x in seps:
            if 0 <= x - used - 1 < len(tail):
                tail[x - used - 1] = "┼"
        out.append(" " + c("".join(tail), "frame"))
    return "".join(out)


def _band_facts(band: KanbanBand, today: date) -> list[tuple]:
    facts = [("▐ ", band.color), (band.name, band.color, True),
             (f"  {band.n_open} open", "mut")]
    if band.n_high:
        facts.append((f" · {band.n_high} high ↑", "mut"))
    p = band.project
    if p is not None:
        if p.status == "at_risk":
            facts.append((" · at risk", "over"))
        due = parse_iso(p.due_date)
        if due is not None:
            text, tone = _due_fact(due, today)
            facts.append((" · project " + text, tone))
    return facts


def band_milestones(board: Board, project, today: date,
                    show_archived: bool = False) -> list[tuple[str, Task]]:
    """`(kind, task)` for a project's band rule (LLR-603.2, M-2): its visible,
    non-archived, dated milestones — the late ones first (by due), then the
    upcoming ones (by due), then the ONE reached milestone with the latest due."""
    ms = [t for t in board.visible_tasks(show_archived)
          if t.project_id == project.id and t.milestone and not t.archived
          and parse_iso(t.due_date) is not None]
    open_ = sort_by_due([t for t in ms if not board.is_done(t)])
    late = [("late", t) for t in open_ if parse_iso(t.due_date) < today]
    ahead = [("ahead", t) for t in open_ if parse_iso(t.due_date) >= today]
    reached = sort_by_due([t for t in ms if board.is_done(t)])[-1:]
    return late + ahead + [("reached", t) for t in reached]


def band_milestone_facts(items: list[tuple[str, Task]], room: int, color: str,
                         today: date) -> list[tuple]:
    """Lay the band's milestones into `room` cells (LLR-603.2): as many as can keep
    a title of at least 8 cells, the first ones whole first; then dates only; then
    `── +N ◆` for the open ones left out (reached never counted); and when not
    one date fits, `+N ◆` alone if it fits (D-619). Facts for `_band_rule`."""
    def piece(kind, t, tw):
        d = parse_iso(t.due_date)
        n = (d - today).days
        if kind == "late":
            tone, dk, tk, rel, rk = "over", "over", "hd", f" · {-n}d late", "over"
        elif kind == "ahead":
            tone, dk, tk, rk = color, "ink", "hd", "soon" if n == 0 else "mut"
            rel = " · today" if n == 0 else f" · in {n}d"
        else:
            tone, dk, tk, rel, rk = "reached", "reached", "reached", " ✓", "reached"
        out = [("◆ ", tone), (_md(d), dk)]
        if tw:
            out.append((" " + fit(t.title, tw), tk))
        return out + [(rel, rk)]

    def plen(fs):
        return sum(vis(f[0]) for f in fs)

    def lay(n, tws):
        out = []
        for i, ((kind, t), tw) in enumerate(zip(items[:n], tws)):
            out += ([(" ── ", "frame")] if i else []) + piece(kind, t, tw)
        more = sum(1 for kind, _t in items[n:] if kind != "reached")
        return out + ([(f" ── +{more} ◆", "mut")] if more else [])

    for n in range(len(items), 0, -1):
        spare, tws = room - plen(lay(n, [0] * n)), []
        for i, (_kind, t) in enumerate(items[:n]):
            tw = min(vis(t.title), spare - 9 * (n - 1 - i) - 1)
            if tw < 8:
                break
            tws.append(tw)
            spare -= tw + 1
        if len(tws) == n:
            return lay(n, tws)
    for n in range(len(items), 0, -1):
        out = lay(n, [0] * n)
        if plen(out) <= room:
            return out
    more = sum(1 for kind, _t in items if kind != "reached")
    return [(f"+{more} ◆", "mut")] if more and len(f"+{more} ◆") <= room else []


def band_rule_facts(board: Board, band: KanbanBand, today: date, show_archived: bool,
                    w: int) -> tuple[list[tuple], bool]:
    """(facts, carries a ◆) for one band rule — THE seat both the renderer and the
    `?` legend read, so the legend names `◆` exactly when a rule draws one (code
    review K-1, the no-ghost law). Only the project grouping's bands have a project
    (D-607)."""
    facts = _band_facts(band, today)
    if band.project is None:
        return facts, False
    items = band_milestones(board, band.project, today, show_archived)
    room = w - sum(vis(f[0]) for f in facts) - 4 - 2
    more = band_milestone_facts(items, room, band.color, today) if items else []
    if not more:
        return facts, False
    return facts + [(" ── ", "frame")] + more, True


def _rail_cells(band: KanbanBand, plan: KanbanPlan, selected_id, today) -> list[str]:
    """The band's rail cells (LLR-304.1): done titles over `done Nd ago`, the
    rest counted; or the count over the newest one's age."""
    rw, out = plan.rail_w, []
    if not band.done:
        return out
    if not plan.rail_titles:
        age = days_in_phase(band.done[0], today)
        return [c(fit(f"✓{len(band.done)}", rw), "done"),
                c(fit(f"{age}d ago" if age is not None else "", rw), "dim")]
    for t in band.rail:
        age = days_in_phase(t, today)
        out += [c("✓", "done") + " "
                + c(_title_piece(t, fit(t.title, rw - 2), t.id == selected_id), "mut"),
                c(fit(f"  done {age}d ago" if age is not None else "", rw), "dim")]
    if len(band.done) > len(band.rail):
        out.append(c(fit(f"  +{len(band.done) - len(band.rail)} more", rw), "mut"))
    return out


def _kanban_grouped(board, show_archived, selected_id, today, w, height, line_map,
                    *, sort="project", group="project", collapsed=False,
                    focus=None) -> tuple[list[str], int]:
    """(rows, pinned): the readable board — the chrome, the high band, the
    bands windowed around the selection, and the fold row (pinned) when bands
    are folded."""
    plan = kanban_plan(board, show_archived, selected_id, today, w, height, sort=sort,
                       group=group, collapsed=collapsed, focus=focus)
    focused = board.project_by_id(focus) if focus is not None else None
    n_open = len(board.phases) - 1
    marks = link_marks(board)
    sep = c("│", "frame")
    seps, x = [], 0
    for wc in plan.widths:
        x += wc
        seps.append(x)
        x += 1

    right = c(f"{len(plan.tasks)} tasks", "mut")
    mode = c(" · grouped", "mut")
    if sort != "project":        # a non-default mode is NAMED (LLR-003.2) —
        mode += c(f" · sort: {sort}", "mut")     # an unnamed mode is a lie
    if group != "project":
        mode += c(f" · group: {group}", "mut")
    if focused is not None:      # the focus is a mode too: it is NAMED (R-08),
        mode += (c(" · focus: ", "mut")          # with the user's own text
                 + c(escape(focused.name), "mut"))  # escaped like everywhere
    head = [header(c("KANBAN", "bright", bold=True) + mode, right, w, tone="bright")]
    n_done = len(phase_buckets(board, plan.tasks)[-1]) if board.phases else 0
    last = board.phases[-1].upper() if board.phases else ""
    rail_head = c(fit(f"✓ {last} {n_done}" if plan.rail_titles else f"✓{n_done}",
                      plan.rail_w), "done", bold=True)
    head.append(sep.join(_windowed_header(board, plan.start, plan.widths, plan.tasks,
                                          n=n_open))
                + (sep if plan.widths else "") + rail_head)
    head.append(rule_row({x: "┼" for x in seps}, w))
    if not plan.tasks:
        return head + [c(fit("  (no tasks — press 'a' to add one)", w), "dim")], 0

    shown = range(plan.start, plan.start + len(plan.widths))

    def block(cells: list[list], rail: list[str]) -> list[tuple[str, list]]:
        """Rows across the drawn columns and the rail, with the ids each names."""
        n = max([len(col) for col in cells] + [len(rail)])
        rows = []
        for r in range(n):
            parts = [col[r][0] if r < len(col) else " " * wc
                     for col, wc in zip(cells, plan.widths)]
            ids = [col[r][1] for col in cells if r < len(col) and col[r][1]]
            rail_cell = rail[r] if r < len(rail) else " " * plan.rail_w
            rows.append((sep.join(parts) + (sep if parts else "") + rail_cell, ids))
        return rows

    pinned_rows: list[tuple[str, list]] = []
    if any(plan.high):
        tags = _project_tags(board)
        cells = []
        for i, wc in zip(shown, plan.widths):
            col = _kanban_cell(plan.high[i], board, wc, selected_id, today, marks, tags)
            if plan.overflow[i]:
                col.append((c(fit(f"+{plan.overflow[i]} more ↓", wc), "mut"), None))
            cells.append(col)
        drawn = [t for col in plan.high for t in col]
        n_proj = len({t.project_id for t in drawn})
        facts = [("── ", "frame"), ("high", "ink", True),
                 (f"  {len(drawn)} open · {n_proj} project{'s' if n_proj != 1 else ''}",
                  "mut")]
        pinned_rows = [(_band_rule(facts, seps, w), [])] + block(cells, [])
    bands = []
    for band in plan.bands:
        cells = [_kanban_cell(band.cols[i], board, wc, selected_id, today, marks)
                 for i, wc in zip(shown, plan.widths)]
        rail = _rail_cells(band, plan, selected_id, today)
        facts, _ms = band_rule_facts(board, band, today, show_archived, w)
        rows = [(_band_rule(facts, seps, w), [])] + block(cells, rail)
        rail_ids = [t.id for t in band.rail]
        for k, tid in enumerate(rail_ids):        # a rail title names its row
            rows[1 + 2 * k][1].append(tid)
        bands.append(rows)

    keep = list(range(len(bands)))
    room = (height - len(head) - len(pinned_rows) - 1) if height else None
    if room is not None and sum(len(b) for b in bands) > room + 1:
        # LLR-309.1: the earliest start that still draws the selection's band,
        # then the bands below it while they fit — a `down` into a band already
        # on screen moves nothing (P2 UX-14)
        ids = [{t for r in b for t in r[1]} for b in bands]
        s = next((i for i, x in enumerate(ids) if selected_id in x), 0)
        first = s
        while first > 0 and sum(len(b) for b in bands[first - 1:s + 1]) <= room:
            first -= 1
        used, end = sum(len(b) for b in bands[first:s + 1]), s + 1
        while end < len(bands) and used + len(bands[end]) <= room:
            used += len(bands[end])
            end += 1
        keep = list(range(first, end))
    drawn = [r for k in keep for r in bands[k]]
    whole = keep == list(range(len(bands)))     # then the fold row's line is free
    cut = None
    if (room is not None and room >= 3 and len(keep) == 1
            and len(drawn) > room + whole):
        # LLR-309.2: a band taller than the room is cut to it — its rule, then
        # whole cards around the selection (cards sit every 3 rows: the cut
        # starts on a card's first row and ends on a card's second) — and the
        # fold row counts the band's cards cut off (P4 UXV3-1: drawn whole it
        # scrolled the head, the card's row 2 and the fold row out of the panel)
        body = drawn[1:]
        rows = (room - 1) - room % 3            # 3j + 2: j + 1 whole cards
        at = next((i for i, r in enumerate(body) if selected_id in r[1]), 0)
        start = -(-max(0, at + 2 - rows) // 3) * 3
        start = min(start, at)                  # a rail title (every 2 rows) stays drawn
        band = plan.bands[keep[0]]
        cards = {t.id for col in band.cols for t in col}     # open cards, not rail titles
        cut = (band.name,
               len(cards & {t for r in body[:start] for t in r[1]}),
               len(cards & {t for r in body[start + rows:] for t in r[1]}))
        drawn = [drawn[0]] + body[start:start + rows]
    lines = list(head)
    for markup, ids in pinned_rows + drawn:
        lines.append(markup)
        if line_map is not None:
            for tid in ids:
                line_map[tid] = len(lines) - 1
    if keep == list(range(len(bands))) and cut is None:
        return lines, 0
    return lines + [_fold_row(plan.bands, keep, w, cut)], 1


def _fold_row(bands: list, keep: list[int], w: int, cut=None) -> str:
    """`▲ N above: …   ▼ M below: …` (LLR-309.1), and for a band cut to the
    room `▲ k more in NAME` / `▼ m more in NAME` between them (LLR-309.2). Every
    count always prints: when the row does not fit, the `▲` names go first (P2
    UX-15), then the cut band's name, and only then is the `▼` list clipped."""
    names = [f"{b.name} ({b.n_open} open)" for b in bands]
    above, below = names[:keep[0]], names[keep[-1] + 1:]
    up = f"▲ {len(above)} above" if above else ""
    down = f"▼ {len(below)} below" if below else ""
    inside = []
    if cut is not None:
        name, k, m = cut
        inside = [x for x in (f"▲ {k} more in {name}" if k else "",
                              f"▼ {m} more in {name}" if m else "") if x]
    tail = [down + (": " + ", ".join(below) if below else "")]
    full = "   ".join(x for x in [up + (": " + ", ".join(above) if above else "")] + inside
                      + tail if x)
    if vis(full) > w and (up or inside) and (inside or down):
        # the `▲` side keeps only its count; the `▼` side is clipped after its
        # own, as the approved 80×24 frame shows it
        full = "   ".join(x for x in [up] + inside + tail if x)
    if inside and vis("   ".join(x for x in [up] + inside + [down] if x)) > w:
        # even the bare counts overflow: the cut band's rule is on screen, so
        # its counts drop its name
        short = [x.split(" in ")[0] for x in inside]
        full = "   ".join(x for x in [up] + short + tail if x)
    return c(_literal(fit(full, w)), "mut")


def _matrix_junctions(label_w: int, widths: list[int], mid: str) -> dict[int, str]:
    j, pos = {}, label_w
    j[pos] = mid
    pos += 1
    for wc in widths:
        pos += wc
        j[pos] = mid
        pos += 1
    return j


def _kanban_matrix(board, show_archived, selected_id, today, w, height, line_map) -> list[str]:
    inner = w
    tasks = kanban_work(board.visible_tasks(show_archived))
    label_w = max(6, min(14, inner // 5))
    prog_w = 5
    selected = board.task_by_id(selected_id)
    start, widths = _phase_window(board, inner - label_w - prog_w - 2, selected)
    sep = c("│", "frame")

    right = c(f"{len(tasks)} tasks", "mut")
    lines = [header(c("KANBAN", "bright", bold=True) + c(" · matrix", "mut"), right, w,
                     tone="bright")]
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
                          + c(fit(pct, prog_w, "right"), "hd" if pid else "dim")))
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
    if sort == "unblock":
        counts = {t.id: unblocks_count(board, t)
                  for t in board.tasks
                  if not board.is_done(t) and not t.archived}
        return sorted(tasks, key=lambda t: (
            t.blocked, -counts.get(t.id, 0)))
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
    tasks = kanban_work(board.visible_tasks(show_archived))
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
    # the link marks are a board-wide fact: compute once, use everywhere.
    marks = link_marks(board)

    right = c(f"{len(tasks)} tasks", "mut")
    mode = c(" · lanes", "mut")
    if group != "project":
        mode += c(f" · group: {group}", "mut")
    if sort != "project":
        mode += c(f" · sort: {sort}", "mut")
    if focused is not None:
        mode += (c(" · focus: ", "mut")
                 + c(escape(focused.name), "mut"))
    lines = [header(c("KANBAN", "bright", bold=True) + mode, right, w, tone="bright")]
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
                           today=today,
                           marks=marks, badge=True,
                           title_floor=CARD_TITLE_FLOOR), t.id)
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
        lines, pinned = _kanban_grouped(board, show_archived, selected_id, today, w,
                                        height, line_map, sort=sort, group=group,
                                        collapsed=collapsed, focus=focus)
        return to_text(lines, height, w, pinned)
    return to_text(lines, height, w)


# ---------------------------------------------------------------------------
# view: CHAIN MAP (the C-2b oracle, batch 2026-10-07-batch-02)
#
# The dependency web as a grid: one band per project that has links, tiles laid
# left to right by dependency depth, edges routed in the gaps (a depth +2 skip
# rides its own lane under the band). The critical chain is STRUCTURE — heavy
# `━`/`┃` and bold — never hue. The per-project dates switch reads `date_links`
# through the shipped lenient read (absent or junk resolves to the default) and
# paints the LABELS, never the stored strings.
# ---------------------------------------------------------------------------
# the labels↔stored map (the contract's): stay↔flag / push↔push_delta /
# together↔together. The STORED strings never paint.
CHAINMAP_SHORT = {"flag": "stay", "push_delta": "push", "together": "together"}
CHAINMAP_LABELS = {"flag": "Keep others, flag conflicts",
                   "push_delta": "Push what it collides with",
                   "together": "Move the whole chain"}
CHAINMAP_WHY = {"flag": "only the moved task moves; overlaps are flagged",
                "push_delta": "a move pushes waiting tasks by the overlap it adds",
                "together": "a move shifts every later task by the same days"}
CHAINMAP_WHY_SHORT = {"flag": "nothing else moves; overlaps flagged",
                      "push_delta": "waiters move by the overlap this adds",
                      "together": "all downstream shifts the same days"}

# the chain map's selection follows the app-wide budget: bright, never accent.

# box-drawing connectors with per-direction weight (light ─ / heavy ━), derived
# from Unicode names — the same table the C-2b prototype built.
_CH_U, _CH_D, _CH_L, _CH_R = 1, 2, 4, 8
_CH_DIR = {"UP": (_CH_U,), "DOWN": (_CH_D,), "LEFT": (_CH_L,), "RIGHT": (_CH_R,),
           "HORIZONTAL": (_CH_L, _CH_R), "VERTICAL": (_CH_U, _CH_D)}


def _chainmap_box_table():
    out = {}
    for cp in range(0x2500, 0x2580):
        words = unicodedata.name(chr(cp), "").replace("BOX DRAWINGS ", "").split()
        if not words or set(words) & {"DOUBLE", "DASH", "TRIPLE", "QUADRUPLE",
                                      "ARC", "DIAGONAL", "SINGLE"}:
            continue
        w: dict[int, bool] = {}
        if words[0] in ("LIGHT", "HEAVY"):
            for x in words[1:]:
                for d in _CH_DIR.get(x, ()):
                    w[d] = words[0] == "HEAVY"
        else:
            pend: list[int] = []
            for x in words:
                if x in _CH_DIR:
                    pend += _CH_DIR[x]
                elif x in ("LIGHT", "HEAVY"):
                    for d in pend:
                        w[d] = x == "HEAVY"
                    pend = []
        if w:
            out.setdefault(frozenset(w.items()), chr(cp))
    for bits, ch in {_CH_D | _CH_L: "╮", _CH_D | _CH_R: "╭",
                     _CH_U | _CH_L: "╯", _CH_U | _CH_R: "╰"}.items():
        out[frozenset((d, False) for d in (_CH_U, _CH_D, _CH_L, _CH_R) if bits & d)] = ch
    return out


_CHAINMAP_BOX = _chainmap_box_table()


def _chainmap_box(bits: int, heavy: int) -> str:
    if bits in (_CH_L, _CH_R):
        bits, heavy = _CH_L | _CH_R, (_CH_L | _CH_R) if heavy else 0
    if bits in (_CH_U, _CH_D):
        bits, heavy = _CH_U | _CH_D, (_CH_U | _CH_D) if heavy else 0
    key = frozenset((d, bool(heavy & d)) for d in (_CH_U, _CH_D, _CH_L, _CH_R) if bits & d)
    return _CHAINMAP_BOX.get(key) or _CHAINMAP_BOX[frozenset(
        (d, bool(heavy)) for d in (_CH_U, _CH_D, _CH_L, _CH_R) if bits & d)]


def _chainmap_st(text: str, fg: str, bg: str | None = None, bold: bool = False) -> str:
    """Markup with an explicit hex fg (and bg); `text` must be plain, unescaped."""
    return f"[{'bold ' if bold else ''}{fg}{' on ' + bg if bg else ''}]{escape(text)}[/]"


def _chainmap_pad(markup: str, width: int) -> str:
    """Pad `markup` out to `width` cells, measured by its RENDERED width — an
    escaped `[` is one cell here, where `_strip` would read it as a tag (S1)."""
    return markup + " " * max(0, width - Text.from_markup(markup, emoji=False).cell_len)


def _chainmap_mode(pr) -> str:
    """The band's rule, read leniently: absent or junk resolves to the default."""
    v = pr.extra.get("date_links") if pr is not None else None
    return v if v in CASCADE_MODES else CASCADE_DEFAULT_MODE


def _chainmap_conflict_days(board: Board, waiter: Task, pred: Task, today: date) -> int:
    """Days the waiter starts (or today, if undated) before `pred` is due — the
    prototype's plain `(pred.due − start).days`, not `link_overlap`'s +1."""
    s = parse_iso(waiter.start_date) or today
    d = parse_iso(pred.due_date)
    return (d - s).days if d and d > s else 0


def _chainmap_depths(board: Board, tasks: list[Task]) -> dict[str, int]:
    """Longest path from a task with no (in-band) predecessor; a stored cycle is
    cut by the `seen` set so the render always terminates."""
    ids = {t.id for t in tasks}
    memo: dict[str, int] = {}

    def depth(t: Task, seen=()) -> int:
        if t.id in memo:
            return memo[t.id]
        ps = [p for x in t.depends_on if x in ids and x not in seen
              and (p := board.task_by_id(x))]
        memo[t.id] = 0 if not ps else 1 + max(depth(p, seen + (t.id,)) for p in ps)
        return memo[t.id]
    for t in tasks:
        depth(t)
    return memo


def _chainmap_plan(board: Board, show_archived: bool):
    """(tasks, linked, depth, chain, ncol, bands, bare) — the one answer the
    renderer and the navigator share, so a cursor can never rest on a tile the
    view does not draw (the F-3 law)."""
    tasks = list(board.visible_tasks(show_archived))
    tid = {t.id for t in tasks}
    linked = [t for t in tasks if any(x in tid for x in t.depends_on)
              or any(t.id in o.depends_on for o in tasks)]
    depth = _chainmap_depths(board, linked)
    chain = set(critical_chain(board))
    ncol = max(depth.values()) + 1 if depth else 1
    # CM-1: cap the columns so the tile width can never crash the wrapper (the
    # 24-column floor gives tile_w >= 3 -> inner >= 1); the oracle frames use
    # ncol 4, so the cap never moves them. Deeper chains pile into the last
    # column instead of raising.
    ncol = min(ncol, 4)
    depth = {tid: min(d, ncol - 1) for tid, d in depth.items()}
    projects = board.visible_projects(show_archived)
    bands = [(pr, [t for t in linked if t.project_id == pr.id]) for pr in projects]
    bands = [(pr, ts) for pr, ts in bands if ts]
    bare = [pr for pr in projects if not any(t.project_id == pr.id for t in linked)]
    return tasks, linked, depth, chain, ncol, bands, bare


def _chainmap_switch(mode: str, wide: bool, custom: bool) -> str:
    """The per-band `dates` switch: `○`/`●` per mode, `set here` when custom."""
    parts = []
    for m in CASCADE_MODES:
        on = m == mode
        parts.append(c("●" if on else "○", "bright" if on else "dim")
                     + (" " if wide else "")
                     + c(CHAINMAP_SHORT[m], "bright" if on else "dim", bold=on))
    lead = (c("set here  ", "hd") if custom else "") + (c("dates  ", "mut") if wide else "")
    return lead + ("  " if wide else " ").join(parts)


def _chainmap_band_rule(pr, facts: list[str], switch: str, width: int) -> str:
    """`─▌Name  facts ─────── switch ─` (exactly `width` cells); the rule wears
    the project's hue shaded 50%, the name the project hue; facts shed from the
    right while the row is too wide."""
    rc = _shade_hex(HEX[pr.color], 0.5)
    head = _chainmap_st("─", rc) + c("▌", pr.color) + c(escape(pr.name), pr.color, bold=True)
    sw_w = vis(_strip(switch))
    facts = list(facts)
    while True:
        f = (c("  ", "dim") + c(" · ", "dim").join(facts)) if facts else ""
        used = vis(_strip(head + f)) + 1 + (1 + sw_w + 1 if switch else 0) + 1
        if used + 2 <= width or not facts:
            break
        facts.pop()
    fill = width - used
    return head + f + " " + _chainmap_st("─" * max(1, fill), rc) \
        + ((" " + switch + " ") if switch else "") + _chainmap_st("─", rc)


def _chainmap_keys(items) -> str:
    """Key hints out of the accent: bold bright keys, muted verbs."""
    return c(" · ", "dim").join(c(k, "bright", bold=True) + (" " + c(v, "mut") if v else "")
                                for k, v in items)


def _chainmap_edge_style(k: str) -> str:
    return {"crit": f"bold {HEX['bright']}", "over": HEX["over"],
            "ash": HEX["ash"]}.get(k, HEX["mut"])


def _chainmap_legend(width: int, items) -> str:
    """The legend row, shedding entries from the right until it fits."""
    while items:
        out = " " + c(" · ", "dim").join(c(g, k) + " " + c(escape(t), "dim") for g, k, t in items)
        if vis(_strip(out)) <= width:
            return _pad(out, width)
        items = items[:-1]
    return " " * width


class _ChainmapCanvas:
    """Cells of (glyph, style); rows are joined into runs at the end."""

    def __init__(self, w: int, h: int):
        self.w, self.h = w, h
        self.g = [[(" ", "")] * w for _ in range(h)]

    def put(self, r: int, x: int, s: str, style: str) -> None:
        for i, ch in enumerate(s):
            if 0 <= r < self.h and 0 <= x + i < self.w:
                self.g[r][x + i] = (ch, style)

    def line(self, r: int) -> str:
        out, run, st = [], "", None
        for ch, s in self.g[r] + [("", "END")]:
            if s != st:
                if run:
                    out.append(f"[{st}]{escape(run)}[/]" if st else escape(run))
                run, st = "", s
            run += ch
        return "".join(out)


class _ChainmapWires:
    """Connector bits + heavy bits per cell; the highest-ranked tone colours it."""
    RANK = {"crit": 3, "over": 2, "mut": 1, "ash": 0}

    def __init__(self):
        self.bits: dict[tuple[int, int], int] = {}
        self.heavy: dict[tuple[int, int], int] = {}
        self.tone: dict[tuple[int, int], str] = {}

    def set(self, r, x, bit, k, heavy=None):
        self.bits[(r, x)] = self.bits.get((r, x), 0) | bit
        if heavy if heavy is not None else k == "crit":
            self.heavy[(r, x)] = self.heavy.get((r, x), 0) | bit
        if (r, x) not in self.tone or self.RANK[k] >= self.RANK[self.tone[(r, x)]]:
            self.tone[(r, x)] = k

    def hseg(self, r, x0, x1, k, heavy=None):
        a, z = sorted((x0, x1))
        for x in range(a, z + 1):
            self.set(r, x, (_CH_L if x > a else 0) | (_CH_R if x < z else 0), k, heavy)

    def vseg(self, x, r0, r1, k, heavy=None):
        a, z = sorted((r0, r1))
        for r in range(a, z + 1):
            self.set(r, x, (_CH_U if r > a else 0) | (_CH_D if r < z else 0), k, heavy)

    def path(self, pts, k, heavy=None):
        for (x0, r0), (x1, r1) in zip(pts, pts[1:]):
            if r0 == r1:
                self.hseg(r0, x0, x1, k, heavy)
            else:
                self.vseg(x0, r0, r1, k, heavy)

    def draw(self, cv: _ChainmapCanvas) -> None:
        for (r, x), bt in self.bits.items():
            k = self.tone[(r, x)]
            cv.put(r, x, _chainmap_box(bt, self.heavy.get((r, x), 0)), _chainmap_edge_style(k))


def _chainmap_tile(cv: _ChainmapCanvas, board: Board, t: Task, rr: int, x: int,
                   tile_w: int, is_sel: bool, is_crit: bool, today: date,
                   wide: bool) -> bool:
    """D-C's two-row tile, inked by the C-2b budget. Returns is_sel."""
    is_done = board.is_done(t)
    d = parse_iso(t.due_date)
    late = d and d < today and not is_done
    pre = open_predecessors(board, t)
    ready = not is_done and t.depends_on and not pre
    bad = any(_chainmap_conflict_days(board, t, q, today) for q in pre)
    inner = tile_w - 2
    words = textwrap.wrap(t.title, inner) or [""]
    l1, rest = fit(words[0], inner), " ".join(words[1:])
    if is_done:
        mk, mk_k = "✓", "ash"
    elif pre:
        mk, mk_k = f"◂{len(pre)}", "over" if bad else "hd"
    elif ready:
        mk, mk_k = ("▷ ready" if wide else "▷"), "done"
    else:
        mk, mk_k = "○", "mut"
    meta, meta_k = ("", "ash") if is_done else (f"▲{(today - d).days}d", "over") if late \
        else ((_md(d), "mut") if d else ("", "mut"))
    if rest and vis(rest) > inner - vis(mk) - vis(meta) - 2 and not late:
        meta = ""
    mid_w = inner - vis(mk) - vis(meta) - 2
    l2_mid = fit(rest, max(0, mid_w)) if rest and mid_w > 3 else " " * max(0, mid_w)
    crit = is_crit and not is_done
    if is_done:
        bg, fg = "", HEX["ash"]
    elif is_sel:
        # the app-wide budget: accent is the today's-rule/studs/cursor seat --
        # the selection is bright+bold like every other view (AT-201)
        bg, fg = f" on {HEX['frame']}", HEX["bright"]
    else:
        bg, fg = f" on {HEX['frame']}", HEX["over"] if late else HEX["bright"] if crit else HEX["hd"]
    bold = "bold " if (is_sel or crit) and not is_done else ""
    cv.put(rr, x, " " + l1 + " ", f"{bold}{fg}{bg}")
    cv.put(rr + 1, x, " ", f"{fg}{bg}".strip() if bg else "")
    cv.put(rr + 1, x + 1, mk, f"{HEX['bright'] if is_sel else HEX[mk_k]}{bg}")
    cv.put(rr + 1, x + 1 + vis(mk), " " + l2_mid + " ", f"{fg}{bg}")
    cv.put(rr + 1, x + 1 + vis(mk) + 1 + vis(l2_mid) + 1, meta + " ",
           f"{HEX['bright'] if is_sel else HEX[meta_k]}{bg}")
    if crit:                                     # the structural critical mark: a heavy left edge
        for r in (rr, rr + 1):
            cv.put(r, x, "┃", f"bold {HEX['bright']}{bg}")
    return is_sel


def render_chainmap(board, show_archived, selected_id, today=None,
                    width=68, height=0, line_map=None) -> Text:
    """The chain map (the C-2b oracle): who waits on whom, per project, with the
    per-band dates switch and the heavy critical chain, fitting the screen at
    118x30 and 80x24."""
    today = today or date.today()
    w = _clamp_width(width)
    if line_map is not None:
        line_map.clear()          # CM-2: the drawn set is rebuilt every render
    tasks, linked, depth, chain, ncol, bands, bare = _chainmap_plan(board, show_archived)
    sel = board.task_by_id(selected_id)
    if sel is None or sel not in linked:
        sel = linked[0] if linked else None
    wide = w >= 100
    gap = 5 if wide else 3
    tile_w = (w - 2 - gap * (ncol - 1)) // ncol
    col_x = [1 + d * (tile_w + gap) for d in range(ncol)]

    plans = []
    for pr, ts in bands:
        slot: dict[str, int] = {}
        used: dict[int, set] = {}
        for d in range(ncol):
            for t in (t for t in ts if depth[t.id] == d):
                pre = [slot[x] for x in t.depends_on if x in slot]
                s = sorted(pre)[len(pre) // 2] if pre else 0
                while s in used.setdefault(d, set()):
                    s += 1
                used[d].add(s)
                slot[t.id] = s
        edges = [(board.task_by_id(x), t) for t in ts for x in t.depends_on if x in slot]
        skips = [e for e in edges if depth[e[1].id] - depth[e[0].id] > 1]
        nslot = max(slot.values()) + 1 if slot else 1
        plans.append(dict(pr=pr, ts=ts, slot=slot, edges=edges, skips=skips,
                          tiles_h=3 * nslot - 1 + len(skips)))

    # vertical rhythm: ONE padding pair for every band, the most that fits
    foot = 3
    body_h = height - 1 - foot - 1      # header + footer(3) + mode footer(1)
    core = sum(1 + p["tiles_h"] for p in plans) + (1 if bare else 0)
    pad = leg = None
    for want_leg in (True, False):
        for pa, pb in ((1, 1), (0, 1), (0, 0)):
            if core + len(plans) * (pa + pb) + want_leg <= body_h:
                pad, leg = (pa, pb), want_leg
                break
        if pad:
            break
    pad = pad or (0, 0)

    def edge_tone(p, t):
        if board.is_done(p):
            return "ash"
        if _chainmap_conflict_days(board, t, p, today):
            return "over"
        return "crit" if (p.id in chain and t.id in chain and not board.is_done(p)) else "mut"

    def is_crit(p, t):
        return p.id in chain and t.id in chain and not board.is_done(p)

    body: list[str] = []
    for p in plans:
        seg_h = 1 + pad[0] + p["tiles_h"] + pad[1]
        if len(body) + seg_h > body_h:
            break                 # CM-2: whole-band fold — the head never dangles
        pr, ts = p["pr"], p["ts"]
        own = [t for t in tasks if t.project_id == pr.id]
        n_un = sum(1 for t in own if t not in ts and not board.is_done(t))
        facts = [c(f"{len(ts)} linked", "dim")] + ([c(f"{n_un} open not linked", "dim")] if n_un else [])
        if any(t.id in chain for t in ts):
            facts.insert(1, _chainmap_st("━", HEX["bright"], None, True) + c(" critical chain", "hd"))
        mode = _chainmap_mode(pr)
        body.append(_chainmap_band_rule(pr, facts, _chainmap_switch(mode, wide,
                                                                    mode != CASCADE_DEFAULT_MODE), w))
        body += [" " * w] * pad[0]
        cv = _ChainmapCanvas(w, p["tiles_h"])
        wires = _ChainmapWires()
        arrows: dict[tuple[int, int], str] = {}
        lane0 = 3 * (max(p["slot"].values()) + 1) - 1
        for pt, t in p["edges"]:
            k = edge_tone(pt, t)
            x_s, x_t = col_x[depth[pt.id]] + tile_w, col_x[depth[t.id]] - 1
            r1, r2 = 3 * p["slot"][pt.id], 3 * p["slot"][t.id]
            if (pt, t) in p["skips"]:
                lane = lane0 + p["skips"].index((pt, t))
                m1, m2 = x_s + gap // 2, col_x[depth[t.id]] - 1 - gap // 2
                wires.path([(x_s, r1), (m1, r1), (m1, lane), (m2, lane), (m2, r2), (x_t, r2)],
                           k, is_crit(pt, t))
            else:
                m = x_s + gap // 2
                wires.path([(x_s, r1), (m, r1), (m, r2), (x_t, r2)], k, is_crit(pt, t))
            arrows[(r2, x_t)] = k
        wires.draw(cv)
        for (rr, x), k in arrows.items():
            cv.put(rr, x, "▸", _chainmap_edge_style(k))
        top = 1 + len(body)
        for t in ts:
            rr, x = 3 * p["slot"][t.id], col_x[depth[t.id]]
            _chainmap_tile(cv, board, t, rr, x, tile_w, t.id == (sel.id if sel else None),
                           t.id in chain, today, wide)
            if line_map is not None:
                line_map[t.id] = top + rr
        body += [cv.line(r) for r in range(cv.h)]
        body += [" " * w] * pad[1]
    if bare:
        for pr in bare:
            n = sum(1 for t in tasks if t.project_id == pr.id and not board.is_done(t))
            body.append(_chainmap_band_rule(pr, [c(f"{n} open", "dim"), c("no links", "dim")], "", w))
    body = body[:body_h]
    body += [" " * w] * (body_h - len(body))
    if leg:
        body[-1] = _chainmap_legend(w, [("✓", "ash", "done"), ("▷", "done", "ready"),
                                        ("◂N", "hd", "waits on N"),
                                        ("━", "bright", "critical chain"),
                                        ("─", "over", "starts before due"),
                                        ("─", "ash", "satisfied"), ("▲", "over", "late")])

    # footer: the selected task's links (both directions), keys out of accent
    if sel is not None:
        pre_all = [board.task_by_id(x) for x in sel.depends_on if board.task_by_id(x)]
        succ = [t for t in tasks if sel.id in t.depends_on]
    else:
        pre_all, succ = [], []

    def ref(t, focus=False, waiter=None):
        w_, p_ = (sel, t) if waiter is None else (waiter, sel)
        g = _chainmap_conflict_days(board, w_, p_, today)
        k = "ash" if board.is_done(t) else "over" if g else "ink"
        s = clip(t.title, 24 if wide else 16)
        extra = c(f" (starts {g}d early)", "over") if g else (c(" ✓", "ash") if board.is_done(t) else "")
        return (c("›", "bright", bold=True) if focus else " ") + c(escape(s), k, bold=focus) + extra

    ft1 = c(" ◂ waits on  ", "mut") + (c(" · ", "dim").join(ref(t, i == 0) for i, t in enumerate(pre_all))
                                       if pre_all else c("nothing", "dim"))
    ft2 = c(" ▸ unblocks  ", "mut") + (c(" · ", "dim").join(ref(t, waiter=t) for t in succ)
                                       if succ else c("nothing waits on it", "dim"))
    keys = [("x", "remove the › link"), ("L", "link"), ("↵", "open"), ("←→↑↓", "move")] if wide \
        else [("x", "remove ›"), ("L", "link"), ("↵", "open")]
    kb = _chainmap_keys(keys)
    kb_raw = " · ".join((f"{k} {v}" if v else k) for k, v in keys)
    seltitle_raw = clip(sel.title, 30 if wide else 22) if sel else ""
    seltxt = c(" " + escape(seltitle_raw), "bright", bold=True) if sel else ""
    # measured RAW, so a hostile title's `[` never inflates the gap (S1)
    gap = max(1, w - (1 + vis(seltitle_raw) if sel else 0) - vis(kb_raw) - 1)
    ft3 = seltxt + " " * gap + kb + " "

    def _foot_row(ln: str) -> str:
        if Text.from_markup(ln, emoji=False).cell_len <= w:
            return _chainmap_pad(ln, w)
        return c(fit(_strip(ln), w), "mut")

    footer = [_foot_row(ln) for ln in (ft3, ft1, ft2)]

    n_late = sum(1 for t in linked if (d := parse_iso(t.due_date)) and d < today and not board.is_done(t))
    title = c("◆ CHAIN MAP", "bright", bold=True) + c(" · who waits on whom", "mut")
    n_drawn = sum(len(ts) for _pr, ts in bands)
    right = (c(f"{n_drawn} linked tasks", "mut") + c(" · ", "dim") + c(f"▲{n_late} late", "over")
             + c(" · ", "dim") + _chainmap_st("━", HEX["bright"], None, True)
             + c(f" chain {len(chain)}", "hd"))
    lines = ([header(title, right, w)]
             + [_chainmap_pad(x, w) for x in body]
             + [_chainmap_pad(x, w) for x in footer])

    # the mode footer: the selected chain's rule (LONG labels + explainers)
    if sel is not None and (pr := board.project_by_id(sel.project_id)) is not None:
        mode = _chainmap_mode(pr)
        src = "set here" if mode != CASCADE_DEFAULT_MODE else "default"
        if wide:
            foot = (c(" ▌", pr.color) + c(f"{escape(pr.name)} · ", "mut")
                    + c(CHAINMAP_LABELS[mode], "bright", bold=True) + c(f" ({src}): ", "dim")
                    + c(CHAINMAP_WHY[mode], "ink") + c(" · ", "dim") + _chainmap_keys([("m", "change")]))
        else:
            foot = (c(" ▌", pr.color) + c(CHAINMAP_SHORT[mode], "bright", bold=True) + c(": ", "dim")
                    + c(CHAINMAP_WHY_SHORT[mode], "ink") + c(" · ", "dim")
                    + _chainmap_keys([("m", "change for this chain")]))
        if Text.from_markup(foot, emoji=False).cell_len > w:
            foot = c(fit(_strip(foot), w), "mut")
        lines.append(_chainmap_pad(foot, w))
    else:
        lines.append(" " * w)

    return to_text(lines, height, w)


def _chainmap_nav(board: Board, show_archived: bool) -> list[list[str]]:
    """The chain map's on-screen order: one column per depth, tasks top-to-bottom
    (band order, then draw order) — left/right walks the chain, up/down a column."""
    _tasks, linked, depth, _chain, ncol, bands, _bare = _chainmap_plan(board, show_archived)
    cols: list[list[str]] = [[] for _ in range(ncol)]
    for _pr, ts in bands:
        for t in ts:
            cols[depth[t.id]].append(t.id)
    return cols


# ---------------------------------------------------------------------------
# presentation (PRES-C): the hybrid — gantt field on top, brief blocks below
# ---------------------------------------------------------------------------
# `R` opens the presentation of the selected task's project (the focused project
# when set). It is read-only: it draws the project, it never writes the board.
# The layout is byte-faithful to the PRES-C oracle frames (prototypes/present_e),
# which is why the composition here matches the prototype's renderer exactly: the
# same label/chip/field split, the same `⟦━⟧` cursor, the same budget (accent =
# the cursor only; today = bright). S1: every untrusted string is escaped and
# clipped before it enters markup; every row is exactly `width` cells.

class _PresentGeo(NamedTuple):
    width: int
    label_w: int
    chip_w: int
    field_w: int
    ax: GanttAxis
    chain: set
    today: date
    wide: bool
    hue: str


def present_project_id(board: Board, selected_id: str | None,
                       focused_id: str | None) -> str | None:
    """The project the presentation shows: the selected task's project, else the
    focused one, else the first visible project. None only when the board has no
    visible project at all."""
    task = board.task_by_id(selected_id)
    if task is not None and task.project_id is not None:
        return task.project_id
    if focused_id is not None:
        return focused_id
    projects = board.visible_projects(False)
    return projects[0].id if projects else None


def present_tasks(board: Board, project_id: str | None) -> tuple[list[Task], list[Task]]:
    """(open tasks by due, all tasks) of one project in gantt order — the same
    split the gantt lists: work still open first, finished work at the tail."""
    tasks = gantt_tasks(board, board.visible_tasks(False), project_id)
    return [t for t in tasks if not board.is_done(t)], tasks


def _present_cols(width: int, wide: bool) -> tuple[int, int, int]:
    """label + gutter + field + space + chip == width (room-sized chips)."""
    label_w = 32 if wide else 22
    chip_w = 11 if wide else 9
    field_w = width - label_w - 1 - 1 - chip_w
    return label_w, chip_w, field_w


def _present_axis(board: Board, proj: Project, open_t: list[Task],
                  field_w: int, today: date) -> GanttAxis:
    dues = [d for t in open_t if (d := parse_iso(t.due_date))]
    starts = [d for t in open_t if (d := parse_iso(t.start_date))]
    pdue = parse_iso(proj.due_date)
    margin = timedelta(days=2)
    lo = min(dues + [today]) - margin
    hi = max(dues + ([pdue] if pdue else []) + [today]) + margin
    ctx = min(starts + [lo])
    return gantt_axis(field_w, today, lo, hi, ctx)


def _present_field(cells: list[tuple[str, str]], ax: GanttAxis) -> str:
    """Cells to markup over the field's own ground. The ONE change from the
    shipped `_gantt_field`: the today rule is `bright` bold, NOT accent — the
    C-2b budget reserves accent for the cursor alone."""
    guides = ax.guides()
    out = []
    for x, (glyph, tone) in enumerate(cells):
        if tone == "gap":
            m = c(" ", "dim")
        elif glyph != " ":
            m = c(glyph, "bright", bold=True) if tone in ("crit", "accent") else c(glyph, tone)
        elif x == ax.tc:
            m = c(RULE, "bright", bold=True)
        else:
            m = c(FIELD_WEEK if x in guides else LATTICE, "ash" if x < ax.tc else "dim")
        out.append(m)
    return "".join(out)


def _present_chip(due_iso: str | None, today: date, width: int, wide: bool) -> str:
    """A room-sized due chip: the date AND the distance (`Oct 10 +10d`)."""
    d = parse_iso(due_iso)
    if width <= 0:
        return ""
    if d is None:
        lab, tone = "no due", "dim"
    elif d < today:
        n = (today - d).days
        lab, tone = (f"{_md(d)} ▲{n}d" if wide else f"▲{n}d"), "over"
    elif d == today:
        lab, tone = "due today", "soon"
    else:
        n = (d - today).days
        lab, tone = (f"{_md(d)} +{n}d" if wide else _md(d)), "mut"
    return c(fit(lab, width, "right"), tone)


def _present_due(d: date | None, today: date) -> tuple[str, str]:
    if d is None:
        return "no due", "dim"
    n = (d - today).days
    if n < 0:
        return f"▲{-n}d", "over"
    if n == 0:
        return "today", "soon"
    return f"in {n}d", "mut"


def _present_title(task: Task, width: int) -> str:
    return c(title_markup(task, max(0, width), False), "bright", bold=True)


def _present_note_lines(notes: str, note_w: int, max_lines: int) -> list[str]:
    notes = (notes or "").strip()
    if not notes:
        return []
    wrapped = textwrap.wrap(notes, note_w) or [""]
    if len(wrapped) > max_lines:
        wrapped = wrapped[:max_lines]
        wrapped[-1] = clip(wrapped[-1], note_w - 1) + "…"
    return wrapped


def _present_note_row(line: str, width: int, note_w: int) -> str:
    body = c("· ", "dim") + c(escape(clip(line, note_w)), "mut")
    return _pad("  " + body, width)


def _present_span_row(proj: Project, board: Board, p: _PresentGeo) -> str:
    progress = board.project_progress(proj.id)
    cells = _gantt_span(proj, p.ax, progress, 0)
    label = c("▌ ", p.hue) + c(escape(fit(proj.name.upper(), p.label_w - 2)), p.hue, bold=True)
    chip = " " + _present_chip(proj.due_date, p.today, p.chip_w, p.wide)
    return _pad(label + " " + _present_field(cells, p.ax) + chip, p.width)


def _present_task_row(task: Task, board: Board, p: _PresentGeo, cursor: bool = False) -> str:
    cells = _gantt_bar(task, board, p.ax, p.chain, 0)
    if cursor:
        lo = next((x for x, (g, _) in enumerate(cells) if g != " "), None)
        hi = next((x for x in range(len(cells) - 1, -1, -1) if cells[x][0] != " "), None)
        if lo is not None and hi is not None:
            for x in range(lo, hi + 1):          # the echo `⟦━⟧`: heavy fill in focus
                cells[x] = ("━", "accent")
            cells[lo] = ("⟦", "accent")
            cells[hi] = ("⟧", "accent")
    label = "  " + c("▎", p.hue) + " " + _present_title(task, p.label_w - 4)
    gut = gantt_dep_mark(task, board, p.chain)
    chip = " " + _present_chip(task.due_date, p.today, p.chip_w, p.wide)
    return _pad(label + gut + _present_field(cells, p.ax) + chip, p.width)


def _present_brief(task: Task, p: _PresentGeo, cursor: bool, width: int) -> str:
    d = parse_iso(task.due_date)
    due_label, due_tone = _present_due(d, p.today)
    due_w = 11 if p.wide else 9
    due = c(fit(due_label, due_w, "right"), due_tone)
    max_title = width - 6 - due_w
    tone = "accent" if cursor else "bright"
    txt = clip(task.title, max_title)
    gap = max_title - vis(txt)
    open_, close = (c("⟦", "accent", bold=True), c("⟧", "accent", bold=True)) if cursor else (" ", " ")
    return _pad("  " + open_ + c(escape(txt), tone, bold=True) + close + " " * gap
                + "  " + due, width)


def _present_counts(open_t: list[Task], tasks: list[Task], today: date) -> tuple[int, int, int]:
    late = sum(1 for t in open_t if (d := parse_iso(t.due_date)) and d < today)
    return late, len(open_t), len(tasks) - len(open_t)


def _present_finish(lines: list[str], height: int, width: int) -> Text:
    if len(lines) > height:
        over = len(lines) - height
        lines = lines[:height - 1]
        lines.append(_pad(c(escape(fit(f"  +{over} more rows not shown", width)), "dim"), width))
    lines = list(lines)
    if len(lines) < height:
        lines += [" " * width] * (height - len(lines))
    for ln in lines:
        assert vis(_strip(ln)) == width, (vis(_strip(ln)), width, _strip(ln))
    return to_text(lines, height, width)


def render_present(board: Board, project_id: str | None, cursor_id: str | None,
                   today: date, width: int, height: int) -> Text:
    """The PRES-C presentation frame: the project's gantt field on top, the brief
    one-liners below, a `⟦━⟧` cursor across the brief blocks (its task's notes
    expand). Byte-faithful to the PRES-C oracle at 118x30 and 80x24."""
    proj = board.project_by_id(project_id)
    if proj is None:
        projects = board.visible_projects(False)
        if not projects:
            return to_text([_pad(c(escape("no project to present"), "dim"), width)], height, width)
        proj = projects[0]
    open_t, tasks = present_tasks(board, project_id)
    late, open_n, done = _present_counts(open_t, tasks, today)
    wide = width >= 100
    label_w, chip_w, field_w = _present_cols(width, wide)
    ax = _present_axis(board, proj, open_t, field_w, today)
    chain = set(critical_chain(board))
    p = _PresentGeo(width, label_w, chip_w, field_w, ax, chain, today, wide, proj.color)

    if open_t:
        wanted = board.task_by_id(cursor_id)
        cursor = wanted if wanted in open_t else open_t[0]
    else:
        cursor = None

    title = (c("◆ PRESENT", "bright", bold=True) + c(" · ", "dim")
             + c(escape(proj.name), proj.color, bold=True) + c(" — hybrid", "mut"))
    right = c(f"{open_n} open", "mut") + c(" · ", "dim") \
        + (c(f"▲{late} past due", "over", bold=True) if late else c(f"{done} done", "done"))
    lines = [header(title, right, width)]

    lines.append(_present_span_row(proj, board, p))
    for t in open_t:
        lines.append(_present_task_row(t, board, p, cursor=cursor is not None and t.id == cursor.id))
    lines.append(_pad(c("─" * width, "frame"), width))

    for t in open_t:
        lines.append(_present_brief(t, p, cursor is not None and t.id == cursor.id, width))
        if cursor is not None and t.id == cursor.id:
            note_w = width - 4
            for ln in _present_note_lines(t.notes, note_w, 3):
                lines.append(_present_note_row(ln, width, note_w))

    keys = " " + c("←", "bright", bold=True) + c("→", "bright", bold=True) \
        + c("  move the cursor", "dim") + c(" · ", "dim") \
        + c("the cursor'd task's notes expand", "dim")
    lines.append(_pad(keys, width))
    return _present_finish(lines, height, width)


def present_paths(board: Board, project_name: str | None,
                  today: date | None = None) -> tuple[Path, Path]:
    """The SVG and PNG export destinations, beside the board in the same
    `reports/` folder the HTML report used — the shipped destination convention."""
    today = today or date.today()
    slug = "".join(ch.lower() if ch.isalnum() else "-" for ch in (project_name or "board"))
    slug = slug.strip("-")[:40] or "board"
    base = Path(board.path).parent / "reports" / f"present-{slug}-{today.isoformat()}"
    return base.with_suffix(".svg"), base.with_suffix(".png")


def save_present_svg(text: Text, path: Path, width: int, height: int) -> Path:
    """The rich export path the report's SVG used: the frame as a standalone SVG.
    The console writes to devnull so the width-1 glyphs (◆ ╎ ┆) never hit the
    Windows console's cp1252 encoder on their way to the file."""
    con = Console(width=width + 2, height=height + 4, force_terminal=True,
                  color_system="truecolor", record=True,
                  file=open(os.devnull, "w", encoding="utf-8"))
    con.print(text, end="")
    path.parent.mkdir(parents=True, exist_ok=True)
    con.save_svg(str(path), title="taskboard · presentation")
    return path


def _find_msedge() -> str | None:
    """The headless Edge binary, from the standard install locations then PATH.
    None when Edge is not installed — the PNG cannot be rasterised without it."""
    pfx = os.environ.get("ProgramFiles(x86)") or r"C:\Program Files (x86)"
    pf = os.environ.get("ProgramFiles") or r"C:\Program Files"
    for base in (pfx, pf):
        cand = Path(base) / "Microsoft" / "Edge" / "Application" / "msedge.exe"
        if cand.is_file():
            return str(cand)
    return shutil.which("msedge") or shutil.which("microsoft-edge")


def save_present_png(svg_path: Path, png_path: Path,
                     width: int, height: int) -> Path | None:
    """Rasterise the SVG to a PNG with headless Edge. The terminal's own
    screenshot is SVG-only, so the PNG is Edge's render of the same file. None
    when Edge is absent or the render fails — the SVG is already written and the
    caller says the PNG needs Edge; it never crashes the export."""
    exe = _find_msedge()
    if exe is None:
        return None
    png_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [exe, "--headless=new", "--disable-gpu",
           f"--screenshot={png_path}",
           f"--window-size={width * 10},{height * 20}",
           svg_path.as_uri()]
    try:
        proc = subprocess.run(cmd, capture_output=True, timeout=30)
    except (subprocess.TimeoutExpired, OSError):
        return None
    if proc.returncode != 0 or not png_path.exists():
        return None
    return png_path


# ---------------------------------------------------------------------------
# dispatcher
# ---------------------------------------------------------------------------
RENDERERS = {
    "swimlanes": render_swimlanes,
    "agenda": render_agenda,
    "gantt": render_gantt,
    "kanban": render_kanban,
    "focus": render_focus,
    "flow": render_flow,
    "standup": render_standup,
    "people": render_people,
    "chainmap": render_chainmap,
}


def render_view(mode, board, show_archived, selected_id, today=None,
                width=68, height=0, line_map=None, presentation="grouped", tick=0,
                kanban_sort="project", kanban_group="project",
                kanban_collapsed=False, kanban_focus=None,
                gantt_focus=None, gantt_previous=None, lanes_presentation="waves",
                focus_presentation="cards",
                search_query: str | None = None,
                team_state: TeamState | None = None,
                team_filter: str = "equipo",
                setup_state: dict | None = None) -> Text:
    query = (search_query or "").strip()
    w = _clamp_width(width)
    # The `/` bar is INSERTED under the view's header, so a filtered view is
    # drawn two rows shorter: drawn at full height, its last two rows — the
    # gantt's time scale and the close — fell under the panel's fold.
    bar_h = max(1, height - 2) if height else height
    if mode == "focus":
        return render_focus(board, show_archived, selected_id, today, width, height,
                            line_map, presentation=focus_presentation)
    if mode == "kanban":
        if query:
            fb = filtered_board(board, query, show_archived)
            total = len(kanban_work(board.visible_tasks(show_archived)))   # LLR-603.1
            hits = len(kanban_work(fb.visible_tasks(show_archived)))
            text = render_kanban(fb, show_archived, selected_id, today, width, bar_h,
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
            text = render_gantt(fb, show_archived, selected_id, today, width, bar_h,
                                line_map, tick=tick, focus=gantt_focus,
                                previous=gantt_previous)
            if line_map is not None:
                for tid in list(line_map.keys()):
                    line_map[tid] += 2
            return _apply_search_overlay(text, query, hits, total, w)
        return render_gantt(board, show_archived, selected_id, today, width, height,
                            line_map, tick=tick, focus=gantt_focus,
                            previous=gantt_previous)
    if mode == "swimlanes":
        return render_swimlanes(board, show_archived, selected_id, today, width,
                                height, line_map, tick=tick,
                                presentation=lanes_presentation)
    if mode == "flow":
        return render_flow(board, show_archived, selected_id, today, width, height,
                           line_map)
    if mode == "standup":
        return render_standup(board, show_archived, selected_id, today, width, height,
                              line_map, team_state=team_state, team_filter=team_filter)
    if mode == "people":
        return render_people(board, show_archived, selected_id, today, width, height,
                             line_map, team_state=team_state, team_filter=team_filter)
    if mode == "setup":
        return render_setup(setup_state, board, width=width, height=height,
                            team_state=team_state)
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


def grid_nav(board, show_archived, today: date, width: int,
             height: int) -> list[list[str]]:
    """2D nav for the grid presentation: one column per panel x-position,
    tasks ordered top-to-bottom across layers exactly as the renderer draws."""
    lanes = lanes_of(board, show_archived, today)
    inner = _clamp_width(width) - 2
    h = height or 24
    n_cols = max(1, min(2, inner // 19))
    layers_n = max(1, -(-len(lanes) // n_cols))
    cap = n_cols * layers_n
    shown = lanes[:cap]
    cols: list[list[str]] = [[] for _ in range(n_cols)]
    for li in range(layers_n):
        chunk = shown[li * n_cols:(li + 1) * n_cols]
        for x, lane in enumerate(chunk):
            cols[x] += [t.id for t in _grid_list_order(lane)]
    return cols


def _fit_text(t: Text, width: int) -> Text:
    """`fit` for a styled Text: the same cut (`…` in the last cell) and padding,
    with the styles kept."""
    out = t.copy()
    if out.cell_len > width:
        out.truncate(max(0, width - 1))
        out.append("…")
    out.pad_right(max(0, width - out.cell_len))
    return out


def render_setup(setup_state: dict | None, board, width: int = 68,
                 height: int = 0, *, team_state: TeamState | None = None) -> Text:
    """The in-app team setup screen.  It edits a staged copy of the team
    configuration; nothing on disk changes until `ctrl+s` commits."""
    from .team_sync import probe_setup_health

    w = _clamp_width(width)
    state = setup_state or {}
    enabled = bool(state.get("enabled"))
    shared_dir = state.get("shared_dir", "")
    interval = state.get("interval_minutes", 30)
    user_id = state.get("user_id")
    projects = state.get("projects", [])
    roster = state.get("roster", [])
    cursor_section = state.get("cursor_section", 0)
    cursor_row = state.get("cursor_row", 0)
    checks = probe_setup_health(state, team_state)

    # Header
    lines: list[Text] = []
    lines.append(Text.assemble(("SETUP", f"bold {HEX['bright']}"),
                               (" · team · projects · roster", HEX["mut"])))
    lines.append(Text("─" * w, style=HEX["dim"]))
    lines.append(Text())

    def section(name: str) -> None:
        lines.append(Text())
        lines.append(Text(f"  {name}", style=f"bold {HEX['bright']}"))

    def fmt_check(key: str) -> tuple[str, str] | None:
        if key not in checks:
            return None
        ok, note = checks[key]
        glyph = "✓" if ok else "!"
        tone = "done" if ok else "soon"
        return (glyph, tone), note

    def row(label: str, control: Text, check_key: str | None,
            selected: bool = False) -> None:
        check, note = (None, "") if check_key is None else fmt_check(check_key)
        glyph = ""
        tone = "mut"
        if check is not None:
            glyph, tone = check
        prefix = "> " if selected else "  "
        label_text = Text.assemble((prefix, HEX["accent"] if selected else ""),
                                   (label, f"bold {HEX['ink']}" if selected else HEX["mut"]))
        check_text = Text(glyph, style=HEX.get(tone, tone))
        # pad to columns: label 24, control 30, check 4 — fitted as styled Text:
        # `str()` of a styled Text keeps its words and drops its styles, which
        # painted the cursor, the chosen chip and the checks plain (P2 UX-1)
        line = Text.assemble(
            _fit_text(label_text, 24), " ", _fit_text(control, 30), " ",
            _fit_text(check_text, 4), " ", (note, HEX["dim"]))
        lines.append(line)

    equipo_rows = [
        ("team mode",
         Text.assemble(
             (" on ", f"bold {HEX['bright']}" if enabled else HEX["mut"]),
             ("  off", HEX["mut"] if enabled else f"bold {HEX['bright']}")),
         "modo"),
        ("shared folder",
         Text.assemble(("▌", HEX["mut"]), (shared_dir or "—", HEX["ink"])),
         "carpeta"),
        ("  reach",
         Text(""),
         "alcance"),
        ("sync every",
         Text.assemble((" - ", HEX["mut"]),
                       (str(interval), HEX["ink"]),
                       (" + ", HEX["mut"]),
                       ("min", HEX["mut"])),
         "sync"),
        ("my identity",
         (Text.assemble((f" {user_id} ", f"bold #0b0f14 on {HEX.get(next((r.get('hue', 'mut') for r in roster if r.get('id') == user_id), 'mut'), HEX['mut'])}"))
          if user_id and roster else Text("—", style=HEX["mut"])),
         "identidad"),
    ]

    section("team")
    for i, (label, control, check_key) in enumerate(equipo_rows):
        row(label, control, check_key,
            selected=(cursor_section == 0 and cursor_row == i))

    section("team projects")
    for i, proj in enumerate(projects):
        shared = bool(proj.get("shared"))
        name = proj.get("name", proj.get("id", "?"))
        color = proj.get("color", "mut")
        # styles reach the screen now (LLR-201.3), so a colour team.json
        # spells wrong must not reach rich as a style (code review F9)
        color_hex = ((HEX.get(color) or (color if re.fullmatch(r"#[0-9a-fA-F]{6}", color)
                                         else None)) if isinstance(color, str) else None
                     ) or HEX["mut"]
        control = Text.assemble(
            (" shared ", f"bold {HEX['bright']}" if shared else HEX["mut"]),
            ("   hue ", HEX["mut"]),
            ("██", color_hex),
        )
        row(f"▐ {name}", control, None,
            selected=(cursor_section == 1 and cursor_row == i))

    section("roster")
    for i, member in enumerate(roster):
        mid = member.get("id", "")
        name = member.get("name", mid)
        hue = HEX.get(member.get("hue", "mut"), HEX["mut"])
        control = Text.assemble((f"{name:<10}", HEX["ink"]),
                                (" hue ", HEX["mut"]),
                                ("██", hue))
        row(f"██ {mid}", control, "roster" if i == 0 else None,
            selected=(cursor_section == 2 and cursor_row == i))

    lines.append(Text())
    lines.append(Text("─" * w, style=HEX["dim"]))
    KEY = f"bold {HEX['bright']}"
    lines.append(Text.assemble(
        ("tab", KEY), (" section   ", HEX["mut"]),
        ("↵", KEY), (" edit   ", HEX["mut"]),
        ("space", KEY), (" toggle   ", HEX["mut"]),
        ("a", KEY), (" add   ", HEX["mut"]),
        ("x", KEY), (" remove   ", HEX["mut"]),
        ("ctrl+s", KEY), (" save   ", HEX["mut"]),
        ("esc", KEY), (" cancel", HEX["mut"]),
    ))

    return Text("\n").join(lines)


def nav_model(mode, board, show_archived, today=None, width: int = 68,
              height: int = 0, *, selected_id: str | None = None,
              kanban_sort="project",
              kanban_group="project", kanban_collapsed=False,
              kanban_focus=None, gantt_focus=None,
              presentation="grouped", focus_presentation="cards",
              team_state: TeamState | None = None,
              team_filter: str = "equipo") -> list[list[str]]:
    today = today or date.today()
    tasks = board.visible_tasks(show_archived)

    if mode == "setup":
        return []
    if mode == "focus":
        pinned = focus_tasks(board, show_archived)
        if focus_presentation in ("review", "stale"):
            ordered = stale_order(board, pinned, today, show_archived)
            return [[t.id for t in ordered]]
        pinned.sort(key=lambda t: _focus_sort_key(board, show_archived, t, today))
        return [[t.id for t in pinned]]

    if mode == "people":
        # Key `9` is ungated, so people IS reachable with team mode off, and
        # `render_people` answers that with a body that says so. Nav is the
        # other seat on that entry point and must agree with the render: a view
        # that draws no cards offers no rows to walk. The disagreement was not
        # merely the F-3 trap (a cursor parked where the screen draws nothing);
        # it was an AttributeError on the first cursor key.
        if team_state is None:
            return []
        ids: list[str] = []
        for member in team_state.roster():
            uid = member["id"]
            tasks = _member_tasks_for_filter(board, team_state, uid, team_filter)
            tasks = sort_by_due(tasks)
            ids.extend(t.id for t in tasks)
        return [ids]

    if mode in ("flow", "standup"):  # read-only dashboards: no selectable rows
        return []

    if mode == "chainmap":     # one column per depth; arrows walk the chains
        return _chainmap_nav(board, show_archived)

    if mode == "kanban":       # the phase columns, in THE shared seat's order
        tasks = kanban_work(tasks)       # a milestone is never a card (LLR-603.1)
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

        if presentation == "grouped":
            # the readable board: THE seat its renderer reads (LLR-301.1, F-3)
            return kanban_nav(kanban_plan(board, show_archived, selected_id, today,
                                          width, height, sort=kanban_sort,
                                          group=kanban_group,
                                          collapsed=kanban_collapsed,
                                          focus=kanban_focus))
        cols = []                  # the matrix: every phase, in the seat's order
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
        # The renderer and the navigator MUST read from the same seat; the
        # grid lays panels in 2D columns, while waves keeps the classic stack.
        if presentation == "grid":
            return grid_nav(board, show_archived, today, width, height)
        # ONE column: the view is a stack of lanes, and the only selectable
        # things in it are the tasks it NAMES, in the order it names them — the
        # lead's worst late task first, then each stacked lane's titles. The
        # allocator decides how many, so the height is part of the question.
        return [swimlane_nav(board, show_archived, today, width, height)]

    if mode == "agenda":       # dated (sorted by due), then undated — matches render
        dated = [t for t in tasks if parse_iso(t.due_date) is not None]
        undated = [t for t in tasks if parse_iso(t.due_date) is None]
        return [[t.id for t in sort_by_due(dated)] + [t.id for t in undated]]

    if mode == "gantt":       # THE renderer's seat: open work, in draw order
        body = max(0, height - 1 - GANTT_RULER_ROWS) if height else 10 ** 6
        groups = gantt_plan(board, show_archived, selected_id, today, body, gantt_focus)
        return [[t.id for g in groups for t in g.rows]]

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
        "open_priorities": {t.priority if t.priority in PRIORITY_BADGE else "normal"
                            for t in open_},
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


# ---------------------------------------------------------------------------
# per-view help copy — the usage text and annotated example for each view.
# The authoritative copy lives in prototypes/team_sync/generate.py; this is
# the runtime mirror used by HelpModal.
# ---------------------------------------------------------------------------
def help_usage(mode: str) -> list[tuple[str, list[str]]]:
    """(section heading, bullet lines) for the active view's help. English, like
    every string the app paints (batch 2026-10-02-batch-02, HLR-204); each
    bullet fits the help column's 44 cells."""
    if mode == "kanban":
        return [
            ("what it is for", ["run the work: move tasks between phases,",
                                "group by project, priority or horizon."]),
            ("first thing to do", ["j/k down and up · ↵ opens the card.",
                                   "then: s sort · g group · z collapse."]),
            ("the card's numbers", ["·Nd = days IN the phase (ageing)",
                                    "+Nd = days UNTIL the deadline (countdown)",
                                    "+/- move a date · m: the move again,",
                                    "next mode (stay / push / together)",
                                    "◂N = waits on N open tasks · L links",
                                    "▸N = N open tasks wait on this one"]),
            ("the board", ["!! high · == normal · ++ low (open only)",
                           "open highs ride one band on top of the",
                           "grouped board; +N more ↓ when it is full",
                           "▐ band rule: a project once, across columns",
                           "◆ on a band rule: a milestone, never a card",
                           "┈ splits cards · ✓ the done rail (✓N narrow)",
                           "▲ above · ▼ below: bands folded off screen"]),
        ]
    if mode == "swimlanes":
        return [
            ("what it is for", ["see the board at a glance: the project under",
                                "most pressure first, its load field drawn."]),
            ("first thing to do", ["read the leader's field — the curve ends",
                                   "at ◆ (its due date). then: tab layout."]),
            ("the marks", ["◆ = the project's due date on the curve",
                           "· lattice = field with no work (ground)",
                           "ash = projects at rest"]),
        ]
    if mode == "agenda":
        return [
            ("what it is for", ["scan what is due: each dated task is a ●",
                                "on ONE shared axis of days."]),
            ("first thing to do", ["read each ●'s distance to today's rule",
                                   "╎ — the order already says the urgency."]),
            ("the marks", ["● = a task on its day",
                           "╎ = today (breathes slowly, same column)",
                           "no meter on purpose: the row says it twice"]),
        ]
    if mode == "gantt":
        return [
            ("what it is for", ["the whole board, fitted to the open work.",
                                "▾ open · ▸ folded when it does not fit."]),
            ("first thing to do", ["read the ruler on top: months and days;",
                                   "⟦━⟧ marks the task's exact dates."]),
            ("the marks", ["─ span · ● progress · ◆ due",
                           "╌ task, tip ○◔◑◕ = phase · ━ critical chain",
                           "↳ waits on another · ✓n done · ▲n late",
                           "◆ title = a milestone · ◆✓ reached · M"]),
        ]
    if mode == "focus":
        return [
            ("what it is for", ["read and annotate the PINNED work, without",
                                "the noise of the rest of the board."]),
            ("first thing to do", ["tab changes the layout (tiles, inspector,",
                                   "images, review, stale). t pins the task."]),
            ("the layouts", ["tiles = cards · inspector = master/detail",
                             "stale = what has sat still too long"]),
        ]
    if mode == "flow":
        return [
            ("what it is for", ["measure MOVEMENT: how long work takes per",
                                "phase, where it ages, how much finishes."]),
            ("first thing to do", ["the heatmap: the busiest cell is where",
                                   "work gets stuck. empty: 'no history yet'."]),
            ("the numbers", ["cycle = median days per phase (closed)",
                             "open n=N = open intervals, never a number",
                             "throughput = finished per week"]),
        ]
    if mode == "standup":
        return [
            ("what it is for", ["the team view to READ: load, current front",
                                "and how fresh each person's data is."]),
            ("first thing to do", ["one row per person; stale is judged, not",
                                   "hidden. ↵ opens their board (read-only)."]),
            ("the marks", ["▰▱ = load (tasks in Doing)",
                           "the sync age always on the right",
                           "red = past the tolerance (45 min)"]),
        ]
    if mode == "people":
        return [
            ("what it is for", ["work with shared visibility: the lanes'",
                                "axis is WHO, not the project."]),
            ("first thing to do", ["the operator's row on top, editable; others",
                                   "◦ read-only · filter: all · team · personal"]),
            ("the marks", ["◦ = read-only (a teammate's)",
                           "the sync age rides on the person's label",
                           "the +Nd countdown works as in the kanban"]),
        ]
    if mode == "setup":
        return [
            ("what it is for", ["set up the team inside the app: shared dir,",
                                "interval, identity, shared projects, roster."]),
            ("first thing to do", ["move with tab/j/k; ↵ edits; space toggles;",
                                   "a add · x remove · ctrl+s save · esc cancel"]),
            ("the checks", ["✓ = verified · ! = needs attention",
                            "advisory: they never block editing",
                            "recomputed on open and after ctrl+s"]),
        ]
    if mode == "chainmap":
        return [
            ("what it is for", ["the dependency web: who waits on whom, per",
                                "project, with ready/waits/late marks."]),
            ("first thing to do", ["6 opens it; arrows walk the chains; ↵ opens",
                                   "x drops the selected task incoming link."]),
            ("the marks", ["✓ done · ▷ ready · ○ chain head · ◂N waits",
                           "┃ heavy = the critical chain · ▲Nd late",
                           "dates switch = the rule a move follows",
                           "set here = that project rule is custom"]),
        ]
    return []


def help_example(mode: str) -> tuple[str, str]:
    """(annotated example line, what it means) for the active view."""
    if mode == "kanban":
        return ("▊ !! sync daemon ↗ ·3d ▸2 ◂1 +4d",
                "!! high (== normal, ++ low) · ↗ url · 3d in phase · "
                "2 wait on it · waits on 1 · due in 4d")
    if mode == "swimlanes":
        return ("▎ platform ████▒░◆ 12d",
                "the curve is the load; the air before ◆ is what does not fit")
    if mode == "agenda":
        return ("────●──╎──●────●──",
                "the distance to ╎ IS the urgency; nothing else is needed")
    if mode == "gantt":
        return ("▸ Ops     4 open  ◂───╎──●────◆··",
                "folded: its row says how much is still open; ▾ opens it")
    if mode == "focus":
        return ("▊ write the ADR ◔ ·12d",
                "pinned 12 days ago, untouched — stale is naming it")
    if mode == "flow":
        return ("Doing ░▒▓█▓▒░░",
                "week 4 in Doing carried everything — that is where it stuck")
    if mode == "standup":
        return ("▐ ana ▰▰▱▱▱ 2 doing · landing hero · 3 h ago",
                "her data is 3 hours old — read it with that age in mind")
    if mode == "people":
        return ("▐ ANA 12 min ago · landing hero ◦ -3d",
                "hers, read-only, due in 3 days, data from 12 min ago")
    if mode == "setup":
        return ("▌ D:/team/taskboard  ✓  exists and is writable",
                "each row shows its check and its note")
    if mode == "chainmap":
        return ("┃Audit dependencies ━━▸┃Add push notifications",
                "the heavy chain is the critical path; each tile's mark says its state")
    return ("", "")


def legend_entries(mode: str, board: Board, today: date | None = None,
                   width: int = 96, height: int = 30,
                   show_archived: bool = False,
                   team_state: TeamState | None = None,
                   team_filter: str = "equipo",
                   selected_id: str | None = None,
                   gantt_focus: str | None = None,
                   gantt_previous: str | None = None,
                   kanban_presentation: str = "grouped",
                   kanban_group: str = "project",
                   kanban_focus: str | None = None) -> list[tuple[str, str]]:
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
        out.append((c("▐", hue), "project band, by colour"))
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
        # EVERY ENTRY IS ASKED OF THE FRAME THE SCREEN SHOWS (G-A + AX-2): the
        # same selection, archive toggle and focus the renderer was given, so a
        # mark the frame does not draw cannot be explained, and one it draws
        # cannot be missing (code review F3, batch 2026-10-02-batch-01).
        g_lines, drawn, groups, gax = _gantt_frame(board, show_archived, selected_id,
                                                   today, width, height, None, 0,
                                                   gantt_focus, gantt_previous)
        body = "\n".join(g_lines[1 + GANTT_RULER_ROWS:])
        g_label = gantt_columns(_clamp_width(width))[0]
        if any(g.project is not None for g in groups):
            out.append((c(FIELD_REACH * 2, "ash") + c(FIELD_REACH * 2, hue),
                        "the span: ash is elapsed, colour is what remains"))
        if "progress" in drawn:
            out.append((c(PROGRESS_DOT, hue), "how far the work actually got"))
        if "due" in drawn:
            out.append((c("◆", hue), "the project's committed due date"))
        out.append((c(RULE, "accent"), "today"))
        if gax.guides():
            out.append((c(LATTICE + FIELD_WEEK + LATTICE, "dim"),
                        "calendar guide: Mondays, or the 1st"))
        if "┃" in g_lines[1]:
            out.append((c("┃", "frame"), "the ruler: a month starts here"))
        if "selected" in drawn:
            out.append((c(ECHO_OPEN + ECHO_FILL + ECHO_CLOSE, "bright", bold=True),
                        "the ruler: the selected task's exact dates"))
        if "milestone" in drawn:
            out.append((c("◆", hue), "a milestone: one date, no bar"))
        if "reached" in drawn:
            out.append((c("◆", "reached") + c("✓", "reached"), "a milestone reached"))
        if FIELD_TASK in body:
            out.append((c(FIELD_TASK * 2, hue) + c(FIELD_PHASE_TIP[1], hue),
                        "a task's reach, tipped by its phase"))
        if "crit" in drawn:
            out.append((c(CRITICAL_REACH * 2, "bright", bold=True),
                        "the critical chain"))
        if "waits" in drawn or "early" in drawn:
            out.append((c("↳", "mut"), "waits on open work (red: starts too early)"))
        if "beyond" in drawn:
            out.append((c(OFF_LEFT + OFF_RIGHT, "mut"), "the work runs beyond the window"))
        if any(not g.unfolded for g in groups):
            out.append((c("▸", hue), "a folded project: its open count, no rows"))
        if g_label >= 26 and re.search(r"✓\d", body):
            out.append((c("✓2", "done"), "finished work, folded into a count"))
    if mode == "agenda":
        out.append((c("●", "over"), "a task's due date, on the shared day axis"))
        out.append((c("─", "dim"), "its reach: from today to that date"))
        out.append((c("┃", "accent"), "today"))
        if f["blocked"]:
            out.append((c("▲", "over"), "blocked"))
    if mode == "flow":
        records, _ = history.read(board.path)
        if records:
            out.append((c("3.5d", "ink"), "median days in phase (closed intervals)"))
            out.append((c("open n=1", "mut"), "open intervals: not a cycle yet"))
            out.append((c("░▒▓█", "mut"), "heatmap: task-days per phase × week"))
            out.append((c("█", "hd"), "throughput: tasks reaching the terminal phase"))
    if mode == "standup":
        out.append((c("▌", "bright"), "operator row"))
        out.append((c("▎", "mut"), "teammate row"))
        out.append((c("▰▱", "mut"), "open task load"))
        if team_state is not None:
            out.append((render_team_filter_chrome(team_filter),
                        "classification filter"))
    if mode == "people":
        out.append((c("▌", "bright"), "operator lane"))
        out.append((c("▎", "mut"), "teammate lane"))
        out.append((c("◦", "mut"), "foreign card: read-only"))
        if team_state is not None:
            out.append((render_team_filter_chrome(team_filter),
                        "classification filter"))
    if mode == "focus":
        pinned = focus_tasks(board, show_archived)
        if pinned:
            out.append((c("▎", hue), "project spine (colour = project)"))
            out.append((c("==text==", "soon"), "highlight: yellow / warning"))
            out.append((c("!!text!!", "over"), "highlight: red / attention"))
            out.append((c("++text++", "green"), "highlight: green / resolved"))
            if any(t.images for t in pinned):
                out.append((c("▤", "mut"), "task has images"))
    if mode == "chainmap":
        out.append((c("✓", "ash"), "done"))
        out.append((c("▷", "done"), "ready"))
        out.append((c("◂N", "hd"), "waits on N open"))
        out.append((c("━", "bright"), "critical chain"))
        out.append((c("─", "over"), "starts before due"))
        out.append((c("─", "ash"), "satisfied"))
        out.append((c("▲", "over"), "late"))
    if mode == "swimlanes":
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
    if mode == "kanban":
        # the badges an open card wears (PRIORITY_BADGE) — each explained only
        # while some visible open card wears it
        for prio, meaning in (("high", "high priority, open"),
                              ("normal", "normal priority, open"),
                              ("low", "low priority, open")):
            if prio in f["open_priorities"]:
                token, tone = PRIORITY_BADGE[prio]
                out.append((f"[b reverse {HEX[tone]}]{token}[/]", meaning))
        # `◆` on a band rule: asked of the same seat that draws it (code review K-1)
        if kanban_presentation == "grouped" and kanban_group == "project":
            kw = _clamp_width(width)
            plan = kanban_plan(board, show_archived, selected_id, today, kw, height,
                               group=kanban_group, focus=kanban_focus)
            if any(band_rule_facts(board, b, today, show_archived, kw)[1] for b in plan.bands):
                out.append((c("◆", "mut"), "a milestone on its project's band rule"))
    # THE NO-GHOST LAW, and archived is its clearest case: the mark exists on
    # screen only while `v` is on AND something is actually archived. Explaining
    # a mark the reader cannot see is the same fault as hiding one they can.
    if show_archived and any(t.archived for t in board.visible_tasks(True)):
        # the gantt draws no row for rest work (D2, batch 2026-10-02-batch-01):
        # archived work is a count on its project's span row, never a `▣` row
        drawn = mode != "gantt"
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


# ---------------------------------------------------------------------------
# the gantt link mode's frame (batch 2026-10-04-batch-01, LLR-502.3, D-A)
# ---------------------------------------------------------------------------
LINK_BACKGROUND = {" ", LATTICE, FIELD_WEEK} | set(RULE_PHASES)


def _cell_index(plain: str, col: int) -> int | None:
    """The index of the character painted at cell `col` (a wide glyph in a label
    takes two cells), or None past the end."""
    w = 0
    for i, ch in enumerate(plain):
        if w == col:
            return i
        w += cell_len(ch)
        if w > col:
            return None
    return None


def gantt_link_order(board: Board, show_archived: bool, today: date,
                     previous: str | None = None) -> list[Task]:
    """The open rows, in the order the gantt draws them (every group unfolded; a
    reached milestone's row is not a candidate): the link mode's candidate cycle."""
    groups = gantt_plan(board, show_archived, None, today, 10 ** 6, None, previous)
    return [t for g in groups for t in g.open]


def gantt_link_frame(board: Board, show_archived: bool, waiter: Task, cand: Task | None,
                     today: date, width: int, height: int, right: str,
                     loops: set[str]) -> tuple[Text, dict]:
    """The gantt as link mode paints it: the candidate is the selection (its group
    unfolds), the waiter's group is kept open as the previous one, the header says
    `GANTT · LINK` with `right`, each loop row wears `⟲` in its gutter, and
    `gantt_link_overlay` draws the proposed link on the FIELD only. Returns the
    Text and the facts the tests read (`label_w`, rows, the `═` and connector
    cells)."""
    w = _clamp_width(width)
    line_map: dict[str, int] = {}
    lines, _drawn, _groups, ax = _gantt_frame(
        board, show_archived, cand.id if cand else None, today, w, height, line_map, 0,
        None, gantt_group_key(board, waiter), waiter.id)
    lines[0] = header(c("◆ GANTT · LINK", "bright", bold=True), c(escape(right), "mut"), w,
                      tone="bright")
    label_w = gantt_columns(w)[0]
    text = Text()
    rows = [Text.from_markup(ln) for ln in lines]
    for tid in loops:
        r = line_map.get(tid)
        i = _cell_index(rows[r].plain, label_w) if r is not None else None
        if i is not None:
            rows[r] = rows[r][:i] + Text("⟲", style=HEX["mut"]) + rows[r][i + 1:]
    facts = gantt_link_overlay(rows, line_map, ax, label_w, waiter, cand)
    for i, r in enumerate(rows[:height] if height else rows):
        if i:
            text.append("\n")
        text.append_text(r)
    facts.update(label_w=label_w, line_map=line_map)
    return text, facts


def gantt_link_overlay(rows: list[Text], line_map: dict[str, int], ax: GanttAxis,
                       label_w: int, waiter: Task, cand: Task | None) -> dict:
    """Draw the proposed link on the painted rows, in place (LLR-502.3): from the
    cell after the candidate's due, a connector in the bright tone toward the
    waiter's row, over BACKGROUND cells only; on the waiter's row the overlap days
    (the one measure) as `═` in the over tone — none for a waiter with no start.
    Never in the label column or the gutter: every cell written is right of
    `label_w`. Returns the columns it wrote."""
    out = {"overlap": [], "connector": []}
    if cand is None:
        return out
    pdue, start = parse_iso(cand.due_date), parse_iso(waiter.start_date)
    rw, rc = line_map.get(waiter.id), line_map.get(cand.id)
    first = label_w + 1                                 # the field's first column

    def put(r: int, col: int, glyph: str, tone: str, only_background: bool) -> bool:
        if col < first or col >= first + ax.w or r >= len(rows):
            return False
        i = _cell_index(rows[r].plain, col)
        if i is None:
            return False
        if only_background and rows[r].plain[i] not in LINK_BACKGROUND:
            return False
        rows[r] = rows[r][:i] + Text(glyph, style=HEX[tone]) + rows[r][i + 1:]
        return True

    if rw is not None and pdue is not None and start is not None and start <= pdue:
        for x in range(max(0, ax.cell(start)), min(ax.w - 1, ax.end_cell(pdue)) + 1):
            if put(rw, first + x, "═", "over", False):
                out["overlap"].append(first + x)
    if rw is not None and rc is not None and pdue is not None and rw != rc:
        col = first + ax.end_cell(pdue) + 1
        down = rw > rc
        if put(rc, col, "╮" if down else "╯", "bright", True):
            out["connector"].append((rc, col))
        lo, hi = (rc, rw) if down else (rw, rc)
        for r in range(lo + 1, hi):
            if put(r, col, "│", "bright", True):
                out["connector"].append((r, col))
        if put(rw, col, "╯" if down else "╮", "bright", True):
            out["connector"].append((rw, col))
    return out
