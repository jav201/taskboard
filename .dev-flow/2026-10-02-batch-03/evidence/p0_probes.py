"""P0/P1 premise probes for batch 2026-10-02-batch-03 (run from the repo root):
    python .dev-flow/2026-10-02-batch-03/evidence/p0_probes.py [PROTO_DIR]
Oracle board only (tests/kg_board.py). PROTO_DIR (optional) is the kg_mejoras
prototype directory; when given, the chosen R-1b frame is re-rendered OVER THIS
TREE's taskboard package and measured with the same metric (the target)."""
import ast
import os
import sys
from pathlib import Path

ROOT = Path.cwd()
sys.path[:0] = [str(ROOT), str(ROOT / "tests"), str(Path(__file__).parent)]
import kg_board  # noqa: E402
from taskboard import views  # noqa: E402  (imported FIRST: the prototype reuses it)
from taskboard.views import KANBAN_BAND, kanban_order, nav_model, phase_buckets, render_view  # noqa: E402
from readability import body, readability  # noqa: E402

SIZES = ((118, 30), (80, 24))
SEL = "tw3"


def shipped(w, h):
    b = kg_board.build()
    lm = {}
    t = render_view("kanban", b, False, SEL, kg_board.TODAY, w, h, lm)
    return b, t.plain.split("\n"), lm


print("== P-1 shipped grouped kanban, oracle board, panel sizes, first h rows")
for w, h in SIZES:
    b, rows, lm = shipped(w, h)
    avg, full, shown = readability(body(rows, h), [t.title for t in b.tasks])
    heads = sum(r.count("▐ ") for r in rows)
    print(f"{w}x{h}: rows={len(rows)} avg/28={avg:.1f} full={full} drawn={shown} "
          f"cards_in_line_map={len(lm)} project_header_cells={heads} "
          f"high_dividers={sum(r.count('── high') for r in rows)}")

print("== P-2 the seat's open-high set (band=True), per column")
b = kg_board.build()
tasks = b.visible_tasks(False)
n = 0
projs = set()
for ph, bucket in zip(b.phases, phase_buckets(b, tasks)):
    g = kanban_order(b, bucket, False, band=True)
    hi = g[0][2] if g and g[0][0] == KANBAN_BAND else []
    n += len(hi)
    projs |= {t.project_id for t in hi}
    print(f"  {ph}: {[t.id for t in hi]}")
print(f"  total open highs={n} projects={len(projs)}")

print("== P-3 grouped nav: columns and the Done column")
cols = nav_model("kanban", b, False, kg_board.TODAY, 118, 30, selected_id=SEL)
print(f"  columns={len(cols)} sizes={[len(c) for c in cols]} last={cols[-1]}")

print("== P-4 the tab cycle in app.py")
src = (ROOT / "taskboard" / "app.py").read_text(encoding="utf-8")
fn = next(n for n in ast.walk(ast.parse(src))
          if isinstance(n, ast.FunctionDef) and n.name == "action_toggle_presentation")
tuples = [ast.literal_eval(n) for n in ast.walk(fn) if isinstance(n, ast.Tuple)
          and all(isinstance(e, ast.Constant) for e in n.elts)]
print(f"  {tuples[0]}")

print("== P-5 is_done is the last phase")
print("  ", [ (ph, b.is_done(next((t for t in b.tasks if t.phase == ph), None) or b.tasks[0]))
          for ph in b.phases])

if len(sys.argv) > 1:
    proto = Path(sys.argv[1])
    sys.path.insert(0, str(proto))
    import types
    # the round-7 module drags in every other round; R-1b reads two constants from it
    sys.modules["variants_polish"] = types.SimpleNamespace(ACCENT=views.HEX["accent"],
                                                           SEL_FG="#0b1220")
    import variants_reconcile as VR  # noqa: E402
    print("== P-6 the R-1b prototype frame re-rendered over this tree, same metric")
    for w, h in SIZES:
        b = kg_board.build()
        lm = {}
        text = VR.render(b, SEL, kg_board.TODAY, w, h, lm, mode="b", key="R-1b")
        rows = text.plain.split("\n")
        avg, full, shown = readability(body(rows, h), [t.title for t in b.tasks])
        print(f"{w}x{h}: avg/28={avg:.1f} full={full} drawn={shown} "
              f"pinned_rows={VR.STATS['R-1b']['pinned_rows']} hidden={VR.STATS['R-1b']['hidden']}")
    print("  (body rows only: rows[3:h], the fold row dropped; a match must cover the first word)")
