"""THROWAWAY PROTOTYPE — kanban high-priority cue, five variants (sub-shape A).

The real TaskboardApp in the kanban view, with `taskboard.views.card_cell`,
`kanban_order` and `_kanban_column_rows` monkeypatched per variant. The real
renderer, real line_map, real nav — only the card / column rows change.

    python prototypes/kanban_priority/proto.py           live: 0-4 / ←→ (shift) switch
    python prototypes/kanban_priority/proto.py live K3 12  open K3, exit after 12 s
    python prototypes/kanban_priority/proto.py shot      SVGs + measurements -> out/

0 baseline · K1 franja · K2 tamaño · K3 insignia · K4 banda
Nothing here ships. Saves go to a temp copy of the fixture board.
"""
from __future__ import annotations

import asyncio
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))

from rich.markup import escape  # noqa: E402
from textual.binding import Binding  # noqa: E402

import fixture  # noqa: E402
import taskboard.views as V  # noqa: E402
from taskboard.app import TaskboardApp  # noqa: E402

fixture.pin_today()

VARIANTS = ["0", "K1", "K2", "K3", "K4"]
NAMES = {"0": "baseline", "K1": "franja", "K2": "tamaño", "K3": "insignia",
         "K4": "banda"}
STATE = {"v": "0"}

_card_cell = V.card_cell
_kanban_order = V.kanban_order
_column_rows = V._kanban_column_rows
c, fit, HEX = V.c, V.fit, V.HEX

BAND = "\x00high"          # the pseudo-group K4 floats high cards into


def _shouts(task, board) -> bool:
    """Only LIVE high work carries the cue — done/archived work rests."""
    return (task.priority == "high" and not board.is_done(task)
            and not task.archived)


def card_cell(task, board, wc, selected, *, prefix="", prefix_color="mut",
              allow_priority=True, today=None, unblocks=None, readonly=False):
    v = STATE["v"]
    kw = dict(today=today, unblocks=unblocks, readonly=readonly)
    if v == "0" or not _shouts(task, board) or wc < 6:
        return _card_cell(task, board, wc, selected, prefix=prefix,
                          prefix_color=prefix_color,
                          allow_priority=allow_priority, **kw)
    if v == "K1":
        # the identity stripe keeps its project hue, the SPACE after it becomes
        # a heavy ink half-block: ▊▌ — zero title cells spent — and the title
        # goes bold-bright. The `!` token is dropped (the edge already says it).
        body = _card_cell(task, board, wc - len(prefix), selected, prefix="",
                          allow_priority=False, **kw)
        pre = (c(prefix[:1], prefix_color) + c("▌", "ink", bold=True)
               if prefix else "")
        return pre + f"[b {HEX['bright']}]" + body + "[/]"
    if v == "K3":
        # reverse-video rose badge right after the stripe; costs 4 cells
        badge = f"[b reverse {HEX['rose']}]!![/]" + " "
        body = _card_cell(task, board, wc - len(prefix) - 3, selected, prefix="",
                          allow_priority=False, **kw)
        return c(prefix, prefix_color) + badge + body
    # K2 / K4: the shipped card (with its ink `!`)
    return _card_cell(task, board, wc, selected, prefix=prefix,
                      prefix_color=prefix_color, allow_priority=allow_priority, **kw)


def kanban_order(board, tasks, show_archived, **kw):
    groups = _kanban_order(board, tasks, show_archived, **kw)
    if STATE["v"] != "K4" or not groups:
        return groups
    # K4: live high cards float out of their groups into one band at the top.
    # Routed through THE ordering seat, so nav follows the screen.
    high = [t for _n, _c, items in groups for t in items if _shouts(t, board)]
    if not high:
        return groups
    rest = [(n, col, [t for t in items if not _shouts(t, board)])
            for n, col, items in groups]
    return [(BAND, "ink", high)] + [g for g in rest if g[2]]


def _kanban_column_rows(board, tasks, wc, selected_id, show_archived, *,
                        group="project", sort="project", collapsed=False,
                        focus=None, today=None, unblocks=None):
    v = STATE["v"]
    if v not in ("K2", "K4"):
        return _column_rows(board, tasks, wc, selected_id, show_archived,
                            group=group, sort=sort, collapsed=collapsed,
                            focus=focus, today=today, unblocks=unblocks)
    rows = []
    for name, color, items in V.kanban_order(board, tasks, show_archived,
                                             group=group, sort=sort,
                                             collapsed=collapsed, focus=focus,
                                             today=today):
        if name == BAND:
            label = " high "
            side = max(0, wc - len(label) - 2)
            rows.append((c("──", "dim") + c(label, "ink", bold=True)
                         + c("─" * side, "dim"), None))
        else:
            rows.append((c("▐ ", color) + c(escape(fit(name, max(0, wc - 2))),
                                            color, bold=True), None))
        for t in items:
            pc = "over" if t.blocked else V.project_color(board, t)
            rows.append((V.card_cell(t, board, wc, t.id == selected_id,
                                     prefix="▲ " if t.blocked else "▊ ",
                                     prefix_color=pc, today=today,
                                     unblocks=unblocks), t.id))
            if v == "K2" and _shouts(t, board):
                rows.append((_second_line(t, board, wc, pc, today,
                                          t.id == selected_id), None))
        if name == BAND:
            rows.append((c("─" * wc, "dim"), None))
    if collapsed:
        rows.append((c(fit(f"✓ {len(tasks)}", wc), "done"), None))
    return rows


