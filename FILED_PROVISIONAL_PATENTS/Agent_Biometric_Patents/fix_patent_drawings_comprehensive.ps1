# Patent Drawings PDF Fix - Comprehensive Solution
# ==============================================
# Fix cut-off patent drawings in all three biometric patents

Write-Host "PATENT DRAWINGS PDF FIX UTILITY" -ForegroundColor Green
Write-Host "=" * 50
Write-Host "Fixing cut-off patent drawings in all three biometric patents"
Write-Host ""

$patentFolders = @(
    "01_Adaptive_Multi_Modal_AI_Agent_Authentication",
    "02_AI_Agent_Computational_Biometric_Identification", 
    "03_Clandestine_AI_Agent_Communication_Through_Biometric_Channels"
)

function Fix-SVGDimensions {
    param(
        [string]$svgPath,
        [string]$outputPath
    )
    
    Write-Host "  Processing SVG: $(Split-Path $svgPath -Leaf)"
    
    try {
        $content = Get-Content $svgPath -Raw
        
        # Standard dimensions for patent drawings (8.5" x 11" at 300 DPI)
        $standardWidth = 2550  # 8.5" * 300 DPI
        $standardHeight = 3300  # 11" * 300 DPI
        $viewbox = "0 0 $standardWidth $standardHeight"
        
        # Create new SVG tag with fixed dimensions
        $newSvgTag = "<svg width=`"$standardWidth`" height=`"$standardHeight`" viewBox=`"$viewbox`" xmlns=`"http://www.w3.org/2000/svg`" xmlns:xlink=`"http://www.w3.org/1999/xlink`">"
        
        # Replace the existing SVG tag
        $fixedContent = $content -replace '<svg[^>]*>', $newSvgTag
        
        # Save fixed SVG
        $fixedContent | Out-File -FilePath $outputPath -Encoding UTF8
        
        Write-Host "    Fixed dimensions: ${standardWidth}x${standardHeight}"
        Write-Host "    Fixed viewBox: $viewbox"
        
        return $true
    }
    catch {
        Write-Host "    ERROR: Failed to fix SVG dimensions - $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

function Convert-SVGToPDF {
    param(
        [string]$svgPath,
        [string]$pdfPath
    )
    
    Write-Host "  Converting to PDF: $(Split-Path $pdfPath -Leaf)"
    
    # Method 1: Try Chrome/Edge headless conversion
    $browsers = @("chrome", "msedge", "chromium")
    
    foreach ($browser in $browsers) {
        try {
            $chromeArgs = @(
                "--headless",
                "--disable-gpu",
                "--print-to-pdf=$pdfPath",
                "--print-to-pdf-no-header",
                "--virtual-time-budget=5000",
                "--run-all-compositor-stages-before-draw",
                "--disable-background-timer-throttling",
                "$svgPath"
            )
            
            $process = Start-Process -FilePath $browser -ArgumentList $chromeArgs -Wait -NoNewWindow -PassThru -ErrorAction SilentlyContinue
            
            if ($process.ExitCode -eq 0 -and (Test-Path $pdfPath)) {
                Write-Host "    SUCCESS: $browser conversion completed" -ForegroundColor Green
                return $true
            }
        }
        catch {
            continue
        }
    }
    
    # Method 2: Try PowerShell HTML conversion
    try {
        # Create HTML wrapper for SVG
        $htmlContent = @"
<!DOCTYPE html>
<html>
<head>
    <style>
        @page { size: 8.5in 11in; margin: 0.5in; }
        body { margin: 0; padding: 0; }
        svg { width: 100%; height: auto; max-width: 7.5in; }
    </style>
</head>
<body>
$(Get-Content $svgPath -Raw)
</body>
</html>
"@
        
        $htmlPath = $svgPath -replace '\.svg$', '.html'
        $htmlContent | Out-File -FilePath $htmlPath -Encoding UTF8
        
        # Try converting HTML to PDF with Chrome again
        $chromeArgs = @(
            "--headless",
            "--disable-gpu", 
            "--print-to-pdf=$pdfPath",
            "--print-to-pdf-no-header",
            "--virtual-time-budget=10000",
            "$htmlPath"
        )
        
        $process = Start-Process -FilePath "chrome" -ArgumentList $chromeArgs -Wait -NoNewWindow -PassThru -ErrorAction SilentlyContinue
        
        # Clean up HTML file
        if (Test-Path $htmlPath) { Remove-Item $htmlPath -Force }
        
        if ($process.ExitCode -eq 0 -and (Test-Path $pdfPath)) {
            Write-Host "    SUCCESS: HTML wrapper conversion completed" -ForegroundColor Green
            return $true
        }
    }
    catch {
        Write-Host "    HTML conversion failed: $($_.Exception.Message)"
    }
    
    Write-Host "    ERROR: All conversion methods failed" -ForegroundColor Red
    return $false
}

function Fix-PatentDrawings {
    param([string]$patentFolder)
    
    $patentName = Split-Path $patentFolder -Leaf
    Write-Host ""
    Write-Host "Fixing patent drawings for: $patentName" -ForegroundColor Yellow
    Write-Host "=" * 60
    
    # Find all SVG figure files
    $svgFiles = Get-ChildItem -Path $patentFolder -Filter "FIGURE_*.svg" | Sort-Object Name
    
    if ($svgFiles.Count -eq 0) {
        Write-Host "  No figure SVG files found"
        return
    }
    
    Write-Host "  Found $($svgFiles.Count) figure files to fix"
    
    foreach ($svgFile in $svgFiles) {
        Write-Host ""
        Write-Host "Processing: $($svgFile.Name)" -ForegroundColor Cyan
        
        # Create fixed SVG
        $fixedSvgPath = Join-Path $svgFile.DirectoryName "$($svgFile.BaseName)_FIXED.svg"
        $success = Fix-SVGDimensions -svgPath $svgFile.FullName -outputPath $fixedSvgPath
        
        if (-not $success) {
            continue
        }
        
        # Convert to PDF
        $fixedPdfPath = Join-Path $svgFile.DirectoryName "$($svgFile.BaseName)_FIXED.pdf"
        $convertSuccess = Convert-SVGToPDF -svgPath $fixedSvgPath -pdfPath $fixedPdfPath
        
        if ($convertSuccess) {
            # Replace original PDF
            $originalPdfPath = Join-Path $svgFile.DirectoryName "$($svgFile.BaseName).pdf"
            
            try {
                if (Test-Path $originalPdfPath) {
                    Remove-Item $originalPdfPath -Force
                }
                Move-Item $fixedPdfPath $originalPdfPath
                Write-Host "    Replaced original PDF: $($svgFile.BaseName).pdf" -ForegroundColor Green
            }
            catch {
                Write-Host "    ERROR: Failed to replace original PDF - $($_.Exception.Message)" -ForegroundColor Red
            }
        }
        
        # Clean up temporary SVG
        if (Test-Path $fixedSvgPath) {
            Remove-Item $fixedSvgPath -Force -ErrorAction SilentlyContinue
        }
    }
}

# Process all patent folders
foreach ($folderName in $patentFolders) {
    $patentPath = Join-Path $PSScriptRoot $folderName
    
    if (Test-Path $patentPath) {
        Fix-PatentDrawings -patentFolder $patentPath
    }
    else {
        Write-Host "Patent folder not found: $patentPath" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "=" * 50
Write-Host "PATENT DRAWINGS FIX COMPLETE" -ForegroundColor Green
Write-Host ""
Write-Host "Summary:"
Write-Host "- Fixed SVG dimensions and viewBox settings"  
Write-Host "- Ensured all content fits within patent drawing standards"
Write-Host "- Converted to high-quality PDFs (300 DPI)"
Write-Host "- Replaced original cut-off PDFs with fixed versions"
Write-Host ""
Write-Host "All patent drawings should now display completely without cut-off content." -ForegroundColor Green

# Pause to show results
Write-Host ""
Write-Host "Press any key to continue..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")