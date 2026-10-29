# PLAN — taskboard — Batch 2026-10-29-batch-02

> **Artifact language.** Canonical **English scaffold**; generate in the batch's language.
> **Owed in.** `core` ✓ · `full` ✓
> Seeded by `/dev-flow-init` step 4 at both levels; the living plan is owed at every gate
> that follows (`/dev-flow` §Living plan is the rule's home).

> **Field guide:** `templates/guides/plan-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.
> **Two header labels are read literally and are never translated:** `Standing authorization` and `Last updated`; the field guide names their readers.

The living compendium of this batch: where-we-are · objective · per-story/per-station status ·
roadmap + increment plan · key decisions · risks/watch-items · conventions honored ·
out-of-scope carries · test ledger · decision log (the human-readable mirror of `state.json`).
**Create at batch open and update at every gate and significant checkpoint** — the
orchestrator presents the full plan in-conversation at each phase gate.

## Header

| Field | Value |
|---|---|
| Project | taskboard |
| Batch | 2026-10-29-batch-02 |
| Objective | `taskboard --report` exports the new HTML reports (workspace B and deck C) through the code path the `H` modal uses, asks which board when the registry holds more than one (number, enter = default, a = all, q/EOF = exit 1, non-TTY empty = exit 2), keeps PROJECT as the project scope, refuses a missing --board path before building anything, and retires the old static report from the CLI (CR-1..CR-5) |
| Last updated | P4 · 2026-10-29 |
| Standing authorization | The operator (`username_subject`), 2026-10-29, on the review of `2026-10-29-batch-01` (which answered `"push": "si"`): «Que el comando --report exporte el html, que pregunte por el board.», quoted in `.dev-flow/COMMISSION-cli-report-html.md`; the orchestrator's task: gates close under it, «Do NOT push or merge». Read from the commission and the task: autonomy over the gates P0..P5; push and merge NOT granted; a HIGH finding blocks regardless and returns to the operator; independent review by spawned reviewers (code-reviewer, security-reviewer for CR-5, qa-reviewer at P4). |
| First gate | start run (`evidence/gate-start.txt`, over the closed 2026-10-29-batch-01 record, after the rollover re-stamped `base_ref`): exit 0 · 0 block · `V7`: bundle identical to the manifest it ships, both directions (57 declared files unmoved, 0 undeclared) at `2026-10-12-rev102` · `V25`: origin answered (5 refs, newest 0.01 day) · `V30` half (3.12.7 witnessed). The pre-rollover `--brief` run at the start also read 0 block / 180 notice. |
| Premises / RC-1 | `origin/main` verified at `4ca4a7d` (`4ca4a7d0e2de3c17ecc0f5231660e309b2cb50b6`, 2026-10-29 11:55 -0600) after `git fetch origin`; RC-1(a): HEAD is 0 behind and 1 ahead (the commission commit) — no rebase; RC-1(b): the story is NOT already shipped — `git show origin/main:taskboard/__main__.py` still imports `write_report` at line 73 and has no `report_html` (`evidence/rc-p0.txt`); RC-2: `git ls-remote --exit-code --heads origin` exit 0, 5 heads. Premises: the in-app `H` path (`report_html.extract` + `write_reports`) is the single code path; synthetic data only; CLI tests are subprocesses on a temp HOME and USERPROFILE. |

## Triggers

The trigger evaluation `state.json`'s `triggers.record` points at: one row per trigger evaluated, fired or not.

| Id | Verdict | Probe output |
|---|---|---|
| A1 | not fired | judged — no new module: the CLI logic lands in `taskboard/__main__.py` |
| A2 | not fired | judged — one module is edited (`__main__`); `report.py` is deliberately untouched (CR-4 decision below), the rest is README and tests |
| A3 | not fired | judged — no interface another module consumes changes; `report_html.extract`/`write_reports`, `Registry`, `peek_board`, `Directory.load` are consumed unchanged |
| A4 | not fired | judged — one increment |
| B1 | fired | `grep -rl "taskboard.__main__\|entry.main\|--report" tests/` → test_report (2 CLI tests), test_boards_backlog_round (TC-2410 `--open` + `--report`), test_readme (TC-120 flags vs README), plus the files that import `open_app` — reverse census at P2/P3 (`evidence/reverse-census.txt`) |
| B2 | not fired | judged — no file moves |
| B3 | not fired | probe — `tests/goldens/` does not exist |
| B4 | fired | judged — the CLI writes files that the browser consumes → output-then-consume AT (AT-4106 loads the written files headless) |
| C1, C2, C3, C5, C7 | not fired | judged — no auth, secrets, external integration, destructive DB or network service |
| C4 | fired | judged — `a` writes every board's data into one folder; a wrong pick would expose a board (same exposure as `H`, now reachable from a script) |
| C6 | fired | judged — a new input surface: a line read from stdin and the argv |
| C8 | fired | judged — board names and file paths are file-derived text printed to a terminal (control bytes) |
| D1 | fired | judged — the CLI prompt and its messages are something the user sees and types |
| D2 | not fired | judged — Python generating HTML, the same technology as the target |
| E1 | not fired | judged — 1 story, 1 increment |
| E2, E3 | not fired | judged — no high-risk or client/regulated context |
| F1 | not fired | bundle runtime — the `V7` line stands as the probe (bundle identical to its manifest at `2026-10-12-rev102`) |
| F2 | not fired | `.dev-flow/BACKLOG.md` line 7 «Last refresh: 2026-10-29 (2026-10-29-batch-01 close)» = the last close |
| ARQ · PDR · DDR | not taken up | A1..A4 did not fire, so none of the three stations is in `stations_active` |

## Where we are

P3 closed under the standing authorization: increment 001 is committed (`c8bc4d9`, review folds `d30acf0`); `code-reviewer` PASS with notes (0 HIGH, 6 LOW, all folded and re-read), `security-reviewer` PASS (0 HIGH, F1 folded, F2/F3 accepted), 27 of 27 mutants killed, 89 passed in the affected files (`evidence/suite-001.txt`), gate 0 block (`evidence/gate-p3-001.txt`). The station is P4: the full suite in three sequential chunks, then `qa-reviewer`. Owed after: the close (fold canon, backlog, `05-close.md`).

## Objective

`taskboard --report` writes the new HTML reports (B workspace, C deck) through the code path the `H` modal uses, asks which board when the registry holds more than one, keeps `PROJECT` as the project scope, refuses a missing `--board` path before anything is built, and no longer reaches the old static report. The commission is `.dev-flow/COMMISSION-cli-report-html.md`.

## Per-story / per-station status

| Story / station | Status | Notes |
|---|---|---|
| P0 | closed | rollover, plan, triggers, gate (`evidence/gate-p0.txt`) |
| P1 | closed | contract, ledger (empty), scan, gate (`evidence/gate-p1.txt`) |
| P2 | closed | one iterate-to-refine pass; `02-review.md` |
| P3 | closed | increment 001 (`increment-001.md`) |
| P4 | in progress | full suite in 3 chunks, qa-reviewer |
| US-4101 | READY | HLR-4101..4105 |

## Roadmap + increment plan

One increment, `001`: `taskboard/__main__.py` (the report flow), `README.md` (the `--report` section and the command table), and tests (`tests/test_report_cli.py` new; `tests/test_report.py` two CLI tests changed). SOURCE budget 2 / 4.

## Key decisions

| Date | Decision | Why |
|---|---|---|
| 2026-10-29 | CR-1..CR-5 are taken from the commission as written. | The operator chose the behaviour; the commission records each decision. |
| 2026-10-29 | **CR-4 decision:** `taskboard/report.py` stays byte-unchanged. | The commission removes dead entry points «only if nothing else uses them». `write_report`, `build_report` and `report_path` are used by `tests/test_report.py` (the old report's own law suite) and `report_path` is TC-3123's oracle for `report_html.slug`; `_e` and `_due_word` are what the new reports import. Retiring the old static report with its law suite is its own batch and is recorded in the backlog. The CLI no longer reaches it. |
| 2026-10-29 | **CR-2a:** a piped (non-TTY) stdin is READ for the answer; only an EMPTY non-TTY stdin exits 2. | AT-a and AT-b feed `2\n` / `a\n` through a subprocess pipe, which is not a TTY, so «non-TTY never prompts» cannot mean «never reads». A non-TTY stdin that is at EOF before any line exits 2 with the board list and `--board PATH`; a TTY at EOF, a later EOF, or `q`, exits 1. The Windows NUL device (`subprocess.DEVNULL`) reports `isatty() == True` (`evidence/premise-probes.txt` P5), so it takes the exit-1 arm; the tests use a pipe or a fake stream. A held-open pipe with no data would wait, as any pipe does; the tests use `input=` or `DEVNULL`. |
| 2026-10-29 | **CR-2b:** the board list and the prompt go to stderr; the written paths go to stdout, one per line. | A script can capture the paths without the prompt. |
| 2026-10-29 | **CR-5a:** `--report` never registers a board and never touches the registry's `last`. | Reading never writes; `--board PATH` keeps `--report`'s old meaning of «this file, read-only» (today's test already asserts `~/.taskboard` is not created). |
| 2026-10-29 | **CR-3a:** `--report PROJECT` with several boards asks first, then looks the project up on the chosen board; with `a` it is refused (exit 2, nothing written). | The commission says `a` refuses PROJECT. |
| 2026-10-29 | **CR-1a:** with `a` the files land in the default board's `reports/`; a missing or unreadable board is skipped and counted on stderr. | `H` writes beside the open board and skips and counts the same way. |

## Risks / watch-items

- A script that used `--report` for the old file now gets two paths and a different file — intended by the operator; the README says so.
- `Registry.load` may copy an unreadable `boards.json` aside (`keep_aside`), the pre-existing S-2 behaviour of every start; a report run inherits it. Accepted and declared; no board file is written.
- A pipe held open with no data waits (CR-2a); the tests never do that.

## Conventions honored

- Tests run as `env -u NO_COLOR python -m pytest`; the import probe first (`evidence/import-probe.txt`).
- CLI tests are subprocesses on a temp HOME and USERPROFILE; synthetic data only; the placeholder `username_subject`.
- English for code, artefacts and commits; `.scratch/` deleted at close.

## Out-of-scope carries

- Retiring `report.py`'s static report and its law suite (CR-4 decision): to the backlog at close.
- No push, no merge.

## Gate notices and runtime absences

**Runtime absences (SKILL.md gate step 5), named once.** No slash commands, no hooks, no prompt guard. Reviewer roles are a generic sub-agent tool carrying the role file from `agents/` as its instructions: `code-reviewer` (increment), `security-reviewer` (CR-5), `qa-reviewer` (P4) — each spawned, never self-executed. No operator to prompt: the standing authorization above closes the gates. `V15`, `V16`, `V17` `not-run` (a bundle has no canon tree, checkout table or `settings.json`); `V30` half; `dev-flow-sync` `not-run` (no export destination; push and merge not granted).

**Gate notices.** `V25`/`V30` benign on this runtime. `V40` benign after the rollover re-stamped `owner`. Older-batch NOTICEs (`V23`, `V42`, `V53`, `V9`) belong to sealed records and are not this batch's. The rest are the seeded-placeholder NOTICEs of the runbook's step-3 row; each leaves as its row fills the field.

## Test ledger

| Suite / command | Last run | Result |
|---|---|---|
| import probe (`python -c "import taskboard…"` from the repo root) | 2026-10-29 | worktree path (`evidence/import-probe.txt`); from `tests/` it imports the MAIN checkout, so CLI tests pass `cwd=` the repo root |
| affected files (report_cli, report, readme, backlog_round, report_html) | 2026-10-29 | 89 passed (`evidence/suite-001.txt`) |
| mutation battery | 2026-10-29 | 27 killed, 0 survived (`evidence/mutation-001.txt`) |
