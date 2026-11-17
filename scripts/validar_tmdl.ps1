# Valida o modelo TMDL com o parser oficial (Microsoft.AnalysisServices.Tabular), sem abrir o Power BI Desktop.
# Uso: powershell -File validar_tmdl.ps1   (baixa a biblioteca para a pasta temporária se ainda não existir)
$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
$dir = Join-Path $env:TEMP 'tom_nuget'
$lib = Join-Path $dir 'pkg\lib\net45'
if (-not (Test-Path (Join-Path $lib 'Microsoft.AnalysisServices.Tabular.dll'))) {
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
    Invoke-WebRequest -Uri 'https://www.nuget.org/api/v2/package/Microsoft.AnalysisServices.retail.amd64' -OutFile (Join-Path $dir 'tom.zip') -UseBasicParsing
    Expand-Archive -Path (Join-Path $dir 'tom.zip') -DestinationPath (Join-Path $dir 'pkg') -Force
}
foreach ($n in 'Microsoft.AnalysisServices.Core', 'Microsoft.AnalysisServices.Tabular.Json', 'Microsoft.AnalysisServices', 'Microsoft.AnalysisServices.Tabular') {
    Add-Type -Path (Join-Path $lib "$n.dll")
}
$modelo = Join-Path (Split-Path $PSScriptRoot -Parent) 'RAIS Emprego Formal.SemanticModel\definition'
try {
    $db = [Microsoft.AnalysisServices.Tabular.TmdlSerializer]::DeserializeDatabaseFromFolder($modelo)
    $m = $db.Model
    "OK: modelo carregado. Tabelas: $($m.Tables.Count) · relações: $($m.Relationships.Count)"
    $med = $m.Tables['_medidas'].Measures
    "Medidas em _medidas: $($med.Count)"
    foreach ($nome in 'Ct_Mul_Valor', 'Ct_Neg_Valor_AFL', 'Ct_Esc_Valor') {
        $x = $med[$nome]
        "{0}: formatStringDefinition = {1}" -f $nome, ($(if ($x.FormatStringDefinition) { $x.FormatStringDefinition.Expression } else { '(nenhum)' }))
    }
    foreach ($t in 'D_Ct_Modo', 'D_Ct_Setor', 'D_Ct_MetMul', 'D_Ct_MetNeg', 'D_Ct_MetEsc', 'D_Ct_Nivel') { "{0}: {1}" -f $t, [bool]$m.Tables.Find($t) }
} catch {
    "ERRO: " + $_.Exception.Message
    $i = $_.Exception.InnerException
    while ($i) { "  -> " + $i.Message; $i = $i.InnerException }
    exit 1
}
