@echo off
REM MWRASP HTML to PDF Conversion Batch Script
echo MWRASP HTML to PDF Conversion
echo =============================

REM Set paths
set HTML_PATH=C:\Users\User\MWRASP-Quantum-Defense\HTML_TEMP
set PDF_PATH=C:\Users\User\MWRASP-Quantum-Defense\PDF_DOCUMENTS

REM Create PDF directory
if not exist "%PDF_PATH%" mkdir "%PDF_PATH%"

REM Find Chrome
set CHROME_PATH=""
if exist "%ProgramFiles%\Google\Chrome\Application\chrome.exe" (
    set CHROME_PATH="%ProgramFiles%\Google\Chrome\Application\chrome.exe"
) else if exist "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe" (
    set CHROME_PATH="%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"
) else if exist "%LocalAppData%\Google\Chrome\Application\chrome.exe" (
    set CHROME_PATH="%LocalAppData%\Google\Chrome\Application\chrome.exe"
) else if exist "%ProgramFiles%\Microsoft\Edge\Application\msedge.exe" (
    set CHROME_PATH="%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"
) else (
    echo Error: Chrome or Edge browser not found
    echo Please install Chrome or Edge to continue
    pause
    exit /b 1
)

echo Using browser: %CHROME_PATH%
echo.

REM Convert key documents first (priority files)
echo Converting priority documents...

REM Executive Summary
if not exist "%PDF_PATH%\01_EXECUTIVE_SUMMARY" mkdir "%PDF_PATH%\01_EXECUTIVE_SUMMARY"
%CHROME_PATH% --headless --disable-gpu --print-to-pdf="%PDF_PATH%\01_EXECUTIVE_SUMMARY\PROJECT_OVERVIEW.pdf" "file:///%HTML_PATH%\01_EXECUTIVE_SUMMARY\PROJECT_OVERVIEW.html"
echo   PROJECT_OVERVIEW.pdf - Created

%CHROME_PATH% --headless --disable-gpu --print-to-pdf="%PDF_PATH%\01_EXECUTIVE_SUMMARY\FUNDING_ACTION_PLAN.pdf" "file:///%HTML_PATH%\01_EXECUTIVE_SUMMARY\FUNDING_ACTION_PLAN.html"
echo   FUNDING_ACTION_PLAN.pdf - Created

REM DARPA Materials
if not exist "%PDF_PATH%\02_FUNDING_MATERIALS\DARPA" mkdir "%PDF_PATH%\02_FUNDING_MATERIALS\DARPA"
%CHROME_PATH% --headless --disable-gpu --print-to-pdf="%PDF_PATH%\02_FUNDING_MATERIALS\DARPA\MWRASP_DARPA_Whitepaper.pdf" "file:///%HTML_PATH%\02_FUNDING_MATERIALS\DARPA\MWRASP_DARPA_Whitepaper.html"
echo   MWRASP_DARPA_Whitepaper.pdf - Created

REM Investment Materials
if not exist "%PDF_PATH%\02_FUNDING_MATERIALS\Private_Investment" mkdir "%PDF_PATH%\02_FUNDING_MATERIALS\Private_Investment"
%CHROME_PATH% --headless --disable-gpu --print-to-pdf="%PDF_PATH%\02_FUNDING_MATERIALS\Private_Investment\05_INVESTMENT_PROSPECTUS_COMPLETE.pdf" "file:///%HTML_PATH%\02_FUNDING_MATERIALS\Private_Investment\05_INVESTMENT_PROSPECTUS_COMPLETE.html"
echo   05_INVESTMENT_PROSPECTUS_COMPLETE.pdf - Created

%CHROME_PATH% --headless --disable-gpu --print-to-pdf="%PDF_PATH%\02_FUNDING_MATERIALS\Private_Investment\23_EXECUTIVE_PRESENTATION_DECK.pdf" "file:///%HTML_PATH%\02_FUNDING_MATERIALS\Private_Investment\23_EXECUTIVE_PRESENTATION_DECK.html"
echo   23_EXECUTIVE_PRESENTATION_DECK.pdf - Created

