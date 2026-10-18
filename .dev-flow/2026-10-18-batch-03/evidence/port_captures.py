"""Real-app captures for batch 2026-10-18-batch-03, and the round's own code as their oracle.

The port of variant A (the operator's verdict of 2026-10-18 on `prototypes/backlog_polish/`)
is compared with the round's code, not with code this batch wrote:

    python port_captures.py --root <checkout> --mode round --out <dir>
        the round's own A looks of every item and scene, by its own `capture._look(item, "A")`
        and `capture._shot` — run on `base_ref` (620f58c) to show the re-run reproduces the
        round's committed A captures (P-6)
    python port_captures.py --root <checkout> --mode upto --k N --out <dir>
        the scenes below with the round's A forks of items 1..N composed (1 contrast, 2 hint80,
        3 notecap) — run on `base_ref`: what the port must paint after increment N
    python port_captures.py --root <checkout> --mode port --out <dir> [--png]
        the same scenes on the checkout as it is, no fork: the port; `--png` rasterises the
        118-column ones with the app's own `views.save_present_png`
    python port_captures.py --compare <dir A> <dir B>
        every SVG of A against its namesake in B, after the run-specific `terminal-<N>` class
        ids are normalised (the round's own acceptance test normalises them the same way)

Each capture is the real `TaskboardApp` headless on the synthetic notes board, the calendar
frozen, keys pressed as a presenter presses them (`capture._shot`). The composition reuses
the round's function bodies verbatim: `contrast_fork`'s fork is rebuilt over another inner
renderer (the same code object, its global `ORIG_RENDER` rebound), `cap_fork("fill")` and
`hint_fork(HINT_A)` are called as the round defines them.
"""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import importlib
import re
import sys
import types
from pathlib import Path

ORDER = ("contrast", "hint80", "notecap")
SIZES = [(118, 31), (80, 25)]
# (scene, keys pressed after `R` with the cursor on the notes board's CURSOR task)
SCENES = [("gantt", []), ("split", ["2"]), ("gantt-hidden", ["space"]),
          ("gantt-long", ["right", "right"]), ("split-long", ["right", "right", "2"])]


def _norm(svg: str) -> str:
    return re.sub(r"terminal-\d+", "terminal-N", svg)


def _load(root: Path):
    sys.path.insert(0, str(root / "prototypes" / "backlog_polish"))
    cap = importlib.import_module("capture")            # inserts root and root/tests itself
    assert Path(cap.__file__).resolve().parent == (root / "prototypes" / "backlog_polish").resolve()
    assert Path(cap.views.__file__).resolve().is_relative_to(root.resolve()), cap.views.__file__
    return cap


def _upto(cap, k: int):
    """(render, hint) with the round's A forks of items 1..k composed."""
    render = cap.ORIG_RENDER
    if k >= 3:
        render = cap.cap_fork("fill")
    if k >= 1:
        fork = cap.contrast_fork(cap.views.HEX["reached"])
        render = types.FunctionType(fork.__code__, {**fork.__globals__, "ORIG_RENDER": render},
                                    fork.__name__, fork.__defaults__, fork.__closure__)
    hint = cap.hint_fork(cap.HINT_A) if k >= 2 else cap.ORIG_HINT
    return render, hint


def _jobs(mode: str, cap, k: int):
    if mode == "round":
        for item in ORDER:
            render, hint = cap._look(item, "A")
            for scene, keys in cap.SCENES[item]:
                for w, h in SIZES:
                    yield f"{item}-A-{scene}-{w}x{h}", render, hint, (w, h), keys
        return
    render, hint = _upto(cap, k) if mode == "upto" else (cap.ORIG_RENDER, cap.ORIG_HINT)
    for scene, keys in SCENES:
        for w, h in SIZES:
            yield f"{scene}-{w}x{h}", render, hint, (w, h), keys


def run(root: Path, mode: str, out: Path, k: int, png: bool) -> None:
    cap = _load(root)
    out.mkdir(parents=True, exist_ok=True)
    for cid, render, hint, size, keys in _jobs(mode, cap, k):
        svg = out / f"{cid}.svg"
        asyncio.run(cap._shot(size, [("key", key) for key in keys], render, hint, svg))
        line = f"{cid}.svg {hashlib.sha256(_norm(svg.read_text(encoding='utf-8')).encode()).hexdigest()}"
        if png and size[0] == 118:
            p = cap.views.save_present_png(svg, svg.with_suffix(".png"), *cap._png_cells(svg, size))
            line += f" png {'written' if p else 'NOT written (Edge absent or failed)'}"
        print(line)


def compare(a: Path, b: Path) -> int:
    bad = 0
    for sa in sorted(a.glob("*.svg")):
        sb = b / sa.name
        if not sb.is_file():
            print(f"MISSING {sa.name} in {b}")
            bad += 1
            continue
        same = _norm(sa.read_text(encoding="utf-8")) == _norm(sb.read_text(encoding="utf-8"))
        print(f"{'EQUAL ' if same else 'DIFFER'} {sa.name}")
        bad += not same
    print(f"{bad} differ or missing")
    return 1 if bad else 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--root")
    ap.add_argument("--mode", choices=("round", "upto", "port"))
    ap.add_argument("--k", type=int, default=0)
    ap.add_argument("--out")
    ap.add_argument("--png", action="store_true")
    ap.add_argument("--compare", nargs=2)
    a = ap.parse_args()
    if a.compare:
        sys.exit(compare(Path(a.compare[0]), Path(a.compare[1])))
    run(Path(a.root), a.mode, Path(a.out), a.k, a.png)
