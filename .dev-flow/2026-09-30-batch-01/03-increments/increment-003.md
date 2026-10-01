# Increment 003 — HLR-005 · `Task text never parsed as Textual markup in TaskDetails / ImageViewer (security S1)`

| Field | Value |
|---|---|
| Batch | `2026-09-30-batch-01` |
| Increment | `003` |
| Lane (if the batch forked) | n/a — one lane |
| Requirement(s) | HLR-005, LLR-005.1 |
| Acceptance | AT-007 · white-box: preservation `test_details_still_highlight_the_notes` |
| Agent | `software-dev` |
| Date | `2026-09-30` |

## 1 · What changed

Owner verdict 2026-09-30: fix the backlog item S1 in `TaskDetails` the way the editor preview
was fixed. New helper `_rich(markup) -> Text` in `taskboard/modals.py` (Rich parses the
app-built markup holding `escape()`d task text, so Textual never parses task text). Every label
in `TaskDetails` carrying task text (title, project, phase, priority, start, due, URLs) goes
through it; the notes render with `notes_preview` (same per-line highlight); `image_block`'s
five labels and — review F1 — the `ImageViewer` title do too. Before: a note/title/URL/image
reference holding `[LINK=http://e]x` raised MarkupError (app died, reachable from team-synced
data) and `[B]x` / `[ red]x` vanished.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/modals.py` | source | HLR-005, LLR-005.1 | `_rich`; `TaskDetails.compose`, `image_block`, `ImageViewer.compose` title wrapped |
| `tests/test_details_markup.py` | test | AT-007, HLR-005, LLR-005.1 | NEW — 29 nodes |
| `tests/test_app.py` | test | HLR-005 | `test_image_block_link_and_missing_fallbacks` reads `.content` (a `Text` label renders only inside an app) |

| Count | Value |
|---|---|
| **SOURCE files** | **1 / 4** |
| Test files | 2 (uncapped) |
| Doc files | batch record only |

## 3 · How to test

`set PYTHONUTF8=1 && python -m pytest -q tests/test_details_markup.py tests/test_app.py -k "details or image_block or Details"`.
Manual: give a task the title `[B]x` and a note `[LINK=http://e]x`, press `enter` and `i`.

## 4 · Test results

| Layer | Owed in | Nodes | Result |
|---|---|---|---|
| **0 · unit** | `core` · `full` | `_rich` is a one-line wrapper — none — no unit met the decision or boundary criterion | n/a |
| **A · white-box** | `core` · `full` | `test_details_still_highlight_the_notes`, `test_image_block_link_and_missing_fallbacks` | 2 passed |
| **B · black-box** | `core` · `full` | AT-007 `test_details_show_bracketed_task_text_literally[7 fields × 4 strings]` | 28 passed |

`tests/test_details_markup.py` + the details/image_block nodes of `tests/test_app.py`: 33 passed
(`inc003-green.txt`). Full suite: see 04-validation.md.

### RED counterfactual

RED on base (the HEAD `modals.py`/`taskboard.tcss` in a scratch copy, `/tmp/rb`, the product tree
untouched): `inc003-red-on-base.txt` — 21 failed, 8 passed. The 8: the 7 `a[b` arms (an unclosed
bracket was already literal — a boundary arm, GREEN by design) and the highlight preservation test.

| Field | Value |
|---|---|
| **RED counterfactual** | 21 of 29 nodes RED on base (`inc003-red-on-base.txt`); the 8 GREEN-on-base arms are boundary/preservation, the preservation one RED under N6; restore proven per mutation, sha256 `c5e60e8b445e0675…` |
| **Mutation verdicts** | 8 mutations (`inc003-mutations.txt`, script `mutate_inc003.py`): N1 notes as str · N2 title as str · N3 project as str · N4 url as str · N5 image fallback as str · N6 notes flattened (highlight lost) · N7 viewer title as str · N8 phase as str — all KILLED, restore ok=True |

### Instrument RED-proof

| Instrument | Known-bad input fed to it | The FAILURE it reported |
|---|---|---|
| whole-screen painted search | first version | project/title arms passed on base because the BOARD behind the modal draws them — narrowed to the modal's region |
| details-grid painted search | phase/project arms | the grid paints blank (pre-existing, also on base) — those two arms read each label's `render()` (Textual's parse) instead |

| Field | Value |
|---|---|
| **Instrument RED-proof** | 2 instruments shown wrong first and corrected (table above) |
| **Emitted-form assertion** | 1 artifact: the painted modal region / Textual's own render of each label |

