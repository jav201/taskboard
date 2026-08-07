# Handoff — taskboard widget overhaul

**Next session's job:** rebuild taskboard's screens on the widget architecture, starting clean.
Everything below is settled; nothing here needs re-deciding.

**Start with:** `/tui-design`. Its INTAKE step will ask for a brief — the brief is already written
(below). Confirm it, do not re-interview.

---

## 1. The brief (confirmed, from the previous session)

| | |
|---|---|
| **SUBJECT** | Frameless Textual desktop widget over one JSON at `~/.taskboard/board.json` |
| **JOB** | First 10 s: *is anything urgent?* Once focused: *what's next?* |
| **POSTURE** | **Glanced at** first, operated second. Band **38–120 columns — narrow is the habitat, not the edge case** |
| **GAP** | Four full-screen views behind number keys; equal columns waste ~60% of the screen; 24 flat keybindings; no focus model, no discoverability |
| **DEPTH** | A signal engine: N providers on ≥2 cadences, extensible to external feeds. The aperture is small; what stands behind it is not |
| **FIXED** | Width-1 glyph discipline · `rich.markup.escape` on all untrusted text · lenient model that never raises on load · single-JSON persistence · pipx CLI entry point |
| **LATITUDE** | Break the mould |
| **LANGUAGE** | **Naught** (Nothing-OS lattice), with 7 others switchable |

**The thesis that drove everything:** the README calls taskboard a *"frameless desktop widget"* while
the code is a full-screen dashboard. The surface should read **its own width** and decide what it can
afford to show — not switch views on a number key.

## 2. The skill is ready — use it, don't re-derive it

`~/.claude/skills/tui-design/` was heavily refined in the previous session (13 docs + 2 asset
modules + a calibration script). Load it and follow it; do not rebuild its knowledge.

Most relevant for this work: `INTAKE.md` (step 0) · `LANGUAGES.md` (9 languages + the pixel-base
axis) · `DENSITY.md` (**ink-fraction budget** — new) · `MOTION.md` (three cost classes, the `level=`
contract) · `BUDGET.md` (three pipeline depths; `scripts/cost_probe.py` is mutation-tested) ·
`VERIFY.md` (drive / MOVES / token-mutation checks).

Ready-made, import them rather than re-writing: `assets/pixel_bases.py` (7 bases + 4x7 and 3x5 dot
fonts + seven-segment) and `assets/languages.py` (8 language token sets).

## 3. The prototype — validated, and it is the reference implementation

`<repo>/.claude/worktrees/kanban-variants/prototypes/widget_slice/` — see `RUN.md` at the worktree
root.

    python prototypes\widget_slice\app.py

`engine.py` (6 signal providers, 2 worker groups) · `themes.py` (8 languages, each with a distinct
pixel base) · `bases.py` · `naught.py` · `motion.py` (precomputed frames) · `kanban.py` (card
widgets) · `views_widget.py` (agenda/gantt/swimlanes) · `app.py` · `widget.tcss`

**What it proved:** size-class routing (glance <46 / widget <80 / board) · a drawn hero that renders
rather than labels · cards as real widgets with focus and hover · **navigation derived from the
widget tree** · two cadences in separate worker groups · animation that measurably moves · full
redraw ~650 µs = **4% of a 60fps frame**.

**Verification lives with it and passes:**

    python prototypes\verify_widget.py
    python prototypes\verify_board.py

## 4. The plan — ADD, do not replace

The previous plan said "replace `views.py`". **That is wrong and was corrected.** Measured test
surface:

| file | lines | renderer references |
|---|---|---|
| `tests/test_app.py` | 2,287 | `render_gantt` 14 · `render_kanban` 13 · `render_columns` 10 · `nav_model` 10 · `render_agenda` 8 · `phase_buckets` 2 · `card_cell` 1 |
| `tests/test_flow.py` | 92 | `render_gantt` 4 · `render_view` 3 |
| `tests/test_rescue.py` | 130 | — |

**2,509 lines of tests — roughly twice the size of `views.py`.** Replacing the renderers makes test
rewriting the dominant cost and turns a design job into weeks of work.

**Corrected approach:** the widget architecture lands as **one more view**, alongside the existing
four. `views.py` stays intact and its tests keep passing. Old views retire **one at a time, later**,
each with its own test block, once the new surface demonstrably covers it. This also dissolves the
open "port or absorb Gantt/agenda/swimlanes?" question — they coexist and get compared by running
them.

**Increment 1** (unblocked, mechanical, zero test risk): move `engine.py`, `themes.py`, `bases.py`,
`motion.py`, `naught.py` from the prototype into `taskboard/` as real modules. No change to `app.py`
or `views.py`; the app behaves identically and gains the foundation.

**Increment 2:** the aperture as a new view behind a key, beside the existing four.

Beyond that, decide from evidence, not from plan.

## 5. Constraints in force

- **Nothing committed.** No commits, no push, no PR — the user's standing instruction. `main` is
  untouched at `b3cc60d`; all work is local in the `kanban-variants` worktree.
