# PowerShell script to convert all HTML files to PDF using Microsoft Edge
# This script will attempt to use Edge's headless mode to convert HTML files to PDF

Write-Output "Starting PDF conversion process..."
Write-Output "Looking for Microsoft Edge..."

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
    Write-Output "Microsoft Edge not found. Please convert HTML files to PDF manually using your browser."
    Write-Output "Instructions:"
    Write-Output "1. Open each HTML file in your browser"
    Write-Output "2. Press Ctrl+P to print"
    Write-Output "3. Select 'Microsoft Print to PDF' or 'Save as PDF'"
    Write-Output "4. Save with the same name but .pdf extension"
    exit 1
}

Write-Output "Found Microsoft Edge at: $edgePath"

# Function to convert HTML to PDF
function Convert-HtmlToPdf {
    param(
        [string]$HtmlPath,
        [string]$PdfPath,
        [string]$EdgePath
    )
    
    try {
        Write-Output "Converting: $HtmlPath -> $PdfPath"
        
        # Use Edge to convert HTML to PDF
        $arguments = @(
            "--headless",
            "--disable-gpu", 
            "--run-all-compositor-stages-before-draw",
            "--disable-background-timer-throttling",
            "--disable-renderer-backgrounding",
            "--disable-backgrounding-occluded-windows",
            "--disable-ipc-flooding-protection",
            "--print-to-pdf=`"$PdfPath`"",
            "`"$HtmlPath`""
        )
        
        $process = Start-Process -FilePath $EdgePath -ArgumentList $arguments -Wait -PassThru -NoNewWindow
        
        if ($process.ExitCode -eq 0 -and (Test-Path $PdfPath)) {
            Write-Output "✓ Successfully created: $PdfPath"
            return $true
        } else {
            Write-Output "✗ Failed to create: $PdfPath"
            return $false
        }
    }
    catch {
        Write-Output "✗ Error converting $HtmlPath : $($_.Exception.Message)"
        return $false
    }
}

# Convert all HTML files
$totalFiles = 0
$successCount = 0
$failCount = 0

# Get all HTML files recursively
$htmlFiles = Get-ChildItem -Recurse -Filter "*.html"

foreach ($file in $htmlFiles) {
    $totalFiles++
    $pdfPath = [System.IO.Path]::ChangeExtension($file.FullName, ".pdf")
    
    if (Convert-HtmlToPdf -HtmlPath $file.FullName -PdfPath $pdfPath -EdgePath $edgePath) {
        $successCount++
    } else {
        $failCount++
    }
    
    # Small delay between conversions
    Start-Sleep -Milliseconds 500
}

Write-Output ""
Write-Output "=== CONVERSION SUMMARY ==="
Write-Output "Total files: $totalFiles"
Write-Output "Successful conversions: $successCount"
Write-Output "Failed conversions: $failCount"

if ($failCount -gt 0) {
    Write-Output ""
    Write-Output "Some conversions failed. You can:"
    Write-Output "1. Try running the script again"
    Write-Output "2. Manually convert failed files using your browser"
    Write-Output "3. Open HTML files in browser and Print > Save as PDF"
}

Write-Output ""
Write-Output "PDF conversion process completed!"

# List all created PDF files
Write-Output ""
Write-Output "=== CREATED PDF FILES ==="
Get-ChildItem -Recurse -Filter "*.pdf" | Select-Object Name, Directory | Sort-Object Directory, Name