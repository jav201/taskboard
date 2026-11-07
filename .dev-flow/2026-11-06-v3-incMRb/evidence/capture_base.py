"""E4 — capture MR-b's base oracle on `8ca174c` (run once, BEFORE any MR-b code exists).

    python -I capture_base.py <tree at 8ca174c> <this branch's tests/> <out.json>

The tree's `taskboard` is imported first (its `__file__` is printed and stored);
the helper modules come from this branch's `tests/`. Writes, for fixture MR-F:
- `deck_l0`  — sha256 of the `x` deck built by the export's own three calls, views 1-3;
- `deck_app` — sha256 of the deck file the real app writes on `x`, views 1-3 (118x30);
- `rows`     — views 1/2: header, ruler and legend strip lines (0-3); view 3: header
               and ruler lines (0-2) of the timeline; cursor `tm2`; 118x30 and 80x24;
- `hint`     — the hint row the app paints in views 1, 2, 3 at 118x30 and 80x24;
- `keys_window` — `?`'s `#pk-text` per view, and `PresentKeys(view).lines()` per view;
- `bindings` — PresentScreen's (key, action) pairs.
"""
from __future__ import annotations

import asyncio
import json
import sys
import tempfile
from datetime import date
from pathlib import Path

tree, tests, out = sys.argv[1:4]
sys.path[:0] = [tree, tests]
import taskboard  # noqa: E402

print("taskboard.__file__ =", taskboard.__file__)
assert Path(taskboard.__file__).resolve().is_relative_to(Path(tree).resolve()), taskboard.__file__

import milestone_row_fixture as fx  # noqa: E402
import milestone_row_present_fixture as mp  # noqa: E402
from taskboard import app as app_module, modals, models, views  # noqa: E402
from taskboard.app import PresentScreen  # noqa: E402


class _Today(date):
    @classmethod
    def today(cls):
        return fx.TODAY


for mod in (app_module, models, views, modals):
    mod.date = _Today

gold: dict = {"base": "8ca174c", "taskboard_file": taskboard.__file__,
              "deck_l0": {}, "deck_app": {}, "rows": {}, "hint": {}, "keys_window": {},
              "keys_lines": {}, "bindings": []}

for v in (1, 2, 3):
    gold["deck_l0"][str(v)] = mp.sha(mp.deck_bytes(fx.board(), v))

for W, H in mp.SIZES:
    b = fx.board()
    for view in mp.VIEWS12:
        gold["rows"][f"{view}-{W}x{H}"] = mp.frame(b, "ppr", "tm2", W, H, view).lines[:4]
    gold["rows"][f"all-{W}x{H}"] = mp.frame3(b, ("task", "tm2"), W, H)[0].lines[:3]

gold["bindings"] = sorted({(k.strip(), bd.action) for bd in PresentScreen.BINDINGS
                           for k in bd.key.split(",")})
for view in ("gantt", "split", "all"):
    gold["keys_lines"][view] = modals.PresentKeys(view).lines().plain


async def run_app():
    for size in mp.SIZES:
        with tempfile.TemporaryDirectory() as d:
            home = Path(d) / ".taskboard"
            Path.home = classmethod(lambda cls, _d=d: Path(_d))
            async with mp.present(home, size, sel="tm2") as (app, pilot):
                for v in (1, 2, 3):
                    await mp.keys(pilot, str(v))
                    gold["hint"][f"{v}-{size[0]}x{size[1]}"] = mp.hint(app)
                    if size == (118, 30):
                        await mp.keys(pilot, "question_mark")
                        c = app.screen.query_one("#pk-text").content
                        gold["keys_window"][str(v)] = c.plain if hasattr(c, "plain") else str(c)
                        await mp.keys(pilot, "escape")
                        await mp.keys(pilot, "x")
                        name = (f"present-{fx.TODAY.isoformat()}.html" if v == 3 else
                                f"present-pilot-rollout-{fx.TODAY.isoformat()}.html")
                        path = home / "reports" / name
                        gold["deck_app"][str(v)] = mp.sha(path.read_bytes())
                        path.unlink()


asyncio.run(run_app())
Path(out).write_text(json.dumps(gold, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, {k: (len(v) if hasattr(v, "__len__") else v) for k, v in gold.items()})
