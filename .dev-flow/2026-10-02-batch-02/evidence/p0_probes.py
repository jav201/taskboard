"""P0 probes for batch 2026-10-02-batch-02, run on the BASE tree (a0e7d9a).

    python .dev-flow/2026-10-02-batch-02/evidence/p0_probes.py   (cwd = repo root)

Every premise of the batch is measured here over RENDERED output of the oracle
board (tests/kg_board.py) plus a scratch team directory and history file — never
a real board. Output: the premise table's evidence, printed.
"""
import asyncio
import ast
import json
import os
import re
import sys
import tempfile
from datetime import timedelta
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))

from rich.color import Color, ColorSystem  # noqa: E402

import kg_board  # noqa: E402
from kg_board import TODAY  # noqa: E402
from taskboard import history, views  # noqa: E402
from taskboard.team_sync import TEAM_FILENAME, TeamState  # noqa: E402
from taskboard.views import HEX, render_view, reldue_token, gantt_plan, gantt_columns  # noqa: E402

ACCENT = HEX["accent"].lower()


def accent_runs(text):
    plain = text.plain
    starts = [0]
    for line in plain.split("\n"):
        starts.append(starts[-1] + len(line) + 1)
    out = []
    for s in text.spans:
        if ACCENT in str(s.style).lower():
            row = max(i for i, st in enumerate(starts) if st <= s.start)
            out.append((row, plain[s.start:s.end]))
    return out


def team(tmp: Path) -> TeamState:
    cfg = {"version": 3, "phases": kg_board.PHASES,
           "projects": [{"id": "pweb", "name": "Website Redesign", "color": "violet",
                         "status": "on_track"}],
           "roster": [{"id": "jav", "name": "Javier", "hue": "sky"},
                      {"id": "ana", "name": "Ana", "hue": "amber"}]}
    (tmp / TEAM_FILENAME).write_text(json.dumps(cfg), encoding="utf-8")
    st = TeamState(tmp, user_id="jav")
    st.load_config()
    return st


