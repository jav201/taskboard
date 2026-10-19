"""PROTOTYPE round — Present view 3 `all projects`, captured FROM THE APP.

    python prototypes/present_portfolio/app_capture.py      (NO_COLOR unset)

Sub-shape A (tui-design PROTOTYPE.md): the real `TaskboardApp` runs headless
over the round's own synthetic board (fixture.py); only `PresentScreen` is
subclassed (`PortfolioScreen`, bound in the capture process only). Views 1 and
2 are the shipped `render_present` untouched; view 3 is `portfolio_proto.render`
in variant A, B or C. Keys go through the pilot; each frame is the app's own
`export_screenshot()` SVG. Nothing under taskboard/ is edited.

Keys of view 3 (prototyped): ↑↓ (and ←→ in A/B) move the cursor over the drawn
rows; `space` hides the cursor's row (a task, or a whole project on its
header); `a` shows every hidden project and task again; `shift+↑/↓` move the
cursor's project in the presentation order; `enter` on a header folds or
unfolds it; `tab` cycles 1 → 2 → 3; `x` exports the frame (C: the timeline
only, never the rail). In C, ←→ switch the focus between the rail and the
timeline; on the rail `space` toggles ● / ○, so a hidden project can come back
alone.

Writes: `space`, `a` and `shift+↑/↓` save the board at once — task flags on
`Task.show_in_present` (shipped), project flags and ranks in `Project.extra`
(the prototype's stand-in for `Project.show_in_present` / `present_rank`)."""
from __future__ import annotations

import asyncio
import json
import re
import sys
import tempfile
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))

from rich.text import Text  # noqa: E402
from textual.binding import Binding  # noqa: E402

import fixture as fx  # noqa: E402
import portfolio_proto as P  # noqa: E402
from taskboard import app as app_mod  # noqa: E402
from taskboard import models  # noqa: E402
from taskboard.views import (PRESENT_MIN_WIDTH, present_hidden, present_tasks,  # noqa: E402
                             render_present, save_present_svg, vis)

OUT = HERE / "out"
VIEWS = ("gantt", "split", "all")
VARIANT = "A"                       # set by the runner before each app


class _Today(date):
    @classmethod
    def today(cls):
        return fx.TODAY


