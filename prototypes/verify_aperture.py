"""THE APERTURE acceptance test — the widget posture inside the REAL app.

HANDOFF.md §4 Increment 2 is only real if: the `6` key opens it in the real
TaskboardApp, the hero RENDERS (not labels), `t` cycles EVERY language in
`themes.ORDER` (TEN since the blueprint pass; the cycle checks read ORDER, so
they scale on their own — the only edit this file has ever needed for a new
language is this sentence, and blueprint needed no more than that: its hero is
`plain` at 7 rows, well inside the 12-row wrap budget, and its title block is
docked inside `#tabs`, a seat the aperture screen does not mount) with the
frame visibly changing (greyscale — never
colour alone), the number
keys exit INTO the chosen view (the launcher thesis), and the five existing
views + their 2,509 lines of tests stay untouched (run pytest separately).

Probe discipline: bounded loops, settled frames, content assertions.
"""
import asyncio
import json
import re
import sys
from datetime import date
from pathlib import Path

W = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(W))

from taskboard import hero as HERO         # noqa: E402
from taskboard import language as LG       # noqa: E402
from taskboard import themes as TH        # noqa: E402
from taskboard.app import HelpScreen, TaskboardApp, binding_map  # noqa: E402
from taskboard.aperture import ApertureScreen  # noqa: E402

fails = []


def check(name, cond, detail=""):
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}{'  ' + detail if detail else ''}")
    if not cond:
        fails.append(name)


_TAG = re.compile(r"\[[^\[\]]*\]")


def grey(m):
    return _TAG.sub("", m.replace("\\[", "\x00")).replace("\x00", "[")


def rows_of(app):
    return ["".join(s.text for s in strip)
            for strip in app.screen._compositor.render_strips()]


# ---- the LEGEND LAW (forty-first pass) -------------------------------------
# The shipped aperture composed no legend at all: 22 bindings were live there
# and one hand-written line named four of them — `q`, which QUIT THE APP, was
# not among them. The law, stated so it can fail: every key that fires on a
# surface is printed on that surface, every key printed there fires, and no
# printed key needs shift.

def legend_of(app):
    """The legend AS COMPOSITED — the row the user's eye lands on, not the
    markup we hoped we wrote (a wrapped or clipped row still reads fine in
    source)."""
    r = app.screen.query_one("#ap-foot").region
    rows = rows_of(app)
    if r.height < 1 or r.y >= len(rows):
        return ""
    return rows[r.y][r.x:r.x + r.width].strip()


def keyset_of(screen):
    """Every key display that is LIVE here, atomised: `q/esc/6` -> q, esc, 6."""
    out = set()
    for disp, _, _ in binding_map(screen):
        out.update(disp.split("/"))
    return out


def parse_legend(row, keys):
    """[(key tokens, label)] for each ` · ` entry. An entry whose leading token
    is not a live key yields NO keys — which is how a phantom entry is caught
    by name rather than by count."""
    out = []
    for e in (p.strip() for p in row.split("·")):
        if not e:
            continue
        toks, i = e.split(), 0
        while i < len(toks) and all(t in keys for t in toks[i].split("/")):
            i += 1
        out.append((toks[:i], " ".join(toks[i:])))
    return out


def shifted(key: str) -> bool:
    return key.startswith("shift+") or (len(key) == 1 and key.isupper())