def main():
    tmp = Path(tempfile.mkdtemp(prefix="kg-p0-"))
    b = kg_board.build(tmp / "board.json")
    b.task_by_id("tw6").urls = ["https://example.org/redirects"]
    for i, (tid, frm, to) in enumerate([("tw3", "Next", "Doing"), ("tw2", "Doing", "Review"),
                                        ("tw1", "Review", "Done")]):
        history.append(b.path, {"task": tid, "from": frm, "to": to},
                       at=__import__("datetime").datetime(2026, 9, 20 + i, 10))
    st = team(tmp)
    setup = {"enabled": True, "shared_dir": "D:/team", "interval_minutes": 30,
             "user_id": "jav", "projects": [{"id": "pweb", "name": "Website Redesign",
                                             "shared": True, "color": "violet"}],
             "roster": [{"id": "jav", "name": "Javier", "hue": "sky"}],
             "cursor_section": 0, "cursor_row": 1}

    print("== P-1 accent census, 118x30, oracle board (+URL card, team, history, setup state)")
    for mode, kw in [("swimlanes", {"lanes_presentation": "waves"}),
                     ("swimlanes", {"lanes_presentation": "grid"}),
                     ("agenda", {}), ("focus", {"focus_presentation": "cards"}),
                     ("flow", {}), ("standup", {"team_state": st}),
                     ("people", {"team_state": st}), ("setup", {"setup_state": setup}),
                     ("kanban", {}), ("gantt", {})]:
        text = render_view(mode, b, False, "tw3", TODAY, 118, 30, {}, **kw)
        runs = accent_runs(text)
        print(f"  {mode} {kw.get('lanes_presentation', '')}: {len(runs)} accent run(s)")
        for r, seg in runs[:12]:
            print(f"     row {r}: {seg!r}")
    from taskboard.views import legend_entries
    print("  legend swatches in accent, per view:")
    for mode in ("swimlanes", "agenda", "gantt", "flow", "standup", "people"):
        ents = legend_entries(mode, b, TODAY, 118, 30, team_state=st, selected_id="tw3")
        print(f"     {mode}: {[m for s, m in ents if ACCENT in s.lower()]}")

    print("== P-2 chrome")
    from taskboard.keymap import GROUP_HUE, render_key_bar
    for layer in ("primary", "more"):
        m = render_key_bar(118, "gantt", layer)
        print(f"  keybar {layer}: accent tags {m.lower().count(ACCENT)}; hues "
              f"{sorted({h for h in re.findall(r'#[0-9a-f]{6}', m.lower())})}")
    print(f"  GROUP_HUE: {GROUP_HUE}")
    from taskboard.ribbon import Ribbon
    rb = Ribbon()
    rb.update = lambda markup: None
    m = rb.update_clock(__import__("datetime").datetime(2026, 9, 30, 9, 5, 0))
    print(f"  ribbon: accent tags {m.lower().count(ACCENT)}")
    css = (ROOT / "taskboard" / "taskboard.tcss").read_text(encoding="utf-8")
    blk = css[css.index(".modal-title {"):].split("}")[0]
    print(f"  taskboard.tcss .modal-title: {' '.join(blk.split())}")
    app_src = (ROOT / "taskboard" / "app.py").read_text(encoding="utf-8")
    print(f"  app.py HelpScreen #2dd4bf literals: {app_src.count('#2dd4bf')}")
    modals = (ROOT / "taskboard" / "modals.py").read_text(encoding="utf-8")
    print(f"  modals.py #palette-input:focus border: "
          f"{[ln.strip() for ln in modals.splitlines() if '#palette-input:focus' in ln]}")

    print("== P-3 Spanish UI strings (AST census of string literals, docstrings excluded)")
    SP = re.compile(r"[áéíóúñ¿¡]|\b(uso|leyenda|ejemplo|teclas|mapa|paleta|cierra|completo|"
                    r"para|qué|que|es|lo|primero|haces|las|los|la|el|de|del|sin|con|hace|"
                    r"historia|curso|equipo|proyectos|compartido|sección|edita|alterna|agrega|"
                    r"quita|guarda|cancela|modo|carpeta|alcance|cada|mi|identidad|falta|existe|"
                    r"escribible|miembro|tolerancia|último|todo|marcas|números|tarjeta)\b", re.I)
    total = 0
    for f in sorted((ROOT / "taskboard").glob("*.py")):
        tree = ast.parse(f.read_text(encoding="utf-8"))
        docs = {id(n.body[0].value) for n in ast.walk(tree)
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Module))
                and n.body and isinstance(n.body[0], ast.Expr)
                and isinstance(n.body[0].value, ast.Constant)}
        hits = []
        for n in ast.walk(tree):
            if (isinstance(n, ast.Constant) and isinstance(n.value, str)
                    and id(n) not in docs and SP.search(n.value)):
                hits.append((n.lineno, n.value))
        hits = [(ln, v) for ln, v in hits if f.name != "models.py"]   # city names
        if hits:
            total += len(hits)
            print(f"  {f.name}: {len(hits)} literal(s), lines "
                  f"{sorted({ln for ln, _ in hits})[:40]}")
    print(f"  total: {total} (models.py excluded: proper city names)")

    print("== P-4 weekend background under 256-colour quantisation")
    for h in ("#0d1117", "#161d27", "#1a1d22"):
        c8 = Color.parse(h).downgrade(ColorSystem.EIGHT_BIT)
        print(f"  {h}: 256-colour index {c8.number} ({c8.get_truecolor().hex})")

    print("== P-5 gantt: a paged project group draws no above/below hint")
    from taskboard.models import Board, Project, Task
    big = Board([Project(name="Big", color="sky", id="pbig")],
                [Task(title=f"task {i:02d}", project_id="pbig", phase="Doing",
                      due_date=(TODAY + timedelta(days=i)).isoformat(), id=f"tb{i}")
                 for i in range(30)], tmp / "big.json", {}, kg_board.PHASES)
    lm = {}
    plain = render_view("gantt", big, False, "tb15", TODAY, 80, 24, lm).plain.split("\n")
    print(f"  80x24, tb15 selected: rows drawn {len(lm)} of 30; span label {plain[3][:28]!r}; "
          f"'above' in frame: {any('above' in l for l in plain)}; "
          f"'below' in frame: {any('below' in l for l in plain)}")

    print("== P-6 UXV-3 fold order at panel 80x22 (terminal 80x24)")
    groups = gantt_plan(b, False, "tw3", TODAY, 22 - 3)
    for g in groups:
        due0 = [t.id for t in g.open if t.due_date == TODAY.isoformat()]
        print(f"  {g.project.name:<17} unfolded={g.unfolded} late={g.late} due_today={due0}")

    print("== P-7 UXV-2 the selection's row on each `down` at panel 80x22 (nav order)")
    nav = views.nav_model("gantt", b, False, TODAY, 80, 22)[0]
    prev, ups = None, []
    for tid in nav:
        lm = {}
        render_view("gantt", b, False, tid, TODAY, 80, 22, lm)
        if prev is not None and lm[tid] < prev:
            ups.append((tid, prev, lm[tid]))
        prev = lm[tid]
    print(f"  {len(nav)} steps; steps where the highlight moved UP: {ups}")

    print("== P-8 the flow packet and the <=7-day token tones")
    text = render_view("gantt", b, False, "tw3", TODAY, 118, 30, {}, tick=0)
    pk = [str(s.style) for s in text.spans if text.plain[s.start:s.end] == "▬"]
    print(f"  packet styles: {sorted(set(pk))} (bright = {HEX['bright']})")
    t = b.task_by_id("tw6")
    due = t.due_date
    t.due_date = (TODAY + timedelta(days=4)).isoformat()
    print(f"  reldue_token(+4d) = {reldue_token(t, TODAY, b)}")
    t.due_date = due

    print("== P-9 UXV-7 the echo of a task started before the window (tw2, 118x30)")
    lines = render_view("gantt", b, False, "tw2", TODAY, 118, 30, {}).plain.split("\n")
    lw = gantt_columns(118)[0]
    print(f"  day row field starts {lines[2][lw + 1:lw + 8]!r}; task start "
          f"{b.task_by_id('tw2').start_date}")

    print("== P-10 D14 `]` finishing a gantt task shows no notice")
    from taskboard.app import TaskboardApp

    async def run():
        bb = kg_board.build(tmp / "app" / "board.json")
        (tmp / "app").mkdir(exist_ok=True)
        bb.save()
        app = TaskboardApp(board_path=str(bb.path), team_sync_interval=1e9)
        async with app.run_test(size=(118, 34)) as pilot:
            await pilot.pause()
            await pilot.press("3")
            await pilot.pause()
            app.selected_task_id = "tw2"           # Review -> one `]` to Done
            app.refresh_view()
            await pilot.pause()
            before = len(app._notifications)
            await pilot.press("]")
            await pilot.pause()
            print(f"  tw2 done: {app.board.is_done(app.board.task_by_id('tw2'))}; "
                  f"notifications added: {len(app._notifications) - before}; "
                  f"selection now {app.selected_task_id}")
    asyncio.run(run())


if __name__ == "__main__":
    main()
