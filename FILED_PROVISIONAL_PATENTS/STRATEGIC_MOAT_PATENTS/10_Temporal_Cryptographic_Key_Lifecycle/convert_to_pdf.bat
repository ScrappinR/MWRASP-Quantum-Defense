@echo off
echo Converting Patent 10 SVG files to PDF...
echo.

cd /d "C:\Users\User\MWRASP-Quantum-Defense\FILED_PROVISIONAL_PATENTS\STRATEGIC_MOAT_PATENTS\10_Temporal_Cryptographic_Key_Lifecycle"

echo Converting Figure 1...
"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --headless --disable-gpu --run-all-compositor-stages-before-draw --virtual-time-budget=30000 --print-to-pdf="FIGURE_1_SYSTEM_ARCHITECTURE.pdf" --print-to-pdf-no-header --no-margins "FIGURE_1_SYSTEM_ARCHITECTURE.html"
echo.

echo Converting Figure 2...
"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --headless --disable-gpu --run-all-compositor-stages-before-draw --virtual-time-budget=30000 --print-to-pdf="FIGURE_2_KEY_LIFECYCLE_PROCESS.pdf" --print-to-pdf-no-header --no-margins "FIGURE_2_KEY_LIFECYCLE_PROCESS.html"
echo.

echo Converting Figure 3...
"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --headless --disable-gpu --run-all-compositor-stages-before-draw --virtual-time-budget=30000 --print-to-pdf="FIGURE_3_TEMPORAL_SECURITY_CONTROLS.pdf" --print-to-pdf-no-header --no-margins "FIGURE_3_TEMPORAL_SECURITY_CONTROLS.html"
echo.

echo Checking results...
dir *.pdf
echo.
echo Conversion complete!