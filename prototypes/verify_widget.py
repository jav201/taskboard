"""Drive + render + budget check for the widget slice (VERIFY.md discipline).
Checks the things the last verify script MISSED: exact widths at several sizes,
focus actually landing, and rendered-vs-nav coherence."""
import asyncio, json, sys, statistics, time
from datetime import date
from pathlib import Path

W = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(W)); sys.path.insert(0, str(W / "prototypes" / "widget_slice"))
from app import TaskboardWidget            # noqa: E402
from taskboard import themes as TH         # noqa: E402
from textual.geometry import Region        # noqa: E402

fails = []
def check(name, cond, detail=""):
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}{'  ' + detail if detail else ''}")
    if not cond: fails.append(name)

async def main():
    print("== DRIVE: size classes, focus, states")
    for size, expect in ((40, "glance"), (60, "widget"), (110, "board")):
        app = TaskboardWidget()
        async with app.run_test(size=(size, 26)) as pilot:
            await pilot.pause()
            check(f"w={size:<4} -> size class {expect}",
                  app.size_class == expect, f"got {app.size_class}")
            check(f"w={size:<4} screen carries sz-{expect} class",
                  app.screen.has_class(f"sz-{expect}"))
            # focus must actually land (the can_focus trap)
            await pilot.press("tab")
            await pilot.pause()
            check(f"w={size:<4} TAB focuses something",
                  app.focused is not None, f"focused={app.focused!r}")
            # hero must have rendered real content
            # The hero must be DATA-COUPLED, and the check must not assume a
            # glyph model: each language now draws through its own pixel base
            # (braille, quadrant, shade...), so counting a specific block char
            # only worked for block-based themes. Assert instead that the drawn
            # mark CHANGES when the underlying value changes.
            from textual.geometry import Region as _R
            hero = app.query_one("#hero")

            def hero_ink():
                strips = hero.render_lines(_R(0, 0, hero.size.width, hero.size.height))
                return "".join(s.text for s in strips)

            before = hero_ink()
            val = app.engine.hero[1].value
            check(f"w={size:<4} hero renders a drawn mark",
                  sum(c not in " ░" for c in before) > 10,
                  f"value={val!r}")
            app.focused_task = None
            app.engine.by_id("deadline").last.value = "88"
            app.redraw()
            check(f"w={size:<4} hero changes when the value changes",
                  hero_ink() != before)
            # the BOARD surface (#queue was retired when the real kanban landed)
            kb = app.query_one("#kb")
            check(f"w={size:<4} board surface visible only in board class",
                  kb.display == (expect == "board"), f"display={kb.display}")

    print("\n== DRIVE: engine, config screen, empty state")
    app = TaskboardWidget()
    async with app.run_test(size=(70, 26)) as pilot:
        await pilot.pause()
        eng = app.engine
        check("all signals produced a reading",
              all(s.last is not None for s in eng.signals),
              f"{sum(s.last is not None for s in eng.signals)}/{len(eng.signals)}")
        check("fast and slow live in separate groups",
              {s.group for s in eng.signals} == {"fast", "slow"})
        await pilot.press("c")
        await pilot.pause()
        check("`c` opens the config screen",
              type(app.screen).__name__ == "ConfigScreen", type(app.screen).__name__)
        await pilot.press("space")          # disable the selected signal
        await pilot.pause()
        check("space toggles a signal off", not eng.signals[0].enabled)
        await pilot.press("escape"); await pilot.pause()
        # turn everything off -> the empty state must appear
        for s in eng.signals: s.enabled = False
        app.redraw(); await pilot.pause()
        hero = app.query_one("#hero")
        txt = "\n".join(s.text for s in hero.render_lines(
            Region(0, 0, hero.size.width, hero.size.height)))
        check("empty state names the key that fixes it", "c" in txt and "No signals" in txt,
              repr(txt.strip()[:60]))

    print("\n== BUDGET")
    app = TaskboardWidget()
    async with app.run_test(size=(110, 26)) as pilot:
        await pilot.pause()
        s = []
        for _ in range(30):
            t0 = time.perf_counter(); app.redraw(); s.append(time.perf_counter()-t0)
        med = statistics.median(s) * 1e6
        frame = 1e6/60
        print(f"  full redraw median {med:.0f} us = {med/frame*100:.2f}% of a 60fps frame")
        check("redraw within budget (H>=5)", med < frame/5, f"{med:.0f} vs {frame/5:.0f}")


