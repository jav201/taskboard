# Requirements ledger — taskboard — Batch 2026-10-18-batch-02

> Append-only. Entries are added in chronological order and never rewritten. The live
> contract is `01-requirements.md`; this file records how it came to say what it says.
> Every entry names the requirement it amends; every requirement names its entries. `V26`
> compares the two sets of pairs both ways.

_No entries yet. The first amendment to the live contract writes the first one, in the
shape the field guide's §7 shows (`req-template.part2.md` in the guide directory init prints), and nothing
above this line is ever edited._

### LED-2026-10-18-batch-02.1 — the backlog fixes and the polish round (P1)
- **Requirement:** HLR-1901, HLR-1902, HLR-1903, HLR-1904, HLR-1905, LLR-1901.1, LLR-1902.1, LLR-1903.1, LLR-1904.1, LLR-1905.1
- **Date:** 2026-10-18
- **What changed:** new requirements: the standup's own-row and name-column behaviour stated so its two tests can encode it with the scrubbed placeholder (HLR-1901); the clipboard roundtrip test's verdict split between the machine and the product (HLR-1902); the presentation's frame below 36 columns (HLR-1903); the hint row's fallback (HLR-1904); the polish prototype round (HLR-1905). They supersede nothing in the canon: the standup and the clipboard reader are unchanged; HLR-1903 widens `render_present`'s domain below the frames LLR-1001.1 and HLR-1801..1803 pin; HLR-1904 adds wordings below the widths LLR-1803.2's TC-1808 pins.
- **Why:** the operator's commission of 2026-10-18 (translated): «Continue with the backlog: fix the Standup tests and the other missing items»; the coordinator's item list; the backlog lanes of 2026-10-16/17/18.
- **Evidence:** P-1..P-9 (`01-requirements.md` §2.7); `evidence/suite-base.txt` (`2 failed, 2721 passed` on `base_ref`).

### LED-2026-10-18-batch-02.2 — P2 iteration 1 amendments (P1, iterate-to-refine)
- **Requirement:** HLR-1901, HLR-1902, HLR-1903, HLR-1904, HLR-1905, LLR-1901.1, LLR-1902.1, LLR-1903.1, LLR-1904.1, LLR-1905.1
- **Date:** 2026-10-18
- **What changed:** Before → After. HLR-1903 / LLR-1903.1: one `dim` line `present needs 36+ columns` cut from the right → the longest of five rungs that fits (`widen to 36+ columns · esc leave` … `36+`), in `mut` (UX-1, UX-2); every key working below 36 → no key but `esc` acts there, `x` notifies `Widen the terminal to 36+ columns to export` and writes nothing (UX-5, UX-7, A-6, A-11, QA-9); width 0 → every row empty (A-8); AT-1903: `2` then "the gantt frame returns" → the frame equal to the one kept before the narrowing, heights 12, every rung's width (QA-1); New: `PRESENT_NARROW`; `PRESENT_MIN_WIDTH` consumed by `app` (ARCHITECTURE §4 row). HLR-1904 / LLR-1904.1: three wordings → four (a compact `⇥ ←→ ␣ x esc`, UX-6) and, below 36, `esc leave` and the hidden count (UX-3); TC-1904's "first wording that fits" recomputation → the literal threshold table of P-7 for 0/3/10 hidden (QA-5); AT-1904: the 25-column arm, which a correct build fails (19 cells fit 23), → three hidden tasks, 50/40/30/15 columns, both views, the bold span asserted (A-1, UX-8, UX-9). HLR-1902 / LLR-1902.1: contention ×5 a SKIP → a FAIL; a skip only when every attempt was refused (QA-2: a reader that disturbs the clipboard would have hidden as a skip); `_ps` named the one seam (QA-3); AT-1902 arm (b), which patched `models.grab_clipboard_text`, → dropped, the mismatch kept in TC-1902 (A-2); the reason "the last refusal" → quoting the refusal, contention now failing (A-5). LLR-1901.1: "a prefix ended by `…`" → the 12-cell name cell equal to `views.fit(name, 12)`; New: the 12/13-cell arm (QA-4). HLR-1905: `inspection` → `test`; New: `out/manifest.json` (SVG→PNG digests), `data-recommend` markers, the RED arms on corrupted copies, the retirement rule, the narrow frame and hint for review (QA-6, QA-7, UX-4). §2.7: P-6 59/66 → 58/65 (A-3), P-7 re-probed for the amended design, P-9 `:6239` → `:6240`, `:6241` (A-4). §5.2: the inspection lines for the HISTORICAL notes and the stale comments (A-7); the `planned` transcripts (QA-8).
- **Why:** the P2 review of 2026-10-18, iteration 1 (architect, qa-reviewer, ux-reviewer `iterate-to-refine`).
- **Evidence:** the reviewers' returns (`02-review.md` §Findings); P-7's re-probe on the scratch worktree (the narrow rungs at widths 0–36, the hint thresholds over widths 1–140, `78 passed` in the presentation tests).

### LED-2026-10-18-batch-02.3 — P2 iteration 2 minor amendments (P2 gate)
- **Requirement:** HLR-1901, HLR-1903, LLR-1901.1, LLR-1903.1, LLR-1905.1
- **Date:** 2026-10-18
- **What changed:** HLR-1903: "every presentation key but `esc`" → "but `esc`/`q` (leave)" (A2-1: `q` is bound with `escape`); AT-1903: before narrowing, `space` hides the cursor task and `2` opens the split view; at 30 columns `1` replaces `2`, so the view, cursor and hidden-set guards are each observed against the kept frame, and `pagedown`'s guard is declared a regression pin (a resize resets the page) (QA2-1). LLR-1903.1: "the arrows" → "every key bound to `move` (the arrows and `h j k l`)" (A2-1). LLR-1901.1: the name cell is read on the row stripped of its padding (QA2-3). LLR-1905.1: its `inspection` scope stated (A2-2). §2.7 P-7: the narrow hint's first whole widths 11 / 22 / 23 for 0 / 3 / 10 hidden (QA2-2). The US-1902 refinement log restated to the amended HLR-1903/1904 (UX2-1). Not changed: UX2-2 (`esc leave` in both the 32–35 rung and the hint — left for the operator's look in the round).
- **Why:** the P2 review of 2026-10-18, iteration 2 (architect, qa-reviewer, ux-reviewer `approve`, each with minors).
- **Evidence:** the reviewers' returns (`02-review.md` §Iteration 2).

### LED-2026-10-18-batch-02.4 — PDR conditions on the test cases (PDR seal)
- **Requirement:** HLR-1903, LLR-1902.1, LLR-1904.1
- **Date:** 2026-10-18
- **What changed:** LLR-1902.1's TC-1902: New arm — contended then refused ×4 → `AssertionError` holding `contended` (PC-1: the mutant `assert not seeded` → `assert refusal is not None` survived the seven arms, executed by the reviewer). LLR-1904.1's TC-1904: New arm — `present_hidden` patched to 123456 tasks, at 36 columns the `esc` wording is cut to 34 cells with `…` (PC-2: the wide-path truncate was unreachable with 0/3/10 hidden). HLR-1903's AT-1903: the keys pressed at 30 columns gain `tab`, `h`, `pageup` (PC-3).
- **Why:** the PDR of 2026-10-18 (`design/PDR-2026-10-18-batch-02.md`, approved with conditions PC-1..PC-6).
- **Evidence:** the reviewer's mutant run on a copy of the helper draft (`<scratchpad>/qa_pdr/mut_clip.py`): the original fails "contended ×4 then refused", the mutant skips.
