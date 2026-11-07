r"""Inc MR-b captures (E13): the SHIPPED presentation `R` with the milestones on one row, driven by real keys.

    python scene.py live <scene> [seconds]     (a real terminal; used by shoot.ps1)
    python scene.py dump <scene> [WxH]         (headless: end state + width check + screen text)
Scenes: mrb-v1 (R, view 1, `down` onto a milestone), mrb-v2 (view 2, split), mrb-v3 (view 3, all),
mrb-hostile (view 1, a milestone titled `[@click=app.quit]x\`, cursor on it).
Fixture: tests/milestone_row_fixture.py (MR-F). Synthetic data only. Path.home is redirected to a temp folder.
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

HOSTILE = "[@click=app.quit]x\\"
EXTRA = {"mrb-hostile": [fx.task("hx", "pr", HOSTILE, "Backlog", None, 7, ms=True, mark="delivery")]}


def lines(app):
    return ["".join(seg.text for seg in strip)
            for strip in app.screen._compositor.render_strips()]


def width_ok(app):
    w = app.size.width
    return all(cell_len(l) <= w for l in lines(app))


def screen_of(app):
    return next(s for s in reversed(app.screen_stack) if type(s).__name__ == "PresentScreen")


async def play(app, scene):
    p = app._press_keys

    async def k(*ks):
        for x in ks:
            await p([x])
            await asyncio.sleep(0.4)
    await asyncio.sleep(1.5)
    await k("escape")
    app.selected_task_id = None
    app.focused_project_id = "ppr"
    await k("R")
    txt = lambda: "\n".join(lines(app))
    if scene == "mrb-v1":
        await k("down")
        ok = "Pilot rollout" in txt()
    elif scene == "mrb-v2":
        await k("2", "down")
        ok = "Pilot rollout" in txt()
    elif scene == "mrb-v3":
        await k("3")
        ok = all(n in txt() for n in ("Pilot rollout", "Eval harness"))
    else:
        for _ in range(12):
            if ("⟦" + HOSTILE[:15]) in txt():
                break
            await k("down")
        ok = ("⟦" + HOSTILE[:15]) in txt()
    await asyncio.sleep(0.6)
    return ok and width_ok(app), f"view_ok={ok} width_ok={width_ok(app)}"


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
    root = Path(tempfile.mkdtemp(prefix="mrb-cap-"))
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
