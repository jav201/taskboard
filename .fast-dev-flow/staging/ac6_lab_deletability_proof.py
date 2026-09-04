"""AC-6 -- the lab's two workarounds are DELETABLE.

Renders emersio-lab's blueprint chrome twice, in a throwaway copy of the lab:
  BEFORE - the lab's own `_blueprint_titleblock()` and `_cell_span()`
  AFTER  - the kit's new `stamp()` and the `label` `raster_region()` now reads
and diffs the two.  `tui-demos` is never written to.
"""
import sys, types
from dataclasses import dataclass
sys.path.insert(0, r"C:\Users\jjgh8\Github\taskboard\.claude\worktrees\kanban-variants")
sys.path.insert(0, "C:/Users/jjgh8/AppData/Local/Temp/lab-emersio-ac6")

import languages as L
from rich.text import Text
from PIL import Image

k = L.kit("blueprint")


@dataclass
class St:
    penal: float = 3.0
    rmin: float = 1.5
    volfrac: float = 0.4
    run: int = 7
    max_iter: int = 40
    hist: list = None
    status: str = "converged"
    grid: object = None


st = St(hist=[1.0, .62, .40, .28, .19, .13])
st.grid = types.SimpleNamespace(shape=(20, 60))
p = L.plan("blueprint", "sixel", "sixel", (60, 20), 110, 40)
W, H = p.controls.w, p.controls.h

# ---------------------------------------------------------------- BEFORE
before_block = L._blueprint_titleblock(k, st, W, H)
before_span = L._cell_span(k, p)

# ---------------------------------------------------------------- AFTER
# the whole replacement for `_blueprint_titleblock`: content as data.
def after_titleblock(k, st, w, h):
    shape = f" {st.grid.shape[1]}x{st.grid.shape[0]}" if st.grid is not None else ""
    rows = [[("", f"EMERSIO  MBB{shape}", False)]
            + [(n, f.format(getattr(st, a)), False) for n, a, f in L.PARAMS],
            [("ITER", f"{len(st.hist)}/{st.max_iter}", False),
             ("C", f"{st.hist[-1]:.3f}" if st.hist else "-", False),
             ("REV", f"{st.run:02d}", False),
             ("", st.status.upper(), True)]]
    return k.stamp(rows, w)[:h]

after_block = after_titleblock(k, st, W, H)
# and the whole replacement for `_cell_span`: pass the datum as the label.
img = Image.new("L", L.IMAGE_PX)
after_res = k.raster_region(img, p.field.w, p.field.h,
                            label=f"{p.src[0]} x {p.src[1]} CELLS")
after_span = after_res.rows[0]

pl = lambda s: Text.from_markup(s).plain

print(f"seat: controls {W} x {H}   field {p.field.w} x {p.field.h}")
print("\n=== THE CELL SPAN (L-31) ===")
print(f"  BEFORE (lab, `_cell_span`, drawn one row ABOVE the region)\n    {pl(before_span)!r}")
print(f"  AFTER  (kit, inside the reserved region)\n    {pl(after_span)!r}")
print(f"  image_box now {after_res.image_box}  (was (0, 1, ...) with no label)")

print("\n=== THE TITLE BLOCK (L-32) ===")
for tag, rows in (("BEFORE (lab, `_blueprint_titleblock`)", before_block),
                  ("AFTER  (kit, `stamp(rows, w)`)", after_block)):
    print(f"  {tag}")
    for r in rows:
        print(f"    |{pl(r)}|")

print("\n=== DIFF ===")
b, a = [pl(r) for r in before_block], [pl(r) for r in after_block]
print(f"  rows: {len(b)} -> {len(a)}")
for i in range(max(len(b), len(a))):
    x, y = (b[i] if i < len(b) else None), (a[i] if i < len(a) else None)
    if x != y:
        print(f"  row {i} differs")
        print(f"    - {x!r}")
        print(f"    + {y!r}")

print("\n=== CONTENT AND MARKS (what must NOT differ) ===")
import re
tok = lambda rows: sorted(re.findall(r"[A-Z0-9][A-Z0-9./]*", " ".join(pl(r) for r in rows)))
print(f"  tokens BEFORE: {tok(before_block)}")
print(f"  tokens AFTER : {tok(after_block)}")
print(f"  same content: {tok(before_block) == tok(after_block)}")
knock_b = "".join(before_block).count(" on ")
knock_a = "".join(after_block).count(" on ")
print(f"  knockouts: before={knock_b} after={knock_a}")
glyph = lambda rows: {c for c in "".join(pl(r) for r in rows)
                      if not (c.isalnum() or c in " -/.:")}
print(f"  glyphs BEFORE: {sorted(glyph(before_block))}")
print(f"  glyphs AFTER : {sorted(glyph(after_block))}")
print(f"  outside the language's ten: {sorted(glyph(after_block) - k.glyphs)}")