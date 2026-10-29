# Commission: the HTML reports exported from the app (variants B + C)

The orchestrator wrote this on 2026-10-29 for batch `2026-10-29-batch-01`. Branch `feat/html-report` holds the prototype round `prototypes/html_report/` (commit `65deb62`) on top of `main` `9cc7d4e`.

## The operator's words (verbatim)

The request:

> «Otra cosa fue el export en SVG, creí que sería más fácil usarlo y manipularlo pero no fue así, quiero que prototipes un reporte con funcionalidad expandida en html que se exporte de la app.»

The verdict on `prototypes/html_report/html-report-round.html`, 2026-10-29:

```
Variante A: no elegida
Variante B: ELEGIDA
Variante C: ELEGIDA
Recomendación general (B, H global, todos los boards, convive con SVG): no confirmada (no objection)
Notas generales: Me gusta la variante B, pero también quisiera tener disponible la variante C que es más concisa.
Ahora, los reportes son bastante completos, pero dentro del html me gustaría que mejoraras los controles para el display y filtro de información y de proyectos... Además de una opción dentro del mismo reporte para exportar la vista (como se ha configurado con los controles dentro del reporte) a PDF. Esto porque no siempre queremos mandar toda la información a distintas personas, esa flexibilidad quiero que persista pero con la opción de consolidar un reporte de una vista para enviar como archivo consolidado.
```

Then: «decide cómo continuar, con opus o sonnet» (Kimi is out of tokens).

## The design

The design is the round itself. Read:

- `prototypes/html_report/variant_b/` and `variant_c/` (`build.py`, `NOTES.md`);
- the generated `out/b-report.html` and `out/c-report.html`.

Port them into the app. Do not reinvent them.

## Decisions (record each one in the plan)

- **HR-1. Two reports from one extraction.**
  - B, the "workspace", is the interactive one: gantt, filters, search, table, notes, embedded JSON, and CSV/JSON download.
  - C, the "deck", is the concise one: vector slides, arrow keys to page through them.
  - Both are built from ONE data extraction (`taskboard/report.py`, or a new `taskboard/report_html.py`), so they cannot disagree on the board's facts.
  - The old CLI report (`taskboard --report`) keeps working. Either it becomes variant B or it stays as it is. Decide, and say why.
- **HR-2. The export key.**
  - The round recommended `H` as a global key (outside `R`) that exports all loaded boards. The operator did not object, so it stands. Check that `H` is free in `taskboard/keymap.py`.
  - `H` opens a small modal. Following the standing standard, every key is direct and shown on screen:
    - `b` workspace, `c` deck, `a` both;
    - scope: `p` the current project, or `o` all boards (take the default from the round);
    - `esc` closes it.
  - Files land in `<board dir>/reports/`, named with the date and the variant.
  - A toast names the path and offers `o` to open the file in the browser with the OS default handler (`os.startfile` on Windows).
  - This export sits beside the presentation's SVG export and does not replace it.
- **HR-3. Better controls in B (the operator's note).** Redesign the display and filter controls so they are clear and fast. B needs:
  - **Projects:** a selector with all/none and a checkbox per project, in its colour.
  - **Status:** chips for open, late, done and archived.
  - **People and classes:** filters by person (`@`) and by milestone class.
  - **Dates:** a date-range control.
  - **Sections:** toggles for which ones show (gantt, table, notes, milestones).
  - **Reset:** one control that clears everything.

  Every control's state is visible at a glance, and the number of active filters is shown. Every control is reachable by keyboard. The state is kept in the URL hash, so a configured view can be bookmarked or re-opened.
- **HR-4. Export the configured view (the operator's note).** Inside B, an "Export this view" action produces a CONSOLIDATED document of exactly what the controls show: the chosen projects, filters and sections. Its header states the filters applied and the date. Provide both outputs:
  - (a) "Print / Save as PDF". A print stylesheet prints only the configured view: cleanly paginated, with no controls in the printout, through the browser's PDF printer.
  - (b) "Download this view". It writes a new self-contained HTML file that holds only the filtered data, including a filtered embedded JSON. The recipient never receives the hidden data.

  The UI states which output leaves the hidden data out: only (b) does. The print only hides it visually.
- **HR-5. C stays concise.** C takes the same project filter, so the chosen projects become its slides. It prints one slide per page.
- **HR-6. Constraints.**
  - Single file, works offline, no CDN, no external request.
  - Light and dark themes.
  - Works at phone width.
  - All user text is escaped, because board text is untrusted.
  - Synthetic data only in tests and captures.
  - English UI strings.

## Increments

At most 4 SOURCE files per increment; tests are uncapped. Suggested order:

| # | Content |
|---|---|
| 001 | The shared extraction, plus variant B with the HR-3 controls |
| 002 | The HR-4 view export: print, plus the filtered download |
| 003 | Variant C |
| 004 | The `H` modal, the toast, `o` to open, keymap, help, README |

## Acceptance (one node per AT)

- **AT-a. Workspace export.**
  - `H`, `b` in the app writes the workspace file, and the toast names it.
  - The file loads headless with 0 console errors and 0 external requests.
- **AT-b. Filters.** The workspace filters by project, status, person, class and date, and the URL hash round-trips the state.
- **AT-c. Filtered download.**
  - "Download this view" produces a file whose embedded data holds ONLY the filtered tasks.
  - A hidden project's task title is absent from the bytes.
- **AT-d. Print.** Print media hides the controls and shows the filter header.
- **AT-e. Deck export.** `H`, `c` writes the deck, and its slides equal the chosen projects.
- **AT-f. Escaping.** Board text such as `<script>` is escaped in both reports.
- **AT-g. Modal keys.** The modal-key law covers the `H` modal.

## Evidence

- **Import probe.** Run a probe from the worktree root that prints `taskboard.__file__`. It must resolve inside the worktree.
- **Test runs.** Run every pytest with `env -u NO_COLOR python -m pytest`.
- **Full suite (P4).** Run it in 3 SEQUENTIAL chunks and keep the transcripts.
  - Baseline: 3281 passed on Windows.
  - The only accepted skip is TC-1902 (clipboard).
  - The 3 known Linux CI failures are backlog, not this batch.
- **Validator.** Run `--brief` at start and at close: 0 BLOCK.
- **Mutation.** Mutation-check the new tests.
- **Browser screenshots.** Both reports at desktop and phone width, in light and dark, plus the filtered-view export and the print preview.
- **Terminal capture.** One real Windows Terminal capture of the `H` modal and its toast at 118x30.
  - Give the window an `hx-` title, and close it by that title.
  - Never close another window.
  - Launch it with `cmd /c 'set NO_COLOR=& set COLORTERM=truecolor& wt.exe -w new --title <t> ...'`.
- **Review page.** Build ONE review page for the operator at `.dev-flow/2026-10-29-batch-01/review.html`.
  - Spanish prose.
  - The screenshots, plus links to the real generated report files.
  - Its purpose: the operator judges the HR-3 controls before the push.
