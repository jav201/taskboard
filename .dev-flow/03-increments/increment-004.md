# Increment 004 — R-00 · Reconcile pre-batch session work (aperture `6`, prism ember hero, colored gallery)

| Field | Value |
|---|---|
| Batch | `2026-08-14-batch-04` |
| Increment | `004` (Increment 0 of the batch — reconciliation) |
| Lane | — (batch not forked) |
| Requirement(s) | R-00 (requirements §3.0; validation plan R-00: test + inspection) |
| Acceptance | `pytest` 775 passed + exactly the 3 documented keymap reds · `verify_aperture.py` ALL PASSED · prism hero carved · kanban-ideas 16 figures |
| Agent | `software-dev` (supervised-incremental-development) |
| Date | 2026-08-15 |

---

## 1 · What changed

**BLUF: nothing was written in this increment — by design.** Increment 0 is a reconciliation gate: the pre-batch session work (aperture key `6` wiring, prism ember-hero carve, NO_COLOR capture fix + colored re-capture, kanban-ideas prototype record) was already in the working tree, uncommitted. This increment independently verified it, classified every dirty file, made the landing decision, and recorded the evidence. The shipped surface the user reaches: pressing `6` in the app opens the ApertureScreen with 4-view jumps, and the prism language's overdue hero shows the day-count digit carved out of the ember braille tablet instead of a solid red wall.

Verification results: the full suite shows exactly the 3 documented keymap reds and no others; `verify_aperture.py` reports ALL PASSED; both inspection items confirmed on disk.

---

## 2 · Files modified

**SOURCE files modified by this increment: 0 / 4.** This is a reconciliation increment — no source, test, or doc files were written or edited by it; the only file created is this packet (`.dev-flow/**`, outside the count).

