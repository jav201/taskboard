# Increment 003 — LLR-2306.2 · `the hardened tests and the hygiene law`

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
> `.dev-flow/2026-10-20-batch-02/03-increments/increment-003.md`. It is not synced to the vault.

> **Notice convention.** `⚠` yellow = notice: does not block, obliges you to DECLARE the reason here.
> `✗` red = block. `✓` green = satisfied **with its evidence cited**. A notice repeated for three
> consecutive batches becomes a rule or is retired.

> **A table you may delete.** A table whose `| **Field** |` row reads `none — <reason>`, or whose question one line of the gate checklist answers, may be deleted, its field row kept: `stations/core-runbook.md` §*A minimal increment packet* is a one-function change written that way.

| Field | Value |
|---|---|
| Batch | `2026-10-20-batch-02` |
| Increment | `003` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | `HLR-2306` / `LLR-2306.2` |
| Acceptance | `AT-2306` · the hardened nodes AT-2204, AT-2104, AT-2106, AT-2102 (of batches 2026-10-20-batch-01 and 2026-10-19-batch-01) · unit: `_unread_names` and `_cursor_rows` are test helpers, exercised by the nodes that use them |
| Agent | `software-dev` (the orchestrator, self-implemented) |
| Date | `2026-10-20` |

---

## 1 · What changed

The suite now reads what the screen shows, and a law keeps it so. `tests/test_boards_forms.py` drops its unused `PAYLOADS` and reads a card's title through Textual's public `border_title` (`Text.from_markup(…).plain`, its `Text` import now read). AT-2204 asserts the key `B` beside `Boards` in the `?` help's keys and reaches `R` with the selection the board opens with. AT-2104 asserts the cursor's row in view 3 — the timeline row holding `⟦`, the tick row aside — after `→` (`Billing Migration`) and `↓` (`Dual-run reconciliation`), beside the tick row it already read; AT-2102 reads the rail's `▶` row instead of `_all_cur`; AT-2106 drives `u` in view 2 too. `tests/test_hygiene.py` gains AT-2306: `_move_target(self, proj, bid)`, no test reads `._border_title`, and every name `tests/test_boards_forms.py` binds by an import or a plain assignment is read. `.dev-flow/BACKLOG.md` marks the eight items `✓ done in 2026-10-20-batch-02` and opens this batch's section with what is still open.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `tests/test_boards_forms.py` | test | HLR-2306, LLR-2306.2 | `PAYLOADS` dropped; the public `border_title` |
| `tests/test_boards_home.py` | test | HLR-2306, LLR-2306.2 | AT-2204: the `B` key in the help; `R` by keys |
| `tests/test_present_all.py` | test | HLR-2306, LLR-2306.2 | `_cursor_rows`; AT-2104, AT-2102, AT-2106 hardened |
| `tests/test_hygiene.py` | test | HLR-2306, LLR-2306.1, LLR-2306.2 | AT-2306, `_unread_names` |
| `.dev-flow/BACKLOG.md` | doc | HLR-2301, HLR-2302, HLR-2303, HLR-2304, HLR-2305, HLR-2306 | the done marks; the batch's open section |
| `.dev-flow/2026-10-20-batch-02/evidence/mutate-003.py` | doc | HLR-2306 | the increment's mutation battery |

| Count | Value |
|---|---|
| **SOURCE files** | **0 / 4** |
| Test files | 4 (uncapped) |

## 3 · How to test

`python -m pytest -q -p no:cacheprovider tests/test_hygiene.py tests/test_boards_forms.py tests/test_boards_home.py tests/test_present_all.py` (with `NO_COLOR` unset); `python .dev-flow/2026-10-20-batch-02/evidence/mutate-003.py`.

## 4 · Test results

| Layer | Nodes | Result |
|---|---|---|
| B and the law | `tests/test_hygiene.py::test_AT_2306_the_hygiene_law`; the hardened `test_AT_2204_the_home`, `test_AT_2104_three_views_one_cursor_and_the_export`, `test_AT_2102_the_order_and_hidden_projects_survive_a_restart`, `test_AT_2106_u_lists_the_hidden_and_brings_one_back`, `test_TC_2205_a_typed_name_paints_literally` (the `border_title` read) | executed: 104 passed in the four files (`suite-003.txt`) |
| full suite | owed at the P4 gate run | not-run |

