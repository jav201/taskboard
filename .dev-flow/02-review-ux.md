# UX Review — taskboard — Batch 2026-08-14-batch-04 (Phase 2, PDR)

> **Reviewer:** ux-reviewer (trigger family D — interaction change: 13 keys + 1 modal).
> **Artifacts reviewed:** `.dev-flow/01-requirements.md` (HLR-001…HLR-012, §3.0 key contract), `.dev-flow/2026-08-14-batch-04/PLAN.md`, `prototypes/kanban_ideas/out/kanban-ideas.html` (operator-approved K1–K11), `taskboard/keymap.py`, `taskboard/app.py`, `taskboard/aperture.py`, `README.md`.
> **Lens:** discoverability, key-map coherence, mode ambiguity, user-facing honesty ("every key shown works, every key that works is shown", `keymap.py:1-18`).
> **Method:** inspection with declared criteria (cognitive walkthrough over the operator's tasks) + executed measurements of the real `fit_bar` degradation law. **Evaluation with real users was not performed** — the context of use is a single expert operator, per §2.3 of the requirements.

## Verdict: **iterate** — 2 blockers, 3 majors, 5 minors

The requirements are strong where they specify mode indicators (sort header token, focus named in header, undo-restores-stamp) and the aperture contract (AT-019 is exactly the right test). Two specification holes must close before Phase 3: **K7 collapse has no exit as specified**, and **at the app's own shipped default window size the new keys fall off the key bar entirely** — the batch's whole discoverability story.

---

## Findings

### B-1 · blocker — K7 collapse: the toggle can never restore a collapsed phase (no exit from the mode)

**Evidence.** HLR-007 (`01-requirements.md:374`) keys the toggle off the *selected task*: "presses `z` with a task selected … toggle the collapsed state of that task's phase". But a collapsed phase contributes **an empty column to the nav model** (LLR-007.1, `:553`) and `action_hmove` "jump[s] to the nearest **non-empty** column's first task" (`taskboard/app.py:403-411`). So after collapse, the selection is relocated to a *non-collapsed* column (HLR-007's own rule), and there is no reachable selection inside the collapsed phase — pressing `z` again toggles the *wrong* phase (collapses the one the cursor landed in), never restores the collapsed one. AT-012 (`:385`) asserts "press `z` again: titles return" without defining what the selection is at that moment; as specified, that assertion is unsatisfiable by the stated toggle semantics.

**Lockout endgame.** HLR-007's boundary catalog explicitly allows collapsing the last non-collapsed phase ("selection becomes none", `:386`). With every phase collapsed there is no selection anywhere, `z` requires a selection, and the board is a wall of `✓ N` rows with no keyboard way back (session-level state; only an app restart recovers).

**Required resolution (PDR decision, then written into HLR-007/AT-012):** make `z` target the **cursor's column**, not the selected task — which requires nav to keep collapsed columns addressable (a column cursor position that survives an empty column), so `hmove` can park on a collapsed column and `z` restores it. Any alternative (e.g. `z` restores the most recently collapsed phase when the current one isn't collapsed) is acceptable if it is *written down* and AT-012 exercises the exact key sequence: collapse → selection relocates → restore via the stated path.

---

### B-2 · blocker — At the shipped default window (96 cols), the batch's new keys drop off the key bar entirely

**Evidence (executed, not asserted).** The shipped WezTerm config sizes the widget at **96 cols** (`wezterm.lua:30-31`). I measured `fit_bar` with the exact §3.0 key set appended to KEYMAP (30 → 40 keys in kanban view):

| view · width | keys shown | labels kept | KEYS dropped |
|---|---|---|---|
| kanban · 96 (default) | 31 / 40 | 0 | **9** |
| kanban · 120 | 40 | 0 | 0 |
| kanban · 160 | 40 | 6 | 0 |
| kanban · full labels | — | — | needs **380 cells** |

Today at 96 cols the law's letter barely holds (30/30 keys shown, 1 label). After this batch, at the app's own default size, **9 keys are invisible** behind a bare `+9` — and because `fit_bar` drops from the end of declaration order (`keymap.py:113-120`), if the new keys are appended at the end of KEYMAP the 9 dropped keys **are exactly the 9 new capabilities**. The keymap law's own words: "a capability whose key is not on screen does not exist" (`keymap.py:4`).

**The doc's candidate resolution does not fix it.** §6.3 (`:684`) punts to Phase 2 with "kanban-scoping some of the new keys" — scoping helps the *other three views* (35 vs 38 keys) but kanban, the view that carries all 40, is untouched. That is the decision this review was asked to make, and scoping alone is insufficient.

**Required resolution (PDR decision, recorded in §6.2):** a combination, e.g. (a) kanban-scope the mode keys (see M-1) so lanes/agenda/gantt stay honest; (b) **place the new KEYMAP entries before the arrows** so at narrow widths the muscle-known arrow keys (which have `hjkl` aliases and need no bar to be discovered) are what drops, not the new capabilities; (c) explicitly accept a glyph-only bar at 96–160 cols and name the discovery seat for it (the `?` legend and/or README), since the `+N` note says *how many* keys are hidden but never *which*. Without (b)+(c) the batch ships nine invisible features at the default size.

---

### M-1 · major — `s` `g` `z` `F` are unscoped in §3.0: advertised in every view, meaningful only in kanban

**Evidence.** §3.0 (`:247-250`) declares the four mode keys with no `views=` scope, so they show on the key bar in lanes, agenda and gantt — while HLR-003/004/007/008 all scope the *behavior* to the kanban view ("presses `s` **in the kanban view**"). No LLR requires a view guard on the actions. Two failure shapes, both contract violations: (i) the action fires outside kanban → a shown key mutates invisible kanban state (press `s` in Agenda, nothing changes on screen, kanban is silently re-sorted for next visit); (ii) the action no-ops outside kanban → a shown key does nothing. The `tab` precedent does both halves correctly: `views=("kanban",)` in the seat (`keymap.py:71`) **and** an explicit guard in the action (`app.py:466-469`, "a no-op elsewhere").

**Required:** `views=("kanban",)` on `s` `g` `z` `F` in §3.0, plus an LLR line per action requiring the `view_mode == "kanban"` guard, plus one Pilot assertion that pressing `s` in lanes changes nothing (rendered text + board file).

---

### M-2 · major — `escape` focus-exit is bound app-wide; only the *bar* is kanban-scoped

**Evidence.** `views=` filters only `bar_keys` (`keymap.py:94`); `app_bindings()` (`keymap.py:84-86`) binds **every** KEYMAP entry in every view. So the new kanban-scoped `escape` (`§3.0:256`) is *live* in lanes/agenda/gantt: pressing Esc there fires `action_focus_exit` and silently clears a kanban focus the user cannot see from that view. LLR-008.1 (`:561`) specifies no view guard. Second wrinkle: the bar shows the `Esc` row in kanban **permanently**, but it only does something while a focus is active — a mostly-dead advertised key, the same lie-in-reverse the `tab` comment warns about (`keymap.py:69-70`). Modal shadowing itself is safe (every modal binds its own `escape` — verified `modals.py:119-1027`; the aperture binds its own, `aperture.py:61`).

**Required:** view-guard `action_focus_exit` (fire only in kanban *and* only when a focus is active); PDR decides whether the permanent bar row is acceptable (precedent says keys that no-op shouldn't be advertised — a conditional bar row is a new mechanism the static KEYMAP seat cannot express, so the honest minimum is the guard + a README row that says what Esc does).

---

### M-3 · major — the `✓ N` collapse summary lies about non-done phases and drops the prototype's restore affordance

**Evidence.** HLR-007 mandates one summary row "of the form `✓ N`" for *any* collapsed phase (`:374`). The approved prototype only ever collapsed **Done** — `✓ 2 completadas` is truthful there (`kanban-ideas.html` K7 section, "Done colapsada a una fila"). Generalized to Backlog/Doing, `✓ 3` reads as "3 completed" — a false claim on screen, against the repo's honesty law. The prototype's row also carried the inline restore hint "… · colapsada (`u` expande)"; the doc's bare `✓ N` drops it, and with the re-key to `z` (PLAN decision log `:108`) the user has no on-screen way to learn the restore key — which matters doubly given B-1.

**Required:** phase-appropriate summary text (e.g. reuse the phase's own glyph/name: `BACKLOG · 3 tasks — z to expand`), and keep an inline key hint in the summary row. Cheap, and it self-documents the exit that B-1 must make real.

---

### m-1 · minor — `z` is the weakest mnemonic of the set; `C` is free

All other keys are strongly mnemonic (`!` matches the on-card `!` marker, `[`/`]` = back/forward, `+`/`-`/`=` due, `u` undo, `S` standup, `s` sort, `g` group, `F` focus). `z` for collapse was a re-key forced by `u`→undo (PLAN `:108`). `C` (uppercase) is unbound in the 30-entry seat and reads "Collapse"; `S`/`F` already set the shifted-key precedent. PDR call; not blocking.

### m-2 · minor — undo domain is under-declared; `u` after a modal edit is a surprise

HLR-010 covers `[` `]` `!` `b` `+` `-` `=` — the right scope, and restoring `phase_changed` (AT-016) is exactly the honesty rule. But: (i) §1.2's out-of-scope line names "modal-driven edits, delete, and purge" — **`a` add-task is not named**, and a user who just added a task may read `u` as "un-add"; (ii) sequence `!` → modal-edit → `u` restores the *priority*, not the edit — correct per spec, surprising per feel. Fix is declarative, not behavioral: name add/edit/delete/purge explicitly in §1.2, and word the README `u` row as the *domain*, e.g. "Undo the last quick-key change (phase move, priority, blocked, due nudge) — not edits, adds, or deletes."

### m-3 · minor — group mode has no header token; sort mode does

HLR-003 requires the header to name the sort mode (`· sort: due`, `:303`); HLR-004 requires no equivalent for grouping — the in-column group headers are the only indicator, and they can be absent (single non-empty group, or shed under width pressure). Asymmetric mode indication for two sibling keys. Cheap fix: `· group: horizon` token on the same header seat as the sort token (LLR-003.2's header already gets touched). Also confirm the header has room for *combined* state (sort token + focus name + WIP tags) at `MIN_COL`.

### m-4 · minor — README rows for the scoped keys must follow the "Kanban only:" convention

`tests/test_keymap.py:272-296` enforces *presence*, not clarity. LLR-012.1 already requires the `escape` row to state its scope (`:601`) — good; extend the same requirement to the `s` `g` `z` `F` rows, matching the existing `Tab` row's wording ("Kanban only: switch between…", `README.md:187`). A first-time reader should learn the mode *cycle* from the row ("cycle column sort: project → priority → due → recent"), not just the key.

### m-5 · minor — new keys fire behind open modals

`check_action` drops only `cursor`/`hmove`/`toggle_presentation` for any stack > 1 (`app.py:206-208`); `BOARD_ACTIONS` members fire while a *modal* (not just the aperture) is up, whenever the focused widget doesn't consume the key. Pre-existing pattern, but nine new keys widen it: `s` pressed with a non-input modal open reshapes the kanban behind the modal invisibly. Consider adding the mode keys to the stack>1 drop clause; at minimum, note it as accepted behavior.

---

## What checks out (verified, not assumed)

- **No key collisions.** All 13 keys + `escape` are absent from the 30-entry seat (`keymap.py:44-80`), from the aperture's bindings (`1-4 t r q/escape/6`, `aperture.py:49-62` — the `escape` overlap is correctly handled by screen-stack shadowing, and AT-019 asserts the aperture's own Esc behavior), and from Textual 8.2.8 defaults (no default bindings on any of these keys; `ctrl+p` command palette and `ctrl+q` are untouched).
- **Aperture contract is complete.** Every new action is slated for `BOARD_ACTIONS` (§3.0 table), and AT-019 drives each of the 13 keys *on the aperture* asserting screen identity + byte-equal board file — exactly the right test for the "hidden board behind the aperture" failure. No new key would act on the hidden board.
- **Mode exits that ARE specified are good:** K2 sort cycles back to default with the header token disappearing (indicator + exit ✓); K8 focus has both cycle-off and `escape`, and the header names the project — the doc *improves* on the approved prototype here (the K8 SVG header shows only `KANBAN · grouped`, no focus name; per §2.5 the document wins, and this is a good deviation — record it in §6.2).
- **K11 standup** closes on `escape`/`q`/`S` (three exits), mutates nothing, has an explicit empty state — clean.
- **Undo restores the stamp** (AT-016) — restoring `phase` without `phase_changed` would fabricate a fresh-looking card; the spec catches it.
- **Modals all bind `escape`** (verified across `modals.py:119-1027`), so the new board-level Esc cannot double-fire while a modal is up.

## Explicitly not covered

- **Real-user evaluation was not performed** (single-operator context of use, §2.3) — this review is inspection with declared criteria plus executed measurements of the real degradation law.
- Visual styling of the new header tokens/WIP tags (not the ux-reviewer's seat; palette choices are cited to existing tones).
- The `prototypes/verify_language.py` latent failures and other out-of-scope carries (§1.2).

## Amendments requested (for §6.5, before Phase 3)

1. **B-1:** rewrite HLR-007's toggle target (cursor column, not selected task) + AT-012's exact restore key sequence; delete the lockout path or specify its exit.
2. **B-2:** record the bar-width resolution in §6.2 (scoping + KEYMAP placement + named discovery seat at glyph-only widths); LLR-012.1's re-measure must include the *placement* rule, not just the constant.
3. **M-1/M-2:** add `views=("kanban",)` for `s g z F` to §3.0 and view-guard Statements to LLR-003.2 / LLR-004 (action) / LLR-007 / LLR-008.1.
4. **M-3:** replace `✓ N` with a phase-honest summary row that includes the restore key hint.
5. **m-2:** name add-task in §1.2's undo out-of-scope; pin the README `u` row's domain wording.