%CHROME_PATH% --headless --disable-gpu --print-to-pdf="%PDF_PATH%\02_FUNDING_MATERIALS\Private_Investment\17_COMPETITIVE_ANALYSIS.pdf" "file:///%HTML_PATH%\02_FUNDING_MATERIALS\Private_Investment\17_COMPETITIVE_ANALYSIS.html"
echo   17_COMPETITIVE_ANALYSIS.pdf - Created

REM Technical Documentation
if not exist "%PDF_PATH%\03_TECHNICAL_DOCUMENTATION\System_Architecture" mkdir "%PDF_PATH%\03_TECHNICAL_DOCUMENTATION\System_Architecture"
%CHROME_PATH% --headless --disable-gpu --print-to-pdf="%PDF_PATH%\03_TECHNICAL_DOCUMENTATION\System_Architecture\COMPLETE_SYSTEM_ARCHITECTURE.pdf" "file:///%HTML_PATH%\03_TECHNICAL_DOCUMENTATION\System_Architecture\COMPLETE_SYSTEM_ARCHITECTURE.html"
echo   COMPLETE_SYSTEM_ARCHITECTURE.pdf - Created

REM Patent Portfolio
if not exist "%PDF_PATH%\04_PATENTS_INTELLECTUAL_PROPERTY\Patent_Strategy" mkdir "%PDF_PATH%\04_PATENTS_INTELLECTUAL_PROPERTY\Patent_Strategy"
%CHROME_PATH% --headless --disable-gpu --print-to-pdf="%PDF_PATH%\04_PATENTS_INTELLECTUAL_PROPERTY\Patent_Strategy\COMPLETE_IP_PORTFOLIO.pdf" "file:///%HTML_PATH%\04_PATENTS_INTELLECTUAL_PROPERTY\Patent_Strategy\COMPLETE_IP_PORTFOLIO.html"
echo   COMPLETE_IP_PORTFOLIO.pdf - Created

echo.
echo Priority documents converted successfully!
echo.
echo Full conversion instructions:
echo 1. Key PDF documents are ready in: %PDF_PATH%
echo 2. For full conversion, use the PowerShell script or browser print
echo 3. All 109 HTML files are available in: %HTML_PATH%
echo.

REM Create quick access shortcuts
echo Creating PDF_QUICK_ACCESS.txt...
(
echo MWRASP Quantum Defense System - Quick PDF Access
echo ==============================================
echo.
echo Key Documents for Funding and Presentations:
echo.
echo EXECUTIVE OVERVIEW:
echo %PDF_PATH%\01_EXECUTIVE_SUMMARY\PROJECT_OVERVIEW.pdf
echo.
echo DARPA FUNDING:
echo %PDF_PATH%\02_FUNDING_MATERIALS\DARPA\MWRASP_DARPA_Whitepaper.pdf
echo.
echo PRIVATE INVESTMENT:
echo %PDF_PATH%\02_FUNDING_MATERIALS\Private_Investment\05_INVESTMENT_PROSPECTUS_COMPLETE.pdf
echo %PDF_PATH%\02_FUNDING_MATERIALS\Private_Investment\23_EXECUTIVE_PRESENTATION_DECK.pdf
echo.
echo COMPETITIVE ANALYSIS:
echo %PDF_PATH%\02_FUNDING_MATERIALS\Private_Investment\17_COMPETITIVE_ANALYSIS.pdf
echo.
echo TECHNICAL ARCHITECTURE:
echo %PDF_PATH%\03_TECHNICAL_DOCUMENTATION\System_Architecture\COMPLETE_SYSTEM_ARCHITECTURE.pdf
echo.
echo PATENT PORTFOLIO:
echo %PDF_PATH%\04_PATENTS_INTELLECTUAL_PROPERTY\Patent_Strategy\COMPLETE_IP_PORTFOLIO.pdf
echo.
echo All 109 HTML files available for browser printing at:
echo %HTML_PATH%
echo.
echo Generated: %date% %time%
) > "%PDF_PATH%\PDF_QUICK_ACCESS.txt"

echo PDF_QUICK_ACCESS.txt created with file locations
echo.
echo =============================
echo CONVERSION COMPLETE
echo =============================
echo Key PDF documents ready for:
echo - DARPA funding submissions
echo - Private investor presentations  
echo - Strategic acquisition discussions
echo - Government stakeholder briefings
echo.
pause