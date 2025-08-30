@echo off
echo ========================================
echo MWRASP Patent Search and Analysis System
echo ========================================
echo.
echo Installing required packages...
pip install pandas numpy matplotlib seaborn plotly scikit-learn networkx wordcloud nltk aiohttp --quiet
echo.
echo Starting Patent Search System...
echo.

cd "C:\Users\User\MWRASP-Quantum-Defense\CONSOLIDATED_PATENT_PORTFOLIO\PATENTS_TO_FILE\MWRASP_PATENT_INTELLIGENCE_SYSTEM"

python launch_patent_search_system.py

pause