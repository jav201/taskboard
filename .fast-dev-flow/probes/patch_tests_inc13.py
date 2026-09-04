"""One-shot patch for inc13's tests. Run once, from the worktree root."""
import pathlib

p = pathlib.Path("tests/test_surface.py")
s = p.read_text(encoding="utf-8")

ANCHOR = '''def test_transport_is_reported_honestly():'''
assert s.count(ANCHOR) == 1, "anchor not unique"

NEW = r'''ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("stdin_mode", ["devnull", "inherit"])
def test_importing_the_kit_with_stdout_devnull_returns(stdin_mode):
    """L-42 / SCOPE F-4. **This is the test that would have hung.**

    `taskboard.raster` imports `textual_image` at module scope on purpose --
    the transport must be detected before Textual seizes the terminal. The
    price was invisible until a consumer paid it: the library probes by
    writing a Sixel device-attributes query to stdout and reading stdin, and
    on Windows `NUL` is a CHARACTER DEVICE, so `isatty()` answers True for it.
    A process with `stdout=subprocess.DEVNULL` therefore queries the void and
    waits forever.

    Measured on this box against the code as it stood BEFORE the guard, so
    this test is known to be capable of failing rather than assumed to be:

        stdin=DEVNULL  stdout=DEVNULL -> HUNG (killed at 8s)
        stdin=inherit  stdout=DEVNULL -> HUNG (killed at 8s)

    It cost SCOPE's second increment two 600-SECOND runs. The 2 s timeout IS
    the assertion -- `subprocess.run` raises `TimeoutExpired` and the test
    fails -- and 2 s is ~5x the measured 0.4 s, not a number chosen to pass.

    WHAT THIS CANNOT REPRODUCE, so it is said rather than implied: the variant
    where stdin is a REAL CONSOLE. Under pytest stdin is never one, so the
    console-stdin limb of L-42 is covered by the guard's own unit test below
    and not by this subprocess."""
    import subprocess
    import sys as _sys
    stdin = subprocess.DEVNULL if stdin_mode == "devnull" else None
    done = subprocess.run(
        [_sys.executable, "-X", "utf8", "-c", "import taskboard.language"],
        cwd=str(ROOT), stdin=stdin, stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE, timeout=2)
    assert done.returncode == 0, done.stderr.decode(errors="replace")[-2000:]


def test_the_guard_reads_the_console_and_not_merely_isatty():
    """The DISCRIMINATOR, on the real OS rather than on a mock.

    `isatty()` is the only thing the library asks, and on Windows it is not
    enough: `NUL` is a character device and answers True. `GetConsoleMode`
    is what separates a console from a character device, and this asserts the
    separation against an actually-opened null device.

    On POSIX `/dev/null` is not a tty, so `isatty()` already answers
    correctly there and only the second assertion has content -- which is why
    the first is guarded by platform rather than skipped wholesale."""
    import os
    import sys as _sys
    with open(os.devnull, "w") as null:
        if _sys.platform == "win32":
            assert null.isatty(), (
                "premise of L-42 no longer holds on this box: NUL stopped "
                "answering isatty() -- the guard may be unnecessary here, but "
                "the finding was measured on Windows and this is the check")
        assert not RS._is_a_real_console(null), (
            "the null device was accepted as a console; the probe would run "
            "against a handle that can never answer")
    assert not RS._is_a_real_console(None)


def test_a_real_console_still_gets_its_capability_when_the_terminal_answers():
    """The guard must GATE the probe, not kill it. A change that made
    `raster_available()` always False would pass every test above and destroy
    the feature.

    WHAT IS MOCKED, named exactly: `RS._import_textual_image` -- i.e. the
    terminal's ANSWER and the library that reads it. Nothing else. The
    renderable classes are stand-ins, and the assertion is that `_detect()`
    maps a library that chose Sixel onto the transport `"sixel"` and onto
    `raster_available() is True`. It cannot be run against a real console
    because pytest never has one."""
    class _Sixel: pass
    class _TGP: pass
    class _Widget: pass

    real = RS._import_textual_image
    try:
        RS._import_textual_image = lambda: (_Widget, _Sixel, _Sixel, _TGP)
        widget, transport = RS._detect()
        assert transport == "sixel"
        assert widget is _Widget

        RS._import_textual_image = lambda: (_Widget, _TGP, _Sixel, _TGP)
        assert RS._detect()[1] == "tgp"

        class _Half: pass
        RS._import_textual_image = lambda: (_Widget, _Half, _Sixel, _TGP)
        assert RS._detect()[1] == "glyph"
    finally:
        RS._import_textual_image = real


def test_an_absent_library_reports_no_transport_rather_than_tgp():
    """A latent bug found while rewriting the lookup, kept as a regression.

    The transport was `{None: "none", _Sixel: "sixel", _TGP: "tgp"}.get(
    _Chosen, "glyph")`. When `textual_image` is absent every one of those
    names is `None`, so the dict literal COLLAPSED to `{None: "tgp"}` and the
    lookup returned `"tgp"` -- a box with no library installed reported a real
    graphics transport and `raster_available()` answered True. The whole point
    of `raster_available()` is that it is honest by construction, and it was
    not."""
    assert RS._transport(None, None, None) == "none"


def test_the_probe_answer_wait_is_bounded():
    """The operator's bound: 200 ms, and no answer means no Sixel."""
    assert RS.PROBE_BUDGET_S <= 0.2


def test_transport_is_reported_honestly():'''

s = s.replace(ANCHOR, NEW)
p.write_text(s, encoding="utf-8")
print("tests patched")
