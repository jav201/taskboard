# Requirements Document — taskboard — Batch 2026-10-20-batch-02

> **Artifact language**
> This template is the canonical **English scaffold**. Generate the artifact in the batch's development language (`state.json` `language`). For Spanish batches, translate the **prose** — section headers and guidance — **and never a label**, and use `deberá` as the normative keyword (≡ `shall`). The normative RULES in this preamble are **language-independent** and enforced regardless of artifact language.

> **Owed in.** `core` ✓ · `full` ✓

> **Field guide:** `templates/guides/req-template.md` and its part 2, `templates/guides/req-template.part2.md`, explain each field below and the rules that read it. It ships with the flow and is not copied into this batch.

> **Reserved field names.** The **field names and block keywords below are language-independent** — the
> validator parses them literally and they are never translated:
> `Validation` · `Acceptance test(s)` · `Boundary catalog` · `Negative control` · `Premise evaluation` · `Fork preconditions` · `Ledger` · `Requirement` · `⏸ DEFER`
> Everything else on this page — headings, guidance, the prose in every cell — is translated with the batch.
> **One strategy, not two:** the flow ships no alias table, so a translated label is read as an ABSENT one and the rule keyed on it reports a true-sounding silence.
> **And one FLOW-WIDE reserved token, read out of this artifact by `V42` no matter which template minted it:** `⏸ DEFER`. It is a MARKER rather than a field name, which is why it is stated here *and* in `/dev-flow` §Language of artifacts rather than in a per-template list — a deferral can be written in any batch artifact, including the ones that carry no block at all.

---

## 1. Introduction

### 1.1 Purpose
The live contract for batch 2026-10-20-batch-02: the non-visual items the multi-board batch (2026-10-20-batch-01) and the present-portfolio batch (2026-10-19-batch-01) left in `.dev-flow/BACKLOG.md` — two taskboard instances that no longer lose each other's registry changes, a move that keeps a copy of the history it rewrites and holds its target while rewriting it, an unarchived project that never ties a presentation rank, `~` read through the suite's home seam, and the test and code hygiene the reviewers recorded.

### 1.2 Scope
In: `models` — `taskboard/boards.py` (`file_lock`, the registry's writers as a read-modify-write, the move's target lock and history copy, `~` through `Path.home()`); `modals` — `taskboard/modals.py` (the stopped-move notice without a false backups sentence, `ProjectPicker`'s unarchive rank, `_move_target`'s parameter); `app` — `taskboard/__main__.py` (a busy registry at start is a message, not a traceback); the tests these change and the hardened tests (`tests/test_boards_forms.py`, `tests/test_boards_home.py`, `tests/test_present_all.py`, new `tests/test_boards_concurrency.py`, new `tests/test_hygiene.py`); `docs/ARCHITECTURE.md`, `.dev-flow/BACKLOG.md` (docs). Out: any notice, warning or screen that tells the operator another instance is running (the prototype round, visual); a lock on a plain board save (`Board.save`/`save_atomic` outside a move); a lock on the move's source board; `~user` paths; every other open item of the two backlog sections; pushing or merging.

### 1.3 Definitions, acronyms, abbreviations
| Term | Definition |
|------|------------|
| instance | one running `taskboard` process |
| registry | `boards.json` beside the default board (batch 2026-10-20-batch-01) |
| lock file | `<file name>.lock` beside the file it guards, created exclusively, removed when released |
| stale lock | a lock file whose modification time is older than `LOCK_STALE` seconds |
| read-modify-write | under the lock: read the file fresh, apply the one change, write the result atomically |
| shown rank | the `present_rank` of a project the presentation lists (`visible_projects(False)`) |
| home seam | `tests/conftest.py::_never_the_real_home`, which points `Path.home()` at a temporary folder |

### 1.4 References
- The operator's commission (2026-10-20): «Haz lo del backlog por favor.», scoped by the orchestrator to the non-visual items of `.dev-flow/BACKLOG.md` lines 138–167 (the commission's six items).
- The backlog entries this batch closes: G-9 (qa-reviewer at P4 of 2026-10-20-batch-01), security N1 of increment 004, "two app instances … a move does not lock the target board", architect A-10 of 2026-10-19-batch-01, code review N2 of increment 004, code review N1/N2 of increment 003, qa QA-03 (DDR), qa G-2 and G-4 (P4 of 2026-10-19-batch-01).
- The shipped code: `taskboard/boards.py` (`_key` 82–84, `Registry.load` 124–169, `register` 226–240, `create` 242–268, `edit` 276–288, `archive` 290–298, `touch` 300–314, `save` 316–320, `_backup` 428–443, `move_project` 464–572), `taskboard/modals.py` (`ProjectPicker.action_move_board` 771–784, `_move_target` 786–802, `_do_archive_toggle` 838–847), `taskboard/models.py` (`write_atomic`, `present_order` 2417–2425, `set_present_order` 2428–2432), `tests/conftest.py:25-36`.

### 1.5 Document overview
§2 the stories, premises and fork preconditions; §3 six HLRs; §4 eight LLRs and the information-flow contract; §5 the validation strategy; §6 the open risks.

---

## 2. Overall description

### 2.1 Product perspective
The registry and the move shipped in 2026-10-20-batch-01 write files a second instance may be writing too; today the last writer wins and a board created by one instance can vanish when the other saves. This batch makes taskboard's own writers of the registry serialise through a short lock file and re-read before writing, and makes a move hold its target board while it re-checks and rewrites it. Nothing on screen changes but the text of the existing error notices when a lock is busy, and the presentation's order after an unarchive.

### 2.2 Product functions
1. A board created, renamed, recoloured, archived or registered by one instance never erases one another instance wrote to the registry.
2. A move into a board another instance is moving into waits briefly or stops before writing anything.
3. A move keeps a byte copy of the source board's history before rewriting it.
4. An unarchived project never ties a presentation rank: its place kept, or after the last shown rank when another took it.
5. A `~` path in the registry is read from the user's home as the suite's seam sees it.
6. The tests read the screen, not private state, where the screen shows it, and the code keeps no dead parameter.

### 2.3 User characteristics
The operator alone (`username_subject`), keyboard only, sometimes with taskboard open in two terminals; the maintainer (the same person) reading the suite.

