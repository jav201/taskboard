import sys, os, time, msvcrt, ctypes
from ctypes import wintypes
k = ctypes.windll.kernel32
hin = k.GetStdHandle(-10); hout = k.GetStdHandle(-11)
mode = wintypes.DWORD(); k.GetConsoleMode(hin, ctypes.byref(mode))
k.SetConsoleMode(hin, 0x0200)  # ENABLE_VIRTUAL_TERMINAL_INPUT only (raw)
m2 = wintypes.DWORD(); k.GetConsoleMode(hout, ctypes.byref(m2)); k.SetConsoleMode(hout, m2.value | 0x0004)
sys.stdout.write("\x1b[?u\x1b[c"); sys.stdout.flush()
buf = ""; t0 = time.time()
while time.time() - t0 < 3:
    while msvcrt.kbhit():
        buf += msvcrt.getwch()
    time.sleep(0.05)
open(sys.argv[1], "w", encoding="utf-8").write(repr(buf) + "\n")
