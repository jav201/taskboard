"""Inc C task captures: the SHIPPED app on a synthetic board, one scene per run.

    python scene.py live <scene> [seconds]     (a real terminal; used by shoot.ps1)
    python scene.py dump <scene> [WxH]         (headless: prints the end state + screen text)
    python scene.py html <out-dir>             (the workspace report for the same board)
Scenes: ed-pen palette details present.  Synthetic data only, owner `username_subject`.
"""
from __future__ import annotations

import asyncio
import json
import os
import shutil
import sys
import tempfile
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

from textual.widgets import TextArea  # noqa: E402

from taskboard import app as app_mod, models, modals, views  # noqa: E402
from taskboard.app import TaskboardApp  # noqa: E402
from taskboard.boards import Registry  # noqa: E402
from taskboard.models import LINKS_MIGRATION, MILESTONES_MIGRATION, Board, Project, Task  # noqa: E402

TODAY = date(2026, 11, 4)
PHASES = ["Backlog", "Next", "Doing", "Review", "Done"]
NOTES = ("::b:: ask the vendor for the store list ::\n"
         "::r:: blocker: 12 questions lack a key ::\n"
         "::g:: done: rubric draft :: and ::o:: later: cost per query ::\n"
         "::v:: idea: judge with two models :: \u2014 ==legacy yellow== still works")


class _Today(date):
    @classmethod
    def today(cls):
        return TODAY


for _m in (app_mod, models, views, modals):
    _m.date = _Today


def build(root: Path) -> Path:
    path = root / "board.json"
    projects = [Project(name="Eval harness", color="blue", start_date="2026-10-28",
                        due_date="2026-11-28", id="pce")]
    tasks = [Task(title="Sync notes", project_id="pce", phase="Doing", priority="High",
                  start_date="2026-11-02", due_date="2026-11-10", notes=NOTES,
                  phase_changed="2026-11-02", id="t1"),
             Task(title="Golden question set", project_id="pce", phase="Next", priority="Med",
                  start_date="2026-11-05", due_date="2026-11-12", notes="Review with the team",
                  phase_changed="2026-11-02", id="t2")]
    settings = {"migrations": {"links": LINKS_MIGRATION, "milestones": MILESTONES_MIGRATION},
                "seen_view_renumber_2026_07": True}
    Board(projects, tasks, path, settings, PHASES).save()
    (root / "boards.json").write_text(json.dumps({"version": 1, "last": "main", "boards": [
        {"id": "main", "name": "Personal", "color": "green", "path": str(path.resolve()),
         "last_opened": datetime.now().isoformat(timespec="minutes"), "archived": False}]},
        indent=2), encoding="utf-8")
    (root / "people.json").write_text(json.dumps({"version": 1, "people": [
        {"id": "username_subject", "name": "username_subject", "role": "Owner", "note": ""}]}),
        encoding="utf-8")
    (root / "marks.json").write_text(json.dumps({"version": 1, "marks": []}), encoding="utf-8")
    return path


def sel(app):
    app.selected_task_id = "t1"
    app.refresh_view()


def notes_end(app):
    ta = app.screen.query_one("#f-notes", TextArea)
    ta.focus()
    ta.move_cursor(ta.document.end)


def on_later(app):
    ta = app.screen.query_one("#f-notes", TextArea)
    ta.focus()
    for r, line in enumerate(ta.document.lines):
        c = line.find("later")
        if c >= 0:
            ta.move_cursor((r, c + 2))
            return
    raise RuntimeError("no 'later' in the notes")


def typed(s):
    return ["space" if ch == " " else ch for ch in s]


def ed_ok(app):
    s = app.screen
    ta = s.query_one("#f-notes", TextArea)
    return (type(s).__name__ == "TaskModal" and s.pen == 4
            and "::b:: new blue words ::" in ta.text)


SCENES = {
    "ed-pen": (["escape", sel, "e", notes_end, "alt+5"] + typed("new blue words"), ed_ok),
    "palette": (["escape", sel, "e", on_later, "alt+c"],
                lambda a: type(a.screen).__name__ == "ColourPalette"),
    "details": (["escape", sel, "enter"], lambda a: type(a.screen).__name__ == "TaskDetails"),
    "present": (["escape", sel, "R"], lambda a: type(a.screen).__name__ == "PresentScreen"),
}


class Scene(TaskboardApp):
    CSS_PATH = str(ROOT / "taskboard" / "taskboard.tcss")

    def __init__(self, scene, root, seconds=None):
        self.scene, self._seconds, self._root, self.played = scene, seconds, root, False
        build(root)
        reg = Registry.load(root / "boards.json", root / "board.json")
        entry = reg.opening()
        super().__init__(board_path=entry.path, registry=reg, team_sync_interval=1e9)

    def on_mount(self) -> None:
        if os.environ.get("PROTO_SHOT_TITLE"):
            self.title = os.environ["PROTO_SHOT_TITLE"]
        self.set_timer(1.0, lambda: self.run_worker(self.play()))

    async def play(self):
        await run_steps(self, SCENES[self.scene][0])
        self.played = True
        ready = os.environ.get("PROTO_READY_FILE")
        if ready:
            ok = SCENES[self.scene][1](self)
            Path(ready).write_text(f"{self._root}\n{'OK' if ok else 'BAD'} {self.screen_stack!r}",
                                   encoding="utf-8")
        if self._seconds:
            self.set_timer(self._seconds, self.exit)


async def run_steps(app, steps):
    for st in steps:
        if isinstance(st, str):
            await app._press_keys([st])
        elif isinstance(st, list):
            await app._press_keys(st)
        else:
            st(app)
        await asyncio.sleep(0.25)
    await asyncio.sleep(0.6)


def screen_text(app) -> str:
    return "\n".join("".join(seg.text for seg in strip)
                     for strip in app.screen._compositor.render_strips())


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "live":
        root = Path(tempfile.mkdtemp(prefix="cp-cap-"))
        try:
            Scene(a[1], root, float(a[2]) if len(a) > 2 else None).run()
        finally:
            shutil.rmtree(root, ignore_errors=True)
    elif a[0] == "dump":
        root = Path(tempfile.mkdtemp(prefix="cp-cap-"))
        w, h = (a[2] if len(a) > 2 else "118x30").split("x")
        app = Scene(a[1], root)

        async def go():
            async with app.run_test(size=(int(w), int(h))) as pilot:
                while not app.played:           # on_mount's timer plays the scene
                    await pilot.pause(0.3)
                print("STATE", "OK" if SCENES[a[1]][1](app) else "BAD", app.screen_stack)
                print(screen_text(app))
        try:
            asyncio.run(go())
        finally:
            shutil.rmtree(root, ignore_errors=True)
    elif a[0] == "html":
        from taskboard import report_html
        root = Path(tempfile.mkdtemp(prefix="cp-cap-"))
        try:
            p = build(root)
            b = Board.load(p)
            d = report_html.extract([("main", "Personal", "green", b)], {}, {}, TODAY)
            out = Path(a[1]); out.mkdir(parents=True, exist_ok=True)
            for f in report_html.write_reports(d, ("workspace",), out, TODAY):
                print(f)
        finally:
            shutil.rmtree(root, ignore_errors=True)