The pre-batch work under verification spans (for the record, not this increment's budget):

| File | Kind | Change (pre-batch, verified here) |
|---|---|---|
| `taskboard/keymap.py` | source | Key `6` seat |
| `taskboard/app.py` | source | binding_map, HelpScreen, BOARD_ACTIONS + check_action, action_aperture, action_legend branch |
| `taskboard/aperture.py` | source | 4-view jumps, LAST_RESORT |
| `taskboard/hero.py` | source | centered tablet carve, sx=3·sy, falls through to `_beside_plot` |
| `prototypes/capture_languages.py` | tool | pops `NO_COLOR` before Textual import |
| `prototypes/verify_aperture.py` | tool | updated to main's reality |
| `README.md` | doc | key `6` row |
| `prototypes/gallery/*` (22 modified + 4 new prism captures) | artifact | colored re-capture |
| `prototypes/gallery.html` | artifact | rebuilt gallery index |
| `prototypes/kanban_ideas/` | artifact | approved-prototype design record |
| `.dev-flow/*` | process | batch artifacts |

| Count | Value |
|---|---|
| **SOURCE files** | **0 / 4** |
| Test files | 0 |
| Doc files | 1 (this packet, outside the count) |

---

## 3 · How to test

```bash
python -m pytest tests -q
PYTHONIOENCODING=utf-8 python prototypes/verify_aperture.py   # UTF-8 forced: the script prints ⏎ (U+23CE), which crashes on a cp1252 console
# inspection: open prototypes/gallery/board_prism.svg — ember hero digit is carved, not solid
# inspection: grep -c "<figure" prototypes/kanban_ideas/out/kanban-ideas.html  → 16
```

---

## 4 · Test results

### Automated limb

`python -m pytest tests -q` — one complete run, tail read from that run:

```
FAILED tests/test_keymap.py::test_every_shown_key_has_a_real_action_on_the_app
FAILED tests/test_keymap.py::test_the_widest_bars_keep_their_words - assert F...
FAILED tests/test_keymap.py::test_the_readme_keybinding_table_matches_the_seat
3 failed, 775 passed in 51.63s
```

Exactly the 3 known keymap reds documented in PLAN.md's test ledger (`test_every_shown_key_has_a_real_action_on_the_app`, `test_the_readme_keybinding_table_matches_the_seat`, `test_the_widest_bars_keep_their_words`). No other failure — 778 total reconciles with PLAN.md R-00's "pytest 778 green" target once Inc 1 closes the 3 reds.

`PYTHONIOENCODING=utf-8 python prototypes/verify_aperture.py` — final lines of the same run:

```
  [PASS] the hero under test is the DEADLINE's reading, and its detail is the user's TITLE — the reason `hero.py` escapes at all  deadline: '[URGENT] rotate keys'
  [PASS] the hero leg is not vacuous: some languages really do compose the detail line into the panel at 118x34 (the rest are a regression guard, and this check is what would notice the last one going away)  3/10: ['swiss', 'industrial', 'darkside']

ALL PASSED
```

(Environment note: without `PYTHONIOENCODING=utf-8` the script dies mid-run with `UnicodeEncodeError: 'charmap' codec can't encode character '\u23ce'` on this cp1252 console — a console-encoding quirk of the Windows host, not a check failure. Worth a backlog line if the verifiers are meant to run unwrapped on Windows.)

### Inspection limb (R-00's non-automatable part)

1. `prototypes/gallery/board_prism.svg` — the ember hero (the `#f43f5e` braille tablet, SVG lines 7–20) renders the overdue day-count digit as carved holes inside the braille wall (open `⠿`/`⠉`/`⣶` gaps forming the digit, centered, with the "DAYS OVERDUE" caption and task title beside it), not a solid red wall. ✓
2. `prototypes/kanban_ideas/out/kanban-ideas.html` — `grep -c "<figure"` returns **16**; the page renders 16 figures. ✓
3. Landing decision — everything in categories (a)–(d) below lands in the batch PR; nothing under `~/kimi/taskboard-overhaul` is in this repo and stays out (C-44 backlog carry, untouched). ✓

### Dirty-tree classification (`git status --porcelain`, every entry)

| Class | Entries |
|---|---|
| (a) aperture wiring | `taskboard/keymap.py`, `taskboard/app.py`, `taskboard/aperture.py`, `prototypes/verify_aperture.py`, `README.md` |
| (b) hero / gallery | `taskboard/hero.py`, `prototypes/capture_languages.py`, `prototypes/gallery/` (22 modified captures + new `board_prism.svg/.txt`, `gallery_prism.svg/.txt`), `prototypes/gallery.html` (new), `prototypes/out/_fixture_late.json` (regenerated) |
| (c) prototype record | `prototypes/kanban_ideas/` (untracked, incl. `proto.py` + `out/`) |
| (d) batch .dev-flow artifacts | `01-requirements.md`, `01b-qa-validation-plan.md`, `02-review.md`, `02-review-architect.md`, `02-review-qa.md`, `02-review-ux.md` (new), `state.json`, `2026-08-14-batch-04/` (new) |
| (e) unexpected | **none** — see below |

**Investigated, not swept:** `M prototypes/out/_fixture_late.json` did not obviously belong to any declared category. Diff inspected: it is the synthetic capture fixture regenerated by the re-capture sweep — dates rolled forward, fresh ids, and a new `phase_changed` field on tasks. It is written by `prototypes/capture.py` / `capture_languages.py` (both declare `FIXTURE = .../out/_fixture_late.json`) and is deliberately synthetic per the in-file doctrine comments. Reclassified as (b), a re-capture byproduct. No other entry required investigation.

### RED counterfactual

Not applicable — this increment adds no code and no new assertions; there is no predicate written here to mutate. The pre-existing oracles were exercised as-is: the 3 keymap reds ARE the suite's live RED signal for the not-yet-landed keymap/README work (Inc 1's job to close), and `verify_aperture.py` is self-checking against vacuity (its "not vacuous" leg explicitly counts how many languages compose the hero detail line: 3/10).

