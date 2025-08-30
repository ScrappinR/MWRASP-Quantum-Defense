#!/usr/bin/env python3
"""
Install Requirements for Patent Search System
============================================

Installs all required packages for the patent search and analysis system.
"""

import subprocess
import sys

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--quiet"])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    """Install all required packages"""
    
    print("🔧 Installing Patent Search System Requirements...")
    print("=" * 60)
    
    required_packages = [
        "pandas",
        "numpy", 
        "matplotlib",
        "seaborn",
        "plotly",
        "scikit-learn",
        "networkx",
        "wordcloud",
        "nltk",
        "aiohttp"
    ]
    
    installed = []
    failed = []
    
    for package in required_packages:
        print(f"📦 Installing {package}...", end=" ")
        if install_package(package):
            print("✅")
            installed.append(package)
        else:
            print("❌") 
            failed.append(package)
    
    print("\n" + "=" * 60)
    print(f"✅ Successfully installed: {len(installed)} packages")
    print(f"❌ Failed to install: {len(failed)} packages")
    
    if failed:
        print(f"\nFailed packages: {', '.join(failed)}")
        print("Please install these manually using: pip install <package_name>")
    else:
        print("\n🚀 All packages installed successfully!")
        print("You can now run the patent search system.")

if __name__ == "__main__":
    main()