### 2.4 Constraints
Standard library only (no new dependency); Windows-safe (`os.open` with `O_CREAT | O_EXCL`, no `fcntl`/`msvcrt`); a lock is never waited on for more than `LOCK_WAIT` seconds and a stale lock never blocks; nothing new is written for a one-board user without a registry file (HLR-2201 of batch 2026-10-20-batch-01 kept); no lock file is left behind after a write; no new screen, notice or key; synthetic data only; the operator's name nowhere; tests never touch the real home.

### 2.5 Assumptions and dependencies
Two instances run on one machine and one filesystem (a lock file on a network share is outside the stated environment). The suite's home seam (`tests/conftest.py`) stays as shipped. The time-dependent parts (the move's backup names) are tested with the calendar frozen as `tests/test_boards_move.py` does.

### 2.6 Source user stories

| ID | User Story | Source | DoR status |
|----|------------|--------|------------|
| US-2301 | As the operator with taskboard open in two terminals, I want a board one of them creates, renames, recolours, archives or registers to survive the other's next registry write, and a move into a board never to overwrite what the other just wrote there, so that two windows never quietly lose my boards. | BACKLOG «two app instances can both write `boards.json` and a board file … a move does not lock the target board» | READY |
| US-2302 | As the operator, I want a move to keep a byte copy of the source board's history before it rewrites it, so that a move can be undone by hand like the board files. | BACKLOG security N1 of increment 004 | READY |
| US-2303 | As the presenter, I want a project I unarchive to come back after the projects I have ordered, never tied with one, so that my order is not reshuffled. | BACKLOG architect A-10 (2026-10-19-batch-01) | READY |
| US-2304 | As the maintainer, I want the suite to reach the screen by keys and read what the screen shows, the home seam to cover `~`, and no dead parameter or import, so that a test fails when the behaviour it names breaks. | BACKLOG G-9, N1/N2 (increment 003), N2 (increment 004), QA-03, G-2, G-4 | READY |

#### Refinement log (one block per story)

**US-2301 — two instances**
- **INVEST:** I ✓ · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality (V, N):** user = the operator · outcome = every registry write by taskboard is a read-modify-write under `boards.json.lock`; a move holds `board.json.lock` beside its target from the stale-plan check to the target's save; a busy lock past `LOCK_WAIT` raises an `OSError` whose text the existing notices show; a stale lock is taken over · why = the backlog item · out of scope = telling the operator another instance is running (visual round), locking plain board saves
- **Feasibility (E, S):** implementation path = `file_lock` and `Registry._commit` in `boards.py`; `move_project` takes the lock · dependencies/unknowns = `O_EXCL` on Windows (P-6, TRUE) · fits one batch? = yes, increment 001, 1 source file
- **Evaluability (T) — behavioral, black-box:** When another taskboard adds a board to `boards.json` while the app runs and the operator then creates a board with `B`, `n`, a name and `enter`, `boards.json` holds both and the home shows both (AT-2301); when the target board's lock is held by another instance, `enter` on the move's confirmation stops with a notice naming the file as busy and neither board file changes (AT-2302).
- **Open questions:** none.
- **Classification:** `READY`.

**US-2302 — the history copy**
- **INVEST:** I ✓ · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality (V, N):** user = the operator · outcome = `history.jsonl.pre-move-<date>` (exclusive, `-2`… never clobbering) beside the source before anything is written · why = the security finding · out of scope = a copy of the target's history (it is only appended to)
- **Feasibility (E, S):** `_backup` already exists for the board files · fits one batch? = yes, increment 001
- **Evaluability (T) — behavioral, black-box:** When the operator moves a project whose source history holds an undecodable byte, the source folder holds `history.jsonl.pre-move-2026-10-20` with the history's original bytes (AT-2303).
- **Open questions:** none.
- **Classification:** `READY`.

**US-2303 — unarchive keeps the order**
- **INVEST:** I ✓ · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality (V, N):** user = the presenter · outcome = unarchiving a ranked project gives it the rank after the last shown rank; with no other ranked project shown, its rank is cleared and it takes board order · why = A-10 · out of scope = the board's own order
- **Feasibility (E, S):** `ProjectPicker._do_archive_toggle` · fits one batch? = yes, increment 002, 1 source file
- **Evaluability (T) — behavioral, black-box:** When the presenter reorders view 3 with one project archived, then unarchives it with `P`, `x`, view 3 lists it after every other ranked project and the file's ranks are distinct (AT-2304).
- **Open questions:** none.
- **Classification:** `READY`.

**US-2304 — the suite proves what it names**
- **INVEST:** I ✓ · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality (V, N):** user = the maintainer · outcome = `~` through `Path.home()`; `_move_target(proj, bid)`; `tests/test_boards_forms.py` without `PAYLOADS`/`Text` and reading `border_title`; AT-2204 checks `B` in the help and reaches `R` by keys; AT-2104 checks the cursor's row; `u` driven in view 2; AT assertions on the presentation cursor read the frame · why = the reviewers' findings · out of scope = the white-box TCs and the navigation helper that read `_all_cur` (no public observation of a task cursor with the rail focused)
- **Feasibility (E, S):** increment 001 (`~`), 002 (the parameter), 003 (tests only) · fits one batch? = yes
- **Evaluability (T) — behavioral, black-box:** When a registry entry reads `~/side/board.json` and the environment's home differs from `Path.home()`, the home lists that board and `enter` opens the file under `Path.home()` (AT-2305); the suite's hygiene law fails on a test reading `_border_title`, on an unused module-level name in `tests/test_boards_forms.py`, or on `_move_target` taking a third parameter (AT-2306).
- **Open questions:** none.
- **Classification:** `READY`.

### 2.7 Premise evaluation (C-43) — MANDATORY, one row per premise

