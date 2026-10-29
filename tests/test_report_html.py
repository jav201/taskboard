"""The one extraction behind the HTML reports (batch 2026-10-29-batch-01, increment 001).

LLR-3101.1..3, LLR-3106.1, LLR-3107.3's slug: `report_html.extract` returns JSON-able
facts only, keys every project and task uniquely across boards, emits ONE status
and ONE due word per task (the CLI report's), keeps only http(s) URLs, never names
another task's text inside a task, and never writes a board. The renderers read
the dict alone. Expected values are the fixture's literals, never read back from
the code under test.
"""
from __future__ import annotations

import ast
import asyncio
import hashlib
import json
import re
import sys
from pathlib import Path

import pytest
import report_fixture as F
from report_browser import new_context, open_page, require_browser, shown_ids

from taskboard import report_html, report_workspace
from taskboard.models import Board
from taskboard.report import _due_word, report_path

PKG = Path(report_html.__file__).parent

TOP_KEYS = {"v", "meta", "boards", "projects", "tasks", "people", "marks"}
META_KEYS = {"generated", "today", "scope", "view"}
BOARD_KEYS = {"key", "name", "colour"}
PROJECT_KEYS = {"key", "board", "id", "name", "colour", "archived", "status", "momentum",
                "open", "done", "late", "worst", "high", "due", "due_word", "phases"}
TASK_KEYS = {"key", "project", "board", "title", "phase", "priority", "start", "due",
             "due_in", "age", "done", "archived", "status", "blocked", "milestone", "mark",
             "mentions", "deps", "chain", "due_word", "notes_html", "notes_text", "urls"}
PERSON_KEYS = {"id", "name", "role"}
MARK_KEYS = {"key", "name", "shape", "colour"}


def _d(project=None, folder=None):
    return report_html.extract(F.lanes(folder), F.PEOPLE, F.MARKS, F.TODAY, project=project)


def _task(d, key):
    return next(t for t in d["tasks"] if t["key"] == key)


def test_TC_3101_extract_is_json_and_holds_every_fact():
    """TC-3101 (LLR-3101.1): the frozen shape, a lossless JSON round trip, keys unique
    across boards (two `Docs` projects share the id `pdocs`), the Inbox and the unlisted
    board keyed by position, deps/chain as keys of tasks present, and no task's title
    inside another task's record — a task carries facts, not its neighbours' text."""
    d = _d()
    assert json.loads(json.dumps(d)) == d
    assert set(d) == TOP_KEYS and d["v"] == 1
    assert set(d["meta"]) == META_KEYS and d["meta"]["view"] is None
    assert d["meta"]["generated"] == d["meta"]["today"] == "2026-10-29"
    assert d["meta"]["scope"] == {"kind": "all", "project": None,
                                  "boards": ["Personal", "Client A", "Course", F.SIDE_BOARD_NAME]}
    assert all(set(b) == BOARD_KEYS for b in d["boards"])
    assert [b["key"] for b in d["boards"]] == F.BOARD_KEYS
    assert all(set(p) == PROJECT_KEYS for p in d["projects"])
    assert all(set(t) == TASK_KEYS for t in d["tasks"])
    assert all(set(p) == PERSON_KEYS for p in d["people"])
    assert all(set(m) == MARK_KEYS for m in d["marks"])

    keys = [p["key"] for p in d["projects"]]
    assert len(set(keys)) == len(keys) == 13
    assert keys == F.PROJECT_KEYS
    inbox = next(p for p in d["projects"] if p["key"] == "personal:inbox")
    assert (inbox["name"], inbox["id"], inbox["colour"]) == ("Inbox", None, "#5b6675")
    assert _task(d, "personal:tin1")["project"] == "personal:inbox"

    assert len(d["tasks"]) == F.TASK_COUNT
    assert [t["key"] for t in d["tasks"]] == F.TASK_KEYS          # archived included, in order
    present = {t["key"] for t in d["tasks"]}
    assert all(k in present for t in d["tasks"] for k in t["deps"] + t["chain"])
    assert _task(d, "client-a:tsp3")["deps"] == ["client-a:tst4"]   # cross-project, all scope
    assert _task(d, "client-a:tst2")["chain"] == ["client-a:tst3", "client-a:tst4",
                                                  "client-a:tst5", "client-a:tsp3"]
    for t in d["tasks"]:
        record = json.dumps(t, ensure_ascii=False)
        others = [o["title"] for o in d["tasks"] if o["key"] != t["key"]]
        assert not [o for o in others if o in record], t["key"]

    assert [p["id"] for p in d["people"]] == F.PEOPLE_IDS          # nora.idle: never mentioned
    assert [m["key"] for m in d["marks"]] == F.CLASS_KEYS          # `unused`: no milestone
    assert _task(d, "personal:ttx1")["mentions"] == ["ana.ruiz", "luis.prado"]
    assert _task(d, "client-a:tst5")["mark"] == "launch"
    assert _task(d, "personal:tmv3")["mark"] is None

    lane = next(p for p in d["projects"] if p["key"] == "client-a:prel")
    # `done` counts the project's tasks whose status is done — archived work excluded
    # (st7 is archived), so a slide's done figure agrees with the task statuses (CR2);
    # `views.lane_facts.done_n` would count st7 too and read 2
    assert (lane["open"], lane["done"], lane["late"], lane["worst"]) == (10, 1, 2, 3)
    assert all(p["done"] == sum(1 for t in d["tasks"] if t["project"] == p["key"]
                                and t["status"] == "done") for p in d["projects"])
    old = next(p for p in d["projects"] if p["key"] == "client-a:pold")
    assert old["due_word"] == "-3d"                                  # closed: no overdue framing
    assert next(p for p in d["projects"] if p["key"] == "client-a:parch")["archived"] is True


