r"""capture_surface_raster.py -- AC-5: the TRUE-RASTER side of a surface
posture, in a terminal that actually has a raster transport.

    python prototypes\capture_surface_raster.py corgi 8

WHAT IT IS FOR.  Everything else in this batch is measured headless, and
headless is exactly where the question AC-5 asks cannot be answered: whether
`textual_image` places a Sixel region correctly INSIDE a Textual layout under
ConPTY (spec premise P-4, hypothesis).  So this file is run in a real Windows
Terminal window, draws one language's `raster_region` on both paths at once,
and the window closes itself.

THE WINDOW CLOSES ITSELF, AND THAT IS NOT A CONVENIENCE.  Windows Terminal is
ONE PROCESS FOR ALL WINDOWS (tui-demos LIMITS L-19): `Stop-Process` on the
window a capture spawned kills every window the operator has open, including
the one the job was launched from.  It cost a session once.  So: the app runs
for `seconds` and exits on its own, and no automation here ever kills a
terminal process.

WHAT IT DRAWS.  Left: the glyph side (`res.rows`), which works anywhere.
Right: the true-raster side (`res.widget()`), which is `None` unless
`textual_image` reports sixel or TGP.  Both are the SAME `RenderResult`, so a
capture of this window is a capture of one posture rendered twice -- which is
what AC-3 claims and what a picture can actually check.

THE REGION IS A RESERVED RECTANGLE (CEILINGS section 7).  Both panes are given
a fixed `width`/`height` in cells and the screen does not scroll: the
compositor knows an image's size and never its content, so anything overlapping
or scrolling over the raster pane would be composited wrongly with no error.
The layout below is the honest form of that constraint, not a simplification.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

os.environ["TEXTUAL_ANIMATIONS"] = "none"

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "prototypes"))

from textual.app import App, ComposeResult                      # noqa: E402
from textual.containers import Horizontal, Vertical             # noqa: E402
from textual.widgets import Static                              # noqa: E402

import taskboard.language as LG                                 # noqa: E402
import taskboard.raster as RS                                   # noqa: E402
import taskboard.themes as TH                                   # noqa: E402
from capture_languages import SURFACE_H, test_image             # noqa: E402

REGION_W = 56                       # cells each pane reserves


class RasterProbe(App):
    CSS = """
    Screen { layout: vertical; }
    #head { height: 2; padding: 0 1; }
    #panes { height: 1fr; }
    .pane { width: 58; height: 1fr; padding: 0 1; }
    #shot { width: 56; height: 26; }
    """

    def __init__(self, lang: str, seconds: float):
        super().__init__()
        self.lang, self.seconds = lang, seconds
        self.kit = LG.kit(lang)
        self.res = self.kit.raster_region(test_image(), REGION_W, SURFACE_H,
                                          label="mbb rho final")

    def compose(self) -> ComposeResult:
        t = TH.THEMES[self.lang]
        yield Static(
            f"[b]{t['label']}[/b]  surface=[b]{self.res.posture}[/b]  "
            f"transport=[b]{RS.TRANSPORT}[/b]  "
            f"raster={'yes' if RS.raster_available() else 'NO'}\n"
            f"left: glyph side  |  right: textual_image  |  "
            f"reserved {self.res.reserved[0]}x{self.res.reserved[1]} cells",
            id="head")
        with Horizontal(id="panes"):
            with Vertical(classes="pane"):
                yield Static("\n".join(self.res.rows), markup=True)
            with Vertical(classes="pane"):
                w = self.res.widget()
                if w is None:
                    why = ("posture REFUSED (pixels is None)"
                           if self.res.pixels is None
                           else f"no raster transport (detected "
                                f"{RS.TRANSPORT!r})")
                    yield Static(f"[dim]no raster pane: {why}[/dim]")
                else:
                    w.id = "shot"
                    yield w

    def on_mount(self) -> None:
        self.screen.styles.background = TH.THEMES[self.lang]["ground"]
        # exits on its own -- see the module docstring on L-19
        self.set_timer(self.seconds, self.exit)


if __name__ == "__main__":
    lang = sys.argv[1] if len(sys.argv) > 1 else "corgi"
    secs = float(sys.argv[2]) if len(sys.argv) > 2 else 8.0
    RasterProbe(lang, secs).run()
