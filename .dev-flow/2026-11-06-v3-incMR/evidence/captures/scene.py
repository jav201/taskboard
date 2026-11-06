"""Inc MR captures (E13): the SHIPPED board gantt with one milestone row per project, driven by real keys.

    python scene.py live <scene> [seconds]     (a real terminal; used by shoot.ps1)
    python scene.py dump <scene> [WxH]         (headless: end state + width check + screen text)
Scenes: mri-rest, mri-sel (up, right, right), mri-hidden (class Review hidden, cursor walks m1 -> m4),
mri-hostile (a milestone titled `[@click=app.quit]x`). Fixture: tests/milestone_row_fixture.py (MR-F).
Synthetic data only. Path.home is redirected to a temp folder.
"""
from __future__ import annotations

import asyncio
import os
import shutil
import sys
import tempfile
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))

import milestone_row_fixture as fx  # noqa: E402
from rich.cells import cell_len  # noqa: E402
from taskboard import app as app_mod, models, views  # noqa: E402

TODAY = fx.TODAY


class _Today(date):
    @classmethod
    def today(cls):
        return TODAY


for _m in (app_mod, models, views):
    _m.date = _Today

HOSTILE = "[@click=app.quit]x"
EXTRA = {"mri-hostile": [fx.task("hx", "pd", HOSTILE, "Backlog", None, 5, ms=True, mark="delivery")]}


def lines(app):
    return ["".join(seg.text for seg in strip)
            for strip in app.screen._compositor.render_strips()]


def width_ok(app):
    w = app.size.width
    return all(cell_len(l) <= w for l in lines(app))


async def play(app, scene):
    p = app._press_keys

    async def k(*ks):
        for x in ks:
            await p([x])
            await asyncio.sleep(0.3)
    await asyncio.sleep(1.5)
    await k("escape", "3")
    app.selected_task_id = "tstore"                  # as the fixture's gantt(): the cursor on a task row
    app.refresh_view()
    await asyncio.sleep(0.4)
    if scene == "mri-rest":
        ok = app.selected_task_id == "tstore"
    elif scene == "mri-sel":
        await k("up", "right", "right")
        ok = app.selected_task_id == "tm5"
    elif scene == "mri-hidden":
        await k("number_sign", "down", "down", "space", "escape")      # Review is the 3rd class
        for _ in range(6):
            if app.selected_task_id in fx.PILOT_MS:
                break
            await k("up")
        for _ in range(5):
            await k("left")
        assert app.selected_task_id == "tm1", app.selected_task_id
        await k("right")
        ok = app.selected_task_id == "tm4"        # tm3 (Review) skipped
        txt = "\n".join(lines(app))
        ok = ok and "■" not in txt.split("Pilot rollout")[1].split("\n")[1]
    else:
        for _ in range(30):
            if app.selected_task_id == "thx":
                break
            await k("down")
        ok = app.selected_task_id == "thx" and HOSTILE[:15] in "\n".join(lines(app))
    await asyncio.sleep(0.6)
    return ok and width_ok(app), f"sel={app.selected_task_id} width_ok={width_ok(app)}"


def make(scene, root, seconds=None):
    fx.build(root / ".taskboard", extra=EXTRA.get(scene, ()))
    Path.home = classmethod(lambda cls: root)
    from taskboard.__main__ import open_app
    app = open_app(None)
    orig = type(app).on_mount

    def on_mount(self):
        orig(self)
        if os.environ.get("PROTO_SHOT_TITLE"):
            self.title = os.environ["PROTO_SHOT_TITLE"]

        async def go():
            ok, info = await play(self, scene)
            self.played = True
            self.result = (ok, info)
            ready = os.environ.get("PROTO_READY_FILE")
            if ready:
                Path(ready).write_text(f"{root}\n{'OK' if ok else 'BAD'} {info}", encoding="utf-8")
            if seconds:
                self.set_timer(seconds, self.exit)
        self.set_timer(1.0, lambda: self.run_worker(go()))
    type(app).on_mount = on_mount
    app.played = False
    return app


if __name__ == "__main__":
    a = sys.argv[1:]
    root = Path(tempfile.mkdtemp(prefix="mri-cap-"))
    try:
        if a[0] == "live":
            make(a[1], root, float(a[2]) if len(a) > 2 else None).run()
        else:
            w, h = (a[2] if len(a) > 2 else "118x30").split("x")
            app = make(a[1], root)

            async def go():
                async with app.run_test(size=(int(w), int(h))) as pilot:
                    while not app.played:
                        await pilot.pause(0.3)
                    print("STATE", app.result)
                    print("\n".join(lines(app)))
            asyncio.run(go())
    finally:
        shutil.rmtree(root, ignore_errors=True)
