# Ultra-conservative SVG to PDF conversion with maximum compatibility
Write-Output "Creating ultra-conservative PDF versions..."

$edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
$totalProcessed = 0

function Create-UltraConservativePDF {
    param($svgFile, $outputPdf)
    
    $svgContent = Get-Content $svgFile -Raw -Encoding UTF8
    $baseName = [System.IO.Path]::GetFileNameWithoutExtension($svgFile)
    
    # Ultra-conservative HTML with very small scaling to ensure everything fits
    $html = @"
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>$baseName</title>
    <style>
        @page {
            size: letter portrait;
            margin: 1in;
        }
        
        body {
            margin: 0;
            padding: 0;
            background: white;
            font-family: Arial, sans-serif;
        }
        
        .page {
            width: 6.5in;
            height: 9in;
            background: white;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            page-break-after: always;
        }
        
        .title {
            font-size: 12pt;
            font-weight: bold;
            text-align: center;
            margin-bottom: 20px;
            color: black;
        }
        
        .svg-container {
            width: 6in;
            height: 8in;
            background: white;
            border: 1px solid #ccc;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
        }
        
        svg {
            max-width: 5.8in !important;
            max-height: 7.8in !important;
            width: auto !important;
            height: auto !important;
            background: white !important;
        }
        
        /* Force very conservative scaling */
        .ultra-safe svg {
            transform: scale(0.85);
            transform-origin: center center;
        }
    </style>
</head>
<body>
    <div class="page">
        <div class="title">$($baseName.Replace('_', ' ').ToUpper())</div>
        <div class="svg-container ultra-safe">
            $svgContent
        </div>
    </div>
</body>
</html>
"@
    
    $htmlFile = [System.IO.Path]::ChangeExtension($svgFile, "_ULTRA.html")
    $html | Out-File -FilePath $htmlFile -Encoding UTF8
    
    # Use maximum compatibility settings
    $args = @(
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-web-security",
        "--disable-features=VizDisplayCompositor",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=30000",
        "--print-to-pdf-no-header",
        "--print-to-pdf=$outputPdf",
        "$htmlFile"
    )
    
    Start-Process -FilePath $edgePath -ArgumentList $args -Wait -WindowStyle Hidden -RedirectStandardOutput $null -RedirectStandardError $null
    
    Start-Sleep -Seconds 5  # Longer wait
    Remove-Item $htmlFile -ErrorAction SilentlyContinue
    
    if (Test-Path $outputPdf) {
        $size = (Get-Item $outputPdf).Length
        Write-Output "  Created: $baseName.pdf ($([Math]::Round($size/1024))KB)"
        return $true
    } else {
        Write-Output "  FAILED: $baseName.pdf"
        return $false
    }
}

# Process each directory
$dirs = @(
    "01_Adaptive_Multi_Modal_AI_Agent_Authentication",
    "02_AI_Agent_Computational_Biometric_Identification", 
    "03_Clandestine_AI_Agent_Communication_Through_Biometric_Channels"
)

foreach ($dir in $dirs) {
    if (Test-Path $dir) {
        Write-Output ""
        Write-Output "=== ULTRA-CONSERVATIVE CONVERSION: $dir ==="
        
        Get-ChildItem -Path $dir -Filter "FIGURE_*.svg" | ForEach-Object {
            $pdfPath = [System.IO.Path]::ChangeExtension($_.FullName, ".pdf")
            if (Create-UltraConservativePDF -svgFile $_.FullName -outputPdf $pdfPath) {
                $totalProcessed++
            }
        }
    }
}

Write-Output ""
Write-Output "=== ULTRA-CONSERVATIVE CONVERSION COMPLETE ==="
Write-Output "Processed: $totalProcessed figure PDFs"
Write-Output ""
Write-Output "This version uses:"
Write-Output "- 85% scaling factor (very conservative)"
Write-Output "- 6x8 inch drawable area (with 1-inch margins)"
Write-Output "- Maximum compatibility PDF rendering"
Write-Output "- Extended processing time for complex figures"
Write-Output ""
Write-Output "If images are still cut off, the SVG content may extend"
Write-Output "beyond the original 800x600 canvas boundaries."