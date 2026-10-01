# THROWAWAY: real Windows Terminal PNG of one prototype variant.
# Adapted from .claude/worktrees/kanban-variants/.fast-dev-flow/captures/shoot.ps1
# and it keeps that file's load-bearing rules verbatim in spirit:
#
# L-19: the spawned window CLOSES ITSELF (the prototype exits on a timer) and
#       NO TERMINAL PROCESS IS EVER KILLED. Windows Terminal is one process for
#       all windows. There is no Stop-Process, Kill, or taskkill below, by policy.
# L-27: the window is selected BY TITLE (wt --title, then the app re-asserts it
#       via PROTO_SHOT_TITLE), zero or two matches are errors; the grab is
#       PrintWindow(PW_RENDERFULLCONTENT), checked against its pixels, with
#       CopyFromScreen as a recorded-as-such fallback.
# The capture process is made DPI-aware before measuring (logical vs physical px).
# The command goes in a .cmd file (wt splits ';' into tabs); launch from PowerShell.
#
#   powershell -File prototypes\edit_modal\shoot.ps1 -Proto edit_modal -Variant A
param(
  [ValidateSet("edit_modal", "kanban_priority")] [string]$Proto = "edit_modal",
  [string]$Variant = "0",
  [double]$Seconds = 14,
  [int]$Cols = 120,
  [int]$Rows = 36,
  [string]$Process = "WindowsTerminal"
)

$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Drawing, System.Windows.Forms

$root   = "C:\Users\jjgh8\Github\taskboard"
$py     = "C:\Users\jjgh8\anaconda3\python.exe"
$outDir = Join-Path $root "prototypes\$Proto\out"
$title  = "tbproto-$Proto-$Variant-" + (Get-Random -Maximum 99999)
$script = Join-Path $env:TEMP "tbproto_$Proto`_$Variant.cmd"
@"
@echo off
chcp 65001 > nul
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
set PROTO_SHOT_TITLE=$title
cd /d $root
"$py" prototypes\$Proto\proto.py live $Variant $Seconds
"@ | Set-Content -Encoding ascii $script

Add-Type @"
using System;
using System.Runtime.InteropServices;
public struct RECT { public int L, T, R, B; }
public class Win {
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int cmd);
  [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr h);
  [DllImport("user32.dll")] public static extern int GetWindowText(IntPtr h, System.Text.StringBuilder s, int n);
  [DllImport("user32.dll")] public static extern int GetWindowThreadProcessId(IntPtr h, ref int pid);
  [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr h, IntPtr hdc, uint flags);
  [DllImport("user32.dll")] public static extern bool SetProcessDpiAwarenessContext(IntPtr ctx);
  public delegate bool EnumProc(IntPtr h, IntPtr l);
  [DllImport("user32.dll")] public static extern bool EnumWindows(EnumProc cb, IntPtr l);

  public static System.Collections.Generic.List<IntPtr> ByTitle(string needle) {
    var hits = new System.Collections.Generic.List<IntPtr>();
    EnumWindows(delegate(IntPtr h, IntPtr l) {
      if (!IsWindowVisible(h)) return true;
      var sb = new System.Text.StringBuilder(512);
      GetWindowText(h, sb, 512);
      if (sb.ToString().IndexOf(needle, StringComparison.OrdinalIgnoreCase) >= 0) hits.Add(h);
      return true;
    }, IntPtr.Zero);
    return hits;
  }
}
"@ -ErrorAction SilentlyContinue

[void][Win]::SetProcessDpiAwarenessContext([IntPtr](-4))   # PER_MONITOR_AWARE_V2

Start-Process wt.exe -ArgumentList @(
  "-w", "new", "--size", "$Cols,$Rows", "--title", $title, "cmd.exe", "/c", $script)
Start-Sleep -Seconds ([math]::Max(5, $Seconds - 6))

$hits = @([Win]::ByTitle($title) | Where-Object {
  $wp = 0; [void][Win]::GetWindowThreadProcessId($_, [ref]$wp)
  (Get-Process -Id $wp -ErrorAction SilentlyContinue).ProcessName -eq $Process
})
if ($hits.Count -eq 0) { throw "no visible $Process window titled '$title' - capture aborted" }
if ($hits.Count -gt 1) { throw "$($hits.Count) windows titled '$title' - refusing to guess" }
$hwnd = $hits[0]

[void][Win]::ShowWindow($hwnd, 9)
[void][Win]::SetForegroundWindow($hwnd)
Start-Sleep -Milliseconds 700

$r = New-Object RECT
[void][Win]::GetWindowRect($hwnd, [ref]$r)
$fw = $r.R - $r.L; $fh = $r.B - $r.T
$full = New-Object System.Drawing.Bitmap $fw, $fh
$fg = [System.Drawing.Graphics]::FromImage($full)
$hdc = $fg.GetHdc()
$printed = [Win]::PrintWindow($hwnd, $hdc, 2)
$fg.ReleaseHdc($hdc)

$distinct = @{}
for ($sy = 20; $sy -lt $fh - 20; $sy += 37) {
  for ($sx = 20; $sx -lt $fw - 20; $sx += 41) { $distinct[$full.GetPixel($sx, $sy).ToArgb()] = 1 }
}
$method = "PrintWindow"
if (-not $printed -or $distinct.Count -lt 3) {
  $method = "CopyFromScreen (PrintWindow gave $($distinct.Count) distinct colours)"
  $fg.CopyFromScreen($r.L, $r.T, 0, 0, $full.Size)
}

$cw = $fw - 20; $ch = $fh - 16
$bmp = New-Object System.Drawing.Bitmap $cw, $ch
$bg = [System.Drawing.Graphics]::FromImage($bmp)
$bg.DrawImage($full, (New-Object System.Drawing.Rectangle 0, 0, $cw, $ch),
              (New-Object System.Drawing.Rectangle 10, 0, $cw, $ch),
              [System.Drawing.GraphicsUnit]::Pixel)
$out = Join-Path $outDir "wt_$Variant`_$Cols`x$Rows.png"
$bmp.Save($out, [System.Drawing.Imaging.ImageFormat]::Png)
$bg.Dispose(); $bmp.Dispose(); $fg.Dispose(); $full.Dispose()
Write-Output "saved $out  ($cw x $ch)  via $method  title '$title'"
# the window closes itself when the prototype's timer fires; nothing is killed here.
