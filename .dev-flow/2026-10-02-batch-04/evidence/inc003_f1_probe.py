"""Code review F1 of increment 003 — the RED proof of AT-406's visibility clause.
Run from the repo root:  python -B .dev-flow/2026-10-02-batch-04/evidence/inc003_f1_probe.py

On the current tree, with the test's own helpers (`_app`, `_details`, `_rows`) and the
89-character name, evaluates at 80x24 and 80x12 (where the box cannot hold five rows):
  old  — `all(y inside the box for painted field rows)`: vacuous, rows come from the box
  new  — the painted field labels, in order, equal all five FIELDS
The new clause must be True at 80x24 and False at 80x12; the old one is True at both."""
import asyncio
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, "tests")
import test_details_grid as g                                    # noqa: E402


async def judge(size):
    d = Path(tempfile.mkdtemp())
    app = g._app(d, name=g.LONG)
    async with app.run_test(size=size) as pilot:
        await g._details(app, pilot)
        rows = g._rows(app)
        box = app.screen.query_one("#details-box").region
        firsts = [t.strip().split(" ")[0] for _, t in rows]
        old = all(box.y <= y < box.y + box.height
                  for y, t in rows if t.strip().split(" ")[0] in g.FIELDS)
        painted = [f for f in firsts if f in g.FIELDS]
        new = painted == g.FIELDS
        print(f"{size[0]}x{size[1]}: painted field labels {painted} | old clause {old} | new clause {new}")


async def main():
    for size in ((80, 24), (80, 12)):
        await judge(size)


asyncio.run(main())
