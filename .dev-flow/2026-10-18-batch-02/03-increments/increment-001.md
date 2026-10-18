# Increment 001 — <REQ-ID> · `<Short title>`

> **Artifact language**
> This template is the canonical **English scaffold**. Generate the artifact in the batch's development
> language — the **prose**, and never a label. **Where that language is declared:**
> `state.json`'s `language` key in `core` and `full`. The normative RULES below are
> language-independent.

> **Owed in.** `core` ✓ · `full` ✓

> **Field guide:** `templates/guides/increment-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

> **Reserved field names.** The **field names and block keywords below are language-independent** — the
> validator parses them literally and they are never translated:
> `SOURCE files` · `Instrument RED-proof` · `Correction population` · `Mutation verdicts` · `Emitted-form assertion` · `Reverse census` · `RED counterfactual` · `Independent review` · `Evidence files` · `Traces to` · `File` · `Kind` · `source` · `test` · `doc` · `config` · `generated` · `fixture` · `⏸ DEFER`
> Everything else on this page — headings, guidance, the prose in every cell — is translated with the batch.
> **One strategy, not two:** the flow ships no alias table, so a translated label is read as an ABSENT one and the rule keyed on it reports a true-sounding silence.
> **And one FLOW-WIDE reserved token, read out of this artifact by `V42` no matter which template minted it:** `⏸ DEFER`. It is a MARKER rather than a field name, which is why it is stated here *and* in `/dev-flow` §Language of artifacts rather than in a per-template list — a deferral can be written in any batch artifact, including the ones that carry no block at all.

> **Where this lives:** the **repo**, next to the diff it describes —
> `.dev-flow/2026-10-18-batch-02/03-increments/increment-001.md`. It is not synced to the vault.

> **Notice convention.** `⚠` yellow = notice: does not block, obliges you to DECLARE the reason here.
> `✗` red = block. `✓` green = satisfied **with its evidence cited**. A notice repeated for three
> consecutive batches becomes a rule or is retired.

> **A table you may delete.** A table whose `| **Field** |` row reads `none — <reason>`, or whose question one line of the gate checklist answers, may be deleted, its field row kept: `stations/core-runbook.md` §*A minimal increment packet* is a one-function change written that way.

| Field | Value |
|---|---|
| Batch | `2026-10-18-batch-02` |
| Increment | `001` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | `HLR-1901` / `LLR-1901.1` · `HLR-1902` / `LLR-1902.1` |
| Acceptance | `AT-1901`, `AT-1902` · white-box `TC-1901` · unit `TC-1902` |
| Agent | `software-dev` (the orchestrator, self-implemented) |
| Date | `2026-10-18` |

---

## 1 · What changed

The suite tells the truth about two things, test-side only. **The standup tests**: the 2026-10-11 scrub (`6bff525`) replaced the fixture's 6-cell roster name with the 16-cell placeholder `username_subject`; the standup paints names in a 12-cell column (`views.py:4303`, `fit` → `username_su…`), so the tests' substring search for the whole placeholder found no row and both failed on `origin/main`. The source was right; the tests now find a row by its 12-cell name cell equal to `views.fit(name, 12)` (`_row_named`, which also refuses a substring or a second match), keep every original assertion, and gain a name-column arm (a 12-cell name whole, a 13-cell name cut) and an app-level AT (key `8`). **The clipboard test**: its loop moved into `_clipboard_roundtrip`, which returns a skip reason only when Windows refused `Set-Clipboard` on every attempt; a held sample read back wrong (the handle bug) and a sample set but never still held after our read (contention, or a reader that disturbs the clipboard) both FAIL; `test_win_clipboard_roundtrip` restores the prior clipboard in `finally` and skips after it. TC-1902 proves both arms with a fake machine; AT-1902 runs the real test body with its one seam `_ps` faked. **The six round files** that no longer import (`prototypes/present_rulers/{proto,app_capture}.py`, `prototypes/present_views/{views_proto,views_d,app_capture,app_capture2}.py`) carry a `HISTORICAL` docstring header naming why and the commit they last ran against (`de9c4a2`, `9810be6`); not repaired, by the PLAN's key decision.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `tests/test_team_views.py` | test | HLR-1901, LLR-1901.1 | `_row_named` locator, `SELF_NAME`, `NAME_CELLS`; the two standup nodes repointed to it (assertions kept); new `test_TC_1901_the_name_column_cuts_at_twelve_cells`, `test_AT_1901_the_standup_marks_the_operators_own_row`; imports `fit`, `_strip` |
| `tests/test_app.py` | test | HLR-1902, LLR-1902.1 | `_clipboard_roundtrip`, `_seed_clipboard`; `test_win_clipboard_roundtrip` through the helper (docstring: the fourth defect); `_Clip` fake; `test_TC_1902_the_roundtrip_verdict` (6 arms), `test_TC_1902_a_held_sample_read_wrong_is_the_handle_bug`, `test_AT_1902_a_refused_setup_skips_with_its_reason` |
| `prototypes/present_rulers/proto.py` | doc | PLAN inventory #5 (doc rows trace nothing) | `HISTORICAL` header |
| `prototypes/present_rulers/app_capture.py` | doc | PLAN inventory #5 (doc rows trace nothing) | `HISTORICAL` header |
| `prototypes/present_views/views_proto.py` | doc | PLAN inventory #5 (doc rows trace nothing) | `HISTORICAL` header |
| `prototypes/present_views/views_d.py` | doc | PLAN inventory #5 (doc rows trace nothing) | `HISTORICAL` header |
| `prototypes/present_views/app_capture.py` | doc | PLAN inventory #5 (doc rows trace nothing) | `HISTORICAL` header |
| `prototypes/present_views/app_capture2.py` | doc | PLAN inventory #5 (doc rows trace nothing) | `HISTORICAL` header |

| Count | Value |
|---|---|
| **SOURCE files** | **0 / 4** |

## 3 · How to test

`python -m pytest -q -p no:cacheprovider -rs tests/test_team_views.py tests/test_app.py -k "standup or clipboard_roundtrip or TC_1902 or AT_1902 or AT_1901"` (with `PYTHONDONTWRITEBYTECODE=1 PYTHONIOENCODING=utf-8`); the battery: `python .dev-flow/2026-10-18-batch-02/evidence/mutate.py 001` from the root of a scratch copy of the tree; the inspection: `grep -n HISTORICAL prototypes/present_rulers/*.py prototypes/present_views/*.py` → the six files.

## 4 · Test results

| Layer | Nodes | Result |
|---|---|---|
| 0 | `tests/test_app.py::test_TC_1902_the_roundtrip_verdict` ×6, `::test_TC_1902_a_held_sample_read_wrong_is_the_handle_bug` (TC-1902) | in the full suite (`suite-001.txt`) |
| A | `tests/test_team_views.py::test_standup_renders_one_row_per_member_and_own_row_identifiable`, `::test_standup_flags_stale_member_in_over_tone`, `::test_TC_1901_the_name_column_cuts_at_twelve_cells` (TC-1901) | in the full suite (`suite-001.txt`) |
| B | `tests/test_team_views.py::test_AT_1901_the_standup_marks_the_operators_own_row` (AT-1901), `tests/test_app.py::test_AT_1902_a_refused_setup_skips_with_its_reason` (AT-1902) | in the full suite (`suite-001.txt`) |
| full suite | `python -m pytest -q -p no:cacheprovider -rs` on the working tree with increment 001 | 0 failed, 2733 passed (`suite-001.txt`; base 2 failed, 2721 passed: + 10 new nodes, the 2 repaired now pass) |

| Field | Value |
|---|---|
| **RED counterfactual** | on `base_ref` `9e82b10` (a `git archive` export): the two standup nodes as base has them fail (`2 failed`), and AT-1902 appended to base's `tests/test_app.py` fails (`AssertionError: SETUP failed — … Requested Clipboard operation did not succeed.`) where a skip is required · `.dev-flow/2026-10-18-batch-02/evidence/red-001.txt` · the RED ran on the export, no file of the tree was mutated (restore digests of the battery below) |
| **Mutation verdicts** | 8 mutants, 12 arms, all KILLED: M1 the operator's row muted (`if is_self` → `if not is_self`, `views.py` the standup's spine) → TC-1901 ×1, AT-1901 · M2 the stale tone on every row → TC-1901 (stale) · M3 the name column 13 → TC-1901 (12/13 arm) · M4 the skip keyed on the last attempt (PC-1) → TC-1902 [contended-then-refused-x4] · M5 a refusal raises → TC-1902 [refused-x5], AT-1902 · M6 contention returns a reason → TC-1902 ×3 · M7 a mismatch passes → TC-1902 (handle bug) · M8 the skip becomes a failure → AT-1902 · arms that stayed GREEN: none · `.dev-flow/2026-10-18-batch-02/evidence/mutation-001.txt` · restore digests `460cf8128c61…` (`views.py`), `db482b3c6c80…` (`tests/test_app.py`), each re-hashed after every arm |
| **Instrument RED-proof** | 1 instrument: `evidence/mutate.py` — its first run reported `BAD (anchor matched 2 times)` / `0 times` for M1/M2 (the standup and people views share the spine line; a CRLF checkout) before any verdict was believed; the anchors were made unique and CRLF-aware and the run repeated (`mutation-001.txt` is that run) |
| **Emitted-form assertion** | 2 artifacts: the standup frame as `#board` renders it (`str(app.query_one("#board").render())`, AT-1901) and as `render_standup` returns it (plain and markup, TC-1901); the pytest outcome as `pytest.skip.Exception`'s message (AT-1902) |
| **Reverse census** | 5 probes: B1 `grep -rl "render_standup\|username_subject" tests/` → `test_team_views.py` (this increment) and `test_present_views_app.py` (`username_subject` inside a note's text, not the standup — untouched, green in `suite-001.txt`); `grep -rl "grab_clipboard_text\|_clipboard_now\|_ps_literal" tests/` → `test_app.py` only · B2 no file moved · B3 no golden; no oracle frame touched · B4 no artifact written · A3 no interface: `render_standup` and `grab_clipboard_text` unchanged — 0 foreign hits left un-revalidated |
| **Correction population** | none — no correction |

### Evidence files

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| suite-001.txt | .dev-flow/2026-10-18-batch-02/evidence/suite-001.txt | 2c9954e3affcd9b6ac9581b4f52b5f4b1b74f31d73c47a4e5b6e6a2b8670ffab |
| red-001.txt | .dev-flow/2026-10-18-batch-02/evidence/red-001.txt | e5042cedb6b86a75538455f7a5d39526c2a02c18caceaa29692a000fcb92a892 |
| mutation-001.txt | .dev-flow/2026-10-18-batch-02/evidence/mutation-001.txt | ca11416732aa96e86e25bfbc989cae1cff6acb3b521144502fbdd09a0a61d497 |

| Field | Value |
|---|---|
| **Evidence files** | `3 artifact(s), each at the declared home, with the digest of its bytes on disk` (the battery `mutate.py` is committed beside them; it grows per increment, so its digest is recorded in the last packet that runs it) |

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned with agents/code-reviewer.md · OK to advance, 0 HIGH, 0 MEDIUM · L1 (AT-1901 slices Ana's name cell by hand instead of `_row_named`), L2 (`_Clip.sample` first set in `seed`), L3 (`monkeypatch.setitem(globals(), …)` idiom) → accepted as written: style only, each node is KILLED by its battery row, and editing would move the reviewed set · L4 (pre-existing: the restore's own result unchecked; a failed `Get-Clipboard` clears the clipboard on restore) → carried to `BACKLOG.md` |

## 5 · Risks

The clipboard test now skips where it failed; the skip is limited to a refusal on every attempt, so a reader regression still fails (M4, M6). The real node passed on this host in `suite-001.txt` (`test_win_clipboard_roundtrip` passed, no skip reported).

## 6 · Pending items / spec deviations

- LED .5: the contract's 13-cell literal `thirteen_cel…` corrected to `thirteen_ce…` (found by TC-1901's first run).
- L4 → `BACKLOG.md` at the close.

## 7 · Suggested next task

Increment 002 — the presentation at any width.

## Increment gate checklist

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | SOURCE budget | ✓ | §2: 0 source files |
| 2 | Tests in this increment | ✓ | §2: 2 test files, 11 new or repointed nodes |
| 3 | Layer 0 where it applies | ✓ | `_clipboard_roundtrip` (cyclomatic 5): TC-1902 |
| 4 | RED counterfactual | ✓ | §4, `red-001.txt` |
| 5 | Reverse census | ✓ | §4: 5 probes |
| 6 | `code-reviewer` passed | ✓ | §4b: 0 HIGH |
| 7 | No file from another lane | ✓ | one lane |
| 8 | Frozen interfaces untouched | ✓ | none frozen |
| 9 | Coverage verified on disk | ✓ | `suite-001.txt` |
| 10 | Load-bearing emptiness | ✓ | no claim rests on an absence |
| 11 | Mutation verdicts | ✓ | §4: 12/12 KILLED |
| 12 | Instrument RED-proof | ✓ | §4 |
| 13 | Correction population | ✓ | §4: none, declared |
| 14 | Emitted-form assertion | ✓ | §4 |
| 15 | Independent review | ✓ | §4b |
| 16 | Evidence files | ✓ | §4: digests |