class PortfolioScreen(app_mod.PresentScreen, inherit_bindings=False):
    BINDINGS = [
        Binding("escape,q", "close", "Leave", priority=True),
        Binding("left,h", "side(-1)", "", priority=True),
        Binding("right,l", "side(1)", "", priority=True),
        Binding("up,k", "move(-1)", "", priority=True),
        Binding("down,j", "move(1)", "", priority=True),
        Binding("shift+up", "reorder(-1)", "", priority=True),
        Binding("shift+down", "reorder(1)", "", priority=True),
        Binding("enter", "fold", "", priority=True),
        Binding("x", "export", "Export", priority=True),
        Binding("space", "hide", "", priority=True),
        Binding("a", "show_all", "", priority=True),
        Binding("1", "view(0)", "", priority=True),
        Binding("2", "view(1)", "", priority=True),
        Binding("3", "view(2)", "", priority=True),
        Binding("tab", "cycle(1)", "", priority=True),
        Binding("shift+tab", "cycle(-1)", "", priority=True),
        Binding("pagedown", "scroll(1)", "", priority=True),
        Binding("pageup", "scroll(-1)", "", priority=True),
    ]

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.variant = VARIANT
        self.cur = ("task", self._cursor_id) if self._cursor_id else None
        self.folded: set[str] = set()       # A / C: folded by hand
        self.unfolded: set[str] = set()     # B: unfolded by hand
        self.rail = True                    # C: the focus starts on the rail
        if self.variant == "C" and self.cur:
            t = self._board.task_by_id(self.cur[1])
            self.cur = ("proj", t.project_id)
        self.nav: list = []
        self.export_path: Path | None = None

    # ---- frame -------------------------------------------------------------
    def _all(self) -> bool:
        return VIEWS[self._view] == "all"

    def _render3(self):
        w, h = self.size.width or 0, self._frame_height()
        return P.render(self._board, w, h, self._today, self.variant, self.cur,
                        self.folded, self.unfolded, focus_rail=self.rail)

    def _frame_text(self, scroll=None) -> Text:
        if not self._all():
            return render_present(self._board, self._project_id, self._cursor_id, self._today,
                                  self.size.width or 0, self._frame_height(),
                                  VIEWS[self._view], self._scroll if scroll is None else scroll)
        text, self.nav, drawn, _ = self._render3()
        if not (self.variant == "C" and self.rail):
            self.cur = drawn
        return text

    def _stops(self) -> list:
        if self.variant == "C" and self.rail:
            return [("proj", p.id) for p in P.ordered(self._board)]
        self._frame_text()
        return self.nav

    def _hint(self, w: int) -> Text:
        room = w - 2
        if room <= 0:
            return Text()
        if self._all():
            np_, nt = P.hidden_counts(self._board)
        else:
            np_, nt = 0, len(present_hidden(self._board, self._project_id))
        bits = ([f"{np_} project{'s' if np_ > 1 else ''}"] if np_ else []) + (
            [f"{nt} task{'s' if nt > 1 else ''}"] if nt else [])
        tail = (" · " + " + ".join(bits) + " hidden") if bits else ""
        if w < PRESENT_MIN_WIDTH:
            hint = Text("esc leave" + tail, style="#8b98a5")
            hint.truncate(room, overflow="ellipsis")
            return hint
        if self._all():
            side = "←→ rail/timeline · " if self.variant == "C" else ""
            wordings = (
                ("  ", f"⇥ next · ↑↓ move · {side}␣ hide · shift ↑↓ reorder · enter fold · "
                       "a show all · x export · esc leave"),
                ("  ", f"⇥ · ↑↓ · {side}␣ hide · shift ↑↓ order · enter fold · a all · x · esc"),
                (" ", "⇥ ↑↓ " + ("←→ " if side else "") + "␣ ⇧↑↓ enter a x esc"),
                (" ", "esc"),
            )
        else:
            split = VIEWS[self._view] == "split"
            wordings = (
                ("  ", ("pgdn notes · " if split else "")
                 + "⇥ next · ←→ ↑↓ move · ␣ hide · a show all · x export · esc leave"),
                ("  ", ("pgdn · " if split else "")
                 + "⇥ next · ←→ ↑↓ · ␣ hide · a show all · x export · esc"),
                (" ", "⇥ ←→ ␣ x esc"),
                (" ", "esc"),
            )
        for gap, keys in wordings:
            names = sum(vis(f"{i + 1} {n}{gap}") for i, n in enumerate(VIEWS))
            if names + vis(keys + tail) <= room:
                break
        hint = Text()
        for i, name in enumerate(VIEWS):
            hint.append(f"{i + 1} {name}", style="bold #e6edf7" if i == self._view else "#5b6675")
            hint.append(gap)
        hint.append(keys + tail, style="#8b98a5")
        hint.truncate(room, overflow="ellipsis")
        return hint

    # ---- keys --------------------------------------------------------------
    def action_view(self, index: int) -> None:
        if self._narrow():
            return
        if VIEWS[index] != "all" and self.cur is not None:
            # leaving view 3: the shared cursor picks the single project
            kind, oid = self.cur
            pid = oid if kind == "proj" else self._board.task_by_id(oid).project_id
            self._project_id = pid
            self._cursor_id = oid if kind == "task" else None
        elif VIEWS[index] == "all" and self._cursor_id:
            self.cur = (("proj", self._board.task_by_id(self._cursor_id).project_id)
                        if self.variant == "C" and self.rail else ("task", self._cursor_id))
        self._view, self._scroll = index, 0
        self._paint()

    def action_cycle(self, delta: int) -> None:
        self.action_view((self._view + delta) % len(VIEWS))

    def action_side(self, delta: int) -> None:
        if self._all() and self.variant == "C":
            self.rail = delta < 0
            if self.rail and self.cur and self.cur[0] == "task":
                self.cur = ("proj", self._board.task_by_id(self.cur[1]).project_id)
            self._paint()
        else:
            self.action_move(delta)

    def action_move(self, delta: int) -> None:
        if not self._all():
            return super().action_move(delta)
        stops = self._stops()
        if not stops:
            return
        i = stops.index(self.cur) if self.cur in stops else 0
        self.cur = stops[max(0, min(len(stops) - 1, i + delta))]
        self._paint()

    def _project_of_cursor(self):
        if self.cur is None:
            return None
        kind, oid = self.cur
        return self._board.project_by_id(
            oid if kind == "proj" else self._board.task_by_id(oid).project_id)

    def action_hide(self) -> None:
        if not self._all():
            return super().action_hide()
        if self.cur is None:
            return
        stops = self._stops()
        kind, oid = self.cur
        if self.variant == "C" and self.rail:        # the rail toggles ● / ○
            p = self._board.project_by_id(oid)
            p.extra["show_in_present"] = not P.shown(p)
            self._board.save()
            self._paint()
            return
        i = stops.index(self.cur)
        if kind == "proj":
            self._board.project_by_id(oid).extra["show_in_present"] = False
        else:
            self._board.task_by_id(oid).show_in_present = False
        self._board.save()
        after = self._stops()
        rest = [s for s in stops[i + 1:] if s in after] + [s for s in reversed(stops[:i])
                                                         if s in after]
        self.cur = rest[0] if rest else None
        self._paint()

    def action_show_all(self) -> None:
        if not self._all():
            return super().action_show_all()
        changed = False
        for p in self._board.visible_projects(False):
            if not P.shown(p):
                p.extra["show_in_present"] = True
                changed = True
            for t in present_hidden(self._board, p.id):
                t.show_in_present = True
                changed = True
        if changed:
            self._board.save()
            self._paint()

    def action_reorder(self, delta: int) -> None:
        if not self._all():
            return
        p = self._project_of_cursor()
        if p is None:
            return
        ids = [q.id for q in P.ordered(self._board)]
        i = ids.index(p.id)
        if self.variant == "C" and self.rail:         # the rail: every project
            j = i + delta
        else:                                         # the timeline: shown only
            shown = [k for k, q in enumerate(P.ordered(self._board)) if P.shown(q)]
            k = shown.index(i) + delta
            j = shown[k] if 0 <= k < len(shown) else -1
        if not 0 <= j < len(ids):
            return
        ids.insert(j, ids.pop(i))
        P.set_order(self._board, ids)
        self._board.save()
        self._paint()

    def action_fold(self) -> None:
        if not self._all() or self.cur is None or self.cur[0] != "proj":
            return
        pid = self.cur[1]
        box = self.unfolded if self.variant == "B" else self.folded
        box.symmetric_difference_update({pid})
        self._paint()

    def action_export(self) -> None:
        if not self._all() or self._narrow():
            return
        text, _nav, _cur, tl = self._render3()
        w, h = self.size.width or 0, self._frame_height()
        if tl is not None:
            text, w = tl, w - P.rail_w(w) - 1
        self.export_path = OUT / f"{self.variant}-{self.size.width}-export.svg"
        save_present_svg(text, self.export_path, w, h)


