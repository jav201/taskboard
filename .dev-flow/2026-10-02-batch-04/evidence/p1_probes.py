"""P1 iteration-2 premise probes for batch 2026-10-02-batch-04 (P-11, P-12, P-13).
Run from the repo root:
    python -B .dev-flow/2026-10-02-batch-04/evidence/p1_probes.py pieces
    python -B .dev-flow/2026-10-02-batch-04/evidence/p1_probes.py sync
Prints no absolute path. P-12 re-runs the P2 security reviewer's S-1 probe (p_status.py)."""
from __future__ import annotations

import asyncio
import contextlib
import io
import json
import sys
import tempfile
from pathlib import Path

from rich.markup import escape
from rich.text import Text

PAYLOADS = ["[LINK=http://e]x", "x\\", ":smile: [b]y[/b]", "a\\\\", "x\\\\\\"]


def pieces():
    from taskboard.modals import _rich
    print("P-11 the escape-and-parse seat, title template `[b]{t}[/b]  —  esc`:")
    for p in PAYLOADS:
        got = _rich(f"[b]{escape(p)}[/b]  —  esc").plain
        want = f"{p}  —  esc"
        print(f"   {p!r:24} -> {got!r:34} exact={got == want}")
    print("P-13 Text pieces, Text.assemble((t, 'bold'), '  —  esc'):")
    for p in PAYLOADS:
        t = Text.assemble((p, "bold"), "  —  esc")
        bold_end = max(s.end for s in t.spans if str(s.style) == "bold")
        print(f"   {p!r:24} -> {t.plain!r:34} exact={t.plain == p + '  —  esc'}"
              f" style-only-on-piece={bold_end == len(p)}")


def sync():
    from textual.widgets import OptionList
    from taskboard.models import Board, Project
    from taskboard.team_sync import TeamState
    from taskboard.modals import ProjectPicker
    from textual.app import App
    from taskboard.views import render_view

    def board_after(entry):
        sd = Path(tempfile.mkdtemp())
        (sd / "team.json").write_text(json.dumps({
            "version": 2, "phases": ["Todo", "Doing", "Done"],
            "roster": [{"id": "a", "name": "A"}], "projects": [{"id": "p1", **entry}]}),
            encoding="utf-8")
        b = Board([], [], Path(tempfile.mkdtemp()) / "b.json")
        b.projects.append(Project(id="p1", name="Alpha"))
        ts = TeamState.from_settings(str(sd), "me")
        ts.load_config()
        ts.apply_config_to_board(b)
        return b

    hit = []

    class A(App):
        def __init__(self, b):
            super().__init__()
            self.b = b

        def action_pwn(self):
            hit.append("pwn")

        def on_mount(self):
            self.push_screen(ProjectPicker(self.b))

    async def click_status(b):
        app = A(b)
        async with app.run_test(size=(120, 30)) as pilot:
            await pilot.pause()
            ol = app.screen.query_one(OptionList)
            prompt = ol.get_option_at_index(0).prompt
            from textual.content import Content
            plain = prompt.plain if hasattr(prompt, "plain") else Content.from_markup(prompt).plain
            x = plain.index("X") if "X" in plain else 0
            for dx in range(3):
                for dy in range(3):
                    st = app.screen.get_style_at(ol.region.x + x + dx, ol.region.y + dy)
                    if st.meta.get("@click"):
                        await pilot.click(ol, offset=(x + dx, dy))
                        await pilot.pause()
                        return f"meta {st.meta.get('@click')!r} under the status; clicked"
            return "no @click meta under the status"

    b = board_after({"status": "[@click=app.pwn]X"})
    print("P-12 synced status applied ->", repr(b.projects[0].status))
    sink = io.StringIO()
    with contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
        try:
            note = asyncio.run(click_status(b))
        except Exception as e:
            note = f"crash {type(e).__name__}"
    print("P-12 project picker:", note, "| actions fired:", hit)
    for entry, label in (({"color": "evil"}, "colour 'evil'"), ({"name": 123}, "name 123")):
        b = board_after(entry)
        from taskboard.models import Task
        b.tasks.append(Task("t", "p1", "Todo", due_date="2026-10-09", start_date="2026-10-01"))
        out = []
        for mode in ("swimlanes", "agenda", "gantt", "kanban", "focus"):
            try:
                render_view(mode, b, False, None, width=100, height=30)
                out.append(f"{mode} ok")
            except Exception as e:
                out.append(f"{mode} {type(e).__name__}")
        print(f"P-12 {label} ->", ", ".join(out))


