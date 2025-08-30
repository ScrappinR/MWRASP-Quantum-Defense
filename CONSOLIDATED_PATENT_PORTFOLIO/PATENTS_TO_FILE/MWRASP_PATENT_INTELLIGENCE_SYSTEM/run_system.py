#!/usr/bin/env python3
"""
MWRASP Patent Intelligence System - Main Launcher
================================================

Main launcher script for the MWRASP Patent Intelligence System v3.0.
This script provides easy access to all system components and capabilities.

Usage Examples:
    python run_system.py                           # Interactive mode
    python run_system.py --portfolio               # Portfolio analysis
    python run_system.py --patent "patent.md"     # Single patent analysis
    python run_system.py --strengthen              # Interactive strengthening
    python run_system.py --search "quantum ML"    # Real-time patent search
    python run_system.py --file                   # USPTO filing preparation

Author: MWRASP Patent Development Team
Date: August 2025
Version: 3.0
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path

# Add core systems to Python path
current_dir = Path(__file__).parent
core_systems_dir = current_dir / "core_systems"
filing_automation_dir = current_dir / "filing_automation"

sys.path.insert(0, str(core_systems_dir))
sys.path.insert(0, str(filing_automation_dir))

def print_banner():
    """Print system banner"""
    print("=" * 80)
    print("MWRASP PATENT INTELLIGENCE SYSTEM v3.0")
    print("Professional Patent Analysis & Filing Automation Platform")
    print("=" * 80)
    print("[OK] Auto Deep Global Prior Art Searches")
    print("[OK] Professional Actionable Reports") 
    print("[OK] Valuable Whitespace Identification")
    print("[OK] Interactive Patent Strengthening")
    print("[OK] Automated USPTO Filing Integration")
    print("=" * 80)

def run_master_system(args):
    """Run the master patent intelligence system"""
    print("\n[LAUNCHING] Master Patent Intelligence System...")
    
    # Build command arguments
    cmd = [sys.executable, str(core_systems_dir / "master_patent_intelligence_system.py")]
    
    if args.portfolio:
        cmd.append("--portfolio")
    elif args.patent:
        cmd.extend(["--patent", args.patent])
    elif args.interactive:
        cmd.append("--interactive")
    else:
        # Default to interactive mode
        cmd.append("--interactive")
        
    if args.base_dir:
        cmd.extend(["--base-dir", args.base_dir])
    
    # Execute the master system
    result = subprocess.run(cmd, cwd=str(core_systems_dir))
    return result.returncode

def run_strengthening_interface():
    """Run interactive patent strengthening interface"""
    print("\n[LAUNCHING] Interactive Patent Strengthening Interface...")
    
    cmd = [sys.executable, str(core_systems_dir / "interactive_patent_strengthening_interface.py")]
    result = subprocess.run(cmd, cwd=str(core_systems_dir))
    return result.returncode

def run_real_time_search(search_terms=None):
    """Run real-time patent search"""
    print("\n[LAUNCHING] Real-Time Patent Search Engine...")
    
    if search_terms:
        print(f"[INFO] Search terms: {search_terms}")
    
    cmd = [sys.executable, str(core_systems_dir / "real_time_patent_search.py")]
    result = subprocess.run(cmd, cwd=str(core_systems_dir))
    return result.returncode

def run_filing_system():
    """Run USPTO filing system"""
    print("\n[LAUNCHING] USPTO Filing Automation System...")
    
    cmd = [sys.executable, str(filing_automation_dir / "automated_patent_filing_system.py")]
    result = subprocess.run(cmd, cwd=str(filing_automation_dir))
    return result.returncode

def run_enhanced_prior_art():
    """Run enhanced prior art analysis"""
    print("\n[LAUNCHING] Enhanced Prior Art Analysis System...")
    
    cmd = [sys.executable, str(core_systems_dir / "enhanced_prior_art_system.py")]
    result = subprocess.run(cmd, cwd=str(core_systems_dir))
    return result.returncode

def show_system_status():
    """Show system status and available components"""
    print("\n[SYSTEM STATUS]")
    print("-" * 50)
    
    # Check core system files
    core_files = [
        "master_patent_intelligence_system.py",
        "enhanced_prior_art_system.py", 
        "real_time_patent_search.py",
        "interactive_patent_strengthening_interface.py",
        "integrated_patent_intelligence.py"
    ]
    
    print("Core Systems:")
    for file in core_files:
        file_path = core_systems_dir / file
        status = "[OK]" if file_path.exists() else "[MISSING]"
        print(f"  {status} {file}")
    
    # Check filing automation files  
    filing_files = [
        "automated_patent_filing_system.py",
        "ads_generator.py",
        "document_validator.py",
        "uspto_form_automation.py",
        "pdf_converter.py"
    ]
    
    print("\nFiling Automation:")
    for file in filing_files:
        file_path = filing_automation_dir / file
        status = "[OK]" if file_path.exists() else "[MISSING]"
        print(f"  {status} {file}")
    
    # Check analysis results directories
    analysis_dir = current_dir / "analysis_results"
    print(f"\nAnalysis Results Directory: {analysis_dir}")
    print(f"  Status: {'[OK]' if analysis_dir.exists() else '[MISSING]'}")
    
    if analysis_dir.exists():
        subdirs = [d for d in analysis_dir.iterdir() if d.is_dir()]
        print(f"  Subdirectories: {len(subdirs)}")
        for subdir in subdirs:
            print(f"    - {subdir.name}")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='MWRASP Patent Intelligence System v3.0',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_system.py                           # Interactive mode
  python run_system.py --portfolio               # Portfolio analysis  
  python run_system.py --patent "patent.md"     # Single patent analysis
  python run_system.py --strengthen              # Interactive strengthening
  python run_system.py --search "quantum ML"    # Real-time patent search
  python run_system.py --file                   # USPTO filing preparation
  python run_system.py --status                 # System status check
        """
    )
    
    # Main operation modes
    parser.add_argument('--portfolio', action='store_true', 
                       help='Run portfolio-wide comprehensive analysis')
    parser.add_argument('--patent', type=str, 
                       help='Run single patent analysis (provide patent file path)')
    parser.add_argument('--strengthen', action='store_true',
                       help='Run interactive patent strengthening session')
    parser.add_argument('--search', type=str,
                       help='Run real-time patent search (provide search terms)')
    parser.add_argument('--file', action='store_true',
                       help='Run USPTO filing automation system')
    parser.add_argument('--prior-art', action='store_true',
                       help='Run enhanced prior art analysis')
    parser.add_argument('--interactive', action='store_true',
                       help='Run interactive CLI mode')
    parser.add_argument('--status', action='store_true',
                       help='Show system status and component availability')
    
    # Configuration options
    parser.add_argument('--base-dir', type=str,
                       help='Base directory for patent files')
    
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    # Handle status check
    if args.status:
        show_system_status()
        return 0
    
    # Determine operation mode and execute
    try:
        if args.strengthen:
            return run_strengthening_interface()
        elif args.search:
            return run_real_time_search(args.search)
        elif args.file:
            return run_filing_system()
        elif args.prior_art:
            return run_enhanced_prior_art()
        else:
            # Default to master system (handles portfolio, patent, interactive modes)
            return run_master_system(args)
            
    except KeyboardInterrupt:
        print("\n\n[INTERRUPTED] System operation cancelled by user")
        return 1
    except Exception as e:
        print(f"\n[ERROR] System operation failed: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)