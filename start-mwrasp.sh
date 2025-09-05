#!/bin/bash
# MWRASP Quantum Defense Platform - Unix/Linux Startup Script
# ===========================================================
# 
# Quick-start script for Unix/Linux/macOS systems.
# Run with: ./start-mwrasp.sh or bash start-mwrasp.sh

set -e  # Exit on error

echo ""
echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                      MWRASP QUANTUM DEFENSE PLATFORM                        ║"
echo "║                         Production System v3.0                              ║"
echo "║                                                                              ║"
echo "║  🛡️  Starting Unified Quantum Defense System...                             ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found! Please install Python 3.9+ from https://python.org"
    echo ""
    exit 1
fi

# Check Python version
python_version=$(python3 -c "import sys; print('.'.join(map(str, sys.version_info[:2])))")
required_version="3.9"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.9+ required. Found: $python_version"
    echo ""
    exit 1
fi

# Check if we're in the right directory
if [[ ! -f "mwrasp.py" ]]; then
    echo "❌ mwrasp.py not found! Please run this script from the MWRASP-Quantum-Defense directory."
    echo ""
    exit 1
fi

# Check if requirements are installed
echo "🔍 Checking system requirements..."
if ! python3 -c "import fastapi, uvicorn" &> /dev/null; then
    echo "⚠️ Required packages not found. Installing dependencies..."
    echo ""
    
    # Try to install requirements
    if command -v pip3 &> /dev/null; then
        pip3 install -r requirements-production.txt
    elif command -v pip &> /dev/null; then
        pip install -r requirements-production.txt
    else
        echo "❌ pip not found! Please install pip to install requirements."
        exit 1
    fi
fi

# Check for quantum hardware support (optional)
if ! python3 -c "import qiskit" &> /dev/null; then
    echo ""
    echo "⚠️ Quantum hardware support not detected."
    echo "💡 For IBM Quantum integration, run: pip3 install qiskit qiskit-ibm-runtime"
    echo "✅ System will run without quantum hardware validation."
    echo ""
fi

echo "✅ All requirements satisfied!"
echo ""

# Create default configuration if it doesn't exist
if [[ ! -f "mwrasp_config.json" ]]; then
    echo "📄 Creating default configuration file..."
    python3 mwrasp.py --create-config
fi

echo "🚀 Starting MWRASP Quantum Defense Platform..."
echo ""
echo "Available at: http://127.0.0.1:8000"
echo "Press Ctrl+C to stop the system"
echo ""

# Start the system with demonstration mode
python3 mwrasp-launcher.py --demo

echo ""
echo "👋 MWRASP Quantum Defense Platform stopped."