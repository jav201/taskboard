"""stdin -> stdout with the home folder written as <home> (both slash forms, any
letter case, the 8.3 short form when Windows reports one) and the temp folder as
<temp>, and the account name anywhere else (pytest's `pytest-of-<user>`, the
scratchpad's folder name) as <user> (P3 security S-1). Every probe and transcript
of this batch passes through here."""
import os
import re
import sys
import tempfile

forms = {os.path.expanduser("~"), tempfile.gettempdir()}
try:
    import ctypes
    buf = ctypes.create_unicode_buffer(512)
    for p in list(forms):
        if ctypes.windll.kernel32.GetShortPathNameW(p, buf, 512):
            forms.add(buf.value)
except (AttributeError, OSError):
    pass
text = sys.stdin.buffer.read().decode("utf-8", "replace")
for form in sorted(forms, key=len, reverse=True):
    tag = "<temp>" if form.lower().startswith(tempfile.gettempdir().lower()[:len(form)]) \
        and len(form) > len(os.path.expanduser("~")) else "<home>"
    for f in {form, form.replace("\\", "/")}:
        text = re.sub(re.escape(f), tag, text, flags=re.IGNORECASE)
import getpass  # noqa: E402

user = getpass.getuser()
if user:
    text = re.sub(r"(?<![A-Za-z0-9])" + re.escape(user) + r"(?![A-Za-z0-9])", "<user>", text,
                  flags=re.IGNORECASE)
sys.stdout.buffer.write(text.encode("utf-8"))
