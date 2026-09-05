"""race_probe.py -- the darkside board capture, N times, instrumented.

WHAT THIS IS FOR.  `PENDING.md` (thirty-first pass, ~7628) left the "darkside
capture race" open: one full run in twelve, four checks red, unpainted widgets
positively excluded.  The forty-sixth pass CLOSED that watch for
`prototypes/verify_language.py` -- a stale-width card bake, cured there by
settle's condition C.  What is still open on the same frame is **F-1**
(`.fast-dev-flow/03-increments/inc6.md` section 5): `prototypes/capture_languages.py`
is intermittently non-reproducible and `board_darkside.txt` is one of the four
implicated frames.  That sweep's own `settle()` implements condition B ONLY and
says so in its docstring.  This probe measures what that costs, on darkside,
with numbers instead of a re-run.

IT IS AN INSTRUMENT, NOT A FIX.  Nothing here mutates the app.  Condition C is
asked as a SHADOW render with `update` intercepted (the forty-sixth pass's own
device) so the probe reports a stale bake and never repairs one; a probe that
repaired would mask the class of bug it exists to find.

PER RUN it records: the four-check signature, the wall time and iteration count
of each settle phase, the compositor reflow count at capture, every
BOARD_CONTENT widget the compositor draws with its painted/blank verdict and
its seat width, the InvokeLater queue depth on the board and its cards
(`call_after_refresh` posts an `InvokeLater` to the widget's OWN queue -- that
is the queue the deferred `render_card` sits in), and a hash of the composited
cell grid.

    python -X utf8 prototypes/race_probe.py               # 30 in-process runs
    python -X utf8 prototypes/race_probe.py --sweep       # darkside 7th of ten
    python -X utf8 prototypes/race_probe.py --amplify 50  # the pass-46 lever
    python -X utf8 prototypes/race_probe.py --cross 30    # 30 WHOLE sweeps,
                                                          # 30 processes
    python -X utf8 prototypes/race_probe.py --cross 30 --engine self \
                                            --stable 8 --cond-c

MEASURED, 2026-09-05, HEAD d47abff.  Every in-process arm is 0/30 -- alone,
amplified, and as the seventh language of a ten-language sweep in one
interpreter.  The defect is only visible ACROSS PROCESSES, which is what
`--cross` is for: 22 frames, 30 fresh interpreters, all diffed.  At the shipped
setting six frames drift and two independent sweeps disagree 58.9 % of the
time; at `--stable 8` that is 13.1 %; at `--stable 8 --cond-c` it is 0.0 %.
See `.fast-dev-flow/03-increments/race-probe.md` for the tables and the diffs.

`--amplify MS` is the falsifiability lever, copied from the forty-sixth pass:
it delays `TaskCard`'s deferred re-render so a bake composed at the 20-cell
fallback survives longer.  If the failure is the stale bake, amplifying drives
the rate up; if it is not, amplifying does nothing.  It patches the PROBE's
copy of the app the same way the pass-46 probe did -- the shipped file is not
edited.

Headless stdout belongs in a FILE, never DEVNULL (L-42).  No terminal process
is killed by anything here.
"""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import sys
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "prototypes"))
sys.path.insert(0, str(ROOT / "prototypes" / "widget_slice"))

# capture_languages has an `if __name__ == "__main__"` guard, so importing it
# is safe and gives us the SHIPPED settle constants, the SHIPPED frame reader
# and the SHIPPED clock freeze rather than a second copy that could drift.
import capture_languages as CL                                   # noqa: E402

OUT = ROOT / "prototypes" / "out"

# the classes `KanbanBoard.build()` attaches -- verify_language.py:319, quoted
# rather than re-derived, because the renderer writes these strings
BOARD_CONTENT = ("kb-card", "col-head", "kb-empty", "kb-detail")


def grid_hash(rows: list[str]) -> str:
    return hashlib.sha256("\n".join(rows).encode("utf-8")).hexdigest()[:12]


