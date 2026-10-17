"""PROTOTYPE — the `?` help modal lists the palette-only keys (R Present, S Standup, …).

    python prototypes/present_rulers/legend_proto.py

`HelpModal`'s Keys section is built from `bar_keys(mode)`, which drops every
`bar=False` key, so `R` and `S` never reach the `?` legend. The variant keeps the
Keys list as shipped and adds a `Global` block of exactly those keys. Captured
headlessly from the real app (gantt view, PRES-C oracle board) as SVG.
"""
from __future__ import annotations

import asyncio
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))

from rich.text import Text
from textual.widgets import Label

import present_board as pb
from taskboard import keymap, modals
from taskboard.app import TaskboardApp

OUT = Path(__file__).resolve().parent / "out"
GRID = False
SIZE = (118, 40)


def global_keys(mode: str) -> list:
    """The live keys the bar never draws — the ones the legend lost."""
    return [k for k in keymap._live_keys(mode) if not k.bar]


_shipped_compose = modals.HelpModal.compose


class _GlobalAfterKeys(modals.HelpModal):
    def compose(self):
        # the shipped compose yields into a context-managed tree; the cheapest
        # honest seam is to let it run and then mount the block into #help-left
        yield from _shipped_compose(self)

    def on_mount(self) -> None:
        left = self.query_one("#help-left")   # the Keys list on the right already
        # overflows the box (it stops at `6 Chains`): appended there, the block is hidden again
        left.mount(Label(""))
        left.mount(Label("[b]Global[/b] [dim]· any view, not on the bar[/dim]",
                         classes="modal-title"))
        for k in global_keys(self._mode):
            left.mount(Label(Text(f"  {k.show}  {k.label}")))
        if GRID:
            self._grid_keys()

    def _grid_keys(self) -> None:
        """Alternative (a): the Keys list as a column-major grid sized to the
        right pane, so the whole list fits instead of running off the box."""
        right = self.query_one("#help-right")
        kids = list(right.children)
        at = next(i for i, w in enumerate(kids)
                  if isinstance(w, Label) and "Keys" in str(w.render()))
        for w in kids[at + 1:]:
            w.remove()
        kids[at].remove()                    # the heading moves with the list
        cells = [f"{k.show:<3} {k.label}" for k in keymap.bar_keys(self._mode)]
        cw = max(len(x) for x in cells) + 2
        ncol = max(1, 104 // cw)             # the box's full inner width, not the pane's
        rows = -(-len(cells) // ncol)
        lines = []
        for r in range(rows):
            lines.append("".join(f"{cells[c * rows + r]:<{cw}}"
                                 for c in range(ncol) if c * rows + r < len(cells)).rstrip())
        box = self.query_one("#help-modal-box")
        foot = list(box.children)[-1]
        box.mount(Label("[b]Keys[/b] [dim]· this view[/dim]", classes="modal-title"), before=foot)
        box.mount(Label(Text("\n".join(lines))), before=foot)


async def capture(variant: str) -> str:
    tmp = Path(tempfile.mkdtemp())
    board = pb.build(tmp / "board.json")
    board.save()
    global GRID
    GRID = variant == "grid"
    if variant in ("proposed", "grid"):
        modals.HelpModal = _GlobalAfterKeys
    else:
        modals.HelpModal = _ORIG
    import taskboard.app as app_mod
    app_mod.HelpModal = modals.HelpModal
    app = TaskboardApp(board_path=str(tmp / "board.json"))
    async with app.run_test(size=SIZE) as pilot:
        for _ in range(50):                    # the one-time milestone offer opens
            if type(app.screen).__name__ == "MilestoneOffer":   # on startup: leave it
                await pilot.press("escape")
                break
            await pilot.pause()
        await pilot.pause()
        await pilot.press("3")
        await pilot.pause()
        await pilot.press("question_mark")
        await pilot.pause()
        svg = app.export_screenshot(title=f"? help · {variant}")
    return re.sub(r"@font-face\s*\{[^}]*\}", "", svg)


_ORIG = modals.HelpModal


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for v in ("shipped", "proposed", "grid"):
        (OUT / f"legend-{v}.svg").write_text(asyncio.run(capture(v)), encoding="utf-8")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