| # | Premise, as a truth-apt proposition | Tier (axiom · hypothesis · premise) | Verdict | Executed evidence (command output / `file:line` — **NOT** a citation of another document) | Disposition |
|---|---|---|---|---|---|
| P-1 | Under the home seam, `boards._key("~/x")` resolves under the environment's home, not under `Path.home()` | premise | TRUE | `evidence/premises.py` on `base_ref`: `P-1 Path.home(): True \| expanduser('~/x') under the seam home: False \| boards._key('~/x') under the env home: True` (`evidence/premises.txt`) | `~` read through `Path.home()` (HLR-2305) |
| P-2 | Two registries loaded from one file: the second writer's save drops a board the first created | premise | TRUE | the same probe: `P-2 ids on disk after A creates and B (loaded before) edits: ['main', 'notes'] \| A's board lost: True` | read-modify-write under a lock (HLR-2301) |
| P-3 | A move rewrites the source `history.jsonl` and leaves no copy of it | premise | TRUE | `P-3 steps: ['copied board.json', 'copied board.json', 'saved the target', 'saved the source', 'moved the history lines', 'wrote the move logs'] \| history copies: []` | the history copy (HLR-2303) |
| P-4 | An archived project keeps its `present_rank`; a reorder while it is archived re-ranks the visible projects only, so unarchiving ties two ranks and board order puts the unarchived one first | premise | TRUE | `P-4 ranks: {'pa': 0, 'pb': 1, 'pc': 0} \| order: ['pa', 'pc', 'pb']` | the rank after the last shown (HLR-2304) |
| P-5 | `ProjectPicker._move_target` never reads its third parameter | premise | TRUE | `P-5 signature: (self, proj: 'Project', bid: 'str \| None', _boards: 'dict') -> 'None' \| `_boards` read in the body: False` | the parameter removed (HLR-2306) |
| P-6 | On this filesystem a second `os.open(..., O_CREAT \| O_EXCL)` of an existing file raises `FileExistsError` | premise | TRUE | `P-6 second O_EXCL create: FileExistsError` | the lock file (LLR-2301.1) |
| P-7 | Textual's public `border_title` holds the title as escaped markup, whose parse is the title's own text | premise | TRUE | `P-7 public border_title: '▶ \\[@click=app.quit]x\\[/]' \| Text.from_markup(...).plain: '▶ [@click=app.quit]x[/]'` (Textual 8.2.8) | the test reads `border_title` (HLR-2306) |

- **Premise evaluation:** 7 premise(s) · ✅ TRUE ×7

### 2.8 Fork preconditions (C-52) — MANDATORY, and the declared empty when the batch does not fork

- **Fork preconditions:** none — this batch runs one lane: three increments in order on one branch, one owner (the orchestrator) holds the trunk.

---

## 3. High-level requirements (HLR)

### HLR-2301 — Registry writes never erase another instance's
- **Traceability:** US-2301
- **Ledger:** LED-2026-10-20-batch-02.1, LED-2026-10-20-batch-02.2
- **Statement:** When taskboard registers, creates, edits, archives or records the opening of a board, the system shall, holding the advisory lock `boards.json.lock` beside the registry, read `boards.json` as it is on disk at that moment, apply only that one change to what it read and write the result atomically, and then hold that result in memory (an entry only memory holds stays in memory); if the lock is busy for more than `LOCK_WAIT` seconds, then the system shall raise an `OSError` naming `boards.json` as busy (`… is busy — another taskboard is writing it; try again in a few seconds (<the lock's path>)`) and change nothing on disk, nor in memory but for the opening recorded by `touch`, which keeps `last` in memory and reports the error as today's `save_error` warning; if the file cannot be read at that moment, then nothing shall be written; if it cannot be parsed, then its bytes shall be copied aside first (unless they are empty or already the copy this registry's load made) and nothing written when no copy can be made; a regular lock file whose time is more than `LOCK_STALE` seconds from now shall be taken over; a lock shall be removed only by the holder that made it; no lock file shall remain after a write; a one-board user with no registry file still gets none; `taskboard --board PATH` while the registry is busy shall exit with status 1 and the busy message on stderr, never a traceback.
- **Rationale (informative):** the backlog item; the existing notices (`The board was not created: …`, `… renamed: …`, `… archived: …`) carry the error text, so no new UI.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_boards_concurrency.py -k "TC_2301 or AT_2301"`
- **Numeric pass threshold:** AT-2301: the round's four boards (`last` Personal) under the seam home, calendar and clock frozen, `LOCK_WAIT` 0.2, `open_app(None)` at 160×45 → the home; while it runs a second `Registry.load(...)` creates `Other desk` on disk; then `n`, the name `Fresh`, `tab`, `enter` → `boards.json` lists `other-desk`, `fresh` and the four round boards; `B` shows cards titled `Other desk` and `Fresh`. With `boards.json.lock` written by the test (fresh, the marker bytes `another taskboard`), `n`, `Late`, `tab`, `enter` → a notice starting `The board was not created: boards.json is busy`, `boards.json`'s bytes unchanged, no `boards/late/`, the lock still holding the test's marker; no `*.lock` under the home after the app exits.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** a board another window made is still there after this window creates one; a busy registry says so and loses nothing.
  - **Shipped surface:** `taskboard` (`__main__.open_app`) → the home (`B`, `n`), `boards.json`.
  - **Acceptance test(s):** AT-2301
  - **Boundary catalog (QC-3):** ☑ boundary (a lock `LOCK_STALE` + 1 s old or + 1 s in the future: taken over; `LOCK_STALE` − 1 s old: busy; a directory at the lock's name: busy, never removed) ☑ empty (no registry file: the change applied to a copy of memory; a one-board `touch` with no file: no lock taken, nothing written; an empty registry file: written over) ☑ invalid (the registry unparseable at commit: copied aside then written; no copy possible: nothing written) ☑ error (a failing atomic swap; a lock busy past `LOCK_WAIT` for each writer; the read failing at commit; a taken-over holder's exit leaving the new lock)
  - **Negative control:** on `base_ref` AT-2301 is RED: the app's create writes its in-memory registry over the other instance's `Other desk` (P-2; `evidence/red-001.txt` — planned).

### HLR-2302 — A move holds its target while it rewrites it
- **Traceability:** US-2301
- **Ledger:** LED-2026-10-20-batch-02.1, LED-2026-10-20-batch-02.2
- **Statement:** When a move is carried out, the system shall hold the advisory lock `<target file name>.lock` beside the target board file from the check that the target is unchanged since the move was planned until the target is saved, renewing it after the byte copies; if that lock is busy for more than `LOCK_WAIT` seconds, then the system shall stop the move before writing anything (no backup, no board file, no log) with an `OSError` naming the target board as busy (`<target board name> is busy — …`), and the move's existing notice shall then read `The move stopped: <reason>. Done: nothing.` without its backups sentence, which it keeps only when something was done.
- **Rationale (informative):** the backlog item; the stale-plan check (the target's mtime and size, batch 2026-10-20-batch-01) becomes a real read-modify-write when another instance's move takes the same lock.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_boards_concurrency.py -k "TC_2302 or AT_2302"`
- **Numeric pass threshold:** AT-2302: the round's boards, Main open (`last` Main), `escape`, `P`, `down`, `m`, `down`, `enter` → the confirmation; the test writes `boards/client-retail-rag/board.json.lock` (the marker `another taskboard`); `enter` → a notice starting `The move stopped: Client · Retail RAG is busy`, holding `Done: nothing.` and not the word `backups`; every file under the home byte-identical (the lock with the test's marker among them); the lock removed, `m`, `down`, `enter`, `enter` (the picker still open) → `Moved Retail RAG · pilot to Client · Retail RAG …`, Client's file holds the project's 7 tasks, and no `*.lock` is left under the home.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** a move into a busy board stops, says why, and writes nothing.
  - **Shipped surface:** the projects modal's `m`, the confirmation, the two board folders.
  - **Acceptance test(s):** AT-2302
  - **Boundary catalog (QC-3):** ☑ boundary (the target lock stale: taken over, the move done) ☐ empty — none ☐ invalid — none beyond HLR-2206 of batch 2026-10-20-batch-01 ☑ error (the lock busy; the target changed while the lock was awaited: refused as changed, nothing written)
  - **Negative control:** on `base_ref` AT-2302 is RED: the move ignores the lock file and writes both boards (`evidence/red-001.txt` — planned).

### HLR-2303 — A move keeps a copy of the history it rewrites
- **Traceability:** US-2302
- **Ledger:** LED-2026-10-20-batch-02.1, LED-2026-10-20-batch-02.2
- **Statement:** When a move is carried out and the source folder holds `history.jsonl`, the system shall copy its bytes, streamed, to the first free name of `history.jsonl.pre-move-<date>`, `-2`, … (created exclusively, never replacing a copy, a partial copy removed when the copy fails) together with the two board files' copies, before anything is written, and the move's steps shall name `copied history.jsonl`.
- **Rationale (informative):** security N1: the rewrite turns an undecodable byte of a kept line into U+FFFD; the copy keeps the original.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_boards_concurrency.py -k "TC_2303 or AT_2303"`
- **Numeric pass threshold:** AT-2303: the round's boards, Main's `history.jsonl` = `{"task": "tr3", "to": "Doing"}\n\xff\xfe kept\n`, the move of `Retail RAG · pilot` to Client · Retail RAG by keys → `history.jsonl.pre-move-2026-10-20` beside Main's board holds exactly those bytes; Client's folder holds no `history.jsonl.pre-move-*`.
- **Priority:** medium
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** the history's original bytes are kept beside the source after a move.
  - **Shipped surface:** the projects modal's `m`, the source board's folder.
  - **Acceptance test(s):** AT-2303
  - **Boundary catalog (QC-3):** ☑ boundary (a second move the same day: `-2`) ☑ empty (no `history.jsonl`: no copy, no step) ☐ invalid — none (the bytes are copied as they are) ☐ error — none beyond HLR-2206
  - **Negative control:** on `base_ref` AT-2303 is RED: no `history.jsonl.pre-move-*` exists after a move (P-3; `evidence/red-001.txt` — planned).

### HLR-2304 — An unarchived project never ties a presentation rank
- **Traceability:** US-2303
- **Ledger:** LED-2026-10-20-batch-02.1, LED-2026-10-20-batch-02.2, LED-2026-10-20-batch-02.3
- **Statement:** When the operator unarchives a project that holds a `present_rank`, the system shall keep that rank when no other project the presentation lists holds the same rank, and otherwise set it to one more than the largest `present_rank` among the other projects the presentation lists, before the board is saved; archiving and unarchiving a project without a rank shall leave its rank unset.
- **Rationale (informative):** A-10: today the unarchived project keeps a rank another project has taken, and board order then puts it first (P-4); an archive undone at once keeps its place (ux UX-1).
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_present_all.py -k "TC_2304 or AT_2304"`
- **Numeric pass threshold:** AT-2304: the round's presentation board (`tests/present_portfolio_board.py`) at 160×45, the selection on its cursor task; `R`, `3`, `shift+down`, `escape` (every shown project ranked); `P`, `down` (Customer Portal), `x`, `tab`, `enter`, `escape` (archived with its tasks); `R`, `3`, `shift+down`, `escape` (the others re-ranked, one of them on Customer Portal's old rank); `P`, `down`, `x`, `escape` (unarchived); `R`, `3` → in view 3 the timeline lists `Customer Portal` after every other ranked project, and the file's `present_rank` values are pairwise distinct with Customer Portal's the largest. An archive and an unarchive with no reorder between keep Customer Portal's rank and place (TC-2304).
- **Priority:** medium
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** the presenter's order stays as set; a project whose rank was taken while it was archived comes back last, never tied.
  - **Shipped surface:** `P` → `x`; `R` → `3`; the board file.
  - **Acceptance test(s):** AT-2304
  - **Boundary catalog (QC-3):** ☑ boundary (no tie: the rank kept; a tie: the largest shown rank + 1, a rank held by a project hidden in the presentation counted; the unarchived project the only ranked one: kept) ☑ empty (no project ranked: the rank stays unset) ☐ invalid — none ☐ error — none
  - **Negative control:** on `base_ref` AT-2304 is RED: `Customer Portal` comes back tied with the project that took its rank and is listed before it (P-4; `evidence/red-002.txt` — planned).

