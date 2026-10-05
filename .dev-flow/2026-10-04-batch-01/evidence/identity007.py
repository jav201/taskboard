"""Hash every render the D-533 change must not touch: every view but the kanban
lanes, over sizes, selections and presentations, on the kg board (synthetic)."""
import hashlib
import inspect
import sys
from datetime import date

root = sys.argv[1]
sys.path.insert(0, root)
sys.path.insert(0, root + "/tests")
import kg_board                                   # noqa: E402
from taskboard import views                       # noqa: E402

b = kg_board.build()
params = inspect.signature(views.render_view).parameters
h = hashlib.sha256()
n = 0
ids = [None] + [t.id for t in b.tasks]
for mode in ("swimlanes", "agenda", "gantt", "kanban", "focus"):
    for (w, ht) in ((60, 20), (80, 24), (118, 30), (118, 40), (160, 40), (200, 50)):
        for sel in ids:
            pres = ["grouped", "matrix"] if mode == "kanban" else [None]
            for p in pres:
                kw = {"width": w, "height": ht, "today": kg_board.TODAY}
                if p is not None:
                    kw["presentation"] = p
                kw = {k: v for k, v in kw.items() if k in params}
                out = views.render_view(mode, b, False, sel, **kw)
                h.update(str(out).encode("utf-8"))
                n += 1
# card_cell's shipped law for every caller but the lanes (title_floor=0)
for t in b.tasks:
    for wc in range(0, 60):
        h.update(views.card_cell(t, b, wc, False, prefix="▊ ", badge=True,
                                 today=kg_board.TODAY).encode("utf-8"))
        h.update(views.card_cell(t, b, wc, True, today=kg_board.TODAY).encode("utf-8"))
        n += 2
print(n, h.hexdigest())
