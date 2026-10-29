"""Build variant B — the INTERACTIVE WORKSPACE HTML report.

One self-contained .html: an interactive gantt (day/week/month zoom, hover
details, click-to-open task card), filters (board/project/person/mark/status
+ search), a sortable task table, notes with ==!!++ highlights and @mentions,
and embedded JSON with Download CSV / Download JSON buttons. Vanilla JS only.

Data comes from the round's synthetic fixture; nothing is saved anywhere.
Honesty laws from taskboard/report.py carry over: counts and dates only, no
forecasts; every user-authored string is escaped server-side or rendered with
textContent client-side; every figure carries a direct label, never hue alone.
"""
from __future__ import annotations

import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "prototypes" / "html_report"))
sys.path.insert(0, str(ROOT))

import fixture  # noqa: E402
from fixture import MARKS, PEOPLE, TODAY, all_boards  # noqa: E402
from taskboard.models import days_in_phase, parse_iso  # noqa: E402
from taskboard.people import split_mentions  # noqa: E402
from taskboard.views import HEX, highlight_segments, lanes_of, sitting  # noqa: E402

OUT_DIR = ROOT / "prototypes" / "html_report" / "out"


def esc(text: object) -> str:
    return html.escape(str(text), quote=True)


def render_notes(text: str) -> str:
    """Notes as safe HTML: ==soon== / !!over!! / ++green++ highlights, @mentions
    resolved to @Name. Same tokeniser the app uses (highlight_segments)."""
    if not text:
        return ""
    lines = []
    for line in text.split("\n"):
        segs = highlight_segments(line)
        parts = []
        for seg, tone in segs:
            if "@" not in seg:
                parts.append(f'<span class="hl-{tone}">{esc(seg)}</span>')
                continue
            for piece, handle in split_mentions(seg):
                if handle is None:
                    parts.append(f'<span class="hl-{tone}">{esc(piece)}</span>')
                elif handle in PEOPLE:
                    parts.append(f'<span class="hl-{tone} mention">'
                                 f'@{esc(PEOPLE[handle].name)}</span>')
                else:
                    parts.append(f'<span class="hl-{tone}">{esc(piece)}</span>')
        lines.append("".join(parts))
    return "<br>".join(lines)


def collect() -> dict:
    boards = all_boards()
    tasks = []
    projects = []
    for bname, board in boards.items():
        lanes = lanes_of(board, True, TODAY)
        id2title = {t.id: t.title for t in board.tasks}
        for lane in lanes:
            projects.append({"board": bname, "name": lane.name,
                             "hue": HEX.get(lane.hue, HEX["mut"]),
                             "status": lane.status,
                             "momentum": sitting(lane, TODAY) or "nothing open",
                             "open": len(lane.open), "done": lane.done_n,
                             "late": len(lane.late)})
        for t in board.tasks:  # archived included on purpose
            done = board.is_done(t)
            start = parse_iso(t.start_date)
            due = parse_iso(t.due_date)
            mark = None
            if t.milestone and t.mark in MARKS:
                m = MARKS[t.mark]
                mark = {"name": m.name, "shape": m.shape,
                        "color": HEX.get(m.colour, HEX["mut"])}
            hue = HEX["mut"]
            proj = board.project_by_id(t.project_id)
            if proj is not None:
                hue = HEX.get(proj.color, HEX["mut"])
            status = "archived" if t.archived else ("done" if done else "open")
            tasks.append({
                "id": t.id, "board": bname,
                "project": proj.name if proj else "Inbox", "hue": hue,
                "title": t.title, "phase": t.phase,
                "priority": t.priority, "status": status,
                "done": done, "archived": t.archived, "blocked": t.blocked,
                "start": start.isoformat() if start else None,
                "due": due.isoformat() if due else None,
                "due_in": (due - TODAY).days if due else None,
                "age": days_in_phase(t, TODAY),
                "milestone": t.milestone, "mark": mark,
                "deps": [{"id": d, "title": id2title.get(d, d)}
                         for d in t.depends_on],
                "chain": [],  # filled below
                "urls": list(t.urls),
                "notes": t.notes or "",
                "notes_html": render_notes(t.notes),
                "mentions": sorted({PEOPLE[h].name for h in
                                    __import__("taskboard.people", fromlist=["mention_ids"])
                                    .mention_ids(t.notes) if h in PEOPLE}),
            })
    by_id = {t["id"]: t for t in tasks}
    for t in tasks:  # downstream chain, computed once for the modal card
        chain, seen, stack = [], set(), [t["id"]]
        kids = {k: [] for k in by_id}
        for k, v in by_id.items():
            for d in v["deps"]:
                kids.setdefault(d["id"], []).append(k)
        while stack:
            cur = stack.pop()
            for kid in kids.get(cur, []):
                if kid not in seen and kid != t["id"]:
                    seen.add(kid)
                    chain.append(by_id[kid]["title"])
                    stack.append(kid)
        t["chain"] = chain
    return {
        "meta": {"today": TODAY.isoformat(), "generated": TODAY.isoformat(),
                 "boards": list(boards)},
        "people": {h: {"name": p.name, "role": p.role}
                   for h, p in PEOPLE.items()},
        "marks": {mid: {"name": m.name, "shape": m.shape,
                        "color": HEX.get(m.colour, HEX["mut"])}
                  for mid, m in MARKS.items()},
        "projects": projects,
        "tasks": tasks,
    }


