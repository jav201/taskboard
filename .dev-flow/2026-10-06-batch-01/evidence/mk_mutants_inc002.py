"""Increment 002 mutation battery — kill the cascade wiring's mutants one at a time.

Each mutant patches taskboard/app.py (or keymap.py for K-missing). The harness applies it,
runs tests/test_cascade_app.py, records KILLED / SURVIVED / BAD, restores, hash-verified.

    PYTHONIOENCODING=utf-8 python .dev-flow/2026-10-06-batch-01/evidence/mk_mutants_inc002.py
"""
import hashlib
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(r"C:\Users\jjgh8\Github\taskboard")
APP = ROOT / "taskboard" / "app.py"
KEYMAP = ROOT / "taskboard" / "keymap.py"

MUTANTS = [
    ("N1 the bump bypasses the cascade (the old body)",
     "        self._apply_cascade(task, 0, delta)",
     "        from .models import bump_due as _bd\n"
     "        self._undo_stack.append(self._snapshot(task))\n"
     "        _bd(task, delta, date.today())\n"
     "        self.board.save()\n"
     "        self.refresh_view()"),
    ("N2 one undo entry per task instead of one cascade entry",
     '        self._undo_stack.append({"cascade": {\n'
     '            "task_id": task.id, "sd": sd, "dd": dd, "mode": plan.mode,\n'
     '            "tasks": [{"task_id": i, "fields": {"start_date": s, "due_date": d}}\n'
     '                      for i, (s, d) in snap.items()]}})',
     '        for _i, (_s, _d) in snap.items():\n'
     '            self._undo_stack.append({"task_id": _i, "fields": {"start_date": _s, "due_date": _d}})'),
    ("N3 m cycles the wrong way (push_delta -> flag)",
     "        nxt = CASCADE_MODES[(CASCADE_MODES.index(cas[\"mode\"]) + 1) % len(CASCADE_MODES)]",
     "        nxt = CASCADE_MODES[(CASCADE_MODES.index(cas[\"mode\"]) - 1) % len(CASCADE_MODES)]"),
    ("N4 m never restores first (re-plans from the moved dates)",
     "        self._undo_stack.pop()                 # undo the entry's writes first\n"
     "        for one in cas[\"tasks\"]:\n"
     "            t = self.board.task_by_id(one[\"task_id\"])\n"
     "            if t is not None:\n"
     "                t.start_date = one[\"fields\"][\"start_date\"]\n"
     "                t.due_date = one[\"fields\"][\"due_date\"]",
     "        self._undo_stack.pop()\n"
     "        pass  # no restore: re-plan from the post-move board"),
    ("N5 the toast never names (count rungs only)",
     "        ladder = [(None, 12, True, 0), (None, 12, False, 0), (None, 12, False, 1),\n"
     "                  (None, 8, False, 1), (None, 0, True, 0), (None, 0, True, 1),\n"
     "                  (None, 0, False, 1), (12, 0, False, 1), (6, 0, False, 2)]",
     "        ladder = [(None, 0, False, 1), (6, 0, False, 2)]"),
    ("N6 the flag clause reports totals, not the added days",
     "                    if len(days) == 1:\n"
     "                        return f\"{verb} {names} +{days.pop()}d\"",
     "                    if True:\n"
     "                        return f\"{verb} {names} +{max(plan.conflicts, key=lambda x: x[2])[2]}d\""),
    ("N7 the refusal literal is wrong",
     'self.notify("m re-applies the last date move — nothing to re-apply",',
     'self.notify("nothing to re-apply",'),
    ("N8 m is not bound",
     None, None),  # handled specially: removes the Key line from keymap.py
    ("N9 BAD ANCHOR — the harness must report this mutant as BAD",
     "this text does not exist anywhere in app.py",
     "pass"),
]


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def run_tests():
    env = dict(os.environ)
    env.pop("NO_COLOR", None)
    env.update({"PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1",
                "TERM": "xterm-256color", "COLORTERM": "truecolor"})
    r = subprocess.run([sys.executable, "-m", "pytest", "tests/test_cascade_app.py", "-q",
                        "-p", "no:cacheprovider"], cwd=ROOT, capture_output=True, text=True, env=env)
    tail = [ln for ln in r.stdout.strip().splitlines() if ln.strip()]
    return r.returncode, (tail[-1] if tail else "no output")


KEY_LINE = '    Key("m", "m", "cascade_mode", "Chain", group="date"),'


def main():
    src, ksrc = APP.read_text(encoding="utf-8"), KEYMAP.read_text(encoding="utf-8")
    digest, kdigest = sha(APP), sha(KEYMAP)
    print(f"app.py sha256 before:    {digest}")
    print(f"keymap.py sha256 before: {kdigest}")
    code, last = run_tests()
    assert code == 0 and "passed" in last, f"BASELINE NOT GREEN ({last})"
    print(f"baseline (unmutated): {last}")
    verdicts = {}
    for name, anchor, repl in MUTANTS:
        if name.startswith("N8"):
            KEYMAP.write_text(ksrc.replace(KEY_LINE, "", 1), encoding="utf-8", newline="\n")
            assert sha(KEYMAP) != kdigest
            code, last = run_tests()
            KEYMAP.write_text(ksrc, encoding="utf-8", newline="\n")
            assert sha(KEYMAP) == kdigest
            verdicts[name] = "KILLED" if code else "SURVIVED"
            print(f"{verdicts[name]:8} {name}  [{last}]")
            continue
        if anchor not in src:
            verdicts[name] = "BAD"
            print(f"BAD      {name}  (anchor not found)")
            continue
        APP.write_text(src.replace(anchor, repl, 1), encoding="utf-8", newline="\n")
        assert sha(APP) != digest, f"{name}: mutation did not change the file"
        code, last = run_tests()
        APP.write_text(src, encoding="utf-8", newline="\n")
        assert sha(APP) == digest, f"{name}: restore failed"
        verdicts[name] = "KILLED" if code else "SURVIVED"
        print(f"{verdicts[name]:8} {name}  [{last}]")
    assert sha(APP) == digest and sha(KEYMAP) == kdigest
    print(f"app.py sha256 after:     {sha(APP)}  (restore proven by hash)")
    n_killed = sum(1 for v in verdicts.values() if v == "KILLED")
    n_bad = sum(1 for v in verdicts.values() if v == "BAD")
    survived = [n for n, v in verdicts.items() if v == "SURVIVED"]
    print(f"\n{n_killed} KILLED · {n_bad} BAD (harness proof) · SURVIVED: {survived or 'none'}")


if __name__ == "__main__":
    main()
