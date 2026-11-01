"""Inc K task captures (E13): the SHIPPED app, capture view `n`, on a synthetic two-board registry.

    python scene.py live <scene> [seconds]     (a real terminal; used by shoot.ps1)
    python scene.py dump <scene> [WxH]         (headless: prints the end state + screen text)
Scenes: k-empty k-dividers k-notice k-rail k-review k-dump k-newproject k-colour.
Synthetic data only, owner `username_subject`. Path.home is redirected to a temp folder
(never the real ~/.taskboard). Adapted from incL's scene.py; imports nothing from prototypes/ or incL.
"""
from __future__ import annotations

import asyncio
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

import taskboard  # noqa: E402
import taskboard.__main__ as entry  # noqa: E402
from taskboard.models import LINKS_MIGRATION, MILESTONES_MIGRATION, Board, Project, Task  # noqa: E402

TB_FILE = str(Path(taskboard.__file__).resolve())
TB_INSIDE = Path(TB_FILE).is_relative_to(ROOT)

SETTINGS = {"migrations": {"links": LINKS_MIGRATION, "milestones": MILESTONES_MIGRATION},
            "seen_view_renumber_2026_07": True}
NOTES4 = ("Golden set: 12 questions still have no answer key\n"
          "ask @username_subject which stores count\n"
          "____\n"
          "Volume lab fails on WSL\nthe oracle script expects /mnt/c\n"
          "____\n"
          "Quote for the new client: contracts Q&A\ntwo weeks, fixed price\n"
          "____\n"
          "Steering deck: demo the hybrid search on pilot stores")
COLOUR = ("Vendor call\n::b:: ask the vendor :: @username_subject\n"
          "::r:: blocker: 12 questions lack a key ::\n==decided: 400-token chunks==")


def build(home_root: Path, pad: str) -> None:
    """Write the registry and the store under `<home_root>/.taskboard` (= Path.home()/.taskboard)."""
    home = home_root / ".taskboard"
    ap, cp = home / "boards" / "client-a" / "board.json", home / "boards" / "course" / "board.json"
    for p in (ap, cp):
        p.parent.mkdir(parents=True, exist_ok=True)
    pe, pr = Project("Eval harness", "blue", id="pe"), Project("Pilot rollout", "indigo", id="pr")
    Board([pe, pr], [
        Task("Golden set questions", project_id="pe", phase="Todo", id="a1"),
        Task("Answer key rubric", project_id="pe", phase="Backlog", id="a2"),
        Task("Pilot stores list", project_id="pr", phase="Doing", id="a3"),
        Task("Steering deck", project_id="pr", phase="Backlog", id="a4"),
    ], ap, dict(SETTINGS), ["Backlog", "Todo", "Doing", "Done"]).save()
    pv = Project("Module 4 · Volumes", "violet", id="pv")
    Board([pv], [Task("Volume lab", project_id="pv", phase="Todo", id="c1"),
                 Task("Oracle script", project_id="pv", phase="Backlog", id="c2")],
          cp, dict(SETTINGS), ["Backlog", "Todo", "Done"]).save()
    entries = [{"id": "client-a", "name": "Client A", "color": "sky", "path": str(ap.resolve()),
                "last_opened": "2026-11-01T07:00", "archived": False},
               {"id": "course", "name": "Course", "color": "violet", "path": str(cp.resolve()),
                "last_opened": "2026-10-31T20:00", "archived": False}]
    (home / "boards.json").write_text(json.dumps({"version": 1, "last": "client-a",
                                                  "boards": entries}, indent=2), encoding="utf-8")
    (home / "people.json").write_text(json.dumps({"version": 1, "people": [
        {"id": "username_subject", "name": "username_subject"}]}, indent=2), encoding="utf-8")
    # the store as LLR-4407.2 shapes it; no `divider_notice` key (no scene sets it)
    (home / "inbox.json").write_text(json.dumps({"version": 1, "pad": pad, "dumped": []},
                                                indent=2, ensure_ascii=False), encoding="utf-8")