### HLR-2305 — `~` in the registry is the home the suite's seam names
- **Traceability:** US-2304
- **Ledger:** LED-2026-10-20-batch-02.1, LED-2026-10-20-batch-02.2
- **Statement:** Where a registry path or a path given to `register` starts with `~` followed by a separator or is `~` alone, the system shall read that `~` as `Path.home()`, never as the environment's `HOME`/`USERPROFILE`, and the registry shall hold the path so normalised (absolute) from its load on, so every reader of an entry's path opens the same file; any other path, `~user` among them, is read as written (relative, so skipped on load).
- **Rationale (informative):** G-9: the suite patches `Path.home` only, so a test writing a `~` path through the shipped resolution would reach the real home; in production `Path.home()` and `expanduser` agree, so nothing changes for the operator.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_boards_concurrency.py -k "TC_2305 or AT_2305"`
- **Numeric pass threshold:** AT-2305: the environment's `HOME` and `USERPROFILE` set to a second temporary folder holding its own `.taskboard/side/board.json` (a task `Env task`), the seam home holding `.taskboard/side/board.json` (a task `Seam task`) and a registry listing Main (`last` Main) and `~/.taskboard/side/board.json` as `Side`; `open_app(None)` at 160×45 → the home, the cursor on Main; `right`, `enter` → the board view holds `Seam task` and not `Env task`; the second folder's files are byte-identical after the app exits.
- **Priority:** medium
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** a `~` board opens from the home the suite controls, never from the environment's.
  - **Shipped surface:** the home's `enter`; the board view.
  - **Acceptance test(s):** AT-2305
  - **Boundary catalog (QC-3):** ☑ boundary (`~` alone; `~/x`; `~\x` on Windows) ☐ empty — none ☑ invalid (`~user/x`: relative, skipped on load as any relative path) ☐ error — none
  - **Negative control:** on `base_ref` AT-2305 is RED: the `~` entry is kept raw, read relative to the working directory, so its card reads `file missing` and `enter` opens nothing (architect A-1; `evidence/red-001.txt` — planned).

### HLR-2306 — The suite reads what the screen shows; no dead parameter or import
- **Traceability:** US-2304
- **Ledger:** LED-2026-10-20-batch-02.1, LED-2026-10-20-batch-02.2
- **Statement:** The system shall carry no parameter of `ProjectPicker._move_target` it does not read, and the suite shall: hold no unused module-level name in `tests/test_boards_forms.py`; read a card's title through Textual's public `border_title`, never `_border_title`; check `B` itself among the `?` help's keys in AT-2204 and reach `R` there by keys; check in AT-2104 the timeline row the cursor is on; drive `u` in view 2 of the presentation; and, in the presentation's AT nodes, read the cursor from the frame where the frame shows it.
- **Rationale (informative):** the reviewers' findings (BACKLOG); a test that reads private state passes while the screen is wrong.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_hygiene.py tests/test_boards_forms.py tests/test_boards_home.py tests/test_present_all.py`
- **Numeric pass threshold:** AT-2306: the hygiene law passes on the tree — `inspect.signature(ProjectPicker._move_target)` names exactly `self, proj, bid`; no `tests/*.py` holds the text `._border_title` (the law builds its needle by concatenation); every name `tests/test_boards_forms.py` binds by an import or a plain module-level assignment is read in it (its `test_*` functions and fixtures aside); and each hardened node goes RED under its recorded mutation (increment 003's battery).
- **Priority:** low
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** the suite fails when the behaviour its nodes name breaks.
  - **Shipped surface:** the test suite (`pytest`).
  - **Acceptance test(s):** AT-2306
  - **Boundary catalog (QC-3):** ☑ boundary (a test file naming `_border_title` in a comment: the law reads the text, so it counts) ☐ empty — none ☑ invalid (a third parameter added back; `PAYLOADS` added back) ☐ error — none
  - **Negative control:** on `base_ref` AT-2306 is RED: `_move_target` has four parameters and `tests/test_boards_forms.py` reads `_border_title` (P-5, P-7; `evidence/red-003.txt` — planned).

---

## 4. Low-level requirements (LLR)

> Each LLR decomposes an HLR into a verifiable property at the implementation level.
> Same regime: EARS syntax owed in `full`, recommended in `core`. ID format: `LLR-<HLR>.<M>`.

### LLR-2301.1 — `boards.file_lock`
- **Traceability:** HLR-2301, HLR-2302
- **Ledger:** LED-2026-10-20-batch-02.1, LED-2026-10-20-batch-02.2
- **Statement:** `taskboard/boards.py` (NEW symbols — created in increment 001) shall provide `LOCK_WAIT = 2.0`, `LOCK_STALE = 10.0` and a context manager `file_lock(path, label=None)` whose lock is `<resolved path>.lock`, created with `os.open(..., O_CREAT | O_EXCL | O_WRONLY)` and holding a random token; on `FileExistsError` or `PermissionError` it removes the lock only when `os.lstat` shows a regular file whose `st_mtime` is more than `LOCK_STALE` seconds from now (past or future) and unchanged at a second `lstat`, any `OSError` there read as busy, then — on every pass — raises `OSError("<label or file name> is busy — another taskboard is writing it; try again in a few seconds (<lock path>)")` once `LOCK_WAIT` seconds have passed, else sleeps 0.05 s and retries; it yields a heartbeat (`os.utime` of the lock); on exit it removes the lock only while the lock still holds its token.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_boards_concurrency.py -k TC_2301`
- **Numeric pass threshold:** TC-2301 (lock): inside `file_lock(p)` the lock file exists and a nested `file_lock(p)` with `LOCK_WAIT` 0.2 raises `OSError` whose text starts `p.name + " is busy — another taskboard is writing it; try again in a few seconds"` after ≥ 0.2 s and < 2 s, the holder's lock left in place; with a label the text starts with the label; after the block, or an exception in it, no lock file; a lock file 11 s old or 11 s in the future is taken over at once (< 0.2 s); one 9 s old is busy and keeps its bytes; a directory at the lock's name is busy and stays; a holder whose lock file was rewritten by another holder leaves it on exit.
- **Negative control:** TC-2301 goes RED when the lock is not exclusive, when it is not removed on exit or on an exception, when a stale lock blocks, when a fresh one is taken over, when the exit removes another holder's lock, when a directory is removed (mutations at increment 001 — planned).
- **Boundary catalog:** ☑ boundary (`LOCK_STALE` ± 1 s; a future time) ☐ empty — none ☑ invalid (a directory at the lock's name) ☑ error (an exception inside the block; a taken-over holder's exit)

### LLR-2301.2 — `Registry._commit` and the registry's writers
- **Traceability:** HLR-2301, HLR-2305
- **Ledger:** LED-2026-10-20-batch-02.1, LED-2026-10-20-batch-02.2
- **Statement:** `Registry.load` shall read through a new `Registry._read(path, main_path) -> Registry | None` (None for unparseable bytes; a failed read raises, and `load` treats it as unreadable as today; the copy-aside stays in `load`), storing each kept entry's path `~`-normalised (LLR-2305.1); a new `Registry._commit(change)` shall create the registry's folder, take `file_lock(self.path)`, read `_read(self.path, self.main_path)` when the file exists (a failed read raises with nothing written; unparseable bytes are set aside by `_set_aside` — empty, or equal to this registry's load copy, or copied now by `_keep_aside` — else `OSError` with nothing written) and else take a deep copy of `self`, call `change(fresh)`, write `fresh.save()`, then adopt `fresh` into `self` — each entry whose id `self` holds updated in place (the same `BoardEntry` object), the others taken as they are, an entry only `self` holds (by id and path) kept at the end, `last` taken — and return `change`'s result; `register`, `create`, `edit`, `archive` and `touch` shall each make their change inside `_commit` on the fresh registry (an entry this registry holds but the file lacks carried over for `edit`, `archive`, `touch`); `register` of a path this registry holds un-archived shall return it without writing; `touch` shall set `last`/`last_opened` in memory first and commit only when the registry holds more than one board or its file exists, never after an unreadable read, a failed commit kept as `save_error`; `create` shall pick its id from the fresh registry and remove the folder it made when the write fails; `save()` stays the atomic write of the registry's own entries. `taskboard/__main__.py::main` shall turn an `OSError` from `open_app` into `parser.exit(1, "taskboard: <reason>\n")`.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_boards_concurrency.py -k TC_2301`; `python -m pytest -q -p no:cacheprovider tests/test_boards.py tests/test_boards_forms.py`
- **Numeric pass threshold:** TC-2301 (registry): two registries A and B loaded from one file; A creates `From A`; B (stale) then edits `course-docker`, archives `client-retail-rag`, registers a new path, creates `From A` again (→ id `from-a-2`, picked against the file) and touches `personal` — after each, the file lists `from-a` and every earlier change, and B's entries equal the file's; B's `BoardEntry` object for `course-docker` is the same object before and after; A, stale in turn, edits its board and keeps B's changes; with the lock busy, each of `create`, `edit`, `archive`, `register` raises `OSError`, the file's bytes and B's entries unchanged, no `create` folder; with `Registry.save` failing, the same and `create`'s folder gone; the file made unparseable after B loaded → B's edit keeps its bytes as `boards.json.corrupt` and writes; unparseable with `_keep_aside` returning None → `OSError`, the bytes unchanged; the read raising `PermissionError` → `OSError`, the bytes unchanged; a one-board `touch` with no file creates neither `boards.json` nor `boards.json.lock`; `main()` with `--board` and the lock busy → `SystemExit(1)`, `boards.json is busy` on stderr; no `*.lock` left; the existing nodes of `tests/test_boards.py` and `tests/test_boards_forms.py` pass unchanged.
- **Negative control:** TC-2301 goes RED when a writer saves its own entries instead of the fresh file's, when the lock is not taken, when adoption replaces entry objects, when the fresh read skips the copy-aside, when a failed copy still writes, when a failed read still writes (mutations at increment 001 — planned).
- **Boundary catalog:** ☑ boundary (an entry the file lacks: carried over; an entry only memory holds: kept in memory) ☑ empty (no file: a copy of memory; an empty file) ☑ invalid (the file unparseable at commit; no copy possible) ☑ error (the save failing; the lock busy; the read failing)

### LLR-2302.1 — `move_project` holds the target's lock
- **Traceability:** HLR-2302
- **Ledger:** LED-2026-10-20-batch-02.1, LED-2026-10-20-batch-02.2
- **Statement:** `move_project` shall take `file_lock(dst.path, names[1])` (through an `ExitStack`) after the refusal check and before the stale-plan check (`_stamp(dst.path) != plan.dst_stamp`), renew it after the byte copies, and release it right after `saved the target`, or in a `finally` when anything before that raises; a busy lock is raised like every other failure, carrying `.steps == []` and `.board is None`. `taskboard/modals.py::ProjectPicker._move_confirmed` shall add its backups sentence to the stopped-move notice only when `exc.steps` is not empty.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_boards_concurrency.py -k TC_2302`
- **Numeric pass threshold:** TC-2302: with the target's lock held (fresh) and `LOCK_WAIT` 0.2 → `OSError` text starting `Client · Retail RAG is busy`, `.steps == []`, `.board is None`, every file of the home byte-identical; during `save_atomic` (spied) the target's lock file exists for the target and not for the source; after the move no lock file; a stale target lock (11 s old) → the move done; the target rewritten while the plan waited → refused as changed, nothing written, no lock left.
- **Negative control:** TC-2302 goes RED when the lock is skipped, taken after the backups, or held past the target's save (mutations at increment 001 — planned).
- **Boundary catalog:** ☑ boundary (a stale lock) ☐ empty — none ☐ invalid — none ☑ error (the lock busy)

### LLR-2303.1 — `move_project` copies the source history
- **Traceability:** HLR-2303
- **Ledger:** LED-2026-10-20-batch-02.1, LED-2026-10-20-batch-02.2
- **Statement:** right after the two board files' `_backup`, `move_project` shall call `_backup(src.path.parent / "history.jsonl", day)` and append `copied history.jsonl` to its steps when a copy was made; `_backup` shall stream the bytes (`shutil.copyfileobj`) into its exclusively created copy and remove that copy when the copy fails.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_boards_concurrency.py -k TC_2303`
- **Numeric pass threshold:** TC-2303: a history with an undecodable byte → `history.jsonl.pre-move-2026-10-20` holds its exact bytes and `steps[:3] == ["copied board.json", "copied board.json", "copied history.jsonl"]`; a second move the same day → `history.jsonl.pre-move-2026-10-20-2`, the first copy unchanged; no history → no copy and no such step; a failing target save → the history copy exists and the history is unchanged; a copy failing midway → no `history.jsonl.pre-move-*` left.
- **Negative control:** TC-2303 goes RED when the copy is skipped, taken after the rewrite, or overwrites an earlier copy (mutations at increment 001 — planned).
- **Boundary catalog:** ☑ boundary (a second copy) ☑ empty (no history) ☐ invalid — none ☑ error (the target save failing)

### LLR-2304.1 — `ProjectPicker._do_archive_toggle` ranks an unarchived project
- **Traceability:** HLR-2304
- **Ledger:** LED-2026-10-20-batch-02.1, LED-2026-10-20-batch-02.2
- **Statement:** in `taskboard/modals.py`, `_do_archive_toggle` shall, when the toggle unarchives a project whose `present_rank` is not None and another project of `self.board.visible_projects(False)` holds the same rank, set it to `max(ranks) + 1` over the `present_rank` values that are not None of those other projects, before `self.board.save()`; with no tie the rank is kept.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_present_all.py -k TC_2304`
- **Numeric pass threshold:** TC-2304: three projects ranked 0, 1, 2, the first archived, the other two re-ranked 0, 1, the first unarchived through the picker → ranks {first: 2, others 0, 1}; archived and unarchived with no reorder → its rank kept; the only ranked project unarchived → kept; an unranked project unarchived → None; archiving a ranked project leaves its rank.
- **Negative control:** TC-2304 goes RED when the rank is kept on a tie, when it is always re-ranked, when the archived projects' ranks are counted, when the project's own rank is counted (mutations at increment 002 — planned).
- **Boundary catalog:** ☑ boundary (a tie; no tie; the only ranked project) ☑ empty (no rank) ☐ invalid — none ☐ error — none

### LLR-2305.1 — `boards._expand_home`
- **Traceability:** HLR-2305
- **Ledger:** LED-2026-10-20-batch-02.1, LED-2026-10-20-batch-02.2
- **Statement:** `taskboard/boards.py` (NEW — created in increment 001) shall provide `_expand_home(p) -> Path` (named apart from `modals._home_path`, which shortens a path the other way): `Path.home() / rest` for `~`, `~/rest` or `~<os.sep>rest`, else `Path(p)`; `_key`, `Registry._read`'s absolute-path check and stored path, and `register` shall use it in place of `Path(p).expanduser()`.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_boards_concurrency.py -k TC_2305`
- **Numeric pass threshold:** TC-2305: with `HOME`/`USERPROFILE` set to a second temporary folder: `_expand_home("~") == Path.home()`, `_expand_home("~/a/b") == Path.home() / "a" / "b"`, on Windows `_expand_home("~\\a") == Path.home() / "a"`, `_expand_home("~user/a") == Path("~user/a")`; a registry entry `~/side/board.json` → its stored `path` is `str(Path.home() / "side" / "board.json")` (no `~`) and `entry_for(Path.home() / "side" / "board.json")` is that entry; a `~user/…` entry skipped; `register("~/n.json")` → its path under `Path.home()`; `taskboard/boards.py` holds no `expanduser`.
- **Negative control:** TC-2305 goes RED with `expanduser` restored at `_key`, at the load check or at `register`, or with the stored path left raw (mutations at increment 001 — planned).
- **Boundary catalog:** ☑ boundary (`~` alone) ☐ empty — none ☑ invalid (`~user`) ☐ error — none

### LLR-2306.1 — `ProjectPicker._move_target(proj, bid)`
- **Traceability:** HLR-2306
- **Ledger:** LED-2026-10-20-batch-02.1
- **Statement:** `_move_target` shall take `(self, proj, bid)` and `action_move_board`'s callback shall pass those two; the picker's `boards` map stays the picker's own (it paints the cards).
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_hygiene.py tests/test_boards_move.py`
- **Numeric pass threshold:** AT-2306's signature arm passes; `tests/test_boards_move.py` passes unchanged (its AT-2206 drives the callback).
- **Negative control:** the signature arm goes RED with the parameter restored (increment 002's battery — planned).
- **Boundary catalog:** ☐ boundary — none ☐ empty — none ☑ invalid (a third parameter) ☐ error — none

### LLR-2306.2 — the hardened tests
- **Traceability:** HLR-2306
- **Ledger:** LED-2026-10-20-batch-02.1, LED-2026-10-20-batch-02.2
- **Statement:** `tests/test_boards_forms.py` shall drop `PAYLOADS` and read `Text.from_markup(card.border_title).plain` (its `Text` import then read); `tests/test_boards_home.py::test_AT_2204_the_home` shall assert a `?` help row holding the key `B` beside `Boards` and reach `R` with the selection the board opens with, not by setting `selected_task_id`; `tests/test_present_all.py::test_AT_2104_three_views_one_cursor_and_the_export` shall assert after `→` and after `↓` the timeline row, other than the tick row, that holds the cursor's `⟦` and names the cursor's project or task, in place of the tick row and `_all_cur`; `test_AT_2106_u_lists_the_hidden_and_brings_one_back` shall drive `u` in view 2 too (a task hidden with `space` first); `test_AT_2102_the_order_and_hidden_projects_survive_a_restart` shall read the rail's `▶` row in place of `_all_cur`; a new `tests/test_hygiene.py` holds AT-2306.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_hygiene.py tests/test_boards_forms.py tests/test_boards_home.py tests/test_present_all.py`
- **Numeric pass threshold:** every hardened node passes on the tree and goes RED under its mutation in increment 003's battery: `B` dropped from the help's keys (AT-2204), the cursor's `⟦` drawn on no task or project row (AT-2104), `u` unbound in view 2 (AT-2106), the rail's `▶` on another row (AT-2102); `test_AT_2104_three_views_one_cursor_and_the_export` and `test_AT_2102_the_order_and_hidden_projects_survive_a_restart` read no `_all_cur`.
- **Negative control:** each node's mutation above (increment 003's battery — planned).
- **Boundary catalog:** ☐ boundary — none ☐ empty — none ☐ invalid — none ☐ error — none

