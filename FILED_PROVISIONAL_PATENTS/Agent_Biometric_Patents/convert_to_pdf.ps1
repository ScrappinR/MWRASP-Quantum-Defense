# PowerShell script to convert markdown and SVG files to PDF
param(
    [string]$InputPath,
    [string]$OutputPath,
    [string]$FileType
)

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

function Convert-MarkdownToPDF {
    param($MarkdownPath, $PDFPath)
    
    # Read markdown content
    $content = Get-Content $MarkdownPath -Raw
    
    # Basic HTML conversion for markdown
    $html = $content -replace '###### (.*)', '<h6>$1</h6>' `
                   -replace '##### (.*)', '<h5>$1</h5>' `
                   -replace '#### (.*)', '<h4>$1</h4>' `
                   -replace '### (.*)', '<h3>$1</h3>' `
                   -replace '## (.*)', '<h2>$1</h2>' `
                   -replace '# (.*)', '<h1>$1</h1>' `
                   -replace '\*\*(.*?)\*\*', '<strong>$1</strong>' `
                   -replace '\*(.*?)\*', '<em>$1</em>' `
                   -replace '`([^`]+)`', '<code>$1</code>' `
                   -replace '^- (.*)$', '<li>$1</li>' `
                   -replace '\n\n', '</p><p>' `
                   -replace '^\|', '<table><tr><td>' `
                   -replace '\|$', '</td></tr></table>' `
                   -replace '\|', '</td><td>'
    
    # Wrap in basic HTML structure
    $htmlContent = @"
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: 'Times New Roman', serif; font-size: 12pt; line-height: 1.5; margin: 1in; }
        h1, h2, h3, h4, h5, h6 { font-weight: bold; }
        code { font-family: 'Courier New', monospace; background: #f5f5f5; padding: 2px; }
        table { border-collapse: collapse; width: 100%; }
        td { border: 1px solid #ddd; padding: 8px; }
    </style>
</head>
<body>
<p>$html</p>
</body>
</html>
"@
    
    # Save as HTML temporarily
    $tempHtml = $PDFPath -replace '\.pdf$', '.html'
    $htmlContent | Out-File -FilePath $tempHtml -Encoding UTF8
    
    Write-Output "Converted $MarkdownPath to HTML: $tempHtml"
}

function Convert-SVGToPDF {
    param($SVGPath, $PDFPath)
    
    # For SVG, we'll create an HTML wrapper and convert
    $svgContent = Get-Content $SVGPath -Raw
    
    $htmlContent = @"
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { margin: 0; padding: 20px; }
        svg { max-width: 100%; height: auto; }
    </style>
</head>
<body>
$svgContent
</body>
</html>
"@
    
    # Save as HTML
    $tempHtml = $PDFPath -replace '\.pdf$', '.html'
    $htmlContent | Out-File -FilePath $tempHtml -Encoding UTF8
    
    Write-Output "Converted $SVGPath to HTML: $tempHtml"
}

# Main conversion logic
if ($FileType -eq "md") {
    Convert-MarkdownToPDF -MarkdownPath $InputPath -PDFPath $OutputPath
} elseif ($FileType -eq "svg") {
    Convert-SVGToPDF -SVGPath $InputPath -PDFPath $OutputPath
}

Write-Output "Conversion completed. Note: HTML files created. Use browser's Print to PDF for final PDF conversion."