def screen_text(app) -> str:
    return "\n".join("".join(seg.text for seg in strip)
                     for strip in app.screen._compositor.render_strips())


def name(app) -> str:
    return type(app.screen).__name__


def capture(app):
    for sc in app.screen_stack:
        if type(sc).__name__ == "CaptureView":
            return sc
    return None


def toasts(app) -> list[str]:
    return [str(n.message) for n in app._notifications]


def plain(app, wid) -> str:
    sc = capture(app)
    c = sc.query_one(wid).content
    return getattr(c, "plain", str(c))


def cur_note(app) -> int | None:
    """1-based index of the note under the pad cursor."""
    from taskboard.inbox import note_at, note_parts
    pad = capture(app).query_one("#cap-pad")
    at = note_at(pad.text, pad.cursor_location[0])
    notes = [p for p in note_parts(pad.text) if p.is_note]
    return notes.index(at) + 1 if at is not None else None


# end-state checks: (ok, detail)
def c_empty(app):
    t = screen_text(app)
    ok = (name(app) == "CaptureView" and capture(app).query_one("#cap-pad").text == ""
          and "first line → the task's title" in t
          and "____ ↵ new note · alt+l divider" in plain(app, "#cap-hint"))
    return ok, "capture open, pad empty, ghost + hint row drawn"


def c_dividers(app):
    t = screen_text(app).split("\n")
    stray = [ln for ln in t if "____" in ln and "↵" not in ln and "divides" not in ln]
    ok = (name(app) == "CaptureView" and cur_note(app) == 4
          and "4 notes" in plain(app, "#cap-head") and not stray
          and sum("─" * 30 in ln for ln in t) >= 3)
    return ok, f"cursor note {cur_note(app)}, head '4 notes', 3 rules, {len(stray)} raw ____ rows"


def c_notice(app):
    ok = (name(app) == "CaptureView"
          and any(m.startswith("That ____ line divides notes") for m in toasts(app))
          and app.inbox.divider_notice is True)
    return ok, "one-time divider notice toast shown, flag stored"


def c_rail(app):
    r = plain(app, "#cap-rail")
    # with the brief's data note 4 shares words with one project only, so options() gives a
    # single hit and the rail draws no `or` line; the check requires → and why, records `or`
    ok = name(app) == "CaptureView" and cur_note(app) == 4 and "→" in r and "why" in r
    alt = "or line drawn" if " or " in r else "no or line (one hit)"
    return ok, f"cursor note {cur_note(app)}, rail has → / why, {alt}"


def c_review(app):
    ok = name(app) == "ReviewList" and "Review" in screen_text(app)
    return ok, "review list on top"


def c_dump(app):
    pad = capture(app).query_one("#cap-pad").text
    ok = (name(app) == "CaptureView" and any(m.startswith("Dumped → ") for m in toasts(app))
          and "Golden set: 12 questions" not in pad and "3 notes" in plain(app, "#cap-head"))
    return ok, "toast 'Dumped →' shown, note 1 gone, head '3 notes'"


def c_newproject(app):
    sc = capture(app)
    f = sc.query_one("#cap-new")
    ok = (name(app) == "CaptureView" and f.has_class("on") and f.value == "Contracts QA"
          and "⇥" in plain(app, "#cap-keys"))
    return ok, f"name field open, value {f.value!r}, ⇥ board in key row"


def c_colour(app):
    ok = name(app) == "CaptureView" and capture(app).query_one("#cap-pad").text == COLOUR
    return ok, "capture open, colour pad loaded verbatim"


def chars(s: str) -> list[str]:
    return list(s)


