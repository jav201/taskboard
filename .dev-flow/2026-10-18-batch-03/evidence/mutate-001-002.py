"""The mutation battery of batch 2026-10-18-batch-03 (the 2026-10-18-batch-02 harness, with
this batch's mutants). Run from the root of a SCRATCH COPY of the tree:

    python <this file> <increment>      e.g.  python mutate.py 001

One node per run, so the runner's exit code is that arm's verdict: 1 RED (KILLED),
0 GREEN (SURVIVED), anything else CRASH/BAD. Each edit is printed whole; an edit that
matches nothing, or matches twice, is BAD. Every file is restored after every arm and its
SHA-256 compared with the value before.
"""
from __future__ import annotations

import hashlib
import os
import pathlib
import subprocess
import sys

V = "taskboard/views.py"
A = "taskboard/app.py"
TP = "tests/test_present_polish.py"
TN = "tests/test_present_narrow.py"

SWEEP = f"{TP}::test_TC_2001_the_quiet_marks_are_reached_and_the_rest_stays_dim"
AT1 = f"{TP}::test_AT_2001_the_quiet_marks_read_in_the_running_app"
MUTANTS = {
    "001": [
        ("M1 the view word dim", V,
         'c(f"  {escape(view)}", "reached")', 'c(f"  {escape(view)}", "dim")', [SWEEP, AT1]),
        ("M2 the one-row cut tag dim", V,
         'c(escape(clip(tag, w)), "reached")', 'c(escape(clip(tag, w)), "dim")',
         [f"{TP}::test_TC_2001_a_one_row_cut_is_reached"]),
        ("M3 the cut row dim", V,
         'lines", w)), "reached")', 'lines", w)), "dim")', [SWEEP, AT1]),
        ("M4 the edge marks dim", V,
         'return _pad(c(escape(clip(text, w)), "reached"), w)',
         'return _pad(c(escape(clip(text, w)), "dim"), w)', [SWEEP, AT1]),
        ("M5 the note lead reached", V,
         'lines += [_pad("  " + c("· ", "dim") + r, width)',
         'lines += [_pad("  " + c("· ", "reached") + r, width)', [SWEEP, AT1]),
        ("M6 no notes reached", V,
         'right = c("no notes", "dim")', 'right = c("no notes", "reached")', [SWEEP]),
    ],
    "002": [
        ("N1 no middle wording", A,
         '            ("  ", ("pgdn · " if split else "")\n'
         '             + "⇥ next · ←→ ↑↓ · ␣ hide · a show all · x export · esc"),\n', '',
         [f"{TP}::test_TC_2002_the_middle_wording_sits_between_the_long_and_the_short[gantt-0]",
          f"{TN}::test_TC_1904_the_hint_takes_the_first_wording_that_fits",
          f"{TP}::test_AT_2002_the_80_column_hint_names_next_and_show_all"]),
        ("N2 the middle wording tried first", A,
         '        wordings = (\n            ("  ", ("pgdn notes · " if split else "")',
         '        wordings = (\n            ("  ", ("pgdn · " if split else "")\n'
         '             + "⇥ next · ←→ ↑↓ · ␣ hide · a show all · x export · esc"),\n'
         '            ("  ", ("pgdn notes · " if split else "")',
         [f"{TP}::test_TC_2002_the_middle_wording_sits_between_the_long_and_the_short[split-3]",
          f"{TN}::test_TC_1904_the_hint_takes_the_first_wording_that_fits"]),
        ("N3 the middle gap one space", A,
         '            ("  ", ("pgdn · " if split else "")\n             + "⇥ next',
         '            (" ", ("pgdn · " if split else "")\n             + "⇥ next',
         [f"{TP}::test_TC_2002_the_middle_wording_sits_between_the_long_and_the_short[gantt-10]",
          f"{TP}::test_AT_2002_the_80_column_hint_names_next_and_show_all"]),
        ("N4 the middle keys drop show all", A,
         '"⇥ next · ←→ ↑↓ · ␣ hide · a show all · x export · esc"),',
         '"⇥ next · ←→ ↑↓ · ␣ hide · a all · x export · esc"),',
         [f"{TP}::test_AT_2002_the_80_column_hint_names_next_and_show_all"]),
    ],
    "003": [
        ("K1 the cap stays 3", V,
         "_present_cut(rows, max(3, height - len(lines) - len(open_t)), width - 6)",
         "_present_cut(rows, 3, width - 6)",
         [f"{TP}::test_TC_2003_the_long_note_equals_the_rounds_frame[80-24]",
          f"{TP}::test_TC_2003_the_note_takes_every_free_row_and_declares_its_cut",
          f"{TP}::test_AT_2003_the_gantt_note_runs_to_the_bottom_of_the_frame"]),
        ("K2 the floor dropped", V,
         "max(3, height - len(lines) - len(open_t))", "max(0, height - len(lines) - len(open_t))",
         [f"{TP}::test_TC_2003_the_note_takes_every_free_row_and_declares_its_cut"]),
        ("K3 the briefs not subtracted", V,
         "max(3, height - len(lines) - len(open_t))", "max(3, height - len(lines))",
         [f"{TP}::test_TC_2003_the_long_note_equals_the_rounds_frame[80-24]",
          f"{TP}::test_TC_2003_the_note_takes_every_free_row_and_declares_its_cut",
          f"{TP}::test_AT_2003_the_gantt_note_runs_to_the_bottom_of_the_frame"]),
        ("K4 one row too many", V,
         "max(3, height - len(lines) - len(open_t))", "max(3, height - len(lines) - len(open_t) + 1)",
         [f"{TP}::test_TC_2003_the_long_note_equals_the_rounds_frame[80-24]",
          f"{TP}::test_TC_2003_the_note_takes_every_free_row_and_declares_its_cut"]),
    ],
}


