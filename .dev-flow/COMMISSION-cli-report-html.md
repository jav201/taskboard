# Commission — `taskboard --report` exports the new HTML and asks for the board

Written by the orchestrator on 2026-10-29 for batch `2026-10-29-batch-02`. Branch `feat/cli-report-html`, from `main` `4ca4a7d`.

## The operator's words (verbatim)

From the review of batch `2026-10-29-batch-01`, which answered `"push": "si"`:

> «Que el comando --report exporte el html, que pregunte por el board.»

## Today

`taskboard/__main__.py` (around line 57) defines `--report [PROJECT]`.

- It writes the OLD static report (`report.write_report`) and exits.
- The board comes from `--board`, `--open`, or the default board. It never asks which board.
- `2026-10-29-batch-01` kept it unchanged (HR-1) and left the choice to the operator. The operator has now chosen: the CLI exports the new HTML.

The new reports are the in-app `H` export, built by `taskboard/report_html.py` (the shared extraction), `report_workspace.py` (B) and `report_deck.py` (C), and by the `H` modal in `modals.py` / `app.py`. Read them by range or with grep.

## Decisions (record each one in the plan)

- **CR-1, what it writes.** `--report` writes the NEW HTML exports through the same code path the `H` modal uses, so the CLI and the app cannot drift.
  - **Default:** both B (workspace) and C (deck), like `H` → `a`.
  - **Optional flag:** `--report-kind {workspace,deck,both}`, default `both`.
  - **Output:** the files land where `H` puts them, `<board dir>/reports/`, and the CLI prints each path on its own line.
  - **Exit:** with no TUI and without writing the board, exactly as today.
- **CR-2, it asks for the board.** When `--report` is given without `--board` or `--open` and the registry (`~/.taskboard/boards.json`) has MORE than one active board, the CLI prints a numbered list (name, and the file path dimmed or after it). It then reads a number from stdin.
  - **Default answer:** `enter` alone picks the default/last board, marked in the list.
  - **`a` picks all boards:** this matches `H`'s scope `o`.
  - **Invalid input:** re-asks.
  - **EOF or `q`:** exits with code 1 and writes nothing.
  - **No prompt:** with one board, or with `--board`/`--open`, it does not ask.
  - **Non-interactive stdin** (not a TTY): it never blocks. It exits with code 2 and a message listing the boards and saying to pass `--board PATH`.
- **CR-3, PROJECT still works.** `--report PROJECT` keeps its meaning and becomes the workspace/deck scope "this project" (`H` → `p`). An unknown project keeps today's error message, listing the board's projects. With a multi-board pick (`a`), PROJECT is refused with a clear message.
- **CR-4, the old static report.** The old static report is no longer reachable from `--report`.
  - **Code:** keep `report.py` only for what the new reports still import (its due-date helpers). Remove its now-dead CLI entry points only if nothing else uses them. Check the tests: a test that asserts the OLD report through the CLI must change to the new one. Justify each change.
  - **README:** the `--report` section describes the new behaviour.
- **CR-5, safety.**
  - Reading a board never writes it.
  - A `--board PATH` that does not exist is refused before anything is built, as `--open` does today (security S-3). The loader must not seed sample data at that path. This also closes BACKLOG's S-3 item for `--report`; mark it.
  - Paths and board names printed in the prompt pass through `strip_controls`.

## Increment

One increment, 001: at most 4 SOURCE files, expected `__main__.py`, plus `report.py` and/or `report_html.py` if a thin CLI entry is needed, and `README.md`. Tests are uncapped.

## Acceptance (one node per AT)

- **AT-a.** `--report` with two registered boards and stdin `2\n` writes B and C for board 2 and prints both paths. Board 1 is untouched (bytes unchanged). Run it as a subprocess with a temp HOME; never touch the real home.
- **AT-b.** `--report` with stdin `a\n` writes reports covering all boards.
- **AT-c.** `--report` with non-TTY empty stdin and two boards exits 2 with the board list and writes nothing. With EOF or `q`, it exits 1.
- **AT-d.** `--report --board PATH` does not prompt. `--report PROJECT` scopes to the project. An unknown project errors with the list.
- **AT-e.** `--report --board <missing path>` is refused and creates nothing at that path.
- **AT-f.** The written files load headless with 0 console errors. Reuse the batch-01 headless check.

## Evidence

- **Import probe.** Before any test, run a probe from the worktree root that prints `taskboard.__file__`.
- **Tests.** Run every pytest with `env -u NO_COLOR python -m pytest`.
- **Full suite (P4).** Run it in 3 SEQUENTIAL chunks. The baseline is 3332 passed. Accept only the TC-1902 skip.
- **Validator.** `--brief` must show 0 BLOCK at start and at close.
- **Mutation.** Mutation-check the new tests.
