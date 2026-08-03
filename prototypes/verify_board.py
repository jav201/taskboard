"""Verify the board surface — specifically the failure classes that got past the
earlier verify script: cursor/render divergence, invisible selection, and frame
breakage at widths other than the one we captured at.

Board discipline (the twentieth pass's cure, applied here in the twenty-sixth):
every app in this suite runs on a DETERMINISTIC FIXTURE and every frame read
waits on a CONDITION. Both were missing, and the suite went red once on
`board still readable with animations disabled` — the mounted-but-unpainted
class, on a board the desktop app rewrites underneath the run."""
import asyncio, sys
from pathlib import Path

W = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(W)); sys.path.insert(0, str(W / "prototypes" / "widget_slice"))
from app import TaskboardWidget          # noqa: E402
from kanban import KanbanBoard, TaskCard  # noqa: E402
from taskboard.models import Board        # noqa: E402
from taskboard import motion as MO        # noqa: E402

fails = []
def check(name, cond, detail=""):
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}{'  ' + detail if detail else ''}")
    if not cond: fails.append(name)


def screen_text(app):
    return ["".join(s.text for s in strip)
            for strip in app.screen._compositor.render_strips()]


SETTLE_MAX = 40
# iterations each settle() actually consumed, reported as headroom at the end.
# A gate that passes because its bound is generous is a gate about to rot.
SETTLE_USED: list[int] = []


async def settle(app, pilot, label: str) -> bool:
    """Wait for a frame that is actually PAINTED, not merely produced.

    Same condition `verify_language.settle` waits on, and deliberately a local
    copy: the two suites share no helpers today (each defines its own
    `screen_text`), and importing across them would make either file's probe
    discipline depend on the other's imports.

      A. every card the compositor SAYS it is drawing has painted pixels
         inside its own clipped area
      B. the rendered frame is identical on two consecutive reads

    `visible_widgets` is what makes A sound: a card's `region` is in SCREEN
    space and keeps growing past the fold, so a naive region slice measures
    whatever is at those coordinates (for a card under the fold, the Footer,
    whose text scores as "painted"). The compositor's map holds only the
    widgets it actually draws, each with its clip.

    Where a size class shows no board there are no cards, A is vacuously true,
    and B settles the frame by itself. Bounded, and a timeout is a FAIL."""
    prev = None
    for i in range(SETTLE_MAX):
        rows = screen_text(app)
        h = len(rows)
        drawn = app.screen._compositor.visible_widgets
        painted = True
        for c in app.query(TaskCard):
            box = drawn.get(c)
            if box is None:
                continue               # clipped away: evidence of nothing
            area = box[0].intersection(box[1])
            if not (area.width and area.height):
                continue
            if not any(rows[y][area.x: area.x + area.width].strip()
                       for y in range(area.y, min(area.y + area.height, h))):
                painted = False
                break
        cur = "\n".join(rows)
        if painted and cur == prev:
            SETTLE_USED.append(i + 1)
            return True
        prev = cur
        await pilot.pause()
    # A TIMEOUT IS A FAIL. A capture that silently returns a blank board turns
    # every check reading it into a lie.
    check(f"settle timeout: board never painted ({label})", False,
          f"gave up after {SETTLE_MAX} iterations")
    return False


FX = W / "prototypes" / "out" / "_fixture_board_vb.json"


def seed_fixture() -> Path:
    """The deterministic board every launch below runs on.

    `Board.load` seeds today-anchored demo data on a missing path, so the file
    is re-created from scratch each run. The MIDDLE phase is then emptied into
    the first one, because the cursor checks were written against a live board
    that had an empty column: without that, `right` skipped nothing and the
    check that says so would be vacuously true."""
    FX.parent.mkdir(exist_ok=True)
    if FX.exists():
        FX.unlink()                    # force a fresh, today-anchored seed
    b = Board.load(str(FX))
    mid = b.phases[1]
    for t in b.tasks:
        if t.phase == mid:
            t.phase = b.phases[0]
    b.save()
    return FX


