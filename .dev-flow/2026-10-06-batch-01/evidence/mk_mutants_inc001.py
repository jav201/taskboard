"""Increment 001 mutation battery — kill the cascade engine's mutants one at a time.

Each mutant is a (name, anchor, replacement) textual patch on taskboard/models.py. The harness
applies it, runs tests/test_cascade.py, records KILLED (suite red) / SURVIVED (suite green —
the defect the tests must catch) / BAD (the anchor did not apply — the harness's own
RED-proof), and restores the file, verified by sha256 returning to its pre-run value.

    PYTHONIOENCODING=utf-8 python .dev-flow/2026-10-06-batch-01/evidence/mk_mutants_inc001.py
"""
import hashlib
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(r"C:\Users\jjgh8\Github\taskboard")
MODELS = ROOT / "taskboard" / "models.py"

MUTANTS = [
    ("M1 push_delta repairs old overlaps (strict in disguise)",
     'ov_old = (_cascade_overlap(*_cascade_dates(w), _cascade_dates(pt)[1])\n'
     '                              if mode == "push_delta" else 0)',
     "ov_old = 0"),
    ("M2 done tasks join the cascade",
     "return not board.is_done(t) and not t.archived",
     "return not t.archived"),
    ("M3 a milestone keeps its start delta",
     "    if t.milestone:\n        start_delta = due_delta",
     "    pass"),
    ("M4 resolve_mode ignores the override",
     "    if override in CASCADE_ALL_MODES:\n        return override",
     "    pass"),
    ("M5 new_conflicts carries the TOTAL, not the added days",
     "plan.new_conflicts = [(a, b_, n - before.get((a, b_), 0)",
     "plan.new_conflicts = [(a, b_, n"),
    ("M6 an undated task never bases on today",
     '    if d is None and due_delta:\n        d = today',
     "    pass"),
    ("M7 the start arm drops the +1 (both days no longer count)",
     "return max(0, (pdue - ws).days + 1)",
     "return max(0, (pdue - ws).days)"),
    ("M8 restore writes nothing",
     "        t.start_date, t.due_date = s, d",
     "        pass"),
    ("M9 together never pulls back",
     '    if mode == "together" and due_delta:',
     '    if mode == "together" and due_delta > 0:'),
    ("M10 the downstream is not transitive",
     "                seen.add(w.id)\n                todo.append(w.id)",
     "                seen.add(w.id)"),
    ("M11 BAD ANCHOR — the harness must report this mutant as BAD, never as killed",
     "this text does not exist anywhere in models.py",
     "pass"),
]


def sha():
    return hashlib.sha256(MODELS.read_bytes()).hexdigest()


def run_tests():
    env = dict(os.environ)
    env.pop("NO_COLOR", None)          # greyscale degradation reddens colour asserts for nothing
    env.update({"PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1",
                "TERM": "xterm-256color", "COLORTERM": "truecolor"})
    r = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/test_cascade.py", "-q", "-p", "no:cacheprovider"],
        cwd=ROOT, capture_output=True, text=True, env=env)
    tail = [ln for ln in r.stdout.strip().splitlines() if ln.strip()]
    return r.returncode, (tail[-1] if tail else "no output")


def main():
    src = MODELS.read_text(encoding="utf-8")
    digest = sha()
    print(f"models.py sha256 before: {digest}")
    code, last = run_tests()                 # baseline control: an ungreen baseline makes
    assert code == 0 and "passed" in last, f"BASELINE NOT GREEN ({last}) — every verdict below would be vacuous"
    print(f"baseline (unmutated): {last}  — the suite is green before any mutant")
    verdicts = {}
    for name, anchor, repl in MUTANTS:
        if anchor not in src:
            verdicts[name] = "BAD"
            print(f"BAD      {name}  (anchor not found — the harness reports non-application)")
            continue
        MODELS.write_text(src.replace(anchor, repl, 1), encoding="utf-8", newline="\n")
        assert sha() != digest, f"{name}: mutation did not change the file"
        code, last = run_tests()
        MODELS.write_text(src, encoding="utf-8", newline="\n")
        assert sha() == digest, f"{name}: restore failed"
        verdicts[name] = "KILLED" if code else "SURVIVED"
        print(f"{verdicts[name]:8} {name}  [{last}]")
    assert sha() == digest
    print(f"models.py sha256 after:  {sha()}  (restore proven by hash)")
    n_killed = sum(1 for v in verdicts.values() if v == "KILLED")
    n_bad = sum(1 for v in verdicts.values() if v == "BAD")
    survived = [n for n, v in verdicts.items() if v == "SURVIVED"]
    print(f"\n{n_killed} KILLED · {n_bad} BAD (harness proof) · SURVIVED: {survived or 'none'}")


if __name__ == "__main__":
    main()
