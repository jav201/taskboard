"""One-shot patch for inc13. Run once, from the worktree root."""
import pathlib

p = pathlib.Path("taskboard/raster.py")
s = p.read_text(encoding="utf-8")

OLD = '''from __future__ import annotations

from PIL import Image, ImageOps

try:                                    # see the module docstring: NOT lazy
    from textual_image.widget import Image as AutoImage
    from textual_image.renderable import Image as _Chosen
    from textual_image.renderable.sixel import Image as _Sixel
    from textual_image.renderable.tgp import Image as _TGP
except Exception:                       # pragma: no cover - declared dependency
    AutoImage = _Chosen = _Sixel = _TGP = None

# WHICH transport the library picked for THIS terminal, decided at its import
# (`textual_image.widget` calls `get_cell_size()` at module scope for exactly
# that reason).  Sixel and TGP are real pixels; halfcell and unicode are the
# glyph path wearing the library's name -- which is why "a widget exists" is
# not the question `raster_available()` answers.
TRANSPORT = {None: "none", _Sixel: "sixel", _TGP: "tgp"}.get(_Chosen, "glyph")
'''

NEW = r'''from __future__ import annotations

import importlib
import sys
import time

from PIL import Image, ImageOps

# THE PROBE IS GUARDED AND BOUNDED (tui-demos LIMITS L-42; SCOPE inc2 F-4).
#
# The docstring above is right that detection must happen at module load.  What
# it did not say is the price: `textual_image.renderable` runs a Sixel DEVICE
# ATTRIBUTES query at ITS module scope -- write ESC[c to stdout, then read
# stdin until the answer arrives -- gated only by its own
# `is_tty = sys.__stdout__ and sys.__stdout__.isatty()`.
#
# On Windows `NUL` is a CHARACTER DEVICE, so `isatty()` answers True for it.
# A process launched with `stdout=subprocess.DEVNULL` therefore believes it is
# talking to a terminal, writes the query into the void, and waits for an
# answer that cannot come.  Measured on this box, both ways, before the fix:
#
#     stdin=DEVNULL  stdout=DEVNULL -> HUNG (killed at 8s)
#     stdin=inherit  stdout=DEVNULL -> HUNG (killed at 8s)
#
# It cost SCOPE's second increment TWO 600-SECOND RUNS before
# `faulthandler.dump_traceback_later` found the stack, and the hang looks
# exactly like a slow numba compile until someone dumps it.  Every headless
# consumer of a kit inherits it -- a test runner, a bench, a CI job -- because
# the chain is `taskboard.language -> taskboard.raster -> textual_image.widget
# -> textual_image.renderable -> sixel.query_terminal_support`.
#
# So: PROBE ONLY WHEN BOTH ENDS ARE REAL CONSOLES, and bound the wait.
PROBE_BUDGET_S = 0.2                    # the whole answer wait, all reads


def _is_a_real_console(stream) -> bool:
    """True when `stream` is a console this process may hold a conversation
    with -- not merely a character device that answers `isatty()`.

    On Windows the discriminator is **`GetConsoleMode`**: it succeeds on a
    console handle and FAILS on `NUL`, which is the exact distinction
    `isatty()` cannot express there.  Elsewhere `isatty()` is already the
    truth -- `/dev/null` is not a tty on POSIX -- so it is the whole test.

    Both stdout AND stdin have to pass, because the probe writes to one and
    reads from the other, and it is the READ that blocks forever."""
    if stream is None:
        return False
    try:
        if not stream.isatty():
            return False
    except Exception:
        return False
    if sys.platform != "win32":
        return True
    try:
        import ctypes
        import msvcrt
        from ctypes.wintypes import DWORD
        mode = DWORD()
        handle = msvcrt.get_osfhandle(stream.fileno())
        return bool(ctypes.WinDLL("kernel32").GetConsoleMode(
            handle, ctypes.byref(mode)))
    except Exception:
        return False


class _NotATerminal:
    """A stdout stand-in that answers `isatty()` ACCURATELY.

    Not a monkeypatch of library internals -- it is telling `textual_image`
    the one truth `isatty()` cannot carry on Windows.  The library's own
    `is_tty` then comes out False, it selects the unicode renderable without
    querying anything, and `get_cell_size()` skips both of its query branches
    and falls through to the VT340 defaults.  Everything else delegates to the
    real stream, so a library that WRITES to stdout during import still
    writes to stdout."""

    def __init__(self, stream):
        self._stream = stream

    def isatty(self) -> bool:
        return False

    def __getattr__(self, name):
        return getattr(self._stream, name)


def _budgeted(read, budget: float):
    """`textual_image._terminal.read` with a DEADLINE across all its calls.

    The library already passes a 0.1 s per-read timeout; what it has no
    concept of is a TOTAL.  This caps the sum at `budget` and then raises
    `TimeoutError`, which both `query_terminal_support()` and
    `get_cell_size()` already catch and treat as "no answer" -- so the failure
    mode is the correct one (assume no Sixel) rather than an exception
    escaping the import.

    WHAT THIS DOES NOT BOUND, said plainly: a single `os.read()` that blocks
    AFTER `WaitForSingleObject` has returned signalled.  There is no
    non-blocking read behind that call, so bounding it would mean forking the
    library.  The GUARD above is what removes the reported failure; this caps
    the answer wait on the path the guard lets through."""
    deadline = time.monotonic() + budget

    def bounded(fd, length, timeout=None):
        left = deadline - time.monotonic()
        if left <= 0:
            raise TimeoutError("sixel probe budget exhausted")
        return read(fd, length, left if timeout is None else min(timeout, left))

    return bounded


def _import_textual_image():
    """Import the library, probing the terminal only if there is one.

    Returns `(AutoImage, chosen, sixel, tgp)`.  The swap and the budget are
    both undone in `finally`: this module must not leave a process's
    `sys.__stdout__` replaced or another module's function rebound."""
    out, stdin = sys.__stdout__, sys.__stdin__
    may_probe = _is_a_real_console(out) and _is_a_real_console(stdin)

    term = importlib.import_module("textual_image._terminal")
    real_read = term.read
    if may_probe:
        term.read = _budgeted(real_read, PROBE_BUDGET_S)
    elif out is not None:
        sys.__stdout__ = _NotATerminal(out)
    try:
        from textual_image.widget import Image as AutoImage
        from textual_image.renderable import Image as chosen
        from textual_image.renderable.sixel import Image as sixel
        from textual_image.renderable.tgp import Image as tgp
        return AutoImage, chosen, sixel, tgp
    finally:
        term.read = real_read
        sys.__stdout__ = out


def _transport(chosen, sixel, tgp) -> str:
    """WHICH transport the library picked for THIS terminal.  Sixel and TGP
    are real pixels; halfcell and unicode are the glyph path wearing the
    library's name -- which is why "a widget exists" is not the question
    `raster_available()` answers.

    SPELLED OUT RATHER THAN AS A DICT LOOKUP, because the dict was WRONG.  It
    was `{None: "none", _Sixel: "sixel", _TGP: "tgp"}.get(_Chosen, "glyph")`,
    and when the library is absent all four names are `None` -- so the literal
    collapsed to `{None: "tgp"}` and a box with no `textual_image` installed
    reported a TGP transport with `raster_available()` True.  Three `is` tests
    cannot collapse."""
    if chosen is None:
        return "none"
    if chosen is sixel:
        return "sixel"
    if chosen is tgp:
        return "tgp"
    return "glyph"


def _detect():
    """`(widget class, transport)` -- the whole decision, in one re-callable
    function so a test can drive it with the library's answer mocked."""
    try:
        AutoImage, chosen, sixel, tgp = _import_textual_image()
    except Exception:                   # pragma: no cover - declared dependency
        return None, "none"
    return AutoImage, _transport(chosen, sixel, tgp)


AutoImage, TRANSPORT = _detect()
'''

assert s.count(OLD) == 1, "import block anchor not unique"
p.write_text(s.replace(OLD, NEW), encoding="utf-8")

# modals.py takes its widget from raster, so the second door closes too.
m = pathlib.Path("taskboard/modals.py")
ms = m.read_text(encoding="utf-8")
OLDM = '''try:
    from textual_image.widget import Image as AutoImage
except Exception:          # pragma: no cover - dependency present in prod
    AutoImage = None
'''
NEWM = '''# ...and imported FROM `raster.py` rather than from the library directly, so
# the Sixel probe has exactly one door (L-42). `raster.py` guards that import:
# on Windows `NUL` is a character device, `isatty()` answers True for it, and
# an unguarded probe writes a device-attributes query into the void and blocks
# on stdin forever. A second direct import here would reopen the hole for
# whichever module Python happened to load first.
from .raster import AutoImage          # noqa: F401  (re-exported for viewers)
'''
assert ms.count(OLDM) == 1, "modals anchor not unique"
m.write_text(ms.replace(OLDM, NEWM), encoding="utf-8")
print("raster.py and modals.py patched")