def test_TC_3101_extract_never_writes_a_board(tmp_path, monkeypatch):
    """TC-3101's read-only arm (the `report.py` law): each board file is byte-identical
    across an extraction and `Board.save` is never called — saving an unmodified board
    can rewrite identical bytes, which a checksum alone cannot see."""
    lanes = F.lanes(tmp_path)
    for _, _, _, board in lanes:
        board.save()
    before = {b.path: hashlib.sha256(b.path.read_bytes()).hexdigest() for *_, b in lanes}
    saves = []
    monkeypatch.setattr(Board, "save", lambda self: saves.append(self.path))
    report_html.extract(lanes, F.PEOPLE, F.MARKS, F.TODAY)
    assert saves == []
    assert {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in before} == before


def test_TC_3102_due_words_are_the_cli_reports():
    """TC-3102 (LLR-3101.2): every task's due word is `report._due_word` of its distance —
    the workspace and the CLI report cannot disagree on `3d overdue`."""
    d = _d()
    for t in d["tasks"]:
        assert t["due_word"] == _due_word(t["due_in"]), t["key"]
    assert {k: _task(d, k)["due_word"] for k in F.DUE_WORDS} == F.DUE_WORDS


def test_TC_3103_project_scope_keeps_one_project():
    """TC-3103 (LLR-3101.3): scope `p` keeps one project and its tasks; a dependency on a
    task outside it is cut (`sp3` waits on `st4` of another project)."""
    d = _d("client-a:pdocs")
    assert [p["key"] for p in d["projects"]] == ["client-a:pdocs"]
    assert [t["key"] for t in d["tasks"]] == ["client-a:tsp1", "client-a:tsp2", "client-a:tsp3"]
    assert _task(d, "client-a:tsp3")["deps"] == []
    keys = {t["key"] for t in d["tasks"]}
    assert all(k in keys for t in d["tasks"] for k in t["deps"] + t["chain"])
    assert d["meta"]["scope"] == {"kind": "project", "project": "client-a:pdocs",
                                  "boards": ["Client A"]}
    assert [b["key"] for b in d["boards"]] == ["client-a"]
    assert [p["id"] for p in d["people"]] == ["ana.ruiz", "carmen.vega"]
    inbox = _d("personal:inbox")
    assert [t["key"] for t in inbox["tasks"]] == ["personal:tin1"]


def test_TC_3103_an_unknown_project_key_is_refused(tmp_path):
    """TC-3103's invalid arm (CR4): a scope naming no project is an error that names the
    key — never an empty report, never a bare StopIteration from the writer."""
    with pytest.raises(ValueError, match="'client-a:nope'"):
        _d("client-a:nope")
    d = _d()
    d["meta"]["scope"] = {"kind": "project", "project": "course:gone", "boards": []}
    with pytest.raises(ValueError, match="'course:gone'"):
        report_html.write_reports(d, ("workspace",), tmp_path / "reports", F.TODAY)
    assert not (tmp_path / "reports").exists()


def _resolve(node: ast.ImportFrom) -> str:
    if node.level == 0:
        return node.module or ""
    return "taskboard" + ("." + node.module if node.module else "")


