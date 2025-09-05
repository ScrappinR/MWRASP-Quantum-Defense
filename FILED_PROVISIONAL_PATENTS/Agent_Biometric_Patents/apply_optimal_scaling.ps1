# Apply Optimal Scaling to All Patent SVG Files
Write-Host "APPLYING OPTIMAL SCALING TO ALL PATENT FIGURES" -ForegroundColor Green
Write-Host "=" * 50

$directories = @(
    "01_Adaptive_Multi_Modal_AI_Agent_Authentication",
    "02_AI_Agent_Computational_Biometric_Identification", 
    "03_Clandestine_AI_Agent_Communication_Through_Biometric_Channels"
)

$totalProcessed = 0

foreach ($dir in $directories) {
    if (Test-Path $dir) {
        Write-Host ""
        Write-Host "Processing: $dir" -ForegroundColor Yellow
        
        $svgFiles = Get-ChildItem -Path $dir -Filter "FIGURE_*.svg"
        
        foreach ($svgFile in $svgFiles) {
            $fileName = $svgFile.Name
            
            # Skip Figure 2 as it's already working correctly
            if ($fileName -like "*FIGURE_2_CONTEXTUAL_ADAPTATION*") {
                Write-Host "  SKIPPING: $fileName (reference figure)" -ForegroundColor Green
                continue
            }
            
            Write-Host "  Processing: $fileName"
            
            try {
                $content = Get-Content $svgFile.FullName -Raw
                
                # Check if it has the old 3.2x scaling
                if ($content -match 'transform="scale\(3\.2\) translate\(100, 50\)"') {
                    # Replace with optimized scaling
                    $newContent = $content -replace 'transform="scale\(3\.2\) translate\(100, 50\)"', 'transform="scale(2.5) translate(250, 200)"'
                    
                    # Also update the comment
                    $newContent = $newContent -replace '<!-- Scaled and centered content -->', '<!-- Optimally scaled and centered content -->'
                    
                    $newContent | Set-Content $svgFile.FullName -Encoding UTF8
                    Write-Host "    UPDATED: Applied 2.5x scaling with better centering" -ForegroundColor Green
                    $totalProcessed++
                }
                elseif ($content -match 'transform="scale\(3\.2\)') {
                    # Handle other 3.2x scaling variations
                    $newContent = $content -replace 'transform="scale\(3\.2\)[^"]*"', 'transform="scale(2.5) translate(250, 200)"'
                    $newContent | Set-Content $svgFile.FullName -Encoding UTF8
                    Write-Host "    UPDATED: Applied 2.5x scaling (variation)" -ForegroundColor Green
                    $totalProcessed++
                }
                else {
                    Write-Host "    SKIPPED: No 3.2x scaling found" -ForegroundColor Gray
                }
            }
            catch {
                Write-Host "    ERROR: $($_.Exception.Message)" -ForegroundColor Red
            }
        }
    }
}

Write-Host ""
Write-Host "=" * 50
Write-Host "OPTIMAL SCALING APPLICATION COMPLETE" -ForegroundColor Green
Write-Host "Total files updated: $totalProcessed"
Write-Host ""
Write-Host "All SVG files now use 2.5x scaling with translate(250, 200) for optimal content fitting."