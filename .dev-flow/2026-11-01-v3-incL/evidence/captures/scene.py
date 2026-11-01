"""Inc L task captures: the SHIPPED app, list view `N`, on a synthetic two-board registry.

    python scene.py live <scene> [seconds]     (a real terminal; used by shoot.ps1)
    python scene.py dump <scene> [WxH]         (headless: prints the end state + screen text)
Scenes: ls-newest ls-oldest ls-archived ls-pane ls-inferred ls-unknown.
Synthetic data only, owner `username_subject`. Path.home is redirected to a temp folder.
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

from taskboard import app as app_mod, modals, models, views  # noqa: E402
import taskboard.__main__ as entry  # noqa: E402
from taskboard.models import LINKS_MIGRATION, MILESTONES_MIGRATION, Board, Project, Task  # noqa: E402

TODAY = date(2026, 11, 1)
NOW = datetime(2026, 11, 1, 8, 10, 0)


class _Today(date):
    @classmethod
    def today(cls):
        return TODAY


class _Now(datetime):
    @classmethod
    def now(cls, tz=None):
        return NOW


for _m in (app_mod, models, views, modals):
    _m.date = _Today
for _m in (app_mod, entry, models):
    _m.datetime = _Now

SETTINGS = {"migrations": {"links": LINKS_MIGRATION, "milestones": MILESTONES_MIGRATION},
            "seen_view_renumber_2026_07": True}
NOTES = ("Sync notes, 3 pens\n::y:: decided: 400-token chunks ::\n"
         "::r:: blocker: 12 questions lack a key ::\n::g:: done: rubric draft ::\n"
         "::b:: ask the vendor for the store list ::")


def build(home_root: Path) -> None:
    """Write the registry under `<home_root>/.taskboard` (= Path.home()/.taskboard)."""
    home = home_root / ".taskboard"
    wp, hp = home / "boards" / "work" / "board.json", home / "boards" / "home" / "board.json"
    for p in (wp, hp):
        p.parent.mkdir(parents=True, exist_ok=True)
    p1 = Project("Eval harness", "blue", id="p1")
    work_tasks = [
        Task("Volume oracle script", project_id="p1", phase="Backlog", id="w1"),
        Task("Pilot store list", project_id="p1", phase="Backlog", id="w2"),
        Task("Sync notes", project_id="p1", phase="Review", priority="high",
             due_date="2026-11-03", urls=["https://example.com/spec"], notes=NOTES, id="w3"),
        Task("Archived memo", project_id="p1", phase="Done", archived=True, id="w4"),
    ]
    work_tasks[2].created = "2026-10-31T18:20:00"
    work_tasks[3].created = "2026-10-30T09:00:00"
    Board([p1], work_tasks, wp, dict(SETTINGS), ["Backlog", "Doing", "Review", "Done"]).save()
    (wp.parent / "history.jsonl").write_text(json.dumps(
        {"task": "w2", "from": None, "to": "Backlog", "at": "2026-10-28T10:30:00"}) + "\n",
        encoding="utf-8")
    p2 = Project("House", "green", id="p2")
    home_tasks = [Task("Pay the rent", project_id="p2", phase="Done", id="h1"),
                  Task("Week 3 plan", project_id="p2", phase="Doing", id="h2")]
    home_tasks[0].created = "2026-11-01T08:10:00"
    home_tasks[1].created = "2026-10-31T21:47:00"
    Board([p2], home_tasks, hp, dict(SETTINGS), ["Backlog", "Doing", "Done"]).save()
    entries = [{"id": "work", "name": "Work", "color": "sky", "path": str(wp.resolve()),
                "last_opened": "2026-11-01T07:00", "archived": False},
               {"id": "home", "name": "Home", "color": "lime", "path": str(hp.resolve()),
                "last_opened": "2026-10-31T20:00", "archived": False}]
    (home / "boards.json").write_text(json.dumps({"version": 1, "last": "work", "boards": entries},
                                                 indent=2), encoding="utf-8")
    (home / "people.json").write_text(json.dumps({"people": [
        {"id": "username_subject", "name": "username_subject"}]}), encoding="utf-8")


def list_text(app) -> str:
    return "\n".join("".join(seg.text for seg in strip)
                     for strip in app.screen._compositor.render_strips())


def cursor_title(app) -> str:
    for line in list_text(app).split("\n"):
        if "▶" in line and "▍" in line:
            return line.split("▍", 1)[1].split("│")[0].strip()
    return ""


def check(title, head=None):
    def f(app):
        if type(app.screen).__name__ != "AddedList":
            return False
        txt = list_text(app)
        if head and head not in txt:
            return False
        return title is None or cursor_title(app) == title
    return f


D = "down"
SCENES = {
    "ls-newest": (["escape", "N"], check("Pay the rent", "1 archived hidden")),
    "ls-oldest": (["escape", "N", "o"], check("Volume oracle script", "1 archived hidden")),
    "ls-archived": (["escape", "N", "v", D, D, D], check("Archived memo", "archived shown")),
    "ls-pane": (["escape", "N", D, D], check("Sync notes")),
    "ls-inferred": (["escape", "N", D, D, D], check("Pilot store list")),
    "ls-unknown": (["escape", "N", D, D, D, D], check("Volume oracle script")),
}


class Scene(entry.TaskboardApp):
    CSS_PATH = str(ROOT / "taskboard" / "taskboard.tcss")

    def __init__(self, scene, root, seconds=None):
        self.scene, self._seconds, self._root, self.played = scene, seconds, root, False
        build(root)
        Path.home = classmethod(lambda cls: root)
        from taskboard.boards import Registry
        from taskboard.boards import registry_path
        from taskboard.models import default_board_path
        reg = Registry.load(registry_path(), default_board_path())
        e = reg.opening()
        reg.touch(e.id, NOW)
        super().__init__(board_path=e.path, registry=reg)

    def on_mount(self) -> None:
        super().on_mount()
        if os.environ.get("PROTO_SHOT_TITLE"):
            self.title = os.environ["PROTO_SHOT_TITLE"]
        self.set_timer(1.0, lambda: self.run_worker(self.play()))

    async def play(self):
        app = self
        await run_steps(app, SCENES[self.scene][0])
        self.played = True
        ready = os.environ.get("PROTO_READY_FILE")
        if ready:
            ok = SCENES[self.scene][1](app)
            Path(ready).write_text(f"{self._root}\n{'OK' if ok else 'BAD'} {cursor_title(app)!r}",
                                   encoding="utf-8")
        if self._seconds:
            app.set_timer(self._seconds, app.exit)


async def run_steps(app, steps):
    for st in steps:
        await app._press_keys([st])
        await asyncio.sleep(0.3)
    await asyncio.sleep(0.6)


if __name__ == "__main__":
    a = sys.argv[1:]
    root = Path(tempfile.mkdtemp(prefix="cp-cap-"))
    try:
        if a[0] == "live":
            Scene(a[1], root, float(a[2]) if len(a) > 2 else None).run()
        else:
            w, h = (a[2] if len(a) > 2 else "118x30").split("x")
            sc = Scene(a[1], root)

            async def go():
                async with sc.run_test(size=(int(w), int(h))) as pilot:
                    while not sc.played:
                        await pilot.pause(0.3)
                    print("STATE", "OK" if SCENES[a[1]][1](sc) else "BAD", repr(cursor_title(sc)))
                    print(list_text(sc))
            asyncio.run(go())
    finally:
        shutil.rmtree(root, ignore_errors=True)