CSS = """
:root{color-scheme:light dark;
  --bg:#0d1117;--panel:#161b22;--line:#21262d;--ink:#e6edf3;--mut:#8b98a5;
  --accent:#2dd4bf;--over:#f43f5e;--soon:#fbbf24;--green:#4ade80;--chip:#1c2330;}
@media (prefers-color-scheme:light){
  :root{--bg:#ffffff;--panel:#f6f8fa;--line:#d0d7de;--ink:#1f2328;--mut:#59636e;--chip:#eaeef2;}
}
*{box-sizing:border-box}
body{margin:0;padding:1.5rem 1.25rem 4rem;background:var(--bg);color:var(--ink);
  font:15px/1.55 ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif}
main{max-width:76rem;margin:0 auto}
h1{font-size:1.45rem;margin:0 0 .25rem;letter-spacing:.01em}
h2{font-size:1.02rem;margin:2.2rem 0 .6rem;padding-bottom:.35rem;
  border-bottom:1px solid var(--line);font-weight:600}
.sub{color:var(--mut);margin:0 0 1.4rem;font-size:.88rem}
.tiles{display:flex;flex-wrap:wrap;gap:.7rem;margin:0 0 .4rem}
.tile{flex:1 1 7rem;background:var(--panel);border:1px solid var(--line);
  border-radius:8px;padding:.6rem .8rem;min-width:6.5rem}
.tile .n{font-size:1.5rem;font-weight:650;letter-spacing:-.01em}
.tile .k{color:var(--mut);font-size:.74rem;text-transform:uppercase;letter-spacing:.06em}
.showing{color:var(--mut);font-size:.85rem;margin:.2rem 0 0}
.panel{background:var(--panel);border:1px solid var(--line);border-radius:10px;
  padding:.9rem 1rem;margin:0 0 1rem}
.controls{display:flex;flex-wrap:wrap;gap:.9rem;align-items:flex-start}
.cgroup{display:flex;flex-wrap:wrap;gap:.35rem;align-items:center}
.cgroup .lbl{font-size:.72rem;text-transform:uppercase;letter-spacing:.06em;
  color:var(--mut);margin-right:.15rem}
button{font:inherit;color:inherit;background:var(--chip);border:1px solid var(--line);
  border-radius:999px;padding:.22rem .7rem;cursor:pointer;font-size:.85rem}
button[aria-pressed="true"]{background:var(--accent);border-color:var(--accent);
  color:#06281f;font-weight:600}
.zbtn[aria-pressed="true"]{background:var(--ink);border-color:var(--ink);color:var(--bg)}
select,input[type=search]{font:inherit;color:var(--ink);background:var(--chip);
  border:1px solid var(--line);border-radius:8px;padding:.28rem .55rem;font-size:.88rem}
input[type=search]{min-width:11rem;flex:1 1 10rem}
.dl{background:transparent;border-style:dashed}
.gantt-wrap{overflow-x:auto;border:1px solid var(--line);border-radius:10px;
  background:var(--panel)}
.gantt-wrap svg{display:block}
.tbl-wrap{overflow-x:auto;border:1px solid var(--line);border-radius:10px}
table{border-collapse:collapse;width:100%;font-size:.88rem;background:var(--panel)}
th,td{text-align:left;padding:.45rem .6rem;border-bottom:1px solid var(--line);
  vertical-align:top;white-space:nowrap}
th{background:var(--bg)}
th button{border:none;background:none;border-radius:6px;padding:.1rem .3rem;
  font-size:.74rem;text-transform:uppercase;letter-spacing:.06em;color:var(--mut);
  cursor:pointer;font-weight:600}
th button .ind{color:var(--accent)}
td .m{color:var(--mut)}
tr.rowdone td{opacity:.55}
tr.rowarch td{opacity:.42;font-style:italic}
.dot{display:inline-block;width:.6rem;height:.6rem;border-radius:2px;margin-right:.4rem}
.flag{color:var(--over);font-weight:600}
.blk{color:var(--soon);font-weight:600}
.tmark{font-weight:700}
a{color:var(--accent)}
.hl-soon{background:color-mix(in srgb,var(--soon) 22%,transparent);border-radius:3px;padding:0 .15em}
.hl-over{background:color-mix(in srgb,var(--over) 22%,transparent);border-radius:3px;padding:0 .15em}
.hl-green{background:color-mix(in srgb,var(--green) 22%,transparent);border-radius:3px;padding:0 .15em}
.mention{color:var(--accent);font-weight:600}
#tt{position:fixed;z-index:40;display:none;max-width:20rem;background:var(--bg);
  border:1px solid var(--line);border-radius:8px;padding:.55rem .7rem;
  font-size:.8rem;box-shadow:0 6px 24px rgba(0,0,0,.4);pointer-events:none}
#tt .ttt{font-weight:650}
#tt .ttm{color:var(--mut)}
#modal{position:fixed;inset:0;z-index:50;display:none;align-items:center;
  justify-content:center;background:rgba(0,0,0,.55);padding:1rem}
#modal.open{display:flex}
.card{background:var(--bg);border:1px solid var(--line);border-radius:12px;
  max-width:34rem;width:100%;max-height:88vh;overflow-y:auto;padding:1.2rem 1.3rem}
.card h3{margin:0 2.2rem .1rem 0;font-size:1.15rem}
.card .csub{color:var(--mut);font-size:.85rem;margin:0 0 .8rem}
.card dl{display:grid;grid-template-columns:8.5rem 1fr;gap:.25rem .8rem;
  margin:.6rem 0;font-size:.88rem}
.card dt{color:var(--mut);font-size:.74rem;text-transform:uppercase;
  letter-spacing:.05em;padding-top:.15rem}
.card dd{margin:0}
.card .notes{border:1px solid var(--line);border-radius:8px;padding:.6rem .75rem;
  background:var(--panel);font-size:.88rem;margin:.5rem 0 0}
#mclose{position:absolute;top:.7rem;right:.8rem;border-radius:8px}
.cardwrap{position:relative;width:100%;max-width:34rem}
footer{color:var(--mut);font-size:.82rem;margin-top:3rem;border-top:1px solid var(--line);
  padding-top:.75rem}
.glabel{fill:var(--ink);font-size:11px}
.gmeta{fill:var(--mut);font-size:11px}
.gtick{fill:var(--mut);font-size:10px}
.gline{stroke:var(--line);stroke-width:1}
.gtoday{stroke:var(--accent);stroke-width:1.5}
.gtodaylbl{fill:var(--accent);font-size:10px;font-weight:700}
.gweekend{fill:rgba(139,152,165,.07)}
@media print{
  body{background:#fff;color:#000;padding:0}
  .controls,#ganttsec,#tt,#modal,.dl,.zbtn{display:none!important}
  .tile,.tbl-wrap,table,.card{background:#fff;border-color:#bbb}
  th,td{border-color:#ccc}
  .sub,.tile .k,th button,.showing,footer{color:#444}
  tr{break-inside:avoid}
  thead{display:table-header-group}
  h2{break-after:avoid}
  .tiles{break-inside:avoid}
  a{color:#000;text-decoration:none}
}
"""

