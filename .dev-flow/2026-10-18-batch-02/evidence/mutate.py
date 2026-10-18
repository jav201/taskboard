"""The mutation battery of batch 2026-10-18-batch-02 (the runbook's harness,
with a file per mutant). Run from the root of a SCRATCH COPY of the tree:

    python <this file> <increment>      e.g.  python mutate.py 001

One node per run, so the runner's exit code is that arm's verdict: 1 RED
(KILLED), 0 GREEN (SURVIVED), anything else CRASH/BAD. Each edit is printed
whole; an edit that matches nothing, or matches twice, is BAD. Every file is
restored after every arm and its SHA-256 compared with the value before.
"""
from __future__ import annotations

import hashlib
import os
import pathlib
import subprocess
import sys

TV = "tests/test_team_views.py"
TA = "tests/test_app.py"
V = "taskboard/views.py"
A = "taskboard/app.py"
TN = "tests/test_present_narrow.py"

MUTANTS = {
    "001": [
        ("M1 own row muted", V,
         "# the operator's own row is identifiable by a bright spine\n"
         '        prefix = c("▌", "bright") + " " if is_self',
         "# the operator's own row is identifiable by a bright spine\n"
         '        prefix = c("▌", "bright") + " " if not is_self',
         [f"{TV}::test_standup_renders_one_row_per_member_and_own_row_identifiable",
          f"{TV}::test_AT_1901_the_standup_marks_the_operators_own_row"]),
        ("M2 stale tone on every row", V,
         "tone = sync_tone(team_state, uid)\n        # the operator's own row",
         "tone = \"over\"\n        # the operator's own row",
         [f"{TV}::test_standup_flags_stale_member_in_over_tone"]),
        ("M3 name column 13", V,
         "name_w = min(12, max(4,", "name_w = min(13, max(4,",
         [f"{TV}::test_TC_1901_the_name_column_cuts_at_twelve_cells"]),
        ("M4 skip keyed on the last attempt (PC-1)", TA,
         "    assert not seeded, (", "    assert refusal is not None, (",
         [f"{TA}::test_TC_1902_the_roundtrip_verdict[contended-then-refused-x4]"]),
        ("M5 a refusal raises", TA,
         '    return (f"Set-Clipboard refused the sample',
         '    raise AssertionError(f"Set-Clipboard refused the sample',
         [f"{TA}::test_TC_1902_the_roundtrip_verdict[refused-x5]",
          f"{TA}::test_AT_1902_a_refused_setup_skips_with_its_reason"]),
        ("M6 contention returns a reason", TA,
         "    assert not seeded, (", "    assert True or not seeded, (",
         [f"{TA}::test_TC_1902_the_roundtrip_verdict[contended-x5]",
          f"{TA}::test_TC_1902_the_roundtrip_verdict[refused-x4-then-contended]",
          f"{TA}::test_TC_1902_the_roundtrip_verdict[contended-then-refused-x4]"]),
        ("M7 a mismatch passes", TA,
         "        assert got == sample, (", "        assert True, (",
         [f"{TA}::test_TC_1902_a_held_sample_read_wrong_is_the_handle_bug"]),
        ("M8 the skip becomes a failure", TA,
         "    if reason is not None:\n        pytest.skip(reason)",
         "    if reason is not None:\n        pytest.fail(reason)",
         [f"{TA}::test_AT_1902_a_refused_setup_skips_with_its_reason"]),
    ],
    "002": [
        ("N1 the floor at 35", V, "PRESENT_MIN_WIDTH = 36 ", "PRESENT_MIN_WIDTH = 35 ",
         [f"{TN}::test_TC_1903_every_width_renders_a_whole_frame",
          f"{TN}::test_AT_1903_narrowed_the_presentation_says_how_wide_and_waits"]),
        ("N2 the floor at 37", V, "PRESENT_MIN_WIDTH = 36 ", "PRESENT_MIN_WIDTH = 37 ",
         [f"{TN}::test_TC_1903_every_width_renders_a_whole_frame"]),
        ("N3 a rung dropped", V, '"needs {}+ cols", ', "",
         [f"{TN}::test_TC_1903_every_width_renders_a_whole_frame",
          f"{TN}::test_AT_1903_narrowed_the_presentation_says_how_wide_and_waits"]),
        ("N4 the rung in dim", V, 'escape(fit(msg, width)), "mut")', 'escape(fit(msg, width)), "dim")',
         [f"{TN}::test_TC_1903_every_width_renders_a_whole_frame"]),
        ("N5 no compact wording", A, '            (" ", ("pgdn " if split else "") + "⇥ ←→ ␣ x esc"),\n', "",
         [f"{TN}::test_TC_1904_the_hint_takes_the_first_wording_that_fits",
          f"{TN}::test_AT_1904_the_hint_shortens_and_cuts_visibly"]),
        ("N6 the narrow hint uncut", A,
         '            hint.truncate(room, overflow="ellipsis")\n            return hint',
         "            return hint",
         [f"{TN}::test_TC_1904_the_hint_takes_the_first_wording_that_fits",
          f"{TN}::test_AT_1904_the_hint_shortens_and_cuts_visibly"]),
        ("N7 the wide hint uncut (PC-2)", A,
         '        hint.truncate(room, overflow="ellipsis")\n        return hint',
         "        return hint",
         [f"{TN}::test_TC_1904_an_overflowing_count_is_cut_visibly"]),
        ("N8 no zero-budget guard", A, "        if room <= 0:\n            return Text()",
         "        if False:\n            return Text()",
         [f"{TN}::test_TC_1904_the_hint_takes_the_first_wording_that_fits"]),
        ("N9 the narrow hint keeps the names", A,
         '        if w < PRESENT_MIN_WIDTH:\n            hint = Text("esc leave"',
         '        if False:\n            hint = Text("esc leave"',
         [f"{TN}::test_TC_1904_the_hint_takes_the_first_wording_that_fits",
          f"{TN}::test_AT_1904_the_hint_shortens_and_cuts_visibly"]),
        ("N10 space acts when narrow", A,
         'the previous one at the end)."""\n        if self._narrow():\n            return',
         'the previous one at the end)."""',
         [f"{TN}::test_AT_1903_narrowed_the_presentation_says_how_wide_and_waits"]),
        ("N11 a acts when narrow", A,
         'nothing written."""\n        if self._narrow():\n            return',
         'nothing written."""',
         [f"{TN}::test_AT_1903_narrowed_the_presentation_says_how_wide_and_waits"]),
        ("N12 the view keys act when narrow", A,
         'scrolled back to the top."""\n        if self._narrow():\n            return',
         'scrolled back to the top."""',
         [f"{TN}::test_AT_1903_narrowed_the_presentation_says_how_wide_and_waits"]),
        ("N13 the moves act when narrow", A,
         "def action_move(self, delta: int) -> None:\n        if self._narrow():\n            return",
         "def action_move(self, delta: int) -> None:",
         [f"{TN}::test_AT_1903_narrowed_the_presentation_says_how_wide_and_waits"]),
        ("N14 x exports when narrow", A,
         "        if self._narrow():\n            self.app.notify(",
         "        if False:\n            self.app.notify(",
         [f"{TN}::test_AT_1903_narrowed_the_presentation_says_how_wide_and_waits"]),
        ("N15 pgdn acts when narrow (a declared regression pin)", A,
         '`pgup` answers at once."""\n        if self._narrow():\n            return',
         '`pgup` answers at once."""',
         [f"{TN}::test_AT_1903_narrowed_the_presentation_says_how_wide_and_waits"]),
    ],
}