def stale_paint(card) -> bool:
    """verify_language.py's `_stale_paint`, verbatim in behaviour: ask the card
    what it would draw at its PRESENT seat with `update` intercepted."""
    got: list = []
    card.update = got.append
    try:
        card.render_card()
    finally:
        del card.update
    return bool(got) and got[0] != card.content


def content_widgets(app, rows: list[str]) -> list[dict]:
    """Every BOARD_CONTENT widget the compositor says it is DRAWING, with the
    painted verdict read off the composited frame inside its clipped area."""
    from textual.widgets import Static
    drawn = app.screen._compositor.visible_widgets
    h = len(rows)
    out: list[dict] = []
    for c in app.query(Static):
        if not any(c.has_class(cl) for cl in BOARD_CONTENT):
            continue
        box = drawn.get(c)
        if box is None:
            continue                      # clipped away: evidence of nothing
        area = box[0].intersection(box[1])
        if not (area.width and area.height):
            continue
        painted = any(rows[y][area.x: area.x + area.width].strip()
                      for y in range(area.y, min(area.y + area.height, h)))
        out.append(dict(cls=".".join(sorted(c.classes)),
                        x=area.x, y=area.y, w=area.width, h=area.height,
                        painted=painted, seat=c.size.width,
                        queued=c.message_queue_size,
                        stale=(stale_paint(c) if c.has_class("kb-card")
                               else False)))
    return out


async def settle_instrumented(pilot, app, label: str) -> dict:
    """`capture_languages.settle()` -- condition B, three identical reads --
    reproduced line for line, with a stopwatch and an iteration log.

    Reproduced rather than called because the shipped one returns only the
    rows: the whole question is WHICH iteration it returns on and what the
    widget tree looks like at that instant.
    """
    stable = 0
    prev: list[str] | None = None
    log: list[dict] = []
    t0 = time.perf_counter()
    for i in range(CL.MAX_SETTLE):
        await pilot.pause()
        rows = CL.screen_text(app)
        stable = stable + 1 if rows == prev else 0
        prev = rows
        log.append(dict(i=i, t_ms=round((time.perf_counter() - t0) * 1000, 2),
                        stable=stable, h=grid_hash(rows)))
        if stable < CL.STABLE_READS - 1:
            continue
        blank = not any(r.strip() for r in rows)
        return dict(ok=not blank, blank=blank, timeout=False, iters=i + 1,
                    ms=round((time.perf_counter() - t0) * 1000, 2),
                    rows=rows, log=log)
    return dict(ok=False, blank=False, timeout=True, iters=CL.MAX_SETTLE,
                ms=round((time.perf_counter() - t0) * 1000, 2),
                rows=prev or [], log=log)


