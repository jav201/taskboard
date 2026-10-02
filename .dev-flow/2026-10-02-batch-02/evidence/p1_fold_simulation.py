"""C-39 pre-execution: simulate UXV-2 + UXV-3 fold orders on the oracle board walk."""
import sys; sys.path.insert(0, '.'); sys.path.insert(0, 'tests')
from datetime import date
import kg_board
from kg_board import TODAY
from taskboard import views
from taskboard.views import parse_iso, GanttGroup

orig = views.gantt_plan
def make(order):
    def plan(board, show_archived, selected_id, today, body_rows, focus=None, recent=()):
        groups = orig(board, show_archived, None, today, 10**6, focus)  # all unfolded, raw data
        raw = [(g.project, g.open, g.rest) for g in groups]
        sel = board.task_by_id(selected_id) if selected_id else None
        sel_i = next((i for i,(p,o,r) in enumerate(raw) if sel is not None and sel in o+r), None)
        left = body_rows - len(raw); unfold=[False]*len(raw)
        if sel_i is not None: unfold[sel_i]=True; left -= len(raw[sel_i][1])
        def late(ts): return sum(1 for t in ts if (d:=parse_iso(t.due_date)) and d < today)
        def urgent(ts): return any((d:=parse_iso(t.due_date)) and d <= today for t in ts)
        def today_n(ts): return sum(1 for t in ts if parse_iso(t.due_date) == today)
        def weight(ts): return sum(1 for t in ts if (d:=parse_iso(t.due_date)) and d <= today)
        def first(ts): return min([d for t in ts if (d:=parse_iso(t.due_date))] or [date.max])
        pid = lambda i: raw[i][0].id if raw[i][0] is not None else None
        def key(i):
            ts = raw[i][1]
            rec = recent.index(pid(i)) if pid(i) in recent else None
            if order == 'base': return (0,0,-late(ts), first(ts))
            if order == 'urgent_only': return (0, not urgent(ts), -late(ts), first(ts))
            if order == 'visited_first': return (rec is None, rec if rec is not None else 0, not urgent(ts), -late(ts), first(ts))
            if order == 'iter2_prev1_today':
                prev = recent[1:2]
                return (pid(i) not in prev, -weight(ts), -today_n(ts), first(ts))
            if order == 'llr_207_1': return (rec is None, rec if rec is not None else 0, -weight(ts), first(ts))
            if order == 'urgent_first': return (not urgent(ts), rec is None, rec if rec is not None else 0, -late(ts), first(ts))
        for i in sorted((i for i in range(len(raw)) if i != sel_i), key=key):
            n=len(raw[i][1])
            if n and n<=left: unfold[i]=True; left-=n
        return [GanttGroup(p,o,r,late(o),unfold[i]) for i,(p,o,r) in enumerate(raw)]
    return plan

for order in ('base','urgent_only','visited_first','urgent_first','llr_207_1','iter2_prev1_today'):
    for (w,h) in ((80,22),(118,28)):
        b = kg_board.build()
        nav = views.nav_model('gantt', b, False, TODAY, w, h)[0]
        recent=[]; prev=None; ups=[]
        p = make(order)
        for tid in nav:
            t=b.task_by_id(tid)
            if t.project_id in recent: recent.remove(t.project_id)
            recent.insert(0, t.project_id)
            views.gantt_plan = lambda *a, **k: p(*a, recent=list(recent), **k)
            lm={}; views.render_gantt(b, False, tid, TODAY, w, h, lm)
            if prev is not None and lm[tid] < prev: ups.append((tid, prev, lm[tid]))
            prev = lm[tid]
        views.gantt_plan = orig
        g0 = p(b, False, 'tw3', TODAY, h-3, recent=['pweb'])
        print(order, (w,h), 'ups', ups, '| initial unfolded', [g.project.name.split()[0] for g in g0 if g.unfolded])