def roster():
    """P-15 (security S2-1, S2-2): roster names/hues and duplicate ids from a
    team.json, and an unhashable project colour, on base."""
    from taskboard.models import Board, Project, Task, project_color_on_load
    from taskboard.team_sync import TeamState
    from taskboard.views import render_view
    for entry, label in (({"id": "a", "name": "A", "hue": "evil"}, "roster hue 'evil'"),
                         ({"id": "a", "name": "A", "hue": []}, "roster hue []"),
                         ({"id": "a", "name": 123}, "roster name 123")):
        sd = Path(tempfile.mkdtemp())
        (sd / "team.json").write_text(json.dumps({"version": 2, "phases": ["Todo", "Done"],
                                                  "roster": [entry], "projects": []}), encoding="utf-8")
        b = Board([], [], Path(tempfile.mkdtemp()) / "b.json")
        ts = TeamState.from_settings(str(sd), "a")
        ts.load_config()
        out = []
        for mode in ("people", "standup", "setup"):
            try:
                render_view(mode, b, False, None, width=100, height=30, team_state=ts,
                            setup_state={"roster": [entry], "projects": [], "phases": ["Todo"]})
                out.append(f"{mode} ok")
            except Exception as e:
                out.append(f"{mode} {type(e).__name__}")
        print(f"P-15 {label} ->", ", ".join(out))
    sd = Path(tempfile.mkdtemp())
    (sd / "team.json").write_text(json.dumps({"version": 2, "phases": ["Todo", "Done"],
        "roster": [{"id": "a"}, {"id": "a"}],
        "projects": [{"id": "n1", "name": "X"}, {"id": "n1", "name": "Y"}]}), encoding="utf-8")
    b = Board([], [], Path(tempfile.mkdtemp()) / "b.json")
    ts = TeamState.from_settings(str(sd), "a")
    ts.load_config()
    ts.apply_config_to_board(b)
    print("P-15 duplicate project id n1 in team.json -> projects with id n1:",
          sum(p.id == "n1" for p in b.projects), "| roster entries with id a:",
          sum(r["id"] == "a" for r in ts.roster()))
    for col in ([], {}):
        try:
            project_color_on_load(col)
            print(f"P-15 project_color_on_load({col!r}) -> ok")
        except Exception as e:
            print(f"P-15 project_color_on_load({col!r}) -> {type(e).__name__}")


def history_error():
    """P-16 (qa Q2-1): the transition-log message when history.jsonl is a
    directory inside a board dir named `a[B]x` — the text the toast shows."""
    from taskboard import history
    from taskboard.models import Board
    root = Path(tempfile.mkdtemp()) / "a[B]x"
    root.mkdir()
    (root / "history.jsonl").mkdir()
    history.append(root / "board.json", {"task": "t", "from": "a", "to": "b"})
    msg = history.HISTORY_ERROR or ""
    tail = msg.split(":", 1)[0]
    print("P-16 HISTORY_ERROR exception type ->", tail,
          "| holds str(path):", str(root / "history.jsonl") in msg,
          "| holds repr(str(path)):", repr(str(root / "history.jsonl")) in msg,
          "| holds 'a[B]x':", "a[B]x" in msg)


if __name__ == "__main__":
    {"pieces": pieces, "sync": sync, "roster": roster, "history": history_error}[sys.argv[1]]()
