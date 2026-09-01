"""THE APERTURE — the widget posture, as a real view of the real app.

HANDOFF.md §4 Increment 2, ADD-don't-replace: `views.py` and its tests are
untouched. The aperture is a pushed Screen behind the `6` key: the ambient
face of the board (first 10 s: is anything urgent? once focused: what's
next?), rendered entirely through the active LANGUAGE's structure kit
(taskboard/language.py — 9 languages, `t` cycles them here too).

The number keys 1-5 EXIT INTO that view: the aperture is a launcher, the
full-screen views are what you operate. That is the widget thesis (the
aperture is small; what stands behind it is not) landing in the product.

Scope: hero + meter + signal tiles + due-calendar + up-next queue,
size-classed by width (glance < 46 shows the hero alone). The FULL language
applies: kit markup AND the kit's surface/composition TCSS, injected per
language with `Screen` rewritten to `ApertureScreen` so the rules can only
land here (naught's widget grid puts the meter BESIDE the hero; darkside
gets its centred 46-col column). Every region builds its rows from its OWN
width — the screen's width wrapped a 92-cell hero inside darkside's column
into fragments (the wrapped-frame bug; caught by looking at the render).
"""
from __future__ import annotations

from datetime import datetime, timedelta

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Static

from taskboard import hero as HERO
from taskboard import language as LG
from taskboard import themes as TH
from taskboard.app import binding_map
from taskboard.engine import ALERT, CALM, NOTICE, WARN, Engine
from taskboard.models import parse_iso

# a numbered family is the one place a group label can honestly stand in for
# five words — and the only reason the legend fits when the width runs out
VIEWS = Binding.Group("views")


