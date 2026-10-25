"""Mutation battery — increment 001 (2026-10-24-batch-02).

One node per run; the runner's exit code is that arm's verdict: 1 = RED (KILLED),
0 = GREEN (SURVIVED), anything else = CRASH/BAD. Restores app.py after every arm
and proves the restore by hash. Run from the project root:
    env -u NO_COLOR python .dev-flow/2026-10-24-batch-02/evidence/mutation-001.py
"""
import hashlib
import itertools
import os
import pathlib
import subprocess
import sys

F = pathlib.Path("taskboard/app.py")
NODES = [
    "tests/test_home_deferred_start.py::test_AT_2701_the_home_touches_nothing",
    "tests/test_home_deferred_start.py::test_AT_2702_enter_runs_the_deferred_start",
    "tests/test_home_deferred_start.py::test_AT_2703_escape_runs_the_start_once",
    "tests/test_home_deferred_start.py::test_AT_2704_another_board_never_writes_the_default",
    "tests/test_home_deferred_start.py::test_AT_2705_the_offer_opens_over_the_board",
    "tests/test_home_deferred_start.py::test_TC_2703_a_failed_deferred_start_keeps_the_board_pending",
]
# (anchor, ONE edit) per mutant — the PDR §5 named mutations.
EDITS = [
    (b"            self._mount_board(at_mount=True)\n            self._warn_registry()",
     b"            self._open_board(at_mount=True)\n            self._warn_registry()"),  # E1: the pre-HD-1 mount
    (b"self._offer_milestones()\n        self._started_board = self._started_key()",
     b"self._offer_milestones()"),                                                # E2: no record write
    (b"        self.app._open_board()\n\n    # ---- the boards themselves (HLR-2205)",
     b"\n    # ---- the boards themselves (HLR-2205)"),                          # E3: esc pops without starting
    (b"if not self._migrate_links(at_switch=not at_mount):",
     b"self._started_board = self._started_key()\n        if not self._migrate_links(at_switch=not at_mount):"),  # E4: record before the gate
]
src = F.read_bytes()
h0 = hashlib.sha256(src).hexdigest()
print("arms:", len(NODES) * len(EDITS))
print("before:", h0, flush=True)
assert NODES and EDITS, "no arm to run"
bad = 0
for (old, new), node in itertools.product(EDITS, NODES):
    arm = "%s [%s -> %s]" % (node, old.decode()[:48].replace("\n", "\\n"),
                             new.decode()[:48].replace("\n", "\\n"))
    try:
        if old not in src:
            print(arm + ": BAD (anchor not found in app.py)")
            sys.exit(1)
        F.write_bytes(src.replace(old, new, 1))
        if hashlib.sha256(F.read_bytes()).hexdigest() == h0:
            print(arm + ": BAD (the edit did not apply)")
            sys.exit(1)
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
                            "--color=no", node], env=dict(os.environ, PY_COLORS="0"))
    finally:
        F.write_bytes(src)  # restore, whatever the run did
    h1 = hashlib.sha256(F.read_bytes()).hexdigest()
    print("after: ", h1)
    assert h1 == h0, "the restore is not proven"
    verdict = {1: "RED (KILLED)", 0: "GREEN (SURVIVED)"}.get(r.returncode)
    bad += verdict is None
    print(arm + ":", verdict or "CRASH/BAD (exit %d)" % r.returncode, flush=True)
sys.exit(1 if bad else 0)
