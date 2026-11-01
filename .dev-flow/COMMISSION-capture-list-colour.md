# Commission — quick capture, the added-order list, multicolour notes

The orchestrator wrote this on 2026-11-01. Branch: `feat/capture-list-colour`, on top of the round `prototypes/capture_round/` (`5c421f8`) and `main` `6705dc0`.

**Process (the operator's order): dev-flow-v3-beta, NOT dev-flow.** The flow is `C:\Users\jjgh8\.claude\skills\dev-flow-v3-beta\SKILL.md`, with stages E1–E5 per increment. The Code-Wire methodology and tools are at `C:\Users\jjgh8\Github\code-wire\` (`docs/Metodologia.md`, `docs/Notation-Grammar.md`, `docs/Review-Method.md`, `tools/codewire_*.py`).

## The operator's verdict (verbatim)

```
D1: de acuerdo   (one global inbox, ~/.taskboard/inbox.json)
D2: de acuerdo   (TF-IDF over normalised words, explained)
D3: de acuerdo   (Task.created; old tasks inferred, never rewritten)
D4: OBJETO · me parece más intuitivo algo como ::b:: para comenzar y :: para cerrar. la b es de blue. ::r:: nota :: eso es para red.
1 capture: A · OBJECIÓN: Me gusta A y C, en su propia vista, enfocada en este block de notas. Podrías hacer un hint para poner 4 guion bajo para hacer la división de la nota, una vez puestos, como hace outlook, se crea una línea que divide claramente los textos. qué opinas? como implementarlo y hacer el hint en la pantalla para que eso no pase desapercibido.
2 list: B · OBJECIÓN: Me gusta la simpleza de B. Me gustaría que tuvieras una columna entre las existentes simplemente con un set de recuadros que representen el estado en el que está (y agregar el toggle de archivar, para que se despliegue o no)
3 colour: B · OBJECIÓN: Creo que quiero combinar B y C.
NOTAS: No uses dev-flow. Usa dev-flow-v3-beta.
```

## Order of increments

There are three increments, run sequentially. Each one is a full E1–E5 pass:

1. **Inc C, colour.** It comes first because the other two render notes through the same tokeniser.
2. **Inc L, the list view.** It brings `Task.created`, which the capture's dump also writes.
3. **Inc K, the capture view.**

## Inc C — multicolour notes (verdict 3: B + C, D4 objection)

- **C-1, the syntax.**
  - A coloured span opens with `::<code>::` and closes with `::`. For example, `::b:: text ::` is blue. The codes are `r` red, `o` orange, `y` yellow, `g` green, `b` blue and `v` violet, in pen order 1–6.
  - The existing `==…==` (yellow), `!!…!!` (red) and `++…++` (green) stay valid. They are the same three tones and are never broken.
  - A span left unclosed at the end of its line closes there.
  - A bare `::` with no span open is literal text, so `std::vector` stays intact. Only `::` + one code letter + `::` opens a span.
  - One tokeniser, `views.highlight_segments`, renders every surface: the board, details, editor preview, presentation, both HTML reports and their exports. The legends list the new colours.
- **C-2, pens (B).**
  - In the task editor's notes, `alt+1`..`alt+6` set the current pen and `alt+0` turns it off.
  - A visible pen chip shows the current pen.
  - Text typed with a pen is wrapped in that span's markers. The editor inserts them; the user never types them.
  - The notes field shows the colour live as you type (the TextArea's highlighting).
- **C-3, the picker (C).** `alt+c` opens a small palette over the selection, or over the word at the cursor when nothing is selected.
  - `1`–`6` pick a colour and `0` removes colour.
  - Every key is direct and shown.
  - It rewrites the markers around that text only.
- **C-4, terminal palette.** The six tones must survive the terminal palette. Check them against the tui-design PALETTE/CEILINGS notes, and the colour-budget tests must hold.

## Inc L — the list view (verdict 2: B + the state column + the archive toggle)

- **L-1, layout.** The view is global, on key `N`, like `A`, `@` and `#`. Its layout is variant B: a narrow list on the left and a detail pane for the cursor's task on the right, as in the round's `list_B` captures.
- **L-2, order.** Tasks appear in the order they were ADDED. A toggle switches between newest first (the default) and oldest first.
- **L-3, the state column.** It is a new column placed between the existing ones. It holds one small box per phase of the task's board, filled up to the task's current phase (for example `■■■□□`); a done task is all filled. It has no text and no hue soup: it is structure, not colour.
- **L-4, archived.** A toggle shows or hides archived tasks. They are hidden by default; when shown, they are dimmed.
- **L-5, `Task.created`.**
  - The field is an ISO datetime, set at EVERY creation path: add, template insert, capture dump, and anything else that creates a `Task`. It is written only when set, so an untouched old board keeps its bytes.
  - Old tasks are inferred, never rewritten. The value comes from a `history.jsonl` creation event, marked `≈`, or else from board-file order, marked `? before <first created date>`.
  - A move between boards keeps `created`.

## Inc K — the capture view (verdict 1: A + C in its own focused view, plus the `____` divider)

- **K-1, the view.** A dedicated full-screen view on key `n`, focused on the notes pad alone. It combines:
  - A's pad with the suggestion rail;
  - C's one-row-per-note review list, opened with `alt+a`. It is the batch review and dump.
- **K-2, the divider (the operator's idea, adopted).**
  - A line holding only 4 or more underscores, `____`, is THE note separator.
  - It renders as a full-width horizontal rule, like Outlook's, the moment `enter` is pressed after it, and the note count updates.
  - Blank lines stay inside a note, so a note can have paragraphs.
  - `alt+enter` inserts a divider directly.
  - The hint is never missed:
    - an always-visible hint row in the view reads `____ ↵ new note · alt+↵ divider`;
    - the empty pad shows a ghost example with a drawn rule;
    - the first time a divider is made, a one-time notice explains it.
- **K-3, suggestions (D2).**
  - TF-IDF over normalised words, as in `prototypes/capture_round/suggest.py`.
  - Each project's text is weighted: name ×3, task titles ×2, `@people` ×2, mark names ×1, notes ×1.
  - A score that rests on a single shared word is halved.
  - Below the medium cut, the suggestion is "+ new project".
  - Ties break on board order, then on name.
  - The rail shows the top suggestion plus up to 2 alternatives, with the matched words as the "why".
  - It reads all boards, and each suggestion carries its board chip.
- **K-4, dump.**
  - `alt+d` dumps the note under the cursor to the suggestion. `alt+o` cycles the alternatives. `alt+n` creates a new project inline, on the current board or a chosen one.
  - The task's title is the note's first line and its notes are the rest. Images, `@mentions` and colour spans carry over. `created` is set.
  - A dumped note leaves the pad. `u` undoes the last dump, and dumped notes are kept for 7 days in `inbox.json` under `dumped`.
- **K-5, the store (D1).** `~/.taskboard/inbox.json` is written exactly like `people.json`: read-modify-write under `boards.file_lock`, atomic, and set aside with `keep_aside` when unreadable. The fresh re-read pattern from batch `2026-10-24-batch-02` applies.
- **K-6, images.** `alt+i` attaches an image to the note under the cursor, as the task editor does. On dump the image moves into the target board's `images/`.

## Standing rules (all increments)

- **Keys.** Every modal button gets a direct, shown key; inside text fields, use `alt+letter` (the modal-key law). Check that keys are free in `taskboard/keymap.py`.
- **Captures.** Real Windows Terminal captures of each shipped item, at 118x30 and 80x24, for E13.
  - Launch with `cmd /c 'set NO_COLOR=& set COLORTERM=truecolor& wt.exe -w new --title <unique cpi-…> ...'`.
  - Close each window by title right after its shot, verify it is gone, and assert at the end that none remains.
  - NEVER close any other window (`JJ_WORKPC: dev-flow`).
  - Reject black shots and shots with fewer than 8 colours.
- **Tests.**
  - Run every test with `env -u NO_COLOR python -m pytest`.
  - Print `taskboard.__file__` in every transcript header.
  - RED runs with cwd = the base tree; GREEN runs with cwd = the worktree.
- **Data.** Synthetic only. Never the operator's real name (placeholder `username_subject`). No secrets.
- **Batch end.** The full suite runs ONCE, in 3 sequential chunks (baseline 3365 passed on Windows; skip allowed only for TC-1902). Then the operator gets one review page, push only on approval, and the GitHub CI run is checked after the push.