# ---- THE ESCAPE SWEEP AT THE PROTOTYPE'S SEATS (fifty-eighth pass) --------
# Item #33. Pass 56 swept `language.py`, pass 57 swept the two SHIPPED design
# surfaces (`aperture.py:386`, `hero.py:250`) and pinned them in
# `verify_aperture`. The prototype's own two sites were swapped to `LG.mark`
# in the same increment and left with NO LAW — a measurement, not a guard.
# This section is their home.
#
# THE DEFECT BEING GUARDED, in one line: rich's `escape` only escapes a `[`
# that looks like the start of a TAG (`[` then `[a-z#/@]`), so `[URGENT]` and
# `[ ` go through untouched — and Textual, whose tokenizer is what
# `Static.update` actually parses, reads them as tags and SWALLOWS the text
# inside. No error, no leak, just the user's words gone.
#
# THE TWO SEATS:
#   `app.py:1404`  `_queue_markup` — the queue row's title, `t.title`, user
#                  text. Composed ONLY at the `widget` size class
#                  (app.py:1308), which is why `verify_language`'s hazard
#                  leg, driven at 118 cells, has never touched it.
#   `app.py:799`   `ConfigScreen.redraw` — the hint row. NOT user text, and
#                  it is a hazard anyway: two of this screen's bindings carry
#                  `key_display="["` and `"]"`, so the row it derives reads
#                  `[ threshold - · ] threshold +` and CONTAINS ITS OWN
#                  BRACKET SPAN. `[ ` is the worst case in the whole app —
#                  rich never escapes it — so this site needs no fixture: the
#                  hazard is the row.
#
# WHY 60x44 AND NOT 60x30, said in full because pass 57 got this wrong and
# did not notice. `#queue` sits low — measured at y=23..29 depending on the
# language's tile and calendar heights — and it is 10 to 12 rows tall. At
# 60x30 EVERY language's queue runs off the bottom: the compositor renders 1
# to 7 of its rows and the hazard, which lives further down the list, is on
# none of them. Measured at 60x30 with this fixture, all ten report
# `heads=[]` — an empty, clean, defect-free surface that was never drawn.
# Pass 57's PRE dump (`_p57_prove.py` §3, `_p57_pre.txt`) was taken at
# exactly that size and reported `heads_on_glass=[]` for all ten, so the
# prototype queue's "before" was never actually measured; `_p58_mut.py` is
# where it finally is. The vacuity guards below are that mistake turned into
# a check: every surface must prove it is ON the glass — all of its region's
# rows composited — before anything is asserted about its content.

HZ_T = (("[urgent] ship it", "[urgent]", "ship it"),
        ("[URGENT] rotate keys", "[URGENT]", "rotate keys"),
        ("[BLOCKED] audit keys", "[BLOCKED]", "audit keys"))


