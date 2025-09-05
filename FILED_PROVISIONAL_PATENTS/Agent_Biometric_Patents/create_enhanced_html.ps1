# Create enhanced HTML files with better scaling controls
Write-Output "Creating enhanced HTML files with manual scaling controls..."

function Create-EnhancedHTML {
    param($svgFile, $htmlFile)
    
    $svgContent = Get-Content $svgFile -Raw -Encoding UTF8
    $figureName = [System.IO.Path]::GetFileNameWithoutExtension($svgFile)
    
    # Enhanced HTML with multiple scaling options and controls
    $html = @"
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>$figureName - Enhanced Scaling</title>
    <style>
        @page {
            size: letter;
            margin: 0.5in;
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
        }
        
        body {
            margin: 0;
            padding: 20px;
            background: white;
            font-family: Arial, sans-serif;
        }
        
        .controls {
            text-align: center;
            margin-bottom: 20px;
            page-break-after: avoid;
        }
        
        .controls button {
            margin: 0 5px;
            padding: 5px 10px;
            font-size: 12px;
        }
        
        .title {
            text-align: center;
            font-size: 14pt;
            font-weight: bold;
            margin-bottom: 15px;
            color: black;
        }
        
        .container {
            width: 7.5in;
            height: 10in;
            margin: 0 auto;
            background: white;
            border: 2px solid #ddd;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
            position: relative;
        }
        
        .svg-wrapper {
            transition: transform 0.3s ease;
            transform-origin: center center;
        }
        
        /* Scaling classes */
        .scale-50 { transform: scale(0.5); }
        .scale-60 { transform: scale(0.6); }
        .scale-70 { transform: scale(0.7); }
        .scale-75 { transform: scale(0.75); }
        .scale-80 { transform: scale(0.8); }
        .scale-85 { transform: scale(0.85); }
        .scale-90 { transform: scale(0.9); }
        .scale-95 { transform: scale(0.95); }
        .scale-100 { transform: scale(1.0); }
        
        svg {
            background: white !important;
            display: block;
        }
        
        .instructions {
            margin-top: 20px;
            padding: 15px;
            background: #f5f5f5;
            border-radius: 5px;
            font-size: 11pt;
        }
        
        .instructions h3 {
            margin-top: 0;
            color: #333;
        }
        
        @media print {
            .controls, .instructions {
                display: none !important;
            }
            
            body {
                margin: 0;
                padding: 0.5in;
            }
            
            .container {
                border: none;
                width: 7.5in;
                height: 10in;
            }
            
            * {
                -webkit-print-color-adjust: exact !important;
                color-adjust: exact !important;
            }
        }
    </style>
    <script>
        function setScale(scale) {
            const wrapper = document.querySelector('.svg-wrapper');
            wrapper.className = 'svg-wrapper scale-' + scale;
            
            // Update button states
            document.querySelectorAll('.scale-btn').forEach(btn => {
                btn.style.backgroundColor = '#f0f0f0';
            });
            document.querySelector('[data-scale="' + scale + '"]').style.backgroundColor = '#007bff';
            document.querySelector('[data-scale="' + scale + '"]').style.color = 'white';
        }
        
        function fitToPage() {
            const container = document.querySelector('.container');
            const svg = document.querySelector('svg');
            if (svg) {
                const svgRect = svg.getBoundingClientRect();
                const containerRect = container.getBoundingClientRect();
                
                const scaleX = (containerRect.width - 20) / svgRect.width;
                const scaleY = (containerRect.height - 20) / svgRect.height;
                const scale = Math.min(scaleX, scaleY, 1);
                
                const wrapper = document.querySelector('.svg-wrapper');
                wrapper.style.transform = 'scale(' + scale + ')';
            }
        }
        
        window.onload = function() {
            setScale('85'); // Default to 85%
        };
    </script>
</head>
<body>
    <div class="controls">
        <h2>Patent Figure Scaling Control</h2>
        <p><strong>$figureName</strong></p>
        <div>
            <button class="scale-btn" data-scale="50" onclick="setScale('50')">50%</button>
            <button class="scale-btn" data-scale="60" onclick="setScale('60')">60%</button>
            <button class="scale-btn" data-scale="70" onclick="setScale('70')">70%</button>
            <button class="scale-btn" data-scale="75" onclick="setScale('75')">75%</button>
            <button class="scale-btn" data-scale="80" onclick="setScale('80')">80%</button>
            <button class="scale-btn" data-scale="85" onclick="setScale('85')">85%</button>
            <button class="scale-btn" data-scale="90" onclick="setScale('90')">90%</button>
            <button class="scale-btn" data-scale="95" onclick="setScale('95')">95%</button>
            <button class="scale-btn" data-scale="100" onclick="setScale('100')">100%</button>
            <button onclick="fitToPage()">Auto Fit</button>
        </div>
    </div>
    
    <div class="title">$($figureName.Replace('_', ' ').ToUpper())</div>
    
    <div class="container">
        <div class="svg-wrapper scale-85">
            $svgContent
        </div>
    </div>
    
    <div class="instructions">
        <h3>Instructions for PDF Conversion:</h3>
        <ol>
            <li>Click scale buttons above to find the best fit (try 75-85% first)</li>
            <li>Ensure the entire diagram is visible within the border</li>
            <li>Press <strong>Ctrl+P</strong> to print</li>
            <li>Select "Save as PDF" or "Microsoft Print to PDF"</li>
            <li>Settings: Paper=Letter, Margins=Default, Background graphics=ON</li>
            <li>Save as: <strong>$figureName.pdf</strong></li>
        </ol>
        <p><strong>Quality Check:</strong> Verify all text is readable and no parts are cut off in the PDF.</p>
    </div>
</body>
</html>
"@
    
    $html | Out-File -FilePath $htmlFile -Encoding UTF8
    Write-Output "Enhanced: $([System.IO.Path]::GetFileName($htmlFile))"
}

# Create enhanced HTML files for all figures
$dirs = @(
    "01_Adaptive_Multi_Modal_AI_Agent_Authentication",
    "02_AI_Agent_Computational_Biometric_Identification",
    "03_Clandestine_AI_Agent_Communication_Through_Biometric_Channels"
)

$totalCreated = 0

foreach ($dir in $dirs) {
    if (Test-Path $dir) {
        Write-Output ""
        Write-Output "Processing: $dir"
        
        Get-ChildItem -Path $dir -Filter "FIGURE_*.svg" | ForEach-Object {
            $enhancedHtml = [System.IO.Path]::ChangeExtension($_.FullName, "_ENHANCED.html")
            Create-EnhancedHTML -svgFile $_.FullName -htmlFile $enhancedHtml
            $totalCreated++
        }
    }
}

Write-Output ""
Write-Output "=== ENHANCED HTML FILES CREATED ==="
Write-Output "Total enhanced HTML files: $totalCreated"
Write-Output ""
Write-Output "Each file now includes:"
Write-Output "- Interactive scale buttons (50% to 100%)"
Write-Output "- Auto-fit function"
Write-Output "- Visual border to check fit"
Write-Output "- Step-by-step PDF conversion instructions"
Write-Output ""
Write-Output "Open any _ENHANCED.html file in your browser to:"
Write-Output "1. Test different scales interactively"
Write-Output "2. Find the perfect fit for each figure"  
Write-Output "3. Print to PDF with confidence"