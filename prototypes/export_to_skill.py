"""export_to_skill.py -- regenerate the tui-design skill's language assets from
the running implementation.

    python prototypes/export_to_skill.py [SKILL_DIR]

WHY THIS EXISTS.  The skill's `assets/languages.py` drifted badly from the code
that actually renders these languages, and the drift was invisible until someone
went looking: the app rendered ten languages, the skill listed eight; Solari and
Blueprint had never reached the skill at all; Ledger existed there only as an
imported picture, not as a language; and phosphor and bbs, retired from the
prototype on 2026-07-26 by operator curation, were still being offered as
implemented.  Worse, the skill's token dicts held colour and a few structural
keys that NO renderer read -- which is precisely the failure `LANGUAGES.md`
itself names ("A language definition is code, not a manifest").  The skill was
preaching what its own asset broke.

A hand-written copy drifts again the moment either side moves.  So the asset is
a PROJECTION of the implementation, produced here, and the file it writes says
so in its own header along with the command that rebuilds it.

WHAT IT WRITES.  One file, `<skill>/assets/languages.py`, containing:

  LANGUAGES  every token of every language, exactly as `themes.py` holds them
  FAMILY     each language's board layout family, from `Kit.board_layout()`
  DOC        each Kit's class docstring -- the doctrine, from the code
  ORDER      the ten, in the order the app cycles them
  RETIRED    the two the operator removed, with the reason, so the skill can
             still OFFER them as design options while being honest that the
             reference implementation no longer renders them

WHAT IT DELIBERATELY DOES NOT DO.  It does not touch `LANGUAGES.md`.  The
catalogue is prose that argues; a generator would flatten it into a data dump
and lose the part that teaches.  The doctrine is carried into the asset via
DOC so a reader has both, and the prose is edited by hand.
"""
from __future__ import annotations

import inspect
import sys
from pathlib import Path

from rich.text import Text

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import taskboard.language as LG                                   # noqa: E402
import taskboard.themes as TH                                     # noqa: E402

DEFAULT_SKILL = Path.home() / ".claude" / "skills" / "tui-design"

# The two the operator retired from the prototype on 2026-07-26.  They are not
# deleted here: a retired IMPLEMENTATION is not an invalid design language, and
# the skill's job is to offer options.  What would be dishonest is listing them
# as though a kit still rendered them.
RETIRED = {
    "phosphor": ("one hue at many lightnesses (amber/green CRT); severity must "
                 "ride brightness and glyph, never a second hue",
                 "retired from the reference app 2026-07-26 by operator "
                 "curation -- still a valid language to choose"),
    "bbs": ("full 16 colours, solid ink, double-line box drawing, "
            "block-gradient shading (ANSI/BBS art)",
            "retired from the reference app 2026-07-26 by operator "
            "curation -- still a valid language to choose"),
}

HEADER = '''r"""languages.py -- the ten visual languages, AS IMPLEMENTED.

DO NOT EDIT BY HAND.  This file is generated from the reference implementation
by `prototypes/export_to_skill.py` in the taskboard repo:

    cd {root}
    $env:PYTHONIOENCODING = "utf-8"
    python prototypes\\export_to_skill.py

WHY IT IS GENERATED.  The previous hand-written version drifted from the code
without anyone noticing: it listed eight languages where the app rendered ten,
it had never heard of Solari or Blueprint, it kept offering phosphor and bbs as
implemented after they were retired, and its structural tokens were read by no
renderer at all -- the exact "a language definition is code, not a manifest"
failure LANGUAGES.md warns about, committed by the file the doc points at.

WHAT EACH NAME MEANS

    LANGUAGES  every token, as `themes.py` holds it.  Structural tokens
               (`layout`, `hero`, `frame`, `meter`, `base`, `sel`, `tempo`...)
               are READ BY RENDERERS in the reference app -- mutate one and the
               render changes, which is the property that keeps a token from
               being dead metadata.  `prototypes/verify_language.py` asserts it.
    FAMILY     the board layout family: columns | sections | split.
    DOC        each language's doctrine, taken from its Kit class docstring, so
               the prose here cannot drift from the class it describes.
    ORDER      the ten in the order the app's `t` key cycles them.
    RETIRED    two languages the operator removed from the reference app.  They
               remain legitimate choices -- see LANGUAGES.md -- but no kit here
               renders them, and pretending otherwise is what this entry exists
               to prevent.

USING IT

    from languages import LANGUAGES, DOC, FAMILY, ORDER
    tok = LANGUAGES["solari"]        # every token, including the structural ones
    print(DOC["solari"])             # why it commits to what it commits to

Reference frames for all ten live in `assets/languages/` -- board and component
sheet each, one sweep, one fixture, one viewport.  A page that puts the frames,
the tokens and the doctrine side by side is generated by
`prototypes/build_languages_html.py`.

Generated {when} from {n} kits in `taskboard/language.py`.
"""
from __future__ import annotations

'''


