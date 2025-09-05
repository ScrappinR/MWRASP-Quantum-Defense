# Simple SVG Dimension Fix
# ========================
# Fix SVG viewBox and dimensions to prevent cut-off

Write-Host "Fixing SVG dimensions for all patent drawings..." -ForegroundColor Green

$patentFolders = Get-ChildItem -Directory | Where-Object { $_.Name -match "^\d+_" }

foreach ($folder in $patentFolders) {
    Write-Host ""
    Write-Host "Processing folder: $($folder.Name)" -ForegroundColor Yellow
    
    $svgFiles = Get-ChildItem -Path $folder.FullName -Filter "FIGURE_*.svg"
    
    foreach ($svgFile in $svgFiles) {
        Write-Host "  Fixing: $($svgFile.Name)"
        
        try {
            $content = Get-Content $svgFile.FullName -Raw
            
            # Check if already has proper dimensions
            if ($content -match 'width="2550"' -and $content -match 'height="3300"') {
                Write-Host "    Already fixed - skipping"
                continue
            }
            
            # Standard patent drawing dimensions
            $newSvgTag = '<svg width="2550" height="3300" viewBox="0 0 2550 3300" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">'
            
            # Replace SVG tag
            $fixedContent = $content -replace '<svg[^>]*>', $newSvgTag
            
            # Also ensure all content is properly scaled
            if ($fixedContent -notmatch 'transform="scale') {
                # Add scaling transform to main group if needed
                $fixedContent = $fixedContent -replace '(<g[^>]*>)', '$1<g transform="scale(0.8)">'
                $fixedContent = $fixedContent -replace '</svg>', '</g></svg>'
            }
            
            # Save fixed SVG
            $fixedContent | Set-Content $svgFile.FullName -Encoding UTF8
            
            Write-Host "    Fixed: dimensions 2550x3300, viewBox 0 0 2550 3300" -ForegroundColor Green
        }
        catch {
            Write-Host "    ERROR: $($_.Exception.Message)" -ForegroundColor Red
        }
    }
}

Write-Host ""
Write-Host "SVG dimension fix complete!" -ForegroundColor Green
Write-Host "Now the SVG files should display properly when converted to PDF."
Write-Host ""
Write-Host "Next step: Use your existing HTML conversion methods to regenerate PDFs from the fixed SVG files."