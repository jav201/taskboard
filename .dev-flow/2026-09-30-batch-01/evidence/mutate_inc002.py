"""RED counterfactuals for increment 002 (kanban band + badges): one mutation
at a time on taskboard/views.py, run the named nodes, restore the bytes and
prove the restore by SHA-256. Run from the project root:
    python .dev-flow/2026-09-30-batch-01/evidence/mutate_inc002.py
"""
import hashlib
import os
import subprocess
import sys

ROOT = os.getcwd()
VIEWS = os.path.join(ROOT, "taskboard", "views.py")
T = "tests/test_kanban_priority.py"

MUTATIONS = [
    ("K1 band takes done highs",
     "        band_items = [t for t in tasks if t.priority == \"high\"\n                      and not board.is_done(t) and not t.archived]",
     "        band_items = [t for t in tasks if t.priority == \"high\"\n                      and not t.archived]",
     "test_seat_band_skips_done"),
    ("K2 nav forgets the band",
     "today=today, band=presentation == \"grouped\")",
     "today=today, band=False)",
     "test_band_is_drawn_and_nav_walks_the_draw_order or test_the_cursor_walks"),
    ("K3 band also under group=priority",
     "    if band and group != \"priority\":",
     "    if band:",
     "test_seat_band_skips_done"),
    ("K4 badge on finished work",
     "    if (badge and not board.is_done(task) and not task.archived\n            and wc - len(prefix) >= 3):",
     "    if (badge and not task.archived\n            and wc - len(prefix) >= 3):",
     "test_card_badge_per_priority_and_none_when_finished"),
    ("K5 badge never shed",
     "    if (badge and not board.is_done(task) and not task.archived\n            and wc - len(prefix) >= 3):",
     "    if (badge and not board.is_done(task) and not task.archived):",
     "test_badged_cards_are_exactly_their_width"),
    ("K6 legend ignores what is on the board",
     "            if prio in f[\"open_priorities\"]:",
     "            if True:",
     "test_legend_lists_the_badges"),
    ("K7 divider unlabelled",
     "c(\" high \", \"ink\", bold=True)",
     "c(\" top  \", \"ink\", bold=True)",
     "test_band_is_drawn_and_nav_walks_the_draw_order"),
    ("K8 lanes cards unbadged",
     "unblocks=unblocks, badge=True), t.id)\n",
     "unblocks=unblocks, badge=False), t.id)\n",
     "test_the_app_paints_a_badge_on_every_open_card"),
    ("K9 band before the focus filter",
     "    if focus is not None:    # a project focus hides every other project (R-08)\n        tasks = [t for t in tasks if t.project_id == focus]\n    band_items: list[Task] = []\n    if band and group != \"priority\":\n        band_items = [t for t in tasks if t.priority == \"high\"\n                      and not board.is_done(t) and not t.archived]\n        lifted = {id(t) for t in band_items}\n        tasks = [t for t in tasks if id(t) not in lifted]\n",
     "    band_items: list[Task] = []\n    if band and group != \"priority\":\n        band_items = [t for t in tasks if t.priority == \"high\"\n                      and not board.is_done(t) and not t.archived]\n        lifted = {id(t) for t in band_items}\n        tasks = [t for t in tasks if id(t) not in lifted]\n    if focus is not None:    # a project focus hides every other project (R-08)\n        tasks = [t for t in tasks if t.project_id == focus]\n",
     "test_seat_band_respects_the_project_focus"),
    ("K10 seat defaults the band on",
     "                 today=None, band=False) -> list[tuple[str, str, list[Task]]]:",
     "                 today=None, band=True) -> list[tuple[str, str, list[Task]]]:",
     "test_seat_without_band_is_unchanged or test_lanes_and_matrix_draw_no_band"),
]


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def main():
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONUTF8="1")
    for name, old, new, node in MUTATIONS:
        before = open(VIEWS, "rb").read()
        digest = sha(VIEWS)
        text = before.decode("utf-8")
        if text.count(old) != 1:
            print(f"{name}: BAD (anchor matched {text.count(old)} times)")
            continue
        open(VIEWS, "wb").write(text.replace(old, new).encode("utf-8"))
        try:
            r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
                                "--color=no", T, "-k", node],
                               capture_output=True, text=True, env=env, cwd=ROOT)
            tail = [ln for ln in r.stdout.splitlines() if " passed" in ln or " failed" in ln]
        finally:
            open(VIEWS, "wb").write(before)
        ok = sha(VIEWS) == digest
        verdict = "KILLED" if r.returncode != 0 else "SURVIVED"
        print(f"{name}: {verdict} · -k {node!r} · restore sha256 {digest[:16]} ok={ok}")
        for ln in tail[-2:]:
            print("    " + ln)


if __name__ == "__main__":
    main()