- **Supervised increments:** propose → wait for approval → ≤5 files → review packet → stop.
- **Language:** Spanish for conversation, English for code and technical artifacts.

## 6. Traps already paid for — do not rediscover these

**Textual/rich**
- `Widget.can_focus` is `False` by default and subclasses inherit it — Tab focuses nothing, **no error**.
- `Binding(group=...)` needs a `Binding.Group` object; a plain string crashes the Footer at render.
- `compose()` runs lazily — children mounted right after `parent.mount(child)` land **before** composed ones.
- `CSS_PATH` resolves relative to the module defining the class; pin it absolutely when subclassing.
- `self.task` on a Widget raises — `MessagePump` owns `task`.
- Arrow keys are eaten by an ancestor `VerticalScroll`; app-level cursor bindings need `priority=True`.
- `Console.capture()` swallows the record buffer, so `export_html()`/`save_svg()` come back **empty**.
- `animate("offset", (x, y))` raises — wrap in `ScalarOffset.from_offset(...)`.
- Block Elements and Box Drawing are **East Asian Ambiguous**; only braille and sextants are width-safe.

**Method — every one of these produced a real defect**
- Build frames from the **widget's own width**, and do width math **before** escaping.
- Budget **rows** as well as columns: an over-tall hero clips mid-glyph or starves the rest off-screen.
- Test at **several widths** (24/40/80/118/200) and assert **content survives**, not only line length.
- A single frame proves nothing about animation — capture several ticks and assert they **differ**.
- Never `except Exception: pass` around a render path; it hid a `NameError` for a whole pass.
- Avoid bash heredocs for Python containing `\n` escapes — it corrupted source three times. Use the
  Write tool.
- **Test-selection bugs outnumbered app bugs.** Three "failures" were the test picking the wrong row
  or shadowing a variable. Verify the probe before believing the verdict.

## 7. Pending — open items carried over

> Also written standalone as **`PENDING.md`** in this worktree, so it survives
> independently of this document.

Nothing here is blocking, but none of it is done. Listed so it is a decision, not an accident.

### Prototype — design debt the previous session flagged on itself

1. **`nord` (20%) and `instrument` (22%) fail the ink-fraction floor** that `DENSITY.md` now
   requires (~35% on a glance surface). Naught and Corgi got the density treatment; these two did
   not. The skill's own rule fails them.
2. **Naught is not yet fully quantized to its lattice.** Still missing: 3x5 dot sprites for
   phase/blocked/done markers in cards and column heads, agenda bars as lit-dot rows rather than
   `━`, and count chips as dot columns. It applies its language to the hero and falls back to plain
   cell text elsewhere.
3. **The hero's dead columns.** At board size the drawn numeral sits in ~100 empty columns. An
   8-week load sparkline through `braille` was proposed and never built — the data is already
   computed every tick.
4. **`action_cycle_size` is one-way.** It sets `self.forced` permanently, so there is no route back
   to automatic width-based sizing — which contradicts the module's own "adapts to its own width"
   thesis.
5. **Dead tokens remain.** Only `base=` got wired. `frame=`, `numbered=`, `dot_w=`, `hero_gap=` are
   still unread metadata — flagged by the very rule added to `LANGUAGES.md` this session.
6. **Minor:** `segmented` imported but unused in `app.py`; `bases.wave` / `from_font` / `render`
   barely used by the app; the `t` binding's tooltip lists 5 languages when there are 8.

### Skill — `~/.claude/skills/tui-design/`

7. **No runnable exemplar screen.** Thirteen documents of vocabulary and zero reference
   implementation. The skill's own "render, don't label" rule applied to itself would demand a
   ~60-line app demonstrating hero + brightness ladder + focus border + curated footer + one
   `level="basic"` animation.
8. **hex vs theme variables never reconciled.** `PALETTE.md` says design 4-6 hex values;
   `NAVIGATION.md`'s example uses `$accent`. Nothing says when tokens should map to Textual's theme
   system versus hardcoded hex — an agent following `PALETTE.md` literally fights the framework.
9. **`SKILL.md.bak`** is a stale leftover in the skill directory (pre-dates this work; left alone
   deliberately).

### Elsewhere

10. **`/html-visualizer` was never touched.** It was deferred in the very first message of the
    session ("dejemos eso para cuando terminemos con TUIs") and the TUI work never ended. Same
    treatment `tui-design` received is still owed to it.
11. **Orphaned `clipboard-fix/` directory** in `<repo>/.claude/worktrees/` — not registered in
    `git worktree list`, left by an earlier session. Not ours; left untouched.

## 8. Suggested skills for the next session

`tui-design` (primary — start here) · `supervised-incremental-development` (the user's workflow gate)
· `review-packet` (mandatory at each increment boundary) · `code-reviewer` or a Fable-model subagent
for an adversarial pass — three such reviews in the previous session each found real defects that
green test suites had missed.
