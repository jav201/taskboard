# Requirements ledger — taskboard — Inc L, the added-order list view

> Append-only. Every entry names the requirements it amends one by one (V26: no ranges).

### LED-2026-11-01-incL.1 — the commission's L-1..L-5 made strict, with the failure paths it left open
- **Requirement:** HLR-4301
- **Requirement:** HLR-4302
- **Requirement:** HLR-4303
- **Requirement:** HLR-4304
- **Requirement:** HLR-4305
- **Requirement:** HLR-4306
- **Date:** 2026-11-01
- **What changed:** the commission text (L-1..L-5) and the round's `ListB` were split into 63 single-`shall` LLRs. Added beyond its words, each as its own requirement: the seed path stamps (LLR-4301.6) and `Board.add_task` is the stamping seam (LLR-4301.5, LLR-4301.7), so Inc K's dump inherits the stamp; edit, move, undo-restore and rescue keep or never invent `created` (LLR-4301.8, LLR-4301.9, LLR-4301.10, LLR-4301.11); a non-string stored `created` round-trips (LLR-4302.3); the list never writes (LLR-4302.6); an unreadable board is said (LLR-4303.6); markup in board text is literal (LLR-4303.20); empty list (LLR-4303.17, LLR-4303.18); unparseable `created`, unreadable history, offset-aware moments (LLR-4304.8, LLR-4304.12, LLR-4304.13); no stamped task anywhere (LLR-4304.11, LLR-4304.15); more than 8 phases (LLR-4305.2) and mixed phase counts (LLR-4305.3); the list's archived toggle starts hidden whatever the board's `v` (LLR-4306.2) and keeps the cursor's task (LLR-4306.4). Self-check against 29148 split the compound archived-row rule into LLR-4306.5 and LLR-4306.7, and the no-record wording into LLR-4304.11 and LLR-4304.15.
- **Why:** each addition closes a path where the literal commission text either invents history for an old task (rewriting it), crashes on a stored value the app did not write, or leaves a key with undefined behaviour. The bound "before <first created date>" is sound: every unstamped task was created before the field existed, hence before any stamp.
- **Evidence:** `prototypes/capture_round/proto.py` `all_rows`/`ordered`/`ListB` (the proto read `created` from `extra` and dropped archived tasks unconditionally); `taskboard/models.py` `Board.add_task` writes the birth record; `taskboard/app.py` `_on_template_picked` writes none; `taskboard/boards.py` `move_project` moves the history lines with the tasks.

### LED-2026-11-01-incL.2 — the baseline graph's key-seat facts
- **Requirement:** LLR-4303.21
- **Requirement:** LLR-4303.22
- **Requirement:** LLR-4303.23
- **Date:** 2026-11-01
- **What changed:** three LLRs added after E2a. `added_list` is gated under a modal like `A`/`@`/`#` (LLR-4303.21); the list view joins the screens that hold the key seat (LLR-4303.22); the README key table carries `N` (LLR-4303.23).
- **Why:** `TaskboardApp.check_action` names the global actions and the holding screens by hand; a new global screen is in neither list until added, so without LLR-4303.22 `a`, `d`, `x` would act on the hidden board behind the list. The README table is pinned to the seat by a test.
- **Evidence:** `baseline-notes.md` "Global views and keys"; `taskboard/app.py:1286-1312`; `tests/test_keymap.py::test_the_readme_keybinding_table_matches_the_seat`.

### LED-2026-11-01-incL.3 — the E2b prototype's findings, ruled (round 0)
- **Requirement:** LLR-4302.3
- **Requirement:** LLR-4302.4
- **Requirement:** LLR-4302.5
- **Requirement:** LLR-4303.21
- **Requirement:** LLR-4303.24
- **Requirement:** LLR-4304.12
- **Requirement:** LLR-4304.16
- **Date:** 2026-11-01
- **What changed:** LLR-4302.4 compares against the bytes base writes (P-D-1: the legacy migration rewrites at base too); LLR-4302.5 runs on the plain board; LLR-4302.3 checks values, not key position (P-D-3); LLR-4303.21's threshold calls `check_action` directly (P-S-1); new LLR-4303.24 for `enter` on an archived task (P-S-3); LLR-4304.12 also covers `ValueError` (P-V-1); new LLR-4304.16 for a failed time-zone conversion (P-V-2).
- **Why:** each was found by a probe on the worktree during E2b: two thresholds could not pass at base or could not fail at all, and two failure paths crashed `N`.
- **Evidence:** `03-pdr-rulings.md` round 0; `graph-proto-D.cw.md` P-D-1, P-D-3; `graph-proto-S.cw.md` P-S-1, P-S-3; `graph-proto-V.cw.md` P-V-1, P-V-2.

### LED-2026-11-01-incL.4 — the PDR round 1 findings, ruled
- **Requirement:** HLR-4302
- **Requirement:** LLR-4302.5
- **Requirement:** LLR-4302.6
- **Requirement:** LLR-4302.7
- **Requirement:** LLR-4304.4
- **Requirement:** LLR-4304.5
- **Requirement:** LLR-4304.11
- **Requirement:** LLR-4304.12
- **Requirement:** LLR-4304.13
- **Requirement:** LLR-4304.15
- **Requirement:** LLR-4304.16
- **Requirement:** LLR-4304.17
- **Requirement:** LLR-4302.1
- **Date:** 2026-11-01
- **What changed:** the tie-break and unknown-first controls get a shuffled input (ARCH-1); HLR-4302's control names TC-4316, whose board gains a birth record (ARCH-2); offset-aware moments are not valid, LLR-4304.13 rewritten and LLR-4304.16 withdrawn (ARCH-3); LLR-4302.6's subject is the list view (ARCH-6); LLR-4304.11/.15 count every task read (ARCH-8); new LLR-4302.7 keeps `created` out of the team push (SEC-1, reversing P-D-6); LLR-4304.12 also covers RecursionError (SEC-2); new LLR-4304.17 for non-str ids (SEC-3); LLR-4302.1's threshold names the saved record (`with_created=True`).
- **Why:** two negative controls could not fire; a conversion was removable instead of guardable; a new class of personal data (when someone worked, to the second) left the machine for no reader; two crafted-file crashes of `N` were confirmed by probe.
- **Evidence:** `03-pdr-architect.md`, `03-pdr-security.md`, `03-pdr-rulings.md` round 1.

### LED-2026-11-01-incL.5 — E5: the first VALID birth record
- **Requirement:** LLR-4304.2
- **Date:** 2026-11-01
- **What changed:** LLR-4304.2 takes the first birth record whose `at` is a valid moment, not the first birth record (CR-1, design-gap). Threshold gains TC-4362b (an offset-aware or garbage first record, then a valid one → source `h` at the valid one).
- **Why:** since ARCH-3 made offset-aware moments not valid, a hand-edited or foreign first record hid a later valid one and the task fell to `?`.
- **Evidence:** `05-review-code.md` CR-1 (probe); `03-pdr-rulings.md` E5.
