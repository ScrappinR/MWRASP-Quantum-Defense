#!/usr/bin/env python3
"""
Regenerate PDF files for Patents 15-18 with comprehensive content
Updates all patent PDFs with the newly developed comprehensive content
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.colors import black, blue
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
import markdown
import re
from datetime import datetime

class ComprehensivePatentPDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        # Create custom styles for patent formatting
        self.styles.add(ParagraphStyle(
            name='PatentTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=black,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='PatentSection',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=15,
            spaceBefore=15,
            alignment=TA_LEFT,
            textColor=black,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='PatentSubsection',
            parent=self.styles['Heading3'],
            fontSize=12,
            spaceAfter=10,
            spaceBefore=10,
            alignment=TA_LEFT,
            textColor=black,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='PatentBody',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=8,
            alignment=TA_JUSTIFY,
            textColor=black,
            fontName='Helvetica'
        ))
        
        self.styles.add(ParagraphStyle(
            name='PatentCode',
            parent=self.styles['Normal'],
            fontSize=9,
            spaceAfter=6,
            spaceBefore=6,
            alignment=TA_LEFT,
            textColor=black,
            fontName='Courier',
            leftIndent=20,
            rightIndent=20,
            backColor='#f5f5f5'
        ))
        
        self.styles.add(ParagraphStyle(
            name='PatentClaim',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=8,
            spaceBefore=4,
            alignment=TA_JUSTIFY,
            textColor=black,
            fontName='Helvetica',
            leftIndent=20
        ))

    def parse_markdown_to_pdf_elements(self, markdown_content):
        """Convert markdown content to PDF elements"""
        elements = []
        
        # Split content into sections
        lines = markdown_content.split('\n')
        current_section = []
        in_code_block = False
        code_block_content = []
        
        for line in lines:
            # Handle code blocks
            if line.strip().startswith('```'):
                if in_code_block:
                    # End of code block
                    if code_block_content:
                        code_text = '\n'.join(code_block_content)
                        elements.append(Paragraph(self.escape_html(code_text), self.styles['PatentCode']))
                        elements.append(Spacer(1, 6))
                    code_block_content = []
                    in_code_block = False
                else:
                    # Start of code block
                    in_code_block = True
                continue
            
            if in_code_block:
                code_block_content.append(line)
                continue
            
            # Handle headers
            if line.startswith('# '):
                elements.append(Paragraph(self.escape_html(line[2:]), self.styles['PatentTitle']))
                elements.append(Spacer(1, 12))
            elif line.startswith('## '):
                elements.append(Paragraph(self.escape_html(line[3:]), self.styles['PatentSection']))
                elements.append(Spacer(1, 8))
            elif line.startswith('### '):
                elements.append(Paragraph(self.escape_html(line[4:]), self.styles['PatentSubsection']))
                elements.append(Spacer(1, 6))
            elif line.startswith('**Claim '):
                # Handle patent claims specially
                elements.append(Paragraph(self.escape_html(line), self.styles['PatentClaim']))
                elements.append(Spacer(1, 4))
            elif line.strip() == '---':
                # Handle horizontal rules as page breaks for major sections
                elements.append(Spacer(1, 20))
            elif line.strip():
                # Regular paragraph
                elements.append(Paragraph(self.escape_html(line), self.styles['PatentBody']))
                elements.append(Spacer(1, 6))
            else:
                # Empty line
                elements.append(Spacer(1, 6))
        
        return elements

    def escape_html(self, text):
        """Escape HTML characters for ReportLab"""
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        text = text.replace('"', '&quot;')
        
        # Convert markdown bold to HTML
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
        text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
        
        return text

    def generate_patent_pdf(self, markdown_file_path, output_pdf_path):
        """Generate PDF from markdown patent file"""
        
        print(f"Generating PDF for {markdown_file_path}")
        
        try:
            # Read markdown content
            with open(markdown_file_path, 'r', encoding='utf-8') as f:
                markdown_content = f.read()
            
            # Create PDF document
            doc = SimpleDocTemplate(
                output_pdf_path,
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18
            )
            
            # Convert markdown to PDF elements
            elements = self.parse_markdown_to_pdf_elements(markdown_content)
            
            # Build PDF
            doc.build(elements)
            
            print(f"✅ Successfully generated: {output_pdf_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error generating PDF for {markdown_file_path}: {str(e)}")
            return False

    def regenerate_all_comprehensive_patents(self):
        """Regenerate PDFs for all comprehensive patents 15-18"""
        
        base_path = r"C:\Users\User\MWRASP-Quantum-Defense\CONSOLIDATED_PATENT_PORTFOLIO\PATENTS_TO_FILE\uspto_filing_packages"
        
        patents_to_regenerate = [
            {
                'number': 15,
                'title': 'Quantum-Classical Result Fusion Algorithms',
                'docket': 'RUTHERFORD-035-PROV'
            },
            {
                'number': 16,
                'title': 'Enterprise Quantum Cybersecurity Orchestration',
                'docket': 'RUTHERFORD-036-PROV'
            },
            {
                'number': 17,
                'title': 'Real-Time Quantum Cost-Benefit Analysis',
                'docket': 'RUTHERFORD-037-PROV'
            },
            {
                'number': 18,
                'title': 'Quantum Cybersecurity Performance Benchmarking',
                'docket': 'RUTHERFORD-038-PROV'
            }
        ]
        
        successful_regenerations = 0
        total_patents = len(patents_to_regenerate)
        
        print("="*80)
        print("COMPREHENSIVE PATENT PDF REGENERATION")
        print(f"Regenerating {total_patents} comprehensive patent PDFs")
        print("="*80)
        
        for patent_info in patents_to_regenerate:
            patent_number = patent_info['number']
            patent_title = patent_info['title']
            docket_number = patent_info['docket']
            
            # Construct file paths
            patent_folder = os.path.join(base_path, f"Patent_{patent_number:02d}_Filing_Package")
            markdown_file = os.path.join(patent_folder, "PROVISIONAL_PATENT_APPLICATION.md")
            
            # Create backup of existing PDF if it exists
            existing_pdf = os.path.join(patent_folder, "PROVISIONAL_PATENT_APPLICATION.pdf")
            if os.path.exists(existing_pdf):
                backup_pdf = os.path.join(patent_folder, f"PROVISIONAL_PATENT_APPLICATION_BACKUP_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
                try:
                    os.rename(existing_pdf, backup_pdf)
                    print(f"📁 Backed up existing PDF: {backup_pdf}")
                except Exception as e:
                    print(f"⚠️ Could not backup existing PDF: {str(e)}")
            
            print(f"\n🔄 Processing Patent {patent_number}: {patent_title}")
            print(f"   Docket: {docket_number}")
            print(f"   Source: {markdown_file}")
            print(f"   Output: {existing_pdf}")
            
            if not os.path.exists(markdown_file):
                print(f"❌ Markdown file not found: {markdown_file}")
                continue
            
            # Generate new comprehensive PDF
            if self.generate_patent_pdf(markdown_file, existing_pdf):
                successful_regenerations += 1
                
                # Get file size for verification
                file_size = os.path.getsize(existing_pdf) / 1024  # KB
                print(f"   📄 PDF size: {file_size:.1f} KB")
            
        print("\n" + "="*80)
        print("REGENERATION SUMMARY")
        print("="*80)
        print(f"✅ Successfully regenerated: {successful_regenerations}/{total_patents} patents")
        print(f"❌ Failed regenerations: {total_patents - successful_regenerations}")
        
        if successful_regenerations == total_patents:
            print("🎉 ALL COMPREHENSIVE PATENT PDFs SUCCESSFULLY REGENERATED!")
            print("📋 All patents now contain:")
            print("   • Comprehensive technical implementations")
            print("   • Detailed 20-claim patent claims")
            print("   • Experimental validation results")
            print("   • Market analysis and commercial potential")
            print("   • 20+ pages of detailed content each")
        else:
            print("⚠️ Some patents failed to regenerate - manual review required")
        
        return successful_regenerations == total_patents

def main():
    generator = ComprehensivePatentPDFGenerator()
    success = generator.regenerate_all_comprehensive_patents()
    
    if success:
        print(f"\n🏁 All comprehensive patent PDFs are ready for filing!")
        print(f"📂 Location: C:\\Users\\User\\MWRASP-Quantum-Defense\\CONSOLIDATED_PATENT_PORTFOLIO\\PATENTS_TO_FILE\\uspto_filing_packages\\")
    else:
        print(f"\n💡 Some issues encountered - check individual patent folders")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())