"""P1 premise probes for batch 2026-10-04-batch-01 (B1: links). Synthetic boards only.

    PYTHONIOENCODING=utf-8 python .dev-flow/2026-10-04-batch-01/evidence/p1_premises.py

Every board here is built in a fresh temp directory; nothing reads or writes a
user data directory. Output: one section per premise, its observed values.
"""
from __future__ import annotations

import asyncio
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))

import kg_board  # noqa: E402
from rich.text import Text  # noqa: E402
from textual.app import App  # noqa: E402
from textual.widgets import OptionList  # noqa: E402
from textual.widgets.option_list import Option  # noqa: E402

from taskboard.app import TaskboardApp  # noqa: E402
from taskboard.keymap import KEYMAP  # noqa: E402
from taskboard.models import Board  # noqa: E402
from taskboard.views import card_cell, gantt_dep_mark, kanban_card  # noqa: E402


def key(action: str) -> str:
    return next(k for k in KEYMAP if k.action == action).keys.split(",")[0]


def strip(markup: str) -> str:
    return Text.from_markup(markup).plain


def board_in(tmp: Path) -> Board:
    b = kg_board.build(tmp / "board.json")
    b.save()
    return b


async def p1_block_flow(tmp: Path) -> None:
    print("## P-1  `b` writes blocked=True AND appends the picked id; unblock keeps the id")
    b = board_in(tmp)
    app = TaskboardApp(board_path=str(b.path))
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.press("4")
        await pilot.pause()
        app.selected_task_id = "to4"                 # Update onboarding copy, no links
        await pilot.press(key("toggle_blocked"))
        await pilot.pause()
        print("   screen after b:", type(app.screen).__name__)
        ol = app.screen.query_one(OptionList)
        ol.highlighted = 1
        await pilot.press("enter")
        await pilot.pause()
        t = app.board.task_by_id("to4")
        print("   after pick: blocked =", t.blocked, "depends_on =", t.depends_on)
        await pilot.press(key("toggle_blocked"))
        await pilot.pause()
        t = app.board.task_by_id("to4")
        print("   after b again: blocked =", t.blocked, "depends_on =", t.depends_on)


async def p3_archive_delete(tmp: Path) -> None:
    print("## P-3  archive `x` and delete `d` of an OPEN task that an open task waits on succeed (no guard)")
    b = board_in(tmp)
    app = TaskboardApp(board_path=str(b.path))
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.press("4")
        await pilot.pause()
        app.selected_task_id = "ta3"                 # Partner notice emails; ta2 waits on it
        await pilot.press(key("archive"))
        await pilot.pause()
        print("   ta3 archived after x:", app.board.task_by_id("ta3").archived)
        app.selected_task_id = "tm2"                 # Audit dependencies; tm3 waits on it
        await pilot.press(key("delete"))
        await pilot.pause()
        print("   screen after d:", type(app.screen).__name__)
        await pilot.click("#yes")
        await pilot.pause()
        print("   tm2 present after d + yes:", app.board.task_by_id("tm2") is not None,
              "· tm3.depends_on =", app.board.task_by_id("tm3").depends_on)


def p2_marks(tmp: Path) -> None:
    print("## P-2  shipped marks: ⛓N on the predecessor only; nothing on the waiting card")
    from datetime import date
    b = kg_board.build(tmp / "b2.json")
    today = kg_board.TODAY
    for tid in ("tm2", "tm3", "tw5", "ta2"):
        r1, r2 = kanban_card(b.task_by_id(tid), b, 24, False, today=today)
        print(f"   kanban {tid}: {strip(r1)!r} / {strip(r2)!r}")
    print("   card_cell tm2:", repr(strip(card_cell(b.task_by_id("tm2"), b, 40, False, today=today))))
    b.task_by_id("ta3").archived = True
    print("   gantt_dep_mark ta2 with its only predecessor ARCHIVED:",
          repr(strip(gantt_dep_mark(b.task_by_id("ta2"), b, set()))))
    t = b.task_by_id("tw5")          # start +4, preds tw2 due -3, tw4 due +6
    b.task_by_id("tw4").due_date = t.start_date
    print("   gantt_dep_mark tw5 starting ON tw4's due day:",
          repr(gantt_dep_mark(t, b, set())), "(over = conflict)")
    _ = date


async def p5_details(tmp: Path) -> None:
    print("## P-5  the details view shows no dependency (enter on a waiting task)")
    b = board_in(tmp)
    app = TaskboardApp(board_path=str(b.path))
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.press("4")
        await pilot.pause()
        app.selected_task_id = "tm3"
        await pilot.press("enter")
        await pilot.pause()
        painted = "\n".join(
            "".join(seg.text for seg in strip_line)
            for strip_line in [app.screen._compositor.render_update(full=True)] if False)
        texts = [str(w.render()) for w in app.screen.query("Label")]
        print("   screen:", type(app.screen).__name__, "· any label holding 'Audit dependencies':",
              any("Audit dependencies" in s for s in texts), "· 'Waits on':",
              any("Waits on" in s for s in texts))


async def p8_optionlist() -> None:
    print("## P-8  OptionList paints a two-line Text prompt, and a disabled option is skipped by the cursor")

    class Probe(App):
        def compose(self):
            yield OptionList(
                Option(Text.assemble(("Same project", "bold")), disabled=True),
                Option(Text("row one [b]x[/b]\n    second line"), id="a"),
                Option(Text("looping row"), id="loop", disabled=True),
                Option(Text("row three"), id="c"))

    app = Probe()
    async with app.run_test(size=(60, 12)) as pilot:
        ol = app.query_one(OptionList)
        ol.focus()
        ol.highlighted = 1
        await pilot.press("down")
        await pilot.pause()
        hi = ol.get_option_at_index(ol.highlighted).id
        print("   highlighted after down from 'a':", hi, "(expected c: the disabled row skipped)")
        print("   option count:", ol.option_count, "· prompt 1 plain:", repr(ol.get_option_at_index(1).prompt.plain))


def p10_undo_shape() -> None:
    print("## P-10 the undo stack holds ONE task per entry (app.py _snapshot)")
    import inspect
    from taskboard.app import TaskboardApp as A
    src = inspect.getsource(A._snapshot)
    print("   _snapshot returns {'task_id', 'fields'[, 'task', 'index']}:",
          '"task_id": task.id' in src and '"fields": fields' in src)
    print("   _UNDO_FIELDS =", A._UNDO_FIELDS)


async def main() -> None:
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        for i, fn in enumerate((p1_block_flow, p3_archive_delete, p5_details)):
            sub = root / f"r{i}"
            sub.mkdir()
            await fn(sub)
        sub = root / "m"
        sub.mkdir()
        p2_marks(sub)
        await p8_optionlist()
        p10_undo_shape()


if __name__ == "__main__":
    asyncio.run(main())
