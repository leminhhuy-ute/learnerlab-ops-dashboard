$ErrorActionPreference = 'Stop'
$root = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$docx = Join-Path $root 'dist\Bao_cao_tuan_1_Learner_Lab_Ops_Dashboard_24110019.docx'
if (-not (Test-Path -LiteralPath $docx)) { throw "Missing report: $docx" }

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
    Write-Output 'Opening report in Word...'
    $document = $word.Documents.Open($docx, $false, $false)
    try {
        Write-Output 'Updating table of contents...'
        if ($document.TablesOfContents.Count -ne 1) { throw 'Expected one Word table of contents.' }
        $document.TablesOfContents.Item(1).Update()
        Write-Output 'Saving DOCX...'
        $document.Save()
    }
    finally {
        $document.Close($false)
    }
}
finally {
    $word.Quit()
}
Write-Output "Updated clickable TOC: $docx"
