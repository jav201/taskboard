"""Inc MR-b — reading the presentation `R` on fixture MR-F (observable output only).

The presentation's three views as the shipped seats draw them: `render_present`
(views 1 `gantt` and 2 `split`) and `render_present_all` (view 3 `all`, its
`timeline`), read as terminal cells after `to_text` (`Text.plain`, `cell_len`),
plus the per-cell Style. The app is driven through keys only (`R`, `1`/`2`/`3`,
arrows, `space`, `x`) on a real registry built by `milestone_row_fixture.build`.

The deck helpers write the `x` deck the way `PresentScreen.action_export` does
(`present_deck_boards` → `report_html.extract` → `report_deck.render`), so a base
copy can be taken on `8ca174c` and compared byte for byte (LLR-4654.1).

Every name and date is synthetic (MR-F, TODAY 2026-10-20).
"""
from __future__ import annotations

import hashlib
import re
from contextlib import asynccontextmanager
from pathlib import Path

from rich.cells import cell_len
from rich.console import Console

import milestone_row_fixture as fx
from milestone_row_fixture import GROUND, MARKS, TODAY, cells_of, norm
from taskboard import report_deck, report_html, views

__all__ = ["GROUND", "MARKS", "TODAY", "cells_of", "norm"]

GOLDEN = Path(__file__).resolve().parent / "milestone_row_present_base.json"
SIZES = [(118, 30), (80, 24)]
VIEWS12 = ("gantt", "split")
_CON = Console(width=400, color_system="truecolor", force_terminal=True)
#: every glyph a milestone can be drawn with on a field (class shapes, hollows, `◆`)
MS_GLYPHS = set(MARKS) | {"◆", "◇"}
PILOT_TASKS = ["Pilot store list", "Pilot telemetry", "Train store staff", "Field support rota"]
PILOT_MS_TITLES = ["Rubric sign-off", "Steering go/no-go", "Store list frozen", "Pilot launch"]


def golden() -> dict:
    import json
    return json.loads(GOLDEN.read_text(encoding="utf-8"))


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class Rows:
    """One frame (a `Text` of `width` cells per line) read as cells and styles,
    with the presentation's own column split (`_present_cols`): label | gutter |
    field | space + chip."""

    def __init__(self, text, width: int):
        self.text, self.W = text, width
        self.lines = text.plain.split("\n")
        self._tl = text.split("\n", allow_blank=True)
        self.label_w, self.chip_w, self.field_w = views._present_cols(width, width >= 100)
        self.x0 = self.label_w + 1

    def __len__(self):
        return len(self.lines)

    def cells(self, i):
        return cells_of(self.lines[i])

    def label(self, i) -> str:
        return "".join(self.cells(i)[:self.label_w])

    def gutter(self, i) -> str:
        return self.cells(i)[self.label_w]

    def fcells(self, i) -> list[str]:
        return self.cells(i)[self.x0:self.x0 + self.field_w]

    def field(self, i) -> str:
        """The field as text, every ground glyph read as one blank."""
        return norm(self.fcells(i))

    def chip(self, i) -> str:
        """The chip cells: the last `chip_w + 1` (the space and the chip)."""
        return "".join(self.cells(i)[-(self.chip_w + 1):])

    def widths(self) -> list[int]:
        return [cell_len(ln) for ln in self.lines]

    def style(self, i, x):
        """The Style painted at cell `x` of line `i`."""
        line, cx = self._tl[i], 0
        for j, ch in enumerate(line.plain):
            w = cell_len(ch)
            if w == 0:
                continue
            if cx == x:
                return line.get_style_at_offset(_CON, j)
            cx += w
        raise IndexError(x)

    def fstyle(self, i, f):
        return self.style(i, self.x0 + f)

    # -- where the rows are ------------------------------------------------------
    def span(self) -> int:
        """Views 1/2: the project's span row (`▌ NAME …`)."""
        return next(i for i, ln in enumerate(self.lines) if ln.startswith("▌ "))

    def rule(self) -> int:
        """Views 1/2: the rule under the field."""
        return next(i for i, ln in enumerate(self.lines) if ln.startswith("─"))

    def head(self, name: str) -> int:
        """View 3: the project's head row (`▾ ■ Name`, `▸ ■ Name`, `⟦ ■ Name`)."""
        pat = re.compile(r"^[▾▸⟦] \S " + re.escape(name[:12]))
        return next(i for i, ln in enumerate(self.lines) if pat.match(ln))

    def heads(self) -> list[int]:
        return [i for i, ln in enumerate(self.lines) if re.match(r"^[▾▸⟦] \S \S", ln)]

    def has_mark(self, i) -> bool:
        """Does line `i`'s FIELD hold a milestone glyph?"""
        return bool(MS_GLYPHS & set(self.field(i)))


def frame(b, pid, cursor, W=118, H=30, view="gantt") -> Rows:
    """Views 1/2 through the shipped `render_present`."""
    return Rows(views.render_present(b, pid, cursor, TODAY, W, H, view), W)


def frame3(b, cur, W=118, H=30, folded=frozenset()):
    """View 3 through `render_present_all`: (its timeline as Rows, the PresentAll)."""
    pa = views.render_present_all(b, cur, TODAY, W, H, folded)
    return Rows(pa.timeline, pa.timeline_w), pa


def due_cell(rows: Rows, b, tid: str, ax) -> int:
    from taskboard.models import parse_iso
    return ax.cell(parse_iso(b.task_by_id(tid).due_date))