JS = r"""
const DATA = JSON.parse(document.getElementById('board-data').textContent);
const TODAY = DATA.meta.today;
const NS = 'http://www.w3.org/2000/svg';
const $ = s => document.querySelector(s);
const state = {boards:new Set(), status:new Set(), person:'all', mark:'all',
               project:'all', q:'', zoom:'fit', sortKey:'due', sortDir:1};

function pd(s){ if(!s) return null; const [y,m,d]=s.split('-').map(Number);
  return new Date(y, m-1, d); }
function dstr(dt){ return dt.getFullYear()+'-'+String(dt.getMonth()+1).padStart(2,'0')
  +'-'+String(dt.getDate()).padStart(2,'0'); }
function addD(dt,n){ const d=new Date(dt); d.setDate(d.getDate()+n); return d; }
function diffD(a,b){ return Math.round((b-a)/86400000); }
const TODAY_D = pd(TODAY);
const MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];

function overdue(t){ return t.status==='open' && t.due_in!==null && t.due_in<0; }
function statusHits(t, wanted){
  return (wanted.has('open')     && t.status==='open') ||
         (wanted.has('done')     && t.status==='done') ||
         (wanted.has('archived') && t.status==='archived') ||
         (wanted.has('blocked')  && t.blocked) ||
         (wanted.has('overdue')  && overdue(t));
}
function matches(t){
  if(state.boards.size && !state.boards.has(t.board)) return false;
  if(state.status.size && !statusHits(t, state.status)) return false;
  if(state.person!=='all' && !t.mentions.includes(state.person)) return false;
  if(state.mark==='none' && t.mark) return false;
  if(state.mark!=='all' && state.mark!=='none' &&
     (!t.mark || t.mark.name!==state.mark)) return false;
  if(state.project!=='all' && t.project!==state.project) return false;
  if(state.q){ const q=state.q.toLowerCase();
    const hay=(t.title+' '+t.board+' '+t.project+' '+(t.notes||'')+' '+t.phase).toLowerCase();
    if(!hay.includes(q)) return false; }
  return true;
}
function filtered(){ return DATA.tasks.filter(matches); }

// ---- tiles -----------------------------------------------------------------
function renderTiles(list){
  const open = list.filter(t=>t.status==='open').length;
  const done = list.filter(t=>t.status==='done').length;
  const arch = list.filter(t=>t.status==='archived').length;
  const late = list.filter(overdue).length;
  $('#tile-open').textContent = open;
  $('#tile-done').textContent = done;
  $('#tile-late').textContent = late;
  $('#tile-arch').textContent = arch;
  $('#showing').textContent =
    'Showing '+list.length+' of '+DATA.tasks.length+' tasks · generated '+
    DATA.meta.generated+' · counts and dates only, nothing here is a forecast';
}

// ---- gantt -----------------------------------------------------------------
const PPD = {day:26, week:11, month:4.5};
function rowMeta(t){
  let tag = '';
  if(t.status==='done') tag=' ✓';
  else if(t.status==='archived') tag=' · archived';
  if(t.blocked) tag += ' ⛔';
  if(overdue(t)) tag += ' '+(-t.due_in)+'d over';
  const ms = t.mark ? ' '+t.mark.shape : '';
  return t.board+' · '+t.title+ms+tag;
}
function ticks(lo, hi, zoom){
  const out = [];
  if(zoom==='month'){
    let d = new Date(lo.getFullYear(), lo.getMonth(), 1);
    while(d<=hi){ out.push({d:new Date(d), lbl:MONTHS[d.getMonth()]}); d=new Date(d.getFullYear(), d.getMonth()+1, 1); }
  } else if(zoom==='week'){
    for(let d=new Date(lo); d<=hi; d=addD(d,7))
      out.push({d:new Date(d), lbl:MONTHS[d.getMonth()]+' '+d.getDate()});
  } else {
    for(let d=new Date(lo); d<=hi; d=addD(d,1)){
      const first = d.getDate()===1;
      out.push({d:new Date(d), lbl:first ? MONTHS[d.getMonth()]+' 1' : String(d.getDate())});
    }
  }
  return out;
}
function el(tag, attrs, parent){
  const e = document.createElementNS(NS, tag);
  for(const k in attrs) e.setAttribute(k, attrs[k]);
  if(parent) parent.appendChild(e);
  return e;
}
function txt(parent, x, y, s, cls, anchor){
  const e = el('text', {x, y, 'class':cls}, parent);
  if(anchor) e.setAttribute('text-anchor', anchor);
  e.textContent = s;
  return e;
}
function renderGantt(list){
  const fig = $('#gantt');
  fig.innerHTML = '';
  const rows = list.filter(t=>t.start||t.due)
    .sort((a,b)=>((a.start||a.due).localeCompare(b.start||b.due)));
  if(!rows.length){
    fig.innerHTML = '<p class="showing">No dated tasks match the current filters.</p>';
    return;
  }
  let lo=null, hi=null;
  for(const t of rows){
    for(const s of [t.start, t.due]){
      if(!s) continue;
      const d = pd(s);
      if(!lo || d<lo) lo=d;
      if(!hi || d>hi) hi=d;
    }
  }
  lo = addD(lo,-3); hi = addD(hi,4);
  if(TODAY_D<lo) lo = addD(TODAY_D,-3);
  if(TODAY_D>hi) hi = addD(TODAY_D,4);
  const span = diffD(lo,hi);
  const narrow = window.innerWidth < 560;
  const gutter = narrow ? 150 : 240;
  let ppd = PPD[state.zoom];
  let mode = state.zoom;
  if(state.zoom==='fit'){
    const avail = Math.max(320, Math.min(fig.parentElement.clientWidth||900, 1400))
                  - gutter - 20;
    ppd = Math.max(1.1, avail/span);
    mode = ppd>=16 ? 'day' : ppd>=6 ? 'week' : 'month';
  }
  const W = Math.ceil(span*ppd)+gutter+10;
  const rowH = 26, headH = 34;
  const H = headH + rows.length*rowH + 6;
  const svg = el('svg', {width:W, height:H, role:'img',
    'aria-label':'gantt of dated tasks'}, fig);
  const X = d => gutter + diffD(lo,d)*ppd;

  if(mode==='day'){
    for(let d=new Date(lo); d<=hi; d=addD(d,1)){
      if(d.getDay()===0 || d.getDay()===6)
        el('rect', {x:X(d), y:0, width:ppd, height:H, 'class':'gweekend'}, svg);
    }
  }
  for(const tk of ticks(lo,hi,mode)){
    el('line', {x1:X(tk.d), y1:headH-4, x2:X(tk.d), y2:H, 'class':'gline'}, svg);
    txt(svg, X(tk.d)+3, 13, tk.lbl, 'gtick');
  }
  el('line', {x1:X(TODAY_D), y1:0, x2:X(TODAY_D), y2:H, 'class':'gtoday'}, svg);
  txt(svg, X(TODAY_D)+4, 26, 'today', 'gtodaylbl');

  rows.forEach((t,i)=>{
    const y = headH + i*rowH;
    if(i%2===0) el('rect', {x:0, y, width:W, height:rowH, fill:'rgba(139,152,165,.045)'}, svg);
    el('line', {x1:0, y1:y+rowH, x2:W, y2:y+rowH, 'class':'gline'}, svg);
    const lbl = rowMeta(t);
    const maxc = Math.floor((gutter-12)/(narrow?5.6:6.2));
    const clipped = lbl.length>maxc ? lbl.slice(0, maxc-1)+'…' : lbl;
    const te = txt(svg, gutter-8, y+17, clipped, 'glabel', 'end');
    te.setAttribute('data-id', t.id);
    te.style.cursor = 'pointer';
    const s = pd(t.start||t.due), d = pd(t.due||t.start);
    if(t.milestone){
      const cx = X(d), cy = y+rowH/2, r=8;
      const dm = el('path', {d:`M ${cx} ${cy-r} L ${cx+r} ${cy} L ${cx} ${cy+r} L ${cx-r} ${cy} Z`,
        fill: t.mark?t.mark.color:'var(--accent)', stroke:'var(--bg)', 'stroke-width':1,
        'data-id':t.id}, svg);
      dm.style.cursor='pointer';
    } else {
      const bx = X(s<d?s:d), bw = Math.max(3, Math.abs(X(d)-X(s)));
      const bar = el('rect', {x:bx, y:y+5, width:bw, height:rowH-10, rx:3,
        fill:t.hue, 'data-id':t.id}, svg);
      bar.style.cursor='pointer';
      if(t.status==='done') bar.setAttribute('fill-opacity','0.45');
      if(t.status==='archived') bar.setAttribute('fill-opacity','0.3');
      if(t.blocked) bar.setAttribute('stroke','var(--soon)');
      if(overdue(t)){
        const mk = el('path', {d:`M ${bx+bw+4} ${y+rowH-8} l 4 -8 l 4 8 Z`,
          fill:'var(--over)', 'data-id':t.id}, svg);
        mk.style.cursor='pointer';
      }
    }
  });
  fig.style.minWidth = W+'px';
}

// ---- tooltip + modal --------------------------------------------------------
const tt = $('#tt');
function tipHtml(t){
  const bits = ['<div class="ttt">'+esc(t.title)+'</div>',
    '<div class="ttm">'+esc(t.board)+' · '+esc(t.project)+'</div>',
    '<div>'+esc(t.phase)+' · '+esc(t.priority)+' priority · '+esc(t.status)+
    (t.blocked?' · <b>blocked</b>':'')+'</div>'];
  if(t.due) bits.push('<div>due '+t.due+(t.due_in!==null?
    ' ('+(t.due_in<0?(-t.due_in)+'d overdue':'in '+t.due_in+'d')+')':'')+'</div>');
  if(t.start) bits.push('<div>start '+t.start+'</div>');
  if(t.mark) bits.push('<div>'+t.mark.shape+' '+esc(t.mark.name)+' milestone</div>');
  if(t.deps.length) bits.push('<div>waits on: '+t.deps.map(d=>esc(d.title)).join(', ')+'</div>');
  bits.push('<div class="ttm">click for the full card</div>');
  return bits.join('');
}
function esc(s){ const d=document.createElement('div'); d.textContent=s; return d.innerHTML; }

function openModal(id){
  const t = DATA.tasks.find(x=>x.id===id);
  if(!t) return;
  $('#m-title').textContent = t.title + (t.mark ? '  '+t.mark.shape : '');
  $('#m-sub').textContent = t.board+' · '+t.project;
  const dl = $('#m-fields');
  dl.innerHTML = '';
  const rows = [
    ['Phase', t.phase], ['Priority', t.priority], ['Status',
      t.status + (t.blocked?' · blocked':'') + (overdue(t)?' · overdue':'')],
    ['Start', t.start || '—'], ['Due', t.due || '—'],
    ['In phase', t.age===null ? 'unaged' : t.age+'d'],
    ['Milestone', t.mark ? t.mark.shape+' '+t.mark.name : '—'],
    ['Depends on', t.deps.length ? t.deps.map(d=>d.title).join(' → ') : '—'],
    ['Downstream', t.chain.length ? t.chain.join(' → ') : '—'],
    ['Mentions', t.mentions.length ? t.mentions.map(m=>'@'+m).join(', ') : '—'],
  ];
  for(const [k,v] of rows){
    const dt=document.createElement('dt'); dt.textContent=k;
    const dd=document.createElement('dd'); dd.textContent=v;
    dl.appendChild(dt); dl.appendChild(dd);
  }
  const ul = $('#m-urls');
  ul.innerHTML='';
  for(const u of t.urls){
    const li=document.createElement('li');
    const a=document.createElement('a');
    a.href=u; a.textContent=u; a.target='_blank'; a.rel='noopener noreferrer';
    li.appendChild(a); ul.appendChild(li);
  }
  $('#m-urls-wrap').style.display = t.urls.length ? '' : 'none';
  $('#m-notes').innerHTML = t.notes_html || '<span class="ttm">no notes</span>';
  $('#modal').classList.add('open');
  $('#mclose').focus();
}
function closeModal(){ $('#modal').classList.remove('open'); }

// ---- table ------------------------------------------------------------------
const COLS = [
  ['title','Task'],['board','Board'],['project','Project'],['phase','Phase'],
  ['priority','Prio'],['start','Start'],['due','Due'],['age','In phase'],['status','Status']];
function cellText(t,k){
  if(k==='start'||k==='due') return t[k] || '—';
  if(k==='age') return t.age===null ? 'unaged' : t.age+'d';
  if(k==='status'){
    let s=t.status;
    if(t.blocked) s+=' · blocked';
    if(overdue(t)) s+=' · overdue';
    return s;
  }
  if(k==='title') return t.mark ? t.title+'  '+t.mark.shape : t.title;
  return t[k];
}
function renderTable(list){
  const sorted = [...list].sort((a,b)=>{
    const k=state.sortKey, d=state.sortDir;
    const av=a[k]===null?'':a[k], bv=b[k]===null?'':b[k];
    if(typeof av==='number' && typeof bv==='number') return (av-bv)*d;
    return String(av).localeCompare(String(bv))*d;
  });
  const tb = $('#tbody');
  tb.innerHTML='';
  for(const t of sorted){
    const tr=document.createElement('tr');
    tr.className = t.status==='done'?'rowdone':(t.status==='archived'?'rowarch':'');
    for(const [k] of COLS){
      const td=document.createElement('td');
      if(k==='title'){
        const dot=document.createElement('span');
        dot.className='dot'; dot.style.background=t.hue;
        td.appendChild(dot);
        const sp=document.createElement('span');
        sp.textContent=cellText(t,k);
        if(t.mark) sp.className='tmark';
        td.appendChild(sp);
        if(t.blocked){ const b=document.createElement('span');
          b.className='blk'; b.textContent=' ⛔'; td.appendChild(b); }
        if(overdue(t)){ const o=document.createElement('span');
          o.className='flag'; o.textContent=' '+(-t.due_in)+'d over'; td.appendChild(o); }
        tr.title='click for the task card';
        tr.style.cursor='pointer';
        tr.addEventListener('click',()=>openModal(t.id));
      } else {
        td.textContent = cellText(t,k);
        if(k==='due' && overdue(t)) td.className='flag';
      }
      tr.appendChild(td);
    }
    tb.appendChild(tr);
  }
  const empty = $('#tempty');
  empty.style.display = sorted.length ? 'none' : '';
}
function renderHead(){
  const hr = $('#thead-row');
  hr.innerHTML='';
  for(const [k,label] of COLS){
    const th=document.createElement('th');
    const b=document.createElement('button');
    b.textContent=label;
    if(state.sortKey===k){
      const ind=document.createElement('span');
      ind.className='ind'; ind.textContent=state.sortDir>0?' ▲':' ▼';
      b.appendChild(ind);
    }
    b.addEventListener('click',()=>{
      if(state.sortKey===k) state.sortDir*=-1;
      else { state.sortKey=k; state.sortDir=1; }
      refresh();
    });
    th.appendChild(b); hr.appendChild(th);
  }
}

// ---- downloads ---------------------------------------------------------------
function csvCell(v){
  v = v===null||v===undefined ? '' : String(v);
  return /[",\n]/.test(v) ? '"'+v.replace(/"/g,'""')+'"' : v;
}
function download(name, text, mime){
  const b=new Blob([text],{type:mime});
  const u=URL.createObjectURL(b);
  const a=document.createElement('a');
  a.href=u; a.download=name; document.body.appendChild(a); a.click(); a.remove();
  setTimeout(()=>URL.revokeObjectURL(u), 500);
}
function exportRows(list){
  return list.map(t=>({
    board:t.board, project:t.project, task:t.title, phase:t.phase,
    priority:t.priority, status:cellText(t,'status'),
    start:t.start||'', due:t.due||'',
    days_in_phase:t.age===null?'':t.age,
    milestone:t.milestone?t.mark?t.mark.name:'yes':'',
    blocked:t.blocked?'yes':'', archived:t.archived?'yes':'',
    depends_on:t.deps.map(d=>d.title).join(' | '),
    mentions:t.mentions.map(m=>'@'+m).join(' '),
    urls:t.urls.join(' '), notes:t.notes,
  }));
}
function dlCsv(){
  const list=filtered();
  const rows=exportRows(list);
  const head=Object.keys(rows[0]||{board:0,project:0,task:0});
  const body=[head.join(',')].concat(
    rows.length ? rows.map(r=>head.map(k=>csvCell(r[k])).join(',')) : []);
  download('taskboard-tasks-'+TODAY+'.csv', body.join('\n'), 'text/csv');
}
function dlJson(){
  const payload={generated:DATA.meta.generated, today:TODAY,
                 note:'counts and dates only — nothing here is a forecast',
                 tasks:exportRows(filtered())};
  download('taskboard-tasks-'+TODAY+'.json',
           JSON.stringify(payload,null,2), 'application/json');
}

// ---- filters wiring -----------------------------------------------------------
function chip(parent, label, on, cb){
  const b=document.createElement('button');
  b.textContent=label; b.setAttribute('aria-pressed', on?'true':'false');
  b.addEventListener('click',cb);
  parent.appendChild(b);
  return b;
}
function buildFilters(){
  const bf=$('#f-boards');
  for(const b of DATA.meta.boards){
    chip(bf, b, false, e=>{
      const on = e.currentTarget.getAttribute('aria-pressed')==='true';
      e.currentTarget.setAttribute('aria-pressed', on?'false':'true');
      on ? state.boards.delete(b) : state.boards.add(b);
      refresh();
    });
  }
  const sf=$('#f-status');
  for(const s of ['open','done','archived','blocked','overdue']){
    chip(sf, s, false, e=>{
      const on = e.currentTarget.getAttribute('aria-pressed')==='true';
      e.currentTarget.setAttribute('aria-pressed', on?'false':'true');
      on ? state.status.delete(s) : state.status.add(s);
      refresh();
    });
  }
  const pf=$('#f-person');
  const names=[...new Set(DATA.tasks.flatMap(t=>t.mentions))].sort();
  chip(pf,'all',true,e=>{state.person='all';pressOnly(pf,e.currentTarget);refresh();});
  for(const n of names){
    chip(pf,n,false,e=>{state.person=n;pressOnly(pf,e.currentTarget);refresh();});
  }
  const mf=$('#f-marks');
  const markNames=[...new Set(DATA.tasks.filter(t=>t.mark).map(t=>t.mark.name))];
  chip(mf,'all',true,e=>{state.mark='all';pressOnly(mf,e.currentTarget);refresh();});
  for(const n of markNames){
    chip(mf,n,false,e=>{state.mark=n;pressOnly(mf,e.currentTarget);refresh();});
  }
  chip(mf,'no milestone',false,e=>{state.mark='none';pressOnly(mf,e.currentTarget);refresh();});
  const sel=$('#f-project');
  for(const p of DATA.projects){
    const o=document.createElement('option');
    o.value=p.name; o.textContent=p.board+' — '+p.name;
    sel.appendChild(o);
  }
  sel.addEventListener('change',()=>{state.project=sel.value;refresh();});
  $('#f-q').addEventListener('input',e=>{state.q=e.target.value;refresh();});
  document.querySelectorAll('.zbtn').forEach(b=>{
    b.addEventListener('click',()=>{
      state.zoom=b.dataset.zoom;
      document.querySelectorAll('.zbtn').forEach(x=>
        x.setAttribute('aria-pressed', x===b?'true':'false'));
      refresh();
    });
  });
  $('#dl-csv').addEventListener('click',dlCsv);
  $('#dl-json').addEventListener('click',dlJson);
}
function pressOnly(group, btn){
  group.querySelectorAll('button').forEach(b=>
    b.setAttribute('aria-pressed', b===btn?'true':'false'));
}

function refresh(){
  const list=filtered();
  renderTiles(list);
  renderGantt(list);
  renderTable(list);
}

// ---- global events -------------------------------------------------------------
document.addEventListener('DOMContentLoaded',()=>{
  buildFilters();
  renderHead();
  refresh();
  const svgFig=$('#gantt');
  svgFig.addEventListener('click',e=>{
    const n=e.target.closest('[data-id]');
    if(n) openModal(n.getAttribute('data-id'));
  });
  svgFig.addEventListener('mousemove',e=>{
    const n=e.target.closest('[data-id]');
    if(!n){ tt.style.display='none'; return; }
    const t=DATA.tasks.find(x=>x.id===n.getAttribute('data-id'));
    if(!t){ tt.style.display='none'; return; }
    tt.innerHTML=tipHtml(t);
    tt.style.display='block';
    const w=tt.offsetWidth, h=tt.offsetHeight;
    let x=e.clientX+14, y=e.clientY+14;
    if(x+w>window.innerWidth-8) x=e.clientX-w-14;
    if(y+h>window.innerHeight-8) y=e.clientY-h-14;
    tt.style.left=x+'px'; tt.style.top=y+'px';
  });
  svgFig.addEventListener('mouseleave',()=>{ tt.style.display='none'; });
  $('#mclose').addEventListener('click',closeModal);
  $('#modal').addEventListener('click',e=>{ if(e.target.id==='modal') closeModal(); });
  document.addEventListener('keydown',e=>{
    if(e.key==='Escape' && $('#modal').classList.contains('open')) closeModal();
  });
});
"""


