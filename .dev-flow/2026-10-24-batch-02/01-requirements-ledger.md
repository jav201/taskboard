# Requirements ledger — taskboard — Batch 2026-10-24-batch-02

> Append-only. Entries are added in chronological order and never rewritten. The live
> contract is `01-requirements.md`; this file records how it came to say what it says.
> Every entry names the requirement it amends; every requirement names its entries. `V26`
> compares the two sets of pairs both ways.

## LED-2701 — HLR-2701
- **Requirement:** HLR-2701
- **Date:** 2026-10-24
- **Entry:** the commission's HD-1, read in the code: `on_mount` (`app.py:1301-1315`) pushes `BoardsHome` and then `_open_board(at_mount=True)` (`app.py:1405-1426`) runs migration, sweep, presence, team start and the milestone offer under the home — the false «already open» notice the operator saw.

## LED-2701.1 — LLR-2701.1
- **Requirement:** LLR-2701.1
- **Date:** 2026-10-24
- **Entry:** the read-only/deferred split follows the commission's «What still happens at mount» list exactly; the rescue/renumber notices that only read `load_report` stay with the read-only half.

## LED-2701.2 — LLR-2701.2
- **Requirement:** LLR-2701.2
- **Date:** 2026-10-24
- **Entry:** `q` on the home already binds to quit (batch 2026-10-20-batch-01), so the clause is the deferred start's absence, not a new binding.

## LED-2702 — HLR-2702
- **Requirement:** HLR-2702
- **Date:** 2026-10-24
- **Entry:** HD-1's paths (enter, esc/back) and «exactly once»; the exact-once numbers (one notice, one marker, one sweep) come from the commission's AT-a/AT-b.

## LED-2702.1 — LLR-2702.1
- **Requirement:** LLR-2702.1
- **Date:** 2026-10-24
- **Entry:** one started-board record is the single mechanism that satisfies all three paths with one writer set — the C-15.1 writer census lands at P3.

## LED-2702.2 — LLR-2702.2
- **Requirement:** LLR-2702.2
- **Date:** 2026-10-24
- **Entry:** both of the home's actions must run the pending start AFTER popping, so the modals they may open land over the board (the HD-2 consequence).

## LED-2702.3 — LLR-2702.3
- **Requirement:** LLR-2702.3
- **Date:** 2026-10-24
- **Entry:** `switch_board`'s early return at `app.py:1458` (`bid == self.board_id`) is the trap: a pending start must not be skipped there, and a completed one must not re-run.

## LED-2703 — HLR-2703
- **Requirement:** HLR-2703
- **Date:** 2026-10-24
- **Entry:** HD-1's «Picking another board» and «the default board, never started, is never written».

## LED-2703.1 — LLR-2703.1
- **Requirement:** LLR-2703.1
- **Date:** 2026-10-24
- **Entry:** the home's card reads go through `peek_board` (`app.py:702`), which does not save; the only write risk was the mount-time start, which LLR-2701.1 defers.

## LED-2704 — HLR-2704
- **Requirement:** HLR-2704
- **Date:** 2026-10-24
- **Entry:** HD-2; closes BACKLOG D-12 (2026-10-20-batch-03's «blank screen behind the start-up modals»). The modal bodies are untouched — only the push moment moves after the home pops.

## LED-2704.1 — LLR-2704.1
- **Requirement:** LLR-2704.1
- **Date:** 2026-10-24
- **Entry:** the stack assertion («home not on the stack under a start-up modal») is the cheapest black-box proof of HD-2; the single-board/`--open` stack shape is pinned by the existing offer suite.

## LED-2705 — HLR-2705
- **Requirement:** HLR-2705
- **Date:** 2026-10-24
- **Entry:** HD-3 — batch-03 item 8 A's notice stays; the operator's complaint was the notice's timing, never its text.

## LED-2705.1 — LLR-2705.1
- **Requirement:** LLR-2705.1
- **Date:** 2026-10-24
- **Entry:** `_enter_presence` keeps its exact wording, severity, timeout and once-per-open semantics; only the call site (actual board start) is constrained.

## LED-2706 — HLR-2706
- **Requirement:** HLR-2706
- **Date:** 2026-10-24
- **Entry:** the commission's second defect (HD-5); closes BACKLOG A-7 («a person another window adds shows here after a restart or this window's next write»).

## LED-2706.1 — LLR-2706.1
- **Requirement:** LLR-2706.1
- **Date:** 2026-10-24
- **Entry:** the mtime/size gate is the cheapest correct freshness test here (a parse only on change); the size arm matters because some editors preserve mtime.

## LED-2706.2 — LLR-2706.2
- **Requirement:** LLR-2706.2
- **Date:** 2026-10-24
- **Entry:** `marks.Directory` is the people directory's byte-level sibling; the same gate and swap apply unchanged.

## LED-2706.3 — LLR-2706.3
- **Requirement:** LLR-2706.3
- **Date:** 2026-10-24
- **Entry:** the four seats are the commission's enumeration; the editor covers both its directory surfaces (`@` picker, `alt+m` Select) because `TaskModal` takes `people` and `marks` together. The in-place swap reuses `_hold`, which mutates the live dict the boards already hold (`_label_board`, `app.py:1324-1325`), so no view needs a second update path.

## LED-2707 — HLR-2707
- **Requirement:** HLR-2707
- **Date:** 2026-10-24
- **Entry:** HD-5's failure posture: a transient bad write by another window must not wipe this window's directory.

## LED-2707.1 — LLR-2707.1
- **Requirement:** LLR-2707.1
- **Date:** 2026-10-24
- **Entry:** mirrors the mount's load notice (`_warn_registry`, `app.py:1434-1445`): keep the in-memory entries, say so once, never empty. The legitimate-empty vs failed-empty distinction is observable only through the notice's absence, so the AT asserts both sides.

## LED-2708 — HLR-2708
- **Requirement:** HLR-2708
- **Date:** 2026-10-24
- **Entry:** HD-4's unchanged paths; the regression pin for the whole batch.

## LED-2708.1 — LLR-2708.1
- **Requirement:** LLR-2708.1
- **Date:** 2026-10-24
- **Entry:** the single-board and `--open` mounts keep `_open_board(at_mount=True)` whole — HD-1 defers only the home-shown start.

## LED-2708.2 — LLR-2708.2
- **Requirement:** LLR-2708.2
- **Date:** 2026-10-24
- **Entry:** `B`'s home opens over an already-started board; `esc` re-runs nothing. Covered by AT-2703's second half and the home suite.