async def main():
    fx = W / "prototypes" / "out" / "_fixture_board.json"

    print("== the 6 key opens the aperture in the REAL app")
    app = TaskboardApp(board_path=str(fx))
    async with app.run_test(size=(96, 30)) as pilot:
        await pilot.pause()
        app.notify = lambda *a, **kw: None
        await pilot.press("6")
        await pilot.pause()
        check("6 pushes the ApertureScreen",
              isinstance(app.screen, ApertureScreen))
        scr = app.screen
        scr.engine.run_all()
        scr.redraw()
        await pilot.pause()
        frame = "\n".join(rows_of(app))
        check("the hero RENDERS (frame carries ink)",
              len(frame.strip()) > 100)
        check("the queue names real tasks", "UP NEXT" in frame)

        print(f"\n== t cycles all {len(TH.ORDER)} languages, frames differ "
              f"in GREYSCALE")
        frames = {}
        for _ in range(len(TH.ORDER)):
            scr.redraw()
            await pilot.pause()
            frames[scr.lang] = "\n".join(rows_of(app))
            # NOTHING WRAPPED: a hero built wider than its widget doubles its
            # rows silently (their geometry gate missed this; ours must not).
            # Budget 9 + airy slack (swiss spends blank rows by design, 11);
            # real wraps measured 15-21 — the boundary is clean at 12
            check(f"{scr.lang}: hero rows fit its budget (no wrap)",
                  scr.query_one("#hero").region.height <= 12,
                  f"h={scr.query_one('#hero').region.height}")
            await pilot.press("t")
            await pilot.pause()
        check(f"all {len(TH.ORDER)} languages reachable",
              set(frames) == set(TH.ORDER), f"{len(frames)} seen")
        check("no two languages render the same aperture frame",
              len(set(frames.values())) == len(frames))

        print("\n== the aperture remembers its language across opens")
        scr.set_language("darkside")
        await pilot.press("escape")
        await pilot.pause()
        check("escape returns to the board",
              not isinstance(app.screen, ApertureScreen))
        await pilot.press("6")
        await pilot.pause()
        check("the language persisted (darkside)",
              getattr(app.screen, "lang", "") == "darkside")

        print("\n== the LAUNCHER thesis: number keys exit INTO a view")
        await pilot.press("3")
        await pilot.pause()
        check("3 pops the aperture and lands on the agenda",
              not isinstance(app.screen, ApertureScreen)
              and app.view_mode == "agenda")

        print("\n== the board's priority arrows stay with the board")
        sel = app.selected_task_id
        await pilot.press("6")
        await pilot.pause()
        await pilot.press("down")
        await pilot.pause()
        check("arrows inside the aperture do not move the hidden selection",
              app.selected_task_id == sel)

