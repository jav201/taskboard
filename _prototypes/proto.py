"""Throwaway prototype — 3 languages x 2 screens, rendered from the REAL board.

Not part of the app. Emits a (char, fg, bg) grid per screen so the HTML page
shows exactly what a terminal would draw, cell for cell.
"""
import sys, pathlib, datetime as dt
sys.path.insert(0, r"C:\Users\jjgh8\Github\taskboard")
sys.path.insert(0, r"C:\Users\jjgh8\.claude\skills\tui-design\assets")
from taskboard.models import Board, Project, Task, parse_iso
import languages as L

W, H = 104, 26
TODAY = dt.date(2026, 8, 6)          # frozen: a prototype must render the same twice

# A SYNTHETIC board, on purpose. These prototypes exist to compare visual
# languages, and a visual language is legible on invented work exactly as well
# as on real work — so the operator's actual board never enters an artifact that
# a repository could carry. The repo's own .gitignore already excludes
# board.json for this reason; rendering from it would have routed around that.
def _demo_board():
    spec = [("Atlas Platform",      "cyan",   [("Migrate the ingest workers", -3, 5),
                                               ("Retire the v1 scheduler", 2, 12),
                                               ("Backfill the audit trail", 6, 21),
                                               ("Cut the release branch", 9, 30)]),
            ("Beacon Telemetry",    "sky",    [("Sampler drops on burst", -9, 4),
                                               ("Ship the ring buffer", 1, 15),
                                               ("Dashboards for p99", 8, 26)]),
            ("Corvus Toolchain",    "violet", [("Pin the compiler", -1, 7),
                                               ("Reproducible builds", 4, 18),
                                               ("Cache the artifact store", 11, 34)]),
            ("Delta Field Kit",     "pink",   [("Bench the radio stack", 3, 9),
                                               ("Waterproof the housing", 7, 22)]),
            ("Ember Docs",          "lime",   [("Rewrite the install guide", -5, 6),
                                               ("Screenshots for the tour", 5, 19),
                                               ("Glossary pass", 13, 40)])]
    phases = ["Backlog", "Doing", "Review", "Done"]
    projects, tasks = [], []
    for i, (name, hue, work) in enumerate(spec):
        pr = Project(name=name, color=hue,
                     start_date=str(TODAY - dt.timedelta(days=20)),
                     due_date=str(TODAY + dt.timedelta(days=25 + i * 14)))
        projects.append(pr)
        for k, (title, due, span) in enumerate(work):
            tasks.append(Task(title=title, project_id=pr.id, phase=phases[k % 4],
                              start_date=str(TODAY + dt.timedelta(days=due - span // 3)),
                              due_date=str(TODAY + dt.timedelta(days=due))))
    return Board(projects, tasks, pathlib.Path("__never_written__.json"), phases=phases)


board = _demo_board()

def projects():
    out = []
    for p in board.projects:
        if p.archived: continue
        ts = [t for t in board.tasks if t.project_id == p.id and not t.archived]
        if not ts: continue
        out.append((p, ts))
    return out[:5]

def days(d):
    d = parse_iso(d) if isinstance(d, str) else d
    return (d - TODAY).days if d else None

class Grid:
    def __init__(s, w, h, bg): s.w, s.h, s.bg = w, h, bg; s.c=[[(" ",None,bg) for _ in range(w)] for _ in range(h)]
    def put(s, x, y, text, fg, bg=None):
        for i, ch in enumerate(text):
            if 0 <= x+i < s.w and 0 <= y < s.h: s.c[y][x+i] = (ch, fg, bg or s.bg)
    def row_bg(s, y, bg):
        if 0 <= y < s.h: s.c[y] = [(ch, fg, bg) for ch, fg, _ in s.c[y]]
    def dump(s): return s.c

# ---- the time gauge: the thing the current gantt does not have ---------------
FIELD_X, FIELD_W = 40, 44          # el campo TERMINA antes de la columna de cifras
SPAN = 112                                  # days across the field
def col(day):                               # day-offset -> column
    return FIELD_X + int(round((day + 14) / SPAN * FIELD_W))
WEEKS = [d for d in range(-14, SPAN-14) if (TODAY + dt.timedelta(days=d)).weekday() == 0]
MONTHS = [d for d in range(-14, SPAN-14) if (TODAY + dt.timedelta(days=d)).day == 1]

def clip(s, n): return s if len(s) <= n else s[:n-1] + "…"

# ============================================================================
# LEDGER — ruled money columns. The rules ARE the week/month gauge.
# ============================================================================
def ledger(sel_task=1):
    t = L.LANGUAGES["ledger"]; g = Grid(W, H, t["ground"])
    g.put(2, 0, "TASKBOARD", t["ink"]); g.put(12, 0, "· gantt", t["mut"])
    g.put(W-22, 0, TODAY.strftime("%d %b %Y"), t["mut"])
    # the gauge: a month name over every month rule, a light rule every week
    for d in MONTHS:
        x = col(d)
        if FIELD_X <= x < FIELD_X+FIELD_W-3:
            g.put(x, 1, (TODAY+dt.timedelta(days=d)).strftime("%b").upper(), t["ink"])
    g.put(2, 1, "PROJECT / TASK", t["mut"]); g.put(W-12, 1, "DUE", t["mut"])
    for x in range(2, W-2): g.c[2][x] = ("─", t["rule"], t["ground"])
    y, n = 3, 0
    for p, ts in projects():
        if y >= H-2: break
        for d in WEEKS:                                   # WEEK RULES = the grid
            x = col(d)
            if FIELD_X <= x < FIELD_X+FIELD_W: g.put(x, y, "│", t["dim"])
        g.put(2, y, clip(p.name.upper(), 34), t["ink"])
        s, e = days(p.start_date), days(p.due_date)
        if s is not None and e is not None:
            a, b = col(min(s, e)), col(max(s, e))
            for x in range(max(FIELD_X, a), min(FIELD_X+FIELD_W, b+1)):
                g.c[y][x] = ("━", t["accent"], t["ground"])
        pct = int(board.project_progress(p.id, False) * 100)
        g.put(W-14, y, f"{pct:3d}%", t["mut"])
        y += 1
        for t_ in ts[:4]:
            if y >= H-2: break
            if n % 5 == 4: g.row_bg(y, t["band"])            # the ruled-paper band
            bgy = t["focus"] if n == sel_task else (t["band"] if n % 5 == 4 else t["ground"])
            if n == sel_task: g.row_bg(y, bgy)
            for d in WEEKS:
                x = col(d)
                if FIELD_X <= x < FIELD_X+FIELD_W: g.c[y][x] = ("│", t["dim"], bgy)
            name = clip(t_.title, 30)
            g.put(4, y, name, t["ink"] if n == sel_task else t["calm"], bgy)
            for x in range(4+len(name), 38): g.c[y][x] = ("." if x % 2 else " ", t["dim"], bgy)
            ds, de = days(t_.start_date), days(t_.due_date)
            if ds is not None and de is not None:
                a, b = col(min(ds, de)), col(max(ds, de))
                for x in range(max(FIELD_X, a), min(FIELD_X+FIELD_W, b+1)):
                    g.c[y][x] = ("─", t["ink"] if n == sel_task else t["mut"], bgy)
            dd = days(t_.due_date)
            if dd is not None:
                lbl = f"{-dd}d over" if dd < 0 else f"{dd}d"
                g.put(W-14, y, f"{lbl:>10s}", t["alert"] if dd < 0 else t["mut"], bgy)
            if n == sel_task:                                 # selection DISCLOSES
                y += 1
                if y < H-2:
                    g.row_bg(y, t["focus"])
                    g.put(6, y, f"↳ {t_.phase} · started {t_.start_date or '—'} · due {t_.due_date or '—'}",
                          t["mut"], t["focus"])
            n += 1; y += 1
    for x in range(2, W-2): g.c[H-2][x] = ("─", t["rule"], t["ground"])
    g.put(2, H-1, "↑↓ move   enter open   e edit   ? keys", t["mut"])
    return g.dump(), t

# ============================================================================
# DARKSIDE — achromatic. Passive data is a grey STEP; the accent is interaction.
# ============================================================================
STEP = "▁▂▃▄▅▆▇"
def darkside(sel_task=1):
    t = L.LANGUAGES["darkside"]; g = Grid(W, H, t["ground"])
    g.put(2, 0, "taskboard", t["wordmark"]); g.put(13, 0, "gantt", t["ink"])
    g.put(W-24, 0, TODAY.strftime("%d %b · week %W"), t["mut"])
    for d in MONTHS:                                   # month = a labelled tick
        x = col(d)
        if FIELD_X <= x < FIELD_X+FIELD_W-3:
            g.put(x, 1, (TODAY+dt.timedelta(days=d)).strftime("%b").lower(), t["mut"])
    for d in WEEKS:                                    # week = a rail notch
        x = col(d)
        if FIELD_X <= x < FIELD_X+FIELD_W: g.put(x, 2, "╷", t["rail"])
    y, n = 3, 0
    for p, ts in projects():
        if y >= H-2: break
        g.put(2, y, clip(p.name.lower(), 34), t["ink"])
        s, e = days(p.start_date), days(p.due_date)
        if s is not None and e is not None:
            a, b = col(min(s, e)), col(max(s, e))
            for x in range(max(FIELD_X, a), min(FIELD_X+FIELD_W, b+1)):
                g.c[y][x] = ("▁", t["mut"], t["panel"])
        pct = int(board.project_progress(p.id, False) * 100)
        g.put(W-14, y, f"{pct:3d}%", t["mut"])
        y += 1
        for t_ in ts[:4]:
            if y >= H-2: break
            focused = (n == sel_task)
            bgy = t["focus"] if focused else t["ground"]
            if focused: g.row_bg(y, bgy)
            g.put(2, y, "▎" if focused else " ", t["accent"] if focused else t["ground"], bgy)
            g.put(4, y, clip(t_.title, 32), t["ink"] if focused else t["mut"], bgy)
            ds, de = days(t_.start_date), days(t_.due_date)
            if ds is not None and de is not None:
                a, b = col(min(ds, de)), col(max(ds, de))
                lvl = STEP[min(len(STEP)-1, max(0, (b-a)//2))]   # LEVEL RIDES ON SHAPE
                for x in range(max(FIELD_X, a), min(FIELD_X+FIELD_W, b+1)):
                    g.c[y][x] = (lvl, t["accent"] if focused else t["mut"], bgy)
            dd = days(t_.due_date)
            if dd is not None:
                lbl = f"▲{-dd}d" if dd < 0 else f"{dd}d"
                g.put(W-14, y, f"{lbl:>10s}", t["alert"] if dd < 0 else t["mut"], bgy)
            if focused:
                y += 1
                if y < H-2:
                    g.row_bg(y, bgy)
                    g.put(6, y, f"{t_.phase.lower()} · {t_.start_date or '—'} → {t_.due_date or '—'}", t["mut"], bgy)
                    g.put(W-30, y, "enter open   e edit", t["accent"], bgy)
            n += 1; y += 1
    g.put(2, H-1, "↑↓ move   enter open   e edit   ? keys", t["mut"])
    return g.dump(), t

# ============================================================================
# NAUGHT — quantity is DISCRETE LIT DOTS. You can count the weeks.
# ============================================================================
def naught(sel_task=1):
    t = L.LANGUAGES["naught"]; g = Grid(W, H, t["ground"])
    g.put(2, 0, "NAUGHT · GANTT", t["ink"])
    g.put(W-20, 0, TODAY.strftime("%d %b %Y"), t["mut"])
    for d in MONTHS:
        x = col(d)
        if FIELD_X <= x < FIELD_X+FIELD_W-3:
            g.put(x, 1, (TODAY+dt.timedelta(days=d)).strftime("%b").upper(), t["ink"])
    y, n = 3, 0
    for p, ts in projects():
        if y >= H-2: break
        g.put(2, y, clip(p.name.upper(), 34), t["ink"])
        s, e = days(p.start_date), days(p.due_date)
        if s is not None and e is not None:
            for d in WEEKS:                       # ONE DOT PER WEEK -> countable
                if min(s,e) <= d <= max(s,e):
                    x = col(d)
                    if FIELD_X <= x < FIELD_X+FIELD_W: g.c[y][x] = ("●", t["ink"], t["ground"])
        y += 1
        for t_ in ts[:4]:
            if y >= H-2: break
            focused = (n == sel_task)
            bgy = t["focus"] if focused else t["ground"]
            if focused: g.row_bg(y, bgy)
            g.put(4, y, clip(t_.title, 32), t["ink"] if focused else t["mut"], bgy)
            ds, de = days(t_.start_date), days(t_.due_date)
            if ds is not None and de is not None:
                for d in WEEKS:
                    if min(ds,de) <= d <= max(ds,de):
                        x = col(d)
                        if FIELD_X <= x < FIELD_X+FIELD_W:
                            g.c[y][x] = ("○" if not focused else "●", t["mut"] if not focused else t["ink"], bgy)
            dd = days(t_.due_date)
            if dd is not None:
                lbl = f"{-dd}d!" if dd < 0 else f"{dd}d"
                g.put(W-14, y, f"{lbl:>10s}", t["alert"] if dd < 0 else t["mut"], bgy)
            if focused:
                y += 1
                if y < H-2:
                    g.row_bg(y, bgy)
                    wk = 0
                    if ds is not None and de is not None:
                        wk = sum(1 for d in WEEKS if min(ds,de) <= d <= max(ds,de))
                    g.put(6, y, f"{wk} week{'s' if wk!=1 else ''} · {t_.phase} · due {t_.due_date or '—'}", t["mut"], bgy)
            n += 1; y += 1
    g.put(2, H-1, "↑↓ move   enter open   e edit   ? keys", t["mut"])
    return g.dump(), t

# ============================================================================
# LANES, compacted: one row per project, and the SELECTION discloses.
# ============================================================================
SPARK = "▁▂▃▄▅▆▇█"
DOTS  = "⣀⣄⣤⣦⣶⣷⣿"
def lanes(lang, sel_task=2):
    t = L.LANGUAGES[lang]; g = Grid(W, H, t["ground"])
    lower = (lang == "darkside")
    title = "taskboard" if lower else "TASKBOARD"
    g.put(2, 0, title, t["wordmark"] if lang == "darkside" else t["ink"])
    opn = sum(1 for x in board.tasks if not x.archived and not board.is_done(x))
    due = sum(1 for x in board.tasks if not x.archived and (days(x.due_date) or 99) <= 7)
    g.put(W-26, 0, f"{opn} open · {due} due this week", t["mut"])
    y, n = 2, 0
    for p, ts in projects():
        if y >= H-2: break
        # ---- ONE row per project: name · compact wave · figures --------------
        name = clip(p.name.lower() if lower else p.name.upper(), 22)
        g.put(2, y, name, t["ink"])
        prof = []
        for wk in range(24):                      # 24 weeks of pressure, one cell each
            lo, hi = wk*7-14, wk*7-7
            prof.append(sum(1 for x in ts if (days(x.due_date) or 999) >= lo
                            and (days(x.due_date) or -999) < hi))
        peak = max(prof) or 1
        ramp = DOTS if lang == "naught" else SPARK
        for i, v in enumerate(prof):
            x = 26 + i
            if x < W-24:
                ch = ramp[min(len(ramp)-1, int(v/peak*(len(ramp)-1)))] if v else "·"
                # NAUGHT: "red only for alarm" -- pressure is not an alarm, so it
                # rides ink. Using the accent here broke the language's own law.
                lit = t["ink"] if lang in ("naught", "darkside") else t["accent"]
                g.c[y][x] = (ch, lit if v else t["dim"], t["ground"])
        nopen = sum(1 for x in ts if not board.is_done(x))
        worst = min((days(x.due_date) for x in ts if days(x.due_date) is not None), default=None)
        g.put(W-22, y, f"{nopen:2d} open", t["mut"])
        if worst is not None:
            g.put(W-12, y, f"{'▲' if worst<0 else ''}{abs(worst)}d{' over' if worst<0 else ''}"[:10].rjust(10),
                  t["alert"] if worst < 0 else t["mut"])
        y += 1
        # ---- its tasks, plain text rows; the focused one opens ---------------
        for t_ in ts[:3]:
            if y >= H-2: break
            focused = (n == sel_task)
            bgy = t["focus"] if focused else t["ground"]
            if focused: g.row_bg(y, bgy)
            g.put(3, y, "▎" if focused else " ", t["accent"] if focused else t["ground"], bgy)
            g.put(5, y, clip(t_.title, 48), t["ink"] if focused else t["mut"], bgy)
            dd = days(t_.due_date)
            if dd is not None:
                lbl = f"▲{-dd}d" if dd < 0 else ("today" if dd == 0 else f"{dd}d")
                g.put(W-12, y, lbl.rjust(10), t["alert"] if dd < 0 else t["mut"], bgy)
            if focused:
                y += 1
                if y < H-2:
                    g.row_bg(y, bgy)
                    g.put(7, y, f"{t_.phase} · {t_.start_date or '—'} → {t_.due_date or '—'}", t["mut"], bgy)
                    g.put(W-32, y, "enter open   e edit   x archive", t["accent"], bgy)
            n += 1; y += 1
    g.put(2, H-1, "1 lanes  2 agenda  3 gantt  4 kanban   ↑↓ move   ? keys", t["mut"])
    return g.dump(), t

# ============================================================================
# HÍBRIDO — la estructura reglada de Ledger + la discreción de Darkside,
# en la PALETA REAL de taskboard.
# ============================================================================
from taskboard.views import HEX
TB = dict(HEX)
TB.update(ground="#0d1117", band="#111823", focus="#16202c", rule="#334154",
          label="Taskboard", note="paleta actual · guías de Ledger · discreción de Darkside")
HUES = ["cyan", "sky", "violet", "pink", "lime", "blue", "indigo", "fuchsia"]

def hybrid(sel_task=1, screen="gantt"):
    t = TB; g = Grid(W, H, t["ground"])
    if screen == "gantt":
        g.put(2, 0, "◆ TASKBOARD", t["accent"]); g.put(14, 0, "· gantt", t["mut"])
        g.put(W-24, 0, TODAY.strftime("%d %b · week %W"), t["mut"])
        for d in MONTHS:                                   # el mes, rotulado
            x = col(d)
            if FIELD_X <= x < FIELD_X+FIELD_W-3:
                g.put(x, 1, (TODAY+dt.timedelta(days=d)).strftime("%b").upper(), t["hd"])
        g.put(2, 1, "PROJECT / TASK", t["dim"]); g.put(W-12, 1, "DUE", t["dim"])
        for x in range(2, W-2): g.c[2][x] = ("─", t["frame"], t["ground"])
        y, n, hi = 3, 0, 0
        for p, ts in projects():
            if y >= H-2: break
            hue = HUES[hi % len(HUES)]; hi += 1
            for d in WEEKS:                                # LA GUÍA DE SEMANA
                x = col(d)
                if FIELD_X <= x < FIELD_X+FIELD_W: g.put(x, y, "│", t["rule"])
            g.put(2, y, clip(p.name.upper(), 34), t[hue])
            s, e = days(p.start_date), days(p.due_date)
            if s is not None and e is not None:
                a, b = col(min(s, e)), col(max(s, e))
                for x in range(max(FIELD_X, a), min(FIELD_X+FIELD_W, b+1)):
                    g.c[y][x] = ("━", t[hue], t["ground"])   # identidad = hue, peso bajo
            g.put(W-16, y, f"{int(board.project_progress(p.id, False)*100):3d}%", t["mut"])
            y += 1
            for t_ in ts[:4]:
                if y >= H-2: break
                foc = (n == sel_task)
                bgy = t["focus"] if foc else (t["band"] if n % 5 == 4 else t["ground"])
                g.row_bg(y, bgy)
                for d in WEEKS:
                    x = col(d)
                    if FIELD_X <= x < FIELD_X+FIELD_W: g.c[y][x] = ("│", t["rule"], bgy)
                g.put(2, y, "▎" if foc else " ", t["accent"] if foc else bgy, bgy)
                name = clip(t_.title, 30)
                g.put(4, y, name, t["ink"] if foc else t["mut"], bgy)
                for x in range(4+len(name)+1, FIELD_X-2):     # guías de puntos
                    g.c[y][x] = ("·" if x % 2 else " ", t["dim"], bgy)
                ds, de = days(t_.start_date), days(t_.due_date)
                if ds is not None and de is not None:
                    a, b = col(min(ds, de)), col(max(ds, de))
                    for x in range(max(FIELD_X, a), min(FIELD_X+FIELD_W, b+1)):
                        # DISCRECIÓN: la tarea pasiva es un trazo fino y apagado
                        g.c[y][x] = ("─", t["ink"] if foc else t["dim"], bgy)
                dd = days(t_.due_date)
                if dd is not None:
                    lbl = f"▲{-dd}d" if dd < 0 else ("today" if dd == 0 else f"{dd}d")
                    g.put(W-12, y, lbl.rjust(10), t["over"] if dd < 0 else t["mut"], bgy)
                if foc:                                       # la selección DESPLIEGA
                    y += 1
                    if y < H-2:
                        g.row_bg(y, bgy)
                        g.put(6, y, f"{t_.phase} · {t_.start_date or '—'} → {t_.due_date or '—'}", t["mut"], bgy)
                        g.put(W-34, y, "enter open   e edit   x archive", t["accent"], bgy)
                n += 1; y += 1
        for x in range(2, W-2): g.c[H-2][x] = ("─", t["frame"], t["ground"])
        g.put(2, H-1, "↑↓ move   enter open   e edit   ? keys", t["dim"])
        return g.dump(), t
    # ---- lanes ------------------------------------------------------------
    g.put(2, 0, "◆ TASKBOARD", t["accent"])
    opn = sum(1 for x in board.tasks if not x.archived and not board.is_done(x))
    g.put(W-26, 0, f"{opn} open · 4 due this week", t["mut"])
    for x in range(2, W-2): g.c[1][x] = ("─", t["frame"], t["ground"])
    y, n, hi = 2, 0, 0
    for p, ts in projects():
        if y >= H-2: break
        hue = HUES[hi % len(HUES)]; hi += 1
        g.put(2, y, clip(p.name.upper(), 22), t[hue])
        prof = []
        for wk in range(24):
            lo, hi2 = wk*7-14, wk*7-7
            prof.append(sum(1 for x in ts if (days(x.due_date) or 999) >= lo
                            and (days(x.due_date) or -999) < hi2))
        peak = max(prof) or 1
        for i, v in enumerate(prof):
            x = 26 + i
            if x < W-26:
                g.c[y][x] = ((SPARK[min(7, int(v/peak*7))] if v else "·"),
                             t[hue] if v else t["rule"], t["ground"])
        nopen = sum(1 for x in ts if not board.is_done(x))
        worst = min((days(x.due_date) for x in ts if days(x.due_date) is not None), default=None)
        g.put(W-24, y, f"{nopen:2d} open", t["mut"])
        if worst is not None:
            g.put(W-12, y, (f"▲{-worst}d" if worst < 0 else f"{worst}d").rjust(10),
                  t["over"] if worst < 0 else t["mut"])
        y += 1
        for t_ in ts[:3]:
            if y >= H-2: break
            foc = (n == sel_task)
            bgy = t["focus"] if foc else t["ground"]
            g.row_bg(y, bgy)
            g.put(3, y, "▎" if foc else " ", t["accent"] if foc else bgy, bgy)
            g.put(5, y, clip(t_.title, 46), t["ink"] if foc else t["mut"], bgy)
            for x in range(5+min(len(t_.title), 46)+1, W-14):
                g.c[y][x] = ("·" if x % 2 else " ", t["dim"], bgy)
            dd = days(t_.due_date)
            if dd is not None:
                lbl = f"▲{-dd}d" if dd < 0 else ("today" if dd == 0 else f"{dd}d")
                g.put(W-12, y, lbl.rjust(10), t["over"] if dd < 0 else t["mut"], bgy)
            if foc:
                y += 1
                if y < H-2:
                    g.row_bg(y, bgy)
                    g.put(7, y, f"{t_.phase} · {t_.start_date or '—'} → {t_.due_date or '—'}", t["mut"], bgy)
                    g.put(W-34, y, "enter open   e edit   x archive", t["accent"], bgy)
            n += 1; y += 1
    g.put(2, H-1, "1 lanes  2 agenda  3 gantt  4 kanban   ↑↓ move   ? keys", t["dim"])
    return g.dump(), t

# ============================================================================
# A / C / D — tres mecanismos para la fila de proyecto, misma paleta y datos.
# ============================================================================
def _cumulative(ts, p, cells=26):
    """LA SEMÁNTICA REAL de wave.load_curve: cuántas tareas vencen EN O ANTES
    del día x, normalizado al conjunto TOTAL del proyecto (no a las abiertas),
    y cortado en la fecha de vencimiento del proyecto."""
    total = max(1, len(ts))
    edge = days(p.due_date)
    span_lo, span_hi = -14, 98
    out = []
    for i in range(cells):
        d = span_lo + (span_hi - span_lo) * i / (cells - 1)
        if edge is not None and d > edge:
            out.append(None)                      # el banco se detiene: no miente
            continue
        n = sum(1 for x in ts if (days(x.due_date) is not None and days(x.due_date) <= d))
        out.append(n / total)
    return out

def mech_rows(mech):
    """Devuelve solo las filas de proyecto, para comparar mecanismos."""
    t = TB; g = Grid(W, 13, t["ground"])
    titles = {"A": "A · curva acumulada, con extremos rotulados",
              "C": "C · medidor de avance, discreto",
              "D": "D · las tres cifras, en texto"}
    g.put(2, 0, titles[mech], t["hd"])
    y, hi = 2, 0
    for p, ts in projects():
        if y >= 12: break
        hue = HUES[hi % len(HUES)]; hi += 1
        # el nombre cede 3 celdas para que el rotulo del eje no lo invada
        g.put(2, y, clip(p.name.upper(), 19), t[hue])
        x0 = 26
        if mech == "A":
            g.put(22, y, "hoy", t["dim"])
            for i, v in enumerate(_cumulative(ts, p)):
                x = x0 + i
                if v is None: g.c[y][x] = ("╵", t["rule"], t["ground"])   # el corte
                else:
                    g.c[y][x] = (SPARK[min(7, int(v*7))] if v > 0 else "·",
                                 t[hue] if v > 0 else t["rule"], t["ground"])
            g.put(x0+27, y, "due", t["dim"])
        elif mech == "C":
            done = sum(1 for x in ts if board.is_done(x)); tot = len(ts)
            fill = int(round(12 * done / max(1, tot)))
            g.put(x0, y, "█"*fill, t[hue]); g.put(x0+fill, y, "░"*(12-fill), t["rule"])
            g.put(x0+14, y, f"{done}/{tot}", t["mut"])
        else:
            nopen = sum(1 for x in ts if not board.is_done(x))
            late = sum(1 for x in ts if (days(x.due_date) or 99) < 0 and not board.is_done(x))
            nxt = min((days(x.due_date) for x in ts
                       if days(x.due_date) is not None and days(x.due_date) >= 0
                       and not board.is_done(x)), default=None)
            g.put(x0, y, f"{nopen:2d} open", t["mut"])
            if late: g.put(x0+9, y, f"▲{late} late", t["over"])
            else:    g.put(x0+9, y, "on time", t["dim"])
            g.put(x0+19, y, f"next {nxt}d" if nxt is not None else "no date",
                  t["mut"] if nxt is None or nxt > 3 else t["soon"])
        y += 1
    return g.dump(), t
