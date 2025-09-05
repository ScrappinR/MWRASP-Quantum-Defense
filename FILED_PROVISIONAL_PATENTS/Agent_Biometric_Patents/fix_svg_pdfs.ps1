# PowerShell script to fix SVG to PDF conversions with proper scaling
Write-Output "Fixing SVG to PDF conversions with proper scaling..."

$edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

if (-not (Test-Path $edgePath)) {
    Write-Output "Microsoft Edge not found."
    exit 1
}

$totalFixed = 0
$directories = @(
    "01_Adaptive_Multi_Modal_AI_Agent_Authentication",
    "02_AI_Agent_Computational_Biometric_Identification", 
    "03_Clandestine_AI_Agent_Communication_Through_Biometric_Channels"
)

foreach ($dir in $directories) {
    if (Test-Path $dir) {
        Write-Output "Processing directory: $dir"
        
        Get-ChildItem -Path $dir -Filter "FIGURE_*.svg" | ForEach-Object {
            $svgFile = $_.FullName
            $htmlFile = [System.IO.Path]::ChangeExtension($svgFile, "_FIXED.html")
            $pdfFile = [System.IO.Path]::ChangeExtension($svgFile, ".pdf")
            
            Write-Output "Fixing: $($_.Name)"
            
            # Create fixed HTML with scaling
            $svgContent = Get-Content $svgFile -Raw -Encoding UTF8
            
            $html = @"
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        @page { size: letter; margin: 0.5in; }
        body { margin: 0; padding: 0; background: white; }
        .container { 
            width: 100%; 
            height: 100vh; 
            display: flex; 
            justify-content: center; 
            align-items: center; 
        }
        svg { 
            max-width: 7.5in !important; 
            max-height: 10in !important; 
            width: auto !important; 
            height: auto !important; 
            background: white; 
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
            
            $html | Out-File -FilePath $htmlFile -Encoding UTF8
            
            # Convert to PDF
            Start-Process -FilePath $edgePath -ArgumentList "--headless", "--disable-gpu", "--print-to-pdf=`"$pdfFile`"", "`"$htmlFile`"" -Wait -WindowStyle Hidden
            
            if (Test-Path $pdfFile) {
                Write-Output "Success: $($_.Name)"
                $totalFixed++
                Remove-Item $htmlFile -ErrorAction SilentlyContinue
            } else {
                Write-Output "Failed: $($_.Name)"
            }
            
            Start-Sleep -Milliseconds 2000
        }
    }
}

Write-Output "Total figures fixed: $totalFixed"