async def legend_laws():
    fx = str(W / "prototypes" / "out" / "_fixture_board.json")

    print("\n== the law's own self-check: a law nobody has seen fail is a law "
          "nobody has tested")
    ks = {"1", "2", "t", "q", "esc", "?"}
    check("a PHANTOM entry is caught by name, not by count",
          not all(k and lab for k, lab in
                  parse_legend("1 lanes · z gallery", ks)))
    check("an entry with keys but NO word is caught",
          not all(k and lab for k, lab in parse_legend("1 lanes · t", ks)))
    check("a deleted key is caught",
          {p for k, _ in parse_legend("1 lanes · t language", ks)
           for t_ in k for p in t_.split("/")} != {"1", "2", "t"})
    check("a shifted key is caught, an unshifted one is not",
          shifted("V") and shifted("shift+tab")
          and not (shifted("q") or shifted("esc") or shifted("?")))

    print("\n== THE LEGEND, per language: it carries every live key and only "
          "live keys")
    app = TaskboardApp(board_path=fx)
    async with app.run_test(size=(118, 34)) as pilot:
        await pilot.pause()
        app.notify = lambda *a, **kw: None
        await pilot.press("6")
        for _ in range(6):
            await pilot.pause()
        scr = app.screen
        promised = {}
        for name in TH.ORDER:
            scr.set_language(name)
            scr.redraw()
            for _ in range(3):
                await pilot.pause()
            row = legend_of(app)
            keys = keyset_of(scr)
            shown = binding_map(scr, shown=True)
            parsed = parse_legend(row, keys)
            named = {p for ks, _ in parsed for k in ks for p in k.split("/")}
            promised[name] = named
            check(f"{name}: every entry starts with a LIVE key and carries a "
                  f"word", bool(parsed) and all(ks and lab for ks, lab in parsed),
                  repr(row[:70]))
            want = {k for disp, _, _ in shown for k in disp.split("/")}
            check(f"{name}: every shown key is printed", named == want,
                  f"missing {sorted(want - named)} extra {sorted(named - want)}")
            check(f"{name}: no printed key needs shift",
                  not any(shifted(k) for k in named))
            check(f"{name}: the row fits its one row (never clipped)",
                  len(row) <= scr.query_one("#ap-foot").region.width)
        check("all languages promise the IDENTICAL key set "
              "(a language restyles the legend, it may not change the keymap)",
              len(set(map(frozenset, promised.values()))) == 1)

        print("\n== the legend DEGRADES instead of clipping")
        seen = {}
        for w in (118, 96, 60):
            app.screen.set_language("naught")
            await pilot.resize_terminal(w, 34)
            for _ in range(4):
                await pilot.pause()
            row = legend_of(app)
            seen[w] = row
            check(f"{w} cols: the row still fits", len(row) <= w,
                  repr(row[:60]))
            check(f"{w} cols: the way out and the map survive",
                  " back" in row and "? keys" in row)
        check("the wide row spends WORDS the narrow one cannot",
              len(seen[118]) > len(seen[60]) and "lanes" in seen[118])
        check("the middle tier keeps every view key under one label",
              all(k in seen[96] for k in "12345") and "views" in seen[96])
        await pilot.resize_terminal(118, 34)
        for _ in range(3):
            await pilot.pause()

        print("\n== the BOARD's keys are dropped here, not merely unindicated")
        for key in ("a", "e", "d", "x", "o", "i", "c", "p", "f", "P", "enter",
                    "delete"):
            await pilot.press(key)
            await pilot.pause()
            if not isinstance(app.screen, ApertureScreen):
                check(f"{key!r} does nothing on the aperture", False,
                      f"pushed {type(app.screen).__name__}")
                await pilot.press("escape")
                await pilot.pause()
        check("no board key fires on the aperture (a d e x o i c p f P ⏎ del)",
              isinstance(app.screen, ApertureScreen)
              and len(app.screen_stack) == 2)
        live = {k for k, _, _ in binding_map(app.screen)}
        check("and none of them is left LISTED-but-disabled",
              not {"a", "e", "d", "x", "o", "i", "c", "p", "f", "P"} & live,
              f"live: {sorted(live)}")

        print("\n== every printed key FIRES, driven one at a time, unshifted")
        for key, mode in (("1", "swimlanes"), ("2", "columns"), ("3", "agenda"),
                          ("4", "gantt"), ("5", "kanban")):
            await pilot.press("6")
            for _ in range(3):
                await pilot.pause()
            await pilot.press(key)
            for _ in range(3):
                await pilot.pause()
            check(f"{key} exits INTO {mode}",
                  not isinstance(app.screen, ApertureScreen)
                  and app.view_mode == mode)
        await pilot.press("6")
        for _ in range(4):
            await pilot.pause()
        before = app.screen.lang
        await pilot.press("t")
        for _ in range(3):
            await pilot.pause()
        check("t cycles the language (unshifted)", app.screen.lang != before)
        frame = "\n".join(rows_of(app))
        await pilot.press("r")
        for _ in range(3):
            await pilot.pause()
        check("r refreshes and stays on the aperture",
              isinstance(app.screen, ApertureScreen)
              and "\n".join(rows_of(app)) != "" and frame != "")
        await pilot.press("escape")
        await pilot.pause()
        check("esc returns to the board", not isinstance(app.screen,
                                                         ApertureScreen))
        await pilot.press("6")
        for _ in range(3):
            await pilot.pause()
        await pilot.press("q")
        for _ in range(3):
            await pilot.pause()
        check("q closes the aperture and the app SURVIVES "
              "(it used to quit from here, unindicated)",
              not isinstance(app.screen, ApertureScreen) and app.is_running)

        print("\n== the `?` map carries what the legend cannot")
        await pilot.press("6")
        for _ in range(3):
            await pilot.pause()
        under = binding_map(app.screen)
        await pilot.press("question_mark")
        for _ in range(4):
            await pilot.pause()
        check("? opens the map from the aperture",
              isinstance(app.screen, HelpScreen))
        mapped = "\n".join(rows_of(app))
        missing = [d for d, _, _ in under if d not in mapped]
        check("the map prints EVERY live key of the surface behind it, "
              "hidden ones included", not missing, f"missing {missing}")
        check("including the two nobody's BINDINGS list owns (ctrl+q, ctrl+p)",
              "ctrl+q" in mapped and "ctrl+p" in mapped)
        await pilot.press("escape")
        await pilot.pause()
        check("esc closes the map onto the aperture",
              isinstance(app.screen, ApertureScreen))

    print("\n== THE MAIN SCREEN: the footer is honest AND fits")
    app = TaskboardApp(board_path=fx)
    async with app.run_test(size=(118, 34)) as pilot:
        await pilot.pause()
        app.notify = lambda *a, **kw: None
        for _ in range(4):
            await pilot.pause()
        foot = rows_of(app)[-1]
        shown = binding_map(app.screen, shown=True)
        check("29 shown bindings became a set the footer can PRINT",
              len(shown) <= 12, f"{len(shown)} shown")
        for disp, desc, _ in shown:
            check(f"footer prints {disp} {desc}",
                  disp.split("/")[0] in foot and desc in foot)
        check("`q Quit` is on the footer (it used to be clipped off the edge)",
              "q Quit" in foot)
        check("`? Keys` is on the footer", "? Keys" in foot)
        check("no shown binding on the board needs shift",
              not any(shifted(k) for disp, _, _ in shown
                      for k in disp.split("/")))
        hidden = binding_map(app.screen, shown=False)
        check("every hidden binding still carries a WORD (the map needs one)",
              all(t for _, t, _ in hidden))

        print("\n== P -> Projects moved off shift")
        check("`m` opens the project manager, unshifted",
              any(d == "m" for d, _, _ in binding_map(app.screen)))
        check("`P` is gone from the binding map ENTIRELY — not merely hidden, "
              "which a shown=True query alone could never tell apart",
              not any("P" in d.split("/")
                      for d, _, b in binding_map(app.screen)))
        await pilot.press("m")
        for _ in range(4):
            await pilot.pause()
        check("pressing `m` really opens it",
              type(app.screen).__name__ == "ProjectPicker",
              type(app.screen).__name__)
        await pilot.press("escape")
        for _ in range(3):
            await pilot.pause()

        print("\n== the `?` map of the board lists every key the footer drops")
        # the two halves separately, exactly as the map builds them: `q Quit`
        # and `ctrl+q Quit` are one action with one word and merge otherwise
        under = (binding_map(app.screen, shown=True)
                 + binding_map(app.screen, shown=False))
        await pilot.press("question_mark")
        for _ in range(4):
            await pilot.pause()
        check("? opens the map from the board", isinstance(app.screen,
                                                           HelpScreen))
        mapped = "\n".join(rows_of(app))
        missing = [f"{d} {t}" for d, t, _ in under
                   if d not in mapped or t not in mapped]
        check("every live key AND its word is in the map, unclipped",
              not missing, f"missing {missing}")
        check("the map names its own way out", "close" in mapped)
        await pilot.press("q")
        for _ in range(3):
            await pilot.pause()
        check("q closes the map, the app survives",
              not isinstance(app.screen, HelpScreen) and app.is_running)

    print("\n== the quit path, on its own app (so a green suite is not a "
          "killed one)")
    app = TaskboardApp(board_path=fx)
    async with app.run_test(size=(118, 34)) as pilot:
        await pilot.pause()
        app.notify = lambda *a, **kw: None
        for _ in range(3):
            await pilot.pause()
        await pilot.press("q")
        for _ in range(4):
            await pilot.pause()
        check("q on the BOARD still quits (quit did not go missing)",
              not app.is_running)

    app = TaskboardApp(board_path=fx)
    async with app.run_test(size=(118, 34)) as pilot:
        await pilot.pause()
        app.notify = lambda *a, **kw: None
        await pilot.press("6")
        for _ in range(4):
            await pilot.pause()
        await pilot.press("ctrl+q")
        for _ in range(4):
            await pilot.pause()
        check("ctrl+q still quits FROM the aperture (the one door from "
              "anywhere)", not app.is_running)


