"""PROTOTYPE round 2 — B (cursor ruler) + start–end chips + a per-task
"show in presentation" flag, captured FROM THE RUNNING APP.

    python prototypes/present_rulers/app_capture.py

Sub-shape A (PROTOTYPE.md): the real `TaskboardApp` runs headless; only
`render_present` and `PresentScreen` are patched. Keys are pressed through the
pilot exactly as a user would (`R`, `→`, `space`, `a`), and each frame is the
app's own `export_screenshot()` SVG — the Textual compositor, the real hint row,
the real modal stack.

The flag lives in `task.extra["present"]` (False = left out), so the prototype
needs no model change; `space` toggles it on the cursor task, `a` brings every
hidden task back. Default: every task shown.
"""
from __future__ import annotations

import asyncio
import re
import sys
import tempfile
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))
sys.path.insert(0, str(HERE))

from textual.binding import Binding

import present_board as pb
import proto as P
from taskboard import app as app_mod
from taskboard import models
from taskboard import views as V
from taskboard.views import (_md, _pad, _present_brief, _present_counts, _present_finish,
                             _present_note_lines, _present_note_row, _PresentGeo, c,
                             critical_chain, escape, fit, gantt_dep_mark, header, parse_iso,
                             present_tasks, title_markup)

OUT = HERE / "out"


class _Today(date):
    @classmethod
    def today(cls):
        return pb.TODAY


# --------------------------------------------------------------------------- #
# the flag
# --------------------------------------------------------------------------- #
def shown(t) -> bool:
    return t.extra.get("present", True) is not False


def shown_tasks(board, project_id):
    open_t, tasks = present_tasks(board, project_id)
    return [t for t in open_t if shown(t)], [t for t in tasks if shown(t)]


def hidden_count(board, project_id) -> int:
    return sum(1 for t in present_tasks(board, project_id)[0] if not shown(t))


# --------------------------------------------------------------------------- #
# start–end chips: both dates, no arithmetic for the audience
# --------------------------------------------------------------------------- #
def span_label(s: date | None, e: date | None) -> str:
    if e is None:
        return f"from {_md(s)}" if s else "no dates"
    if s is None:
        return f"due {_md(e)}"          # no start set: say so, the bar's left end is drawn
    if s == e:
        return _md(e)
    if (s.year, s.month) == (e.year, e.month):
        return f"{_md(s)}–{e.day}"
    return f"{_md(s)}–{_md(e)}"


def chip(s_iso, e_iso, today, width, is_open=True) -> str:
    s, e = parse_iso(s_iso), parse_iso(e_iso)
    tone = "over" if (is_open and e is not None and e < today) else "mut"
    if e is None and s is None:
        tone = "dim"
    return c(fit(span_label(s, e), width, "right"), tone)


def cols(width: int, wide: bool) -> tuple[int, int, int]:
    label_w = 30 if wide else 20
    chip_w = 13                         # `Aug 21–Oct 10` is 13: 12 clipped it at 80
    return label_w, chip_w, width - label_w - 1 - 1 - chip_w


def span_row(proj, board, p) -> str:
    cells = V._gantt_span(proj, p.ax, board.project_progress(proj.id), 0)
    label = c("▌ ", p.hue) + c(escape(fit(proj.name.upper(), p.label_w - 2)), p.hue, bold=True)
    start = getattr(proj, "start_date", None)
    return _pad(label + " " + V._present_field(cells, p.ax) + " "
                + chip(start, proj.due_date, p.today, p.chip_w), p.width)


def task_row(task, board, p, cursor=False) -> str:
    cells = V._gantt_bar(task, board, p.ax, p.chain, 0)
    if cursor:
        lo = next((x for x, (g, _) in enumerate(cells) if g != " "), None)
        hi = next((x for x in range(len(cells) - 1, -1, -1) if cells[x][0] != " "), None)
        if lo is not None and hi is not None:
            for x in range(lo, hi + 1):
                cells[x] = ("━", "accent")
            cells[lo], cells[hi] = ("⟦", "accent"), ("⟧", "accent")
    label = "  " + c("▎", p.hue) + " " + c(title_markup(task, max(0, p.label_w - 4), False),
                                           "bright", bold=True)
    return _pad(label + gantt_dep_mark(task, board, p.chain) + V._present_field(cells, p.ax)
                + " " + chip(task.start_date, task.due_date, p.today, p.chip_w), p.width)


