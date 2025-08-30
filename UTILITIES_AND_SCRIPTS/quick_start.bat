@echo off
title MWRASP Patent Search System
echo ========================================
echo MWRASP Patent Search System
echo ========================================
echo.

REM First install packages
echo Step 1: Installing required packages...
python -m pip install --upgrade pip --quiet
python -m pip install pandas numpy matplotlib seaborn plotly scikit-learn networkx wordcloud nltk aiohttp --quiet

echo.
echo Step 2: Starting Patent Search System...
echo.

cd "C:\Users\User\MWRASP-Quantum-Defense\CONSOLIDATED_PATENT_PORTFOLIO\PATENTS_TO_FILE\MWRASP_PATENT_INTELLIGENCE_SYSTEM"
python launch_patent_search_simple.py

pause