# ---- THE PANEL'S GEOMETRY LAWS (forty-fifth pass) --------------------------
# Two shipped-seat defects, both invisible in source and both measured on the
# compositor, closed together because they are the same kind of mistake — a
# region built against a budget that is not the one it stands in.
#
#   A. the hero's dead columns RENOUNCED a row. `_beside_plot` reserved the
#      load caption twice (`min(7, len(rows) - 1)`, then `kit.plot(..., ph-1)`),
#      so a 7-row hero drew 5 data rows + caption in a panel that afforded 6,
#      and the bottom visible row of the panel went empty (industrial, 118x34).
#   B. the queue row OVERFLOWED. It was built as `marker + 1 + (w - 8) + 5`,
#      which closes on `w` only for a 2-cell marker: corgi and industrial draw
#      `[1]` and spent w+1 (measured 114 in a 113-cell panel), and ledger cut
#      its folio to two cells rather than step on it.
#
# Both laws run against the SETTLED frame: `set_language` says in its own
# comment that `redraw` right after it measures the PREVIOUS language's
# geometry, so the layout is allowed to land before the render is asked for.

async def show(pilot, scr, name):
    scr.set_language(name)
    scr.engine.run_all()
    for _ in range(4):                     # let the new stylesheet lay out
        await pilot.pause()
    scr.redraw()                           # ... and only then measure widths
    for _ in range(3):
        await pilot.pause()


