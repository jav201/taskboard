# Review — taskboard — Batch 2026-10-04-batch-01

> Phase 2 artifact (flow `templates/review-template.md`). Reviewers in parallel, each spawned as an
> independent sub-agent on the pinned snapshot's `agents/<role>.md`: `architect` ∥ `qa-reviewer` ∥
> `security-reviewer` (family C) ∥ `ux-reviewer` (family D). Their probes ran on synthetic boards in
> the session scratchpad (`qa-p2/`, `arch-p2/`, `secp2/`, `uxprobe/`); no repo file was changed.

## ✅ Verdict (read first) — iteration 1

- **Gate:** `iterate-to-refine` → Phase 1 (2 blockers: Q-1, A-1). **No HIGH**: security PASS-WITH-NOTES with 8 MEDIUM — the batch is not stopped; the fold is self-approved under the standing authorization and every disposition is recorded below.
- **Out-of-scope findings:** 3 named and routed (S-6, S-13, S-7's setup-view branch) → `BACKLOG.md` at close.
- **Findings:** 2 blocker · 33 major · 31 minor (architect 1/6/7, qa 1/10/6, security 0/8/5 as MEDIUM/LOW, ux 0/9/13).
- **shall/should check:** ✓ clean (architect and qa: `grep -n should 01-requirements.md` → 0 in statements).
- **Two-layer (blockers):** ✓ every story has an `AT`; ✗ Q-1: the ATs' board would be migrated at mount, so HLR-501..504's thresholds are unreachable as written.
- **Census (change-first):** best-effort + gate-confirmed; extended by Q-1 (every `TaskboardApp(` starter over a board with links), Q-5 (card callers derived), Q-11 (README + keymap tests), A-6 (every `blocked` consumer).
- **Security:** ⚠ 13 findings (8 MEDIUM, 5 LOW), 0 HIGH.
- **Evidence checklists:** ✓ all four reviewers attached theirs (in their verdicts, summarised below).

## Detail

### Findings and dispositions (iteration 1)

Every disposition below is an autonomous decision recorded under the standing authorization (D-515..D-532 in `01-requirements.md` §6.2). "Folded" = written into the iteration-2 contract.

| ID | Reviewer | Sev | Req | What | Disposition |
|---|---|---|---|---|---|
| A-1 | architect | blocker | LLR-502.1, LLR-504.1 | TC-507 owned twice | Folded: the guard's TC is TC-517 |
| Q-1 | qa | blocker | HLR-505 vs §5 | the kg board has no migration mark: mount would migrate it (8 tasks change) | Folded: every non-migration board carries the mark through ONE fixture seam (`kg_board.build` marks its board — it is new-model data); only the migration ATs start unmarked; the migration increment reverse-censuses every `TaskboardApp(` starter over a board with links or a blocked task |
| A-2 | architect | major | LLR-505.1 | the last-id rule misreads a blocked flag set by the editor after its last link closed | Folded (D-515): a blocked task whose last live id points at a CLOSED task keeps the flag (logged "kept — its last link is done"); flagged for the operator as a provisional ruling |
| A-3 | architect | major | LLR-501.1, LLR-505.1 | the shipped `b` can write a 2-cycle; migration keeps it | Folded (D-516): a current blocker whose kept link would close a loop over links already kept is dropped and the flag kept (logged); every derivation terminates on a cyclic stored graph (seen sets), TC arm |
| A-4 / S-12 | architect, security | major / LOW | HLR-505, D-511 | revert semantics: after `u` the mark stays, old links read under the new meaning; restoring the backup re-migrates | Folded (D-517): `u` restores every changed task exactly and leaves the mark at 1 (the migration never re-runs on its own — the operator's "never runs twice"); its toast says the old links now read as waits; restoring the backup file brings back the pre-migration board and, being unmarked, it migrates again at the next start — stated in the toast-free docs (README) and the log. Flagged for the operator as a provisional ruling |
| A-5 | architect | major | LLR-505.2 | after a failed backup the session edits unmigrated data under the new rules | Folded (D-518): fail closed — a failed backup or log write leaves the file untouched and the app exits with a one-line reason (basename + `strerror`) |
| A-6 | architect | major | HLR-501 | every `blocked` consumer changes meaning | Folded (D-519): `▲`, lanes `▲`, sorts' blocked-first and the legend stay on the external flag; `_flowing` (the in-progress packet) also stops for a waiting task (a waiting task was always `blocked` before the migration, so its motion is unchanged); symbols declared for the reverse census |
| A-7 | architect | major | PLAN | increment order not dependency-safe | Folded: the migration becomes increment 001 (models + app), then semantics (002), `L` + details (003), gantt link mode (004) |
| A-8 / S-2 / Q-2 | architect, security, qa | minor / MEDIUM / major | LLR-505.3 | `on_mount` saves before the migration could run (renumber, sweep, team init) | Folded: the migration is the first statement of `on_mount`, the session's first board write; the AT board lacks the renumber key and holds an old done task so a wrong order goes RED; threshold "exactly one toast starting `Links migrated`" |
| A-9 / S-3 / Q-15 | all three | minor / MEDIUM / minor | LLR-505.2 | only the backup is protected; log overwrite, failed log or save, in-place truncating save, symlink at the name | Folded (D-520): order backup → log → apply + mark → atomic save; backup and log by exclusive create (`'xb'`), numbered names, never overwrite (a dangling symlink counts as taken); the save writes a temp file then `os.replace`; any failure undoes the in-memory changes, leaves the file unmarked and fails closed (D-518); TCs for a failing log and a failing save |
| A-10 / UX-8 | architect, ux | minor / major | LLR-503.1, LLR-502.3 | no-start waiter: conflict wording and `═` cells undefined | Folded: "◂ due ‹date›, overlaps ‹pred› by Nd (due ‹date›)"; no `═` cells for a waiter with no start (the hint row states the overlap) |
| A-11 / S-8 | architect, security | minor / MEDIUM | LLR-501.2 etc. | teammates' tasks never excluded explicitly | Folded: marks, guard, candidates, loops and the migration read `board.tasks` only; a task not in the board (a teammate's) paints no mark; TC arm with a foreign task depending on a local id |
| A-12 | architect | minor | LLR-504.1 | editor: phase-then-archive order | Folded: judged after the edited phase is applied |
| A-13 | architect | minor | LLR-501.1 | `dependents_chain` domain | Folded: open tasks only, each once (seen set) |
| A-14 | architect | minor | §6.3 | an older app version on a marked board writes legacy shapes again | Folded as an accepted risk in §6.3 |
| S-1 | security | MEDIUM | LLR-505.2 | backup/log names match team pull's `board.*.json` | Folded (D-521): `<board file name>.pre-links-migration[.N]` and `<board file name>.links-migration-log[.N]` (suffix after the full name, as `.corrupt`); TC: a pull over a folder holding them sees no extra user |
| S-4 | security | MEDIUM | LLR-505.2 | a malformed mark crashes startup | Folded: marked ⇔ `settings["migrations"]` is a dict whose `links` is exactly 1; any other value is unmarked and replaced (the old value logged); TCs list / str / `links: 0` |
| S-5 | security | MEDIUM | LLR-501.1, 502.2/.3 | no cost bound: linear lookups, path copying | Folded (D-522): one id dict per derivation; iterative searches marking visited before push with parent pointers; the picker's loop set computed once per open (one reverse-reachability pass from the waiter); hostile-board TC (chain 5000, one task with 100k ids, dense 800): each derivation < 1 s, no `RecursionError` |
| S-6 | security | MEDIUM (existing) | — | `critical_chain` recursion and exponential cost | Routed to `BACKLOG.md` (pre-existing seat, not this batch's requirement); named in §6.3; security re-reads it at close |
| S-7 / Q-10 | security, qa | MEDIUM / major | HLR-504 | the project archive archives open predecessors; `d` checked only before its confirm; setup-view `x` | Folded: every archive/delete path listed — `x`, `d` (checked before the confirm and again in `_on_delete`), the editor, the project archive (refused naming the outside waiters, D-523); sweep and `X` (done only) and project delete (tasks to the Inbox) exempt. The setup-view `x` branch is pre-existing → BACKLOG |
| S-9 | security | LOW | LLR-502.3 | link-mode status rows lack the S1 clause | Folded: built as Text pieces in `modals.py` (census-visible); one EXEMPT entry for the gantt frame repaint (the views seat, D-405) named in the LLR; S1 payloads in AT-503; a created task's title goes through `strip_controls` and must be non-empty |
| S-10 / UX-14 | security, ux | LOW / minor | LLR-504.1, 502.1 | unbounded toast text; `task(s)` | Folded: titles clipped to 40, at most 3 names + "and N more", a long loop path shortened in the middle; real singular/plural |
| S-11 | security | LOW | LLR-505.3 | full paths in toasts | Folded: basename and `strerror` only |
| S-13 | security | LOW (existing) | HLR-505 | an unreadable board is saved over by renumber | Folded: the migration does nothing on an unreadable file; the existing behaviour routed to BACKLOG |
| Q-3 | qa | major | ATs | fixed fixture dates vs `date.today()`: the done predecessor gets swept | Folded: the AT boards are the kg board shifted by `date.today() − TODAY` (every date and `phase_changed`), one helper |
| Q-4 | qa | major | HLR-501 | one 118×30 frame cannot see every card; shed order incomplete | Folded: the AT counts marks at a height where every band fits (measured at P3, guarded: cards observed = open tasks); shed order fixed in full: `↗`, `▤`, age, tag, `▸`, `◂`, due |
| Q-5 | qa | major | LLR-501.2 | card callers hand-listed; lanes not driven | Folded: the TC derives the callers (AST, guard ≥ 4) and AT-501 cycles to lanes |
| Q-6 / Q-17 | qa | major / minor | LLR-501.1, 502.2, 503.1 | the three tables are referenced, not written; the state set undeclared | Folded: the tables are pasted into §5 (generated by `evidence/p1_tables.py` over the kg board with the prototype's rule functions); the session states listed |
| Q-7 | qa | major | TC-509 | only 3 of 6 hint branches reachable from `tw5` | Folded: waiters `tw5`, `ta2` (no start), `to4` (no dates); every hint text asserted (derived set, guard == 6) |
| Q-8 / UX-6 | qa, ux | major | LLR-502.3 | 0 loop candidates for `tw5`; N unpinned; linked candidate undefined | Folded: precondition "`SEO redirects map` waits on `Launch new homepage`" (⟲1); N = open tasks but the waiter (24); a linked candidate shows "✓ linked · ↵ unlink"; the `═` count uses the unlinked pair `tw5`/`tm3` |
| Q-9 | qa | major | HLR-505 | one AT for five branches; no fault-injection seam | Folded: AT-506 (change, revert, restart), AT-507 (no change), AT-508 (backup fails, fault injected at the OS boundary: the stdlib open/copy, never a product symbol); the backup name pre-created in AT-506 |
| Q-11 | qa | major | LLR-502.1 | `L` turns the README/keymap test RED; README describes `b` and `⛓` | Folded: LLR-502.4 (README key row, `b`'s meaning, the dependencies section); `test_readme.py`, `test_keymap.py` in the reverse census |
| Q-12 | qa | minor | D-503 | rule 9′'s boundary changed by an implementation note | Folded as PV-7 (the operator's visual verdict) |
| Q-13 | qa | minor | LLR-503.1 | "K in chain" includes direct?; `x` on an Unblocks row | Folded: K counts direct + chain (2 for `tm3`); AT-504 arm `x` on `Offline sync` |
| Q-14 / UX-10 | qa, ux | minor / major | LLR-502.2 | create branch and start highlight unspecified | Folded: highlight starts on the first candidate; empty filter → a title prompt; the new task is in the waiter's project, first phase, no dates; `u` removes the link, the created task stays (said in its toast) |
| Q-16 | qa | minor | several | undo silent arm; `‹name>` typo; `L` with nothing selected; AT-502 persistence; rename/delete into the last phase | Folded: arms added; typo fixed; `L` with no selection is a no-op; AT-502 re-reads the file; phase rename/delete gives no ready toast (D-524) |
| UX-1 / UX-2 | ux | major | LLR-503.1 | focus and the keys line in the details | Folded (D-525): the box keeps focus (arrows scroll as today); `tab` moves focus to the links list and back; `x`/`↵` act on the highlighted link; the keys go in the title row: "L link · tab links · x remove · ↵ jump · o open raw · esc close" (`tab`/`x`/`↵` only when a direct row exists) |
| UX-3 / UX-21 | ux | major / minor | LLR-502.1 | `L` invisible at 80 cols; live in setup | Folded: `L` in the primary layer of group `task`, views lanes, agenda, gantt, kanban, focus; threshold: painted in the key bar at 80×24 in kanban and gantt, any other key it pushes off counted in the reverse census |
| UX-4 | ux | major | LLR-502.3 | link-mode filter invisible | Folded: the LINK row echoes "filter: ‹text›▏"; backspace edits; no match → "no match", `↵` a no-op; every printable key is filter text in link mode |
| UX-5 | ux | major | LLR-502.3 | loop rows unmarked in the gantt | Folded: `⟲` in the loop rows' gutter and a legend line "⟲ loop: ‹path›" for the first loop |
| UX-7 | ux | major | LLR-502.3 | cursor on hidden rows; start candidate | Folded: the candidate is the gantt's selection, so its group unfolds; the start is the first non-loop candidate in gantt order |
| UX-9 / UX-13 | ux | major / minor | LLR-505.3, 502.1 | migration toast too long and short-lived; no undo hint on link toasts | Folded: "Links migrated: N tasks · backup ‹name› · u undo" with a 30 s timeout; link/unlink toasts end " · u undo" |
| UX-11 / UX-12 | ux | minor | LLR-502.2, D-503 | linked row drops timing; "due Nd after" a second measure wording | Folded: the linked row keeps its timing hint; one wording "◂ overlaps Nd: …" |
| UX-15 / UX-16 / UX-17 / UX-18 | ux | minor | LLR-504.1, 501.4, 503.1 | editor refusal, toast flood, `L` discoverability, jump to a hidden task | Folded: "— other changes saved"; at most 3 ready toasts then "+K more ready"; the kanban help names `L`; the jump clears focus and search, and an archived target with archived hidden says "‹title› is archived — v shows it" |
| UX-19 / UX-20 / UX-22 | ux | minor | LLR-502.3, ATs, PV-1 | 80-col status rows; colour claims need painted styles; `◂`'s four meanings | Folded: keys never dropped, titles clipped first; colour asserted from painted segments; the overlap of `◂` recorded under PV-1 |

### Security review summary
PASS-WITH-NOTES, 0 HIGH (8 MEDIUM, 5 LOW). Every MEDIUM is `planned` in the iteration-2 contract and re-verified by the reviewer at its increment gate; S-6 and S-13 are pre-existing and routed.

### Evidence checklists — architect · qa-reviewer · security-reviewer · ux-reviewer
- architect: derivation, `shall`, model soundness, increment order — ✓ attached in the verdict (files reviewed listed).
- qa-reviewer: plan-mode checklist — expected values ✗ (Q-6, Q-8), branch ATs ✗ (Q-7, Q-9), reachability ✗ (Q-5, Q-10), placeholders ✗ (Q-6); all folded.
- security-reviewer: each finding with what/where/why/fold ✓, severity ✓, no secret ✓, explicit verdict ✓, no new tool ✓.
- ux-reviewer: expert inspection against the frames, 3 probes; criteria `planned` (walkthrough at P4).

## Iteration 2 (2026-10-04) — the same four lenses re-read their findings

**Gate: `approve` → Phase 3** under the standing authorization. qa PASS-WITH-NOTES (17/17 discharged; tables re-executed identical, sha256 `0583fb00…`), architect PASS-WITH-NOTES (14/14, A-2 partial → A2-1; D-517 pending the operator), security PASS-WITH-NOTES (13/13 closed or routed at requirement level, every fold `planned` until its increment; 0 HIGH), ux PASS-WITH-NOTES (9/9 majors; UX-14 partial, UX-22). 0 blocker, 0 major, 16 new minors, all folded at the gate (LED .11):

| ID | Reviewer | Fold |
|---|---|---|
| A2-1 | architect | the unresolvable case (flag set after a release to a still-open task) named in §6.3; its log note "flag cleared — press b if this was an outside block" |
| A2-2 | architect | every kept link checked for a loop over the links already kept (not only open blockers); TC-514 arm |
| A2-3 | architect | `b` = external block moves into increment 001 (`app.py` is already there); 001 and 002 land in one commit anyway (the coordinator commits after the batch) |
| A2-4 | architect | "last stored id" throughout LLR-505.1 |
| A2-5 / S2-1 | architect, security | the board path resolved once; backup, log and `<board file name>.tmp-links-migration` beside the resolved file; temp removed on failure; a symlinked-board TC (skipped where symlinks are unavailable, declared) |
| S2-2 | security | a replaced malformed mark forces the backup and log |
| S2-3 / UX2-3 | security, ux | fail closed kept (decision: exit rather than open unmigrated, D-518); the exit message, printed after the terminal is restored, names the way out without a path; README too |
| UX-14 / UX-22 | ux | real plurals in the migration toast; PV-1's row names `◂`'s other meanings |
| UX2-1 / UX2-2 | ux | the details keys on their own row under the title, all painted at 80×24; `tab` reaches `#deps-list` and back with the board layout unchanged |
| Q2-1 | qa | measured now: every band drawn from 33 rows grouped, 20 lanes (`evidence/p2-kanban-height.txt`); the AT runs at 118×40 |
| Q2-2 | qa | AT-508 patches `open` to raise only for names holding `.pre-links-migration`, and reads the app's exit message |
| Q2-3 | qa | "no `Links migrated` toast" |
| Q2-4 | qa | the ATs compare order, counts and day counts; date text only in the TCs over the unshifted board; TC-513's `tw5` row has no precondition |
| Q2-5 | qa | the increment landing the `kg_board` mark reverse-greps its users that compare settings or saved bytes |
