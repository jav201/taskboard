"""Mutation harness of batch 2026-10-19-batch-01.

    python .dev-flow/2026-10-19-batch-01/evidence/mutate.py <increment>   (from the repo root, NO_COLOR unset)

Each mutant replaces one exact source snippet (it must occur exactly once), runs
the named test selection, and restores the file byte for byte (the restore digest
is checked against the digest taken before). KILLED = the selection fails on the
mutant; SURVIVED = it passes. A pre-check refuses to run on a red tree."""
from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

MUTANTS = {
    "001": [
        ("M1 the milestone branch removed (the bar returns)", "taskboard/views.py",
         "    if task.milestone:\n        tone = milestone_tone(task, board, p.today)",
         "    if False:\n        tone = milestone_tone(task, board, p.today)",
         ["tests/test_present_milestone.py"]),
        ("M2 the chip keeps the start date", "taskboard/views.py",
         "chip = \" \" + _present_chip(None, task.due_date, p.today, p.chip_w)",
         "chip = \" \" + _present_chip(task.start_date, task.due_date, p.today, p.chip_w)",
         ["tests/test_present_milestone.py"]),
        ("M3 the cursor's ◆ not accented", "taskboard/views.py",
         "        if cursor:\n            cells = [(\"◆\", \"accent\")",
         "        if False:\n            cells = [(\"◆\", \"accent\")",
         ["tests/test_present_milestone.py"]),
        ("M4 the label's ◆ dropped", "taskboard/views.py",
         "c(\"▎\", p.hue) + \" \" + c(\"◆\", tone) + \" \"",
         "c(\"▎\", p.hue) + \" \" + c(\" \", tone) + \" \"",
         ["tests/test_present_milestone.py"]),
        ("M5 the cursor's ⟦ lead never drawn (code review F1)", "taskboard/views.py",
         "lead = c(\"⟦\", \"accent\", bold=True) if cursor else \" \"",
         "lead = \" \"",
         ["tests/test_present_milestone.py"]),
    ],
}


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _run(tests: list[str]) -> int:
    return subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider",
                           "--color=no", *tests], cwd=ROOT, capture_output=True).returncode


def main(inc: str) -> int:
    muts = MUTANTS[inc]
    selection = sorted({t for *_, ts in muts for t in ts})
    pre = _run(selection)
    print(f"pre-check: {' '.join(selection)} -> exit {pre}")
    if pre != 0:
        print("REFUSED: the selection is red before any mutation")
        return 2
    killed = 0
    for name, rel, old, new, tests in muts:
        path = ROOT / rel
        before = _digest(path)
        raw = path.read_bytes()
        text = raw.decode("utf-8")
        nl = "\r\n" if "\r\n" in text else "\n"
        o, n = old.replace("\n", nl), new.replace("\n", nl)
        assert text.count(o) == 1, (name, text.count(o))
        try:
            path.write_bytes(text.replace(o, n).encode("utf-8"))
            code = _run(tests)
        finally:
            path.write_bytes(raw)
        assert _digest(path) == before, name
        verdict = "KILLED" if code != 0 else "SURVIVED"
        killed += code != 0
        print(f"{name} · {rel} · {' '.join(tests)} -> exit {code} · {verdict} · restore digest {before}")
    print(f"{killed}/{len(muts)} KILLED")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
