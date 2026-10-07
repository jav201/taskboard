"""The failed-backup partial-file law (batch 2026-10-07-batch-05, LLR-1101.1 · AT-1101).

`models._create_beside` writes a backup/log beside the board by EXCLUSIVE create:
`with open(p, "xb") as fh: fh.write(data)`. If the WRITE itself fails — a full
disk — the exclusively-created file used to stay on disk as a partial file that
pretends to be a backup. The law: any exception from the write closes the handle
and removes the just-created path best-effort (the removal in a nested guard that
swallows its own errors), then re-raises the ORIGINAL exception unchanged.

The fault is injected at the mechanism level — a fake file whose `write` raises
`ENOSPC` — so no real disk is filled. RED on base: arm 1 finds the partial file
still on disk after the failed write.
"""
from __future__ import annotations

import builtins
import errno
from pathlib import Path

import pytest

from taskboard.models import _create_beside


class _FlakyFile:
    """A file that has been exclusively created, but whose `write` fails as a
    full disk would. `close` (and the context-manager exit) still release the
    real handle, so a best-effort unlink can succeed on Windows."""

    def __init__(self, real):
        self._real = real

    def write(self, data):
        raise OSError(errno.ENOSPC, "No space left on device")

    def close(self):
        self._real.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self._real.close()
        return False


def _flaky_open(monkeypatch):
    """Route the helper's exclusive-create `open` to `_FlakyFile`."""
    real_open = builtins.open

    def open_flaky(file, mode="r", *a, **k):
        if mode == "xb":
            return _FlakyFile(real_open(file, mode, *a, **k))
        return real_open(file, mode, *a, **k)

    monkeypatch.setattr(builtins, "open", open_flaky)


def test_failed_write_leaves_no_partial_file(tmp_path, monkeypatch):
    """LLR-1101.1 arm 1: the exclusive create succeeds, the write fails — after
    the call the partial file does NOT exist and the ORIGINAL error propagates.
    RED on base: the partial file survives the failed write."""
    target = tmp_path / "board.json"
    target.write_bytes(b"{}")
    _flaky_open(monkeypatch)
    partial = target.with_name(target.name + ".backup")
    with pytest.raises(OSError) as exc:
        _create_beside(target, ".backup", b"data")
    assert exc.value.errno == errno.ENOSPC
    assert not partial.exists()
    assert {p.name for p in tmp_path.iterdir()} == {"board.json"}


def test_refusing_unlink_never_masks_the_write_error(tmp_path, monkeypatch):
    """LLR-1101.1 arm 2 (the negative control): the write fails AND `Path.unlink`
    refuses — the ORIGINAL error still propagates; the guard adds no new error."""
    target = tmp_path / "board.json"
    target.write_bytes(b"{}")
    _flaky_open(monkeypatch)

    def refuse(self, *a, **k):
        raise PermissionError(errno.EACCES, "Permission denied")

    monkeypatch.setattr(Path, "unlink", refuse)
    with pytest.raises(OSError) as exc:
        _create_beside(target, ".backup", b"data")
    assert exc.value.errno == errno.ENOSPC