def launch(board_path=None, **kw) -> TaskboardWidget:
    """Every app in this suite is built here, and the fixture is REQUIRED.

    The default stays on the signature only so no call site changes shape;
    passing nothing raises. `TaskboardWidget()` falls back to
    `default_board_path()`, i.e. the user's live board.json — which the
    desktop app rewrites underneath a running suite, making every frame read a
    race against a file this suite does not own. That is the standing suspect
    for the one red this file has produced (PENDING: the live-board probe)."""
    if board_path is None:
        raise ValueError(
            "launch() requires an explicit fixture board_path; probing the "
            "live board.json is forbidden")
    return TaskboardWidget(board_path=board_path, **kw)


async def main():
    print("== PROBE SELF-CHECK (verify the instrument before the verdict)")
    fx = seed_fixture()
    b = Board.load(str(fx))
    n_vis = len(b.visible_tasks(False))
    check("the fixture seeded a board with work on it",
          n_vis > 0 and len(b.phases) >= 3, f"{n_vis} tasks / {b.phases}")
    check("the fixture really leaves a phase with nothing in it",
          not any(t.phase == b.phases[1] for t in b.visible_tasks(False)),
          f"empty phase {b.phases[1]!r}")
    # an unfired guard is a comment
    try:
        launch()
        fired = False
    except ValueError:
        fired = True
    check("launch() refuses to probe the live board (the guard fires)", fired)

    print("\n== CURSOR / RENDER COHERENCE (the class that broke the box-art variants)")
    app = launch(board_path=str(fx))
    async with app.run_test(size=(118, 34)) as pilot:
        await settle(app, pilot, "cursor @118x34")
        kb = app.query_one("#kb", KanbanBoard)
        n_cards = sum(len(c) for c in kb.cards)
        check("board built cards for every visible task",
              n_cards == len(app.board.visible_tasks(False)),
              f"{n_cards} cards / {len(app.board.visible_tasks(False))} tasks")

        # walk DOWN and assert each step lands on the card drawn directly below
        await pilot.press("down"); await settle(app, pilot, "down 0")
        prev = app.focused
        ok_rows, drift = 0, []
        for i in range(8):
            await pilot.press("down"); await settle(app, pilot, f"down {i + 1}")
            cur = app.focused
            if not isinstance(cur, TaskCard) or not isinstance(prev, TaskCard):
                break
            # the NEXT card visually is the one whose region.y is greater
            if cur.region.y > prev.region.y and cur.col == prev.col:
                ok_rows += 1
            else:
                drift.append((prev.item.title[:20], cur.item.title[:20]))
            prev = cur
        check("`down` always moves to the card drawn BELOW", not drift,
              f"{ok_rows} coherent steps" + (f", drift: {drift[:2]}" if drift else ""))

        # the focused card must be ON SCREEN and its title actually rendered
        cur = app.focused
        txt = "\n".join(screen_text(app))
        check("focused task is visible on screen",
              cur.item.title[:18] in txt, repr(cur.item.title[:30]))

        # the hero must be showing the FOCUSED task, not a stale signal
        check("hero followed the cursor",
              app.focused_task is not None and app.focused_task.id == cur.item.id,
              f"hero={getattr(app.focused_task,'title','None')[:24]!r}")

        # horizontal move keeps the row where it can, and skips empty columns
        before = app.focused
        await pilot.press("right"); await settle(app, pilot, "right")
        after = app.focused
        check("`right` lands on a card in a LATER column",
              isinstance(after, TaskCard) and after.col > before.col,
              f"col {before.col} -> {getattr(after,'col','?')}")
        check("`right` skipped the empty phase",
              isinstance(after, TaskCard) and after.col > before.col + 1
              and len(kb.cards[after.col]) > 0,
              f"cards in the skipped column: {len(kb.cards[before.col + 1])}")

    print("\n== FRAME INTEGRITY at widths we did NOT design at")
    for w in (80, 100, 140, 200):
        app = launch(board_path=str(fx))
        async with app.run_test(size=(w, 30)) as pilot:
            await settle(app, pilot, f"frame @{w}x30")
            rows = screen_text(app)
            bad = [len(r) for r in rows if len(r) != w]
            check(f"w={w:<4} every rendered row is exactly {w} cells",
                  not bad, f"{len(bad)} rows off: {sorted(set(bad))[:3]}")
            kb = app.query_one("#kb", KanbanBoard)
            widths = [c.styles.width.value for c in kb.query(".kb-col")]
            check(f"w={w:<4} no column width <= 0", all(x > 0 for x in widths),
                  f"widths={[int(x) for x in widths]}")

    print("\n== DEGRADED MOTION (animation must not be load-bearing)")
    app = launch(board_path=str(fx))
    async with app.run_test(size=(118, 30)) as pilot:
        await settle(app, pilot, "degraded mount @118x30")
        app.animation_level = "none"
        app.engine.run_all(); app.redraw()
        await settle(app, pilot, "degraded redraw @118x30")
        # Probe CONTENT, not a glyph: each language draws with its own glyph
        # family (braille, segments, hairlines...), so asserting on "█" only
        # held for block-based themes — same probe bug the hero check had.
        await pilot.press("down"); await settle(app, pilot, "degraded down")
        txt = "\n".join(screen_text(app))
        cur = app.focused
        check("board still readable with animations disabled",
              "BACKLOG" in txt and isinstance(cur, TaskCard)
              and cur.item.title[:18] in txt,
              repr(getattr(getattr(cur, "item", None), "title", "None")[:24]))

    print("\n== MOTION actually MOVES (a single frame proves nothing)")
    app = launch(board_path=str(fx))
    async with app.run_test(size=(96, 30)) as pilot:
        await settle(app, pilot, "motion mount @96x30")
        # the gantt probe is the PROJECT ROWS (where the packet travels), not a
        # bar glyph — the bar glyphs are per-language now (kit.GANTT). ALL
        # project rows, plural: probing one project re-creates the 1-cell-bar
        # trap the comment below records.
        projs = [p.name[:12] for p in app.board.visible_projects(False)]
        probes = {"gantt": lambda r: any(p in r for p in projs),
                  "agenda": lambda r: "OVERDUE" in r}
        # a FULL PERIOD of the flow packet, not a third of one. motion.build_flow
        # precomputes 20 frames and sweeps the packet across the whole span in
        # those 20, so a short bar is inside the packet's path for only a few of
        # them. The live board happened to carry a project whose bar spanned most
        # of the axis, and 8 ticks caught it; the fixture's projects span weeks,
        # not months, and 8 ticks sampled a stretch of axis their bars never
        # touch. Sampling the period is what the check always meant.
        TICKS = len(MO.build_flow(10))
        for key, name in (("4", "gantt"), ("3", "agenda")):
            await pilot.press(key)
            await settle(app, pilot, f"{name} view")
            frames = []
            for t in range(TICKS):
                app.ticker.advance()
                app.redraw()
                await settle(app, pilot, f"{name} tick {t}")
                # join EVERY matching row: taking the first one picked a
                # 1-cell bar the packet never crosses, and the test reported a
                # static animation that was in fact moving. Test bug, not app bug.
                hit = [r for r in screen_text(app) if probes[name](r)]
                if hit:
                    frames.append("|".join(hit))
            check(f"{name}: animation changes across ticks",
                  len(set(frames)) > 1, f"{len(set(frames))} distinct frames")
        app.animation_level = "none"
        app.redraw()
        await settle(app, pilot, "agenda @none")
        check("view still readable with animation_level=none",
              "AGENDA" in "\n".join(screen_text(app)))

    print("\n== THE GATE ITSELF: settle headroom")
    worst = max(SETTLE_USED) if SETTLE_USED else 0
    check("settle() keeps headroom under its bound (a gate near its limit "
          "is a gate about to rot)",
          worst * 2 <= SETTLE_MAX,
          f"worst {worst} of {SETTLE_MAX} over {len(SETTLE_USED)} settles")

    print("\n" + ("ALL PASSED" if not fails else f"{len(fails)} FAILURE(S): {fails}"))
    sys.exit(1 if fails else 0)

asyncio.run(main())