def fmt(v) -> str:
    return repr(v)


def build(root: Path, when: str) -> str:
    langs = TH.ORDER
    out = [HEADER.format(root=root, when=when, n=len(langs))]

    out.append("LANGUAGES: dict[str, dict] = {\n")
    for n in langs:
        t = {k: v for k, v in TH.THEMES[n].items()
             if isinstance(v, (str, int, float, bool))}
        label = t.get("label", n.title())
        note = t.get("note", "")
        out.append(f"    # {label} -- {note}\n" if note else f"    # {label}\n")
        out.append(f"    {n!r}: dict(\n")
        # structural first, then palette, then the rest -- reading order
        struct = ["layout", "hero", "frame", "meter", "base", "numbered",
                  "sel", "tempo", "easing"]
        pal = ["ground", "ink", "mut", "dim", "accent", "warn", "alert",
               "panel", "focus", "screen", "alu"]
        seen = set()
        for group in (struct, pal):
            line = "        "
            for k in group:
                if k in t:
                    seen.add(k)
                    piece = f"{k}={fmt(t[k])}, "
                    if len(line) + len(piece) > 78:
                        out.append(line.rstrip() + "\n")
                        line = "        "
                    line += piece
            if line.strip():
                out.append(line.rstrip() + "\n")
        rest = [k for k in sorted(t) if k not in seen]
        line = "        "
        for k in rest:
            piece = f"{k}={fmt(t[k])}, "
            if len(line) + len(piece) > 78:
                out.append(line.rstrip() + "\n")
                line = "        "
            line += piece
        if line.strip():
            out.append(line.rstrip() + "\n")
        out.append("    ),\n")
    out.append("}\n\n")

    out.append("# board layout family, from Kit.board_layout()\n")
    out.append("FAMILY: dict[str, str] = {\n")
    for n in langs:
        out.append(f"    {n!r}: {LG.kit(n).board_layout()!r},\n")
    out.append("}\n\n")

    out.append("# The doctrine, straight off each Kit class -- edit it THERE.\n")
    out.append("DOC: dict[str, str] = {\n")
    for n in langs:
        doc = inspect.getdoc(type(LG.kit(n))) or ""
        out.append(f"    {n!r}: '''{doc}''',\n")
    out.append("}\n\n")

    out.append(f"ORDER: list[str] = {langs!r}\n\n")

    out.append("# Retired from the reference app -- still valid to CHOOSE.\n")
    out.append("RETIRED: dict[str, tuple[str, str]] = {\n")
    for k, (commits, why) in RETIRED.items():
        out.append(f"    {k!r}: (\n        {commits!r},\n        {why!r}),\n")
    out.append("}\n")
    return "".join(out)


GALLERY = ROOT / "prototypes" / "gallery"

#: the geometry `capture_languages.py --surface` reserves for the region, and
#: therefore the geometry every `surface_*.txt` in `GALLERY` was rendered at.
#: Repeated rather than imported for the reason `_probe()` gives below: that
#: module pulls in a Textual app and numpy, to write a markdown table.
SHEET_W, SHEET_H = 116, 26
#: ...AND THE LABEL IT PASSES, which stopped being ignorable on 2026-09-04.
#: `_surface_tint` now READS the label (LIMITS L-31): blueprint's sheet letters
#: it onto a third dimension span, and the span is paid for out of the reserved
#: rectangle, so the glass moves down a row and loses one. Asking a posture for
#: its box WITHOUT the label therefore printed `0, 1 116x24` beside a frame
#: rendered at `0, 2 116x23` -- the table describing a render that is not the
#: one it names, which is precisely what `surfaces_index()`'s own comment
#: promises it does not do. Caught in the STAGED export, before shipping --
#: by a person reading the table, not by any check (F-12). `check_box_
#: matches_shipped()` below is that check.
SHEET_LABEL = "mbb rho final"

