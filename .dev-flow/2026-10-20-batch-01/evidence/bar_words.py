import json, sys
sys.path.insert(0, sys.argv[1])
from taskboard.keymap import fit_bar
from taskboard.app import VIEW_ORDER
out = {}
for v in VIEW_ORDER:
    for layer in ("primary", "more"):
        for w in (80, 118, 160):
            entries, dropped = fit_bar(w, v, layer)
            out[f"{v}/{layer}/{w}"] = [[k, l] for k, l in entries] + ([["+", str(dropped)]] if dropped else [])
print(json.dumps(out, ensure_ascii=False))