def build(data: dict) -> str:
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>taskboard — interactive workspace report</title>
<style>{CSS}</style></head>
<body><main>
<h1>taskboard · interactive workspace</h1>
<p class="sub">Every board, every task: an explorable gantt, filters, and a
sortable table. Generated {TODAY.isoformat()} from the boards' own data.</p>

<div class="tiles">
  <div class="tile"><div class="n" id="tile-open">0</div><div class="k">open</div></div>
  <div class="tile"><div class="n" id="tile-done">0</div><div class="k">done</div></div>
  <div class="tile"><div class="n" id="tile-late">0</div><div class="k">overdue</div></div>
  <div class="tile"><div class="n" id="tile-arch">0</div><div class="k">archived</div></div>
</div>
<p class="showing" id="showing"></p>

<div class="controls panel">
  <div class="cgroup"><span class="lbl">zoom</span>
    <button class="zbtn" data-zoom="fit" aria-pressed="true">fit</button>
    <button class="zbtn" data-zoom="day" aria-pressed="false">day</button>
    <button class="zbtn" data-zoom="week" aria-pressed="false">week</button>
    <button class="zbtn" data-zoom="month" aria-pressed="false">month</button>
  </div>
  <div class="cgroup" id="f-boards"><span class="lbl">board</span></div>
  <div class="cgroup"><span class="lbl">project</span>
    <select id="f-project"><option value="all">all projects</option></select>
  </div>
  <div class="cgroup" id="f-person"><span class="lbl">person</span></div>
  <div class="cgroup" id="f-marks"><span class="lbl">milestone</span></div>
  <div class="cgroup" id="f-status"><span class="lbl">status</span></div>
  <div class="cgroup"><span class="lbl">search</span>
    <input type="search" id="f-q" placeholder="title, notes, project…"></div>
  <div class="cgroup"><span class="lbl">export</span>
    <button class="dl" id="dl-csv">Download CSV</button>
    <button class="dl" id="dl-json">Download JSON</button></div>