### Reverse census

No symbol was touched, renamed, or moved by this increment, so no census probe fires. Probes run anyway for the record:

| Probe | Command | Result |
|---|---|---|
| B2 file moved on disk | `git status --porcelain` shows no `R` rename entries | did not fire |
| B4 artifact consumed elsewhere | `grep -rl "_fixture_late" prototypes/` | fixture is read by `capture.py`, `capture_languages.py`, `verify_variants.py`, `verify_widget.py`, `verify_ink.py`, `verify_language.py`, `kanban_ideas/proto.py` — all prototype tooling, all consistent with the regenerated schema (`phase_changed` field present); full suite green over it |
| A3 frozen interface changed | none — no source edited this increment | did not fire |

### Signed-balance test ledger

`post = base − deleted + added` → `778 = 778 − 0 + 0` ✓ reconciles (775 green + 3 documented reds; zero tests added or deleted by this increment)

---

## 5 · Risks

- The 3 keymap reds are EXPECTED but still RED on the trunk-facing tree: anything that grooms "zero failures" as a merge gate will block until Inc 1 closes them. They must not be "fixed" by deleting the tests — they are the acceptance signal for R-01/R-02.
- `verify_aperture.py` (and likely sibling verifiers) crash on a stock cp1252 Windows console; CI or another Windows contributor running it without `PYTHONIOENCODING=utf-8` will see a UnicodeEncodeError, not a verdict.
- The regenerated `_fixture_late.json` adds a `phase_changed` field; all current consumers are green, but any out-of-tree reader pinned to the old schema would notice.

## 6 · Pending items / spec deviations

- C-44 carry: `~/kimi/taskboard-overhaul` lives OUTSIDE this repo; it is excluded from the batch PR and remains a backlog item. Not touched.
- The 3 documented keymap reds remain open by design — owned by Inc 1 (R-01/R-02).
- Packet location deviation: the dev-flow template places packets at `.dev-flow/<batch_id>/03-increments/`, but this repo's existing packets live at `.dev-flow/03-increments/` (increments 001–003); this packet follows the repo convention per the batch instruction.

## 7 · Suggested next task

**Inc 1 — R-01 + R-02:** revive the 4 dead keys and close the 3 red tests (`test_every_shown_key_has_a_real_action_on_the_app`, `test_the_readme_keybinding_table_matches_the_seat`, `test_the_widest_bars_keep_their_words`), per requirements §3.0 / HLR-001 / HLR-002. The reds show the gap concretely: e.g. `[` (Phase−) is bound but absent from the README keybinding table.

---

## Increment gate checklist

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | ≤4 source files, or reason declared | ✓ | 0 source files — reconciliation increment, §2 |
| 2 | Tests written in this same increment | ⚠ | None written — none scoped to R-00; verification ran the existing suite + verifier (declared per notice convention) |
| 3 | Layer 0 written where the criterion applies | ⚠ | No new code paths, so the criterion does not apply |
| 4 | RED counterfactual captured and restored by hash | ⚠ | N/A — no new assertion to mutate; pre-existing oracles exercised as-is (§4) |
| 5 | Reverse census run on every touched symbol | ✓ | No touched symbols; probes B2/B4/A3 recorded incl. non-fires (§4) |
| 6 | `code-reviewer` passed — a HIGH blocks | ⚠ | No diff to review in this increment; the reviewed content is the pre-batch work already covered by `.dev-flow/02-review*.md` |
| 7 | No file from another lane touched | ✓ | Batch not forked; no source touched at all |
| 8 | Frozen interfaces untouched | ✓ | No source touched |
| 9 | Coverage claims verified on disk, not from intent | ✓ | pytest tail pasted from one complete run; verify_aperture `ALL PASSED` pasted; prism SVG read on disk; `grep -c "<figure"` = 16 |
