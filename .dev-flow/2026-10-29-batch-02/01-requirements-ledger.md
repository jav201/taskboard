# Requirements ledger — taskboard — Batch 2026-10-29-batch-02

> Append-only. Entries are added in chronological order and never rewritten. The live
> contract is `01-requirements.md`; this file records how it came to say what it says.
> Every entry names the requirement it amends; every requirement names its entries. `V26`
> compares the two sets of pairs both ways.

### LED-2026-10-29-batch-02.1 — the loaders copy unreadable files aside; the report reads without them
- **Requirement:** LLR-4104.2
- **Requirement:** HLR-4104
- **Date:** 2026-10-29
- **What changed:** LLR-4104.2 named only the board writers; it now requires the non-copying readers for the registry, people and marks and adds a corrupt-files arm to the threshold.
- **Why:** the P2 security review (F1, MEDIUM): `Registry.load`, `people.Directory.load` and `marks.Directory.load` call `keep_aside`, so a «read-only» command would create `.corrupt` files in the owner's data folders on every run.
- **Evidence:** `taskboard/boards.py` (`Registry.load` → `keep_aside`), `taskboard/people.py:141`, `taskboard/marks.py:90`; `02-review.md` finding SEC-1.

### LED-2026-10-29-batch-02.2 — one print function for everything file-derived or typed
- **Requirement:** LLR-4104.3
- **Requirement:** HLR-4104
- **Date:** 2026-10-29
- **What changed:** the control-stripping rule covered names and paths only and collapsed whitespace; it now covers project names, the echo of an answer, error text and the notice, writes tab and newline visibly, drops separators and bidi overrides, and leaves stdout paths unchanged.
- **Why:** the P2 security review (F2, MEDIUM): the unknown-project message printed project names raw, and collapsing spaces would have corrupted a real path that a script reads.
- **Evidence:** `taskboard/models.py` `strip_controls` keeps tab, newline, U+2028 and U+202E; `02-review.md` finding SEC-2.

### LED-2026-10-29-batch-02.3 — stdin that misbehaves
- **Requirement:** LLR-4102.5
- **Requirement:** HLR-4102
- **Date:** 2026-10-29
- **What changed:** a new LLR bounds the answer line, and treats a closed stdin, an `OSError` and a decoding error as end of input.
- **Why:** the P2 security review (F3, MEDIUM): invalid bytes and a closed stdin would raise a traceback; an unbounded line is read whole.
- **Evidence:** `02-review.md` finding SEC-3.

### LED-2026-10-29-batch-02.4 — the `a` notice and the empty `--board`
- **Requirement:** LLR-4102.4
- **Requirement:** LLR-4104.1
- **Requirement:** HLR-4102
- **Requirement:** HLR-4104
- **Date:** 2026-10-29
- **What changed:** `a` now names the folder and the board count on stderr before writing; the refusal covers the resolved path of every source, an empty `--board` value included.
- **Why:** the P2 security review (F4 MEDIUM, F5 LOW): the prompt did not say where the combined data goes; `args.board or args.open` let an empty value fall through to the default board.
- **Evidence:** `02-review.md` findings SEC-4, SEC-5.

### LED-2026-10-29-batch-02.5 — the error arm, the default under `a`, the two old CLI tests
- **Requirement:** LLR-4101.2
- **Requirement:** LLR-4102.4
- **Requirement:** LLR-4105.3
- **Requirement:** HLR-4105
- **Date:** 2026-10-29
- **What changed:** LLR-4101.2 states the `OSError` arm (exit 1); LLR-4102.4 says `a` falls back to the first readable board's folder when the default is unreadable; LLR-4105.3 is new and names the two rewritten tests; AT-4107 keeps only its stdout assertion and the source and README pins move to TC-4109.
- **Why:** the P2 QA review F-1, F-2, F-3, F-4 (majors and a minor): an error arm promised in a boundary catalog with no requirement, an undefined folder, and a supersession the commission asks to justify.
- **Evidence:** `02-review.md` findings QA-1..QA-4.

### LED-2026-10-29-batch-02.6 — the backlog edits
- **Requirement:** LLR-4105.4
- **Requirement:** HLR-4105
- **Date:** 2026-10-29
- **What changed:** LLR-4105.4 (inspection) owns the two BACKLOG edits CR-5 and D-4 promise.
- **Why:** the P2 QA review F-5: nothing owned them.
- **Evidence:** `02-review.md` finding QA-5.

