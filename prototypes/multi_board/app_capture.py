"""THROWAWAY — capture the multi-board round FROM THE APP.

    unset NO_COLOR; PYTHONUTF8=1 python prototypes/multi_board/app_capture.py [PNG_DIR]

Every frame is the real `TaskboardApp` (subclassed in mb_proto.py) driven by
real keypresses through `run_test`'s pilot, saved with `export_screenshot()`.
Each run gets a fresh synthetic registry (fixture.py) in a temporary folder.
With PNG_DIR, each SVG is also rasterised with headless Edge.
"""
from __future__ import annotations

import asyncio
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))

import fixture as fx  # noqa: E402
import mb_proto as M  # noqa: E402
from taskboard import app as app_mod, models, views  # noqa: E402
from datetime import date  # noqa: E402

OUT = HERE / "out"
SIZES = [(160, 45), (118, 30), (80, 24)]


class _Today(date):
    @classmethod
    def today(cls):
        return fx.TODAY


app_mod.date = _Today
models.date = _Today
views.date = _Today


def _save(app, name: str, title: str) -> None:
    svg = app.export_screenshot(title=title)
    (OUT / f"{name}.svg").write_text(re.sub(r"@font-face\s*\{[^}]*\}", "", svg),
                                     encoding="utf-8")


def tree(root: Path) -> str:
    lines = []
    for p in sorted(root.rglob("*")):
        rel = p.relative_to(root).as_posix()
        lines.append(("~/.taskboard/" + rel) + ("/" if p.is_dir() else ""))
    return "\n".join(lines)


async def run(variant: str, size, steps, name: str, last="personal", evidence=None,
              baseline=False):
    """One app: a fresh registry, then each step's keys and a frame per step."""
    root = Path(tempfile.mkdtemp())
    reg = fx.build(root, last)
    if baseline:                                   # today's app, no registry at all
        app = app_mod.TaskboardApp(board_path=str(fx.board_path(root, "main")))
    else:
        app = M.make_app(variant, reg, root)
    async with app.run_test(size=size) as pilot:
        for _ in range(4):
            await pilot.pause()
        for frame, keys in steps:
            for k in keys:
                if k.startswith("@type:"):             # into the focused Input
                    box = app.focused
                    box.value = box.value + k[6:]
                    box.cursor_position = len(box.value)
                elif k.startswith("@sel:"):
                    app.selected_task_id = k[5:]
                    app.refresh_view()
                elif k.startswith("@cursor:"):            # the projects list highlight
                    ol = app.screen.query_one("#proj-list")
                    ids = [p.id for p in app.board.projects]
                    ol.highlighted = ids.index(k[8:])
                elif k.startswith("@tree:"):
                    evidence[k[6:]] = tree(root)
                else:
                    await pilot.press(k)
                await pilot.pause()
            await pilot.pause()
            await pilot.pause()
            _save(app, f"{name}-{frame}", f"taskboard · {variant} · {frame}")
    if evidence is not None:
        evidence.setdefault("registry_" + name, json.loads(reg.read_text(encoding="utf-8")))
        for e in evidence["registry_" + name]["boards"]:
            e["path"] = M.pretty(e["path"])


def to_png(png_dir: Path) -> int:
    exe = None
    for base in (os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"),
                 os.environ.get("ProgramFiles", r"C:\Program Files")):
        cand = Path(base) / "Microsoft" / "Edge" / "Application" / "msedge.exe"
        if cand.is_file():
            exe = str(cand)
    if exe is None:
        print("no Edge: PNGs skipped")
        return 0
    png_dir.mkdir(parents=True, exist_ok=True)
    n = 0
    for svg in sorted(OUT.glob("*.svg")):
        m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg.read_text(encoding="utf-8"))
        w, h = (int(float(m.group(1))) + 4, int(float(m.group(2))) + 4) if m else (1700, 1000)
        png = png_dir / f"{svg.stem}.png"
        subprocess.run([exe, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        f"--screenshot={png}", f"--window-size={w},{h}", svg.as_uri()],
                       capture_output=True, timeout=60)
        n += png.exists()
    return n


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("*.svg"):
        old.unlink()
    ev: dict = {}
    # today, for the before/after of P2
    asyncio.run(run("A", (160, 45), [("today", [])], "before-160", last="main", baseline=True))
    for w, h in SIZES:
        # A: B opens the picker over the last board (Personal)
        steps = [("open", ["B"])]
        if w == 160:
            steps += [("filter", ["@type:do"])]
        asyncio.run(run("A", (w, h), steps, f"A-{w}"))
        # B: the strip is always there; `B` is not needed to see it
        asyncio.run(run("B", (w, h), [("open", [])], f"B-{w}"))
        # C: the home launcher at launch
        asyncio.run(run("C", (w, h), [("open", [])], f"C-{w}"))
    # after switching, 160x45: the header says where you are
    asyncio.run(run("A", (160, 45), [("switched", ["B", "down", "enter"])], "A-160"))
    asyncio.run(run("B", (160, 45), [("switched", ["greater_than_sign"])], "B-160"))
    asyncio.run(run("C", (160, 45), [("switched", ["right", "enter"])], "C-160"))
    asyncio.run(run("C", (160, 45), [("switched-gantt", ["right", "enter", "3"])], "C-160"))
    # P3: split Main — move "Retail RAG · pilot" to "Client · Retail RAG"
    asyncio.run(run("A", (160, 45), [
        ("0-main-before", ["@tree:tree_before"]),
        ("1-projects", ["P", "@cursor:pmr"]),
        ("2-target", ["m", "down"]),
        ("3-confirm", ["enter"]),
        ("4-moved", ["enter", "@tree:tree_after"]),
        ("5-main-after", ["escape"]),
        ("6-client-after", ["B", "@type:client", "enter"]),
    ], "move-160", last="main", evidence=ev))
    # P4: create a board from the picker
    asyncio.run(run("A", (160, 45), [
        ("1-form", ["B", "ctrl+n", "@type:Course · Kubernetes", "tab", "tab", "tab"]),
        ("2-created", ["enter"]),
    ], "create-160"))
    # D (option): the read-only agenda across every board
    asyncio.run(run("A", (160, 45), [("open", ["A"])], "D-160"))
    asyncio.run(run("A", (80, 24), [("open", ["A"])], "D-80"))
    (OUT / "evidence.json").write_text(json.dumps(ev, indent=2), encoding="utf-8")
    n = len(list(OUT.glob("*.svg")))
    print("wrote", n, "svg to", OUT)
    if len(sys.argv) > 1:
        print("png:", to_png(Path(sys.argv[1])))


if __name__ == "__main__":
    main()
