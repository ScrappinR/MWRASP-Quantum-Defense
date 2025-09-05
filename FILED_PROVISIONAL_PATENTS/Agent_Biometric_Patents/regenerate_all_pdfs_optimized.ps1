# Regenerate All Patent PDFs with Optimized Scaling
Write-Host "REGENERATING ALL PATENT PDFs WITH OPTIMIZED SCALING" -ForegroundColor Green  
Write-Host "=" * 55

$edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

if (-not (Test-Path $edgePath)) {
    Write-Host "Microsoft Edge not found at: $edgePath" -ForegroundColor Red
    exit 1
}

function Convert-SVGToPDFOptimized {
    param(
        [string]$svgPath,
        [string]$pdfPath
    )
    
    $fileName = Split-Path $svgPath -Leaf
    Write-Host "  Converting: $fileName"
    
    try {
        # Read SVG content
        $svgContent = Get-Content $svgPath -Raw
        
        # Create optimized HTML wrapper
        $htmlContent = @"
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        @page { 
            size: 8.5in 11in; 
            margin: 0.5in;
            -webkit-print-color-adjust: exact;
            color-adjust: exact;
        }
        body { 
            margin: 0; 
            padding: 0; 
            background: white;
            font-family: Arial, sans-serif;
        }
        svg { 
            width: 100%; 
            height: auto; 
            max-width: 7.5in;
            max-height: 10in;
            display: block;
            background: white;
        }
        @media print {
            * {
                -webkit-print-color-adjust: exact !important;
                color-adjust: exact !important;
            }
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
        
        # Convert to PDF using Edge
        $arguments = @(
            "--headless",
            "--disable-gpu",
            "--disable-dev-shm-usage", 
            "--no-sandbox",
            "--disable-background-timer-throttling",
            "--print-to-pdf=`"$pdfPath`"",
            "--print-to-pdf-no-header",
            "--virtual-time-budget=10000",
            "`"$tempHtml`""
        )
        
        $process = Start-Process -FilePath $edgePath -ArgumentList $arguments -Wait -NoNewWindow -PassThru
        
        # Check if PDF was created successfully
        if ($process.ExitCode -eq 0 -and (Test-Path $pdfPath)) {
            $size = (Get-Item $pdfPath).Length
            if ($size -gt 5KB) {
                Write-Host "    SUCCESS: $([Math]::Round($size/1KB))KB" -ForegroundColor Green
                return $true
            }
        }
        
        Write-Host "    FAILED: Conversion failed" -ForegroundColor Red
        return $false
    }
    catch {
        Write-Host "    ERROR: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
    finally {
        # Clean up temporary HTML file
        if (Test-Path $tempHtml) {
            Remove-Item $tempHtml -Force -ErrorAction SilentlyContinue
        }
    }
}

# Process all directories
$directories = @(
    "01_Adaptive_Multi_Modal_AI_Agent_Authentication",
    "02_AI_Agent_Computational_Biometric_Identification", 
    "03_Clandestine_AI_Agent_Communication_Through_Biometric_Channels"
)

$totalProcessed = 0
$totalSuccess = 0

foreach ($dir in $directories) {
    if (Test-Path $dir) {
        Write-Host ""
        Write-Host "Processing: $dir" -ForegroundColor Yellow
        
        $svgFiles = Get-ChildItem -Path $dir -Filter "FIGURE_*.svg" | Sort-Object Name
        
        foreach ($svgFile in $svgFiles) {
            $pdfPath = [System.IO.Path]::ChangeExtension($svgFile.FullName, ".pdf")
            $totalProcessed++
            
            if (Convert-SVGToPDFOptimized -svgPath $svgFile.FullName -pdfPath $pdfPath) {
                $totalSuccess++
            }
            
            # Small delay to prevent system overload
            Start-Sleep -Milliseconds 1500
        }
    } else {
        Write-Host "Directory not found: $dir" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "=" * 55
Write-Host "PDF REGENERATION COMPLETE" -ForegroundColor Green
Write-Host "Total figures processed: $totalProcessed"
Write-Host "Successful conversions: $totalSuccess" 
Write-Host "Failed conversions: $($totalProcessed - $totalSuccess)"

if ($totalSuccess -eq $totalProcessed) {
    Write-Host ""
    Write-Host "🎯 ALL PATENT DRAWINGS SUCCESSFULLY REGENERATED!" -ForegroundColor Green
    Write-Host "All PDFs should now display complete content with optimal scaling."
} else {
    Write-Host ""
    Write-Host "⚠️  Some conversions failed. Review may be needed." -ForegroundColor Yellow
}