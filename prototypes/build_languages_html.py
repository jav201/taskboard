"""build_languages_html.py -- one self-contained HTML page for consulting the
ten TUI design languages, built from the running app.

    python prototypes/build_languages_html.py [DEST.html]

WHAT IT IS.  A reference page (genre A under the html-visualizer skill) that
puts, for every language: its doctrine, its structural tokens, its palette, its
BOARD and its COMPONENT SHEET -- side by side, at one size, off one fixture.

NOTHING ON THIS PAGE IS TYPED TWICE.  Three sources, all read at build time:

  * doctrine   -- `inspect.getdoc()` on each Kit subclass in
                  `taskboard/language.py`.  The prose in this page IS the
                  docstring in the code, so the two cannot drift.  A language
                  whose docstring changes changes here on the next build.
  * tokens     -- `taskboard/themes.py` THEMES dict, structural and palette
                  alike, read key by key rather than transcribed.
  * pictures   -- `prototypes/gallery/*.svg`, and every dimension and ink
                  figure is MEASURED from the matching `.txt` with the same
                  formula the skill's gallery uses (non-space cells / total).

That is the whole design of this file: the one thing a documentation page
reliably gets wrong is being a copy, so it is built as a projection instead.

RUN `capture_languages.py` FIRST.  This script renders what is in
`prototypes/gallery/`; it does not drive the app.  If a capture is missing the
build fails loudly rather than emitting a page with a hole in it.
"""
from __future__ import annotations

import html
import inspect
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import taskboard.language as LG                                   # noqa: E402
import taskboard.themes as TH                                     # noqa: E402

GALLERY = ROOT / "prototypes" / "gallery"
DEFAULT_DEST = Path(r"G:\My Drive\Courses\tui-lenguajes-de-diseno.html")

E = html.escape

# Structural tokens, in the order they are worth reading: what the board IS,
# then what draws the hero, the divider, the quantity, then pace.
STRUCT = [
    # NOT "board layout".  `board_layout()` returns the FAMILY (columns /
    # sections / split) and is shown as the section badge; the `layout` token
    # is the language's own composition mode (lattice, strip, trace,
    # editorial, panel...).  Rendering both under one name put "COLUMNS LAYOUT"
    # next to "BOARD LAYOUT: lattice" on the same screen, which reads as a
    # contradiction rather than as two levels.
    ("layout", "composition", "the language's own composition mode"),
    ("hero", "hero", "what draws the one number that dominates"),
    ("frame", "structure device", "what separates one region from another"),
    ("meter", "quantity", "how an amount is said"),
    ("base", "pixel base", "the shape of the smallest mark"),
    ("numbered", "numbered", "are parameters addressed by number"),
    ("sel", "focus", "how the focused thing is marked"),
    ("tempo", "tempo", "motion pace, in seconds"),
]

PALETTE = [("ground", "ground"), ("ink", "ink"), ("mut", "muted"),
           ("dim", "dim"), ("accent", "accent"), ("warn", "warn"),
           ("alert", "alert"), ("panel", "panel"), ("focus", "focus"),
           ("screen", "screen"), ("alu", "aluminium"), ("label", "label"),
           ("note", "note")]

# The one thing the code cannot tell you: why the set is these ten.  Two
# languages were removed by the operator, and a page that silently listed eight
# where the skill's own catalogue lists ten would be hiding a decision.
RETIRED = {
    "phosphor": "one hue at many lightnesses (amber/green CRT)",
    "bbs": "full 16 colours, solid ink, double-line boxes (ANSI/BBS art)",
}


def doc_to_html(doc: str) -> str:
    """Render a Kit docstring.  It is written as prose with `*` bullets and
    `**bold**`/`` `code` `` inline, so that shape is honoured rather than
    flattened into a <pre>."""
    doc = E(doc)
    doc = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", doc, flags=re.S)
    doc = re.sub(r"`([^`]+)`", r"<code>\1</code>", doc)
    out, para, bullets = [], [], []

    def flush_para():
        if para:
            out.append("<p>" + " ".join(para) + "</p>")
            para.clear()

    def flush_bullets():
        if bullets:
            out.append("<ul>" + "".join(f"<li>{b}</li>" for b in bullets)
                       + "</ul>")
            bullets.clear()

    for raw in doc.split("\n"):
        line = raw.strip()
        if not line:
            flush_para(); flush_bullets()
        elif line.startswith("* "):
            flush_para()
            bullets.append(line[2:])
        elif bullets:
            bullets[-1] += " " + line
        else:
            para.append(line)
    flush_para(); flush_bullets()
    return "".join(out)