def region_rows(app, wid):
    r = app.screen.query_one(wid).region
    rows = rows_of(app)
    return [rows[y][r.x:r.x + r.width]
            for y in range(r.y, min(r.y + r.height, len(rows)))], r


def old_band(n_rows: int) -> int:
    """Pass 44's arithmetic verbatim, kept here as the CONTROL: the band the
    join used to draw for a hero of `n_rows` rows (data + caption)."""
    return min(7, n_rows - 1)


def old_queue_row(mark: str, w: int, chip: str) -> str:
    """The queue row as it was BUILT before the cure — `marker + 1 + (w - 8)
    + 5` — so the overflow can be measured rather than remembered."""
    return f"{mark} " + " " * max(1, w - 8) + f"{chip:>5}"


async def panel_laws():
    fx = str(W / "prototypes" / "out" / "_fixture_board.json")

    print("\n== THE LOAD BAND SPENDS EVERY ROW THE HERO PANEL HAS")
    app = TaskboardApp(board_path=fx)
    async with app.run_test(size=(118, 34)) as pilot:
        await pilot.pause()
        app.notify = lambda *a, **kw: None
        await pilot.press("6")
        for _ in range(4):
            await pilot.pause()
        scr = app.screen
        plotted = 0
        for name in TH.ORDER:
            await show(pilot, scr, name)
            hrows, hr = region_rows(app, "#hero")
            cap = [i for i, r in enumerate(hrows) if HERO.PLOT_CAP in r]
            if not cap:
                # asserted, never silent: the only honest reason a hero has no
                # dead columns is that it has no columns to spare
                check(f"{name}: no dead-columns plot, and the panel SAYS why "
                      f"(its hero is under the 72-cell threshold)",
                      hr.width - 1 < 72, f"hero w={hr.width}")
                continue
            plotted += 1
            i = cap[-1]
            below = hrows[i + 1:]
            if HERO.ambient_load(scr.kit):
                # the demoted tier is ONE row and it rides the hero's last
                # drawn row — there is nothing under it to renounce
                check(f"{name}: the ambient load row rides the panel's LAST "
                      f"drawn row", not any(r.strip() for r in below),
                      f"caption row {i} of {len(hrows)}")
                continue
            check(f"{name}: the load band renounces no row of its panel — it "
                  f"is at its 7-row cap or every row under it is USED",
                  i + 1 == 7 or all(r.strip() for r in below),
                  f"band {i + 1}, {sum(1 for r in below if not r.strip())} "
                  f"blank row(s) under it")
        check("the law is not vacuous: most languages really do draw the "
              "dead-columns plot at 118x34", plotted >= 7, f"{plotted}/10")

        print("\n== ... and the CONTROL: the arithmetic it replaces failed it")
        # industrial is the language the cure moved: a `plain` hero of 4 rows,
        # padded to 7 so the load has a band to stand in
        await show(pilot, scr, "industrial")
        hrows, hr = region_rows(app, "#hero")
        cap_i = [i for i, r in enumerate(hrows) if HERO.PLOT_CAP in r][-1]
        check("industrial: the cured band closes on the panel's last row",
              cap_i + 1 == len(hrows) == 7, f"band {cap_i + 1} of {len(hrows)}")
        check("the OLD arithmetic gave that same 7-row panel a 6-row band, "
              "leaving the bottom row blank (the defect, reproduced)",
              old_band(7) == 6 and old_band(7) < cap_i + 1)
        # and the same arithmetic really is what shipped: re-break the join and
        # watch the law go red, then restore it
        real = HERO._beside_plot

        def broken(kit, text, w_main, plot_w, series, max_rows):
            rows = text.split(HERO.NL)
            if HERO.ambient_load(kit):
                return real(kit, text, w_main, plot_w, series, max_rows)
            while len(rows) < min(7, max_rows):
                rows.append("")
            ph = old_band(len(rows))
            if ph < 4:
                return text
            prows = kit.plot(series, plot_w, ph - 1)
            prows.append(f"[{kit.c['dim']}]{HERO.PLOT_CAP}[/]")
            out = []
            for i2, r in enumerate(rows):
                if i2 < len(prows):
                    r = (r + " " * max(0, w_main - HERO.vis_w(r))
                         + "  " + prows[i2])
                out.append(r)
            return HERO.NL.join(out)

        HERO._beside_plot = broken
        try:
            await show(pilot, scr, "industrial")
            brows, _ = region_rows(app, "#hero")
            bcap = [i for i, r in enumerate(brows) if HERO.PLOT_CAP in r][-1]
            check("MUTATION: with the old join back, industrial's bottom "
                  "panel row goes blank again and the law FAILS",
                  bcap + 1 < 7 and not brows[-1].strip(),
                  f"band {bcap + 1} of {len(brows)}")
        finally:
            HERO._beside_plot = real
        await show(pilot, scr, "industrial")
        rrows, _ = region_rows(app, "#hero")
        check("... and the cure restores it (the control left nothing behind)",
              HERO.PLOT_CAP in rrows[-1])

        print("\n== EVERY QUEUE ROW CLOSES INSIDE THE PANEL IT STANDS IN")
        fit = {}
        for name in TH.ORDER:
            await show(pilot, scr, name)
            prows, pr = region_rows(app, "#ap-panel")
            # exactly what `redraw`'s `wof()` hands the queue: the region minus
            # the cell it reserves
            budget = max(10, pr.width - 1)
            body = [r for r in prows if r.strip()]
            # the queue rows are the ones carrying a due chip; the header and
            # any calendar rows above it are not measured by this law
            qrows = [r for r in prows if r.rstrip().endswith(("d", "d!", "--"))]
            over = [(i, len(r.rstrip())) for i, r in enumerate(prows)
                    if len(r.rstrip()) > budget]
            check(f"{name}: the panel really drew a queue (a fit law over an "
                  f"empty panel is vacuous)",
                  len(body) >= 4 and any("UP NEXT" in r for r in prows)
                  and len(qrows) >= 3,
                  f"{len(body)} row(s), {len(qrows)} queued, panel w={pr.width}")
            check(f"{name}: no queue row exceeds the panel's own measure",
                  not over, f"budget {budget}, over: {over}")
            fit[name] = (budget, sorted({len(r.rstrip()) for r in qrows}))
        check("and every language's queue rows close EXACTLY on that measure "
              "— a row one cell short is the same missed measurement as a row "
              "one cell over, pointing the other way",
              all(w == [b] for b, w in fit.values()),
              f"{[(n, b, w) for n, (b, w) in fit.items() if w != [b]]}")

        print("\n== ... and the CONTROL: the row the cure replaced overflowed")
        widths = {n: HERO.vis_w(LG.kit(n).queue_marker(0)) for n in TH.ORDER}
        check("the language set really exercises a 3-cell marker, so the "
              "overflow case is REACHED and not merely guarded against",
              max(widths.values()) >= 3,
              f"marker widths {sorted(set(widths.values()))}")
        await show(pilot, scr, "corgi")
        _, pr = region_rows(app, "#ap-panel")
        budget = max(10, pr.width - 1)
        mark = scr.kit.queue_marker(0)
        check("corgi: the OLD row arithmetic overflows this very panel by a "
              "cell (pass 21's 93-in-92, at this width)",
              HERO.vis_w(old_queue_row(mark, budget, "2d!")) == budget + 1,
              f"{HERO.vis_w(old_queue_row(mark, budget, '2d!'))} in {budget}")
        built = [HERO.vis_w(r)
                 for r in scr._queue_markup(budget, 6).split("\n")[1:]]
        check("corgi: the CURED rows close on the panel EXACTLY — the marker "
              "is measured, not assumed two cells wide",
              bool(built) and set(built) == {budget},
              f"built {sorted(set(built))} against {budget}")


