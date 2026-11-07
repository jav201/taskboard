# Inc MR-b captures: real Windows Terminal PNGs of scene.py's scenes (adapted from
# prototypes/capture_round/shoot.ps1). Unique title <scene>-<WxH>-<n> (scene names start mrb-); each window is closed
# by exact title (WM_CLOSE) right after its shot and verified gone; no process is killed and no
# other window is touched; a black / <8-colour grab or a wrong end state is retried (<=3).
param([string[]]$Scenes = @("mrb-v1","mrb-v2","mrb-v3","mrb-hostile"), [string]$Sizes = "118x30,80x24")
$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Drawing
$here   = Split-Path -Parent $MyInvocation.MyCommand.Path
$root   = (Resolve-Path (Join-Path $here "..\..\..\..")).Path
$py     = Join-Path $env:USERPROFILE "anaconda3\python.exe"
$Process = "WindowsTerminal"
$Scenes = @($Scenes | ForEach-Object { $_ -split "," } | Where-Object { $_ })
Add-Type @"
using System;
using System.Runtime.InteropServices;
public struct RECT { public int L, T, R, B; }
public class WinCP {
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
[void][WinCP]::SetProcessDpiAwarenessContext([IntPtr](-4))

function Mine([string]$title) {
  @([WinCP]::ByTitle($title) | Where-Object {
    $wp = 0; [void][WinCP]::GetWindowThreadProcessId($_, [ref]$wp)
    (Get-Process -Id $wp -ErrorAction SilentlyContinue).ProcessName -eq $Process })
}
function Close-Shot([string]$title) {
  foreach ($h in (Mine $title)) { [void][WinCP]::PostMessage($h, 0x0010, [IntPtr]::Zero, [IntPtr]::Zero) }
  $t0 = Get-Date
  while ((Mine $title).Count -gt 0 -and ((Get-Date) - $t0).TotalSeconds -lt 10) { Start-Sleep -Milliseconds 200 }
  return ((Mine $title).Count -eq 0)
}
function Remove-Home([string]$ready) {
  if (-not (Test-Path $ready)) { return "" }
  $h = (Get-Content $ready -TotalCount 1).Trim()
  $tmp = [IO.Path]::GetTempPath().TrimEnd('\')
  if ((Split-Path -Leaf $h) -like 'mrb-cap-*' -and (Split-Path -Parent $h) -eq $tmp) {
    for ($k = 0; $k -lt 25 -and (Test-Path -LiteralPath $h); $k++) {
      Start-Sleep -Milliseconds 200
      Remove-Item -Recurse -Force -LiteralPath $h -ErrorAction SilentlyContinue }
    if (Test-Path -LiteralPath $h) { return "WARN $h not removed" }
    return ""
  }
  return "WARN unexpected home '$h' left alone"
}
function Shoot-Once([string]$scene, [string]$size, [int]$try) {
  $cols, $rows = $size -split "x"
  $title = "$scene-$size-" + (Get-Random -Maximum 99999)
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
"$py" "$here\scene.py" live $scene 40
"@ | Set-Content -Encoding ascii $cmd
  $launch = "set NO_COLOR=& set COLORTERM=truecolor& wt.exe -w new --size $cols,$rows --title $title cmd.exe /c `"$cmd`""
  Start-Process cmd.exe -WindowStyle Hidden -ArgumentList @("/c", $launch)
  $t0 = Get-Date
  while (-not (Test-Path $ready) -and ((Get-Date) - $t0).TotalSeconds -lt 45) { Start-Sleep -Milliseconds 250 }
  if (-not (Test-Path $ready)) {
    $c = Close-Shot $title; Remove-Item $cmd -ErrorAction SilentlyContinue
    return @("retry", "never ready" + $(if ($c) { "" } else { "; FAIL not closed" }))
  }
  Start-Sleep -Milliseconds 900
  $state = (Get-Content $ready -TotalCount 2)[1]
  if ($state -notlike "OK*") {
    $c = Close-Shot $title; $w = Remove-Home $ready; Remove-Item $ready, $cmd -ErrorAction SilentlyContinue
    return @("retry", "wrong end state: $state $w" + $(if ($c) { "" } else { "; FAIL not closed" }))
  }
  $hits = Mine $title
  if ($hits.Count -ne 1) {
    $c = Close-Shot $title; $w = Remove-Home $ready; Remove-Item $ready, $cmd -ErrorAction SilentlyContinue
    return @("retry", "$($hits.Count) windows titled $title $w" + $(if ($c) { "" } else { "; FAIL not closed" }))
  }
  $hwnd = $hits[0]
  [void][WinCP]::ShowWindow($hwnd, 9); [void][WinCP]::SetForegroundWindow($hwnd)
  Start-Sleep -Milliseconds 700
  $r = New-Object RECT; [void][WinCP]::GetWindowRect($hwnd, [ref]$r)
  $fw = $r.R - $r.L; $fh = $r.B - $r.T
  $full = New-Object System.Drawing.Bitmap $fw, $fh
  $fg = [System.Drawing.Graphics]::FromImage($full)
  $hdc = $fg.GetHdc(); $printed = [WinCP]::PrintWindow($hwnd, $hdc, 2); $fg.ReleaseHdc($hdc)
  $count = { $d = @{}
    for ($sy = 20; $sy -lt $fh - 20; $sy += 5) { for ($sx = 20; $sx -lt $fw - 20; $sx += 7) { $d[$full.GetPixel($sx, $sy).ToArgb()] = 1 } }
    $d.Count }
  $n = & $count; $method = "PrintWindow"
  if (-not $printed -or $n -lt 8) {
    $method = "CopyFromScreen (PrintWindow gave $n colours)"
    $fg.CopyFromScreen($r.L, $r.T, 0, 0, $full.Size); $n = & $count }
  $status = "ok"; $msg = ""
  if ($n -lt 8) { $status = "retry"; $msg = "rejected: $n colours sampled via $method" }
  else {
    $cw = $fw - 16; $ch = $fh - 8
    $bmp = New-Object System.Drawing.Bitmap $cw, $ch
    $bg = [System.Drawing.Graphics]::FromImage($bmp)
    $bg.DrawImage($full, (New-Object System.Drawing.Rectangle 0, 0, $cw, $ch),
                  (New-Object System.Drawing.Rectangle 8, 0, $cw, $ch), [System.Drawing.GraphicsUnit]::Pixel)
    $bmp.Save((Join-Path $here "$scene`_$size.png"), [System.Drawing.Imaging.ImageFormat]::Png)
    $bg.Dispose(); $bmp.Dispose()
    $msg = "($cw x $ch, $n colours sampled) via $method, try $try, state $state"
  }
  $fg.Dispose(); $full.Dispose()
  $c = Close-Shot $title; $w = Remove-Home $ready
  Remove-Item $ready, $cmd -ErrorAction SilentlyContinue
  if (-not $c) { $msg += " - FAIL: window $title not closed" } else { $msg += " - window closed" }
  if ($w) { $msg += " - $w" }
  return @($status, $msg)
}
$log = @()
foreach ($scene in $Scenes) { foreach ($size in ($Sizes -split ",")) {
  for ($try = 1; $try -le 3; $try++) {
    $res = Shoot-Once $scene $size $try
    if ($res[0] -eq "ok") { $log += "ok   $scene $size $($res[1])"; break }
    $log += "try  $scene $size : $($res[1])"
    if ($try -eq 3) { $log += "FAIL $scene $size : 3 tries" }
  }
  Write-Output $log[-1] } }
$log | Add-Content -Encoding utf8 (Join-Path $here "capture-log.txt")
$left = @(Mine "mrb-")
if ($left.Count -gt 0) { Write-Output "FAIL: $($left.Count) mrb-* window(s) still open"; exit 1 }
Write-Output "no mrb-* window left open"
