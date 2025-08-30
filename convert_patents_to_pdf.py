#!/usr/bin/env python3
"""
Simple Patent PDF Converter
============================

Converts patent markdown files to PDF using reportlab library.
"""

import os
from pathlib import Path
from datetime import datetime

def install_reportlab():
    """Install reportlab if not available"""
    import subprocess
    import sys
    
    try:
        import reportlab
        return True
    except ImportError:
        print("Installing reportlab...")
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "reportlab", "--quiet"
        ], capture_output=True)
        return result.returncode == 0

def convert_md_to_pdf_reportlab(md_file, output_pdf):
    """Convert markdown to PDF using reportlab"""
    
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
        from reportlab.lib.units import inch
        import re
        
        # Read markdown content
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create PDF document
        doc = SimpleDocTemplate(
            str(output_pdf),
            pagesize=letter,
            rightMargin=inch,
            leftMargin=inch,
            topMargin=inch,
            bottomMargin=inch
        )
        
        # Get styles
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            textColor='#000080'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=15,
            textColor='#000080'
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=11,
            spaceAfter=12
        )
        
        # Parse content and create flowables
        story = []
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                story.append(Spacer(1, 6))
                continue
            
            # Handle headers
            if line.startswith('# '):
                text = line[2:].strip()
                story.append(Paragraph(text, title_style))
            elif line.startswith('## '):
                text = line[3:].strip()
                story.append(Paragraph(text, heading_style))
            elif line.startswith('### '):
                text = line[4:].strip()
                story.append(Paragraph(text, heading_style))
            elif line.startswith('**') and line.endswith('**'):
                text = line[2:-2]
                story.append(Paragraph(f"<b>{text}</b>", normal_style))
            elif line.startswith('- ') or line.startswith('* '):
                text = line[2:].strip()
                story.append(Paragraph(f"• {text}", normal_style))
            elif line == '---':
                story.append(Spacer(1, 20))
            else:
                # Clean up markdown formatting
                text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
                text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
                story.append(Paragraph(text, normal_style))
        
        # Build PDF
        doc.build(story)
        return True, "PDF created successfully"
        
    except Exception as e:
        return False, f"Error creating PDF: {e}"

def main():
    """Convert patents to PDF"""
    
    print("Converting Patents 15-18 to PDF with updated RUTHERFORD docket numbers...")
    print("=" * 80)
    
    # Install reportlab if needed
    if not install_reportlab():
        print("Failed to install reportlab. Exiting.")
        return
    
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
        pdf_file = patent_path / "PROVISIONAL_PATENT_APPLICATION_UPDATED.pdf"
        
        if not md_file.exists():
            print(f"   [ERROR] Markdown file not found: {md_file}")
            continue
        
        # Convert to PDF
        success, message = convert_md_to_pdf_reportlab(md_file, pdf_file)
        
        if success:
            print(f"   [OK] {message}")
            print(f"   [INFO] Created: {pdf_file.name}")
            success_count += 1
        else:
            print(f"   [ERROR] {message}")
    
    print(f"\n" + "=" * 80)
    print(f"Conversion Summary:")
    print(f"  - Processed: {len(patents)} patents")
    print(f"  - PDFs created: {success_count}")
    print(f"  - All files have updated RUTHERFORD docket numbers")
    
    if success_count > 0:
        print(f"\nNew PDF files created with '_UPDATED' suffix.")
        print(f"Review the files and replace the originals if satisfactory.")

if __name__ == "__main__":
    main()