# ---- THE ESCAPE SWEEP AT THE SHIPPED SEAT (fifty-seventh pass) ------------
# Pass 56 swept `language.py` and found the defect was not a leaked `[/]` but
# SILENT DELETION: rich's `escape` only escapes a `[` that looks like the start
# of a TAG (`[` then `[a-z#/@]`), so `[URGENT]` goes through untouched — and
# Textual, whose tokenizer is not rich's and is what `Static.update` actually
# parses, reads it as a tag and swallows it. That pass's budget stopped at
# `language.py` and it filed the rest as item #32, with `aperture.py:386`
# MEASURED eating `[URGENT]` out of the queue in three languages.
#
# This section is that item's design-scope half, closed and pinned. Two
# shipped files carry user text through markup here, and both were doing it
# rich's way:
#
#   `aperture.py:386`  the queue row's title. Driven for all TEN languages
#                      (`_p57_prove.py` §1 PRE), all ten ate `[URGENT]`.
#   `hero.py:250`      the hero's detail line. `detail` is NOT an app literal:
#                      `engine.sig_deadline` puts `t.title` in it
#                      (engine.py:100-105), so the nearest deadline's TITLE is
#                      what the hero prints. swiss, industrial and darkside
#                      were each printing a bare `rotate keys`.
#
# WHY THE FIXTURE'S DATES ARE NOT ALL THE SAME DAY. Pass 56's hazard fixture
# gives its three titles one due date, so `sig_deadline`'s `min` hands the
# hero the FIRST of them — `[urgent] ship it`, the one rich escapes CORRECTLY.
# Measured that way the hero's site reads clean while the queue beside it eats
# text, which is a law that cannot fail. The upper-cased title is the hazard
# rich passes through, so it is made the nearest deadline and the hero is
# under test at all.
#
# WHAT IS NOT ASSERTED HERE, said rather than implied: seven of the ten
# languages do not compose the detail into the hero panel at 118x34 (their
# row budget spends it elsewhere), so the hero leg is a real test on three and
# a regression guard on seven — and the vacuity guard below counts them, so a
# future layout change that quietly drops the last one goes red here rather
# than turning this into decoration. The prototype's own two sites
# (`widget_slice/app.py:1404, 800`) are swept and measured in `_p57_prove.py`
# §3 but are NOT pinned here: `verify_widget` is their home and was outside
# this increment's budget. That is a named debt in PENDING, not a silence.