def sha(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def run(node: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
                           "--color=no", node], capture_output=True, text=True,
                          encoding="utf-8", errors="replace",
                          env=dict(os.environ, PY_COLORS="0", PYTHONIOENCODING="utf-8"))


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    inc = sys.argv[1]
    for node in sorted({node for *_, nodes in MUTANTS[inc] for node in nodes}):
        r = run(node)                            # PDR PC-2: a node red before the edit kills nothing
        print(f"pre-check {node}: {'GREEN' if r.returncode == 0 else 'NOT GREEN (exit %d)' % r.returncode}",
              flush=True)
        if r.returncode != 0:
            print("the battery stops: a node is not green on the unmutated tree")
            return 1
    arms = [(name, f, o, n, node) for name, f, o, n, nodes in MUTANTS[inc] for node in nodes]
    print("arms:", len(arms), flush=True)
    bad = killed = 0
    for name, f, old, new, node in arms:
        p = pathlib.Path(f)
        src = p.read_bytes()
        h0 = sha(p)
        text = src.decode("utf-8")
        if "\r\n" in text:                       # a checkout with CRLF line ends
            old, new = old.replace("\n", "\r\n"), new.replace("\n", "\r\n")
        if text.count(old) != 1:
            print(f"{name} · {node}: BAD (anchor matched {text.count(old)} times)", flush=True)
            bad += 1
            continue
        try:
            p.write_bytes(text.replace(old, new, 1).encode("utf-8"))
            assert sha(p) != h0, "the edit did not apply"
            r = run(node)
        finally:
            p.write_bytes(src)
        assert sha(p) == h0, "the restore is not proven"
        verdict = {1: "RED (KILLED)", 0: "GREEN (SURVIVED)"}.get(r.returncode)
        bad += verdict is None
        killed += r.returncode == 1
        tail = (r.stdout.strip().splitlines() or [""])[-1]
        print(f"{name} · {f}: {old!r} -> {new!r}\n    {node}: "
              f"{verdict or 'CRASH/BAD (exit %d)' % r.returncode} · {tail} · restored {h0[:12]}",
              flush=True)
    print(f"killed {killed} / {len(arms)} arms; bad {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
