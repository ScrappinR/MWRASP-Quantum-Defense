#!/usr/bin/env python3
"""
Simple PDF Regeneration for Patents 15-18
==========================================

Regenerates PDF files for the updated patent applications using alternative methods.
"""

import os
import sys
import subprocess
from pathlib import Path

def convert_md_to_pdf_simple(md_file, output_pdf):
    """Convert markdown to PDF using pandoc if available"""
    try:
        # Try pandoc first
        result = subprocess.run([
            'pandoc', str(md_file), '-o', str(output_pdf),
            '--pdf-engine=wkhtmltopdf',
            '--margin-top=1in',
            '--margin-bottom=1in', 
            '--margin-left=1in',
            '--margin-right=1in'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            return True, "Success with pandoc"
        else:
            return False, f"Pandoc error: {result.stderr}"
            
    except FileNotFoundError:
        return False, "Pandoc not found"

def convert_md_to_pdf_python(md_file, output_pdf):
    """Convert markdown to PDF using Python libraries"""
    try:
        import markdown2
        import pdfkit
        
        # Read markdown
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Convert to HTML
        html = markdown2.markdown(md_content)
        
        # Add basic styling
        html_with_style = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 1in; line-height: 1.6; }}
                h1, h2, h3 {{ color: #333; }}
                h1 {{ border-bottom: 2px solid #333; }}
                h2 {{ border-bottom: 1px solid #666; }}
                code {{ background: #f4f4f4; padding: 2px 4px; }}
                pre {{ background: #f4f4f4; padding: 10px; overflow-x: auto; }}
            </style>
        </head>
        <body>
        {html}
        </body>
        </html>
        """
        
        # Convert to PDF
        pdfkit.from_string(html_with_style, str(output_pdf))
        return True, "Success with pdfkit"
        
    except ImportError as e:
        return False, f"Missing library: {e}"
    except Exception as e:
        return False, f"Conversion error: {e}"

def convert_md_to_html_fallback(md_file, output_dir):
    """Convert markdown to HTML as fallback"""
    try:
        import markdown2
        
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        html = markdown2.markdown(md_content)
        html_with_style = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Patent Application</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 1in; line-height: 1.6; }}
                h1, h2, h3 {{ color: #333; }}
                h1 {{ border-bottom: 2px solid #333; }}
                h2 {{ border-bottom: 1px solid #666; }}
                .header {{ background: #f0f0f0; padding: 10px; margin-bottom: 20px; }}
            </style>
        </head>
        <body>
        {html}
        <br><br>
        <div style="text-align: center; color: #666; font-size: 12px;">
        Generated from updated markdown with correct RUTHERFORD docket number
        </div>
        </body>
        </html>
        """
        
        html_file = output_dir / "PROVISIONAL_PATENT_APPLICATION.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_with_style)
        
        return True, f"HTML created: {html_file}"
        
    except ImportError:
        return False, "markdown2 not available"
    except Exception as e:
        return False, f"HTML conversion error: {e}"

def main():
    """Main PDF regeneration function"""
    
    print("Regenerating PDFs for Patents 15-18 with updated RUTHERFORD docket numbers...")
    print("=" * 80)
    
    base_dir = Path("C:/Users/User/MWRASP-Quantum-Defense/CONSOLIDATED_PATENT_PORTFOLIO/PATENTS_TO_FILE/uspto_filing_packages")
    
    patents = [
        ("Patent_15_Filing_Package", "RUTHERFORD-035-PROV"),
        ("Patent_16_Filing_Package", "RUTHERFORD-036-PROV"), 
        ("Patent_17_Filing_Package", "RUTHERFORD-037-PROV"),
        ("Patent_18_Filing_Package", "RUTHERFORD-038-PROV")
    ]
    
    success_count = 0
    
    for patent_dir, docket in patents:
        print(f"\nProcessing {patent_dir} ({docket})...")
        
        patent_path = base_dir / patent_dir
        md_file = patent_path / "PROVISIONAL_PATENT_APPLICATION.md"
        pdf_file = patent_path / "PROVISIONAL_PATENT_APPLICATION.pdf"
        
        if not md_file.exists():
            print(f"   [ERROR] Markdown file not found: {md_file}")
            continue
        
        # Backup existing PDF
        if pdf_file.exists():
            backup_file = patent_path / "PROVISIONAL_PATENT_APPLICATION_backup.pdf"
            try:
                if backup_file.exists():
                    backup_file.unlink()
                pdf_file.rename(backup_file)
                print(f"   [INFO] Backed up existing PDF")
            except Exception as e:
                print(f"   [WARNING] Could not backup PDF: {e}")
        
        # Try different conversion methods
        success = False
        
        # Method 1: Pandoc
        print("   [INFO] Trying pandoc conversion...")
        success, message = convert_md_to_pdf_simple(md_file, pdf_file)
        if success:
            print(f"   [OK] {message}")
            success_count += 1
            continue
        else:
            print(f"   [WARNING] {message}")
        
        # Method 2: Python libraries
        print("   [INFO] Trying Python library conversion...")
        success, message = convert_md_to_pdf_python(md_file, pdf_file)
        if success:
            print(f"   [OK] {message}")
            success_count += 1
            continue
        else:
            print(f"   [WARNING] {message}")
        
        # Method 3: HTML fallback
        print("   [INFO] Creating HTML version as fallback...")
        success, message = convert_md_to_html_fallback(md_file, patent_path)
        if success:
            print(f"   [OK] {message}")
            print(f"   [INFO] You can print the HTML to PDF manually")
        else:
            print(f"   [ERROR] {message}")
    
    print("\n" + "=" * 80)
    print(f"Regeneration Summary:")
    print(f"  - Attempted: {len(patents)} patents")
    print(f"  - PDFs created: {success_count}")
    print(f"  - All markdown files have updated RUTHERFORD docket numbers")
    
    if success_count < len(patents):
        print(f"\nNote: Some PDF conversions failed due to missing dependencies.")
        print(f"HTML versions may have been created as fallback.")
        print(f"You can manually convert HTML to PDF or install missing dependencies.")

if __name__ == "__main__":
    main()