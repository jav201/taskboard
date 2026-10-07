# Requirements Document — taskboard — Batch 2026-10-07-batch-05

> **Artifact language**
> This template is the canonical **English scaffold**. Generate the artifact in the batch's development language (`state.json` `language`). For Spanish batches, translate the **prose** — section headers and guidance — **and never a label**, and use `deberá` as the normative keyword (≡ `shall`). The normative RULES in this preamble are **language-independent** and enforced regardless of artifact language.

> **Owed in.** `core` ✓ · `full` ✓

> **Field guide:** `templates/docs/req-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

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
| US-1101 | As the operator, I want a failed backup write to leave no partial file beside my board, so that a full disk never litters the board's folder with junk that pretends to be a backup. | security close S5-3 (LOW), carried from batch B2a | READY |
| US-1102 | As a maintainer, I want the `Mon D` date formatter defined once, so that a format change can't fix one view and starve another. | code review F-6 (NIT), carried from batch B2a | READY |
| US-1103 | As the operator, I want `u` after a single-task change to say what came back, so that the card that left or rejoined the columns is named, not silent. | ux UXV-3 (LOW), carried from batch B2a | READY |
| US-1104 | As the operator, I want the `?` help at 80 cells to never cut a word in half, so that narrow screens read clean. | ux UXV-6 (LOW), carried from batch B2a | READY |
| US-1105 | As the operator, I want the chain map's deepest chains to cap with a `+N more` tail instead of vanishing whole, and the selection to survive a resize heal in one pass, so that tall projects stay readable at typical heights. | code review rev-2 note + LOW carry, from batch C | READY |
| US-1106 | As a maintainer, I want the acceptance arms to walk the surface with keys, so that the tests prove the user's path, not a shortcut. | qa P4 F-3..F-5 (LOW), carried from batch B2a | READY |

#### Refinement log

**Refinement:** INVEST all ✓ for the six carries — each is a scoped, evidenced item from a
closed batch's record (the BACKLOG is the source, the code anchors were re-verified at P1).
Every story's observable outcome is stated at its HLR below. None needs a prototype round;
none is blocked by another. Classification: `READY` ×6. The `u`-toast and the `?`-clip
literals ship at the increment's discretion and are pinned there (no oracle round owed).

### 2.7 Premise evaluation (C-43) — MANDATORY, one row per premise

| # | Premise, as a truth-apt proposition | Tier | Verdict | Executed evidence (command output / `file:line` — **NOT** a citation of another document) | Disposition |
|---|---|---|---|---|---|
| P-1 | The three `Mon D` definitions are byte-identical today — `return f"{d:%b} {d.day}"` at each site — so the dedup is behavior-neutral | base behavior | TRUE | `taskboard/app.py:40-41`, `taskboard/models.py:2133-2134`, `taskboard/views.py:2680-2681` (the three bodies read equal at P1) | the owner lands at `models._md` (lowest in the import chain); the other two delegate |
| P-2 | `_create_beside` is the ONE writer of backup/log files beside the board — both writers (the link migration, the milestone offer) call it — so one fix covers both | base behavior | TRUE | `taskboard/models.py:1562` (the definition); call sites `models.py:1606,1612` (migration) and `models.py:1720,1729` (offer) | LLR-1101.1 fixes the helper itself |
| P-3 | The `?` help at 80 cells renders through `HelpModal` from `legend_entries` — the component identity; the mid-word cut's exact mechanism is the increment's investigation | base behavior | TRUE | `taskboard/modals.py:1750` (the modal), `taskboard/views.py:6882` (`legend_entries`), `modals.py:1800` (the render call) | HLR-1104 pins the outcome, LLR-1104.1 pins the mechanism it finds |

- **Premise evaluation:** 3 premise(s) · ✅ TRUE / ✅ TRUE / ✅ TRUE

### 2.8 Fork preconditions (C-52) — MANDATORY, and the declared empty when the batch does not fork

- **Fork preconditions:** none — the batch runs one lane on the main checkout. (The parallel
agent briefs at P3 take DISJOINT file sets — increment 001 owns `models.py`; increment 002 owns
`app.py` + `modals.py` + the help-render region of `views.py`; increment 003 then lands the
chain-map carries on `views.py`'s chainmap region + `app.py`'s `refresh_view` AFTER 002 is
green, so no two live briefs share a file; the trunk — requirements, backlog, this record —
is the coordinator's alone.)

---

## 3. High-level requirements (HLR)

### HLR-1101 — A failed backup write leaves no partial file
- **Traceability:** US-1101
- **Ledger:** LED-2026-10-07-batch-05.1
- **Statement:** When a backup or log write beside the board file fails mid-write (a full disk), the system shall leave NO partial file: the exclusively-created file is removed best-effort, the removal's own failure never masks the original, and the original failure propagates unchanged — for BOTH writers (the link migration and the milestone offer) through their one shared helper.
- **Rationale (informative):** security close S5-3 (LOW): a half-written `board.json.backup` pretends to be a backup; the next run already takes `.1`, so the junk only accumulates.
- **Validation:** `test`
- **Executed verification:** `python -m pytest tests/test_backup_write.py -q` (the increment's file)
- **Numeric pass threshold:** `0 failures`; both arms green (the write fails, the file is gone; the write fails AND the removal refuses — the original error still surfaces, the guard adds nothing).
- **Priority:** medium
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** after a failed backup write, the board's folder holds no new partial file and the error the user sees names the original failure.
  - **Shipped surface:** the backup/log write beside the board (both the migration's and the offer's).
  - **Acceptance test(s):** AT-1101.
  - **Boundary catalog (QC-3):** ☑ error (the failing write; the refusing removal).
  - **Negative control:** the arm where the removal itself refuses — the guard must not raise past the original error.

### HLR-1102 — One `Mon D` formatter
- **Traceability:** US-1102
- **Ledger:** LED-2026-10-07-batch-05.1
- **Statement:** The `Mon D` date formatter (`f"{d:%b} {d.day}"`) shall have exactly ONE definition in the package — owned at `taskboard/models.py` — with the views and app copies removed in favor of the shared one; the output is byte-identical for every date.
- **Rationale (informative):** code review F-6 (NIT): three copies invite a fix in one view that starves another.
- **Validation:** `test`
- **Executed verification:** `grep -c "def _md" taskboard/*.py` then 1; `python -m pytest tests/test_mon_d.py -q` (the increment's characterization pin)
- **Numeric pass threshold:** exactly one `def _md`; a date sweep (month boundaries, year ends) renders identical strings through every consumer.
- **Priority:** low
- **Acceptance (black-box):**
  - **Observable outcome:** dates render exactly as before in every view (no visible change).
  - **Shipped surface:** the date chips across lanes/gantt/kanban/details/help.
  - **Acceptance test(s):** AT-1102 (the characterization pin through the shipped surface).
  - **Boundary catalog (QC-3):** ☑ boundary (month/year boundaries in the sweep).
  - **Negative control:** a sweep arm where a consumer's formatter is shadowed back to a divergent body — the pin goes RED.

### HLR-1103 — `u` on a single-task change says what came back
- **Traceability:** US-1103
- **Ledger:** LED-2026-10-07-batch-05.1
- **Statement:** When `u` undoes a mutation that touched exactly one task (the kanban card leave/rejoin among them), the system shall toast ONE line naming the task whose change came back — `markup=False` — alongside the existing save and refresh; the whole-cascade, milestones and migration branches keep their current behavior.
- **Rationale (informative):** ux UXV-3 (LOW): after `M` in the kanban the card leaves or rejoins the columns with no message; the user scans the board for what changed.
- **Validation:** `test`
- **Executed verification:** `python -m pytest tests/test_undo_toast.py -q`
- **Numeric pass threshold:** `0 failures`; the toast read off the painted `Toast` equals the pinned literal with the task's title, exactly.
- **Priority:** low
- **Acceptance (black-box):**
  - **Observable outcome:** pressing `u` after a single-task change names the task in a one-line toast.
  - **Shipped surface:** key `u`, the notification channel.
  - **Acceptance test(s):** AT-1103.
  - **Boundary catalog (QC-3):** ☑ empty (a purged-since snapshot — the stale skip stays silent). ☑ boundary (the title is clipped by the toast width).
  - **Negative control:** an undo on an entry whose task was purged — still no toast (the skip branch is untouched).

### HLR-1104 — The `?` help never cuts a word in half
- **Traceability:** US-1104
- **Ledger:** LED-2026-10-07-batch-05.1
- **Statement:** At 80 cells (and every width), the `?` help — every legend line and every usage bullet, not only the new ones — shall break lines at word boundaries or clip at the last fitting word with `…`; no line ends mid-word.
- **Rationale (informative):** ux UXV-6 (LOW): at 80 cells the help text cuts lines mid-word; the screen stops matching what the user knows the words to be.
- **Validation:** `test`
- **Executed verification:** `python -m pytest tests/test_help_clip.py -q`
- **Numeric pass threshold:** `0 failures`; at 80×24 on the fixture board, every visible help line ends at a word boundary or with `…` (the assertion checks each wrapped line's tail).
- **Priority:** low
- **Acceptance (black-box):**
  - **Observable outcome:** the `?` help at 80 cells reads clean; clipped lines end with `…`.
  - **Shipped surface:** the `?` modal (HelpModal) and the full-map legend.
  - **Acceptance test(s):** AT-1104.
  - **Boundary catalog (QC-3):** ☑ boundary (a meaning word exactly at the width edge; an unbreakable token longer than the width).
  - **Negative control:** a fixture line whose only break is mid-word — GREEN only via the clip.

### HLR-1105 — The chain-map carries: the deep-chain cap and the one-pass resize heal
- **Traceability:** US-1105
- **Ledger:** LED-2026-10-07-batch-05.1
- **Statement:** The chain map shall (a) draw a band that does not fit whole as its fitting chains plus ONE tail row naming the rest `+N more ↓` (the kanban law), amending the whole-band-drop rule of TC-810 — a band with zero fitting chains still drops whole (no dangling head); and (b) re-verify the selection against the fresh `line_map` at the end of `refresh_view`, so the resize heal completes in ONE refresh; and (c) carry AT-801b's docstring corrected to what the arm does.
- **Rationale (informative):** code review rev-2 (deep chains fold whole at typical heights; a per-band `+N more` is the refinement) + batch C's LOW resize-heal carry.
- **Validation:** `test`
- **Executed verification:** `python -m pytest tests/test_chainmap.py tests/test_chainmap_app.py -q`
- **Numeric pass threshold:** `0 failures`; TC-810 amended (a partially-fitting band draws its chains + the `+N more ↓` tail; a zero-fit band still drops whole, head and canvas together); the resize arm asserts the selection is valid after ONE refresh; AT-801b's docstring matches its body.
- **Priority:** medium
- **Acceptance (black-box):**
  - **Observable outcome:** a tall project on the chain map at 80×24 shows its first bands with a `+N more ↓` tail instead of vanishing; resizing the window heals the selection without a second refresh.
  - **Shipped surface:** the chain map view, `refresh_view`, the help/tests.
  - **Acceptance test(s):** AT-1105 (the cap) · the amended TC-810 · the resize arm.
  - **Boundary catalog (QC-3):** ☑ boundary (exactly-fits vs one-chain-over) ☑ empty (a band whose first chain doesn't fit).
  - **Negative control:** the zero-fit band must still drop whole — a dangling head fails the arm.

### HLR-1106 — The acceptance arms walk the surface with keys
- **Traceability:** US-1106
- **Ledger:** LED-2026-10-07-batch-05.1
- **Statement:** The carried test-strength items shall ship: AT-601's and AT-602's arms walk the selection to its place with KEYS instead of assigning `selected_task_id` directly; one arm drives the offer-converted milestones into a team folder (the `M` path); AT-602's ash `◆` is asserted at the exact column, not "any".
- **Rationale (informative):** qa P4 F-3..F-5 (LOW): an arm that sets the selection directly proves the render, not the path.
- **Validation:** `test`
- **Executed verification:** `python -m pytest tests/test_milestones.py tests/test_gantt_milestones.py -q`
- **Numeric pass threshold:** `0 failures`; the rewritten arms drive only keys; the ash arm asserts the column.
- **Priority:** low
- **Acceptance (black-box):**
  - **Observable outcome:** the same user-visible outcomes as AT-601/602, reached by key presses.
  - **Shipped surface:** the same shipped surfaces (the editor, the gantt, the offer).
  - **Acceptance test(s):** AT-601/602 as amended.
  - **Boundary catalog (QC-3):** none new (the arms' fixtures stand).
  - **Negative control:** an arm reverted to assigning the selection directly — a grep pin goes RED.

---

## 4. Low-level requirements (LLR)

> Each LLR decomposes an HLR into a verifiable property at the implementation level.
> Same regime: EARS syntax owed in `full`, recommended in `core`. ID format: `LLR-<HLR>.<M>`.

### LLR-1101.1 — `_create_beside` unlinks its file on a failed write
- **Traceability:** HLR-1101
- **Ledger:** LED-2026-10-07-batch-05.1
- **Statement:** `models._create_beside` shall wrap the exclusive-create write so that ANY exception from `fh.write` (a full disk) closes the handle and removes the just-created path best-effort — the removal in a nested guard that swallows its own errors — and then re-raises the ORIGINAL exception unchanged; the two callers (the link migration, the milestone offer) inherit the law through the shared helper, untouched themselves.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest tests/test_backup_write.py -q`
- **Numeric pass threshold:** arm 1 (write fails, removal works): the file does not exist after the call, the original `OSError` propagates; arm 2 (write fails, `Path.unlink` refuses): the original `OSError` still propagates — no new exception escapes the guard.
- **Negative control:** arm 2 is the negative control; a build WITHOUT the unlink keeps the partial file on disk (RED on base).
- **Boundary catalog:** ☑ error (the failing write; the refusing removal).

### LLR-1102.1 — one `_md`, owned at models
- **Traceability:** HLR-1102
- **Ledger:** LED-2026-10-07-batch-05.1
- **Statement:** the package shall define `def _md` exactly once — at `taskboard/models.py` — with `taskboard/views.py` and `taskboard/app.py` importing it (their local definitions deleted); the function body is unchanged (`f"{d:%b} {d.day}"`).
- **Validation:** `test (unit)`
- **Executed verification:** `grep -c "def _md" taskboard/*.py` then 1 · `python -m pytest tests/test_mon_d.py -q`
- **Numeric pass threshold:** `0 failures`; exactly 1 definition of `def _md` in the package; a 14-date sweep (month boundaries, year ends) renders identical strings through `views._md` and `app._md` (now the same object).
- **Negative control:** a consumer shadowing a divergent body — the sweep pin goes RED.
- **Boundary catalog:** ☑ boundary (the sweep's month/year edges).

### LLR-1103.1 — the single-task undo toast
- **Traceability:** HLR-1103
- **Ledger:** LED-2026-10-07-batch-05.1
- **Statement:** the single-task branch of `app.action_undo` (the fall-through after the cascade/milestones/migration branches) shall `notify` ONE line naming the task — the literal pinned at the increment, `markup=False` — before its save and refresh; the other branches and the stale-skip stay exactly as shipped.
- **Validation:** `test (integration)`
- **Executed verification:** `python -m pytest tests/test_undo_toast.py -q`
- **Numeric pass threshold:** `0 failures`; the toast read off the painted `Toast` equals the pinned 1-line literal with the task's title, exactly; the purged-skip arm stays silent (0 toasts).
- **Negative control:** the purged-skip arm (no toast) — RED if the notify moves above the skip.
- **Boundary catalog:** ☑ empty (the purged skip) ☑ boundary (a long title, clipped by the toast width).

### LLR-1104.1 — word-boundary clipping in the help lines
- **Traceability:** HLR-1104
- **Ledger:** LED-2026-10-07-batch-05.1
- **Statement:** the `?` help's line composition (the legend meanings in `legend_entries`' render path and the usage bullets in `help_usage`, through `HelpModal`) shall clip each line at the modal's usable width at a WORD boundary, appending `…` when a word is cut; an unbreakable token longer than the width clips with `…` at the edge; no line ends mid-word.
- **Validation:** `test (integration)`
- **Executed verification:** `python -m pytest tests/test_help_clip.py -q`
- **Numeric pass threshold:** at 80×24 on the fixture board every visible help line ends at a word boundary or with `…`; the exact-edge and unbreakable-token arms hold.
- **Negative control:** a fixture line whose only possible break is mid-word — GREEN only via the clip (on base it cuts the word).
- **Boundary catalog:** ☑ boundary (exact-edge word; overlong token).

### LLR-1105.1 — the deep-chain cap amends the fold
- **Traceability:** HLR-1105
- **Ledger:** LED-2026-10-07-batch-05.1
- **Statement:** the chain map's fold shall draw a partially-fitting band's fitting chains and ONE tail row `+N more ↓` (N exact, the kanban law), amending TC-810's whole-band-drop (LED .1); a band whose FIRST chain does not fit still drops whole — the dangling-head law stands; the resize-heal re-verifies `selected_task_id` against the fresh `line_map` at the end of `refresh_view` (one refresh, not two); AT-801b's docstring is corrected to its body.
- **Validation:** `test (integration)`
- **Executed verification:** `python -m pytest tests/test_chainmap.py tests/test_chainmap_app.py -q`
- **Numeric pass threshold:** the amended TC-810 (cap row present, N exact; zero-fit band drops whole); the resize arm (selection valid after ONE refresh); the docstring arm.
- **Negative control:** the zero-fit band with a dangling head — RED.
- **Boundary catalog:** ☑ boundary (exactly-fits vs one-chain-over) ☑ empty (zero-fit band).

### LLR-1106.1 — the key-walking arms
- **Traceability:** HLR-1106
- **Ledger:** LED-2026-10-07-batch-05.1
- **Statement:** the AT-601/AT-602 arms shall reach their selection by key presses alone (no `selected_task_id` assignment in the amended arms); one arm converts offer milestones into a TEAM folder (the `M` path end to end); AT-602's ruler arm asserts the ash `◆` at the exact column.
- **Validation:** `test (integration)`
- **Executed verification:** `python -m pytest tests/test_milestones.py tests/test_gantt_milestones.py -q`
- **Numeric pass threshold:** `0 failures`; a grep pin over the amended arms shows no direct `selected_task_id` assignment.
- **Negative control:** the grep pin — an arm reverted to the assignment goes RED.
- **Boundary catalog:** none new.

### Information Flow Contract (IFC) — C-54

> Part A in every batch; Part B when the system's boundary has components a consumer can address independently. The block syntax, its fields and the rules that read them are in `templates/ifc-template.md`, which ships with the flow and is not copied into this batch.

- **Part A — flows:**

```
FLOW: the carries, from the board/key to the surface
  SOURCE : the board file (backup/log writes, tasks, dates); the keys (u, ?, the arrows); the terminal size
  NODES  :
    - fn    : models._create_beside (the backup/log write law)
      owner : LLR-1101.1
    - fn    : models._md (the one formatter)
      owner : LLR-1102.1
    - fn    : app.action_undo (the single-task toast)
      owner : LLR-1103.1
    - fn    : app.refresh_view (the resize heal)
      owner : LLR-1105.1
    - fn    : the ? help line composition (legend_entries' render path + help_usage through HelpModal)
      owner : LLR-1104.1
    - fn    : the chain map fold (the +N more cap)
      owner : LLR-1105.1
  SINK   : the board's folder (no partial files), the toast channel, the ? modal at 80x24, the chain map canvas
```

- **Part B — boundary decomposition:** `no — no new addressable component.` (the carries amend shipped components; nothing new is addressable on its own.)

---

## 5. Validation strategy

### 5.1 Methods

> **Two layers** (per the Two-layer validation rule). Every batch declares BOTH:
> - **Layer A — white-box / functional (`TC-NNN`):** validates the HLR/LLR mechanism (the HOW). Methods: `test`, `inspection`, `analysis`.
> - **Layer B — black-box / behavioral acceptance (`AT-NNN`):** validates the user story's outcome through the shipped surface (the WHAT). Method: `acceptance`.

### 5.2 Batch acceptance criteria
- every HLR has a passing AT; every LLR a passing TC; every new assertion RED on the base tree or by a recorded mutation.
- full suite: 0 failures.
- the BACKLOG's carries this batch claims are marked done; nothing new opens without a reason.

---

## 6. Appendices (optional)

### 6.1 Extended glossary
### 6.2 Relevant design decisions
### 6.3 Open risks
### 6.4 Phase-1 reconciliation log — moved to the ledger (§7)

### 6.5 Requirement amendments — moved to the ledger (§7)

---

## 7. The ledger — authored as a SEPARATE FILE

The fence below is the ledger's seed: `devflow-init.py` writes it to `01-requirements-ledger.md`. The shape of an entry is in the field guide.

```markdown
# Requirements ledger — taskboard — Batch 2026-10-07-batch-05

> Append-only. Entries are added in chronological order and never rewritten. The live
> contract is `01-requirements.md`; this file records how it came to say what it says.
> Every entry names the requirement it amends; every requirement names its entries. `V26`
> compares the two sets of pairs both ways.

_No entries yet. The first amendment to the live contract writes the first one, in the
shape the field guide's §7 shows (`req-template.md` in the guide directory init prints), and nothing
above this line is ever edited._
```