### Information Flow Contract (IFC) — C-54

> Part A in every batch; Part B when the system's boundary has components a consumer can address independently. The block syntax, its fields and the rules that read them are in `templates/ifc-template.md`, which ships with the flow and is not copied into this batch.

- **Part A — flows:**

```
FLOW: a registry change, from a key or a start to boards.json
  SOURCE : the home's n, e, x; --board PATH; the board opened at start or from the home
  NODES  :
    - fn    : boards.file_lock
      owner : LLR-2301.1
    - fn    : boards.Registry._commit, _read, _set_aside, register, create, edit, archive, touch; __main__.main
      owner : LLR-2301.2
    - fn    : boards._expand_home
      owner : LLR-2305.1
  SINK   : boards.json (and boards/<slug>/board.json for create); the app's registry in memory
```

```
FLOW: a project moved, from the confirmation to two board folders
  SOURCE : the move's confirmation (enter)
  NODES  :
    - fn    : boards.move_project (the target lock); modals.ProjectPicker._move_confirmed (the notice)
      owner : LLR-2302.1
    - fn    : boards.move_project (the history copy)
      owner : LLR-2303.1
    - fn    : modals.ProjectPicker._move_target
      owner : LLR-2306.1
  SINK   : both board files, their .pre-move copies, history.jsonl.pre-move-<date>, move-<date>.json
```