SURFACES_HEADER = """# The surface axis, as the reference implementation renders it

**Generated.**  `prototypes/export_to_skill.py` in the taskboard repo writes this file from the
capture sweep (`python prototypes\\capture_languages.py --surface`).  Do not edit by hand.

**One image, every language.**  The frames below are the SAME picture --
`tui-demos/lab/mbb_rho_final.npy`, a 20x60 topology-optimisation density field rendered through
R1's PAPER/INK colormap at scale 6 (360x120 px) -- put through every kit's `raster_region()`.
"The same image in {n} languages" is only an honest comparison when it really is one image, which
is the argument the board sweep makes one level up.

**The `.txt` is the GLYPH side and it works on any terminal.**  Where `textual_image` reports a
raster transport, the same posture is applied to the pixels and rendered through it; the `raster`
column says what those pixels are, and `refused` is a COMMITMENT rather than a gap -- ledger
audits a figure instead of showing it, solari cannot flip an image.

**Two surfaces, one token -- and since 2026-09-04 the frame is a third thing you can ask for.**
`raster_region()` returns `rows` (the fused glyph rendering: frame AND image, which is what the
`.txt` files below are), `pixels` (the glass alone), and now also **`chrome`** and
**`image_box`**.  They exist because the first two are not enough for a consumer that draws TRUE
PIXELS: corgi's `[1] DISPLAY` box and blueprint's dimension spans live in `rows` and are absent
from `pixels`, so a Sixel field rendered from `pixels` came out bare, with none of the language
around it.  `image_box` is `(col, row, w, h)` -- where inside the rectangle the glass goes -- and
`chrome` is `rows` with exactly those cells replaced by a transparent sentinel (`RASTER_HOLE`,
U+E000), meaning "do not paint: the raster belongs here".  So a compositor draws `chrome`,
reserves `image_box`, and puts the image widget in the hole, and gets the posture whole.

`chrome` is DERIVED from `rows` and never the reverse, which is why adding it moved no frame in
this directory.  For the refusing postures `image_box` is `None` and `chrome` IS `rows`: there is
no glass, so there is no hole to cut -- and `None` rather than an empty rectangle, because a
language that refuses has nowhere to put an image, which is not the same as having a place of no
size.  The `image box` column below is the rectangle at the frames' own {w}x{h} geometry.

| language | posture | frame | ink | raster | image box |
|---|---|---|---|---|---|
"""


#: the sweep's own image SIZE (`capture_languages.py`'s `test_image()`: a
#: 20x60 field at `MBB_SCALE=6`).  Repeated for the same reason `SHEET_LABEL`
#: is: a flat probe of THIS size reproduces the dimension captions the
#: shipped frames actually show -- blueprint's `360px` span, ledger's
#: `width`/`height` exhibit rows -- because those read `img.size`, never a
#: pixel value, and reproducing them is what lets `check_box_matches_shipped`
#: compare against the shipped `.txt` without numpy or the other repo's
#: `.npy`. Content stays flat: nothing this file compares reads a pixel.
IMG_W, IMG_H = 360, 120


def _probe():
    """A flat `IMG_W`x`IMG_H` image -- enough to ask a posture what it does
    (posture, image box, and every caption that reads `img.size`) without
    the real sweep image. The sweep's real image lives in
    `capture_languages.py`, which this file deliberately does not import --
    importing it would pull in a Textual app and numpy to write a markdown
    table."""
    from PIL import Image
    return Image.new("RGB", (IMG_W, IMG_H), (128, 128, 128))


class SurfaceIndexMismatch(RuntimeError):
    """SURFACES.md's `image box` column would print a rectangle that
    disagrees with the frame it names -- F-12."""


def _plain(rows: list[str]) -> list[str]:
    return [Text.from_markup(r).plain for r in rows]


