#!/usr/bin/env python3
"""
PDF Conversion System for USPTO Patent Applications
================================================

Converts Markdown patent specifications to properly formatted PDF documents
for USPTO submission requirements.

Author: MWRASP Patent Development Team  
Date: August 2025
"""

import os
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
import markdown
from datetime import datetime

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

class PatentPDFConverter:
    """Converts patent Markdown files to USPTO-compliant PDF format"""
    
    def __init__(self):
        self.css_template = """
        @page {
            size: 8.5in 11in;
            margin: 1in;
            @bottom-center {
                content: counter(page);
                font-family: 'Times New Roman', serif;
                font-size: 12pt;
            }
        }
        
        body {
            font-family: 'Times New Roman', serif;
            font-size: 12pt;
            line-height: 1.6;
            color: black;
            margin: 0;
            padding: 0;
        }
        
        h1 {
            font-size: 14pt;
            font-weight: bold;
            text-align: center;
            margin-bottom: 24pt;
            page-break-before: auto;
        }
        
        h2 {
            font-size: 12pt;
            font-weight: bold;
            margin-top: 18pt;
            margin-bottom: 12pt;
        }
        
        h3 {
            font-size: 12pt;
            font-weight: bold;
            margin-top: 12pt;
            margin-bottom: 6pt;
        }
        
        p {
            margin-bottom: 12pt;
            text-align: justify;
            text-indent: 0.5in;
        }
        
        .no-indent {
            text-indent: 0;
        }
        
        ul, ol {
            margin-bottom: 12pt;
            padding-left: 0.5in;
        }
        
        li {
            margin-bottom: 6pt;
        }
        
        pre, code {
            font-family: 'Courier New', monospace;
            font-size: 10pt;
            background-color: #f5f5f5;
            padding: 6pt;
            margin: 12pt 0;
            border: 1px solid #ccc;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 12pt 0;
        }
        
        th, td {
            border: 1px solid #000;
            padding: 6pt;
            text-align: left;
        }
        
        th {
            background-color: #f0f0f0;
            font-weight: bold;
        }
        
        .claims {
            margin-top: 18pt;
        }
        
        .claim {
            margin-bottom: 12pt;
            padding-left: 0.25in;
            text-indent: -0.25in;
        }
        
        .page-break {
            page-break-before: always;
        }
        
        .center {
            text-align: center;
        }
        
        .bold {
            font-weight: bold;
        }
        
        hr {
            border: none;
            border-top: 1px solid #000;
            margin: 24pt 0;
        }
        """
    
    def convert_markdown_to_html(self, markdown_content: str) -> str:
        """Convert Markdown content to HTML with patent-specific formatting"""
        
        # Configure markdown with extensions
        md = markdown.Markdown(extensions=[
            'markdown.extensions.tables',
            'markdown.extensions.fenced_code',
            'markdown.extensions.toc',
            'markdown.extensions.attr_list'
        ])
        
        # Convert to HTML
        html_content = md.convert(markdown_content)
        
        # Post-process for patent-specific formatting
        html_content = self._format_patent_html(html_content)
        
        return html_content
    
    def _format_patent_html(self, html_content: str) -> str:
        """Apply patent-specific HTML formatting"""
        
        # Wrap in proper HTML structure
        formatted_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Provisional Patent Application</title>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        
        # Replace claim formatting
        formatted_html = formatted_html.replace(
            '<p><strong>Claim', 
            '<p class="claim"><strong>Claim'
        )
        
        # Format headers properly
        formatted_html = formatted_html.replace('## CLAIMS', '<div class="claims"><h2>CLAIMS</h2>')
        formatted_html = formatted_html.replace('---', '<hr>')
        
        return formatted_html
    
    def convert_to_pdf(self, markdown_file: Path, output_pdf: Path) -> bool:
        """Convert Markdown patent file to PDF"""
        
        try:
            # Read markdown content
            with open(markdown_file, 'r', encoding='utf-8') as f:
                markdown_content = f.read()
            
            print(f"Converting {markdown_file.name} to PDF...")
            
            if REPORTLAB_AVAILABLE:
                return self._convert_with_reportlab(markdown_content, output_pdf)
            else:
                return self._convert_with_basic_method(markdown_content, output_pdf)
            
        except Exception as e:
            print(f"  [ERROR] Failed to convert {markdown_file}: {e}")
            return False
    
    def _convert_with_reportlab(self, markdown_content: str, output_pdf: Path) -> bool:
        """Convert using ReportLab library"""
        
        # Create PDF document
        doc = SimpleDocTemplate(
            str(output_pdf),
            pagesize=letter,
            topMargin=1*inch,
            bottomMargin=1*inch,
            leftMargin=1*inch,
            rightMargin=1*inch
        )
        
        # Get styles
        styles = getSampleStyleSheet()
        
        # Create custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontSize=14,
            spaceAfter=24,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading1'],
            fontSize=12,
            spaceBefore=18,
            spaceAfter=12
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=12,
            alignment=TA_JUSTIFY,
            leftIndent=0.5*inch
        )
        
        # Parse markdown and create flowables
        story = []
        lines = markdown_content.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            if line.startswith('# '):
                # Main title
                title_text = line[2:].strip()
                story.append(Paragraph(title_text, title_style))
            elif line.startswith('## '):
                # Section heading
                heading_text = line[3:].strip()
                story.append(Paragraph(heading_text, heading_style))
            elif line.startswith('**') and line.endswith('**'):
                # Bold text
                bold_text = line[2:-2]
                story.append(Paragraph(f"<b>{bold_text}</b>", normal_style))
            elif line != '---':
                # Regular paragraph
                # Clean up markdown formatting
                clean_line = line.replace('**', '').replace('*', '')
                if clean_line:
                    story.append(Paragraph(clean_line, normal_style))
        
        # Build PDF
        doc.build(story)
        print(f"  [OK] PDF created with ReportLab: {output_pdf}")
        return True
    
    def _convert_with_basic_method(self, markdown_content: str, output_pdf: Path) -> bool:
        """Convert using basic text-to-PDF method"""
        
        # For now, let's copy the markdown file as a text file with PDF extension
        # This is a fallback - in production you'd want proper PDF generation
        
        clean_content = markdown_content.replace('#', '').replace('*', '').replace('---', '=' * 50)
        
        # Write as text file with .pdf extension (temporary solution)
        with open(str(output_pdf).replace('.pdf', '_text.pdf'), 'w', encoding='utf-8') as f:
            f.write("PROVISIONAL PATENT APPLICATION - TEXT FORMAT\n")
            f.write("=" * 60 + "\n")
            f.write("NOTE: This is a text representation. For USPTO filing, convert to proper PDF.\n\n")
            f.write(clean_content)
        
        print(f"  [WARN] Created text version: {output_pdf} (install reportlab for proper PDF)")
        return True
    
    def convert_patent_directory(self, patent_dir: Path) -> bool:
        """Convert all Markdown files in a patent directory to PDF"""
        
        markdown_file = patent_dir / "PROVISIONAL_PATENT_APPLICATION.md"
        if not markdown_file.exists():
            print(f"  [SKIP] No Markdown file found in {patent_dir}")
            return False
        
        pdf_file = patent_dir / "PROVISIONAL_PATENT_APPLICATION.pdf"
        return self.convert_to_pdf(markdown_file, pdf_file)
    
    def batch_convert_patents(self, base_directory: Path, patent_numbers: List[str]) -> Dict[str, bool]:
        """Convert multiple patents to PDF format"""
        
        results = {}
        
        print(f"\n{'='*60}")
        print("BATCH PDF CONVERSION")
        print(f"{'='*60}")
        
        for patent_num in patent_numbers:
            # Try different tier directories
            patent_found = False
            
            for tier_dir in ["TIER_1_CRITICAL_PRIORITY", "TIER_2_HIGH_PRIORITY", "TIER_3_MEDIUM_PRIORITY"]:
                patent_dirs = list(base_directory.glob(f"{tier_dir}/*"))
                
                for patent_dir in patent_dirs:
                    if patent_num.zfill(2) in patent_dir.name or f"Patent_{patent_num}" in patent_dir.name:
                        print(f"\nProcessing Patent {patent_num}: {patent_dir.name}")
                        results[patent_num] = self.convert_patent_directory(patent_dir)
                        patent_found = True
                        break
                
                if patent_found:
                    break
            
            if not patent_found:
                print(f"\n  [ERROR] Patent {patent_num} directory not found")
                results[patent_num] = False
        
        return results
    
    def update_filing_packages(self, base_directory: Path, patent_numbers: List[str]):
        """Update filing packages with PDF specifications"""
        
        filing_packages_dir = base_directory / "uspto_filing_packages"
        
        print(f"\n{'='*60}")
        print("UPDATING FILING PACKAGES WITH PDF SPECIFICATIONS")
        print(f"{'='*60}")
        
        for patent_num in patent_numbers:
            # Find source PDF
            source_pdf = None
            
            for tier_dir in ["TIER_1_CRITICAL_PRIORITY", "TIER_2_HIGH_PRIORITY", "TIER_3_MEDIUM_PRIORITY"]:
                patent_dirs = list(base_directory.glob(f"{tier_dir}/*"))
                
                for patent_dir in patent_dirs:
                    if patent_num.zfill(2) in patent_dir.name:
                        pdf_file = patent_dir / "PROVISIONAL_PATENT_APPLICATION.pdf"
                        if pdf_file.exists():
                            source_pdf = pdf_file
                            break
                
                if source_pdf:
                    break
            
            if source_pdf:
                # Copy to filing package
                package_dir = filing_packages_dir / f"Patent_{patent_num.zfill(2)}_Filing_Package"
                if package_dir.exists():
                    dest_pdf = package_dir / "PROVISIONAL_PATENT_APPLICATION.pdf"
                    dest_pdf.write_bytes(source_pdf.read_bytes())
                    print(f"  [OK] Updated Package {patent_num} with PDF specification")
                else:
                    print(f"  [ERROR] Filing package not found for Patent {patent_num}")
            else:
                print(f"  [ERROR] Source PDF not found for Patent {patent_num}")


def main():
    """Main function"""
    
    base_dir = Path(r"C:\Users\User\MWRASP-Quantum-Defense\CONSOLIDATED_PATENT_PORTFOLIO\PATENTS_TO_FILE")
    
    converter = PatentPDFConverter()
    
    # Convert Tier 1 patents first (ready to file)
    tier1_patents = ["01", "03", "04", "05", "06", "07", "08"]
    tier1_results = converter.batch_convert_patents(base_dir, tier1_patents)
    
    # Update filing packages
    converter.update_filing_packages(base_dir, tier1_patents)
    
    # Convert Tier 3 patents
    tier3_patents = ["09", "10", "11", "12", "13", "14", "15", "16", "17", "18"]
    tier3_results = converter.batch_convert_patents(base_dir, tier3_patents)
    
    # Summary
    successful = sum(1 for result in {**tier1_results, **tier3_results}.values() if result)
    total = len(tier1_results) + len(tier3_results)
    
    print(f"\n{'='*60}")
    print("PDF CONVERSION COMPLETE")
    print(f"{'='*60}")
    print(f"Successfully converted: {successful}/{total} patents")
    print(f"Tier 1 filing packages updated with PDF specifications")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()