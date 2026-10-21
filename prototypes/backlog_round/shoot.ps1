# THROWAWAY: real Windows Terminal PNGs of the backlog round's scenes.
# Adapted from prototypes/edit_modal/shoot.ps1 and keeps its load-bearing rules:
#
# - the spawned window CLOSES ITSELF (the prototype exits on a timer) and NO
#   TERMINAL PROCESS IS EVER KILLED (Windows Terminal is one process for all
#   windows): no Stop-Process, Kill or taskkill below, by policy.
# - the window is selected BY TITLE (wt --title, re-asserted by the app via
#   PROTO_SHOT_TITLE); zero or two matches are errors. The grab is
#   PrintWindow(PW_RENDERFULLCONTENT), checked against its pixels, with
#   CopyFromScreen as a recorded-as-such fallback.
# - full colour: NO_COLOR is cleared and COLORTERM=truecolor set in the window.
# - the capture waits for the scene's READY file (written when its keys are
#   played), not for a guessed number of seconds.
#
#   powershell -NoProfile -File prototypes\backlog_round\shoot.ps1 -Scenes ag-A,pc-B
#   powershell -NoProfile -File prototypes\backlog_round\shoot.ps1            (every scene)
param(
  [string[]]$Scenes = @(),
  [string]$Sizes = "118x30,80x24",
  [string]$Process = "WindowsTerminal"
)

$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Drawing

$here   = Split-Path -Parent $MyInvocation.MyCommand.Path
$root   = (Resolve-Path (Join-Path $here "..\..")).Path
$py     = Join-Path $env:USERPROFILE "anaconda3\python.exe"
$outDir = Join-Path $here "out\png"
New-Item -ItemType Directory -Force $outDir | Out-Null
if ($Scenes.Count -eq 0 -or ($Scenes.Count -eq 1 -and $Scenes[0] -eq "")) {
  $Scenes = (& $py (Join-Path $here "proto.py") list).Trim() -split " "
}
# allow "-Scenes a,b" through -File (one string)
$Scenes = @($Scenes | ForEach-Object { $_ -split "," } | Where-Object { $_ })

Add-Type @"
using System;
using System.Runtime.InteropServices;
public struct RECT { public int L, T, R, B; }
public class WinBR {
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int cmd);
  [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr h);
  [DllImport("user32.dll", CharSet=CharSet.Unicode)] public static extern int GetWindowText(IntPtr h, System.Text.StringBuilder s, int n);
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
[void][WinBR]::SetProcessDpiAwarenessContext([IntPtr](-4))   # PER_MONITOR_AWARE_V2

$log = @()
foreach ($scene in $Scenes) {
  foreach ($size in ($Sizes -split ",")) {
    $cols, $rows = $size -split "x"
    $title = "tbbr-$scene-$size-" + (Get-Random -Maximum 99999)
    $ready = Join-Path $env:TEMP "$title.ready"
    $cmd   = Join-Path $env:TEMP "$title.cmd"
@"
@echo off
chcp 65001 > nul
set NO_COLOR=
set COLORTERM=truecolor
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
set PROTO_SHOT_TITLE=$title
set PROTO_READY_FILE=$ready
cd /d "$root"
"$py" prototypes\backlog_round\proto.py live $scene 6
"@ | Set-Content -Encoding ascii $cmd

    Start-Process wt.exe -ArgumentList @("-w", "new", "--size", "$cols,$rows", "--title", $title,
                                         "cmd.exe", "/c", $cmd)
    $t0 = Get-Date
    while (-not (Test-Path $ready) -and ((Get-Date) - $t0).TotalSeconds -lt 45) {
      Start-Sleep -Milliseconds 250
    }
    if (-not (Test-Path $ready)) { $log += "FAIL $scene $size : never ready"; continue }
    Start-Sleep -Milliseconds 900

    $hits = @([WinBR]::ByTitle($title) | Where-Object {
      $wp = 0; [void][WinBR]::GetWindowThreadProcessId($_, [ref]$wp)
      (Get-Process -Id $wp -ErrorAction SilentlyContinue).ProcessName -eq $Process
    })
    if ($hits.Count -ne 1) { $log += "FAIL $scene $size : $($hits.Count) windows titled $title"; continue }
    $hwnd = $hits[0]
    [void][WinBR]::ShowWindow($hwnd, 9)
    [void][WinBR]::SetForegroundWindow($hwnd)
    Start-Sleep -Milliseconds 600

    $r = New-Object RECT
    [void][WinBR]::GetWindowRect($hwnd, [ref]$r)
    $fw = $r.R - $r.L; $fh = $r.B - $r.T
    $full = New-Object System.Drawing.Bitmap $fw, $fh
    $fg = [System.Drawing.Graphics]::FromImage($full)
    $hdc = $fg.GetHdc()
    $printed = [WinBR]::PrintWindow($hwnd, $hdc, 2)
    $fg.ReleaseHdc($hdc)
    $distinct = @{}
    for ($sy = 20; $sy -lt $fh - 20; $sy += 37) {
      for ($sx = 20; $sx -lt $fw - 20; $sx += 41) { $distinct[$full.GetPixel($sx, $sy).ToArgb()] = 1 }
    }
    $method = "PrintWindow"
    if (-not $printed -or $distinct.Count -lt 8) {
      $method = "CopyFromScreen (PrintWindow gave $($distinct.Count) colours)"
      $fg.CopyFromScreen($r.L, $r.T, 0, 0, $full.Size)
    }
    # trim the invisible resize border (8 px each side, none on top)
    $cw = $fw - 16; $ch = $fh - 8
    $bmp = New-Object System.Drawing.Bitmap $cw, $ch
    $bg = [System.Drawing.Graphics]::FromImage($bmp)
    $bg.DrawImage($full, (New-Object System.Drawing.Rectangle 0, 0, $cw, $ch),
                  (New-Object System.Drawing.Rectangle 8, 0, $cw, $ch),
                  [System.Drawing.GraphicsUnit]::Pixel)
    $out = Join-Path $outDir "$scene`_$size.png"
    $bmp.Save($out, [System.Drawing.Imaging.ImageFormat]::Png)
    $bg.Dispose(); $bmp.Dispose(); $fg.Dispose(); $full.Dispose()
    $log += "ok   $scene $size ($cw x $ch, $($distinct.Count) colours sampled) via $method"
    Remove-Item $ready, $cmd -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 6          # the app's own exit timer closes the window
  }
}
$log | ForEach-Object { Write-Output $_ }
$log | Add-Content -Encoding utf8 (Join-Path $outDir "capture-log.txt")
# nothing is killed here: every window closes itself when its scene's timer fires.
