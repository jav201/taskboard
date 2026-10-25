"""Mutation battery + RED counterfactual for increment 001 (batch
2026-10-25-batch-01, LLR-2801.1's negative control, C-40).

One mutant: the background-only declaration deleted from taskboard.tcss
(the RED side of AT-2801..AT-2803; TC-2801 is a labelled pin and must
SURVIVE). Per-arm verdicts; the file's hash is verified restored.
Run from the worktree root: python .dev-flow/2026-10-25-batch-01/evidence/mutation-001.py
"""
import hashlib
import pathlib
import subprocess
import sys

F = pathlib.Path("taskboard/taskboard.tcss")
NODES = [
    ("tests/test_startup_backdrop.py::test_AT_2801_the_offer_opens_over_the_painted_board[size0]", "AT-2801 118x30"),
    ("tests/test_startup_backdrop.py::test_AT_2801_the_offer_opens_over_the_painted_board[size1]", "AT-2801 80x24"),
    ("tests/test_startup_backdrop.py::test_AT_2802_enter_on_the_home_opens_the_offer_over_the_chosen_board[size0]", "AT-2802 118x30"),
    ("tests/test_startup_backdrop.py::test_AT_2802_enter_on_the_home_opens_the_offer_over_the_chosen_board[size1]", "AT-2802 80x24"),
    ("tests/test_startup_backdrop.py::test_AT_2803_team_mode_shows_the_board_behind_both_modals_in_todays_order[size0]", "AT-2803 118x30"),
    ("tests/test_startup_backdrop.py::test_AT_2803_team_mode_shows_the_board_behind_both_modals_in_todays_order[size1]", "AT-2803 80x24"),
    ("tests/test_startup_backdrop.py::test_AT_2803_the_picker_keeps_its_pre_batch_geometry", "AT-2803 geometry"),
    ("tests/test_startup_backdrop.py::test_TC_2801_quitting_with_the_picker_open_writes_nothing", "TC-2801 (pin)"),
]
ANCHOR = (b"/* the start-up modals dim the board like the working modals (D-12), but keep\n"
          b"   their own placement \xe2\x80\x94 the shared rule's align: center middle is NOT wanted\n"
          b"   here (the picker renders top-left; batch 2026-10-25-batch-01, LLR-2801.1) */\n"
          b"MilestoneOffer, TeamIdentityPicker {\n"
          b"    background: #0007;\n"
          b"}\n")
REPLACEMENT = b""

src = F.read_bytes()
h0 = hashlib.sha256(src).hexdigest()
print("arms:", len(NODES), flush=True)
print("before:", h0, flush=True)
assert ANCHOR in src, "mutation anchor not found"
F.write_bytes(src.replace(ANCHOR, REPLACEMENT))
h_mut = hashlib.sha256(F.read_bytes()).hexdigest()
print("mutated:", h_mut, flush=True)
try:
    for node, label in NODES:
        r = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", node],
            capture_output=True, text=True, encoding="utf-8", errors="replace")
        tail = (r.stdout + r.stderr).strip().splitlines()
        verdict = "KILLED" if r.returncode == 1 else (
            "SURVIVED" if r.returncode == 0 else f"BAD({r.returncode})")
        print(f"{label}: {verdict} :: {tail[-1] if tail else 'no output'}",
              flush=True)
finally:
    F.write_bytes(src)
h1 = hashlib.sha256(F.read_bytes()).hexdigest()
print("restored:", h1, flush=True)
print("restore-ok:", h1 == h0, flush=True)
