$edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

Get-ChildItem -Filter "*.html" | ForEach-Object {
    $pdfFile = [System.IO.Path]::ChangeExtension($_.FullName, ".pdf")
    Write-Output "Converting $($_.Name)..."
    
    Start-Process -FilePath $edgePath -ArgumentList "--headless", "--disable-gpu", "--print-to-pdf=`"$pdfFile`"", "`"$($_.FullName)`"" -Wait -WindowStyle Hidden
    
    if (Test-Path $pdfFile) {
        Write-Output "Success: $($_.Name)"
    } else {
        Write-Output "Failed: $($_.Name)"
    }
}