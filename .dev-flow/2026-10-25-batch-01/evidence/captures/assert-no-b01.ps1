# The final no-b01-window assertion, as its own command: every capture window was
# closed by title right after its shot; this enumerates the visible Windows Terminal
# windows and asserts none carries an `b01-` title.
$ErrorActionPreference = "Stop"
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class WinPP3 {
  [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr h);
  [DllImport("user32.dll", CharSet=CharSet.Unicode)] public static extern int GetWindowText(IntPtr h, System.Text.StringBuilder s, int n);
  [DllImport("user32.dll")] public static extern int GetWindowThreadProcessId(IntPtr h, ref int pid);
  public delegate bool EnumProc(IntPtr h, IntPtr l);
  [DllImport("user32.dll")] public static extern bool EnumWindows(EnumProc cb, IntPtr l);
  public static System.Collections.Generic.List<string> ByTitle(string needle) {
    var hits = new System.Collections.Generic.List<string>();
    EnumWindows(delegate(IntPtr h, IntPtr l) {
      if (!IsWindowVisible(h)) return true;
      var sb = new System.Text.StringBuilder(512);
      GetWindowText(h, sb, 512);
      var pid = 0; GetWindowThreadProcessId(h, ref pid);
      string p = "";
      try { p = System.Diagnostics.Process.GetProcessById(pid).ProcessName; } catch { }
      if (sb.ToString().IndexOf(needle, StringComparison.OrdinalIgnoreCase) >= 0 && p == "WindowsTerminal")
        hits.Add(sb.ToString() + " [" + p + "]");
      return true;
    }, IntPtr.Zero);
    return hits;
  }
}
"@
$left = @(,[WinPP3]::ByTitle("b01-") | ForEach-Object { $_ } | Where-Object { $_ })
$flat = @()
foreach ($batch in $left) { foreach ($t in $batch) { $flat += $t } }
if ($flat.Count -gt 0) {
  Write-Output "FAIL: $($flat.Count) b01-* window(s) still open:"
  $flat | ForEach-Object { Write-Output "  $_" }
  exit 1
}
Write-Output "no b01-* window left open"
