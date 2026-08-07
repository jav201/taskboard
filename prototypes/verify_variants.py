"""VERIFY the prototypes the way tui-design/VERIFY.md demands:
  * DRIVE check  — boot the REAL app, cycle every variant, assert on runtime values
  * RENDER check — assert each variant produced real, non-blank content
  * BUDGET       — measure each variant's render cost (tui-design/BUDGET.md)

    python prototypes/verify_variants.py
"""
from __future__ import annotations

import asyncio
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import kanban_variants as KV               # noqa: E402  (installs the patch)
from taskboard.models import Board   # noqa: E402

# Synthetic on purpose: this benchmark used to time renders of the operator's
# live board, so its numbers moved with private data nobody reading them could
# see, and its output named real tasks. Same fixture the captures use.
FIXTURE = ROOT / "prototypes" / "out" / "_fixture_late.json"

W, H = 118, 30
CELLS = W * H
N = 30

fails: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}{'  ' + detail if detail else ''}")
    if not cond:
        fails.append(name)


async def drive_check() -> None:
    print("\n== DRIVE check (real app, real data, real bindings)")
    App = KV.build_app()
    app = App()
    async with app.run_test(size=(W, H + 2)) as pilot:
        await pilot.pause()
        check("app boots in kanban mode", app.view_mode == "kanban",
              f"view_mode={app.view_mode}")
        check("a task is selected on mount", app.selected_task_id is not None,
              f"id={app.selected_task_id}")

        seen = set()
        for i in range(len(KV.VARIANTS)):
            label, _ = KV.VARIANTS[KV._state["i"] % len(KV.VARIANTS)]
            # Read the RASTERISED cells, not the source renderable — VERIFY.md
            # requires asserting on what actually rendered.
            from textual.geometry import Region
            board_w = app.query_one("#board")
            strips = board_w.render_lines(
                Region(0, 0, board_w.size.width, board_w.size.height))
            rows = [s.text for s in strips if s.text.strip()]
            text = "\n".join(rows)
            body = [r for r in rows if r.strip("│╭╮╰╯─┬┴┼├┤ ")]
            check(f"variant {label}: renders non-blank body",
                  len(body) >= 5, f"{len(body)} content rows")
            seen.add(text[:400])
            await pilot.press("V")
            await pilot.pause()

        check("every variant renders a DIFFERENT screen",
              len(seen) == len(KV.VARIANTS), f"{len(seen)} distinct of {len(KV.VARIANTS)}")

        # navigation must still work while a variant is mounted
        before = app.selected_task_id
        await pilot.press("down")
        await pilot.pause()
        check("cursor still moves under a variant",
              app.selected_task_id != before,
              f"{before} -> {app.selected_task_id}")


def budget_check() -> None:
    print("\n== BUDGET (tui-design/BUDGET.md)")
    if not FIXTURE.exists():
        raise SystemExit(f"FIXTURE MISSING: {FIXTURE}")
    board = Board.load(FIXTURE)
    tasks = board.visible_tasks(False)
    sel = tasks[len(tasks) // 3].id if tasks else None
    frame60 = 1e6 / 60

    print(f"  {'variant':<14}{'median us':>11}{'us/cell':>10}{'% 60fps frame':>16}")
    for label, fn in KV.VARIANTS:
        render = fn or KV._BASELINE
        samples = []
        for _ in range(N):
            t0 = time.perf_counter()
            render(board, False, sel, None, W, H, {}, "grouped")
            samples.append(time.perf_counter() - t0)
        med = statistics.median(samples) * 1e6
        print(f"  {label:<14}{med:>11.1f}{med / CELLS:>10.3f}"
              f"{med / frame60 * 100:>15.2f}%")
        check(f"variant {label} within frame budget (H>=5)",
              med < frame60 / 5, f"{med:.0f}us vs {frame60/5:.0f}us ceiling")


async def main() -> None:
    await drive_check()
    budget_check()
    print("\n" + ("ALL CHECKS PASSED" if not fails
                  else f"{len(fails)} FAILURE(S): {fails}"))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    asyncio.run(main())
