# Delete Old Problematic Patent Drawing PDFs
Write-Host "DELETING OLD PROBLEMATIC PATENT DRAWING PDFs" -ForegroundColor Red
Write-Host "=" * 50

$directories = @(
    "01_Adaptive_Multi_Modal_AI_Agent_Authentication",
    "02_AI_Agent_Computational_Biometric_Identification", 
    "03_Clandestine_AI_Agent_Communication_Through_Biometric_Channels"
)

$problematicSuffixes = @("_ENHANCED", "_FIXED", "_TEST", "._ENHANCED")
$totalDeleted = 0

foreach ($dir in $directories) {
    if (Test-Path $dir) {
        Write-Host ""
        Write-Host "Processing: $dir" -ForegroundColor Yellow
        
        # Get all PDF files in the directory
        $pdfFiles = Get-ChildItem -Path $dir -Filter "FIGURE_*.pdf"
        
        foreach ($pdfFile in $pdfFiles) {
            $fileName = $pdfFile.BaseName
            $shouldDelete = $false
            
            # Check if it matches any problematic suffix
            foreach ($suffix in $problematicSuffixes) {
                if ($fileName.EndsWith($suffix)) {
                    $shouldDelete = $true
                    break
                }
            }
            
            if ($shouldDelete) {
                try {
                    # Force close any processes that might have the file open
                    $processes = Get-Process | Where-Object { $_.MainWindowTitle -like "*$($pdfFile.Name)*" }
                    foreach ($process in $processes) {
                        try {
                            $process.CloseMainWindow()
                            Start-Sleep -Milliseconds 500
                            if (!$process.HasExited) {
                                $process.Kill()
                            }
                        } catch {
                            # Ignore process termination errors
                        }
                    }
                    
                    # Wait a moment then delete
                    Start-Sleep -Milliseconds 1000
                    Remove-Item $pdfFile.FullName -Force -ErrorAction Stop
                    Write-Host "  DELETED: $($pdfFile.Name)" -ForegroundColor Red
                    $totalDeleted++
                }
                catch {
                    Write-Host "  FAILED to delete: $($pdfFile.Name) - $($_.Exception.Message)" -ForegroundColor Yellow
                }
            }
            else {
                Write-Host "  KEPT: $($pdfFile.Name)" -ForegroundColor Green
            }
        }
    }
}

Write-Host ""
Write-Host "=" * 50
Write-Host "OLD PDF CLEANUP COMPLETE" -ForegroundColor Red
Write-Host "Total problematic PDFs deleted: $totalDeleted"
Write-Host ""
Write-Host "Only the newly regenerated PDFs with proper scaling remain."