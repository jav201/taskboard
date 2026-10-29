# Batch close — taskboard — Batch 2026-10-29-batch-02

> **Artifact language.** Canonical **English scaffold**; generate in the batch's language — the **prose**,
> and never a label.

> **Owed in.** `core` ✓ · `full` —

> **Field guide:** `templates/guides/close-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

> **Reserved field names.** The **field names and block keywords below are language-independent** — the
> validator parses them literally and they are never translated:
> `Conditional-gate discharge` · `New controls` · `Human perimeter` · `Human review ledger` · `Gated tree` · `Found before the batch` · `⏸ DEFER`
> **And the §6 DEPTH tokens — cell VALUES rather than field names, reserved for the same reason:**
> `light` · `rigorous` · `spot-check` · `none` · `✅` · `❌`. A CLOSED set, declared closed by the first
> revision that ships it — so the vocabulary a later promotion of `V54` to BLOCK will need already exists,
> instead of being introduced over a free-text field that six authors have by then written six ways.
> Everything else on this page — headings, guidance, the prose in every cell — is translated with the batch.
> **One strategy, not two:** the flow ships no alias table, so a translated label is read as an ABSENT one and the rule keyed on it reports a true-sounding silence.
> **And one FLOW-WIDE reserved token, read out of this artifact by `V42` no matter which template minted it:** `⏸ DEFER`. It is a MARKER rather than a field name, which is why it is stated here *and* in `/dev-flow` §Language of artifacts rather than in a per-template list — a deferral can be written in any batch artifact, including the ones that carry no block at all.

> **Notice convention.** `⚠` yellow = declare and continue · `✗` red = block · `✓` green = satisfied
> **with its citation**.

---

## 0 · Gate record — which tree this close gated

| Field | Value |
|---|---|
| Gate record | `python "C:/Users/jjgh8/.claude/skills/dev-flow/scripts/devflow-validate.py" .` from the project root · exit 0 · 0 block · 178 notice · 2026-10-29 |
| Gated tree | `6ad688d1c64661be52921ec96ee34c43c954d9cb` · dirty — .dev-flow/BACKLOG.md (the close record itself excluded) |
| Requirements canon | `REQUIREMENTS.md` (`artifact_homes.requirements_canon`): 20 ids folded by `devflow-init.py --fold-canon` (US-4101, HLR-4101..4105, 14 LLR) |

---

## 1 · What changed

`taskboard --report` now exports the interactive workspace and the deck, the same two reports as `H`, into `<board dir>/reports/`, prints each path, and asks which board when the registry holds several (a number, enter for the default, `a` for all, `q` to quit). `--report PROJECT` scopes to a project, `--report-kind` picks the files, a missing `--board` path is refused before anything is built, and the command only reads. Mechanism: `run_report` and `ask_board` in `taskboard/__main__.py`, calling `report_html.extract` and `write_reports` unchanged. Example: `echo 2 | taskboard --report` prints `…oardsetaeports\workspace-2026-10-29.html` and `…\deck-2026-10-29.html`. Code commits on the local branch `feat/cli-report-html` (not pushed): `c8bc4d9`, `d30acf0`, `9a0d1b1`.

| Requirement | Version | Verified by | Verdict |
|---|---|---|---|
| `HLR-4101` | `v1` | `AT-4104` · `AT-4106` · `TC-4101` · `TC-4107` | pass |
| `HLR-4102` | `v1` | `AT-4101` · `AT-4102` · `AT-4103` · `TC-4103` · `TC-4110` | pass |
| `HLR-4103` | `v1` | `AT-4104` · `TC-4105` | pass |
| `HLR-4104` | `v1` | `AT-4105` · `TC-4106` · `TC-4110` · `TC-4113` | pass |
| `HLR-4105` | `v1` | `AT-4107` · `TC-4109` · `TC-120` | pass; LLR-4105.4 (the backlog) discharged in §4

---

## 2 · New controls discovered — and where they landed (C-45)

| Control | What failure it closes | Measured origin |
|---|---|---|

**The four landings — record which ones actually happened. Command-but-not-template is *half-encoded*, and the missing half is the enforceable one:**

| # | Landing | Done? | SHA / path |
|---|---|---|---|
| 1 | the **command** (`commands/…`) — the rule itself | | |
| 2 | its **artifact** (a template section) — a control with no output degrades to "I thought about it" | | |
| 3 | the **catalog** entry (`dev-flow-lessons`) with its measured origin | | |
| 4 | **committed and pushed**, manifest re-hashed and bumped | | |

- **New controls:** `none — no new control: the P4 failure (a second-person literal in help text) was caught by an existing law, tests/test_prism_laws.py, and the flow itself was not changed`

---

## 3 · Working-file reconciliation (C-44)

| File | State | Evidence |
|---|---|---|
| `taskboard/__main__.py`, `taskboard/app.py`, `README.md`, `tests/test_report_cli.py`, `tests/test_report.py` | ✅ committed (`c8bc4d9`, `d30acf0`, `9a0d1b1` and the deliverable commit) on the local branch `feat/cli-report-html`; NOT pushed or merged — the commission's "Do NOT push or merge"; `origin` exists, so landing is the operator's (PR or merge) | `git log feat/cli-report-html --not --remotes` |
| `REQUIREMENTS.md`, `.dev-flow/2026-10-29-batch-02/**`, `.dev-flow/state.json`, `.dev-flow/COMMISSION-cli-report-html.md`, `.gitattributes`, `.dev-flow/2026-10-29-batch-01/decisions-log.json` | ✅ committed on the same branch, not landed | same |
| `.dev-flow/BACKLOG.md` | ✅ committed in the close commit, not landed | same |
| `.scratch/` (rollover and probe scripts, reviewer probes) | 🗑️ deleted at the close; nothing running | `ls .scratch` → absent |
| `reports/` in the repo root (a mutant wrote it) | 🗑️ deleted; the harness now removes it | `git status --short` clean of it |

- **Found before the batch:** `none — no tracked file was modified when the batch began`

### Conditional-gate discharge

- **Conditional-gate discharge:** `none — no gate closed conditionally`

| Condition | Discharged? | The artifact line that proves it |
|---|---|---|

---

## 4 · Backlog reconciliation — the carry-over contract

| Item | Move | Reference |
|---|---|---|
| `--report --board <missing path>` seeds sample data (S-3) | closed | BACKLOG, marked ✓; AT-4105 |
| «The CLI report — retire, re-point or keep» (operator decision) | closed: re-pointed | BACKLOG, marked ✓ |
| retire the old static report and its law suite (D-4) | added | BACKLOG, «Open — after 2026-10-29-batch-02» |
| `--report` message polish (qa G-002, G-004) | added | same section |
| LLR-4105.1 threshold wording (qa G-001) | added | same section |
| security residuals (symlink, check-then-read, abspath) | added | same section |
| the untested fallback and Ctrl-C arms | added | same section |

---

## 5 · Batch metrics — the 13 keys of `core`

Extract, do not invent: a key the artifacts did not record goes `null`, and the key is never dropped.

```yaml
type: dev-flow-batch
project: taskboard
batch_id: 2026-10-29-batch-02
mode: core
verdict: pass
increments: 1
source_files_max: 2
notices_raised: 6
rework_returns: 3                # P2 iterate-to-refine (QA 3 major, SEC 4 medium); P3 review folds (6 LOW); P4 one prism-law failure
triggers_fired: "B1,B4,C4,C6,C8,D1"
tests_base_to_post: "3332 -> 3365"
new_control: none
open_items_next: 5
```

---

## 6 · Human review ledger — what a human audited, at what depth

| Artifact | Machine verdict (citation) | Human review | Depth | Deliberately NOT reviewed |
|---|---|---|---|---|
| `01-requirements.md` | gate `0 block`; `V26` green; scan-spec run | ❌ | `none` | read by qa-reviewer and security-reviewer (agents), not by a human |
| Tests / ATs | mutation 27/27 KILLED; 3365 passed | ❌ | `none` | no human read the tests |
| Code (`taskboard/__main__.py`) | gates + code-reviewer PASS, security-reviewer PASS | ❌ | `none` | not audited by a human |
| README | `TC-120`, `TC-4109` | ❌ | `none` | not read by a human |

**A worked example — text to read, never rows of your record.** It sits in a fence so that
nothing has to be deleted: a row copied out of it would claim a reading that did not happen.
Write your own rows in the table above, one per artifact.

```text
| *(example)* `01-requirements.md` | gate §4 ✓ · `V26` green | ✅ | `rigorous` | |
| *(example)* Test cases / ATs | `V37` 12/12 · mutants 9/9 KILLED | ✅ | `light` | the fixture matrix behind `AT-007` |
| *(example)* Evidence view | `V41` — every cited file resolved | ❌ | `none — read the packet summaries instead` | |
| *(example)* Code | gates + reviewer verdict `PASS` | ✅ | `spot-check` | not audited line by line |
```

- **Human perimeter:** `the operator owns the prompt's wording and feel on a real terminal (no TTY and no user evaluation was run), the decision to push and merge, and when to retire the old static report`
- **Human review ledger:** `none — this batch ran under a standing authorization with spawned reviewer agents; no human reviewed an artifact`
