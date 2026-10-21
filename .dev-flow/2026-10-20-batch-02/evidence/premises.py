"""Premise probes P-1..P-7 for batch 2026-10-20-batch-02, run on base_ref (b1b71e4).
Synthetic data only, every path under a temporary folder; the real home is never read:
`Path.home` and the environment's HOME/USERPROFILE are both pointed at temporary folders."""
import inspect, json, os, sys, tempfile
from datetime import datetime
from pathlib import Path

sys.path.insert(0, os.getcwd())
tmp = Path(tempfile.mkdtemp(prefix="premises-"))
seam, env_home = tmp / "seam-home", tmp / "env-home"
seam.mkdir(); env_home.mkdir()
os.environ["HOME"] = os.environ["USERPROFILE"] = str(env_home)
Path.home = classmethod(lambda cls: seam)

from taskboard import boards, models, modals
from taskboard.boards import Registry, move_plan, move_project, peek_board
from taskboard.models import Board, Project, Task, set_present_order, present_order

# P-1: `~` in boards.py resolves through the environment, not Path.home()
print("P-1 Path.home():", Path.home() == seam,
      "| expanduser('~/x') under the seam home:", Path("~/x").expanduser().parent == seam,
      "| boards._key('~/x') under the env home:",
      boards._key("~/x").startswith(os.path.normcase(str(env_home.resolve()))))

# P-2: two registries loaded from one file: the second writer drops the first's board
d = tmp / "p2"; d.mkdir()
main = d / "board.json"; Board([], [], main).save_atomic()
reg_path = d / "boards.json"
Registry.load(reg_path, main).register(d / "side" / "notes.json")
a, b = Registry.load(reg_path, main), Registry.load(reg_path, main)
a.create("From A", "lime", datetime(2026, 10, 20, 9, 30), {})
b.edit("notes", "Notes renamed", "blue")
ids = [e["id"] for e in json.loads(reg_path.read_text(encoding="utf-8"))["boards"]]
print("P-2 ids on disk after A creates and B (loaded before) edits:", ids,
      "| A's board lost:", "from-a" not in ids)

# P-3: a move rewrites the source history.jsonl and leaves no copy of it
d = tmp / "p3"; (d / "src").mkdir(parents=True); (d / "dst").mkdir()
src = Board([Project("Moving", id="pm")], [Task("t", id="t1", project_id="pm", phase="Backlog")],
            d / "src" / "board.json"); src.save_atomic()
Board([], [], d / "dst" / "board.json").save_atomic()
(d / "src" / "history.jsonl").write_bytes(b'{"task": "t1", "to": "Doing"}\n{"task": "x"}\n')
s, t = Board.load(d / "src" / "board.json"), peek_board(d / "dst" / "board.json")
plan = move_plan(s, t, "pm", set(), set())
_, steps = move_project(s, t, "pm", plan, "2026-10-20", ("A", "B"))
print("P-3 steps:", steps, "| history copies:",
      sorted(p.name for p in (d / "src").iterdir() if p.name.startswith("history.jsonl.")))

# P-4: an archived project keeps its rank; a reorder while it is archived re-ranks
# the visible ones only, so unarchiving ties two ranks
b4 = Board([Project(n, id=n) for n in ("pa", "pb", "pc")], [], tmp / "p4.json")
set_present_order(b4, ["pa", "pb", "pc"])
b4.project_by_id("pa").archived = True
set_present_order(b4, ["pc", "pb"])
b4.project_by_id("pa").archived = False
print("P-4 ranks:", {p.id: p.present_rank for p in b4.projects},
      "| order:", [p.id for p in present_order(b4)])

# P-5: ProjectPicker._move_target never reads its third parameter
src5 = inspect.getsource(modals.ProjectPicker._move_target)
print("P-5 signature:", inspect.signature(modals.ProjectPicker._move_target),
      "| `_boards` read in the body:", src5.count("_boards") > 1)

# P-6: an exclusive create on this filesystem refuses a second creator
lock = tmp / "x.lock"
fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY); os.close(fd)
try:
    os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    print("P-6 second O_EXCL create: succeeded")
except FileExistsError:
    print("P-6 second O_EXCL create: FileExistsError")

# P-7: Textual's public `border_title` is the markup string; its parse is the title's text
from rich.text import Text
from textual.widgets import Static
w = Static()
w.border_title = Text("▶ [@click=app.quit]x[/]")
print("P-7 public border_title:", repr(w.border_title),
      "| Text.from_markup(...).plain:", repr(Text.from_markup(w.border_title).plain))
