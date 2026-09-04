# Increment 3 — one image through every kit, and the raster path measured for real

Batch `2026-09-03-fastflow-06` ("surface") · phase B · one agent, sequential.
Scope from spec §7: *the `--surface` sweep, AC-5 captures, export, INDEX.md,
AC-6 byte-identity.*

## 1. What changed

**`capture_languages.py --surface`** renders **one fixed image** —
`tui-demos/lab/mbb_rho_final.npy`, the 20×60 MBB density field through R1's own
PAPER/INK colormap at scale 6 (360×120 px, NEAREST) — through every kit's
`raster_region()` at the board's own 118×34 viewport, writing
`surface_<lang>.txt` and `.svg`. The `.npy` load lives in `prototypes/` because
numpy is not a declared dependency of the package.

The sheet it photographs is the language's own `sect()` header plus the
reserved rectangle, and **deliberately not a board screen**: spec §5 says no
existing screen renders a region in this batch, so wiring one in to take a
picture of it would be the batch shipping what it declared out of scope. The
header is what makes the frames differ *outside* the image rectangle, which is
AC-4's boundary. The sweep keeps the board sweep's own law — no two frames
identical — and fails loud rather than leaving it to the eye.

**`capture_surface_raster.py`** is the AC-5 probe: one language, both surfaces
side by side in a real Windows Terminal, glyph pane left and `textual_image`
pane right, from the *same* `RenderResult`. Per LIMITS L-19 the window **closes
itself** — WT is one process for all windows, and no terminal process is killed
anywhere in this harness. The capture script (`.fast-dev-flow/captures/
shoot.ps1`) puts the command in a `.cmd` file because `wt.exe` splits its
arguments on `;` into tabs, launches from PowerShell because Git Bash rewrites
paths for Windows exes, takes the newest `WindowsTerminal` rect, and crops
10 px sides / 16 px bottom.

**`export_to_skill.py` now carries the frames**, which it never did. It wrote
`languages.py` and nothing else, so the twenty `.txt`/`.svg` under the skill's
`assets/languages/` were copied by hand once and then rotted (F-2). It also
writes a generated `SURFACES.md` index — a *separate* file rather than an edit
to `INDEX.md`, for the same reason the exporter already refuses to touch
`LANGUAGES.md`: that file is prose that argues, and a generator would flatten
the part that teaches.

**The export was run into a staging directory, not into the skill.** See §5 —
one operator decision is outstanding.

## 2. Files modified

| file | source? | what |
| --- | --- | --- |
| `prototypes/capture_languages.py` | source | `--surface` entry point, `test_image()`, `surface_sheet()`, `sweep_surfaces()`, `surface_main()` |
| `prototypes/capture_surface_raster.py` | **new source** | the AC-5 two-pane probe, self-closing |
| `prototypes/export_to_skill.py` | source | `copy_captures()`, `surfaces_index()`, wired into `main()` |
| `.fast-dev-flow/captures/shoot.ps1` | harness | the L-19 capture procedure |

**3 of 4 source files used.** No new dependency (numpy is dev-side only).

## 3. How to test

    cd C:\Users\jjgh8\Github\taskboard\.claude\worktrees\kanban-variants
    python -m pytest -q
    $env:PYTHONIOENCODING = "utf-8"
    python prototypes\capture_languages.py            # boards, AC-6
    python prototypes\capture_languages.py --surface  # AC-4
    python prototypes\export_to_skill.py <STAGING_DIR>
    .\.fast-dev-flow\captures\shoot.ps1 -Lang corgi -Seconds 12 -OutDir .\.fast-dev-flow\captures

## 4. Test results

    231 passed, 4 warnings in 29.62s

**AC-4 — the same image through all eleven.** The sweep produced 11 `.txt` and
11 `.svg`, and its own no-duplicates law passed:

    naught      lattice   118x34  82.3% ink   raster (360, 120)
    corgi       display   118x34  78.6% ink   raster (360, 120)
    instrument  lattice   118x34  79.2% ink   raster (360, 120)
    swiss       figure    118x34  74.1% ink   raster (360, 120)
    industrial  display   118x34  78.6% ink   raster (360, 120)
    nord        untinted  118x34  75.8% ink   raster (360, 120)
    darkside    depth     118x34  68.7% ink   raster (360, 120)
    prism       depth     118x34  68.7% ink   raster (360, 120)
    ledger      refuse    118x34  10.5% ink   raster refused
    solari      refuse    118x34   3.5% ink   raster refused
    blueprint   tint      118x34  75.7% ink   raster (360, 120)

