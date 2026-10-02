"""Mutation battery for an increment of batch 2026-10-02-batch-02 (C-40).

    python <this file> SCRATCH_TREE MUTANTS_JSON

SCRATCH_TREE is an export of the working tree (never the live checkout). Each mutant
is {"id", "file", "old", "new", "nodes": [pytest node ids or -k expressions], "why"}.
For each: the file's sha256 is recorded, the mutation applied (the old text must occur
exactly once, so a typo'd mutant cannot "fail" for the wrong reason), the nodes run
with -rA, ONE VERDICT PER RESOLVED NODE recorded, and the file restored and its sha256
re-checked against the pre-mutation value.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> None:
    tree, spec = Path(sys.argv[1]), json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    killed = 0
    for m in spec:
        f = tree / m["file"]
        before, text = sha(f), f.read_text(encoding="utf-8")
        assert text.count(m["old"]) == 1, (m["id"], "mutation site not unique / absent")
        f.write_text(text.replace(m["old"], m["new"]), encoding="utf-8")
        assert sha(f) != before, (m["id"], "mutation did not apply")
        args = [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", "-rA"]
        for n in m["nodes"]:
            args += (["-k", n[3:]] if n.startswith("-k ") else [n])
        out = subprocess.run(args, cwd=tree, capture_output=True, text=True,
                             encoding="utf-8", errors="replace").stdout
        verdicts = [ln for ln in out.splitlines() if ln.startswith(("PASSED ", "FAILED ", "ERROR "))]
        red = [v for v in verdicts if not v.startswith("PASSED")]
        f.write_text(text, encoding="utf-8")
        restored = sha(f) == before
        status = "KILLED" if red else "SURVIVED"
        killed += bool(red)
        print(f"{m['id']} {status} — {m['why']}")
        print(f"   arms resolved {len(verdicts)}, red {len(red)}; restore sha256 {before[:16]}… "
              f"{'OK' if restored else 'MISMATCH'}")
        for v in verdicts:
            print("   ", v[:160])
        assert restored
    print(f"{killed} of {len(spec)} KILLED")


if __name__ == "__main__":
    main()
