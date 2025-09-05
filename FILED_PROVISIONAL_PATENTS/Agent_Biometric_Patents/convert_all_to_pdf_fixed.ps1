# PowerShell script to convert all HTML files to PDF using Microsoft Edge
Write-Output "Starting PDF conversion process..."

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
    Write-Output "Microsoft Edge not found. Manual conversion required."
    Write-Output "Please convert HTML files to PDF using your browser:"
    Write-Output "1. Open each HTML file in browser"
    Write-Output "2. Press Ctrl+P to print"
    Write-Output "3. Select 'Save as PDF'"
    Write-Output "4. Save with same name but .pdf extension"
    exit 1
}

Write-Output "Found Edge at: $edgePath"

# Convert HTML files to PDF
$totalFiles = 0
$successCount = 0

Get-ChildItem -Recurse -Filter "*.html" | ForEach-Object {
    $totalFiles++
    $htmlFile = $_.FullName
    $pdfFile = [System.IO.Path]::ChangeExtension($htmlFile, ".pdf")
    
    Write-Output "Converting: $($_.Name)"
    
    try {
        $arguments = "--headless --disable-gpu --print-to-pdf=`"$pdfFile`" `"$htmlFile`""
        $process = Start-Process -FilePath $edgePath -ArgumentList $arguments -Wait -PassThru -WindowStyle Hidden
        
        if (Test-Path $pdfFile) {
            Write-Output "Success: $($_.Name) -> PDF"
            $successCount++
        } else {
            Write-Output "Failed: $($_.Name)"
        }
    }
    catch {
        Write-Output "Error: $($_.Name) - $($_.Exception.Message)"
    }
    
    Start-Sleep -Milliseconds 1000
}

Write-Output ""
Write-Output "Conversion Summary:"
Write-Output "Total files: $totalFiles"
Write-Output "Successful: $successCount"
Write-Output "Failed: $($totalFiles - $successCount)"

if ($successCount -gt 0) {
    Write-Output ""
    Write-Output "Created PDF files:"
    Get-ChildItem -Recurse -Filter "*.pdf" | ForEach-Object {
        Write-Output "  $($_.FullName)"
    }
}