async def one_run(idx: int, lang: str, after_pauses: int, amplify: int,
                  in_sweep: bool = False) -> dict:
    from app import TaskboardWidget
    import kanban
    import taskboard.themes as TH

    reflow = Counter()
    # EVERY `render_card` CALL, with the seat it saw.  This is what says
    # whether the 20-cell fallback (`max(8, (size.width or 20) - 2)` = 18) is
    # ever composed on this posture at all -- the pass-46 mechanism -- rather
    # than assumed present or assumed absent.  Records only; the original is
    # always called.
    paints: list[int] = []
    orig_render = kanban.TaskCard.render_card

    def tracing_render(self):
        paints.append(self.size.width)
        return orig_render(self)

    kanban.TaskCard.render_card = tracing_render
    from textual._compositor import Compositor
    orig_reflow = Compositor.reflow

    def counting_reflow(self, *a, **kw):
        reflow["n"] += 1
        return orig_reflow(self, *a, **kw)

    Compositor.reflow = counting_reflow

    # --amplify: widen the window in which a card holds a paint composed at
    # the 20-cell fallback, by delaying the deferred corrective re-render.
    orig_mount = kanban.TaskCard.on_mount
    #
    # It must SCHEDULE the correction later, not sleep inside it.  Measured:
    # a `time.sleep` in the deferred callback blocks the event loop, so
    # `pilot.pause()` cannot return a frame during the delay and settle
    # trivially waits it out -- 0/30 with a 50 ms blocking sleep, settle
    # 1.7-3.2 s per run.  A `set_timer` yields, which is what opens the window
    # the shipped condition B has to survive.
    if amplify:
        def slow_on_mount(self):
            self.render_card()
            self.set_timer(amplify / 1000.0, self.render_card)
        kanban.TaskCard.on_mount = slow_on_mount

    rec: dict = dict(run=idx, lang=lang, amplify=amplify, in_sweep=in_sweep)
    try:
        # --sweep: put the process in the state the SHIPPED sweep is in when
        # it reaches darkside -- six languages already captured, board AND
        # gallery each, in this one interpreter.  The historical evidence is
        # that an isolated loop misses this flake (0/12 at pass 21, 0/30
        # since) while the full sweep hits it about one run in three, so
        # "alone" and "seventh of ten" are different experiments and the
        # probe has to be able to run the second one.
        if in_sweep:
            t_pre = time.perf_counter()
            for pre in TH.ORDER:
                if pre == lang:
                    break
                a2 = TaskboardWidget(board_path=CL.FIXTURE)
                async with a2.run_test(size=CL.SIZE) as p2:
                    await p2.pause()
                    a2.notify = lambda *a, **kw: None
                    a2.set_theme(pre)
                    await CL.settle(p2, a2, f"board {pre}")
                    await p2.press("g")
                    await CL.settle(p2, a2, f"gallery {pre}")
            rec["t_prelude_ms"] = round((time.perf_counter() - t_pre) * 1000, 2)

        t_app = time.perf_counter()
        app = TaskboardWidget(board_path=CL.FIXTURE)
        async with app.run_test(size=CL.SIZE) as pilot:
            await pilot.pause()
            app.notify = lambda *a, **kw: None
            rec["t_boot_ms"] = round((time.perf_counter() - t_app) * 1000, 2)

            t_th = time.perf_counter()
            app.set_theme(lang)
            rec["t_set_theme_ms"] = round((time.perf_counter() - t_th) * 1000, 2)

            s = await settle_instrumented(pilot, app, f"board {lang}")
            rows = s["rows"]
            rec["settle_iters"] = s["iters"]
            rec["settle_ms"] = s["ms"]
            rec["settle_ok"] = bool(s["ok"])
            rec["settle_timeout"] = bool(s["timeout"])
            rec["settle_blank"] = bool(s["blank"])
            rec["settle_log"] = s["log"]
            rec["reflow_at_capture"] = reflow["n"]
            # snapshot BEFORE the widget scan: `stale_paint` calls
            # `render_card` through the tracer, and those shadow calls are the
            # probe's, not the app's.
            rec["paint_seats"] = dict(Counter(paints))
            rec["paints_before_capture"] = len(paints)

            widgets = content_widgets(app, rows)
            rec["widgets"] = widgets
            rec["n_widgets"] = len(widgets)
            rec["n_blank"] = sum(1 for w in widgets if not w["painted"])
            rec["n_stale"] = sum(1 for w in widgets if w["stale"])
            rec["seats"] = sorted({w["seat"] for w in widgets})
            try:
                board = app.query_one(kanban.KanbanBoard)
                rec["board_queue"] = board.message_queue_size
                rec["board_pending_cb"] = len(board._next_callbacks)
            except Exception as e:                       # noqa: BLE001
                rec["board_queue"] = -1
                rec["board_pending_cb"] = f"n/a: {type(e).__name__}"
            rec["card_queue_total"] = sum(w["queued"] for w in widgets)
            rec["app_queue"] = app.message_queue_size

            # THE CAPTURE the sweep would write, hashed the way the sweep's
            # determinism check compares it: the padded rectangle `write()`
            # produces, not the raw rows.
            w = max(len(r) for r in rows)
            rec["grid_hash"] = grid_hash([r.ljust(w) for r in rows])
            rec["ink"] = round(CL.ink([r.ljust(w) for r in rows]), 3)
            rec["rows"] = [r.ljust(w) for r in rows]

            # AND THEN KEEP WATCHING.  If settle signed off early, the frame
            # it signed off on is not the frame the app comes to rest at, and
            # a second process settling one beat later writes a different
            # file.  That is F-1's mechanism stated as a measurement.
            for _ in range(after_pauses):
                await pilot.pause()
            late = CL.screen_text(app)
            lw = max(len(r) for r in late)
            rec["late_hash"] = grid_hash([r.ljust(lw) for r in late])
            rec["late_drift"] = rec["late_hash"] != rec["grid_hash"]
            rec["late_rows"] = [r.ljust(lw) for r in late]
            rec["reflow_after"] = reflow["n"]
    finally:
        Compositor.reflow = orig_reflow
        kanban.TaskCard.on_mount = orig_mount
        kanban.TaskCard.render_card = orig_render
    return rec


