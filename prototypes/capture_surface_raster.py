r"""capture_surface_raster.py -- AC-5: the TRUE-RASTER side of a surface
posture, in a terminal that actually has a raster transport.

    python prototypes\capture_surface_raster.py corgi 8

WHAT IT IS FOR.  Everything else in this batch is measured headless, and
headless is exactly where the question AC-5 asks cannot be answered: whether
`textual_image` places a Sixel region correctly INSIDE a Textual layout under
ConPTY (spec premise P-4, hypothesis).  So this file is run in a real Windows
Terminal window, draws one language's `raster_region` on both paths at once,
and the window closes itself.

WHAT IT DRAWS.  Left: the glyph side (`res.rows`), which works anywhere.
Right: the true-raster side (`res.widget()`), which is `None` unless
`textual_image` reports sixel or TGP.  Both are the SAME `RenderResult`, so a
capture of this window is a capture of one posture rendered twice -- which is
what AC-3 claims and what a picture can actually check.

    python prototypes\capture_surface_raster.py corgi 8 over
    python prototypes\capture_surface_raster.py corgi 8 around

AND SINCE 2026-09-04, THE RIGHT PANE CARRIES THE POSTURE'S CHROME TOO.  That is
the whole of finding F-4: the first run of these captures showed corgi's
`[1] DISPLAY` box on the glyph side and a BARE raster pane beside it, because
`rows` fuses chrome and image while `pixels` is the glass alone.  `chrome` and
`image_box` (increment 4) give a consumer the frame separately, and this file is
the first consumer -- so the right pane is now the frame composited around the
widget rather than the widget alone.

THE THIRD ARGUMENT IS A QUESTION, NOT AN OPTION.  Spec premise P-3 asks whether
a transparent-cell sentinel can be composited around a `textual_image` widget in
a Textual layout, and CEILINGS section 7 predicts it cannot: a raster region is
drawn by the TERMINAL, not by the compositor, which knows the image's size and
never its content -- so z-order over it cannot be correct.  The two modes are
the two answers, and the capture decides between them:

  over    one Static holding ALL of `chrome`, holes included, with the image
          widget on a HIGHER LAYER at `image_box`.  This is P-3 read
          literally.  If the compositor cannot honour it the picture shows it
          directly -- the sentinel's own glyph left visible in the hole, or the
          raster landing somewhere other than the rectangle.

  around  `chrome` cut at the box's edges and set AROUND the reserved
          rectangle as its own widgets -- rows above, a band of (left cells |
          widget | right cells), rows below.  Nothing is ever drawn over the
          raster.  This is the fallback the premise table names, and it is the
          honest layout if `over` fails.

THE WINDOW CLOSES ITSELF, AND THAT IS NOT A CONVENIENCE.  Windows Terminal is
ONE PROCESS FOR ALL WINDOWS (tui-demos LIMITS L-19): `Stop-Process` on the
window a capture spawned kills every window the operator has open, including
the one the job was launched from.  It cost a session once.  So: the app runs
for `seconds` and exits on its own, and no automation here ever kills a
terminal process.

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

from rich.text import Text                                      # noqa: E402
from textual.app import App, ComposeResult                      # noqa: E402
from textual.containers import Container, Horizontal, Vertical  # noqa: E402
from textual.widgets import Static                              # noqa: E402

import taskboard.language as LG                                 # noqa: E402
import taskboard.raster as RS                                   # noqa: E402
import taskboard.themes as TH                                   # noqa: E402
from capture_languages import SURFACE_H, test_image             # noqa: E402

REGION_W = 56                       # cells each pane reserves
MODES = ("over", "around")


def band(row: str, x: int, w: int) -> str:
    """Cells `[x, x+w)` of a markup row, as markup.

    The same instrument `language._punch` measures with, and for the same
    reason: a markup row's `len()` counts its tags, so a column slice has to be
    taken on CELLS.  Used only by `around`, which needs the chrome to the left
    and to the right of the reserved rectangle as separate widgets."""
    return Text.from_markup(row).divide([x, x + w])[1].markup


class RasterProbe(App):
    CSS = """
    Screen { layout: vertical; }
    #head { height: 3; padding: 0 1; }
    #panes { height: 1fr; }
    .pane { width: 58; height: 1fr; padding: 0 1; }
    /* THE LAYER RULES ARE SCOPED TO `over` ON PURPOSE.  Written unscoped
       (`#shot { layer: glass; }`) they also matched the widget in `around`,
       which took it OUT OF FLOW inside its Horizontal: the pre-flight found
       all three children of the band starting at the same column, the glass
       overlapping the very bar it was supposed to sit beside.  A layer is a
       property of the composite, not of the widget. */
    #over { width: 56; height: 26; layers: frame glass; }
    #over > #chrome { layer: frame; width: 56; height: 26; }
    #over > #shot { layer: glass; }
    #around { width: 56; height: 26; }
    """

    def __init__(self, lang: str, seconds: float, mode: str = "over"):
        super().__init__()
        self.lang, self.seconds, self.mode = lang, seconds, mode
        # THE WINDOW NAMES ITSELF (tui-demos LIMITS L-27).  `wt.exe --title`
        # names the window before this process starts, but Textual sets the
        # terminal title from `App.title` once it is running and would
        # overwrite it -- so the same string is set HERE too, and the capture
        # harness's title selector keeps working either way.  Without this the
        # selector falls back to matching whatever Textual chose, which is the
        # class name, which every one of these captures would share.
        self.title = os.environ.get("SURFACE_SHOT_TITLE", "taskboard-surface")
        self.kit = LG.kit(lang)
        self.res = self.kit.raster_region(test_image(), REGION_W, SURFACE_H,
                                          label="mbb rho final")

    # -- the right pane: the posture's chrome WITH the glass in it -----------

    def composite(self):
        """The raster pane: `chrome` around `widget()`, in the chosen mode.

        Falls back to plain chrome whenever there is no glass to place -- a
        refusing posture or a terminal with no raster transport.  That is not a
        degraded rendering: for `refuse`, `chrome` IS `rows`, so what it draws
        is the complete posture."""
        w = self.res.widget()
        box = self.res.image_box
        if w is None or box is None:
            why = ("posture REFUSED (pixels is None)" if self.res.pixels is None
                   else f"no raster transport (detected {RS.TRANSPORT!r})")
            yield Static("\n".join(self.res.chrome) + f"\n[dim]{why}[/dim]",
                         markup=True)
            return
        x, y, bw, bh = box
        w.id = "shot"
        w.styles.width, w.styles.height = bw, bh
        if self.mode == "over":
            # P-3 read literally: the whole chrome on one layer, the glass on a
            # higher one, offset into the hole.  If CEILINGS section 7 is right
            # about z-order over a raster region, this is where it shows.
            with Container(id="over"):
                yield Static("\n".join(self.res.chrome), markup=True,
                             id="chrome")
                w.styles.offset = (x, y)
                yield w
        else:
            # the fallback: chrome cut at the box's edges, nothing drawn OVER
            # the rectangle.  Empty sides are omitted rather than yielded at
            # width 0 -- a zero-width widget is a layout the compositor has to
            # round, and rounding is what moves a reserved rectangle.
            #
            # EVERY SIZE HERE IS SET EXPLICITLY, and that is not belt-and-
            # braces.  The first draft left the side columns to `auto` and a
            # headless pre-flight found corgi's glass one cell LEFT of its
            # box -- the left bar's Static had not claimed its single column,
            # so the raster sat on top of the frame it was supposed to be
            # inside.  On corgi, which is the language AC-3 names.  A reserved
            # rectangle cannot be left to a layout rule to infer.
            ch = self.res.chrome
            mid = ch[y:y + bh]
            right = REGION_W - (x + bw)
            with Vertical(id="around"):
                if y:
                    top = Static("\n".join(ch[:y]), markup=True)
                    top.styles.width, top.styles.height = REGION_W, y
                    yield top
                band_row = Horizontal()
                band_row.styles.width, band_row.styles.height = REGION_W, bh
                with band_row:
                    if x:
                        lf = Static("\n".join(band(r, 0, x) for r in mid),
                                    markup=True)
                        lf.styles.width, lf.styles.height = x, bh
                        yield lf
                    yield w
                    if right:
                        rt = Static(
                            "\n".join(band(r, x + bw, right) for r in mid),
                            markup=True)
                        rt.styles.width, rt.styles.height = right, bh
                        yield rt
                if y + bh < len(ch):
                    bot = Static("\n".join(ch[y + bh:]), markup=True)
                    bot.styles.width = REGION_W
                    bot.styles.height = len(ch) - (y + bh)
                    yield bot

    def compose(self) -> ComposeResult:
        t = TH.THEMES[self.lang]
        yield Static(
            f"[b]{t['label']}[/b]  surface=[b]{self.res.posture}[/b]  "
            f"transport=[b]{RS.TRANSPORT}[/b]  "
            f"raster={'yes' if RS.raster_available() else 'NO'}\n"
            f"left: glyph side (rows)  |  right: chrome + textual_image  |  "
            f"reserved {self.res.reserved[0]}x{self.res.reserved[1]} cells\n"
            f"mode=[b]{self.mode}[/b]  image_box=[b]{self.res.image_box}[/b]",
            id="head")
        with Horizontal(id="panes"):
            with Vertical(classes="pane"):
                yield Static("\n".join(self.res.rows), markup=True)
            with Vertical(classes="pane"):
                yield from self.composite()

    def on_mount(self) -> None:
        self.screen.styles.background = TH.THEMES[self.lang]["ground"]
        # exits on its own -- see the module docstring on L-19
        self.set_timer(self.seconds, self.exit)


if __name__ == "__main__":
    lang = sys.argv[1] if len(sys.argv) > 1 else "corgi"
    secs = float(sys.argv[2]) if len(sys.argv) > 2 else 8.0
    mode = sys.argv[3] if len(sys.argv) > 3 else "over"
    if mode not in MODES:
        raise SystemExit(f"mode must be one of {MODES}, got {mode!r}")
    RasterProbe(lang, secs, mode).run()