class ApertureScreen(Screen):
    # This screen composes no Footer (a docked Textual Footer would wear the
    # app's palette inside a surface the LANGUAGE owns, and darkside's centred
    # 46-column composition would squeeze it). Its legend is `#ap-foot`,
    # DERIVED from these bindings — see `_legend`.
    BINDINGS = [
        # the aperture is a LAUNCHER: a number key exits INTO that view
        Binding("1", "jump('swimlanes')", "Lanes", group=VIEWS),
        Binding("2", "jump('columns')", "Cols", group=VIEWS),
        Binding("3", "jump('agenda')", "Agenda", group=VIEWS),
        Binding("4", "jump('gantt')", "Gantt", group=VIEWS),
        Binding("5", "jump('kanban')", "Kanban", group=VIEWS),
        Binding("7", "jump('flow')", "Flow", group=VIEWS),
        Binding("8", "jump('standup')", "Standup", group=VIEWS),
        Binding("9", "jump('people')", "People", group=VIEWS),
        Binding("t", "cycle_language", "Language"),
        Binding("r", "refresh_now", "Refresh"),
        # `q` closes the surface in front of you. It used to QUIT THE APP from
        # here — a working, unindicated key that ended the session. Quit now
        # lives on the board's own `q`, and ctrl+q stays the door from anywhere.
        Binding("q,escape,6", "app.pop_screen", "Back"),
    ]

    # when the width cannot afford the legend, these two survive: the way out,
    # and the way to the full map (the rest is one keypress away in `?`)
    LAST_RESORT = ("app.pop_screen", "help")

    # the ids MATCH the widget-slice prototype's on purpose: the kits'
    # surface()/composition() TCSS targets #hero/#meter/#tiles/#top/#ap,
    # and none of those ids exist in the real app's main screen — so the
    # injected per-language stylesheet lands here and nowhere else
    DEFAULT_CSS = """
    ApertureScreen { background: #000000; }
    #ap { width: 1fr; height: 1fr; padding: 1 2; }
    #top { width: 1fr; height: auto; }
    #hero { width: 1fr; height: auto; }
    #meter { width: 1fr; height: 2; margin-top: 1; }
    #tiles { width: 1fr; height: auto; margin-top: 1; }
    #ap-panel { width: 1fr; height: auto; margin-top: 1; }
    /* DOCKED, because a legend below the fold is a legend nobody has: the
       stacked panel above overflows a 34-row screen in instrument, swiss,
       darkside and blueprint (region y=45 on a 34-row screen — measured), and
       took the key row with it. Docking it also keeps it out of the languages
       that narrow #top/#tiles/#ap-panel into a centred column. */
    #ap-foot { width: 1fr; height: 1; margin-top: 1; dock: bottom; }
    """

    def __init__(self, board):
        super().__init__()
        self.board = board
        self.engine = Engine(board)
        self._tick_n = 0

    # ---- lifecycle ---------------------------------------------------------
    def compose(self) -> ComposeResult:
        with Vertical(id="ap"):
            with Vertical(id="top"):       # hero+meter: the language may lay
                yield Static("", id="hero")    # them out side by side (naught)
                yield Static("", id="meter")
            yield Static("", id="tiles")
            yield Static("", id="ap-panel")
            yield Static("", id="ap-foot")

    def on_mount(self) -> None:
        # the chosen language persists across opens, on the app
        self.set_language(getattr(self.app, "_aperture_lang", "naught"))
        self.engine.run_all()
        self.redraw()
        # layout has not run at mount: widget widths are 0 and the first
        # frame falls back to screen width — re-render once sizes exist
        self.call_after_refresh(self.redraw)
        # one slow heartbeat: the aperture is ambient, not animated — the
        # data cadences matter, the 60fps class does not (BUDGET.md)
        self.set_interval(1.0, self._tick_fast)
        self.set_interval(5.0, self._tick_slow)

    def on_resize(self, event) -> None:
        self.redraw()

    # ---- language ----------------------------------------------------------
    def set_language(self, name: str) -> None:
        if name not in TH.THEMES:
            name = "naught"
        self.lang = name
        self.kit = LG.kit(name)
        t = self.kit.t
        calm = t.get("calm", t["accent"])
        self.tone = {CALM: calm, NOTICE: calm,
                     WARN: t["warn"], ALERT: t["alert"]}
        self.app._aperture_lang = name
        self.styles.background = t["ground"]
        # the FULL language, not just markup: palette + the kit's structural
        # stylesheet (surface + composition), scoped to this screen by
        # rewriting `Screen` → `ApertureScreen` (its other selectors are ids
        # that exist only here; on pop the rules go inert)
        css = (TH.tcss(name) + "\n" + self.kit.tcss()).replace(
            "Screen", "ApertureScreen")
        self.app.stylesheet.add_source(css, read_from=("aperture", ""))
        self.app.stylesheet.reparse()
        self.app.stylesheet.update(self.app)
        # NOT scheduled here: a redraw queued after this (call_after_refresh,
        # one frame or two) fires while the new stylesheet's layout is still
        # running, and `redraw`'s wof() then measures TRANSIENT widths — tried,
        # and verify_language's solari/ledger/blueprint band laws went red on
        # the frames it produced. The 1 s tick already rebuilds at the settled
        # width; the open half of this is in PENDING (a width-change trigger).

    def action_cycle_language(self) -> None:
        i = TH.ORDER.index(self.lang)
        self.set_language(TH.ORDER[(i + 1) % len(TH.ORDER)])
        self.redraw()
        t = TH.THEMES[self.lang]
        self.notify(f"{t['label']} — {t['note']}", timeout=2.5)

    # ---- launcher ----------------------------------------------------------
    def action_jump(self, mode: str) -> None:
        self.app.pop_screen()
        self.app.action_view(mode)

    def action_refresh_now(self) -> None:
        self.engine.run_all()
        self.redraw()

    # ---- ticks -------------------------------------------------------------
    def _tick_fast(self) -> None:
        self._tick_n += 1
        self.engine.run_group("fast")
        self.redraw()

    def _tick_slow(self) -> None:
        if self.engine.run_group("slow"):
            self.redraw()

    # ---- render ------------------------------------------------------------
    def redraw(self) -> None:
        k = self.kit
        sw = self.size.width or 80
        w = max(10, sw - 4)

        # every region builds its rows from ITS OWN width, never the
        # screen's: darkside's centred 46-col column made a 92-cell hero
        # WRAP into ███ fragments (the wrapped-frame bug, again — found by
        # looking at the render, invisible in code)
        def wof(wid: str, fallback: int) -> int:
            ww = self.query_one(wid).size.width
            return max(10, ww - 1 if ww else fallback)
        glance = sw < 46
        # size classes ON THE SCREEN: the kits' composition CSS keys off
        # ApertureScreen.sz-board (naught's grid, darkside's centred column)
        cls = "glance" if glance else ("widget" if sw < 80 else "board")
        for c_ in ("glance", "widget", "board"):
            self.set_class(c_ == cls, f"sz-{c_}")
        b = self.board
        tasks = b.visible_tasks(False)
        done = sum(1 for t in tasks if b.is_done(t))

        # board MOOD feeds identity elements with a job (naught's face)
        today = datetime.now().date()
        over = any((d := parse_iso(t.due_date)) is not None and d < today
                   and not b.is_done(t) for t in tasks)
        k.mood = "alert" if over else ("busy" if done < len(tasks) else "clear")

        h = self.engine.hero
        hero_w = self.query_one("#hero", Static)
        # ROW BUDGET: at widget size the hero takes a fixed 9 rows so the
        # meter/tiles/panel below always fit; at glance it takes the screen
        max_rows = max(5, (self.size.height or 24) - 4) if glance else 9
        if h is None:
            hero_w.update(f"[{k.c['mut']}]{k.VOICE['no_signals']}[/]")
        else:
            series = None if glance else self._load_series()
            hero_w.update(HERO.draw(
                k, str(h[1].value), h[1].caption, h[1].detail,
                self.tone[h[1].severity], wof("#hero", w), max_rows,
                series=series, source=h[0].id))

        for wid in ("#meter", "#tiles", "#ap-panel"):
            self.query_one(wid).display = not glance
        if not glance:
            from taskboard.views import phase_buckets
            counts = [len(x) for x in phase_buckets(b, tasks)]
            self.query_one("#meter", Static).update(
                k.meter(done, len(tasks), counts, wof("#meter", w)))
            self.query_one("#tiles", Static).update(
                self._tiles_markup(wof("#tiles", w)))
            # the panel reads its own ROOM: queue first (the "what's next"
            # job), the calendar only when the height affords both
            n_tiles = sum(1 for s in self.engine.signals if s.enabled)
            avail = max(0, (self.size.height or 24) - (9 + 2 + n_tiles + 8))
            wp = wof("#ap-panel", w)
            if avail >= 12:
                panel = (self._calendar_markup(wp) + NL2
                         + self._queue_markup(wp, avail - 8))
            elif avail >= 3:
                panel = self._queue_markup(wp, avail - 1)
            else:
                panel = ""
            self.query_one("#ap-panel", Static).update(panel)
        self.query_one("#ap-foot", Static).update(
            self._legend(wof("#ap-foot", w)))

    def _legend(self, w: int) -> str:
        """The legend, DERIVED from the keys that actually fire here.

        The hand-written row this replaces promised four keys while 22 bindings
        were live — `q` among them, which quit the app. A derived row cannot
        drift; it also cannot lie about what `check_action` dropped.

        `#ap-foot` is one row high, so a row that does not fit is CLIPPED, not
        wrapped: it degrades in three tiers instead (words -> the numbered
        family under one label -> the two doors)."""
        rows = binding_map(self, shown=True)

        def line(items):
            return " · ".join(f"{d} {t.lower()}" for d, t, _ in items)

        out = line(rows)
        if len(out) > w:                      # tier 2: keep every key, spend
            grouped, at = [], {}              # one label on the whole family
            for disp, desc, b in rows:
                g = b.group.description if b.group else None
                if g in at:
                    i = at[g]
                    grouped[i] = (grouped[i][0] + " " + disp, g, b)
                    continue
                if g is not None:
                    at[g] = len(grouped)
                    desc = g
                grouped.append((disp, desc, b))
            rows = grouped
            out = line(rows)
        if len(out) > w:                      # tier 3: the two doors only
            out = line([r for r in rows if r[2].action in self.LAST_RESORT])
        return f"[{self.kit.c['dim']}]{out}[/]"

    def _tiles_markup(self, w: int) -> str:
        k = self.kit
        rows = []
        for s in self.engine.signals:
            if not s.enabled:
                continue
            r = s.last
            if r is None:
                rows.append(k.spinner(self._tick_n)
                            + f" [{k.c['dim']}]{s.label[:18]}[/]")
                continue
            if not r.ok:
                rows.append(f"[{k.c['alert']}]{s.label[:18]:<18} err[/]")
                continue
            tone = self.tone[r.severity]
            ic = k.icon(s.id)
            g = ""
            try:
                num = int(r.value)
            except (TypeError, ValueError):
                num = None
            if num is not None and s.threshold and w >= 40:
                g = " " + k.gauge(num, 0, max(num, s.threshold * 2), 10, tone,
                                  thr=s.threshold)
            rows.append((ic + " " if ic else "")
                        + k.tile_row(f"{r.value:>3}", s.label, tone,
                                     w - (14 if g else 0)) + g)
        return "\n".join(rows)

    def _load_series(self, weeks: int = 8) -> list[int]:
        today = datetime.now().date()
        start = today - timedelta(days=today.weekday())
        out = [0] * weeks
        for t in self.board.visible_tasks(False):
            if self.board.is_done(t):
                continue
            d = parse_iso(t.due_date)
            if d is None:
                continue
            wk = (d - start).days // 7
            if 0 <= wk < weeks:
                out[wk] += 1
        return out

    def _calendar_markup(self, w: int, weeks: int = 4) -> str:
        k = self.kit
        today = datetime.now().date()
        start = today - timedelta(days=today.weekday())
        counts: dict = {}
        for t in self.board.visible_tasks(False):
            d = parse_iso(t.due_date)
            if d is None or self.board.is_done(t):
                continue
            counts[d] = counts.get(d, 0) + 1
        rows = [f"[{k.c['mut']}]{'M  T  W  T  F  S  S':<21}[/]  "
                f"[{k.c['dim']}]due[/]"]
        for wk in range(weeks):
            cells = []
            for dy in range(7):
                d = start + timedelta(days=wk * 7 + dy)
                n = counts.get(d, 0)
                if n == 0:
                    cells.append(k.cal_cell("none"))
                elif d < today:
                    cells.append(k.cal_cell("over"))
                elif n > 1:
                    cells.append(k.cal_cell("multi"))
                else:
                    cells.append(k.cal_cell("one"))
            mark = "◀" if wk == 0 else " "
            rows.append(" ".join(cells) + f"  [{k.c['dim']}]{mark}[/]")
        series = [counts.get(start + timedelta(days=i), 0)
                  for i in range(weeks * 7)]
        hi = max(series) if series else 1
        rows.append(k.spark(series, 21, hi=hi) + f" [{k.c['dim']}]load[/]")
        return "\n".join(rows)

    def _queue_markup(self, w: int, n: int = 6) -> str:
        k = self.kit
        today = datetime.now().date()
        rows = [f"[{k.c['mut']}]UP NEXT[/]"]
        open_t = [t for t in self.board.visible_tasks(False)
                  if not self.board.is_done(t)]

        def key(t):
            d = parse_iso(t.due_date)
            return (0 if getattr(t, "blocked", False) else 1,
                    0 if d else 1, (d - today).days if d else 9999)

        # ONE MEASURE, the marker's own (kanban.row_width's law, at this seat).
        # The row used to be built as `marker + 1 + (w - 8) + 5`, which closes
        # on w only for a 2-cell marker: corgi and industrial draw `[1]` and
        # overflowed the panel by a cell at every width (measured 114-in-113 at
        # 118x34), and ledger's folio was cut to two cells to decline it.
        # `queue_marker` is MARKUP, so the width is the visible one, and the
        # widest marker in the batch sets the column for all of them — a
        # per-row budget would fit and stagger the chips.
        picked = list(enumerate(sorted(open_t, key=key)[:max(1, n)]))
        marks = [(m, HERO.vis_w(m))
                 for m in (k.queue_marker(i) for i, _ in picked)]
        mw = max((x for _, x in marks), default=0)
        tw = max(1, w - mw - QUEUE_GAP - QUEUE_CHIP)
        for (i, t), (mark, mkw) in zip(picked, marks):
            d = parse_iso(t.due_date)
            days = (d - today).days if d else None
            chip = ("--" if days is None
                    else (f"{-days}d!" if days < 0 else f"{days}d"))
            tone = k.c["alert"] if (days is not None and days < 0) else k.c["mut"]
            rows.append(f"{mark}{' ' * (mw - mkw + QUEUE_GAP)}"
                        f"[{k.c['mut']}]{LG.mark(t.title)[:tw]:<{tw}}[/]"
                        f"[{tone}]{chip:>{QUEUE_CHIP}}[/]")
        return "\n".join(rows)


NL2 = chr(10) * 2

# the queue row's fixed columns, named rather than spelled `- 8` in a format
# string: one space after the marker, five cells for the due chip
QUEUE_GAP = 1
QUEUE_CHIP = 5
