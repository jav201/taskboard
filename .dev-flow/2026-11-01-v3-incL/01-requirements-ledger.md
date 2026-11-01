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
