#!/usr/bin/env python3
"""
Simple PDF regeneration for Patents 15-18 with comprehensive content
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.colors import black, blue
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
import re
from datetime import datetime

class PatentPDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        self.styles.add(ParagraphStyle(
            name='PatentTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='PatentSection',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=15,
            spaceBefore=15,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='PatentBody',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=8,
            alignment=TA_JUSTIFY,
            fontName='Helvetica'
        ))

    def escape_html(self, text):
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
        return text

    def generate_patent_pdf(self, markdown_file_path, output_pdf_path):
        try:
            with open(markdown_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            doc = SimpleDocTemplate(output_pdf_path, pagesize=letter, 
                                  rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
            
            elements = []
            lines = content.split('\n')
            
            for line in lines:
                line = line.strip()
                if not line:
                    elements.append(Spacer(1, 6))
                elif line.startswith('# '):
                    elements.append(Paragraph(self.escape_html(line[2:]), self.styles['PatentTitle']))
                    elements.append(Spacer(1, 12))
                elif line.startswith('## '):
                    elements.append(Paragraph(self.escape_html(line[3:]), self.styles['PatentSection']))
                    elements.append(Spacer(1, 8))
                elif line.startswith('### '):
                    elements.append(Paragraph(self.escape_html(line[4:]), self.styles['PatentSection']))
                    elements.append(Spacer(1, 6))
                elif line == '---':
                    elements.append(Spacer(1, 20))
                else:
                    elements.append(Paragraph(self.escape_html(line), self.styles['PatentBody']))
                    elements.append(Spacer(1, 4))
            
            doc.build(elements)
            return True
            
        except Exception as e:
            print(f"Error generating PDF: {str(e)}")
            return False

def main():
    generator = PatentPDFGenerator()
    base_path = r"C:\Users\User\MWRASP-Quantum-Defense\CONSOLIDATED_PATENT_PORTFOLIO\PATENTS_TO_FILE\uspto_filing_packages"
    
    patents = [15, 16, 17, 18]
    successful = 0
    
    print("Regenerating comprehensive patent PDFs...")
    
    for patent_num in patents:
        patent_folder = os.path.join(base_path, f"Patent_{patent_num:02d}_Filing_Package")
        markdown_file = os.path.join(patent_folder, "PROVISIONAL_PATENT_APPLICATION.md")
        pdf_file = os.path.join(patent_folder, "PROVISIONAL_PATENT_APPLICATION_COMPREHENSIVE.pdf")
        
        print(f"Processing Patent {patent_num}...")
        
        if os.path.exists(markdown_file):
            if generator.generate_patent_pdf(markdown_file, pdf_file):
                file_size = os.path.getsize(pdf_file) / 1024
                print(f"  Success! PDF size: {file_size:.1f} KB")
                successful += 1
            else:
                print(f"  Failed to generate PDF")
        else:
            print(f"  Markdown file not found: {markdown_file}")
    
    print(f"\nCompleted: {successful}/{len(patents)} patents successfully regenerated")
    return successful == len(patents)

if __name__ == "__main__":
    success = main()
    if success:
        print("All comprehensive patent PDFs generated successfully!")
    else:
        print("Some errors occurred during PDF generation")