def signature(rec: dict) -> tuple[bool, bool, bool, bool]:
    """The four-check signature, one row of the table.

    C1 SETTLED   settle returned, not blank, no timeout
    C2 PAINTED   every drawn BOARD_CONTENT widget carries ink   (condition A)
    C3 FRESH     no card holds a paint composed at a lost seat  (condition C)
    C4 FINAL     the frame settle signed off on is the frame the app rests at
    """
    return (rec["settle_ok"] and not rec["settle_timeout"],
            rec["n_blank"] == 0,
            rec["n_stale"] == 0,
            not rec["late_drift"])


async def main_async(n: int, lang: str, after: int, amplify: int,
                     tag: str, in_sweep: bool) -> int:
    # the same order `sweep()` uses: import the app FIRST, then freeze -- the
    # freeze rebinds the `datetime` NAME inside modules that must already be
    # imported, and raises loudly if it patched nothing.
    import app as _app_mod                              # noqa: F401
    import kanban as _kanban_mod                        # noqa: F401
    CL.freeze_clock()
    recs = []
    for i in range(n):
        rec = await one_run(i, lang, after, amplify, in_sweep)
        recs.append(rec)
        print(f"  run {i:>2}  settle {rec['settle_iters']:>2} it "
              f"{rec['settle_ms']:>7.1f} ms  reflow {rec['reflow_at_capture']:>3}"
              f"->{rec['reflow_after']:<3} widgets {rec['n_widgets']:>2} "
              f"blank {rec['n_blank']} stale {rec['n_stale']} "
              f"seats {rec['seats']} q(board {rec['board_queue']} cards "
              f"{rec['card_queue_total']}) ink {rec['ink']:>6.2f} "
              f"seats@paint {rec['paint_seats']} "
              f"{rec['grid_hash']} -> {rec['late_hash']}"
              f"{'  LATE-DRIFT' if rec['late_drift'] else ''}", flush=True)

    hashes = Counter(r["grid_hash"] for r in recs)
    modal = hashes.most_common(1)[0][0]
    print(f"\n  grid hashes at capture: {dict(hashes)}")
    print(f"  grid hashes after {after} extra pauses: "
          f"{dict(Counter(r['late_hash'] for r in recs))}")

    print("\n  run | C1 settled | C2 painted | C3 fresh | C4 final | hash")
    bad = []
    for r in recs:
        c1, c2, c3, c4 = signature(r)
        flag = "" if (c1 and c2 and c3 and c4 and r["grid_hash"] == modal) \
            else "   <-- FAIL"
        if flag:
            bad.append(r)
        print(f"  {r['run']:>3} | {'PASS' if c1 else 'FAIL':^10} | "
              f"{'PASS' if c2 else 'FAIL':^10} | {'PASS' if c3 else 'FAIL':^8} | "
              f"{'PASS' if c4 else 'FAIL':^8} | {r['grid_hash']}{flag}")

    print(f"\n  FAIL RATE: {len(bad)}/{n}")
    print(f"  C1 settled  failures: {sum(1 for r in recs if not signature(r)[0])}")
    print(f"  C2 painted  failures: {sum(1 for r in recs if not signature(r)[1])}")
    print(f"  C3 fresh    failures: {sum(1 for r in recs if not signature(r)[2])}")
    print(f"  C4 final    failures: {sum(1 for r in recs if not signature(r)[3])}")
    print(f"  hash != modal       : {sum(1 for r in recs if r['grid_hash'] != modal)}")

    # THE DIFF: which CELLS differ, named by row, so the failing grid points
    # at a widget instead of at "the board".
    good = next(r for r in recs if r["grid_hash"] == modal)
    for r in bad:
        print(f"\n  --- run {r['run']}: diff vs the modal grid {modal} ---")
        for y, (a, b) in enumerate(zip(good["rows"], r["rows"])):
            if a != b:
                print(f"    row {y:>2} GOOD |{a}|")
                print(f"    row {y:>2} BAD  |{b}|")
        if len(good["rows"]) != len(r["rows"]):
            print(f"    ROW COUNT good={len(good['rows'])} bad={len(r['rows'])}")
        if r["late_drift"]:
            print(f"    --- and its own late frame {r['late_hash']} ---")
            for y, (a, b) in enumerate(zip(r["rows"], r["late_rows"])):
                if a != b:
                    print(f"    row {y:>2} AT-SETTLE |{a}|")
                    print(f"    row {y:>2} LATE      |{b}|")

    dump = OUT / f"_race_probe_{tag}.json"
    dump.write_text(json.dumps(recs, indent=1), encoding="utf-8")
    print(f"\n  full record -> {dump}")
    return 0 if not bad else 1


