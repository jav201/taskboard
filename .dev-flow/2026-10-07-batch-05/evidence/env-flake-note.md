# Environmental note — the 20 "failures" of inc-001's full-suite run

inc-001's parallel full-suite pass reported 20 failures, all OUTSIDE its files
(test_no_live_board 1, test_precommit_gate 7, test_report 2,
test_scratch_cannot_be_committed 10). The coordinator re-ran exactly those four
files on the settled tree: 45 passed, 0 failed. Cause: the suite ran while the
parallel inc-004 was editing test files (and the dead inc-002 session had just
released the tree) — the known git-subprocess-under-load flake family, plus
dirty-tree git-fixture tests reacting to the uncommitted batch-05 state.

Recorded so the close does not chase them: at P4 the coordinator re-owns the one
complete clean-tree run (C-25) and triages anything that survives it.
