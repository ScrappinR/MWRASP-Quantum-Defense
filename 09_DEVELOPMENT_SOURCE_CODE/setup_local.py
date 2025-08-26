#!/usr/bin/env python3
"""
MWRASP Local Setup Script
Creates a complete local installation package
"""

import os
import zipfile
import shutil
from pathlib import Path

def create_local_package():
    """Create a local installation package"""
    print("Creating MWRASP local installation package...")
    
    # Get current directory (should be MWRASP-Quantum-Defense)
    current_dir = Path.cwd()
    
    # Create package directory
    package_dir = current_dir.parent / "MWRASP-Local-Package"
    if package_dir.exists():
        shutil.rmtree(package_dir)
    
    package_dir.mkdir()
    
    # Copy all files except __pycache__ and .pyc files
    for item in current_dir.iterdir():
        if item.name in ['__pycache__', '.git', 'setup_local.py']:
            continue
        
        if item.is_file():
            shutil.copy2(item, package_dir)
        elif item.is_dir():
            shutil.copytree(item, package_dir / item.name, 
                          ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    
    # Create setup instructions
    setup_instructions = """
# MWRASP Quantum Defense System - Local Installation

## Quick Start

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Simple Demo:**
   ```bash
   python simple_demo.py
   ```

3. **Run Full System with Web Dashboard:**
   ```bash
   python -m uvicorn src.api.server:app --reload --host 127.0.0.1 --port 8000
   ```
   Then open: http://127.0.0.1:8000/dashboard/index.html

4. **Run Tests:**
   ```bash
   pytest
   ```

## Demo Options

- **Interactive Menu Demo:** `python simple_demo.py`
- **Rich UI Demo:** `python demo.py` (may have issues on some Windows terminals)
- **Quick Demo:** `python demo.py --quick`
- **Verbose Demo:** `python simple_demo.py` (recommended for Windows)

## Troubleshooting

If you get import errors, run from the project root directory and ensure all dependencies are installed.

For Windows users, use `simple_demo.py` for best compatibility.
    """.strip()
    
    with open(package_dir / "LOCAL_SETUP.md", "w") as f:
        f.write(setup_instructions)
    
    print(f"Local package created at: {package_dir}")
    print("\nTo use:")
    print(f"1. Copy the contents of '{package_dir}' to your desired location")
    print("2. Follow the instructions in LOCAL_SETUP.md")
    
    return package_dir

if __name__ == "__main__":
    create_local_package()