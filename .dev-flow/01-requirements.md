# Requirements Document — taskboard — Batch 2026-07-18-batch-01

> **Artifact language**
> This template is the canonical **English scaffold**. Generate the artifact in the batch's development language (`state.json` `language`). For Spanish batches, translate the section headers and guidance and use `deberá` as the normative keyword (≡ `shall`). The normative RULES in this preamble are **language-independent** and enforced regardless of artifact language.

> **Strict normative convention — IEEE 830 + EARS**
> - `shall` / `deberá` = normative, binding, verifiable requirement. **Only** inside HLR / LLR statements.
> - `should` / `debería` = informative / explanatory text, **NOT binding**. **Only** outside HLR / LLR statements (rationale, description, context).
> - Any modal `should` / `debería` inside an HLR / LLR statement is a **writing error** and will be flagged as a blocker in phase 2.
> - `may` = optional. `will` = future declaration or fact about an external actor.

> **Verifiability rule — captured at draft, not at phase-2 gate**
> (Root cause of the batch-02 + batch-03 post-mortems: both batches forced a phase-1 iteration for the same reason — `test`/`analysis` validation labels without a named executed verification and a numeric pass threshold. The corrective action is baked into the template.)
>
> Every requirement labelled `test` or `analysis` **must** carry TWO fields on its line:
> - **Executed verification:** what EXACTLY runs / is inspected (e.g. `npm run typecheck`, `vitest run path/to/file.test.ts -t TC-001`, `signature-diff inspection vs main`). Without this the method is not executable.
> - **Numeric pass threshold:** the quantitative pass criterion (e.g. `0 errors`, `peak post-limiter ≤ −6 dBFS`, `RMS error < 0.01`, `LLR coverage ≥ 100 %`). Without this the result is not objective.
>
> For `demo` (perceptual): describe the observable procedure + the named qualitative criterion.
> For `inspection` (structural): name the file / commit / section to inspect + the observable condition.
>
> **Any `test`/`analysis` LLR missing these two fields is a phase-2 blocker.**

