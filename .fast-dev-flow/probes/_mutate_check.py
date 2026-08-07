"""C-40: mutate taskboard/views.py FOR REAL, run tests/test_row_cost.py, restore.

Source mutation, not monkeypatch: the test binds `lead_band` at import time, so a
patch applied after collection would leave the test measuring the original while
the renderer used the mutant -- a weaker signal than the thing being claimed.

Every mutation is checked for a UNIQUE anchor before it is applied, and the file
is restored from an in-memory copy in a finally block, then verified byte-equal.
"""
import subprocess, sys, hashlib
from pathlib import Path

VIEWS = Path(__file__).resolve().parents[2] / "taskboard" / "views.py"
TEST = Path(__file__).resolve().parents[2] / "tests" / "test_row_cost.py"

CALL_SITE = "len([ln for ln in lanes if ln.resting]), h - 2 - (2 if active else 0))"
RUNG_FOUR = "prof += max(0, room - best_score[0] - 1)"
MUTANTS = {
    "M1 call site never pays for the lead band":
        (CALL_SITE, CALL_SITE.replace("h - 2 - (2 if active else 0))", "h - 2)")),
    "M2 call site pays for the lead band twice":
        (CALL_SITE, CALL_SITE.replace("(2 if active else 0)", "(4 if active else 0)")),
    "M4 rung four reserves no absence row":
        (RUNG_FOUR, "prof += max(0, room - best_score[0])"),
}

# `return rows` is not unique in views.py, and the file is CRLF, so lead_band's
# own return is located structurally: the first one after its `def`.
LEAD_MUTANTS = {
    "M3 lead_band draws one row more": '    return rows + [("", None)]',
    "M5 lead_band draws one row fewer": "    return rows[:-1]",
}


def mutate_lead_return(src: str, replacement: str) -> str | None:
    start = src.index("def lead_band(")
    for eol in ("\r\n", "\n"):
        anchor = f"{eol}    return rows{eol}"
        i = src.find(anchor, start)
        if i != -1:
            return src[:i] + eol + replacement + eol + src[i + len(anchor):]
    return None


def run_tests():
    p = subprocess.run([sys.executable, "-m", "pytest", str(TEST), "-q", "--no-header",
                        "-p", "no:cacheprovider"],
                       capture_output=True, text=True)
    tail = [l for l in p.stdout.strip().split("\n") if "passed" in l or "failed" in l]
    return p.returncode, (tail[-1] if tail else p.stdout.strip()[-90:])


def main():
    original = VIEWS.read_bytes()
    digest = hashlib.sha256(original).hexdigest()
    src = original.decode("utf-8")
    print(f"views.py sha256 {digest[:16]}  ({len(original)} bytes)\n")
    rc, line = run_tests()
    print(f"{'BASELINE (unmutated)':46s} rc={rc} {line}\n")
    if rc != 0:
        print("baseline is not green -- aborting"); return
    try:
        for name, (old, new) in MUTANTS.items():
            n = src.count(old)
            if n != 1:
                print(f"{name:46s} ANCHOR NOT UNIQUE ({n} matches) -- SKIPPED")
                continue
            VIEWS.write_bytes(src.replace(old, new).encode("utf-8"))
            rc, line = run_tests()
            print(f"{name:46s} rc={rc} {line}   "
                  f"{'<- RED (good)' if rc != 0 else '<- SURVIVED (BAD)'}")
            VIEWS.write_bytes(original)
        for name, repl in LEAD_MUTANTS.items():
            mutated = mutate_lead_return(src, repl)
            if mutated is None:
                print(f"{name:46s} ANCHOR NOT FOUND -- SKIPPED"); continue
            VIEWS.write_bytes(mutated.encode("utf-8"))
            rc, line = run_tests()
            print(f"{name:46s} rc={rc} {line}   "
                  f"{'<- RED (good)' if rc != 0 else '<- SURVIVED (BAD)'}")
            VIEWS.write_bytes(original)
    finally:
        VIEWS.write_bytes(original)
    same = hashlib.sha256(VIEWS.read_bytes()).hexdigest() == digest
    print(f"\nviews.py restored byte-identical: {same}")
    rc, line = run_tests()
    print(f"{'BASELINE (restored)':46s} rc={rc} {line}")


main()
