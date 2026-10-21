"""Premise probes of batch 2026-10-20-batch-03, run on `base_ref` (1fd667b) from the
project root with NO_COLOR unset:  python .dev-flow/2026-10-20-batch-03/evidence/premises.py
Synthetic data only, in a temporary folder that stands in for the home."""
import asyncio
import json
import sys
import tempfile
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))
TMP = Path(tempfile.mkdtemp(prefix="b03-premises-"))
Path.home = classmethod(lambda cls: TMP)          # never the real home

import multi_board_fixture as mb  # noqa: E402
from taskboard import app as app_mod, keymap, modals, views  # noqa: E402
from taskboard.app import BoardsHome, PresentScreen, TaskboardApp  # noqa: E402
from taskboard.boards import Registry  # noqa: E402

app_mod.milestones_marked = lambda settings: True


def probe(n, text):
    print(f"P-{n} {text}")


async def present_probes():
    home = TMP / "p" / ".taskboard"
    reg = mb.build(home, "main")
    app = TaskboardApp(board_path=home / "board.json",
                       registry=Registry.load(reg, home / "board.json"))
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        if isinstance(app.screen, BoardsHome):
            await pilot.press("escape")
            await pilot.pause()
        await pilot.press("R")
        await pilot.pause()
        scr = app.screen
        hint = scr.query_one("#present-hint").render()
        probe(2, f"label {app.board.label!r} | hint holds the board name: "
                 f"{app.board.label[0] in str(hint)} | frame holds it: "
                 f"{app.board.label[0] in scr._frame_text().plain}")
        await pilot.press("3")
        await pilot.pause()
        before = list(app.screen_stack)
        await pilot.press("question_mark")
        await pilot.pause()
        probe(3, f"`?` in view 3 changes the screen stack: {list(app.screen_stack) != before}")
        r = scr._render_all()
        lines = r.timeline.plain.split("\n")
        blank_tail = len(lines) - len(list(l for l in lines if l.strip())) if lines else 0
        probe(4, f"view-3 export: {len(lines)} rows x {r.timeline_w} cells | `⟦` in it: "
                 f"{'⟦' in r.timeline.plain} | 'project span' in it: "
                 f"{'project span' in r.timeline.plain} | trailing blank rows: "
                 f"{len(lines) - max(i for i, l in enumerate(lines) if l.strip()) - 1}")
        bound = {b.key for b in PresentScreen.BINDINGS for _ in [0]}
        keys = set()
        for b in PresentScreen.BINDINGS:
            keys.update(k.strip() for k in b.key.split(","))
        probe(5, f"K/J bound in R: {'K' in keys or 'J' in keys} | in KEYMAP: "
                 f"{any(k in {'K', 'J'} for e in keymap.KEYMAP for k in e.keys.split(','))} | "
                 f"reorder keys in R: {sorted(k for k in keys if 'shift' in k)}")


def keymap_probes():
    seat = {k for e in keymap.KEYMAP for k in e.keys.split(",")}
    home = {k for b in BoardsHome.BINDINGS for k in b.key.split(",")}
    pres = {k for b in PresentScreen.BINDINGS for k in b.key.split(",")}
    probe(1, f"`A` in KEYMAP: {'A' in seat} | in the home: {'A' in home} | in R: {'A' in pres}")


async def confirm_probe():
    home = TMP / "c" / ".taskboard"
    reg = mb.build(home, "main")
    app = TaskboardApp(board_path=home / "board.json",
                       registry=Registry.load(reg, home / "board.json"))
    msg = ("Archive Personal? It leaves the home; its folder is not touched. "
           "taskboard --board /x/boards/personal/board.json brings it back.")
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        got = []
        app.push_screen(modals.ConfirmModal(msg, confirm="Archive", variant="warning"), got.append)
        await pilot.pause()
        label = app.screen.query_one(".modal-title")
        rows = label.size.height
        await pilot.press("y")
        await pilot.pause()
        y_done = bool(got)
        await pilot.press("enter")
        await pilot.pause()
        probe(6, f"message rows on screen: {rows} for {len(msg)} chars in a "
                 f"{label.size.width}-cell label | `y` answers: {y_done} | `enter` answers: "
                 f"{bool(got)} | buttons: {[b.id for b in app.screen.query('Button')]}")