def _imports(path: Path):
    """(module, names, at module level) per import; dynamic imports as `<dynamic>`."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    top = {id(n) for n in tree.body}
    out = []
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            out += [(a.name, [], id(n) in top) for a in n.names]
        elif isinstance(n, ast.ImportFrom):
            base = _resolve(n)
            if base == "taskboard":
                out += [(f"taskboard.{a.name}", [], id(n) in top) for a in n.names]
            else:
                out.append((base, [a.name for a in n.names], id(n) in top))
        elif isinstance(n, ast.Call):
            f = n.func
            name = f.id if isinstance(f, ast.Name) else f.attr if isinstance(f, ast.Attribute) else ""
            if name in ("import_module", "__import__"):
                out.append(("<dynamic>", [name], id(n) in top))
    return out


def _stdlib(mod: str) -> bool:
    return mod.split(".")[0] in sys.stdlib_module_names or mod == "__future__"


def renderer_offences(path: Path) -> list:
    return [(m, names) for m, names, _ in _imports(path)
            if m != "taskboard.report_html" and not (_stdlib(m) and m != "<dynamic>")]


def extraction_offences(path: Path) -> list:
    banned = {f"taskboard.{m}" for m in ("app", "modals", "keymap", "boards", "team_sync")}
    renderers = {"taskboard.report_workspace", "taskboard.report_deck"}
    bad = []
    for m, names, top in _imports(path):
        if m in banned or m == "<dynamic>":
            bad.append((m, names))
        elif m == "taskboard.report" and (not names or set(names) - {"_e", "_due_word"}):
            bad.append((m, names))
        elif m in renderers and top:
            bad.append((m, "module level"))
    return bad


def test_TC_3104_renderers_read_the_dict_only():
    """TC-3104 (LLR-3101.3, PDR PA3/PQ10): an AST walk — the workspace renderer imports
    nothing of the package but `report_html` (no dynamic import either); `report_html`
    imports nothing of app/modals/keymap/boards/team_sync, from `report` only `_e` and
    `_due_word`, and the renderers only inside a function (they import it). The same
    dict renders to the same bytes."""
    assert renderer_offences(PKG / "report_workspace.py") == []
    assert extraction_offences(PKG / "report_html.py") == []
    # the walk is not vacuous: it sees the imports it allows
    seen = {m for m, _, _ in _imports(PKG / "report_html.py")}
    assert {"taskboard.report", "taskboard.views", "taskboard.report_workspace"} <= seen
    assert "taskboard.report_html" in {m for m, _, _ in _imports(PKG / "report_workspace.py")}
    d = _d()
    assert report_workspace.render(d) == report_workspace.render(_d())


def test_TC_3115_embed_json_and_notes_are_inert():
    """TC-3115 (LLR-3106.1): the embedded JSON carries no `<`, `>` or `&`, so no board
    string can close its `<script>` element, and it decodes to the original; notes HTML
    escapes every piece and holds only the constant tags."""
    s = "</script><b>x</b> & \"q\""
    out = report_html.embed_json({"s": s})
    assert not set("<>&") & set(out)
    assert json.loads(out) == {"s": s}
    page = report_workspace.render(_d())
    assert "<script>alert(1)" not in page and "</script><b>" not in page
    assert page.count("<script") == 2

    html = report_html.notes_html("==a== <b>x</b> @ana.ruiz", F.PEOPLE)
    assert "&lt;b&gt;x&lt;/b&gt;" in html
    assert set(re.findall(r"</?([a-zA-Z]+)", html)) <= {"span", "br"}
    assert '<span class="hl-soon">a</span>' in html
    assert '<span class="hl-mut mention">@Ana Ruiz</span>' in html
    hostile = report_html.notes_html(F.HOSTILE_NOTE, F.PEOPLE)
    assert set(re.findall(r"</?([a-zA-Z]+)", hostile)) <= {"span", "br"}
    assert "&lt;/script&gt;" in hostile and "&amp;" in hostile
    assert "@Zed &lt;/script&gt;&lt;img src=x onerror=window.__x=1&gt; &amp; co" in hostile
    assert report_html.notes_html("", F.PEOPLE) == ""


def test_TC_3123_the_slug_is_the_cli_reports():
    """TC-3123 (LLR-3107.3): `report_html.slug` is `report.report_path`'s slug rule, and
    a project file name carries the board slug AND the project slug, so two boards'
    same-named projects never collide."""
    board = F.client_a()
    for name in ("Storefront relaunch", "Año 2026 — ñandú", "a" * 60):
        cli = report_path(board, F.TODAY, project=name).name
        assert cli == f"{report_html.slug(name)}-2026-10-29.html"
    assert report_html.report_name("workspace", F.TODAY) == "workspace-2026-10-29.html"
    assert report_html.report_name("deck", F.TODAY) == "deck-2026-10-29.html"
    assert report_html.report_name("workspace", F.TODAY, "client-a", "storefront-relaunch") == \
        "workspace-client-a-storefront-relaunch-2026-10-29.html"
    assert report_html.report_name("workspace", F.TODAY, "personal", "docs") != \
        report_html.report_name("workspace", F.TODAY, "client-a", "docs")


def test_TC_3123_write_reports_lands_in_the_folder_and_overwrites(tmp_path):
    """LLR-3107.3's writer: the workspace is written in the given folder (created),
    named for its scope; a same-day export overwrites instead of adding a file."""
    folder = tmp_path / "reports"
    paths = report_html.write_reports(_d(), ("workspace",), folder, F.TODAY)
    assert paths == [folder / "workspace-2026-10-29.html"]
    assert paths[0].read_text(encoding="utf-8") == report_workspace.render(_d())
    scoped = report_html.write_reports(_d("client-a:prel"), ("workspace",), folder, F.TODAY)
    assert scoped == [folder / "workspace-client-a-storefront-relaunch-2026-10-29.html"]
    report_html.write_reports(_d(), ("workspace",), folder, F.TODAY)
    fresh = tmp_path / "other"
    with pytest.raises(ValueError, match="bogus"):
        report_html.write_reports(_d(), ("workspace", "bogus"), fresh, F.TODAY)
    assert not fresh.exists()                         # checked before anything is written (CR3)
    assert sorted(p.name for p in folder.iterdir()) == [
        "workspace-2026-10-29.html", "workspace-client-a-storefront-relaunch-2026-10-29.html"]


def test_TC_3124_extract_keeps_only_http_urls():
    """TC-3124 (LLR-3101.1, D1): only `views.valid_url` results survive — a
    `javascript:` or `data:` URL never reaches either report."""
    d = _d()
    assert _task(d, "client-a:tst8")["urls"] == ["https://example.test/ok"]
    assert _task(d, "client-a:tst4")["urls"] == ["https://staging.example.test/storefront"]
    blob = report_html.embed_json(d)
    assert "javascript:" not in blob and "data:text" not in blob


def test_TC_3125_one_status_rule():
    """TC-3125 (LLR-3101.1, D19): archived > done > late (open, due before today) > open,
    computed once by `extract`; a task due TODAY is open. The page reads the field and
    never re-derives it from the due distance."""
    d = _d()
    assert {t["key"]: t["status"] for t in d["tasks"]} == F.STATUS
    assert _task(d, "personal:tdc1")["due_in"] == 0
    assert not re.search(r"due_in\s*[<>]", report_workspace.JS)


# ---- PQ6 spike: an app-level (asyncio) test checks a written page in a worker thread ------------

async def test_PQ6_spike_an_async_test_checks_the_page_in_a_worker_thread(tmp_path):
    """PDR PQ6 spike, decided for increment 004: inside a Textual `run_test` (a running
    asyncio loop, where the sync Playwright API refuses to start), the written file is
    checked with `await asyncio.to_thread(check, path)` — Playwright launched INSIDE the
    worker thread, no shared browser fixture. The app's loop keeps running meanwhile.
    It lives in this module, not beside the module-scoped browser of
    `test_report_workspace.py`: with that sync Playwright alive on the main thread the
    test's own loop fails (`RuntimeError: This event loop is already running`) — the
    reason increment 004's export-app module must hold no shared browser fixture."""
    api = require_browser()
    from textual.app import App

    path = report_html.write_reports(
        report_html.extract(F.lanes(), F.PEOPLE, F.MARKS, F.TODAY), ("workspace",),
        tmp_path / "reports", F.TODAY)[0]

    def check(p):
        with api.sync_playwright() as pw:
            b = pw.chromium.launch()
            ctx = new_context(b)
            o = open_page(ctx, p)
            out = (set(shown_ids(o.page)), o.problems())
            b.close()
        return out

    ticks = []

    class Probe(App):
        def on_mount(self):
            self.set_interval(0.05, lambda: ticks.append(1))

    async with Probe().run_test() as pilot:
        shown, problems = await asyncio.to_thread(check, path)
        await pilot.pause()
    assert shown == F.DEFAULT_SHOWN and problems == []
    assert len(ticks) > 1