async def settle_cond_c(pilot, app, label: str, stable_reads: int) -> list[str]:
    """`capture_languages.settle()` plus verify_language's CONDITION C.

    Condition B (N identical composited reads) with one extra demand: no
    `TaskCard` may be holding a paint composed at a seat it no longer has.
    The staleness is asked as a SHADOW render -- `update` intercepted -- so
    the check measures and never repairs, which is the forty-sixth pass's own
    rule and the reason the answer can be trusted.

    This is the candidate fix, run as an EXPERIMENT.  It is not applied to
    `capture_languages.py` by this probe.
    """
    from kanban import TaskCard
    n = 0
    prev: list[str] | None = None
    for _ in range(CL.MAX_SETTLE):
        await pilot.pause()
        rows = CL.screen_text(app)
        n = n + 1 if rows == prev else 0
        prev = rows
        if n < stable_reads - 1:
            continue
        if any(stale_paint(c) for c in app.query(TaskCard)):
            n = 0                     # a stale bake is not a settled frame
            continue
        if not any(r.strip() for r in rows):
            raise RuntimeError(f"{label}: frame settled BLANK")
        return rows
    raise RuntimeError(f"{label}: never settled after {CL.MAX_SETTLE} frames")


async def sweep_to(dirpath: str, stable: int, extra: int,
                   cond_c: bool = False) -> None:
    """`capture_languages.sweep()` with TWO knobs, and nothing else changed.

    The loop, the writer, the fixture, the clock freeze and the settle are the
    shipped ones -- `CL.settle` is CALLED, not reimplemented -- so
    `--stable 3 --after 0` is the shipped sweep by construction and is the
    honest control arm for any other setting.  `--stable K` raises
    `STABLE_READS`; `--after P` takes P more pauses after settle signs off and
    re-reads the frame.  Both are levers on ONE hypothesis: that the sweep
    writes a frame the app has not finished composing.
    """
    from app import TaskboardWidget
    import taskboard.themes as TH

    CL.freeze_clock()
    out = Path(dirpath)
    out.mkdir(parents=True, exist_ok=True)
    orig_out, orig_stable = CL.OUT, CL.STABLE_READS
    CL.OUT, CL.STABLE_READS = out, stable

    async def _settle(pilot, app, label):
        if cond_c:
            return await settle_cond_c(pilot, app, label, stable)
        return await CL.settle(pilot, app, label)

    try:
        for lang in TH.ORDER:
            app = TaskboardWidget(board_path=CL.FIXTURE)
            async with app.run_test(size=CL.SIZE) as pilot:
                await pilot.pause()
                app.notify = lambda *a, **kw: None
                app.set_theme(lang)
                rows = await _settle(pilot, app, f"board {lang}")
                for _ in range(extra):
                    await pilot.pause()
                if extra:
                    rows = CL.screen_text(app)
                CL.write(f"board_{lang}", rows, app, f"{lang} board")
                await pilot.press("g")
                grows = await _settle(pilot, app, f"gallery {lang}")
                for _ in range(extra):
                    await pilot.pause()
                if extra:
                    grows = CL.screen_text(app)
                CL.write(f"gallery_{lang}", grows, app, f"{lang} components")
    finally:
        CL.OUT, CL.STABLE_READS = orig_out, orig_stable


