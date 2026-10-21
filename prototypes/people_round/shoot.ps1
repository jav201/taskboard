# THROWAWAY: real Windows Terminal PNGs of the people round's scenes.
# Adapted from .dev-flow/2026-10-20-batch-03/evidence/captures/shoot_real.ps1 (the fixed
# version that closes its windows) and keeps its load-bearing rules:
#
# - every window gets a UNIQUE title `ppl-<scene>-<size>-<n>`, re-asserted by the app via
#   PROTO_SHOT_TITLE; zero or two matches are errors. It is closed right after its shot
#   (WM_CLOSE by that title, Windows Terminal windows only) and verified gone. NO TERMINAL
#   PROCESS IS EVER KILLED (Windows Terminal is one process for all windows) and no other
#   window is touched. At the end the script asserts no `ppl-*` window remains.
# - full colour: NO_COLOR is cleared and COLORTERM=truecolor set in the window. A grab
#   that is black or has fewer than 8 sampled colours is REJECTED and the scene retried
#   in a new window (the known capture-fallback failure), up to 3 tries.
# - the capture waits for the scene's READY file (written when its keys are played);
#   its first line is the scene's temporary home (TEMP\ppl-cap-*), removed here once the
#   window is closed (closing the window ends the app before it can remove it).
#
#   powershell -NoProfile -File prototypes\people_round\shoot.ps1 -Scenes pv-A,mt-A
#   powershell -NoProfile -File prototypes\people_round\shoot.ps1            (every scene)
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
$Scenes = @($Scenes | ForEach-Object { $_ -split "," } | Where-Object { $_ })

