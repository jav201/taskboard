# The surface axis, as the reference implementation renders it

**Generated.**  `prototypes/export_to_skill.py` in the taskboard repo writes this file from the
capture sweep (`python prototypes\capture_languages.py --surface`).  Do not edit by hand.

**One image, every language.**  The frames below are the SAME picture --
`tui-demos/lab/mbb_rho_final.npy`, a 20x60 topology-optimisation density field rendered through
R1's PAPER/INK colormap at scale 6 (360x120 px) -- put through every kit's `raster_region()`.
"The same image in 11 languages" is only an honest comparison when it really is one image, which
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
size.  The `image box` column below is the rectangle at the frames' own 116x26 geometry.

| language | posture | frame | ink | raster | image box |
|---|---|---|---|---|---|
| **Naught** | `lattice` | `surface_naught.txt` | 82.3 % | sixel / TGP | `0, 0 116x26` |
| **Corgi Engineering** | `display` | `surface_corgi.txt` | 78.6 % | sixel / TGP | `1, 1 114x24` |
| **Instrument** | `lattice` | `surface_instrument.txt` | 79.2 % | sixel / TGP | `0, 0 116x26` |
| **Swiss** | `figure` | `surface_swiss.txt` | 74.1 % | sixel / TGP | `0, 0 113x24` |
| **Industrial** | `display` | `surface_industrial.txt` | 78.6 % | sixel / TGP | `1, 1 114x24` |
| **Nord (base16)** | `untinted` | `surface_nord.txt` | 75.8 % | sixel / TGP | `0, 0 116x26` |
| **Darkside** | `depth` | `surface_darkside.txt` | 68.7 % | sixel / TGP | `1, 1 114x24` |
| **Prism** | `depth` | `surface_prism.txt` | 68.7 % | sixel / TGP | `1, 1 114x24` |
| **Ledger** | `refuse` | `surface_ledger.txt` | 10.5 % | **refused** | **none** |
| **Solari** | `refuse` | `surface_solari.txt` | 3.5 % | **refused** | **none** |
| **Blueprint** | `tint` | `surface_blueprint.txt` | 75.6 % | sixel / TGP | `0, 2 116x23` |
