"""Increment 003 mutation battery — kill the editor/setting wiring's mutants.

Each mutant patches taskboard/app.py or taskboard/modals.py, runs
tests/test_cascade_app.py, records KILLED / SURVIVED / BAD, restores, hash-verified.

    PYTHONIOENCODING=utf-8 python .dev-flow/2026-10-06-batch-01/evidence/mk_mutants_inc003.py
"""
import hashlib
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(r"C:\Users\jjgh8\Github\taskboard")
APP = ROOT / "taskboard" / "app.py"
MODALS = ROOT / "taskboard" / "modals.py"

MUTANTS = [
    ("P1 the editor writes dates directly, no cascade",
     "                self._apply_cascade(task, sd, dd, say_solo=False)",
     "                task.start_date, task.due_date = new_start, new_due\n"
     "                self.board.save()"),
    ("P2 the editor toasts every date save (say_solo forced)",
     "                self._apply_cascade(task, sd, dd, say_solo=False)",
     "                self._apply_cascade(task, sd, dd)"),
    ("P3 the milestone branch cascades even on a zero due delta (K returns)",
     "                if dd_eff:",
     "                if True:"),
    ("P4 the undo-entry patch loop removed (TC-633's fix reverted)",
     "                for one in self._undo_stack[-1][\"cascade\"][\"tasks\"]:\n"
     "                    if one[\"task_id\"] == task.id:\n"
     "                        if not sd:\n"
     "                            one[\"fields\"][\"start_date\"] = old_start\n"
     "                        if not dd:\n"
     "                            one[\"fields\"][\"due_date\"] = old_due",
     "                pass"),
    ("P5 resolve_mode repairs junk (coerces instead of defaulting silently)",
     "MODELS:    return v if v in CASCADE_MODES else CASCADE_DEFAULT_MODE",
     "    return (v if v in CASCADE_MODES else CASCADE_DEFAULT_MODE) if not isinstance(v, (int, list)) else \"flag\""),
    ("P6 the picker's carve-out setattr's onto the project (no extra write)",
     '            if k == "date_links":\n'
     "                proj.extra[\"date_links\"] = v\n"
     "                continue",
     "            if k == \"date_links\":\n"
     "                setattr(proj, k, v)\n"
     "                continue"),
    ("P7 the select stores the on-screen label instead of the engine string",
     "            \"date_links\": self._val(\"f-date-links\"),",
     "            \"date_links\": dict(zip(DATE_LINKS_VALUES, DATE_LINKS_LABELS)).get(\n"
     "                self._val(\"f-date-links\"), \"push\"),"),
    ("P8 the silence gate drops the conflicts arm (flag edits go silent)",
     "        if say_solo or len(plan.moved) > 1 or plan.new_conflicts:",
     "        if say_solo or len(plan.moved) > 1:"),
    ("P9 the empty-title guard removed (DS-1 returns)",
     "        if not words:\n            return \"\"",
     "        pass"),
    ("P10 BAD ANCHOR — the harness must report this mutant as BAD",
     "this text does not exist anywhere in app.py",
     "pass"),
]

FILES = {"app.py": APP, "modals.py": MODALS, "models.py": ROOT / "taskboard" / "models.py"}


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def run_tests():
    env = dict(os.environ)
    env.pop("NO_COLOR", None)
    env.update({"PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1",
                "TERM": "xterm-256color", "COLORTERM": "truecolor"})
    r = subprocess.run([sys.executable, "-m", "pytest", "tests/test_cascade_app.py", "-q",
                        "-p", "no:cacheprovider"], cwd=ROOT, capture_output=True, env=env)
    out = (r.stdout or b"").decode("utf-8", "replace")
    tail = [ln for ln in out.strip().splitlines() if ln.strip()]
    return r.returncode, (tail[-1] if tail else "no output")


def main():
    srcs = {n: f.read_text(encoding="utf-8") for n, f in FILES.items()}
    digs = {n: sha(f) for n, f in FILES.items()}
    print("sha256 before:", {n: d[:12] for n, d in digs.items()})
    code, last = run_tests()
    assert code == 0 and "passed" in last, f"BASELINE NOT GREEN ({last})"
    print(f"baseline (unmutated): {last}")
    verdicts = {}
    for name, anchor, repl in MUTANTS:
        target = ("modals.py" if ("DATE_LINKS" in repl or "self._val" in anchor or "proj.extra" in anchor)
                  else "models.py" if anchor.startswith("MODELS:")
                  else "app.py")
        anchor = anchor.removeprefix("MODELS:")
        src, path = srcs[target], FILES[target]
        if anchor not in src:
            verdicts[name] = "BAD"
            print(f"BAD      {name}  (anchor not found in {target})")
            continue
        path.write_text(src.replace(anchor, repl, 1), encoding="utf-8", newline="\n")
        assert sha(path) != digs[target], f"{name}: no change"
        code, last = run_tests()
        path.write_text(src, encoding="utf-8", newline="\n")
        assert sha(path) == digs[target], f"{name}: restore failed"
        verdicts[name] = "KILLED" if code else "SURVIVED"
        print(f"{verdicts[name]:8} {name}  [{last}]")
    for n, f in FILES.items():
        assert sha(f) == digs[n]
    print("sha256 after: ", {n: sha(f)[:12] for n, f in FILES.items()}, " (restore proven)")
    n_killed = sum(1 for v in verdicts.values() if v == "KILLED")
    n_bad = sum(1 for v in verdicts.values() if v == "BAD")
    survived = [n for n, v in verdicts.items() if v == "SURVIVED"]
    print(f"\n{n_killed} KILLED · {n_bad} BAD (harness proof) · SURVIVED: {survived or 'none'}")


if __name__ == "__main__":
    main()
