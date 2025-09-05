# Convert Fixed SVG Files to PDF
# ==============================
# This script converts the fixed SVG files (with proper dimensions) directly to PDF

Write-Host "CONVERTING FIXED SVG FILES TO PDF" -ForegroundColor Green
Write-Host "=" * 40

# Find Edge executable
$edgePath = $null
$possiblePaths = @(
    "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe",
    "${env:ProgramFiles}\Microsoft\Edge\Application\msedge.exe",
    "${env:LOCALAPPDATA}\Microsoft\Edge\Application\msedge.exe"
)

foreach ($path in $possiblePaths) {
    if (Test-Path $path) {
        $edgePath = $path
        break
    }
}

if (-not $edgePath) {
    Write-Host "Microsoft Edge not found. Cannot convert SVG to PDF." -ForegroundColor Red
    exit 1
}

Write-Host "Found Edge at: $edgePath" -ForegroundColor Green

function Convert-SVGToPDFDirect {
    param(
        [string]$svgPath,
        [string]$pdfPath
    )
    
    Write-Host "Converting: $(Split-Path $svgPath -Leaf) -> $(Split-Path $pdfPath -Leaf)"
    
    # Create HTML wrapper for the SVG with proper dimensions
    $svgContent = Get-Content $svgPath -Raw
    
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
    
    # Create temporary HTML file
    $tempHtml = [System.IO.Path]::ChangeExtension($svgPath, ".temp.html")
    $htmlContent | Out-File -FilePath $tempHtml -Encoding UTF8
    
    try {
        # Convert HTML to PDF using Edge
        $arguments = @(
            "--headless",
            "--disable-gpu",
            "--print-to-pdf=`"$pdfPath`"",
            "--print-to-pdf-no-header",
            "--virtual-time-budget=5000",
            "`"$tempHtml`""
        )
        
        $process = Start-Process -FilePath $edgePath -ArgumentList $arguments -Wait -NoNewWindow -PassThru
        
        if ($process.ExitCode -eq 0 -and (Test-Path $pdfPath)) {
            Write-Host "  SUCCESS: PDF created" -ForegroundColor Green
            return $true
        } else {
            Write-Host "  FAILED: Edge conversion failed" -ForegroundColor Red
            return $false
        }
    }
    finally {
        # Clean up temporary HTML file
        if (Test-Path $tempHtml) {
            Remove-Item $tempHtml -Force -ErrorAction SilentlyContinue
        }
    }
}

# Process all patent folders
$patentFolders = Get-ChildItem -Directory | Where-Object { $_.Name -match "^\d+_" }
$totalConverted = 0

foreach ($folder in $patentFolders) {
    Write-Host ""
    Write-Host "Processing folder: $($folder.Name)" -ForegroundColor Yellow
    
    # Find all SVG figure files
    $svgFiles = Get-ChildItem -Path $folder.FullName -Filter "FIGURE_*.svg" | Sort-Object Name
    
    if ($svgFiles.Count -eq 0) {
        Write-Host "  No SVG files found"
        continue
    }
    
    foreach ($svgFile in $svgFiles) {
        $pdfPath = [System.IO.Path]::ChangeExtension($svgFile.FullName, ".pdf")
        
        $success = Convert-SVGToPDFDirect -svgPath $svgFile.FullName -pdfPath $pdfPath
        
        if ($success) {
            $totalConverted++
        }
        
        # Small delay to prevent overwhelming the system
        Start-Sleep -Milliseconds 500
    }
}

Write-Host ""
Write-Host "=" * 40
Write-Host "CONVERSION COMPLETE" -ForegroundColor Green
Write-Host "Total files converted: $totalConverted"
Write-Host ""
Write-Host "All patent drawings have been regenerated from the fixed SVG files."
Write-Host "The new PDFs should display complete content without cut-offs."

Write-Host ""
Write-Host "Press any key to continue..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")