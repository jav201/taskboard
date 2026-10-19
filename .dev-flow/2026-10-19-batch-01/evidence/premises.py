"""P1 premise probes (batch 2026-10-19-batch-01), run on base_ref:
    python .dev-flow/2026-10-19-batch-01/evidence/premises.py   (from a checkout of base_ref)"""
import subprocess, sys, tempfile
from datetime import date
from pathlib import Path
sys.path.insert(0, "prototypes/present_portfolio")
import fixture as fx                      # noqa: E402
import portfolio_proto as P               # noqa: E402
from taskboard import views as V          # noqa: E402

print("HEAD", subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip())
b = fx.build(Path(tempfile.mkdtemp()) / "b.json")
rows = V.render_present(b, "pbm", "tb3", fx.TODAY, 118, 30).plain.split("\n")
print("P-1", [r for r in rows if "Cut-over weekend" in r][0])
hits = subprocess.run(["git", "grep", "-n", "present_rank", "--", "taskboard/"], capture_output=True, text=True).stdout
print("P-3 git grep present_rank taskboard/ ->", repr(hits))
rw = P.rail_w(80)
print("P-4 rail_w(80) =", rw, "· name cells =", rw - 8, "· _present_cols(80-rw-1) =", V._present_cols(80 - rw - 1, False))
svg, png = V.present_paths(b, None, date(2026, 10, 19), "all")
print("P-7", svg.name, png.name)