def _derive_glass_box(shipped: list[str], chrome: list[str]
                       ) -> tuple[int, int, int, int] | None:
    """Where `shipped` (the artefact in `prototypes/gallery/`) and `chrome`
    (this kit's own hole, at the same geometry) DISAGREE -- glass, located by
    comparing two texts, never by reading `image_box` back to itself, which
    would let a bug in `image_box` mark its own homework.

    `None` if the two texts agree everywhere (the `refuse` postures, whose
    `chrome` IS `rows`, so there is nothing to disagree about). Raises if the
    disagreeing cells are not a solid rectangle -- a check that only ever
    diffs two numbers already assumes they describe a rectangle, and a hole
    that leaked into a caption row would be exactly that assumption unpaid
    for."""
    cells = {(i, j) for i, (s, c) in enumerate(zip(shipped, chrome))
             for j, (sc, cc) in enumerate(zip(s, c)) if sc != cc}
    if not cells:
        return None
    ys, xs = [i for i, _ in cells], [j for _, j in cells]
    y, x = min(ys), min(xs)
    bh, bw = max(ys) - y + 1, max(xs) - x + 1
    expected = {(i, j) for i in range(y, y + bh) for j in range(x, x + bw)}
    if cells != expected:
        raise SurfaceIndexMismatch(
            f"the glass cells the shipped frame and chrome disagree on are "
            f"not a rectangle: {sorted(cells)}")
    return (x, y, bw, bh)


def check_box_matches_shipped(n: str, gallery: Path = GALLERY):
    """F-12. Verify that the box `surfaces_index()` is about to print for
    `surface_<n>.txt` is the box that shipped frame actually shows, before
    the table repeats a claim nothing checked.

    Re-derives the sheet's head offset from the frame the same way
    `tests/test_surface.py::test_chrome_preserves_the_frame_the_shipped_capture_shows`
    does (`head = kit.sect(...)`): the note text passed to `sect()` does not
    change `head`'s LENGTH for any of the eleven kits -- only `title` (always
    "SURFACE" here) and the fixed `SHEET_W`/`SHEET_H` do -- so a placeholder
    note re-derives the same offset the real capture used, without needing
    the sweep's own image. Then it finds the rectangle where that shipped
    frame and this kit's own `chrome` disagree (`_derive_glass_box`) and
    compares it to `image_box` itself -- the original defect: a call to
    `raster_region()` made WITHOUT `label=` gave blueprint a DIFFERENT
    geometry (one row shorter caption, glass one row lower) than the label'd
    call that produced the shipped `surface_blueprint.txt`, so the printed
    `0, 1 116x24` sat beside a frame captured at `0, 2 116x23` and nothing
    noticed. `refuse` postures (ledger, solari) show no disagreeing cells;
    their `image_box` must be `None` too, checked the same way.

    Raises `SurfaceIndexMismatch` -- an ERROR, not a warning -- naming both
    rectangles, rather than let the table ship a description of a frame it
    does not name. Returns the `raster_region()` result once it agrees, so
    `surfaces_index()` need not render the sheet a second time."""
    kit = LG.kit(n)
    f = gallery / f"surface_{n}.txt"
    grid = f.read_text(encoding="utf-8").splitlines()
    head = kit.sect("SURFACE", "probe", SHEET_W, SHEET_H)
    shipped = [grid[len(head) + i][1:1 + SHEET_W] for i in range(SHEET_H)]
    res = kit.raster_region(_probe(), SHEET_W, SHEET_H, label=SHEET_LABEL)
    derived = _derive_glass_box(shipped, _plain(res.chrome))
    if derived != res.image_box:
        raise SurfaceIndexMismatch(
            f"{n}: SURFACES.md would print image_box={res.image_box!r} for "
            f"{f.name}, but the shipped frame's glass is at {derived!r} -- "
            f"the table would describe a frame it does not name. Re-run "
            f"`capture_languages.py --surface` and re-export.")
    return res