```
FLOW: an unarchive, from the projects modal to the presentation's order
  SOURCE : the projects modal's x on an archived project
  NODES  :
    - fn    : modals.ProjectPicker._do_archive_toggle
      owner : LLR-2304.1
  SINK   : board.json (present_rank) and view 3's order
```

- **Part B — boundary decomposition:** `no — the lock, the registry and the move are functions of one module addressed through the app`

---

## 5. Validation strategy

### 5.1 Methods

> **Two layers** (per the Two-layer validation rule). Every batch declares BOTH:
> - **Layer A — white-box / functional (`TC-NNN`):** validates the HLR/LLR mechanism (the HOW). Methods: `test`, `inspection`, `analysis`.
> - **Layer B — black-box / behavioral acceptance (`AT-NNN`):** validates the user story's outcome through the shipped surface (the WHAT). Method: `acceptance`.

Layer 0: `file_lock`'s wait/stale/release paths, `_expand_home`'s forms, `_commit`'s fresh-or-copy and adoption (TC-2301, TC-2305). Layer A: TC-2301..TC-2305 at the function level (`Registry`, `move_project`, `_do_archive_toggle`). Layer B: AT-2301..AT-2305 drive the real app headless (`run_test`, keys) built by the shipped `open_app` or `TaskboardApp`, with `Path.home()` the seam's temporary folder, reading the screen, the notices and the files; "another instance" is the shipped `Registry` (or a lock file) acting on the same files from the test, the same code a second process runs. AT-2306 is the suite's hygiene law, plus increment 003's mutations proving each hardened node can fail.