def hazard_fixture() -> Path:
    """Written here rather than read, so this suite is order-independent and
    its due dates are relative to the day it runs."""
    p = W / "prototypes" / "out" / "_fixture_wd_hazard.json"
    due = {1: 0, 2: -1, 3: 0}
    p.write_text(json.dumps({
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


def screen_rows(app):
    return ["".join(s.text for s in strip)
            for strip in app.screen._compositor.render_strips()]


def region_rows(app, wid):
    """(rows actually on the glass, the widget's region). The two are compared
    by the caller: a short list against a tall region is a surface hanging off
    the screen, which is the y=29 trap."""
    r = app.screen.query_one(wid).region
    rows = screen_rows(app)
    return [rows[y][r.x:r.x + r.width]
            for y in range(r.y, min(r.y + r.height, len(rows)))], r


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
    print("\n== THE ESCAPE SWEEP: the prototype calls ONE escaping")
    # (1) THE RULE IS GREP-ABLE. "this string happens to have no bracket in
    # it" is a promise every future edit has to keep at every call site; "this
    # module does not call rich's escape" is a claim one search settles.
    src = (W / "prototypes" / "widget_slice" / "app.py").read_text(
        encoding="utf-8")
    check("`widget_slice/app.py` calls rich's `escape` at ZERO sites",
          "escape(" not in src, f"{src.count('escape(')} left")
    check("... and it does not IMPORT it either — an unused import is a seat "
          "the next edit sits back down in",
          "from rich.markup import" not in src
          and "import rich.markup" not in src)

    fx = hazard_fixture()
    for name in TH.ORDER:
        # a fresh app per language: `set_theme` reparses the stylesheet, and
        # the queue's row count is the KIT's, so re-driving one app would
        # measure a layout mid-swap.
        app = TaskboardWidget(board_path=str(fx))
        async with app.run_test(size=(60, 44)) as pilot:
            await pilot.pause()
            app.notify = lambda *a, **kw: None
            app.set_theme(name)
            for _ in range(4):
                await pilot.pause()

            if name == TH.ORDER[0]:
                check("probe self-check: 60x44 is the WIDGET size class, the "
                      "only class that composes `#queue` (app.py:1308)",
                      app.size_class == "widget", app.size_class)

            qrows, qreg = region_rows(app, "#queue")
            # VACUITY A — the y=29 trap. Assert the surface is on the glass
            # BEFORE asserting anything about what is written on it.
            check(f"{name}/queue: the surface is ON the glass — all "
                  f"{qreg.height} of its rows composited, not hanging off the "
                  f"bottom the way it does at 60x30",
                  len(qrows) == qreg.height and qreg.height > 1,
                  f"{len(qrows)}/{qreg.height} rows at y={qreg.y}")
            # VACUITY B — and the hazard really reached it. Counted on the
            # TAILS, not the heads, and that is a correction rather than a
            # preference: `mangled` is case-insensitive (it has to be —
            # darkside lower-cases titles, blueprint upper-cases them), so
            # `[urgent]` and `[URGENT]` fold to the SAME string and a
            # head-count of "at least 2" is one hazard counted twice. It
            # cannot distinguish "both titles rendered" from "one did". The
            # tails are genuinely distinct, and two is the right number: three
            # titles go in, `[BLOCKED] audit keys` rides a Done task and
            # `_queue_markup` filters those out.
            qblob = "\n".join(qrows).lower()
            tails = [t for _, _, t in HZ_T if t.lower() in qblob]
            check(f"{name}/queue: the hazard rows really rendered — both open "
                  f"titles are on the glass (a no-deletion law over text that "
                  f"never drew cannot fail)",
                  len(tails) == 2, f"tails found: {tails}")
            leaked, eaten = mangled(qrows)
            check(f"{name}/queue: no row carries a literal `[/]` — a tag on "
                  f"the glass is a style that never closed",
                  not leaked, f"{leaked[:1]}")
            check(f"{name}/queue: and no bracketed head is EATEN — a row "
                  f"showing a title's tail without its head is user text the "
                  f"markup parser deleted", not eaten, f"{eaten[:1]}")

            await pilot.press("c")
            for _ in range(4):
                await pilot.pause()
            crows, creg = region_rows(app, "#cfg-body")
            cblob = "\n".join(crows)
            # VACUITY, per surface again: `#cfg-body` lives inside a
            # VerticalScroll, so "the hint row is intact" is only a claim if
            # the hint row is on screen at all. `esc/q back` sits BEFORE the
            # bracket span, so it survives the defect and is an independent
            # witness that the row composed.
            check(f"{name}/cfg: the hint row is ON the glass — {creg.height} "
                  f"rows composited and the row itself visible, not scrolled "
                  f"out of the box",
                  len(crows) == creg.height and "esc/q back" in cblob,
                  f"{len(crows)}/{creg.height}, esc/q "
                  f"{'found' if 'esc/q back' in cblob else 'MISSING'}")
            check(f"{name}/cfg: no row carries a literal `[/]`",
                  "[/]" not in cblob)
            # THE NO-DELETION LEG, and it is a presence law rather than
            # `mangled` for a measured reason: what Textual eats here is the
            # span from `[` to the first `]`, which takes the LABEL with it.
            # `threshold -` gone is the whole signature, so `mangled`'s
            # tail-without-head pattern would find nothing to report.
            check(f"{name}/cfg: the bracketed key displays survive with their "
                  f"labels — `[ threshold -` and `] threshold` are what the "
                  f"markup parser eats when this row is not marked",
                  "[ threshold -" in cblob and "] threshold" in cblob,
                  f"open={'[ threshold -' in cblob} "
                  f"close={'] threshold' in cblob}")


async def run():
    await main()
    await escape_laws()
    print("\n" + ("ALL PASSED" if not fails else f"{len(fails)} FAILURE(S): {fails}"))
    sys.exit(1 if fails else 0)

asyncio.run(run())
