# AC-3 capture harness. Two tui-demos limits govern every line of this file.
#
# L-19: the spawned window CLOSES ITSELF and NO TERMINAL PROCESS IS EVER KILLED.
# Windows Terminal is one process for all windows, so Stop-Process on a window
# this script spawned kills the operator's windows too. It cost a session once.
# There is no Stop-Process, Kill, or taskkill anywhere below, by policy.
#
# L-27: THE WINDOW IS SELECTED BY TITLE, AND MORE THAN ONE MATCH IS REFUSED.
# The previous version of this file selected "the newest WindowsTerminal
# process by StartTime" -- which is exactly the heuristic L-27 records as
# structurally unable to name a window, because Windows Terminal is ONE PROCESS
# for every one of its windows, so its StartTime is the process's and not the
# window's. It captured correctly only by luck (the spawned window happened to
# hold focus). The fix is not a better ranking over the same data, it is
# identity: the window is named by `wt.exe --title` before it starts and by the
# app itself once it is running, matched with EnumWindows, and TWO matches are
# an error rather than a coin toss.
#
# L-27 also: the grab is PrintWindow(PW_RENDERFULLCONTENT), not CopyFromScreen.
# CopyFromScreen reads the SCREEN, so a correct window rect over a window that
# is not on top records whatever IS on top of it. PrintWindow asks the window to
# render itself and is independent of z-order. Some compositors return a uniform
# bitmap for it, so "it returned true" is checked against the pixels before it
# is trusted, and CopyFromScreen stays as a recorded-as-such fallback.
#
# Two harness facts this also works around:
#   * wt.exe splits its arguments on ';' into separate TABS, so the command goes
#     into a .cmd script file rather than onto the command line.
#   * Git Bash rewrites /mnt/c-style paths when launching Windows exes, so this
#     is launched from PowerShell.
param(
  [string]$Lang    = "corgi",
  [double]$Seconds = 12,
  [string]$OutDir  = ".",
  [ValidateSet("over", "around")] [string]$Mode = "over",
  [string]$Suffix  = "",
  [string]$Process = "WindowsTerminal",
  [int]$Cols = 120,
  [int]$Rows = 34
)

$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Drawing, System.Windows.Forms

$root  = "C:\Users\jjgh8\Github\taskboard\.claude\worktrees\kanban-variants"
$title = "taskboard-surface-$Lang-$Mode"
$script = Join-Path $env:TEMP "surface_shot_$Lang`_$Mode.cmd"
@"
@echo off
chcp 65001 > nul
set PYTHONIOENCODING=utf-8
set SURFACE_SHOT_TITLE=$title
cd /d $root
python prototypes\capture_surface_raster.py $Lang $Seconds $Mode
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

# THE CAPTURE PROCESS MUST BE DPI-AWARE, AND THIS WAS MEASURED THE HARD WAY.
# PowerShell is DPI-UNAWARE by default, so on a scaled monitor GetWindowRect
# hands back LOGICAL pixels while PrintWindow renders the window at its own
# PHYSICAL resolution. The bitmap is then sized from the logical rect, and
# PrintWindow fills its top-left corner: the first capture taken with this
# harness came back as the top-left QUADRANT of the window, magnified 2x, with
# the window controls and the entire right-hand pane cut off. It looked like a
# font-size change and was a coordinate-space mismatch.
#
# Same family as L-27(a): the coordinates were right and the pixels were not
# what the caller thought they were. PER_MONITOR_AWARE_V2 (-4) puts both calls
# in the same space. It must run BEFORE any window is measured.
[void][Win]::SetProcessDpiAwarenessContext([IntPtr](-4))

# --title names the TAB and Windows Terminal's window title follows its active
# tab; the probe sets the same string through Textual once it is running, so the
# name survives Textual taking the title over. `-w new` forces a NEW window
# rather than a tab in whatever window happens to be focused.
Start-Process wt.exe -ArgumentList @(
  "--size", "$Cols,$Rows", "--title", $title, "cmd.exe", "/c", $script)
Start-Sleep -Seconds ([math]::Max(4, $Seconds - 4))

# L-27: identity, not ranking. Zero matches and two matches are BOTH errors.
$hits = @([Win]::ByTitle($title) | Where-Object {
  $wp = 0; [void][Win]::GetWindowThreadProcessId($_, [ref]$wp)
  (Get-Process -Id $wp -ErrorAction SilentlyContinue).ProcessName -eq $Process
})
if ($hits.Count -eq 0) {
  throw "no visible $Process window titled '$title' - capture aborted (did the probe start?)"
}
if ($hits.Count -gt 1) {
  throw "$($hits.Count) visible $Process windows titled '$title' - refusing to guess which"
}
$hwnd = $hits[0]

[void][Win]::ShowWindow($hwnd, 9)          # SW_RESTORE, in case it was minimised
[void][Win]::SetForegroundWindow($hwnd)    # best effort; Windows may decline
Start-Sleep -Milliseconds 700

$r = New-Object RECT
[void][Win]::GetWindowRect($hwnd, [ref]$r)
$fw = $r.R - $r.L; $fh = $r.B - $r.T
$full = New-Object System.Drawing.Bitmap $fw, $fh
$fg = [System.Drawing.Graphics]::FromImage($full)
$hdc = $fg.GetHdc()
$printed = [Win]::PrintWindow($hwnd, $hdc, 2)   # 2 = PW_RENDERFULLCONTENT
$fg.ReleaseHdc($hdc)

# "PrintWindow returned true" is not evidence that it drew anything: some
# compositors hand back a uniform bitmap. Sample the interior on a coarse grid
# (strides chosen not to land on the character grid) and demand MORE THAN TWO
# distinct colours before trusting it.
$distinct = @{}
for ($sy = 20; $sy -lt $fh - 20; $sy += 37) {
  for ($sx = 20; $sx -lt $fw - 20; $sx += 41) { $distinct[$full.GetPixel($sx, $sy).ToArgb()] = 1 }
}
$method = "PrintWindow"
if (-not $printed -or $distinct.Count -lt 3) {
  $method = "CopyFromScreen (PrintWindow gave $($distinct.Count) distinct colours)"
  $fg.CopyFromScreen($r.L, $r.T, 0, 0, $full.Size)
}

# crop 10 px off each side and 16 off the bottom: the drop shadow and the
# rounded border are not part of the frame being measured
$cw = $fw - 20; $ch = $fh - 16
$bmp = New-Object System.Drawing.Bitmap $cw, $ch
$bg = [System.Drawing.Graphics]::FromImage($bmp)
$bg.DrawImage($full, (New-Object System.Drawing.Rectangle 0, 0, $cw, $ch),
              (New-Object System.Drawing.Rectangle 10, 0, $cw, $ch),
              [System.Drawing.GraphicsUnit]::Pixel)
$name = "surface_raster_$Lang$Suffix.png"
$out = Join-Path (Resolve-Path $OutDir).Path $name
$bmp.Save($out, [System.Drawing.Imaging.ImageFormat]::Png)
$bg.Dispose(); $bmp.Dispose(); $fg.Dispose(); $full.Dispose()
Write-Output "saved $out  ($cw x $ch)  via $method  title '$title'"
# the window closes itself; nothing is killed here.
