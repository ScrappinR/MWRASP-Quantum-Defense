# Fix SVG Scaling for All Patent Drawings
# =====================================
# Scale all SVG content to fill the proper canvas size like the working Figure 2

Write-Host "COMPREHENSIVE SVG SCALING FIX" -ForegroundColor Green
Write-Host "=" * 40
Write-Host "Analyzing working figure and applying scaling to all others"

function Scale-SVGContent {
    param(
        [string]$svgPath
    )
    
    Write-Host "Processing: $(Split-Path $svgPath -Leaf)"
    
    try {
        $content = Get-Content $svgPath -Raw
        
        # Check if this is the working Figure 2 (skip it)
        if ($svgPath -like "*FIGURE_2_CONTEXTUAL_ADAPTATION*") {
            Write-Host "  SKIPPING: This is the working reference figure" -ForegroundColor Green
            return $true
        }
        
        # The issue is that most figures have small coordinates that need to be scaled up
        # We need to wrap all content in a transform group to scale it properly
        
        # Find the main content (everything after </defs> and before </svg>)
        if ($content -match '(?s)<\/defs>\s*(.*?)\s*<\/svg>') {
            $mainContent = $matches[1]
            
            # Create scaled version with proper centering
            $scaledContent = @"
<?xml version="1.0" encoding="UTF-8"?>
<svg width="2550" height="3300" viewBox="0 0 2550 3300" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <style>
      .title-text { font-family: Arial, sans-serif; font-size: 36px; font-weight: bold; text-anchor: middle; }
      .label-text { font-family: Arial, sans-serif; font-size: 28px; text-anchor: middle; }
      .small-text { font-family: Arial, sans-serif; font-size: 22px; text-anchor: middle; }
      .tiny-text { font-family: Arial, sans-serif; font-size: 18px; text-anchor: middle; }
      .module-box { fill: none; stroke: black; stroke-width: 4; }
      .sub-module { fill: lightgray; stroke: black; stroke-width: 2; }
      .connection-line { stroke: black; stroke-width: 2; fill: none; }
      .decision-diamond { fill: white; stroke: black; stroke-width: 4; }
      .process-flow { stroke: black; stroke-width: 4; fill: none; marker-end: url(#arrowhead); }
      .assessment-box { fill: #f0f0f0; stroke: black; stroke-width: 2; }
      .data-flow { stroke: black; stroke-width: 2; fill: none; stroke-dasharray: 10,10; }
      .input-box { fill: lightgray; stroke: black; stroke-width: 2; }
      .output-box { fill: white; stroke: black; stroke-width: 4; }
    </style>
    <marker id="arrowhead" markerWidth="20" markerHeight="14" refX="20" refY="7" orient="auto">
      <polygon points="0 0, 20 7, 0 14" fill="black" />
    </marker>
  </defs>
  
  <!-- Scaled and centered content -->
  <g transform="scale(3.2) translate(100, 50)">
    $mainContent
  </g>
  
</svg>
"@
            
            # Write the scaled content back to file
            $scaledContent | Set-Content $svgPath -Encoding UTF8
            
            Write-Host "  FIXED: Applied 3.2x scaling with centering" -ForegroundColor Green
            return $true
        }
        else {
            Write-Host "  WARNING: Could not parse SVG structure" -ForegroundColor Yellow
            return $false
        }
    }
    catch {
        Write-Host "  ERROR: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Process all patent folders
$patentFolders = Get-ChildItem -Directory | Where-Object { $_.Name -match "^\d+_" }
$totalFixed = 0

foreach ($folder in $patentFolders) {
    Write-Host ""
    Write-Host "Processing folder: $($folder.Name)" -ForegroundColor Yellow
    
    $svgFiles = Get-ChildItem -Path $folder.FullName -Filter "FIGURE_*.svg" | Sort-Object Name
    
    foreach ($svgFile in $svgFiles) {
        $success = Scale-SVGContent -svgPath $svgFile.FullName
        if ($success) {
            $totalFixed++
        }
    }
}

Write-Host ""
Write-Host "=" * 40
Write-Host "SVG SCALING FIX COMPLETE" -ForegroundColor Green
Write-Host "Total files processed: $totalFixed"
Write-Host ""
Write-Host "All figures should now display at proper scale when converted to PDF."
Write-Host "Next step: Re-run the PDF conversion script."

Write-Host ""
Write-Host "Press any key to continue..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")