app_mod.PresentScreen = PortfolioScreen
app_mod.date = _Today
models.date = _Today


def _save_svg(app, path: Path, title: str) -> None:
    svg = app.export_screenshot(title=title)
    path.write_text(re.sub(r"@font-face\s*\{[^}]*\}", "", svg), encoding="utf-8")


async def _boot(app, pilot):
    for _ in range(50):
        if type(app.screen).__name__ == "MilestoneOffer":
            await pilot.press("escape")
            break
        await pilot.pause()
    await pilot.pause()


async def goto(pilot, screen, target) -> None:
    """Real keypresses (↑/↓) until the cursor sits on `target`."""
    for _ in range(60):
        if screen.cur == target:
            return
        stops = screen._stops()
        i = stops.index(screen.cur) if screen.cur in stops else 0
        await pilot.press("down" if stops.index(target) > i else "up")
        await pilot.pause()
    raise AssertionError(f"cursor never reached {target}: {screen.cur}")


async def run(variant: str, size, steps, name: str, board_order=None) -> dict:
    """One app, one variant: R, then 3, then each step's keys; a frame per step.
    Returns the saved board's project flags and ranks (the write's evidence)."""
    global VARIANT
    VARIANT = variant
    tmp = Path(tempfile.mkdtemp())
    board = fx.build(tmp / "board.json", board_order)
    board.save()
    app = app_mod.TaskboardApp(board_path=str(tmp / "board.json"))
    async with app.run_test(size=size) as pilot:
        await _boot(app, pilot)
        app.selected_task_id = fx.CURSOR
        await pilot.press("R")
        await pilot.pause()
        scr = app.screen
        assert type(scr).__name__ == "PortfolioScreen", type(scr).__name__
        await pilot.press("3")
        await pilot.pause()
        for frame, keys in steps:
            for k in keys:
                if isinstance(k, tuple):
                    await goto(pilot, scr, k)
                elif k.startswith("@resize"):
                    _, w, h = k.split(":")
                    await pilot.resize_terminal(int(w), int(h))
                else:
                    await pilot.press(k)
                await pilot.pause()
            await pilot.pause()
            _save_svg(app, OUT / f"{name}-{frame}.svg",
                      f"taskboard · R present · 3 all · {variant} {NAMES[variant]} · {frame}")
    saved = json.loads((tmp / "board.json").read_text(encoding="utf-8"))
    return {p["name"]: {k: p[k] for k in ("show_in_present", "present_rank") if k in p}
            for p in saved["projects"]}


