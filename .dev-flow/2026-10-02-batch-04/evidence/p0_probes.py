"""P0/P1 premise probes for batch 2026-10-02-batch-04 (Batch S), executed over the
working tree. Run from the repo root:  python -B .dev-flow/2026-10-02-batch-04/evidence/p0_probes.py
Prints no absolute path (the record must not leak the home directory)."""
from __future__ import annotations

import asyncio
import contextlib
import io
import json
import tempfile
from pathlib import Path

from rich.markup import escape
from textual.app import App
from textual.containers import Grid, VerticalScroll
from textual.markup import MarkupError
from textual.widgets import Label

PAYLOAD = "[LINK=http://e]x"


def p1_label_crash():
    """P-1: a Textual Label handed escape(payload) as a str raises MarkupError."""
    class A(App):
        def compose(self):
            yield Label(escape(PAYLOAD))

    async def run():
        try:
            async with A().run_test() as pilot:
                await pilot.pause()
            return "no error"
        except MarkupError as e:
            return f"MarkupError: {str(e)[:60]}"
        except Exception as e:  # the harness may wrap it
            return f"{type(e).__name__}: {str(e)[:60]}"
    sink = io.StringIO()     # Textual prints its traceback (with local paths): drop it
    with contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
        verdict = asyncio.run(run())
    print("P-1 Label(escape(payload)) ->", verdict)
    print("P-1 escape(payload) == payload ->", escape(PAYLOAD) == PAYLOAD)


def p2_rich_text_ok():
    """P-2: the same payload through modals._rich (Rich Text.from_markup over
    escaped text) builds a Text whose plain is the payload."""
    from taskboard.modals import _rich
    t = _rich(f"[b]{escape(PAYLOAD)}[/b]")
    print("P-2 _rich(...).plain == payload ->", t.plain == PAYLOAD)


def p3_controls_survive_load():
    """P-3: Board.load keeps ESC / C1 / BEL bytes in task text today."""
    from taskboard.models import Board
    d = Path(tempfile.mkdtemp())
    raw = {"phases": ["Backlog", "Doing", "Done"], "projects": [],
           "tasks": [{"id": "t1", "title": "a\x1b[31mred\x07", "phase": "Backlog",
                      "notes": "n\x9bx\tok\nline"}], "settings": {}}
    (d / "board.json").write_text(json.dumps(raw), encoding="utf-8")
    b = Board.load(d / "board.json")
    t = b.tasks[0]
    print("P-3 ESC kept in title ->", "\x1b" in t.title, "| BEL kept ->", "\x07" in t.title,
          "| C1 0x9b kept in notes ->", "\x9b" in t.notes)


def p4_controls_survive_sync():
    """P-4: TeamState.foreign_tasks keeps ESC in a teammate's title today."""
    from taskboard.team_sync import TeamState
    d = Path(tempfile.mkdtemp())
    (d / "board.ana.json").write_text(json.dumps(
        {"user": "ana", "tasks": [{"id": "f1", "title": "x\x1b]0;pwn\x07y"}]}), encoding="utf-8")
    ts = TeamState(d, user_id="me")
    ts.pull()
    titles = [t.title for t, _ in ts.foreign_tasks()]
    print("P-4 ESC kept in a synced title ->", any("\x1b" in s for s in titles))


def p5_grid_heights():
    """P-5: the shipped .modal-grid Label rule paints a Label-only grid with
    0-row cells (the TaskDetails info grid)."""
    css = (Path("taskboard") / "taskboard.tcss").read_text(encoding="utf-8")

    class A(App):
        CSS = css

        def compose(self):
            with VerticalScroll(classes="modal", id="details-box"):
                with Grid(classes="modal-grid"):
                    yield Label("Project")
                    yield Label("Alpha")

    async def run():
        async with A().run_test(size=(100, 30)) as pilot:
            await pilot.pause()
            return [w.region.height for w in pilot.app.query_one(Grid).children]
    print("P-5 grid label heights ->", asyncio.run(run()))


def p6_fix_forms_paint():
    """P-6: the fix forms paint the payload literally in textual 8.2.8 — a Rich
    Text in Label / Option / Select prompt / Button, and notify(markup=False)."""
    from rich.text import Text
    from textual.widgets import Button, OptionList, Select
    from textual.widgets.option_list import Option

    class A(App):
        def compose(self):
            yield Label(Text(PAYLOAD), id="l")
            yield OptionList(Option(Text(PAYLOAD), id="o"), id="ol")
            yield Select([(Text(PAYLOAD), "v")], value="v", allow_blank=False, id="s")
            yield Button(Text(PAYLOAD), id="b")

    async def run():
        async with A().run_test(size=(100, 30)) as pilot:
            await pilot.pause()
            await pilot.pause()
            strips = pilot.app.screen._compositor.render_strips(pilot.app.screen.size)
            painted = "\n".join(st.text for st in strips)
            return painted.count(PAYLOAD)
    sink = io.StringIO()
    with contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
        n = asyncio.run(run())
    print("P-6 payload painted literally, count over (label, option, select, button) ->", n)


def p7_notify_markup_off():
    """P-7: inside the taskboard app, notify(payload, markup=False) paints a
    Toast holding the payload; notify(escape(payload)) with markup on kills it."""
    from taskboard.app import TaskboardApp
    from taskboard.models import Board

    async def run(markup):
        d = Path(tempfile.mkdtemp())
        Board.load(d / "board.json")
        app = TaskboardApp(board_path=str(d / "board.json"), team_sync_interval=1e9)
        try:
            async with app.run_test(size=(120, 32), notifications=True) as pilot:
                await pilot.pause()
                if markup:
                    app.notify(escape(PAYLOAD))
                else:
                    app.notify(PAYLOAD, markup=False)
                for _ in range(3):
                    await pilot.pause()
                return [str(t.render()) for t in app.screen.query("Toast")]
        except Exception as e:
            return f"{type(e).__name__}"
    sink = io.StringIO()
    with contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
        off, on = asyncio.run(run(False)), asyncio.run(run(True))
    print("P-7 notify(markup=False) toasts ->", off)
    print("P-7 notify(escape(payload)) markup on ->", on)


if __name__ == "__main__":
    p1_label_crash()
    p2_rich_text_ok()
    p3_controls_survive_load()
    p4_controls_survive_sync()
    p5_grid_heights()
    p6_fix_forms_paint()
    p7_notify_markup_off()
