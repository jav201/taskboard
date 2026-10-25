# Requirements Document — taskboard — Batch 2026-10-24-batch-02

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
*(Informative text. Describes the document's objective.)*

### 1.2 Scope
*(What this batch covers and what it does NOT cover.)*

### 1.3 Definitions, acronyms, abbreviations
| Term | Definition |
|------|------------|
| | |

### 1.4 References
*(Related documents, standards, external tickets.)*

### 1.5 Document overview
*(How this document is structured.)*

---

## 2. Overall description

### 2.1 Product perspective
*(How the change fits into the larger system.)*

### 2.2 Product functions
*(High-level list of functional capabilities.)*

### 2.3 User characteristics
*(Roles, permissions, expected experience levels.)*

### 2.4 Constraints
*(Technological, regulatory, business.)*

### 2.5 Assumptions and dependencies
*(What we take for granted. If an assumption fails, the batch is invalidated.)*

### 2.6 Source user stories

| ID | User Story | Source | DoR status |
|----|------------|--------|------------|
| US-2701 | As an operator with several boards, I want the start screen to touch nothing until I pick a board, so that a second window with another board open no longer alarms me that the board is "already open" while I am still on the home. | The operator, 2026-10-23: «Me es útil incluso tener dos terminales abiertas, cada una con un board distinto… vi el mensaje de que ya tenía el board abierto y tenía que cerrarlo, a pesar de que estaba en la ventana de selección de Boards.» · approval 2026-10-24: «Ok, arréglalo.» · `.dev-flow/COMMISSION-home-deferred-start.md` (HD-1..HD-4) | READY |
| US-2702 | As an operator working in two windows, I want people and mark classes added in the other window to appear without a restart, so that the `@` picker, the `alt+m` Select and `#` reflect the directories as they are on disk. | The commission's second defect (HD-5) · BACKLOG item (architect A-7, accepted): «a person another window adds shows here after a restart or this window's next write» | READY |

#### Refinement log (one block per story)

**US-2701 — the home defers the board's start**
- **INVEST:** I ✓ · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality (V, N):** user = the operator running several boards in two terminals · outcome = the home at start writes nothing, announces nothing and opens no board modals until a board is picked; picking a board (its card's `enter`, or `esc`/`back`) starts exactly that board once; the start-up modals then open over the board · why = the false "already open" notice and the blank screen behind the start-up modals (BACKLOG D-12) · out of scope = any other home behaviour, any change to the single-board start, `--open`, or `B` pressed later.
- **Feasibility (E, S):** implementation path = read in `TaskboardApp.on_mount` / `_open_board` / `switch_board` and the `BoardsHome` actions: defer the write/announce/modal half of the start behind a per-board "started" flag · dependencies/unknowns = none — the commission records the defect read in the code · fits one batch? = yes.
- **Evaluability (T) — behavioral, black-box:** "When the app starts with two boards and another window's presence marker on the default board, the user observes on the home: no open-twice notice, no marker written, the board file's bytes unchanged; after `enter` on the card: the notice once, the marker written, the sweep run." (AT-a; AT-b..AT-d in Phase 1.)
- **Open questions:** none — the operator approved the fix as described («Ok, arréglalo.»), no prototype needed.
- **Classification:** READY — observable through the home, the notices and the board file.

**US-2702 — the directories stay fresh**
- **INVEST:** I ✓ · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality (V, N):** user = the operator in either window · outcome = the `@` picker, the `alt+m` class Select, `#` and the `/` `@…`/`#…` search re-read `people.json` / `marks.json` when the file changed (mtime or size) and show what the other window wrote; a failed re-read keeps the in-memory directory and notifies once · why = a person or class added in another window does not appear until restart (BACKLOG A-7) · out of scope = any other refresh path, the team roster, cross-window deletion semantics.
- **Feasibility (E, S):** implementation path = a cheap mtime/size-gated re-read helper on `Directory` (people.py / marks.py), called at the four open sites in app.py · dependencies/unknowns = none · fits one batch? = yes.
- **Evaluability (T) — behavioral, black-box:** "When a second `Directory` instance (the other window) appends a person to `people.json`, the user observes the new person in the `@` picker the next time the editor opens; the same holds for a class in the `alt+m` Select and in `#`." (AT-e; AT-f for the unreadable re-read.)
- **Open questions:** none.
- **Classification:** READY — observable through the pickers and the marks manager.

### 2.7 Premise evaluation (C-43) — MANDATORY, one row per premise

| # | Premise, as a truth-apt proposition | Tier (axiom · hypothesis · premise) | Verdict | Executed evidence (command output / `file:line` — **NOT** a citation of another document) | Disposition |
|---|---|---|---|---|---|
| 1 | At start with more than one board, `TaskboardApp.on_mount` pushes `BoardsHome` and then calls `_open_board(at_mount=True)`, which migrates links, sweeps old done, enters presence and opens the start-up modals — before the user picks a board. | premise | ✅ TRUE | `grep -n "at_mount" taskboard/app.py` → `app.py:1307` `self.push_screen(BoardsHome())` · `app.py:1308` `if self._open_board(at_mount=True):` · `app.py:1410` `self._migrate_links(at_switch=not at_mount)` · `app.py:1417` `if at_mount:` | the defect's pre-image; HD-1 removes the write/announce/modal half of that start |
| 2 | `switch_board` returns early when `bid == self.board_id`, so a deferred default board needs the early-return path to still run the start. | premise | ✅ TRUE | `grep -n "def switch_board" taskboard/app.py` → `app.py:1453` (the early return read at P1 increment 001) | HD-1's «esc / back runs the deferred start» leans on it |
| 3 | `self.people` and `self.marks` are loaded once at mount; a file the other window changes is not re-read until restart. | premise | ✅ TRUE | `grep -n "def load" taskboard/people.py taskboard/marks.py` → `people.py:119` · `marks.py:67`; the only loads are the mount's (read at P1) | HD-5's pre-image |
| 4 | The directories' cross-window writes are safe today (read-modify-write under a lock), so re-reading at open time inherits that safety. | hypothesis | ✅ TRUE (pending the lock read) | asserted by the commission (§The defect, defect 2); the lock is read at P1 increment 002 | relied on, not re-proven |
| 5 | The suite's baseline at this batch's base is 3235 passed + 1 environmental skip (the clipboard arm TC-1902 / G-001, batch 2026-10-24-batch-01's P4), so P4 expects the same plus this batch's new nodes. | premise | ✅ TRUE | `.dev-flow/2026-10-24-batch-01/04-validation.md` (its P4 transcripts) · BACKLOG G-001 | P4's expected totals derive from it |

- **Premise evaluation:** 5 premise(s) · ✅ TRUE ×5 — the batch's derivation stands on all five; 4 is the commission's assertion, re-read at the increment it binds.

### 2.8 Fork preconditions (C-52) — MANDATORY, and the declared empty when the batch does not fork

| # | Condition (`C-52`) | Discharged? | The executed evidence |
|---|---|---|---|
| 1 | **Frozen contract** — no shared interface is touched inside a lane; one that must change returns to the trunk (trigger A3) | ✅ | not applicable — one lane, no frozen interface is re-signed (A3 judged not fired at intake) |
| 2 | **Disjoint FILE sets**, not just modules — two lanes may not edit the same file, not even different regions | ✅ | not applicable — one lane; the commission's increments 001 and 002 run sequentially and both touch `taskboard/app.py` in sequence, never concurrently |
| 3 | **Crossed reverse census** — family B run per lane and **shared before starting**; the trunk's act, impossible from inside a lane | ✅ | not applicable — one lane; the B1 probe at intake (`grep -rln` over `tests/`) is the batch-wide census, re-run per increment cut per family B's rule |
| 4 | **One owner of the trunk** — requirements, traceability, backlog and spec are never written from a lane | ✅ | the orchestrator owns the trunk; no lane exists |

- **Fork preconditions:** none — this batch runs one lane (declared empty per C-52).

---

## 3. High-level requirements (HLR)

**The chains, one line each:** US-2701 → HLR-2701, HLR-2702, HLR-2703, HLR-2704, HLR-2705, HLR-2708 → AT-2701..AT-2705 (and the regression pin HLR-2708) · US-2702 → HLR-2706, HLR-2707 → AT-2706, AT-2707 (the commission's AT-a..AT-f map onto AT-2701..AT-2707, two ids where a letter has two beats).

### HLR-2701 — the home at start touches nothing
- **Traceability:** US-2701
- **Ledger:** LED-2701
- **Statement:** When the app starts with more than one active board and the home is shown, the system shall not run any board's migration, sweep, presence announcement, team start or milestone offer, shall not write any board file or presence marker for this window, and shall show no start-up modal, until the user leaves the home onto a board.
- **Rationale (informative):** the operator saw the false «already open» notice while still on the home; the commission (HD-1) read the cause in the code: `_open_board(at_mount=True)` runs the whole start under the home. This HLR also covers quitting from the home (`q`): nothing is ever written.
- **Validation:** `test`
- **Executed verification:** `env -u NO_COLOR python -m pytest -q tests/test_home_deferred_start.py -k AT_2701` (node minted at P3; RED probe executed at P1, `evidence/red-p1.txt`)
- **Numeric pass threshold:** on the home, with a foreign marker planted on the default board and a sweepable old-done task in it: notifications titled `Boards · open twice` = 0; this window's presence markers for the default board = 0 (only the foreign one exists); the default board file's bytes = the pre-start bytes.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** the home paints its cards and nothing else happens — no notice, no modal, and the boards on disk (file bytes, presence markers) are exactly as before the start.
  - **Shipped surface:** `BoardsHome` at start (`TaskboardApp.on_mount` with more than one active board).
  - **Acceptance test(s):** AT-2701
  - **Boundary catalog (QC-3):** ☐ empty (no boards — the home never shows) ☐ boundary (a default board that is sweepable AND foreign-marked — both deferred halves exercised at once) ☐ invalid (a board file unreadable — the home card already handles it, unchanged) ☐ error (none new)
  - **Negative control:** executed at P1 against `base_ref`: the future assertions fail — the open-twice notice fired at mount, this window's marker was written, and the sweep changed the file (`evidence/red-p1.txt`, probe AT-2701). The node-minted RED lands in increment 001's evidence (C-40).

### HLR-2702 — leaving the home runs the deferred start exactly once
- **Traceability:** US-2701
- **Ledger:** LED-2702, LED-2702.1r2, LED-2702.1r3
- **Statement:** When the user leaves the home onto the default board — `enter` on its card, or `esc`/`back` from the home — the system shall run that board's deferred start exactly once: the link migration, the sweep of old done work, the presence marker, the team-mode start and the milestone offer; pressing `B` and then `esc` later shall not run it again.
- **Rationale (informative):** HD-1 names the two paths onto the default board and pins «exactly once»; the same-board early return of `switch_board` (`app.py:1458`) must not skip the pending start, and must not re-run it either.
- **Validation:** `test`
- **Executed verification:** `env -u NO_COLOR python -m pytest -q tests/test_home_deferred_start.py -k "AT_2702 or AT_2703"` (P3)
- **Numeric pass threshold:** after `enter` on the default card (or `esc` at the home): the open-twice notice fired exactly once, this window's marker exists, and the board file's bytes changed iff the sweep ran (the sweepable task archived; the AT fixture's board carries `RENUMBER_NOTICE_KEY`, a completed link migration and the milestones mark, so the deferred start's other writers are no-ops there); a `B`-then-`esc` round trip later adds no second notice, no second marker, and no second sweep (the board file bytes stay put).
- **Priority:** high
- **Acceptance (black-box):**
  - **Observable outcome:** the chosen board comes up started — its real start notices appear once, over the board.
  - **Shipped surface:** `BoardsHome.action_open` / `BoardsHome.action_back` and the board beneath them.
  - **Acceptance test(s):** AT-2702, AT-2703
  - **Boundary catalog (QC-3):** ☐ empty (no entries — `action_open` guards, unchanged) ☐ boundary (enter lands on the already-open default board — the early-return path that must still start) ☐ invalid ☐ error (a migration failure on the deferred start: LLR-2702.4's posture — the record stays pending, the user is on the board view, the migration's own notice explains)
  - **Negative control:** the P1 probe's inverse: at `base_ref` the start runs at mount, so a node asserting «no start before leaving the home» is RED at base by the same transcript (`evidence/red-p1.txt`); the executed mutation battery at P3 reddens each arm.

### HLR-2703 — another board from the home starts as today; the default is never written
- **Traceability:** US-2701
- **Ledger:** LED-2703
- **Statement:** When the user picks a board other than the default from the home, the system shall start that board as it does today and shall not write the default board's file — the default board, never started, is never written.
- **Rationale (informative):** HD-1's «picking another board» clause; the home reads every board once for its cards, and reads never write.
- **Validation:** `test`
- **Executed verification:** `env -u NO_COLOR python -m pytest -q tests/test_home_deferred_start.py -k AT_2704` (P3)
- **Numeric pass threshold:** after `enter` on the second board's card: the second board is open and started (its marker exists); the default board file's bytes = the pre-start bytes; the sweepable task in the default board is still present (not archived).
- **Priority:** high
- **Acceptance (black-box):**
  - **Observable outcome:** the chosen board's work on screen; the default board exactly as it was.
  - **Shipped surface:** `BoardsHome.action_open` → `TaskboardApp.switch_board`.
  - **Acceptance test(s):** AT-2704
  - **Boundary catalog (QC-3):** ☐ boundary (the default board is sweepable and foreign-marked: picking the OTHER board must still not start or write it) — the other classes are covered by HLR-2702's and the home suite's existing arms.
  - **Negative control:** at `base_ref` the default board was started (and possibly swept) at mount — a default-board-bytes assertion is RED at base (same P1 transcript family; node-minted RED at P3).

### HLR-2704 — the start-up modals open over the board
- **Traceability:** US-2701
- **Ledger:** LED-2704
- **Statement:** When a board's deferred start runs its team-mode start or milestone offer, the system shall open those modals over the chosen board, after the home is gone — never over the home.
- **Rationale (informative):** HD-2; closes the BACKLOG item D-12 (the blank screen behind the start-up modals) of 2026-10-20-batch-03. A timing consequence of HLR-2701/2702, asserted in its own AT because the commission names it (AT-d).
- **Validation:** `test`
- **Executed verification:** `env -u NO_COLOR python -m pytest -q tests/test_home_deferred_start.py -k AT_2705` (P3; the node carries the `milestone_offer` seam marker)
- **Numeric pass threshold:** at start with the home, a board holding an unmarked milestone candidate: while the home is up, no `MilestoneOffer` (and no identity picker) is on the screen stack; after `enter` on the card, `MilestoneOffer` is the top screen and `BoardsHome` is NOT on the stack beneath it (the board view is).
- **Priority:** high
- **Acceptance (black-box):**
  - **Observable outcome:** the offer appears only once a board is chosen, over that board — the blank home behind it is gone.
  - **Shipped surface:** `TaskboardApp._offer_milestones` / `_init_team_mode` as invoked by the deferred start.
  - **Acceptance test(s):** AT-2705
  - **Boundary catalog (QC-3):** ☐ boundary (a candidate exists and the offer was never answered — the modal path) ☐ empty (no candidate — the board is marked silently, no modal: covered by the offer suite's existing arms, unchanged).
  - **Negative control:** at `base_ref` the offer opens at mount over the home — the «home not on the stack under the offer» assertion is RED at base (node-minted RED at P3; the update of the offer suite's mount-timing arms is named in the increment packet, per the commission's regression clause).

### HLR-2705 — the open-twice notice stays real
- **Traceability:** US-2701
- **Ledger:** LED-2705
- **Statement:** When a board is actually opened while another window holds it, the system shall notify once, with the existing wording, severity and time clause; when no board has been opened (the home at start), no such notice shall fire.
- **Rationale (informative):** HD-3 — the notice is kept, only its trigger moment moves (from «mount» to «actual open»). This is batch-03 item 8 A's law with the HD-1 timing.
- **Validation:** `test`
- **Executed verification:** `env -u NO_COLOR python -m pytest -q tests/test_home_deferred_start.py tests/test_boards_backlog_round.py -k "AT_2702 or open_twice or AT_2409"` (P3; the updated AT-2408/AT-2409 arms named in the packet)
- **Numeric pass threshold:** the notice's title, severity, message and once-per-open semantics are byte-identical to today's (`test_boards_backlog_round.py`'s pinned strings); the only change is when it fires.
- **Priority:** high
- **Acceptance (black-box):**
  - **Observable outcome:** same notice, same moment of truth — only when a board is actually opened.
  - **Shipped surface:** `TaskboardApp._enter_presence`.
  - **Acceptance test(s):** AT-2702 (the notice clause) and the updated AT-2408/AT-2409 arms.
  - **Boundary catalog (QC-3):** the boundary/invalid/error classes are the existing presence suite's arms (multiple foreign markers, a planted offset `since`, stale-marker removal) — unchanged and re-run at P4.
  - **Negative control:** the P1 probe AT-2701 transcript (notice at mount = RED for the future «no notice at home»).

### HLR-2706 — the directories stay fresh
- **Traceability:** US-2702
- **Ledger:** LED-2706
- **Statement:** When the task editor opens (its `@` picker and `alt+m` class Select), when the people directory opens (`@`), when the marks manager opens (`#`), or when the `/` search opens with an `@…` or `#…` query, the system shall re-read `people.json` and `marks.json` when the file's mtime or size changed since the last read, so a person or class another window added appears without a restart.
- **Rationale (informative):** the commission's second defect; closes the BACKLOG item (architect A-7, accepted) «a person another window adds shows here after a restart or this window's next write». The re-read is cheap (a stat; a parse only on change). The board's live dicts are the same objects the directory swaps in place, so every view sees the fresh directory at once.
- **Validation:** `test`
- **Executed verification:** `env -u NO_COLOR python -m pytest -q tests/test_directory_refresh.py -k AT_2706` (P3; P1 RED probe executed, `evidence/red-p1.txt` probe AT-2706)
- **Numeric pass threshold:** a person appended to `people.json` by a second `Directory` instance appears in the people view the next time it opens (the frame names the person); the same holds for a class appended to `marks.json` in the `#` manager's frame and in the editor's `alt+m` Select options; the `/` search offers the fresh person for an `@` query (the completion names the person); a file whose mtime and size are unchanged is not re-parsed (a read spy sees zero re-reads).
- **Priority:** high
- **Acceptance (black-box):**
  - **Observable outcome:** the other window's person/class is there, no restart needed.
  - **Shipped surface:** `TaskboardApp.action_add_task` / `action_edit` (`TaskModal`), `action_people_directory` (`PeopleDirectory`), `action_marks_manager` (`MarksManager`), `action_search` (`SearchPrompt`).
  - **Acceptance test(s):** AT-2706
  - **Boundary catalog (QC-3):** ☐ empty (no people/classes — the frames say so, unchanged) ☐ boundary (a change that keeps size constant — an edit in place; mtime moves, so the re-read still fires) ☐ invalid (a malformed entry in the re-read file is skipped like the mount's load — the same `_read`) ☐ error — see HLR-2707.
  - **Negative control:** executed at P1 against `base_ref`: the people view says «No one in the directory yet» after the other window's add (`evidence/red-p1.txt`, probe AT-2706).

### HLR-2707 — an unreadable re-read keeps the directory
- **Traceability:** US-2702
- **Ledger:** LED-2707
- **Statement:** When a directory re-read fails (the file cannot be parsed), the system shall keep the in-memory directory unchanged and notify once, with a `markup=False` warning; the directory shall never be emptied by a failed re-read.
- **Rationale (informative):** HD-5's failure posture, mirroring the mount's load notice (the `_warn_registry` shape): a transient bad write by another window must not wipe this window's directory.
- **Validation:** `test`
- **Executed verification:** `env -u NO_COLOR python -m pytest -q tests/test_directory_refresh.py -k AT_2707` (P3; P1 RED probe executed, `evidence/red-p1.txt` probe AT-2707)
- **Numeric pass threshold:** with people.json replaced by unparseable bytes after a successful mount: exactly one notification titled `People`, `markup=False`, severity `warning`; the people view still lists every person the mount loaded; opening the view again without fixing the file does not add a second notice for the same failure (one notice per failed re-read, not per open).
- **Priority:** high
- **Acceptance (black-box):**
  - **Observable outcome:** the directory survives the other window's bad write, and the user is told once.
  - **Shipped surface:** the directory re-read helper and its four call seats.
  - **Acceptance test(s):** AT-2707
  - **Boundary catalog (QC-3):** ☐ error (unparseable file) ☐ boundary (a file that parses to an empty directory — a LEGITIMATE empty, the directory becomes empty with no failure notice; distinguishable from the error case by the notice's absence) — the other classes are the mount-load suite's arms, unchanged.
  - **Negative control:** executed at P1 against `base_ref`: no notice fires at all (`evidence/red-p1.txt`, probe AT-2707: `assert len(notes) == 1` failed with 0).

### HLR-2708 — the unchanged paths stay unchanged
- **Traceability:** US-2701
- **Ledger:** LED-2708, LED-2708r1
- **Statement:** When the app starts with a single active board, or with `--open PATH`, or when `B` is pressed after the start, the system shall behave exactly as before this batch: the start runs at mount (no home), the start-up modals open as they do today, and `B`'s home pops back to an already-started board without re-running anything.
- **Rationale (informative):** HD-4; these paths are outside the defect and must not move — the regression pin for the whole batch.
- **Validation:** `test`
- **Executed verification:** the existing suites stay green: `tests/test_boards_home.py`, `tests/test_boards.py`, `tests/test_boards_backlog_round.py`, `tests/test_milestone_offer.py`, `tests/test_milestone_offer_seam.py`, `tests/test_team_*.py`, plus the P4 full suite.
- **Numeric pass threshold:** 0 regressions in those suites at P3 and at P4. The permitted diffs — timing arms the change of timing makes unavoidable, each named in increment 001's packet: `tests/test_boards_backlog_round.py`'s AT-2408/AT-2409 presence arms (the marker and notice move off mount), its `test_TC_2409_the_lifecycle` arms (same reason), `tests/test_boards.py`'s `test_TC_2202_the_mount_order_is_the_shipped_one` (the with-home mount order loses its write half) and `test_TC_2202_switch_board_starts_the_other_board_over` (its same-board no-op assertion meets a pending start — the arm leaves the home first, as LLR-2702.3 requires), and the HD-2-timed offer arms.
- **Priority:** high
- **Acceptance (black-box):**
  - **Observable outcome:** nothing different on those paths.
  - **Shipped surface:** `TaskboardApp.on_mount` (single board / `--open`), `action_boards`.
  - **Acceptance test(s):** the named existing suites (regression pin — labelled per C-40's corollary, not a new gate).
  - **Boundary catalog (QC-3):** none new — the suites' own arms.
  - **Negative control:** the suites themselves at P3; any RED names a leaked change (the gate, not a counterfactual).

---

## 4. Low-level requirements (LLR)

> Each LLR decomposes an HLR into a verifiable property at the implementation level.
> Same regime: EARS syntax owed in `full`, recommended in `core`. ID format: `LLR-<HLR>.<M>`.

### LLR-2701.1 — the mount with a home runs the read-only half only
- **Traceability:** HLR-2701
- **Ledger:** LED-2701.1, LED-2701.1r1
- **Statement:** When `on_mount` shows the home, `TaskboardApp` shall run only the read-only start work — the board label, the first selection, the view refresh, the one shared clock interval, the registry/people/marks load notices, the rescue-load notice (`_warn_if_rescued`, which only reads `load_report`) — and shall not call the link migration, the renumbering notice, the old-done sweep, the presence announcement, the team-mode start or the milestone offer.
- **Note (verified at P2):** `_announce_renumbering` is a WRITER — it sets the settings flag and saves the board (`app.py:1583-1594`); it sits in the deferred set with the migration, and first runs with the deferred start.
- **Validation:** `test (integration)`
- **Executed verification:** `env -u NO_COLOR python -m pytest -q tests/test_home_deferred_start.py -k AT_2701` (P3)
- **Numeric pass threshold:** the AT-2701 numbers hold (0 notices of that title, 0 own markers, byte-identical default board).
- **Negative control:** the P1 probe transcript (`evidence/red-p1.txt`): at base every deferred writer ran at mount.
- **Boundary catalog:** none new — the mount's read-only set is enumerated in the statement; the single-board/`--open` mount is LLR-2708.1's, unchanged.

### LLR-2701.2 — quitting from the home writes nothing
- **Traceability:** HLR-2701
- **Ledger:** LED-2701.2
- **Statement:** When the user quits from the home (`q`), the system shall exit without running any deferred start and without writing any board file, registry change or presence marker beyond what the home's own reads did.
- **Validation:** `test (integration)`
- **Executed verification:** the AT-2701 fixture variant that presses `q` instead of leaving the home (same node file, P3)
- **Numeric pass threshold:** after `q`: the default board file's byte-count delta vs pre-start = 0, this window's markers = 0, exit code = 0.
- **Negative control:** same P1 transcript family (the start ran at base, so the future «nothing ran» assertion is RED at base).
- **Boundary catalog:** none — the home's `q` binding already exists.

### LLR-2702.1 — one started-board record, written by the start itself
- **Traceability:** HLR-2702
- **Ledger:** LED-2702.1, LED-2702.1r1, LED-2702.1r2, LED-2702.1r4, LED-2702.1r5
- **Statement:** `TaskboardApp` shall record which board id the start has run for, the start shall run only when the record does not name the current board, and completing the start shall write the record — so every path onto a board (the home's `enter` and `esc`, `switch_board`, the agenda-of-every-board and people-view jump onto it, the mount without a home) runs the start exactly once per board. The record is written ONLY on a completed start (the migration gates the rest, so a failed start has no partial writers to double-run); `switch_board`'s restore path writes the record back to the previously started board's id when a switch fails after the record moved.
- **Validation:** `test (unit)` + `test (integration)`
- **Executed verification:** `env -u NO_COLOR python -m pytest -q tests/test_home_deferred_start.py -k "AT_2702 or AT_2703 or TC_2703"` (P3; TC-2703 carries the record's unit-level arms)
- **Numeric pass threshold:** AT-2702/AT-2703's once-numbers hold across all three paths.
- **Negative control:** a unit arm flips the record to the current board and asserts the start body does not re-run (its writers are the start itself and `switch_board`'s restore — the C-15.1 writer census is done at P3).
- **Boundary catalog:** none new.

### LLR-2702.2 — the home's two paths onto the default board
- **Traceability:** HLR-2702
- **Ledger:** LED-2702.2
- **Statement:** `BoardsHome.action_open` on the already-open board and `BoardsHome.action_back` shall leave the home and then run the deferred start when it is pending for the current board; when the start already ran (a later `B` home), both shall behave as today — pop, nothing re-run.
- **Validation:** `test (integration)`
- **Executed verification:** AT-2702 (`enter`) and AT-2703 (`esc`, then `B`/`esc`) (P3)
- **Numeric pass threshold:** AT-2702/AT-2703 numbers.
- **Negative control:** P1 transcript; the mutation battery at P3 reddens each arm.
- **Boundary catalog:** none new.

### LLR-2702.3 — `switch_board`'s same-board early return still starts a pending board
- **Traceability:** HLR-2702
- **Ledger:** LED-2702.3
- **Statement:** When `switch_board` is asked for the board already open and that board's start is pending, the system shall run the deferred start instead of returning silently; when the start already ran, it shall return as today.
- **Validation:** `test (integration)`
- **Executed verification:** AT-2702 drives this path (`enter` on the default card reaches the app through the same-board branch) (P3)
- **Numeric pass threshold:** the start's effects appear exactly once (LLR-2702.1's record).
- **Negative control:** at base the early return skips the start entirely (the P1 probe's mount already started it — the node asserts the pending case via a fresh app).
- **Boundary catalog:** none new.

### LLR-2702.4 — a failed deferred start keeps the board pending
- **Traceability:** HLR-2702
- **Ledger:** LED-2702.4
- **Statement:** When the deferred start's migration fails, the system shall leave the started-record unwritten for that board, leave the user on the board view with the home popped, and let the migration's own notice explain; a later path onto the board shall retry the start from the migration.
- **Validation:** `test (integration)`
- **Executed verification:** `env -u NO_COLOR python -m pytest -q tests/test_home_deferred_start.py -k TC_2703` (P3)
- **Numeric pass threshold:** after a forced migration failure on the deferred start: 1 failure notice, the started-record still names no board for it, the screen beneath is the board view, and pressing `B` then `esc` retries the start exactly once (the migration spy runs again).
- **Negative control:** at base the same-board early return never starts, so the node is RED at base by inspection of `app.py:1458` (node-minted RED at P3).
- **Boundary catalog:** ☐ error (the migration refusal) — the other classes are the migration suite's existing arms, unchanged.

### LLR-2703.1 — picking another board never writes the default
- **Traceability:** HLR-2703
- **Ledger:** LED-2703.1, LED-2703.1r1
- **Statement:** When the user picks another board from the home, `switch_board` shall run that board's start as today, and no path shall write the default board's file — the home's card reads (`peek_board`) never save, and the deferred default start never ran.
- **Validation:** `test (integration)`
- **Executed verification:** AT-2704 (P3)
- **Numeric pass threshold:** AT-2704's byte-equality and un-archived task hold.
- **Negative control:** at base the default board was started at mount — byte-equality is RED at base (P3 node-minted RED).
- **Boundary catalog:** none new.

### LLR-2704.1 — the start-up modals open after the home pops
- **Traceability:** HLR-2704
- **Ledger:** LED-2704.1
- **Statement:** The team identity picker and the milestone offer shall be pushed while the board view is the screen beneath them — the home shall not be on the stack under a start-up modal.
- **Validation:** `test (integration)`
- **Executed verification:** AT-2705 (P3, `milestone_offer` seam marker)
- **Numeric pass threshold:** AT-2705's stack assertions hold at start-with-home; the single-board/`--open` paths keep today's stack shape (the offer suite's existing arms, re-run).
- **Negative control:** at base the offer pushes over the home (node-minted RED at P3).
- **Boundary catalog:** ☐ empty (no candidate — the silent-mark arm, unchanged).

### LLR-2705.1 — the notice is byte-identical, the trigger moment moves
- **Traceability:** HLR-2705
- **Ledger:** LED-2705.1
- **Statement:** `_enter_presence` shall keep its exact wording, severity, timeout and once-per-open semantics, and the system shall call it only as part of an actual board start.
- **Validation:** `test (integration)`
- **Executed verification:** the updated `tests/test_boards_backlog_round.py` arms (named in increment 001's packet) + AT-2702's notice clause (P3)
- **Numeric pass threshold:** the presence suite's pinned-string arms: 0 assertion diffs (byte-identical notices), 1 notice per actual open.
- **Negative control:** the P1 probe (notice at mount is RED for the future).
- **Boundary catalog:** none new — the suite's planted-marker arms stand.

### LLR-2706.1 — the people directory re-reads on change, cheaply
- **Traceability:** HLR-2706
- **Ledger:** LED-2706.1
- **Statement:** `people.Directory` shall expose a re-read that stats the file's mtime and size against the last read, re-parses only when either changed, and swaps the parsed entries into the live `people` dict in place; when nothing changed it shall not touch the dict or re-parse.
- **Validation:** `test (unit)`
- **Executed verification:** `env -u NO_COLOR python -m pytest -q tests/test_directory_refresh.py -k TC_2701` (P3)
- **Numeric pass threshold:** TC-2701: an unchanged file → the same dict object, zero parse calls (a monkeypatched `_read` counter); an mtime change with the same size → exactly one re-parse and the new entry present; a size change with a frozen mtime → re-parsed (the size arm).
- **Negative control:** the P1 probe AT-2706 (no re-read seam exists at base — the P3 mutation battery reddens the gate).
- **Boundary catalog:** ☐ boundary (size-only change) — the empty/invalid classes are the mount-load suite's arms, re-run.

### LLR-2706.2 — the marks directory re-reads the same way
- **Traceability:** HLR-2706
- **Ledger:** LED-2706.2
- **Statement:** `marks.Directory` shall expose the same mtime/size-gated re-read, swapping parsed classes into the live `marks` dict in place.
- **Validation:** `test (unit)`
- **Executed verification:** TC-2701's marks parameter arm (P3)
- **Numeric pass threshold:** as LLR-2706.1, over `marks.json`.
- **Negative control:** as LLR-2706.1.
- **Boundary catalog:** as LLR-2706.1.

### LLR-2706.3 — the four seats re-read before they show
- **Traceability:** HLR-2706
- **Ledger:** LED-2706.3, LED-2706.3r1
- **Statement:** The task editor's open (add and edit), the people directory's open and the marks manager's open shall run the directories' re-reads before the surface builds; the `/` search shall run them when its query names the directories (`@…`/`#…`) — so every surface shows the file as it is now.
- **Validation:** `test (integration)`
- **Executed verification:** AT-2706 (people view + manager + the editor's Select options + the `/` `@` completion) (P3)
- **Numeric pass threshold:** AT-2706's frame assertions hold for each named surface.
- **Negative control:** the P1 probe AT-2706 transcript (the person was invisible at base).
- **Boundary catalog:** ☐ invalid (a malformed new entry is skipped — the `_read` leniency, unchanged).

### LLR-2707.1 — a failed re-read keeps the directory and says so once
- **Traceability:** HLR-2707
- **Ledger:** LED-2707.1
- **Statement:** When the re-read's parse fails, the directory shall keep its current in-memory entries, record the failure once, and the app shall surface one `markup=False` warning per failed re-read — never empty the directory, never re-notify on every open while the file stays bad.
- **Validation:** `test (integration)`
- **Executed verification:** AT-2707 (P3; P1 probe executed)
- **Numeric pass threshold:** AT-2707's once-and-kept numbers.
- **Negative control:** the P1 probe (0 notices at base).
- **Boundary catalog:** ☐ error (unparseable) ☐ boundary (a legitimate empty file re-read → empty directory, NO notice).

### LLR-2708.1 — the no-home mounts run the full start at mount, unchanged
- **Traceability:** HLR-2708
- **Ledger:** LED-2708.1
- **Statement:** With a single active board or with `--open PATH`, `on_mount` shall run the full start exactly as before this batch, including the start-up modals' timing.
- **Validation:** `test (integration)`
- **Executed verification:** the existing single-board and `--open` suites, re-run at P3 and P4 (regression pin).
- **Numeric pass threshold:** 0 diffs in those suites.
- **Negative control:** the suites themselves.
- **Boundary catalog:** none new.

### LLR-2708.2 — `B`'s home pops back to a started board
- **Traceability:** HLR-2708
- **Ledger:** LED-2708.2
- **Statement:** When `B` opens the home after the start, `esc` from it shall pop the home and re-run nothing — the board beneath is already started.
- **Validation:** `test (integration)`
- **Executed verification:** AT-2703's second half + the home suite (P3/P4)
- **Numeric pass threshold:** the once-numbers hold across the `B` round trip.
- **Negative control:** the suites themselves.
- **Boundary catalog:** none new.

### Information Flow Contract (IFC) — C-54

> Part A in every batch; Part B when the system's boundary has components a consumer can address independently. The block syntax, its fields and the rules that read them are in `templates/ifc-template.md`, which ships with the flow and is not copied into this batch.

- **Part A — flows:**

```
FLOW: the deferred board start, from leaving the home to the started board
  SOURCE : BoardsHome — enter on a card, or esc/back; the agenda/people
           jump onto a task's board (open_on_board)
  NODES  :
    - fn    : app.TaskboardApp deferred-start runner (the started-board record)
      owner : LLR-2702.1
    - fn    : app.TaskboardApp._migrate_links, _sweep_old_done, _enter_presence,
              _init_team_mode, _offer_milestones (unchanged bodies, re-timed)
      owner : LLR-2702.2
    - fn    : the start-up modals' stack position (over the board, home gone)
      owner : LLR-2704.1
    - fn    : boards.announce, withdraw, open_elsewhere (unchanged)
      owner : LLR-2705.1
  SINK   : the chosen board's file (migration marks, the sweep's archive); this
           window's presence marker; the open-twice notice; the identity picker
           and the milestone offer over the board
```

```
FLOW: the people directory, re-read at the four open seats
  SOURCE : people.json as another window wrote it
  NODES  :
    - fn    : people.Directory re-read (mtime/size gate, in-place swap)
      owner : LLR-2706.1
    - fn    : app.TaskboardApp.action_add_task, action_edit, action_people_directory,
              action_marks_manager, action_search (the four seats)
      owner : LLR-2706.3
    - fn    : app._label_board (the board's live dict is the same object the swap
              happens in — every view sees the fresh directory)
      owner : LLR-2706.3
  SINK   : directory.people (memory); the people view, the editor's @ picker, the
           SearchPrompt completions; the refresh-failure notice (markup=False)
```

```
FLOW: the marks directory, re-read at the same seats
  SOURCE : marks.json as another window wrote it
  NODES  :
    - fn    : marks.Directory re-read (the same gate, the same swap)
      owner : LLR-2706.2
    - fn    : the four seats (the same call sites)
      owner : LLR-2706.3
  SINK   : directory.marks (memory); the # manager, the editor's alt+m Select,
           the /#cls search; the refresh-failure notice
```

- **Part B — boundary decomposition:** `no — every flow is the app's own, addressed through its keys and its files` (the same answer as batch 2026-10-24-batch-01: one TUI process; the screens are not independently addressable components)

---

## 5. Validation strategy

### 5.1 Methods

> **Two layers** (per the Two-layer validation rule). Every batch declares BOTH:
> - **Layer A — white-box / functional (`TC-NNN`):** validates the HLR/LLR mechanism (the HOW). Methods: `test`, `inspection`, `analysis`.
> - **Layer B — black-box / behavioral acceptance (`AT-NNN`):** validates the user story's outcome through the shipped surface (the WHAT). Method: `acceptance`.

Layer A nodes: `tests/test_directory_refresh.py::test_TC_2701_refresh_gates_on_mtime_or_size[people|marks]` (the gate's three arms per directory — unchanged / mtime / size) and `test_TC_2702_a_failed_refresh_keeps_and_flags_once` (the failure record, unit level), plus `tests/test_home_deferred_start.py::test_TC_2703_a_failed_deferred_start_keeps_the_board_pending` (LLR-2702.1's record semantics and LLR-2702.4's retry posture). Layer B nodes (all NEW, minted at P3, provisional per V-5): `tests/test_home_deferred_start.py::test_AT_2701_the_home_touches_nothing`, `::test_AT_2702_enter_runs_the_deferred_start`, `::test_AT_2703_escape_runs_the_start_once`, `::test_AT_2704_another_board_never_writes_the_default`, `::test_AT_2705_the_offer_opens_over_the_board`; `tests/test_directory_refresh.py::test_AT_2706_the_directories_stay_fresh`, `::test_AT_2707_a_failed_re_read_keeps_the_directory`. The P1 RED probes of the same behaviours were executed at base_ref and live at `evidence/red-p1.txt` (their scratch file moved out of `tests/`).

### 5.2 Batch acceptance criteria
- 100% of HLRs/LLRs covered by at least one Layer B node with pass result (AT-2701..AT-2707), and the Layer A TCs green.
- Every new test mutation-checked; the RED counterfactuals and restore digests recorded per increment packet (C-40).
- The P4 full suite: the batch-01 baseline (3235 passed + 1 environmental skip) plus this batch's new nodes, in 3 sequential chunks; any other skip or fail blocks the close.
- The real Windows Terminal capture pair (118x30, 80x24) of the milestone offer over the chosen board after the home, `h01-` window titles, each closed by title and verified gone (the commission's Evidence clause).

---

## 6. Appendices (optional)

### 6.1 Extended glossary
### 6.2 Relevant design decisions
### 6.3 Open risks

- **Security scan (family C) — the two flags answered:** the scanner flagged `migration`
  (Destructive-DB family) and `expose` (Network/exposure family). Neither applies: the
  «link migration» is the shipped JSON-file link migration whose body this batch does not
  touch (it is re-timed only, LLR-2702.2/2704.1), and «expose a re-read» is an in-process
  API verb — no new route, endpoint or listener exists, and the directories' files are the
  same local `people.json`/`marks.json` the mount already reads. The batch adds no auth
  surface, no secrets, no external integration, no sensitive data beyond what the mount
  already loads, no destructive DB operation, no network exposure, and no new markup/ANSI/HTML
  rendering over file-derived text (C-17 does not fire: the re-read surfaces render through
  the unchanged pickers). `security_required: true` is discharged by this paragraph.

### 6.4 Phase-1 reconciliation log — moved to the ledger (§7)

### 6.5 Requirement amendments — moved to the ledger (§7)

---

## 7. The ledger — authored as a SEPARATE FILE

The fence below is the ledger's seed: `devflow-init.py` writes it to `01-requirements-ledger.md`. The shape of an entry is in the field guide.

```markdown
# Requirements ledger — taskboard — Batch 2026-10-24-batch-02

> Append-only. Entries are added in chronological order and never rewritten. The live
> contract is `01-requirements.md`; this file records how it came to say what it says.
> Every entry names the requirement it amends; every requirement names its entries. `V26`
> compares the two sets of pairs both ways.

_No entries yet. The first amendment to the live contract writes the first one, in the
shape the field guide's §7 shows (`req-template.part2.md` in the guide directory init prints), and nothing
above this line is ever edited._
```
