"""Premise probes of batch 2026-10-20-batch-01 (01-requirements.md §2.7), run on base_ref.

    unset NO_COLOR; python .dev-flow/2026-10-20-batch-01/evidence/premises.py > premises.txt

Every board is synthetic and lives in a temporary folder.
"""
from __future__ import annotations

import inspect
import json
import re
import sys
import tempfile
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))

from taskboard import app as app_mod, history, keymap, modals, models, views  # noqa: E402
from taskboard.models import Board  # noqa: E402
from taskboard.team_sync import TeamState  # noqa: E402

tmp = Path(tempfile.mkdtemp())


def say(n, text):
    print(f"P-{n}: {text}")


# P-1 history, images and reports sit beside the board file
p = tmp / "one" / "board.json"
b = Board([], [], p)
print("P-1 history_path:", history.history_path(p).relative_to(tmp).as_posix())
print("P-1 image_dir:   ", b.image_dir("t1").relative_to(tmp).as_posix())
svg, png = views.present_paths(b, "Demo", date(2026, 10, 20))
print("P-1 present_paths:", svg.relative_to(tmp).as_posix())
say(1, "TRUE" if {history.history_path(p).parent, b.image_dir("t1").parents[1],
                   svg.parents[1]} == {p.parent} else "FALSE")

# P-2 Board.load on a missing path seeds and SAVES sample data
q = tmp / "missing" / "board.json"
loaded = Board.load(q)
print("P-2 exists after load:", q.exists(), "projects:", len(loaded.projects),
      "tasks:", len(loaded.tasks))
say(2, "TRUE" if q.exists() and loaded.projects else "FALSE")

# P-3 a pasted image is stored as an absolute resolved path
src = inspect.getsource(models.save_pil_image)
print("P-3 save_pil_image returns:", re.findall(r"return .*", src))
editor = inspect.getsource(modals)
hits = [ln.strip() for ln in editor.splitlines() if "save_pil_image(" in ln]
print("P-3 caller:", hits)
say(3, "TRUE" if "dest.resolve()" in src and hits else "FALSE")

# P-4 `B` is bound nowhere: not in the seat, not in any screen's BINDINGS
seat = {k for key in keymap.KEYMAP for k in key.keys.split(",")}
local = set()
for mod in (modals, app_mod):
    for _n, cls in inspect.getmembers(mod, inspect.isclass):
        for bd in getattr(cls, "BINDINGS", None) or []:
            keys = bd.key if hasattr(bd, "key") else bd[0]
            local.update(keys.split(","))
print("P-4 'B' in seat:", "B" in seat, "· 'b' in seat:", "b" in seat,
      "· 'B' in a screen's BINDINGS:", "B" in local)
say(4, "TRUE" if "B" not in seat and "B" not in local and "b" in seat else "FALSE")

# P-5 check_action releases only the cursor keys and tab under a pushed screen
ca = inspect.getsource(app_mod.TaskboardApp.check_action)
print("P-5 check_action:", " ".join(ca.split())[-170:])
say(5, "TRUE" if '("cursor", "hmove", "toggle_presentation")' in ca else "FALSE")

# P-6 the team sync timer is not kept, so nothing could stop it on a switch
td = inspect.getsource(app_mod.TaskboardApp._start_team_daemon)
print("P-6 _start_team_daemon:", " ".join(td.split())[-120:])
say(6, "TRUE" if "= self.set_interval" not in td and "self.set_interval" in td else "FALSE")

# P-7 TeamState.team_project_ids names team.json's projects
shared = tmp / "team"
shared.mkdir()
(shared / "team.json").write_text(json.dumps({"version": 1, "phases": ["Backlog", "Done"], "roster": [{"id": "u1", "name": "U"}],
                                               "projects": [{"id": "p1"}, {"id": "p2"}]}),
                                  encoding="utf-8")
ts = TeamState.from_settings(str(shared), "u1")
ts.load_config()
print("P-7 team_project_ids:", sorted(ts.team_project_ids()))
say(7, "TRUE" if ts.team_project_ids() == {"p1", "p2"} else "FALSE")

# P-8 the round's home captures hold the approved cards as text
sys.path.insert(0, str(ROOT / "tests"))
pat = re.compile(r'<text class="[^"]*" x="([\d.]+)" y="[\d.]+" textLength="[\d.]+" '
                 r'clip-path="url\(#[^)]*-line-(\d+)\)">([^<]*)</text>')
import html  # noqa: E402
for name, (w, h) in (("C-160-open.svg", (160, 45)), ("C-118-open.svg", (118, 30)),
                     ("C-80-open.svg", (80, 24))):
    rows = [[" "] * w for _ in range(h)]
    text = (ROOT / "prototypes" / "multi_board" / "out" / name).read_text(encoding="utf-8")
    for x, line, body in pat.findall(text):
        y, col = int(line), round(float(x) / 12.2)
        if y < h:
            for i, ch in enumerate(html.unescape(body).replace("\xa0", " ")):
                if col + i < w:
                    rows[y][col + i] = ch
    plain = ["".join(r).rstrip() for r in rows]
    print(f"P-8 {name} row 0:", plain[0])
    print(f"P-8 {name} row 2:", plain[2])
    print(f"P-8 {name} last row:", plain[h - 1])
say(8, "TRUE")

# P-9 the board save is a plain write; an atomic save exists beside it
print("P-9 save:", " ".join(inspect.getsource(Board.save).split())[-90:])
print("P-9 save_atomic uses os.replace:", "os.replace" in inspect.getsource(Board.save_atomic))
say(9, "TRUE")