Add-Type @"
using System;
using System.Runtime.InteropServices;
public struct RECT { public int L, T, R, B; }
public class WinPP {
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
[void][WinPP]::SetProcessDpiAwarenessContext([IntPtr](-4))   # PER_MONITOR_AWARE_V2

function Mine([string]$title) {
  @([WinPP]::ByTitle($title) | Where-Object {
    $wp = 0; [void][WinPP]::GetWindowThreadProcessId($_, [ref]$wp)
    (Get-Process -Id $wp -ErrorAction SilentlyContinue).ProcessName -eq $Process })
}

# Close this capture's own terminal window (found by its unique title, in $Process only)
# and wait until it is gone; never any other window.
function Close-Shot([string]$title) {
  foreach ($h in (Mine $title)) { [void][WinPP]::PostMessage($h, 0x0010, [IntPtr]::Zero, [IntPtr]::Zero) }  # WM_CLOSE
  $t0 = Get-Date
  while ((Mine $title).Count -gt 0 -and ((Get-Date) - $t0).TotalSeconds -lt 10) { Start-Sleep -Milliseconds 200 }
  return ((Mine $title).Count -eq 0)
}

function Remove-Home([string]$ready) {
  if (-not (Test-Path $ready)) { return "" }
  $home_ = (Get-Content $ready -TotalCount 1).Trim()
  $tmp = [IO.Path]::GetTempPath().TrimEnd('\')
  if ((Split-Path -Leaf $home_) -like 'ppl-cap-*' -and (Split-Path -Parent $home_) -eq $tmp) {
    for ($k = 0; $k -lt 25 -and (Test-Path -LiteralPath $home_); $k++) {
      Start-Sleep -Milliseconds 200
      Remove-Item -Recurse -Force -LiteralPath $home_ -ErrorAction SilentlyContinue
    }
    if (Test-Path -LiteralPath $home_) { return "WARN $home_ not removed" }
    return ""
  }
  return "WARN unexpected home '$home_' left alone"
}

# one try: open, wait, grab, close. Returns @(status, message)
function Shoot-Once([string]$scene, [string]$size, [int]$try) {
  $cols, $rows = $size -split "x"
  $title = "ppl-$scene-$size-" + (Get-Random -Maximum 99999)
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
"$py" prototypes\people_round\proto.py live $scene 40
"@ | Set-Content -Encoding ascii $cmd

  Start-Process wt.exe -ArgumentList @("-w", "new", "--size", "$cols,$rows", "--title", $title,
                                       "cmd.exe", "/c", $cmd)
  $t0 = Get-Date
  while (-not (Test-Path $ready) -and ((Get-Date) - $t0).TotalSeconds -lt 45) {
    Start-Sleep -Milliseconds 250
  }
  if (-not (Test-Path $ready)) {
    $closed = Close-Shot $title
    Remove-Item $cmd -ErrorAction SilentlyContinue
    return @("retry", "never ready" + $(if ($closed) { "" } else { "; FAIL window $title not closed" }))
  }
  Start-Sleep -Milliseconds 900
  $state = (Get-Content $ready -TotalCount 2)[1]
  if ($state -notlike "OK*") {
    $closed = Close-Shot $title
    $w = Remove-Home $ready
    Remove-Item $ready, $cmd -ErrorAction SilentlyContinue
    return @("retry", "wrong end state: $state $w" + $(if ($closed) { "" } else { "; FAIL not closed" }))
  }
  $hits = Mine $title
  if ($hits.Count -ne 1) {
    $closed = Close-Shot $title
    $w = Remove-Home $ready
    Remove-Item $ready, $cmd -ErrorAction SilentlyContinue
    return @("retry", "$($hits.Count) windows titled $title $w" + $(if ($closed) { "" } else { "; FAIL not closed" }))
  }
  $hwnd = $hits[0]
  [void][WinPP]::ShowWindow($hwnd, 9)
  [void][WinPP]::SetForegroundWindow($hwnd)
  Start-Sleep -Milliseconds 700

  $r = New-Object RECT
  [void][WinPP]::GetWindowRect($hwnd, [ref]$r)
  $fw = $r.R - $r.L; $fh = $r.B - $r.T
  $full = New-Object System.Drawing.Bitmap $fw, $fh
  $fg = [System.Drawing.Graphics]::FromImage($full)
  $hdc = $fg.GetHdc()
  $printed = [WinPP]::PrintWindow($hwnd, $hdc, 2)
  $fg.ReleaseHdc($hdc)
  $count = {
    $d = @{}
    for ($sy = 20; $sy -lt $fh - 20; $sy += 37) {
      for ($sx = 20; $sx -lt $fw - 20; $sx += 41) { $d[$full.GetPixel($sx, $sy).ToArgb()] = 1 }
    }
    $d.Count
  }
  $n = & $count
  $method = "PrintWindow"
  if (-not $printed -or $n -lt 8) {
    $method = "CopyFromScreen (PrintWindow gave $n colours)"
    $fg.CopyFromScreen($r.L, $r.T, 0, 0, $full.Size)
    $n = & $count
  }
  $status = "ok"; $msg = ""
  if ($n -lt 8) {
    $status = "retry"; $msg = "rejected: $n colours sampled via $method (black / colourless)"
  } else {
    $cw = $fw - 16; $ch = $fh - 8          # trim the invisible resize border (8 px each side, none on top)
    $bmp = New-Object System.Drawing.Bitmap $cw, $ch
    $bg = [System.Drawing.Graphics]::FromImage($bmp)
    $bg.DrawImage($full, (New-Object System.Drawing.Rectangle 0, 0, $cw, $ch),
                  (New-Object System.Drawing.Rectangle 8, 0, $cw, $ch),
                  [System.Drawing.GraphicsUnit]::Pixel)
    $bmp.Save((Join-Path $outDir "$scene`_$size.png"), [System.Drawing.Imaging.ImageFormat]::Png)
    $bg.Dispose(); $bmp.Dispose()
    $msg = "($cw x $ch, $n colours sampled) via $method, try $try"
  }
  $fg.Dispose(); $full.Dispose()
  $closed = Close-Shot $title
  $w = Remove-Home $ready
  Remove-Item $ready, $cmd -ErrorAction SilentlyContinue
  if (-not $closed) { $msg += " - FAIL: window $title not closed" } else { $msg += " - window closed" }
  if ($w) { $msg += " - $w" }
  return @($status, $msg)
}

$log = @()
foreach ($scene in $Scenes) {
  foreach ($size in ($Sizes -split ",")) {
    for ($try = 1; $try -le 3; $try++) {
      $res = Shoot-Once $scene $size $try
      if ($res[0] -eq "ok") { $log += "ok   $scene $size $($res[1])"; break }
      $log += "try  $scene $size : $($res[1])"
      if ($try -eq 3) { $log += "FAIL $scene $size : 3 tries" }
    }
    Write-Output $log[-1]
  }
}
$log | Add-Content -Encoding utf8 (Join-Path $outDir "capture-log.txt")
# every shot's window was closed above; assert none of this harness's windows remains
$left = @(Mine "ppl-")
if ($left.Count -gt 0) { Write-Output "FAIL: $($left.Count) ppl-* window(s) still open"; exit 1 }
Write-Output "no ppl-* window left open"