async def startup_probe():
    home = TMP / "s" / ".taskboard"
    reg = mb.build(home, "personal")
    app = TaskboardApp(board_path=home / "boards" / "personal" / "board.json",
                       registry=Registry.load(reg, home / "board.json"))
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        app.push_screen(modals.TeamIdentityPicker([{"id": "u1", "name": "username_subject"}]))
        await pilot.pause()
        title = str(app.screen.query_one(".modal-title").render())
        probe(7, f"label {app.board.label!r} | identity picker title names the board: "
                 f"{app.board.label[0] in title} | MilestoneOffer.__init__ takes "
                 f"{list(modals.MilestoneOffer.__init__.__code__.co_varnames[1:4])}")


async def twice_probe():
    home = TMP / "t" / ".taskboard"
    reg = mb.build(home, "personal")
    path = home / "boards" / "personal" / "board.json"
    one = TaskboardApp(board_path=path, registry=Registry.load(reg, home / "board.json"))
    two = TaskboardApp(board_path=path, registry=Registry.load(reg, home / "board.json"))
    async with one.run_test(size=(118, 30), notifications=True) as p1:
        await p1.pause()
        async with two.run_test(size=(118, 30), notifications=True) as p2:
            await p2.pause()
            notes = [str(n.message) for n in two._notifications]
            probe(8, f"second window on one board: notices {notes} | files under the home "
                     f"besides the boards: "
                     f"{sorted(p.name for p in home.rglob('*') if p.is_file() and 'board' not in p.name)}")


def register_probe():
    import argparse
    import taskboard.__main__ as entry
    Path.home = classmethod(lambda cls: TMP / "r")
    home = TMP / "r" / ".taskboard"
    mb.build(home, "main")
    copy = TMP / "r" / "elsewhere" / "board-copy.json"
    copy.parent.mkdir(parents=True)
    copy.write_bytes((home / "board.json").read_bytes())
    before = [e["id"] for e in json.loads((home / "boards.json").read_text("utf-8"))["boards"]]
    entry.open_app(str(copy))
    after = [e["id"] for e in json.loads((home / "boards.json").read_text("utf-8"))["boards"]]
    src = Path(entry.__file__).read_text(encoding="utf-8")
    probe(9, f"--board PATH registers: {before} -> {after} | `--open` in the CLI: {'--open' in src}")


def alt_probe():
    from textual._xterm_parser import XTermParser
    parser = XTermParser(debug=False)
    keys = [e.key for e in parser.feed("\x1bs") if hasattr(e, "key")]
    keys += [e.key for e in parser.feed("") if hasattr(e, "key")]
    probe(10, f"ESC s read by Textual 8.2.8's parser as: {keys}")


async def unmount_probe():
    seen = []

    class A(TaskboardApp):
        CSS_PATH = str(ROOT / "taskboard" / "taskboard.tcss")

        def on_unmount(self):
            seen.append("unmount")
    home = TMP / "u" / ".taskboard"
    app = A(board_path=home / "board.json")
    async with app.run_test(size=(80, 24)) as pilot:
        await pilot.pause()
    probe(11, f"an App subclass's on_unmount runs at exit: {seen == ['unmount']}")


async def export_probe():
    """P-4 on the prototype round's own boards (Client A), where the timeline is shorter
    than the frame."""
    sys.path.insert(0, str(ROOT / "prototypes" / "backlog_round"))
    import fixture as fx
    root = TMP / "x"
    fx.build(root, last="client-a")
    reg = Registry.load(root / "boards.json", root / "board.json")
    entry = reg.get("client-a")
    app = TaskboardApp(board_path=entry.path, registry=reg)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        if isinstance(app.screen, BoardsHome):
            await pilot.press("escape")
            await pilot.pause()
        await pilot.press("R", "3")
        await pilot.pause()
        r = app.screen._render_all()
        lines = r.timeline.plain.split(chr(10))
        last = max(i for i, l in enumerate(lines) if l.strip())
        probe("4b", f"Client A view-3 export: {len(lines)} rows x {r.timeline_w} cells, "
                    f"{len(lines) - last - 1} of them blank at the end | `⟦` in it: "
                    f"{'⟦' in r.timeline.plain}")


keymap_probes()
asyncio.run(present_probes())
asyncio.run(export_probe())
asyncio.run(confirm_probe())
asyncio.run(startup_probe())
asyncio.run(twice_probe())
register_probe()
alt_probe()
asyncio.run(unmount_probe())
