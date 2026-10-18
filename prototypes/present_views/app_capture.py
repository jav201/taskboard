"""HISTORICAL (2026-10-18-batch-02): this round file no longer runs against the
shipped tree -- it imports `views_proto.py`, historical (`views._present_note_lines` and `_present_note_row`, deleted in 2026-10-18-batch-01 (a729f78)). It last ran against `9810be6`; the captures in `out/`
and the round page are the record. Not repaired on purpose: its outputs came
from helpers that are gone, so a repaired script would not reproduce them
(`docs/ARCHITECTURE.md` §3, `prototypes` row).

PROTOTYPE round — several views inside Present (`R`), captured FROM THE APP.

    python prototypes/present_views/app_capture.py

Sub-shape A (tui-design PROTOTYPE.md): the real `TaskboardApp` runs headless
over the prototype's own synthetic board (fixture.py); only `PresentScreen` is
subclassed. Keys go through the pilot (`R`, `1`-`4`, `tab`, arrows, `space`,
`pagedown`); each frame is the app's own `export_screenshot()` SVG, then a PNG
rasterised by headless Edge (the shipped `save_present_png` recipe).

Keys added: `1`-`4` jump to a view, `tab` / `shift+tab` cycle, `pgdn`/`pgup`
scroll the notes in slide and split. The view switch, like the hidden count,
rides the hint row only."""
from __future__ import annotations

import asyncio
import re
import subprocess
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
import views_proto as VP  # noqa: E402
from taskboard import app as app_mod  # noqa: E402
from taskboard import models  # noqa: E402
from taskboard.views import _find_msedge, present_hidden  # noqa: E402

OUT = HERE / "out"


class _Today(date):
    @classmethod
    def today(cls):
        return fx.TODAY


class PresentViews(app_mod.PresentScreen):
    BINDINGS = app_mod.PresentScreen.BINDINGS + [
        Binding("1", "view(0)", "", priority=True),
        Binding("2", "view(1)", "", priority=True),
        Binding("3", "view(2)", "", priority=True),
        Binding("4", "view(3)", "", priority=True),
        Binding("tab", "cycle(1)", "", priority=True),
        Binding("shift+tab", "cycle(-1)", "", priority=True),
        Binding("pagedown", "scroll(1)", "", priority=True),
        Binding("pageup", "scroll(-1)", "", priority=True),
    ]

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self._view = 0
        self._scroll = 0

    def _frame(self, w, h):
        return VP.RENDER[VP.VIEWS[self._view]](self._board, self._project_id, self._cursor_id,
                                               self._today, w, h, self._scroll)

    def _paint(self) -> None:
        w, h = self.size.width or 0, self._frame_height()
        self.query_one("#present-frame").update(self._frame(w, h))
        hint = Text()
        for i, name in enumerate(VP.VIEWS):
            on = i == self._view
            hint.append(f"{i + 1} {name}",
                        style="bold #e6edf7" if on else "#5b6675")
            hint.append("  " if w >= 100 else " ")
        rest = ("⇥ next · ←→ move · ␣ hide · a all · x export · esc" if w >= 100
                else " ⇥ · ←→ · ␣ hide · a · x · esc")
        if VP.VIEWS[self._view] in getattr(VP, "SCROLLS", ("slide", "split")) and w >= 100:
            rest = "pgdn notes · " + rest
        hint.append(rest, style="#8b98a5")
        hidden = len(present_hidden(self._board, self._project_id))
        if hidden:
            hint.append(f" · {hidden} hidden", style="#8b98a5")
        self.query_one("#present-hint").update(hint)

    def action_view(self, i: int) -> None:
        self._view, self._scroll = i, 0
        self._paint()

    def action_cycle(self, d: int) -> None:
        self.action_view((self._view + d) % len(VP.VIEWS))

    def action_scroll(self, d: int) -> None:
        self._scroll = max(0, self._scroll + d * 5)
        self._paint()

    def action_move(self, delta: int) -> None:
        self._scroll = 0
        super().action_move(delta)

    def action_export(self) -> None:          # prototype: never exports
        pass


app_mod.PresentScreen = PresentViews
app_mod.date = _Today
models.date = _Today


def to_png(svg: Path) -> Path | None:
    """Edge renders the SVG at its own viewBox size (the shipped recipe, sized
    from the file instead of the cell grid)."""
    exe = _find_msedge()
    if exe is None:
        return None
    m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg.read_text(encoding="utf-8"))
    w, h = (int(float(m.group(1))) + 1, int(float(m.group(2))) + 1) if m else (1500, 900)
    png = svg.with_suffix(".png")
    html = svg.with_suffix(".view.html")
    html.write_text(f'<html><body style="margin:0;background:#0d1117">'
                    f'<img src="{svg.name}" width="{w}" height="{h}"></body></html>',
                    encoding="utf-8")
    subprocess.run([exe, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    f"--screenshot={png}", f"--window-size={w},{h}", html.as_uri()],
                   capture_output=True, timeout=60)
    html.unlink()
    return png if png.exists() else None


async def run(size, steps, name) -> None:
    tmp = Path(tempfile.mkdtemp())
    board = fx.build(tmp / "board.json")
    board.save()
    app = app_mod.TaskboardApp(board_path=str(tmp / "board.json"))
    async with app.run_test(size=size) as pilot:
        for _ in range(50):
            if type(app.screen).__name__ == "MilestoneOffer":
                await pilot.press("escape")
                break
            await pilot.pause()
        await pilot.pause()
        app.selected_task_id = fx.CURSOR
        await pilot.press("R")
        await pilot.pause()
        assert type(app.screen).__name__ == "PresentViews", type(app.screen).__name__
        for frame, keys in steps:
            for k in keys:
                await pilot.press(k)
            await pilot.pause()
            svg = app.export_screenshot(title=f"taskboard · R present · {frame}")
            path = OUT / f"{name}-{frame}.svg"
            path.write_text(re.sub(r"@font-face\s*\{[^}]*\}", "", svg), encoding="utf-8")
            to_png(path)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    # fixture order (open, by due): component library · checkout 500 (cursor) ·
    # image assets · launch (long note) · SEO redirects (empty note)
    big = [("A-gantt", []),
           ("B-cards", ["2"]),
           ("B-cards-moved", ["right", "right"]),          # → Launch new homepage
           ("B-cards-hidden", ["left", "space"]),         # hide Optimize image assets
           ("C-slide", ["a", "3", "left", "left"]),        # back on checkout 500
           ("C-slide-moved", ["right", "right"]),          # → Launch (long note)
           ("C-slide-empty", ["right"]),                   # SEO redirects: no notes
           ("D-split", ["4", "left", "left", "left"]),     # checkout 500
           ("D-split-long", ["right", "right"]),           # Launch: long note overflow
           ("tab-cycle", ["tab"])]                          # tab wraps split -> gantt
    asyncio.run(run((118, 31), big, "118"))
    small = [("A-gantt", []),
             ("B-cards", ["2"]),
             ("B-cards-moved", ["right"]),
             ("C-slide", ["3", "left"]),
             ("C-slide-long", ["right", "right"]),
             ("C-slide-long-pgdn", ["pagedown"]),
             ("D-split", ["4", "left", "left"]),
             ("D-split-long", ["right", "right"]),
             ("D-split-long-pgdn", ["pagedown"])]
    asyncio.run(run((80, 25), small, "80"))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
