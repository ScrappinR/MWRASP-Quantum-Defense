@echo off
REM MWRASP Quantum Defense Platform - Windows Startup Script
REM ========================================================
REM 
REM Quick-start script for Windows systems.
REM Double-click to run or execute from command line.

echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                      MWRASP QUANTUM DEFENSE PLATFORM                        ║  
echo ║                         Production System v3.0                              ║
echo ║                                                                              ║
echo ║  🛡️  Starting Unified Quantum Defense System...                             ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found! Please install Python 3.9+ from https://python.org
    echo.
    pause
    exit /b 1
)

REM Check if we're in the right directory
if not exist "mwrasp.py" (
    echo ❌ mwrasp.py not found! Please run this script from the MWRASP-Quantum-Defense directory.
    echo.
    pause
    exit /b 1
)

REM Check if requirements are installed
echo 🔍 Checking system requirements...
python -c "import fastapi, uvicorn" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️ Required packages not found. Installing dependencies...
    echo.
    pip install -r requirements-production.txt
    if %errorlevel% neq 0 (
        echo ❌ Failed to install requirements. Please check your internet connection.
        echo.
        pause
        exit /b 1
    )
)

REM Check for quantum hardware support (optional)
python -c "import qiskit" >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ⚠️ Quantum hardware support not detected.
    echo 💡 For IBM Quantum integration, run: pip install qiskit qiskit-ibm-runtime
    echo ✅ System will run without quantum hardware validation.
    echo.
)

echo ✅ All requirements satisfied!
echo.

REM Create default configuration if it doesn't exist
if not exist "mwrasp_config.json" (
    echo 📄 Creating default configuration file...
    python mwrasp.py --create-config
)

echo 🚀 Starting MWRASP Quantum Defense Platform...
echo.
echo Available at: http://127.0.0.1:8000
echo Press Ctrl+C to stop the system
echo.

REM Start the system with demonstration mode
python mwrasp-launcher.py --demo

echo.
echo 👋 MWRASP Quantum Defense Platform stopped.
pause