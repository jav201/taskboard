# PROTOTYPE round — components: six canonical screens × five languages

> Operator decision 2026-09-04 (Javier): *"mejorar los lenguajes de diseño con base en taskboard y otras
> aplicaciones comunes, teniendo como objetivo tener elementos para UI/UX"* → "Dale, haz la planeación y
> delega la ejecución." This is the **prototype round** the tui-design rule requires before any design
> implementation: real renders, a packet, the operator's verdict; **no kit code changes ship from this round**.
> Worktree: `taskboard/.claude/worktrees/kanban-variants` (the eleven kits live in `taskboard/language.py`).

## 0. Why this round, and why it is not the one that was stopped

The round stopped on 2026-09-04 morning put five languages on ONE screen (the physics lab) — variations of skin
on a single case. This one puts FIVE languages on SIX screens that every terminal app needs, so each language
has to *implement* the components a real interface uses, not evoke them. Evidence that this is where the
languages are thin: every limit a real consumer produced this week was a UI element — Corgi had no notation for
a passive readout (L-33) and dropped its display legend (kits-learn-2); Blueprint could not draw an axis or a
series (L-34) and needed `stamp()`/`series()`; Prism's tint lost the label (L-31); the title block fell outside
its domain (L-32). `COMPONENTS.md` in the skill has the interaction inventory and the state matrix, but almost
no frames that prove a language can render them.

## 1. The six screens (mock content, fixed across languages so frames are comparable)

| id | screen | components it forces | states to show |
| --- | --- | --- | --- |
| S1 | **List + detail** — the taskboard board itself: columns of cards, one selected, a detail pane | list, selection, focus ring, scroll indicator, detail header | selected · focused · empty column |
| S2 | **Form with validation** — "new task": title, due date, priority (radio), tags (multi), notes (textarea), Save/Cancel | inputs, radio/checkbox group, inline error, required marker, primary vs secondary button | invalid field with message · disabled Save · focused input with cursor |
| S3 | **Settings** — five switches, two selects, one slider, a danger zone | switch on/off, select closed/open, slider with value, destructive action | one switch disabled · select open · slider at 70 % |
| S4 | **Modal dialog** — "delete 3 tasks?" over S1, with confirm/cancel | overlay dimming or not (the language decides), focus trap, default button | dialog focused · background visibly inactive |
| S5 | **Live monitor / log** — a streaming log with levels, a sparkline, a rate readout | log rows with levels, tail marker, sparkline, passive readout, timestamp column | one ERROR row · paused state · readout labelled (L-33) |
| S6 | **Command palette** — "> " query with 6 results, one highlighted, hints | search input, result list with match highlight, key hints, empty state | 2-char query with matches · no-match state |

Terminal size for every frame: **100×32**. Same mock data across all languages (write it once in a fixture).

## 2. The five languages, and why these

Corgi Engineering, Blueprint, Prism (each has a real consumer and measured debt), Naught and Ledger (the two
most different from each other and from the first three; they force decisions the others never take — Naught
refuses ornament, Ledger is a lattice). The other six inherit after the verdict.

## 3. What the prototype must do — and must not

- **Render through the kit** (`Kit` primitives, the surface registry, the same headless compositor path
  `prototypes/capture_languages.py` uses) so every frame is what the kit can do today. Output per frame:
  `prototypes/components/<lang>_<S>.txt` (cell grid) + `.svg` (via the existing renderer) — **30 frames**.
- **Where a kit lacks a primitive, the prototype draws the candidate** inside the frame **and marks it**: a
  sidecar `prototypes/components/<lang>_<S>.candidates.md` listing each drawn-by-hand element, the primitive
  it proposes (name, signature, what the language's commitment says it must look like), and whether it is
  *implemented*, *evoked* (looks right, no mechanism), or *refused* (the language's answer is "no", with the
  reason — refusals are design, L-33 is one). No hand-drawn element ships unmarked.
- **No changes to `taskboard/language.py` or any kit** in this round. Scratch code lives under
  `prototypes/components/` only. Tests of the worktree stay green and untouched (`python -X utf8 -m pytest -q`,
  341 passed baseline).
- **Real renders, not descriptions.** Each SVG is the deliverable; the packet points at them. If a screen cannot
  be rendered in a language with what exists, the frame shows what CAN be rendered and the candidates file says
  what is missing — that is a finding, not a failure.

## 4. The packet — `prototypes/components/PROTOTYPE.md`

For the operator's verdict, in Spanish, ≤ 2 pages of prose plus the 30 frames linked:

1. **Matriz 6 × 5**: por celda, un veredicto propuesto: `implementa` / `evoca` / `rehúsa` / `falta`, con el
   elemento concreto que lo decide.
2. **Por lenguaje**: qué primitivas nuevas propone (nombre, firma, compromiso del lenguaje que debe cumplir),
   qué rehúsa y por qué, y qué ya tenía y bastó.
3. **Por pantalla**: qué componente resultó más difícil en más lenguajes (eso es lo que va primero al
   COMPONENTS.md del skill).
4. **Preguntas para el veredicto**, cerradas: "¿Corgi numera los botones de un formulario o los etiqueta?",
   "¿Naught dibuja un overlay para el modal o sólo cambia el foco?", etc. Máximo diez.
5. **Plan de implementación propuesto** (no ejecutado): incrementos por kit, ≤ 4 archivos cada uno, cada uno con
   test de propiedad y captura antes del commit; luego exportación al skill (`export_to_skill.py`) y frames a la
   galería con su línea Limit.

## 5. Acceptance for the round

- [ ] 30 `.txt` + 30 `.svg` frames exist, 100×32, rendered through the kit path; every hand-drawn element is in
  a `.candidates.md`.
- [ ] `PROTOTYPE.md` has the 6×5 matrix, per-language primitives, per-screen difficulty, ≤ 10 closed questions,
  the implementation plan.
- [ ] Worktree suite unchanged and green; `git status` shows only `prototypes/components/` and this file.
- [ ] The capture hygiene rules hold if any real terminal window is opened (title, DPI, WM_CLOSE, never a kill);
  headless stdout to a file, never DEVNULL (L-42).

## 6. After the verdict (not this round)

Implementation batch `kits-learn-3` in this worktree: only the cells the operator approved; each increment
produces its capture before commit; export to the skill; gallery frames with Limit lines; COMPONENTS.md gains
the frames it lacks. Then the six remaining languages.