def render_b2(board, project_id, cursor_id, today, width, height):
    """Variant B, round 2: the cursor ruler, start–end chips, hidden tasks out."""
    proj = board.project_by_id(project_id)
    open_t, tasks = shown_tasks(board, project_id)
    late, open_n, done = _present_counts(open_t, tasks, today)
    wide = width >= 100
    label_w, chip_w, field_w = cols(width, wide)
    ax = V._present_axis(board, proj, open_t, field_w, today)
    p = _PresentGeo(width, label_w, chip_w, field_w, ax, set(critical_chain(board)), today,
                    wide, proj.color)
    wanted = board.task_by_id(cursor_id)
    cursor = (wanted if wanted in open_t else open_t[0]) if open_t else None
    title = (c("◆ PRESENT", "bright", bold=True) + c(" · ", "dim")
             + c(escape(proj.name), proj.color, bold=True))
    right = c(f"{open_n} open", "mut") + c(" · ", "dim") \
        + (c(f"▲{late} past due", "over", bold=True) if late else c(f"{done} done", "done"))
    lines = [header(title, right, width)]
    lines += P._ruler_rows(p, board, proj, cursor, "B")
    lines.append(span_row(proj, board, p))
    for t in open_t:
        lines.append(task_row(t, board, p, cursor=cursor is not None and t.id == cursor.id))
    lines.append(_pad(c("─" * width, "frame"), width))
    for t in open_t:
        on = cursor is not None and t.id == cursor.id
        lines.append(_present_brief(t, p, on, width))
        if on:
            for ln in _present_note_lines(t.notes, width - 4, 3):
                lines.append(_present_note_row(ln, width, width - 4))
    return _present_finish(lines, height, width)


# --------------------------------------------------------------------------- #
# the screen: the shipped PresentScreen + two keys
# --------------------------------------------------------------------------- #
class PresentB2(app_mod.PresentScreen):
    BINDINGS = app_mod.PresentScreen.BINDINGS + [
        Binding("space", "toggle_shown", "Hide/show", priority=True),
        Binding("a", "show_all", "Show all", priority=True),
    ]

    def __init__(self, board, project_id, project_name, cursor_id):
        super().__init__(board, project_id, project_name, cursor_id)
        self._open_ids = [t.id for t in present_tasks(board, project_id)[0]]

    def _paint(self) -> None:
        w, h = self.size.width or 0, self._frame_height()
        self.query_one("#present-frame").update(
            render_b2(self._board, self._project_id, self._cursor_id, self._today, w, h))
        # the hidden count rides the hint row, NOT the frame: the frame is what the
        # room sees and what `x` exports, and a meeting should not read "2 hidden"
        hid = hidden_count(self._board, self._project_id)
        tail = f" · {hid} hidden" if hid else ""
        hint = ("←→ ↑↓ move · ␣ hide · a show all · x export · esc leave" if w >= 100
                else "←→ move · ␣ hide · a all · x export · esc")
        self.query_one("#present-hint").update(hint + tail)

    def action_move(self, delta: int) -> None:
        ids = [i for i in self._open_ids if shown(self._board.task_by_id(i))]
        if not ids:
            return
        i = ids.index(self._cursor_id) if self._cursor_id in ids else 0
        self._cursor_id = ids[max(0, min(len(ids) - 1, i + delta))]
        self._paint()

    def action_toggle_shown(self) -> None:
        t = self._board.task_by_id(self._cursor_id)
        if t is None:
            return
        ids = [i for i in self._open_ids if shown(self._board.task_by_id(i))]
        i = ids.index(t.id) if t.id in ids else 0
        t.extra["present"] = False
        rest = [x for x in ids if x != t.id]
        self._cursor_id = rest[min(i, len(rest) - 1)] if rest else None
        self._paint()

    def action_show_all(self) -> None:
        for i in self._open_ids:
            self._board.task_by_id(i).extra.pop("present", None)
        self._paint()


app_mod.PresentScreen = PresentB2
app_mod.date = _Today
models.date = _Today


async def run(size, steps, name) -> None:
    tmp = Path(tempfile.mkdtemp())
    board = pb.build(tmp / "board.json")
    board.save()
    app = app_mod.TaskboardApp(board_path=str(tmp / "board.json"))
    async with app.run_test(size=size) as pilot:
        for _ in range(50):
            if type(app.screen).__name__ == "MilestoneOffer":
                await pilot.press("escape")
                break
            await pilot.pause()
        await pilot.pause()
        app.selected_task_id = pb.CURSOR
        await pilot.press("R")
        await pilot.pause()
        for frame, keys in steps:
            for k in keys:
                await pilot.press(k)
            await pilot.pause()
            svg = app.export_screenshot(title=f"taskboard · R present · {frame}")
            (OUT / f"app-{name}-{frame}.svg").write_text(
                re.sub(r"@font-face\s*\{[^}]*\}", "", svg), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    big = [("1-open", []),
           ("2-cursor-moved", ["right", "right"]),            # → Launch new homepage
           ("3-hidden", ["left", "space"]),                    # hide Optimize image assets
           ("4-show-all", ["a"])]
    asyncio.run(run((118, 31), big, "118"))
    asyncio.run(run((80, 25), [("1-open", []), ("3-hidden", ["right", "space"])], "80"))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
