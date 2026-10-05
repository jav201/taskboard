"""The details view shows and edits a task's links (batch 2026-10-04-batch-01, HLR-503,
LLR-503.1, D-B).

Field report: the details view (`enter`) painted no dependency at all (P-5) — a link
could neither be seen nor removed where the operator reads a task. The verdict frame
D-B: "Waits on" and "Unblocks" (direct and down the chain), the conflict line, `x`
remove, `↵` jump, `L` add.

Law: the section lists every live predecessor (open, done or archived) and every open
dependent, each once; only direct rows can be acted on. Synthetic boards only.
"""
from __future__ import annotations

import json

import kg_board
from taskboard.app import TaskboardApp
from taskboard.modals import TaskDetails


def _toasts(app) -> list[str]:
    return [str(t.render()) for t in app.screen.query("Toast")]


def _section(app) -> tuple[str, list[tuple[str | None, bool, str]], list[str]]:
    """(the heading, the list's (id, disabled, plain) rows, the conflict lines)."""
    scr = app.screen
    head = str(scr.query_one("#deps-head").render())
    rows = []
    lists = scr.query("#deps-list")
    if lists:
        ol = lists.first()
        rows = [(ol.get_option_at_index(i).id, ol.get_option_at_index(i).disabled,
                 ol.get_option_at_index(i).prompt.plain) for i in range(ol.option_count)]
    conflicts = [str(w.render()) for w in scr.query("Label")
                 if str(w.render()).startswith("◂ ")]
    return head, rows, conflicts


async def _details(tmp_path, tid, *, mutate=None, size=(118, 40)):
    path = tmp_path / "board.json"
    b = kg_board.build(path)                       # unshifted: TC-513's dates
    if mutate:
        mutate(b)
    b.save()
    app = TaskboardApp(board_path=str(path))
    return app, path


async def test_TC_513_the_section_equals_the_oracle(tmp_path):
    """TC-513 (LLR-503.1; `evidence/p1-tables.txt`): `tm3` — waits on 1 open of 1
    (`Audit dependencies`, open), ▸1 direct · 2 in chain (`Offline sync`, then
    `└ Beta release to testers`, disabled), the conflict "◂ starts Oct 1, overlaps
    Audit dependencies by 2d (due Oct 2)"; `tw5` — 2 open of 2, no dependents, the
    3-day conflict with `Optimize image assets`; `ta2` — 1 open of 1, no conflict;
    `to4` — "no links — L adds one"; a waiter with no start paints the due form. RED:
    a chain row selectable, a dangling id listed, the conflict measured strictly."""
    want = {
        "tm3": ([("p:tm2", "Audit dependencies", "open")], ["d:tm4"], ["Beta release to testers"],
                ["◂ starts Oct 1, overlaps Audit dependencies by 2d (due Oct 2)"]),
        "tw5": ([("p:tw2", "Build component library", "open"),
                 ("p:tw4", "Optimize image assets", "open")], [], [],
                ["◂ starts Oct 4, overlaps Optimize image assets by 3d (due Oct 6)"]),
        "ta2": ([("p:ta3", "Partner notice emails", "open")], [], [], []),
    }
    for tid, (preds, direct, chain, conflicts) in want.items():
        app, _p = await _details(tmp_path / tid, tid)
        async with app.run_test(size=(118, 40)) as pilot:
            app.selected_task_id = tid
            await pilot.press("enter")
            await pilot.pause()
            head, rows, got_conflicts = _section(app)
            assert head.startswith("Dependencies  ◂ waiting"), (tid, head)
            assert [(r[0], r[2].split("   ")[0], r[2].rsplit("· ", 1)[-1])
                    for r in rows if r[0] and r[0].startswith("p:")] == preds, tid
            assert [r[0] for r in rows if r[0] and r[0].startswith("d:")] == direct, tid
            chain_rows = [r for r in rows if "└ " in r[2]]
            assert [r[2].split("└ ")[1].split("   ")[0] for r in chain_rows] == chain, tid
            assert all(r[1] for r in chain_rows), tid
            assert got_conflicts == conflicts, tid
            if tid == "tm3":
                assert any("▸1 direct · 2 in chain" in r[2] for r in rows)
                assert any("◂1 open of 1" in r[2] for r in rows)
    app, _p = await _details(tmp_path / "to4", "to4")
    async with app.run_test(size=(118, 40)) as pilot:
        app.selected_task_id = "to4"
        await pilot.press("enter")
        await pilot.pause()
        assert [str(w.render()) for w in app.screen.query("Label")
                if "no links" in str(w.render())] == ["no links — L adds one"]
    app, _p = await _details(tmp_path / "ns", "ta2",
                             mutate=lambda b: setattr(b.task_by_id("ta3"), "due_date", "2026-10-09"))
    async with app.run_test(size=(118, 40)) as pilot:
        app.selected_task_id = "ta2"                  # no start, due Oct 7
        await pilot.press("enter")
        await pilot.pause()
        assert _section(app)[2] == [
            "◂ due Oct 7, overlaps Partner notice emails by 2d (due Oct 9)"]


