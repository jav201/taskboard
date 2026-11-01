# Prototype brief — quick capture, the list view, multicolour notes

Written by the orchestrator on 2026-10-31. Branch `proto/capture-list-colour`, from `main` `6705dc0`.

## The operator's words (verbatim)

> «Me di cuenta de algo... para hacer una tarea el tiempo que se toma hacer el setup es ya considerable..., hay veces que estoy tomando notas y sólo puedo hacer como en un scratchpad y después ya no vuelvo la información al taskboard... será que haya una manera más sencilla de simplemente escribir, volcar imágenes y tener una especie de parser (o usar un ngram o por similitud de palabras, algo determinista) para que según las notas me sugiera volcar la información a un task de un proyecto? (es decir que el autocompletador ya me sugiera el proyecto donde pertenece, si no, crear uno nuevo ahí mismo) ya me lo imagino como una lista de notas random, divididas por línea (para separar tópicos) y tener la opción de volcar... y veo que me hace falta también una vista de lista precisamente, donde vea las tareas pero como se fueron agregando, no por las fechas dispuestas de planeación, donde vea toda la información... y me gustaría que las notas acepten color... que sea fácil de hacer ese cambio, para tener el texto multicolor, eso es algo que uso en mis cuadernos.»

## Three items, one round

Each item gets real-app renders at 118x30 and 80x24: the current state plus 2–3 radically different variants.

### 1. Quick capture: a scratchpad that turns into tasks

- **The posture.** It is used during a meeting or while thinking. Typing has to start with ONE key and zero setup, with no dialog to fill in first.
- **The surface.** A free-text capture pad.
  - A blank line, or any line break, separates topics. Each topic is a note.
  - Images can be dropped in: paste from the clipboard or give a path. Reuse how the task editor attaches images today (`alt+i`, `images/`).
  - The pad persists. Decide whether there is one global inbox (`~/.taskboard/inbox.json`, like `people.json`/`marks.json`) or one per board, and recommend one.
- **Suggestions: deterministic, no AI, no network.** For each note, suggest the project it belongs to and show WHY, meaning the words that matched.
  - Candidate method: TF-IDF or character n-gram similarity of the note against each project's name and its tasks' titles, notes, `@people` and mark names, across all boards (the board chip shows where).
  - The method must be explainable, fast, and stable: the same input gives the same suggestion.
  - Show the top suggestion plus 1–2 alternatives with a confidence cue. When nothing scores, the suggestion is "new project".
- **Dumping ("volcar") a note.** One key turns a note into a task in the suggested project.
  - The first line becomes the title. The rest becomes the notes. Images, `@mentions` and highlights are carried over.
  - Accept, pick an alternative, or type a new project name. That creates the project right there, on the current board or a chosen board.
  - A dumped note leaves the pad. Decide between moving it to a "dumped" fold and removing it, and keep undo either way.
  - A batch action dumps all notes with their suggestions after a review pass.
- **Keys.** Follow the standing standard: every modal button has a direct, shown key, and fields with text use `alt+letter`. Check `taskboard/keymap.py` for free keys. Candidates: `N` (note) or `i` (inbox), plus a view number.

### 2. The list view: tasks in the order they were added

- **The view.** A flat list of every task in the order it was ADDED, newest first or oldest first (a toggle). It is not ordered by planned dates.
- **Content.** Each row shows all the information: title, project and board chip, phase, priority, dates, milestone mark, `@people`, a notes excerpt, links and attachments. Choose one of two designs:
  - expandable rows, where `enter` or `space` shows the full note inline;
  - a detail pane.
- **Creation order is NOT stored today.** `Task` has no created timestamp (`taskboard/models.py` ~line 869).
  - Propose adding `created` (an ISO datetime), written only when set.
  - Existing tasks have no `created`. Infer their order from `history.jsonl` creation events where they exist, else from board file order, which is append order. Mark the inferred ones honestly ("added: unknown, before Oct 31").
  - Show how that reads.
- **Key.** Propose a view key. `1`–`0` are taken (`7` flow, `8` standup, `9` people, `0` setup). Check the free keys and say how the list joins the view cycle.

### 3. Multicolour notes

- **Today.** Notes support `==yellow==`, `!!red!!` and `++green++` highlights (`views.highlight_segments`), rendered in the board, the details, the presentation and the HTML reports.
- **The ask.** Changing colour must be EASY while typing, like switching pens in a notebook.
- **Variants to prototype:**
  - (A) more marker pairs for blue, violet and so on, plus a key that wraps the selection or the current word;
  - (B) a "pen" palette in the editor: `alt+1..6` sets the current pen, typed text takes that colour, and a pen chip shows the current one;
  - (C) a colour picker on the selection.
- **Storage.** It stays plain-text friendly. Prefer markers that degrade readably, so a note stays readable outside taskboard.
- **One tokeniser.** Every surface renders the colours the same way: board, details, presentation, HTML reports and their exports. `highlight_segments` stays the one tokeniser.
- **Colours.** They must survive the terminal palette. See the tui-design skill's PALETTE/CEILINGS notes.

## Decisions to put on the page (with consequences)

- **D1.** Inbox global vs per board.
- **D2.** The suggestion method, and what it reads.
- **D3.** `created`: the new field, and the inference for old tasks.
- **D4.** Colour storage syntax.

## Rules

- **Design discipline.** Follow the tui-design skill (`C:\Users\jjgh8\.claude\skills\tui-design\SKILL.md` + `PROTOTYPE.md`) and html-visualizer (genre A) for the page.
- **Model.** Use `prototypes/milestone_marks/` and `prototypes/people_round/`: their `proto.py` scenes, real Windows Terminal capture harness and verdict page.
- **Captures.** Real full-colour Windows Terminal PNGs.
  - Launch with `cmd /c 'set NO_COLOR=& set COLORTERM=truecolor& wt.exe -w new --title <unique cp-…> ...'`.
  - Close each window by title right after its shot and verify it is gone. At the end, assert that no `cp-*` window remains.
  - NEVER close any other window (`JJ_WORKPC: dev-flow` is the operator's).
  - Reject black shots, shots with fewer than 8 colours, and shots in the wrong end state.
- **Page.** `prototypes/capture_round/capture-round.html`.
  - Spanish prose, English UI strings.
  - BLUF at the top.
  - Per item: the captures, the plain-Spanish consequence before/after, and a recommendation.
  - D1–D4 each with an objection field.
  - Per item: «Elijo esta» plus an objection field.
  - A GENERAL NOTES field.
  - An «Exportar respuestas» button that copies text and JSON.
  - 0 console errors, then open the page with `Start-Process`.
- **Data.** Synthetic only. Never the operator's real name (placeholder `username_subject`).
- **Scope.** Nothing under `taskboard/` changes; the prototype wraps or forks the app inside `prototypes/capture_round/`.
- **Tests.** `env -u NO_COLOR` for pytest. Do not run the full suite.
