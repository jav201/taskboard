"""Mutation battery for batch 2026-10-16-batch-01 (byte-level, restore-verified).

    python .dev-flow/2026-10-16-batch-01/evidence/mutate.py <increment>

Each mutant replaces ONE exact byte string (it must occur exactly once) in one
source file, runs the named test nodes, records KILLED (the run fails) or SURVIVED
(it passes), restores the original bytes and verifies their SHA-256. The battery's
transcript is printed; redirect it into `mutation-<inc>.txt`.
"""
from __future__ import annotations

import hashlib
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

M001 = [
    ("M1", "taskboard/views.py",
     "dcells, meta = gantt_day_row(ax, today, echo, shade_weekends=False)",
     "dcells, meta = gantt_day_row(ax, today, echo, shade_weekends=True)",
     ["tests/test_present_rulers.py::test_TC_1601_the_ruler_rows_their_colours_and_no_weekend"]),
    ("M2", "taskboard/views.py", "    chip_w = 13\n", "    chip_w = 12\n",
     ["tests/test_present_rulers.py::test_TC_1602_the_oracle_boards_chips_whole_at_both_sizes",
      "tests/test_present.py::test_TC_1001_the_exact_presc_frame_at_118x30"]),
    ("M3", "taskboard/views.py",
     '        return f"{_md(start)}–{due.day}"', '        return f"{_md(start)}–{_md(due)}"',
     ["tests/test_present_rulers.py::test_TC_1602_the_span_label_cases"]),
    ("M4", "taskboard/views.py",
     "    echo = gantt_echo(cursor, board, ax, today) if cursor is not None else None\n",
     "    echo = gantt_echo(cursor, board, ax, today) if cursor is not None else None\n"
     "    echo = (echo[0], 'bright', echo[2], echo[3]) if echo else None\n",
     ["tests/test_present_rulers.py::test_TC_1601_the_ruler_rows_their_colours_and_no_weekend"]),
    ("M5", "taskboard/views.py",
     'p.label_w - 1, "right") + " ", "accent")', 'p.label_w - 1, "right") + " ", "bright")',
     ["tests/test_present_rulers.py::test_TC_1601_the_ruler_rows_their_colours_and_no_weekend"]),
    ("M6", "taskboard/views.py",
     "    lines += _present_ruler(proj, board, p, cursor)\n", "",
     ["tests/test_present_rulers.py::test_AT_1601_R_paints_the_ruler_and_the_dates_follow_the_cursor",
      "tests/test_present.py::test_AT_1001_R_presents_the_project_and_the_frame_is_the_oracle"]),
    ("M7", "taskboard/views.py",
     '    elif d is not None and d < today:\n        tone = "over"',
     '    elif d is not None and d < today:\n        tone = "mut"',
     ["tests/test_present_rulers.py::test_TC_1602_the_chip_tones_and_an_unparseable_date"]),
    ("M8", "taskboard/views.py",
     'p.label_w - 1, "right") + " ",\n                   echo[1], bold=True)',
     'p.label_w - 1, "right") + " ",\n                   "dim", bold=True)',
     ["tests/test_present_rulers.py::test_TC_1601_an_echo_too_long_for_the_field_moves_to_the_label"]),
]

BATTERIES = {"001": M001}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def run(nodes: list[str]) -> tuple[int, str]:
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *nodes],
                       cwd=ROOT, capture_output=True, text=True, encoding="utf-8", env=env)
    tail = [ln for ln in r.stdout.splitlines() if ln.strip()][-1:]
    return r.returncode, tail[0] if tail else ""


def main(inc: str) -> int:
    failed = 0
    for mid, rel, old, new, nodes in BATTERIES[inc]:
        path = ROOT / rel
        orig = path.read_bytes()
        digest = sha(path)
        text = orig.decode("utf-8")
        if chr(13) + chr(10) in text:            # the working copy is CRLF: match it
            old = old.replace(chr(10), chr(13) + chr(10))
            new = new.replace(chr(10), chr(13) + chr(10))
        if text.count(old) != 1:
            print(f"{mid} {rel}: anchor occurs {text.count(old)}x — NOT APPLIED")
            failed += 1
            continue
        try:
            path.write_bytes(text.replace(old, new).encode("utf-8"))
            code, tail = run(nodes)
        finally:
            path.write_bytes(orig)
        assert sha(path) == digest, f"{mid}: restore digest mismatch"
        verdict = "KILLED" if code != 0 else "SURVIVED"
        failed += verdict == "SURVIVED"
        print(f"{mid} {rel}: {old.strip()[:60]!r} -> {new.strip()[:60]!r} · {verdict} · {tail} "
              f"· restore sha256 {digest}")
    return failed


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
