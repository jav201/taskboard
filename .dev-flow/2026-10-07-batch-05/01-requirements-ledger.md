# Requirements ledger — taskboard — Batch 2026-10-07-batch-05

> Append-only. Entries are added in chronological order and never rewritten. The live
> contract is `01-requirements.md`; this file records how it came to say what it says.
> Every entry names the requirement it amends; every requirement names its entries. `V26`
> compares the two sets of pairs both ways.

_No entries yet. The first amendment to the live contract writes the first one, in the
shape the field guide's §7 shows (`req-template.md` in the guide directory init prints), and nothing
above this line is ever edited._
### LED-2026-10-07-batch-05.1 — the carries batch derived from the BACKLOG (P1)
- **Requirement:** HLR-1101, HLR-1102, HLR-1103, HLR-1104, HLR-1105, HLR-1106, LLR-1101.1, LLR-1102.1, LLR-1103.1, LLR-1104.1, LLR-1105.1, LLR-1106.1
- **Date:** 2026-10-07
- **What changed:** new requirements carrying the open BACKLOG items into one batch: S5-3 a failed backup write leaves no partial file; F-6 the `Mon D` formatter in three copies becomes one; UXV-3 `u` on a single-task change names what came back; UXV-6 the `?` help clips at word boundaries with `...`; the chain-map carries — the deep-chain per-band `+N more ↓` cap AMENDS TC-810's whole-band-drop rule (the zero-fit band still drops whole), the resize heal re-verifies the selection in one refresh, AT-801b's docstring; the P4 F-3..F-5 test-strength arms. HLR-1105(a) rides this entry as the fold-law amendment (the amended TC-810 cites it, the fold-canon discipline).
- **Why:** the operator's 2026-10-07 "Ok, continuemos" — continue until the plan's proposed changes are done; these are the plan's remaining open carries.
- **Evidence:** `.dev-flow/BACKLOG.md` (the open sections) · the P1 anchors re-verified against the tree: `taskboard/models.py:1562` (`_create_beside`), `:2133` (`_md`), `taskboard/views.py:2680` (`_md`), `:6882` (`legend_entries`), `taskboard/app.py:40` (`_md`), `:1408` (`action_undo`), `:1495` (`refresh_view`), `taskboard/modals.py:1750` (`HelpModal`).