U = "up"
# QUIET: the store has no `divider_notice` (the brief), so on a 4-note pad the one-time notice
# toast opens with the view and, in the first run, covered the scene's subject (the alt+n field,
# the dump toast at 80x24). The harness checks the notice was shown, then waits out its 15 s
# timeout before the scene's own keys; the data stays as the brief gives it.
QUIET = "wait:notice"
SCENES = {
    "k-empty": ("", ["n"], c_empty),
    "k-dividers": (NOTES4, ["n", QUIET], c_dividers),
    "k-notice": ("", ["n", *chars("First note"), "enter", *chars("____"), "enter"], c_notice),
    "k-rail": (NOTES4, ["n", QUIET], c_rail),
    "k-review": (NOTES4, ["n", QUIET, "alt+a"], c_review),
    "k-dump": (NOTES4, ["n", QUIET, *[U] * 9, "alt+d"], c_dump),
    "k-newproject": (NOTES4, ["n", QUIET, U, U, U, "alt+n", *chars("Contracts QA")], c_newproject),
    "k-colour": (COLOUR, ["n"], c_colour),
}


class Scene(entry.TaskboardApp):
    CSS_PATH = str(ROOT / "taskboard" / "taskboard.tcss")

    def __init__(self, scene, root, seconds=None):
        self.scene, self._seconds, self._root, self.played = scene, seconds, root, False
        self.result = (False, "not played")
        self.first_screen = ""
        self.quiet = ""
        build(root, SCENES[scene][0])
        Path.home = classmethod(lambda cls: root)
        from taskboard.boards import Registry, registry_path
        from taskboard.models import default_board_path
        assert registry_path().is_relative_to(root), registry_path()
        reg = Registry.load(registry_path(), default_board_path())
        e = reg.opening()
        super().__init__(board_path=e.path, registry=reg)

    def on_mount(self) -> None:
        # no super().on_mount(): Textual already runs TaskboardApp.on_mount (MRO dispatch);
        # calling it again pushes the boards home twice (seen in the dry run)
        if os.environ.get("PROTO_SHOT_TITLE"):
            self.title = os.environ["PROTO_SHOT_TITLE"]
        self.set_timer(1.0, lambda: self.run_worker(self.play()))

    async def play(self):
        self.first_screen = name(self)
        if self.first_screen == "BoardsHome":
            await run_steps(self, ["escape"])
        await run_steps(self, SCENES[self.scene][1])
        await asyncio.sleep(0.6)
        try:
            ok, detail = SCENES[self.scene][2](self)
        except Exception as exc:        # a missing widget = wrong end state
            ok, detail = False, f"check raised {exc!r}"
        if not TB_INSIDE:
            ok, detail = False, f"taskboard imported from outside the worktree: {TB_FILE}"
        if self.quiet and not self.quiet.endswith("waited out"):
            ok = False
        if self.quiet:
            detail += f"; {self.quiet}"
        self.result = (ok, f"{detail}; opened on {self.first_screen}")
        self.played = True
        ready = os.environ.get("PROTO_READY_FILE")
        if ready:
            Path(ready).write_text(f"{self._root}\n{'OK' if ok else 'BAD'} {self.result[1]}\n"
                                   f"taskboard.__file__={TB_FILE}", encoding="utf-8")
        if self._seconds:
            self.set_timer(self._seconds, self.exit)


NOTICE = "That ____ line divides notes"


async def run_steps(app, steps):
    for st in steps:
        if st == QUIET:
            if not any(m.startswith(NOTICE) for m in toasts(app)):
                app.quiet = "notice NOT shown at open"
                continue
            for _ in range(100):              # <= 20 s; the notice's timeout is 15 s
                if not any(m.startswith(NOTICE) for m in toasts(app)):
                    break
                await asyncio.sleep(0.2)
            await asyncio.sleep(0.8)          # the toast widget leaves the rack
            gone = not any(m.startswith(NOTICE) for m in toasts(app))
            app.quiet = "divider notice shown at open, waited out" if gone else "notice still up"
            continue
        await app._press_keys([st])
        await asyncio.sleep(0.12 if len(st) == 1 else 0.3)


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
                    print("TB", TB_FILE, "inside" if TB_INSIDE else "OUTSIDE")
                    print("STATE", "OK" if sc.result[0] else "BAD", sc.result[1])
                    print("TOASTS", toasts(sc))
                    print(screen_text(sc))
            asyncio.run(go())
    finally:
        shutil.rmtree(root, ignore_errors=True)
