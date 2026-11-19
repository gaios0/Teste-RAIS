param([int]$Port, [string]$File)
# Roda uma consulta DAX no modelo aberto no Power BI Desktop (msmdsrv local). Só leitura.
$dll = Get-ChildItem (Join-Path $env:KIROCREW_SCRATCH "adomd\pkg\lib\net45\Microsoft.AnalysisServices.AdomdClient.dll") -ErrorAction SilentlyContinue | Select-Object -First 1
if (-not $dll) { $dll = Get-ChildItem "C:\Program Files\WindowsApps\Microsoft.MicrosoftPowerBIDesktop_*\bin\Microsoft.AnalysisServices.AdomdClient.dll" -ErrorAction SilentlyContinue | Select-Object -First 1 }
Add-Type -Path $dll.FullName
$q = Get-Content $File -Raw -Encoding UTF8
$c = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:$Port")
$c.Open()
$cmd = $c.CreateCommand(); $cmd.CommandText = $q
$r = $cmd.ExecuteReader()
$cols = 0..($r.FieldCount - 1) | ForEach-Object { $r.GetName($_) }
($cols -join " | ")
while ($r.Read()) { (0..($r.FieldCount - 1) | ForEach-Object { $r.GetValue($_) }) -join " | " }
$c.Close()
