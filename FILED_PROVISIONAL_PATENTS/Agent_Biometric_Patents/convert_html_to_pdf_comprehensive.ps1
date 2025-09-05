# Comprehensive HTML to PDF conversion script
Write-Output "=== COMPREHENSIVE HTML TO PDF CONVERSION ==="
Write-Output "Converting all HTML files to PDF format..."

$edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

if (-not (Test-Path $edgePath)) {
    Write-Output "Microsoft Edge not found. Trying alternative paths..."
    $altPaths = @(
        "${env:ProgramFiles}\Microsoft\Edge\Application\msedge.exe",
        "${env:LOCALAPPDATA}\Microsoft\Edge\Application\msedge.exe"
    )
    
    foreach ($path in $altPaths) {
        if (Test-Path $path) {
            $edgePath = $path
            break
        }
    }
    
    if (-not (Test-Path $edgePath)) {
        Write-Output "ERROR: Microsoft Edge not found. Cannot proceed."
        exit 1
    }
}

Write-Output "Using Edge at: $edgePath"

function Convert-HtmlToPdf {
    param(
        [string]$HtmlPath,
        [string]$PdfPath,
        [string]$Type = "document"
    )
    
    $fileName = [System.IO.Path]::GetFileName($HtmlPath)
    Write-Output "Converting: $fileName"
    
    # Different settings based on content type
    if ($Type -eq "figure") {
        # Optimized for technical drawings
        $args = @(
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-web-security",
            "--run-all-compositor-stages-before-draw",
            "--virtual-time-budget=15000",
            "--print-to-pdf-no-header",
            "--print-to-pdf=`"$PdfPath`"",
            "`"$HtmlPath`""
        )
    } else {
        # Optimized for text documents
        $args = @(
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            "--run-all-compositor-stages-before-draw",
            "--virtual-time-budget=10000",
            "--print-to-pdf=`"$PdfPath`"",
            "`"$HtmlPath`""
        )
    }
    
    try {
        $process = Start-Process -FilePath $edgePath -ArgumentList $args -Wait -PassThru -WindowStyle Hidden
        
        Start-Sleep -Seconds 2
        
        if (Test-Path $PdfPath) {
            $fileSize = (Get-Item $PdfPath).Length
            if ($fileSize -gt 5000) {  # Minimum viable size
                $sizeKB = [Math]::Round($fileSize / 1024)
                Write-Output "  ✓ SUCCESS: $fileName -> $([System.IO.Path]::GetFileName($PdfPath)) (${sizeKB}KB)"
                return $true
            } else {
                Write-Output "  ⚠ WARNING: $fileName -> PDF too small (${fileSize} bytes)"
                return $false
            }
        } else {
            Write-Output "  ✗ FAILED: $fileName -> PDF not created"
            return $false
        }
    }
    catch {
        Write-Output "  ✗ ERROR: $fileName -> $($_.Exception.Message)"
        return $false
    }
}

# Track conversion statistics
$totalFiles = 0
$successCount = 0
$failCount = 0

# Convert all HTML files in each directory
$directories = @(
    "01_Adaptive_Multi_Modal_AI_Agent_Authentication",
    "02_AI_Agent_Computational_Biometric_Identification",
    "03_Clandestine_AI_Agent_Communication_Through_Biometric_Channels"
)

foreach ($dir in $directories) {
    if (Test-Path $dir) {
        Write-Output ""
        Write-Output "=== PROCESSING DIRECTORY: $dir ==="
        
        # Get all HTML files (excluding enhanced versions for now)
        $htmlFiles = Get-ChildItem -Path $dir -Filter "*.html" | Where-Object { $_.Name -notmatch "_ENHANCED" }
        
        foreach ($htmlFile in $htmlFiles) {
            $totalFiles++
            $pdfPath = [System.IO.Path]::ChangeExtension($htmlFile.FullName, ".pdf")
            
            # Determine content type for optimization
            $contentType = if ($htmlFile.Name -match "^FIGURE_") { "figure" } else { "document" }
            
            if (Convert-HtmlToPdf -HtmlPath $htmlFile.FullName -PdfPath $pdfPath -Type $contentType) {
                $successCount++
            } else {
                $failCount++
            }
            
            # Small delay between conversions for stability
            Start-Sleep -Milliseconds 1500
        }
    }
}

# Convert main summary file
if (Test-Path "PATENT_FILING_SUMMARY.html") {
    Write-Output ""
    Write-Output "=== CONVERTING SUMMARY DOCUMENT ==="
    $totalFiles++
    $summaryPdf = "PATENT_FILING_SUMMARY.pdf"
    
    if (Convert-HtmlToPdf -HtmlPath "PATENT_FILING_SUMMARY.html" -PdfPath $summaryPdf -Type "document") {
        $successCount++
    } else {
        $failCount++
    }
}

# Final summary
Write-Output ""
Write-Output "=== CONVERSION SUMMARY ==="
Write-Output "Total HTML files processed: $totalFiles"
Write-Output "Successful conversions: $successCount"
Write-Output "Failed conversions: $failCount"
Write-Output "Success rate: $([Math]::Round(($successCount / $totalFiles) * 100, 1))%"

if ($successCount -eq $totalFiles) {
    Write-Output ""
    Write-Output "🎉 ALL HTML FILES SUCCESSFULLY CONVERTED TO PDF!"
    Write-Output ""
    Write-Output "Patent filing package is now complete with:"
    Write-Output "✅ All patent specifications in PDF format"
    Write-Output "✅ All micro entity forms in PDF format" 
    Write-Output "✅ All technical drawings in PDF format"
    Write-Output "✅ Filing summary document in PDF format"
    Write-Output ""
    Write-Output "🏆 READY FOR USPTO SUBMISSION!"
} elseif ($failCount -gt 0) {
    Write-Output ""
    Write-Output "⚠️ Some conversions failed. You may need to:"
    Write-Output "1. Manually convert failed files using browser Print-to-PDF"
    Write-Output "2. Check the enhanced HTML files for better scaling"
    Write-Output "3. Verify file permissions and available disk space"
} else {
    Write-Output ""
    Write-Output "✅ Conversion completed successfully!"
}

# List all created PDF files for verification
Write-Output ""
Write-Output "=== CREATED PDF FILES ==="
Get-ChildItem -Recurse -Filter "*.pdf" | ForEach-Object {
    $size = [Math]::Round($_.Length / 1024)
    Write-Output "$($_.FullName) (${size}KB)"
}