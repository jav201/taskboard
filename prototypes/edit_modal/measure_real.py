"""Measurement harness for batch 2026-09-30-batch-01 — the REAL app, no patches.

Run before and after the change; prints one JSON document:

    python prototypes/edit_modal/measure_real.py > out.json

edit window: notes rows visible (TextArea content region clipped by the
compositor), notes width, title/save visibility with focus in the notes,
for the round's 23-line fixture task at 120x36 and 80x24.
kanban: board rows and visible title characters per open card at 120/80.
Throwaway harness (not shipped); the assertions live in tests/.
"""
from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "prototypes" / "kanban_priority"))

import fixture  # noqa: E402

fixture.pin_today()

from textual.widgets import TextArea  # noqa: E402

from taskboard import views as V  # noqa: E402
from taskboard.app import TaskboardApp  # noqa: E402
from taskboard.modals import TaskModal  # noqa: E402


def _visible(scr, widget) -> bool:
    vis = scr._compositor.visible_widgets
    if widget not in vis:
        return False
    region, clip = vis[widget]
    return region.intersection(clip).area == region.area and region.area > 0


async def edit_facts(size):
    app = TaskboardApp(board_path=str(fixture.write_board()), team_sync_interval=1e9)
    async with app.run_test(size=size) as pilot:
        await pilot.pause()
        task = app.board.task_by_id(fixture.LONG_TASK_ID)
        app.push_screen(TaskModal(app.board, task))
        for _ in range(4):
            await pilot.pause()
        scr = app.screen
        ta = scr.query_one("#f-notes", TextArea)
        ta.focus()
        ta.move_cursor(ta.document.end)
        for _ in range(3):
            await pilot.pause()
        vis = scr._compositor.visible_widgets
        rows = cols = 0
        if ta in vis:
            region, clip = vis[ta]
            content = region.shrink(ta.styles.gutter).intersection(clip)
            rows, cols = content.height, content.width
        out = {"notes_rows_visible": rows, "notes_cols": cols,
               "title_fully_visible": _visible(scr, scr.query_one("#f-title")),
               "save_fully_visible": _visible(scr, scr.query_one("#save"))}
        for wid in ("f-project", "f-phase", "f-priority", "f-start", "cal-f-start",
                    "f-due", "cal-f-due", "f-blocked", "f-archived", "f-pinned",
                    "f-urls", "f-images", "paste-img", "cancel"):
            out.setdefault("controls_fully_visible", {})[wid] = _visible(
                scr, scr.query_one(f"#{wid}"))
        return out


def kanban_facts(width, height):
    b = V.Board.load(fixture.write_board())
    lm: dict = {}
    text = V.render_kanban(b, False, "t11", today=fixture.TODAY, width=width,
                           height=height, line_map=lm)
    lines = text.plain.split("\n")
    chars = {}
    for t in b.tasks:
        if t.id not in lm or b.is_done(t):
            continue
        segs = lines[lm[t.id]].split("│")
        pi = b.phase_index(t)
        row = segs[pi] if pi < len(segs) else ""
        k = 0
        while k < len(t.title) and t.title[:k + 1] in row:
            k += 1
        chars[t.id] = {"priority": t.priority, "title_chars": k}
    body = [ln for ln in lines if ln.strip()]
    return {"board_rows": len(body), "open_cards": chars,
            "ids_in_line_map": len(lm)}


def main():
    facts = {"edit": {}, "kanban": {}}
    for size in ((120, 36), (80, 24)):
        facts["edit"][f"{size[0]}x{size[1]}"] = asyncio.run(edit_facts(size))
        facts["kanban"][f"{size[0]}x{size[1]}"] = kanban_facts(size[0], size[1] - 2)
    print(json.dumps(facts, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