### 5.2 Batch acceptance criteria
- every LLR has a passing TC; every story a passing AT through its surface;
- every new assertion RED on `base_ref` or by a recorded mutation; mutants KILLED on the new logic;
- the full suite in three sequential chunks: 0 failures; transcripts under the batch's evidence; 2936 + the new nodes;
- no `*.lock` left by any test (the conftest seam's home holds none at the end of AT-2301..AT-2303);
- no test reads or writes the real home.

---

## 6. Appendices (optional)

### 6.1 Extended glossary
### 6.2 Relevant design decisions
See `PLAN.md` §Key decisions and `docs/ARCHITECTURE.md` (amended by this batch: `file_lock`, the registry's read-modify-write, the move's lock and history copy, `~`).
### 6.3 Open risks
- **Security questions (the P1 scan):** `devflow-scan-spec.py` over this document, 2026-10-20: 65 patterns, 5 control rows ok, `flags: escape`, `security_required: true`, exit 1 (`evidence/scan-p1.txt`). The answer: `escape` (C6, input surface) — the word names the markup escaping Textual applies to a card's `border_title`, which a test now reads through the public route (HLR-2306); no new markup site is added and no file-derived text reaches markup in a new place. The batch's real input and file surfaces, judged with it: the registry's `~` paths are file-derived input, now resolved through `Path.home()` (HLR-2305; `~/../..` still leaves the home, as any absolute path a hand edit names may — no new surface, security S-4); the lock file is created exclusively beside a file the app already writes and removed by the instance that made it, or taken over after `LOCK_STALE` (an `unlink` of a `*.lock` name only, never of a board, registry or history file); the history copy is an exclusive create (`xb`) that never replaces a file. No credential, network, permission or schema change. The security-reviewer reads the lock and the copies at P2 and at increment 001 (`C5`/`C6`).
- **A plain board save takes no lock.** Two instances editing the same board still last-write-win, as today; the move's lock serialises moves only. Out of scope (§1.2).
- **A stale lock taken over while its owner still lives.** A write held longer than `LOCK_STALE` (10 s) — never the registry's milliseconds, nor a move's check-and-save — could be broken by a second instance; the registry's re-read keeps even that case from losing an entry written before.
- **Two instances breaking one stale lock at once.** Both may unlink and one recreates it; the other's `O_EXCL` then fails and waits — advisory, accepted.
- **An unwritable folder reads as busy (security S-9, architect A-8, code review F3 of increment 001).** A `PermissionError` creating the lock for another reason than a held lock (a read-only folder) is retried as busy for `LOCK_WAIT` and then reported as busy; the message names the lock's path, so the operator sees where. Accepted.
- **`~user` paths** are read as written (relative → skipped on load), where `expanduser` read them; the app never writes one.
- **A lock wait blocks the event loop (ux UX-6, architect A-4, code review F6 of increment 001).** A busy lock is retried on the app's thread for up to `LOCK_WAIT` (2 s): the screen does not repaint and keys queue meanwhile. A collision is rare (a write holds the lock for milliseconds) — accepted; a waiting indicator is a note for the visual round.
- **The source history outside the lock (security S-5).** The move rewrites the source's `history.jsonl` after the target's lock is released and holds no lock on the source; a line another instance appends in between is in neither the copy nor the rewrite. Out of scope with the source lock (§1.2), recorded here.
- **The takeover race (architect A-3, security S-2).** Two instances can both find one lock stale; the `lstat` re-check and the token-checked release narrow it, and the re-read under the lock keeps every entry written before. A holder past `LOCK_STALE` renews its lock only in the move (the heartbeat after the copies).
### 6.4 Phase-1 reconciliation log — moved to the ledger (§7)

### 6.5 Requirement amendments — moved to the ledger (§7)

---

## 7. The ledger — authored as a SEPARATE FILE

The fence below is the ledger's seed: `devflow-init.py` writes it to `01-requirements-ledger.md`. The shape of an entry is in the field guide.

```markdown
# Requirements ledger — taskboard — Batch 2026-10-20-batch-02

> Append-only. Entries are added in chronological order and never rewritten. The live
> contract is `01-requirements.md`; this file records how it came to say what it says.
> Every entry names the requirement it amends; every requirement names its entries. `V26`
> compares the two sets of pairs both ways.

_No entries yet. The first amendment to the live contract writes the first one, in the
shape the field guide's §7 shows (`req-template.part2.md` in the guide directory init prints), and nothing
above this line is ever edited._
```
