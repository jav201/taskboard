# Requirements ledger — taskboard — Batch 2026-10-07-batch-07

> Append-only. Entries are added in chronological order and never rewritten. The live
> contract is `01-requirements.md`; this file records how it came to say what it says.
> Every entry names the requirement it amends; every requirement names its entries. `V26`
> compares the two sets of pairs both ways.

_No entries yet. The first amendment to the live contract writes the first one, in the
shape the field guide's §7 shows (`req-template.md` in the guide directory init prints), and nothing
above this line is ever edited._

### LED-2026-10-07-batch-07.1 — process/chain templates insertable into a project (P1)
- **Requirement:** HLR-1301, LLR-1301.1, LLR-1301.2
- **Date:** 2026-10-07
- **What changed:** new requirements: the template store (`settings["templates"]`, lenient read, two factory presets) and the one-action insert (key `T`, the picker, creation in the first phase with no dates, forward-only `wait` links, ONE undo step, the exact toast). v1 edits templates in the board JSON (documented in the `?` help); "save this chain as a template" is a declared carry.
- **Why:** the operator's request 2026-10-07: "crear templates de procesos o templates de cadenas que se reflejan en tareas que se pueden insertar a proyecto".
- **Evidence:** the shipped patterns it composes (picker · milestones undo · presentation resolution · batch-06 tiles), each cited at P1.

### LED-2026-10-07-batch-07.2 — the templates key is `I`, not `T` (P1 correction, before the first edit)
- **Requirement:** HLR-1301, LLR-1301.2
- **Date:** 2026-10-07
- **What changed:** the contract pinned `T` for the template picker without checking the seat; `T` ships `project_pin_toggle` ("Pin proj", keymap.py:86, pinned by tests/test_focus.py and tests/test_markup_sites.py). The templates key is `I` (Insert) — global, palette-only, group "misc" — and every existing seat stays untouched. Caught by the implementing agent's stop-and-name gate before any code was written; the contract is corrected here, before the first site was edited.
- **Why:** the operator's standing rule — the suite stays green and no shipped seat moves without a verdict.
- **Evidence:** `taskboard/keymap.py:86` (`Key("T", "T", "project_pin_toggle", ...)`); the agent's stopped-run report (evidence/inc001-run.log).
