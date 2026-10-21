# Review — taskboard — Batch 2026-10-20-batch-02

> **Artifact language:** canonical English scaffold. Generate in the batch's development language (`state.json` `language`).
> Phase 2 artifact. Reviewers (in parallel): `architect` ∥ `qa-reviewer` ∥ `security-reviewer` by trigger family C (always in `full`).

> **Owed in.** `core` ✓ · `full` ✓

> **Field guide:** `templates/guides/review-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

## ✅ Verdict (read first)

- **Gate:** `approve` — iteration 1 `iterate-to-refine` (architect A-1 HIGH; qa-reviewer QA-1 HIGH requirement defect; security-reviewer `BLOCK-UNTIL: S-1`; ux-reviewer UX-1/UX-2 major) → LED-2026-10-20-batch-02.2; iteration 2: architect approve, qa-reviewer approve, security-reviewer approve with conditions (S-6..S-9 LOW), ux-reviewer approve with conditions (UX-8, UX-9 minor) → Phase 3 through the PDR
- **Out-of-scope findings:** 4 named and routed below — UX notes for the visual round (a waiting indicator, an "another instance is running" notice, feedback that an unarchive changed the order) → the prototype round, not this batch; A-7 (adoption by id when a memory-only id is reused for another file) → `BACKLOG.md`, accepted LOW
- **Findings:** iteration 1: 4 blocker-class (A-1, QA-1, S-1, UX-1/UX-2 as one major pair) · 8 major/medium (QA-2..QA-5, S-2..S-4, UX-2) · 13 minor/low; iteration 2: 0 blocker · 1 medium (QA-8) · 11 low/minor (A-7, A-8, QA-9, QA-10, S-6..S-9, UX-8, UX-9)
- **shall/should check:** ✓ clean
- **Two-layer (blockers):** ✓ every story has an `AT` · output reqs name deliverable+observation · both trace chains complete · ATs are genuinely black-box (they drive `open_app`/`TaskboardApp` and keys; "another taskboard" is the shipped `Registry` or a lock file acting on the same files)
- **Census (change-first):** done — best-effort + gate-confirmed
- **Security:** ⚠ 9 findings (S-1 HIGH, discharged by LED .2; S-2..S-4 medium, folded; S-5..S-9 low — S-5 folded, S-6..S-8 conditions of the PDR, S-9 recorded)
- **Evidence checklists (architect / qa / security):** ✓ all complete (in the reviewers' returns; ux-reviewer too)

> If gate = `approve` and every line is ✓, the Detail below is reference. Any blocker/⚠ → read the matching part.

---

## Detail (reference)

Reviewers: `architect`, `qa-reviewer`, `ux-reviewer` (D1 fired), `security-reviewer` (C5, C6 fired) — each spawned as a sub-agent with its `agents/<role>.md` role, read-only, in parallel, 2026-10-20, two iterations; each reviewed the ARQ amendment, the requirements (P2) and the design proposal (PDR) together; iteration 2 also read the draft `boards.py` and test file kept outside the tree.

### Findings
| ID | Reviewer | Severity | Area / Req | What | Recommendation | Status |
|----|----------|----------|------------|------|----------------|--------|
| A-1 | architect | blocker | HLR-2305, LLR-2305.1 | the `~` fix at `_key`/load/`register` only; every opener reads the raw stored path, so AT-2305 cannot pass and its negative control misstates the base | normalise once in `_read`, store absolute; correct the negative control | fixed (LED .2) |
| A-2 | architect | minor | LLR-2301.2 | the fate of memory-only entries at adoption unstated | keep them in memory | fixed (LED .2) |
| A-3 | architect | minor | LLR-2301.1 | release and takeover not owner-safe; a stat race | token, `lstat` re-check, stat error read as busy | fixed (LED .2) |
| A-4 | architect | minor | HLR-2301 | a busy `register` at `--board` start is a traceback; the wait blocks the event loop | exit 1 with the message; §6.3 | fixed (LED .2) |
| A-5 | architect | minor | HLR-2302 | the stopped-move notice claims backups never made | the sentence only when something was done | fixed (LED .2) |
| A-6 | architect | minor | PDR §4 | wrong consumers named for the registry's writers | `BoardsHome`, `switch_board`, `open_app` | fixed |
| A-7 | architect | minor | LLR-2301.2 | adoption by id could rewrite a memory-only entry's path if another instance reused its id for another file | adopt in place only for the same file | accepted LOW → `BACKLOG.md` (the guard keeps two entries of one id in memory; the case needs a synthesized `main-2` reused elsewhere) |
| A-8 | architect | minor | LLR-2301.1 | a `PermissionError` on create for an unwritable folder reads as "busy" | a distinct message | accepted — the message names the lock's path and the wait is bounded (with S-9) |
| QA-1 | qa-reviewer | blocker | HLR-2304 | AT-2304 GREEN on the base (Customer Portal never ranked) | rank first, then archive, re-rank, unarchive | fixed (LED .2); re-probed RED on base in iteration 2 |
| QA-2 | qa-reviewer | major | HLR-2306 | the hygiene law counts `test_*` functions and matches its own needle | imports and plain assignments; concatenated needle | fixed (LED .2) |
| QA-3 | qa-reviewer | major | LLR-2306.2 | "drop `Text`" contradicts "read `Text.from_markup`" | keep `Text`, drop `PAYLOADS` | fixed (LED .2) |
| QA-4 | qa-reviewer | major | LLR-2306.2 | no view-3 row starts with `⟦` | the row holding `⟦`, the tick row aside | fixed (LED .2) |
| QA-5 | qa-reviewer | major | TC-2301, TC-2302 | missing arms: busy per writer; target changed while awaited | add them | fixed (LED .2); the drafted arm missing → QA-8 |
| QA-6 | qa-reviewer | minor | HLR-2301 | `touch` changes memory on a busy lock | state the exception | fixed (LED .2) |
| QA-7 | qa-reviewer | minor | thresholds | lock catalog gaps; AT-2302's retry `P`; the lock marker; AT-2305's `last`; the `_all_cur` count | as recommended | fixed (LED .2) |
| QA-8 | qa-reviewer | major | TC-2302 | the draft lacks the "rewritten while the move waited" arm | add it with its mutation | PDR condition PC-1 |
| QA-9 | qa-reviewer | minor | TC-2301 | the busy loop asserts once, at the end | assert after each call | PDR condition PC-1 |
| QA-10 | qa-reviewer | minor | AT-2304 | the selection set through `selected_task_id` | record as set-up | recorded (increment 002's packet) |
| S-1 | security-reviewer | blocker | LLR-2301.2 | an unreadable registry written over without a copy | a failed read raises; unparseable bytes set aside, else nothing written | fixed (LED .2); discharged at iteration 2 |
| S-2 | security-reviewer | major | LLR-2301.1 | release not owner-checked; takeover race; long holders | token, re-check, heartbeat | fixed (LED .2) |
| S-3 | security-reviewer | major | LLR-2301.1 | a directory at the lock path; a future mtime; the deadline | regular files only, `abs`, deadline per pass, the path in the message | fixed (LED .2) |
| S-4 | security-reviewer | major | LLR-2305.1 | the `~` at three sites only; `_home_path` name clash | normalise at load; rename | fixed (LED .2) |
| S-5 | security-reviewer | minor | LLR-2303.1 | the copy in memory, a partial copy; the source history unlocked; a symlinked lock path | stream; resolved path; §6.3 | fixed (LED .2) |
| S-6 | security-reviewer | minor | LLR-2301.1 | a failed token write leaves a token-less lock | unlink before re-raising | PDR condition PC-2 |
| S-7 | security-reviewer | minor | LLR-2301.1 | the takeover re-check compares the mtime only | add `st_ino` | PDR condition PC-2 |
| S-8 | security-reviewer | minor | LLR-2302.1 | one heartbeat after three copies | renew after each copy | PDR condition PC-2 |
| S-9 | security-reviewer | minor | LLR-2301.1 | an unwritable folder reported as busy | record | recorded (§6.3 at increment 001, with A-8) |
| UX-1 | ux-reviewer | major | HLR-2304 | always max + 1 moves an undone archive to last | keep the rank without a tie | fixed (LED .2) |
| UX-2 | ux-reviewer | major | HLR-2302 | the busy notice claims backups | drop the sentence when nothing was done | fixed (LED .2) |
| UX-3 | ux-reviewer | minor | HLR-2302 | `board.json is busy` names no board | name the target board | fixed (LED .2) |
| UX-4 | ux-reviewer | minor | HLR-2301 | a busy start is a traceback | the exit path | fixed (LED .2) |
| UX-5 | ux-reviewer | minor | AT-2304 | "shown" vs "ranked" | the HLR's wording | fixed (LED .2) |
| UX-6 | ux-reviewer | minor | §6.3 | the 2 s wait blocks the screen | record | fixed (LED .2) |
| UX-7 | ux-reviewer | minor | LLR-2301.1 | "try again" while a dead lock ages | "in a few seconds" | fixed (LED .2) |
| UX-8 | ux-reviewer | minor | HLR-2301 | the start clause has no node | a node through `main()` | PDR condition PC-3 |
| UX-9 | ux-reviewer | minor | HLR-2304 | the title and outcome still say "comes last" | "never ties a presentation rank" | PDR condition PC-4 (wording, at increment 002) |

### shall / should check

✓ clean — every HLR states one `shall` (EARS event-driven, unwanted-behaviour or ubiquitous); no `should` in a normative slot.

### Two-layer acceptance review (blockers)

| Story / Req | (a) AT present | (b) deliverable+method named | (c) both chains | (d) black-box pure | Status |
|-------------|----------------|------------------------------|-----------------|--------------------|--------|
| US-2301 / HLR-2301, HLR-2302 | AT-2301, AT-2302 | yes (`boards.json`, the notices, the two folders) | yes | yes | ✓ |
| US-2302 / HLR-2303 | AT-2303 | yes (`history.jsonl.pre-move-<date>`) | yes | yes | ✓ |
| US-2303 / HLR-2304 | AT-2304 | yes (view 3's order, the file's ranks) | yes | yes (after QA-1) | ✓ |
| US-2304 / HLR-2305, HLR-2306 | AT-2305, AT-2306 | yes (the board view; the suite's law) | yes | AT-2305 yes; AT-2306 is a law over the suite, its surface | ✓ |

### Supersession census (change-first)

`tests/test_boards.py`, `tests/test_boards_forms.py` (the registry's writers; `Registry.save` patched in `test_TC_2205_a_failed_registry_save_changes_nothing`, `_unique_id` patched in `test_TC_2205_a_folder_on_disk_is_never_written_into`), `tests/test_boards_move.py` (`move_project`'s steps; the stopped-move notice at line 294), `tests/test_present_all.py` and `tests/test_archive.py` (the archive toggle), `tests/test_boards_home.py` (AT-2204). The I-gate confirms each still passes, or names the law-driven update.

### Security review summary
iteration 1 `BLOCK-UNTIL: S-1` (S-1 HIGH; S-2..S-4 medium; S-5 low); iteration 2 approve with conditions — S-1 discharged by the contract, S-6..S-8 conditions of the PDR, S-9 recorded; the code is re-read at increment 001.

### Evidence checklists (full) — architect · qa-reviewer · security-reviewer
In the reviewers' returns (iterations 1 and 2), each with its role file's checklist complete; ux-reviewer: expert inspection, no user evaluation (one-person team), stated.