HZ_T = (("[urgent] ship it", "[urgent]", "ship it"),
        ("[URGENT] rotate keys", "[URGENT]", "rotate keys"),
        ("[BLOCKED] audit keys", "[BLOCKED]", "audit keys"))


def hazard_fixture() -> Path:
    """Written here rather than read, so this suite is order-independent and
    its due dates are relative to the day it runs."""
    p = W / "prototypes" / "out" / "_fixture_ap_hazard.json"
    due = {1: 0, 2: -1, 3: 0}          # t2 overdue => the upper-cased title
    p.write_text(json.dumps({          #                is the hero's reading
        "projects": [{"id": "p1", "name": "[QA] Web", "color": "#88c0d0",
                      "status": "active"}],
        "tasks": [{"id": f"t{i}", "title": t, "project_id": "p1", "phase": ph,
                   "priority": pr,
                   "due_date": date.fromordinal(
                       date.today().toordinal() + due[i]).isoformat(),
                   "notes": "note [x] with a bracket" if i == 1 else "",
                   "urls": []}
                  for i, ((t, _, _), ph, pr) in enumerate(
                      zip(HZ_T, ("Doing", "Backlog", "Done"),
                          ("high", "low", "med")), start=1)],
        "phases": ["Backlog", "Doing", "Done"],
    }), encoding="utf-8")
    return p


def mangled(rows):
    """(leaked rows, eaten (head, row) pairs). CASE-INSENSITIVE, which is pass
    56's instrument fix and not a convenience: darkside lower-cases titles and
    blueprint upper-cases them, and a title is intact in whatever case its
    language prints it."""
    leaked = [r for r in rows if "[/]" in r]
    eaten = []
    for _, head, tail in HZ_T:
        for r in rows:
            low = r.lower()
            if tail.lower() in low and head.lower() not in low:
                eaten.append((head, r.strip()[:58]))
    return leaked, eaten


