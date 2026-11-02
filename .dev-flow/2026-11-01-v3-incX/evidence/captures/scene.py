"""Inc X captures (E13): the SHIPPED app - key bar `H`, `R` + `x` toast, presentation `?` - on a synthetic registry.

    python scene.py live <scene> [seconds]     (a real terminal; used by shoot.ps1)
    python scene.py dump <scene> [WxH]         (headless: prints the end state + screen text)
Scenes: xh-bar xh-bar-wide xh-toast xh-keys; `deck <outdir>` writes the view-3 deck with one project hidden.
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
    p3 = Project("Quasar Hidden", "red", id="p3", show_in_present=False)
    work_tasks += [Task("Quasar secret task", project_id="p3", phase="Doing", id="w5",
                        urls=["https://hidden.example.org/quasar"])]
    work_tasks[2].created = "2026-10-31T18:20:00"
    work_tasks[3].created = "2026-10-30T09:00:00"
    Board([p1, p3], work_tasks, wp, dict(SETTINGS), ["Backlog", "Doing", "Review", "Done"]).save()
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


def toast_text(app) -> str:
    return "\n".join(str(n.message) for n in app._notifications)


def bar_ok(app):
    t = list_text(app)
    return type(app.screen).__name__ == "Screen" and " H " in t.split("\n")[-1]


def toast_ok(app):
    return type(app.screen).__name__ == "PresentScreen" and "present-" in toast_text(app)         and ".html" in toast_text(app) and "o opens it" in toast_text(app)


def keys_ok(app):
    t = list_text(app)
    return type(app.screen).__name__ == "PresentKeys" and "HTML deck" in t and "open the last export" in t


SCENES = {
    "xh-bar": (["enter", "escape"], bar_ok),
    "xh-bar-wide": (["enter", "escape"], lambda app: "H Report" in list_text(app)),
    "xh-toast": (["enter", "escape", "R", "x"], toast_ok),
    "xh-keys": (["enter", "escape", "R", "question_mark"], keys_ok),
}


def cursor_title(app) -> str:
    return type(app.screen).__name__


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
        await asyncio.sleep(1.5)
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
        if a[0] == "deck":
            sc = Scene("xh-toast", root)
            sc.scene = "deck"
            SCENES["deck"] = (["enter", "escape", "R", "3", "x"], lambda app: True)

            async def godeck():
                async with sc.run_test(size=(140, 40)) as pilot:
                    while not sc.played:
                        await pilot.pause(0.3)
                    print("SCREEN", type(sc.screen).__name__, "view3?", getattr(sc.screen, "_view", None))
                    print(toast_text(sc))
                    reps = list((root / ".taskboard" / "boards" / "work" / "reports").glob("present-*.html"))
                    print("FILES", [r.name for r in reps])
                    Path(a[1]).mkdir(parents=True, exist_ok=True)
                    shutil.copy(reps[0], Path(a[1]) / reps[0].name)
            asyncio.run(godeck())
        elif a[0] == "live":
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
