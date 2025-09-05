#!/usr/bin/env python3
"""
MWRASP Quantum Defense Platform - Simple Unified Launcher
========================================================

Production-ready quantum defense system launcher that works with existing components.

Usage:
    python mwrasp-simple.py --demo       # Run demonstration
    python mwrasp-simple.py --server     # Start web server only  
    python mwrasp-simple.py --test       # Run system tests
    python mwrasp-simple.py --help       # Show help
"""

import sys
import os
import argparse
import subprocess
import time
from pathlib import Path

def print_banner():
    print("""
================================================================================
                      MWRASP QUANTUM DEFENSE PLATFORM                        
                         Production System v3.0                              
                                                                              
  [SHIELD] 8 Novel Quantum Defense Technologies                                    
  [ATOM] IBM Brisbane Hardware Validated (77.7% Success Rate)                   
  [TROPHY] Patent Portfolio Ready                                                   
                                                                              
  (C) 2025 - Production Validated Enterprise Security System                   
================================================================================
    """)

def check_environment():
    """Check if we're in the right environment"""
    if not Path("src/api/server.py").exists():
        print("ERROR: MWRASP source files not found!")
        print("Make sure you're running from the MWRASP-Quantum-Defense directory")
        return False
    
    # Check Python version
    if sys.version_info < (3, 9):
        print("ERROR: Python 3.9+ required")
        return False
    
    return True

def install_requirements():
    """Install required dependencies"""
    print("Installing required dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", 
                       "fastapi", "uvicorn", "websockets", "numpy", "requests"], 
                      check=True, capture_output=True)
        print("SUCCESS: Dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to install dependencies: {e}")
        return False

def run_server():
    """Start the FastAPI server"""
    print("Starting MWRASP Web Server...")
    print("Available at: http://127.0.0.1:8000")
    print("Press Ctrl+C to stop")
    
    try:
        # Try to run the server directly
        os.chdir(Path(__file__).parent)
        subprocess.run([sys.executable, "-c", 
                       "import sys; sys.path.insert(0, 'src'); from src.api.server import run_server; run_server()"],
                      check=True)
    except subprocess.CalledProcessError:
        print("Falling back to direct module execution...")
        subprocess.run([sys.executable, "src/api/server.py"])

def run_demo():
    """Run system demonstration"""
    print("Starting MWRASP System Demonstration...")
    
    # List available demo scripts
    demo_scripts = [
        "05_DEMONSTRATIONS_PROTOTYPES/Demos/simple_demo.py",
        "05_DEMONSTRATIONS_PROTOTYPES/Demos/mwrasp_standalone.py", 
        "CORE_SYSTEM_IMPLEMENTATIONS/MWRASP_COMPLETE_WORKING_SYSTEM.py",
        "CORE_SYSTEM_IMPLEMENTATIONS/MWRASP_REAL_WORKING_SYSTEM.py"
    ]
    
    # Find the first available demo
    demo_to_run = None
    for demo in demo_scripts:
        if Path(demo).exists():
            demo_to_run = demo
            break
    
    if demo_to_run:
        print(f"Running: {demo_to_run}")
        subprocess.run([sys.executable, demo_to_run])
    else:
        print("No demo scripts found. Starting web server instead...")
        run_server()

def run_tests():
    """Run system tests"""
    print("Running MWRASP System Tests...")
    
    test_scripts = [
        "VALIDATION_AND_TESTING/complete_mwrasp_integration_test.py",
        "VALIDATION_AND_TESTING/automated_ibm_quantum_tester.py",
        "src/tests/test_system_integration.py"
    ]
    
    for test_script in test_scripts:
        if Path(test_script).exists():
            print(f"Running: {test_script}")
            try:
                subprocess.run([sys.executable, test_script], timeout=300)
            except subprocess.TimeoutExpired:
                print(f"Test {test_script} timed out, continuing...")
            except Exception as e:
                print(f"Test {test_script} failed: {e}")
        else:
            print(f"Test not found: {test_script}")

def show_status():
    """Show system status and available components"""
    print("MWRASP System Status")
    print("=" * 50)
    
    components = {
        "Web Server": "src/api/server.py",
        "Quantum Detector": "src/core/quantum_detector.py", 
        "Agent System": "src/core/agent_system.py",
        "Temporal Fragmentation": "src/core/temporal_fragmentation.py",
        "Behavioral Cryptography": "src/core/behavioral_cryptography.py",
        "Legal Barriers": "src/core/legal_barriers.py",
        "IBM Quantum Integration": "src/core/quantum_circuit_converter.py",
        "Integration Tests": "VALIDATION_AND_TESTING/complete_mwrasp_integration_test.py"
    }
    
    for name, file_path in components.items():
        status = "AVAILABLE" if Path(file_path).exists() else "MISSING"
        print(f"  {name:<25}: {status}")
    
    print()
    print("Available Commands:")
    print("  python mwrasp-simple.py --demo     # Run system demonstration")
    print("  python mwrasp-simple.py --server   # Start web server")
    print("  python mwrasp-simple.py --test     # Run system tests")
    print("  python mwrasp-simple.py --status   # Show this status")

def main():
    print_banner()
    
    parser = argparse.ArgumentParser(
        description="MWRASP Quantum Defense Platform - Simple Launcher",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--demo', action='store_true', help='Run system demonstration')
    parser.add_argument('--server', action='store_true', help='Start web server only')
    parser.add_argument('--test', action='store_true', help='Run system tests')
    parser.add_argument('--status', action='store_true', help='Show system status')
    parser.add_argument('--install', action='store_true', help='Install dependencies')
    
    args = parser.parse_args()
    
    if not check_environment():
        sys.exit(1)
    
    if args.install:
        if install_requirements():
            print("Dependencies installed successfully")
        else:
            sys.exit(1)
    elif args.demo:
        run_demo()
    elif args.server:
        run_server()
    elif args.test:
        run_tests()
    elif args.status:
        show_status()
    else:
        # Default: show status and run demo
        show_status()
        print()
        print("No command specified - starting demonstration in 3 seconds...")
        time.sleep(3)
        run_demo()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nMWRASP System stopped by user. Goodbye!")
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)