async def escape_laws():
    print("\n== THE ESCAPE SWEEP: the shipped seat calls ONE escaping")
    # (1) THE RULE IS GREP-ABLE. "this string happens to have no bracket in it"
    # is a promise every future edit has to keep at every call site; "this
    # module does not call rich's escape" is a claim one search settles. So the
    # import is gone rather than merely unused, and its absence is asserted.
    for mod in ("aperture", "hero"):
        src = (W / "taskboard" / f"{mod}.py").read_text(encoding="utf-8")
        check(f"`{mod}.py` calls rich's `escape` at ZERO sites",
              "escape(" not in src, f"{src.count('escape(')} left")
        check(f"... and `{mod}.py` does not IMPORT it either — an unused "
              f"import is a seat the next edit sits back down in",
              "from rich.markup import" not in src)

    fx = hazard_fixture()
    app = TaskboardApp(board_path=str(fx))
    async with app.run_test(size=(118, 34)) as pilot:
        await pilot.pause()
        app.notify = lambda *a, **kw: None
        await pilot.press("6")
        for _ in range(6):
            await pilot.pause()
        scr = app.screen
        check("probe self-check: the surface driven is the APERTURE",
              isinstance(scr, ApertureScreen), type(scr).__name__)
        # ONE signal enabled, so the hero is the deadline's reading and this
        # law does not change its verdict at 18:00 (`sig_workday` also turns
        # ALERT after the workday ends, and a tie would hand it the panel).
        for s in scr.engine.signals:
            s.enabled = (s.id == "deadline")
        composed = []
        for name in TH.ORDER:
            await show(pilot, scr, name)
            qrows, _ = region_rows(app, "#ap-panel")
            hrows, _ = region_rows(app, "#hero")
            for label, rows_ in (("queue", qrows), ("hero", hrows)):
                leaked, eaten = mangled(rows_)
                check(f"{name}/{label}: no row carries a literal `[/]` — a tag "
                      f"on the glass is a style that never closed",
                      not leaked, f"{leaked[:1]}")
                check(f"{name}/{label}: and no bracketed head is EATEN — a row "
                      f"showing a title's tail without its head is user text "
                      f"the markup parser deleted, which is what this seat was "
                      f"doing to `[URGENT] rotate keys`",
                      not eaten, f"{eaten[:1]}")
            # VACUITY, per language and on the surface it is claimed about: the
            # queue really carries the hazard, so "it is intact" means something
            # COUNTED ON THE TAILS, NOT ON THE HEADS (PENDING #35, cured
            # here). `mangled` is case-insensitive and HAS to be — darkside
            # lower-cases titles, blueprint upper-cases them — so `[urgent]`
            # and `[URGENT]` fold to the SAME string and a head-count of "at
            # least 2" was one hazard counted twice: it could not tell "both
            # hazard titles rendered" from "one did", which is the exact
            # question a vacuity guard exists to answer. The tails are
            # genuinely distinct, and TWO is the right number rather than
            # three: `[BLOCKED] audit keys` rides a Done task and
            # `_queue_markup` filters those out.
            qblob = "\n".join(qrows).lower()
            on_glass = [t for _, _, t in HZ_T if t.lower() in qblob]
            check(f"{name}/queue: the hazard is actually ON the glass — both "
                  f"open titles, counted on their distinct TAILS (a "
                  f"no-deletion law over text that never rendered cannot fail)",
                  len(on_glass) == 2, f"tails found: {on_glass}")
            # THE HERO LEG TAKES THE SAME READ, and it already did — it has
            # always counted tails, because a head is not what a hero prints
            # once the language has recased it. Named here so the two legs
            # are visibly one rule.
            if any(t.lower() in "\n".join(hrows).lower()
                   for _, _, t in HZ_T):
                composed.append(name)
        h = scr.engine.hero
        check("the hero under test is the DEADLINE's reading, and its detail "
              "is the user's TITLE — the reason `hero.py` escapes at all",
              h is not None and h[0].id == "deadline"
              and h[1].detail == HZ_T[1][0],
              f"{h[0].id if h else None}: {h[1].detail if h else None!r}")
        check("the hero leg is not vacuous: some languages really do compose "
              "the detail line into the panel at 118x34 (the rest are a "
              "regression guard, and this check is what would notice the last "
              "one going away)", len(composed) >= 3,
              f"{len(composed)}/10: {composed}")


async def run():
    await main()
    await legend_laws()
    await panel_laws()
    await escape_laws()
    print("\n" + ("ALL PASSED" if not fails
                  else f"{len(fails)} FAILURE(S): {fails}"))
    sys.exit(1 if fails else 0)


asyncio.run(run())
