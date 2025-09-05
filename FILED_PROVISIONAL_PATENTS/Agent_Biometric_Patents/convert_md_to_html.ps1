param(
    [Parameter(Mandatory=$true)]
    [string]$InputFile,
    [Parameter(Mandatory=$true)]
    [string]$OutputFile
)

# Read the markdown content
$content = Get-Content $InputFile -Raw -Encoding UTF8

# Convert markdown to HTML
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
$content = $content -replace '\n', '<br/>'

# Create full HTML document
$html = @"
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Patent Document</title>
    <style>
        body { 
            font-family: 'Times New Roman', serif; 
            font-size: 12pt; 
            line-height: 1.5; 
            margin: 1in; 
            color: black;
        }
        h1, h2, h3, h4, h5, h6 { 
            font-weight: bold; 
            margin-top: 1em; 
            margin-bottom: 0.5em; 
            color: black;
        }
        h1 { font-size: 18pt; }
        h2 { font-size: 16pt; }
        h3 { font-size: 14pt; }
        p { margin-bottom: 1em; }
        code { 
            font-family: 'Courier New', monospace; 
            background: #f5f5f5; 
            padding: 2px 4px; 
            border: 1px solid #ddd;
        }
        pre {
            font-family: 'Courier New', monospace; 
            background: #f5f5f5; 
            padding: 10px; 
            border: 1px solid #ddd;
            white-space: pre-wrap;
        }
        table { 
            border-collapse: collapse; 
            width: 100%; 
            margin: 1em 0; 
        }
        td, th { 
            border: 1px solid #ddd; 
            padding: 8px; 
            text-align: left; 
        }
        th { 
            background-color: #f2f2f2; 
            font-weight: bold;
        }
        @page { 
            size: letter; 
            margin: 1in; 
        }
        @media print {
            body { margin: 0; padding: 1in; }
        }
        strong { font-weight: bold; }
        em { font-style: italic; }
    </style>
</head>
<body>
<p>$content</p>
</body>
</html>
"@

# Write HTML to file
$html | Out-File -FilePath $OutputFile -Encoding UTF8

Write-Output "Converted $InputFile to $OutputFile"