param(
    [Parameter(Mandatory=$true)]
    [string]$InputFile,
    [Parameter(Mandatory=$true)]
    [string]$OutputFile
)

# Read the SVG content
$svgContent = Get-Content $InputFile -Raw -Encoding UTF8

# Extract SVG dimensions if available
$widthMatch = [regex]::Match($svgContent, 'width="([^"]+)"')
$heightMatch = [regex]::Match($svgContent, 'height="([^"]+)"')

$svgWidth = if ($widthMatch.Success) { $widthMatch.Groups[1].Value } else { "800" }
$svgHeight = if ($heightMatch.Success) { $heightMatch.Groups[1].Value } else { "600" }

# Remove units and convert to numbers for scaling calculation
$svgWidthNum = [regex]::Replace($svgWidth, '[^\d]', '')
$svgHeightNum = [regex]::Replace($svgHeight, '[^\d]', '')

if ([string]::IsNullOrEmpty($svgWidthNum)) { $svgWidthNum = "800" }
if ([string]::IsNullOrEmpty($svgHeightNum)) { $svgHeightNum = "600" }

# Calculate scale to fit within 7.5" x 10" (letter size minus margins)
$maxWidthInches = 7.5
$maxHeightInches = 10
$dpi = 96

$maxWidthPx = $maxWidthInches * $dpi  # 720px
$maxHeightPx = $maxHeightInches * $dpi # 960px

$scaleX = $maxWidthPx / [int]$svgWidthNum
$scaleY = $maxHeightPx / [int]$svgHeightNum
$scale = [Math]::Min($scaleX, $scaleY)

# Don't scale up, only scale down if needed
if ($scale -gt 1) { $scale = 1 }

$scaledWidth = [int]$svgWidthNum * $scale
$scaledHeight = [int]$svgHeightNum * $scale

# Create HTML wrapper with proper scaling
$html = @"
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>$([System.IO.Path]::GetFileNameWithoutExtension($InputFile))</title>
    <style>
        @page {
            size: letter;
            margin: 0.75in;
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
        }
        
        html, body {
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            background: white;
            font-family: Arial, sans-serif;
        }
        
        .container {
            width: 100%;
            height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            page-break-inside: avoid;
        }
        
        .svg-container {
            width: ${scaledWidth}px;
            height: ${scaledHeight}px;
            max-width: 7.5in;
            max-height: 10in;
            overflow: visible;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        svg {
            width: 100% !important;
            height: 100% !important;
            max-width: 100%;
            max-height: 100%;
            background: white;
            border: 1px solid #ccc;
        }
        
        .figure-title {
            text-align: center;
            font-weight: bold;
            font-size: 12pt;
            margin-bottom: 10px;
            page-break-after: avoid;
        }
        
        @media print {
            html, body {
                width: 210mm;
                height: 297mm;
            }
            
            .container {
                height: 100vh;
                width: 100vw;
            }
            
            .svg-container {
                max-width: 7.5in;
                max-height: 9.5in;
            }
            
            * {
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="figure-title">$([System.IO.Path]::GetFileNameWithoutExtension($InputFile).Replace('_', ' ').ToUpper())</div>
        <div class="svg-container">
            $svgContent
        </div>
    </div>
</body>
</html>
"@

# Write HTML to file
$html | Out-File -FilePath $OutputFile -Encoding UTF8

Write-Output "Fixed SVG conversion: $InputFile -> $OutputFile"
Write-Output "Original size: ${svgWidth}x${svgHeight}, Scaled: ${scaledWidth}x${scaledHeight} (scale: $($scale.ToString('F2')))"