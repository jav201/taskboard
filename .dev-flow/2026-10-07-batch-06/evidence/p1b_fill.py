"""Batch-06 P1 part 2: stories, premises, fork, 5.2, LED .1."""
from pathlib import Path

p = Path(".dev-flow/2026-10-07-batch-06/01-requirements.md")
s = p.read_text(encoding="utf-8")

OLD_US = "| US-001 | As a `<role>`, I want `<goal>`, so that `<benefit>`. | `<ticket / conversation / client>` | READY \\| REFINE \\| SPIKE \\| OUT |"
NEW_US = ("| US-1201 | As the operator, I want the chain map to show every open task and let me create the first link right there with `L`, so that building the dependency web happens where I look at it. | operator report 2026-10-07 (\"es imposible crear cadenas\") | READY |\n"
          "| US-1202 | As the operator, I want the kanban to show me when phase columns are hidden and on which side, so that I know the rest exists without guessing. | operator report 2026-10-07 (\"no logro ver el resto... incluso reescalando\") | READY |")
assert OLD_US in s
s = s.replace(OLD_US, NEW_US)

OLD_PRE = "| `<one row per premise this batch relies on>` | | | | | |\n\n- **Premise evaluation:** `<the table's roll-up: N premise(s) · \u2705 TRUE / \u274c FALSE / \u2753 UNDECIDABLE — or: none — this batch relies on no premise>`"
NEW_PRE = (
    "| P-1 | The shipped `L` LinkPicker flow works off-view (kanban/gantt): on a copy of the operator's real board (84 tasks, 0 links) `L` on kanban opened the picker with all 34 open tasks as candidates | base behavior | TRUE | coordinator reproduction 2026-10-07 on a temp copy of the operator's default board (LinkPicker opened, 34 candidates; the board file is read-only input) | the fix moves creation INTO the map (LLR-1201.2) |\n"
    "| P-2 | The chain map's nav/selection machinery (`_chainmap_nav`, the seats) and the `○` \"open chain head\" glyph already exist — the tiles are an admission change, not a new mechanism | base behavior | TRUE | `taskboard/views.py` (`_chainmap_nav`, the legend in `help_usage`) | LLR-1201.1 admits the tasks; LLR-1201.2 wires the seats |\n"
    "| P-3 | The C-2b frames pin a zero-link band as an inert `no links` row and the fixture's bands carry \"open not linked\" counts (2 on Website) — those tasks exist in the fixture and the amended frames change | contract being amended | TRUE — and it is exactly what LED-2026-10-07-batch-06.1 amends | `.dev-flow/2026-10-07-batch-02/evidence/frames/C-2b-118x30.txt:22` | the amended oracle is this renderer's bytes on the same frozen fixture, stored at this batch's evidence home |\n"
    "\n- **Premise evaluation:** 3 premise(s) · \u2705 TRUE / \u2705 TRUE / \u2705 TRUE")
assert OLD_PRE in s
s = s.replace(OLD_PRE, NEW_PRE)

i = s.index("### 2.8 Fork preconditions (C-52)")
j = s.index("---\n\n## 3. High-level requirements (HLR)")
s = s[:i] + ("### 2.8 Fork preconditions (C-52) — MANDATORY, and the declared empty when the batch does not fork\n\n"
             "- **Fork preconditions:** none — the batch runs one lane on the main checkout. (One implementing brief at P3 owns the whole tree sequentially; the trunk — requirements, the LED, the oracle amendment's record — is the coordinator's alone.)\n\n") + s[j:]

OLD_52 = """### 5.2 Batch acceptance criteria
- *(e.g.: 100% of LLRs covered by at least one TC with pass result.)*
- *(e.g.: 0 blocker fails in validation.)*
- *(e.g.: test coverage >= X% where applicable.)*
- *(e.g.: no requirement without an assigned validation method.)*
- *(e.g.: every user story has ≥1 passing `AT-NNN` black-box acceptance test observing its outcome through the shipped surface — with boundary + negative evidence.)*"""
NEW_52 = """### 5.2 Batch acceptance criteria
- every HLR has a passing AT; every LLR a passing TC; every new assertion RED on the base tree or by a recorded mutation.
- full suite: 0 failures.
- the amended C-2b oracle ships at this batch's evidence home with the LED; the operator's visual re-verdict is requested at close (batch C's precedent: the verdict folds on arrival)."""
assert OLD_52 in s
s = s.replace(OLD_52, NEW_52)
p.write_text(s, encoding="utf-8")

led = Path(".dev-flow/2026-10-07-batch-06/01-requirements-ledger.md")
t = led.read_text(encoding="utf-8")
t += """
### LED-2026-10-07-batch-06.1 — the chain map admits every open task; the kanban window shows its sides (P1)
- **Requirement:** HLR-1201, HLR-1202, LLR-1201.1, LLR-1201.2, LLR-1202.1
- **Date:** 2026-10-07
- **What changed:** (a) HLR-1201 AMENDS the C-2b oracle (the batch-02 frames this operator's verdict accepted): the chain map now draws every open task — unlinked open tasks as one-row `○` tiles at depth 0 in their band — so chains are created on the map with the shipped `L` picker; the inert `no links` row survives only for a project with no open work; the `x` unlink leaves the task as a visible `○` tile. The amended frames are the new renderer's bytes on the SAME frozen fixture at 118×30 and 80×24, stored at `.dev-flow/2026-10-07-batch-06/evidence/frames/`; the sealed batch-02 frames stay history; `tests/test_chainmap.py`'s frame path moves to the amended home citing this LED. (b) HLR-1202: the kanban's phase-head row marks the hidden window sides (`◂` left, `▸ N` right, exact N) plus the `?` bullet.
- **Why:** the operator's reports from real use 2026-10-07: the chain map shows projects with no tasks and no way to create a chain; the kanban hides later phase columns with no on-screen sign.
- **Evidence:** the coordinator's reproduction on a copy of the operator's board (84 tasks, 0 links — `L` worked only off-view) · `C-2b-118x30.txt:22` (the inert row being amended) · the amended frames (this batch's evidence home, hashes in increment-001).
"""
led.write_text(t, encoding="utf-8")
print("part 2 done")
