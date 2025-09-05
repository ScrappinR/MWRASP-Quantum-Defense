# Comprehensive SVG to PDF scaling fix
Write-Output "=== COMPREHENSIVE SVG PDF SCALING FIX ==="

$edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if (-not (Test-Path $edgePath)) {
    Write-Output "Edge not found. Cannot proceed."
    exit 1
}

function Fix-SvgScaling {
    param($svgFile, $outputPdf)
    
    Write-Output "Processing: $([System.IO.Path]::GetFileName($svgFile))"
    
    # Read and analyze SVG
    $svgContent = Get-Content $svgFile -Raw -Encoding UTF8
    
    # Extract current width/height
    $widthMatch = [regex]::Match($svgContent, 'width="([^"]+)"')
    $heightMatch = [regex]::Match($svgContent, 'height="([^"]+)"')
    
    $originalWidth = if ($widthMatch.Success) { $widthMatch.Groups[1].Value } else { "800" }
    $originalHeight = if ($heightMatch.Success) { $heightMatch.Groups[1].Value } else { "600" }
    
    # Remove any existing viewBox and add a proper one that ensures all content is visible
    $svgContent = $svgContent -replace 'viewBox="[^"]*"', ''
    
    # Add viewBox that covers a larger area to catch any overflow content
    $expandedViewBox = "0 0 1000 800"  # Generous viewBox
    $svgContent = $svgContent -replace '<svg([^>]*?)>', "<svg`$1 viewBox=`"$expandedViewBox`">"
    
    # Create HTML with multiple scaling approaches
    $htmlContent = @"
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Patent Figure</title>
    <style>
        @page {
            size: letter;
            margin: 0.25in;
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
        }
        
        * {
            box-sizing: border-box;
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }
        
        html, body {
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            background: white;
            overflow: hidden;
        }
        
        .page-container {
            width: 8in;
            height: 10.5in;
            margin: 0 auto;
            background: white;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            page-break-inside: avoid;
            position: relative;
        }
        
        .svg-wrapper {
            width: 7.5in;
            height: 10in;
            display: flex;
            justify-content: center;
            align-items: center;
            background: white;
            border: 1px solid #eee;
            overflow: hidden;
        }
        
        svg {
            max-width: 100% !important;
            max-height: 100% !important;
            width: auto !important;
            height: auto !important;
            display: block !important;
            background: white !important;
        }
        
        /* Force scale down if needed */
        .scale-to-fit svg {
            transform-origin: center center;
            transform: scale(0.95);
        }
        
        @media print {
            html, body {
                width: 8.5in;
                height: 11in;
            }
            
            .page-container {
                width: 8in;
                height: 10.5in;
            }
            
            .svg-wrapper {
                width: 7.5in;
                height: 9.5in;
            }
            
            svg {
                max-width: 7.5in !important;
                max-height: 9.5in !important;
            }
            
            * {
                -webkit-print-color-adjust: exact !important;
                color-adjust: exact !important;
            }
        }
    </style>
</head>
<body>
    <div class="page-container">
        <div class="svg-wrapper scale-to-fit">
            $svgContent
        </div>
    </div>
</body>
</html>
"@
    
    $htmlFile = [System.IO.Path]::ChangeExtension($svgFile, "_FIXED.html")
    $htmlContent | Out-File -FilePath $htmlFile -Encoding UTF8
    
    # Convert with enhanced parameters
    $args = @(
        "--headless",
        "--disable-gpu",
        "--disable-dev-shm-usage",
        "--disable-software-rasterizer",
        "--no-sandbox",
        "--disable-background-timer-throttling",
        "--disable-backgrounding-occluded-windows", 
        "--disable-renderer-backgrounding",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=15000",
        "--print-to-pdf-no-header",
        "--print-to-pdf=`"$outputPdf`"",
        "`"$htmlFile`""
    )
    
    try {
        Start-Process -FilePath $edgePath -ArgumentList $args -Wait -NoNewWindow -RedirectStandardError $null
        Start-Sleep -Seconds 2
        
        if (Test-Path $outputPdf) {
            $size = (Get-Item $outputPdf).Length
            if ($size -gt 10KB) {  # Reasonable size check
                Write-Output "  ✓ SUCCESS: $([System.IO.Path]::GetFileName($outputPdf)) ($([Math]::Round($size/1KB))KB)"
                Remove-Item $htmlFile -ErrorAction SilentlyContinue
                return $true
            }
        }
        
        Write-Output "  ✗ FAILED: $([System.IO.Path]::GetFileName($outputPdf))"
        return $false
    }
    catch {
        Write-Output "  ✗ ERROR: $([System.IO.Path]::GetFileName($outputPdf)) - $($_.Exception.Message)"
        return $false
    }
}

# Process all directories
$totalProcessed = 0
$totalSuccess = 0

$directories = @(
    "01_Adaptive_Multi_Modal_AI_Agent_Authentication",
    "02_AI_Agent_Computational_Biometric_Identification",
    "03_Clandestine_AI_Agent_Communication_Through_Biometric_Channels"
)

foreach ($dir in $directories) {
    if (Test-Path $dir) {
        Write-Output ""
        Write-Output "=== PROCESSING: $dir ==="
        
        $figures = Get-ChildItem -Path $dir -Filter "FIGURE_*.svg"
        foreach ($figure in $figures) {
            $totalProcessed++
            $pdfPath = [System.IO.Path]::ChangeExtension($figure.FullName, ".pdf")
            
            if (Fix-SvgScaling -svgFile $figure.FullName -outputPdf $pdfPath) {
                $totalSuccess++
            }
            
            Start-Sleep -Milliseconds 3000  # Longer delay for stability
        }
    }
}

Write-Output ""
Write-Output "=== COMPREHENSIVE SCALING FIX SUMMARY ==="
Write-Output "Total figures processed: $totalProcessed"
Write-Output "Successful conversions: $totalSuccess"
Write-Output "Failed conversions: $($totalProcessed - $totalSuccess)"

if ($totalSuccess -eq $totalProcessed) {
    Write-Output ""
    Write-Output "🎯 ALL FIGURES SUCCESSFULLY FIXED WITH COMPREHENSIVE SCALING!"
    Write-Output "All technical drawings should now display completely within PDF boundaries."
} else {
    Write-Output ""
    Write-Output "⚠️  Some conversions failed. Manual review may be needed."
}