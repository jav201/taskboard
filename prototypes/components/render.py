"""render.py -- the six screens through five kits, headless, 30 frames.

    python -X utf8 prototypes/components/render.py

THE RENDER PATH IS NOT REIMPLEMENTED HERE.  `settle`, `cell_grid` and
`svg_from_grid` are IMPORTED from `prototypes/capture_languages.py`, which is
the module the gallery's own board/gallery/surface frames were taken with.
That is the spec's "rendered through the kit path" taken literally: if these
frames were produced by a second renderer they would not be comparable with
the ones already in `prototypes/gallery/`, and the whole point of a sweep is
that its frames can be laid beside each other.

`capture_languages` has an `if __name__ == "__main__"` guard, so importing it
runs nothing -- unlike `verify_language.py`, which is why that one is quoted
from rather than imported (see the sweep's `settle` docstring).

WHAT IS DIFFERENT FROM THE BOARD SWEEP, and why.  The board sweep drives the
real `TaskboardWidget` and photographs a live app.  These six screens are not
screens the app HAS -- they are the canonical screens every terminal app
needs, which is the question this round was asked.  So the frame is composed
from kit calls and mounted in a bare `Static`, exactly as `sweep_surfaces()`
does for the surface axis, and for the same stated reason: photographing a
primitive no screen consumes yet must not require wiring it into a screen.
"""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "prototypes"))
sys.path.insert(0, str(HERE))

import capture_languages as CAP                                  # noqa: E402
import taskboard.themes as TH                                    # noqa: E402
import screens as S                                              # noqa: E402

LANGS = ["corgi", "blueprint", "prism", "naught", "ledger"]
SIZE = (S.W, S.H)
OUT = HERE


async def one(lang: str, screen: str):
    from textual.app import App, ComposeResult
    from textual.widgets import Static

    sh = S.build(lang, screen)
    body, over = sh.body()

    class Frame(App):
        CSS = ("Screen { layout: vertical; overflow: hidden; }\n"
               "#f { padding: 0; width: 100%; height: 100%; }")

        def compose(self) -> ComposeResult:
            yield Static(body, id="f", markup=True)

    app = Frame()
    async with app.run_test(size=SIZE) as pilot:
        await pilot.pause()
        app.screen.styles.background = TH.THEMES[lang]["ground"]
        rows = await CAP.settle(pilot, app, f"{lang} {screen}")
        name = f"{lang}_{screen}"
        title = f"taskboard · {lang} · {screen} {S.TITLES[screen]}"
        # the RECTANGLE LAW: every row padded to the widest, never clipped
        w = max(len(r) for r in rows)
        rect = [r.ljust(w) for r in rows]
        (OUT / f"{name}.txt").write_text("\n".join(rect) + "\n",
                                         encoding="utf-8")
        grid, ground = CAP.cell_grid(app)
        (OUT / f"{name}.svg").write_text(
            CAP.svg_from_grid(grid, ground, title), encoding="utf-8")
    return sh, (w, len(rect), CAP.ink(rect)), over


VERDICT_ORDER = {"refused": 0, "evoked": 1}


def candidates_md(lang: str, screen: str, sh) -> str:
    """The sidecar.  One section per hand-drawn element, with the row numbers
    it occupies -- which is HOW the element is marked.

    A marker glyph inside the frame was considered and rejected: the operator
    is judging these frames as designs, and a gutter column of `°` would be
    ink this language did not choose to spend.  Row numbers are exact, they
    cost the design nothing, and they point at the `.txt` -- which is the
    artifact any law measures.
    """
    k = sh.k
    out = [f"# {lang} · {screen} — {S.TITLES[screen]} — candidates",
           "",
           f"Frame: `{lang}_{screen}.txt` / `.svg` — {S.W}×{S.H}, rendered "
           f"through `taskboard.language.kit(\"{lang}\")`.",
           "",
           "Every element below was drawn **by hand in "
           "`prototypes/components/screens.py`**, not by a kit method. "
           "Everything else in the frame came out of a kit call and is "
           "therefore *implemented*. Verdicts are the spec's closed set: "
           "**implemented / evoked / refused**.",
           ""]
    if not sh.cands:
        out += ["## Nothing was drawn by hand",
                "",
                "This screen is composed entirely of kit primitives in this "
                "language. Every element is *implemented*.", ""]
        return "\n".join(out)

    items = sorted(sh.cands.values(),
                   key=lambda t: (VERDICT_ORDER.get(t[0].verdict, 2),
                                  t[0].name))
    for cd, rows in items:
        where = (", ".join(str(r) for r in rows) if rows
                 else "— nothing is drawn; that is the answer")
        out += [f"## `{cd.name}` — **{cd.verdict}**",
                "",
                f"- **element drawn:** {cd.element}",
                f"- **frame rows:** {where}",
                f"- **proposed signature:** `{cd.sig}`",
                f"- **the commitment it must honour:** {cd.commitment}",
                ""]
    return "\n".join(out)


