# Test Single SVG to PDF Conversion
Write-Host "Testing single SVG conversion with new scaling" -ForegroundColor Green

$edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
$svgFile = "01_Adaptive_Multi_Modal_AI_Agent_Authentication\FIGURE_1_SYSTEM_ARCHITECTURE.svg"
$pdfFile = "01_Adaptive_Multi_Modal_AI_Agent_Authentication\\FIGURE_1_SYSTEM_ARCHITECTURE.pdf"

if (-not (Test-Path $edgePath)) {
    Write-Host "Edge not found" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $svgFile)) {
    Write-Host "SVG file not found: $svgFile" -ForegroundColor Red
    exit 1
}

# Read SVG content
$svgContent = Get-Content $svgFile -Raw

# Create HTML wrapper
$htmlContent = @"
<!DOCTYPE html>
<html>
<head>
    <style>
        @page { 
            size: 8.5in 11in; 
            margin: 0.5in; 
        }
        body { 
            margin: 0; 
            padding: 0; 
            background: white;
        }
        svg { 
            width: 100%; 
            height: auto; 
            max-width: 7.5in;
            display: block;
        }
    </style>
</head>
<body>
$svgContent
</body>
</html>
"@

$tempHtml = "temp_figure1.html"
$htmlContent | Out-File -FilePath $tempHtml -Encoding UTF8

try {
    $arguments = @(
        "--headless",
        "--disable-gpu", 
        "--print-to-pdf=`"$pdfFile`"",
        "--print-to-pdf-no-header",
        "--virtual-time-budget=5000",
        "`"$tempHtml`""
    )
    
    Start-Process -FilePath $edgePath -ArgumentList $arguments -Wait -NoNewWindow
    
    if (Test-Path $pdfFile) {
        Write-Host "SUCCESS: PDF generated at $pdfFile" -ForegroundColor Green
    } else {
        Write-Host "FAILED: PDF not generated" -ForegroundColor Red
    }
}
finally {
    if (Test-Path $tempHtml) {
        Remove-Item $tempHtml -Force -ErrorAction SilentlyContinue
    }
}