> **Parent-HLR re-read rule — captured at the Phase-1 reconciliation gate**
> (Root cause of the batch-06 A-B1 + batch-07 A-03 + batch-08 A-01-cluster post-mortems: THREE consecutive batches relaxed an LLR threshold or claimed a promotion during reconciliation without propagating the change up to the parent HLR / into the LLR body, leaving §6.4 asserting things the §3/§4 body didn't reflect. Adding this rule as prose at batch-07 closeout did NOT prevent the batch-08 recurrence — because a rule that says "re-read" with no required output silently degrades to "I thought about it." The corrective action is to mandate an ARTIFACT, not a process step.)
>
> **Any time an LLR's `Numeric pass threshold` or `Statement` changes at the Phase-1 reconciliation gate — or an LLR is added/promoted/removed — the §6.4 reconciliation log MUST contain a per-decision audit table** with one row per changed decision and these columns: `Decision ID | What changed | Parent HLR re-read? (which HLR + what changed there, or "no change required" + why) | Body edit landed? (the §3/§4 line that now reflects it)`.
>
> **Body-first ordering is mandatory:** write the §3/§4 HLR/LLR body edit FIRST, then write the §6.4 audit row that points at it. Never write a §6.4 claim before the body line it describes exists. This eliminates the "claimed but missing" failure mode that recurred in batch-06/07/08.
>
> **Two phase-2 blockers enforce this:** (a) any HLR threshold contradicting its decomposed LLRs; (b) any §6.4 audit row whose "Body edit landed?" column points at a §3/§4 line that does not exist (a reviewer greps for it). Both are mechanically checkable.

> **Testing-strategy-vs-ADR rule — captured at draft, not at phase-3 boundary**
> (Root cause of the batch-06 F-6 / Phase-3 infrastructure correction: every `test (...)` label was labelled against a testing stack — JSDOM + Testing Library — that didn't exist in the repo and was explicitly rejected by ADR-0002. The software-dev agent correctly stopped at the boundary, but the gap should be caught in Phase 1.)
>
> **Every `test (...)` validation label MUST be cross-checked against the project's testing-strategy ADR and the actual `package.json` / `requirements.txt`** before locking the LLR. If the labelled runtime isn't installed and isn't the strategy-ratified path, that's a phase-2 blocker.

> **LLR symbol-citation rule — captured at draft, not at the phase-3 boundary**
> (Root cause of the batch-05 F-A-01 blocker + three Phase-3 doc deviations: LLRs named specific private fields/methods — `_alt_hex_window_start`, `_mac_hex_window_start`, `_on_mac_records_row_highlighted`, `current_file.sorted_ranges` — and a layout constant (`width: 78`) that were inferred from plausible symmetry, NOT from observed code. The fabricated paging fields were caught by the independent Phase-2 re-review before any code was written; the other three survived to Phase 3 and surfaced only at implementation time. The common failure mode is "named a symbol that looks like it should exist." A rule that says "verify" with no required artifact silently degrades to "I assumed," so this mandates a CITATION, not a process step.)
>
> **Any LLR (or its Acceptance criteria / Executed verification) that names a concrete code symbol — a private field, method, function, class, or widget id — MUST cite a grep-verified `file:line` for that symbol at draft time.** If the symbol does not yet exist (it will be created by the increment), it MUST be explicitly flagged `NEW — created in Phase 3` so the reviewer does not expect to find it. Layout-geometry / magic-number constants (pane widths, row counts, byte offsets) MUST either cite a measured value with the measurement method, or be flagged `assumed — verify in Phase 3`.
>
> **Two phase-2 blockers enforce this:** (a) any LLR that names a symbol without a `file:line` citation and without a `NEW` flag (a reviewer greps for the symbol; if it neither exists nor is flagged NEW, block); (b) any layout/magic-number constant asserted as fact without a measurement citation or an `assumed` flag. Both are mechanically checkable by grep.

> **Environmental-measurement citation rule — extends the LLR symbol-citation rule.** Any constant describing the runtime or layout **environment** — container/parent widths, derived geometry (e.g. `body_w`, pane shares), responsive breakpoints and transition points, timing/latency budgets, platform or CI environment values — MUST cite, at draft time: **(a) WHERE it was measured** (the probe or test `file:line`, or the exact `App.run_test(size=...)` / command invocation), **AND (b) the REGIME/CONDITIONS under which the measurement holds** (terminal-size band, CSS class state, rail/panel visibility, platform, dataset size). A measurement applied **outside its measured regime** MUST be re-measured in that regime or flagged `assumed — verify per-regime`. **Derived numbers inherit the flag**: any cell count, threshold, or transition point computed from an environmental constant is not a fact until the underlying measurement is regime-valid, and must cite the constant it derives from. **Phase-2 blocker classes:** (a) an environmental constant asserted as fact whose citation lacks its measurement conditions; (b) a constant or its derivatives applied in a regime other than the one cited. (Origin: batch-06 B-1.)

> **Probe self-test rule — captured from batch-07 B-3/B-4.** Any executable verification artifact written into an HLR/LLR — a grep/rg probe, a regex, a pytest node id, a determinism/equality procedure, an inspection command — MUST be EXECUTED at draft time against the current tree, with its **expected pre-state result recorded next to the spec** (e.g. "probe run 2026-06-10: 164 hits pre-retirement; pass condition = 0 post"). A probe that cannot demonstrate a non-trivial pre-state — hits today for a future-absence check, a failing-then-passing pair for a behavioral check, both sides exercised for an equality — is unproven and shall be flagged `unexecuted — verify in Phase 2`. **Phase-2 blocker classes:** (a) a verification command recorded without executed pre-state evidence; (b) a verification whose pre-state execution contradicts its claimed semantics. (Origin: batch-07 B-3 — a BRE grep returning 0 on a tree known to contain 164 hits — and B-4 — a double-apply equality no correct implementation could satisfy.)

> **Contract-touch rule — captured from batch-07 B-1/B-2.** A cross-cutting interface contract (canonical field set, producer/consumer table) is reconciled at merge but **invalidated by any subsequent edit to any LLR it cites** — including gate-decision insertions, which are the most likely to add fields and the least likely to be reconciled. Any post-draft edit touching a producer or consumer LLR re-opens the contract as a mandatory checklist row: the editor shall re-run the identity check (field-set equality across every producer and consumer enumeration) and record the re-run in that edit's audit-table row. An edit that adds a field to one side without the recorded re-run is a Phase-2 blocker. (Origin: batch-07 B-1/B-2 — LLR-002.7/002.8 added `saved_path`/`issues` hours after the C-6 contract was drafted.)

> **AC-artifact citation rule — extends the LLR symbol-citation rule.** Any data artifact named in an HLR/LLR **Acceptance criteria** line — a test fixture, example file, directory, or data path — is citation surface, same as a code symbol: it MUST carry either an EXECUTED existence probe recorded at draft time (e.g. `Glob examples/**/*.hex → N files, <date>`) or an explicit `NEW — created in Phase 3` flag with the artifact counted in the increment file budget. **Phase-2 blocker:** an AC-named artifact with neither an executed existence probe nor a NEW flag. (Origin: batch-08 B-1 — an acceptance criterion demanded "a real `.hex` example from `examples/`" on a tree measured to contain zero `.hex` files; found independently by two reviewers because the rule's wording covered only symbols.)

> **Probe-regime rule — extends the probe self-test rule.** A probe's positive control MUST exercise the same syntactic/structural REGIME as the protected targets (import depth, package level, file class, CSS state, platform), and the ledger entry MUST state that regime next to the recorded execution. If the target does not exist yet, the control runs on a synthetic in-regime fixture created at the exact target location/depth and deleted after (the batch-08 `_b2_scratch` pattern: scratch package at target depth → probe hits all violation forms → negative control on a known-legitimate module → scratch removed). An out-of-regime control does not discharge the probe self-test rule — it is recorded `superseded-pending` until an in-regime control exists. **Phase-2 blocker classes:** (a) a probe whose positive control's regime differs from the target regime; (b) a ledger entry that omits the control's regime. (Origin: batch-08 B-2 — a reverse-import probe whose executed control ran at single-dot import depth while the protected targets lived one package level deeper, where the natural violation form was two-dot relative and escaped the regex on the SOLE verification of its LLR.)

> **Supersession-census-completeness rule — captured from batch-09 Lesson 1, reframed at batch-10.** When a batch supersedes scaffold/placeholder behavior OR adds/moves a module OR edits an existing file, the Phase-1 supersession census MUST account for ALL guard families that the change can break, not only the named behavioral-placeholder one: (a) **behavioral-placeholder guards** — deferral/placeholder/"not-yet" assertions; (b) **structural / placement / allowlist guards** — package-shape invariants (e.g. `rg -n 'glob\(.\*\.py.\)|listdir|iterdir|allowlist|_root_modules' tests/`); (c) **AST-composition guards** (e.g. `rg -n 'ast\.|\.body|calls\s*<=' tests/`); (d) **engine-frozen / no-diff-vs-main guards** (e.g. `rg -n '_ENGINE_PATHS|no_diff_vs_main|engine_modules_unchanged' tests/`). The predicted-red set is incomplete until all run; any guard whose invariant the change violates is added with its disposition at Phase 1, not discovered at the increment gate. (Origin: batch-09 — two package-root placement guards escaped a placeholder-only census; batch-10 — a 4th family, the engine-frozen guards that git-freeze `core.py`/`hexfile.py`/`range_index.py`/`validation/`/`tui/a2l.py`/`tui/mac.py`/`tui/color_policy.py`, was MISSED even after the b09 widening and broke the emitter's `hexfile.py` placement at the I1 gate, forcing the R2 relocation to `tui/changes/io.py`.)

> **Census = completeness PRINCIPLE, not a grep checklist (A-1, batch-10).** The family list above is a starting set, NOT an exhaustive enumeration — "grep these N patterns" is structurally blind to any guard whose pattern isn't listed. The census MUST be run **change-first**: take the batch's planned new/moved/edited file list and, for EACH file, check it against EVERY test that asserts on a file PATH / module STRUCTURE / import GRAPH / git-DIFF (key on the CATEGORY of assertion, not the specific pattern). A guard that fires on a planned file is a Phase-1 finding, before code. **Corollary — new-symbol-into-existing-file probe (A-3):** any LLR adding a NEW symbol to an EXISTING module MUST cite a draft-time probe proving that file is not frozen/allowlisted against the edit. (Origin: batch-10 — the emitter into the frozen `hexfile.py`.)

> **Ban the "VERIFIED COMPLETE" census stamp (A-2, batch-10).** A census/completeness claim MUST NOT be stamped "VERIFIED COMPLETE" by re-running the known families — re-running an incomplete checklist cannot detect that the checklist is incomplete. A completeness verdict must EITHER show why no (N+1)th family exists (the enumeration of the whole structural-guard surface), OR be downgraded to "best-effort + gate-confirmed." **The increment GATE — running the actual moved/edited file against the real suite — is the completeness guarantee; the census is a Phase-1 cost-reduction heuristic that catches it cheaply, not a proof.** (Origin: batch-10 — Phase-2 certified the census "VERIFIED COMPLETE (re-ran all 3 grep families)"; "all 3" was the bug, and the 4th family broke at the I1 gate.)

> **Phase-4 supersession-completeness inspection (V-3, batch-09).** The Phase-4 validation matrix MUST include a row that greps the WHOLE class of superseded placeholder constants/markers and asserts every surviving reference is a NEGATIVE assertion (absence), not a live dependency — e.g. confirm the only surviving `#diff_deferral_notice` reference is `not bool(...)` and the removed constants survive solely inside a "they're gone" guard. A by-hand confirmation is insufficient; promote it to a standing matrix row.

> **Provisional-identifier scope rule (V-5, batch-09).** The `provisional until Phase 3` flag (batch-08 A-3) covers EVERY implementer-owned identifier in an Executed-verification line — the test FILE path AND the `-k` selector AND the pytest node id — not only node ids. A pinned-but-wrong file name or `-k` token produces a false "test missing" signal at the validation gate exactly as a pinned node id does. Spec convention: "Executed-verification file paths, `-k` selectors, and node ids are all provisional-until-Phase-3; the implemented names are reconciled from the real tree at Phase 4." (Origin: batch-09 DEV-1 — the spec pinned `tests/test_diff_report.py`; the implementer chose `test_diff_report_service.py`, producing a Phase-6 rename-reconciliation chore.)

> **Purity-probe form rule (V-4, batch-09).** An import-purity probe MUST match import statements, not the bare token — use `rg -n "import <pkg>|from <pkg>|<Pkg>"`, never substring `rg -c "<pkg>"` (which matches the word in docstrings/prose and yields a benign-but-noisy false positive that must then be hand-resolved). (Origin: batch-09 DEV-5 — `rg -c "textual"` matched the word "textual" in a module docstring.)

> **Story-dimension coverage / surface-reachability rule (A-5, batch-11).** Coverage must reach the SHIPPED surface, not only a service's direct API. (a) For each input dimension named in a source user story, ≥1 TC MUST exercise it through the shipped surface (the handler/UI call-site), not only via direct service kwargs. (b) When a handler wires a writer/service that accepts dimensions the handler defaults empty, decompose a COMPOSITION LLR for that wiring or record the dimension out-of-scope explicitly. (c) Phase-4 carries a standing surface-reachability matrix row: handler call-site kwargs vs service signature vs story dimensions. (Origin: batch-11 SCOPE-1 — a manifest writer fully tested via direct kwargs while the save handler passed empty batch/assignments, so the shipped artifact carried only `active_variant`; 23/23 TCs + full suite passed because coverage was keyed on the writer's API, not the user's story.)

> **Two-layer validation rule — black-box behavioral acceptance + white-box functional (headline, non-negotiable).** A user story is a user-verified OUTCOME / observable behavior (the WHAT), validated black-box through the shipped surface; HLR/LLR are the internal workings (the HOW), validated white-box by functional TCs. **No story is "done" until a black-box test (`AT-NNN`) observes its user-verified outcome through the shipped surface, with boundary + negative evidence — independent of the white-box `TC-NNN` that validate the HLR/LLR mechanism. A green white-box suite that never observes the behavior is not acceptance.** Every output-producing requirement MUST name its concrete deliverable and how it is observed (file at path + non-empty + required content; or rendered screen element). **Dual traceability is mandatory** (§5.2): behavioral `US → AT-NNN → observed outcome` AND functional `US → HLR → LLR → TC-NNN`; a requirement with only one chain is incomplete. Layer B is the `test (pilot)` / e2e / artifact-on-disk idiom (automated), **not `demo`**; `AT-NNN` ids are provisional-until-Phase-3 per the **Provisional-identifier scope rule (V-5)** and reconciled at Phase 4. **Phase-2 blocker classes:** (a) a story with no `AT`; (b) an output-producing requirement that doesn't name its observable deliverable + observation method; (c) an incomplete traceability chain (either side); (d) an "acceptance" test that references an internal symbol (not genuinely black-box). (Origin: a project-report story whose white-box TCs — `test_full_report_content`, builders, window math — passed green while the report was never produced as a user-facing output; batch-14.)
>
> **State-lifetime provenance rule (batch-24).** When a story CONSUMES state captured earlier by another flow (a retained summary, a cached result, a stamped path), the spec MUST state that state's LIFETIME story — who writes it, what invalidates/clears it, what happens if the world changed since capture (file reloaded, project switched) — and bind consumption to provenance (a recorded link to what the state was derived FROM, refused on mismatch). A consume-only story gets no new-write-surface security pass by default, so this is the spec-layer net. (Origin: batch-24 B-2 — `last_summary` survived project switches with no source-image field; the specced before/after report would pair project B's file with project A's patch, and every then-specced AT passed over it. Fix: `source_image_path` stamp + refusal class + a cross-project refusal AT.)

---

## 1. Introduction

### 1.1 Purpose
This document specifies the requirements for **batch 2026-07-18-batch-01** of the `taskboard` tool — a frameless Textual TUI kanban desktop-widget. The batch delivers three user-facing changes: (1) replace the author-revealing demo seed with a neutral, capability-showcasing seed; (2) let a task hold **multiple URLs**; (3) let a task hold **image references**. It is written to the IEEE-830 + EARS convention with the two-layer (black-box acceptance / white-box functional) validation model mandated by the template preamble.

### 1.2 Scope
**In scope.** Model changes to `Task` (multi-URL list + image-ref list, with back-compat migration of the legacy single `url`); the add/edit task modal input surface for both; the card indicators and the open actions; a rewritten `seed_data()` demo dataset that both hides author identity and exercises every board feature dimension including the two new ones.

**Out of scope (explicit).**
- Inline in-terminal image rendering as a *core guarantee*. It is specified only as an OPTIONAL/stretch LLR (LLR-007.4) that degrades to open-in-viewer; the batch does not promise inline preview (see §2.4, Constraint C-5).
- Project-status edit binding and the wezterm paste-binding sync (parked in `PLAN.md` out-of-scope carries).
- Any change to the four view renderers beyond adding the two new indicators.
- Deleting/renaming the legacy `url` JSON key semantics beyond a one-way forward migration (§6.2, DD-2).

### 1.3 Definitions, acronyms, abbreviations
| Term | Definition |
|------|------------|
| Standalone task | A task with `project_id is None`; rendered in the "Inbox" group (`models.py:325`, `views.py:325`). |
| Urgency bucket | overdue / today / week / later / none / done, computed by `urgency()` at `views.py:195-208`. |
| Indicator glyph | A right-aligned width-1 marker on a card cell (`↗` URL, `◉` priority) — `card_cell` `views.py:142-161`. |
| OSC-8 link | Terminal hyperlink escape emitted by `[link=…]` markup around a title — `title_markup` `views.py:117-118`. |
| Open action | The `o`-bound `action_open_url` that opens a task's URL in the OS browser — `app.py:48`, `app.py:252-255`. |
| Denylist | Regex of author-identifying tokens the new seed must not contain (§3, HLR-001 / AT-001). |
| DoR | Definition of Ready (INVEST) — Phase-0 gate before a story becomes HLR. |
| AT / TC | Black-box acceptance test / white-box functional test-case ids. |

### 1.4 References
- Source stories & batch context: `.dev-flow/state.json`, `.dev-flow/PLAN.md`.
- Code under change: `taskboard/models.py`, `taskboard/modals.py`, `taskboard/views.py`, `taskboard/app.py`.
- Test conventions: `tests/test_app.py` (pytest 9.1.1 + pytest-asyncio 1.4.0, `asyncio_mode = "auto"` — `pyproject.toml:24-25`).
- Template library section 1 (Arquitectura / requirements) — GRNDIA project OS.

### 1.5 Document overview
§2 overall description + constraints + Phase-0 DoR for the three stories. §3 HLR (EARS, one per capability slice) with black-box Acceptance blocks. §4 LLR decomposition with symbol citations. §5 the two-layer validation strategy + dual-traceability tables. §6 appendices: design decisions, risks, reconciliation log, evidence checklist.

---

## 2. Overall description

### 2.1 Product perspective
`taskboard` is a single-process Textual desktop widget persisting to one JSON file at `~/.taskboard/board.json` (`models.py:136-142`). The `Board` class owns `projects` + `tasks` and round-trips them via `asdict` / `from_dict` (`models.py:209-245`). A missing file is seeded from `seed_data()` (`models.py:220-224`, `311-347`); a corrupt file starts empty and is never overwritten (`models.py:234-236`). This batch touches the model dataclasses, the seed, the task modal, two renderers' indicator logic, and one/two app actions — no architectural change.

### 2.2 Product functions
1. A neutral demo seed that reveals nothing about the author yet exercises every feature dimension (standalone/project, all project & task statuses, all priorities, all urgency buckets, archived items, URLs, multiple URLs, images).
2. A task holding an ordered list of URLs, editable in the modal, indicated on the card, all opened by the open action.
3. A task holding an ordered list of image references (local paths and/or image URLs), editable in the modal, indicated on the card, opened in the OS default viewer; inline preview only as a graceful-degrading stretch.

### 2.3 User characteristics
- **Repo cloner / evaluator** (US-1 role): runs the public app for the first time, sees the seeded board. Must not infer anything about the author.
- **End user** (US-2, US-3 roles): a single local user managing their own tasks via keyboard; trusts their own `board.json` content.

### 2.4 Constraints
- **C-1 — Textual 8.2.8 pinned** (`requirements.txt:3`). `TextArea` is available in this version (verified: `from textual.widgets import TextArea` imports OK, 2026-07-18). Any multi-line input widget choice is bounded by this.
- **C-2 — width-1 glyphs only.** All indicator glyphs must be single-cell to preserve box-art alignment across monospace fonts (the "M22 ambiguous-glyph trap", `views.py:6-11`). The image indicator glyph inherits this.
- **C-3 — markup-injection safety.** All untrusted text is escaped with `rich.markup.escape` before entering markup (`views.py:8-10`, `views.py:114-118`); URLs additionally pass `valid_url` which rejects `[`, `]`, whitespace, newlines (`views.py:97-105`) — the OSC-8 link-injection guard. New URL/image surfaces must preserve this.
- **C-4 — lenient edges.** The model validates leniently and never raises on load (`from_dict` at `models.py:194-206`, `parse_iso` at `models.py:149-156`). New list fields must degrade gracefully on malformed JSON, not raise.
- **C-5 — terminal graphics are not guaranteed.** Inline image rendering needs a terminal graphics protocol (Kitty/iTerm/Sixel) that is terminal-dependent and cannot be verified headlessly (`App.run_test()` has no real terminal). WezTerm (the packaged config, `wezterm.lua`) supports Kitty/iTerm, but this cannot be asserted in CI. Therefore inline preview is OPTIONAL/stretch only.
- **C-6 — os.startfile is Windows-only + is an external-action surface.** `os.startfile(path)` opens a path with its OS-associated handler; for a non-image file (e.g. `.exe`/`.bat`) that means *execution*. Opening image refs must be constrained to an image-extension allowlist (LLR-007.3) and reviewed by `security-reviewer` before sign-off.

### 2.5 Assumptions and dependencies
- **A-1.** The board JSON is user-owned and locally authored; image/URL refs are the user's own strings (single-user trust boundary). US-3's write surface still gets the allowlist net (C-6) because `os.startfile` can execute.
- **A-2.** `webbrowser.open` (already imported, `app.py:5`) is the cross-platform opener for `http(s)` refs; `os.startfile` is the Windows local-file opener. Non-Windows local-file opening is out of scope for this batch (documented limitation, DD-4) — the app is described as a "desktop widget" and the packaged terminal is WezTerm on Windows.
- **A-3.** Existing 28 tests in `tests/test_app.py` stay green; `test_url_task_open_action` (`tests/test_app.py:382-391`) and `test_url_renders_link_and_arrow` (`tests/test_app.py:394-398`) will need updating because they read the old singular `task.url` — flagged as a migration touch, not a regression.

---

### 2.6 Source user stories

> Connextra format: **"As a `<role>`, I want `<goal>`, so that `<benefit>`"**. Each US gets a unique ID `US-NNN` and must be traceable to one or more HLRs.
> **Phase 0 — Definition of Ready (INVEST):** every story is refined and classified before it can be derived into HLR (Phase 1). Only `READY` stories proceed.

| ID | User Story | Source | DoR status |
|----|------------|--------|------------|
| US-001 | As anyone cloning the public repo, I want the built-in demo data to showcase every feature **without revealing anything about the tool's author**, so that I can evaluate the app on its merits and the author's identity stays private. | `state.json` batch_objective; `PLAN.md` US-1 | **READY** |
| US-002 | As a user, I want a task to hold **more than one URL**, so that I can attach several links to one task and open them from the board. | `state.json` batch_objective; `PLAN.md` US-2 | **READY** |
| US-003 | As a user, I want a task to hold **image references** (screenshots/mockups), so that I can attach and open images tied to a task. | `state.json` batch_objective; `PLAN.md` US-3 | **READY** |

#### Refinement log (one block per story)

**US-001 — Generic capability-showcase seed**
- **INVEST:** I ✓ · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality (V, N):** user = repo cloner/evaluator · outcome = the seeded board reveals no author identity yet exercises every feature dimension · why = public repo hygiene + a self-demonstrating demo · out of scope = changing any renderer behavior; changing which dimensions exist.
- **Feasibility (E, S):** implementation path = rewrite `seed_data()` (`models.py:311-347`) only · dependencies = the model's enums (`PROJECT_STATUSES` `models.py:19`, `TASK_STATUSES` `models.py:20`, `TASK_PRIORITIES` `models.py:21`) + the two NEW list fields from US-2/US-3 · fits one batch = yes.
- **Evaluability (T) — behavioral, black-box:** "When the app is first run on a machine with no `board.json`, the user observes a seeded board whose serialized content matches **zero** author-denylist tokens AND contains at least one item in **every** feature dimension (all 4 project statuses incl. `cancelled`, all 4 task statuses, all 3 priorities, all urgency buckets, ≥1 archived project, ≥1 archived task, standalone + project tasks, ≥1 task with ≥2 URLs, ≥1 task with ≥1 image)." → AT-001.
- **Open questions (closed with assumptions):**
  - Q: Is the framework word "Textual" itself forbidden? → **A (assumption):** yes inside seed *content* (project/task titles, URLs) because "Textual" was the author's course; the app may still be *built with* Textual elsewhere. Denylist targets seed strings only.
  - Q: Which exact denylist tokens? → **A:** the executed set below (author's real projects/artifacts), case-insensitive.
- **Classification:** `READY`.

**US-002 — Multiple URLs per task**
- **INVEST:** I ✓ · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality (V, N):** user = end user · outcome = a task stores/edits/opens several URLs · why = one task often has multiple relevant links · out of scope = per-URL labels/titles; a rich link manager.
- **Feasibility (E, S):** path = `Task.url:str` → `Task.urls:list[str]` with `from_dict` migration (`models.py:190`, `204`); modal multi-line entry (`modals.py:66-68`, `96`); card indicator (`views.py:154`, `108-121`); open action (`app.py:252-255`) · fits one batch = yes.
- **Evaluability (T) — behavioral, black-box:** "When the user edits a task and enters 3 URLs, the user observes the ↗ indicator on that task's card, and pressing `o` opens all 3 URLs." → AT-002.
- **Open questions (closed with assumptions):**
  - Q: >1 URL open behavior — chooser or open-all? → **A (assumption, simple>clever):** **open-all** (each valid URL via `webbrowser.open`). Deterministic, no new UI, testable headlessly. Recorded as DD-3.
  - Q: Show a count on the indicator? → **A:** OPTIONAL (LLR-004.1 acceptance allows `↗` or `↗n`); the binding requirement is only that ≥1 URL shows the indicator.
  - Q: Modal entry format? → **A (assumption):** a `TextArea`, **one URL per line** (Constraint C-1 confirms `TextArea` exists in 8.2.8). Flagged for Phase-3 confirmation of exact widget id.
- **Classification:** `READY`.

**US-003 — Images per task**
- **INVEST:** I ✓ · N ✓ · V ✓ · E ✓ · S ✓ · T ✓ (E/S bounded by C-5; core is feasible, preview is the stretch)
- **Functionality (V, N):** user = end user · outcome = a task stores/edits/opens image refs · why = attach screenshots/mockups · out of scope (core) = guaranteed inline in-terminal rendering (C-5).
- **Feasibility (E, S):** path = NEW `Task.images:list[str]` (no migration needed — new field); modal multi-line entry; NEW width-1 card glyph; NEW open-image action (`os.startfile` for local image-ext paths / `webbrowser.open` for http(s)) · fits one batch = yes for the core; inline preview flagged stretch.
- **Evaluability (T) — behavioral, black-box:** "When the user attaches 1 image path (image extension) + 1 image URL to a task, the user observes the image indicator on the card, and the open-image action opens both in the OS viewer/browser; a non-image local path is refused." → AT-003.
- **Open questions (closed with assumptions):**
  - Q: Inline preview promised? → **A (KEY ASSUMPTION):** **No.** Core = store + open-in-viewer. Inline preview = optional LLR-007.4 flagged `assumed — verify terminal-graphics support at Phase 3`, degrading to open-in-viewer. This is the central US-3 design constraint (C-5).
  - Q: Open binding — reuse `o` or new key? → **A (assumption):** a **separate** open-image action/binding (proposed key `i`), so URL-open and image-open stay independently testable. Exact key flagged for Phase-3 (`NEW` binding).
  - Q: Security of `os.startfile`? → **A:** image-extension allowlist before `os.startfile` (C-6, LLR-007.3); `security-reviewer` loop before sign-off.
- **Classification:** `READY`.

---

## 3. High-level requirements (HLR)

> EARS patterns; normative `shall` only. Every HLR traces to a US and carries a black-box Acceptance block.

### HLR-001 — Author-neutral, dimension-complete demo seed
- **Traceability:** US-001
- **Statement:** When the application is first run without an existing board file, the system **shall** seed a demo board whose serialized content contains **no** author-identifying token from the denylist AND contains **at least one** item in every feature dimension enumerated in LLR-001.1…001.6.
- **Rationale (informative):** the public repo must not leak the author's projects; the demo must also self-demonstrate the whole tool. The current seed does neither fully — it names GRNDIA/Textual/Job Hunt and (measured) omits the `cancelled` project status and all archived items.
- **Validation:** `test`
- **Executed verification:** `pytest tests/test_app.py -k seed_generic_complete` (node id provisional-until-Phase-3) — asserts denylist match count + per-dimension presence over `Board.load(fresh_path)`.
- **Numeric pass threshold:** denylist matches over serialized seed `== 0`; project-status coverage `== 4/4`; task-status `== 4/4`; priority `== 3/3`; urgency buckets `⊇ {overdue, today, later|week, none}`; archived projects `≥ 1`; archived tasks `≥ 1`; tasks with `len(urls) ≥ 2` `≥ 1`; tasks with `len(images) ≥ 1` `≥ 1`.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** a freshly seeded board that a reviewer can grep and find no author token, and can enumerate every feature dimension in.
  - **Shipped surface:** `Board.load()` on a non-existent path → `seed_data()` (`models.py:220-224`, `311-347`); the persisted `~/.taskboard/board.json`.
  - **Deliverable + observation:** the seeded, on-disk `board.json` (and the in-memory `Board`) — observed by serializing it and asserting the denylist regex yields `0` matches and every dimension set is populated.
  - **Acceptance test(s):** `AT-001` (drives `Board.load(tmp_path)`, asserts denylist == 0 + all dimension thresholds; FAILS if any author token survives or any dimension is empty).
  - **Boundary catalog (QC-3):** ☑ empty (fresh/no-file path → seed fires) ☑ boundary (exactly-one item satisfies each `≥1` dimension) ☑ invalid (denylist is the "must-not-contain" negative class) ☑ error (corrupt-file path must still start empty, not reseed — regression guard `tests/test_app.py:434-439`).

### HLR-002 — Task holds an ordered list of URLs (with legacy migration)
- **Traceability:** US-002
- **Statement:** The `Task` model **shall** store an ordered list of URL strings, and on load **shall** migrate a legacy single `url` string into a one-element list without data loss.
- **Rationale (informative):** the model is the single source of truth for both the card indicator and the open action; migration preserves existing boards created with the singular `url` (`models.py:190`).
- **Validation:** `test`
- **Executed verification:** `pytest tests/test_app.py -k task_urls_model_migration` (provisional) — constructs `Task.from_dict` from legacy `{"url": "https://x"}` and modern `{"urls": [..]}` and round-trips through `save`/`load`.
- **Numeric pass threshold:** legacy `{"url":"https://x"}` → `urls == ["https://x"]`; modern `{"urls":[a,b]}` → `urls == [a,b]`; save→load round-trip equality `== True`; `0` exceptions on malformed input.
- **Priority:** high
- **Acceptance (black-box):**
  - **Observable outcome:** an old board file opens with its single link preserved as a one-item list; a new board persists multiple links.
  - **Shipped surface:** `Board.load` / `Board.save` (`models.py:220-245`), `Task.from_dict` (`models.py:194-206`).
  - **Deliverable + observation:** the reloaded `Board.tasks[*].urls` list — observed by writing a legacy JSON to disk, loading, asserting the list.
  - **Acceptance test(s):** `AT-002` (shared with the modal/open surface; the migration leg asserts a hand-written legacy `board.json` loads with `urls == ["…"]`).
  - **Boundary catalog (QC-3):** ☑ empty (no `url` and no `urls` → `urls == []`) ☑ boundary (1 URL) ☑ invalid (`url: null` / non-list `urls` → `[]`, no raise) ☑ error (corrupt file → empty board, unchanged behavior).

### HLR-003 — Task modal edits multiple URLs
- **Traceability:** US-002
- **Statement:** When the user opens the add/edit task modal, the system **shall** present all of the task's URLs for editing and, on save, **shall** return the entered URLs as an ordered list of valid `http(s)` URLs (blanks and invalid entries removed).
- **Rationale (informative):** the modal is the only write path for task fields (`app.py:200-224`); it must accept more than the current single `#f-url` Input (`modals.py:66-68`).
- **Validation:** `test`
- **Executed verification:** `pytest tests/test_app.py -k modal_multi_url` (provisional) — Pilot presses `a`, sets the multi-URL widget to 3 lines (1 invalid), saves, asserts the created task's `urls`.
- **Numeric pass threshold:** 3 input lines with 1 non-`http` line → saved `urls` length `== 2`, order preserved; empty widget → `urls == []`.
- **Priority:** high
- **Acceptance (black-box):**
  - **Observable outcome:** the user types several URLs in the modal and the saved task carries exactly the valid ones, in order.
  - **Shipped surface:** `TaskModal` (`modals.py:28-98`); `action_add_task`/`action_edit` handlers (`app.py:200-224`).
  - **Deliverable + observation:** the created/edited `Task.urls` — observed via Pilot after `save_open_modal` (`tests/test_app.py:26-28`).
  - **Acceptance test(s):** `AT-002`.
  - **Boundary catalog (QC-3):** ☑ empty (no URLs entered) ☑ boundary (1 URL) ☑ invalid (a non-`http` line dropped) ☑ error (markup/injection line dropped by `valid_url`, no crash — C-3).

### HLR-004 — Card indicator + open action for multiple URLs
- **Traceability:** US-002
- **Statement:** While a task has ≥1 valid URL, the system **shall** render the ↗ indicator on that task's card, and when the user triggers the open action on that task, the system **shall** open every valid URL.
- **Rationale (informative):** the card indicator and the `o`-action are the read/act surfaces; today both read the singular `task.url` (`views.py:154`, `app.py:252-255`) and must read the list.
- **Validation:** `test`
- **Executed verification:** `pytest tests/test_app.py -k open_all_urls` (provisional) — Pilot selects a task with 3 URLs, monkeypatches `taskboard.app.webbrowser.open` to collect calls, invokes the open action, asserts 3 opens; a render assertion checks ↗ present.
- **Numeric pass threshold:** task with 3 valid URLs → `webbrowser.open` call count `== 3`, opened set `==` the 3 URLs; task with 0 URLs → ↗ absent and open-call count `== 0`.
- **Priority:** high
- **Acceptance (black-box):**
  - **Observable outcome:** a 3-URL task shows ↗ and pressing `o` opens all three; a 0-URL task shows no ↗ and `o` does nothing.
  - **Shipped surface:** `card_cell`/`title_markup` (`views.py:142-161`, `108-121`); `action_open_url` bound to `o` (`app.py:48`, `252-255`).
  - **Deliverable + observation:** the rendered board text (↗ presence) + the collected `webbrowser.open` calls — observed via `board_text()` (`tests/test_app.py:21-23`) and a monkeypatch (pattern at `tests/test_app.py:382-391`).
  - **Acceptance test(s):** `AT-002`.
  - **Boundary catalog (QC-3):** ☑ empty (0 URLs → no ↗, no open) ☑ boundary (1 URL → 1 open) ☑ invalid (only-invalid URLs → treated as 0) ☑ error (open action on no-selection → no-op, existing guard `app.py:253-254`).

### HLR-005 — Task holds an ordered list of image references
- **Traceability:** US-003
- **Statement:** The `Task` model **shall** store an ordered list of image-reference strings (local file paths and/or `http(s)` image URLs) and **shall** round-trip it through save/load without raising on malformed input.
- **Rationale (informative):** parallels HLR-002; a brand-new field (`images`), so no legacy migration is required — only lenient load.
- **Validation:** `test`
- **Executed verification:** `pytest tests/test_app.py -k task_images_model` (provisional) — `Task.from_dict` with/without `images`, plus save→load round-trip.
- **Numeric pass threshold:** absent key → `images == []`; `{"images":[a,b]}` → `[a,b]`; round-trip equality `== True`; non-list `images` → `[]`, `0` exceptions.
- **Priority:** high
- **Acceptance (black-box):**
  - **Observable outcome:** a task persists and reloads its image list intact; an old board (no `images` key) loads with an empty list.
  - **Shipped surface:** `Task.from_dict` / `Board.save` (`models.py:194-206`, `238-245`).
  - **Deliverable + observation:** reloaded `Board.tasks[*].images` — observed by save/load round-trip assertion.
  - **Acceptance test(s):** `AT-003` (model leg).
  - **Boundary catalog (QC-3):** ☑ empty (no key → `[]`) ☑ boundary (1 ref) ☑ invalid (non-list → `[]`) ☑ error (corrupt file → empty board).

### HLR-006 — Task modal edits image references
- **Traceability:** US-003
- **Statement:** When the user opens the add/edit task modal, the system **shall** present the task's image references for editing and, on save, **shall** return them as an ordered list (blank lines removed).
- **Rationale (informative):** same write-path constraint as HLR-003; image refs are not restricted to `http(s)` (local paths are valid), so the modal keeps every non-blank line — the extension allowlist is applied only at *open* time (LLR-007.3), not at entry.
- **Validation:** `test`
- **Executed verification:** `pytest tests/test_app.py -k modal_images` (provisional) — Pilot sets the image widget to 2 non-blank lines + 1 blank, saves, asserts `images` length.
- **Numeric pass threshold:** 2 refs + 1 blank line → saved `images` length `== 2`, order preserved.
- **Priority:** medium
- **Acceptance (black-box):**
  - **Observable outcome:** the user types image refs in the modal and the saved task carries them in order.
  - **Shipped surface:** `TaskModal` (`modals.py:28-98`).
  - **Deliverable + observation:** created/edited `Task.images` via Pilot.
  - **Acceptance test(s):** `AT-003`.
  - **Boundary catalog (QC-3):** ☑ empty (none entered) ☑ boundary (1 ref) ☑ invalid (blank lines dropped) ☑ error (markup in a ref escaped on render — C-3).

### HLR-007 — Card indicator + open-in-viewer action for images (inline preview optional)
- **Traceability:** US-003
- **Statement:** While a task has ≥1 image reference, the system **shall** render a width-1 image indicator on that task's card, and when the user triggers the open-image action, the system **shall** open each reference in the OS default viewer — `http(s)` refs via the browser and local paths whose extension is in the image-extension allowlist via `os.startfile` — and **shall** ignore any local path not in the allowlist. Where a terminal graphics protocol is available, the system **may** additionally render an inline preview, degrading to open-in-viewer otherwise.
- **Rationale (informative):** the robust core is store + open-in-viewer (C-5). `os.startfile` executes non-image files by association, so the allowlist is a security control (C-6), not a nicety. Inline preview is the only non-core, terminal-dependent part.
- **Validation:** `test` (core) + `demo` (optional inline-preview stretch)
- **Executed verification:** `pytest tests/test_app.py -k open_images` (provisional) — Pilot selects a task with [1 image-ext local path, 1 image URL, 1 non-image local path], monkeypatches `os.startfile` and `webbrowser.open` to collect calls, invokes the open-image action; render assertion checks the image glyph present. Inline preview: manual `demo` in WezTerm (see §5.1) — NOT a CI gate.
- **Numeric pass threshold:** `os.startfile` called exactly once (the image-ext path); `webbrowser.open` called exactly once (the URL); the non-image path yields `0` `os.startfile` calls; task with 0 images → glyph absent + `0` opens.
- **Priority:** high (core) / low (inline-preview stretch)
- **Acceptance (black-box):**
  - **Observable outcome:** a task with mixed image refs shows the image glyph and opens exactly the allowed refs; a non-image path is silently ignored; a 0-image task shows no glyph.
  - **Shipped surface:** `card_cell` (`views.py:142-161`); a NEW open-image action + binding (proposed `i`, `app.py` BINDINGS `36-57`) using `os.startfile` (NEW import) + `webbrowser.open` (`app.py:5`).
  - **Deliverable + observation:** rendered board text (glyph presence) + collected `os.startfile`/`webbrowser.open` calls — observed via `board_text()` + monkeypatch.
  - **Acceptance test(s):** `AT-003`.
  - **Boundary catalog (QC-3):** ☑ empty (0 images → no glyph, no open) ☑ boundary (1 image) ☑ invalid (non-image path ignored; `.exe`/`.bat` never `startfile`'d — security) ☑ error (open-image on no-selection → no-op).

---

## 4. Low-level requirements (LLR)

> ID format `LLR-<HLR>.<M>`. Symbol citations are grep-verified `file:line` (2026-07-18) or flagged `NEW`.

### LLR-001.1 — Seed covers all project statuses (incl. the missing `cancelled`) and archived projects
- **Traceability:** HLR-001
- **Statement:** `seed_data()` **shall** return projects whose `.status` set equals the full `PROJECT_STATUSES` tuple and **shall** include ≥1 project with `archived=True`.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_app.py -k seed_generic_complete` asserting `{p.status for p in projects} == set(PROJECT_STATUSES)` and `sum(p.archived) >= 1`.
- **Numeric pass threshold:** status set `== 4/4`; archived projects `≥ 1`.
- **Acceptance criteria:**
  - Symbols: `seed_data` `models.py:311`; `PROJECT_STATUSES=("on_track","paused","cancelled","completed")` `models.py:19`; `Project.archived` `models.py:164`.
  - Pre-state (probe run 2026-07-18): current seed status set `= {on_track, paused, completed}`, **missing `cancelled`**; archived projects `= 0`. Post: both satisfied.

### LLR-001.2 — Seed covers all task statuses, all priorities, and archived tasks
- **Traceability:** HLR-001
- **Statement:** `seed_data()` **shall** return tasks whose `.status` set equals `TASK_STATUSES`, whose `.priority` set equals `TASK_PRIORITIES`, and **shall** include ≥1 task with `archived=True`.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_app.py -k seed_generic_complete` (same node) asserting the two sets and `sum(t.archived) >= 1`.
- **Numeric pass threshold:** task-status set `== 4/4`; priority set `== 3/3`; archived tasks `≥ 1`.
- **Acceptance criteria:**
  - Symbols: `TASK_STATUSES=("backlog","active","blocked","done")` `models.py:20`; `TASK_PRIORITIES=("low","normal","high")` `models.py:21`; `Task.archived` `models.py:191`.
  - Pre-state (2026-07-18): statuses `4/4` ✓, priorities `3/3` ✓ already; **archived tasks `= 0`** (must be added).

### LLR-001.3 — Seed covers all urgency buckets + standalone/project split
- **Traceability:** HLR-001
- **Statement:** `seed_data()` **shall** return tasks that populate the urgency buckets `{overdue, today, later|week, none, done}` and **shall** include both ≥1 standalone task (`project_id is None`) and ≥1 project task.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_app.py -k seed_generic_complete` computing `urgency(t, date.today())` (`views.py:195-208`) over tasks; counting `project_id is None`.
- **Numeric pass threshold:** buckets `⊇ {overdue, today, none}` and `⊇ {week or later}`; standalone `≥ 1`; project `≥ 1`.
- **Acceptance criteria:**
  - Symbols: `urgency` `views.py:195`; dates via `iso(offset)` helper pattern `models.py:315-316`; Inbox rule `board.project_by_id(t.project_id) is None` `views.py:325`.
  - Pre-state (2026-07-18): buckets `{overdue, done, none, week, today, later}` ✓; standalone `= 3`, project `= 13` ✓ (preserve in rewrite).

### LLR-001.4 — Seed exercises the two NEW fields (multi-URL + image)
- **Traceability:** HLR-001 (composition with HLR-002/HLR-005 — surface-reachability rule A-5)
- **Statement:** `seed_data()` **shall** include ≥1 task with `len(urls) ≥ 2` and ≥1 task with `len(images) ≥ 1`, so the demo showcases the batch's own new capabilities.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_app.py -k seed_generic_complete` asserting `max(len(t.urls) for t) >= 2` and `sum(1 for t if t.images) >= 1`.
- **Numeric pass threshold:** tasks with `len(urls) ≥ 2` `≥ 1`; tasks with `len(images) ≥ 1` `≥ 1`.
- **Acceptance criteria:**
  - Symbols: `Task.urls` `NEW — created in Phase 3 (LLR-002.1)`; `Task.images` `NEW — created in Phase 3 (LLR-005.1)`.
  - Pre-state (2026-07-18): `hasattr(task,'urls') == False`, `hasattr(task,'images') == False` — both NEW, so this LLR is unsatisfiable until LLR-002.1/005.1 land (correct dependency order recorded).

### LLR-001.5 — Seed content contains no author-identifying token
- **Traceability:** HLR-001
- **Statement:** No project name, task title, URL, or image reference produced by `seed_data()` **shall** match the author-identifier denylist (case-insensitive).
- **Validation:** `test (unit)` + `inspection`
- **Executed verification:** `pytest tests/test_app.py -k seed_generic_complete` running the denylist regex over `json.dumps` of the seeded projects+tasks. Denylist (executed 2026-07-18): `grndia | textualize\.io | job\s*hunt | m22 | dev-flow | proposal v2 | funnel | portfolio | interview prep | cv refresh | systems 5/5 | count-guard | rag paper | textual`.
- **Numeric pass threshold:** regex match count `== 0`.
- **Acceptance criteria:**
  - **Probe self-test (recorded 2026-07-18):** the denylist regex over the CURRENT seed returns **16 distinct hits** — `['CV refresh','GRNDIA','Job Hunt','M22','RAG paper','Textual','count-guard','dev-flow','funnel','grndia','interview prep','portfolio','proposal v2','systems 5/5','textual','textualize.io']`. Pass condition = **0** after the rewrite. This is a valid future-absence probe (non-trivial pre-state demonstrated).
  - Current offending symbols to remove: `Project("GRNDIA",...)` `models.py:319`; `Project("Job Hunt",...)` `models.py:320`; `Project("Textual",...)` `models.py:318`; `"https://grndia.com/pricing"` `models.py:333`; `"https://textual.textualize.io/"` `models.py:327`; titles `models.py:326-345`.

### LLR-001.6 — Seed remains load-safe and keeps existing invariants
- **Traceability:** HLR-001
- **Statement:** The rewritten `seed_data()` **shall** return `(list[Project], list[Task])` anchored to `date.today()` such that `Board.load` on a missing file seeds and saves it, and a corrupt file still starts empty.
- **Validation:** `test (integration)`
- **Executed verification:** existing `tests/test_app.py:32-39` (`test_boots_and_seeds`) + `tests/test_app.py:434-439` (`test_corrupt_file_starts_empty`) stay green.
- **Numeric pass threshold:** both existing tests pass (exit 0); `len(projects) > 0` and `len(tasks) > 0`.
- **Acceptance criteria:** Symbols: `seed_data` return tuple `models.py:311/347`; `iso` today-anchoring `models.py:313-316`; `Board.load` seed path `models.py:220-224`.

### LLR-002.1 — `Task.urls` list field replaces the singular `url`
- **Traceability:** HLR-002
- **Statement:** The `Task` dataclass **shall** declare `urls: list[str]` defaulting to an empty list (via `field(default_factory=list)`), replacing the singular `url` attribute as the canonical store.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_app.py -k task_urls_model_migration` asserting `Task("t").urls == []` and independence across instances (no shared mutable default).
- **Numeric pass threshold:** default `== []`; two `Task` instances do not share the list (identity check `is not`).
- **Acceptance criteria:** Symbols to change: `Task.url: str | None = None` `models.py:190` (removed/replaced); default pattern mirrors `id: str = field(default_factory=_new_id)` `models.py:192`. `Task.urls` = `NEW — created in Phase 3`.

### LLR-002.2 — `from_dict` migrates legacy `url` and reads modern `urls`
- **Traceability:** HLR-002
- **Statement:** `Task.from_dict` **shall** populate `urls` from the `urls` key when it is a list, else wrap a truthy legacy `url` string into a one-element list, else default to `[]`, never raising on malformed input.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_app.py -k task_urls_model_migration` with inputs `{"url":"https://x"}`, `{"urls":["a","b"]}`, `{}`, `{"urls":"notalist"}`, `{"url":None}`.
- **Numeric pass threshold:** `→ ["https://x"]`, `["a","b"]`, `[]`, `[]`, `[]` respectively; `0` exceptions.
- **Acceptance criteria:** Symbol: `Task.from_dict` `models.py:194-206`, legacy read at `url=d.get("url")` `models.py:204`. Lenient-edge convention cited `models.py:200-205`.

### LLR-002.3 — Save serializes `urls` and round-trips
- **Traceability:** HLR-002
- **Statement:** `Board.save` **shall** serialize `Task.urls` via `asdict`, and a subsequent `Board.load` **shall** reconstruct the identical list.
- **Validation:** `test (integration)`
- **Executed verification:** `pytest tests/test_app.py -k task_urls_model_migration` — build board with a multi-URL task, `save()`, `Board.load(path)`, assert equality.
- **Numeric pass threshold:** reloaded `urls == original urls` (order-exact) for a 3-URL task.
- **Acceptance criteria:** Symbols: `Board.save` `asdict(t)` `models.py:241-244`; `Board.load` `Task.from_dict` `models.py:230`.

### LLR-003.1 — Modal presents all URLs for editing
- **Traceability:** HLR-003
- **Statement:** `TaskModal.compose` **shall** render a multi-line URL entry widget pre-filled with the task's URLs, one per line.
- **Validation:** `test (e2e)` — Pilot
- **Executed verification:** `pytest tests/test_app.py -k modal_multi_url` — press `e` on a 2-URL task, assert the widget's initial text has both URLs on separate lines.
- **Numeric pass threshold:** widget initial line count for a 2-URL task `== 2`; both URLs present.
- **Acceptance criteria:** Replaces the single `Input(... id="f-url")` `modals.py:66-68`. Proposed widget: `TextArea(id="f-urls")` (`TextArea` import available, C-1). `id="f-urls"` and `TextArea` usage = `NEW — created in Phase 3`.

### LLR-003.2 — Modal save returns the ordered valid-URL list
- **Traceability:** HLR-003
- **Statement:** `TaskModal._save` **shall** split the URL widget by lines, strip each, drop blanks and any line failing `valid_url`, preserve order, and place the result under `data["urls"]`.
- **Validation:** `test (e2e)` — Pilot
- **Executed verification:** `pytest tests/test_app.py -k modal_multi_url` — set widget to `"https://a\nnot a url\nhttps://b"`, save, assert `data`/task `urls == ["https://a","https://b"]`.
- **Numeric pass threshold:** 3 lines (1 invalid) → `urls` length `== 2`, order `["https://a","https://b"]`.
- **Acceptance criteria:** Symbols: `_save` builds `data` dict `modals.py:86-98`, current `"url": self._val("f-url") or None` `modals.py:96` (replaced); `valid_url` reused `views.py:97-105`. The handler `_on_task_added`/`_on_task_edited` set fields from `data` (`app.py:203-224`) — `data` keys must match `Task` fields (contract-touch note: `url`→`urls`).

### LLR-004.1 — Card renders ↗ when a task has ≥1 valid URL
- **Traceability:** HLR-004
- **Statement:** `card_cell` and `title_markup` **shall** treat a task as URL-bearing when `any(valid_url(u) for u in task.urls)`, rendering the ↗ indicator (optionally suffixed with a count).
- **Validation:** `test (unit)` + `test (e2e)`
- **Executed verification:** `pytest tests/test_app.py -k open_all_urls` render leg + retained `test_url_renders_link_and_arrow` (`tests/test_app.py:394-398`, updated to a multi-URL seed task) — assert `↗` in `board_text`.
- **Numeric pass threshold:** ≥1-URL task → `↗` present; 0-URL task → `↗` absent in its cell.
- **Acceptance criteria:** Symbols to change: `valid_url(task.url)` gate at `card_cell` `views.py:154` and `title_markup` `views.py:113-118`; `has_url` helper `views.py:93-95`. Indicator-overlap invariant `test_columns_card_indicators_never_overlap_title` (`tests/test_app.py:350-379`) must stay green (width-1 glyph, C-2).

### LLR-004.2 — Open action opens all valid URLs
- **Traceability:** HLR-004
- **Statement:** `action_open_url` **shall** iterate the selected task's `urls`, and for each that passes `valid_url`, **shall** call `webbrowser.open`.
- **Validation:** `test (e2e)` — Pilot
- **Executed verification:** `pytest tests/test_app.py -k open_all_urls` — monkeypatch `taskboard.app.webbrowser.open` to append to a list (pattern `tests/test_app.py:382-391`), select a 3-URL task, call `app.action_open_url()`, assert the collected list.
- **Numeric pass threshold:** 3 valid URLs → open-call count `== 3`, collected set `==` the 3 URLs; 0 URLs → `0` calls.
- **Acceptance criteria:** Symbols: `action_open_url` currently `if task and valid_url(task.url): webbrowser.open(task.url)` `app.py:252-255`; binding `("o","open_url","Open URL")` `app.py:48`; `webbrowser` import `app.py:5`.

### LLR-005.1 — `Task.images` list field
- **Traceability:** HLR-005
- **Statement:** The `Task` dataclass **shall** declare `images: list[str]` defaulting via `field(default_factory=list)`.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_app.py -k task_images_model` asserting `Task("t").images == []` and per-instance identity.
- **Numeric pass threshold:** default `== []`; no shared mutable default (`is not`).
- **Acceptance criteria:** `Task.images` = `NEW — created in Phase 3`; add near `Task.url`/`urls` `models.py:190`. `default_factory` pattern `models.py:192`.

### LLR-005.2 — `from_dict` reads and `save` serializes `images`
- **Traceability:** HLR-005
- **Statement:** `Task.from_dict` **shall** populate `images` from the `images` key when it is a list, else `[]`, never raising; `Board.save` **shall** serialize it via `asdict`.
- **Validation:** `test (unit)` + `test (integration)`
- **Executed verification:** `pytest tests/test_app.py -k task_images_model` with `{"images":["a","b"]}`, `{}`, `{"images":"x"}`; plus save→load round-trip.
- **Numeric pass threshold:** `→ ["a","b"]`, `[]`, `[]`; round-trip equality `== True`; `0` exceptions.
- **Acceptance criteria:** Symbols: `Task.from_dict` `models.py:194-206`; `Board.save` `asdict` `models.py:241-244`.

### LLR-006.1 — Modal presents image refs for editing
- **Traceability:** HLR-006
- **Statement:** `TaskModal.compose` **shall** render a multi-line image-refs entry widget pre-filled with the task's images, one per line.
- **Validation:** `test (e2e)` — Pilot
- **Executed verification:** `pytest tests/test_app.py -k modal_images` — press `e` on a task with 1 image, assert the widget shows it.
- **Numeric pass threshold:** widget initial content for a 1-image task contains that ref; empty task → empty widget.
- **Acceptance criteria:** New `TextArea(id="f-images")` added to the modal Grid `modals.py:49-68`. `id="f-images"` and `TextArea` = `NEW — created in Phase 3`.

### LLR-006.2 — Modal save returns the ordered image-ref list
- **Traceability:** HLR-006
- **Statement:** `TaskModal._save` **shall** split the image widget by lines, strip each, drop blanks, preserve order, and place the result under `data["images"]` (no `http`-only filter — local paths are valid at entry).
- **Validation:** `test (e2e)` — Pilot
- **Executed verification:** `pytest tests/test_app.py -k modal_images` — set widget to `"C:/a.png\n\nhttps://x/b.jpg"`, save, assert `images == ["C:/a.png","https://x/b.jpg"]`.
- **Numeric pass threshold:** 2 refs + 1 blank → `images` length `== 2`, order preserved.
- **Acceptance criteria:** Symbols: `_save` `data` dict `modals.py:86-98`; `_val` strip helper `modals.py:82-84`. `data["images"]` must match the `Task.images` field name (contract-touch with `_on_task_*` at `app.py:203-224`).

### LLR-007.1 — Card renders a width-1 image indicator
- **Traceability:** HLR-007
- **Statement:** `card_cell` **shall** append a width-1 image indicator glyph to a task's indicator tokens when `len(task.images) ≥ 1`.
- **Validation:** `test (unit)` + `test (e2e)`
- **Executed verification:** `pytest tests/test_app.py -k open_images` render leg — a task with an image → glyph present in `board_text`; a task without → absent. Plus the overlap invariant `tests/test_app.py:350-379` stays green.
- **Numeric pass threshold:** image glyph present iff `len(images) ≥ 1`; every rendered line still `== width` (overlap test); glyph cell-width `== 1`.
- **Acceptance criteria:** Symbols: token list built in `card_cell` `views.py:153-158` (append after the `↗`/`◉` tokens via `_fit_indicators` `views.py:124-139`). Exact glyph = `assumed — verify in Phase 3`; constraint: single-cell (C-2), visually distinct from `↗`(`views.py:154`) and `◉`(`views.py:156`) — candidate `▤` (U+25A4) pending Phase-3 render check in WezTerm.

### LLR-007.2 — Open-image action opens each reference in the OS viewer
- **Traceability:** HLR-007
- **Statement:** A NEW open-image action **shall** iterate the selected task's `images`; for each `http(s)` ref it **shall** call `webbrowser.open`, and for each local path in the image-extension allowlist it **shall** call `os.startfile`.
- **Validation:** `test (e2e)` — Pilot
- **Executed verification:** `pytest tests/test_app.py -k open_images` — monkeypatch `taskboard.app.os.startfile` and `taskboard.app.webbrowser.open` to collect calls; select a task with `["C:/a.png","https://x/b.jpg"]`; invoke the action; assert one `startfile` (a.png) + one `webbrowser.open` (b.jpg).
- **Numeric pass threshold:** `startfile` calls `== 1`, `webbrowser.open` calls `== 1` for that input.
- **Acceptance criteria:** Symbols NEW: `action_open_images` + a binding (proposed `("i","open_images","Open image")` in BINDINGS `app.py:36-57`) + `import os` (`app.py` imports `1-17`, `os` not currently imported — verified: only `webbrowser`, `pathlib.Path` at `app.py:5-6`). `os.startfile` = Windows-only (C-6, DD-4). Reuse `valid_url` for the http branch (`views.py:97-105`).

### LLR-007.3 — Image-extension allowlist gates `os.startfile` (security)
- **Traceability:** HLR-007
- **Statement:** The open-image action **shall** pass a local path to `os.startfile` only if its lowercased suffix is in the allowlist `{.png,.jpg,.jpeg,.gif,.webp,.bmp,.svg}`, and **shall** ignore any other local path.
- **Validation:** `test (unit)` + `analysis`
- **Executed verification:** `pytest tests/test_app.py -k open_images` negative leg — a task with `["C:/evil.exe","C:/ok.png"]` → `startfile` called only for `ok.png`. Analysis: enumerate that no allowlist member is an executable-by-association extension on Windows.
- **Numeric pass threshold:** `startfile` calls for `["C:/evil.exe","C:/ok.png"]` `== 1` (ok.png only); `evil.exe` `startfile` calls `== 0`.
- **Acceptance criteria:** allowlist constant = `NEW — created in Phase 3`. Security rationale C-6; `security-reviewer` sign-off required before merge (§6.3 R-1). Extension check via `Path(ref).suffix.lower()` (`pathlib.Path` already imported `app.py:6`).

### LLR-007.4 — Inline preview is optional and degrades to open-in-viewer (STRETCH)
- **Traceability:** HLR-007
- **Statement:** Where a terminal graphics protocol (Kitty/iTerm/Sixel) is detected, the system **may** render an inline image preview; otherwise it **shall** fall back to the open-in-viewer behavior of LLR-007.2.
- **Validation:** `demo` (perceptual, NOT a CI gate) — flagged `assumed — verify terminal-graphics support at Phase 3`
- **Executed verification:** manual `demo` in WezTerm (`wezterm.lua` present) — open a task's image and observe an inline preview OR a viewer launch. No headless assertion possible (C-5).
- **Numeric pass threshold (qualitative):** on a graphics-capable terminal an inline preview appears; on a non-capable terminal the viewer opens instead and nothing crashes.
- **Acceptance criteria:** **KEY ASSUMPTION** — this LLR is the ONLY inline-preview claim and it is non-binding for CI; the batch does not overpromise inline rendering. If Phase-3 finds no reliable protocol path within budget, this LLR is dropped and the core (007.1–007.3) still satisfies US-3. No symbols named (nothing to cite).

---

## 5. Validation strategy

### 5.1 Methods

> **Two layers.** Layer A (white-box `TC-NNN`) validates HLR/LLR mechanism; Layer B (black-box `AT-NNN`) validates each story's outcome through the shipped surface.

- **Test (Layer A · white-box):** pytest 9.1.1 + pytest-asyncio 1.4.0, `asyncio_mode="auto"` (`pyproject.toml:24-25`); Textual `App.run_test()` Pilot for e2e (pattern throughout `tests/test_app.py`). This is the repo's ratified and installed stack (testing-strategy-vs-ADR rule satisfied: `requirements.txt:3,6,7`; no conflicting ADR exists).
- **Inspection (Layer A):** static review of `seed_data()` and modal/action diffs against the cited `file:line` symbols.
- **Analysis (Layer A):** the LLR-007.3 allowlist enumeration (no image-allowlist extension executes by Windows association).
- **Acceptance (Layer B · black-box):** Textual Pilot e2e + on-disk `board.json` inspection, asserting each story's outcome through the shipped surface with representative + boundary + negative evidence. `AT-NNN` ids and all Executed-verification file paths / `-k` selectors / node ids are **provisional-until-Phase-3** (V-5) and reconciled at Phase 4.
- **Demo (auxiliary · perceptual):** only LLR-007.4 inline preview (manual, WezTerm). NOT a substitute for the automated `AT-003` core.

### 5.2 Dual-traceability table

**Behavioral chain (black-box) — per user story:**

| US | Observable outcome | Shipped surface | Acceptance test (`AT-NNN`) | Observed? |
|----|--------------------|-----------------|----------------------------|-----------|
| US-001 | Seeded board has 0 author tokens + ≥1 item in every feature dimension | `Board.load`→`seed_data`; `~/.taskboard/board.json` | AT-001 | denylist==0 + all dimension thresholds |
| US-002 | 3-URL task shows ↗ and `o` opens all 3; legacy board migrates 1→[1] | `TaskModal`, `card_cell`, `action_open_url`, `from_dict` | AT-002 | ↗ present + 3 opens + migration list |
| US-003 | Image task shows glyph; open-image opens allowed refs; non-image ignored | `TaskModal`, `card_cell`, NEW open-image action | AT-003 | glyph + 1 startfile + 1 browser + 0 for exe |

**Functional chain (white-box) — per requirement:**

| Requirement | Method | Test Case (`TC-NNN`) | Notes |
|-------------|--------|----------------------|-------|
| HLR-001 | test (pilot/unit) | TC-001 | seed denylist + dimensions |
| LLR-001.1 | test (unit) | TC-001a | project statuses 4/4 + archived project |
| LLR-001.2 | test (unit) | TC-001b | task statuses/priorities + archived task |
| LLR-001.3 | test (unit) | TC-001c | urgency buckets + standalone/project |
| LLR-001.4 | test (unit) | TC-001d | ≥2-URL + ≥1-image seed task |
| LLR-001.5 | test (unit)+inspection | TC-001e | denylist == 0 (pre-state 16 hits) |
| LLR-001.6 | test (integration) | TC-001f | boots+seeds / corrupt-empty stay green |
| HLR-002 | test | TC-002 | urls model + migration |
| LLR-002.1 | test (unit) | TC-002a | `urls` default_factory |
| LLR-002.2 | test (unit) | TC-002b | legacy `url`→[url], modern, malformed |
| LLR-002.3 | test (integration) | TC-002c | save/load round-trip |
| HLR-003 | test (e2e) | TC-003 | modal multi-URL |
| LLR-003.1 | test (e2e) | TC-003a | prefill all URLs |
| LLR-003.2 | test (e2e) | TC-003b | save → valid ordered list |
| HLR-004 | test | TC-004 | ↗ + open-all |
| LLR-004.1 | test (unit/e2e) | TC-004a | ↗ iff ≥1 valid URL |
| LLR-004.2 | test (e2e) | TC-004b | open-all count == n |
| HLR-005 | test | TC-005 | images model |
| LLR-005.1 | test (unit) | TC-005a | `images` default_factory |
| LLR-005.2 | test (unit/integration) | TC-005b | from_dict + round-trip |
| HLR-006 | test (e2e) | TC-006 | modal images |
| LLR-006.1 | test (e2e) | TC-006a | prefill images |
| LLR-006.2 | test (e2e) | TC-006b | save → ordered list |
| HLR-007 | test | TC-007 | glyph + open-in-viewer |
| LLR-007.1 | test (unit/e2e) | TC-007a | width-1 glyph iff ≥1 image + overlap green |
| LLR-007.2 | test (e2e) | TC-007b | startfile / webbrowser routing |
| LLR-007.3 | test (unit)+analysis | TC-007c | allowlist gates startfile (exe → 0) |
| LLR-007.4 | demo | — | manual WezTerm; no CI TC (stretch) |

### 5.3 Batch acceptance criteria
- 100 % of LLRs (except the `demo`-only LLR-007.4) covered by ≥1 passing `TC`.
- Every user story has ≥1 passing `AT` observing its outcome through the shipped surface with boundary + negative evidence (AT-001/002/003).
- Denylist match count over the seeded board `== 0`.
- All 28 pre-existing tests in `tests/test_app.py` green after the migration touch (the two URL tests updated, not deleted).
- 0 blocker fails; every requirement has an assigned validation method.
- `security-reviewer` sign-off on LLR-007.2/007.3 (`os.startfile` surface) before merge.

---

## 6. Appendices

### 6.1 Extended glossary
See §1.3. Additionally: **image-extension allowlist** = `{.png,.jpg,.jpeg,.gif,.webp,.bmp,.svg}` (LLR-007.3); **denylist** = author-identifier regex (LLR-001.5).

### 6.2 Relevant design decisions
- **DD-1 — one seed rewrite, no renderer change.** US-1 is satisfied purely inside `seed_data()`; renderers already handle every dimension (verified: urgency buckets already appear in pre-state). Reversible.
- **DD-2 — `url`→`urls` is a one-way forward migration.** `from_dict` consumes the legacy `url` key into `urls`; `save` writes only `urls`. Old readers of a new file lose links (acceptable: single-user local app). **One-way door for the on-disk format** — flagged loudly; if reversibility is required, keep writing a mirror `url` (first element). Recommend NOT mirroring (simplicity) unless a downgrade path is needed.
- **DD-3 — open-all for multi-URL** (not a chooser). Simple > clever; deterministic; headless-testable. Reversible (a chooser can be added later).
- **DD-4 — Windows-only local image open.** `os.startfile` is Windows-only; the app is a Windows/WezTerm desktop widget. Non-Windows local-file open is a documented limitation, not a bug. `http(s)` image refs work cross-platform via `webbrowser`. Low reversibility cost (add a `sys.platform` branch later).
- **DD-5 — image indicator glyph deferred to Phase-3 render check** (C-2 width-1 constraint; candidate `▤`).

### 6.3 Open risks
- **R-1 (security, high) — `os.startfile` executes by association.** Mitigation: LLR-007.3 allowlist + `security-reviewer` sign-off. Residual: a user could name a `.svg` that a browser renders with script — acceptable within the single-user trust boundary (A-1) but noted.
- **R-2 (operational, medium) — migration breaks the two existing URL tests.** `test_url_task_open_action` (`tests/test_app.py:382-391`) and `test_url_renders_link_and_arrow` (`394-398`) read `task.url`. Mitigation: update them to the list API in the same increment (A-3); counts as a migration touch, not scope creep.
- **R-3 (UX, low) — inline preview may not work in the user's terminal.** Mitigation: it is a stretch LLR that degrades to open-in-viewer (C-5, LLR-007.4). No overpromise.
- **R-4 (cost, low) — file budget.** Changes span `models.py`, `modals.py`, `views.py`, `app.py`, `tests/test_app.py` = 5 files. At the ≤5-file increment ceiling; recommend splitting into 3 increments (seed / multi-URL / images) so each increment stays well under budget.
- **R-5 (contract, medium) — modal `data` keys must equal `Task` field names.** `_on_task_added`/`_on_task_edited` do `setattr`/`Task(**data)` (`app.py:206`, `221-222`); a `data["urls"]`/`data["images"]` key that mismatches the field raises. Contract-touch checkpoint at Phase-3.

### 6.4 Phase-1 reconciliation log
No reconciliation events yet (initial draft). Any later threshold/statement change or LLR add/promote/remove will add a per-decision audit table here (body edit first, then the audit row).

### 6.5 Requirement amendments (Before / After · Deleted / New)
None (initial draft).

---

## Evidence checklist (architect gate)
- [✓] **Constraints stated explicitly.** §2.4 C-1…C-6 (Textual 8.2.8 pin `requirements.txt:3`; width-1 glyphs `views.py:6-11`; `os.startfile` execution risk).
- [✓] **At least 2 alternatives considered.** DD-3 open-all vs chooser; DD-2 one-way migration vs mirror `url`; §6.2.
- [✓] **Recommendation has rationale tied to constraints.** DD-2/DD-3/DD-4 each tie to a stated constraint (single-user trust, headless-testability, Windows target).
- [✓] **Risks listed (operational, security, cost, lock-in).** §6.3 R-1…R-5 (security `os.startfile`; migration regression; file budget; contract).
- [✓] **Cost / latency estimated where relevant.** No token/API cost (local app); file-budget cost in R-4 (5 files → split into 3 increments).
- [✓] **Diagram included when flow is non-trivial.** Flow is linear (model→modal→card→action); expressed as the shipped-surface column in §5.2 rather than a mermaid diagram — noted as a deliberate omission.
- [✓] **What would change the recommendation is stated.** DD-2 (mirror `url` if downgrade path needed); LLR-007.4 (drop inline preview if no protocol within budget); DD-4 (`sys.platform` branch if non-Windows needed).
- [✓] **Two-layer requirements.** Every US has a first-class Acceptance block + `AT-NNN` (§3) AND both traceability chains exist (§5.2 behavioral US→AT→outcome + functional US→HLR→LLR→TC).
- [✓] **Draft-time symbol verification.** Every referenced symbol cited `file:line` (verified 2026-07-18) or flagged `NEW`/`assumed`: `Task.url` `models.py:190`; `seed_data` `models.py:311`; `TaskModal` `modals.py:28`, `#f-url` `modals.py:66-68`; `action_open_url` `app.py:252-255`, binding `app.py:48`; `valid_url` `views.py:97-105`; `card_cell` `views.py:142-161`. NEW: `Task.urls`, `Task.images`, open-image action, allowlist. `os` not currently imported (`app.py:1-17`).
- [✓] **Probe self-test executed.** Denylist probe run 2026-07-18 → 16 pre-state hits (recorded LLR-001.5); dimension probe → `cancelled` status + archived items MISSING in current seed (recorded LLR-001.1/001.2).
