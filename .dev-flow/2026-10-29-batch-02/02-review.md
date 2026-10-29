# Review — taskboard — Batch 2026-10-29-batch-02

> **Artifact language:** canonical English scaffold. Generate in the batch's development language (`state.json` `language`).
> Phase 2 artifact. Reviewers: `qa-reviewer` and `security-reviewer` (trigger family C fired), each spawned as a generic agent carrying its role file from `agents/`; no `architect` lens (A1..A4 did not fire; one module is edited).

> **Owed in.** `core` ✓ · `full` ✓

## ✅ Verdict (read first)

- **Gate:** `approve` → Phase 3 (after one `iterate-to-refine` pass, recorded in the ledger as `LED-2026-10-29-batch-02.1` to `.6`)
- **Out-of-scope findings:** `none`

- **Findings:** 0 blocker · 3 major (QA-1, QA-2, QA-3, all fixed in the contract) · 4 medium security (SEC-1..SEC-4, fixed) · minors fixed or accepted below
- **shall/should check:** ✓ clean
- **Two-layer (blockers):** ✓ every story has an `AT` · output reqs name deliverable+observation · both trace chains complete · ATs are genuinely black-box (AT-4107 trimmed to its stdout arm after QA-4)
- **Census (change-first):** done — best-effort + gate-confirmed
- **Security:** ⚠ 4 medium + 4 low findings, 5 closed in the contract, 3 accepted as residual in §6.3
- **Evidence checklists (qa / security):** ✓ both returned complete

---

## Detail (reference)

### Findings
| ID | Reviewer | Severity | Area / Req | What | Recommendation | Status |
|----|----------|----------|------------|------|----------------|--------|
| QA-1 (F-1) | qa-reviewer | major | HLR-4105 | the two CLI tests of the old report in `tests/test_report.py` would go RED and no requirement owned them | LLR-4105.3: rewrite both, justify (D-7) | fixed (`.5`) |
| QA-2 (F-2) | qa-reviewer | major | LLR-4101.2 | the `reports/` OSError arm had no statement or TC | statement added; TC-4111 | fixed (`.5`) |
| QA-3 (F-3) | qa-reviewer | major | LLR-4102.4 / 4104.1 | `a` with an unreadable default board: the folder was undefined | first readable board's folder; TC-4112 | fixed (`.5`) |
| QA-4 (F-4) | qa-reviewer | minor | AT-4107 | white-box arms inside an AT | stdout only in the AT; the pins move to TC-4109 | fixed (`.5`) |
| QA-5 (F-5) | qa-reviewer | minor | CR-5 / D-4 | nobody owned the two BACKLOG edits | LLR-4105.4 (inspection) | fixed (`.6`) |
| QA-6 (F-6) | qa-reviewer | minor | negative controls | mutant controls are plans | §5.1 says they run in the P3 battery | fixed |
| QA-7 (F-7) | qa-reviewer | minor | D-2 | Windows NUL exits 1 | README exit-codes text says so (D-7) | fixed |
| QA-8 (F-8) | qa-reviewer | minor | TC-4107 | the oracle is in-process, not the app handler | declared in §6.3 | accepted |
| SEC-1 (F1) | security-reviewer | medium | LLR-4104.2 | `Registry.load`, `people.Directory.load`, `marks.Directory.load` copy unreadable files aside | non-copying readers; corrupt-files arm | fixed (`.1`) |
| SEC-2 (F2) | security-reviewer | medium | LLR-4104.3 | project names, answers and errors printed raw; collapsing spaces corrupts stdout paths | one print function; stdout paths unchanged | fixed (`.2`) |
| SEC-3 (F3) | security-reviewer | medium | LLR-4102.5 | binary or closed stdin, unbounded line | new LLR, TC-4110 | fixed (`.3`) |
| SEC-4 (F4) | security-reviewer | medium | LLR-4102.4 | `a` named no folder | stderr notice before writing; README warning | fixed (`.4`) |
| SEC-5 (F5) | security-reviewer | low | LLR-4104.1 | `--board ''` fell through | `is not None`, refuse | fixed (`.4`) |
| SEC-6/7/8 (F6-F8) | security-reviewer | low | symlinked `reports/`, empty slug, check-then-read | equal to `H`; no separator in a slug; `peek_board` seeds nothing | accepted, §6.3 |
| SEC-N1 | security-reviewer | low | §6.3 | a stale sentence said whitespace collapsed | rewritten | fixed |
| SEC-N2 | security-reviewer | low | Phase 3 | each `_read` raises OSError on a missing file | guard in `_read_registry` / `_read_directory` | carried into increment 001 |

### shall / should check
No `should` / `debería` inside any HLR or LLR statement (qa-reviewer's grep; the author's re-read after the amendments).

### Two-layer acceptance review (blockers)

| Story / Req | (a) AT present | (b) deliverable+method named | (c) both chains | (d) black-box pure | Status |
|-------------|----------------|------------------------------|-----------------|--------------------|--------|
| US-4101 | yes (AT-4101..AT-4107) | yes (files, stdout paths, stderr, exit code, embedded data) | yes | yes | ✓ |

### Supersession census (change-first)
Planned edits: `taskboard/__main__.py`, `README.md`, `tests/test_report.py` (two functions), `tests/test_report_cli.py` (new), `.dev-flow/BACKLOG.md`. Families run: file path / module structure / import graph (`grep -rl "taskboard.__main__\|entry.main\|--report" tests/`, `evidence/reverse-census.txt`: 24 files import `__main__`, almost all only `open_app`, which is unchanged); golden (none, `tests/goldens/` absent); README-vs-code pin (`tests/test_readme.py::test_TC_120…` requires each argparse flag as «`taskboard --flag» in the README, so the README row for `--report-kind` is owed); `--open … --report` refusal (`tests/test_boards_backlog_round.py::test_TC_2410…` stays valid: the `--open` refusal runs before the report branch). Reservations: best-effort + gate-confirmed — the increment gate and the P4 full suite are the completeness guarantee.

### Security review summary
`security-reviewer` (spawned as a generic agent with `agents/security-reviewer.md`, default model) reviewed the contract twice: first pass `iterate-to-refine` (0 HIGH, 4 MEDIUM, 4 LOW); after the amendments, second pass: F1-F5 closed, F6-F8 accepted, one stale sentence (SEC-N1, fixed) and one Phase-3 note (SEC-N2). A third pass over the CODE is owed at Phase 3 (scope-change re-routing).

### Evidence checklists
- qa-reviewer: mode plan; expected values explicit; edge classes covered after QA-2/QA-3; no real PII; surface reachability ✓.
- security-reviewer: each finding has what, where, why, recommendation; severities; no secret values; explicit verdict; no new external tools.