def measure(name: str) -> tuple[int, int, float]:
    p = GALLERY / f"{name}.txt"
    if not p.exists():
        raise SystemExit(f"MISSING CAPTURE: {p}\nRun capture_languages.py first.")
    rows = p.read_text(encoding="utf-8").rstrip("\n").split("\n")
    total = sum(len(r) for r in rows)
    ink = sum(1 for r in rows for c in r if c not in " \u00a0")
    return max(len(r) for r in rows), len(rows), ink / total * 100


def svg(name: str) -> str:
    p = GALLERY / f"{name}.svg"
    if not p.exists():
        raise SystemExit(f"MISSING PICTURE: {p}\nRun capture_languages.py first.")
    s = p.read_text(encoding="utf-8")
    return s.replace("<svg ", '<svg class="frame" ', 1)


def swatch_row(t: dict) -> str:
    out = []
    for k, label in PALETTE:
        v = t.get(k)
        if not isinstance(v, str) or not v.startswith("#"):
            continue
        out.append(f'<div class="sw"><span class="chip" style="background:{v}">'
                   f'</span><span class="swk">{label}</span><code>{v}</code></div>')
    return f'<div class="swatches">{"".join(out)}</div>'


def build() -> str:
    langs = TH.ORDER
    kits = {n: LG.kit(n) for n in langs}
    themes = {n: TH.THEMES[n] for n in langs}
    docs = {n: (inspect.getdoc(type(kits[n])) or "") for n in langs}
    m_board = {n: measure(f"board_{n}") for n in langs}
    m_gal = {n: measure(f"gallery_{n}") for n in langs}
    layouts = {n: kits[n].board_layout() for n in langs}

    P: list[str] = []
    a = P.append

    a("""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Ten TUI design languages \u2014 taskboard</title>
<style>
:root{
  --bg:#0f1115;--panel:#151922;--panel2:#1b2029;--line:#242b36;
  --fg:#dfe4ec;--mut:#93a0b4;--dim:#5d6b80;--accent:#4bb3d4;--warn:#d8a23a;
  --ok:#6cc08b;--bad:#d4756b;
  --mono:ui-monospace,SFMono-Regular,'DejaVu Sans Mono','Cascadia Mono',Menlo,Consolas,monospace;
  --sans:system-ui,-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.62 var(--sans);
  -webkit-font-smoothing:antialiased}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}
code{font-family:var(--mono);font-size:.88em;background:#0b0d12;
  border:1px solid var(--line);border-radius:3px;padding:.05em .32em}
b{color:#fff;font-weight:600}
nav{position:sticky;top:0;z-index:40;background:rgba(15,17,21,.94);
  backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.navin{max-width:1240px;margin:0 auto;padding:.55rem 1.1rem;display:flex;
  gap:.4rem;flex-wrap:wrap;align-items:center}
.navin .brand{font-weight:700;margin-right:.5rem;font-size:.88rem}
.navin a{font-size:.78rem;color:var(--mut);border:1px solid transparent;
  border-radius:99px;padding:.13rem .55rem;white-space:nowrap}
.navin a:hover{color:var(--fg);border-color:var(--line);background:var(--panel);
  text-decoration:none}
main{max-width:1240px;margin:0 auto;padding:2rem 1.1rem 6rem}
.hero h1{font-size:2.05rem;line-height:1.15;margin:.2rem 0 .55rem;
  letter-spacing:-.015em}
.hero .sub{color:var(--mut);font-size:1.02rem;max-width:76ch}
.kpis{display:flex;gap:.6rem;flex-wrap:wrap;margin:1.4rem 0 0}
.kpi{background:var(--panel);border:1px solid var(--line);border-radius:8px;
  padding:.55rem .85rem;min-width:100px}
.kpi b{display:block;font-size:1.4rem;line-height:1.1;font-family:var(--mono)}
.kpi span{font-size:.68rem;color:var(--mut);text-transform:uppercase;
  letter-spacing:.07em}
h2{font-size:1.55rem;margin:0;letter-spacing:-.01em}
h3{font-size:1rem;margin:1.8rem 0 .5rem;color:var(--mut);
  text-transform:uppercase;letter-spacing:.08em;font-size:.72rem}
section.lang{margin:4rem 0 0;scroll-margin-top:58px}
.lhead{display:flex;align-items:baseline;gap:.7rem;flex-wrap:wrap;
  border-bottom:1px solid var(--line);padding-bottom:.6rem}
.num{font-family:var(--mono);color:var(--dim);font-size:1.1rem}
.badge{font-size:.65rem;text-transform:uppercase;letter-spacing:.08em;
  padding:.16rem .5rem;border-radius:99px;border:1px solid var(--line);
  color:var(--mut);background:var(--panel2);white-space:nowrap}
.note{color:var(--dim);font-size:.88rem;font-style:italic;margin:.55rem 0 0}
.doc{margin:1.1rem 0 0;max-width:84ch}
.doc p{margin:.55rem 0;color:var(--mut)}
.doc ul{margin:.6rem 0;padding:0 0 0 1.1rem}
.doc li{margin:.42rem 0;color:var(--mut)}
.doc b{color:var(--fg)}
.axrow{display:flex;gap:.4rem;flex-wrap:wrap;margin:.9rem 0 0}
.ax{font-size:.74rem;background:var(--panel2);border:1px solid var(--line);
  border-radius:5px;padding:.22rem .5rem}
.ax i{color:var(--dim);font-style:normal;text-transform:uppercase;
  font-size:.62rem;letter-spacing:.08em;margin-right:.35rem}
.swatches{display:flex;gap:.32rem;flex-wrap:wrap;margin:.7rem 0 0}
.sw{display:flex;align-items:center;gap:.3rem;background:var(--panel);
  border:1px solid var(--line);border-radius:5px;padding:.2rem .45rem;
  font-size:.71rem}
.chip{width:13px;height:13px;border-radius:3px;
  border:1px solid rgba(255,255,255,.16);display:inline-block}
.swk{color:var(--mut)}
.sw code{background:none;border:none;padding:0;color:var(--dim);font-size:.69rem}
/* CONTENT-VISIBILITY IS LOAD-BEARING HERE, NOT A MICRO-OPTIMISATION.  Twenty
   frames hold ~2900 <text> elements and every glyph carries its own `x`, which
   is what stops the cell grid drifting under a fallback font.  Laying all of
   that out at once froze the renderer for 30 s whenever the whole page was
   forced through layout -- jumping straight to an #anchor does exactly that.
   `content-visibility:auto` lets the browser skip layout and paint for figures
   outside the viewport; `contain-intrinsic-size` gives it a placeholder height
   so the scrollbar and anchor offsets stay honest instead of jumping. */
figure{margin:1.5rem 0 0;background:var(--panel);border:1px solid var(--line);
  border-radius:9px;overflow:hidden;
  content-visibility:auto;contain-intrinsic-size:auto 640px}
figcaption{padding:.65rem .95rem;border-bottom:1px solid var(--line);
  display:flex;gap:.6rem;align-items:baseline;flex-wrap:wrap;font-size:.85rem}
figcaption .what{font-weight:600}
figcaption .dim{font-family:var(--mono);font-size:.74rem;color:var(--mut)}
.pic{padding:.55rem;overflow-x:auto;background:#07080b}
svg.frame{max-width:100%;height:auto;display:block;min-width:min(100%,720px)}
/* NO GREYSCALE TOGGLE, AND THE REASON IS WORTH KEEPING.  `filter:grayscale(1)`
   on these frames froze Chrome's renderer for 30 s+ -- reproducibly, and just
   as badly on ONE figure as on all twenty, which is what ruled out "too many
   layers" as the cause.  It is the `x` list: every glyph carries its own
   coordinate (that is what stops the cell grid drifting), so a filtered layer
   makes the compositor re-rasterise ~14 000 individually positioned glyphs per
   frame.  The grid fidelity is load-bearing and the toggle was a convenience,
   so the toggle went.  To run the greyscale test, open two `.svg` files from
   `prototypes/gallery/` side by side in a viewer that can desaturate. */
table{width:100%;border-collapse:collapse;font-size:.85rem;margin:.8rem 0 0}
th,td{text-align:left;padding:.42rem .6rem;border-bottom:1px solid var(--line);
  vertical-align:top}
th{color:var(--mut);font-size:.66rem;text-transform:uppercase;
  letter-spacing:.08em;font-weight:600}
.tw{overflow-x:auto}
.bar{display:inline-block;height:8px;background:var(--accent);border-radius:2px;
  vertical-align:middle;margin-right:.4rem}
/* THE APPARATUS IS AN APPENDIX WITH AN ANCHOR ROUTER, NOT A FLOATING PANEL,
   AND THAT IS FORCED BY MEASUREMENT.  A fixed overlay -- with or without a
   scrim -- froze Chrome's renderer for 30 s every single time it opened: a
   composited layer stacked over the document makes the compositor rasterise
   everything beneath it, and beneath it are twenty frames holding ~2900 text
   elements.  `content-visibility` cannot help, because the overlay is exactly
   the thing that forces the skipped content back into the frame.
   APPARATUS.md accepts "an appendix with an anchor router" alongside the
   floating panel, and the appendix costs nothing to composite, so the contract
   is met by the cheap form rather than the expensive one.  The `back` link on
   each entry is what makes it consultable from anywhere without losing your
   place. */
#ap{margin:4rem 0 0;scroll-margin-top:58px;border-top:1px solid var(--line);
  padding-top:1.6rem}
#ap .body{padding:1.1rem 0 0}
#ap .body h4{margin:1.4rem 0 .3rem;font-size:.92rem}
#ap .body h4:first-child{margin-top:0}
#ap .body p{font-size:.88rem;color:var(--mut);margin:.35rem 0;max-width:82ch}
#apbtn{position:fixed;right:1rem;bottom:1rem;z-index:60;background:var(--accent);
  color:#06222c;border:none;border-radius:99px;padding:.6rem 1rem;
  font:600 .8rem var(--sans);cursor:pointer;text-decoration:none;
  box-shadow:0 4px 18px rgba(0,0,0,.5)}
#apbtn:hover{text-decoration:none}
.backtop{display:inline-block;margin-top:1.6rem;font-size:.8rem}
.hidden{display:none}
footer{margin-top:5rem;padding-top:1.4rem;border-top:1px solid var(--line);
  color:var(--dim);font-size:.82rem}
@media (max-width:640px){.hero h1{font-size:1.5rem}main{padding:1.4rem .8rem 5rem}}
</style>
</head>
<body>""")

    a('<nav><div class="navin"><span class="brand">TEN LANGUAGES</span>')
    for n in langs:
        a(f'<a href="#{n}">{E(themes[n].get("label", n.title()))}</a>')
    a('<a href="#compare">Compare</a><a href="#how">How</a>'
      '<a href="#gloss">Glossary</a><a href="#refut">Refutations</a>'
      '<a href="#audit">Audit</a></div></nav>')

    dark = sum(1 for n in langs if themes[n]["ground"].lower() < "#800000")
    a(f"""<main id="top">
<div class="hero">
<h1>Ten TUI design languages</h1>
<p class="sub">Every language the <code>taskboard</code> widget prototype can
render, each shown twice: the <b>board</b> it composes and the <b>component
sheet</b> it draws. All twenty captures come from one sweep \u2014 one fixture,
one viewport ({m_board[langs[0]][0]}\u00d7{m_board[langs[0]][1]}), animations
off \u2014 because \u201csame screen, ten languages\u201d is only an honest
comparison when it really is the same screen. The doctrine under each name is
read from that language's own class docstring in
<code>taskboard/language.py</code>, so this page cannot drift from the code.</p>
<div class="kpis">
<div class="kpi"><b>{len(langs)}</b><span>languages</span></div>
<div class="kpi"><b>{len(langs) * 2}</b><span>captures</span></div>
<div class="kpi"><b>{len(set(layouts.values()))}</b><span>board layouts</span></div>
<div class="kpi"><b>{min(m_board[n][2] for n in langs):.0f}\u2013{max(m_board[n][2] for n in langs):.0f}%</b><span>ink range</span></div>
<div class="kpi"><b>{len(langs) - dark}</b><span>light ground</span></div>
</div>
<p style="color:var(--dim);font-size:.86rem;margin-top:1.2rem">
<b>The greyscale test is not built into this page, and that is a finding rather
than an omission.</b> The test matters — <i>a language that only changes
colour is not a language</i>: strip the hue from two frames, and if you cannot
tell them apart, one is a palette wearing a name. But applying
<code>filter:grayscale(1)</code> here froze the renderer for 30 s, as badly
on one frame as on twenty, because every glyph carries its own <code>x</code> so
the cell grid cannot drift — which means a filtered layer has to
re-rasterise ~14 000 individually positioned glyphs. Grid fidelity is
load-bearing; the toggle was a convenience. To run the test, open two files from
<code>prototypes/gallery/</code> in a viewer that can desaturate.
</p>
</div>""")

    # ---- the languages ----------------------------------------------------
    for i, n in enumerate(langs):
        t = themes[n]
        label = t.get("label", n.title())
        a(f'\n<section class="lang" id="{n}">')
        a(f'<div class="lhead"><span class="num">{i}</span><h2>{E(label)}</h2>'
          f'<span class="badge">{E(layouts[n])} family</span>'
          f'<span class="badge">{m_board[n][2]:.1f}% ink</span></div>')
        if t.get("note"):
            a(f'<p class="note">{E(str(t["note"]))}</p>')
        if docs[n]:
            a(f'<div class="doc">{doc_to_html(docs[n])}</div>')

        a("<h3>Structural tokens</h3><div class=\"axrow\">")
        for key, label_, _ in STRUCT:
            if key in t:
                a(f'<span class="ax"><i>{E(label_)}</i>'
                  f'<code>{E(str(t[key]))}</code></span>')
        a("</div>")
        a("<h3>Palette</h3>")
        a(swatch_row(t))

        for kind, fname, meas, what in (
                ("board", f"board_{n}", m_board[n], "Board"),
                ("gallery", f"gallery_{n}", m_gal[n], "Component sheet")):
            w, h, ik = meas
            a("<figure>")
            a(f'<figcaption><span class="what">{what}</span>'
              f'<span class="dim">{w}\u00d7{h} cells \u00b7 {ik:.1f}\u202f% ink '
              f'\u00b7 {fname}.txt</span>'
              f'</figcaption>')
            a(f'<div class="pic">{svg(fname)}</div>')
            a("</figure>")
        a("</section>")

    # ---- compare ----------------------------------------------------------
    mx = max(m_board[n][2] for n in langs)
    a("""
<section id="compare" style="margin-top:4.5rem;scroll-margin-top:58px">
<h2>All ten, side by side</h2>
<p style="color:var(--mut);max-width:78ch">Every column is read from the code,
not transcribed. Two languages agreeing on a whole row would be the defect
<code>LANGUAGES.md</code> records \u2014 <i>two of the eight languages rendered
byte-identically</i> \u2014 which is why the capture sweep refuses to finish
if any two boards come out the same.</p>
<div class="tw"><table><thead><tr><th>language</th><th>family</th><th>hero</th>
<th>structure</th><th>quantity</th><th>base</th><th>ink</th>
</tr></thead><tbody>""")
    for n in langs:
        t = themes[n]
        pct = m_board[n][2]
        a(f'<tr><td><a href="#{n}"><b>{E(t.get("label", n.title()))}</b></a></td>'
          f'<td>{E(str(layouts[n]))}</td>'
          f'<td><code>{E(str(t.get("hero", "\u2014")))}</code></td>'
          f'<td><code>{E(str(t.get("frame", "\u2014")))}</code></td>'
          f'<td><code>{E(str(t.get("meter", "\u2014")))}</code></td>'
          f'<td><code>{E(str(t.get("base", "\u2014")))}</code></td>'
          f'<td><span class="bar" style="width:{pct / mx * 70:.0f}px"></span>'
          f'{pct:.1f}\u202f%</td></tr>')
    a("</tbody></table></div>")

    a(f"""
<h3 style="margin-top:2.2rem">Two languages were retired, and that was a
decision</h3>
<p style="color:var(--mut);max-width:78ch">The skill's catalogue in
<code>LANGUAGES.md</code> still lists them; this app no longer renders them.
They were removed on 2026-07-26 by operator curation, not by a bug \u2014 so the
count here is ten and not twelve, and the difference is on the record rather
than hidden in a diff.</p>
<div class="tw"><table><thead><tr><th>retired</th><th>what it committed to</th>
</tr></thead><tbody>""")
    for k, v in RETIRED.items():
        a(f"<tr><td><b>{E(k)}</b></td><td>{E(v)}</td></tr>")
    a("</tbody></table></div></section>")

    # ---- how --------------------------------------------------------------
    a(f"""
<section id="how" style="margin-top:4rem;scroll-margin-top:58px">
<h2>How to run it yourself</h2>
<p style="color:var(--mut);max-width:78ch">The pictures are a projection. The
thing itself is an app, and it is worth driving \u2014 resize the window and
the surface changes on its own, which is the part a still cannot show.</p>
<pre style="background:#0b0d12;border:1px solid var(--line);border-radius:8px;
padding:.9rem 1.1rem;overflow-x:auto;font-size:.83rem;color:var(--mut)"><code
style="background:none;border:none;padding:0">cd "C:\\Users\\jjgh8\\Github\\taskboard\\.claude\\worktrees\\kanban-variants"
$env:PYTHONIOENCODING = "utf-8"
python prototypes\\widget_slice\\app.py</code></pre>
<div class="tw"><table><thead><tr><th>key</th><th>what it does</th></tr></thead>
<tbody>
<tr><td><code>t</code></td><td>cycle the visual language \u2014 the ten above,
in this order</td></tr>
<tr><td><code>g</code></td><td>component gallery: every component of the active
language on one screen. Press <code>t</code> inside it to compare</td></tr>
<tr><td><code>1</code>\u2013<code>4</code></td><td>board \u00b7 swimlanes \u00b7
agenda \u00b7 gantt</td></tr>
<tr><td><code>v</code></td><td>force size class (glance / widget / board)</td></tr>
<tr><td><code>c</code></td><td>the signal engine config \u2014 the screen
COMPONENTS.md calls the canary</td></tr>
<tr><td><code>?</code></td><td>the full keymap, including the bindings the
footer hides</td></tr>
</tbody></table></div>
<h3 style="margin-top:2rem">Rebuild these captures and this page</h3>
<pre style="background:#0b0d12;border:1px solid var(--line);border-radius:8px;
padding:.9rem 1.1rem;overflow-x:auto;font-size:.83rem;color:var(--mut)"><code
style="background:none;border:none;padding:0">python prototypes\\capture_languages.py     # 20 captures, checked for determinism
python prototypes\\build_languages_html.py   # this page</code></pre>
</section>

""")

    # ---- apparatus --------------------------------------------------------
    a("""
<a id="apbtn" href="#ap">Apparatus ↓</a>
<section id="ap" aria-label="Apparatus">
<h2>Apparatus</h2>
<p style="color:var(--mut);max-width:80ch">Consultable from anywhere — linked
from the top bar and from the button that follows you down the page. Every term,
every refutation, and the provenance of every capture.</p>
<div class="body">
<div data-p="gloss" id="gloss">
<h3 style="font-size:1.15rem;text-transform:none;letter-spacing:0;color:var(--fg)">Glossary</h3>
<h4>The structural tokens</h4>""")
    for key, label_, why in STRUCT:
        a(f"<p><b>{E(label_)}</b> (<code>{E(key)}</code>) \u2014 {E(why)}. "
          f"Values in use: "
          + ", ".join(f"<code>{E(str(themes[n][key]))}</code>"
                      for n in dict.fromkeys(
                          x for x in langs if key in themes[x]))
          + ".</p>")
    a("""<h4>Terms</h4>
<p><b>structure kit</b> \u2014 the implementation shape a language survives in:
one Kit object every surface draws through, one method per surface primitive,
mechanisms dispatched on the token. Its opposite is per-widget
<code>if theme ==</code> branches, which is how a language decays into a
palette.</p>
<p><b>ink fraction</b> \u2014 non-space cells / total cells, measured from the
captured grid. It is a density reading, not a quality score: Swiss is airy on
purpose and Ledger is dense on purpose.</p>
<p><b>component sheet</b> \u2014 slider, bar, switch, checkbox, radio, button,
text field, scroll bar and stepper, each in every state. The layer that ships
unstyled because \u201cit's just settings\u201d, which is why it is captured
here beside the board.</p>
<p><b>the greyscale test</b> \u2014 render two languages with hue removed. If
you cannot tell them apart, you changed the palette and called it a language.
Run it outside this page: see the note under the title.</p>
<p><b>settle</b> \u2014 waiting for a frame that is actually PAINTED, not
merely produced. A widget can be mounted and still not flushed, and it is the
flush a capture reads.</p>
</div>
<div data-p="refut" id="refut">
<h3 style="font-size:1.15rem;text-transform:none;letter-spacing:0;color:var(--fg);margin-top:2.6rem">Refutations</h3>
<p style="color:var(--mut)">Verified corrections, each stating what changes if
you believe the wrong version.</p>
<div class="ref" style="border:1px solid var(--line);border-radius:7px;
padding:.7rem .85rem;margin:.7rem 0;background:var(--panel)">
<span style="font-family:var(--mono);color:var(--accent);font-size:.78rem">
M-01</span>
<span style="font-size:.62rem;text-transform:uppercase;letter-spacing:.08em;
color:var(--warn);border:1px solid #5c4a22;border-radius:99px;padding:.1rem
.45rem;margin-left:.4rem">creencia popular</span>
<span style="display:block;margin:.35rem 0 .5rem;color:var(--fg);
font-size:.9rem">\u201cWe shipped N palettes, so we shipped N design
languages.\u201d</span>
<p><b>Verified:</b> the first attempt shipped six palettes over one identical
layout \u2014 same hero, same frames, same meter. A later pass declared
<code>base</code>, <code>frame</code>, <code>numbered</code> and
<code>dot_w</code> on eight languages and <b>none of them were read by any
renderer</b>; two of the eight rendered byte-identically.</p>
<p><b>What holds instead:</b> a language is at least three structural
commitments \u2014 hero mechanism, structure device, quantity mechanism \u2014
and every token must be consumed by a renderer. The check is to
<b>mutate the token and confirm the render changes</b>.</p>
<p><b>What changes if you believe the wrong version:</b> the token
<i>documents</i> a difference that does not exist, which is worse than a plain
recolour. And you lose the second-order consequence that makes languages worth
having: a language changes <b>what each channel is allowed to mean</b>.
Phosphor had one hue, so severity moved to brightness; Industrial spends colour
on identity, so urgency moved to a glyph; Swiss removes drawn type, so emphasis
moved to space.</p>
</div>
<div class="ref" style="border:1px solid var(--line);border-radius:7px;
padding:.7rem .85rem;margin:.7rem 0;background:var(--panel)">
<span style="font-family:var(--mono);color:var(--accent);font-size:.78rem">
M-02</span>
<span style="font-size:.62rem;text-transform:uppercase;letter-spacing:.08em;
color:var(--warn);border:1px solid #5c4a22;border-radius:99px;padding:.1rem
.45rem;margin-left:.4rem">creencia popular</span>
<span style="display:block;margin:.35rem 0 .5rem;color:var(--fg);
font-size:.9rem">\u201cThe languages look completely different \u2014 look at
the hero.\u201d</span>
<p><b>Verified:</b> the failed version of the kit passed every eyeball test
<i>because</i> the hero did change, while the rest of the screen was
identical.</p>
<p><b>What holds instead:</b> languages must differ <b>outside the signature
element</b>. Mask the hero's region out of the captured strips before diffing
the pair \u2014 and capture the component sheet, not only the board.</p>
<p><b>What changes if you believe the wrong version:</b> you ship one language
wearing ten hats, and find out on the settings screen, which has no hero to
carry it.</p>
</div>
<div class="ref" style="border:1px solid var(--line);border-radius:7px;
padding:.7rem .85rem;margin:.7rem 0;background:var(--panel)">
<span style="font-family:var(--mono);color:var(--accent);font-size:.78rem">
M-03</span>
<span style="font-size:.62rem;text-transform:uppercase;letter-spacing:.08em;
color:var(--warn);border:1px solid #5c4a22;border-radius:99px;padding:.1rem
.45rem;margin-left:.4rem">era cierto y caduc\u00f3</span>
<span style="display:block;margin:.35rem 0 .5rem;color:var(--fg);
font-size:.9rem">\u201cTwo identical frames means the screen has
settled.\u201d</span>
<p><b>Verified:</b> measured while building this page. With animations on,
<code>solari</code> came back at 36.3\u202f% ink on one run and 36.1\u202f% on
the next; the diff was a single row, <code>DAYS OVERDUE</code>, present in one
capture and blank in the other. Solari is a split-flap board and its label was
caught mid-flip.</p>
<p><b>What holds instead:</b> an animation has still moments between steps, so
two identical frames is not proof of rest. Set
<code>TEXTUAL_ANIMATIONS=none</code>, which degrades every animation to its
final frame, and then <b>sweep twice and diff</b>.</p>
<p><b>What changes if you believe the wrong version:</b> your reference picture
is a photograph of a moment, not of a design \u2014 and it changes under you
every time you rebuild, which reads as a rendering bug in whatever consumes it.</p>
</div>
</div>
<div data-p="audit" id="audit">
<h3 style="font-size:1.15rem;text-transform:none;letter-spacing:0;color:var(--fg);margin-top:2.6rem">Audit</h3>""")
    a(f"<p style='color:var(--mut)'>{len(langs) * 2} captures, one sweep, "
      f"fixture <code>_fixture_late.json</code>, viewport "
      f"{m_board[langs[0]][0]}\u00d7{m_board[langs[0]][1]}, animations off. "
      f"Every grid was verified identical across two consecutive sweeps.</p>")
    a("<div class='tw'><table><thead><tr><th>language</th><th>board</th>"
      "<th>components</th></tr></thead><tbody>")
    for n in langs:
        a(f'<tr><td>{E(themes[n].get("label", n))}</td>'
          f'<td>{m_board[n][0]}\u00d7{m_board[n][1]} \u00b7 '
          f'{m_board[n][2]:.1f}\u202f%</td>'
          f'<td>{m_gal[n][0]}\u00d7{m_gal[n][1]} \u00b7 '
          f'{m_gal[n][2]:.1f}\u202f%</td></tr>')
    a("</tbody></table></div>")
    a("""<h4>What this page did NOT verify</h4>
<p>That every structural token is <i>consumed</i> by a renderer \u2014 the
mutation check that keeps a token from being dead metadata. That is
<code>prototypes/verify_language.py</code>'s job, and it is the file that owns
the claim. This page reads the tokens and shows the renders; it does not prove
the link between them.</p>
<p>That the captures match a real terminal. They are taken off Textual's
compositor headless, which is the same surface the app paints, but no run in a
real terminal emulator was diffed against them.</p>
</div>
</div>
<a class="backtop" href="#top">↑ back to the top</a>
</section>
""")

    a(f"""<footer>
Built by <code>build_languages_html.py</code> from {len(langs) * 2} captures
taken by <code>capture_languages.py</code> off
<code>_fixture_late.json</code>. Doctrine is <code>inspect.getdoc()</code> on
each Kit; tokens are read from <code>themes.py</code>; every dimension and ink
figure is measured from the captured grid. Nothing on this page is transcribed.
</footer>
</main>""")

    a("""</body>
</html>
""")
    return "\n".join(P)


if __name__ == "__main__":
    dest = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_DEST
    out = build()
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(out, encoding="utf-8")
    print(f"  {dest}  ({len(out) / 1024:.0f} KB)")