**Pairwise diff, with the image masked** (every half-block, naught dot and
braille cell replaced, leaving chrome and text — LANGUAGES.md's "mask the hero,
diff the rest"):

| | pairs | identical |
| --- | --- | --- |
| raw frames | 55 | **none** |
| image masked out | 55 | **none** |

Chrome cells surviving the mask, per language: corgi 419 · industrial 317 ·
swiss 262 · ledger 261 · blueprint 251 · solari 139 · nord 25 · darkside 22 ·
prism 22 · naught 17 · instrument 17.

**AC-6 — nothing else moved.** 22 / 22 board and gallery captures byte-identical
against a control sweep with every `surface` token popped before any kit is
built. The sweep's own cross-process reproducibility check passed on the same
run.

**AC-5 — true raster, captured.**

| capture | verdict |
| --- | --- |
| `.fast-dev-flow/captures/surface_raster_corgi.png` | `transport=sixel`, `raster=yes`; both panes render, side by side, in their reserved rectangles |
| `.fast-dev-flow/captures/surface_raster_blueprint.png` | same; the cyanotype is on the pixels, and the dimension spans are on the cells |
| `.fast-dev-flow/captures/surface_raster_ledger.png` | the refusal reaches the raster path: no image anywhere, the ruled exhibit stands, `shown···no` |

## 5. Findings

**P-4 is TRUE, and it was a hypothesis.** `textual_image` **does** place a Sixel
region correctly inside a Textual layout under WT/ConPTY. The corgi capture
shows the raster pane beside the glyph pane, both in their reserved rectangles,
with no stacking and no offset. LIMITS L-16 (cursor desync after an inline
image) is a limit on **raw writers**; `textual_image` compensates, and this is
the measurement that says so.

**AC-3 is visually confirmed, not merely asserted.** In the corgi capture the
raster pane is green — corgi's screen ramp applied to the *pixels*, not the
source's PAPER/INK grey. In blueprint it is cyanotype blue. The posture reaches
both surfaces.

**F-4 · NEW · A posture's CHROME does not reach the raster path.** Visible only
in the captures. On the glyph side corgi draws its `[1] DISPLAY` box *around*
the image; on the raster side the pane is bare, and blueprint's dimension spans
are likewise absent. This is a real gap in `RenderResult`, not a rendering bug:
`rows` is the complete glyph rendering (chrome **and** image, fused), and
`pixels` is the glass alone, so a consumer that wants raster **plus** the
language's frame has nothing to draw the frame from. The shape of the fix is a
chrome-only row set plus the interior rectangle's geometry, so a caller can
reserve, draw the frame, and place the widget in the hole. **Not done here** —
it is an API addition beyond "the primitive and its sweep", and emersio-lab is
the first consumer that will need it. Reported rather than widened.

**No posture proved unimplementable as written.** Nothing was substituted;
Phosphor and BBS raise `NotImplementedError` naming themselves. Two narrowings
are recorded in inc 2 (`depth`'s ambient motion is unbuilt; ledger's exhibit
fills a region narrower than ~34 cells).

**F-1 (carried, still open).** `capture_languages.py` is intermittently
non-deterministic in `board_solari.txt` (the `DAYS OVERDUE` row, which the
file's own header claims `TEXTUAL_ANIMATIONS=none` cured — it has not) and in
`gallery_blueprint.txt` (a switch caught at `▅▅` vs `▁▁`). Both observed on
token-popped control sweeps, so neither is caused by this batch. It makes the
sweep exit red about one run in three.

**Probe limitation, stated:** `capture_surface_raster.py`'s own header text
uses Textual's default foreground, which is nearly invisible on a light ground
(see the ledger capture). It affects the probe's chrome only, not any kit.

## 6. Pending — ONE OPERATOR DECISION BLOCKS THE EXPORT

The exporter was run into `%TEMP%\skillstage`, **not** into
`~/.claude/skills/tui-design/`. Running it for real would make three changes,
and only one of them is this batch's:

1. **What the batch asked for** — adds `SURFACES.md` and 22 `surface_*` frames;
   adds a `surface=` token to all eleven entries in `languages.py`.
2. **A pre-existing correction (F-2)** — rewrites all 20 `board_*` frames,
   which differ from the shipped ones because `_fixture_late.json` was edited
   on 2026-08-03 at 10:38, after the 08:47 sweep that produced them. The
   shipped frames are stale; the exporter would make them true.
3. **Out of this batch's scope (F-3)** — adds **prism**: `ORDER` goes from ten
   to eleven and four `*_prism` frames appear. `INDEX.md`'s hand-written prose
   says "The ten languages" and would then be wrong.

**Decision needed:** run the exporter as-is (accepting 2 and 3, and INDEX.md's
prose needing a hand edit), or pin the export to the ten. I did not choose.

Also open: F-4 (chrome on the raster path) for the emersio-lab batch; F-1 (the
capture harness's flakiness) as its own fix.

## 7. Suggested next task

Settle the prism question, then run `export_to_skill.py` at the real skill and
update `INDEX.md`'s prose by hand to match. After that, F-1 — the sweep's
`settle()` needs the harness's condition A, or the batch's own captures stay a
coin flip.
