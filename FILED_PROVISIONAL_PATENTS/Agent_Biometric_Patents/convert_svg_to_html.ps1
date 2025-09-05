param(
    [Parameter(Mandatory=$true)]
    [string]$InputFile,
    [Parameter(Mandatory=$true)]
    [string]$OutputFile
)

# Read the SVG content
$svgContent = Get-Content $InputFile -Raw -Encoding UTF8

# Create HTML wrapper for SVG
$html = @"
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Patent Drawing</title>
    <style>
        body { 
            margin: 0; 
            padding: 20px; 
            background: white;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        svg { 
            max-width: 100%; 
            height: auto; 
            display: block; 
            margin: 0 auto;
            background: white;
        }
        @page { 
            size: letter; 
            margin: 0.5in; 
        }
        @media print { 
            body { 
                margin: 0; 
                padding: 0.5in;
                min-height: auto; 
            } 
            svg {
                max-height: 10in;
            }
        }
    </style>
</head>
<body>
$svgContent
</body>
</html>
"@

# Write HTML to file
$html | Out-File -FilePath $OutputFile -Encoding UTF8

Write-Output "Converted $InputFile to $OutputFile"