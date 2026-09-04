# AC-5 capture harness. LIMITS L-19: the spawned window CLOSES ITSELF and no
# terminal process is ever killed -- Windows Terminal is one process for all
# windows, and Stop-Process on a spawned window kills the operator's too.
#
# Two harness facts this works around:
#   * wt.exe splits its arguments on ';' into separate TABS, so the command
#     goes into a .cmd script file rather than onto the command line.
#   * Git Bash rewrites /mnt/c-style paths when launching Windows exes, so this
#     is launched from PowerShell.
param([string]$Lang = "corgi", [double]$Seconds = 8, [string]$OutDir = ".")

$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Drawing, System.Windows.Forms

$root = "C:\Users\jjgh8\Github\taskboard\.claude\worktrees\kanban-variants"
$script = Join-Path $env:TEMP "surface_shot_$Lang.cmd"
@"
@echo off
chcp 65001 > nul
set PYTHONIOENCODING=utf-8
cd /d $root
python prototypes\capture_surface_raster.py $Lang $Seconds
"@ | Set-Content -Encoding ascii $script

$before = @(Get-Process WindowsTerminal -ErrorAction SilentlyContinue |
            Select-Object -ExpandProperty Id)

Start-Process wt.exe -ArgumentList @("--size","120,34","cmd.exe","/c",$script)
Start-Sleep -Seconds ([math]::Max(3, $Seconds - 3))

# the NEWEST WindowsTerminal window -- by start time, so an already-open one
# is never the target
$proc = Get-Process WindowsTerminal | Sort-Object StartTime -Descending |
        Select-Object -First 1
$h = $proc.MainWindowHandle
if ($h -eq 0) { throw "no window handle on WindowsTerminal pid $($proc.Id)" }

Add-Type @"
using System;
using System.Runtime.InteropServices;
public struct RECT { public int L, T, R, B; }
public class W {
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
}
"@ -ErrorAction SilentlyContinue

[void][W]::SetForegroundWindow($h)
Start-Sleep -Milliseconds 700
$r = New-Object RECT
[void][W]::GetWindowRect($h, [ref]$r)

# crop 10 px off each side and 16 off the bottom: the drop shadow and the
# rounded border are not part of the frame being measured
$x = $r.L + 10; $y = $r.T
$w = ($r.R - $r.L) - 20; $hh = ($r.B - $r.T) - 16
$bmp = New-Object System.Drawing.Bitmap $w, $hh
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.CopyFromScreen($x, $y, 0, 0, $bmp.Size)
$out = Join-Path (Resolve-Path $OutDir).Path "surface_raster_$Lang.png"
$bmp.Save($out, [System.Drawing.Imaging.ImageFormat]::Png)
$g.Dispose(); $bmp.Dispose()
Write-Output "saved $out  ($w x $hh)"
# the window closes itself; nothing is killed here.

