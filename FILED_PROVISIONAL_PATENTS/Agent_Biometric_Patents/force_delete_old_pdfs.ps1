# Force Delete Old Problematic Patent Drawing PDFs
Write-Host "FORCE DELETING OLD PROBLEMATIC PDFs" -ForegroundColor Red
Write-Host "=" * 40

# Close any PDF viewers that might be open
$pdfProcesses = @("AcroRd32", "Acrobat", "FoxitReader", "PDFXEdit", "SumatraPDF", "msedge", "chrome", "firefox")
foreach ($processName in $pdfProcesses) {
    try {
        Get-Process -Name $processName -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
        Write-Host "Closed $processName processes" -ForegroundColor Yellow
    } catch {
        # Ignore errors
    }
}

Start-Sleep -Seconds 2

# Now delete the problematic files using more specific patterns
$filesToDelete = @(
    "01_Adaptive_Multi_Modal_AI_Agent_Authentication\FIGURE_1_SYSTEM_ARCHITECTURE._ENHANCED.pdf",
    "01_Adaptive_Multi_Modal_AI_Agent_Authentication\FIGURE_1_SYSTEM_ARCHITECTURE_FIXED.pdf", 
    "01_Adaptive_Multi_Modal_AI_Agent_Authentication\FIGURE_1_TEST.pdf",
    "01_Adaptive_Multi_Modal_AI_Agent_Authentication\FIGURE_2_CONTEXTUAL_ADAPTATION._ENHANCED.pdf",
    "01_Adaptive_Multi_Modal_AI_Agent_Authentication\FIGURE_2_CONTEXTUAL_ADAPTATION_FIXED.pdf",
    "01_Adaptive_Multi_Modal_AI_Agent_Authentication\FIGURE_3_SELF_EVOLVING_TEMPLATES._ENHANCED.pdf",
    "01_Adaptive_Multi_Modal_AI_Agent_Authentication\FIGURE_3_SELF_EVOLVING_TEMPLATES_FIXED.pdf",
    "01_Adaptive_Multi_Modal_AI_Agent_Authentication\FIGURE_4_PARTNER_SPECIFIC_MODELING._ENHANCED.pdf",
    "01_Adaptive_Multi_Modal_AI_Agent_Authentication\FIGURE_4_PARTNER_SPECIFIC_MODELING_FIXED.pdf",
    "01_Adaptive_Multi_Modal_AI_Agent_Authentication\FIGURE_5_MULTI_MODAL_FUSION._ENHANCED.pdf",
    "01_Adaptive_Multi_Modal_AI_Agent_Authentication\FIGURE_5_MULTI_MODAL_FUSION_FIXED.pdf"
)

$deleted = 0
foreach ($file in $filesToDelete) {
    if (Test-Path $file) {
        try {
            # Use cmd to force delete
            $fullPath = Resolve-Path $file
            cmd /c "del /f /q `"$fullPath`""
            
            if (-not (Test-Path $file)) {
                Write-Host "  DELETED: $file" -ForegroundColor Red
                $deleted++
            } else {
                Write-Host "  STILL EXISTS: $file" -ForegroundColor Yellow
            }
        }
        catch {
            Write-Host "  FAILED: $file - $($_.Exception.Message)" -ForegroundColor Red
        }
    }
}

Write-Host ""
Write-Host "Total old PDFs deleted: $deleted"
Write-Host ""
Write-Host "Listing remaining PDFs:" -ForegroundColor Green
Get-ChildItem -Path "01_Adaptive_Multi_Modal_AI_Agent_Authentication" -Filter "FIGURE_*.pdf" | ForEach-Object {
    Write-Host "  $($_.Name)" -ForegroundColor Green
}