# Convert a .docx to .pdf with Microsoft Word (COM). Windows + Word required.
# Usage: powershell -NoProfile -ExecutionPolicy Bypass -File docx2pdf.ps1 <input.docx> [output.pdf]
param(
    [Parameter(Mandatory = $true)][string]$Docx,
    [string]$Pdf
)
$Docx = (Resolve-Path $Docx).Path
if (-not $Pdf) { $Pdf = [System.IO.Path]::ChangeExtension($Docx, '.pdf') }
try {
    $w = New-Object -ComObject Word.Application
    $w.Visible = $false
    $d = $w.Documents.Open($Docx)
    $d.SaveAs2($Pdf, 17)
    Write-Output ("pages: " + $d.ComputeStatistics(2))
    $d.Close($false)
    $w.Quit()
    Write-Output "PDF OK: $Pdf"
} catch {
    Write-Output ("Word COM failed: " + $_.Exception.Message)
    Write-Output "Fallback: open the .docx in Word/LibreOffice and export PDF manually, or run: soffice --headless --convert-to pdf <docx>"
    exit 1
}
