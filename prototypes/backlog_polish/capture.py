"""PROTOTYPE round — three presentation polish items, captured FROM THE RUNNING APP
(batch 2026-10-18-batch-02, increment 003; HLR-1905 / LLR-1905.1).

    python prototypes/backlog_polish/capture.py
    python prototypes/backlog_polish/build_html.py

Nothing under `taskboard/` changes. The real `TaskboardApp` runs headless on the
synthetic notes board (`tests/present_notes_board.py`) with the calendar frozen
on its TODAY; keys are pressed as a presenter presses them; every frame is the
app's own `export_screenshot()` SVG, rasterised to PNG by the app's own
`views.save_present_png` (headless Edge). Each VARIANT is shown by rebinding,
inside this process only, `taskboard.app.render_present` (which `app` binds at
import), `PresentScreen._hint`, or the private `views._present_cut` that
`render_present` calls, to a fork this script holds — and restoring the
original before the next look. The forks are frozen to the commit the round
ran on, like the round's imports (`docs/ARCHITECTURE.md` §3).

Items (the 2026-10-18-batch-01 P4 walkthrough's UX4-2, UX4-3, UX4-4):
  contrast  the dim view word and cut marks (~3.2:1): current `dim` · A `reached` · B `mut`
  hint80    the terse 80-column hint: current · A a middle wording · B double spaces
  notecap   the gantt view's 3-row note cap: current · A fill the free rows · B 6 rows
and, for review only (shipped by increment 002 under the commission's FIX class):
  narrow    the frame and hint below 36 columns
Writes `out/<id>.svg`, `out/<id>.png` and `out/manifest.json` (each pair's SHA-256).
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import re
import sys
import tempfile
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))

from rich.style import Style  # noqa: E402
from rich.text import Span, Text  # noqa: E402

import present_notes_board as nb  # noqa: E402
from taskboard import app as app_mod  # noqa: E402
from taskboard import models, views  # noqa: E402

OUT = HERE / "out"
SIZES = [(118, 31), (80, 25)]
TITLE = "taskboard · R present"          # one title for every look: equal frames, equal SVGs


class _Today(date):
    @classmethod
    def today(cls):
        return nb.TODAY


app_mod.date = _Today
models.date = _Today
views.date = _Today

ORIG_RENDER = app_mod.render_present
ORIG_HINT = app_mod.PresentScreen._hint
ORIG_CUT = views._present_cut


# ---- item 1: the tone of the view word and the cut marks ------------------ #
_QUIET = re.compile(r"^\s*(gantt|split)\s*$|… \+\d+ lines|lines above|more lines")


def contrast_fork(tone_hex: str):
    """`render_present` with the dim view word and cut/edge marks repainted
    in `tone_hex`; every other dim span (the lattice, `no notes`) kept."""
    dim = views.HEX["dim"]

    def fork(*args, **kwargs) -> Text:
        text = ORIG_RENDER(*args, **kwargs)
        plain = text.plain
        spans = []
        for s in text.spans:
            style = str(s.style)
            if dim in style and _QUIET.search(plain[s.start:s.end]):
                s = Span(s.start, s.end, Style.parse(style.replace(dim, tone_hex)))
            spans.append(s)
        out = text.copy()
        out.spans = spans
        return out
    return fork


# ---- item 2: the 80-column hint ------------------------------------------ #
def hint_fork(extra):
    """The shipped `_hint` (increment 002) with `extra(pg)` — a list of
    (gap, keys) wordings — tried right after the long one."""
    def fork(self, w: int) -> Text:
        room = w - 2
        if room <= 0:
            return Text()
        hidden = len(app_mod.present_hidden(self._board, self._project_id))
        tail = f" · {hidden} hidden" if hidden else ""
        if w < views.PRESENT_MIN_WIDTH:
            hint = Text("esc leave" + tail, style="#8b98a5")
            hint.truncate(room, overflow="ellipsis")
            return hint
        pg = app_mod.PRESENT_VIEWS[self._view] == "split"
        wordings = [
            ("  ", ("pgdn notes · " if pg else "")
             + "⇥ next · ←→ ↑↓ move · ␣ hide · a show all · x export · esc leave"),
            *extra(pg),
            (" ", ("pgdn · " if pg else "") + "⇥ · ←→ · ␣ hide · a all · x export · esc"),
            (" ", ("pgdn " if pg else "") + "⇥ ←→ ␣ x esc"),
            (" ", "esc"),
        ]
        for gap, keys in wordings:
            names = sum(views.vis(f"{i + 1} {n}{gap}") for i, n in enumerate(app_mod.PRESENT_VIEWS))
            if names + views.vis(keys + tail) <= room:
                break
        hint = Text()
        for i, name in enumerate(app_mod.PRESENT_VIEWS):
            hint.append(f"{i + 1} {name}", style="bold #e6edf7" if i == self._view else "#5b6675")
            hint.append(gap)
        hint.append(keys + tail, style="#8b98a5")
        hint.truncate(room, overflow="ellipsis")
        return hint
    return fork


HINT_A = lambda pg: [("  ", ("pgdn · " if pg else "")  # noqa: E731
                      + "⇥ next · ←→ ↑↓ · ␣ hide · a show all · x export · esc")]
HINT_B = lambda pg: [(" ", (" pgdn " if pg else " ")  # noqa: E731
                      + "⇥ next  ←→↑↓ move  ␣ hide  a show all  x export  esc")]


# ---- item 3: the gantt view's note cap ----------------------------------- #
_CAP = {"k": None}


def _cut_fork(rows, k, w):
    """`_present_cut` with the gantt view's 3-row cap replaced while a cap
    fork is rendering (the split view never calls it with the flag set)."""
    if _CAP["k"] is not None and k == 3:
        k = _CAP["k"]
    return ORIG_CUT(rows, k, w)


def cap_fork(mode):
    def fork(board, project_id, cursor_id, today, width, height, view="gantt", scroll=0):
        if view != "gantt":
            return ORIG_RENDER(board, project_id, cursor_id, today, width, height, view, scroll)
        first = ORIG_RENDER(board, project_id, cursor_id, today, width, height, view, scroll)
        rows = first.plain.split("\n")
        free = len(rows) - len(rows[:max(i for i, r in enumerate(rows) if r.strip()) + 1])
        _CAP["k"] = 3 + free if mode == "fill" else 6
        views._present_cut = _cut_fork
        try:
            return ORIG_RENDER(board, project_id, cursor_id, today, width, height, view, scroll)
        finally:
            views._present_cut = ORIG_CUT
            _CAP["k"] = None
    return fork


# ---- the round ------------------------------------------------------------ #
def _look(item, look):
    """(render_present, _hint) for one look."""
    if item == "contrast":
        tone = {"current": None, "A": views.HEX["reached"], "B": views.HEX["mut"]}[look]
        return (contrast_fork(tone) if tone else ORIG_RENDER), ORIG_HINT
    if item == "hint80":
        return ORIG_RENDER, {"current": ORIG_HINT, "A": hint_fork(HINT_A), "B": hint_fork(HINT_B)}[look]
    if item == "notecap":
        return {"current": ORIG_RENDER, "A": cap_fork("fill"), "B": cap_fork("six")}[look], ORIG_HINT
    return ORIG_RENDER, ORIG_HINT


# scenes: (name, keys pressed after `R` with the cursor on the oracle task)
SCENES = {
    "contrast": [("gantt-long", ["right", "right"]), ("split-long", ["right", "right", "2"])],
    "hint80": [("gantt", []), ("split", ["2"]), ("gantt-hidden", ["space"])],
    "notecap": [("gantt-long", ["right", "right"]), ("gantt-short", [])],
}
LOOKS = {"contrast": ["current", "A", "B"], "hint80": ["current", "A", "B"],
         "notecap": ["current", "A", "B"]}
# the `x` notice is not in these captures: `export_screenshot` paints no toast over
# PresentScreen (probed at 118 columns too, where the shipped "Exported …" toast is
# absent from the SVG), so the notice is asserted by AT-1903's text only
NARROW = [("narrow-30x12", (30, 12), [("resize", (30, 12))]),
          ("narrow-20x12", (20, 12), [("resize", (20, 12))]),
          ("narrow-50x20-hidden", (50, 20), [("key", "space"), ("resize", (50, 20))])]


async def _shot(size, steps, render, hint, path: Path) -> None:
    with tempfile.TemporaryDirectory() as scratch:      # the app saves its board: a scratch copy
        await _shot_in(Path(scratch), size, steps, render, hint, path)


async def _shot_in(tmp: Path, size, steps, render, hint, path: Path) -> None:
    nb.build(tmp / "board.json").save()
    app_mod.render_present, app_mod.PresentScreen._hint = render, hint
    try:
        app = app_mod.TaskboardApp(board_path=str(tmp / "board.json"))
        async with app.run_test(size=size) as pilot:
            for _ in range(50):
                if type(app.screen).__name__ == "MilestoneOffer":
                    await pilot.press("escape")
                    break
                await pilot.pause()
            await pilot.pause()
            app.selected_task_id = nb.CURSOR
            await pilot.press("R")
            await pilot.pause()
            for kind, arg in steps:
                if kind == "key":
                    await pilot.press(arg)
                else:
                    await pilot.resize_terminal(*arg)
                await pilot.pause()
                await pilot.pause()
            await pilot.pause()
            svg = app.export_screenshot(title=TITLE)
    finally:
        app_mod.render_present, app_mod.PresentScreen._hint = ORIG_RENDER, ORIG_HINT
    path.write_text(re.sub(r"@font-face\s*\{[^}]*\}", "", svg), encoding="utf-8")


def _png_cells(svg: Path, size) -> tuple[int, int]:
    """The Edge window for the PNG, in the cells `save_present_png` takes
    (10 × 20 px each): the frame's own size, but never narrower than 60 cells —
    Edge will not open a narrower window, so a 30-column frame came out cropped;
    the height follows the SVG's own aspect."""
    w = max(size[0], 60)
    vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg.read_text(encoding="utf-8"))
    h = round(w * 10 * float(vb.group(2)) / float(vb.group(1)) / 20) + 1
    return w, max(h, size[1])


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    jobs = []
    for item, scenes in SCENES.items():
        for look in LOOKS[item]:
            for scene, keys in scenes:
                for w, h in SIZES:
                    cid = f"{item}-{look}-{scene}-{w}x{h}"
                    jobs.append((cid, item, look, scene, (w, h), (w, h),
                                 [("key", k) for k in keys]))
    for scene, size, steps in NARROW:
        jobs.append((f"narrow-current-{scene}", "narrow", "current", scene, size, (118, 31), steps))
    manifest = []
    for cid, item, look, scene, size, start, steps in jobs:
        render, hint = _look(item, look)
        svg = OUT / f"{cid}.svg"
        asyncio.run(_shot(start, steps, render, hint, svg))
        png = views.save_present_png(svg, svg.with_suffix(".png"), *_png_cells(svg, size))
        manifest.append({"id": cid, "item": item, "look": look, "scene": scene,
                         "size": f"{size[0]}x{size[1]}", "svg": svg.name, "svg_sha256": _sha(svg),
                         "png": png.name if png else None, "png_sha256": _sha(png) if png else None})
        print(cid, "png" if png else "png: Edge absent or failed")
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=1, ensure_ascii=False) + "\n",
                                       encoding="utf-8")


if __name__ == "__main__":
    main()
