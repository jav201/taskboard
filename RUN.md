# Run, test and develop taskboard

Every command runs from the root of your clone.

## Run from source

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1          # macOS / Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m taskboard                   # your board: ~/.taskboard/board.json
python -m taskboard --board scratch.json   # a throwaway board, seeded on first run
```

`requirements.txt` pins the versions the app is built and verified against (Textual 8.2.8,
rich 15.0.0) and includes the test tools.

On Windows, set `$env:PYTHONIOENCODING = "utf-8"` once per terminal before running scripts
that print the app's glyphs; under the default code page Python's `print` fails on them.

## Test

```powershell
python -m pytest -q
```

That is the whole suite, the same command CI runs (`.github/workflows/ci.yml`, Python 3.12).
`tests/test_app.py::test_win_clipboard_roundtrip` needs a working Windows clipboard and can
fail in a non-interactive shell; rerun it on its own before treating it as a defect.

## The privacy hook

A real board never belongs in this repository. Turn on the pre-commit hook once per clone:

```powershell
git config core.hooksPath .githooks
```

It runs `tools/precommit_privacy.py`, which refuses a commit whose staged files carry text from
your own board (`~/.taskboard/board.json`), including truncated forms. Captures and test
fixtures use the seeded demo board or a board built in the test itself.

## Layout

The package is `taskboard/`; `keymap.py` is the one source of key bindings, and `views.py`
holds every view's renderer and its navigation order. The README's
[Development](README.md#development) section lists every module.
