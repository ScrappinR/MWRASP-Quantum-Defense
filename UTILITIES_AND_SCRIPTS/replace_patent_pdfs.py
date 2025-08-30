#!/usr/bin/env python3
"""
Replace Patent PDF Files
=========================

Replace the old PDF files with the updated ones containing RUTHERFORD docket numbers.
"""

import os
import shutil
import time
from pathlib import Path

def replace_pdf_files():
    """Replace the original PDF files with updated versions"""
    
    print("Replacing original PDF files with updated RUTHERFORD versions...")
    print("=" * 70)
    
    base_dir = Path("C:/Users/User/MWRASP-Quantum-Defense/CONSOLIDATED_PATENT_PORTFOLIO/PATENTS_TO_FILE/uspto_filing_packages")
    
    patents = [
        "Patent_15_Filing_Package",
        "Patent_16_Filing_Package", 
        "Patent_17_Filing_Package",
        "Patent_18_Filing_Package"
    ]
    
    success_count = 0
    
    for patent_dir in patents:
        print(f"\nProcessing {patent_dir}...")
        
        patent_path = base_dir / patent_dir
        original_pdf = patent_path / "PROVISIONAL_PATENT_APPLICATION.pdf"
        updated_pdf = patent_path / "PROVISIONAL_PATENT_APPLICATION_UPDATED.pdf"
        backup_pdf = patent_path / "PROVISIONAL_PATENT_APPLICATION_OLD.pdf"
        
        if not updated_pdf.exists():
            print(f"   [ERROR] Updated PDF not found: {updated_pdf}")
            continue
        
        try:
            # Remove old backup if exists
            if backup_pdf.exists():
                backup_pdf.unlink()
                print(f"   [INFO] Removed old backup")
            
            # Backup original if exists
            if original_pdf.exists():
                # Wait a moment for any file locks to release
                time.sleep(1)
                shutil.move(str(original_pdf), str(backup_pdf))
                print(f"   [INFO] Backed up original PDF")
            
            # Move updated file to replace original
            shutil.move(str(updated_pdf), str(original_pdf))
            print(f"   [OK] Replaced with updated PDF containing RUTHERFORD docket number")
            success_count += 1
            
        except Exception as e:
            print(f"   [ERROR] Failed to replace PDF: {e}")
            # Try to restore backup if something went wrong
            try:
                if backup_pdf.exists() and not original_pdf.exists():
                    shutil.move(str(backup_pdf), str(original_pdf))
                    print(f"   [INFO] Restored original PDF")
            except:
                pass
    
    print(f"\n" + "=" * 70)
    print(f"Replacement Summary:")
    print(f"  - Attempted: {len(patents)} patents")
    print(f"  - Successfully replaced: {success_count} PDFs")
    print(f"  - All replaced PDFs now contain updated RUTHERFORD docket numbers")
    
    if success_count == len(patents):
        print(f"\n[SUCCESS] All PDF files have been updated with RUTHERFORD docket numbers!")
    else:
        print(f"\n[WARNING] Some PDF replacements failed. Check individual patent directories.")

if __name__ == "__main__":
    replace_pdf_files()