NAMES = P.NAMES


async def board_gantt(order, name: str, size=(160, 45)) -> None:
    """The MAIN app's gantt (key 3) over a board in `order` — the consequence
    of each reorder choice."""
    tmp = Path(tempfile.mkdtemp())
    board = fx.build(tmp / "board.json", order)
    board.save()
    app = app_mod.TaskboardApp(board_path=str(tmp / "board.json"))
    async with app.run_test(size=size) as pilot:
        await _boot(app, pilot)
        app.selected_task_id = fx.CURSOR
        await pilot.press("3")
        await pilot.pause()
        await pilot.pause()
        _save_svg(app, OUT / f"{name}.svg", f"taskboard · 3 gantt · {name}")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("*.svg"):
        old.unlink()
    evidence = {}
    sizes = [(160, 45), (118, 30), (80, 24)]
    for v in P.VARIANTS:
        for w, h in sizes:
            steps = [("initial", [])]
            if v == "A" and w == 160:      # the shared cursor: ⇥ wraps 3 -> 1
                steps.append(("tab-to-view1", ["tab"]))
            asyncio.run(run(v, (w, h), steps, f"{v}-{w}"))
        # the hide / reorder sequence at 160x45
        if v == "C":
            seq = [("1-cursor-header", [("proj", "pbr")]),
                   ("2-hidden", ["space"]),
                   ("3-moved-top", [("proj", "pmr"), "shift+up", "shift+up"]),
                   ("4-show-all", ["a", "x"])]
        else:
            seq = [("1-cursor-header", [("proj", "pbr")]),
                   ("2-hidden", ["space"]),
                   ("3-moved-top", [("proj", "pmr"), "shift+up", "shift+up"]),
                   ("4-show-all", ["a"])]
            if v == "B":
                seq.append(("5-unfolded", [("proj", "pbm"), "enter"]))
            if v == "A":
                seq.append(("5-folded", [("proj", "pcp"), "enter"]))
        evidence[v] = asyncio.run(run(v, (160, 45), seq, f"{v}-160-seq"))
        if v == "C":
            # the timeline focus: ←→ leaves the rail, the cursor walks tasks
            asyncio.run(run(v, (160, 45), [("timeline", ["right", "down"])], "C-160"))
    asyncio.run(run("A", (160, 45), [("narrow", ["@resize:30:12"])], "A-30"))
    order0 = [k for k, *_ in fx.PROJECTS]
    moved = ["mr"] + [k for k in order0 if k != "mr"]
    asyncio.run(board_gantt(None, "board-gantt-before"))
    asyncio.run(board_gantt(moved, "board-gantt-board-order"))
    (OUT / "evidence.json").write_text(json.dumps(evidence, indent=2), encoding="utf-8")
    n = len(list(OUT.glob("*.svg")))
    print("wrote", n, "svg to", OUT)
    print(json.dumps(evidence, indent=1))


if __name__ == "__main__":
    main()