async def test_AT_504_the_details_show_and_edit_the_links(tmp_path):
    """AT-504 (US-503): on the shifted kg board, `enter` on `Add push notifications`
    paints the section; `tab` moves focus to the links and back without changing the
    board's layout; `x` on the `Waits on` row removes `tm2` from `tm3` (board and
    file) and the section is repainted without it; `x` on the `Unblocks` row removes
    `tm3` from `Offline sync`; `u` brings it back; `↵` on a row closes the view and
    the board's selection is that task; `L` opens the picker and a link made there
    shows in the repainted section; titles holding markup are painted literally.
    RED on base: no dependency painted (P-5)."""
    path = tmp_path / "board.json"
    b = kg_board.shifted(path)
    b.task_by_id("tm4").title = "Offline [b]sync[/b]"
    b.save()
    app = TaskboardApp(board_path=str(path))
    async with app.run_test(size=(118, 40), notifications=True) as pilot:
        await pilot.press("4")
        await pilot.pause()
        layout = app.kanban_presentation
        app.selected_task_id = "tm3"
        await pilot.press("enter")
        await pilot.pause()
        assert isinstance(app.screen, TaskDetails)
        _head, rows, _c = _section(app)
        assert any(r[0] == "d:tm4" and r[2].startswith("Offline [b]sync[/b]") for r in rows)
        box, ol = app.screen.query_one("#details-box"), app.screen.query_one("#deps-list")
        assert box.has_focus
        await pilot.press("tab")
        await pilot.pause()
        assert ol.has_focus and ol.get_option_at_index(ol.highlighted).id == "p:tm2"
        await pilot.press("tab")
        await pilot.pause()
        assert box.has_focus and app.kanban_presentation == layout
        await pilot.press("x")                         # the highlighted Waits-on row
        await pilot.pause()
        assert app.board.task_by_id("tm3").depends_on == []
        saved = {t["id"]: t for t in json.loads(path.read_text(encoding="utf-8"))["tasks"]}
        assert saved["tm3"]["depends_on"] == []
        _head, rows, _c = _section(app)
        assert not any(r[0] == "p:tm2" for r in rows)
        await pilot.press("tab")
        await pilot.pause()
        ol = app.screen.query_one("#deps-list")
        assert ol.get_option_at_index(ol.highlighted).id == "d:tm4"
        await pilot.press("x")
        await pilot.pause()
        assert "tm3" not in app.board.task_by_id("tm4").depends_on
        await pilot.press("escape")
        await pilot.pause()
        await pilot.press("u")
        await pilot.pause()
        assert "tm3" in app.board.task_by_id("tm4").depends_on
        app.selected_task_id = "tm3"                   # `u` selected the task it restored
        await pilot.press("enter")
        await pilot.pause()
        await pilot.press("tab")
        await pilot.pause()
        ol = app.screen.query_one("#deps-list")
        assert ol.get_option_at_index(ol.highlighted).id == "d:tm4"
        await pilot.press("enter")
        await pilot.pause()
        assert not isinstance(app.screen, TaskDetails)
        assert app.selected_task_id == "tm4" and "tm4" in app._line_map
        await pilot.press("enter")
        await pilot.pause()
        await pilot.press("L")
        await pilot.pause()
        await pilot.press(*"rotate")
        await pilot.press("enter")
        await pilot.pause()
        assert isinstance(app.screen, TaskDetails)
        _head, rows, _c = _section(app)
        assert any(r[0] == "p:to2" for r in rows)