async def sweep():
    report = []
    for lang in LANGS:
        for screen in S.SCREENS:
            sh, (w, h, ink), over = await one(lang, screen)
            name = f"{lang}_{screen}"
            cand_n = len(sh.cands)
            # ALWAYS WRITTEN, INCLUDING WHEN THERE IS NOTHING TO DECLARE
            # (kits-learn-3 close). Writing it only when `cand_n` left the
            # sidecars of frames that had become clean STALE ON DISK, still
            # claiming elements the kit now draws -- a sidecar that survives
            # the thing it describes is worse than no sidecar, because it is
            # the file the matrix's readers trust. `candidates_md` already
            # had the empty case written for it.
            (OUT / f"{name}.candidates.md").write_text(
                candidates_md(lang, screen, sh), encoding="utf-8")
            verdicts = [c.verdict for c, _ in sh.cands.values()]
            report.append(dict(lang=lang, screen=screen, w=w, h=h, ink=ink,
                               cands=cand_n,
                               refused=verdicts.count("refused"),
                               evoked=verdicts.count("evoked")))
            print(f"  {name:<20} {w}x{h} {ink:5.1f}% ink   "
                  f"{cand_n} candidates "
                  f"({verdicts.count('refused')} refused, "
                  f"{verdicts.count('evoked')} evoked)"
                  + (f"   CLIPPED {over}" if over else ""))
    return report


def main() -> int:
    print(f"{len(LANGS)} languages x {len(S.SCREENS)} screens | "
          f"viewport {S.W}x{S.H} | animations off")
    report = asyncio.run(sweep())

    if len(report) != len(LANGS) * len(S.SCREENS):
        print("INCOMPLETE SWEEP", file=sys.stderr)
        return 1

    # THE SWEEP'S OWN LAW, the board sweep's applied one axis over: for each
    # screen, no two languages may render byte-identically.  Two languages
    # agreeing on a whole screen is the exact defect LANGUAGES.md records.
    bad = []
    for screen in S.SCREENS:
        got = {L: (OUT / f"{L}_{screen}.txt").read_text(encoding="utf-8")
               for L in LANGS}
        for i, a in enumerate(LANGS):
            for b in LANGS[i + 1:]:
                if got[a] == got[b]:
                    bad.append((screen, a, b))
    if bad:
        print(f"IDENTICAL FRAMES: {bad}", file=sys.stderr)
        return 1

    n_txt = len(list(OUT.glob("*_S?.txt")))
    n_svg = len(list(OUT.glob("*_S?.svg")))
    n_cnd = len(list(OUT.glob("*.candidates.md")))
    print(f"\n  {n_txt} .txt + {n_svg} .svg -> {OUT}")
    print(f"  {n_cnd} candidates files")
    print(f"  no two frames identical within a screen "
          f"({len(S.SCREENS) * len(LANGS) * (len(LANGS) - 1) // 2} pairs)")
    tot = sum(r["cands"] for r in report)
    print(f"  {tot} hand-drawn elements declared "
          f"({sum(r['refused'] for r in report)} refused, "
          f"{sum(r['evoked'] for r in report)} evoked)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
