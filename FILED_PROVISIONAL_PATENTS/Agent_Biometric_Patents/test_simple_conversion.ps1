# Simple test conversion
$edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
$svgPath = "C:\Users\User\MWRASP-Quantum-Defense\FILED_PROVISIONAL_PATENTS\Agent_Biometric_Patents\01_Adaptive_Multi_Modal_AI_Agent_Authentication\FIGURE_1_SYSTEM_ARCHITECTURE.svg"
$pdfPath = "C:\Users\User\MWRASP-Quantum-Defense\FILED_PROVISIONAL_PATENTS\Agent_Biometric_Patents\01_Adaptive_Multi_Modal_AI_Agent_Authentication\FIGURE_1_TEST.pdf"

# Create simple HTML
$svgContent = Get-Content $svgPath -Raw
$html = @"
<!DOCTYPE html>
<html><head><style>@page{size:8.5in 11in;margin:0.5in;}body{margin:0;padding:0;background:white;}svg{width:100%;height:auto;max-width:7.5in;display:block;}</style></head>
<body>$svgContent</body></html>
"@

$html | Out-File "temp.html" -Encoding UTF8

$args = "--headless --disable-gpu --print-to-pdf=`"$pdfPath`" --print-to-pdf-no-header temp.html"
Start-Process -FilePath $edgePath -ArgumentList $args -Wait -NoNewWindow

if (Test-Path $pdfPath) {
    Write-Host "SUCCESS: Created $pdfPath" -ForegroundColor Green
} else {
    Write-Host "FAILED" -ForegroundColor Red
}

Remove-Item "temp.html" -ErrorAction SilentlyContinue