async def test_TC_513_rows_paint_done_and_archived_and_the_jump_clears_filters(tmp_path):
    """TC-513 (LLR-503.1, code review T3/T6, battery P17): an open waiter's done and
    archived predecessors are painted as such and the count reads "◂1 open of 3";
    the heading of a waiter whose links are all closed reads "ready"; a jump from
    the details clears a project focus and a search that would hide the target and
    selects it on a drawn row. RED: a jump that keeps the hiding filter."""
    path = tmp_path / "board.json"

    def mutate(b):
        b.task_by_id("tw5").depends_on = ["tw1", "tw4", "ta5"]
        b.task_by_id("ta5").archived = True        # done tw1, open tw4, archived ta5
    b = kg_board.shifted(path)
    mutate(b)
    b.save()
    app = TaskboardApp(board_path=str(path))
    async with app.run_test(size=(118, 40)) as pilot:
        await pilot.press("4")
        await pilot.pause()
        app.selected_task_id = "tw5"
        await pilot.press("enter")
        await pilot.pause()
        _head, rows, _c = _section(app)
        states = {r[0]: r[2].rsplit("· ", 1)[-1] for r in rows if r[0]}
        assert states == {"p:tw1": "done", "p:tw4": "open", "p:ta5": "archived"}
        assert any("◂1 open of 3" in r[2] for r in rows)
        await pilot.press("escape")
        await pilot.pause()
        app.board.task_by_id("tw4").phase = "Done"
        app.selected_task_id = "tw5"
        await pilot.press("enter")
        await pilot.pause()
        assert _section(app)[0].startswith("Dependencies  ready")
        await pilot.press("escape")
        await pilot.pause()
        app.selected_task_id = "tm3"
        app.refresh_view()
        await pilot.press("enter")
        await pilot.pause()
        await pilot.press("tab")
        ol = app.screen.query_one("#deps-list")
        assert ol.get_option_at_index(ol.highlighted).id == "p:tm2"
        app.focused_project_id = "pweb"              # both would hide the target
        app.search_query = "nothing matches this"
        await pilot.press("enter")
        await pilot.pause()
        assert app.focused_project_id is None and app.search_query is None
        assert app.selected_task_id == "tm2" and "tm2" in app._line_map


async def test_TC_513_a_closed_tasks_rows_show_their_own_state(tmp_path):
    """TC-513 (LLR-503.1; code review F1, operator "Corregir en el 003"): the details
    of a task that is itself done (or archived) paint each predecessor's OWN state —
    an open one `open`, a done one `done`, an archived one `archived` — the count
    counts those states ("◂1 open of 3"), and the heading carries neither "waiting"
    nor "ready". RED on frozen r1: the open predecessor painted `done`, "◂0 open of
    3", from `open_predecessors()` (empty for a closed waiter)."""
    path = tmp_path / "board.json"
    b = kg_board.shifted(path)
    b.task_by_id("tw5").depends_on = ["tw1", "tw4", "ta5"]   # done, open, archived
    b.task_by_id("ta5").archived = True
    b.task_by_id("tw5").phase = "Done"
    b.save()
    app = TaskboardApp(board_path=str(path))
    async with app.run_test(size=(118, 40)) as pilot:
        await pilot.press("4")
        await pilot.pause()
        for archived in (False, True):
            app.board.task_by_id("tw5").archived = archived
            app.show_archived = True
            app.selected_task_id = "tw5"
            await pilot.press("enter")
            await pilot.pause()
            head, rows, _c = _section(app)
            states = {r[0]: r[2].rsplit("· ", 1)[-1] for r in rows if r[0]}
            assert states == {"p:tw1": "done", "p:tw4": "open", "p:ta5": "archived"}, archived
            assert any("◂1 open of 3" in r[2] for r in rows), archived
            assert "waiting" not in head and "ready" not in head, (archived, head)
            await pilot.press("escape")
            await pilot.pause()


async def test_TC_513_a_jump_the_view_cannot_draw_is_said(tmp_path):
    """TC-513 (LLR-503.1; code review F3): in a view that does not draw the target
    (Focus draws pinned work only), the jump says so instead of selecting another
    task silently; an archived target with archived hidden says how to see it. RED:
    the jump selecting a neighbour without a word."""
    path = tmp_path / "board.json"
    b = kg_board.shifted(path)
    b.task_by_id("ta5").archived = True
    b.save()
    app = TaskboardApp(board_path=str(path))
    async with app.run_test(size=(118, 40), notifications=True) as pilot:
        await pilot.press("5")
        await pilot.pause()
        app.clear_notifications()
        app.jump_to("tm2")
        await pilot.pause()
        assert any("Audit dependencies is not drawn in this view" in t for t in _toasts(app))
        app.jump_to("ta5")
        await pilot.pause()
        assert any("Plan Q4 roadmap is archived — v shows it" in t for t in _toasts(app))
