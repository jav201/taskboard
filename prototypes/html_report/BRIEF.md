# Prototype brief — an expanded HTML report exported from the app

Written by the orchestrator on 2026-10-29. Branch `proto/html-report`, from `main` `9cc7d4e`.

## The operator's words (verbatim)

> «Otra cosa fue el export en SVG, creí que sería más fácil usarlo y manipularlo pero no fue así, quiero que prototipes un reporte con funcionalidad expandida en html que se exporte de la app.»

## Today (read the code)

There are two exports today:

- **The presentation's SVG export.** `x` in `R` writes an SVG/PNG of the terminal frame (`save_present_svg`, `app.py` around line 613). It is a picture of text cells: hard to edit, search, or reuse.
- **The HTML report.** `taskboard/report.py` `build_report` writes a static HTML report, but only from the CLI (`taskboard --report [PROJECT]`), into `<board dir>/reports/`. It contains count tiles, a horizon table, and one section per project with a small SVG curve. The app has no key for it. Read `report.py` and run it on a synthetic board to see it.

## The goal

One self-contained `.html` file exported FROM THE APP that is easy to use, read and manipulate:

- It opens in any browser, offline: everything inline, no CDN.
- It is interactive where that helps.
- It prints cleanly to PDF.
- It carries the board's real data: projects, tasks, phases, dates, milestones with their class marks, `@people` mentions, notes with their `==`/`!!`/`++` highlights, links/critical chain, done vs open vs archived.

## What the round must show (2–3 radically different variants)

Each variant is a real HTML file generated from a synthetic board by prototype code. Take browser screenshots at desktop width (1366) and phone width (390), in light and dark.

Candidate directions; propose better ones if you see them:

- **(A) Status report / one-pager for a meeting.** Summary tiles, what changed since a date, late and next 7 days, milestones by class, per-project progress. It prints to 1–2 pages.
- **(B) Interactive workspace.**
  - An interactive gantt: zoom by day, week or month; hover for details; click a bar to open the task's card.
  - Filters by board, project, person (`@`), milestone class and status. A search box.
  - A sortable task table.
  - Notes rendered with highlights and mentions.
  - Data embedded as JSON, with a "download CSV/JSON" button so the data can be reused in Excel or other tools.
- **(C) Presentation/handout.** The presentation's gantt (views 1/2/3) as real HTML/SVG vector elements, with selectable text and per-project slides. Arrow keys page through them.

For each variant, also propose:

1. **The key in the app that exports it.**
   - Check that it is free in `taskboard/keymap.py`.
   - Say whether it is global or inside `R`.
   - Say what scope it exports: the current board, the current project, or what is shown/hidden in the presentation.
2. **Where the file lands, and what the app says after.** For example, a toast with the path and an `o` to open it in the browser.
3. **Whether it replaces or sits beside the SVG export.**

## Rules

- **The page and its form.** The verdict page is `prototypes/html_report/html-report-round.html`.
  - Prose in Spanish; UI strings in the reports in English.
  - BLUF at the top.
  - Per variant: the screenshots embedded, plus a link to open the real report file. The report files are committed in `prototypes/html_report/out/`.
  - Per variant: the plain-Spanish consequence and a recommendation.
  - Per item: «Elijo esta» plus an objection field.
  - A GENERAL NOTES field.
  - An «Exportar respuestas» button that copies text and JSON to the clipboard.
  - Verify 0 console errors, both on the verdict page and on each report file (use a headless browser).
  - Then open the verdict page with `Start-Process`.
- **The reports.** Single file each, no external requests. Light and dark themes. Phone width works. Prints cleanly.
- **Data.** Synthetic only: boards "Personal", "Client A", "Course"; people like "Ana Ruiz"; classes like "Delivery ▲". Never the operator's real name (the placeholder is `username_subject`).
- **Scope.** Nothing under `taskboard/` changes. Prototype code lives in `prototypes/html_report/`, and it may import `taskboard` to read a board.
- **TUI captures.** Only if you show the in-app key or toast:
  - each Windows Terminal window gets a unique `hr-` title;
  - close it by that title and verify it is gone; never close another window;
  - launch with `cmd /c 'set NO_COLOR=& set COLORTERM=truecolor& wt.exe -w new --title <t> ...'`.
- **Tests.** Use `env -u NO_COLOR` for pytest.
