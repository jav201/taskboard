"""Mutation battery for batch 2026-10-17-batch-01, increment 001 (restore-verified).

    python .dev-flow/2026-10-17-batch-01/evidence/mutate.py <tree root>

Run against a tree no other session is reading (the increment ran it in a
scratch `git worktree` holding the increment's exact bytes, while the full
suite ran in the checkout). Each mutant replaces ONE exact byte string (it must
occur exactly once) in `taskboard/views.py`, runs each named node on its own,
records one verdict per node — KILLED (exit 1), SURVIVED (exit 0), BAD (any
other code) — restores the original bytes and verifies their SHA-256. The arm
count is asserted before any verdict is trusted. Redirect into `mutation-001.txt`.
"""
from __future__ import annotations

import hashlib
import os
import subprocess
import sys
from pathlib import Path

T = "tests/test_tick_label.py::"
MUTANTS = [
    ("M1", 'the no-selection branch returns text',
     b'"right") + " ", "dim")\n    return ""\n',
     b'"right") + " ", "dim")\n    return "Mondays \xc2\xb7 1 cell = 1 day"\n',
     [T + "test_TC_1701_gantt_dateless_and_no_selection[118-30]",
      T + "test_TC_1701_present_follows_the_same_rule[118-30]",
      T + "test_TC_1701_the_label_function_branches",
      T + "test_TC_1701_no_gantt_frame_paints_the_scale[118-30]",
      T + "test_AT_1701_a_board_with_no_task_has_a_blank_label[size0]"]),
    ("M2", 'the echo branch paints dim, not the echo tone',
     b'"right") + " ", echo[1], bold=True)',
     b'"right") + " ", "dim", bold=True)',
     [T + "test_TC_1701_gantt_names_the_selected_task[118-30]",
      T + "test_TC_1701_the_label_function_branches"]),
    ("M3", 'the dateless branch paints the over tone, not dim',
     b'fit("selected: no dates", label_w - 1, "right") + " ", "dim")',
     b'fit("selected: no dates", label_w - 1, "right") + " ", "over")',
     [T + "test_TC_1701_gantt_dateless_and_no_selection[118-30]",
      T + "test_TC_1701_the_label_function_branches"]),
    ("M4", 'a too-long echo is labelled "selected task" anyway',
     b'text = meta["echo_label"] or "selected task"',
     b'text = "selected task"',
     [T + "test_TC_1701_gantt_too_long_echo_keeps_its_dates[118-30]",
      T + "test_TC_1701_present_follows_the_same_rule[118-30]"]),
    ("M5", 'a dateless selection is treated as no selection',
     b'    if selected is not None:\n        return c(fit("selected: no dates"',
     b'    if False:\n        return c(fit("selected: no dates"',
     [T + "test_TC_1701_gantt_dateless_and_no_selection[118-30]",
      T + "test_TC_1701_present_follows_the_same_rule[80-24]"]),
    ("M6", 'the gantt view passes no selection to the label',
     b'dlabel = _gantt_tick_label(sel, echo, dmeta, label_w)',
     b'dlabel = _gantt_tick_label(None, None, dmeta, label_w)',
     [T + "test_TC_1701_gantt_names_the_selected_task[118-30]",
      T + "test_TC_1701_link_mode_names_the_candidate[118-30]",
      T + "test_AT_1701_the_tick_row_names_the_selection[size0]"]),
    ("M7", 'the presentation passes no cursor to the label',
     b'dlabel = _gantt_tick_label(cursor, echo, meta, p.label_w)',
     b'dlabel = _gantt_tick_label(None, None, meta, p.label_w)',
     [T + "test_TC_1701_present_follows_the_same_rule[118-30]",
      "tests/test_present_room.py::test_TC_1608_the_tick_row_names_the_selected_task[118-30]",
      T + "test_AT_1701_the_tick_row_names_the_selection[size1]"]),
]


def main(root: Path) -> int:
    f = root / "taskboard" / "views.py"
    src = f.read_bytes()
    h0 = hashlib.sha256(src).hexdigest()
    arms = sum(len(m[4]) for m in MUTANTS)
    print("tree:", root)
    print("arms:", arms, "over", len(MUTANTS), "mutants")
    assert arms == 19, arms
    print("before:", h0, flush=True)
    eol = b"\r\n" if b"\r\n" in src else b"\n"      # a checkout with core.autocrlf
    print("line ending:", "CRLF" if eol == b"\r\n" else "LF")
    bad = 0
    for mid, what, old, new, nodes in MUTANTS:
        old, new = old.replace(b"\n", eol), new.replace(b"\n", eol)
        assert src.count(old) == 1, (mid, src.count(old))
        print(f"\n== {mid}: {what}", flush=True)
        for node in nodes:
            try:
                f.write_bytes(src.replace(old, new, 1))
                if hashlib.sha256(f.read_bytes()).hexdigest() == h0:
                    print(f"{mid} {node}: BAD (the edit did not apply)")
                    return 1
                r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
                                    "--color=no", node], cwd=root, capture_output=True, text=True,
                                   encoding="utf-8", errors="replace",
                                   env=dict(os.environ, PY_COLORS="0",
                                            PYTHONDONTWRITEBYTECODE="1"))
            finally:
                f.write_bytes(src)
            h1 = hashlib.sha256(f.read_bytes()).hexdigest()
            assert h1 == h0, "the restore is not proven"
            tail = (r.stdout.strip().splitlines() or ["(no output)"])[-1]
            verdict = {1: "KILLED", 0: "SURVIVED"}.get(r.returncode)
            bad += verdict != "KILLED"
            print(f"{mid} {node}: {verdict or 'BAD (exit %d)' % r.returncode} -- {tail}",
                  flush=True)
            print("  after:", h1)
    print("\nafter all:", hashlib.sha256(f.read_bytes()).hexdigest())
    print("not killed:", bad)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1]).resolve()))