</div>

<h2 id="ganttsec">The gantt — all dated tasks</h2>
<div class="gantt-wrap" id="ganttscroll"><div id="gantt"></div></div>

<h2>The tasks</h2>
<div class="tbl-wrap"><table>
<thead><tr id="thead-row"></tr></thead>
<tbody id="tbody"></tbody>
</table></div>
<p class="showing" id="tempty" style="display:none">No tasks match the current filters.</p>

<div id="tt" role="tooltip"></div>
<div id="modal" role="dialog" aria-modal="true" aria-labelledby="m-title">
  <div class="cardwrap"><div class="card">
    <button id="mclose" aria-label="close">✕</button>
    <h3 id="m-title"></h3>
    <p class="csub" id="m-sub"></p>
    <dl id="m-fields"></dl>
    <div id="m-urls-wrap"><span class="lbl" style="font-size:.74rem;text-transform:uppercase;letter-spacing:.05em;color:var(--mut)">links</span>
    <ul id="m-urls"></ul></div>
    <div class="notes" id="m-notes"></div>
  </div></div>
</div>

<footer>taskboard · a local file, generated on demand. Counts and dates only —
nothing here is a forecast. Work with no recorded phase change reads
<em>unaged</em> rather than a guess.</footer>
</main>
<script id="board-data" type="application/json">{payload}</script>
<script>{JS}</script>
</body></html>
"""


def main() -> None:
    data = collect()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / "b-report.html"
    out.write_text(build(data), encoding="utf-8")
    print(f"wrote {out} ({out.stat().st_size} bytes, "
          f"{len(data['tasks'])} tasks, {len(data['projects'])} projects)")


if __name__ == "__main__":
    main()
