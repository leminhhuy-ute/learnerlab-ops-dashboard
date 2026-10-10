$ErrorActionPreference = 'Stop'
$root = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$docx = Join-Path $root 'dist\Bao_cao_tuan_1_Learner_Lab_Ops_Dashboard_24110019.docx'
$pdf = Join-Path $root 'dist\Bao_cao_tuan_1_Learner_Lab_Ops_Dashboard_24110019.pdf'
if (-not (Test-Path -LiteralPath $docx)) { throw "Missing report: $docx" }

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
    $document = $word.Documents.Open($docx, $false, $false)
    try {
        if ($document.TablesOfContents.Count -ne 1) { throw 'Expected one Word table of contents.' }
        $null = $document.Fields.Update()
        $document.TablesOfContents.Item(1).Update()
        $document.Save()
        $document.ExportAsFixedFormat($pdf, 17)
    }
    finally {
        $document.Close($false)
    }
}
finally {
    $word.Quit()
}
Write-Output "Updated clickable TOC and PDF: $pdf"
