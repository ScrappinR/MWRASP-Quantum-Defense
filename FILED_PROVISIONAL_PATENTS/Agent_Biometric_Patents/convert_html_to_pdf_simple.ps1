# Simple HTML to PDF conversion script
Write-Output "Converting HTML files to PDF format..."

$edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

if (-not (Test-Path $edgePath)) {
    Write-Output "Edge not found at default location. Checking alternatives..."
    
    $altPaths = @(
        "${env:ProgramFiles}\Microsoft\Edge\Application\msedge.exe",
        "${env:LOCALAPPDATA}\Microsoft\Edge\Application\msedge.exe"
    )
    
    foreach ($path in $altPaths) {
        if (Test-Path $path) {
            $edgePath = $path
            Write-Output "Found Edge at: $path"
            break
        }
    }
    
    if (-not (Test-Path $edgePath)) {
        Write-Output "ERROR: Microsoft Edge not found."
        exit 1
    }
}

$totalConverted = 0
$totalFailed = 0

# Function to convert HTML to PDF
function ConvertToPdf($htmlFile, $pdfFile) {
    Write-Output "Converting: $([System.IO.Path]::GetFileName($htmlFile))"
    
    $arguments = @(
        "--headless",
        "--disable-gpu",
        "--no-sandbox", 
        "--disable-dev-shm-usage",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=20000",
        "--print-to-pdf=$pdfFile",
        "$htmlFile"
    )
    
    try {
        Start-Process -FilePath $edgePath -ArgumentList $arguments -Wait -WindowStyle Hidden
        Start-Sleep -Seconds 3
        
        if (Test-Path $pdfFile) {
            $size = (Get-Item $pdfFile).Length
            $sizeKB = [Math]::Round($size / 1024)
            Write-Output "  Success: $([System.IO.Path]::GetFileName($pdfFile)) - Size: ${sizeKB}KB"
            return $true
        } else {
            Write-Output "  Failed: PDF not created"
            return $false
        }
    }
    catch {
        Write-Output "  Error: $($_.Exception.Message)"
        return $false
    }
}

# Convert files in each directory
$directories = @(
    "01_Adaptive_Multi_Modal_AI_Agent_Authentication",
    "02_AI_Agent_Computational_Biometric_Identification", 
    "03_Clandestine_AI_Agent_Communication_Through_Biometric_Channels"
)

foreach ($dir in $directories) {
    if (Test-Path $dir) {
        Write-Output ""
        Write-Output "Processing directory: $dir"
        
        # Get HTML files (exclude _ENHANCED versions)
        Get-ChildItem -Path $dir -Filter "*.html" | Where-Object { $_.Name -notmatch "_ENHANCED" } | ForEach-Object {
            $htmlPath = $_.FullName
            $pdfPath = [System.IO.Path]::ChangeExtension($htmlPath, ".pdf")
            
            if (ConvertToPdf $htmlPath $pdfPath) {
                $global:totalConverted++
            } else {
                $global:totalFailed++
            }
        }
    }
}

# Convert summary file
if (Test-Path "PATENT_FILING_SUMMARY.html") {
    Write-Output ""
    Write-Output "Converting summary document..."
    
    if (ConvertToPdf "PATENT_FILING_SUMMARY.html" "PATENT_FILING_SUMMARY.pdf") {
        $totalConverted++
    } else {
        $totalFailed++
    }
}

Write-Output ""
Write-Output "=== CONVERSION COMPLETE ==="
Write-Output "Successful conversions: $totalConverted"
Write-Output "Failed conversions: $totalFailed"
Write-Output "Total files processed: $($totalConverted + $totalFailed)"

if ($totalFailed -eq 0) {
    Write-Output ""
    Write-Output "ALL HTML FILES SUCCESSFULLY CONVERTED TO PDF!"
    Write-Output "Patent filing package is ready for USPTO submission."
} else {
    Write-Output ""
    Write-Output "Some conversions failed. Consider manual conversion for failed files."
}

# List created PDFs
Write-Output ""
Write-Output "Created PDF files:"
Get-ChildItem -Recurse -Filter "*.pdf" | Sort-Object DirectoryName, Name | ForEach-Object {
    $relativePath = $_.FullName.Replace((Get-Location).Path + "\", "")
    $size = [Math]::Round($_.Length / 1024)
    Write-Output "  $relativePath (${size}KB)"
}