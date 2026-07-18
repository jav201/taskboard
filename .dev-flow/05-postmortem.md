# Post-mortem — taskboard — Batch 2026-07-18-batch-01

> **Artifact language:** English (`state.json` `language = en`).
> Phase 5 artifact. Co-authors: `architect` + `qa-reviewer`. Structured for cross-batch sweeping — keep the section order.

## 🔑 At a glance (read first)

- **Outcome:** **closed clean** — 0 phase iterations, validation PASS, 3 commits on `main`. Two honestly-open items carried forward as ACCEPTED (not failures).
- **Top 3:** ① **Phase-2 review caught two pre-implementation defects** the spec's own census missed — the 3rd migration observer (`test_app.py:361` `url=` constructor kwarg, F1) and the scriptable-`.svg` hole in the `os.startfile` allowlist (F4) — before a line of Phase-3 code. ② **Scope grew 2→3 stories mid-kickoff** (US-3 images added), which forced an unplanned in-batch migration of 3 seed `url=` kwargs in Increment 1 just to keep the app booting. ③ **No root cause** — no phase needed a 2nd iteration.
- **New control this batch:** none *new* — this batch instead **exercised** the accumulated batch-06→11 census/probe/two-layer controls, and they paid off (F1 is exactly the "(N+1)th observer the reverse-grep misses" case those controls exist to catch).
- **Open items → next batch:** **5** — biggest: the **project-status edit binding** (`e` edits tasks only; there is still no UI path to set a project `paused`/`cancelled`/`completed`, so the seed's new `cancelled` project can be shown but not reached by a user).
- **Metrics:** iterations `0` · findings `10 closed-or-accepted` / `10 opened` · ledger `28`→`36`.

> Enough to know the batch's health and what carries forward. Detail below only for the why.

---

## Detail (reference)

### What worked
- **0-blocker requirements.** Phase-1 shipped 3 US / 7 HLR / 23 LLR / 3 AT / 26 TC with every DoR `READY` and draft-time citations real (denylist probe recorded 16 live pre-state hits; dimension probe recorded the missing `cancelled` status + zero archived items). Phase-2 opened **0 blockers** against it.
- **The Phase-2 review caught real defects before implementation.** Two independent-lens findings that a naive spec would have carried into a red Phase-3 suite:
  - **F1** — the change-first supersession census found a **3rd** `Task.url` observer the spec's reverse-grep missed: `test_columns_card_indicators_never_overlap_title` builds `Task(url="…")` at `test_app.py:361`. Because it is a **constructor kwarg** it raises `TypeError` at construction (not the `AttributeError` a `\.url\b` grep anticipates), so it escaped the spec's own two-site census. Caught at Phase 2, fixed in Increment 1.
  - **F4** — the security lens flagged `.svg` inside the `os.startfile` allowlist as the one member that *defeats the control's purpose* (scriptable format, executes embedded script via browser association). Removed pre-implementation; final startfile allowlist `{.png,.jpg,.jpeg,.gif,.webp,.bmp}`.
- **All 3 ATs are mutation-discriminating, RED→GREEN.** Each acceptance test has a recorded counterfactual RED: open-all→first-only turned **AT-002** red; re-adding `.svg` turned **AT-003** red; renaming a seed project to "Textual Redesign" turned **AT-001** red. The black-box suite discriminates *value*, not merely wiring — and F2 was discharged by pressing the **real** `o`/`i` bindings through Pilot, not calling `action_*()` directly.
- **The security hardening landed exactly as reviewed.** `_open_local_image` implements F3+F4 as specced: UNC (`\\`/`//`) refused, `file://` refused, extension allowlist (no `.svg`), `os.path.isfile` existence check, `try/except OSError` so a keypress never crashes. Negative proven live: `["C:/evil.exe", "\\\\host\\share\\a.png", "file:///c:/a.png", missing.png]` → `startfile` called for `ok.png` only.

### What didn't / friction (honest)
- **US-3 (images) was added mid-kickoff** — the batch objective grew from 2 stories (seed scrub + multi-URL) to 3 (+ images per task). It landed cleanly, but it is scope drift against the originating objective and is recorded as such below.
- **`TextArea` default `height: 1fr` collapses in the auto-height modal.** The multi-line URL/image widgets render zero-height under the modal's content-sized layout, so height was set **programmatically to 4** rather than via CSS — chosen to stay within the 5-file increment cap (no `.tcss` touch). Verified functionally by AT-002/003, **not** by eye in a real terminal.
- **The new `▤` glyph risked breaking the overlap invariant** (`test_columns_card_indicators_never_overlap_title`). Resolved by **seed design, not code**: image-bearing seed tasks are normal/low priority with no URLs, so their card carries only `▤`, never co-occurring with `◉`/`↗`. The invariant test stayed green **unmodified** — the guard is still armed for any future seed that combines them.
- **Inline image preview intentionally NOT built.** It depends on a terminal graphics protocol (Kitty/iTerm/Sixel) that cannot be asserted headlessly (`App.run_test()` has no real terminal, C-5). Specified only as the stretch `may`-clause LLR-007.4, degrading to open-in-viewer (LLR-007.2, fully validated). No overpromise — but it is a promised-looking capability the batch deliberately did not ship.
- **`▤` true terminal cell-width is unverifiable in CI.** Headless proof is Python line-width invariance only; true WezTerm rendered cell width is a manual/Phase-3 render check. Accepted, attributed to C-2/C-5.

### Scope drift (planned vs actual)
| Planned | Actual | Note |
|---------|--------|------|
| 2 stories (seed scrub + multi-URL) | **3 stories** (+ US-3 images per task) | US-3 added mid-kickoff; objective grew. Landed clean, but drift against the originating scope. |
| Migrate the 2 URL-reading tests named in the census (`:388-391`, `:394-398`) | **3 sites in 2 functions** migrated (`:361` added, F1) | The `url=` constructor kwarg at `:361` was not in the spec census; found at Phase 2. |
| No seed change until Increment 3 | **Not-in-spec migration of 3 seed `url=` kwargs in Increment 1** | Necessary: without it the app would not boot after `Task.url`→`Task.urls` and before the Increment-3 seed rewrite. |

### Metrics (full)
| Metric | Value |
|--------|-------|
| Iterations per phase | `{0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0}` — no phase re-iterated |
| Findings opened / closed-or-accepted | `10` / `10` (F1–F9 Phase-2 + G-001 Phase-4) |
| Findings by severity (blocker/major/minor) | `0 / 4 / 6` (Phase-2: 0/4/5; Phase-4: +1 minor G-001) |
| Where caught (Phase 2 / P3 gate / P4) | `9 / 0 / 1` (F1–F9 at review; G-001 at validation) |
| Test ledger (base − D + A = post) | `28 − 0 + 8 = 36` (36 collected, 36 passed) |
| Files touched · increments (cap trips) | `5` unique (`models.py`, `views.py`, `app.py`, `modals.py`, `tests/test_app.py`) · `3` increments (`2` cap trips — Inc-1 & Inc-2 both at the 5-file cap; Inc-3 = 2) |
| Commits pushed to `main` | `3` — `f1b9e96` multi-URL · `63f4a22` images · `7532e03` generic seed |

### Root causes (only if a phase took ≥2 iterations)
- **None.** No phase took ≥2 iterations, so no root-cause analysis is required. (F1/F4 were caught *within* Phase 2 and folded into Phase 3 — they never forced a re-iteration of an approved gate.)

### Process / workflow findings
> About the dev-flow itself (phases, gates, templates, agents, controls).
- **The change-first census earns its keep, and the `url=` kwarg is a reusable lesson.** F1 confirms the batch-10 A-1 principle: a reverse-grep keyed on the *read* form (`\.url\b`) is structurally blind to the *constructor-kwarg* form (`url=`), which fails at a different point (construction `TypeError` vs `AttributeError`). **Suggested workflow note:** when a field is renamed/removed, the census reverse-grep must include the `field=` constructor form, not only `\.field\b` reads. (This batch already did — that is *how* F1 was found — worth promoting to the census-family prose.)
- **Mid-kickoff scope growth (2→3 stories) had no gate to catch it.** The objective in `state.json` already read "images per task," so Phase 1 absorbed US-3 without friction, but there was no explicit "objective changed since batch open" checkpoint. **Suggested change:** a one-line scope-delta note at the Phase-1 gate when the story count differs from the batch-open objective.
- **The standing-authorization self-approval model worked but concentrates risk.** Every gate was self-approved by the agent against the objective exit criteria under the operator's end-to-end authorization, and each decision was logged in `state.json decisions_log`. Clean here because findings were 0-blocker; worth noting the model has no second human in the loop on a blocker.

### Product findings
> About the code/product under development.
- **The `Task.url`→`Task.urls` migration is a one-way door (DD-2)** — an old reader opening a new file loses links. Flagged loudly, accepted under the single-user local-app trust boundary; `not hasattr(Task("t"), "url")` is now a negative regression guard.
- **`os.startfile` is Windows-only (DD-4).** Non-Windows local-image open is a documented limitation; `http(s)` image refs open cross-platform via `webbrowser`.
- **No UI path to set project status.** The seed now includes a `cancelled` project (dimension coverage), but `e` edits **tasks** only — a user cannot move a project to `paused`/`cancelled`/`completed` from the board. Product gap, carried forward.
- **The seed is heavier (16 tasks / 6 projects)** — intentionally tall enough to exercise the overflow-scroll test; nav/scroll tests stayed green.

### Control lineage
- **New control proposed this batch:** none. This batch was a *consumer* of the accumulated controls, not a producer.
- **Prior controls exercised — which held:**
  - **Change-first supersession census (batch-10 A-1)** — HELD and paid off; surfaced the F1 (N+1)th observer that the spec's own two-site census missed. Not stamped "VERIFIED COMPLETE" (batch-10 A-2 respected); the increment gate remained the completeness guarantee.
  - **Probe self-test (batch-07 B-3/B-4)** — HELD; the denylist probe demonstrated a non-trivial pre-state (16 live hits) so the "0 after rewrite" future-absence check was proven, not assumed.
  - **Two-layer black-box acceptance (batch-14)** — HELD; every story reconciled to exactly one on-disk collected AT node with representative + boundary + **negative** evidence, and F2 forced the ATs onto the **real** `o`/`i` key bindings (a green suite could not pass with them unwired).
  - **Surface-reachability (batch-11 A-5)** — HELD; LLR-001.4 explicitly composes the two new fields into the seed, and the Phase-4 bidirectional matrix drove all 4 inputs through the modal/binding (not direct service kwargs) and observed all 4 deliverables at the shipped surface.
  - **`os.startfile` security gate (C-6)** — STRESS-TESTED; the review split it into core-allowlist (blocker-preventing) vs F3/F4 hardening, and the hardening landed with live negative proof.
- **Near-misses:** F1 (the `url=` kwarg) would have produced a `TypeError`-red Phase-3 suite had the census not been change-first; F4 (`.svg`) would have shipped a scriptable-format execution vector had the security lens not run pre-implementation.

### Open / deferred items → next batch
| Item | Type (process/product) | Reason deferred | Trigger / owner |
|------|------------------------|-----------------|-----------------|
| Project-status edit binding (no UI path to set a project `paused`/`cancelled`/`completed`; `e` edits tasks only) | product | Out of scope for this batch (parked in objective as out-of-scope carry) | Next batch spec / `architect` + `software-dev` |
| `▤` true terminal cell-width real-terminal (WezTerm) render check | process/product | Unverifiable headlessly (C-2/C-5); CI proves single-cell only via Python line-width invariance | Manual render check / `qa-reviewer` |
| Inline image preview stretch (Kitty/iTerm via `textual-image`; WezTerm-capable) | product | Terminal-graphics-dependent; specced as `may`-clause LLR-007.4, degrades to open-in-viewer | Stretch batch / `architect` (terminal-graphics spike) |
| Modal prefill-on-edit dedicated `e`-key assertion (Phase-4 minor **G-001**) | process | Write path + black-box deliverable both observed; read-back prefill covered by inspection, not a dedicated TC | Optional TC / `qa-reviewer` |
| Sync the `wezterm.lua` paste binding into the repo | process/product | Parked in objective out-of-scope carries | Next batch / `software-dev` |

### Decisions summary (from `state.json decisions_log`)
> Every autonomous decision, mirrored. All gates **self-approved** under the operator's 2026-07-18 end-to-end standing authorization (agent self-approves each gate against the objective exit criteria and documents it); merge = **commit straight to `main`, no PR**.

| Phase | Decision | Basis logged |
|-------|----------|--------------|
| 1 | **approved** | 3 US / 7 HLR / 23 LLR / 3 AT / 26 TC; DoR all READY; draft-time citations real; gaps (missing `cancelled`+archived in seed; 16 author-tokens) recorded. Coverage/Certainty/Evidence met. |
| 2 | **approved** | 0 blockers; 4 majors (F1 `test:361` `url=` kwarg; F2 AT-003 press `i`; F3 startfile isfile/try-except/UNC; F4 drop `.svg`) folded into Phase 3; 5 minors. Bars met. |
| 3 | **approved** | 3 increments (`f1b9e96`, `63f4a22`, `7532e03`) pushed to `main`; 36 tests green (28+8); seed denylist 0 author tokens (independently rescanned); startfile allowlist hardened; AT-001/002/003 black-box + mutation-checked. |
| 4 | **approved** | Validation PASS; each AT reconciled to one node; both layers; ledger 28→36; supersession 0 live `.url`; 1 minor (G-001, prefill by inspection); 2 accepted open items; no iterate. |
| — | **Commit-to-`main`** | Operator standing authorization ("Commit straight to main, no PR"). |
| — | **Images inline-preview DESCOPED** | C-5 terminal-graphics dependency; specced as stretch `may`-clause LLR-007.4. |
| — | **Neutral seed theme chosen** | Generic software-product org (Website Redesign / Mobile App / API Platform / Legacy Sunset / Data Warehouse / Internal Wiki); 0 denylist tokens, all dimensions covered. |

### Evidence checklist — architect + qa-reviewer

**architect gate**
- [✓] Constraints stated explicitly — C-1…C-6 in §2.4 requirements (Textual pin, width-1 glyph, markup-safety, lenient edges, terminal-graphics, `os.startfile` external-action).
- [✓] At least 2 alternatives considered — open-all vs chooser (DD-3, open-all chosen); separate `i` binding vs overloading `o` (separate chosen); CSS `1fr` vs programmatic height (programmatic, to respect the 5-file cap).
- [✓] Recommendation tied to constraints — one-way migration DD-2 chosen against the single-user trust boundary (A-1); startfile allowlist chosen against C-6.
- [✓] Risks listed — DD-2 one-way door, Windows-only `startfile` (DD-4), `TextArea` height, `▤` cell-width, inline-preview descope; all in increments + §6.3.
- [✓] Cost/latency estimated where relevant — N/A (local single-process TUI, no model calls or per-request cost surface this batch); noted rather than hand-waved.
- [✓] Diagram — N/A; no non-trivial new flow (model field + modal widget + indicator + open action, all linear); the trace tables carry the structure.
- [✓] What would change the recommendation — a multi-user or shared-board trust model would reopen DD-2 (one-way migration) and the "no open-all cap" (F5) decisions.
- [✓] Two-layer requirements — every story has a first-class Acceptance block + `AT-NNN` and BOTH chains exist (behavioral US→AT→outcome + functional US→HLR→LLR→TC); confirmed in Phase-2 two-layer table and Phase-4 AT→node reconciliation.

**qa-reviewer gate**
- [✓] Acceptance criteria use Given/When/Then equivalents — HLR Acceptance blocks (Observable outcome / Shipped surface / Deliverable+observation) drive each AT.
- [✓] Test cases have explicit Expected — numeric thresholds on every `test`/`analysis` LLR (`urls==2`, `startfile==[real_png]`, denylist `==0`).
- [✓] Edge cases include empty/boundary/invalid/error — 0-URL/0-image no-open (empty), single glyph/1-item dims (boundary), `not a url`/non-list refs (invalid), corrupt-file→empty + missing/UNC/`file://` refused (error).
- [✓] Regression checklist exists — supersession inspection (singular `url` 0 live refs) + ledger `28−0+8=36` + pre-existing suite green.
- [✓] No real PII/secrets — seed scrubbed to 0 author-denylist tokens over the on-disk `board.json` deliverable (`:536`).
- [✓] Test results not fabricated — every result cites the actual `36 passed in 12.08s` run and a collected node id.
- [✓] Layer B (black-box) — each story observed through the shipped surface (Pilot `o`/`i` keypress; on-disk `board.json`) with boundary + negative evidence; ATs mutation-discriminating (recorded RED per AT).
- [✓] Bidirectional surface-reachability — all 4 inputs + 4 deliverables exercised/observed through the handler, not only the service API (Phase-4 matrix).