def _second_line(t, board, wc, pc, today, selected) -> str:
    """K2's second row: the stripe continues under the card with the first
    note line (the countdown already rides row one); undated-note cards fall
    back to the date chip so the row is never empty."""
    inner = wc - 2
    left, used = "", 0
    if not (t.notes or "").strip():
        chip, tone = V.date_chip(t, today, board)
        chip = fit(chip, min(len(chip), inner)) if chip else ""
        left, used = c(escape(chip), tone), len(chip)
    note = V._focus_note_snippet(t.notes, max(0, inner - used)) if t.notes else ""
    note_w = V.vis(V._strip(note)) if note else 0
    pad = " " * max(0, inner - used - note_w)
    body = left + note + pad
    if selected:
        body = f"[reverse]{body}[/reverse]"
    return c("▊ ", pc) + body


V.card_cell = card_cell
V.kanban_order = kanban_order
V._kanban_column_rows = _kanban_column_rows


class KanbanProto(TaskboardApp):
    CSS_PATH = str(ROOT / "taskboard" / "taskboard.tcss")   # the REAL stylesheet
    BINDINGS = [Binding(k, f"variant({i})", k, priority=True)
                for i, k in enumerate("01234")] + [
        Binding("shift+left", "cycle(-1)", "prev", priority=True),
        Binding("shift+right", "cycle(1)", "next", priority=True),
    ]

    def __init__(self, variant: str = "0", seconds: float | None = None):
        super().__init__(board_path=fixture.write_board(), team_sync_interval=1e9)
        STATE["v"] = variant
        self._seconds = seconds

    def on_mount(self) -> None:
        super().on_mount()
        if os.environ.get("PROTO_SHOT_TITLE"):
            self.title = os.environ["PROTO_SHOT_TITLE"]
        self.view_mode = "kanban"
        self.selected_task_id = "t11"        # a NORMAL card: reverse ≠ the cue
        self.refresh_view()
        if self._seconds:
            self.set_timer(self._seconds, self.exit)

    def check_action(self, action, parameters):
        if action in ("variant", "cycle") and len(self.screen_stack) > 1:
            return False
        return super().check_action(action, parameters)

    def action_variant(self, i: int) -> None:
        STATE["v"] = VARIANTS[i]
        self.notify(f"{VARIANTS[i]} · {NAMES[VARIANTS[i]]}", timeout=1.5)
        self.refresh_view()

    def action_cycle(self, d: int) -> None:
        self.action_variant((VARIANTS.index(STATE["v"]) + d) % len(VARIANTS))


# ---------------------------------------------------------------------------
# measurement + shot
# ---------------------------------------------------------------------------
def measure(width: int, height: int) -> dict:
    """Render the board the way the app does and count what the cue costs."""
    b = V.Board.load(fixture.write_board())
    lm: dict = {}
    text = V.render_kanban(b, False, "t11", today=fixture.TODAY, width=width,
                           height=height, line_map=lm)
    lines = text.plain.split("\n")
    body = [ln for ln in lines if ln.strip()]
    high = [t for t in b.tasks if _shouts(t, b)]
    title_chars = {}
    for t in high:
        row = lines[lm[t.id]] if t.id in lm else ""
        segs = row.split("│")                     # the phase-column separator
        pi = b.phase_index(t)
        row = segs[pi] if pi < len(segs) else row
        k = 0
        while k < len(t.title) and t.title[:k + 1] in row:
            k += 1
        title_chars[t.id] = k
    return {"board_rows": len(body), "high_open": len(high),
            "high_title_chars": title_chars,
            "nav_ids_in_line_map": len(lm)}


def _shot() -> None:
    out = HERE / "out"
    out.mkdir(exist_ok=True)
    facts: dict = {}

    async def run(v: str, size: tuple[int, int]) -> None:
        app = KanbanProto(variant=v)
        async with app.run_test(size=size) as pilot:
            for _ in range(3):
                await pilot.pause()
            app.refresh_view()
            await pilot.pause(0.2)
            name = f"kanban_{v}_{size[0]}x{size[1]}.svg"
            app.save_screenshot(filename=name, path=str(out))
            facts[f"{v}-{size[0]}"] = measure(size[0], size[1] - 2)
            print(name, facts[f"{v}-{size[0]}"])

    for v in VARIANTS:
        for size in ((120, 36), (80, 24)):
            asyncio.run(run(v, size))
    (out / "facts_kanban.json").write_text(json.dumps(facts, indent=2), encoding="utf-8")


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "shot":
        _shot()
    elif args and args[0] == "live":
        v = args[1] if len(args) > 1 else "0"
        secs = float(args[2]) if len(args) > 2 else None
        KanbanProto(variant=v, seconds=secs).run()
    else:
        KanbanProto().run()
