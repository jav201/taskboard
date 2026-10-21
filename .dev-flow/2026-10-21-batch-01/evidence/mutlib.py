"""The batch's mutation runner (batch 2026-10-21-batch-01, the 2026-10-20-batch-03 pattern),
run from the project root with NO_COLOR unset. One edit per arm, one node per run: exit 1 =
RED (KILLED), 0 = GREEN (SURVIVED), anything else = CRASH/BAD. Each file's hash is checked
before and after; the restore is proven, never assumed."""
import hashlib
import os
import pathlib
import subprocess
import sys


def run(arms) -> None:
    env = dict(os.environ)
    env.pop("NO_COLOR", None)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    bad = 0
    for label, path, old, new, node in arms:
        f = pathlib.Path(path)
        src = f.read_bytes()
        text = src.decode("utf-8")
        nl = "\r\n" if "\r\n" in text else "\n"
        o, n = old.replace("\n", nl), new.replace("\n", nl)
        h0 = hashlib.sha256(src).hexdigest()
        if text.count(o) != 1:
            print(f"{label}: BAD (anchor found {text.count(o)} times)", flush=True)
            bad += 1
            continue
        try:
            f.write_bytes(text.replace(o, n, 1).encode("utf-8"))
            r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
                                "--color=no", node], env=env, capture_output=True, text=True,
                               encoding="utf-8", errors="replace", timeout=300)
        finally:
            f.write_bytes(src)
        h1 = hashlib.sha256(f.read_bytes()).hexdigest()
        assert h1 == h0, "the restore is not proven"
        verdict = {1: "RED (KILLED)", 0: "GREEN (SURVIVED)"}.get(r.returncode)
        bad += verdict != "RED (KILLED)"
        tail = (r.stdout.strip().splitlines() or [""])[-1]
        print(f"{label} · {path} · {node.split('::')[1]}: "
              f"{verdict or 'CRASH/BAD (exit %d)' % r.returncode} · sha256 {h0[:12]} restored · {tail}",
              flush=True)
    print("not killed:", bad)
    sys.exit(1 if bad else 0)
