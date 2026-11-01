$title = "cpi-kittyq-" + (Get-Random)
$out = Join-Path $PSScriptRoot "kq.log"; Remove-Item $out -ErrorAction SilentlyContinue
$py = Join-Path $env:USERPROFILE "anaconda3\python.exe"
cmd /c "wt.exe -w new --title $title --suppressApplicationTitle `"$py`" `"$PSScriptRoot\kq.py`" `"$out`""
for ($i=0; $i -lt 40 -and -not (Test-Path $out); $i++) { Start-Sleep -Milliseconds 500 }
Start-Sleep -Seconds 1
Add-Type @"
using System; using System.Runtime.InteropServices; using System.Text;
public class KQ { public delegate bool EnumProc(IntPtr h, IntPtr l);
 [DllImport("user32.dll")] public static extern bool EnumWindows(EnumProc p, IntPtr l);
 [DllImport("user32.dll", CharSet=CharSet.Unicode)] public static extern int GetWindowText(IntPtr h, StringBuilder s, int n);
 [DllImport("user32.dll")] public static extern bool PostMessage(IntPtr h, uint m, IntPtr w, IntPtr l); }
"@
$script:hits=@(); [KQ]::EnumWindows({ param($h,$l) $sb=New-Object Text.StringBuilder 512; [void][KQ]::GetWindowText($h,$sb,512); if ($sb.ToString() -eq $title) { $script:hits += $h }; $true }, [IntPtr]::Zero) | Out-Null
foreach ($h in $script:hits) { [void][KQ]::PostMessage($h, 0x0010, [IntPtr]::Zero, [IntPtr]::Zero) }
"closed: $($script:hits.Count)"
Get-Content $out -Encoding UTF8
(Get-AppxPackage Microsoft.WindowsTerminal*).Version
