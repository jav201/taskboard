# Real Windows Terminal PNGs of batch 2026-10-20-batch-03's shipped items (the round's method).
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
#   powershell -NoProfile -File .dev-flow\2026-10-20-batch-03\evidence\captures\shoot_real.ps1 -Scenes agenda
#   powershell -NoProfile -File .dev-flow\2026-10-20-batch-03\evidence\captures\shoot_real.ps1   (every scene)
param(
  [string[]]$Scenes = @(),
  [string]$Sizes = "118x30,80x24",
  [string]$Process = "WindowsTerminal"
)

$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Drawing

$here   = Split-Path -Parent $MyInvocation.MyCommand.Path
$root   = (Resolve-Path (Join-Path $here "..\..\..\..")).Path
$py     = Join-Path $env:USERPROFILE "anaconda3\python.exe"
$outDir = Join-Path $here "png"
New-Item -ItemType Directory -Force $outDir | Out-Null
if ($Scenes.Count -eq 0 -or ($Scenes.Count -eq 1 -and $Scenes[0] -eq "")) {
  $Scenes = (& $py (Join-Path $here "shoot_real.py") list).Trim() -split " "
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
  [DllImport("user32.dll")] public static extern bool PostMessage(IntPtr h, uint msg, IntPtr w, IntPtr l);
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

# Close this capture's own terminal window (found by its unique title, in $Process only)
# and wait until it is gone; never any other window.
function Close-Shot([string]$title) {
  $mine = { @([WinBR]::ByTitle($title) | Where-Object {
    $wp = 0; [void][WinBR]::GetWindowThreadProcessId($_, [ref]$wp)
    (Get-Process -Id $wp -ErrorAction SilentlyContinue).ProcessName -eq $Process }) }
  foreach ($h in (& $mine)) { [void][WinBR]::PostMessage($h, 0x0010, [IntPtr]::Zero, [IntPtr]::Zero) }  # WM_CLOSE
  $t0 = Get-Date
  while ((& $mine).Count -gt 0 -and ((Get-Date) - $t0).TotalSeconds -lt 10) { Start-Sleep -Milliseconds 200 }
  return ((& $mine).Count -eq 0)
}

$log = @()
foreach ($scene in $Scenes) {
  foreach ($size in ($Sizes -split ",")) {
    $cols, $rows = $size -split "x"
    $title = "tb03-$scene-$size-" + (Get-Random -Maximum 99999)
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
set CAPTURE_EXPORT_DIR=$outDir
set CAPTURE_SIZE=$size
cd /d "$root"
"$py" .dev-flow\2026-10-20-batch-03\evidence\captures\shoot_real.py live $scene 6
"@ | Set-Content -Encoding ascii $cmd

    Start-Process wt.exe -ArgumentList @("-w", "new", "--size", "$cols,$rows", "--title", $title,
                                         "cmd.exe", "/c", $cmd)
    $t0 = Get-Date
    while (-not (Test-Path $ready) -and ((Get-Date) - $t0).TotalSeconds -lt 45) {
      Start-Sleep -Milliseconds 250
    }
    if (-not (Test-Path $ready)) {
      $log += "FAIL $scene $size : never ready"
      if (-not (Close-Shot $title)) { $log += "FAIL $scene $size : window $title not closed" }
      Remove-Item $cmd -ErrorAction SilentlyContinue; continue
    }
    Start-Sleep -Milliseconds 900

    $hits = @([WinBR]::ByTitle($title) | Where-Object {
      $wp = 0; [void][WinBR]::GetWindowThreadProcessId($_, [ref]$wp)
      (Get-Process -Id $wp -ErrorAction SilentlyContinue).ProcessName -eq $Process
    })
    if ($hits.Count -ne 1) {
      $log += "FAIL $scene $size : $($hits.Count) windows titled $title"
      if (-not (Close-Shot $title)) { $log += "FAIL $scene $size : window $title not closed" }
      Remove-Item $ready, $cmd -ErrorAction SilentlyContinue; continue
    }
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
    $closed = Close-Shot $title
    # closing the window ends the app before it can remove its synthetic home: do it here,
    # only for a folder this harness made (TEMP\b03-cap-*); retried while the app's files close
    $home_ = (Get-Content $ready -TotalCount 1).Trim()
    $tmp = [IO.Path]::GetTempPath().TrimEnd('\')
    if ((Split-Path -Leaf $home_) -like 'b03-cap-*' -and (Split-Path -Parent $home_) -eq $tmp) {
      for ($k = 0; $k -lt 25 -and (Test-Path -LiteralPath $home_); $k++) {
        Start-Sleep -Milliseconds 200
        Remove-Item -Recurse -Force -LiteralPath $home_ -ErrorAction SilentlyContinue
      }
      if (Test-Path -LiteralPath $home_) { $log += "WARN $scene $size : $home_ not removed" }
    } else { $log += "WARN $scene $size : unexpected home '$home_' left alone" }
    $log += "ok   $scene $size ($cw x $ch, $($distinct.Count) colours sampled) via $method" +
            $(if ($closed) { " - window closed" } else { " - FAIL: window $title not closed" })
    Remove-Item $ready, $cmd -ErrorAction SilentlyContinue
  }
}
$log | ForEach-Object { Write-Output $_ }
$log | Add-Content -Encoding utf8 (Join-Path $outDir "capture-log.txt")
# every shot's window was closed above; assert none of this harness's windows remains
$left = @([WinBR]::ByTitle("tb03-") | Where-Object {
  $wp = 0; [void][WinBR]::GetWindowThreadProcessId($_, [ref]$wp)
  (Get-Process -Id $wp -ErrorAction SilentlyContinue).ProcessName -eq $Process })
if ($left.Count -gt 0) { Write-Output "FAIL: $($left.Count) tb03-* window(s) still open"; exit 1 }
Write-Output "no tb03-* window left open"