| Field | Value |
|---|---|
| **RED counterfactual** | AT-2306 on increment 002's commit `9cec898` (a clean worktree, the hardened files untouched, `tests/test_hygiene.py` copied in): 1 failed — `['test_boards_forms.py']` (the `._border_title` needle), TC-2306 passing (002 already shipped the signature) · `.dev-flow/2026-10-20-batch-02/evidence/red-003.txt`. The hardened ATs test shipped behaviour, so their RED is each one's mutation below |
| **Mutation verdicts** | 7 arms, one run, each restore proven by digest: the `B` key left out of the help's keys, the word kept (`modals.HelpModal._key_texts`) · KILLED (AT-2204); the cursor's echo drawn on every other row (`views._all_echo_span`) · KILLED (AT-2104); `u` inert in view 2 (`PresentScreen.action_hidden_picker`) · KILLED (AT-2106); the rail's cursor on the next row (`views` rail) · KILLED (AT-2102); `PAYLOADS` back in `tests/test_boards_forms.py` · KILLED (AT-2306); the private `_border_title` read again · KILLED (AT-2306); `_move_target`'s parameter back · KILLED (AT-2306) · arms that stayed GREEN: none · `.dev-flow/2026-10-20-batch-02/evidence/mutation-003.txt` |
| **Instrument RED-proof** | 1 instrument: `evidence/mutate-003.py` — increment 001's harness with this increment's arms (its first draft would not compile — a newline unescaped in an anchor — and was fixed before any run); `arms: 7` |
| **Emitted-form assertion** | none — this increment emits no artifact; the nodes read the screen's widgets (`#help-keys`, `#present-frame`, `#picker-rows`, a card's `border_title`) |
| **Reverse census** | 4 probes: B1 `grep -rn "_all_cur" tests/test_present_all.py` → 12 (from 14): the white-box TCs and the `goto` helper keep it — declared in LLR-2306.2's scope; `grep -rn "_border_title" tests/` → none (`tests/test_hygiene.py` holds only the needle's two parts, `"._border" + "_title"`) · B2 no file moves · B3 no golden capture changes · B4 none — 0 foreign hits |
| **Correction population** | 5 shipped assertions changed, each strengthened and never weakened: AT-2204's `"Boards" in _all_text(…)` → the `B` key's regex over `#help-keys`; AT-2204's `selected_task_id` set-up → an assertion that the board opens with a selection; AT-2104 gains two cursor-row assertions beside its tick-row ones; AT-2102's `_all_cur == ("proj", "pmr")` → the rail's single `▶` row is Mobile Release's; `test_boards_forms`'s `card._border_title.plain` → the public `border_title` parsed |

### Evidence files

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| suite-003.txt | .dev-flow/2026-10-20-batch-02/evidence/suite-003.txt | 64329309895dd2d3143d461c593c2339da178f713764b90bc5d5b9345117d2d8 |
| red-003.txt | .dev-flow/2026-10-20-batch-02/evidence/red-003.txt | 649364560dabac952263ff13a54ad07b3c67a1e9b6fec9e374cc34e6d34db81a |
| mutation-003.txt | .dev-flow/2026-10-20-batch-02/evidence/mutation-003.txt | a5b48c10d32e9eb92dfba4c5b3f30b7e0ed43cb450fbf678997514e9dd9a0fd5 |
| mutate-003.py | .dev-flow/2026-10-20-batch-02/evidence/mutate-003.py | d818df7564d64c3867a6c7c71ddbc1ea27e3ca51b582a8da729cb3054278f754 |
| inc003.diff | .dev-flow/2026-10-20-batch-02/evidence/inc003.diff | 615b3d72f88e7b9c71089583dd2eae26b3e3ed346221b9f4697016626d6ddd9b |

| Field | Value |
|---|---|
| **Evidence files** | 5 artifacts, each at the declared home with the digest of its stored bytes |

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` · **OK to advance** (PASS) · no findings; LLR-2306.2 verified by re-read (public observations replace `_border_title`/`_all_cur` in the ATs; H1–H7 KILLED); `BACKLOG.md`'s done marks and new open items checked true against the code |

## 5 · Risks

`_cursor_rows` reads the frame's text: a renderer change to the cursor's glyphs fails AT-2104 loudly rather than passing silently; the hygiene law reads only `tests/test_boards_forms.py` for unread names (the backlog item's file), not the whole suite.

## 6 · Pending items / spec deviations

The full suite is owed at P4. `_all_cur` stays in the white-box TCs and the `goto` navigation helper (12 reads; no public observation of the task cursor exists with the rail focused) — within LLR-2306.2, which names the two AT nodes that drop it.

## 7 · Suggested next task

The DDR, then Phase 4.

## Increment gate checklist

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | SOURCE budget | ✓ | §2: 0 source files |
| 2 | Tests in this increment | ✓ | four test files |
| 3 | Layer 0 where it applies | ✓ | not due: no source unit changed |
| 4 | RED counterfactual | ✓ | §4, `red-003.txt` + the battery |
| 5 | Reverse census | ✓ | §4: 4 probes, 0 foreign hits |
| 6 | `code-reviewer` passed | ✓ | §4b |
| 7 | No file from another lane | ✓ | one lane |
| 8 | Frozen interfaces untouched | ✓ | none frozen |
| 9 | Coverage verified on disk | ⚠ | `suite-003.txt` (targeted); the full run owed at P4 |
| 10 | Load-bearing emptiness | ✓ | the census's greps quoted |
| 11 | Mutation verdicts | ✓ | §4: 7/7 KILLED |
| 12 | Instrument RED-proof | ✓ | §4 |
| 13 | Correction population | ✓ | §4: 5 strengthened, declared |
| 14 | Emitted-form assertion | ✓ | §4: none, declared |
| 15 | Independent review | ✓ | §4b |
| 16 | Evidence files | ✓ | §4: the digests |