def cross_process(n: int, tag: str, engine: str = "shipped",
                  stable: int = 3, extra: int = 0,
                  cond_c: bool = False) -> int:
    """The SHIPPED sweep, N times, in N fresh interpreters -- F-1's own
    experiment, run to a temporary directory.

    This is the only arm that can see F-1 as the sweep sees it: the shipped
    determinism check compares ONE sweep against ONE control sweep in a fresh
    process, so the flake is a disagreement BETWEEN PROCESSES and an
    in-process loop cannot express it.  `--sweep-to DIR` is the sweep's own
    control entry point, so this runs the same code path the check runs, and
    it writes into a temp directory -- `prototypes/gallery/` is never touched.
    """
    import subprocess
    import tempfile
    import taskboard.themes as TH
    frames = [f"{sheet}_{lang}.txt"
              for lang in TH.ORDER for sheet in CL.BOARD_SHEETS]
    seen: dict[str, Counter] = {f: Counter() for f in frames}
    texts: dict[str, dict[str, str]] = {f: {} for f in frames}
    if engine == "shipped":
        cmd_head = [sys.executable, "-X", "utf8",
                    str((ROOT / "prototypes" / "capture_languages.py").resolve())]
        cmd_tail: list[str] = []
    else:
        cmd_head = [sys.executable, "-X", "utf8", str(Path(__file__).resolve())]
        cmd_tail = ["--stable", str(stable), "--after-pauses", str(extra)]
        if cond_c:
            cmd_tail.append("--cond-c")
    runs: list[dict[str, str]] = []
    with tempfile.TemporaryDirectory() as td:
        for i in range(n):
            d = Path(td) / f"run{i:02d}"
            d.mkdir()
            t0 = time.perf_counter()
            r = subprocess.run(cmd_head + ["--sweep-to", str(d)] + cmd_tail,
                               capture_output=True, text=True,
                               env={**__import__("os").environ,
                                    "PYTHONIOENCODING": "utf-8"})
            dt = time.perf_counter() - t0
            if r.returncode != 0:
                print(f"  sweep {i:>2} FAILED rc={r.returncode}",
                      r.stderr[-800:], flush=True)
                continue
            hs: dict[str, str] = {}
            for f in frames:
                t = (d / f).read_text(encoding="utf-8")
                h = hashlib.sha256(t.encode("utf-8")).hexdigest()[:12]
                seen[f][h] += 1
                texts[f].setdefault(h, t)
                hs[f] = h
            runs.append(hs)
            print(f"  sweep {i:>2}  {dt:6.1f} s  darkside "
                  f"{seen_hash(texts, 'board_darkside.txt', d)}  "
                  f"distinct so far: "
                  f"{sum(1 for f in frames if len(seen[f]) > 1)} frame(s) "
                  f"drifting", flush=True)

        print("\n  frame                       | distinct grids | counts")
        drift = []
        for f in frames:
            c = seen[f]
            mark = "  <-- DRIFTS" if len(c) > 1 else ""
            if len(c) > 1:
                drift.append(f)
            print(f"  {f:<27} | {len(c):^14} | {dict(c)}{mark}")

        print(f"\n  CROSS-PROCESS DRIFT: {len(drift)}/{len(frames)} frames "
              f"over {n} sweeps -> {drift}")

        # THE NUMBER THE SHIPPED CHECK ACTUALLY PRODUCES.  `main()` compares
        # ONE sweep against ONE control sweep, so its red rate is not the
        # per-frame drift rate: it is the chance that two independent sweeps
        # disagree anywhere.  Both are reported, because only the second one
        # is what the operator sees at the terminal.
        modal_of = {f: seen[f].most_common(1)[0][0] for f in frames}
        odd = [i for i, hs in enumerate(runs)
               if any(hs[f] != modal_of[f] for f in frames)]
        pairs = sum(1 for i in range(len(runs)) for j in range(i + 1, len(runs))
                    if any(runs[i][f] != runs[j][f] for f in frames))
        total_pairs = len(runs) * (len(runs) - 1) // 2 or 1
        print(f"  sweeps that are non-modal on >=1 frame: "
              f"{len(odd)}/{len(runs)} {odd}")
        print(f"  PAIRWISE DISAGREEMENT (what the shipped determinism check "
              f"asks): {pairs}/{total_pairs} pairs = "
              f"{100.0 * pairs / total_pairs:.1f} %")
        for f in drift:
            c = seen[f]
            modal = c.most_common(1)[0][0]
            good = texts[f][modal].split("\n")
            for h, k in c.most_common()[1:]:
                bad = texts[f][h].split("\n")
                print(f"\n  --- {f}: variant {h} (x{k}) vs modal {modal} "
                      f"(x{c[modal]}) ---")
                for y, (a, b) in enumerate(zip(good, bad)):
                    if a != b:
                        print(f"    row {y:>2} MODAL   |{a}|")
                        print(f"    row {y:>2} VARIANT |{b}|")
    return 0 if not drift else 1