def sha(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    inc = sys.argv[1]
    arms = [(name, f, o, n, node) for name, f, o, n, nodes in MUTANTS[inc] for node in nodes]
    print("arms:", len(arms), flush=True)
    bad = 0
    killed = 0
    for name, f, old, new, node in arms:
        p = pathlib.Path(f)
        src = p.read_bytes()
        h0 = sha(p)
        text = src.decode("utf-8")
        if "\r\n" in text:                       # a checkout with CRLF line ends
            old, new = old.replace("\n", "\r\n"), new.replace("\n", "\r\n")
        if text.count(old) != 1:
            print(f"{name} · {node}: BAD (anchor matched {text.count(old)} times)", flush=True)
            bad += 1
            continue
        try:
            p.write_bytes(text.replace(old, new, 1).encode("utf-8"))
            assert sha(p) != h0, "the edit did not apply"
            r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
                                "--color=no", node], capture_output=True, text=True,
                               encoding="utf-8", errors="replace",
                               env=dict(os.environ, PY_COLORS="0", PYTHONIOENCODING="utf-8"))
        finally:
            p.write_bytes(src)
        assert sha(p) == h0, "the restore is not proven"
        verdict = {1: "RED (KILLED)", 0: "GREEN (SURVIVED)"}.get(r.returncode)
        bad += verdict is None
        killed += r.returncode == 1
        tail = (r.stdout.strip().splitlines() or [""])[-1]
        print(f"{name} · {f}: {old!r} -> {new!r}\n    {node}: "
              f"{verdict or 'CRASH/BAD (exit %d)' % r.returncode} · {tail} · restored {h0[:12]}",
              flush=True)
    print(f"killed {killed} / {len(arms)} arms; bad {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