### Evidence files

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| inc003-red-on-base.txt | `.dev-flow/2026-09-30-batch-01/evidence/inc003-red-on-base.txt` | `6e83205cdbc8ebe8654b090e1c7d911464ad8c2c2a1372f7c60f70e3b781a9b8` |
| inc003-mutations.txt | `.dev-flow/2026-09-30-batch-01/evidence/inc003-mutations.txt` | `a9204f6b5a73b23025785ed1a1eb9be7787892c33adf233dbde096b7659457bc` |
| inc003-green.txt | `.dev-flow/2026-09-30-batch-01/evidence/inc003-green.txt` | `767a1144877085fd8e8cf66b2c802f9439f8d037ab4c82a14ca837d02c756705` |
| full-suite-after.txt | `.dev-flow/2026-09-30-batch-01/evidence/full-suite-after.txt` | `a64ea72a3221a02a0467518571349064ab54f545db08e5c11c9276924fe5fc15` |

| Field | Value |
|---|---|
| **Evidence files** | 4 artifacts, each cited above with its SHA-256 |

### Load-bearing emptiness

"No task text reaches Textual as a str in TaskDetails/ImageViewer/image_block" is an absence:
guarded by the 7-field AT matrix and by N1–N5, N7, N8 (each re-introduces one str path → RED).

### Reverse census

| Probe | Command | Result |
|---|---|---|
| B1 | `grep -rln "TaskDetails\|image_block\|ImageViewer" tests/` | `test_app.py` (1 RED → `.content`), `test_details_markup.py` |
| B2 | none moved | did not fire |
| B3 | no golden | did not fire |
| B4 | team sync feeds task text | covered: the AT strings are what a synced task can carry |
| A3 | `grep -n "image_block(\|TaskDetails(" taskboard/` | `app.py` constructors unchanged |

| Field | Value |
|---|---|
| **Reverse census** | 5 probes: B1 fired (1 test changed, reason in §2); B2/B3 did not fire; B4 covered; A3 unchanged |
| **Correction population** | 1 correction ("escaped task text is safe for a widget"), enumerated with `grep -n "escape(" taskboard/modals.py`: TaskDetails 8 sites, image_block 5, ImageViewer 1 — all 14 edited; ~13 other sites in other modals left (Select/Option labels, confirm/prompt titles, notify, standup) → BACKLOG, out of the owner's S1 scope |

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a generic agent with agents/code-reviewer.md · PASS-WITH-NOTES, 0 HIGH / 1 MEDIUM / 1 LOW · F1 (ImageViewer title still a str) folded + AT arm + N7; F2 (phase arm missing) folded + N8; the ~13 other-modal sites → BACKLOG |

## 5 · Risks

- The TaskDetails info grid (project/phase/priority/dates) paints blank — PRE-EXISTING on the base tree, not caused here; → BACKLOG.
- Other modals still hand escaped user text to Textual as str (≈13 sites) → BACKLOG.

## 6 · Pending items / spec deviations

- S2 (control bytes) unchanged → BACKLOG.

## 7 · Suggested next task

A sweep of the remaining `escape()`-into-Textual sites (security follow-up).

## Increment gate checklist

| # | Item | Owed in | ✓/⚠/✗ | Evidence |
|---|---|---|---|---|
| 1 | ≤4 source files | all | ✓ | §2 |
| 2 | Tests written in this same increment | all | ✓ | `tests/test_details_markup.py` |
| 3 | Layer 0 written where the criterion applies | `core` · `full` ‹one complete run owned by the orchestrator ~ Layer 0› | ✓ | §4 |
| 4 | **RED counterfactual** declared | `core` · `full` ‹RED counterfactual mandatory ~ RED counterfactual› | ✓ | §RED |
| 5 | **Reverse census** declared | `core` · `full` ‹reverse census of the touched symbol ~ Reverse census› | ✓ | §Reverse census |
| 6 | `code-reviewer` passed | `core` · `full` ‹RED counterfactual mandatory ~ code-reviewer› | ✓ | §4b |
| 7 | No file from another lane touched | all | ✓ | one lane |
| 8 | Frozen interfaces untouched | all | ✓ | no signature changed |
| 9 | Coverage claims verified on disk | all | ✓ | nodes collected and run |
| 10 | Load-bearing emptiness declared | all | ✓ | §Load-bearing emptiness |
| 11 | **Mutation verdicts** declared | all | ✓ | §RED |
| 12 | **Instrument RED-proof** declared | all | ✓ | §Instrument |
| 13 | **Correction population** declared | all | ✓ | §Correction |
| 14 | **Emitted-form assertion** declared | all | ✓ | §Emitted |
| 15 | **Independent review** names somebody | all | ✓ | §4b |
| 16 | **Evidence files** declared | all | ✓ | §Evidence |