def seen_hash(texts, frame, d: Path) -> str:
    t = (d / frame).read_text(encoding="utf-8")
    return hashlib.sha256(t.encode("utf-8")).hexdigest()[:12]


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("-n", type=int, default=30)
    p.add_argument("--lang", default="darkside")
    p.add_argument("--after", type=int, default=12,
                   help="extra pauses after settle, to catch a late frame")
    p.add_argument("--amplify", type=int, default=0,
                   help="ms to delay TaskCard's deferred re-render")
    p.add_argument("--tag", default="plain")
    p.add_argument("--engine", default="shipped",
                   choices=("shipped", "self"),
                   help="which sweep --cross runs: the shipped "
                        "capture_languages.py, or this probe's own sweep "
                        "(same loop, same writer, settle knobs exposed)")
    p.add_argument("--stable", type=int, default=3,
                   help="STABLE_READS for --engine self / --sweep-to")
    p.add_argument("--after-pauses", type=int, default=0, dest="after_pauses",
                   help="extra pauses after settle before the frame is read")
    p.add_argument("--cond-c", action="store_true", dest="cond_c",
                   help="add verify_language's condition C (no TaskCard "
                        "holding a paint composed at a lost seat) to settle")
    p.add_argument("--sweep-to", default="", dest="sweep_to",
                   help="write one full sweep into DIR and say nothing "
                        "(the arm --cross --engine self drives)")
    p.add_argument("--cross", type=int, default=0,
                   help="run the SHIPPED sweep this many times in fresh "
                        "processes and diff every frame (F-1's experiment)")
    p.add_argument("--sweep", action="store_true",
                   help="capture darkside as the SEVENTH language of a full "
                        "ten-language sweep in one process, the way "
                        "capture_languages.py does")
    a = p.parse_args()
    if not a.sweep_to:
        print(f"race_probe | lang={a.lang} n={a.n} viewport {CL.SIZE[0]}x{CL.SIZE[1]}"
          f" | MAX_SETTLE={CL.MAX_SETTLE} STABLE_READS={CL.STABLE_READS}"
              f" | after={a.after} amplify={a.amplify}ms sweep={a.sweep}"
              f" engine={a.engine} stable={a.stable} "
              f"after_pauses={a.after_pauses}")
    if a.sweep_to:
        asyncio.run(sweep_to(a.sweep_to, a.stable, a.after_pauses,
                             a.cond_c))
        return 0
    if a.cross:
        return cross_process(a.cross, a.tag, a.engine, a.stable,
                             a.after_pauses, a.cond_c)
    return asyncio.run(main_async(a.n, a.lang, a.after, a.amplify, a.tag,
                                  a.sweep))


if __name__ == "__main__":
    raise SystemExit(main())