def surfaces_index() -> str | None:
    """The generated index of the surface sweep, or None if it has not run.

    A SEPARATE FILE rather than an edit to `INDEX.md`, for the reason this
    exporter already refuses to touch `LANGUAGES.md`: that file is prose that
    argues.  A generator that rewrote it would flatten the part that teaches,
    and one that appended to it would fight the author."""
    rows = []
    for n in TH.ORDER:
        f = GALLERY / f"surface_{n}.txt"
        if not f.exists():
            return None
        grid = f.read_text(encoding="utf-8").splitlines()
        total = sum(len(r) for r in grid) or 1
        ink = sum(1 for r in grid for c in r if c != " ") / total * 100
        # AT THE FRAMES' OWN GEOMETRY, not the probe's.  A posture's image box
        # depends on the RESERVED SIZE and on the kit, never on the image's
        # content -- so a 2x2 probe measured at 116x26 gives exactly the
        # rectangle the `.txt` beside it was rendered with, and quoting the
        # probe's own 10x4 box would print a number that describes nothing a
        # reader can see. F-12: `check_box_matches_shipped` VERIFIES that
        # rectangle against the shipped frame before it is trusted to print
        # anything -- an ERROR, not a warning, aborts the export on drift.
        res = check_box_matches_shipped(n)
        box = ("**none**" if res.image_box is None
               else "`{}, {} {}x{}`".format(*res.image_box))
        rows.append(
            f"| **{TH.THEMES[n].get('label', n)}** | `{res.posture}` | "
            f"`surface_{n}.txt` | {ink:.1f} % | "
            f"{'**refused**' if res.pixels is None else 'sixel / TGP'} | "
            f"{box} |")
    # the count is interpolated, not typed: a header that says "ten" over
    # eleven rows is the drift this whole file exists to stop
    return (SURFACES_HEADER.format(n=len(TH.ORDER), w=SHEET_W, h=SHEET_H)
            + "\n".join(rows) + "\n")


def copy_captures(skill: Path) -> tuple[int, int]:
    """Carry the capture sweep's frames into the skill.

    THIS DID NOT EXIST, AND THE ASSETS DRIFTED BECAUSE OF IT.  The exporter
    wrote `languages.py` and nothing else, so the twenty `.txt`/`.svg` frames
    under `assets/languages/` were copied by hand once and then silently fell
    behind: `prototypes/out/_fixture_late.json` was edited after the sweep that
    produced them, and every board frame in the skill now differs from a fresh
    sweep of unmodified code.  A projection that projects half the asset is how
    the other half rots -- which is the exact failure this file's own header
    says it exists to prevent."""
    dst = skill / "assets" / "languages"
    dst.mkdir(parents=True, exist_ok=True)
    written = unchanged = 0
    for src in sorted(GALLERY.glob("*.*")):
        if src.suffix not in (".txt", ".svg"):
            continue
        target = dst / src.name
        data = src.read_bytes()
        if target.exists() and target.read_bytes() == data:
            unchanged += 1
            continue
        target.write_bytes(data)
        written += 1
    return written, unchanged


def main() -> int:
    skill = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SKILL
    dst = skill / "assets" / "languages.py"
    if not dst.parent.exists():
        print(f"NO SUCH SKILL ASSETS DIR: {dst.parent}", file=sys.stderr)
        return 2
    # the date is passed in rather than read from the clock so a rebuild that
    # changes nothing produces no diff
    when = "2026-08-02"
    src = build(ROOT, when)
    dst.write_text(src, encoding="utf-8")
    print(f"  wrote {dst} ({len(src) / 1024:.0f} KB, {len(TH.ORDER)} languages)")

    # prove the generated file actually imports and holds what it claims
    ns: dict = {}
    exec(compile(src, str(dst), "exec"), ns)
    assert ns["ORDER"] == TH.ORDER, "ORDER drifted"
    assert set(ns["LANGUAGES"]) == set(TH.ORDER), "LANGUAGES drifted"
    for n in TH.ORDER:
        got = ns["LANGUAGES"][n]
        want = {k: v for k, v in TH.THEMES[n].items()
                if isinstance(v, (str, int, float, bool))}
        assert got == want, f"{n}: tokens differ"
        assert ns["DOC"][n] == (inspect.getdoc(type(LG.kit(n))) or ""), f"{n}: doc"
        assert ns["FAMILY"][n] == LG.kit(n).board_layout(), f"{n}: family"
    print(f"  verified: {len(TH.ORDER)} languages, every token, doc and family "
          f"round-trips")

    # THE FRAMES, which used to be copied by hand and therefore rotted
    written, unchanged = copy_captures(skill)
    print(f"  captures: {written} written, {unchanged} already identical "
          f"-> {skill / 'assets' / 'languages'}")

    idx = surfaces_index()
    if idx is None:
        print("  SURFACES.md NOT written: run "
              "`capture_languages.py --surface` first", file=sys.stderr)
    else:
        (skill / "assets" / "languages" / "SURFACES.md").write_text(
            idx, encoding="utf-8")
        print(f"  wrote SURFACES.md ({len(TH.ORDER)} postures)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