def axis12(b, pid, W):
    """The axis views 1/2 draw on (the presentation's own helper, as at base)."""
    open_t = views.present_tasks_m(b, pid)[0]
    _l, _c, field_w = views._present_cols(W, W >= 100)
    return views._present_axis(b, b.project_by_id(pid), open_t, field_w, TODAY)


def axis3(b, tw):
    _l, _c, field_w = views._present_cols(tw, tw >= 100)
    return views._all_axis(views._all_plan(b), field_w, TODAY)


def literal_cut(text: str, title: str) -> bool:
    """`text` is `title` whole, or `title`'s head cut with `…` (at least 1 char kept;
    a one-cell pad before the `…` is allowed where a wide glyph did not fit)."""
    text = text.strip()
    if text == title:
        return True
    head = text[:-1].rstrip(" ")
    return text.endswith("…") and len(head) > 0 and title.startswith(head)


# ============================================================================
# the `x` deck, layer 0 — the export's own three calls (app.py action_export)
# ============================================================================
LANE = ("main", "Client A", "sky")


def deck_bytes(board, view: int, deck_boards=None) -> bytes:
    """The deck `x` writes in view `view` (1, 2: the presented project `ppr`;
    3: every shown project) for `board`, with MR-F's classes and no people."""
    deck_boards = deck_boards or views.present_deck_boards
    boards = deck_boards(LANE + (board,), None if view == 3 else "ppr")
    key = None
    if view < 3 and boards[0][3].projects:
        key = f"{LANE[0]}:{boards[0][3].projects[0].id}"
    d = report_html.extract(boards, {}, board.marks, TODAY, project=key)
    return report_deck.render(d).encode("utf-8")


def deck_boards_mutant(lane, project_id):
    """LLR-4654.1's negative control (B-4, RB-6, A-1): `present_deck_boards`
    holding `present_stop_order(present_tasks_m(board, p.id)[0])` in place of
    `present_tasks_m(board, p.id)[1]`. `present_stop_order` is pure — it adds and
    drops nothing (SEAM-2) — and the deck re-sorts what it holds by board
    position, so the mutant's held SET is `[0]`'s: the open shown tasks, the
    reached `tm1` dropped. Built on the shipped function by feeding it `[0]` as
    `[1]`, so the control runs on the base revision too."""
    real = views.present_tasks_m

    def open_only(board, pid):
        open_t, _all = real(board, pid)
        return open_t, list(open_t)

    views.present_tasks_m = open_only
    try:
        return views.present_deck_boards(lane, project_id)
    finally:
        views.present_tasks_m = real


# ============================================================================
# the real app, keys only
# ============================================================================
@asynccontextmanager
async def present(home, size=(118, 30), sel=None, focus="ppr", view=1, hidden=(), **kw):
    """The real app on MR-F (`kw` for `build`), `R` pressed with `sel` selected
    (None: the project `focus` focused, no cursor), then `view`'s key."""
    fx.build(home, **kw)
    from taskboard.__main__ import open_app
    app = open_app(None)
    async with app.run_test(size=size) as pilot:
        await pilot.pause()
        await pilot.press("escape")                  # the home -> the board
        await pilot.pause()
        if hidden:
            await pilot.press("3")                   # the gantt: `#` lives there
            await pilot.pause()
            for cid in hidden:
                await fx.hide_class(pilot, cid)
        app.selected_task_id = sel
        app.focused_project_id = focus if sel is None else None
        await pilot.press("R")
        await pilot.pause()
        if view != 1:
            await pilot.press(str(view))
            await pilot.pause()
        yield app, pilot


def screen_of(app):
    """The PresentScreen under any modal on top."""
    return next(s for s in reversed(app.screen_stack) if type(s).__name__ == "PresentScreen")


def pframe(app) -> Rows:
    """The frame the PresentScreen paints (its `#present-frame` Text, after `to_text`).
    View 3: the timeline columns only when the rail is drawn."""
    scr = screen_of(app)
    text = scr.query_one("#present-frame").content
    return Rows(text, scr.size.width)


def ptimeline(app) -> Rows:
    """View 3's timeline as the screen draws it (the rail cut off when drawn)."""
    scr = screen_of(app)
    pa = scr._render_all()
    return Rows(pa.timeline, pa.timeline_w)


def hint(app) -> str:
    return screen_of(app).query_one("#present-hint").content.plain


async def keys(pilot, *ks):
    for k in ks:
        await pilot.press(k)
        await pilot.pause()


def cursor_brief(rows: Rows) -> str | None:
    """View 1: the title inside the cursor brief's `⟦…⟧` (below the rule)."""
    for ln in rows.lines[rows.rule() + 1:]:
        m = re.search(r"⟦(.*)⟧", ln)
        if m:
            return m.group(1)
    return None


def briefs(rows: Rows) -> list[str]:
    """View 1: the brief titles below the rule, top to bottom."""
    out = []
    for ln in rows.lines[rows.rule() + 1:]:
        s = ln.strip()
        if not s:
            break
        s = s.lstrip("⟦")
        out.append(re.split(r"⟧|\s{2,}", s)[0].strip())
    return out


def blocks(rows: Rows) -> tuple[list[str], list[str]]:
    """View 2: the block headings (`▌ ` / `▎ ` rows) of the left and right columns."""
    left, right = [], []
    cw = (rows.W - 2 - 3) // 2 if rows.W >= 100 else rows.W - 2
    for ln in rows.lines[rows.rule() + 1:]:
        parts = [ln[1:1 + cw]] + ([ln[1 + cw + 3:]] if rows.W >= 100 else [])
        for col, part in zip((left, right), parts):
            m = re.match(r"^[▌▎] (.+?)(\s{2,}|$)", part)
            if m:
                col.append(m.group(1).strip())
    return left, right
