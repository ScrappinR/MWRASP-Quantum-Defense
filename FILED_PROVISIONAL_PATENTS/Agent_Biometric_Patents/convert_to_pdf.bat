@echo off
setlocal enabledelayedexpansion

echo Converting documents to PDF format...
echo.

REM Function to convert markdown to HTML then PDF
:convert_markdown
set "input_file=%~1"
set "output_file=%~2"

echo Converting: %input_file%

REM Create HTML wrapper for markdown content
powershell -Command "& {
    $content = Get-Content '%input_file%' -Raw -Encoding UTF8
    $content = $content -replace '###### (.*)', '<h6>$1</h6>'
    $content = $content -replace '##### (.*)', '<h5>$1</h5>'
    $content = $content -replace '#### (.*)', '<h4>$1</h4>'
    $content = $content -replace '### (.*)', '<h3>$1</h3>'
    $content = $content -replace '## (.*)', '<h2>$1</h2>'
    $content = $content -replace '# (.*)', '<h1>$1</h1>'
    $content = $content -replace '\*\*(.*?)\*\*', '<strong>$1</strong>'
    $content = $content -replace '\*(.*?)\*', '<em>$1</em>'
    $content = $content -replace '`([^`]+)`', '<code>$1</code>'
    $content = $content -replace '\n\n', '</p><p>'
    
    $html = '<!DOCTYPE html>
<html>
<head>
    <meta charset=\"UTF-8\">
    <style>
        body { font-family: \"Times New Roman\", serif; font-size: 12pt; line-height: 1.5; margin: 1in; }
        h1, h2, h3, h4, h5, h6 { font-weight: bold; margin-top: 1em; margin-bottom: 0.5em; }
        p { margin-bottom: 1em; }
        code { font-family: \"Courier New\", monospace; background: #f5f5f5; padding: 2px; }
        pre { font-family: \"Courier New\", monospace; background: #f5f5f5; padding: 10px; }
        table { border-collapse: collapse; width: 100%; margin: 1em 0; }
        td, th { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        @page { size: letter; margin: 1in; }
    </style>
</head>
<body>
<p>' + $content + '</p>
</body>
</html>'
    
    $html | Out-File -FilePath '%output_file%.html' -Encoding UTF8
}"

goto :eof

REM Function to convert SVG to HTML
:convert_svg
set "input_file=%~1"
set "output_file=%~2"

echo Converting: %input_file%

powershell -Command "& {
    $svgContent = Get-Content '%input_file%' -Raw -Encoding UTF8
    
    $html = '<!DOCTYPE html>
<html>
<head>
    <meta charset=\"UTF-8\">
    <style>
        body { margin: 0; padding: 20px; }
        svg { max-width: 100%%; height: auto; display: block; margin: 0 auto; }
        @page { size: letter; margin: 0.5in; }
        @media print { body { margin: 0; padding: 0; } }
    </style>
</head>
<body>
' + $svgContent + '
</body>
</html>'
    
    $html | Out-File -FilePath '%output_file%.html' -Encoding UTF8
}"

goto :eof

echo Batch conversion functions ready.
echo Use: call convert_to_pdf.bat convert_markdown "input.md" "output"
echo Use: call convert_to_pdf.bat convert_svg "input.svg" "output"