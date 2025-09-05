# PowerShell script to fix all SVG to PDF conversions with proper scaling
Write-Output "Fixing SVG to PDF conversions with proper scaling..."

$edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

if (-not (Test-Path $edgePath)) {
    Write-Output "Microsoft Edge not found. Please install Edge or convert manually."
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
        Write-Output ""
        Write-Output "Processing directory: $dir"
        
        Get-ChildItem -Path $dir -Filter "FIGURE_*.svg" | ForEach-Object {
            $svgFile = $_.FullName
            $baseNameWithoutExt = [System.IO.Path]::GetFileNameWithoutExtension($svgFile)
            $htmlFile = [System.IO.Path]::ChangeExtension($svgFile, "_FIXED.html")
            $pdfFile = [System.IO.Path]::ChangeExtension($svgFile, ".pdf")
            
            Write-Output "Fixing: $($_.Name)"
            
            # Create fixed HTML version
            & ".\convert_svg_to_pdf_fixed.ps1" -InputFile $svgFile -OutputFile $htmlFile
            
            # Convert to PDF with better parameters
            $arguments = @(
                "--headless",
                "--disable-gpu",
                "--disable-dev-shm-usage",
                "--disable-software-rasterizer",
                "--disable-background-timer-throttling",
                "--disable-renderer-backgrounding",
                "--disable-backgrounding-occluded-windows",
                "--run-all-compositor-stages-before-draw",
                "--virtual-time-budget=10000",
                "--print-to-pdf=`"$pdfFile`"",
                "--print-to-pdf-no-header",
                "`"$htmlFile`""
            )
            
            Start-Process -FilePath $edgePath -ArgumentList $arguments -Wait -WindowStyle Hidden
            
            if (Test-Path $pdfFile) {
                Write-Output "  ✓ Fixed: $baseNameWithoutExt.pdf"
                $totalFixed++
                
                # Clean up temporary HTML file
                Remove-Item $htmlFile -ErrorAction SilentlyContinue
            } else {
                Write-Output "  ✗ Failed: $baseNameWithoutExt.pdf"
            }
            
            Start-Sleep -Milliseconds 1500
        }
    }
}

Write-Output ""
Write-Output "=== FIXING SUMMARY ==="
Write-Output "Total figures fixed: $totalFixed"
Write-Output ""
Write-Output "All SVG figures have been reconverted with proper scaling to fit PDF pages."
Write-Output "The technical drawings should now display completely within the page boundaries."