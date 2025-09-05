# Final SVG to PDF scaling fix
Write-Output "Starting comprehensive SVG PDF fix..."

$edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
$totalFixed = 0

$directories = @(
    "01_Adaptive_Multi_Modal_AI_Agent_Authentication",
    "02_AI_Agent_Computational_Biometric_Identification",
    "03_Clandestine_AI_Agent_Communication_Through_Biometric_Channels"
)

foreach ($dir in $directories) {
    if (Test-Path $dir) {
        Write-Output "Processing: $dir"
        
        Get-ChildItem -Path $dir -Filter "FIGURE_*.svg" | ForEach-Object {
            $svgFile = $_.FullName
            $pdfFile = [System.IO.Path]::ChangeExtension($svgFile, ".pdf")
            $htmlFile = [System.IO.Path]::ChangeExtension($svgFile, "_TEMP.html")
            
            Write-Output "  Converting: $($_.Name)"
            
            # Read SVG content
            $svgContent = Get-Content $svgFile -Raw -Encoding UTF8
            
            # Add proper viewBox to ensure all content is visible
            $svgContent = $svgContent -replace '<svg([^>]*?)>', '<svg$1 viewBox="0 0 1200 900" preserveAspectRatio="xMidYMid meet">'
            
            # Create comprehensive HTML
            $html = @"
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        @page { 
            size: letter; 
            margin: 0.5in; 
            -webkit-print-color-adjust: exact;
        }
        
        body { 
            margin: 0; 
            padding: 0; 
            background: white;
            width: 7.5in;
            height: 10in;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .container {
            width: 100%;
            height: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            background: white;
        }
        
        svg { 
            max-width: 7in !important; 
            max-height: 9.5in !important; 
            width: auto !important; 
            height: auto !important; 
            background: white !important;
        }
        
        @media print {
            * { -webkit-print-color-adjust: exact !important; }
        }
    </style>
</head>
<body>
    <div class="container">
        $svgContent
    </div>
</body>
</html>
"@
            
            # Write HTML file
            $html | Out-File -FilePath $htmlFile -Encoding UTF8
            
            # Convert to PDF with optimal settings
            $arguments = @(
                "--headless",
                "--disable-gpu",
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--run-all-compositor-stages-before-draw",
                "--virtual-time-budget=20000",
                "--print-to-pdf-no-header",
                "--print-to-pdf=$pdfFile",
                "$htmlFile"
            )
            
            Start-Process -FilePath $edgePath -ArgumentList $arguments -Wait -WindowStyle Hidden
            
            # Clean up and verify
            Start-Sleep -Seconds 3
            Remove-Item $htmlFile -ErrorAction SilentlyContinue
            
            if (Test-Path $pdfFile) {
                $fileSize = (Get-Item $pdfFile).Length
                if ($fileSize -gt 10000) {
                    Write-Output "    Success: $($_.Name) (Size: $([Math]::Round($fileSize/1024))KB)"
                    $totalFixed++
                } else {
                    Write-Output "    Warning: $($_.Name) file seems too small"
                }
            } else {
                Write-Output "    Failed: $($_.Name)"
            }
        }
    }
}

Write-Output ""
Write-Output "Scaling fix completed."
Write-Output "Total figures processed: $totalFixed"
Write-Output ""
Write-Output "All SVG figures have been reprocessed with:"
Write-Output "- Expanded viewBox for full content visibility"
Write-Output "- Proper scaling to fit within 7x9.5 inch area"
Write-Output "- Enhanced PDF conversion parameters"